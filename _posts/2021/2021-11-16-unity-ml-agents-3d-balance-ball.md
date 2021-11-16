---
layout: post
title: "Unity ML-Agents로 3DBalanceBall 예제 돌려보기"
tags:
  - unity
---

Unity ML Agents라는 것을 보고 [3D Balance Ball 예제](https://github.com/jeongukjae/ml-agents-3d-balance-ball)를 돌려보았다.

{% include image.html url="https://github.com/jeongukjae/ml-agents-3d-balance-ball/raw/main/example_image.png" alt="요약 이미지" description="요약 이미지" width=80 %}

## ML Agents

[GitHub Unity-Technologies/ml-agents](https://github.com/Unity-Technologies/ml-agents)에 존재하는 ml agent이고, Unity를 시뮬레이션 환경으로 이용하면서 RL 등의 머신러닝 알고리즘을 쉽게 돌릴 수 있도록 제공하는 프로젝트인 것으로 보인다. RL 배우는 사람들에게 익숙한 gym까지 환경을 구성할 수 있도록 제공하니, 꽤 좋은 퀄리티의 프로젝트인 것 같다. unity package와 python package 두개로 제공되며, 둘 다 쉽게 설치가 가능하다. 파이썬은 pypi로, 유니티 패키지는 유니티 패키지 매니저에서 git url로 설치할 수 있다. ([참고 링크](https://github.com/jeongukjae/ml-agents-3d-balance-ball/commit/6e19706e98216227b24c238de6652d43a24fd073))

## 만들어보기

[GitHub jeongukjae/ml-agents-3d-balance-ball](https://github.com/jeongukjae/ml-agents-3d-balance-ball)에 구성했다. Unity-Technologies/ml-agents 레포지토리의 [Project/Assets/ML-Agents/Examples/3DBall](https://github.com/Unity-Technologies/ml-agents/tree/c1b26d49e4f4fc692c2688531f9e7c69dba12682/Project/Assets/ML-Agents/Examples/3DBall) 폴더에 존재하는 3DBall 에셋을 사용해서 프로젝트를 구성했다.

작성할 때 주의할 점은 `.gitignore`에 `/Assets/ML-Agents/Timers*` 추가해주기. ([관련 링크](https://github.com/jeongukjae/ml-agents-3d-balance-ball/blob/6ba54bb7bd951d43365aac15cb3490002ce4371f/3DBalanceBall/.gitignore#L74))

그 후에 pip으로 설치한 mlagents cli를 사용해서 학습하면 된다. config는 examples와 동일하게 구성했고, 생각보다 굉장히 빠르게 구성할 수 있었다. gym으로 직접 구성하는 것도 이제 시도해봐야겠다.

balance ball 자체가 쉬운 태스크라 그런지 금방금방 학습을 하고 `MacBook Pro (13-inch, 2020, Four Thunderbolt 3 ports)` (`2 GHz 쿼드 코어 Intel Core i5`) 기종인데 CPU로 충분히 학습시킬만한 정도이다. 크게 복잡한 게임이 아니라면 이런 도구를 활용해서 agent를 만들어보면 좋을 것 같다.
