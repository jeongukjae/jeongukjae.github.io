---
layout: post
title: "TensorFlow의 softmax_cross_entropy_with_logits의 Non-determinism 이슈"
tags:
    - tensorflow
---

얼마전 [tensorflow/community/pull/346](https://github.com/tensorflow/community/pull/346)을 보면서 놀란 점이 있다. 바로 `tf.nn.sparse_softmax_cross_entropy_with_logits`, `tf.nn.softmax_cross_entropy_with_logits` 연산이 non-deterministic하다는 것인데, 수식상으로 생각해볼때 저 Ops들이 그렇다는 것을 알기 힘들었다. 매우 자주 사용하는 Op들이고, [이전에 코드를 살펴보았을 때](https://blog.ukjae.io/posts/tf-sparse-categorical-cross-entropy/)도 log softmax 이후 정상적으로 crossentropy를 연산하는 것으로 보였기 때문이다.

***일단 먼저 말하자면 정확한 원인을 찾지는 못했다.*** 나중에 다시 살펴보기 편하게 한번 정리만..

## Determinism RFC

우선 해당 PR부터 보면 특정 분야(medicine, finance, ..)등에서 determinism을 강하게 요구하고 있고 해당 분야에서도 TF를 잘 사용하도록 돕기 위해 determinism을 강화한다는 RFC이다.
Accepted된 상태이고, 해당 주제에 관심이 있던 차라 자세히 읽어보던 중 `tf.nn.sparse_softmax_cross_entropy_with_logits`, `tf.nn.softmax_cross_entropy_with_logits` Op들도 non-deterministic하다는 것을 알게 되었다.

## 관련 이슈/PR들

그래서 조금 더 살펴보니 [tensorflow/tensorflow/pull/47925](https://github.com/tensorflow/tensorflow/pull/47925)로 해당 내용을 패치하는 (실제로 구현하기보다 determinism 플래그가 켜져있으면 에러를 발생시키는) PR이 올라와있는 것을 발견했다. 원본 이슈가 링크되어 있지 않아 조금 더 살펴보니 [tensorflow/tensorflow/issues/38185](https://github.com/tensorflow/tensorflow/issues/38185), [NVIDIA/framework-determinism/issues/9](https://github.com/NVIDIA/framework-determinism/issues/9) 이슈를 찾을 수 있었고, 20년 1월즈음부터 해당 내용이 발견되었다는 것을 알 수 있었다.

위 이슈/PR/코드들을 읽으면서 알게 된 내용들을 정리하면 아래 정도이다.

* CPU에서는 deterministic하다. [이렇게 해결한 분도 있다.](https://github.com/NVIDIA/framework-determinism/issues/9#issuecomment-575613764)
* [`tf.nn.sparse_softmax_cross_entropy_with_logits`의 Backprop이 학습을 non-deterministic하게 만든다.](https://github.com/NVIDIA/framework-determinism/issues/9#issuecomment-608121499)
* [해당 colab 노트북](https://colab.research.google.com/drive/1syj32Jl7dS6mBa-GhNrq_LLIxvfumIOz)으로 재현해볼 수 있다. [원본 이슈 링크](https://github.com/tensorflow/tensorflow/issues/38185#issue-593067194)
* NVIDIA 쪽에서 유지해오고 있는 레포지토리에 작성된 [PR (NVIDIA/framework-determinism/pull/21)](https://github.com/NVIDIA/framework-determinism/pull/21)도 있었다. (비록 답장이 없지만..)
* xent with logit 관련 numerical stability 이슈는 [tensorflow/tensorflow/issues/2462](https://github.com/tensorflow/tensorflow/issues/2462)를 참고할 수 있다.
* [non-deterministic한 xent의 원인은 forward path algorithm이다.](https://github.com/tensorflow/tensorflow/pull/47925#issue-596788474)
* 알고리즘의 문제가 아니라 해당 알고리즘에서 사용한 쿠다 커널의 문제인 것 같다. -> 동일한 알고리즘을 tf ops로 작성해보았을 때는 또 괜찮다.
* Sparse Xent Op 코드 위치는 [여기](https://github.com/tensorflow/tensorflow/blob/dec8e0b11f4f87693b67e125e67dfbc68d26c205/tensorflow/core/kernels/sparse_xent_op.h#L172)이다.
* 지금 tensorflow의 xent 코드를 보면 알 수 있지만, numerical stability를 위해 max 값을 미리 처리해주는데, 이게 일반적인 log softmax에 비해 [한번 더 스캔](https://github.com/tensorflow/tensorflow/blob/dec8e0b11f4f87693b67e125e67dfbc68d26c205/tensorflow/core/kernels/sparse_xent_op.h#L213)을 하기 때문에 느리지만 numerically stable하다고 한다. 여기서 이 로직을 Streaming logsumexp로 바꾸어 줄 수 있는데, ([관련 블로그 포스트](http://www.nowozin.net/sebastian/blog/streaming-log-sum-exp-computation.html))에서는 두배정도 빠를 수 있다고 한다. 진짜로 그럴지는 모르겠지만 시간나면 한번쯤 구현해봐도 좋아보인다.

    생각해보면 예전에 [Apex의 FusedLayerNorm 코드 뜯어보면서](https://blog.ukjae.io/posts/apex-fused-layer-norm-vs-torch-layer-norm/) 봤던 Welford's online algorithm (Variance 계산용 알고리즘)봤던 느낌이다.

궁금해서 [위의 노트북](https://colab.research.google.com/drive/1syj32Jl7dS6mBa-GhNrq_LLIxvfumIOz)을 2.4.1 버전으로 돌려봤는데 아래와 같은 결과를 얻었고, 아직 non-deterministic하다는 것을 확인할 수 있었다.

```text
TensorFlow version: '2.4.1'
INFO:tensorflow:time(__main__.DeterministicTest.testDistributionLabelsDeterministicGradients): 0.08s
FINFO:tensorflow:time(__main__.DeterministicTest.testExclusiveLabelsDeterministicGradients): 0.07s
Fs
======================================================================
FAIL: testDistributionLabelsDeterministicGradients (__main__.DeterministicTest)
DeterministicTest.testDistributionLabelsDeterministicGradients
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<ipython-input-4-dae8152b1a5c>", line 66, in testDistributionLabelsDeterministicGradients
    self._testDeterministicGradients(exclusive_labels=False)
  File "<ipython-input-4-dae8152b1a5c>", line 60, in _testDeterministicGradients
    self.assertAllEqual(result_a, result_b)
  File "/usr/local/lib/python3.7/dist-packages/tensorflow/python/framework/test_util.py", line 1236, in decorated
    return f(*args, **kwds)
  File "/usr/local/lib/python3.7/dist-packages/tensorflow/python/framework/test_util.py", line 2843, in assertAllEqual
    np.testing.assert_array_equal(a, b, err_msg="\n".join(msgs))
  File "/usr/local/lib/python3.7/dist-packages/numpy/testing/_private/utils.py", line 931, in assert_array_equal
    verbose=verbose, header='Arrays are not equal')
  File "/usr/local/lib/python3.7/dist-packages/numpy/testing/_private/utils.py", line 840, in assert_array_compare
    raise AssertionError(msg)
AssertionError:
Arrays are not equal

not equal where = (array([   1,    1,    1, ..., 1023, 1023, 1023]), array([ 38,  63, 156, ..., 972, 987, 988]))
not equal lhs = array([-0.01129362, -0.00140473, -0.00028352, ..., -0.00012536,
        0.00221102, -0.0012473 ], dtype=float32)
not equal rhs = array([-0.01129362, -0.00140473, -0.00028352, ..., -0.00012536,
        0.00221102, -0.0012473 ], dtype=float32)
Mismatched elements: 28415 / 1024000 (2.77%)
Max absolute difference: 2.3841858e-07
Max relative difference: 0.00027467
 x: array([[ 0.004697,  0.007204,  0.002064, ...,  0.001554,  0.005809,
         0.004852],
       [ 0.087343,  0.051957,  0.043549, ...,  0.053608,  0.07078 ,...
 y: array([[ 0.004697,  0.007204,  0.002064, ...,  0.001554,  0.005809,
         0.004852],
       [ 0.087343,  0.051957,  0.043549, ...,  0.053608,  0.07078 ,...
```

---

위에 있는 이슈/PR들이 정리된다면 다시 보고 정리해보아야겠다.
제대로 어느 부분이 문제였는지 보려면 eigen 코드와 같이 봐야할 것 같은데 너무 시간이 오래 걸릴 것 같아서 패스..
