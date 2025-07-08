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
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서의 Herd](#herd-on-macos)
    - [Windows에서의 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개

라라벨은 표현력 있고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 여러분의 애플리케이션을 만드는 데 필요한 구조와 시작점을 제공해 주므로, 세부적인 부분은 맡기고 멋진 기능 구현에 집중할 수 있습니다.

라라벨은 풍부한 의존성 주입, 표현력 있는 데이터베이스 추상 계층, 큐 및 예약 작업, 단위/통합 테스트 등 강력한 기능을 제공하면서 개발자에게 뛰어난 개발 경험을 선사하는 것을 목표로 합니다.

PHP 웹 프레임워크가 처음이든, 오랜 경험을 가진 개발자이든, 라라벨은 여러분의 성장에 맞추어 함께 발전할 수 있는 프레임워크입니다. 저희는 여러분이 웹 개발자로 첫발을 내딛는 데도, 더 높은 수준으로 실력을 올리는 데도 도움이 되고자 합니다. 여러분이 무엇을 만들어 나갈지 기대하겠습니다.

<a name="why-laravel"></a>
### 왜 라라벨인가?

웹 애플리케이션을 개발할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그럼에도 불구하고, 저희는 라라벨이 최신의 풀스택 웹 애플리케이션을 만들기 위한 최고의 선택이라고 생각합니다.

#### 점진적(Progressive) 프레임워크

저희는 라라벨을 "점진적(Progressive)" 프레임워크라고 부릅니다. 이 말은 곧, 라라벨이 여러분의 성장에 맞춰 함께 확장된다는 의미입니다. 웹 개발을 처음 접하는 분이라면 라라벨이 제공하는 방대한 문서, 가이드, [동영상 강의](https://laracasts.com)를 통해 쉽게 기본기를 익힐 수 있습니다.

시니어 개발자라면 라라벨이 제공하는 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 강력한 도구들을 활용할 수 있습니다. 라라벨은 전문적인 웹 애플리케이션을 구축하는 데 최적화되어 있으며, 엔터프라이즈급 대규모 트래픽도 무리 없이 처리할 수 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 확장성이 뛰어납니다. PHP의 확장 친화적 특성과, 라라벨이 기본적으로 지원하는 Redis 같은 빠르고 분산된 캐시 시스템 덕분에 수평 확장도 간편하게 할 수 있습니다. 실제로 라라벨 애플리케이션은 한 달에 수억 건의 요청을 무리 없이 처리하도록 손쉽게 확장할 수 있습니다.

극한의 확장이 필요한 경우 [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 거의 무제한에 가까운 규모로 라라벨 애플리케이션을 운영할 수 있습니다.

#### 커뮤니티 중심의 프레임워크

라라벨은 PHP 생태계에서 최고의 패키지들을 결합해 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 뛰어난 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 라라벨 기여자가 될 수도 있습니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성

<a name="installing-php"></a>
### PHP 및 라라벨 인스톨러 설치

처음 라라벨 애플리케이션을 생성하기 전에 여러분의 로컬 환경에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 인스톨러](https://github.com/laravel/installer)가 설치되어 있는지 확인해야 합니다. 또한, 프런트엔드 자산 빌드를 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나도 설치해야 합니다.

만약 로컬에 PHP와 Composer가 없다면, macOS, Windows, Linux에서는 아래 명령어로 PHP, Composer, 라라벨 인스톨러까지 한 번에 설치할 수 있습니다.

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

위 명령 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 PHP, Composer, 라라벨 인스톨러를 설치한 뒤 버전을 최신으로 유지하려면, 해당 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 라라벨 인스톨러를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

> [!NOTE]
> 더욱 다양한 기능과 그래픽 환경을 갖춘 PHP 설치 및 관리를 원하신다면 [Laravel Herd](#installation-using-herd)를 참고해 보세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, 라라벨 인스톨러 설치까지 마쳤다면, 이제 새로운 라라벨 애플리케이션을 만들 준비가 된 것입니다. 라라벨 인스톨러는 기본적으로 원하는 테스트 프레임워크, 데이터베이스, 스타터 키트 등을 선택하도록 안내합니다.

```shell
laravel new example-app
```

애플리케이션 생성 후에는 `dev` Composer 스크립트를 이용해 라라벨의 로컬 개발 서버, 큐 워커, 그리고 Vite 개발 서버를 한 번에 실행할 수 있습니다.

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 애플리케이션에 접속할 수 있습니다. 이제 [라라벨 생태계에서 다음 단계로 나아갈 준비가 되었습니다](#next-steps). 물론, [데이터베이스 설정](#databases-and-migrations)도 이어서 진행할 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 보다 빠르게 시작하고 싶다면 [공식 스타터 키트](/docs/12.x/starter-kits)를 활용해 보세요. 스타터 키트는 백엔드와 프런트엔드 인증 관련 기본 코드를 한 번에 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 자세한 설명이 있으니, 직접 파일을 살펴보면서 사용할 수 있는 옵션들을 익혀두는 것이 좋습니다.

라라벨은 설치 직후 거의 추가 설정 없이 바로 개발을 시작할 수 있도록 설계되어 있습니다. 하지만 필요에 따라 `config/app.php` 파일과 그에 대한 문서를 확인해 보세요. 이 파일에서는 `url`, `locale` 등 애플리케이션에 맞게 변경할 수 있는 여러 옵션이 제공됩니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

라라벨의 설정 옵션 값들은 애플리케이션이 로컬에서 실행되는지, 운영 서버에서 실행되는지 등 환경에 따라 달라질 수 있습니다. 이런 이유로, 중요한 환경별 설정 값들은 애플리케이션 루트 디렉터리의 `.env` 파일에서 관리합니다.

`.env` 파일은 프로젝트의 소스 제어 시스템(예: Git)에 커밋해서는 안 됩니다. 애플리케이션을 사용하는 각 개발자나 서버별로 개별적인 환경 구성이 필요할 수 있기 때문입니다. 또한 만약 소스 제어 저장소가 유출될 경우, 민감한 자격 증명이 노출될 수 있으므로 보안상 위험할 수 있습니다.

> [!NOTE]
> `.env` 파일과 환경별 설정에 대한 더 자세한 내용은 [환경설정 전체 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션

라라벨 애플리케이션을 생성했다면, 이제 데이터를 저장할 데이터베이스가 필요할 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 라라벨이 SQLite 데이터베이스에 연결하도록 설정되어 있습니다.

애플리케이션 생성 시, 라라벨이 자동으로 `database/database.sqlite` 파일을 만들고, 필요한 마이그레이션을 실행해 데이터베이스 테이블도 생성해 둡니다.

MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일에서 해당 데이터베이스에 맞게 값을 변경하면 됩니다. 예를 들어, MySQL을 사용하고 싶다면 다음처럼 `.env` 내부 `DB_*` 변수들을 수정하세요.

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 이외의 데이터베이스를 사용할 경우, 직접 데이터베이스를 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다.

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 로컬로 MySQL, PostgreSQL, Redis를 설치해야 할 경우, [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 활용하는 것도 좋은 방법입니다.

<a name="directory-configuration"></a>
### 디렉터리 설정

라라벨은 반드시 웹 서버의 "웹 루트 디렉터리"에서 직접 서비스되어야 합니다. "웹 루트 디렉터리"의 하위 폴더에서 라라벨 애플리케이션을 서빙하면 안 됩니다. 그렇게 할 경우, 애플리케이션 내부의 민감한 파일이 노출될 위험이 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 초고속, 네이티브 라라벨 및 PHP 개발 환경입니다. Herd에는 라라벨 개발을 시작하는 데 필요한 PHP, Nginx 등 모든 것이 포함되어 있습니다.

Herd 설치만으로도 바로 라라벨 개발을 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등의 명령줄 도구를 모두 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가적으로, 로컬 MySQL, Postgres, Redis 데이터베이스 생성/관리는 물론 로컬 메일 보기, 로그 모니터링 등 강력한 기능을 더해줍니다.

<a name="herd-on-macos"></a>
### macOS에서의 Herd

macOS에서 개발하는 경우, [Herd 웹사이트](https://herd.laravel.com)에서 Herd 인스톨러를 다운로드할 수 있습니다. 인스톨러는 최신 PHP 버전을 자동으로 설치하며, Mac에서 [Nginx](https://www.nginx.com/)가 항상 백그라운드에서 동작하도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 "주차(Parked)" 디렉터리를 지원합니다. 주차된 디렉터리 안의 모든 라라벨 애플리케이션은 자동으로 Herd에 의해 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 주차 디렉터리를 생성하며, 이 디렉터리 내의 모든 라라벨 애플리케이션은 디렉터리명을 그대로 이용해 `.test` 도메인에서 접속할 수 있습니다.

Herd 설치 후, 새로운 라라벨 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 라라벨 CLI를 이용하는 것입니다.

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

주차 디렉터리 관리나 기타 PHP 설정 등은 시스템 트레이의 Herd 메뉴에서 실행되는 UI를 통해 손쉽게 다룰 수 있습니다.

Herd에 대해 더 알고 싶다면 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서의 Herd

Windows용 Herd 인스톨러는 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면 Herd를 시작해 온보딩 과정을 마치고, 처음으로 Herd UI에 접속할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 '왼쪽 클릭'하면 접근할 수 있습니다. '오른쪽 클릭' 시에는 자주 사용하는 모든 도구에 빠르게 접근할 수 있는 퀵 메뉴가 열립니다.

설치 과정에서 Herd는 홈 디렉터리 내 `%USERPROFILE%\Herd` 위치에 "주차(Parked)" 디렉터리를 생성합니다. 이 디렉터리 내의 라라벨 애플리케이션은 자동으로 Herd에 의해 서비스되며, 각 디렉터리명으로 `.test` 도메인에서 곧바로 접속할 수 있습니다.

Herd 설치 후, Herd에 포함된 라라벨 CLI를 이용해 새로운 애플리케이션을 가장 빠르게 만들 수 있습니다. Powershell을 열어 아래와 같이 입력해 보세요.

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows용 Herd에 대해 더 알고 싶다면 [Herd for Windows 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원

라라벨 애플리케이션 개발 시 여러분이 원하는 어떤 코드 에디터도 사용할 수 있습니다. 가볍고 확장 가능한 에디터를 찾는다면, [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 함께 사용해 보세요. Eloquent 모델, 라우트, 미들웨어, 에셋, config, Inertia.js에 대한 구문 강조, 스니펫, 아티즌 명령 연동, 스마트 자동 완성 등 뛰어난 라라벨 지원 기능을 제공합니다.

JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)에 [Laravel Idea 플러그인](https://laravel-idea.com/)을 추가하면 라라벨 및 생태계(예: Laravel Pint, Larastan, Pest)까지 폭넓게 지원됩니다. Blade 템플릿, Eloquent 모델, 라우트, 뷰, 번역, 컴포넌트 등에 대한 스마트 자동 완성, 강력한 코드 생성 및 프로젝트 전반에 걸친 이동 기능도 제공됩니다.

클라우드 기반 개발 환경을 원한다면, [Firebase Studio](https://firebase.studio/)를 이용해 웹 브라우저만으로 즉시 라라벨 개발을 시작할 수 있습니다. 별도의 셋업 없이 어느 기기에서나 라라벨 애플리케이션을 쉽게 만들어 볼 수 있습니다.

<a name="next-steps"></a>
## 다음 단계

라라벨 애플리케이션 생성을 마쳤다면, 이제 무엇을 더 배워야 할지 궁금할 수 있습니다. 무엇보다 라라벨의 작동 방식을 잘 이해하는 것이 중요하므로, 먼저 아래 문서를 읽어 보길 적극 추천합니다.

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프런트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

여러분이 라라벨을 어떻게 활용할 계획이냐에 따라, 앞으로의 학습 경로도 달라질 수 있습니다. 라라벨을 사용하는 주요 방법 두 가지를 아래에서 살펴보겠습니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨

라라벨은 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이란, 라라벨이 애플리케이션의 라우팅을 담당하고, [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술로 프런트엔드를 렌더링하는 것을 뜻합니다. 대부분의 라라벨 사용 사례가 여기에 해당하며, 개발 생산성 측면에서도 가장 효율적인 방식입니다.

이런 방식으로 라라벨을 사용한다면, [프런트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 관련 문서를 참고해 보세요. 또한, 커뮤니티 패키지인 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 도 함께 둘러보면 좋습니다. 이 패키지들은 라라벨을 풀스택 프레임워크로 쓰면서도, 싱글 페이지 JavaScript 애플리케이션의 다양한 UI 장점도 누릴 수 있게 해줍니다.

풀스택 방식으로 라라벨을 사용할 계획이라면, [Vite](/docs/12.x/vite)를 이용해 애플리케이션의 CSS, JavaScript를 컴파일하는 방법도 꼭 익혀 두시길 바랍니다.

> [!NOTE]
> 애플리케이션 개발을 보다 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)도 참고해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨

라라벨은 JavaScript 싱글 페이지 애플리케이션이나 모바일 앱의 API 백엔드 역할도 할 수 있습니다. 예를 들어, 라라벨을 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 사용할 수 있습니다. 이럴 때 라라벨은 [인증](/docs/12.x/sanctum) 및 데이터 저장/조회 기능은 물론, 큐, 이메일, 알림 등 강력한 서비스도 함께 이용할 수 있습니다.

이 방식으로 라라벨을 사용하려면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent) 등의 문서를 참고해 보세요.
