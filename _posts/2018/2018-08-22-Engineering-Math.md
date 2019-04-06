---
layout: post
title: "Engineering Math"
tags:
  - engineering math
  - 대학
---

18년 1학기에 서울시립대학교에서 수강했던 Engineering Math를 제 필요에 의해 정리해봅니다. 영어 강의이고 제가 다시 참고하기 위한 글입니다. 귀찮은 부분 다 건너 뛰어요.

## Matrix

* $$ A = (a_{ij}) $$ : collection of numbers. `i`: row, `j`: col

* $$ A = \pmatrix{ 1 & 2 & 3 \\ 4 & 5 & 6 } $$에서 1~4 방향이 `col`, 4~6 방향이 `row`. 그리고 각각이 `element`.

* $$ a_{11} = 1, a_{12} = 2, a_{13} = 3$$ ...
* $$A$$ : 2x3 matrix (#row x #col matrix)

### 연산

#### Transpose

$$ A = (a_{ij}), A^T = (a_{ji}) $$.

associative: $$(AB)^T = B^TA^T$$, $$(ABC)^T = C^TB^TA^T$$.

#### Multiplication

$$ (AB)_{ij} = \sum^n_{k=1} (A)_{ik}(B)_{kj} $$

In general, $$ AB \neq BA $$. -> matrix multiplication is non commutative. "Non-Abelian"[^non-abelian]

#### Determinant

##### for 2x2 matrix

if $$ A= \pmatrix {a & b \\ c & d} $$, then $$ det A = \|A\| = ad - be $$

##### for larger matrix

[프로그래머를-위한-선형대수1-벡터,행렬,행렬식 포스트](/프로그래머를-위한-선형대수1-벡터,행렬,행렬식/) 참고

#### Inverse

$$AA^{-1} = I $$, $$AC^T = C^TA = \|A\|I$$

$$\therefore I = \frac {AC^T} {\|A\|} = \frac {C^TA} {\|A\|} $$ (if $$\|A\| \neq 0$$)

### Eigen value problem

* $$ A\|x\rangle = \lambda \|x\rangle $$ : `eigen value problem` 

* $$ \|x\rangle $$: `eigen vector`
* $$\lambda$$: `eigen value`

$$A\|x_\lambda\rangle = \lambda \|x_\lambda\rangle $$.

#### Hermitian matrix

A matrix $$A$$ is the hermitian matrix if $$ (A^T)^* = A $$  ($$^*$$ = complex conjugate) [^daggar-operator]

#### norm

$$\langle x_\lambda \| = (\|x_\lambda\rangle)^\dagger$$, $$ \langle x_\lambda \| x_\lambda \rangle$$: inner product

$$\sqrt{ \langle x_\lambda \| x_\lambda \rangle}$$ called `norm` of a vector $$ \|x_\lambda\rangle$$

#### normalized vector

$$\|e_\lambda\rangle$$ : normalized vector

$$\|e_\lambda \rangle = \frac 1 {\sqrt{ \langle x_\lambda \| x_\lambda \rangle}} \|x_\lambda \rangle$$, $$\langle e_\lambda \|e_\lambda \rangle = \frac 1 { \langle x_\lambda \| x_\lambda \rangle} \langle x_\lambda \|x_\lambda \rangle = 1$$

#### Eigen value problem

1. $$ det (A - \lambda I) \neq 0 $$ : $$\|x_\lambda\rangle = 0$$ : null vector
2. $$ det (A - \lambda I) = 0 $$ then we have an arbitrary solution.

* we will be focusing on the "Hermitian matrix" only

### Other matrices

#### Identity matrix

$$ IA = AI = I$$. Identity matrix `I` plays the same role as the number `1` in the multiplication of numbers.

#### Square matrix

* square matrix: nxn matrix
* closed to addition, subtraction and multiplication

Example : $$I = \pmatrix {1 & 0 & 0 & ... \\ 0 & 1 & 0 & ... \\ 0 & 0 & 1 & ... \\ ... & ... & ... & ... }$$ [^kronecker-delta]

#### Column, Row Vector

$$ \pmatrix {x_1 \\ x_2 \\ ...} $$ : column vector (column matrix) or ket vector[^bra-ket-notation]

$$ \pmatrix {x_1 & x_2 & ...} $$ : row vector (row matrix) or bra vector[^bra-ket-notation]

##### braket notation

$$ \langle x \| y \rangle = \pmatrix{x_1 & x_2 & ...} \pmatrix {y_1 \\ y_2 \\ ... } $$.

#### Pauli matrix

## Differential equation

### Ordinary Differential Equation O.D.E.

### Partial Differential Equation P.D.E.

### Exact & Separable

### O.D.E.

#### Integrating Factor

#### Homogeneous & Inhomogeneous

### Equidimensional O.D.E.

#### Inhomogen

[^non-abelian]: [https://en.wikipedia.org/wiki/Non-abelian_group](https://en.wikipedia.org/wiki/Non-abelian_group)
[^kronecker-delta]: [https://en.wikipedia.org/wiki/Kronecker_delta](https://en.wikipedia.org/wiki/Kronecker_delta)
[^bra-ket-notation]: [https://en.wikipedia.org/wiki/Bra–ket_notation](https://en.wikipedia.org/wiki/Bra–ket_notation)

[^daggar-operator]: https://en.wikipedia.org/wiki/Conjugate_transpose 수업에서는 dagger로 주로 쓰셨다.