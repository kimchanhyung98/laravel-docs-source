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
    - [응답 가짜로 만들기](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [실수로 발생하는 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 표현적이고 최소한의 API를 제공하여 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 만들 수 있게 지원합니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례에 초점을 맞추고 훌륭한 개발 경험을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 다양한 응답 검사 메서드를 제공하는 `Illuminate\Http\Client\Response`의 인스턴스를 반환합니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로, JSON 응답 데이터를 응답 객체에서 바로 접근할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 메서드 외에도, 특정 상태 코드를 가졌는지 확인할 때 사용할 수 있는 메서드들은 다음과 같습니다:

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용해 요청 URL을 구성할 수 있습니다. 템플릿에서 확장할 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용하면 됩니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 내용 덤프(dump)하기

요청 인스턴스를 전송 전 덤프(dump)한 후, 스크립트 실행을 종료하고 싶으면 요청 정의의 시작 부분에 `dd` 메서드를 추가하십시오:

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청을 보낼 때 요청에 추가 데이터를 보내는 일이 일반적입니다. 이들 메서드는 두 번째 인수로 데이터 배열을 받으며, 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때 URL에 쿼리 문자열을 직접 추가하거나, `get` 메서드의 두 번째 인수로 키/값 쌍의 배열을 전달할 수 있습니다:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 전송하려면, 요청을 보내기 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시(Request Body) 바디 전송

요청 시 원시 요청 바디를 직접 제공하려면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 전송하려면, 요청 전 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일 이름과 내용을 받으며, 필요하다면 세 번째 인수에 파일명을, 네 번째 인수에 파일에 연결할 헤더를 지정할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용 대신 스트림 리소스를 전달할 수도 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 인수로 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

애플리케이션이 요청에 대한 응답에서 기대하는 콘텐츠 타입을 명시하려면 `accept` 메서드를 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

`application/json` 콘텐츠 타입을 빠르게 지정하려면 `acceptJson` 메서드를 사용할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드로 새 헤더를 기존 헤더에 병합합니다. 만약 모든 헤더를 완전히 대체하려면 `replaceHeaders` 메서드를 사용하십시오:

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

기본 인증(basic authentication) 또는 다이제스트 인증(digest authentication) 자격 증명을 각각 `withBasicAuth`, `withDigestAuth` 메서드를 통해 지정할 수 있습니다:

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰(Bearer Tokens)

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하고 싶다면 `withToken` 메서드를 사용할 수 있습니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답을 기다리는 최대 시간을 초 단위로 지정하려면 `timeout` 메서드를 사용하십시오. 기본적으로 HTTP 클라이언트는 30초 후에 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃이 초과되면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버 접속을 시도하는 동안 대기할 최대 시간을 초 단위로 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다(기본값: 10초):

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트나 서버 오류가 발생한 경우 요청을 자동으로 다시 시도하게 하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 최대 시도 횟수와 각 시도 사이에 Laravel이 대기할 밀리초 단위의 시간을 인수로 받습니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 횟수 사이에 대기할 밀리초를 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해, 첫 번째 인수로 배열을 제공할 수도 있습니다. 이 배열은 각각의 시도 사이에 대기할 밀리초를 결정하는 데 사용됩니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 콜러블을 지정해서 실제로 재시도를 할지 여부를 결정할 수 있습니다. 예를 들어, 첫 번째 요청 시도에서 `ConnectionException`이 발생했을 때만 재시도하도록 할 수 있습니다:

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패할 경우 새 시도가 시작되기 전에 요청을 변경하고 싶을 때도 있습니다. 이럴 때는 `retry` 메서드에 전달한 콜러블의 요청 인수에서 직접 요청을 수정하면 됩니다. 예를 들어, 첫 시도에서 인증 오류가 발생하면 새로운 토큰으로 다시 요청해보고 싶을 때 사용할 수 있습니다:

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 지정할 수 있습니다. 비활성화하면, 모든 재시도를 마친 후 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는 `throw` 인수 값을 `false`로 해도 `Illuminate\Http\Client\ConnectionException` 예외가 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버로부터의 `400`, `500`번대 응답)에 대해 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다:

```php
// 상태 코드가 >= 200 이고 < 300인지 확인합니다...
$response->successful();

// 상태 코드가 >= 400 인지 확인합니다...
$response->failed();

// 400번대 상태 코드인지 확인합니다...
$response->clientError();

// 500번대 상태 코드인지 확인합니다...
$response->serverError();

// 클라이언트 또는 서버 오류가 발생하면, 즉시 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스가 있고, 상태 코드가 클라이언트 또는 서버 오류를 나타낸다면 `Illuminate\Http\Client\RequestException` 인스턴스를 예외로 발생시키고 싶을 때는 `throw` 또는 `throwIf` 메서드를 사용하십시오:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트나 서버 오류가 발생하면 예외를 발생시킵니다...
$response->throw();

// 에러가 발생했고, 주어진 조건이 true면 예외 발생...
$response->throwIf($condition);

// 에러가 발생했고, 주어진 클로저가 true를 반환하면 예외 발생...
$response->throwIf(fn (Response $response) => true);

// 에러가 발생했고, 주어진 조건이 false면 예외 발생...
$response->throwUnless($condition);

// 에러가 발생했고, 주어진 클로저가 false를 반환하면 예외 발생...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외 발생...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있는 공개 `$response` 속성이 있습니다.

`throw` 메서드는 오류가 발생하지 않은 경우 응답 인스턴스를 반환하므로, `throw` 뒤에 다른 작업을 체이닝할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 실행하고 싶을 경우, `throw` 메서드에 클로저를 전달하면 됩니다. 클로저 내에서 예외를 다시 던질 필요 없이 자동으로 예외가 발생합니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로깅 또는 보고 시 120자까지로 잘립니다. 이 동작을 사용자 정의하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php`에서 `truncateRequestExceptionsAt`, `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지를 240자로 줄입니다...
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 잘림을 비활성화합니다...
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, `truncateExceptionsAt` 메서드를 통해 요청별로 예외 메시지 잘림 동작을 사용자 정의할 수 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 동작하기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드를 사용하여 Guzzle 미들웨어를 등록하십시오:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 들어오는 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드를 통해 미들웨어를 등록할 수 있습니다:

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

때로는 모든 나가는 요청과 들어오는 응답에 적용되는 미들웨어를 등록하고자 할 때가 있습니다. 이럴 땐 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하면 됩니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

나가는 요청에 대해 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 `withOptions` 메서드를 통해 지정할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

모든 나가는 요청에 대한 기본 옵션을 설정하려면 `globalOptions` 메서드를 이용할 수 있습니다. 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

때로는 여러 HTTP 요청을 동시에 실행하고 싶을 때가 있습니다. 즉, 순차적으로 요청하는 대신 여러 요청을 한 번에 보냅니다. 이는 느린 HTTP API와 연동할 때 상당한 성능 향상을 가져올 수 있습니다.

이런 작업을 `pool` 메서드를 통해 간편하게 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 전달하는 클로저를 받으며, 이를 통해 여러 요청을 한 번에 풀에 추가할 수 있습니다:

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

보시다시피 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 필요하다면 `as` 메서드로 요청에 이름을 부여하고, 이름으로 결과를 참조할 수도 있습니다:

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

`pool` 메서드는 `withHeaders`나 `middleware` 등의 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀 내 요청에 커스텀 헤더나 미들웨어를 적용하고 싶을 때, 각 요청별로 해당 옵션을 직접 설정하면 됩니다:

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

Laravel HTTP 클라이언트는 애플리케이션 내에서 다양한 서비스와 상호작용할 때 공통적인 요청 경로와 헤더 구성을 간편하고 표현적으로 정의할 수 있도록 "매크로"를 지원합니다. 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 매크로를 정의합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

매크로를 정의한 뒤에는 애플리케이션 어디에서나 지정된 설정이 적용된 페딩(pending) 요청을 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스에서는 쉽고 표현적으로 테스트 코드를 작성할 수 있도록 다양한 기능을 지원하며, HTTP 클라이언트도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면, 실제 요청이 발생할 때 더미/가짜 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜로 만들기

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드의 응답을 반환하도록 하려면 인수 없이 `fake` 메서드를 호출하십시오:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 응답 가짜로 만들기

또는, `fake` 메서드에 배열을 전달할 수 있습니다. 배열의 키는 가짜로 만들 URL 패턴, 값은 해당 패턴에 대한 응답입니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 가짜 응답을 만들기 위해 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트의 문자열 응답 스텁...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜로 처리되지 않은 URL에 대한 요청은 실제로 수행됩니다. 모든 패턴에 매칭되지 않은 URL도 스텁 응답으로 처리하고 싶다면, 단일 `*` 키를 쓸 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지 모든 엔드포인트의 문자열 응답 스텁...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단히 문자열, 배열, 정수만 전달해도 빠르게 문자열, JSON, 빈 응답이 생성됩니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜로 만들기

HTTP 클라이언트에서 요청 시에 `Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트해야 할 때가 있습니다. 이럴 때 `failedConnection` 메서드를 사용하면 됩니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 예외 발생 상황을 테스트하고 싶으면 `failedRequest` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 일련의 응답 가짜로 만들기

때로는 하나의 URL에서 일련의 가짜 응답을 순서대로 반환하도록 하고 싶을 때가 있습니다. 이런 경우 `Http::sequence` 메서드를 활용해 응답 목록을 만들 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스의 모든 응답이 소모되면, 이후 요청은 예외를 발생시킵니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 일련의 가짜 응답만 필요하다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 더 복잡한 콜백을 이용한 가짜 처리

특정 엔드포인트에 어떤 응답을 반환할지 결정하는 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받아 응답 인스턴스를 반환해야 합니다. 이 안에서 원한다면 다양한 조건에 따라 다양한 응답을 반환할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

가짜 응답을 반환할 때, 클라이언트가 실제로 올바른 데이터나 헤더를 전송했는지 확인하고 싶을 때가 있습니다. 이럴 때는 `Http::fake` 호출 후 `Http::assertSent` 메서드를 사용할 수 있습니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받는 클로저를 인수로 받으며, 해당 요청이 기대에 부합하면 true를 반환해야 합니다. 검사에 성공하려면 적어도 하나의 요청이 해당 조건과 일치해야 합니다:

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

특정 요청이 전송되지 않았음을 검증하고 싶을 때는 `assertNotSent` 메서드를 사용하십시오:

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

테스트 중 "전송된" 요청 개수를 검증하려면 `assertSentCount` 메서드를 사용하세요:

```php
Http::fake();

Http::assertSentCount(5);
```

혹은, 어떠한 요청도 전송되지 않았음을 검증하려면 `assertNothingSent` 메서드를 사용하세요:

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 및 응답 기록(Recording)

`recorded` 메서드를 사용해 모든 요청과 해당 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 객체로 이루어진 배열 컬렉션을 반환합니다:

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

추가로, `recorded` 메서드에 클로저를 전달하면 특정 조건에 맞는 요청/응답 쌍만 필터링해서 가져올 수 있습니다:

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
### 실수로 발생하는 요청 방지

HTTP 클라이언트를 통해 전송되는 모든 요청이 테스트 코드 또는 전체 테스트 스위트 동안 반드시 가짜 응답을 반환하도록 강제하고 싶다면, `preventStrayRequests` 메서드를 사용할 수 있습니다. 이 메서드 호출 이후 가짜로 지정하지 않은 요청이 발생하면 실제 HTTP 요청 대신 예외가 발생합니다:

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

특정 요청만 예외적으로 허용하면서 대부분의 실수로 발생하는 요청을 방지하고 싶다면, `allowStrayRequests` 메서드에 URL 패턴 배열을 전달하세요. 해당 패턴에 일치하는 요청은 허용되고, 나머지는 모두 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실제로 실행됩니다...
Http::get('http://127.0.0.1:5000/generate');

// 예외가 발생합니다...
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청을 보내는 과정에서 세 개의 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에, `ResponseReceived` 이벤트는 각 요청의 응답이 수신된 후, 그리고 `ConnectionFailed` 이벤트는 해당 요청에 대해 응답을 받지 못할 때 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 공개 `$request` 속성이 있습니다. 마찬가지로, `ResponseReceived` 이벤트는 `$request` 속성뿐 아니라 응답을 확인할 수 있는 `$response` 속성도 가집니다. 이러한 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에 만들 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
