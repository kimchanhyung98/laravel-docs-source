# 에러 처리

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [유형별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
- [예외 보고 제한(쓰로틀링)](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면, 에러 및 예외 처리가 이미 기본적으로 설정되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용하여 예외가 보고되고 렌더링되는 방식을 관리할 수 있습니다.

`withExceptions` 클로저에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션의 예외 처리를 관리하는 역할을 합니다. 이 문서 전체에서 이 객체에 대해 더 자세히 설명합니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 에러에 대한 정보가 얼마나 표시되는지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 프로덕션에서 이 값이 `true`로 설정되어 있으면 애플리케이션의 최종 사용자에게 민감한 설정 값이 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그에 남기거나, [Sentry](https://github.com/getsentry/sentry-laravel)나 [Flare](https://flareapp.io)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/{{version}}/logging) 설정에 따라 기록됩니다. 물론, 원하는 방식으로 예외를 로그할 수도 있습니다.

다른 유형의 예외에 대해 서로 다른 방식으로 보고하고 싶다면, `bootstrap/app.php` 파일의 `report` 예외 메서드를 이용해 특정 유형의 예외가 보고되어야 할 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입힌트를 검사하여 어떤 예외 유형을 보고하는지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드로 커스텀 예외 보고 콜백을 등록하면, Laravel은 여전히 기본 로깅 설정에 따라 예외를 로그합니다. 예외가 기본 로깅 스택으로 전달되지 않도록 하려면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```

> [!NOTE]
> 특정 예외의 보고를 커스터마이즈하려면 [보고 및 렌더링 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

가능하다면, Laravel은 현재 사용자의 ID를 모든 예외 로그 메시지에 컨텍스트 데이터로 자동 추가합니다. 애플리케이션의 `bootstrap/app.php` 파일의 `context` 예외 메서드를 사용해 전역 컨텍스트 데이터를 직접 정의할 수 있습니다. 이 정보는 애플리케이션에서 기록하는 모든 예외 로그 메시지에 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 특정 예외만의 고유한 컨텍스트 정보를 로그에 남기고 싶을 때가 있습니다. 애플리케이션에서 사용하는 예외에 `context` 메서드를 정의하면, 해당 예외에 관련 있는 데이터를 로그 항목에 추가할 수 있습니다:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보 반환
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

때로는 예외를 보고하면서 현재 요청 처리는 계속 진행해야 할 수 있습니다. `report` 헬퍼 함수를 사용하면, 사용자에게 에러 페이지를 렌더링하지 않고도 신속하게 예외를 보고할 수 있습니다:

```php
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
#### 중복된 예외 보고 방지

애플리케이션 전체에서 `report` 함수를 사용하다 보면 동일한 예외가 여러 번 보고되어 로그에 중복 항목이 생길 수 있습니다.

동일한 예외 인스턴스가 오직 한 번만 보고되도록 하려면, `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출할 수 있습니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스에 대해 `report` 헬퍼가 여러 번 호출되더라도, 첫 번째 호출만 보고됩니다:

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

애플리케이션의 [로그](/docs/{{version}}/logging)에 메시지가 기록될 때, 메시지는 특정 [로그 레벨](/docs/{{version}}/logging#log-levels)로 저장되며, 이는 기록되는 메시지의 심각도나 중요도를 나타냅니다.

앞서 설명한 것처럼, `report` 메서드로 커스텀 예외 보고 콜백을 등록하더라도 Laravel은 여전히 기본 로깅 설정에 따라 예외를 로그합니다. 하지만 로그 레벨에 따라 메시지가 기록되는 채널이 달라질 수 있으므로, 특정 예외의 로그 레벨을 직접 지정하고 싶을 수 있습니다.

이럴 때는 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 예외 유형, 두 번째 인자로 로그 레벨을 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 유형별 예외 무시

애플리케이션을 개발하다 보면, 결코 보고하고 싶지 않은 예외 유형이 생길 수 있습니다. 이러한 예외를 무시하려면, `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용하면 됩니다. 이 메서드에 제공된 모든 클래스는 결코 보고되지 않지만, 커스텀 렌더링 로직은 여전히 사용할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스만 구현해도 됩니다. 이 인터페이스가 지정된 예외는 Laravel의 예외 핸들러에서 절대 보고되지 않습니다:

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

내부적으로 Laravel은 404 HTTP 에러나 잘못된 CSRF 토큰으로 인한 419 HTTP 응답처럼 이미 일부 오류 유형을 무시하고 있습니다. 무시되는 특정 예외를 더 이상 무시하지 않도록 하려면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로, Laravel의 예외 핸들러는 예외를 HTTP 응답으로 변환합니다. 하지만, 특정 유형의 예외에 대해 커스텀 렌더링 클로저를 등록할 수 있습니다. 이는 앱의 `bootstrap/app.php` 파일의 `render` 예외 메서드를 사용해서 구현할 수 있습니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response`의 인스턴스를 반환해야 하며, `response` 헬퍼를 통해 쉽게 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 검사하여 어떤 예외 유형을 렌더링하는지 판단합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

`render` 메서드를 사용해 Laravel이나 Symfony의 내장 예외(`NotFoundHttpException` 등)에 대한 렌더링 동작도 오버라이드할 수 있습니다. 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions) {
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

예외를 렌더링할 때, Laravel은 요청의 `Accept` 헤더를 기준으로 예외를 HTML 또는 JSON 응답으로 제공할지 자동으로 결정합니다. 만약 Laravel이 HTML 또는 JSON 예외 응답을 렌더링할지 결정하는 방식을 커스터마이즈하고 싶다면, `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```

<a name="customizing-the-exception-response"></a>
#### 예외 응답 커스터마이즈

드물게, Laravel 예외 핸들러가 렌더링하는 전체 HTTP 응답을 커스터마이즈해야 할 경우가 있습니다. 이럴 때는 `respond` 메서드로 응답 커스터마이제이션 클로저를 등록할 수 있습니다:

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions) {
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

애플리케이션의 `bootstrap/app.php` 파일에서 커스텀 보고 및 렌더링 동작을 정의하는 대신, 예외 클래스 내에 `report`와 `render` 메서드를 직접 정의할 수 있습니다. 이 메서드가 존재하면 프레임워크가 자동으로 호출합니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외를 보고합니다.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * 예외를 HTTP 응답으로 렌더링합니다.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 렌더링 가능한 예외(Laravel 또는 Symfony의 내장 예외 등)를 상속하는 경우, 예외의 `render` 메서드에서 `false`를 반환하면 기본 HTTP 응답을 렌더링할 수 있습니다:

```php
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 예외가 커스텀 렌더링이 필요한 경우 */) {

        return response(/* ... */);
    }

    return false;
}
```

예외에 커스텀 보고 로직이 있는데, 특정 조건에서만 필요하다면 예외의 `report` 메서드에서 `false`를 반환하게 하여, Laravel이 기본 예외 처리 구성을 사용하도록 할 수 있습니다:

```php
/**
 * 예외를 보고합니다.
 */
public function report(): bool
{
    if (/** 예외가 커스텀 보고가 필요한 경우 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에서 필요한 의존성을 타입힌트로 선언하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 예외 보고 제한(쓰로틀링)

애플리케이션에서 매우 많은 예외가 보고된다면, 실제로 로그에 남기거나 외부 에러 트래킹 서비스로 전송되는 예외의 수를 제한(쓰로틀링)하고 싶을 수 있습니다.

무작위 샘플 비율로 예외를 보고하려면, `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. `throttle` 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 받습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

예외 유형에 따라 샘플링 여부를 조건부로 지정할 수도 있습니다. 예를 들어, 특정 예외 클래스에 대해서만 샘플링하고 싶다면 해당 클래스에만 `Lottery` 인스턴스를 반환하면 됩니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```

또는, 예외를 로그에 남기거나 외부 에러 트래킹 서비스로 전송할 때, `Lottery` 대신 `Limit` 인스턴스를 반환하여 레이트 리미트(시간당 제한)를 둘 수 있습니다. 이는 예를 들어, 앱에서 사용하는 서드파티 서비스가 다운되어 예외가 대량 발생할 때 로그 폭주를 방지하는 데 유용합니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```

기본적으로 제한은 예외 클래스 자체를 키로 사용합니다. `Limit`의 `by` 메서드를 사용하면 제한 키를 직접 지정할 수도 있습니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```

물론, 예외별로 `Lottery`와 `Limit`을 혼합하여 사용할 수도 있습니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
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

일부 예외는 서버에서 발생한 HTTP 에러 코드를 설명합니다. 예를 들어, "페이지를 찾을 수 없음"(404), "인증되지 않음"(401), 또는 개발자가 발생시킨 500 에러 등이 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 손쉽게 표시할 수 있게 해줍니다. 예를 들어, 404 HTTP 상태 코드용 에러 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하세요. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉토리 내의 뷰 파일 이름은 대응하는 HTTP 상태 코드와 일치해야 합니다. `abort` 함수로 발생한 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있습니다. 퍼블리시한 후에는 원하는 대로 템플릿을 커스터마이즈할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백(Fallback) HTTP 에러 페이지

특정 HTTP 상태 코드에 해당하는 페이지가 없을 때 표시할 "폴백" 에러 페이지도 정의할 수 있습니다. 이를 위해 `resources/views/errors` 디렉토리에 `4xx.blade.php` 및 `5xx.blade.php` 템플릿을 생성하세요.

폴백 에러 페이지를 정의해도, `404`, `500`, `503` 오류 응답에는 영향을 주지 않습니다. 이 상태 코드들은 Laravel이 내부적으로 전용 페이지를 제공하기 때문입니다. 이런 상태 코드에 대해 표시할 페이지를 변경하려면 각 코드에 맞는 커스텀 에러 페이지를 각각 정의해야 합니다.