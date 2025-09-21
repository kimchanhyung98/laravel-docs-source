# 업그레이드 가이드 (Upgrade Guide)

- [9.x에서 10.0으로 업그레이드](#upgrade-10.0)

<a name="high-impact-changes"></a>
## 영향도가 높은 변경 사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [최소 안정성(minimum stability) 업데이트](#updating-minimum-stability)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경 사항

<div class="content-list" markdown="1">

- [데이터베이스 표현식](#database-expressions)
- [모델 "dates" 속성](#model-dates-property)
- [Monolog 3](#monolog-3)
- [Redis 캐시 태그](#redis-cache-tags)
- [서비스 모킹](#service-mocking)
- [언어 디렉터리](#language-directory)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경 사항

<div class="content-list" markdown="1">

- [클로저 유효성 검증 규칙 메시지](#closure-validation-rule-messages)
- [Form Request `after` 메서드](#form-request-after-method)
- [public 경로 바인딩](#public-path-binding)
- [Query Exception 생성자](#query-exception-constructor)
- [Rate Limiter 반환값](#rate-limiter-return-values)
- [`Redirect::home` 메서드](#redirect-home)
- [`Bus::dispatchNow` 메서드](#dispatch-now)
- [`registerPolicies` 메서드](#register-policies)
- [ULID 컬럼](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## 9.x에서 10.0으로 업그레이드 (Upgrading to 10.0 from 9.x)

<a name="estimated-upgrade-time-??-minutes"></a>
#### 예상 업그레이드 소요 시간: 10분

> [!NOTE]  
> 모든 잠재적 하위 호환성 깨짐(breaking change)을 문서화하려고 노력하였으나, 일부 변경 사항은 프레임워크의 잘 사용되지 않는 부분이므로 실제로는 일부만이 애플리케이션에 영향을 미칠 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하면 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음(High)**

#### PHP 8.1.0 필수

Laravel은 이제 PHP 8.1.0 이상이 필요합니다.

#### Composer 2.2.0 필수

Laravel은 이제 [Composer](https://getcomposer.org) 2.2.0 이상이 필요합니다.

#### Composer 의존성

애플리케이션의 `composer.json` 파일에서 아래의 의존성 버전을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework`를 `^10.0`으로
- `laravel/sanctum`을 `^3.2`로
- `doctrine/dbal`을 `^3.0`으로
- `spatie/laravel-ignition`을 `^2.0`으로
- `laravel/passport`를 `^11.0`으로 ([업그레이드 가이드](https://github.com/laravel/passport/blob/11.x/UPGRADE.md) 참고)
- `laravel/ui`를 `^4.0`으로

</div>

Sanctum 3.x 버전으로 2.x에서 업그레이드하는 경우, [Sanctum 업그레이드 가이드](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md)를 반드시 참고하시기 바랍니다.

또한, [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html)을 사용하려면, `phpunit.xml` 설정 파일의 `<coverage>` 섹션에서 `processUncoveredFiles` 속성을 삭제해야 합니다. 그런 다음 아래 의존성을 `composer.json`에서 업데이트하세요.

<div class="content-list" markdown="1">

- `nunomaduro/collision`을 `^7.0`으로
- `phpunit/phpunit`을 `^10.0`으로

</div>

마지막으로, 애플리케이션에서 사용하는 다른 모든 서드파티 패키지가 Laravel 10을 지원하는 적절한 버전을 사용하는지도 확인해야 합니다.

<a name="updating-minimum-stability"></a>
#### 최소 안정성(minimum stability)

애플리케이션의 `composer.json` 파일 내 `minimum-stability` 값을 `stable`로 수정하세요. 또는, 기본값이 이미 `stable`이므로 해당 설정을 완전히 삭제해도 무방합니다:

```json
"minimum-stability": "stable",
```

### 애플리케이션

<a name="public-path-binding"></a>
#### public 경로 바인딩

**영향 가능성: 낮음(Low)**

애플리케이션이 `path.public`을 컨테이너에 바인딩하여 "public 경로"를 커스텀하게 설정하는 경우, 이제 `Illuminate\Foundation\Application` 객체가 제공하는 `usePublicPath` 메서드를 사용하도록 코드를 변경해야 합니다:

```php
app()->usePublicPath(__DIR__.'/public');
```

### 인가(Authorization)

<a name="register-policies"></a>
### `registerPolicies` 메서드

**영향 가능성: 낮음(Low)**

`AuthServiceProvider`의 `registerPolicies` 메서드는 이제 프레임워크에서 자동으로 호출됩니다. 따라서, `AuthServiceProvider`의 `boot` 메서드에서 이 메서드 호출을 제거해도 됩니다.

### 캐시(Cache)

<a name="redis-cache-tags"></a>
#### Redis 캐시 태그

**영향 가능성: 중간(Medium)**

`Cache::tags()` 사용은 Memcached를 사용하는 애플리케이션에서만 권장됩니다. 애플리케이션의 캐시 드라이버로 Redis를 사용하는 경우, Memcached로 전환하거나 Laravel [12.30.0](https://github.com/laravel/framework/pull/57098)으로 업그레이드하는 것을 고려해야 합니다.

### 데이터베이스

<a name="database-expressions"></a>
#### 데이터베이스 표현식

**영향 가능성: 중간(Medium)**

Laravel 10.x에서는 데이터베이스 "표현식"(주로 `DB::raw`를 통해 생성)의 내부 구현이 개선되어, 추후 추가 기능 확장에 대비하게 되었습니다. 주요 변경점은, 문법(grammar)의 원시 문자열 값을 이제 표현식의 `getValue(Grammar $grammar)` 메서드로 가져와야 한다는 점입니다. `(string)`으로 표현식을 문자열로 변환하는 방식은 더 이상 지원되지 않습니다.

**일반적으로, 이 변경은 대부분의 애플리케이션에는 영향을 주지 않습니다**. 하지만, 수동으로 `(string)`을 사용하거나 `__toString` 메서드를 직접 호출해 문자열로 변환하고 있다면, 다음과 같이 `getValue` 메서드를 사용해야 합니다:

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
#### Query Exception 생성자

**영향 가능성: 매우 낮음(Very Low)**

`Illuminate\Database\QueryException`의 생성자는 이제 첫 번째 인수로 연결명(connection name, 문자열)을 받습니다. 애플리케이션에서 이 예외를 직접 던지고 있다면, 코드에 반영해야 합니다.

<a name="ulid-columns"></a>
#### ULID 컬럼

**영향 가능성: 낮음(Low)**

마이그레이션에서 `ulid` 메서드를 인수 없이 사용할 때, 이제 컬럼명이 `ulid`로 생성됩니다. 이전 Laravel 버전에서는 인수 없이 호출 시 잘못된 `uuid` 컬럼명이 생성되었습니다.

```
$table->ulid();
```

`ulid` 메서드에 원하는 컬럼명을 명시적으로 지정하려면, 아래처럼 이름을 전달하면 됩니다:

```
$table->ulid('ulid');
```

### Eloquent

<a name="model-dates-property"></a>
#### 모델 "dates" 속성

**영향 가능성: 중간(Medium)**

Eloquent 모델의 더 이상 사용되지 않는 `$dates` 속성이 제거되었습니다. 애플리케이션에서는 이제 `$casts` 속성을 사용해야 합니다:

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

### 로컬라이제이션(Localization)

<a name="language-directory"></a>
#### 언어 디렉터리

**영향 가능성: 없음(None)**

기존 애플리케이션에는 해당 사항이 없으나, 새로운 Laravel 애플리케이션에서는 더 이상 기본적으로 `lang` 디렉터리가 포함되지 않습니다. 신규 애플리케이션에서는 `lang:publish` Artisan 명령어로 언어 디렉터리를 생성할 수 있습니다:

```shell
php artisan lang:publish
```

### 로깅(Logging)

<a name="monolog-3"></a>
#### Monolog 3

**영향 가능성: 중간(Medium)**

Laravel의 Monolog 의존성이 Monolog 3.x로 업데이트되었습니다. 애플리케이션에서 Monolog를 직접 사용하고 있다면, Monolog의 [업그레이드 가이드](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md)를 반드시 확인하세요.

BugSnag, Rollbar 등과 같이, 서드파티 로깅 서비스를 사용하는 경우, Monolog 3.x와 Laravel 10.x를 지원하는 버전으로 해당 패키지를 업그레이드해야 할 수도 있습니다.

### 큐(Queues)

<a name="dispatch-now"></a>
#### `Bus::dispatchNow` 메서드

**영향 가능성: 낮음(Low)**

더 이상 사용되지 않는 `Bus::dispatchNow` 및 `dispatch_now` 메서드가 삭제되었습니다. 이제 `Bus::dispatchSync` 및 `dispatch_sync` 메서드를 각각 사용해야 합니다.

<a name="dispatch-return"></a>
#### `dispatch()` 헬퍼 반환값

**영향 가능성: 낮음(Low)**

이전에는 `Illuminate\Contracts\Queue`를 구현하지 않은 클래스를 `dispatch`로 호출하면, 해당 클래스의 `handle` 메서드 반환값이 반환되었습니다. 이제는 `Illuminate\Foundation\Bus\PendingBatch` 인스턴스를 반환합니다. 기존과 같은 동작을 원한다면 `dispatch_sync()`를 사용하면 됩니다.

### 라우팅(Routing)

<a name="middleware-aliases"></a>
#### 미들웨어 별칭(Middleware Alias)

**영향 가능성: 선택(Optional)**

신규 Laravel 애플리케이션에서는 `App\Http\Kernel` 클래스의 `$routeMiddleware` 속성이 `$middlewareAliases`로 이름이 변경되었습니다. 기존 애플리케이션에서도 원한다면 이 속성명을 변경할 수 있으나, 필수는 아닙니다.

<a name="rate-limiter-return-values"></a>
#### Rate Limiter 반환값

**영향 가능성: 낮음(Low)**

`RateLimiter::attempt` 메서드를 호출하면, 전달한 클로저의 반환값이 그대로 반환됩니다. 클로저에서 아무 값도 반환하지 않거나 `null`을 반환하면, `attempt` 메서드는 `true`를 반환합니다:

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
#### `Redirect::home` 메서드

**영향 가능성: 매우 낮음(Very Low)**

더 이상 사용되지 않는 `Redirect::home` 메서드가 삭제되었습니다. 대신, 명시적으로 지정한 라우트로 리다이렉트해야 합니다:

```php
return Redirect::route('home');
```

### 테스트(Testing)

<a name="service-mocking"></a>
#### 서비스 모킹(Service Mocking)

**영향 가능성: 중간(Medium)**

더 이상 사용되지 않는 `MocksApplicationServices` trait가 프레임워크에서 제거되었습니다. 이 trait는 `expectsEvents`, `expectsJobs`, `expectsNotifications`와 같은 테스트 메서드를 제공했습니다.

이러한 메서드를 사용하셨다면, 각각 `Event::fake`, `Bus::fake`, `Notification::fake`로 전환할 것을 권장합니다. 각 기능별로 'fake'를 사용하는 방법은 해당 구성요소의 공식 문서를 참고하세요.

### 유효성 검증(Validation)

<a name="closure-validation-rule-messages"></a>
#### 클로저 유효성 검증 규칙 메시지

**영향 가능성: 매우 낮음(Very Low)**

클로저 기반 커스텀 유효성 검증 규칙 작성 시, `$fail` 콜백을 여러 번 호출하면 이제 메시지가 배열에 추가(append)되고, 이전 메시지를 덮어쓰지 않습니다. 일반적으로 애플리케이션에는 영향이 없습니다.

또한, `$fail` 콜백이 객체를 반환하게 변경되었습니다. 이전에 유효성 검증 클로저의 반환 타입을 타입힌트했다면, 이에 맞춰 타입힌트도 업데이트해야 할 수 있습니다:

```php
public function rules()
{
    'name' => [
        function ($attribute, $value, $fail) {
            $fail('validation.translation.key')->translate();
        },
    ],
}
```

<a name="validation-messages-and-closure-rules"></a>
#### 유효성 검증 메시지와 클로저 규칙

**영향 가능성: 매우 낮음(Very Low)**

이전에는, 클로저 기반 유효성 검사 규칙에서 `$fail` 콜백에 배열을 전달하여 다른 키로 실패 메시지를 지정할 수 있었습니다. 이제는 첫 번째 인수로 키를, 두 번째 인수로 실패 메시지를 전달해야 합니다:

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
#### Form Request after 메서드

**영향 가능성: 매우 낮음(Very Low)**

Form Request 클래스 내 `after` 메서드는 이제 [Laravel에 예약됨](https://github.com/laravel/framework/pull/46757)으로 지정되어 있습니다. 만약 애플리케이션의 Form Request가 `after` 메서드를 정의하고 있다면, 메서드명을 변경하거나 Laravel의 새로운 "after validation" Form Request 기능을 활용하여 코드를 수정해야 합니다.

<a name="miscellaneous"></a>
### 기타(Miscellaneous)

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)를 참고하여 변경사항을 확인하는 것도 권장합니다. 이 변경사항의 상당수는 필수 사항이 아니며, 애플리케이션과 동기화하고 싶은 경우에만 적용하셔도 됩니다. 본 업그레이드 가이드에서 다루는 변경사항 외에도, 설정 파일 또는 주석과 같은 부분들은 별도로 다루지 않습니다.

[GitHub 비교 도구](https://github.com/laravel/laravel/compare/9.x...10.x)를 이용해 변경점을 손쉽게 확인하며, 필요한 업데이트만 선택적으로 적용할 수 있습니다. 다만, GitHub 비교에서 보이는 많은 변경사항은 PHP 네이티브 타입 채택과 관련되어 있으니, 이 변경사항들은 하위 호환성 문제를 일으키지 않아 Laravel 10으로 마이그레이션 시 필수는 아닙니다.
