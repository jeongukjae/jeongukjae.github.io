---
layout: post
title: PyTorch C++ FrontEnd 개발환경 맥에서 세팅
tags:
  - pytorch
---

TorchScript 사용법을 체크해보면서, PyTorch C++ FrontEnd 환경을 구성해볼 필요가 있었는데, 맥 환경에서는 생각보다 쉽게는 진행이 되지 않아서 정리해본다.

\+ 정리해놓고 보니 굉장히 순조롭게 진행한 것처럼 쓰여져 버렸다. 이렇게 써놓았지만 왜 빌드가 안 돌지...? 하면서 몇시간을 썼다.

## LibTorch 다운로드

LibTorch부터 다운로드해서 로컬에서 사용할 수 있게 세팅해야 한다. LibTorch를 로컬에서 구성할 수 있는 방법은 두가지가 있는 것으로 보이는데, 하나는 직접 빌드하는 것이고, 두번째는 다운로드하는 것이다. 처음에 MacOS에서 linker 오류가 나서 직접 빌드를 시도해보았는데, 생각보다 시간이 오래 걸려서 다운로드 하는 방법을 추천한다.

처음에 굉장히 삽질을 했던 부분이 PyTorch 튜토리얼에는 이런 언급이 나와있지 않고, 바이너리를 바로 wget으로 받아서 진행하도록 나와있는데, 이게 url에 linux용이라는 명시가 없어서 한참 헤맸다.

[https://pytorch.org](https://pytorch.org)에서 QUICK START LOCALLY 섹션에서 다운로드를 진행하면 되는데, MacOS에서는 CUDA가 지원되지 않아 아래처럼 나와있다.

> MacOS binaries do not support CUDA. Download CPU libtorch here:
>
> [https://download.pytorch.org/libtorch/cpu/libtorch-macos-1.3.0.zip](https://download.pytorch.org/libtorch/cpu/libtorch-macos-1.3.0.zip)

1.3.0 버전을 받으려면 아래처럼 시도하면 된다.

```sh
wget https://download.pytorch.org/libtorch/cpu/libtorch-macos-1.3.0.zip
unzip libtorch-macos-1.3.0.zip
```

## 튜토리얼 진행해보기

다운로드 받고 나서 [PyTorch Docs - INSTALLING C++ DISTRIBUTIONS OF PYTORCH](https://pytorch.org/cppdocs/installing.html#minimal-example)를 참고해서 아래와 같은 파일을 작성했다.

### `main.cc`

```cpp
#include <torch/torch.h>
#include <iostream>

int main() {
  torch::Tensor tensor = torch::rand({2, 3});
  std::cout << tensor << std::endl;
}
```

### `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(example-project)

find_package(Torch REQUIRED)

add_executable(example-ap main.cc)

target_link_libraries(example-ap "${TORCH_LIBRARIES}")

set_property(TARGET example-ap PROPERTY CXX_STANDARD 11)
```

그리고 아래처럼 실행했다. (나는 libtorch를 `~/libs/libtorch`에 넣어놓았다)

```sh
$ mkdir build & build
$ cmake -DCMAKE_PREFIX_PATH=~/libs/libtorch  ..
-- The C compiler identification is AppleClang 11.0.0.11000033
-- The CXX compiler identification is AppleClang 11.0.0.11000033
-- Check for working C compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc
-- Check for working C compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
...
$ make
Scanning dependencies of target server
[ 50%] Building CXX object ....
...
$ ./example-app
```

## ???

그런데, Cmake로 빌드하고 실행하다보면 막히는 부분이 있는데, 아래처럼 뜨면서 안된다.

```sh
$ ./example-app
dyld: Library not loaded: @rpath/libiomp5.dylib
  Referenced from: /libs/libtorch/lib/libtorch.dylib
  Reason: image not found
```

`libiomp5.dylib`이 없다는 것인데 이게 [intel/mkl-dnn](https://github.com/intel/mkl-dnn) 레포지토리에서 다운로드받을 수 있다. 관련 이슈는 [pytorch/pytorch#14727](https://github.com/pytorch/pytorch/issues/14727)를 참고히면 될 것 같다. `libiomp5.dylib`, `libmklml.dylib` 두 라이브러리 파일을 libtorch가 있는 폴더의 `lib`안에 넣어주면 된다.

## ---

이렇게 결국 잘 돌아간다.

```sh
$ ./example-app
 0.2055  0.5863  0.5734
 0.1759  0.7157  0.3312
[ Variable[CPUFloatType]{2,3} ]
```

## 참고

* [PyTorch](https://pytorch.org)
* [PyTorch Docs - INSTALLING C++ DISTRIBUTIONS OF PYTORCH](https://pytorch.org/cppdocs/installing.html#minimal-example)
* [pytorch/pytorch#14727](https://github.com/pytorch/pytorch/issues/14727)
* [intel/mkl-dnn](https://github.com/intel/mkl-dnn)
