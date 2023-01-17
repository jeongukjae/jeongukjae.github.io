---
layout: post
title: "Enabling S3 Filesystem Support for TensorFlow Serving"
tags:
    - tensorflow
    - bazel
---

Since version 2.7, TensorFlow's filesystem support for S3 and HDFS is migrated to the Modular File System ([RFC link](https://github.com/tensorflow/community/blob/master/rfcs/20190506-filesystem-plugin-modular-tensorflow.md)), and moved S3 filesystem implementation to [tensorflow-io](https://github.com/tensorflow/io) project.
In the python environment, it was easy to install and use tensorflow-io, but not in the C++ environment.
So I struggled to operate TensorFlow Serving in AWS workloads because I couldn't use the S3 filesystem.
That was a big problem for me, so I tried to build TensorFlow Serving with tensorflow-io.
And here is the result.

*This post is written based on TensorFlow and TF-Serving 2.11.0 and TF-IO 0.29.0.*

## TOC <!-- omit in toc -->

- [Background](#background)
- [Modular File System and TensorFlow IO](#modular-file-system-and-tensorflow-io)
- [Let's build](#lets-build)
  - [First, load all dependencies](#first-load-all-dependencies)
  - [Add S3 plugin](#add-s3-plugin)
  - [Link S3 plugin](#link-s3-plugin)
  - [Add build rules](#add-build-rules)
  - [Build model server](#build-model-server)
- [Test S3 filesystem](#test-s3-filesystem)
- [All codes and images](#all-codes-and-images)

**If you want to check the codes and docker images first, check [All codes and images](#all-codes-and-images) section.**

## Background

I reported [an issue (tensorflow/serving#1963)](https://github.com/tensorflow/serving/issues/1963) to TensorFlow Serving's GitHub repository, and I'm waiting for the official support for S3 filesystem.
But a few days ago, I noticed that S3 support in TensorFlow ecosystem is not maintained by TensorFlow team, but by the community in the [TensorFlow IO project](https://github.com/tensorflow/io).
So I decided to try to build and share how to build TensorFlow Serving with TensorFlow IO.

## Modular File System and TensorFlow IO

Filesystem of TensorFlow is modularized since version 2.7, so you can build a plugin to support arbitrary filesystem by following the Modular File System Interface.
The interface is defined in [tensorflow/c/experimental/filesystem/filesystem_interface.h](https://github.com/tensorflow/tensorflow/tree/r2.11/tensorflow/c/experimental/filesystem/filesystem_interface.h),
and the registration can be done in `void TF_InitPlugin(TF_FilesystemPluginInfo* plugin_info)` function that you implemented in your plugin. (For more details, check this [comment](https://github.com/tensorflow/tensorflow/blob/r2.11/tensorflow/c/experimental/filesystem/filesystem_interface.h#L1100-L1119))

The S3 plugin is already implemented in tensorflow-io project with the Modular File System Interface in [tensorflow_io/core/filesystems/s3](https://github.com/tensorflow/io/tree/v0.29.0/tensorflow_io/core/filesystems/s3).
So all we need to do is to build TensorFlow Serving with tensorflow-io and `aws-sdk-cpp` as dependencies.

## Let's build

### First, load all dependencies

All deps are declared in `WORKSPACE` file and `third_party` directory in tensorflow-io, so we can use them by copying the desired deps to `WORKSPACE` file in TensorFlow Serving. (Technically, TensorFlow Serving manages its own deps in `tensorflow_serving/workspace.bzl` file, and load them in `WORKSPACE` file, but it's not a big deal.)

```diff
diff --git a/tensorflow_serving/workspace.bzl b/tensorflow_serving/workspace.bzl
index 251174a5..6837ce5f 100644
--- a/tensorflow_serving/workspace.bzl
+++ b/tensorflow_serving/workspace.bzl
@@ -129,3 +129,61 @@ def tf_serving_workspace():
         recursive_init_submodules = True,
         remote = "https://github.com/boostorg/boost",
     )
+
+    # ==== TensorFlow IO ====
+    http_archive(
+        name = "org_tensorflow_io",
+        strip_prefix = "io-0.29.0",
+        sha256 = "a11235b83e1f695e2796128a25cf7881134d22c63f71a41ba729049912434fc9",
+        url = "https://github.com/tensorflow/io/archive/v0.29.0.zip",
+        patches = ["@//third_party/tfio:tfio.patch"],
+        patch_args = ["-p1"],
+    )
+
+    http_archive(
+        name = "aws-checksums",
+        build_file = "//third_party:aws-checksums.BUILD",
+        sha256 = "6e6bed6f75cf54006b6bafb01b3b96df19605572131a2260fddaf0e87949ced0",
+        strip_prefix = "aws-checksums-0.1.5",
+        urls = [
+            "https://storage.googleapis.com/mirror.tensorflow.org/github.com/awslabs/aws-checksums/archive/v0.1.5.tar.gz",
+            "https://github.com/awslabs/aws-checksums/archive/v0.1.5.tar.gz",
+        ],
+    )
+
+    http_archive(
+        name = "aws-c-common",
+        build_file = "//third_party:aws-c-common.BUILD",
+        sha256 = "01c2a58553a37b3aa5914d9e0bf7bf14507ff4937bc5872a678892ca20fcae1f",
+        strip_prefix = "aws-c-common-0.4.29",
+        urls = [
+            "https://storage.googleapis.com/mirror.tensorflow.org/github.com/awslabs/aws-c-common/archive/v0.4.29.tar.gz",
+            "https://github.com/awslabs/aws-c-common/archive/v0.4.29.tar.gz",
+        ],
+    )
+
+    http_archive(
+        name = "aws-c-event-stream",
+        build_file = "//third_party:aws-c-event-stream.BUILD",
+        sha256 = "31d880d1c868d3f3df1e1f4b45e56ac73724a4dc3449d04d47fc0746f6f077b6",
+        strip_prefix = "aws-c-event-stream-0.1.4",
+        urls = [
+            "https://storage.googleapis.com/mirror.tensorflow.org/github.com/awslabs/aws-c-event-stream/archive/v0.1.4.tar.gz",
+            "https://github.com/awslabs/aws-c-event-stream/archive/v0.1.4.tar.gz",
+        ],
+    )
+
+    http_archive(
+        name = "aws-sdk-cpp",
+        build_file = "//third_party:aws-sdk-cpp.BUILD",
+        patch_cmds = [
+            """sed -i.bak 's/UUID::RandomUUID/Aws::Utils::UUID::RandomUUID/g' aws-cpp-sdk-core/source/client/AWSClient.cpp""",
+            """sed -i.bak 's/__attribute__((visibility("default")))//g' aws-cpp-sdk-core/include/aws/core/external/tinyxml2/tinyxml2.h """,
+        ],
+        sha256 = "749322a8be4594472512df8a21d9338d7181c643a00e08a0ff12f07e831e3346",
+        strip_prefix = "aws-sdk-cpp-1.8.186",
+        urls = [
+            "https://storage.googleapis.com/mirror.tensorflow.org/github.com/aws/aws-sdk-cpp/archive/1.8.186.tar.gz",
+            "https://github.com/aws/aws-sdk-cpp/archive/1.8.186.tar.gz",
+        ],
+    )
```

You can see the `build_file` options in the deps.
They are copied from `third_party` directory in tensorflow-io.
You also have to patch `org_tensorflow_io` since tensorflow-io loads TensorFlow from installed Python package (maybe pip package), but TensorFlow Serving loads TensorFlow from source code.
So delete the lines related to `@local_config_tf`, and add deps using `@org_tensorflow` instead.

```diff
diff --git a/tensorflow_io/core/filesystems/BUILD b/tensorflow_io/core/filesystems/BUILD
index 9276208f..204d2740 100644
--- a/tensorflow_io/core/filesystems/BUILD
+++ b/tensorflow_io/core/filesystems/BUILD
@@ -11,18 +11,13 @@ cc_library(
     name = "filesystem_plugins_header",
     srcs = [
         "filesystem_plugins.h",
-    ] + select({
-        "@bazel_tools//src/conditions:windows": [
-            "@local_config_tf//:stub/libtensorflow_framework.lib",
-        ],
-        "//conditions:default": [
-            "@local_config_tf//:stub/libtensorflow_framework.so",
-        ],
-    }),
+    ],
     copts = tf_io_copts(),
     linkstatic = True,
     deps = [
-        "@local_config_tf//:tf_c_header_lib",
+        "@org_tensorflow//tensorflow/c:c_api_macros",
+        "@org_tensorflow//tensorflow/c:logging",
+        "@org_tensorflow//tensorflow/c/experimental/filesystem:modular_filesystem",
     ],
     alwayslink = 1,
 )
```

### Add S3 plugin

And now we can connect the S3 implementation to TensorFlow Serving.
I added the following small code to `tensorflow_serving/model_servers` directory to load the S3 plugin.

```c++
// tensorflow_serving/model_servers/filesystem/s3_adapter.h
#ifndef TENSORFLOW_SERVING_MODEL_SERVERS_FILESYSTEM_S3_ADAPTER_H_
#define TENSORFLOW_SERVING_MODEL_SERVERS_FILESYSTEM_S3_ADAPTER_H_

#include "tensorflow/c/experimental/filesystem/filesystem_interface.h"

void TF_InitPlugin(TF_FilesystemPluginInfo* info);

namespace tensorflow {
namespace io {

// Copied from tensorflow_io/core/filesystems/filesystem_plugins.h.
static void* plugin_memory_allocate(size_t size) { return calloc(1, size); }
static void plugin_memory_free(void* ptr) { free(ptr); }

namespace s3 {

// This function is defined in
// tensorflow_io/core/filesystems/s3/s3_filesystem.cc. It is not exposed in
// tensorflow_io/core/filesystems/s3/s3_filesystem.h, so we need to declare it
// here.
void ProvideFilesystemSupportFor(TF_FilesystemPluginOps* ops, const char* uri);

}  // namespace s3
}  // namespace io
}  // namespace tensorflow

#endif  // TENSORFLOW_SERVING_MODEL_SERVERS_FILESYSTEM_S3_ADAPTER_H_
```

```c++
// tensorflow_serving/model_servers/filesystem/s3_adapter.cc
#include "tensorflow_serving/model_servers/filesystem/s3_adapter.h"

#include <stdlib.h>

#include "tensorflow/c/experimental/filesystem/filesystem_interface.h"
#include "tensorflow_io/core/filesystems/s3/s3_filesystem.h"

void TF_InitPlugin(TF_FilesystemPluginInfo* info) {
  info->plugin_memory_allocate = tensorflow::io::plugin_memory_allocate;
  info->plugin_memory_free = tensorflow::io::plugin_memory_free;

  info->num_schemes = 1;
  info->ops = static_cast<TF_FilesystemPluginOps*>(
      tensorflow::io::plugin_memory_allocate(info->num_schemes *
                                             sizeof(info->ops[0])));

  tensorflow::io::s3::ProvideFilesystemSupportFor(&info->ops[0], "s3");
}
```

### Link S3 plugin

I defined the S3 plugin successfully, but it is not loaded yet.
We need to load the plugin in model server code to use it, or we can statically load it.
I chose the latter, so I added the following code to `tensorflow_serving/model_servers/filesystem/s3_adapter_static.cc` to statically load the plugin.

```c++
// tensorflow_serving/model_servers/filesystem/s3_adapter_static.cc
#include "tensorflow/c/experimental/filesystem/modular_filesystem_registration.h"
#include "tensorflow_io/core/filesystems/s3/s3_filesystem.h"
#include "tensorflow_serving/model_servers/filesystem/s3_adapter.h"

namespace tensorflow {

// Register the S3 filesystems statically.
bool RegisterS3Statically() {
  TF_FilesystemPluginInfo info;
  TF_InitPlugin(&info);
  Status status = filesystem_registration::RegisterFilesystemPluginImpl(&info);
  if (!status.ok()) {
    VLOG(0) << "Static POSIX filesystem could not be registered: " << status;
    return false;
  }
  return true;
}

// Perform the actual registration
static bool unused = RegisterS3Statically();

}  // namespace tensorflow
```

### Add build rules

Now we have to add the build rules to build all the codes.

```python
# tensorflow_serving/model_servers/filesystem/BUILD
licenses(["notice"])

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "s3_adapter",
    hdrs = ["s3_adapter.h"],
    srcs = ["s3_adapter.cc"],
    linkstatic = True,
    deps = [
        "@org_tensorflow//tensorflow/c/experimental/filesystem:filesystem_interface",
        "@org_tensorflow_io//tensorflow_io/core/filesystems/s3",
    ],
    alwayslink = 1,
)

# This is a library that always links s3 filesystem.
cc_library(
    name = "s3_adapter_static",
    srcs = ["s3_adapter_static.cc"],
    linkstatic = True,
    deps = [
        ":s3_adapter",
        "@org_tensorflow//tensorflow/c/experimental/filesystem:filesystem_interface",
        "@org_tensorflow//tensorflow/c/experimental/filesystem:modular_filesystem",
        "@org_tensorflow_io//tensorflow_io/core/filesystems/s3",
    ],
    alwayslink = 1,
)
```

So finally, we can link `s3_adapter_static` to model server to use S3 filesystem.

```python
# tensorflow_serving/model_servers/BUILD
...

cc_library(
    name = "tensorflow_model_server_main_lib",
    srcs = [
        "main.cc",
    ],
    hdrs = [
        "version.h",
    ],
    linkstamp = "version.cc",
    visibility = [
        ":tensorflow_model_server_custom_op_clients",
        "//tensorflow_serving:internal",
    ],
    deps = [
        ":server_lib",
        "//tensorflow_serving/model_servers/filesystem:s3_adapter_static",  # <--- Add this line
        "@org_tensorflow//tensorflow/c:c_api",
        "@org_tensorflow//tensorflow/compiler/jit:xla_cpu_jit",
        "@org_tensorflow//tensorflow/core:lib",
        "@org_tensorflow//tensorflow/core/platform/cloud:gcs_file_system",
    ] + if_libtpu([
        "@org_tensorflow//tensorflow/core/tpu:tpu_global_init",
        "@org_tensorflow//tensorflow/core/tpu:tpu_api_dlsym_initializer",
    ]),
)

...
```

### Build model server

Now we can build the model server with S3 filesystem!
Build process is the same as of the original model server.
So, I will skip details.
I packaged the model server using Docker.

## Test S3 filesystem

I build the model server image(`ghcr.io/jeongukjae/tf-serving-s3:2.11.0`), and I uploaded a sample model (`saved_model_half_plus_three` in TensorFlow Serving repository) to my S3 bucket.
And here's the execution result.

```bash
$ docker run \
    --rm \
    -it \
    -p 8501:8501 \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION \
    -e MODEL_BASE_PATH=s3://BUCKET_NAME \
    -e MODEL_NAME=saved_model_half_plus_three \
    ghcr.io/jeongukjae/tf-serving-s3:2.11.0 \
    --file_system_poll_wait_seconds=0
2023-01-17 17:10:14.476020: I tensorflow_serving/model_servers/server.cc:74] Building single TensorFlow model file config:  model_name: saved_model_half_plus_three model_base_path: s3://BUCKET_NAME/saved_model_half_plus_three
2023-01-17 17:10:14.476373: I tensorflow_serving/model_servers/server_core.cc:465] Adding/updating models.
2023-01-17 17:10:14.476441: I tensorflow_serving/model_servers/server_core.cc:594]  (Re-)adding model: saved_model_half_plus_three
2023-01-17 17:10:16.334251: I tensorflow_serving/core/basic_manager.cc:739] Successfully reserved resources to load servable {name: saved_model_half_plus_three version: 123}
2023-01-17 17:10:16.334398: I tensorflow_serving/core/loader_harness.cc:66] Approving load for servable version {name: saved_model_half_plus_three version: 123}
2023-01-17 17:10:16.334457: I tensorflow_serving/core/loader_harness.cc:74] Loading servable version {name: saved_model_half_plus_three version: 123}
2023-01-17 17:10:16.439278: I external/org_tensorflow/tensorflow/cc/saved_model/reader.cc:45] Reading SavedModel from: s3://BUCKET_NAME/saved_model_half_plus_three/00000123
2023-01-17 17:10:16.793316: I external/org_tensorflow/tensorflow/cc/saved_model/reader.cc:89] Reading meta graph with tags { serve }
2023-01-17 17:10:16.793397: I external/org_tensorflow/tensorflow/cc/saved_model/reader.cc:130] Reading SavedModel debug info (if present) from: s3://BUCKET_NAME/saved_model_half_plus_three/00000123
2023-01-17 17:10:16.849092: I external/org_tensorflow/tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2023-01-17 17:10:16.869606: I external/org_tensorflow/tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
2023-01-17 17:10:16.871608: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:229] Restoring SavedModel bundle.
2023-01-17 17:10:17.425487: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:213] Running initialization op on SavedModel bundle at path: s3://BUCKET_NAME/saved_model_half_plus_three/00000123
2023-01-17 17:10:17.437070: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:305] SavedModel load for tags { serve }; Status: success: OK. Took 997794 microseconds.
2023-01-17 17:10:17.522369: I tensorflow_serving/servables/tensorflow/saved_model_warmup_util.cc:62] No warmup data file found at s3://BUCKET_NAME/saved_model_half_plus_three/00000123/assets.extra/tf_serving_warmup_requests
2023-01-17 17:10:19.476532: I tensorflow_serving/core/loader_harness.cc:95] Successfully loaded servable version {name: saved_model_half_plus_three version: 123}
2023-01-17 17:10:19.482374: I tensorflow_serving/model_servers/server_core.cc:486] Finished adding/updating models
2023-01-17 17:10:19.482595: I tensorflow_serving/model_servers/server.cc:118] Using InsecureServerCredentials
2023-01-17 17:10:19.482671: I tensorflow_serving/model_servers/server.cc:383] Profiler service is enabled
2023-01-17 17:10:19.486500: I tensorflow_serving/model_servers/server.cc:409] Running gRPC ModelServer at 0.0.0.0:8500 ...
[warn] getaddrinfo: address family for nodename not supported
2023-01-17 17:10:19.491998: I tensorflow_serving/model_servers/server.cc:430] Exporting HTTP/REST API at:localhost:8501 ...
[evhttp_server.cc : 245] NET_LOG: Entering the event loop ...
```

And then, I sent a request to the server.

```bash
$ curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"instances": [1.0, 2.0, 5.0]}' \
    http://localhost:8501/v1/models/saved_model_half_plus_three:predict
{
    "predictions": [3.5, 4.0, 5.5
    ]
}
```

It was successfully served! 🎉🎉🎉

## All codes and images

* All the codes are available on GitHub: <https://github.com/jeongukjae/tf-serving-s3>
* and I pushed the model server image to GitHub Container Registry: <https://github.com/jeongukjae/tf-serving-s3/pkgs/container/tf-serving-s3>
