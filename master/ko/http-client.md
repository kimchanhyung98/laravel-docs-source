# HTTP 클라이언트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [오류 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 모킹](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [불필요한 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 표현적이고 미니멀한 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 생성할 수 있게 해줍니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내기 위해서는 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체는 응답을 확인할 수 있는 다양한 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하므로, JSON 응답 데이터를 응답 객체에서 바로 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위의 응답 메서드 외에도, 다음과 같은 메서드를 활용해 특정 상태 코드 여부를 확인할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 구성할 수 있습니다. URI 템플릿에서 확장할 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(Dump)

요청이 전송되기 전에 요청 인스턴스를 덤프하고 스크립트 실행을 종료하려면 요청 정의의 시작 부분에 `dd` 메서드를 추가할 수 있습니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

일반적으로 `POST`, `PUT`, `PATCH` 요청 시 추가 데이터를 보냅니다. 이러한 메서드는 데이터 배열을 두 번째 인수로 받으며, 기본적으로 `application/json` 컨텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청의 경우, URL에 쿼리 문자열을 직접 추가하거나, `get` 메서드의 두 번째 인수로 키/값 쌍의 배열을 전달할 수 있습니다.

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
#### Form URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 컨텐츠 타입으로 데이터를 보내려면 요청 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 보내기

요청 시 Raw 요청 본문을 직접 지정하려면 `withBody` 메서드를 사용하세요. 컨텐츠 타입은 두 번째 인수로 지정할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 보내려면 요청 전에 `attach` 메서드를 사용합니다. 파일 이름과 파일 내용을 전달하며, 필요하다면 세 번째 인수로 파일명을, 네 번째 인수로 파일 관련 헤더를 추가할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 콘텐츠 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

`withHeaders` 메서드를 사용해 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키/값 쌍의 배열을 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

요청에 대한 응답으로 어떤 컨텐츠 타입을 기대하는지 명시하려면 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해, `acceptJson` 메서드를 사용해 응답으로 `application/json` 컨텐츠 타입을 간단히 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새로운 헤더를 기존 요청 헤더에 병합합니다. 모든 헤더를 완전히 교체해야 한다면 `replaceHeaders` 메서드를 사용할 수 있습니다.

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

기본 인증과 다이제스트 인증 자격 증명은 각각 `withBasicAuth` 와 `withDigestAuth` 메서드를 사용해 지정할 수 있습니다.

```php
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용하세요.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용해 응답을 기다릴 최대 초(second)를 지정할 수 있습니다. 기본값은 30초입니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 시간 초과 시 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결 시도 중 대기할 최대 초(second)는 `connectTimeout` 메서드로 지정할 수 있습니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 총 시도 횟수와 시도 간 대기할 밀리초(ms)를 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 사이의 sleep 시간을 직접 계산하려면, 두 번째 인수에 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해, 첫 번째 인수에 배열을 전달하면 각 시도 간 대기할 밀리초를 지정할 수 있습니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드의 세 번째 인수로 호출 가능한 콜백을 전달할 수 있습니다. 실제로 재시도를 할지 여부를 결정할 수 있습니다. 예를 들어 최초 요청이 `ConnectionException`을 만났을 때만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 전에 요청을 수정해야 할 경우, `retry` 메서드의 콜백에서 요청 인수를 수정할 수 있습니다. 예를 들어, 인증 오류 시 새로운 인증 토큰으로 재시도하도록 할 수 있습니다.

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

모든 요청이 실패할 경우, `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw: false` 인수를 전달하세요. 이 경우 모든 재시도 완료 후 클라이언트가 받은 마지막 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 문제로 인해 모든 요청이 실패한 경우에는 `throw` 인수가 `false`여도 `Illuminate\Http\Client\ConnectionException`이 여전히 발생합니다.

<a name="error-handling"></a>
### 오류 처리

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버로부터의 400 또는 500대 응답)에 대해 예외를 던지지 않습니다. `successful`, `clientError`, `serverError` 메서드로 이러한 오류 여부를 판단할 수 있습니다.

```php
// 상태 코드가 >= 200이고 < 300인지 확인...
$response->successful();

// 상태 코드가 >= 400인지 확인...
$response->failed();

// 400대 상태 코드가 있는지 확인...
$response->clientError();

// 500대 상태 코드가 있는지 확인...
$response->serverError();

// 클라이언트/서버 오류 시 콜백을 즉시 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생

응답 인스턴스가 있고, 만약 응답의 상태 코드가 클라이언트 또는 서버 오류라면 `Illuminate\Http\Client\RequestException` 인스턴스를 throw 하려면, `throw` 또는 `throwIf` 메서드를 사용합니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류 발생 시 예외 throw...
$response->throw();

// 오류가 발생했고 주어진 조건이 true라면 예외 throw...
$response->throwIf($condition);

// 오류가 발생했고 클로저가 true를 리턴하면 예외 throw...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했고 주어진 조건이 false라면 예외 throw...
$response->throwUnless($condition);

// 오류가 발생했고 클로저가 false를 리턴하면 예외 throw...
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드이면 예외 throw...
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외 throw...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있는 public `$response` 프로퍼티가 있습니다.

`throw` 메서드는 오류가 없을 경우 응답 인스턴스를 반환하므로, `throw` 메서드 이후에도 다른 연산을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 throw되기 전에 추가 로직을 실행하려면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 실행된 후 예외는 자동으로 throw되므로, 클로저 안에서 직접 re-throw 할 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 기록 또는 리포트 시 120자로 잘립니다. 이 동작을 사용자 정의하거나 비활성화하려면, `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지를 240자로 잘라서 기록...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel HTTP 클라이언트는 Guzzle을 기반으로 하기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 나가는 요청을 조작하거나, 반환받은 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 미들웨어를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 반환받은 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드를 사용하세요.

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

모든 나가는 요청 및 오는 응답에 공통으로 적용되는 미들웨어를 등록하고 싶다면 `globalRequestMiddleware` 및 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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

`withOptions` 메서드를 이용해 [추가 Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 이 메서드는 키/값 배열을 인수로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 나가는 요청의 기본 옵션을 설정하려면, `globalOptions` 메서드를 활용할 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩.
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

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 요청을 순차적으로 보내는 대신 여러 요청을 한번에 보냅니다. 이는 느린 HTTP API와 상호작용 시 상당한 성능 향상을 가져올 수 있습니다.

이를 위해 `pool` 메서드를 사용할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받아, 요청 풀에 손쉽게 요청을 추가할 수 있게 해줍니다.

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

보시다시피, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 원한다면 요청에 `as` 메서드로 별명을 붙여, 이름으로 응답을 참조할 수도 있습니다.

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

`pool` 메서드는 `withHeaders`나 `middleware` 등의 HTTP 클라이언트 다른 메서드와 체이닝할 수 없습니다. 풀에 포함될 각 요청에 대해 별도로 옵션을 설정해야 합니다.

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있게 하여, 반복적인 서비스 인터페이스에 사용할 공통 요청 경로 및 헤더 구성을 유창하고 선언적으로 설정할 수 있게 해줍니다. 먼저 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 매크로를 정의하세요.

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩.
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

매크로가 준비되면, 애플리케이션 어디에서나 호출해 지정된 설정으로 대기(pending) 요청을 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스가 쉽고 선언적으로 테스트를 작성할 수 있도록 도와주며, HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드는 HTTP 클라이언트에게 요청 시 스텁/더미 응답을 반환하도록 지시할 수 있습니다.

<a name="faking-responses"></a>
### 응답 모킹

예를 들어, 모든 요청에 대해 빈 200 상태 코드 응답을 반환하도록 하려면 인수 없이 `fake` 메서드를 호출하세요.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 응답 모킹

또는, `fake` 메서드에 배열을 전달해 URL 패턴별로 다른 응답을 지정할 수 있습니다. 배열의 키는 모킹할 URL 패턴이고, 값은 스텁 응답입니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 지정되지 않은 URL은 실제로 요청이 전송됩니다. 엔드포인트별 스텁 응답은 `Http` 파사드의 `response` 메서드로 생성할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 스텁...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

매칭되지 않는 모든 URL을 스텁 처리하는 기본 패턴을 지정하려면 `*` 단일 문자로 설정할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 스텁...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 나머지 엔드포인트 모두에 대한 문자열 응답 스텁...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

단순한 문자열, JSON 배열, 정수 값만으로도 간단히 응답을 지정할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 연결 예외 응답 모킹

때로는 HTTP 클라이언트가 요청 시 `Illuminate\Http\Client\ConnectionException` 예외를 만나도록 테스트가 필요할 수 있습니다. 이때는 `failedConnection` 메서드를 사용해 클라이언트가 연결 예외를 throw하게 만들 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 모킹

하나의 URL에서 일련의 응답을 순서대로 반환해야 하는 경우, `Http::sequence` 메서드를 통해 응답 시퀀스를 구성할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면, 추가 요청 시 예외가 발생합니다. 시퀀스가 비었을 때 반환되는 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답 스텁...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 시퀀스 모킹이 필요하다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 응답 모킹 콜백

특정 엔드포인트에 대해 더 복잡한 논리가 필요하면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 원하는 모든 로직을 수행할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 불필요한 요청 방지

테스트나 테스트 전체 범위에서 HTTP 클라이언트로 전송되는 모든 요청이 반드시 모킹(응답 모킹)을 적용받도록 하려면 `preventStrayRequests` 메서드를 호출하세요. 모킹되지 않은 요청이 발생하면 실제 HTTP 요청 대신 예외가 발생합니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답 반환됨
Http::get('https://github.com/laravel/framework');

// 예외 발생
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 모킹할 때, 클라이언트가 받은 요청을 검사해 올바른 데이터나 헤더가 전송됐는지 확인할 필요가 있습니다. 이럴 때는 `Http::fake` 이후 `Http::assertSent` 메서드를 사용하세요.

`assertSent`는 클로저를 받아 `Illuminate\Http\Client\Request` 인스턴스를 인수로 전달하고, 요청이 기대와 일치하면 true를 반환해야 합니다. 최소 한 건의 요청이 기대에 부합해야 테스트가 통과합니다.

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

필요하다면 `assertNotSent` 메서드를 사용해 특정 요청이 전송되지 않았음을 확인할 수 있습니다.

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

보낸 요청의 개수를 확인하려면 `assertSentCount` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 테스트 중 아무 요청도 전송되지 않았는지를 확인하려면 `assertNothingSent` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용해 모든 요청과 그에 대한 응답을 수집할 수 있습니다. `recorded`는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스가 담긴 배열의 컬렉션을 반환합니다.

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

또한, `recorded` 메서드는 클로저를 인수로 받을 수 있으며, 이를 통해 요청/응답 쌍을 원하는 기준에 따라 필터링할 수 있습니다.

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

Laravel은 HTTP 요청 전송 과정에서 3가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 보내지기 전에, `ResponseReceived` 이벤트는 요청에 대한 응답을 받은 후, `ConnectionFailed` 이벤트는 요청에 대한 응답을 받지 못할 때 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트는 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있게 하는 public `$request` 프로퍼티를 포함합니다. `ResponseReceived` 이벤트 역시 `$request` 및 `Illuminate\Http\Client\Response` 인스턴스를 담은 `$response` 프로퍼티를 가집니다. 해당 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 앱 내에서 만들 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 주어진 이벤트를 처리합니다.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```