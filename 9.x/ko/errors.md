# 오류 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [예외 유형별 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [Reportable & Renderable 예외](#renderable-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면, 오류 및 예외 처리가 이미 설정되어 있습니다. `App\Exceptions\Handler` 클래스는 애플리케이션에서 발생하는 모든 예외를 기록하고 사용자에게 보여줄 응답으로 변환하는 역할을 합니다. 이 문서 내내 이 클래스에 대해 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 구성 파일의 `debug` 옵션은 오류에 대해 사용자에게 얼마나 많은 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따르도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 반드시 이 값을 `false`로 설정해야 하며, 만약 운영 환경에서 `true`로 설정하면 민감한 구성 정보가 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러 (The Exception Handler)

<a name="reporting-exceptions"></a>
### 예외 보고 (Reporting Exceptions)

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리합니다. 이 클래스에는 `register` 메서드가 있으며, 여기서 사용자 정의 예외 보고 및 렌더링 콜백을 등록할 수 있습니다. 각 개념을 자세히 살펴보겠습니다. 예외 보고는 예외를 로그에 기록하거나 외부 서비스([Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel) 등)로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/9.x/logging) 설정에 따라 기록되지만, 원한다면 자유롭게 보고 방식을 지정할 수 있습니다.

예를 들어, 서로 다른 유형의 예외를 다르게 보고해야 하는 경우, `reportable` 메서드를 사용하여 특정 예외 유형이 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입힌트를 보고 어떤 예외 유형인지 자동으로 추론합니다:

```
use App\Exceptions\InvalidOrderException;

/**
 * Register the exception handling callbacks for the application.
 *
 * @return void
 */
public function register()
{
    $this->reportable(function (InvalidOrderException $e) {
        //
    });
}
```

`reportable` 메서드로 사용자 정의 예외 보고 콜백을 등록해도 Laravel은 여전히 애플리케이션의 기본 로깅 설정을 사용해 예외를 기록합니다. 기본 로그 기록으로의 예외 전파를 중단하려면, 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

```
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!NOTE]
> 특정 예외의 예외 보고를 맞춤화하려면 [reportable 예외](/docs/9.x/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트 (Global Log Context)

Laravel은 사용자가 로그인했을 경우 모든 예외 로그 메시지에 현재 사용자 ID를 컨텍스트 데이터로 자동 추가합니다. 애플리케이션의 `App\Exceptions\Handler` 클래스에서 `context` 메서드를 오버라이드하여 자신만의 전역 컨텍스트 데이터를 정의할 수 있습니다. 이렇게 하면 애플리케이션에서 기록하는 모든 예외 로그 메시지에 이 정보가 포함됩니다:

```
/**
 * Get the default context variables for logging.
 *
 * @return array
 */
protected function context()
{
    return array_merge(parent::context(), [
        'foo' => 'bar',
    ]);
}
```

<a name="exception-log-context"></a>
#### 예외 로그 컨텍스트 (Exception Log Context)

모든 로그 메시지에 컨텍스트를 추가하는 것이 유용할 수 있지만, 때로는 특정 예외에만 고유한 컨텍스트를 포함하고 싶을 때가 있습니다. 사용자 정의 예외 클래스에 `context` 메서드를 정의하면 그 예외에 관련된 데이터를 예외 로그 항목에 포함시킬 수 있습니다:

```
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * Get the exception's context information.
     *
     * @return array
     */
    public function context()
    {
        return ['order_id' => $this->orderId];
    }
}
```

<a name="the-report-helper"></a>
#### `report` 헬퍼

가끔 예외를 보고(기록)하되 현재 요청 처리는 계속해야 할 때가 있습니다. `report` 헬퍼 함수는 예외 핸들러를 통해 예외를 빠르게 보고할 수 있게 해주며, 사용자에게 오류 페이지를 보여주지 않습니다:

```
public function isValid($value)
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨 (Exception Log Levels)

애플리케이션의 [로그](/docs/9.x/logging) 메시지는 특정 [로그 레벨](/docs/9.x/logging#log-levels)에 따라 기록됩니다. 이 레벨은 로그 메시지의 심각도나 중요도를 나타냅니다.

앞서 언급한 바와 같이 `reportable` 메서드로 사용자 정의 예외 보고 콜백을 등록해도, Laravel은 여전히 기본 로깅 설정을 사용해 예외를 기록합니다. 하지만 로그 레벨에 따라 로그 메시지가 기록되는 채널에 영향을 줄 수 있으므로, 특정 예외가 기록될 로그 레벨을 설정하고 싶을 수 있습니다.

이를 위해 애플리케이션의 예외 핸들러에 `$levels` 속성 배열을 정의하여, 예외 유형별로 로그 레벨을 지정할 수 있습니다:

```
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
### 예외 유형별 무시 (Ignoring Exceptions By Type)

애플리케이션을 개발하다 보면, 아예 보고하지 않고 무시하고 싶은 예외 유형도 있을 수 있습니다. 예외 핸들러에는 `$dontReport` 속성이 빈 배열로 초기화되어 있는데, 여기에 지정한 클래스들은 절대 보고되지 않습니다. 다만, 여전히 사용자 정의 렌더링 로직은 가질 수 있습니다:

```
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

> [!NOTE]
> Laravel은 이미 내부적으로 404 HTTP "찾을 수 없음" 예외나 무효한 CSRF 토큰으로 인해 발생하는 419 HTTP 응답 예외 등을 자동으로 무시하고 있습니다.

<a name="rendering-exceptions"></a>
### 예외 렌더링 (Rendering Exceptions)

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환합니다. 하지만 특정 예외 유형에 대해 사용자 정의 렌더링 클로저를 등록할 수 있습니다. 이는 예외 핸들러의 `renderable` 메서드를 통해 할 수 있습니다.

`renderable` 메서드에 전달된 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼를 통해 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 보고 어떤 예외 유형에 대해 렌더링하는지 자동으로 추론합니다:

```
use App\Exceptions\InvalidOrderException;

/**
 * Register the exception handling callbacks for the application.
 *
 * @return void
 */
public function register()
{
    $this->renderable(function (InvalidOrderException $e, $request) {
        return response()->view('errors.invalid-order', [], 500);
    });
}
```

내장된 Laravel 또는 Symfony 예외(`NotFoundHttpException` 등)에 대한 렌더링 동작을 덮어쓸 수도 있습니다. 만약 클로저가 값을 반환하지 않으면 Laravel의 기본 예외 렌더링이 사용됩니다:

```
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Register the exception handling callbacks for the application.
 *
 * @return void
 */
public function register()
{
    $this->renderable(function (NotFoundHttpException $e, $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
}
```

<a name="renderable-exceptions"></a>
### Reportable & Renderable 예외

예외 핸들러의 `register` 메서드에서 타입 검사를 하지 않고, 사용자 정의 예외 클래스에 직접 `report` 및 `render` 메서드를 정의할 수 있습니다. 이 메서드들이 존재하면 프레임워크가 자동으로 호출합니다:

```
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     *
     * @return bool|null
     */
    public function report()
    {
        //
    }

    /**
     * Render the exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function render($request)
    {
        return response(/* ... */);
    }
}
```

이미 렌더링 가능한 예외(예: Laravel 또는 Symfony 내장 예외)를 확장한 경우, 예외의 기본 HTTP 응답을 렌더링하려면 `render` 메서드에서 `false`를 반환하면 됩니다:

```
/**
 * Render the exception into an HTTP response.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function render($request)
{
    // 커스텀 렌더링이 필요한지 판단...

    return false;
}
```

특정 조건에서만 필요한 커스텀 보고 로직이 있는 경우, 예외의 `report` 메서드에서 `false`를 반환하여 Laravel이 기본 예외 처리 설정으로 예외를 보고하도록 할 수 있습니다:

```
/**
 * Report the exception.
 *
 * @return bool|null
 */
public function report()
{
    // 커스텀 보고가 필요한지 판단...

    return false;
}
```

> [!NOTE]
> `report` 메서드의 매개변수로 필요한 의존성을 타입힌트하면, Laravel의 [서비스 컨테이너](/docs/9.x/container)가 자동으로 주입해 줍니다.

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버에서 발생하는 HTTP 에러 코드를 나타냅니다. 예를 들어, "페이지를 찾을 수 없음" (404), "인가되지 않음" (401), 또는 개발자가 발생시킨 500 에러 등이 있습니다. 애플리케이션 어디서든 이런 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 맞는 커스텀 에러 페이지를 쉽게 표시할 수 있도록 지원합니다. 예를 들어, 404 HTTP 상태 코드에 대한 에러 페이지를 커스터마이징하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 만들어야 합니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉토리 내 뷰 파일 이름은 대응하는 HTTP 상태 코드와 일치해야 합니다. `abort` 함수가 발생시키는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어를 통해 퍼블리시할 수 있습니다. 템플릿이 퍼블리시된 후에는 자유롭게 수정할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 에러 페이지

특정 HTTP 상태 코드에 대응하는 페이지가 없을 때 렌더링할 "폴백" 에러 페이지를 정의할 수도 있습니다. 이를 위해 `resources/views/errors` 디렉토리에 `4xx.blade.php`와 `5xx.blade.php` 템플릿 파일을 생성하면, 해당 상태 코드 범위에 속하는 에러가 발생할 때 이 뷰가 렌더링됩니다.