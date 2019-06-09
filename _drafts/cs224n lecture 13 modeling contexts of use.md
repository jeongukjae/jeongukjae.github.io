---
layout: post
title: "📕 CS224n Lecture 13 Modeling contexts of use: Contextual Representations and Pretraining"
tags:
  - nlp
  - cs224n
  - machine learning
---

13강 정리! 11강부터인가? 그때부터 대부분 소개가 되어가고 있어서 좋은 링크 정리 정도만 하고 있는 것 같다.

## Reflections on word representation

지금까지는 word embedding을 시작부터 했는데, pretrained model를 사용하자는 말. 그 이유는 더 많은 단어와 더 많은 데이터에 대해 학습이 가능해진다는 이유이다. 실제로 성능도 더 높은 것으로 보인다.

근데 unknown words에 대해서는 어떻게 대응할 것인가? `UNK`으로 매핑해서 어쩌구저쩌구를 하지만 결론은 char-level model을 사용하자! 또는 테스트때 `<UNK>`가 unsupervised word embedding에 존재한다면 그걸 계속 쓰고, 그냥 아예 모르는 것은 random vector로 만든다음에 vocab에 추가하는 방법도 고려해보라고 한다. [^Dhingra2017]

[^Dhingra2017]: [A Comparative Study of Word Embeddings for Reading Comprehension](https://arxiv.org/abs/1703.00993) 헤딩 논문

어찌되었든 word embedding을 시작부터 학습시키는 것은 두가지 큰 문제가 있는데, 하나의 단어에 대해 context 상관없이 다 같은 representation을 가져온다는 점이다.

## Pre-ELMo and ELMO

## ULMfit and onward

## Transformer architecture

## BERT
