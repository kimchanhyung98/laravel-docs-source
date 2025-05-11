#!/usr/bin/env python3
"""
Laravel 문서 관련 유틸리티 함수 모듈
"""
import os
import shutil

from utils.common import run_command


def clone_laravel_docs(temp_dir, original_repo):
    """Laravel 원본 문서를 임시 디렉토리에 클론

    Args:
        temp_dir: 임시 디렉토리 경로
        original_repo: Laravel 원본 문서 저장소 URL

    Returns:
        bool: 성공 여부
    """
    try:
        # 임시 디렉토리가 있으면 삭제
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        # 원본 저장소 클론
        run_command(f"git clone {original_repo} {temp_dir}")
        return True
    except Exception as e:
        print(f"Laravel 문서 클론 중 오류 발생: {e}")
        return False


def update_branch_docs(branch, temp_dir, excluded_files):
    """특정 브랜치의 문서를 업데이트

    Args:
        branch: 브랜치 이름
        temp_dir: 임시 디렉토리 경로
        excluded_files: 번역에서 제외할 파일 목록

    Returns:
        bool: 성공 여부
    """
    try:
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

        print(f"{branch} 브랜치 문서 업데이트 완료")
        return True
    except Exception as e:
        print(f"{branch} 브랜치 문서 업데이트 중 오류 발생: {e}")
        return False
