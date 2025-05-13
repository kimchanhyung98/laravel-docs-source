#!/usr/bin/env python3
"""
번역 관련 유틸리티 함수 모듈
"""
import os
import time

import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from utils.chunk import orchestrate_chunk_translation
from utils.common import retry, timeout
from utils.filtering import filter_markdown


def get_translation_client():
    """번역에 사용할 AI 클라이언트를 가져옴

    TRANSLATION_PROVIDER 환경변수에 따라 OpenAI 또는 Azure OpenAI 클라이언트를 반환

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
        raise ValueError(f"지원하지 않는 번역 제공자: {provider}. 'openai' 또는 'azure'를 사용하세요.")


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
    # 클라이언트와 모델 가져오기
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
@timeout(seconds=300)
def translate_file(source_file, target_file, source_lang="en", target_lang="ko"):
    """OpenAI API를 사용하여, 마크다운 파일을 번역하고 저장
    대용량 파일은 청크로 분할하여 번역

    Args:
        source_file: 원본 파일 경로
        target_file: 번역된 파일을 저장할 경로
        source_lang: 원본 언어 코드 (기본값: "en")
        target_lang: 대상 언어 코드 (기본값: "ko")

    Returns:
        bool: 번역 성공 여부
    """
    try:
        # 파일 읽기
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"빈 파일: {source_file}")
            return False

        # 파일 경로에서 버전 정보 추출
        version = None
        # 전체 경로를 문자열로 처리하여 버전 추출
        source_path_str = str(source_file)
        if "master" in source_path_str:
            version = "master"
        elif "12.x" in source_path_str:
            version = "12.x"
        elif "11.x" in source_path_str:
            version = "11.x"
        elif "10.x" in source_path_str:
            version = "10.x"
        elif "9.x" in source_path_str:
            version = "9.x"
        elif "8.x" in source_path_str:
            version = "8.x"

        # 마크다운 필터링 적용 (버전 정보 포함)
        content = filter_markdown(content, version)

        # 시스템 프롬프트 설정
        try:
            with open("translation_prompt.txt", 'r', encoding='utf-8') as f:
                system_prompt_template = f.read()
        except Exception as e:
            print(f"프롬프트 파일 오류: {e}")
            return False

        # 파일 크기 확인 (줄 수 기준)
        line_count = len(content.splitlines())
        file_name = os.path.basename(source_file)

        print(f"번역 시작: {source_file} -> {target_file} ({line_count}줄)")

        # 대용량 파일 기준 (1000줄 이상)
        if line_count > 1000:
            print(f"대용량 파일 감지: {file_name} - 청크 분할 번역 시작")
            translated_content = orchestrate_chunk_translation(
                content=content,
                source_lang=source_lang,
                target_lang=target_lang,
                original_filename_for_logging=file_name,
                translate_api_call_func=translate_text_with_openai
            )
        else:

            system_prompt = system_prompt_template.format(source_lang=source_lang, target_lang=target_lang)
            translated_content = translate_text_with_openai(content, system_prompt)

        # 번역 결과 저장
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"번역 완료: {source_file} -> {target_file}")
        return True

    except openai.APITimeoutError as e:
        print(f"APITimeoutError - {str(e)}")
        raise
    except openai.APIConnectionError as e:
        print(f"APIConnectionError - {str(e)}")
        raise
    except openai.RateLimitError as e:
        print(f"RateLimitError - {str(e)}")
        time.sleep(30)
        raise
    except Exception as e:
        print(f"Exception - {type(e).__name__} - {str(e)}")
        raise
