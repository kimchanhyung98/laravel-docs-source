# 설치 (Installation)

- [Laravel 소개](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치 프로그램 설치](#installing-php)
    - [애플리케이션 생성하기](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉토리 설정](#directory-configuration)
- [Herd를 이용한 로컬 설치](#local-installation-using-herd)
    - [macOS에서 Herd](#herd-on-macos)
    - [Windows에서 Herd](#herd-on-windows)
- [Sail을 이용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서 Sail](#sail-on-macos)
    - [Windows에서 Sail](#sail-on-windows)
    - [Linux에서 Sail](#sail-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 소개 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란 애플리케이션을 만드는 데 구조와 출발점을 제공하여 개발자가 놀라운 것을 만드는 데 집중할 수 있게 세부 작업을 대신 처리해 줍니다.

Laravel은 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 탁월한 개발자 경험을 목표로 합니다.

PHP 웹 프레임워크가 처음이든 수년간 경험이 있든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 처음 웹 개발자로서의 첫걸음을 도와주거나, 전문가로서 다음 단계로 뛰어오르도록 지원해 드립니다. 어떤 멋진 것을 만드실지 기대됩니다.

> [!NOTE]  
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인해 보세요. 실습을 통해 첫 Laravel 애플리케이션 구축 과정을 안내해 드립니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 만들 때 선택 가능한 도구와 프레임워크가 다양합니다. 하지만 저희는 현대적인 풀스택 웹 애플리케이션을 만드는 데 Laravel이 최선이라 믿습니다.

#### 점진적(progressive) 프레임워크

저희는 Laravel을 "점진적(progressive)" 프레임워크라 부릅니다. 즉, Laravel은 여러분과 함께 성장합니다. 웹 개발을 처음 시작하는 단계라면, 방대한 문서, 가이드, [비디오 튜토리얼](https://laracasts.com)을 통해 부담 없이 배우도록 도와줍니다.

고급 개발자라면, Laravel은 [의존성 주입](/docs/11.x/container), [단위 테스트](/docs/11.x/testing), [큐](/docs/11.x/queues), [실시간 이벤트](/docs/11.x/broadcasting) 등 강력한 도구들을 제공합니다. Laravel은 전문 웹 애플리케이션 제작에 최적화되어 있으며, 기업용 작업 부하도 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 확장 가능합니다. PHP의 확장 우호적 특성과 Laravel의 빠르고 분산된 캐시 시스템(Redis 등) 기본 지원 덕분에 Laravel로 수평적 확장을 손쉽게 할 수 있습니다. 실제로 Laravel 애플리케이션은 월 수억 건의 요청도 쉽게 처리할 수 있도록 확장된 사례도 있습니다.

극한 확장이 필요하다면 [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼으로 AWS 최신 서버리스 기술 위에서 사실상 무제한 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티가 함께하는 프레임워크

Laravel은 PHP 생태계에서 가장 우수한 패키지를 결합해 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 뿐만 아니라 전 세계 수천 명의 뛰어난 개발자가 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 Laravel 커뮤니티의 일원이 될지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel 설치 프로그램 설치 (Installing PHP and the Laravel Installer)

첫 번째 Laravel 애플리케이션을 만들기 전, 로컬 머신에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel 설치 프로그램](https://github.com/laravel/installer)이 설치되어 있어야 합니다. 또한 애플리케이션의 프론트엔드 자산을 컴파일하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/)을 설치하는 것이 좋습니다.

만약 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어는 macOS, Windows, Linux에서 PHP, Composer, 그리고 Laravel 설치 프로그램을 설치합니다:

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

해당 명령어 실행 후 터미널 세션을 재시작해야 합니다. `php.new`를 통해 설치한 PHP, Composer, Laravel 설치 프로그램을 업데이트하려면, 같은 명령어를 다시 터미널에서 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, 다음과 같이 Composer로 Laravel 설치 프로그램만 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]  
> 풀 기능 그래픽 환경을 제공하는 PHP 설치 및 관리 도구로는 [Laravel Herd](#local-installation-using-herd)를 확인해 보세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성하기 (Creating an Application)

PHP, Composer, Laravel 설치 프로그램이 준비되면 새로운 Laravel 애플리케이션을 만들 준비가 된 것입니다. Laravel 설치 프로그램은 테스트 프레임워크, 데이터베이스, 스타터 키트 선택을 안내합니다:

```nothing
laravel new example-app
```

애플리케이션 생성 후, 다음 Composer `dev` 스크립트를 이용해 Laravel의 로컬 개발 서버, 큐 작업자, Vite 개발 서버를 실행할 수 있습니다:

```nothing
cd example-app
npm install && npm run build
composer run dev
```

개발 서버 시작 후, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다. 이후 [Laravel 생태계의 다음 단계로 나아갈 준비](#next-steps)가 됩니다. 물론 [데이터베이스 설정](#databases-and-migrations)도 함께 진행할 수 있습니다.

> [!NOTE]  
> Laravel 애플리케이션 개발에 빠르게 착수하고 싶다면, [스타터 키트](/docs/11.x/starter-kits)를 사용해 보세요. 스타터 키트는 백엔드 및 프론트엔드 인증 기본 구조를 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에 주석과 문서가 포함되어 있으니 자유롭게 살펴보고 익숙해지시기 바랍니다.

Laravel은 기본적으로 별도의 설정 없이 바로 개발을 시작할 수 있습니다. 하지만 `config/app.php` 파일과 그 문서도 살펴보면 좋습니다. 이 파일에는 `url`, `locale` 같은 애플리케이션에 맞게 변경할 수 있는 여러 설정이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

Laravel 설정 값들은 애플리케이션이 로컬 머신에서 실행되거나 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 중요한 설정 값들을 `.env`라는 파일에서 정의하도록 되어 있으며, 이 파일은 애플리케이션 루트에 위치합니다.

`.env` 파일은 보통 소스 저장소에 커밋하지 않습니다. 여러 개발자 혹은 서버 환경마다 다를 수 있고, 보안상 위험할 수 있기 때문입니다. 예를 들어, 침입자가 저장소에 접근한다면 민감한 자격 증명 정보가 노출될 수 있습니다.

> [!NOTE]  
> `.env` 파일과 환경 기반 설정에 대해 더 알고 싶다면, 전체 [설정 문서](/docs/11.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

Laravel 애플리케이션이 준비되면, 데이터를 저장할 데이터베이스 구성이 필요할 것입니다. 기본적으로 애플리케이션 `.env` 파일에서는 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션 생성 시 Laravel은 `database/database.sqlite` 파일을 생성하고, 필요한 데이터베이스 테이블 생성을 위한 마이그레이션을 실행합니다.

MySQL이나 PostgreSQL 같은 다른 데이터베이스를 사용하고 싶다면 `.env` 파일을 아래 예시처럼 수정할 수 있습니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 대신 다른 데이터베이스를 사용하려면, 데이터베이스를 직접 만들고 애플리케이션의 [마이그레이션](/docs/11.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]  
> macOS나 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면, [Herd Pro](https://herd.laravel.com/#plans) 사용을 고려해 보세요.

<a name="directory-configuration"></a>
### 디렉토리 설정 (Directory Configuration)

Laravel 애플리케이션은 웹 서버의 "웹 디렉토리" 루트에서 제공되어야 합니다. Laravel 애플리케이션을 웹 디렉토리 하위 디렉토리에서 서비스하려고 시도해서는 안 됩니다. 그렇게 하면 애플리케이션 내 민감한 파일이 노출될 위험이 있습니다.

<a name="local-installation-using-herd"></a>
## Herd를 이용한 로컬 설치 (Local Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠른 네이티브 Laravel과 PHP 개발 환경입니다. Herd는 PHP와 Nginx 등 Laravel 개발에 필요한 모든 것을 포함합니다.

Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 명령줄 도구를 포함합니다.

> [!NOTE]  
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 보기, 로그 모니터링 등 강력한 추가 기능을 제공합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd (Herd on macOS)

macOS 환경에서는 [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 PHP 버전을 자동으로 다운로드하여 Mac에서 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 실행되도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "parked" 디렉토리를 지원합니다. 이 디렉토리 내의 모든 Laravel 애플리케이션은 자동으로 Herd에 의해 서비스됩니다. 기본적으로 `~/Herd` 경로에 'parked' 디렉토리를 생성하며, 이 디렉토리 내 Laravel 애플리케이션은 해당 디렉토리 이름을 붙인 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후 Laravel CLI(내장된)를 사용해 Laravel 애플리케이션을 가장 빠르게 만들 수 있습니다:

```nothing
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, Herd UI를 통해 parked 디렉토리 및 PHP 설정 관리를 할 수 있습니다. Herd 아이콘은 시스템 트레이에 있습니다.

Herd에 대한 자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd (Herd on Windows)

Windows용 Herd 설치 프로그램은 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치 완료 후 Herd를 실행해 온보딩 프로세스를 완료하고, 최초로 Herd UI에 접근할 수 있습니다.

Herd UI는 시스템 트레이 아이콘을 왼쪽 클릭으로 열 수 있으며, 오른쪽 클릭 시 일상적으로 필요한 도구에 빠르게 접근할 수 있는 퀵 메뉴가 나타납니다.

설치 과정에서 Herd는 홈 디렉토리의 `%USERPROFILE%\Herd`에 "parked" 디렉토리를 만듭니다. 이 디렉토리 내 모든 Laravel 애플리케이션은 자동으로 Herd가 서비스하며, 해당 디렉토리 이름을 붙인 `.test` 도메인으로 접속할 수 있습니다.

Herd 설치 후 Windows PowerShell에서 Laravel CLI를 사용해 빠르게 새 애플리케이션을 만들 수 있습니다:

```nothing
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows용 Herd에 관해 더 알고 싶으면 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="docker-installation-using-sail"></a>
## Sail을 이용한 Docker 설치 (Docker Installation Using Sail)

Laravel은 어떤 운영체제를 사용하든 쉽게 시작할 수 있도록 다양한 옵션을 제공합니다. 그중 하나가 Laravel 자체 내장 도구인 [Sail](/docs/11.x/sail)입니다. Sail은 [Docker](https://www.docker.com)를 이용해 Laravel 애플리케이션을 로컬에서 실행하는 방법입니다.

Docker는 애플리케이션과 서비스를 작은 경량 컨테이너로 실행해, 로컬에 설치된 소프트웨어나 설정과 충돌하지 않습니다. 복잡한 웹 서버, 데이터베이스 설정에 신경 쓸 필요 없이 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 시작할 수 있습니다.

Sail은 Laravel 기본 Docker 설정과 상호작용할 수 있는 경량 명령줄 인터페이스입니다. 별도의 Docker 경험 없이도 PHP, MySQL, Redis로 Laravel 애플리케이션 개발에 바로 뛰어들게 해줍니다.

> [!NOTE]  
> 이미 Docker 사용에 익숙하다면, Laravel에 포함된 `docker-compose.yml` 파일을 수정해 Sail 설정을 마음대로 커스터마이징할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail (Sail on macOS)

Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치한 상태라면, 터미널에서 간단한 명령어로 새 Laravel 애플리케이션을 만들 수 있습니다. 예를 들어, "example-app"이라는 이름의 디렉토리에 만들려면 터미널에 다음을 입력하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

"example-app"을 원하는 애플리케이션 이름으로 바꿔도 되지만, 이름에는 영문자, 숫자, 대시, 밑줄만 사용해야 합니다. 명령어를 실행한 디렉토리 내에 Laravel 애플리케이션 디렉토리가 생성됩니다.

설치 중에는 Sail의 애플리케이션 컨테이너가 로컬에서 빌드되기 때문에 몇 분이 걸릴 수 있습니다.

애플리케이션 생성 후 해당 디렉토리로 이동해 Laravel Sail을 시작할 수 있습니다. Sail은 Laravel 기본 Docker 설정을 다룰 수 있는 간단한 CLI를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너들이 시작되면, 애플리케이션의 [데이터베이스 마이그레이션](/docs/11.x/migrations)을 실행하세요:

```shell
./vendor/bin/sail artisan migrate
```

마지막으로 웹 브라우저에서 http://localhost 주소로 애플리케이션에 접속할 수 있습니다.

> [!NOTE]  
> Laravel Sail에 대해 더 배우고 싶다면, [전체 문서](/docs/11.x/sail)를 참고하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail (Sail on Windows)

Windows에서 새 Laravel 애플리케이션을 만들려면, 먼저 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치해야 합니다. 그리고 Windows Subsystem for Linux 2(WSL2)를 설치·활성화해야 합니다. WSL은 Windows 10에서 리눅스 바이너리를 네이티브 실행할 수 있게 합니다. 설치 및 활성화 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 참고하세요.

> [!NOTE]  
> WSL2 설치 및 활성화 후 Docker Desktop이 [WSL2 백엔드를 사용하도록 구성되었는지](https://docs.docker.com/docker-for-windows/wsl/) 반드시 확인하세요.

준비가 끝나면 [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행해 WSL2 리눅스 터미널 세션을 시작합니다. 그리고 아래 명령어로 새 Laravel 애플리케이션을 만듭니다. 예시로 "example-app" 디렉토리 이름을 사용합니다:

```shell
curl -s https://laravel.build/example-app | bash
```

이 URL의 "example-app" 부분을 원하는 이름으로 바꿀 수 있지만, 이름에 영문자, 숫자, 대시, 밑줄만 포함해야 하며, 명령어를 실행한 디렉토리에 애플리케이션 디렉토리가 생성됩니다.

설치 과정에서 Sail 컨테이너가 빌드되므로 시간이 걸릴 수 있습니다.

생성이 끝난 후, 애플리케이션 디렉토리로 이동해 Laravel Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 시작되면 애플리케이션의 [데이터베이스 마이그레이션](/docs/11.x/migrations)을 실행합니다:

```shell
./vendor/bin/sail artisan migrate
```

웹 브라우저에서 http://localhost로 접근할 수 있습니다.

> [!NOTE]  
> Laravel Sail에 대해 더 배우고 싶다면, [전체 문서](/docs/11.x/sail)를 확인하세요.

#### WSL2 내에서 개발하기

WSL2 내에 생성된 Laravel 애플리케이션 파일을 수정하려면, Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 공식 [원격 개발 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 사용하는 것을 권장합니다.

설치 후, 애플리케이션 루트 디렉토리에서 `code .` 명령어를 터미널에 입력하면 Visual Studio Code가 해당 프로젝트로 열립니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail (Sail on Linux)

Linux에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 간단한 명령어로 Laravel 애플리케이션을 만들 수 있습니다.

먼저, Docker Desktop for Linux를 사용하는 경우 아래 명령어를 실행합니다. 그렇지 않은 경우 이 단계는 생략하세요:

```shell
docker context use default
```

그다음, "example-app"이라는 이름의 디렉토리에 새 Laravel 애플리케이션을 생성합니다:

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app" 대신 원하는 이름을 사용해도 되지만, 이름에는 영문자, 숫자, 대시, 밑줄만 포함해야 하며, 명령어 실행 위치에 디렉토리가 생성됩니다.

설치 과정에서 Sail 컨테이너가 빌드되므로 시간이 걸릴 수 있습니다.

애플리케이션 생성 후 해당 디렉토리로 이동해 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 시작되면 애플리케이션의 [데이터베이스 마이그레이션](/docs/11.x/migrations)을 실행합니다:

```shell
./vendor/bin/sail artisan migrate
```

그리고 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

> [!NOTE]  
> Laravel Sail에 대해 더 자세히 알고 싶다면, [전체 문서](/docs/11.x/sail)를 확인하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기 (Choosing Your Sail Services)

Sail로 새 Laravel 애플리케이션 생성 시 `with` 쿼리 문자열 변수를 사용해 `docker-compose.yml` 파일에 포함할 서비스를 선택할 수 있습니다. 선택 가능한 서비스로는 `mysql`, `pgsql`, `mariadb`, `redis`, `valkey`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

서비스를 지정하지 않으면, 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium` 스택이 구성됩니다.

또한 `devcontainer` 매개변수를 URL에 추가하면 기본 [Devcontainer](/docs/11.x/sail#using-devcontainers)도 설치할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 개발에는 어떤 코드 편집기든 자유롭게 사용하셔도 됩니다. 그러나 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 Laravel과 생태계를 광범위하게 지원합니다. 예를 들면 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) 지원 등이 포함됩니다.

또한 커뮤니티에서 유지하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동완성, 유효성 검사 룰 완성 등 여러 유용한 IDE 확장 기능을 제공합니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 생성했으니, 다음에 어떤 것을 배울지 궁금할 것입니다. 우선 Laravel의 작동 방식을 이해하기 위해 다음 문서를 먼저 읽어보는 것을 권장합니다:

<div class="content-list" markdown="1">

- [요청 수명주기](/docs/11.x/lifecycle)
- [설정](/docs/11.x/configuration)
- [디렉토리 구조](/docs/11.x/structure)
- [프론트엔드](/docs/11.x/frontend)
- [서비스 컨테이너](/docs/11.x/container)
- [파사드](/docs/11.x/facades)

</div>

Laravel의 사용 목적에 따라 다음 단계가 달라집니다. 아래에 두 가지 주요 사용 사례를 소개합니다.

> [!NOTE]  
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 통해 실습하며 첫 Laravel 애플리케이션을 만드는 과정을 확인하세요.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 풀스택이란, Laravel로 애플리케이션의 요청을 라우팅하고, [Blade 템플릿](/docs/11.x/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술로 프론트엔드를 렌더링하는 것을 말합니다. Laravel 프레임워크의 가장 흔한 사용 방식이며, 저희가 생각하기에 가장 생산적인 방법입니다.

이 방식을 선택한다면, [프론트엔드 개발](/docs/11.x/frontend), [라우팅](/docs/11.x/routing), [뷰](/docs/11.x/views), [Eloquent ORM](/docs/11.x/eloquent) 문서를 참고하세요. 뿐만 아니라 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지도 살펴보세요. 이 패키지들은 Laravel을 풀스택 프레임워크로 사용하면서 싱글 페이지 JavaScript 애플리케이션이 제공하는 UI 이점을 활용할 수 있게 해줍니다.

풀스택으로 사용하는 경우, [Vite](/docs/11.x/vite)를 활용해 애플리케이션 CSS와 JavaScript 컴파일 방법도 익히시길 권장합니다.

> [!NOTE]  
> 빠르게 애플리케이션 개발을 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/11.x/starter-kits) 중 하나를 사용해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel (Laravel the API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로도 사용할 수 있습니다. 예를 들어, Laravel을 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 써서 인증 및 데이터 저장/조회 기능을 제공하면서, 큐, 이메일, 알림 등 Laravel의 강력한 서비스도 활용할 수 있습니다.

이 용도라면 [라우팅](/docs/11.x/routing), [Laravel Sanctum](/docs/11.x/sanctum), [Eloquent ORM](/docs/11.x/eloquent) 문서를 함께 읽어보세요.

> [!NOTE]  
> Laravel 백엔드와 Next.js 프론트엔드를 빠르게 만들고 싶다면, Laravel Breeze의 [API 스택](/docs/11.x/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 참고하세요. 몇 분 만에 시작할 수 있습니다.