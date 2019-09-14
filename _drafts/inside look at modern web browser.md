---
layout: post
title: 🕸 Inside Look at Modern Web Browser
tags:
  - web
---

[Google Developers - Web](https://developers.google.com/web/updates/)에 올라온 4편짜리 시리즈 블로그 포스트이다. 원문은 아래 링크들에 있고, 좋은 내용이라 생각해서 4편을 읽으면서 다시 볼 것 같은 내용만 정리한다. (너무 아는데 정리하기 귀찮으면 건너 뛸꺼야..)

- [Inside Look at Modern Web Browser 1](https://developers.google.com/web/updates/2018/09/inside-browser-part1)
- [Inside Look at Modern Web Browser 2](https://developers.google.com/web/updates/2018/09/inside-browser-part2)
- [Inside Look at Modern Web Browser 3](https://developers.google.com/web/updates/2018/09/inside-browser-part3)
- [Inside Look at Modern Web Browser 4](https://developers.google.com/web/updates/2018/09/inside-browser-part4)

간략한 내용은 Chrome Browser에 대해 전반적으로 훑어보는 내용이며, 코드가 어떻게 웹사이트가 되는지, 특정 코드가 왜 성능이 좋다고 여겨지는지 궁금한 사람들을 위한 포스트라고 한다.

## Browser Architecture

브라우저의 구현은 구현한 브라우저마다 모두 다를 것이므로, 포스트의 목적에 따라 Chrome의 최근 아키텍처만을 다룬다고 한다.

{% include image.html url="/images/inside-look-browser/browser-arch2.png" description="Chrome의 멀티 프로세스 구조" %}

Chrome은 Browser Process가 메인이 되어 다른 프로세스들을 관리하게 된다. Renderer Process의 경우에는 멀티 프로세스가 만들어진 다음에 각각의 탭에 할당된다. 비교적 최근까지 가능하면 각 탭에 프로세스 하나씩 할당을 했지만, 지금은 각 사이트(iframe을 포함해서)에 프로세스를 할당해준다고 한다. ([Site Isolation](https://developers.google.com/web/updates/2018/09/inside-browser-part1#site-isolation)을 참고하자)

### Which process controls what?

Browser Process는 **"chrome"** part라고 불리우는 부분들을 제어한다. 예를 들어 address bar나 bookmark, back button, forward button같은?? 그리고 네트워크 요청이나 파일 접근같은 권한이 필요한 태스크도 제어한다.

Renderer Process는 웹사이트가 표시되는 부분인 탭 안쪽을 관리한다.

Plugin Process는 플래시같은 플러그인과 관련된 작업들을 처리한다.

GPU 처리와 관련된 태스크들은 GPU Process로 분리되어 있는데, 그 이유는 GPU가 여러개의 어플리케이션에서 요청하는 태스크들을 처리하고 그 요청들을 같은 영역에 그려야 하기 때문이다.

그 외에도 Extension process나 utility process같은 더 많은 프로세스가 있다. 만약 직접 확인하고 싶다면 우측 상단의 옵션을 누른 다음 More Tools를 누르고 Task Manager를 눌러보자. 프로세스의 목록과 해당 프로세스가 얼마나 CPU, Memory를 사용하는지 보여주는 윈도우가 띄워질 것이다.

{% include image.html class="noshadow" url="/images/inside-look-browser/task-manager.png" description="내 Chrome으로 Netflix를 들어갔을 때의 Task Manager 창" %}

### The benefit of multi-process architecture in Chrome

크롬은 renderer process를 여러개 사용한다. 하지만 renderer process를 여러개 사용해서 얻는 이점이 무엇일까? 우선 각각의 탭이 renderer process를 가지는 경우를 생각해보자. 이 경우는 하나의 탭이 멈추어 버리면 그 탭을 끄고 다른 탭을 계속해서 사용하면 된다. 하지만, 모든 탭이 renderer process를 하나만 가진다고 가정해보자. 이 때는 하나의 탭이라도 멈추어 버리면 무조건 모든 탭이 멈춘다.

프로세스를 각자 할당해주어서 얻는 또 다른 이점은 보안과 sandboxing이다. OS가 process의 권한을 제한할 방법을 제공하므로 browser는 각각의 프로세스들의 권한을 조정할 수 있다. 예를 들어서 Chrome은 renderer process처럼 사용자의 입력을 받는 프로세스들의 파일 접근을 제한한다.

하지만 각각의 프로세스로 분리되므로 공통된 정보를 각각 복사해서 가지고 있을 때도 있다. (V8 엔진을 모두 각각 띄운다면..?) 즉, thread일 때처럼 메모리 공유가 힘들어서 프로세스가 뜨는대로 메모리를 잡아먹는다는 소리다. 그래서 크롬은 메모리를 아끼기 위해 프로세스의 갯수에 제한을 두었다. 제한은 기기의 메모리와 CPU에 따라 달라지지만, 제한에 도달하면 크롬은 같은 사이트인 여러 탭들을 하나의 프로세스만 사용해서 렌더링한다.

### Saving more memory - Servicification in Chrome
