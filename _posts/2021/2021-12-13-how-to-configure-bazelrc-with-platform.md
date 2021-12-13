---
layout: post
title: "How to configure .bazelrc with platform"
tags:
  - bazel
---

There are certain needs to configure the `.bazelrc` file with platform tags like `build:macos`. You can simply add OS-specific configurations with `--enable_platform_specific_config`[^1] like below.

```sh
build --enable_platform_specific_config

# for macOS-specific configurations
build:macos --action_env=CC
...

# for linux-specific configurations
build:macos --action_env=CXX
...

```

Also, you can find the exact platform names by OS in [these lines (ConfigExpander.java#L38-L53)](https://github.com/bazelbuild/bazel/blob/4.2.2/src/main/java/com/google/devtools/build/lib/runtime/ConfigExpander.java#L38-L53).

```java
  private static String getPlatformName() {
    switch (OS.getCurrent()) {
      case LINUX:
        return "linux";
      case DARWIN:
        return "macos";
      case WINDOWS:
        return "windows";
      case FREEBSD:
        return "freebsd";
      case OPENBSD:
        return "openbsd";
      default:
        return OS.getCurrent().getCanonicalName();
    }
  }
```

[^1]: <https://docs.bazel.build/versions/main/command-line-reference.html#flag--enable_platform_specific_config>
