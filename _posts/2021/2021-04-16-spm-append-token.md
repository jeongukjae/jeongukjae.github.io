---
layout: post
title: SentencePiece 새로운 토큰 추가하기
---

SentencePiece 기존 모델을 유지하면서 사용할 일이 있어서 해봤다.

## 참고한 이슈

* [google/sentencepiece#398](https://github.com/google/sentencepiece/issues/398)
* [google/sentencepiece#121](https://github.com/google/sentencepiece/issues/121)
* [google/sentencepiece#323](https://github.com/google/sentencepiece/issues/323)

핵심은 sentencepiece model 파일은 protobuf serialize 된 binary 파일이고, `sentencepiece.sentencepiece_model_pb2`에 존재하는 `ModelProto`를 활용하면 토큰을 교체하거나 score를 바꾸는 것, 토큰을 추가하는 것도 다 가능하다고 한다. score 바꾸거나, 토큰 교체는 위 이슈들 참고.

## 추가하는 법

```python
import sentencepiece as spm
import sentencepiece.sentencepiece_model_pb2 as model

m = model.ModelProto()
m.ParseFromString(open("old.model", "rb").read())

new_piece = type(m.pieces[0])()
new_piece.piece = "NEW_TOKEN_TO_ADD"
new_piece.score = 0.0
new_piece.type = 1  # normal

m.pieces.append(new_piece)

with open("new.model", "wb") as f:
    f.write(m.SerializeToString())

sp = spm.SentencePieceProcessor(model_file="new.model")
print(sp.encode("NEW_TOKEN_TO_ADD ㅋㅋㅋ", out_type=str))
```

score가 0.0이면 무조건 해당 토큰으로 잘리는 것으로 알고 있어 0.0으로 설정했다. type은 `sentencepiece.sentencepiece_model_pb2` 패키지 안에서 적당히 들고오면 될 듯. `1`이 normal token이길래 normal로 했다.
