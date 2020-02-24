---
layout: post
title: 핑퐁팀의 Python 문화 구축기
tags:
  - python
  - scatterlab
---

**[핑퐁팀 블로그](https://blog.pingpong.us/python-in-pingpong/)에 올라간 글입니다. 직접 작성한 글이라 여기에 재 업로드합니다.**

---

*본격 Python 문화 바로잡기*

핑퐁팀은 머신러닝 모델 실험 코드부터 프로덕션에 이르기까지 Python을 많이 사용합니다. 하나의 프로젝트는 여러 명의 협업으로 진행되기 때문에 그 특성상 스타일, 구조의 불일치로 많은 문제를 겪을 수 밖에 없습니다. 이 문제를 핑퐁팀이 어떻게 해결해나갔는지 소개합니다.

## 목차

- [시작은 가볍게, 코드 품질 관리 도구](#시작은-가볍게-코드-품질-관리-도구)
  - [Style Checker, Code Formatter](#style-checker-code-formatter)
  - [Type Checker](#type-checker)
- [관리는 확실하게, CI와 테스트 코드](#관리는-확실하게-ci와-테스트-코드)
  - [CI](#ci)
  - [테스트 코드](#테스트-코드)
    - [CI에서의 pytest](#ci에서의-pytest)
    - [Code Coverage](#code-coverage)
    - [병렬 실행](#병렬-실행)
    - [Python 버전별 실행](#python-버전별-실행)
  - [초기 템플릿 생성](#초기-템플릿-생성)
- [후기](#후기)
- [참고](#참고)

## 시작은 가볍게, 코드 품질 관리 도구

코드의 많은 부분이 구조적으로 일치하지 않는 상황에서 가장 먼저 고려한 것은 **각 팀원들이 손쉽게 사용할 수 있는 도구**를 도입하는 것이었습니다.
예를 들어 GitHub을 활용한 협업 과정에 대한 이해가 필요한 CI 개념이나 설정을 먼저 다루기보다, `black`, `yapf`와 같이 빠르게 명령어 하나로 적용 가능한 도구를 먼저 소개하는 것이 더 좋은 방법이라고 생각했습니다.

### Style Checker, Code Formatter

그래서 코드 스타일 체크와 포맷 자동화를 위한 도구들의 후보를 몇 가지 뽑았습니다.
저희는 그 중 black, flake8, yapf 등의 도구를 빠르게 적용해 볼 수 있다고 생각했습니다. 다음은 각 도구에 대한 간략한 설명입니다.

* black

  Python Software Foundation에서 작성한 Python 자동 포맷팅 도구입니다.

* flake8

  Python Code Quality Authority (PyCQA)에서 작성한 스타일 체크 도구로, 플러그인을 붙이기 쉬운 것이 장점입니다.

* yapf

  구글에서 배포하는 자동 포맷팅 도구입니다.
  다른 포맷팅 도구들이 스타일 가이드를 어긴 부분만 잡아준다면, yapf는 스타일 가이드를 어기지 않았더라도 다시 포맷팅을 진행하는 상당히 엄격한 자동 포맷팅 도구입니다.

이 중 yapf는 스타일 가이드를 어기지 않았더라도 다시 포맷팅을 진행하여 좋은 생김새의 코드를 만들겠다는 철학을 지니고 있었고, 시험적으로 도입해보았더니 (~~엄청나게...🤦~~) 많은 설정 값들을 가지고 있었습니다.
설정할 값이 많으면 코드 스타일을 자세하게 관리할 수 있다는 장점이 있지만, 사용하기에 따라 생김새가 각기 다른 코드들이 나올 수 있다는 문제가 있었습니다.
그에 비해 black은 설정 가능한 옵션이 Python Version과 Line Length뿐일 정도로 적기 때문에 같은 도구를 사용한다면 생김새가 다른 코드가 나올 확률이 매우 적었죠.
따라서 누구나 최소한의 설정만으로 핑퐁팀의 코드 스타일을 똑같이 만들어낼 수 있었고, 그 결과 black을 도입하게 되었습니다.

{% include image.html url="/images/2020-02-12-python-in-pingpong/f1.png" alt="Auto Formatting is the new black" description="PyCon Cleveland 2019에 나온 발표 자료. black 적용 당시의 핑퐁팀의 마음을 잘 대변해줍니다." %}

black을 적용한 후, docstring 형식과 같이 black이 잡지 못하는 부분을 잡아내기 위해 flake8도 적용해보기로 하였습니다.
flake8은 flake8-bugbear, flake8-rst와 같은 수많은 플러그인이 존재하고 적용하기에도 간편하기 때문에 기능 확장성이 매우 뛰어난 도구입니다.
하지만 flake8과 black이 종종 충돌이 일어났는데, 그런 경우는 [black 문서](https://github.com/psf/black#line-length)대로 해결했습니다.

black과 flake8으로 전반적인 코드 생김새는 다 잡혔는데, Python 생태계에서는 Java의 checkstyle이나 Typescript의 Prettier처럼 import statement의 스타일까지 체크해주는 도구를 찾기 어려웠습니다.
그래서 관련된 도구를 찾아보니 isort라는 도구를 발견했습니다.

{% include image.html url="https://github.com/timothycrosley/isort/raw/a92ab4b67f5f78a26a247fe979da153fa7674ddb/example.gif" alt="isort 예시" description="isort 예시" %}

주 기능은 이름처럼 import statement를 정렬하는 도구입니다.
하지만 도입 후에 살펴보니, import statement를 잘 정렬하는 것뿐만이 아니라 standard library, third party, first party를 나누어 정렬해주기 때문에 어떤 라이브러리를 사용하고 import 하는지 파악하기 더 편해지는 효과가 있었습니다.

그래서 핑퐁팀은 black, flake8 (과 여러 가지 플러그인), isort를 사용하고 있습니다.

### Type Checker

핑퐁팀은 Python을 사용할 때 안정성을 위해서 Type Hints를 자주 사용합니다. ([Type Hints가 무엇인가요?](https://www.python.org/dev/peps/pep-0484/))
하지만, 정작 Type Checking을 위한 도구를 사용하고 있진 않았습니다.
그래서 Formatter를 적용할 때처럼 쉽게 적용할 수 있는 도구를 정리해보았습니다. 아래는 그 목록입니다.

* mypy

  Python에서 개발하는 공식 Type Checker입니다.

* pyright

  Microsoft에서 개발하는 Type Checker로, Typescript로 작성되었습니다.
  Visual Studio Code와 직접 연동됩니다.

* pyre-check

  Facebook에서 개발한 Type Checker입니다.

이 중 가장 먼저 도입한 도구는 pyre-check이었습니다.
Pyre는 F8 2019에서 진행된 "Facebook Loves Python and Python Loves Facebook" 발표의 "Types at Scale" 챕터에서 처음 발표되었으며, Instagram처럼 대규모 코드 베이스에서의 Type Checking을 위한 도구라고 소개되었습니다.
스캐터랩에는 쌓인 Python 코드가 많았고, 모노레포 형식으로 사용하고 있는 프로젝트도 존재했기 때문에 Pyre를 적용하는 것이 좋겠다고 생각했습니다.

하지만 Pyre는 IDE Integration 부분에서 부족한 점이 많아 교체를 고민하던 중 pyright의 1.0.0 릴리즈가 발표되어 pyright로 교체하게 되었습니다.
[Visual Studio Code와의 연동](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright)도 강력하게 지원해서, Visual Studio Code를 많이 사용하는 핑퐁팀에서 사용하지 않을 이유가 정말 1도 없었죠. 🥴

하지만, Python은 그 특성상 모든 코드에 타입을 명시하긴 힘듭니다.
타입을 명시하자는 커뮤니티가 Typescript처럼 굉장히 크지 않기도 하고, 아직 코드에 타입을 명확하게 정의하고 있지 않은 라이브러리가 많습니다.
그래서 핑퐁팀은 [pyright의 strict 옵션](https://github.com/microsoft/pyright/blob/master/docs/configuration.md#master-pyright-config-options)은 사용하지 않고 있고, 일부 사용 가능한 옵션만을 설정하여 사용하는 중입니다.

{% include image.html url="/images/2020-02-12-python-in-pingpong/f3.png" alt="한없이 부러워지는 DefinitelyTyped 😭" description="한없이 부러워지는 DefinitelyTyped 😭" %}

## 관리는 확실하게, CI와 테스트 코드

팀원들이 코드 품질 관리 도구들에 익숙해질 쯤에, 코드의 무결성을 위해서 간혹 작성해오던 테스트 코드를 팀 내 문화로 정착시키고 더욱 완벽하게 코드를 관리할 수 있게 하면 좋겠다는 생각을 했습니다.
그래서 가장 기본적인 규칙인 **"Git에 올라가는 코드들은 잘 동작하는 코드여야 한다"**를 기틀로 잡고, 이 목표를 이룰 수 있도록 도와줄 도구들을 세팅하기 시작했습니다.

### CI

핑퐁팀에서는 CI를 2019년부터 적극적으로 도입하기 시작했습니다.
선택지는 여러 가지가 있었지만, GitHub을 주된 Git 플랫폼으로 가져가면서 Private을 강력하게 지원하는 도구들은 한정되어 있었죠.
그래서 핑퐁팀은 아래와 같은 CI 서비스를 이용하고 있습니다.

* CircleCI
* Jenkins Blueocean
* GitHub Actions

CircleCI는 Private Repository를 위한 가장 강력한 CI 서비스 중 하나입니다.
Parallelism, Cache 기능, Orb, 단순한 설정 파일, 권한 관리, Coveralls 같은 각종 도구의 편리한 통합까지 우리가 원하는 기능을 대부분 지원하고 있습니다.
하지만 Pull Request 작성 시 트리거를 주는 기능과 같이 사소하지만 있으면 굉장히 좋은 몇 가지의 기능을 지원하지 않죠.
그래서 핑퐁팀은 CircleCI를 주 CI 서버로 활용하고 있고, GitHub Actions는 일부 기능을 처리하기 위해 상대적으로 드물게 활용하고 있습니다.

추가로, 머신러닝이 주가 되는 핑퐁팀의 특성 상 데이터를 이용한 테스트가 필요해질 때가 많습니다.
따라서 그런 경우에만 예외적으로 내부 서버에 Jenkins Blueocean을 구축하여 사용하고 있습니다.
한편으로는 올해 초 GitHub Actions Self Hosted Runner가 오픈소스화 된 만큼 Jenkins 대신 GitHub Actions를 이용한 CI 세팅을 시도하고 있습니다.

위 설명을 읽으시면 아래처럼 생각하실 수도 있습니다.

> *"CircleCI없이 GitHub Actions만 사용하면 되지 않을까?"*

머신러닝이 주가 되는 프로젝트는 TensorFlow, PyTorch 등등의 큰 라이브러리를 필수적으로 설치해야 해서 캐시 파일 용량이 어마어마해지기 때문(😰)...도 있고, CI에서 사용하는 도구의 통합이나 SSH를 통한 디버깅 같은 편리한 기능 지원이 아직은 미흡하기 때문에 GitHub Actions만으로는 부족함이 있어 CircleCI를 계속해서 사용하는 중입니다.

지금의 핑퐁팀이 Pull Request를 보낼 때는 다음의 세 가지 요소가 CI에서 확인됩니다.

* 모든 테스트 코드가 통과함
* 코드 품질 관리 기준을 만족함 (Code Formatting, Style Checking, ...)
* 팀 내 Git Convention을 지킴

### 테스트 코드

믿을 수 있는 코드라고 말하려면 역시 테스트 케이스가 잘 작성된 코드여야겠죠? 😊
핑퐁팀 안에서도 좋은 테스트 케이스를 작성하기 위해 노력하고 있지만, 이 글에서는 어떤 식으로 사용하는지만 간단하게 언급해보겠습니다.

Python 코드를 테스트하기 위한 도구로 pytest와 unittest 정도를 들 수 있습니다.
unittest는 Python의 기본 라이브러리이고, 테스트 코드를 작성하기 충분한 기능을 제공합니다.
fixture 등의 기능도 pytest보다 훨씬 Pythonic하게 사용이 가능합니다.
하지만 pytest는 테스트 코드 자체를 간결하게 만들고 Parameterized Test도 훨씬 간편하도록 해줍니다.
더군다나 다른 플러그인을 붙이기에도 간편하죠.

unittest나 pytest 중 하나만을 사용하기로 합의하진 않았지만, 핑퐁 팀 내부에서는 간결함 때문에 자연스럽게 pytest를 주로 사용하는 중입니다.
핑퐁팀은 pytest를 어떻게 사용하는지 더 자세하게 알려드릴게요!

#### CI에서의 pytest

CI에서 실행하는 명령은 어떤 행동이 일어났는지 정확히 알아야 하기 때문에 기본적으로 Verbose 옵션(`-v`)을 주고 있습니다.
테스트 실행도 예외가 아니죠.

또한 어떤 테스트를 건너뛰었고 어떤 테스트가 실패했는지 한눈에 보기 위해 마지막에 Summary를 출력하도록 옵션(`-ra`)을 주고 있습니다.
이 옵션의 의미는 pytest 문서의 [Detailed summary report](https://docs.pytest.org/en/latest/usage.html#detailed-summary-report)를 살펴보시면 좋습니다.

하지만, 테스트가 실패했을 때 어떤 상황에 실패했는지 정확히 모른다면, 실패한 이유과 실패하기까지의 과정을 명확히 알 수 없습니다.
그래서 로컬 변수들을 출력하도록 옵션(`-l`)을 주어 사용하고 있습니다.
이 옵션 역시 pytest 문서의 [Modifying Python traceback printing](https://docs.pytest.org/en/latest/usage.html#modifying-python-traceback-printing)을 살펴보시는 것을 추천드립니다.

#### Code Coverage

Code Coverage는 테스트 코드 작성할 때 참고하기 좋은 지표 중 하나입니다.
어떤 코드에 더 테스트가 필요한지, 혹은 특정 Branch에 있는 코드에 테스트가 충분히 이루어졌는지 확인하기 위한 지표가 될 수 있습니다.
그렇기에 핑퐁팀도 Code Coverage를 최대한 측정하려고 하고 있으며, 이를 위해 사용하는 것이 pytest-cov입니다.
pytest-cov와 함께 pytest를 실행하게 되면 Coverage Report가 함께 생성됩니다.
해당 Report가 Coveralls, CodeCov와 같은 서비스에 업로드되면 어떤 코드를 더 테스트해야 하는지, 최근 Code Coverage 추이는 어떤지 등을 웹 상에서 손쉽게 확인할 수 있습니다.

#### 병렬 실행

테스트 케이스가 많아지는 경우 병렬 실행이 필요해지는 시점이 있습니다.
이럴 때 pytest를 쉽게 병렬화할 수 있는 방법은 pytest-xdist 플러그인을 사용하는 것입니다.
CPU 코어 개수에 알맞게 Worker 수를 설정하고 나면 자동으로 병렬로 실행되게 됩니다.
하지만, 전체 실행 시간 자체가 그렇게 길지 않거나 테스트가 독립적이지 않으면 오버헤드 때문에 오히려 실행 시간이 길어지기도 하니 적절한 상황에만 사용하는 것을 추천드립니다.

#### Python 버전별 실행

때로는 다양한 Python 버전에서 사용할 도구를 작성해야 하는 상황이 있습니다.
핑퐁팀은 그러한 도구를 테스트하기 위해 tox를 사용하고 있습니다.
tox는 `tox.ini` 파일 하나를 추가하는 것만으로 손쉽게 여러 가지 버전의 Python에서 테스트를 하도록 해주죠.
심지어 대부분의 경우에는 기존 테스트 과정을 고칠 필요도 없는 것이 장점입니다.

### 초기 템플릿 생성

위의 사항들을 아무리 잘 정해놓아도 새로운 프로젝트를 생성할 때 하나라도 빠뜨린다면.... 🤭
그래서 핑퐁팀에서는 템플릿을 통해 프로젝트를 생성하도록 하고 있습니다.

{% include image.html url="/images/2020-02-12-python-in-pingpong/f2.png" alt="템플릿 레포지토리는 엄청 편해요 🥳" description="템플릿 레포지토리는 엄청 편해요 🥳" %}

GitHub Template Repository를 구성해서 사용할 수도 있고, Cookiecutter를 통해 구성할 수도 있습니다.
하지만 핑퐁팀에서는 기존에 템플릿 레포지토리들이 존재했기 때문에 GitHub Template Repository를 사용하게 되었습니다.
해당 템플릿 레포지토리에는 CI, 테스트, 포맷팅 도구 등등을 미리 세팅해놓아서 생성 후 몇 가지만 고치면 바로 사용이 가능합니다.

## 후기

**정욱재 (ML Software Engineer)**

평소에 코드 품질을 너무나도 중요시 여겨 팀 내에서 욱킨스라는 별명까지 있을 정도지만, 팀 전체가 품질 하나를 두고 움직인 것은 처음 겪어보는 일이에요.
이렇게 맞추어진 규약을 지키는 것이 누군가에게는 기본적일 수도 있지만 팀 전체가 같이 해내기란 어려운 일이란 것을 알았습니다.
그리고 이런 과정을 거칠수록 언어 자체에 대한 이해도 더 많이 할 수 있는 것 같아요.
Python 친화적인 핑퐁팀이 되기까지! 👊👊

**홍승환 (ML Software Engineer)**

회사 안에서 사용할 개발 가이드를 작성하며 Python 생태계에서 코드 품질 관리를 위해 사용할 수 있는 여러가지 도구들을 둘러보았습니다.
처음에는 팀 내에서 사용하는 코드들의 품질을 개선하기 위해서 시작한 프로젝트였는데, 점점 그 규모가 커지더니 회사 전체에서 그 가이드를 사용하게 되었어요!
앞으로도 핑퐁팀은 높은 기준의 코드 품질을 지켜나가기 위해서 많은 노력들을 할 예정입니다.
지켜봐주세요 😉

## 참고

* 각 명령어 도구
  * [GitHub - psf/black](https://github.com/psf/black)
  * [GitHub - timothycrosley/isort](https://github.com/timothycrosley/isort)
  * [GitLab - PyCQA/flake8](https://gitlab.com/pycqa/flake8)
  * [GitHub - google/yapf](https://github.com/google/yapf)
  * [GitHub - python/mypy](https://github.com/python/mypy)
  * [GitHub - microsoft/pyright](https://github.com/microsoft/pyright)
  * [GitHub - facebook/pyre-check](https://github.com/facebook/pyre-check)
  * [GitHub - pytest-dev/pytest](https://github.com/pytest-dev/pytest)
  * [GitHub - tox-dev/tox](https://github.com/tox-dev/tox)
  * [GitHub - cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
* 참고한 컨퍼런스, 세미나 자료
  * [F8 2019: Facebook Loves Python and Python Loves Facebook](https://www.youtube.com/watch?v=O3q7A2ruzxA)
  * [PyCon 2019: Life Is Better Painted Black, or: How to Stop Worrying and Embrace Auto-Formatting](https://www.youtube.com/watch?v=esZLCuWs_2Y)
