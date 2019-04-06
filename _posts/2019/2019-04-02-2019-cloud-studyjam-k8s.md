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

저번의 입문반의 내용은 주로 `kubectl`, docker, helm등을 어떻게 사용하는지에 대한 내용이었다. 이번에는 정말 이론적인 부분을 파고들 생각인가 싶어 참가하게 되었다. Coursera를 이용하며, [Getting Started with Google Kubernetes Engine](https://www.coursera.org/learn/google-kubernetes-engine?)이라는 강좌를 수강하게 된다. 해당 강좌를 수강하면서 배우는 내용을 [쿠버네티스 마스터](https://book.naver.com/bookdb/book_detail.nhn?bid=13799840)라는 책과 같이 읽어보면서 정리해보려 한다. 이 책을 선택한 이유는 특별한 이유가 있다기 보다는 회사에 있어서..이다. 일주일 분량의 강의이므로 각각 강의에 대한 내용을 추가하면서 작성한다.

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

쿠버네티스를 통해서 위에서 말한 하기 힘든 일들을 처리할 수 있다. 그게 쿠버네타스를 사용하는 이유가 된다.

책에서는 k8s를 이렇게 설명한다. 예전의 서버를 다루는 것은 애완동물을 다루는 것처럼 소수를 애지중지하면서 다뤄왔다면, k8s를 통해 서버를 다루는 것은 소 떼를 몰아가는 것과 같다고. 개별 서버를 모두 소중히 다룰 수가 없는 대규모의 환경에 적합한 k8s인만큼, 하나의 집단으로 보고 다루어야 한다는 것이다.

### Basic Concepts

이제 쿠버네티스의 `Cluster`, `Node`, ...같은 기본 개념들을 설명한다.

#### [Node](https://kubernetes.io/docs/concepts/architecture/nodes/)

node는 단일 호스트로 kubernetes cluster의 worker와도 같은 개념이다. 예전에는 minion으로 불렸다고 한다. 각각의 node는 [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)과 [kube proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) 등 여러 k8s 컨테이너를 실행한다. node는 VM일수도 있고, 물리 머신일수도 있다.

#### [Master](https://kubernetes.io/docs/concepts/#overview)

Kubernetes의 master는 하나의 노드에서 아래의 세개가 동작한다.

* [kube-apiserver](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
* [kube-controller-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)
* [kube-scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)

이런 세개의 프로세스들은 보통 GKE, EKS 등을 사용할 때는 cloud provider가 직접 관리해준다고 한다.

#### [Volume](https://kubernetes.io/docs/concepts/storage/volumes/)

Coursera 강의에서 Volume을 따로 비디오를 만들어서 설명해주는데, Volume을 사용해본적이 없어 한번 따로 정리를 할 필요성을 느꼈다.

docker는 container들에게 저장공간을 제공한다. 하지만 이 저장공간은 container 사이에 공유가 불가능하다. (가능하지 않나 싶지만 넘어가자 🤔) 그리고 그것보다 중요한 점은 lifecycle에 대한 지원이 미흡하다는 것이다. 하지만 쿠버네티스는 volume으로 container 사이의 데이터 공유를 지원하고, stateful하게 해준다. 그리고 생성되는 방법같은 것은 volume의 type에 따라 달라진다. volume은 pod에 붙어서 pod이 online 상태가 되기 전에 준비된다. container에 한번 마운트되고 나면 Unix 파일 시스템을 다루듯이 다룰 수 있다.

책에서는 이렇게 설명한다.

문서에는 이렇게 적혀있다. Docker도 [volume](https://docs.docker.com/storage/)의 개념이 있지만, 조금 looser & less managed 된다고 한다. Docker에서는 그저 디스크나 다른 컨테이너 상의 디렉토리일뿐이다. 그래도 발전을 계속하고 있지만, 많이 제한되어 있다.

volume의 종류는 아래같은 것들이 있다.

* `awsElasticBlockStore`
* `azureDisk`
* `configMap`
* `emptyDir`
* `hostPath`
* `local`
* `persistentVolumeClaim`
* `secret`

그 외에도 정말... 많은데, 선택이나 연결은 사용자에게 맡기는 듯 싶다. aws ebs나, azure에서의 disk 같은 것들을 mount할 수 있게 해주거나, [`emptyDir`](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)처럼 Pod이 생성될 때 이름처럼 정말 Empty 한다음에 Pod이 꺼질때 사라지는 그런 Volume도 있다. 물론 [`hostpath`](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath)처럼 host에 mount 할 수 있고, 그와 잘 구분이 가질 않는 [`local`](https://kubernetes.io/docs/concepts/storage/volumes/#local)같은 타입의 volume도 있다. 또 그냥 신경안쓰고 cloud provider에서 제공하는 디스크를 붙일 수 있도록 [`persistentVolumeClaim`](https://kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) 같은 것도 있다. 이건 `persistentVolume`을 pod에 마운트하기 위해 쓰이는데 실제 어떤 디스크인지 신경쓰지 않고 `persistentVolume`인것만을 확신하고 싶을때 사용하는 것 같다. (이름대로 claim)

또 정말 특이하게 `configMap`이랑 `secret`도 있다. 이름대로 [`configMap`](https://kubernetes.io/docs/concepts/storage/volumes/#configmap)은 말 그대로 어플리케이션 설정을 위한 volume 타입이고, [`secret`](https://kubernetes.io/docs/concepts/configuration/secret/)은 자격증명/토큰 등등을 저장하는 volume이다.

`secret`에 대해 더 적어보자면, 얘는 volume 같은 형식으로도 사용이 가능하고 env var로도 사용이 가능하다. [^using-secrets] 그리고 api server에서는 (master) [`etcd`](https://github.com/etcd-io/etcd)에 저장되고, kubelet에서는 (worker, node) 에서는 tmpfs에 저장한다.

---

이 뒤로는 CI / CD와 관련된 내용이므로, 다른 포스트에 정리해야할 것 같다.

[^using-secrets]: [https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets) pod에 환경변수로 노출시킬 수 있다고 한다.
