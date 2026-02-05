# AI 지원 개발 (AI Assisted Development)

- [소개](#introduction)
    - [왜 Laravel이 AI 개발에 적합한가?](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [설치](#installation)
    - [사용 가능한 도구](#available-tools)
    - [AI 가이드라인](#ai-guidelines)
    - [에이전트 스킬](#agent-skills)
    - [문서 검색](#documentation-search)
    - [에이전트 통합](#agents-integration)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 AI 지원 및 에이전트 기반 개발에 가장 적합한 프레임워크로 독보적인 위치를 차지하고 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장은 개발자가 코드를 작성하는 방식을 혁신적으로 바꾸고 있습니다. 이러한 도구들은 전체 기능을 생성하고, 복잡한 문제를 디버깅하며, 빠른 속도로 코드를 리팩터링할 수 있습니다. 하지만 이 도구들의 효과는 여러분의 코드베이스를 얼마나 잘 이해하는지에 크게 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
### 왜 Laravel이 AI 개발에 적합한가? (Why Laravel for AI Development?)

Laravel은 명확한 관습(opinionated conventions)과 잘 정의된 구조 덕분에 AI 지원 개발에 이상적인 프레임워크입니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가해달라고 요청하면, 어디에 코드를 생성해야 할지 정확히 알고 있습니다. 새로운 마이그레이션이 필요한 경우에도 네이밍 규칙과 파일 위치가 예측 가능합니다. 이러한 일관성 덕분에, 다른 유연한 프레임워크에서 종종 발생하는 AI 도구의 예측 실패를 줄일 수 있습니다.

파일 구성 이상의 장점으로, Laravel의 표현력 있는 문법과 풍부한 공식 문서는 AI 에이전트가 정확하고 관용적인 코드를 생성할 수 있는 충분한 맥락 정보를 제공합니다. Eloquent 연관관계, Form Request, Middleware 등과 같은 기능들은 표준화된 패턴을 따르기 때문에 에이전트가 쉽게 이해하고 재현할 수 있습니다. 그 결과, AI가 생성한 코드가 마치 숙련된 Laravel 개발자가 작성한 것처럼 자연스럽고, 단순한 PHP 조각들을 억지로 이어 붙인 것과는 완전히 다릅니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 여러분의 Laravel 애플리케이션을 효과적으로 연결해주는 역할을 합니다. Boost는 15개가 넘는 특화 도구가 내장된 MCP(Model Context Protocol) 서버로, AI 에이전트가 애플리케이션의 구조, 데이터베이스, 라우트 등 깊은 수준까지 이해할 수 있도록 도와줍니다. Boost를 설치하면, AI 에이전트는 일반적인 코드 비서에서 여러분 애플리케이션 맞춤형 Laravel 전문가로 탈바꿈합니다.

Boost는 세 가지 주요 역량을 제공합니다. 애플리케이션을 점검하고 상호작용할 수 있는 MCP 도구 모음, Laravel 생태계에 특화되어 작성된 AI 가이드라인, 그리고 17,000개 이상의 Laravel 관련 지식을 담은 강력한 문서 API가 그것입니다.

<a name="installation"></a>
### 설치 (Installation)

Boost는 PHP 8.1 이상을 사용하는 Laravel 10, 11, 12 버전에서 설치할 수 있습니다. 먼저 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후, 대화형 인스톨러를 실행합니다:

```shell
php artisan boost:install
```

이 인스톨러는 사용 중인 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 통합 옵션을 선택하도록 안내합니다. Boost는 MCP-호환 에디터에서 사용하는 `.mcp.json`과 AI 컨텍스트를 위한 가이드라인 파일 등 필요한 설정 파일들을 자동으로 생성합니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json`과 같은 생성된 설정 파일들은 각 개발자가 각자 환경을 설정하길 원한다면 `.gitignore`에 안전하게 추가해둘 수 있습니다.

<a name="available-tools"></a>
### 사용 가능한 도구 (Available Tools)

Boost는 Model Context Protocol을 통해 AI 에이전트에게 다양한 도구를 제공합니다. 이 도구들을 이용하면 에이전트가 여러분의 Laravel 애플리케이션을 깊이 이해하고 실제로 상호작용할 수 있습니다.

<div class="content-list" markdown="1">

- **애플리케이션 내부 점검** - PHP 및 Laravel 버전 조회, 설치된 패키지 목록 확인, 애플리케이션 환경 변수와 설정 등 점검
- **데이터베이스 도구** - 데이터베이스 스키마 점검, 읽기 전용 쿼리 실행, 데이터 구조 파악까지 대화 내에서 해결
- **라우트 점검** - 등록된 전체 라우트 목록, 연결된 미들웨어, 컨트롤러, 인수까지 상세 확인
- **Artisan 명령어** - 사용 가능한 Artisan 명령어와 인수 확인, 작업에 적합한 명령어 추천 및 실행 가능
- **로그 분석** - 애플리케이션 로그 파일을 읽어 문제 해결을 위한 분석 지원
- **브라우저 로그** - Laravel 프런트엔드 도구와 함께 개발할 때 브라우저 콘솔 로그 및 에러 확인
- **Tinker 통합** - Laravel Tinker를 통해 애플리케이션 맥락에서 PHP 코드 실행, 가설 검증 및 동작 확인 지원
- **문서 검색** - 설치된 패키지 버전에 맞춰 결과를 제공하는, Laravel 생태계 문서 검색 지원

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인 (AI Guidelines)

Boost에는 Laravel 생태계 전용으로 전략적으로 설계된 AI 가이드라인이 포함되어 있습니다. 이 가이드라인들은 AI 에이전트에게 관용적인 Laravel 코드 작성법, 프레임워크 관습 준수, 그리고 흔히 발생하는 실수 예방 법을 가르칩니다. 각 가이드라인은 조합해서 사용할 수 있고, 버전에 따라 맞춤 안내가 제공되므로 여러분의 패키지 버전에 딱 맞는 지침이 인식됩니다.

Laravel 자체와 16개 이상의 인기 패키지(Laravel 생태계)용 가이드라인이 지원됩니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Vue 변형)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 그 외 다수

</div>

`boost:install`을 실행하면 Boost가 여러분 애플리케이션에서 사용하는 패키지를 자동 탐지하여, 해당하는 가이드라인을 프로젝트의 AI 컨텍스트 파일에 자동으로 포함합니다.

<a name="agent-skills"></a>
### 에이전트 스킬 (Agent Skills)

[Agent Skills](https://agentskills.io/home)는 특정 도메인에 맞춰 AI 에이전트가 필요할 때 바로 활성화할 수 있는 가볍고 타겟팅된 지식 모듈입니다. 가이드라인이 미리 로드되는 것과 달리, 스킬은 실제로 필요할 때만 로드되기 때문에, 컨텍스트가 불필요하게 커지는 것을 막으면서 더 적합한 AI 코드 생성을 유도할 수 있습니다.

이 스킬은 Livewire, Inertia, Tailwind CSS, Pest 등 인기 Laravel 패키지용으로 제공됩니다. `boost:install`을 실행하고 스킬 기능을 선택하면, `composer.json`에서 감지된 패키지에 맞춰 필요한 스킬이 자동으로 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색 (Documentation Search)

Boost는 17,000개 이상의 Laravel 생태계 공식 문서에 접근할 수 있는 강력한 문서 API를 제공합니다. 일반적인 웹 검색과 달리, 이 문서 API는 인덱싱, 벡터화, 그리고 여러분의 패키지 버전에 맞춰 필터링된 정보를 제공합니다.

에이전트가 특정 기능의 동작 원리를 파악해야 할 때 Boost의 문서 API에 질의하면, 정확하고 버전에 맞는 정보를 제공받을 수 있습니다. 이를 통해 에이전트가 이미 폐기된 오래된 방식이나 문법의 코드를 제안하는 문제를 근본적으로 해결합니다.

<a name="agents-integration"></a>
### 에이전트 통합 (Agents Integration)

Boost는 Model Context Protocol을 지원하는 인기 IDE 및 AI 도구들과 통합할 수 있습니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie 등의 상세 설정 방법은 Boost 문서의 [에이전트 설정](/docs/12.x/boost#set-up-your-agents) 섹션을 참고하시기 바랍니다.
