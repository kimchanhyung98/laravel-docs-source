# URL 생성

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성](#generating-urls)
    - [현재 URL 접근](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [플루언트 URI 객체](#fluent-uri-objects)
- [기본값](#default-values)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 URL을 생성할 수 있도록 도와주는 다양한 헬퍼를 제공합니다. 이러한 헬퍼는 주로 템플릿이나 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항

<a name="generating-urls"></a>
### URL 생성

`url` 헬퍼는 애플리케이션의 임의의 URL을 생성하는 데 사용할 수 있습니다. 생성된 URL은 자동으로 현재 애플리케이션에서 처리되는 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 사용합니다:

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

경로에 이미 존재하는 쿼리 문자열 파라미터에 값을 제공하면 해당 값이 덮어써집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

값의 배열도 쿼리 파라미터로 전달할 수 있습니다. 이 값들은 생성된 URL에서 적절하게 키가 붙고 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근

`url` 헬퍼에 경로를 전달하지 않을 경우, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 확인할 수 있습니다:

```php
// 쿼리 문자열 없이 현재 URL을 가져옵니다...
echo url()->current();

// 쿼리 문자열을 포함해 현재 URL을 가져옵니다...
echo url()->full();

// 이전 요청의 전체 URL을 가져옵니다...
echo url()->previous();

// 이전 요청의 경로를 가져옵니다...
echo url()->previousPath();
```

이러한 메서드는 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL

`route` 헬퍼는 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)에 대한 URL을 생성하는 데 사용할 수 있습니다. 이름이 지정된 라우트를 사용하면 라우트에 정의된 실제 URL에 의존하지 않고 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되더라도 `route` 함수를 호출하는 코드를 수정할 필요가 없습니다. 예를 들어, 애플리케이션에 다음과 같이 라우트를 정의했다고 가정해봅시다:

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

물론, `route` 헬퍼는 여러 개의 파라미터가 있는 라우트에 대한 URL도 생성할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트의 정의된 파라미터에 해당하지 않는 추가 배열 요소는 URL의 쿼리 문자열에 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델

대부분의 경우 [Eloquent 모델](/docs/{{version}}/eloquent)의 라우트 키(보통은 기본키)를 사용하여 URL을 생성하게 됩니다. 따라서 Eloquent 모델 객체를 파라미터 값으로 직접 전달할 수 있습니다. `route` 헬퍼는 자동으로 모델의 라우트 키를 추출합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 이름이 지정된 라우트에 손쉽게 "서명된" URL을 생성할 수 있도록 지원합니다. 이러한 URL은 쿼리 문자열에 "서명" 해시가 첨부되어 있어, URL이 생성된 이후 변경되지 않았음을 Laravel이 확인할 수 있습니다. 서명된 URL은 누구나 접근 가능하지만 URL 변조로부터 보호가 필요한 라우트에 적합합니다.

예를 들어, 고객에게 이메일로 발송하는 공개 "구독 취소" 링크 구현에 서명된 URL을 활용할 수 있습니다. 이름이 지정된 라우트에 대한 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

`absolute` 인자를 `signedRoute` 메서드에 전달하면 서명된 URL 해시에서 도메인을 제외할 수 있습니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 시간 후 만료되는 임시 서명 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하면 됩니다. Laravel이 임시 서명 라우트 URL을 확인할 때, 서명된 URL에 인코딩된 만료 타임스탬프가 지나지 않았는지 검사합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명 라우트 요청 검증

들어오는 요청에 유효한 서명이 있는지 확인하려면, 들어오는 `Illuminate\Http\Request` 인스턴스의 `hasValidSignature` 메서드를 호출해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때에 따라, 프론트엔드에서 클라이언트 사이드 페이지네이션과 같은 이유로 서명된 URL에 데이터를 추가해야 할 수도 있습니다. 이럴 경우, `hasValidSignatureWhileIgnoring` 메서드를 사용해 검증 시 무시할 쿼리 파라미터를 지정할 수 있습니다. 단, 해당 파라미터는 누구나 변경 가능함을 유의하세요:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 사용해 직접 서명된 URL 유효성을 검사하는 대신, 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/{{version}}/middleware)를 할당할 수도 있습니다. 요청이 유효한 서명을 포함하지 않을 경우, 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다.

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL 해시에 도메인이 포함되지 않은 경우, 미들웨어에 `relative` 인자를 제공해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 라우트 응답하기

서명된 URL이 만료되었을 때 접속할 경우, 기본적으로 `403` HTTP 상태 코드의 일반적인 오류 페이지가 표시됩니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 커스텀 "render" 클로저를 정의하여 이 동작을 맞춤화할 수 있습니다:

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

`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인자에 라우트 파라미터의 연관 배열을 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## 플루언트 URI 객체

Laravel의 `Uri` 클래스는 객체를 통해 URI를 손쉽게 생성하고 조작할 수 있는 플루언트 인터페이스를 제공합니다. 이 클래스는 기본적으로 하위 League URI 패키지의 기능을 감싸며, Laravel의 라우팅 시스템과 완벽하게 통합됩니다.

정적 메서드를 사용해 손쉽게 `Uri` 인스턴스를 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 지정한 문자열로부터 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 이름이 지정된 라우트, 컨트롤러 액션에 대한 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL로부터 URI 인스턴스 생성...
$uri = $request->uri();
```

URI 인스턴스를 얻은 후에는 플루언트하게 수정할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

플루언트 URI 객체를 더욱 사용하는 방법은 [URI 문서](/docs/{{version}}/helpers#uri)를 참조하세요.

<a name="default-values"></a>
## 기본값

일부 애플리케이션에서는 특정 URL 파라미터에 대해 요청 범위의 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에 `{locale}` 파라미터가 정의되어 있다고 가정해 봅시다:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

매번 `route` 헬퍼를 호출할 때마다 항상 `locale`을 전달하는 것은 번거롭습니다. 이럴 때는 `URL::defaults` 메서드를 사용해서, 해당 파라미터의 기본값을 현재 요청 동안 항상 적용되도록 지정할 수 있습니다. 이 메서드는 현재 요청에 접근할 수 있으므로 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하는 것이 좋습니다:

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
     * 들어오는 요청을 처리합니다.
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

`locale` 파라미터에 대한 기본값이 설정되면, 이제 `route` 헬퍼로 URL을 생성할 때 더 이상 해당 값을 명시적으로 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값을 설정하면 Laravel의 암시적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어의 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 지정해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용해 달성할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
