---
layout: post
title: 📕 CS224n Lecture 11 ConvNets for NLP
tags:
  - nlp
  - cs224n
  - machine learning
---

11강! 마지막 과제인 과제 5도 슬슬 마감으로 보인다. 강의에서도 second half라고 한다! 이제부터 거의 소개에 가깝다고 한다.

* [slide](http://web.stanford.edu/class/cs224n/slides/cs224n-2019-lecture11-convnets.pdf)
* [video](https://www.youtube.com/watch?v=EAJoRA0KX7I)

Suggested Readings. 나중에 읽어봐야지

1. [Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882)
2. [A Convolutional Neural Network for Modelling Sentences](https://arxiv.org/abs/1404.2188)

이건 읽으면 좋다는 책

[Natural language processing with PyTorch : build intelligent language applications using deep learning](https://searchworks.stanford.edu/view/13241676)

강의 초반에 CNN에 관한 간략한 설명이 나와있는데, 이것은 CS231n에서 더 자세하게 알려준다. 하지만 해당 강의 초반을 이미 들어서 쭉 넘기면서 들었다.

## Why CNNs?

CNN을 사용하기 위해서 RNN과 구분되는 CNN의 장점과 RNN의 단점을 알아보자.

우선 RNN은 phrase를 prefix context 없이 잡아내지 못한하고, phrase를 잡아낼 때 단어를 너무 많이 잡아낸다.

하지만 CNN은 특정한 길이의 word subsequence를 모두 만들어 계산하므로, 문법적으로 옳은 phrase만을 잡아내는 것이 아니다.

## Single Layer CNN for Sentence Classification

Sentence Classification에 관한 Yoon Kim (2014)의 논문을 참고하면 좋다고 한다. 해당 논문의 코드는 [github yoonkim/CNN_sentence](https://github.com/yoonkim/CNN_sentence)에 있다.

CNN을 sentence classification에 활용하기 위해서 사용한다. 주로 sentiment 분석을 위한 용도로 사용할 수 있다고 한다. [A Sensitivity Analysis of (and Practitioners' Guide to) Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1510.03820) 도 나중에 읽어보자.

강의에서 추가로 좀 더 살펴볼 수 있는 내용, 키워드로 나온 것은 "Multiple filter를 이용하면 어떨까?", "Multiple Channel을 이용하면 어떨까?", Dropout, BatchNorm, 1x1 convolution 등이다. 아래는 그 상세한 내용 + 추가 링크

* [Batch Normalization](https://arxiv.org/abs/1502.03167)
* [Network in Network (1x1 convolution)](https://arxiv.org/abs/1312.4400)
* [Recurrent Continuous Translation Models](https://www.aclweb.org/anthology/D13-1176) : CNN을 encoding에 사용하고 RNN을 decoding에 사용해서 기계번역하는 방법
* [Character-Aware Neural Language Models](https://arxiv.org/abs/1508.06615)
* [Learning Character-level Representations for Part-of-Speech Tagging](http://proceedings.mlr.press/v32/santos14.pdf) : word embedding
* [VDCNN](https://arxiv.org/abs/1606.01781)
* [QRNN](https://arxiv.org/abs/1611.01576)

여튼 RNN은 느리고, 그래서 더 다양한 방법을 찾는다.
