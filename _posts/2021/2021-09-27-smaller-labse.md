---
layout: post
title: "Smaller LaBSE & TF Hub"
tags:
  - tensorflow
---

얼마전에, [Geotrend-research/smaller-transformers](https://github.com/Geotrend-research/smaller-transformers)라는 레포지토리를 우연히 보게 되어서 최근에 관심이 가는 LaBSE(Language-agnostic BERT Sentence Embedding)에 적용해보았다.

* GitHub: <https://github.com/jeongukjae/smaller-labse>
* TensorFlow Hub
  * 모델: <https://tfhub.dev/jeongukjae/smaller_LaBSE_15lang/1>
  * 전처리 모델: <https://tfhub.dev/jeongukjae/smaller_LaBSE_15lang_preprocess/1>

## 배경

어느정도 배경 설명을 적어보자면, Language agnostic한 임베더를 찾아보고 있었고, 이런 모델이 파인튜닝 이후에도 그런 성질(language agnostic한 성질)을 유지하는지 궁금했다. 그러기 위해서 파인튜닝을 해보려고 헀는데, 모델이 커도 너무 컸다. 471M 파라미터인데, Adam만 써도 GPU 8GB 정도는 금세 먹고 시작하는 사이즈라.. 간단하게 못 줄이나?? 찾아보던 도중 `Load What You Need: Smaller Versions of Multilingual BERT`이라는 논문을 찾았고, LaBSE에 맞게 구현해봤다. 줄이고 나니 15개 언어를 사용할 경우 219M까지 줄고, 5개 언어정도로 줄이면 132M까지 줄어든다.

## 방법

원 구현에서 사용하는 위키 덤프 데이터를 가져와서, tokenize한 후에 빈도 기준으로 상위 토큰들만 유지했다. 원 구현에서 살짝 수정했는데, 이건 알고리즘은 유지하면서 `tf.data.Dataset` 사용만 하도록 수정했다. 그리고 사용할 언어에 대해서 상위 토큰만 합쳐서 모델을 export만 하면 된다. 그냥 이런 식(<https://github.com/jeongukjae/smaller-labse/blob/104e4ff7f49a6c8490b3d55a4d32584fe356dcfb/make_smaller_labse.py#L86>)으로 뚝딱 하면 된다. m-USE에서 사용하는 것과 최대한 비슷하게 15개 언어에 대해 추출했고, `smaller_LaBSE_15lang`이란 이름으로 tfhub에 올려놓았다.

### 평가

facebook research에서 나온 LASER 모델 낼 때 같이 배포해준 tatoeba testset 기준으로 평가해봤다. 알고리즘 상 성능이 거의 떨어지면 안되는데, 역시 굉장히 적은 수치의 차이만 있었다. 자세한 성능은 <https://github.com/jeongukjae/smaller-labse#tatoeba> 참고.

### tfhub

사실 올릴 생각은 별로 없었는데, (학습도 안했고, 워낙 간단한 코드로 만든 모델이라) [tensorflow forum show&tell에 글](https://discuss.tensorflow.org/t/reducing-the-parameter-size-of-labse-language-agnostic-bert-sentence-embedding-for-practical-usage/4418?u=jeongukjae) 올려봤다가 올려보면 좋을 것 같다고 해서 올려봤다. 개인적으로도 한번 해보는셈 치고 올려봤는데, 생각보다 편하게 올릴 수 있었다. GCS에 올려놓고 링크 주면 TFHub에서 긁어다가 배포하는 것 같고(일관성 유지를 위해서 이렇게 한 것 같음), [tensorflow/tfhub.dev](https://github.com/tensorflow/tfhub.dev)는 assets 내부 파일들 거의 스태틱 사이트처럼 쓰는 느낌이다. (정확히 말하자면 쿼리 스트링에 따라 compressed, uncompressed로 잘 반환해야해서 스태틱 사이트는 아니다)

나중에 개인적으로 사용할 모델 있으면 좀 더 올려놔야겠다. 올리면서 다른 PR이나 TF Forum 글 훑어보았는데, 많이 활성화시키고 싶은 것 같다. 생태계가 잘 구성하기 위해 잘 만들어 놓은게 많은데, 대형 모델이 huggingface에 많아서 그런가? 싶기도 하고.

## 참고자료

* Load What You Need: Smaller Versions of Multilingual BERT (Paper: <https://arxiv.org/abs/2010.05609>, GitHub: <https://github.com/Geotrend-research/smaller-transformers>)
* Language-agnostic BERT Sentence Embedding: <https://arxiv.org/abs/2007.01852>
* TFHub - LaBSE: <https://tfhub.dev/google/LaBSE/2>
* LaBSE blog post: <https://ai.googleblog.com/2020/08/language-agnostic-bert-sentence.html>
* Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond: <https://arxiv.org/abs/1812.10464>
