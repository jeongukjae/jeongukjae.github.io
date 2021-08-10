---
layout: post
title: "SchemaGen의 결과물로부터 FeatureSpec을 얻는 방법"
tags:
    - python
    - tensorflow
---

TFX를 사용하면서 가끔 빠르게 실험해보고 싶은 것이 생길경우 간단한 스크립트 성으로 코드를 작성하는데, 그때 유용한 팁정도이다.

TFX를 자주 사용하면 보통 `ExampleGen`, `StatisticsGen`, `SchemaGen`의 순서로 뽑아내면서, TFRecord Serialize를 직접할 필요도 없고, TFRecord를 deserialize하기 위한 Feature Spec도 직접 작성할 필요가 없어서 보통 넘어오는 대로 사용한다. 그래도 언젠가 대충 코드를 짜서 실험해보고 싶은 마음이 생길 때가 있어서 SchemaGen을 가져올 방법이 필요하다.

`.pbtxt` 파일 형태라서 급하면 text editor로 열어서 옮겨도, 아니면 protobuf로 읽어서 변환해도 되는데 아래 방법이 편해서, 아래처럼 사용한다.

```python
from tensorflow_transform.tf_metadata import schema_utils
from tfx.utils import io_utils

schmea_gen_artifact_path = "pipline_root/schemagen-id/schema/version/schema.pbtxt"
schema_reader = io_utils.SchemaReader()
schema_pb = schema_reader.read(schmea_gen_artifact_path)
feature_spec = schema_utils.schema_as_feature_spec(schema_pb).feature_spec
```

이걸 `tfx.utils.io_utils`나 `tfx.types.artifact_utils`와 함께 사용하면 아래처럼 schema_gen artifact로부터 직접 얻어오는 것도 가능하다.

```python
from tensorflow_transform.tf_metadata import schema_utils
from tfx.types import artifact_utils
from tfx.utils import io_utils

schema_reader = io_utils.SchemaReader()
schema_pb = schema_reader.read(io_utils.get_only_uri_in_dir(artifact_utils.get_single_uri([schema])))
feature_spec = schema_utils.schema_as_feature_spec(schema_pb).feature_spec
```

사실 이게 TFX Trainer를 작성하다보면 자주 보게되는 `run_fn`의 인자를 사용하는 `tfx.components.trainer.fn_args_utils.FnArgs.data_accessor.tf_dataset_factory`에서 하는 일이긴 하다.

---

조금만 더 응용해보면 아래처럼 pipeline root, artifact id를 받아서 데이터셋을 읽어오는 함수도 작성해놓고 쓸 수 있다. (종종 그렇게 쓴다)

```python
import os

import tensorflow as tf
from tensorflow_transform.tf_metadata import schema_utils
from tfx.utils import io_utils


def read_dataset(
    pipeline_root: str,
    example_gen_id: str,
    schema_gen_id: str,
    shuffle_buffer_size: int = 100_000,
    split: str = "train",
) -> tf.data.Dataset:
    # read feature spec from SchemaGen
    schema_gen_dir = os.path.join(pipeline_root, schema_gen_id, "schema")
    schema_uri = os.path.join(schema_gen_dir, _get_latest(schema_gen_dir), "schema.pbtxt")
    schema_reader = io_utils.SchemaReader()
    schema_pb = schema_reader.read(schema_uri)
    feature_spec = schema_utils.schema_as_feature_spec(schema_pb).feature_spec

    # read examples
    examples_dir = os.path.join(pipeline_root, example_gen_id, "examples")
    examples = os.path.join(examples_dir, _get_latest(examples_dir), f"Split-{split}", "*.gz")
    dataset = (
        tf.data.Dataset.list_files(examples, shuffle=True)
        .interleave(lambda filename: tf.data.TFRecordDataset(filename, compression_type="GZIP"))
        .map(lambda x: tf.io.parse_single_example(x, feature_spec), num_parallel_calls=tf.data.AUTOTUNE)
        .shuffle(shuffle_buffer_size)
    )
    return dataset


def _get_latest(base_path: str) -> str:
    latest_version = sorted([int(v) for v in os.listdir(base_path)], reverse=True)[0]
    return str(latest_version)
```

간단한 코드지만, 여기에 여러가지 옵션 붙이고 I/O 바꿔서 자동으로 tf.string dtype들을 가져와서 sentencepiece train 시킨다거나 할 수도 있고, 나름 TFX Custom Component 만들 때 이런 식으로 유용하게 사용했다.
