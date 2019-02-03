---
layout: post
title: "2019 클라우드 스터디잼 1~3 - kubernetes"
tags:
  - cloud
  - gcp
  - kubernetes
  - studyjam
  - 커뮤니티
---

GDGKR(Google Developer Group Korea)라는 커뮤니티에 드문드문 나가게 되면서, 해당 커뮤니티 구성원 분들과 [2019 클라우드 스터디잼 입문반](https://sites.google.com/view/cloud-studyjam)[^cloud-studyjam]을 같이 하게될 기회를 얻었다. 그래서 아래는 스터디했던 내용. 스터디잼은 Qwiklab이라는 곳에서 특정 퀘스트를 완료하면 수료하게 된다. 퀘스트는 여러개의 랩(강의 하나로 생각)으로 이루어져있다.

- [참가했었던 팀의 스터디 내용 github repo (yangroro/cloud-studyjam-entry)](https://github.com/yangroro/cloud-studyjam-entry)

## 1강 - Introduction to Docker

Docker에 대해 설명을 해주는 랩이었다. 그래서 간단하게 통과

## 2강 - Hello Node Kubernetes

해당 랩은 Node JS 어플리케이션을 간단하게 만들어서 Docker Image로 만든 후, 해당 Image를 통해 k8s로 구동해보는 랩이다.

### 설정

```javascript
var http = require("http");
var handleRequest = function(request, response) {
  response.writeHead(200);
  response.end("Hello World!");
};
var www = http.createServer(handleRequest);
www.listen(8080);
```

```dockerfile
FROM node:6.9.2
EXPOSE 8080
COPY server.js .
CMD node server.js
```

이렇게 간단하게 만들어서 docker image를 만들자.

### Pod 만들기

Pod은 [k8s 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod/)를 살펴보면 알 수 있듯이 container[^container-of-pod]들을 모아놓은 하나의 그룹이다. 다만 단순히 모아놓기만 한 것은 아니고, 네트워크와 디스크를 공유한다. 특이한 점은 네트워크를 공유한다는 점이었는데, 아래와 같이 설명을 해놓았다.

> Containers within a pod share an IP address and port space, and can find each other via `localhost`. They can also communicate with each other using standard inter-process communications like SystemV semaphores or POSIX shared memory. Containers in different pods have distinct IP addresses and can not communicate by IPC without special configuration. These containers usually communicate with each other via Pod IP addresses.

즉, 하나의 Pod안에 있는 Container들은 IP와 Port를 공유하는데, `localhost`를 통해 접근이 가능하다고 한다. 또한 IPC(SystemV semaphore나, POSIX 공유 메모리 등)를 통해 접근할 수 있다고 한다. 하지만 보통 하나의 container만 가지는 pod을 생성하는게 일반적이고[^single-container-pod], 여러개를 생성하는 경우는 2개 또는 그 이상의 서비스가 서로 강하게 결합되어 있을때 사용한다고 한다. 예를 들어 두개의 서비스가 shared volume이 반드시 필요하다면 하나의 pod안에 두개의 서비스의 이미지를 넣어 같이 돌려주면 좋다고 한다.

Qwiklab에서는 간단하게 아래처럼 설명한다.

> A Kubernetes pod is a group of containers tied together for administration and networking purposes. It can contain single or multiple containers.

여튼 이 정도이고, docker image로 pod 만드는 방법은 아래와 같다. (정말 간단하게)

```bash
$ kubectl run hello-node \
    --image=gcr.io/PROJECT_ID/hello-node:v1 \
    --port=8080
deployment "hello-node" created
```

근데 deployment가 created 되었다고 나온다.

### Deployment

Deployment도 [k8s 문서](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)에 잘 나와있다. 대략적인 의미는 이해하겠지만, 정확하게는 이해못하겠다 ㅠㅠ

### 그래서 계속 해보자

근데 이게 만들어줬다고 끝나는게 아니고, 기본적으로 pod이 내부 네트워킹만 가능해서, external traffic을 하나 뚫어줘야 하는데, k8s의 service로 expose하는게 가능하다고 한다.

```bash
kubectl expose deployment [NAME_OF_POT] --type="LoadBalancer"
```

저거 `type` 플래그는 외부 IP 만들려고 필요하단다. 이건 나중에 설명해야지.

### Pod의 Scaling

k8s의 기능 중에 Pod을 scaling해주는 기능이 있다. Autoscaling도 존재하며, 수동으로 지정된 숫자만큼(desired state라고 부른다) scale out도 할 수 있다. 여튼 아래처럼 하면 hello-node deployment가 4개의 pod로 배포된다.

```bash
kubectl scale deployment hello-node --replicas=4
```

### Rolling Update

Rolling Update가 무중단 배포를 위해서 하나씩 교체해주는 거라 생각하면 된다. Qwiklab에서는 아래처럼 실제로 docker image의 태그를 수정해주었다.

```bash
kubectl edit deployment hello-node
```

근데 `latest`로 사용하는게 편하지 않으려나..? 싶어서 찾아봤다. ([참고한 문서](https://kubernetes.io/docs/concepts/containers/images/#updating-images)) `imagePullPolicy` 옵션을 `Always`로 두면, 이미지를 `latest`로 사용할 수 있다고 한다.

## 3강 - Orchestrating the Cloud with Kubernetes

이건 그냥 한번 개념 쭉 훑어보는 것 같다.

### Services

Pod은 시작하면 종료할 수 있고, 오류 또한 날 수 있어서, (그래서 IP가 계속 바뀔 수 있어서) 영속적이지 않기 때문에 Pod들을 묶어서 `service`라고 부르는 개념을 사용한다. service는 pod 묶음의 일정한 endpoint를 제공한다. Qwiklab에서 설명하는 service의 종류는 세가지였는데, `ClusterIP`, `NodePort`, `LoadBalancer`이다.

#### ClusterIP

클러스터의 내부 IP용으로 사용하는 서비스 타입이다. 클러스터 내부에서 접근이 가능하도록 하기 위해서 사용한다. 기본 service type이다.

#### NodePort

해당 노드(인스턴스?)의 IP의 고정적인 포트를 사용하기 위한 service type이다. NodePort를 위해 ClusterIP가 기본적으로 만들어진다. (아마 이게 ClusterIP를 만들고 그 내부 IP를 바로 포트로 expose 시키는 건가..?)

#### LoadBalancer

Cloud Provider(AWS, GCP, …)의 load balancer에서 쓸 수 있도록 expose한다. NodePort와 ClusterIP 서비스도 같이 만들어진다.

#### ExternalName

그 외 ExtenralName이라는 것도 있었는데, DNS의 CNAME 연결용인 것으로 보인다. 아마 이걸로 Expose해서 다른 서비스에서 사용하기 쉽게 하려고..?

### Label

Qwiklab을 진행하다보니 Label이라는 개념이 나왔는데, 그래서 찾아본 결과 문서에서 이렇게 설명한다.

> _Labels_ are key/value pairs that are attached to objects, such as pods. Labels are intended to be used to specify identifying attributes of objects that are meaningful and relevant to users, but do not directly imply semantics to the core system. Labels can be used to organize and to select subsets of objects.

pod을 organize 하기 위해서 사용할 수 있다고 한다.

---

[^cloud-studyjam]: url을 보니 나중에 같은 url로 다른 스터디잼 내용을 띄워주지 않을까 싶다.
[^single-container-pod]: https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/#understanding-pods 여기에 잘 나와있다.
[^container-of-pod]: https://kubernetes.io/docs/concepts/workloads/pods/pod/#what-is-a-pod 여기서의 container는 꼭 docker container만을 의미하지 않는다.
