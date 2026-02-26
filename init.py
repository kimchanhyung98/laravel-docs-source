"""Laravel 문서 초기화 도구 - 전체 문서 번역 (초기 설정용)

DDD/클린 아키텍처 기반으로 구조화된 문서 번역 도구.
이 스크립트는 모든 브랜치의 모든 문서를 처음부터 번역합니다.
"""

import os
import time

from dotenv import load_dotenv

from src.config.settings import Settings
from src.domain.services.markdown_filter import MarkdownFilterService
from src.domain.value_objects.branch import Branch
from src.domain.value_objects.file_path import FilePath
from src.infrastructure.repositories.file_document_repository import FileDocumentRepository
from src.infrastructure.services.command_git_service import CommandGitService
from src.infrastructure.services.openai_translation_service import OpenAITranslationService


def main():
    """
    모든 브랜치의 모든 문서를 처음부터 번역하는 초기화 스크립트.

    실행 흐름:
    1. 원본 저장소 클론
    2. 각 브랜치별로:
       - origin 디렉터리에 마크다운 파일 복사
       - 제외 파일이 아닌 경우 번역하여 ko 디렉터리에 저장
    3. Git에 변경사항 스테이징
    """
    load_dotenv()

    # 의존성 생성
    settings = Settings.from_environment()
    document_repository = FileDocumentRepository()
    git_service = CommandGitService()
    markdown_filter = MarkdownFilterService()

    try:
        translation_service = OpenAITranslationService(
            prompt_file=settings.prompt_file,
            timeout_seconds=settings.translation_timeout
        )
    except ValueError as e:
        print(f"번역 서비스 초기화 실패: {e}")
        return

    temp_dir = settings.temp_dir

    # 임시 디렉터리 정리 및 저장소 클론
    document_repository.remove_directory(temp_dir)

    print("\n[1] 문서 복사")
    if not document_repository.clone_repository(settings.original_repo_url, temp_dir):
        print("저장소 클론 실패")
        return

    print("\n[2] 문서 번역")
    branches = [Branch(name) for name in settings.branches]

    for branch in branches:
        print(f"\n브랜치: {branch}")

        if not document_repository.checkout_branch(temp_dir, branch):
            print(f"{branch} 브랜치 체크아웃 실패")
            continue

        origin_dir = os.path.join(os.getcwd(), str(branch), "origin")
        ko_dir = os.path.join(os.getcwd(), str(branch), "ko")
        document_repository.ensure_directory(origin_dir)
        document_repository.ensure_directory(ko_dir)

        # 마크다운 파일 목록 가져오기
        md_files = document_repository.get_markdown_files(temp_dir)
        print(f"파일 {len(md_files)}개")

        for file_name in md_files:
            source_path = os.path.join(temp_dir, file_name)

            # origin에 복사
            origin_target_path = os.path.join(origin_dir, file_name)
            document_repository.copy_file(source_path, origin_target_path)

            ko_target_path = os.path.join(ko_dir, file_name)

            # 번역 제외 파일
            if file_name.lower() in settings.excluded_files:
                document_repository.copy_file(source_path, ko_target_path)
            else:
                print(f"번역 시작: {file_name}")
                try:
                    # 콘텐츠 읽기 및 필터링
                    content = document_repository.read_file(source_path)
                    if not content.strip():
                        continue

                    filtered_content = markdown_filter.filter(content, str(branch))

                    # 토큰 수 확인
                    token_count = translation_service.get_token_count(filtered_content)
                    print(f"{file_name}: {token_count:,} 토큰")

                    # 번역
                    from src.domain.value_objects.language import Language
                    translated = translation_service.translate(
                        filtered_content,
                        Language.english(),
                        Language.korean()
                    )

                    # 저장
                    document_repository.write_file(ko_target_path, translated)
                    print(f"번역 완료: {file_name}")
                    time.sleep(settings.translation_delay)

                except Exception as e:
                    print(f"번역 오류 ({file_name}): {type(e).__name__}")

        print(f"브랜치: {branch}, 완료")

    document_repository.remove_directory(temp_dir)
    git_service.add_all_markdown_files()
    print("\n번역 완료")


if __name__ == "__main__":
    main()
