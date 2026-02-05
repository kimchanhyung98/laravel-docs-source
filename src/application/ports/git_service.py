"""GitService 인터페이스 - Git 작업 포트"""

from abc import ABC, abstractmethod


class GitService(ABC):
    """Git 작업 인터페이스"""

    @abstractmethod
    def get_changed_files(self, file_extension: str = ".md") -> list[str]:
        """변경된 파일 목록 가져오기"""
        pass

    @abstractmethod
    def add_files(self, pattern: str) -> bool:
        """파일을 스테이징 영역에 추가"""
        pass

    @abstractmethod
    def add_all_markdown_files(self) -> bool:
        """모든 마크다운 파일 스테이징"""
        pass
