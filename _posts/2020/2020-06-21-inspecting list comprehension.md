---
layout: post
title: List Comprehension이 빠른 이유를 찾아보자
tags:
  - python
---

Python을 어느정도 쓰는 사람이면 누구나 듣는 "List Append를 하는 것보다 List Comprehension을 써서 구현하는 것이 더 빠르고 간결하다."라는 말. 하지만 실제 내부 동작과 더불어 설명하는 사람은 드물다. 실제 구현이 어떻게 되어 있길래 그렇게들 말하는 것일까?

> Python 3.7.7 기준으로 작성되었으며, 버전 별로 실제 동작은 다를 수 있음을 알려드립니다.

## 속도 비교

```shell
$ python3.7 -m timeit "result = []
dquote> for i in range(10000000):
dquote>     result.append(i)"
1 loop, best of 5: 641 msec per loop
$ python3.7 -m timeit "result = [i for i in range(10000000)]"
1 loop, best of 5: 388 msec per loop
```

우선 아래의 문법이 List Comp 방식이고 위 방식이 for loop를 돌며 append해가는 방식이다. 이 두가지 방식의 실행시간을 timeit으로 비교해보니 꽤 많은 시간이 차이가 난다. 이 두가지 방식의 차이는 무엇일까?

## Byte code 비교

```python
Python 3.7.7 (default, Jun 20 2020, 16:27:13)
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import dis
>>> def append():
...     result = []
...     for i in range(10000):
...             result.append(i)
...     return result
...
>>> dis.dis(append)
  2           0 BUILD_LIST               0
              2 STORE_FAST               0 (result)

  3           4 SETUP_LOOP              26 (to 32)
              6 LOAD_GLOBAL              0 (range)
              8 LOAD_CONST               1 (10000)
             10 CALL_FUNCTION            1
             12 GET_ITER
        >>   14 FOR_ITER                14 (to 30)
             16 STORE_FAST               1 (i)

  4          18 LOAD_FAST                0 (result)
             20 LOAD_METHOD              1 (append)
             22 LOAD_FAST                1 (i)
             24 CALL_METHOD              1
             26 POP_TOP
             28 JUMP_ABSOLUTE           14
        >>   30 POP_BLOCK

  5     >>   32 LOAD_FAST                0 (result)
             34 RETURN_VALUE
>>> timeit.timeit("append()", setup="from __main__ import append", number=10000)
6.290953219999892
```

append 방식을 `dis.dis`로 바이트 코드를 살펴보자. `BUILD_LIST` 후 `SETUP_LOOP` 하고, 14 ~ 28까지 루프를 돈다.

```python
>>> def list_comp():
...     return [i for i in range(10000)]
...
>>> dis.dis(list_comp)
  2           0 LOAD_CONST               1 (<code object <listcomp> at 0x10df3d660, file "<stdin>", line 2>)
              2 LOAD_CONST               2 ('list_comp.<locals>.<listcomp>')
              4 MAKE_FUNCTION            0
              6 LOAD_GLOBAL              0 (range)
              8 LOAD_CONST               3 (10000)
             10 CALL_FUNCTION            1
             12 GET_ITER
             14 CALL_FUNCTION            1
             16 RETURN_VALUE

Disassembly of <code object <listcomp> at 0x10df3d660, file "<stdin>", line 2>:
  2           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                 8 (to 14)
              6 STORE_FAST               1 (i)
              8 LOAD_FAST                1 (i)
             10 LIST_APPEND              2
             12 JUMP_ABSOLUTE            4
        >>   14 RETURN_VALUE
>>> timeit.timeit("list_comp()", setup="from __main__ import list_comp", number=10000)
3.2182092880000255
```

List Comprehension이 굉장히 특이했던 것이 listcomp로 `MAKE_FUNCTION`을 한 후 해당 함수를 호출하는 방식으로 구현되었다는 것이다. `LOAD_GLOBAL`, `LOAD_CONST`, `CALL_FUNCTION`, `GET_ITER`로 range 함수의 반환값을 받아온 다음에 `CALL_FUNCTION`으로 List Comprehension을 호출한다.

### 상세 분석

우선 다르다고 의심할 수 있는 부분은 List Append 부분과 Function Call 부분이다.

List Append를 바이트 코드로 구현했기 때문에 최적화가 되어있다고 생각해볼 수 있을 것 같고, *Function Call 오버헤드가 굉장히 크다고 가정*할 경우에 Iteration안에 `CALL_METHOD`가 있는 Append 방식이 덜 최적화가 된 코드라고 생각할 수 있을 것 같다.

#### `LIST_APPEND` Byte Code

그럼 실제 바이트 코드 구현을 살펴보자. `LIST_APPEND`의 바이트 코드 해석 부분은 [https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1382](https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1382)에 있고, 해당 케이스는 `PyList_Append` 함수([https://github.com/python/cpython/blob/3.7/Objects/listobject.c#L301](https://github.com/python/cpython/blob/3.7/Objects/listobject.c#L301))를 호출한다.

하지만 해당함수에서 호출하는 `app1`은 실제로 Python의 `list` 구현체의 append 메소드([https://github.com/python/cpython/blob/3.7/Objects/listobject.c#L802](https://github.com/python/cpython/blob/3.7/Objects/listobject.c#L802))에서 사용하는 함수이기 때문에 같은 구현체라 볼 수 있다. 정말 [`dis`모듈의 `LIST_APPEND` 설명](https://docs.python.org/3.7/library/dis.html#opcode-LIST_APPEND)처럼 그냥 List Comprehension용으로 구현된 것으로 보인다. 당연히 memory resize하는 전략도 같다.

#### `CALL_METHOD` Byte Code

Python의 `CALL_METHOD` 구현을 찾아보면 [https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3071](https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3071)에 있고, 부르는 함수를 타고타고 들어가면서 읽다보면 CallStack을 저장하면서 함수 Input, Output 확인하고 실행하는 코드인 것으로 보인다.

하지만 이렇게 확인하면 굉장히 오래 걸릴 것 같아서 간단하게 timeit으로 확인을 해보니

```sh
$ python3.7 -m timeit -s "def empty(): pass" "for i in range(10000000): empty()"
1 loop, best of 5: 555 msec per loop
```

찾았다!

#### 더 찾아보자

그럼 함수 콜 안하고 루프만 도는 것이 얼마나 느릴까?

```sh
$ python3.7 -m timeit "for i in range(10000000): pass"
2 loops, best of 5: 164 msec per loop
```

그럼 (함수 콜 + 루프) - (루프) => 함수만 콜하는 시간 .. 하면 그냥 함수 콜이 겁나 느리다.

## 정리

역시나 조금 글이 정리가 많이 안되었지만, list comprehension이 빠른 이유는 Loop + Append 방식에 비해 Function Call 횟수를 굉장히 많이 줄였기 때문이다.
