# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 만들기](#making-requests)
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
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [무단 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 표현력이 풍부하고 최소한의 API를 제공하여, 다른 웹 애플리케이션과의 통신을 위해 외부 HTTP 요청을 빠르게 보낼 수 있도록 지원합니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례와 개발자 경험에 초점을 맞추고 있습니다.

시작하기 전에, 애플리케이션의 의존성으로 Guzzle 패키지가 설치되어 있는지 확인해야 합니다. Laravel은 기본적으로 이 의존성을 자동으로 포함합니다. 그러나 이전에 이 패키지를 제거했다면, 다음 Composer 명령어로 다시 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

요청을 만들기 위해 `Http` 파사드에 제공된 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 대한 기본 `GET` 요청을 만드는 방법을 살펴보겠습니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공합니다:

```
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
```

`Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스도 구현하여, JSON 응답 데이터를 응답 인스턴스에서 직접 접근할 수 있습니다:

```
return Http::get('http://example.com/users/1')['name'];
```

위에 나열한 응답 메서드 외에도, 다음 메서드를 사용하여 응답의 특정 상태 코드 여부를 알 수 있습니다:

```
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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수 있습니다. URI 템플릿에 의해 확장될 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '9.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프하기

보낼 요청 인스턴스를 스크립트 실행 전 덤프하고 종료하고 싶다면, 요청 정의 시작 부분에 `dd` 메서드를 추가하면 됩니다:

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청을 보낼 때 추가 데이터를 보내는 것이 일반적이므로, 이 메서드들은 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 매개변수

`GET` 요청 시, 쿼리 문자열을 URL에 직접 추가하거나 `get` 메서드의 두 번째 인수로 키-값 배열을 전달할 수 있습니다:

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 전송하려면 요청 전에 `asForm` 메서드를 호출해야 합니다:

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청 시 원시 요청 본문을 제공하려면 `withBody` 메서드를 사용할 수 있으며, 두 번째 인수로 콘텐츠 타입도 지정할 수 있습니다:

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 전송하려면, 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일 이름과 내용물을 받으며, 필요시 세 번째 인수로 파일 이름을 명시할 수 있습니다:

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
)->post('http://example.com/attachments');
```

파일의 원시 내용 대신 스트림 리소스를 전달할 수도 있습니다:

```
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키-값 배열을 받습니다:

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드는 요청에 대해 기대하는 응답 콘텐츠 타입을 지정하는 데 사용할 수 있습니다:

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

간편하게 `application/json` 타입을 지정하려면 `acceptJson` 메서드를 사용할 수 있습니다:

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<a name="authentication"></a>
### 인증 (Authentication)

`withBasicAuth`와 `withDigestAuth` 메서드를 사용해 각각 기본 인증과 다이제스트 인증 자격 증명을 지정할 수 있습니다:

```
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용할 수 있습니다:

```
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드는 응답을 기다릴 최대 시간을 초 단위로 지정하는 데 사용합니다:

```
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃 시간이 초과되면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 던져집니다.

서버에 연결 시 최대 대기 시간을 초 단위로 지정하려면 `connectTimeout` 메서드를 사용합니다:

```
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류가 발생할 경우 HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry`는 요청을 최대 시도할 횟수와 각 시도 사이의 대기 시간(밀리초)을 인수로 받습니다:

```
$response = Http::retry(3, 100)->post(/* ... */);
```

필요하면 `retry` 메서드에 세 번째 인수로 재시도 여부를 결정하는 콜러블을 전달할 수 있습니다. 예를 들어, 초기 요청이 `ConnectionException`을 만났을 때만 재시도하도록 할 수 있습니다:

```
$response = Http::retry(3, 100, function ($exception, $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

재시도 시 요청을 변경하고 싶다면, `retry` 메서드에 넘긴 콜러블의 요청 인수를 수정할 수 있습니다. 예를 들어 첫 시도에서 인증 오류가 발생하면 새 인증 토큰으로 재시도할 수 있습니다:

```
$response = Http::withToken($this->getToken())->retry(2, 0, function ($exception, $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 던져집니다. 이 동작을 비활성화하려면 `throw` 인수에 `false` 값을 줄 수 있습니다. 비활성화 시, 모든 재시도가 끝난 후 마지막 응답이 반환됩니다:

```
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패하면, `throw`가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException`이 던져집니다.

<a name="error-handling"></a>
### 오류 처리 (Error Handling)

Guzzle 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(`400`, `500`번대 응답) 발생 시 예외를 던지지 않습니다. 대신 `successful`, `clientError`, `serverError` 메서드로 오류 여부를 확인할 수 있습니다:

```
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 클라이언트 오류(400번대)인지 확인...
$response->clientError();

// 서버 오류(500번대)인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 있으면 즉시 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스를 가지고 있고, 클라이언트 또는 서버 오류가 있으면 `Illuminate\Http\Client\RequestException`을 던지고 싶다면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```
$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 발생하면 예외 던지기...
$response->throw();

// 오류가 있고 주어진 조건이 참일 때 예외 던지기...
$response->throwIf($condition);

// 오류가 있고 주어진 클로저가 참일 때 예외 던지기...
$response->throwIf(fn ($response) => true);

// 오류가 있고 주어진 조건이 거짓일 때 예외 던지기...
$response->throwUnless($condition);

// 오류가 있고 주어진 클로저가 거짓일 때 예외 던지기...
$response->throwUnless(fn ($response) => false);

// 특정 상태 코드일 때 예외 던지기...
$response->throwIfStatus(403);

// 특정 상태 코드가 아닐 때 예외 던지기...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 반환된 응답을 검사할 수 있게 공개된 `$response` 속성을 포함합니다.

오류가 없으면 `throw` 메서드는 응답 인스턴스를 반환하여 메서드 체이닝을 지원합니다:

```
return Http::post(/* ... */)->throw()->json();
```

예외가 던져지기 전에 추가 작업을 하려면 `throw` 메서드에 클로저를 넘길 수 있습니다. 이 클로저가 호출된 후 예외가 자동으로 던져지므로, 클로저 내에서 다시 던질 필요는 없습니다:

```
return Http::post(/* ... */)->throw(function ($response, $e) {
    //
})->json();
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트가 Guzzle 기반이므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 전송 요청을 조작하거나 받은 응답을 검사할 수 있습니다. 전송 요청을 조작하려면 `withMiddleware` 메서드와 Guzzle의 `mapRequest` 미들웨어 팩토리를 함께 등록하세요:

```
use GuzzleHttp\Middleware;
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withMiddleware(
    Middleware::mapRequest(function (RequestInterface $request) {
        $request = $request->withHeader('X-Example', 'Value');
        
        return $request;
    })
)->get('http://example.com');
```

마찬가지로, `withMiddleware` 메서드와 Guzzle의 `mapResponse` 미들웨어 팩토리를 이용해 들어오는 HTTP 응답을 검사할 수 있습니다:

```
use GuzzleHttp\Middleware;
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withMiddleware(
    Middleware::mapResponse(function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...
        
        return $response;
    })
)->get('http://example.com');
```

<a name="guzzle-options"></a>
### Guzzle 옵션 (Guzzle Options)

추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)은 `withOptions` 메서드로 지정할 수 있으며, 이 메서드는 키-값 배열을 받습니다:

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
## 동시 요청 (Concurrent Requests)

여러 HTTP 요청을 동시에 보내길 원할 때가 있습니다. 즉, 순차적으로 요청을 보내는 대신 여러 요청을 동시에 실행하면 느린 HTTP API와 통신할 때 성능이 크게 향상될 수 있습니다.

이 경우, `pool` 메서드를 사용하면 됩니다. `pool`은 `Illuminate\Http\Client\Pool` 인스턴스를 매개변수로 받는 클로저를 받아, 요청 풀에 쉽게 요청을 추가하고 동시에 요청을 보낼 수 있게 해 줍니다:

```
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

각 응답 인스턴스는 요청이 추가된 순서대로 배열에서 접근할 수 있습니다. 필요하다면 `as` 메서드로 요청에 이름을 붙여, 이름으로 응답에 접근할 수도 있습니다:

```
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

<a name="macros"></a>
## 매크로 (Macros)

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있어, 애플리케이션 전반에 걸쳐 서비스와 상호작용할 때 공통적인 요청 경로나 헤더를 유창하고 표현력 있게 구성하는 데 사용할 수 있습니다. 시작하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 `boot` 메서드 내에서 매크로를 정의하세요:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

매크로를 설정한 후에는 애플리케이션 어디서든 해당 매크로를 호출하여 지정한 구성으로 대기 중인 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스가 테스트를 쉽게 우아하게 작성할 수 있도록 기능을 제공하며, Laravel HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드는 요청 시 가짜(스텁) 응답을 반환하도록 클라이언트를 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜 처리 (Faking Responses)

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하도록 HTTP 클라이언트에 지시하려면 `fake` 메서드를 인수 없이 호출합니다:

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 가짜 처리

또는, `fake` 메서드에 배열을 전달할 수 있으며, 배열 키는 가짜 처리를 원하는 URL 패턴이고 값은 대응하는 스텁 응답입니다. `*` 문자를 와일드카드로 사용할 수 있으며, 가짜 처리하지 않은 URL 요청은 실제로 요청됩니다. `Http` 파사드의 `response` 메서드로 스텁 응답을 생성할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 스텁 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 스텁 응답...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

가짜 처리되지 않은 URL에 대해 기본 응답을 지정하려면 단일 `*` 문자를 사용할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 스텁 응답...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대한 문자열 스텁 응답...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 가짜 처리

단일 URL이 일정한 순서로 여러 가짜 응답을 반환해야 할 때가 있습니다. 이 경우 `Http::sequence` 메서드를 사용하여 응답들을 구성할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 스텁 응답...
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->pushStatus(404),
]);
```

응답 시퀀스의 모든 응답을 다 사용하면, 추가 요청 시 시퀀스가 예외를 던집니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용하세요:

```
Http::fake([
    // GitHub 엔드포인트에 대한 일련의 스텁 응답...
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 지정 없이 응답 시퀀스를 가짜 처리하려면 `Http::fakeSequence` 메서드를 쓸 수 있습니다:

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 반환할 응답을 더 복잡한 로직으로 결정하고자 하면, 클로저를 `fake` 메서드에 넘길 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받고, 응답 인스턴스를 반환해야 합니다:

```
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
### 무단 요청 방지 (Preventing Stray Requests)

HTTP 클라이언트를 통한 모든 요청이 테스트 내내 가짜 처리되었는지 보장하고 싶다면, `preventStrayRequests` 메서드를 호출하세요. 이후 가짜 대응이 없는 요청 시 실제 요청 대신 예외가 던져집니다:

```
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답 반환...
Http::get('https://github.com/laravel/framework');

// 예외 발생...
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

가짜 응답을 처리할 때, 클라이언트가 올바른 데이터나 헤더를 보내고 있는지 요청을 검사하고 싶으면 `Http::assertSent` 메서드를 `Http::fake` 호출 후 사용할 수 있습니다.

`assertSent`는 `Illuminate\Http\Client\Request` 인스턴스를 전달받는 클로저를 인수로 받으며, 요청이 예상에 부합하면 `true`를 반환해야 합니다. 테스트가 통과하려면 적어도 하나의 요청이 해당 조건과 일치해야 합니다:

```
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

필요하면 특정 요청이 보내지지 않았음을 단언하려면 `assertNotSent` 메서드를 사용할 수 있습니다:

```
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

`assertSentCount` 메서드로 테스트 중에 "전송된" 요청 수를 단언할 수도 있습니다:

```
Http::fake();

Http::assertSentCount(5);
```

또는, `assertNothingSent` 메서드로 요청이 전송되지 않았음을 단언할 수 있습니다:

```
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하면 모든 요청과 해당 응답 쌍을 가져올 수 있습니다. `recorded`는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 포함하는 배열 컬렉션을 반환합니다:

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

또한, `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`를 받는 클로저를 인수로 받아 요청/응답 쌍을 필터링하는 데 사용할 수 있습니다:

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
## 이벤트 (Events)

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청을 보내기 전에, `ResponseReceived` 이벤트는 응답을 받은 후, `ConnectionFailed` 이벤트는 응답을 받지 못했을 때 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트는 둘 다 공개된 `$request` 속성으로 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있게 합니다. `ResponseReceived` 이벤트는 `$request`와 더불어 응답인 `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있는 `$response` 속성을 포함합니다. 이 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider`에서 등록할 수 있습니다:

```
/**
 * 애플리케이션 이벤트 리스너 매핑.
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
```