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

기본적으로 제공되는 Laravel 애플리케이션 구조는 대규모와 소규모 애플리케이션 모두에 훌륭한 출발점을 제공합니다. 하지만 애플리케이션 구조는 자유롭게 조직할 수 있습니다. Laravel은 클래스가 반드시 특정 위치에 있어야 한다는 제약을 두지 않습니다. Composer가 클래스를 오토로딩할 수만 있다면 어디든 둘 수 있습니다.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
### App 디렉터리

`app` 디렉터리는 애플리케이션의 핵심 코드를 포함합니다. 곧 이 디렉터리를 더 자세히 알아보겠지만, 애플리케이션의 거의 모든 클래스는 이 디렉터리에 위치합니다.

<a name="the-bootstrap-directory"></a>
### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 있습니다. 또한 이 디렉터리에는 프레임워크가 생성한 파일(예: 라우트 캐시, 서비스 캐시 파일 등)을 위한 `cache` 디렉터리도 포함되어 있습니다. 이 파일들은 성능 최적화를 위해 사용됩니다.

<a name="the-config-directory"></a>
### Config 디렉터리

이름에서 알 수 있듯이, `config` 디렉터리에는 애플리케이션의 모든 설정 파일이 들어있습니다. 이 파일들을 읽고 사용 가능한 옵션들을 숙지하는 것이 좋습니다.

<a name="the-database-directory"></a>
### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시더가 포함되어 있습니다. 원한다면 SQLite 데이터베이스 파일도 이 디렉터리에 둘 수 있습니다.

<a name="the-public-directory"></a>
### Public 디렉터리

`public` 디렉터리에는 모든 요청이 진입하며 오토로딩을 설정하는 진입점 파일인 `index.php`가 있습니다. 또한 이미지, JavaScript, CSS와 같은 자산 파일들도 이 디렉터리에 위치합니다.

<a name="the-resources-directory"></a>
### Resources 디렉터리

`resources` 디렉터리에는 [뷰](/docs/{{version}}/views)와 CSS 또는 JavaScript와 같은 원시(컴파일되지 않은) 자산들이 포함되어 있습니다.

<a name="the-routes-directory"></a>
### Routes 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 들어있습니다. 기본적으로 Laravel에는 `web.php`와 `console.php` 두 개의 라우트 파일이 포함되어 있습니다.

`web.php` 파일에는 Laravel이 `web` 미들웨어 그룹에 포함시키는 라우트가 정의되며, 세션 상태, CSRF 보호, 쿠키 암호화 등이 제공됩니다. 만약 애플리케이션이 stateless한 RESTful API가 아니라면 대부분의 라우트는 `web.php`에 정의됩니다.

`console.php` 파일에는 클로저 기반의 콘솔 커맨드를 정의할 수 있습니다. 각 클로저는 커맨드 인스턴스에 바인딩되어 있어, 각 커맨드의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하진 않지만, 콘솔 진입점(라우트)을 정의합니다. `console.php` 파일에서는 [작업 스케줄링](/docs/{{version}}/scheduling)도 할 수 있습니다.

또한 Artisan의 `install:api`, `install:broadcasting` 명령을 통해 API 라우트(`api.php`), 브로드캐스팅 채널(`channels.php`)용 추가 라우트 파일을 설치할 수 있습니다.

`api.php` 파일에는 stateless 요청을 위한 라우트가 포함되며, 이 경로를 통해 들어오는 요청은 [토큰을 통한 인증](/docs/{{version}}/sanctum)이 필요하고 세션 상태에는 접근할 수 없습니다.

`channels.php` 파일은 애플리케이션에서 지원하는 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 프레임워크에서 생성된 기타 파일이 포함되어 있습니다. 이 디렉터리는 `app`, `framework`, `logs`로 분리됩니다. `app` 디렉터리는 애플리케이션에서 생성한 파일을 저장하는 데 사용할 수 있습니다. `framework` 디렉터리는 프레임워크가 생성하는 파일과 캐시를 저장합니다. 마지막으로 `logs` 디렉터리에는 애플리케이션의 로그 파일이 위치합니다.

`storage/app/public` 디렉터리는 프로필 아바타와 같이 사용자가 생성한 파일을 공개적으로 제공해야 할 때 사용할 수 있습니다. 이 디렉터리에 연결되는 심볼릭 링크를 `public/storage`에 만들어야 합니다. 이 링크는 `php artisan storage:link` Artisan 명령으로 생성할 수 있습니다.

<a name="the-tests-directory"></a>
### Tests 디렉터리

`tests` 디렉터리에는 자동화된 테스트가 들어있습니다. 기본으로 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트가 제공됩니다. 각 테스트 클래스의 이름은 `Test`로 끝나야 합니다. `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령어로 테스트를 실행할 수 있습니다. 더 상세하고 아름다운 결과를 원할 경우 `php artisan test` 명령을 사용할 수도 있습니다.

<a name="the-vendor-directory"></a>
### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 의존성이 저장됩니다.

<a name="the-app-directory"></a>
## App 디렉터리

애플리케이션의 주요 부분은 `app` 디렉터리에 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스를 사용하며, [PSR-4 오토로딩 표준](https://www.php-fig.org/psr/psr-4/)에 따라 Composer로 오토로딩됩니다.

기본적으로 `app` 디렉터리에는 `Http`, `Models`, `Providers` 디렉터리가 포함되어 있습니다. 그러나 시간이 지나면서 Artisan의 make 명령을 사용해 클래스를 생성할 때 다양한 하위 디렉터리가 추가됩니다. 예를 들어, `make:command` 명령을 실행하기 전까진 `app/Console` 디렉터리가 존재하지 않습니다.

`Console`과 `Http` 디렉터리는 아래 별도의 섹션에서 더 자세히 설명하지만, 두 디렉터리는 코어 애플리케이션에 접근할 수 있는 API를 제공한다고 생각하면 됩니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 수단일 뿐, 실제 비즈니스 로직이 포함되어 있는 것은 아닙니다. 즉, 두 가지 방식 모두 애플리케이션에 명령을 전달하는 수단입니다. `Console` 디렉터리에는 모든 Artisan 명령이, `Http` 디렉터리에는 컨트롤러, 미들웨어, 요청 객체가 위치합니다.

> [!NOTE]
> `app` 디렉터리의 많은 클래스들은 Artisan 명령으로 생성할 수 있습니다. 사용 가능한 명령 목록을 확인하려면 터미널에서 `php artisan list make` 명령을 실행하세요.

<a name="the-broadcasting-directory"></a>
### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 모든 브로드캐스팅 채널 클래스가 포함됩니다. 이 클래스들은 `make:channel` 명령으로 생성합니다. 이 디렉터리는 기본적으로 존재하지 않지만 첫 채널을 생성할 때 만들어집니다. 채널에 대해 더 알아보려면 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 사용자 정의 Artisan 명령이 포함됩니다. 이 명령들은 `make:command` 명령으로 생성할 수 있습니다.

<a name="the-events-directory"></a>
### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` Artisan 명령어로 생성할 수 있습니다. `Events` 디렉터리에는 [이벤트 클래스](/docs/{{version}}/events)가 보관됩니다. 이벤트는 특정 동작이 발생했을 때 애플리케이션의 다른 부분에 알리는 용도로 유용하며, 높은 유연성과 분리를 제공합니다.

<a name="the-exceptions-directory"></a>
### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 사용자 정의 예외 클래스가 포함됩니다. 이 예외들은 `make:exception` 명령으로 생성할 수 있습니다.

<a name="the-http-directory"></a>
### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청 객체가 포함됩니다. 외부에서 들어오는 요청을 처리하는 로직의 대부분이 이 디렉터리에 위치하게 됩니다.

<a name="the-jobs-directory"></a>
### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:job` Artisan 명령을 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션의 [큐 처리 가능한 작업](/docs/{{version}}/queues)이 포함됩니다. 작업(Job)은 큐에 저장되거나 현재 요청 라이프사이클 내에서 동기적으로 실행될 수 있습니다. 동기적으로 실행되는 작업은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현이기 때문에 "커맨드"라 부르기도 합니다.

<a name="the-listeners-directory"></a>
### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` Artisan 명령을 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/{{version}}/events)를 처리하는 클래스들이 담깁니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생 시 로직을 실행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너에 의해 처리될 수 있습니다.

<a name="the-mail-directory"></a>
### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` Artisan 명령을 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 전송하는 [메일을 표현하는 클래스](/docs/{{version}}/mail)가 들어있습니다. 메일 객체는 이메일 생성 로직을 하나의 간단한 클래스로 캡슐화할 수 있으며, `Mail::send` 메서드로 전송할 수 있습니다.

<a name="the-models-directory"></a>
### Models 디렉터리

`Models` 디렉터리에는 모든 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)가 들어 있습니다. Laravel의 Eloquent ORM은 데이터베이스와 상호작용할 수 있는 쉽고 아름다운 액티브레코드 구현을 제공합니다. 각 데이터베이스 테이블은 대응하는 "모델"이 있으며, 이를 통해 테이블의 데이터를 조회하거나 새로운 레코드를 삽입할 수 있습니다.

<a name="the-notifications-directory"></a>
### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` Artisan 명령을 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 전송되는 ["트랜잭션 알림"](/docs/{{version}}/notifications)이 들어있습니다. 예를 들어 애플리케이션 내 이벤트 발생 시의 간단한 알림 등을 이곳에서 관리합니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버로의 전송을 추상화합니다.

<a name="the-policies-directory"></a>
### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` Artisan 명령을 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [권한 정책 클래스](/docs/{{version}}/authorization)가 들어 있습니다. 정책은 사용자가 리소스에 대해 특정 작업을 수행할 수 있는지 여부를 결정하는 데 사용됩니다.

<a name="the-providers-directory"></a>
### Providers 디렉터리

`Providers` 디렉터리에는 [서비스 프로바이더](/docs/{{version}}/providers)가 모두 포함되어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하거나, 이벤트를 등록하거나, 요청을 받기 위한 기타 준비 작업 등 애플리케이션을 부트스트랩합니다.

새로운 Laravel 애플리케이션에는 이미 `AppServiceProvider`가 들어 있습니다. 필요에 따라 이 디렉터리에 자유롭게 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` Artisan 명령을 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션의 사용자 정의 유효성 검사 규칙 객체가 포함됩니다. 규칙 객체는 복잡한 유효성 검사 로직을 간단한 객체로 캡슐화합니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.