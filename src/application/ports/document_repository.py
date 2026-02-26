"""DocumentRepository 인터페이스 - 문서 저장소 포트"""

from abc import ABC, abstractmethod

from src.domain.entities.document import Document
from src.domain.value_objects.branch import Branch


class DocumentRepository(ABC):
    """문서 저장소 인터페이스"""

    @abstractmethod
    def clone_repository(self, repo_url: str, target_dir: str) -> bool:
        """원격 저장소 클론"""
        pass

    @abstractmethod
    def checkout_branch(self, repo_dir: str, branch: Branch) -> bool:
        """특정 브랜치로 체크아웃"""
        pass

    @abstractmethod
    def get_markdown_files(self, directory: str) -> list[str]:
        """디렉터리에서 마크다운 파일 목록 가져오기"""
        pass

    @abstractmethod
    def copy_file(self, source: str, target: str) -> bool:
        """파일 복사"""
        pass

    @abstractmethod
    def read_file(self, path: str) -> str:
        """파일 읽기"""
        pass

    @abstractmethod
    def write_file(self, path: str, content: str) -> bool:
        """파일 쓰기"""
        pass

    @abstractmethod
    def ensure_directory(self, path: str) -> bool:
        """디렉터리 생성 (없으면)"""
        pass

    @abstractmethod
    def remove_directory(self, path: str) -> bool:
        """디렉터리 삭제"""
        pass

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """파일 존재 여부 확인"""
        pass

    @abstractmethod
    def save_document(self, document: Document) -> bool:
        """Document 엔티티 저장"""
        pass
