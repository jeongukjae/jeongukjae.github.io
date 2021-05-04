---
layout: post
title: "CLIP Self Attention Visualization"
tags:
    - python
    - note
---

<https://github.com/facebookresearch/dino>에서 볼 수 있듯 DINO가 Self supervised learning만으로도 굉장히 신기한 Self Attention 결과가 나오길래 CLIP으로도 해보고 싶어서 해봤다.

레포지토리 링크: <https://github.com/jeongukjae/CLIP-self-attention-visualization>

사용가능한 CLIP weight가 `ViT-B/32` 기반이라 Patch Size가 32px이어서 32px을 하나의 토큰으로 봤고, 입력 해상도도 `224px X 224px`이어서 결국 `7 X 7` 그리드가 입력인 셈이었다. VisionTransformer를 이번에 제대로 봤으니 실망은 안했는데, 그래도 원하는 만큼의 결과는 안나왔다.

---

PLACE365 데이터

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/place365_52.png?raw=true" width=60 %}

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/place365_350.png?raw=true" width=60 %}

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/place365_1250.png?raw=true" width=60 %}

---

CIFAR 100 데이터

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/cifar100_1.png?raw=true" width=60 %}

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/cifar100_12.png?raw=true" width=60 %}

{% include image.html url="https://github.com/jeongukjae/CLIP-self-attention-visualization/blob/main/cifar100_150.png?raw=true" width=60 %}

---

그래도 self attention 결과와 이미지가 실제로 연관이 있어보여서 재밌긴 했다.

이렇게 해보고 드는 생각은 사람의 시선을 트래킹해서 해당 정보로 self attention을 학습해보면 좋은 사전학습 모델이 나올까?? 정도 ㅋㅋㅋ
