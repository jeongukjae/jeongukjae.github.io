---
layout: post
title: "📕 CS224n Lecture 12 Information from parts of words: Subword Models"
tags:
  - nlp
  - cs224n
  - machine learning
---

12강까지는 저저번주에 들었던 것이지만, 이제 정리하려고 하니 제대로 기억이 안나서 다시 들으면서 정리한다.

## A tiny bit of linguistics

* phonetics: sound stream
* phonology는 phonemes로 이루어진다.

하나의 단어는 여러 개의 semantic unit으로 구성된 경우가 많은데, 예를 들어 `un- + fortun(e)- + -ate + -ly`와 같은 경우이다. "그럼 이런 정보를 모델에서 더 이용할 수는 없을까?" 라는 생각이 subword models의 메인 아이디어이다. (Wickelphones (Rumelhart & McClelland 1986), Microsoft’s DSSM (Huang, He, Gao, Deng, Acero, & Hect 2013))

그럼 모든 언어들이 단어를 구분을 해주는가는 또 아니다. 중국어를 예로 보면 word segmentation이 없다고 한다. (이 부분은 확실하지 않지만, 강의에서 나온 내용이다) 일본어를 보더라고 띄어쓰기를 하지 않는다.

word level model을 사용하면 large, open vocabulary가 필요하기 때문에 차라리 character level model을 사용하는 것은 어떨까?

## Purely character-level models

word embedding이 character embedding으로부터 구성할 수 있는 모델을 만든다. 따라서 모르는 단어도 embed할 수 있다는 장점이 있다. 그리고 비슷한 스펠링의 단어는 비슷한 임베딩을 가지게 된다. 따라서 Out of Vocabulary (OOV) Problem를 해결하게 된다. 그리고 connected language (중국어같은) 들도 자연스럽게 처리할 수 있게 된다. [^VDCNN]

[^VDCNN]: [Very Deep Convolutional Networks for Text Classification](https://arxiv.org/abs/1606.01781) 아주 좋은 예시

Purely Character Level NMT Model에 관심이 있으면 아래 목록을 찾아보자

* Vilar et al., 2007
* Neubig et al., 2013
* Junyoung Chung, Kyunghyun Cho, Yoshua Bengio. arXiv 2016
* Wang Ling, Isabel Trancoso, Chris Dyer, Alan Black, arXiv 2015
* Thang Luong, Christopher Manning, ACL 2016
* Marta R. Costa-Jussà, José A. R. Fonollosa, ACL 2016

그 이후 seq2seq를 character level로 만들어서 테스트를 했는데, word level baseline에 비해 나름 잘 동작했다. 하지만 training time이 3주나 걸리는 등 너무 느렸다.. (참고로 word level model이 BLEU가 15.7 점이었는데, character level modle이 15.9정도가 나왔다) English-Czech WMT 2015 결과였다고 한다.

그 외에도 [Jason Lee, Kyunghyun Cho, Thomas Hoffmann. 2017](https://arxiv.org/abs/1610.03017)도 참고해보면 좋을 것 같다. decoder로 char-level GRU를 사용했다고 한다. [Revisiting Character-Based Neural Machine Translation with Capacity and Compression](https://arxiv.org/abs/1808.09943)도 참고해보라고..

## Subword-models: byte pair encoding and friends

두가지 트렌드가 있는데, word-level model관련된 모델[^wp1][^wp2]이랑 (word pieces) hybrid 방식을 사용하는 모델이다. 일단 메인은 word-level이고, character level을 추가적으로 사용한다.[^hybrid1][^hybrid2]

[^wp1]: [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) 참고해보자
[^wp2]: [A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation](https://arxiv.org/abs/1603.06147) 참고해보자

[^hybrid1]: [Character-based Neural Machine Translation](https://arxiv.org/abs/1603.00810)
[^hybrid2]: [Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models](https://arxiv.org/abs/1604.00788)

### Byte Pair Encoding

Byte Pair Encoding은 원래 Compression Algorithm이다. most frequent byte pair를 병합하는 알고리즘 정도로 볼 수 있는데, [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909), [GitHub rsennrich/subword-nmt](https://github.com/rsennrich/subword-nmt), [GitHub EdinburghNLP/nematus](https://github.com/EdinburghNLP/nematus)를 참고하라고 한다.

### Wordpiece/SentencePiece model

wordpiece는 word안에서 tokenizing하는 모델. sentencepiece는 raw text에서 동작하는 모델인데, whitespace가 special token을 가지게 하고, grouping하는 등의 처리를 해주는 모델..?인가 싶다.

* [GitHub google/sentencepiece](https://github.com/google/sentencepiece)
* [Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates](https://arxiv.org/abs/1804.10959)

Bert가 wordpiece 모델의 variant를 사용한다. 다른 단어들을 wordpiece로 만들어낼 수 있기 때문에 이점이 있다고.

---

그 외에도 subword models로 볼 수 있는 모델들 중에 word embedding을 만들어내기 위해 convolution을 character들에 시키는 모델들도 있고, word representation을 위해 character based LSTM을 적용한 모델도 있다고 한다.

Highway Network도 나중에 살펴보자.[^HN]

[^HN]: [Highway Networks](https://arxiv.org/abs/1505.00387)

## Hybrid character and word level models

Hybrid NMT라고, 거의 word level에서 번역하고, 필요할 경우 char-level을 가는 모델도 있다고 한다.[^hybrid2]

## FastText

[A Joint Model for Word Embedding and Word Morphology](https://arxiv.org/abs/1606.02601)을 살펴보면 기본적으로 word embedding을 하기 위한 모델이지만 word morphology도 살펴볼 수 있는 모델이라고 한다.

[Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606)은 fastText의 논문인데, 실제 코드나 사용은 [https://fasttext.cc](https://fasttext.cc) 를 살펴보자
