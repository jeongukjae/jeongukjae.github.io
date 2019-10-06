---
layout: post
title: "📃 Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data"
tags:
  - nlp
  - paper
---

MeCab을 한국어를 위해 새로 작성해보고 싶어서 [그 논문(Applying Conditional Random Fields to Japanese Morphological Analysis)](https://www.aclweb.org/anthology/W04-3230.pdf)을 찾아보았더니, CRF based segmentation이라고 불러서 CRF에 대해 우선 정리한다. ~~(프로 야크 쉐이버)~~

대충 MeCab 관련 글들을 보니 [이 논문(Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data)](https://repository.upenn.edu/cgi/viewcontent.cgi?article=1162&context=cis_papers)이 제일 연관있어 보여서 이거로 정리해본다.

---

## Abstract

CRFs는 Hidden Markov model에 비해서도 몇몇 이점들이 있고, CRFs는 MEMMs(Maximum entropy Markov models)의 기본적인 한계를 극복할 수도 있고,다른 directed graphical model들의 기반인 discriminative Markov modl들의 한계도 극복할 수 있다. 이 논문에서 CRFs를 위한 iterative parameter estimation algorithm을 여기서 제시한다. 그리고 그 결과를 HMMs와 MEMMs과 비교한다.

## 1. Introduction

HMMs이랑 stochastic grammers는 generative model인데, 이게 joint prob을 observation과 label sequence에 대해 정의하기 위해서 모든 가능한 observation sequence에 대해서 계산을 해야하기 때문에 조금.. 그렇다. 그래서 이런 복잡도가 conditional field를 사용하게 된 원인이라고 한다.

conditional model은 오로지 given observation sequence에 대해 가능한 label sequence의 prob을 계산한다. 이게 observation 찾으려고 애쓰지 않아도 되어서 좋다고 한다. MEMMs이 conditional probabilistic sequence model이라고.

MEMMs은 각각의 source state가 exponential model인데, observation features를 입력으로 distribution over possible next states를 출력으로 낸는 모델이다. 근데 MEMMs이나 non-generative, finite-state, next-state classifiers based인 모델(discriminative Markov model같은)은 label bias problem이 있다. 일단 transition score는 이전의 state에서 이 state로 올 확률인데, 이미지를 따오기 귀찮아서 글로만 설명하자면, 하나의 state에서 다른 state로 이동할 확률의 총합이 1이다. 그래서 path가 계속 늘어날 수록 총 score는 계속 낮아지는데, 그래서 진짜진짜 안좋은 경우에는 single outgoing path가 되게 길지만 좋은 path를 이길 수도 있다.

여기서 소개하는 CRFs는 sequence modeling frameowrk인데, MEMMs의 이점을 가져오면서 label bais problem을 푼다. 가장 중요한 차이점은 MEMM은 per-state exponential model인데, CRF는 single exponential model이다.

CRF는 unnormalzied transition probabilites를 가지는 finite state model이다. 하지만 다른 weighted fininte-state approaches와는 다르게 CRF는 possible labeling에 대해 well-defined probability distribution을 배정한다. 그리고 loss function이 convex 이고 global optimum으로 convergence를 보장한다.

그래서 이 모델의 두가지 학습 방법을 소개하고, convergence의 증명을 소개한다고 한다.

## 2. The Label Bias Problem

일단 넘기고 나중에 필요하면 볼래요.

## 3. Conditional Random Fields

* $$X$$ : random variable over data sequence to be labeled
* $$Y$$ : random variable over corresponding label sequence
* $$\mathcal {Y}$$ : range over a finite label

그냥 $$X$$가 natural language sentence이고, $$Y$$가 POS tagging 한거라 생각하면 될것 같아요. $$\mathcal Y$$는 가능한 POS 태그 전부..?

CRF는 random field globally conditioned on the observation $$X$$이고, $$Y$$와 $$X$$는 jointly distributed이다. 그래서 jointly didstribution over the label sequence $$Y$$ given $$X$$는 아래와 같아진다.

$$p_\theta (y|x) \propto \exp(\sum_{e \in E, k} \lambda_k f_k (e, y|_e, x) + \sum_{v\in V, k} \mu_kg_k(v, y|_v, x))$$

$$x$$는 data sequence이고, $$y$$는 label sequence이다. feature function인 $$f_k$$와 $$g_k$$는 고정되어있다고 한다. $$Y$$의 graph $$G = (V, E)$$는 tree 형태이다.

parameter estimation은 $$\theta = (\lambda_1, \lambda_2, ... ; \mu_1, \mu_2, ...)$$을 training data $$ \mathcal D = \{(x^i, y^i)\}^N_{i=1} $$로부터 결정하는 problem이다.

Objective function은 아래와 같다.

$$\mathcal O (\theta) = \sum^N_{i=1} \log p_{\theta} (y^i | x^i) \propto \sum_{x, y} \tilde p (x, y) \log p_{\theta} (y|x)$$

{% include image.html url="/images/crf/fig2.png" description="HMMs, MEMMs, chain-structed case of CRFs를 순서대로 나타낸 graphical structures. open circle은 모델에서 만들어진 게 아니다." %}

근데 위 이미지에서 chain-structed case of CRFs라고 적어놓았는데, 이 논문에서 주로 다루는 것은 chain-structed case of CRFs이다.

표현을 단순하게 하기 위해서 start, stop state를 넣어준다고 한다. BOS, EOS 같은 토큰인가보다. $$Y_0 = \text{start}$$, $$Y_{n+1} = \text{stop}$$이다.

chain structure에서 label의 conditional prob은 matrix form으로 나타낼 수 있다. 이건 parameter estimation이랑 inference에서 엄청 유용하다는데 이건 또 다음 섹션에서..

$$p_\theta (Y\rvert X)$$가 CRF라고 할 때, observation sequence $$x$$의 각 position $$i$$에 대해 $$\rvert \mathcal Y \rvert \times \rvert \mathcal Y \rvert$$ matrix random variable $$M_i (x) = [M_i(y', y\rvert x)]$$를 정의한다.

$$M_i (y', y\rvert x) = \exp (\Lambda_i (y', y \rvert x))$$

$$\Lambda_i (y', y \rvert x) = \sum_k \lambda_k f_k (e_i, Y\rvert_{e_i} = (y', y), x) + \sum_k \mu_k g_k (v_i, Y \rvert_{v_i} = y, x)$$

$$e_i$$는 edge with labels $$(Y_{i-1}, Y_i)$$이고 $$v_i$$는 vertex with label $$Y_i$$이다.

normalization (partition function) $$Z_\theta(x)$$는 위의 모든 matrices들의 곱의 $$(\text{start}, \text{stop})$$ entry이다.

$$Z_\theta (x) = (\prod_{i=1}^{n+1} M_i (x))_{\text{start, stop}} $$

위를 이용하면 $$y_0 = \text{start}$$, $$y_{n+1} = \text{stop}$$일 때 아래처럼 다시 쓸 수 있다.

$$p_\theta(y \rvert x) = \frac {\prod^{n+1}_{i=1} M_i(y_{i-1}, y_i \rvert x)} {Z_\theta (x)}$$

## 4. Parameter Estimation for CRFs

두개의 iterative scaling algorithm을 소개하는데, 둘 다 improved iterative scaling algorithm of Deela Pietra et al.(1997)에 기반한다.

Iterative scaling algorithm은 weights를 $$\lambda_k \leftarrow \lambda_k + \delta \lambda_k$$랑 $$\mu_k \leftarrow \mu_k + \delta \mu_k$$로 한다.

---

이 이후로는 Viterbi algorithm처럼 inference에 필요한 알고리즘을 먼저 알아야 할 것 같아서 일단 Pending..
