"""FileDocumentRepository - 파일 시스템 기반 문서 저장소 구현"""

import os
import shutil
import subprocess

from src.application.ports.document_repository import DocumentRepository
from src.domain.entities.document import Document
from src.domain.value_objects.branch import Branch


class FileDocumentRepository(DocumentRepository):
    """파일 시스템 기반 문서 저장소 구현체"""

    def __init__(self, base_dir: str | None = None):
        self._base_dir = base_dir or os.getcwd()

    def clone_repository(self, repo_url: str, target_dir: str) -> bool:
        """원격 저장소 클론"""
        try:
            self.remove_directory(target_dir)
            self._run_command(f"git clone {repo_url} {target_dir}")
            return True
        except Exception as e:
            print(f"저장소 클론 오류: {e}")
            return False

    def checkout_branch(self, repo_dir: str, branch: Branch) -> bool:
        """특정 브랜치로 체크아웃"""
        try:
            self._run_command(f"git checkout {branch}", cwd=repo_dir)
            return True
        except Exception as e:
            print(f"브랜치 체크아웃 오류: {e}")
            return False

    def get_markdown_files(self, directory: str) -> list[str]:
        """디렉터리에서 마크다운 파일 목록 가져오기"""
        try:
            files = [f for f in os.listdir(directory) if f.endswith(".md")]
            return sorted(files)
        except Exception:
            return []

    def copy_file(self, source: str, target: str) -> bool:
        """파일 복사"""
        try:
            shutil.copy2(source, target)
            return True
        except Exception as e:
            print(f"파일 복사 오류: {e}")
            return False

    def read_file(self, path: str) -> str:
        """파일 읽기"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, path: str, content: str) -> bool:
        """파일 쓰기"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"파일 쓰기 오류: {e}")
            return False

    def ensure_directory(self, path: str) -> bool:
        """디렉터리 생성 (없으면)"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"디렉터리 생성 오류: {e}")
            return False

    def remove_directory(self, path: str) -> bool:
        """디렉터리 삭제"""
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
            return True
        except Exception as e:
            print(f"디렉터리 삭제 오류: {e}")
            return False

    def file_exists(self, path: str) -> bool:
        """파일 존재 여부 확인"""
        return os.path.exists(path)

    def save_document(self, document: Document) -> bool:
        """Document 엔티티 저장"""
        if not document.is_translated():
            return False

        target_dir = document.target_path.directory
        self.ensure_directory(target_dir)

        return self.write_file(
            str(document.target_path),
            document.translated_content  # type: ignore
        )

    @staticmethod
    def _run_command(command: str, cwd: str | None = None) -> str:
        """명령어 실행"""
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        return result.stdout.strip()
