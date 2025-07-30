import os
import shutil
import time

from dotenv import load_dotenv

from utils.common import run_command
from utils.git import add_files_to_git
from utils.translation import translate_file


def main():
    load_dotenv()
    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]
    excluded_files = ["license.md", "readme.md"]

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    print("\n[1] 문서 복사")
    run_command(f"git clone {original_repo} {temp_dir}")

    print("\n[2] 문서 번역")
    for branch in branches:
        print(f"\n브랜치: {branch}")
        run_command(f"git checkout {branch}", cwd=temp_dir)

        origin_dir = os.path.join(os.getcwd(), branch, "origin")
        ko_dir = os.path.join(os.getcwd(), branch, "ko")
        os.makedirs(origin_dir, exist_ok=True)
        os.makedirs(ko_dir, exist_ok=True)

        # 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]
        md_files.sort()
        print(f"파일 {len(md_files)}개")

        for file_name in md_files:
            source_path = os.path.join(temp_dir, file_name)

            # origin에 복사 후, ko에 번역 파일 생성
            origin_target_path = os.path.join(origin_dir, file_name)
            shutil.copy2(source_path, origin_target_path)
            ko_target_path = os.path.join(ko_dir, file_name)

            # 번역 제외 파일
            if file_name.lower() in excluded_files:
                shutil.copy2(source_path, ko_target_path)
            else:
                print(f"번역 시작: {file_name}")
                translate_file(source_path, ko_target_path)
                time.sleep(10)

        print(f"브랜치: {branch}, 완료")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    add_files_to_git()
    print("\n번역 완료")


if __name__ == "__main__":
    main()
