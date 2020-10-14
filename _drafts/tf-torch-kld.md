---
title: "Tensorflow와 Torch의 다른 KLDivergence"
layout: post
tags:
  - tensorflow
  - pytorch
---

얼마전에 Torch 학습 코드를 Tensorflow로 고쳐야 할 일이 있었는데, KLDivergence loss값의 스케일이 너무 다른 경우가 있었다.

https://github.com/pytorch/pytorch/blob/4d08930ccb1b27a74db796b0477f1aeebc031f0a/aten/src/ATen/native/Loss.cpp#L79-L120

https://github.com/tensorflow/tensorflow/blob/fcc4b966f1265f466e82617020af93670141b009/tensorflow/python/keras/losses.py#L1608-L1649
