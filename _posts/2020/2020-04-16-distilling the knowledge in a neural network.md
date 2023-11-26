---
layout: post
title: "Distilling the Knowledge in a Neural Network 리뷰"
tags:
  - paper
---

구글에서 Geoffrey Hinton, Oriol Vinyals, Jeff Dean이 작성한 Distillation 개념을 제안한 논문이다. arvix 링크는 [https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531)이고, NIPS 2014 워크샵에 나온 논문이다.

## Abstract

* 모델을 ensemble하는 것이 좋은 성능을 얻는 간단한 방법 중 하나지만 너무 연산이 비싸고 배포하기 힘들다.
* 그래서 해당 정보를 압축하여 간단한 뉴럴 넷에 옮겨주는 것이 효과적인 방법이 될 수 있다.

## 1 Introduction

* 큰 모델 (논문에서는 cumbersome model이라 말한다)의 knowledge를 효과적으로 transfer하는 방법은 큰 모델에서 나온 class probabilities를 바로 small model의 target (soft target) 이용하는 것이다.
* 이것이 왜 효과적인지는 아래 설명을 보자

  MNIST용으로 학습된 큰 모델은 굉장히 높은 정확도로 숫자들을 맞출테지만, 어느정도 다른 클래스에도 prob을 준다. 예를 들어 2를 맞출 때 닮은 숫자인 3과 7도 낮은 확률이지만 값을 부여할 것이다. 이 정보들은 굉장히 중요한 정보인데, data의 structure에 대한 정보가 들어있는 값이기 때문이다.

  * 하지만 그 값도 굉장히 낮은 값이라, temperature 개념을 도입했다. (다른 값이 0에 가까우면 hard target을 학습하는 것과 다를 것이 없다.)

## 2 Distillation

* 보통의 softmax 식과는 다르게 temperature 개념을 도입한다. logit $$z_i$$에 대해 prob $$q_i$$는 아래 식이 된다.

  $$q_i = \frac {\exp (z_i / T)} {\sum_j \exp (z_j / T)}$$

  * T는 Temperature이고, T=1이라면 보통의 softmax 식이다. T가 커지면 훨씬 soft한 probability distribution이 나온다.
* loss는 두가지를 주게 되는데,
  * 높은 T에 대해서 distilled model과 cumbersome model의 output 사이의 cross entropy loss와
  * T=1로 두고 hard label과 distilled model의 output 사이의 cross entropy loss를 계산한다.
* 하지만 첫번째 loss가 gradient 계산 시 $$\frac 1 {T^2}$$으로 scaling되므로, 해당 loss에 weight를 주는 것이 좋다. 각각에 $$T^2$$를 곱해서 적용해주자. (결국 hard target은 안곱한다는 말 아닌가..?)
  * softmax - cross entropy 식 미분해보니까  $$\frac 1 {T^2}$$으로 scaling된다.
  * 이게 hyper parameter를 변경하더라도 결국 sfot target, hard target의 relative contribution이 안바뀌도록 해준다.

### 2.1 Matching logits is a special case of distillation

* 먼저 Softmax - Cross Entropy 식의 미분은 [https://ratsgo.github.io/deep%20learning/2017/10/02/softmax/](https://ratsgo.github.io/deep%20learning/2017/10/02/softmax/)를 참고하자.

* Cross Entropy 계산 (v_i는 cumbersome model의 결과 logit)

  $$\frac {\partial C} {\partial z_i} = \frac 1 T (q_i - p_i) $$

  여기서 temperatrue가 충분히 높다면

  softmax 식의 $$exp(z_i / T)$$가 0에 가까워져 기울기가 1이므로 $$1 + z_i / T$$로 근사가 가능하다.

  $$\frac {\partial C} {\partial z_i} \approx \frac 1 T (\frac {1 + z_i / T} {N + \sum_j z_j / T} - \frac {1 + v_i / T} {N + \sum_j v_j / T} )$$

  여기서 logit이 zero-mean이라면 아래처럼 전개가 된다.

  $$\frac {\partial C} {\partial z_i} \approx \frac 1 {NT^2} (z_i - v_i)$$

* 그래서 높은 temperature에서는 distaillation이 $$1/2(z_i - v_i)^2$$을 minimize하는 것과 같다.
  * 어차피 gradient 계산할 때 $$T^2$$으로 scaling을 해주니 $$T^2$$항이 사라지는데,
  * $$\frac {\partial C} {\partial z_i} $$을 적분한 것이 loss와 같아야 하니 $$(z_i - v_i)^2$$항을 minimize해야 훈련이 된다는 것이다.
  * 여기서 알 수 있는 것은 절댓값이 크고 음수인 logits은 유용한 정보를 전달할 수 있다는 것이다.
* 낮은 temperature에서는 negative에 신경을 많이 쓰지 않도록 훈련이 된다.
  * 낮은 temperature의 경우에는 softmax 값 자체를 맞추려하기 때문인가???
  * 근데 이게 logit 값 자체가 엄청 noisy하기 때문에 좋은 점이 될 수 있는 있다.
* distilled model이 parent model의 정보를 다 담기에 너무 작다면 temperature를 작게 해보자. (large negative logit을 무시할 수 있도록)

## ---

* 3 Preliminary experiments on MNIST
* 4 Experiments on speech recognition
* 5 Training ensembles of specialists on very big datasets

위 장들은 읽어만 보자

## 6 Soft Targets as Regularizers

* soft target이 overfitting을 방지하는 방법 중 하나로 쓰일 수 있다.

## ------

그 뒤도 읽어만 보자
