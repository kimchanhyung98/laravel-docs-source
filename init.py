#!/usr/bin/env python3
"""
라라벨 문서 초기 번역 스크립트

이 스크립트는 라라벨 원본 문서를 클론하여 현재 프로젝트에 복사하고,
모든 마크다운 파일을 전체 번역하는 기능을 수행합니다.
이 스크립트는 프로젝트 초기 설정 또는 전체 문서 재번역이 필요할 때 사용합니다.
"""
import os
import shutil

from dotenv import load_dotenv

from utils.common import run_command
from utils.git import add_files_to_git
from utils.translation import translate_file


def main():
    """메인 함수: 라라벨 문서 전체 번역 수행"""
    # 환경 변수 로드
    load_dotenv()

    # 기본 설정
    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]
    excluded_files = ["license.md", "readme.md"]

    print("\n[1] 작업 디렉토리 준비")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"기존 임시 디렉토리 '{temp_dir}' 삭제 완료")

    print("\n[2] 라라벨 원본 문서 복사")
    run_command(f"git clone {original_repo} {temp_dir}")
    print(f"라라벨 문서 클론 완료: {original_repo}")

    print("\n[3] 각 브랜치별 문서 처리")
    for branch in branches:
        print(f"\n브랜치: {branch}")

        # 브랜치 체크아웃
        run_command(f"git checkout {branch}", cwd=temp_dir)
        print(f"브랜치 체크아웃: {branch}")

        # 디렉토리 설정 및 생성
        origin_dir = os.path.join(os.getcwd(), branch, "origin")
        ko_dir = os.path.join(os.getcwd(), branch, "ko")

        os.makedirs(origin_dir, exist_ok=True)
        os.makedirs(ko_dir, exist_ok=True)
        print(f"디렉토리 생성: {origin_dir}, {ko_dir}")

        # 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]
        md_files.sort()  # 파일 이름을 알파벳 순서로 정렬

        print(f"처리할 파일: {len(md_files)}개")

        # 각 마크다운 파일 처리
        for file_name in md_files:
            source_path = os.path.join(temp_dir, file_name)

            # origin 디렉토리에 파일 복사
            origin_target_path = os.path.join(origin_dir, file_name)
            shutil.copy2(source_path, origin_target_path)
            print(f"파일 복사: {file_name} -> {origin_dir}")

            # ko 디렉토리에 파일 복사 또는 번역
            ko_target_path = os.path.join(ko_dir, file_name)

            # 번역 제외 파일은 그대로 복사
            if file_name.lower() in excluded_files:
                shutil.copy2(source_path, ko_target_path)
                print(f"예외 파일: {file_name} -> {ko_dir}")
            else:
                # 번역 수행
                print(f"번역 시작: {file_name}")
                translate_file(source_path, ko_target_path)
                print(f"번역 완료: {file_name} -> {ko_dir}")

        print(f"브랜치: {branch} 처리 완료")

    print("\n[4] 임시 디렉토리 삭제")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    add_files_to_git()
    print("\n전체 번역 완료")


if __name__ == "__main__":
    main()
