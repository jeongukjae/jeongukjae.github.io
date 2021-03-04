---
layout: post
title: "TensorFlow Custom Op으로 데이터 변환 최적화하기; 4.697ms → 17.147μs"
author:
  - 정욱재
  - 홍승환
tags:
  - scatterlab
  - tensorflow
---

***[핑퐁팀 블로그](https://blog.pingpong.us/)에 업로드했던 "TensorFlow Custom Op으로 데이터 변환 최적화하기"글입니다. 제가 [홍승환](https://github.com/harrydrippin)님과 같이 작성한 글이기 때문에 이 블로그에 아카이브합니다.***

---

{% include image.html url="/images/2021/01-07-custom-op/preview.png" description="Great TF Custom Ops, That Was Fast" width=70 %}

핑퐁팀에서는 모델 학습의 효율성을 위해 자주 TFRecord를 생성합니다. 하지만 정제할 데이터가 많은 경우에는 변환이 느려지고, 속도 최적화가 필요합니다. 이 때의 병목점을 Custom Op으로 교체하면 처리 속도를 매우 빠르게 만들 수 있습니다.
실제로 이번 최적화를 통해 한 문장 당 4.697ms가 소요되던 병목점이 약 250배 빨라져 17.147μs 정도로 줄었는데, 이번 포스트에서 그 방법에 대해 자세하게 다루어보겠습니다.

## Custom Op

**Custom Op은 TensorFlow C++ Library 기능을 이용하여 직접 작성하는 Operation을 말합니다.**

대부분 C++을 이용하여 작성하기 때문에 리소스가 더 많이 들지만, 매우 효율적인 Operation을 작성할 수 있습니다. TensorFlow 문서에서는 다음과 같은 상황에 사용할 수 있다고 설명되어 있습니다.

1. 이미 존재하는 Op으로 원하는 Operation을 표현하기 어려운 경우
2. 이미 존재하는 Op으로 나타낼 때 비효율적인 경우
3. 직접 Operation을 Fusing하고 싶은 경우

해당 Custom Op을 사용하는 방법은 아래와 같습니다.

1. C++ 파일로 Op 작성
2. (선택) Gradient 함수 작성
3. Op 테스트

Custom Op은 Bazel이 설치되어 있다면 편하게 빌드할 수도 있지만, Bazel이 없더라도 기본 `g++` 혹은 `clang++`만으로도 빌드할 수 있습니다. 이 포스트에서는 `g++` 또는 `clang++`로 빌드하는 것을 기본으로 설명합니다.

## 우리의 상황

핑퐁팀은 매우 많은 양의 코퍼스를 보유하고 있습니다. 해당 코퍼스를 이용해 TPU에서 Large-scale Language Model을 학습하려 할 때 데이터 정제 및 전처리/변환이 필요한데, 변환 후의 결과물을 TFRecord로 만들기를 원하는 상황이었습니다.
즉, 만들어져야 할 TFRecord는 아래와 같습니다. (자세한 사항은 BERT 논문 또는 [카톡 대화 데이터를 BERT로 잘 학습시킬 수 있을까? - Dialog-BERT 만들기 3편](https://blog.pingpong.us/dialog-bert-pretrain/) 포스트를 참고하시길 바랍니다)

- Bert Input: input_ids, attention_mask와 같은 Bert에 필요한 입력값
- Masking Positions: 마스킹할 위치
- NSP(Next Sentence Prediction) or SOP(Sentence Order Prediction)에 필요한 레이블

마스킹된 입력 값을 바로 만들지 않고 마스킹할 위치를 받는 이유는 여러 Epoch을 돌면서 각각 다른 위치에 마스킹이 되게 하기 위해서입니다.
그와 동시에 모델의 성능을 위해 ALBERT의 데이터처럼 N-gram Masking을 적용하기로 했습니다.

공개된 ALBERT 코드와 비슷하게 아래처럼 Masking할 곳의 값을 구했습니다.

1. 주어진 Sequence를 확률에 따라 n-gram으로 나눔
2. 나누어진 Sequences를 전부 Shuffle
3. Masking할 토큰의 개수만큼 Masking

위와 같은 알고리즘으로 TensorFlow 코드를 작성할 때 데이터 변환 소요 시간의 절반 이상이 마스킹할 위치를 골라내는데 소요되었습니다.

### TensorFlow Op을 이용하여 작성한 코드

이해를 위해 간단한 형태의 코드와 주석으로 표현하겠습니다.

```python
def get_masking_positions(maskable_positions, num_tokens_to_mask, max_n):
    """
    주어진 maskable_positions에 대해 num_tokens_to_mask만큼 마스킹할 위치를 구하는 함수

    Args:
        maskable_positions: 마스킹 가능한 위치를 담는 텐서 (tf.Tensor, shape: (SequenceLength,))
        num_tokens_to_mask: 최대로 마스킹할 토큰 개수 (Scalar)
        max_n: 최대로 연속하여 마스킹할 토큰 개수 (Scalar)

    Return:
        masking_positions: 마스킹할 포지션 (tf.Tensor, shape: (SequenceLength,))
    """
    # 실제로 마스킹할 수 있는 값만큼 루프를 돌았는지 테스트 (특수 토큰, Padding을 제외한 위치)
    while_condition = lambda idx, _: idx < tf.size(maskable_positions)

    def while_body(idx, mask_candidates):
        # 1. 확률적으로 n 값을 구한 다음 n-gram만큼 자름
        # 2. mask candidates에 추가
        # ...

    idx, mask_candidates = tf.while_loop(
        while_condition,
        while_body,
        # ...
    )

    shuffled = tf.random.shuffle(mask_candidates)

    # 이후 필요한 만큼 shuffled의 앞쪽부터 사용함
    # ...
```

### Custom Op으로 작성하기

이제 위의 Python 코드와 동일한 역할을 하는 Custom Op을 작성해보겠습니다.
Custom Ops는 C++로 작성되고, 그 이후에 Shared Object로 컴파일되어 TensorFlow 코드에서 불러오게 됩니다.

#### REGISTER_OP

우선 Op의 Metadata를 다음과 같이 작성합니다.

```c++
REGISTER_OP("GetMaskingPosition")
    .Input("maskable_positions: float32")
    .Input("max_n: int32")
    .Input("num_tokens_to_mask: int32")
    .Output("masking_position: float32")
    .Attr("seed: int = 23")
    .Doc(R"doc(
마스킹 가능한 부분이 추출된 maskable_positions에서 확률적으로 ngram masking하는 Op입니다.
)doc")
    .SetShapeFn([](::tensorflow::shape_inference::InferenceContext* c) {
      c->set_output(0, c->input(0));
      return Status::OK();
    });
```

Op의 이름과 Input, Output, Attribute (Python의 Keyword Argument), 그리고 Doc을 기술합니다.
또한, `SetShapeFn`에서 Input Shape으로부터 Output Shape을 도출해내는 함수를 작성하여 넘겨줍니다.

#### OpKernel 클래스 작성

그 다음은 실제 Op의 구현체인 클래스를 명시합니다.

```c++
class GetMaskingPositionOp : public OpKernel {
 public:
  void Compute(OpKernelContext* context) override {
    // Ops 구현을 여기에 넣습니다.
  }
}
```

`OpKernel` 클래스를 상속받는 클래스를 만들고, `Compute()` 함수를 오버라이딩하여 내용을 작성합니다.
Input을 가져오는 방법은 다음과 같습니다.

```c++
const Tensor& candidates_mask_tensor = context->input(0);
auto candidates_mask = candidates_mask_tensor.flat<float>();
```

OpKernelContext 객체 안에 Input이 있고, 위의 `REGISTER_OP`에서 명시한 순서대로 저장되어 있습니다.
위의 예제에서는 `context->input(0)`을 통해 0번째 Input인 `maskable_positions`의 Reference를 꺼내왔습니다.
그 후 `tensor.flat<float>()` 을 통해 내부의 값을 접근할 수 있는 Handle을 가져오고, `candidates_mask(0) = 0.0` 과 같이 내부의 값을 읽거나 쓸 수 있습니다.

이런 식으로 모든 계산을 완료하였다면, Output을 Context에 넣어주어야 합니다.
Output 역시 Input과 비슷한 방법으로 쓸 수 있습니다.

```c++
Tensor* masking_position_tensor = NULL;
OP_REQUIRES_OK(context, context->allocate_output(0, maskable_positions_tensor.shape(), &masking_position_tensor));
auto masking_position = masking_position_tensor->flat<float>();
```

우선 Tensor의 포인터를 만들고, `context->allocate_output()`을 통해 Context 객체 안에 있는 Tensor의 Reference를 방금 만든 포인터에 할당해줍니다.
그 뒤 Tensor의 포인터에 `pointer->flat<자료형>()` 함수를 실행해서 Handle을 가져오고, 그 Handle에 Output의 값을 써줄 수 있습니다.

#### REGISTER_KERNEL_BUILDER

이제 OpKernel 클래스를 모두 작성했으니, 위의 `REGISTER_OP`에 있는 Metadata와 실제 구현을 이어줄 차례입니다.
파일 최하단에 다음과 같이 선언합니다.

```c++
REGISTER_KERNEL_BUILDER(Name("GetMaskingPosition").Device(DEVICE_CPU), GetMaskingPositionOp);
```

이름이 `GetMaskingPosition`인 Op 명세를 가져와 방금 기술했던 OpKernel 클래스와 연결합니다.
여기서는 데이터 프로세싱에 사용할 Op을 만들고 있기 때문에, `Device()` 함수에 `DEVICE_CPU`를 넣습니다.
만약 GPU에서의 연산까지 포함한 Op을 만들었다면 이 시점에서 GPU용 Op으로 연결해주면 됩니다.

#### 컴파일

이제 컴파일을 통해 Shared Object를 만듭니다.
다음 명령을 통해 컴파일할 수 있습니다.

```shell
TF_CFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_compile_flags()))') )
TF_LFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_link_flags()))') )

echo "TF_CFLAGS: ${TF_CFLAGS}"
echo "TF_LFLAGS: ${TF_LFLAGS}"

g++ -std=c++11 -shared get_masking_position_op.cc -o get_masking_position_op.so -fPIC ${TF_CFLAGS[@]} ${TF_LFLAGS[@]} -O2
```

TensorFlow 안에 있는 `tf.sysconfig` 안에서 컴파일과 링킹에 필요한 인자를 받아올 수 있습니다.
`g++`를 실행할 때 이를 넘겨줌으로써 컴파일된 `.so` 파일을 얻을 수 있습니다.

#### Python에서 로딩하기

이제 만들어진 Shared Object를 Python에서 로딩해서 사용할 수 있습니다.
다음과 같이 로딩할 수 있습니다.

```python
import tensorflow as tf

GET_MASKING_POSITION_OP_PATH = "get_masking_position_op.so"

get_masking_position = tf.load_op_library(GET_MASKING_POSITION_OP_PATH).get_masking_position

# 아래와 같이 함수처럼 사용합니다.
get_masking_position(inputs, max_n=max_n, num_tokens_to_mask=num_tokens_to_mask)
```

`tf.load_op_library()` 함수에 `.so` 파일의 위치를 넘겨서 불러오고, 안에 있는 함수를 잡아줍니다.
`PascalCase`로 작성한 이름이 `snake_case`로 바뀌어 있으므로 이 점에 유의하여 불러와야 합니다.

더욱 자세한 내용은 [TensorFlow의 공식 가이드](https://www.tensorflow.org/guide/create_op)에서 찾아보실 수 있습니다.

### 속도

아래와 같은 코드로 실제 TensorFlow Operation과 C++로 작성된 Custom Op의 속도를 비교해보았습니다.

```python
import os
import timeit
import tensorflow as tf

from xxx import masking_fn # tf function으로 작성된 함수 불러오기

ops_so_file = os.path.join(os.path.dirname(__file__), "ops", "get_masking_position_op.so")
get_masking_position = tf.load_op_library(ops_so_file).get_masking_position


if __name__ == "__main__":
    # 0.2, 0.8의 확률로 sequence length 128인 입력값을 랜덤으로 생성
    maskable_positions = tf.cast(tf.random.categorical(tf.math.log([[0.2, 0.8]]), 128)[0], tf.float32)
    # 1인 부분의 0.2만큼만 masking
    num_tokens_to_mask = tf.cast(tf.math.reduce_sum(maskable_positions) * 0.2, tf.int32)
    # 최대 3개의 토큰까지 이어서 마스킹
    max_n = 3

    get_masking_position(maskable_positions, num_tokens_to_mask, max_n)
    masking_fn(maskable_positions, num_tokens_to_mask, max_n)

    print("Custom Op:", timeit.timeit(lambda: get_masking_position(maskable_positions, num_tokens_to_mask, max_n), number=100))
    print("TF Op:", timeit.timeit(lambda: masking_fn(maskable_positions, num_tokens_to_mask, max_n), number=100))
```

이 경우 `MacBook Pro (13-inch, 2020, Four Thunderbolt 3 ports), 2 GHz Quad-Core Intel Core i5`, `TensorFlow 2.3.1` 기준으로 아래와 같은 결과값을 볼 수 있었습니다.

```shell
$ python test.py
2020-11-18 17:41:33.572617: I tensorflow/core/platform/cpu_feature_guard.cc:142] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN)to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2020-11-18 17:41:33.586511: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x7fc543418b70 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
2020-11-18 17:41:33.586568: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
Custom Op: 0.0017147309999998583
TF Op: 0.4697395919999998
```

**같은 기능을 하면서 약 250배 빠른 성능의 Op을 얻었습니다.** 기존 TensorFlow로 작성된 Op은 한 문장을 처리하는데 약 `4.697ms` 정도 소요되는데 반해 C++로 작성된 Custom Op은 한 문장을 처리하는데 `17.147μs`만이 소요되었습니다. 제일 느린 연산이던 `masking_fn`이 C++ Custom Op으로 교체한 후 데이터 변환 연산 중 가장 빠른 연산이 되었습니다.

## 마치며

TensorFlow Custom Op은 1) Bazel을 쓰지 않는다면 유지보수를 하기 어렵고, 2) 자칫하면 Op을 제대로 이해하는데 많은 시간을 소요하고, 3) 디버깅이 어려워지는 단점이 있습니다.
이 때문에 가능하면 피해야 하지만, 필요한 곳에 사용하면 굉장히 큰 효과를 불러올 수 있습니다.

심지어 모델 연산에도 연산자를 Fusing하면서 불필요한 중간 계산값과 비효율적인 연산을 많이 없앨 수 있기 때문에 활용 가치가 큽니다.
CUDA 프로그래밍을 활용하여 Custom Op을 만들면 모델 연산 자체도 많이 최적화할 수 있을 뿐더러, Backward 연산까지 빠르게 최적화할 수 있습니다.
TensorFlow에 해당되지는 않지만, DeepSpeed가 퍼포먼스를 위해 최적화된 Transformer Kernel을 직접 작성(<https://github.com/microsoft/DeepSpeed/tree/master/csrc/transformer>)하는 것에서 알 수 있듯 중요한 모델 아키텍쳐를 Custom Op으로 작성하면 큰 효과를 볼 수 있습니다.

## 참고자료

- TensorFlow Guide - Create an op (<https://www.tensorflow.org/guide/create_op>)
- GitHub - TensorFlow/custom-op (<https://github.com/tensorflow/custom-op>)
- GitHub - Google-Research/bert (<https://github.com/google-research/bert>)
- ALBERT: A Lite BERT for Self-supervised Learning of Language Representations (<https://arxiv.org/abs/1909.11942>)
- GitHub - Google-Research/albert (<https://github.com/google-research/albert>)
- GitHub - Microsoft/DeepSpeed (<https://github.com/microsoft/DeepSpeed>)
