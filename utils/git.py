import os
import subprocess

from utils.common import run_command


def get_git_changes():
    """git을 사용하여 현재 프로젝트의 변경된 마크다운 파일 목록을 가져옴

    Returns:
        list: 변경된 마크다운 파일 경로 목록 (branch/origin/filename.md 형식)
    """
    try:
        status_output = run_command("git status --porcelain", cwd=os.getcwd())

        changed_files = set()

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            if len(line) >= 3:
                file_path = line[2:].lstrip()
            else:
                continue

            if file_path.endswith('.md'):
                norm_path = os.path.normpath(file_path)
                path_parts = norm_path.split(os.sep)

                # 경로 검증: origin 디렉토리가 첫 번째가 아닌 위치에 포함된 경로만 추가
                if len(path_parts) >= 3 and 'origin' in path_parts[1:]:
                    changed_files.add(file_path)

        return sorted(changed_files)
    except subprocess.CalledProcessError:
        print("Git 오류 발생")
        return []


def add_files_to_git():
    """변경된 마크다운 파일을 git에 추가

    Returns:
        bool: 성공 여부
    """
    try:
        run_command("git add *.md */*.md */*/*.md", cwd=os.getcwd())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 파일 추가 오류 발생: {e}")
        return False
