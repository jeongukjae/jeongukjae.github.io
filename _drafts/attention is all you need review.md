---
title: "📃 Review of \"Attention Is All You Need\""
layout: post
tags:
  - nlp
  - paper
---

Transformer를 소개하는 논문으로, CS224n강의의 suggested readings 목록에 있어서 읽어본 논문이다. 한국어 리뷰도 엄청 많을 정도로 유명한 논문이다. 해당 논문을 읽고, 간략한 정리를 해보았다. 논문은 [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)에 있다.

## Abtract

Transformer는 기존과 다르게 완전히 attention만으로 이루어진 구조이다. 2014 WMT English-to-German translation task에서 sota를 찍은 모델이라고 한다.

## 1. Introduction & 2. Background

Recurrent Model은 순서가 중요하다는 특성상 병렬화하기가 어렵다. 하지만 이 transformer라는 Attention에 기반한 모델은 input과 output의 global dependency를 바로 뽑아낼 수 있기 때문에 병렬화하기 좋다. 따라서 sota인 모델을 P100 8대로 12시간만에 만들어낼 수 있었다. sequence-aligned RNN없이 완전히 self-attention (intra attention)만 사용하는 모델이다.

## 3. Model Architecture

{% include image.html url="/images/2019-06-09-transformer/1.png" description="Transformer architecture" %}

우선 Encoder-decoder structure를 가지고 있다. 하지만 stacked self-attention을 사용하고, point-wise feed forward network를 사용한다.

### Encoder

Encoder의 Layer 하나는 두 개의 sublayer로 되어 있으며, 첫번째는 multi-head self-attention mechanism을 가지고 있다. 두번째는 position-wise fully-connected feed-forward network를 사용한다. residual connection을 사용한 것을 그림에서 볼 수 있다. 논문에서 설명하길 하나의 sublayer를 $$\text{LayerNorm}(x + \text{SubLayer}(x))$$로 보라고 한다. 이런 layer 하나를 6개를 쌓았다.

### Decoder

여기다가 두개의 sublayer가 더 있다.
