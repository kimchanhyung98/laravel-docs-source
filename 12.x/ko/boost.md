# Laravel Boost (Laravel Boost)

- [소개](#introduction)
- [설치](#installation)
    - [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated)
    - [에이전트 설정하기](#set-up-your-agents)
- [MCP 서버](#mcp-server)
    - [사용 가능한 MCP 도구](#available-mcp-tools)
    - [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 가이드라인](#ai-guidelines)
    - [사용 가능한 AI 가이드라인](#available-ai-guidelines)
    - [사용자 정의 AI 가이드라인 추가하기](#adding-custom-ai-guidelines)
    - [Boost AI 가이드라인 오버라이드](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [사용자 정의 스킬](#custom-skills)
    - [스킬 오버라이드](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인과 스킬의 차이](#guidelines-vs-skills)
- [문서화 API](#documentation-api)
- [Boost 확장하기](#extending-boost)
    - [다른 IDE/AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개

Laravel Boost는 AI 에이전트가 Laravel 모범 사례에 부합하는 고품질의 Laravel 애플리케이션을 작성할 수 있도록 돕는 필수 가이드라인과 에이전트 스킬을 제공하여 AI 기반 개발을 가속화합니다.

Boost는 또한 내장 MCP 도구와 17,000개 이상의 Laravel 특화 지식이 포함된 방대한 지식 베이스, 의미 검색(임베딩 기반)으로 강화된 강력한 Laravel 에코시스템 문서화 API를 제공합니다. Boost는 Claude Code, Cursor와 같은 AI 에이전트에게 이 API 활용법을 안내하여 최신 Laravel 기능 및 모범 사례를 학습할 수 있도록 지원합니다.

<a name="installation"></a>
## 설치

Laravel Boost는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/boost --dev
```

다음으로, MCP 서버와 코딩 가이드라인을 설치합니다.

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 에이전트 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost 설치가 완료되면, Cursor, Claude Code 또는 원하는 AI 에이전트와 함께 코딩을 바로 시작할 수 있습니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 설정 파일은 `.gitignore`에 추가해도 됩니다. 이 파일들은 `boost:install` 및 `boost:update` 실행 시 자동으로 다시 생성됩니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정하기

#### Cursor

1. 명령 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "/open MCP Settings"를 선택하고 `enter` 키 누르기
3. `laravel-boost` 토글을 켜기

#### Claude Code

Claude Code 지원은 보통 자동으로 활성화됩니다. 만약 활성화되지 않은 경우, 프로젝트 디렉터리에서 다음 명령어를 실행하세요.

```shell
claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

#### Codex

Codex 지원도 일반적으로 자동 활성화됩니다. 그렇지 않다면, 프로젝트 디렉터리에서 다음 명령어를 실행하세요.

```shell
codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

#### Gemini CLI

Gemini CLI도 기본적으로 지원됩니다. 비활성화된 경우, 프로젝트 디렉터리에서 다음 명령어를 실행하세요.

```shell
gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

#### GitHub Copilot (VS Code)

1. 명령 팔레트 열기 (`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)
2. "MCP: List Servers" 선택 후 `enter` 키 누르기
3. `laravel-boost`로 이동해 `enter` 누르기
4. "Start server" 선택

#### Junie

1. shift 키를 두 번 눌러 명령 팔레트 열기
2. "MCP Settings" 검색 후 `enter` 누르기
3. `laravel-boost` 옆 체크박스 선택
4. 우측 하단의 "Apply" 클릭

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 최신 상태로 유지하기

설치된 Laravel 에코시스템 패키지의 최신 버전을 반영하기 위해 주기적으로 Boost 리소스(AI 가이드라인과 스킬)를 업데이트하는 것이 좋습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

이 명령을 Composer의 "post-update-cmd" 스크립트에 추가하여 자동화할 수도 있습니다.

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

Laravel Boost는 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있는 MCP(Model Context Protocol) 서버를 제공합니다. 이 MCP 도구들은 애플리케이션 구조 탐색, 데이터베이스 질의 및 실행, 코드 실행 등 다양한 기능을 제공합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                       | 설명                                                                                                    |
|----------------------------|--------------------------------------------------------------------------------------------------------|
| Application Info           | PHP & Laravel 버전, 데이터베이스 엔진, 사용 중인 에코시스템 패키지 및 버전, Eloquent 모델 목록 조회         |
| Browser Logs               | 브라우저에서 발생한 로그와 에러 조회                                                                    |
| Database Connections       | 사용 가능한 데이터베이스 연결(기본 연결 포함) 확인                                                       |
| Database Query             | 데이터베이스에 쿼리 실행                                                                                 |
| Database Schema            | 데이터베이스 스키마 조회                                                                                 |
| Get Absolute URL           | 상대 URI를 절대 경로로 변환해 올바른 URL 생성                                                             |
| Get Config                 | "dot" 표기법으로 설정 파일에서 값 조회                                                                   |
| Last Error                 | 애플리케이션 로그에서 마지막 에러 조회                                                                   |
| List Artisan Commands      | 사용 가능한 Artisan 명령어 목록 확인                                                                     |
| List Available Config Keys | 사용 가능한 설정 키 목록 확인                                                                            |
| List Available Env Vars    | 사용 가능한 환경 변수 키 목록 확인                                                                       |
| List Routes                | 애플리케이션의 라우트 목록 확인                                                                          |
| Read Log Entries           | 최근 N개의 로그 엔트리 조회                                                                              |
| Search Docs                | 설치된 패키지에 따라 Laravel 공식 문서 API 서비스에 질의하여 문서 검색                                    |
| Tinker                     | 애플리케이션 컨텍스트 내에서 임의의 코드 실행                                                            |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

특정 에디터에서 Laravel Boost MCP 서버를 직접 등록해야 할 때가 있습니다. MCP 서버는 아래 정보를 이용해 등록할 수 있습니다.

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

AI 가이드라인은 AI 에이전트가 Laravel 에코시스템 패키지에 대한 핵심 문맥과 정보를 빠르게 이해할 수 있도록 하는, 조합 가능한(Composable) 명령 파일입니다. 이러한 가이드라인은 코딩 일관성, 모범 사례, 프레임워크별 패턴 정보를 담고 있어, 에이전트가 더 신뢰도 높은 코드를 생성할 수 있도록 돕습니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인

Laravel Boost에는 아래와 같은 패키지 및 프레임워크별 AI 가이드라인이 포함되어 있습니다. `core` 가이드라인은 각 패키지에서 모든 버전에 공통적으로 적용할 수 있는 일반적 조언을 제공합니다.

| 패키지             | 지원 버전                 |
|--------------------|--------------------------|
| Core & Boost       | core                     |
| Laravel Framework  | core, 10.x, 11.x, 12.x   |
| Livewire           | core, 2.x, 3.x, 4.x      |
| Flux UI            | core, free, pro          |
| Folio              | core                     |
| Herd               | core                     |
| Inertia Laravel    | core, 1.x, 2.x           |
| Inertia React      | core, 1.x, 2.x           |
| Inertia Vue        | core, 1.x, 2.x           |
| Inertia Svelte     | core, 1.x, 2.x           |
| MCP                | core                     |
| Pennant            | core                     |
| Pest               | core, 3.x, 4.x           |
| PHPUnit            | core                     |
| Pint               | core                     |
| Sail               | core                     |
| Tailwind CSS       | core, 3.x, 4.x           |
| Livewire Volt      | core                     |
| Wayfinder          | core                     |
| Enforce Tests      | conditional              |

> **참고:** AI 가이드라인을 항상 최신 상태로 유지하려면 [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 사용자 정의 AI 가이드라인 추가하기

직접 만든 AI 가이드라인을 Laravel Boost에 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. `boost:install` 실행 시 이 파일들이 자동으로 Boost 가이드라인과 함께 적용됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 오버라이드

Boost 내장 AI 가이드라인은 파일 경로가 일치하는 사용자 정의 가이드라인을 만들어 오버라이드할 수 있습니다. 파일 경로가 Boost 가이드라인과 같으면, Boost는 내장 가이드라인 대신 해당 사용자 버전을 사용합니다.

예를 들어, Boost의 "Inertia React v2 Form Guidance"를 오버라이드하고 싶다면, `.ai/guidelines/inertia-react/2/forms.blade.php`에 파일을 생성하면 됩니다. `boost:install` 실행 시 커스텀 가이드라인이 대신 포함됩니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 가이드라인

서드파티 패키지를 직접 개발 중이라면 Boost가 이를 위한 AI 가이드라인을 포함하도록 할 수 있습니다. 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행할 때 Boost가 해당 가이드라인을 자동으로 불러옵니다.

AI 가이드라인에는 패키지의 간략한 개요, 필요 파일 구조 및 관례, 주요 기능 생성 및 사용 방법(명령이나 코드 예시 포함)을 소개해야 합니다. 내용은 간결하고 실용적으로 작성해 AI가 적절한 코드를 생성할 수 있게 해주세요. 예시는 아래와 같습니다.

```php
## 패키지 이름

이 패키지는 [기능에 대한 간략한 설명]을 제공합니다.

### 특징

- 기능 1: [간단한 설명].
- 기능 2: [간단한 설명]. 사용 예시:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

<a name="agent-skills"></a>
## 에이전트 스킬

[에이전트 스킬](https://agentskills.io/home)은 특정 도메인 작업 시 에이전트가 선택적으로 활성화하는, 경량화된 지식 모듈입니다. 가이드라인은 에이전트가 시작될 때 항상 불러오지만, 스킬은 필요한 순간에만 로드되어 AI 코드 생성의 정확성과 효율을 높여줍니다.

`boost:install` 실행 시 스킬 기능을 선택하면, `composer.json`에서 감지된 패키지에 따라 스킬이 자동 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 있다면 `livewire-development` 스킬이 자동 설치됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬

| 스킬                        | 패키지        |
|-----------------------------|--------------|
| fluxui-development          | Flux UI      |
| folio-routing               | Folio        |
| inertia-react-development   | Inertia React|
| inertia-svelte-development  | Inertia Svelte|
| inertia-vue-development     | Inertia Vue  |
| livewire-development        | Livewire     |
| mcp-development             | MCP          |
| pennant-development         | Pennant      |
| pest-testing                | Pest         |
| tailwindcss-development     | Tailwind CSS |
| volt-development            | Volt         |
| wayfinder-development       | Wayfinder    |

> **참고:** 스킬 역시 [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하여 업데이트할 수 있습니다.

<a name="custom-skills"></a>
### 사용자 정의 스킬

직접 만든 사용자 정의 스킬을 생성하려면, 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가하세요. `boost:update` 실행 시, 사용자 스킬이 Boost 내장 스킬과 함께 설치됩니다.

예를 들어, 도메인 로직에 대한 사용자 스킬을 만들려면 다음 경로에 파일을 생성하세요.

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 오버라이드

Boost 내장 스킬과 이름이 같은 사용자 정의 스킬을 만들면, Boost는 내장 스킬 대신 해당 사용자 버전을 사용합니다.

예를 들어, Boost의 `livewire-development` 스킬을 오버라이드하려면 이 경로에 파일을 생성하세요.

```
.ai/skills/livewire-development/SKILL.md
```

`boost:update` 실행 시 커스텀 스킬이 포함됩니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

서드파티 패키지를 개발 중이라면, Boost가 해당 패키지에 대한 스킬을 포함하도록 만들 수 있습니다. 패키지 내부에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행할 때 Boost가 해당 스킬을 사용자 선택에 따라 설치합니다.

Boost 스킬은 [Agent Skills 포맷](https://agentskills.io/what-are-skills)을 지원하며, 폴더 내에 YAML 프론트매터와 Markdown으로 작성된 `SKILL.md` 파일을 포함해야 합니다. 프론트매터에는 반드시 `name`과 `description`이 포함되어야 하며, 필요에 따라 스크립트, 템플릿, 참고 자료를 추가할 수 있습니다.

스킬에는 필수 파일 구조 또는 관례, 주요 기능 생성 및 사용 방법(명령어나 코드 예시 포함)이 설명되어야 합니다. 내용은 간결하고 실용적이어야 하며, AI가 올바른 코드를 생성할 수 있도록 작성하세요.

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## 이 스킬을 사용해야 할 때
PackageName의 주요 기능을 개발할 때 이 스킬을 사용하세요...

## 특징

- 기능 1: [간단한 설명].
- 기능 2: [간단한 설명]. 사용 예시:

$result = PackageName::featureTwo($param1, $param2);
```

<a name="guidelines-vs-skills"></a>
## 가이드라인과 스킬의 차이

Laravel Boost는 AI 에이전트에게 애플리케이션 맥락 제공을 위해 **가이드라인**과 **스킬**, 이 두 가지 접근을 제공합니다.

**가이드라인**은 AI 에이전트가 시작할 때 미리 불러와, Laravel 전반에 적용되는 핵심 관례와 모범 사례 등 중요 정보를 제공합니다.

**스킬**은 특정 작업 시 온디맨드 방식으로 활성화되며, Livewire 컴포넌트, Pest 테스트 등 세부 도메인별 패턴과 모범 사례를 담고 있습니다. 스킬을 필요할 때만 로드하면, 전체 컨텍스트 부담을 줄이고 코드의 품질을 높일 수 있습니다.

| 구분          | 가이드라인             | 스킬                   |
|---------------|-----------------------|------------------------|
| **로드 시점**  | 시작 시, 항상 활성화   | 필요 시 온디맨드 로드  |
| **범위**      | 전체적, 기초적         | 도메인별, 작업 특화    |
| **목적**      | 핵심 관례/모범 사례    | 구체적 구현 패턴       |

<a name="documentation-api"></a>
## 문서화 API

Laravel Boost는 17,000개가 넘는 Laravel 특화 정보를 담은 방대한 지식 베이스에 AI 에이전트가 접근할 수 있는 문서화 API를 제공합니다. 이 API는 임베딩을 활용한 의미 기반 검색을 통해 정확하고 맥락에 맞는 결과를 제공합니다.

`Search Docs` MCP 도구를 통해, 에이전트는 설치 패키지에 기반한 Laravel 공식 문서 API 서비스에 질의할 수 있습니다. Boost의 AI 가이드라인과 스킬 역시 자동으로 코딩 에이전트에 이 API 사용법을 안내합니다.

| 패키지            | 지원 버전               |
|------------------|------------------------|
| Laravel Framework| 10.x, 11.x, 12.x       |
| Filament         | 2.x, 3.x, 4.x, 5.x     |
| Flux UI          | 2.x Free, 2.x Pro      |
| Inertia          | 1.x, 2.x               |
| Livewire         | 1.x, 2.x, 3.x, 4.x     |
| Nova             | 4.x, 5.x               |
| Pest             | 3.x, 4.x               |
| Tailwind CSS     | 3.x, 4.x               |

<a name="extending-boost"></a>
## Boost 확장하기

Boost는 많은 주요 IDE와 AI 에이전트를 기본적으로 지원합니다. 지원되지 않는 코딩 도구를 사용하고 있다면, 직접 에이전트를 구현해 Boost와 연동할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE/AI 에이전트 지원 추가

새로운 IDE 또는 AI 에이전트를 지원하려면, `Laravel\Boost\Install\Agents\Agent`를 확장하는 클래스를 생성하고, 필요에 따라 아래 계약 인터페이스를 구현하세요.

- `Laravel\Boost\Contracts\SupportsGuidelines`: AI 가이드라인 지원 추가
- `Laravel\Boost\Contracts\SupportsMcp`: MCP 지원 추가
- `Laravel\Boost\Contracts\SupportsSkills`: 에이전트 스킬 지원 추가

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

예시 구현은 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)를 참고하세요.

<a name="registering-the-agent"></a>
#### 에이전트 등록

애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 에이전트를 등록하세요.

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면, `php artisan boost:install` 실행 시 해당 에이전트를 선택할 수 있습니다.
