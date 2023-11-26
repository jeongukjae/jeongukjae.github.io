---
layout: post
title: CS224n Lecture 9 Practical Tips for Final Projects
tags:
  - cs224n
---

이번 강의는 유튜브로 업로드되는 강의는 아니고, 슬라이드와 노트만 올라왔다. 하지만 한번 충분히 훑어볼만한 것 같아서 정리를 해본다.

## final projects

스터디 하는 사람들끼리 final project도 기본으로 주어지는 프로젝트를 구현해보기로 했기 때문에 이번 강의 슬라이드를 살펴보기로 했다. SQuAD question answering이 기본 final project이다. 1 ~ 3명의 인원으로 한다고 한다. 언어나 프레임워크의 제한은 없다고. 그리고 기본적으로 주어지는 starter code가 pytorch라고 한다.

## research topic

일단 final project의 주제는 기본적으로 SQuAD이지만, project type (topic)도 정해야 한다고 한다.

1. 모델의 application을 찾아보고 어떻게 효율적으로 적용할 지 찾거나
2. complex neural architecture를 구현해보고 특정 데이터에 대한 performance를 측정해보거나
3. new, variant NN model을 구현해서 실험적인 데이터로 향상을 보여주거나
4. 모델의 동작법을 분석하거나
5. rare theoretical project, 그냥 개쩌는 걸 가져오거나..?

대충 위의 다섯가지를 보여주었다.

## finding data

데이터는 알아서 만들어서, 회사에서 쓰는걸 샘플만 들고와서 쓸 수도 있지만, 이미 잘 선별된 데이터셋을 쓰는 것도 좋다. 아래의 사이트들을 참고해보자.

* [https://catalog.ldc.upenn.edu](https://catalog.ldc.upenn.edu)
* [https://linguistics.stanford.edu/resources/resources-corpora](https://linguistics.stanford.edu/resources/resources-corpora)
* [http://statmt.org](http://statmt.org)
* [https://universaldependencies.org](https://universaldependencies.org)
* 역시 갓갓 캐글
* research paper 참고하는 것도 좋음
* [github - niderhoff/nlp-datasets](https://github.com/niderhoff/nlp-datasets)
* [https://machinelearningmastery.com/datasets-natural-language-processing/](https://machinelearningmastery.com/datasets-natural-language-processing/)

## review of gated neural sequence models

이 부분은 역시 강의가 없으니 이해하기 힘들어서 눈에 보인 것만 정리하자면

* 직관적으로 RNN에서 무슨 일이 일어나는지 이해하고 사용하자 (이거 잘 모르겠다)
* vanishing gradient 문제를 조심하자
* naive transition function (tanh같은)을 쓰는 것이 문제가 될까..? -> 내 생각에는 될 것 같지만 아직 확실하지 않다.
* backprop은 잘 안될수도 있다.
  * shortcut connection을 만들 수 있다.
  * adaptive shortcut connection도 만들 수 있다. -> 선택적으로 unnecessary connection들은 없앤다.

## a couple of MT topics

자 그래서 좀 문제로 여겨지는 topic들은?

* softmax computation이 너무 cost가 크다.
* word generation problem -> 이거 슬라이드 이해를 못하곘다 ㅠㅠㅠ

그래서 Hierarchical softmax 사용가능하고 noise contrastive estimation도 사용이 가능하다. attention도 사용이 가능하고 일단 키워드만 적었다.

그럼 Evaluation은 어떻게 할 수 있을까?

automatic metric을 사용할 수도 있는데, BLEU나, TER, METEOR같은 것들을 사용할 수 있다. 실제로 사용할 때 여기 다시 봐야겠다.

## doing your research

한번 에시를 들어보자면,

1. summarization이라는 task를 정하자
2. dataset을 정하자
    1. search for academic datasets
        1. newsroom summarization dataset을 사용한다!
    2. define your own data (harder one)
        2. 트윗, 블로그 포스트, 뉴스들도 데이터셋이 될 수 있다.
3. dataset hygiene
    1. 시작할 때 바로 테스트셋같은 것은 분리해두자
4. metric도 정하자!
    1. summarization은 rouge같은 것도 쓸 수 있다.
5. baseline을 정하자
    1. 너무 잘나오면 문제가 너무 쉬웠던 거다. 다시하자
6. Always be close to your data!
    1. visualize the dataset
    2. collect summary datset
    3. look at erros
    4. analyze how different hyperparameters affect performance
7. 다른 시도도 많이 해보자

이런 내용도 같이 있다.

* overfit도 조심해라
* validation이랑 test set을 따로 두고 잘 살펴보아라
* training/tuning/dev/test set같은 것을 잘 구분해라

RNN을 학습할 땐 아래와 같은 내용도 살펴보자

1. LSTM이나 GRU를 써보자
2. orthogonal하게 recurrent matrices를 초기화하자
3. 다른 matrices들을 sensible scale로 만들자
4. forget gate bias를 1로 두자 (default to remembering이다)
5. adaptive learning rate를 사용하자
6. clip the norm of the gradient. (1 ~ 5가 적당한 threshold이다)
7. dropout을 vertically하게 적용시키거나 Bayesian Dropout을 사용하자
8. 학습은 좀 기다리자
