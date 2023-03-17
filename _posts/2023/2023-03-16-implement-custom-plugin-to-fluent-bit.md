---
layout: post
title: "Implement a custom C/C++ DSO plugin for Fluent Bit"
tags:
    - c++
---

[Fluent Bit](https://github.com/fluent/fluent-bit) is a widely used, fast and lightweight processor for logs and metrics, written in C and offering a rich set of plugins for collecting, parsing, and forwarding logs and metrics. Despite its versatility, however, there are still scenarios that may not be covered by the existing plugins, such as the need to filter or map records based on custom logic.

In this post, I'll share my experience of implementing a custom C/C++ DSO plugin for Fluent Bit to address my particular use case. This will be of interest to software engineers looking to extend the functionality of Fluent Bit.

This post is based on Fluent Bit v2.0.x, and all the code discussed here is available at [jeongukjae/flb-plugin-sample](https://github.com/jeongukjae/flb-plugin-sample).

## What is a DSO plugin?

DSO stands for Dynamic Shared Object., and it can be dynamically loaded by Fluent Bit at runtime.
The interface of a DSO plugin is not well-documented, but you can find some examples and related documentation and code in the following resources:

* [Plugin API Section in Developer Guide - Fluent Bit Docs](https://docs.fluentbit.io/manual/development/developer-guide#plugin-api)
    > Each plugin is a shared object which is loaded into Fluent Bit using `dlopen` and `dlsym`.
* [Function that registers a plugin - GitHub](https://github.com/fluent/fluent-bit/blob/2.0/src/flb_plugin.c#L189-L297)

## Implement a custom C DSO plugin

Let's begin by creating a simple C/C++ DSO plugin.

### Bring the plugin interface header file

To build the project, Fluent Bit uses [CMake](https://cmake.org/).
However, in version 2.0.x, the installation of Fluent Bit as a library is broken, as noted in this related issue: [fluent/fluent-bit#7028](https://github.com/fluent/fluent-bit/issues/7028).
Because the plugin is loaded dynamically at runtime with `dlopen` and `dlsym`, it is enough to have the same structure and function signatures as the original plugin.
To accomplish this, copy the `struct flb_filter_plugin` from `include/fluent-bit/flb_filter.h` and related functions to your project.

```c++
#ifndef __FLUENT_BIT_FLB_FILTER_H__
#define __FLUENT_BIT_FLB_FILTER_H__

// This is the simplified filter plugin interface. The original is in
// https://github.com/fluent/fluent-bit/blob/master/include/fluent-bit/flb_filter.h

#include <cstdlib>

#include "fluentbit/flb_config.h"

#define FLB_FILTER_MODIFIED 1
#define FLB_FILTER_NOTOUCH  2

struct flb_filter_plugin {
  int flags;         /* Flags (not available at the moment */
  char *name;        /* Filter short name            */
  char *description; /* Description                  */

  /* Config map */
  struct flb_config_map *config_map;

  /* Callbacks */
  int (*cb_init)(struct flb_filter_instance *, struct flb_config *, void *);
  int (*cb_filter)(const void *, size_t, const char *, int, void **, size_t *,
                   struct flb_filter_instance *, struct flb_input_instance *,
                   void *, struct flb_config *);
  int (*cb_exit)(void *, struct flb_config *);

  struct mk_list _head; /* Link to parent list (config->filters) */
};

#endif  // __FLUENT_BIT_FLB_FILTER_H__
```

As you can see, the plugin interface is simple and easy to understand.

### Implement the plugin interface

Now that the plugin interface is ready, we can implement it.
In my use case, I want to implement a filter plugin.
Therefore, I copied and modified the `stdout` filter plugin from the original source code.
Additionaly, I added dependencies on [msgpack-c](https://github.com/msgpack/msgpack-c) and [spdlog](https://github.com/gabime/spdlog) for the convenience of marshal/unmarshal and logging.

```c++
#include <cstdio>
#include <iostream>

#include "fluentbit/flb_config.h"
#include "fluentbit/flb_filter.h"
#include "fluentbit/flb_time.h"
#include "msgpack.hpp"
#include "spdlog/spdlog.h"

static int cb_stdout_init(struct flb_filter_instance *f_ins,
                          struct flb_config *config, void *data) {
  spdlog::set_pattern("[%Y/%m/%d %H:%M:%S] [%5!l] [stdout_cxx] %v");
  spdlog::info("Initializing stdout_cxx filter plugin");

  return 0;
}

static int cb_stdout_filter(const void *data, size_t bytes, const char *tag,
                            int tag_len, void **out_buf, size_t *out_bytes,
                            struct flb_filter_instance *f_ins,
                            struct flb_input_instance *i_ins,
                            void *filter_context, struct flb_config *config) {
  size_t off = 0;
  size_t cnt = 0;

  std::string tag_string(tag, tag_len);

  while (off != bytes) {
    msgpack::object_handle result =
        msgpack::unpack(static_cast<const char *>(data), bytes, off);

    msgpack::object deserialized = result.get();
    if (deserialized.type != msgpack::type::ARRAY) {
      spdlog::error("Unexpected type: {}", deserialized.type);
      return FLB_FILTER_NOTOUCH;
    }
    msgpack::object timeobj = deserialized.via.array.ptr[0];
    msgpack::object record = deserialized.via.array.ptr[1];

    flb_time time;
    if (flb_time_msgpack_to_time(time, timeobj) != 0) {
      spdlog::error("Failed to parse time");
      return FLB_FILTER_NOTOUCH;
    }

    std::cout << "[" << cnt++ << "] " << tag_string << ": [" << time.tm.tv_sec
              << "." << time.tm.tv_nsec << ", " << record << "]" << std::endl;
  }

  return FLB_FILTER_NOTOUCH;
}

static struct flb_config_map config_map[] = {
    /* EOF */
    {0}};

struct flb_filter_plugin filter_stdout_cxx_plugin = {
    .flags = 0,
    .name = "stdout_cxx",
    .description = "Filter events to STDOUT",
    .config_map = config_map,
    .cb_init = cb_stdout_init,
    .cb_filter = cb_stdout_filter,
    .cb_exit = NULL};
```

As you can see, this plugin initializes the spdlog logger in `cb_stdout_init` and prints the records to stdout in `cb_stdout_filter`. Since Fluent Bit loads the plugin with `dlsym`, it is necessary to have the global variable `filter_{PLUGIN_NAME}_plugin` with the type `struct flb_filter_plugin`. In this case, the plugin name is `stdout_cxx`, so the global variable name is `filter_stdout_cxx_plugin`.

### Build the plugin

To build the plugin, we will be using the build tool called Bazel.
We can define build rules easily and explicitly with Bazel.

Here, we will create a `BUILD.bazel` file to build the shared library for our plugin.

```python
package(default_visibility = ["//visibility:public"])

cc_library(
    name = "filter_stdout_cxx_lib",
    alwayslink = True,
    srcs = ["stdout_cxx.cc"],
    deps = [
        "//fluentbit",
        "@msgpack",
        "@spdlog",
    ],
)

cc_binary(
    name = "filter_stdout_cxx_shared",
    deps = [":filter_stdout_cxx_lib"],
    linkshared = True,
)

genrule(
   name = "filter_stdout_cxx",
   srcs = [":filter_stdout_cxx_shared"],
   outs = ["flb-filter_stdout_cxx.so"],
   cmd = "cp $(location :filter_stdout_cxx_shared) $(location flb-filter_stdout_cxx.so)",
)
```

I built a shared library with `cc_binary` and copied it to the output file with `genrule` to match the C DSO plugin name format (ref: [fluent-bit/src/flb_plugin.c](https://github.com/fluent/fluent-bit/blob/eb70ee72edfedc66afb038e1ce323469fd44457e/src/flb_plugin.c#L306-L313)).

The rest of the build files can be found in [jeongukjae/flb-plugin-sample](https://github.com/jeongukjae/flb-plugin-sample) like following.

* [WOKSPACE.bazel](https://github.com/jeongukjae/flb-plugin-sample/blob/main/WORKSPACE.bazel)
* [fluentbit/BUILD.bazel](https://github.com/jeongukjae/flb-plugin-sample/blob/main/fluentbit/BUILD.bazel)

Finally, I can build the plugin with the following command.

```bash
bazel build //plugins/filter_stdout_cxx
```

### Dockerize the plugin

```dockerfile
FROM ubuntu:20.04 as base_build

RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG BAZELISK_VERSION=1.16.0
ARG BAZELISK_ARCH=amd64

RUN curl -LO https://github.com/bazelbuild/bazelisk/releases/download/v${BAZELISK_VERSION}/bazelisk-linux-${BAZELISK_ARCH} && \
    chmod +x bazelisk-linux-${BAZELISK_ARCH} && \
    mv bazelisk-linux-${BAZELISK_ARCH} /usr/local/bin/bazel

WORKDIR /app
COPY . .
RUN bazel build //plugins

FROM fluent/fluent-bit:2.0 as fluent_bit

COPY --from=base_build /app/bazel-bin/plugins/filter_stdout_cxx/flb-filter_stdout_cxx.so /fluent-bit/

ENTRYPOINT ["/fluent-bit/bin/fluent-bit", \
    "-e", "/fluent-bit/flb-filter_stdout_cxx.so"]
```

Dockerfile is pretty simple.
It installs `bazelisk` (launcher for bazel) and build dependencies.
Then, it builds the plugin with bazel and copy the plugin to the fluent bit image.

## Result

I can run the plugin in docker image with the following command.

```bash
$ docker build -t flb-plugin-sample .
$ docker run --rm -it flb-plugin-sample -i cpu -F stdout_cxx -m '*'
Fluent Bit v2.0.9
* Copyright (C) 2015-2022 The Fluent Bit Authors
* Fluent Bit is a CNCF sub-project under the umbrella of Fluentd
* https://fluentbit.io

[2023/03/10 15:53:10] [ info] [fluent bit] version=2.0.9, commit=4c0ca4fc5f, pid=1
[2023/03/10 15:53:10] [ info] [storage] ver=1.4.0, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2023/03/10 15:53:10] [ info] [cmetrics] version=0.5.8
[2023/03/10 15:53:10] [ info] [ctraces ] version=0.2.7
[2023/03/10 15:53:10] [ info] [input:cpu:cpu.0] initializing
[2023/03/10 15:53:10] [ info] [input:cpu:cpu.0] storage_strategy='memory' (memory only)
[2023/03/10 15:53:10] [ info] [stdout_cxx] Initializing stdout_cxx filter plugin
[2023/03/10 15:53:10] [ info] [sp] stream processor started
[0] cpu.0: [1678463590.275378839, {"cpu_p":0,"user_p":0,"system_p":0,"cpu0.p_cpu":0,"cpu0.p_user":0,"cpu0.p_system":0,"cpu1.p_cpu":0,"cpu1.p_user":0,"cpu1.p_system":0,"cpu2.p_cpu":0,"cpu2.p_user":0,"cpu2.p_system":0,"cpu3.p_cpu":0,"cpu3.p_user":0,"cpu3.p_system":0,"cpu4.p_cpu":0,"cpu4.p_user":0,"cpu4.p_system":0,"cpu5.p_cpu":0,"cpu5.p_user":0,"cpu5.p_system":0,"cpu6.p_cpu":0,"cpu6.p_user":0,"cpu6.p_system":0,"cpu7.p_cpu":0,"cpu7.p_user":0,"cpu7.p_system":0}]
[0] cpu.0: [1678463591.276133756, {"cpu_p":0.125,"user_p":0,"system_p":0.125,"cpu0.p_cpu":0,"cpu0.p_user":0,"cpu0.p_system":0,"cpu1.p_cpu":0,"cpu1.p_user":0,"cpu1.p_system":0,"cpu2.p_cpu":0,"cpu2.p_user":0,"cpu2.p_system":0,"cpu3.p_cpu":0,"cpu3.p_user":0,"cpu3.p_system":0,"cpu4.p_cpu":1,"cpu4.p_user":1,"cpu4.p_system":0,"cpu5.p_cpu":0,"cpu5.p_user":0,"cpu5.p_system":0,"cpu6.p_cpu":0,"cpu6.p_user":0,"cpu6.p_system":0,"cpu7.p_cpu":0,"cpu7.p_user":0,"cpu7.p_system":0}]
[0] cpu.0: [1678463592.278890923, {"cpu_p":0.25,"user_p":0.125,"system_p":0.125,"cpu0.p_cpu":0,"cpu0.p_user":0,"cpu0.p_system":0,"cpu1.p_cpu":0,"cpu1.p_user":0,"cpu1.p_system":0,"cpu2.p_cpu":0,"cpu2.p_user":0,"cpu2.p_system":0,"cpu3.p_cpu":0,"cpu3.p_user":0,"cpu3.p_system":0,"cpu4.p_cpu":0,"cpu4.p_user":0,"cpu4.p_system":0,"cpu5.p_cpu":0,"cpu5.p_user":0,"cpu5.p_system":0,"cpu6.p_cpu":0,"cpu6.p_user":0,"cpu6.p_system":0,"cpu7.p_cpu":0,"cpu7.p_user":0,"cpu7.p_system":0}]
[0] cpu.0: [1678463593.280610299, {"cpu_p":0,"user_p":0,"system_p":0,"cpu0.p_cpu":0,"cpu0.p_user":0,"cpu0.p_system":0,"cpu1.p_cpu":0,"cpu1.p_user":0,"cpu1.p_system":0,"cpu2.p_cpu":0,"cpu2.p_user":0,"cpu2.p_system":0,"cpu3.p_cpu":0,"cpu3.p_user":0,"cpu3.p_system":0,"cpu4.p_cpu":0,"cpu4.p_user":0,"cpu4.p_system":0,"cpu5.p_cpu":1,"cpu5.p_user":0,"cpu5.p_system":1,"cpu6.p_cpu":0,"cpu6.p_user":0,"cpu6.p_system":0,"cpu7.p_cpu":0,"cpu7.p_user":0,"cpu7.p_system":0}]
...
^C[2023/03/10 15:53:29] [engine] caught signal (SIGINT)
[2023/03/10 15:53:29] [ warn] [engine] service will shutdown in max 5 seconds
[2023/03/10 15:53:29] [ info] [input] pausing cpu.0
[2023/03/10 15:53:30] [ info] [engine] service has stopped (0 pending tasks)
[2023/03/10 15:53:30] [ info] [input] pausing cpu.0
```

In the above example, the `cpu` input plugin is used to collect dummy input records, and `stdout_cxx` filter plugin is used to print the records to the standard output.

`stdout_cxx` plugin is installed successfully!! 🎉

## Conclusion

I know this is a little bit tricky to use, and may not be guaranteed to work in the future.
But I hope this helps someone who wants to use Fluent Bit with C++ plugins.
Custom filter plugins are supported by [WASM filter](https://docs.fluentbit.io/manual/development/wasm-filter-plugins), but in my case, I couldn't use WASM filter plugin since the dependencies that I want to use are not supported by WASM environment.
(Specifically, I want to use Protocol Buffers in WASM environment with Go, but it's not supported yet)
