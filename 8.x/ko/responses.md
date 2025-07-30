# HTTP 응답 (HTTP Responses)

- [응답 생성하기](#creating-responses)
    - [응답에 헤더 붙이기](#attaching-headers-to-responses)
    - [응답에 쿠키 붙이기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름 있는 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
- [기타 응답 형식](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성하기 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열 (Strings & Arrays)

모든 라우트와 컨트롤러는 사용자의 브라우저로 다시 전송될 응답을 반환해야 합니다. Laravel은 여러 다양한 응답 반환 방식을 제공합니다. 가장 기본적인 응답 방식은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 해당 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐 아니라 배열을 반환할 수도 있습니다. 그러면 프레임워크는 해당 배열을 자동으로 JSON 응답으로 변환합니다:

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!TIP]
> 라우트 또는 컨트롤러에서 [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)을 반환할 수도 있다는 사실, 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체 (Response Objects)

대개 라우트 액션에서는 단순한 문자열이나 배열 대신 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환합니다.

`Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 세밀하게 제어할 수 있습니다. `Response`는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속받으며, 다양한 HTTP 응답을 생성하는 메서드를 제공합니다:

```
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션 (Eloquent Models & Collections)

라우트와 컨트롤러에서 [Eloquent ORM](/docs/{{version}}/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 이때 Laravel은 모델과 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 존중합니다:

```
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 붙이기 (Attaching Headers To Responses)

대부분의 응답 메서드는 체이닝이 가능하므로, 응답 인스턴스를 유창하게 구성할 수 있습니다. 예를 들어 `header` 메서드를 사용해 여러 헤더를 응답에 붙인 후 사용자에게 전송할 수 있습니다:

```
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 여러 헤더를 배열로 한 번에 지정할 수도 있습니다:

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

Laravel은 `cache.headers` 미들웨어를 제공하며, 이를 사용하면 여러 라우트에 대해 빠르게 `Cache-Control` 헤더를 설정할 수 있습니다. 캐시 관련 지시어는 대응하는 캐시 제어 지시어의 "스네이크 케이스" 형태로 세미콜론으로 구분하여 전달해야 합니다. 만약 목록에 `etag`가 포함되어 있으면, 응답 본문의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

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
### 응답에 쿠키 붙이기 (Attaching Cookies To Responses)

`cookie` 메서드를 사용하면 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 붙일 수 있습니다. 이 메서드에는 쿠키 이름, 값, 그리고 쿠키가 유효한 분 단위 시간을 전달해야 합니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 그 외에도 덜 자주 사용되는 몇 가지 인자를 더 받습니다. 일반적으로 이 인자들은 PHP의 네이티브 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에 전달하는 인자들과 동일한 역할을 합니다:

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없더라도, `Cookie` 파사드를 사용해 "큐(queue)" 방식으로 쿠키를 저장할 수 있습니다. 이렇게 하면 응답이 전송될 때 해당 쿠키들이 자동으로 응답에 부착됩니다. 큐에 추가하는 `queue` 메서드에도 쿠키 생성에 필요한 인자를 전달합니다:

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기 (Generating Cookie Instances)

`Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하여 나중에 응답 인스턴스에 붙이고 싶다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 반드시 응답에 붙여져야만 클라이언트에 전송됩니다:

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 빨리 만료시키기 (Expiring Cookies Early)

`withoutCookie` 메서드를 사용하면 쿠키를 만료시켜 제거할 수 있습니다:

```
return response('Hello World')->withoutCookie('name');
```

아직 응답 인스턴스가 없으면 `Cookie` 파사드의 `expire` 메서드를 사용할 수도 있습니다:

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화 (Cookies & Encryption)

Laravel에서 생성된 모든 쿠키는 기본적으로 암호화 및 서명되어 클라이언트가 수정하거나 읽을 수 없습니다. 만약 애플리케이션에서 일부 쿠키에 대해 암호화를 비활성화하고 싶다면, `app/Http/Middleware` 디렉토리에 위치한 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 속성에 해당 쿠키 이름을 추가하면 됩니다:

```
/**
 * 암호화하지 않을 쿠키 이름 목록.
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스는 여러 방법으로 생성할 수 있는데, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

사용자가 이전 위치로 리다이렉트되어야 하는 경우가 종종 있습니다. 예를 들어 폼 전송이 유효하지 않을 때가 그렇습니다. 이럴 경우 전역 `back` 헬퍼 함수를 쓸 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 사용하기 때문에, `back` 함수를 호출하는 라우트는 반드시 `web` 미들웨어 그룹을 사용해야 합니다:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름 있는 라우트로 리다이렉트 (Redirecting To Named Routes)

`redirect` 헬퍼에 파라미터 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 해당 인스턴스 메서드를 자유롭게 사용할 수 있습니다. 예를 들어 이름 있는 라우트로 리다이렉트하려면 `route` 메서드를 사용하세요:

```
return redirect()->route('login');
```

라우트에 파라미터가 있다면 `route` 메서드의 두 번째 인자로 넘길 수 있습니다:

```
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 채우기 (Populating Parameters Via Eloquent Models)

만약 "ID" 파라미터가 Eloquent 모델에서 자동으로 채워지는 라우트로 리다이렉트할 경우, 모델 인스턴스를 직접 넘길 수 있습니다. 그러면 Laravel이 자동으로 ID 값을 추출합니다:

```
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', [$user]);
```

파라미터에 넣을 값을 커스터마이징하려면, 라우트 파라미터를 `/profile/{id:slug}`처럼 컬럼을 지정하거나, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드하세요:

```
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
### 컨트롤러 액션으로 리다이렉트 (Redirecting To Controller Actions)

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리다이렉트하려면 `action` 메서드에 컨트롤러 클래스와 액션 이름을 넘기면 됩니다:

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인자로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트 (Redirecting To External Domains)

애플리케이션 외부 도메인으로 리다이렉트하려면 `away` 메서드를 사용하세요. 이 메서드는 추가적인 URL 인코딩이나 검증 없이 `RedirectResponse`를 생성합니다:

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시 세션 데이터와 함께 리다이렉트 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하고 동시에 [세션에 플래시 데이터](/docs/{{version}}/session#flash-data)를 저장하는 작업은 보통 같이 이루어집니다. 예를 들어, 동작을 성공적으로 수행한 후 성공 메시지를 세션에 플래시할 때 이렇게 합니다. 편리하도록 `RedirectResponse`를 생성하면서 세션 데이터도 한 번에 플래시하는 유창한 체인 메서드를 사용할 수 있습니다:

```
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후 세션에 저장된 메시지를 [세션](/docs/{{version}}/session)에서 읽어 화면에 출력할 수 있습니다. 예를 들어 [Blade 문법](/docs/{{version}}/blade)으로는 다음과 같습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트하기 (Redirecting With Input)

현재 요청의 입력값을 플래시해서 리다이렉트 전에 세션에 저장하려면, `RedirectResponse`의 `withInput` 메서드를 사용하세요. 일반적으로 사용자가 입력값 검증에서 실패했을 때 이 방식을 사용합니다. 입력값이 세션에 플래시되면, 다음 요청에서 해당 값을 쉽게 [재사용하여 폼을 다시 채울 수 있습니다](/docs/{{version}}/requests#retrieving-old-input):

```
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 형식 (Other Response Types)

`response` 헬퍼는 다른 다양한 응답 인스턴스를 생성할 때도 사용됩니다. 인자 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/{{version}}/contracts)을 구현한 객체를 반환합니다. 이 계약은 여러 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답 (View Responses)

응답의 상태와 헤더를 제어하면서 [뷰](/docs/{{version}}/views)를 반환해야 할 때는 `view` 메서드를 사용하면 됩니다:

```
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

만약 별도의 HTTP 상태 코드나 헤더 지정이 필요 없다면, 전역 `view` 헬퍼 함수를 사용해도 좋습니다.

<a name="json-responses"></a>
### JSON 응답 (JSON Responses)

`json` 메서드는 자동으로 `Content-Type` 헤더를 `application/json`으로 설정하며, 주어진 배열을 PHP의 `json_encode` 함수로 JSON 문자열로 변환합니다:

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶다면, `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다:

```
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드 (File Downloads)

`download` 메서드는 특정 경로의 파일을 사용자 브라우저에서 강제로 다운로드하게 만드는 응답을 생성합니다. 두 번째 인자로 파일명을 지정할 수 있는데, 이 이름이 사용자가 보는 다운로드 파일명입니다. 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!NOTE]
> Symfony HttpFoundation(파일 다운로드를 관리하는 라이브러리)는 다운로드할 파일명이 ASCII 문자여야 함을 요구합니다.

<a name="streamed-downloads"></a>
#### 스트리밍 다운로드 (Streamed Downloads)

작업 결과를 문자열로 곧바로 다운로드 응답으로 바꾸고 싶지만 파일로 저장하지 않고 싶을 때는 `streamDownload` 메서드를 사용하세요. 이 메서드는 콜백, 파일명, 헤더 배열(선택적)을 인자로 받습니다:

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

`file` 메서드는 이미지나 PDF 같은 파일을 다운로드가 아닌 브라우저 내에서 바로 표시할 때 씁니다. 첫 번째 인자로 파일 경로, 두 번째 인자로 헤더 배열을 받습니다:

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

여러 라우트나 컨트롤러에서 재사용할 수 있는 사용자 정의 응답을 만들고 싶다면, `Response` 파사드의 `macro` 메서드를 사용하세요. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나, 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드 안에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 초기화
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

`macro` 함수는 첫 번째 인자로 이름을, 두 번째 인자로 클로저를 받습니다. 이 매크로 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 해당 매크로 이름을 호출할 때 실행됩니다:

```
return response()->caps('foo');
```