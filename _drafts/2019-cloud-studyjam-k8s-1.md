---
layout: post
title: 2019 Cloud Studyjam 중급반(k8s) 1
tags:
  - devops
  - cloud
  - docker
  - gcp
  - kubernetes
  - studyjam
  - 커뮤니티
---

또 스터디잼에 참여하게 되었는데, 이번에는 [클라우드 스터디잼 중급반](https://sites.google.com/view/cloud-studyjam2/home)이다. 주제는 입문반과 똑같이 kubernetes이다. 스터디잼 소개 페이지에 학습 내용은 아래처럼 적혀있다.

> 입문반의 퀵랩에서 실습에 집중한 것과 다르게 쿠버네티스를 이해하기 위한 용어 및 개념 등을 학습합니다.

저번의 입문반의 내용은 주로 `kubectl`, docker, helm등을 어떻게 사용하는지에 대한 내용이었다. 이번에는 정말 이론적인 부분을 파고들 생각인가 싶어 참가하게 되었다. Coursera를 이용하며, [Getting Started with Google Kubernetes Engine](https://www.coursera.org/learn/google-kubernetes-engine?)이라는 강좌를 수강하게 된다. 해당 강좌를 수강하면서 배우는 내용을 정리해보려 한다.

## Week 1

강의 전체 오버뷰를 진행해주었는데, 간략하게 배우는 내용을 정리해보면 아래와 같다.

* Docker로 workflow들을 컨테이너화하는 방법
* 해당 컨테이너를 클러스터(Google Kubernetes Engine 사용)에 배포하는 방법
* 그 클러스터를 트래픽을 견디기 위해 스케일링하는 방법
* 해당 클러스터에 배포된 코드들을 업데이트/배포하는 방법

그리고 Docker에 대한 간략한 내용이 나온다. 하지만, 이전의 스터디잼에서 충분히 다룬 내용이므로 스킵! 다만 다시 본다고 가정한다면 볼만한 내용은 기존의 배포방식과 container를 사용하는 배포방식이 왜 다르고 효율적인지에 대해 설명하는 내용인 것 같다.
