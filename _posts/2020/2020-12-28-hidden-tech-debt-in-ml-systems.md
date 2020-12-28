---
title: "Hidden Technical Debt in Machine Learning Systems"
layout: post
tags:
  - paper
---

[Building Machine Learning Pipelines](https://www.amazon.com/Building-Machine-Learning-Pipelines-Automating/dp/1492053198/ref=sr_1_1)를 최근 읽고 있는데, 해당 책에서 말하는 논문이었고, 읽어보면 좋을 것 같아 읽어보았다.

핵심적으로 이 논문에서 말하고자 하는 바는 ***머신러닝 시스템의 기술 부채는 굉장히 관리하기 어렵고, 힘든데 그 이유는 기존의 코드 관리와 함께 데이터 관리가 같이 들어가기 때문***이라고 한다. 다방면에서 머신러닝 시스템의 기술 부채를 말해주는 논문이라 최신의 내용이 아닐지라도 좋은 논문이라 생각한다.

## _

머신러닝 시스템은 최근에 개발해서 사용하기에 환경이 상당히 좋아지고 있고, 편해지고 있다. 많은 라이브러리들과 프레임워크들이 나오고 있고, 서버, 웹, 임베디드 시스템 등등에 배포하기에도 예전보다 훨씬 수월해졌다. 하지만 이를 관리하기에는 아직 좋은 명확한 방법이 존재하지 않는다.

그 어려움이 기술부채로 나타나고 있다. 모든 부채가 나쁜 것은 아니라지만, 기술부채는 종종 리팩토링, 테스트 코드 보강, 사용하지 않는 코드 삭제, 의존성 정리, 문서 고도화 등등 많이 비용을 부과한다. 그래서 기술부채를 잘 관리해야 하지만, 기존의 소프트웨어 엔지니어링과는 다르게 머신러닝은 머신러닝만의 기술부채가 별도로 존재한다.

## Complex Models Erode Boundaries

기존의 소프트웨어 엔지니어링은 캡슐화와 Modular Design을 통해 잘 추상화를 할 수 있고, 유지보수하기에도 편하게 관리할 수 있다. **하지만, 그에 비해 머신러닝 엔지니어링은 외부 데이터 의존성에 대한 설명 없이는 좋은 추상화가 불가능에 가깝다.** 아래 정도가 그를 보여주는 예시가 될 수 있다.

### Entanglement

머신러닝 모델들은 보통 여러개의 피쳐를 입력으로 받는다. 해당 피쳐들의 분포에 매우 민감한데, 피쳐 하나의 분포가 바뀌게 된다면 다른 피쳐들이 바뀌지 않더라도 결과물이 많이 바뀔 수 밖에 없다. 그래서 하나의 피쳐만 바꾼다는 것은 모델 아키텍쳐가 특이하지 않는 한 있을 수 없으며, 이 현상을 이 논문에서 **CACE principle**이라고 말하는 것 같다. (Changing Anything Changes Everything)

이 경우에 두 가지의 해결법이 있을 것 같은데 첫번째는 모델을 분리해서 앙상블하는 기법이고, (아마 딥러닝 모델보다 조금 더 전통적인 머신러닝 모델을 말하는 것 같다) 두번째는 prediction behavior가 변했음을 탐지할 수 있도록 모니터링하는 것이다. 후자와 관련된 방법은 [Ad Click Prediction: a View from the Trenches](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41159.pdf)이라는 논문에 자세히 나와있는 것 같다.

### Correction Cascades

이 부분은 사실 개인적으로도 많이 공감할 수 있는 부분으로 생각한다.

문제 P1이 있고 이를 풀기위한 머신러닝 모델 A가 있다고 가정해보자. 그리고 P1과 유사한 P2가 존재하고 이를 풀기위한 머신러닝 모델 B가 있을 때 가장 빠르게 풀어내는 방법은 A위에 간단한 레이어를 추가해서 머신러닝 모델 B를 구성하는 방법이다.

하지만 이렇게 할 때 의존성을 강하게 거는 것으로 볼 수 있다. A를 변경하는 것으로 B의 동작이 변한다. A모델의 버전을 올리면서 얼마나 좋아졌는지 분석하기에도 정말 어렵게 만든다.

### Undeclared Consumers

머신러닝 모델이 개발되고 난 후에는 access control이 없다면 consumer를 알 수 없다. 다른 시스템에 의해서 조용하게 사용될 수도 있다. 이것을 원래는 visibility debt라고 부른다.

개인적으로는 이 부분이 정확히 무슨 말을 하는지 모르겠다. 아마도 "개발해놓고 모델 weight, graph만 떼가면 어디서든지 사용할 수 있다" 이런 말인가?

어쨌든 이것은 feedback을 명시적으로 받을 수 없게 만들고 머신러닝 모델을 유지보수하기 어렵게 만든다.

## Data Dependencies Cost More than Code Dependencies

"Code Dependencies는 적어도 정적 분석기와 compiler, linker로 알 수 있는데 Data dependencies는 그렇지 않다."에서 출발한다.

### Unstable Data Dependencies

머신러닝 모델은 데이터 의존성이 굉장히 큰데, 만약 그 데이터가 다른 모델로부터 온 데이터이거나, TF/IDF 스코어처럼 data-dependent lookup table일 경우 위험성이 크다. 해당 데이터가 조용히 변경될 경우 어떤 것이 문제인지, 왜 나타난 문제인지도 알기 힘들다.

이 경우 해결법은 versioned copy를 만들어두는 것이다. 근데 이것도 사실 versioning하는 자체의 비용이 있어서 계속해서 관리하기는 힘들다.

### Under-utilized Data Dependencies

논문에 굉장히 좋은 예시가 있는데, 조금 길어서 짧게 옮겨보자면 아래 정도이다.

> 레거시 상품 번호에서 새로운 상품 번호 시스템으로 옮겨간다고 가정하자. 이 때 둘 다 머신러닝 모델의 feature로 들어갈 때 머신러닝 모델은 일부 상품에서 레거시 상품 번호에 의존할 수 밖에 없다.
>
> 어느 날 레거시 상품 번호는 없어질 것이고 이것은 머신러닝 모델에게 그닥 좋은 현상은 아니다.

위처럼 좋지 않은 feature를 넣는 것은 정말 안좋은 에시이다. 보통 아래정도로 묶어볼 수 있는데, 각각 다 중요한 요소인 것 같다.

* **Legacy Features**
  * 특정 피쳐가 머신러닝 모델이 배포되고 난 후 다른 새로운 피쳐에 의해 대체될 수 있지만 그러지 않을 때
* **Bundled Features**
  * 데드라인 압박이 있을 때, 그냥 모든 피쳐를 넣어버리는 경우가 있다.
* **$$\epsilon$$-Features**
  * 머신러닝 리서처는 조금의 모델 성능을 약간 올리기 위해 모델 complexity가 너무 올라가더라도 피쳐들을 넣어버리는 경우가 있다.
* **Correlated Features**
  * 두 피쳐가 상관관계가 클 때 하나의 피쳐는 굳이 필요없을 때도 많다.

## Feedback Loops

live ML System들은 analysis debt가 발생할 경우가 많은데, 이는 자신의 prediction이 결국 자신의 training data로 들어오는 것과 같은 현상을 말한다.

### Direct Feedback Loops

모델이 직접적으로 자신의 training data를 구성해버리는 경우를 말한다. bandit algorithm과 같은 해결법을 사용할 수 있다.

### Hidden Feedback Loops

여러 모델이 서로 training data를 구성해주는 경우..인데 이 루프를 탐지하기 더 어려워보인다.

## ML-System Anti-Patterns

### Glue Code

***개인적으로 이 부분은 모든 커뮤니티가 노력을 기울어야 하는 부분으로 보인다.***

일반적으로 많이들 아는 그 Glue Code가 맞다. 다만 조금 더 설명해보자면 pandas, scikit learn, transformers 등등을 사용하면서 진짜 연결을 위해서 작성하는 코드들을 말한다. 머신러닝 업계의 많은 라이브러리가 black box 형태로 동작하고, 매우매우 크면서 한줄만 추가하면 다 된다.. 같이 설명을 많이 하기 때문에 재사용성이 많이 떨어지는 경우가 많다.

black-box packages를 일반적인 API로 감싸는 것이 해결책이 될 수 있다고 하는데, 개인적인 생각으로는 tensorflow처럼 대체 불가능한 라이브러리가 아니라면 사용을 하지 않는 것도 방법으로 보인다.

예를 들어 pandas, scikit learn의 많은 API는 기본적으로 일반적인 코드로 빠르게 작성이 가능한 경우가 많고, transformers도 패키지 사이즈가 굉장히 큰데, decoding과 같이 많은 코드가 필요한 경우를 제외하면 그냥 작성하는 것이 깔끔한 경우가 훨씬 많다.

### Pipeline Jungles

glue code의 pipeline 버전이다. glue code가 프로덕션으로 가는 길을 방해한다면, pipeline jungles는 실험으로 가는 길을 방해한다. 이를 해결하기 위해 research와 engineering 역할을 가진 사람들을 같은 팀에 넣어주는 것이 좋을 수도 있다.

### Dead Experimental Codepaths

실험 코드를 대충 붙여서 실험하는 것이 분기문을 잘 나누어서 실험 요소만 뜯어주는 것보다 단기적으로는 좋아보인다. 하지만 이런 실험코드가 계속해서 늘어날 경우 굉장히 큰 기술 부채가 되므로 분기문을 잘 나누어서 뜯어주는 것이 좋은데, 이조차도 시간이 지나며 큰 기술 부채가 된다. 그래서 이런 분기도 사용하지 않는 경우에는 주기적으로 삭제해주는 것이 중요하다.

### Abstraction Debt

사실 머신러닝 쪽의 추상화 요소들은 상당히 부족하다. iterative한 머신러닝 알고리즘 특성상 Map-Reduce가 그렇게까지 좋지는 않으며, parameter server abstraction도 있지만 그외에 좋은 경쟁자들이 있다. 하지만 이런 상황 자체가 좋은 하나의 개념으로 정리하기에는 아직 시간이 많이 걸린다는 것을 말하기도 한다.

## Configuration Debt

실험을 진행하기 위해서 Configuration으로 만드는 경우가 많은데, pre-, post-processing, 학습 세팅(optimizer, lr 등등)까지 보통 다 빠지게 된다. 이런 상황에서 극한까지 가면 코드 라인보다 설정파일의 라인수가 많아지기도 한다. (ㅋㅋㅋ) 그래서 실수하기도 좋은데, 테스트는 거의 불가능해진다. 수정하는데 시간도 많이 쓰게 되고, production으로 옮기기도 힘들어진다.

그래서 아래와 같은 사항을 지켜주면 좋다. (약간 의미가 안와닿는 것은 영어로 적었어요.)

* small change를 적용하기 좋은 시스템이어야 한다.
* It should be hard to make manual errors, omissions, or oversights.
* 두 모델 사이의 configuration diff를 보기 쉬워야 한다.
* 기본적인 세팅에 관한 assert를 잘 걸어주어야 한다. (feature 갯수같은 경우)
* unused, redundant한 세팅을 발견할 수 있어야 한다.
* configuration은 반드시 코드 리뷰를 받아야 하고 레포지토리에 들어가 있어야 한다.

## Dealing with Chagnes in the External World

### Fixed Thresholds in Dynamic Systems

threshold는 머신러닝 모델들에서 상당히 자주 사용하는데, 보통 고정값을 많이 쓴다. 근데 실 데이터는 계속 변하므로 메트릭을 고정해두고 해당 메트릭에 대해 최적인 theshold를 가변값으로 가져가는 것이 좋다.

### Monitoring and Testing

unit test만으로는 불충분하다. 그래서 의도대로 동작하는지 확인하기 위해 모니터링 시스템을 잘 만들어놓아야 한다. 아래정도를 시작으로 모니터링을 구성해보자.

* Prediction Bias: 자동 알림 주기에 좋다.
* Action Limits: 스팸 필터 만들었는데 갑자기 모두를 스팸 표시해버리면 안되니.. 어느정도 리밋을 걸자. 그리고 리밋에 도달하면 무조건 이상한 것이니까 그 때는 모델을 다시 확인하자.
* Up-Stream Producers: 다른 모델의 학습 데이터로 들어가는 경우가 많으니까 조심하자.

## Other Areas of ML-related Debt

* Data Testing Debt: 데이터 수집 후 distribution만 검증해줘도 좋다.
* Reproducibility Debt: 이건.. 무조건..
* Process Management Debt: 비즈니스 우선순위에 따라서 어떤 것을 잘 해낼지, 리소스를 할당할지 정해야한다.
* Cultural Debt: ML 리서처와 엔지니어는 넘기 힘든 선이 있다. 팀 컬쳐를 잘 구성해주자.

## __

굉장히 공감되는 논문이고.. 다들 한번씩 읽어보았으면 좋겠다.
