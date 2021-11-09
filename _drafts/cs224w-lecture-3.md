---
layout: post
title: "CS224W Lecture 3 Node Embeddings"
tags:
  - cs224w
---

- [CS224W](http://web.stanford.edu/class/cs224w/)
- [Youtube link](https://www.youtube.com/watch?v=rMq21iY61SE)

## Introduction

- traditional ml for graphs
  - input-graph => feature-engineering => structured feature => learning algorithm => prediction
- graph representation learning
  - input-graph => ~~feature-engineering~~ **representation learning** => structured feature => learning algorithm => prediction
  - goal: efficient task-independent feature learning
  - task: map nodes into an embedding space
    - possible downstream tasks: node classification, link prediction, graph classification, anomalous node detection, clustering, ...

## node embeddings: encoder and decoder

- encoder: maps from nodes -> embeddings
- decoder(similarity function): maps embeddings -> similarity scores
- learning node embeddings: optimize parameters of the encoder
- simplest approach: encoder is just an embedding-lookup (DeepWalk, node2vec)
- deep encoders -> lecture 6
- objective: maximize similarity score for node pairs that are similar
- key choice: how can we define node similarity

## random walk approaches for node embeddings

![random walk](/images/cs224w/lecture3-random-walk.png)

- similarity score approximates a probability that two nodes co-occur on a random walk over the graph
- why random walk?
    ![why?](/images/cs224w/lecture3-random-walk-why.png)

## embedding entire graphs
