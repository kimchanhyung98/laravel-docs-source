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

기본 Laravel 애플리케이션 구조는 대규모 및 소규모 애플리케이션 모두에 훌륭한 출발점을 제공하도록 설계되었습니다. 하지만 애플리케이션을 원하는 방식으로 자유롭게 구성할 수 있습니다. Laravel은 클래스가 어디에 위치하든 거의 제한을 두지 않습니다. Composer가 해당 클래스를 자동 로드할 수 있기만 하면 됩니다.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
### App 디렉터리

`app` 디렉터리는 애플리케이션의 핵심 코드를 포함합니다. 이 디렉터리에 대해 곧 더 자세히 살펴보도록 하겠습니다. 대부분의 애플리케이션 클래스는 이 디렉터리에 위치하게 됩니다.

<a name="the-bootstrap-directory"></a>
### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 포함되어 있습니다. 또한 이 디렉터리에는 라우트 및 서비스 캐시 파일과 같은 성능 최적화를 위한 프레임워크 생성 파일이 저장되는 `cache` 디렉터리도 포함됩니다.

<a name="the-config-directory"></a>
### Config 디렉터리

`config` 디렉터리에는 이름에서 알 수 있듯이 애플리케이션의 모든 설정 파일이 들어 있습니다. 모든 옵션을 숙지하고 활용할 수 있도록 이 파일들을 꼼꼼히 읽어보는 것이 좋습니다.

<a name="the-database-directory"></a>
### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 포함되어 있습니다. 원한다면 이 디렉터리에 SQLite 데이터베이스 파일도 보관할 수 있습니다.

<a name="the-public-directory"></a>
### Public 디렉터리

`public` 디렉터리에는 모든 요청이 들어오는 애플리케이션의 진입점인 `index.php` 파일이 위치하며, 오토로딩을 설정합니다. 또한 이미지, JavaScript, CSS 같은 에셋 파일도 이곳에 보관합니다.

<a name="the-resources-directory"></a>
### Resources 디렉터리

`resources` 디렉터리에는 [뷰 파일](/docs/{{version}}/views)과 CSS·JavaScript 등 컴파일되지 않은 원본 에셋이 들어 있습니다.

<a name="the-routes-directory"></a>
### Routes 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 포함되어 있습니다. 기본적으로 Laravel에는 `web.php`와 `console.php` 두 개의 라우트 파일이 제공됩니다.

`web.php` 파일에는 Laravel이 `web` 미들웨어 그룹에 넣는 라우트가 정의되어 있습니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 애플리케이션이 상태 비저장 RESTful API를 제공하지 않는다면, 대부분의 라우트는 `web.php`에 정의하게 됩니다.

`console.php` 파일에서는 클로저 기반 콘솔 명령을 정의할 수 있습니다. 각각의 클로저는 명령 인스턴스에 바인딩되어, 각 명령의 IO 메서드와 쉽게 상호 작용할 수 있습니다. 이 파일이 HTTP 라우트를 정의하진 않지만, 콘솔 기반 진입점(라우트)을 정의합니다. 또한 `console.php` 파일에서 [스케줄링](/docs/{{version}}/scheduling)도 할 수 있습니다.

필요에 따라 `install:api` 및 `install:broadcasting` Artisan 명령어를 통해 API 라우트(`api.php`)와 브로드캐스팅 채널(`channels.php`)을 위한 추가 라우트 파일을 설치할 수 있습니다.

`api.php` 파일에는 상태 비저장을 전제로 한 라우트가 정의됩니다. 이 라우트를 통해 애플리케이션에 진입하는 요청은 [토큰](/docs/{{version}}/sanctum)을 통해 인증되며, 세션 상태에는 접근하지 않습니다.

`channels.php` 파일은 애플리케이션에서 지원하는 모든 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 프레임워크가 생성하는 기타 파일이 저장됩니다. 이 디렉터리는 `app`, `framework`, `logs`로 구분됩니다. `app` 디렉터리는 애플리케이션에서 생성한 파일을 저장하는 데 사용할 수 있습니다. `framework` 디렉터리는 프레임워크에서 생성한 파일과 캐시를 저장합니다. 마지막으로 `logs` 디렉터리엔 애플리케이션의 로그 파일이 들어 있습니다.

`storage/app/public` 디렉터리는 프로필 아바타 등 공개적으로 접근 가능한 사용자 생성 파일을 저장하는 데 사용할 수 있습니다. 이 디렉터리에 연결된 심볼릭 링크를 `public/storage`에 생성해야 하며, 이 링크는 `php artisan storage:link` 명령어로 만들 수 있습니다.

<a name="the-tests-directory"></a>
### Tests 디렉터리

`tests` 디렉터리에는 자동화된 테스트가 저장됩니다. 예시로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de/)의 단위 테스트 및 기능 테스트가 기본 제공됩니다. 각 테스트 클래스 이름 끝에는 `Test`가 붙어야 합니다. `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령으로 테스트를 실행할 수 있습니다. 테스트 결과를 더 자세하고 아름답게 확인하려면 `php artisan test` 명령을 사용할 수도 있습니다.

<a name="the-vendor-directory"></a>
### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 패키지 의존성이 저장됩니다.

<a name="the-app-directory"></a>
## App 디렉터리

애플리케이션의 대부분은 `app` 디렉터리에 위치합니다. 기본적으로 이 디렉터리는 `App` 네임스페이스가 적용되어 있으며, [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/)을 사용해 Composer가 자동 로드합니다.

기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 세 디렉터리가 포함되어 있습니다. 그러나 Artisan 명령어를 사용해 클래스를 생성하다 보면 다양한 하위 디렉터리가 생성됩니다. 예를 들어 `make:command` 명령을 통해 명령 클래스를 생성하기 전에는 `app/Console` 디렉터리가 존재하지 않습니다.

`Console` 및 `Http` 디렉터리에 대해서는 아래에서 더 자세히 설명하지만, 이 두 디렉터리는 애플리케이션의 핵심에 대한 API 역할을 한다고 볼 수 있습니다. HTTP 프로토콜과 CLI 모두 애플리케이션과 상호작용하는 수단일 뿐, 실제 비즈니스 로직을 담고 있진 않습니다. 즉, 둘 다 애플리케이션에 명령을 내리는 방식입니다. `Console` 디렉터리는 모든 Artisan 명령을, `Http` 디렉터리는 컨트롤러, 미들웨어, 요청(Requests)을 포함합니다.

> [!NOTE]
> `app` 디렉터리의 많은 클래스는 Artisan 명령어로 생성할 수 있습니다. 사용 가능한 명령을 확인하려면 터미널에서 `php artisan list make`를 실행하세요.

<a name="the-broadcasting-directory"></a>
### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 애플리케이션의 브로드캐스트 채널 클래스가 모두 저장됩니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 이 디렉터리는 기본적으로 존재하지 않으며, 첫 채널을 만드는 순간 생성됩니다. 채널에 대해 더 알고 싶다면 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 커스텀 Artisan 명령어가 모두 들어 있습니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `event:generate` 또는 `make:event` Artisan 명령어를 실행하면 생성됩니다. `Events` 디렉터리에는 [이벤트 클래스](/docs/{{version}}/events)가 저장됩니다. 이벤트는 특정 동작이 발생했을 때 애플리케이션의 다른 부분에 알람을 보내는 용도로 사용되며, 높은 유연성과 코드의 결합도를 낮추는 데 도움이 됩니다.

<a name="the-exceptions-directory"></a>
### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 커스텀 예외 클래스가 저장됩니다. 이 예외 클래스들은 `make:exception` 명령으로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청 클래스가 들어 있습니다. 외부로부터 들어오는 요청을 처리하는 거의 모든 로직은 이 디렉터리에 위치합니다.

<a name="the-jobs-directory"></a>
### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:job` Artisan 명령을 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션의 [큐잉 가능한 작업](/docs/{{version}}/queues)이 들어 있습니다. 작업(Job)은 큐잉되어 나중에 실행될 수도 있고, 현재 요청 라이프사이클 내에서 동기적으로 즉시 실행될 수도 있습니다. 현재 요청에서 동기적으로 실행되는 작업은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)을 구현하므로 때때로 "커맨드"라고도 부릅니다.

<a name="the-listeners-directory"></a>
### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `event:generate` 또는 `make:listener` Artisan 명령을 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/{{version}}/events)를 처리하는 클래스들이 들어 있습니다. 이벤트 리스너는 이벤트 인스턴스를 받아, 해당 이벤트 발생에 대한 동작을 수행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너에서 처리될 수 있습니다.

<a name="the-mail-directory"></a>
### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:mail` Artisan 명령을 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 발송되는 [이메일을 나타내는 클래스](/docs/{{version}}/mail)가 모두 저장됩니다. 메일 객체는 이메일 작성에 필요한 모든 로직을 하나의 간단한 클래스로 캡슐화할 수 있도록 하며, `Mail::send` 메서드로 메일을 보낼 수 있습니다.

<a name="the-models-directory"></a>
### Models 디렉터리

`Models` 디렉터리에는 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)가 모두 들어 있습니다. Laravel에 포함된 Eloquent ORM은 데이터베이스와 상호작용하기 위한 우아하고 단순한 액티브 레코드(ActiveRecord) 구현체를 제공합니다. 각 데이터베이스 테이블에는 하나의 "모델"이 대응되어 테이블과의 상호작용을 담당합니다. 모델을 통해 테이블에서 데이터를 쿼리하거나, 새로운 레코드를 추가할 수 있습니다.

<a name="the-notifications-directory"></a>
### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:notification` Artisan 명령을 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 전송하는 모든 "트랜잭션성" [알림](/docs/{{version}}/notifications) 클래스가 들어 있습니다(예: 애플리케이션 내에서 발생한 이벤트 알림 등). Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 추상화합니다.

<a name="the-policies-directory"></a>
### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:policy` Artisan 명령을 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [인가 정책 클래스](/docs/{{version}}/authorization)가 담깁니다. 정책은 사용자가 특정 리소스에 대해 어떤 동작을 할 수 있는지 판단하는 데 사용됩니다.

<a name="the-providers-directory"></a>
### Providers 디렉터리

`Providers` 디렉터리에는 애플리케이션의 모든 [서비스 프로바이더](/docs/{{version}}/providers)가 포함되어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록 등, 애플리케이션을 요청 전 처리하는 여러 작업을 담당합니다.

초기 Laravel 애플리케이션에는 이미 `AppServiceProvider`가 포함되어 있습니다. 필요에 따라 이 디렉터리에 자신의 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:rule` Artisan 명령을 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션에서 사용하는 커스텀 유효성 검사 규칙 객체가 담깁니다. 규칙 객체는 복잡한 유효성 검사 로직을 간단한 객체로 캡슐화하는 데 사용됩니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.