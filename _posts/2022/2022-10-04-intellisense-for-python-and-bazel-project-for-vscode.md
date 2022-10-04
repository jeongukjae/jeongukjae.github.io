---
layout: post
title: "Set up intellisense for Python and Bazel project for VSCode"
tags:
    - python
    - bazel
---

Bazel provides powerful build system for any projects, but sometimes, it is not that easy to set up intellisense for Python and Bazel project for VSCode.
So here's my quick solution for this.

```json
{
    "python.analysis.extraPaths": ["bazel-bin"]
}
```

## Why this works

I use Bazel with Python when I need to build with other languages such as C++ or ProtoBuf, and all build results (files in `./bazel-*`) are not searched by default by VSCode.
So adding extra paths to python analyzer is the easiest way to make it work.
