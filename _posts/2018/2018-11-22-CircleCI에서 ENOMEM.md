---
layout: post
title: "CircleCI에서 jest 사용할 때 ENOMEM이 뜨는 오류"
---

나는 보통 CI 서버를 CircleCI를 자주 이용하는 편인데, 그 이유는 private repo여도 어느정도 무료로 CI 서버를 구동할 수 있기 때문이다. 그래서 외주할 때도 간간히 쓰는데, VueJS/jest를 이용해서 frontend 외주를 하던 도중 CircleCI에서 아래와 같은 오류가 발생했다.

```
FAIL  some-test-file
  ● Test suite failed to run

    ENOMEM: not enough memory, read

      at Object.<anonymous> (node_modules/lodash/_baseMerge.js:4:21)
```

## 일단 구성부터 보자

일단 내 프로젝트는 아래와 같은 구성이다.

* vue@^2.5.17
* vue-jest@^3.0.0
* @vue/test-utils@^1.0.0-beta.25

그리고 아래처럼 테스팅을 한다

```shell
$ yarn test:ci
yarn run v1.10.1
yarn lint && yarn unit --coverage
...
...
...
vue-cli-service test:unit --coverage
```

뭐 그 외 다른 설정들도 있지만, 대충 이 정도만 기록한다.

## 문제 원인은?

일단 jest에는 이러한 [문서 (Tests are Extremely Slow on Docker and/or Continuous Integration (CI) server)](https://jestjs.io/docs/en/troubleshooting.html#tests-are-extremely-slow-on-docker-and-or-continuous-integration-ci-server)가 있다.

일단 이 [이슈 코멘트](https://github.com/facebook/jest/issues/1524#issuecomment-262366820)에서 말하는 대로 나 또한 circleci 에서는 테스트가 linting 테스트까지 포함해서 10분동안 오직 대기상태였다. 하지만 로컬에서는 코어M을 사용하는데도, 10초정도면 돌아가는 테스트들이었다.

일단 jest의 troubleshooting에 존재하는 위 문서(Tests are Extremely Slow on Docker and/or Continuous Integration (CI) server)는 아래처럼 말한다.

> In order to do this you can run tests in the same thread using `--runInBand`:
>
> ```shell
> # Using Jest CLI
> jest --runInBand
>
> # Using yarn test (e.g. with create-react-app)
> yarn test --runInBand
> ```
>
> Another alternative to expediting test execution time on Continuous Integration Servers such as Travis-CI is to set the max worker pool to ~4. Specifically on Travis-CI, this can reduce test execution time in half. Note: The Travis CI free plan available for open source projects only includes 2 CPU cores.
>
> ```shell
> # Using Jest CLI
> jest --maxWorkers=4
>
> # Using yarn test (e.g. with create-react-app)
> yarn test --maxWorkers=4
> ```

## 그래서 해결은?

CircleCI는 `2CPU/4096MB`의 리소스를 제공하기 때문에 나는 아래처럼 수정했다. (`--runInBand`나, `--maxWorkers=1`보다는 당연히 `--maxWorkers=2`가 성능이 좋겠죠?)

```json
{
  ...
  "scripts": {
    "lint": "run-s lint:all:*",
    ...
    "unit": "vue-cli-service test:unit",
    ...
    "test": "yarn unit",
    "test:ci": "yarn lint && yarn unit --maxWorkers=2 --coverage",
    ...
  },
  ...
}
```

그 뒤로는 잘 돌아간다.

{% include image.html url="/images/2018/11-22-enomem/s.png" alt="workflow가 성공했다!" description="workflow가 성공했다!" %}

이 오류는 이슈/문서에 적힌바에 의하면 Docker 컨테이너나 CI 서버에서 나타나는 오류라고 한다. (~~어차피 요즘 CI 서버들 docker에서 많이 돌리니까 그게 그거 아닌가...? 라고 생각하는데 그냥 넘어가자.~~) 일단은 자세한 문제 원인을 살펴보고 싶지만, 시간이 남으면서 이 포스트를 다시 볼 때 다시 하기로.
