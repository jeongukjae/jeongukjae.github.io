---
layout: post
title: "python assignment operator"
tags:
  - python
---

python 3.8.0 a1, [a2](https://www.python.org/downloads/release/python-380a2/) 버전이 2월달에 릴리즈되었다. 4개의 알파버전 중 두번째인 a2버전은 2월 25일에 출시되었다. 베타가 나오기 전 (alpha phase, ~2019-05-26)에 새로운 기능들이 추가된다고 한다.

이번 알파버전 Changelog에 3.7과의 차이점을 기술해놓았는데, 그 중 눈에 띄는 점이 [PEP 572](https://www.python.org/dev/peps/pep-0572/)이다. Assignment Operator (Operator가 바다코끼리의 이빨과도 비슷하게 생겨서 Walrus Operator라고도 부르는 것 같다)에 관한 내용이며, 해당 문서의 Abstract는 아래와 같다.

> This is a proposal for creating a way to assign to variables within an expression using the notation `NAME := expr`. A new exception, `TargetScopeError` is added, and there is one change to evaluation order.
