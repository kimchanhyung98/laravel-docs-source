# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [사용 가능한 첫 번째 뷰 생성](#creating-the-first-available-view)
    - [뷰의 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저](#view-composers)
    - [뷰 크리에이터](#view-creators)
- [뷰 최적화하기](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

경로(route)나 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 현실적으로 비효율적입니다. 다행히도, 뷰(View)를 사용하면 모든 HTML을 별도의 파일에 편리하게 분리해 둘 수 있습니다.

뷰는 컨트롤러 및 애플리케이션 로직을 프레젠테이션 로직과 분리해주며, `resources/views` 디렉터리에 저장됩니다. Laravel을 사용할 때 뷰 템플릿은 일반적으로 [Blade 템플릿 언어](/docs/master/blade)를 사용하여 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰는 `resources/views/greeting.blade.php`에 저장되어 있으므로, 전역 `view` 헬퍼를 사용하여 다음과 같이 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성 방법에 대해 더 알고 싶으신가요? 시작하려면 [Blade 전체 문서](/docs/master/blade)를 확인해보십시오.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자들이 PHP와 Blade 대신 React나 Vue를 사용해 프런트엔드 템플릿을 작성하는 방식을 선호하기 시작했습니다. Laravel은 [Inertia](https://inertiajs.com/) 라이브러리 덕분에 이 과정을 매우 간단하게 만들어줍니다. Inertia는 여러분의 React/Vue 프런트엔드와 Laravel 백엔드를 Single Page Application을 직접 구축할 때의 복잡함 없이 손쉽게 연결해줍니다.

[React 및 Vue 애플리케이션 스타터 키트](/docs/master/starter-kits)를 통해 Inertia 기반의 차기 Laravel 애플리케이션을 손쉽게 시작할 수 있습니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 직접 생성하거나, `make:view` Artisan 명령어로 뷰를 만들 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/master/blade)을 포함하고 있음을 프레임워크에 알립니다. Blade 템플릿에는 HTML뿐만 아니라 Blade 지시문(디렉티브)이 포함될 수 있어, 값을 쉽게 출력하거나, if문을 만들거나, 데이터를 반복하는 등 다양한 작업을 할 수 있습니다.

뷰를 만들었다면, 다음과 같이 애플리케이션의 경로나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한 `View` 파사드(Facade)를 사용해 뷰를 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

위 예시에서 첫 번째 인수는 `resources/views` 디렉터리 내의 뷰 파일 이름과 일치합니다. 두 번째 인수는 뷰에서 사용할 수 있도록 전달할 데이터의 배열입니다. 여기서는 `name` 변수를 전달하며, [Blade 문법](/docs/master/blade)을 통해 뷰에서 출력합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰 파일은 `resources/views` 디렉터리의 하위 디렉터리에도 중첩하여 저장할 수 있습니다. 이때 뷰를 참조할 때에는 "점(dot) 표기법"을 사용할 수 있습니다. 예를 들어, `resources/views/admin/profile.blade.php`에 뷰가 있을 때, 애플리케이션의 경로나 컨트롤러에서 아래와 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에는 `.` 문자를 포함하면 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 사용 가능한 첫 번째 뷰 생성

`View` 파사드의 `first` 메서드를 사용하여, 지정한 뷰 배열 중에서 존재하는 첫 번째 뷰를 사용할 수 있습니다. 이 기능은 애플리케이션이나 패키지에서 뷰를 커스터마이즈하거나 덮어쓸 수 있도록 할 경우에 유용합니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰의 존재 여부 확인

특정 뷰가 존재하는지 확인해야 한다면, `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 해당 뷰가 존재하면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기 (Passing Data to Views)

앞서의 예제처럼, 뷰에 데이터를 전달할 때는 뷰에서 사용할 수 있도록 데이터 배열을 인수로 넘길 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

이렇게 데이터를 전달할 때에는 배열의 키/값 쌍을 사용해야 합니다. 뷰에 데이터를 전달한 후에는, 해당 데이터의 키로 뷰 내부에서 각 값을 참조할 수 있습니다. (예: `<?php echo $name; ?>`)

또한, 데이터 전체 배열을 `view` 헬퍼에 전달하는 대신, `with` 메서드를 사용하여 개별 데이터를 뷰에 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 반환 전에 메서드 체이닝 방식으로 여러 데이터를 연이어 추가할 수 있습니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

애플리케이션에서 렌더링되는 모든 뷰에 공통 데이터를 공유할 필요가 있을 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드 호출은 서비스 제공자(ServiceProvider)의 `boot` 메서드 안에 작성하는 것이 좋으며, `App\Providers\AppServiceProvider` 클래스에 직접 추가하거나 별도의 서비스 제공자를 만들어서 사용해도 무방합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저 (View Composers)

뷰 컴포저(View Composer)는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 데이터가 항상 바인딩되어야 한다면, 뷰 컴포저를 통해 이런 로직을 한 곳에 모아 관리할 수 있습니다. 똑같은 뷰가 여러 경로나 컨트롤러에서 반환되며 항상 특정 데이터를 가져야 하는 경우에 특히 유용합니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 제공자](/docs/master/providers) 내에 등록합니다. 아래 예제에서는 `App\Providers\AppServiceProvider`에 관련 로직을 추가한다고 가정하겠습니다.

`View` 파사드의 `composer` 메서드를 통해 뷰 컴포저를 등록할 수 있습니다. Laravel에서는 클래스 기반 뷰 컴포저를 저장할 디렉터리를 별도로 제공하지 않으므로 자유롭게 구조화할 수 있습니다. 예를 들어, 모든 뷰 컴포저를 위한 `app/View/Composers` 디렉터리를 생성할 수도 있습니다:

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
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // 클래스 기반 컴포저 사용...
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저 기반 컴포저 사용...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

이제 컴포저가 등록되었으므로, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예제는 다음과 같습니다:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새 프로필 컴포저 생성자.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 뷰에 데이터를 바인딩.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

위 예시처럼, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 컴포저의 생성자에서 필요한 모든 의존성을 타입힌트로 명시해 주입받을 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

뷰 컴포저를 여러 뷰에 한 번에 연결하려면, `composer` 메서드의 첫 번째 인수로 뷰 배열을 전달하면 됩니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

`composer` 메서드는 `*` 문자도 와일드카드로 인식하므로, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터

뷰 "크리에이터(Creator)"는 뷰 컴포저와 매우 유사하지만, 뷰가 실제로 렌더되기 바로 전이 아닌, 뷰 객체가 인스턴스화될 때 즉시 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화하기 (Optimizing Views)

기본적으로, Blade 템플릿 뷰는 필요할 때마다(on demand) 컴파일됩니다. 요청이 들어와 뷰를 렌더링할 때, Laravel은 해당 뷰의 컴파일된 버전이 존재하는지 확인합니다. 파일이 존재한다면, 원본 뷰가 컴파일된 뷰보다 더 최근에 수정되었는지도 확인합니다. 컴파일된 뷰가 없거나, 원본 뷰가 더 최근에 수정된 경우, Laravel은 뷰를 새로 컴파일합니다.

요청을 처리하며 뷰를 컴파일하면 약간의 성능 저하가 발생할 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해, 이 명령어를 배포(Deployment) 과정의 일부로 실행하는 것이 좋습니다:

```shell
php artisan view:cache
```

뷰 캐시를 비우려면 `view:clear` 명령어를 사용할 수 있습니다:

```shell
php artisan view:clear
```
