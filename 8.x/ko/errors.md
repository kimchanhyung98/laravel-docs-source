# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 핸들러](#the-exception-handler)
    - [예외 보고하기](#reporting-exceptions)
    - [타입별 예외 무시하기](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링 가능한 예외](#renderable-exceptions)
    - [타입별 예외 매핑](#mapping-exceptions-by-type)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면 에러와 예외 처리가 이미 구성되어 있습니다. `App\Exceptions\Handler` 클래스는 애플리케이션에서 발생한 모든 예외를 기록하고 사용자에게 렌더링하는 역할을 합니다. 이 문서 전체에서 이 클래스를 자세히 살펴보겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 실제로 보여줄 에러 정보의 양을 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따르도록 설정되어 있습니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 항상 `false`로 설정해야 하며, 만약 프로덕션에서 `true`로 설정하면 민감한 설정 값이 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
## 예외 핸들러

<a name="reporting-exceptions"></a>
### 예외 보고하기

모든 예외는 `App\Exceptions\Handler` 클래스에서 처리합니다. 이 클래스는 `register` 메서드를 포함하고 있으며, 여기서 커스텀 예외 보고 및 렌더링 콜백을 등록할 수 있습니다. 각각의 개념을 자세히 살펴보겠습니다. 예외 보고는 예외를 로그로 기록하거나 [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 예외는 [로깅](/docs/{{version}}/logging) 설정에 따라 기록됩니다. 그러나 자유롭게 원하는 방식으로 로그를 남길 수 있습니다.

예를 들어, 서로 다른 유형의 예외를 서로 다른 방식으로 보고해야 한다면, `reportable` 메서드를 사용해 특정 예외 타입에서 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 보고 어떤 종류의 예외인지 자동으로 추론합니다:

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

`reportable` 메서드를 사용해 커스텀 예외 보고 콜백을 등록해도, Laravel은 기본 로깅 설정을 사용해 계속 예외를 기록합니다. 만약 기본 로깅 스택으로의 전파를 멈추고 싶다면, 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

```
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!TIP]
> 특정 예외에 대한 예외 보고를 커스터마이징하려면 [보고 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

사용자가 있으면 Laravel은 자동으로 현재 사용자 ID를 각각의 예외 로그 메시지에 컨텍스트 데이터로 추가합니다. 애플리케이션의 `App\Exceptions\Handler` 클래스 내 `context` 메서드를 오버라이드하여 자체 전역 컨텍스트 데이터를 정의할 수도 있습니다. 이렇게 하면 애플리케이션이 남기는 모든 예외 로그에 이 정보가 포함됩니다:

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
#### 예외별 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것은 유용하지만, 특정 예외에만 적용할 특수한 컨텍스트가 필요할 때도 있습니다. 애플리케이션 커스텀 예외 클래스에 `context` 메서드를 정의하면, 해당 예외 로그 엔트리에 추가할 관련 데이터를 지정할 수 있습니다:

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

때때로 예외를 보고만 하고 현재 요청 처리는 계속 진행해야 할 때가 있습니다. `report` 헬퍼 함수는 사용자에게 에러 페이지를 렌더링하지 않고도 예외 핸들러를 통해 빠르게 예외를 보고할 수 있게 해줍니다:

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

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시하기

애플리케이션을 개발하다 보면 아예 보고하지 않고 무시하고 싶은 예외 종류가 있을 수 있습니다. 애플리케이션 예외 핸들러는 `$dontReport` 속성을 가진데, 기본적으로 빈 배열로 초기화되어 있습니다. 이 배열에 포함된 클래스들은 보고되지 않지만, 여전히 커스텀 렌더링 로직은 적용될 수 있습니다:

```
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

> [!TIP]
> Laravel은 내부적으로 404 HTTP "찾을 수 없음" 에러나, 유효하지 않은 CSRF 토큰으로 인해 발생하는 419 응답과 같은 몇 가지 예외를 이미 자동으로 무시합니다.

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해 줍니다. 그러나 특정 예외 타입에 대해 커스텀 렌더링 클로저를 등록하는 것도 가능합니다. 이는 예외 핸들러의 `renderable` 메서드를 통해 수행할 수 있습니다.

`renderable` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼 함수를 통해 생성할 수 있습니다. Laravel은 클로저 파라미터의 타입 힌트를 보고 어떤 예외 타입을 렌더링하는지 자동으로 인식합니다:

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

Laravel이나 Symfony 예외 클래스(`NotFoundHttpException` 등)에 대해서도 `renderable` 메서드를 이용해 렌더링 동작을 덮어쓸 수 있습니다. 만약 `renderable` 클로저가 값을 반환하지 않으면 Laravel의 기본 예외 렌더링이 사용됩니다:

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
### 보고 및 렌더링 가능한 예외

예외 핸들러 `register` 메서드 내에서 타입 체크를 하는 대신, 커스텀 예외 클래스에 직접 `report` 와 `render` 메서드를 정의할 수도 있습니다. 이 메서드들이 존재하면 프레임워크가 자동으로 호출합니다:

```
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    /**
     * 예외를 보고합니다.
     *
     * @return bool|null
     */
    public function report()
    {
        //
    }

    /**
     * 예외를 HTTP 응답으로 렌더링합니다.
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

만약 예외가 Laravel이나 Symfony의 기본 렌더링 가능한 예외를 상속받았다면, `render` 메서드에서 `false`를 반환하여 해당 예외의 기본 HTTP 응답을 렌더링할 수도 있습니다:

```
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function render($request)
{
    // 필요한 경우 커스텀 렌더링 동작 판단...

    return false;
}
```

커스텀 예외 보고 로직이 특정 조건에서만 실행되어야 할 때는, `report` 메서드에서 `false`를 반환하여 Laravel 기본 예외 처리 구성에 따라 예외를 보고하도록 할 수 있습니다:

```
/**
 * 예외를 보고합니다.
 *
 * @return bool|null
 */
public function report()
{
    // 필요한 경우 커스텀 보고 동작 판단...

    return false;
}
```

> [!TIP]
> `report` 메서드에 필요한 의존성을 타입 힌트하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 주입해 줍니다.

<a name="mapping-exceptions-by-type"></a>
### 타입별 예외 매핑

애플리케이션에서 사용하는 서드파티 라이브러리가 던지는 예외를 [렌더링 가능한 예외](#renderable-exceptions)로 만들고 싶지만, 해당 서드파티 예외 정의를 직접 수정할 수 없을 때가 있습니다.

다행히 Laravel은 이런 예외들을 애플리케이션 내에서 관리하는 다른 예외 타입으로 편리하게 매핑할 수 있게 해줍니다. 예외 핸들러의 `register` 메서드에서 `map` 메서드를 호출하여 수행할 수 있습니다:

```
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

목표 예외 생성 방식을 더 정교하게 제어하고 싶다면, 클로저를 `map` 메서드에 전달할 수도 있습니다:

```
use League\Flysystem\Exception;
use App\Exceptions\FilesystemException;

$this->map(fn (Exception $e) => new FilesystemException($e));
```

<a name="http-exceptions"></a>
## HTTP 예외

어떤 예외는 서버의 HTTP 에러 코드를 나타냅니다. 예를 들어 "페이지를 찾을 수 없음"(404), "권한 없음"(401), 또는 개발자가 생성한 500 에러가 이에 해당합니다. 애플리케이션 어디서든 이런 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 커스텀 에러 페이지를 손쉽게 표시하도록 도와줍니다. 예를 들어 404 HTTP 상태 코드의 에러 페이지를 커스터마이징하고 싶다면, `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉터리 내 뷰 파일들은 대응하는 HTTP 상태 코드와 일치하는 이름으로 만들어야 합니다. `abort` 함수가 던지는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 뷰에 `$exception` 변수로 전달됩니다:

```
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어를 사용해 퍼블리시할 수 있습니다. 템플릿을 퍼블리시한 후에는 원하는 대로 커스터마이징할 수 있습니다:

```
php artisan vendor:publish --tag=laravel-errors
```