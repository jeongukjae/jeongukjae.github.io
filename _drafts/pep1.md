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

### PEP를 읽는 사람들

그럼 누가 이 PEP문서를 읽을까? 주로 이 PEP문서를 읽는, 읽어야 하는 사람은 CPython 코어 개발자, 코어 개발자들이 선출한 Steering Council, 그리고 CPython이 아닌 다른 Python 구현체를 만드는 사람들이다. 그 외에도 Python 커뮤니티에서 Informatinal PEP와 같은 형태로 앞으로의 API Convention이나, 복잡한 설계를 합의하기 위해 사용할 수도 있다.

### PEP의 종류

PEP는 세가지 종류가 있다.

* **Standards Track PEP**는 새로운 기능 혹은 구현을 설명하기 위한 PEP문서이다. 이후에 표준 라이브러리로 추가될 기능이지만 현재는 서드파티로 지원되는 기능에 대한 interoperability를 기술할 수도 있다.
* **Informational PEP**는 Python의 설계 이슈 혹은 일반적인 가이드와 정보를 Python 커뮤니티에 전달하기 위해 작성하는 PEP문서이다. 하지만 사용자와 Python 개발자는 꼭 이 PEP문서를 따를 필요는 없고, 조언 정도로 생각하면 된다.
* **Process PEP**는 Python과 관련된 프로세스를 기술하거나, 해당 프로세스에 대한 변경을 제안하는 PEP문서이다. Standards Track PEP와 비슷하게 보일 수 있지만, 이 PEP 문서는 Python언어 그 자체에 대한 것은 아니다. 하지만 이 문서는 Informational PEP와는 다르게 커뮤니티의 합의가 필요한 문서이다. 즉, 사용자는 이 Process PEP를 마냥 무시할 수 있는 것이 아니다. [Meta-PEP](https://www.python.org/dev/peps/#meta-peps-peps-about-peps-or-processes)의 목록이 Process PEP에 속한다.
