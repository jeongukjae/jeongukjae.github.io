---
layout: post
title: "📃 Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding 리뷰"
tags:
  - paper
---

ICLR 2016에 나온 Deep Compression이라는 논문이다. 워낙 유명한 논문이다보니 빨리 빨리 읽어보려고 정리한다.

arxiv 링크: [https://arxiv.org/abs/1510.00149](https://arxiv.org/abs/1510.00149)

## Abstract

* pruning -> trained quantization -> huffman coding 으로 35x에서 49x까지 압축
* CPU, GPU, mobile GPU에서 3x, 4x 정도의 layerwise speedup
* 3x ~ 7x 정도의 에너지 효율성을 보임

{% include image.html url="/images/2020-05-27-deep-compression/fig1.png" class='noshadow' %}

## 1 INTRODUCTION

* mobile-first 회사들은 앱스토어나 플레이스토어가 "100MB 넘으면 와이파이 써서 다운로드해야 함"같은 메시지를 띄우는 것처럼 모바일 앱 사이즈에 매우 민감함
* energy consumption에도 매우 민감함
  * 근데 이게 memory access때문에 많이 소비한다.
  * > Under 45nm CMOS technology, a 32 bit floating point add consumes 0.9pJ, a 32bit SRAM cache access takes 5pJ, while a 32bit DRAM memory access takes 640pJ, which is 3 orders of magnitude of an add operation.

## 2 NETWORK PRUNING

* Connectivity 학습 -> small weight connection pruning -> 다시 학습
* 이걸로 AlexNet이랑 VGG 16을 9x, 13x 줄임
* 그래서 Sparse Structure를 가질 수 밖에 없는데, 이걸 Compressed Sparse Row, Compressed Sparse Column 형태로 저장함

## 3 TRAINED QUANTIZATION AND WEIGHT SHARING

* 이 부분에 대해서 더 읽어보자. 이거 잘 이해가 안간다.
* Conv 레이어에 대해서 8-bit로 quantize하고, FC 레이어에 대해서 5 bit로 quantize함.
