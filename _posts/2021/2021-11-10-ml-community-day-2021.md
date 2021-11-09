---
layout: post
title: "ML Community Day 정리"
tags:
  - conference
---

ML Community Day 들으면서 신기한 것들만 정리

{% include image.html url="/images/2021/11-10-ml-community-day/1.png" alt="생태계 요약" description="생태계 요약" %}

* For edge devices
    * TensorFlow Lite는 모바일에서 학습 가능
    * TF Lite에서 XNNPack을 사용하도록 업데이트
    * **TF Lite를 브라우저에서 실행 가능** -> quatization 까지도 상관 없음
* ML Ops
    * Fairness를 판별하는 것을 도와주도록 TFX에 통합
    * language Interpretability Tool (LIT)
* Jax, TPU
    * T5X 참고해보면 좋은 예제가 될 듯
    * 서빙은 괜찮나? 생각하는데, `We're working on it, but TF-Serving is generally your friend here.` 이렇게 대답해줌
* tf lite
    * <https://www.tensorflow.org/lite/performance/quantization_debugger>
    * <https://www.tensorflow.org/lite/guide/authoring>
    * <https://www.tensorflow.org/lite/guide/model_analyzer>
* TFX
    * Exit Handler
    * Pipleine Branching
    * 이거 엄청 편해보이는데...

{% include image.html url="/images/2021/11-10-ml-community-day/2.png" alt="TPU 사용 방식의 변화" description="TPU 사용 방식의 변화" %}

* Cloud TPU 얼마나 사용하기 편해졌는지 살펴보아야겠다.
