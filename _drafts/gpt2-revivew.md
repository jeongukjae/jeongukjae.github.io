---
layout: post
title: 📃 GPT2 리뷰
tags:
  - nlp
  - paper
---

GPT에 이어서 [GPT2 논문 (Language Models are Unsupervised Multitask Learners)](https://openai.com/blog/better-language-models/)도 간단하게 읽어보았다. 역시 정리하기에 귀찮은 부분은 다 건너뛴다.

## Abstract

원래 NLP를 수행할 때 task specific dataset에다가 supervised learning을 하는데, GPT2는 이런 supervision 없이 LM만으로 풀어보자고 하는 모델이다. 가장 큰 모델 GPT-2는 1.5B개의 파라미터를 가지는 Transformer로 WebText에 대해 다 학습이 안되었어도 테스트한 8개의 분야 중 7개에서 sota를 달성했다고 한다.

## 1. Introduction

Language task들에서 최근 좋은 성능을 모델은 pre-training과 superivsed fine-tuning의 조합으로 구성되는 모델인데, 이런 접근법이 더 유연한 방식으로 학습된 정보를 transfer하는 것이라고 한다. 첫번째는 Word2Vec처럼 word vector를 학습해서 task-specific architecture의 input으로 넣어주다가, recurrent network의 contextual representation을 사용하게 되고, 이제는 task-specific한 architecture없이 그냥 self-attention block을 계속 이어서 사용하게 되었다. 하지만 문제점은 이런 방식은 여전히 supervised training을 요구한다는 것이다. supervised training을 할 수 없을 때, 즉, supervised data가 없거나 매우 적을 때 사용할 수 있는 방법으로 LM을 특정한 태스크들을 위해 동작하게 만드는 방법이 있다.

그래서 GPT-2는 이 방법을 합쳐서 LM으로 엄청나게 학습시켜서 down-stream task들을 parameter 수정이나 architecture modification 없이 수행하게 만든다는 것이다.

## 2. Approach

일단 핵심은 LM이다. 그리고 언어는 natural sequential ordering이 있으니 joint probabilities를 conditional probabilities의 곱으로 factorize하는 것이 일반적이다.

$$ p(x) = \prod^n_{i=1} p(s_n\rvert s_1, ..., s_{n-1})$$

(근데 이거 $$s_n$$이 아니라 $$s_i$$아닐까...?) 여기서 conditional probability가 나왔으니까 이 것들을 잘 표현할 수 있는 self-attention arhictecture로 잘 계산한다.

근데 general system은 많은 태스크들을 수행할 수 있어야 하는데, 위 형태는 $$p(output \rvert input)$$ 밖에 수행을 못한다. 그래서 $$p(output \rvert input, task)$$와 같은 형태로 모델링을 한다고 한다. task conditioning은 보통 architectrure level에서 구현하는 것은 task specific encoders and decoders(Kaiser et al., 2017)와 같은 것을 살펴보면 될 것 같다. 그와 반대로 알고리즘 레벨에서 구현하는 것은 the inner and outer loop optimization framework of MAML (Finn et al., 2017)같은 것을 살펴보면 될 것 같다.

## 더 읽어보고 싶은 리스트

* Bengio, Y., Ducharme, R., Vincent, P., and Jauvin, C. A neural probabilistic language model. Journal of machine learning research, 3(Feb):1137–1155, 2003.
* Kaiser, L., Gomez, A. N., Shazeer, N., Vaswani, A., Parmar, N., Jones, L., and Uszkoreit, J. One model to learn them all. arXiv preprint arXiv:1706.05137, 2017.
