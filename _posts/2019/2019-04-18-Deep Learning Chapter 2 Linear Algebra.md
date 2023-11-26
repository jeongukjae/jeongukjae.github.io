---
layout: post
title: "Deep Learning Chapter 2 Linear Algebra"
tags:
  - note
---

Ian Goodfellow의 [Deep Learning](http://www.deeplearningbook.org) 책을 보기 시작했다. 해당 책에 대해 추천을 많이 받았고, 마침 출판사 이벤트로 참가해서 번역본도 운 좋게 집에 있었기 때문에 중요한 부분만 골라서 정리해본다!

책은 크게 3개의 Part로 나누어진다. Part 1은 4개의 장으로 되어 있고, Linear Algebra, Probability and Information Theory, Numerical Computation, Machine Learning Basics 순서로 되어 있다. 기본 수학 지식과 ML 개념들을 설명한다. 그래서 해당 장부터 정리해보기로 했다. 물론 아는 부분은 키워드만 적어두고 넘어간다.

일단 선형 대수에 익숙하면 안봐도 되는 챕터로 보이지만 수업에서 들었던 내용들을 간단하게 떠올릴 겸 읽어보기로 했다. 책을 읽는데 지장 없는 수준만 설명하기 때문에 더 공부하고 싶다면, *The Matrix Cookbook* (Petersen & Pedersen, 2006)이나, Shilov 1997을 읽어보라고 한다.

## Scalars, Vectors, Matrices, and Tensors

* Scalars
* Vectors
* Matrices
* Tensors : an array of numbers arranged on a regular grid with a variable number of axes

### broadcasting

머신러닝에서 덜 엄밀한 개념을 몇몇 사용하는데 그 중 하나가 broad casting이다. matrix와 vector를 더해서 다른 matrix가 나오는 연산이 broadcasting이고, 예를 들어 $$\textbf C = \textbf A  + \textbf b $$를 $$ C_{i,j} = A_{i,j} + b_j$$처럼 연산하는 경우를 말한다. 이 연산은 $$b$$를 굳이 복사해서 새 matrix를 만들지 않아도 되게 한다.

## Multiplying Matrices and Vectors

* standard product : $$\textbf C = \textbf A \textbf B$$
* Hadamard product (element-wise product) : $$\textbf C = \textbf A \odot \textbf B$$

### a system of linear equation

$$\textbf A \textbf x = \textbf b$$

where $$ \textbf A \in \mathbb R^{m \times n} $$, $$\textbf b \in \mathbb R^m$$ and $$\textbf x \in \mathbb R^n $$ ($$x$$ is unknown vector)

## Identity and Inverse Matrices

* Identity matrices : $$I_n \in \mathbb R^{n\times n}$$
* Invese Matrix of $$\textbf A$$ : $$\textbf A ^{-1}$$

## Linear Dependence and Span

위에서 나온 a system of linear equation식이 아래와 같다.$$\textbf A_{:,i}$$는 $$\textbf A$$의 $$i$$번째 column.

$$\textbf A \textbf x = \sum_i x_i \textbf A_{:,i} = \textbf b$$

즉, $$\textbf A$$의 column들의 linear combination으로 보는 것이다.

span은 주어진 벡터 집합에서 linear combination으로 얻을 수 있는 점의 집합이다. 따라서 $$\textbf A \textbf x = \textbf b$$식을 행렬 $$\textbf A$$의 column들의 span에 $$\textbf b$$가 있는지의 문제로 접근할 수 있는데, 이 경우 해당 span을 column space라 한다.

linear independent는 주어진 벡터 집합에서 어느 한 벡터가 다른 벡터의 linear combination으로 표현할 수 없는 경우를 말한다. linear dependent는 그 반대.

square matrix이면서 $$\textbf A$$의 column들이 linearly independent하면 singular matrix라 한다.

## Norm

* $$L^p$$ Norm
$$||x||_p = (\sum_i |x_i|^p)^{\frac 1 p}$$
* $$L^2$$ Norm = Euclidean norm
* 가끔 nonzero element의 갯수를 센 것을 $$L^0$$ norm이라 하는데, 이건 잘못된 용어. 그냥 $$L^1$$ norm으로 대체하자.
* max norm
$$||x||_\infty = \max_i |x_i|$$

## Special Kinds of Matrices and Vectors

* diagonal matrix: main diagonal 빼고 다 0인 행렬
  * multiplication이 매우 효율적
  * inverting도 매우 효율적
* symmetric matrix: $$\textbf A = \textbf A ^\intercal$$
* unit vector
$$||x||_2 = 1$$
* orthogonal vector: $$\textbf x^\intercal \textbf y = 0$$
* orthogonal matrix: $$\textbf A^\intercal \textbf A = \textbf A \textbf A^\intercal = \textbf I$$

## eigen decomposition

아래는 right eigen vector를 구하는 식인데, left는 굳이 별로 안쓴다고 한다.

$$ \textbf A \textbf v = \lambda \textbf v$$

* eigen value: $$\lambda$$
* eigen vector: $$\textbf v$$
* eigendecompositoin: $$\textbf A = \textbf V diag (\lambda) \textbf V ^{-1}$$
  * 보통 eigen value의 벡터는 내림차순으로 정렬해서 작성한다고 함.
* 임의의 real symmetric matrix는 최소한 하나의 eigen decomposition이 존재한다.
* eigen value의 부호에 따라 positive definite, positive semidefinite, negative definite, negative semidefinite로 부른다.

## Singular Value Decomposition

singular value와 singular vector로 decompose하는 것이다. square matrix가 아닐 때 eigen decomposition을 하지 못하니 쓴다고 한다.

$$\textbf A = \textbf U \textbf D \textbf V^\intercal$$

$$\textbf U$$는 $$m\times m$$이면서 orthogonal하고 그 column들이 left singular vectors이다. $$\textbf D$$는 diagonal matrix이면서 $$m \times n$$이며 main diagonal에 있는 element들이 singular values이다. $$\textbf V$$는 $$n \times n$$이면서 orthogonal하고 그 column들을 right singular vectors로 부른다.

## The Moore-Penrose Pseudoinverse

$$\textbf A^{+} = \lim_{a \rightarrow 0} (\textbf  A^\intercal \textbf  A + \alpha \textbf I) ^ {-1} \textbf  A ^\intercal $$

$$\textbf A^{+} = \textbf V \textbf D^+ \textbf U^\intercal$$

첫번째가 정의이고 실제로 구현할 때는 두번째식을 따른다고 한다. $$\textbf D^+$$는 0이 아닌 element들에 역수를 취하고 transpose해서 얻은 행렬이다.

## Trace Operator

* 정의: $$Tr(\textbf A) = \sum_i \textbf A_{i, j}$$
* 성질: $$Tr(\textbf A \textbf B \textbf C) = Tr(\textbf B \textbf C \textbf A) = ...$$

## The Determinant

* 그냥 $$det (\textbf A)$$
