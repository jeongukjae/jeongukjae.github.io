---
layout: post
title: "🚀 Apex's FusedLayerNorm vs Torch's LayerNorm"
tags:
  - pytorch
---

[microsoft/DeepSpeedExamples](https://github.com/microsoft/DeepSpeedExamples)의 BERT에서 [Apex의 FusedLayerNorm을 사용](https://github.com/microsoft/DeepSpeedExamples/blob/8610e5e3fcce5fb247e3b85ea2bed0f2296b5443/bing_bert/nvidia/modelingpreln.py#L308-L313)하고 있고, [NVIDIA/DeepLearningExamples](https://github.com/NVIDIA/DeepLearningExamples)에서도 [Apex의 FusedLayerNorm을 사용](https://github.com/NVIDIA/DeepLearningExamples/blob/6c1d562eb9079760a4deaece4806967b092b583b/PyTorch/LanguageModeling/BERT/modeling.py#L287)하고 있다. 그럼 Apex의 FusedLayerNorm과 torch.nn.LayerNorm의 차이는 무엇일까?

두 모듈의 문서를 살펴보면 ([apex fused_layer_norm 문서](https://nvidia.github.io/apex/layernorm.html), [torch.nn.LayerNorm 문서](https://pytorch.org/docs/master/generated/torch.nn.LayerNorm.html)) 인터페이스, 수식은 같다.

$$y = \frac{x - \mathrm{E}[x]}{ \sqrt{\mathrm{Var}[x] + \epsilon}} * \gamma + \beta$$

실제로 연산을 수행하는 부분은 각각 [NVIDIA/apex/csrc/layer_norm_cuda_kernel.cu](https://github.com/NVIDIA/apex/blob/c3fad1ad120b23055f6630da0b029c8b626db78f/csrc/layer_norm_cuda_kernel.cu#L670), [pytorch/pytorch/aten/src/ATen/native/cuda/layer_norm_kernel.cu](https://github.com/pytorch/pytorch/blob/23739654cd6e6b55c86d74608d84d3f6c3ac8cb6/aten/src/ATen/native/cuda/layer_norm_kernel.cu#L423)이다.

## 코드의 차이

[apex 코드](https://github.com/NVIDIA/apex/blob/c3fad1ad120b23055f6630da0b029c8b626db78f/csrc/layer_norm_cuda_kernel.cu#L279)에서는 아래처럼 LayerNorm을 계산한다.

```c++
template<typename T, typename U> __global__
void cuApplyLayerNorm(
  T* __restrict__ output_vals,
  U* __restrict__ mean,
  U* __restrict__ invvar,
  const T* __restrict__ vals,
  const int n1,
  const int n2,
  const U epsilon,
  const T* __restrict__ gamma,
  const T* __restrict__ beta
  )
{
  // Assumptions:
  // 1) blockDim.x == warpSize
  // 2) Tensors are contiguous
  //
  for (auto i1=blockIdx.y; i1 < n1; i1 += gridDim.y) {
    SharedMemory<U> shared;
    U* buf = shared.getPointer();
    U mu,sigma2;
    cuWelfordMuSigma2(vals,n1,n2,i1,mu,sigma2,buf);
    const T* lvals = vals + i1*n2;
    T* ovals = output_vals + i1*n2;
    U c_invvar = rsqrt(sigma2 + epsilon);
    const int numx = blockDim.x * blockDim.y;
    const int thrx = threadIdx.x + threadIdx.y * blockDim.x;
    if (gamma != NULL && beta != NULL) {
      for (int i = thrx;  i < n2;  i+=numx) {
        U curr = static_cast<U>(lvals[i]);
        ovals[i] = gamma[i] * static_cast<T>(c_invvar * (curr - mu)) + beta[i];
      }
    } else {
      for (int i = thrx;  i < n2;  i+=numx) {
        U curr = static_cast<U>(lvals[i]);
        ovals[i] = static_cast<T>(c_invvar * (curr - mu));
      }
    }
    if (threadIdx.x == 0 && threadIdx.y == 0) {
      mean[i1] = mu;
      invvar[i1] = c_invvar;
    }
  }
}
```

실제로 mu, sigma를 계산하는 `cuWelfordMuSigma2`를 살펴보면 아래처럼 코드가 작성되어 있다.

```c++
template<typename T, typename U> __device__
void cuWelfordMuSigma2(
  const T* __restrict__ vals,
  const int n1,
  const int n2,
  const int i1,
  U& mu,
  U& sigma2,
  U* buf)
{
  // Assumptions:
  // 1) blockDim.x == warpSize
  // 2) Tensor is contiguous
  // 3) 2*blockDim.y*sizeof(U)+blockDim.y*sizeof(int) shared memory available.
  //
  // compute variance and mean over n2
  U count = U(0);
  mu= U(0);
  sigma2 = U(0);
  if (i1 < n1) {
    // one warp normalizes one n1 index,
    // synchronization is implicit
    // initialize with standard Welford algorithm
    const int numx = blockDim.x * blockDim.y;
    const int thrx = threadIdx.x + threadIdx.y * blockDim.x;
    const T* lvals = vals + i1*n2;
    int l = 4*thrx;
    for (;  l+3 < n2;  l+=4*numx) {
      for (int k = 0;  k < 4;  ++k) {
        U curr = static_cast<U>(lvals[l+k]);
        cuWelfordOnlineSum<U>(curr,mu,sigma2,count);
      }
    }
    for (;  l < n2;  ++l) {
      U curr = static_cast<U>(lvals[l]);
      cuWelfordOnlineSum<U>(curr,mu,sigma2,count);
    }
    ...
```

계속해서 루프를 돌며 OnlineSum을 해간다. OnlineSum은 Welford's Online Algorithm을 사용한다.

근데 이 알고리즘은 [이렇게 설명](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm)이 되어 있다.

> This algorithm is much less prone to loss of precision due to catastrophic cancellation, but might not be as efficient because of the division operation inside the loop.

---

그에 비해 Torch는 다르게 계산을 하는데, 우선 LayerNormKernel이라는 이름으로 [아래처럼 구현](https://github.com/pytorch/pytorch/blob/23739654cd6e6b55c86d74608d84d3f6c3ac8cb6/aten/src/ATen/native/cuda/layer_norm_kernel.cu#L257)해놓았다.

```c++
template <typename T>
void LayerNormKernelImplInternal(
    const Tensor& X,
    const Tensor& gamma,
    const Tensor& beta,
    int64_t M,
    int64_t N,
    T eps,
    Tensor* Y,
    Tensor* mean,
    Tensor* rstd) {
  DCHECK_EQ(X.numel(), M * N);
  DCHECK(!gamma.defined() || gamma.numel() == N);
  DCHECK(!beta.defined() || beta.numel() == N);
  const T* X_data = X.data_ptr<T>();
  const T* gamma_data = gamma.defined() ? gamma.data_ptr<T>() : nullptr;
  const T* beta_data = beta.defined() ? beta.data_ptr<T>() : nullptr;
  T* Y_data = Y->data_ptr<T>();
  T* mean_data = mean->data_ptr<T>();
  T* rstd_data = rstd->data_ptr<T>();
  cudaStream_t cuda_stream = at::cuda::getCurrentCUDAStream();
  RowwiseMomentsCUDAKernel<T>
      <<<M, cuda_utils::kCUDABlockReduceNumThreads, 0, cuda_stream>>>(
          N, eps, X_data, mean_data, rstd_data);
  LayerNormForwardCUDAKernel<T><<<M, kCUDANumThreads, 0, cuda_stream>>>(
      N, X_data, mean_data, rstd_data, gamma_data, beta_data, Y_data);
  AT_CUDA_CHECK(cudaGetLastError());
}
```

Moments를 계산하고, LayerNorm을 계산하는 것으로 보인다. Moments를 계산하는 과정은 [`RowwiseMomentsCUDAKernel`에 구현](https://github.com/pytorch/pytorch/blob/23739654cd6e6b55c86d74608d84d3f6c3ac8cb6/aten/src/ATen/native/cuda/layer_norm_kernel.cu#L22)되어 있다.

```c++
template <typename T>
__global__ void RowwiseMomentsCUDAKernel(
    int64_t N,
    T eps,
    const T* X,
    T* mean,
    T* rstd) {
  using T_ACC = acc_type<T, true>;
  __shared__ T_ACC m_shared[C10_WARP_SIZE];
  __shared__ T_ACC v_shared[C10_WARP_SIZE];
  const int64_t i = blockIdx.x;
  T_ACC sum1 = 0;
  T_ACC sum2 = 0;
  for (int64_t j = threadIdx.x; j < N; j += blockDim.x) {
    const int64_t index = i * N + j;
    sum1 += static_cast<T_ACC>(X[index]);
    sum2 += static_cast<T_ACC>(X[index]) * static_cast<T_ACC>(X[index]);
  }
  sum1 = cuda_utils::BlockReduceSum<T_ACC>(sum1, m_shared);
  sum2 = cuda_utils::BlockReduceSum<T_ACC>(sum2, v_shared);
  if (threadIdx.x == 0) {
    const T_ACC scale = T_ACC(1) / static_cast<T_ACC>(N);
    sum1 *= scale;
    sum2 = c10::cuda::compat::max(sum2 * scale - sum1 * sum1, T_ACC(0));
    mean[i] = sum1;
    rstd[i] = c10::cuda::compat::rsqrt(sum2 + static_cast<T_ACC>(eps));
  }
}
```

일반적으로 평균, 분산을 구하는 코드와 같은 코드이다.

그 외에는 거의 같은 코드이며, 이 부분의 코드만 다른 것으로 보아 성능이 다르다면 이 부분으로 인해 달라질 것 같다.

## History

근데 현재 구현을 보면 메모리 접근 시간이 정말 느리지 않는 이상 Apex FusedLayerNorm이 더 느릴 것 같은데 관련 Issue, Commit history를 살펴보자.

* [NVIDIA/apex/issues/449](https://github.com/NVIDIA/apex/issues/449)
* [Gist - layernorm vs fused](https://gist.github.com/ptrblck/8b1c6a7efd97604a7dedbf2c3edd1019)
* [pytorch/pytorch/issues/37713](https://github.com/pytorch/pytorch/issues/37713)
* [pytorch/fairseq/issues/2012](https://github.com/pytorch/fairseq/issues/2012)
* ...

Apex가 더 빠르다는 사람도 있고, Torch가 더 빠르다는 사람도 있고.. 해서 Commit History를 보면 `pytorch/aten/src/ATen/native/cuda/layer_norm_kernel.cu` 파일의 첫 커밋이 ["Add fused layer norm impl on CUDA in PyTorch (#27634)"](https://github.com/pytorch/pytorch/commit/8b87f9a5107e8b3c4f87d5297af698bb55838d81#diff-f12c726e3e8cd2b4768f8984fef27059)이다..?

타고 들어가보면 PyTorch에 FusedLayerNorm을 추가하는 PR이고, 원래는 LayerNorm이 PyTorch가 Apex보다 많이 느렸다. 하지만 [해당 PR의 설명](https://github.com/pytorch/pytorch/pull/27634)을 참고하면 Apex와 비교해서 거의 모든 케이스에서 빨라진 것을 볼 수 있다.

적용된 버전은 1.4.0 이후이고 그 전에는 CUDA 커널이 없었던 것 같지만, 해당 커널이 적용된 1.4.0이상을 쓰면 apex FusedLayerNorm을 쓸 필요가 없어보인다.

## 돌려보자

그래서 일단 1.4.0버전을 기준으로 테스트하면 PyTorch LayerNorm이 더 빠를 것 같아서 실제로 forward, backward 한번씩 돌려보았다.

apex는 [NVIDIA/apex#161(comment)](https://github.com/NVIDIA/apex/issues/161#issuecomment-466611317)처럼 설치했고, Tesla V100-DGXS-32GB, torch==1.4.0에서 테스트를 진행했다.

```python
import torch
import apex
import time

ApexLayerNorm = apex.normalization.fused_layer_norm.FusedLayerNorm
LayerNorm = torch.nn.LayerNorm

for dim in range(128, 1025, 128):
    bsz = 2048
    apex_norm = ApexLayerNorm(dim).half().cuda()
    torch_norm = LayerNorm(dim).half().cuda()

    target = torch.rand((bsz, dim)).half().cuda()

    # warm up
    for _ in range(10):
        input_tensor = torch.rand((bsz, dim)).half().cuda().contiguous()
        output1 = apex_norm(input_tensor)
        loss = torch.nn.functional.mse_loss(output1, target)
        loss.backward()

        output2 = torch_norm(input_tensor)
        loss = torch.nn.functional.mse_loss(output2, target)
        loss.backward()

    input_tensor = torch.rand((bsz, dim)).half().cuda().contiguous()

    start = time.time()
    for _ in range(1000):
        output = torch_norm(input_tensor)
        loss = torch.nn.functional.mse_loss(output, target)
        loss.backward()
    torch_end = time.time()
    for _ in range(1000):
        output = apex_norm(input_tensor)
        loss = torch.nn.functional.mse_loss(output, target)
        loss.backward()
    apex_end = time.time()

    torch_dur = (torch_end - start) / 1000
    apex_dur = (apex_end - torch_end) / 1000
    print(f"dim {dim:4d} Batch Size {bsz:3d}, Torch: {torch_dur:.8f} Apex: {apex_dur:.8f} Imp {(torch_dur - apex_dur) / apex_dur * 100:2.2f}")
```

이 코드의 결과는 아래처럼 나왔고

```shell
(env) jeongukjae@server:~$ python test.py
dim  128 Batch Size 2048, Torch: 0.00031060 Apex: 0.00035981 Imp -13.67
dim  256 Batch Size 2048, Torch: 0.00030215 Apex: 0.00035082 Imp -13.87
dim  384 Batch Size 2048, Torch: 0.00033065 Apex: 0.00037036 Imp -10.72
dim  512 Batch Size 2048, Torch: 0.00029822 Apex: 0.00035301 Imp -15.52
dim  640 Batch Size 2048, Torch: 0.00031614 Apex: 0.00036779 Imp -14.04
dim  768 Batch Size 2048, Torch: 0.00030238 Apex: 0.00036041 Imp -16.10
dim  896 Batch Size 2048, Torch: 0.00029817 Apex: 0.00036967 Imp -19.34
dim 1024 Batch Size 2048, Torch: 0.00030955 Apex: 0.00036211 Imp -14.51
```

결국 1.4.0이면 apex fusedlayernorm은 필요없는 것 같다.

그래서 [다른 사람이 올려놓은 벤치마크 코드](https://gist.github.com/ptrblck/8b1c6a7efd97604a7dedbf2c3edd1019)를 가져와서 실행해보았다.

```shell
import torch
import torch.nn as nn

torch.backends.cudnn.benchmark = True

from apex.normalization import FusedLayerNorm

import time


# Create data
x = torch.randn(64, 16, 224, 224, device='cuda')

# upstream layernorm
norm = nn.LayerNorm(x.size()[1:]).cuda()

# cudnn warmup
for _ in range(50):
    _ = norm(x)

nb_iters = 1000
torch.cuda.synchronize()
t0 = time.time()

for _ in range(nb_iters):
    _ = norm(x)

torch.cuda.synchronize()
t1 = time.time()

print('upstream layernorm {:.3f}'.format(t1 -t0))

# apex fusedlayernorm
fused_norm = FusedLayerNorm(x.size()[1:]).cuda()

# cudnn warmup
for _ in range(50):
    _ = fused_norm(x)

nb_iters = 1000
torch.cuda.synchronize()
t0 = time.time()

for _ in range(nb_iters):
    _ = fused_norm(x)

torch.cuda.synchronize()
t1 = time.time()

print('apex layernorm {:.3f}'.format(t1 -t0))

```

```shell
(env) jeongukjae@server:~$ python test2.py
upstream layernorm 2.464
apex layernorm 3.490
```

근데 그럼 1.3.1을 사용해서 테스트하면 실제로 느릴까? 결과는 아래와 같다.

```shell
(env) jeongukjae@server:~$ python test.py
dim  128 Batch Size 2048, Torch: 0.00047603 Apex: 0.00038654 Imp 23.15
dim  256 Batch Size 2048, Torch: 0.00045056 Apex: 0.00037928 Imp 18.79
dim  384 Batch Size 2048, Torch: 0.00052916 Apex: 0.00041193 Imp 28.46
dim  512 Batch Size 2048, Torch: 0.00048436 Apex: 0.00039859 Imp 21.52
dim  640 Batch Size 2048, Torch: 0.00047772 Apex: 0.00036401 Imp 31.24
dim  768 Batch Size 2048, Torch: 0.00048790 Apex: 0.00041975 Imp 16.24
dim  896 Batch Size 2048, Torch: 0.00048001 Apex: 0.00041013 Imp 17.04
dim 1024 Batch Size 2048, Torch: 0.00050486 Apex: 0.00045190 Imp 11.72
```

1.3.1버전은 Apex가 더 빠르다.

---

엄청 정리안하고 글을 썼지만 간단하게 정리해보자면,

* 원래는 Apex LayerNorm이 더 빠른 것이 맞았다.
* 하지만 torch 1.4.0에 적용된 ["Add fused layer norm impl on CUDA in PyTorch (#27634)"](https://github.com/pytorch/pytorch/commit/8b87f9a5107e8b3c4f87d5297af698bb55838d81#diff-f12c726e3e8cd2b4768f8984fef27059) 커밋 이후로는 성능이 Torch가 더 좋다.
* 하지만 mean, variance를 구하는 로직이 다른데, apex 버전이 더 precision의 loss가 덜 하다.
