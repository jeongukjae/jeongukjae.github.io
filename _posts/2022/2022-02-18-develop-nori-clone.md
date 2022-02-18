---
layout: post
title: nori-clone 개발 노트
tags:
  - nlp
---

문득 생각이 들어서 [jeongukjae/nori-clone](https://github.com/jeongukjae/nori-clone)을 만들었다.
몇 주 동안 내버려 뒀다가 다시 하다가를 반복하면서 1.0.0 버전을 찍었다.
내가 왜 이렇게 개발했나를 남겨보기 위해 이 블로그 포스트를 적어본다.
이렇게 하나를 개발해보고 무언가를 선택한 이유를 적어보는 것은 처음이다.

## 배경

### 먼저, nori가 뭘까

nori란 ElasticSearch 내에 공식 한국어 내장되어 있는 한국어 형태소 분석기 중 하나이다.
Lucene 내에 내장되어 있다.
MeCab 사전을 사용하고, Kuromoji 엔진을 수정해서 개발했다고 한다.
형태소 사전 학습에 대한 고려가 들어가지 않고, 기존 엔진을 수정해서 개발한만큼 빠른 시간 내에 개발된 형태소 분석기라고 한다.
더 관심이 간다면 [ElasticSearch 블로그에 올라온 글](https://www.elastic.co/kr/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis)을 참고하면 좋을 것 같다. 😀

기존 [MeCab](https://taku910.github.io/mecab/)은 linear chain CRF 연산을 수행해야 형태소 분석을 할 수 있는데 비해 nori는 미리 계산된 연접 비용(코드를 뜯어보면 Connection cost에 해당하는 값), 단어 자체 비용과 같은 여러가지 값의 합만을 사용해서 형태소를 분석해내기 때문에 훨씬 빠르고 간단한 알고리즘을 가진다.

### 왜 nori-clone을 개발했을까

나는 형태소 분석기 자체에 굉장히 관심이 많다.
딥러닝이 대부분인 현재 NLP에서 형태소 분석기는 잘만 만들어져 있다면 큰 도움이 된다고 생각한다.
직접 모델의 전처리로는 사용하지 않아도 대량 데이터의 필터링을 위해 사용하거나, 키워드 추출 등에 잘 사용할 수 있다.
김칫국을 조금 많이 마셔보면 Knowledge Graph 등에도 활용할 수 있겠다. 😅

그런 관점에서 볼 때 여러모로 사용하기 좋은 형태소 분석기를 잘 구성해두고 싶었다.
기존에 mecab을 python 환경, tensorflow 환경에서 사용할 수 있도록 구성을 해둔 적이 있다. ([GitHub - jeongukjae/mecab-bind](https://github.com/jeongukjae/mecab-bind))
하지만 사전 파일들을 관리하기 귀찮고, 사용자 사전 추가가 너무 귀찮았다.
형태소 분석기를 구성할 때 cli 바인딩도 무조건 해놓아야 하는 점도 그러한 귀찮음에 한 몫 했다.

따라서 다른 형태소 분석기를 찾아보거나, 다른 형태소 분석 엔진을 개발하여 사용하는 편이 좋다고 생각했고,
속도가 빠르면서도 어느정도 합리적인 결과를 제공하는 nori가 후보에 들어왔다.

속도에 대해 조금 이야기해보자면, 다른 형태소 분석기와 비교할 것도 없이 검색 엔진에서 사용된다는 것만으로도 그 속도가 보장된다고 생각하는데, 실제로도 그렇다.
여러 한국어 형태소 분석기의 속도 비교 자료를 찾아보면 mecab이 제일 빠른 분석 성능을 보여주지만, nori는 개인 랩탑에서 mecab보다 약 두 배정도 빠른 성능을 보여주었다.

사용자 사전 측면에서는 굉장히 심플하게 텍스트 파일로 관리하는데 예시 포맷이 아래와 같다.

```text
c++
C샤프
세종
세종시 세종 시
```

`c++`, `C샤프` 등이 입력되면 붙여서 분절하고, `세종시`가 들어오면 `세종`과 `시`를 분리해서 분절하라는 뜻이다.
간단한 만큼 여러 품사의 사용자 사전 추가가 힘든 단점도 있지만, 실제로 사용하기에는 너무 좋겠다는 생각을 했다.

## 개발 과정의 이유

### 언어 선택

언어에 대한 고민을 잠깐 해보았지만, 하는 의미가 있을까 싶었다.
핵심 라이브러리는 C++로 개발해놓고 다른 언어로 바인딩해서 사용하는 편이 좋다고 생각한다.
Python으로 개발하면 Python 유저들에게는 좋아 보일 수는 있다.

나도 Python 환경으로 주로 사용할테지만, 바이너리 컴파일이 필요한 환경이 오지 않으리란 법도 없고, 애초에 tensorflow binding도 염두에 두고 있고, 결정적으로 속도가 너무 심하게 느리다.
Python도 매우 좋은 언어이지만 결국은 도구일 뿐이고, 이 언어에서 문자 처리에서 메모리 관리를 명시적으로 하는 것에 어려움이 있는데, 이는 연산 속도가 중요한 소프트웨어에서 매우 큰 문제라고 생각한다.
결국 속도가 느려서 사용되지 않는 것을 원하지는 않았다. (굳이 Python으로 사용하려면 [pynori](https://github.com/gritmind/python-nori)라는 라이브러리도 이미 존재했다)

따라서 Rust, C++을 두고 고민했지만, Rust에 대한 숙련도가 너무 떨어져서 C++로 골랐다.
~~물론 그렇다고 C++을 잘하지는 않는다. 🙄~~
그리고 TensorFlow binding을 해놓고 전처리 도구로 사용할까 생각 중이기도 해서 C++이 여러모로 편할 것으로 보였다.

#### UTF 처리

이 부분에 대해서 큰 고민을 하지 않았다.
utf를 처리하는 라이브러리를 개발하면서 utf 처리할 방법을 생각하지 않은 것을 깨닫고 아직 전체적인 계획을 생각하는 것이 부족하구나 생각했다.

처음에는 `wchar_t`와 같은 자료형으로 처리할까 했다.
여러 라이브러리를 찾아보고 고민을 해보았다.
그러다 [unicode-org/icu](https://github.com/unicode-org/icu)가 널리 쓰이는 것으로 보이고, 풍부한 기능을 제공해서 해당 코드를 사용하기로 했다.

### 빌드 시스템

떠오른 것이 Bazel, CMake 밖에 없었다. (IDE 종속적인 것은 애초에 고려하지 않는다)
CMake는 예전에 PyTorch에 자주 기여할 때 조금 써보았고, Bazel은 TensorFlow 코드를 살펴볼 때나 개인 프로젝트를 진행할 때 살펴보았었다.
다른 언어에 바인딩하는 것을 중요한 목표 중 하나로 두고 있었기 때문에 Bazel을 사용하기로 했다.

Bazel 철학에 많이 동의하기도 하고, 언어 중립적으로 사용할 수 있는 Bazel이 이 프로젝트에서 사용하기에 더 편할 것으로 보였다.
아래에서 더 이야기하겠지만, protobuf 관리가 편한 것도 이유 중 하나였다.
여러모로 언어에 종속적이지 않은 가장 강력한 빌드 시스템은 Bazel이 아닌가 생각한다.

### 사전 파일 포맷

사전 파일 포맷에 고민이 많았다.
lucene의 nori는 바이너리 포맷의 사전을 사용하고, mecab도 바이너리 형태를 사용한다.
(몇몇 글에서는 csv를 사용한다고 하지만 해당 포맷은 빌드하기 전의 사전 파일들이고, 실제로 빌드 후에는 바이너리 파일 및 설정 파일 형태로 빌드 된다)
lucene nori 코드를 살펴보면 몇몇 필드들을 `uint16`과 같은 형태로 serialize하여 저장 공간을 아끼고, 문자들의 경우 FST를 사용해서 더더욱 저장 공간을 아낀다.
이렇게 해서 24MB 정도의 사전파일을 만드는데, 대단하기도 하면서 직접 serializer/deserializer를 짜야할까를 많이 고민했다.

이런저런 고민을 하다가 결국 protobuf message를 binary로 serialize해서 저장하기로 했다.
[Protobuf Techniques docs](https://developers.google.com/protocol-buffers/docs/techniques)에서 아래처럼 말해서 양심에 매우 찔렸지만..

> Protocol Buffers are not designed to handle large messages. As a general rule of thumb, if you are dealing in messages larger than a megabyte each, it may be time to consider an alternate strategy.

그래서 퍼포먼스 이슈가 있을지 서치해보았다.
[Stackoverflow 답변 하나](https://stackoverflow.com/questions/47564437/why-protobuf-is-bad-for-large-data-structures)와 [GitHub Issue 하나](https://github.com/protocolbuffers/protobuf/issues/7968)를 찾을 수 있었고, 카피가 많이 일어나는 것, 시스템 제한으로 2GiB 정도까지만 사용할 수 있는 점 (<- TensorFlow 사용 시에 종종 보았던 이슈) 정도인 것으로 보였다.
내 경우에는 크게 걱정할 일이 없어서 Protobuf로 사용했다.

다만, protobuf로 serialize하고 나니 꽤 용량이 커서 snappy로 추가 압축을 진행했다.
사전 로딩 속도에 큰 영향을 주지 않으면서, 최종 바이너리에도 큰 영향을 주지 않는 snappy라 사용하기로 했고, 압축 후에는 25MB 근처의 용량의 사전 파일 하나가 나왔다.

## 결과

위에서 고민한대로 구현했고, <https://github.com/jeongukjae/nori-clone> 에서 결과를 볼 수 있다.

C++로 개발 후 Golang, Python 대상으로 바인딩을 진행했고, 속도는 아래 정도가 나왔다. Lucene 내에 포함된 nori에 비해 약간 빠르거나 비슷한 성능이다.
조금 더 최적화를 할 수 있겠지만, 내 C++ 지식으로는 여기까지가 충분하다고 생각이 들어 속도 자체에 큰 집착을 하지는 않았다.

{% include image.html url="https://github.com/jeongukjae/nori-clone/raw/00834cbb1c2d348208bef3ea067d65787723be33/tools/benchmark/imgs/elapsed_time.png" width=80 description="nori clone 벤치마크 자료" %}

실제 nori와 같은 분석결과가 나오는지 궁금해서 몇몇 예시를 만들어서 maven에서 nori를 땡겨와 비교해보았다. (<https://github.com/jeongukjae/nori-clone/tree/v1.0.0/tools/comparison>)
NSMC 텍스트나 nori 내에 존재하는 테스트 케이스, 이것저것 한자, 영어 텍스트를 추가해서 테스트해보았고, SYMBOL을 제외하고는 모두 같은 결과인 것을 확인할 수 있었다.
`..` 과 같은 케이스만 다르게 나오고 의미있는 단어로 볼 수 있는 문자들은 분석 결과가 동일했다.
의아한 점은 분석 시에 nori-clone의 구현체의 출력값이 총 비용이 더 낮은데 원래의 nori가 왜 그렇게 나오는지 궁금하다.
결과 분석을 위한 케이스는 <https://github.com/jeongukjae/nori-clone/blob/main/tools/comparison/data.txt>에서 볼 수 있다.

해당 시스템을 사용해서 NFKC utf normalization이 들어가 있고 최신 mecab 사전으로 빌드한 사전도 사용할 수 있도록 구성했다.

## Future works

여러가지를 시도해보고 싶다. 지금 생각나는 것은 아래 정도이다.

- 사용자 사전에 다양한 품사 태그 지원
- 아직 추가해놓지 않은 동의어 사전 기능 추가
- MeCab 사전에 존재하는 메타 정보 지원
- 비지도 신조어 탐색 (이 블로그 글을 쓰는 것이 늦어지면서 완료할 때에 이미 해보았다 - <https://jeongukjae.github.io/posts/pos-tagger-branching-entropy/>)
- 이러한 형태소 분석기를 모아서 의존성이 아예 존재하지 않는 한국어 텍스트 처리 라이브러리
- 동의어 사전을 사용해 Data augmentation - 추후에 TensorFlow에도 Custom ops로 연결해 쉽게 data augmentation을 할 수 있도록 하고 싶다.

## 마무리

Future works로 생각 중인 것들을 언제 다 할 수 있을지, 진짜 다 할지는 모르겠지만, 지금 시점에는 여기까지 진행한 것으로 우선 만족이다.
Bazel 자체에 대해서나 C++에 대해서도 숙련도가 많이 올라갔다.
또 아직 더 배우고 만들어 볼 것이 넘쳐나는 것에 감사하다.
