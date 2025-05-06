# 오류 처리

- [소개](#introduction)
- [구성](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [Reportable 및 Renderable 예외](#renderable-exceptions)
- [보고된 예외 제한](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새 Laravel 프로젝트를 시작하면 오류 및 예외 처리가 이미 구성되어 있습니다. 애플리케이션에서 발생한 모든 예외는 `App\Exceptions\Handler` 클래스에서 로깅되고, 이후 사용자에게 렌더링됩니다. 이 문서 전체에서 이 클래스에 대해 더 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 구성

`config/app.php` 파일의 `debug` 옵션은 에러에 대한 정보가 실제로 사용자에게 얼마나 표시될지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 중에는 반드시 `APP_DEBUG` 환경 변수를 `true`로 지정해야 합니다. **운영 환경에서는 이 값이 반드시 `false`이어야 합니다. 운영 환경에서 이 값이 `true`로 설정되어 있으면, 애플리케이션의 최종 사용자에게 민감한 구성 값이 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러

<a name="reporting-exceptions"></a>
### 예외 보고

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리됩니다. 이 클래스에는 사용자 정의 예외 보고 및 렌더링 콜백을 등록할 수 있는 `register` 메서드가 포함되어 있습니다. 이 개념들을 자세히 살펴보겠습니다. 예외 보고는 예외를 로그로 남기거나 [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel)와 같은 외부 서비스로 전송할 때 사용됩니다. 기본적으로 예외는 애플리케이션의 [로그](/docs/{{version}}/logging) 구성에 따라 기록됩니다. 물론, 원하는 방식으로 예외를 기록할 수 있습니다.

예외의 종류에 따라 다르게 보고하려면 `reportable` 메서드를 사용하여 해당 타입의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 확인하여 어떤 예외를 보고할지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->reportable(function (InvalidOrderException $e) {
        // ...
    });
}
```

`reportable` 메소드를 사용해 사용자 정의 예외 보고 콜백을 등록해도, Laravel은 기본 로깅 설정에 따라 예외를 계속 기록합니다. 기본 로깅 스택으로 예외 전파를 중지하려면, 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

```php
$this->reportable(function (InvalidOrderException $e) {
    // ...
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!NOTE]  
> 특정 예외의 보고 방식 커스터마이징은 [reportable exceptions](/docs/{{version}}/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 글로벌 로그 컨텍스트

가능하다면, Laravel은 자동으로 현재 사용자 ID를 컨텍스트 데이터로 모든 예외 로그 메시지에 추가합니다. `App\Exceptions\Handler` 클래스에 `context` 메서드를 정의해 전역 컨텍스트 데이터를 지정할 수 있습니다. 이 정보는 애플리케이션에서 작성되는 모든 예외 로그 메시지에 포함됩니다:

```php
/**
 * Get the default context variables for logging.
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

모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 때로는 특정 예외만의 고유한 컨텍스트 정보를 로그에 포함하고 싶을 수 있습니다. 애플리케이션의 예외에 `context` 메서드를 정의함으로써, 해당 예외와 관련된 데이터를 로그 엔트리에 추가할 수 있습니다:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * Get the exception's context information.
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

때로는 예외를 보고만 하고, 현재 요청 처리는 그대로 계속하고 싶을 수 있습니다. `report` 헬퍼 함수는 에러 페이지를 렌더링하지 않고도, 예외를 예외 핸들러에 바로 보고할 수 있게 합니다:

```php
public function isValid(string $value): bool
{
    try {
        // 값을 검증...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 보고된 예외 중복 제거

애플리케이션 전역적으로 `report` 함수를 사용하다 보면, 동일한 예외를 여러 번 보고하는 경우가 있어 로그에 중복 항목이 발생할 수 있습니다.

하나의 예외 인스턴스가 한 번만 보고되게 하려면, `App\Exceptions\Handler` 클래스에서 `$withoutDuplicates` 프로퍼티를 `true`로 설정하세요:

```php
namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;

class Handler extends ExceptionHandler
{
    /**
     * Indicates that an exception instance should only be reported once.
     *
     * @var bool
     */
    protected $withoutDuplicates = true;

    // ...
}
```

이제 동일한 예외 인스턴스로 `report` 헬퍼를 호출할 때, 첫 번째 호출만 보고됩니다:

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

애플리케이션의 [로그](/docs/{{version}}/logging)에 메시지를 남길 때, 메시지는 지정한 [로그 레벨](/docs/{{version}}/logging#log-levels)로 기록되며, 이는 메시지의 중요도나 심각도를 나타냅니다.

위에서 설명한 것처럼 `reportable` 메서드로 사용자 정의 예외 보고 콜백을 등록해도, Laravel은 애플리케이션의 기본 로깅 설정에 따라 예외를 기록합니다. 하지만, 로그 레벨이 메시지가 기록되는 채널에 영향을 미칠 수 있으므로 특정 예외를 기록할 로그 레벨을 설정하고 싶을 수 있습니다.

이를 위해 예외 핸들러에 `$levels` 프로퍼티를 정의하면 됩니다. 이 프로퍼티는 예외 타입과 그에 해당하는 로그 레벨의 배열이어야 합니다:

```php
use PDOException;
use Psr\Log\LogLevel;

/**
 * A list of exception types with their corresponding custom log levels.
 *
 * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
 */
protected $levels = [
    PDOException::class => LogLevel::CRITICAL,
];
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 개발하다 보면, 절대 보고하지 않아도 되는 예외 타입이 있을 수 있습니다. 이런 예외를 무시하려면, 예외 핸들러에 `$dontReport` 프로퍼티를 정의하세요. 여기에 추가한 예외 클래스는 절대 보고되지 않습니다. 단, 커스텀 렌더링 로직은 계속 동작합니다:

```php
use App\Exceptions\InvalidOrderException;

/**
 * A list of the exception types that are not reported.
 *
 * @var array<int, class-string<\Throwable>>
 */
protected $dontReport = [
    InvalidOrderException::class,
];
```

Laravel은 내부적으로 이미 404 오류, 잘못된 CSRF 토큰으로 인한 419 응답 등 일부 오류를 자동으로 무시합니다. 무시를 해제하고 싶은 예외 타입이 있으면, 예외 핸들러의 `register` 메서드에서 `stopIgnoring` 메서드를 호출하면 됩니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->stopIgnoring(HttpException::class);

    // ...
}
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로, Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환합니다. 하지만, 원하는 예외 타입에 대해 사용자 정의 렌더링 클로저를 등록할 수 있습니다. 예외 핸들러에서 `renderable` 메서드를 사용하여 등록할 수 있습니다.

`renderable` 메서드에 넘기는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 참고해 어떤 예외를 렌더링할지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->renderable(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', [], 500);
    });
}
```

내장 Laravel 또는 Symfony 예외(e.g. `NotFoundHttpException`)의 렌더링도 `renderable` 메서드로 오버라이드할 수 있습니다. 만약 클로저가 값을 반환하지 않으면 Laravel의 기본 예외 렌더링 동작이 사용됩니다:

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Register the exception handling callbacks for the application.
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
### Reportable 및 Renderable 예외

예외 핸들러의 `register` 메서드에서 사용자 정의 보고 및 렌더링을 정의하는 대신, 애플리케이션의 예외 클래스에서 직접 `report` 및 `render` 메서드를 정의할 수도 있습니다. 이 메서드가 존재하면 프레임워크가 자동으로 호출합니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * Render the exception into an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 렌더링 가능한 예외(Laravel/Symfony 내장 예외 등)를 상속받는 경우, 예외 클래스의 `render` 메서드에서 `false`를 반환하면 해당 예외의 기본 HTTP 응답 렌더링이 사용됩니다:

```php
/**
 * Render the exception into an HTTP response.
 */
public function render(Request $request): Response|bool
{
    if (/** 커스텀 렌더링 필요 여부 판별 */) {
        return response(/* ... */);
    }

    return false;
}
```

예외에 특정 조건이 맞을 때만 필요한 커스텀 보고 로직이 포함되어 있다면, 예외의 `report` 메서드에서 `false`를 반환하여 기본 예외 처리 구성을 통해 예외를 보고하도록 할 수 있습니다:

```php
/**
 * Report the exception.
 */
public function report(): bool
{
    if (/** 커스텀 보고 필요 여부 판별 */) {
        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]  
> `report` 메서드의 의존성은 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 제한

애플리케이션에서 매우 많은 수의 예외가 보고되는 경우, 실제로 기록되거나 외부 오류 추적 서비스로 전송되는 예외의 수를 제한(트래픽 제한/throttle)할 수 있습니다.

예외를 무작위 샘플링하고 싶다면, 예외 핸들러 클래스에 `throttle` 메서드를 추가하고, 이 안에서 `Lottery` 인스턴스를 반환하면 됩니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    return Lottery::odds(1, 1000);
}
```

예외 타입에 따라 조건부로 샘플링하고 싶은 경우, 특정 예외 클래스만 `Lottery` 인스턴스를 반환하세요:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof ApiMonitoringException) {
        return Lottery::odds(1, 1000);
    }
}
```

로그로 기록되거나 외부 추적 서비스로 전송되는 예외에 대해, `Lottery` 대신 `Limit` 인스턴스를 반환하여 속도 제한(레이트 리밋)할 수도 있습니다. 이는 예를 들어 외부 서비스가 다운되어 예외가 폭주하는 경우 로그를 보호하는 데 유용합니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300);
    }
}
```

기본적으로, 제한 키는 예외 클래스명이 사용됩니다. `Limit`의 `by` 메서드로 직접 키를 지정해 커스터마이징할 수도 있습니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300)->by($e->getMessage());
    }
}
```

물론, 서로 다른 예외에 대해 `Lottery`와 `Limit`를 혼합해 반환할 수 있습니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
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

일부 예외는 서버의 HTTP 오류 코드와 관련이 있습니다. 예를 들어, "페이지를 찾을 수 없음"(404), "권한 없음"(401), 혹은 개발자가 명시적으로 발생시킨 500 오류일 수 있습니다. 이러한 응답을 애플리케이션의 어디서나 생성하려면, `abort` 헬퍼를 사용하세요:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 오류 페이지

Laravel에서는 다양한 HTTP 상태 코드를 위한 커스텀 오류 페이지를 손쉽게 정의할 수 있습니다. 예를 들어, 404 상태 코드의 오류 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하세요. 이 뷰는 애플리케이션에서 발생한 모든 404 오류에 렌더링됩니다. 이 디렉토리의 뷰들은 해당 HTTP 상태 코드와 일치하는 파일명이어야 합니다. `abort` 함수에 의해 발생된 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 오류 페이지 템플릿은 `vendor:publish` 아티즌 명령어로 배포할 수 있습니다. 템플릿을 배포한 후 원하는 대로 커스터마이즈하세요:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 오류 페이지

특정 HTTP 상태 코드가 발생했을 때 일치하는 페이지가 없으면, "폴백" 오류 페이지를 정의할 수도 있습니다. 이를 위해 애플리케이션의 `resources/views/errors` 디렉토리에 `4xx.blade.php` 및 `5xx.blade.php` 템플릿을 만들어 두세요.