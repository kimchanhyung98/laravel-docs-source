# 설치

- [라라벨 소개](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 라라벨 인스톨러 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉토리 설정](#directory-configuration)
- [Herd를 사용한 설치](#installation-using-herd)
    - [macOS에서 Herd](#herd-on-macos)
    - [Windows에서 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 소개

라라벨은 표현력 있고 우아한 문법을 자랑하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하여, 세부 사항은 우리가 신경 쓸 테니 여러분은 멋진 무언가를 만드는 데 집중할 수 있도록 해줍니다.

라라벨은 강력한 종속성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 훌륭한 개발자 경험을 제공하고자 노력합니다.

PHP 웹 프레임워크를 처음 접하셨더라도, 혹은 다년간의 경험이 있으시더라도, 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 우리는 여러분이 웹 개발자로 첫 걸음을 내딛거나, 전문성을 한 단계 더 끌어올리는 데 힘을 보태겠습니다. 여러분이 어떤 것을 만들어낼지 기대하고 있습니다.

<a name="why-laravel"></a>
### 왜 라라벨인가?

웹 애플리케이션을 구축할 때 사용할 수 있는 다양하고 많은 도구와 프레임워크가 있습니다. 하지만, 저희는 라라벨이 현대적이고 풀스택 웹 애플리케이션을 만드는 데 최고의 선택이라고 생각합니다.

#### 발전하는 프레임워크

우리는 라라벨을 '진화하는(progressive)' 프레임워크라고 부릅니다. 이는 라라벨이 여러분과 함께 성장한다는 뜻입니다. 웹 개발에 첫발을 내딛는 경우에도, 라라벨의 방대한 문서, 가이드, [비디오 튜토리얼](https://laracasts.com)이 초보자를 압도하지 않으면서도 기본을 익히도록 도와줍니다.

경험 많은 개발자라면, 라라벨은 [의존성 주입](/docs/{{version}}/container), [단위 테스트](/docs/{{version}}/testing), [큐](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등 전문적인 웹 애플리케이션 개발에 적합한 강력한 도구를 제공합니다. 라라벨은 엔터프라이즈 환경의 대규모 작업도 문제없이 처리할 수 있도록 최적화되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장성 친화적인 특성과, Redis와 같이 빠르고 분산된 캐시 시스템을 기본적으로 지원하기 때문에, 라라벨로는 수평 확장이 매우 쉽습니다. 실제로, 라라벨 애플리케이션은 한 달에 수억 건의 요청도 무리 없이 처리하도록 확장된 사례가 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 통해 거의 무제한적인 확장도 가능합니다.

#### 커뮤니티 중심 프레임워크

라라벨은 PHP 생태계에서 최고의 패키지를 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한 세계 각지의 수많은 재능 있는 개발자들이 [라라벨 프레임워크에 기여](https://github.com/laravel/framework)해 왔습니다. 어쩌면 여러분도 라라벨 기여자가 될 수 있을지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성

<a name="installing-php"></a>
### PHP 및 라라벨 인스톨러 설치

처음으로 라라벨 애플리케이션을 만들기 전, [PHP](https://php.net), [Composer](https://getcomposer.org), [라라벨 인스톨러](https://github.com/laravel/installer)가 로컬 머신에 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프론트엔드 에셋을 컴파일할 수 있도록 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬 머신에 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어를 사용해 macOS, Windows, 또는 Linux에서 PHP, Composer, 라라벨 인스톨러를 설치할 수 있습니다:

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

위 명령어 중 하나를 실행한 후, 터미널 세션을 재시작하세요. `php.new`로 설치한 후 PHP, Composer, 라라벨 인스톨러를 업데이트하려면 동일한 명령을 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer로 라라벨 인스톨러를 설치할 수도 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 보다 완전한, 그래픽 환경의 PHP 설치와 관리를 원한다면 [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, 라라벨 인스톨러를 설치했다면 이제 새로운 라라벨 애플리케이션을 만들 준비가 되었습니다. 라라벨 인스톨러는 원하는 테스트 프레임워크, 데이터베이스, 스타터 킷 선택을 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 후, 다음 `dev` Composer 스크립트를 사용해 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

서버를 시작하면, [http://localhost:8000](http://localhost:8000)에서 브라우저로 애플리케이션에 접근할 수 있습니다. 이제 [라라벨 생태계의 다음 단계로](#next-steps) 나아갈 준비가 되었습니다. 물론, [데이터베이스 설정](#databases-and-migrations)도 진행할 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발 시 빠른 시작을 원한다면 [스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 이용해 보세요. 라라벨 스타터 킷은 신규 라라벨 애플리케이션에 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션은 문서화되어 있으니 파일을 자유롭게 살펴보고 사용할 수 있는 옵션에 익숙해지세요.

라라벨은 기본적으로 거의 추가 설정이 필요하지 않습니다. 바로 개발을 시작하셔도 좋습니다! 그러나, `config/app.php` 파일과 해당 문서를 검토하는 것이 좋습니다. `url`과 `locale` 등 여러분의 애플리케이션에 맞게 변경할 수 있는 옵션들이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

라라벨의 설정 값 중 많은 부분은 로컬 머신이나 운영 서버 등 어디에서 실행하는지에 따라 달라질 수 있으므로, 주요 설정 값은 애플리케이션 루트에 위치한 `.env` 파일에 정의되어 있습니다.

`.env` 파일은 애플리케이션의 소스 제어에 커밋되지 않아야 합니다. 각 개발자나 서버에 따라 다른 환경 설정이 필요할 수 있기 때문입니다. 또한, 만약 침입자가 소스 저장소에 접근하게 될 경우, 민감한 정보가 노출되는 보안 위험이 있으니 주의하세요.

> [!NOTE]
> `.env` 파일 및 환경 기반 설정에 대해 더 알아보려면 [설정 문서](/docs/{{version}}/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

이제 라라벨 애플리케이션을 만들었으니, 데이터를 데이터베이스에 저장하고 싶을 수 있습니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 라라벨이 SQLite 데이터베이스와 상호작용하도록 지정되어 있습니다.

애플리케이션 생성 시, 라라벨은 자동으로 `database/database.sqlite` 파일을 만들고, 필요한 마이그레이션을 실행해 데이터베이스 테이블을 생성합니다.

만약 MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고자 한다면, `.env` 설정 파일을 적절한 값으로 수정하면 됩니다. 예를 들어, MySQL을 사용하려면 `DB_*` 변수를 다음과 같이 수정하세요:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 다른 데이터베이스를 선택한 경우, 데이터베이스를 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용해 보세요.

<a name="directory-configuration"></a>
### 디렉토리 설정

라라벨은 항상 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 라라벨 애플리케이션을 서비스하는 시도는 하지 마세요. 그렇게 할 경우, 민감한 파일이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 사용한 설치

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows용으로 개발된, 매우 빠르고 네이티브한 라라벨 및 PHP 개발 환경입니다. Herd에는 라라벨 개발에 필요한 PHP와 Nginx를 비롯해 모든 것이 포함되어 있습니다.

Herd를 설치하면, 라라벨 개발을 바로 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 명령줄 도구가 포함되어 있습니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 뷰어와 로그 모니터링 등 다양한 강력한 기능을 추가합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd

macOS에서 개발한다면, [Herd 웹사이트](https://herd.laravel.com)에서 Herd 인스톨러를 다운로드할 수 있습니다. 인스톨러는 최신 PHP 버전을 자동으로 다운로드하고, Mac이 항상 백그라운드에서 [Nginx](https://www.nginx.com/)를 실행하도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용하여 "파크된(parked)" 디렉토리를 지원합니다. 파크된 디렉터리에 위치한 모든 라라벨 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 파크된 디렉터리를 생성하며, 이 디렉터리 내의 어떤 라라벨 애플리케이션이든 디렉터리 이름을 사용해 `.test` 도메인에서 접근할 수 있습니다.

Herd 설치 후, 라라벨 CLI를 사용해 새로운 라라벨 애플리케이션을 만드는 것이 가장 빠른 방법입니다. 라라벨 CLI는 Herd에 포함되어 있습니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 파크된 디렉터리 및 기타 PHP 설정도 관리할 수 있습니다.

자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)에서 확인하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd

[Herd 웹사이트](https://herd.laravel.com/windows)에서 Windows용 설치 프로그램을 다운로드할 수 있습니다. 설치가 끝나면 Herd를 실행해 온보딩을 완료하고, 처음으로 Herd UI에 접근할 수 있습니다.

Herd UI는 시스템 트레이에서 Herd 아이콘을 왼쪽 클릭하면 열립니다. 오른쪽 클릭하면 매일 자주 사용하는 모든 도구에 접근할 수 있는 빠른 메뉴가 열립니다.

설치 과정에서 Herd는 홈 디렉터리 내 `%USERPROFILE%\Herd`에 "파크된" 디렉터리를 생성합니다. 이 디렉터리 내의 어떤 라라벨 애플리케이션이든 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 사용해 `.test` 도메인에서 접근할 수 있습니다.

Herd 설치 후, 새로운 라라벨 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 라라벨 CLI를 사용하는 것입니다. PowerShell을 열고 아래와 같이 명령을 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)에서 확인할 수 있습니다.

<a name="ide-support"></a>
## IDE 지원

라라벨 애플리케이션 개발 시 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 그러나, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 라라벨과 생태계 전반에 대해 풍부한 지원([Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) 포함)을 제공합니다.

또한, 커뮤니티에서 관리하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 완성, 검증 규칙 자동 완성 등 유용한 IDE 기능을 제공해 줍니다.

[Visual Studio Code (VS Code)](https://code.visualstudio.com)를 사용한다면, 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)이 출시되어 있습니다. 이 확장 기능은 라라벨 전용 도구를 VS Code 환경에 직접 통합해 생산성을 높여줍니다.

<a name="next-steps"></a>
## 다음 단계

이제 라라벨 애플리케이션을 만들었으니, 다음에 무엇을 배울지 궁금하실 수 있습니다. 먼저, 아래 문서를 읽으며 라라벨의 작동 방식을 꼭 숙지하시길 권합니다:

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/{{version}}/lifecycle)
- [설정](/docs/{{version}}/configuration)
- [디렉터리 구조](/docs/{{version}}/structure)
- [프론트엔드](/docs/{{version}}/frontend)
- [서비스 컨테이너](/docs/{{version}}/container)
- [파사드](/docs/{{version}}/facades)

</div>

라라벨을 어떻게 활용할지에 따라, 여러분의 다음 단계도 달라집니다. 라라벨을 사용하는 다양한 방법이 있으니, 아래에서 프레임워크의 대표적 두 가지 활용 사례를 살펴보세요.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨

라라벨은 풀스택(Full Stack) 프레임워크로 활용할 수 있습니다. 여기서 '풀스택'이란, 라라벨을 사용해 애플리케이션의 요청을 라우팅하고, [Blade 템플릿](/docs/{{version}}/blade)이나 [Inertia](https://inertiajs.com) 같은 싱글 페이지 애플리케이션 하이브리드 기술로 프론트엔드를 렌더링하는 것을 의미합니다. 이는 라라벨 프레임워크의 가장 일반적인 사용법이며, 저희가 생각하기에 가장 생산적인 방법이기도 합니다.

라라벨을 이런 방식으로 사용한다면, [프론트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views), 또는 [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참고하세요. 또한, [Livewire](https://livewire.laravel.com)와 [Inertia](https://inertiajs.com)와 같은 커뮤니티 패키지도 살펴볼 수 있습니다. 이 패키지들은 라라벨을 풀스택 프레임워크로 사용하면서도, 싱글 페이지 자바스크립트 애플리케이션의 다양한 UI 이점을 누릴 수 있게 해줍니다.

풀스택 프레임워크로 라라벨을 사용한다면, [Vite](/docs/{{version}}/vite)를 이용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 꼭 익히세요.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨

라라벨은 자바스크립트 싱글 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이런 구성에서 라라벨은 애플리케이션의 [인증](/docs/{{version}}/sanctum), 데이터 저장 및 조회를 제공하고, 큐, 이메일, 알림 등 강력한 서비스도 활용할 수 있습니다.

라라벨을 이런 방식으로 사용할 계획이라면, [라우팅](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 문서를 참고하세요.