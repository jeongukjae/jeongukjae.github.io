---
layout: post
title: DistilKoBERT sentence encoder 만들어보기
tags:
  - tensorflow
  - nlp
---

얼마전에 [TensorFlow KR에 DistilKoBERT 기반의 문장 임베딩 모델을 만들어 공유](https://www.facebook.com/groups/TensorFlowKR/permalink/1620684584939260/)했다. Knowledge Distillation을 활용해서 KorNLI, KorSTS를 학습한 모델이고 TensorFlow Hub에서 바로 사용할 수 있도록 구성해두었다.

<https://tfhub.dev/jeongukjae/distilkobert_sentence_encoder/1>에서 TensorFlow Hub에 올라간 DistilKoBERT sentence encoder를 볼 수 있다.

## 학습 과정

### 모델 변환 및 준비

개인적으로 TensorFlow 기반으로 학습하는게 고성능 데이터 루프, 미리 구성해둔 tfds-korean 라이브러리([GitHub](https://github.com/jeongukjae/tfds-korean), [Dataset List](https://jeongukjae.github.io/tfds-korean/), [블로그 포스트](https://blog.ukjae.io/posts/tfds-korean-start/)), TPU를 활용할 수 있어서 편하다. 그래서 이번에도 Colab으로 간단하게 학습해보았다.

모델 변환은 기존에 작성하던 [`jeongukjae/huggingface-to-tfhub`](https://github.com/jeongukjae/huggingface-to-tfhub) 레포지토리에서 약간 수정한 뒤 DistilKoBERT와 KLUE RoBERTa 모델을 전부 추출해두었다. 데이터는 labeled data만 활용했고, KorNLI, KorSTS, KLUE STS만 활용했다.

* <https://jeongukjae.github.io/tfds-korean/datasets/klue_sts.html>
* <https://jeongukjae.github.io/tfds-korean/datasets/kornli.html>
* <https://jeongukjae.github.io/tfds-korean/datasets/korsts.html>

## 모델 학습

모델 학습은 아래와 같이 작성했다. 간편하게 colab 노트북 4개 만들어서 돌렸다.

1. KLUE RoBERTa large를 KorNLI 사용해서 supervised SimCSE 학습
1. KorSTS + KLUE STS로 regression 문제 학습
1. DistilKoBERT로 2번 모델 Knowledge Distillation
1. 3번 모델을 KorSTS + KLUE STS로 regression 추가 학습

이전에 해보았던 SimCSE 방법론([블로그 글](https://blog.ukjae.io/posts/simcse-kr-bert/))을 그대로 활용했고, sentence bert에서 진행하는 것처럼 regression 태스크 추가로 학습했다. 근데 KLUE RoBERTa large를 실제 서비스할 때나 분석할 때 그대로 쓰는 것은 힘들 것 같아서, DistilKoBERT(3 layer - 768 hidden size 크기라 CPU에서도 충분히 추론 가능) 모델에 Knowledge Distillation을 수행했다.

아직 귀찮아서 깃헙에 코드 업로드는 안해놓았는데, 공개하면 여기 블로그 글을 업데이트 해두어야겠다.

## 결과

SRoBERTa, BERT base 사이즈보다 4배 빠르면서 성능은 비슷하거나 좋게 나왔다. KorSTS testset 기준으로 cross-encoding으로 학습한 Korean RoBERTa base보다 성능이 좋다.

### KorSTS development set

| Model                             | # Params | encoding strategy | Spearman correlation \* 100 |
| --------------------------------- | -------: | ----------------- | --------------------------: |
| **distilkobert_sentence_encoder** |      28M | bi-encoding       |                       86.53 |
| Korean SRoBERTa (base)†           |     111M | bi-encoding       |                       83.54 |
| Korean SRoBERTa (large)†          |     338M | bi-encoding       |                       84.21 |
| SXLM-R (base)†                    |     270M | bi-encoding       |                       81.95 |
| SXLM-R (large)†                   |     550M | bi-encoding       |                       84.13 |
| Korean RoBERTa (base)†            |     111M | cross-encoding    |                       84.97 |
| Korean RoBERTa (large)†           |     338M | cross-encoding    |                       87.82 |
| XLM-R (base)†                     |     270M | cross-encoding    |                       83.02 |
| XLM-R (large)†                    |     550M | cross-encoding    |                       88.37 |

- †: results from [Ham et al., 2020](https://arxiv.org/abs/2004.03289).

### KorSTS test set

| Model                             | # Params | encoding strategy | Spearman correlation \* 100 |
| --------------------------------- | -------: | ----------------- | --------------------------: |
| **distilkobert_sentence_encoder** |      28M | bi-encoding       |                       83.12 |
| Korean SRoBERTa (base)†           |     111M | bi-encoding       |                       80.29 |
| Korean SRoBERTa (large)†          |     338M | bi-encoding       |                       80.49 |
| SXLM-R (base)†                    |     270M | bi-encoding       |                       79.13 |
| SXLM-R (large)†                   |     550M | bi-encoding       |                       81.84 |
| Korean RoBERTa (base)†            |     111M | cross-encoding    |                       83.00 |
| Korean RoBERTa (large)†           |     338M | cross-encoding    |                       85.27 |
| XLM-R (base)†                     |     270M | cross-encoding    |                       77.78 |
| XLM-R (large)†                    |     550M | cross-encoding    |                       84.68 |

- †: results from [Ham et al., 2020](https://arxiv.org/abs/2004.03289).

### KLUE STS development set

| Model                             | # Params | encoding strategy | Pearson correlation \* 100 |
| --------------------------------- | -------: | ----------------- | -------------------------: |
| **distilkobert_sentence_encoder** |      28M | bi-encoding       |                      86.87 |
| KLUE-BERT (base)\*                |     110M | cross-encoding    |                      91.01 |
| KLUE-RoBERTa (base)\*             |     110M | cross-encoding    |                      92.91 |

- \*: results from [Park et al., 2021](https://arxiv.org/abs/2105.09680)

## 사용법

TensorFlow Hub에서 바로 끌어다가 아래처럼 사용할 수 있다.

```python
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

# Load required models
encoder = hub.KerasLayer("https://tfhub.dev/jeongukjae/distilkobert_sentence_encoder/1")
preprocessor = hub.KerasLayer("https://tfhub.dev/jeongukjae/distilkobert_cased_preprocess/1")

# Define sentence encoder model
inputs = tf.keras.Input([], dtype=tf.string)
encoder_inputs = preprocessor(inputs)
sentence_embedding = encoder(encoder_inputs)
normalized_sentence_embedding = tf.nn.l2_normalize(sentence_embedding, axis=-1)
model = tf.keras.Model(inputs, normalized_sentence_embedding)

# Encode sentences using distilkobert_sentence_encoder
sentences1 = tf.constant([
    "다만, 도로와 인접해서 거리의 소음이 들려요.",
    "형이 다시 캐나다 들어가야 하니 가족모임 일정은 바꾸지 마세요.",
    "방안에 필요한 시설이 모두 있어서 매우 편리합니다.",
    "관광자원화 검토를 모범적으로 적용한 지자체에는 홍보·컨설팅, 관광상품 개발 지원 등을 제공할 계획이다.",
])
sentences2 = tf.constant([
    "하지만, 길과 가깝기 때문에 거리의 소음을 들을 수 있습니다.",
    "가족 모임 일정은 바꾸지 말도록 하십시오.",
    "특히, 숙소 근처에 안전한 실내 주차장이 있어서 편리합니다.",
    "아울러 지자체, 지역관광협회 등과 함께 수시로 관광지 현장을 점검할 계획이다.",
])
embeddings1 = model(sentences1)
embeddings2 = model(sentences2)

# Calculate cosine similarity
print(tf.tensordot(embeddings1, embeddings2, axes=[[1], [1]]))
# Expected outputs:
#
# tf.Tensor(
# [[ 0.8907616   0.07906969 -0.09612353  0.00167902]
#  [ 0.0184274   0.6840409  -0.1102942   0.02653065]
#  [-0.00795126 -0.10688838  0.5041443  -0.01270578]
#  [ 0.04684553 -0.0619101   0.00684686  0.68705124]], shape=(4, 4), dtype=float32)
```
