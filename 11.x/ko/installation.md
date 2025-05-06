# 설치

- [Laravel 만나보기](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성하기](#creating-a-laravel-project)
    - [PHP 및 Laravel 인스톨러 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 로컬 설치](#local-installation-using-herd)
    - [macOS용 Herd](#herd-on-macos)
    - [Windows용 Herd](#herd-on-windows)
- [Sail을 이용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서 Sail 사용](#sail-on-macos)
    - [Windows에서 Sail 사용](#sail-on-windows)
    - [Linux에서 Sail 사용](#sail-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나보기

Laravel은 표현력이 뛰어나고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 여러분이 세부 사항에 신경 쓰지 않고도 멋진 무언가를 만드는 데 집중할 수 있게 해줍니다.

Laravel은 뛰어난 개발자 경험을 제공하는 동시에 강력한 기능들을 제공합니다. 이에는 완전한 의존성 주입, 표현력 있는 데이터베이스 추상화 레이어, 큐와 예약된 작업, 단위 및 통합 테스트 등이 포함됩니다.

PHP 웹 프레임워크가 처음인 분이든, 경험이 많은 분이든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫 걸음을 내딛는 것을 돕거나, 여러분이 전문성을 한 단계 끌어올릴 수 있도록 도와줍니다. 여러분이 무엇을 만들어낼지 기대가 큽니다.

> [!NOTE]  
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)에서 직접 실습하며 프레임워크를 익히고, 첫 Laravel 애플리케이션을 만드는 과정을 따라가 보세요.

<a name="why-laravel"></a>
### 왜 Laravel인가?

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 저희는 Laravel이 최신의 풀스택 웹 애플리케이션을 만드는 데 최고의 선택이라고 믿습니다.

#### 발전형(Progressive) 프레임워크

Laravel은 "발전형(progresive)" 프레임워크라고 부릅니다. 이는 Laravel이 여러분의 성장에 맞춰 함께 발전한다는 의미입니다. 웹 개발에 처음 입문했다면, Laravel의 방대한 문서, 가이드, [영상 튜토리얼](https://laracasts.com)을 통해 부담 없이 기초를 익힐 수 있습니다.

숙련된 개발자라면, Laravel은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 전문적인 웹 애플리케이션을 만드는 데 필요한 강력한 도구를 제공합니다. Laravel은 기업 수준의 요구사항도 충분히 감당할 준비가 되어 있습니다.

#### 확장성 높은 프레임워크

Laravel은 놀라울 정도로 확장성이 높습니다. PHP의 확장성에 친화적인 특성과 Redis와 같은 빠른 분산 캐시 시스템에 내장 지원을 제공함으로써, Laravel로 수평 확장이 매우 수월합니다. 실제로, Laravel 애플리케이션은 월 수억 건의 요청을 처리할 정도로 손쉽게 확장되었습니다.

더 극단적인 확장이 필요한가요? [Laravel Vapor](https://vapor.laravel.com)와 같은 플랫폼을 이용하면 AWS의 최신 서버리스 기술에서 거의 무한한 확장성을 갖고 Laravel 애플리케이션을 실행할 수 있습니다.

#### 커뮤니티 중심의 프레임워크

Laravel은 PHP 생태계의 최고의 패키지들을 결합해 가장 견고하면서 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 Laravel의 기여자가 될 수 있을지 모릅니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성하기

<a name="installing-php"></a>
### PHP 및 Laravel 인스톨러 설치

처음 Laravel 애플리케이션을 만들기 전, 로컬 컴퓨터에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel 인스톨러](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프론트엔드 자산을 컴파일하려면 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬 컴퓨터에 아직 PHP와 Composer가 없다면, 아래의 명령어로 macOS, Windows, 또는 Linux에서 PHP, Composer, 그리고 Laravel 인스톨러를 설치할 수 있습니다:

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

위의 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`로 설치한 후, PHP, Composer, Laravel 인스톨러를 업데이트하려면 터미널에서 해당 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 인스톨러를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 기능의 그래픽 PHP 설치 및 관리 환경이 필요하다면, [Laravel Herd](#local-installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, Laravel 인스톨러를 설치했다면, 이제 새로운 Laravel 애플리케이션을 만들 준비가 끝났습니다. Laravel 인스톨러는 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트 선택을 안내합니다:

```nothing
laravel new example-app
```

애플리케이션이 생성되면 `dev` Composer 스크립트를 사용하여 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 시작할 수 있습니다:

```nothing
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다. 이제 [Laravel 에코시스템을 더 알아보는 것](#next-steps)도 좋고, [데이터베이스를 설정](#databases-and-migrations)할 수도 있습니다.

> [!NOTE]  
> 더 빠르게 Laravel 애플리케이션 개발을 시작하고 싶다면 [스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하는 것도 고려해보세요. Laravel의 스타터 키트는 인증 scaffolding을 포함한 백엔드와 프론트엔드 구조를 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 문서가 작성되어 있으니, 설정 파일을 둘러보고 사용 가능한 옵션에 익숙해지는 것이 좋습니다.

Laravel은 기본값만으로도 거의 추가 설정이 필요 없습니다. 바로 개발을 시작할 수 있습니다! 하지만 `config/app.php` 파일과 그 문서를 한 번 검토하는 것이 좋습니다. 해당 파일에는 `url`, `locale` 등 여러분의 애플리케이션에 맞게 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

Laravel의 많은 설정 옵션 값은 애플리케이션이 로컬에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 설정 값들은 애플리케이션 루트의 `.env` 파일을 통해 정의됩니다.

`.env` 파일은 애플리케이션의 소스 제어에 커밋해서는 안 됩니다. 각 개발자 또는 서버가 서로 다른 환경 설정을 필요로 할 수 있기 때문입니다. 또한 이는 침입자가 소스 저장소에 접근할 경우 민감한 정보가 노출될 위험이 있습니다.

> [!NOTE]  
> `.env` 파일과 환경 기반 설정에 대한 더 자세한 정보는 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 확인하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

Laravel 애플리케이션을 만들었으니, 이제 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 `.env` 설정 파일에서는 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션 생성 시, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하며, 필요한 마이그레이션을 실행해 데이터베이스 테이블을 만들어줍니다.

MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하려면, `.env` 설정 파일의 데이터베이스 관련 부분을 다음과 같이 변경하면 됩니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 이외의 데이터베이스를 사용한다면, 데이터베이스를 직접 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]  
> macOS 또는 Windows에서 개발 중이고, 로컬에 MySQL, PostgreSQL, Redis 등을 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 사용을 고려해보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정

Laravel은 항상 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. 즉, "웹 디렉터리"의 하위 디렉터리에서 Laravel 애플리케이션을 서비스하려고 시도해서는 안 됩니다. 그렇게 하면 애플리케이션 내의 민감한 파일이 노출될 수 있습니다.

<a name="local-installation-using-herd"></a>
## Herd를 이용한 로컬 설치

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠르고, 네이티브한 Laravel 및 PHP 개발 환경입니다. Herd는 Laravel 개발을 시작하는 데 필요한 PHP, Nginx 등을 모두 포함하고 있습니다.

Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm`의 명령줄 도구가 포함되어 있습니다.

> [!NOTE]  
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰잉, 로그 모니터링 등 추가적인 강력한 기능을 제공합니다.

<a name="herd-on-macos"></a>
### macOS용 Herd

macOS에서 개발하는 경우 [Herd 웹사이트](https://herd.laravel.com)에서 Herd 인스톨러를 다운로드할 수 있습니다. 인스톨러는 최신 버전의 PHP를 자동 다운로드하고, Mac이 항상 [Nginx](https://www.nginx.com/)를 백그라운드에서 실행하도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "주차된" 디렉터리를 지원합니다. 주차 디렉터리 내의 어떤 Laravel 애플리케이션도 Herd가 자동으로 서비스합니다. 기본적으로 Herd는 `~/Herd` 경로에 주차 디렉터리를 만들고, 이 디렉터리에 있는 모든 Laravel 애플리케이션은 디렉터리 이름을 통해 `.test` 도메인에서 접근할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 함께 묶여 있는 Laravel CLI를 이용하는 것입니다:

```nothing
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, 메뉴바의 Herd 아이콘을 통해 Herd UI를 열고, 주차 디렉터리 및 기타 PHP 설정을 관리할 수도 있습니다.

더 자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows용 Herd

Windows용 Herd 인스톨러는 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면 Herd를 시작해 온보딩 절차를 마치고 처음으로 Herd UI에 접근할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하여 사용할 수 있습니다. 오른쪽 클릭하면 자주 사용하는 도구에 빠르게 접근할 수 있는 퀵 메뉴가 열립니다.

설치 중 Herd는 사용자 홈 디렉터리의 `%USERPROFILE%\Herd`에 "주차된" 디렉터리를 생성합니다. 이 디렉터리에 위치한 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 사용하여 `.test` 도메인에서 접근할 수 있습니다.

Herd 설치 이후, Laravel CLI를 이용해 새로운 애플리케이션을 즉시 만들 수 있습니다. Powershell을 열고 다음과 같이 실행하세요:

```nothing
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="docker-installation-using-sail"></a>
## Sail을 이용한 Docker 설치

운영체제 종류에 관계없이 Laravel을 간편하게 시작할 수 있도록 여러가지 옵션을 제공합니다. Laravel은 [Sail](/docs/{{version}}/sail)이라는 내장 솔루션을 통해 [Docker](https://www.docker.com)를 사용하여 Laravel 애플리케이션을 실행할 수 있게 지원합니다.

Docker는 애플리케이션과 서비스를 소형, 경량의 "컨테이너"로 실행하는 도구입니다. 컨테이너는 로컬 머신에 설치된 소프트웨어나 설정을 해치지 않으므로, 복잡한 개발 도구인 웹 서버나 데이터베이스를 직접 설치 및 구성하지 않아도 됩니다. Docker를 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치하면 됩니다.

Laravel Sail은 Laravel의 기본 Docker 설정을 다루는 경량의 커맨드라인 인터페이스입니다. PHP, MySQL, Redis 등으로 Laravel 애플리케이션을 개발하는 데 완벽한 출발점을 제공하며, Docker 경험 없이도 쉽게 사용할 수 있습니다.

> [!NOTE]  
> 이미 Docker 전문가인가요? 걱정 마세요! Sail의 모든 요소는 Laravel에 포함된 `docker-compose.yml` 파일을 이용해 자유롭게 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail 사용

Mac에서 개발하고 있으며 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 아주 간단한 터미널 명령어로 새로운 Laravel 애플리케이션을 생성할 수 있습니다. 예를 들어, "example-app"이라는 디렉터리에 새로운 Laravel 애플리케이션을 만들려면 아래 명령을 실행하세요:

```shell
curl -s "https://laravel.build/example-app" | bash
```

URL에서 "example-app" 부분은 원하는 이름으로 변경할 수 있습니다. 단, 이름에는 영숫자, 대시, 언더스코어만 사용하세요. 애플리케이션 디렉터리는 명령을 실행한 디렉터리 내에 생성됩니다.

Sail 설치는 로컬에서 애플리케이션 컨테이너를 빌드하는 동안 몇 분 정도 소요될 수 있습니다.

애플리케이션이 생성되면 디렉터리로 이동해 Laravel Sail을 사용할 수 있습니다. Sail은 Laravel의 Docker 기본 설정을 다루는 간단한 커맨드라인 인터페이스를 제공합니다:

```shell
cd example-app

./vendor/bin/sail up
```

Docker 컨테이너가 실행된 후, 애플리케이션의 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요:

```shell
./vendor/bin/sail artisan migrate
```

이제 웹 브라우저에서 http://localhost로 애플리케이션에 접근할 수 있습니다.

> [!NOTE]  
> Laravel Sail에 대해 더 알아보고 싶다면 [전체 Sail 문서](/docs/{{version}}/sail)를 확인하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail 사용

Windows에서 새로운 Laravel 애플리케이션을 만들기 전, [Docker Desktop](https://www.docker.com/products/docker-desktop)이 설치되어 있는지 확인하세요. 그리고 Windows Subsystem for Linux 2 (WSL2)가 설치 및 활성화되어 있어야 합니다. WSL2는 Windows 10에서 Linux 바이너리 실행 파일을 네이티브로 실행할 수 있게 해줍니다. WSL2 설치 및 활성화 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 참고하세요.

> [!NOTE]  
> WSL2 설치 후, Docker Desktop이 [WSL2 백엔드 사용으로 설정되었는지](https://docs.docker.com/docker-for-windows/wsl/) 확인하세요.

이제 첫 Laravel 애플리케이션을 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)를 실행하고, WSL2 Linux 운영 체제용 새 터미널 세션을 시작하세요. 그리고 다음과 같은 명령어로 Laravel 애플리케이션을 생성할 수 있습니다:

```shell
curl -s https://laravel.build/example-app | bash
```

URL 내 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름은 영숫자, 대시, 언더스코어만 사용하세요. 애플리케이션 디렉터리는 명령을 실행한 위치에 생성됩니다.

Sail 설치에는 컨테이너가 빌드되는 동안 몇 분이 소요될 수 있습니다.

애플리케이션 생성 후 디렉터리로 이동해 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 실행된 후, [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요:

```shell
./vendor/bin/sail artisan migrate
```

이제 http://localhost에서 애플리케이션에 접근할 수 있습니다.

> [!NOTE]  
> Sail에 대해 더 배우고 싶다면 [전체 Sail 문서](/docs/{{version}}/sail)를 참고하세요.

#### WSL2 환경에서 개발하기

WSL2 환경 내에 생성된 Laravel 애플리케이션 파일을 수정하려면, Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 및 공식 [Remote Development 확장팩](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)을 사용하는 것이 좋습니다.

이 도구가 설치된 상태에서, Windows Terminal을 통해 애플리케이션 루트 디렉터리에서 `code .` 명령어를 실행하면 언제든 Laravel 애플리케이션을 열 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail 사용

Linux에서 개발 중이고 이미 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 아주 간단한 터미널 명령어로 Laravel 애플리케이션을 만들 수 있습니다.

만약 Docker Desktop for Linux를 사용 중이라면, 먼저 아래 명령을 실행하세요. 사용하지 않는 경우 이 절차는 건너뛰어도 됩니다:

```shell
docker context use default
```

그 후, "example-app" 디렉터리에 새로운 Laravel 애플리케이션을 생성하려면 다음을 실행하세요:

```shell
curl -s https://laravel.build/example-app | bash
```

URL에서 "example-app" 부분은 원하는 이름으로 변경할 수 있습니다. 이름에는 영숫자, 대시, 언더스코어만 사용할 수 있습니다. 애플리케이션 디렉터리는 커맨드를 실행한 위치에 생성됩니다.

Sail 설치에는 로컬에서 컨테이너를 빌드하는 동안 몇 분이 소요될 수 있습니다.

애플리케이션 생성 후, 디렉터리로 이동해 Sail을 시작하세요:

```shell
cd example-app

./vendor/bin/sail up
```

컨테이너가 실행된 후, [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요:

```shell
./vendor/bin/sail artisan migrate
```

마지막으로, 웹 브라우저에서 http://localhost로 접근해 애플리케이션을 사용할 수 있습니다.

> [!NOTE]  
> Laravel Sail에 대해 더 상세히 배우시려면 [전체 Sail 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 통해 새 Laravel 애플리케이션을 생성할 때, `with` 쿼리 스트링 변수를 사용해 `docker-compose.yml`에 어떤 서비스를 구성할지 선택할 수 있습니다. 사용할 수 있는 서비스에는 `mysql`, `pgsql`, `mariadb`, `redis`, `valkey`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit` 등이 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

서비스를 별도로 지정하지 않으면 기본적으로 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`이 구성됩니다.

기본 [Devcontainer](/docs/{{version}}/sail#using-devcontainers)를 설치하려면 URL에 `devcontainer` 파라미터를 추가할 수 있습니다:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원

Laravel 애플리케이션 개발에는 원하는 어떤 코드 에디터든 자유롭게 사용할 수 있습니다. 그러나 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html)를 포함한 Laravel 및 에코시스템에 대한 강력한 지원을 제공합니다.

또한 커뮤니티에서 유지 보수하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 구문 완성, 검증 규칙 자동완성 등 다양한 편의 기능을 제공합니다.

<a name="next-steps"></a>
## 다음 단계

이제 Laravel 애플리케이션을 만들었으니, 앞으로 무엇을 배워야 할지 궁금할 수 있습니다. 우선, 아래의 문서에서 Laravel이 어떻게 동작하는지 익혀보시길 적극 추천합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [프론트엔드](/docs/{{version}}/frontend)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

Laravel을 어떻게 사용하고 싶은지도 여러분의 다음 단계에 영향을 줍니다. Laravel을 활용할 수 있는 여러 방법이 있으며, 대표적인 두 가지 사용 사례를 아래에서 소개합니다.

> [!NOTE]  
> Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 직접 실습하며 프레임워크의 다양한 기능을 체험해보세요.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 풀스택은, 요청을 라우팅하고 [Blade 템플릿](/docs/{{version}}/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글페이지 애플리케이션 하이브리드 기술을 사용해 프론트엔드를 렌더링할 수 있다는 뜻입니다. 이것이 Laravel을 사용하는 가장 일반적이면서, 가장 생산적인 방법이라고 생각합니다.

이 방식을 계획하고 있다면, [프론트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 관련 문서를 참고해보세요. 또한, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 등 커뮤니티 패키지도 검토해볼 가치가 있습니다. 이들 패키지를 통해 싱글페이지 JavaScript 애플리케이션의 많은 UI 이점을 누리면서도 Laravel을 풀스택 프레임워크로 사용할 수 있습니다.

풀스택 프레임워크로 Laravel을 사용한다면, [Vite](/docs/{{version}}/vite)를 이용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 반드시 익히길 추천합니다.

> [!NOTE]  
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel

Laravel은 JavaScript 싱글페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로도 사용될 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이런 경우 Laravel로 애플리케이션의 [인증](/docs/{{version}}/sanctum), 데이터 저장/조회 등을 처리하고, 큐, 이메일, 알림 등 강력한 서비스들도 활용할 수 있습니다.

이처럼 사용할 계획이라면 [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참고하시기 바랍니다.

> [!NOTE]  
> Laravel 백엔드와 Next.js 프론트엔드의 스캐폴딩을 빠르게 시작하고 싶으신가요? Laravel Breeze는 [API 스택](/docs/{{version}}/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현체](https://github.com/laravel/breeze-next)를 제공해 몇 분 만에 시작할 수 있습니다.