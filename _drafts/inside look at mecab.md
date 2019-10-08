---
layout: post
title: 🔪 Mecab을 살펴보자
tags:
  - nlp
---

[이 논문(Applying Conditional Random Fields to Japanese Morphological Analysis)](https://www.aclweb.org/anthology/W04-3230.pdf)을 참고해서 적어본다.

CRFs가 word boundary ambiguity가 존재할 때 어떻게 해결할 수 있는지를 보여준다고 하니, MeCab은 일본어를 word boudnary를 찾기 위해 시작한 프로젝트인 것 같다. 그리고 CRFs가 corpus based나 statistical한 일본어 morphological analysis(형태소 분석이라고 부르면 되려나?)에 있는 문제점들을 해결할 수 있다고 한다. hierarchical tagsets을 위한 flexible feature design이 가능해지고, label bias, length bias의 영향이 적어진다.

## 1. Introduction

일단 일본어는 중국어처럼 non-segmented language이다. 그래서 word boundary를 찾는 것이 word segmentation을 찾아내는 거나 POS Tagging하는 것에 매우 중요하다. CRFs를 HMMs(hidden Markov models)과 같이 쓰거나 MEMMs(maximum entropy Markov models)과 같이 쓰면 이 문제들을 풀어낼 수 있다. HMMs은 generative하지만, MEMMs은
