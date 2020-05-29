---
layout: post
title: "Vue에서 v-html warning 없이 줄바꿈하기"
---

외주를 하면서 Vue를 정말 열심히 사용하고 있다. 쇼핑몰같은 사이트를 Vue로 작성하는 중인데, 상품 정보를 받아와서 보여주어야 하는 상황이다. `\n`으로 띄어쓰기를 하는 데이터가 있고, 우리는 `<br>` 태그로 나누어줘야 한다.

이걸 stackoverflow에 검색을 해보니

```html
<script>
...
  computed: {
    content: function() {
      return this.message.split('\n').join('<br />');
    }
  }
...
</script>

<template>
  ...
  <div v-html='content'>
  </div>
  ...
</template>

...
```

와 같은 방식으로 사용을 하는 것을 볼 수 있었다. 근데 이게 XSS 때문에 eslint가 자꾸 바꾸라고 한다.. [^vuejs-documentation]
사실 크게 문제되는 데이터는 아니지만, 이런저런 warning이 쌓이기 시작하면 다른 warning 메시지를 못 보고 지나치는 경우가 있어서 나의 경우는 가능하면 빨리빨리 없애는 편이다.
그래서 이 것을 없애려고 하니, 그냥 문자열 데이터이므로, `React`의 `React.Fragment`같은 것이 필요했는데,  `Vuejs`에서는 `template`을 그렇게 쓸 수 있단다.

즉, `template` 태그를 사용하면 다른 태그들을 렌더링하지 않고 virtual dom만 그려주는 것 같다. 그래서 아래처럼 처리했다.

```html
<script>
...
  computed: {
    content: function() {
      return this.message.split('\n');
    }
  }
...
</script>

<template>
  <div>
    <template v-for="(v, index) in content">
      {{ v }} <br :key="index">
    </template>
  </div>
</template>

...
```

해당 예제 코드는 [jsfiddle](https://jsfiddle.net/jeongukjae/mown9gjb/7/)로 작성을 해보았다. [^jsfiddle]

`template`에는 `key`라는 attribute가 적용되지 않아서, `br`에 적용을 해야한다. 뭐 어쨌든 warning 없이 잘 돌아간다.

[^vuejs-documentation]: https://vuejs.org/v2/guide/syntax.html#Raw-HTML 이게 여기서도 볼 수 있겠지만, XSS에 대한 위험이 있다고 한다.
[^jsfiddle]: 이렇게 쓰는 것인지는 잘 모르겠는데, 처음이라 그런지 뭔가 이렇게 다른 사람들의 url은 안 생긴것 같기도 하고..
