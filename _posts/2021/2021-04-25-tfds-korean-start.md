---
layout: post
title: "TensorFlow Datasets로 tfds-korean 작성하기"
tags:
    - tensorflow
---

종종 개인적으로 궁금한 것들이 있을 때 실험을 해보는데, 각각 데이터셋을 불러오는 코드를 작성하니 너무 파편화되어 있기도 하고 찾아오기도 힘들어서 한국어/한글 관련 데이터셋 라이브러리를 하나 만들기로 했다.

* 레포지토리: <https://github.com/jeongukjae/tfds-korean>
* 카탈로그 페이지: <https://jeongukjae.github.io/tfds-korean/>

## 왜 만들었을까

우선 TensorFlow 환경이 실험하기에 무엇보다 좋다고 생각한다.
리서치와 관련되어 있는 실험이라기보다 간단한 데이터셋이 있을 때 거기에 알맞는 바로바로 적용가능한 코드를 작성하기에 좋다.
데이터셋 코드는 짧고, 빠르며, 병목이 거의 없고, 모델 코드는 같은 코드로 프로덕션 모델까지 갈 수 있고 안정적이다.
또한 실제 파이프라이닝을 할 때도 큰 고민 없이 TensorFlow에서 지원하는 것들만으로 구성이 가능하다.

하지만 TensorFlow는 한국 커뮤니티가 크지 않다고 생각하는데, 내 생각은 아래 정도이다.
TensorFlow KR이 페이스북에서 가장 큰 한국의 ML 커뮤니티로 보이지만, TensorFlow 컴포넌트 활용을 앞서서 홍보하는 것은 아니다.
그렇다고 절대 나쁘다는 것은 아니고, 머신러닝을 이야기하기에 굉장히 좋은 커뮤니티라 그 자체만으로 좋은 커뮤니티라 생각한다.
어쨌든 그러다보니 생각보다 TensorFlow 컴포넌트들의 좋은 기능에 비해 한글/한국어 데이터와 연관된 생태계가 충분히 잘 갖춰져 있지 않다.

그 중에 제일 내가 필요한 게 데이터셋 쪽이라 생각하고 한국어 데이터셋 위주로 TensorFlow Datasets를 사용해서 하나 만들어 놓았다.
추가로 회사에서 사용가능하도록 private한 데이터셋 라이브러리가 편하게 만들어지는지 궁금했다.

### 기존에 있는 것들은?

충분히 좋다. 두 개의 좋은 라이브러리를 찾았는데, [HuggingFace/Datasets](https://github.com/huggingface/datasets)와 [Korpora](https://github.com/ko-nlp/Korpora)이다.

HuggingFace가 ML 분야에서 매우 좋은 생태계를 만들어주고 있는데, Transformers나 Accelerate 라이브러리들 보다도 Datasets가 제일 좋은 편이라 생각한다.
framework agnostic하면서 많은 데이터셋을 담고 있다.
하지만 Framework agnostic하게 가면서 dataset 자체를 다시 구현해야 해서 다시 구현한 것 같은데, 그렇게 쓰기보다는 나는 차라리 라이브러리 자체의 Dataset, DataLoader를 쓰겠다는 입장이어서 고려사항은 아니었다.
HuggingFace Datasets 자체에서 굉장히 좋은 기능이 많이 추가되거나 PyTorch 팀으로 들어가게 된다면 생각은 달라질 것 같다.
당연히 라이브러리 팀과 협력하겠지만, 라이브러리 자체의 기능이 풍부하고 비슷하거나 좋으면 라이브러리 자체의 기능을 쓰는 편이 좋다고 판단했다.

그 다음으로 Korpora인데, 카탈로그 페이지가 없는게 흠이었다.
또한 checksum 확인 같은 기능이 없었고, 너무 반복되는 코드가 많다고 생각했다. (괜찮다고 생각이 들면 허깅페이스 쪽이나 Korpora 쪽이나 당연히 기여하면서 사용할 생각이었다)
그리고 HugginFace/Datasets와 같은 이유로 framework agnostic하다는 점이 조금은 불안했다.

그래서 TensorFlow Datasets를 기반으로 작성하기로 했다.

## 만들어보기

우선 데이터셋 로딩, Dataset 객체 변환과정 등등은 프레임워크 기능에 맡길 수 있으니 너무 편했다.
내가 작성해야하는 부분은 `다운로드 후 파일 파싱`과 `메타 정보 채우기`, `Example 작성`, `Dataset Catalog 페이지 만들기` 이 네개 정도.

다운로드 후 파일 파싱하는 부분도 tfds cli를 이용하니 템플릿이 다 만들어졌다.
자세한 내용은 TFDS 가이드의 <https://www.tensorflow.org/datasets/add_dataset>를 참고.
아래 같은 커맨드를 실행하면 checksum 등록까지 다 된다.

```sh
cd path/to/my/project/datasets/
tfds new my_dataset  # Create `my_dataset/my_dataset.py` template files
# [...] Manually modify `my_dataset/my_dataset.py` to implement your dataset.
cd my_dataset/
tfds build --register_checksums # Download and prepare the dataset to `~/tensorflow_datasets/`
```

`tfds new` 커맨드를 통해 생성된 템플릿 안에서 데이터셋을 파싱하는 builder, builder에 대한 테스트 케이스를 작성한다.
그 후 이렇게 바로 `tf.data.Dataset` 객체로 불러올 수 있다.

```python
import my.project.datasets.my_dataset  # Register `my_dataset`

ds = tfds.load('my_dataset')  # `my_dataset` registered
```

내가 원하는 기능은 충분히 잘 제공되는 셈이고, 테스트 케이스까지 작성할 수 있게 템플릿을 제공해서 좋았다.

다만 조금 부족했던 점은 Dataset Catalog 페이지를 빌드하는 것인데, TFDS 코드를 뜯어보면서 당연히 가능할 줄 알았던 기능이지만 불가능했다.
내부 doc 빌드용으로 사용했던 코드였던 걸로 보인다.

그래서 tfds 기능과 jinja, jekyll을 조합해서 적당히 만들었고, 볼 수 있는 수준은 되었다. (<https://github.com/jeongukjae/tfds-korean/blob/develop/tfds_korean/build_catalog.py>)
대충 설명해보면 tfds에 역시 builder만을 가지고 조작할 수 있는 기능이 존재해서, 해당 기능을 이용해 jinja를 써서 렌더링 후 Jekyll로 호스팅했다. 순서는 아래정도.

그렇게 작성된 카탈로그 페이지는 <https://jeongukjae.github.io/tfds-korean/>이고 Jekyll 테마를 잘 가져온 덕에 검색이나 Edit this page 같은 rtd + sphinx에 있는 기능이 잘 구현되어 있었다.

그렇게 카탈로그까지 추가하고 나니 꽤 사용할만한 라이브러리가 됐고, 당연히 pypi 패키지 등록이나 테스트 코드 돌리는 Github Action 등등은 해놓았다.

## 앞으로 어떻게 사용할까

여러모로 사용해볼까 싶은데, 일단은 NER을 하고 싶었던 탓에 NER 데이터만 더 추가해본 다음에 테스트해보고 싶은 것들을 좀 테스트해볼까 싶고, 그 다음 문서 리트리벌에서 테스트하고 싶은 아이디어가 있어서 해당 데이터도 같이 추가해놓을까 싶다.
그래서 KorQuad 같은 데이터 혹은 좀 Raw한 문장이 많이 있는 데이터를 찾아보고 있다.

이렇게 구성해보니 꽤 괜찮아서 계속 데이터셋 추가해볼 것 같고, 이걸 만들어 볼 때 궁금했던 `회사에서 사용하기에도 좋을까?`는 잘 모르겠어서 계속 해보려 한다.
내가 구현했던 방식(`http`로 다운로드)과는 다르게 gcs에서 받아오는 옵션도 구현가능해서 팀 내에서 사용해볼만 할 것 같긴 하지만, 어디까지나 리서치 팀 용으로 보이고, 프로덕션 팀에게는 힘들 것 같다.

그래도 외부데이터는 이런식으로 한번 만들어 두면 엄청 가져오기 편해지니까 외부 데이터로 벤치마크 해보기에는 좋아보인다.
