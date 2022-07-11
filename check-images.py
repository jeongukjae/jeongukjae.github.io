import os
import re

images = []
for dirpath, dirnames, filenames in os.walk("images"):
    images.extend(["/" + os.path.join(dirpath, f) for f in filenames])

founds = []
for dirpath, dirnames, filenames in os.walk("_posts"):
    for filename in filenames:
        with open(os.path.join(dirpath, filename)) as f:
            content = f.read()
            founds.extend([
                m[0]
                for m in
                re.findall(r"(/images.+(png|gif|jpeg|jpg))", content, re.IGNORECASE)
            ])

print(f"missing: {set(founds) - set(images)}")
print(f"unnecessary: {set(images) - set(founds)}")
