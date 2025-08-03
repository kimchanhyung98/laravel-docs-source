# 설치 (Installation)

- [Laravel 소개](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치 도구 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉토리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd](#herd-on-macos)
    - [Windows에서 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 소개 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만드는 데 구조와 시작점을 제공하며, 이를 통해 세부 사항에 신경 쓰지 않고도 멋진 애플리케이션을 만드는 데 집중할 수 있습니다.

Laravel은 뛰어난 개발자 경험을 제공하는 동시에, 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능들을 포함하고 있습니다.

PHP 웹 프레임워크에 익숙하지 않은 초보자든 오래된 숙련자든 Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로 첫발을 내딛거나, 이미 가진 전문성을 한 단계 끌어올리는 데 도움을 드릴 것입니다. 여러분이 무엇을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 만들 때 사용할 수 있는 도구와 프레임워크가 다양하지만, 우리는 Laravel이 현대적인 풀스택 웹 애플리케이션 구축에 가장 적합한 선택이라고 믿습니다.

#### 진보적인 프레임워크

우리는 Laravel을 "진보적(progressive)"인 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장한다는 의미입니다. 웹 개발에 첫발을 내딛는 초보자라면, Laravel의 방대한 문서, 가이드, 그리고 [비디오 튜토리얼](https://laracasts.com)이 여러분이 부담 없이 배울 수 있도록 도와줍니다.

숙련 개발자라면 Laravel은 [의존성 주입](/docs/master/container), [단위 테스트](/docs/master/testing), [큐](/docs/master/queues), [실시간 이벤트](/docs/master/broadcasting) 등 전문적인 웹 애플리케이션 구축에 필요한 강력한 도구를 제공합니다. Laravel은 엔터프라이즈급 작업 부하도 감당할 수 있도록 최적화되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적 특성과 Redis 같은 빠른 분산 캐시 시스템에 대한 내장 지원 덕분에, Laravel으로의 수평적 확장이 매우 쉽습니다. 실제로 Laravel 애플리케이션은 한 달에 수억 건의 요청도 문제없이 처리해 왔습니다.

극한의 확장이 필요한 경우, [Laravel Cloud](https://cloud.laravel.com) 같은 플랫폼을 사용해 거의 무한대 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 중심 프레임워크

Laravel은 PHP 생태계에서 가장 견고하고 개발자 친화적인 프레임워크를 제공하기 위해 최고의 패키지를 결합했습니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 이 프레임워크에 [기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있을지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel 설치 도구 설치 (Installing PHP and the Laravel Installer)

첫 Laravel 애플리케이션을 만들기 전에, 로컬 컴퓨터에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel installer](https://github.com/laravel/installer)가 설치되어 있어야 합니다. 또한 애플리케이션의 프런트엔드 자산을 컴파일하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치하는 것도 권장합니다.

만약 로컬에 PHP와 Composer가 없다면, 아래 명령어로 macOS, Windows, Linux 환경에 PHP, Composer, Laravel 설치 도구를 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행하세요...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작하는 것이 좋습니다. `php.new`를 통해 설치한 PHP, Composer, Laravel 설치 도구를 업데이트하려면 동일 명령을 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 사용해 Laravel 설치 도구만 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 기능이 완비된 그래픽 기반 PHP 설치 및 관리 경험이 필요하다면, [Laravel Herd](#installation-using-herd)를 확인하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel 설치 도구를 설치했다면, 이제 새 Laravel 애플리케이션을 생성할 준비가 된 것입니다. Laravel 설치 도구는 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택하도록 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 생성되면, 다음 명령어로 Laravel의 로컬 개발 서버, 큐 작업자 및 Vite 개발 서버를 시작할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 실행되면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 으로 접속해 애플리케이션을 확인할 수 있습니다. 다음으로는 [Laravel 생태계의 다음 단계](#next-steps)를 시작할 준비가 된 것입니다. 물론 [데이터베이스 설정](#databases-and-migrations)을 먼저 진행할 수도 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발에 빠르게 착수하고 싶다면, 다양한 [스타터 키트](/docs/master/starter-kits) 사용을 고려해보세요. Laravel의 스타터 키트는 백엔드 및 프런트엔드 인증 골격 코드를 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크 관련 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션은 문서화되어 있으니, 필요에 따라 파일들을 살펴보며 어떤 옵션들이 있는지 익히는 것을 추천합니다.

Laravel은 기본적으로 별도의 추가 설정이 거의 필요 없습니다. 바로 개발을 시작할 수 있습니다! 하지만 `config/app.php` 파일과 해당 문서를 검토하면 `url`, `locale` 등의 여러 옵션을 애플리케이션에 맞게 변경할 수 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

Laravel의 많은 설정 값은 애플리케이션이 로컬 개발 환경인지, 프로덕션 서버인지에 따라 달라질 수 있기 때문에, 중요한 설정 값들은 애플리케이션 루트에 위치한 `.env` 파일에서 정의됩니다.

`.env` 파일은 각 개발자나 서버가 환경 구성이 달라질 수 있으므로 소스 코드 관리에 포함하지 않아야 합니다. 또한, `.env`에 민감한 인증 정보가 포함될 수 있으므로, 저장소에 노출되는 보안 위험을 방지할 수 있습니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 설정에 대한 자세한 내용은 [환경 설정 문서](/docs/master/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

Laravel 애플리케이션을 만들고 나면, 데이터를 저장할 데이터베이스가 필요할 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션 생성 시, Laravel은 `database/database.sqlite` 파일을 만들어주고, 애플리케이션 데이터베이스 테이블 생성을 위한 필수 마이그레이션도 실행합니다.

MySQL이나 PostgreSQL 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일 내 `DB_*` 변수를 해당 데이터베이스에 맞게 바꿔주세요. 예를 들어 MySQL을 사용하려면 다음과 같이 `.env` 파일을 수정합니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 외의 데이터베이스를 사용할 경우, 데이터베이스를 직접 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/master/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows에서 MySQL, PostgreSQL, Redis를 로컬 설치해야 할 경우, [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 고려해보세요.

<a name="directory-configuration"></a>
### 디렉토리 설정 (Directory Configuration)

Laravel은 웹 서버에서 "웹 디렉토리"의 루트에서 제공되어야 합니다. Laravel 애플리케이션을 "웹 디렉토리"의 하위 디렉토리에서 제공하려고 시도하면, 애플리케이션 내부에 존재하는 민감한 파일이 노출될 위험이 있으므로 피해야 합니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows용 네이티브 Laravel 및 PHP 개발 환경으로 매우 빠릅니다. Herd에는 PHP, Nginx 포함, Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다.

Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등의 명령줄 도구도 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가로 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰어, 로그 모니터링과 같은 강력한 기능을 더합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd (Herd on macOS)

macOS 개발자라면 [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 PHP 버전을 자동으로 다운로드하고, macOS에서 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 실행되도록 설정합니다.

macOS용 Herd는 "parked" 디렉토리를 지원하기 위해 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용합니다. park된 디렉토리 내의 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd` 위치에 park된 디렉토리를 생성하며, 이 디렉토리 내 애플리케이션은 `.test` 도메인으로 디렉토리 이름을 사용해 접속할 수 있습니다.

Herd 설치 후, Laravel CLI가 Herd에 포함되어 있어 가장 빠른 방법으로 새 Laravel 애플리케이션을 생성할 수 있습니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 park된 디렉토리 관리 및 PHP 설정을 조작할 수도 있습니다.

더 자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd (Herd on Windows)

Windows에서 Herd 설치 프로그램은 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면 Herd를 시작해 온보딩 프로세스를 완료하고, 최초로 Herd UI에 접속할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 좌클릭하면 접근 가능하며, 우클릭 시 일상적으로 필요한 도구에 빠르게 접근할 수 있는 메뉴가 열립니다.

설치 과정에서 `"%USERPROFILE%\Herd"` 위치에 "parked" 디렉토리가 생성됩니다. 이 디렉토리 내 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, `.test` 도메인에서 디렉토리 이름으로 접속할 수 있습니다.

설치 후 Laravel CLI가 Herd에 포함되어 있기 때문에, 다음 명령어로 빠르게 새 애플리케이션을 생성할 수 있습니다. PowerShell을 열고 아래를 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

더 자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참조하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션 개발에는 원하는 코드 에디터를 자유롭게 사용할 수 있지만, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 Laravel과 그 생태계에 대한 광범위한 지원을 제공합니다. 예를 들어 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html)도 포함되어 있습니다.

또한, 커뮤니티가 유지하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 구문 완성, 유효성 검사 규칙 완성과 같은 다양한 유용한 IDE 기능을 지원합니다.

[Visual Studio Code (VS Code)](https://code.visualstudio.com)를 사용하는 경우, 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 설치하면 Laravel 특정 툴들이 VS Code 환경 내로 통합되어 생산성을 높일 수 있습니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 Laravel 애플리케이션을 생성했으니 무엇을 학습할지 궁금할 것입니다. 먼저, Laravel 작동 방식을 익히기 위해 다음 문서들을 읽어보길 강력히 추천합니다:

<div class="content-list" markdown="1">

- [요청 수명 주기](/docs/master/lifecycle)
- [설정](/docs/master/configuration)
- [디렉토리 구조](/docs/master/structure)
- [프런트엔드](/docs/master/frontend)
- [서비스 컨테이너](/docs/master/container)
- [파사드](/docs/master/facades)

</div>

Laravel 활용법에 따라 다음 학습 방향도 달라집니다. 여기서는 Laravel의 두 가지 주요 사용 사례를 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. "풀스택"이라고 할 때는, Laravel이 애플리케이션으로 향하는 요청을 라우팅하고, [Blade 템플릿](/docs/master/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술을 통해 프런트엔드를 렌더링하는 방식을 의미합니다. 이것이 Laravel을 사용하는 가장 흔하고 생산적인 방법입니다.

이런 식으로 Laravel을 사용한다면, [프런트엔드 개발](/docs/master/frontend), [라우팅](/docs/master/routing), [뷰](/docs/master/views), [Eloquent ORM](/docs/master/eloquent) 문서를 확인해보세요. 또한, [Livewire](https://livewire.laravel.com)와 [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지도 흥미로울 것입니다. 이 패키지들은 싱글 페이지 자바스크립트 애플리케이션이 제공하는 UI 장점을 누리면서 Laravel을 풀스택 프레임워크로 활용할 수 있게 도와줍니다.

또한, Laravel을 풀스택 프레임워크로 사용하는 경우, [Vite](/docs/master/vite)를 이용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 익히시길 권장합니다.

> [!NOTE]
> 빠르게 개발을 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/master/starter-kits)를 활용해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel (Laravel the API Backend)

Laravel은 JavaScript 싱글 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드 역할도 할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 앱의 API 백엔드로 Laravel을 사용할 수 있습니다. 이런 경우 Laravel은 애플리케이션의 [인증](/docs/master/sanctum)과 데이터 저장/조회 기능을 제공하면서 큐, 이메일, 알림 등 Laravel의 강력한 서비스도 활용할 수 있습니다.

이렇게 Laravel을 사용하려면 [라우팅](/docs/master/routing), [Laravel Sanctum](/docs/master/sanctum), [Eloquent ORM](/docs/master/eloquent) 문서를 참조하세요.