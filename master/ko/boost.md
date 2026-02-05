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
    - [Boost AI 가이드라인 오버라이드](#overriding-boost-ai-guidelines)
    - [서드파티 패키지용 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [커스텀 스킬](#custom-skills)
    - [스킬 오버라이드](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인 vs. 스킬](#guidelines-vs-skills)
- [문서 API](#documentation-api)
- [Boost 확장](#extending-boost)
    - [다른 IDE/AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개

Laravel Boost는 AI 에이전트가 Laravel 베스트 프랙티스를 따르면서 고품질의 Laravel 애플리케이션을 작성할 수 있도록 필수적인 가이드라인과 에이전트 스킬을 제공함으로써 AI 기반 개발을 가속화합니다.

Boost는 또한 1만 7천개 이상의 Laravel 특화 정보가 담긴 강력한 지식 기반과 임베딩 기반 의미론적 검색 기능을 결합한 내장 MCP 도구를 갖춘 Laravel 에코시스템 문서 API를 제공합니다. 이로 인해 AI 에이전트(예: Claude Code, Cursor 등)는 이 API를 활용해 최신 Laravel의 기능과 베스트 프랙티스를 빠르게 학습할 수 있습니다.

<a name="installation"></a>
## 설치

Laravel Boost는 Composer를 통해 설치할 수 있습니다:

```shell
composer require laravel/boost --dev
```

다음으로 MCP 서버와 코딩 가이드라인을 설치하세요:

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 가이드라인과 스킬 파일을 생성합니다.

설치가 완료되면, Cursor, Claude Code 또는 선호하는 AI 에이전트와 함께 코딩을 시작할 수 있습니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 설정 파일은 `.gitignore`에 추가해도 무방합니다. 이 파일들은 `boost:install` 및 `boost:update` 명령 실행 시 자동으로 재생성됩니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정

#### Cursor

1. 명령 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "/open MCP Settings"에서 enter 키 입력
3. `laravel-boost` 토글을 켜세요

#### Claude Code

Claude Code 지원은 일반적으로 자동으로 활성화됩니다. 만약 활성화되어 있지 않다면, 프로젝트 디렉터리에서 다음 명령을 실행하세요:

```shell
claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

#### Codex

Codex 지원 역시 대부분 자동으로 활성화됩니다. 만약 그렇지 않다면, 프로젝트 디렉터리에서 다음 명령을 실행하세요:

```shell
codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

#### Gemini CLI

Gemini CLI 지원은 대개 자동으로 활성화됩니다. 만약 활성화되지 않는다면, 다음 명령을 실행하세요:

```shell
gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

#### GitHub Copilot (VS Code)

1. 명령 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "MCP: List Servers"에서 enter 키 입력
3. `laravel-boost`로 이동 후 enter 키 입력
4. "Start server" 선택

#### Junie

1. shift 키를 두 번 눌러 명령 팔레트 열기
2. "MCP Settings"를 검색해 enter 키 입력
3. `laravel-boost` 옆 체크박스 선택
4. 오른쪽 아래 "Apply" 클릭

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 최신 상태 유지

설치한 Laravel 에코시스템 패키지의 최신 버전에 맞춰 Boost 리소스(AI 가이드라인과 스킬)를 주기적으로 업데이트하는 것이 좋습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

이 과정을 자동화하려면, Composer의 "post-update-cmd" 스크립트에 추가하면 됩니다:

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
## MCP 서버 (MCP Server)

Laravel Boost는 MCP(Model Context Protocol) 서버를 제공하여 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있는 다양한 도구를 활용할 수 있게 합니다. 이 도구들을 이용해 애플리케이션 구조를 검사하거나, 데이터베이스 쿼리를 실행하고, 코드를 실행하는 등 다양한 작업이 가능합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                        | 비고                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| Application Info           | PHP 및 Laravel 버전, 데이터베이스 엔진, 에코시스템 패키지와 버전, Eloquent 모델 목록 확인              |
| Browser Logs               | 브라우저에서 발생한 로그와 에러를 읽기                                                          |
| Database Connections       | 사용 가능한 데이터베이스 연결(기본 연결 포함) 검사                                               |
| Database Query             | 데이터베이스 쿼리 실행                                                                          |
| Database Schema            | 데이터베이스 스키마 읽기                                                                        |
| Get Absolute URL           | 상대 경로 URI를 절대 경로로 변환 (에이전트가 올바른 URL을 생성할 수 있게 함)                    |
| Get Config                 | "dot" 표기법을 사용하여 설정 파일 값 얻기                                                       |
| Last Error                 | 애플리케이션 로그 파일에서 마지막 에러 읽기                                                     |
| List Artisan Commands      | 사용 가능한 Artisan 명령어 확인                                                                 |
| List Available Config Keys | 사용 가능한 설정 키 목록 확인                                                                   |
| List Available Env Vars    | 사용 가능한 환경 변수 목록 확인                                                                 |
| List Routes                | 애플리케이션 라우트 목록 확인                                                                   |
| Read Log Entries           | 최근 N개의 로그 항목 읽기                                                                       |
| Search Docs                | 설치된 패키지에 따라 문서 API를 쿼리하여 문서 검색                                             |
| Tinker                     | 애플리케이션 컨텍스트에서 임의의 코드 실행                                                      |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

에디터에 따라 Laravel Boost MCP 서버를 수동으로 등록해야 할 수도 있습니다. MCP 서버 등록 시 다음 정보를 사용하세요:

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
## AI 가이드라인 (AI Guidelines)

AI 가이드라인은 AI 에이전트가 Laravel 에코시스템 패키지에 대해 필수적인 컨텍스트를 사전에 이해할 수 있도록 하는 지침 파일입니다. 이 가이드라인은 핵심 규약, 베스트 프랙티스, 프레임워크 특유의 패턴을 포함해 에이전트가 일관되고 수준 높은 코드를 생성하도록 돕습니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인

Laravel Boost에는 다음 패키지 및 프레임워크에 대한 AI 가이드라인이 포함되어 있습니다. `core` 가이드라인은 모든 버전에서 사용 가능한 일반적이고 넓은 범위의 지침을 제공합니다.

| 패키지               | 지원 버전                     |
| ------------------ | ---------------------------- |
| Core & Boost       | core                         |
| Laravel Framework  | core, 10.x, 11.x, 12.x       |
| Livewire           | core, 2.x, 3.x, 4.x          |
| Flux UI            | core, free, pro              |
| Folio              | core                         |
| Herd               | core                         |
| Inertia Laravel    | core, 1.x, 2.x               |
| Inertia React      | core, 1.x, 2.x               |
| Inertia Vue        | core, 1.x, 2.x               |
| Inertia Svelte     | core, 1.x, 2.x               |
| MCP                | core                         |
| Pennant            | core                         |
| Pest               | core, 3.x, 4.x               |
| PHPUnit            | core                         |
| Pint               | core                         |
| Sail               | core                         |
| Tailwind CSS       | core, 3.x, 4.x               |
| Livewire Volt      | core                         |
| Wayfinder          | core                         |
| Enforce Tests      | 조건부                        |

> **참고:** AI 가이드라인을 최신 상태로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 커스텀 AI 가이드라인 추가

자신만의 커스텀 AI 가이드라인을 Laravel Boost에 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install` 실행 시 자동으로 Boost 가이드라인과 함께 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 오버라이드

Boost의 내장 AI 가이드라인과 동일한 경로에 커스텀 가이드라인 파일을 추가해 오버라이드할 수 있습니다. 경로가 일치하는 커스텀 가이드라인이 존재하면, Boost는 내장 가이드라인 대신 해당 파일을 사용합니다.

예를 들어, Boost의 "Inertia React v2 Form Guidance" 가이드라인을 오버라이드하려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 생성하세요. 이후 `boost:install`을 실행하면 커스텀 가이드라인이 포함됩니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지용 AI 가이드라인

서드파티 패키지를 유지 관리하고 있고 Boost에 대한 AI 가이드라인을 제공하고 싶다면, 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하세요. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 해당 가이드라인을 자동으로 불러옵니다.

AI 가이드라인은 패키지에 대한 짧은 개요, 필요한 파일 구조 및 관례, 주요 기능 사용 방법(명령어/코드 예시 포함)을 안내해야 합니다. 내용은 간결하며, 실용적이고, 베스트 프랙티스에 집중해야 AI가 올바른 코드를 생성할 수 있습니다. 예시는 아래와 같습니다:

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
## 에이전트 스킬 (Agent Skills)

[Agent Skills](https://agentskills.io/home)는 특정 분야에 대해 에이전트가 필요할 때만 활성화되는 경량화된 지식 모듈입니다. 가이드라인은 사전에 로딩되고 항상 유지되는 반면, 스킬은 필요한 순간에만 세부적인 패턴과 베스트 프랙티스를 로드해 컨텍스트 오염을 줄이고 AI가 더 관련성 높은 코드를 생성하도록 돕습니다.

`boost:install` 실행 시 스킬이 기능으로 선택되면, 프로젝트의 `composer.json`에서 감지된 패키지에 따라 스킬이 자동 설치됩니다. 예를 들어, 프로젝트에 `livewire/livewire`가 있으면 `livewire-development` 스킬이 자동으로 설치됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬

| 스킬                        | 관련 패키지      |
| -------------------------- | -------------- |
| fluxui-development         | Flux UI        |
| folio-routing              | Folio          |
| inertia-react-development  | Inertia React  |
| inertia-svelte-development | Inertia Svelte |
| inertia-vue-development    | Inertia Vue    |
| livewire-development       | Livewire       |
| mcp-development            | MCP            |
| pennant-development        | Pennant        |
| pest-testing               | Pest           |
| tailwindcss-development    | Tailwind CSS   |
| volt-development           | Volt           |
| wayfinder-development      | Wayfinder      |

> **참고:** 스킬을 최신 상태로 유지하는 방법은 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated)를 참고하세요.

<a name="custom-skills"></a>
### 커스텀 스킬

직접 커스텀 스킬을 만들고 싶다면, `.ai/skills/{skill-name}/` 경로에 `SKILL.md` 파일을 추가하세요. 이후 `boost:update` 명령으로 커스텀 스킬이 Boost 내장 스킬과 함께 설치됩니다.

예시로, 도메인 로직에 대한 커스텀 스킬을 만들려면 다음과 같이 디렉터리를 구성합니다:

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 오버라이드

Boost의 내장 스킬과 동일한 이름으로 커스텀 스킬을 작성할 수 있습니다. 동일한 이름의 커스텀 스킬이 있으면, Boost는 내장 스킬 대신 해당 스킬을 사용합니다.

예를 들어, Boost의 `livewire-development` 스킬을 오버라이드하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 생성하세요. 이후 `boost:update`를 실행하면 커스텀 스킬이 적용됩니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

서드파티 패키지를 유지 관리하고 있으며, Boost 스킬을 포함하길 원한다면, 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하세요. 패키지 사용자가 `php artisan boost:install`을 실행할 때 Boost가 사용자 선택에 따라 해당 스킬을 자동으로 설치합니다.

Boost 스킬은 [Agent Skills 포맷](https://agentskills.io/what-are-skills)을 지원하며, `SKILL.md` 파일에 YAML frontmatter 및 마크다운 지침이 담긴 폴더 구조를 따라야 합니다. `SKILL.md`에는 필수 frontmatter(`name`과 `description`)가 있어야 하며, 스크립트, 템플릿, 참조 자료도 포함할 수 있습니다.

스킬에는 필요한 파일 구조, 관례, 주요 기능의 사용법(명령어나 코드 예시 등)을 간결하고 실용적으로 설명해야 합니다. 예시는 아래와 같습니다:

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
## 가이드라인 vs. 스킬

Laravel Boost는 애플리케이션에 대한 컨텍스트 제공 방식을 **가이드라인**과 **스킬**로 명확히 구분합니다.

**가이드라인**은 AI 에이전트가 시작할 때 사전에 로딩되어, Laravel의 규약과 전반적인 베스트 프랙티스를 안내합니다.

**스킬**은 특정 작업이나 상황에서 필요할 때만 활성화되어, 도메인(예: Livewire 컴포넌트, Pest 테스트 등)별로 세부적인 구현 패턴을 담고 있습니다. 스킬을 필요할 때만 로드하면 컨텍스트 오염이 줄고 코드 품질이 향상됩니다.

| 구분        | 가이드라인                           | 스킬                                 |
| ----------- | ---------------------------------- | ------------------------------------ |
| **로딩 시점** | 시작 시 항상 로딩                     | 필요 시, 작업에 따라 동적으로 로딩      |
| **범위**      | 넓고, 전반적인                        | 좁고, 작업/도메인 특화                 |
| **목적**      | 핵심 규약, 베스트 프랙티스             | 세부적인 구현 패턴                    |

<a name="documentation-api"></a>
## 문서 API (Documentation API)

Laravel Boost는 AI 에이전트가 1만 7천개 이상의 Laravel 특화 정보가 담긴 방대한 지식 베이스에 접근할 수 있도록 문서 API를 제공합니다. 해당 API는 임베딩 기반 의미론적 검색을 활용하여 정확하고 상황에 맞는 결과를 제공합니다.

`Search Docs` MCP 도구는 설치된 패키지에 따라 Laravel 공식 문서 API 서비스를 쿼리할 수 있도록 하며, Boost의 AI 가이드라인과 스킬은 코딩 에이전트가 이 API를 사용할 수 있도록 자동으로 안내합니다.

| 패키지               | 지원 버전                   |
| ------------------ | ------------------------ |
| Laravel Framework  | 10.x, 11.x, 12.x         |
| Filament           | 2.x, 3.x, 4.x, 5.x       |
| Flux UI            | 2.x Free, 2.x Pro        |
| Inertia            | 1.x, 2.x                 |
| Livewire           | 1.x, 2.x, 3.x, 4.x       |
| Nova               | 4.x, 5.x                 |
| Pest               | 3.x, 4.x                 |
| Tailwind CSS       | 3.x, 4.x                 |

<a name="extending-boost"></a>
## Boost 확장 (Extending Boost)

Boost는 많은 인기 IDE 및 AI 에이전트와 기본적으로 작동합니다. 만약 사용 중인 코딩 도구가 아직 지원되지 않는다면, 자신만의 에이전트를 만들어 Boost와 연동할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE/AI 에이전트 지원 추가

새로운 IDE나 AI 에이전트 지원을 추가하려면, `Laravel\Boost\Install\Agents\Agent`를 확장하는 클래스를 만들고 다음 중 필요한 계약을 구현하세요:

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 가이드라인 지원 추가
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원 추가
- `Laravel\Boost\Contracts\SupportsSkills` - 에이전트 스킬 지원 추가

<a name="writing-the-agent"></a>
#### 에이전트 작성 예시

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

구현 예시는 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)를 참고하세요.

<a name="registering-the-agent"></a>
#### 에이전트 등록

애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 직접 커스텀 에이전트를 등록하세요:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

에이전트가 등록되면 `php artisan boost:install` 실행 시 선택 항목으로 나타납니다.
