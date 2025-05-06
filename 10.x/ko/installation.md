# 설치

- [라라벨 만나기](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 프로젝트 생성하기](#creating-a-laravel-project)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 구성](#directory-configuration)
- [Sail을 사용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서 Sail 사용하기](#sail-on-macos)
    - [Windows에서 Sail 사용하기](#sail-on-windows)
    - [Linux에서 Sail 사용하기](#sail-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [라라벨 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [라라벨 API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 만나기

라라벨은 표현력 있고 우아한 문법을 지닌 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란 애플리케이션을 만드는 데 필요한 구조와 출발점을 제공하며, 개발자는 세부적인 문제보다 멋진 결과물에 집중할 수 있습니다.

라라벨은 놀라운 개발자 경험을 제공하는 동시에, 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등과 같은 다양한 고급 기능을 제공합니다.

PHP 웹 프레임워크가 처음인 분이든, 오랜 경험을 가진 분이든 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 여러분이 웹 개발자로 첫 발을 내딛거나 더 높은 수준의 전문성을 쌓는 데 라라벨이 함께하겠습니다. 여러분이 어떤 것을 만들어낼지 기대됩니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [라라벨 부트캠프](https://bootcamp.laravel.com)에서 실제로 라라벨 애플리케이션을 만들어보며 프레임워크를 익혀보세요.

<a name="why-laravel"></a>
### 왜 라라벨인가?

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 존재합니다. 하지만 우리는 라라벨이 현대적이고 풀스택 웹 애플리케이션을 구축하는 데 가장 적합한 선택이라고 믿습니다.

#### 점진적(Progressive) 프레임워크

라라벨은 "점진적" 프레임워크라고 부릅니다. 즉, 라라벨은 여러분과 함께 성장합니다. 웹 개발을 막 시작한 분이라면, 라라벨의 방대한 문서, 가이드, [비디오 튜토리얼](https://laracasts.com)로 부담 없이 차근차근 배울 수 있습니다.

숙련된 개발자라면, 라라벨은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 전문적인 웹 애플리케이션 개발에 필요한 강력한 도구들을 제공합니다. 라라벨은 엔터프라이즈 대규모 업무도 다룰 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 뛰어난 확장성을 자랑합니다. PHP의 확장성 좋은 특성과 라라벨의 내장된 Redis와 같은 빠르고 분산된 캐시 시스템 지원 덕분에, 라라벨에서는 수평적 확장이 매우 쉽습니다. 실제로 라라벨 애플리케이션이 월 수억 건의 요청도 무리 없이 처리한 사례가 있습니다.

극한의 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 통해 최신 AWS 서버리스 기술로 거의 무제한에 가까운 규모로 라라벨 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 중심 프레임워크

라라벨은 PHP 생태계 최고의 패키지들을 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 게다가 전 세계 수천 명의 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해왔습니다. 여러분도 라라벨 기여자가 될 수 있습니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 프로젝트 생성하기

첫 번째 라라벨 프로젝트를 만들기 전에, 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인하세요. macOS에서 개발하는 경우, [Laravel Herd](https://herd.laravel.com)를 통해 PHP와 Composer를 몇 분 만에 설치할 수 있습니다. 또한 [Node와 NPM 설치](https://nodejs.org)도 권장합니다.

PHP와 Composer 설치 후, Composer의 `create-project` 명령어로 새로운 라라벨 프로젝트를 만들 수 있습니다:

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

또는, [라라벨 인스톨러](https://github.com/laravel/installer)를 Composer로 전역(global) 설치한 뒤 다음과 같이 프로젝트를 생성할 수 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트 생성이 완료되면, Laravel Artisan의 `serve` 명령어로 로컬 개발 서버를 시작하세요:

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버가 시작되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 접속하여 애플리케이션에 접근할 수 있습니다. 이제 [라라벨 생태계의 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 물론, [데이터베이스를 설정](#databases-and-migrations)할 수도 있습니다.

> [!NOTE]  
> 라라벨 애플리케이션 개발을 빠르게 시작하고 싶다면, [스타터 키트](/docs/{{version}}/starter-kits)를 활용해 보세요. 스타터 키트는 새로운 라라벨 프로젝트에 백엔드, 프론트엔드 인증 관련 기본 구조를 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에 대한 문서가 포함되어 있으니, 파일을 둘러보며 사용할 수 있는 옵션을 익혀보세요.

라라벨은 기본적으로 추가 설정이 거의 필요하지 않습니다. 바로 개발을 시작할 수 있습니다! 하지만 `config/app.php` 파일과 그 설명서를 살펴보는 것을 권장합니다. 이 파일에는 `timezone`, `locale` 등 애플리케이션 환경에 맞게 수정할 수 있는 여러 옵션이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

라라벨의 설정 옵션 값은 애플리케이션이 로컬 환경에서 실행되는지, 혹은 운영 서버에서 실행되는지에 따라 달라질 수 있습니다. 이에 따라 중요한 설정 값들은 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의됩니다.

`.env` 파일은 각 개발자/서버마다 환경 설정이 다를 수 있으므로 소스 컨트롤에 커밋하지 않아야 합니다. 만약 해커가 소스 저장소에 접근할 경우 민감한 자격 증명이 노출되는 보안 위험이 발생할 수 있습니다.

> [!NOTE]  
> `.env` 파일 및 환경 기반 설정에 대한 더 자세한 정보는 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션

라라벨 애플리케이션을 만들었다면, 이제 데이터베이스에 정보를 저장하고 싶을 것입니다. 기본적으로, 애플리케이션의 `.env` 설정 파일은 MySQL 데이터베이스와 `127.0.0.1`에서 연결하도록 설정되어 있습니다.

> [!NOTE]  
> macOS에서 MySQL, Postgres 또는 Redis를 설치해야 한다면 [DBngin](https://dbngin.com/)을 사용해보세요.

로컬 머신에 MySQL이나 Postgres를 설치하고 싶지 않다면, [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수 있습니다. SQLite는 작고 빠르며 독립적인 데이터베이스 엔진입니다. 시작하려면, `.env` 파일을 Laravel의 `sqlite` 데이터베이스 드라이버를 사용하도록 변경하고, 나머지 데이터베이스 설정은 삭제하세요:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite 데이터베이스 설정이 완료되면, [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하여 애플리케이션의 데이터베이스 테이블을 생성할 수 있습니다:

```shell
php artisan migrate
```

애플리케이션에 SQLite 데이터베이스가 없다면, 라라벨이 데이터베이스 파일을 생성할지 물어봅니다. 일반적으로 `database/database.sqlite`에 파일이 생성됩니다.

<a name="directory-configuration"></a>
### 디렉터리 구성

라라벨은 웹 서버에서 "웹 디렉터리"의 루트에서 제공되어야 합니다. 웹 디렉터리의 하위 디렉터리에서 라라벨 애플리케이션을 제공하려고 하면 애플리케이션의 민감한 파일이 노출될 수 있으므로 반드시 루트에서 제공해야 합니다.

<a name="docker-installation-using-sail"></a>
## Sail을 사용한 Docker 설치

운영 체제에 상관없이 라라벨을 쉽게 시작할 수 있도록 다양한 로컬 개발 및 실행 방법을 제공합니다. 이 옵션들은 나중에 탐색할 수 있지만, 라라벨은 [Sail](/docs/{{version}}/sail)이라는, [Docker](https://www.docker.com)를 활용한 기본 솔루션을 제공합니다.

Docker는 각 앱과 서비스를 독립적이고 경량화된 "컨테이너"에서 실행해, 로컬 머신 소프트웨어나 설정과 충돌하지 않게 합니다. 따라서 복잡한 개발 도구(웹 서버, 데이터베이스 등)를 로컬에 직접 설치할 필요 없이 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

라라벨 Sail은 라라벨의 기본 Docker 설정과 상호작용하는 경량 커맨드라인 인터페이스입니다. Sail을 이용하면 Docker를 몰라도 PHP, MySQL, Redis 환경의 라라벨 애플리케이션을 쉽게 개발할 수 있습니다.

> [!NOTE]  
> 이미 Docker 전문가라면, 걱정 마세요! Sail의 모든 설정은 Laravel에 포함된 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail 사용하기

Mac에서 개발하고 있고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 터미널에서 간단한 명령어만으로 새로운 라라벨 프로젝트를 만들 수 있습니다. 예를 들어, "example-app"이라는 디렉터리에 라라벨 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론, 이 URL의 "example-app" 부분은 원하는 것으로 바꿀 수 있지만, 애플리케이션명에는 영문자, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 애플리케이션 디렉터리는 명령어를 실행하는 위치에 생성됩니다.

Sail 설치는 로컬에서 애플리케이션 컨테이너를 빌드하므로 몇 분이 걸릴 수 있습니다.

프로젝트 생성 후, 애플리케이션 디렉터리로 이동해 라라벨 Sail을 시작하세요. Sail은 라라벨 기본 Docker 설정과 대화할 수 있는 커맨드라인 인터페이스를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 모두 시작되면 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 알아보고 싶다면, [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail 사용하기

Windows에서 새 라라벨 애플리케이션을 만들기 전에, [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치하세요. 그리고 Windows Subsystem for Linux 2(WSL2)도 설치 및 활성화해야 합니다. WSL은 Windows 10에서 Linux 바이너리 프로그램을 직접 실행할 수 있게 합니다. WSL2 설치 및 활성화 방법은 Microsoft의 [개발 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인하세요.

> [!NOTE]  
> WSL2 설치 및 활성화 후, Docker Desktop이 [WSL2 백엔드 사용으로 설정되어 있는지](https://docs.docker.com/docker-for-windows/wsl/) 확인하세요.

이제 첫 라라벨 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 열고, WSL2 리눅스 OS 세션에서 아래 명령어로 새 프로젝트를 생성하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app"을 원하는 이름으로 바꿔도 되지만, 영문자, 숫자, 대시, 언더스코어만 사용할 수 있습니다. 애플리케이션 디렉터리는 명령어 실행 위치에 생성됩니다.

Sail 설치는 로컬에서 애플리케이션 컨테이너를 빌드하므로 몇 분이 걸릴 수 있습니다.

프로젝트 생성 후, 애플리케이션 디렉터리로 이동해 라라벨 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

모든 Docker 컨테이너가 시작되면 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 알아보고 싶다면, [전체 문서](/docs/{{version}}/sail)를 확인하세요.

#### WSL2 내에서 개발하기

WSL2 환경에 생성된 라라벨 애플리케이션 파일을 수정하려면, Microsoft의 [Visual Studio Code](https://code.visualstudio.com)와 [원격 개발 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 사용하는 것이 좋습니다.

이 도구들이 설치되었다면, Windows Terminal에서 프로젝트 루트에서 `code .` 명령을 실행해 어떤 라라벨 프로젝트든 바로 열 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail 사용하기

Linux에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 간단한 명령어로 새 라라벨 프로젝트를 만들 수 있습니다.

먼저, Docker Desktop for Linux를 사용한다면 다음 명령어를 실행하세요. Docker Desktop for Linux를 사용하지 않는다면 이 단계는 건너도 됩니다:

```shell
docker context use default
```

그 다음, "example-app"이라는 디렉터리에 애플리케이션을 생성하려면 다음 명령어를 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app"은 원하는 이름으로 변경할 수 있으나, 영문자, 숫자, 대시, 언더스코어만 사용하세요.

Sail 설치는 로컬에서 컨테이너를 빌드하는 동안 몇 분이 걸릴 수 있습니다.

프로젝트 생성 후 애플리케이션 디렉터리로 이동하여 라라벨 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 모두 시작되면 웹 브라우저에서 http://localhost로 애플리케이션을 확인할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 알아보려면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 이용해 새로운 라라벨 애플리케이션을 만들 때, `with` 쿼리 스트링 변수를 사용하여 `docker-compose.yml` 파일에 구성할 서비스를 직접 선택할 수 있습니다. 사용 가능한 서비스로는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit`이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

구현할 서비스를 명시하지 않으면, 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`이 추가됩니다.

또한 URL에 `devcontainer` 파라미터를 추가하면 Sail이 기본 [Devcontainer](/docs/{{version}}/sail#using-devcontainers)를 설치할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원

라라벨 애플리케이션 개발 시 원하시는 어떤 코드 에디터든 사용하실 수 있습니다. 하지만 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) 등 라라벨 및 그 생태계에 대한 폭넓은 지원을 제공합니다.

또한 커뮤니티에서 유지하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동 완성, 유효성 검사 규칙 완성 등 다양한 유용한 기능을 추가해줍니다.

<a name="next-steps"></a>
## 다음 단계

라라벨 프로젝트를 생성했다면, 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저, 라라벨이 어떻게 동작하는지 이해하기 위해 아래 문서를 꼭 읽어보길 권장합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [프론트엔드](/docs/{{version}}/frontend)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

라라벨을 어떻게 활용하고 싶은지에 따라 다음 단계가 달라질 수 있습니다. 라라벨은 다양한 방식으로 사용할 수 있으며, 아래에 두 가지 주요 사용 사례를 소개합니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [라라벨 부트캠프](https://bootcamp.laravel.com)에서 실제로 라라벨 애플리케이션을 만들어보며 프레임워크를 익혀보세요.

<a name="laravel-the-fullstack-framework"></a>
### 라라벨 풀스택 프레임워크

라라벨은 풀스택 프레임워크로 활용할 수 있습니다. "풀스택" 프레임워크란 라라벨로 라우팅을 처리하고, [Blade 템플릿](/docs/{{version}}/blade) 또는 [Inertia](https://inertiajs.com)와 같은 싱글페이지 애플리케이션 하이브리드 기술을 사용해 프론트엔드까지 함께 구현하는 방식을 말합니다. 이는 라라벨 프레임워크를 사용하는 가장 일반적이면서도 생산성이 높은 방법입니다.

이렇게 라라벨을 사용할 계획이라면, [프론트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 관련 문서도 읽어보세요. 또한 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 등 커뮤니티 패키지를 통해 라라벨을 풀스택 프레임워크처럼 활용하면서 싱글페이지 자바스크립트 애플리케이션의 다양한 UI 장점들도 누릴 수 있습니다.

라라벨을 풀스택 프레임워크로 활용한다면, [Vite](/docs/{{version}}/vite)를 사용해 CSS와 자바스크립트도 빌드하는 방법을 꼭 익혀 두세요.

> [!NOTE]  
> 애플리케이션을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="laravel-the-api-backend"></a>
### 라라벨 API 백엔드

라라벨은 자바스크립트 싱글페이지 애플리케이션이나 모바일 앱을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 경우, 라라벨로 [인증](/docs/{{version}}/sanctum), 데이터 저장 및 조회, 큐, 이메일, 알림 등 다양한 강력한 서비스를 제공할 수 있습니다.

이런 방식으로 라라벨을 사용할 계획이라면, [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 관련 문서를 참고하세요.

> [!NOTE]  
> 라라벨 백엔드와 Next.js 프론트엔드 개발을 빠르게 시작하고 싶다면, 라라벨 Breeze의 [API 스택](/docs/{{version}}/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)도 참고해 보세요. 수 분 내 바로 시작할 수 있습니다.