# HTTP 리다이렉트

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
- [세션 데이터 플래시와 함께 리다이렉트](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스로, 사용자를 다른 URL로 리다이렉트하기 위한 적절한 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

    Route::get('/dashboard', function () {
        return redirect('/home/dashboard');
    });

때로는 폼 전송이 유효하지 않을 때처럼 사용자를 이전 위치로 리다이렉트하고 싶을 수도 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용하세요. 이 기능은 [세션](/docs/{{version}}/session)을 활용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있어야 합니다:

    Route::post('/user/profile', function () {
        // 요청을 검증...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트

`redirect` 헬퍼를 매개변수 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 해당 인스턴스의 다양한 메서드를 이용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다:

    return redirect()->route('login');

라우트에 파라미터가 필요한 경우, 두 번째 인자로 전달할 수 있습니다:

    // URI가 profile/{id}인 라우트의 경우

    return redirect()->route('profile', ['id' => 1]);

편의를 위해 Laravel은 전역 `to_route` 함수도 제공합니다:

    return to_route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 대입

"ID" 파라미터가 있는 라우트로 리다이렉트할 때, Eloquent 모델에서 해당 값을 가져와야 한다면, 모델 자체를 전달해도 됩니다. 그러면 ID가 자동으로 추출됩니다:

    // URI가 profile/{id}인 라우트의 경우

    return redirect()->route('profile', [$user]);

라우트 파라미터에 사용될 값을 커스텀하고 싶다면, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

    /**
     * 모델의 라우트 키 값 반환.
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉트

[컨트롤러 액션](/docs/{{version}}/controllers)으로의 리다이렉트도 생성할 수 있습니다. 이를 위해서는 컨트롤러와 액션명을 `action` 메서드에 전달하면 됩니다:

    use App\Http\Controllers\HomeController;

    return redirect()->action([HomeController::class, 'index']);

컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인자로 전달할 수 있습니다:

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-with-flashed-session-data"></a>
## 세션 데이터 플래시와 함께 리다이렉트

새로운 URL로 리다이렉트 하면서 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 작업은 일반적으로 동시에 이루어집니다. 보통, 작업이 성공적으로 완료된 후 성공 메시지를 세션에 플래시하는 경우입니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하면서 플루언트(체이닝) 방식으로 세션에 데이터를 플래시할 수 있습니다:

    Route::post('/user/profile', function () {
        // 사용자 프로필 업데이트...

        return redirect('/dashboard')->with('status', 'Profile updated!');
    });

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시한 후 사용자를 새로운 위치로 리다이렉트할 수 있습니다. 이렇게 입력값이 세션에 플래시되면, 다음 요청에서 [쉽게 꺼내어 사용할 수 있습니다](/docs/{{version}}/requests#retrieving-old-input):

    return back()->withInput();

사용자가 리다이렉트된 후, [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)을 사용하면 다음과 같습니다:

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif
