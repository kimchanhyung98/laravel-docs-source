# HTTP 리다이렉트

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함하고 있습니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

    Route::get('/dashboard', function () {
        return redirect('/home/dashboard');
    });

때때로 제출된 폼이 유효하지 않을 때 등 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이 경우 전역 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/{{version}}/session)을 이용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있는지 확인하세요:

    Route::post('/user/profile', function () {
        // 요청을 검증하세요...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector` 인스턴스의 어떤 메서드도 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로의 `RedirectResponse`를 생성하려면 `route` 메서드를 사용하면 됩니다:

    return redirect()->route('login');

라우트에 파라미터가 필요한 경우, 두 번째 인수로 전달할 수 있습니다:

    // URI가 다음과 같은 라우트: profile/{id}

    return redirect()->route('profile', ['id' => 1]);

편의를 위해, Laravel은 전역 `to_route` 함수도 제공합니다:

    return to_route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통해 파라미터 채우기

Eloquent 모델에서 추출한 "ID" 파라미터를 가진 라우트로 리다이렉트하는 경우, 모델 자체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

    // URI가 다음과 같은 라우트: profile/{id}

    return redirect()->route('profile', [$user]);

라우트 파라미터에 들어갈 값을 커스터마이즈하고 싶다면, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

    /**
     * 모델의 라우트 키 값을 반환합니다.
     */
    public function getRouteKey(): mixed
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉트하기

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리다이렉트도 생성할 수 있습니다. 이를 위해 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요:

    use App\Http\Controllers\HomeController;

    return redirect()->action([HomeController::class, 'index']);

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인수로 함께 전달할 수 있습니다:

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-with-flashed-session-data"></a>
## 플래시 세션 데이터와 함께 리다이렉트하기

새 URL로 리다이렉트하면서 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 일이 자주 발생합니다. 일반적으로 작업을 성공적으로 수행한 후 성공 메시지를 세션에 플래시할 때 이 방법을 사용합니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하고 단일 메서드 체이닝으로 세션에 데이터를 플래시할 수 있습니다:

    Route::post('/user/profile', function () {
        // 사용자의 프로필을 갱신하세요...

        return redirect('/dashboard')->with('status', 'Profile updated!');
    });

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시한 후 사용자를 새 위치로 리다이렉트할 수 있습니다. 입력 데이터가 세션에 플래시된 후, 다음 요청에서 [입력값을 쉽게 가져올 수 있습니다](/docs/{{version}}/requests#retrieving-old-input):

    return back()->withInput();

사용자가 리다이렉트된 이후, [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/{{version}}/blade)를 사용하면 다음과 같이 할 수 있습니다:

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif
