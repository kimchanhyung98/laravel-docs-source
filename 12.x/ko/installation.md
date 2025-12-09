# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP와 라라벨 설치 도구 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 구성](#initial-configuration)
    - [환경 기반 구성](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 구성](#directory-configuration)
- [Herd를 활용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

Laravel은 표현적이며 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란, 여러분의 애플리케이션을 만들 수 있는 구조와 출발점을 제공하여, 세부적인 부분에 신경 쓸 필요 없이 핵심에 집중해 멋진 결과물을 만들 수 있도록 도와주는 도구입니다.

Laravel은 뛰어난 개발 경험을 제공하면서도, 강력한 기능들을 포함하고 있습니다. 예를 들어, 꼼꼼한 의존성 주입, 직관적인 데이터베이스 추상화 계층, 큐와 예약된 작업, 단위 및 통합 테스트 등 다양한 기능을 지원합니다.

PHP 웹 프레임워크가 처음인 분이든, 풍부한 경험을 가진 분이든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발에 입문하는 첫걸음을 함께하거나, 여러분의 전문 역량을 한 단계 끌어올릴 수 있도록 돕겠습니다. 여러분이 무엇을 만들어갈지 기대하겠습니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 선택할 수 있는 많은 도구와 프레임워크가 존재합니다. 그러나 Laravel이 현대적인 풀스택 웹 애플리케이션을 구축하기 위한 최고의 선택이라고 자신합니다.

#### 점진적인(Progressive) 프레임워크

Laravel은 "점진적인(progressive)" 프레임워크라 부릅니다. 즉, 여러분의 실력과 함께 Laravel도 점진적으로 성장합니다. 웹 개발에 막 입문하는 분이라면, 방대한 공식 문서, 가이드, 그리고 [동영상 강의](https://laracasts.com)를 통해 부담을 느끼지 않고 기초부터 탄탄하게 배울 수 있습니다.

상위 개발자라면, Laravel이 제공하는 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 도구들을 활용할 수 있습니다. Laravel은 전문적인 웹 애플리케이션 구축을 위해 조정되어 있으며, 엔터프라이즈급 작업 부하도 감당할 준비가 되어 있습니다.

#### 확장 가능한(Scalable) 프레임워크

Laravel은 매우 뛰어난 확장성을 지원합니다. PHP 특유의 확장 친화적 특성과, Redis와 같은 빠르고 분산된 캐시 시스템을 내장 지원함으로써, Laravel을 이용한 수평적(호리즌탈) 확장이 매우 쉽습니다. 실제로 Laravel로 개발된 애플리케이션이 월 수억 건의 요청도 무리 없이 처리해왔습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 거의 무한대에 가까운 확장성을 경험할 수 있습니다.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계에서 가장 뛰어난 패키지들을 결합하여 개발자 친화적이고 견고한 프레임워크를 제공합니다. 또한, 전 세계의 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해 왔습니다. 어쩌면, 여러분도 Laravel에 기여하게 될지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP와 라라벨 설치 도구 설치 (Installing PHP and the Laravel Installer)

첫 번째 Laravel 애플리케이션을 만들기 전에, 로컬 환경에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 설치 도구](https://github.com/laravel/installer)가 설치되어 있어야 합니다. 또한, 프론트엔드 자산 번들을 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나도 설치해야 합니다.

만약 PHP와 Composer가 설치되어 있지 않다면, 아래의 명령어로 macOS, Windows, Linux에서 PHP, Composer, 라라벨 설치 도구를 한 번에 설치할 수 있습니다.

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

위 명령 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 PHP, Composer, 라라벨 설치 도구를 설치한 후 업데이트가 필요하다면, 위와 동일한 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer로 라라벨 설치 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 기능과 그래픽 환경에서 PHP 설치와 관리를 원한다면 [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, 라라벨 설치 도구의 설치가 끝났다면, 이제 새 Laravel 애플리케이션을 생성할 준비가 되었습니다. 라라벨 설치 도구를 이용하면, 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택할 수 있습니다.

```shell
laravel new example-app
```

애플리케이션이 생성된 후에는, `dev` Composer 스크립트를 사용해 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 동시에 실행할 수 있습니다.

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되고 나면 [http://localhost:8000](http://localhost:8000)에서 브라우저로 애플리케이션을 확인할 수 있습니다. 이제, [다음 단계로 라라벨 생태계를 좀 더 경험해볼 준비가 되었습니다](#next-steps). 물론, [데이터베이스 구성](#databases-and-migrations)도 할 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 빠르게 시작하고 싶다면 [스타터 키트](/docs/12.x/starter-kits)를 활용해 보세요. 라라벨 스타터 키트는 백엔드와 프론트엔드 인증 스캐폴딩을 제공하여 새로운 애플리케이션 구축을 한층 더 쉽고 빠르게 할 수 있습니다.

<a name="initial-configuration"></a>
## 초기 구성 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일들은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 문서가 잘 작성되어 있으므로 파일을 자유롭게 열어보고 어떤 설정들이 있는지 미리 익혀두시길 권장합니다.

Laravel은 기본적으로 별도의 추가 설정 없이 바로 개발을 시작할 수 있도록 설계되었습니다. 하지만 필요하다면 `config/app.php` 파일과 문서를 확인해보세요. `url`, `locale` 등 여러분의 애플리케이션에 맞게 변경할 수 있는 항목들이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 구성 (Environment Based Configuration)

Laravel의 많은 설정값은 애플리케이션이 로컬에서 실행되는지, 프로덕션 서버에서 실행되는지에 따라 달라질 수 있습니다. 이런 환경에 따라 중요한 설정값들을 별도로 관리할 수 있도록, 애플리케이션 루트에 위치한 `.env` 파일을 사용합니다.

`.env` 파일은 소스 제어에 커밋해서는 안 됩니다. 왜냐하면, 각 개발자/서버마다 각기 다른 환경 설정이 필요하며, 만약 소스 저장소가 외부에 노출된다면 중요한 인증 정보가 유출될 위험이 있기 때문입니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 더 많은 정보는 전체 [설정 문서](/docs/12.x/configuration#environment-configuration)에서 확인하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션 (Databases and Migrations)

이제 Laravel 애플리케이션을 만들었다면, 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 Laravel이 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션을 생성할 때 Laravel이 자동으로 `database/database.sqlite` 파일을 만들어주고, 필요한 마이그레이션을 실행해서 기본 데이터베이스 테이블까지 직접 생성해줍니다.

MySQL, PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일에서 적절한 데이터베이스 정보를 수정하면 됩니다. 예를 들어 MySQL을 사용하려면 아래와 같이 `DB_*` 변수를 수정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 사용한다면, 해당 데이터베이스를 직접 만들어주고 아래와 같이 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다.

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows 환경에서 MySQL, PostgreSQL, Redis를 간편하게 설치하고 싶다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용해 보세요.

<a name="directory-configuration"></a>
### 디렉터리 구성 (Directory Configuration)

Laravel 애플리케이션은 항상 웹 서버에서 설정한 "웹 디렉터리"의 루트에서 서비스되어야 합니다. "웹 디렉터리"의 서브디렉터리에서 라라벨 애플리케이션을 서비스하려고 하면, 내부적으로 중요한 파일들이 외부에 노출될 위험이 있으니 절대 그렇게 하지 마세요.

<a name="installation-using-herd"></a>
## Herd를 활용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd는 Laravel 개발에 필요한 모든 것(PHP, Nginx 등)을 한 번에 제공합니다.

Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 다양한 명령어 도구가 포함되어 있습니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가로, 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰잉, 로그 모니터링처럼 개발에 도움이 되는 강력한 기능들이 추가로 제공됩니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS에서 개발하는 경우, [Herd 공식 웹사이트](https://herd.laravel.com)에서 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP를 자동으로 설치하고, Mac 환경에서 [Nginx](https://www.nginx.com/)가 항상 백그라운드에서 실행되도록 설정해줍니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여 "파크드 디렉터리(parked directory)" 기능을 지원합니다. 파크드 디렉터리 내에 있는 어떤 Laravel 애플리케이션도 자동으로 Herd에 의해 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 파크드 디렉터리를 생성하며, 이 안의 모든 Laravel 애플리케이션에 디렉터리 이름을 통해 `.test` 도메인으로 접근할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 번들된 Laravel CLI를 사용하는 것입니다.

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, Herd 메뉴(시스템 트레이)에서 파크드 디렉터리 관리, PHP 설정 등 다양한 기능을 UI를 통해 직접 관리할 수도 있습니다.

Herd에 대해 더 자세한 내용은 [Herd 공식 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

Windows용 Herd 설치 프로그램은 [Herd 공식 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면 Herd를 실행하여 최초 온보딩 과정을 진행할 수 있으며, Herd UI에 처음으로 접근할 수 있습니다.

Herd UI는 시스템 트레이에 있는 Herd 아이콘을 왼쪽 클릭해 접근할 수 있습니다. 오른쪽 클릭 시에는 자주 사용하는 모든 툴에 빠르게 접근할 수 있는 메뉴가 열립니다.

설치 과정에서 Herd는 홈 디렉터리 내에 `%USERPROFILE%\Herd` 경로로 파크드 디렉터리를 자동 생성합니다. 이 디렉터리 안의 Laravel 애플리케이션이면 어떤 것이든 Herd에서 자동으로 서비스하며, 디렉터리 이름을 활용한 `.test` 도메인으로 접근할 수 있습니다.

Herd 설치 이후, Laravel CLI를 사용해 새로운 애플리케이션을 만드는 가장 빠른 방법은 PowerShell에서 아래 명령어를 실행하는 것입니다.

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows용 Herd에 대해 더 자세히 알고 싶다면 [Herd 공식 Windows 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발하면서 어떤 코드 에디터를 사용해도 무방합니다. 가볍고 확장성 있는 에디터를 찾으신다면 [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)와 공식 [Laravel VS Code 확장 프로그램](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 조합해 사용할 수 있습니다. 이 조합은 구문 하이라이팅, 코드 스니펫, 아티즌 명령어 연동, Eloquent 모델, 라우트, 미들웨어, 자산, 설정, Inertia.js에 대한 스마트 자동완성 등 다양한 기능을 지원합니다.

라라벨에 대한 광범위하고 견고한 지원을 원한다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)이 훌륭한 선택입니다. PhpStorm은 Blade 템플릿, Eloquent 모델, 라우트, 뷰, 번역, 컴포넌트의 스마트 자동 완성, 강력한 코드 생성 및 라라벨 프로젝트 전체에 걸친 코드 네비게이션 기능을 내장 지원합니다.

클라우드 기반 개발 환경이 필요하다면, [Firebase Studio](https://firebase.studio/)를 사용해 브라우저만으로도 즉시 Laravel 개발을 시작할 수 있습니다. 별도 설치 없이 즉시 Laravel 애플리케이션을 구축할 수 있어 어느 환경에서나 유용하게 활용할 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션을 잇는 강력한 도구입니다. Boost는 AI 에이전트에 라라벨 생태계에 특화된 컨텍스트, 도구, 가이드라인을 제공하여, 더 정확하고 버전별 표준에 맞는 코드를 생성할 수 있도록 돕습니다.

Boost를 Laravel 애플리케이션에 설치하면, AI 에이전트가 사용할 수 있는 15개 이상의 특수 도구들이 활성화됩니다. 예를 들어, 설치된 패키지 확인, 데이터베이스 쿼리, 라라벨 공식 문서 검색, 브라우저 로그 읽기, 테스트 코드 자동 생성, Tinker를 통한 코드 실행 등이 지원됩니다.

또한 Boost는 설치된 패키지 버전에 맞는 약 17,000개 이상의 샘플로 벡터화된 Laravel 생태계 문서에도 접근할 수 있게 해줍니다. 덕분에, AI 에이전트는 프로젝트에서 실제 사용하는 버전에 정확히 맞는 가이드를 제공할 수 있습니다.

Boost에는 라라벨팀이 유지·관리하는 AI 가이드라인도 포함되어 있어서, AI 에이전트가 프레임워크의 규칙을 잘 지키고, 적절한 테스트 코드를 작성하며, 코드 생성 시 흔히 발생할 수 있는 실수를 예방할 수 있도록 돕습니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상이 실행되는 Laravel 10, 11, 12버전에 설치할 수 있습니다. 다음 명령어로 Boost를 개발 의존성으로 추가하세요.

```shell
composer require laravel/boost --dev
```

설치가 끝나면, 아래와 같이 대화형(인터랙티브) 설치 프로그램을 실행하세요.

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동 감지하여 여러분의 프로젝트에 맞는 기능들을 선택할 수 있게 해줍니다. Boost는 기존 프로젝트의 규칙을 존중하며, 기본적으로 별도의 스타일 규칙을 강요하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알고 싶다면 [Laravel Boost의 GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 만들었다면, 다음에는 무엇을 배워야 할지 궁금하실 것입니다. 먼저, Laravel의 동작 원리를 익히기 위해 아래 문서를 꼭 읽어보길 강력하게 권장합니다.

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

Laravel을 어떻게 활용하는지에 따라 마주할 다음 단계도 달라질 수 있습니다. 아래에서는 프레임워크의 두 가지 대표적인 활용 사례를 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란, 라라벨이 애플리케이션의 요청 라우팅을 담당하고, [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 SPA(싱글 페이지 애플리케이션) 하이브리드 기술을 활용해 프론트엔드까지 함께 렌더링하는 방식을 의미합니다. 이는 가장 일반적이며, 가장 생산적인 라라벨 활용 방법입니다.

이렇게 활용하고자 한다면, [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent)을 살펴보세요. 또한, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 등 커뮤니티 패키지로 SPA의 강력한 UI 경험도 함께 사용할 수 있습니다.

풀스택 프레임워크로 활용한다면, [Vite](/docs/12.x/vite)를 사용해 애플리케이션의 CSS, JavaScript 등을 빌드하는 방법도 필수로 익히시길 권장합니다.

> [!NOTE]
> 빠른 애플리케이션 구축을 원한다면 [공식 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

Laravel은 자바스크립트 SPA(싱글 페이지 애플리케이션)나 모바일 앱의 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이때, Laravel은 [인증](/docs/12.x/sanctum), 데이터 저장/조회, 큐, 메일, 알림 등 다양한 서비스를 제공하게 됩니다.

이런 방식으로 Laravel을 사용할 계획이라면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 관련 문서를 확인해보세요.