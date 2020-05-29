---
layout: post
title: "📃 Lite Transformer with Long-Short Range Attention 리뷰"
tags:
  - paper
---

ICLR 2020 보면서 제일 재밌었던 논문 몇편도 앞으로 몇일간 리뷰를 올려보도록 하겠다. 이 논문은 한줄로 말하자면 transformer의 연산을 (특히 FFN + Attention을) 간단하게 만들어보는 논문이다. 논문/슬라이드/발표 영상은 [https://iclr.cc/virtual_2020/poster_ByeMPlHKPH.html](https://iclr.cc/virtual_2020/poster_ByeMPlHKPH.html)에서 볼 수 있다.

## Abstract

* Key Primitive: Long Short Range Attention (LSRA)
  1. Convolution Layer -> Local Context Modeling
  2. Atttention -> Long Distance Modeling
* machine translation, abstractive summarization, language modeling에서 improvement를 보여줌
  * NMT에서는 0.3 BLEU Score degradation을 수용할 경우 2.5x까지 computation을 줄일 수 있음
  * Quantization + Pruning까지 적용할 경우 18.2x까지 압축가능
  * LM은 500MACs(Mul + Add) 근처에서 1.8정도 perplexity 낮아짐

## 1 Introduction

* Mobile NLP에 적용가능한 모델
* Main Contribution
  1. Transformer의 연산 bottleneck을 찾고 해결
  2. 기존 transformer를 multi brnach feature extractor를 사용해 수정함
  3. mobile computation resource constraints에서도 좋은 성능을 보여줌
  4. AutoML 베아스인 Evolved Transformer와도 비교해보았더니 0.5정도 높은 BLEU score를 가져가면서 20,000x 정도의 CO2 배출량을 절약함
* main contribution-4는 AutoML이라 그런거 아닌가...?

## 2 Related Work

패스

## 3 Is bottelneck effective for 1-D attention?
