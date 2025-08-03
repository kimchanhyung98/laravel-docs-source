# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 리포팅](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시하기](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [리포팅 가능 및 렌더링 가능 예외](#renderable-exceptions)
- [리포트 예외 제한하기](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

Laravel 프로젝트를 새로 시작하면, 에러와 예외 처리 기능이 이미 설정되어 있습니다. 하지만 필요에 따라 애플리케이션의 `bootstrap/app.php` 파일 내에서 `withExceptions` 메서드를 사용해 예외가 어떻게 리포팅되고 렌더링될지 관리할 수 있습니다.

`withExceptions` 클로저에 전달되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions` 클래스의 인스턴스이며, 애플리케이션 내 예외 처리 책임을 맡고 있습니다. 이 문서 전반에서 이 객체에 대해 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 에러에 대해 사용자에게 어느 정도 정보를 보여줄지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 사용하도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG` 값을 `true`로 설정해야 합니다. **그러나 운영 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 운영 환경에서 `true`로 설정하면 애플리케이션의 민감한 구성 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 리포팅

Laravel에서는 예외 리포팅이란 예외를 로그에 기록하거나 [Sentry](https://github.com/getsentry/sentry-laravel)나 [Flare](https://flareapp.io) 같은 외부 서비스로 보내는 작업입니다. 기본적으로 예외는 [로깅](/docs/master/logging) 설정에 따라 기록됩니다. 그러나 원하는 방식을 직접 정의해 로그를 남길 수 있습니다.

만약 서로 다른 예외 타입별로 리포팅 방식을 달리 하고 싶다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드를 사용해 특정 타입 예외 발생 시 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 보고 어떤 예외 타입인지 식별합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드를 사용해 커스텀 예외 리포팅 콜백을 등록해도, Laravel은 애플리케이션의 기본 로그 설정에 따라 예외를 여전히 로그에 기록합니다. 기본 로그 동작을 중단하고 싶다면 리포팅 콜백을 정의할 때 `stop` 메서드를 호출하거나 콜백에서 `false`를 반환하세요:

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
> 특정 예외 리포팅을 맞춤 설정하려면, [리포트 가능 예외](/docs/master/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

Laravel은 가능할 경우 매 예외 로그 메시지에 현재 로그인한 사용자의 ID를 자동으로 컨텍스트 데이터로 추가합니다. `bootstrap/app.php` 내 `context` 예외 메서드를 통해 직접 전역 컨텍스트 데이터를 정의할 수도 있습니다. 이렇게 하면 모든 예외 로그에 이 정보가 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 개별 예외 로그 컨텍스트

로그마다 컨텍스트를 추가하는 것이 유용하지만, 가끔 특정 예외만의 고유한 정보도 로그에 남기고 싶을 때가 있습니다. 이럴 때는 해당 예외 클래스에 `context` 메서드를 정의하여 예외 관련 데이터를 로그에 포함할 수 있습니다:

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

예외를 리포팅하되, 현재 요청 처리는 계속해야 할 경우가 있습니다. `report` 헬퍼 함수는 사용자에게 에러 페이지를 보여주지 않고 간단히 예외만 리포트할 때 사용합니다:

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
#### 중복 리포팅 방지

애플리케이션 전반에서 `report` 함수를 쓰다 보면 동일한 예외가 여러 번 리포트되어 로그에 중복 기록될 수 있습니다.

이걸 방지하려면 `bootstrap/app.php`의 `dontReportDuplicates` 예외 메서드를 호출하여 동일 인스턴스 예외는 한 번만 리포트되도록 설정하세요:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 같은 예외 인스턴스를 두 번째 이상 `report` 호출해도 무시됩니다:

```php
$original = new RuntimeException('Whoops!');

report($original); // 기록됨

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // 무시됨
}

report($original); // 무시됨
report($caught);   // 무시됨
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨

애플리케이션의 [로그](/docs/master/logging)에 메시지가 기록될 때, 그 메시지는 지정된 [로그 레벨](/docs/master/logging#log-levels)에 따라 저장됩니다. 이 레벨은 메시지의 심각도나 중요도를 나타냅니다.

앞서 언급했듯 `report`로 커스텀 예외 리포팅 콜백을 등록해도 Laravel은 기본 로그 설정에 따라 예외를 기록합니다. 하지만 로그 레벨에 따라 메시지가 기록되는 채널이 달라질 수 있으므로, 특정 예외가 기록될 로그 레벨을 설정하는 것이 유용할 수 있습니다.

이를 위해 `bootstrap/app.php` 내에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 예외 클래스, 두 번째 인자로 로그 레벨을 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시하기

애플리케이션에서 절대 리포트하고 싶지 않은 예외 타입이 있을 수 있습니다. 이럴 때는 `bootstrap/app.php`에서 `dontReport` 예외 메서드에 무시할 클래스 배열을 넘겨 무시할 수 있습니다. 단, 이 예외들은 여전히 커스텀 렌더링은 할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는, 예외 클래스에서 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현해 "표시"만 해도 Laravel이 해당 예외를 절대 리포팅하지 않습니다:

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

Laravel은 내부적으로 404 HTTP 예외, 419 HTTP (invalid CSRF token) 응답 등 일부 예외를 기본적으로 무시합니다. 이 기본 동작을 멈추고 싶을 때는 `stopIgnoring` 예외 메서드를 사용하세요:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환합니다. 그러나 특정 타입 예외에 대해 커스텀 렌더링 클로저를 등록할 수 있습니다. `bootstrap/app.php` 내 `render` 예외 메서드를 사용하세요.

`render`에 넘기는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼를 통해 쉽게 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 보고 어떤 예외 타입인지 식별합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

내장 Laravel 또는 Symfony 예외 (`NotFoundHttpException` 등)에 대해서도 `render` 메서드를 활용해 렌더링 동작을 덮어쓸 수 있습니다. 만약 클로저가 값을 반환하지 않으면 Laravel 기본 렌더러가 실행됩니다:

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
#### JSON 형식으로 예외 렌더링

예외를 렌더링할 때, Laravel은 클라이언트 요청의 `Accept` 헤더를 보고 예외를 HTML 또는 JSON 응답 중 어떤 형식으로 렌더링할지 자동으로 판단합니다. 이 동작을 직접 제어하려면 `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

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

가끔 Laravel 기본 예외 핸들러가 렌더링하는 전체 HTTP 응답을 완전히 커스터마이징할 필요가 생길 수 있습니다. 이 경우 `respond` 메서드에 응답 커스터마이징 클로저를 등록하세요:

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
### 리포팅 가능 및 렌더링 가능 예외

애플리케이션의 `bootstrap/app.php` 파일에서 직접 커스텀 예외 리포팅 및 렌더링을 정의하는 대신, 예외 클래스 내에 `report` 및 `render` 메서드를 정의할 수 있습니다. 이 메서드들이 존재하면 프레임워크가 자동으로 호출합니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외를 리포트합니다.
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

만약 예외가 이미 렌더링 가능한 부모 클래스를 상속하는 경우 (내장 Laravel 또는 Symfony 예외 등), `render` 메서드에서 `false`를 반환하면 프레임워크가 예외의 기본 HTTP 응답을 렌더링합니다:

```php
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 커스텀 렌더링 필요 판단 */) {

        return response(/* ... */);
    }

    return false;
}
```

비슷하게, 특정 조건에서만 커스텀 리포팅이 필요하다면 `report` 메서드에서 `false`를 반환해 Laravel이 기본 예외 처리 설정으로 리포팅하게 할 수 있습니다:

```php
/**
 * 예외를 리포트합니다.
 */
public function report(): bool
{
    if (/** 커스텀 리포팅 필요 판단 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 종속성을 타입 힌트로 지정하면 Laravel [서비스 컨테이너](/docs/master/container)가 자동으로 주입해줍니다.

<a name="throttling-reported-exceptions"></a>
### 리포트 예외 제한하기

애플리케이션에서 많은 수의 예외를 리포팅한다면, 얼마나 자주 리포팅할지 제한하고 싶을 수 있습니다.

무작위 확률 샘플링을 하려면 `bootstrap/app.php` 내에서 `throttle` 예외 메서드를 사용하세요. 이 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 받습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

특정 예외 타입에 대해서만 샘플링하려면, 그 클래스 인스턴스일 때만 `Lottery` 인스턴스를 반환할 수 있습니다:

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

또한 `Lottery` 대신 `Limit` 인스턴스를 반환해 리포트 속도를 제한할 수도 있습니다. 이는 예외가 갑자기 몰려 로그를 불필요하게 가득 채우는 상황, 예를 들어 제3자 서비스 장애 시 유용합니다:

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

기본적으로 `Limit`은 예외 클래스명을 Rate Limit 키로 사용합니다. 직접 키를 지정하려면 `Limit`의 `by` 메서드를 호출하세요:

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

`Lottery`와 `Limit`을 혼합해서 예외별로 다르게 적용하는 것도 가능합니다:

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

일부 예외는 서버에서 발생한 HTTP 에러 코드를 나타냅니다. 예를 들어 "페이지를 찾을 수 없음(404)", "권한 없음(401)", 개발자가 만든 500 에러 등이 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 여러 HTTP 상태 코드에 대해 쉽게 커스텀 에러 페이지를 보여줄 수 있게 지원합니다. 예를 들어, 404 오류 페이지를 바꾸려면 `resources/views/errors/404.blade.php` 뷰 파일을 생성하세요. 이렇게 하면 애플리케이션에서 발생하는 모든 404 에러에 대해 이 뷰가 렌더링됩니다. 이 디렉토리 내 뷰 파일명은 HTTP 상태 코드 번호와 일치해야 합니다. `abort`가 발생시킨 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있으며, 퍼블리시 후 원하는 대로 수정 가능합니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체 HTTP 에러 페이지

HTTP 상태 코드 범위별로 "대체(fallback)" 에러 페이지를 정의할 수도 있습니다. 이는 특정 HTTP 상태 코드 페이지가 없을 때 표시됩니다. 예를 들어 `resources/views/errors` 내 `4xx.blade.php`와 `5xx.blade.php` 파일을 정의하세요.

단, Laravel이 기본제공하는 404, 500, 503 오류 페이지는 내부에 전용 페이지가 있으므로, 이들에 대해 대체 페이지가 적용되지 않습니다. 이 오류 페이지들을 변경하려면 개별적으로 커스텀 에러 페이지를 만들어야 합니다.