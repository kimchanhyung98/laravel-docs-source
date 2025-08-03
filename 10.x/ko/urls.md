# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [기본 값](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에서 URL을 생성하는 데 도움이 되는 여러 헬퍼(helper) 함수를 제공합니다. 이러한 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 생성하거나, 애플리케이션 내 다른 부분으로 리디렉션 응답을 생성할 때 유용하게 사용됩니다.

<a name="the-basics"></a>
## 기본 사항 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼는 애플리케이션을 위한 임의의 URL을 생성하는 데 사용할 수 있습니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS) 및 호스트를 자동으로 사용합니다:

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing the Current URL)

`url` 헬퍼에 경로를 제공하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어, 현재 URL에 관한 정보를 얻을 수 있습니다:

```
// 쿼리 문자열 제외한 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열 포함한 현재 URL 가져오기...
echo url()->full();

// 이전 요청의 전체 URL 가져오기...
echo url()->previous();
```

이러한 메서드들은 `URL` [파사드](/docs/10.x/facades)를 통해서도 접근할 수 있습니다:

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL (URLs for Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/10.x/routing#named-routes)로의 URL을 생성할 때 사용됩니다. 이름이 지정된 라우트를 사용하면 라우트에 실제 정의된 URL에 의존하지 않고도 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되어도 `route` 함수 호출을 수정할 필요가 없습니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다고 가정해 보겠습니다:

```
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

이 라우트의 URL을 생성하려면 `route` 헬퍼를 다음과 같이 사용할 수 있습니다:

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 헬퍼는 여러 파라미터를 가진 라우트의 URL 생성에도 사용할 수 있습니다:

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의 파라미터와 일치하지 않는 추가 배열 요소는 URL의 쿼리 문자열에 추가됩니다:

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

주로 [Eloquent 모델](/docs/10.x/eloquent)의 라우트 키(일반적으로 기본 키)를 사용해 URL을 생성합니다. 따라서 파라미터 값으로 Eloquent 모델을 전달할 수 있으며, `route` 헬퍼가 자동으로 모델의 라우트 키를 추출합니다:

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel은 이름이 지정된 라우트에 대해 "서명된" URL을 쉽게 생성할 수 있도록 지원합니다. 이러한 URL에는 쿼리 문자열에 "서명" 해시가 추가되며, Laravel은 URL 생성 후 변경되었는지 여부를 검증합니다. 서명된 URL은 공개 접근이 가능한 라우트지만 URL 조작에 대한 보호가 필요한 경우에 유용합니다.

예를 들어, 이메일로 고객에게 공개되는 "구독 취소" 링크에 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 대해 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

서명된 URL 해시에 도메인을 제외하고 싶다면 `signedRoute` 메서드에 `absolute` 인수를 `false`로 제공하면 됩니다:

```
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

지정된 시간 후 만료되는 임시 서명된 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용하세요. Laravel은 서명된 URL에 포함된 만료 타임스탬프가 지나지 않았는지 검증합니다:

```
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증하기 (Validating Signed Route Requests)

들어오는 요청이 유효한 서명을 갖는지 확인하려면, `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

때때로 프론트엔드에서 페이징 등 클라이언트 측 URL 조작을 허용해야 할 수 있으므로, 검증 시 무시할 쿼리 파라미터를 `hasValidSignatureWhileIgnoring` 메서드를 통해 지정할 수 있습니다. 단, 무시하는 파라미터는 누구나 요청에서 수정할 수 있다는 점을 유념하세요:

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

들어오는 요청 인스턴스를 사용해 서명된 URL을 검증하는 대신, `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/10.x/middleware)를 라우트에 할당할 수도 있습니다. 해당 미들웨어가 아직 등록되지 않았다면, HTTP 커널의 `$middlewareAliases` 배열에 별칭으로 등록할 수 있습니다:

```
/**
 * 애플리케이션의 미들웨어 별칭들
 *
 * 별칭을 이용해 라우트 및 그룹에 편리하게 미들웨어를 할당할 수 있습니다.
 *
 * @var array<string, class-string|string>
 */
protected $middlewareAliases = [
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
];
```

커널에 미들웨어를 등록한 후, 라우트에 미들웨어를 붙일 수 있습니다. 요청이 유효한 서명을 포함하지 않으면 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL이 해시에 도메인을 포함하지 않는다면, 미들웨어에 `relative` 인수를 제공해야 합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명된 URL 대응하기 (Responding to Invalid Signed Routes)

서명된 URL이 만료된 경우 접속하면 기본적으로 `403` HTTP 상태 코드의 일반 오류 페이지가 표시됩니다. 그러나 예외 처리기에서 `InvalidSignatureException` 예외에 대한 커스텀 "렌더러블(renderable)" 클로저를 정의하여 이 동작을 맞춤화할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다:

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

/**
 * 애플리케이션 예외 핸들링 콜백 등록
 */
public function register(): void
{
    $this->renderable(function (InvalidSignatureException $e) {
        return response()->view('error.link-expired', [], 403);
    });
}
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL (URLs for Controller Actions)

`action` 함수는 주어진 컨트롤러 액션의 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받으면 두 번째 인수로 연관 배열의 라우트 파라미터를 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본 값 (Default Values)

일부 애플리케이션에서는 특정 URL 파라미터의 요청 전역 기본값을 지정하고 싶을 수 있습니다. 예컨대, 많은 라우트에 `{locale}` 파라미터가 정의되어 있다고 가정합시다:

```
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

`route` 헬퍼를 호출할 때마다 `locale` 값을 반복해서 전달하는 것은 번거롭습니다. 이럴 때 `URL::defaults` 메서드를 사용해 현재 요청 동안 항상 적용될 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/10.x/middleware#assigning-middleware-to-routes)에서 호출하면 현재 요청에 접근할 수 있어 유용합니다:

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

`locale` 파라미터의 기본값이 설정되면, `route` 헬퍼로 URL을 생성할 때 더 이상 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본 값과 미들웨어 실행 순서 (URL Defaults and Middleware Priority)

URL 기본 값 설정은 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본 값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/10.x/middleware#sorting-middleware)를 지정해야 합니다. 이는 애플리케이션 HTTP 커널의 `$middlewarePriority` 속성에서 해당 미들웨어가 `SubstituteBindings` 미들웨어 앞에 오도록 배열 순서를 조정하여 가능합니다.

`$middlewarePriority` 속성은 기본 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 해당 클래스에서 정의를 복사해 애플리케이션 HTTP 커널에서 덮어써서 수정할 수 있습니다:

```
/**
 * 우선순위에 따라 정렬된 미들웨어 목록
 *
 * 비전역 미들웨어의 실행 순서를 강제합니다.
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