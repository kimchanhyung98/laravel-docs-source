# HTTP 클라이언트

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [에러 핸들링](#error-handling)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 모킹(Faking Responses)](#faking-responses)
    - [요청 검사](#inspecting-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 하는 간결하고 직관적인 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 신속하게 보낼 수 있게 해줍니다. Laravel의 Guzzle 래퍼는 개발자 경험과 자주 쓰는 사용 사례에 집중하여 구현되어 있습니다.

시작하기 전에, 애플리케이션의 의존성에 Guzzle 패키지가 설치되어 있는지 확인해야 합니다. 기본적으로 Laravel은 이 의존성을 자동으로 포함합니다. 그러나 이전에 패키지를 제거한 경우, Composer를 통해 다시 설치할 수 있습니다:

    composer require guzzlehttp/guzzle

<a name="making-requests"></a>
## 요청 보내기

요청을 보내려면 `Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 알아봅시다:

    use Illuminate\Support\Facades\Http;

    $response = Http::get('http://example.com');

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다양한 메서드를 통해 응답을 확인할 수 있습니다:

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, JSON 응답 데이터를 응답 객체에서 바로 접근할 수 있습니다:

    return Http::get('http://example.com/users/1')['name'];

<a name="dumping-requests"></a>
#### 요청 출력(Dump)

전송 전에 발신 요청 인스턴스를 출력하고 스크립트 실행을 중단하려면 요청 정의의 앞에 `dd` 메서드를 추가하면 됩니다:

    return Http::dd()->get('http://example.com');

<a name="request-data"></a>
### 요청 데이터

`POST`, `PUT`, `PATCH` 요청 시 추가 데이터를 함께 보내는 것이 일반적이며, 이 메서드들은 두 번째 인자로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다:

    use Illuminate\Support\Facades\Http;

    $response = Http::post('http://example.com/users', [
        'name' => 'Steve',
        'role' => 'Network Administrator',
    ]);

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때는 URL에 쿼리 문자열을 직접 추가하거나, 두 번째 인자로 키/값 쌍 배열을 전달할 수 있습니다:

    $response = Http::get('http://example.com/users', [
        'name' => 'Taylor',
        'page' => 1,
    ]);

<a name="sending-form-url-encoded-requests"></a>
#### Form URL 인코딩 방식 데이터 전송

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출하면 됩니다:

    $response = Http::asForm()->post('http://example.com/users', [
        'name' => 'Sara',
        'role' => 'Privacy Consultant',
    ]);

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 전송

요청 시 raw 데이터를 본문으로 보낼 경우 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인자로 콘텐츠 타입을 지정할 수 있습니다:

    $response = Http::withBody(
        base64_encode($photo), 'image/jpeg'
    )->post('http://example.com/photo');

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 보내고 싶다면, 요청 전에 `attach` 메서드를 이용합니다. 이 메서드는 파일명과 파일 내용을 인자로 받으며, 필요하다면 세 번째 인자로 실제 파일명을 지정할 수 있습니다:

    $response = Http::attach(
        'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
    )->post('http://example.com/attachments');

파일의 raw 데이터를 전달하는 대신, 스트림 리소스를 전달할 수도 있습니다:

    $photo = fopen('photo.jpg', 'r');

    $response = Http::attach(
        'attachment', $photo, 'photo.jpg'
    )->post('http://example.com/attachments');

<a name="headers"></a>
### 헤더

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 메서드는 키/값 쌍 배열을 받습니다:

    $response = Http::withHeaders([
        'X-First' => 'foo',
        'X-Second' => 'bar'
    ])->post('http://example.com/users', [
        'name' => 'Taylor',
    ]);

요청에 대한 응답으로 어떤 콘텐츠 타입을 기대하는지 `accept` 메서드를 통해 지정할 수 있습니다:

    $response = Http::accept('application/json')->get('http://example.com/users');

`application/json` 콘텐츠 타입을 응답으로 기대할 때는 더 간편하게 `acceptJson` 메서드를 사용할 수 있습니다:

    $response = Http::acceptJson()->get('http://example.com/users');

<a name="authentication"></a>
### 인증

기본 인증(Basic)과 다이제스트 인증(Digest)은 각각 `withBasicAuth`와 `withDigestAuth` 메서드로 지정할 수 있습니다:

    // 기본 인증...
    $response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(...);

    // 다이제스트 인증...
    $response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(...);

<a name="bearer-tokens"></a>
#### Bearer 토큰

Bearer 토큰을 Authorization 헤더에 빠르게 추가하려면 `withToken` 메서드를 사용할 수 있습니다:

    $response = Http::withToken('token')->post(...);

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드를 사용해 응답을 기다릴 최대 초 단위를 지정할 수 있습니다:

    $response = Http::timeout(3)->get(...);

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 에러가 발생할 때 HTTP 클라이언트가 요청을 자동으로 재시도하게 하려면 `retry` 메서드를 사용할 수 있습니다. 이 메서드는 요청 시도 최대 횟수와 각 시도 사이 대기할 밀리초(ms) 단위를 인자로 받습니다:

    $response = Http::retry(3, 100)->post(...);

필요하다면 세 번째 인자로 호출 가능 객체(callable)를 전달할 수 있습니다. 예를 들어, 첫 번째 요청이 `ConnectionException`이 발생한 경우에만 재시도를 실행하도록 지정할 수 있습니다:

    $response = Http::retry(3, 100, function ($exception) {
        return $exception instanceof ConnectionException;
    })->post(...);

모든 요청이 실패할 경우, `Illuminate\Http\Client\RequestException` 예외가 발생합니다.

<a name="error-handling"></a>
### 에러 핸들링

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 에러(서버에서의 `400`, `500` 레벨 응답)시 예외를 던지지 않습니다. 이런 에러가 반환되었는지는 `successful`, `clientError`, `serverError` 메서드를 사용해 확인할 수 있습니다:

    // 상태 코드가 >= 200 이고 < 300인지 확인...
    $response->successful();

    // 상태 코드가 >= 400 인지 확인...
    $response->failed();

    // 400 번대 에러인지 확인...
    $response->clientError();

    // 500 번대 에러인지 확인...
    $response->serverError();

    // 클라이언트 또는 서버 에러 발생 시 즉시 콜백 실행...
    $response->onError(callable $callback);

<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스를 가지고 있고, 응답 상태 코드가 클라이언트 또는 서버 에러를 나타내면 `Illuminate\Http\Client\RequestException` 예외를 던지게 하려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

    $response = Http::post(...);

    // 클라이언트 또는 서버 에러 발생 시 예외를 던짐
    $response->throw();

    // 조건이 참이고 에러가 발생했다면 예외를 던짐
    $response->throwIf($condition);

    return $response['user']['id'];

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있는 공개 `$response` 프로퍼티가 있습니다.

에러가 없으면 `throw` 메서드는 응답 인스턴스를 반환하므로, `throw` 이후 다른 연산을 체이닝할 수 있습니다:

    return Http::post(...)->throw()->json();

예외가 발생하기 전 추가 작업을 하고 싶다면, `throw` 메서드에 클로저를 넘길 수 있습니다. 클로저가 실행된 후 예외는 자동으로 던져집니다:

    return Http::post(...)->throw(function ($response, $e) {
        //
    })->json();

<a name="guzzle-options"></a>
### Guzzle 옵션

추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)은 `withOptions` 메서드를 통해 지정할 수 있습니다. 이 메서드는 키/값 쌍 배열을 받습니다:

    $response = Http::withOptions([
        'debug' => true,
    ])->get('http://example.com/users');

<a name="concurrent-requests"></a>
## 동시 요청

여러 HTTP 요청을 동시에(=동시성으로) 처리하고 싶을 때도 있습니다. 즉, 여러 요청을 차례로 보내는 대신, 한 번에 즉시 실행하는 방식으로 성능을 크게 개선할 수 있습니다.

이때는 `pool` 메서드를 활용하면 됩니다. 이 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인자로 받아, 요청 풀에 요청을 쉽게 추가할 수 있습니다:

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

위 예시처럼, 각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 원한다면 `as` 메서드로 각 요청에 이름을 부여하여, 이름으로도 결과를 참조할 수 있습니다:

    use Illuminate\Http\Client\Pool;
    use Illuminate\Support\Facades\Http;

    $responses = Http::pool(fn (Pool $pool) => [
        $pool->as('first')->get('http://localhost/first'),
        $pool->as('second')->get('http://localhost/second'),
        $pool->as('third')->get('http://localhost/third'),
    ]);

    return $responses['first']->ok();

<a name="macros"></a>
## 매크로

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있게 해주어, 서비스와의 반복적 통신에서 자주 사용하는 요청 경로와 헤더를 유창하게 구성할 수 있습니다. 예를 들어, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에 매크로를 정의할 수 있습니다:

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

매크로를 구성한 후에는 애플리케이션 어디서든 해당 매크로를 호출해 지정한 구성이 적용된 대기 요청 인스턴스를 만들 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트

Laravel의 여러 기능이 쉽고 직관적으로 테스트를 작성할 수 있도록 지원하는 것처럼, HTTP 래퍼도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드는 HTTP 요청시 더미(Stub)/모킹(Mock) 응답을 반환하도록 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 모킹(Faking Responses)

예를 들어, 모든 요청에 대해 빈 200 응답을 반환하도록 하려면 인자 없이 `fake` 메서드를 호출하면 됩니다:

    use Illuminate\Support\Facades\Http;

    Http::fake();

    $response = Http::post(...);

> {note} 요청을 모킹할 때, HTTP 클라이언트 미들웨어는 실행되지 않습니다. 모킹된 응답에 대한 예상은 미들웨어가 정상적으로 실행된 것으로 간주하여 테스트해야 합니다.

<a name="faking-specific-urls"></a>
#### 특정 URL 모킹

배열을 `fake` 메서드에 전달해 특정 URL 패턴만 모킹할 수도 있습니다. 배열의 키는 모킹할 URL 패턴이고, 값은 반환할 응답입니다. `*` 문자로 와일드카드 패턴을 지정할 수 있습니다. 지정하지 않은 URL로 요청할 경우 실제 요청이 전송됩니다. HTTP 파사드의 `response` 메서드를 이용해 스텁/모킹 응답을 만들 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트 JSON 응답 스텁...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

        // Google 엔드포인트 문자열 응답 스텁...
        'google.com/*' => Http::response('Hello World', 200, $headers),
    ]);

모든 매칭되지 않은 URL에 대한 기본 스텁을 지정하려면 `*` 를 사용할 수 있습니다:

    Http::fake([
        // GitHub 엔드포인트 JSON 응답 스텁...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

        // 기타 모든 엔드포인트 문자열 응답 스텁...
        '*' => Http::response('Hello World', 200, ['Headers']),
    ]);

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 모킹

가끔 한 URL이 여러 번 요청될 때, 순차적으로 다양한 응답을 반환하도록 해야 할 수 있습니다. 이 경우 `Http::sequence` 메서드를 활용하면 됩니다:

    Http::fake([
        // GitHub 엔드포인트 시퀀스 응답 스텁...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->pushStatus(404),
    ]);

응답 시퀀스를 모두 소진하면, 이후의 추가 요청은 예외가 발생합니다. 빈 시퀀스일 때 반환할 기본 응답을 지정하고 싶다면 `whenEmpty` 메서드를 사용하세요:

    Http::fake([
        // GitHub 엔드포인트 시퀀스 응답 스텁...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->whenEmpty(Http::response()),
    ]);

특정 URL 패턴 없이 응답 시퀀스를 모킹하려면 `Http::fakeSequence`를 사용할 수 있습니다:

    Http::fakeSequence()
            ->push('Hello World', 200)
            ->whenEmpty(Http::response());

<a name="fake-callback"></a>
#### Fake 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 더 복잡한 로직이 필요하다면, 함수를 `fake` 메서드에 넘길 수 있습니다. 이 함수는 `Illuminate\Http\Client\Request` 인스턴스를 받아, 반환할 응답 인스턴스를 반환해야 합니다. 함수 내에서 다양한 로직을 구현할 수 있습니다:

    Http::fake(function ($request) {
        return Http::response('Hello World', 200);
    });

<a name="inspecting-requests"></a>
### 요청 검사

응답을 모킹할 때, 클라이언트가 올바른 데이터 또는 헤더를 보내는지 요청을 검사하고 싶을 때가 있습니다. 이럴 때는 `Http::fake` 이후 `Http::assertSent` 메서드를 호출하면 됩니다.

`assertSent`는 클로저를 받아 `Illuminate\Http\Client\Request` 인스턴스를 인자로 전달하며, 요청이 조건에 부합하면 true를 반환해야 합니다. 테스트가 통과하려면 조건에 맞는 요청이 한 번 이상 전송되어야 합니다:

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

특정 요청이 전송되지 않았는지 검사하고 싶다면 `assertNotSent` 메서드를 사용할 수 있습니다:

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

`assertSentCount` 메서드로 테스트 중 몇 건의 요청이 "전송"되었는지 검사할 수 있습니다:

    Http::fake();

    Http::assertSentCount(5);

또는 `assertNothingSent`로 테스트 중 어떠한 요청도 전송되지 않았는지 검사할 수 있습니다:

    Http::fake();

    Http::assertNothingSent();

<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청 처리 과정에서 세 가지 이벤트를 발생시킵니다. 요청 전에는 `RequestSending` 이벤트가 발생하며, 요청에 대한 응답이 도착하면 `ResponseReceived` 이벤트가 발생합니다. 응답을 받지 못한 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`와 `ConnectionFailed` 이벤트에는 모두 `$request` 프로퍼티가 있어, `Illuminate\Http\Client\Request` 인스턴스를 참고할 수 있습니다. `ResponseReceived` 이벤트에는 `$request`와 `$response` 프로퍼티가 모두 있어, 두 객체를 모두 검사할 수 있습니다. 이 이벤트들은 `App\Providers\EventServiceProvider` 서비스 프로바이더에 다음과 같이 리스너를 등록해 사용할 수 있습니다:

    /**
     * 애플리케이션의 이벤트-리스너 매핑.
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