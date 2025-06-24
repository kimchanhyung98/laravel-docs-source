# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [에러 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싼 표현력 있고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 빠르게 만들 수 있습니다. 라라벨의 Guzzle 래퍼는 가장 일반적인 사용 사례와 훌륭한 개발자 경험에 집중되어 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해서는 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 등의 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체를 이용해 응답을 다양한 방식으로 확인할 수 있습니다.

```php
$response->body() : string;
$response->json($key = null, $default = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, JSON 응답 데이터를 마치 배열처럼 직접 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 설명한 응답 메서드 이외에도, 응답의 상태 코드가 특정 값인지 확인할 때 아래 메서드들을 사용할 수 있습니다.

```php
$response->ok() : bool;                  // 200 OK
$response->created() : bool;             // 201 Created
$response->accepted() : bool;            // 202 Accepted
$response->noContent() : bool;           // 204 No Content
$response->movedPermanently() : bool;    // 301 Moved Permanently
$response->found() : bool;               // 302 Found
$response->badRequest() : bool;          // 400 Bad Request
$response->unauthorized() : bool;        // 401 Unauthorized
$response->paymentRequired() : bool;     // 402 Payment Required
$response->forbidden() : bool;           // 403 Forbidden
$response->notFound() : bool;            // 404 Not Found
$response->requestTimeout() : bool;      // 408 Request Timeout
$response->conflict() : bool;            // 409 Conflict
$response->unprocessableEntity() : bool; // 422 Unprocessable Entity
$response->tooManyRequests() : bool;     // 429 Too Many Requests
$response->serverError() : bool;         // 500 Internal Server Error
```

<a name="uri-templates"></a>
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 활용하여 요청 URL을 만들 수 있도록 지원합니다. URI 템플릿에서 확장할 수 있는 URL 파라미터를 정의하려면, `withUrlParameters` 메서드를 사용하면 됩니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 정보 Dump

요청을 전송하기 전에 해당 요청 인스턴스의 정보를 dump 하고, 스크립트 실행을 종료하고자 한다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터도 함께 전송하게 됩니다. 이 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로, 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때는 URL에 쿼리 문자열을 직접 추가하거나, 두 번째 인수로 키-값 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는, `withQueryParameters` 메서드도 사용할 수 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내려면, 요청 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 바디로 요청 보내기

요청 시 raw 데이터를 바디로 직접 전달하고 싶다면, `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인수로 지정할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 전송하려면 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 파일 내용을 인수로 받습니다. 필요한 경우, 세 번째 인수에 파일의 실제 파일명을, 네 번째 인수에는 파일 관련 헤더를 배열로 추가할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원본 내용을 직접 전달하는 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 메서드는 키-값 쌍이 담긴 배열을 인수로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 원하는 콘텐츠 타입을 명시적으로 지정하려면 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

간단히, `acceptJson` 메서드를 사용하여 응답에서 `application/json` 타입을 기대한다고 빠르게 명시할 수도 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새로운 헤더를 병합합니다. 필요하다면 `replaceHeaders` 메서드를 사용해 모든 헤더를 완전히 대체할 수도 있습니다.

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<a name="authentication"></a>
### 인증

기본 인증과 Digest 인증 자격 증명은 각각 `withBasicAuth`와 `withDigestAuth` 메서드를 이용해 지정할 수 있습니다.

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 손쉽게 추가하고 싶다면, `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답을 기다릴 최대 초(second) 수를 지정하려면 `timeout` 메서드를 사용합니다. 기본적으로 HTTP 클라이언트는 30초가 지나면 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

설정한 타임아웃을 초과할 경우, `Illuminate\Http\Client\ConnectionException`이 발생합니다.

서버에 연결을 시도할 때 대기할 최대 초(second) 수는 `connectTimeout` 메서드로 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 혹은 서버 오류가 발생했을 때 HTTP 클라이언트가 자동으로 요청을 재시도하게 하려면, `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청을 최대 몇 번 재시도할지, 그리고 각 시도 사이에 라라벨이 몇 밀리초 대기할지 지정합니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이에 대기할 밀리초를 직접 계산하려면, `retry` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

보다 간단하게, 첫 번째 인수에 배열을 전달하면 해당 배열의 값(밀리초)을 재시도 사이마다 사용할 수 있습니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드에 세 번째 인수로 콜러블을 전달할 수 있으며, 해당 콜러블에서 실제로 재시도를 진행할지 판단할 수 있습니다. 예를 들어, 첫 요청에서 `ConnectionException`이 발생했을 때만 재시도하려면 아래와 같이 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패할 때마다 재시도 전에 요청을 수정하고 싶을 때는, `retry` 메서드에 전달하는 콜러블에서 인자로 받은 요청 객체를 조작하면 됩니다. 예를 들어, 첫 번째 시도가 인증 오류(401)를 반환한다면 새로운 인증 토큰으로 요청을 재실행하도록 변경할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Exception $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

만약 모든 요청이 실패한다면 `Illuminate\Http\Client\RequestException` 인스턴스가 던져집니다. 이 동작을 비활성화하려면 `throw` 옵션 값을 `false`로 지정하면 됩니다. 비활성화 시, 모든 재시도가 끝난 후 마지막 응답 객체가 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는, `throw` 값을 `false`로 지정했더라도 `Illuminate\Http\Client\ConnectionException`이 여전히 던져집니다.

<a name="error-handling"></a>
### 에러 처리

기본적으로 Guzzle과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버로부터의 `400` 및 `500`번대 응답)일 때 예외를 던지지 않습니다. 이러한 오류가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 메서드를 사용할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 응답이 400번대 상태 코드인지 확인...
$response->clientError();

// 응답이 500번대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 발생했다면 주어진 콜백을 바로 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스를 가지고 있으며, 상태 코드에 따라 클라이언트 또는 서버 오류가 발생하면 `Illuminate\Http\Client\RequestException` 예외를 던지려면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트나 서버 오류가 발생했다면 예외 발생...
$response->throw();

// 오류가 발생하고 해당 조건이 true이면 예외 발생...
$response->throwIf($condition);

// 오류가 발생하고 전달된 클로저가 true를 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생하고 해당 조건이 false이면 예외 발생...
$response->throwUnless($condition);

// 오류가 발생하고 전달된 클로저가 false를 반환하면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답의 상태 코드가 특정 값일 때 예외 발생...
$response->throwIfStatus(403);

// 응답의 상태 코드가 특정 값이 아닐 때 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 확인할 수 있는 public `$response` 속성이 있습니다.

`throw` 메서드는 오류가 없을 경우 응답 인스턴스를 반환하므로, `throw` 메서드 뒤에 다른 작업을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 실행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 실행된 후 예외는 자동으로 던져지므로, 클로저 안에서 예외를 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그나 리포트 시 120자로 잘려 표시됩니다. 이 동작을 커스터마이즈하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지를 최대 240자로 잘라서 기록...
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 잘라내기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또는 요청별로 예외 메시지 잘라내는 동작을 커스터마이즈하려면, `truncateExceptionsAt` 메서드를 사용할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨의 HTTP 클라이언트는 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

반대로, 들어오는 HTTP 응답을 검사하고 싶다면, `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```

<a name="global-middleware"></a>
#### 전역 미들웨어

때때로, 모든 나가는 요청과 들어오는 응답에 공통으로 적용되는 미들웨어를 등록하고 싶을 수 있습니다. 이럴 때는 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 적합합니다.

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a name="guzzle-options"></a>
### Guzzle 옵션

나가는 요청에 대해 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 설정하려면 `withOptions` 메서드를 사용하면 됩니다. 이 메서드는 키-값 쌍이 담긴 배열을 인수로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 나가는 요청에 기본 옵션을 설정하고 싶다면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a name="concurrent-requests"></a>
## 동시 요청

여러 HTTP 요청을 동시에 처리하고 싶을 때가 있습니다. 즉, 요청을 순차적으로 보내는 것이 아니라 여러 요청을 한꺼번에 발송하여, 느린 HTTP API와 상호작용할 때 성능을 크게 향상할 수 있습니다.

다행히 `pool` 메서드를 사용하면 이를 쉽게 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 인수로 받는 클로저를 받고, 이 풀에 요청을 추가하여 동시에 발송할 수 있습니다.

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->get('http://localhost/first'),
    $pool->get('http://localhost/second'),
    $pool->get('http://localhost/third'),
]);

return $responses[0]->ok() &&
       $responses[1]->ok() &&
       $responses[2]->ok();
```

보시다시피, 각 응답 인스턴스는 풀에 추가한 순서대로 접근할 수 있습니다. 필요하다면, `as` 메서드를 사용해 요청에 이름을 부여한 뒤, 해당 이름으로 응답을 참조할 수도 있습니다.

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이즈

`pool` 메서드는 `withHeaders`나 `middleware` 등 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 만약 풀로 처리하는 각 요청에 커스텀 헤더나 미들웨어를 적용하고 싶다면, 풀 내 각 요청에 직접 옵션을 지정해야 합니다.

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```

<a name="macros"></a>
## 매크로

라라벨 HTTP 클라이언트는 "매크로" 기능을 지원합니다. 매크로는 서비스와 상호작용할 때 자주 사용하는 요청 경로와 헤더 설정을 손쉽게 구성하는 방법이 될 수 있습니다. 사용을 시작하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 매크로를 정의하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

이제 미리 정의한 매크로를 애플리케이션 어디에서나 호출해, 지정된 환경설정으로 Pending Request를 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

## 테스트

라라벨의 다양한 서비스는 테스트를 쉽고 명확하게 작성할 수 있도록 여러 기능을 제공하며, 라라벨 HTTP 클라이언트도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 실제로 요청이 발생했을 때 미리 정해진 가짜(스텁) 응답을 반환하도록 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리

예를 들어, 모든 요청에 대해 비어 있고 HTTP 상태 코드가 `200`인 응답을 반환하도록 하려면 `fake` 메서드를 아무 인자 없이 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 가짜 처리

또는 `fake` 메서드에 배열을 전달할 수도 있습니다. 배열의 키는 가짜 처리를 적용할 URL 패턴이며, 값은 해당 URL 패턴에 대한 응답입니다. `*` 문자를 와일드카드로 활용할 수 있습니다. 가짜 처리가 지정되지 않은 URL로의 요청은 실제로 실행됩니다. `Http` 파사드의 `response` 메서드를 사용해 해당 엔드포인트에 대한 가짜(스텁) 응답을 생성할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 문자열 응답 스텁...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

매치되지 않은 모든 URL에 대해 예비(기본) URL 패턴을 적용하고 싶다면, `*` 하나만 사용하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 다른 모든 엔드포인트에 문자열 응답 스텁...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편리하게도, 간단한 문자열, JSON, 비어 있는 응답 등은 문자열, 배열, 정수 등을 응답으로 바로 지정할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트해야 하는 경우가 있습니다. `failedConnection` 메서드를 사용해 HTTP 클라이언트가 연결 예외를 던지도록 할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`이 발생하는 경우를 테스트하고 싶다면, `failedRequest` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 순차 응답 가짜 처리

특정 URL이 여러 개의 가짜 응답을 지정된 순서대로(순차적으로) 반환하도록 하고 싶을 수 있습니다. 이럴 때는 `Http::sequence` 메서드를 사용해서 응답 시퀀스를 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 순차 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스에 등록한 모든 응답이 소진되면, 이후의 요청에 대해서는 예외가 발생합니다. 만약 시퀀스가 비어있을 때 기본적으로 반환할 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 순차 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 순차 응답 가짜 처리를 하고 싶을 경우, `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 콜백을 이용한 가짜 처리

특정 엔드포인트에 대해 반환할 응답을 더 복잡한 로직에 따라 결정해야 하는 경우, `fake` 메서드에 클로저(익명 함수)를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아서 적절한 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 원하는 만큼의 로직을 구현해, 어떤 응답을 반환할지 결정할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

가짜 응답을 설정했을 때, 클라이언트가 실제로 어떤 요청을 보냈는지 확인하고 싶을 때가 있습니다. 애플리케이션에서 올바른 데이터나 헤더를 전송하고 있는지 검증하려면, `Http::fake` 호출 후에 `Http::assertSent` 메서드를 사용할 수 있습니다.

`assertSent` 메서드는 클로저를 인자로 받습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인자로 받고, 기대에 부합하는 요청이면 `true`를 반환해야 합니다. 해당 조건에 맞는 요청이 하나 이상 존재해야 테스트가 통과합니다.

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::withHeaders([
    'X-First' => 'foo',
])->post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertSent(function (Request $request) {
    return $request->hasHeader('X-First', 'foo') &&
           $request->url() == 'http://example.com/users' &&
           $request['name'] == 'Taylor' &&
           $request['role'] == 'Developer';
});
```

특정한 요청이 전송되지 않았음을 검사하고 싶다면, `assertNotSent` 메서드를 사용하면 됩니다.

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```

`assertSentCount` 메서드를 사용해 테스트에서 "전송된" 요청의 횟수를 검증할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또한, 테스트 중에 어떠한 요청도 발생하지 않아야 하는 경우에는 `assertNothingSent` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록하기

`recorded` 메서드를 사용하면 모든 요청 및 해당 요청에 대한 응답을 모아서 확인할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 포함하는 배열의 컬렉션을 반환합니다.

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```

또한, `recorded` 메서드는 클로저를 인자로 받을 수 있으며, 이 클로저는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 전달받아, 원하는 조건에 따라 요청/응답 쌍을 필터링하는 데에 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```

<a name="preventing-stray-requests"></a>
### 의도치 않은 실제 요청 방지

HTTP 클라이언트를 통해 보낸 모든 요청이 가짜 처리되었는지(=실제로 요청이 이루어지지 않았는지) 개별 테스트 또는 전체 테스트 스위트 수준에서 보장하고 싶다면, `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 메서드를 호출하면, 가짜 응답이 지정되지 않은 요청을 보낼 경우 실제 HTTP 요청을 하지 않고 예외를 발생시킵니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됩니다...
Http::get('https://github.com/laravel/framework');

// 예외가 발생합니다...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

라라벨은 HTTP 요청을 보내는 과정에서 총 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청을 보내기 전에, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 후에 발생합니다. 만약 응답을 받지 못한 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 모두 공개 속성(public property)인 `$request`가 포함되어 있어, `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있습니다. 또한, `ResponseReceived` 이벤트에는 `$request` 속성뿐만 아니라 `$response` 속성도 제공되어, `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있습니다. 이러한 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 애플리케이션에 등록하여 활용할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트를 처리합니다.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```