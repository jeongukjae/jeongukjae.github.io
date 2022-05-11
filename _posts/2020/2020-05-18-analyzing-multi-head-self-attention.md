---
layout: post
title: "Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned 리뷰"
tags:
  - paper
---

이 논문 역시 MHA를 Pruning 하는 논문이다. English-Russian WMT dataset에서 48 encoder heads중 38개를 pruning해도 0.15 BLEU drop만 있었다고 한다. 코드는 [GitHub - lena-voita/the-story-of-heads](https://github.com/lena-voita/the-story-of-heads)에 공개되어 있고, Arxiv 링크는 [https://arxiv.org/abs/1905.09418](https://arxiv.org/abs/1905.09418)이다.

"Are Sixteen Heads Really Better than One?" 이랑 다르게 뭔가 NMT에서도 충분히 잘 된다를 말하는건가?

## 1 Introduction

이런 질문에서 출발

> * To what extent does translation quality de- pend on individual encoder heads?
> * Do individual encoder heads play consistent and interpretable roles? If so, which are the most important ones for translation quality?
> * Which types of model attention (encoder self-attention, decoder self-attention or decoder-encoder attention) are most sensitive to the number of attention heads and on which layers?
> * Can we significantly reduce the number of attention heads while preserving translation quality?

* [Ding et al., 2017](https://www.aclweb.org/anthology/P17-1106/)에서 말하는 layer wise relevance propagation으로 head의 중요성을 파악함
* 중요한 head는 세가지로 파악 가능
  * positional (attending to an adjacent token)
  * syntactic (attending to tokens in a specific syntactic dependency relation)
  * rare words (attending to the least frequent tokens)
* [Louizos et al., 2018](https://openreview.net/forum?id=H1Y8hhg0b)에 나온 방법을 기반으로 pruning 수행
* 결국 찾은 것은
  * 몇몇만 translation에 중요함
  * 중요한 헤드는 하나 이상의 specialized, interpretable 기능을 가짐
  * 여기서 말하는 긴으은 주변 단어/문법적인 단어에 attending 하는 것을 말함

## 2 Transformer Architecture

* 그냥 Transformer 설명은 패스
* ReLU 사용
* encoder self attention에 집중

## 3 Data and setting

* 정리 패스

## 4 Identifying Important Heads

* head의 confidence를 계산함
  * confident한 head는 하나의 토큰에 높은 attention을 건다
  * 직관적으로 이게 더 NMT에 중요한 것 같음
* LRP(Layer-wise relevance propagation)으로 top-1 logit에 기여하는 정도를 계산하고 그 순서대로 head를 정렬

## 5 Characterizing heads

### 5.1 Positional heads

* confidence가 매우 높음
* 특정 position에 attending함

### 5.2 Syntactic heads

* 가설: encoder는 syntactic structure 를 이해하는데 공헌이 클 것이다.
* 그래서 몇몇 head가 major syntactic structure를 잘 attend할 것이다.
* 그래서 이런걸 살펴봄
  * nominal subject (nsubj)
  * direct object (dobj)
  * adjectival modifier (amod)
  * adverbial modifier (advmod)
* CoreNLP (Manning et al., 2014)로 분석함
* 그래서 진짜 보니까 예를 들어 nsubj같은 경우는 토큰의 앞 n개의 토큰에 attending을 많이 한다.

### 5.3 Rare words

* 모든 모델에서 첫 레이어의 하나의 헤드가 엄청 중요함
* least frequent word에 대해서 attending함

## 6 Pruning Attention Heads

이거 실제로 수행하는 방법이 조금 긴데 정확하게 남기기 어려울 것 같아서 나중에 다시 보더라도 직접 읽어보는 것이 좋은 것 같다.

-> 패스

간단하게 적어보면, head masking하고, L0 regularization 적용하는데, 이게 미분가능하지가 않다. 그래서 Hard Concrete distribution을 적용했다. 그리고 Relaxation도 넣은 다음에 그 Relaxation의 가중치를 하이퍼파라미터로 가지면서 head 개수를 조절한다.

---

추가적으로 부록에 Layer-wise Relevance Propagation도 있으니 시간날때 살펴보자
