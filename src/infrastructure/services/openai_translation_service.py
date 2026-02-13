"""OpenAITranslationService - OpenAI 기반 번역 서비스 구현"""

import os
import time
from functools import wraps

import openai
import tiktoken
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.application.ports.translation_service import TranslationService
from src.domain.entities.document import Document
from src.domain.value_objects.language import Language


def retry(max_attempts: int = 3, delay: int = 3, backoff: int = 2, exceptions: tuple = (Exception,)):
    """재시도 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        print(f"최대 시도 횟수 초과. 오류: {type(e).__name__} - {e}")
                        raise
                    print(f"재시도 중... ({attempt}/{max_attempts})")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator


class OpenAITranslationService(TranslationService):
    """OpenAI API 기반 번역 서비스 구현체"""

    DEFAULT_TIMEOUT_SECONDS = 1000

    def __init__(
        self,
        prompt_file: str = "prompt.md",
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    ):
        self._prompt_file = prompt_file
        self._timeout_seconds = timeout_seconds
        self._client, self._model = self._get_client()

    def _get_client(self) -> tuple:
        """AI 클라이언트 및 모델 가져오기"""
        provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
        model = os.environ.get("TRANSLATION_MODEL", "gpt-4.1")

        if provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY 미설정")

            openai.api_key = api_key
            client = openai.OpenAI()
            return client, model

        elif provider == "azure":
            api_key = os.environ.get("AZURE_OPENAI_API_KEY")
            endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
            api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-05-01-preview")

            if not api_key or not endpoint:
                raise ValueError("AZURE_OPENAI_API_KEY 또는 AZURE_OPENAI_ENDPOINT 미설정")

            client = openai.AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            return client, model

        else:
            raise ValueError(f"미지원 번역 제공자: {provider}")

    def _get_system_prompt(self, source_lang: Language, target_lang: Language) -> str:
        """시스템 프롬프트 가져오기"""
        with open(self._prompt_file, 'r', encoding='utf-8') as f:
            template = f.read()
        return template.format(source_lang=str(source_lang), target_lang=str(target_lang))

    @retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,))
    def translate(
        self,
        content: str,
        source_lang: Language,
        target_lang: Language
    ) -> str:
        """텍스트 번역

        Note: OpenAI API는 자체적으로 timeout을 지원하며,
        self._timeout_seconds를 통해 설정 가능합니다.
        """
        try:
            system_prompt = self._get_system_prompt(source_lang, target_lang)

            system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
            user_message = ChatCompletionUserMessageParam(role="user", content=content)

            response = self._client.chat.completions.create(
                model=self._model,
                messages=[system_message, user_message],
                timeout=self._timeout_seconds
            )

            return response.choices[0].message.content or ""

        except openai.RateLimitError as e:
            print(f"RateLimitError: {e}")
            time.sleep(30)
            raise
        except Exception as e:
            print(f"번역 오류: {type(e).__name__}")
            raise

    def translate_document(
        self,
        document: Document,
        source_lang: Language,
        target_lang: Language
    ) -> Document:
        """Document 엔티티 번역"""
        if not document.has_content():
            return document

        translated_content = self.translate(
            document.content,  # type: ignore
            source_lang,
            target_lang
        )
        document.set_translated_content(translated_content)
        return document

    def get_token_count(self, text: str) -> int:
        """텍스트의 토큰 수 반환"""
        encoding = tiktoken.encoding_for_model("gpt-4")
        tokens = encoding.encode(text)
        return len(tokens)
