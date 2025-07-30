# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 개념](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트를 위한 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션을 위한 URL](#urls-for-controller-actions)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 URL을 생성할 때 도움을 주는 여러 헬퍼 함수를 제공합니다. 이 헬퍼들은 주로 템플릿이나 API 응답 내에서 링크를 만들거나 애플리케이션의 다른 부분으로 리다이렉트 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 개념 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 헬퍼는 애플리케이션의 임의 URL을 생성하는 데 사용됩니다. 생성된 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다:

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기 (Accessing The Current URL)

`url` 헬퍼에 경로가 제공되지 않을 경우, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 관한 정보를 얻을 수 있습니다:

```
// 쿼리 문자열 제외한 현재 URL 가져오기...
echo url()->current();

// 쿼리 문자열을 포함한 현재 URL 가져오기...
echo url()->full();

// 이전 요청의 전체 URL 가져오기...
echo url()->previous();
```

이 메서드들은 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트를 위한 URL (URLs For Named Routes)

`route` 헬퍼는 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)에 대한 URL을 생성할 때 사용합니다. 이름이 지정된 라우트를 통해 라우트에 실제 지정된 URL에 종속되지 않고 URL을 생성할 수 있습니다. 따라서 라우트 URL이 변경되더라도 `route` 함수 호출부는 변경할 필요가 없습니다. 예를 들어, 아래와 같이 라우트가 정의되어 있다고 가정합니다:

```
Route::get('/post/{post}', function (Post $post) {
    //
})->name('post.show');
```

이 라우트에 대한 URL을 생성하려면 `route` 헬퍼를 다음과 같이 사용할 수 있습니다:

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, 여러 인자를 가진 라우트에 대해서도 `route` 헬퍼를 사용할 수 있습니다:

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    //
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의에 포함되지 않은 추가 배열 요소들은 URL의 쿼리 문자열로 자동으로 추가됩니다:

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 (Eloquent Models)

라우트 키(일반적으로 기본 키)를 사용해 URL을 생성하는 경우가 많기 때문에, Eloquent 모델 인스턴스를 인수로 전달할 수 있습니다. `route` 헬퍼가 자동으로 모델의 라우트 키를 추출합니다:

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel에서는 이름이 지정된 라우트에 대해 쉽게 "서명된" URL을 생성할 수 있습니다. 이런 URL은 쿼리 문자열에 "서명" 해시가 추가되어 URL이 생성된 이후 변경되지 않았음을 Laravel이 검증할 수 있게 해줍니다. 서명된 URL은 공개적으로 접근 가능하지만 URL 조작으로부터 보호가 필요한 라우트에 매우 유용합니다.

예를 들어, 고객에게 이메일로 전송하는 공개 "구독 해지(unsubscribe)" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 서명된 URL을 만들려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

특정 시간 이후 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용합니다. Laravel은 서명된 URL에 내장된 만료 타임스탬프가 지나지 않았는지를 검증합니다:

```
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증 (Validating Signed Route Requests)

들어오는 요청이 유효한 서명을 갖고 있는지 확인하려면, `Request` 객체의 `hasValidSignature` 메서드를 호출하세요:

```
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

또는 `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/{{version}}/middleware)를 라우트에 할당할 수 있습니다. 이 미들웨어가 아직 HTTP 커널의 `routeMiddleware` 배열에 등록되지 않았다면, 다음과 같이 등록해야 합니다:

```
/**
 * 애플리케이션 라우트 미들웨어 목록
 *
 * 이 미들웨어들은 그룹에 할당하거나 개별적으로 사용할 수 있습니다.
 *
 * @var array
 */
protected $routeMiddleware = [
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
];
```

커널에 미들웨어 등록이 완료되면, 라우트에 이 미들웨어를 연결할 수 있습니다. 요청 내 서명이 유효하지 않으면 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 URL에 대한 처리 (Responding To Invalid Signed Routes)

만료된 서명 URL을 방문하면 기본적으로 `403` HTTP 상태 코드의 일반 오류 페이지가 표시됩니다. 하지만 예외 핸들러에 `InvalidSignatureException` 예외에 대한 커스텀 렌더러(closure)를 정의하여 이 동작을 변경할 수 있습니다. 이 렌더러는 HTTP 응답을 반환해야 합니다:

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

/**
 * 애플리케이션의 예외 처리 콜백 등록
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
## 컨트롤러 액션을 위한 URL (URLs For Controller Actions)

`action` 함수는 특정 컨트롤러 액션에 대한 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관 배열 형태의 파라미터 값을 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
## 기본값 설정 (Default Values)

애플리케이션에 따라 특정 URL 파라미터에 대한 요청 단위 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트가 `{locale}` 파라미터를 정의한다고 가정합시다:

```
Route::get('/{locale}/posts', function () {
    //
})->name('post.index');
```

매번 `route` 헬퍼를 호출할 때마다 `locale` 값을 넘기는 것은 번거롭습니다. 이때 `URL::defaults` 메서드를 사용하여 현재 요청 동안 항상 적용될 `locale` 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes) 내에서 호출하여 현재 요청에 접근할 수 있게 하는 것이 일반적입니다:

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\URL;

class SetDefaultLocaleForUrls
{
    /**
     * 들어오는 요청 처리
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

`locale` 파라미터 기본값이 설정되면, `route` 헬퍼를 사용해 URL을 생성할 때 더 이상 이 값을 명시적으로 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 실행 순서 (URL Defaults & Middleware Priority)

URL 기본값 설정은 Laravel의 암묵적 모델 바인딩 처리 과정에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 앞서 실행되도록 [미들웨어 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 지정하는 것이 좋습니다. 이를 위해 애플리케이션 HTTP 커널의 `$middlewarePriority` 속성에서 미들웨어 실행 순서를 조정할 수 있습니다.

`$middlewarePriority` 속성은 기본 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 해당 속성 정의를 복사해 애플리케이션의 HTTP 커널에서 덮어쓰면 수정할 수 있습니다:

```
/**
 * 우선순위에 따라 정렬된 미들웨어 목록
 *
 * 글로벌 미들웨어가 아닌 미들웨어들이 항상 이 순서대로 실행되도록 강제합니다.
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