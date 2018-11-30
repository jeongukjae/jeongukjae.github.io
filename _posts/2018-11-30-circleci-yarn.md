---
layout: post
title: "CircleCI에서 발생하는 yarn 오류"
tags:
  - javascript
  - ci
  - devops
  - 에러해결기
---

지금 개발중인 프로젝트가 node `10.11.0` 버전을 사용해서 CircleCI의 `circleci/node:10.11.0` 이미지로 빌드는 하는데, 이번주부터 갑자기 `checkout` job이 실패했다고 뜨더라.

{% include image.html url="/images/2018-11-30-yarn/error.png" alt="yarn 오류" description="슬랙으로 자꾸 넘어오는 동일한 오류" %}

## 뭐가 문제야?

그래서 circleci 빌드 로그를 확인해보니 아래처럼 떴다.

```shell
$ yarn
yarn install v1.9.4
[1/4] Resolving packages...
[2/4] Fetching packages...
(node:68) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
error An unexpected error occurred: "https://registry.yarnpkg.com/event-stream/-/event-stream-3.3.6.tgz: Request failed \"404 Not Found\"".
info If you think this is a bug, please open a bug report with the information provided in "/home/circleci/프로젝트이름이예요 ㅎㅎ 이건 좀 지울게요/yarn-error.log".
info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
Exited with code 1
```

프로젝트 빌드 설정은 그대로 쓰고 있었기 때문에 아마도 버전이 올라가면서 기존 낮은 버전들을 `deprecated` 시켰나 싶어서 circleci 쉘로 들어가보았다.

```shell
circleci@some-hash:~$ yarn -v
1.9.4
```

## 일단 고쳐보자

사용중인 버전은 위의 로그에서도 확인가능하듯 1.9.4. 그래서 일단 1.12.3으로 버전업부터 해보았다.

```shell
circleci@some-hash:~$ sudo npm install -g yarn
/usr/local/bin/yarnpkg -> /usr/local/lib/node_modules/yarn/bin/yarn.js
/usr/local/bin/yarn -> /usr/local/lib/node_modules/yarn/bin/yarn.js
+ yarn@1.12.3
added 1 package in 0.349s
circleci@some-hash:~$ yarn -v
1.12.3
```

그러고 나서 프로젝트 폴더로 들어가서 다시 설치를 해보니

```shell
circleci@some-hash:~$ cd some-project-name/
circleci@some-hash:~/some-project-name$ yarn
yarn install v1.12.3
[1/4] Resolving packages...
[2/4] Fetching packages...
error https://registry.yarnpkg.com/event-stream/-/event-stream-3.3.6.tgz: Extracting tar content of undefined failed, the file appears to be corrupt: "Unexpected end of data"
info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
```

그래도 오류가 뜬다. 저런 오류는 처음봐서 일단 `yarn.lock`을 지우고 다시 설치나 해볼까 했더니 

```shell
circleci@some-hash:~/some-project-name$ rm yarn.lock
circleci@some-hash:~/some-project-name$ yarn
yarn install v1.12.3
info No lockfile found.
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Saved lockfile.
Done in 18.63s.
```

된다..

## -

왜 이런 오류가 뜰까 하고 [yarn github repo](https://github.com/yarnpkg/yarn)에서 이슈를 찾아봤다. 다른 사람들도 이런 오류를 많이 겪는 것 같았고, 보통 yarn 커맨드에 옵션을 붙여서 사용하거나, `~/.npmrc`를 지워보거나, `yarn.lock`을 지워보고 해결했다고 한다. 나의 경우에는 자세한 오류의 원인이 필요없어서 `yarn.lock` 지우고 그냥 regenerating 했다. 그리고 비교적 최근까지도 이슈에 코멘트가 달리고 있길래 (심지어 해결책은 달랐다) 내 상황이랑 해결한 방법 정도만 남겨놓고 왔다. [이 이슈 (#6312)](https://github.com/yarnpkg/yarn/issues/6312)가 내가 참고한 이슈.

{% include image.html url="/images/2018-11-30-yarn/github.png" alt="issue 댓글" description="그냥 다들 자기 상황을 알리고 있길래..." %}

yarn을 쓰기 시작하고나서 yarn오류를 꽤나 자주 겪는데, 그 오류는 십중팔구 `yarn.lock`을 regernating하면 해결이 되었다. 왜 그런지는 잘 모르겠지만..

## 그래서 성공했어?

{% include image.html url="/images/2018-11-30-yarn/s.png" alt="성공" description="결국 성공했다" %}

그냥 `.circleci/config.yml`에 사용한 커맨드 다 추가했고, 레포지토리에도 `yarn.lock` 파일 재생성해서 넣어줬다.