---
layout: post
title: "VSCode에서 Aliasing된 경로들 intellisense 지원하기"
tags:
  - editor
  - node js
  - vue
---

나는 반복되고, 읽기 힘든 경로를 손으로 쓰는 것(심지어 에디터에서 자동완성을 지원하더라도)을 매우 싫어하는데, 그 때 자주 쓰는 기능이 webpack에서 지원하는 aliasing이다. (vuejs cli가 내부적으로는 webpack을 사용하므로) 우선 이 방법은 [chrisvfritz/vue-enterprise-boilerplate](https://github.com/chrisvfritz/vue-enterprise-boilerplate)에서 처음 보고 다른 자바스크립트 프로젝트에도 적용해서 쓰는 방식이다.

## 기능부터 지원하자

intellisense가 지원이 되어도 실제로 aliasing이 안되면 쓸모가 없는 기능이니, 실제 aliasing 부터 지원하자. 먼저 나는 webpack에서 지원하는 resolve라는 기능을 사용하기 위해 `vue.config.js` 를 아래처럼 자주 쓴다.

```javascript
...

module.exports = {
  configureWebpack: {
    ...
    resolve: {
      alias: require('./aliases.config').webpack,
    },
  },
  ...
}
```

자, 그럼 `aliases.config.js`는 어떻게 쓰는지 궁금할텐데, 아래처럼 쓴다.

```javascript
const aliases = {
  '@src': 'src',
  '@assets': 'src/assets',
  '@router': 'src/router',
  '@store': 'src/store',
  ...
}

module.exports = {
  webpack: {},
  jsconfig: {},
}

for (const alias in aliases) {
  const aliasTo = aliases[alias]
  const aliasHasExtension = /\.\w+$/.test(aliasTo)

  module.exports.webpack[alias] = path.resolve(__dirname, aliasTo)
  module.exports.jsconfig[alias + '/*'] = [aliasTo + '/*']
  module.exports.jsconfig[alias] = [
    aliasTo + '/index.js',
    aliasTo + '/index.json',
    aliasTo + '/index.vue',
    aliasTo + '/index.scss',
    aliasTo + '/index.css',
  ]
}
```

webpack의 aliasing을 위해 `@src`와 같은 폴더를 `src`로 매핑하준다. (코드를 보면 알겠지만, `webpack` 이외에도 `jsconfig` 용 오브젝트도 존재하는데, 그게 나중에 쓰일 것이다.) 이 방식이 좋은 방식이라고 생각하는 이유는, 나는 같은 방식으로 aliasing을 해야할 때, 반복해서 작성하는 것이 싫었는데, 이 방식은 한번 작성해놓고, export를 통해서 여러 곳에서 공유해서 사용을 하여 중복을 줄이고 편하게 관리를 해준다는 점이다. 지금은 webpack, jsconfig 뿐이지만, jest에서도 이 파일을 접근해서 사용을 한다. 그리고 나는, vue cli를 시작할 때 매핑된 경로들을 보여주고 시작하게 설정을 해놓았다. 

일단은 다시 본론으로 돌아와 실제로 생성되는 object는 아래와 같을 것이다.

```json
{
  "@src": "some-path-to-project/src",
  "@assets": "some-path-to-project/src/assets",
  "@router": "some-path-to-project/src/router",
  "@store": "some-path-to-project/src/store",
  ...
}
```

이 경로들이 `vue.config.js`에서 resolve되어 정상적으로 실행이 된다. 자세한 사용방법이나, 그 외 다른 설정들은 [webpack 문서 - configuration - resolve](https://webpack.js.org/configuration/resolve/)를 살펴보면 된다.

## 자 그럼 intellisense는?

자 그럼 intellisense를 지원해보자. 일단은 어떤 ide를 쓰는지 알아야 하는데, 나는 자바도 간단한 것은 gradle 스크립트를 직접 작성하여 vscode에서 돌릴정도로 vscode를 애용하기 때문에 vscode 기준으로 설명한다. (jsconfig를 쓴 시점부터 이미..) 

### vscode의 intellisense 설정

`jsconifg.js`나, `jsconfig.json`은 어떤 방식을 가지는지가 먼저 궁금할텐데, 아래와 같은 파일 형태이다. 물론 더 자세한 파일 형태는 [vscode의 jsconfig 레퍼런스](https://code.visualstudio.com/docs/languages/jsconfig)를 참고하자.

```json
{
  "baseUrl": ".",
  "include": ["src/**/*"],
  "compilerOptions": {
    "baseUrl": ".",
    "target": "es6/es2018/...",
    "module": "es6/es2018/...",
    "paths": {
      "ClientApp/*": ["./ClientApp/*"]
      ...
    }
  }
}
```

그 외 더 많은 옵션이 있겠지만, 나는 사용을 하진 않았다. 잘 보면 `compilerOptions.paths` 안의 값이 array 형태이므로 위의 `alias.config.js`에서 배열 형태로 들어갔다.

```javascript
module.exports.jsconfig[alias + '/*'] = [aliasTo + '/*']
module.exports.jsconfig[alias] = [
  aliasTo + '/index.js',
  aliasTo + '/index.json',
  aliasTo + '/index.vue',
  aliasTo + '/index.scss',
  aliasTo + '/index.css',
]
```

### intellisense 설정 파일 자동화

그리고 잘 생각해보면 vue cli를 이용하는 한 `yarn serve`라는 키워드도 많이 작성을 할 것인데, 그 때마다 `vue.config.js`가 호출이 되므로, 그 파일에서 `alias.config.js`를 require할 때마다 `jsconfig.json`을 다시 교체해준다면 크게 문제는 없을 것이다. (alias를 자주 설정하는 초기를 제외하고는)

그래서 `vue-enterprise-boilerplate` 레포지토리에서는 `jsconfig.template.js`라는 파일을 생성해 기본적인 설정들을 넣어두고(`compilerOptions.paths`를 제외한 값들) `alias.config.js`이 require 될 때 `jsconfig.template.js` 파일에 `compilerOptions.paths`만 넣어준 json 오브젝트들을 `jsconfig.json`으로 작성을 해준다.

그래서 아래와 같은 형식으로 `jsconfig.template.js`를 작성을 해준다.

```javascript
module.exports = {
  baseUrl: '.',
  include: ['src/**/*', 'tests/**/*'],
  compilerOptions: {
    baseUrl: '.',
    target: 'es6',
    module: 'es6',
    // ... paths
  },
}
```

그리고 `alias.config.js`에서 아래처럼 `jsconfig.json`을 생성해준다.

```javascript
const jsconfigTemplate = require('./jsconfig.template') || {}
const jsconfigPath = path.resolve(__dirname, 'jsconfig.json')

fs.writeFile(
  jsconfigPath,
  JSON.stringify({
    ...jsconfigTemplate,
    compilerOptions: {
      ...(jsconfigTemplate.compilerOptions || {}),
      paths: module.exports.jsconfig,
    },
  }),
  error => {
    if (error) {
      console.error(
        'Error while creating jsconfig.json from aliases.config.js.'
      )
      throw error
    }
  }
)
```

원래 `vue-enterprise-bolierplate`에는 prettier로 포맷팅해주는 코드가 존재했는데, 나는 "어차피 `.gitignore`에도 등록된 파일인데 굳이..?" 라는 생각이 들어 뺐다.

### 끝

자 그래서 결과를 살펴보면 아래처럼 잘 뜬다.

{% include image.html url="/images/2018-11-22-jsconfig/working.png" alt="intellisense가 잘 동작한다!" description="intellisense가 잘 동작한다!" %}

---

근데 사실 이 포스트는 해당 레포지토리의 코드를 잘 사용하다가 분석 해놓은 것밖에 되지는 않기 때문에 그렇게 공을 들이진 않았지만, 자주 사용을 하게 되다보니 한번 정리를 해보았다. 나름 편하게 잘 사용하는 설정이다.

이제 공부하는 내용 말고도 코드를 작성할 때 막히는 부분이나, 자주 사용하는 프로젝트 설정 등을 하나 둘 씩 정리를 하려고 하는데, 역시 생각만 한달을 하다가 이제 시작한다.
