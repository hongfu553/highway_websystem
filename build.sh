#!/bin/bash

# 构建 Docker 镜像
docker build -t highway .

# 运行 Docker 容器
docker run -p 5000:5000 highway
