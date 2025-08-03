# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 프로젝트 생성하기](#creating-a-laravel-project)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉토리 구성](#directory-configuration)
- [Sail을 이용한 도커 설치](#docker-installation-using-sail)
    - [macOS에서 Sail 사용하기](#sail-on-macos)
    - [Windows에서 Sail 사용하기](#sail-on-windows)
    - [Linux에서 Sail 사용하기](#sail-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀 스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

라라벨은 표현력이 풍부하고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하여, 개발자가 세부사항에 신경 쓰지 않고도 놀라운 것을 만드는 데 집중할 수 있도록 합니다.

라라벨은 훌륭한 개발자 경험을 제공하는 동시에, 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능들을 지원하도록 설계되었습니다.

PHP 웹 프레임워크에 익숙하지 않든, 수년간 경험이 있든 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛든, 전문성을 한 단계 끌어올리든 저희가 도와드리겠습니다. 여러분이 어떤 것을 만들지 기대됩니다.

> [!NOTE]  
> 라라벨이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 직접 라라벨 프레임워크를 체험하고 첫 라라벨 애플리케이션을 만드는 과정을 따라가 보세요.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 하지만 저희는 현대적인 풀스택 웹 애플리케이션 개발에 라라벨이 가장 좋은 선택이라고 믿습니다.

#### 점진적 프레임워크

라라벨을 “점진적(progressive)” 프레임워크라고 부릅니다. 이는 라라벨이 여러분과 함께 성장한다는 뜻입니다. 웹 개발을 처음 시작하는 분이라면, 방대한 문서와 가이드, 그리고 [비디오 튜토리얼](https://laracasts.com)을 통해 부담 없이 배울 수 있습니다.

경험 많은 시니어 개발자라면, 라라벨은 [의존성 주입](/docs/10.x/container), [단위 테스트](/docs/10.x/testing), [큐](/docs/10.x/queues), [실시간 이벤트](/docs/10.x/broadcasting) 등 강력한 도구를 제공합니다. 라라벨은 전문적인 웹 애플리케이션 구축에 최적화되어 있고, 엔터프라이즈급 작업 부하도 문제없이 처리할 수 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 우수한 확장성을 자랑합니다. PHP의 확장 친화적인 특성과 Redis 같은 빠르고 분산된 캐시 시스템을 내장 지원하는 덕분에, 라라벨로 손쉽게 수평 확장이 가능합니다. 실제로 라라벨 애플리케이션은 월간 수억 건의 요청을 무리 없이 처리해 왔습니다.

극단적인 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼을 통해 AWS의 최신 서버리스 기술 상에서 무한에 가까운 규모로 라라벨 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 중심의 프레임워크

라라벨은 PHP 생태계 최고의 패키지들을 결합하여 가장 강력하며 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 언젠가는 여러분도 라라벨 기여자가 될지 누가 알겠습니까?

<a name="creating-a-laravel-project"></a>
## 라라벨 프로젝트 생성하기 (Creating a Laravel Project)

첫 라라벨 프로젝트를 만들기 전에, 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있어야 합니다. macOS에서 개발 중이라면 [Laravel Herd](https://herd.laravel.com)를 통해 몇 분 만에 PHP와 Composer를 설치할 수 있습니다. 추가로 [Node와 NPM 설치](https://nodejs.org)를 권장합니다.

PHP와 Composer가 설치되면 Composer의 `create-project` 명령어로 새 라라벨 프로젝트를 만들 수 있습니다:

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

또는 전역으로 [Laravel installer](https://github.com/laravel/installer)를 Composer를 통해 설치하고, 아래 명령어로 새 프로젝트를 만들 수도 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트가 생성되면 Laravel Artisan의 `serve` 명령어로 로컬 개발 서버를 실행하세요:

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버가 시작되면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 으로 애플리케이션에 접속할 수 있습니다. 이제 [라라벨 생태계에서 다음 단계를 진행할 준비가 되었습니다](#next-steps). 물론, [데이터베이스 설정](#databases-and-migrations)도 할 수 있습니다.

> [!NOTE]  
> 라라벨 애플리케이션 개발을 빠르게 시작하고 싶다면 [스타터 키트](/docs/10.x/starter-kits)를 사용해 보세요. 스타터 키트는 백엔드와 프론트엔드 인증 기본 구조를 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크 관련 설정 파일은 모두 `config` 디렉터리에 저장됩니다. 각 옵션은 문서화되어 있으니 자유롭게 살펴보면서 어떤 옵션들이 있는지 익히세요.

라라벨은 기본적으로 별다른 추가 설정이 거의 필요 없으며, 바로 개발을 시작할 수 있습니다! 다만, `config/app.php` 파일과 문서를 검토해 보기를 권합니다. 이 파일에는 애플리케이션에 맞게 변경할 수 있는 `timezone`(시간대)이나 `locale`(지역) 같은 몇 가지 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 많은 설정 옵션 값은 애플리케이션이 로컬 환경인지, 아니면 운영 환경인지에 따라 달라질 수 있으므로, 중요한 설정 값들은 애플리케이션 루트에 위치한 `.env` 파일로 정의합니다.

`.env` 파일은 각 개발자 또는 서버마다 환경 구성이 다르기 때문에 절대로 소스 관리 시스템에 포함해서는 안 됩니다. 또한, `.env` 파일을 공개 소스 관리에 포함하면 보안상 민감한 인증 정보가 노출될 위험이 있습니다.

> [!NOTE]  
> `.env` 파일 및 환경 기반 설정에 대한 더 자세한 내용은 [전체 설정 문서](/docs/10.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션 (Databases and Migrations)

애플리케이션을 만들었으니 데이터를 저장할 데이터베이스도 필요할 것입니다. 기본적으로, 애플리케이션의 `.env` 파일에서는 라라벨이 MySQL 데이터베이스와 통신하며 `127.0.0.1`에서 연결한다고 지정되어 있습니다.

> [!NOTE]  
> macOS에서 MySQL, Postgres, Redis를 로컬에 설치해야 할 경우 [DBngin](https://dbngin.com/) 사용을 고려해 보세요.

로컬에 MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html)를 사용할 수도 있습니다. SQLite는 작고 빠르며 독립적인 데이터베이스 엔진입니다. 시작하려면 `.env` 파일에서 데이터베이스 드라이버를 `sqlite`로 변경하고, 다른 데이터베이스 관련 설정은 모두 제거하세요:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite 데이터베이스를 설정한 후에는, 애플리케이션의 [데이터베이스 마이그레이션](/docs/10.x/migrations)을 실행하여 데이터베이스 테이블을 생성할 수 있습니다:

```shell
php artisan migrate
```

SQLite 데이터베이스 파일이 존재하지 않으면 라라벨이 생성할지 물어봅니다. 보통 SQLite 데이터베이스 파일은 `database/database.sqlite` 경로에 생성됩니다.

<a name="directory-configuration"></a>
### 디렉토리 구성 (Directory Configuration)

라라벨 애플리케이션은 항상 웹 서버가 설정한 "웹 디렉터리"의 루트(root)에서 서비스되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨을 서비스하려고 해서는 안 됩니다. 그렇게 하면 애플리케이션 내 민감한 파일들이 노출될 수 있습니다.

<a name="docker-installation-using-sail"></a>
## Sail을 이용한 도커 설치 (Docker Installation Using Sail)

운영 체제에 관계없이 라라벨을 쉽게 시작할 수 있도록 다양한 로컬 개발 옵션이 있습니다. 그 중 라라벨은 [Docker](https://www.docker.com)를 이용해 라라벨 프로젝트를 실행하는 내장 솔루션인 [Sail](/docs/10.x/sail)을 제공합니다.

Docker는 애플리케이션과 서비스를 작은 경량화된 "컨테이너" 안에서 실행하여, 로컬 머신에 설치된 소프트웨어나 설정과 충돌하지 않도록 해줍니다. 즉, 로컬에 복잡한 웹 서버나 데이터베이스 설치를 신경 쓸 필요 없이 쉽게 개발 환경을 구축할 수 있습니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop) 만 설치하면 됩니다.

라라벨 Sail은 라라벨 기본 도커 설정을 조작하기 위한 경량 명령어 인터페이스입니다. PHP, MySQL, Redis를 사용해 라라벨 애플리케이션을 구축하는 데 아주 좋은 출발점이며, Docker 경험이 없어도 사용할 수 있습니다.

> [!NOTE]  
> Docker 전문가라면 걱정 마세요! Sail은 라라벨에 포함된 `docker-compose.yml` 파일을 통해 모든 설정을 자유롭게 변경할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail 사용하기 (Sail on macOS)

Mac에서 개발 중이고 이미 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 설치되어 있다면, 단순한 터미널 명령어로 새 라라벨 프로젝트를 생성할 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 라라벨 애플리케이션을 만들려면 다음 명령어를 터미널에서 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론 URL 내 "example-app"은 원하는 이름으로 바꿀 수 있습니다. 단, 이름에는 영문자, 숫자, 대시, 언더스코어만 포함해야 합니다. 라라벨 애플리케이션 디렉터리는 이 명령어를 실행한 곳 아래에 생성됩니다.

Sail 설치는 로컬에서 Sail 애플리케이션 컨테이너가 빌드되는 동안 몇 분 정도 걸릴 수 있습니다.

프로젝트가 생성되면, 애플리케이션 디렉터리로 이동하여 라라벨 Sail을 시작하세요. Sail은 라라벨 기본 도커 구성을 다루기 위한 간단한 커맨드라인 도구입니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션 도커 컨테이너가 시작되면 브라우저에서 http://localhost 로 접속해 애플리케이션을 확인할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 배우고 싶으면 [전체 문서](/docs/10.x/sail)를 참고하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail 사용하기 (Sail on Windows)

Windows에서 새 라라벨 애플리케이션을 만들기 전에, [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치해야 합니다. 또한 Windows Subsystem for Linux 2 (WSL2)가 설치 및 활성화되어 있어야 합니다. WSL은 Windows 10에서 리눅스 바이너리 실행을 지원합니다. 설치 및 활성화 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]  
> WSL2 설치 및 활성화 후에는 Docker Desktop이 [WSL2 백엔드를 사용하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인하세요.

이제 첫 라라벨 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행하여 WSL2 리눅스 환경 터미널 세션을 시작하세요. 그런 다음 다음 명령어로 새 라라벨 프로젝트를 생성할 수 있습니다. 예를 들어 "example-app" 폴더에 생성하려면 다음과 같이 입력:

```shell
curl -s https://laravel.build/example-app | bash
```

마찬가지로 "example-app" 이름은 원하는 대로 바꿀 수 있으나, 영숫자, 대시, 언더스코어만 허용됩니다. 애플리케이션 디렉터리는 명령어를 실행하는 위치 아래에 만들어집니다.

Sail의 애플리케이션 컨테이너가 빌드되는 데 몇 분이 걸릴 수 있습니다.

프로젝트 생성 후 애플리케이션 디렉터리로 이동하여 라라벨 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 실행되면 브라우저에서 http://localhost 를 열어 애플리케이션을 확인할 수 있습니다.

> [!NOTE]  
> Sail에 대해 더 알고 싶으면 [전체 문서](/docs/10.x/sail)를 참조하세요.

#### WSL2 내에서 개발하기

WSL2 내부에 생성된 라라벨 애플리케이션 파일을 수정할 수 있어야 합니다. 이를 위해, Microsoft의 [Visual Studio Code](https://code.visualstudio.com)와 [원격 개발(Remote Development)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 확장팩을 사용하기를 권장합니다.

이 도구들을 설치하면, Windows Terminal에서 애플리케이션 루트 디렉터리로 이동해 `code .` 명령어로 Visual Studio Code를 실행할 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail 사용하기 (Sail on Linux)

Linux에서 개발 중이고 이미 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있으면, 단순한 터미널 명령어로 새 라라벨 프로젝트를 만들 수 있습니다.

먼저, Docker Desktop for Linux를 사용 중이라면 다음 명령어를 실행하세요. 아니라면 이 단계는 건너뛰어도 됩니다:

```shell
docker context use default
```

그 다음, "example-app" 디렉터리에 새 라라벨 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app"은 원하는 프로젝트 이름으로 변경 가능하며, 영숫자, 대시, 언더스코어만 포함돼야 합니다. 프로젝트 디렉터리는 이 명령어를 실행한 경로 아래 생성됩니다.

Sail 애플리케이션 컨테이너 빌드에는 몇 분 정도 소요될 수 있습니다.

프로젝트 생성 후 애플리케이션 디렉터리로 이동하여 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 실행되면 http://localhost 로 접속해 애플리케이션을 확인할 수 있습니다.

> [!NOTE]  
> 더 자세한 내용은 Sail의 [전체 문서](/docs/10.x/sail)를 확인하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기 (Choosing Your Sail Services)

Sail을 통해 새 애플리케이션을 만들 때, `with` 쿼리 스트링 변수를 사용해 새 애플리케이션의 `docker-compose.yml` 파일에 포함할 서비스를 선택할 수 있습니다. 선택 가능한 서비스는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

서비스를 지정하지 않으면 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium` 스택이 설정됩니다.

또한 `devcontainer` 파라미터를 URL에 추가하면 기본 [Devcontainer](/docs/10.x/sail#using-devcontainers)도 설치하도록 지정할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발 시 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 다만, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 라라벨 및 생태계 전반에 대해 광범위한 지원을 제공하며, [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html)도 포함됩니다.

또한, 커뮤니티에서 관리하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 완성, 유효성 검증 규칙 완성 등 다양한 IDE 기능을 제공합니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

라라벨 프로젝트를 만들었으니, 무엇을 다음으로 배워야 할지 궁금할 수 있습니다. 먼저, 라라벨이 어떻게 작동하는지 익히기 위해 다음 문서를 읽어보시길 강력히 권장합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/10.x/lifecycle)
- [설정](/docs/10.x/configuration)
- [디렉토리 구조](/docs/10.x/structure)
- [프론트엔드](/docs/10.x/frontend)
- [서비스 컨테이너](/docs/10.x/container)
- [파사드](/docs/10.x/facades)

</div>

라라벨을 어떻게 사용하고 싶은지에 따라 다음 학습 방향도 달라집니다. 라라벨의 주요 활용 사례 두 가지를 아래에서 살펴보겠습니다.

> [!NOTE]  
> 라라벨이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 라라벨 프레임워크 투어와 첫 애플리케이션 빌드를 함께 경험할 수 있습니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀 스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

라라벨은 풀 스택 프레임워크로 사용할 수 있습니다. "풀 스택"이란 라라벨을 통해 애플리케이션 라우팅을 처리하고, [Blade 템플릿](/docs/10.x/blade) 이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술로 프론트엔드를 렌더링한다는 뜻입니다. 라라벨을 사용하는 가장 일반적이며 생산적인 방법입니다.

만약 이렇게 라라벨을 사용하고 싶다면, [프론트엔드 개발](/docs/10.x/frontend), [라우팅](/docs/10.x/routing), [뷰](/docs/10.x/views), [Eloquent ORM](/docs/10.x/eloquent) 관련 문서를 살펴보는 것이 좋습니다. 또한, [Livewire](https://livewire.laravel.com)나 [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 관심 있을 겁니다. 이 패키지들은 라라벨을 풀 스택 프레임워크로 사용하면서도 싱글 페이지 자바스크립트 애플리케이션의 UI 이점을 누릴 수 있게 해줍니다.

풀 스택 프레임워크로 라라벨을 사용할 때는, [Vite](/docs/10.x/vite)를 통해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 배우길 적극 추천합니다.

> [!NOTE]  
> 애플리케이션 빌드를 빠르게 시작하려면, 공식 [애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 확인하세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

라라벨은 자바스크립트 싱글 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로도 사용할 수 있습니다. 예를 들어, 라라벨을 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 사용할 수 있습니다. 이 경우, 라라벨은 애플리케이션 인증(/docs/10.x/sanctum)과 데이터 저장/조회 기능을 제공하고, 큐, 이메일, 알림 등 라라벨의 강력한 서비스를 활용할 수 있습니다.

이렇게 사용한다면 [라우팅](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), [Eloquent ORM](/docs/10.x/eloquent) 문서를 확인하시길 권장합니다.

> [!NOTE]  
> 라라벨 백엔드와 Next.js 프론트엔드를 빠르게 구축하고 싶다면, Laravel Breeze가 [API 스택](/docs/10.x/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 제공합니다. 수분 내 시작할 수 있습니다.