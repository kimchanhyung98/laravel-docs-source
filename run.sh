#!/bin/bash

# 환경 변수 확인
if [ ! -f ".env" ]; then
    echo ".env 파일이 없습니다."
    exit 1
fi

# Docker 이미지 빌드 및 실행
docker build -t laravel-docs . && \
docker run --rm -v "$(pwd):/app" laravel-docs
