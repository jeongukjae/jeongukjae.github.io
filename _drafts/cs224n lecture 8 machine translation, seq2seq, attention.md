---
layout: post
title: 📕 CS224n Lecture 8 Machine translation, Seq2seq, Attention
tags:
  - nlp
  - cs224n
  - machine learning
---

CS224n 8번째 강의를 듣고 정리한 포스트! machine translation에 대해 살펴보고 seq2seq와 attention을 살펴본다.

## Machine Translation

### Pre-neural translation

일단 기계번역은 source language의 말들을 target language의 말로 옮기는 태스크이다. 1950's까지는 대부분 rule base로 구현했다. (사전을 이용한 mapping이 많았다) 1990's - 2010's statistical machine translatin 방식을 사용했다. data로부터 probability model을 사용했고, 이를 SMT라고 줄여부른다.

$$ argmax_y P(y|x) = argmax_y P(x|y)P(y) $$

$$P(x|y)$$
가 translation model이고 $$P(y)$$가 LM이다. 이러한 모델을 사용하면 정말 많은 데이터가 필요하다..

#### alignment

SMT에서는 alignment를 학습해야한다.
$$P(x,a|y)$$
로 나타내고, word를 매핑하고 나서 각각의 언어에 맞는 어순으로 배열하기 위해 alignment를 따로 학습한다.

{% include image.html url="/images/cs224n/8-1.png" description="alignment" %}

근데 어떤 단어들은 counterpart도 없고, align을 하는 것이 "one to many", "many to many", "many to one" 등등 실제로 매핑되지 않는 경우까지 너무 많아서 쉽지 않다. 확률적인 모델을 학습하는 것 자체가 모든 단어들을 돌아야 하는 것인데, 너무 계산 비용이 크다.

### NMT

자 그래서 NMT(neural machine translation)을 한다.

{% include image.html url="/images/cs224n/8-2.png" description="NMT" %}

이걸 seq2seq로 풀어낸다. 잠깐 seq2seq로 푸는 문제를 말해보자면, summarization, dialogue, parsing, code generation 같은 문제들이 있다. (conditional LM의 일종)

위처럼 `<END>`가 나올 때까지 계속하는데, 이게 안나타나면..? 이라는 생각을 했지만, 어느정도 리밋을 둔다는 말을 들었다.

decoding을 위처럼 하는 방식이 greedy decoding인데, 이게 문제점이 있다. 앞의 것만 보고 예측을 하니 그렇게 된다.

그래서 beam search decoding 방식을 사용하는데 아래와 같은 방법이다.

{% include image.html url="/images/cs224n/8-3.png" description="Beam Search Decoding" %}
