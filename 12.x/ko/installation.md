# 설치 (Installation)

- [Laravel 만나기](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel Installer 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 구성](#initial-configuration)
    - [환경 기반 구성](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 구성](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [IDE 지원](#ide-support)
- [Laravel과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나기 (Meet Laravel)

Laravel은 표현력이 뛰어나고 세련된 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란, 여러분이 애플리케이션을 개발할 때 구조와 출발점을 제공하여, 반복적이고 세부적인 부분은 Laravel이 처리하고, 여러분은 창의적이고 멋진 기능 구현에 집중할 수 있도록 돕습니다.

Laravel은 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 풍부한 기능과 함께, 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

PHP 웹 프레임워크가 처음인 분이든, 다년간의 경험을 가진 분이든, Laravel은 여러분의 성장과 함께할 수 있는 프레임워크입니다. 처음 웹 개발을 시작할 때도, 더 높은 수준의 역량을 쌓고 싶을 때도 Laravel이 함께합니다. 여러분이 어떤 것들을 만들어 나갈지 저희도 기대하고 있습니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 선택할 수 있는 다양한 도구와 프레임워크가 있지만, 저희는 현대적인 풀스택 웹 애플리케이션을 만들기 위한 최고의 선택지가 Laravel이라고 생각합니다.

#### 발전하는 프레임워크

Laravel은 "진화하는(progressive)" 프레임워크라 불립니다. 즉, 여러분의 성장에 맞춰 함께 성장할 수 있다는 의미입니다. 웹 개발에 첫 발을 내딛는 분이라면, Laravel의 방대한 공식 문서, 가이드, [동영상 튜토리얼](https://laracasts.com) 덕분에 막막함 없이 개념들을 익힐 수 있습니다.

숙련된 개발자라면, Laravel에서 제공하는 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 개발 도구를 이용할 수 있습니다. Laravel은 엔터프라이즈급 업무도 무리 없이 처리할 수 있도록 정교하게 조율되어 있습니다.

#### 확장성 높은 프레임워크

Laravel은 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적인 특성과, Redis와 같은 빠르고 분산된 캐시 시스템에 대한 Laravel의 내장 지원 덕분에, 수평 확장은 매우 수월합니다. 실제로, Laravel 애플리케이션은 월 수억 건의 요청도 무난히 처리할 수 있도록 손쉽게 확장할 수 있습니다.

극단적인 확장이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 이용하여 거의 무제한의 규모로 Laravel 애플리케이션을 운영할 수도 있습니다.

#### Agent 지원에 최적화된 프레임워크

Laravel의 일관된 컨벤션과 명확하게 정의된 구조는 [AI 도우미(agent)](/docs/12.x/ai)를 활용한 개발에 매우 적합합니다. 예를 들어, AI 도우미에게 컨트롤러 생성을 요청하면 어디에 파일을 두어야 할지 정확히 알 수 있고, 새 마이그레이션을 추가할 때도 파일명과 위치가 예측 가능합니다. 이러한 일관성은 다른 유연성이 높은 프레임워크에서 AI 도구가 실수하기 쉬운 부분을 제거해줍니다.

구조뿐만 아니라, Laravel의 표현적 문법과 방대한 문서는 AI 도우미가 정확하고 Laravel다운 코드(관용적 코드)를 생성할 수 있도록 충분한 컨텍스트를 제공합니다. Eloquent 연관관계, form 요청 처리, 미들웨어 등은 모두 AI 도구가 쉽게 이해하고 따라할 수 있는 패턴으로 구현되어 있습니다. 그 결과 생성된 코드는 경험 많은 Laravel 개발자가 작성한 듯 자연스럽게 보입니다.

AI 도우미와 함께 Laravel로 개발해보고 싶다면, [agentic 개발](/docs/12.x/ai) 문서를 참고해보세요.

#### 커뮤니티 중심의 프레임워크

Laravel은 PHP 생태계에서 최고의 패키지들을 집약하여, 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 여러분도 언제든 기여자가 될 수 있습니다!

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel Installer 설치 (Installing PHP and the Laravel Installer)

Laravel 애플리케이션을 처음 생성하기 전에, [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel installer](https://github.com/laravel/installer)가 로컬 머신에 설치되어 있는지 확인하세요. 그리고 프론트엔드 에셋을 빌드하려면 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/)도 필요합니다.

로컬에 PHP와 Composer가 없다면, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer, Laravel installer를 한 번에 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

위 명령어를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 설치한 경우 PHP, Composer, Laravel installer를 최신 버전으로 업데이트하려면 터미널에서 위의 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 이용해 Laravel installer를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> GUI 기반의 PHP 설치 및 관리를 원하는 경우, [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel installer가 설치되었다면, 이제 새 Laravel 애플리케이션을 만들 준비가 된 것입니다. Laravel installer는 사용자의 선호에 따라 테스트 프레임워크, 데이터베이스, 스타터 키트 선택을 안내합니다:

```shell
laravel new example-app
```

애플리케이션 생성 후에는, 로컬 개발 서버, 큐 워커, Vite 개발 서버를 `dev` Composer 스크립트로 한 번에 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)에 접속하여 애플리케이션을 사용할 수 있습니다. 이제 [Laravel 생태계에서 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 물론, [데이터베이스 구성](#databases-and-migrations)도 필요한 경우 진행하세요.

> [!NOTE]
> Laravel 애플리케이션 개발을 빠르게 시작하려면, [스타터 키트](/docs/12.x/starter-kits) 사용을 고려하세요. 스타터 키트는 백엔드/프론트엔드 인증 기능을 포함한 기본 뼈대를 제공합니다.

<a name="initial-configuration"></a>
## 초기 구성 (Initial Configuration)

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 자세한 주석이 작성되어 있으니, 구성 파일을 둘러보며 어떤 설정들이 있는지 익혀보시기 바랍니다.

Laravel은 기본적으로 별도의 추가 설정 없이도 바로 개발을 시작할 수 있습니다. 하지만 `config/app.php` 파일과 해당 문서를 한 번 읽어볼 것을 권장합니다. 이 파일에는 `url`, `locale` 등 애플리케이션별로 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 구성 (Environment Based Configuration)

Laravel의 여러 구성 옵션 값은 애플리케이션이 로컬에서 실행되는지, 프로덕션 서버에서 실행되는지에 따라 달라질 수 있습니다. 이를 위해, 중요한 구성 값 대부분은 애플리케이션 루트에 위치한 `.env` 파일을 통해 설정됩니다.

`.env` 파일은 각 개발자나 서버가 각기 다른 환경 구성을 필요로 할 수 있으므로, 소스 제어(예: git)에 포함되지 않아야 합니다. 만약 소스 저장소에 이 파일이 노출된다면, 민감한 정보(접근키 등)가 유출될 위험이 있으니 보안에 각별히 유의해야 합니다.

> [!NOTE]
> `.env` 파일과 환경 기반 구성에 대한 자세한 내용은 [구성 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

Laravel 애플리케이션을 생성한 후에는 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로, `.env` 환경 설정에서는 SQLite 데이터베이스를 사용하도록 설정되어 있습니다.

애플리케이션 생성 시, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 필수 마이그레이션을 실행하여 필요한 데이터베이스 테이블을 만들어줍니다.

MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 파일에서 관련 데이터베이스 정보를 아래 예시처럼 수정하면 됩니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 사용할 경우, 직접 데이터베이스를 생성하고, 아래와 같이 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows 환경에서 MySQL, PostgreSQL, Redis를 로컬에 설치하려면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/) 사용을 고려해보세요.

<a name="directory-configuration"></a>
### 디렉터리 구성 (Directory Configuration)

Laravel은 반드시 웹 서버에 설정된 "웹 디렉터리"의 루트에서 제공되어야 합니다. 웹 디렉터리 내의 서브 디렉터리에서 Laravel 애플리케이션을 제공해서는 안 됩니다. 그렇게 하면 애플리케이션의 민감한 파일이 노출될 수 있으니 주의하세요.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd만 설치하면, Laravel 개발에 필요한 PHP, Nginx 등이 전부 준비됩니다.

Herd를 설치하면 즉시 Laravel 개발을 시작할 수 있습니다. `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 다양한 커맨드라인 도구가 기본 제공됩니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 확인과 로그 모니터링 등 Herd의 강력한 기능을 추가로 제공합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS를 사용하는 경우, [Herd 공식 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 이 설치 프로그램은 Mac에 최적화된 최신 PHP를 자동으로 내려받아 설치하고, [Nginx](https://www.nginx.com/)가 항상 백그라운드에서 실행되도록 설정합니다.

macOS 버전의 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 "parked" 디렉터리를 지원합니다. parked 디렉터리에 있는 Laravel 애플리케이션은 Herd가 자동으로 제공합니다. 기본적으로 `~/Herd`에 parked 디렉터리가 생성되며, 이 디렉터리 안의 각 애플리케이션은 `.test` 도메인으로 바로 접속할 수 있습니다.

Herd 설치 후, Laravel CLI(명령어 도구)를 사용하면 가장 빠르게 새 Laravel 애플리케이션을 만들 수 있습니다. Laravel CLI는 Herd에 기본 포함되어 있습니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

고급 설정이나 parked 디렉터리 관리, PHP 설정 등은 Herd의 UI(시스템 트레이 메뉴에서 실행)에서 할 수 있습니다.

더 자세한 내용은 [Herd 공식 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

[Herd 공식 웹사이트](https://herd.laravel.com/windows)에서 Windows용 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치가 끝나면 Herd를 실행해 초기 설정을 완료하고 UI를 처음 사용할 수 있습니다.

Herd의 UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하면 열 수 있고, 오른쪽 클릭하면 자주 쓰는 도구에 빠르게 접근할 수 있는 퀵 메뉴가 나타납니다.

설치 과정에서 Heimdall은 `%USERPROFILE%\Herd`에 "parked" 디렉터리를 만듭니다. 이 디렉터리에 있는 Laravel 애플리케이션은 Herd가 자동으로 제공하며, 디렉터리명으로 `.test` 도메인에 바로 접근할 수 있습니다.

Windows에서도 Laravel CLI가 번들로 제공되며, 아래와 같이 Powershell에서 Laravel 애플리케이션을 빠르게 생성할 수 있습니다:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

자세한 사항은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발할 때 어떤 코드 에디터를 사용해도 무방합니다. 가볍고 확장성 있는 에디터로는 [VS Code](https://code.visualstudio.com)나 [Cursor](https://cursor.com)가 있으며, 공식 [Laravel VS Code 확장 프로그램](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 함께 사용하면 구문 강조, 코드 스니펫, 아티즌 명령 통합, Eloquent 모델/라우트/미들웨어/에셋/설정/Inertia.js에 대한 스마트 자동완성 등 뛰어난 Laravel 지원을 경험할 수 있습니다.

더 풍부한 기능을 원한다면 JetBrains 사의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 추천합니다. PhpStorm은 Blade 템플릿, Eloquent, 라우트, 뷰, 번역, 컴포넌트에 대한 스마트 자동완성과 코드 생성, 프로젝트 내비게이션 등 Laravel 개발에 최적화된 기능을 제공합니다.

클라우드 기반 개발 환경을 원한다면, [Firebase Studio](https://firebase.studio/)에서 브라우저만으로 Laravel 애플리케이션을 즉시 개발할 수 있습니다. 설치나 준비 과정 없이, 어떤 기기에서든 손쉽게 Laravel 개발을 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## Laravel과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션을 연결해주는 강력한 도구입니다. Boost는 AI 에이전트에게 Laravel에 특화된 컨텍스트, 도구, 가이드라인을 제공하여, 라라벨 컨벤션을 준수하는 정확하고 버전별로 최적화된 코드를 생성할 수 있도록 도와줍니다.

Boost를 설치하면 AI 에이전트는 15가지가 넘는 전문 도구를 사용할 수 있게 되며, 프로젝트에서 사용하는 패키지 조회, 데이터베이스 질의, 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등이 가능해집니다.

또한 Boost는 현재 설치된 패키지 버전 기준으로 17,000건 이상의 벡터화된 Laravel 생태계 문서에 AI가 접근할 수 있게 해줍니다. AI는 프로젝트 버전에 맞춰 정확한 가이드와 설명을 제공할 수 있습니다.

Boost에는 Laravel 팀이 관리하는 AI 가이드라인도 포함되어 있어, AI가 프레임워크 컨벤션을 준수하고, 적절한 테스트를 작성하며, 코드 생성 시 흔한 문제를 피할 수 있도록 도와줍니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상을 사용하는 Laravel 10, 11, 12 애플리케이션에서 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성(dev dependency)으로 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후, 대화형 설치 프로그램을 아래와 같이 실행합니다:

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지한 뒤, 프로젝트에 적합한 기능을 선택적으로 활성화할 수 있게 합니다. Boost는 기존 프로젝트 컨벤션을 존중하며, 기본적으로 스타일에 관한 의견을 강제하지 않습니다.

> [!NOTE]
> Boost에 대한 자세한 내용은 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
#### 커스텀 AI 가이드라인 추가

사용자만의 AI 가이드라인을 Laravel Boost에 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. Boost 설치 시 이 파일들도 함께 적용됩니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 Laravel 애플리케이션을 생성하셨다면, 다음으로 무엇을 학습할지 고민이 될 수 있습니다. 우선 아래 문서들을 통해 Laravel의 핵심 동작 방식을 익혀보는 것을 강력히 권장합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

여러분이 Laravel을 사용하려는 방식에 따라 앞으로의 여정이 달라집니다. Laravel에는 다양한 활용 방법이 있으며, 아래에서는 대표적인 두 가지 용도를 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel (Laravel the Full Stack Framework)

Laravel을 풀스택 프레임워크로 사용할 수 있습니다. 여기서 풀스택이란, Laravel이 요청을 라우팅하고, [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com)와 같은 SPA 하이브리드 기술로 프론트엔드를 렌더링하는 것을 의미합니다. 일반적으로 Laravel을 사용하는 가장 보편적이고 생산적인 방법입니다.

이렇게 사용하려면, [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 살펴보세요. 그리고 커뮤니티 패키지인 [Livewire](https://livewire.laravel.com)나 [Inertia](https://inertiajs.com)도 관심 있게 볼 만합니다. 이 패키지들은 JavaScript 기반 싱글 페이지 애플리케이션의 UI 장점을 그대로 누리면서 Laravel을 풀스택 프레임워크로 활용할 수 있게 도와줍니다.

풀스택 프레임워크로 Laravel을 사용할 경우, [Vite](/docs/12.x/vite)를 이용해 CSS/JavaScript를 직접 빌드하는 법도 꼭 익혀두시길 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하려면 공식 [스타터 키트](/docs/12.x/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel (Laravel the API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 앱을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 앱의 API 백엔드로 Laravel을 활용할 수 있습니다. 이 때 Laravel은 [인증](/docs/12.x/sanctum)과 데이터 저장/조회, 큐, 이메일, 알림 등 강력한 서비스들을 제공합니다.

이렇게 사용할 경우, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 문서를 꼭 읽어보시기 바랍니다.