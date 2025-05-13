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
    - [응답 가짜처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 직관적이고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하는 HTTP 요청을 빠르게 보낼 수 있습니다. 라라벨의 Guzzle 래퍼는 가장 자주 사용되는 기능과 뛰어난 개발자 경험에 중점을 두고 설계되었습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저 다른 URL에 간단한 `GET` 요청을 보내는 방법을 살펴보겠습니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스를 구현하고 있으므로, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위 응답 관련 메서드 외에도, 응답이 특정 상태 코드인지 확인할 때 다음 메서드들을 사용할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 이용하여 요청 URL을 동적으로 생성할 수도 있습니다. URL 템플릿에서 확장할 수 있는 파라미터들을 지정하려면 `withUrlParameters` 메서드를 사용합니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 정보 출력 및 중단

보내기 전에 실제로 전송되는 요청 내용을 출력하고 스크립트 실행을 중단하고 싶다면, 요청 정의의 맨 앞에 `dd` 메서드를 붙이면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청을 할 때는 보통 추가적인 데이터를 함께 보내게 됩니다. 이런 경우 두 번째 인수로 배열을 전달할 수 있으며, 데이터는 기본적으로 `application/json` 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청의 쿼리 파라미터

`GET` 요청을 보낼 때는 URL에 직접 쿼리 문자열을 붙이거나, `get` 메서드의 두 번째 인자로 키/값 쌍의 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 보내기

만약 `application/x-www-form-urlencoded` 타입으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출하세요.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청에 raw(가공 없는 데이터) 바디를 직접 전달하려면, `withBody` 메서드를 사용할 수 있습니다. 이때 콘텐츠 타입은 두 번째 인수로 지정합니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청 (파일 전송 등)

파일을 여러 부분으로 나누어 업로드할 때는, 요청 전에 `attach` 메서드를 사용합니다. 이 메서드는 파일명과 파일 내용을 인수로 받으며, 필요하다면 세 번째 인수로 파일의 이름, 네 번째 인수로 파일에 관련된 헤더를 전달할 수 있습니다.

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

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 받습니다.

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

자주 사용하는 `application/json` 타입을 보다 간편하게 지정하려면 `acceptJson` 메서드를 활용하세요.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders`는 기존 요청 헤더에 새로운 헤더를 합쳐줍니다. 필요하다면 `replaceHeaders` 메서드로 모든 헤더를 한 번에 교체할 수도 있습니다.

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

기본 인증과 다이제스트 인증을 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다.

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

`Authorization` 헤더에 bearer 토큰을 간단하게 추가하려면 `withToken` 메서드를 사용하세요.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용해 응답을 기다릴 최대 초(seconds)를 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

설정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결만 시도하는 데 걸리는 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생할 경우 요청을 자동으로 재시도하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 요청을 최대 몇 번 시도할지, 각 시도 사이에 몇 밀리초를 대기할지 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 간 대기시간을 직접 계산하고 싶다면, 두 번째 인수에 클로저를 전달할 수도 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한, 편의상 첫 번째 인수로 배열로 밀리초 간격을 지정할 수 있습니다. 이렇게 하면 각 재시도 마다 해당 시간만큼 대기합니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 실제로 재시도를 수행할지 판단하는 콜러블을 넘길 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생했을 때만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패할 경우 새로운 요청을 보내기 전에 요청 객체를 수정하고 싶다면, `retry`에 전달하는 콜러블에서 요청 인자를 조작하면 됩니다. 예를 들어 인증 에러로 첫 시도가 실패했을 때 새로운 토큰으로 재시도할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 파라미터에 `false`를 전달할 수 있습니다. 비활성화하면 마지막으로 받은 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패할 경우에는 `throw`가 `false`여도 `Illuminate\Http\Client\ConnectionException` 예외가 무조건 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트/서버 오류(서버에서 `400`, `500`번대 응답) 시 예외를 자동으로 발생시키지 않습니다. 오류가 발생했는지 확인하려면 `successful`, `clientError`, `serverError` 등의 메서드를 사용할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 400번대 에러(클라이언트 오류) 확인
$response->clientError();

// 500번대 에러(서버 오류) 확인
$response->serverError();

// 클라이언트/서버 오류가 있으면 즉시 콜백을 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스의 상태 코드가 클라이언트 또는 서버 오류를 나타내면, `throw`나 `throwIf` 메서드를 사용하여 `Illuminate\Http\Client\RequestException` 예외를 발생시킬 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트/서버 오류 발생 시 예외 던지기
$response->throw();

// 오류가 있고 주어진 조건이 true면 예외 던지기
$response->throwIf($condition);

// 오류가 있고 클로저가 true 반환 시 예외 던지기
$response->throwIf(fn (Response $response) => true);

// 오류가 있고 주어진 조건이 false면 예외 던지기
$response->throwUnless($condition);

// 오류가 있고 클로저가 false 반환 시 예외 던지기
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 던지기
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아닐 때 예외 던지기
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스의 퍼블릭 `$response` 속성으로 반환된 응답을 자세히 확인할 수 있습니다.

`throw` 메서드는 에러가 발생하지 않으면 응답 인스턴스를 그대로 반환하므로, 체이닝해서 사용할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전 추가 로직을 실행하려면 `throw`에 클로저를 전달할 수 있습니다. 클로저 실행 후에는 자동으로 예외가 발생하므로, 클로저 내에서 다시 예외를 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘립니다. 이 동작을 변경하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지를 240자로 제한...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 제한 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨 HTTP 클라이언트는 Guzzle 기반이기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해서 요청 전후를 조작하거나 응답을 참조할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드에 미들웨어를 등록합니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하고 싶다면 `withResponseMiddleware` 메서드를 사용할 수 있습니다.

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

모든 요청 및 응답에 공통적으로 적용되는 미들웨어를 등록하려면 `globalRequestMiddleware`와 `globalResponseMiddleware`를 이용하세요. 일반적으로 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 호출되어야 합니다.

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

[추가 Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)이 필요할 경우, `withOptions` 메서드를 이용해 요청 시 옵션을 지정할 수 있습니다. 이 메서드는 키/값 쌍 배열을 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 요청에 기본적으로 적용할 옵션이 있다면, `globalOptions` 메서드를 사용할 수 있습니다. 이도 역시 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 일반적입니다.

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

여러 HTTP 요청을 동시에(병렬로) 보내고 싶을 때가 있습니다. 즉, 요청을 순차적으로 하나씩 보내는 것이 아니라, 여러 요청을 동시에 전송하여 오래 걸리는 HTTP API와의 상호작용 성능을 크게 높일 수 있습니다.

이런 동작은 `pool` 메서드를 사용해 손쉽게 구현할 수 있습니다. `pool`은 클로저를 받아 `Illuminate\Http\Client\Pool` 인스턴스를 제공하며, 여기에 요청을 추가해 동시에 보낼 수 있습니다.

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

이와 같이, 각 응답 인스턴스는 추가한 순서대로 인덱스로 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면 `as` 메서드를 사용하면 되고, 이름으로 응답을 조회할 수 있게 됩니다.

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
#### 동시 요청 옵션 커스터마이징

`pool` 메서드는 `withHeaders`나 `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 들어가는 각 요청별로 필요한 옵션이나 미들웨어, 헤더를 직접 지정해주어야 합니다.

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

라라벨 HTTP 클라이언트는 "매크로"라는 기능으로 서비스별 공통 경로 및 헤더 구성을 편리하게 재사용할 수 있습니다. 매크로는 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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

매크로를 정의했다면, 애플리케이션 어디서든 지정한 구성의 요청을 쉽게 작성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

라라벨의 여러 서비스처럼, HTTP 클라이언트도 쉽고 명확하게 테스트를 작성할 수 있도록 다양한 기능을 제공합니다. `Http` 파사드의 `fake` 메서드를 사용하면, 실제 요청이 아닌 가짜(더미) 응답을 반환하도록 클라이언트를 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜처리

예를 들어, 모든 요청에 대해 빈 200 응답을 반환하도록 만들고 싶다면 다음처럼 사용합니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 가짜처리

또는, `fake` 메서드에 배열을 전달하여 원하는 URL 패턴별로 개별 응답을 설정할 수 있습니다. `*` 문자를 와일드카드로 사용할 수 있으며, 가짜처리되지 않은 URL로의 실제 요청은 실제로 실행됩니다. `Http` 파사드의 `response` 메서드를 사용하면 다양한 형태의 더미 응답을 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 더미
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트의 문자열 응답 더미
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

URL 패턴을 단일 `*`로 지정하면, 매칭되지 않은 모든 URL에 대해 더미 응답을 반환할 수도 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트의 JSON 응답 더미
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트의 문자열 응답 더미
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의상 문자열, 배열, 정수(상태 코드)로도 더미 응답을 즉시 지정할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 처리 가짜처리

`Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트해야 할 경우, `failedConnection` 메서드를 사용해 연결 실패를 가짜처리할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`이 발생하는 상황을 테스트하려면, `failedRequest` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜처리

특정 URL에서 여러 가지 더미 응답을 순서대로 반환해야 할 때는 `Http::sequence` 메서드를 이용해 시퀀스를 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 연속 응답 더미 지정
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면 이후 요청에서는 예외가 발생합니다. 시퀀스가 비었을 때 반환되는 기본 응답을 지정하려면 `whenEmpty` 메서드를 활용하세요.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 연속 응답 더미 지정
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴이 필요 없고, 단순히 응답 시퀀스만 만들고 싶을 때는 `Http::fakeSequence`를 사용하면 됩니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### Fake 콜백

특정 엔드포인트에 대해 복잡한 로직으로 적절한 응답을 반환해야 한다면, `fake` 메서드에 클로저를 전달하세요. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아서, 직접 응답을 반환하면 됩니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 의도치 않은 요청 방지

테스트 중 HTTP 클라이언트로 보내는 모든 요청이 반드시 가짜처리(faked) 되어야 한다면, `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 기능을 켜면, 더미 응답이 지정되지 않은 모든 요청은 실제로 전송되는 대신 예외가 발생합니다.

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

<a name="inspecting-requests"></a>
### 요청 검사

가짜 응답 테스트 중 실제로 어떤 형태로 클라이언트가 요청을 보냈는지 확인하고 싶을 때는, `Http::fake` 이후에 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent`는 클로저를 받아, `Illuminate\Http\Client\Request` 인스턴스를 전달합니다. 이 클로저에서 테스트 조건을 정의하며, 조건을 만족하는 요청이 하나라도 있으면 테스트에 통과합니다.

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

특정 요청이 아예 전송되지 않았음을 검증하려면 `assertNotSent` 메서드를 사용할 수 있습니다.

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

테스트 중 "전송된" 요청이 몇 개인지 검증할 때는 `assertSentCount`를 사용할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

아예 아무 요청도 전송되지 않았음을 검증하려면 `assertNothingSent`를 사용할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록하기

`recorded` 메서드를 이용하면 모든 요청과 그에 대한 응답을 모아볼 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 포함하는 배열 컬렉션을 반환합니다.

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

또한, `recorded` 메서드에 클로저를 전달할 수 있으며, 각 요청/응답 페어를 조건별로 필터링할 수 있습니다.

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

<a name="events"></a>
## 이벤트

라라벨에서는 HTTP 요청을 보낼 때 세 가지 이벤트가 발생합니다. `RequestSending` 이벤트는 요청이 보내지기 전에 실행되며, `ResponseReceived` 이벤트는 요청에 대한 응답을 받은 후 실행됩니다. 요청에 대해 응답을 받지 못하면 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 퍼블릭 `$request` 속성을 가지고 있습니다. 마찬가지로 `ResponseReceived` 이벤트는 `$request`, `$response` 속성을 통해 각각 `Illuminate\Http\Client\Request`, `Illuminate\Http\Client\Response` 인스턴스를 참조할 수 있습니다. 애플리케이션 내에서 [이벤트 리스너](/docs/12.x/events)를 생성해 이 이벤트들에 대응할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 핸들러.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
