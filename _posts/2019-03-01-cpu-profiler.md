---
layout: post
title: python의 profiler
tags:
  - python
---

파이썬을 사용하면서 프로파일링을 통해 실제로 어느 코드가 병목점인지, 어느 코드를 수정해야할 지 알고 싶을 때가 있다. 그럴 때 사용가능한 모듈들을 [고성능 파이썬](https://book.naver.com/bookdb/book_detail.nhn?bid=10910544)에서 잘 설명해주어서 Python 공식문서의 [The Python Profiler](https://docs.python.org/3.7/library/profile.html)의 내용과 함께 정리해보았다.

## 프로파일링이란

위키백과에서는 프로파일링을 다음과 같이 설명한다. "space complexity나, time complexity, 또는 실제 메모리 사용량, 실행시간 등등을 측정해보는 동적인 프로그램 분석". 주로 퍼포먼스 향상을 목표로 병목점을 찾기 위해 사용한다고 한다.

## 파이썬 프로파일러

[The Pytho Profiler](https://docs.python.org/3.7/library/profile.html)라는 제목의 파이썬 문서에서는 두가지 프로파일러를 소개한다. `cProfile`과 `profile`이라는 모듈인데, 아래처럼 설명한다.

> 1. `cProfile` is recommended for most users; it’s a C extension with reasonable overhead that makes it suitable for profiling long-running programs. Based on `lsprof`, contributed by Brett Rosen and Ted Czotter.
> 2. `profile`, a pure Python module whose interface is imitated by `cProfile`, but which adds significant overhead to profiled programs. If you’re trying to extend the profiler in some way, the task might be easier with this module. Originally designed and written by Jim Roskind.

즉, `cProfile`은 lsprof 기반의 C확장 모듈이라 오버헤드가 심하지 않아 대부분의 사용자에게 추천하며, `profile`은 순수 파이썬 코드라 오브헤드가 좀 있는 편이다. 다만 `cProfile` 인터페이스과 비슷하게 만들어졌고 커스터마이징을 할 경우 이 모듈을 이용하면 좋을 것이라고 한다.

고성능 파이썬이라는 책에서는 한가지 모듈을 더 설명한다. `hotshot`이라는 모듈인데, 이 모듈은 2.7 문서에는 존재하지만,[^hotshot] 3.5 이후로는 존재하지 않는 것으로 보아 사라진 것 같다..

### [`cProfile`](https://docs.python.org/3.7/library/profile.html#module-cProfile)

`cProfile`은 실제로 코드 내에서 사용할 수도 있지만, 그럴 일은 많지 않을 것 같아서 아래와 같은 사용법만 찾아보았다.

```bash
python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)
```

cProfile의 결과를 더 자세히 알아보기 위해서 프로파일링 결과를 파일로 만들어(`-o` 옵션) 다시 불러온 다음 살펴볼 수 있다고 한다. 또한 `-s` 옵션으로 정렬방법을 지정할 수 있는데, `-s cumulative`로 지정할 경우 각 함수에서 얼마나 시간을 소비했는지 누적시켜 정렬해주므로, 어떤 함수가 느린지 쉽게 확인할 수 있다고 한다. 불러올 때는 [`pstats`](https://docs.python.org/3/library/profile.html#module-pstats) 모듈을 참고하자. 간단하게 사용을 해보기 위해 제곱수의 합을 구하는 코드를 아래처럼 작성하였다.

```python
k = 0

for i in range(1000):
    x = i ** 2
    k += x

print(k)
```

그리고 그 결과값을 보기 위해 아래처럼 실행시켰다.

```bash
$ python3.6 -m cProfile test.py
332833500
         4 function calls in 0.001 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.001    0.001 test.py:1(<module>)
        1    0.000    0.000    0.001    0.001 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

각 함수별 프로파일링 결과를 출력해준다. 프로파일링 결과는 프로그램이 종료된 뒤 출력되는 것으로 보인다. 함수별로 프로파일링을 실행할 때 유용할 것 같은 도구이다.

### [`line_profiler`](https://github.com/rkern/line_profiler)

파이썬 기본 도구가 아니지만, 파이썬 코드를 한 줄씩 프로파일링할 수 있다. `line_profiler`의 레포지토리의 [`README.rst`](https://github.com/rkern/line_profiler/blob/master/README.rst)에서 아래처럼 기본 프로파일링 도구들의 문제점을 설명한다.

> The current profiling tools supported in Python 2.7 and later only time function calls. This is a good first step for locating hotspots in one's program and is frequently all one needs to do to optimize the program. However, sometimes the cause of the hotspot is actually a single line in the function, and that line may not be obvious from just reading the source code.

파이썬의 프로파일링 도구가 함수 호출 단위별로 분석을 해주기 때문에 맨 처음 병목지점을 대략적으로 잡아내기에 좋다고 한다. 하지만 그런 특성 때문에 실제로 개별 라인을 기준으로 병목점을 찾아내기에는 좋지 않다는 것이다. 그래서 `cProfile`과 같은 모듈로 어떤 함수를 살펴볼지에 대해 방향을 잡고, `line_profiler`로 상세한 프로파일링을 진행하면 된다는 것이다.

`line_profiler`는 아래처럼 설치할 수 있다. Line Profiler는 아래처럼 설치 후, `kernprof`이라는 명령어를 통해 실행할 수 있다.

```bash
pip install line_profiler
```

프로파일링을 위해 아래처럼 코드를 수정해주어야 한다.

```python
@profile
def some_function():
  k = 0

  for i in range(1000):
      x = i ** 2
      k += x

  print(k)

some_function()
```

함수 내부의 라인을 분석하기 때문에 분석할 함수에 `@profile` 데코레이터를 추가해준다. `@profile` 데코레이터 사용을 위해 특별히 모듈을 import할 필요는 없다. 그 이유는 `kernprof`를 실행할 때 Line Profiler가 `__builtins__` 네임스페이스에 자동으로 `profile`을 추가해주기 때문이다. `kernprof` 사용은 아래처럼 할 수 있다.

```bash
kernprof -l script_to_profile.py
```

`-l` 옵션은 함수 단위가 아닌 라인 단위로 프로파일링을 한다는 것이다. 하지만 위처럼 실행할 경우 프로파일링 결과가 파일로 남게되는데 바로 보고 싶을 경우는 `-v`옶션을 주면 된다. 위에서 작성한 예시 파일은 아래처럼 프로파일링할 수 있다.

```bash
$ kernprof -l -v test.py
332833500
Wrote profile results to test.py.lprof
Timer unit: 1e-06 s

Total time: 0.002131 s
File: test.py
Function: some_function at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def some_function():
     3         1         10.0     10.0      0.5    k = 0
     4
     5      1001        506.0      0.5     23.7    for i in range(1000):
     6      1000        929.0      0.9     43.6        x = i ** 2
     7      1000        592.0      0.6     27.8        k += x
     8
     9         1         94.0     94.0      4.4    print(k)

```

위의 내용을 토대로 어떤 라인이 시간을 많이 소비하는지 알 수 있다. 위의 코드에서는 제곱을 하는 부분이 제일 많이 시간을 소비하였는데, 약 43.6% 정도의 시간을 소비하였다. 책에서 추가적으로 아래와 같은 순서로 분석을 하면 좋다고 한다. 이렇게 할 경우 정확히 어떤 부분이 문제인지 알 수 있게 되고, 그 근거를 토대로 수정을 할 경우 안정적인 성능 개선을 기대할 수 있다고 한다.

1. 어떤 함수가 제일 시간을 많이 소비하는지
2. 그 함수에서 어떤 라인이 병목점인지
3. 해당 라인이 충분히 길 경우 `timeit`을 통해 어떤 명령이 병목점인지

timeit은 이전에 공부를 하면서 [포스트](/posts/python에서-시간측정하기/)로 작성을 했었기 때문에, 건너 뛴다.

---

메모리 프로파일링은 다음에!

[^hotshot]: [https://docs.python.org/2/library/hotshot.html](https://docs.python.org/2/library/hotshot.html) 이 모듈도 C로 작성된 것으로 보인다.
