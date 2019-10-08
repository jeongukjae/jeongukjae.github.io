---
layout: post
title: 🔪 Mecab을 살펴보자
tags:
  - nlp
---

[이 논문(Applying Conditional Random Fields to Japanese Morphological Analysis)](https://www.aclweb.org/anthology/W04-3230.pdf)을 참고해서 적어본다.

CRFs가 word boundary ambiguity가 존재할 때 어떻게 해결할 수 있는지를 보여준다고 하니, MeCab은 일본어를 word boudnary를 찾기 위해 시작한 프로젝트인 것 같다. 그리고 CRFs가 corpus based나 statistical한 일본어 morphological analysis(형태소 분석이라고 부르면 되려나?)에 있는 문제점들을 해결할 수 있다고 한다. hierarchical tagsets을 위한 flexible feature design이 가능해지고, label bias, length bias의 영향이 적어진다.

## 1. Introduction

일단 일본어는 중국어처럼 non-segmented language이다. 그래서 word boundary를 찾는 것이 word segmentation을 찾아내는 거나 POS Tagging하는 것에 매우 중요하다. CRFs를 쓰면 이 문제들을 풀어낼 수 있다. HMMs은 generative하기 때문에 hierarchical tagsets들로부터 나온 feature들을 사용하기 힘들다. suffix, prefix 같은 정보들이 예시이다. MEMMs은 label bias나 legnth bias를 해결하기 힘들다.

## 2. Japanese Morphological Analysis

word boundary를 찾는 가장 쉬운 방법은 character를 token으로 취급해서 Begin/Inside를 tagging하도록 만드는 것이다. (character based BI tagging) 하지만 이 것은 word segmentation에 대해 미리 정보가 있는 lexicon을 활용하기 힘들고, decoding 자체가 정말 많이 느려진다는 데 문제가 있다. (BI Tagging은 candidates를 많이 생성해놓아야 한다)

단어, 품세 페어를 포함하는 lexicon이 없는 것이 아니기 때문에 이를 활용하자는 것이 핵심인 것 같다. (MeCab을 원래 빌드할 떄 사전을 넣는 일이 크기도 하고)

어찌되었든, 일본어 morph analysis를 정리해보면 아래와 같다.

* let $$x$$ be an input, unsegmented sentence.
* let $$y$$ be a path, sequence of tuples containing word $$w_i$$ and pos $$t_i$$

  $$y = [(w1, t1,), ..., (wn, tn)]$$
* let $$\mathcal Y(x)$$ be a set of candidate paths in a lattice built from the input sentence $$x$$ and a lexicon
* let $$\hat y$$ be a corrent path by input sentence $$x$$

### 2.2.1. Hierarchical Tagset

