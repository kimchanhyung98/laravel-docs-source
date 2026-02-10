# AI 지원 개발 (AI Assisted Development)

- [소개](#introduction)
    - [AI 개발에 왜 Laravel인가?](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [설치](#installation)
    - [사용 가능한 도구](#available-tools)
    - [AI 가이드라인](#ai-guidelines)
    - [에이전트 스킬](#agent-skills)
    - [문서 검색](#documentation-search)
    - [에이전트 통합](#agents-integration)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 및 에이전트 기반 개발에 가장 적합한 프레임워크로 독보적인 위치를 차지하고 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장으로 개발자가 코드를 작성하는 방식이 크게 변화하였습니다. 이러한 도구들은 전체 기능을 자동 생성하거나, 복잡한 문제를 디버그하고, 코드 리팩터링을 놀라울 정도로 빠르고 쉽게 수행할 수 있습니다. 하지만 이 도구들의 효과는 여러분의 코드베이스를 얼마나 잘 이해하느냐에 크게 달려 있습니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 왜 Laravel인가?

Laravel은 명확하게 정의된 구조와 강력한 관례를 가지고 있어 AI 지원 개발에 이상적인 프레임워크입니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가해달라고 요청하면, 어디에 파일을 생성해야 할지 정확하게 알 수 있습니다. 새로운 마이그레이션을 추가할 때도, 이름 규칙과 파일 위치가 예측 가능합니다. 이러한 일관성 덕분에, 다른 프레임워크들처럼 유동적이지 않아 생길 수 있는 혼란이 줄어듭니다.

파일 구조 이상의 장점도 있습니다. Laravel의 표현력 있는 문법과 방대한 공식 문서는 AI 에이전트가 정확하고 Laravel다운 코드를 만들기 위한 충분한 맥락을 제공합니다. 예를 들어 Eloquent 연관관계, 폼 리퀘스트, 미들웨어 등은 모두 예측 가능한 패턴을 따릅니다. 결과적으로, AI가 생성한 코드는 경험 많은 Laravel 개발자가 작성한 것처럼 보이며, 단순 PHP 조각을 연결한 수준에서 벗어납니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 여러분의 Laravel 애플리케이션 사이의 격차를 메워주는 도구입니다. Boost는 15가지 이상의 특화 도구를 갖춘 MCP(Model Context Protocol) 서버로, AI 에이전트가 애플리케이션의 구조, 데이터베이스, 라우트 등 다양한 정보를 깊이 파악할 수 있도록 지원합니다. Boost를 설치하면, AI 에이전트는 범용 코드 어시스턴트에서 여러분의 Laravel 애플리케이션을 이해하는 전문가로 변신합니다.

Boost는 세 가지 주요 기능을 제공합니다. 애플리케이션을 점검하고 상호작용할 수 있는 MCP 도구 모음, Laravel 생태계에 맞춰 설계된 조합형 AI 가이드라인, 그리고 17,000개가 넘는 Laravel 관련 지식을 담은 강력한 문서 API입니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상이 실행되는 Laravel 10, 11, 12 버전에서 설치할 수 있습니다. 다음과 같이 개발 의존성으로 Boost를 설치해 시작할 수 있습니다.

```shell
composer require laravel/boost --dev
```

설치가 완료되면, 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

이 설치 프로그램은 여러분의 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 통합 도구를 선택할 수 있도록 안내합니다. Boost는 MCP 호환 에디터를 위한 `.mcp.json`과 AI 컨텍스트용 가이드라인 파일 등 필요한 설정 파일을 생성합니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json` 등과 같은 생성된 설정 파일은 각 개발자가 직접 환경을 구성하기 원한다면 `.gitignore`에 안전하게 추가할 수 있습니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에 다양한 도구를 제공합니다. 이 도구들은 에이전트가 여러분의 Laravel 애플리케이션을 심층적으로 이해하고 상호작용할 수 있도록 돕습니다.

<div class="content-list" markdown="1">

- **애플리케이션 점검** - PHP 및 Laravel 버전 조회, 설치된 패키지 목록, 설정과 환경 변수 확인 등 애플리케이션 정보를 조회할 수 있습니다.
- **데이터베이스 도구** - 데이터베이스 스키마를 점검하거나, 읽기 전용 쿼리를 실행하고, 데이터 구조를 쉽게 파악할 수 있습니다.
- **라우트 점검** - 모든 등록된 라우트 및 관련 미들웨어, 컨트롤러, 파라미터 정보를 열람할 수 있습니다.
- **Artisan 명령어** - 사용 가능한 Artisan 명령어와 인수를 조회하여, 에이전트가 적절한 명령어를 제안하거나 실행할 수 있게 합니다.
- **로그 분석** - 애플리케이션 로그 파일을 읽고 분석하여 오류를 신속하게 디버그할 수 있습니다.
- **브라우저 로그** - Laravel의 프런트엔드 도구로 개발할 때, 브라우저 콘솔 로그 및 오류에도 접근할 수 있습니다.
- **Tinker 연동** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드를 실행하면서, 에이전트가 가설을 검증하거나 동작을 확인할 수 있습니다.
- **문서 검색** - 설치된 패키지 버전에 맞춘 결과로, Laravel 생태계의 공식 문서를 빠르게 검색할 수 있습니다.

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost는 Laravel 생태계에 최적화된 포괄적인 AI 가이드라인을 포함하고 있습니다. 이 가이드라인은 AI 에이전트에게 Laravel다운 코드 스타일, 프레임워크의 규칙, 자주 발생하는 실수 피하기 등 다양한 노하우를 전달합니다. 모든 가이드라인은 패키지 버전에 맞춰 조합되고 적용되므로, 사용 중인 패키지 환경에 딱 맞는 지침을 제공합니다.

가이드라인은 Laravel 자체뿐만 아니라, 생태계 주요 패키지 16개 이상에 대해 준비되어 있습니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React 및 Vue 버전)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 그 외 다수

</div>

`boost:install`을 실행하면 Boost가 여러분의 애플리케이션에 설치된 패키지를 자동으로 감지하여, 관련 가이드라인을 AI 컨텍스트 파일에 자동으로 조합합니다.

<a name="agent-skills"></a>
### 에이전트 스킬

[Agent Skills](https://agentskills.io/home)는 특별한 도메인 작업을 할 때 에이전트가 필요에 따라 활성화할 수 있는, 경량화되고 목표가 명확한 지식 모듈입니다. 가이드라인이 처음부터 모두 불러와지는 것과 달리, 스킬은 상황에 따라 필요한 패턴과 권장 사례만 로드하므로, 맥락 정보가 넘쳐나서 코드를 흐리게 하는 현상을 줄이고 AI가 생성하는 코드의 정확도와 관련성을 높입니다.

스킬은 Livewire, Inertia, Tailwind CSS, Pest 등 인기 있는 Laravel 패키지에 대해 제공됩니다. `boost:install` 시 스킬 기능을 선택하면 `composer.json`에서 감지된 패키지에 맞춰 관련 스킬이 자동으로 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색

Boost는 AI 에이전트가 17,000개 이상의 Laravel 생태계 공식 문서에 즉각 접근할 수 있도록 강력한 문서 API를 제공합니다. 기존의 웹 검색과는 달리, 이 문서는 여러분의 설치된 패키지 버전에 따라 인덱싱, 벡터화, 필터링하여 제공합니다.

에이전트가 특정 기능 동작을 정확히 파악해야 할 때, Boost의 문서 API를 통해 검색이 가능하며, 설치된 버전에 꼭 맞는 최신 정보를 제공합니다. 덕분에 AI가 예전 버전의 문법이나 폐기된 메서드를 추천하는 실수를 줄일 수 있습니다.

<a name="agent-integration"></a>
### 에이전트 통합

Boost는 Model Context Protocol을 지원하는 다양한 IDE 및 AI 도구와 연동할 수 있습니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie 등과의 상세 설정 방법은 Boost 공식 문서의 [에이전트 설정하기](/docs/master/boost#set-up-your-agents) 섹션을 참고하시기 바랍니다.
