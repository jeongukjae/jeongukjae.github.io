---
layout: post
title: "📕 CS224n Lecture 17 The Natural Language Decathlon: Multitask Learning as Question Answering"
tags:
  - nlp
  - cs224n
  - machine learning
---

Richard Socher라는 Saleforce의 Chief Scientist가 게스트로 나와 강의를 한다고 한다.

강의는 전체적으로 multi-task learning에 대한 내용인데, single-task의 한계에 대해서 먼저 알아보자. 최근에 dataset, task, model, metric에 대한 엄청난 발전이 있었지만, 예전에는 새로운 모델은 거의 random한 상태에서 새로 시작하거나 일부만 pre-train된 상태에서 시작해야했다. 하지만 시간이 지나면서 word2vec, GloVe, CoVe, ELMo, BERT처럼 더 많은 부분을 pretrain해서 모델을 새로 구성할 때 더 좋은 결과를 내는 것을 볼 수 있었다.

그럼 전체를 왜 pretrained model을 사용하지 않을까?

{% include image.html url="/images/cs224n/17-1.png" %}
