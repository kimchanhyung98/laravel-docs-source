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
## 소개 (Introduction)

기본 Laravel 애플리케이션 구조는 크고 작은 애플리케이션 모두에 훌륭한 출발점을 제공하도록 설계되었습니다. 하지만 애플리케이션을 원하는 방식으로 자유롭게 구성할 수 있습니다. Laravel은 Composer가 클래스를 자동 로드할 수 있다는 조건 하에 특정 클래스가 어디에 위치해야 한다는 제약을 거의 두지 않습니다.

<a name="the-root-directory"></a>
## 루트 디렉토리 (The Root Directory)

<a name="the-root-app-directory"></a>
#### `app` 디렉토리

`app` 디렉토리는 애플리케이션의 핵심 코드를 담고 있습니다. 이 디렉토리는 곧 자세히 살펴보겠지만, 애플리케이션 내 거의 모든 클래스가 이 디렉토리에 위치합니다.

<a name="the-bootstrap-directory"></a>
#### `bootstrap` 디렉토리

`bootstrap` 디렉토리는 프레임워크를 부트스트랩하는 `app.php` 파일을 포함하고 있습니다. 또한, 라우트와 서비스 캐시 파일과 같은 성능 최적화용 프레임워크 생성 파일들이 저장되는 `cache` 디렉토리도 이곳에 있습니다. 일반적으로 이 디렉토리 내 파일을 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
#### `config` 디렉토리

이름 그대로 `config` 디렉토리는 애플리케이션의 모든 구성 파일을 담고 있습니다. 이 파일들을 모두 읽고 사용 가능한 옵션들을 익히는 것이 좋습니다.

<a name="the-database-directory"></a>
#### `database` 디렉토리

`database` 디렉토리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 포함되어 있습니다. 필요에 따라 SQLite 데이터베이스 파일을 보관하는 용도로도 사용할 수 있습니다.

<a name="the-public-directory"></a>
#### `public` 디렉토리

`public` 디렉토리는 모든 요청이 진입하는 진입점인 `index.php` 파일과 자동 로딩 구성이 포함되어 있습니다. 또한, 이미지, JavaScript, CSS 등 자산 파일들도 이 디렉토리에 위치합니다.

<a name="the-resources-directory"></a>
#### `resources` 디렉토리

`resources` 디렉토리는 [뷰](/docs/{{version}}/views)뿐만 아니라 컴파일되지 않은 원본 자산(CSS, JavaScript 등)을 담고 있습니다. 그리고 모든 언어 파일이 이 디렉토리에 있습니다.

<a name="the-routes-directory"></a>
#### `routes` 디렉토리

`routes` 디렉토리에는 애플리케이션의 모든 라우트 정의가 포함되어 있습니다. 기본적으로 Laravel에는 `web.php`, `api.php`, `console.php`, `channels.php` 라우트 파일이 제공됩니다.

- `web.php` 파일은 `RouteServiceProvider`가 `web` 미들웨어 그룹에 포함하는 라우트를 담고 있습니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. RESTful API를 별도로 제공하지 않는 한 대부분의 라우트가 여기에 정의됩니다.
- `api.php` 파일은 `RouteServiceProvider`가 `api` 미들웨어 그룹에 포함하는 라우트를 담고 있습니다. 이 라우트들은 상태 비저장(stateless) API를 위한 것으로, 토큰 기반 인증([토큰 인증](/docs/{{version}}/sanctum))을 사용하며 세션 상태에 접근하지 않습니다.
- `console.php` 파일은 클로저 기반의 커스텀 콘솔 명령어를 정의하는 곳입니다. 각 클로저는 명령 인스턴스에 바인딩되어 명령어의 입출력 메서드에 쉽게 접근할 수 있습니다. HTTP 라우트를 정의하지 않지만 콘솔 명령어(입력 경로)를 정의합니다.
- `channels.php` 파일에서는 애플리케이션이 지원하는 모든 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록할 수 있습니다.

<a name="the-storage-directory"></a>
#### `storage` 디렉토리

`storage` 디렉토리는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 캐시, 그리고 프레임워크가 생성한 기타 파일이 저장됩니다. 이 디렉토리는 `app`, `framework`, `logs`로 구분되어 있습니다. 
- `app` 디렉토리는 애플리케이션에서 생성하는 파일 저장에 사용됩니다. 
- `framework` 디렉토리는 프레임워크가 생성하는 파일과 캐시 저장에 사용합니다.
- `logs` 디렉토리에는 애플리케이션 로그 파일이 있습니다.

`storage/app/public` 디렉토리는 프로필 아바타 같은 사용자 생성 파일을 공개적으로 저장할 때 사용됩니다. 이 디렉토리를 가리키는 심볼릭 링크를 `public/storage`에 만들어야 하며, `php artisan storage:link` Artisan 명령어로 생성할 수 있습니다.

<a name="the-tests-directory"></a>
#### `tests` 디렉토리

`tests` 디렉토리는 자동화 테스트를 포함합니다. 기본적으로 [PHPUnit](https://phpunit.de/) 단위 및 기능 테스트 예제가 제공됩니다. 각 테스트 클래스 이름은 `Test` 접미사가 붙습니다. 테스트는 `phpunit` 또는 `php vendor/bin/phpunit` 명령으로 실행할 수 있습니다. 좀 더 상세하고 보기 좋은 결과를 원한다면 `php artisan test` Artisan 명령어를 이용할 수 있습니다.

<a name="the-vendor-directory"></a>
#### `vendor` 디렉토리

`vendor` 디렉토리는 [Composer](https://getcomposer.org) 의존성 패키지를 저장합니다.

<a name="the-app-directory"></a>
## 앱 디렉토리 (The App Directory)

애플리케이션 대부분은 `app` 디렉토리에 저장됩니다. 기본적으로 이 디렉토리는 `App` 네임스페이스 하에 있으며, [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)을 사용하는 Composer에 의해 자동 로드됩니다.

`app` 디렉토리 내부에는 `Console`, `Http`, `Providers` 같은 다양한 하위 디렉토리가 있습니다. `Console`과 `Http` 디렉토리는 애플리케이션 핵심에 대한 API 역할을 한다고 생각할 수 있습니다. HTTP 프로토콜과 CLI는 앱과 상호작용하는 방법이며 애플리케이션 로직 그 자체가 아닙니다. 즉, 애플리케이션에 명령을 내리는 두 가지 방식입니다. `Console` 디렉토리는 Artisan 명령어를, `Http` 디렉토리는 컨트롤러, 미들웨어, 요청을 포함합니다.

`make` Artisan 명령어로 클래스를 생성할 때마다 `app` 디렉토리 내에 다양한 하위 디렉토리가 만들어집니다. 예를 들어, `app/Jobs` 디렉토리는 `make:job` 명령어로 잡 클래스를 생성할 때까지 존재하지 않습니다.

> [!TIP]
> `app` 디렉토리 내 많은 클래스가 Artisan 명령어로 생성 가능합니다. 사용 가능한 명령어를 확인하려면 터미널에서 `php artisan list make` 명령어를 실행하세요.

<a name="the-broadcasting-directory"></a>
#### `Broadcasting` 디렉토리

`Broadcasting` 디렉토리는 애플리케이션의 모든 브로드캐스트 채널 클래스를 포함합니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 이 디렉토리는 기본적으로 존재하지 않지만, 첫 번째 채널을 생성하면 자동으로 만들어집니다. 채널에 대해 더 알고 싶다면 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
#### `Console` 디렉토리

`Console` 디렉토리는 애플리케이션의 모든 커스텀 Artisan 명령어를 담고 있습니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다. 또한 커스텀 Artisan 명령어가 등록되는 콘솔 커널과 [스케줄된 작업](/docs/{{version}}/scheduling)이 정의되는 곳이기도 합니다.

<a name="the-events-directory"></a>
#### `Events` 디렉토리

기본으로 존재하지 않지만 `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 생성됩니다. `Events` 디렉토리는 [이벤트 클래스](/docs/{{version}}/events)를 저장합니다. 이벤트는 특정 동작이 발생했음을 애플리케이션의 다른 부분에 알리는 데 사용되어 큰 유연성과 결합도 완화를 제공합니다.

<a name="the-exceptions-directory"></a>
#### `Exceptions` 디렉토리

`Exceptions` 디렉토리는 애플리케이션의 예외 핸들러를 포함하며, 애플리케이션이 던지는 예외 클래스를 두기에 적합합니다. 예외가 기록되거나 렌더링되는 방식을 커스터마이징하고 싶다면 이 디렉토리 내 `Handler` 클래스를 수정하세요.

<a name="the-http-directory"></a>
#### `Http` 디렉토리

`Http` 디렉토리는 컨트롤러, 미들웨어, 폼 요청을 포함합니다. 애플리케이션으로 들어오는 요청을 처리하는 거의 모든 로직이 이 디렉토리에 위치합니다.

<a name="the-jobs-directory"></a>
#### `Jobs` 디렉토리

기본으로 존재하지 않지만 `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉토리는 애플리케이션의 [큐에 넣을 수 있는 잡](/docs/{{version}}/queues)을 포함합니다. 잡은 애플리케이션에서 큐에 넣거나 현재 요청 생명주기 내에서 동기적으로 실행할 수 있습니다. 현재 요청 중 동기적으로 실행하는 잡은 커맨드 패턴의 구현이므로 때때로 "commands"라고 불립니다.

<a name="the-listeners-directory"></a>
#### `Listeners` 디렉토리

기본으로 존재하지 않지만 `event:generate` 또는 `make:listener` Artisan 명령어를 실행하면 생성됩니다. `Listeners` 디렉토리는 [이벤트를 처리하는 클래스](/docs/{{version}}/events)를 포함합니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생에 따른 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트가 발생하면 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
#### `Mail` 디렉토리

기본으로 존재하지 않지만 `make:mail` Artisan 명령어를 실행하면 생성됩니다. `Mail` 디렉토리는 애플리케이션에서 보내는 모든 [이메일 클래스](/docs/{{version}}/mail)를 포함합니다. 메일 객체는 이메일 작성 로직을 단일하고 간단한 클래스로 캡슐화하며, `Mail::send` 메서드로 보낼 수 있습니다.

<a name="the-models-directory"></a>
#### `Models` 디렉토리

`Models` 디렉토리는 모든 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)를 포함합니다. Laravel에 내장된 Eloquent ORM은 데이터베이스 작업을 위한 심플하고 아름다운 ActiveRecord 구현체를 제공합니다. 각 데이터베이스 테이블에 대응하는 "모델"로서 해당 테이블 자료를 조회하거나 새 레코드 삽입에 활용됩니다.

<a name="the-notifications-directory"></a>
#### `Notifications` 디렉토리

기본으로 존재하지 않지만 `make:notification` Artisan 명령어를 실행하면 생성됩니다. `Notifications` 디렉토리는 애플리케이션에서 보내는 "트랜잭셔널" [알림](/docs/{{version}}/notifications) 클래스를 포함합니다. 예를 들어 애플리케이션 내 특정 이벤트에 관한 간단한 알림이 여기에 속합니다. Laravel 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 추상화합니다.

<a name="the-policies-directory"></a>
#### `Policies` 디렉토리

기본으로 존재하지 않지만 `make:policy` Artisan 명령어를 실행하면 생성됩니다. `Policies` 디렉토리는 애플리케이션의 [인가 정책 클래스](/docs/{{version}}/authorization)를 포함합니다. 정책 클래스는 사용자가 특정 리소스에 대해 어떤 행동을 할 수 있는지 판단하는 역할을 합니다.

<a name="the-providers-directory"></a>
#### `Providers` 디렉토리

`Providers` 디렉토리는 애플리케이션의 모든 [서비스 프로바이더](/docs/{{version}}/providers)를 포함합니다. 서비스 프로바이더는 서비스 컨테이너에 바인딩하거나 이벤트를 등록하는 등 애플리케이션 부트스트랩 역할을 수행해 요청 처리 준비를 합니다.

새 Laravel 애플리케이션에서는 이미 여러 프로바이더가 포함되어 있습니다. 필요에 따라 추가 프로바이더를 자유롭게 이 디렉토리에 넣을 수 있습니다.

<a name="the-rules-directory"></a>
#### `Rules` 디렉토리

기본으로 존재하지 않지만 `make:rule` Artisan 명령어를 실행하면 생성됩니다. `Rules` 디렉토리는 애플리케이션의 커스텀 유효성 검사 규칙 객체를 담습니다. 규칙 객체는 복잡한 유효성 검사 로직을 단순한 객체로 캡슐화합니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.