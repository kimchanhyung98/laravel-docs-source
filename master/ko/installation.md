# 설치

- [Laravel 소개](#meet-laravel)
    - [왜 Laravel인가?](#why-laravel)
- [Laravel 애플리케이션 만들기](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치 도구 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd](#herd-on-macos)
    - [Windows에서 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 소개

Laravel은 표현적이고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 시작점을 제공하여, 여러분이 세부적인 내용을 걱정하지 않고도 놀라운 무언가를 만드는 데 집중할 수 있도록 도와줍니다.

Laravel은 뛰어난 개발자 경험을 제공하는 것을 목표로 하며, 강력한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등과 같은 강력한 기능을 제공합니다.

PHP 웹 프레임워크가 처음인 분들이나 많은 경험을 가진 분들 모두에게 Laravel은 함께 성장할 수 있는 프레임워크입니다. 여러분이 웹 개발자로 첫걸음을 내딛을 때도, 더 전문성을 키우며 도약할 때도 Laravel이 함께합니다. 여러분이 어떤 것을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
### 왜 Laravel인가?

웹 애플리케이션을 구축할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 저희는 현대적이고 풀스택 웹 애플리케이션을 구축할 때 Laravel이 최고의 선택이라고 믿습니다.

#### 진보적인 프레임워크

저희는 Laravel을 "진보적인" 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장할 수 있다는 의미입니다. 웹 개발을 처음 시작하는 분이라면, 방대한 문서, 가이드, [동영상 튜토리얼](https://laracasts.com)을 통해 부담 없이 기초부터 차근차근 배울 수 있습니다.

이미 시니어 개발자라면, Laravel은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 전문 웹 애플리케이션 개발을 위한 강력한 도구를 제공합니다. Laravel은 엔터프라이즈 규모의 작업도 문제 없이 처리할 수 있도록 세심하게 조율되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 확장성이 뛰어납니다. PHP의 수평 확장에 유리한 특성과 Redis와 같은 고속 분산 캐시 시스템에 대한 내장 지원 덕분에, Laravel로 수평 확장 환경을 손쉽게 구축할 수 있습니다. 실제로, Laravel 애플리케이션은 한 달에 수억 건의 요청도 무리 없이 처리할 수 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 거의 무제한에 가까운 확장성을 누릴 수 있습니다.

#### 커뮤니티 중심 프레임워크

Laravel은 PHP 생태계 최고의 패키지들을 결합하여 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한, 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)하고 있습니다. 어쩌면 여러분도 언젠가 Laravel의 기여자가 될 수 있습니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 만들기

<a name="installing-php"></a>
### PHP 및 Laravel 설치 도구 설치

첫 번째 Laravel 애플리케이션을 만들기 전에, 여러분의 로컬 환경에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel 설치 도구](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프런트엔드 자산을 컴파일할 수 있도록 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/)을 설치해야 합니다.

만약 PHP와 Composer가 로컬에 설치되어 있지 않다면, 다음 커맨드를 통해 macOS, Windows, Linux에 PHP, Composer, Laravel 설치 도구를 설치할 수 있습니다:

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

위의 명령 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. 설치 이후 `php.new` 명령을 다시 실행하여 PHP, Composer, Laravel 설치 도구를 업데이트할 수 있습니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치 도구를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> GUI 기반의 완전한 PHP 설치 및 관리 환경이 필요하다면, [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, Laravel 설치 도구를 설치했다면 이제 새로운 Laravel 애플리케이션을 만들 준비가 된 것입니다. Laravel 설치 도구는 원하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택하도록 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 후, `dev` Composer 스크립트를 사용해 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 시작할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 애플리케이션에 접속할 수 있습니다. 이제 [Laravel 생태계의 다음 단계](#next-steps)로 나아갈 준비가 되었습니다. 물론, [데이터베이스 설정](#databases-and-migrations)도 진행할 수 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 빠르게 시작하고 싶다면, [스타터 키트](/docs/{{version}}/starter-kits)를 활용해 보세요. Laravel 스타터 키트는 백엔드와 프런트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션마다 문서가 잘 작성되어 있으니 파일을 살펴보며 다양한 설정 옵션에 익숙해지길 권장합니다.

Laravel은 처음 설치했을 때 거의 추가 설정이 필요하지 않습니다. 바로 개발을 시작해도 무방합니다! 그러나, 필요에 따라 `config/app.php` 파일과 관련 문서를 검토하는 것이 좋습니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 맞게 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

Laravel의 다수 설정 옵션은 애플리케이션이 로컬 머신에서 실행되는지, 프로덕션 서버에서 실행되는지에 따라 값이 달라질 수 있습니다. 따라서, 많은 중요한 설정 값들이 애플리케이션 루트에 위치한 `.env` 파일에 정의되어 있습니다.

`.env` 파일은 애플리케이션의 소스 제어에 포함하지 않아야 합니다. 개발자나 서버마다 다른 환경 설정이 필요할 수 있기 때문이며, 소스 제어 저장소가 유출될 경우 중요한 자격 증명이 노출되는 보안 위험이 발생할 수 있습니다.

> [!NOTE]
> `.env` 파일 및 환경 기반 설정에 대한 자세한 내용은 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

Laravel 애플리케이션을 만들었다면, 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로, 애플리케이션의 `.env` 설정 파일은 Laravel이 SQLite 데이터베이스와 상호작용하도록 지정되어 있습니다.

애플리케이션 생성 시 Laravel은 `database/database.sqlite` 파일을 생성하고, 필요한 마이그레이션을 실행하여 데이터베이스 테이블을 준비합니다.

MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일의 값을 적절히 수정하면 됩니다. 예를 들어 MySQL을 사용하려면 아래와 같이 `.env` 파일의 `DB_*` 변수를 수정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 이외의 데이터베이스를 사용할 경우, 데이터베이스를 직접 생성한 후 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 활용해 보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정

Laravel은 항상 웹 서버에 설정된 "웹 디렉터리"의 루트에서 제공되어야 합니다. Laravel 애플리케이션을 "웹 디렉터리"의 하위 디렉터리에서 제공하려고 시도해서는 안 됩니다. 그렇게 할 경우 애플리케이션 내에 포함된 민감한 파일이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows를 위한 매우 빠르고 네이티브한 Laravel 및 PHP 개발 환경입니다. Herd는 PHP, Nginx 등 Laravel 개발을 시작하는 데 필요한 모든 것을 내장하고 있습니다.

Herd를 설치하면 Laravel 개발을 바로 시작할 수 있습니다. Herd는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 커맨드라인 도구도 제공합니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스 생성/관리, 로컬 메일 확인, 로그 모니터링 등 다양한 고급 기능을 추가로 제공합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd

macOS에서 개발하려면 [Herd 웹사이트](https://herd.laravel.com)에서 설치 프로그램을 다운로드하세요. 이 설치 도구는 최신 PHP 버전을 자동으로 다운로드하고, 백그라운드에서 [Nginx](https://www.nginx.com/)를 항상 실행하도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여 "주차된(parked)" 디렉터리를 지원합니다. 주차된 디렉터리에 있는 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 주차 디렉터리를 만들고, 이 디렉터리에 있는 모든 Laravel 애플리케이션은 디렉터리 이름을 사용해 `.test` 도메인으로 접근할 수 있습니다.

Herd 설치 후, Laravel CLI(설치에 포함됨)로 가장 빠르게 새 Laravel 애플리케이션을 만들 수 있습니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, Herd의 시스템 트레이 메뉴에서 Herd UI를 열어서 주차 디렉터리 관리와 기타 PHP 설정을 할 수도 있습니다.

Herd에 대해 더 알아보려면 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd

Windows용 Herd 설치 프로그램은 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치를 완료한 후, Herd를 시작하여 온보딩 과정을 마치고 처음으로 Herd UI에 접속할 수 있습니다.

Herd UI는 트레이 아이콘을 왼쪽 클릭하면 열립니다. 오른쪽 클릭 시 자주 사용하는 각종 도구에 접근할 수 있는 퀵 메뉴가 열립니다.

설치 중 Herd는 `%USERPROFILE%\Herd` 경로에 "주차된(parked)" 디렉터리를 생성합니다. 이곳에 있는 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 통해 `.test` 도메인으로 접근할 수 있습니다.

Herd 설치 후, 가장 빠르게 새 Laravel 애플리케이션을 만드는 방법은 Herd에 포함된 Laravel CLI를 이용하는 것입니다. Powershell을 열고 아래 명령을 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Windows용 Herd에 대해 더 알아보려면 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원

Laravel 애플리케이션 개발시 원하는 에디터를 자유롭게 사용할 수 있지만, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 Laravel 및 생태계에 대한 광범위한 지원, [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) 등의 기능을 제공합니다.

또한, 커뮤니티에서 관리하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동완성, 유효성 검증 규칙 자동완성 등 다양한 IDE 확장 기능을 제공합니다.

[Visual Studio Code(VS Code)](https://code.visualstudio.com)로 개발한다면 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)이 제공됩니다. 이 확장 프로그램은 Laravel 전용 도구를 VS Code 환경 내로 바로 제공하여 생산성을 높여줍니다.

<a name="next-steps"></a>
## 다음 단계

이제 Laravel 애플리케이션을 만들었으니, 다음에는 무엇을 배워야 할지 궁금하실 수 있습니다. 먼저 아래 문서를 통해 Laravel의 작동 방식에 익숙해지는 것을 강력히 추천합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [프런트엔드](/docs/{{version}}/frontend)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

Laravel을 어떻게 활용할 것인지에 따라 앞으로의 단계가 달라질 수 있습니다. 아래에서 대표적인 두 가지 활용 사례를 알아보세요.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 Laravel

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. "풀스택" 프레임워크란, Laravel을 사용해 요청을 라우팅하고, [Blade 템플릿](/docs/{{version}}/blade) 또는 [Inertia](https://inertiajs.com) 같은 SPA 하이브리드 기술로 프런트엔드를 렌더링하는 방식을 의미합니다. 이 방식이 Laravel 프레임워크를 사용하는 가장 일반적이며, 생산성을 극대화할 수 있는 추천 방식입니다.

이렇게 Laravel을 사용한다면, [프런트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참고하세요. 더불어 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지에도 관심을 가져보세요. 이 패키지들은 싱글페이지 자바스크립트 애플리케이션이 제공하는 UI 장점도 함께 누릴 수 있게 해줍니다.

풀스택 프레임워크로 Laravel을 사용한다면, [Vite](/docs/{{version}}/vite)로 CSS와 JavaScript를 컴파일하는 방법도 꼭 익히길 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel

Laravel은 자바스크립트 싱글페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, 여러분의 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 활용할 수 있습니다. 이처럼 사용할 때, Laravel의 [인증](/docs/{{version}}/sanctum), 데이터 저장 및 조회, 큐, 이메일, 알림 등의 강력한 서비스를 모두 이용할 수 있습니다.

이렇게 사용한다면 [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 관련 문서를 참고하세요.