---
layout: post
title: "ViT는 태스크를 어떻게 풀어낼까?"
tags:
  - paper
---

제목이 관심이 가서 본 논문(`Do Vision Transformers See Like Convolutional Neural Networks?`)에서 던진 핵심 질문이다.

> Recent work has shown that (Vision) Transformer models (ViT) can achieve comparable or even superior performance on image classification tasks. This raises a central question: *how are Vision Transformers solving these tasks?*

- arxiv 링크: <https://arxiv.org/abs/2108.08810>

## _

- ViT, CNN 구조, 이미지 분류 벤치마크를 같이 살펴보면서 두 아키텍쳐가 어떻게 다른지, 왜 달라지게 되는지를 살펴본 논문.
  - self-attention이 거기서 어떤 중요한 역할을 하는지, residual connection이 낮은 레이어에서 높은 레이어로 어떻게 정보를 전파시키는지
- main contributions:
  - ViT, CNN의 internal representation structure를 조사해보고 다른 점을 찾아봄. -> ViT이 조금 더 uniform한 표현값을 지님
  - 어떻게 local/global한 spatial 정보가 활용되는지 확인 ViT은 낮은 레이어에서 더 global한 피쳐를 보고 있음.
  - 여전히 중요한 local 정보를 pre-training을 통해서 attention layer가 배우는 것을 확인
  - skip connection이 ViT에서 더 영향력이 크다는 것을 확인
  - 공간적인 정보가 얼마나 잘 유지되는지 확인 (object detection 같은 곳에 사용이 가능하도록)
  - transfer learning에서 dataset scale의 영향을 확인.

---

- representation structure
  - ResNet과 비교했을 때 ViT는 굉장히 uniform하게 representation이 분포함. (분포한다고 하면 이상하긴 한데, 이전 레이어와 다음 레이어의 representation 차이가 극심하지 않다는 의미)
- local and global informations
  - attention mean distances를 재봄.
  - 신기하게도 lower layer는 attention된 레이어간의 mean distance가 higher layer보다 뚜렷히 작은 경향을 보여줌 -> lower layer는 local을 중요하게 판단한다.
  - 더 신기한 것은 pre train을 약간만 진행할 경우 레이어 간의 mean distance 차이가 pre train이 잘 된 경우보다 훨씬 작음. -> pre train이 잘될수록 lower layer에서 local 정보를 잘 본다.
- representation propagation through skip connection
  - skip connection의 long branch (MLP or Self Attention)를 $$f(z_i)$$라 할 때, $$\left\lVert z_i \right\rVert / \left\lVert f(z_i) \right\rVert$$를 계산함
  - 결과는 lower layer에서는 cls 토큰만 굉장히 높은 값을 가지고, 나머지는 낮은 값을 가짐. 레이어를 절반 정도 거치면 그 값이 역전됨
  - 레이어 간의 이런 norm ratio의 뚜렷한 경향 -> skip connction이 ViT에서 중요한 역할
  - 특정 레이어에서 skip connection을 없애고 학습해볼 떄 representation structure가 망가짐.
    - 성능도 4%정도나 떨어짐
- spartial information and localization
  - ResNet과 비교해서 higher layer에서 얼마나 spatial한 정보를 잘 담고 있을까?
  - ViT이 localization을 뚜렷히 잘함 -> 왜 그럴까?
    - 이유는 ResNet은 classification task를 풀기 위해 average pooling을 거쳐야하지만, ViT은 `CLS` 토큰이 존재하기 때문인 것으로 보임
    - 그 근거로 ViT을 global average pooling으로 학습시키면 localization이 약해짐
  - 10-shot imagenet을 해볼경우 `CLS` 토큰으로 학습시킨 ViT은 `CLS` 없이 각 토큰으로 classify할 경우 거의 못함 -> 반면에 ResNet이나 GAP으로 학습시킨 ViT은 꽤 잘 해냄.
    - localization을 잘한다는 것은 한 토큰이 전체 정보를 담는게 아니라 그 토큰을 이해하는데 필요한 정보만을 담기 때문
- effect of scale on transfer learning
  - lower layer는 적은 데이터로도 representation이 좋아지는데, higher layer는 많은 데이터를 보지 않으면 representation이 좋아지기 힘듦
  - 큰 모델일수록 higher layer가 더 많은 데이터를 필요로 함
  - 좋은 분석을 잘 해주었지만, 정리하면 `많은 데이터/큰 모델일수록 굉장히 잘한다.` 정도

---

태스크에 직접 적용한다거나 하진 못하겠지만, 재밌는 인사이트를 주는 논문이어서 재밌게 읽었다. ViT을 활용할 일이 생긴다면 모델의 경향을 잘 파악하기 위해서 읽으면 좋은 논문으로 보인다.
