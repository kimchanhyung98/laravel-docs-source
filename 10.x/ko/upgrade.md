# 업그레이드 가이드

- [9.x에서 10.0으로 업그레이드](#upgrade-10.0)

<a name="high-impact-changes"></a>
## 주요 영향 변경사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [최소 안정성 업데이트](#updating-minimum-stability)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경사항

<div class="content-list" markdown="1">

- [데이터베이스 표현식](#database-expressions)
- [모델 "Dates" 프로퍼티](#model-dates-property)
- [Monolog 3](#monolog-3)
- [Redis 캐시 태그](#redis-cache-tags)
- [서비스 Mocking](#service-mocking)
- [언어 디렉터리](#language-directory)

</div>

<a name="low-impact-changes"></a>
## 낮은 영향 변경사항

<div class="content-list" markdown="1">

- [클로저 유효성 검사 규칙 메시지](#closure-validation-rule-messages)
- [폼 리퀘스트 `after` 메서드](#form-request-after-method)
- [public 경로 바인딩](#public-path-binding)
- [쿼리 예외 생성자](#query-exception-constructor)
- [Rate Limiter 반환값](#rate-limiter-return-values)
- [`Redirect::home` 메서드](#redirect-home)
- [`Bus::dispatchNow` 메서드](#dispatch-now)
- [`registerPolicies` 메서드](#register-policies)
- [ULID 컬럼](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## 9.x에서 10.0으로 업그레이드

<a name="estimated-upgrade-time-??-minutes"></a>
#### 예상 소요 시간: 10분

> [!NOTE]  
> 모든 잠재적인 브레이킹 체인지를 문서화하고자 노력했습니다. 일부 변경 사항은 프레임워크의 잘 알려지지 않은 부분에 적용되므로 실제로는 일부가 여러분의 애플리케이션에만 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용해 자동으로 업그레이드를 도와줄 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

#### PHP 8.1.0 요구

이제 Laravel은 PHP 8.1.0 이상이 필요합니다.

#### Composer 2.2.0 요구

이제 Laravel은 [Composer](https://getcomposer.org) 2.2.0 이상이 필요합니다.

#### Composer 의존성

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^10.0`으로
- `laravel/sanctum`을 `^3.2`로
- `doctrine/dbal`을 `^3.0`으로
- `spatie/laravel-ignition`을 `^2.0`으로
- `laravel/passport`를 `^11.0`으로 ([업그레이드 가이드](https://github.com/laravel/passport/blob/11.x/UPGRADE.md) 참고)
- `laravel/ui`를 `^4.0`으로

</div>

Sanctum 2.x에서 3.x로 업그레이드하는 경우, [Sanctum 업그레이드 가이드](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md)를 참고하세요.

또한, [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html)을 사용하려면 애플리케이션의 `phpunit.xml` 파일의 `<coverage>` 섹션에서 `processUncoveredFiles` 속성을 삭제해야 합니다. 그리고 다음 의존성도 `composer.json`에서 업데이트하세요:

<div class="content-list" markdown="1">

- `nunomaduro/collision`을 `^7.0`으로
- `phpunit/phpunit`을 `^10.0`으로

</div>

마지막으로, 애플리케이션에서 사용하는 기타 타사 패키지도 모두 검토하여 Laravel 10을 지원하는 올바른 버전을 사용하는지 확인하세요.

<a name="updating-minimum-stability"></a>
#### 최소 안정성

애플리케이션의 `composer.json` 파일에서 `minimum-stability` 설정을 `stable`로 업데이트하십시오. 또는, 기본값이 이미 `stable`이므로 이 설정을 파일에서 삭제해도 됩니다:

```json
"minimum-stability": "stable",
```

### 어플리케이션

<a name="public-path-binding"></a>
#### public 경로 바인딩

**영향 가능성: 낮음**

애플리케이션에서 `path.public`을 컨테이너에 바인딩하여 public 경로를 커스텀하는 경우, 이제 `Illuminate\Foundation\Application` 객체에서 제공하는 `usePublicPath` 메서드를 사용해야 합니다:

```php
app()->usePublicPath(__DIR__.'/public');
```

### 인증

<a name="register-policies"></a>
### `registerPolicies` 메서드

**영향 가능성: 낮음**

`AuthServiceProvider`의 `registerPolicies` 메서드는 이제 프레임워크가 자동으로 호출합니다. 따라서 애플리케이션의 `AuthServiceProvider`에서 이 메서드 호출을 `boot` 메서드에서 제거할 수 있습니다.

### 캐시

<a name="redis-cache-tags"></a>
#### Redis 캐시 태그

**영향 가능성: 중간**

`Cache::tags()` 사용은 Memcached를 사용하는 애플리케이션에만 권장됩니다. 애플리케이션의 캐시 드라이버로 Redis를 사용 중이라면, Memcached로 이동하거나 대체 솔루션을 고려하세요.

### 데이터베이스

<a name="database-expressions"></a>
#### 데이터베이스 표현식

**영향 가능성: 중간**

데이터베이스 "표현식"(`DB::raw`로 생성되는 경우가 많음)이 Laravel 10.x에서 추가 기능을 제공할 수 있도록 재작성되었습니다. 주목할 점은, 이제 원시 문자열 값은 해당 표현식의 `getValue(Grammar $grammar)` 메서드를 통해 가져와야 합니다. `(string)`으로 표현식을 문자열로 강제 변환하는 것은 더 이상 지원하지 않습니다.

**일반적으로 최종 사용자 애플리케이션에는 영향이 없습니다**. 하지만, 애플리케이션에서 표현식을 `(string)`으로 변환하거나 `__toString` 메서드를 직접 호출하는 경우, 코드에서 대신 `getValue` 메서드를 호출하도록 업데이트해야 합니다:

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
#### 쿼리 예외 생성자

**영향 가능성: 매우 낮음**

`Illuminate\Database\QueryException` 생성자는 이제 첫 번째 인수로 문자열 커넥션 이름을 받습니다. 이 예외를 직접 발생시키는 경우 코드에서 이에 맞게 인수를 조정해야 합니다.

<a name="ulid-columns"></a>
#### ULID 컬럼

**영향 가능성: 낮음**

마이그레이션에서 `ulid` 메서드를 아무 인자 없이 호출하면 이제 컬럼 이름이 `ulid`로 생성됩니다. 이전 릴리스에서는 인자 없이 호출 시 잘못하여 `uuid`로 생성되었습니다:

    $table->ulid();

`ulid` 메서드를 호출할 때 명시적으로 컬럼 이름을 지정하려면, 컬럼명을 인자로 전달하세요:

    $table->ulid('ulid');

### Eloquent

<a name="model-dates-property"></a>
#### 모델 "Dates" 프로퍼티

**영향 가능성: 중간**

Eloquent 모델의 더 이상 사용되지 않는 `$dates` 프로퍼티가 제거되었습니다. 이제 명시적으로 `$casts` 프로퍼티를 사용해야 합니다:

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

### 로컬라이제이션

<a name="language-directory"></a>
#### 언어 디렉터리

**영향 가능성: 없음**

기존 애플리케이션에는 해당되지 않지만, Laravel 기본 스켈레톤에서는 이제 기본적으로 `lang` 디렉터리를 포함하지 않습니다. 새 Laravel 애플리케이션을 작성할 때는 `lang:publish` Artisan 명령어로 공개할 수 있습니다:

```shell
php artisan lang:publish
```

### 로깅

<a name="monolog-3"></a>
#### Monolog 3

**영향 가능성: 중간**

Laravel의 Monolog 의존성이 Monolog 3.x로 업데이트되었습니다. 애플리케이션에서 Monolog을 직접 다루는 경우 Monolog의 [업그레이드 가이드](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md)를 참고하세요.

BugSnag, Rollbar 등 서드 파티 로깅 서비스를 사용하는 경우 Monolog 3.x 및 Laravel 10.x를 지원하는 버전으로 해당 패키지를 업그레이드해야 할 수 있습니다.

### 큐

<a name="dispatch-now"></a>
#### `Bus::dispatchNow` 메서드

**영향 가능성: 낮음**

더 이상 사용되지 않는 `Bus::dispatchNow` 및 `dispatch_now` 메서드가 제거되었습니다. 대신 각각 `Bus::dispatchSync` 및 `dispatch_sync` 메서드를 사용하세요.

<a name="dispatch-return"></a>
#### `dispatch()` 헬퍼 반환값

**영향 가능성: 낮음**

이전에는 `Illuminate\Contracts\Queue`를 구현하지 않은 클래스로 `dispatch`를 호출하면 해당 클래스의 `handle` 메서드 결과가 반환되었습니다. 이제는 `Illuminate\Foundation\Bus\PendingBatch` 인스턴스가 반환됩니다. 기존 동작을 재현하려면 `dispatch_sync()`를 사용하세요.

### 라우팅

<a name="middleware-aliases"></a>
#### 미들웨어 별칭

**영향 가능성: 선택적**

새로운 Laravel 애플리케이션에서는 `App\Http\Kernel` 클래스의 `$routeMiddleware` 프로퍼티가 `$middlewareAliases`로 변경되었습니다. 기존 애플리케이션에서도 원한다면 이름을 변경해도 되지만, 필수는 아닙니다.

<a name="rate-limiter-return-values"></a>
#### Rate Limiter 반환값

**영향 가능성: 낮음**

`RateLimiter::attempt` 메서드를 호출하면, 이제 클로저가 반환한 값이 메서드의 반환값이 됩니다. 아무 값도 반환하지 않거나 `null`을 반환하면 메서드는 `true`를 반환합니다:

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
#### `Redirect::home` 메서드

**영향 가능성: 매우 낮음**

더 이상 사용되지 않는 `Redirect::home` 메서드가 제거되었습니다. 대신 명명된 경로로 명시적으로 리디렉션하세요:

```php
return Redirect::route('home');
```

### 테스트

<a name="service-mocking"></a>
#### 서비스 Mocking

**영향 가능성: 중간**

더 이상 사용되지 않는 `MocksApplicationServices` 트레이트가 프레임워크에서 제거되었습니다. 이 트레이트는 `expectsEvents`, `expectsJobs`, `expectsNotifications`와 같은 테스트 메서드를 제공했습니다.

해당 메서드를 사용하는 경우, 각각 `Event::fake`, `Bus::fake`, `Notification::fake`로 전환하는 것을 권장합니다. 페이크(mock)를 이용한 테스트 방법은 관련 컴포넌트의 공식 문서를 참고하세요.

### 유효성 검사

<a name="closure-validation-rule-messages"></a>
#### 클로저 유효성 검사 규칙 메시지

**영향 가능성: 매우 낮음**

클로저 기반 커스텀 유효성 검사 규칙을 작성할 때, `$fail` 콜백을 여러 번 호출하면 이제 메시지를 배열로 누적하며, 이전 메시지를 덮어쓰지 않습니다. 일반적으로는 애플리케이션에 영향이 없습니다.

또한, `$fail` 콜백이 이제 객체를 반환합니다. 이전에 유효성 검사 클로저의 반환 타입에 타입힌트를 사용했다면, 이를 업데이트해야 할 수 있습니다:

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
#### 유효성 검사 메시지와 클로저 규칙

**영향 가능성: 매우 낮음**

기존에는 배열을 `$fail` 콜백에 전달하여 다른 키에 실패 메시지를 할당할 수 있었습니다. 이제는 첫 번째 인자로 키, 두 번째 인자로 실패 메시지를 전달해야 합니다:

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
#### 폼 리퀘스트 After 메서드

**영향 가능성: 매우 낮음**

폼 리퀘스트 내에서 Laravel에서 [예약된 after 메서드](https://github.com/laravel/framework/pull/46757)를 사용할 수 있습니다. 리퀘스트에서 `after` 메서드를 정의하고 있다면, 메서드 이름을 변경하거나 Laravel의 새로운 "유효성 검사 후" 기능을 이용해 수정해야 합니다.

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경사항도 살펴보는 것을 권장합니다. 많은 변경사항이 반드시 필요한 것은 아니지만, 애플리케이션의 파일을 최신 상태로 유지하기 위해 참조할 수 있습니다. 이 업그레이드 가이드에서 다루지 않는 구성 파일이나 주석 변경 등도 있습니다.

[GitHub 비교 도구](https://github.com/laravel/laravel/compare/9.x...10.x)를 사용하면 쉽게 변경사항을 확인하고 필요한 변경만 선택할 수 있습니다. 다만, GitHub 비교 도구에서 표시되는 많은 변경사항은 PHP 네이티브 타입 채택 때문입니다. 이 변경들은 하위 호환성을 유지하며, Laravel 10으로 마이그레이션할 때 반드시 적용하지 않아도 됩니다.