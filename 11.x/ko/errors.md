# 오류 처리

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
- [보고된 예외 쓰로틀링](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작할 때, 오류 및 예외 처리는 이미 사전 구성되어 있습니다. 하지만 언제든지 애플리케이션의 `bootstrap/app.php`에서 `withExceptions` 메서드를 사용하여 예외가 어떻게 보고되고 렌더링되는지 관리할 수 있습니다.

`withExceptions` 클로저에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션의 예외 처리를 담당합니다. 이 문서에서는 이 객체에 대해 더 자세히 다룹니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 오류에 대한 정보가 얼마나 표시될지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수를 따르도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값이 반드시 `false`여야 합니다. 운영 환경에서 `true`로 설정되어 있으면, 민감한 설정 정보가 애플리케이션의 최종 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그로 남기거나 [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/{{version}}/logging) 구성에 따라 기록됩니다. 하지만 예외를 어떻게 처리할지는 자유롭게 결정할 수 있습니다.

각기 다른 예외 타입에 따라 다른 방식으로 보고가 필요하다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드를 사용하여 특정 타입의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입힌트를 확인하여 어떤 예외 타입을 처리하는지 결정합니다:

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->report(function (InvalidOrderException $e) {
            // ...
        });
    })

`report` 메서드를 이용해 커스텀 예외 보고 콜백을 등록하면 Laravel은 여전히 애플리케이션의 기본 로깅 구성을 사용해 예외를 기록합니다. 예외가 기본 로깅 스택으로 전파되는 것을 중단하고 싶다면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나, 콜백에서 `false`를 반환할 수 있습니다:

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->report(function (InvalidOrderException $e) {
            // ...
        })->stop();

        $exceptions->report(function (InvalidOrderException $e) {
            return false;
        });
    })

> [!NOTE]  
> 특정 예외에 대해 예외 보고를 커스터마이징하려면 [보고 및 렌더링 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 전체 로그 컨텍스트

가능하다면 Laravel은 자동으로 현재 사용자의 ID를 각 예외의 로그 메시지에 컨텍스트 데이터로 추가합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용하여 전체 예외 로그 메시지에 포함될 글로벌 컨텍스트 데이터를 정의할 수 있습니다:

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->context(fn () => [
            'foo' => 'bar',
        ]);
    })

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것이 유용할 수 있지만, 특정 예외에만 고유한 컨텍스트 정보가 필요할 때도 있습니다. 애플리케이션의 예외 클래스에 `context` 메서드를 정의하면 해당 예외에 대한 로그 항목에 포함시킬 데이터를 지정할 수 있습니다:

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

<a name="the-report-helper"></a>
#### `report` 헬퍼

가끔은 예외를 보고하되, 현재 요청 처리를 계속해야 할 때가 있습니다. `report` 헬퍼 함수는 에러 페이지를 렌더링하지 않고도 예외를 빠르게 보고할 수 있게 해줍니다:

    public function isValid(string $value): bool
    {
        try {
            // 값 검증...
        } catch (Throwable $e) {
            report($e);

            return false;
        }
    }

<a name="deduplicating-reported-exceptions"></a>
#### 중복 예외 보고 방지

애플리케이션 전반에서 `report` 함수를 사용하다보면, 같은 예외를 여러 번 보고하여 로그에 중복 항목이 생길 수 있습니다.

하나의 예외 인스턴스가 한 번만 보고되도록 보장하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 사용할 수 있습니다:

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->dontReportDuplicates();
    })

이제 동일한 예외 인스턴스로 `report` 헬퍼가 여러 번 호출되어도 처음 한 번만 보고됩니다:

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

애플리케이션의 [로그](/docs/{{version}}/logging)에 메시지가 기록될 때, 해당 로그는 [로그 레벨](/docs/{{version}}/logging#log-levels)에 따라 기록됩니다. 이 레벨은 메시지의 심각도나 중요도를 나타냅니다.

앞서 언급했듯, `report` 메서드로 커스텀 예외 보고 콜백을 등록해도 Laravel은 기본 로깅 구성을 사용해 예외를 기록합니다. 다만 로그 레벨이 메시지가 기록되는 채널에 영향을 줄 수 있으므로, 예외별로 로그 레벨을 지정하고 싶을 수 있습니다.

이를 위해, 애플리케이션의 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 예외 타입, 두 번째 인수로 로그 레벨을 받습니다:

    use PDOException;
    use Psr\Log\LogLevel;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->level(PDOException::class, LogLevel::CRITICAL);
    })

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 개발하다 보면, 일부 예외는 결코 보고하고 싶지 않을 때가 있습니다. 이런 예외는 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용해 무시할 수 있습니다. 여기에 등록된 클래스는 예외가 보고되지 않지만, 커스텀 렌더링 로직은 적용될 수 있습니다.

    use App\Exceptions\InvalidOrderException;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->dontReport([
            InvalidOrderException::class,
        ]);
    })

또 다른 방법으로, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현하도록 "마킹"할 수도 있습니다. 이 인터페이스가 마킹된 예외는 Laravel의 예외 핸들러에 의해 절대 보고되지 않습니다:

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

Laravel은 내부적으로 이미 404 HTTP 오류나, 잘못된 CSRF 토큰 등으로 발생한 419 응답에서 발생하는 특정 유형의 에러는 자동으로 무시합니다. 특정 예외 타입의 무시 처리를 중단하고 싶다면, 애플리케이션의 `bootstrap/app.php`에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

    use Symfony\Component\HttpKernel\Exception\HttpException;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->stopIgnoring(HttpException::class);
    })

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해줍니다. 하지만 특정 타입의 예외에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. 애플리케이션의 `bootstrap/app.php`에서 `render` 예외 메서드를 사용하세요.

`render` 메서드에 전달되는 클로저는 `Illuminate\Http\Response`의 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 보고 어떤 예외 타입인지 결정합니다:

    use App\Exceptions\InvalidOrderException;
    use Illuminate\Http\Request;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->render(function (InvalidOrderException $e, Request $request) {
            return response()->view('errors.invalid-order', status: 500);
        });
    })

`render` 메서드를 사용해 `NotFoundHttpException` 같은 Laravel 또는 Symfony의 내장 예외의 렌더링 동작도 오버라이드할 수 있습니다. 만약 `render` 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

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

<a name="rendering-exceptions-as-json"></a>
#### 예외를 JSON으로 렌더링

예외를 렌더링할 때 Laravel은 요청의 `Accept` 헤더를 기반으로 예외가 HTML이나 JSON 응답으로 렌더링되어야 하는지 자동으로 결정합니다. 만약 Laravel이 HTML과 JSON 예외 응답을 판별하는 방식을 커스터마이징하고 싶다면 `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

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

<a name="customizing-the-exception-response"></a>
#### 예외 응답 커스터마이징

드물기는 하지만, Laravel의 예외 핸들러가 렌더링하는 전체 HTTP 응답을 커스터마이징해야 할 때가 있습니다. 이럴 땐 `respond` 메서드를 사용해 응답 커스터마이징 클로저를 등록할 수 있습니다:

    use Symfony\Component\HttpFoundation\Response;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->respond(function (Response $response) {
            if ($response->getStatusCode() === 419) {
                return back()->with([
                    'message' => '페이지가 만료되었습니다. 다시 시도해 주세요.',
                ]);
            }

            return $response;
        });
    })

<a name="renderable-exceptions"></a>
### 보고 및 렌더링 가능한 예외

애플리케이션의 `bootstrap/app.php` 파일이 아닌, 직접 예외 클래스 내에 `report` 및 `render` 메서드를 정의할 수도 있습니다. 이 메서드들이 존재하면 프레임워크가 자동으로 호출합니다:

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

내장 Laravel 또는 Symfony 예외처럼 이미 렌더링 기능이 있는 예외를 확장할 경우, 예외 클래스의 `render` 메서드에서 `false`를 반환해 기본 HTTP 응답을 렌더링하도록 할 수 있습니다:

    /**
     * 예외를 HTTP 응답으로 렌더링합니다.
     */
    public function render(Request $request): Response|bool
    {
        if (/** 예외에 커스텀 렌더링이 필요한지 판단 */) {

            return response(/* ... */);
        }

        return false;
    }

예외에 커스텀 보고 로직이 있고, 특정 조건에서만 필요할 경우 Laravel에 기본 예외 처리 구성을 사용해 보고하도록 `report` 메서드에서 `false`를 반환하면 됩니다:

    /**
     * 예외를 보고합니다.
     */
    public function report(): bool
    {
        if (/** 예외에 커스텀 보고가 필요한지 판단 */) {

            // ...

            return true;
        }

        return false;
    }

> [!NOTE]  
> `report` 메서드는 의존성이 필요하면 타입힌트로 명시하면 됩니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 쓰로틀링

애플리케이션에서 매우 많은 수의 예외가 보고된다면, 실제로 로그에 기록하거나 외부 오류 추적 서비스로 전송되는 예외의 수를 제한하고 싶을 수 있습니다.

랜덤 샘플링 비율로 예외를 처리하려면 `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. 이 메서드는 `Lottery` 인스턴스를 반환해야 하는 클로저를 인수로 받습니다:

    use Illuminate\Support\Lottery;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            return Lottery::odds(1, 1000);
        });
    })

예외 타입별로 조건부 샘플링도 가능합니다. 특정 예외 클래스의 인스턴스만 샘플링하려면 해당 클래스에만 `Lottery` 인스턴스를 반환하면 됩니다:

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

또한, `Lottery` 대신 `Limit` 인스턴스를 반환하여 예외의 로그 기록 또는 외부 오류 추적 서비스 전송을 속도 제한할 수도 있습니다. 이는 예를 들어, 애플리케이션에서 사용하는 서드파티 서비스가 다운되었을 때 예외가 대량으로 쏟아지는 것을 방지하는 데 유용합니다:

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

기본적으로 제한은 예외 클래스명을 키로 사용합니다. `Limit`의 `by` 메서드를 통해 키를 직접 지정할 수도 있습니다:

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

물론, 여러 예외에 대해 `Lottery`와 `Limit` 인스턴스를 혼합해 반환할 수도 있습니다:

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

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버에서 발생한 HTTP 에러 코드를 나타냅니다. 예를 들어, "페이지를 찾을 수 없음" 오류(404), "인증되지 않은 에러"(401), 혹은 개발자에 의해 발생된 500 에러 등이 있습니다. 애플리케이션에서 어디서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

    abort(404);

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel에서는 다양한 HTTP 상태 코드에 대해 커스텀 오류 페이지를 쉽게 표시할 수 있습니다. 예를 들어, 404 상태 코드의 오류 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 파일을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 오류에 대해 렌더링됩니다. 이 디렉터리 내의 뷰는 각 HTTP 상태 코드에 해당하는 파일명으로 생성해야 합니다. `abort` 함수에서 발생된 `Symfony\Component\HttpKernel\Exception.HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

    <h2>{{ $exception->getMessage() }}</h2>

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어를 사용하여 퍼블리시할 수 있습니다. 퍼블리시 후에는 원하는 대로 템플릿을 커스터마이징할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 에러 페이지

특정 HTTP 상태 코드에 해당하는 에러 페이지가 없을 때를 대비하여, 해당 계열의 폴백 오류 페이지를 정의할 수도 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php`와 `5xx.blade.php` 템플릿을 추가합니다.

폴백 오류 페이지를 정의하더라도 404, 500, 503 오류 응답에는 영향을 미치지 않습니다. Laravel은 이 상태 코드들에 대해 내부적으로 별도의 전용 페이지를 가지고 있기 때문입니다. 이 상태 코드에 대한 렌더링 페이지를 커스터마이즈하려면 해당 코드별로 직접 에러 페이지를 정의해야 합니다.