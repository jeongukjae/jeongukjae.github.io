---
layout: post
title: Flask로 CI 구성해보기
tags:
  - python
---

간단한 예제를 보기 이전에, 이 예제는 python3를 기준으로 작성되고, Flask를 이용하여 작성되며, Virtualenv를 활용하기 때문에 혹시 읽다가 잘 모르시겠다면 아래의 링크를 참고하시면 될 것 같습니다.

* [Python3 공식 사이트](https://www.python.org/)
* [Flask 공식 문서](http://flask.pocoo.org/docs/0.12/)
* [Virtualenv 공식 문서](https://virtualenv.pypa.io/en/stable/)

## 플라스크 개발환경

### 개발환경 갖추기

먼저 virtualenv를 사용하여 개발환경을 갖추고, Flask와 필요한 라이브러리들을 설치합니다.

```shell
$ virtualenv env
$ source env/bin/activate
(env) $ pip install Flask
(env) $ pip install Flask-WTF
```

맨 밑의 Flask-WTF 패키지[^Flask-WTF] 같은 경우는 사용하지 않아도 상관없습니다. 폼을 조금 더 잘 관리하도록 도와주는 패키지입니다.

## 예제 작성

### 기본적인 뼈대

```
.
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   └── forms.py
│   ├── static
│   └── templates
│       ├── auth
│       │   ├── signin.html
│       │   └── success.html
│       └── index.html
├── tests
│   └── test.py
├── requirements.txt
├── run.py
├── setup.py
├── MANIFEST.in
└── README.md
```

기본적인 파일 구조는 다음과 같이 이루어질 예정입니다.

`static`은 폴더이지만, 내부에 아무런 파일이 없어서 마치 파일처럼 보입니다.

파일 구조에 대해 설명을 드리자면, `app` 폴더는 웹 페이지의 소스코드입니다. 3페이지로 이루어져 있으며, 밑의 3 페이지입니다.

![index.html 화면]({{ site.url }}/images/2017/08-30-ci-example-with-flask/index.png)
index.html 화면

![auth/signin.html 화면]({{ site.url }}/images/2017/08-30-ci-example-with-flask/auth.signin.png)
signin.html 화면

![auth/sucess.html 화면]({{ site.url }}/images/2017/08-30-ci-example-with-flask/auth.success.png)
success.html 화면

index.html은 signin.html로 넘어가는 링크 하나가 있습니다. signin.html은 이메일과 이름을 입력하는 입력칸 두개가 있고요, success.html은 signin.html에서 입력한 이메일과 이름을 **validating** 후 보여주는 화면이 있습니다.

**validating**하는 것이 중요한데, test code를 작성하기 위해 일부러 넣은 기능이기 때문입니다.

### 예제 작성

예제는 위에서 본 뼈대를 기반으로 간단하게 작성하겠습니다.

밑에 나오는 코드들은 전부 이 저장소에 저장되어 있는 코드들입니다.

* app/\_\_init__.py

```python
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.TestingConfig')

    from .auth import auth_page
    app.register_blueprint(auth_page, url_prefix='/auth')

    @app.route('/')
    def index_page():
        return render_template('index.html')

    return app
```

테스트 할 때 flask app 오브젝트에 접근하기 쉽도록 `create_app`이라는 함수를 만들어 반환값으로 app을 반환하도록 했습니다.

* app/config.py

```python
class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SECRET_KEY = "random secret key"
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    SECRET_KEY = "random secret key for test"
    TESTING = True
```

config.py에서 `ProductionConfig`는 작성하지 않았는데, 그 이유는 큰 이유가 있는 것이 아니고 단순히 귀찮아서... 입니다.

* app/auth/\_\_init__.py

```python
from .controller import auth_page
```

이 파일은 큰 의미없이, `from .auth import auth_page` 처럼 쓸 수 있도록 하려고 만든 파일입니다.

* app/auth/controller.py

```python
from flask import Blueprint, render_template, request, url_for, redirect

from .forms import SignInForm

auth_page = Blueprint('auth_page', __name__)

@auth_page.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm(request.form)

    if form.validate_on_submit():
        return redirect(url_for('.success', email=form.email.data, name=form.name.data))

    return render_template('auth/signin.html', form=form)

@auth_page.route('/success', methods=['GET'])
def success():
    email = request.args.get('email')
    name = request.args.get('name')

    if email and name:
        return render_template('auth/success.html', data={
            'email': email,
            'name' : name
        })
    else:
        return "bad request"
```

`auth_page`라는 Blueprint를 만들어서, `signin`과 `success`에 라우트를 추가했습니다. `def signin()`에서 나오는 `form.validate_on_submit()`는 email 형식과 이름 형식을 체크합니다. 만약 올바르지 않으면, 다시 signin.html 페이지가 나오고, 올바른 형식이라면 success.html로 넘어가는 형식입니다. `def success()`는 email과 name을 받아서 존재한다면 success.html을 보여주고 아니라면 'bad request'라는 응답을 반환하는 뷰 함수입니다.

`from .forms import SignInForm`에서 import하는 forms는 다음에 나오는 파일입니다.

* app/auth/forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class SignInForm(FlaskForm):
    email = StringField('Email Field', [Email(), DataRequired(message='Must provide an email.')])
    name = StringField('Name Field', [DataRequired(message='Must provide a name')])
```

여기서 Sign In 필드의 형식을 정의하는데, 이메일과 이름을 받을 것이라 Email Field, Name Field 두 개를 만들었습니다. 그 다음에는 입력값을 검증하기 위해 이메일 필드에는 `Email()`이라는 Validator와 `DataRequired`라는 Validator를 넣었습니다. 이름 필드에는 `DataRequired`라는 Validator만을 넣었습니다.

나머지는 html 템플릿을 작성하는 부분이라 그 부분을 제외하였습니다.

### 서버 구동해보기

* run.py

```python
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
```

이 코드를 추가한 후 다음과 같이 구동하시면 됩니다.

```shell
(env) $ python run.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * ...
 * ...
```

위와 같은 출력값을 보실 수 있으실 겁니다.

## 테스트 코드 작성

테스트 코드는 간단하게 두 개의 테스트를 작성하였습니다. 또한 테스트를 위해 파이썬에 기본적으로 내장된 unittest를 이용하였습니다.

```python
import unittest
from app import create_app

class CIExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        assert 'Sign In' in rv.data.decode('utf8')

    def test_login(self):
        rv = self.app.post('/auth/signin', data=dict(
            name='jeongukjae',
            email='jeongukjae@gmail.com'
        ), follow_redirects=True)

        assert 'You were logged in' in rv.data.decode('utf-8')

if __name__ == '__main__':
    unittest.main()
```

`setUp`과 `tearDown`은 테스트를 시작하고 종료할 때 실행되는 함수이므로, 지금은 크게 신경쓰실 필요는 없습니다. 밑의 test_로 시작하는 두 개의 함수에 주목하시면 됩니다. 이 두개의 함수가 테스트를 진행하는 함수로, 각각 '/'를 잘 받아오는지, signin의 post method가 잘 작동하는 지 체크하는 테스트입니다.

## setup.py 설정

* setup.py

```python
from setuptools import setup, find_packages

setup(
    name='Flask-CI-Example',
    packages=find_packages(),
    version='0.1',
    long_description=__doc__,
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'Flask==0.12.2',
        'Flask-WTF==0.14.2',
        'itsdangerous==0.24',
        'Jinja2==2.9.6',
        'MarkupSafe==1.0',
        'Werkzeug==0.12.2',
        'WTForms==2.1',
    ],
    tests_require=['nose'],
)
```

이 setup.py를 통해 travis ci에서의 테스트와 coveralls의 code coverage 측정을 진행합니다. 이 setup.py에서 주목해야 할 부분은 `test_suite`, `install_requires`, `tests_require` 이 세부분입니다. `test_suite`는 어떤 것으로 테스트를 진행할 지 알려주는 것입니다. `install_requires`는 디펜던시를 지정하는 것이고, 저는 `pip freeze` 명령어를 이용하여 작성하였습니다. `test_require`는 테스트를 진행하는 데 필요한 패키지들을 작성하는 것입니다.

* MANIFEST.in

```
recursive-include app/templates *
recursive-include app/static *
```

이 부분은 `app/templates` 폴더와 `app/static` 폴더를 `setup.py`를 실행하여도 포함하도록 하는 설정파일입니다.

## Travis-CI 설정하기

### travis-ci.org

[travis-ci.org](http://travis-ci.org)[^TrvisCI]에서 GitHub 계정을 이용하여 가입하신 후, repository를 이름 왼쪽의 스위치 버튼을 켜시면 해당 레포지토리에 대해 travis-ci 설정이 됩니다.

![Travis CI]({{ site.url }}/images/2017/08-30-ci-example-with-flask/travis-ci.png)

저는 이 레포지토리를 Travis CI에 추가하기 위해 이 레포지토리에 해당하는 스위치 버튼을 켰습니다.

그리고 이 레포지토리에 .travis.yml 파일을 추가해주면 모든 설정이 완료됩니다.

### .travis.yml

```yml
sudo: false
language: python
python:
  - "3.6"

install:
  - pip install coveralls

script:
  - coverage run --source=app setup.py test

after_success:
  - coveralls
```

저는 python 3.6 버전으로 테스트를 진행하였습니다. (버전은 하나를 선택할 수도 있고, 여러가지를 선택할 수도 있습니다) 테스트를 진행하기 전 `coveralls`를 설치합니다. `coveralls`는 code coverage를 측정하는 도구의 파이썬 패키지인데, python-coveralls와 coveralls-python이 있습니다. coveralls 패키지를 설치하면 coverage 명령어를 실행할 수 있습니다.

script 부분에 대해서는 [coveralls-clients/coveralls-python](https://github.com/coveralls-clients/coveralls-python) 레포지토리에 설명되어 있습니다. `coveralls` 명령어를 실행하면 coveralls.io에 데이터가 전달됩니다.

어쩄든 이렇게 해두고 푸쉬하시면 travis ci가 열심히 돌아갑니다. 근데, coveralls에 관련된 부분이 설정되지 않았기 때문에 테스트가 통과되어도 code coverage를 보실 수는 없으실 겁니다.

## Coveralls

### Coveralls 웹 페이지

[coveralls 웹 페이지](https://coveralls.io/)[^coveralls]로 가서 GitHub 계정으로 가입한다면 다음과 같은 화면을 볼 수 있습니다.

![coveralls 화면]({{ site.url }}/images/2017/08-30-ci-example-with-flask/coveralls.png)

coveralls도 똑같이 repo들을 스위치 방식으로 키고 끄는데, 이 중 원하는 repo를 키고 난 후 Token을 받습니다. 그리고 해당 Token을 Travis CI에 설정해주어야 합니다.

 이 토큰을 설정하는 방법은 따로 설정 파일을 만들어서 설정하는 방법, 환경변수로 설정하는 방법이 있는데, 지금 이 예제는 public repo로 만들었으니, 환경변수로 넣어줘야 받은 token을 나만 알수 있도록 관리할 수 있습니다. 만약 파일로 만들어 저장한다면, 해당 repo가 public이므로, 누구든지 파일을 볼 수 있으니 더 이상 비밀 토큰이 아니게 됩니다. 공식문서에는 이 토큰을 비밀로 유지하라고 써져 있습니다.

### Travis CI에 설정

![travis ci 환경변수]({{ site.url }}/images/2017/08-30-ci-example-with-flask/travis-ci-env.png)

그렇게 받은 토큰을 travis ci 환경변수에 설정합니다.

환경변수 이름은 ```COVERALLS_REPO_TOKEN```로 하고, 값은 coveralls에서 받은 값으로 합니다.

## 마무리

### 뱃지 달기

[![Coverage Status](https://coveralls.io/repos/github/JeongUkJae/Continuous-Integration-Example-with-Flask/badge.svg?branch=master)](https://coveralls.io/github/JeongUkJae/Continuous-Integration-Example-with-Flask?branch=master) [![Build Status](https://travis-ci.org/JeongUkJae/Flask-JWT-Login.svg?branch=master)](https://travis-ci.org/JeongUkJae/Flask-JWT-Login)

위처럼 다른 오픈소스 프로젝트에 상단에 있는 것과 같이 뱃지를 달아봅시다.

![Coveralls Badge]({{ site.url }}/images/2017/08-30-ci-example-with-flask/coveralls.badge.png)

Coveralls에서는 레포지토리 세팅에서 Badge 옆에 Embed라는 버튼이 존재합니다. 해당 버튼을 누르면 마크다운 문법으로 바로 뱃지를 보여줍니다.

![TravisCI Badge]({{ site.url }}/images/2017/08-30-ci-example-with-flask/travis-ci.badge.png)

Travis CI에서는 바로 보이는 Badge를 클릭하면 Markdown으로 표기 가능하도록 변환해줍니다.

위의 두 가지 뱃지를 자신의 레포지토리 `README.md` 상단에 넣어주면 됩니다.

## 끝

이제 적당히 코드를 수정해서 푸쉬해봅시다. 이제 테스트가 잘 돌아갈 것이고, PR에 대해서도 미리 테스트가 돌아갈 것입니다. 물론 Code Coverage는 덤이고요.

### 참고자료

[^Flask-WTF]: https://flask-wtf.readthedocs.io Flask와 WTForms를 결합해놓은 패키지이다.
[^TrvisCI]: https://travis-ci.org 오픈소스를 위해 CI 서비스를 제공한다.
[^coveralls]: https://coveralls.io 오픈소스에게는 무료인 커버리지 관련 툴이다. 파일별로 커버리지를 보여준다.
