#!/bin/bash

docker build -f .devcontainer/Dockerfile -t jekyll .
docker run --rm -it -p 4000:4000 -v $(pwd):/src -w /src jekyll jekyll serve --incremental --host 0.0.0.0
