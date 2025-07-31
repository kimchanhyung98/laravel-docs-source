import tiktoken


def get_token_count(text: str) -> int:
    """주어진 텍스트의 토큰 수를 계산

    Args:
        text: 토큰 수를 계산할 텍스트

    Returns:
        int: 계산된 토큰 수
    """
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)

    return len(tokens)
