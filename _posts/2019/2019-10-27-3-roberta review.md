---
layout: post
title: 📃 RoBERTa 리뷰
tags:
  - nlp
  - paper
---

[RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)라는 이름으로 Facebook AI와 UW에서 같이 낸 논문이다. 이번에도 그냥 정리하고 싶은 부분만 정리.

## Abstract

BERT가 좋은 성능을 내었지만, 이 연구팀에서는 아직 underfit인 상황으로 생각했다고 한다. 그리고 hyperparameter를 다시 선택해보고 replication study를 진행했다고 한다. 그리고 training data도 다시 정해서 학습을 했다.

## 1. Introduction

이 논문에서 제시하고자 하는 것은 간단하게 요약 가능한데 아래와 같다.

1. model을 더 오래 학습시키고, 더 큰 배치를 넣어주고 더 많은 데이터를 넣어준다.
2. NSP를 없애본다.
3. longer sequence를 넣어준다. (max sequence length를 늘린다는 말...?)
4. masking pattern을 다이나믹하게 해준다.

그리고 Introduction 섹션도 정리해주는데 그냥 그걸 읽었다.

1. BERT의 성능을 위해 training strategies를 다르게 잡았다.
2. novel dataset, CC-NEWS를 활용했고, 큰 데이터가 downstream task의 성능에 도움이 되는 것을 증명해냈다.
3. 그리고 MLM pretraining 모델이 짱이다.

## 2. Background

background라고 적어두고 BERT 정리다. 나중에 기억안나면 읽어야지.

## 3. Experimental Setup

### 3.1. Implementation

기본적으로 BERT의 training hyperparameter를 따랐다. peak learning rate랑 warm up step은 변경했다고 한다. 그리고 adam의 epsilon도 변경했고, $$\beta_2$$도 변경했다고 한다.

BERT는 간간히 short sequence를 넣은 것에 비해, RoBERTa는 Sequence는 대부분 max length 근처에 맞추도록 했다.

### 3.2. Data

RoBERTa는 가능한 한 많은 데이터를 모으는데 집중했고, 160GB 정도의 데이터를 모았다. (여기서 사실 좀.. 그랬다.. 10배나 데이터를 더 넣으니 물론 좋겠지..? 라는 생각?)

For our study, we focus on gath- ering as much data as possible for experimenta- tion, allowing us to match the overall quality and quantity of data as appropriate for each compari- son.

## 4. Training Procedure Analysis

BERT base와 같은 사이즈로 픽스해두고 진행했다고 한다.

### 4.1. Static vs. Dynamic Masking

같은 masking만 계속해서 쓰는 것을 방지하기 위해 training data를 10개로 복사하고 10가지 방식으로 masking을 했다. 그리고 40 epoch로 학습을 했으니 같은 masking을 네번만 보게했다.

static masking을 구현했을 때는 BERT랑 거의 같았고, dynamic masking을 했을 때에는 거의 비슷하거나 static masking보다 조금 더 나았다.

### 4.2. Model Input Format and Next Sentence Prediction

NSP와 같은 태스크를 BERT에서는 중요하다 했지만, (AlBERT에서도) 최근 연구들은 NSP가 정말 중요한지에 대한 의문을 제기하고 있다.

그래서 RoBERTa를 구현하면서 4가지 다른 방식으로 테스트를 해보았는데, BERT에서 말하는 sentence와 진짜 언어의 sentence를 비교했을 때는 진짜 언어의 sentence를 사용했을 때 downstream 태스크에서의 성능이 안좋아졌다고. 아마 long range deps를 학습하지 못해서인것 같다고 한다. 그리고 NSP loss를 없애니까 결론적으로 성능이 올랐다고 한다. 하지만 그럴 때 sequence pair를 구성하면 같은 문서에서 오게는 해줘야 한다고.

### 4.3. Training with large batches

최근 연구들이 BERT가 large batch에도 잘 동작한다고 한다. 원래 256 sequences로 1M step으로 학습시켰다고 한다. 이게 8k 배치로 31k step으로 학습시킨거랑, 2k 배치로 125k step으로 학습시킨거랑 똑같다. batch size를 늘려서 학습시켜본 결과 perplexity가 좋아졌고, parallel하게 학습하는 것도 편했다고.

### 4.4. Text Encoding

원래 BERT는 30k vocab으로 character-level BPE를 썼는데, heuristic tokenization rule이랑 함께 썼다. 근데 RoBERTa는 50k vocab으로 BPE를 사용했고, preprocess나 tokenization rule을 추가한게 없다고.

## 5. RoBERTa

이거 Robustly optimized BERT approach라서 RoBERTa라고 부른대요. dynamic masking 쓰고, full sentences without NSP loss 방법 쓰고, large mini batch 사용하고, large BPE 씁니다.
