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
    - [응답 모의하기](#faking-responses)
    - [요청 검사하기](#inspecting-requests)
    - [불필요한 요청 차단](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로, 표현력 있고 최소한의 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 빠르고 쉽게 만들 수 있습니다. 라라벨의 Guzzle 래퍼는 가장 일반적인 사용 사례와, 개발자가 사용하기 쉬운 경험에 중점을 두고 설계되었습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면, `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 우선, 다른 URL로 `GET` 요청을 보내는 기본 예제를 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 인스턴스는 응답을 다양한 방식으로 조회할 수 있는 여러 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있기 때문에, 응답이 JSON 데이터인 경우 배열처럼 직접 값을 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 소개한 응답 메서드 외에도, 다음과 같은 메서드로 특정 상태 코드 여부를 간편하게 확인할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 지원하여, 요청 URL을 동적으로 만들 수 있도록 합니다. URI 템플릿에서 확장될 수 있는 URL 파라미터를 정의하려면, `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프(Dump)하기

전송 이전에 아웃고잉 요청 인스턴스를 덤프하고, 스크립트 실행을 즉시 중단하고 싶다면 `dd` 메서드를 요청 정의의 맨 앞에 붙여 사용할 수 있습니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH`와 같은 요청 방식에서는 요청과 함께 추가 데이터를 전송하는 경우가 많습니다. 이 메서드들은 두 번째 인자로 데이터 배열을 받을 수 있습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때, 쿼리 문자열을 직접 URL에 붙이거나, `get` 메서드의 두 번째 인자로 키-값 쌍 배열을 전달할 수 있습니다.

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
#### Form URL Encoded 요청 전송

`application/x-www-form-urlencoded` 타입으로 데이터를 전송하고 싶다면, 요청을 보내기 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청 시, Raw 데이터로 바디를 직접 지정하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인자로 지정합니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청(multi-part request)으로 전송하려면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일명을 비롯하여, 파일의 내용, 필요하다면 세 번째 인자로 파일 이름, 네 번째 인자로 관련 헤더 배열을 받을 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 Raw 데이터를 직접 전달하는 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드는 키-값 쌍 배열을 인자로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답에서 애플리케이션이 기대하는 콘텐츠 타입을 지정하고 싶다면 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

보다 간편하게, `acceptJson` 메서드를 사용하면 응답에서 `application/json` 타입을 기대함을 빠르게 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드를 사용하면 새로운 헤더가 기존 요청 헤더에 병합됩니다. 필요에 따라, `replaceHeaders` 메서드로 모든 헤더를 완전히 교체할 수도 있습니다.

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

Basic 인증과 Digest 인증 정보를 각각 `withBasicAuth`와 `withDigestAuth` 메서드를 통해 지정할 수 있습니다.

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하고 싶다면, `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용하여, 응답을 기다릴 최대 초(second) 단위를 지정할 수 있습니다. 별도의 지정이 없다면 HTTP 클라이언트는 기본적으로 30초 뒤에 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정된 타임아웃을 초과하면, `Illuminate\Http\Client\ConnectionException` 인스턴스가 예외로 발생합니다.

서버에 연결을 시도할 때 기다릴 최대 초를 명시하고 싶다면, `connectTimeout` 메서드를 사용하세요. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생할 때 요청을 자동으로 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 시도할 최대 횟수와, 각 시도 사이에 라라벨이 대기할 밀리초(ms) 단위를 인자로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이에 대기할 시간을 직접 계산하고 싶다면, 두 번째 인자로 클로저를 전달하면 됩니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또는, 첫 번째 인자로 배열을 전달할 수도 있습니다. 이 배열은 각 시도마다 대기할 밀리초를 순차적으로 지정합니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인자로 실제로 재시도가 이루어질지 판단하는 콜러블을 전달할 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생했을 때만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

시도 중 요청이 실패했다면, 재시도 전에 요청을 변경하고 싶을 수 있습니다. 이 경우, `retry`에 전달한 콜러블의 두 번째 인자인 요청 인스턴스를 수정하여 처리할 수 있습니다. 예를 들어, 첫 번째 시도에서 인증 오류가 발생했을 때 새로운 인증 토큰으로 재시도하고자 할 경우 아래와 같이 구현할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면, `throw` 인자를 `false`로 전달할 수 있습니다. 비활성화 시, 모든 재시도 후 마지막으로 수신한 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는 `throw` 인자가 `false`여도 `Illuminate\Http\Client\ConnectionException` 예외가 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트 오류(`400`) 또는 서버 오류(`500`)가 발생해도 예외를 발생시키지 않습니다. 이러한 오류가 반환되었는지는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 상태 코드가 400대인지 확인...
$response->clientError();

// 상태 코드가 500대인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류 발생 시 콜백 즉시 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

응답 인스턴스를 가지고 있고, 응답 상태 코드가 클라이언트 혹은 서버 오류라면 `Illuminate\Http\Client\RequestException` 예외를 발생시키려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트나 서버 오류가 발생했을 때 예외를 던짐...
$response->throw();

// 오류가 발생했고 주어진 조건이 true이면 예외를 던짐...
$response->throwIf($condition);

// 오류가 발생했고 주어진 클로저가 true로 평가되면 예외를 던짐...
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했고 주어진 조건이 false이면 예외를 던짐...
$response->throwUnless($condition);

// 오류가 발생했고 주어진 클로저가 false로 평가되면 예외를 던짐...
$response->throwUnless(fn (Response $response) => false);

// 특정 상태 코드를 응답받았을 때 예외를 던짐...
$response->throwIfStatus(403);

// 특정 상태 코드가 아닌 경우 예외를 던짐...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 public `$response` 속성을 가지고 있어, 반환된 응답을 확인할 수 있습니다.

`throw` 메서드는 에러가 없을 경우 응답 인스턴스를 반환하므로, `throw` 이후에 다른 메서드를 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외 발생 전 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 이후 예외가 자동으로 던져지므로, 클로저 내에서 예외를 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로, `RequestException` 메시지는 로그 또는 리포트 시 120자까지만 잘려서 기록됩니다. 이 동작을 커스터마이즈 하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 및 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 예외 메시지를 240자까지 잘라서 기록...
    $exceptions->truncateRequestExceptionsAt(240);

    // 예외 메시지 자르기를 비활성화...
    $exceptions->dontTruncateRequestExceptions();
})
```

또한, 한 요청에서만 예외 메시지 자르기 동작을 커스터마이즈 하려면 `truncateExceptionsAt` 메서드를 사용할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨의 HTTP 클라이언트는 Guzzle을 기반으로 동작하기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 아웃고잉 요청을 수정하거나, 인커밍 응답을 검사할 수 있습니다. 아웃고잉 요청을 조작하려면, `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, `withResponseMiddleware` 메서드로 미들웨어를 등록해 들어오는 HTTP 응답을 검사할 수도 있습니다.

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

모든 아웃고잉 요청과 인커밍 응답에 일괄 적용되는 미들웨어를 등록하고 싶을 때가 있습니다. 이럴 때는 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 보통 이러한 설정은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다.

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

아웃고잉 요청에 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 명시하려면, `withOptions` 메서드를 사용할 수 있습니다. 이 메서드는 키-값 쌍 배열을 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 아웃고잉 요청의 기본 옵션을 지정하려면, `globalOptions` 메서드를 활용할 수 있습니다. 이 메서드는 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

여러 개의 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 요청을 순차적으로 보내는 대신, 여러 요청을 한 번에 동시에 보낼 때 사용할 수 있습니다. 느린 HTTP API와 상호 작용할 때, 이런 방식은 성능 개선에 큰 도움이 됩니다.

라라벨에서는 `pool` 메서드를 사용해 이 기능을 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인자로 받아, 이 인스턴스에 요청을 쉽게 추가할 수 있도록 해줍니다.

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

보시다시피, 각 응답 인스턴스는 풀에 추가된 순서대로 배열 인덱스로 접근할 수 있습니다. 원한다면 요청에 이름을 붙일 수도 있는데, `as` 메서드를 사용하면 됩니다. 이렇게 하면 이름으로 응답을 조회할 수 있습니다.

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

`pool` 메서드는 `withHeaders`나 `middleware`와 같은 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 담긴 각 요청마다 커스텀 헤더나 미들웨어를 적용하려면, 각 요청에 직접 옵션을 설정해야 합니다.

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

라라벨 HTTP 클라이언트는 "매크로" 기능을 지원합니다. 매크로를 통해 서비스별로 자주 사용하는 요청 경로나 헤더 설정을 한 번에 구성하는 등, 보다 선언적이고 유연하게 재사용할 수 있습니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의하면 됩니다.

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

매크로가 설정되면, 애플리케이션 어디에서나 지정한 구성을 가진 대기 중인 요청을 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

## 테스트

많은 라라벨 서비스들은 테스트를 쉽고 명확하게 작성할 수 있도록 다양한 기능을 제공합니다. 라라벨의 HTTP 클라이언트 역시 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면, 요청이 발생할 때 HTTP 클라이언트가 미리 준비해둔 더미(stub) 응답을 반환하게 만들 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리

예를 들어, HTTP 클라이언트가 모든 요청에 대해 비어 있는 `200` 상태 코드의 응답을 반환하도록 하려면, `fake` 메서드를 인자 없이 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는 `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜 처리를 원하는 URL 패턴을, 값은 해당 URL에 대한 응답을 나타냅니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 가짜 처리가 지정되지 않은 URL로의 요청은 실제로 실행됩니다. `Http` 파사드의 `response` 메서드를 사용하여 이러한 엔드포인트에 대한 더미/가짜 응답을 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답 가짜 처리...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 일치하지 않는 URL에 대해 응답을 가짜 처리하는 기본 URL 패턴을 지정하려면, 단일 `*` 문자를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대한 문자열 응답 가짜 처리...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

간단하게 문자열, JSON, 빈 응답을 생성하고 싶을 때는 응답값으로 문자열, 배열, 또는 정수를 전달하면 됩니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜 처리

때로는 HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`이 발생할 경우 애플리케이션이 어떻게 동작하는지 테스트해야 할 경우가 있습니다. 이럴 때는 `failedConnection` 메서드를 사용하여 HTTP 클라이언트가 연결 예외를 발생시키도록 할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`이 발생할 경우를 테스트하고 싶다면 `failedRequest` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

특정 URL에 대해 연속된 여러 개의 가짜 응답을 차례대로 반환해야 할 때가 있습니다. `Http::sequence` 메서드를 사용하여 응답의 시퀀스를 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답을 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스에 포함된 응답이 모두 소진되면, 이후 요청이 발생할 경우 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하고 싶다면 `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 응답을 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 응답 시퀀스를 가짜 처리하고 싶다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 결정하는 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 매개변수로 받아, 원하는 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 필요한 모든 로직을 구현할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 의도치 않은 실제 요청 방지

HTTP 클라이언트를 통한 모든 요청이 테스트 중에 반드시 가짜 처리되었는지 보장하고 싶다면, `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 메서드를 호출하면, 가짜 응답이 지정되지 않은 요청이 실제로 실행되는 대신 예외가 발생하게 됩니다.

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

<a name="inspecting-requests"></a>
### 요청 확인

가짜 응답을 사용할 때, 클라이언트가 받는 요청을 확인해서 애플리케이션이 올바른 데이터나 헤더를 전송하는지 검증하고 싶을 수 있습니다. 이럴 때는 `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 사용할 수 있습니다.

`assertSent` 메서드는 클로저를 인자로 받으며, 이 클로저에는 `Illuminate\Http\Client\Request` 인스턴스가 전달됩니다. 클로저는 요청이 기대한 조건과 일치할 경우 `true`를 반환해야 합니다. 최소한 하나 이상의 요청이 조건을 만족해야 테스트가 통과하게 됩니다.

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

필요하다면, 특정 요청이 전송되지 않았는지 검증하는 `assertNotSent` 메서드도 사용할 수 있습니다.

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

테스트 중 "전송된" 요청의 개수를 검증하려면 `assertSentCount` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는, 테스트 중 어떤 요청도 전송되지 않았음을 검증하고 싶다면 `assertNothingSent` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 해당 응답을 수집할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스가 포함된 배열(들)로 이루어진 컬렉션을 반환합니다.

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

또한, `recorded` 메서드는 클로저를 인자로 받아, 이 안에서 특정 요청/응답 페어만 필터링할 수 있습니다.

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

라라벨은 HTTP 요청을 보내는 과정에서 총 세 가지 이벤트를 발생시킵니다. 요청이 전송되기 전에 `RequestSending` 이벤트가, 특정 요청에 대한 응답을 받은 후에는 `ResponseReceived` 이벤트가 발생합니다. 요청에 대해 응답을 받지 못하면 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 모두 `public $request` 속성이 포함되어 있어, `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있습니다. `ResponseReceived` 이벤트에는 `request` 속성과 함께, `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있는 `response` 속성도 포함되어 있습니다. 이러한 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 애플리케이션 내에서 만들 수 있습니다.

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