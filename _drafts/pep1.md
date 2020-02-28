---
layout: post
title: PEP(Python Enhancement Proposal)란 무엇일까
tags:
  - python
---

PEP와 숫자로 이루어진 수많은 python proposal이 존재하지만, 그 많은 proposal들은 어떤 기준으로 읽어야 하고, 판단을 해야 할까? 어떤 proposal을 읽어야 하고 어떤 proposal을 읽지 않아도 될까? 이런 질문에 대한 답을 공교롭게도 [PEP의 1번 문서](https://www.python.org/dev/peps/pep-0001/)가 설명해준다.

## PEP가 뭘까

PEP가 뭔지 위해 [PEP의 1번 문서](https://www.python.org/dev/peps/pep-0001/)를 살펴보면 가장 첫 소제목으로 나와있다. 해당 섹션의 첫번째 문단을 가져와보자.

> PEP stands for Python Enhancement Proposal. A PEP is a design document providing information to the Python community, or describing a new feature for Python or its processes or environment. The PEP should provide a concise technical specification of the feature and a rationale for the feature.

즉, Python Enhancement Proposal의 약어로, Python 커뮤니티로의 정보전달을 위한 일종의 설계 문서가 될 수도 있고, 파이썬의 새로운 기능을 설명하는  문서가 될 수도 있다. 따라서 PEP는 정확한 기술적인 명세가 들어가야하고 그 기능이 필요한 이유 또한 필요하다. 또한 PEP 문서는 텍스트 파일로 관리하므로, [versioned repository](https://github.com/python/peps), 즉 GitHub에 저장된다.

## PEP를 읽는 사람들

그럼 누가 이 PEP문서를 읽을까? 주로 이 PEP문서를 읽는, 읽어야 하는 사람은 CPython 코어 개발자, 코어 개발자들이 선출한 Steering Council, 그리고 CPython이 아닌 다른 Python 구현체를 만드는 사람들이다. 그 외에도 Python 커뮤니티에서 Informatinal PEP와 같은 형태로 앞으로의 API Convention이나, 복잡한 설계를 합의하기 위해 사용할 수도 있다.

## PEP의 종류

PEP는 세가지 종류가 있다.

* **Standards Track PEP**는 새로운 기능 혹은 구현을 설명하기 위한 PEP문서이다. 이후에 표준 라이브러리로 추가될 기능이지만 현재는 서드파티로 지원되는 기능에 대한 interoperability를 기술할 수도 있다.
* **Informational PEP**는 Python의 설계 이슈 혹은 일반적인 가이드와 정보를 Python 커뮤니티에 전달하기 위해 작성하는 PEP문서이다. 하지만 사용자와 Python 개발자는 꼭 이 PEP문서를 따를 필요는 없고, 조언 정도로 생각하면 된다.
* **Process PEP**는 Python과 관련된 프로세스를 기술하거나, 해당 프로세스에 대한 변경을 제안하는 PEP문서이다. Standards Track PEP와 비슷하게 보일 수 있지만, 이 PEP 문서는 Python언어 그 자체에 대한 것은 아니다. 하지만 이 문서는 Informational PEP와는 다르게 커뮤니티의 합의가 필요한 문서이다. 즉, 사용자는 이 Process PEP를 마냥 무시할 수 있는 것이 아니다. [Meta-PEP](https://www.python.org/dev/peps/#meta-peps-peps-about-peps-or-processes)의 목록이 Process PEP에 속한다.

## PEP는 어떻게 만들어질까

### Python's Steering Council

PEP가 최종적으로 accept 될 지, reject 될 지 정하는 사람들이다. [PEP 13](https://www.python.org/dev/peps/pep-0013/)에 자세히 설명되어 있다.

### Python's Core Developers

Python's Core Developers는 Python core team 멤버들을 말하며, 이들 역시 [PEP 13](https://www.python.org/dev/peps/pep-0013/)에 자세히 설명되어 있다.

### Python's BDFL

BDFL은 Benevolent dictator for life를 말하며 한국어로는 대부분 "자비로운 종신 독재자"정도로 번역되었다. 그 유명한 파이썬의 창시자인 Guido van Rossum을 일컫는 말이 맞지만, Guido van Rossum은 [PEP 572](https://www.python.org/dev/peps/pep-0572/)가 끝나면서 [BDFL에서 물러났으므로](https://mail.python.org/pipermail/python-committers/2018-July/005664.html) BDFL-Delegate는 historical reference 정도이다.

### PEP Editors

PEP Editor들은 PEP 숫자를 지정하거나 PEP status를 바꾸는 등의 PEP Workflow에 대해서 책임이 있는 사람이다. editorship은 editor들의 초대로 이루어진다.

### Start with an idea for Python

위는 PEP 수정, 작성에 참여하는 사람, 조직들이고, 이제서야 PEP 작성에 대한 내용이 시작한다.

PEP 작성은 Python에 대한 새로운 아이디어로부터 시작하며, Single key proposal이나 new idea만을 포함하길 추천한다고 한다. 엄청 작은 enhancement들은 PEP로 작성할 필요가 없으며 [Python Issue Tracker](https://bugs.python.org)만으로도 충분하다고 한다. 만약 작성한 PEP가 너무 광범위하거나 제대로 기술되지 않는다면 PEP Editor들은 이를 reject할 수도 있다.

각 PEP는 Champion이 필요하다. 지금부터 설명할 스타일과 포맷으로 PEP를 작성하고, 적절하게 토론이 이루어지도록 유도하며, 아이디어를 커뮤니티에서 잘 합의하도록 하는 사람이 Champion(a.k.a. Author)이다.
