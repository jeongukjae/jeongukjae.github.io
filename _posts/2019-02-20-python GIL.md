---
layout: post
title: "Python GIL"
tags:
  - python
---

얼마 전 면접을 보면서 Python 이야기가 나왔다. Python을 자주 쓰긴 한다. 하지만 아직 그 내부 구현을 상세하게 체크하는 실력이라곤 생각을 안하기도 하고 실제로 그렇게 한적도 없지만, 면접에서 GIL과 관련된 질문을 받고 나서 Python의 기초적인 내용에 대해서도 공부를 해야함을 느꼈다.

---

저도 공부하면서 작성하는 것이기 때문에 부정확한 정보를 작성할 수 있습니다. 부정확한 정보에 대해서는 메일이나 댓글을 주시면 감사하겠습니다.

## GIL(global interpreter lock)

[Python 3.7.2 Glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock)에 자세히 나와있다. 아래처럼 설명한다.

> The mechanism used by the [CPython](https://docs.python.org/3/glossary.html#term-cpython) interpreter to assure that only one thread executes Python [bytecode](https://docs.python.org/3/glossary.html#term-bytecode) at a time. This simplifies the CPython implementation by making the object model (including critical built-in types such as  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)) implicitly safe against concurrent access.

CPython 인티프리터에서 쓰이는 메커니즘인데, Python bytecode를 한번에 하나의 쓰레드로만 실행하기 위한 것이다. CPython의 구현을 쉽게하기 때문에 쓰인다고 적혀있는데, 추가적인 특징이 몇가지 적혀있다.

1. 특정 모듈이 압축이나 해쉬같은 연산이 굉장히 많이 필요한 작업을 할 때 GIL을 풀도록 할 수 있다. (release the GIL이라고 적혀있다)
2. IO 를 처리할 때 GIL이 풀려있다.

지금 당장 무슨 의미인지 알기 어려우므로 나중에 이 의미에 대해 정리하자.

예전에 "free-threaded" 인티프리터를 작성하려 했으나, single processor 인 경우에서 성능에 문제가 생겨서 제대로 만들지 못했다고 한다. 해당 성능 이슈를 해결하려면 구현이 조금 더 복잡해지고, 유지보수하기에 더 힘들어질 것이라 생각했으므로, GIL을 사용했다고 한다.

## [What is the Python Global Interpreter Lock (GIL)?](https://realpython.com/python-gil/)

위의 Real Python[^RealPython]에 올라온 글을 살펴보자. 여기서도 하나의 쓰레드가 Python Interpreter를 제어하기 위한 것이라고 한다. 다만 예를 들어서 조금 더 자세하게 작성해놓았다.

일단 예상할 수 있듯 인티프리터 실행을 한 쓰레드가 하기 때문에 여러 쓰레드를 사용할 경우 bottleneck이 될 수도 있다고 한다. 하지만 그래도 특정한 문제들을 풀 수 있다고 하는데, 예시 중 하나가 reference counting이라고 한다. reference counting에 대해서는 나중에 정리하기로 하자. GIL은 thread safe한 모델을 제공하기 때문에 몇몇 특정한 C 표준 라이브러리들이 thread safe하지 않더라도 통합하기 쉬워졌다고 한다.

### Reference Counting?

[Python 3.7.2 Documentation - Python/C API Reference Manual](https://docs.python.org/3.7/c-api/refcounting.html)을 보면 Reference Counting의 C레벨의 매크로 함수에 대한 문서가 작성되어 있다. reference count라는 것에 대해 설명하자면, 파이썬은 메모리를 관리하기 위해 객체들의 참조 횟수를 추적하는데, 해당 참조 횟수에 관한 것이다. 여기서 자세히 봐야할 점은 `void Py_DECREF(PyObject *o)`인데, 아래처럼 적혀있다.

> If the reference count reaches zero, the object’s type’s deallocation function (which must not be NULL) is invoked.

수많은 참조에 의해 reference count가 증가했다가, 후에 0이 되면 해당 오브젝트의 deallocation 함수가 호출된다고 한다. 이 때 생각할 수 있는 것이 교착상황인데, 여러 쓰레드가 reference count를 증가시키고 감소시킨다고 가정할 때, 해당 객체는 절대 release 되지 않을 수도 있고, 참조되고 있는 와중에 release될 수도 있다는 것이다. 이 상황에서 파이썬 인티프리터를 실행하는 쓰레드를 하나로 고정해버리면 그럴 일이 없다는 것이 Real Python 글의 설명인 것 같다. 운영체제 수업 등에서 가르쳐주는 Race Condition과 비슷한 상황이다.

하지만 이 역시 단점이 있는데, 역시나 첫번째는 성능 저하이고, 두번째는 deadlock이다.

## 실제 구현은?

실제 구현에 관한 부분은 [CPython의 GitHub 레포지토리(python/cpython)](https://github.com/python/cpython)의 [Python/ceval_gil.h](https://github.com/python/cpython/blob/master/Python/ceval_gil.h)와 관련된 부분에서 찾을 수 있다. 해당 파일에 GIL의 구현과 관련된 Note들이 적혀있어서 찾아보았다. GIL은 mutex로 처리되고, 각 스레드의 요구에 의해 GIL을 release/drop 하고, GIL을 acquire하려고 할 때는 특정한 밀리초를 인자로 넘기는 등 여러가지 정보들이 적혀있었는데, 파이썬의 구조를 같이 살펴볼때 도움이 될 정보들도 보였다.

## 결국 정리해보면

파이썬에서 멀티쓰레딩 성능이 떨어지는 것은, 각각의 쓰레드가 독립적으로 실행되지 못하고 GIL을 획득하였을 경우에만 실행이 되기 때문에 그런 성능 이슈를 보이는 것이다. 다만, 파이썬 Glossary에서 설명하듯, IO를 처리할때, GIL을 release하게 되는데, IO를 자주 처리하게 되는 소프트웨어같은 경우는 CPU에서 많은 연산을 처리하기 보다 IO를 기다리는 부분이 bottleneck이 될 수 밖에 없으므로 그런 경우에는 GIL이 심각한 성능 이슈를 가져오지 못할 것으로 생각된다.

결국은 쓰레드는 공유되는 메모리를 가지므로 특정 자원을 공유하는 부분에서 더 자유롭고, 편할 수 밖에 없지만, 파이썬에서 멀티쓰레딩의 경우 GIL이라는 성능상의 단점으로 작용할 수 있는 것이 존재하고, 그 대신 멀티프로세스를 사용하게 되면, 자원공유가 어려워지고 프로세스 spawn 과정에서 시간이 조금 더 지연되는 대신 각각의 태스크가 독립적으로 실행됨을 보장할 수 있을 것이다.

\+  혼자 찾고 싶은 것을 찾으면서 정리하다보니 이상한 글이 되어버렸다..

[^RealPython]: [https://realpython.com](https://realpython.com) 파이썬 관련 정보를 구글링하다보면 이런저런 글이 많이 나오는 사이트라 가끔 참고하고 있다.
