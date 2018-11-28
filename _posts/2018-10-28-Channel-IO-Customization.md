---
layout: post
title: "Channel IO 커스텀화"
tags:
  - javascript
  - vue
  - web
---

## Channel IO

최근 Vue js를 사용하는 외주를 하면서, 고객들에게 웹 페이지에 [channel io](https://channel.io/ko)를 달아달라는 요청을 받았다. channel io는 고객과 상담을 위해 웹/앱에 메신저 기능을 넣어주는 플러그인이다.

![channel io]({{ site.url }}/images/2018-10-28-channel-io/channel-io-home.png)

하지만 우리는 Vue js를 사용하기 때문에 컴포넌트화를 시켜서 사용을 하는 것이 좋겠다는 생각을 했다. 그 이유는 "필요한 페이지에서 끄고 킬 수 있어야 한다"는 것이었고, *vue-router*를 사용중이기 때문에 적용되어야 하는 뷰 별로 템플릿 맨 아래 컴포넌트를 붙여서 사용을 하기로 헀다.

## 시작

### 방법 1

우선 어떤 방식으로 사용을 할 수 있는지 살펴야 하므로 [channel io 개발자 문서](https://developers.channel.io/docs)를 참고한다. [^1]

![general case]({{ site.url }}/images/2018-10-28-channel-io/general-case.png)

일단은 단순하게 로딩만 하는 범용적인 상황에 대한 예시 코드가 있길래 적용을 해봤다. 하지만 이 경우 문제점이 생겼다.

1. 우리가 원하는 "페이지 별 메신저 로딩"이 적용되지 않는다.
2. z-index가 너무 크다... (하지만 이 경우는 문서를 읽어보니 해결이 되는 상황이었다)

### 방법 2

그래서 문서를 뒤져보다가 찾은 것이 커스터마이제이션.

![custom]({{ site.url }}/images/2018-10-28-channel-io/customization.png)

커스터마이제이션 탭을 참고하는데, 이것은 작성중인 사이트에 그대로 적용이 불가능하다..

1. 가끔 페이지를 많이 이동하고 나서 커스텀 버튼이 동작을 하지 않는다.
2. 원래의 메신저 호출 버튼과 같은 버튼을 사용할 수 없다. (이건 최종도 마찬가지이다.)

그 원인으로는 한가지 생각된 것은 해당 컴포넌트가 계속해서 mount, unmount (destory) 하는데, 계속해서 스크립트를 불러오고 (물론 중복해서 스크립트를 불러오진 않는다), 불러온 후의 이벤트를 호출하면서 예상대로 동작하지 않는 것 같았다. 

### 방법 3

SDK 레퍼런스 뒤져보기

![sdk]({{ site.url }}/images/2018-10-28-channel-io/sdk.png)

SDK 레퍼런스를 뒤져보니까 스크립트 로딩 후, 로딩된 이벤트, 메신저를 여는 트리거 등등이 다 존재했다.

```javascript
// 이건 로딩 후 초기화하는 트리거
ChannelIO('boot', channelPluginSettings: Object);

// 메신저 화면을 보여주는 이벤트
// 이걸 버튼 이벤트에 달았다
ChannelIO('show');

// 이게 초기화 완료 이벤트
ChannelIO('onBoot', function(guest) {
  // YOUR CODE...
});
```

나는 위의 트리거/이벤트 등을 활용했다.

## 최종

기본적으로 launcher 아이콘이 나타나지 않게 하고, 그 launcher button의 스타일은 그대로 가져왔다. 또한 unreadBadge에 대한 설정을 추가적으로 해주었다.

아래는 그 코드이다.

```html
<script>
import { loadScript } from '@libs/scripts'

window.channelPluginSettings = {
  pluginKey: 'plugin key',
  hideDefaultLauncher: true,
}

export default {
  name: 'channel-io',
  data: () => ({
    active: false,
    unreadCount: 0,
  }),
  methods: {
    launcher() {
      console.log('show messenger')
      window.ChannelIO('show')
    },
  },
  mounted() {
    loadScript(
      'https://cdn.channel.io/plugin/ch-plugin-web.js',
      'ChannelIO'
    ).then(value => {
      if (value) {
        var ch = function() {
          ch.c(arguments)
        }
        ch.q = []
        ch.c = function(args) {
          ch.q.push(args)
        }
        window.ChannelIO = ch
        window.ChannelIO('boot', window.channelPluginSettings)
        window.ChannelIO('onBoot', () => {
          this.active = true
        })
        window.ChannelIO('onChangeBadge', unreadCount => {
          this.unreadCount = unreadCount
        })
      }
    })
  },
}
</script>

<template>
  <div id='ch-plugin-wrapper' @click="launcher" v-bind:class="{active: active}">
    <div id="ch-plugin-launcher">
      <span />
      <div id='ch-plugin-badge' size="24" font-size="14" v-bind:class="{active: unreadCount > 0}">{{ unreadCount }}</div>
    </div>
  </div>
</template>

<style lang='scss' scoped>
#ch-plugin-wrapper {
  /* some styles */
}
</style>
```

우리는 `loadScript`라는 공통적인 스크립트 로드 함수를 만들어놓고 쓰기 때문에 그를 사용하였고, 두번째 인자로 넘어가는 `'ChannelIO'`는 스크립트를 중복되게 로드하지 않기 위해 `window` 오브젝트에 추가해서 사용하는 오브젝트의 키이다. 

promise의 `resolve`의 인자로 넘어오는 `value`는 스크립트가 정상적으로 로드되었을 경우 해당 스크립트에 대한 정보가 넘어온다. 그래서 로드가 되었을 경우에만 처리해주기 위해서 저렇게 처리했다. 

```javascript
window.ChannelIO('boot', window.channelPluginSettings)
window.ChannelIO('onBoot', () => {
  this.active = true
})
window.ChannelIO('onChangeBadge', unreadCount => {
  this.unreadCount = unreadCount
})
```

이 부분이 스크립트를 불러오고 나서 초기화 해주는 부분이다. mount 될 때 해당 스크립트를 불러오면서 런처 아이콘을 css 애니메이션과 함께 보여주는데, (이 때문에 hot reloading인 상황에서는 보이지 않는다. 무조건 refresh 버튼을 눌러주어야 보인다.. 이부분은 추후 문제가 될 때 수정을 할 예정) 단순히 스크립트가 로드되지 않았을 때 버튼을 숨기기 위한 것이다. 

onChangeBadge 이벤트 리스너는 사용자가 메신저 창을 닫고, 사용을 할 때 상담사로부터 메시지가 오면 channel io의 아이콘에 알림 표시로 안 읽은 메시지 숫자가 떠서 그 ui 처리를 위한 것이다.

![result]({{ site.url }}/images/2018-10-28-channel-io/result.png)

최종 결과 화면. 잘 뜬다..

## 끝

1. 사실 처음에 Customization이라는 이름의 문서를 읽고, 원하는 정보가 없었다. 그래서 다른 라이브러리 들과 비슷하게 js 파일 뜯어서 트리거 함수 찾아서 사용하려 하다가, 부분적으로 react + redux를 사용하는 플러그인인 것을 보았는데 이게 더 귀찮겠다 싶어서 다른 문서들도 읽어보기 시작했다. 그러고 sdk 방법3의 문서를 읽어보았다. customization 탭에 있는 정보가 '당연히' 전부 인 줄 알고, sdk reference는 내부 개발자를 위한 정보를 밖에 열어준 줄 알았기 때문이다. (이제 잘 좀 읽자)
2. 어떻게 되었든 원하는 형태로 구현을 했는데, 만약 channel io에서 `launcher button`의 스타일을 변경하거나, 고객측에서 문구를 변경하고 싶을 때, 일일히 코드를 만져야 하는 점이 문제이긴 하다.
3. 덕분에 channel io를 처음 사용하게 되어서 플랜들과 기능들을 살펴보았는데 생각보다 다른 서비스들에 적용하기 좋은 서비스들 같아서 많이 사용하게 될 것 같다.
4. 아직도 왜 저런식으로 `window.ChannelIO`를 등록하는지는 잘 모르겠다.. (내 지식이 부족한 것일 수도..)

---

[^1]: 개발자 문서를 읽는데, 개발때문에 컴퓨터 언어를 영어로 사용하는 탓인지, 영어와 일본어(..?)만 뜬다. 영어는 이해를 하지만, 일본어는 왜..?
