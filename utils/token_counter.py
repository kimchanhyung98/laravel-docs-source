#!/usr/bin/env python3
"""
토큰 계산 관련 유틸리티 함수 모듈
"""
import tiktoken


def get_token_count(text: str, model: str = "gpt-4") -> int:
    """주어진 텍스트의 토큰 수를 계산

    Args:
        text: 토큰 수를 계산할 텍스트
        model: 사용할 모델명 (기본값: "gpt-4")

    Returns:
        int: 계산된 토큰 수
    """
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)
    return len(tokens)



