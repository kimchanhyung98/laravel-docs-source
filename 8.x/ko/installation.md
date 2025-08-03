# 설치 (Installation)

- [Laravel 소개](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [첫 번째 Laravel 프로젝트](#your-first-laravel-project)
    - [macOS에서 시작하기](#getting-started-on-macos)
    - [Windows에서 시작하기](#getting-started-on-windows)
    - [Linux에서 시작하기](#getting-started-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
    - [Composer를 통한 설치](#installation-via-composer)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [디렉터리 설정](#directory-configuration)
- [다음 단계](#next-steps)
    - [Laravel: 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [Laravel: API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 소개 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 가진 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 사용자가 세세한 부분에 신경 쓰기보다 멋진 것을 만드는 데 집중할 수 있게 도와줍니다.

Laravel은 광범위한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하는 동시에 뛰어난 개발자 경험을 제공합니다.

PHP나 웹 프레임워크가 처음이든, 다년간의 경험이 있든, Laravel은 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫 발걸음을 내딛거나, 더 높은 수준으로 실력을 향상할 때 Laravel이 도움을 드릴 것입니다. 여러분이 무엇을 만들지 매우 기대됩니다.

<a name="why-laravel"></a>
### 왜 Laravel인가? (Why Laravel?)

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 우리는 Laravel이 현대적이고 풀스택 웹 애플리케이션을 만드는 데 가장 좋은 선택이라고 믿습니다.

#### 점진적(프로그레시브) 프레임워크

Laravel을 "점진적(progressive)" 프레임워크라고 부르는 이유는, Laravel이 여러분과 함께 성장하기 때문입니다. 웹 개발의 첫걸음을 떼는 초보자라면, Laravel의 방대한 문서, 가이드, [비디오 튜토리얼](https://laracasts.com)이 너무 복잡하지 않게 배우는 데 도움을 줄 것입니다.

경력 많은 개발자라면 Laravel은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 견고한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션을 만들기 위해 정교하게 다듬어졌으며, 엔터프라이즈 급 업무량도 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 놀랍도록 확장 가능합니다. PHP의 확장 친화적 특성과 Redis 같은 빠른 분산 캐시 시스템을 본격 지원하기 때문에, Laravel로 수평적 확장이 매우 쉽습니다. 실제로 Laravel 애플리케이션은 월 수억 건의 요청을 무리 없이 처리해 왔습니다.

극한 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼으로 AWS 최신 서버리스 기술에서 거의 무제한 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

#### 활발한 커뮤니티 프레임워크

Laravel은 PHP 생태계 최고 패키지들을 모아 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 뛰어난 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해 왔습니다. 언젠가 여러분도 Laravel 커뮤니티의 일원이 될 수 있길 바랍니다.

<a name="your-first-laravel-project"></a>
## 첫 번째 Laravel 프로젝트 (Your First Laravel Project)

Laravel 시작을 쉽게 하기 위해 다양한 방법으로 내 컴퓨터에서 개발 및 실행할 수 있습니다. 나중에 다른 옵션도 탐색할 수 있지만, Laravel은 [Docker](https://www.docker.com) 기반 내장 솔루션인 [Sail](/docs/{{version}}/sail)를 제공합니다.

Docker는 컴퓨터에 설치된 소프트웨어나 설정에 영향을 주지 않는 작고 가벼운 “컨테이너”에서 애플리케이션과 서비스를 실행하는 도구입니다. 즉, 웹 서버나 데이터베이스 같은 복잡한 개발 도구 설정을 걱정하지 않아도 됩니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

Laravel Sail은 Laravel 기본 Docker 설정과 상호작용하기 위한 가벼운 커맨드라인 인터페이스입니다. Sail은 기본적인 Docker 경험이 없어도 PHP, MySQL, Redis를 사용하는 Laravel 애플리케이션을 쉽게 시작할 수 있도록 도와줍니다.

> [!TIP]
> 이미 Docker 전문가이신가요? 걱정 마세요! Sail의 모든 설정은 Laravel에 포함된 `docker-compose.yml` 파일을 통해 자유롭게 커스터마이징할 수 있습니다.

<a name="getting-started-on-macos"></a>
### macOS에서 시작하기 (Getting Started On macOS)

Mac에서 개발 중이며 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 간단한 터미널 명령어로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어 "example-app"이라는 디렉터리명으로 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하세요:

```nothing
curl -s "https://laravel.build/example-app" | bash
```

물론, URL의 "example-app"은 원하는 이름으로 바꿀 수 있습니다. Laravel 애플리케이션 디렉터리는 명령어를 실행한 디렉터리 내에 생성됩니다.

프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작하세요. Sail은 Laravel 기본 Docker 설정과 상호작용하기 위한 간단한 커맨드라인 인터페이스를 제공합니다:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 Sail `up` 명령을 실행할 때는 애플리케이션 컨테이너가 로컬에서 빌드되므로 몇 분 걸릴 수 있습니다. **걱정하지 마세요, 이후 시작은 훨씬 빨라집니다.**

애플리케이션의 Docker 컨테이너가 실행되면 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

> [!TIP]
> Laravel Sail에 대해 더 배우고 싶다면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="getting-started-on-windows"></a>
### Windows에서 시작하기 (Getting Started On Windows)

Windows에서 새 Laravel 애플리케이션을 만들기 전에, [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치하세요. 그 다음, Windows Subsystem for Linux 2(WSL2)가 설치되어 활성화되어 있어야 합니다. WSL은 Windows 10에서 Linux 바이너리 실행 파일을 네이티브로 구동할 수 있게 해줍니다. 설치 및 활성화 방법은 마이크로소프트 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 참고하세요.

> [!TIP]
> WSL2를 설치하고 활성화한 뒤에는 Docker Desktop이 [WSL2 백엔드를 사용하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인하세요.

준비가 되면, [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 열고 WSL2 Linux 운영체제용 새로운 터미널 세션을 시작하세요. 그리고 간단히 터미널 명령으로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어 "example-app"이라는 디렉터리명으로 Laravel 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```nothing
curl -s https://laravel.build/example-app | bash
```

URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. Laravel 애플리케이션 디렉터리는 명령어를 실행한 디렉터리 내에 생성됩니다.

프로젝트 생성 후, 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작하세요:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 `sail up` 명령 실행 시, 애플리케이션 컨테이너가 빌드되어 몇 분 걸릴 수 있습니다. **후속 실행은 훨씬 빠릅니다.**

컨테이너가 시작되면 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

> [!TIP]
> Laravel Sail을 더 알고 싶다면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

#### WSL2 내 개발

WSL2 내에 생성된 Laravel 애플리케이션 파일을 수정해야 하므로, 마이크로소프트의 [Visual Studio Code](https://code.visualstudio.com) 편집기와 그들의 공식 [원격 개발(Remote Development)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 확장 기능 사용을 추천합니다.

이 도구들이 설치되면, Windows Terminal에서 애플리케이션 루트 디렉터리에서 `code .` 명령을 실행해 Laravel 프로젝트를 바로 열 수 있습니다.

<a name="getting-started-on-linux"></a>
### Linux에서 시작하기 (Getting Started On Linux)

Linux에서 개발 중이며 [Docker Compose](https://docs.docker.com/compose/install/)가 설치되어 있다면, 간단한 터미널 명령으로 새 Laravel 프로젝트를 생성할 수 있습니다. 예를 들어 "example-app"이라는 이름으로 새 Laravel 애플리케이션을 만들려면 다음 명령어를 실행하세요:

```nothing
curl -s https://laravel.build/example-app | bash
```

물론 "example-app"은 원하는 이름으로 변경 가능합니다. Laravel 애플리케이션 디렉터리는 명령어 실행 위치에 생성됩니다.

프로젝트가 생성되면 애플리케이션 디렉터리로 이동한 후 Laravel Sail을 시작하세요:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 `sail up` 명령 실행 시 애플리케이션 컨테이너 빌드로 몇 분 걸릴 수 있습니다. **이후 실행은 빠릅니다.**

컨테이너가 실행되면 웹 브라우저에서 http://localhost를 통해 애플리케이션에 접속할 수 있습니다.

> [!TIP]
> Laravel Sail의 자세한 내용은 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기 (Choosing Your Sail Services)

Sail로 새 Laravel 애플리케이션을 만들 때, `with` 쿼리 문자열 변수를 사용하여 새 애플리케이션의 `docker-compose.yml`에 구성할 서비스를 선택할 수 있습니다. 사용 가능한 서비스는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailhog` 등이 있습니다:

```nothing
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

특별히 서비스를 지정하지 않으면, 기본으로 `mysql`, `redis`, `meilisearch`, `mailhog`, `selenium` 스택이 구성됩니다.

<a name="installation-via-composer"></a>
### Composer를 통한 설치 (Installation Via Composer)

컴퓨터에 PHP와 Composer가 이미 설치되어 있다면, Composer를 직접 사용해 새 Laravel 프로젝트를 만들 수 있습니다. 애플리케이션 생성 후, Artisan CLI의 `serve` 명령어로 로컬 개발 서버를 시작할 수 있습니다:

```
composer create-project laravel/laravel:^8.0 example-app

cd example-app

php artisan serve
```

<a name="the-laravel-installer"></a>
#### Laravel 설치 도구 (The Laravel Installer)

또한 Laravel 설치 도구를 글로벌 Composer 의존성으로 설치할 수 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

`laravel` 실행 파일을 시스템에서 찾을 수 있도록 Composer의 시스템 전역 `vendor/bin` 디렉터리를 `$PATH`에 포함하세요. 운영체제별 위치는 아래와 같습니다.

<div class="content-list" markdown="1">

- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux 배포판: `$HOME/.config/composer/vendor/bin` 또는 `$HOME/.composer/vendor/bin`

</div>

편의를 위해 Laravel 설치 도구는 새 프로젝트에 Git 리포지토리를 생성할 수도 있습니다. Git 리포지토리를 만들고자 할 때는 프로젝트 생성 시 `--git` 플래그를 사용하세요:

```bash
laravel new example-app --git
```

이 명령은 새 Git 리포지토리를 초기화하고 기본 Laravel 골격을 자동으로 커밋합니다. `git` 플래그를 사용하려면 Git이 제대로 설치 및 설정되어 있어야 합니다. 초기 브랜치 이름을 설정하려면 `--branch` 플래그를 사용할 수 있습니다:

```bash
laravel new example-app --git --branch="main"
```

또한 `--github` 플래그를 사용하여 Git 리포지토리를 만들고 GitHub에 대응하는 비공개 리포지토리를 생성할 수 있습니다:

```bash
laravel new example-app --github
```

생성된 리포지토리는 `https://github.com/<your-account>/example-app`에서 확인할 수 있습니다. `github` 플래그는 GitHub CLI([GitHub CLI](https://cli.github.com))를 설치하고 GitHub 인증을 완료한 상태여야 하며, Git도 설치되어 있고 설정되어 있어야 합니다. GitHub CLI에서 지원하는 추가 플래그도 전달할 수 있습니다:

```bash
laravel new example-app --github="--public"
```

특정 GitHub 조직 아래에 리포지토리를 생성하려면 `--organization` 플래그를 사용하세요:

```bash
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 포함되어 있으니 파일을 확인하면서 어떤 옵션을 사용할 수 있는지 익히는 것이 좋습니다.

Laravel은 기본적으로 거의 추가 설정이 필요 없습니다. 바로 개발을 시작해도 됩니다! 다만, `config/app.php` 파일과 문서를 검토하는 것을 추천합니다. 여기에는 `timezone`(표준시), `locale`(로케일) 같은 애플리케이션에 맞게 바꿀 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

Laravel 설정 값들은 로컬 컴퓨터에서 실행할 때와 실제 배포된 서버에선 달라질 수 있기 때문에, 중요한 설정 값들은 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의되는 경우가 많습니다.

`.env` 파일은 애플리케이션의 소스 컨트롤(버전관리)에 포함시키지 말아야 합니다. 각 개발자나 서버별로 환경 설정이 다르기 때문입니다. 그리고, 만약 악의적인 사용자가 소스 컨트롤 저장소에 접근한다면 중요한 자격증명이 노출될 위험도 있습니다.

> [!TIP]
> `.env` 파일과 환경 기반 설정에 대해 자세히 알고 싶다면 전체 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

Laravel 애플리케이션은 항상 웹 서버에서 설정한 "웹 디렉터리"의 루트에서 서비스되어야 합니다. "웹 디렉터리"의 서브디렉터리에서 Laravel 애플리케이션을 서빙하려 시도하면, 애플리케이션 내 중요한 파일에 접근이 노출될 위험이 있습니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 프로젝트를 만들었으니, 이제 무엇을 배워야 할지 궁금할 수 있습니다. 먼저 Laravel이 어떻게 동작하는지 익히는 것을 강력 추천합니다. 다음 문서를 읽어보세요:

<div class="content-list" markdown="1">

- [요청 수명주기(Request Lifecycle)](/docs/{{version}}/lifecycle)
- [설정(Configuration)](/docs/{{version}}/configuration)
- [디렉터리 구조(Directory Structure)](/docs/{{version}}/structure)
- [서비스 컨테이너(Service Container)](/docs/{{version}}/container)
- [파사드(Facades)](/docs/{{version}}/facades)

</div>

Laravel을 어떻게 사용할지에 따라 다음 배워야 할 내용이 달라집니다. 기본적으로 Laravel 사용법은 크게 두 가지 주요 사용 사례로 나뉩니다.

<a name="laravel-the-fullstack-framework"></a>
### Laravel: 풀스택 프레임워크 (Laravel The Full Stack Framework)

Laravel은 풀스택(framework) 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이라 함은, 라우팅을 통해 요청을 처리하고 [Blade 템플릿](/docs/{{version}}/blade)이나 단일 페이지 애플리케이션 하이브리드 기술인 [Inertia.js](https://inertiajs.com)를 통해 프론트엔드를 렌더링한다는 뜻입니다. 이것은 Laravel을 가장 많이 사용하는 방식입니다.

이 방식으로 Laravel을 사용한다면, [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 확인해 보십시오. 또한, [Livewire](https://laravel-livewire.com)와 [Inertia.js](https://inertiajs.com)와 같은 커뮤니티 패키지에도 관심을 가질 수 있습니다. 이 패키지들은 단일 페이지 JavaScript 애플리케이션이 제공하는 UI 이점들을 Laravel 풀스택 프레임워크와 함께 사용할 수 있게 해줍니다.

만약 Laravel을 풀스택 프레임워크로 사용한다면, [Laravel Mix](/docs/{{version}}/mix)를 사용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 꼭 익히시길 권장합니다.

> [!TIP]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### Laravel: API 백엔드 (Laravel The API Backend)

또한 Laravel은 JavaScript 단일 페이지 애플리케이션이나 모바일 애플리케이션의 API 백엔드로서 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이런 경우 Laravel은 [인증](/docs/{{version}}/sanctum), 데이터 저장 및 조회를 제공하며, 큐, 이메일, 알림 등 Laravel의 강력한 서비스도 함께 사용할 수 있습니다.

만약 이렇게 사용하고자 한다면 [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참조하세요.

> [!TIP]
> Laravel 백엔드와 Next.js 프론트엔드를 빠르게 구축하고 싶다면, Laravel Breeze가 [API 스택](/docs/{{version}}/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 제공합니다. 몇 분 내에 시작할 수 있습니다.