"""TranslateDocumentUseCase - 문서 번역 유스케이스"""

import os
import time
from dataclasses import dataclass

from src.application.ports.document_repository import DocumentRepository
from src.application.ports.git_service import GitService
from src.application.ports.translation_service import TranslationService
from src.domain.entities.document import Document
from src.domain.services.markdown_filter import MarkdownFilterService
from src.domain.value_objects.branch import Branch
from src.domain.value_objects.language import Language

# 경로 구조 상수
ORIGIN_DIR_NAME = "origin"
MIN_PATH_PARTS = 3  # branch/origin/filename.md
BRANCH_INDEX = 0
ORIGIN_INDEX = 1
FILENAME_INDEX = 2


@dataclass
class TranslateDocumentsResult:
    """문서 번역 결과"""

    success: bool
    translated_count: int
    skipped_count: int
    failed_count: int
    message: str


class TranslateDocumentUseCase:
    """변경된 문서를 번역하는 유스케이스"""

    def __init__(
        self,
        document_repository: DocumentRepository,
        translation_service: TranslationService,
        git_service: GitService,
        markdown_filter: MarkdownFilterService | None = None,
        excluded_files: list[str] | None = None,
        translation_delay: int = 10
    ):
        self._document_repository = document_repository
        self._translation_service = translation_service
        self._git_service = git_service
        self._markdown_filter = markdown_filter or MarkdownFilterService()
        self._excluded_files = excluded_files or ["license.md", "readme.md"]
        self._translation_delay = translation_delay

    def execute(
        self,
        source_lang: Language | None = None,
        target_lang: Language | None = None
    ) -> TranslateDocumentsResult:
        """변경된 문서 번역 실행"""
        source_lang = source_lang or Language.english()
        target_lang = target_lang or Language.korean()

        changed_files = self._git_service.get_changed_files(".md")

        if not changed_files:
            print("변경된 문서가 없음")
            return TranslateDocumentsResult(
                success=True,
                translated_count=0,
                skipped_count=0,
                failed_count=0,
                message="변경된 문서 없음"
            )

        translated_count = 0
        skipped_count = 0
        failed_count = 0
        processed_files: set[str] = set()

        for file_path in changed_files:
            result = self._process_file(
                file_path, processed_files, source_lang, target_lang
            )
            if result == "translated":
                translated_count += 1
                time.sleep(self._translation_delay)
            elif result == "skipped":
                skipped_count += 1
            elif result == "failed":
                failed_count += 1

        # Git에 변경사항 추가
        self._git_service.add_all_markdown_files()

        return TranslateDocumentsResult(
            success=failed_count == 0,
            translated_count=translated_count,
            skipped_count=skipped_count,
            failed_count=failed_count,
            message=f"{translated_count}개 문서 번역 완료"
        )

    def _process_file(
        self,
        file_path: str,
        processed_files: set[str],
        source_lang: Language,
        target_lang: Language
    ) -> str:
        """개별 파일 처리"""
        norm_path = os.path.normpath(file_path)
        path_parts = norm_path.split(os.sep)

        # 경로 구조 검증: branch/origin/filename.md
        if len(path_parts) < MIN_PATH_PARTS or path_parts[ORIGIN_INDEX] != ORIGIN_DIR_NAME:
            return "skipped"

        branch_name = path_parts[BRANCH_INDEX]
        filename = path_parts[FILENAME_INDEX]

        # 유효한 브랜치인지 확인
        try:
            branch = Branch(branch_name)
        except ValueError:
            return "skipped"

        # 중복 처리 방지
        file_key = f"{branch}/{filename}"
        if file_key in processed_files:
            return "skipped"
        processed_files.add(file_key)

        # 제외 파일 확인
        if filename.lower() in self._excluded_files:
            print(f"예외 파일: {file_key}")
            return "skipped"

        # Document 엔티티 생성
        document = Document.create(branch, filename)

        # 원본 파일 확인
        if not self._document_repository.file_exists(str(document.source_path)):
            return "skipped"

        # 번역 실행
        return self._translate_document(document, source_lang, target_lang)

    def _translate_document(
        self,
        document: Document,
        source_lang: Language,
        target_lang: Language
    ) -> str:
        """문서 번역 실행"""
        try:
            # 콘텐츠 읽기
            content = self._document_repository.read_file(str(document.source_path))
            if not content.strip():
                print(f"빈 파일: {document.source_path}")
                return "skipped"

            document.set_content(content)

            print(f"번역 시작: {document.source_path}")

            # 마크다운 필터링 적용
            filtered_content = self._markdown_filter.filter(
                content, str(document.branch)
            )

            # 토큰 수 확인
            token_count = self._translation_service.get_token_count(filtered_content)
            print(f"{document.source_path}: {token_count:,} 토큰")

            # 임시로 필터링된 콘텐츠 설정
            document.set_content(filtered_content)

            # 번역
            translated_document = self._translation_service.translate_document(
                document, source_lang, target_lang
            )

            # 저장
            if self._document_repository.save_document(translated_document):
                print(f"번역 완료: {document.source_path} -> {document.target_path}")
                return "translated"
            else:
                return "failed"

        except Exception as e:
            print(f"번역 오류: {type(e).__name__} - {e}")
            return "failed"
