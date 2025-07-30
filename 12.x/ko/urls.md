# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션을 위한 URL](#urls-for-controller-actions)
- [Fluent URI 객체](#fluent-uri-objects)
- [기본값](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 URL 생성을 돕는 여러 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿과 API 응답에서 링크를 생성하거나 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼는 애플리케이션의 임의 URL을 생성하는 데 사용할 수 있습니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 문자열 매개변수를 포함한 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로에 이미 존재하는 쿼리 문자열 매개변수를 제공하면 기존 값이 덮어써집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

값의 배열도 쿼리 매개변수로 전달할 수 있습니다. 이 값들은 생성되는 URL에서 적절하게 키가 지정되고 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing the Current URL)

`url` 헬퍼에 경로를 전달하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 관한 정보를 얻을 수 있습니다:

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

이 메서드들은 `URL` [파사드](/docs/12.x/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL (URLs for Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)의 URL을 생성할 때 사용합니다. 이름이 지정된 라우트를 사용하면 라우트에 정의된 실제 URL에 독립적으로 URL을 생성할 수 있습니다. 따라서 라우트 URL이 변경되어도 `route` 함수 호출을 수정할 필요가 없습니다. 예를 들어, 다음과 같이 정의된 라우트가 있다고 가정해봅니다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트의 URL을 생성하려면 `route` 헬퍼를 다음과 같이 사용할 수 있습니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 매개변수를 갖는 라우트의 URL 생성에도 사용할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의 매개변수와 일치하지 않는 추가 배열 요소는 URL 쿼리 문자열에 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

종종 [Eloquent 모델](/docs/12.x/eloquent)의 라우트 키(보통 기본키)를 사용해 URL을 생성합니다. 그래서 `route` 헬퍼에 Eloquent 모델 인스턴스를 직접 전달할 수 있습니다. 그러면 `route` 헬퍼가 자동으로 모델의 라우트 키를 추출합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 이름이 지정된 라우트에 쉽게 "서명된" URL을 생성할 수 있게 합니다. 이러한 URL들은 쿼리 문자열에 "서명(signature)" 해시가 추가되어 있어 Laravel이 URL이 생성된 이후에 변경되지 않았음을 검증할 수 있습니다. 서명된 URL은 공개적으로 접근 가능하지만 URL 조작에 대한 보호가 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 보내는 공개 "구독 해지(unsubscribe)" 링크에 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

`absolute` 인수를 `false`로 전달하면 도메인을 서명 URL 해시에 포함하지 않을 수 있습니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 시간 후에 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하세요. Laravel은 임시 서명 URL의 만료 타임스탬프가 아직 경과되지 않았는지 검증합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증하기 (Validating Signed Route Requests)

들어오는 요청에 유효한 서명이 포함되어 있는지 확인하려면, `Illuminate\Http\Request` 인스턴스의 `hasValidSignature` 메서드를 호출하세요:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때로는 클라이언트 측 페이지네이션처럼 프론트엔드에서 서명된 URL에 쿼리 데이터를 추가할 필요가 있습니다. 이 경우 `hasValidSignatureWhileIgnoring` 메서드를 사용해 검증 시 무시할 쿼리 매개변수를 지정할 수 있습니다. 단, 무시된 매개변수는 누구나 수정할 수 있음을 유념하세요:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 사용하지 않고 서명된 URL 검증을 하려면, 해당 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/12.x/middleware)를 할당할 수 있습니다. 요청에 유효한 서명이 없으면 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명이 URL 해시에 도메인을 포함하지 않은 경우, 미들웨어에 `relative` 인수를 전달하세요:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 URL에 대한 응답 (Responding to Invalid Signed Routes)

서명된 URL이 만료된 경우 방문자는 기본 `403` HTTP 오류 페이지를 받게 됩니다. 이를 사용자 맞춤화하려면 앱의 `bootstrap/app.php` 파일에 `InvalidSignatureException` 예외용 커스텀 "render" 클로저를 정의할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션을 위한 URL (URLs for Controller Actions)

`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 매개변수를 받으면, 두 번째 인수로 연관 배열 형태의 매개변수를 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## Fluent URI 객체 (Fluent URI Objects)

Laravel의 `Uri` 클래스는 URI를 객체로 생성하고 조작할 수 있게 하는 편리하고 유창한 인터페이스를 제공합니다. 이 클래스는 League URI 패키지의 기능을 래핑하며 Laravel 라우팅 시스템과 원활하게 통합됩니다.

정적 메서드를 사용해 쉽게 `Uri` 인스턴스를 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열에서 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 이름이 지정된 라우트, 컨트롤러 액션으로 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

한 번 URI 인스턴스를 생성하면 다음과 같이 유창하게 수정할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

Fluent URI 객체 사용법에 관한 더 자세한 내용은 [URI 문서](/docs/12.x/helpers#uri)를 참고하세요.

<a name="default-values"></a>
## 기본값 (Default Values)

특정 URL 매개변수에 대해 요청 범위의 기본값을 지정하고 싶을 수도 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 매개변수를 정의한다고 가정해봅니다:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

매번 `route` 헬퍼를 호출할 때마다 `locale`을 매개변수로 전달하는 것은 번거롭습니다. 이럴 때 `URL::defaults` 메서드를 사용해 현재 요청 중 항상 적용할 기본값을 지정할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/12.x/middleware#assigning-middleware-to-routes) 내에서 호출해 현재 요청에 접근할 수 있습니다:

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

`locale` 매개변수에 대한 기본값이 한 번 설정되면 `route` 헬퍼로 URL을 생성할 때 더 이상 값을 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위 (URL Defaults and Middleware Priority)

URL 기본값 설정은 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [우선순위](/docs/12.x/middleware#sorting-middleware)를 조정해야 합니다. 이를 앱의 `bootstrap/app.php` 파일에 있는 `priority` 미들웨어 메서드를 통해 수행할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```