# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [세션에 플래시 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하기 위한 적절한 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있으며, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로 사용자가 제출한 폼이 유효하지 않을 때처럼, 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/11.x/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 세션 미들웨어가 모두 적용되어 있는지 반드시 확인하세요:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

`redirect` 헬퍼에 인수를 전달하지 않고 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 이 인스턴스의 메서드를 자유롭게 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```
return redirect()->route('login');
```

라우트에 파라미터가 필요하다면, `route` 메서드의 두 번째 인수로 배열 형태로 전달할 수 있습니다:

```
// URI가 다음과 같은 라우트가 있다고 가정: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

편의를 위해 Laravel은 전역 `to_route` 함수도 제공합니다:

```
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 채우기

Eloquent 모델에서 ID 파라미터를 채우는 경로로 리다이렉트할 때는 모델 인스턴스 자체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

```
// URI가 다음과 같은 라우트가 있다고 가정: profile/{id}

return redirect()->route('profile', [$user]);
```

만약 라우트 파라미터로 전달되는 값을 커스텀하고 싶다면, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉트하기 (Redirecting To Controller Actions)

컨트롤러 액션으로 리다이렉트를 생성할 수도 있습니다. 이를 위해 `action` 메서드에 컨트롤러 클래스와 액션 이름을 배열로 전달하세요:

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트가 파라미터를 요구한다면, `action` 메서드의 두 번째 인수로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 세션에 플래시 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하고 동시에 [세션에 데이터를 플래시](/docs/11.x/session#flash-data)하는 작업은 보통 함께 이루어집니다. 일반적으로 어떤 작업을 성공적으로 수행한 후, 성공 메시지를 세션에 플래시할 때 자주 사용합니다. 편리하게도 `RedirectResponse` 인스턴스를 생성하면서 세션에 데이터를 플래시하는 것을 하나의 메서드 체인으로 할 수 있습니다:

```
Route::post('/user/profile', function () {
    // 사용자의 프로필 업데이트...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면 현재 요청의 입력 데이터를 세션에 플래시한 후, 사용자를 새 위치로 리다이렉트할 수 있습니다. 입력 데이터가 세션에 플래시되면 다음 요청에서 쉽게 [복원하여 사용할 수 있습니다](/docs/11.x/requests#retrieving-old-input):

```
return back()->withInput();
```

사용자가 리다이렉트된 후, [세션](/docs/11.x/session)에 플래시된 메시지를 보여줄 수 있습니다. 예를 들어, [Blade 문법](/docs/11.x/blade)를 사용하면 다음과 같이 작성할 수 있습니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```