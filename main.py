#!/usr/bin/env python3
import os
import shutil
import subprocess

from dotenv import load_dotenv

from utils import run_command, translate_file


def get_git_changes():
    """
    git을 사용하여 현재 프로젝트의 변경사항을 확인하는 함수
    """
    try:
        # git status 명령어 실행
        status_output = run_command("git status --porcelain", cwd=os.getcwd())

        changed_files = set()

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            file_path = line[3:].strip()

            if file_path.endswith('.md'):
                # 파일 경로에서 브랜치 추출
                path_parts = file_path.split('/')
                if len(path_parts) >= 3 and path_parts[1] == 'en':
                    changed_files.add(file_path)

        return sorted(list(changed_files))
    except subprocess.CalledProcessError:
        # git 명령어 실패 시 빈 목록 반환
        return []


def main():
    """Laravel 원본 문서를 현재 프로젝트에 덮어쓰고, 변경사항을 번역 및 동기화하는 함수

    주요 기능:
        1. Laravel 원본 문서를 클론하여 현재 프로젝트에 덮어씀.
        2. 변경된 마크다운 파일을 자동으로 번역. (예외: license.md, readme.md는 번역하지 않음)
        3. Git을 사용하여 변경사항을 동기화.
    """
    # 환경 변수 및 기본 설정
    load_dotenv()

    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]
    excluded_files = ["license.md", "readme.md"]

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

        # 원본 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]

        # 각 마크다운 파일 복사
        for file_name in md_files:
            source_path = os.path.join(temp_dir, file_name)
            shutil.copy2(source_path, os.path.join(en_dir, file_name))
            # 번역 제외 파일은 그대로 복사
            if file_name.lower() in excluded_files:
                shutil.copy2(source_path, os.path.join(ko_dir, file_name))

        print(f"{branch} 업데이트 완료")

    # 임시 디렉토리 삭제
    shutil.rmtree(temp_dir)

    processed_files = set()
    for file_path in get_git_changes():
        path_parts = file_path.split('/')
        if len(path_parts) >= 3 and path_parts[1] == 'en':
            branch = path_parts[0]
            filename = path_parts[2]

            # 이미 처리한 파일인지 확인
            file_key = f"{branch}/{filename}"
            if file_key in processed_files:
                continue

            processed_files.add(file_key)

            if filename.lower() in excluded_files:
                continue

            translate_file(
                os.path.join(os.getcwd(), branch, 'en', filename),
                os.path.join(os.getcwd(), branch, 'ko', filename)
            )

    try:
        run_command("git add *.md */*.md */*/*.md", cwd=os.getcwd())
        print("완료")
    except subprocess.CalledProcessError:
        print("오류")


if __name__ == "__main__":
    main()
