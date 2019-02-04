---
layout: post
title: "Kubernetes 패키지 매니저 Helm"
tags:
  - cloud
  - kubernetes
---

구글 클라우드 스터디잼을 진행하면서, [Helm](https://helm.sh)이라는 Kubernetes용 패키지매니저를 사용했었는데, 해당 패키지 매니저 문서를 살펴보다보니 생각보다 훨씬 이해해야할 것이 많아서 한번 정리를 하게 되었다.

## 우선 시작하기

Helm이 Kubernetes를 위한 패키지 매니저인만큼, 우선 Kubernetes부터 쓸 줄 알아야하는데, 저도 잘 모르기때문에 일단 해보는 걸로! 여튼 kubernetes가 정상적으로 돌아가는지 확인해봅시다.

```bash
$ kubectl config current-context
docker-for-desktop
```

Docker Desktop을 사용하고 있기 때문에 설정에서 간단하게 enable 시켜주는 것 만으로도 사용할 수 있었다. enable을 시키면 kubernetes를 구동시키기 위해 필요한 것들을 설치해준다.

{% include image.html url="/images/2019-02-04-helm/docker-desktop.png" alt="docker desktop의 kubernetes" description="docker desktop의 kubernetes" class='noshadow' %}

### helm 설치

Helm 설치는 OS별로 아주 상세하게 [helm 문서 - Installing Helm](https://docs.helm.sh/using_helm/#installing-helm)에 적혀있다. macOS에서는 homebrew가 설치되어 있다면 아래의 명령어로 helm을 설치할 수 있다.

```bash
$ brew install kubernetes-helm
Updating Homebrew...
...
...
```

#### 보안

자 근데 여기서 생각을 해야할 점은 helm의 tiller는 k8s의 cluster위에 올라가기 때문에 production용이나, 다른 사람과 같이 쓰는 cluster에서는 보안을 신경을 써주어야 한다! 하지만 난 개인 노트북에서 연습만 해보고 있으므로, 나중에 보자. [안전하게 Helm 설치하기](https://docs.helm.sh/using_helm/#securing-your-helm-installation)

### tiller 설치

자 그렇게 helm을 설치하고 나면, tiller를 설치해주어야 하는데, tiller는 아래처럼 설치한다.

```bash
$ helm init
Creating ...
...
...

Happy Helming!
```

몇몇 메시지가 뜨면서 잘 설치가 된다. 그리고 tiller를 업그레이드하려면 아래처럼 하면된다.

```bash
helm init --upgrade
```

#### tiller

자 근데 tiller 얘기를 계속했는데, tiller는 pod 형태로 설치되는 helm의 서버라고 생각하면 된다. helm이 client이고, tiller가 server인 한 쌍의 구조이다.

## 사용해보자

helm을 설치하고 나면 이제 helm의 chart를 이용해서 설치할 수도 있다.

```bash
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Skip local chart repository
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈ Happy Helming!⎈
```

그 전에 위의 명령어처럼 chart의 최신 버전을 들고오도록 해주자.

### Chart란

자 근데 chart란 말이 등장하는데 chart는 helm의 패키지의 형식이다. node js를 이용할 때 패키지 매니저를 이용하여 설치되는 패키지를 모듈이라고 부르듯이 k8s에서는 chart라고 부른다. chart에 대한 설명은 [kubernetes 문서](https://docs.helm.sh/developing_charts/)를 더 참고해보자.
