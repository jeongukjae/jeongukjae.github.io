---
layout: post
title: 하나의 조직에서 TensorFlow와 PyTorch 동시 활용하기
tags:
  - scatterlab
  - tensorflow
  - pytorch
featured: true
---

***[핑퐁팀 블로그](https://blog.pingpong.us/)의 [하나의 조직에서 TensorFlow와 PyTorch 동시 활용하기](https://blog.pingpong.us/torch-to-tf-tf-to-torch/)에 올라간 글입니다. 제가 작성한 글이기 때문에 이 블로그에 아카이브합니다.***

---

보통 제품이 있는 조직은 TensorFlow를, 리서치 조직은 PyTorch를 활용하는 것이 좋다고 알려져 있습니다. 그리고 하나의 조직에서는 하나의 프레임워크만 사용하는 것이 일반적이죠. 하지만 핑퐁팀의 형태는 다소 특이합니다. TensorFlow와 PyTorch를 동시에 사용하고 있습니다. 어떻게 둘 다 동시에 사용이 가능한지 소개해드리도록 하겠습니다.

## 근데 왜 TensorFlow와 PyTorch를 동시에 써요?

핑퐁팀은 작년 초까지 TensorFlow만을 사용하던 팀이었습니다. 그러던 중 리서치 조직에서 조금 더 유연한 리서치를 위해 PyTorch에 대한 수요를 말해주었고, 이 때부터는 PyTorch 하나를 사용하도록 하고 있었습니다. 하지만 대형 모델이 점점 더 많아지면서 배포가 어려워지자, 연산과 가중치가 같다면 같은 결과를 낸다는 가정하에 부분적으로 TensorFlow를 도입하기 시작하였습니다. 왜 TensorFlow가 배포에 유리한지는 아래에서 설명하겠습니다.

### 그럼 왜 PyTorch로 배포를 안했나요?

결정적인 이유는 아래정도로 요약이 가능합니다.

**우리는 배포될 서버에서 성능상의 큰 오버헤드인 Python 오버헤드를 제외하고 싶었습니다.** 많은 사람들이 Python flask와 같은 서버로 서빙을 한다고 하지만 이 때의 Python 오버헤드와 HTTP의 오버헤드는 정말 큽니다. 모델이 작은 경우에는 모델 추론 시간보다 오버헤드가 더 심한 경우도 있습니다. 이 때 사용가능한 옵션은 TensorFlow serving과 Onnx, 그리고 PyTorch의 C++ 런타임인 libtorch 정도였습니다. 현재까지 옵션을 늘리면 PyTorch Serve의 JIT 적용된 모델이 archive 된 형태가 되겠죠. 하지만 이 옵션은 그 당시 존재하지 않았습니다.

**배포 편의성이 좋아야 했고, 어느 시스템에서도 잘 구동되는 형태여야 했습니다.** 배포를 편하게 할 수 있어야 서로의 리소스를 아낄 수 있고, 모델 개발에 집중할 수 있습니다. 현재도 Cortex를 제외한다면 Onnx는 그렇다할 배포 옵션이 존재하지 않습니다. 이 때 Onnx는 옵션에서 빠지게 되었고, 도커 이미지와 모델 파일 하나로 서빙이 가능한 TensorFlow Serving만이 옵션으로 남게 되었죠.

현재 시점에서 다시 고려를 해본다면 PyTorch Serve가 대체재가 될 수 있습니다. 하지만 아직은 model archiver를 따로 돌려야 하는 점, 유연한 리서치를 위한 코드에서 TorchScript와 호환되는 코드로 다시 수정해서 유지해야하는 점을 들어보았을 때 TensorFlow Serving이 제일 합리적인 선택지로 보입니다.

TensorFlow Serving에 대해 부가설명을 해보자면 TensorFlow 기본 저장 옵션인 saved model로 저장을 할 경우 그 파일만을 이용하여 바로 GRPC/HTTP 서버를 구동할 수 있습니다. 해당 서버들은 내부적으로 Python 오버헤드는 전혀 존재하지 않으며 고성능 C++ 서버로 작성되어 있습니다.

### 그럼 TensorFlow 코드와 PyTorch 코드를 이중으로 유지해야하는 불편함이 있을 것 같아요. 이 부분에 들이는 리소스는 크지 않았나요?

이 부분이 제일 걱정이 되었습니다. 아무래도 이중으로 코드를 유지하다보면 실수할 여지가 크고, 좋은 이너소스 라이브러리로 남기 힘들다는 생각이 들었습니다. 하지만 아래 정도가 리소스를 많이 들이더라도 TensorFlow 코드를 유지하기로 마음먹은 이유가 되었습니다.

**TPU Compatible한 코드를 항상 작성할 수 있습니다.** Custom Ops만 넣지 않는다면 Strategy 변경만으로 TPU를 바로 사용할 수 있는 코드가 나옵니다. 이 부분은 대형 모델을 학습할 때 매우 큰 장점이 되었고, 따라서 핑퐁팀에서 대형 모델 학습을 시작할 때 TensorFlow 코드로 많은 부분이 옮겨졌습니다.

**대형 모델 학습 시의 데이터 파이프라인 코드가 간결해집니다.** PyTorch가 동적으로 데이터를 생성해낼 수 있다는 장점이 있지만, 자유로운만큼 버그는 증가하고 가독성은 떨어집니다. 하지만 TensorFlow는 `tf.data.Dataset`만으로 코드를 작성할 경우 모든 device(CPU, GPU, TPU)에서 작동하며 순수함수에 가깝게 작성을 할 수 있습니다.

**프로덕션과 엮여있는 모델들의 학습코드가 정말 쉬워집니다.** PyTorch를 사용할 경우 TensorFlow Keras에 버금가는 읽기 좋은, Pythonic한 학습 코드를 작성하기 위해서는 pytorch-lightning을 사용해야 합니다. 하지만 pytorch-lightning을 사용하더라도 프로덕션으로 바로 이어지기 힘드며, 위쪽의 서빙에서의 고려사항과 다시금 부딪히게 되었습니다.

## 그럼 어떻게 내부적으로 두 코드를 유지했나요?

**우선은 내부에서 사용하는 모델들을 PyTorch, TensorFlow 버전으로 재작성을 하였습니다.** PyTorch까지 재작성을 한 이유는 많은 변경을 해야하는 리서치 프로젝트에서의 고려사항이 빠진 후 최종 정리된 형태로 만들기 위함이었고 이를 기반으로 TensorFlow로 작성하였습니다. 유지보수가능한 코드를 작성하기 위해서 별도의 코드 베이스에서 작업하였습니다.

그 결과 읽기 쉬우면서도 기존 리서치 프로젝트와 호환되는 PyTorch 모델 코드가 탄생하였고, PyTorch 모델의 가중치를 옮길 대상인 TensorFlow 모델 코드도 잘 작성되었습니다. 예시로 현재 스캐터랩의 내부 라이브러리를 이용하여 아래의 코드로 같은 동작을 보장하는 TensorFlow, PyTorch용 BERT 모델을 생성할 수 있습니다.

```python
#
# TensorFlow 모델 로딩
from models.tf.language_model import LanguageModel

model = LanguageModel(vocab_size=32000, word_embedding_size=64, hidden_size=64, num_layers=4)

#
# PyTorch 모델 로딩
from models.torch.language_model import LanguageModel

model = LanguageModel(vocab_size=32000, word_embedding_size=64, hidden_size=64, num_layers=4)
```

**그 다음에는 모델의 모든 가중치를 변환해주는 코드를 추가 작성하였습니다.** 변환해야하는 상황은 1) 리서치 중 나온 PyTorch 가중치를 TensorFlow로 옮겨 배포를 해야하거나, 2) TensorFlow로 학습된 대형 모델 가중치를 리서치를 할 수 있도록 PyTorch로 옮겨주어야 했습니다. 자세한 사항은 아래에서 설명하겠습니다.

## 모델 가중치 변환

이 경우 여러가지 고려사항이 있을 수 있지만 아래정도로 압축하였습니다.

* TensorFlow Checkpoint에서 값을 로딩하여 PyTorch 모델로 적용하는 경우
* PyTorch State Dict 파일에서 값을 로딩하여 TensorFlow 모델로 적용하는 경우
* PyTorch나 TensorFlow 모델에서 다른 프레임워크의 모델로 적용하는 경우

### from TensorFlow Checkpoint to PyTorch Model

TensorFlow Checkpoint에서 PyTorch Model Weight를 만들어내는 경우에 제가 활용한 api는 아래정도입니다.

* [`tf.train.list_variables`](https://www.tensorflow.org/api_docs/python/tf/train/list_variables)
* [`tf.train.load_variable`](https://www.tensorflow.org/api_docs/python/tf/train/load_variable)

위 함수이름을 보면 예측할 수 있듯, `tf.train.list_variables`로 Checkpoint들의 값들을 확인한 다음 값들을 `tf.train.load_variable`로 로딩하여 PyTorch 모델에 적용하였습니다. `tf.train.load_variable`의 반환 타입은 `numpy.ndarray`이기 때문에 torch model로 적용하기 위해서는 `torch.from_numpy`를 호출하면 됩니다. 결론적으로 아래와 같은 방식으로 로딩이 가능합니다.

```python
# 가중치 목록 확인
# print(tf.train.list_variables("checkpoint-path"))
weight = tf.train.load_variables("checkpoint-path", "variable-name")
torch_model.weight.data = torch.from_numpy(weight)
```

위에서 특정 weight에 적용하기 위해서 `data` 필드에 접근하는 이유는 다음과 같습니다. PyTorch 내부의 모듈들은 대부분 `torch.Tensor`보다 [`torch.nn.parameter.Parameter`](https://github.com/pytorch/pytorch/blob/v1.7.0/torch/nn/parameter.py)를 모델 가중치로 사용하기 때문입니다.

### from PyTorch State Dict to TensorFlow Model

이 경우도 위의 경우와 크게 다르지 않습니다. torch의 state dict 로딩은 아래와 같은 과정을 거칩니다.

```python
import torch

# PyTorch의 가중치는 GPU용으로 저장이 되어있는 경우가 많기 때문에 꼭 map_location 인자를 넣어주어야 합니다.
torch_state_dict = torch.load(args.model_path, map_location=torch.device("cpu"))
# 기본적으로 torch.Tensor로 로딩이 됩니다. 따라서 detach()와 numpy() 메소드를 불러주는 것이 꼭 필요합니다.
torch_state_dict = {key: val.detach().numpy() for key, val in torch_state_dict.items()}
```

현재 pytorch의 master branch에 [torch/serialization.py#L484-L488](https://github.com/pytorch/pytorch/blob/79f8582289a2967fbf512e722bfd3f2f932aea53/torch/serialization.py#L484-L488)과 같은 코드가 존재하기 때문에 앞으로 나올 버전을 사용하는 경우 `map_location` 인자가 필요없어집니다.

위 과정을 통해 가져온 state_dict는 아래와 같이 [`set_weights`](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Layer#set_weights) 함수를 통해 가져올 수 있습니다.

```python
tf_module.set_weights(
    [
        torch_state_dict["some-keys-for-weight"],
        torch_state_dict["some-keys-for-bias"],
    ]
)
```

Weight를 위와 같은 함수를 통해 바로 적용하게 되는데, 이 경우 Weight의 순서는 아래처럼 알 수 있습니다.

`tf.keras.layers.Dense`의 경우 [`tensorflow/python/keras/layers/core.py#L1067-L1233`](https://github.com/tensorflow/tensorflow/blob/v2.3.1/tensorflow/python/keras/layers/core.py#L1067-L1233) 코드를 참고하면 `build` 메소드에서 kernel과 bias를 순서대로 할당하는 것을 알 수 있습니다. 이 경우에는 `set_weights`의 인자에도 kernel과 bias가 순서대로 들어가야 합니다.

### from TensorFlow Model to PyTorch Model

모델과 모델 사이의 가중치 변환은 조금 더 쉬워집니다. TensorFlow Model은 `set_weights`와 같이 [`get_weights`](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Layer#get_weights)가 존재하는데 이 함수의 반환값은 list of numpy array이기 때문에 `set_weights`의 인자와 같다고 생각하시면 됩니다. 따라서 아래와 같은 방법으로 가져올 수 있습니다.

```python
# tf_module의 첫번째 weight를 torch_module의 weight에 적용하는 예시
tf_weights = tf_module.get_weights()
torch_module.weight.data = torch.from_numpy(tf_weights[0])
```

### from PyTorch Model to TensorFlow Model

여기서는 `nn.Module`에 존재하는 `state_dict`를 활용할 수 있습니다. 아래는 weight, bias를 tf_module에 적용하는 에시입니다.

```python
weight = torch_module.state_dict()["weight"].detach().numpy()
bias = torch_module.state_dict()["bias"].detach().numpy()

tf_module.set_weights([weight, bias])
```

## 테스팅

아무리 같은 모델을 작성을 하고, 같은 weight를 공유한다고 하여도 같은 값을 만들어는지 직접 확인할 수 없는 이상 제대로 구현했는지 확신할 수 없기 때문에 테스팅이 매우 중요합니다. 핑퐁팀에서는 아래처럼 테스팅을 진행했습니다.

1. torch, tf 모델 초기화 및 빌드
1. torch, tf 사이의 가중치 변환
1. numpy로 예시 입력값을 만들어 두 모델의 결과값 비교

아래는 PyTorch LayerNormalization을 받아서 TensorFlow LayerNormalization으로 변환해주는 `convert_torch_layer_norm`를 테스트하는 예시입니다.

```python
@pytest.mark.parametrize("input_dim", [pytest.param(10), pytest.param(100)])
def test_convert_torch_layer_normalization_with_dims(input_dim: int):
    batch_size = 10
    epsilon = 1e-6

    # Build Layer
    tf_layer_norm = tf.keras.layers.LayerNormalization(epsilon=epsilon)
    tf_layer_norm(tf.keras.Input([input_dim]))

    torch_layer_norm = nn.LayerNorm(input_dim, eps=epsilon)
    torch_layer_norm.eval()

    # Convert Weight
    convert_torch_layer_norm(torch_layer_norm, tf_layer_norm)

    for _ in range(100):
        # Build Input
        test_input = np.random.randn(batch_size, input_dim).astype(np.float32)
        tf_input = tf.constant(test_input, dtype=tf.float32)
        torch_input = torch.tensor(test_input, dtype=torch.float32)

        # Check Output
        tf_output = tf_layer_norm(tf_input).numpy()
        torch_output = torch_layer_norm(torch_input).detach().numpy()

        # Layer Normalization은 구하는 방식에 따라 조금씩 값이 차이가 나기 때문에 tolerance를 조금은 높게 줍니다.
        assert np.allclose(tf_output, torch_output, rtol=1e-5, atol=1e-6)
```

## 추가 고려사항

아래는 제가 weight 변환을 진행하면서 발견했던 대표적인 이슈입니다. 아래의 이슈 외에도 다른 이슈가 존재하였으나 대부분 큰 시간 소요없이 해결 가능하였습니다.

### `tf.keras.layers.Dense`, `torch.nn.Linear`의 weight shape

```python
>>> import torch
>>> import tensorflow as tf
>>> torch_linear = torch.nn.Linear(10, 20)
>>> torch_linear.weight.data.shape
torch.Size([20, 10])
>>> tf_dense = tf.keras.layers.Dense(20)
>>> tf_dense(tf.keras.Input([10]))
<tf.Tensor 'dense/BiasAdd:0' shape=(None, 20) dtype=float32>
>>> tf_dense.get_weights()[0].shape
(10, 20)
```

위에서 볼 수 있듯이 TensorFlow와 PyTorch의 Feed Forward Layer의 weight shape가 다릅니다. Transpose할 시 정확하게 부여됩니다.

### 특정 경우의 Matrix Multiplication 결과값의 차이

```python
>>> import tensorflow as tf
>>> import torch
>>> import numpy as np
>>> a = np.random.randn(20, 30).astype(np.float32)
>>> b = np.random.randn(30, 20).astype(np.float32)
>>> tf_result = tf.matmul(tf.constant(a), tf.constant(b))
>>> torch_result = torch.matmul(torch.tensor(a), torch.tensor(b))
>>> # absolute diff
>>> np.max(np.abs(tf_result.numpy() - torch_result.numpy()))
2.861023e-06
>>> # relative diff
>>> np.max(np.abs((tf_result.numpy() - torch_result.numpy()) / tf_result.numpy()))
1.0196954e-06
```

대부분의 경우는 안전합니다. 하지만 위 같은 경우를 보았을 때 numpy의 기본 `allclose`의 `atol`(`1e-8`), `rtol`(`1e-5`) 오차는 안전한 범위이지만, 오차가 있는 경우가 누적이 되더라도 큰 모델의 결과값이 꽤 달라질 수 있습니다.

### GRU와 같은 레이어의 Weight 순서

LSTM, GRU와 같은 레이어를 TensorFlow와 PyTorch를 서로 변환할 때 Gate의 순서가 다를 수 있습니다. 여기서는 GRU를 예시로 설명해보겠습니다.

#### TensorFlow의 GRU

TensorFlow의 GRU는 아래와 같이 Gate 연산을 진행합니다. ([`tensorflow/python/keras/layers/recurrent.py#L1672-L1949`](<https://github.com/tensorflow/tensorflow/blob/fcc4b966f1265f466e82617020af93670141b009/tensorflow/python/keras/layers/recurrent.py#L1672-L1949>))

```python
      x_z = K.dot(inputs_z, self.kernel[:, :self.units])
      x_r = K.dot(inputs_r, self.kernel[:, self.units:self.units * 2])
      x_h = K.dot(inputs_h, self.kernel[:, self.units * 2:])
```

`self.kernel`이 Update Gate, Reset Gate, Output Candidate를 계산하기 위한 커널이 순서대로 연결되어 있다고 이해할 수 있습니다. 또한 bias는 아래처럼 계산합니다. (전체 코드가 아닌 일부 코드입니다.)

```python
      recurrent_z = K.dot(h_tm1_z, self.recurrent_kernel[:, :self.units])
      recurrent_r = K.dot(h_tm1_r,
                          self.recurrent_kernel[:, self.units:self.units * 2])
      if self.reset_after and self.use_bias:
        recurrent_z = K.bias_add(recurrent_z, recurrent_bias[:self.units])
        recurrent_r = K.bias_add(recurrent_r,
                                 recurrent_bias[self.units:self.units * 2])
```

`self.recurrent_kernel`과 `self.bias`(`recurrent_bias`는 `self.bias`에서 나온 값입니다.)도 구역을 나누어 쓰는 것을 알 수 있습니다. `tf.keras.layers.GRUCell` 전체 코드를 들여다보면 결국 아래처럼 weight가 구성되어 있는 것을 알 수 있습니다.

* `kernel`, `(input_size, hidden_size * 3)`: Update gate kernel, Reset gate kernel, Output candidate vector kernel
* `recurrent_kernel`, `(hidden_size, hidden_size * 3)`: Update gate kernel, Reset gate kernel, Output candidate vector kernel
* `bias`, `(2, hidden_size * 3)`: 첫번째 `(hidden_size * 3)` 벡터는 `kernel`을 위한 bias, 두번째 `(hidden_size * 3)` 벡터는 `recurrent_kernel`을 위한 bias

#### PyTorch의 GRU

그렇다면 PyTorch의 GRU 구현은 어떻게 되어 있을까요? 아래와 같이 연산을 진행합니다. ([`aten/src/ATen/native/RNN.cpp#L723-L753`](https://github.com/pytorch/pytorch/blob/e85d494707b835c12165976b8442af54b9afcb26/aten/src/ATen/native/RNN.cpp#L723-L753))

```c++
template <typename cell_params>
struct GRUCell : Cell<Tensor, cell_params> {
  using hidden_type = Tensor;

  hidden_type operator()(
      const Tensor& input,
      const hidden_type& hidden,
      const cell_params& params,
      bool pre_compute_input = false) const override {
    if (input.is_cuda()) {
      TORCH_CHECK(!pre_compute_input);
      auto igates = params.matmul_ih(input);
      auto hgates = params.matmul_hh(hidden);
      auto result = at::_thnn_fused_gru_cell(
          igates, hgates, hidden, params.b_ih(), params.b_hh());
      // Slice off the workspace argument (it's needed only for AD).
      return std::move(std::get<0>(result));
    }
    const auto chunked_igates = pre_compute_input
        ? input.unsafe_chunk(3, 1)
        : params.linear_ih(input).unsafe_chunk(3, 1);
    auto chunked_hgates = params.linear_hh(hidden).unsafe_chunk(3, 1);
    const auto reset_gate =
        chunked_hgates[0].add_(chunked_igates[0]).sigmoid_();
    const auto input_gate =
        chunked_hgates[1].add_(chunked_igates[1]).sigmoid_();
    const auto new_gate =
        chunked_igates[2].add(chunked_hgates[2].mul_(reset_gate)).tanh_();
    return (hidden - new_gate).mul_(input_gate).add_(new_gate);
  }
};
```

`chunked_hgates`와 `chunked_igates` 변수를 활용하는 것을 잘 보면, reset, input, new로 순서대로 구성이 되어있는 것을 알 수 있습니다. 각각 Reset gate, Update gate, Output candidated에 해당합니다. 그리고 PyTorch GRU의 State Dict를 추출해보면 `weight_ih_l{LAYER 숫자}`, `weight_hh_l{LAYER 숫자}`, `bias_ih_l{LAYER 숫자}`, `bias_hh_l{LAYER 숫자}`(예를 들면 `weight_ih_l0`와 같은 식)처럼 나옵니다. 즉 아래처럼 구성되어 있다는 것을 알 수 있죠.

* `weight_ih`, `(hidden_size * 3, input_size)`: TensorFlow GRU의 `kernel`에 해당하고 Reset gate, Update gate kernel의 위치가 바뀌어 있는 상황
* `weight_hh`, `(hidden_size * 3, hidden_size)`: TensorFlow GRU의 `recurrent_kernel`에 해당하고 Reset gate, Update gate kernel의 위치가 바뀌어 있는 상황
* `bias_ih`, `(hidden_size * 3)`: TensorFlow GRU의 `bias`의 첫번째 벡터 (`weight_ih`의 bias)
* `bias_hh`, `(hidden_size * 3)`: TensorFlow GRU의 `bias`의 두번째 벡터 (`weight_hh`의 bias)

#### 변환한다면?

이 점을 모두 알게된다면 다소 편해집니다. Torch 혹은 TF의 kernel을 가져와서 Reset gate, Update gate의 순서를 바꾸어주고 Transpose를 한 뒤, bias들을 합치거나 분해하면 각각의 weight로 사용이 가능하게 됩니다.

## 결론

TensorFlow와 PyTorch를 한 조직내에서 사용한다는 것은 어렵고 고된 일입니다. 리소스가 많이 들지만, 리서치의 편의성을 보장해주면서도 서빙의 용이함을 가져갈 수 있다는 것은 분명한 장점입니다. 핑퐁팀은 리서치 코드 베이스와 엔지니어링 코드 베이스를 분리하기로 하였고 그 결과 팀 내의 모든 모델을 PyTorch 버전으로 리서치 시에 편하게 가져다 쓸 수 있으면서 리서치가 끝난 경우 그 가중치를 TensorFlow 모델로 빠르게 옮겨 배포도 용이하게 할 수 있는 라이브러리가 탄생하게 되었습니다.
