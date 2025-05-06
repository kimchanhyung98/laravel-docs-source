# HTTP 클라이언트

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

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 위에 간결하고 직관적인 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 보낼 수 있도록 지원합니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자 경험에 초점을 맞추고 있습니다.

시작하기 전에, 애플리케이션에서 Guzzle 패키지가 의존성으로 설치되어 있는지 확인해야 합니다. 기본적으로 Laravel은 이 의존성을 자동으로 포함하지만, 이전에 패키지를 삭제했다면 Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

    use Illuminate\Support\Facades\Http;

    $response = Http::get('http://example.com');

`get` 메서드는 다양한 응답 검사 메서드를 제공하는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다:

    $response->body() : string;
    $response->json($key = null, $default = null) : array|mixed;
    $response->object() : object;
    $response->collect($key = null) : Illuminate\Support\Collection;
    $response->status() : int;
    $response->successful() : bool;
    $response->redirect(): bool;
    $response->failed() : bool;
    $response->clientError() : bool;
    $response->header($header) : string;
    $response->headers() : array;

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다:

    return Http::get('http://example.com/users/1')['name'];

위에서 나열한 응답 메서드 외에도, 주어진 상태 코드를 가지고 있는지 확인하는 메서드도 사용할 수 있습니다:

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

<a name="uri-templates"></a>
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 규격](https://www.rfc-editor.org/rfc/rfc6570)에 따라 요청 URL을 구성할 수도 있습니다. URI 템플릿에서 확장할 수 있는 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용하세요:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '9.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버깅(dump)

요청을 보내기 전에 요청 인스턴스를 dump하고 스크립트 실행을 중단하려면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하세요:

    return Http::dd()->get('http://example.com');

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청을 할 때 추가 데이터를 함께 전송하는 것이 일반적입니다. 이런 메서드들은 두 번째 인수로 데이터 배열을 받으며, 기본적으로 데이터는 `application/json` Content-Type으로 전송됩니다:

    use Illuminate\Support\Facades\Http;

    $response = Http::post('http://example.com/users', [
        'name' => 'Steve',
        'role' => 'Network Administrator',
    ]);

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 할 때, URL에 쿼리 문자열을 직접 추가하거나, `get` 메서드의 두 번째 인수로 키/값 쌍 배열을 전달할 수 있습니다:

    $response = Http::get('http://example.com/users', [
        'name' => 'Taylor',
        'page' => 1,
    ]);

혹은 `withQueryParameters` 메서드를 사용해도 됩니다:

    Http::retry(3, 100)->withQueryParameters([
        'name' => 'Taylor',
        'page' => 1,
    ])->get('http://example.com/users')

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 전송

`application/x-www-form-urlencoded` 타입으로 데이터를 보내고 싶다면, 요청 전 `asForm` 메서드를 호출하세요:

    $response = Http::asForm()->post('http://example.com/users', [
        'name' => 'Sara',
        'role' => 'Privacy Consultant',
    ]);

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 바디 전송

요청할 때 Raw 바디를 직접 제공하고 싶다면, `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 Content-Type을 지정할 수 있습니다:

    $response = Http::withBody(
        base64_encode($photo), 'image/jpeg'
    )->post('http://example.com/photo');

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 전송하고자 한다면, 요청 전 `attach` 메서드를 호출합니다. 첫 번째 인수는 파일 이름, 두 번째는 파일 내용이며, 세 번째는 파일명을, 네 번째는 파일에 대한 헤더를 지정할 수 있습니다:

    $response = Http::attach(
        'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
    )->post('http://example.com/attachments');

파일의 raw 내용 대신 stream 리소스를 전달할 수도 있습니다:

    $photo = fopen('photo.jpg', 'r');

    $response = Http::attach(
        'attachment', $photo, 'photo.jpg'
    )->post('http://example.com/attachments');

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용하세요. `withHeaders`는 키/값 쌍의 배열을 받습니다:

    $response = Http::withHeaders([
        'X-First' => 'foo',
        'X-Second' => 'bar'
    ])->post('http://example.com/users', [
        'name' => 'Taylor',
    ]);

요청 응답에서 기대하는 Content-Type을 지정하려면 `accept` 메서드를 사용할 수 있습니다:

    $response = Http::accept('application/json')->get('http://example.com/users');

자주 사용되는 경우, `acceptJson` 메서드로 `application/json` 타입을 간편하게 지정할 수 있습니다:

    $response = Http::acceptJson()->get('http://example.com/users');

`withHeaders`는 새로운 헤더를 기존 요청 헤더에 병합합니다. 필요시, `replaceHeaders`를 사용해 모든 헤더를 대체할 수도 있습니다:

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

기본 및 다이제스트 인증 자격 정보를 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다:

    // 기본 인증...
    $response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

    // 다이제스트 인증...
    $response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);

<a name="bearer-tokens"></a>
#### 베어러 토큰

`Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면, `withToken` 메서드를 사용하세요:

    $response = Http::withToken('token')->post(/* ... */);

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드로 응답 대기 최대 시간을(초 단위) 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다:

    $response = Http::timeout(3)->get(/* ... */);

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버 연결을 시도하는 시간의 최대값을 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다:

    $response = Http::connectTimeout(3)->get(/* ... */);

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류 발생 시 요청을 자동으로 재시도하고 싶다면, `retry` 메서드를 사용하세요. 이 메서드는 최대 시도 횟수와 각 시도 사이 대기 밀리초(ms)를 받습니다:

    $response = Http::retry(3, 100)->post(/* ... */);

시도 사이 대기 시간을 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다:

    use Exception;

    $response = Http::retry(3, function (int $attempt, Exception $exception) {
        return $attempt * 100;
    })->post(/* ... */);

또는 첫 번째 인수에 배열을 전달할 수도 있습니다. 이 배열은 각 시도별 대기 시간을 밀리초 단위로 지정합니다:

    $response = Http::retry([100, 200])->post(/* ... */);

필요하다면, 세 번째 인수로 실제 재시도 여부를 판단하는 콜러블을 줄 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생할 때만 재시도하도록 할 수 있습니다:

    use Exception;
    use Illuminate\Http\Client\PendingRequest;

    $response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
        return $exception instanceof ConnectionException;
    })->post(/* ... */);

요청이 실패하면 재시도 전 요청을 수정할 수 있습니다. 콜러블에서 요청 인수를 수정하면 됩니다. 예를 들어, 401 인증 오류 발생 시 새로운 토큰으로 재시도할 수 있습니다:

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException`이 발생합니다. 이 동작을 비활성화하려면 `throw` 인수에 `false`를 전달하세요. 비활성화 시 모든 재시도 후 마지막 응답이 반환됩니다:

    $response = Http::retry(3, 100, throw: false)->post(/* ... */);

> [!WARNING]  
> 연결 문제로 모든 요청이 실패할 경우, `throw` 인수가 `false`이어도 `Illuminate\Http\Client\ConnectionException`은 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트/서버 오류(서버로부터 `400`·`500` 상태)가 발생해도 예외를 throw하지 않습니다. 이런 오류가 반환되었는지는 `successful`, `clientError`, `serverError` 메서드를 통해 확인할 수 있습니다:

    // 상태 코드가 200 이상 300 미만인지 확인
    $response->successful();

    // 400 이상인지 확인
    $response->failed();

    // 400번대 상태코드인지 확인
    $response->clientError();

    // 500번대 상태코드인지 확인
    $response->serverError();

    // 클라이언트 혹은 서버 에러가 있으면 콜백 즉시 실행
    $response->onError(callable $callback);

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스가 있을 때, 클라이언트나 서버 오류가 발생하면 `Illuminate\Http\Client\RequestException`을 throw하도록 하려면, `throw` 또는 `throwIf` 메서드를 사용하세요:

    use Illuminate\Http\Client\Response;

    $response = Http::post(/* ... */);

    // 에러가 발생하면 예외 throw
    $response->throw();

    // 에러 발생하며 주어진 조건이 true라면 예외 throw
    $response->throwIf($condition);

    // 에러 발생이며 클로저 결과가 true라면 예외 throw
    $response->throwIf(fn (Response $response) => true);

    // 에러 발생하며 조건이 false라면 예외 throw
    $response->throwUnless($condition);

    // 에러 발생이며 클로저 결과가 false라면 예외 throw
    $response->throwUnless(fn (Response $response) => false);

    // 특정 상태 코드면 예외 throw
    $response->throwIfStatus(403);

    // 특정 상태 코드가 아니라면 예외 throw
    $response->throwUnlessStatus(200);

    return $response['user']['id'];

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 확인할 수 있는 public `$response` 속성을 가집니다.

`throw` 메서드는 에러가 없으면 응답 인스턴스를 반환하므로, 메서드 체이닝이 가능합니다:

    return Http::post(/* ... */)->throw()->json();

예외가 throw되기 전에 추가 로직을 실행하고 싶다면, 클로저를 `throw`에 전달할 수 있습니다. 클로저 실행 후 예외는 자동으로 throw되므로, 클로저 내에서 직접 예외를 다시 던질 필요는 없습니다:

    use Illuminate\Http\Client\Response;
    use Illuminate\Http\Client\RequestException;

    return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
        // ...
    })->json();

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 하기 때문에 [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청을 조작하거나 응답을 검사할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle 미들웨어를 등록하세요:

    use Illuminate\Support\Facades\Http;
    use Psr\Http\Message\RequestInterface;

    $response = Http::withRequestMiddleware(
        function (RequestInterface $request) {
            return $request->withHeader('X-Example', 'Value');
        }
    )->get('http://example.com');

마찬가지로 들어오는 응답을 검사하려면 `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다:

    use Illuminate\Support\Facades\Http;
    use Psr\Http\Message\ResponseInterface;

    $response = Http::withResponseMiddleware(
        function (ResponseInterface $response) {
            $header = $response->getHeader('X-Example');

            // ...

            return $response;
        }
    )->get('http://example.com');

<a name="global-middleware"></a>
#### 전역 미들웨어

모든 요청 및 응답에 공통 미들웨어를 적용하려면, `globalRequestMiddleware` 및 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)이 필요하다면, `withOptions` 메서드를 통해 키/값 쌍의 배열로 전달할 수 있습니다:

    $response = Http::withOptions([
        'debug' => true,
    ])->get('http://example.com/users');

<a name="concurrent-requests"></a>
## 동시 요청

때때로, 여러 HTTP 요청을 동시에 보내고 싶을 수 있습니다. 즉, 순차적으로 요청하는 대신 여러 요청을 한 번에 발송하면 느린 HTTP API와 상호작용할 때 성능을 크게 향상시킬 수 있습니다.

`pool` 메서드를 사용하여 이 작업을 손쉽게 수행할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받아, 요청 풀에 요청을 쉽게 추가할 수 있게 해줍니다:

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

각 응답 인스턴스는 풀에 추가된 순서에 따라 접근할 수 있습니다. 요청에 이름을 붙이고 싶다면, `as` 메서드를 사용해 해당 이름으로 응답에 접근할 수 있습니다:

    use Illuminate\Http\Client\Pool;
    use Illuminate\Support\Facades\Http;

    $responses = Http::pool(fn (Pool $pool) => [
        $pool->as('first')->get('http://localhost/first'),
        $pool->as('second')->get('http://localhost/second'),
        $pool->as('third')->get('http://localhost/third'),
    ]);

    return $responses['first']->ok();

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이징

`pool` 메서드는 `withHeaders`, `middleware` 등의 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 들어가는 각 요청별로 헤더, 미들웨어를 직접 설정해야 합니다:

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있습니다. 매크로란 서비스와 상호작용할 때 공통 경로나 헤더를 유연하고 명확하게 설정할 수 있는 방법입니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의할 수 있습니다:

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

매크로를 설정한 후에는 어디서든 해당 매크로를 호출해 지정한 설정의 대기 요청 인스턴스를 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

다른 Laravel 서비스와 마찬가지로, HTTP 클라이언트도 쉽고 명확하게 테스트를 작성할 수 있는 다양한 기능을 제공합니다. `Http` 파사드의 `fake` 메서드는 요청이 발생할 때 스텁/더미 응답을 반환하도록 HTTP 클라이언트에 지시합니다.

<a name="faking-responses"></a>
### 응답 가짜 처리(Fake)

예를 들어, 모든 요청에 대해 빈 `200` 응답을 반환하려면 `fake` 메서드를 인수 없이 호출하면 됩니다:

    use Illuminate\Support\Facades\Http;

    Http::fake();

    $response = Http::post(/* ... */);

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

대신, `fake` 메서드에 배열을 전달하여 특정 URL 패턴에 대해 어떤 응답을 반환할지 정의할 수 있습니다. `*`는 와일드카드로 사용됩니다. 지정하지 않은 URL은 실제 요청이 발생합니다. 엔드포인트 응답의 스텁 작성에는 `Http` 파사드의 `response` 메서드를 활용할 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트에 대한 JSON 응답 스텁
        'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

        // Google 엔드포인트에 대한 문자열 응답 스텁
        'google.com/*' => Http::response('Hello World', 200, $headers),
    ]);

매치되지 않은 모든 URL에 대한 기본값을 지정하려면, 하나의 `*` 패턴을 사용하세요:

    Http::fake([
        // GitHub 엔드포인트에 대한 JSON 응답 스텁
        'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

        // 그 외 모든 엔드포인트에 문자열 응답 스텁
        '*' => Http::response('Hello World', 200, ['Headers']),
    ]);

<a name="faking-response-sequences"></a>
#### 연속 응답 가짜 처리

특정 URL에 대해 순차적으로 여러 개의 스텁 응답을 반환하도록 하려면, `Http::sequence`를 사용해서 응답 시퀀스를 구성할 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트에 대한 응답 연속 스텁
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->pushStatus(404),
    ]);

응답 시퀀스의 모든 항목을 소비하면 이후 요청에는 예외가 발생합니다. 빈 시퀀스에 대해 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

    Http::fake([
        // GitHub 엔드포인트에 대한 응답 연속 스텁
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->whenEmpty(Http::response()),
    ]);

특정 URL 패턴 없이 응답 연속 스텁만 필요하다면, `Http::fakeSequence`를 사용할 수 있습니다:

    Http::fakeSequence()
            ->push('Hello World', 200)
            ->whenEmpty(Http::response());

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 반환할 응답을 결정하는 로직이 복잡하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스와 옵션 배열을 받으며, 응답 인스턴스를 반환해야 합니다. 클로저 내에서 어떤 응답을 반환할지 자유롭게 로직을 구현할 수 있습니다:

    use Illuminate\Http\Client\Request;

    Http::fake(function (Request $request, array $options) {
        return Http::response('Hello World', 200);
    });

<a name="preventing-stray-requests"></a>
### 불필요한(실제) 요청 방지

테스트 도중 모든 요청이 가짜 처리가 되었는지 확인하고 싶다면, `preventStrayRequests` 메서드를 사용할 수 있습니다. 이 메서드 호출 후에 스텁되지 않은 요청이 발생하면 실제 요청이 실행되는 대신 예외가 throw됩니다:

    use Illuminate\Support\Facades\Http;

    Http::preventStrayRequests();

    Http::fake([
        'github.com/*' => Http::response('ok'),
    ]);

    // "ok" 응답 반환
    Http::get('https://github.com/laravel/framework');

    // 예외 발생
    Http::get('https://laravel.com');

<a name="inspecting-requests"></a>
### 요청 검사

응답 스텁을 사용할 때, 클라이언트가 받은 요청에 올바른 데이터/헤더가 전송되었는지 검사하고 싶을 수 있습니다. `Http::fake` 호출 후 `Http::assertSent` 메서드로 이를 확인할 수 있습니다.

`assertSent`는 `Illuminate\Http\Client\Request` 인스턴스를 받는 클로저를 인수로 받으며, 요청이 조건에 부합하면 반드시 하나 이상 통과해야 테스트가 성공합니다:

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

특정 요청이 발송되지 않았는지도 `assertNotSent`로 체크합니다:

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

테스트 중 "전송된" 요청 수를 `assertSentCount`로 검증할 수 있습니다:

    Http::fake();

    Http::assertSentCount(5);

또는, 테스트 동안 아무 요청도 전송되지 않았는지를 `assertNothingSent`으로 확인할 수 있습니다:

    Http::fake();

    Http::assertNothingSent();

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 해당 응답을 수집할 수 있습니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 배열로 가지는 컬렉션을 반환합니다:

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

또한, `recorded`는 클로저도 받아, 요청/응답 쌍에 대한 필터링이 가능합니다:

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

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에, `ResponseReceived` 이벤트는 응답을 받은 후, `ConnectionFailed` 이벤트는 응답을 받지 못한 경우 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스 확인을 위한 public `$request` 속성이 있으며, `ResponseReceived` 이벤트에는 `$request`와 `$response` 속성이 포함되어 있습니다. 이벤트 리스너는 `App\Providers\EventServiceProvider` 서비스 제공자에 등록할 수 있습니다:

    /**
     * 애플리케이션 이벤트 리스너 매핑
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Http\Client\Events\RequestSending' => [
            'App\Listeners\LogRequestSending',
        ],
        'Illuminate\Http\Client\Events\ResponseReceived' => [
            'App\Listeners\LogResponseReceived',
        ],
        'Illuminate\Http\Client\Events\ConnectionFailed' => [
            'App\Listeners\LogConnectionFailed',
        ],
    ];