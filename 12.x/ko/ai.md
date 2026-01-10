# AI 지원 개발 (AI Assisted Development)

- [소개](#introduction)
    - [AI 개발에 Laravel을 사용하는 이유](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [설치](#installation)
    - [사용 가능한 도구](#available-tools)
    - [AI 가이드라인](#ai-guidelines)
    - [문서 검색](#documentation-search)
    - [IDE 연동](#ide-integration)
- [맞춤형 Boost 가이드라인](#custom-guidelines)
    - [프로젝트 가이드라인 추가](#adding-project-guidelines)
    - [패키지 가이드라인](#package-guidelines)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 및 에이전트 기반(Agentic) 개발에 가장 적합한 프레임워크로 독보적인 위치를 차지하고 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장은 개발자가 코드를 작성하는 방식을 완전히 변화시켰습니다. 이 도구들은 전체 기능을 생성하고, 복잡한 문제를 디버깅하며, 놀랄 만큼 빠르게 코드를 리팩터링할 수 있습니다. 그러나 이러한 AI 도구의 효과는 여러분의 코드베이스를 얼마나 잘 이해하고 있는지에 크게 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 Laravel을 사용하는 이유

Laravel의 명확한 규칙과 잘 정의된 구조는 AI 지원 개발에 이상적인 환경을 제공합니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가하라고 요청하면, 컨트롤러가 어디에 생성되어야 하는지 정확하게 알고 있습니다. 또, 새로운 마이그레이션이 필요할 때, 파일 명명 규칙과 위치가 예측 가능합니다. 이러한 일관성은 더 유연한 프레임워크에서 AI 도구가 자주 마주하는 시행착오를 없애줍니다.

파일 구조 외에도, Laravel의 표현력 있는 문법과 방대한 공식 문서는 AI 에이전트가 정확하고 라라벨스러운 코드를 생성하는 데 필요한 맥락을 제공합니다. Eloquent 연관관계, 폼 리퀘스트, 미들웨어 등은 AI가 신뢰도 높게 이해하고 재현할 수 있는 명확한 패턴을 따릅니다. 그 결과 AI가 생성한 코드는 경험 많은 Laravel 개발자가 직접 작성한 것처럼 보이고, 단순한 PHP 코드 조각을 이어붙인 것과는 전혀 다릅니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 여러분의 Laravel 애플리케이션 사이의 간극을 메워주는 도구입니다. Boost는 15개 이상의 전문화된 도구를 장착한 MCP(Model Context Protocol) 서버로, AI 에이전트가 여러분의 애플리케이션 구조, 데이터베이스, 라우팅 등 깊은 정보에 접근할 수 있도록 돕습니다. Boost를 설치하면, 여러분의 AI 에이전트는 범용 코드 어시스턴트에서 여러분의 애플리케이션을 정확히 이해하는 Laravel 전문가로 거듭납니다.

Boost는 세 가지 주요 기능을 제공합니다: 애플리케이션을 점검하고 상호작용할 수 있는 다양한 MCP 도구, Laravel 생태계에 특화된 AI 가이드라인, 그리고 17,000개 이상의 Laravel 전문 지식이 담긴 강력한 문서 API입니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상에서 구동되는 Laravel 10, 11, 12 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발용 의존성으로 설치하세요.

```shell
composer require laravel/boost --dev
```

설치 후, 대화형 인스톨러를 실행합니다.

```shell
php artisan boost:install
```

인스톨러는 여러분의 IDE와 AI 에이전트를 자동으로 감지하며, 프로젝트에 적합한 연동 옵션을 선택할 수 있도록 안내합니다. Boost는 `.mcp.json`(MCP 호환 에디터용)이나, AI 맥락 생성을 위한 가이드라인 파일 등 필요한 설정 파일을 자동으로 생성합니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json` 등과 같은 생성된 설정 파일은 모든 개발자가 자신만의 환경을 설정할 수 있도록 `.gitignore`에 추가해도 무방합니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에게 애플리케이션을 깊이 이해하고 상호작용할 수 있도록 다양한 도구를 제공합니다.

<div class="content-list" markdown="1">

- **애플리케이션 조사** - PHP 및 Laravel 버전 확인, 설치된 패키지 목록, 애플리케이션 설정 및 환경 변수 점검 등
- **데이터베이스 도구** - 데이터베이스 스키마 확인, 읽기 전용 쿼리 실행, 데이터 구조 파악 등
- **라우트 점검** - 등록된 모든 라우트와 해당 미들웨어, 컨트롤러, 파라미터 확인
- **Artisan 명령어** - 사용 가능한 Artisan 명령어와 그 인수 조사로, AI가 적절한 명령어를 제안하고 실행할 수 있도록 지원
- **로그 분석** - 애플리케이션 로그 파일 읽기 및 문제 디버깅 지원
- **브라우저 로그** - Laravel 프론트엔드 도구 사용 시 브라우저 콘솔 로그 및 오류 확인
- **Tinker 연동** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드 실행 및 가설 테스트
- **문서 검색** - 설치된 패키지 버전에 최적화된 결과로 Laravel 생태계 문서 검색

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost에는 Laravel 생태계에 특화된 포괄적인 AI 가이드라인 세트가 포함되어 있습니다. 이 가이드라인은 AI 에이전트에게 Laravel스러운 코드를 작성하고, 프레임워크 관례를 따르며, 자주 범하는 실수를 방지하는 방법을 교육합니다. 가이드라인은 조합·확장 가능하며, 버전에 따라 적합한 내용만 제공되어, 현재 사용 중인 패키지 버전에 정확히 맞는 지침을 받을 수 있습니다.

가이드라인은 Laravel 본체뿐만 아니라 아래를 포함한 16개 이상의 생태계 패키지도 지원합니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Vue 변형 포함)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 기타 다수

</div>

`boost:install` 실행 시, Boost는 애플리케이션에서 사용 중인 패키지를 자동 감지하여 관련된 가이드라인을 프로젝트의 AI 맥락 파일에 포함시킵니다.

<a name="documentation-search"></a>
### 문서 검색

Boost는 17,000개 이상의 Laravel 생태계 문서에 접근할 수 있는 강력한 문서 API를 제공합니다. 일반적인 웹 검색과 달리, 이 문서는 패키지 버전별로 인덱싱 및 벡터화되어, 여러분의 정확한 패키지 버전에 맞는 정보를 제공합니다.

에이전트가 기능을 이해할 필요가 있을 때, Boost의 문서 API로 검색하여 버전에 맞는 정확한 정보를 얻을 수 있습니다. 이로써 AI 에이전트가 구버전 프레임워크 방식이나 오래된 문법을 제안하는 문제를 근본적으로 해결할 수 있습니다.

<a name="ide-integration"></a>
### IDE 연동

Boost는 Model Context Protocol을 지원하는 주요 IDE 및 AI 도구와 연동할 수 있습니다. 아래는 주요 에디터에서 Boost를 활성화하는 방법입니다.

```text tab="Claude Code"
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요하다면:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 다음을 실행합니다: claude mcp add laravel-boost -- php artisan boost:mcp
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
3. "laravel-boost"로 이동해 엔터를 누릅니다.
4. "Start server"를 선택합니다.
```

```text tab=PhpStorm
// torchlight! {"lineNumbers": false}
1. Shift 키를 두번 눌러 Search Everywhere를 엽니다.
2. "MCP Settings"를 검색하고 엔터를 누릅니다.
3. "laravel-boost" 옆 체크박스를 활성화합니다.
4. "Apply"를 클릭합니다.
```

```text tab=Codex
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요하다면:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 다음을 실행합니다: codex mcp add -- php artisan boost:mcp
```

```text tab=Gemini
// torchlight! {"lineNumbers": false}
Boost는 일반적으로 자동으로 감지됩니다. 수동 설정이 필요하다면:

1. 프로젝트 디렉터리에서 터미널을 엽니다.
2. 다음을 실행합니다: gemini mcp add laravel-boost -- php artisan boost:mcp
```

<a name="custom-guidelines"></a>
## 맞춤형 Boost 가이드라인

Boost의 기본 가이드라인만으로도 Laravel 생태계 전반을 폭넓게 지원하지만, 프로젝트별로 AI 에이전트를 위한 추가 지침이 필요할 수도 있습니다.

<a name="adding-project-guidelines"></a>
### 프로젝트 가이드라인 추가

프로젝트에 맞는 맞춤형 가이드라인을 추가하려면, 애플리케이션의 `.ai/guidelines` 디렉터리에 `.blade.php` 또는 `.md` 파일을 생성하세요.

```text
.ai/
└── guidelines/
    └── api-conventions.md
    ├── architecture.md
    ├── testing-standards.blade.php
```

이 파일들은 `boost:install` 실행 시 자동으로 포함됩니다. 팀의 코딩 표준, 아키텍처 결정, 도메인 용어 정의 등 AI 에이전트가 더 나은 코드를 작성하는 데 도움이 되는 모든 맥락을 상세히 기록할 수 있습니다.

<a name="package-guidelines"></a>
### 패키지 가이드라인

Laravel 패키지를 직접 관리하고 있다면, 사용자들을 위한 AI 가이드라인을 패키지의 `resources/boost/guidelines` 디렉터리에 포함시킬 수 있습니다.

```text
resources/
└── boost/
    └── guidelines/
        └── core.blade.php
```

AI 가이드라인 파일에는 패키지 기능의 간단한 개요, 필요한 파일 구조나 권장 관례, 주요 기능 생성 또는 사용 방법(예제 명령어, 코드 스니펫 포함)을 담는 것이 좋습니다. 내용은 간결하고, 실제 활용에 도움이 되도록 하며, 모범 사례 중심으로 작성해 주세요. 아래는 예시입니다.

```md
## Package Name

이 패키지는 [기능에 대한 간단한 설명]을 제공합니다.

### 기능

- 기능 1: [짧고 명확한 설명].
- 기능 2: [짧고 명확한 설명]. 예시 사용법:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

사용자가 여러분의 패키지를 포함한 애플리케이션에 Boost를 설치할 경우, 여러분의 가이드라인도 자동으로 감지되어 AI 맥락에 포함됩니다. 이를 통해 패키지 제작자는 AI 에이전트가 자신이 만든 패키지를 올바르게 활용할 수 있도록 도울 수 있습니다.
