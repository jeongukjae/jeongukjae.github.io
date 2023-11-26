---
layout: post
title: Negative Sampling 논문 정리해보기
tags:
  - paper
---

cs224n을 공부하면서 관련된 논문이 suggested readings에 있어서 천천히 읽어보는 중인데 이번에 읽은 논문은 negative sampling으로 유명한 [Distributed Representations of Words and Phrases and their Compositionality](http://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)이다.

## Introduction

원래 통계학을 활용한 많은 모델들이 좋은 성능을 보였는데, 그러던 중 neural net을 활용한 모델이 나오고, 더 좋은 성능을 보였지만, 수많은 matrix multiplication이 있다 한다. 그리고 더 최근에는 skip-gram같은 모델이 나오면서 matrix multiplication도 줄이면서 더 좋은 성능을 보이는 모델도 나왔다.

이 논문에서는 해당 skip-gram 모델의 여러 다른 방법을 보여준다고 한다. 자주 나오는 단어를 subsampling하거나, NCE(Noise Contrastive Estimation)을 적용해보거나, hierachical softmax도 적용해본다. 성능 테스트는 직접 analogical reasoning task를 만들었다고 한다. 예를 들어서 아래와 같이 테스트를 한다.

```text
"Montreal":"Montreal Canadiens"::"Toronto":"Toronto Maple Leafs"
```

## Skip-Gram 모델

### Hierarchical Softmax

Softmax는 컴퓨터의 연산량이 너무 많아서 근사시킨것이 hierarchical softmax이다. NNLM에서 처음 소개되었다. 일단 이점부터 말해보자면, 복잡도가 원래 $$W$$개의 output node를 연산하는 것 대신 $$log_2 (W)$$개의 output node만 계산해도 된다는 것이다.

HS는 binary tree representation을 사용한다. root에서 leaf로 가는 길에서 계속해서 확률을 곱해 선택해가면서 연산량을 줄이는 것이다. 자세히 알아본 것은 아니니, 다른 것을 참고하자 ㅠㅠ

실제로 HS를 사용해서 실험을 해보면 training time과 accuracy가 향상된다고 한다. binary huffman tree를 사용하면 더 짧은 코드로 더 빠른 학습이 가능하다 한다.

### Negative Sampling

hierarchical softmax대신, Noise Cotrastive Estimation(NCE)를 사용할 수 있다. NCE가 softmax의 log probability를 maxmize하는데, 그게 조금 비효율적이라, Negative Sampling(NEG)를 사용해 NCE를 간단하게 변환시켜서 사용할 수 있다고 한다. skip gram에서 `log P(w_O|w_I)`(바 때문에 자꾸 테이블로 바뀐다.. ㅠㅠ)를 다 치환한 아래 식을 objective로 사용한다.

$$ \log \sigma ({v'}_{w_O}^\intercal v_{w_I}) + \sum_{i=1}^k \mathbb{E}_{w_i \sim P_n(w)} [\log \sigma (-{v'}_{w_i}^\intercal v_{w_I})]$$

큰 데이터에 대해서는 k를 2 ~ 5정도로 선택하고 작은 데이터셋에 대해서는 k를 5 ~ 20정도로 선택한다고 한다.

NCE와 NEG의 다른 점은 NCE는 sample과 noise distribution의 numberical probabilities를 필요로 하고, skip-gram에 중요하지 않은 softmax의 log probability를 maximize하지만, NEG는 샘플만을 필요로 한다는 점이다. 훨씬 효율적이다.

실험에 대한 얘기도 간략하게 나와있는데, Unigram distribution의 3/4승을 사용할 때 제일 성능이 잘 나왔다고 한다.

### Subsampling of Frequent Words

in, the, a 같은 단어(frequent word)들은 일반적인 단어(rare word)들보다 훨씬 적은 정보를 준다. 그래서 이들을 일정확률로 빼고 훈련을 시켰더니, 어차피 frequent word들은 벡터값이 거의 바뀌지 않고, rare word는 훨씬 빠르게 학습되었다고 한다.

어떤 방식으로 제외를 시키냐면, 단어 $$w_i$$에 대해서 아래와 같은 확률로 제외를 시킨다.

$$ P(w_i) = 1 - \sqrt {\frac t {f(w_i)}} $$

$$f(w_i)$$는 각각의 단어의 빈도이고, t는 threshold이다. 대략 $$10^{-5}$$정도라고 한다.

## Empirical Results

HS, NCE, NEG, subsampling을 진행했다. analogy로 검증하는 작업은 syntactic(`quick:quickly::slow::slowly`같은)과 semantic으로 나뉘었다.[^word2vec]

뭐 실제 결과는 건너뛰었고 여기서는 코드 링크만 봤다.

[^word2vec]: [https://code.google.com/archive/p/word2vec/](https://code.google.com/archive/p/word2vec/) 자세한 코드는 여기를 참고하자
