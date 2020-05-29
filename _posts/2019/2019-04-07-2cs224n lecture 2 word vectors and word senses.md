---
layout: post
title: 📕 CS224n Lecture 2 Word Vectors and Word Senses
tags:
  - cs224n
---

CS224n 두번째 강의를 듣고 정리한 포스트!!

## Finish Looking at Word Vectors and Word2Vec

일단 강의를 시작하면서 지난번 강의때부터 이어서 word2vec와 word vector에 관한 내용을 마무리한다. review를 해보면 word2vec의 main idea는 주변의 단어(context)를 word vector를 통해 예측하거나 그 반대의 것을 예측하는 것이었다. (CBOW, Skip-gram) 한 단어당 두개의 벡터를 사용했고, $$u$$ (context), $$\vec sv$$ (center) 두개의 벡터를 dot product를 한 다음에 softmax를 취해 값들을 계산했다. 그리고 그 학습 과정을 통해 결과로 비슷한 단어를 비슷한 공간에 놓아놓았다. 이 과정이 cost function을 maximize하는 과정이었다.

## Optimization

이제 Optimization에 대해 공부를 하는데, 자세한 부분을 가르치진 않으니 알아두라고 말한다. 자세한 optimization 과정은 CS229 (아마 머신 러닝 자체에 대한 강좌였던 걸로 기억한다)를 들어보면 배울 수 있다고.

어쨌든 gradient descent를 사용해서 $$J(\theta)$$를 minimize 하는데, 그 과정에서 backprop을 사용한다. 업데이트 하는 방법은

$$\theta_{new} = \theta_{old} - \alpha \nabla_{\theta} J(\theta) $$

의 식을 활용한다. 여기서 alpha는 step size로 그 learning rate를 가리키는 것 같다. 하지만 여기서 문제점은 모든 corpus에 대해 이 연산을 수행하기에는 너무 연산량이 많다. 그래서 SGD를 사용하는데, Stochastic Gradient Descent이다. sampling을 해서 Grdient Descent를 적용하는 방법으로 이러한 이점이 있다고 한다.

1. noise가 적다
2. 병렬화가 가능하다 -> 빠른 학습이 가능하다

하지만 SGD를 적용하면 word vector들이 매우 sparse해진다. (sampling을 했으니..?) 그럼 여기서 굳이 다 업데이트를 할 필요가 있나?라는 생각이 든다. 그래서 UV decomposition을 사용하라고 한다. 이건 제대로 이해를 못한 부분인 것 같다.

여튼 이제 word2vec를 구현할 때 왜 벡터를 두개나 쓰는지에 대해 설명을 해주는데, 그 이유는 그저 optimization이 쉬워지기 때문이라고 한다. 아마 이건 이론적인 이유보다 실험적인 이유가 아닐까 싶다. 학습이 끝나고 나서 평균을 취해준다고 한다.

그리고 다른 optim 방법은 training method 부분에서 negative sampling을 하는 방법도 있고 (논문을 읽어보았는데 더 자세히 봐야할 것 같다) naive softmax를 취하는 방법도 있다.

여기서 negative sampling에 대한 main idea는 true pair와 noise pair에 대해 binary logistic regression을 훈련한다는 것이다. NCE도 나오고 뭐 많이 나오던데, 따로 정리하자 ㅠㅠ

## Capture co-occurance counts directly?

### count base

단어의 숫자를 기준으로 co-occurance를 판단하는데, 두가지 방식이 있다.

window size를 사용하는 경우: syntactix한 정보와 semantic한 정보를 받을 수 있고, high dimensionality한 이슈와 sparsity한 이슈가 있다. 그리고 robust하지 않다. 그래서 UV decomposition같은 것을 통해 low dimensionality vector로 바꾸어준다.

full document -> general topic에 관해 잡아내기 좋다. (Latent Semantic Analysis를 보자) 대충 이런 쪽으로는 LSA, HAL, COALS, Hellinger-PCA 등등이 있다.

어쨌든 count base는 빠르고, 효율적인 통계학 기반의 접근법이고, 다만 기능이 제한적이며 많은 갯수의 단어(the같은?)에 대해 취약하다.

### direct prediction

어쩄든 그래서 직접 prediction하는 것으로 넘어가자. 이건 skip-gram, cbow를 생각하면 된다. 성능이 매우 좋고 복잡한 패턴에 대해 매우 잘 알아차린다. 다만 corpus 사이즈가 매우 중요하고 효율적이지 않은 통계를 사용한다.

## Encodig Meaning in vector differences

co-occurance를 분석해서 meaning component를 알아낸다. 근데 이건 그냥 EMNLP 2014, Penningtokn et al. 을 살펴보자.

## Evaluating

Intrinsic한 방법과 Extrinsic한 방법이 있는데, Intrinsic한 방법은 빠르고 clear하지 않다. 자세한 방법으로는 cos-distance를 활용해 analofy 테스트를 하거나 wordsim등을 활용한다. Extrinsic한 방법은 긴 시간이 걸리지만 정확하다.

---

추가로 한 단어가 여러가지 의미를 가지는 경우에 대해 분석한 논문이 있는데 이건 Huang et al. 2012을 살펴보자.
