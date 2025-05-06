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

기본 Laravel 애플리케이션 구조는 대규모 및 소규모 애플리케이션 모두에 훌륭한 출발점을 제공하도록 설계되었습니다. 하지만 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel은 클래스를 어디에 배치하는지에 대해 거의 제한을 두지 않습니다. Composer가 클래스를 오토로딩 할 수 있는 한 어떤 위치라도 괜찮습니다.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
#### App 디렉터리

`app` 디렉터리에는 애플리케이션의 핵심 코드가 포함되어 있습니다. 이 디렉터리에 대해 곧 더 자세히 살펴보겠지만, 여러분의 애플리케이션에서 대부분의 클래스들은 이 디렉터리 내에 위치하게 됩니다.

<a name="the-bootstrap-directory"></a>
#### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 들어 있습니다. 이 디렉터리에는 또한 프레임워크에서 생성하는 캐시 파일(예: 라우트와 서비스 파일 캐시) 등 성능 최적화를 위한 `cache` 디렉터리가 있습니다. 일반적으로 이 디렉터리 내의 파일을 수정할 필요는 없습니다.

<a name="the-config-directory"></a>
#### Config 디렉터리

`config` 디렉터리에는 이름에서 알 수 있듯이 애플리케이션의 모든 설정 파일이 포함되어 있습니다. 이 파일들을 하나하나 읽어보며 사용할 수 있는 옵션들을 익혀두는 것이 좋습니다.

<a name="the-database-directory"></a>
#### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 포함되어 있습니다. 필요하다면 이 디렉터리에 SQLite 데이터베이스 파일을 저장할 수도 있습니다.

<a name="the-public-directory"></a>
#### Public 디렉터리

`public` 디렉터리에는 모든 요청이 처음 들어오는 진입점인 `index.php` 파일이 들어 있으며, 오토로딩 설정도 포함되어 있습니다. 또한 이미지, JavaScript, CSS와 같은 애셋 파일도 이곳에 위치합니다.

<a name="the-resources-directory"></a>
#### Resources 디렉터리

`resources` 디렉터리에는 [뷰](/docs/{{version}}/views)와 컴파일되지 않은 원시 애셋(CSS, JavaScript 등)이 들어 있습니다. 또한 모든 언어 파일도 이 디렉터리에 포함되어 있습니다.

<a name="the-routes-directory"></a>
#### Routes 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우팅 정의가 포함되어 있습니다. 기본적으로 Laravel에는 여러 라우트 파일이 제공되는데, `web.php`, `api.php`, `console.php`, 그리고 `channels.php`입니다.

- `web.php` 파일에는 `RouteServiceProvider`가 `web` 미들웨어 그룹에 할당하는 라우트가 정의되며, 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 여러분의 애플리케이션이 무상태의 RESTful API를 제공하지 않는다면 대부분의 라우트는 `web.php` 파일에 정의될 것입니다.

- `api.php` 파일에는 `RouteServiceProvider`가 `api` 미들웨어 그룹에 할당하는 라우트가 포함됩니다. 이 라우트는 무상태(stateless)로 동작하며, 해당 경로를 통해 들어온 요청은 [토큰](/docs/{{version}}/sanctum) 인증을 거치고 세션 상태에 접근할 수 없습니다.

- `console.php` 파일에서는 클로저 기반의 콘솔 명령어를 정의할 수 있습니다. 각 클로저는 커맨드 인스턴스에 바인딩되어 있어, 각 커맨드의 IO 메서드와 쉽게 상호작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션의 콘솔 진입점(라우트)을 정의합니다.

- `channels.php` 파일은 애플리케이션이 지원하는 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록하는 곳입니다.

<a name="the-storage-directory"></a>
#### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 블레이드 템플릿, 파일 기반 세션, 파일 캐시, 그리고 프레임워크에서 생성한 기타 파일이 들어 있습니다. 이 디렉터리는 `app`, `framework`, `logs`의 하위 디렉터리로 분리되어 있습니다. `app` 디렉터리는 애플리케이션이 생성하는 파일을 저장하는 용도입니다. `framework` 디렉터리는 프레임워크에서 생성된 파일과 캐시가 저장됩니다. 마지막으로 `logs` 디렉터리에는 애플리케이션의 로그 파일이 저장됩니다.

`storage/app/public` 디렉터리는 프로필 아바타와 같은 공개적으로 접근 가능한 사용자 생성 파일을 보관할 때 사용할 수 있습니다. 이 디렉터리를 가리키는 심볼릭 링크를 `public/storage`에 생성해야 합니다. `php artisan storage:link` 명령어로 링크를 만들 수 있습니다.

<a name="the-tests-directory"></a>
#### Tests 디렉터리

`tests` 디렉터리에는 자동화된 테스트가 들어 있습니다. 예시 [PHPUnit](https://phpunit.de/) 단위 테스트와 기능 테스트가 기본적으로 제공됩니다. 각 테스트 클래스 이름은 `Test`로 끝나야 합니다. `phpunit` 또는 `php vendor/bin/phpunit` 명령어로 테스트를 실행할 수 있습니다. 또는 보다 아름답고 상세한 테스트 결과를 원한다면 `php artisan test` 명령어를 사용할 수 있습니다.

<a name="the-vendor-directory"></a>
#### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 패키지 의존성이 들어 있습니다.

<a name="the-app-directory"></a>
## App 디렉터리

애플리케이션의 대부분은 `app` 디렉터리 내부에 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스 하에 있으며, [PSR-4 오토로딩 표준](https://www.php-fig.org/psr/psr-4/)을 사용해 Composer로 자동 로딩됩니다.

`app` 디렉터리에는 `Console`, `Http`, `Providers` 등 여러 하위 디렉터리가 포함되어 있습니다. `Console`, `Http` 디렉터리는 애플리케이션 코어에 대한 API 제공자 역할을 한다고 볼 수 있습니다. HTTP 프로토콜과 CLI는 애플리케이션과 상호작용하는 수단일 뿐 실제 비즈니스 로직은 포함되어 있지 않습니다. 즉, 두 방식 모두 애플리케이션에 명령을 내리는 방법입니다. `Console` 디렉터리에는 모든 Artisan 커맨드가, `Http` 디렉터리에는 컨트롤러, 미들웨어, 리퀘스트 클래스가 포함됩니다.

`app` 디렉터리 내부에는 클래스를 생성할 때마다 `make` Artisan 명령어를 통해 다양한 하위 디렉터리가 생성됩니다. 예를 들어, `make:job` 명령을 실행하기 전까지는 `app/Jobs` 디렉터리가 존재하지 않습니다.

> {tip} `app` 디렉터리 내 다수의 클래스는 Artisan 명령어로 생성할 수 있습니다. 사용 가능한 명령어 목록을 확인하려면 터미널에서 `php artisan list make` 명령을 실행해 보세요.

<a name="the-broadcasting-directory"></a>
#### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 애플리케이션의 브로드캐스트 채널 클래스가 모두 포함됩니다. 이 클래스들은 `make:channel` 명령어로 생성됩니다. 기본적으로 이 디렉터리는 존재하지 않지만 첫 채널을 생성하면 자동으로 만들어집니다. 채널에 대해 더 알고 싶다면 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
#### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 커스텀 Artisan 명령어가 모두 포함되어 있습니다. 이 명령어는 `make:command` 명령어로 생성할 수 있습니다. 또한 이 디렉터리에는 콘솔 커널 파일이 위치하며, 이곳에 커스텀 Artisan 명령을 등록하고 [스케줄러 작업](/docs/{{version}}/scheduling)을 정의할 수 있습니다.

<a name="the-events-directory"></a>
#### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 혹은 `make:event` 명령어를 사용하면 생성됩니다. `Events` 디렉터리는 [이벤트 클래스](/docs/{{version}}/events)들이 위치하는 곳입니다. 이벤트는 애플리케이션 내에서 특정 동작이 발생했을 때 다른 부분에 알리는 역할을 하며, 뛰어난 유연성과 결합도 감소 효과를 제공합니다.

<a name="the-exceptions-directory"></a>
#### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 예외 처리기가 포함되어 있으며, 애플리케이션에서 발생하는 예외를 저장하기에도 좋은 위치입니다. 예외의 로깅 또는 렌더링 방식을 커스텀하고 싶다면 이 디렉터리 내의 `Handler` 클래스를 수정하면 됩니다.

<a name="the-http-directory"></a>
#### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 리퀘스트가 포함되어 있습니다. 애플리케이션에 들어오는 요청을 처리하는 대부분의 로직이 이 디렉터리에 위치하게 됩니다.

<a name="the-jobs-directory"></a>
#### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `make:job` Artisan 명령을 실행하면 생성됩니다. `Jobs` 디렉터리에는 [큐 작업](/docs/{{version}}/queues)이 위치합니다. 작업(Job)은 애플리케이션이 큐에 넣거나, 현재 요청 사이클 내에서 동기적으로 실행할 수 있습니다. 현재 요청 중에 동기적으로 실행되는 작업은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)을 구현하기 때문에 '커맨드'라고 부르기도 합니다.

<a name="the-listeners-directory"></a>
#### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 혹은 `make:listener` 명령어를 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/{{version}}/events)를 처리하는 클래스가 들어 있습니다. 이벤트 리스너는 이벤트 인스턴스를 받아 이벤트 발생 시 후처리 로직을 수행합니다. 예를 들면 `UserRegistered` 이벤트가 발생하면 `SendWelcomeEmail` 리스너가 해당 이벤트를 처리할 수 있습니다.

<a name="the-mail-directory"></a>
#### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:mail` 명령어로 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 보내는 [이메일을 표현하는 클래스](/docs/{{version}}/mail)가 들어 있습니다. 메일 오브젝트는 이메일을 구성하는 모든 로직을 하나의 간단한 클래스로 캡슐화할 수 있으며, `Mail::send` 메서드를 통해 전송될 수 있습니다.

<a name="the-models-directory"></a>
#### Models 디렉터리

`Models` 디렉터리에는 [Eloquent 모델 클래스](/docs/{{version}}/eloquent)가 모두 저장됩니다. Laravel에 포함된 Eloquent ORM은 데이터베이스 작업을 위한 아름답고 간단한 액티브레코드(Active Record) 구현을 제공합니다. 각 데이터베이스 테이블당 하나의 '모델'이 존재하며, 이 모델을 통해 해당 테이블과 상호작용을 합니다. 모델을 통해 테이블에서 데이터를 조회하거나 새 레코드를 추가할 수 있습니다.

<a name="the-notifications-directory"></a>
#### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:notification` Artisan 명령어 실행 시 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 발송하는 "트랜잭션성" [알림](/docs/{{version}}/notifications)이 모여 있습니다. Laravel의 알림 기능은 이메일, Slack, SMS, 데이터베이스 등 다양한 드라이버를 통해 알림을 보낼 수 있게 추상화되어 있습니다.

<a name="the-policies-directory"></a>
#### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:policy` 명령어로 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [인증 정책 클래스](/docs/{{version}}/authorization)가 포함되어 있습니다. 정책은 사용자가 특정 리소스에 대해 동작을 수행할 수 있는지 판단할 때 사용됩니다.

<a name="the-providers-directory"></a>
#### Providers 디렉터리

`Providers` 디렉터리에는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)가 모두 포함되어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하거나, 이벤트를 등록하거나, 들어오는 요청을 위한 다양한 초기화 작업을 수행함으로써 애플리케이션을 부트스트랩합니다.

새로운 Laravel 애플리케이션에는 이미 몇 가지 프로바이더가 포함되어 있습니다. 필요하다면 이 디렉터리에 자신만의 프로바이더를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
#### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않으며, `make:rule` 명령어로 생성됩니다. `Rules` 디렉터리에는 애플리케이션의 커스텀 유효성 검사(Validation) 규칙 객체가 모여 있습니다. 규칙 객체를 사용해 복잡한 유효성 검사 로직을 간단한 객체로 캡슐화할 수 있습니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.