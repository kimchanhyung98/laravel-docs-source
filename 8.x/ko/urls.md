# URL 생성

- [소개](#introduction)
- [기본 사항](#the-basics)
    - [URL 생성](#generating-urls)
    - [현재 URL 접근](#accessing-the-current-url)
- [이름 있는 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [기본 값](#default-values)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에서 URL을 생성하는 데 도움이 되는 다양한 헬퍼를 제공합니다. 이러한 헬퍼들은 주로 템플릿과 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리다이렉트 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사항

<a name="generating-urls"></a>
### URL 생성

`url` 헬퍼를 사용하여 애플리케이션의 임의의 URL을 생성할 수 있습니다. 생성된 URL은 현재 요청에서 사용 중인 스키마(HTTP 또는 HTTPS)와 호스트를 자동으로 사용합니다:

    $post = App\Models\Post::find(1);

    echo url("/posts/{$post->id}");

    // http://example.com/posts/1

<a name="accessing-the-current-url"></a>
### 현재 URL 접근

`url` 헬퍼에 경로를 전달하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되며, 이를 통해 현재 URL에 대한 정보를 접근할 수 있습니다:

    // 쿼리 문자열 없이 현재 URL 가져오기...
    echo url()->current();

    // 쿼리 문자열을 포함한 전체 현재 URL 가져오기...
    echo url()->full();

    // 이전 요청의 전체 URL 가져오기...
    echo url()->previous();

이러한 메서드들은 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

    use Illuminate\Support\Facades\URL;

    echo URL::current();

<a name="urls-for-named-routes"></a>
## 이름 있는 라우트의 URL

`route` 헬퍼를 사용하여 [이름 있는 라우트](/docs/{{version}}/routing#named-routes)의 URL을 생성할 수 있습니다. 이름 있는 라우트를 사용하면 라우트에 정의된 실제 URL에 의존하지 않고 URL을 생성할 수 있으므로, 라우트의 URL이 변경되더라도 `route` 함수를 사용하는 부분을 수정할 필요가 없습니다. 예를 들어, 애플리케이션에 다음과 같은 라우트가 있다고 가정해봅시다:

    Route::get('/post/{post}', function (Post $post) {
        //
    })->name('post.show');

이 라우트의 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다:

    echo route('post.show', ['post' => 1]);

    // http://example.com/post/1

물론, `route` 헬퍼를 사용하여 여러 개의 파라미터가 있는 라우트의 URL도 생성할 수 있습니다:

    Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
        //
    })->name('comment.show');

    echo route('comment.show', ['post' => 1, 'comment' => 3]);

    // http://example.com/post/1/comment/3

라우트 정의의 파라미터와 일치하지 않는 추가 배열 요소는 URL의 쿼리 문자열에 추가됩니다:

    echo route('post.show', ['post' => 1, 'search' => 'rocket']);

    // http://example.com/post/1?search=rocket

<a name="eloquent-models"></a>
#### Eloquent 모델

대부분의 경우 [Eloquent 모델](/docs/{{version}}/eloquent)의 라우트 키(일반적으로 기본 키)를 사용해 URL을 생성하게 됩니다. 이를 위해, 파라미터 값으로 Eloquent 모델 인스턴스를 전달할 수 있습니다. `route` 헬퍼는 자동으로 모델의 라우트 키를 추출합니다:

    echo route('post.show', ['post' => $post]);

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 이름 있는 라우트에 대해 손쉽게 "서명된" URL을 생성할 수 있도록 해줍니다. 이런 URL에는 쿼리 문자열에 "서명" 해시가 추가되어, URL이 생성된 이후 변경되지 않았음을 Laravel이 검증할 수 있습니다. 서명된 URL은 퍼블릭하게 접근 가능하지만 URL 조작으로부터 보호가 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 발송되는 공개 "구독 취소" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름 있는 라우트에 대한 서명된 URL을 생성하려면, `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

    use Illuminate\Support\Facades\URL;

    return URL::signedRoute('unsubscribe', ['user' => 1]);

특정 시간 동안만 유효한 임시 서명 라우트 URL을 생성하려면, `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel이 임시 서명 라우트 URL을 검증할 때, 서명된 URL에 포함된 만료 시간이 경과하지 않았는지 확인합니다:

    use Illuminate\Support\Facades\URL;

    return URL::temporarySignedRoute(
        'unsubscribe', now()->addMinutes(30), ['user' => 1]
    );

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증

들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면, 들어온 `Request`에서 `hasValidSignature` 메서드를 호출해야 합니다:

    use Illuminate\Http\Request;

    Route::get('/unsubscribe/{user}', function (Request $request) {
        if (! $request->hasValidSignature()) {
            abort(401);
        }

        // ...
    })->name('unsubscribe');

또는, 라우트에 `Illuminate\Routing\Middleware\ValidateSignature` [미들웨어](/docs/{{version}}/middleware)를 할당할 수도 있습니다. 만약 이미 등록되어 있지 않다면, 이 미들웨어의 키를 HTTP 커널의 `routeMiddleware` 배열에 할당해야 합니다:

    /**
     * 애플리케이션의 라우트 미들웨어.
     *
     * 이 미들웨어들은 그룹에 할당되거나 개별로 사용될 수 있습니다.
     *
     * @var array
     */
    protected $routeMiddleware = [
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    ];

커널에 미들웨어를 등록했다면, 이제 라우트에 적용할 수 있습니다. 들어오는 요청이 유효한 서명을 가지고 있지 않다면, 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다:

    Route::post('/unsubscribe/{user}', function (Request $request) {
        // ...
    })->name('unsubscribe')->middleware('signed');

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 라우트에 대한 응답

만약 누군가 서명된 URL에 접근했는데 그 URL이 만료되었다면, `403` HTTP 상태 코드에 대한 일반적인 오류 페이지를 받게 됩니다. 하지만, 예외 처리기에서 `InvalidSignatureException` 예외에 대한 커스텀 "렌더러블" 클로저를 정의하여 이 동작을 커스터마이징할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다:

    use Illuminate\Routing\Exceptions\InvalidSignatureException;

    /**
     * 애플리케이션의 예외 처리 콜백 등록.
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

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관 배열을 전달할 수 있습니다:

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="default-values"></a>
## 기본 값

일부 애플리케이션에서는 특정 URL 파라미터에 대해 요청 전체에 적용되는 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 파라미터를 정의한다고 가정해봅시다:

    Route::get('/{locale}/posts', function () {
        //
    })->name('post.index');

매번 `route` 헬퍼를 사용해서 URL을 생성할 때마다 `locale`을 전달하는 것은 번거롭습니다. 이럴 때 `URL::defaults` 메서드를 사용하여 해당 파라미터에 대해 현재 요청 동안 항상 적용되는 기본값을 정의할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하면, 현재 요청 정보를 사용할 수 있으므로 더욱 유용합니다:

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

`locale` 파라미터에 대한 기본값이 설정되면, 이제 `route` 헬퍼로 URL을 생성할 때 해당 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값 & 미들웨어 우선순위

URL 기본값 설정은 Laravel의 암시적 모델 바인딩 처리와 충돌할 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/{{version}}/middleware#sorting-middleware)를 조정해야 합니다. 이는 애플리케이션의 HTTP 커널에 있는 `$middlewarePriority` 속성에서 해당 미들웨어가 `SubstituteBindings` 미들웨어보다 앞서 오도록 하면 됩니다.

`$middlewarePriority` 속성은 기본적으로 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 해당 정의를 복사하여 애플리케이션의 HTTP 커널에서 덮어써서 수정할 수 있습니다:

    /**
     * 우선순위에 따라 정렬된 미들웨어 목록.
     *
     * 이 설정으로 인해 전역이 아닌 미들웨어도 항상 주어진 순서로 실행됩니다.
     *
     * @var array
     */
    protected $middlewarePriority = [
        // ...
         \App\Http\Middleware\SetDefaultLocaleForUrls::class,
         \Illuminate\Routing\Middleware\SubstituteBindings::class,
         // ...
    ];