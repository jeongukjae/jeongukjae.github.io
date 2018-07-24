---
layout: post
title: "Efficient BackProp 정리"
tags:
  - machine learning
  - paper
  - neural network
---

정석으로 배우는 딥러닝 책을 다 읽었는데, 더 자세히 보고 싶어서 참고 문헌에 있던 논문들을 하나씩 찾아보기 시작했습니다.

이 논문은 Efficient BackProp[^Paper]이라는 제목의 논문으로, Yann LeCun, Leon Bottou 등의 저자들에 의해 작성됨.

대충대충 다시 볼 내용들만 정리합니다. 일단 궁금했던 부분까지만 읽어요.

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

### 4.3

입력값이 전부 양수라 학습을 느리게 할 수 있으니, 데이터 분포를 생각해 데이터의 평균이 0이 되도록 만들어 준다.

1. 평균이 0이 되도록 옮겨준다.
2. covariance가 같아지도록 입력을 rescale해준다.
3. 입력 변수들은 가능하면 uncorrelated 되어야 한다.

---

[^Paper]: http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf 이 링크말고도 여러가지가 있는 듯 한데, 그냥 구글링해서 찾았다.

---

나중에 더 읽기로
