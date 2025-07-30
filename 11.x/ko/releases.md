# 릴리스 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 11](#laravel-11)

<a name="versioning-scheme"></a>
## 버전 관리 체계 (Versioning Scheme)

Laravel과 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 메이저 프레임워크 릴리스는 매년 (~1분기) 출시되며, 마이너 및 패치 릴리스는 매주처럼 자주 출시될 수 있습니다. 마이너 및 패치 릴리스에는 **절대** 파괴적 변경이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크나 그 구성 요소를 참조할 때는 항상 `^11.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. 왜냐하면 Laravel 메이저 릴리스에는 파괴적 변경이 포함되기 때문입니다. 하지만 저희는 대부분 하루 이내에 새 메이저 릴리스로 손쉽게 업데이트할 수 있도록 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수 (Named Arguments)

[명명된 인수](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 이전 버전 호환성 정책에 포함되지 않습니다. Laravel 코드베이스 개선을 위해 필요할 경우 함수 인수 이름을 변경할 수 있으므로, Laravel 메서드 호출 시 명명된 인수 사용은 주의하여야 하며, 이후 인수 이름이 바뀔 수 있음을 염두에 두어야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리스에 대해 버그 수정은 18개월 동안, 보안 수정은 2년 동안 제공됩니다. Lumen을 포함한 추가 라이브러리들은 최신 메이저 릴리스에 한해 버그 수정이 제공됩니다. 또한 Laravel이 지원하는 데이터베이스 버전도 참고하시기 바랍니다([database](https://laravel.com/docs/11.x/database#introduction)).

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리스일 | 버그 수정 지원 종료 | 보안 수정 지원 종료 |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 수정 전용</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-11"></a>
## Laravel 11

Laravel 11은 Laravel 10.x에서 진행한 개선을 이어가며, 간소화된 애플리케이션 구조, 초당(rate limiting) 요청 제한, 헬스 라우팅, 원활한 암호화 키 갱신, 큐 테스트 기능 향상, [Resend](https://resend.com) 메일 전송, Prompt 유효성 검사 통합, 새로운 Artisan 명령어 등 다양한 기능을 도입했습니다. 또한, 공식적으로 제공하는 확장성 높은 WebSocket 서버인 Laravel Reverb가 추가되어 애플리케이션에 강력한 실시간 기능을 제공합니다.

<a name="php-8"></a>
### PHP 8.2

Laravel 11.x는 최소 PHP 8.2 버전을 요구합니다.

<a name="structure"></a>
### 간소화된 애플리케이션 구조

_Laravel의 간소화된 애플리케이션 구조는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)에 의해 개발되었습니다._

Laravel 11은 **새로운** Laravel 애플리케이션에 대해 간소화된 애플리케이션 구조를 도입하며, 기존 애플리케이션에는 변경을 요구하지 않습니다. 이 새로운 구조는 기존 Laravel 개발자들이 익숙한 개념을 유지하면서도 더욱 가볍고 현대적인 경험을 제공하도록 설계되었습니다. 아래에서는 Laravel의 새로운 애플리케이션 구조의 주요 특징을 설명합니다.

#### 애플리케이션 부트스트랩 파일

`bootstrap/app.php` 파일은 코드 중심의 애플리케이션 설정 파일로 재탄생했습니다. 이 파일에서 애플리케이션의 라우팅, 미들웨어, 서비스 프로바이더, 예외 처리 등을 직접 커스터마이징할 수 있습니다. 이 파일은 기존에 애플리케이션 내 여러 위치에 흩어져 있던 다양한 고수준 동작 설정들을 하나로 통합합니다:

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

기본 Laravel 애플리케이션 구조가 다섯 개의 서비스 프로바이더를 포함했던 것과 달리, Laravel 11은 단일 `AppServiceProvider`만 포함합니다. 이전의 여러 서비스 프로바이더 기능들은 `bootstrap/app.php`에 통합되었거나 프레임워크가 자동으로 처리하며, 필요하다면 `AppServiceProvider`에 배치할 수 있습니다.

예를 들어, 이벤트 자동 탐색(event discovery)이 기본 활성화되어 이벤트와 리스너를 직접 등록할 필요가 거의 없어졌습니다. 하지만 수동 등록이 필요한 경우 `AppServiceProvider`에서 직접 등록할 수 있습니다. 마찬가지로, `AuthServiceProvider`에 등록했던 라우트 모델 바인딩이나 권한 검사(authorization gates)도 `AppServiceProvider`에서 등록할 수 있습니다.

<a name="opt-in-routing"></a>
#### API 및 브로드캐스트 라우팅 선택적 설정

기본적으로 `api.php`와 `channels.php` 라우트 파일은 존재하지 않습니다. 많은 애플리케이션에 해당 파일들이 필요 없기 때문입니다. 필요 시 아래 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
#### 미들웨어

이전에는 새 Laravel 애플리케이션이 9개의 미들웨어를 포함하여 요청 인증, 입력 문자열 트림, CSRF 토큰 검증 등 다양한 작업을 수행했습니다.

Laravel 11에서는 이러한 미들웨어가 프레임워크 내부로 이동하여 애플리케이션 구조에 불필요한 부하를 주지 않습니다. 미들웨어 동작을 커스터마이징하는 새로운 메서드가 프레임워크에 추가되었으며, 이를 애플리케이션의 `bootstrap/app.php` 파일에서 호출할 수 있습니다:

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

모든 미들웨어가 `bootstrap/app.php`에서 쉽게 커스터마이징 가능해졌으므로, 별도의 HTTP "커널" 클래스의 필요성이 사라졌습니다.

<a name="scheduling"></a>
#### 스케줄링

새로운 `Schedule` 파사드를 사용하면 예약 작업을 이제 애플리케이션의 `routes/console.php` 파일에 직접 정의할 수 있습니다. 따라서 별도의 콘솔 "커널" 클래스를 만들 필요가 없어졌습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
#### 예외 처리

라우팅과 미들웨어처럼, 예외 처리도 별도의 예외 처리기 클래스를 사용하지 않고 `bootstrap/app.php` 파일에서 직접 커스터마이징할 수 있어, 새 Laravel 애플리케이션에 포함된 파일 수가 줄었습니다:

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

새 Laravel 애플리케이션에 포함된 기본 컨트롤러는 단순화되었습니다. 더 이상 내부 Laravel `Controller` 클래스를 상속하지 않고, `AuthorizesRequests`와 `ValidatesRequests` 트레이트도 제거되었습니다. 필요하다면 개별 컨트롤러에서 직접 사용할 수 있도록 분리된 것입니다:

```
<?php

namespace App\Http\Controllers;

abstract class Controller
{
    //
}
```

<a name="application-defaults"></a>
#### 애플리케이션 기본 설정

기본적으로 새 Laravel 애플리케이션은 데이터베이스 저장소로 SQLite를 사용하고, 세션, 캐시, 큐에는 `database` 드라이버를 사용합니다. 이 덕분에 별도의 소프트웨어 설치나 추가 데이터베이스 마이그레이션 없이 바로 애플리케이션 개발을 시작할 수 있습니다.

또한 시간이 지나면서, Laravel 서비스들의 `database` 드라이버가 많은 애플리케이션 환경에서 프로덕션 사용에 충분히 견고해졌기에, 로컬 환경과 프로덕션 모두에 적합한 합리적인 선택지를 제공합니다.

<a name="reverb"></a>
### Laravel Reverb

_Laravel Reverb는 [Joe Dixon](https://github.com/joedixon)이 개발했습니다._

[Laravel Reverb](https://reverb.laravel.com)는 Laravel 애플리케이션에 빠르고 확장 가능한 실시간 WebSocket 통신 기능을 직접 제공하며, Laravel Echo 등 기존 이벤트 브로드캐스팅 도구와도 원활하게 통합됩니다.

```shell
php artisan reverb:start
```

또한 Reverb는 Redis의 발행/구독(publish/subscribe) 기능을 활용해 수평 확장을 지원하며, 여러 백엔드 Reverb 서버에 WebSocket 트래픽을 분산시켜 단일 고부하 애플리케이션을 지원할 수 있습니다.

Laravel Reverb에 대한 자세한 내용은 [Reverb 문서](/docs/11.x/reverb)를 참고하세요.

<a name="rate-limiting"></a>
### 초당 요청 제한 (Per-Second Rate Limiting)

_초당 요청 제한 기능은 [Tim MacDonald](https://github.com/timacdonald)가 기여했습니다._

Laravel은 이제 HTTP 요청과 큐 작업을 포함한 모든 레이트 리미터에 대해 "초당" 요청 제한을 지원합니다. 이전에는 "분당" 단위 요청 제한만 가능했습니다:

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

레이트 리미팅에 관한 자세한 정보는 [레이트 리미팅 문서](/docs/11.x/routing#rate-limiting)를 참고하세요.

<a name="health"></a>
### 헬스 라우팅 (Health Routing)

_헬스 라우팅은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

새 Laravel 11 애플리케이션에는 `health` 라우팅 지시자가 포함되어, 서드파티 애플리케이션 헬스 모니터링 서비스나 Kubernetes 같은 오케스트레이션 시스템에서 호출할 수 있는 간단한 헬스 체크 엔드포인트를 정의합니다. 기본 경로는 `/up`입니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

이 경로에 HTTP 요청이 들어오면 Laravel은 `DiagnosingHealth` 이벤트를 발생시키며, 이 이벤트를 활용해 애플리케이션과 관련된 추가 헬스 체크를 수행할 수 있습니다.

<a name="encryption"></a>
### 원활한 암호화 키 갱신 (Graceful Encryption Key Rotation)

_원활한 암호화 키 갱신은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Laravel은 모든 쿠키를 암호화하므로, 애플리케이션의 암호화 키를 변경하면 사용자가 모두 로그아웃되고 이전 키로 암호화한 데이터를 복호화할 수 없게 됩니다.

Laravel 11은 `APP_PREVIOUS_KEYS` 환경 변수를 통해 이전 암호화 키 목록을 콤마로 구분하여 지정할 수 있습니다.

암호화 시에는 항상 현재 키(`APP_KEY`)를 사용하며, 복호화 시에는 현재 키로 먼저 시도하고 실패하면 이전 키들을 순서대로 시도해 데이터를 복호화합니다.

이 방식 덕분에 암호화 키를 갱신해도 사용자가 중단 없이 애플리케이션을 계속 이용할 수 있습니다.

암호화에 관한 자세한 내용은 [암호화 문서](/docs/11.x/encryption)를 참고하세요.

<a name="automatic-password-rehashing"></a>
### 자동 비밀번호 재해싱 (Automatic Password Rehashing)

_자동 비밀번호 재해싱 기능은 [Stephen Rees-Carter](https://github.com/valorin)이 기여했습니다._

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "작업 계수(work factor)"는 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

일반적으로 CPU/GPU 성능이 향상됨에 따라 bcrypt 작업 계수를 증가시키는 것이 권장되며, 이 경우 Laravel은 사용자가 인증할 때 비밀번호를 우아하게 자동으로 재해싱합니다.

<a name="prompt-validation"></a>
### Prompt 유효성 검사 (Prompt Validation)

_Prompt 유효성 검사 통합은 [Andrea Marco Sartori](https://github.com/cerbero90)가 기여했습니다._

[Laravel Prompts](/docs/11.x/prompts)는 CLI 애플리케이션에 직관적이고 미려한 폼을 추가할 수 있는 PHP 패키지로, 플레이스홀더 텍스트와 유효성 검사 같은 브라우저와 유사한 기능을 제공합니다.

Prompt는 클로저를 사용한 입력 유효성 검사를 지원합니다:

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

하지만 입력이 많거나 복잡한 검사일 경우 불편할 수 있습니다. 그래서 Laravel 11에서는 Laravel의 [validator](/docs/11.x/validation)를 활용해 Prompt 입력을 쉽게 검증할 수 있습니다:

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
### 큐 상호작용 테스트 (Queue Interaction Testing)

_큐 상호작용 테스트는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

이전에는 큐 작업이 큐에서 해제, 삭제되거나 수동으로 실패했는지 테스트하려면 커스텀 큐 페이크와 스텁을 정의해야 했습니다. 하지만 Laravel 11에서는 `withFakeQueueInteractions` 메서드를 사용해 간단히 큐 상호작용을 테스트할 수 있습니다:

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

큐 테스트에 관한 자세한 내용은 [큐 문서](/docs/11.x/queues#testing)를 참고하세요.

<a name="new-artisan-commands"></a>
### 새로운 Artisan 명령어

_클래스 생성 Artisan 명령어는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

클래스, 열거형(enum), 인터페이스, 트레이트를 빠르게 생성할 수 있는 새로운 Artisan 명령어가 추가되었습니다:

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
### 모델 캐스트 개선 (Model Casts Improvements)

_모델 캐스트 개선은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

Laravel 11에서는 모델의 캐스트를 속성이 아닌 메서드로 정의할 수 있습니다. 이는 특히 인수를 갖는 캐스트를 사용할 때 간결하고 유창한 정의를 가능하게 합니다:

```
/**
 * 캐스트할 속성 반환 메서드
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
```

속성 캐스팅에 관한 자세한 내용은 [Eloquent 문서](/docs/11.x/eloquent-mutators#attribute-casting)를 참고하세요.

<a name="the-once-function"></a>
### `once` 함수

_`once` 헬퍼는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

`once` 헬퍼 함수는 주어진 콜백을 실행하고, 요청 처리 중 메모리에 결과를 캐싱합니다. 동일 콜백으로 `once`를 여러 번 호출하면 이전에 캐시된 결과를 반환합니다:

```
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (캐시된 결과)
random(); // 123 (캐시된 결과)
```

`once` 헬퍼에 관한 자세한 내용은 [헬퍼 문서](/docs/11.x/helpers#method-once)를 참고하세요.

<a name="database-performance"></a>
### 인메모리 데이터베이스 테스트 성능 향상

_인메모리 데이터베이스 테스트 성능 향상은 [Anders Jenbo](https://github.com/AJenbo)가 기여했습니다._

Laravel 11은 테스트 시 `:memory:` SQLite 데이터베이스 사용 시 속도를 대폭 개선합니다. PHP의 PDO 객체 참조를 유지하고 연결 간 이를 재사용하여, 전체 테스트 실행 시간을 절반으로 줄이는 경우도 있습니다.

<a name="mariadb"></a>
### MariaDB 지원 향상

_MariaDB 지원 향상은 [Jonas Staudenmeir](https://github.com/staudenmeir)와 [Julius Kiekbusch](https://github.com/Jubeki)가 기여했습니다._

이전 Laravel에서는 MariaDB를 MySQL 드라이버를 통해 사용했으나, Laravel 11부터는 MariaDB 전용 드라이버가 포함되어 MariaDB에 더 적합한 기본 설정과 동작을 제공합니다.

Laravel 데이터베이스 드라이버에 관한 자세한 내용은 [데이터베이스 문서](/docs/11.x/database)를 참고하세요.

<a name="inspecting-database"></a>
### 데이터베이스 검사 및 스키마 작업 개선

_스키마 작업과 데이터베이스 검사 향상은 [Hafez Divandari](https://github.com/hafezdivandari)가 기여했습니다._

Laravel 11은 컬럼의 수정, 이름 변경, 삭제를 네이티브 방식으로 지원하는 등 데이터베이스 스키마 작업과 검사 기능을 확장했습니다. 또한 고급 공간 타입, 비기본 스키마명, 그리고 테이블, 뷰, 컬럼, 인덱스, 외래 키 조작을 위한 네이티브 스키마 메서드를 추가 제공합 니다:

```
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```