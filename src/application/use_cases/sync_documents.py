"""SyncDocumentsUseCase - 문서 동기화 유스케이스"""

from dataclasses import dataclass

from src.application.ports.document_repository import DocumentRepository
from src.domain.value_objects.branch import Branch


@dataclass
class SyncDocumentsResult:
    """문서 동기화 결과"""

    success: bool
    synced_branches: list[str]
    failed_branches: list[str]
    message: str


class SyncDocumentsUseCase:
    """원본 Laravel 문서 저장소에서 문서를 동기화하는 유스케이스"""

    def __init__(
        self,
        document_repository: DocumentRepository,
        repo_url: str = "https://github.com/laravel/docs.git",
        temp_dir: str = "temp",
        excluded_files: list[str] | None = None
    ):
        self._document_repository = document_repository
        self._repo_url = repo_url
        self._temp_dir = temp_dir
        self._excluded_files = excluded_files or ["license.md", "readme.md"]

    def execute(self, branches: list[Branch] | None = None) -> SyncDocumentsResult:
        """문서 동기화 실행"""
        if branches is None:
            branches = Branch.all_branches()

        synced_branches: list[str] = []
        failed_branches: list[str] = []

        # 임시 디렉터리 정리 및 저장소 클론
        self._document_repository.remove_directory(self._temp_dir)

        if not self._document_repository.clone_repository(self._repo_url, self._temp_dir):
            return SyncDocumentsResult(
                success=False,
                synced_branches=[],
                failed_branches=[str(b) for b in branches],
                message="저장소 클론 실패"
            )

        # 각 브랜치별로 문서 동기화
        for branch in branches:
            if self._sync_branch(branch):
                synced_branches.append(str(branch))
            else:
                failed_branches.append(str(branch))

        # 임시 디렉터리 정리
        self._document_repository.remove_directory(self._temp_dir)

        return SyncDocumentsResult(
            success=len(failed_branches) == 0,
            synced_branches=synced_branches,
            failed_branches=failed_branches,
            message=f"{len(synced_branches)}개 브랜치 동기화 완료"
        )

    def _sync_branch(self, branch: Branch) -> bool:
        """개별 브랜치 동기화"""
        try:
            # 브랜치 체크아웃
            if not self._document_repository.checkout_branch(self._temp_dir, branch):
                print(f"{branch} 브랜치 체크아웃 실패")
                return False

            # 대상 디렉터리 준비
            import os
            origin_dir = os.path.join(os.getcwd(), str(branch), "origin")
            ko_dir = os.path.join(os.getcwd(), str(branch), "ko")

            self._document_repository.ensure_directory(origin_dir)
            self._document_repository.ensure_directory(ko_dir)

            # 마크다운 파일 복사
            md_files = self._document_repository.get_markdown_files(self._temp_dir)

            for filename in md_files:
                source_path = os.path.join(self._temp_dir, filename)
                origin_target = os.path.join(origin_dir, filename)

                self._document_repository.copy_file(source_path, origin_target)

                # 제외 파일은 ko 디렉터리에도 복사
                if filename.lower() in self._excluded_files:
                    ko_target = os.path.join(ko_dir, filename)
                    self._document_repository.copy_file(source_path, ko_target)

            print(f"{branch} 브랜치, 문서 업데이트 완료")
            return True

        except Exception as e:
            print(f"{branch} 브랜치, 문서 업데이트 오류 발생: {e}")
            return False
