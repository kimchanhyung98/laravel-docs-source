#!/usr/bin/env python3
import os
import shutil
import subprocess
import time
from functools import wraps

import dotenv
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
    """명령어를 실행하고 결과를 반환하는 함수"""
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
def translate_with_openai(content):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return content

    openai.api_key = api_key
    client = openai.OpenAI()

    system_prompt = """당신은 전문 번역가입니다. EN에서 ko로 마크다운 문서를 번역해주세요.
중요한 지침:
1. 코드 블록, HTML 태그, 링크 URL은 번역하지 마세요.
2. 마크다운 형식을 유지하세요.
3. 전문 용어는 적절하게 번역하세요."""

    try:
        system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
        user_message = ChatCompletionUserMessageParam(role="user", content=f"다음 마크다운 문서를 번역해주세요:\n\n{content}")

        response = client.chat.completions.create(
            model=os.environ.get("TRANSLATION_MODEL", "gpt-4.1"),
            messages=[system_message, user_message]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"번역 오류: {e}")
        return content


def translate_markdown_file(source_file, target_file):
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        translated_content = translate_with_openai(content)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        return True

    except Exception as e:
        print(f"번역 오류: {str(e)}")
        return False


def get_git_changes():
    """
    git을 사용하여 현재 프로젝트의 변경사항을 확인하는 함수
    """
    try:
        # git status 명령어 실행
        status_output = run_command("git status --porcelain", cwd=os.getcwd())

        # 변경된 파일만 필터링
        changed_files = []

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            file_path = line[3:].strip()

            # 마크다운 파일만 처리
            if file_path.endswith('.md'):
                # 파일 경로에서 브랜치 정보 추출
                path_parts = file_path.split('/')
                if len(path_parts) >= 3 and path_parts[1] == 'en':
                    changed_files.append(file_path)

        return sorted(changed_files)
    except subprocess.CalledProcessError:
        # git 명령어 실패 시 빈 목록 반환
        return []


def main():
    """Laravel 원본 문서를 현재 프로젝트에 덮어쓰고, 변경사항을 번역 및 동기화하는 함수
    
    주요 기능:
        1. Laravel 원본 문서를 클론하여 현재 프로젝트에 덮어씀.
        2. 변경된 마크다운 파일을 자동으로 번역.
        3. Git을 사용하여 변경사항을 동기화.
    """
    # 원본 저장소 URL 및 작업 디렉토리 설정
    dotenv.load_dotenv()

    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "laravel-docs-temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]

    # 임시 디렉토리 삭제 후 새로 클론
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    run_command(f"git clone {original_repo} {temp_dir}")

    # 각 브랜치별 문서 업데이트
    for branch in branches:
        # 브랜치 체크아웃
        run_command(f"git checkout {branch}", cwd=temp_dir)

        # 현재 프로젝트의 해당 브랜치 디렉토리 확인
        branch_dir = os.path.join(os.getcwd(), branch)
        en_dir = os.path.join(branch_dir, "en")
        ko_dir = os.path.join(branch_dir, "ko")

        # 디렉토리가 없으면 생성
        os.makedirs(en_dir, exist_ok=True)
        os.makedirs(ko_dir, exist_ok=True)

        # 원본 저장소의 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]

        # 각 마크다운 파일 복사
        for file in md_files:
            source_path = os.path.join(temp_dir, file)
            en_target_path = os.path.join(en_dir, file)
            ko_target_path = os.path.join(ko_dir, file)

            # en 디렉토리에 파일 복사
            shutil.copy2(source_path, en_target_path)

            # ko 디렉토리에 파일 복사 (없을 경우에만)
            if not os.path.exists(ko_target_path):
                shutil.copy2(source_path, ko_target_path)

        # 변경사항을 git에 추가
        run_command(f"git add {branch}/en/*.md", cwd=os.getcwd())
        print(f"{branch} 업데이트 완료")

    # 작업 완료 후 임시 디렉토리 삭제
    shutil.rmtree(temp_dir)

    changed_files = get_git_changes()

    for file_path in changed_files:
        path_parts = file_path.split('/')
        if len(path_parts) >= 3 and path_parts[1] == 'en':
            branch = path_parts[0]
            filename = path_parts[2]

            source_file = os.path.join(os.getcwd(), branch, 'en', filename)
            target_file = os.path.join(os.getcwd(), branch, 'ko', filename)

            print(f"번역: {filename}")
            translate_markdown_file(source_file, target_file)
            run_command(f"git add {branch}/ko/{filename}", cwd=os.getcwd())


if __name__ == "__main__":
    main()
