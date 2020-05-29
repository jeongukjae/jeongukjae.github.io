---
layout: post
title: flask에서 profiling 하기
tags:
  - python
---

얼마 전 `flask`를 사용하는 환경에서 프로파일링을 할 필요가 생겼는데, `cProfile`은 아무래도 실행 한번에 대해서 프로파일링을 해주다보니, 사용하는 것에 어려움이 있었다. 그래서 `flask`에서 프로파일링을 진행하는 방법을 찾아보게 되었는데, 아래와 같은 방법으로 사용가능하다고 한다. 이 방식은 `flask`에서 받는 request 한번 당 프로파일링 한번을 해준다.

```python
from flask import Flask

from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
app.run()
```

위와 같은 설정을 해서 한번 프로파일링 결과를 뽑아봤는데 아래처럼 나온다.

```text
--------------------------------------------------------------------------------
PATH: '/'
         12423 function calls (11924 primitive calls) in 0.015 seconds

   Ordered by: internal time, call count

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    76/18    0.002    0.000    0.007    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:475(_parse)
   135/18    0.001    0.000    0.003    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:71(_compile)
     1193    0.001    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:233(__next)
        2    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
      910    0.001    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:164(__getitem__)
     1082    0.001    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:254(get)
   166/50    0.001    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:174(getwidth)
       15    0.000    0.000    0.002    0.000 {built-in method builtins.__build_class__}
       90    0.000    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:276(_optimize_charset)
     1095    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
     1978    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
1606/1459    0.000    0.000    0.000    0.000 {built-in method builtins.len}
    63/18    0.000    0.000    0.007    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:417(_parse_sub)
       76    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:343(_escape)
       20    0.000    0.000    0.011    0.001 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/re.py:271(_compile)
       18    0.000    0.000    0.011    0.001 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:759(compile)
       90    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:249(_compile_charset)
      304    0.000    0.000    0.000    0.000 {built-in method builtins.min}
      257    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:172(append)
      199    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:286(tell)
       18    0.000    0.000    0.001    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:536(_compile_info)
      326    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:249(match)
        6    0.000    0.000    0.000    0.000 {built-in method posix.stat}
      294    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:160(__len__)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:914(get_data)
      147    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:111(__init__)
       18    0.000    0.000    0.007    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:919(parse)
        1    0.000    0.000    0.013    0.013 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/site-packages/werkzeug/test.py:10(<module>)
       27    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:408(_uniq)
        1    0.000    0.000    0.012    0.012 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/http/cookiejar.py:26(<module>)
      184    0.000    0.000    0.000    0.000 {method 'find' of 'bytearray' objects}
       57    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
       18    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/enum.py:827(__and__)
       42    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/enum.py:537(__new__)
      132    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
       64    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:423(_simple)
        7    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:413(<listcomp>)
       32    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_parse.py:84(opengroup)
       18    0.000    0.000    0.003    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/sre_compile.py:598(_code)
       42    0.000    0.000    0.000    0.000 {홈 디렉토리예요!!!!}/.pyenv/versions/3.7.0/lib/python3.7/enum.py:281(__call__)

--------------------------------------------------------------------------------

127.0.0.1 - - [04/Apr/2019 00:14:29] "GET / HTTP/1.1" 404 -
```

기본적으로 `tottime` 기준으로 정렬을 해준다. 근데 이게 아무것도 없는 404에러를 처리하는데도 함수 호출이 12423번 일어나니, 프로파일링 결과가 아무래도 너무 길 수밖에 없다. 그래서 `ProfilerMiddleware`에 `restrictions = [30]`과 같은 형식으로 추가인자를 넣어주면 상위 30개만 나오도록 조정할 수 있다.
