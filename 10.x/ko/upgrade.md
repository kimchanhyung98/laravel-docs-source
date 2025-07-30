# 업그레이드 가이드 (Upgrade Guide)

- [9.x 버전에서 10.0 버전으로 업그레이드하기](#upgrade-10.0)

<a name="high-impact-changes"></a>
## 영향도가 큰 변경사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [최소 안정성 설정 업데이트](#updating-minimum-stability)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [데이터베이스 표현식](#database-expressions)
- [모델의 "Dates" 속성](#model-dates-property)
- [Monolog 3 버전](#monolog-3)
- [Redis 캐시 태그](#redis-cache-tags)
- [서비스 목킹](#service-mocking)
- [언어 디렉터리](#language-directory)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [클로저 기반 유효성 검증 규칙 메시지](#closure-validation-rule-messages)
- [폼 요청의 `after` 메서드](#form-request-after-method)
- [퍼블릭 경로 바인딩](#public-path-binding)
- [쿼리 예외 생성자](#query-exception-constructor)
- [레이트 리미터 반환 값](#rate-limiter-return-values)
- [`Redirect::home` 메서드](#redirect-home)
- [`Bus::dispatchNow` 메서드](#dispatch-now)
- [`registerPolicies` 메서드](#register-policies)
- [ULID 컬럼](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## 9.x 버전에서 10.0 버전으로 업그레이드하기 (Upgrading to 10.0 from 9.x)

<a name="estimated-upgrade-time-??-minutes"></a>
#### 예상 업그레이드 시간: 10분

> [!NOTE]  
> 모든 잠재적 호환성 깨짐(브레이킹) 변경사항을 문서화하려 노력하고 있습니다. 그러나 일부 변경사항은 프레임워크의 덜 알려진 부분에만 영향을 미치므로 실제 애플리케이션에는 일부만 영향이 있을 수 있습니다. 시간을 절약하고 싶다면 [Laravel Shift](https://laravelshift.com/)를 사용해 자동으로 업그레이드를 도울 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

#### PHP 8.1.0 이상 필수

Laravel은 이제 PHP 8.1.0 이상을 요구합니다.

#### Composer 2.2.0 이상 필수

Laravel은 이제 [Composer](https://getcomposer.org) 2.2.0 이상을 요구합니다.

#### Composer 의존성

애플리케이션의 `composer.json` 파일에 다음 의존성들을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework` 버전 `^10.0`
- `laravel/sanctum` 버전 `^3.2`
- `doctrine/dbal` 버전 `^3.0`
- `spatie/laravel-ignition` 버전 `^2.0`
- `laravel/passport` 버전 `^11.0` ([업그레이드 가이드](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` 버전 `^4.0`

</div>

Sanctum 2.x에서 3.x로 업그레이드하는 경우, [Sanctum 업그레이드 가이드](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md)를 참고하세요.

또한 PHPUnit 10을 사용하려면, 애플리케이션의 `phpunit.xml` 설정 파일 `<coverage>` 섹션에서 `processUncoveredFiles` 속성을 삭제해야 합니다. 그리고 다음 의존성들을 업데이트하세요:

<div class="content-list" markdown="1">

- `nunomaduro/collision` 버전 `^7.0`
- `phpunit/phpunit` 버전 `^10.0`

</div>

마지막으로, 애플리케이션에서 사용하는 다른 서드파티 패키지들도 검토하여 Laravel 10 지원 버전을 사용 중인지 확인하세요.

<a name="updating-minimum-stability"></a>
#### 최소 안정성 설정 (Minimum Stability)

애플리케이션의 `composer.json` 파일에서 `minimum-stability` 설정을 `stable`로 변경하세요. 또는 기본값이 이미 `stable`이므로 해당 설정을 삭제해도 됩니다:

```json
"minimum-stability": "stable",
```

### 애플리케이션

<a name="public-path-binding"></a>
#### 퍼블릭 경로 바인딩 (Public Path Binding)

**영향 가능성: 낮음**

애플리케이션이 컨테이너에 `path.public` 을 바인딩하여 "퍼블릭 경로"를 사용자 정의하고 있다면, 대신 `Illuminate\Foundation\Application` 객체의 `usePublicPath` 메서드를 호출하도록 코드를 변경해야 합니다:

```php
app()->usePublicPath(__DIR__.'/public');
```

### 권한(Authorization)

<a name="register-policies"></a>
### `registerPolicies` 메서드

**영향 가능성: 낮음**

`AuthServiceProvider`의 `registerPolicies` 메서드는 이제 프레임워크에서 자동으로 호출됩니다. 따라서 애플리케이션의 `AuthServiceProvider` `boot` 메서드에서 이 메서드 호출을 제거할 수 있습니다.

### 캐시(Cache)

<a name="redis-cache-tags"></a>
#### Redis 캐시 태그

**영향 가능성: 중간**

`Cache::tags()` 사용은 Memcached를 사용하는 애플리케이션에만 권장됩니다. 애플리케이션이 Redis를 캐시 드라이버로 사용한다면, Memcached로 전환하거나 다른 대안을 고려해야 합니다.

### 데이터베이스(Database)

<a name="database-expressions"></a>
#### 데이터베이스 표현식 (Database Expressions)

**영향 가능성: 중간**

Laravel 10.x에서 데이터베이스 "표현식"(대부분 `DB::raw`로 생성)은 앞으로 추가 기능을 지원하도록 재작성되었습니다. 특히, 표현식의 원시 문자열 값은 이제 `getValue(Grammar $grammar)` 메서드를 통해서만 얻어야 합니다. `(string)` 형 변환으로 표현식을 직접 변환하는 것은 더 이상 지원되지 않습니다.

**보통 최종 사용자 애플리케이션에 영향이 없으나**, 만약 애플리케이션에서 데이터베이스 표현식을 `(string)`으로 강제 변환하거나 `__toString`을 직접 호출한다면, 코드를 아래와 같이 `getValue` 메서드를 호출하도록 변경해야 합니다:

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
#### 쿼리 예외 생성자 (Query Exception Constructor)

**영향 가능성: 매우 낮음**

`Illuminate\Database\QueryException` 생성자는 이제 첫 번째 인수로 문자열 형태의 커넥션 이름을 받습니다. 만약 애플리케이션에서 이 예외를 수동으로 던지고 있다면, 코드를 이에 맞게 조정해야 합니다.

<a name="ulid-columns"></a>
#### ULID 컬럼

**영향 가능성: 낮음**

마이그레이션 시 `ulid` 메서드를 인자 없이 호출하면 이제 컬럼 이름이 `ulid`가 됩니다. 이전 Laravel 버전에서는 인자를 주지 않으면 잘못하여 `uuid` 컬럼이 생성되었습니다:

```
$table->ulid();
```

별도의 컬럼명을 지정하려면 다음과 같이 인자로 이름을 명시할 수 있습니다:

```
$table->ulid('ulid');
```

### 엘로퀀트(Eloquent)

<a name="model-dates-property"></a>
#### 모델의 "Dates" 속성

**영향 가능성: 중간**

Eloquent 모델의 더 이상 권장되지 않는 `$dates` 속성이 제거되었습니다. 애플리케이션은 이제 `$casts` 속성을 사용해야 합니다:

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

### 지역화(Localization)

<a name="language-directory"></a>
#### 언어 디렉터리

**영향 가능성: 없음**

기존 애플리케이션과 무관하게, Laravel 애플리케이션 스켈레톤은 기본적으로 `lang` 디렉터리를 포함하지 않습니다. 새로운 애플리케이션을 작성할 때는 `lang:publish` Artisan 명령어로 언어 파일을 게시할 수 있습니다:

```shell
php artisan lang:publish
```

### 로깅(Logging)

<a name="monolog-3"></a>
#### Monolog 3

**영향 가능성: 중간**

Laravel의 Monolog 의존성이 Monolog 3.x로 업데이트되었습니다. 애플리케이션에서 Monolog를 직접 다룬다면 Monolog의 [업그레이드 가이드](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md)를 검토하세요.

BugSnag, Rollbar 같은 서드파티 로깅 서비스를 쓴다면, 이들 패키지 또한 Monolog 3.x 및 Laravel 10.x 지원 버전으로 업그레이드가 필요할 수 있습니다.

### 큐(Queues)

<a name="dispatch-now"></a>
#### `Bus::dispatchNow` 메서드

**영향 가능성: 낮음**

더 이상 권장되지 않는 `Bus::dispatchNow` 및 `dispatch_now` 메서드가 제거되었습니다. 대신 `Bus::dispatchSync` 및 `dispatch_sync` 메서드를 사용해야 합니다.

<a name="dispatch-return"></a>
#### `dispatch()` 헬퍼 반환 값

**영향 가능성: 낮음**

`Illuminate\Contracts\Queue`를 구현하지 않은 클래스를 `dispatch`로 호출할 경우, 이전에는 해당 클래스의 `handle` 메서드 결과가 반환되었습니다. 이제는 `Illuminate\Foundation\Bus\PendingBatch` 인스턴스를 반환합니다. 이전 동작이 필요하다면 `dispatch_sync()`를 사용하세요.

### 라우팅(Routing)

<a name="middleware-aliases"></a>
#### 미들웨어 별칭(Middleware Aliases)

**영향 가능성: 선택적**

새 Laravel 애플리케이션에서는 `App\Http\Kernel` 클래스의 `$routeMiddleware` 속성이 역할을 더 잘 반영하도록 `$middlewareAliases`로 이름이 변경되었습니다. 기존 애플리케이션에서도 원한다면 이름을 변경할 수 있지만 필수 사항은 아닙니다.

<a name="rate-limiter-return-values"></a>
#### 레이트 리미터 반환값 (Rate Limiter Return Values)

**영향 가능성: 낮음**

`RateLimiter::attempt` 메서드를 호출할 때, 전달한 클로저가 반환한 값이 이제 그대로 반환됩니다. 만약 아무 값도 반환하지 않거나 `null`을 반환하면, `attempt` 메서드는 `true`를 반환합니다:

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
#### `Redirect::home` 메서드

**영향 가능성: 매우 낮음**

더 이상 권장되지 않는 `Redirect::home` 메서드가 제거되었습니다. 대신 명시적으로 이름이 지정된 라우트로 리다이렉트해야 합니다:

```php
return Redirect::route('home');
```

### 테스트(Testing)

<a name="service-mocking"></a>
#### 서비스 목킹(Service Mocking)

**영향 가능성: 중간**

더 이상 권장되지 않는 `MocksApplicationServices` 트레이트가 프레임워크에서 제거되었습니다. 해당 트레이트는 `expectsEvents`, `expectsJobs`, `expectsNotifications` 같은 테스트 메서드를 제공했습니다.

이 메서드들을 사용하는 경우 각각 `Event::fake`, `Bus::fake`, `Notification::fake`로 전환할 것을 권장합니다. 목킹할 컴포넌트의 문서에서 가짜(fakes)를 활용하는 방법을 확인할 수 있습니다.

### 유효성 검증(Validation)

<a name="closure-validation-rule-messages"></a>
#### 클로저 유효성 검증 규칙 메시지

**영향 가능성: 매우 낮음**

클로저 기반 사용자 정의 유효성 검증 규칙에서, `$fail` 콜백을 여러 번 호출하면 이제 메시지가 덮어쓰지 않고 배열로 추가됩니다. 보통은 애플리케이션에 영향을 미치지 않습니다.

또한 `$fail` 콜백이 이제 객체를 반환합니다. 만약 클로저 반환 타입을 명시적으로 선언했다면, 타입 힌트를 수정해야 할 수 있습니다:

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
#### 유효성 메시지와 클로저 규칙

**영향 가능성: 매우 낮음**

이전에는 클로저 기반 유효성 검증 규칙의 `$fail` 콜백에 배열을 전달하여 다른 키에 실패 메시지를 지정할 수 있었습니다. 이제는 첫 번째 인수로 키, 두 번째 인수로 실패 메시지를 전달해야 합니다:

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
#### 폼 요청의 `after` 메서드

**영향 가능성: 매우 낮음**

폼 요청에서 `after` 메서드는 Laravel에서 예약어가 되었습니다. 만약 폼 요청에 `after` 메서드가 정의되어 있다면, 이름을 바꾸거나 Laravel 폼 요청의 "유효성 검사 후" 기능을 활용하도록 수정해야 합니다.

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경사항도 확인하는 것을 권장합니다. 많은 변경사항은 필수가 아니지만, 설정 파일이나 주석 업데이트 등 일부를 애플리케이션과 동기화하면 좋습니다. 이 가이드에서 다루는 내용도 있으며, 그렇지 않은 부분도 있습니다.

[GitHub 비교 도구](https://github.com/laravel/laravel/compare/9.x...10.x)를 사용해 쉽게 변경사항을 확인하고 필요한 업데이트만 반영할 수 있습니다. 다만 GitHub 비교 도구에 나타나는 많은 변경은 PHP 기본 타입 도입 때문이며, 이는 하위 호환성을 유지하며 Laravel 10 마이그레이션 시 선택사항입니다.