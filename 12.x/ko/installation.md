# 설치 (Installation)

- [Laravel 만나보기](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel Installer 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용하기](#herd-on-macos)
    - [Windows에서 Herd 사용하기](#herd-on-windows)
- [IDE 지원](#ide-support)
- [Laravel과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나보기 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 지닌 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하여, 세부적인 부분은 Laravel이 신경 쓸 동안 여러분은 멋진 무언가를 만드는 데에 집중할 수 있게 합니다.

Laravel은 뛰어난 개발자 경험을 제공하는 동시에, 강력한 기능을 지원합니다. 예를 들어, 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 스케줄된 작업, 단위 및 통합 테스트 등 다양한 기능을 제공합니다.

PHP 웹 프레임워크가 처음인 분이든, 수년간의 경험이 있으신 분이든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 여러분이 웹 개발자로 첫걸음을 내딛을 때도, 전문성을 한 단계 더 끌어올릴 때에도 Laravel이 도움을 드립니다. 여러분이 무엇을 만들지 기대하겠습니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 사용할 수 있는 다양한 도구와 프레임워크가 존재합니다. 하지만 저희는 Laravel이 현대적인 풀스택 웹 애플리케이션을 개발하는 데 가장 적합하다고 믿습니다.

#### 점진적(Progressive) 프레임워크

Laravel은 "점진적(Progressive)" 프레임워크라고 부르고 싶습니다. 이는 곧 Laravel이 여러분과 함께 성장한다는 뜻입니다. 웹 개발을 처음 시작하는 분이라면, 방대한 문서, 가이드 그리고 [비디오 튜토리얼](https://laracasts.com)이 있어, 부담 없이 학습을 시작할 수 있습니다.

시니어 개발자라면, Laravel은 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 도구들을 제공합니다. Laravel은 전문가용 애플리케이션 개발에 최적화되어 있으며, 엔터프라이즈급 워크로드도 문제없이 처리할 수 있습니다.

#### 확장 가능한(Scalable) 프레임워크

Laravel은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장성에 친화적인 특성과, Laravel이 내장 지원하는 빠르고 분산된 캐시 시스템(Redis 등) 덕분에, Laravel로 수평 확장이 매우 쉽습니다. 실제로 Laravel 애플리케이션은 월 수억 건의 요청도 무난히 처리할 수 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 사실상 무제한에 가까운 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계의 최고의 패키지들을 결합하여, 가장 강력하면서도 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크 개발에 기여](https://github.com/laravel/framework)해 왔습니다. 어쩌면 앞으로 여러분 또한 Laravel에 기여하는 개발자가 될 수도 있습니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel Installer 설치 (Installing PHP and the Laravel Installer)

처음으로 Laravel 애플리케이션을 만들기 전, [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel Installer](https://github.com/laravel/installer)가 로컬 컴퓨터에 설치되어 있는지 확인해야 합니다. 또한, 애플리케이션의 프론트엔드 자산을 컴파일하려면 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/)도 설치해야 합니다.

로컬 컴퓨터에 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어를 사용하여 macOS, Windows, Linux에서 PHP, Composer, Laravel Installer를 설치할 수 있습니다:

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

위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 설치한 이후 PHP, Composer, Laravel Installer를 업데이트하려면 터미널에서 동일한 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel Installer를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 그래픽 환경에서 PHP를 완전하게 설치하고 관리하는 경험을 원한다면 [Laravel Herd](#installation-using-herd)를 확인해 보세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel Installer를 설치했다면, 이제 새로운 Laravel 애플리케이션을 만들 준비가 되었습니다. Laravel Installer는 선호하는 테스트 프레임워크, 데이터베이스, 스타터 킷을 선택하라는 안내를 제공합니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 후에는, `dev` Composer 스크립트를 이용해 Laravel의 로컬 개발 서버, 큐 워커, 그리고 Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다. 다음으로 [Laravel 생태계의 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 물론, [데이터베이스 설정](#databases-and-migrations)도 진행할 수 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 빠르게 시작하려면, 공식 [스타터 킷](/docs/12.x/starter-kits) 중 하나를 사용하는 것도 고려해 보세요. Laravel의 스타터 킷은 새로운 애플리케이션에 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 설정 항목에는 관련 문서가 함께 제공되니, 자유롭게 파일을 살펴보며 다양한 옵션에 익숙해지시길 바랍니다.

Laravel은 기본적으로 별도의 추가 설정 없이도 바로 사용할 수 있습니다. 바로 개발을 시작하셔도 무방합니다! 다만, `config/app.php` 파일과 그 문서를 한 번 검토하는 것이 좋습니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 맞춰 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

Laravel의 많은 설정값은 애플리케이션이 로컬 컴퓨터에서 실행되는지, 또는 운영 서버에서 실행되는지에 따라 달라질 수 있으므로, 중요한 설정값 다수는 애플리케이션 루트에 있는 `.env` 파일로 정의됩니다.

`.env` 파일은 소스 제어(버전 관리)에 포함하지 않아야 합니다. 왜냐하면 애플리케이션을 사용하는 각 개발자나 서버마다 환경 설정이 달라질 수 있기 때문입니다. 또한, 누군가 소스 저장소에 접근한다면, 중요한 자격 증명이 노출되어 보안에 심각한 위협이 될 수 있습니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 설정에 대해 더 자세한 내용이 필요하다면, [전체 설정 문서](/docs/12.x/configuration#environment-configuration)를 살펴보세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션 (Databases and Migrations)

이제 Laravel 애플리케이션이 생성된 만큼 데이터베이스에 데이터를 저장하고 싶을 수 있습니다. 기본적으로, 애플리케이션의 `.env` 파일에는 Laravel이 SQLite 데이터베이스를 사용하도록 설정되어 있습니다.

애플리케이션 생성 시, Laravel은 `database/database.sqlite` 파일을 자동으로 생성하고, 애플리케이션에 필요한 마이그레이션을 실행하여 데이터베이스 테이블을 만듭니다.

MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 파일을 해당 데이터베이스에 맞게 수정하면 됩니다. 예를 들어, MySQL을 사용하려면 `.env` 파일의 `DB_*` 변수들을 아래와 같이 설정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 사용할 경우, 해당 데이터베이스를 직접 생성하고 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows에서 개발 중이라면, MySQL, PostgreSQL, Redis를 로컬에 설치할 필요가 있을 수 있습니다. 이럴 때는 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용하는 것을 고려해 보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

Laravel은 항상 웹 서버에 구성된 "웹 디렉터리"의 루트에서 서비스되어야 합니다. Laravel 애플리케이션을 "웹 디렉터리"의 하위 디렉터리에서 서비스하려 시도하지 마십시오. 그렇게 할 경우, 애플리케이션 내에 존재하는 민감한 파일이 외부에 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS 및 Windows에서 사용할 수 있는 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd에는 Laravel 개발을 시작하는 데 필요한 모든 것이 내장되어 있으며, PHP와 Nginx도 포함되어 있습니다.

Herd를 설치하고 나면, 바로 Laravel 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 다양한 커맨드라인 도구를 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가 강력한 기능을 제공하여, 로컬에서 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰어, 로그 모니터링 등을 지원합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용하기 (Herd on macOS)

macOS에서 개발한다면, [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 이 설치 프로그램은 최신 버전의 PHP를 자동으로 다운로드하며, Mac에서 [Nginx](https://www.nginx.com/)가 항상 백그라운드로 실행되도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여 "주차(parking)" 된 디렉터리를 지원합니다. 주차 디렉터리에 위치한 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 주차 디렉터리를 만들고, 이 디렉터리 안의 Laravel 애플리케이션에 디렉터리 이름을 사용하여 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 함께 제공되는 Laravel CLI를 사용하는 것입니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

또한, 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 주차 디렉터리 및 기타 PHP 설정을 손쉽게 관리할 수 있습니다.

macOS용 Herd에 대해 더 알아보려면 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용하기 (Herd on Windows)

Windows용 Herd는 [Herd 웹사이트](https://herd.laravel.com/windows)에서 설치 프로그램을 다운로드할 수 있습니다. 설치가 완료되면 Herd를 실행하여 온보딩 과정을 마치고, 처음으로 Herd UI에 접근할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하면 열립니다. 아이콘을 오른쪽 클릭하면 평소 자주 사용하는 모든 도구에 접근할 수 있는 빠른 메뉴가 나타납니다.

설치 과정에서 Herd는 홈 디렉터리 아래 `%USERPROFILE%\Herd`에 "주차" 디렉터리를 생성합니다. 이 디렉터리 안의 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 이용해 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd와 함께 제공되는 Laravel CLI를 사용하는 것입니다. 시작하려면 Powershell을 열어 아래 명령어를 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows에서 Herd를 사용하는 방법에 대해 더 자세히 알고 싶다면 [Herd 문서](https://herd.laravel.com/docs/windows)를 확인하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발할 때 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 가볍고 확장 가능한 에디터를 찾는다면, [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code 확장 프로그램](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 추가해 보세요. 이 확장 프로그램은 구문 강조, 코드 스니펫, 아티즌 명령어 통합, Eloquent 모델, 라우트, 미들웨어, 에셋, config, Inertia.js에 대한 자동완성 등 훌륭한 Laravel 지원 기능을 제공합니다.

더 전문적이고 강력한 Laravel 지원이 필요하다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 고려해 볼 수 있습니다. PhpStorm은 Blade 템플릿 지원, Eloquent 모델, 라우트, 뷰, 번역, 컴포넌트에 대한 스마트 자동완성, 강력한 코드 생성, 프로젝트 전체 탐색 기능 등을 내장하고 있습니다.

클라우드 기반 개발 환경을 선호한다면 [Firebase Studio](https://firebase.studio/)를 사용해 보세요. 별도의 설치 없이 브라우저에서 바로 Laravel 애플리케이션을 개발할 수 있으며, 모든 기기에서 즉시 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## Laravel과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션을 연결해 주는 강력한 도구입니다. Boost는 AI 에이전트에게 Laravel에 특화된 컨텍스트, 도구, 가이드라인을 제공하여, Laravel 관행을 준수하며 더 정확하고 버전별로 특화된 코드를 생성할 수 있도록 돕습니다.

Boost를 Laravel 애플리케이션에 설치하면, AI 에이전트는 15개 이상의 전문화된 도구(프로젝트에 설치된 패키지 식별, 데이터베이스 쿼리, Laravel 공식 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등)에 접근할 수 있습니다.

또한 Boost는 프로젝트에 설치된 패키지 버전에 맞는, 17,000개 이상의 벡터화된 Laravel 생태계 문서에 대한 접근 권한을 AI 에이전트에게 제공합니다. 즉, 프로젝트에서 사용하는 정확한 버전에 맞는 가이드를 AI가 제공할 수 있게 됩니다.

Boost에는 Laravel이 유지 관리하는 AI 가이드라인도 포함되어 있어, 에이전트가 프레임워크의 관행을 잘 따르고, 적절한 테스트를 작성하며, 코드 생성 시 자주 발생하는 문제를 피할 수 있도록 지원합니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상을 사용하는 Laravel 10, 11, 12 버전의 애플리케이션에 설치할 수 있습니다. Boost를 시작하려면 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후, 대화형 설치 프로그램을 실행합니다:

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하며, 프로젝트에 적합한 기능을 선택할 수 있도록 안내합니다. Boost는 기존 프로젝트의 관행을 존중하며, 기본적으로 특정 스타일 규칙을 강제하지 않습니다.

> [!NOTE]
> Boost에 대한 자세한 내용은 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
#### 맞춤형 AI 가이드라인 추가

Laravel Boost에 자체 AI 가이드라인을 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install` 실행 시 Laravel Boost의 가이드라인과 함께 자동으로 포함됩니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 생성했다면, 이제 무엇을 배우면 좋을지 고민될 수 있습니다. 우선, 아래의 문서를 읽고 Laravel의 동작 방식을 익히는 것을 적극 권장합니다:

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

사용 목적에 따라 Laravel을 활용하는 방식도 달라질 수 있습니다. 다양한 활용 방법 중, 아래 두 가지 주요 사용 사례를 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택" 프레임워크란, Laravel을 통해 애플리케이션 라우팅뿐 아니라 [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술을 이용해 프론트엔드까지 렌더링하는 방식을 말합니다. 이는 Laravel 프레임워크를 사용하는 가장 일반적이면서도, 생산성이 매우 높은 방법입니다.

이 방식을 고려한다면, [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고하면 좋습니다. 또한, 커뮤니티 패키지인 [Livewire](https://livewire.laravel.com)와 [Inertia](https://inertiajs.com)도 알아보세요. 이 패키지들은 Laravel을 풀스택 프레임워크로 활용하면서, 최신 JavaScript 단일 페이지 애플리케이션의 유저 인터페이스 장점도 동시에 누릴 수 있게 합니다.

풀스택 프레임워크로 Laravel을 사용하는 경우, [Vite](/docs/12.x/vite)를 이용해 CSS와 JavaScript를 컴파일하는 방법도 꼭 배워두길 추천합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel (Laravel the API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로서도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수도 있습니다. 이 경우, Laravel은 애플리케이션의 [인증](/docs/12.x/sanctum), 데이터 저장 및 조회를 담당하며, 강력한 큐, 이메일, 알림 등의 서비스를 함께 사용할 수 있습니다.

이렇게 Laravel을 활용할 계획이라면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 관련 문서를 참고해 보세요.

