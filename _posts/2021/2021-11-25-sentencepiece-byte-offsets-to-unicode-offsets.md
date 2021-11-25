---
layout: post
title: SplitterWithOffsets - split_with_offsets를 UTF8 단위로 변경하기
tags:
  - python
---

아래처럼 변경해서 쓸 수 있다.

```python
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

preprocessor = hub.load("https://tfhub.dev/jeongukjae/distilkobert_cased_preprocess/1")
tokenize_with_offsets = hub.KerasLayer(preprocessor.tokenize_with_offsets)

@tf.function(input_signature=[tf.TensorSpec([None], dtype=tf.string)])
def _tokenize(x):
    tokens, starts, ends = tokenize_with_offsets(x)
    x = tf.map_fn(
        lambda x: tf.repeat(x[0], tf.size(x[1])),
        [x, tokens],
        fn_output_signature=tf.RaggedTensorSpec([None], dtype=tf.string),
    )  # 이 부분은 더 편하게 바꿀 방법이 있을 것 같다.

    zeros = tf.cast(tf.repeat(0, tf.size(starts)), starts.dtype)
    starts = tf.strings.length(x.with_flat_values(tf.strings.substr(x.values, zeros, starts.values)), unit='UTF8_CHAR')
    ends = tf.strings.length(x.with_flat_values(tf.strings.substr(x.values, zeros, ends.values)), unit='UTF8_CHAR')
    return tokens, starts, ends
```

문자열에서 starts, ends까지 substring후 length를 세는 방식으로 작성했다.

이렇게 사용하는 이유는 CJK에서 NER 같은 문제를 풀려할 때 오프셋이 안 맞을 때가 있기 때문이다. <https://www.tensorflow.org/text/api_docs/python/text/SplitterWithOffsets#split_with_offsets>를 보면 알 수 있지만, `split_with_offsets`은 bytes indices를 반환한다.

위 코드에서 `tokenize_with_offsets`로 쓴 이유는 saved model을 그렇게 뽑아놓아서..
