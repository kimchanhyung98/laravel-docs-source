# URL 생성

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [기본값](#default-values)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 URL 생성을 돕는 다양한 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿 및 API 응답 내에서 링크를 생성하거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항

<a name="generating-urls"></a>
### URL 생성

`url` 헬퍼는 애플리케이션을 위한 임의의 URL을 생성하는 데 사용할 수 있습니다. 생성된 URL은 현재 애플리케이션에서 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 문자열 파라미터와 함께 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로에 이미 존재하는 쿼리 문자열 파라미터를 제공하면 해당 값이 덮어써집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

배열 형태의 값을 쿼리 파라미터로 전달할 수 있습니다. 이러한 값들은 생성된 URL에서 적절하게 키와 인코딩이 적용됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기

`url` 헬퍼에 경로를 전달하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 얻을 수 있습니다:

```php
// 쿼리 문자열 없이 현재 URL을 가져옵니다...
echo url()->current();

// 쿼리 문자열을 포함한 현재 URL을 가져옵니다...
echo url()->full();

// 이전 요청의 전체 URL을 가져옵니다...
echo url()->previous();

// 이전 요청의 경로를 가져옵니다...
echo url()->previousPath();
```

이러한 메서드들은 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL

`route` 헬퍼는 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)로의 URL을 생성하는 데 사용할 수 있습니다. 이름이 지정된 라우트를 사용하면 실제 라우트 URL에 의존하지 않고 URL을 생성할 수 있으므로, 라우트의 URL이 변경되더라도 `route` 함수 사용 코드를 수정할 필요가 없습니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다고 가정해봅시다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트로의 URL을 생성하려면, 아래와 같이 `route` 헬퍼를 사용할 수 있습니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 파라미터를 가지는 라우트에 대해서도 사용할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트에 정의된 파라미터와 일치하지 않는 추가 배열 요소들은 URL의 쿼리 문자열에 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델

일반적으로 [Eloquent 모델](/docs/{{version}}/eloquent)의 라우트 키(보통 기본 키)를 사용하여 URL을 자주 생성하게 됩니다. 따라서 Eloquent 모델을 파라미터 값으로 전달할 수 있습니다. `route` 헬퍼는 모델의 라우트 키를 자동으로 추출합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 이름이 지정된 라우트에 대해 "서명된" URL을 손쉽게 생성할 수 있도록 지원합니다. 이 URL들은 쿼리 문자열에 "signature" 해시가 추가되어, URL이 생성 이후에 변조되지 않았음을 Laravel이 검증할 수 있게 합니다. 서명된 URL은 공개적으로 접근 가능하지만 URL 변조로부터 보호가 필요한 라우트에 특히 유용합니다.

예를 들어, 고객에게 이메일로 보내는 공개 "구독 해지" 링크 등에서 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트로의 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

서명된 URL 해시에서 도메인을 제외하려면 `signedRoute` 메서드에 `absolute` 인자를 전달하세요:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

지정한 시간이 지난 후 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel이 임시 서명 라우트 URL을 검증할 때, 서명된 URL에 인코딩된 만료 시간이 아직 지나지 않았는지 확인합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증

들어오는 요청이 올바른 서명을 가지고 있는지 확인하려면, 들어오는 `Illuminate\Http\Request` 인스턴스의 `hasValidSignature` 메서드를 호출해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때때로, 프론트엔드에서 페이지네이션 등과 같이 서명된 URL에 데이터를 추가로 붙여야 할 수 있습니다. 이런 경우 `hasValidSignatureWhileIgnoring` 메서드를 사용하여 서명 검증 시 무시할 쿼리 파라미터를 지정할 수 있습니다. 단, 무시된 파라미터는 누구나 변경할 수 있으므로 주의가 필요합니다:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 통해 서명된 URL을 검증하는 대신, 해당 라우트에 `signed`(`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/{{version}}/middleware)를 지정할 수도 있습니다. 유효한 서명이 없는 경우, 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL에 도메인이 포함되어 있지 않은 경우, 미들웨어에 `relative` 인자를 제공해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 라우트 응답 처리

서명된 URL이 만료되었을 때 방문하면, 기본적으로 `403` HTTP 상태 코드의 일반적인 오류 페이지가 표시됩니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 사용자 지정 "렌더" 클로저를 정의하여 이 동작을 커스터마이즈할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL

`action` 함수는 주어진 컨트롤러 액션의 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는다면, 두 번째 인자로 연관 배열 형태의 라우트 파라미터를 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본값

일부 애플리케이션에서는 특정 URL 파라미터에 대해 전체 요청에 걸친 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트들이 `{locale}` 파라미터를 정의하고 있다고 가정합시다:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

`route` 헬퍼를 호출할 때마다 항상 `locale`을 전달하는 것은 번거롭습니다. 그래서, `URL::defaults` 메서드를 이용해 현재 요청 동안 항상 적용될 파라미터의 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하여 현재 요청에 접근하는 것이 좋습니다:

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
     * 들어오는 요청 처리.
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

`locale` 파라미터의 기본값이 설정되면, `route` 헬퍼를 통해 URL을 생성할 때 더 이상 해당 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값 및 미들웨어 우선순위

URL 기본값을 설정하면 Laravel의 암시적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 지정해야 합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용하여 이를 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
