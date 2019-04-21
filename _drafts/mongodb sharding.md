---
layout: post
title: 🍃 Mongo DB Sharding
tags:
  - db
---

데이터베이스를 사용하면서 언제까지나 인스턴스 하나만을 사용할 수는 없다. 데이터베이스에 많은 부하가 몰린다면, 다른 대책이 필요하다. 두 가지 방법이 존재하는데, Vertical Scaling과 Horizontal Scaling이다. Vertical Scaling은 하나의 머신에 더 많은 RAM과 더 많은 코어 등을 추가하는 방법이다. Horizontal Scaling은 여러 대의 머신을 구성하는 방법이다.

데이터베이스를 구성하면서 horizontal scaling을 하는 대표적인 방법은 replica를 늘리는 것이다. mysql의 경우는 read replica를 여러대 생성하여 write는 master에서 실행하고 read 작업은 replicated된 노드에서 실행하여 부하를 분산시킨다.

mongodb도 그러한 개념의 기능을 지원하는데, sharding이다. [mongodb의 문서](https://docs.mongodb.com/manual/sharding/)에서는 아래처럼 설명한다.

> Sharding is a method for distributing data across multiple machines. MongoDB uses sharding to support deployments with very large data sets and high throughput operations.

시스템이 더 이상 부하를 견디지 못할 때, sharding을 통해 가용성을 늘려주고, 버틸 수 있는 throughput도 늘려주는 것이다.

## [Sharded Cluster](https://docs.mongodb.com/manual/reference/glossary/#term-sharded-cluster)

mongodb의 sharded cluster는 3가지 component로 구성된다. shard, mongos와 config server이다.

### [Shard](https://docs.mongodb.com/manual/core/sharded-cluster-shards/)

shard는 sharded cluster안에서 sharded data의 subset을 가진다. cluster의 shard들에 존재하는 데이터를 합하면 원본의 데이터가 된다. 그래서 하나의 shard에 대해서 query를 실행하면, 해당 shard안의 데이터에 대해서만 결과를 가져온다. cluster level에서 query를 실행하고 싶다면, mongos를 사용하자.

shard는 고가용성을 위해 반드시 [replica set](https://docs.mongodb.com/manual/reference/glossary/#term-replica-set)으로 구성되어야 한다.

하나의 데이터베이스 안에서 primary shard는 반드시 존재한다. primary shard는 shard되지 않은 모든 collection들을 저장한다. 다만, 이름에서 혼동이 올 수 있는데, primary shard는 replica set의 primary와 관계가 없다.

### [mongos](https://docs.mongodb.com/manual/core/sharded-cluster-query-router/)

mongodb는 각각의 shard에 대해 query를 분산시키기 위해 mongos라는 instance를 제공한다. mongos에 대한 역할에 대해서는 아래처럼 mongodb 문서가 설명한다.

> `mongos` provide the only interface to a sharded cluster from the perspective of applications. Applications never connect or communicate directly with the shards.

적절한 shard로 route하기 위해서 config server로부터 metadata를 캐싱해두고 있다. 하지만, persistent state는 없다.

query를 routing하는 방법에 대해서는 문서를 참고해보자.

### [config server](https://docs.mongodb.com/manual/core/sharded-cluster-config-servers/)

config server는 sharded cluster에 대한 metadata를 저장하는 서버이다. 모든 shard에 대해 어떤 chunk를 들고있는지의 정보를 가지고 있는데, 해당 metadata를 mongos에서 활용하여 query를 route한다.

또한 추가적으로 mongodb가 distributed lock을 관리하기 위해 config server를 사용한다고 하는데, 이는 잘 모르겠다..

config server에 대해서도 replica set을 구성해야 할텐데, 이는 나중에 알아보자.

### 보안

sharded cluster는 보안을 위해서 [internal authentication](https://docs.mongodb.com/manual/core/security-internal-authentication/)을 사용할 수 있다. mongod에 각각 보안 설정을 넣어주어야 하는 점을 잊지 말자. 실제로 구성하기 위해서는 [Deploy Sharded Clsuter wit Keyfile Access Control](https://docs.mongodb.com/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control/)을 참고하자.

## 이를 통해 얻는 장점들

Read Write가 분산되어 잘 실행되는 것과 저장소를 확장할 수 있는 것은 당연하고, 제일 궁금한 것은 "고가용성이 보장되는가?"이다. 그에 대해 문서에 설명되어 있는데, 아래처럼 적혀있다.

> A sharded cluster can continue to perform partial read / write operations even if one or more shards are unavailable. While the subset of data on the unavailable shards cannot be accessed during the downtime, reads or writes directed at the available shards can still succeed.

하나의 shard를 사용할 수 없을 때, 다른 shard에 대해서 여전히 query를 실행할 수 있다고 한다.

## 실제로 구성해보기

깔끔하게 구성을 해보기 위해 docker를 통해서 구성해보겠다. 일단 container 사이를 이어주기 위해 network부터 만들어주고, docker image부터 받아주자.

```zsh
❯ docker pull mongo
Using default tag: latest
latest: Pulling from library/mongo
...

~
❯ docker network create mongo
0836403418d33db29b701e6911f641048d0a880720c88a6de4d3a9f3c4376bc5

~
❯ docker network ls
NETWORK ID          NAME                                DRIVER              SCOPE
...
...
0836403418d3        mongo                               bridge              local
```

### config server 구성하기
