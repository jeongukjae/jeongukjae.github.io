---
layout: post
title: CS224n Lecture 10 (Textual) Question Answering
tags:
  - cs224n
---

드디어 10강을 정리한다. 기본적으로 QA시스템에 관한 설명이다.

* [강의 영상](https://www.youtube.com/watch?v=yIdF-17HwSk)

## Motivation

방대한 양의 full-text documents에서 단순히 관련있는 문서들을 찾아내는 것은 힘들다. 그리고 관련있는 문서를 question에 대한 answer로 받고 싶어한다.

이것을 두 파트로 나누어보면 아래와 같다.

1. finding document that might contain an answer
    * 이건 CS276을 참고하자
2. finding answer in a paragraph or a document
    * 이건 Reading comprehension과 관련이 있고, 이 부분에 대해서 이제 수업한다고 한다.

### Reading Comprehension

초기의 NLP때부터 연구되어오다가 2013년 MCTest[^MCTest]때 엄청 활발하게 연구되었다고 한다. MCTest가 Machine Comprehension에 관한 대회인 것 같은데, Machine Comprehension이 주어진 텍스트에 대해 질문이 주어지면, 좋은 답을 내어놓는 것이 주요 태스크라고 한다.

Passage (P) + Question (Q) -> Answer (A)

## SQuAD (Stanford Question Answering Dataset)[^SQuAD]

QA 시스템을 위한 오픈 데이터이고, 한번 나중에 자세히 살펴보아야겠다. 한국어버전으로는 [KorQuAD](https://korquad.github.io)가 있다. 1.0, 1.1에 관한 간략한 설명을 하고 2.0에 대한 설명도 한다.

1.0은 답이 passage안에 무조건 있었고, 시스템이 후보들을 고른 다음에 ranking만 하면 되었다. 그래서 해당 span이 답인지 아닌지를 확인할 필요가 없었다. 그래서 No Answer가 있는 것을 만들었다고 한다.

SQuAD는 무조건 span-based answer만을 가져오고, question이 무조건 passage를 위해서 구성된 것이면서, multi-fact/sentence inference는 거의 없다는 점이다. 그래도 well-targeted, well-structed, clean dataset이라고 한다. 나중에 한번 토이 프로젝트로 시도해보아도 좋을 듯 하다.

## Stanford Attentive Reader

* [Chen, Bolton, & Manning 2016](https://arxiv.org/abs/1606.02858)
* [Chen, Fisch, Weston & Bordes 2017](https://arxiv.org/abs/1704.00051)

위 논문 두개와 다른 하나가 더 있는데 \[Chen 2018]이라고만 되어있어서 뭔지 잘 모르곘다. 이건 나중에 간단하게 읽어보자. 자신들의 학교에서 만든 Reading Comprehension, QA 시스템을 보여주는 듯 하다..

{% include image.html url="/images/cs224n/10-1.png" description="The Stanford Attentive Reader 1" %}

{% include image.html url="/images/cs224n/10-2.png" description="The Stanford Attentive Reader 2" %}

Stanford Attentive Reader++도 있다고 하니 (이건 모델 그림이 많이 복잡해보이고 간단한 이해가 되지 않아서 그냥 미첨부) 나중에 더 살펴보자. (Chen et al., 2016; Chen et al., 2017)

## BiDAF (Bi-Directional Attention Flow for Machine Comprehension) [^BiDAF]

Attention을 양방향으로 사용하기 위한 구조의 논문. 메인 아이디어를 "the Attention Flow layer"라고 생각하면 된다.

## 그리고 또 다른 것들은

* [Dynamic Coattention Networks For Question Answering](https://arxiv.org/abs/1611.01604)
* [FusionNet](https://arxiv.org/abs/1612.05360)
* [DrQA](https://arxiv.org/abs/1704.00051) : Open domain QA

그리고 좀 중요하게 더 살펴보면 좋을 것

* [Elmo](https://arxiv.org/abs/1802.05365)
* [Bert](https://arxiv.org/abs/1810.04805)
* [SDNet](https://arxiv.org/abs/1812.03593) : Bert를 submodule로 사용한 에제

[^MCTest]: [Link](https://www.microsoft.com/en-us/research/publication/mctest-challenge-dataset-open-domain-machine-comprehension-text/) Machine Comprehension Test
[^SQuAD]: [arxiv](https://arxiv.org/abs/1606.05250) SQuAD에 관한 논문
[^BiDAF]: [arxiv](https://arxiv.org/abs/1611.01603) Seo, Kembhavi, Farhadi, Hajishirzi, ICLR 2017
