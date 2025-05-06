# 에러 처리

- [소개](#introduction)
- [설정](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고](#reporting-exceptions)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
    - [타입별 예외 매핑](#mapping-exceptions-by-type)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작할 때, 에러 및 예외 처리는 이미 기본적으로 구성되어 있습니다. `App\Exceptions\Handler` 클래스는 애플리케이션에서 발생한 모든 예외를 기록하고, 이를 사용자에게 렌더링하는 역할을 합니다. 이 문서에서는 이 클래스에 대해 더 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 얼마나 많은 에러 정보를 보여줄지 결정합니다. 기본적으로, 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 프로덕션에서 `true`로 설정하면, 민감한 설정 값들이 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러

<a name="reporting-exceptions"></a>
### 예외 보고

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리됩니다. 이 클래스에는 커스텀 예외 보고 및 렌더링 콜백을 등록할 수 있는 `register` 메서드가 있습니다. 이번 단락에서는 각 개념을 자세히 살펴봅니다. 예외 보고는 예외를 기록하거나 [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel)와 같은 외부 서비스로 전송할 때 사용됩니다. 기본적으로는 [로깅](/docs/{{version}}/logging) 설정에 따라 예외가 기록됩니다. 하지만 원하는 방식으로 예외를 기록할 수도 있습니다.

예를 들어, 다양한 종류의 예외를 다른 방식으로 보고해야 할 경우, `reportable` 메서드를 사용해 해당 예외 타입에 대해 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 참고해 어떤 예외를 처리할지 추론합니다:

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

`reportable` 메서드를 사용하여 커스텀 예외 보고 콜백을 등록해도, Laravel은 기본 로깅 설정에 따라 예외를 계속 기록합니다. 만약 기본 로깅 스택으로의 예외 전파를 중단하고 싶다면, 보고 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

```php
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> {tip} 특정 예외에 대한 보고 방식을 커스터마이징하고 싶다면, [보고 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 글로벌 로그 컨텍스트

가능한 경우, Laravel은 현재 사용자의 ID를 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. `App\Exceptions\Handler` 클래스의 `context` 메서드를 오버라이드하여 자체 글로벌 컨텍스트 데이터를 정의할 수도 있습니다. 이 정보는 앱에서 기록되는 모든 예외 로그 메시지에 포함됩니다:

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

모든 로그 메시지에 컨텍스트를 추가하는 것이 유용할 때도 있지만, 특정 예외에만 고유한 컨텍스트 정보를 로그에 포함시키고 싶을 수 있습니다. 커스텀 예외에 `context` 메서드를 정의하면 해당 예외와 관련된 데이터를 로그 엔트리에 추가할 수 있습니다:

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

현재 요청 처리를 계속하면서 예외만 보고해야 할 때가 있습니다. `report` 헬퍼 함수를 사용하면 에러 페이지를 렌더링하지 않고도 예외를 빠르게 보고할 수 있습니다:

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

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시

애플리케이션을 구축할 때, 일부 예외 타입은 보고를 원하지 않을 수도 있습니다. 예외 핸들러의 `$dontReport` 속성(기본값은 빈 배열)에 추가한 클래스들은 보고되지 않습니다. 단, 렌더링 로직은 별도로 적용할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

/**
 * A list of the exception types that should not be reported.
 *
 * @var array
 */
protected $dontReport = [
    InvalidOrderException::class,
];
```

> {tip} Laravel은 이미 404 HTTP "not found" 에러나 잘못된 CSRF 토큰으로 인한 419 HTTP 응답과 같은 일부 오류 유형은 자동으로 무시합니다.

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환합니다. 하지만 특정 예외 타입에 대해 커스텀 렌더링 클로저를 등록할 수도 있습니다. 이는 예외 핸들러의 `renderable` 메서드로 구현할 수 있습니다.

`renderable` 메서드에 전달되는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 참고하여 처리할 예외 타입을 결정합니다:

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

`renderable` 메서드는 `NotFoundHttpException` 같은 Laravel 또는 Symfony 내장 예외의 렌더링 동작도 오버라이드할 수 있습니다. 만약 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

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
### 보고 및 렌더링 가능한 예외

예외 핸들러의 `register` 메서드에서 타입 체크를 하는 대신, 커스텀 예외에 `report`와 `render` 메서드를 직접 정의할 수도 있습니다. 이 메서드가 존재하면 프레임워크가 자동으로 호출합니다:

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
        return response(...);
    }
}
```

만약 이미 렌더링 기능이 있는 예외(Laravel 또는 Symfony 내장 예외)에서 상속한 경우, `render` 메서드에서 `false`를 반환하면 기본 HTTP 응답 렌더링이 실행됩니다:

```php
/**
 * Render the exception into an HTTP response.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function render($request)
{
    // 예외에 대해 커스텀 렌더링이 필요한 경우...

    return false;
}
```

특정 조건일 때만 커스텀 예외 보고가 필요하다면, `report` 메서드에서 `false`를 반환하여 기본 예외 처리 구성을 사용하도록 할 수 있습니다:

```php
/**
 * Report the exception.
 *
 * @return bool|null
 */
public function report()
{
    // 예외에 대해 커스텀 보고가 필요한 경우...

    return false;
}
```

> {tip} `report` 메서드에 필요한 의존성을 타입 힌트로 지정하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 주입해줍니다.

<a name="mapping-exceptions-by-type"></a>
### 타입별 예외 매핑

애플리케이션에서 사용하는 서드파티 라이브러리가 관리 권한이 없어 [렌더링](#renderable-exceptions) 할 수 없는 예외를 발생시킬 수 있습니다.

이럴 때는, 해당 예외를 앱에서 관리 가능한 다른 예외로 쉽게 매핑할 수 있습니다. 이는 예외 핸들러의 `register` 메서드에서 `map` 메서드를 사용해 구현합니다:

```php
use League\Flysystem\Exception;
use App\Exceptions\FilesystemException;

/**
 * Register the exception handling callbacks for the application.
 *
 * @return void
 */
public function register()
{
    $this->map(Exception::class, FilesystemException::class);
}
```

타깃 예외 생성 방식을 세밀하게 제어하려면, `map` 메서드에 클로저를 전달할 수도 있습니다:

```php
use League\Flysystem\Exception;
use App\Exceptions\FilesystemException;

$this->map(fn (Exception $e) => new FilesystemException($e));
```

<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버에서 발생한 HTTP 에러 코드를 설명합니다. 예를 들어, "페이지를 찾을 수 없음"(404), "권한 없음"(401), 혹은 개발자가 수동으로 발생시킨 500 에러일 수 있습니다. 애플리케이션 어디서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대한 커스텀 에러 페이지를 쉽게 표시할 수 있습니다. 예를 들어, 404 상태 코드에 대해 에러 페이지를 커스터마이즈하고 싶다면 `resources/views/errors/404.blade.php` 뷰 파일을 만들면 됩니다. 이 뷰는 앱에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉터리 안의 뷰 파일 이름은 해당 HTTP 상태 코드와 일치해야 합니다. `abort` 함수로 발생한 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` 아티즌 명령어로 퍼블리시 할 수 있습니다. 퍼블리시 후에는 원하는 대로 커스터마이즈할 수 있습니다:

```bash
php artisan vendor:publish --tag=laravel-errors
```