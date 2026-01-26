# Laravel Boost (Laravel Boost)

- [소개](#introduction)
- [설치](#installation)
    - [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated)
    - [에이전트 설정](#set-up-your-agents)
- [MCP 서버](#mcp-server)
    - [사용 가능한 MCP 도구](#available-mcp-tools)
    - [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 가이드라인](#ai-guidelines)
    - [사용 가능한 AI 가이드라인](#available-ai-guidelines)
    - [커스텀 AI 가이드라인 추가](#adding-custom-ai-guidelines)
    - [Boost AI 가이드라인 재정의](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [커스텀 스킬](#custom-skills)
    - [스킬 재정의](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인과 스킬의 차이](#guidelines-vs-skills)
- [문서 API](#documentation-api)
- [Boost 확장하기](#extending-boost)
    - [기타 IDE/AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개

Laravel Boost는 AI 지원 개발을 가속화하는 도구로, AI 에이전트가 Laravel 베스트 프랙티스에 부합하는 고품질의 Laravel 애플리케이션을 작성할 수 있도록 꼭 필요한 가이드라인과 에이전트 스킬을 제공합니다.

Boost는 또한 내장 MCP 툴과 17,000개가 넘는 Laravel 특화 정보가 담긴 방대한 지식베이스를 결합하여, 임베딩을 활용한 시맨틱 검색 기능으로 매우 정확하고 문맥에 맞는 결과를 제공하는 강력한 Laravel 생태계 문서 API도 포함합니다. Boost는 Claude Code, Cursor와 같은 AI 에이전트에게 이 API를 활용하여 최신 Laravel 기능 및 베스트 프랙티스 정보를 학습하도록 안내합니다.

<a name="installation"></a>
## 설치

Laravel Boost는 Composer로 설치할 수 있습니다:

```shell
composer require laravel/boost --dev
```

다음으로, MCP 서버와 코딩 가이드라인을 설치합니다:

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정 중에 선택한 코딩 에이전트에 필요한 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost 설치가 완료되면, Cursor, Claude Code 또는 원하는 AI 에이전트로 코드를 작성할 준비가 된 것입니다.

> [!NOTE]
> 설치 시 생성되는 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 설정 파일은 애플리케이션의 `.gitignore`에 추가해도 무방합니다. 이 파일들은 `boost:install` 또는 `boost:update` 명령 실행 시 자동으로 재생성됩니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정

#### Cursor

1. 커맨드 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "/open MCP Settings"에서 `enter` 입력
3. `laravel-boost` 토글을 켜기

#### Claude Code

Claude Code 지원은 일반적으로 자동 활성화됩니다. 만약 활성화되지 않았다면, 프로젝트 디렉터리에서 셸을 열고 아래 명령어를 실행하세요:

```shell
claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

#### Codex

Codex 역시 일반적으로 자동 지원됩니다. 활성화되지 않았다면, 프로젝트 디렉터리에서 셸을 열고 아래 명령어를 입력하세요:

```shell
codex mcp add -- php artisan boost:mcp
```

#### Gemini CLI

Gemini CLI도 일반적으로 자동 지원됩니다. 필요한 경우, 프로젝트 디렉터리에서 셸을 열고 다음 명령어를 실행하세요:

```shell
gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

#### GitHub Copilot (VS Code)

1. 커맨드 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "MCP: List Servers"에서 `enter` 입력
3. `laravel-boost`로 이동한 뒤 `enter` 입력
4. "Start server" 선택

#### Junie

1. Shift 두 번 눌러 커맨드 팔레트 열기
2. "MCP Settings"를 검색해 `enter` 입력
3. `laravel-boost` 옆 체크박스 선택
4. 우측 하단 "Apply" 클릭

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 최신 상태 유지

AI 가이드라인 및 스킬과 같이 Boost에서 제공하는 리소스가 프로젝트에 최신 Laravel 생태계 패키지 및 버전 정보를 반영하도록 주기적으로 업데이트하는 것이 좋습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

또한, Composer의 "post-update-cmd" 스크립트에 아래와 같이 추가하여 이 프로세스를 자동화할 수 있습니다:

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```

<a name="mcp-server"></a>
## MCP 서버

Laravel Boost는 MCP(Model Context Protocol) 서버를 제공하여, AI 에이전트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있도록 도구를 노출합니다. 이를 통해 에이전트는 애플리케이션의 구조를 탐색하거나 데이터베이스를 조회하고, 코드를 실행하는 등 다양한 작업이 가능합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                         | 설명                                                                                                           |
|------------------------------|--------------------------------------------------------------------------------------------------------------|
| Application Info             | PHP 및 Laravel 버전, 데이터베이스 엔진, 생태계 패키지 목록(버전 포함), Eloquent 모델 조회                      |
| Browser Logs                 | 브라우저에서 발생한 로그 및 오류 읽기                                                                         |
| Database Connections         | 사용 가능한 데이터베이스 연결, 기본 연결 등 확인                                                              |
| Database Query               | 데이터베이스에 직접 쿼리 실행                                                                                 |
| Database Schema              | 데이터베이스 스키마 정보 읽기                                                                                 |
| Get Absolute URL             | 상대 경로 URI를 절대 URL로 변환하여 에이전트가 유효한 URL을 생성할 수 있도록 지원                              |
| Get Config                   | "dot" 표기법을 사용하여 설정 파일에서 값 가져오기                                                            |
| Last Error                   | 애플리케이션 로그 파일에서 마지막 오류 읽기                                                                   |
| List Artisan Commands        | 사용 가능한 Artisan 명령어 목록 조회                                                                          |
| List Available Config Keys   | 사용 가능한 설정 키 목록 확인                                                                                 |
| List Available Env Vars      | 사용 가능한 환경 변수 키 목록 확인                                                                            |
| List Routes                  | 애플리케이션의 라우트 목록 조회                                                                              |
| Read Log Entries             | 최근 N개의 로그 엔트리 읽기                                                                                   |
| Search Docs                  | Laravel 공식 문서 API 서비스 조회 및 설치된 패키지에 맞는 문서 검색                                            |
| Tinker                       | 애플리케이션 컨텍스트 내에서 임의의 코드 실행                                                                 |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

특정 편집기에서 Laravel Boost MCP 서버를 수동으로 등록해야 할 수도 있습니다. MCP 서버는 아래 정보로 등록 가능합니다:

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

JSON 예시:

```json
{
    "mcpServers": {
        "laravel-boost": {
            "command": "php",
            "args": ["artisan", "boost:mcp"]
        }
    }
}
```

<a name="ai-guidelines"></a>
## AI 가이드라인

AI 가이드라인은 AI 에이전트에 Laravel 생태계 패키지에 대한 중요한 정보를 미리 제공하는 조합형 지침 파일입니다. 이 가이드라인에는 핵심 규칙, 베스트 프랙티스, 프레임워크별 패턴 등이 담겨 있으므로, 에이전트가 일관성 있고 우수한 품질의 코드를 생성할 수 있습니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인

Laravel Boost는 다음 패키지 및 프레임워크에 대한 AI 가이드라인을 포함합니다. `core` 가이드라인은 각 패키지에 대해 모든 버전에서 사용할 수 있는 일반화된 조언을 제공합니다.

| 패키지              | 지원 버전                |
|---------------------|-------------------------|
| Core & Boost        | core                    |
| Laravel Framework   | core, 10.x, 11.x, 12.x  |
| Livewire            | core, 2.x, 3.x, 4.x     |
| Flux UI             | core, free, pro         |
| Folio               | core                    |
| Herd                | core                    |
| Inertia Laravel     | core, 1.x, 2.x          |
| Inertia React       | core, 1.x, 2.x          |
| Inertia Vue         | core, 1.x, 2.x          |
| Inertia Svelte      | core, 1.x, 2.x          |
| MCP                 | core                    |
| Pennant             | core                    |
| Pest                | core, 3.x, 4.x          |
| PHPUnit             | core                    |
| Pint                | core                    |
| Sail                | core                    |
| Tailwind CSS        | core, 3.x, 4.x          |
| Livewire Volt       | core                    |
| Wayfinder           | core                    |
| Enforce Tests       | 조건부                   |

> **참고:** AI 가이드라인을 최신 상태로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 커스텀 AI 가이드라인 추가

직접 만든 AI 가이드라인을 Boost에 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install` 명령 실행 시 자동으로 Boost 가이드라인에 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 재정의

Boost 내장 AI 가이드라인을 본인만의 커스텀 가이드라인으로 대체하려면, 기존 Boost 가이드라인과 동일한 파일 경로에 커스텀 파일을 만들면 됩니다. 경로가 일치하는 커스텀 가이드라인을 만들면 Boost에서는 내장 버전 대신 커스텀 버전을 사용합니다.

예를 들어, "Inertia React v2 Form Guidance" 가이드라인을 재정의하려면, `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 생성하세요. `boost:install` 시 디폴트 대신 이 파일이 포함됩니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 가이드라인

직접 개발한 서드파티 패키지에서 Boost에 AI 가이드라인을 추가하고자 한다면, 패키지의 `resources/boost/guidelines/core.blade.php` 파일에 작성하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 이 가이드라인이 자동으로 적용됩니다.

AI 가이드라인에는 패키지 주요 기능 소개, 필요 파일구조/관례 설명, 그리고 주요 기능을 어떻게 구현/사용하는지(명령어나 코드 스니펫 예시) 등이 포함되어야 합니다. 간결하고 actionable하며, 베스트 프랙티스에 중점을 두어 AI가 올바른 코드를 생성할 수 있도록 안내하세요. 예시:

```php
## Package Name

This package provides [brief description of functionality].

### Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

<a name="agent-skills"></a>
## 에이전트 스킬

[Agent Skills](https://agentskills.io/home)는 특정 도메인 작업을 할 때 에이전트가 필요에 따라 활성화할 수 있는, 경량화된 지식 모듈입니다. 가이드라인이 사전에 전체적으로 로딩되는 것과 달리, 스킬은 실제 작업에 필요할 때만 불러와서 문맥 과부하를 줄이고 AI가 보다 정확하게 코드를 생성할 수 있게 합니다.

`boost:install`을 실행하고 스킬 기능을 선택하면, `composer.json`에서 감지된 패키지에 맞는 스킬이 자동 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 포함되면, `livewire-development` 스킬이 자동 설치됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬

| 스킬명                        | 패키지         |
|-------------------------------|---------------|
| fluxui-development            | Flux UI       |
| folio-routing                 | Folio         |
| inertia-react-development     | Inertia React |
| inertia-svelte-development    | Inertia Svelte|
| inertia-vue-development       | Inertia Vue   |
| livewire-development          | Livewire      |
| mcp-development               | MCP           |
| pennant-development           | Pennant       |
| pest-testing                  | Pest          |
| tailwindcss-development       | Tailwind CSS  |
| volt-development              | Volt          |
| wayfinder-development         | Wayfinder     |

> **참고:** 스킬도 최신 상태를 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="custom-skills"></a>
### 커스텀 스킬

직접 만든 커스텀 스킬을 추가하려면, 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 작성하세요. `boost:update` 명령 실행 시 커스텀 스킬도 Boost 내장 스킬과 함께 설치됩니다.

예시: 도메인 로직용 커스텀 스킬 생성

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 재정의

Boost 내장 스킬을 커스텀 버전으로 덮어쓰려면, 기존 스킬과 이름이 동일한 커스텀 스킬을 생성하면 됩니다. 동일한 이름의 커스텀 스킬이 있으면 Boost는 내장 버전 대신 이를 사용합니다.

예를 들어, `livewire-development` 스킬을 재정의하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 만들고 `boost:update` 실행 시 이 파일이 적용됩니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

본인이 개발한 서드파티 패키지에 Boost 스킬을 포함시키려면, 패키지의 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행할 때 사용자 선택에 따라 스킬이 자동 설치됩니다.

Boost 스킬은 [Agent Skills 포맷](https://agentskills.io/what-are-skills)을 지원하며, 폴더 내에 YAML 프론트매터 및 마크다운 지침이 포함된 `SKILL.md` 파일로 구성되어야 합니다. `SKILL.md`에는 필수 프론트매터(`name`과 `description`)가 필요하며, 필요에 따라 스크립트, 템플릿, 레퍼런스 자료도 포함할 수 있습니다.

스킬은 필요한 파일 구조, 규칙, 주요 기능의 생성·사용법(명령이나 코드 예시 포함)을 설명해야 하며, 간결하고 actionable하게—그리고 베스트 프랙티스 중심으로 작성해야 AI가 올바른 코드를 생성할 수 있습니다:

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## When to use this skill
Use this skill when working with PackageName features...

## Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

$result = PackageName::featureTwo($param1, $param2);
```

<a name="guidelines-vs-skills"></a>
## 가이드라인과 스킬의 차이

Laravel Boost는 AI 에이전트에게 애플리케이션 정보를 제공하는 두 가지 방식을 지원합니다: **가이드라인**과 **스킬**입니다.

**가이드라인**은 에이전트가 시작될 때 미리 로딩되어, Laravel의 기본 규칙과 전반적 베스트 프랙티스를 코드 전반에 적용할 수 있도록 통합적 컨텍스트를 제공합니다.

**스킬**은 특정 작업에 필요할 때만 불러와져, Livewire 컴포넌트나 Pest 테스트 등 특정 도메인의 상세 규칙과 패턴을 제공합니다. 스킬을 작업에 따라 필요시만 로딩하면 전체 컨텍스트 부하를 줄이고 코드 품질을 높일 수 있습니다.

| 구분     | 가이드라인        | 스킬           |
|----------|------------------|----------------|
| **로딩 시점** | 시작 시 항상 적용    | 필요시 즉시 적용 |
| **범위**   | 전체, 기본적         | 좁고, 과업 맞춤형 |
| **목적**   | 규칙 및 베스트 프랙티스 | 상세 구현 패턴   |

<a name="documentation-api"></a>
## 문서 API

Laravel Boost는 17,000개 이상의 Laravel 특화 정보가 포함된 방대한 지식베이스에 AI 에이전트가 접근할 수 있도록 문서 API를 제공합니다. 이 API는 임베딩을 활용한 시맨틱 검색으로, 아주 정밀하고 문맥에 맞는 결과를 반환합니다.

`Search Docs` MCP 도구를 활용하면 에이전트가 Laravel 공식 문서 API 서비스에 쿼리를 보낼 수 있고, 설치된 패키지에 맞는 문서를 가져올 수 있습니다. Boost의 AI 가이드라인과 스킬은 코딩 에이전트에게 이 API를 활용하도록 자동 안내합니다.

| 패키지            | 지원 버전                  |
|-------------------|---------------------------|
| Laravel Framework | 10.x, 11.x, 12.x          |
| Filament          | 2.x, 3.x, 4.x, 5.x        |
| Flux UI           | 2.x Free, 2.x Pro         |
| Inertia           | 1.x, 2.x                  |
| Livewire          | 1.x, 2.x, 3.x, 4.x        |
| Nova              | 4.x, 5.x                  |
| Pest              | 3.x, 4.x                  |
| Tailwind CSS      | 3.x, 4.x                  |

<a name="extending-boost"></a>
## Boost 확장하기

Boost는 대표적인 IDE와 많은 AI 에이전트와 기본적으로 잘 작동합니다. 만약 여러분이 사용하는 코딩 도구가 아직 공식 지원되지 않는다면, 직접 에이전트를 만들어 Boost에 연동할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 기타 IDE/AI 에이전트 지원 추가

새로운 IDE나 AI 에이전트를 지원하고 싶다면, `Laravel\Boost\Install\Agents\Agent`를 확장한 클래스를 만들고 목적에 따라 아래 계약(Contract) 중 하나 이상을 구현하면 됩니다:

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 가이드라인 지원 추가
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원 추가
- `Laravel\Boost\Contracts\SupportsSkills` - Agent Skills 지원 추가

<a name="writing-the-agent"></a>
#### 에이전트 작성 방법

```php
<?php

declare(strict_types=1);

namespace App;

use Laravel\Boost\Contracts\SupportsGuidelines;
use Laravel\Boost\Contracts\SupportsMcp;
use Laravel\Boost\Contracts\SupportsSkills;
use Laravel\Boost\Install\Agents\Agent;

class CustomAgent extends Agent implements SupportsGuidelines, SupportsMcp, SupportsSkills
{
    // Your implementation...
}
```

구현 예시는 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php) 파일을 참고하세요.

<a name="registering-the-agent"></a>
#### 에이전트 등록

애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 커스텀 에이전트를 등록하세요:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면, `php artisan boost:install` 실행 시 해당 에이전트를 선택할 수 있습니다.

