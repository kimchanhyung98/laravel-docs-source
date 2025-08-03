# 디렉토리 구조 (Directory Structure)

- [소개](#introduction)
- [루트 디렉토리](#the-root-directory)
    - [`app` 디렉토리](#the-root-app-directory)
    - [`bootstrap` 디렉토리](#the-bootstrap-directory)
    - [`config` 디렉토리](#the-config-directory)
    - [`database` 디렉토리](#the-database-directory)
    - [`public` 디렉토리](#the-public-directory)
    - [`resources` 디렉토리](#the-resources-directory)
    - [`routes` 디렉토리](#the-routes-directory)
    - [`storage` 디렉토리](#the-storage-directory)
    - [`tests` 디렉토리](#the-tests-directory)
    - [`vendor` 디렉토리](#the-vendor-directory)
- [앱 디렉토리](#the-app-directory)
    - [`Broadcasting` 디렉토리](#the-broadcasting-directory)
    - [`Console` 디렉토리](#the-console-directory)
    - [`Events` 디렉토리](#the-events-directory)
    - [`Exceptions` 디렉토리](#the-exceptions-directory)
    - [`Http` 디렉토리](#the-http-directory)
    - [`Jobs` 디렉토리](#the-jobs-directory)
    - [`Listeners` 디렉토리](#the-listeners-directory)
    - [`Mail` 디렉토리](#the-mail-directory)
    - [`Models` 디렉토리](#the-models-directory)
    - [`Notifications` 디렉토리](#the-notifications-directory)
    - [`Policies` 디렉토리](#the-policies-directory)
    - [`Providers` 디렉토리](#the-providers-directory)
    - [`Rules` 디렉토리](#the-rules-directory)

<a name="introduction"></a>
## 소개

기본 Laravel 애플리케이션 구조는 크고 작은 애플리케이션 모두에 훌륭한 출발점을 제공합니다. 그러나 애플리케이션을 원하는 방식으로 자유롭게 구성할 수 있습니다. Laravel은 Composer가 클래스를 자동 로드할 수 있는 한, 특정 클래스의 위치에 거의 제한을 두지 않습니다.

<a name="the-root-directory"></a>
## 루트 디렉토리

<a name="the-root-app-directory"></a>
### `app` 디렉토리

`app` 디렉토리는 애플리케이션의 핵심 코드를 포함합니다. 곧 이 디렉토리를 자세히 살펴보겠지만, 애플리케이션 내 거의 모든 클래스는 이 디렉토리 내에 위치합니다.

<a name="the-bootstrap-directory"></a>
### `bootstrap` 디렉토리

`bootstrap` 디렉토리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 포함되어 있습니다. 또한 라우트와 서비스 캐시 파일과 같은 성능 최적화용 프레임워크 생성 파일을 담는 `cache` 디렉토리도 이곳에 있습니다.

<a name="the-config-directory"></a>
### `config` 디렉토리

이름에서 알 수 있듯이, `config` 디렉토리에는 애플리케이션의 모든 설정 파일이 들어있습니다. 이 파일들을 꼼꼼히 읽어보고 사용 가능한 옵션을 익히는 것을 권장합니다.

<a name="the-database-directory"></a>
### `database` 디렉토리

`database` 디렉토리에는 데이터베이스 마이그레이션, 모델 팩토리 및 시드가 포함됩니다. 필요에 따라 이 디렉토리 안에 SQLite 데이터베이스를 보관할 수도 있습니다.

<a name="the-public-directory"></a>
### `public` 디렉토리

`public` 디렉토리는 모든 요청의 진입점이자 자동 로딩을 설정하는 `index.php` 파일을 포함합니다. 또한 이미지, JavaScript, CSS 같은 자산 파일을 보관하는 공간이기도 합니다.

<a name="the-resources-directory"></a>
### `resources` 디렉토리

`resources` 디렉토리에는 [뷰](/docs/master/views) 파일과 CSS, JavaScript 등의 아직 컴파일되지 않은 원본 자산이 있습니다.

<a name="the-routes-directory"></a>
### `routes` 디렉토리

`routes` 디렉토리에는 애플리케이션의 모든 라우트 정의가 들어있습니다. 기본적으로 Laravel은 `web.php`와 `console.php` 두 개의 라우트 파일을 포함합니다.

`web.php` 파일은 세션 상태, CSRF 보호, 쿠키 암호화를 제공하는 `web` 미들웨어 그룹에 포함되는 라우트를 정의합니다. 애플리케이션이 상태 비저장 RESTful API를 제공하지 않는다면, 대부분의 라우트는 이 파일에 정의될 것입니다.

`console.php` 파일은 클로저 기반의 콘솔 명령어를 정의하는 곳입니다. 각 클로저는 명령어 인스턴스에 바인딩되어 있어 명령어의 IO 메서드와 쉽게 상호 작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 기반 진입점(라우트)을 정의합니다. 또한 이 파일에서 작업 스케줄링도 할 수 있습니다.

선택적으로 `install:api` 및 `install:broadcasting` Artisan 명령어를 통해 API 라우트(`api.php`)와 방송 채널(`channels.php`)에 대한 추가 라우트 파일을 설치할 수 있습니다.

`api.php` 파일은 상태를 유지하지 않는 라우트를 위한 것으로, 이 라우트로 들어오는 요청은 [토큰](/docs/master/sanctum)을 통해 인증되며 세션 상태에 접근하지 않습니다.

`channels.php` 파일에서는 애플리케이션이 지원하는 모든 [이벤트 방송](/docs/master/broadcasting) 채널을 등록할 수 있습니다.

<a name="the-storage-directory"></a>
### `storage` 디렉토리

`storage` 디렉토리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시 등 프레임워크가 생성한 파일이 포함됩니다. 이 디렉토리는 `app`, `framework`, `logs` 하위 디렉토리로 구분됩니다. `app`은 애플리케이션에서 생성한 파일을 저장하는 데 사용되고, `framework`는 프레임워크 생성 파일과 캐시를 보관하며, `logs`는 애플리케이션 로그 파일이 저장됩니다.

`storage/app/public` 디렉토리는 프로필 아바타와 같은 사용자 생성 파일을 공개적으로 접근 가능하게 저장하는 용도로 사용될 수 있습니다. 이 디렉토리를 가리키는 심볼릭 링크를 `public/storage` 위치에 만들어야 하며, `php artisan storage:link` 명령어로 쉽게 생성할 수 있습니다.

<a name="the-tests-directory"></a>
### `tests` 디렉토리

`tests` 디렉토리에는 자동화된 테스트가 포함되어 있습니다. 기본적으로 [Pest](https://pestphp.com) 혹은 [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트의 예제가 제공됩니다. 각 테스트 클래스는 반드시 `Test`라는 접미사를 가져야 합니다. 테스트는 `/vendor/bin/pest`나 `/vendor/bin/phpunit` 명령어로 실행하거나, 테스트 결과를 좀 더 자세하고 보기 좋게 확인하려면 `php artisan test` Artisan 명령어를 사용할 수 있습니다.

<a name="the-vendor-directory"></a>
### `vendor` 디렉토리

`vendor` 디렉토리에는 [Composer](https://getcomposer.org) 의존성 패키지가 저장됩니다.

<a name="the-app-directory"></a>
## 앱 디렉토리

대부분의 애플리케이션 코드는 `app` 디렉토리에 포함되어 있습니다. 기본적으로 이 디렉토리는 `App` 네임스페이스 하에 있으며, Composer가 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)을 이용해 자동 로드합니다.

기본적으로 `app` 디렉토리에는 `Http`, `Models`, `Providers` 세 디렉토리가 포함되어 있습니다. 그러나 Artisan의 make 명령어를 통해 클래스를 생성하면 다양한 다른 디렉토리들도 추가로 생성됩니다. 예를 들어, `app/Console` 디렉토리는 `make:command` Artisan 명령어로 명령어 클래스를 생성하기 전까지는 존재하지 않습니다.

`Console`과 `Http` 디렉토리는 아래에서 더 상세히 설명하지만, 두 디렉토리는 애플리케이션 핵심에 대한 API 역할을 한다고 생각하면 됩니다. HTTP 프로토콜과 CLI 모두 애플리케이션과 상호 작용하는 수단이지만, 실제 애플리케이션 로직이 포함된 곳은 아닙니다. 즉, 두 방식은 애플리케이션에 명령을 내리는 두 가지 방법입니다. `Console` 디렉토리는 모든 Artisan 명령어를 포함하고, `Http` 디렉토리는 컨트롤러, 미들웨어, 요청 객체를 포함합니다.

> [!NOTE]
> `app` 디렉토리 내 많은 클래스는 Artisan 명령어로 생성할 수 있습니다. 가능한 명령어 목록은 터미널에서 `php artisan list make` 명령을 실행해 확인할 수 있습니다.

<a name="the-broadcasting-directory"></a>
### `Broadcasting` 디렉토리

`Broadcasting` 디렉토리에는 애플리케이션의 모든 방송 채널 클래스가 포함됩니다. 이 클래스들은 `make:channel` 명령어로 생성합니다. 기본적으로 이 디렉토리는 존재하지 않지만, 첫 채널을 생성할 때 자동으로 만들어집니다. 채널에 대한 자세한 내용을 알고 싶다면 [이벤트 방송](/docs/master/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### `Console` 디렉토리

`Console` 디렉토리에는 애플리케이션의 모든 사용자 정의 Artisan 명령어가 포함되어 있습니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### `Events` 디렉토리

기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 생성됩니다. `Events` 디렉토리는 [이벤트 클래스](/docs/master/events)를 보관합니다. 이벤트는 특정 동작이 발생했음을 애플리케이션 다른 부분에 알리는 데 사용되어, 높은 유연성과 결합도 감소 효과를 제공합니다.

<a name="the-exceptions-directory"></a>
### `Exceptions` 디렉토리

이 디렉토리에는 애플리케이션의 모든 사용자 정의 예외가 포함됩니다. `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### `Http` 디렉토리

`Http` 디렉토리에는 컨트롤러, 미들웨어, 폼 요청이 포함되어 있습니다. 애플리케이션으로 들어오는 요청을 처리하는 거의 모든 로직이 이곳에 위치합니다.

<a name="the-jobs-directory"></a>
### `Jobs` 디렉토리

기본적으로 존재하지 않지만 `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉토리에는 애플리케이션의 [큐 가능한 작업](/docs/master/queues)을 포함합니다. 작업은 애플리케이션에서 큐에 넣어 비동기 처리하거나 현재 요청 라이프사이클에서 동기적으로 실행할 수 있습니다. 현재 요청 중 동기적으로 실행되는 작업은 종종 "커맨드"라고 불리는데, 이는 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)을 구현한 것이기 때문입니다.

<a name="the-listeners-directory"></a>
### `Listeners` 디렉토리

기본적으로 존재하지 않지만 `event:generate` 또는 `make:listener` Artisan 명령어를 실행하면 생성됩니다. `Listeners` 디렉토리에는 [이벤트](/docs/master/events)를 처리하는 클래스가 포함되어 있습니다. 이벤트 리스너는 이벤트 인스턴스를 받아 해당 이벤트가 발생했을 때 실행할 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너에 의해 처리될 수 있습니다.

<a name="the-mail-directory"></a>
### `Mail` 디렉토리

기본적으로 존재하지 않지만 `make:mail` Artisan 명령어를 실행하면 생성됩니다. `Mail` 디렉토리에는 애플리케이션에서 발송하는 [이메일을 나타내는 클래스](/docs/master/mail)가 포함되어 있습니다. Mail 객체는 메일을 구성하는 모든 로직을 하나의 단순한 클래스로 캡슐화하여, `Mail::send` 메서드로 손쉽게 전송할 수 있게 해줍니다.

<a name="the-models-directory"></a>
### `Models` 디렉토리

`Models` 디렉토리에는 모든 [Eloquent 모델 클래스](/docs/master/eloquent)가 포함됩니다. Laravel의 Eloquent ORM은 데이터베이스 작업을 위한 아름답고 단순한 ActiveRecord 구현체를 제공합니다. 각 데이터베이스 테이블에 대응하는 "모델" 클래스를 통해, 테이블에 대한 쿼리를 수행하고 새 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
### `Notifications` 디렉토리

기본적으로 존재하지 않지만 `make:notification` Artisan 명령어를 실행하면 생성됩니다. `Notifications` 디렉토리에는 애플리케이션에서 발송하는 "트랜잭셔널" [알림](/docs/master/notifications) 클래스들이 포함되어 있습니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 통해 알림을 추상화해서 보낼 수 있게 해줍니다.

<a name="the-policies-directory"></a>
### `Policies` 디렉토리

기본적으로 존재하지 않지만 `make:policy` Artisan 명령어를 실행하면 생성됩니다. `Policies` 디렉토리에는 애플리케이션의 [인가 정책 클래스](/docs/master/authorization)가 포함됩니다. 정책 클래스는 사용자가 특정 리소스에 대해 어떤 작업을 수행할 권한이 있는지 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
### `Providers` 디렉토리

`Providers` 디렉토리에는 애플리케이션의 모든 [서비스 프로바이더](/docs/master/providers)가 포함됩니다. 서비스 프로바이더는 서비스 컨테이너에 바인딩을 하거나, 이벤트를 등록하거나, 애플리케이션을 요청 처리할 준비를 하도록 부트스트랩하는 역할을 합니다.

새로운 Laravel 애플리케이션에서는 이미 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 직접 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### `Rules` 디렉토리

기본적으로 존재하지 않지만 `make:rule` Artisan 명령어를 실행하면 생성됩니다. `Rules` 디렉토리에는 애플리케이션의 커스텀 유효성 검증 규칙 객체들이 포함됩니다. 이 규칙 클래스들은 복잡한 검증 로직을 단순한 객체로 캡슐화하는 용도로 사용됩니다. 자세한 내용은 [유효성 검증 문서](/docs/master/validation)를 참고하세요.