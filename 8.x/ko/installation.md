# 설치

- [라라벨 만나기](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [첫 번째 라라벨 프로젝트 만들기](#your-first-laravel-project)
    - [macOS에서 시작하기](#getting-started-on-macos)
    - [Windows에서 시작하기](#getting-started-on-windows)
    - [Linux에서 시작하기](#getting-started-on-linux)
    - [Sail 서비스 선택하기](#choosing-your-sail-services)
    - [Composer를 통한 설치](#installation-via-composer)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [디렉토리 설정](#directory-configuration)
- [다음 단계](#next-steps)
    - [라라벨: 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [라라벨: API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 만나기

라라벨은 표현력 있고 우아한 문법을 지닌 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 여러분이 멋진 무언가를 만드는 데 집중할 수 있도록 세부 사항을 대신 챙겨줍니다.

라라벨은 훌륭한 개발자 경험을 제공함과 동시에, 완벽한 의존성 주입, 표현적인 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공합니다.

여러분이 PHP나 웹 프레임워크에 처음 입문하셨든, 다년간의 경험이 있으시든 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 저희는 여러분이 웹 개발자로 첫발을 내딛는 것을 돕거나, 전문가로 나아가는 데 한층 도약할 수 있도록 지원합니다. 여러분이 무엇을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
### 왜 라라벨인가?

웹 애플리케이션을 구축할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 저희는 라라벨이 현대적인 풀스택 웹 애플리케이션을 구축하는 데 최고의 선택이라고 믿습니다.

#### 점진적(Progressive) 프레임워크

저희는 라라벨을 "점진적" 프레임워크라고 부릅니다. 이는 라라벨이 여러분과 함께 성장한다는 의미입니다. 웹 개발에 처음 입문하신 경우, 라라벨의 방대한 문서, 안내서, [영상 튜토리얼](https://laracasts.com)이 여러분이 압도당하지 않고 기초를 익히는 데 도움을 줄 것입니다.

시니어 개발자라면, 라라벨은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 강력한 도구들을 제공합니다. 라라벨은 전문가용 웹 애플리케이션 구축에 최적화되어 있으며, 엔터프라이즈급 작업량도 쉽게 처리할 수 있습니다.

#### 확장 가능한(Scalable) 프레임워크

라라벨은 탁월한 확장성을 자랑합니다. PHP의 확장성에 친화적인 구조와 Redis 같은 빠르고 분산된 캐시 시스템을 내장 지원하여, 라라벨은 수평적 확장이 매우 쉽습니다. 실제로 라라벨 애플리케이션은 한 달에 수억 건의 요청을 처리하도록 쉽게 확장된 사례가 있습니다.

극한의 확장이 필요하다면, [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼을 활용해 AWS의 최신 서버리스 기술로 사실상 무제한에 가까운 확장이 가능합니다.

#### 커뮤니티 프레임워크

라라벨은 PHP 생태계 최고의 패키지들을 통합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 뛰어난 개발자가 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 라라벨 기여자가 될 수 있습니다.

<a name="your-first-laravel-project"></a>
## 첫 번째 라라벨 프로젝트 만들기

라라벨을 최대한 쉽게 시작할 수 있도록 다양한 개발 및 실행 방법을 제공합니다. 나중에 다른 옵션을 탐색할 수 있지만, 라라벨은 [Sail](/docs/{{version}}/sail)이라는 내장 솔루션을 통해 [Docker](https://www.docker.com)를 사용하여 라라벨 프로젝트를 실행할 수 있습니다.

Docker는 애플리케이션과 서비스를 컴퓨터에 설치된 소프트웨어나 설정에 영향을 주지 않는, 작고 가벼운 "컨테이너"에서 실행할 수 있게 해주는 도구입니다. 즉, 웹 서버나 데이터베이스와 같은 복잡한 개발 도구 설치 및 설정에 신경 쓰지 않아도 됩니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

라라벨 Sail은 라라벨의 기본 Docker 설정과 상호작용할 수 있는 경량의 명령줄 인터페이스입니다. Sail을 이용하면 별도의 Docker 경험 없이 PHP, MySQL, Redis를 사용하는 라라벨 애플리케이션을 쉽게 시작할 수 있습니다.

> {tip} 이미 Docker 전문가이신가요? 걱정하지 마세요! Sail의 모든 것은 라라벨에 포함된 `docker-compose.yml` 파일로 커스터마이징할 수 있습니다.

<a name="getting-started-on-macos"></a>
### macOS에서 시작하기

Mac에서 개발 중이고, [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 간단한 터미널 명령으로 새 라라벨 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 라라벨 애플리케이션을 생성하려면 터미널에 아래 명령을 입력하세요:

```nothing
curl -s "https://laravel.build/example-app" | bash
```

물론, 이 URL의 "example-app" 부분을 원하는 이름으로 변경할 수 있습니다. 라라벨 애플리케이션 디렉터리는 명령어를 실행한 경로에 생성됩니다.

프로젝트가 생성된 후, 애플리케이션 디렉터리로 이동해 라라벨 Sail을 시작할 수 있습니다. Sail은 라라벨의 기본 Docker 설정과 상호작용할 수 있는 간단한 명령줄 인터페이스를 제공합니다:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 Sail의 `up` 명령을 실행하면 Sail의 애플리케이션 컨테이너가 컴퓨터에 빌드됩니다. 이 과정은 몇 분 정도 걸릴 수 있습니다. **걱정하지 마세요. 이후엔 훨씬 더 빨리 실행됩니다.**

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 http://localhost 로 접속해 사용할 수 있습니다.

> {tip} 라라벨 Sail에 대해 더 알고 싶다면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="getting-started-on-windows"></a>
### Windows에서 시작하기

Windows에서 새 라라벨 애플리케이션을 만들기 전에, [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치하세요. 다음으로, Windows Subsystem for Linux 2(WSL2)가 설치 및 활성화되어 있는지 확인하세요. WSL은 Windows 10에서 리눅스 바이너리 실행파일을 네이티브로 실행할 수 있게 해줍니다. WSL2 설치 및 활성화 방법은 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> {tip} WSL2를 설치 및 활성화한 후, Docker Desktop이 [WSL2 백엔드를 사용하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인하세요.

이제 첫 번째 라라벨 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행해 WSL2 리눅스 OS용 새 터미널 세션을 시작하세요. 이제 아래와 같이 간단한 명령으로 새 라라벨 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 애플리케이션을 생성하려면 다음 명령을 실행하세요:

```nothing
curl -s https://laravel.build/example-app | bash
```

물론, 이 URL의 "example-app" 부분을 원하는 이름으로 변경할 수 있습니다. 라라벨 애플리케이션 디렉터리는 명령어를 실행한 경로에 생성됩니다.

프로젝트가 생성된 후, 애플리케이션 디렉터리로 이동하여 라라벨 Sail을 시작하세요. Sail은 라라벨의 기본 Docker 설정과 상호작용할 수 있는 간단한 명령줄 인터페이스를 제공합니다:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 Sail의 `up` 명령을 실행하면 Sail의 애플리케이션 컨테이너가 컴퓨터에 빌드됩니다. 이 과정은 몇 분 정도 걸릴 수 있습니다. **걱정하지 마세요. 이후엔 훨씬 더 빨리 실행됩니다.**

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 http://localhost 로 접속해 사용할 수 있습니다.

> {tip} 라라벨 Sail에 대해 더 알고 싶다면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

#### WSL2 환경에서 개발하기

WSL2 설치경로 내에 생성된 라라벨 애플리케이션 파일을 수정할 수 있어야 합니다. 이를 위해 마이크로소프트의 [Visual Studio Code](https://code.visualstudio.com) 에디터와 [원격 개발 플러그인](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 설치를 권장합니다.

도구 설치 후, Windows Terminal에서 애플리케이션 루트 디렉터리에서 `code .` 명령을 실행해 라라벨 프로젝트를 열 수 있습니다.

<a name="getting-started-on-linux"></a>
### Linux에서 시작하기

Linux에서 개발 중이며 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면, 간단한 터미널 명령으로 새 라라벨 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 라라벨 애플리케이션을 생성하려면 다음 명령을 입력하세요:

```nothing
curl -s https://laravel.build/example-app | bash
```

마찬가지로, URL의 "example-app" 부분을 자유롭게 변경할 수 있습니다. 라라벨 애플리케이션 디렉터리는 명령어를 실행한 경로에 생성됩니다.

프로젝트가 생성된 후, 애플리케이션 디렉터리로 이동해 라라벨 Sail을 시작하세요. Sail은 라라벨의 기본 Docker 설정과 상호작용할 수 있는 간단한 명령줄 인터페이스를 제공합니다:

```nothing
cd example-app

./vendor/bin/sail up
```

처음 Sail의 `up` 명령을 실행하면 Sail의 애플리케이션 컨테이너가 컴퓨터에 빌드됩니다. 이 과정은 몇 분 정도 걸릴 수 있습니다. **걱정하지 마세요. 이후엔 훨씬 더 빨리 실행됩니다.**

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 http://localhost 로 접속해 사용할 수 있습니다.

> {tip} 라라벨 Sail에 대해 더 알고 싶다면 [전체 문서](/docs/{{version}}/sail)를 참고하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택하기

Sail을 통해 새 라라벨 애플리케이션을 생성할 때, `with` 쿼리 스트링 변수를 사용해 새 애플리케이션의 `docker-compose.yml` 파일에 구성될 서비스를 지정할 수 있습니다. 사용 가능한 서비스로는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, `mailhog` 등이 있습니다:

```nothing
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

설정하고 싶은 서비스를 명시하지 않으면, 기본적으로 `mysql`, `redis`, `meilisearch`, `mailhog`, `selenium` 스택이 구성됩니다.

<a name="installation-via-composer"></a>
### Composer를 통한 설치

이미 컴퓨터에 PHP와 Composer가 설치되어 있다면, Composer를 직접 사용해 새 라라벨 프로젝트를 만들 수 있습니다. 애플리케이션이 생성된 후, Artisan CLI의 `serve` 명령어로 라라벨의 로컬 개발 서버를 시작할 수 있습니다:

    composer create-project laravel/laravel:^8.0 example-app

    cd example-app

    php artisan serve

<a name="the-laravel-installer"></a>
#### 라라벨 인스톨러 사용

또는, Composer 전역 의존성으로 라라벨 인스톨러를 설치할 수도 있습니다:

```nothing
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

`laravel` 실행 파일이 시스템의 `$PATH`에 포함되어 있어야 합니다. OS에 따라 이 디렉토리의 위치가 다르며, 일반적으로 아래 위치 중 하나입니다:

<div class="content-list" markdown="1">

- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux 배포판: `$HOME/.config/composer/vendor/bin` 또는 `$HOME/.composer/vendor/bin`

</div>

편의를 위해, 라라벨 인스톨러는 새 프로젝트에 Git 저장소를 생성할 수도 있습니다. 새 프로젝트 생성 시 `--git` 플래그를 사용하면 저장소가 자동 생성됩니다:

```bash
laravel new example-app --git
```

이 명령은 새 Git 저장소를 초기화하고 기본 라라벨 골격을 자동으로 커밋합니다. `git` 플래그는 Git이 올바르게 설치 및 설정되어 있음을 가정합니다. 초기 브랜치 이름을 지정하려면 `--branch` 플래그를 사용할 수 있습니다:

```bash
laravel new example-app --git --branch="main"
```

`--git` 플래그 대신 `--github` 플래그를 사용하면 Git 저장소 뿐만 아니라 GitHub에 해당 저장소(비공개)도 생성할 수 있습니다:

```bash
laravel new example-app --github
```

생성된 저장소는 `https://github.com/<your-account>/example-app`에서 확인할 수 있습니다. `github` 플래그는 [GitHub CLI](https://cli.github.com)가 설치되어 있고, GitHub 인증이 완료되어야 하며, 또한 `git`도 설치 및 설정되어 있어야 합니다. 필요하다면 GitHub CLI가 지원하는 추가 플래그도 전달할 수 있습니다:

```bash
laravel new example-app --github="--public"
```

특정 GitHub 조직에 저장소를 생성하려면 `--organization` 플래그를 사용할 수 있습니다:

```bash
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
## 초기 설정

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 주석이 달려 있으니, 파일을 탐색하며 다양한 설정 옵션에 익숙해지세요.

라라벨은 기본적으로 추가 설정 없이 바로 개발을 시작할 수 있습니다. 바로 개발을 진행해도 좋지만, `config/app.php` 파일과 주석을 한번 살펴보는 것도 좋습니다. 이 파일에는 `timezone`과 `locale` 등 애플리케이션에 맞게 변경할 수 있는 몇 가지 옵션이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

라라벨의 많은 설정 옵션 값들은 애플리케이션이 로컬 컴퓨터에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있으므로, 많은 중요한 설정값들은 애플리케이션의 루트에 있는 `.env` 파일에 정의되어 있습니다.

각 개발자나 서버의 환경 설정이 다를 수 있으므로, `.env` 파일은 소스 버전 관리에 커밋하지 않는 것이 좋습니다. 만약 침입자가 소스 저장소에 접근하게 되면 민감한 인증정보가 노출될 수 있으므로 보안상 위험합니다.

> {tip} `.env` 파일과 환경 기반 설정에 관한 자세한 내용은 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="directory-configuration"></a>
### 디렉토리 설정

라라벨은 항상 웹서버의 "웹 디렉토리" 루트에서 서비스되어야 합니다. "웹 디렉토리"의 하위 디렉터리에서 라라벨 애플리케이션을 서비스하려 하지 마세요. 그렇게 하면 애플리케이션 내부의 민감한 파일이 노출될 수 있습니다.

<a name="next-steps"></a>
## 다음 단계

라라벨 프로젝트를 생성했다면, 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저, 라라벨이 어떻게 동작하는지 아래 문서를 숙지하시길 강력히 권장합니다.

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

라라벨을 어떻게 활용할지에 따라 이후 학습 방향도 달라질 수 있습니다. 라라벨을 사용하는 다양한 방법 중, 아래에서 두 가지 주요 활용 방식을 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 라라벨: 풀스택 프레임워크

라라벨은 풀스택 프레임워크로 활용할 수 있습니다. "풀스택" 프레임워크란 라라벨로 애플리케이션의 요청 라우팅과, [Blade 템플릿](/docs/{{version}}/blade)이나 [Inertia.js](https://inertiajs.com)와 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드 렌더링까지 처리한다는 의미입니다. 이것이 라라벨을 사용하는 가장 일반적인 방식입니다.

이 방식으로 라라벨을 사용하려면, [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 확인해보세요. 더불어, [Livewire](https://laravel-livewire.com), [Inertia.js](https://inertiajs.com)와 같은 커뮤니티 패키지도 참고할 만합니다. 이 패키지들을 사용하면, 자바스크립트 단일 페이지 애플리케이션들이 제공하는 UI 이점을 누리면서도 라라벨을 풀스택 프레임워크로 활용할 수 있습니다.

풀스택 프레임워크로 라라벨을 사용할 경우, [Laravel Mix](/docs/{{version}}/mix)를 활용해 CSS와 자바스크립트를 컴파일하는 방법도 꼭 익혀두세요.

> {tip} 애플리케이션 구축을 빠르게 시작하고 싶다면, 공식 [스타터 키트](/docs/{{version}}/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### 라라벨: API 백엔드

라라벨은 또한 자바스크립트 단일 페이지 애플리케이션(SPA)이나 모바일 애플리케이션의 API 백엔드로도 활용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 경우 라라벨은 애플리케이션의 [인증](/docs/{{version}}/sanctum), 데이터 저장/검색 등 핵심 기능은 물론, 큐, 이메일, 알림 등 다양한 강력한 서비스를 제공합니다.

이 방식을 고려한다면, [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 확인해보세요.

> {tip} 라라벨 백엔드와 Next.js 프론트엔드의 빠른 스캐폴딩이 필요하다면, Laravel Breeze의 [API 스택](/docs/{{version}}/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 참고해 몇 분 만에 시작할 수 있습니다.
