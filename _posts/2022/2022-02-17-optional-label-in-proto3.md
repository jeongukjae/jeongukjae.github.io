---
layout: post
title: proto3 문법의 optional label (Field presence)
tags:
  - protobuf
---

Protobuf를 사용해서 코드를 작성할 때 `optional` label이 실제로 있는 것과 없는 것의 차이를 거의 몰랐다. 그래서 기능을 정확히 알아보기 위해 기능과 관련 GitHub을 찾아보고 `optional` 레이블에 대해 알아본 것들을 이 포스트로 남긴다.

## `required`, `optional` label

Protocol Buffer 3는 proto2 문법에서 많이 사용되던 `required`와 `optional` 없이 출시했다고 한다. 나는 proto2 문법을 사용해본 적이 없기 때문에 관련된 이유를 GitHub 이슈에서 찾아보았고, [아래 코멘트](https://github.com/protocolbuffers/protobuf/issues/2497#issuecomment-267422550)를 찾을 수 있었다.

> We dropped required fields in proto3 because required fields are generally considered harmful and violating protobuf's compatibility semantics. The whole idea of using protobuf is that it allows you to add/remove fields from your protocol definition while still being fully forward/backward compatible with newer/older binaries. Required fields break this though. You can never safely add a required field to a .proto definition, nor can you safely remove an existing required field because both of these actions break wire compatibility. ... ... ... We have seen production issues caused by this multiple times and it's pretty much banned everywhere inside Google for anyone to add/remove required fields. For this reason we completely removed required fields in proto3.
>
> After the removal of "required", "optional" is just redundant so we removed "optional" as well.

즉, 이유를 정리하면 "깨지지 말아야 할 상황에서도 `required` 필드 때문에 backward/forward compatibility가 맞지 않게 되고 안전하게 `required` 필드를 제거/추가할 수 없었다고 한다. 구글 내부에서도 그래서 아무도 `required` 레이블을 쉽게 추가/제거할 수 없었다" 정도이다. 그래서 `required`를 제거하고 보니 `optional`도 redundant해서 같이 제거했다고 한다. 전 구글러 분께 여쭤보니 구글 내에서는 실제로  best practice로 `optional`을 가급적 전부 붙이게 한다고.

몇몇 문서를 더 찾아보면, `optional`을 redundant하게 생각할 수 있는 이유는 natual zero value를 가진 필드를 optional한 것처럼 처리할 수 있었기 때문이라고 한다.

여기서 `required`를 없애는 것은 어느정도 이해가 가는 결정이지만, `optional`을 제외하는 것은 크게 이해가 가지는 않았다. 그래도 어플리케이션 코드에서 잘 처리하면 되는 것은 맞기 때문에 문제는 없다고 생각한다.

## Protobuf 3.15

하지만 이게 [Protobuf 3.15](https://github.com/protocolbuffers/protobuf/releases/tag/v3.15.0)에서는 다시 추가가 된다. 정확한 타임라인은 모르는 상태이지만, 여기저기 돌아다니면서 가끔 볼 수 있는 WKT(WellKnownTypes)에 있는 [`protocolbuffers/protobuf/src/google/protobuf/wrappers.proto` (링크)](https://github.com/protocolbuffers/protobuf/blob/b0bf163c78d6839fad43146e7d2f85c59a4e5b6d/src/google/protobuf/wrappers.proto)를 참고해보면 어느정도 이유를 알 것 같기도 하다. 주석에 아래처럼 적혀있다.

```c++
// Wrappers for primitive (non-message) types. These types are useful
// for embedding primitives in the `google.protobuf.Any` type and for places
// where we need to distinguish between the absence of a primitive
// typed field and its default value.
//
// These wrappers have no meaningful use within repeated fields as they lack
// the ability to detect presence on individual elements.
// These wrappers have no meaningful use within a map or a oneof since
// individual entries of a map or fields of a oneof can already detect presence.
```

"Primitive Type 필드에서 값의 부재와 default value 사이의 차이를 알 수 있으니 유용하다." 정도로 이해하면 된다. 대부분의 경우에는 아니겠지만, 분명히 string 타입에서 `null`과 `""` 차이를 주어야 할 때가 있는데, 그럴 때 처리할 수 있는 wrapper들이다.

아무튼 다시 3.15로 돌아와서 이야기하면, optional에 대한 구현체가 공식적으로 들어왔다.
해당 동작방식을 설명하는 문서가 [`protocolbuffers/protobuf/docs/field_presence.md` 파일](https://github.com/protocolbuffers/protobuf/blob/master/docs/field_presence.md)에 있다.

## proto3 & Field presence

이 문서를 핵심만 살펴보자.

> There are two different manifestations of presence for protobufs
> * no presence, where the generated message API stores field values (only)
> * explicit presence, where the API also stores whether or not a field has been set.
>   * Singular proto3 fields of basic types (numeric, string, bytes, and enums) which are defined with the `optional` label have explicit presence, like proto2 (this feature is enabled by default as release 3.15).

Protobuf에 presence에 관한 두가지 동작방식이 있는데, `no presence`와 `explicit presence`이다. `no presence`는 필드의 값만 저장하고, `explicit presence`는 필드의 값이 설정되었는지 여부를 같이 저장한다. 기본 타입들에 `optional` 레이블을 추가할 경우 `explicit presence`로 동작하게 된다.

> The no presence discipline relies upon the field value itself to make decisions at (de)serialization time, while the explicit presence discipline relies upon the explicit tracking state instead.

`no presence`는 런타임에 해당 값이 설정되어 있는지 확인하고 (natural zero value라면 clear된 환경), `explicit presence`는 state 값을 살펴본다.

여기서 왜 계속 기본 타입에 대해 이야기하는지는 [Presence in proto3 APIs 섹션](https://github.com/protocolbuffers/protobuf/blob/master/docs/field_presence.md#presence-in-proto3-apis)을 보면 알 수 있는데, message, repeated, oneofs, maps는 `optional` label에 영향을 받지 않는다. 오히려 message를 제외한 나머지 세개는 붙일 수 없다.

{% include image.html url="/images/2022/02-17-proto3-presence/table.png" width=60 %}

하지만 singular message와 같은 경우에는 presence의 동작 차이가 없는데 왜 `optional`레이블을 붙이는 것이 가능한걸까? 실제로 동일하게 처리되는지도 궁금하다.

## 확인해보기

우선 확인해보기 위해 몇개의 메시지를 정의해보았다.

```proto
// sample.proto
syntax = "proto3";

enum FooEnum {
    BASE = 0;
    FOO = 1;
    BAR = 2;
}

message Foo {
    string str_field = 1;
    optional string optional_str_field = 2;

    int32 int32_field = 3;
    optional int32 optional_int32_field = 4;

    FooEnum enum_field = 5;
    optional FooEnum optional_enum_field = 6;
}

message Bar {
    message Msg {}
    Msg msg_field = 1;
    optional Msg optional_msg_field = 2;
}

```

그리고 파이썬 스크립트로 돌려보았다.

```python
from contextlib import contextmanager

import sample_pb2


def main():
    # Check singular values' presence
    message = sample_pb2.Foo()

    with _should_raise():
        message.HasField("str_field")
    message.HasField("optional_str_field")

    with _should_raise():
        message.HasField("int32_field")
    message.HasField("optional_int32_field")

    with _should_raise():
        message.HasField("enum_field")
    message.HasField("optional_enum_field")

    # Check messages' presence
    message = sample_pb2.Bar()
    message.HasField("msg_field")
    message.HasField("optional_msg_field")


@contextmanager
def _should_raise():
    try:
        yield
        raise Exception("Not raised any exception")
    except ValueError as e:
        print("_should_raise succeed, msg:", e)


if __name__ == "__main__":
    main()
```

위 스크립트는 exit code 0으로 정상 종료한다.
`string`, `int32`, `enum`은 정상적으로 HasField를 호출 할 때 `Protocol message Foo has no non-repeated submessage field "str_field" nor marked as optional` 와 같이 에러가 난다.
하지만 `msg_field`, `optional_msg_field`는 `HasField` 메소드가 둘 다 문제 없이 돌아간다.

추가로 message를 확인해보면 natural zero value들로 잘 나온다.

## 마무리

`explicit presence`, `no presence`에 대해서는 충분히 이해했다.

* 필드를 optional로 처리하는 것이 best practice이다.
* optional 레이블과 protobuf WKT의 wrappers는 같은 역할로 사용할 수 있다.
* optional 레이블이 explicit presence에 영향을 주는 타입이 아닌 경우에는 영향이 없다.
* optional 레이블이 영향이 있는 경우(singluar numeric, enum, string or bytes)에는 가급적 사용하자

위 정도로 이해했는데, 마지막으로 풀리지 않은 하나의 의문은 정말 message는 왜 `optional`을 붙일 수 있는 걸까?
