"""Language 값 객체 - 언어 코드를 표현"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    """언어를 표현하는 값 객체"""

    code: str

    ENGLISH: str = "en"
    KOREAN: str = "ko"

    def __post_init__(self) -> None:
        if not self.code or len(self.code) != 2:
            raise ValueError(f"Invalid language code: {self.code}")

    @classmethod
    def english(cls) -> "Language":
        """영어 언어 객체 반환"""
        return cls(cls.ENGLISH)

    @classmethod
    def korean(cls) -> "Language":
        """한국어 언어 객체 반환"""
        return cls(cls.KOREAN)

    def __str__(self) -> str:
        return self.code
