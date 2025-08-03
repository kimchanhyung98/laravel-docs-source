# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [예외 유형별 무시하기](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 가능 및 렌더링 가능 예외](#renderable-exceptions)
- [보고된 예외 제한하기](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면, 에러 및 예외 처리가 이미 설정되어 있습니다. `App\Exceptions\Handler` 클래스는 애플리케이션에서 발생하는 모든 예외를 기록하고 사용자에게 렌더링하는 역할을 합니다. 이 문서 전반에 걸쳐 이 클래스에 대해 더 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일 내의 `debug` 옵션은 사용자에게 에러에 대한 정보를 얼마나 자세히 보여줄지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따르도록 되어 있습니다.

로컬 개발 시에는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 운영 환경에서 `true`로 설정하면 애플리케이션의 민감한 설정 값들이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러

<a name="reporting-exceptions"></a>
### 예외 보고

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리됩니다. 이 클래스에는 사용자 정의 예외 보고 및 렌더링 콜백을 등록할 수 있는 `register` 메서드가 포함되어 있습니다. 예외 보고는 예외를 로그에 남기거나 [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel) 같은 외부 서비스에 전송할 때 사용합니다. 기본적으로 예외는 [로깅](/docs/10.x/logging) 설정에 따라 기록됩니다. 하지만 예외 로그 기록은 자유롭게 커스터마이징 가능합니다.

예외 유형별로 다른 방식으로 보고해야 할 경우, `reportable` 메서드를 사용해 해당 예외 타입이 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 검사해 어떤 예외를 처리할지 결정합니다:

```
use App\Exceptions\InvalidOrderException;

/**
 * 애플리케이션의 예외 처리 콜백 등록.
 */
public function register(): void
{
    $this->reportable(function (InvalidOrderException $e) {
        // ...
    });
}
```

`reportable` 메서드를 통해 사용자 정의 예외 보고 콜백을 등록해도, Laravel은 기본 로깅 설정에 따라 여전히 예외를 기록합니다. 기본 로그 핸들러로의 전파를 중지하려면 콜백 내부에서 `stop` 메서드를 호출하거나 콜백에서 `false`를 반환하면 됩니다:

```
$this->reportable(function (InvalidOrderException $e) {
    // ...
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!NOTE]  
> 특정 예외에 대해 예외 보고를 커스터마이징하려면 [보고 가능한 예외(reportable exceptions)](/docs/10.x/errors#renderable-exceptions)도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

Laravel은 가능하면 현재 사용자의 ID를 모든 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. `App\Exceptions\Handler` 클래스에서 `context` 메서드를 정의하여 자신만의 전역 컨텍스트 데이터를 지정할 수도 있습니다. 이렇게 하면 이 정보가 애플리케이션에서 작성하는 모든 예외 로그 메시지에 포함됩니다:

```
/**
 * 로그를 위한 기본 컨텍스트 변수 반환.
 *
 * @return array<string, mixed>
 */
protected function context(): array
{
    return array_merge(parent::context(), [
        'foo' => 'bar',
    ]);
}
```

<a name="exception-log-context"></a>
#### 예외 로그 컨텍스트

모든 로그 메시지에 공통 컨텍스트를 추가하는 것이 유용할 수 있지만, 특정 예외에는 고유한 컨텍스트 데이터를 로그에 담고 싶을 때가 있습니다. 이럴 경우 애플리케이션의 특정 예외 클래스에 `context` 메서드를 정의해 해당 예외 관련 데이터를 로그에 추가할 수 있습니다:

```
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보 반환.
     *
     * @return array<string, mixed>
     */
    public function context(): array
    {
        return ['order_id' => $this->orderId];
    }
}
```

<a name="the-report-helper"></a>
#### `report` 헬퍼

때로는 예외를 보고만 하고 현재 요청 처리는 계속 진행해야 할 때가 있습니다. `report` 헬퍼 함수는 사용자에게 에러 페이지를 렌더링하지 않고도 신속하게 예외를 예외 핸들러를 통해 보고할 수 있게 해줍니다:

```
public function isValid(string $value): bool
{
    try {
        // 값 유효성 검사...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 중복 예외 보고 방지

애플리케이션 전체에서 `report` 함수를 여러 번 호출하면 동일한 예외가 여러 번 보고되어 로그가 중복될 수 있습니다.

예외 인스턴스가 단 한 번만 보고되도록 보장하고 싶다면, `App\Exceptions\Handler` 클래스에 `$withoutDuplicates` 속성을 `true`로 설정하세요:

```php
namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;

class Handler extends ExceptionHandler
{
    /**
     * 동일 예외 인스턴스는 한 번만 보고됨을 나타냄.
     *
     * @var bool
     */
    protected $withoutDuplicates = true;

    // ...
}
```

이제 동일한 예외 인스턴스를 `report` 헬퍼로 여러 번 호출해도 첫 호출만 보고됩니다:

```php
$original = new RuntimeException('Whoops!');

report($original); // 보고됨

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // 무시됨
}

report($original); // 무시됨
report($caught); // 무시됨
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨

애플리케이션의 [로그](/docs/10.x/logging)에 메시지가 작성될 때, 메시지는 지정된 [로그 레벨](/docs/10.x/logging#log-levels)로 기록되어 메시지의 심각도나 중요도를 나타냅니다.

앞서 설명한 것처럼 `reportable` 메서드로 사용자 정의 예외 보고 콜백을 등록해도 Laravel은 기본 로깅 설정에 따라 예외를 기록합니다. 하지만 로그 레벨에 따라 어떤 채널에 로그가 기록될지 결정될 수 있으므로, 특정 예외에 대해 로그 레벨을 설정하고 싶을 수 있습니다.

이를 위해 애플리케이션 예외 핸들러에 `$levels` 속성을 정의할 수 있습니다. 이 속성은 예외 클래스와 해당 로그 레벨을 매핑하는 배열이어야 합니다:

```
use PDOException;
use Psr\Log\LogLevel;

/**
 * 예외 유형별 사용자 정의 로그 레벨 목록.
 *
 * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
 */
protected $levels = [
    PDOException::class => LogLevel::CRITICAL,
];
```

<a name="ignoring-exceptions-by-type"></a>
### 예외 유형별 무시하기

애플리케이션을 개발할 때, 보고하지 않을 예외 유형이 존재할 수 있습니다. 이러한 예외를 무시하려면, 예외 핸들러에 `$dontReport` 속성을 정의하세요. 여기에 추가한 클래스는 예외 보고 대상에서 제외되지만, 사용자 정의 렌더링 로직은 여전히 유지할 수 있습니다:

```
use App\Exceptions\InvalidOrderException;

/**
 * 보고하지 않을 예외 유형 목록.
 *
 * @var array<int, class-string<\Throwable>>
 */
protected $dontReport = [
    InvalidOrderException::class,
];
```

Laravel 내부적으로도 404 HTTP 에러, 잘못된 CSRF 토큰으로 인한 419 응답 등 일부 예외 유형은 자동으로 무시합니다. 만약 Laravel이 무시하는 특정 예외 유형을 다시 보고하도록 지시하려면, 예외 핸들러의 `register` 메서드에서 `stopIgnoring` 메서드를 호출하면 됩니다:

```
use Symfony\Component\HttpKernel\Exception\HttpException;

/**
 * 애플리케이션의 예외 처리 콜백 등록.
 */
public function register(): void
{
    $this->stopIgnoring(HttpException::class);

    // ...
}
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해줍니다. 하지만 특정 예외 유형에 대해 사용자 정의 렌더링 클로저를 등록할 수 있습니다. 예외 핸들러의 `renderable` 메서드를 활용하면 됩니다.

`renderable` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼를 통해 응답을 생성할 수 있습니다. Laravel은 클로저 타입 힌트를 검사해 어떤 예외를 렌더링할지 결정합니다:

```
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

/**
 * 애플리케이션의 예외 처리 콜백 등록.
 */
public function register(): void
{
    $this->renderable(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', [], 500);
    });
}
```

`renderable` 메서드를 사용하면 Laravel 또는 Symfony 내장 예외(`NotFoundHttpException` 등)의 렌더링 동작도 재정의할 수 있습니다. 클로저가 값을 반환하지 않으면 Laravel 기본 예외 렌더링이 사용됩니다:

```
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * 애플리케이션의 예외 처리 콜백 등록.
 */
public function register(): void
{
    $this->renderable(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
}
```

<a name="renderable-exceptions"></a>
### 보고 가능 및 렌더링 가능 예외

예외 핸들러의 `register` 메서드가 아닌, 애플리케이션의 특정 예외 클래스 내에 `report` 메서드와 `render` 메서드를 직접 정의할 수도 있습니다. 이렇게 메서드가 존재하면 프레임워크가 자동으로 호출합니다:

```
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외 보고.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * HTTP 응답으로 예외 렌더링.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 렌더링 가능한 Laravel 또는 Symfony 내장 예외를 상속하는 경우, 예외의 기본 HTTP 응답을 렌더링하려면 `render` 메서드에서 `false`를 반환할 수 있습니다:

```
/**
 * HTTP 응답으로 예외 렌더링.
 */
public function render(Request $request): Response|bool
{
    if (/** 커스텀 렌더링이 필요하다고 판단 */) {

        return response(/* ... */);
    }

    return false;
}
```

특정 조건에서만 커스텀 보고가 필요한 경우에는, 기본 예외 처리 구성을 통해서도 때때로 예외를 보고하도록 하기 위해 `report` 메서드에서 `false`를 반환할 수 있습니다:

```
/**
 * 예외 보고.
 */
public function report(): bool
{
    if (/** 커스텀 보고가 필요하다고 판단 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]  
> `report` 메서드에 필요한 의존성을 타입 힌트로 지정하면 Laravel의 [서비스 컨테이너](/docs/10.x/container)가 자동으로 주입해줍니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 제한하기

애플리케이션에서 많은 수의 예외가 보고된다면, 실제로 로그에 기록되거나 외부 에러 추적 서비스에 전송되는 예외 수를 제한(throttle)하고 싶을 수 있습니다.

무작위 샘플링으로 예외를 제한하려면, 예외 핸들러 내 `throttle` 메서드에서 `Lottery` 인스턴스를 반환하면 됩니다. `App\Exceptions\Handler` 클래스에 해당 메서드가 없으면 새로 추가할 수도 있습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

/**
 * 들어오는 예외 제한 처리.
 */
protected function throttle(Throwable $e): mixed
{
    return Lottery::odds(1, 1000);
}
```

예외 타입에 따라 조건부 샘플링을 하고 싶으면 지정한 예외 클래스일 때만 `Lottery` 인스턴스를 반환하면 됩니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * 들어오는 예외 제한 처리.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof ApiMonitoringException) {
        return Lottery::odds(1, 1000);
    }
}
```

외부 에러 추적 서비스에 기록하거나 로그로 남기는 예외 수를 제한하기 위해 `Lottery` 대신 `Limit` 인스턴스를 반환할 수도 있습니다. 이는 예를 들어 서드파티 서비스 장애 등으로 예외가 급증하는 상황에서 로그 과부하를 방지하는 데 유용합니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * 들어오는 예외 제한 처리.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300);
    }
}
```

기본적으로 `Limit`는 예외 클래스명을 기준으로 제한 키(rate limit key)를 사용합니다. `by` 메서드를 사용해 임의의 키를 지정할 수도 있습니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * 들어오는 예외 제한 처리.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300)->by($e->getMessage());
    }
}
```

물론, 서로 다른 예외에 대해 `Lottery`와 `Limit` 인스턴스를 혼용해 반환하는 것도 가능합니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * 들어오는 예외 제한 처리.
 */
protected function throttle(Throwable $e): mixed
{
    return match (true) {
        $e instanceof BroadcastException => Limit::perMinute(300),
        $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
        default => Limit::none(),
    };
}
```

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버에서 발생한 HTTP 에러 코드를 나타냅니다. 예를 들어 “페이지를 찾을 수 없음” 에러(404), “인증되지 않음” 에러(401), 또는 개발자가 생성한 500 에러 등이 있습니다. 애플리케이션 어디에서든 이런 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 쉽게 보여줄 수 있도록 해줍니다. 예를 들어 404 HTTP 상태 코드 에러 페이지를 커스터마이징하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하세요. 이 뷰는 애플리케이션에서 발생한 모든 404 에러에 대해 렌더링됩니다. 이 디렉토리 내의 뷰 파일은 대응하는 HTTP 상태 코드 이름으로 파일명을 지정해야 합니다. `abort` 함수에 의해 발생하는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 뷰에 `$exception` 변수로 전달됩니다:

```
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿을 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있으며, 퍼블리시 후 자유롭게 수정 가능합니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체 HTTP 에러 페이지

특정 HTTP 상태 코드에 맞는 에러 페이지가 없을 때 렌더링되는 “대체(fallback)” 에러 페이지도 정의할 수 있습니다. 이를 위해 `resources/views/errors` 디렉토리 내에 `4xx.blade.php`와 `5xx.blade.php` 템플릿을 생성하세요. 이 페이지들은 해당 범위의 HTTP 에러 발생 시 사용됩니다.