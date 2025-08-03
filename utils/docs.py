import os
import shutil

from utils.common import run_command


def clone_laravel_docs(temp_dir, original_repo):
    """
    Clone the original Laravel documentation repository into a specified temporary directory.
    
    Parameters:
        temp_dir (str): Path to the temporary directory where the repository will be cloned.
        original_repo (str): URL of the original Laravel documentation repository.
    
    Returns:
        bool: True if the repository was successfully cloned, False otherwise.
    """
    try:
        # 임시 디렉토리가 있으면 삭제
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        # 원본 저장소 클론
        run_command(f"git clone {original_repo} {temp_dir}")
        return True
    except Exception as e:
        print(f"Laravel 클론 오류 발생: {e}")
        return False


def update_branch_docs(branch, temp_dir, excluded_files):
    """
    Update documentation files for a specific branch from a cloned Laravel documentation repository.
    
    Copies all markdown files from the specified branch in the temporary directory to an "origin" subdirectory within the branch folder in the current working directory. Files listed in `excluded_files` are also copied to a "ko" subdirectory.
    
    Parameters:
        branch (str): The name of the branch to update.
        temp_dir (str): Path to the temporary directory containing the cloned repository.
        excluded_files (list): List of markdown file names (case-insensitive) to also copy to the "ko" directory.
    
    Returns:
        bool: True if the update succeeds, False if an error occurs.
    """
    try:
        run_command(f"git checkout {branch}", cwd=temp_dir)

        # 현재 프로젝트의 해당 브랜치 디렉토리 확인
        branch_dir = os.path.join(os.getcwd(), branch)
        origin_dir = os.path.join(branch_dir, "origin")
        ko_dir = os.path.join(branch_dir, "ko")

        # 디렉토리가 없으면 생성
        os.makedirs(origin_dir, exist_ok=True)
        os.makedirs(ko_dir, exist_ok=True)

        # 원본 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]

        # 각 마크다운 파일 복사
        for file_name in md_files:
            source_path = os.path.join(temp_dir, file_name)
            shutil.copy2(source_path, os.path.join(origin_dir, file_name))
            # 번역 제외 파일은 그대로 복사
            if file_name.lower() in excluded_files:
                shutil.copy2(source_path, os.path.join(ko_dir, file_name))

        print(f"{branch} 브랜치, 문서 업데이트 완료")
        return True
    except Exception as e:
        print(f"{branch} 브랜치, 문서 업데이트 오류 발생: {e}")
        return False
