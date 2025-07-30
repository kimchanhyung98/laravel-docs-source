# 설치 (Installation)

- [Laravel 소개](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치 프로그램 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 구성](#initial-configuration)
    - [환경 기반 구성](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 구성](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd](#herd-on-macos)
    - [Windows에서 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [Laravel 풀스택 프레임워크로서](#laravel-the-fullstack-framework)
    - [Laravel API 백엔드로서](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 소개 (Meet Laravel)

Laravel은 표현력이 풍부하고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하며, 이를 통해 세부 사항에 신경 쓰는 대신 정말 멋진 무언가를 만드는 데 집중할 수 있습니다.

Laravel은 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

PHP 웹 프레임워크를 처음 접하는 개발자든, 수년간 경험이 있는 개발자든, Laravel은 당신과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서의 첫 걸음을 돕고, 전문성을 한 단계 끌어올리는 데 힘을 보탤 것입니다. 여러분이 어떤 것을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 사용할 수 있는 여러 도구와 프레임워크가 있습니다. 하지만 우리는 Laravel이 현대적인 풀스택 웹 애플리케이션을 만드는데 가장 적합한 선택이라고 믿습니다.

#### 점진적 프레임워크

Laravel을 "점진적(progressive)" 프레임워크라고 부릅니다. 이는 Laravel이 사용자와 함께 성장한다는 의미입니다. 웹 개발에 첫 발을 내딛는 초보자라면, Laravel의 방대한 문서, 가이드, 그리고 [비디오 튜토리얼](https://laracasts.com)이 부담 없이 기본을 익힐 수 있도록 도와줍니다.

고급 개발자라면 Laravel은 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션 개발에 최적화되어 있으며, 기업 규모의 부하를 감당할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적 특성과 Redis 같은 빠르고 분산된 캐시 시스템에 대한 Laravel의 기본 지원 덕분에, Laravel로 수평 확장(horizontal scaling)을 하는 것이 매우 쉽습니다. 실제로 Laravel 애플리케이션은 월 수억 건의 요청도 무리 없이 처리할 수 있도록 확장된 사례가 있습니다.

더 큰 규모 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 거의 무한에 가까운 확장성을 누릴 수 있습니다.

#### 커뮤니티 기반 프레임워크

Laravel은 PHP 생태계의 최고 패키지를 결합하여 가장 강력하면서도 개발자 친화적인 프레임워크를 제공합니다. 게다가 전 세계 수천 명의 실력 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 당신도 Laravel 기여자가 될 수 있을지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel 설치 프로그램 설치 (Installing PHP and the Laravel Installer)

첫 Laravel 애플리케이션을 생성하기 전에, 로컬 컴퓨터에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel installer](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 그리고 애플리케이션의 프론트엔드 자산을 컴파일하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

PHP와 Composer가 로컬에 아직 없으면, 아래 명령어들을 통해 macOS, Windows, 또는 Linux에서 PHP, Composer, Laravel 설치 프로그램을 설치할 수 있습니다:

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

위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작하세요. `php.new`를 통해 설치한 PHP, Composer, Laravel 설치 프로그램 업데이트도 같은 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, 다음 명령으로 Composer를 통해 Laravel 설치 프로그램을 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 기능의 그래픽 PHP 설치 및 관리 환경을 원한다면, [Laravel Herd](#installation-using-herd)를 확인해 보세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel 설치 프로그램 설치가 완료되면, 새 Laravel 애플리케이션을 생성할 준비가 된 것입니다. Laravel 설치 프로그램은 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택하도록 안내합니다:

```shell
laravel new example-app
```

애플리케이션 생성이 끝나면, `dev` Composer 스크립트를 사용해 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다. 그 다음에는 [Laravel 생태계로의 다음 단계](#next-steps)를 시작하거나, [데이터베이스를 구성](#databases-and-migrations)할 수 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 손쉽게 시작하고 싶다면, 공식 [스타터 키트](/docs/12.x/starter-kits)를 사용하는 것을 고려해 보세요. 스타터 키트는 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 구성 (Initial Configuration)

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션마다 문서가 작성되어 있으므로, 파일을 살펴보며 어떤 옵션이 있는지 익혀두는 것이 좋습니다.

Laravel은 기본적으로 거의 추가 구성이 필요 없도록 설계되어 있습니다. 바로 개발을 시작할 수 있습니다! 다만 `config/app.php` 파일과 그 문서를 검토하면, `url`, `locale` 등 애플리케이션에 맞게 변경하고 싶은 옵션이 있을 수 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 구성 (Environment Based Configuration)

Laravel의 많은 구성 옵션은 애플리케이션이 로컬 환경에서 실행 중인지, 프로덕션 서버에서 실행 중인지에 따라 달라질 수 있으므로, 중요한 구성 값들은 애플리케이션 루트에 있는 `.env` 파일을 통해 정의됩니다.

`.env` 파일은 각 개발자나 서버마다 다른 환경 구성을 가질 수 있으므로 소스 관리에 커밋하지 않아야 합니다. 또한, 만약 외부 침입자가 소스 저장소에 접근할 경우 민감한 인증 정보가 노출되는 보안 위험이 있습니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 구성에 대한 자세한 내용은 전체 [구성 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

Laravel 애플리케이션을 생성했다면, 데이터를 저장할 데이터베이스를 설정하고 싶을 것입니다. 기본적으로 `.env` 구성 파일은 Laravel이 SQLite 데이터베이스와 상호작용하도록 지정되어 있습니다.

애플리케이션 생성 시 Laravel이 `database/database.sqlite` 파일을 생성하고 필요한 마이그레이션을 실행해 테이블을 만들었습니다.

MySQL이나 PostgreSQL 같은 다른 데이터베이스 드라이버를 사용하려면 `.env` 파일을 해당 데이터베이스에 맞게 수정해야 합니다. 예를 들어 MySQL을 사용하려면 `.env` 파일의 `DB_*` 변수들을 아래와 같이 설정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 사용한다면, 데이터베이스를 직접 생성한 후 애플리케이션의 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용하는 것을 추천합니다.

<a name="directory-configuration"></a>
### 디렉터리 구성 (Directory Configuration)

Laravel 애플리케이션은 항상 웹 서버가 설정한 "웹 디렉터리"의 루트에서 제공되어야 합니다. Laravel을 "웹 디렉터리"의 하위 디렉터리에서 제공하려고 하면 애플리케이션 내 민감한 파일이 노출될 위험이 있으니 주의하세요.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows용으로 제공되는 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd에는 PHP와 Nginx를 포함해 Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다.

Herd 설치 후 바로 Laravel 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등의 커맨드 라인 도구들도 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리 기능, 로컬 메일 뷰어, 로그 모니터링 등 강력한 기능을 추가합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd (Herd on macOS)

macOS에서 개발한다면, [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 PHP 버전을 자동으로 다운로드하며, 백그라운드에서 항상 [Nginx](https://www.nginx.com/)가 실행되도록 Mac을 구성합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "parked" 디렉터리를 지원합니다. 이 디렉터리에 있는 Laravel 애플리케이션은 자동으로 Herd에 의해 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 parked 디렉터리를 생성하며, 이 디렉터리 내의 Laravel 애플리케이션은 해당 디렉터리 이름을 이용한 `.test` 도메인에서 접근할 수 있습니다.

Herd 설치 후 새 Laravel 애플리케이션을 가장 빠르게 생성하는 방법은 Herd에 번들된 Laravel CLI를 이용하는 것입니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 parked 디렉터리와 PHP 설정을 관리할 수도 있습니다.

자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd (Herd on Windows)

Windows용 Herd 설치 프로그램은 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치 완료 후 Herd를 실행해 온보딩을 완료하고 처음으로 Herd UI에 접근할 수 있습니다.

Herd UI는 Herd 시스템 트레이 아이콘에서 왼쪽 클릭으로 열 수 있으며, 오른쪽 클릭 시 매일 필요한 모든 도구에 접근할 수 있는 빠른 메뉴가 나타납니다.

설치 과정에서 Herd는 홈 디렉터리 내 `%USERPROFILE%\Herd`에 "parked" 디렉터리를 생성합니다. 이 디렉터리에 있는 Laravel 애플리케이션은 자동으로 Herd에 의해 서비스되며, 디렉터리 이름을 사용한 `.test` 도메인에서 접근 가능합니다.

설치 후 새 Laravel 애플리케이션을 만들려면, 터미널(PowerShell)에서 아래 명령어를 순서대로 실행하면 됩니다:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 확인하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발할 때 어떤 코드 편집기를 사용해도 무방합니다. 가볍고 확장성이 좋은 편집기를 찾는다면, [VS Code](https://code.visualstudio.com)나 [Cursor](https://cursor.com)에 공식 [Laravel VS Code 확장](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 함께 사용하면, 구문 강조, 코드 스니펫, Artisan 명령어 통합, Eloquent 모델, 라우트, 미들웨어, 에셋, 설정, Inertia.js에 대한 스마트 자동완성 등 훌륭한 지원을 받을 수 있습니다.

JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)과 [Laravel Idea 플러그인](https://laravel-idea.com/)을 함께 사용하면, Laravel Pint, Larastan, Pest 등 Laravel 생태계를 폭넓게 지원합니다. Blade 템플릿, Eloquent 모델, 라우트, 뷰, 번역, 컴포넌트에 대한 스마트 자동완성은 물론, 강력한 코드 생성과 내비게이션 기능도 제공합니다.

클라우드 기반 개발 환경을 원한다면 [Firebase Studio](https://firebase.studio/)를 통해 브라우저에서 바로 Laravel 개발을 시작할 수 있습니다. 별도의 설정 없이 언제 어디서나 Laravel 애플리케이션을 빌드할 수 있습니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 생성했으니, 이후 무엇을 학습해야 할지 궁금할 것입니다. 가장 먼저, Laravel이 어떻게 동작하는지 익히기 위해 아래 문서들을 읽어보길 강력히 추천합니다:

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/12.x/lifecycle)
- [구성](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

Laravel을 어떻게 사용하고 싶은지에 따라 다음 학습 방향도 달라집니다. 여기서는 Laravel의 두 가지 주요 사용 사례를 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### Laravel 풀스택 프레임워크로서 (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란, Laravel이 요청 라우팅과 프론트엔드 렌더링을 [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술을 통해 처리한다는 뜻입니다. Laravel 프레임워크를 사용하는 가장 일반적이면서도 생산적인 방법입니다.

이 용도로 Laravel을 사용한다면, [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고하세요. 또한 [Livewire](https://livewire.laravel.com)나 [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지에도 관심을 가져보세요. 이 패키지들은 Laravel을 풀스택 프레임워크로 사용하면서도 싱글 페이지 자바스크립트 애플리케이션의 UI 이점을 누릴 수 있게 해줍니다.

Laravel을 풀스택 프레임워크로 쓴다면, 애플리케이션의 CSS와 자바스크립트를 컴파일하기 위한 [Vite](/docs/12.x/vite) 학습도 적극 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### Laravel API 백엔드로서 (Laravel the API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로도 사용할 수 있습니다. 예를 들어, Laravel을 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 활용할 수 있죠. 이 경우 Laravel은 애플리케이션의 [인증](/docs/12.x/sanctum)과 데이터 저장 및 조회 기능을 제공하는 한편, 큐, 이메일, 알림 등 Laravel의 강력한 서비스를 활용할 수 있습니다.

이 방법으로 Laravel을 사용하려면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고하세요.