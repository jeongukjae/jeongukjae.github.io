---
layout: post
title: "Efficient BackProp 정리"
tags:
  - paper
---

정석으로 배우는 딥러닝 책을 다 읽었는데, 더 자세히 보고 싶어서 참고 문헌에 있던 논문들을 하나씩 찾아보기 시작했습니다.

이 논문은 Efficient BackProp[^Paper]이라는 제목의 논문으로, Yann LeCun, Leon Bottou 등의 저자들에 의해 작성됨.

대충대충 다시 볼 내용들만 정리합니다. 일단 궁금했던 부분까지만 읽어요.

## 수정

18.09.20 수정 4.3 ~

## 1

우선 BackProp(BackPropagation을 줄여씀)은 쉽고, 연산의 효율성이 좋고, 잘 동작하는 경우가 많아서 매우 흔한 Neural Network 학습 알고리즘이다.

## 2

머신 러닝 접근법이 여러가지가 있는데 gradient-base인 학습법이 많이들 성공적이라고 한다.

쉽게 보면 $$M(Z^p, W)$$인 함수를 연산하는게 Learning Machine인데, $$Z^p$$가 p번째 입력값이고, $$W$$가 가중치이다. 그 결과값이 prediction. 주어진 데이터셋은 $$\{(Z^1, D^1), (Z^2, D^2), (Z^3, D^3) ... \}$$으로 본다. 그 결과로 Cost를 $$E^p = C(D^p, M(Z^p, W))$$로 쓸 수 있다. 학습은 $$E_{train}(W)$$를 minimize 시키는 과정. 자주 쓰이는 예시 중 하나인 Mean Squared Error는 $$E^p = \frac 1 2 (D^p - M(Z^p, W))^2$$, $$E_{train} = \frac 1 P \sum_{p=1} E^p$$이다.

generalize 하는 능력이 중요. 새로운 것에 대해 에러 없이 잘 처리하는 능력 말한다. Generalization Technique은 네트워크 상의 에러를 잘 정정하려고 하는 것이다. 여기서 나오는 많은 것들은 cost function에 대한 minimization strategy들과 그것들을 빠르고, 정확히 하기 위한 트릭들이라고 한다.

## 3

classical한 Multi-layer feed-forward NN이라고 하더라도 Gradient-base 학습을 적용하는 것이 많다고 한다. 가장 simple한 learning procedure는 (minimization) gradient descent algorithm인데, $$W(t) = W(t-1) - \eta \frac {\partial E} {\partial W}$$이다. Loss를 해당 변수로 미분한 값이 Gradient이다. $$\eta$$는 간단한 경우 스칼라 값이다. 그 외에 diagonal matrix, estimate of the inverse Hessian matrix of the cost function 일수도 있다. cost가 인자를 두개 받으니 second order. step size (learning rate)인 $$\eta$$를 잘 선택하는 법은 나중에 거론한다고 한다.

## 4

BackProp은 cost surface가 non-quadratic, non-convex, high-dimensional with many local minima and/or flat regions인 multilayer 네트워크일 때 매우 느릴 수 있다고 한다. 어떤 식도 네트워크의 convergence를 보장할 수 없다.(전혀 발생할 수 없진 않고, 항상 좋은 정답으로 갈수도 없고, 빠른지도 모르고)

### 4.1

Stochastic 과 Batch를 비교하는데, Batch는 전체 데이터셋을 순회하는 것, Stochastic은 Error의 기댓값을 구하는 것. Stochastic 장점은 3가지.

 - 보통 Stochastic이 batch보다 훨씬 빠르다.
 - 보통 더 좋은 답을 낸다. => batch면 갈 확률이 높은 local minima를 벗어날 수 있단다.
 - 변경사항 tracking하는데 쓸 수 있다.

물론 Batch도 좋다고 한다.

 - convergence 조건이 이해하기 좋다.
 - Batch에만 동작하는 Acceleration Technique들이 많다.
 - 이론적인 분석이 훨씬 간단하다.

이 이점들은 모두 Stochastic이 noise 특성이 있기 때문이라고...

우리는 fluctuation을 줄이기 위해(noise를 없애기 위해) learning rate를 annealing하거나, adaptive batch size를 적용할 수 있다. adaptive batch size는 mini-batches를 활용하는 것인데, 처음에는 작은 batch를 이용하다가 점점 큰 batch를 이용하는 것이다.

### 4.2

네트워크는 가장 익숙하지 않은 sample로부터 빠르게 배운다. 따라서 시스템에게 제일 익숙하지 않은 것들을 매 iteration마다 가져다 주는 것이 좋다. Stochastic만 해당. 방법은 아래와 같다.

1. Training set을 섞고, 이어진 example들이 거의 같은 class에 속하지 않도록 해라.
2. large error를 만들어내는 example들을 자주 넣어라.

### 4.3 Normalizing the Inputs

보통 Convergence는 각각의 input variable들의 평균이 0에 가까울 때 빠르다. 극단적인 경우에 입력값이 전부 양수면 학습을 느리게 할 수 있으니, 데이터 분포를 생각해 데이터의 평균이 0이 되도록 만들어 준다. Convergence는 근데 평균이 0으로 될때만 빠른게 아니라 같은 공분산(Covariance[^Covariance])을 가지도록 해줘도 빨라진다.

그 우리가 보통 생각하는 Covariance Matrix가 아니고 그냥 아래처럼 간단하게 썼다.

$$ C_i = \frac 1 P \sum ^P_{p=1} (z^p_i)^2 $$

$$C_i$$는 covariance of $$i^{th}$$ input variable이고, $$z^p_i$$는 p번째 training example의 i번째 컴포넌트이다.

1. 평균이 0이 되도록 옮겨준다.
2. covariance가 같아지도록 입력을 rescale해준다.
3. 입력 변수들은 가능하면 uncorrelated 되어야 한다.

이를 위해 KL Expansion[^KL]으로 알려진 PCA를 할수도 있다고 한다. (to remove *linear* correlations in inputs)

## 4.4 The Sigmoid

가장 유명한 Activation function 중 하나. 단조 증가 함수(monotonically increasing function)이다. 그리고 특정한 유한한 값으로 수렴한다. $$f(x) = \frac 1 {1 + e^{-x}} $$ 또는 $$f(x) = tanh(x)$$가 많이 쓰이는데, Sigmoid도 4.3과 같은 이유때문에 output을 0에 가깝게 내어서 원점 대칭이 선호된다. (그 값은 다음 layer의 input이다)

1. 따라서 hyperbolic tangent 함수가 보통 convergence가 빠르다.
2. 추천되는 sigmoid는 $$f(x) = 1.7159 tanh(\frac 2 3 x)$$이다. tanh 함수는 때때로 계산하기 힘들어서 ratio of polynomials로 근사한 함수가 쓰일 때도 있다.
3. 작은 linear term을 추가하는 것이 도움이 되기도 한다. flat spots들을 피할 수 있기 때문. $$+ ax$$ 처럼

하지만 잠재적인 위험이 있을 수 있는데, 그건 symmetric sigmoid를 쓰면 origin 근처에서 *very flat* 할 수 있다는 것이다. 따라서 very small weights로 초기화를 해준다. origin에서 먼 error surface는 매우 flat하기 떄문이다. 3번을 사용하는 것도 도움이 된다.

## 4.5

나중에 더 읽기로

---

[^Paper]: http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf 이 링크말고도 여러가지가 있는 듯 한데, 그냥 구글링해서 찾았다.
[^Covariance]: https://en.wikipedia.org/wiki/Covariance 공분산에 대해서는 이 링크 참고
[^KL]: https://en.wikipedia.org/wiki/Karhunen–Loève_theorem 나중에 읽어봐야지...
