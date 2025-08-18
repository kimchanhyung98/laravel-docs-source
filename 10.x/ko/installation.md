# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 프로젝트 생성](#creating-a-laravel-project)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Sail을 이용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서의 Sail 사용](#sail-on-macos)
    - [Windows에서의 Sail 사용](#sail-on-windows)
    - [Linux에서의 Sail 사용](#sail-on-linux)
    - [Sail 서비스 선택](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들 때 구조와 출발점을 제공하여, 세부 구현은 라라벨이 담당하고 개발자는 놀라운 기능 개발에 집중할 수 있도록 도와줍니다.

Laravel은 강력한 의존성 주입, 명확한 데이터베이스 추상화 계층, 큐 및 스케줄링 작업, 단위 및 통합 테스트 등 풍부한 기능을 제공하면서, 개발자가 뛰어난 경험을 할 수 있도록 노력하고 있습니다.

PHP 웹 프레임워크가 처음이신 분이나 다년간 경험이 있으신 분 모두에게 Laravel은 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로써의 첫 걸음을 함께 하거나, 이미 가진 전문성을 한 단계 끌어올리는 데 도움을 드리겠습니다. 여러분이 어떤 것을 만들어낼지 저희도 매우 기대하고 있습니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [라라벨 부트캠프](https://bootcamp.laravel.com)를 방문하여, 직접 프레임워크를 체험하면서 첫 라라벨 애플리케이션을 함께 만들어보세요.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 저희는 현대적이고 풀스택 웹 애플리케이션을 구축할 때 라라벨이 최고의 선택이라고 생각합니다.

#### 진화하는(Progressive) 프레임워크

라라벨은 "진화하는(Progressive)" 프레임워크입니다. 즉, 여러분의 성장에 맞추어 라라벨도 함께 성장합니다. 웹 개발에 첫 발을 내딛는 분이라면, 방대한 공식 문서, 다양한 가이드, [비디오 튜토리얼](https://laracasts.com)을 통해 부담 없이 체계적으로 학습할 수 있습니다.

경험 많은 개발자라면, 라라벨은 [의존성 주입](/docs/10.x/container), [단위 테스트](/docs/10.x/testing), [큐](/docs/10.x/queues), [실시간 이벤트](/docs/10.x/broadcasting) 등 전문적인 웹 애플리케이션을 만들 수 있도록 강력한 도구를 제공합니다. 라라벨은 엔터프라이즈 급의 업무까지도 수월하게 처리할 수 있도록 조율되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적인 특성과, Redis처럼 빠르고 분산된 캐시 시스템과의 빌트인 연동 덕분에, 라라벨을 통한 가로 확장은 매우 간단합니다. 실제로 월 수억 건의 요청을 처리하는 라라벨 애플리케이션이 이미 존재합니다.

극한의 확장성을 원한다면, [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 활용해 AWS의 최신 서버리스 기술로 사실상 제한 없는 규모의 라라벨 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 프레임워크

라라벨은 PHP 생태계에서 최고의 패키지들을 통합하여 개발자 친화적이면서도 견고한 프레임워크를 제공합니다. 더불어 전 세계 수천 명의 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 아마 여러분도 언젠가는 라라벨 컨트리뷰터가 될 수 있을 것입니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 프로젝트 생성 (Creating a Laravel Project)

첫 번째 라라벨 프로젝트를 생성하기 전에, 로컬 컴퓨터에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인하세요. macOS 환경에서는 [Laravel Herd](https://herd.laravel.com)를 통해 몇 분 만에 PHP와 Composer를 설치할 수 있습니다. 또한 [Node와 NPM 설치](https://nodejs.org)를 권장합니다.

PHP와 Composer 설치가 완료되면, Composer의 `create-project` 명령어를 사용해 새 라라벨 프로젝트를 만들 수 있습니다:

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

또는, Composer를 통해 [라라벨 인스톨러](https://github.com/laravel/installer)를 글로벌로 설치한 후, 인스톨러 명령어로도 새 라라벨 프로젝트를 생성할 수 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트 생성이 완료되면, Laravel Artisan의 `serve` 명령어로 라라벨의 로컬 개발 서버를 시작하세요:

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버를 시작하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다. 이제 [라라벨 생태계에 대한 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 물론 [데이터베이스 설정](#databases-and-migrations)도 진행하실 수 있습니다.

> [!NOTE]  
> 라라벨 애플리케이션 개발을 더 빠르게 시작하고 싶으시다면, [스타터 키트](/docs/10.x/starter-kits)를 활용해 보세요. 라라벨 스타터 키트는 새로운 라라벨 애플리케이션에 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션은 파일 내에서 문서화되어 있으니, 마음껏 살펴보고 사용할 수 있는 설정들을 익혀보세요.

라라벨은 기본적으로 별도의 추가 설정이 거의 필요하지 않습니다. 바로 개발을 시작하셔도 무방합니다! 다만, `config/app.php` 파일과 해당 문서를 한 번쯤 살펴보는 것을 권장합니다. 이에는 `timezone`, `locale` 등 프로젝트에 맞게 바꿀 수 있는 다양한 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 많은 설정 옵션 값은, 애플리케이션이 로컬 컴퓨터에서 실행되는지 아니면 운영 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 대부분의 설정 값은, 애플리케이션 루트에 위치한 `.env` 파일을 통해 지정됩니다.

`.env` 파일은 절대 버전 관리 시스템에 커밋하지 않아야 하며, 각 개발자와 서버 환경마다 서로 다른 환경 구성이 필요할 수 있습니다. 또한, 소스 저장소가 외부에 노출된 경우 중요한 인증 정보가 유출될 위험이 있으므로 보안상 주의가 필요합니다.

> [!NOTE]  
> `.env` 파일과 환경 기반 설정에 대한 자세한 정보는 [설정 문서](/docs/10.x/configuration#environment-configuration)에서 확인할 수 있습니다.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

이제 라라벨 애플리케이션을 만들었으니, 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 MySQL 데이터베이스를 사용하며, `127.0.0.1`에서 데이터베이스에 접근하도록 지정되어 있습니다.

> [!NOTE]  
> macOS에서 MySQL, Postgres, 혹은 Redis를 설치해야 하는 경우 [DBngin](https://dbngin.com/)을 사용해보세요.

만약 로컬 환경에 MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수도 있습니다. SQLite는 작고 빠르며 자체적으로 동작하는 데이터베이스 엔진입니다. 사용하려면 `.env` 설정 파일을 라라벨의 `sqlite` 드라이버로 업데이트하고, 다른 데이터베이스 설정 옵션은 삭제하세요:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite 데이터베이스 구성이 끝나면, [데이터베이스 마이그레이션](/docs/10.x/migrations)을 실행해 애플리케이션에서 사용할 데이터베이스 테이블을 생성할 수 있습니다:

```shell
php artisan migrate
```

애플리케이션을 위한 SQLite 데이터베이스 파일이 없다면, 라라벨이 데이터베이스를 새로 생성할 것인지 물어봅니다. 일반적으로 SQLite 데이터베이스 파일은 `database/database.sqlite` 경로에 생성됩니다.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

라라벨은 반드시 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨을 서비스하려고 하면, 애플리케이션 내의 민감한 파일들이 외부에 노출될 수 있으므로 삼가야 합니다.

<a name="docker-installation-using-sail"></a>
## Sail을 이용한 Docker 설치 (Docker Installation Using Sail)

여러분이 어떤 운영체제를 사용하든 라라벨을 쉽게 시작할 수 있도록, 로컬 환경에서 라라벨 프로젝트를 개발하고 실행하는 다양한 방법을 제공합니다. 이러한 옵션을 나중에 살펴볼 수도 있지만, 라라벨은 [Sail](/docs/10.x/sail)이라는 기본 제공 솔루션을 통해 [Docker](https://www.docker.com)를 이용한 라라벨 프로젝트 실행을 지원합니다.

Docker는 어플리케이션과 서비스를 가벼운 "컨테이너"라는 독립된 환경에서 실행할 수 있게 해주는 도구입니다. 컨테이너는 로컬 컴퓨터의 소프트웨어나 설정에 영향을 주지 않기 때문에, 웹 서버나 데이터베이스 같은 복잡한 개발 도구를 따로 설치·설정할 필요가 없습니다. 시작을 위해서는 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

라라벨 Sail은 라라벨의 기본 Docker 설정과 상호작용할 수 있게 해주는 가벼운 커맨드라인 인터페이스입니다. 사전 Docker 경험이 없어도 PHP, MySQL, Redis 환경에서 라라벨 애플리케이션을 손쉽게 시작할 수 있습니다.

> [!NOTE]  
> 이미 Docker를 잘 다루신다면 걱정하지 마세요! Sail의 모든 부분은 라라벨에 포함된 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서의 Sail 사용

Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 터미널에서 간단한 명령어로 새 라라벨 프로젝트를 생성할 수 있습니다. 예를 들어, "example-app"이라는 디렉터리에 새 라라벨 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론, 위 URL의 "example-app" 대신 원하는 이름으로 바꿀 수 있으며, 애플리케이션 이름은 영문, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 라라벨 애플리케이션 디렉터리는 명령어를 실행한 위치에 생성됩니다.

Sail 설치는 애플리케이션 컨테이너를 로컬에서 빌드하는 과정 때문에 몇 분 정도 소요될 수 있습니다.

프로젝트가 생성되면, 해당 디렉터리로 이동하여 라라벨 Sail을 실행할 수 있습니다. Sail은 라라벨의 기본 Docker 설정을 손쉽게 다룰 수 있는 CLI를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 모두 시작되면, 웹 브라우저에서 http://localhost 로 접속할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 자세히 알고 싶다면, [Sail 완전 문서](/docs/10.x/sail)를 참고하세요.

<a name="sail-on-windows"></a>
### Windows에서의 Sail 사용

Windows PC에서 새 라라벨 애플리케이션을 만들기 전에, 반드시 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치하세요. 그리고 Windows Subsystem for Linux 2 (WSL2)가 설치 및 활성화되어 있는지 확인해야 합니다. WSL은 Windows 10에서 리눅스 실행 파일을 네이티브로 실행할 수 있게 해줍니다. WSL2의 설치 및 활성화 방법은 Microsoft의 [개발 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]  
> WSL2 설치 및 활성화 후, Docker Desktop이 [WSL2 백엔드 사용으로 설정되었는지](https://docs.docker.com/docker-for-windows/wsl/) 꼭 확인하세요.

이제 첫 라라벨 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행하고, WSL2 리눅스 세션을 시작하세요. 그리고 아래와 같은 터미널 명령어로 새 라라벨 프로젝트를 생성할 수 있습니다:

```shell
curl -s https://laravel.build/example-app | bash
```

물론, "example-app" 대신 원하는 이름을 넣어도 되며, 애플리케이션 이름에는 영문, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 라라벨 애플리케이션 디렉터리는 명령 실행 위치에 생성됩니다.

Sail 설치 과정은 컨테이너 빌드 때문에 몇 분 정도 소요될 수 있습니다.

프로젝트 생성 후 애플리케이션 디렉터리로 이동해 라라벨 Sail을 실행해보세요. Sail은 라라벨의 기본 Docker 설정을 관리하는 간편한 커맨드라인 인터페이스를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 모두 실행되면 웹 브라우저에서 http://localhost 주소로 접속할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 많이 알고 싶다면, [Sail 완전 문서](/docs/10.x/sail)를 참고하세요.

#### WSL2 환경에서의 개발

물론, WSL2 환경에 생성된 라라벨 애플리케이션 파일을 편집할 수 있어야 합니다. 이를 위해 Microsoft의 [Visual Studio Code](https://code.visualstudio.com)와, 공식 [Remote Development 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 추천합니다.

이 도구들을 설치했다면, Windows Terminal을 통해 애플리케이션 루트 디렉터리에서 `code .` 명령어를 실행해 언제든 라라벨 프로젝트를 열 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서의 Sail 사용

Linux에서 개발 중이고 이미 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 아래와 같은 터미널 명령어로 새 라라벨 프로젝트를 만들 수 있습니다.

먼저, Linux용 Docker Desktop을 사용 중이라면 아래 명령어를 실행하세요. 아니라면 이 단계는 건너뛰어도 됩니다:

```shell
docker context use default
```

그 다음, "example-app"이라는 디렉터리에 새 라라벨 애플리케이션을 만들려면 터미널에서 다음처럼 명령어를 입력하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

물론, "example-app" 부분을 원하는 이름으로 바꿀 수 있으며, 이름에는 영문, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 명령어를 실행한 디렉터리 내에 애플리케이션이 생성됩니다.

Sail 설치 과정은 컨테이너 빌드로 인해 몇 분 정도 소요될 수 있습니다.

프로젝트가 만들어진 후 디렉터리로 이동하여 라라벨 Sail을 실행하면, 기본 Docker 설정을 간편하게 제어할 수 있습니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 모두 실행되면 웹 브라우저에서 http://localhost 주소로 접속해보세요.

> [!NOTE]  
> 라라벨 Sail에 대해 더 자세히 알아보고 싶으면, [Sail 완전 문서](/docs/10.x/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택 (Choosing Your Sail Services)

Sail을 이용해 새 라라벨 애플리케이션을 만들 때, `with` 쿼리 문자열 변수를 활용하면 `docker-compose.yml`에 어떤 서비스를 추가할지 직접 고를 수 있습니다. 사용 가능한 서비스로는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

설정을 명시하지 않으면, 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium` 스택이 설정됩니다.

또한, `devcontainer` 파라미터를 URL에 추가해 Sail에서 기본 [Devcontainer](/docs/10.x/sail#using-devcontainers)를 설치하도록 지시할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발에는 원하는 어떤 코드 에디터든 자유롭게 사용할 수 있습니다. 그 중에서도 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 라라벨과 그 생태계에 대한 강력한 지원(예: [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html))을 제공합니다.

또한, 커뮤니티에서 유지되는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 자동 생성, Eloquent 문법 자동 완성, 유효성 검사 규칙 자동 완성 등 다양한 IDE 보조 기능을 제공합니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션 사이의 연결을 강화해주는 강력한 도구입니다. Boost는 AI 에이전트에게 라라벨 특화 맥락, 도구, 가이드라인을 제공하여, 라라벨 규칙에 맞는 더 정확하고 버전별로 최적화된 코드를 생성할 수 있도록 합니다.

Boost를 라라벨 애플리케이션에 설치하면, AI 에이전트는 15개 이상의 특화 도구에 접근하여 여러분이 사용 중인 패키지 파악, 데이터베이스 질의, 라라벨 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등이 가능합니다.

또한, Boost는 프로젝트에서 사용하는 라라벨 및 패키지 버전에 맞춘 17,000개 이상의 라라벨 생태계 벡터화 문서에 AI 에이전트가 접근하도록 제공합니다. 이는 AI 에이전트가 여러분 프로젝트의 실제 버전에 최적화된 안내를 줄 수 있음을 의미합니다.

Boost에는 라라벨에서 관리하는 AI 가이드라인도 포함되어 있어, 에이전트가 프레임워크 규칙을 따르고, 적절한 테스트 코드를 작성하며, 코드 자동 생성 시 일반적인 문제점을 피할 수 있도록 유도합니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상을 사용하는 라라벨 10, 11, 12 애플리케이션에 설치할 수 있습니다. 우선 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치가 완료되면, 인터랙티브 인스톨러를 실행하세요:

```shell
php artisan boost:install
```

인스톨러는 여러분의 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 기능을 선택할 수 있도록 돕습니다. Boost는 기존 프로젝트의 규칙을 존중하며, 기본적으로 강제적인 스타일 규칙을 적용하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알아보고 싶다면 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

라라벨 프로젝트를 생성했다면, 이제 다음에 무엇을 익혀야 할지 고민될 수 있습니다. 먼저 라라벨의 작동 방식을 충분히 이해하기 위해 아래 문서를 꼭 읽어보시길 강력히 추천합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/10.x/lifecycle)
- [설정](/docs/10.x/configuration)
- [디렉터리 구조](/docs/10.x/structure)
- [프론트엔드](/docs/10.x/frontend)
- [서비스 컨테이너](/docs/10.x/container)
- [파사드](/docs/10.x/facades)

</div>

라라벨을 어떻게 활용할지에 따라 여러분의 여정은 달라집니다. 라라벨을 활용하는 방법에는 여러 가지가 있는데, 아래에서 프레임워크의 대표적인 두 가지 사용 사례를 소개합니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [라라벨 부트캠프](https://bootcamp.laravel.com)에서, 직접 프레임워크를 체험하며 첫 라라벨 애플리케이션을 함께 만들어보세요.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

라라벨은 풀스택(Full Stack) 프레임워크로 사용할 수 있습니다. "풀스택" 프레임워크란, 요청을 라우팅하고, [Blade 템플릿](/docs/10.x/blade) 또는 [Inertia](https://inertiajs.com)와 같은 SPA 하이브리드 기술을 사용해 프론트엔드를 렌더링하는 방식으로 라라벨을 이용함을 의미합니다. 이는 라라벨을 사용하는 가장 일반적이고, 동시에 가장 생산적인 방법입니다.

이 방식으로 라라벨을 사용하려면 [프론트엔드 개발](/docs/10.x/frontend), [라우팅](/docs/10.x/routing), [뷰](/docs/10.x/views), [Eloquent ORM](/docs/10.x/eloquent) 관련 문서를 확인해보세요. 또한, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 함께 살펴보시길 추천합니다. 이 패키지들은 라라벨을 풀스택 프레임워크로 쓰면서도 SPA의 UI 장점을 누릴 수 있습니다.

풀스택 프레임워크로 라라벨을 활용한다면, [Vite](/docs/10.x/vite)를 사용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 꼭 익혀보시길 권장합니다.

> [!NOTE]  
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/10.x/starter-kits)를 활용해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

라라벨은 JavaScript 기반의 싱글페이지 애플리케이션(SPA)이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, 여러분의 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 경우 라라벨은 애플리케이션의 [인증](/docs/10.x/sanctum), 데이터 저장/조회, 그리고 큐, 이메일, 알림 등 강력한 서비스들을 제공할 수 있습니다.

이 방식으로 라라벨을 사용하려면 [라우팅](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), [Eloquent ORM](/docs/10.x/eloquent) 문서를 살펴보세요.

> [!NOTE]  
> 라라벨 백엔드와 Next.js 프론트엔드의 스캐폴딩을 빠르게 시작하고 싶나요? 라라벨 Breeze는 [API 스택](/docs/10.x/starter-kits#breeze-and-next)과 함께 [Next.js 프론트엔드 구현체](https://github.com/laravel/breeze-next)도 제공하여 몇 분 만에 시작할 수 있게 해줍니다.
