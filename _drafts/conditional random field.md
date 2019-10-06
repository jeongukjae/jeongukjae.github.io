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

## Introduction

* HMMs and stochastic grammars are generative models
  * To define a joint probability over observation and label sequences, a generative model needs to enumerate all possible ob- servation sequences, typically requiring a representation in which observations are task-appropriate atomic entities, such as words or nucleotides
  * This difficulty is one of the main motivations for looking at conditional models as an alternative.
* A conditional model specifies the probabilities of possible label sequences given an observation sequence
  * Therefore, it does not expend modeling effort on the observations, which at test time are fixed anyway.
  * Maximum entropy Markov models (MEMMs) are condi- tional probabilistic sequence models
* In MEMMs, each source state1 has a exponential model that takes the observation features as input, and outputs a distribution over possible next states
  * MEMMs and other non-generative finite-state models based on next-state classifiers, such as discriminative Markov models (Bottou, 1991), share a weakness we call here the label bias problem
  * label bias problem: the transitions leaving a given state compete only against each other, rather than against all other transitions in the model
