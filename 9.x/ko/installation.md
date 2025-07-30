# 설치 (Installation)

- [Laravel 만나기](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [첫 번째 Laravel 프로젝트](#your-first-laravel-project)
- [Laravel & Docker](#laravel-and-docker)
    - [macOS에서 시작하기](#getting-started-on-macos)
    - [Windows에서 시작하기](#getting-started-on-windows)
    - [Linux에서 시작하기](#getting-started-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [초기 구성](#initial-configuration)
    - [환경 기반 구성](#environment-based-configuration)
    - [데이터베이스 & 마이그레이션](#databases-and-migrations)
- [다음 단계](#next-steps)
    - [Laravel, 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [Laravel, API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나기 (Meet Laravel)

Laravel은 표현력이 뛰어나고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 구축하기 위한 구조와 출발점을 제공하며, 여러분은 멋진 무언가를 만드는 데 집중할 수 있도록 세부 사항을 처리해줍니다.

Laravel은 완전한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

PHP 웹 프레임워크 사용이 처음이든 수년의 경험이 있든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫 발을 내딛도록 도와드리거나, 이미 쌓은 전문성을 한 단계 끌어올릴 수 있도록 지원합니다. 여러분이 어떤 프로젝트를 만들지 기대가 큽니다.

> [!NOTE]
> Laravel이 처음이신가요? 프레임워크를 체험하며 첫 Laravel 애플리케이션을 만드는 과정을 안내하는 [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인해보세요.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 만들 때 선택할 수 있는 다양한 도구와 프레임워크가 있습니다. 하지만 우리는 Laravel이 현대적이고 풀스택 웹 애플리케이션을 만들기에 가장 좋은 선택이라고 믿습니다.

#### 진보적인 프레임워크

Laravel을 "진보적(progressive)"이라고 부르는 이유는, Laravel이 여러분과 함께 성장한다는 뜻입니다. 웹 개발에 첫걸음을 내딛는 분이라면, 방대한 문서, 가이드, [영상 튜토리얼](https://laracasts.com)이 어려움 없이 배울 수 있도록 도와줍니다.

반대로 경력 많은 개발자에게는 [의존성 주입](/docs/9.x/container), [단위 테스트](/docs/9.x/testing), [큐](/docs/9.x/queues), [실시간 이벤트](/docs/9.x/broadcasting) 등 풍부하고 강력한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션 구축에 최적화되어 있으며, 기업용 고부하 환경도 거뜬히 처리할 수 있도록 준비되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 확장성이 뛰어납니다. PHP의 확장 친화적 특성과 Laravel 내부에서 지원하는 빠른 분산 캐시 시스템인 Redis 덕분에, Laravel을 수평적으로 확장하는 것이 매우 간편합니다. 실제로 수억 건의 요청을 한 달에 처리하는 규모로 Laravel 애플리케이션을 확장한 사례도 있습니다.

더 큰 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼을 통해 AWS의 최신 서버리스 기술로 거의 무한에 가까운 규모로 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계에서 가장 뛰어난 패키지들을 결합해 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 아울러 전 세계 수많은 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있을지도 모릅니다.

<a name="your-first-laravel-project"></a>
## 첫 번째 Laravel 프로젝트 (Your First Laravel Project)

첫 Laravel 프로젝트를 만들기 전에, 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인해야 합니다. macOS에서 개발한다면 PHP와 Composer를 [Homebrew](https://brew.sh/)를 통해 설치할 수 있습니다. 또한 [Node와 NPM 설치](https://nodejs.org)를 권장합니다.

PHP와 Composer 설치를 마친 후, Composer의 `create-project` 명령어를 통해 새로운 Laravel 프로젝트를 만들 수 있습니다:

```nothing
composer create-project laravel/laravel:^9.0 example-app
```

또는, Composer로 전역에 Laravel 인스톨러를 설치하여 새 프로젝트를 만들 수도 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트가 생성되면, Laravel의 Artisan CLI `serve` 명령어로 로컬 개발 서버를 시작하세요:

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버를 시작하면, 웹 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다. 그다음으로 [Laravel 생태계의 다음 단계로 나아갈 준비](#next-steps)가 되었으며, 물론 [데이터베이스 설정](#databases-and-migrations)도 진행할 수 있습니다.

> [!NOTE]
> 빠르게 Laravel 애플리케이션 개발을 시작하고 싶다면, [스타터 킷](/docs/9.x/starter-kits) 중 하나를 사용해보세요. Laravel 스타터 킷은 새로운 애플리케이션을 위한 백엔드와 프론트엔드 인증 구조를 제공합니다.

<a name="laravel-and-docker"></a>
## Laravel & Docker

Laravel 사용자는 운영체제에 상관없이 쉽게 시작할 수 있길 바랍니다. 그래서 로컬 머신에서 Laravel 프로젝트를 개발하고 실행하는 다양한 옵션이 있습니다. 나중에 살펴볼 수도 있지만, Laravel은 [Docker](https://www.docker.com)를 이용해 Laravel 프로젝트를 실행하는 기본 내장 솔루션인 [Sail](/docs/9.x/sail)을 제공합니다.

Docker는 애플리케이션과 서비스를 로컬 머신에 설치된 소프트웨어나 설정과 충돌하지 않는 작고 가벼운 '컨테이너' 내에서 실행하는 도구입니다. 따라서 로컬에 웹 서버나 데이터베이스 등 복잡한 개발 도구를 직접 설치하거나 설정할 필요가 없습니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용할 수 있는 가벼운 커맨드 라인 인터페이스입니다. Sail은 Docker 경험이 없더라도 PHP, MySQL, Redis를 사용해 Laravel 애플리케이션을 구축할 수 있는 좋은 출발점을 제공합니다.

> [!NOTE]
> 이미 Docker 전문가라면 걱정하지 마세요! Sail은 Laravel에 포함된 `docker-compose.yml` 파일을 통해 모든 설정을 자유롭게 수정할 수 있습니다.

<a name="getting-started-on-macos"></a>
### macOS에서 시작하기

Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 이미 설치했다면, 간단한 터미널 명령어를 통해 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어, "example-app"이라는 디렉토리명으로 새 Laravel 애플리케이션을 생성하려면 터미널에서 아래 명령어를 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

URL 내의 "example-app"은 원하는 이름으로 변경할 수 있으며, 애플리케이션 이름에는 영문, 숫자, 대시, 밑줄만 포함되어야 합니다. 실행한 위치 내에 Laravel 애플리케이션 디렉토리가 생성됩니다.

Sail 설치는 로컬에서 애플리케이션 컨테이너를 빌드하는 데 몇 분이 걸릴 수 있습니다.

프로젝트 생성이 완료되면, 프로젝트 디렉토리로 이동해 Laravel Sail을 실행하세요. Sail은 Laravel의 기본 Docker 설정과 상호작용하는 간단한 커맨드 라인 인터페이스입니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션 Docker 컨테이너가 시작되면, 웹 브라우저에서 http://localhost 로 애플리케이션에 접근할 수 있습니다.

> [!NOTE]
> Laravel Sail에 대해 더 알고 싶다면, [공식 문서](/docs/9.x/sail)를 참고하세요.

<a name="getting-started-on-windows"></a>
### Windows에서 시작하기

Windows에서 새 Laravel 애플리케이션을 만들기 전에 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치해야 합니다. 그다음 Windows Subsystem for Linux 2(WSL2)가 설치 및 활성화되어 있는지 확인하세요. WSL은 Windows 10에서 리눅스 실행 파일을 natively 실행할 수 있도록 해줍니다. WSL2 설치 및 활성화 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]
> WSL2 설치 및 활성화 후에는 Docker Desktop이 [WSL2 백엔드를 사용하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 반드시 확인하세요.

준비가 되면 첫 번째 Laravel 프로젝트를 만들 수 있습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 열고 WSL2 리눅스 환경에서 새 터미널 세션을 시작하세요. 그다음 간단한 터미널 명령어로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어, "example-app"이라는 디렉토리에 Laravel 애플리케이션을 생성하려면 다음 명령어를 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app"은 원하는 이름으로 변경할 수 있으며, 이름에는 영문, 숫자, 대시, 밑줄만 허용됩니다. 실행한 위치 내에 Laravel 애플리케이션 디렉토리가 만들어집니다.

Sail 설치는 컨테이너 빌드에 몇 분 소요될 수 있습니다.

프로젝트 생성 후, 프로젝트 디렉토리로 이동해 Laravel Sail을 시작하세요. Sail은 Laravel의 기본 Docker 설정에 편리하게 접근할 수 있는 커맨드 라인 도구입니다:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 시작되면 웹 브라우저에서 http://localhost 주소로 접근할 수 있습니다.

> [!NOTE]
> 더 자세한 Laravel Sail 학습은 [공식 문서](/docs/9.x/sail)를 참고하세요.

#### WSL2 내 개발하기

WSL2에 생성된 Laravel 애플리케이션 파일을 수정하려면, Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 원격 개발을 위한 공식 확장인 [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 확장 프로그램을 사용하는 것을 권장합니다.

이 툴들이 설치된 후, Windows Terminal에서 애플리케이션 루트 디렉토리로 가서 `code .` 명령어를 실행하면 해당 프로젝트를 바로 열 수 있습니다.

<a name="getting-started-on-linux"></a>
### Linux에서 시작하기

Linux에서 개발하며 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면 간단한 터미널 명령어로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어, "example-app"이라는 이름으로 새 Laravel 애플리케이션을 생성하려면 터미널에서 다음 명령어를 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

이름은 원하는 대로 변경할 수 있으나 영문, 숫자, 대시, 밑줄만 허용됩니다. 현재 위치에 Laravel 프로젝트 디렉토리가 만들어집니다.

Sail의 애플리케이션 컨테이너 빌드는 몇 분이 걸릴 수 있습니다.

프로젝트 생성 완료 후 디렉토리로 이동하여 다음 명령으로 Laravel Sail을 시작합니다:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너들이 실행되면, 브라우저에서 http://localhost 로 접근할 수 있습니다.

> [!NOTE]
> Laravel Sail에 대해 더 알고 싶다면 [공식 문서](/docs/9.x/sail)를 살펴보세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 사용해 새 Laravel 애플리케이션을 생성할 때 URL의 `with` 쿼리 문자열 변수로 `docker-compose.yml`에 포함할 서비스를 선택할 수 있습니다. 사용 가능한 서비스는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailpit` 등입니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

특정 서비스를 지정하지 않으면 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`이 포함됩니다.

또한 URL에 `devcontainer` 파라미터를 추가하면 기본 [Devcontainer](/docs/9.x/sail#using-devcontainers) 설정을 설치하도록 지시할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="initial-configuration"></a>
## 초기 구성 (Initial Configuration)

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 문서가 작성되어 있으니 자유롭게 살펴보며 어떤 옵션들이 있는지 익혀보세요.

Laravel은 기본 설정 상태에서 추가 구성이 거의 필요하지 않아 바로 개발을 시작할 수 있습니다. 다만 `config/app.php` 파일과 그 문서를 검토해보는 것을 권장합니다. 이 파일에는 애플리케이션에 맞게 바꿀 수 있는 `timezone`, `locale` 같은 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 구성

Laravel의 많은 구성 옵션 값은 로컬 머신에서 실행할 때와 프로덕션 서버에서 실행할 때 다를 수 있으므로, 중요한 구성 값을 애플리케이션 루트에 있는 `.env` 파일로 관리합니다.

`.env` 파일은 여러 개발자 또는 서버가 각기 다른 환경 구성을 가질 수 있기 때문에 소스 제어에 포함하지 않아야 합니다. 또한, 만약 침입자가 소스 제어 저장소에 접근한다면 민감한 인증 정보가 노출될 위험이 있습니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 구성에 대한 더 자세한 내용은 [전체 구성 문서](/docs/9.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 & 마이그레이션

Laravel 애플리케이션을 만들었으니 데이터를 저장할 데이터베이스 설정이 필요할 것입니다. 기본적으로 `.env` 파일은 Laravel이 MySQL 데이터베이스(`127.0.0.1`)와 연동하도록 설정되어 있습니다. macOS에서 MySQL, Postgres, Redis를 로컬에 설치할 필요가 있다면, [DBngin](https://dbngin.com/)을 이용하면 편리합니다.

MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수 있습니다. SQLite는 작고 빠르며 독립적인 데이터베이스 엔진입니다. SQLite를 사용하려면, `.env` 파일에서 데이터베이스 드라이버를 `sqlite`로 변경하고 다른 데이터베이스 설정은 삭제하세요:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite를 설정한 뒤, 애플리케이션의 [데이터베이스 마이그레이션](/docs/9.x/migrations)을 실행하면 데이터베이스 테이블이 생성됩니다:

```shell
php artisan migrate
```

만약 애플리케이션용 SQLite 데이터베이스 파일이 없다면, Laravel이 생성 여부를 물어봅니다. 일반적으로 `database/database.sqlite` 위치에 파일이 만들어집니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 프로젝트를 생성했으니, 이제 무엇을 배우면 좋을지 고민될 수 있습니다. 우선 Laravel이 어떻게 동작하는지 잘 이해하기 위해 다음 문서들을 익히는 것을 강력히 권장합니다:

<div class="content-list" markdown="1">

- [요청 수명주기](/docs/9.x/lifecycle)
- [구성](/docs/9.x/configuration)
- [디렉터리 구조](/docs/9.x/structure)
- [프론트엔드](/docs/9.x/frontend)
- [서비스 컨테이너](/docs/9.x/container)
- [파사드](/docs/9.x/facades)

</div>

Laravel을 어떻게 활용할지에 따라 다음 배우게 될 내용도 달라질 것입니다. 크게 두 가지 주요 사용 사례를 아래에서 소개합니다.

> [!NOTE]
> Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 프레임워크를 직접 체험하며 첫 번째 애플리케이션을 만드는 과정을 권장합니다.

<a name="laravel-the-fullstack-framework"></a>
### Laravel, 풀스택 프레임워크 (Laravel The Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란, Laravel을 요청을 라우팅하고 [Blade 템플릿](/docs/9.x/blade) 혹은 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 렌더링하는 데 사용하는 것을 의미합니다. 이것이 가장 흔한 Laravel 사용 방식이며, 가장 생산적인 방식이라고 생각합니다.

이러한 목적이라면 [프론트엔드 개발](/docs/9.x/frontend), [라우팅](/docs/9.x/routing), [뷰](/docs/9.x/views), [Eloquent ORM](/docs/9.x/eloquent) 문서를 참고하세요. 또한 [Livewire](https://laravel-livewire.com)와 [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지에 관심을 가져보세요. 이들 패키지는 Laravel을 풀스택 프레임워크로 사용하면서 싱글 페이지 자바스크립트 애플리케이션이 제공하는 UI 혜택을 누릴 수 있게 해줍니다.

풀스택으로 Laravel을 활용한다면, [Vite](/docs/9.x/vite)를 사용해 애플리케이션의 CSS와 자바스크립트를 컴파일하는 방법도 배워보길 권장합니다.

> [!NOTE]
> 빠르게 프로젝트를 시작하고 싶다면, 공식 [애플리케이션 스타터 킷](/docs/9.x/starter-kits)을 확인해보세요.

<a name="laravel-the-api-backend"></a>
### Laravel, API 백엔드 (Laravel The API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용하는 경우를 생각할 수 있습니다. 이 경우 Laravel은 [인증](/docs/9.x/sanctum), 데이터 저장/조회 역할을 담당하는 한편, 큐, 이메일, 알림 등 Laravel의 강력한 기능을 동시에 활용할 수 있습니다.

이러한 목적이라면 [라우팅](/docs/9.x/routing), [Laravel Sanctum](/docs/9.x/sanctum), [Eloquent ORM](/docs/9.x/eloquent) 문서들을 참고하세요.

> [!NOTE]
> Laravel 백엔드와 Next.js 프론트엔드 개발을 빠르게 시작하고 싶다면, Laravel Breeze가 [API 스택](/docs/9.x/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 제공합니다. 몇 분 만에 시작할 수 있습니다.