---
layout: post
title: "📃 Layer Normalization 리뷰"
tags:
  - paper
  - machine learning
---

Layer Normalization은 BERT에 쓰이는 것 때문에 찾아보게 된 논문이다. arxiv 링크는 [https://arxiv.org/abs/1607.06450](https://arxiv.org/abs/1607.06450)이다. training시간을 줄이는 것이 큰 기여인데, 이름에서 알 수 있듯이 neuron의 activity를 normalize하는 것이다. Batch Normalization도 비슷한 역할을 할 수 있지만 Batch Normalization은 min-batch에 dependent한 부분이 존재하고 recurrent network에는 적용하기 어렵다.

AdamW를 찾아보면, weight decay식을 볼 수 있는데 그 역할과 비슷하다고 생각할 수 있을 것 같다. Weight Decay를 하는 이유도 weight를 normalize해주기 위함인데, 이 논문은 weight 자체를 normalize하진 않지만, neuron의 output들의 Mean, Variance를 맞추어 주면서 normalize를 하게 된다.

## 1, 2

* 건너뜀

## 3 Layer Normalization

{% include image.html url="/images/2020-05-01-layer-norm/fig1.png" class='noshadow' %}

* layer 별로 mean, vairance를 구한 뒤 beta, gamma라는 learnable variable과 함께 recentering, rescaling해준다.

## 5 Analysis

* 이렇게 하면 특정 네트워크의 $$W$$와 $$W^\prime$$이 scale만 다르다고 해도 완전히 같은 output을 낼 수 있다.
* weight norm이 커지면 learning rate가 작아지는 효과를 볼 수 있다.
  * 그래서 implicit하게 early stopping과 비슷한 효과를 볼 수 있고, convergence가 더 안정적으로 된다.

---

이 뒤로는 전부 실험 내용. 전후로 riemannian metric, fisher information matrix와 관련된 설명이 너무 어려워서 다음에 다시 봐야겠다.
