# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [명명된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [플루언트 URI 객체](#fluent-uri-objects)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 URL을 생성하는 데 도움이 되는 다양한 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 생성하거나, 애플리케이션 내 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성 (Generating URLs)

`url` 헬퍼를 사용하여 임의의 URL을 생성할 수 있습니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다.

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 스트링 파라미터가 포함된 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로 내에 이미 존재하는 쿼리 파라미터가 있을 경우, 새로 전달한 값으로 기존 값이 덮어써집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

배열 형태의 값을 쿼리 파라미터로 전달할 수도 있습니다. 이런 값들은 생성된 URL에서 적절하게 키/값으로 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing the Current URL)

`url` 헬퍼에 경로를 지정하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되며, 이를 통해 현재 URL 정보를 얻을 수 있습니다:

```php
// 쿼리 스트링 없이 현재 URL을 가져옵니다...
echo url()->current();

// 쿼리 스트링을 포함한 현재 URL을 가져옵니다...
echo url()->full();

// 이전 요청의 전체 URL을 가져옵니다...
echo url()->previous();

// 이전 요청의 경로만 가져옵니다...
echo url()->previousPath();
```

이러한 메서드들은 `URL` [파사드](/docs/12.x/facades)를 통해서도 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 명명된 라우트의 URL (URLs for Named Routes)

`route` 헬퍼는 [명명된 라우트](/docs/12.x/routing#named-routes)의 URL을 생성할 때 사용할 수 있습니다. 명명된 라우트를 사용하면 실제 라우트에 정의된 URL에 의존하지 않고 URL을 생성할 수 있으므로, 라우트의 URL이 변경되어도 `route` 함수 호출 부분은 수정할 필요가 없습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해봅시다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트로의 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 파라미터가 필요한 라우트의 URL을 생성할 때도 사용할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의에 없는 추가 배열 요소들은 URL의 쿼리 스트링으로 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델

대부분의 경우, [Eloquent 모델](/docs/12.x/eloquent)의 라우트 키(보통 기본 키)를 사용해 URL을 생성하게 됩니다. 이 때문에, Eloquent 모델을 라우트 파라미터 값으로 그대로 전달할 수 있습니다. `route` 헬퍼는 자동으로 모델의 라우트 키를 추출하여 사용합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 명명된 라우트에 대해 손쉽게 "서명(signed)"된 URL을 생성할 수 있게 해줍니다. 이러한 URL은 쿼리 스트링에 "signature" 해시가 추가되어, 해당 URL이 생성된 이후로 변경되지 않았음을 Laravel이 검증할 수 있도록 합니다. 서명된 URL은 외부에 공개적으로 접근 가능하지만, URL 조작에서 보호가 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 발송되는 공개 "구독 해지" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 명명된 라우트로 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

`signedRoute` 메서드에 `absolute` 인수를 전달하여 서명 URL 해시 계산 시 도메인을 제외할 수도 있습니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 시간 이후 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. 만료 시간을 인코딩하여, 유효성 검증 시 만료되지 않았는지 확인합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청의 유효성 검증

들어오는 요청이 올바른 서명을 가지고 있는지 검증하려면, `Illuminate\Http\Request` 인스턴스의 `hasValidSignature` 메서드를 호출하세요:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때로는 프런트엔드에서 페이지네이션 등과 같이 데이터 추가를 위해 서명된 URL에 파라미터를 추가해야 할 수도 있습니다. 이때는 `hasValidSignatureWhileIgnoring` 메서드를 사용하여, 검증에서 무시할 쿼리 파라미터를 지정할 수 있습니다. 물론, 무시하게 한 파라미터는 누구나 값 수정이 가능합니다:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

요청 인스턴스를 직접 사용하여 서명을 검증하는 대신, 해당 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/12.x/middleware)를 지정할 수도 있습니다. 올바른 서명이 없는 요청이 들어오면, 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL에 도메인이 해시에 포함되어 있지 않다면, 미들웨어에 `relative` 인수를 추가해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명된 라우트への 응답

만료된 서명 URL에 접속하면 기본적으로 `403` HTTP 상태 코드의 일반 에러 페이지가 표시됩니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 커스텀 "렌더" 클로저를 정의하여 이 동작을 사용자 정의할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL (URLs for Controller Actions)

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관 배열 형태의 라우트 파라미터를 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## 플루언트 URI 객체 (Fluent URI Objects)

Laravel의 `Uri` 클래스는 객체 지향적이면서도 유연하게 URI를 생성·조작할 수 있는 편리한 플루언트 인터페이스를 제공합니다. 이 클래스는 League URI 패키지의 기능을 감싸고 있으며, Laravel의 라우팅 시스템과 완벽하게 통합됩니다.

정적 메서드를 통해 쉽게 `Uri` 인스턴스를 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열로 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 명명된 라우트, 컨트롤러 액션 등으로 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL로 URI 인스턴스 생성...
$uri = $request->uri();
```

URI 인스턴스가 준비되면, 아래처럼 연속적으로 조작할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

플루언트 URI 객체 활용에 대한 더 자세한 정보는 [URI 문서](/docs/12.x/helpers#uri)를 참고하세요.

<a name="default-values"></a>
## 기본값 설정 (Default Values)

일부 애플리케이션에서는 특정 URL 파라미터에 대해 요청 전체에서 사용될 기본값을 설정하고 싶을 수 있습니다. 예를 들어, 라우트에 `{locale}` 파라미터가 자주 사용된다면:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

`route` 헬퍼를 사용할 때마다 항상 `locale`을 전달하는 것은 불편합니다. 이런 경우, `URL::defaults` 메서드를 이용하여 해당 파라미터의 기본값을 현재 요청에 대해 항상 적용되도록 설정할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/12.x/middleware#assigning-middleware-to-routes)에서 호출하는 것이 일반적이며, 현재 요청 객체를 사용할 수 있습니다:

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
     * Handle an incoming request.
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

`locale` 파라미터에 대한 기본값이 한 번 설정되면, 이후부터는 `route` 헬퍼로 URL을 생성할 때 별도로 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값 설정은 Laravel의 암묵적(implicit) 모델 바인딩 동작과 충돌을 일으킬 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어를, Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/12.x/middleware#sorting-middleware)를 조정해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 활용하여 다음과 같이 할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```