import os
import time

import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from utils.common import retry, timeout
from utils.filtering import filter_markdown
from utils.token_counter import get_token_count


def get_translation_client():
    """번역에 사용할 AI 클라이언트를 가져옴

    Returns:
        tuple: (client, model) - AI 클라이언트와 모델명

    Raises:
        ValueError: 필요한 환경변수가 설정되지 않은 경우
    """
    provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
    model = os.environ.get("TRANSLATION_MODEL", "gpt-4.1")

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 미설정")

        openai.api_key = api_key
        client = openai.OpenAI()
        return client, model

    elif provider == "azure":
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-05-01-preview")

        if not api_key or not endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY 또는 AZURE_OPENAI_ENDPOINT 미설정")

        client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        return client, model

    else:
        raise ValueError(f"미지원 번역 제공자: {provider}")


def translate_text_with_openai(text_to_translate, system_prompt):
    """AI API를 사용하여 텍스트를 번역

    Args:
        text_to_translate: 번역할 텍스트
        system_prompt: 시스템 프롬프트

    Returns:
        str: 번역된 텍스트

    Raises:
        Exception: API 호출 중 오류 발생 시
    """
    client, model = get_translation_client()
    system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
    user_message = ChatCompletionUserMessageParam(role="user", content=text_to_translate)

    # 번역 요청
    response = client.chat.completions.create(
        model=model,
        messages=[system_message, user_message]
    )
    return response.choices[0].message.content


@retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,))
@timeout(seconds=1000)
def translate_file(source_file, target_file, source_lang="en", target_lang="ko"):
    """OpenAI API를 사용하여, 마크다운 파일을 번역하고 저장

    Args:
        source_file: 원본 파일 경로
        target_file: 번역된 파일을 저장할 경로
        source_lang: 원본 언어 코드 (기본값: "en")
        target_lang: 대상 언어 코드 (기본값: "ko")

    Returns:
        bool: 번역 성공 여부
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"빈 파일: {source_file}")
            return False

        print(f"번역 시작: {source_file}")

        # 버전 정보 추출
        version = None
        abs_target_path = os.path.abspath(target_file).replace("\\", "/")
        if '/9.x/' in abs_target_path:
            version = '9.x'
        elif '/10.x/' in abs_target_path:
            version = '10.x'
        elif '/11.x/' in abs_target_path:
            version = '11.x'
        elif '/12.x/' in abs_target_path:
            version = '12.x'
        elif '/master/' in abs_target_path:
            version = 'master'

        content = filter_markdown(content, version)

        # 시스템 프롬프트 설정
        with open("translation_prompt.txt", 'r', encoding='utf-8') as f:
            system_prompt_template = f.read()
        system_prompt = system_prompt_template.format(source_lang=source_lang, target_lang=target_lang)

        content_tokens = get_token_count(content)
        print(f"{source_file}: {content_tokens:,} 토큰")

        translated_content = translate_text_with_openai(content, system_prompt)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"번역 완료: {source_file} -> {target_file}")
        return True

    except openai.RateLimitError as e:
        print(f"RateLimitError: {e}")
        time.sleep(30)
        raise
    except Exception as e:
        print(f"번역 오류: {type(e).__name__}")
        raise
