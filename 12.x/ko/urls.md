# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [네임드 라우트용 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션용 URL](#urls-for-controller-actions)
- [유연한 URI 객체](#fluent-uri-objects)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 URL 생성을 도와주는 여러 헬퍼 함수들을 제공합니다. 이러한 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 만들거나, 다른 경로로 리다이렉트 응답을 생성할 때 유용하게 사용됩니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기

`url` 헬퍼를 사용하여 애플리케이션의 임의 URL을 생성할 수 있습니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스키마(HTTP 또는 HTTPS)와 호스트를 자동으로 사용합니다.

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 문자열 파라미터를 포함한 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다.

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로에 이미 존재하는 쿼리 문자열 파라미터에 대해 새로운 값을 제공하면, 기존 값이 덮어쓰기 됩니다.

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

값의 배열도 쿼리 파라미터로 전달할 수 있습니다. 배열로 전달된 값들은 생성된 URL에서 제대로 인코딩 처리됩니다.

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기

`url` 헬퍼에 경로를 제공하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 확인할 수 있습니다.

```php
// 쿼리 문자열을 제외한 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열을 포함한 현재 URL 가져오기...
echo url()->full();
```

위 메서드들은 `URL` [파사드](/docs/12.x/facades)를 통해서도 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="accessing-the-previous-url"></a>
#### 이전 URL 접근하기

사용자가 마지막으로 방문한 URL을 알아야 할 때도 있습니다. `url` 헬퍼의 `previous` 및 `previousPath` 메서드를 통해 이전 URL을 확인할 수 있습니다.

```php
// 이전 요청의 전체 URL 가져오기...
echo url()->previous();

// 이전 요청의 경로만 가져오기...
echo url()->previousPath();
```

또는, [세션](/docs/12.x/session)을 통해 [유연한 URI](#fluent-uri-objects) 인스턴스로 이전 URL을 얻을 수도 있습니다.

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});
```

또한, 세션을 통해 이전에 방문한 URL의 라우트 이름을 가져올 수도 있습니다.

```php
$previousRoute = $request->session()->previousRoute();
```

<a name="urls-for-named-routes"></a>
## 네임드 라우트용 URL (URLs for Named Routes)

`route` 헬퍼는 [네임드 라우트](/docs/12.x/routing#named-routes)로의 URL을 생성하는 데 사용할 수 있습니다. 네임드 라우트를 사용하면 실제 라우트에 정의된 URL에 의존하지 않고 URL을 생성할 수 있으므로, 라우트의 URL이 변경되어도 `route` 함수 호출 부분은 수정할 필요가 없습니다. 예를 들어, 아래와 같이 라우트를 정의했다고 가정해봅니다.

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

위 라우트로의 URL을 생성하려면, 다음과 같이 `route` 헬퍼를 사용할 수 있습니다.

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 개의 파라미터가 있는 라우트의 URL도 생성할 수 있습니다.

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트에 정의되지 않은 추가 배열 요소들은 쿼리 문자열로 URL에 추가됩니다.

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델

대부분의 경우 [Eloquent 모델](/docs/12.x/eloquent)의 경로 키(일반적으로 기본 키)를 사용하여 URL을 생성하게 됩니다. 따라서, Eloquent 모델 인스턴스를 파라미터 값으로 전달할 수 있으며, `route` 헬퍼는 모델의 경로 키를 자동으로 추출합니다.

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL

Laravel에서는 네임드 라우트로 "서명된" URL을 쉽게 만들 수 있습니다. 이런 URL에는 쿼리 문자열에 "signature" 해시가 추가되어, Laravel이 URL 생성 이후 수정되지 않았음을 검증할 수 있습니다. 서명된 URL은 외부 공개가 필요하지만 URL 변조에 대한 보호가 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 전송되는 공개 "구독 취소" 링크 구현 시 서명된 URL을 사용할 수 있습니다. 서명된 URL을 생성하려면, `URL` 파사드의 `signedRoute` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

서명된 URL 해시 생성에서 도메인을 제외하고 싶다면, `signedRoute` 메서드에 `absolute` 인수를 제공하세요.

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

특정 시간 이후 만료되는 임시 서명 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. 임시 서명 URL을 검증할 때 Laravel은 서명된 URL에 인코딩된 만료 타임스탬프가 아직 유효한지 확인합니다.

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증

들어오는 요청이 올바른 서명을 포함하는지 확인하려면, 들어온 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하세요.

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

애플리케이션의 프론트엔드에서 페이징 등으로 인해 추가 데이터를 서명 URL에 붙여야 할 수도 있습니다. 이럴 때는, `hasValidSignatureWhileIgnoring` 메서드를 사용해 검증 시 무시할 요청 쿼리 파라미터를 지정할 수 있습니다. 단, 무시된 파라미터는 누구든지 변경할 수 있습니다.

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

또한, 요청 인스턴스 대신 [미들웨어](/docs/12.x/middleware)를 라우트에 할당하는 방식으로도 서명 URL 검증이 가능합니다. `signed`(`Illuminate\Routing\Middleware\ValidateSignature`) 미들웨어는 유효하지 않은 서명 요청에 대해 자동으로 `403` HTTP 응답을 반환합니다.

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL 해시에 도메인이 포함되어 있지 않다면, 미들웨어에 `relative` 인수를 전달해야 합니다.

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 라우트에 대한 응답

누군가 만료된 서명 URL을 방문할 경우, 일반적으로 `403` HTTP 상태 코드용 에러 페이지가 표시됩니다. 그러나, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 사용자 정의 "render" 클로저를 정의함으로써 이 동작을 커스터마이즈할 수 있습니다.

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션용 URL (URLs for Controller Actions)

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다.

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 파라미터의 연관 배열을 전달할 수 있습니다.

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## 유연한 URI 객체 (Fluent URI Objects)

Laravel의 `Uri` 클래스는 URI를 객체로 생성 및 조작할 수 있는 편리하고 유연한 인터페이스를 제공합니다. 이 클래스는 League URI 패키지의 기능을 감싸면서 Laravel의 라우팅 시스템과도 자연스럽게 연동됩니다.

정적 메서드를 통해 간단하게 `Uri` 인스턴스를 생성할 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열로부터 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션으로부터 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청의 URL로부터 URI 인스턴스 생성...
$uri = $request->uri();

// 이전 요청의 URL로부터 URI 인스턴스 생성...
$uri = $request->session()->previousUri();
```

URI 인스턴스를 획득한 뒤에는 다음과 같이 메서드 체이닝 방식으로 값을 쉽게 수정할 수 있습니다.

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

유연한 URI 객체 사용법에 대한 자세한 내용은 [URI 문서](/docs/12.x/helpers#uri)를 참고하세요.

<a name="default-values"></a>
## 기본값 설정 (Default Values)

특정 URL 파라미터에 대해 요청 전체에서 적용할 기본값을 지정하고 싶을 때가 있습니다. 예를 들어, 많은 라우트에 `{locale}` 파라미터가 사용된다면,

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

매번 `route` 헬퍼를 호출할 때마다 `locale`을 전달하는 게 번거롭습니다. 이럴 때는 `URL::defaults` 메서드를 호출해 해당 파라미터의 기본값을 이번 요청에 대해 항상 적용할 수 있습니다. 보통 [라우트 미들웨어](/docs/12.x/middleware#assigning-middleware-to-routes) 안에서 현재 요청 객체에 접근 가능한 시점에 이 메서드를 호출하는 것이 좋습니다.

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

이처럼 `locale` 파라미터의 기본값을 설정하면, 이후부터는 `route` 헬퍼로 URL을 생성할 때 해당 값을 직접 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값을 설정하면 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서, URL 기본값을 설정하는 미들웨어가 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/12.x/middleware#sorting-middleware)를 조정하는 것이 좋습니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용해 설정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
