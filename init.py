#!/usr/bin/env python3
import os
import shutil
import subprocess

import dotenv
import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam


def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()


def translate_with_openai(content):
    """OpenAI API를 사용하여 마크다운 콘텐츠를 영어에서 한국어로 번역합니다."""
    # OpenAI API 키 가져오기
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY가 설정되지 않았습니다.")
        return content

    # OpenAI 클라이언트 설정
    openai.api_key = api_key
    client = openai.OpenAI()

    # 시스템 프롬프트 설정
    system_prompt = """당신은 전문 번역가입니다. EN에서 ko로 마크다운 문서를 번역해주세요.
중요한 지침:
1. 코드 블록, HTML 태그, 링크 URL은 번역하지 마세요.
2. 마크다운 형식을 유지하세요.
3. 전문 용어는 적절하게 번역하세요.
"""

    try:
        # 올바른 타입의 메시지 생성
        system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
        user_message = ChatCompletionUserMessageParam(role="user", content=f"다음 마크다운 문서를 번역해주세요:\n\n{content}")

        response = client.chat.completions.create(
            model=os.environ.get("TRANSLATION_MODEL", "gpt-4.1"),
            messages=[system_message, user_message]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"번역 중 오류 발생: {e}")
        return content


def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    repo_url = "https://github.com/laravel/docs.git"
    branches = ["master"]
    # branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]

    # 작업 디렉토리 설정
    work_dir = os.path.join(os.getcwd(), "laravel-docs-temp")
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    run_command(f"git clone {repo_url} {work_dir}")
    for branch in branches:
        print(f"\n브랜치 : {branch}")
        run_command(f"git checkout {branch}", cwd=work_dir)

        # en 디렉토리 설정 및 생성
        en_target_dir = os.path.join(os.getcwd(), f"{branch}/en")
        os.makedirs(en_target_dir, exist_ok=True)

        # ko 디렉토리 설정 및 생성
        ko_target_dir = os.path.join(os.getcwd(), f"{branch}/ko")
        os.makedirs(ko_target_dir, exist_ok=True)

        # 최상위 디렉토리의 마크다운 파일만 가져오기
        for file in os.listdir(work_dir):
            if file.endswith(".md"):
                source_path = os.path.join(work_dir, file)

                # en 디렉토리에 파일 복사
                en_target_path = os.path.join(en_target_dir, file)
                shutil.copy2(source_path, en_target_path)
                print(f"파일 복사: {file} -> {en_target_dir}")

                # 파일 내용 읽기
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # OpenAI로 번역
                print(f"번역 중: {file}")
                translated_content = translate_with_openai(content)

                # ko 디렉토리에 번역된 파일 저장
                ko_target_path = os.path.join(ko_target_dir, file)
                with open(ko_target_path, 'w', encoding='utf-8') as f:
                    f.write(translated_content)
                print(f"번역 완료: {file} -> {ko_target_dir}")

        print(f"{branch} 처리 완료")

    print("\n작업 디렉토리 정리")
    shutil.rmtree(work_dir)


if __name__ == "__main__":
    main()
