# 릴리즈 노트

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 11](#laravel-11)

<a name="versioning-scheme"></a>
## 버전 관리 정책

라라벨과 공식 1차 파티 패키지들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년(대략 1분기)에 한 번씩 출시되며, 마이너/패치 릴리스는 매주 단위로 제공될 수 있습니다. 마이너 및 패치 릴리스에는 **절대** 호환성에 영향을 주는 변경사항이 포함되지 않습니다.

애플리케이션이나 패키지에서 라라벨 프레임워크 혹은 컴포넌트를 참조할 때는 `^11.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. 라라벨의 주요 릴리스는 호환성에 영향을 미칠 수 있기 때문입니다. 하지만, 새로운 주요 버전으로 하루 이내에 마이그레이션할 수 있도록 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트(Named Arguments)

[네임드 아규먼트](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 라라벨의 하위 호환성 가이드라인에 포함되지 않습니다. 라라벨 코드베이스의 개선을 위해 필요한 경우 함수 인자명을 변경할 수 있습니다. 따라서, 라라벨 메서드를 호출할 때 네임드 아규먼트를 사용할 경우, 향후 파라미터명이 변경될 가능성을 숙지하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 라라벨 릴리스는 버그 픽스가 18개월, 보안 픽스가 2년간 제공됩니다. Lumen을 포함한 추가 라이브러리는 최신 주요 버전에만 버그 픽스가 제공됩니다. 또한 라라벨이 지원하는 데이터베이스 버전을 [문서](/docs/{{version}}/database#introduction)에서 확인하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리스 | 버그 픽스 종료 | 보안 픽스 종료 |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 픽스만 제공</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-11"></a>
## 라라벨 11

라라벨 11은 라라벨 10.x의 개선 사항을 지속하며, 간소화된 애플리케이션 구조, 초 단위의 속도 제한, Health 라우팅, 부드러운 암호화 키 로테이션, 큐 테스트 개선, [Resend](https://resend.com) 메일 전송 지원, Prompt 유효성 검사 통합, 새로운 Artisan 명령어 등을 도입했습니다. 또한, 공식 확장 WebSocket 서버인 Laravel Reverb를 통해 실시간 기능이 강력하게 추가되었습니다.

<a name="php-8"></a>
### PHP 8.2

라라벨 11.x는 최소 PHP 8.2 버전이 필요합니다.

<a name="structure"></a>
### 간소화된 애플리케이션 구조

_라라벨의 간소화된 애플리케이션 구조는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)에 의해 개발되었습니다._

라라벨 11은 **새로운** 라라벨 애플리케이션에서 간소화된 구조를 도입합니다. 기존 애플리케이션에는 영향을 주지 않습니다. 이 새로운 구조는 더 효율적이고 현대적인 경험을 위해 설계되었으며, 라라벨 개발자에게 익숙한 많은 개념을 그대로 유지합니다. 아래에서 이 구조의 주요 내용을 소개합니다.

#### 애플리케이션 부트스트랩 파일

`bootstrap/app.php` 파일이 코드 기반 애플리케이션 설정 파일로 재구성되었습니다. 이 파일에서 라우팅, 미들웨어, 서비스 프로바이더, 예외 처리 등 대부분의 애플리케이션 설정을 할 수 있습니다. 이전에는 여러 파일에 흩어져 있던 주요 설정을 이곳에서 통합적으로 관리할 수 있습니다:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

<a name="service-providers"></a>
#### 서비스 프로바이더

기본 라라벨 애플리케이션 구조에는 다섯 개의 서비스 프로바이더가 있었지만, 라라벨 11에서는 `AppServiceProvider` 하나만 포함됩니다. 기존 프로바이더의 역할은 `bootstrap/app.php`로 이동되었거나 프레임워크가 자동으로 처리하며, 필요시 `AppServiceProvider`에 추가할 수 있습니다.

예를 들어, 이벤트 디스커버리는 기본적으로 활성화되어 더 이상 이벤트와 리스너를 수동 등록할 필요가 거의 없습니다. 하지만 수동 등록이 필요한 경우 `AppServiceProvider`에서 처리할 수 있습니다. 마찬가지로, 기존에 `AuthServiceProvider`에 등록했던 라우트 모델 바인딩이나 인증 게이트도 이제 `AppServiceProvider`에 등록할 수 있습니다.

<a name="opt-in-routing"></a>
#### 선택적 API 및 브로드캐스트 라우팅

많은 애플리케이션에서 필요하지 않은 `api.php`와 `channels.php` 라우트 파일은 기본적으로 제공되지 않습니다. 해당 기능이 필요하면 아래와 같은 간단한 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
#### 미들웨어

이전에는 새로운 라라벨 애플리케이션에 아홉 개의 미들웨어가 기본 포함되어 있었습니다. 이 미들웨어들은 인증, 입력 값 트림, CSRF 토큰 검증 등 다양한 역할을 수행했습니다.

라라벨 11에서는 이러한 미들웨어들이 프레임워크 내부로 이동되어, 애플리케이션 구조를 더 간결하게 만들었습니다. 각 미들웨어의 동작을 사용자 정의할 수 있도록 프레임워크에 새로운 메서드들이 추가되었으며, `bootstrap/app.php`에서 쉽게 호출할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(
        except: ['stripe/*']
    );

    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ])
})
```

모든 미들웨어는 `bootstrap/app.php`에서 쉽게 커스터마이즈할 수 있으므로, 별도의 HTTP "kernel" 클래스가 더 이상 필요하지 않습니다.

<a name="scheduling"></a>
#### 스케줄링

이제 새로운 `Schedule` 파사드를 이용해, 예약 작업을 애플리케이션의 `routes/console.php`에서 직접 정의할 수 있습니다. 별도의 콘솔 "kernel" 클래스가 필요 없습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
#### 예외 처리

라우팅과 미들웨어처럼, 예외 처리 역시 별도의 예외 핸들러 클래스 없이도 `bootstrap/app.php`에서 커스터마이즈할 수 있습니다. 이로써 새 라라벨 애플리케이션의 파일 수가 더욱 줄어듭니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport(MissedFlightException::class);

    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<a name="base-controller-class"></a>
#### 기본 `Controller` 클래스

새로운 라라벨 애플리케이션의 기본 컨트롤러가 단순화되었습니다. 프레임워크 내부의 `Controller` 클래스를 상속받지 않으며, `AuthorizesRequests` 및 `ValidatesRequests` 트레잇도 제거되었습니다. 필요한 경우 개별 컨트롤러에서 트레잇을 포함할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    abstract class Controller
    {
        //
    }

<a name="application-defaults"></a>
#### 애플리케이션 기본값

기본적으로, 새로운 라라벨 애플리케이션은 데이터베이스 저장소로 SQLite를, 세션·캐시·큐는 모두 `database` 드라이버를 사용합니다. 별도의 소프트웨어 설치나 데이터베이스 마이그레이션 없이 개발을 즉시 시작할 수 있습니다.

또한, 시간이 지나면서 이 Laravel 서비스의 `database` 드라이버는 많은 상황에서 실 서비스에도 충분할 만큼 견고해졌기에, 로컬/운영 환경 모두에서 적절한 기본값이 됩니다.

<a name="reverb"></a>
### 라라벨 리버브(Laravel Reverb)

_Laravel Reverb는 [Joe Dixon](https://github.com/joedixon)이 개발했습니다._

[라라벨 리버브](https://reverb.laravel.com)는 초고속·확장성 높은 실시간 WebSocket 통신을 라라벨 애플리케이션에 직접 제공하며, Laravel Echo 같은 기존 이벤트 브로드캐스팅 도구와도 완벽하게 통합됩니다.

```shell
php artisan reverb:start
```

또한 Redis의 publish/subscribe 기능을 활용해 수평 확장(여러 대 서버 운영)이 가능하므로, 단일 대용량 애플리케이션을 여러 리버브 서버에서 지원할 수 있습니다.

라라벨 리버브에 대한 더 자세한 내용은 [공식 문서](/docs/{{version}}/reverb)를 참고하세요.

<a name="rate-limiting"></a>
### 초 단위 속도 제한(Per-Second Rate Limiting)

_초 단위 속도 제한은 [Tim MacDonald](https://github.com/timacdonald)가 기여했습니다._

이제 라라벨은 HTTP 요청 및 큐 작업 등 모든 속도 제한자에서 "초 단위" 제한이 가능합니다. 이전에는 "분 단위"만 지원했습니다.

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

라라벨의 속도 제한에 관한 자세한 내용은 [문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="health"></a>
### Health 라우팅

_Health 라우팅은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

라라벨 11에서는 `health` 라우팅 디렉티브가 포함되어, 쿠버네티스 등 외부 헬스 모니터링 시스템이나 오케스트레이션 시스템이 사용할 수 있는 간단한 헬스 체크 엔드포인트를 제공합니다. 기본적으로 이 라우트는 `/up`에서 제공됩니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

이 경로에 HTTP 요청이 오면 라라벨은 `DiagnosingHealth` 이벤트를 디스패치하여, 추가적인 헬스 체크 로직을 구현할 수도 있습니다.

<a name="encryption"></a>
### 부드러운 암호화 키 회전(Graceful Encryption Key Rotation)

_암호화 키 회전은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

라라벨은 세션 쿠키를 포함한 모든 쿠키를 암호화합니다. 때문에 암호화 키를 회전하면 모든 사용자가 로그아웃되고, 이전 키로 암호화된 데이터는 복호화할 수 없습니다.

라라벨 11에서는 `APP_PREVIOUS_KEYS` 환경변수에 이전 암호화 키들을 콤마로 구분해 지정할 수 있습니다.

암호화 시에는 항상 `APP_KEY`의 "현재" 키를 사용하고, 복호화 시 실패할 경우 이전 키들을 차례로 시도하여 복호화에 성공하면 해당 값을 사용합니다.

이 덕분에 암호화 키를 회전해도 사용자 경험에 끊김이 없습니다.

라라벨의 암호화에 대한 자세한 내용은 [문서](/docs/{{version}}/encryption)를 참고하세요.

<a name="automatic-password-rehashing"></a>
### 자동 비밀번호 재해싱

_자동 비밀번호 재해싱은 [Stephen Rees-Carter](https://github.com/valorin)가 기여했습니다._

라라벨의 기본 비밀번호 해싱 알고리즘은 bcrypt이고, work factor는 `config/hashing.php` 또는 `BCRYPT_ROUNDS` 환경변수로 조정할 수 있습니다.

CPU/GPU 성능이 증가함에 따라 work factor를 늘려야 하는데, 값을 높이면 사용자가 로그인할 때 자동으로 비밀번호가 새롭게 해싱됩니다.

<a name="prompt-validation"></a>
### 프롬프트 유효성 검사

_Prompt 유효성 검사 통합은 [Andrea Marco Sartori](https://github.com/cerbero90)가 기여했습니다._

[라라벨 프롬프트](/docs/{{version}}/prompts)는 커맨드라인에 브라우저 형태의 폼이나 유효성 검사를 쉽게 구현할 수 있는 PHP 패키지입니다. 클로저로 입력값 검증이 가능합니다:

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

복잡한 입력이나 다수의 입력을 처리할 경우에는 불편할 수 있어, 라라벨 11에서는 [validator](/docs/{{version}}/validation) 규칙 전체를 활용할 수 있습니다:

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
### 큐 상호작용 테스트

_큐 상호작용 테스트는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

이전에는 큐 작업이 릴리스, 삭제, 수동 실패했는지 테스트하기가 까다로웠지만, 라라벨 11에서는 `withFakeQueueInteractions` 메서드를 통해 손쉽게 테스트할 수 있습니다:

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

큐 작업 테스트에 대한 자세한 내용은 [문서](/docs/{{version}}/queues#testing)를 참고하세요.

<a name="new-artisan-commands"></a>
### 새로운 Artisan 명령어

_클래스 생성 Artisan 명령어는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

새로운 Artisan 명령어를 통해 클래스, enum, interface, trait을 빠르게 생성할 수 있습니다:

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
### 모델 캐스트 개선

_모델 캐스트 개선은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

라라벨 11에서는 모델의 캐스트를 속성 대신 메서드로 정의할 수 있습니다. 인자가 필요한 캐스트를 더욱 명확하고 간결하게 활용할 수 있습니다:

    /**
     * 캐스트 대상 attribute 정의.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsCollection::using(OptionCollection::class),
                      // AsEncryptedCollection::using(OptionCollection::class),
                      // AsEnumArrayObject::using(OptionEnum::class),
                      // AsEnumCollection::using(OptionEnum::class),
        ];
    }

attribute 캐스팅에 대한 자세한 내용은 [Eloquent 문서](/docs/{{version}}/eloquent-mutators#attribute-casting)를 참고하세요.

<a name="the-once-function"></a>
### `once` 함수

_`once` 헬퍼는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

`once` 헬퍼 함수는 전달된 콜백을 한 번만 실행하고, 그 결과를 요청 동안 메모리에 캐시합니다. 동일한 콜백에 대한 이후 호출은 캐시된 결과를 반환합니다:

    function random(): int
    {
        return once(function () {
            return random_int(1, 1000);
        });
    }

    random(); // 123
    random(); // 123 (캐시된 값)
    random(); // 123 (캐시된 값)

`once` 헬퍼에 대한 자세한 내용은 [헬퍼 문서](/docs/{{version}}/helpers#method-once)를 참조하세요.

<a name="database-performance"></a>
### 인메모리 데이터베이스 테스트 성능 개선

_인메모리 데이터베이스 테스트 성능 개선은 [Anders Jenbo](https://github.com/AJenbo)가 기여했습니다._

라라벨 11은 테스트 시 `:memory:` SQLite 데이터베이스 사용 시 속도가 크게 향상됩니다. PHP의 PDO 객체를 재활용하여 연결을 유지함으로써 전체 테스트 실행 시간을 절반 가까이 단축할 수 있습니다.

<a name="mariadb"></a>
### MariaDB 지원 개선

_MariaDB 지원 개선은 [Jonas Staudenmeir](https://github.com/staudenmeir)와 [Julius Kiekbusch](https://github.com/Jubeki)가 기여했습니다._

라라벨 11은 MariaDB에 대한 지원이 더욱 향상되었습니다. 이전 버전에서는 MySQL 드라이버를 사용했지만, 이제는 MariaDB 전용 드라이버가 포함되어 MariaDB에 최적화된 기본값을 제공합니다.

더 자세한 내용은 [데이터베이스 문서](/docs/{{version}}/database)를 참조하세요.

<a name="inspecting-database"></a>
### 데이터베이스 인스펙션 및 스키마 작업 개선

_스키마 작업 및 데이터베이스 인스펙션 개선은 [Hafez Divandari](https://github.com/hafezdivandari)가 기여했습니다._

라라벨 11은 데이터베이스 스키마의 조작 및 인스펙션을 위한 추가 메서드를 제공합니다. 여기에는 컬럼 수정, 이름 변경, 삭제 등 다양한 원시 동작이 포함되며, 고급 공간 타입, 비기본 스키마 네임, 테이블·뷰·컬럼·인덱스·외래키를 위한 네이티브 스키마 메서드가 제공됩니다:

    use Illuminate\Support\Facades\Schema;

    $tables = Schema::getTables();
    $views = Schema::getViews();
    $columns = Schema::getColumns('users');
    $indexes = Schema::getIndexes('users');
    $foreignKeys = Schema::getForeignKeys('users');