---
layout: post
title: "리그오브레전드의 챔피언 픽으로 승률 예측하기"
tags:
    - game
    - ML
---

리그오브레전드 게임에서 챔피언 픽은 중요한 요소지만, 어느 정도로 중요할까요?
티어가 높은 챔피언이 반드시 승리를 가져다 줄 수 있을까요?
실제 챔피언의 구도는 사람들이 생각하는 것과 같을까요?
이런 궁금증을 해결하기 위해 챔피언 픽을 통해 승률을 예측하는 모델을 만들어보았습니다.

> 이 블로그 글은 개인적인 목적이 있어 디테일한 기술적인 내용은 생략하고, 전체적인 흐름만을 소개합니다.

## 목적

승률을 단순히 챔피언 픽을 통해서만 예측하면 크게 의미가 없고, 정확도는 그렇게 높지 않을거라 생각합니다.
그래서 게임 시간을 버켓을 나누어 시간별 승률도 예측해서 챔피언 픽에 따라 어떻게 시간별로 승률을 예측할 수 있는지도 알아보았습니다.
**즉, 챔피언 픽과 기타 정보를 통해 승률과 시간별 승률을 예측하는 모델을 만들어보았습니다.**

## 데이터 수집

먼저, 모델을 학습시키기 위해서는 최소한의 데이터가 필요합니다.
Riot Games API를 확인해보니 필요한 정보들을 다 얻을 수 있었고, 이를 통해 챔피언 픽, 승패 등의 정보를 얻을 수 있었습니다.
하지만 한가지 문제가 있었는데요..

{% include image.html url="/images/2023/lol/devkey.png" description="Development API key는 Rate Limit 꽤 심하게 걸려있다" %}

이번 모델 학습으로 데모 하나 만들어서 제출해야 프로덕션 키를 받을 수 있어, 그 이후에 더 정확한 테스트를 진행해볼 수 있을 것 같네요 ㅠㅠ

우선은 시간이 걸리더라도 데이터를 모아봤습니다.
최상위권 (챌린저, 그랜드마스터) 소환사 정보를 1,000명 가량 수집하고, 각 소환사의 최근 게임 100건 이내의 목록만을 저장했습니다.
그 후 각 게임의 세부 정보를 받아오는 API를 통해 게임의 승패, 챔피언 픽 등의 정보를 얻었습니다.
이것만 해도 수 시간 걸렸던 것으로 기억합니다.

## 데이터 전처리

데이터 전처리는 비교적 간단했는데요, 각 게임의 챔피언과 승리팀, 항복여부, 게임 시간을 피쳐로 준비하고 정답을 승리팀으로 설정했습니다.
이렇게 준비한 데이터를 훈련 데이터와 테스트 데이터로 나누어 학습을 진행했습니다.
전부 모으고 나면 중복 제거, 비정상 데이터 제거 후 대략 17,000건의 데이터가 준비되었습니다.

## 모델 학습

모델은 정말 단순하게 600K 내외의 파라미터를 가지도록 모델링을 진행했습니다.
챔피언 별로 주요했던, 주요하지 않았던 챔피언을 구분할 수 있도록 attention을 활용했습니다.

{% include image.html url="/images/2023/lol/attention.png" description="Attention is all you need 논문 상의 figure. 학습 가능한 weighted sum 으로 볼 수 있습니다" %}

그 결과 테스트 셋에서 단순 승리확률 예측은 65% 이상의 정확도를 보였고, 시간별 승률 예측은 90% 이상의 정확도를 보였습니다.

## 시각화 및 예시

제가 상위 티어 게임은 잘 모르는데요,
블루 픽을 후반에 강한 조합으로 맞추고 레드 픽을 돌진 및 난전에 좋은 조합으로 맞춰 예시를 뽑아보았습니다.
시각화를 해보면 아래 스크린샷처럼 나타납니다. (Riot API 프로덕션 키를 받기 위해 제출한 웹사이트의 일부입니다)

{% include image.html url="/images/2023/lol/results.png" description="챔피언 픽을 통한 승률 예측" %}

첫 파이 차트는 게임 승률 예측이고, 그 아래의 라인 차트는 시간별 승률 예측입니다.
X축이 시간이고, Y축이 승률입니다.
그 아래의 라인 차트는 포지션별 승률에 대한 기여도를 나타냅니다.
X축이 포지션, Y축이 기여도입니다.
이 기여도는 Attention의 weight를 통해 계산합니다.

블루 픽이 초반에는 승률이 낮지만, 40분을 기점으로 승률이 높아지게 예측하네요.

신기하게도 제가 좋다고 생각하는 탑 아트록스보다는 정글 세주아니를 픽한 것이 승리 확률을 많이 높여주는 것으로 나옵니다.
만약 다른 정글로 바꾸게 되면 승률이 떨어짐과 동시에 블루팀 정글의 가중치가 떨어집니다.
아무래도 흔히 해설에서도 말하는 정글 세주아니와 근접 탑/미드 챔피언의 시너지가 좋다는 것이 여기서 드러나는 걸까 싶습니다.
궁금해서 미드를 근접 챔피언인 사일러스로 바꿔보면 승률과 관계없이 세주아니의 가중치는 더 올라갑니다.

## 결론

챔피언 픽만으로 게임의 승패를 이미 6할 이상 알 수 있는 것은 꽤 주목할만한 결과라고 생각합니다.
특히 게임 시간과 같이 고려하면 9할 이상의 정확도를 보이는 것도 놀랍습니다.
충분하지 못한 데이터를 쓰는 상황에서 이 정도의 정확도인데요, 더 큰 모델과 많은 데이터를 쓸 수 있게 된다면 더 좋은 결과를 얻을 것으로 보입니다.

특히 각종 피쳐들도 같이 넣어보면 더 좋은 결과를 이룰 수 있어보이는데요, 단순히 챔피언 승률과 픽률을 비교하는 것보다는 더 디테일한 통찰을 얻을 수 있어보입니다.

-

이 글을 쓰는 시점은 이미 프로덕션 키를 받은 상태인데요, 몇가지 정도만 개선을 해보니 85% 정도의 정확도를 얻었습니다.
정성적으로 봤을 때 LCK 서머 경기 결과들을 대입해보아도 꽤 괜찮은 결과를 보이고 있습니다.
이를 시작으로 재밌는 분석을 해볼 수 있을 것 같은데요, 관련된 기회를 찾아보려 합니다.