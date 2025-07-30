# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 여러 방법이 있지만, 가장 간단한 방법은 전역 `redirect` 헬퍼 함수를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는 제출한 폼이 유효하지 않을 때처럼, 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 사용하기 때문에, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용하거나 세션 미들웨어가 모두 적용되어 있어야 합니다:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

매개변수 없이 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 메서드를 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트 응답을 생성하려면 `route` 메서드를 사용합니다:

```
return redirect()->route('login');
```

라우트가 매개변수를 가지고 있다면, 두 번째 인수로 해당 매개변수를 전달할 수 있습니다:

```
// URI가 다음과 같은 라우트의 경우: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통해 매개변수 채우기

ID 파라미터가 Eloquent 모델에서 자동으로 채워지는 라우트로 리다이렉트할 때는, 모델 인스턴스 자체를 전달할 수 있으며, ID는 자동으로 추출됩니다:

```
// URI가 다음과 같은 라우트의 경우: profile/{id}

return redirect()->route('profile', [$user]);
```

만약 라우트 매개변수에 넣을 값을 사용자 정의하고 싶다면, Eloquent 모델 내에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```
/**
 * 모델의 라우트 키 값을 반환합니다.
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

컨트롤러 액션으로 리다이렉트를 생성할 수도 있습니다. 이 경우 `action` 메서드에 컨트롤러와 액션 이름을 전달합니다:

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트가 매개변수를 요구하는 경우, 두 번째 인수로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하고 동시에 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 작업은 보통 같이 이루어집니다. 대부분은 어떤 작업을 성공적으로 수행한 후, 성공 메시지를 세션에 플래시하기 위해 사용합니다. 이때 편리하게도, `RedirectResponse` 인스턴스를 생성하면서 동시에 세션에 데이터를 플래시할 수 있도록 메서드를 체이닝할 수 있습니다:

```
Route::post('/user/profile', function () {
    // 사용자의 프로필 업데이트...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 플래시하여 사용자 리다이렉트 전에 세션에 저장할 수 있습니다. 이렇게 플래시된 입력 데이터는 다음 요청에서 쉽게 [불러올 수 있습니다](/docs/{{version}}/requests#retrieving-old-input):

```
return back()->withInput();
```

사용자가 리다이렉트된 후에는, [세션](/docs/{{version}}/session)에서 플래시된 메시지를 화면에 출력할 수 있습니다. 예를 들어 [Blade 문법](/docs/{{version}}/blade)에서는 다음과 같이 작성합니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```