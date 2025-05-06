# HTTP 응답

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리디렉션(redirect)](#redirects)
    - [이름이 지정된 라우트로 리디렉션하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리디렉션하기](#redirecting-controller-actions)
    - [외부 도메인으로 리디렉션하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리디렉션하기](#redirecting-with-flashed-session-data)
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

모든 라우트와 컨트롤러는 사용자 브라우저로 보내질 응답을 반환해야 합니다. Laravel은 여러 가지 방법으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 자동으로 문자열을 전체 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열 뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> {tip} [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)도 라우트나 컨트롤러에서 그대로 반환할 수 있다는 사실을 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한번 사용해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로는 라우트 액션에서 단순 문자열이나 배열만 반환하지는 않습니다. 그 대신, 보통 `Illuminate\Http\Response` 인스턴스 또는 [뷰](/docs/{{version}}/views)를 반환합니다.

전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 직접 지정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이를 통해 다양한 HTTP 응답을 손쉽게 구성할 수 있습니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[Eloquent ORM](/docs/{{version}}/eloquent) 모델과 컬렉션을 라우트와 컨트롤러에서 직접 반환할 수도 있습니다. 이 경우, Laravel이 모델의 [hidden 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 고려하여 자동으로 JSON 응답으로 변환합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝이 가능하므로, 응답 인스턴스를 유연하게 구성할 수 있습니다. 예를 들어, 응답을 사용자에게 보내기 전에 `header` 메서드를 사용하여 여러 개의 헤더를 추가할 수 있습니다:

```php
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용하여 한 번에 여러 개의 헤더를 배열로 지정할 수도 있습니다:

```php
return response($content)
            ->withHeaders([
                'Content-Type' => $type,
                'X-Header-One' => 'Header Value',
                'X-Header-Two' => 'Header Value',
            ]);
```

<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

Laravel은 여러 라우트 그룹에 대해 `Cache-Control` 헤더를 쉽고 빠르게 설정할 수 있도록 `cache.headers` 미들웨어를 제공합니다. 지시자는 캐시 제어 디렉티브의 "스네이크 케이스"로, 세미콜론(`;`)으로 구분합니다. 만약 지시자 목록에 `etag`를 포함하면, 응답 본문에 대한 MD5 해시가 ETag 식별자로 자동 설정됩니다:

```php
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
### 응답에 쿠키 추가하기

`cookie` 메서드를 사용하여 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 붙일 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효기간(분 단위)을 전달합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 메서드와 마찬가지로 몇몇 추가 인자를 받을 수 있습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

만약 아직 응답 인스턴스가 없는데 나가는 응답에 쿠키를 반드시 포함시키고 싶으면, `Cookie` 파사드를 사용하여 "queue"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수를 받습니다. 이 쿠키들은 브라우저에 응답이 전송되기 전에 응답에 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

`Symfony\Component\HttpFoundation\Cookie` 인스턴스를 미리 생성하여 나중에 응답 인스턴스에 붙이고 싶다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 경우 쿠키는 응답에 추가하지 않으면 클라이언트로 보내지지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

나가는 응답의 `withoutCookie` 메서드를 사용하여 쿠키를 만료(삭제)할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 나가는 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드로 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

Laravel이 생성하는 모든 쿠키는 기본적으로 암호화되고 서명되어, 클라이언트가 쿠키를 읽거나 수정할 수 없습니다. 애플리케이션에서 생성되는 일부 쿠키에 대해 암호화를 비활성화하려면, `app/Http/Middleware` 디렉토리의 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 프로퍼티를 사용하세요:

```php
/**
 * 암호화하지 않을 쿠키 이름 목록
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

<a name="redirects"></a>
## 리디렉션(redirect)

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 올바른 헤더를 포함합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 단순한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

폼 전송이 유효하지 않을 때처럼 사용자를 이전 페이지로 다시 리디렉션해야 하는 경우도 있습니다. 이때 전역 `back` 헬퍼 메서드를 사용하면 됩니다. 이 기능은 [세션](/docs/{{version}}/session)을 활용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용하도록 해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리디렉션하기

`redirect` 헬퍼를 인자 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스를 반환합니다. 이를 통해 `Redirector` 인스턴스의 다양한 메서드들을 바로 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리디렉션을 생성하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요하다면, `route` 메서드의 두 번째 인자로 파라미터 배열을 전달합니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 전달

만약 "ID" 파라미터가 필요한 라우트로 리디렉션하며, Eloquent 모델 인스턴스에서 파라미터를 추출하려면 모델 자체를 전달하면 됩니다. ID는 자동으로 추출됩니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 직접 지정하려면, 라우트 파라미터 정의(`/profile/{id:slug}`)에 컬럼명을 지정하거나, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

```php
/**
 * 모델의 라우트 키 값을 반환합니다.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션하기

[컨트롤러 액션](/docs/{{version}}/controllers)으로도 리디렉션을 생성할 수 있습니다. 이때는 `action` 메서드에 컨트롤러와 액션 이름을 전달합니다:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하면 두 번째 인자로 전달하면 됩니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션하기

때로는 애플리케이션 외부의 도메인으로 리디렉션해야 할 수도 있습니다. 이 경우, URL 인코딩·검증·확인 작업 없이 `away` 메서드를 호출하여 `RedirectResponse`를 생성하세요:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리디렉션하기

새 URL로 리디렉션하면서 [세션에 데이터를 플래시](#flash-data)하는 경우가 많습니다. 일반적으로 어떤 작업을 성공적으로 수행한 뒤 성공 메시지를 세션에 플래시하고 바로 리디렉션합니다. 편의상, 한 번의 메서드 체인으로 `RedirectResponse` 인스턴스 생성과 세션 데이터 플래시가 가능합니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리디렉션된 뒤에는 [세션](/docs/{{version}}/session)에 저장된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)을 사용할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리디렉션하기

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 사용자가 새 위치로 리디렉션되기 전에 현재 요청의 입력값을 세션에 플래시할 수 있습니다. 일반적으로 사용자가 유효성 검사 오류를 만났을 때 사용합니다. 입력값이 세션에 플래시되면, 다음 요청에서 [이전 입력값을 손쉽게 가져와](#retrieving-old-input) 폼을 다시 채울 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼를 사용하면 다른 타입의 응답 인스턴스들도 생성할 수 있습니다. 인자 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/{{version}}/contracts)이 구현된 객체가 반환됩니다. 이 계약은 다양한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 및 헤더를 직접 지정하면서 [뷰](/docs/{{version}}/views)를 응답 본문으로 반환하려면 `view` 메서드를 사용하세요:

```php
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

맞춤 HTTP 상태 코드나 헤더를 직접 전달할 필요가 없다면, 단순히 전역 `view` 헬퍼 함수를 사용할 수도 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 `application/json`으로 자동 지정하고, 주어진 배열을 PHP의 `json_encode` 함수를 사용하여 JSON으로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답이 필요하다면, `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다:

```php
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용하면, 해당 경로의 파일을 사용자의 브라우저가 다운로드하도록 강제하는 응답을 생성할 수 있습니다. `download` 메서드는 두 번째 인자로 파일명을 전달하면, 사용자가 다운로드할 때 보이는 파일 이름이 결정됩니다. 마지막으로, HTTP 헤더 배열을 세 번째 인자로 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> {note} 파일 다운로드를 관리하는 Symfony HttpFoundation은, 다운로드되는 파일에 ASCII 파일명이 있어야 한다는 점에 유의하세요.

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드

어떤 연산의 반환 문자열을 디스크에 저장하지 않고, 곧바로 다운로드 응답으로 전송하고 싶을 때가 있습니다. 이럴 때 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일 이름, (선택적으로) 헤더 배열을 인자로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
                ->contents()
                ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면, 파일(예: 이미지나 PDF 등)을 사용자의 브라우저에서 바로 표시할 수 있습니다(다운로드를 시작하는 것이 아니라). 이 메서드는 첫 번째 인자로 파일 경로, 두 번째 인자로 헤더 배열을 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
## 응답 매크로

다양한 라우트와 컨트롤러에서 재사용할 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나(예: `App\Providers\AppServiceProvider`)의 `boot` 메서드에서 호출하면 됩니다:

```php
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
```

`macro` 함수는 첫 번째 인자로 매크로의 이름, 두 번째 인자로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory`의 구현 또는 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
