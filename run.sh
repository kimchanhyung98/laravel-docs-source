#!/bin/bash

IMAGE_NAME="laravel-docs"
API_KEY_NAME="OPENAI_API_KEY"

TRIMMED_API_KEY_VALUE=$(grep "^${API_KEY_NAME}=" ".env" 2>/dev/null | head -n 1 | sed -n "s/^${API_KEY_NAME}=//p" | xargs)

if [ -z "$TRIMMED_API_KEY_VALUE" ]; then
    echo ".env 파일에 ${API_KEY_NAME}가 유효하지 않습니다."
    exit 1
fi

if ! { docker build -t "$IMAGE_NAME" . && docker run --rm "$IMAGE_NAME"; }; then
    echo "Docker 작업 중 오류가 발생했습니다."
    exit 1
fi
