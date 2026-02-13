"""FilePath 값 객체 - 파일 경로를 표현"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class FilePath:
    """파일 경로를 표현하는 값 객체"""

    path: str

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("File path cannot be empty")

    @property
    def filename(self) -> str:
        """파일명만 반환"""
        return os.path.basename(self.path)

    @property
    def directory(self) -> str:
        """디렉터리 경로 반환"""
        return os.path.dirname(self.path)

    @property
    def extension(self) -> str:
        """확장자 반환"""
        return os.path.splitext(self.path)[1]

    def is_markdown(self) -> bool:
        """마크다운 파일인지 확인"""
        return self.extension.lower() == ".md"

    def join(self, *paths: str) -> "FilePath":
        """경로 결합"""
        return FilePath(os.path.join(self.path, *paths))

    def exists(self) -> bool:
        """파일 존재 여부 확인"""
        return os.path.exists(self.path)

    def __str__(self) -> str:
        return self.path
