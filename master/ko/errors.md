# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
- [예외 보고 제한(Throttling)](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면, 에러 및 예외 처리가 이미 기본적으로 설정되어 있습니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용하여 예외가 어떻게 보고(report)되고 렌더(render)될지 직접 관리할 수 있습니다.

`withExceptions` 클로저에 전달되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션에서 예외 처리를 담당합니다. 본 문서에서는 이 객체를 더욱 자세히 살펴봅니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일에 있는 `debug` 옵션은 사용자에게 노출되는 에러 정보의 상세 정도를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 반드시 `false`로 유지해야 합니다. 만약 운영 환경에서 `true`로 두면 민감한 환경설정 정보가 애플리케이션의 최종 사용자에게 노출될 수 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서는 예외 보고를 통해 예외를 로그로 남기거나, [Sentry](https://github.com/getsentry/sentry-laravel)나 [Flare](https://flareapp.io)와 같은 외부 서비스로 전송할 수 있습니다. 기본적으로, 예외는 [로그 설정](/docs/master/logging)에 따라 기록됩니다. 물론 원하는 방식으로 예외를 기록할 수도 있습니다.

다양한 종류의 예외를 각각 다르게 보고할 필요가 있다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드를 사용해 특정 타입의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 통해 어떤 예외를 처리해야 할지 판단합니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드로 커스텀 예외 보고 콜백을 등록하면, Laravel은 여전히 기본 로그 설정에 따라 예외를 기록합니다. 만약 기본 로그 흐름으로 예외가 전달되지 않도록 하려면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```

> [!NOTE]
> 특정 예외에 대한 예외 보고 방식을 커스터마이즈하려면 [보고 및 렌더링 가능한 예외](/docs/master/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

가능하다면, Laravel은 현재 사용자 ID를 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. `bootstrap/app.php` 파일의 `context` 예외 메서드를 사용해 자체 전역 컨텍스트 데이터를 정의할 수 있습니다. 해당 정보는 애플리케이션이 기록한 모든 예외 로그 메시지에 포함됩니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 특정 예외에만 고유한 컨텍스트를 추가하고 싶을 때가 있습니다. 애플리케이션의 예외 클래스에 `context` 메서드를 정의하면, 해당 예외에 관련된 데이터를 예외의 로그 항목에 추가할 수 있습니다.

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보를 반환
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

때로는 예외를 보고(report)만 하고, 현재 요청 처리를 계속 진행하고 싶을 수 있습니다. `report` 헬퍼 함수는 사용자에게 에러 페이지를 렌더링하지 않고 신속하게 예외를 보고할 수 있게 해줍니다.

```php
public function isValid(string $value): bool
{
    try {
        // 값 유효성 검증...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 중복 예외 보고 방지

애플리케이션 곳곳에서 `report` 함수를 사용하면 동일한 예외 인스턴스가 여러 번 보고되어 로그에 중복 항목이 생길 수 있습니다.

같은 예외 인스턴스가 단 한 번만 보고되도록 하고 싶다면, `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출하면 됩니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스로 `report` 헬퍼가 호출되면, 최초 1회만 보고됩니다.

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

애플리케이션의 [로그](/docs/master/logging)에 메시지가 기록될 때, 해당 메시지는 [로그 레벨](/docs/master/logging#log-levels)에 따라 중요도(심각도)가 결정됩니다.

앞서 언급했듯, `report` 메서드로 커스텀 예외 보고 콜백을 등록하더라도 Laravel은 여전히 기본 로그 설정에 따라 예외를 기록합니다. 하지만 로그 레벨에 따라 기록되는 로그 채널이 다를 수 있으므로, 특정 예외가 어떤 레벨로 기록될지 지정하고 싶을 수 있습니다.

이럴 때는 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용하면 됩니다. 이 메서드는 첫 번째 인수로 예외 타입, 두 번째 인수로 로그 레벨을 받습니다.

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 개발하다 보면 일부 예외 타입은 아예 보고하고 싶지 않을 수 있습니다. 이런 예외들은 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용해 무시할 수 있습니다. 이 메서드에 전달한 클래스는 절대 보고되지 않지만, 별도의 렌더링 로직은 여전히 가질 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또 다른 방법으로, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현(implements)해 '마크' 할 수도 있습니다. 이 인터페이스가 적용된 경우, 해당 예외는 Laravel의 예외 처리기에서 절대 보고되지 않습니다.

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Contracts\Debug\ShouldntReport;

class PodcastProcessingException extends Exception implements ShouldntReport
{
    //
}
```

특정 타입의 예외에 대해 더욱 세밀한 제어가 필요하다면, `dontReportWhen` 메서드에 클로저를 전달해 조건부로 예외 무시 여부를 결정할 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```

Laravel은 내부적으로도 이미 일부 예외 타입(예: 404 HTTP 에러나 잘못된 CSRF 토큰의 419 응답 등)은 자동으로 무시하고 있습니다. 이런 예외를 더 이상 무시하지 않도록 하려면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다.

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel의 예외 처리기는 예외를 HTTP 응답으로 변환합니다. 하지만 특정 타입의 예외에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. `bootstrap/app.php` 파일의 `render` 예외 메서드를 사용하면 됩니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 보고 어떤 예외를 렌더링할지 판단합니다.

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

또한, `render` 메서드를 사용해 Laravel이나 Symfony의 기본 예외(`NotFoundHttpException` 등)에 대한 렌더링 동작을 오버라이드할 수도 있습니다. 만약 전달한 렌더 클로저에서 값을 반환하지 않으면, Laravel의 기본 예외 렌더링 방식이 활용됩니다.

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
})
```

<a name="rendering-exceptions-as-json"></a>
#### 예외를 JSON으로 렌더링

예외를 렌더링할 때, Laravel은 요청의 `Accept` 헤더 값을 참고해 HTML 또는 JSON 응답 중 어느 쪽으로 렌더링할지 자동으로 결정합니다. 만약 이 판단 방식을 커스터마이즈하고 싶다면, `shouldRenderJsonWhen` 메서드를 이용할 수 있습니다.

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```

<a name="customizing-the-exception-response"></a>
#### 예외 응답 커스터마이징

아주 드물게, Laravel의 예외 처리기가 렌더하는 전체 HTTP 응답을 완전히 커스터마이즈할 필요가 있을 수 있습니다. 이때는 `respond` 메서드를 사용해 응답 커스터마이징 클로저를 등록할 수 있습니다.

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
})
```

<a name="renderable-exceptions"></a>
### 보고 및 렌더링 가능한 예외

`bootstrap/app.php` 파일에서 커스텀 보고 및 렌더링 동작을 정의하는 대신, 해당 예외 클래스에 직접 `report`와 `render` 메서드를 정의할 수도 있습니다. 이 메서드들이 존재하면, 프레임워크가 자동으로 호출합니다.

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외 보고
     */
    public function report(): void
    {
        // ...
    }

    /**
     * 예외를 HTTP 응답으로 렌더
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 renderer를 지원하는 예외(예: Laravel 또는 Symfony의 기본 예외)를 상속받았다면, 예외의 `render` 메서드에서 `false`를 반환해 기본 HTTP 응답을 렌더할 수 있습니다.

```php
/**
 * 예외를 HTTP 응답으로 렌더.
 */
public function render(Request $request): Response|bool
{
    if (/** 커스텀 렌더링이 필요한 경우 */) {

        return response(/* ... */);
    }

    return false;
}
```

특정 조건일 때만 커스텀 예외 보고 로직이 필요하다면, 예외의 `report` 메서드에서 `false`를 반환해 Laravel이 기본 예외 처리 설정을 사용하도록 할 수 있습니다.

```php
/**
 * 예외 보고.
 */
public function report(): bool
{
    if (/** 커스텀 보고가 필요한 경우 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에서 필요한 의존성은 타입 힌트하면 Laravel의 [서비스 컨테이너](/docs/master/container)가 자동으로 주입합니다.

<a name="throttling-reported-exceptions"></a>
### 예외 보고 제한(Throttling)

애플리케이션에서 매우 많은 예외를 보고한다면, 실제로 로그로 기록하거나 외부 에러 추적 서비스로 전송되는 예외의 수를 제한하고 싶을 수 있습니다.

무작위 샘플링 비율로 예외 보고를 제한하고 싶다면, `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. `throttle` 메서드에는 `Lottery` 인스턴스를 반환하는 클로저를 전달합니다.

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

예외 타입에 따라 조건부로 샘플링할 수도 있습니다. 특정 예외 클래스에 한해 샘플링 비율을 적용하려면 해당 클래스에만 `Lottery` 인스턴스를 반환하세요.

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```

또한, `Lottery` 대신 `Limit` 인스턴스를 반환하여, 예외가 로그로 기록되거나 외부 에러 추적 서비스로 전송되는 빈도를 제한할 수 있습니다. 이는 예를 들어, 애플리케이션이 사용하는 외부 서비스에 장애가 발생해 일시에 예외가 쏟아질 때 로그가 넘치지 않도록 보호할 때 유용합니다.

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```

기본적으로 제한의 키는 예외의 클래스명이 사용됩니다. 직접 키를 지정하고 싶다면, `Limit`의 `by` 메서드를 활용할 수 있습니다.

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```

물론, 예외마다 `Lottery`와 `Limit`을 혼합해 사용할 수도 있습니다.

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return match (true) {
            $e instanceof BroadcastException => Limit::perMinute(300),
            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
            default => Limit::none(),
        };
    });
})
```

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버의 HTTP 에러 코드를 설명합니다. 예를 들어 "페이지를 찾을 수 없음" (404), "인증되지 않음"(401), 혹은 개발자가 의도적으로 발생시키는 500 에러 등이 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다.

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 손쉽게 만들 수 있도록 지원합니다. 예를 들어, 404 에러 상태 코드 전용 에러 페이지를 커스터마이즈하려면, `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 디렉터리의 각 뷰 파일 이름은 해당 HTTP 상태 코드와 동일하게 만들어야 합니다. `abort` 함수 등으로 발생하는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다.

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있습니다. 퍼블리시 후에는 원하는 대로 템플릿을 수정할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체(fallback) HTTP 에러 페이지

특정 HTTP 상태 코드에 대응하는 페이지가 없을 때 렌더링되는 "대체 에러 페이지"도 정의할 수 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php` 및 `5xx.blade.php` 템플릿을 만드세요.

단, 대체 에러 페이지는 `404`, `500`, `503` 에러 응답에는 적용되지 않습니다. 이 상태 코드에는 Laravel이 별도의 내장 에러 페이지를 사용하기 때문입니다. 만약 이 코드들의 페이지를 커스터마이즈하려면, 각각의 상태 코드에 맞춰 개별적으로 커스텀 에러 페이지를 정의해야 합니다.
