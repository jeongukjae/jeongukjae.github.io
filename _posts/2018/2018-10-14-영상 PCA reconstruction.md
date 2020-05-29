---
layout: post
title: "영상 PCA reconstruction"
tags:
  - math
---

서울시립대학교에서 18학년 2학기에 수강하는 기계학습개론 과목을 들으면서, 과제로 영상 PCA reconstruction을 작성해보았다.

jupyter notebook을 이용해서 작성했고, [GitHub Repo](https://github.com/JeongUkJae/introduction-to-machine-learning-assignments) 의 homework2이다.

구현에 참고한 자료는 [Principal Component Analysis for Hyperspectral Image Classification](https://engineering.purdue.edu/~jshan/publications/2002/SaLIS_2002_HyperImagesPCA.pdf)[^paper1]이다.

## 내용

같은 크기의 이미지(m x n) N 장을 겹칠경우 (paper에서는 band라는 용어를 사용하더라) N-dim 벡터가 이미지 mn개 나온다. 이 벡터들의 공분산(covariance)를 구한 뒤, 공분산의 eigenvalues, eigenvectors($$A$$)를 구한다. 그리고 original image의 approximation을 구한다.
최종적으로 밑의 z_i을 다 모으면 PCA 이미지의 K개의 밴드가 구해진다. (z_i을 구하는 식에서 eigen vector를 K개를 넣는다.)

$$ \vec {x_i} = \pmatrix {x_1 && x_2 && x_3 && ... && x_n} _i ^T $$

$$ C_x = Cov(x) = \frac 1 M \sum ^M _{i=1} (x_i - m)(x_i - m)^T $$

$$ C_x = ADA^T, (D = diag(\lambda_1, \lambda_2, \lambda_3, ... \lambda_N)) $$

$$ \vec {z_i} = \pmatrix{eigen-vector1 \\ eigen-vector2 \\ ...} \vec{x_i} $$

(개인적으로 위의 식이 너무 신기했다. 선형 대수학 더 공부해야지.. 잘 보면 GitRepo의 homework2에서 In[6]의 출력과 Out[9]의 값이 같다.)

[^paper1]: https://engineering.purdue.edu/~jshan/publications/2002/SaLIS_2002_HyperImagesPCA.pdf Craig Rodarmel and Jie Shan, KEYWORDS: Hyperspectral images, image classification, land use, principal component analysis
