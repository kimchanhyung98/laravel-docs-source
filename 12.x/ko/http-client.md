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
    - [요청 점검](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 간결하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 보낼 수 있습니다. 라라벨의 Guzzle 래퍼는 가장 일반적인 활용 사례와 개발자 경험 향상에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

HTTP 요청을 보내려면 `Http` 파사드를 통해 제공되는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 기본적인 `GET` 요청을 다른 URL로 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 반환된 인스턴스는 아래와 같은 다양한 메서드를 통해 응답 값을 확인할 수 있도록 지원합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, JSON 응답 데이터를 배열 접근 방식으로 바로 가져올 수도 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 언급한 응답 메서드 외에도, 응답이 특정 상태 코드인지 확인할 수 있는 다음과 같은 메서드를 사용할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 이용하여 요청 URL을 유연하게 구성할 수 있도록 지원합니다. 템플릿에 확장 가능한 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 정보 출력(dump)

요청을 서버로 전송하기 전에 해당 요청 인스턴스를 덤프(출력)하며 스크립트 실행을 즉시 중단하고 싶을 때, 요청 정의의 앞에 `dd` 메서드를 추가하면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때에는 추가 데이터를 전송하는 경우가 많으므로, 이 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로 요청 데이터는 `application/json` 컨텐트 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때는 직접 URL에 쿼리 문자열을 붙이거나, 두 번째 인수로 키/값 배열을 전달할 수 있습니다.

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
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 방식으로 데이터 전송

`application/x-www-form-urlencoded` 컨텐츠 타입으로 데이터를 전송하려면, 요청을 보내기 전에 `asForm` 메서드를 호출하면 됩니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문(body) 전송

요청 시 본문을 직접 지정하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 컨텐츠 타입은 두 번째 인수로 전달할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트(form-data)로 전송하려면 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일 이름, 파일 내용을 인수로 받고, 필요하다면 세 번째 인수로 파일의 파일명, 네 번째 인수로 파일 헤더를 지정할 수도 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 데이터 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 메서드는 키/값 배열을 인수로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하면 요청에 대한 응답으로 어떤 컨텐츠 타입을 기대하는지 명시할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 빠르게 `application/json` 컨텐츠 타입을 명시하고 싶다면 `acceptJson` 메서드를 사용할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새 헤더를 합쳐줍니다. 만약 모든 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용할 수 있습니다.

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

기본 인증 및 다이제스트 인증(Basic, Digest)을 사용할 때 각각 `withBasicAuth`, `withDigestAuth` 메서드를 사용할 수 있습니다.

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 쓸 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답을 기다릴 최대 시간을(초 단위로) 지정하려면 `timeout` 메서드를 사용할 수 있습니다. 기본값은 30초입니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

만약 타임아웃이 초과되면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 데 최대 대기 시간(초)을 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

만약 클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 요청을 자동으로 재시도하길 원한다면, `retry` 메서드를 사용하면 됩니다. 이 메서드는 요청 시도 최대 횟수와 각 시도 사이 대기할 밀리초(ms) 값을 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이 대기 시간을 직접 계산하고 싶다면, `retry`의 두 번째 인수에 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한 배열을 첫 번째 인수로 넘겨서 각 시도 간 대기 시간을 지정할 수도 있습니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry`의 세 번째 인수로 콜러블을 전달해, 실제로 재시도를 해야 할 조건을 직접 정할 수 있습니다. 예를 들어, 첫 요청에서 `ConnectionException`이 발생했을 때만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패할 경우, 새 시도가 이루어지기 전에 요청 정보를 수정하고 싶다면, `retry` 메서드에 전달한 콜러블 안에서 요청 인수를 변경하면 됩니다. 예를 들어, 첫 요청에서 인증 오류가 발생했다면 새 토큰으로 재요청하는 식입니다.

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

모든 요청이 실패할 경우, `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 false로 전달하면 됩니다. 비활성화 시, 모든 재시도 후 마지막으로 받은 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우, `throw` 인수를 false로 설정했더라도 `Illuminate\Http\Client\ConnectionException` 예외는 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버에서 `400` 또는 `500`번대 응답)가 발생해도 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지 여부는 `successful`, `clientError`, `serverError`와 같은 메서드로 알 수 있습니다.

```php
// 상태 코드가 >= 200 이고 < 300 인지 확인...
$response->successful();

// 상태 코드가 >= 400 인지 확인...
$response->failed();

// 400번대 상태 코드를 반환했는지 확인...
$response->clientError();

// 500번대 상태 코드를 반환했는지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류일 경우 지정한 콜백을 즉시 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스를 가지고 있고, 상태 코드가 클라이언트 또는 서버 오류라면 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶을 때는 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 있을 경우 예외 발생...
$response->throw();

// 오류가 발생하고, 주어진 조건이 true라면 예외 발생...
$response->throwIf($condition);

// 오류가 발생하고, 주어진 클로저가 true를 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생하고, 주어진 조건이 false라면 예외 발생...
$response->throwUnless($condition);

// 오류가 발생하고, 주어진 클로저가 false를 반환하면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드라면 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스의 공개 `$response` 프로퍼티를 통해 반환된 응답 정보를 확인할 수 있습니다.

`throw` 메서드는 오류가 없을 경우 응답 인스턴스를 그대로 반환하므로, 추가적인 메서드 체이닝이 가능합니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전 추가 로직을 실행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 실행된 후에는 별도 re-throw 없이 예외가 자동으로 발생됩니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException`의 메시지는 로그 또는 예외 리포팅 시 120자로 잘려(truncate)서 남겨집니다. 이 동작을 커스터마이징하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // request 예외 메시지는 240자로 잘라서 저장
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, 요청별로 예외 메시지 자르기 동작을 지정하려면 `truncateExceptionsAt` 메서드를 사용할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨 HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 요청을 조작하거나 응답을 검사할 수 있습니다. 요청을 조작하고자 한다면 `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, `withResponseMiddleware` 메서드를 통해 들어오는 응답을 검사할 수도 있습니다.

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
#### 글로벌 미들웨어

모든 전송 요청 및 수신 응답에 적용되는 미들웨어를 전역으로 등록하고 싶을 때는, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로 이 두 메서드는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다.

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

개별 요청에 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하려면 `withOptions` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 배열을 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 전송 요청에 대해 기본값을 지정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출하는 것이 일반적입니다.

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

여러 건의 HTTP 요청을 동시에(비동기적으로) 보내고 싶을 때가 있습니다. 즉, 요청을 순차적으로 보내는 대신 한 번에 여러 요청을 전송하면, 느린 HTTP API와 상호작용할 때 성능을 크게 높일 수 있습니다.

이런 경우, `pool` 메서드를 사용하면 쉽게 동시 요청을 구현할 수 있습니다. `pool` 메서드는 클로저를 받아, 이 클로저는 `Illuminate\Http\Client\Pool` 인스턴스를 전달받아 여러 요청을 풀에 추가 후 전송하도록 해줍니다.

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

보시는 것처럼, 각 응답 인스턴스는 풀에 추가된 순서대로 배열을 통해 접근할 수 있습니다. 요청에 이름을 지정하고 싶다면 `as` 메서드를 사용하면 되고, 이 이름으로 응답을 참조할 수 있습니다.

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

`pool` 메서드는 `withHeaders`, `middleware`와 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 포함되는 각 요청별로 커스텀 헤더나 미들웨어를 적용하고 싶다면, 각각의 요청에 직접 옵션을 지정해야 합니다.

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

라라벨 HTTP 클라이언트는 "매크로"를 정의하여, 서비스들과의 통신 시 반복적으로 사용하는 요청 경로나 헤더 등을 유연하고 간결하게 설정하도록 지원합니다. 매크로를 정의하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정할 수 있습니다.

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

이렇게 매크로를 설정한 후에는, 애플리케이션 어디에서든 해당 매크로를 호출하여 등록된 설정값으로 Pending Request 인스턴스를 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

## 테스트

라라벨의 여러 서비스는 보다 쉽고 명확하게 테스트를 작성할 수 있도록 다양한 기능을 제공합니다. 라라벨의 HTTP 클라이언트도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 HTTP 클라이언트가 요청을 보냈을 때, 미리 지정한 스텁(가짜) 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리(Faking Responses)

예를 들어, 모든 요청에 대해 빈 응답과 상태 코드 `200`을 반환하도록 HTTP 클라이언트에 지시하려면 `fake` 메서드를 인자 없이 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 가짜 처리

또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜 응답을 지정할 URL 패턴을 나타내며, 값에는 해당 URL 요청에 반환할 응답을 지정합니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 가짜 처리가 적용되지 않은 URL로의 요청은 실제로 실행됩니다. 이런 엔드포인트에 대해 스텁/가짜 응답을 만들려면 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답을 스텁 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대해 문자열 응답을 스텁 처리...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 매치되지 않은 URL에 대해 적용될 기본 가짜 처리 패턴을 지정하고 싶다면, 와일드카드로 `*`만 사용하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답을 스텁 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대해 문자열 응답을 스텁 처리...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단하게 문자열, JSON, 빈 응답을 생성하고 싶을 때는 응답값으로 각각 문자열, 배열, 정수를 전달할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

HTTP 클라이언트가 요청 중에 `Illuminate\Http\Client\ConnectionException`을 발생시켰을 때 애플리케이션의 동작을 테스트해야 할 때가 있을 수 있습니다. `failedConnection` 메서드를 사용하여 HTTP 클라이언트가 연결 예외를 발생시키도록 할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

만약 `Illuminate\Http\Client\RequestException`이 발생하는 상황을 테스트하려면, `failedRequest` 메서드를 사용하면 됩니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 순차적 응답 가짜 처리(Faking Response Sequences)

특정 URL에 대해 여러 개의 응답이 순서대로 반환되도록 지정해야 하는 경우가 있습니다. 이럴 때는 `Http::sequence` 메서드를 이용해 응답 시퀀스를 구성할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 일련의 응답을 스텁 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스에 준비된 응답을 모두 소진하면, 이후 요청부터는 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 일련의 응답을 스텁 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

만약 특정한 URL 패턴을 지정할 필요 없이 여러 응답을 순차적으로 반환만 하면 된다면, `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 콜백을 이용한 가짜 처리

특정 엔드포인트에 대해 어떤 응답을 반환할지 보다 복잡한 로직이 필요한 경우, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 넘겨받으며, 반환값으로 응답 인스턴스를 돌려주면 됩니다. 클로저 안에서 원하는 만큼 복잡한 분기나 조건을 구성할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사(Inspecting Requests)

가짜 응답을 사용할 때, 클라이언트가 실제로 어떤 요청을 받았는지 확인하고, 애플리케이션이 올바른 데이터나 헤더를 전송하는지 검사하고 싶을 수 있습니다. 이런 경우, `Http::fake` 이후에 `Http::assertSent` 메서드를 호출하면 됩니다.

`assertSent` 메서드는 클로저를 인자로 받으며, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인자로 받고, 해당 요청이 기대에 부합하는지를 판단해 불린 값을 반환합니다. 조건에 맞는 요청이 최소한 하나라도 있었다면, 테스트가 통과하게 됩니다.

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

특정 요청이 전송되지 않았는지 검증해야 할 경우, `assertNotSent` 메서드를 사용할 수 있습니다.

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

`assertSentCount` 메서드를 사용하면 테스트 중 "전송된" 요청의 개수를 검증할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

아니면, `assertNothingSent` 메서드를 사용하여 테스트 중 어떤 요청도 전송되지 않았는지 검사할 수도 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 및 응답 기록

`recorded` 메서드를 사용하면 모든 요청과 그에 대한 응답을 한 번에 수집할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`, `Illuminate\Http\Client\Response` 인스턴스로 이루어진 배열을 컬렉션으로 반환합니다.

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

또한, `recorded` 메서드는 클로저를 인자로 받을 수 있으며, 이 클로저는 각 요청(Request)과 응답(Response) 인스턴스를 넘겨받아, 원하는 조건에 맞는 쌍만 필터링하여 반환하게 할 수 있습니다.

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
### 의도치 않은 요청 방지

개별 테스트나 전체 테스트 모음에서 HTTP 클라이언트를 통해 보낸 모든 요청이 반드시 가짜 처리되어야 한다고 보장하려면, `preventStrayRequests` 메서드를 호출하면 됩니다. 이 메서드 호출 후에는, 미리 가짜 응답이 지정되지 않은 요청이 발생하면 실제 HTTP 요청이 실행되는 대신 예외가 발생하게 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨...
Http::get('https://github.com/laravel/framework');

// 예외가 발생함...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

라라벨은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. 요청이 전송되기 전에는 `RequestSending` 이벤트가, 특정 요청에 대한 응답을 받은 후에는 `ResponseReceived` 이벤트가, 그리고 요청에 대한 응답을 받지 못하는 경우(연결 실패)는 `ConnectionFailed` 이벤트가 각각 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 공개 `$request` 속성이 있습니다. 마찬가지로, `ResponseReceived` 이벤트에는 `$request` 속성과 함께, `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있는 `$response` 속성도 제공됩니다. 이러한 이벤트에 대해 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에 만들 수 있습니다.

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