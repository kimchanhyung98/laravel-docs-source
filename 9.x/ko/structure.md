# 디렉터리 구조

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
## 소개

Laravel의 기본 애플리케이션 구조는 대규모와 소규모 애플리케이션 모두에 적합한 출발점을 제공합니다. 하지만 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 클래스가 어디에 위치하는지에 대해 거의 제한을 두지 않습니다. 단, Composer가 해당 클래스를 자동으로 로드할 수 있기만 하면 됩니다.

> **참고**
> Laravel이 처음이신가요? [Laravel 부트캠프](https://bootcamp.laravel.com)에서 프레임워크를 직접 체험하며 첫 Laravel 애플리케이션을 만들어 보세요.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
#### App 디렉터리

`app` 디렉터리에는 애플리케이션의 핵심 코드가 포함되어 있습니다. 이 디렉터리에 대해서는 곧 더 자세히 살펴보겠지만, 여러분의 애플리케이션 내 대부분의 클래스가 이곳에 위치하게 됩니다.

<a name="the-bootstrap-directory"></a>
#### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 있습니다. 이 디렉터리 안에는 성능 최적화를 위한 프레임워크 생성 파일(예: 라우트 및 서비스 캐시 파일 등)이 포함된 `cache` 디렉터리도 있습니다. 일반적으로 이 디렉터리 내의 파일을 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
#### Config 디렉터리

`config` 디렉터리는 이름에서 알 수 있듯이 애플리케이션의 모든 설정 파일을 포함하고 있습니다. 이 파일들을 모두 읽어보며 제공되는 다양한 옵션에 익숙해지는 것이 좋습니다.

<a name="the-database-directory"></a>
#### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드가 들어 있습니다. 필요하다면 이 디렉터리를 SQLite 데이터베이스 파일을 저장하는 용도로도 사용할 수 있습니다.

<a name="the-lang-directory"></a>
#### Lang 디렉터리

`lang` 디렉터리에는 애플리케이션의 모든 언어 파일이 들어 있습니다.

<a name="the-public-directory"></a>
#### Public 디렉터리

`public` 디렉터리에는 모든 요청이 애플리케이션에 진입하는 진입점인 `index.php` 파일이 있으며, 자동 로딩 구성을 담당합니다. 또한 이미지, JavaScript, CSS와 같은 에셋 파일도 이곳에 저장됩니다.

<a name="the-resources-directory"></a>
#### Resources 디렉터리

`resources` 디렉터리에는 [뷰](/docs/{{version}}/views) 및 컴파일되지 않은 원본 에셋(예: CSS, JavaScript 등)이 포함되어 있습니다.

<a name="the-routes-directory"></a>
#### Routes 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 들어 있습니다. Laravel은 기본적으로 `web.php`, `api.php`, `console.php`, `channels.php` 등 여러 라우트 파일을 제공합니다.

`web.php` 파일에는 `RouteServiceProvider`가 `web` 미들웨어 그룹에 배치하는 라우트가 포함되어 있습니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 만약 애플리케이션이 상태 비저장(stateless) RESTful API를 제공하지 않는다면, 모든 라우트가 대부분 `web.php`에 정의될 것입니다.

`api.php` 파일에는 `RouteServiceProvider`가 `api` 미들웨어 그룹에 배치하는 라우트가 정의되어 있습니다. 이 라우트들은 상태 비저장을 의도하므로, 토큰 기반 인증을 통해 요청이 들어오며 세션 상태에는 접근할 수 없습니다.

`console.php` 파일에서는 클로저 기반 콘솔 명령어를 정의할 수 있습니다. 각 클로저는 명령어 인스턴스에 바인딩되어 있어 각 명령어의 입출력(IO) 메서드에 쉽게 접근할 수 있습니다. 이 파일은 HTTP 라우트는 정의하지 않지만, 애플리케이션에 대한 콘솔 기반 진입점(라우트)을 정의합니다.

`channels.php` 파일에서는 애플리케이션에서 지원하는 모든 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록할 수 있습니다.

<a name="the-storage-directory"></a>
#### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 Blade 템플릿, 파일 기반 세션, 파일 캐시, 그리고 프레임워크가 생성한 기타 파일이 저장됩니다. 이 디렉터리는 `app`, `framework`, `logs`의 하위 디렉터리로 구분되어 있습니다.  
- `app` 디렉터리는 애플리케이션에서 생성한 파일들을 저장하는 용도입니다.
- `framework` 디렉터리는 프레임워크가 생성한 파일과 캐시를 저장합니다.
- `logs` 디렉터리는 애플리케이션의 로그 파일을 포함합니다.

`storage/app/public` 디렉터리는 프로필 아바타와 같이 공개적으로 접근 가능해야 하는 사용자 생성 파일을 저장하는 용도로 사용할 수 있습니다. `public/storage`에 심볼릭 링크를 만들어 이 디렉터리를 가리키게 해야 합니다. `php artisan storage:link` 아티즌(Artisan) 명령어로 링크를 생성할 수 있습니다.

<a name="the-tests-directory"></a>
#### Tests 디렉터리

`tests` 디렉터리에는 자동화된 테스트가 포함되어 있습니다. 예시 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트가 기본 제공됩니다. 각 테스트 클래스의 이름은 `Test`로 끝나야 합니다. `phpunit` 또는 `php vendor/bin/phpunit` 명령어로 테스트를 실행할 수 있습니다. 더 자세하고 보기 좋은 테스트 결과를 원한다면, `php artisan test` 아티즌 명령어로 실행할 수도 있습니다.

<a name="the-vendor-directory"></a>
#### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 의존성이 포함되어 있습니다.

<a name="the-app-directory"></a>
## App 디렉터리

애플리케이션의 대부분의 코드는 `app` 디렉터리에 위치합니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 아래에 있으며 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/) 을 사용해 Composer에 의해 자동 로드됩니다.

`app` 디렉터리에는 `Console`, `Http`, `Providers` 등 다양한 하위 디렉터리가 포함될 수 있습니다. `Console` 및 `Http` 디렉터리는 애플리케이션의 코어에 진입하는 API 역할을 합니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 방식에 불과하며, 실제 비즈니스 로직은 포함하지 않습니다. 즉, 애플리케이션에 명령을 내리는 두 가지 방법입니다.  
- `Console` 디렉터리는 모든 아티즌(Artisan) 명령어를 포함합니다.
- `Http` 디렉터리는 컨트롤러, 미들웨어, 요청(Request) 클래스를 포함합니다.

또한, 클래스 생성을 위한 `make` 아티즌 명령어를 사용하다 보면 다양한 디렉터리가 추가 생성될 수 있습니다. 예를 들어, `make:job` 명령어로 작업 클래스를 생성하기 전까지는 `app/Jobs` 디렉터리가 존재하지 않습니다.

> **참고**  
> `app` 디렉터리 내의 많은 클래스들은 아티즌 명령어를 통해 생성할 수 있습니다. 사용 가능한 명령어 목록을 확인하려면, 터미널에서 `php artisan list make` 명령어를 실행하세요.

<a name="the-broadcasting-directory"></a>
#### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 애플리케이션의 모든 브로드캐스트 채널 클래스가 포함됩니다. 이 클래스들은 `make:channel` 명령어로 생성할 수 있습니다. 이 디렉터리는 기본적으로 존재하지 않지만, 첫 채널을 만들 때 자동으로 생성됩니다. 채널에 대한 자세한 내용은 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
#### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 모든 커스텀 아티즌(Artisan) 명령어가 포함되어 있습니다. 이 명령어들은 `make:command` 명령어로 생성할 수 있습니다. 또한 이 디렉터리에는 콘솔 커널이 위치하며, 커스텀 아티즌 명령어의 등록 및 [스케줄링된 작업](/docs/{{version}}/scheduling) 정의를 담당합니다.

<a name="the-events-directory"></a>
#### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` 아티즌 명령어를 실행하면 생성됩니다. `Events` 디렉터리에는 [이벤트 클래스](/docs/{{version}}/events)가 포함됩니다. 이벤트는 특정 동작이 발생했음을 애플리케이션의 다른 부분에 알리는 용도로 사용되어, 유연성과 결합도를 낮추는 데 도움이 됩니다.

<a name="the-exceptions-directory"></a>
#### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 예외 처리기가 포함되어 있으며, 애플리케이션에서 발생하는 예외를 보관하기에도 적합한 위치입니다. 예외의 로깅이나 렌더링 방식을 커스터마이징하려면 이 디렉터리의 `Handler` 클래스를 수정하면 됩니다.

<a name="the-http-directory"></a>
#### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청 클래스가 포함됩니다. 애플리케이션으로 들어오는 요청을 처리하는 거의 모든 로직이 이곳에 위치하게 됩니다.

<a name="the-jobs-directory"></a>
#### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:job` 아티즌 명령어를 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션의 [큐 작업 클래스](/docs/{{version}}/queues)가 포함됩니다. 작업(Job)은 큐에 넣어 비동기적으로 처리하거나, 현재 요청의 라이프사이클 내에서 동기적으로 실행될 수 있습니다. 이러한 동기 실행 작업은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현체로 "커맨드"라고 부르기도 합니다.

<a name="the-listeners-directory"></a>
#### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:listener` 아티즌 명령어를 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트 리스너](/docs/{{version}}/events) 클래스가 포함됩니다. 이벤트 리스너는 이벤트 인스턴스를 받아 특정 이벤트가 발생했을 때 로직을 처리합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
#### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:mail` 아티즌 명령어를 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 보내는 [이메일 클래스](/docs/{{version}}/mail)가 모두 들어 있습니다. 메일 객체를 사용하면 이메일 생성과 관련된 모든 로직을 하나의 간단한 클래스에 캡슐화할 수 있으며, `Mail::send` 메서드를 통해 보낼 수 있습니다.

<a name="the-models-directory"></a>
#### Models 디렉터리

`Models` 디렉터리에는 모든 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)가 포함되어 있습니다. Laravel의 Eloquent ORM은 데이터베이스 작업을 위한 심플하고 아름다운 액티브 레코드(ActiveRecord) 구현을 제공합니다. 각 데이터베이스 테이블은 상응하는 "모델"을 가지고 있으며, 이 모델을 통해 테이블과 상호작용합니다. 모델을 사용하면 데이터 조회, 신규 레코드 추가 등 다양한 작업을 수행할 수 있습니다.

<a name="the-notifications-directory"></a>
#### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:notification` 아티즌 명령어를 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 전송하는 "트랜잭션성" [알림](/docs/{{version}}/notifications)이 모두 포함됩니다. 예를 들어, 애플리케이션 내에서 발생하는 이벤트에 대한 간단한 알림을 정의할 수 있습니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 저장 등 다양한 드라이버를 통한 알림 전송을 추상화해 제공합니다.

<a name="the-policies-directory"></a>
#### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:policy` 아티즌 명령어를 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [인증 정책 클래스](/docs/{{version}}/authorization)가 포함됩니다. 정책 클래스는 사용자가 특정 리소스에 대해 주어진 동작을 수행할 수 있는지를 결정하는 데 사용됩니다.

<a name="the-providers-directory"></a>
#### Providers 디렉터리

`Providers` 디렉터리에는 애플리케이션의 모든 [서비스 프로바이더](/docs/{{version}}/providers)가 포함됩니다. 서비스 프로바이더는 서비스 컨테이너에 서비스 바인딩, 이벤트 등록, 애플리케이션 준비 등 다양한 작업을 수행하여 애플리케이션을 부트스트랩합니다.

새로운 Laravel 애플리케이션에는 몇 개의 프로바이더가 이미 포함되어 있습니다. 필요에 따라 이 디렉터리에 직접 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
#### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:rule` 아티즌 명령어를 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션의 커스텀 유효성 검사 규칙 객체가 포함됩니다. 규칙(Rule)을 사용하면 복잡한 유효성 검사 로직을 간단한 객체로 캡슐화할 수 있습니다. 더 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)에서 확인하세요.