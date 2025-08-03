# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL (Signed URLs)](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에서 URL을 생성할 때 도움이 되는 여러 헬퍼 함수를 제공합니다. 이러한 헬퍼는 주로 템플릿이나 API 응답 내에서 링크를 만들거나, 애플리케이션 내 다른 부분으로 리다이렉트 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼는 애플리케이션을 위한 임의의 URL을 생성할 때 사용할 수 있습니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스키마(HTTP 또는 HTTPS)와 호스트를 자동으로 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 문자열 파라미터가 포함된 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

이미 경로에 존재하는 쿼리 문자열 파라미터를 제공하면 기존 값이 덮어쓰여집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

쿼리 파라미터로 배열 값을 전달할 수도 있습니다. 이 경우 생성된 URL에서 적절히 키가 붙고 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing the Current URL)

`url` 헬퍼에 경로를 제공하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 얻을 수 있습니다:

```php
// 쿼리 문자열 없이 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열을 포함한 현재 URL 가져오기...
echo url()->full();

// 이전 요청의 전체 URL 가져오기...
echo url()->previous();

// 이전 요청의 경로 가져오기...
echo url()->previousPath();
```

이 메서드들은 `URL` [파사드](/docs/master/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL (URLs for Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/master/routing#named-routes)의 URL을 생성할 때 사용됩니다. 이름이 지정된 라우트를 사용하면 라우트에 정의된 실제 URL에 결합되지 않고 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되어도 `route` 함수 호출 부분은 변경할 필요가 없습니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다고 가정합시다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트에 대한 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, 여러 개의 파라미터가 필요한 라우트의 URL도 생성할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의 파라미터에 포함되지 않는 추가 배열 요소는 URL의 쿼리 문자열로 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

많은 경우 [Eloquent 모델](/docs/master/eloquent)의 라우트 키(일반적으로 기본 키)를 이용해 URL을 생성합니다. 따라서 Eloquent 모델을 파라미터 값으로 전달할 수 있으며, `route` 헬퍼가 모델의 라우트 키를 자동으로 추출합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 이름이 지정된 라우트에 대해 쉽게 "서명된(Signed)" URL을 생성할 수 있도록 지원합니다. 이런 URL은 쿼리 문자열에 "서명" 해시가 포함되어, 생성된 이후 URL이 변경되지 않았는지 Laravel이 검증할 수 있습니다. 서명된 URL은 공개 접근이 가능하지만 URL 조작에 대한 보호가 필요한 라우트에 특히 유용합니다.

예를 들어, 고객에게 이메일로 전송하는 공개 "구독 취소(unsubscribe)" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 서명된 URL을 만들려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

서명 URL 해시에 도메인을 포함하지 않으려면 `signedRoute` 메서드에 `absolute` 인수를 `false`로 전달하면 됩니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 기간 후 만료되는 임시 서명된 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하세요. Laravel은 서명된 URL에 인코딩된 만료 시간이 초과됐는지 검증합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증 (Validating Signed Route Requests)

들어오는 요청이 유효한 서명을 갖는지 확인하려면, 요청의 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때때로 애플리케이션 프론트엔드가 서명된 URL에 데이터를 덧붙여야 할 수 있습니다(예: 클라이언트 측 페이징). 이 경우 `hasValidSignatureWhileIgnoring` 메서드를 사용하여 서명 검증 시 무시할 쿼리 파라미터를 지정할 수 있습니다. 다만 이렇게 하면 누구나 해당 파라미터를 요청에서 수정할 수 있다는 점에 유의하세요:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 통해 서명 URL을 검증하는 대신, 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/master/middleware)를 할당할 수도 있습니다. 만약 유효한 서명이 없으면, 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명 URL 해시에 도메인을 포함하지 않은 경우, 미들웨어에 `relative` 인수를 제공합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명된 라우트에 응답하기 (Responding to Invalid Signed Routes)

서명된 URL이 만료되어 접속 시도하면 기본적으로 `403` HTTP 상태 코드를 가진 일반 오류 페이지가 표시됩니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대해 사용자 지정 "렌더링" 클로저를 정의하여 이 행동을 변경할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL (URLs for Controller Actions)

`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관배열 형태의 파라미터를 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본값 설정 (Default Values)

일부 애플리케이션에서는 특정 URL 파라미터에 대해 요청 범위 내 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에 `{locale}` 파라미터가 정의되어 있다고 가정합시다:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

매번 `route` 헬퍼 호출 시마다 `locale`을 전달하는 것은 번거로울 수 있습니다. 이럴 때 `URL::defaults` 메서드를 사용하면 현재 요청 동안 항상 적용되는 이 파라미터의 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/master/middleware#assigning-middleware-to-routes) 내에서 호출하여 현재 요청에 접근할 수 있도록 하는 것이 좋습니다:

```php
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

`locale` 파라미터의 기본값이 설정된 후에는 `route` 헬퍼를 사용할 때마다 해당 값을 명시적으로 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 실행 순서 (URL Defaults and Middleware Priority)

URL 기본값 설정은 Laravel의 암묵적 모델 바인딩(implicit model bindings)에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [우선순위(priority)](/docs/master/middleware#sorting-middleware)를 지정하는 것이 좋습니다. 다음과 같이 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용해 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```