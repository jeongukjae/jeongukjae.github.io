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

single dataset, metric, task에만 맞춘 것이 아닌 범용적인 모델을 만들었다고 한다. 총 10개의 태스크를 시도했다.

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

위 10개를 전부 question answering 처럼 변환해서 접근했다.

## 1. Introduction

## 2. Tasks and Metrics

## 3. Multitask Question Answering Network (MQAN)

## 4. Experiments and Analysis

## 5. Related Work

[^decanlp]: [https://github.com/salesforce/decaNLP](https://github.com/salesforce/decaNLP) salesforce에서 공개한 범용 NLP 모델..? 정도이다
