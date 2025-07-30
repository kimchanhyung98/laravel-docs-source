# 오류 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [유형별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 가능 및 렌더 가능 예외](#renderable-exceptions)
- [보고된 예외 제한](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [맞춤 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면 기본적으로 오류 및 예외 처리 기능이 설정되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php`에서 `withExceptions` 메서드를 사용하여 예외 보고 및 렌더링 방식을 관리할 수 있습니다.

`withExceptions` 클로저에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스로, 애플리케이션 내 예외 처리 관리를 담당합니다. 이 문서 전반에서 이 객체에 대해 더 깊이 알아보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일 내 `debug` 옵션은 오류에 대해 사용자에게 실제로 표시되는 정보의 양을 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따르도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **하지만 프로덕션 환경에서는 항상 `false`로 설정해야 합니다. 만약 프로덕션에서 `true`로 설정하면 애플리케이션의 민감한 설정 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그에 기록하거나 [Sentry](https://github.com/getsentry/sentry-laravel) 또는 [Flare](https://flareapp.io) 같은 외부 서비스로 전송하는 데 활용됩니다. 기본적으로 예외는 [로깅](/docs/12.x/logging) 설정에 따라 기록됩니다. 하지만 원하는 방식으로 자유롭게 예외를 기록할 수 있습니다.

서로 다른 유형의 예외를 각기 다르게 보고해야 한다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드로 특정 유형의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 보고 어떤 예외 타입을 처리할지 판단합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드로 사용자 정의 예외 보고 콜백을 등록하면, Laravel은 여전히 애플리케이션의 기본 로깅 설정을 사용해 예외를 기록합니다. 기본 로깅에 예외 전달을 중단하려면, 보고 콜백을 정의할 때 `stop` 메서드를 호출하거나 콜백에서 `false`를 반환하면 됩니다:

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
> 특정 예외에 대한 예외 보고를 더 세밀하게 조정하고자 한다면 [보고 가능 예외](/docs/12.x/errors#renderable-exceptions)도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

가능하면 Laravel은 자동으로 현재 사용자의 ID를 모든 예외 로그 메시지의 컨텍스트 데이터로 추가합니다. `bootstrap/app.php` 내 `context` 예외 메서드를 사용하여 자체 전역 컨텍스트 데이터를 정의할 수도 있습니다. 이 데이터는 애플리케이션이 작성하는 모든 예외 로그 메시지에 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것이 유용할 때도 있지만, 특정 예외마다 고유한 컨텍스트를 포함하고 싶을 수도 있습니다. 이때 애플리케이션의 예외 클래스에 `context` 메서드를 정의하여, 해당 예외에 관련된 임의 데이터를 예외 로그에 추가할 수 있습니다:

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
#### `report` 헬퍼 함수

예외를 보고하되 현재 요청 처리 흐름은 계속 유지하고 싶을 때가 있습니다. 이때 `report` 헬퍼 함수는 오류 페이지를 렌더링하지 않고도 신속하게 예외를 보고하는 방법을 제공합니다:

```php
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
#### 보고 예외 중복 제거

애플리케이션에서 `report` 함수를 여기저기 사용하면 동일한 예외가 여러 번 보고되어 로그에 중복 항목이 생길 수 있습니다.

예외 인스턴스 하나가 단 한 번만 보고되도록 하려면, 애플리케이션의 `bootstrap/app.php`에서 `dontReportDuplicates` 예외 메서드를 호출하세요:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스로 `report` 헬퍼가 호출되면 첫 번째 호출만 보고되고, 이후 호출은 무시됩니다:

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

애플리케이션 로그에 메시지가 기록될 때는 메시지의 심각도 또는 중요도를 나타내는 [로그 레벨](/docs/12.x/logging#log-levels)과 함께 기록됩니다.

앞서 설명한 것처럼 `report` 메서드로 사용자 정의 예외 보고 콜백을 등록해도 Laravel은 여전히 기본 로깅 설정을 사용해 예외를 기록합니다. 하지만 로그 레벨은 메시지가 기록될 채널에 영향을 줄 수 있으므로, 특정 예외가 어느 로그 레벨로 기록될지 설정할 수도 있습니다.

이때 애플리케이션 `bootstrap/app.php`에서 `level` 예외 메서드를 사용하면 됩니다. 이 메서드는 첫 번째 인수로 예외 타입, 두 번째 인수로 로그 레벨을 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 유형별 예외 무시

애플리케이션을 구축하다 보면 절대 보고할 필요 없는 일부 예외 유형이 존재합니다. 이런 예외를 무시하려면 `bootstrap/app.php`에서 `dontReport` 예외 메서드를 사용하세요. 해당 메서드에 지정한 클래스는 절대 보고되지 않지만, 여전히 사용자 정의 렌더링 로직을 가질 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현하여 "표시"하는 방식도 있습니다. 이 인터페이스를 구현한 예외는 Laravel의 예외 처리기에서 절대 보고하지 않습니다:

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

특정 예외를 무시하는 조건을 더 세밀하게 조절해야 한다면, `dontReportWhen` 메서드에 클로저를 제공할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```

Laravel은 내부적으로 이미 404 HTTP 오류나, 무효한 CSRF 토큰으로 발생하는 419 HTTP 응답 예외 등 일부 오류 유형을 무시합니다. 만약 특정 예외 유형을 더 이상 무시하지 않도록 지시하려면 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 처리기는 예외를 HTTP 응답으로 변환해 반환합니다. 그러나 특정 예외 타입에 대해 사용자 정의 렌더링 클로저를 등록할 수 있습니다. `bootstrap/app.php`에서 `render` 예외 메서드를 사용해 이 작업을 수행할 수 있습니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼를 통해 생성할 수 있습니다. Laravel은 클로저 타입 힌트를 통해 어떤 예외 타입을 처리할지 판단합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

내장 Laravel 또는 Symfony 예외(예: `NotFoundHttpException`)에 대해서도 `render` 메서드로 렌더링 동작을 재정의할 수 있습니다. 반환 값이 없으면 Laravel 기본 예외 렌더링이 사용됩니다:

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
#### 예외를 JSON으로 렌더링하기

예외 렌더링 시 Laravel은 요청의 `Accept` 헤더를 보고 HTML 또는 JSON 응답으로 렌더링할지 자동으로 판단합니다. 렌더링 방식을 직접 정의하려면 `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

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
#### 예외 응답 커스터마이징

가끔 Laravel 예외 처리기가 렌더링하는 HTTP 응답 전체를 사용자 정의해야 할 때가 있습니다. 이럴 때는 `respond` 메서드에 응답 커스터마이징 클로저를 등록하세요:

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
### 보고 가능 및 렌더 가능 예외

사용자 정의 보고 및 렌더링 동작을 `bootstrap/app.php`에 정의하는 대신, 애플리케이션 예외 클래스 내에 직접 `report` 및 `render` 메서드를 정의할 수 있습니다. 이 메서드들이 존재하면 프레임워크가 자동으로 호출합니다:

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

예외가 이미 렌더 가능 예외(내장 Laravel 또는 Symfony 예외 등)를 확장하는 경우, `render` 메서드에서 `false`를 반환하여 기본 HTTP 응답을 사용하도록 할 수 있습니다:

```php
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 예외가 사용자 정의 렌더링이 필요한지 판단 */) {

        return response(/* ... */);
    }

    return false;
}
```

특정 조건에서만 사용자 정의 보고 로직이 필요하다면, `report` 메서드에서 `false`를 반환해 Laravel 기본 예외 처리 구성이 해당 예외를 보고하게 만들 수도 있습니다:

```php
/**
 * 예외를 보고합니다.
 */
public function report(): bool
{
    if (/** 예외가 사용자 정의 보고가 필요한지 판단 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 의존성을 타입 힌트하면 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 제한

애플리케이션이 대량의 예외를 보고할 경우, 실제 로그나 외부 오류 추적 서비스로 전송되는 예외 수를 제한할 필요가 있습니다.

`bootstrap/app.php`에서 `throttle` 예외 메서드에 클로저를 전달하면 랜덤 확률 표본으로 예외를 제한할 수 있습니다. 클로저는 `Lottery` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

예외 유형에 따라 조건부 샘플링도 가능합니다. 특정 예외 클래스에 대해서만 `Lottery` 인스턴스를 반환하여 제한할 수 있습니다:

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

`Lottery` 대신 `Limit` 인스턴스를 반환하면 레이트 리밋(rate limit)도 설정할 수 있습니다. 이는 외부 서비스 장애 등 갑작스러운 예외 폭주로 로그가 넘치는 상황에 유용합니다:

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

기본적으로 제한 키는 예외 클래스명입니다. `Limit`의 `by` 메서드를 이용해 커스텀 키를 지정할 수 있습니다:

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

`Lottery`와 `Limit` 인스턴스를 혼합해 여러 예외를 다르게 제한할 수도 있습니다:

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

일부 예외는 서버에서 발생하는 HTTP 오류 코드를 설명합니다. 예를 들어 "페이지를 찾을 수 없음"(404), "권한 없음"(401), 심지어 개발자가 만든 500 오류 등이 있습니다. 애플리케이션 어디서나 이런 응답을 만들려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 맞춤 HTTP 오류 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 맞춤 오류 페이지를 쉽게 표시할 수 있도록 합니다. 예를 들어 404 상태 코드에 대한 오류 페이지를 커스터마이징하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 오류에 대해 렌더링됩니다. 이 디렉토리 안의 뷰 파일 이름은 대응하는 HTTP 상태 코드와 일치해야 합니다. `abort` 함수가 발생시키는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel 기본 오류 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있습니다. 퍼블리시한 후 자유롭게 커스터마이징할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체 HTTP 오류 페이지

특정 HTTP 상태 코드에 대응하는 페이지가 없는 경우 표시할 "대체" 오류 페이지도 정의할 수 있습니다. 이를 위해 `resources/views/errors` 디렉토리에 `4xx.blade.php`와 `5xx.blade.php` 템플릿을 만들어 두세요.

단, 대체 오류 페이지는 Laravel이 내부적으로 전용 페이지를 제공하는 `404`, `500`, `503` 상태 코드에는 영향을 주지 않습니다. 이들 상태 코드에 대해 페이지를 커스터마이즈하려면 개별적으로 맞춤 오류 페이지를 정의해야 합니다.