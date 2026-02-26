"""Settings - 애플리케이션 설정 관리"""

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    """애플리케이션 설정"""

    # 저장소 설정
    original_repo_url: str = "https://github.com/laravel/docs.git"
    temp_dir: str = "temp"

    # 브랜치 설정
    branches: list[str] = field(default_factory=lambda: [
        "master", "12.x", "11.x", "10.x", "9.x", "8.x"
    ])

    # 제외 파일
    excluded_files: list[str] = field(default_factory=lambda: [
        "license.md", "readme.md"
    ])

    # 번역 설정
    translation_delay: int = 10
    translation_timeout: int = 1000
    prompt_file: str = "prompt.md"

    # 언어 설정
    source_language: str = "en"
    target_language: str = "ko"

    @classmethod
    def from_environment(cls) -> "Settings":
        """환경 변수에서 설정 로드"""
        settings = cls()

        # 번역 딜레이
        try:
            delay = int(os.environ.get("TRANSLATION_DELAY", "10"))
            if delay > 0:
                settings.translation_delay = delay
        except ValueError:
            print("TRANSLATION_DELAY 환경 변수 값이 유효하지 않음. 기본값 10초 사용.")

        return settings
