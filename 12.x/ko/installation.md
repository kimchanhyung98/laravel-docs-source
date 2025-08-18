# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 만들기](#creating-a-laravel-project)
    - [PHP 및 라라벨 인스톨러 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [라라벨 Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

라라벨은 표현력 있고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하여, 여러분이 세부 사항에 신경 쓰지 않고도 멋진 것을 만드는 데 집중할 수 있도록 돕습니다.

라라벨은 개발자 경험을 극대화하는 것을 목표로 하며, 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위/통합 테스트 등 강력한 기능을 제공합니다.

PHP 웹 프레임워크가 처음인 분이든, 오랜 경험을 가진 분이든 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자의 첫걸음을 지원하거나, 전문성을 한 단계 끌어올리고자 할 때도 라라벨이 든든한 도약판이 되어줄 것입니다. 여러분이 무엇을 만들어낼지 기대하겠습니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 만들 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 하지만 저희는 라라벨이 현대적인 풀스택 웹 애플리케이션을 만들기에 최고의 선택이라고 믿습니다.

#### 진보형 프레임워크

라라벨을 "진보형(Progressive) 프레임워크"라고 부르곤 합니다. 즉, 라라벨은 사용자의 성장에 맞춰 함께 발전합니다. 웹 개발을 처음 시작하신다면, 방대한 문서, 가이드, 그리고 [영상 튜토리얼](https://laracasts.com)을 참고하여 부담 없이 학습할 수 있습니다.

경험 많은 시니어 개발자라면, 라라벨에서 제공하는 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 견고한 도구들을 활용하실 수 있습니다. 라라벨은 전문적인 웹 애플리케이션 구축에 최적화되어 있으며, 엔터프라이즈 급의 업무량도 거뜬하게 처리할 준비가 되어 있습니다.

#### 확장성 높은 프레임워크

라라벨은 매우 뛰어난 확장성을 자랑합니다. PHP가 본래 갖는 확장 친화적인 특성과, Redis 같은 빠르고 분산된 캐시 시스템을 위한 라라벨의 내장 지원 덕분에, 수평 확장 또한 매우 쉽습니다. 실제로 라라벨 애플리케이션은 한 달에 수억 건의 요청도 무리 없이 처리한 사례가 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 사실상 무제한에 가까운 확장이 가능합니다.

#### 커뮤니티 중심 프레임워크

라라벨은 PHP 생태계 최고의 패키지를 결합하여, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 뛰어난 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해주고 있습니다. 어쩌면 여러분도 라라벨 컨트리뷰터가 될 수도 있습니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 만들기 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 라라벨 인스톨러 설치 (Installing PHP and the Laravel Installer)

첫 번째 라라벨 애플리케이션을 만들기 전에, 로컬 컴퓨터에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 인스톨러](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프런트엔드 자산(assets) 빌드를 위해 [Node 및 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나가 설치되어 있어야 합니다.

만약 로컬 컴퓨터에 PHP와 Composer가 아직 설치되어 있지 않다면, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer, 그리고 라라벨 인스톨러를 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 PHP, Composer, 라라벨 인스톨러를 설치한 경우, 추후 업데이트도 동일 명령을 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer로 라라벨 인스톨러를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 그래픽 기반의 완전한 PHP 설치 및 관리를 원하신다면, [라라벨 Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, 라라벨 인스톨러까지 모두 설치했다면 이제 새로운 라라벨 애플리케이션을 만들 준비가 되었습니다. 라라벨 인스톨러를 이용하면 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택할 수 있습니다:

```shell
laravel new example-app
```

애플리케이션이 생성되면, `dev` Composer 스크립트를 이용해 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 동시에 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면, 웹브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션 접속이 가능합니다. 다음 단계로 [라라벨 생태계 활용시작](#next-steps)을 안내합니다. 물론 필요하다면 [데이터베이스 설정](#databases-and-migrations)도 진행할 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 좀 더 빠르게 시작하고 싶다면, [공식 스타터 키트](/docs/12.x/starter-kits)를 사용해보세요. 라라벨 스타터 키트는 새로운 라라벨 애플리케이션의 백엔드 및 프런트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에 대한 문서가 포함되어 있으니, 설정 파일을 살펴보면서 다양한 옵션을 익혀보시기 바랍니다.

라라벨은 기본적으로 거의 추가 설정이 필요 없습니다. 바로 개발을 시작하셔도 됩니다! 단, `config/app.php` 파일과 그 문서를 한 번 읽어보는 것을 권장합니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 따라 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 설정 값 중에는 애플리케이션이 로컬에서 실행 중인지, 프로덕션 웹 서버에서 실행 중인지에 따라 값이 달라지는 항목이 많습니다. 이런 중요한 값들은 대부분 애플리케이션 루트에 있는 `.env` 파일을 통해 정의합니다.

`.env` 파일은 애플리케이션의 소스 컨트롤에 커밋해서는 안 됩니다. 개발자 또는 서버별로 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 또한, 만약 소스 컨트롤 저장소가 외부에 노출될 경우, 중요한 인증 정보 유출 위험도 있습니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 더 자세한 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

라라벨 애플리케이션을 만들었다면, 아마 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 라라벨이 SQLite 데이터베이스와 상호작용하도록 지정되어 있습니다.

애플리케이션 생성 시, 라라벨이 자동으로 `database/database.sqlite` 파일을 만들고, 데이터베이스 테이블 생성을 위한 필요한 마이그레이션도 실행했습니다.

MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, 해당 데이터베이스에 맞게 `.env` 설정 파일을 수정하면 됩니다. 예를 들어 MySQL을 사용하려면 다음과 같이 `DB_*` 변수들을 바꿔주세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 사용할 경우, 데이터베이스를 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다.

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 개발하면서 MySQL, PostgreSQL, Redis 등을 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)를 활용해보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

라라벨 애플리케이션은 반드시 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨을 서비스하려고 시도하면, 애플리케이션의 민감한 파일이 외부에 노출될 수 있으니 절대 그렇게 하면 안 됩니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows를 위한 매우 빠른 네이티브 라라벨 및 PHP 개발 환경입니다. Herd에는 라라벨 개발에 필요한 모든 요소(PHP, Nginx 포함)가 들어 있습니다.

Herd를 설치하면, 바로 라라벨 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등의 명령어 도구도 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 보기, 로그 모니터링 등 강력한 기능을 추가로 제공합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS에서 개발하는 경우, [Herd 공식 사이트](https://herd.laravel.com)에서 인스톨러를 다운로드할 수 있습니다. 인스톨러는 최신 PHP 버전을 자동으로 다운로드하며, Mac에서 [Nginx](https://www.nginx.com/)를 항상 백그라운드로 실행하도록 설정해줍니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "파킹된(parked)" 디렉터리를 지원합니다. 파킹된 디렉터리에 위치한 모든 라라벨 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 파킹된 디렉터리를 만들며, 이 디렉터리 내 애플리케이션은 각각의 디렉터리명으로 `.test` 도메인을 통해 접속할 수 있습니다.

Herd 설치 후, 가장 빠르게 새로운 라라벨 애플리케이션을 만드는 방법은 Herd에 포함된 라라벨 CLI를 사용하는 것입니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, Herd의 시스템 트레이 메뉴에서 UI를 통해 파킹 디렉터리 관리와 PHP 관련 설정도 언제든지 할 수 있습니다.

Herd에 대해 더 알고 싶다면 [Herd 공식 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

Windows용 Herd 인스톨러는 [Herd 공식 사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면 Herd를 시작해 온보딩 과정을 마치고, 처음으로 Herd UI를 사용할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하면 열립니다. 오른쪽 클릭 시 자주 쓰는 각종 도구를 빠르게 사용할 수 있는 퀵 메뉴가 나옵니다.

설치 시, Herd는 사용자 홈 디렉터리 `%USERPROFILE%\Herd`에 "파킹된" 디렉터리를 생성합니다. 이 디렉터리에 있는 모든 라라벨 애플리케이션은 Herd에 의해 자동으로 서비스되며, 각각의 디렉터리 이름을 가진 `.test` 도메인에서 접속할 수 있습니다.

Herd 설치 후, Herd에 포함된 라라벨 CLI를 이용해 새로운 라라벨 애플리케이션을 가장 빠르게 만들 수 있습니다. PowerShell을 열고 다음 명령어들을 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows용 Herd에 대해 더 알고 싶다면 [공식 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발 시 원하는 코드 에디터를 자유롭게 선택할 수 있습니다. 가볍고 확장 가능한 에디터를 찾는다면 [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [라라벨 VS Code 확장](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 설치해 사용할 수 있습니다. 이 확장으로 구문 강조, 코드 스니펫, Artisan 명령어 통합, Eloquent 모델, 라우트, 미들웨어, 자산, 설정, Inertia.js 등에 대한 스마트 자동완성 기능을 사용할 수 있습니다.

JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)과 [Laravel Idea 플러그인](https://laravel-idea.com/) 조합은 라라벨 및 생태계(Pint, Larastan, Pest 포함)에 대한 종합적인 지원을 제공합니다. 프레임워크 지원 범위에는 Blade 템플릿, Eloquent 모델/라우트/뷰/번역/컴포넌트에 대한 스마트 자동완성, 코드 생성, 라라벨 프로젝트 전반에 걸친 강력한 네비게이션이 포함됩니다.

클라우드 기반 개발 환경을 원한다면 [Firebase Studio](https://firebase.studio/)를 통해 브라우저에서 즉시 라라벨을 개발할 수 있습니다. 별도의 설치 절차 없이, 어떤 기기에서든 손쉽게 라라벨 애플리케이션을 만들 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션 사이의 격차를 해소하는 강력한 도구입니다. Boost는 AI 에이전트에게 라라벨 전용 컨텍스트, 도구, 가이드를 제공하여 라라벨 컨벤션을 따르는 더 정확하고 버전별 맞춤 코드를 생성할 수 있게 해줍니다.

Boost를 애플리케이션에 설치하면, AI 에이전트가 15개 이상의 라라벨 전용 도구를 사용할 수 있습니다. 예를 들어 사용 중인 패키지 확인, 데이터베이스 쿼리, 라라벨 공식 문서 검색, 브라우저 로그 읽기, 테스트 코드 생성, Tinker를 통한 코드 실행 등이 가능합니다.

또한 Boost는 현재 프로젝트에 설치된 패키지 버전에 맞춘 1만 7천 개 이상의 벡터화된 라라벨 생태계 문서에 AI가 접근할 수 있도록 하여, 프로젝트에 꼭 맞는 맞춤형 도움을 제공합니다.

Boost에는 라라벨 팀이 유지 관리하는 AI 가이드라인도 포함되어 있습니다. 이 가이드라인을 통해 AI가 라라벨 관례를 잘 따르고, 적절한 테스트 코드를 작성하며, 코드를 자동 생성할 때 흔히 저지르는 실수를 피하도록 유도합니다.

<a name="installing-laravel-boost"></a>
### 라라벨 Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상의 환경에서 실행되는 라라벨 10, 11, 12 버전에서 설치할 수 있습니다. 시작하려면 개발용 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치가 끝나면, 인터랙티브 인스톨러를 실행하세요:

```shell
php artisan boost:install
```

인스톨러가 IDE와 AI 에이전트를 자동으로 감지하고 프로젝트에 맞는 기능을 선택할 수 있게 도와줍니다. Boost는 기존 프로젝트의 컨벤션을 존중하며, 기본적으로 강제적인 스타일 규칙을 적용하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알아보려면 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 확인하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 라라벨 애플리케이션을 만들었으니 다음에 무엇을 해야 할지 고민될 수 있습니다. 먼저, 아래 문서를 읽어 라라벨의 동작 방식을 충분히 이해해 두실 것을 강력히 권장합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프런트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

라라벨을 어떻게 활용할 것인지에 따라 이후 학습 경로가 달라집니다. 라라벨은 다양한 쓰임새가 있으며, 여기서는 프레임워크의 대표적인 두 가지 사용법을 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

라라벨은 풀스택 프레임워크로 동작할 수 있습니다. "풀스택" 프레임워크란, 라라벨로 모든 요청을 라우팅하고 [Blade 템플릿](/docs/12.x/blade) 또는 [Inertia](https://inertiajs.com) 같은 SPA(싱글 페이지 애플리케이션) 하이브리드 기술로 프런트엔드를 렌더링하는 구조를 의미합니다. 라라벨을 사용하는 가장 일반적이면서 생산적인 방법입니다.

이 방법으로 라라벨을 사용할 계획이라면, [프런트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서부터 살펴보길 추천합니다. [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지로, 자바스크립트 싱글 페이지 UI의 장점을 누리며 라라벨을 전체 스택 프레임워크로 활용할 수 있습니다.

풀스택 프레임워크 환경이라면, [Vite](/docs/12.x/vite)를 통한 CSS/JS 빌드 방법도 꼭 숙지해 두시기 바랍니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

또는 라라벨을 자바스크립트 싱글 페이지 애플리케이션이나 모바일 애플리케이션용 API 백엔드로 활용할 수도 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 방식에서는 라라벨이 [인증](/docs/12.x/sanctum), 데이터 저장 및 조회 기능을 제공하며, 큐, 이메일, 알림 등 라라벨의 강력한 서비스도 함께 활용할 수 있습니다.

이처럼 라라벨을 API 백엔드로 사용하려면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 관련 문서를 참고하면 좋습니다.
