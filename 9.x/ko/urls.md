# URL 생성

- [소개](#introduction)
- [기본 사용법](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 접근하기](#accessing-the-current-url)
- [이름이 지정된 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에서 URL을 생성하는 데 도움을 주는 다양한 헬퍼를 제공합니다. 이러한 헬퍼는 주로 템플릿이나 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사용법

<a name="generating-urls"></a>
### URL 생성하기

`url` 헬퍼를 사용하여 애플리케이션의 임의의 URL을 생성할 수 있습니다. 생성된 URL은 자동으로 현재 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 사용합니다:

    $post = App\Models\Post::find(1);

    echo url("/posts/{$post->id}");

    // http://example.com/posts/1

<a name="accessing-the-current-url"></a>
### 현재 URL 접근하기

`url` 헬퍼에 경로를 제공하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되며, 이를 통해 현재 URL에 대한 정보를 얻을 수 있습니다:

    // 쿼리 문자열을 제외한 현재 URL을 가져옵니다...
    echo url()->current();

    // 쿼리 문자열을 포함한 현재 URL을 가져옵니다...
    echo url()->full();

    // 이전 요청의 전체 URL을 가져옵니다...
    echo url()->previous();

이러한 메서드는 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

    use Illuminate\Support\Facades\URL;

    echo URL::current();

<a name="urls-for-named-routes"></a>
## 이름이 지정된 라우트의 URL

`route` 헬퍼를 사용하면 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)의 URL을 생성할 수 있습니다. 이름이 지정된 라우트를 사용하면 실제 라우트의 URL에 의존하지 않고 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되어도 `route` 함수 호출 부분을 변경할 필요가 없습니다. 예를 들어, 애플리케이션에 다음과 같이 정의된 라우트가 있다고 가정해보겠습니다:

    Route::get('/post/{post}', function (Post $post) {
        //
    })->name('post.show');

이 라우트의 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용하면 됩니다:

    echo route('post.show', ['post' => 1]);

    // http://example.com/post/1

물론, `route` 헬퍼는 여러 개의 파라미터를 가진 라우트의 URL도 생성할 수 있습니다:

    Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
        //
    })->name('comment.show');

    echo route('comment.show', ['post' => 1, 'comment' => 3]);

    // http://example.com/post/1/comment/3

라우트 정의의 파라미터에 대응하지 않는 추가 배열 요소는 URL 쿼리 문자열로 추가됩니다:

    echo route('post.show', ['post' => 1, 'search' => 'rocket']);

    // http://example.com/post/1?search=rocket

<a name="eloquent-models"></a>
#### 엘로퀀트 모델

대부분의 경우, [엘로퀀트 모델](/docs/{{version}}/eloquent)의 라우트 키(일반적으로 기본 키)를 사용하여 URL을 생성하게 됩니다. 그래서 엘로퀀트 모델을 파라미터 값으로 바로 전달할 수 있습니다. `route` 헬퍼는 모델의 라우트 키를 자동으로 추출합니다:

    echo route('post.show', ['post' => $post]);

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 이름이 지정된 라우트에 대해 "서명된" URL을 쉽게 생성할 수 있도록 해줍니다. 이러한 URL에는 쿼리 문자열에 "서명" 해시가 추가되어, URL이 생성된 이후로 수정되지 않았는지 Laravel이 검증할 수 있습니다. 서명된 URL은 공개적으로 접근 가능한 라우트이면서도 URL 변조로부터 보호가 필요한 경우에 특히 유용합니다.

예를 들어, 고객에게 이메일로 발송되는 공개 "구독 해지" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 대한 서명된 URL을 생성하려면, `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

    use Illuminate\Support\Facades\URL;

    return URL::signedRoute('unsubscribe', ['user' => 1]);

특정 시간 이후 만료되는 임시 서명 라우트 URL을 생성하고 싶다면, `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel이 임시 서명 라우트 URL을 검증할 때는, 서명된 URL에 인코딩된 만료 타임스탬프가 아직 지나지 않았는지 확인합니다:

    use Illuminate\Support\Facades\URL;

    return URL::temporarySignedRoute(
        'unsubscribe', now()->addMinutes(30), ['user' => 1]
    );

<a name="validating-signed-route-requests"></a>
#### 서명 라우트 요청 검증

들어오는 요청에 유효한 서명이 있는지 확인하려면, 해당 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출해야 합니다:

    use Illuminate\Http\Request;

    Route::get('/unsubscribe/{user}', function (Request $request) {
        if (! $request->hasValidSignature()) {
            abort(401);
        }

        // ...
    })->name('unsubscribe');

경우에 따라, 애플리케이션의 프론트엔드에서 페이징 등으로 서명된 URL에 데이터를 추가해야 할 수 있습니다. 이럴 때는, `hasValidSignatureWhileIgnoring` 메서드를 사용하여, 서명된 URL을 검증할 때 무시할 쿼리 파라미터를 지정할 수 있습니다. 파라미터를 무시하면, 누구나 해당 파라미터를 수정할 수 있다는 점을 유의하세요:

    if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
        abort(401);
    }

들어오는 요청 인스턴스로 서명된 URL을 검증하는 대신, 해당 라우트에 `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/{{version}}/middleware)를 지정할 수도 있습니다. 이 미들웨어가 아직 없으면, HTTP 커널의 `routeMiddleware` 배열에 키를 할당해야 합니다:

    /**
     * 애플리케이션의 라우트 미들웨어.
     *
     * 이 미들웨어들은 그룹에 할당되거나 개별적으로 사용할 수 있습니다.
     *
     * @var array
     */
    protected $routeMiddleware = [
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    ];

커널에서 미들웨어를 등록했다면, 라우트에 연결할 수 있습니다. 유효한 서명이 없는 요청이 들어오면, 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

    Route::post('/unsubscribe/{user}', function (Request $request) {
        // ...
    })->name('unsubscribe')->middleware('signed');

<a name="responding-to-invalid-signed-routes"></a>
#### 만료된 서명 라우트에 대한 응답

누군가 만료된 서명 URL에 접근하면, `403` HTTP 상태 코드의 일반적인 오류 페이지를 받게 됩니다. 하지만, `InvalidSignatureException` 예외에 대해 커스텀 "렌더러블" 클로저를 예외 핸들러에 정의하여 이 동작을 맞춤화할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다:

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

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL

`action` 함수는 지정한 컨트롤러 액션의 URL을 생성합니다:

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

컨트롤러 메서드가 라우트 파라미터를 받는다면, 두 번째 인자로 파라미터의 연관 배열을 전달할 수 있습니다:

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="default-values"></a>
## 기본값 설정

일부 애플리케이션에서는 특정 URL 파라미터에 대해 전체 요청에 적용되는 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트가 `{locale}` 파라미터를 정의한다고 가정해봅시다:

    Route::get('/{locale}/posts', function () {
        //
    })->name('post.index');

`route` 헬퍼를 호출할 때마다 매번 `locale`을 전달하는 것은 번거롭습니다. 따라서 `URL::defaults` 메서드를 사용하여 해당 파라미터의 기본값을 현재 요청 동안 항상 적용되도록 할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하여 현재 요청에 접근하는 것이 좋습니다:

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Support\Facades\URL;

    class SetDefaultLocaleForUrls
    {
        /**
         * 들어오는 요청을 처리합니다.
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

`locale` 파라미터의 기본값이 설정되면, 이제 `route` 헬퍼로 URL을 생성할 때 값을 따로 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값 & 미들웨어 우선순위

URL 기본값을 설정하면, Laravel의 암시적(Implicit) 모델 바인딩 처리와 충돌할 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 지정해야 합니다. 이를 위해 애플리케이션 HTTP 커널 내의 `$middlewarePriority` 속성에서 해당 미들웨어가 `SubstituteBindings` 미들웨어보다 먼저 위치하도록 해야 합니다.

`$middlewarePriority` 속성은 기본 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 그 정의를 복사하여 애플리케이션의 HTTP 커널에서 덮어쓸 수 있습니다:

    /**
     * 우선순위가 적용된 미들웨어 목록입니다.
     *
     * 이 설정은 글로벌이 아닌 미들웨어의 순서를 강제합니다.
     *
     * @var array
     */
    protected $middlewarePriority = [
        // ...
         \App\Http\Middleware\SetDefaultLocaleForUrls::class,
         \Illuminate\Routing\Middleware\SubstituteBindings::class,
         // ...
    ];