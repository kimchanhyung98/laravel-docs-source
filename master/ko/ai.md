# AI 지원 개발 (AI Assisted Development)

- [소개](#introduction)
    - [왜 라라벨인가? (Why Laravel for AI Development?)](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [설치](#installation)
    - [사용 가능한 도구](#available-tools)
    - [AI 가이드라인](#ai-guidelines)
    - [문서 검색](#documentation-search)
    - [IDE 통합](#ide-integration)
- [커스텀 Boost 가이드라인](#custom-guidelines)
    - [프로젝트 가이드라인 추가](#adding-project-guidelines)
    - [패키지 가이드라인](#package-guidelines)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 및 에이전트 기반 개발에 최적화된 프레임워크입니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot) 등의 AI 코딩 에이전트의 등장으로 개발자가 코드를 작성하는 방식이 크게 변화했습니다. 이러한 도구들은 전체 기능 생성, 복잡한 이슈 디버깅, 코드 리팩터링 등을 놀라운 속도로 수행할 수 있지만, 이들의 성능은 여러분의 코드베이스를 얼마나 잘 이해하는지에 따라 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
### 왜 라라벨인가? (Why Laravel for AI Development?)

Laravel은 명확하게 정의된 규칙(컨벤션)과 구조를 갖추고 있기 때문에 AI 지원 개발에 이상적입니다. AI 에이전트에게 컨트롤러 생성을 요청하면, 해당 파일을 어디에 어떻게 위치시켜야 하는지 명확하게 알 수 있습니다. 새로운 마이그레이션 작성이 필요할 때에도 네이밍 규칙과 파일 위치가 예측 가능합니다. 이런 일관성 덕분에 더 유연한 프레임워크에서 AI 도구들이 겪는 시행착오나 추측을 줄일 수 있습니다.

파일 구성뿐 아니라, Laravel의 명확한 문법과 풍부한 공식 문서는 AI 에이전트들이 적절하고 라라벨스러운(idiomatic) 코드를 작성하는 데 필요한 맥락을 제공합니다. Eloquent 연관관계, 폼 요청, 미들웨어 등은 일정한 패턴을 따르므로 AI가 쉽게 이해하고 재현할 수 있습니다. 그 결과, AI가 생성한 코드는 경험 많은 라라벨 개발자가 작성한 수준의 완성도를 가지며, 단순한 PHP 코드 조각을 이어 붙인 것과는 전혀 다릅니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 여러분의 Laravel 애플리케이션 사이의 격차를 메워주는 도구입니다. Boost는 15가지 이상의 전문화된 도구를 내장한 MCP(Model Context Protocol) 서버로, AI 에이전트가 애플리케이션의 구조, 데이터베이스, 라우트 등 다양한 정보를 깊이 이해하도록 지원합니다. Boost를 설치하면, 일반적인 범용 코드 어시스턴트였던 AI가 여러분의 애플리케이션을 제대로 이해하는 '라라벨 전문가'로 변신합니다.

Boost의 주요 기능은 세 가지입니다. 첫째, MCP 도구 모음을 통해 애플리케이션을 탐색하고 상호작용할 수 있습니다. 둘째, Laravel 생태계에 최적화된 AI 가이드라인을 제공하여 AI가 올바른 관행을 따르도록 돕습니다. 셋째, 17,000건이 넘는 Laravel 관련 정보가 포함된 강력한 문서 API를 제공합니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상이 구동되는 Laravel 10, 11, 12 버전에서 설치할 수 있습니다. 시작하려면 개발용 의존성으로 Boost를 설치하세요.

```shell
composer require laravel/boost --dev
```

설치 후, 인터랙티브 설치 도구를 실행하세요.

```shell
php artisan boost:install
```

설치 도중 여러분이 사용하는 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 통합 옵션을 선택할 수 있습니다. Boost는 MCP 호환 에디터용 `.mcp.json` 같은 설정 파일과, AI 컨텍스트 파일용 가이드라인 파일을 자동으로 생성합니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json`과 같은 생성된 설정 파일들은, 각 개발자가 자신의 환경을 따로 구성하도록 하고 싶다면 `.gitignore`에 추가해도 안전합니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트가 Laravel 애플리케이션을 정밀하게 이해하고 탐색할 수 있도록 다양한 도구를 제공합니다.

<div class="content-list" markdown="1">

- **애플리케이션 정보 조회** – PHP/Laravel 버전, 설치된 패키지 목록, 설정값, 환경 변수 등을 조회할 수 있습니다.
- **데이터베이스 도구** – 데이터베이스 스키마 확인, 읽기 전용 쿼리 실행, 데이터 구조 파악이 대화 중에 가능합니다.
- **라우트 탐색** – 등록된 모든 라우트의 미들웨어, 컨트롤러, 파라미터 등을 확인할 수 있습니다.
- **Artisan 명령어** – 사용 가능한 Artisan 명령어와 인수를 탐색할 수 있어서, AI가 적절한 명령어 제안 및 실행이 가능합니다.
- **로그 분석** – 애플리케이션 로그 파일을 읽고 분석함으로써 버그 추적을 도와줍니다.
- **브라우저 로그** – 프론트엔드 개발 시 브라우저 콘솔 로그와 에러를 열람할 수 있습니다.
- **Tinker 통합** – Laravel Tinker를 통한 PHP 코드 실행으로, AI가 가설을 테스트하거나 동작을 검증할 수 있습니다.
- **문서 검색** – 설치된 패키지 버전에 맞는 Laravel 생태계의 공식 문서 검색 결과를 제공합니다.

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost에는 Laravel 생태계에 특화된 AI 가이드라인이 포함되어 있습니다. 이 가이드라인은 AI 에이전트가 관례에 맞는 라라벨 코드를 작성하고, 프레임워크 규칙을 지키며, 흔히 저지르는 실수를 피하도록 교육합니다. 가이드라인은 컴포저블(조합 가능) 및 버전 인식 기능을 갖추고 있어, 프로젝트의 패키지 버전에 최적화된 지침을 제공합니다.

가이드라인은 라라벨 자체는 물론, 다음을 포함한 16개 이상의 Laravel 생태계 패키지를 지원합니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Vue 변종)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 기타 다수

</div>

`boost:install` 명령어를 실행하면, Boost가 애플리케이션 내 사용 중인 패키지를 자동으로 감지하여 해당 가이드라인을 프로젝트의 AI 컨텍스트 파일로 편성합니다.

<a name="documentation-search"></a>
### 문서 검색

Boost에는 17,000건 이상의 Laravel 생태계 공식 문서에 접근할 수 있는 강력한 문서 API가 포함되어 있습니다. 일반적인 웹 검색과는 달리, 이 문서는 색인화 및 벡터화되어 있으며, 사용 중인 패키지 버전에 정확히 맞게 필터링됩니다.

AI 에이전트가 특정 기능 사용법을 이해해야 할 때 Boost의 문서 API를 검색하면, 해당되는 정확한 버전의 정보를 받아볼 수 있습니다. 이로써 AI가 구버전의 문법이나 더 이상 권장되지 않는(deprecated) 메서드를 제안하는 문제를 줄일 수 있습니다.

<a name="ide-integration"></a>
### IDE 통합

Boost는 Model Context Protocol을 지원하는 주요 IDE와 AI 도구들과 통합할 수 있습니다. 아래는 인기 있는 에디터에서 Boost를 활성화하는 방법입니다.

```text tab="Claude Code"
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요할 경우:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 명령어를 실행: claude mcp add laravel-boost -- php artisan boost:mcp
```

```text tab=Cursor
// torchlight! {"lineNumbers": false}
1. 커맨드 팔레트(Cmd+Shift+P 또는 Ctrl+Shift+P)를 엽니다.
2. "MCP: Open Settings"를 선택합니다.
3. "laravel-boost" 옵션을 켭니다.
```

```text tab="VS Code"
// torchlight! {"lineNumbers": false}
1. 커맨드 팔레트(Cmd+Shift+P 또는 Ctrl+Shift+P)를 엽니다.
2. "MCP: List Servers"를 선택합니다.
3. "laravel-boost"를 찾아 엔터를 누릅니다.
4. "Start server"를 선택합니다.
```

```text tab=PhpStorm
// torchlight! {"lineNumbers": false}
1. Shift 키를 두 번 눌러 Search Everywhere를 엽니다.
2. "MCP Settings"를 검색해 엔터를 누릅니다.
3. "laravel-boost" 옆의 체크박스를 활성화합니다.
4. "Apply"를 클릭합니다.
```

```text tab=Codex
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요할 경우:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 명령어를 실행: codex mcp add -- php artisan boost:mcp
```

```text tab=Gemini
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요할 경우:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 명령어를 실행: gemini mcp add laravel-boost -- php artisan boost:mcp
```

<a name="custom-guidelines"></a>
## 커스텀 Boost 가이드라인

Boost에 내장된 가이드라인은 Laravel 생태계를 폭넓게 다루지만, 프로젝트별로 AI 에이전트에게 전달하고 싶은 내용을 직접 추가할 수도 있습니다.

<a name="adding-project-guidelines"></a>
### 프로젝트 가이드라인 추가

프로젝트 맞춤 가이드라인을 추가하려면, 애플리케이션의 `.ai/guidelines` 디렉터리에 `.blade.php` 또는 `.md` 파일을 생성하세요.

```text
.ai/
└── guidelines/
    └── api-conventions.md
    ├── architecture.md
    ├── testing-standards.blade.php
```

이 폴더의 파일들은 `boost:install` 실행 시 자동으로 AI 컨텍스트에 포함됩니다. 팀의 코딩 규칙, 아키텍처 결정사항, 도메인별 용어, AI가 더 나은 코드를 작성할 수 있도록 돕는 모든 참고사항을 이곳에 문서화하세요.

<a name="package-guidelines"></a>
### 패키지 가이드라인

Laravel 패키지 개발자가 자신의 패키지를 AI가 더 잘 이해할 수 있도록 가이드라인을 제공하고 싶다면, 패키지의 `resources/boost/guidelines` 디렉터리에 가이드라인 파일을 포함할 수 있습니다.

```text
resources/
└── boost/
    └── guidelines/
        └── core.blade.php
```

AI 가이드라인에는 패키지가 무엇을 하는지 간략한 설명, 필요한 파일 구조나 관례, 주요 기능 사용법(명령어나 코드 조각 예시 등)을 담아야 합니다. 설명은 명확하고 간결하며, 모범 사례 중심으로 작성하여 AI가 사용자를 위해 올바른 코드를 생성할 수 있도록 해야 합니다. 아래는 예시입니다.

```md
## 패키지 이름

이 패키지는 [기능 간략 설명]을 제공합니다.

### 주요 기능

- 기능 1: [간단명료한 설명].
- 기능 2: [간단명료한 설명]. 사용 예시:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

사용자가 여러분의 패키지가 포함된 애플리케이션에 Boost를 설치하면, 해당 가이드라인이 자동으로 AI 컨텍스트에 추가됩니다. 이를 통해 패키지 개발자가 AI 에이전트에게 패키지의 적절한 사용법을 안내할 수 있습니다.
