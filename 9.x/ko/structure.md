# 디렉터리 구조 (Directory Structure)

- [소개](#introduction)
- [루트 디렉터리](#the-root-directory)
    - [`app` 디렉터리](#the-root-app-directory)
    - [`bootstrap` 디렉터리](#the-bootstrap-directory)
    - [`config` 디렉터리](#the-config-directory)
    - [`database` 디렉터리](#the-database-directory)
    - [`lang` 디렉터리](#the-lang-directory)
    - [`public` 디렉터리](#the-public-directory)
    - [`resources` 디렉터리](#the-resources-directory)
    - [`routes` 디렉터리](#the-routes-directory)
    - [`storage` 디렉터리](#the-storage-directory)
    - [`tests` 디렉터리](#the-tests-directory)
    - [`vendor` 디렉터리](#the-vendor-directory)
- [App 디렉터리](#the-app-directory)
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

기본 Laravel 애플리케이션 구조는 크고 작은 애플리케이션 모두에 적합한 훌륭한 출발점을 제공합니다. 하지만 애플리케이션 구조를 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 Composer가 클래스 자동 로딩을 할 수 있다는 전제 하에, 해당 클래스가 어디에 위치하는지 거의 제한하지 않습니다.

> [!NOTE]
> Laravel 초보자라면 [Laravel Bootcamp](https://bootcamp.laravel.com)를 참고해 보세요. 첫 Laravel 애플리케이션을 구축하며 프레임워크를 실습해 볼 수 있습니다.

<a name="the-root-directory"></a>
## 루트 디렉터리 (The Root Directory)

<a name="the-root-app-directory"></a>
#### App 디렉터리

`app` 디렉터리는 애플리케이션의 핵심 코드를 담고 있습니다. 본문에서 자세히 다룰 예정이지만, 애플리케이션 내 거의 모든 클래스가 이 디렉터리에 위치합니다.

<a name="the-bootstrap-directory"></a>
#### Bootstrap 디렉터리

`bootstrap` 디렉터리는 프레임워크를 부트스트랩하는 `app.php` 파일을 포함합니다. 이 디렉터리 내에 성능 최적화를 위해 생성된 라우트 및 서비스 캐시 파일 같은 프레임워크 생성 파일을 담는 `cache` 디렉터리도 있습니다. 일반적으로 이 디렉터리 내의 파일을 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
#### Config 디렉터리

`config` 디렉터리는 이름 그대로 애플리케이션의 모든 설정 파일을 포함합니다. 모든 설정 옵션을 숙지하기 위해 이 파일들을 꼼꼼히 읽어보는 것이 좋습니다.

<a name="the-database-directory"></a>
#### Database 디렉터리

`database` 디렉터리는 데이터베이스 마이그레이션, 모델 팩토리, 시드(seed) 파일들을 포함합니다. 원한다면 이 위치에 SQLite 데이터베이스 파일을 둘 수도 있습니다.

<a name="the-lang-directory"></a>
#### Lang 디렉터리

`lang` 디렉터리는 애플리케이션의 모든 언어 파일을 담고 있습니다.

<a name="the-public-directory"></a>
#### Public 디렉터리

`public` 디렉터리는 애플리케이션으로 들어오는 모든 요청의 진입점인 `index.php` 파일이 위치합니다. 이 파일은 자동 로딩을 설정합니다. 또한 이미지, JavaScript, CSS 등 자산 파일들도 이 디렉터리에 저장됩니다.

<a name="the-resources-directory"></a>
#### Resources 디렉터리

`resources` 디렉터리는 [뷰](/docs/9.x/views)와 컴파일되지 않은 원시 자산(CSS, JavaScript 등)을 보관합니다.

<a name="the-routes-directory"></a>
#### Routes 디렉터리

`routes` 디렉터리는 애플리케이션의 모든 라우트 정의 파일을 포함합니다. Laravel에서는 기본적으로 `web.php`, `api.php`, `console.php`, `channels.php` 파일이 제공됩니다.

- `web.php` 파일은 `RouteServiceProvider`가 `web` 미들웨어 그룹에 배치하는 라우트를 담습니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 애플리케이션이 RESTful API가 아닌 경우 대부분의 라우트가 이 파일에 정의됩니다.
- `api.php` 파일은 `RouteServiceProvider`가 `api` 미들웨어 그룹에 배치하는 라우트를 담습니다. 이 라우트들은 상태 비저장(stateless) API 용도로, 토큰을 통한 인증이 적용되며 세션 상태에 접근할 수 없습니다.
- `console.php` 파일은 클로저 기반 커스텀 콘솔 커맨드를 정의하는 곳입니다. 각 클로저는 커맨드 인스턴스에 바인딩되어 커맨드의 입출력 메서드를 쉽게 사용할 수 있습니다. HTTP 라우트를 정의하지는 않지만, 콘솔 진입점 역할을 합니다.
- `channels.php` 파일은 애플리케이션이 지원하는 모든 [이벤트 방송](/docs/9.x/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
#### Storage 디렉터리

`storage` 디렉터리는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시 그리고 프레임워크에서 생성하는 기타 파일을 포함합니다. 이 디렉터리는 `app`, `framework`, `logs` 하위 디렉터리로 구분됩니다. 

- `app` 디렉터리는 애플리케이션이 생성하는 파일들을 저장할 수 있습니다.
- `framework` 디렉터리는 프레임워크 생성 파일과 캐시를 저장합니다.
- `logs` 디렉터리는 애플리케이션 로그 파일을 보관합니다.

`storage/app/public` 디렉터리는 프로필 아바타 같은 사용자가 생성한 파일을 공개적으로 저장하는 공간입니다. 이를 `public/storage`에 심볼릭 링크로 연결해야 하며, `php artisan storage:link` Artisan 명령어로 쉽게 생성할 수 있습니다.

<a name="the-tests-directory"></a>
#### Tests 디렉터리

`tests` 디렉터리는 자동화된 테스트 코드를 담고 있습니다. 기본적으로 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트 샘플이 포함되어 있습니다. 각 테스트 클래스명은 `Test` 접미어를 갖습니다. 테스트는 `phpunit` 또는 `php vendor/bin/phpunit` 명령어로 실행할 수 있으며, 보다 상세하고 보기 좋은 테스트 결과를 원한다면 `php artisan test` Artisan 명령어를 사용할 수 있습니다.

<a name="the-vendor-directory"></a>
#### Vendor 디렉터리

`vendor` 디렉터리는 [Composer](https://getcomposer.org)로 설치한 의존성 패키지들이 위치합니다.

<a name="the-app-directory"></a>
## App 디렉터리 (The App Directory)

애플리케이션의 핵심 대부분은 `app` 디렉터리에 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 아래에 위치하며, Composer가 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)에 따라 자동 로딩합니다.

`app` 디렉터리 내부에는 `Console`, `Http`, `Providers` 등 여러 하위 디렉터리가 있습니다. `Console`과 `Http` 디렉터리는 애플리케이션 핵심에 대한 API 역할을 합니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 방식이지만, 실제 애플리케이션 로직을 포함하지는 않습니다. 즉, 이들은 애플리케이션에 명령을 내리는 두 가지 방법인 셈입니다. `Console`은 모든 Artisan 명령어를, `Http`는 컨트롤러, 미들웨어, 요청을 담고 있습니다.

`make` Artisan 명령으로 클래스를 생성할 때마다 `app` 디렉터리에 여러 다른 디렉터리들이 함께 생성됩니다. 예를 들어, `make:job` 명령어를 실행하기 전까지는 `app/Jobs` 디렉터리가 없습니다.

> [!NOTE]
> `app` 디렉터리 내 클래스 대부분은 Artisan 명령어로 생성할 수 있습니다. 사용 가능한 명령어 목록은 터미널에서 `php artisan list make` 명령어를 실행해 확인하세요.

<a name="the-broadcasting-directory"></a>
#### Broadcasting 디렉터리

`Broadcasting` 디렉터리는 애플리케이션의 방송 채널 클래스들을 포함합니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 기본적으로 이 디렉터리는 없지만, 첫 채널 생성 시 함께 만들어집니다. 채널에 관해 자세히 알고 싶다면 [이벤트 방송](/docs/9.x/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
#### Console 디렉터리

`Console` 디렉터리는 애플리케이션의 커스텀 Artisan 명령어가 위치합니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다. 이 디렉터리에는 또한 커스텀 Artisan 명령어 등록과 [스케줄된 작업들](/docs/9.x/scheduling)이 정의되는 콘솔 커널이 포함되어 있습니다.

<a name="the-events-directory"></a>
#### Events 디렉터리

기본적으로 이 디렉터리는 존재하지 않으나, `event:generate` 또는 `make:event` Artisan 명령어 실행 시 생성됩니다. `Events` 디렉터리는 [이벤트 클래스](/docs/9.x/events)를 포함하며, 이벤트는 애플리케이션 내 특정 작업이 발생했음을 다른 부분에 알리는데 사용되어 유연성과 결합도를 낮추는 효과가 있습니다.

<a name="the-exceptions-directory"></a>
#### Exceptions 디렉터리

`Exceptions` 디렉터리는 애플리케이션의 예외 처리기를 포함하며, 애플리케이션에서 던지는 예외 클래스도 위치시키기 적합한 곳입니다. 예외가 로그되거나 렌더링되는 방식을 커스터마이징하려면 이 디렉터리의 `Handler` 클래스를 수정하면 됩니다.

<a name="the-http-directory"></a>
#### Http 디렉터리

`Http` 디렉터리는 컨트롤러, 미들웨어, 폼 요청 클래스를 포함합니다. 애플리케이션으로 들어오는 요청을 처리하는 로직의 대부분이 이곳에 위치합니다.

<a name="the-jobs-directory"></a>
#### Jobs 디렉터리

기본적으로 존재하지 않지만, `make:job` Artisan 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리는 애플리케이션의 [큐 작업](/docs/9.x/queues)을 포함합니다. 작업은 큐에 넣어 비동기 실행하거나, 현재 요청 주기 내에서 동기적으로 실행할 수도 있습니다. 동기 실행되는 작업은 때때로 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현이라 하여 “커맨드”라고도 부릅니다.

<a name="the-listeners-directory"></a>
#### Listeners 디렉터리

기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` Artisan 명령어 실행 시 생성됩니다. `Listeners` 디렉터리는 [이벤트 리스너](/docs/9.x/events) 클래스를 포함합니다. 이벤트 리스너는 이벤트 인스턴스를 받아, 해당 이벤트가 발생했을 때 실행할 로직을 수행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너에 의해 처리될 수 있습니다.

<a name="the-mail-directory"></a>
#### Mail 디렉터리

기본적으로 존재하지 않지만, `make:mail` Artisan 명령어로 생성됩니다. `Mail` 디렉터리는 애플리케이션이 보내는 [메일을 표현하는 클래스들](/docs/9.x/mail)을 포함합니다. 메일 객체는 이메일 빌드 로직을 간단한 클래스 하나에 캡슐화하여 `Mail::send` 메서드로 전송할 수 있게 해줍니다.

<a name="the-models-directory"></a>
#### Models 디렉터리

`Models` 디렉터리는 모든 [Eloquent 모델 클래스](/docs/9.x/eloquent)를 포함합니다. Laravel의 Eloquent ORM은 데이터베이스 작업을 쉽고 우아하게 할 수 있는 ActiveRecord 구현체입니다. 각 데이터베이스 테이블에 대응하는 모델이 하나씩 있으며, 모델을 통해 데이터 조회와 새 레코드 삽입이 가능합니다.

<a name="the-notifications-directory"></a>
#### Notifications 디렉터리

기본적으로 없지만, `make:notification` Artisan 명령어를 실행하면 생성됩니다. `Notifications` 디렉터리는 애플리케이션에서 보내는 “트랜잭셔널” [알림](/docs/9.x/notifications)을 포함합니다. Laravel 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 통해 알림 전송을 추상화합니다.

<a name="the-policies-directory"></a>
#### Policies 디렉터리

기본적으로 존재하지 않지만, `make:policy` Artisan 명령어 실행 시 생성됩니다. `Policies` 디렉터리는 애플리케이션의 [인가 정책 클래스](/docs/9.x/authorization)를 포함합니다. 정책은 사용자가 리소스에 대해 특정 작업을 수행할 수 있는지 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
#### Providers 디렉터리

`Providers` 디렉터리는 애플리케이션의 모든 [서비스 프로바이더](/docs/9.x/providers)를 포함합니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록, 기타 요청 처리 준비 작업을 수행하여 애플리케이션을 부트스트랩합니다.

새로운 Laravel 애플리케이션에는 이미 여러 프로바이더가 포함되어 있습니다. 필요에 따라 직접 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
#### Rules 디렉터리

기본적으로 존재하지 않지만, `make:rule` Artisan 명령어로 생성됩니다. `Rules` 디렉터리는 애플리케이션의 커스텀 유효성 검증 규칙 객체를 포함합니다. 규칙 클래스는 복잡한 검증 로직을 간단한 객체 안에 캡슐화할 때 사용됩니다. 자세한 내용은 [유효성 검증 문서](/docs/9.x/validation)를 참고하세요.