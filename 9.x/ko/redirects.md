# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로, 제출한 폼이 유효하지 않을 때처럼 사용자를 이전 위치로 리다이렉트시키고 싶을 수 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/9.x/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있는지 확인해야 합니다:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

`redirect` 헬퍼를 매개변수 없이 호출하면 `Illuminate\Routing\Redirector` 클래스의 인스턴스가 반환되며, 이 인스턴스에서 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```
return redirect()->route('login');
```

라우트에 매개변수가 있다면, `route` 메서드의 두 번째 인수로 매개변수를 전달할 수 있습니다:

```
// 다음과 같은 URI를 가진 라우트인 경우: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

편의를 위해 Laravel은 전역 `to_route` 함수도 제공합니다:

```
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 매개변수 자동 채우기

만약 Eloquent 모델에서 "ID" 매개변수를 채워야 하는 라우트로 리다이렉트한다면, 모델 자체를 전달할 수 있습니다. 그러면 자동으로 ID가 추출됩니다:

```
// 다음과 같은 URI를 가진 라우트인 경우: profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 매개변수에 들어갈 값을 맞춤화하고 싶다면, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```
/**
 * 모델의 라우트 키 값을 가져옵니다.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉트하기 (Redirecting To Controller Actions)

[컨트롤러 액션](/docs/9.x/controllers)으로도 리다이렉트를 생성할 수 있습니다. 이렇게 하려면, `action` 메서드에 컨트롤러 클래스와 액션 이름을 전달하세요:

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트에 매개변수가 필요한 경우, `action` 메서드의 두 번째 인수로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새로운 URL로 리다이렉트하고 동시에 [세션에 데이터를 플래시](/docs/9.x/session#flash-data)하는 경우가 많습니다. 보통 어떤 작업을 성공적으로 처리한 뒤, 세션에 성공 메시지를 플래시할 때 주로 사용합니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하고 플래시 데이터를 하나의 유창한 메서드 체인으로 처리할 수 있습니다:

```
Route::post('/user/profile', function () {
    // 사용자 프로필 업데이트...

    return redirect('/dashboard')->with('status', '프로필이 업데이트되었습니다!');
});
```

또한 `RedirectResponse`에서 제공하는 `withInput` 메서드를 사용해 현재 요청의 입력 데이터를 세션에 플래시한 다음, 사용자를 새로운 위치로 리다이렉트할 수 있습니다. 입력 데이터가 세션에 플래시된 후에는, 다음 요청 시 쉽게 [입력값을 다시 불러올 수 있습니다](/docs/9.x/requests#retrieving-old-input):

```
return back()->withInput();
```

사용자가 리다이렉트된 후에는 [세션](/docs/9.x/session)에 플래시된 메시지를 출력할 수 있습니다. 예를 들어, [Blade 문법](/docs/9.x/blade)을 사용한다면 다음과 같습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```