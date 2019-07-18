---
layout: post
title: "📃 Review of \"The Natural Language Decathlon: Multitask Learning as Question Answering\""
tags:
  - nlp
  - cs224n
  - paper
---

decaNLP[^decanlp]라는 이름의 모델을 cs224n의 17강에서 엄청나게 들었다. saleforce에서 공개했다고도 하고, 기존의 NLP와 다르게 생각을 했다고 말하기도 해서 궁금해서 읽어보았다. 원래는 태스크별로 모델을 만드는데 여러개의 태스크를 하나의 모델로 처리한다고 하니..? 전체를 살펴보진 않고 관심있는 부분정도만..?

## Abstract

single dataset, metric, task에만 맞춘 것이 아닌 범용적인 모델을 만들었다고 한다. 총 10개의 태스크를 시도했다. 아래 10개를 전부 question answering 처럼 변환해서 접근해서 task-specific한 파라미터나 모듈 없이 모든 태스크를 학습할 수 있었다고 한다.

1. question answering
2. machine translation
3. summarization
4. natural language inference
5. sentiment analysis
6. semantic role labeling
7. relation extraction
8. goal-oriented dialogue
9. semantic parsing
10. commonsense pronoun resolution

## 1. Introduction

{% include image.html url="/images/decanlp/1.png" description="예시 input. Question, Context, Answer로 이루어져 있다." %}

기본적인 아이디어는 모든 태스크를 QA처럼 다루는 것이다. 무조건 input은 context, question, answer를 받는다. 이런 아이디어를 검증하기 위해 baseline으로 s2s의 기본적인 컴포넌트들과 pointer network를 활용한 모델, attention network, curriculum learning등 다양한 모델들을 비교했다.

우선 결과부터 말하자면 MQAN(Multitask Question Answering Network)를 right anti-curriculum learning strategy를 이용해 학습시킨 성능과 각각 MQAN을 이용해 따로 학습시킨 성능이 비슷하게 나왔다. 이 외에도 decaNLP상에서 pretrain된 MQAN은 MT나 NER을 위해 transfer learning을 하는 것이나, sentiment analysis, natural langauge inference를 위해 domain adoption을 하는 것이나, text classification을 위해 zero-shot capability에도 성능 향상이 있었다. 코드는 [GitHub - salesforce/decaNLP](https://github.com/salesforce/decaNLP)에 공개되어 있다.

## 2. Tasks and Metrics

우선 decaNLP는 공개 dataset을 `(question, context, answer)`로 바꾸어서 각각의 task에 적용했다. 해당 task들 중 관심있는 task들만 차례차례 나열해 보자면,

### Question Answering

question과 필요한 정보가 포함된 context를 받으면 output으로 answer를 내는 task이다. [SQuAD](https://arxiv.org/abs/1606.05250)를 데이터셋으로 이용했다. metric은 nF1(normalized F1 Score)를 사용했다.

### Machine Translation

source language로 이루어진 input document를 받으면 target language로 만들어주는 것이 Machine Translation이다. International Workshop on Spoken Language Translation을 위해 만들어진 2016 English to German training data를 사용했다고 한다. metric은 corpus-level BLEU score를 사용했다.

### Sentiment Analysis

input text에 표현된 sentiment를 분석하는 task이다. Stanford Sentiment Treebank의 dataset을 사용했다고 한다. metric은 EM Score를 사용했다.

그 외에는 아래같은 Task들이 있었다.

* Summarization
* Natural Language Inference
* Semantic Role Labeling
* Relation Extraction
* Goal-Oriented Dialogue
* Semantic Parsing
* Pronoun Parsing
* The Decathlon Score

{% include image.html url="/images/decanlp/2.png" description="decaNLP에서 풀고자 하는 task들과 dataset, metric" %}

## 3. Multitask Question Answering Network (MQAN)

{% include image.html url="/images/decanlp/3.png" description="MQAN의 구조" %}

MQAN에서 풀고자 했던 점에 대해서 말해보자. 최근 많은 QA 모델이 answer는 context로부터 copy해올 수 있다고 믿는데, 이런 점은 general QA를 위한 모델을 만들어주진 못한다. question으로부터 올 수도 있고 그 외에서 올 수도 있다. 그래서 MQAN은 세 개의 input sequence를 받는다. context $$c$$, question $$q$$, 그리고 answer $$a$$. 모두 $$d_{emb}$$ 차원으로 embedding되어 있다. $$C$$는 $$l \times d_{emb}$$의 차원을, $$Q$$는 $$m \times d_{emb}$$의 차원을 $$A$$는 $$n \times d_{emb}$$의 차원을 가진다.

구조 그림의 중간에 보이는 encoder는 이 세 input sequence를 받아서 recurrent, coattentive, self-attentive한 layer에 넣어서 final repesentation을 만들어준다. 모델 최종단의 final distribution을 만들어주는 것이 아닌 attention layer 다음에 보이는 $$C_{fin}$$과 $$Q_{fin}$$을 만들어준다.

하나하나 뜯어보자면 아래정도와 같다.

### Answer Representation

Answer를 $$d$$ 차원으로 한번 projection시켜준 뒤, Positional Encoding을 진행해준다.

$$AW_2 = A_{proj} \in \mathbb R^{n \times d}$$

$$A_{proj} + PE = A_{ppr} \in \mathbb R^ {n \times d}$$

$$ PE[t, k] = \begin{cases} \sin(t / 10000^{k / 2d}) & k \text{ is even} \\ \cos(t / 10000^{(k - 1) / 2d}) & k \text{ is odd}  \end{cases}$$

그 후 그림에 나와있는 것처럼, self attention을 사용한다. Appendix C를 참고하면 더 자세하게 나와있다고 하지만, 그냥 [Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)을 참고하면 모든 것이 해결되는 것이 아닌가? 싶다. 중간중간 residual network도 엮어주었다.



## 4. Experiments and Analysis

## 5. Related Work

## 내 생각

일단 Abstract를 읽었을 때, NLP를 오랜기간 배우진 않았지만 굉장히 특이한 접근법이라 생각했고, "과연 생각만큼 효율이 나올까?"라는 생각 때문에 자세히 읽어보았다.

[^decanlp]: [https://github.com/salesforce/decaNLP](https://github.com/salesforce/decaNLP) salesforce에서 공개한 범용 NLP 모델..? 정도이다
