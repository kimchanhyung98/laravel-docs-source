<div align="center">

# 라라벨 한국어 문서

[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/kimchanhyung98/laravel-docs-source/main?label=Last%20Updated)](https://github.com/kimchanhyung98/laravel-docs-source/commits/main)
[![License](https://img.shields.io/github/license/kimchanhyung98/laravel-docs-source)](https://github.com/kimchanhyung98/laravel-docs-source/blob/main/LICENSE)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 공식 문서를 한국어로 번역하고 최신 상태를 유지합니다.

이 프로젝트는 문서 번역을 관리하며, 번역된 마크다운 문서는 [laravel-docs-web](https://github.com/letsescape/laravel-docs-web)에서 호스팅됩니다.

- 지원 버전 : `master`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 업데이트 주기 : 매일 04시 (KST)
- 번역 엔진 : OpenAI GPT-4.1 및 [번역 프롬프트](translation_prompt.txt)

## 실행

전체 번역 및 동기화 스크립트를 로컬 환경에서 간편하게 실행해 볼 수 있습니다.
`.env.example` 파일을 복사하여 `.env` 파일을 만들어, `OPENAI_API_KEY`를 추가하고, 스크립트를 실행합니다.

```bash
chmod +x run.sh
./run.sh
```

## 라이선스

- 번역 코드 : MIT License
- 라라벨 문서 : MIT License `(Copyright (c) Taylor Otwell)`
