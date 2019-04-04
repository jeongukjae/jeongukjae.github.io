---
layout: post
title: Word2Vec
tags:
  - machine learning
  - nlp
  - paper
  - cs224n
---

CS224n을 듣기 시작하고 나서 같이 나오는 suggested readings를 가끔 읽는데, word2vec의 논문으로 유명한 [Efficient Estimation of Word Representation in Vector Space](https://arxiv.org/pdf/1301.3781.pdf)도 그 중 하나이다. 공부를 하면서 다시 볼만한 내용, 생각났던 내용들을 적어두기 위해 이 포스트를 작성했다.

## word2vec

word2vec는 word embedding 방법 중의 하나로, 논문에 제안한 모델에 대한 간략 설명으로 "for computing continous vector representations fof words from very large data"라고 적혀있다.

// TODO

## Introduction

2013에 나온 논문인데, 그 때의 많은 NLP 방법들은 단어를 하나의 작은 단위로 취급하고 있었다고 한다. 근데 이런 방법은 단어 사이의 유사도를 판별하기가 힘들다. 그리고 성능이 데이터의 크기에 크게 좌우된다. 하지만 어느정도 장점도 가지고 있는데, 간단하고 robust하며, 나름 좋은 성능을 냈다고 한다. Ngram이 그 중 하나라고 한다. [^ngram] 하지만 통계적인 방법을 이용하지 않고 기계학습을 사용한 방법을 이용하면서 distributed representation을 사용하는 방법이 꽤 좋은 접근법으로 떠올랐다고 한다. [^nnlm]

그래서 50 ~ 100정도 dimension에 word vector로 임베딩 하는 것을 소개한다. 그러면서 word vector의 놀라운 점을 소개한다. word2vec을 설명하다 보면 많이 나오는 단어를 더하고 빼는 연산을 아래처럼 예시를 보여주면서 소개한다.

> *vector(”King”) - vector(”Man”) + vec- tor(”Woman”)* results in a vector that is closest to the vector representation of the word Queen

단어를 연속적인 벡터로 표현하는 것이 이 논문이 처음은 아니다. 하지만 해당 방식을 제안했던 많은 논문들 중 NNLM에 관한 논문[^nnlm]에서 제안한 방식이 많은 주목을 받았다. feedforward neural network 방식을 사용한다고 한다.

## Model Architecture

neural network를 사용해서 distributed representation을 구현한다. 해당 아키텍쳐를 말하기 전에 computational complexity를 먼저 논한다고 한다. 모델을 소개하면서 어떻게 정확도는 높이고 complexity는 낮추었는지 소개해준다. 일단 앞으로 나올 모델들은 이런 training complexity를 갖는다고 한다.

$$ O = E \times T \times Q $$

$$E$$가 training epoch, $$T$$가 training set에 존재하는 단어의 수, $$Q$$는 앞으로 각 모델에서 정의될 것이라고 한다. 보통 epoch는 3 ~ 50으로 정하고, $$T$$는 1 billion까지로 정한다고 한다. 학습은 SGD와 backprop을 이용한다고.

### NNLM

NNLM은 input, projection, hidden, output layer로 구성이 되어 있다. input layer에서 $$V$$가 단어의 수라고 하면, 1-of-$$V$$ coding(one hot)을 사용해서 단어를 인코딩하고, 공유되는 projection용 행렬을 사용해서 $$N \times D$$ 차원의 projection layer로 project한다고 한다. $$N \times D$$ 차원이니까 한번에 $$N$$개의 단어를 사용가능하다. 보통 $$N$$은 10정도로 쓰고, projection layer는 500 ~ 2000 차원쯤 쓴다고 한다. hiddden layer는 500 ~ 1000차원쯤, output layer에 대해서는 $$V$$라고만 나와있다. 자 이렇게 되니까 파라미터 수는 아래와 같다.

$$ Q = N \times D + N \times D \times H + H \times V $$

$$ H \times V $$가 매우 비싼 연산이므로 hierarchical softmax를 사용한다고 한다. (이건 다음에 정리해야지) 또는 normalize를 안한다고. 어쩄든 그런 방법을 적용하면 $$ log_2 V$$ 정도로 줄어들어서 $$ N \times D \times H $$가 제일 complexity해진다.

word2vec에서는 huffman binary tree를 사용하는데, 이는 $$V$$를 $$log_2(Unigram\_perplexity(V))$$정도로 줄여준다고 한다. 이렇게 적어두고.. 사실은 $$V$$는 bottleneck이 아니니 그렇게까지 중요하진 않다고 한다.

### RNNLM



---

[^ngram]: [T. Brants et al. 2007](https://www.aclweb.org/anthology/D07-1090.pdf) Ngram의 논문으로 통계적인 방법론을 사용했다고 한다.
[^nnlm]: [A Neural Probabilistic Language Model](http://www.jmlr.org/papers/v3/bengio03a.html) word2vec의 NNLM에 관한 논문으로, distributed representation을 설명하며 참고로 달려있는 논문 중 하나이다.
