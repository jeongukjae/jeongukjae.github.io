---
layout: post
title: "TensorFlow Model.compile Customization 시 Mixed Precision Training 실패"
tags:
    - python
    - tensorflow
---

TensorFlow에서 Mixed Precision Training 할 때, Model.compile을 직접 수정하여 사용하다보면 Loss Scaling이 제대로 되지 않을때가 있다.

원래는 Mixed Precision Training 시에 FP16 loss 범위를 보고 Loss, Gradient를 Rescale해주는 작업이 필요하다. 왜 필요한지를 다루는 것은 이 포스트의 범위를 벗어나는 것 같으니 <https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html>를 참고해주시면 좋을 것 같다. 어쨌든 해당 작업을 위한 준비는 Keras API 상에서는 Model.compile에서 한다. Model.compile에서 `_get_optimizer`라는 함수를 호출하면 해당 함수에서 optimizer 객체를 [`tf.keras.mixed_precision.LossScaleOptimizer`](https://www.tensorflow.org/api_docs/python/tf/keras/mixed_precision/LossScaleOptimizer)로 감싸준다.

하지만 해당 함수는 문서화가 되어있지도 읺고 [Keras Model을 Custom하는 튜토리얼](https://www.tensorflow.org/guide/keras/customizing_what_happens_in_fit)에도 없어서 빠뜨리기 쉽다.. 해결하는 방법은 간단하고, 2.4, 2.5버전에서는 아래처럼 추가해주기만 하면 된다. ([실제로 TF 코드에서는 이렇게 사용](https://github.com/tensorflow/tensorflow/blob/a4dfb8d1a71385bd6d122e4f27f86dcebb96712d/tensorflow/python/keras/engine/training.py#L573))

```python
class MyCustomModel(tf.keras.Model):
    ...

    def compile(self, my_custom_loss1, my_custom_loss2, optimizer1, optimizer2, ...):
        super().compile()

        self.optimizer1 = self._get_optimizer(optimizer1)
        self.optimizer2 = self._get_optimizer(optimizer2)
```

아니면 optimizer가 하나라면 `super().compile(optimizer=optimizer)`로 해결해도 되고..

그래서 튜토리얼에 관련 내용 한줄이라도 추가해달라고 이슈를 이렇게 [tensorflow/tensorflow/issues/49368](https://github.com/tensorflow/tensorflow/issues/49368) 적어보았는데, (당연하지만) private method니까 안된다고 한다.
