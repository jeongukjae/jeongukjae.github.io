---
layout: post
title: " Python Iterator"
tags:
  - python
---

Python을 자주 사용하기는 하지만, 제대로 처음부터 개념을 본적은 많이 없기 때문에, 계속해서 자주 사용하는 용어, 개념들에 대해서 정리해보기로 했다. (Python 공식문서의 [Glossary](https://docs.python.org/3/glossary.html)에 중요한 용어 등이 정리되어 있다.)

## `Iterator`

`iterator`는 데이터 스트림(stream of data)을 표현하는 객체이다. `__next__()`를 계속해서 호출하면서 연속되는 값들을 받아온다. 단, 더 이상 받아올 값들이 존재하지 않을 때에는 [`StopIternation`](https://docs.python.org/3/library/exceptions.html#StopIteration)이라는 오류가 발생한다. 이 `iterator` 객체들은 [`__iter__()`](https://docs.python.org/3/reference/datamodel.html#object.__iter__) 메소드가 반드시 선언되어 있어야한다.

추가적으로 [Iterator Types](https://docs.python.org/3/library/stdtypes.html#typeiter)에서 설명을 더 찾을 수 있는데, Python은 iteration을 `container`로 지원한다고 한다. `list`를 예로 들자면, `list` 자체가 `container` object가 되는 것이다. 하지만, `list`가 `iterator`가 되는 것은 아니고, `iterator` 객체를 반환하는 메소드를 구현해놓은 `container`가 되는 것이다. 즉 아래처럼 `iterator`가 동작하는 것이다.

```python
>>> list_1 = list([1, 2, 3])
>>> list_1
[1, 2, 3]
>>> iterator_of_list = list_1.__iter__()
>>> iterator_of_list.__next__()
1
>>> iterator_of_list.__next__()
2
>>> iterator_of_list.__next__()
3
>>> iterator_of_list.__next__()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

### user defined `iterator` & `container`

또한 위의 문서에서 iteration을 user-defined class들에서 지원하기 위해 특정한 메소드들을 작성하라고 적혀있다. 위의 `list` 예시에서 볼 수 있듯, `container` object에서는 `__iter__()`를 작성하라고 한다. 하지만, `iterator` 자체를 구현하려면, [iterator protocol](https://docs.python.org/3/c-api/iter.html)에서 알 수 있듯이, 두가지 메소드를 구현해야한다.

첫번째는 `__iter__()` 메소드이고, 자기자신을 반환한다고 한다. 자기자신을 반환할 것이면 타입체킹으로 가능하지 않나 싶었지만, 아래처럼 `container`와 `iterator` 둘 다 `for`, `in` 둘 다 사용하기 위함이라고 적혀있다.

> Return the iterator object itself. This is required to allow both containers and iterators to be used with the [`for`](https://docs.python.org/3/reference/compound_stmts.html#for) and [`in`](https://docs.python.org/3/reference/expressions.html#in) statements.

두번째는 `__next__()` 메소드이고, 위의 사용법에서 알 수 있듯이 다음 값들을 반환하는 메소드이다. 만약 더 이상 반환할 값이 존재하지 않는다면, [`StopIteration`](https://docs.python.org/3/library/exceptions.html#StopIteration)을 raise 한다고 한다.

위에서 설명했던 예제를 확인하기 위해 `list`에서 `__next__()`를 호출해보면 아래처럼 오류를 일으킨다.

```python
>>> list_1 = list([1,2,3])
>>> list_1.__next__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute '__next__'
```

### iterable

Python을 사용하다보면, `iterator`대신 `iterable`이라는 말도 볼 수 있는데, 이는 한번에 하나의 값을 반환할 능력이 있는 (iteration이 가능한) 객체를 말한다. `list`, `str`, `tuple`등이 있다.

## Asynchronous Generator Iterator

Glossary를 보다가 [aynchronous generator iterator](https://docs.python.org/3/glossary.html#term-asynchronous-generator-iterator)라는 용어를 발견헀다. 일단 관련된 용어를 정리하자면 아래와 같다.

### asynchronous iterable

[`async for`](https://docs.python.org/3/reference/compound_stmts.html#async-for) 문법에서 사용가능한 object를 말한다고 한다. `asynchronous iterator`를 `__aiter__`를 호출했을때 반환해야한다고 한다. [PEP 492](https://www.python.org/dev/peps/pep-0492)를 살펴보자.

나름 Python에 관해서 소식을 많이 듣고 있다고 생각하고 있었는데, `async for` 문법 자체를 처음본다..

#### PEP 492

PEP 492는 `async`, `await` 문법과 함께 코루틴을 다룬다. 더 자세한 내용은 나중에 기회가 되면 보기로 하고, 지금은 궁금했던 내용만 찾아서 보자.

[Asynchronous Iterator and "async for"](https://www.python.org/dev/peps/pep-0492/#asynchronous-iterators-and-async-for)라는 목차가 중간에 있는데, 간략하게 정리해보면 아래와 같다.

일반적인 `iterator`와 똑같이 `__aiter__`를 전부 구현해야한다. 그리고 `__anext__`도 구현을 해야 `asynchronous iterator`로 사용이 가능하다고 한다. 역시나 멈추기 위해서는 `__anext__`를 호출했을 때, `StopAsyncIteration`을 raise해야한다고 한다. `__aiter__`에서 다른 객체를 반환한다면, `container`처럼도 구현할 수 있을 것 같지만, `container`에 관한 설명은 없으므로 건너뛴다.

이 `asynchronous iterator`를 이용해서 `async for`를 사용할 수 있는데, 문법은 일반적인 `for`와 사용법이 같고 앞에 `aync`만 붙여준다.

```python
async for TARGET in ITER:
  BLOCK
else:
  BLOCK2
```

위의 문법은 아래와 같다고 한다.

```python
iter = (ITER)
iter = type(iter).__aiter__(iter)
running = True
while running:
    try:
        TARGET = await type(iter).__anext__(iter)
    except StopAsyncIteration:
        running = False
    else:
        BLOCK
else:
    BLOCK2
```

Python에서 비동기/코루틴이 어떻게 구현되어있고, 어떻게 동작하는지 확실하지 않기 떄문에 이 부분에 대해서 공부해야할 것 같다. 하지만 코드를 보면, API Call이나, 여러가지 네트워크 관련 연산이 필요할 때 유용할 듯 하다.

### asynchronous iterator

위에서 설명한 것과 같이 `__aiter__`와 `__anext__`를 구현해야한다. 또 더 이상 반환할 값이 없을 때 [`StopAsyncIteration`](https://docs.python.org/3/library/exceptions.html#StopAsyncIteration)을 호출한다.

### asynchronous generator iterator

`generator`가 asynchronous하게 구현되었는데, 그 `generator function`에 의해 생성된 객체가 `asynchronous generator iterator`이다.

---

iterator를 정리해보면서 부족한 점도 많이 느꼈고, 앞으로 공부해야할 것들이 산더미인 것을 깨닫는다.. ㅠㅠ

TOOD:

* coroutine/async/await in python
* asyncio 정리
* generator
