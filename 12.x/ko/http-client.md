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
    - [응답 페이크](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

라라벨은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 한 간결하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 빠르게 처리할 수 있습니다. 라라벨이 제공하는 Guzzle 래퍼는 가장 일반적으로 사용되는 기능과 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다양한 응답 검사용 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있기 때문에, 아래처럼 바로 JSON 응답 데이터를 배열처럼 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 소개한 응답 메서드 외에도, 다음과 같은 메서드들을 사용하면 응답의 HTTP 상태 코드가 특정 값인지 쉽게 판별할 수 있습니다.

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

HTTP 클라이언트는 [URI 템플릿 규격](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 동적으로 생성할 수 있도록 지원합니다. 템플릿에서 사용할 URL 매개변수를 지정하려면 `withUrlParameters` 메서드를 사용하세요.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 디버깅(dump)

요청이 전송되기 전에 해당 요청 인스턴스를 덤프(dump)하고 스크립트 실행을 즉시 중지하고 싶을 때는, 요청 정의 앞에 `dd` 메서드를 붙이면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

보통 `POST`, `PUT`, `PATCH` 요청에는 추가적인 데이터를 함께 전송하는 일이 많기 때문에, 이 메서드들은 데이터 배열을 두 번째 인수로 받을 수 있습니다. 기본적으로 이 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청 시에는 URL에 쿼리 문자열을 직접 추가하거나, 쿼리에서 사용할 키/값 쌍의 배열을 `get` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는, `withQueryParameters` 메서드를 활용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL Encoded 요청 보내기

`application/x-www-form-urlencoded` 형식으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청 시 Raw 데이터를 직접 본문에 넣고 싶다면, `withBody` 메서드를 사용할 수 있습니다. 이때 콘텐츠 타입은 메서드의 두 번째 인수로 지정할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 형식으로 전송하려면, 요청 전에 `attach` 메서드를 사용하세요. 이 메서드는 파일의 이름과 데이터(내용)를 인수로 받습니다. 필요하다면 세 번째 인수로 업로드 시 사용할 파일명, 네 번째 인수로 파일에 적용할 헤더 배열을 넘길 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원본 데이터를 직접 넘기는 대신, 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용하면 됩니다. 이 메서드는 키/값 쌍으로 이루어진 배열을 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

응답으로 기대하는 콘텐츠 타입을 지정하고 싶을 때는 `accept` 메서드를 사용할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 간단하게, 응답의 콘텐츠 타입으로 `application/json`을 지정하고 싶다면 `acceptJson` 메서드를 사용할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 요청 헤더에 새로운 헤더를 병합합니다. 만약 필요한 경우, `replaceHeaders` 메서드를 사용하여 모든 헤더를 아예 교체할 수도 있습니다.

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

기본 인증(Basic)과 다이제스트 인증(Digest) 정보를 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다.

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 간편하게 추가하려면, `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

응답을 대기하는 최대 시간을 지정하려면 `timeout` 메서드를 사용하면 됩니다. 기본적으로 HTTP 클라이언트는 30초가 지나면 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 시간이 초과되면, `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도하는 최대 시간을 별도로 지정하고 싶다면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

HTTP 클라이언트가 클라이언트 오류나 서버 오류가 발생했을 때 자동으로 요청을 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 요청을 최대 몇 번까지 시도할지 그리고 각 재시도 사이 대기할 밀리초(ms)를 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

만약 재시도 사이에 대기할 시간을 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

또한, 첫 번째 인수에 배열을 전달하여 요청별로 서로 다른 대기 시간을 지정할 수도 있습니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면, 세 번째 인수로 콜러블을 전달해서 실제로 재시도를 할지 판단하는 조건을 지정할 수 있습니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생한 경우에만 재시도하도록 할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

만약 요청이 실패하면, 다음과 같이 재시도 전에 요청을 조작할 수도 있습니다. 예를 들어, 첫 번째 요청에서 인증 오류가 발생했을 때 새로운 인증 토큰으로 재시도할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수에 `false` 값을 지정하면 됩니다. 비활성화 시, 모든 재시도가 끝난 후 마지막으로 받은 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우에는, `throw` 인수가 `false`여도 여전히 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<a name="error-handling"></a>
### 에러 처리

Guzzle의 기본 동작과 달리, 라라벨의 HTTP 클라이언트 래퍼는 클라이언트 오류(`400`번대), 서버 오류(`500`번대) 발생 시 예외를 자동으로 발생시키지 않습니다. 해당 오류가 발생했는지는 `successful`, `clientError`, `serverError` 메서드를 통해 판단할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 400번대 에러인지 확인
$response->clientError();

// 500번대 에러인지 확인
$response->serverError();

// 클라이언트 또는 서버 오류가 있을 때 바로 주어진 콜백 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 강제 발생

응답 인스턴스가 있는 상태에서, 응답의 상태 코드가 클라이언트 또는 서버 오류를 나타낼 경우 `Illuminate\Http\Client\RequestException` 예외를 강제로 발생시키고 싶다면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트 또는 서버 오류가 발생하면 예외 발생
$response->throw();

// 오류 발생 및 주어진 조건이 true면 예외 발생
$response->throwIf($condition);

// 오류 발생 및 클로저가 true를 반환하면 예외 발생
$response->throwIf(fn (Response $response) => true);

// 오류 발생 및 주어진 조건이 false면 예외 발생
$response->throwUnless($condition);

// 오류 발생 및 클로저가 false를 반환하면 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아니면 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있도록 public `$response` 속성이 포함되어 있습니다.

`throw` 메서드는 오류가 없다면 응답 인스턴스를 그대로 반환하므로, 추가적인 작업을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 실행하고 싶다면, 클로저를 `throw` 메서드에 전달할 수 있습니다. 클로저 실행 후 예외는 자동으로 던져지므로, 클로저 내부에서 다시 예외를 발생시킬 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException`의 메시지는 로깅 또는 보고 시 최대 120자로 잘려(truncate) 표시됩니다. 이 동작을 커스터마이즈하거나 비활성화하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt`와 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions) {
    // 요청 예외 메시지 최대 240자로 자르기
    $exceptions->truncateRequestExceptionsAt(240);

    // 요청 예외 메시지 자르기 비활성화
    $exceptions->dontTruncateRequestExceptions();
})
```

또는, 요청마다 `truncateExceptionsAt` 메서드를 사용하여 예외 메시지 길이를 조정할 수도 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

라라벨 HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) 기능을 활용하여, 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면, `withRequestMiddleware` 메서드를 사용해 Guzzle 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, `withResponseMiddleware` 메서드를 사용하면 들어오는 HTTP 응답도 검사할 수 있습니다.

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

모든 나가는 요청과 들어오는 응답에 공통으로 적용되는 미들웨어를 등록하고 싶을 때는, `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용하면 됩니다. 보통 이 메서드들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 전달하려면, `withOptions` 메서드를 사용하세요. 이 메서드는 키/값 형식의 배열을 인수로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

모든 나가는 요청에 기본 옵션을 적용하고 싶다면, `globalOptions` 메서드를 사용할 수 있습니다. 이 메서드 역시 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

여러 HTTP 요청을 동시에(병렬로) 보내고 싶은 경우가 있습니다. 즉, 요청을 순차적으로 처리하지 않고 한 번에 발송하려는 경우입니다. 이는 느린 HTTP API와 통신할 때 성능을 크게 향상시킬 수 있습니다.

이럴 때는 `pool` 메서드를 사용할 수 있습니다. `pool` 메서드는 콜백을 받으며, 콜백에 전달되는 `Illuminate\Http\Client\Pool` 인스턴스를 통해 여러 요청을 풀에 등록하여 한 번에 발송할 수 있습니다.

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

이렇게 하면, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 원한다면 `as` 메서드로 요청에 이름을 붙이고, 이후 결과도 이름으로 접근할 수 있습니다.

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

`pool` 메서드는 `withHeaders`나 `middleware` 같은 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 개별 요청마다 헤더나 미들웨어를 적용하려면, 풀 내 요청 각각에 대해 옵션을 구성해야 합니다.

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

라라벨 HTTP 클라이언트는 다양한 서비스와 상호 작용할 때 자주 쓰는 경로나 헤더 구성을 손쉽게 복합적으로 지정하도록 "매크로"를 정의할 수 있습니다. 매크로는 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 등록합니다.

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

매크로가 준비되면, 애플리케이션 어디서든 바로 호출하여 해당 설정이 적용된 PendingRequest를 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

## 테스트

많은 라라벨 서비스들은 테스트를 더 쉽고 명확하게 작성할 수 있도록 다양한 기능을 제공합니다. 라라벨의 HTTP 클라이언트 또한 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 HTTP 클라이언트가 요청을 보낼 때 미리 지정한 더미(가짜) 응답을 반환하도록 할 수 있습니다.

<a name="faking-responses"></a>
### 응답 가짜로 만들기

예를 들어, 모든 요청에 대해 비어있는 200 상태 코드의 응답을 반환하도록 HTTP 클라이언트에 지시하고 싶다면, 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 응답 가짜로 만들기

또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜 처리할 URL 패턴을 지정하며, 그 값으로 반환할 응답을 정합니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 가짜 처리가 지정되지 않은 URL로의 요청은 실제로 실행됩니다. 각 엔드포인트를 위한 더미(가짜) 응답을 생성하려면 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대해 문자열 응답 가짜 처리...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

모든 일치하지 않는 URL에 대해 기본적으로 가짜 응답을 반환하고 싶다면, 와일드카드 `*`를 키로 지정하면 됩니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 가짜 처리...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 기타 모든 엔드포인트에 대해 문자열 응답 가짜 처리...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

더 간단하게, 문자열, JSON(배열), 혹은 정수를 응답 값으로 지정하면 자동으로 적절한 가짜 응답이 생성됩니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 가짜로 만들기

HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 상황을 테스트하고 싶을 때가 있습니다. 이 경우 `failedConnection` 메서드를 사용하여 HTTP 클라이언트가 연결 예외를 발생시키도록 설정할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

만약 `Illuminate\Http\Client\RequestException`이 던져지는 상황을 테스트하고 싶다면 `failedRequest` 메서드를 사용하면 됩니다.

```php
Http::fake([
    'github.com/*' => Http::failedRequest(['code' => 'not_found'], 404),
]);
```

<a name="faking-response-sequences"></a>
#### 순차 응답 가짜로 만들기

하나의 URL에서 여러 개의 가짜 응답을 순차적으로 지정하고 싶을 때가 있습니다. 이 때는 `Http::sequence` 메서드를 사용하여 응답 시퀀스를 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 여러 개의 응답을 순차적으로 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스에 지정한 모든 응답이 소진되면, 이후 요청에서는 예외가 발생합니다. 만약 시퀀스가 비었을 때 반환할 기본 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 여러 개의 응답을 순차적으로 가짜 처리...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴을 지정하지 않고 단순히 일련의 응답 시퀀스를 가짜로 만들고 싶다면, `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저에는 `Illuminate\Http\Client\Request` 인스턴스가 전달되며, 이곳에서 필요한 로직을 처리한 뒤 적절한 응답 인스턴스를 반환하면 됩니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사하기

가짜 응답을 사용할 때, 실제로 클라이언트가 어떤 요청을 받았는지 확인해서 애플리케이션이 올바른 데이터나 헤더를 전송하는지 검사하고 싶을 때가 있습니다. 이럴 때는 `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent` 메서드는 클로저를 인자로 받으며, 이 클로저에는 `Illuminate\Http\Client\Request` 인스턴스가 전달됩니다. 클로저는 요청이 기대와 일치하면 `true`를 반환해야 합니다. 하나라도 해당 조건을 만족하는 요청이 있었다면 테스트는 통과합니다.

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

필요하다면, `assertNotSent` 메서드를 사용해서 특정 요청이 전송되지 않았음을 검증할 수도 있습니다.

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

테스트 중에 "전송된" 요청의 수를 검증하고 싶을 때는 `assertSentCount` 메서드를 사용할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는 테스트 중에 어떤 요청도 전송되지 않았음을 검증하고 싶다면 `assertNothingSent` 메서드를 사용하세요.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 및 응답 기록하기

`recorded` 메서드를 사용하면 모든 요청과 각 요청에 대한 응답을 모을 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request` 및 `Illuminate\Http\Client\Response` 인스턴스를 포함하는 배열의 컬렉션을 반환합니다.

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

또한, `recorded` 메서드에 클로저를 전달하여 특정 조건에 맞는 요청/응답 페어만 필터링할 수도 있습니다. 이 클로저에는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스가 인자로 주어집니다.

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
### 의도하지 않은 요청 방지하기

테스트 전체 또는 개별 테스트 내에서 HTTP 클라이언트를 통해 전송되는 모든 요청이 반드시 가짜로 처리되도록 보장하고 싶다면, `preventStrayRequests` 메서드를 호출하면 됩니다. 이 메서드를 호출한 후, 가짜 응답이 지정되지 않은 요청이 발생할 경우 실제 HTTP 요청이 실행되는 대신 예외가 발생합니다.

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

라라벨은 HTTP 요청을 보내는 과정에서 세 가지 이벤트를 발생시킵니다. 요청이 전송되기 전에 `RequestSending` 이벤트가, 특정 요청에 대해 응답을 받은 후에는 `ResponseReceived` 이벤트가 발생합니다. 요청에 대해 응답을 받지 못한 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 공개 `$request` 속성을 가집니다. 마찬가지로, `ResponseReceived` 이벤트에는 `$request`뿐만 아니라 `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있는 `$response` 속성도 포함되어 있습니다. 여러분의 애플리케이션에서 이 이벤트들을 위해 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트 처리 메서드
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```