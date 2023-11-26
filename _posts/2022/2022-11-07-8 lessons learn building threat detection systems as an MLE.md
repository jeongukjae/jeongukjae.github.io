---
layout: post
title: "8 Lessons Learn Building Threat Detection Systems as an MLE"
tags:
  - Operation
  - ML
---

너무 좋은 자료가 있어 메모.

Google docs link: <https://docs.google.com/presentation/d/1UMF4mysIeEShsj3o0CYUbxbnhZKoiPFeoTjGYbOee_I/edit#slide=id.g16286b535dd_0_0>

Tweet:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">i&#39;ll be giving a talk at <a href="https://twitter.com/eugeneyan?ref_src=twsrc%5Etfw">@eugeneyan</a> and <a href="https://twitter.com/chipro?ref_src=twsrc%5Etfw">@chipro</a>&#39;s meetup group this thursday. come out and listen to hear about my experience building threat detection systems as an MLE! <a href="https://t.co/N1Bc5y2V5k">https://t.co/N1Bc5y2V5k</a></p>&mdash; Jeremy Jordan (@jeremyjordan) <a href="https://twitter.com/jeremyjordan/status/1574567844041445378?ref_src=twsrc%5Etfw">September 27, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

---

# Building a threat detection system 목적

* 정상 컨텐츠를 간섭하지 않기
* 위협적인 컨텐츠를 분류하고 차단하기
* \+ 유저에게 부담을 주지 않으면서

## Lesson 0: Understand the threats you're trying to detect

* 내부적으로 프로덕트에 대한 위협을 잘 논의하고 용어/분류에 대해 잘 정의하기
* community-led 기준도 잘 활용하기

## Lesson 1: Start with rules

* 도메인 지식을 기반으로 높은 정밀도(precision)으로 탐지할 수 있는 탐지 룰들을 작성
* 이 휴리스틱 룰들을 이벤트들에 대해 처리할 수 있는 데이터 인프라를 구성

## Lesson 2: Annotate your data

* 정의된 위협 분류에 따라 데이터 레이블링 하기
* 이 레이블들은 룰 등을 평가하기에 굉장히 중요함
* 필요한 정보를 충분히 수집하도록 시스템이 준비되어야 함
    * ex) 로그인 시도가 정상인지 판단하려면 어느정도의 세션 정보가 필요할까?
    * ex) URL이 피싱인지 알아내려면 어느정도의 정보가 필요할까?

## Lesson 3: Scale your detections with ML

* ML Model은 특정 정밀도에 고정 후 재현율을 높이기 좋다. (recall@precision)
* ML은 휴리스틱 룰을 보완하는 존재. 각자의 장점이 있다.
* ML 모델은 바로 위협을 차단할 필요 없다. threat hunting 만으로도 의미있다.

## Lesson 4: Pay attention when detection systems disagree

* 룰/ML 시스템 모두 위협을 탐지할 때 두 시스템 사이의 판단이 다른 경우 데이터 레이블링을 위한 좋은 perspective가 될 수 있다.

## Lesson 5. Build cascading detection systems

* cheap/fast detection을 앞에, 모호할 경우 more expensive model을 통해 판단
* 효과와 비용 사이에 밸런스가 필요하다

## Lesson 6. Focus on the threats (.. not the anomalies)

* 사람들은 인터넷에서 이상한 행동을 많이 하지만, 그 행동들이 괜찮을 때가 많다
* 우리는 weird content가 아닌 threats를 탐지하는 것이고, 그 관점에서 컨텐츠를 평가해야 한다.

## Lesson 7. Mitigate detection errors with design

* 우리는 컨텐츠를 차단할 때는 매우 높은 정밀도가 필요하다
* binary outcome(allow/block)이 아닌 gradient of possible outcome로 대응하자
* 이 것은 그레이 영역에 있는 컨텐츠를 어떻게 대할지에 대한 설계 문제이다.

## Lesson 8. Understand you're playing an infinite game

* threat detection은 자연적으로 adversarial한 환경이다.
* threat actor는 계속해서 취약점을 찾을 것이고, 우리는 계속해서 민첩하게 새로운 위협에 대해 대응해야한다.
