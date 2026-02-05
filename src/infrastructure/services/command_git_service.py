"""CommandGitService - 명령줄 기반 Git 서비스 구현"""

import os
import subprocess
from pathlib import Path

from src.application.ports.git_service import GitService

# 경로 구조 상수
ORIGIN_DIR_NAME = "origin"
MIN_PATH_PARTS = 3


class CommandGitService(GitService):
    """명령줄 기반 Git 서비스 구현체"""

    def __init__(self, working_dir: str | None = None):
        self._working_dir = working_dir or os.getcwd()

    def get_changed_files(self, file_extension: str = ".md") -> list[str]:
        """변경된 파일 목록 가져오기"""
        try:
            status_output = self._run_command(["git", "status", "--porcelain"])

            changed_files: set[str] = set()

            for line in status_output.split('\n'):
                if not line.strip():
                    continue

                if len(line) >= 3:
                    file_path = line[2:].lstrip()
                else:
                    continue

                if file_path.endswith(file_extension):
                    norm_path = os.path.normpath(file_path)
                    path_parts = norm_path.split(os.sep)

                    # origin 디렉터리가 포함된 경로만 추가
                    if len(path_parts) >= MIN_PATH_PARTS and ORIGIN_DIR_NAME in path_parts[1:]:
                        changed_files.add(file_path)

            return sorted(changed_files)

        except subprocess.CalledProcessError:
            print("Git 오류 발생")
            return []

    def add_files(self, pattern: str) -> bool:
        """파일을 스테이징 영역에 추가

        Note: pattern이 glob 패턴인 경우 pathlib을 사용하여 파일을 찾아 개별적으로 추가합니다.
        """
        try:
            # glob 패턴으로 파일 찾기
            files = list(Path(self._working_dir).glob(pattern))
            if files:
                file_paths = [str(f.relative_to(self._working_dir)) for f in files]
                self._run_command(["git", "add"] + file_paths)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git 파일 추가 오류: {e}")
            return False

    def add_all_markdown_files(self) -> bool:
        """모든 마크다운 파일 스테이징"""
        try:
            # pathlib을 사용하여 모든 마크다운 파일 찾기
            patterns = ["*.md", "*/*.md", "*/*/*.md"]
            all_files: list[str] = []

            for pattern in patterns:
                files = list(Path(self._working_dir).glob(pattern))
                all_files.extend([str(f.relative_to(self._working_dir)) for f in files])

            if all_files:
                self._run_command(["git", "add"] + all_files)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git 파일 추가 오류: {e}")
            return False

    def _run_command(self, command: list[str]) -> str:
        """명령어 실행 (shell=False로 안전하게 실행)"""
        result = subprocess.run(
            command,
            shell=False,
            check=True,
            text=True,
            capture_output=True,
            cwd=self._working_dir
        )
        return result.stdout.strip()
