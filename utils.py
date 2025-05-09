#!/usr/bin/env python3
import os
import subprocess
import time
from functools import wraps

import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam


def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """예외 발생 시 함수를 재시도하는 데코레이터

    Args:
        max_attempts: 최대 시도 횟수
        delay: 초기 대기 시간(초)
        backoff: 대기 시간 증가 요소(다음 시도에서는 delay * backoff)
        exceptions: 재시도할 예외 클래스 튜플
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        print(f"최대 시도 횟수({max_attempts})를 초과했습니다. 마지막 오류: {e}")
                        raise

                    print(f"오류 발생: {e}. {current_delay}초 후 재시도 ({attempt}/{max_attempts})...")
                    time.sleep(current_delay)
                    current_delay *= backoff  # 대기 시간 증가

            return None  # 이 코드는 실행되지 않지만 형식적으로 필요

        return wrapper

    return decorator


def timeout(seconds=420):
    """함수 실행 시 타임아웃을 적용하는 데코레이터

    Args:
        seconds: 타임아웃 시간(초)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal

            def handler(signum, frame):
                raise TimeoutError(f"함수 실행이 {seconds}초를 초과했습니다.")

            # 타임아웃 설정
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # 타이머 재설정
                return result
            except TimeoutError as e:
                print(f"타임아웃: {e}")
                raise
            finally:
                signal.alarm(0)  # 타이머 재설정

        return wrapper

    return decorator


def run_command(command, cwd=None):
    """명령어를 실행하고 결과를 반환

    Args:
        command: 실행할 명령어
        cwd: 명령어를 실행할 디렉토리 (기본값: None)

    Returns:
        str: 명령어 실행 결과
    """
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()


@retry(max_attempts=3, delay=5, backoff=2, exceptions=(Exception,))
@timeout(seconds=300)
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
        # 파일 읽기
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 파일이 비어있는지 확인
        if not content.strip():
            print(f"빈 파일이 발견되었습니다: {source_file}")
            # 빈 파일을 그대로 복사
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        # OpenAI API 키 가져오기
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY가 설정되지 않았습니다.")
            return False

        # OpenAI 클라이언트 설정
        openai.api_key = api_key
        client = openai.OpenAI()

        # 시스템 프롬프트 설정
        prompt_file = os.environ.get("TRANSLATION_PROMPT_FILE", "translation_prompt.txt")
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                system_prompt_template = f.read()
        except Exception as e:
            print(f"프롬프트 파일 읽기 오류: {e}")
            system_prompt_template = "{source_lang}에서 {target_lang}로 번역해주세요."

        system_prompt = system_prompt_template.format(source_lang=source_lang, target_lang=target_lang)
        system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
        user_message = ChatCompletionUserMessageParam(role="user", content=content)

        # 번역 요청
        print(f"번역 시작: {source_file} -> {target_file}")
        response = client.chat.completions.create(
            model=os.environ.get("TRANSLATION_MODEL", "gpt-4.1"),
            messages=[system_message, user_message]
        )
        translated_content = response.choices[0].message.content
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"번역 완료: {source_file} -> {target_file}")
        return True

    except Exception as e:
        print(f"번역 오류: {str(e)}")
        return False
