---
layout: post
title: "📃 Are Sixteen Heads Really Better than One? 리뷰"
tags:
  - paper
  - nlp
---

Multi head attention이 표현력이 좋고 많은 정보를 담을 수 있다지만, 모든 head가 필요한 것은 아니다. 이에 관한 논문이 Are Sixteen Heads Really Better Than One? (Michel et al., 2019)이고, arxiv 링크는 [https://arxiv.org/abs/1905.10650](https://arxiv.org/abs/1905.10650)이다.

## 1. Introduction

## 2. Background: Attention, Multi-headed Attention, and Masking

### 2.1. Single-headed Attention

### 2.2. Multi-headed Attention

### 2.3. Masking Attention Heads

## 3. Are All Attention Heads Important?

### 3.1. Experimental Setup

### 3.2. Ablating One Head

### 3.3. Ablating All Heads but One

### 3.4. Are Important Heads the Same Across Datasets?

## 4. Iterative Pruning of Attention Heads

### 4.1. Head Importance Score for Pruning

### 4.2. Effect of Pruning on BLEU/Accuracy

### 4.3. Effect of Pruning on Efficiency

## 5. When Are More Heads Important? The Case of Machine Translation

## 6. Dynamics of Head Importance during Training

## 7. Related work

## 8. Conclusion
