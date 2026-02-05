import os
import shutil
import time

from dotenv import load_dotenv

from utils.docs import clone_laravel_docs, update_branch_docs
from utils.git import get_git_changes, add_files_to_git
from utils.translation import translate_file


def main():
    """
    Automates cloning, updating, and translating Laravel documentation across multiple branches.
    
    This function performs the following steps:
    1. Loads environment variables.
    2. Clones the original Laravel documentation repository into a temporary directory.
    3. Updates documentation for each specified branch, excluding certain files.
    4. Removes the temporary directory after processing.
    5. Identifies changed documentation files using Git.
    6. Translates changed files (excluding specified files) from the original to the target language directory.
       Waits between translations (default: 10 seconds, configurable via TRANSLATION_DELAY environment variable).
    7. Stages all changes in Git and prints a completion message.
    """
    load_dotenv()
    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]
    excluded_files = ["license.md", "readme.md"]
    try:
        translation_delay = int(os.environ.get("TRANSLATION_DELAY", "10"))
    except ValueError:
        print("TRANSLATION_DELAY 환경 변수 값이 유효하지 않음. 기본값 10초 사용.")
        translation_delay = 10

    if not clone_laravel_docs(temp_dir, original_repo):
        print("git clone 오류")
        return

    print("\n[1] 브랜치별 문서 처리")
    for branch in branches:
        update_branch_docs(branch, temp_dir, excluded_files)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    print("\n[2] 변경된 파일 번역")
    processed_files = set()
    changed_files = get_git_changes()

    if not changed_files:
        print("변경된 문서가 없음")
    else:
        for file_path in changed_files:
            norm_path = os.path.normpath(file_path)
            path_parts = norm_path.split(os.sep)
            if len(path_parts) >= 3 and path_parts[1] == 'origin':
                branch = path_parts[0]
                filename = path_parts[2]

                # 이미 처리한 파일인지 확인
                file_key = f"{branch}/{filename}"
                # 이미 처리한 파일인지 확인
                if file_key in processed_files:
                    continue

                processed_files.add(file_key)

                # 번역 제외 파일 확인
                if filename.lower() in excluded_files:
                    print(f"예외 파일: {file_key}")
                    continue

                # 경로 생성
                source_path = os.path.join(branch, 'origin', filename)
                target_path = os.path.join(branch, 'ko', filename)

                # 원본 파일 확인
                if not os.path.exists(source_path):
                    continue

                # 번역 실행
                translate_file(source_path, target_path)
                time.sleep(translation_delay)

    add_files_to_git()
    print("\n갱신 완료")


if __name__ == "__main__":
    main()
