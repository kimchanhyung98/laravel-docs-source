# HTTP 응답

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [세션 데이터를 플래시하며 리디렉션](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 여러 가지 다양한 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 방식은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 문자열을 자동으로 전체 HTTP 응답으로 변환합니다:

    Route::get('/', function () {
        return 'Hello World';
    });

라우트와 컨트롤러에서 문자열뿐만 아니라 배열을 반환할 수도 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

    Route::get('/', function () {
        return [1, 2, 3];
    });

> **참고**  
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)를 라우트나 컨트롤러에서 직접 반환할 수 있다는 사실, 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 사용해보세요!

<a name="response-objects"></a>
#### 응답 객체

대부분의 경우 라우트 액션에서 단순 문자열이나 배열만 반환하지 않습니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

`Response` 인스턴스를 전체로 반환하면 응답의 HTTP 상태 코드와 헤더를 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이는 HTTP 응답을 구성할 수 있는 다양한 메서드를 제공합니다:

    Route::get('/home', function () {
        return response('Hello World', 200)
                      ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/{{version}}/eloquent) 모델과 컬렉션도 라우트와 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환합니다. 이때 모델의 [hidden 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)은 제대로 처리됩니다:

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능하여 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용해 응답에 여러 헤더를 추가할 수 있습니다:

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');

혹은 `withHeaders` 메서드를 사용해 한 번에 여러 헤더를 배열로 지정할 수도 있습니다:

    return response($content)
                ->withHeaders([
                    'Content-Type' => $type,
                    'X-Header-One' => 'Header Value',
                    'X-Header-Two' => 'Header Value',
                ]);

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

Laravel에는 `cache.headers`라는 미들웨어가 포함되어 있어, 라우트 그룹에 대해 `Cache-Control` 헤더를 손쉽게 지정할 수 있습니다. 디렉티브는 해당 cache-control 디렉티브의 "스네이크 케이스"로 지정하며, 세미콜론(;)으로 구분해야 합니다. 만약 디렉티브 목록에 `etag`가 포함되어 있다면 응답 콘텐츠의 MD5 해시가 자동으로 ETag로 설정됩니다:

    Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
        Route::get('/privacy', function () {
            // ...
        });

        Route::get('/terms', function () {
            // ...
        });
    });

<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 추가하기

`cookie` 메서드를 사용하여 `Illuminate\Http\Response` 인스턴스에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효기간(분 단위)을 전달합니다:

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

`cookie` 메서드는 추가적으로 몇 가지 잘 사용되지 않는 인자를 더 받을 수 있습니다. 일반적으로 이 인자들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에 전달하는 인자와 동일한 의미를 갖습니다:

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

아직 응답 인스턴스가 없지만, 응답이 전송될 때 쿠키가 반드시 첨부되도록 하고 싶다면, `Cookie` 파사드를 사용해서 쿠키를 "큐"에 추가할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 만든 데 필요한 인자를 받으며, 이 쿠키들은 브라우저로 응답을 보내기 전에 자동으로 응답에 첨부됩니다:

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면, 글로벌 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부하지 않는 한 클라이언트로 전송되지 않습니다:

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### 쿠키 미리 만료시키기

응답의 `withoutCookie` 메서드를 이용하여 특정 쿠키를 만료시켜 제거할 수 있습니다:

    return response('Hello World')->withoutCookie('name');

응답 인스턴스가 아직 없는 경우, `Cookie` 파사드의 `expire` 메서드를 사용하여 쿠키를 만료시킬 수 있습니다:

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, Laravel이 생성하는 모든 쿠키는 암호화 및 서명되어 클라이언트에서 수정하거나 읽을 수 없습니다. 만약 애플리케이션에서 일부 쿠키에 대해서는 암호화를 비활성화하고 싶다면, `app/Http/Middleware` 디렉터리에 위치한 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 프로퍼티를 사용하면 됩니다:

    /**
     * 암호화되지 않을 쿠키의 이름.
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다:

    Route::get('/dashboard', function () {
        return redirect('home/dashboard');
    });

입력 폼이 유효하지 않을 때처럼 사용자를 원래 위치로 리디렉션시키고 싶을 때도 있습니다. 이럴 때는 글로벌 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 이용하므로, `back` 함수를 호출하는 라우트는 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

    Route::post('/user/profile', function () {
        // 요청 유효성 검사...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼를 매개변수 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 해당 인스턴스의 모든 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션하려면 `route` 메서드를 사용하면 됩니다:

    return redirect()->route('login');

만약 라우트에 매개변수가 있다면, 두 번째 인자로 전달하면 됩니다:

    // 해당 URI: /profile/{id} 인 경우

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 매개변수 채우기

"ID" 매개변수를 Eloquent 모델에서 추출해 값을 채워야 하는 라우트로 리디렉션할 경우, 모델 인스턴스를 바로 전달하면 됩니다. ID는 자동으로 추출됩니다:

    // 해당 URI: /profile/{id} 인 경우

    return redirect()->route('profile', [$user]);

라우트 파라미터에 들어갈 값을 커스터마이즈하고 싶다면, 라우트 파라미터 정의에 컬럼을 지정(`/profile/{id:slug}`)하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

    /**
     * 모델의 라우트 키 값을 반환합니다.
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/{{version}}/controllers)으로도 리디렉션할 수 있습니다. 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다:

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

컨트롤러 라우트에 매개변수가 필요하다면 두 번째 인자로 전달할 수 있습니다:

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

가끔 애플리케이션 외부의 도메인으로 리디렉션해야 할 때가 있습니다. 이럴 때는 `away` 메서드를 사용하면 추가적인 URL 인코딩이나 검증 없이 `RedirectResponse`가 생성됩니다:

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터를 플래시하며 리디렉션

새로운 URL로 리디렉션하면서 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 주로, 작업이 성공적으로 수행된 후 성공 메시지를 세션에 플래시할 때 사용됩니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성한 후 메서드 체이닝을 통해 세션 데이터도 플래시할 수 있습니다:

    Route::post('/user/profile', function () {
        // ...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

사용자가 리디렉션된 후 [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시하면 됩니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)으로도 다음과 같이 표시할 수 있습니다:

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### 입력값을 플래시하며 리디렉션

리디렉션 전 현재 요청의 입력 데이터를 세션에 플래시하려면, `RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용할 수 있습니다. 이는 유효성 검사 오류 발생 시 주로 사용됩니다. 입력값이 세션에 플래시되면, 다음 요청에서 [입력값을 쉽게 가져와](/docs/{{version}}/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다:

    return back()->withInput();

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 유형의 응답 인스턴스를 생성할 수 있습니다. 인자 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/{{version}}/contracts)의 구현 인스턴스가 반환됩니다. 이 계약은 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 제어해야 하면서, 동시에 [뷰](/docs/{{version}}/views)를 응답 본문으로 반환해야 한다면, `view` 메서드를 사용하세요:

    return response()
                ->view('hello', $data, 200)
                ->header('Content-Type', $type);

특별한 HTTP 상태 코드나 헤더가 필요 없다면, 글로벌 `view` 헬퍼 함수를 사용하면 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하며, 전달된 배열을 PHP의 `json_encode` 함수로 JSON으로 변환합니다:

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

JSONP 응답을 만들려면, `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다:

    return response()
                ->json(['name' => 'Abigail', 'state' => 'CA'])
                ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자의 브라우저에서 다운로드하도록 강제하는 응답을 생성합니다. 이때 두 번째 인자로 파일명을 지정하면 사용자가 다운로드할 때 파일명으로 보입니다. 마지막 인자에는 HTTP 헤더 배열을 전달할 수 있습니다:

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> **경고**  
> 파일 다운로드를 담당하는 Symfony HttpFoundation은, 다운로드하는 파일의 파일명이 ASCII로 되어 있어야 함을 요구합니다.

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

특정 작업의 문자열 형태 결과를 디스크에 저장하지 않고 곧바로 다운로드 응답으로 변환하고 싶을 때는 `streamDownload` 메서드를 사용하세요. 이 메서드는 콜백, 파일명, 선택적 헤더 배열을 인자로 받습니다:

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
                    ->contents()
                    ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF 등 파일을 다운로드하지 않고, 사용자의 브라우저에서 바로 표시하도록 응답을 반환합니다. 첫 번째 인자는 파일의 경로이고, 두 번째 인자는 헤더의 배열입니다:

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="response-macros"></a>
## 응답 매크로

여러 라우트 및 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하려면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출합니다. 예를 들어, `App\Providers\AppServiceProvider`에서 사용하면 됩니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            Response::macro('caps', function ($value) {
                return Response::make(strtoupper($value));
            });
        }
    }

`macro` 함수의 첫 번째 인자는 이름, 두 번째 인자는 클로저입니다. 매크로 이름을 `ResponseFactory` 구현이나 `response` 헬퍼로 호출하면 등록된 클로저가 실행됩니다:

    return response()->caps('foo');
