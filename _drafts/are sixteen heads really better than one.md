---
layout: post
title: "📃 Are Sixteen Heads Really Better than One? 리뷰"
tags:
  - paper
  - nlp
---

Multi head attention이 표현력이 좋고 많은 정보를 담을 수 있다지만, 모든 head가 필요한 것은 아니다. 이에 관한 논문이 Are Sixteen Heads Really Better Than One? (Michel et al., 2019)이고, arxiv 링크는 [https://arxiv.org/abs/1905.10650](https://arxiv.org/abs/1905.10650)이다.

## Abstract

* MultiHead로 학습이 되었더라도 Test Time에는 많은 head를 제거해도 비슷한 성능을 보존하는 것이 가능함.
* 특히 몇몇 레이어는 single head여도 성능하락이 없었다.

## 1. Introduction

* greedy 하고 iterative한 attention head pruning 방법 제시
* inference time을 17.5% 높였다.
* MT는 pruning에 특히 민감했는데, 이를 자세히 살펴봄

## 2. Background: Attention, Multi-headed Attention, and Masking

* 거의 다 패스
* Multi Head Attention Masking하는 것은 mask variable로 계산함
* 특정 head의 결과값을 0으로 지정

## 3. Are All Attention Heads Important?

* WMT에서 테스트

### 3.2. Ablating One Head

* 하나의 Head만 제거하는 테스트

{%include image.html url="/images/2020-05-13-sixteen-heads/fig1.png" class='noshadow' %}


### 3.3. Ablating All Heads but One

### 3.4. Are Important Heads the Same Across Datasets?

## 4. Iterative Pruning of Attention Heads

### 4.1. Head Importance Score for Pruning

### 4.2. Effect of Pruning on BLEU/Accuracy

### 4.3. Effect of Pruning on Efficiency

## 5. When Are More Heads Important? The Case of Machine Translation

## 6. Dynamics of Head Importance during Training

## 7. Related work

## 8. Conclusion
