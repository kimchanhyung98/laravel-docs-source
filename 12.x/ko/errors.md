# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더 가능한 예외](#renderable-exceptions)
- [예외 보고 제한(Throttling)](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 라라벨 프로젝트를 시작할 때, 에러 및 예외 처리가 이미 미리 구성되어 있습니다. 하지만, 필요하다면 언제든 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용해 예외가 보고(로깅)되고 렌더링되는 방식을 관리할 수 있습니다.

`withExceptions` 클로저로 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions` 클래스의 인스턴스이며, 애플리케이션의 예외 처리를 담당합니다. 이 문서에서는 이 객체를 더 깊이 다루겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 어느 정도의 정보가 표시될지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정하는 것이 좋습니다. **하지만 운영 환경(프로덕션)에서는 반드시 이 값을 `false`로 해야 합니다. 만약 운영 환경에서 `true`로 설정하면, 애플리케이션의 중요한 설정 정보가 사용자에게 노출될 수 있으니 주의해야 합니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

라라벨에서는 예외 보고(exception reporting)란 예외를 로그에 기록하거나, [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io)와 같은 외부 서비스로 전송하는 것을 의미합니다. 기본적으로 예외는 [로깅](/docs/12.x/logging) 설정에 따라 기록됩니다. 물론, 원하는 방식대로 예외를 로그로 기록할 수 있습니다.

예외 종류별로 다른 방식으로 보고해야 할 때는, 애플리케이션의 `bootstrap/app.php` 파일에 `report` 예외 메서드를 사용해, 특정 타입의 예외가 보고되어야 할 때 실행할 클로저를 등록할 수 있습니다. 이때, 라라벨은 클로저의 타입힌트를 기반으로 어떤 예외 타입을 처리할지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드를 사용해 커스텀 예외 보고 콜백을 등록하더라도, 라라벨은 해당 예외를 기본 로깅 설정에 맞춰 여전히 기록합니다. 만약 예외가 기본 로깅 스택으로 전달되는 것을 중단하고 싶다면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다.

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
> 특정 예외의 보고 방식을 커스터마이즈하려면 [보고 및 렌더 가능한 예외](/docs/12.x/errors#renderable-exceptions)도 참고할 수 있습니다.

<a name="global-log-context"></a>
#### 글로벌 로그 컨텍스트

가능하다면, 라라벨은 현재 사용자의 ID를 모든 예외 로그 메시지에 컨텍스트 데이터로 자동 추가합니다. 직접 글로벌 컨텍스트 데이터를 정의하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용할 수 있습니다. 해당 데이터는 애플리케이션이 작성하는 모든 예외 로그 메시지에 포함됩니다.

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 개별 예외 로그 컨텍스트

모든 로그 메시지에 공통 데이터를 추가하는 것도 유용하지만, 특정 예외에만 기록하고 싶은 고유한 컨텍스트 데이터가 있을 수도 있습니다. 이런 경우에는, 애플리케이션의 예외 클래스 내에 `context` 메서드를 정의해 해당 예외만의 관련 데이터를 로그 항목에 추가할 수 있습니다.

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

특정 예외를 보고(로그 기록 등)하면서도 현재 요청 처리를 계속 진행해야 할 때가 있습니다. 이럴 때는 `report` 헬퍼 함수를 사용하여, 에러 페이지를 사용자에게 표시하지 않고도 예외를 빠르게 보고할 수 있습니다.

```php
public function isValid(string $value): bool
{
    try {
        // 값을 검증합니다...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 중복된 예외 보고 방지

애플리케이션 전체에서 `report` 함수를 사용하다 보면, 동일한 예외 인스턴스를 여러 번 보고하는 상황이 발생할 수 있습니다. 이럴 경우 로그에 중복된 항목이 생길 수 있습니다.

한번 생성된 예외 인스턴스가 단 한 번만 보고되도록 보장하고 싶다면, `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출하면 됩니다.

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스를 대상으로 `report` 헬퍼가 여러 번 호출되어도, 첫 번째 호출만 보고됩니다.

```php
$original = new RuntimeException('Whoops!');

report($original); // 기록됨

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

애플리케이션의 [로그](/docs/12.x/logging)에 메시지가 기록될 때, 메시지에는 [로그 레벨](/docs/12.x/logging#log-levels)이 지정되며, 이는 메시지의 심각도 또는 중요도를 나타냅니다.

앞서 설명했듯, `report` 메서드로 커스텀 예외 보고 콜백을 등록하더라도 라라벨은 여전히 기본 로깅 설정에 따라 예외를 기록합니다. 하지만, 로그 레벨에 따라 메시지가 기록되는 채널이 달라지기 때문에, 특정 예외의 로그 레벨을 설정하고 싶을 수 있습니다.

이럴 때는 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 첫 번째 인수로는 예외 타입, 두 번째 인수로는 로그 레벨을 전달합니다.

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 개발하다 보면, 특정 예외 타입은 아예 보고되지 않도록 하고 싶을 때가 있습니다. 이런 예외들은 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용해 무시할 수 있습니다. 여기에 지정된 클래스는 결코 보고되지 않지만, 커스텀 렌더링은 여전히 동작할 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현(implements)시키는 방법도 있습니다. 이 인터페이스가 적용된 예외는 라라벨의 예외 핸들러에 의해 절대 보고되지 않습니다.

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

특정 예외가 무시되는 조건을 더욱 세밀하게 제어하고 싶다면, `dontReportWhen` 메서드에 클로저를 전달할 수 있습니다.

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

라라벨은 기본적으로 404 HTTP 에러, 유효하지 않은 CSRF 토큰으로 인한 419 HTTP 응답 등 일부 오류 타입은 이미 무시하고 있습니다. 만약 특정 예외를 더 이상 무시하지 않도록 하고 싶다면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다.

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

라라벨의 예외 핸들러는 기본적으로 예외를 HTTP 응답으로 변환해줍니다. 하지만 특정 타입의 예외에 대해 직접 렌더링 로직을 등록할 수도 있습니다. 이를 위해 `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용할 수 있습니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. 라라벨은 클로저 타입힌트를 통해 어떤 예외를 렌더링할지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

또한 `render` 메서드를 활용해, `NotFoundHttpException`과 같은 라라벨이나 Symfony의 내장 예외에 대한 렌더링 동작을 오버라이드할 수도 있습니다. 만약 클로저가 값을 반환하지 않으면, 라라벨의 기본 예외 렌더링이 사용됩니다.

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

예외를 렌더링할 때 라라벨은 요청의 `Accept` 헤더를 기준으로, HTML 또는 JSON 응답 중 어떤 형식으로 렌더링할지 자동으로 결정합니다. 만약 라라벨이 HTML과 JSON 중 어떤 형식으로 예외를 렌더링할지 결정하는 방식을 커스터마이즈하고 싶다면, `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다.

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

특별한 경우, 라라벨의 예외 핸들러가 렌더링하는 HTTP 응답 전체를 수정해야 할 수도 있습니다. 이를 위해 `respond` 메서드에 응답을 수정하는 클로저를 등록할 수 있습니다.

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
### 보고 및 렌더 가능한 예외

애플리케이션의 `bootstrap/app.php` 파일에서 별도의 커스텀 보고 및 렌더링 동작을 정의하는 대신, 예외 클래스 자체에 `report`와 `render` 메서드를 정의할 수도 있습니다. 이 메서드들이 있으면 프레임워크가 자동으로 호출합니다.

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
     * 예외를 HTTP 응답으로 렌더링
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

만약 예외가 이미 렌더 가능한 예외(예: 라라벨/심포니의 내장 예외)를 상속받고 있다면, 예외 클래스의 `render` 메서드에서 `false`를 반환하여 기본 HTTP 응답 렌더링을 사용할 수 있습니다.

```php
/**
 * 예외를 HTTP 응답으로 렌더링
 */
public function render(Request $request): Response|bool
{
    if (/** 예외를 커스텀 렌더링해야 하는 경우 */) {

        return response(/* ... */);
    }

    return false;
}
```

예외에 커스텀 보고 로직이 있는데, 특정 조건에서만 기본 예외 처리 설정대로 보고하도록 할 필요가 있다면, 예외 클래스의 `report` 메서드에서 `false`를 반환하면 됩니다.

```php
/**
 * 예외 보고
 */
public function report(): bool
{
    if (/** 예외를 커스텀 보고해야 하는 경우 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 의존성을 타입힌트로 지정하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

<a name="throttling-reported-exceptions"></a>
### 예외 보고 제한(Throttling)

애플리케이션에서 매우 많은 예외가 보고되는 경우, 실제로 얼마나 많은 예외를 로그하거나 외부 에러 추적 서비스로 전송할지 제한(Throttle)하는 것이 좋습니다.

예외를 무작위 비율로 샘플링하여 보고하려면, `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. 이 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 받습니다.

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

특정 예외 타입에만 개별적으로 샘플링을 적용하고 싶다면, 해당 클래스에만 `Lottery` 인스턴스를 반환하면 됩니다.

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

또한 예외 로그 혹은 외부 추적 서비스로 전송되는 예외를 일정 비율로 제한(rate limit)하고 싶다면, `Lottery` 대신 `Limit` 인스턴스를 반환할 수 있습니다. 예를 들어, 외부 서비스 장애 등으로 인해 예외가 한꺼번에 쏟아지는 상황에서 로그가 몰리는 것을 막을 수 있습니다.

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

기본적으로 제한 키는 예외 클래스명이 사용됩니다. 직접 키를 지정하고 싶다면, `Limit`의 `by` 메서드를 사용하면 됩니다.

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

물론, 서로 다른 예외마다 `Lottery`와 `Limit`을 혼합해 반환할 수도 있습니다.

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

일부 예외는 서버에서 HTTP 에러 코드와 함께 반환되는 경우가 있습니다. 예를 들어, "페이지를 찾을 수 없습니다" 에러(404), "권한 없음" 에러(401), 또는 개발자가 생성한 500 에러 등이 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다.

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

라라벨은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 쉽게 표시할 수 있도록 해줍니다. 예를 들어, 404 상태 코드의 에러 페이지를 커스터마이즈 하려면, `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 랜더링됩니다. 이 디렉터리 내의 뷰 파일 명칭은 해당하는 HTTP 상태 코드와 일치해야 합니다. 또한, `abort` 함수로 발생시킨 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다.

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

라라벨의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어를 통해 프로젝트로 복사(퍼블리시)할 수 있습니다. 템플릿을 퍼블리시한 후에는 자유롭게 수정해서 사용할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백(fallback) HTTP 에러 페이지

한 범위에 해당하는 HTTP 상태 코드를 위한 "폴백(fallback)" 에러 페이지도 정의할 수 있습니다. 예를 들어, 명확하게 정의된 페이지가 없는 경우, 이 폴백 페이지가 사용됩니다. `resources/views/errors` 디렉터리에 `4xx.blade.php` 또는 `5xx.blade.php` 템플릿을 만들어 사용할 수 있습니다.

폴백 에러 페이지를 정의해도, 라라벨은 404, 500, 503 응답에 대해서는 내부적으로 별도의 전용 페이지를 사용합니다. 이 상태 코드에 대한 페이지를 커스터마이즈하려면, 각각 개별 파일로 에러 페이지를 생성해 주어야 합니다.