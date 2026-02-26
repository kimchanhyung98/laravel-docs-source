"""Branch 값 객체 - 문서의 브랜치 버전을 표현"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Branch:
    """문서의 브랜치 버전을 표현하는 값 객체"""

    name: str

    VALID_BRANCHES: ClassVar[tuple[str, ...]] = (
        "master", "12.x", "11.x", "10.x", "9.x", "8.x"
    )

    def __post_init__(self) -> None:
        if self.name not in self.VALID_BRANCHES:
            raise ValueError(f"Invalid branch: {self.name}")

    @classmethod
    def all_branches(cls) -> list["Branch"]:
        """지원되는 모든 브랜치 목록 반환"""
        return [cls(name) for name in cls.VALID_BRANCHES]

    def __str__(self) -> str:
        return self.name
