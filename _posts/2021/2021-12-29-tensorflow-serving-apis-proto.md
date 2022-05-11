---
layout: post
title: "Writing gRPC client for TensorFlow Serving in other languages (golang)"
tags:
  - bazel
  - tensorflow
  - golang
---

With TensorFlow-Serving, we can use the well-optimized server for machine learning models in production. However, it is a little bit hard to develop gRPC clients for other languages except for python and C++. So I want to let you know how I implemented the gRPC client in other languages for TensorFlow Serving. In this post, I will use golang and TensorFlow-Serving 2.7.

If you want just codes, check this links.

* <https://github.com/jeongukjae/chips/tree/main/tfs-go-client-example>
* <https://github.com/jeongukjae/tensorflow-serving-apis-proto>

## Prepare example `SavedModel` files

To write a sample client in golang, we first have to prepare example `SavedModel` to serve. I copied `SavedModel` from [TensorFlow-Serving's test cases (`tensorflow_serving/servables/tensorflow/testdata`)](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/servables/tensorflow/testdata).

## Pull protobuf files

### TensorFlow Serving APIs

TensorFlow Serving provides APIs in [this path (`tensorflow_serving/apis`)](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/apis) via protobuf files. We pull those files and other imported files from `tensorflow/serving` repository.

```sh
function fetchTFSApi() {
    mkdir -p $TMP/tensorflow-serving
    pushd $TMP/tensorflow-serving

    curl -LS -o serving.zip https://github.com/tensorflow/serving/archive/$TFS_VERSION.zip
    unzip -q serving.zip

    mkdir -p $1/tensorflow_serving
    rsync -r --include="*.proto" --exclude="*" serving-$TFS_VERSION/tensorflow_serving/apis/ $1/tensorflow_serving/apis/
    rsync -r --include="*.proto" --exclude="*" serving-$TFS_VERSION/tensorflow_serving/config/ $1/tensorflow_serving/config/

    popd
}
```

### TensorFlow Core Protos

Because TensorFlow Serving APIs require TensorFlow core's protobuf files, we also have to pull files from `tensorflow/tensorflow` repository.

```sh
function fetchTFProto() {
    mkdir -p $TMP/tensorflow
    pushd $TMP/tensorflow

    curl -LS -o tf.zip https://github.com/tensorflow/tensorflow/archive/v$TF_VERSION.zip
    unzip -q tf.zip

    mkdir -p $1/tensorflow/core
    rsync -r --include="*.proto" --exclude="*" tensorflow-$TF_VERSION/tensorflow/core/framework/ $1/tensorflow/core/framework/
    rsync -r --include="*.proto" --exclude="*" tensorflow-$TF_VERSION/tensorflow/core/example/ $1/tensorflow/core/example/
    rsync -r --include="*.proto" --exclude="*" tensorflow-$TF_VERSION/tensorflow/core/protobuf/ $1/tensorflow/core/protobuf/

    popd
}
```

### Remove unnecessary protobuf files

Since Tensorflow's protobufs are not all necessary, I pruned it with simple python script. Since the script is about 50 lines long, I'm not pasting the code here, just [a link](https://github.com/jeongukjae/tensorflow-serving-apis-proto/blob/main/prune_protos.py).

### Update `go_package` path

It is okay to just compile those files, but I love to use Bazel, so I updated all `go_package` options in TensorFlow cores. Since all protobuf files have unique paths, we have to manually set all `importmap` options in [`go_proto_library`](https://github.com/bazelbuild/rules_go/blob/master/proto/core.rst#go_proto_library) to use them with bazel. So I updated `go_package` option not to set `importmap` options.

```sh
for file in tensorflow/core/**/*.proto ; do
    sed -i '' -E 's/(option go_package.+)\/[^\/]+";/\1";/' $file
done
```

For example, this script updates `tensorflow/core/example/example.proto` like below.

```diff
diff --git a/tensorflow/core/example/example.proto b/tensorflow/core/example/example.proto
index a6251de..0b49514 100644
--- a/tensorflow/core/example/example.proto
+++ b/tensorflow/core/example/example.proto
@@ -10,7 +10,7 @@ option cc_enable_arenas = true;
 option java_outer_classname = "ExampleProtos";
 option java_multiple_files = true;
 option java_package = "org.tensorflow.example";
-option go_package = "github.com/tensorflow/tensorflow/tensorflow/go/core/example/example_protos_go_proto";
+option go_package = "github.com/tensorflow/tensorflow/tensorflow/go/core/example";
```

## Add sample client code

Then we can write our starlark codes and build our sample client for TensorFlow Serving like below.

```golang
package main

import (
    "context"
    "encoding/json"
    "log"
    "time"

    "google.golang.org/grpc"

    tfs_api_pb "github.com/tensorflow/serving/tensorflow_serving/apis"
    tf_framework "github.com/tensorflow/tensorflow/tensorflow/go/core/framework"
)

const (
    HOST                 = "0.0.0.0:8500"
    MODEL_NAME           = "half_plus_two"
    MODEL_SIGNATURE_NAME = "serving_default"
)

func main() {
    conn, err := grpc.Dial(HOST, grpc.WithInsecure())
    if err != nil {
        log.Fatalf("did not connect: %v", err)
    }
    defer conn.Close()

    c := tfs_api_pb.NewPredictionServiceClient(conn)

    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()
    predictRequest := tfs_api_pb.PredictRequest{
        ModelSpec: &tfs_api_pb.ModelSpec{
            Name:          MODEL_NAME,
            SignatureName: MODEL_SIGNATURE_NAME,
        },
        Inputs: map[string]*tf_framework.TensorProto{
            "x": &tf_framework.TensorProto{
                Dtype: tf_framework.DataType_DT_FLOAT,
                TensorShape: &tf_framework.TensorShapeProto{
                    Dim: []*tf_framework.TensorShapeProto_Dim{
                        {
                            Size: 1,
                        },
                        {
                            Size: 3,
                        },
                    },
                },
                FloatVal: []float32{
                    1.0, 2.0, 5.0,
                },
            },
        },
    }

    for key, value := range predictRequest.Inputs {
        log.Printf("Input %s", key)

        for _, element := range value.FloatVal {
            log.Printf("\t%f", element)
        }
    }

    predictResponse, err := c.Predict(ctx, &predictRequest)
    if err != nil {
        log.Fatalf("could not get response: %v", err)
    }

    jsonResponse, err := json.Marshal(predictResponse)
    if err != nil {
        log.Fatalf("could not marshal: %v", err)
    }
    log.Printf("Response: %s", jsonResponse)
}
```

For the details(`BUILD` or `WORKSPACE` files), check out this link (<https://github.com/jeongukjae/chips/tree/main/tfs-go-client-example>).

And we prepared all we need. Start a TF Serving server and run sample client like below.

```sh
$ docker run -d --rm -p 8500:8500 \
    -v "$(pwd)/example_model:/models/:ro" \
    -e MODEL_NAME=half_plus_two \
    tensorflow/serving
5a4443554baec51b945881d42edf7bef2bf26671b8bdd33eae06c23b0c3d5ea1
$ bazel run //:main
INFO: Analyzed target //:main (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:main up-to-date:
  bazel-bin/main_/main
INFO: Elapsed time: 0.296s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Build completed successfully, 1 total action
2021/12/29 18:07:28 Input x
2021/12/29 18:07:28     1.000000
2021/12/29 18:07:28     2.000000
2021/12/29 18:07:28     5.000000
2021/12/29 18:07:28 Response: {"model_spec":{"name":"half_plus_two","VersionChoice":{"Version":{"value":123}},"signature_name":"serving_default"},"outputs":{"y":{"dtype":1,"tensor_shape":{"dim":[{"size":1},{"size":3}]},"float_val":[2.5,3,4.5]}}}
2021/12/29 18:07:28 Output y
2021/12/29 18:07:28     2.500000
2021/12/29 18:07:28     3.000000
2021/12/29 18:07:28     4.500000
```
