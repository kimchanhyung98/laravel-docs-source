# HTTP 응답

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션](#redirects)
    - [이름이 지정된 라우트로 리디렉션](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리디렉션](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트 및 컨트롤러는 사용자 브라우저로 반환할 응답을 제공해야 합니다. 라라벨은 여러 가지 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 해당 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

    Route::get('/', function () {
        return 'Hello World';
    });

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON응답으로 변환합니다.

    Route::get('/', function () {
        return [1, 2, 3];
    });

> [!NOTE]  
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)도 라우트나 컨트롤러에서 반환할 수 있다는 사실, 알고 계셨나요? 이들도 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서는 단순 문자열이나 배열만을 반환하지 않습니다. 대신, `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

`Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드 및 헤더를 직접 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답 생성을 위한 다양한 메서드를 제공합니다.

    Route::get('/home', function () {
        return response('Hello World', 200)
                      ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/{{version}}/eloquent) 모델과 컬렉션도 라우트 및 컨트롤러에서 직접 반환할 수 있습니다. 이 경우, 라라벨은 모델의 [히든 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 반영하여, 자동으로 JSON 응답으로 변환합니다.

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝(chaining)이 가능하므로, 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, `header` 메서드를 사용하여 응답에 여러 헤더를 추가할 수 있습니다.

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');

혹은, `withHeaders` 메서드를 사용해 배열 형태로 여러 헤더를 한 번에 지정할 수도 있습니다.

    return response($content)
                ->withHeaders([
                    'Content-Type' => $type,
                    'X-Header-One' => 'Header Value',
                    'X-Header-Two' => 'Header Value',
                ]);

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

라라벨은 `cache.headers` 미들웨어를 제공하며, 여러 라우트에 `Cache-Control` 헤더를 쉽게 지정할 수 있습니다. 각 디렉티브는 해당 cache-control 디렉티브의 snake_case 버전을 세미콜론으로 구분해 전달합니다. `etag`가 지정된 경우, 응답 내용의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

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

`cookie` 메서드를 이용해 `Illuminate\Http\Response` 인스턴스에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키명, 값, 유효기간(분)을 전달해야 합니다.

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

`cookie` 메서드는 추가로 몇 가지 인자를 더 받을 수 있습니다. 이들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수의 인자와 동일한 목적과 의미를 갖습니다.

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

응답 인스턴스가 아직 없는 경우, `Cookie` 파사드를 이용해 쿠키를 "대기열에 추가"할 수 있습니다. 이 쿠키들은 실제 응답이 전송되기 직전 자동으로 첨부됩니다.

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 전역 `cookie` 헬퍼로 생성할 수 있습니다. 이 쿠키는 응답에 첨부되기 전까지는 클라이언트에 전송되지 않습니다.

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### 쿠키 미리 만료시키기

응답의 `withoutCookie` 메서드로 쿠키를 미리 만료시켜 제거할 수 있습니다.

    return response('Hello World')->withoutCookie('name');

아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용할 수 있습니다.

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 라라벨이 생성하는 모든 쿠키는 암호화되고 서명되어, 클라이언트가 임의로 읽거나 수정할 수 없습니다. 만약 애플리케이션에서 생성하는 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, `app/Http/Middleware` 디렉터리에 위치한 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 프로퍼티를 사용하면 됩니다.

    /**
     * 암호화에서 제외할 쿠키 이름
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키기 위한 적절한 헤더를 포함합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

    Route::get('/dashboard', function () {
        return redirect('home/dashboard');
    });

입력값이 유효하지 않을 때 등, 사용자를 이전 위치로 리디렉트하고 싶을 수 있습니다. 이 경우 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 활용하므로, `back` 함수를 호출하는 라우트는 반드시 `web` 미들웨어 그룹을 사용해야 합니다.

    Route::post('/user/profile', function () {
        // 요청 검증...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션

`redirect` 헬퍼를 인자 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스를 반환하므로, 이 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, `route` 메서드로 이름이 지정된 라우트로 리디렉트할 수 있습니다.

    return redirect()->route('login');

라우트에 파라미터가 있다면 두 번째 인자로 전달하면 됩니다.

    // 해당 URI: /profile/{id}

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 지정

ID 파라미터가 Eloquent 모델로 채워지는 라우트로 리디렉트할 경우, 모델 인스턴스 자체를 전달하면 됩니다. ID는 자동으로 추출됩니다.

    // 해당 URI: /profile/{id}

    return redirect()->route('profile', [$user]);

라우트 파라미터로 실제 전달되는 값을 커스터마이즈하고 싶다면, 라우트 파라미터 정의에서 컬럼(`/profile/{id:slug}`)을 지정하거나, 모델에서 `getRouteKey` 메서드를 오버라이드할 수도 있습니다.

    /**
     * 모델 라우트 키 값 반환
     */
    public function getRouteKey(): mixed
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리디렉션하려면, 컨트롤러와 액션명을 `action` 메서드로 전달하면 됩니다.

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인자로 파라미터 배열을 넘기면 됩니다.

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

때로는 애플리케이션 외부의 도메인으로 리디렉션해야 할 수도 있습니다. 이 경우 `away` 메서드를 호출하면 추가적인 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성합니다.

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션

새로운 URL로 리디렉트하면서 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 보통 어떤 동작이 성공적으로 처리된 후에 성공 메시지를 세션에 플래시한 다음 리디렉트합니다. 편의상, 하나의 체이닝 메서드로 `RedirectResponse` 인스턴스 생성과 세션 데이터 플래시를 동시에 할 수 있습니다.

    Route::post('/user/profile', function () {
        // ...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

사용자가 리디렉트된 후, [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)을 사용하면 다음과 같습니다.

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션

`RedirectResponse` 인스턴스의 `withInput` 메서드를 이용하면 현재 요청의 입력 데이터를 플래시한 뒤 사용자에게 새로운 위치로 리디렉트할 수 있습니다. 이는 주로 사용자가 유효성 검증 오류를 경험했을 때 사용됩니다. 입력값이 세션에 저장되면, 다음 요청에서 [이전 입력값을 쉽게 조회](/docs/{{version}}/requests#retrieving-old-input)하여 폼을 다시 채울 수 있습니다.

    return back()->withInput();

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼는 다양한 유형의 응답 인스턴스를 생성할 때 사용할 수 있습니다. 인자가 없을 때 `response` 헬퍼를 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/{{version}}/contracts)의 구현을 반환합니다. 이 컨트랙트는 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 제어하면서, 동시에 [뷰](/docs/{{version}}/views)를 응답 내용으로 반환하려면 `view` 메서드를 사용하면 됩니다.

    return response()
                ->view('hello', $data, 200)
                ->header('Content-Type', $type);

커스텀 HTTP 상태 코드나 헤더가 필요 없다면, 전역 `view` 헬퍼 함수를 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 자동으로 `Content-Type` 헤더를 `application/json`으로 설정하고, 주어진 배열을 PHP의 `json_encode`로 변환합니다.

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

JSONP 응답이 필요하다면, `json`과 `withCallback` 메서드를 함께 사용할 수 있습니다.

    return response()
                ->json(['name' => 'Abigail', 'state' => 'CA'])
                ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면 사용자의 브라우저가 지정한 경로의 파일을 다운로드하도록 강제할 수 있습니다. 두 번째 인자에 파일명을 지정하면, 다운로드 시 사용자에게 보여질 이름이 변경됩니다. 세 번째 인자에는 HTTP 헤더 배열을 전달할 수 있습니다.

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> [!WARNING]  
> 파일 다운로드를 담당하는 Symfony HttpFoundation은 다운로드되는 파일명이 ASCII 문자여야 함을 요구합니다.

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

어떤 작업의 응답 문자열을 파일로 저장하지 않고 바로 다운로드 응답으로 제공하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 옵션으로 헤더 배열을 인자로 받습니다.

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
                    ->contents()
                    ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면 이미지를 비롯한 파일(PDF 등)을 다운로드가 아닌 브라우저 내에서 바로 표시할 수 있습니다. 첫 번째 인자로 파일의 절대 경로, 두 번째 인자로 헤더 배열을 전달합니다.

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="response-macros"></a>
## 응답 매크로

여러 라우트나 컨트롤러에서 반복적으로 사용할 커스텀 응답을 정의하려면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드(예: `App\Providers\AppServiceProvider`)에서 이 메서드를 호출합니다.

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            Response::macro('caps', function (string $value) {
                return Response::make(strtoupper($value));
            });
        }
    }

`macro` 함수는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받습니다. 매크로 이름을 `ResponseFactory` 구현 또는 `response` 헬퍼에서 호출할 때 해당 클로저가 실행됩니다.

    return response()->caps('foo');
