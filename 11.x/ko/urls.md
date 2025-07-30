# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트용 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션용 URL](#urls-for-controller-actions)
- [기본값](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 URL을 생성하는 데 도움을 주는 여러 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 생성하거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 만들 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼를 사용하면 애플리케이션의 임의 URL을 생성할 수 있습니다. 생성된 URL은 자동으로 현재 처리 중인 요청의 스킴(HTTP 혹은 HTTPS)과 호스트를 사용합니다:

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 문자열 매개변수가 포함된 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로에 이미 존재하는 쿼리 문자열 매개변수를 제공하면 기존 값이 덮어쓰기 됩니다:

```
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

값이 배열인 쿼리 매개변수도 전달할 수 있으며, 생성된 URL에서는 해당 배열 값들이 적절한 키와 함께 인코딩되어 표현됩니다:

```
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing the Current URL)

`url` 헬퍼에 경로를 제공하지 않으면 `Illuminate\Routing\UrlGenerator` 객체가 반환되어 현재 URL에 관한 다양한 정보를 접근할 수 있습니다:

```
// 쿼리 문자열을 제외한 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열을 포함한 현재 URL 가져오기...
echo url()->full();

// 이전 요청의 전체 URL 가져오기...
echo url()->previous();

// 이전 요청의 경로 가져오기...
echo url()->previousPath();
```

이 메서드들은 `URL` [파사드](/docs/11.x/facades)를 통해서도 사용할 수 있습니다:

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트용 URL (URLs for Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/11.x/routing#named-routes)의 URL을 생성하는 데 사용됩니다. 이름이 지정된 라우트는 URL이 변경되어도 라우트 호출 형태를 바꿀 필요 없이 URL 생성을 가능하게 합니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다고 가정해 봅시다:

```
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트로의 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용합니다:

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론 `route` 헬퍼는 여러 인수를 가진 라우트에 대해서도 URL 생성이 가능합니다:

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의된 매개변수에 해당하지 않는 추가 배열 요소들은 URL 쿼리 문자열에 추가됩니다:

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

라우트 키(보통 기본 키)로 URL을 만드는 상황이 많기 때문에 [Eloquent 모델](/docs/11.x/eloquent)을 매개변수로 넘길 수도 있습니다. `route` 헬퍼는 자동으로 모델의 라우트 키를 추출합니다:

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 이름이 지정된 라우트를 위한 "서명된" URL을 쉽게 만들 수 있도록 지원합니다. 이 URL은 쿼리 문자열에 "서명" 해시가 추가되어 URL이 생성된 이후 변경되지 않았음을 Laravel이 확인할 수 있게 합니다. 서명된 URL은 공개적으로 접근이 가능하지만 URL 조작 방지가 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 전송하는 공개 "구독 취소" 링크를 구현할 때 사용할 수 있습니다. 이름이 지정된 라우트의 서명된 URL을 만들려면 `URL` 파사드의 `signedRoute` 메서드를 사용합니다:

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

URL 해시에 도메인을 포함하지 않으려면 `signedRoute` 메서드에 `absolute` 인수를 `false`로 제공할 수 있습니다:

```
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 시간 이후 만료되는 임시 서명된 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하세요. Laravel은 URL에 인코딩된 만료 타임스탬프가 경과하지 않았는지 검증합니다:

```
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증 (Validating Signed Route Requests)

들어오는 요청이 유효한 서명을 가지는지 확인하려면, `Illuminate\Http\Request` 인스턴스의 `hasValidSignature` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

경우에 따라 클라이언트 측 페이지네이션처럼 애플리케이션 프론트엔드에서 서명된 URL에 데이터를 추가해야 할 수 있습니다. 이때 `hasValidSignatureWhileIgnoring` 메서드를 사용해 검증 시 무시할 쿼리 파라미터를 지정할 수 있습니다. 단, 무시된 파라미터는 누구나 수정할 수 있음을 명심하세요:

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

요청 인스턴스를 사용해 서명된 URL을 검증하는 대신, `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/11.x/middleware)를 라우트에 할당할 수 있습니다. 서명이 유효하지 않으면 미들웨어가 자동으로 HTTP 403 응답을 반환합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL에 도메인을 해시에 포함하지 않았다면, 미들웨어에 `relative` 인수를 전달해야 합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 무효한 서명 URL에 대한 응답 (Responding to Invalid Signed Routes)

서명된 URL이 만료된 경우, 방문자는 HTTP 403 상태 코드의 기본 에러 페이지를 받게 됩니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 사용자 지정 "render" 클로저를 정의해 이 동작을 커스터마이즈할 수 있습니다:

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션용 URL (URLs for Controller Actions)

`action` 함수는 지정한 컨트롤러 액션의 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 매개변수를 받는 경우, 두 번째 인수로 연관 배열 형태의 라우트 매개변수를 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본값 (Default Values)

일부 애플리케이션에서는 특정 URL 매개변수에 대해 요청 전체에서 사용할 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 매개변수를 정의한 상황을 생각해보세요:

```
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

라우트를 호출할 때마다 `locale`을 항상 전달하는 것은 번거롭습니다. 그래서 `URL::defaults` 메서드를 사용해 현재 요청 동안 항상 적용될 해당 매개변수의 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/11.x/middleware#assigning-middleware-to-routes)에서 호출하면 현재 요청에 접근할 수 있어 유용합니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;
use Symfony\Component\HttpFoundation\Response;

class SetDefaultLocaleForUrls
{
    /**
     * 들어오는 요청 처리
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

한번 `locale` 매개변수 기본값을 설정하면, 이후 `route` 헬퍼를 사용할 때 기본값을 명시할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값 설정은 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있으므로, URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/11.x/middleware#sorting-middleware)를 지정해야 합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 통해 다음과 같이 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```