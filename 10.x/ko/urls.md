# URL 생성

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [네임드 라우트용 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션용 URL](#urls-for-controller-actions)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 URL을 생성하는 데 도움이 되는 여러 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 생성하거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항

<a name="generating-urls"></a>
### URL 생성하기

`url` 헬퍼를 사용하여 애플리케이션의 임의의 URL을 생성할 수 있습니다. 생성된 URL은 현재 처리 중인 요청의 스키마(HTTP 또는 HTTPS)와 호스트를 자동으로 사용합니다.

    $post = App\Models\Post::find(1);

    echo url("/posts/{$post->id}");

    // http://example.com/posts/1

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기

`url` 헬퍼에 경로를 제공하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 얻을 수 있습니다.

    // 쿼리 스트링을 제외한 현재 URL을 가져옵니다...
    echo url()->current();

    // 쿼리 스트링을 포함한 현재 URL을 가져옵니다...
    echo url()->full();

    // 이전 요청의 전체 URL을 가져옵니다...
    echo url()->previous();

이 메서드들은 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

    use Illuminate\Support\Facades\URL;

    echo URL::current();

<a name="urls-for-named-routes"></a>
## 네임드 라우트용 URL

`route` 헬퍼를 사용하여 [네임드 라우트](/docs/{{version}}/routing#named-routes)의 URL을 생성할 수 있습니다. 네임드 라우트를 사용하면 실제 라우트에 정의된 URL에 종속되지 않고 URL을 생성할 수 있으므로, 라우트의 URL이 변경되어도 `route` 함수 호출은 수정할 필요가 없습니다. 예를 들어 애플리케이션에 다음과 같이 라우트가 정의되어 있다고 상상해 보세요.

    Route::get('/post/{post}', function (Post $post) {
        // ...
    })->name('post.show');

이 라우트의 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다.

    echo route('post.show', ['post' => 1]);

    // http://example.com/post/1

물론, `route` 헬퍼를 사용해 파라미터가 여러 개인 라우트의 URL도 생성할 수 있습니다.

    Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
        // ...
    })->name('comment.show');

    echo route('comment.show', ['post' => 1, 'comment' => 3]);

    // http://example.com/post/1/comment/3

라우트 정의에 해당하지 않는 추가적인 배열 요소들은 URL의 쿼리 스트링으로 추가됩니다.

    echo route('post.show', ['post' => 1, 'search' => 'rocket']);

    // http://example.com/post/1?search=rocket

<a name="eloquent-models"></a>
#### Eloquent 모델

[Eloquent 모델](/docs/{{version}}/eloquent)의 라우트 키(일반적으로 기본키)를 사용해 URL을 생성하는 경우가 많으므로, 파라미터 값에 Eloquent 모델을 직접 전달할 수 있습니다. `route` 헬퍼는 모델의 라우트 키를 자동으로 추출합니다.

    echo route('post.show', ['post' => $post]);

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 네임드 라우트에 "서명된" URL을 쉽게 생성할 수 있도록 도와줍니다. 이러한 URL은 쿼리 스트링에 "signature" 해시가 추가되어, 생성 이후 URL이 변경되지 않았음을 Laravel에서 검증할 수 있게 해줍니다. 서명된 URL은 공개적으로 접근 가능한 라우트지만 URL 변조에 대한 추가 보호 계층이 필요한 경우에 유용합니다.

예를 들어, 고객에게 메일로 발송하는 공개 "구독 해지" 링크에 서명된 URL을 사용할 수 있습니다. 네임드 라우트의 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요.

    use Illuminate\Support\Facades\URL;

    return URL::signedRoute('unsubscribe', ['user' => 1]);

서명된 URL 해시에서 도메인을 제외하려면 `signedRoute` 메서드에 `absolute` 인자를 전달하세요.

    return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);

지정된 시간이 지나면 만료되는 임시 서명 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel은 임시 서명 라우트 URL을 검증할 때, 서명된 URL에 인코딩된 만료 시간이 지나지 않았는지 확인합니다.

    use Illuminate\Support\Facades\URL;

    return URL::temporarySignedRoute(
        'unsubscribe', now()->addMinutes(30), ['user' => 1]
    );

<a name="validating-signed-route-requests"></a>
#### 서명 라우트 요청 검증

들어오는 요청이 올바른 서명을 가지고 있는지 확인하려면, 전달받은 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하면 됩니다.

    use Illuminate\Http\Request;

    Route::get('/unsubscribe/{user}', function (Request $request) {
        if (! $request->hasValidSignature()) {
            abort(401);
        }

        // ...
    })->name('unsubscribe');

경우에 따라, 예를 들면 클라이언트 사이드 페이지네이션 등으로 서명된 URL에 프론트엔드에서 데이터를 추가해야 할 수도 있습니다. 그럴 땐, `hasValidSignatureWhileIgnoring` 메서드를 이용해 검증 시 무시해야 하는 쿼리 파라미터를 지정할 수 있습니다. 파라미터를 무시하면 누구나 해당 값을 수정할 수 있으므로 주의해야 합니다.

    if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
        abort(401);
    }

요청 인스턴스로 서명된 URL을 검증하는 대신, 해당 라우트에 `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/{{version}}/middleware)를 지정할 수도 있습니다. 만약 등록되어 있지 않다면, HTTP 커널의 `$middlewareAliases` 배열에 별칭을 지정할 수 있습니다.

    /**
     * 애플리케이션의 미들웨어 별칭.
     *
     * 별칭은 라우트와 그룹에 미들웨어를 편리하게 지정할 때 사용됩니다.
     *
     * @var array<string, class-string|string>
     */
    protected $middlewareAliases = [
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    ];

커널에 미들웨어가 등록되면, 해당 미들웨어를 라우트에 지정할 수 있습니다. 올바른 서명이 없는 경우, 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다.

    Route::post('/unsubscribe/{user}', function (Request $request) {
        // ...
    })->name('unsubscribe')->middleware('signed');

서명된 URL이 해시에 도메인을 포함하지 않는 경우, 미들웨어에 `relative` 인자를 전달해야 합니다.

    Route::post('/unsubscribe/{user}', function (Request $request) {
        // ...
    })->name('unsubscribe')->middleware('signed:relative');

<a name="responding-to-invalid-signed-routes"></a>
#### 잘못된 서명 라우트에 대한 응답 처리

누군가 만료된 서명 URL에 접근하면, 일반적인 `403` HTTP 상태 코드의 에러 페이지를 받게 됩니다. 하지만 예외 처리기에서 `InvalidSignatureException` 예외에 대해 커스텀 "렌더러블" 클로저를 정의하여 원하는 형태로 동작을 변경할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다.

    use Illuminate\Routing\Exceptions\InvalidSignatureException;

    /**
     * 애플리케이션의 예외 처리를 등록합니다.
     */
    public function register(): void
    {
        $this->renderable(function (InvalidSignatureException $e) {
            return response()->view('error.link-expired', [], 403);
        });
    }

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션용 URL

`action` 함수는 지정한 컨트롤러 액션에 해당하는 URL을 생성합니다.

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인자로 파라미터의 연관 배열을 전달할 수 있습니다.

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="default-values"></a>
## 기본값 설정

어떤 애플리케이션에서는 특정 URL 파라미터의 기본값을 애플리케이션 전체 요청에 대해 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 파라미터가 정의되어 있다고 가정해 봅시다.

    Route::get('/{locale}/posts', function () {
        // ...
    })->name('post.index');

URL을 생성할 때마다 `locale` 값을 일일이 넘기기는 번거로울 수 있습니다. 이럴 땐, `URL::defaults` 메서드를 사용해서 해당 파라미터의 기본값을 현재 요청 동안 항상 적용되도록 지정할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하여 현재 요청에 접근하는 것이 좋습니다.

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\URL;
    use Symfony\Component\HttpFoundation\Response;

    class SetDefaultLocaleForUrls
    {
        /**
         * 요청을 처리합니다.
         *
         * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
         */
        public function handle(Request $request, Closure $next): Response
        {
            URL::defaults(['locale' => $request->user()->locale]);

            return $next($request);
        }
    }

`locale` 파라미터의 기본값이 지정되면, `route` 헬퍼를 통해 URL을 생성할 때 더 이상 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값을 설정하면 Laravel의 암시적 모델 바인딩 처리와 충돌이 발생할 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel 자체의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어의 실행 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 지정하는 것이 좋습니다. 이는 애플리케이션의 HTTP 커널에 있는 `$middlewarePriority` 속성에서 미들웨어 순서를 조정하여 할 수 있습니다.

`$middlewarePriority` 속성은 기본적으로 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 애플리케이션의 HTTP 커널에서 이 속성을 복사해 수정할 수 있습니다.

    /**
     * 우선순위가 지정된 미들웨어 목록.
     *
     * 이 속성은 비 전역 미들웨어도 항상 지정된 순서로 실행되게 합니다.
     *
     * @var array
     */
    protected $middlewarePriority = [
        // ...
         \App\Http\Middleware\SetDefaultLocaleForUrls::class,
         \Illuminate\Routing\Middleware\SubstituteBindings::class,
         // ...
    ];