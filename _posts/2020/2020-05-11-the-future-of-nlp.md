---
title: "🤗 The Future of Natural Language Processing - Model Size and Computational Efficiency"
layout: post
tags:
  - nlp
---

HuggingFace에서 올린 슬라이드/영상인 The Future of Natural Language Processing이 최근 NLP 전반에 대한 오버뷰를 잘 제공하고 있는데, 이 세션에서 나오는 내용들 중 Model Size, Computational Efficiency와 관련된 부분에 대해서 간단한 내용과 내 생각과 함께 정리해본다.

[Youtube 링크](https://www.youtube.com/watch?v=G5lmya6eKtc) | [슬라이드 링크](https://docs.google.com/presentation/d/1k3Npb47q5_p2cnY0IvLwwSdS0tHg3ctJLUz1s6vgDLk/edit#slide=id.g6e76c30798_0_0)

## Bigger Size and More Data!

computational efficiency와 관련된 부분은 아무래도 최근 BERT 이후로 급격하게 필요성이 커지고 있다. Transformer Encoder 블럭이 24 layer인 BERT Large만 하더라도 340M 정도의 파라미터를 가지고 있어서 실시간 추론 & 서빙이 힘들기 떄문에 각 회사들에서 많은 노력을 하고 있다. 심지어 최근 나오는 모델들 중 T5는 1B를 넘고 Meena와 같은 경우는 2.6B이다.

ZeRO, Metatron등으로 해결이 가능하겠지만, Model/Data Parallelism은 필수 불가결한 상황이 되었다. T5는 아래처럼 논문에 서술해놓았다.

> Training large models can be non-trivial
> since they might not fit on a single machine and require a great deal of computation. As a result,
> we use a combination of model and data parallelism and train models on “slices” of Cloud TPU Pods.

그럼 왜 큰 모델이 문제가 될까? Research Competition field를 단순하게 만들고, CO2 배출량을 증가시킨다. 물론 그게 정말로 단순해지겠냐만서도 아래 트윗은 많은 생각을 하게 한다.

<center><blockquote class="twitter-tweet"><p lang="en" dir="ltr">Training ever bigger convnets and LSTMs on ever bigger datasets gets us closer to Strong AI -- in the same sense that building taller towers gets us closer to the moon.</p>&mdash; François Chollet (@fchollet) <a href="https://twitter.com/fchollet/status/1122330598968705025?ref_src=twsrc%5Etfw">April 28, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script></center>

아마도 `성능 향상 == 큰 모델`이 굳어져 가는 것이 *비록 잘 되더라도,* 아쉬운 모양새인 사람이 많은가보다. CO2 배출량은 [Strubell et al., 2019](https://arxiv.org/abs/1906.02243)을 살펴보자. 하나 예시를 들고와보자면 뉴욕에서 샌프란시스코를 비행할 때 CO2 배출량이 1984 lbs인데, V100 64장을 사용하고 79시간이 소요된 BERT base 학습은 1438 lbs의 CO2를 배출한다.

## 그럼 모델을 작게 만들어볼까?

그럼 모델을 작게 만드는 연구 방향은 없을까? 당연히 있고, Pruning을 진행하는 [Lecun et al., 1989](https://papers.nips.cc/paper/250-optimal-brain-damage)부터 찾아볼 수 있다. 이 논문에서는 아래처럼 말한다.

> By removing unimportant weights from a network, several improvements can be expoected: better generalization, fewer training examples required, and improved speed of learning and/or classification.

그럼 **구체적으로** 모델을 작게 만드는 것은 어떤 방법들이 있을까? Distillation, Pruning, Quantization 등이 있다.

### Distillation

Distilation은 그 중 대표적인 방법 중 하나로, "Teacher 모델을 이용해 Student 모델을 어떻게 잘 학습시키나" 정도로 요약이 가능하다. HuggingFace에서 만든 자료이니 DistilBERT를 예시로 보자면 **40% 모델 사이즈와 60% 빠른 속도로 BERT 성능의 95%를 보존**이 가능하다. 최근에도 [Tsai et al., 2019](https://arxiv.org/abs/1909.00100), [Turc et al., 2019](https://arxiv.org/abs/1908.08962), [Tang et al., 2019](https://arxiv.org/abs/1903.12136)과 같은 연구들이 많이 진행되고 있다. 또한 이전에 리뷰했던 TinyBERT도 그 중 하나이다.

Adaptive Inference를 위한 Self Distillation 연구도 꽤 보인다는 느낌을 받는데 주로 [Slimmable Neural Network](https://arxiv.org/abs/1812.08928)와 같은 연구에서 많은 영감을 받은 것으로 보인다.

### Pruning

두번째 방법인 Pruning은 중요도를 계산하고 성능에 영향을 끼치지 않는 네트워크를 제거하는 방식이다. 진짜 단어의 뜻 그대로 가지치기라 생각하면 된다. [Elena Voita et al., 2019](https://arxiv.org/abs/1905.09418), [Paul Michel et al., 2019](https://arxiv.org/abs/1905.10650)과 같이 Multi Head Attnetion에 적용이 가능한 연구들도 지속적으로 이루어지고 있다. 그 외에도 [Wang et al., 2019](https://arxiv.org/abs/1910.04732)처럼 Weight Pruning을 사용해 **65%의 파라미터만 가지고 99%의 성능을 보존**하는 연구도 있으며, 최근 ICLR 2020에 Accept된 [Fan et al., 2020](https://arxiv.org/abs/1909.11556)과 같이 Transformer Depth를 줄이는, Layer Pruning을 진행하는 연구도 있다.

대부분의 네트워크는 Dense Matrix Multiplication을 염두에 두고 디자인, 연구가 이루어지는데, Sparse Model도 최근 많은 연구가 이루어지고 있다. 개인적인 생각은 모델 사이즈나, 효율성으로 볼 때, 물론 GPU상에서 효율적인 Sparse Matrix 연산이 어렵지만, Sparse Model들에 대한 연구가 활발히 이루어지면 좋겠다는 생각을 많이 한다. 분명히 어려운 분야이지만 좋은 성능을 유지가능하다면 Memory Consumption이나 Inference Speed 부분에서 1.nx 같은 "개량"정도의 성능 향상보다는 Nx 정도의 엄청난 향상을 볼 것이 너무 분명하기 때문이다. 관련 연구는 Open AI의 글인 [Block-Sparse GPU Kernels](https://openai.com/blog/block-sparse-gpu-kernels/), Balanced Sparsity ([Yao et al., 2018](https://arxiv.org/abs/1811.00206))등부터 보면 좋을 것 같다.

### Quantization

세번째 방법은 Quantization인데, Tensor들을 downcasting 후 연산을 진행하는 방법이다. 최근에는 CPU Inference를 위해 INT8로 줄이는 것이 대세가 된 듯 하고, PyTorch 튜토리얼의 [(EXPERIMENTAL) DYNAMIC QUANTIZATION ON BERT](https://pytorch.org/tutorials/intermediate/dynamic_quantization_bert_tutorial.html)이나 [Q8BERT](https://www.intel.com/content/www/us/en/artificial-intelligence/posts/q8bert.html)를 참고해보면 좋을 것 같다.

개인적으로 생각하는 이 분야의 핵심은 "어떻게 Distribution을 잃지 않고 잘 매핑할 수 있을끼?"이다. Quantization은 Tensor들을 Downcast하니 정보를 잃을 수 밖에 없는데, 이 점을 해결하기 위해 Fake Quantized Tensor를 사용하는 Quantization Aware Training이나 Post Training Quantization을 Calibration Data와 함께 적절한 Threshold를 찾아 outlier를 제외하는 방식의 quantization이 잘 되는 것 같다.

다만 아직 아쉬운 점은 Intel CPU가 아무래도 AWS에서 많은 점유율을 차지하고 있고, TensorFlow가 서빙에 강세를 보이는 것은 자명한 사실인데, TensorFlow의 INT8 연산 지원이 아직은 활발하지 않다는 점이다. TensorFlow가 사용하는 라이브러리중 하나인 [google/gemmlowp](https://github.com/google/gemmlowp)에서도 아직 AVX2지원이다. VNNI를 사용하기 위해 (아마 Custom Ops로 사용한 것으로 보이는데) 직접 몇몇 연산자를 개발해 사용한 [Bhandare et al., 2019](https://arxiv.org/abs/1906.00532)와 같은 경우를 볼 때 더 TensorFlow 자체에서 지원이 활발하면 좋겠다는 생각이 든다. TF Lite가 INT8 연산을 지원하긴 하지만, 직접 int8 연산을 미세하게 조정하여 사용할 수 있는 연산의 지원이 미약해보인다.

## _

되게 재밌는 영상이고 설명을 잘해준다. 모델 경량화와 관련된 주제는 메인이 아닐뿐더러, Continual and Meta Learning, Common Sense Question, Out of domain generalization, NLU vs NLG등의 재밌는 주제도 많이 다룬다.
