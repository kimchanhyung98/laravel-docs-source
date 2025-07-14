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
    - [예상치 못한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 직관적인 API를 제공합니다. 이를 활용하면 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 쉽고 빠르게 보낼 수 있습니다. 라라벨의 Guzzle 래퍼는 가장 자주 사용되는 기능에 초점을 맞추고 있어 개발자 경험을 크게 향상시킵니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보낼 때는 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 가장 기본적인 `GET` 요청을 다른 URL로 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다. 이 객체는 응답을 다양한 방식으로 확인할 수 있는 여러 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있기 때문에, JSON 응답 데이터를 배열처럼 바로 접근할 수도 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 소개한 응답 메서드 외에도, 응답이 특정 상태 코드인지 확인할 때 사용할 수 있는 메서드는 다음과 같습니다.

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

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 활용해 요청 URL을 만들 수 있도록 지원합니다. `withUrlParameters` 메서드는 URI 템플릿에서 사용할 URL 파라미터를 정의합니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버그(dump)하기

요청을 보내기 전에 해당 요청 인스턴스를 화면에 출력하고 스크립트 실행을 중단하고 싶을 때는, 요청 정의의 처음에 `dd` 메서드를 추가하면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때는 요청과 함께 추가 데이터를 전송하는 경우가 많습니다. 이런 경우, 해당 메서드의 두 번째 인자로 데이터 배열을 전달하면 됩니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때, 쿼리 문자열을 URL에 직접 추가할 수도 있고, 두 번째 인자로 키/값 쌍의 배열을 전달할 수도 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는, `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 데이터 전송

요청 데이터를 `application/x-www-form-urlencoded` 콘텐츠 타입으로 전송하려면, 요청 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

원하는 데이터로 Raw 요청 바디를 직접 지정하고 싶을 때는 `withBody` 메서드를 사용할 수 있습니다. 이때 콘텐츠 타입은 두 번째 인자로 전달합니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 전송하려면, 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 내용을 인자로 받습니다. 필요하다면 세 번째 인자로 파일명을, 네 번째 인자로 파일과 관련된 헤더를 지정할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 내용을 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

`withHeaders` 메서드를 사용하면 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키/값 쌍 배열을 인자로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 기대하는 콘텐츠 타입을 지정하려면 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

좀 더 간단하게, `application/json` 콘텐츠 타입을 명시하려면 `acceptJson` 메서드를 활용할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새 헤더를 기존 요청 헤더에 병합합니다. 필요하다면, `replaceHeaders` 메서드를 사용해 모든 헤더를 아예 교체할 수도 있습니다.

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

기본 인증(Basic)과 다이제스트 인증(Digest) 정보를 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다.

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 손쉽게 추가하려면, `withToken` 메서드를 사용하면 됩니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용하면 응답을 기다릴 최대 초(second) 단위를 지정할 수 있습니다. 기본적으로 HTTP 클라이언트의 타임아웃은 30초입니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

만약 지정한 타임아웃을 초과하면, `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결을 시도하는데 걸릴 최대 대기 초를 따로 설정하고 싶다면, `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트나 서버 오류 발생 시 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 최대 시도 횟수와, 각 시도 사이에 라라벨이 기다릴 시간(밀리초 단위)을 인자로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이 대기 시간을 직접 계산하고 싶다면, 두 번째 인자로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한, 편의를 위해 `retry` 메서드의 첫 번째 인자에 배열을 사용할 수도 있습니다. 배열은 각 시도 간 대기할 밀리초 단위 값들을 의미합니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드에 세 번째 인자를 추가로 전달할 수 있습니다. 이 인자는 실제로 재시도를 시도할지 여부를 결정하는 callable이어야 합니다. 예를 들어, 최초 요청이 `ConnectionException`을 만났을 때만 재시도하고 싶을 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도에 실패한 경우, 다음 시도 전에 해당 요청을 수정하고 싶을 수도 있습니다. 이때는 `retry` 메서드에 전달한 callable이 가진 요청 인자를 수정하면 됩니다. 예를 들어, 첫 시도에서 인증 오류가 발생하면 새로운 인증 토큰으로 다시 요청을 보내도록 할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 만약 이런 동작을 끄고 싶다면, `throw` 인자를 `false`로 전달하면 됩니다. 이 경우, 클라이언트가 마지막으로 받은 응답이 모든 재시도 후에 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우, `throw` 인자를 `false`로 지정해도 `Illuminate\Http\Client\ConnectionException`은 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트나 서버 오류(`400` 및 `500` 레벨 응답)가 발생해도 예외를 던지지 않습니다. 이러한 오류가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 메서드를 사용할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 응답이 400 레벨 상태 코드인지 확인...
$response->clientError();

// 응답이 500 레벨 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류 발생 시, 바로 지정한 콜백을 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스를 갖고 있고, 만약 클라이언트 또는 서버 오류가 발생했다면 `Illuminate\Http\Client\RequestException`을 던지고 싶다면, `throw`나 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 발생했다면 예외 발생...
$response->throw();

// 오류가 발생했고 주어진 조건이 true라면 예외 발생...
$response->throwIf($condition);

// 오류가 발생했고 주어진 클로저의 결과가 true라면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했고 주어진 조건이 false라면 예외 발생...
$response->throwUnless($condition);

// 오류가 발생했고 주어진 클로저의 결과가 false라면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아닐 때 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 확인할 수 있는 public `$response` 속성이 있습니다.

`throw` 메서드는 오류가 없다면 응답 인스턴스를 그대로 반환하므로, `throw` 다음에 다른 메서드를 체이닝해서 사용할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 던져지기 전에 추가 로직을 실행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이때 클로저가 실행된 후 예외는 자동으로 발생하므로 클로저 안에서 직접 예외를 다시 던질 필요가 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 또는 보고 시 120자까지로 잘려서(truncate) 출력됩니다. 이 동작을 변경하거나 비활성화하려면, `bootstrap/app.php` 파일에서 애플리케이션의 예외 처리 설정 시 `truncateRequestExceptionsAt`, `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지를 240자로 잘라서 처리
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, `truncateExceptionsAt` 메서드를 통해 요청별로 예외 메시지 자르기 동작을 조정할 수도 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨 HTTP 클라이언트는 Guzzle 기반이기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청을 조작하거나 응답을 점검할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록합니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 수신된 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록하면 됩니다.

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
#### 글로벌(전역) 미들웨어

모든 요청 및 응답에 공통적으로 적용할 미들웨어를 등록하고 싶을 때는, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용합니다. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 일반적입니다.

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

요청별로 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하고 싶을 때는 `withOptions` 메서드를 사용합니다. 이 메서드는 키/값 쌍 배열을 인자로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌(전역) 옵션

모든 요청에 대해 기본 옵션을 설정하려면, `globalOptions` 메서드를 활용할 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다.

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

여러 개의 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 여러 요청을 순차적으로 보내는 것이 아니라 한 번에 동시에 보냄으로써, 느린 HTTP API와 상호작용할 때 성능을 대폭 향상시킬 수 있습니다.

라라벨에서는 `pool` 메서드를 사용해 이를 손쉽게 구현할 수 있습니다. 이 메서드는 클로저를 인자로 받으며, 이 클로저에서는 `Illuminate\Http\Client\Pool` 인스턴스를 통해 요청들을 풀에 추가할 수 있습니다.

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

위 예시처럼 풀에 추가된 순서대로 각 응답 인스턴스에 접근할 수 있습니다. 만약 요청에 이름을 붙이고 싶다면, `as` 메서드를 통해 각 요청에 이름을 부여할 수 있으며, 이후 이름으로 응답에 접근이 가능합니다.

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
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware`와 같은 다른 HTTP 클라이언트 메서드와 체이닝해서 사용할 수 없습니다. 풀에 추가한 요청 각각에 원하는 헤더나 미들웨어 등을 적용하려면, 각 요청별로 직접 옵션을 지정해야 합니다.

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

라라벨 HTTP 클라이언트는 "매크로"를 정의할 수 있게 해줍니다. 매크로를 활용하면, 여러 곳에서 반복되어 사용되는 요청 경로나 헤더 설정 등을 보다 간편하고 일관되게 구성할 수 있습니다. 시작하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 매크로를 정의합니다.

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

이제 매크로가 설정되었으면, 애플리케이션 어디에서든 해당 매크로를 호출해 지정된 설정이 적용된 요청 객체를 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

## 테스트

라라벨의 여러 서비스는 쉽고 명확하게 테스트를 작성할 수 있도록 다양한 기능을 제공합니다. 라라벨의 HTTP 클라이언트도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 HTTP 클라이언트가 요청을 보낼 때 미리 정해둔 가짜(더미) 응답을 반환하도록 만들 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜로 만들기

예를 들어, 모든 요청에 대해 빈 응답과 `200` 상태 코드를 반환하도록 HTTP 클라이언트에 지시하려면, 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 가짜 응답 만들기

또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜로 만들고자 하는 URL 패턴이며, 각각의 값은 해당 URL의 응답이 됩니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 각 엔드포인트에 대한 가짜 응답을 생성할 때는 `Http` 파사드의 `response` 메서드를 사용하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜화...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 가짜화...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜로 지정하지 않은 URL로의 요청은 실제로 실행됩니다. 모든 일치하지 않는 URL에 대해 기본 가짜 응답을 지정하려면, `*` 와일드카드만 사용하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜화...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대한 문자열 응답 가짜화...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의를 위해, 문자열, JSON, 비어 있는 응답을 생성할 때는 응답 값을 문자열, 배열, 정수로 간단하게 지정할 수도 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜화

HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트하고 싶을 때가 있습니다. 이 경우, `failedConnection` 메서드를 사용해서 HTTP 클라이언트가 연결 예외를 던지도록 만들 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

애플리케이션에서 `Illuminate\Http\Client\RequestException`이 발생하는 경우를 테스트하려면, `failedRequest` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜화

특정 URL이 여러 번 호출될 때, 순서대로 여러 개의 가짜 응답을 반환해야 하는 경우가 있습니다. 이럴 때는 `Http::sequence` 메서드를 사용해 응답 시퀀스를 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 시퀀스 응답 가짜화...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스에 정의된 모든 응답이 소진된 이후에는, 추가 요청 시 예외가 발생합니다. 시퀀스가 비어 있을 때 반환할 기본 응답을 지정하고 싶으면, `whenEmpty` 메서드를 사용합니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 시퀀스 응답 가짜화...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

만약 특정 URL 패턴을 지정하지 않고, 응답 시퀀스만 가짜로 만들고 싶다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트마다 반환할 응답을 더 복잡한 로직으로 결정해야 한다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 매개변수로 받으며, 반환 값으로 응답 인스턴스를 내려야 합니다. 클로저 내부에서는 원하는 방식으로 조건을 체크해 반환할 응답을 자유롭게 지정할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사하기

가짜 응답을 사용할 때, 애플리케이션이 올바른 데이터나 헤더를 포함해 요청을 보내는지 확인하고 싶을 수 있습니다. 이럴 때는 `Http::fake` 호출 이후에 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent` 메서드는 클로저를 인수로 받으며, 이 클로저에는 `Illuminate\Http\Client\Request` 인스턴스가 전달됩니다. 클로저에서는 요청이 원하는 조건을 만족하는지 확인하고, boolean 값을 반환해야 합니다. 테스트가 통과하려면 적어도 하나 이상의 요청이 인자로 전달된 조건을 충족해야 합니다.

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

특정 요청이 전송되지 않았는지 검사해야 할 경우에는 `assertNotSent` 메서드를 사용할 수 있습니다.

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

테스트 중에 "보낸" 요청이 몇 번 있었는지 검사하려면 `assertSentCount` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는 테스트 중에 아무 요청도 전송되지 않았는지 확인하려면 `assertNothingSent` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 / 응답 기록

`recorded` 메서드를 사용하면 모든 요청과 그에 대한 응답을 모아볼 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스로 이뤄진 배열의 컬렉션을 반환합니다.

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

또한, `recorded` 메서드는 클로저를 인수로 받아 사용할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 받으며, 원하는 기준에 따라 요청/응답 쌍을 필터링하는 데 사용할 수 있습니다.

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
### 예외적 요청 방지

개별 테스트 또는 전체 테스트 스위트에서 HTTP 클라이언트를 통해 전송된 모든 요청이 반드시 가짜로 처리되도록 보장하려면, `preventStrayRequests` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 이후로, 미리 지정한 가짜 응답이 없는 요청이 실제 HTTP 요청을 전송하는 대신 예외를 발생시키게 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨
Http::get('https://github.com/laravel/framework');

// 예외 발생
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

라라벨은 HTTP 요청을 보내는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 보내지기 직전에 발생하며, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 후에 발생합니다. 그리고, 요청에 대한 응답을 받지 못한 경우는 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트 모두에는 `Illuminate\Http\Client\Request` 인스턴스를 참조할 수 있는 public `$request` 속성이 있습니다. 마찬가지로 `ResponseReceived` 이벤트에는 `$request` 속성과 더불어, `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있는 `$response` 속성도 포함되어 있습니다. 이러한 이벤트에 대해 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에서 작성할 수 있습니다.

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