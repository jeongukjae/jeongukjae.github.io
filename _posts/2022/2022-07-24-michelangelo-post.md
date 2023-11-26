---
layout: post
title: "우버 - Michelangelo blog post"
tags:
  - Operation
  - ML
---

우버의 [Meet Michelangelo: Uber’s Machine Learning Platform](https://eng.uber.com/michelangelo-machine-learning-platform/) 블로그 포스트를 보고 핵심만 정리해보았다. 2017년 9월 글인데, 이 시기에 MLOps에 대해 이렇게 잘 정리했다는 것에 놀랐다.

특히나 정말 좋아보이는 것은 Shared feature store를 관리함으로써 생기는 여러 이득이다.
예를 들어 나중에는 모델링 문제만 나온다면 자동으로 importance score가 높은 피쳐들만 모아서 보여준다던가 하는 기능을 생각하는 것 같은데, (지금은 이미 잘 쓰고 있을 수도) 정말 좋아보인다.

---

- Michelangelo: 우버의 비전을 더 효율적으로 달성하기 위한 내부 ML-as-a-service platform
    - 우버 스케일에 맞게 머신러닝 솔루션을 개발하고 배포, 운영할 수 있는 e2e 플랫폼이고, 우버의 production use cases의 de-facto.
    - 데이터 관리, 모델 학습, 평가, 배포, 추론, 모니터링 등의 기능을 지원

## **Motivation behind Michelangelo**

- Michelangelo 이전
    - 각자 만들다보니, ML로 영향을 주는 것이 소수의 데이터 사이언티스트들과 엔지니어가 짧은 시간안에 오픈소스 도구로 구축할 수 있는 것에 제한됨.
        - 데이터 사이언티스트들의 데스크탑에서 돌릴 수 없는 큰 모델을 사용하는 것도 불가능에 가까움
        - 모델, 실험 결과등을 저장하는 스탠다드도 존재하지 않음
    - 프로덕션으로 배포하는 일반화된 과정이 없음
    - 수많은 기술부채가 쌓이게 됨
- 그래서 Michelangelo를,
    - 단순히 이러한 문제를 푸는 것만이 아닌 회사의 성장에 따라 같이 성장할 수 있는 플랫폼을 개발
    - 개발자의 생산성에 주목; 첫 프로덕션 모델을 빠르게 만들고, 이터레이션을 더 빠르게 돌 수 있도록

## **UberEATS 유즈 케이스 (배달 시간 예측)**

- 우버 이츠에는 배달 시간 예측, 검색 랭킹, 검색 자동완성, 음식점 랭킹 등 많은 머신러닝 모델이 존재
- 그 중 배달 시간 예측에는 수많은 변수가 존재; 가게가 얼마나 바쁜지, 주문이 얼마나 복잡한지, 교통량이 어떠한지, 주차장이 어떠한지, …
- 각 스텝을 잘 계산하면서 토탈 시간도 잘 계산해야 함
- Michelangelo 상에서 여러가지 피쳐를 이용해 gradient boosted decision tree regression 모델 학습
- Michelangelo 모델 서빙 컨테이너를 통해 배포되고, 우버이츠 마이크로서비스에서 네트워크 요청을 보내서 추론함

## **System architecture**

- 여러 오픈소스(HDFS, Spark, Samza, Cassandra, MLLib, XGBoost, TensorFlow)를 활용해 만든 시스템.
    - 성숙한 오픈소스 선택을 좋아하고, 필요한 경우 fork, customize, contribute back 함
- 우버의 인프라 위에 구축되어 있고, 아래와 같은 컴포넌트가 같이 제공
    - 우버의 로그, 거래 데이터가 저장된 데이터 레이크
    - 우버 서비스들로부터 나오는 로그를 전달하는 Kafka broker
    - 연산 처리를 위한 Samza
    - 관리형 Cassandra cluster
    - 우버 인하우스 배포 도구

## **Michelangelo의 Machine learning workflow**

- workflow는 implementation-agnostic해서 쉽게 확장 가능.
- 아래와 같은 컴포넌트들로 이루어짐

1. Manage data
    - 요구사항
        - 회사의 데이터 레이크, 온라인 데이터 서빙 시스템과 잘 연동되어 있어야 함
        - Scalable, Performant한 구조, 데이터 플로우와 퀄리티를 위한 모니터링, 온/오프라인 학습과 추론 환경을 지원
        - 일의 중복과 데이터 퀄리티를 위해 팀 간 공유가 가능하도록 피쳐 생성해야 함
    - Offline
        - transactional data, log data는 HDFS 데이터 레이크로 쌓이고 있고, Spark, Hive SQL을 통해 쉽게 접근 가능
        - 피쳐 계산을 위해 컨테이너와 스케쥴링을 제공 (프로젝트 단인지, 피쳐스토어 publish까지 되는지는 선택가능)
        - 배치 계산이 되면서 데이터 퀄리티 모니터링을 수행
    - Online
        - 배치성 작업으로 계산한 HDFS 내부의 데이터에 접근하는 것은 어렵기 때문에, 해당 피쳐를 Cassandra에 저장해서 추론 때 짧은 지연시간 내에 읽을 수 있도록 만듦
        - 두 가지 타입의 온라인 피쳐를 제공
            - batch precompute
                - 벌크로 미리 계산된 피쳐를 HDFS에서 카산드라로 적재.
                - 간단하고 효율적이며 historical feature에 대해 잘 작동한다.
                - N 시간마다 업데이트되거나 하루에 한번 업데이트되는 피쳐들에 대해 좋다.
                - 학습과 서빙에 동일한 피쳐가 사용되는 것을 보장.
            - near-real-time compute
                - Kafka와 Samza based streaming compute job을 사용하여 계산.
                - 카산드라에 바로 쓰여지는 피쳐 종류이고, HDFS에는 로그 적재
                - HDFS에 적절하게 쌓인다면 학습과 서빙에 동일한 피쳐가 사용되는 것을 보장
                - cold start를 피하기 위해 backfill을 지원해야 함.
        - Shared feature store
            - 쉽게 피쳐를 만들고 관리하며, 팀간에도 간단히 피쳐를 공유할 수 있음
            - 아래 두가지를 달성하도록
                - 피쳐 스토어에 쉽게 피쳐를 추가할 수 있음. 그 때 Owner, Description, SLA 등의 적은 메타데이터만 필요.
                - 모델 설정에서 canonical name을 참조하는 것으로 온오프라인상에서 쉽게 피쳐를 사용할 수 있음.
            - 미래에는 주어진 prediction problem이 있다면 가장 유용하고 좋은 피쳐를 찾아주는 자동 시스템도 고려 중
        - DSL for feature selection and transformation
            - 모델러들이 select, transform, combine을 할 수 있는 DSL을 개발. (Scala의 서브셋)
            - DSL expression은 모델의 설정으로 들어가게 됨.
            - 같은 DSL expression이 학습/서빙 시에 피쳐 전처리를 담당하도록 함

2. Train models
    - 여러가지 학습 알고리즘을 돌릴 수 있는 환경
        - 필요 시 Uber의 AI Labs에서 새로운 알고리즘을 추가
    - 모델 설정에 포함되는 값들: 모델 종류, 하이퍼파라미터, 데이터 소스, 피쳐 DSL 표현식, 리소스, …
    - 모델 학습 후에 메트릭, 설정 값, 모델 가중치, 평가 리포트 등이 모델 레포지토리에 저장
    - 하이퍼 파라미터 튜닝 등을 지원
    - web UI, API, 혹은 Jupyter Notebook을 통한 학습 지원

3. Evaluate models
    - Michelangelo로 학습된 모델들은 카산드라에 버저닝하여 저장. 아래 정보 포함
        - Author
        - start, end time of training job
        - model configuration
        - training, test data references
        - chart, graph for each model type (ROC/PR curve, confusion matrix)
        - model parameters
        - summary statistics for model visualization
    - Model Accuracy Report
        - **이 부분은 실제 블로그 글로 들어가서 이미지를 같이 보자.**
    - Decision tree visualization
        - 왜 모델이 해당 방식대로 추론하는지 등을 시각화
        - 디버그에 도움이 됨
        - **이 부분은 실제 블로그 글로 들어가서 이미지를 같이 보자.**
    - Feature report
        - 모델에게 중요한 순으로 피쳐를 시각화
        - **이 부분은 실제 블로그 글로 들어가서 이미지를 같이 보자.**

4. Deploy models
    - 아래와 같은 방식들을 지원
        - offline deployment
            - offline 컨테이너로 배포, spark job에서 배치 추론을 하기 위한 용도
        - online deployment
            - 서비스 클러스터에 배포, RPC Call을 받아내기 위한 용도
        - library deployment
            - 라이브러리 형태로 서빙 컨테이에 포함시켜 배포, 다른 서비스 혹은 Java API 내에서 부르기 위한 용도

5. Make predictions
    - 추론 과정
        - Raw 피쳐가 컴파일된 DSL 표현식으로 전달, 피쳐 스토어에서 추가 피쳐 가져와서, 모델로 전달
        - online 배포인 경우 네트워크로 아니면 Hive에 저장되어 job에서 다음 실행에 가져감
    - Referencing Models
        - A/B 테스트 등을 할 때 중요한 것은 각 모델을 잘 구분해서 다루어야 하는 것
        - UUID로 구분되고, 선택적으로 태그가 붙음
        - 온라인 모델의 경우 피쳐와 UUID를 보내야 추론이 가능
        - 오프라인 모델의 경우 prediction records가 UUID를 포함하고 있어, consumer에서 필터
    - Scale and latency
        - 머신러닝 모델은 stateless해서 scale out하기 쉬움
        - 온라인 모델은 서비스 클러스터에서 호스트 추가해서 LB에 추가함
        - 오프라인 모델은 Spark executor 추가해서 스파크에서 관리
        - 온라인 서빙 latency는 피쳐 스토어 찌르는 여부가 꽤 중요
            - 추가 피쳐 필요없는 경우 P95 latency가 5ms 정도
            - 추가 피쳐 필요한 경우 P95 latency가 10ms 정도
        - 가장 throughput이 높은 모델이 250,000 prediction per seconds 정도

6. Monitor predictions
    - 모델의 성능을 위해 추론을 모니터링하는 것은 중요함
        - 추론 값의 일정 비율을 샘플링하여 저장하고, 나중에 이 값을 실제 레이블과 대조해봄
        - 지속적으로 실제 모델 정확도를 비교가능
        - 우버의 time series monitoring system과 연동하여 시각화, 알람 등을 걸 수 있음
    - Management plan, API, and web UI
        - 우버의 시스템 모니터링, 얼럿 인프라와 연동하여 web UI, netwrok API도 같이 제공
        - Michelangelo를 쓰는 사람은 위 컴포넌트들을 web UI, REST API, 모니터링/얼럿 도구로 바로 접근 가능

## **Future works**

- 더 하고 싶은 것
- AutoML
    - 주어진 모델링 문제에 대해서 모델 설정(피쳐, 알고리즘, 하이퍼 파라미터)를 찾아내는 것.
    - 피쳐 스토어가 이미 존재하니 충분히 가능함
- Model Visualization
    - 딥러닝의 경우 모델을 이해하고 디버깅하는게 굉장히 중요
- Online Learning
    - Michelangelo를 사용해 주기적으로 학습하고 있지만, 더 빠른 학습과 평가, 높은 정확도를 위해 online learning이 목표
- Distributed Deep Learning
