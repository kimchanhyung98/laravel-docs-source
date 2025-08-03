# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름 있는 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시된 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있으며, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는 제출한 폼이 유효하지 않을 때처럼 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이럴 경우 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/10.x/session)을 활용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있어야 합니다:

```
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름 있는 라우트로 리다이렉트하기 (Redirecting To Named Routes)

`redirect` 헬퍼를 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스를 반환하며, 이 인스턴스에서 여러 메서드를 호출할 수 있습니다. 예를 들어 이름 있는 라우트로 리다이렉트할 때는 `route` 메서드를 사용할 수 있습니다:

```
return redirect()->route('login');
```

라우트에 매개변수가 있을 경우, 두 번째 인수로 전달할 수 있습니다:

```
// URI가 다음과 같은 라우트: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

더 편리하게, Laravel은 전역 `to_route` 함수를 제공합니다:

```
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 매개변수 채우기

라우트의 "ID" 매개변수가 Eloquent 모델에서 채워지는 경우, 모델 자체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

```
// URI가 다음과 같은 라우트: profile/{id}

return redirect()->route('profile', [$user]);
```

만약 라우트 매개변수에 들어갈 값을 사용자 지정하고 싶으면, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하세요:

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

[컨트롤러 액션](/docs/10.x/controllers)으로 리다이렉트를 생성할 수도 있습니다. 이때는 `action` 메서드에 컨트롤러와 액션 이름을 전달하면 됩니다:

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트에 매개변수가 필요할 경우, 두 번째 인수로 전달할 수 있습니다:

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시된 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하면서 동시에 [세션에 데이터를 플래시](/docs/10.x/session#flash-data)하는 경우가 많습니다. 일반적으로 어떤 작업을 성공적으로 완료한 후 세션에 성공 메시지를 플래시할 때 사용합니다. 편리하게도, `RedirectResponse` 인스턴스를 생성하면서 세션에 데이터를 플래시하는 메서드 체이닝을 할 수 있습니다:

```
Route::post('/user/profile', function () {
    // 사용자 프로필 업데이트...

    return redirect('/dashboard')->with('status', '프로필이 업데이트되었습니다!');
});
```

`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시한 뒤 사용자를 새 위치로 리다이렉트할 수 있습니다. 플래시된 입력 데이터는 다음 요청에서 쉽게 [불러올 수 있습니다](/docs/10.x/requests#retrieving-old-input):

```
return back()->withInput();
```

사용자가 리다이렉트된 후에는 [세션](/docs/10.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/10.x/blade)으로 다음과 같이 작성합니다:

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```