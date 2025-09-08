# 설치 (Installation)

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치 프로그램 설치](#installing-php)
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
    - [라라벨: 풀스택 프레임워크](#laravel-the-fullstack-framework)
    - [라라벨: API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개 (Meet Laravel)

Laravel은 표현적이고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 여러분이 디테일에 신경 쓰는 대신 놀라운 것을 만드는 데 집중할 수 있도록 도와줍니다.

Laravel은 강력한 기능과 더불어 뛰어난 개발자 경험을 제공하기 위해 노력합니다. 포괄적인 의존성 주입, 표현적인 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 갖추고 있습니다.

PHP 웹 프레임워크가 처음인 분이든, 여러 해의 경험이 있으신 분이든 Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로 첫발을 내딛는 여러분을 돕거나, 이미 전문가인 분들의 역량 향상에 도움을 드릴 수 있습니다. 여러분이 무엇을 만들어낼지 기대가 큽니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그럼에도 불구하고, 저희는 Laravel이 현대적인 풀스택 웹 애플리케이션을 만드는 데 최고의 선택이라고 믿습니다.

#### 점진적인 프레임워크

라라벨을 "점진적(progressive)" 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장할 수 있다는 의미입니다. 웹 개발을 처음 접한다면, 라라벨의 방대한 문서, 안내서, 그리고 [비디오 튜토리얼](https://laracasts.com)이 기초를 쉽게 익힐 수 있도록 도울 것입니다.

숙련된 개발자라면, Laravel은 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 도구들을 제공합니다. 라라벨은 전문가 수준의 웹 애플리케이션을 위한 미세 조정과 대규모 업무도 원활하게 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 확장성이 뛰어납니다. PHP 고유의 확장 친화적인 특성과, Redis와 같은 빠르고 분산된 캐시 시스템에 대한 내장 지원 덕분에, 라라벨로 수평 확장은 매우 쉽습니다. 실제로, 라라벨 애플리케이션은 월 수억 건의 요청도 무난히 처리하도록 확장된 사례가 있습니다.

극한의 확장성이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 활용해 사실상 무제한에 가까운 규모로 라라벨 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 프레임워크

라라벨은 PHP 생태계 최고의 패키지들을 결합해, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수많은 재능 있는 개발자들이 이 프레임워크에 [기여](https://github.com/laravel/framework)해왔습니다. 여러분 역시 미래의 라라벨 기여자가 될 수도 있습니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel 설치 프로그램 설치 (Installing PHP and the Laravel Installer)

처음으로 라라벨 애플리케이션을 만들기 전에, [PHP](https://php.net), [Composer](https://getcomposer.org), [라라벨 설치 프로그램](https://github.com/laravel/installer)이 로컬 컴퓨터에 설치되어 있어야 합니다. 또한, 애플리케이션의 프런트엔드 에셋을 컴파일하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬에 PHP와 Composer가 없다면, 아래 명령어를 통해 macOS, Windows, Linux에서 PHP, Composer, Laravel 설치 프로그램을 한 번에 설치할 수 있습니다:

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

위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. PHP, Composer, Laravel 설치 프로그램을 `php.new`를 통해 설치했다면, 추후 업데이트도 위 명령어를 다시 실행하여 진행할 수 있습니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 이용해 라라벨 설치 프로그램만 따로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> GUI 기반의 완전한 PHP 설치·관리 환경을 원한다면 [Laravel Herd](#installation-using-herd)를 참고하십시오.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel 설치 프로그램이 준비되었다면, 이제 신규 라라벨 애플리케이션을 생성할 수 있습니다. 라라벨 설치 프로그램은 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트 선택을 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 후, `dev` Composer 스크립트를 이용해 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면, [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 브라우저로 접속할 수 있습니다. 이제 [라라벨 생태계의 다음 단계](#next-steps)를 시작할 준비가 되었습니다. 혹은 [데이터베이스 설정](#databases-and-migrations)을 먼저 진행할 수도 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 빠르게 시작하고 싶다면 [스타터 키트](/docs/12.x/starter-kits)를 고려해보세요. 스타터 키트는 백엔드와 프런트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 잘 달려 있으니, 파일을 살펴보며 다양한 옵션에 익숙해지는 것을 추천합니다.

라라벨은 기본적으로 거의 추가적인 설정 없이 바로 개발을 시작할 수 있습니다. 하지만, 가이드 차원에서 `config/app.php` 파일의 문서를 한 번 살펴보는 것도 좋습니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 맞게 변경할 수 있는 다양한 설정이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 여러 설정값은 애플리케이션이 로컬 컴퓨터에서 실행되는지, 또는 프로덕션 환경 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 설정값 대부분은 애플리케이션 루트에 위치한 `.env` 파일에 정의되어 있습니다.

`.env` 파일은 애플리케이션의 소스 관리(버전관리) 시스템에 커밋하지 말아야 합니다. 각 개발자와 서버가 서로 다른 환경 구성을 가질 수 있기 때문입니다. 또한 누군가가 소스 저장소에 접근할 경우, 민감한 자격 정보가 노출될 위험이 있으므로 보안상 반드시 주의해야 합니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 설정에 대한 더 자세한 내용은 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

라라벨 애플리케이션을 생성했다면, 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 SQLite 데이터베이스와 연동하도록 설정되어 있습니다.

애플리케이션 생성 과정에서 라라벨은 `database/database.sqlite` 파일을 자동으로 생성하고, 필요한 마이그레이션을 실행해 데이터베이스 테이블을 만들어줍니다.

MySQL이나 PostgreSQL 같은 다른 데이터베이스 드라이버를 사용하려면, `.env` 설정 파일에서 적절한 데이터베이스로 변경해주면 됩니다. 예를 들어 MySQL을 사용하려면 아래와 같이 `.env` 파일의 `DB_*` 변수를 수정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 이외의 데이터베이스를 고른 경우, 해당 데이터베이스를 미리 생성하고, 아래 명령어로 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows 환경에서 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 참고하세요.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

라라벨은 반드시 웹 서버의 "웹 디렉터리" 루트에서 제공되어야 합니다. 라라벨 애플리케이션을 "웹 디렉터리"의 하위 폴더에서 제공하려고 시도해서는 안 됩니다. 그렇게 하면 애플리케이션 내의 민감한 파일들이 외부에 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows를 위한 매우 빠르고 네이티브한 Laravel 및 PHP 개발 환경입니다. Herd에는 PHP와 Nginx를 비롯해 라라벨 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다.

Herd를 설치하면 바로 라라벨 개발을 시작할 준비가 된 것입니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 다양한 커맨드라인 도구도 함께 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스 생성·관리, 로컬 메일 뷰어, 로그 모니터링 같은 추가 강력 기능을 제공하여 Herd를 보강합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS에서 개발할 경우, [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP를 자동으로 다운로드하고, 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 실행되도록 Mac을 설정해줍니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "파크(parking)" 디렉터리를 지원합니다. 파크 디렉터리 내 라라벨 애플리케이션들은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 파크 디렉터리를 만들고, 이 디렉터리 내의 라라벨 앱을 `.test` 도메인에서 디렉터리 이름으로 접속할 수 있습니다.

Herd 설치 후, 라라벨 CLI(설치 시 함께 제공)를 이용해 가장 빠르게 새 라라벨 애플리케이션을 만들 수 있습니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론 Herd 메뉴(시스템 트레이)에서 Herd UI를 열어 파크 디렉터리와 다양한 PHP 설정을 편리하게 관리할 수도 있습니다.

더 자세한 사항은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

Windows용 Herd 설치 프로그램 역시 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 끝나면 Herd를 실행해 첫 설정 과정과 Herd UI 접속을 완료할 수 있습니다.

Herd UI는 시스템 트레이에 있는 Herd 아이콘을 왼쪽 클릭하면 접근할 수 있습니다. 오른쪽 클릭 시 자주 사용하는 도구에 바로 접근할 수 있는 퀵 메뉴가 열립니다.

설치 과정에서 Herd는 홈 디렉터리의 `%USERPROFILE%\Herd`에 "파크" 디렉터리를 생성합니다. 이 디렉터리 내의 라라벨 애플리케이션들은 Herd에 의해 자동으로 서비스되고, 해당 디렉터리 이름을 이용해 `.test` 도메인에서 접속할 수 있습니다.

Herd 설치 후, 함께 제공된 라라벨 CLI로 새 라라벨 애플리케이션을 손쉽게 만들 수 있습니다. Powershell에서 다음과 같이 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

더 자세한 사항은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발 시 원하는 모든 코드 에디터를 자유롭게 사용할 수 있습니다. 가볍고 확장성 높은 에디터를 원한다면 [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)와 공식 [라라벨 VS Code 익스텐션](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 결합해 사용하는 것도 좋은 방법입니다. 이 조합은 구문 강조, 스니펫, 아티즌 명령어 통합, Eloquent 모델·라우트·미들웨어·에셋·설정·Inertia.js를 위한 스마트 자동완성 등 우수한 라라벨 지원 기능을 제공합니다.

라라벨을 위한 강력하고 폭넓은 지원을 원한다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)도 좋은 선택입니다. [Laravel Idea 플러그인](https://laravel-idea.com/)과 함께라면, Laravel Pint, Pest, Larastan 등 생태계 툴도 정확히 지원하며, Blade 템플릿, Eloquent 모델·라우트·뷰·번역·컴포넌트의 자동완성, 코드 생성, 라라벨 프로젝트 전역 코드 탐색 등 막강한 기능을 제공합니다.

클라우드 기반 개발 환경을 찾는다면 [Firebase Studio](https://firebase.studio/)를 통해 브라우저에서 즉시 라라벨 프로젝트를 시작할 수 있습니다. 별도의 설정 없이, 어떤 기기에서도 쉽게 라라벨 애플리케이션을 개발할 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션의 간극을 좁혀 주는 강력한 도구입니다. Boost는 AI 에이전트에게 라라벨 버전 별 컨텍스트, 전용 도구, 가이드라인을 제공하여 보다 정확하고 버전 맞춤화된, 라라벨 관례를 따르는 코드를 생성할 수 있도록 도와줍니다.

Boost를 라라벨 애플리케이션에 설치하면, AI 에이전트는 15개 이상의 라라벨 특화 도구를 활용할 수 있습니다. 예를 들어, 여러분이 사용하는 패키지 목록 확인, 데이터베이스 조회, 라라벨 공식 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등이 있습니다.

또한 Boost는 설치된 패키지 버전에 맞춘 1만 7천 개 이상의 라라벨 생태계 문서를 벡터 형태로 제공합니다. 이를 통해 AI 에이전트는 프로젝트에 맞는 정확한 가이드를 제안할 수 있습니다.

Boost에는 라라벨에서 직접 관리하는 AI 가이드라인도 포함되어 있어, 에이전트가 프레임워크 관례를 따르고, 적절한 테스트를 작성하며, 코드 생성 시 흔히 저지르는 실수를 피하는 데에도 도움을 줍니다.

<a name="installing-laravel-boost"></a>
### 라라벨 Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상에서 실행되는 라라벨 10, 11, 12 버전 모두에 설치할 수 있습니다. 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치가 끝나면, 아래와 같이 대화형 설치 도우미를 실행하세요:

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동 감지하여, 프로젝트에 맞는 기능을 선택할 수 있도록 안내해줍니다. Boost는 기존 프로젝트의 관례를 존중하며, 기본적으로 의견이 강한 스타일 규칙을 강요하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알고 싶다면, [라라벨 Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

라라벨 애플리케이션을 만들었다면, 이제 무엇을 배워야 할지 고민될 수 있습니다. 먼저, 라라벨의 동작 방식을 익히기 위해 아래 문서를 꼭 읽어보길 권장합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프런트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

라라벨을 어떻게 활용할지에 따라 이후 학습 방향도 달라질 수 있습니다. 라라벨을 활용하는 다양한 방법 가운데, 아래에 소개할 두 가지 주요 용례를 참고하세요.

<a name="laravel-the-fullstack-framework"></a>
### 라라벨: 풀스택 프레임워크 (Laravel the Full Stack Framework)

라라벨은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택" 프레임워크란, 라라벨이 애플리케이션의 요청 라우팅과 [Blade 템플릿](/docs/12.x/blade) 또는 [Inertia](https://inertiajs.com)와 같은 싱글페이지 애플리케이션 하이브리드 기술을 이용해 프런트엔드까지 직접 렌더링하는 방식을 뜻합니다. 이 방식은 라라벨의 가장 일반적인 활용법이자, 가장 생산성이 높은 방법이라고 생각합니다.

이 방식으로 사용한다면 [프런트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고하세요. 또한, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 학습하면 좋습니다. 이 패키지들은 라라벨을 풀스택 프레임워크로 사용하면서도 싱글페이지 JavaScript 애플리케이션의 UI 이점을 누릴 수 있게 해줍니다.

풀스택 프레임워크로 라라벨을 쓴다면, [Vite](/docs/12.x/vite)를 이용해 CSS와 JavaScript를 컴파일하는 방법도 꼭 익히시길 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 참고하세요.

<a name="laravel-the-api-backend"></a>
### 라라벨: API 백엔드 (Laravel the API Backend)

라라벨은 JavaScript 싱글페이지 애플리케이션(SPA)이나 모바일 애플리케이션의 API 백엔드로도 활용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 환경에서는 라라벨로 [인증](/docs/12.x/sanctum) 및 데이터 저장·조회 등 핵심 기능을 제공하면서, 라라벨의 강력한 큐, 이메일, 알림 등 다양한 서비스를 함께 활용할 수 있습니다.

API 백엔드로 라라벨을 사용할 계획이라면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 문서를 참고하세요.
