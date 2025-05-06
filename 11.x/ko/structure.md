# 디렉터리 구조

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
## 소개

Laravel의 기본 어플리케이션 구조는 크든 작든 다양한 규모의 어플리케이션을 위한 훌륭한 출발점을 제공하도록 설계되어 있습니다. 하지만 여러분이 원하는 대로 어플리케이션을 구성할 자유가 있습니다. Laravel은 Composer가 클래스를 자동 로드할 수 있는 한, 클래스의 위치에 거의 제한을 두지 않습니다.

> [!NOTE]
> Laravel이 처음인가요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인해 실습을 따라 하며 첫 Laravel 어플리케이션을 만들어 보세요.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
### App 디렉터리

`app` 디렉터리는 어플리케이션의 핵심 코드를 담고 있습니다. 곧 이 디렉터리를 더 자세히 살펴보겠지만, 어플리케이션의 거의 모든 클래스가 이 디렉터리에 위치합니다.

<a name="the-bootstrap-directory"></a>
### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 있습니다. 이 디렉터리에는 성능 최적화를 위한 프레임워크 생성 파일(라우트 및 서비스 캐시 파일 등)을 담는 `cache` 디렉터리도 포함되어 있습니다.

<a name="the-config-directory"></a>
### Config 디렉터리

`config` 디렉터리는 이름에서 알 수 있듯이 어플리케이션의 모든 설정 파일을 담고 있습니다. 이 설정 파일들을 읽어보고 어떤 옵션들이 있는지 익혀두는 것이 좋습니다.

<a name="the-database-directory"></a>
### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 포함됩니다. 필요하다면 SQLite 데이터베이스 파일을 이 디렉터리에 둘 수도 있습니다.

<a name="the-public-directory"></a>
### Public 디렉터리

`public` 디렉터리는 어플리케이션으로 들어오는 모든 요청의 진입점인 `index.php` 파일이 들어 있습니다. 이 파일은 자동 로딩을 설정합니다. 또한 이 디렉터리에는 이미지, 자바스크립트, CSS 등과 같은 에셋이 위치합니다.

<a name="the-resources-directory"></a>
### Resources 디렉터리

`resources` 디렉터리에는 [뷰](/docs/{{version}}/views)와 CSS 또는 자바스크립트 등 컴파일되지 않은 원시 에셋들이 포함되어 있습니다.

<a name="the-routes-directory"></a>
### Routes 디렉터리

`routes` 디렉터리에는 어플리케이션의 모든 라우트 정의가 들어 있습니다. 기본적으로 Laravel에는 `web.php`와 `console.php`라는 두 개의 라우트 파일이 포함되어 있습니다.

`web.php` 파일에는 Laravel이 `web` 미들웨어 그룹에 넣는 라우트가 포함됩니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화 등을 제공합니다. 어플리케이션에 상태 없는 RESTful API가 없다면, 대부분의 라우트는 `web.php` 파일에 정의될 것입니다.

`console.php` 파일에서는 클로저 기반의 콘솔 명령들을 정의할 수 있습니다. 각 클로저는 명령 인스턴스에 바인딩되어 각 명령의 IO 메서드와 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 어플리케이션에 대한 콘솔 기반 진입점(라우트)을 정의합니다. 또한, `console.php` 파일에서 [작업 예약](/docs/{{version}}/scheduling)도 할 수 있습니다.

선택적으로, `install:api` 와 `install:broadcasting` Artisan 명령어를 사용해 API 라우트(`api.php`)나 브로드캐스팅 채널(`channels.php`)용 추가 라우트 파일도 설치할 수 있습니다.

`api.php` 파일에는 상태 없는 사용을 위한 라우트가 정의되어 있어서 이 경로로 들어오는 요청은 [토큰을 통해](/docs/{{version}}/sanctum) 인증되도록 설계되어 있으며, 세션 상태에는 접근하지 않습니다.

`channels.php` 파일은 어플리케이션이 지원하는 모든 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시 및 프레임워크에서 생성한 기타 파일이 담깁니다. 이 디렉터리는 `app`, `framework`, `logs` 하위 디렉터리로 구분됩니다. `app` 디렉터리는 어플리케이션에서 생성하는 파일을 저장할 수 있습니다. `framework` 디렉터리는 프레임워크에서 생성하는 각종 파일 또는 캐시가 저장됩니다. 마지막으로 `logs` 디렉터리에는 어플리케이션의 로그 파일들이 위치하게 됩니다.

`storage/app/public` 디렉터리는 프로필 이미지 등 공개적으로 접근이 가능한 사용자가 생성한 파일을 저장하는 데 사용할 수 있습니다. 이 디렉터리와 연결되는 심볼릭 링크를 `public/storage` 경로에 만들어야 하며, `php artisan storage:link` Artisan 명령어로 생성할 수 있습니다.

<a name="the-tests-directory"></a>
### Tests 디렉터리

`tests` 디렉터리는 자동화 테스트를 위해 사용됩니다. 기본적으로 [Pest](https://pestphp.com)나 [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트 예제가 제공됩니다. 각 테스트 클래스 이름 끝에는 반드시 `Test`라는 접미사를 붙여야 합니다. 테스트는 `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 실행할 수 있습니다. 테스트 결과를 더 상세하고 보기 좋게 출력하려면 `php artisan test` Artisan 명령어로 실행할 수도 있습니다.

<a name="the-vendor-directory"></a>
### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 패키지 의존성들이 담겨 있습니다.

<a name="the-app-directory"></a>
## App 디렉터리

어플리케이션의 대부분은 `app` 디렉터리에 들어 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 아래에 위치하며, [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)에 따라 Composer에 의해 자동 로드됩니다.

기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 디렉터리가 포함되어 있습니다. 그러나 Artisan의 make 명령어를 이용하여 클래스를 생성하게 되면 이 디렉터리 안에 여러 추가 디렉터리들이 만들어지게 됩니다. 예를 들어, `app/Console` 디렉터리는 `make:command` Artisan 명령어로 커맨드 클래스를 생성할 때에만 생깁니다.

`Console`과 `Http` 디렉터리에 관해서는 아래 섹션에서 좀 더 자세히 설명합니다. 간단히 말해, 이 두 디렉터리는 어플리케이션의 코어로 명령을 전달하는 API와 같다고 볼 수 있습니다. HTTP 프로토콜과 CLI는 각각 어플리케이션과 상호작용하는 방식이지만 실제 비즈니스 로직을 담지는 않습니다. 즉, 어플리케이션에 대한 명령을 내리는 두 가지 방법입니다. `Console` 디렉터리에는 모든 Artisan 명령이, `Http` 디렉터리에는 컨트롤러, 미들웨어, 요청 클래스가 위치합니다.

> [!NOTE]
> `app` 디렉터리의 많은 클래스들은 Artisan 명령으로 생성 가능합니다. 사용 가능한 명령을 확인하려면 터미널에서 `php artisan list make`를 실행하세요.

<a name="the-broadcasting-directory"></a>
### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 어플리케이션의 브로드캐스트 채널 클래스들이 들어 있습니다. 이 클래스들은 `make:channel` 명령어로 생성할 수 있습니다. 이 디렉터리는 기본적으로 존재하지 않지만 첫 채널을 만들 때 자동으로 생성됩니다. 자세한 내용은 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### Console 디렉터리

`Console` 디렉터리에는 어플리케이션의 커스텀 Artisan 명령들이 포함됩니다. 이 명령들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` Artisan 명령으로 생성됩니다. `Events` 디렉터리는 [이벤트 클래스](/docs/{{version}}/events)를 저장합니다. 이벤트를 사용하면 특정 동작이 발생했을 때 어플리케이션의 다른 부분에 알릴 수 있어 유연성과 결합도를 낮출 수 있습니다.

<a name="the-exceptions-directory"></a>
### Exceptions 디렉터리

`Exceptions` 디렉터리에는 어플리케이션의 커스텀 예외 클래스들이 들어 있습니다. 이 예외들은 `make:exception` 명령어로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청 클래스가 포함됩니다. 어플리케이션으로 들어오는 요청을 처리하는 대부분의 로직은 이 디렉터리에 작성하게 됩니다.

<a name="the-jobs-directory"></a>
### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:job` Artisan 명령어 실행 시 생성됩니다. `Jobs` 디렉터리에는 어플리케이션의 [큐 작업 클래스](/docs/{{version}}/queues)가 저장됩니다. 작업은 큐에 넣거나, 현재 요청의 생애 주기 내에서 동기적으로 실행될 수 있습니다. 동기적으로 실행되는 작업은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현체이기에 종종 "명령"이라 불리기도 합니다.

<a name="the-listeners-directory"></a>
### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` Artisan 명령을 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/{{version}}/events)를 처리하는 클래스가 들어 있습니다. 이벤트 리스너는 이벤트 인스턴스를 받아서 해당 이벤트가 발생했을 때 로직을 실행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` Artisan 명령을 실행하면 생성됩니다. `Mail` 디렉터리에는 어플리케이션에서 발송하는 [이메일 클래스](/docs/{{version}}/mail)가 모두 담겨 있습니다. 이 객체는 이메일 작성 로직을 한 클래스에 모두 캡슐화할 수 있으며, `Mail::send` 메소드를 통해 발송할 수 있습니다.

<a name="the-models-directory"></a>
### Models 디렉터리

`Models` 디렉터리에는 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)가 모두 저장됩니다. Laravel의 Eloquent ORM은 데이터베이스와 손쉽게 작업할 수 있는 ActiveRecord 구현을 제공합니다. 데이터베이스의 각 테이블에는 해당 테이블과 연결된 "모델"이 존재하며, 이를 통해 데이터를 조회하거나 새 레코드를 추가할 수 있습니다.

<a name="the-notifications-directory"></a>
### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` Artisan 명령을 실행하면 생성됩니다. `Notifications` 디렉터리에는 어플리케이션에서 발송하는 "트랜잭션성" [알림](/docs/{{version}}/notifications)이 모두 들어 있습니다. Laravel의 알림 기능은 이메일, 슬랙, SMS, 데이터베이스 등에 알림을 보낼 수 있도록 다양한 드라이버를 추상화하여 제공합니다.

<a name="the-policies-directory"></a>
### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` Artisan 명령을 실행하면 생성됩니다. `Policies` 디렉터리에는 어플리케이션의 [인증 정책 클래스](/docs/{{version}}/authorization)가 들어 있습니다. 정책은 사용자가 특정 리소스에 대해 작업을 수행할 수 있는지 여부를 결정하는 데 사용됩니다.

<a name="the-providers-directory"></a>
### Providers 디렉터리

`Providers` 디렉터리에는 어플리케이션의 모든 [서비스 프로바이더](/docs/{{version}}/providers)가 들어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하거나, 이벤트를 등록하거나, 기타 여러 작업을 수행하여 어플리케이션을 초기화합니다.

새로운 Laravel 어플리케이션에는 이 디렉터리에 이미 `AppServiceProvider`가 포함되어 있습니다. 필요하다면 이 디렉터리에 직접 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` Artisan 명령을 실행하면 생성됩니다. `Rules` 디렉터리에는 어플리케이션의 커스텀 유효성 검사 규칙 객체가 들어 있습니다. 규칙 객체는 복잡한 유효성 검사 로직을 하나의 객체로 캡슐화할 수 있습니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.