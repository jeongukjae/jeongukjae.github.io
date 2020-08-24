---
layout: post
title: "Compound File Binary File Format 오버뷰..?"
tags:
  - note
---

사이드 프로젝트로 HWP 파일 포맷 파싱 라이브러리를 짜면 어떨까 싶어서 포맷을 살펴보니, CompoundFileBinary File Format을 따르는 것 같다. 그리고 이를 줄여서 MS에서는 CFB라 부르는 것 같고, 해당 포맷이 [[MS-CFB]](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/53989ce4-7b05-4f8d-829b-d08d6148375b)라는 이름의 문서로 공개되어 있다.

[MS-CFB version v20180912](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/53989ce4-7b05-4f8d-829b-d08d6148375b) 기준.

## Compound File Overview

* A compound file is a structure to store heirarchy of **storage objects** and **stream objects**.
  * A storage object is similar with a file system directory.
  * A stream object is similar with a traditional notion of a file. A stream contains user-defined data.
* The hierarchy of compound file is tree structure.
  * A stream object should be a leaf node.
  * A storage object can contain streams and/or storages.
  * Each object has a name, but root (storage) object has no name because names are used to identify child objects.

### Vendor data

* No vendor-extensible fields.
* Only way to store vendor data is to store user-defined data and struct them using storage objects and stream objects.

---

결국 정리하면, 파일안에 "폴더 - 파일" 구조를 만든 것이고, 폴더에 해당하는 오브젝트가 storage object, 파일에 해당하는 오브젝트가 stream object라고 한다. 이를 트리 형태로 구성하면 CFB. 그리고 vendor specific한 데이터를 넣으려면 storage와 stream만 쓰라는 정도이다. 뒤쪽을 더 읽어보았는데, 실제 구현할 때 중요한 것 같고, [GitHub - microsoft/compoundfilereader](https://github.com/microsoft/compoundfilereader)을 사용할 때는 그닥 중요한 것 같지는 않아서 그만 두었다.

이 정도만 알고, [GitHub - jeongukjae/compoundfilereader](https://github.com/jeongukjae/compoundfilereader)에 포크떠서 사용가능하도록 정리했고, 프로젝트를 그냥 CMake로 변경한 것이다. hwp 파일에 테스트해보니까 적당히 잘 된다.

원래 좀 많이 정리하려고 했는데, 패스..
