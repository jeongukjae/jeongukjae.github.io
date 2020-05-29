---
layout: post
title: "2019 클라우드 스터디잼 4~6 - kubernetes"
tags:
  - studyjam
---

저번의 1~3강에 이어서 그 뒤의 내용 정리

## 4강 - Managing Deployments with Kubernetes Engine

이거 그냥 배포해보고 kubectl 사용해보는 랩

### 4강 설정

프로젝트 : [GitHub - googlecodelabs/orchestrate-with-kubernetes: Orchestrating the Cloud with Kubernetes](https://github.com/googlecodelabs/orchestrate-with-kubernetes.git)

### kubectl

#### explain

```bash
kubectl explain [TOPIC]
```

위와 같은 형식으로 쓰면 설명해준다. `--recursive` 옵션 붙이면 밑으로 다 뽑아준다 심지어. 그리고 `.`으로 이어서 세부 항목 설명도 가능하다.

#### configmap

#### services

`svc`로 짧게 사용이 가능한가보다. 그리고 `-o` 옵션으로 출력값 조정이 가능하다. (jsonpath 문법에 대해서는 따로 한번 정리를 하자) 아래는 그 예시

```bash
$ kubectl get svc frontend -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"
35.224.55.215
```

#### scale

```bash
kubectl scale deployment hello --replicas=5
```

이렇게 replica를 바로 늘릴 수 있다.

```bash
$ kubectl get deployment
NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
auth       1         1         1            1           6m
frontend   1         1         1            1           5m
hello      5         5         5            5           5m
```

아래처럼 다시 되돌리면

```bash
kubectl scale deployment hello --replicas=3
```

아래처럼 줄어든다아아아아아

```bash
$ kubectl get pods
NAME                        READY     STATUS        RESTARTS   AGE
auth-6ccd6fd58c-7qphg       1/1       Running       0          7m
frontend-5f79fbf477-ghvlc   1/1       Running       0          6m
hello-c7f8d5464-2h4h6       0/1       Terminating   0          1m
hello-c7f8d5464-5g96w       1/1       Running       0          6m
hello-c7f8d5464-7j8xd       1/1       Running       0          6m
hello-c7f8d5464-n729b       1/1       Running       0          6m
```

### Rolling Update

> When a Deployment is updated with a new version, it creates a new ReplicaSet and slowly increases the number of replicas in the new ReplicaSet as it decreases the replicas in the old ReplicaSet.

새로운 버전을 배포할 때 새 replica를 만들고 기존 replica를 없앤다

```bash
kubectl edit deployment hello
```

```bash
$ kubectl get replicaset
NAME                  DESIRED   CURRENT   READY     AGE
auth-6ccd6fd58c       1         1         1         10m
frontend-5f79fbf477   1         1         1         10m
hello-5d479547f       2         2         0         7s
hello-c7f8d5464       2         2         2         10m
```

rollout 제대로 되었는지 검사함

```bash
kubectl get pods -o jsonpath --template='{range .items[*]}{.metadata.name}{"\t"}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
```

#### 그럼 롤백도?

```bash
kubectl rollout undo deployment/hello
```

```bash
$ kubectl get pods -o jsonpath --template='{range .items[*]}{.metadata.name}{"\t"}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
auth-6ccd6fd58c-7qphg		kelseyhightower/auth:1.0.0
frontend-5f79fbf477-ghvlc		nginx:1.9.14
hello-5d479547f-q4ncl		kelseyhightower/hello:2.0.0
hello-c7f8d5464-8ql5z		kelseyhightower/hello:1.0.0
hello-c7f8d5464-gsmmm		kelseyhightower/hello:1.0.0
hello-c7f8d5464-zsw4c		kelseyhightower/hello:1.0.0
```

잘 된다!

### Canary Update

> When you want to test a new deployment in production with a subset of your users, use a canary deployment. Canary deployments allow you to release a change to a small subset of your users to mitigate risk associated with new releases.

음.. ab 테스트 용도..?

```yaml
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello
        track: canary
```

### blue green

이건 blue 앱에서 green 앱으로 어떻게 전환하는지를 더 살펴봐야겠다… ㅠㅠ
아마 pods들을 services들로 묶어주면서, selector들로 그것들을 골라내는듯..?
그래서 service로 expose 한 후에는 종료를 따로 내가 시켜줘야하는 것 같다. (리소스를 많이 먹는다.)

## 5강 - Continuous Delivery with Jenkins in Kubernetes Engine

이건 진짜 너무 제목 그대로 Jenkins 써보는 랩...

### 설정

git repo: [GitHub - GoogleCloudPlatform/continuous-deployment-on-kubernetes: Get up and running with Jenkins on Google Kubernetes Engine](https://github.com/GoogleCloudPlatform/continuous-deployment-on-kubernetes.git)

### Helm

helm은 jenkins 설치용으로 설치한다. package manager란다. (k8s 어플리케이션 배포용) 그래서 그 중간에 `clusterrolebindng`, `serviceaccount` 등이 나오는데, 좀… 공부해야겠다… 그리고 helm 문서를 조금 보아야 할 것 같다. 이건 나중에 더 나오니까 나중에 한꺼번에 정리해야지.

```shell
$ helm install -n cd stable/jenkins -f jenkins/values.yaml --version 0.16.6 --wait
NAME:   cd
LAST DEPLOYED: Thu Jan 17 19:57:48 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/ConfigMap
NAME              DATA  AGE
cd-jenkins        4     5s
cd-jenkins-tests  1     5s

==> v1/PersistentVolumeClaim
NAME        STATUS  VOLUME                                    CAPACITY  ACCESS MODES  STORAGECLASS  AGE
cd-jenkins  Bound   pvc-ba31884b-1a46-11e9-b76b-42010a8000c6  100Gi     RWO           standard      5s

==> v1/ServiceAccount
NAME        SECRETS  AGE
cd-jenkins  1        5s

==> v1beta1/ClusterRoleBinding
NAME                     AGE
cd-jenkins-role-binding  5s

==> v1/Service
NAME              TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)    AGE
cd-jenkins-agent  ClusterIP  10.11.241.99   <none>       50000/TCP  5s
cd-jenkins        ClusterIP  10.11.243.148  <none>       8080/TCP   5s

==> v1beta1/Deployment
NAME        DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
cd-jenkins  1        1        1           0          5s

==> v1/Pod(related)
NAME                         READY  STATUS   RESTARTS  AGE
cd-jenkins-5bb9d7ccff-k76dx  0/1    Pending  0         5s

==> v1/Secret
NAME        TYPE    DATA  AGE
cd-jenkins  Opaque  2     5s


NOTES:
1. Get your 'admin' user password by running:
  printf $(kubectl get secret --namespace default cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
2. Get the Jenkins URL to visit by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "component=cd-jenkins-master" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8080
  kubectl port-forward $POD_NAME 8080:8080

3. Login with the password from step 1 and the username: admin

For more information on running Jenkins on Kubernetes, visit:
https://cloud.google.com/solutions/jenkins-on-container-engine
Configure the Kubernetes plugin in Jenkins to use the following Service Account name cd-jenkins using the following steps:
  Create a Jenkins credential of type Kubernetes service account with service account name cd-jenkins
  Under configure Jenkins -- Update the credentials config in the cloud section to use the service account credential you created in the step above.
```

막 저렇게 한꺼번에 쭉 뜨면서 설치됨. 근데 저기서 `NOTES`에 적혀있는 것 중 2에서 `kubectl port-forward $POD_NAME 8080:8080`으로 적으라고 하는데, 이게 loop가 계속 도는 것처럼 끝나질 않는다. 아마 그냥 소켓 listen 중인가보다. 그래서 뒤에 `>> /dev/null &` 붙여주면 좋다.
그리고 password는 위에 적혀있는 것처럼 `printf $(kubectl get secret --namespace default cd-jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo`로 찾자. 그럼 잘 뜬다.

### Namespace

aws에서 리소스 그룹 같은거 생각하면 될 것 같다. namespace 따라 전부 분리된다.

하지만 그 뒤로 전부 Jenkins 사용법이라 그냥 생략함

## 6강 - Running a MongoDB Database in Kubernetes with StatefulSets

이건 그냥 MongoDB 배포하고 사용해보는 것인데 이 랩에서 나오는 핵심 개념이 두가지 있다.

### Headless Service

`ClusterIP`를 할당하지 않는 서비스이다. 로드 밸런싱할 필요가 없고, IP도 필요가 없을때 사용할 수 있다고는 한다.

k8s 문서는 [여기](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)를 살펴보자

### StatefulSet

이 API object는 MongoDB Pod을 생성해서 사용할 때 썼는데, [k8s 문서](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)에서는 아래처럼 설명한다.

> Manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods.
>
> Like a Deployment, a StatefulSet manages Pods that are based on an identical container spec. Unlike a Deployment, a StatefulSet maintains a sticky identity for each of their Pods. These pods are created from the same spec, but are not interchangeable: each has a persistent identifier that it maintains across any rescheduling.

그냥 말 그대로 stateful한 어플리케이션들(데이터베이스나, 이미지 저장소같은?)을 위해 쓰는 기능이다. 사실 난 AWS를 주로 써서 많이 살펴볼 기능은 아닐 것 같지만.. 여튼 특이한 점은 StatefulSet은 Persistent Storage가 있는데, 이 디스크가 Pod가 종료되어도 종료되지 않는다. 아래의 인용은 [StatefulSet - Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)의 Limitation에 나와있다.

> Deleting and/or scaling a StatefulSet down will not delete the volumes associated with the StatefulSet. This is done to ensure data safety, which is generally more valuable than an automatic purge of all related StatefulSet resources.

이건 내가 세심하게 살펴보진 않았었지만, 스터디잼을 같이 진행하던 분이 "scale in을 하여도 persistent disk가 사라지지 않더라고요"라고 해주셔서 알게 되었다. 이것에 관한 것은 [Delete a StatefulSet - Kubernetes](https://kubernetes.io/docs/tasks/run-application/delete-stateful-set/#persistent-volumes)에 잘 나와있다. 아래와 같은 이유로 지워지지 않는다고 한다.

> Deleting the Pods in a StatefulSet will not delete the associated volumes. This is to ensure that you have the chance to copy data off the volume before deleting it.

그래서 StatefulSet과 Persisten Storage는 따로 따로 지워야 한다.

## 7 ~ 10

이게 7 ~ 10은 사실 쓸게 Helm 밖에 안보인다... 나중에 따로 Helm 쓰자.
