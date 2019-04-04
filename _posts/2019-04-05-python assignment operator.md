---
layout: post
title: "python assignment operator (PEP 572)"
tags:
  - python
---

python 3.8.0 a1, [a2](https://www.python.org/downloads/release/python-380a2/) 버전이 2월달에 릴리즈되었다. 4개의 알파버전 중 두번째인 a2버전은 2월 25일에 출시되었다. 베타가 나오기 전 (alpha phase, ~2019-05-26)에 새로운 기능들이 추가된다고 한다.

이번 알파버전 Changelog에 3.7과의 차이점을 기술해놓았는데, 그 중 눈에 띄는 점이 [PEP 572](https://www.python.org/dev/peps/pep-0572/)이다. 귀도 반 로썸이 싸우고 파이썬의 자비로운 종신독재자에서 물러서게 된 사건의 시작이 PEP 572이다. Assignment Operator (Operator가 바다코끼리의 이빨과도 비슷하게 생겨서 Walrus Operator라고도 부르는 것 같다)에 관한 내용이며, 해당 문서의 Abstract는 아래와 같다.

> This is a proposal for creating a way to assign to variables within an expression using the notation `NAME := expr`. A new exception, `TargetScopeError` is added, and there is one change to evaluation order.

assignment operator를 추가하고 그를 사용하면서 생길 수 있는 `TargetScopeError`를 추가하자는 것이다.

## 사용해보기

일단 말을 많이 하는 것보다 사용해보고자 해서 설치해보았다. `pyenv`를 이용해서 설치했고 아래처럼 설치하면된다.

```bash
$ pyenv install 3.8-dev
$ # pyenv에 설치된 모든 버전을 바로 사용이 가능하게 한다.
$ # python3.x 처럼 치면 모든 버전에 바로 접근이 가능해진다.
$ pyenv global `pyenv versions --bare`
$ python3.8 -V
Python 3.8.0a2+
```

일단 어떻게 사용하는지 보기 위해 PEP572를 다시 보니 예시를 몇가지 제시해놓았다. 우선 가장 눈에 띄는 코드를 가져왔다. 아래와 같은 코드를 프로그래머들이 작성하는 것을 막을 수 있다고 한다.

```python
match1 = pattern1.match(data)
match2 = pattern2.match(data)
if match1:
    result = match1.group(1)
elif match2:
    result = match2.group(2)
else:
    result = None
```

이 예시는 `match1`이어도 `match2`를 계산하는데, 만약 그렇지 않게 작성하려면 indentation을 아래쪽에 모두 넣어주어야 한다.

```python
match1 = pattern1.match(data)
if match1:
    result = match1.group(1)
else:
    match2 = pattern2.match(data)
    if match2:
        result = match2.group(2)
    else:
        result = None
```

이렇게..

하지만 이걸 assignment operator를 사용한다고 생각하니 이렇게 고칠 수 있다.

```python
import re

pattern1 = re.compile(r"([1-9]+)")
pattern2 = re.compile(r"([a-z]+)")

if match1 := pattern1.match(data):
    result = match1.group(1)
elif match2 := pattern2.match(data):
    result = match2.group(2)
else:
    result = None
```

`data = "1234"`를 넣으니 아래처럼 결과가 나온다.

```python
>>> result
'1234'
```

그리고 `data = "abcde"`라고 넣으니 이렇게 나온다.

```python
>>> if match1 := pattern1.match(data):
...     result = match1.group(1)
... elif match2 := pattern2.match(data):
...     result = match2.group(2)
... else:
...     result = None
...
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
IndexError: no such group
```

당연히 그룹 하나만 잡았으니 (`r"([a-z]+)"`) 에러가 나야한다. 그걸 보면 잘 동작하는 듯 싶다.

## 실제로 사용할때가 되면 어떨까

PEP 572를 구글에 검색하면 "pep 572 guido"가 먼저 나올 정도로 핫한 이슈였다. 주요 논쟁점은 "파이썬에서 이미 할당하는 연산자(`=`)가 존재하는데 왜 하나를 더 만드나". 파이썬에서는 무언가를 하기 위해 하나의 길만 있어야 함을 철학으로 삼고 있다. (파이썬에서 `import this`를 실행하면 "There should be one-- and preferably only one --obvious way to do it." 이 문장이 포함되어 있다)

그 철학을 기준으로 볼 때 물론 PEP572는 좋지 않은 제의라고 볼 수 있지만, 지금 파이썬을 주로 사용하는 입장에서 볼 때 파이썬은 이미 충분히 많은 복잡한 문법이 존재하는 편이다. 처음에는 double list comprehension을 왜 그렇게 작성을 했나 할 정도로 익숙해지면 꽤 좋지만, 처음에는 당황스러운 문법이 몇몇 존재한다고 생각한다.

물론 다른 "더" 복잡한 문법이 존재한다고 assignment operator를 도입해야 한다는 것은 아니다. 다만, walrus operator는 이미 다른 언어에서 채택해서 사용하고 있는 문법 중 하나임에는 틀림없고, 분명히 라인 수를 줄이면서 직관적인 코드를 작성할 수 있다. 또한 위의 예시같은 상황에서 볼 때 assignment operator를 도입하면 다른 파이썬의 철학("Flat is better than nested." 외의 몇몇 개의 문장들)에 매우 적합하게 코드를 작성할 수 있다고 생각한다.

또 C언어처럼 walrus operator가 존재하지 않는 언어에서는 if문에서 `==`을 써야할 것을 `=`를 써서 잘못 작동하는 코드를 작성하는 경우가 있다. 그런 오류를 미리 작성자의 의도를 굳이 알지 않아도 잡아줄 수 있는 것으로 생각한다고 하면 assignment operator를 추가로 도입하는 것이 좋은 일이 아닌가 싶다.
