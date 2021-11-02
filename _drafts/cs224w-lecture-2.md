---
layout: post
title: "CS224W Lecture 2 Traditional feature based methods"
tags:
  - cs224w
---

- [CS224W](http://web.stanford.edu/class/cs224w/)
- [Youtube link](https://www.youtube.com/watch?v=3IS7UhNMQ3U)

---

- This lecture
  - In traditional graph ml pipeline, features for nodes, link, and graphs are manullay desinged. (hand-designed features)
  - topic of this lecture: traditional features for ..
    - node level preiction
    - link level prediction
    - graph level prediction
  - for simplicity, we focus on undirected graphs
- Node level tasks
  - features
    - node degress
      - the number of edges the node has
      - nothing special, but very useful feature
    - node centrality
      - node degree counts the neighboring nodes without capturing importance.
      - different ways to model importance
        - eigenvector centrality
        - betweenness centrality
        - closeness centrality
        - and many others...
    - clustering coefficient
      - <https://en.wikipedia.org/wiki/Clustering_coefficient>
    - graphlets
      - clustering coefficient coutns the # triangles in the ego-networks
      - => so we can generalize it by counting # pre-specificed subgraphs
