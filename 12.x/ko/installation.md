# 설치 (Installation)

- [라라벨 알아보기](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 라라벨 설치 도구 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [라라벨 Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 알아보기 (Meet Laravel)

Laravel은 표현력이 뛰어나고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란 애플리케이션 개발에 필요한 구조와 출발점을 제공함으로써, 세부적인 부분에 신경 쓰는 대신 멋진 결과물을 만드는 데만 집중할 수 있도록 돕는 도구입니다.

라라벨은 뛰어난 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서, 개발자에게 놀라운 경험을 선사하는 데 주력하고 있습니다.

PHP 웹 프레임워크가 처음이거나 오랜 경험을 가진 개발자라면, 라라벨은 여러분의 성장과 함께 발전할 수 있는 프레임워크입니다. 여러분의 첫걸음을 도와주거나, 더 높은 전문성에 도달하는 데 도움을 줄 준비가 되어 있습니다. 여러분이 만들어갈 작품을 기대합니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 여러 가지 도구와 프레임워크가 존재합니다. 하지만 저희는 라라벨이 현대적이고 풀스택 웹 애플리케이션 개발에 가장 적합한 선택이라고 믿습니다.

#### 점진적 프레임워크

라라벨은 "점진적(Progressive)" 프레임워크라고 부를 수 있습니다. 즉, 라라벨은 여러분과 함께 성장한다는 의미입니다. 웹 개발에 막 입문했다면, 방대한 문서, 가이드, 그리고 [비디오 튜토리얼](https://laracasts.com)을 통해 부담 없이 배워나갈 수 있습니다.

시니어 개발자라면, 라라벨은 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 전문적인 웹 애플리케이션 구축에 꼭 맞는 강력한 도구들을 제공합니다. 라라벨은 엔터프라이즈 규모의 부담도 거뜬히 처리할 수 있도록 최적화되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 확장성이 매우 뛰어납니다. PHP의 확장 친화적인 특성과, Redis 같은 빠른 분산 캐시 시스템에 대한 내장 지원 덕분에, 라라벨로 수평 확장을 간편하게 구현할 수 있습니다. 실제로 라라벨 애플리케이션이 한 달에 수억 건 이상의 요청을 쉽게 처리한 사례도 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com) 같은 플랫폼을 활용하여 전례 없는 확장성을 누릴 수 있습니다.

#### 커뮤니티 기반 프레임워크

라라벨은 PHP 생태계의 최고의 패키지를 결합하여, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 실력 있는 개발자가 [프레임워크 개발에 기여](https://github.com/laravel/framework)하고 있습니다. 여러분도 앞으로 라라벨의 기여자가 될 수도 있습니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 라라벨 설치 도구 설치 (Installing PHP and the Laravel Installer)

라라벨 애플리케이션을 처음 만들기 전에, 여러분의 로컬 환경에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 설치 도구](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프론트엔드 에셋을 컴파일하려면 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬 환경에 PHP와 Composer가 설치되지 않은 경우, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer 그리고 라라벨 설치 도구까지 한번에 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

위 명령어 중 하나를 실행했다면, 터미널 세션을 재시작해야 합니다. `php.new`를 통해 설치 후 PHP, Composer, 라라벨 설치 도구를 최신 상태로 유지하려면, 위 명령어를 터미널에 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 라라벨 설치 도구를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 그래픽 환경의 PHP 설치 및 관리를 원한다면 [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, 라라벨 설치 도구가 준비됐다면, 이제 새로운 라라벨 애플리케이션을 만들 수 있습니다. 라라벨 설치 도구를 사용하면 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택할 수 있도록 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 뒤에는, `dev` Composer 스크립트를 사용하여 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 동시에 시작할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다. 이제 [라라벨 생태계의 다음 단계](#next-steps)를 시작할 준비가 된 것입니다. 물론, [데이터베이스 설정](#databases-and-migrations)도 추가로 진행할 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션을 더 빠르게 시작하고 싶다면, [스타터 키트](/docs/12.x/starter-kits)를 활용해 보세요. 라라벨 스타터 키트는 백엔드 및 프론트엔드 인증 스캐폴딩을 미리 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 자세한 설명이 있으니, 파일들을 살펴보며 어떤 설정이 가능한지 익혀보세요.

기본적으로 라라벨은 추가적인 설정이 거의 필요 없습니다. 바로 개발을 시작해도 좋습니다! 하지만, `config/app.php` 파일과 문서를 한 번쯤 검토하는 것이 좋습니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 맞게 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 많은 설정 옵션 값은 애플리케이션이 로컬 환경에서 실행되는지, 운영 서버에서 실행되는지에 따라 달라집니다. 그래서 여러 중요한 설정 값은 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의합니다.

`.env` 파일은 애플리케이션을 사용하는 각 개발자나 서버별로 환경이 달라질 수 있기 때문에, 소스 컨트롤에는 절대 커밋하지 않아야 합니다. 만약 소스 컨트롤이 외부에 노출된다면 중요한 정보(자격 증명 등)가 위험에 빠지기 때문입니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대해 더 알고 싶다면 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

라라벨 애플리케이션을 만들었다면, 이제 데이터를 데이터베이스에 저장하고 싶을 수 있습니다. 기본적으로 여러분의 `.env` 설정 파일에는 라라벨이 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션을 생성할 때, 라라벨은 자동으로 `database/database.sqlite` 파일을 만들고, 필요한 마이그레이션을 실행해 데이터베이스 테이블을 구성해줍니다.

만약 MySQL이나 PostgreSQL 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일을 원하는 데이터베이스에 맞게 수정하면 됩니다. 예를 들어, MySQL을 사용하려면 다음과 같이 `DB_*` 변수를 변경하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 외의 데이터베이스를 사용할 경우, 데이터베이스를 직접 생성한 뒤 애플리케이션의 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치하려면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용할 수 있습니다.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

라라벨은 반드시 웹 서버에 설정된 "웹 디렉터리"의 루트에서 제공되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨 애플리케이션을 제공하려고 하면, 애플리케이션 내부의 민감한 파일이 외부에 노출될 수 있으므로 절대 그렇게 하지 마세요.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠르고, 네이티브한 라라벨 및 PHP 개발 환경입니다. Herd만 설치하면 라라벨 개발에 필요한 PHP, Nginx 등 모든 것을 바로 사용할 수 있습니다.

Herd를 설치하면 라라벨 개발을 바로 시작할 수 있으며, `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등의 커맨드라인 도구가 함께 제공됩니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가로 강력한 기능을 더해주며, 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰잉, 로그 모니터링 등도 지원합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS에서 개발한다면 [Herd 웹사이트](https://herd.laravel.com)에서 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 자동으로 최신 PHP를 다운로드하고, Mac이 항상 [Nginx](https://www.nginx.com/)를 백그라운드에서 실행하도록 설정해줍니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해서 "파킹된(parked)" 디렉터리를 지원합니다. parked 디렉터리에 있는 라라벨 애플리케이션은 Herd가 자동으로 서비스합니다. 기본적으로 Herd는 `~/Herd`에 parked 디렉터리를 만들며, 이 안에 있는 모든 라라벨 애플리케이션은 디렉터리 이름을 그대로 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후 새로운 라라벨 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 라라벨 CLI를 사용하는 것입니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, System Tray의 Herd 메뉴에서 Herd UI를 열어 parked 디렉터리 및 PHP 설정도 쉽게 관리할 수 있습니다.

Her드에 대한 더 자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

[Herd 웹사이트](https://herd.laravel.com/windows)에서 Windows용 Herd 설치 파일을 다운로드할 수 있습니다. 설치가 끝나면 Herd를 실행해서 초기 설정을 완료하고, Herd UI에 처음으로 접근할 수 있습니다.

Herd UI는 시스템 트레이에 있는 Herd 아이콘을 마우스 왼쪽 클릭해 접근할 수 있습니다. 오른쪽 클릭하면, 자주 사용하는 모든 도구에 빠르게 접근할 수 있는 퀵 메뉴가 열립니다.

설치 과정에서 Herd는 홈 디렉터리 `%USERPROFILE%\Herd`에 "파킹된" 디렉터리를 만듭니다. parked 디렉터리에 있는 라라벨 애플리케이션은 자동으로 Herd가 서비스하며, 디렉터리 이름을 그대로 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후 Powershell을 열고 아래 명령으로 새로운 라라벨 애플리케이션을 가장 빠르게 만들 수 있습니다:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows에서 Herd 사용에 대해 더 알고 싶다면 [Herd의 Windows 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발 시 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 가볍고 확장성 있는 에디터를 원한다면, [VS Code](https://code.visualstudio.com)나 [Cursor](https://cursor.com)에 공식 [Laravel VS Code 확장](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 설치해 사용할 수 있습니다. 이 확장은 구문 강조, 코드 스니펫, 아티즌 명령어 통합, Eloquent 모델, 라우트, 미들웨어, 에셋, 설정, Inertia.js에 대한 스마트 자동 완성 등 뛰어난 라라벨 지원 기능을 제공합니다.

JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)과 [Laravel Idea 플러그인](https://laravel-idea.com/)을 조합해 사용하면 라라벨 및 생태계(Pint, Larastan, Pest 등)에 대한 폭넓은 지원을 받을 수 있습니다. Blade 템플릿, Eloquent 모델, 라우트, 뷰, 번역 파일, 컴포넌트까지 스마트 자동 완성, 강력한 코드 생성, 라라벨 프로젝트 전체에 걸친 코드 네비게이션을 지원합니다.

클라우드 기반 개발 환경을 찾는다면, [Firebase Studio](https://firebase.studio/)를 통해 브라우저에서 바로 라라벨을 개발할 수 있습니다. 별도의 설정 없이 바로 사용할 수 있으며, 어느 기기에서든 라라벨 애플리케이션 개발을 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션 간의 간극을 메워주는 강력한 도구입니다. Boost는 AI 에이전트에게 라라벨 특화된 컨텍스트, 도구, 가이드라인을 제공하여, 라라벨 관례에 맞고 버전별로 정확한 코드를 생성하도록 도와줍니다.

Boost를 애플리케이션에 설치하면, AI 에이전트는 설치된 패키지 확인, 데이터베이스 쿼리, 라라벨 공식 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등 15개 이상의 특화 도구를 사용할 수 있습니다.

또한 Boost는 라라벨 생태계 공식 문서 17,000여 개를 벡터화해, 프로젝트에 설치된 패키지 버전에 맞는 정확한 정보를 AI 에이전트에 제공합니다.

Boost는 라라벨에서 유지 관리하는 AI용 가이드라인도 함께 제공하여, 프레임워크의 관례를 잘 지키도록 하고, 적절한 테스트 작성과 흔한 실수를 피하는 데 도움을 줍니다.

<a name="installing-laravel-boost"></a>
### 라라벨 Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상을 사용하는 라라벨 10, 11, 12 버전에서 설치할 수 있습니다. 먼저, 개발 의존성으로 Boost를 설치합니다:

```shell
composer require laravel/boost --dev
```

설치가 끝나면, 대화형 설치 도구를 실행해주세요:

```shell
php artisan boost:install
```

설치 도구는 여러분의 IDE와 AI 에이전트를 자동으로 감지하고, 프로젝트에 적합한 기능을 선택하도록 안내합니다. Boost는 기존 프로젝트의 관례를 존중하며, 기본적으로 의견이 강한 스타일 규칙을 강제하지 않습니다.

> [!NOTE]
> Boost에 대해 더 알아보고 싶다면, [Laravel Boost의 GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 라라벨 애플리케이션을 만들었으니, 다음으로 무엇을 배워야 할지 궁금할 수 있습니다. 먼저, 라라벨이 어떻게 동작하는지 익히기 위해 아래 문서를 꼭 읽어보시길 적극 추천합니다:

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

여러분이 라라벨을 어떻게 활용할지에 따라서도 배워야 할 다음 단계가 달라집니다. 라라벨을 사용할 수 있는 다양한 방법 중, 아래 두 가지 주요 활용 사례를 살펴보겠습니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

라라벨은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란 라라벨로 요청 라우팅과 함께, [Blade 템플릿](/docs/12.x/blade) 또는 [Inertia](https://inertiajs.com)와 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 랜더링하는 방식을 의미합니다. 라라벨을 사용하는 가장 일반적인 방법이자, 가장 생산적인 방법이라고 생각합니다.

이 방식을 선택했다면, [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고해 보세요. 뿐만 아니라, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 배워볼 만합니다. 이러한 패키지는, 라라벨을 풀스택 프레임워크로 사용하면서, 단일 페이지 자바스크립트 애플리케이션의 UI 혜택을 누릴 수 있도록 해줍니다.

풀스택 프레임워크로 라라벨을 사용할 경우, [Vite](/docs/12.x/vite)를 이용해 애플리케이션의 CSS 및 JavaScript를 컴파일하는 방법도 꼭 익혀두시길 추천합니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 더 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

라라벨은 자바스크립트 기반의 단일 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로도 활용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용하는 경우입니다. 이 경우, 라라벨을 통해 [인증](/docs/12.x/sanctum), 데이터 저장 및 조회 기능을 제공받고, 큐, 이메일, 알림 등 다양한 강력한 서비스를 활용할 수 있습니다.

이 방식을 선택했다면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고해 보세요.
