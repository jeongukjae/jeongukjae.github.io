---
layout: post
title: 📕 CS224n Lecture 4 Backpropagation
tags:
  - cs224n
---

CS224n 네번째 강의를 듣고 정리한 포스트!! 이번 강의는 다른 강의를 들으면서 많이 보았던 내용이고 많이 다를 것이 없다 생각하고 별 기대없이 들었다.

## Matrix gradients for our simple neural net and some tips

편미분 하는 식은 건너뛴다! 너무 여기저기 많이 나오기도 했고 개인적으로도 정리할 필요성을 못 느낀다.

다만, 이런저런 팁이 나왔는데 아래와 같다.

* Tip 1: Carefully define your variables and keep track of their dimensionality!
* Tip 2: Chain rule!
* Tip 3: For the top softmax part of a model: First consider the derivative wrt $$f_c$$ when $$c = y$$ (the correct class), then consider derivative wrt $$f_c$$ when $$c \neq y$$ (all the incorrect classes)
* Tip 4: Work out element-wise partial derivatives if you’re getting confused by matrix calculus!
* Tip 5: Use Shape Convention. Note: The error message $$\delta$$ that arrives at a hidden layer has the same dimensionality as that hidden layer

여튼 쭉 건너뛰어서 word gradients를 window model에서 계산하는 부분까지 왔다. window를 사용하는 모델의 경우 $$x$$의 gradient를 계산한 결과가 window 전체인데, 이는 word vector들을 단순히 연결한 것이므로 다시 나눠서 생각해준다.

$$ x_{window} = \pmatrix { x_{museums} && x_{in} && x_{Paris} && x_{is} && x_{amazing} }$$

### Updating word gradients in window model

gradient를 가져외서 word vector를 업데이트할 때 주의해야하는 점이 있다. 잘 생각해보면 원래의 ML 접근법은 n차원에 데이터들이 공간에 존재할 때 decision boundary를 정하는 것이다. 하지만, word vector를 학습하는 것은 word vector 자체가 움직인다. 특정 batch에 대해 학습한다고 할 때, batch에 존재하지 않은 단어들은 움직이지 않지만, batch에 들어있는 단어들은 움직이게 된다.

그에 대한 비교적 좋은 해결책은 pre-trained word vector들을 사용하는 것이다. 대부분, 거의 모든 경우에 좋은 답이 될 수 있다고 한다. 만약 좋은 방대한 데이터셋을 가지고 있는 경우 pre trained 모델에 대해서 fine tuning을 해줘도 좋다고 한다. (다만, 작은 데이터셋인 경우 학습하는 것이 오히려 해가 될수도 있다고)

## Computation graphs and backpropagation

이제 graph로 설명하는 backprop 부분인데, 건너뛴다.

## Stuff you should know

다양한, 좀 알아두면 좋을 것들에 대해서 설명하는데 아래와 같은 리스트를 알려준다.

* Regularization: overfitting을 방지하는 기법
* Vecotrization: pythonic한 방법은 ML에서는 좀 많이.. 느릴 수 있다.
* non-linearity: activation function에 대해 설명을 했는데, sigmoid, tanh는 이제 특별한 상황에서만 사용한다고 한다. ReLU를 그냥 처음 시도해보는 것이 좋을 거라고..
* parameter initialization: weight를 처음 어떻게 초기화할지가 문제인데, 0은 쓰지말고(backprop 해야하니까) Xavier같은 것을 써주면 잘 된다고 한다.
* optimization: SGD, adargrad, RMSProp, Adam, SparseAdam같은 것들이 많이 나왔는데, SGD가 보통의 상황에 잘 동작한대요.
* Learning Rate: 적절한 lr를 정해주는 것이 좋은데, cyclic learning rates같은 신기한 방법도 있으니 잘 정합시다.
