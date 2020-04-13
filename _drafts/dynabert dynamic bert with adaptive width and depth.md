---
layout: post
title: "📃 DynaBERT: Dynamic BERT with Adaptive Width and Depth 리뷰"
tags:
  - paper
  - nlp
---

이 논문에서는 BERT, RoBERTa가 매우 좋은 성능을 보이지만, memory, computing power가 너무 많이 필요하므로 그를 압축해보는 방법을 제안한다. 아직 WIP인 논문이고, [https://arxiv.org/abs/2004.04037](https://arxiv.org/abs/2004.04037)가 링크이다.

## Abstract

* dynamic BERT Model 제안, width, depth 방향으로 dynamic함
* Knowledge Distillation 방식으로 full BERT 모델을 width adaptive BERT로 학습한 뒤, width, depth 모두 adaptive하게 학습함

## 1. Introduction

* 기존의 Transformer-based model을 압축하거나, 추론 가속화를 시도한 방법론들:
  * low-rank approximation
    * [ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://arxiv.org/abs/1909.11942)
    * [A Tensorized Transformer for Language Modeling](https://arxiv.org/abs/1906.09777)
  * weight sharing
    * [Universal transformers](https://arxiv.org/abs/1807.03819)
    * [ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://arxiv.org/abs/1909.11942)
  * knowledge distillation
    * [Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter](https://arxiv.org/abs/1910.01108)
    * [Patient knowledge distillation for bert model compression](https://arxiv.org/abs/1908.09355)
    * [Tinybert: Distilling bert for natural language understanding](https://arxiv.org/abs/1909.10351)
  * quantization
    * [Efficient 8-Bit Quantization of Transformer Neural Machine Language Translation Model](https://arxiv.org/abs/1906.00532)
    * [Q8bert: Quantized 8bit bert](https://arxiv.org/abs/1910.06188)
    * [Q-bert: Hessian based ultra low precision quantization of bert](https://arxiv.org/abs/1909.05840)
  * pruning
    * [Pruning Convolutional Neural Networks for Resource Efficient Inference](https://arxiv.org/abs/1611.06440)
    * [Pruning a BERT-based Question Answering Model](https://deepai.org/publication/pruning-a-bert-based-question-answering-model)
    * [Are sixteen heads really better than one?](https://arxiv.org/abs/1905.10650)
    * [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](https://arxiv.org/abs/1905.09418)
    * [Fine-tune BERT with sparse self-attention mechanism](https://www.semanticscholar.org/paper/Fine-tune-BERT-with-Sparse-Self-Attention-Mechanism-Cui-Li/a3ef6ee560e93e6f58be2b28f27aed0eb86dc463)
* 몇몇 리서치에서 depth adaptive models도 충분한 의미가 있음을 증명
* 최근의 리서치는 width direction도 충분히 redundant함을 말하고 있음
  * ex> Attention Head를 pruning해도 충분히 성능이 좋음
* CNN에서 width, depth - adaptive하게 모델을 만들어낸 시도가 있었지만, BERT에 적용하긴 힘들다.
  * Transformer 레이어 안의 Multi Head Attention과 Position wise Feed Forward Network 때문
* Training 방법
  * width adaptive BERT 학습 : attention heads랑 neuron 중 중요한 것들만 rewire한 뒤 distillation 진행
  * adaptive BERT 학습 : width adaptive BERT에서 initialize한 뒤에 width, depth 둘 다 distillation

## 2. Related Work

### 2.1. Transformer Layer

이거는 그냥 Transformer 설명임

### 2.2. Compression for Transformer/BERT

* Low Rank Approximation
  * weight matrix를 두 lower rank matrix의 곱으로 근사한다.
  * ALBERT는 embedding layer를 근사
  * Tensorized Transformer는 MHA 결과가 orthonormal base vectors로 표현 가능하다고 함 + multi-linear attention 사용
* weight sharing
  * Universal Transformer는 layer간 weight sharing
  * Deep Equilibrium Model은 특정 레이어의 input, output이 같아지게 함 -> ??? 모르겠다 찾아보자
  * ALBERT는 레이어간 parameter sharing이 network parameter를 안정적으로 만들게 해주고 좋은 성능을 얻는다고 함
  * 근데 model size는 줄어도 inference는 안빠름
* Distillation
  * DistilBert는 soft logit이랑 hidden states distillation 시킴
  * BERT PKD는 intermediate layer에 로스 줌
  * Tiny BERT는 general distillation, task-specific distillation으로 나눠서 진행함
* Quantizaiton
  * QBERT는 second order information을 활용해 각 레이어별로 몇 비트를 할당할 지 정함
    * steeper curvature에는 더 많은 bit 할당
  * Fully Quantized Transformer는 uniform min max quantization을 씀
  * Q8BERT는 quantization aware training + symmetric 8 bit linear quantizatio 활용함
* Pruing
  * "Fine-tune BERT with sparse self-attention mechanism"이란 논문에서 sparse self attention을 사용
  * "Compressing bert: Studying the effects of weight pruning on transfer learning"이란 논문에서 magnitude-based pruning 사용
  * LayerDrop에서는 transformer layer들의 추론을 위해 structed dropout을 적용함
* 근데 이 방법들 대부분이 압축과 관련된 거고 Universal Transformer나 LayerDrop, Depth-adaptive transformer도 압축이랑 가속에 신경쓰기는 하나 depth direction뿐이다.

## 3. Method

### 3.1. Training DynaBERT_w with Adaptive Width

* CNN과 비교해 BERT는 Transformers Layer가 쌓여있는 형태라 더 복잡
* MHA에는 linear transformation과  key, query, value의 곱이 존재함.

### 3.1.1. Using Attention heads and Intermediate Neurons in FFN to Adapt the Width

* MHA를 각 Attention 연산으로 분리한 다음 중요한 attention heads만을 취한다.
* 가장 중요한 순으로 Head와 Neuron을 왼쪽으로 몰아넣는다.

### 3.1.2. Network Rewiring

* "Pruning convolutional neural networks for resource efficient inference"와 "Analyzing multi-head self-attention: Specialized heads do the heavy lifting, the rest can be pruned" 에 따라서 importance score를 구함.
* 그런 다음 아래처럼 재구성함

{% include image.html url="/images/dynabert/fig1.png" %}

### 3.1.3. Training with Adaptive Width
