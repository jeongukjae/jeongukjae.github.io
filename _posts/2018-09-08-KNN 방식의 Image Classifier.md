---
layout: post
title: "KNN 방식의 Image Classifier"
tags:
  - cs231n
  - python
  - numpy
  - machine learning
---

사실 이전 포스트에서 [한번 작성했던 글](/CS231n-KNN-방식의-Image-Classifier/)인데, 일년이 넘어서 다시 정리하기로 생각했다. (GitHub에도 과제들을 레포지토리로 다시 정리하기로 했다.)

[CIFAR - University of Toronto](https://www.cs.toronto.edu/~kriz/cifar.html)에서 데이터셋을 가져왔다.

Jupyter notebook으로 작성을 했고, GitHub Repository 링크는 [여기](https://github.com/JeongUkJae/CS231n-assignments/blob/master/assignments1/knn_image_classifier.ipynb)이다

소스코드는 아래에 있다.

```Python
#!/usr/bin/env python
# # KNN Image Classifier
# 
# * Dataset from [University of Toronto - CS](https://www.cs.toronto.edu/~kriz/cifar.html)
# * [list of CS231n assignment 1](http://cs231n.stanford.edu/slides/2017/cs231n_2017_lecture2.pdf)
# * This KNN image classifier is a first assignment of CS231n.

import numpy as np
import pickle

# Hyperparameters
K = 3

# a function that loads data from file
def unpickle(file):
    with open(file, 'rb') as fo:
        data = pickle.load(fo, encoding='bytes')
    return data

# Manhattan distance
def L1_distance(x, y):
    return np.abs(np.sum(x - y))

# Euclidean distance
def L2_distance(x, y):
    return np.sqrt(np.abs(np.sum((x-y) ** 2)))

batches = {'data': [], 'label': []}

def train(data, labels):
    # Training process of KNN is just remembering all images and labels.
    batches['data'].extend(data)
    batches['label'].extend(labels)
    
def predict(item, distance=L1_distance):
    min_values = []
    min_labels = []
    
    data = batches['data']
    labels = batches['label']
    
    for index in range(len(data)):
        d = distance(item, data[index])
        
        if len(min_values) < K:
            min_values.append(d)
            min_labels.append(labels[index])
        elif max(min_values) > d:
            removed_item_index = min_values.index(max(min_values))
            min_values[removed_item_index] = d
            min_labels[removed_item_index] = labels[index]

    majority = max(min_labels, key=min_labels.count)
    
    return majority

data_batch_1 = unpickle('../cifar-10-batches-py/data_batch_1')
test_batch = unpickle('../cifar-10-batches-py/test_batch')

print("key of data_batch_1: ", data_batch_1.keys())
print("the number of images in data_batch_1: ", len(data_batch_1[b'labels']))
print("the number of images in test_batch: ", len(test_batch[b'labels']))

# train data_batch_1
train(data_batch_1[b'data'], data_batch_1[b'labels'])

correct_l1 = 0
correct_l2 = 0

count = 0

for index in range(len(test_batch[b'data'])):
    data = test_batch[b'data'][index]
    label = test_batch[b'labels'][index]
    
    kNN_output = predict(data)
    kNN_output_l2 = predict(data, distance=L2_distance)
    
    if kNN_output == label:
        correct_l1 += 1
    if kNN_output_l2 == label:
        correct_l2 += 1
    count += 1
    
    print(f"index {index}, label is {label}, and predicted label is {kNN_output} and {kNN_output_l2}")
    
    if count == 100:
        break

print("accuracy of kNN using L1 distance: ", 100 * correct_l1 / count, "%")
print("accuracy of kNN using L2 distance: ", 100 * correct_l2 / count, "%")
```

아무래도 학습한 10000개의 데이터(test batch 1 만 사용했다.)를 다 일일히 비교하다보니까 너무 느리다..
