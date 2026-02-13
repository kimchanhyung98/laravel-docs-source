"""TranslationService 인터페이스 - 번역 서비스 포트"""

from abc import ABC, abstractmethod

from src.domain.entities.document import Document
from src.domain.value_objects.language import Language


class TranslationService(ABC):
    """번역 서비스 인터페이스"""

    @abstractmethod
    def translate(
        self,
        content: str,
        source_lang: Language,
        target_lang: Language
    ) -> str:
        """텍스트 번역"""
        pass

    @abstractmethod
    def translate_document(
        self,
        document: Document,
        source_lang: Language,
        target_lang: Language
    ) -> Document:
        """Document 엔티티 번역"""
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """텍스트의 토큰 수 반환"""
        pass
