# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 라라벨 인스톨러 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 사용한 로컬 설치](#local-installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [Sail을 이용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서 Sail 사용](#sail-on-macos)
    - [Windows에서 Sail 사용](#sail-on-windows)
    - [Linux에서 Sail 사용](#sail-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [라라벨 Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [라라벨 풀스택 프레임워크로 활용하기](#laravel-the-fullstack-framework)
    - [라라벨을 API 백엔드로 활용하기](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

라라벨은 표현력 있고 우아한 문법을 자랑하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란 여러분이 애플리케이션을 개발할 수 있도록 구조와 출발점을 제공해, 세부적인 사항은 라라벨이 처리하는 동안 여러분은 멋진 무언가를 만드는 데 집중할 수 있게 해줍니다.

라라벨은 뛰어난 개발자 경험을 제공하는 동시에, 강력한 기능도 함께 제공합니다. 대표적으로, 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약된 작업, 단위 테스트와 통합 테스트 등이 있습니다.

PHP 웹 프레임워크가 처음인 분이든, 이미 오랜 경험이 있는 개발자든 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛거나 이미 쌓은 전문성을 한 단계 업그레이드하고자 할 때, 라라벨이 여러분을 도와드립니다. 여러분이 무엇을 만들지 기대하겠습니다.

> [!NOTE]  
> 라라벨을 처음 접하시나요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 참고하여 실습을 통해 첫 라라벨 애플리케이션을 만들어보세요.

<a name="why-laravel"></a>
### 왜 라라벨인가?

웹 애플리케이션을 개발할 때 사용할 수 있는 다양한 도구나 프레임워크가 존재합니다. 하지만 저희는 라라벨이 현대적인 풀스택 웹 애플리케이션을 개발하는 데 최고의 선택이라고 믿습니다.

#### 발전적인(Progressive) 프레임워크

라라벨은 발전적인(Progressive) 프레임워크라고 부릅니다. 즉, 라라벨은 여러분의 성장에 맞춰 함께 커나갑니다. 웹 개발에 처음 입문하더라도, 방대한 공식 문서, 가이드, [동영상 튜토리얼](https://laracasts.com)이 여러분이 막막하지 않게 기초를 익히도록 도와줍니다.

경험이 많은 시니어 개발자라면, 라라벨은 [의존성 주입](/docs/11.x/container), [단위 테스트](/docs/11.x/testing), [큐](/docs/11.x/queues), [실시간 이벤트](/docs/11.x/broadcasting) 등 전문가용 고급 도구를 제공합니다. 라라벨은 전문적인 웹 애플리케이션 구축에 최적화되어 있으며, 엔터프라이즈 규모의 워크로드까지도 감당할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 뛰어난 확장성을 가지고 있습니다. PHP의 확장 친화적인 특성과, Redis와 같은 빠르고 분산 가능한 캐시 시스템에 대한 내장 지원 덕분에, 라라벨을 이용한 수평 확장은 매우 간단합니다. 실제로, 라라벨 애플리케이션은 월 수억 건의 요청을 무리 없이 처리하도록 손쉽게 확장된 경험이 있습니다.

더 극한의 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 통해 AWS의 최신 서버리스 기술 위에서 사실상 무한대에 가까운 확장을 이룰 수 있습니다.

#### 커뮤니티 중심의 프레임워크

라라벨은 PHP 생태계에서 최고의 패키지를 결합해, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 재능 있는 개발자들이 [라라벨 프레임워크에 기여](https://github.com/laravel/framework)했습니다. 언젠가는 여러분도 라라벨 컨트리뷰터가 될지 모릅니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성

<a name="installing-php"></a>
### PHP 및 라라벨 인스톨러 설치

첫 라라벨 애플리케이션을 생성하기 전에 여러분의 로컬 환경에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 인스톨러](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한 애플리케이션의 프론트엔드 에셋을 컴파일하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

만약 아직 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer, 라라벨 인스톨러를 한 번에 설치할 수 있습니다:

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

위 명령어 중 하나를 실행한 뒤, 터미널 세션을 재시작해야 합니다. 추후 `php.new`를 통해 설치한 PHP, Composer, 라라벨 인스톨러를 최신으로 유지하려면, 터미널에서 동일한 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer로 라라벨 인스톨러를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> GUI 기반으로 PHP를 설치하고 관리하고 싶다면 [Laravel Herd](#local-installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, 라라벨 인스톨러 설치가 완료되었다면 이제 새 라라벨 애플리케이션을 만들 준비가 되었습니다. 라라벨 인스톨러는 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트 선택을 안내합니다:

```nothing
laravel new example-app
```

애플리케이션이 생성되면 `dev` Composer 스크립트를 사용해 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 동시에 시작할 수 있습니다:

```nothing
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 접속할 수 있습니다. 이제 [라라벨 생태계의 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 물론, 원한다면 [데이터베이스를 설정](#databases-and-migrations)할 수도 있습니다.

> [!NOTE]  
> 라라벨 애플리케이션을 보다 빠르게 시작하고 싶다면, 공식 [스타터 키트](/docs/11.x/starter-kits)를 활용해보세요. 라라벨 스타터 키트는 신규 라라벨 애플리케이션에 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 설정 항목에는 설명이 달려 있으니, 파일을 살펴보며 어떤 옵션들이 제공되는지 익혀두는 것이 좋습니다.

라라벨은 기본적으로 거의 추가 설정이 필요 없기 때문에, 바로 개발을 시작할 수 있습니다! 하지만, `config/app.php` 파일과 그 항목에 대한 문서를 한 번 검토해볼 것을 추천합니다. 이 파일에는 여러분의 애플리케이션에 맞게 바꿔야 할 수도 있는 `url`, `locale` 등 여러 옵션도 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

라라벨의 많은 설정값들은 로컬 PC에서 구동할 때와 프로덕션 서버에서 구동할 때 달라질 수 있습니다. 그래서 중요한 설정값들은 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의됩니다.

`.env` 파일은 버전 관리 시스템(소스 컨트롤)에 포함시키지 않아야 합니다. 왜냐하면 각 개발자나 서버별로 환경 설정이 다를 수 있으며, 악의를 가진 사용자가 소스 저장소에 접근한다면 민감정보(자격증명 등)가 노출될 수 있기 때문입니다.

> [!NOTE]  
> `.env` 파일 및 환경 기반 설정에 대한 자세한 내용은 [설정 관련 전체 문서](/docs/11.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션

라라벨 애플리케이션을 생성했다면 이제 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 파일에는 라라벨이 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션 생성 과정에서 라라벨은 `database/database.sqlite` 파일을 자동 생성하고, 기본적인 데이터베이스 테이블을 만들기 위한 마이그레이션도 실행합니다.

만약 MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 파일에서 알맞은 값으로 수정하면 됩니다. 예를 들어, MySQL을 사용하려면 `.env` 파일 내의 `DB_*` 변수를 다음과 같이 변경합니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

만약 SQLite가 아닌 다른 데이터베이스를 선택했다면, 데이터베이스를 직접 생성한 후 [데이터베이스 마이그레이션](/docs/11.x/migrations) 명령어를 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]  
> macOS 또는 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치하려면 [Herd Pro](https://herd.laravel.com/#plans) 사용을 추천합니다.

<a name="directory-configuration"></a>
### 디렉터리 설정

라라벨 애플리케이션은 반드시 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨을 구동하려 시도하면, 애플리케이션 내의 민감한 파일들이 외부에 노출될 수 있습니다.

<a name="local-installation-using-herd"></a>
## Herd를 사용한 로컬 설치 (Local Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS 및 Windows에서 빠르게 라라벨 및 PHP 개발 환경을 구축할 수 있는 네이티브 개발 환경입니다. Herd만 설치하면 라라벨 개발에 필요한 PHP, Nginx 등 모든 구성요소가 포함되어 있어, 바로 개발을 시작할 수 있습니다.

Herd를 설치하면, `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 다양한 커맨드라인 도구도 함께 제공됩니다.

> [!NOTE]  
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 강력한 기능을 추가합니다. Herd Pro에서는 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 확인, 로그 모니터링 등의 기능을 제공합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용

macOS에서 개발 중이라면 [Herd 웹사이트](https://herd.laravel.com)에서 인스톨러를 다운로드할 수 있습니다. 설치 프로그램은 최신 PHP 버전을 자동 다운로드하며, [Nginx](https://www.nginx.com/)도 백그라운드에서 항상 실행되도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 "주차(Parked)" 디렉터리 기능을 지원합니다. 주차된 디렉터리 안의 모든 라라벨 애플리케이션은 자동으로 Herd에서 서비스되며, 기본적으로 `~/Herd` 디렉터리를 주차 디렉터리로 만듭니다. 이 디렉터리 안의 모든 라라벨 앱에 도메인명 `.test`를 붙여 접속할 수 있습니다.

설치 이후, 가장 빠르게 라라벨 애플리케이션을 만드는 방법은 Herd에 포함된 Laravel CLI를 활용하는 것입니다:

```nothing
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, 주차 디렉터리 관리나 기타 PHP 설정은 시스템 트레이 메뉴의 Herd UI를 열어 손쉽게 관리할 수 있습니다.

추가 정보는 [Herd 공식 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용

[Herd 웹사이트](https://herd.laravel.com/windows)에서 Windows용 Herd 인스톨러를 다운로드할 수 있습니다. 설치가 완료되면 Herd를 실행해 온보딩 과정을 마치고, 처음으로 Herd UI를 사용할 수 있습니다.

Herd UI는 시스템 트레이에 있는 Herd 아이콘을 왼쪽 클릭하면 접근할 수 있습니다. 아이콘을 오른쪽 클릭하면 일상적으로 필요한 각종 도구에 빠르게 접근할 수 있는 메뉴가 나타납니다.

설치 시, Herd는 홈 디렉터리에 `%USERPROFILE%\Herd`라는 이름의 "주차(Parked)" 디렉터리를 만듭니다. 이 디렉터리 안의 모든 라라벨 앱은 Herd가 자동으로 서비스하며, 디렉터리명에 `.test` 도메인을 붙여 바로 접속할 수 있습니다.

설치가 끝나면, Herd에 포함된 Laravel CLI로 새 라라벨 애플리케이션을 가장 빠르게 만들 수 있습니다. Powershell을 열어 아래 명령어를 실행하면 됩니다:

```nothing
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

추가 정보는 [Windows용 Herd 공식 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="docker-installation-using-sail"></a>
## Sail을 이용한 Docker 설치 (Docker Installation Using Sail)

OS 환경에 상관없이 라라벨을 쉽게 시작할 수 있도록 다양한 방법을 제공하고 있습니다. 그 중 한 가지는 [Sail](/docs/11.x/sail)입니다. Sail은 [Docker](https://www.docker.com)를 활용해 라라벨 애플리케이션을 구동하는 솔루션으로, 복잡한 서버나 데이터베이스 설정 없이 개발 환경을 구축할 수 있습니다.

Docker는 애플리케이션과 서비스를 작은 컨테이너라는 격리된 환경에서 구동하는 툴로, 로컬 시스템의 기존 소프트웨어나 설정과 충돌하지 않습니다. 즉, 웹 서버나 데이터베이스 등의 복잡한 개발 도구를 직접 설치·설정할 필요 없이 간편하게 환경을 구성할 수 있습니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop) 설치만 필요합니다.

라라벨 Sail은 라라벨 기본 Docker 설정과 상호작용할 수 있는 가벼운 커맨드라인 인터페이스입니다. Dockerd와 미리 지식 없이도 PHP, MySQL, Redis 기반 라라벨 앱 개발을 바로 시작할 수 있습니다.

> [!NOTE]  
> Docker에 익숙하신가요? Sail의 모든 동작은 함께 제공되는 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail 사용

Mac에서 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 간단한 터미널 명령어로 새 라라벨 애플리케이션을 만들 수 있습니다. 예를 들어 "example-app" 디렉터리에 라라벨 앱을 만들려면:

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론 "example-app" 대신 원하는 이름을 사용할 수 있습니다. 단, 앱 이름에는 영어 대소문자, 숫자, 대시(-), 밑줄(_)만 사용할 수 있습니다. 라라벨 앱의 디렉터리는 명령 실행 위치에 생성됩니다.

Sail 설치는 로컬에서 앱 컨테이너를 빌드하는 데 몇 분 정도 걸릴 수 있습니다.

앱이 생성된 후에는 해당 디렉터리로 이동해 Sail을 실행합니다. Sail은 라라벨의 기본 Docker 환경과 상호작용할 수 있는 간단한 CLI를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 준비되면, 애플리케이션의 [데이터베이스 마이그레이션](/docs/11.x/migrations)도 실행하세요:

```shell
./vendor/bin/sail artisan migrate
```

마지막으로, 웹 브라우저에서 http://localhost로 앱에 접속할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대해 더 자세히 알아보려면 [자세한 공식 문서](/docs/11.x/sail)를 참고하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail 사용

Windows PC에서 새 라라벨 애플리케이션을 만들기 전 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 먼저 설치해야 합니다. 다음으로 "Windows Subsystem for Linux 2 (WSL2)"가 설치·활성화되어 있는지 확인하세요. WSL2는 Windows 10에서 리눅스 바이너리 실행을 지원해줍니다. 설치 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 참고하세요.

> [!NOTE]  
> WSL2 설치 후 Docker Desktop이 [WSL2 백엔드로 동작하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)해야 합니다.

이제 준비가 되었다면, [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행해 WSL2 리눅스 환경으로 새 터미널 세션을 여세요. 그리고 아래 명령어로 새 라라벨 앱을 생성할 수 있습니다(예: "example-app" 디렉터리에 생성):

```shell
curl -s https://laravel.build/example-app | bash
```

"example-app" 대신 원하는 이름을 사용해도 됩니다. 단, 이름에는 영어, 숫자, 대시(-), 밑줄(_)만 사용할 수 있습니다. 앱의 디렉터리는 명령을 실행한 위치에 생성됩니다.

Sail 설치 시 로컬에 컨테이너를 빌드하므로 몇 분 정도 소요될 수 있습니다.

앱이 만들어지면 해당 디렉터리로 이동해 Sail을 실행합니다:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 준비되었으면, [데이터베이스 마이그레이션](/docs/11.x/migrations)도 실행해야 합니다.

```shell
./vendor/bin/sail artisan migrate
```

마지막으로, 브라우저에서 http://localhost로 앱을 확인할 수 있습니다.

> [!NOTE]  
> 라라벨 Sail에 대한 더 많은 정보는 [공식 문서](/docs/11.x/sail)를 참고하세요.

#### WSL2에서 개발하기

WSL2에서 생성된 라라벨 앱의 파일을 수정하려면 적절한 코드 편집기가 필요합니다. Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 [원격 개발(REMOTE) 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 사용하는 것이 좋습니다.

설치가 끝나면, Windows Terminal에서 애플리케이션 루트 디렉터리에서 `code .` 명령을 실행하면 Visual Studio Code로 해당 앱을 열 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail 사용

Linux에서 개발하고 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면, 간단한 커맨드로 라라벨 애플리케이션을 만들 수 있습니다.

먼저, Docker Desktop for Linux를 사용 중이라면 아래 명령어를 실행하세요. 사용 중이 아니라면 이 단계는 건너뛰어도 됩니다.

```shell
docker context use default
```

그리고 "example-app" 디렉터리에 새 라라벨 앱을 만들려면 다음과 같이 입력합니다.

```shell
curl -s https://laravel.build/example-app | bash
```

예시의 "example-app"은 원하는 이름으로 바꿀 수 있습니다. 단, 앱 이름은 영어, 숫자, 대시(-), 밑줄(_)만 가능합니다. 앱 디렉터리는 현재 위치에 생성됩니다.

Sail 설치는 로컬에서 컨테이너 빌드 때문에 몇 분 정도 걸릴 수 있습니다.

이후 앱 디렉터리로 이동 후 Sail을 실행하고:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 시작되면 애플리케이션의 [데이터베이스 마이그레이션](/docs/11.x/migrations) 명령을 실행하세요.

```shell
./vendor/bin/sail artisan migrate
```

완료 후 웹 브라우저에서 http://localhost로 접속해 확인할 수 있습니다.

> [!NOTE]  
> 추가로 Sail에 대해 알고 싶다면, [공식 문서](/docs/11.x/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 통해 신규 라라벨 애플리케이션을 생성할 때, `with` 쿼리 문자열로 `docker-compose.yml`에 어떤 서비스가 추가될지 선택할 수 있습니다. 사용 가능한 서비스는 `mysql`, `pgsql`, `mariadb`, `redis`, `valkey`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit`입니다.

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

특정 서비스를 지정하지 않으면 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`의 기본 스택이 설정됩니다.

또한 URL에 `devcontainer` 파라미터를 추가하면, Sail이 기본 [Devcontainer](/docs/11.x/sail#using-devcontainers)도 설치합니다.

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 개발 시 어떤 코드 에디터든 사용할 수 있지만, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 라라벨 및 그 생태계에 대한 강력한 지원(예: [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html))을 제공합니다.

또한, 커뮤니티에서 유지보수하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동완성, 유효성 검증 규칙 자동완성 등 다양한 유용한 IDE 기능을 제공합니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션을 연결하는 강력한 도구입니다. Boost는 AI 에이전트가 라라벨 고유의 맥락, 도구, 지침에 접근할 수 있게 하여, 더 정확하고 버전에 특화된 라라벨 코드를 생성할 수 있게 도와줍니다.

Boost를 애플리케이션에 설치하면, AI 에이전트는 15가지 이상의 특별한 도구(사용 중인 패키지 정보 확인, 데이터베이스 쿼리, 라라벨 공식 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker 통한 코드 실행 등)에 접근할 수 있습니다.

또한, Boost는 17,000개 이상의 벡터화된 라라벨 생태계 공식 문서(프로젝트에 설치된 실제 패키지 버전별)를 AI가 활용할 수 있게 합니다. 이를 통해 에이전트는 여러분이 사용하는 바로 그 버전에 맞춘 안내와 조언을 제공합니다.

Boost에는 라라벨에서 관리하는 AI 가이드라인도 포함되어 있습니다. 이는 에이전트가 프레임워크의 컨벤션을 따르고, 적절한 테스트를 작성하며, 흔한 실수를 방지하도록 유도합니다.

<a name="installing-laravel-boost"></a>
### 라라벨 Boost 설치

Boost는 PHP 8.1 이상을 사용하는 라라벨 10, 11, 12 버전에서 설치할 수 있습니다. 시작하려면, 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후에는 인터랙티브 인스톨러를 실행합니다:

```shell
php artisan boost:install
```

인스톨러는 아이디이(IDE)와 AI 에이전트를 자동으로 감지해, 프로젝트에 맞는 기능만 선택적으로 적용할 수 있게 도와줍니다. Boost는 기존 프로젝트의 컨벤션을 존중하며, 기본적으로 과도한 스타일 규칙을 강요하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알아보려면 [라라벨 Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

라라벨 애플리케이션을 생성한 뒤, 무엇을 먼저 공부해야 할지 고민이라면 아래 문서를 읽어보실 것을 강력히 추천합니다. 라라벨의 동작 방식을 이해하는 데 큰 도움이 됩니다.

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/11.x/lifecycle)
- [설정](/docs/11.x/configuration)
- [디렉터리 구조](/docs/11.x/structure)
- [프론트엔드](/docs/11.x/frontend)
- [서비스 컨테이너](/docs/11.x/container)
- [파사드(Facades)](/docs/11.x/facades)

</div>

여러분이 라라벨을 어떻게 활용할지에 따라 앞으로 배워야 할 방향도 달라질 수 있습니다. 라라벨을 사용하는 다양한 방법이 있지만, 여기서는 대표적인 두 가지 사용 목적을 안내합니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)에 참여해 실습을 통해 처음부터 애플리케이션을 만들어보세요.

<a name="laravel-the-fullstack-framework"></a>
### 라라벨 풀스택 프레임워크로 활용하기

라라벨은 풀스택 프레임워크로 동작할 수 있습니다. "풀스택" 프레임워크란 라라벨이 라우팅만 담당하는 것이 아니라, [Blade 템플릿](/docs/11.x/blade)이나 [Inertia](https://inertiajs.com)와 같은 SPA 하이브리드 기술을 활용해 프론트엔드 렌더링까지 전부 담당할 수 있다는 뜻입니다. 이는 가장 일반적이면서, 생산성 면에서 라라벨을 활용하는 가장 좋은 방법입니다.

이 방식으로 라라벨을 쓸 예정이라면 [프론트엔드 개발](/docs/11.x/frontend), [라우팅](/docs/11.x/routing), [뷰(Views)](/docs/11.x/views), [Eloquent ORM](/docs/11.x/eloquent) 문서를 참고해보세요. 또한 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지도 관심을 가져 볼 만합니다. 이 패키지들은 싱글페이지 자바스크립트 앱의 UI 장점을 누리면서 라라벨을 풀스택 프레임워크처럼 활용할 수 있도록 도와줍니다.

CSS와 자바스크립트 자산을 [Vite](/docs/11.x/vite)로 컴파일하는 방법도 꼭 익혀두기를 권장합니다.

> [!NOTE]  
> 애플리케이션 개발을 더욱 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/11.x/starter-kits)를 참고하세요.

<a name="laravel-the-api-backend"></a>
### 라라벨을 API 백엔드로 활용하기

라라벨은 자바스크립트 싱글페이지 애플리케이션 또는 모바일 앱의 API 백엔드 역할도 할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 앱의 API 백엔드로 라라벨을 사용할 수 있습니다. 이런 방식에서는 라라벨이 [인증](/docs/11.x/sanctum) 및 데이터 저장/조회 기능을 제공하며, 강력한 큐, 이메일, 알림 등 다양한 서비스를 함께 사용할 수 있습니다.

API 백엔드로 라라벨을 사용할 계획이라면 [라우팅](/docs/11.x/routing), [Laravel Sanctum](/docs/11.x/sanctum), [Eloquent ORM](/docs/11.x/eloquent) 관련 문서도 읽어보세요.

> [!NOTE]  
> 라라벨 백엔드와 Next.js 프론트엔드를 빠르게 구축하고 싶다면, Laravel Breeze의 [API 스택](/docs/11.x/starter-kits#breeze-and-next) 및 [Next.js 프론트엔드 구현체](https://github.com/laravel/breeze-next)를 통해 몇 분 만에 시작할 수 있습니다.
