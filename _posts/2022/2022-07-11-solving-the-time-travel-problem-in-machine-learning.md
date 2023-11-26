---
layout: post
title: "머신러닝에서의 time travel 문제"
tags:
  - Operation
  - ML
---

[원 블로그 글](https://www.tecton.ai/blog/time-travel-in-ml/) 보면서 정리

* 어플리케이션에서 머신러닝 모델(추천, 광고 타게팅, ...)은 굉장히 효과적이고 다양하게 사용 가능
* 미래를 예측하는 모델은 과거 데이터를 통해 학습됨
  * 예: 미래의 광고 타게팅을 위해서는 과거의 클릭 데이터를 참고
* 그 시간에 접근할 수 있었던 데이터만을 활용하여 data leakage 문제를 잘 방지하는 것이 중요함
* The data leakage conundrum
  * 여러가지 문제로 실시간 추론에서 사용하는 쿼리와는 다른 쿼리로 학습 데이터를 구성해야 함
  * 오프라인 검증 셋에서는 잘 동작하는 것처럼 보일테지만, 실시간 추론에서는 성능이 굉장히 떨어지게 됨
  * 학습에서 그 시간에 얻을 수 없는 데이터로 학습되었기 때문
  * 알아채기도 힘들고 디버그도 힘든 문제임
  * 마치 이게 시간 여행을 하는 것 같아서 원 블로그 글에서 time travel 문제라고 말하는 듯
* log and wait approach
  * 이를 방지하기 위한 방법 중 하나. 실시간 추론 시에 feature 값들을 로그를 찍는 방법.
  * 특정 피쳐를 추가하고 싶을 때는 우선 실시간 추론 때에 로그 찍고 모델에는 전달하지 않기.
  * 그리고 나중에 이 로그 데이터를 레이블링하기
  * data leakage를 잘 방지할 수 있고, 많은 조직에서 사용하는 방법이지만, 단점 역시 존재
    * 새로운 피쳐 추가에 시간이 걸림. 로그를 찍기 시작한 상태에서 충분한 시간이 지나야 함.
    * 같은 피쳐를 필요로 하는 다른 머신러닝 시스템에서 활용하기 어려움.
* backfilling data and point in time joins
  * backfilling은 어렵고, backfill한 학습 셋과 실제 추론 당시의 피쳐 사이의 오류도 적어야 함
  * log and wait 방식과 결합하면 시간에 관한 정보를 더 얻을 수는 있지만, 그 역시도 정확한 시간 계산에 어려움이 있음
  * snapshot based time travel
    * 피쳐가 많이 안바뀌는 경우 이런 방식이 가능.
    * 6개월 이전까지의 피쳐를 사용하고, 6개월 이전부터 현재까지의 레이블 데이터를 사용해서 학습 셋 구축
  * continous time travel
    * 추천과 같은 경우 피쳐가 자주 바뀌어서 snapshot based가 불가능
    * 각 label 별로 feature value cutoff time을 다르게 설정 (snapshot based에서의 cutoff time: 6개월)
    * 각 레이블 별로 추론 당시의 피쳐들을 모두 최대한 정확하게 사용해서 학습 셋 구성
    * point-in-time join이 필요함.
    * -> 이후는 텍톤 광고
