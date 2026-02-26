"""Document 엔티티 - 번역 대상 문서를 표현"""

from dataclasses import dataclass

from src.domain.value_objects.branch import Branch
from src.domain.value_objects.file_path import FilePath


@dataclass
class Document:
    """번역 대상 문서 엔티티"""

    source_path: FilePath
    target_path: FilePath
    branch: Branch
    content: str | None = None
    translated_content: str | None = None

    @property
    def filename(self) -> str:
        """파일명 반환"""
        return self.source_path.filename

    def is_excluded(self, excluded_files: list[str]) -> bool:
        """제외 대상 파일인지 확인"""
        return self.filename.lower() in [f.lower() for f in excluded_files]

    def has_content(self) -> bool:
        """콘텐츠가 있는지 확인"""
        return bool(self.content and self.content.strip())

    def is_translated(self) -> bool:
        """번역이 완료되었는지 확인"""
        return bool(self.translated_content)

    def set_content(self, content: str) -> None:
        """콘텐츠 설정"""
        self.content = content

    def set_translated_content(self, translated: str) -> None:
        """번역된 콘텐츠 설정"""
        self.translated_content = translated

    @classmethod
    def create(cls, branch: Branch, filename: str, base_dir: str = ".") -> "Document":
        """팩터리 메서드: 브랜치와 파일명으로 Document 생성"""
        import os

        source = FilePath(os.path.join(base_dir, str(branch), "origin", filename))
        target = FilePath(os.path.join(base_dir, str(branch), "ko", filename))
        return cls(source_path=source, target_path=target, branch=branch)
