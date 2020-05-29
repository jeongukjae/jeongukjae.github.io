---
layout: post
title: 성능을 위한 TensorFlow Serving 커스텀 빌드
tags:
  - tensorflow
---

아래는 TensorFlow를 사용하다보면 자주 볼 수 있는 경고 메시지이다. CPU가 AVX2, AVX512F, FMA를 지원하지만 해당 extension들을 사용하도록 빌드되지 않았다는 메시지인데, 이런 메시지는 tensorflow/serving에도 똑같이 적용된다. 그래서 "빨라지면 얼마나 빨라질까?"하고 테스트해보았다.

> 2020-02-26 20:00:59.166194: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA

우선 그 명령어들은 인텔 프로세서의 Extension들이기 때문에 해당 종류들을 알아보자.
[Intel® Instruction Set Extensions Technology](https://www.intel.com/content/www/us/en/support/articles/000005779/processors.html)를 참고하면 SIMD를 활용한 여러가지 명령어 확장 세트를 확인할 수 있다.
ML에서는 병렬화가 매우 중요하기 때문에 CPU를 통한 Inference는 SIMD를 많이 활용한다. 그 중 많이 들어봤을만한 것들은 SSE, AVX 정도가 있다.

## FMA

Fused Multiply-Add의 약어로 floating point 연산을 한번에 진행하도록 해준다. [Intel® Instruction Set Extensions Technology](https://www.intel.com/content/www/us/en/support/articles/000005779/processors.html)를 참고해보면 `_mm_fmadd_pd` 같은 함수의 경우는 두 double precision floating point element를 곱하고 더한 뒤 반환해주는 것을 볼 수 있다.

## SSE

[Intel® Instruction Set Extensions Technology](https://www.intel.com/content/www/us/en/support/articles/000005779/processors.html)에 아래처럼 설명되어 있다.

> SSE is a processor technology that enables single instruction multiple data. Older processors only process a single data element per instruction. SSE enables the instruction to handle multiple data elements. It's used in intensive applications, such as 3D graphics, for faster processing.
>
> SSE is designed to replace MMX™ Technology. It expanded over the generations of Intel® Processors to include SSE2, SSE3/SSE3S, and SSE4. Each iteration has brought new instructions and increased performance.

SSE는 말 그대로 SIMD를 쓰기 위한 Extension이고, SSE가 나온 뒤 SSE2, SSE3, SSE4가 나오고 있다.

### SSE 4

SSE 4.1, SSE 4.2를 subset으로 가지고 있는 SSE 4는 2006년 Intel Developer Forum에서 발표되었다. 4.1의 몇몇은 연산과 깊게 연관되어 있고, 4.2는 STTNI (String and Text New Instructions)와 연관되어 있다. 아래 글을 한번 읽어보면 SSE가 성능 향상이 얼마나 되는지 대략적으로 알 수 있다.

* [Intel Developer Zone - XML Parsing Accelerator with Intel® Streaming SIMD Extensions 4](https://software.intel.com/en-us/articles/xml-parsing-accelerator-with-intel-streaming-simd-extensions-4-intel-sse4/)
* [GitHub - lemire/simdjson](https://github.com/lemire/simdjson)

## AVX

Advanced Vector Extensions로 최근에는 AVX 512까지 나왔다. 512라는 말은 버전 512가 아니라 512 bit이고, SIMD 대역폭을 512bit까지 늘렸기 때문에 AVX 512이다. 이전에는 AVX 256 (AVX2)였다. Extension이름에 맞게 부동 소수점 연산에 강하다.

### AVX 512

여러가지 Instruction set으로 나뉘어져 있는데, ML 분야에서 주목할 만한 기능으로는 F와 VNNI가 있다. F는 Foundation이고, VNNI는 Vector Neural Network Instructions이다. 특히 VNNI는 애초에 딥러닝 전용으로 나온 명령어들이다.

## 이런 기능들을 어떻게 사용할까

사용하는 방법은 적절하게 CC option들을 주는 것이다. TensorFlow Serving은 bazel을 빌드 툴로 사용하기 때문에 [`--copt`](https://docs.bazel.build/versions/2.0.0/user-manual.html#flag--copt) 로 적절한 옵션들을 주면 된다. 어떤 옵션을 줄지는 [GCC 4.5.3 Manual - 3.17.15 Intel 386 and AMD x86-64 Options](https://gcc.gnu.org/onlinedocs/gcc-4.5.3/gcc/i386-and-x86_002d64-Options.html)에 자세히 나와있다.

실제 사용할 서버와 같은 환경에서 이미지를 빌드한다면 대부분은 `-march=native`정도로 해결이 된다.
하지만 이미지 빌드 서버와 실제 서버를 다르게 가져간다면, 실제 서버의 CPU의 스펙을 보고 아래와 같은 옵션을 적당히 넣으면 된다.

* `-msse4.1`
* `-msse4.2`
* `-msse4`
* `-mavx`
* `-mfma4`
* `-mavx512f`

물론 미리 정의된 cpu type을 넣어서 해결할 수도 있다.

> * ‘core2’
>   * Intel Core 2 CPU with 64-bit extensions, MMX, SSE, SSE2, SSE3 and SSSE3 instruction set support.
> * ‘corei7’
>   * Intel Core i7 CPU with 64-bit extensions, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1 and SSE4.2 instruction set support.
> * ‘corei7-avx’
>   * Intel Core i7 CPU with 64-bit extensions, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, AVX, AES and PCLMUL instruction set support.
> * ‘core-avx-i’
>   * Intel Core CPU with 64-bit extensions, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, AVX, AES, PCLMUL, FSGSBASE, RDRND and F16C instruction set support.
> * ‘core-avx2’
>   * Intel Core CPU with 64-bit extensions, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, AVX, AVX2, AES, PCLMUL, FSGSBASE, RDRND, FMA, BMI, BMI2 and F16C instruction set support.

### AWS에서는??

[AWS EC2 인스턴스 유형](https://aws.amazon.com/ko/ec2/instance-types/)을 살펴보면 인텔 프로세서를 사용하는 EC2를 여러가지 기능을 분류해놓고 제공하는데 아래와 같다.

* 인텔 AES-NI: 빠른 암호화 알고리즘 기능
* 인텔 Advanced Vector Extensions: AVX 지원
* 인텔 터보 부스트 기술: 정말 터보 부스트 말하는거
* 인텔 DL 부스트: AVX512VNNI를 지원한다.

여기서 중요한 점은 AVX, DL 부스트 정도이다. 둘 다 지원하는 인스턴스는 C5, C5d의 12xlarge, 24xlarge, metal 정도이다. 근데 이 중 가장 싼 c5.12xlarge (48코어}는 시간당 2.04달러로 한달을 30일을 계산했을 때 1,658달러.. 정도이다.. 스케일링을 생각해서 avx 512까지만 지원하는 c5.2xlarge(8코어)를 띄운다고 하면 한달을 30일로 계산했을 때 276달러정도이므로 적당한 가격에 스케일링이 가능하다.

### Tensorflow Serving 빌드하기

[GitHub - tensorflow/serving](https://github.com/tensorflow/serving)을 가보면 코드를 받을 수 있다. Tensorflow serving 도커 이미지 빌드는 두가지로 나누어진다.
일반 도커 이미지가 `devel`이미지인데, 일반 도커 이미지는 `devel` 이미지에서 바이너리만 가져온다. 따라서 우리가 수정해서 사용할 이미지는 `devel`이미지이다.

[GitHub - tensorflow/serving/tensorflow_serving/tools/docker/Dockerfile.devel](https://github.com/tensorflow/serving/blob/master/tensorflow_serving/tools/docker/Dockerfile.devel)를 참고해보면 맨 밑에서 Tensorflow Serving 바이너리를 빌드하는 것을 볼 수 있는데, 그 부분을 위해 `TF_SERVING_BAZEL_OPTIONS`를 조정하면 된다.

나는 c5 계열을 사용할 예정이라 아래 정도를 주었다.

* `--copt=-mfma`
* `--copt=-mfpmath=both`
* `--copt=-msse4.1`
* `--copt=-msse4.2`
* `--copt=-mavx`
* `--copt=-mavx2`
* `--copt=-mavx512f`

## 결과

네트워크 속도가 포함되어 있지만, 10~20%정도의 처리량 향상을 경험했다. VNNI를 테스트해보지는 못했지만 해당 기능까지 활성화하면 더 빨라질 것으로 보인다. 아마 정말 급한 것이 아니면 간단한 설정만으로 처리량이 증가하니 무조건 해봐야 하지 않을까..?

## 참고

* [TensorFlow Docs - Build from source](https://www.tensorflow.org/install/source)
* [Intel® Instruction Set Extensions Technology](https://www.intel.com/content/www/us/en/support/articles/000005779/processors.html)
* [Intel 386 Optimization Options](https://gcc.gnu.org/onlinedocs/gcc-4.5.3/gcc/i386-and-x86_002d64-Options.html)
* [x86 built in functions](https://gcc.gnu.org/onlinedocs/gcc-4.5.3/gcc/X86-Built_002din-Functions.html#X86-Built_002din-Functions)
* [Intel Developer Zone - XML Parsing Accelerator with Intel® Streaming SIMD Extensions 4](https://software.intel.com/en-us/articles/xml-parsing-accelerator-with-intel-streaming-simd-extensions-4-intel-sse4/)
