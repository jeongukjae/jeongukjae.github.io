---
layout: post
title: GitHub Codespaces에서 Dev container 설정해보기
tags:
  - github
---

GitHub codespaces에서 dev container를 세팅해보았다. Codespaces를 별로 사용해보지 않아서, 우선 블로그 레포지토리를 기준으로 세팅해봤다.

## dev container 관련 Docs

* <https://code.visualstudio.com/docs/remote/devcontainerjson-reference>
* <https://github.com/microsoft/vscode-dev-containers/tree/main/containers/codespaces-linux>
  * GitHub codespaces에서 사용하는 이미지에 대한 설명

## 설정해보기

종합하면 [이 커밋 하나](https://github.com/jeongukjae/jeongukjae.github.io/commit/030970e02686336c6725f13b1fed8e97ca243058)로 설명이 되긴한다. 그래도 파일 단위로 살펴보자

### `.devcontainer/devcontainer.json`

레포지토리 루트 경로 혹은 `.devcontainer` 폴더 아래에 `devcontainer.json`을 두면 되는 것으로 보이고, 나는 `.devcontainer` 안에 넣어보았다.

```json
{
    "name": "Jekyll builder",
    "workspaceFolder": "/workspace",

    "build": {
        "dockerfile": "Dockerfile"
    }
}
```

굉장히 간단하게, Dockerfile 하나만 추가해놓았다.

### `.devcontainer/Dockerfile`

도커이미지는 [위의 링크로 달려있는 깃헙 코드 스페이스 기본 이미지](https://github.com/microsoft/vscode-dev-containers/tree/main/containers/codespaces-linux)를 활용해서 빌드했고, gem install 명령어만 하나 추가했다.

```Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/universal:1-linux

RUN sudo gem install jekyll-sitemap jekyll-feed jekyll-paginate
```

블로그 테마에서 이용하는 패키지만 gem으로 설치했다.

### 주의점?

`devcontainer.json`을 작성할 때 `build.dockerfile` 속성을 레포지토리 아래의 경로(`.devcontainer/Dockerfile`)로 주었다가 상대경로(`Dockerfile`)로 변경했다. 문서를 다시 보니, 아래처럼 잡는다고 한다.

> The path is relative to the `devcontainer.json` file.

세팅 후에는 한번씩 오른쪽 아래 알람으로 다시 빌드할 것이냐고 물어보는 창이 뜨는 것 같은데 Cmd + Shift + P 누르고 `Codespaces: Rebuild Container` 누르면 바로 빌드해볼 수 있다.

---

* 추가로 미리 port 정의해두고 코드스페이스 뜰 때 실행할 커맨드를 설정해둘 수 있는 것 같지만, 맛보기만 하려 했으니 패스!
