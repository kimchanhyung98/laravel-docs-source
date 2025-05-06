# 오류 처리

- [소개](#introduction)
- [설정](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더 가능한 예외](#renderable-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면 오류 및 예외 처리가 이미 구성되어 있습니다. `App\Exceptions\Handler` 클래스는 애플리케이션에서 발생한 모든 예외를 로깅하고, 이를 사용자에게 렌더링하는 역할을 합니다. 이 문서에서는 이 클래스에 대해 자세히 다루겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자가 실제로 볼 수 있는 오류 정보의 양을 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따르도록 설정되어 있습니다.

로컬 개발 시에는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 운영 환경에서 `true`로 설정되어 있다면, 민감한 설정 값이 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러

<a name="reporting-exceptions"></a>
### 예외 보고

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리됩니다. 이 클래스는 예외 보고 및 렌더링 콜백을 등록할 수 있는 `register` 메서드를 포함합니다. 이 문서에서는 각각의 개념을 자세히 살펴봅니다. 예외 보고는 예외를 로그로 남기거나 [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel) 같은 외부 서비스에 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/{{version}}/logging) 설정에 따라 기록됩니다. 그러나 원하는 방식대로 예외를 기록할 수 있습니다.

예를 들어, 서로 다른 타입의 예외를 각기 다르게 보고해야 할 때 `reportable` 메서드를 사용하여 특정 타입의 예외가 보고될 때 실행되는 클로저(익명 함수)를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 확인하여 어떤 예외 타입을 처리하는지 유추합니다:

```php
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

`reportable` 메서드를 사용해 커스텀 예외 보고 콜백을 등록해도, Laravel은 여전히 애플리케이션의 기본 로깅 설정을 사용하여 예외를 기록합니다. 만약 기본 로깅 스택에 예외가 전달되는 것을 중단하고 싶다면, 콜백 정의 시 `stop` 메서드를 사용하거나, 콜백에서 `false`를 반환할 수 있습니다:

```php
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> **참고**  
> 특정 예외에 대한 예외 보고를 커스터마이징하려면 [보고 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)를 사용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

사용 가능한 경우, Laravel은 현재 사용자의 ID를 모든 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. `App\Exceptions\Handler` 클래스의 `context` 메서드를 오버라이드(재정의)하면 자신만의 전역 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션에서 기록하는 모든 예외 로그 메시지에 포함됩니다:

```php
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
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 특정 예외에만 포함하고 싶은 고유 컨텍스트가 있을 때도 있습니다. 애플리케이션의 커스텀 예외에 `context` 메서드를 정의하면 해당 예외에 관련된 모든 데이터를 예외 로그 엔트리에 추가할 수 있습니다:

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

때로는 예외를 보고하고 나서도 현재 요청 처리를 계속 진행해야 할 수도 있습니다. `report` 헬퍼 함수는 예외 핸들러를 통해 사용자에게 오류 페이지를 렌더링하지 않고도 예외를 빠르게 보고할 수 있게 해줍니다:

```php
public function isValid($value)
{
    try {
        // 값 검증...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨

애플리케이션의 [로그](/docs/{{version}}/logging)에 메시지를 기록할 때, 로그가 기록되는 [로그 레벨](/docs/{{version}}/logging#log-levels)이 지정되며, 이는 메시지의 심각도 또는 중요도를 나타냅니다.

앞서 언급한 것처럼, `reportable` 메서드를 사용해 커스텀 예외 보고 콜백을 등록하더라도 Laravel은 여전히 애플리케이션의 기본 로그 설정을 사용하여 예외를 기록합니다. 하지만 로그 레벨이 메시지가 기록되는 채널에 영향을 미칠 수 있기 때문에, 특정 예외의 로그 레벨을 설정하고 싶을 수 있습니다.

이를 위해 애플리케이션 예외 핸들러의 `$levels` 속성에 예외 타입과 해당하는 로그 레벨을 배열로 정의할 수 있습니다:

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

애플리케이션을 개발하다 보면 일부 예외 타입은 단순히 무시하고, 보고하지 않도록 하고 싶을 수 있습니다. 예외 핸들러에는 기본값이 빈 배열인 `$dontReport` 속성이 있습니다. 이 속성에 추가된 클래스들은 보고되지 않습니다. 단, 별도의 렌더링 로직은 가질 수 있습니다:

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

> **참고**  
> 내부적으로 Laravel은 404 HTTP "찾을 수 없음" 오류나, 잘못된 CSRF 토큰으로 생성된 419 응답 등 일부 오류 유형을 이미 자동 무시합니다.

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해줍니다. 하지만 특정 타입의 예외에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. 예외 핸들러의 `renderable` 메서드를 통해 이를 구현할 수 있습니다.

`renderable` 메서드에 전달되는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼를 사용해 생성할 수 있습니다. Laravel은 마찬가지로 클로저의 타입 힌트를 통해 어떤 예외를 처리하는지 유추합니다:

```php
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

`renderable` 메서드를 사용해 `NotFoundHttpException`과 같은 Laravel 또는 Symfony의 기본 예외의 렌더링 동작을 오버라이드할 수도 있습니다. 만약 `renderable` 메서드에 전달된 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

```php
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
### 보고 및 렌더 가능한 예외

예외 핸들러의 `register` 메서드에서 예외 타입 검사를 하는 대신, 커스텀 예외 클래스에 직접 `report` 및 `render` 메서드를 정의할 수 있습니다. 이러한 메서드가 존재하면 프레임워크에서 자동으로 호출해줍니다:

```php
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

이미 렌더 가능한 Laravel 또는 Symfony의 내장 예외를 상속한 경우, `render` 메서드에서 `false`를 반환하면 해당 예외의 기본 HTTP 응답을 렌더링합니다:

```php
/**
 * Render the exception into an HTTP response.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function render($request)
{
    // 예외에 커스텀 렌더링이 필요한 경우 판단...

    return false;
}
```

예외에 특정 조건에서만 필요한 커스텀 보고 로직이 있는 경우, `report` 메서드에서 `false`를 반환하여 Laravel에서 기본 예외 처리 설정을 사용하도록 할 수 있습니다:

```php
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

> **참고**  
> `report` 메서드에 필요한 의존성을 타입힌트로 지정하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 주입해줍니다.

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버의 HTTP 오류 코드를 나타냅니다. 예를 들어 "페이지를 찾을 수 없음"(404), "인증 오류"(401), 개발자가 직접 발생시키는 500 오류 등이 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 오류 페이지

Laravel에서는 다양한 HTTP 상태 코드에 대해 커스텀 오류 페이지를 쉽게 표시할 수 있습니다. 예를 들어 404 HTTP 상태 코드의 오류 페이지를 커스터마이즈하려면, `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생한 모든 404 오류에 대해 렌더링됩니다. 이 디렉터리 내의 뷰들은 해당하는 HTTP 상태 코드와 이름이 일치해야 합니다. `abort` 함수에 의해 발생된 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

`vendor:publish` 아티즌 명령어를 사용해, Laravel의 기본 오류 페이지 템플릿을 퍼블리시할 수 있습니다. 템플릿을 퍼블리시한 후에는 원하는 대로 커스터마이즈하면 됩니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 오류 페이지

특정 HTTP 상태 코드에 해당하는 페이지가 없는 경우를 위해, 해당 코드 계열에 대한 "폴백" 오류 페이지를 정의할 수도 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php` 및 `5xx.blade.php` 템플릿을 생성하면 됩니다.