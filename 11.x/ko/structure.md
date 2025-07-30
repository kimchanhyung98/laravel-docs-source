# 디렉터리 구조 (Directory Structure)

- [소개](#introduction)
- [루트 디렉터리](#the-root-directory)
    - [`app` 디렉터리](#the-root-app-directory)
    - [`bootstrap` 디렉터리](#the-bootstrap-directory)
    - [`config` 디렉터리](#the-config-directory)
    - [`database` 디렉터리](#the-database-directory)
    - [`public` 디렉터리](#the-public-directory)
    - [`resources` 디렉터리](#the-resources-directory)
    - [`routes` 디렉터리](#the-routes-directory)
    - [`storage` 디렉터리](#the-storage-directory)
    - [`tests` 디렉터리](#the-tests-directory)
    - [`vendor` 디렉터리](#the-vendor-directory)
- [앱 디렉터리](#the-app-directory)
    - [`Broadcasting` 디렉터리](#the-broadcasting-directory)
    - [`Console` 디렉터리](#the-console-directory)
    - [`Events` 디렉터리](#the-events-directory)
    - [`Exceptions` 디렉터리](#the-exceptions-directory)
    - [`Http` 디렉터리](#the-http-directory)
    - [`Jobs` 디렉터리](#the-jobs-directory)
    - [`Listeners` 디렉터리](#the-listeners-directory)
    - [`Mail` 디렉터리](#the-mail-directory)
    - [`Models` 디렉터리](#the-models-directory)
    - [`Notifications` 디렉터리](#the-notifications-directory)
    - [`Policies` 디렉터리](#the-policies-directory)
    - [`Providers` 디렉터리](#the-providers-directory)
    - [`Rules` 디렉터리](#the-rules-directory)

<a name="introduction"></a>
## 소개 (Introduction)

기본 Laravel 애플리케이션 구조는 대규모 애플리케이션과 소규모 애플리케이션 모두에 훌륭한 출발점을 제공하도록 설계되었습니다. 그러나 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 Composer가 클래스를 자동 로드할 수 있는 한, 특정 클래스가 어디에 위치해야 하는지 거의 제한을 두지 않습니다.

> [!NOTE]  
> Laravel이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)에서 프레임워크를 직접 체험하고 첫 번째 Laravel 애플리케이션을 만드는 과정을 살펴보세요.

<a name="the-root-directory"></a>
## 루트 디렉터리 (The Root Directory)

<a name="the-root-app-directory"></a>
### `app` 디렉터리 (The App Directory)

`app` 디렉터리는 애플리케이션의 핵심 코드를 포함합니다. 곧 자세히 살펴보겠지만, 애플리케이션 내 거의 모든 클래스가 이 디렉터리에 위치합니다.

<a name="the-bootstrap-directory"></a>
### `bootstrap` 디렉터리 (The Bootstrap Directory)

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 있습니다. 이 디렉터리에는 또한 성능 최적화를 위해 route와 services 캐시 파일 같은 프레임워크 생성 파일을 저장하는 `cache` 디렉터리가 포함되어 있습니다.

<a name="the-config-directory"></a>
### `config` 디렉터리 (The Config Directory)

`config` 디렉터리는 이름 그대로 애플리케이션의 모든 설정 파일을 포함합니다. 이 파일들을 모두 읽어보고 제공되는 옵션을 숙지하는 것이 좋습니다.

<a name="the-database-directory"></a>
### `database` 디렉터리 (The Database Directory)

`database` 디렉터리는 데이터베이스 마이그레이션, 모델 팩토리, 시드를 포함합니다. 원한다면 이 디렉터리에 SQLite 데이터베이스 파일을 저장할 수도 있습니다.

<a name="the-public-directory"></a>
### `public` 디렉터리 (The Public Directory)

`public` 디렉터리에는 애플리케이션으로 들어오는 모든 요청의 진입점인 `index.php` 파일이 있습니다. 또한 이 디렉터리에는 이미지, 자바스크립트, CSS 같은 정적 자산도 위치합니다.

<a name="the-resources-directory"></a>
### `resources` 디렉터리 (The Resources Directory)

`resources` 디렉터리는 [뷰](/docs/11.x/views)와 CSS 또는 자바스크립트와 같이 원시 상태로 컴파일되지 않은 자산들을 포함합니다.

<a name="the-routes-directory"></a>
### `routes` 디렉터리 (The Routes Directory)

`routes` 디렉터리는 애플리케이션의 모든 라우트 정의를 포함합니다. 기본적으로 Laravel은 `web.php`와 `console.php` 두 개의 라우트 파일을 제공합니다.

- `web.php` 파일은 `web` 미들웨어 그룹에 포함될 라우트를 정의합니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 만약 애플리케이션이 무상태(stateless) RESTful API를 제공하지 않는다면 대부분의 라우트가 이 파일에 정의될 것입니다.

- `console.php` 파일은 클로저 기반의 콘솔 명령어들을 정의하는 곳입니다. 각 클로저는 명령어 인스턴스에 바인딩되어, 각 명령어의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션의 콘솔 진입점(라우트)을 제공합니다. 또한 `console.php` 파일에서 [스케줄링](/docs/11.x/scheduling) 작업을 설정할 수 있습니다.

필요에 따라 Artisan의 `install:api` 및 `install:broadcasting` 명령어를 사용해, API 라우트를 위한 `api.php` 파일과 브로드캐스팅 채널을 위한 `channels.php` 파일 같은 추가 라우트 파일을 설치할 수도 있습니다.

- `api.php` 파일은 무상태성(stateless)을 목적으로 하는 라우트를 포함하며, 이 경로로 들어오는 요청은 [토큰을 통한 인증](/docs/11.x/sanctum) 절차를 거치고 세션 상태에 접근할 수 없습니다.

- `channels.php` 파일은 애플리케이션이 지원하는 모든 [이벤트 브로드캐스팅](/docs/11.x/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### `storage` 디렉터리 (The Storage Directory)

`storage` 디렉터리는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 캐시, 그리고 프레임워크가 생성하는 기타 파일들을 저장합니다. 이 디렉터리는 `app`, `framework`, `logs` 하위 디렉터리로 구분되어 있습니다.

- `app` 디렉터리는 애플리케이션에서 생성하는 파일들을 저장하는 데 사용됩니다.
- `framework` 디렉터리는 프레임워크가 생성하는 파일과 캐시를 저장합니다.
- `logs` 디렉터리는 애플리케이션 로그 파일을 보관합니다.

특히 `storage/app/public` 디렉터리는 프로필 아바타 같은 사용자 생성 파일을 공개적으로 접근 가능하도록 저장하는 데 사용할 수 있습니다. 이 디렉터리를 `public/storage`에 심볼릭 링크로 연결해야 하며, `php artisan storage:link` Artisan 명령어로 이 링크를 쉽게 만들 수 있습니다.

<a name="the-tests-directory"></a>
### `tests` 디렉터리 (The Tests Directory)

`tests` 디렉터리에는 자동화된 테스트가 들어 있습니다. 예를 들어 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트가 기본으로 제공됩니다. 각 테스트 클래스는 반드시 이름 끝에 `Test`가 붙어야 합니다. 터미널에서 `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 테스트를 실행할 수 있고, 더 디테일하고 보기 좋은 결과를 원한다면 `php artisan test` Artisan 명령어를 사용할 수 있습니다.

<a name="the-vendor-directory"></a>
### `vendor` 디렉터리 (The Vendor Directory)

`vendor` 디렉터리에는 [Composer](https://getcomposer.org)로 설치한 의존 패키지들이 저장됩니다.

<a name="the-app-directory"></a>
## 앱 디렉터리 (The App Directory)

대부분의 애플리케이션 코드는 `app` 디렉터리에 위치합니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 하에 있으며, Composer의 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)을 통해 자동 로딩됩니다.

기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 디렉터리가 포함되어 있습니다. 하지만 시간이 지나면서 Artisan의 make 명령어로 클래스를 생성함에 따라 다양한 다른 디렉터리들이 추가로 생기게 됩니다. 예를 들어, `app/Console` 디렉터리는 `make:command` Artisan 명령어로 커맨드 클래스를 생성하기 전까지는 존재하지 않습니다.

`Console`과 `Http` 디렉터리는 이후에 각 섹션에서 더 자세히 설명하지만, 이 두 디렉터리는 애플리케이션 핵심에 접근하는 API 역할을 한다고 볼 수 있습니다. HTTP 프로토콜과 CLI는 둘 다 애플리케이션과 상호작용하는 방법이지만, 실제 애플리케이션 로직을 포함하는 곳은 아닙니다. 즉, 애플리케이션에 명령을 내릴 수 있는 두 가지 방식이란 의미입니다. `Console` 디렉터리는 모든 Artisan 커맨드를 포함하고, `Http` 디렉터리는 컨트롤러, 미들웨어, 요청을 포함합니다.

> [!NOTE]  
> `app` 디렉터리 내 다수 클래스는 Artisan 명령어로 쉽게 생성할 수 있습니다. 사용 가능한 make 명령어를 확인하려면 터미널에서 `php artisan list make` 명령어를 실행하세요.

<a name="the-broadcasting-directory"></a>
### `Broadcasting` 디렉터리 (The Broadcasting Directory)

`Broadcasting` 디렉터리는 애플리케이션의 모든 브로드캐스트 채널 클래스를 포함합니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 기본 설치에는 이 디렉터리가 없으나, 첫 번째 채널을 생성할 때 자동으로 만들어집니다. 채널에 관한 자세한 내용은 [이벤트 브로드캐스팅](/docs/11.x/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### `Console` 디렉터리 (The Console Directory)

`Console` 디렉터리는 애플리케이션을 위한 모든 커스텀 Artisan 커맨드를 포함합니다. 이 커맨드들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### `Events` 디렉터리 (The Events Directory)

기본 설치에 포함되어 있지 않으며, `event:generate` 또는 `make:event` Artisan 명령어로 생성됩니다. `Events` 디렉터리는 [이벤트 클래스](/docs/11.x/events)를 포함합니다. 이벤트는 애플리케이션의 다른 부분에서 특정 작업이 발생했음을 알리는 데 사용되어 높은 유연성과 느슨한 결합을 제공합니다.

<a name="the-exceptions-directory"></a>
### `Exceptions` 디렉터리 (The Exceptions Directory)

`Exceptions` 디렉터리는 애플리케이션에 필요한 커스텀 예외(classes)를 포함하며, `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### `Http` 디렉터리 (The Http Directory)

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청이 포함됩니다. 애플리케이션에 들어오는 요청을 처리하는 거의 모든 로직이 이 디렉터리에 위치합니다.

<a name="the-jobs-directory"></a>
### `Jobs` 디렉터리 (The Jobs Directory)

기본 설치에 포함되지 않으며, `make:job` Artisan 명령어로 생성됩니다. `Jobs` 디렉터리는 애플리케이션의 [큐잉 가능한 잡](/docs/11.x/queues)을 포함합니다. 잡은 비동기로 큐에 쌓이거나, 현재 요청 생명주기 내에서 동기적으로 실행될 수 있습니다. 현재 요청 과정에서 동기 실행되는 잡을 "커맨드"라고 부르기도 하는데, 이는 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현이기 때문입니다.

<a name="the-listeners-directory"></a>
### `Listeners` 디렉터리 (The Listeners Directory)

기본 설치에 포함되어 있지 않으며, `event:generate` 또는 `make:listener` Artisan 명령어로 생성됩니다. `Listeners` 디렉터리는 [이벤트](/docs/11.x/events)를 처리하는 클래스들을 포함합니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생 시 실행할 로직을 수행합니다. 예를 들어 `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
### `Mail` 디렉터리 (The Mail Directory)

기본 설치에 포함되어 있지 않으며, `make:mail` Artisan 명령어로 생성됩니다. `Mail` 디렉터리는 애플리케이션에서 보내는 [이메일 클래스](/docs/11.x/mail)를 포함합니다. Mail 객체는 이메일 생성 로직을 하나의 간단한 클래스로 캡슐화하며, `Mail::send` 메서드로 발송할 수 있습니다.

<a name="the-models-directory"></a>
### `Models` 디렉터리 (The Models Directory)

`Models` 디렉터리는 모든 [Eloquent 모델 클래스](/docs/11.x/eloquent)를 포함합니다. Laravel에 포함된 Eloquent ORM은 데이터베이스 작업을 위한 아름답고 간단한 ActiveRecord 구현체입니다. 각 데이터베이스 테이블마다 상응하는 "모델"이 있어, 데이터 조회 및 새 레코드 삽입에 사용됩니다.

<a name="the-notifications-directory"></a>
### `Notifications` 디렉터리 (The Notifications Directory)

기본 설치에 포함되어 있지 않으며, `make:notification` Artisan 명령어로 생성됩니다. `Notifications` 디렉터리는 애플리케이션에서 보내는 "트랜잭션성" [알림](/docs/11.x/notifications)들을 포함합니다. Laravel 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 추상화하여 알림을 전송할 수 있게 지원합니다.

<a name="the-policies-directory"></a>
### `Policies` 디렉터리 (The Policies Directory)

기본 설치에 포함되어 있지 않으며, `make:policy` Artisan 명령어로 생성됩니다. `Policies` 디렉터리는 애플리케이션의 [인가 정책 클래스](/docs/11.x/authorization)를 포함합니다. 정책은 사용자가 자원에 대해 특정 작업을 수행할 권한이 있는지 여부를 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
### `Providers` 디렉터리 (The Providers Directory)

`Providers` 디렉터리는 애플리케이션의 모든 [서비스 프로바이더](/docs/11.x/providers)를 포함합니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록 등 애플리케이션을 요청에 준비시키는 작업을 수행하며 애플리케이션 부트스트랩 역할을 합니다.

새로운 Laravel 애플리케이션에서는 기본적으로 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 이 디렉터리에 직접 서비스를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### `Rules` 디렉터리 (The Rules Directory)

기본 설치에 포함되어 있지 않으며, `make:rule` Artisan 명령어로 생성됩니다. `Rules` 디렉터리는 애플리케이션의 커스텀 유효성 검사 규칙 객체를 포함합니다. 복잡한 검증 로직을 단순한 객체로 캡슐화하는 데 사용됩니다. 자세한 내용은 [유효성 검사 문서](/docs/11.x/validation)를 참고하세요.