---
layout: post
title: "[CS231n] Python Numpy Tutorial"
tags:
  - cs231n
  - python
  - numpy
  - machine learning
---

[Justin Johnson](http://cs.stanford.edu/people/jcjohns/)에 의해 작성된 튜토리얼을 공부용으로 번역 + 정리하였어요.

원문은 [링크](http://cs231n.github.io/python-numpy-tutorial/#python)로 들어가면 볼 수 있습니다.

개인적으로 크게 필요하지 않은 내용이거나, 별로 굳이 써야하는 내용이 아니면 건너 뛰었네요.

과학 연구용으로 자주 쓰이는 언어와 라이브러리들인 Python, Numpy, SciPy, Matplotlib의 사용법을 정리하였어요.

원문에는 밑의 목차처럼 있었는데, 여기 없으면 원문 보시면 돼요. 좀 생략한게 많아요.

* Python
	* Basic data types
		* Containers
		* Lists
		* Dictionaries
		* Sets
		* Tuples
	* Functions
	* Classes
* Numpy
	* Arrays
	* Array indexing
	* Datatypes
	* Array math
	* Broadcasting
* SciPy
	* Image operations
	* MATLAB files
	* Distance between points
* Matplotlib
	* Plotting
	* Subplots
	* Images

	
## Python

파이썬은 High-level, 동적 타입, multiparadigm 프로그래밍 언어이다. 읽기 매우 쉬운 언어이고 라이브러리들이 많아 자주 쓰인다. 예제로 작성한 파이썬으로 구현한 QuickSort는 다음과 같다.

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

print(quicksort([3,6,8,10,1,2,1]))
# Prints "[1, 1, 2, 3, 6, 8, 10]"
```

### Python Version

원문에는 2.7과 3.5를 언급해놓았다.

> There are currently two different supported versions of Python, 2.7 and 3.5. 

참고로 밑에 나오는 코드들은 전부 3.5 버전을 기준으로 쓰였다고 한다. 버전 확인은 ```python3 --version```으로 가능하다고 한다.

### Basic data types

파이썬도 다른 언어들처럼 Integers, Floats, Booleans, Strings 같은 자료형을 가지고 있다.

**Numbers** : 그냥 다른 언들 쓰는 것처럼 쓰시면 돼요.

```python
x = 3
print(type(x)) # Prints "<class 'int'>"
print(x)       # Prints "3"
print(x + 1)   # Addition; prints "4"
print(x - 1)   # Subtraction; prints "2"
print(x * 2)   # Multiplication; prints "6"
print(x ** 2)  # Exponentiation; prints "9"
x += 1
print(x)  # Prints "4"
x *= 2
print(x)  # Prints "8"
y = 2.5
print(type(y)) # Prints "<class 'float'>"
print(y, y + 1, y * 2, y ** 2) # Prints "2.5 3.5 5.0 6.25"
```

근데 주의할 점은 Python은 ```x++```나 ```x--```같은 연산자가 없다.

**Booleans** : Python도 다른 언어들처럼 Boolean을 사용하는데 ```&&```나, ```||```같은 연산자보다, 영어 단어를 쓴다.

```python
t = True
f = False
print(type(t)) # Prints "<class 'bool'>"
print(t and f) # Logical AND; prints "False"
print(t or f)  # Logical OR; prints "True"
print(not t)   # Logical NOT; prints "False"
print(t != f)  # Logical XOR; prints "True"
```

**Strings** : 개인적으로 파이썬이 제공하는 가장 강력한 기능 중 하나라고 생각한다.

```python
hello = 'hello'    # String literals can use single quotes
world = "world"    # or double quotes; it does not matter.
print(hello)       # Prints "hello"
print(len(hello))  # String length; prints "5"
hw = hello + ' ' + world  # String concatenation
print(hw)  # prints "hello world"
hw12 = '%s %s %d' % (hello, world, 12)  # sprintf style string formatting
print(hw12)  # prints "hello world 12"
```

String은 좋은 메소드들을 많이 제공한다.

```python
s = "hello"
print(s.capitalize())  # Capitalize a string; prints "Hello"
print(s.upper())       # Convert a string to uppercase; prints "HELLO"
print(s.rjust(7))      # Right-justify a string, padding with spaces; prints "  hello"
print(s.center(7))     # Center a string, padding with spaces; prints " hello "
print(s.replace('l', '(ell)'))  # Replace all instances of one substring with another;
                                # prints "he(ell)(ell)o"
print('  world '.strip())  # Strip leading and trailing whitespace; prints "world"
```

### Containers

**List**

Array라 생각하세요.

```python
xs = [3, 1, 2]    # Create a list
print(xs, xs[2])  # Prints "[3, 1, 2] 2"
print(xs[-1])     # Negative indices count from the end of the list; prints "2"
xs[2] = 'foo'     # Lists can contain elements of different types
print(xs)         # Prints "[3, 1, 'foo']"
xs.append('bar')  # Add a new element to the end of the list
print(xs)         # Prints "[3, 1, 'foo', 'bar']"
x = xs.pop()      # Remove and return the last element of the list
print(x, xs)      # Prints "bar [3, 1, 'foo']"
```

이런 건 Slicing, Loops, List Comprehensions 등 좋은 기능을 많이 제공한다.

**Dictionaries**

dictionary는 key value 쌍을 가지는 자료형이다. 자바스크립트의 오브젝트와 비슷하다.

```python
d = {'cat': 'cute', 'dog': 'furry'}  # Create a new dictionary with some data
print(d['cat'])       # Get an entry from a dictionary; prints "cute"
print('cat' in d)     # Check if a dictionary has a given key; prints "True"
d['fish'] = 'wet'     # Set an entry in a dictionary
print(d['fish'])      # Prints "wet"
# print(d['monkey'])  # KeyError: 'monkey' not a key of d
print(d.get('monkey', 'N/A'))  # Get an element with a default; prints "N/A"
print(d.get('fish', 'N/A'))    # Get an element with a default; prints "wet"
del d['fish']         # Remove an element from a dictionary
print(d.get('fish', 'N/A')) # "fish" is no longer a key; prints "N/A"
```

**Sets**

Unordered Collection이다. 자바의 Set과 똑같은 거 같다.

```python
animals = {'cat', 'dog'}
print('cat' in animals)   # Check if an element is in a set; prints "True"
print('fish' in animals)  # prints "False"
animals.add('fish')       # Add an element to a set
print('fish' in animals)  # Prints "True"
print(len(animals))       # Number of elements in a set; prints "3"
animals.add('cat')        # Adding an element that is already in the set does nothing
print(len(animals))       # Prints "3"
animals.remove('cat')     # Remove an element from a set
print(len(animals))       # Prints "2"
```

**Tuples**

ordered list이다. 여기 밑에 있는 거 말고 여러가지 좀 찾다보면 의외로 상당히 유용한 자료형이다.

```python
d = {(x, x + 1): x for x in range(10)}  # Create a dictionary with tuple keys
t = (5, 6)        # Create a tuple
print(type(t))    # Prints "<class 'tuple'>"
print(d[t])       # Prints "5"
print(d[(1, 2)])  # Prints "1"
```

### Functions

```def``` 키워드를 사용한다.

```python
def sign(x):
    if x > 0:
        return 'positive'
    elif x < 0:
        return 'negative'
    else:
        return 'zero'

for x in [-1, 0, 1]:
    print(sign(x))
# Prints "negative", "zero", "positive"
```

이렇게 optional keyword argument도 사용할 수 있다.

```python
def hello(name, loud=False):
    if loud:
        print('HELLO, %s!' % name.upper())
    else:
        print('Hello, %s' % name)

hello('Bob') # Prints "Hello, Bob"
hello('Fred', loud=True)  # Prints "HELLO, FRED!"
```


### Classes

그냥 타 언어들의 클래스와 비슷하다.

```python
class Greeter(object):

    # Constructor
    def __init__(self, name):
        self.name = name  # Create an instance variable

    # Instance method
    def greet(self, loud=False):
        if loud:
            print('HELLO, %s!' % self.name.upper())
        else:
            print('Hello, %s' % self.name)

g = Greeter('Fred')  # Construct an instance of the Greeter class
g.greet()            # Call an instance method; prints "Hello, Fred"
g.greet(loud=True)   # Call an instance method; prints "HELLO, FRED!"
```


## Numpy

Numpy는 Python으로 과학적인 계산을 하는데 필요한 중요한 라이브러리 중 하나이다. MATLAB에 익숙하다면 이걸 보는 것보다 [이거 (Numpy for Matlab Users)](http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users) 보는게 좋다고 하네요.

### Arrays

numpy에서 제공하는 array는 모두 같은 타입이여야 하고 0 이상의 수로만 인덱스 접근이 가능하다 하네요.

```python
import numpy as np

a = np.array([1, 2, 3])   # Create a rank 1 array
print(type(a))            # Prints "<class 'numpy.ndarray'>"
print(a.shape)            # Prints "(3,)"
print(a[0], a[1], a[2])   # Prints "1 2 3"
a[0] = 5                  # Change an element of the array
print(a)                  # Prints "[5, 2, 3]"

b = np.array([[1,2,3],[4,5,6]])    # Create a rank 2 array
print(b.shape)                     # Prints "(2, 3)"
print(b[0, 0], b[0, 1], b[1, 0])   # Prints "1 2 4"
```
그리고 배열을 만들기 위한 함수들도 여럿 지원을 하네요.

```python
import numpy as np

a = np.zeros((2,2))   # Create an array of all zeros
print(a)              # Prints "[[ 0.  0.]
                      #          [ 0.  0.]]"

b = np.ones((1,2))    # Create an array of all ones
print(b)              # Prints "[[ 1.  1.]]"

c = np.full((2,2), 7)  # Create a constant array
print(c)               # Prints "[[ 7.  7.]
                       #          [ 7.  7.]]"

d = np.eye(2)         # Create a 2x2 identity matrix
print(d)              # Prints "[[ 1.  0.]
                      #          [ 0.  1.]]"

e = np.random.random((2,2))  # Create an array filled with random values
print(e)                     # Might print "[[ 0.91940167  0.08143941]
                             #               [ 0.68744134  0.87236687]]"
```

Array Indexing에서 신기한 트릭?이 많네요

```python
import numpy as np

# Create the following rank 2 array with shape (3, 4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])

# Two ways of accessing the data in the middle row of the array.
# Mixing integer indexing with slices yields an array of lower rank,
# while using only slices yields an array of the same rank as the
# original array:
row_r1 = a[1, :]    # Rank 1 view of the second row of a
row_r2 = a[1:2, :]  # Rank 2 view of the second row of a
print(row_r1, row_r1.shape)  # Prints "[5 6 7 8] (4,)"
print(row_r2, row_r2.shape)  # Prints "[[5 6 7 8]] (1, 4)"

# We can make the same distinction when accessing columns of an array:
col_r1 = a[:, 1]
col_r2 = a[:, 1:2]
print(col_r1, col_r1.shape)  # Prints "[ 2  6 10] (3,)"
print(col_r2, col_r2.shape)  # Prints "[[ 2]
                             #          [ 6]
                             #          [10]] (3, 1)"
```

```python
import numpy as np

a = np.array([[1,2], [3, 4], [5, 6]])

# An example of integer array indexing.
# The returned array will have shape (3,) and
print(a[[0, 1, 2], [0, 1, 0]])  # Prints "[1 4 5]"

# The above example of integer array indexing is equivalent to this:
print(np.array([a[0, 0], a[1, 1], a[2, 0]]))  # Prints "[1 4 5]"

# When using integer array indexing, you can reuse the same
# element from the source array:
print(a[[0, 0], [1, 1]])  # Prints "[2 2]"

# Equivalent to the previous integer array indexing example
print(np.array([a[0, 1], a[0, 1]]))  # Prints "[2 2]"
```

이거 말고도 Boolean Array Indexing이라던가 뭐 여러가지 있는데, 그 기능은 제가 많이 쓰지 않을 것 같은 기능이라 적진 않았습니다.

그리고 Numpy에 Datatype들이 있는데, 그거에 관해선 다음 코드 보시면 이해하실거라 믿어요.

```python
import numpy as np

x = np.array([1, 2])   # Let numpy choose the datatype
print(x.dtype)         # Prints "int64"

x = np.array([1.0, 2.0])   # Let numpy choose the datatype
print(x.dtype)             # Prints "float64"

x = np.array([1, 2], dtype=np.int64)   # Force a particular datatype
print(x.dtype)                         # Prints "int64"
```

그 밑에도 Broadcasting 같은 여러가지 기능이 많은데, 별로 흥미롭진 않아서 적진 않았습니다.

## Scipy

Numpy가 고성능의 다차원 배열을 제공한다면, Scipy는 이거 위에다가 더 여러가지 좋은 기능들을 많이 제공한다네요.

[공식 Documentation](https://docs.scipy.org/doc/scipy/reference/index.html) 보는 게 가장 좋겠지만, 몇가지 부분을 주목해서 작성했다고 합니다.

### Image Operation

이미지 잘 이용하는 함수를 Scipy가 제공하는데, 예를 들어 디스크에서 읽어서 numpy 배열로 넣거나, numpy 배열에서 이미지로 저장하거나, resize하거나 등등을 제공한다.

밑에는 그 예제

```python
from scipy.misc import imread, imsave, imresize

# Read an JPEG image into a numpy array
img = imread('assets/cat.jpg')
print(img.dtype, img.shape)  # Prints "uint8 (400, 248, 3)"

# We can tint the image by scaling each of the color channels
# by a different scalar constant. The image has shape (400, 248, 3);
# we multiply it by the array [1, 0.95, 0.9] of shape (3,);
# numpy broadcasting means that this leaves the red channel unchanged,
# and multiplies the green and blue channels by 0.95 and 0.9
# respectively.
img_tinted = img * [1, 0.95, 0.9]

# Resize the tinted image to be 300 by 300 pixels.
img_tinted = imresize(img_tinted, (300, 300))

# Write the tinted image back to disk
imsave('assets/cat_tinted.jpg', img_tinted)
```

![고양이]({{ site.url }}/images/cs231n/python-numpy-tutorial.png)

뭐 위의 사진처럼 결과가 나온다고 한다.

## Matplotlib

plotting하는 라이브러리라고 하네요. plotting이라는 말의 뜻을 정확히 모르겠지만, "눈에 보이도록 그래프를 그려준다"정도로 보면 될 것 같아요.

```python
import numpy as np
import matplotlib.pyplot as plt

# Compute the x and y coordinates for points on a sine curve
x = np.arange(0, 3 * np.pi, 0.1)
y = np.sin(x)

# Plot the points using matplotlib
plt.plot(x, y)
plt.show()  # You must call plt.show() to make graphics appear.
```

![그래프]({{ site.url }}/images/cs231n/python-numpy-tutorial-2.png)

위의 예제는 sin 그래프네요.

축에 레이블 추가하는거나, 제목 추가하는거나, legend 추가하는거나 여러가지 많이 할 수 있다고 합니다.

그리고 subplot이라 해서 같은 figure안에 여러가지 그래프를 그릴 수 있고요.

이미지도 보여줄 수 있다고 합니다.

![고양이 그래프]({{ site.url }}/images/cs231n/python-numpy-tutorial-3.png)
