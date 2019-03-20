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

저번의 입문반의 내용은 주로 `kubectl`, docker, helm등을 어떻게 사용하는지에 대한 내용이었다. 이번에는 정말 이론적인 부분을 파고들 생각인가 싶어 참가하게 되었다. Coursera를 이용하며, [Getting Started with Google Kubernetes Engine](https://www.coursera.org/learn/google-kubernetes-engine?)이라는 강좌를 수강하게 된다. 해당 강좌를 수강하면서 배우는 내용을 정리해보려 한다. 일주일 분량의 강의이므로 각각 강의에 대한 내용을 추가하면서 작성한다.

## Overview

강의 전체 오버뷰를 진행해주었는데, 간략하게 배우는 내용을 정리해보면 아래와 같다.

* Docker로 workflow들을 컨테이너화하는 방법
* 해당 컨테이너를 클러스터(Google Kubernetes Engine 사용)에 배포하는 방법
* 그 클러스터를 트래픽을 견디기 위해 스케일링하는 방법
* 해당 클러스터에 배포된 코드들을 업데이트/배포하는 방법

그리고 Docker에 대한 간략한 내용이 나온다. 하지만, 이전의 스터디잼에서 충분히 다룬 내용이므로 스킵! 다만 다시 본다고 가정한다면 볼만한 내용은 기존의 배포방식과 container를 사용하는 배포방식이 왜 다르고 효율적인지에 대해 설명하는 내용인 것 같다.

## Kubernetes

쿠버네티스를 왜 사용할까? 강좌에서는 아래처럼 설명한다.

> Docker를 통해 하나의 어플리케이션을 모듈단위로 쪼개어서 containerize 한 다음에 각각을 같거나 다른 머신에서 구동시킬 수 있다. 하지만 이 때 "어떤 container가 어느 노드에 들어가야 하는지", "만약 실패한다면 어떻게 해야할지", "container 들을 디스크나 다른 container와는 어떻게 연결할지"는 구현하기 힘들다. 그래서 container ochestration system을 사용하는데 쿠버네티스도 그의 일종이다.

쿠버네티스를 통해서 위에서 말한 하기 힘든 일들을 처리할 수 있다. 그게 쿠버네타스를 사용하는 이유가 된다. 이제 쿠버네티스의 `Cluster`, `Node`, ...같은 기본 개념들을 설명한다. 하지만 이것도 저번 스터디잼에서 충분히 익혔으니까 스킵! 대신 나오는 개념만 적어두자

* Cluster
* Node
* Pod
* Service
* Label
* Selector

아래 리스트는 공부해야할 개념들

* Kubelet: 각각의 node에 돌아가는 node agent같은 느낌이다.
* ConfigMap
* SecretMap

### Volumes

Volume을 따로 비디오를 만들어서 설명해주는데, Volume을 사용해본적이 없어 한번 따로 정리를 할 필요성을 느꼈다.

docker는 container들에게 저장공간을 제공한다. 하지만 이 저장공간은 container 사이에 공유가 불가능하다. (가능하지 않나 싶지만 넘어가자 🤔) 그리고 그것보다 중요한 점은 lifecycle에 대한 지원이 미흡하다는 것이다.

하지만 쿠버네티스는 volume으로 container 사이의 데이터 공유를 지원하고, stateful하게 해준다. (stateful 하게 해준다는 내용이 한번에 이해가 되지 않으므로 더 찾아보자) 그리고 생성되는 방법같은 것은 volume의 type에 따라 달라진다. volume은 pod에 붙어서 pod이 online 상태가 되기 전에 준비된다. container에 한번 마운트되고 나면 Unix 파일 시스템을 다루듯이 다룰 수 있다.
