# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [가장 먼저 사용 가능한 뷰 생성](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저](#view-composers)
    - [뷰 크리에이터](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

라우트(route)나 컨트롤러(controller)에서 전체 HTML 문서 문자열을 직접 반환하는 것은 비효율적입니다. 다행히도, 뷰(View)는 모든 HTML을 별도의 파일에 저장할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러/애플리케이션 로직과 프레젠테이션 로직을 분리해주며, `resources/views` 디렉터리에 저장됩니다. Laravel을 사용할 때, 뷰 템플릿은 보통 [Blade 템플릿 언어](/docs/{{version}}/blade)를 사용해 작성됩니다. 간단한 뷰는 다음과 같습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 전역 `view` 헬퍼를 사용해 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성법이 궁금하다면 [Blade 공식 문서](/docs/{{version}}/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자들은 Blade를 이용한 PHP 기반 템플릿 대신, React나 Vue를 이용해 프론트엔드 템플릿을 작성하는 방식을 선호하고 있습니다. Laravel은 [Inertia](https://inertiajs.com/)라는 라이브러리를 통해 React/Vue 프론트엔드를 Laravel 백엔드와 쉽게 연결할 수 있게 해줍니다. 별도의 SPA 구축에 따르는 복잡함 없이도 기능을 구현할 수 있습니다.

[React 및 Vue 애플리케이션 시작 키트](/docs/{{version}}/starter-kits)는 Inertia 기반의 새로운 Laravel 프로젝트를 시작하기에 좋은 출발점입니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 추가하거나, `make:view` Artisan 명령어로 뷰를 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알려줍니다. Blade 템플릿은 HTML과, 쉽게 값을 출력하거나 if문을 작성하거나 데이터를 반복 처리하는 등의 Blade 지시어를 포함할 수 있습니다.

뷰를 생성한 후에는, 아래와 같이 라우트나 컨트롤러에서 전역 `view` 헬퍼로 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

`View` 파사드를 이용해서도 뷰를 반환할 수 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

위 코드에서 알 수 있듯, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리의 뷰 파일명을 의미합니다. 두 번째 인자는 뷰에서 사용할 수 있도록 전달할 데이터 배열입니다. 여기서는 `name` 변수를 전달했으며, 뷰에서는 [Blade 문법](/docs/{{version}}/blade)으로 출력합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰 파일은 `resources/views`의 하위 디렉터리에 중첩할 수도 있습니다. 이 경우 "닷(.)" 표기법을 사용해서 뷰를 참조합니다. 예를 들어, 뷰 파일이 `resources/views/admin/profile.blade.php`에 있다면, 아래와 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에는 `.` 문자를 사용하지 마세요.

<a name="creating-the-first-available-view"></a>
### 가장 먼저 사용 가능한 뷰 생성

`View` 파사드의 `first` 메서드를 사용해, 주어진 뷰 배열 중 첫 번째로 존재하는 뷰를 반환할 수 있습니다. 애플리케이션이나 패키지에서 뷰를 커스터마이즈하거나 재정의 가능하도록 할 때 유용합니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

특정 뷰가 존재하는지 확인하려면 `View` 파사드를 사용하세요. `exists` 메서드는 뷰가 존재하면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달

앞선 예제와 같이, 뷰에 데이터 배열을 전달하여 뷰에서 해당 데이터를 사용할 수 있게 할 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

이 방식으로 데이터를 전달할 때, 데이터는 키-값 쌍의 배열이어야 합니다. 데이터를 뷰로 전달하면, 뷰 파일 내에서 해당 키를 사용해 값을 출력할 수 있습니다. 예: `<?php echo $name; ?>`.

전체 데이터 배열 대신, `with` 메서드를 체이닝하여 개별 데이터를 뷰에 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 뷰 반환 전에 여러 메서드를 계속 체이닝할 수 있습니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

애플리케이션의 모든 뷰에서 동일한 데이터를 공유해야 할 때가 있습니다. 이런 경우, `View` 파사드의 `share` 메서드를 사용하세요. 보통 서비스를 등록하는 프로바이더의 `boot` 메서드에서 이 메서드를 호출합니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나 별도의 서비스 프로바이더를 만들어 관리할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 함수 또는 클래스 메서드입니다. 뷰가 렌더링될 때마다 특정 데이터를 해당 뷰에 바인딩해야 한다면, 뷰 컴포저를 활용해 해당 로직을 한 곳에 집중시킬 수 있습니다. 특히, 여러 라우트나 컨트롤러에서 동일한 뷰가 반환될 때 항상 특정 데이터를 포함해야 한다면 유용합니다.

일반적으로 뷰 컴포저 등록은 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)에서 진행합니다. 여기서는 `App\Providers\AppServiceProvider`에 로직을 작성한다고 가정하겠습니다.

`View` 파사드의 `composer` 메서드로 뷰 컴포저를 등록할 수 있습니다. Laravel에서는 클래스 기반 뷰 컴포저를 위한 기본 디렉터리를 제공하지 않으므로 원하는대로 구성해도 됩니다. 예를 들어, `app/View/Composers` 디렉터리를 생성하여 모든 컴포저를 관리할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        // 클래스 기반 컴포저 사용
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저(익명함수) 기반 컴포저 사용
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

이제 컴포저가 등록되었으므로, `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드는 `profile` 뷰가 렌더링될 때마다 실행됩니다. 컴포저 클래스 예시는 다음과 같습니다:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새로운 프로필 컴포저 생성자
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 뷰에 데이터 바인딩
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동 해결되므로, 컴포저 생성자에서 필요에 따라 의존성 타입 힌트를 사용할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 한 번에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 배열을 넘겨주면 여러 뷰에 한 번에 컴포저를 연결할 수 있습니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한, `composer` 메서드는 와일드카드로 `*` 문자를 지원하여, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 인스턴스화된 즉시 실행된다는 점이 다릅니다(컴포저는 뷰가 렌더링 직전에 실행). 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 필요할 때마다 컴파일됩니다. 뷰를 렌더링할 때, Laravel은 컴파일된 뷰가 존재하는지 확인합니다. 파일이 존재하면, 원본 뷰 파일이 컴파일된 뷰보다 더 최근에 수정되었는지도 확인합니다. 컴파일된 뷰가 없거나, 원본 뷰가 더 최근에 수정되었다면 Laravel은 뷰를 다시 컴파일합니다.

요청 중에 뷰를 컴파일하는 과정은 성능에 약간 부정적인 영향을 줄 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일 해주는 `view:cache` Artisan 명령어를 제공합니다. 배포 프로세스의 일부로 이 명령어를 실행하면 성능이 향상될 수 있습니다:

```shell
php artisan view:cache
```

뷰 캐시를 지우고 싶다면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```
