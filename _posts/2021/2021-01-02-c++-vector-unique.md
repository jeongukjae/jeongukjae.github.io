---
layout: post
title: C++ std::unique 동작
tags:
  - c++
---

leetcode를 풀다가 중복제거에 사용할 수 있는 STL 함수가 없을까 찾아보았는데, [`std::unique`](https://en.cppreference.com/w/cpp/algorithm/unique)가 있었다. 근데 동작이 잘 이해가 안가서 찾아보았다.

```c++
vector<int> nums{1, 1, 2, 2, 3, 3, 3, 3, 7, 7, 8, 10};
auto iterator = unique(nums.begin(), nums.end());
for (int i = 0;i < nums.size();i++)
    cout << nums.data() + i << "(" << nums[i] << ") ";
cout << endl;

for (int i = 0;i < nums.size() - std::distance(nums.begin(), iterator);i++)
    cout << iterator.base() + i << "(" << *(iterator + i) << ") ";
cout << endl;
```

출력 결과는 아래와 같은데, `iterator` 뒷부분이 원래 벡터와 똑같다. `unique`로 넘겨준 `iterator`의 데이터 자체를 변화시키는 듯.

```text
0x7fe856c05b10(1) 0x7fe856c05b14(2) 0x7fe856c05b18(3) 0x7fe856c05b1c(7) 0x7fe856c05b20(8) 0x7fe856c05b24(10) 0x7fe856c05b28(3) 0x7fe856c05b2c(3) 0x7fe856c05b30(7) 0x7fe856c05b34(7) 0x7fe856c05b38(8) 0x7fe856c05b3c(10)
0x7fe856c05b28(3) 0x7fe856c05b2c(3) 0x7fe856c05b30(7) 0x7fe856c05b34(7) 0x7fe856c05b38(8) 0x7fe856c05b3c(10)
```

그래서 cppreference.com을 찾아보니 내부 구현을 아래처럼 생각하라고 한다.

```c++
template<class ForwardIt>
ForwardIt unique(ForwardIt first, ForwardIt last)
{
    if (first == last)
        return last;

    ForwardIt result = first;
    while (++first != last) {
        if (!(*result == *first) && ++result != first) {
            *result = std::move(*first);
        }
    }
    return ++result;
}
```

연속되는 같은 값인 경우 계속 옮기다가 다른 값이 나오면 `*result = std::move(*first);` 이렇게 값 자체를 바꾸어서 unique인 iterator 다음 주소값을 반환하는 듯하다.
