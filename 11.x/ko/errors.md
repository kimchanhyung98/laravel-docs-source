# 오류 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [예외 유형별 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
- [보고된 예외 제한](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [사용자 정의 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작할 때, 오류 및 예외 처리는 이미 구성되어 있습니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용하여 예외가 어떻게 보고되고 렌더링되는지 직접 관리할 수도 있습니다.

`withExceptions` 클로저에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions` 인스턴스이며, 애플리케이션 내 예외 처리를 담당합니다. 이 문서 전체에서 이 객체에 대해 더 깊이 다루겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 실제로 얼마나 많은 오류 정보를 보여줄지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따르도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG`를 `true`로 설정해야 합니다. **하지만 운영 환경에서는 항상 `false`로 설정해야 합니다. 만약 운영 환경에서 `true`로 설정하면, 애플리케이션의 민감한 설정 값들이 끝 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그에 기록하거나 [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io) 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/11.x/logging) 설정에 따라 기록됩니다. 하지만 예외를 원하는 방식으로 자유롭게 기록할 수 있습니다.

예외 유형별로 다른 방식으로 보고해야 할 경우, 애플리케이션의 `bootstrap/app.php`에서 `report` 메서드를 사용해 특정 타입의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 검사하여 어떤 예외를 처리할지 판단합니다:

```
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드로 사용자 정의 예외 보고 콜백을 등록해도, Laravel은 여전히 애플리케이션 기본 로깅 설정에 따라 예외를 로그로 남깁니다. 기본 로깅 스택에 예외가 전달되는 것을 막으려면 리포트 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

```
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
> 특정 예외에 대한 예외 보고를 맞춤화하려면 [보고 가능 예외](/docs/11.x/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

가능한 경우, Laravel은 현재 사용자의 ID를 각 예외 로그 메시지에 컨텍스트 데이터로 자동으로 추가합니다. `bootstrap/app.php`에서 `context` 메서드를 사용해 애플리케이션 전역에서 사용할 사용자 지정 컨텍스트 데이터를 정의할 수 있으며, 이 데이터는 모든 예외 로그 메시지에 포함됩니다:

```
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것 외에도, 특정 예외에만 포함할 고유한 정보가 있을 수 있습니다. 애플리케이션의 예외 클래스에 `context` 메서드를 정의하여 해당 예외와 관련된 데이터를 로그 항목에 추가할 수 있습니다:

```
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
#### `report` 헬퍼 함수

예외를 보고하되, 현재 요청 처리 흐름은 계속 이어가야 하는 경우가 있습니다. `report` 헬퍼 함수는 오류 페이지를 렌더링하지 않고 빠르게 예외를 보고할 때 사용합니다:

```
public function isValid(string $value): bool
{
    try {
        // 값 검증...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 중복 예외 보고 방지

애플리케이션 전반에서 `report` 함수를 사용하다 보면 동일한 예외가 여러 번 보고되어 로그에 중복 기록될 수 있습니다.

예외 인스턴스가 한 번만 보고되도록 하려면 `bootstrap/app.php`에서 `dontReportDuplicates` 메서드를 호출하세요:

```
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스로 `report`를 여러 번 호출해도 첫 번째만 보고되고 이후 호출은 무시됩니다:

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

애플리케이션의 [로그](/docs/11.x/logging)에 메시지를 기록할 때, 로그 메시지의 심각도나 중요도를 나타내는 [로그 레벨](/docs/11.x/logging#log-levels)로 기록됩니다.

앞서 설명했듯, `report` 메서드 조합으로 사용자 정의 보고 콜백을 등록해도 Laravel은 기본 로깅 설정에 따라 예외를 기록합니다. 그러나 로그 레벨에 따라 로그가 기록되는 채널이 달라질 수 있기 때문에 특정 예외가 기록될 로그 레벨을 설정하고 싶을 수 있습니다.

이 경우 `bootstrap/app.php`에서 `level` 메서드를 사용하세요. 첫 번째 인수로 예외 클래스, 두 번째 인수로 로그 레벨을 전달합니다:

```
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 예외 유형별 무시

애플리케이션을 개발할 때, 보고하지 않으려는 특정 예외 유형이 있을 수 있습니다. 이런 예외는 `bootstrap/app.php`에서 `dontReport` 메서드에 클래스 배열로 지정하면 절대 보고되지 않지만, 여전히 렌더링 로직은 커스터마이징할 수 있습니다:

```
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현하여 해당 예외를 "보고 금지" 표시할 수도 있습니다. 이 인터페이스가 적용된 예외는 Laravel 예외 핸들러에서 절대 보고하지 않습니다:

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

Laravel은 내부적으로 404 HTTP 오류, CSRF 토큰 유효하지 않아 발생하는 419 HTTP 응답 예외 등을 자동으로 무시합니다. 만약 Laravel이 무시하지 않도록 하려면 `bootstrap/app.php`에서 `stopIgnoring` 메서드를 사용하세요:

```
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해 반환합니다. 하지만 특정 예외 유형에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. `bootstrap/app.php`에서 `render` 메서드를 사용해 구현할 수 있습니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼를 사용해 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 확인해 어떤 예외를 렌더링할지 판단합니다:

```
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

Laravel 내부 예외나 Symfony 예외(`NotFoundHttpException` 등)에 대한 렌더링도 `render` 메서드로 오버라이드할 수 있습니다. 만약 `render`에 건 클로저가 아무 응답을 반환하지 않으면, Laravel의 기본 예외 렌더링이 수행됩니다:

```
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

Laravel은 요청의 `Accept` 헤더를 기반으로, 예외를 HTML로 렌더링할지 JSON으로 렌더링할지 자동으로 판단합니다. 이 기본 동작을 직접 제어하고 싶다면 `shouldRenderJsonWhen` 메서드를 활용하세요:

```
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
#### 예외 응답 사용자 정의

가끔 Laravel 예외 핸들러가 렌더링하는 HTTP 응답 자체를 전면적으로 수정해야 하는 경우가 있습니다. 이럴 땐 `respond` 메서드를 사용해 응답 커스터마이징 클로저를 등록하세요:

```
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
### 보고 가능 및 렌더링 가능 예외

애플리케이션의 `bootstrap/app.php`에서 직접 사용자 정의 예외 보고와 렌더링 동작을 정의하는 대신, 애플리케이션 내 예외 클래스에 `report` 및 `render` 메서드를 정의할 수 있습니다. 이 메서드들이 있으면 프레임워크가 자동으로 호출합니다:

```
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

만약 예외가 이미 렌더링 가능한 예외(예: Laravel 내장 예외나 Symfony 예외)를 확장한다면, 렌더링 메서드에서 `false`를 반환해 기본 HTTP 응답을 사용하도록 할 수 있습니다:

```
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 렌더링 커스텀 필요 시 */) {

        return response(/* ... */);
    }

    return false;
}
```

조건에 따라 맞춤 예외 보고 로직이 필요한 경우, 기본 예외 보고 처리로 예외 보고를 위임하려면 `report` 메서드에서 `false`를 반환하면 됩니다:

```
/**
 * 예외를 보고합니다.
 */
public function report(): bool
{
    if (/** 예외 맞춤 보고 필요 시 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]  
> `report` 메서드의 필요한 의존성은 Laravel [서비스 컨테이너](/docs/11.x/container)를 통해 자동으로 의존성 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 제한

애플리케이션에서 매우 많은 예외가 보고된다면, 실제로 기록되거나 외부 오류 추적 서비스로 전송되는 예외의 개수를 제한하는 기능이 필요할 수 있습니다.

랜덤 샘플링을 하려면 `bootstrap/app.php`에서 `throttle` 메서드에 `Lottery` 인스턴스를 반환하는 클로저를 등록하세요:

```
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

특정 예외 클래스만 샘플링하려면 조건문을 사용해 해당 클래스에만 `Lottery` 인스턴스를 반환하도록 할 수 있습니다:

```
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

또는 `Lottery` 대신 `Limit` 인스턴스를 반환하여 속도 제한(rate limit)하는 것도 가능합니다. 이는 당장 처리량 급증으로 로그가 도배되는 상황(예: 서드파티 서비스 오류 발생 시)을 방지하는 데 유용합니다:

```
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

기본 설정으로는 예외 클래스명이 제한 키로 사용됩니다. `Limit` 인스턴스에서 `by` 메서드로 제한 키를 직접 지정할 수도 있습니다:

```
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

물론 서로 다른 예외마다 `Lottery`와 `Limit` 인스턴스를 혼합해서 반환해도 무방합니다:

```
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

일부 예외는 서버의 HTTP 오류 코드를 나타냅니다. 예를 들어 "페이지를 찾을 수 없음"(404), "권한 없음"(401), 또는 개발자가 직접 발생시킨 500 오류 등이 있습니다. 이런 응답을 애플리케이션 어디서든 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```
abort(404);
```

<a name="custom-http-error-pages"></a>
### 사용자 정의 HTTP 오류 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 사용자 정의 오류 페이지를 쉽게 표시할 수 있게 합니다. 예를 들어 404 오류 페이지를 커스터마이징하려면 `resources/views/errors/404.blade.php` 뷰를 생성하세요. 이 뷰는 애플리케이션에서 발생하는 모든 404 오류에 대해 렌더링됩니다. 이 디렉토리 내 뷰 파일 이름은 대응하는 HTTP 상태 코드와 일치해야 합니다. `abort` 함수가 발생시키는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 뷰 내에 `$exception` 변수로 전달됩니다:

```
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 오류 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있습니다. 퍼블리시 후에는 마음껏 커스터마이즈할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체(Fallback) HTTP 오류 페이지

특정 HTTP 상태 코드별 오류 페이지가 없을 경우 렌더링할 "대체" 오류 페이지를 정의할 수도 있습니다. `resources/views/errors` 디렉토리에 `4xx.blade.php`와 `5xx.blade.php` 템플릿을 생성하면 각각 클라이언트 오류 및 서버 오류 시 기본으로 보여집니다.

다만 대체 페이지는 Laravel 내부적으로 전용 페이지가 있는 `404`, `500`, `503` 상태 코드에는 영향을 미치지 않습니다. 이들 상태 코드에 대한 오류 페이지를 커스터마이즈하려면 각각 별도의 사용자 정의 오류 페이지를 작성해야 합니다.