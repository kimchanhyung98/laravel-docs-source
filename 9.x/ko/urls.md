# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션용 URL](#urls-for-controller-actions)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션용 URL을 생성하는 데 도움을 주는 여러 헬퍼를 제공합니다. 이러한 헬퍼는 주로 템플릿이나 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리다이렉트 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼는 애플리케이션을 위한 임의의 URL을 생성할 때 사용됩니다. 생성된 URL은 현재 처리 중인 요청의 스키마(HTTP 또는 HTTPS)와 호스트를 자동으로 사용합니다:

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing The Current URL)

`url` 헬퍼에 경로를 전달하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 얻을 수 있습니다:

```
// 쿼리 문자열 없이 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열을 포함한 전체 현재 URL 가져오기...
echo url()->full();

// 이전 요청의 전체 URL 가져오기...
echo url()->previous();
```

이 메서드들은 `URL` [파사드](/docs/9.x/facades)를 통해서도 접근할 수 있습니다:

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL (URLs For Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/9.x/routing#named-routes)의 URL을 생성하는 데 사용됩니다. 이름이 지정된 라우트를 사용하면 실제 라우트 URL에 종속되지 않고 URL을 생성할 수 있습니다. 따라서 라우트 URL이 변경되어도 `route` 함수를 호출하는 부분을 수정할 필요가 없습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해봅시다:

```
Route::get('/post/{post}', function (Post $post) {
    //
})->name('post.show');
```

이 라우트의 URL을 생성하려면 `route` 헬퍼를 다음과 같이 사용할 수 있습니다:

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 개의 매개변수가 있는 라우트의 URL 생성에도 사용할 수 있습니다:

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    //
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의 매개변수와 일치하지 않은 추가 배열 요소는 URL의 쿼리 문자열에 추가됩니다:

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

주로 [Eloquent 모델](/docs/9.x/eloquent)의 라우트 키(보통 기본 키)를 사용해 URL을 생성하게 됩니다. 따라서 Eloquent 모델을 매개변수 값으로 전달할 수 있으며, `route` 헬퍼가 자동으로 모델의 라우트 키를 추출합니다:

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 이름이 지정된 라우트에 대해 쉽게 "서명된" URL을 생성할 수 있도록 지원합니다. 이 URL에는 쿼리 문자열에 "서명" 해시가 붙어 있어 URL이 생성된 이후 변경되지 않았음을 검증할 수 있습니다. 서명된 URL은 공개적으로 액세스 가능하지만 URL 조작에 대한 보호층이 필요한 라우트에서 매우 유용합니다.

예를 들어, 고객에게 이메일로 전송하는 공개 "구독 해제" 링크에 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 대해 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

지정한 시간 후 만료되는 임시 서명된 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하세요. Laravel은 서명된 URL에 인코딩된 만료 타임스탬프가 경과했는지 검증합니다:

```
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증 (Validating Signed Route Requests)

들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면, `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때로는 프론트엔드에서 페이지네이션 등 클라이언트 사이드 작업을 위해 서명된 URL에 데이터를 추가해야 할 수도 있습니다. 이럴 때는 `hasValidSignatureWhileIgnoring` 메서드를 사용해 서명 검증 시 무시할 쿼리 매개변수를 지정할 수 있습니다. 다만, 무시된 매개변수는 누구나 수정할 수 있다는 점을 유념하세요:

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 사용해 서명된 URL을 검증하는 대신, `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/9.x/middleware)를 라우트에 할당할 수 있습니다. 아직 할당하지 않은 경우 HTTP 커널의 `routeMiddleware` 배열에 이 미들웨어를 키와 함께 등록해야 합니다:

```
/**
 * 애플리케이션의 라우트 미들웨어 목록.
 *
 * 이 미들웨어들은 그룹에 할당하거나 개별로 사용할 수 있습니다.
 *
 * @var array
 */
protected $routeMiddleware = [
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
];
```

미들웨어를 커널에 등록했다면 라우트에 첨부할 수 있습니다. 들어오는 요청에 유효한 서명이 없으면 미들웨어가 자동으로 HTTP 상태 코드 `403` 응답을 반환합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명된 라우트에 대한 응답 (Responding To Invalid Signed Routes)

만료된 서명된 URL에 접속하면 기본적으로 `403` HTTP 상태 코드를 가진 일반 오류 페이지가 표시됩니다. 하지만 `InvalidSignatureException` 예외에 대한 커스텀 "renderable" 클로저를 예외 처리기에 정의하여 이 동작을 변경할 수 있습니다. 클로저는 HTTP 응답을 반환해야 합니다:

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

/**
 * 애플리케이션 예외 처리 콜백 등록.
 *
 * @return void
 */
public function register()
{
    $this->renderable(function (InvalidSignatureException $e) {
        return response()->view('error.link-expired', [], 403);
    });
}
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션용 URL (URLs For Controller Actions)

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 매개변수를 받는다면, 두 번째 인자로 라우트 매개변수의 연상 배열을 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본값 설정 (Default Values)

일부 애플리케이션에서는 요청 전역으로 특정 URL 매개변수에 대해 기본값을 지정하고 싶을 수 있습니다. 예를 들어 많은 라우트가 `{locale}` 매개변수를 정의하는 경우를 생각해봅시다:

```
Route::get('/{locale}/posts', function () {
    //
})->name('post.index');
```

매번 `route` 헬퍼 호출 시 `locale` 값을 넘겨주는 것이 번거롭다면, 현재 요청 동안 항상 적용될 기본값을 `URL::defaults` 메서드로 설정할 수 있습니다. 보통 이 메서드는 [라우트 미들웨어](/docs/9.x/middleware#assigning-middleware-to-routes)에서 호출하여 현재 요청에 접근합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\URL;

class SetDefaultLocaleForUrls
{
    /**
     * 들어오는 요청 처리.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return \Illuminate\Http\Response
     */
    public function handle($request, Closure $next)
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

`locale` 매개변수에 대한 기본값이 설정되면, `route` 헬퍼를 통해 URL 생성 시 더 이상 해당 값을 명시적으로 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 실행 순서 (URL Defaults & Middleware Priority)

URL 기본값 설정은 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있으므로, `URL::defaults`를 호출하는 미들웨어는 Laravel 기본 미들웨어인 `SubstituteBindings`보다 먼저 실행되도록 [미들웨어 우선순위](/docs/9.x/middleware#sorting-middleware)를 지정해야 합니다. 이는 애플리케이션 HTTP 커널의 `$middlewarePriority` 속성에 미들웨어 순서를 적절히 배치함으로써 가능하며, `Illuminate\Foundation\Http\Kernel` 클래스에서 구현을 복사해 재정의하는 방식으로 수정할 수 있습니다:

```
/**
 * 우선순위에 따라 정렬된 미들웨어 목록.
 *
 * 비전역 미들웨어가 항상 지정된 순서대로 실행되도록 강제합니다.
 *
 * @var array
 */
protected $middlewarePriority = [
    // ...
     \App\Http\Middleware\SetDefaultLocaleForUrls::class,
     \Illuminate\Routing\Middleware\SubstituteBindings::class,
     // ...
];
```