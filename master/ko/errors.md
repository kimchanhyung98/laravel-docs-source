# 오류 처리

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

새로운 Laravel 프로젝트를 시작하면, 오류 및 예외 처리는 이미 기본적으로 설정되어 있습니다. 하지만 언제든지 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용하여 예외가 어떻게 보고되고 렌더링될지 관리할 수 있습니다.

`withExceptions` 클로저에 전달되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며 애플리케이션의 예외 처리를 담당합니다. 이 문서 전반에 걸쳐 이 객체에 대해 더 자세히 다루겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 오류 정보를 얼마나 많이 노출할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영(프로덕션) 환경에서는 이 값을 반드시 `false`로 두어야 합니다. 운영 환경에서 `true`로 설정하면 민감한 설정 정보가 애플리케이션의 최종 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그로 남기거나 [Sentry](https://github.com/getsentry/sentry-laravel) 또는 [Flare](https://flareapp.io)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/{{version}}/logging) 설정에 따라 기록됩니다. 그러나 원하는 방식으로 예외를 자유롭게 기록할 수 있습니다.

다양한 타입의 예외를 각각 다르게 보고하려면, 애플리케이션의 `bootstrap/app.php`의 `withExceptions`에서 `report` 예외 메서드를 사용해 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 통해 어떤 예외를 보고하는지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드를 사용해 커스텀 예외 보고 콜백을 등록하면, Laravel은 여전히 애플리케이션의 기본 로깅 설정에 따라 예외를 기록합니다. 예외가 기본 로깅 스택으로 전파되는 것을 막으려면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환할 수 있습니다:

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
> 특정 예외의 보고 방식을 커스터마이즈하려면 [보고 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)를 사용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

가능하다면, Laravel은 현재 사용자의 ID를 모든 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용해 전역 로그 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션이 기록하는 모든 예외 로그 메시지에 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것은 유용할 수 있지만, 특정 예외의 경우에만 특별한 컨텍스트를 추가하고 싶을 수도 있습니다. 애플리케이션의 예외 클래스에 `context` 메서드를 정의해 해당 예외와 관련된 데이터를 예외 로그에 포함할 수 있습니다:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보를 반환합니다.
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

가끔 예외를 보고해야 하지만, 현재 요청을 계속 처리하고 싶을 수 있습니다. `report` 헬퍼 함수는 에러 페이지를 사용자에게 렌더링하지 않고도 손쉽게 예외를 보고할 수 있게 해줍니다:

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
#### 예외 보고 중복 제거

애플리케이션 전반에서 `report` 함수를 사용하다 보면, 동일한 예외를 여러 번 보고하게 되어 로그에 중복이 발생할 수 있습니다.

특정 예외 인스턴스가 한 번만 보고되도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출할 수 있습니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 `report` 헬퍼가 동일한 예외 인스턴스로 여러 번 호출되더라도 첫 번째 호출만 보고됩니다:

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

애플리케이션의 [로그](/docs/{{version}}/logging)에 메시지가 기록될 때, 메시지는 [로그 레벨](/docs/{{version}}/logging#log-levels)에 따라 기록되어 메시지의 심각도(중요도)를 나타냅니다.

앞서 언급했듯이, `report` 메서드를 사용해 커스텀 예외 보고 콜백을 등록하더라도 Laravel은 여전히 애플리케이션의 기본 로깅 설정에 따라 예외를 기록합니다. 다만, 로그 레벨이 어떤 채널에 메시지가 기록될지에 영향을 줄 수 있으므로, 특정 예외를 기록할 때의 로그 레벨을 설정할 수 있습니다.

이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 예외 타입, 두 번째 인수로 로그 레벨을 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 개발하다 보면, 아예 보고하고 싶지 않은 타입의 예외가 있을 수 있습니다. 이 경우, `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용해 이를 무시할 수 있습니다. 이 메서드에 전달된 클래스의 예외는 절대 보고되지 않습니다. 단, 별도의 렌더링 로직은 여전히 동작할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또 다른 방법으로는, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현(implements)하는 것도 있습니다. 이 인터페이스가 지정된 예외는 Laravel의 예외 핸들러에서 절대 보고되지 않습니다:

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

내부적으로 Laravel은 일부 오류(404 HTTP 오류 또는 CSRF 토큰 무효로 인한 419 HTTP 응답 등)는 이미 자동으로 무시합니다. Laravel이 특정 예외 타입을 무시하지 않도록 하려면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel의 예외 핸들러는 예외를 HTTP 응답으로 변환해줍니다. 하지만 특정 타입의 예외에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. 이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용할 수 있습니다.

`render` 메서드에 전달되는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼를 사용해 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 참고하여 어떤 타입의 예외를 렌더링할지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

`render` 메서드를 사용해 Laravel 또는 Symfony의 내장 예외(`NotFoundHttpException` 등)의 렌더링 동작을 덮어쓸 수도 있습니다. 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

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
#### JSON으로 예외 렌더링

예외를 렌더링할 때, Laravel은 요청의 `Accept` 헤더를 기반으로 예외를 HTML 또는 JSON 응답으로 자동 렌더링할지 결정합니다. HTML이나 JSON 예외 응답이 렌더링되는 방식을 커스터마이즈하려면 `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

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
#### 예외 응답 전체 커스터마이즈

드물긴 하지만, Laravel의 예외 핸들러가 렌더링하는 HTTP 응답 전체를 커스터마이즈해야 하는 경우도 있습니다. 이럴 때 `respond` 메서드를 통해 응답 커스터마이즈 클로저를 등록할 수 있습니다:

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

예외에 대한 커스텀 보고 및 렌더링 동작을 애플리케이션의 `bootstrap/app.php`에서 정의하는 대신, 예외 클래스 내부에 `report` 및 `render` 메서드를 직접 정의할 수도 있습니다. 이 메서드가 존재하면 프레임워크에서 자동으로 호출됩니다:

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

예외가 이미 렌더링 가능한 예외(예: 내장 Laravel 또는 Symfony 예외)를 상속하고 있다면, 예외의 `render` 메서드에서 `false`를 반환해 기본 HTTP 응답을 렌더링할 수 있습니다:

```php
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 예외에 대해 커스텀 렌더링이 필요한지 판단 */) {

        return response(/* ... */);
    }

    return false;
}
```

예외에 특정 조건에서만 필요한 커스텀 보고 로직이 있다면, `report` 메서드에서 `false`를 반환해 Laravel이 기본 예외 처리 구성을 사용해 예외를 보고하도록 할 수 있습니다:

```php
/**
 * 예외를 보고합니다.
 */
public function report(): bool
{
    if (/** 예외에 대해 커스텀 보고가 필요한지 판단 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 의존성을 타입 힌트로 지정하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에서 자동으로 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 예외 보고 제한(Throttling)

애플리케이션이 매우 많은 수의 예외를 보고한다면, 실제로 기록되거나 외부 오류 추적 서비스로 전송되는 예외의 수를 제한하고 싶을 수 있습니다.

무작위 표본(sample) 비율로 예외를 선택하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. `throttle` 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 받습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

예외 타입별로 조건부 표본 추출도 가능합니다. 특정 예외 클래스의 인스턴스만 샘플링하려면, 해당 클래스의 경우에만 `Lottery` 인스턴스를 반환하면 됩니다:

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

외부 오류 추적 서비스로 전송하거나 로그에 기록되는 예외의 비율을 제한(rate limit)하려면, `Lottery` 대신 `Limit` 인스턴스를 반환할 수 있습니다. 예를 들어, 애플리케이션이 사용하는 타사 서비스가 다운되어 예외가 폭주(log flooding)하는 것을 방지하는 데 유용합니다:

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

기본적으로 rate limit는 예외의 클래스명을 키로 사용합니다. `Limit`의 `by` 메서드를 통해 직접 키를 지정할 수도 있습니다:

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

물론, 여러 예외에 대해 `Lottery`와 `Limit`을 혼합하여 반환할 수도 있습니다:

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

일부 예외는 서버에서 발생하는 HTTP 오류 코드를 설명합니다. 예를 들어, 이는 "페이지를 찾을 수 없음"(404), "인증되지 않음"(401), 또는 개발자가 생성한 500 오류일 수 있습니다. 애플리케이션 어디서나 이런 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 손쉽게 표시할 수 있도록 해줍니다. 예를 들어, 404 HTTP 상태 코드의 에러 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하세요. 이 뷰는 애플리케이션에서 발생한 모든 404 오류에 대해 렌더링됩니다. 이 디렉터리 내의 뷰들은 각각의 HTTP 상태 코드와 이름이 일치해야 합니다. `abort` 함수에 의해 발생된 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어를 사용해 퍼블리시할 수 있습니다. 퍼블리시 후에는 원하는 대로 자유롭게 커스터마이즈할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체 Fallback HTTP 에러 페이지

특정 일련의 HTTP 상태 코드에 대한 "대체" 에러 페이지를 정의할 수도 있습니다. 특정 HTTP 상태 코드에 해당하는 페이지가 존재하지 않을 때 이 페이지가 렌더링됩니다. 이를 위해 애플리케이션의 `resources/views/errors` 디렉터리에 `4xx.blade.php` 및 `5xx.blade.php` 템플릿을 생성하세요.

404, 500, 503 오류의 경우 Laravel이 별도의 전용 내장 페이지를 사용하므로, fallback 페이지가 영향을 주지 않습니다. 이 상태 코드에 대한 페이지를 커스터마이즈하려면 각각 별도의 에러 페이지를 정의해야 합니다.