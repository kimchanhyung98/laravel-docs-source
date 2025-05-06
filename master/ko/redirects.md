# HTTP 리디렉션

- [리디렉션 생성하기](#creating-redirects)
- [이름 있는 라우트로 리디렉션](#redirecting-named-routes)
- [컨트롤러 액션으로 리디렉션](#redirecting-controller-actions)
- [플래시 세션 데이터와 함께 리디렉션](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리디렉션 생성하기

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로 제출된 폼이 유효하지 않을 때 등, 사용자를 이전 위치로 리디렉션하고 싶을 수도 있습니다. 이 경우 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 활용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하고 있거나 모든 세션 미들웨어가 적용되어 있는지 확인해야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 검증...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름 있는 라우트로 리디렉션

`redirect` 헬퍼를 파라미터 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 해당 인스턴스의 모든 메서드를 사용할 수 있습니다. 예를 들어, 이름 있는 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, 두 번째 인자로 파라미터를 전달할 수 있습니다:

```php
// 다음 URI를 갖는 라우트: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

편의를 위해 Laravel은 전역 `to_route` 함수도 제공합니다:

```php
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 완성

"ID" 파라미터가 Eloquent 모델에서 자동으로 채워지는 라우트로 리디렉션할 때, 모델 인스턴스를 그대로 전달할 수 있습니다. 이 경우 ID 값은 자동으로 추출됩니다:

```php
// 다음 URI를 갖는 라우트: profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스터마이즈하려면 Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드해야 합니다:

```php
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/{{version}}/controllers)으로도 리디렉션을 생성할 수 있습니다. 이를 위해 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요:

```php
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요할 경우, 두 번째 인자에 파라미터를 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시 세션 데이터와 함께 리디렉션

새 URL로 리디렉션하면서 [데이터를 세션에 플래시](/docs/{{version}}/session#flash-data)하는 경우가 많습니다. 주로 어떤 동작을 성공적으로 수행한 후 성공 메시지를 세션에 플래시할 때 사용합니다. 편의상, `RedirectResponse` 인스턴스를 생성하며 플래시 데이터 저장까지 한 번에 체이닝으로 할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // 사용자 프로필 업데이트...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시한 뒤 사용자를 새 위치로 리디렉션할 수 있습니다. 입력값이 세션에 플래시된 후에는 다음 요청에서 [간편하게 입력값을 조회](/docs/{{version}}/requests#retrieving-old-input)할 수 있습니다:

```php
return back()->withInput();
```

사용자가 리디렉션된 이후에는 [세션](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/{{version}}/blade)을 사용할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```