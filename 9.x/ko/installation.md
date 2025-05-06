# 설치

- [Laravel 만나기](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [나만의 첫 Laravel 프로젝트](#your-first-laravel-project)
- [Laravel & Docker](#laravel-and-docker)
    - [macOS에서 시작하기](#getting-started-on-macos)
    - [Windows에서 시작하기](#getting-started-on-windows)
    - [Linux에서 시작하기](#getting-started-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 & 마이그레이션](#databases-and-migrations)
- [다음 단계](#next-steps)
    - [Laravel, 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [Laravel, API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나기

Laravel은 표현력 있고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 여러분이 세부 사항에 신경 쓰지 않고 놀라운 것을 만드는 데 집중할 수 있게 해줍니다.

Laravel은 놀라운 개발자 경험을 제공하면서도, 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등 다양한 강력한 기능을 제공합니다.

PHP 웹 프레임워크가 처음이든, 수년간의 경험이 있든, Laravel은 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛는 분들을 돕거나, 여러분의 전문성을 한 단계 끌어올리는 데 도움을 드릴 수 있습니다. 여러분이 무엇을 만들지 기대가 됩니다.

> **참고**  
> Laravel이 처음이신가요? [Laravel 부트캠프](https://bootcamp.laravel.com)에서 첫 Laravel 애플리케이션을 만들어보며 프레임워크를 직접 체험해보세요.

<a name="why-laravel"></a>
### 왜 Laravel인가?

웹 애플리케이션 개발 시 사용할 수 있는 다양한 도구와 프레임워크들이 있습니다. 하지만, 저희는 Laravel이 최신 풀스택 웹 애플리케이션을 구축하기에 최고의 선택이라고 믿습니다.

#### 점진적인 프레임워크

Laravel은 “점진적(progressive)” 프레임워크라고 부릅니다. 그 의미는, 사용자의 성장과 함께 Laravel도 성장한다는 뜻입니다. 웹 개발에 처음 입문하신 분이라면, 방대한 문서, 가이드, [비디오 튜토리얼](https://laracasts.com)을 통해 부담 없이 학습할 수 있습니다.

이미 숙련된 개발자라면, Laravel은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 전문적인 웹 애플리케이션 개발에 바로 적용 가능한 강력한 도구들을 제공합니다. Laravel은 엔터프라이즈 환경의 대규모 작업을 다룰 수 있도록 세밀하게 조율되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화성 및 Redis와 같은 빠른 분산 캐시 시스템에 대한 기본 지원 덕분에, Laravel을 이용하면 수평 확장이 정말 쉽습니다. 실제로, Laravel 애플리케이션은 월 수억 건의 요청도 손쉽게 처리할 수 있습니다.

극한의 확장이 필요하신가요? [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 이용하면 AWS의 최신 서버리스 기술에서 Laravel 애플리케이션을 거의 무한에 가까운 규모로 실행할 수 있습니다.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계 내 최고의 패키지들을 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 우수한 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해왔습니다. 어쩌면 여러분도 Laravel 기여자가 될지도 모릅니다.

<a name="your-first-laravel-project"></a>
## 나만의 첫 Laravel 프로젝트

처음 Laravel 프로젝트를 생성하기 전에, 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있어야 합니다. macOS에서 개발하는 경우 [Homebrew](https://brew.sh/)로 PHP와 Composer를 설치할 수 있습니다. 추가로 [Node와 NPM 설치](https://nodejs.org)도 추천합니다.

PHP와 Composer가 설치된 후, Composer의 `create-project` 명령어를 이용해 새 Laravel 프로젝트를 생성할 수 있습니다:

```nothing
composer create-project laravel/laravel:^9.0 example-app
```

또는, Composer로 Laravel 인스톨러를 전역 설치한 뒤 새 프로젝트를 생성할 수도 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트가 생성된 후, Laravel의 Artisan CLI `serve` 명령어로 로컬 개발 서버를 시작합니다:

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버가 시작되면, 웹 브라우저에서 `http://localhost:8000`을 통해 애플리케이션에 접속할 수 있습니다. 이제 [Laravel 생태계에서 다음 단계를 진행](#next-steps)할 준비가 되었습니다. 물론, [데이터베이스를 설정](#databases-and-migrations)할 수도 있습니다.

> **참고**  
> Laravel 애플리케이션 개발을 더 빠르게 시작하고 싶다면, [스타터 키트](/docs/{{version}}/starter-kits) 사용을 고려해보세요. Laravel 스타터 키트는 새 Laravel 애플리케이션에 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="laravel-and-docker"></a>
## Laravel & Docker

여러분이 선호하는 운영체제와 상관없이 Laravel을 쉽게 시작할 수 있도록, 로컬 머신에서 Laravel 프로젝트를 개발 및 실행하는 여러 옵션이 준비되어 있습니다. 다양한 옵션을 추후 탐색하실 수도 있지만, Laravel은 내장 솔루션인 [Sail](/docs/{{version}}/sail)을 통해 [Docker](https://www.docker.com)를 이용한 개발 환경을 손쉽게 제공합니다.

Docker는 각 애플리케이션이나 서비스를 작은 경량 “컨테이너”로 실행해 로컬 머신의 소프트웨어나 설정과 충돌을 일으키지 않도록 해줍니다. 즉, 웹 서버나 데이터베이스 등 복잡한 개발 도구를 직접 설치할 필요가 없으며, [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용할 수 있도록 하는 경량 명령줄 인터페이스입니다. Docker 경험이 없어도 PHP, MySQL, Redis를 활용한 Laravel 애플리케이션 구축을 손쉽게 시작할 수 있습니다.

> **참고**  
> 이미 Docker 전문가이신가요? 걱정하지 마세요! Sail 관련 모든 것은 Laravel에 포함된 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이즈할 수 있습니다.

<a name="getting-started-on-macos"></a>
### macOS에서 시작하기

Mac에서 개발 중이며 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 터미널 한 줄 명령어로 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어, “example-app” 디렉터리에 새 Laravel 애플리케이션을 생성하려면 다음 명령어를 입력하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론 위 URL에서 “example-app” 이름은 원하는 대로 바꿀 수 있습니다. 단, 앱 이름에는 알파벳, 숫자, - (대시), _ (언더스코어)만 사용할 수 있습니다. 이 명령어를 실행한 디렉터리 내에 Laravel 애플리케이션이 생성됩니다.

Sail 설치 및 컨테이너 빌드는 몇 분이 걸릴 수 있습니다.

프로젝트 생성 후, 앱 디렉터리로 이동해 Laravel Sail을 실행하세요. Sail은 Laravel 기본 Docker 설정과 상호작용할 수 있는 간단한 CLI를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 모두 구동되면, 웹 브라우저에서 http://localhost 를 통해 애플리케이션에 접속할 수 있습니다.

> **참고**  
> Laravel Sail에 대해 더 자세히 알고 싶다면, [공식 문서](/docs/{{version}}/sail)를 참조하세요.

<a name="getting-started-on-windows"></a>
### Windows에서 시작하기

Windows 머신에서 새 Laravel 애플리케이션을 만들기 전에 [Docker Desktop](https://www.docker.com/products/docker-desktop) 설치를 먼저 진행하세요. 그리고 Windows Subsystem for Linux 2(WSL2)가 설치 및 활성화되어 있는지 확인해야 합니다. WSL을 사용하면 Windows 10에서 리눅스 바이너리 실행이 가능합니다. WSL2 설치 방법은 Microsoft의 [개발 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 참고하세요.

> **참고**  
> WSL2 설치 후, Docker Desktop이 [WSL2 백엔드로 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인해야 합니다.

이제 첫 Laravel 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 열고, WSL2 리눅스 터미널 세션을 시작하세요. 그런 다음, 아래의 명령어로 새 Laravel 프로젝트를 만드세요:

```shell
curl -s https://laravel.build/example-app | bash
```

앱 이름은 원하시는 대로 변경할 수 있으며, 알파벳, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 명령을 실행한 위치에 Laravel 앱 디렉터리가 생성됩니다.

Sail 설치와 컨테이너 빌드에는 몇 분 정도 소요될 수 있습니다.

프로젝트가 생성되면, 앱 디렉터리로 이동해 Laravel Sail을 실행합니다.

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 모두 구동되면, 웹 브라우저에서 http://localhost 에 접속할 수 있습니다.

> **참고**  
> Laravel Sail에 대해 더 자세히 알고 싶다면, [공식 문서](/docs/{{version}}/sail)를 참고하세요.

#### WSL2 환경에서 개발하기

WSL2에서 생성한 Laravel 애플리케이션 파일을 편집해야 합니다. 이를 위해, Microsoft의 [Visual Studio Code](https://code.visualstudio.com)와 [원격 개발 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 사용하는 것을 권장합니다.

이 도구들이 설치되어 있다면, Windows Terminal을 통해 앱 루트 디렉터리에서 `code .` 명령어로 바로 프로젝트를 열 수 있습니다.

<a name="getting-started-on-linux"></a>
### Linux에서 시작하기

Linux에서 개발 중이며 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 터미널 한 줄로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어, “example-app” 디렉터리에 Laravel 앱을 만들려면 다음처럼 입력하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

앱 이름은 원하는 대로 변경할 수 있으나 알파벳, 숫자, 대시, 언더스코어만 허용됩니다. 실행한 위치에 Laravel 앱 디렉터리가 생성됩니다.

Sail 설치와 컨테이너 빌드에는 시간이 다소 소요될 수 있습니다.

프로젝트가 생성된 후, 디렉터리로 이동하여 Sail을 실행하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 모두 실행되면, 웹 브라우저에서 http://localhost 로 접속할 수 있습니다.

> **참고**  
> Laravel Sail에 대해 더 자세히 알고 싶다면, [공식 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 통해 새로운 Laravel 애플리케이션을 만들 때, `with` 쿼리 문자열 변수를 사용하여 새 애플리케이션의 `docker-compose.yml` 파일에 어떤 서비스들을 설정할지 선택할 수 있습니다. 사용 가능한 서비스로는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

명시적으로 설정하지 않으면, 기본 스택으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`이 구성됩니다.

또한, URL에 `devcontainer` 파라미터를 추가하여 기본 [Devcontainer](/docs/{{version}}/sail#using-devcontainers)를 설치하도록 Sail에 지시할 수 있습니다.

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="initial-configuration"></a>
## 초기 설정

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 주석이 붙어 있으니, 파일을 살펴보고 사용 가능한 설정 옵션에 익숙해지세요.

Laravel은 거의 추가 설정 없이 바로 개발을 시작할 수 있습니다. 자유롭게 개발을 시작하세요! 다만, `config/app.php` 파일과 해당 설명서를 확인해보는 것도 좋습니다. 이 파일에는 `timezone`과 `locale` 등 애플리케이션 특성에 맞게 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

Laravel의 많은 설정 값들은 애플리케이션이 로컬에서 실행 중인지, 프로덕션 웹 서버에서 실행 중인지에 따라 달라질 수 있습니다. 많은 주요 설정 값들은 애플리케이션 루트의 `.env` 파일에서 정의됩니다.

각 개발자 및 서버의 환경 설정이 서로 다를 수 있기 때문에 `.env` 파일은 소스 컨트롤에 커밋하지 마세요. 또한, 이 파일에 민감한 정보가 포함될 수 있어, 외부 침입자가 소스 리포지터리에 접근할 경우 보안 위험이 발생할 수 있습니다.

> **참고**  
> `.env` 파일 및 환경 기반 설정에 대해 더 알고 싶다면, [설정 문서 전체](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 & 마이그레이션

Laravel 애플리케이션을 만들었으니, 이제 데이터를 데이터베이스에 저장하고 싶으실 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 MySQL 데이터베이스를 사용하며, 데이터베이스는 `127.0.0.1`에서 접근하도록 되어 있습니다. macOS에서 MySQL, Postgres, Redis를 설치해야 한다면 [DBngin](https://dbngin.com/) 사용이 편리합니다.

로컬 머신에 MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수도 있습니다. SQLite는 작고, 빠르며, 독립 실행형 데이터베이스 엔진입니다. 시작하려면, `.env` 파일을 수정하여 Laravel의 `sqlite` 데이터베이스 드라이버를 사용하도록 설정하세요. 다른 데이터베이스 옵션들은 지워도 됩니다:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite 데이터베이스를 설정한 후, 애플리케이션의 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)를 실행해 데이터베이스 테이블을 생성할 수 있습니다:

```shell
php artisan migrate
```

애플리케이션용 SQLite 데이터베이스가 없다면, Laravel에서 생성 여부를 물어봅니다. 보통 이 데이터베이스 파일은 `database/database.sqlite`에 생성됩니다.

<a name="next-steps"></a>
## 다음 단계

Laravel 프로젝트를 만들었으니, 앞으로 무엇을 배우면 좋을지 궁금하실 수 있습니다. 먼저 추천드리는 것은 아래 문서를 읽어 Laravel의 작동 방식을 익히는 것입니다:

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [프론트엔드](/docs/{{version}}/frontend)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

Laravel을 어떻게 사용할지에 따라 앞으로의 학습 방향도 달라집니다. Laravel을 활용할 수 있는 다양한 방법 중, 여기에서는 대표적인 두 가지 사용 사례를 소개합니다.

> **참고**  
> Laravel이 처음이라면, [Laravel 부트캠프](https://bootcamp.laravel.com)에서 첫 애플리케이션을 직접 만들어보며 프레임워크를 경험해보세요.

<a name="laravel-the-fullstack-framework"></a>
### Laravel, 풀스택 프레임워크로 활용하기

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. “풀스택” 프레임워크란, Laravel을 사용하여 요청을 라우팅하고 [Blade 템플릿](/docs/{{version}}/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글페이지 하이브리드 기술로 프론트엔드를 렌더링할 수 있음을 의미합니다. 이는 Laravel을 사용하는 가장 일반적이면서 생산적인 방법입니다.

이 방식을 계획한다면, [프론트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 확인해보세요. 또한, [Livewire](https://laravel-livewire.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 흥미로울 것입니다. 이 패키지들을 이용하면 싱글페이지 자바스크립트 애플리케이션의 UI 이점을 그대로 누릴 수 있습니다.

풀스택 프레임워크로 Laravel을 활용한다면, [Vite](/docs/{{version}}/vite)를 이용해 CSS와 자바스크립트를 컴파일하는 방법도 꼭 익히시기 바랍니다.

> **참고**  
> 애플리케이션을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### Laravel, API 백엔드로 활용하기

Laravel은 자바스크립트 싱글페이지 애플리케이션 또는 모바일 앱의 API 백엔드로도 활용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 경우 Laravel은 [인증](/docs/{{version}}/sanctum), 데이터 저장/검색 서비스를 제공하면서, 큐, 이메일, 알림 등 강력한 서비스도 함께 사용할 수 있습니다.

이러한 목적으로 Laravel을 사용할 예정이라면, [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참조해보세요.

> **참고**  
> Laravel 백엔드와 Next.js 프론트엔드를 빠르게 구축하고 싶으시다면, Laravel Breeze가 [API 스택](/docs/{{version}}/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현체](https://github.com/laravel/breeze-next)를 제공하므로 몇 분 만에 시작할 수 있습니다.