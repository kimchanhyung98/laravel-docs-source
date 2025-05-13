#!/usr/bin/env python3
"""
라라벨 문서 번역 자동화 스크립트

이 스크립트는 라라벨 원본 문서를 클론하여 현재 프로젝트에 복사하고,
변경된 마크다운 파일을 자동으로 번역하는 기능을 수행합니다.
"""
import os
import shutil

from dotenv import load_dotenv

from utils import get_git_changes, translate_file, add_files_to_git
from utils.docs import clone_laravel_docs, update_branch_docs


def main():
    """메인 함수: 라라벨 문서 업데이트 및 번역 수행"""
    # 환경 변수 로드
    load_dotenv()

    # 기본 설정
    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]
    excluded_files = ["license.md", "readme.md"]

    print("\n[1] 라라벨 원본 문서 복사")
    if not clone_laravel_docs(temp_dir, original_repo):
        print("git clone 오류")
        return

    print("\n[2] 각 브랜치별 문서 처리")
    for branch in branches:
        update_branch_docs(branch, temp_dir, excluded_files)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print("임시 디렉토리 삭제")

    print("\n[3] 변경된 파일 번역")
    processed_files = set()
    changed_files = get_git_changes()

    if not changed_files:
        print("변경된 문서가 없음")
    else:
        for file_path in changed_files:
            path_parts = file_path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'origin':
                branch = path_parts[0]
                filename = path_parts[2]

                # 이미 처리한 파일인지 확인
                file_key = f"{branch}/{filename}"
                if file_key in processed_files:
                    continue

                processed_files.add(file_key)

                # 번역 제외 파일 확인
                if filename.lower() in excluded_files:
                    print(f"예외 파일: {file_key}")
                    continue

                # 번역
                translate_file(
                    os.path.join(os.getcwd(), branch, 'origin', filename),
                    os.path.join(os.getcwd(), branch, 'ko', filename)
                )

    add_files_to_git()
    print("\n갱신 완료")


if __name__ == "__main__":
    main()
