# HTTP 리다이렉션

- [리다이렉션 생성하기](#creating-redirects)
- [이름 있는 라우트로 리다이렉션](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉션](#redirecting-controller-actions)
- [세션 데이터와 함께 리다이렉션](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉션 생성하기

리다이렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

    Route::get('/dashboard', function () {
        return redirect('/home/dashboard');
    });

사용자를 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 예를 들어, 제출된 폼이 유효하지 않을 때가 그 예입니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있는지 꼭 확인하세요.

    Route::post('/user/profile', function () {
        // 요청을 검증합니다...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
## 이름 있는 라우트로 리다이렉션

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector` 인스턴스의 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름 있는 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용하면 됩니다.

    return redirect()->route('login');

라우트에 파라미터가 있다면, 두 번째 인수로 배열 형태로 전달할 수 있습니다.

    // 다음과 같은 URI를 가진 라우트: profile/{id}

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 채우기

Eloquent 모델로부터 채워지는 "ID" 파라미터를 가진 라우트로 리다이렉트하고자 할 때는 모델 인스턴스 자체를 전달할 수 있습니다. ID 값이 자동으로 추출됩니다.

    // 다음과 같은 URI를 가진 라우트: profile/{id}

    return redirect()->route('profile', [$user]);

라우트 파라미터에 들어갈 값을 커스터마이즈하고 싶을 때는 Eloquent 모델의 `getRouteKey` 메서드를 오버라이드하면 됩니다.

    /**
     * 모델의 라우트 키 값을 반환합니다.
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉션

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리다이렉트하는 것도 가능합니다. 이를 위해서는 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다.

    use App\Http\Controllers\HomeController;

    return redirect()->action([HomeController::class, 'index']);

컨트롤러 라우트에 파라미터가 필요한 경우에는 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-with-flashed-session-data"></a>
## 세션 데이터와 함께 리다이렉션

새 URL로 리다이렉트하면서 [데이터를 세션에 플래시](/docs/{{version}}/session#flash-data)하는 것이 일반적입니다. 보통 어떤 동작을 성공적으로 수행한 후, 세션에 성공 메시지를 플래시할 때 이렇게 합니다. 편의를 위해, 하나의 유창한 메서드 체인에서 `RedirectResponse` 인스턴스를 생성하고 세션에 데이터를 플래시할 수 있습니다.

    Route::post('/user/profile', function () {
        // 사용자의 프로필을 업데이트합니다...

        return redirect('/dashboard')->with('status', '프로필이 업데이트되었습니다!');
    });

새 위치로 리다이렉트하기 전에 현재 요청의 입력 데이터를 세션에 플래시하려면 `RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용할 수 있습니다. 입력 데이터가 세션에 플래시된 후에는 다음 요청에서 [이 데이터를 쉽게 가져올 수 있습니다](/docs/{{version}}/requests#retrieving-old-input).

    return back()->withInput();

사용자가 리다이렉트된 후, [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)을 사용하면 다음과 같이 할 수 있습니다.

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif