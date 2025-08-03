# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [오류 처리](#error-handling)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 위조(faking)](#faking-responses)
    - [요청 검사](#inspecting-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 표현력 있는 최소한의 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위해 빠르게 HTTP 요청을 보낼 수 있게 해줍니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례에 초점을 맞추고 뛰어난 개발자 경험을 제공합니다.

시작하기 전에, 애플리케이션의 의존성으로 Guzzle 패키지가 설치되어 있는지 확인해야 합니다. 기본적으로 Laravel은 이 의존성을 자동으로 포함합니다. 하지만 이전에 패키지를 제거했다면, Composer를 통해 다시 설치할 수 있습니다:

```
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
## 요청 만들기 (Making Requests)

요청을 만들 때 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 간단한 `GET` 요청을 하는 방법을 살펴보겠습니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이 객체는 응답을 검사할 때 사용할 수 있는 다양한 메서드를 제공합니다:

```
$response->body() : string;
$response->json($key = null) : array|mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->status() : int;
$response->ok() : bool;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->serverError() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

또한 `Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스를 구현하여, 응답의 JSON 데이터를 배열처럼 직접 접근할 수 있습니다:

```
return Http::get('http://example.com/users/1')['name'];
```

<a name="dumping-requests"></a>
#### 요청 덤프하기 (Dumping Requests)

발신되는 요청 인스턴스를 전송 전에 덤프하고 스크립트 실행을 중단하고 싶다면, 요청 정의 시작 부분에 `dd` 메서드를 추가할 수 있습니다:

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

일반적으로 `POST`, `PUT`, `PATCH` 요청을 할 때 추가 데이터를 같이 보내므로, 이들 메서드는 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 매개변수

`GET` 요청 시 URL에 직접 쿼리 문자열을 붙이거나, `get` 메서드의 두 번째 인수로 키/값 쌍 배열을 전달할 수 있습니다:

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 전송하고 싶다면, 요청하기 전에 `asForm` 메서드를 호출해야 합니다:

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청 시 원시 요청 본문을 직접 제공하고 싶으면 `withBody` 메서드를 사용할 수 있습니다. 이 메서드의 두 번째 인수로 콘텐츠 타입을 지정할 수 있습니다:

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청 (Multi-Part Requests)

파일을 멀티파트 요청으로 보내려면, 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일 이름과 파일 내용을 인수로 받습니다. 필요하다면 세 번째 인수로 파일 이름을 명시할 수 있습니다:

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
)->post('http://example.com/attachments');
```

파일의 원시 내용을 전달하는 대신 스트림 리소스를 전달할 수도 있습니다:

```
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키/값 쌍 배열을 인수로 받습니다:

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용해 요청에 대한 응답으로 기대하는 콘텐츠 타입을 지정할 수 있습니다:

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

더 간편하게, 요청이 `application/json` 콘텐츠 타입을 기대한다고 빠르게 지정하고 싶으면 `acceptJson` 메서드를 사용할 수 있습니다:

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<a name="authentication"></a>
### 인증 (Authentication)

기본 인증과 다이제스트 인증 자격 증명은 각각 `withBasicAuth` 및 `withDigestAuth` 메서드를 사용해 지정할 수 있습니다:

```
// 기본 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(...);

// 다이제스트 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(...);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰 (Bearer Tokens)

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하고 싶다면 `withToken` 메서드를 사용할 수 있습니다:

```
$response = Http::withToken('token')->post(...);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

응답 대기 최대 시간을 초 단위로 지정하려면 `timeout` 메서드를 사용하세요:

```
$response = Http::timeout(3)->get(...);
```

지정한 타임아웃 시간을 초과하면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면 `retry` 메서드를 사용하세요. 이 메서드는 재시도 최대 횟수와 재시도 사이 대기 시간(밀리초 단위)을 받습니다:

```
$response = Http::retry(3, 100)->post(...);
```

필요하다면 `retry` 메서드에 세 번째 인수로 재시도 여부를 결정하는 콜백을 전달할 수 있습니다. 예를 들어 최초 요청이 `ConnectionException` 예외를 만났을 때만 재시도하도록 할 수 있습니다:

```
$response = Http::retry(3, 100, function ($exception) {
    return $exception instanceof ConnectionException;
})->post(...);
```

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다.

<a name="error-handling"></a>
### 오류 처리 (Error Handling)

Guzzle 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트나 서버 오류 (`400` 및 `500`대 응답)에서 예외를 던지지 않습니다. 대신 `successful`, `clientError`, `serverError` 메서드를 사용해 이러한 오류가 발생했는지 확인할 수 있습니다:

```
// 상태 코드가 200 이상 300 미만인지 확인...
$response->successful();

// 상태 코드가 400 이상인지 확인...
$response->failed();

// 400대 상태 코드인지 확인...
$response->clientError();

// 500대 상태 코드인지 확인...
$response->serverError();

// 클라이언트 또는 서버 오류가 있었을 때 즉시 콜백 실행...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스가 있고, 응답 상태 코드가 클라이언트 또는 서버 오류일 경우 `Illuminate\Http\Client\RequestException` 예외를 던지고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```
$response = Http::post(...);

// 클라이언트 또는 서버 오류가 있었다면 예외 던지기...
$response->throw();

// 오류가 발생했고 주어진 조건이 참이면 예외 던지기...
$response->throwIf($condition);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스는 공개 `$response` 속성을 갖고 있어, 반환된 응답을 검사할 수 있습니다.

`throw` 메서드는 오류가 없을 때 응답 인스턴스를 반환해서, `throw` 메서드 체이닝을 허용합니다:

```
return Http::post(...)->throw()->json();
```

예외를 던지기 전에 추가 로직을 실행하려면, `throw` 메서드에 클로저를 넘길 수 있습니다. 클로저 호출 후 예외가 자동으로 던져지므로, 클로저 내부에서 다시 예외를 던질 필요는 없습니다:

```
return Http::post(...)->throw(function ($response, $e) {
    //
})->json();
```

<a name="guzzle-options"></a>
### Guzzle 옵션 (Guzzle Options)

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정하고 싶으면 `withOptions` 메서드를 사용하세요. 이 메서드는 키/값 쌍 배열을 받습니다:

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
## 동시 요청 (Concurrent Requests)

때때로 여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 요청들을 순차적으로 보내는 대신 한꺼번에 여러 요청을 발송하여 응답을 기다리는 것을 의미합니다. 이는 느린 HTTP API와 상호작용할 때 상당한 성능 향상을 가져올 수 있습니다.

Laravel에서는 `pool` 메서드를 사용해 이를 쉽게 구현할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받아, 요청 풀에 요청들을 추가해 동시에 발송하도록 합니다:

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

보시다시피, 각 응답은 풀에 추가된 순서대로 배열을 통해 접근할 수 있습니다. 요청에 이름을 지정하고 싶다면 `as` 메서드를 사용하세요. 그러면 이름으로 응답에 접근할 수 있습니다:

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

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있게 하여, 애플리케이션 전반에서 여러 서비스와 상호작용할 때 공통 요청 경로나 헤더를 구성하는 데 유창하고 표현력 있는 방법을 제공합니다. 시작하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 매크로를 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

매크로가 구성되면 애플리케이션 어디서든 호출하여 지정한 설정으로 대기 중인 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스들이 테스트를 쉽게 작성할 수 있도록 기능을 제공하며, HTTP 래퍼도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드는 요청이 발생할 때 스텁 또는 더미 응답을 반환하도록 HTTP 클라이언트를 지시할 수 있게 해줍니다.

<a name="faking-responses"></a>
### 응답 위조(faking) (Faking Responses)

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하도록 HTTP 클라이언트에 지시하려면 `fake` 메서드를 인수 없이 호출합니다:

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(...);
```

> [!NOTE]
> 응답 위조 시 HTTP 클라이언트 미들웨어는 실행되지 않습니다. 따라서 위조된 응답에 대한 기대를 정의할 때 해당 미들웨어들이 정상 실행된 경우처럼 가정해야 합니다.

<a name="faking-specific-urls"></a>
#### 특정 URL 위조하기

대신 `fake` 메서드에 배열을 전달할 수 있습니다. 이 배열의 키는 위조하고자 하는 URL 패턴이며, 값은 해당 URL에 대해 반환할 응답입니다. 와일드카드 `*` 문자를 사용할 수 있습니다. 위조되지 않은 URL에 대한 요청은 실제로 실행됩니다. `Http` 파사드의 `response` 메서드를 사용해 스텁(더미) 응답을 만들 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 스텁 생성...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대해 문자열 응답 스텁 생성...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

위조되지 않은 모든 URL에 대해 기본 응답을 지정하고 싶으면 단일 `*` 문자로 와일드카드 패턴을 사용할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대해 JSON 응답 스텁 생성...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 그 외 모든 엔드포인트에 대해 문자열 응답 스텁 생성...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 위조하기

단일 URL이 특정 순서대로 여러 위조 응답을 반환하도록 지정해야 할 때가 있습니다. `Http::sequence` 메서드를 사용해 이를 구성할 수 있습니다:

```
Http::fake([
    // GitHub 엔드포인트에 대해 일련의 응답 스텁 생성...
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->pushStatus(404),
]);
```

시퀀스 내 모든 응답이 소진되면 추가 요청 시 예외가 발생합니다. 시퀀스가 비어있을 때 반환할 기본 응답을 지정하고 싶으면 `whenEmpty` 메서드를 사용하세요:

```
Http::fake([
    // GitHub 엔드포인트에 대해 일련의 응답 스텁 생성...
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->whenEmpty(Http::response()),
]);
```

특정 URL 패턴 위조가 필요 없고 응답 시퀀스만 위조하고 싶다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 위조 콜백 (Fake Callback)

특정 엔드포인트에 반환할 응답을 더 복잡한 로직으로 결정해야 한다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아, 반환할 응답 인스턴스를 반환해야 합니다:

```
Http::fake(function ($request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사 (Inspecting Requests)

응답을 위조하는 중간에, 애플리케이션이 올바른 데이터나 헤더를 전송하는지 요청을 검사하고 싶을 수 있습니다. 이때 `Http::fake` 호출 이후에 `Http::assertSent` 메서드를 사용하면 됩니다.

`assertSent` 메서드는 요청이 기대에 부합하는지 검사하는 클로저를 받으며, 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받아 불리언 값을 반환해야 합니다. 테스트가 통과하려면 적어도 하나 이상의 요청이 이 조건에 부합해야 합니다:

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

필요하면 특정 요청이 전송되지 않았음을 검증하는 `assertNotSent` 메서드도 사용할 수 있습니다:

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

테스트 중에 전송된 요청 수를 검사할 때는 `assertSentCount` 메서드를 사용할 수 있습니다:

```
Http::fake();

Http::assertSentCount(5);
```

아예 요청이 전송되지 않았음을 확인할 때는 `assertNothingSent` 메서드를 사용합니다:

```
Http::fake();

Http::assertNothingSent();
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청 과정을 처리하는 동안 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청을 보내기 직전에 발생하며, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 후 발생합니다. 그리고 `ConnectionFailed` 이벤트는 특정 요청에 대해 응답을 받지 못했을 때 발생합니다.

`RequestSending`과 `ConnectionFailed` 이벤트 둘 다 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있는 공개 `$request` 속성을 갖고 있습니다. 마찬가지로, `ResponseReceived` 이벤트는 요청 인스턴스뿐 아니라 응답 인스턴스를 검사할 수 있는 `$response` 공개 속성도 포함합니다. 이 이벤트에 대한 리스너는 `App\Providers\EventServiceProvider` 서비스 프로바이더 내에서 등록할 수 있습니다:

```
/**
 * 애플리케이션의 이벤트 리스너 매핑입니다.
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