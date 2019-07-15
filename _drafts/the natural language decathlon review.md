---
layout: post
title: "📃 Review of \"The Natural Language Decathlon: Multitask Learning as Question Answering\""
tags:
  - nlp
  - cs224n
  - paper
---

decaNLP[^decanlp]라는 이름의 모델을 cs224n의 17강에서 엄청나게 들었다. saleforce에서 공개했다고도 하고, 기존의 NLP와 다르게 생각을 했다고 말하기도 해서 궁금해서 읽어보았다. 원래는 태스크별로 모델을 만드는데 여러개의 태스크를 하나의 모델로 처리한다고 하니..?

## Table Of Contents

* [Abstract](#abstract)
* [1. Introduction](#1-introduction)
* [2. Tasks and Metrics](#2-tasks-and-metrics)
* [3. Multitask Question Answering Network (MQAN)](#3-multitask-question-answering-network-mqan)
* [4. Experiments and Analysis](#4. Experiments and Analysis)
* [5. Related Work](#5. Related Work)

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

우선 decaNLP는 공개 dataset을 `(question, context, answer)`로 바꾸어서 각각의 task에 적용했다. 해당 task들을 차례차례 나열해 보자면,

### Question Answering

question과 필요한 정보가 포함된 context를 받으면 output으로 answer를 내는 task이다. [SQuAD](https://arxiv.org/abs/1606.05250)를 데이터셋으로 이용했다. metric은 nF1(normalized F1 Score)를 사용했다.

### Machine Translation

### Summarization

### Natural Language Inference

### Sentiment Analysis

### Semantic Role Labeling

### Relation Extraction

### Goal-Oriented Dialogue

### Semantic Parsing

### Pronoun Parsing

### The Decathlon Score

## 3. Multitask Question Answering Network (MQAN)

## 4. Experiments and Analysis

## 5. Related Work

## 내 생각

일단 Abstract를 읽었을 때, NLP를 오랜기간 배우진 않았지만 굉장히 특이한 접근법이라 생각했고, "과연 생각만큼 효율이 나올까?"라는 생각 때문에 자세히 읽어보았다.

[^decanlp]: [https://github.com/salesforce/decaNLP](https://github.com/salesforce/decaNLP) salesforce에서 공개한 범용 NLP 모델..? 정도이다
