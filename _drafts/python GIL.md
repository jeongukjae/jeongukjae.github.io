---
layout: post
title: "Python GIL"
tags:
  - python
---

얼마 전 면접을 보면서 Python 이야기가 나왔다. Python을 자주 쓰긴 한다. 하지만 아직 그 내부 구현을 상세하게 체크하는 실력이라곤 생각을 안하기도 하고 실제로 그렇게 한적도 없지만, 면접에서 GIL과 관련된 질문을 받고 나서 Python의 기초적인 내용에 대해서도 공부를 해야함을 느꼈다.

## GIL(global interpreter lock)

[Python 3.7.2 Glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock)에 자세히 나와있다. 아래처럼 설명한다.

> The mechanism used by the [CPython](https://docs.python.org/3/glossary.html#term-cpython) interpreter to assure that only one thread executes Python [bytecode](https://docs.python.org/3/glossary.html#term-bytecode) at a time. This simplifies the CPython implementation by making the object model (including critical built-in types such as  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)) implicitly safe against concurrent access.

CPython 인티프리터에서 쓰이는 메커니즘인데, Python bytecode를 한번에 하나의 스레드로만 실행하기 위한 것이다. CPython의 구현을 쉽게하기 때문에 쓰인다고 적혀있는데, 추가적인 특징이 몇가지 적혀있다.

1. 특정 모듈이 압축이나 해쉬같은 연산이 굉장히 많이 필요한 작업을 할 때 GIL을 풀도록 할 수 있다. (release the GIL이라고 적혀있다)
2. IO 를 처리할 때 GIL이 풀려있다.

지금 당장 무슨 의미인지 알기 어려우므로 나중에 이 의미에 대해 정리하자.

예전에 "free-threaded" 인티프리터를 작성하려 했으나, single processor 인 경우에서 성능에 문제가 생겨서 제대로 만들지 못했다고 한다. 해당 성능 이슈를 해결하려면 구현이 조금 더 복잡해지고, 유지보수하기에 더 힘들어질 것이라 생각했으므로, GIL을 사용했다고 한다.

자 일단 CPython이 기본적인 Python 구현체[^CPython]이기 때문에 이제 뭔지 제대로 알아보자.

## [What is the Python Global Interpreter Lock (GIL)?](https://realpython.com/python-gil/)

위의 Real Python에 올라온 글을 살펴보자.

[^CPython]: [https://www.python.org/downloads/](https://www.python.org/downloads/) python.org에서 "This site hosts the "traditional" implementation of Python (nicknamed CPython)."라고 설명한다.
