"""Laravel 문서 번역 자동화 - 메인 진입점

DDD/클린 아키텍처 기반으로 구조화된 문서 번역 도구.
의존성 주입을 통해 각 계층 간의 결합도를 낮추고 테스트 용이성을 높임.
"""

from dotenv import load_dotenv

from src.application.use_cases.sync_documents import SyncDocumentsUseCase
from src.application.use_cases.translate_document import TranslateDocumentUseCase
from src.config.settings import Settings
from src.domain.services.markdown_filter import MarkdownFilterService
from src.domain.value_objects.branch import Branch
from src.infrastructure.repositories.file_document_repository import FileDocumentRepository
from src.infrastructure.services.command_git_service import CommandGitService
from src.infrastructure.services.openai_translation_service import OpenAITranslationService


def create_sync_use_case(settings: Settings) -> SyncDocumentsUseCase:
    """문서 동기화 유스케이스 생성 (의존성 주입)"""
    document_repository = FileDocumentRepository()

    return SyncDocumentsUseCase(
        document_repository=document_repository,
        repo_url=settings.original_repo_url,
        temp_dir=settings.temp_dir,
        excluded_files=settings.excluded_files
    )


def create_translate_use_case(settings: Settings) -> TranslateDocumentUseCase:
    """문서 번역 유스케이스 생성 (의존성 주입)"""
    document_repository = FileDocumentRepository()
    translation_service = OpenAITranslationService(
        prompt_file=settings.prompt_file,
        timeout_seconds=settings.translation_timeout
    )
    git_service = CommandGitService()
    markdown_filter = MarkdownFilterService()

    return TranslateDocumentUseCase(
        document_repository=document_repository,
        translation_service=translation_service,
        git_service=git_service,
        markdown_filter=markdown_filter,
        excluded_files=settings.excluded_files,
        translation_delay=settings.translation_delay
    )


def main():
    """
    Laravel 문서 번역 자동화 메인 함수.

    DDD/클린 아키텍처 원칙에 따라 구조화:
    - Domain Layer: 핵심 비즈니스 로직 (엔티티, 값 객체, 도메인 서비스)
    - Application Layer: 유스케이스 및 애플리케이션 서비스
    - Infrastructure Layer: 외부 시스템 연동 (Git, OpenAI, 파일시스템)

    실행 흐름:
    1. 환경 변수 로드 및 설정 초기화
    2. 원본 Laravel 문서 저장소 동기화
    3. 변경된 문서 번역
    4. Git에 변경사항 스테이징
    """
    load_dotenv()

    # 설정 로드
    settings = Settings.from_environment()

    # 브랜치 객체 생성
    branches = [Branch(name) for name in settings.branches]

    # [1] 문서 동기화
    print("\n[1] 브랜치별 문서 처리")
    sync_use_case = create_sync_use_case(settings)
    sync_result = sync_use_case.execute(branches)

    if not sync_result.success:
        print(f"문서 동기화 실패: {sync_result.message}")
        if sync_result.failed_branches:
            print(f"실패한 브랜치: {', '.join(sync_result.failed_branches)}")

    # [2] 변경된 문서 번역
    print("\n[2] 변경된 파일 번역")
    translate_use_case = create_translate_use_case(settings)
    translate_result = translate_use_case.execute()

    print(f"\n{translate_result.message}")
    if translate_result.translated_count > 0:
        print(f"번역됨: {translate_result.translated_count}개")
    if translate_result.skipped_count > 0:
        print(f"건너뜀: {translate_result.skipped_count}개")
    if translate_result.failed_count > 0:
        print(f"실패: {translate_result.failed_count}개")

    print("\n갱신 완료")


if __name__ == "__main__":
    main()
