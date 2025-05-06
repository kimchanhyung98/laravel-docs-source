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

Laravel의 기본 애플리케이션 구조는 대규모 및 소규모 애플리케이션 모두에 훌륭한 출발점을 제공합니다. 하지만 원하는 대로 애플리케이션 구조를 자유롭게 조직할 수 있습니다. Laravel에서는 어떤 클래스든 위치에 거의 제한을 두지 않으며, Composer에서 자동 로드가 가능하기만 하면 됩니다.

> [!NOTE]  
> 라라벨이 처음이신가요? [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인하여, 첫 라라벨 애플리케이션을 구축하는 과정을 직접 실습해 보세요.

<a name="the-root-directory"></a>
## 루트 디렉터리

<a name="the-root-app-directory"></a>
#### App 디렉터리

`app` 디렉터리에는 애플리케이션의 핵심 코드가 담겨 있습니다. 이 디렉터리에 대해 곧 더 자세히 살펴보겠지만, 거의 모든 애플리케이션 클래스는 이 안에 위치합니다.

<a name="the-bootstrap-directory"></a>
#### Bootstrap 디렉터리

`bootstrap` 디렉터리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 들어 있습니다. 또한 이 디렉터리에는 프레임워크가 성능 최적화를 위해 생성한 파일(예: 라우트 및 서비스 캐시 파일)을 저장하는 `cache` 디렉터리가 포함되어 있습니다. 이 디렉터리의 파일을 수정할 일은 거의 없습니다.

<a name="the-config-directory"></a>
#### Config 디렉터리

`config` 디렉터리에는 이름에서 알 수 있듯이, 애플리케이션의 모든 설정 파일이 들어 있습니다. 이 파일들을 한번 쭉 읽어보고, 사용 가능한 다양한 옵션을 숙지하는 것이 좋습니다.

<a name="the-database-directory"></a>
#### Database 디렉터리

`database` 디렉터리에는 데이터베이스 마이그레이션, 모델 팩토리, 시드 파일이 포함되어 있습니다. 원한다면 이 디렉터리에 SQLite 데이터베이스 파일을 둘 수도 있습니다.

<a name="the-public-directory"></a>
#### Public 디렉터리

`public` 디렉터리에는 애플리케이션에 들어오는 모든 요청의 진입점인 `index.php` 파일과 오토로딩 설정이 들어 있습니다. 이 디렉터리에는 이미지, 자바스크립트, CSS와 같은 애셋 파일도 포함되어 있습니다.

<a name="the-resources-directory"></a>
#### Resources 디렉터리

`resources` 디렉터리에는 [뷰](/docs/{{version}}/views)와 더불어, 컴파일되지 않은 원시 CSS, 자바스크립트 등 애셋 파일이 들어 있습니다.

<a name="the-routes-directory"></a>
#### Routes 디렉터리

`routes` 디렉터리에는 애플리케이션의 모든 라우트 정의가 들어 있습니다. 기본적으로 라라벨에는 여러 라우트 파일들이 포함되어 있습니다: `web.php`, `api.php`, `console.php`, `channels.php`.

`web.php` 파일에는 `RouteServiceProvider`가 `web` 미들웨어 그룹에 할당하는 라우트가 들어 있습니다. 이 그룹은 세션 상태, CSRF 보호, 쿠키 암호화를 제공합니다. 만약 애플리케이션이 상태 없는 RESTful API를 제공하지 않는다면, 대부분의 라우트는 `web.php`에 정의될 것입니다.

`api.php` 파일에는 `RouteServiceProvider`가 `api` 미들웨어 그룹에 할당하는 라우트가 담겨 있습니다. 이 라우트들은 상태가 없도록 설계되어 있어서, 해당 라우트로 들어오는 요청은 [토큰](/docs/{{version}}/sanctum)을 통해 인증되어야 하며 세션 상태에는 접근할 수 없습니다.

`console.php` 파일은 클로저 기반의 콘솔 명령을 정의하는 곳입니다. 각 클로저는 명령 인스턴스에 바인딩되어 각 명령의 IO 메서드와 쉽게 상호 작용할 수 있습니다. 이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 기반의 진입점(라우트)을 정의하는 곳입니다.

`channels.php` 파일은 애플리케이션에서 지원하는 모든 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 채널을 등록하는 위치입니다.

<a name="the-storage-directory"></a>
#### Storage 디렉터리

`storage` 디렉터리에는 로그, 컴파일된 블레이드 템플릿, 파일 기반 세션, 파일 캐시, 프레임워크에서 생성한 기타 파일들이 저장됩니다. 이 디렉터리는 `app`, `framework`, `logs`로 분리되어 있습니다. `app` 디렉터리는 애플리케이션에서 생성한 모든 파일을 저장하는 용도로 사용할 수 있습니다. `framework` 디렉터리는 프레임워크에서 생성한 파일과 캐시를 저장합니다. 마지막으로 `logs` 디렉터리에는 애플리케이션의 로그 파일이 들어 있습니다.

`storage/app/public` 디렉터리는 프로필 아바타와 같이 사용자가 생성한 파일을 저장하는 용도로 사용할 수 있으며, 외부에서도 접근할 수 있어야 합니다. 이 디렉터리를 가리키는 심볼릭 링크를 `public/storage`에 생성해야 합니다. `php artisan storage:link` 아티즌 명령어로 이 링크를 만들 수 있습니다.

`storage` 디렉터리의 위치는 `LARAVEL_STORAGE_PATH` 환경 변수로 변경할 수 있습니다.

<a name="the-tests-directory"></a>
#### Tests 디렉터리

`tests` 디렉터리에는 자동화된 테스트가 포함되어 있습니다. [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트 예제가 기본적으로 제공됩니다. 각 테스트 클래스는 `Test`라는 접미사를 가져야 합니다. 테스트는 `phpunit` 또는 `php vendor/bin/phpunit` 명령어로 실행할 수 있습니다. 더 자세하고 보기 좋은 테스트 결과를 원하면, `php artisan test` 아티즌 명령으로 실행할 수 있습니다.

<a name="the-vendor-directory"></a>
#### Vendor 디렉터리

`vendor` 디렉터리에는 [Composer](https://getcomposer.org) 의존성이 포함되어 있습니다.

<a name="the-app-directory"></a>
## App 디렉터리

애플리케이션의 대부분은 `app` 디렉터리에 있습니다. 기본적으로 이 디렉터리는 `App` 네임스페이스를 사용하며, [PSR-4 오토로딩 표준](https://www.php-fig.org/psr/psr-4/)을 통해 Composer에 의해 자동 로드됩니다.

`app` 디렉터리에는 `Console`, `Http`, `Providers` 등 다양한 하위 디렉터리가 있습니다. `Console`과 `Http` 디렉터리는 애플리케이션의 핵심으로 API를 제공하는 역할을 한다고 볼 수 있습니다. HTTP 프로토콜과 CLI는 모두 애플리케이션과 상호작용하는 방식일 뿐, 실제 애플리케이션 로직을 담지 않습니다. 즉, 이들은 애플리케이션에 명령을 내리는 두 가지 방법입니다. `Console` 디렉터리에는 모든 아티즌 명령어가, `Http` 디렉터리에는 컨트롤러, 미들웨어, 요청 클래스가 들어 있습니다.

`make` 아티즌 명령어로 클래스를 생성하다 보면, `app` 디렉터리 내에 여러 하위 디렉터리가 추가로 생성됩니다. 예를 들어, `make:job` 명령어를 실행하여 잡 클래스를 생성하기 전까지는 `app/Jobs` 디렉터리가 존재하지 않습니다.

> [!NOTE]  
> `app` 디렉터리 내 클래스를 아티즌 명령어로 만들 수 있습니다. 사용 가능한 명령어를 확인하려면, 터미널에서 `php artisan list make`를 실행해 보세요.

<a name="the-broadcasting-directory"></a>
#### Broadcasting 디렉터리

`Broadcasting` 디렉터리에는 애플리케이션의 모든 브로드캐스트 채널 클래스가 들어 있습니다. 이 클래스들은 `make:channel` 명령으로 생성할 수 있습니다. 기본적으로 존재하지 않는 디렉터리이나, 첫 채널을 생성하면 만들어집니다. 채널에 대해 더 알고 싶다면 [이벤트 브로드캐스팅](/docs/{{version}}/broadcasting) 문서를 참고하세요.

<a name="the-console-directory"></a>
#### Console 디렉터리

`Console` 디렉터리에는 애플리케이션의 모든 커스텀 아티즌 명령어가 들어 있습니다. 이 명령어들은 `make:command`로 생성할 수 있습니다. 또한 이 디렉터리에는 모든 커스텀 아티즌 명령어의 등록과 [스케줄링 작업](/docs/{{version}}/scheduling)을 정의하는 콘솔 커널도 포함되어 있습니다.

<a name="the-events-directory"></a>
#### Events 디렉터리

이 디렉터리는 기본적으로 존재하지 않지만, `event:generate` 또는 `make:event` 아티즌 명령으로 생성됩니다. `Events` 디렉터리에는 [이벤트 클래스](/docs/{{version}}/events)가 들어 있습니다. 이벤트는 특정 동작이 발생했을 때 애플리케이션의 다른 부분에 알림을 보내며, 높은 유연성과 결합도 감소라는 장점을 제공합니다.

<a name="the-exceptions-directory"></a>
#### Exceptions 디렉터리

`Exceptions` 디렉터리에는 애플리케이션의 예외 핸들러가 들어 있으며, 애플리케이션에서 발생하는 모든 예외를 관리하기에 좋은 위치입니다. 예외의 로깅이나 렌더링 방식을 커스터마이징하고 싶다면, 이 디렉터리의 `Handler` 클래스를 수정하세요.

<a name="the-http-directory"></a>
#### Http 디렉터리

`Http` 디렉터리에는 컨트롤러, 미들웨어, 폼 요청이 들어 있습니다. 애플리케이션에 들어오는 요청을 처리하는 로직의 대부분이 이 디렉터리에 위치합니다.

<a name="the-jobs-directory"></a>
#### Jobs 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:job` 아티즌 명령을 실행하면 생성됩니다. `Jobs` 디렉터리에는 애플리케이션의 [큐 작업](/docs/{{version}}/queues)이 들어 있습니다. 잡은 큐에 의해 처리될 수도 있고, 현재 요청 수명 내에서 동기적으로 실행될 수도 있습니다. 동기적으로 실행되는 잡은 [커맨드 패턴](https://en.wikipedia.org/wiki/Command_pattern)의 구현체이므로 "커맨드"라고도 부릅니다.

<a name="the-listeners-directory"></a>
#### Listeners 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `event:generate` 또는 `make:listener` 아티즌 명령어를 실행하면 생성됩니다. `Listeners` 디렉터리에는 [이벤트](/docs/{{version}}/events)를 처리하는 클래스들이 들어 있습니다. 이벤트 리스너 클래스는 이벤트 인스턴스를 받아 이벤트 발생에 따라 로직을 실행합니다. 예를 들어, `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너가 처리할 수 있습니다.

<a name="the-mail-directory"></a>
#### Mail 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:mail` 아티즌 명령을 실행하면 생성됩니다. `Mail` 디렉터리에는 애플리케이션에서 발송하는 [이메일 클래스](/docs/{{version}}/mail)가 들어 있습니다. 메일 오브젝트를 통해 이메일 작성 로직을 하나의 간단한 클래스로 캡슐화할 수 있으며, `Mail::send` 메서드로 발송할 수 있습니다.

<a name="the-models-directory"></a>
#### Models 디렉터리

`Models` 디렉터리에는 모든 [엘로퀀트 모델 클래스](/docs/{{version}}/eloquent)가 들어 있습니다. 라라벨의 엘로퀀트 ORM은 데이터베이스와 상호작용하기 위한 아름답고 간단한 액티브 레코드 패턴을 제공합니다. 각 데이터베이스 테이블에는 해당 테이블과 상호작용하는 "모델"이 존재합니다. 모델은 테이블의 데이터를 조회하거나, 새로운 레코드를 삽입할 수 있도록 해줍니다.

<a name="the-notifications-directory"></a>
#### Notifications 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:notification` 아티즌 명령을 실행하면 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 발송하는 모든 "트랜잭션" [알림](/docs/{{version}}/notifications)이 들어 있습니다. 예를 들어, 애플리케이션 내 이벤트 발생 시 간단한 알림을 전송할 때 사용합니다. 라라벨의 알림 기능은 이메일, 슬랙, SMS, 데이터베이스 저장 등 다양한 드라이버를 통한 전송을 추상화해 제공합니다.

<a name="the-policies-directory"></a>
#### Policies 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:policy` 아티즌 명령어를 실행하면 생성됩니다. `Policies` 디렉터리에는 애플리케이션의 [인가 정책 클래스](/docs/{{version}}/authorization)가 들어 있습니다. 정책은 사용자가 리소스에 대해 특정 작업을 수행할 권한이 있는지 판단하는 데 사용합니다.

<a name="the-providers-directory"></a>
#### Providers 디렉터리

`Providers` 디렉터리에는 애플리케이션의 모든 [서비스 프로바이더](/docs/{{version}}/providers)가 들어 있습니다. 서비스 프로바이더는 서비스 컨테이너에 서비스를 바인딩하고 이벤트를 등록하며, 애플리케이션이 요청을 처리할 준비를 할 수 있도록 다양한 작업을 수행합니다.

새로운 라라벨 애플리케이션에는 이 디렉터리에 이미 여러 프로바이더가 포함되어 있습니다. 필요한 경우 여기에 직접 서비스를 추가할 수 있습니다.

<a name="the-rules-directory"></a>
#### Rules 디렉터리

이 디렉터리는 기본적으로 존재하지 않으나, `make:rule` 아티즌 명령을 실행하면 생성됩니다. `Rules` 디렉터리에는 애플리케이션의 커스텀 유효성 검사 규칙 객체가 들어 있습니다. 규칙을 통해 복잡한 검증 로직을 하나의 객체로 캡슐화할 수 있습니다. 자세한 내용은 [유효성 검사 문서](/docs/{{version}}/validation)를 참고하세요.