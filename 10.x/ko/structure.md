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

기본 Laravel 애플리케이션 구조는 대규모 또는 소규모 애플리케이션 모두에 적합한 훌륭한 출발점을 제공합니다. 하지만 애플리케이션 구성을 원하는 대로 자유롭게 조직할 수 있습니다. Laravel은 Composer가 클래스를 자동 로드할 수 있는 한, 특정 클래스의 위치에 거의 제한을 두지 않습니다.

> [!NOTE]  
> Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)에서 첫 Laravel 애플리케이션을 만들면서 프레임워크를 실습하는 과정을 체험해 보세요.

<a name="the-root-directory"></a>
## 루트 디렉터리 (The Root Directory)

<a name="the-root-app-directory"></a>
#### `app` 디렉터리

`app` 디렉터리는 애플리케이션의 핵심 코드를 담고 있습니다. 곧 자세히 살펴보겠지만, 애플리케이션 내 대부분의 클래스가 이 디렉터리에 위치합니다.

<a name="the-bootstrap-directory"></a>
#### `bootstrap` 디렉터리

`bootstrap` 디렉터리는 프레임워크를 부트스트랩하는 `app.php` 파일을 포함합니다. 또한 성능 최적화를 위한 라우트 및 서비스 캐시 파일 같은 프레임워크 생성 파일이 저장된 `cache` 디렉터리를 포함하고 있습니다. 보통 이 디렉터리 내 파일을 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
#### `config` 디렉터리

말 그대로, `config` 디렉터리는 애플리케이션의 모든 설정 파일이 들어 있습니다. 모든 설정 파일을 살펴보며 제공되는 옵션을 익히는 것을 권장합니다.

<a name="the-database-directory"></a>
#### `database` 디렉터리

`database` 디렉터리는 데이터베이스 마이그레이션, 모델 팩토리, 시드를 포함합니다. 원한다면 SQLite 데이터베이스 파일도 이 디렉터리에 둘 수 있습니다.

<a name="the-public-directory"></a>
#### `public` 디렉터리

`public` 디렉터리는 모든 요청이 진입하는 진입점인 `index.php` 파일과 자동 로딩 구성을 포함합니다. 또한 이미지, 자바스크립트, CSS 같은 자산들이 이 디렉터리에 위치합니다.

<a name="the-resources-directory"></a>
#### `resources` 디렉터리

`resources` 디렉터리는 [뷰](/docs/10.x/views)와 CSS나 자바스크립트와 같은 원본 컴파일되지 않은 자산을 포함합니다.

<a name="the-routes-directory"></a>
#### `routes` 디렉터리

`routes` 디렉터리는 애플리케이션의 모든 라우트 정의를 포함합니다. 기본적으로 Laravel은 `web.php`, `api.php`, `console.php`, `channels.php` 파일을 제공합니다.

- `web.php` 파일은 `RouteServiceProvider`가 `web` 미들웨어 그룹에 배치하는 라우트를 정의합니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 애플리케이션이 상태가 없는 RESTful API가 아니라면 대부분의 라우트가 이 파일에 정의됩니다.

- `api.php` 파일은 `RouteServiceProvider`가 `api` 미들웨어 그룹에 배치하는 라우트를 포함합니다. 이 라우트들은 상태가 없는(stateless) 것으로, 토큰 인증을 통해 요청이 인증되고 세션 상태 접근이 없습니다.

- `console.php` 파일은 클로저 기반 콘솔 명령어를 정의하는 곳입니다. 각 클로저는 명령어 인스턴스에 바인딩되어 명령어 IO 메서드를 쉽게 사용할 수 있습니다. HTTP 라우트는 정의하지 않지만 콘솔용 진입점 역할을 합니다.

- `channels.php` 파일은 애플리케이션에서 지원하는 모든 [이벤트 브로드캐스팅](/docs/10.x/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
#### `storage` 디렉터리

`storage` 디렉터리는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 캐시 및 기타 프레임워크 생성 파일들을 저장합니다. 세부적으로는 `app`, `framework`, `logs` 디렉터리로 구분됩니다. 
- `app` 디렉터리는 애플리케이션이 생성한 파일을 저장합니다.  
- `framework` 디렉터리는 프레임워크가 생성한 파일과 캐시를 보관합니다.  
- `logs` 디렉터리는 애플리케이션 로그 파일을 포함합니다.

`storage/app/public` 디렉터리는 프로필 아바타 같은 사용자 생성 파일을 공개 저장소로 쓸 수 있습니다. 이 디렉터리를 가리키는 `public/storage` 심볼릭 링크를 생성해야 하며, `php artisan storage:link` Artisan 명령어로 쉽게 만들 수 있습니다.

`storage` 디렉터리 위치는 `LARAVEL_STORAGE_PATH` 환경 변수로 변경할 수 있습니다.

<a name="the-tests-directory"></a>
#### `tests` 디렉터리

`tests` 디렉터리는 자동화 테스트를 포함합니다. 기본으로 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트 예제가 들어 있습니다. 각 테스트 클래스는 반드시 `Test` 접미어를 붙여야 합니다. `phpunit` 또는 `php vendor/bin/phpunit` 명령으로 테스트를 실행하거나, 좀 더 예쁘고 상세한 결과를 보고 싶다면 `php artisan test` Artisan 명령을 사용할 수 있습니다.

<a name="the-vendor-directory"></a>
#### `vendor` 디렉터리

`vendor` 디렉터리는 [Composer](https://getcomposer.org) 의존성을 포함합니다.

<a name="the-app-directory"></a>
## 앱 디렉터리 (The App Directory)

애플리케이션 대부분이 `app` 디렉터리에 위치합니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 아래에 있으며, Composer가 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)에 따라 자동 로드합니다.

`app` 디렉터리 안에는 `Console`, `Http`, `Providers` 같은 여러 서브 디렉터리가 있습니다. `Console`과 `Http` 디렉터리는 애플리케이션 핵심에 대한 API 역할을 합니다. HTTP 프로토콜과 CLI는 두 가지 다른 방식으로 애플리케이션과 상호작용하는 수단이지만, 실제 애플리케이션 로직을 담고 있지 않습니다. 다시 말해, 명령을 내리는 두 가지 방법인 셈입니다. `Console` 디렉터리는 모든 Artisan 명령어를, `Http` 디렉터리는 컨트롤러, 미들웨어, 요청을 담고 있습니다.

더 많은 클래스가 Artisan의 `make` 명령어로 생성됨에 따라 `app` 디렉터리 내에 여러 하위 디렉터리가 추가로 만들어집니다. 예를 들어 `app/Jobs` 디렉터리는 `make:job` Artisan 명령으로 작업 클래스를 생성하기 전까지는 존재하지 않습니다.

> [!NOTE]  
> `app` 디렉터리 내의 많은 클래스는 Artisan 명령으로 생성할 수 있습니다. 사용 가능한 명령어 목록을 확인하려면 터미널에서 `php artisan list make` 명령을 실행하세요.

<a name="the-broadcasting-directory"></a>
#### `Broadcasting` 디렉터리

`Broadcasting` 디렉터리는 애플리케이션의 브로드캐스트 채널 클래스를 포함합니다. 이 클래스들은 `make:channel` 명령으로 생성합니다. 기본 생성되어 있지 않지만, 채널을 처음 생성할 때 해당 디렉터리가 만들어집니다. 채널에 관해 더 알고 싶다면 [이벤트 브로드캐스팅](/docs/10.x/broadcasting) 문서를 참조하세요.

<a name="the-console-directory"></a>
#### `Console` 디렉터리

`Console` 디렉터리는 애플리케이션 커스텀 Artisan 명령어를 모두 담고 있습니다. 이 명령어들은 `make:command` 명령으로 생성할 수 있습니다. 이 디렉터리에는 또한 콘솔 커널이 포함되며, 이곳에서 커스텀 Artisan 명령어 등록과 [예약 작업](/docs/10.x/scheduling)이 정의됩니다.

<a name="the-events-directory"></a>
#### `Events` 디렉터리

기본 생성되어 있지는 않지만, `event:generate` 및 `make:event` Artisan 명령으로 생성할 때 만들어집니다. `Events` 디렉터리는 [이벤트 클래스](/docs/10.x/events)를 담고 있습니다. 이벤트는 특정 동작이 발생했음을 애플리케이션의 다른 부분에 알려 복잡한 구조를 느슨하게 연결할 때 유용합니다.

<a name="the-exceptions-directory"></a>
#### `Exceptions` 디렉터리

`Exceptions` 디렉터리는 애플리케이션의 예외 처리기와 예외 클래스들을 포함합니다. 예외가 기록되고 렌더링되는 방식을 커스터마이징하려면, 이 디렉터리 내 `Handler` 클래스를 수정하면 됩니다.

<a name="the-http-directory"></a>
#### `Http` 디렉터리

`Http` 디렉터리는 컨트롤러, 미들웨어, 폼 요청 클래스를 포함합니다. 애플리케이션으로 들어오는 요청을 처리하는 거의 모든 로직이 이곳에 위치합니다.

<a name="the-jobs-directory"></a>
#### `Jobs` 디렉터리

기본으로 생성되어 있지 않지만, `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리는 애플리케이션의 [큐 작업](/docs/10.x/queues)을 포함합니다. 작업은 애플리케이션에서 큐에 넣어 비동기로 실행하거나 현재 요청 라이프사이클 내에서 동기 실행할 수 있습니다. 현재 요청 중에 동기 실행되는 작업은 때때로 "명령(command)"이라고도 하는데, 이는 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern) 구현의 일종입니다.

<a name="the-listeners-directory"></a>
#### `Listeners` 디렉터리

이 디렉터리는 기본으로 존재하지 않지만, `event:generate` 또는 `make:listener` Artisan 명령 실행 시 생성됩니다. `Listeners` 디렉터리는 [이벤트 핸들러 클래스](/docs/10.x/events)를 포함합니다. 이벤트 리스너는 이벤트 인스턴스를 받아 그에 대응하는 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트가 발생하면 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
#### `Mail` 디렉터리

이 디렉터리도 기본으로 존재하지 않지만, `make:mail` Artisan 명령 실행 시 생성됩니다. `Mail` 디렉터리는 애플리케이션에서 보내는 이메일을 나타내는 모든 클래스를 포함합니다. Mail 객체로 이메일 생성 로직을 한 클래스에 캡슐화해 `Mail::send` 메서드를 사용해 간편히 이메일을 보낼 수 있습니다.

<a name="the-models-directory"></a>
#### `Models` 디렉터리

`Models` 디렉터리는 모든 [Eloquent 모델 클래스](/docs/10.x/eloquent)를 포함합니다. Laravel에 포함된 Eloquent ORM은 데이터베이스를 다루기 위한 아름답고 간단한 액티브 레코드 구현체를 제공합니다. 각 데이터베이스 테이블은 상응하는 모델을 가지고 있으며, 모델을 통해 테이블의 데이터를 조회하거나 새 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
#### `Notifications` 디렉터리

기본으로 생성되어 있지 않지만, `make:notification` Artisan 명령으로 생성됩니다. `Notifications` 디렉터리는 애플리케이션에서 보내는 "트랜잭셔널" [알림](/docs/10.x/notifications)을 포함합니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 추상화하여 알림을 전송합니다.

<a name="the-policies-directory"></a>
#### `Policies` 디렉터리

기본으로 존재하지 않지만, `make:policy` Artisan 명령 실행 시 생성됩니다. `Policies` 디렉터리는 애플리케이션의 [인가 정책 클래스](/docs/10.x/authorization)를 담고 있습니다. 정책은 사용자가 특정 리소스에 대해 주어진 작업을 수행할 수 있는지 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
#### `Providers` 디렉터리

`Providers` 디렉터리는 애플리케이션의 모든 [서비스 프로바이더](/docs/10.x/providers)를 포함합니다. 서비스 프로바이더는 서비스 컨테이너에 바인딩하거나 이벤트를 등록하는 등, 요청이 들어오기 전에 애플리케이션을 부트스트랩하는 역할을 합니다.

새 Laravel 애플리케이션에는 이미 여러 프로바이더가 포함되어 있습니다. 필요에 따라 직접 프로바이더를 추가할 수도 있습니다.

<a name="the-rules-directory"></a>
#### `Rules` 디렉터리

기본으로 존재하지 않으며, `make:rule` Artisan 명령어 실행 시 생성됩니다. `Rules` 디렉터리는 애플리케이션의 사용자 정의 유효성 검증 규칙 객체를 포함합니다. 복잡한 유효성 검증 로직을 간단한 객체로 캡슐화할 때 사용합니다. 자세한 내용은 [유효성 검증 문서](/docs/10.x/validation)를 참조하세요.