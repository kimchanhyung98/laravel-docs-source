#!/usr/bin/env python3
"""
Git 관련 유틸리티 함수 모듈
"""
import os
import subprocess

from utils.common import run_command


def get_git_changes():
    """git을 사용하여 현재 프로젝트의 변경된 마크다운 파일 목록을 가져옴

    Returns:
        list: 변경된 마크다운 파일 경로 목록 (branch/origin/filename.md 형식)
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
                if len(path_parts) >= 3 and path_parts[1] == 'origin':
                    changed_files.add(file_path)

        return sorted(list(changed_files))
    except subprocess.CalledProcessError:
        # git 명령어 실패 시 빈 목록 반환
        print("Git 명령어 실행 중 오류 발생")
        return []


def add_files_to_git():
    """변경된 마크다운 파일을 git에 추가

    Returns:
        bool: 성공 여부
    """
    try:
        run_command("git add *.md */*.md */*/*.md", cwd=os.getcwd())
        print("Git 파일 추가 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 파일 추가 중 오류 발생: {e}")
        return False
