---
layout: post
title: 📕 CS224n Lecture 18 Constituency Parsing and Tree Recursive Neural Networks
tags:
  - nlp
  - cs224n
  - machine learning
---

18강이고 강의 전체가 다 끝나기까지 이 강의를 제외하고 2강정도만 남았다.

#### Last Minute Project Tips

이건 파이널 프로젝트 팁인데, 느리고 아무것도 동작안하면 처음으로 그냥 맘편히 돌아가서 다시 해보는 것이 좋다고. 패닉인 상황일테니까. 디버깅을 위해 매우 작은 네트워크랑 데이터를 넣어보기도 하고, 잘 동작하면 모델 사이즈를 키워보기도 하라고 한다.

## Motivation: Compositionality and Recursion

* semantic 정보를 우리가 잘 가져갈 수 있을까?
* word embedding만으로 충분할까?
* 만약 잘 가져갈 수 있다고 해도, 정말 큰 phrase에 대해서는?

위의 문제 때문에 compositionality를 생각하게 되었고, 단어, 구들의 semantic composition을 구성하자는 아이디어가 나왔다.

{% include image.html url="/images/cs224n/18-1.png" description="약간 요런 composition??" %}

그럼 tree 형태로 구성하기 위해서 recursive한지 물어본다면 논쟁이 있을 수 있겠지만, language 자체를 표현하는데 엄청 자연스럽다고.

{% include image.html url="/images/cs224n/18-2.png" description="암튼 자연스러움" %}

## Structure prediction with simple Tree RNN: Parsing

vector space에 word vector를 뿌려놓는데, 그럼 구들은 어떻게 해야하나?? -> 그냥 바로 같은 vector space에 넣어버리자. 그럼 어떻게 phrase의 embedding을 결정할까??

1. 단어의 의미들과
2. 그들을 combine하는 규칙을 만들어서!

{% include image.html url="/images/cs224n/18-3.png" description="이렇게 이렇게 잘 뽀까뽀까" %}

위의 경우는 recursive한 경우이고, 일반적인 rnn을 통해서도 결과는 다르겠지만 구해볼 수 있다. 하지만 recursive한 구조는 tree structure를 구성해주어야 한다는 어려움이 따르고, rnn을 통한 구조는 phrase를 prefix context없이 잡아내지도 못하고, 마지막 결과 vector가 마지막 단어에 좌우된다는 단점이 있다.

그럼 NN에 어떻게 structure prediction을 할 수 있을까? 이렇게 children을 넣고 semantic representation을 뽑아내고, 얼마나 plausible한지(얼마나 Network가 이 노드를 확신하는지 정도..?)도 뽑아낸다. 그런 NN을 모든 children 대상으로 쭉 돌린다음에 그 위의 층에서도 또 돌리고, 또 돌리고 한다고 하는데, 내가 다시 이 글을 봐도 이해 못할 듯 하니 아래 사진을 보자.

{% include image.html url="/images/cs224n/18-4.png" description="이렇게 이렇게 잘" %}

{% include image.html url="/images/cs224n/18-5.png" description="이걸 잘 children을 넣어서" %}

{% include image.html url="/images/cs224n/18-6.png" description="잘 요렇게 요렇게" %}

{% include image.html url="/images/cs224n/18-7.png" description="뿅!" %}

## Backpropagation through Structure

general backprop과 크게 다를 것은 없다. 원칙적으로는 같다. [Goller & Küchler (1996)](https://www.semanticscholar.org/paper/Learning-task-dependent-distributed-representations-Goller-Kuchler/794e6ed81d21f1bf32a0fd3be05c44c1fa362688)에 의해 소개되었다.

forward prop일 때, children $$c_1$$, $$c_2$$가 있다고 하자. 거기서 parent $$p$$를 뽑아내기 위해 $$p = \tanh (W \pmatrix {c_1 \\ c_2} + b)$$와 같은 연산을 한다. 그럼 backward prop은 반대로 각각의 노드별로 연산을 해준다. 이런 Simple TreeRNN에 대해서 아래와 같은 점을 생각해볼 수 있다.

* 생각보다 결과는 나쁘지 않고
* 좀 phrase를 잡아낼 수는 있는데, more higher order composition, more complex한 long sentence를 파싱하는데 어려움이 있다.
* input word들 사이의 interaction은 하나도 없다.
* composition function이 다 똑같다

## More complex TreeRNN units

두번째로 Syntactically-United RNN이 있는데, [Socher, Bauer, Manning, Ng 2013](https://www.aclweb.org/anthology/P13-1045)을 살펴보자.

기본적인 syntactic structure를 위해서는 symbolic Context-Free Grammar (CFG) backbone이 좋았다고 한다. 그리고 discrete syntactic category를 사용했다고 하고, 다른 syntactic environment에서는 다른 composition matrix를 사용하게 해주는 것이 훨씬 좋은 결과를 내었다고 한다. 그리고 더 좋은 semantic의 결과를 볼 수 있었다고.

아직 위의 논문을 읽어보지 않아서 자세한 내용을 모르지만, 강의의 내용대로 써보자면, Compositional Vector Grammar를 이용하는 것의 단점이 일단 문제점이 속도가 느리다고 한다. Beam Search 과정에서 matrix-vector product를 하니 연산량이 많아질 수 밖에 없다고. 그래서 subset of tree를 먼저 계산해보고 very unlikely candidates를 미리 없애는 방법(PCFG)을 사용했다고 한다. 그래서 CVG = PCFG + TreeRNN

{% include image.html url="/images/cs224n/18-8.png" description="나중을 위해 저장! (CVG = Compositional Vector Grammer인듯..?)" %}

45:11 까지 들음

## Other uses of tree-recursive neural nets

## Institute for Human-Centered Artificial Intelligence
