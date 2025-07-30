# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트하기](#redirecting-external-domains)
    - [세션 플래시 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열 (Strings & Arrays)

모든 라우트와 컨트롤러는 사용자의 브라우저로 전송할 응답을 반환해야 합니다. Laravel은 응답을 반환하는 여러 가지 방법을 제공합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크가 자동으로 문자열을 완전한 HTTP 응답으로 변환합니다:

```
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트 또는 컨트롤러에서 [Eloquent 컬렉션](/docs/9.x/eloquent-collections)을 반환할 수도 있다는 것을 알고 계셨나요? 컬렉션도 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체 (Response Objects)

일반적으로 라우트 액션에서 단순 문자열이나 배열만 반환하지는 않습니다. 대신에 보통 `Illuminate\Http\Response` 인스턴스 또는 [뷰](/docs/9.x/views)를 반환합니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 사용자 정의할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, HTTP 응답을 구성하는 다양한 메서드를 제공합니다:

```
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션 (Eloquent Models & Collections)

라우트나 컨트롤러에서 [Eloquent ORM](/docs/9.x/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 이 경우 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/9.x/eloquent-serialization#hiding-attributes-from-json)을 존중합니다:

```
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기 (Attaching Headers To Responses)

대부분의 응답 메서드는 체이닝이 가능하여 유연하게 응답 인스턴스를 구성할 수 있음을 기억하세요. 예를 들어, `header` 메서드를 사용해 응답에 여러 헤더를 추가한 뒤 사용자의 브라우저에 응답을 전송할 수 있습니다:

```
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용하여 응답에 추가할 헤더 배열을 지정할 수도 있습니다:

```
return response($content)
            ->withHeaders([
                'Content-Type' => $type,
                'X-Header-One' => 'Header Value',
                'X-Header-Two' => 'Header Value',
            ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어 (Cache Control Middleware)

Laravel은 `cache.headers` 미들웨어를 포함하며, 이를 사용해 여러 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 디렉티브는 해당 캐시 제어 디렉티브의 스네이크 케이스(snake case) 형태로 세미콜론으로 구분해 제공해야 합니다. 만약 디렉티브 목록에 `etag`가 포함되면, 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

```
Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 추가하기 (Attaching Cookies To Responses)

`Illuminate\Http\Response` 인스턴스에 `cookie` 메서드를 사용해 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 유효 기간(분 단위)을 전달해야 합니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 더 적게 사용하는 몇 가지 추가 인수도 받습니다. 일반적으로 이 인수들은 PHP의 원래 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에 전달되는 인수와 동일한 의미를 가집니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

만약 아직 응답 인스턴스가 없지만, 응답 전송 시 쿠키를 포함하고 싶다면 `Cookie` 파사드를 이용해 쿠키를 "대기열에 추가(queue)"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수를 받아, 응답 전 브라우저로 전송되기 전에 쿠키가 자동으로 첨부됩니다:

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기 (Generating Cookie Instances)

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 반드시 응답 인스턴스에 첨부되어야 클라이언트에 전송됩니다:

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료하기 (Expiring Cookies Early)

응답에서 쿠키를 제거하려면, 응답의 `withoutCookie` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies & Encryption)

기본적으로 Laravel에서 생성하는 모든 쿠키는 암호화되고 서명되어 있어 클라이언트에서 수정하거나 읽을 수 없습니다. 만약 애플리케이션에서 생성하는 일부 쿠키에 대해 암호화를 비활성화하려면, `app/Http/Middleware` 디렉토리에 위치한 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 속성을 사용하세요:

```
/**
 * 암호화를 적용하지 않을 쿠키 이름 목록.
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스 인스턴스로, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

때때로 제출된 폼이 유효하지 않을 경우와 같이 사용자를 이전 위치로 리다이렉트해야 할 때가 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/9.x/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하는지 확인하세요:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

인수를 주지 않고 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```
return redirect()->route('login');
```

라우트에 파라미터가 있는 경우 `route` 메서드에 두 번째 인자로 전달할 수 있습니다:

```
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 채우기 (Populating Parameters Via Eloquent Models)

만약 Eloquent 모델을 이용해 "ID" 파라미터를 채우는 라우트로 리다이렉트할 경우, 모델 자체를 전달할 수 있습니다. 그러면 ID 값이 자동으로 추출됩니다:

```
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스텀하고 싶다면, 라우트 파라미터 정의에서 컬럼을 지정할 수 있습니다 (`/profile/{id:slug}`) 또는 Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

```
/**
 * 모델 라우트 키 값을 반환합니다.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리다이렉트하기 (Redirecting To Controller Actions)

컨트롤러의 특정 액션으로 리다이렉트를 생성하려면, `action` 메서드에 컨트롤러 클래스와 액션 메서드 이름을 전달합니다:

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하면 `action` 메서드의 두 번째 인자로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트하기 (Redirecting To External Domains)

애플리케이션 밖의 도메인으로 리다이렉트해야 하는 경우가 있습니다. `away` 메서드를 호출하면 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성합니다:

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 플래시 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하면서 동시에 세션에 [플래시 데이터](/docs/9.x/session#flash-data)를 저장하는 경우가 많습니다. 보통 작업 성공 후 세션에 성공 메시지를 플래시하는 경우입니다. 편의를 위해 `RedirectResponse` 인스턴스를 생성하면서 플래시 데이터를 체이닝할 수 있습니다:

```
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

리다이렉트 후 사용자는 [세션](/docs/9.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/9.x/blade)을 사용하면 다음과 같습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트하기 (Redirecting With Input)

사용자가 유효성 검사 오류 등으로 인해 입력한 데이터를 유지하고 싶다면, `RedirectResponse`가 제공하는 `withInput` 메서드를 사용해 현재 요청의 입력 데이터를 세션에 플래시할 수 있습니다. 이후 요청에서 쉽게 [이전 입력값을 불러와](/docs/9.x/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다:

```
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입 (Other Response Types)

`response` 헬퍼는 다양한 응답 인스턴스를 생성할 때 사용됩니다. 인수 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/9.x/contracts) 구현체가 반환되고, 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답 상태 코드와 헤더를 제어하면서 [뷰](/docs/9.x/views)를 콘텐츠로 반환할 때는 `view` 메서드를 사용하세요:

```
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

만약 상태 코드나 헤더를 따로 지정하지 않는다면 전역 `view` 헬퍼 함수를 사용해도 됩니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드를 사용하면 `Content-Type` 헤더가 자동으로 `application/json`으로 설정되며, 전달한 배열을 `json_encode` PHP 함수로 JSON 형식으로 변환합니다:

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하려면 `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다:

```
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 사용자의 브라우저에게 특정 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인자로 다운로드할 때 보여질 파일 이름을 지정할 수 있고, 세 번째 인자로 HTTP 헤더 배열을 전달할 수 있습니다:

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> Symfony HttpFoundation는 파일 다운로드를 처리하는데, 다운로드할 파일의 이름은 ASCII 문자여야 합니다.

<a name="streamed-downloads"></a>
#### 스트림 다운로드 (Streamed Downloads)

어떤 작업의 문자열 결과를 디스크에 저장하지 않고 바로 다운로드 가능한 응답으로 전송하고 싶을 때는 `streamDownload` 메서드를 사용하세요. 이 메서드는 콜백 함수, 파일 이름, 그리고 선택적 헤더 배열을 받습니다:

```
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
                ->contents()
                ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="file-responses"></a>
### 파일 응답 (File Responses)

`file` 메서드는 이미지나 PDF 같은 파일을 브라우저에서 바로 표시하도록 할 때 사용합니다. 첫 번째 인자로 파일 경로, 두 번째 인자로는 헤더 배열을 전달할 수 있습니다:

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

라우트나 컨트롤러 여러 곳에서 재사용할 수 있는 사용자 정의 응답을 만들고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider` 같은 앱의 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 앱 서비스 부트스트랩 메서드.
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
```

`macro` 메서드는 첫 번째 인자로 이름을, 두 번째 인자로 클로저를 받습니다. 해당 이름으로 호출하면 클로저가 실행됩니다. `ResponseFactory` 구현체나 `response` 헬퍼를 통해 매크로를 호출할 수 있습니다:

```
return response()->caps('foo');
```