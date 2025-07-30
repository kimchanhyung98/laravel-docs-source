# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue로 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉터리](#nested-view-directories)
    - [사용 가능한 첫 번째 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰와 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화하기](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론, 라우트(route)와 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 실용적이지 않습니다. 다행히도 뷰(View)는 모든 HTML을 별도의 파일에 편리하게 저장할 수 있는 방법을 제공합니다.

뷰는 컨트롤러 / 애플리케이션 로직과 프레젠테이션 로직을 분리하며, 기본적으로 `resources/views` 디렉터리에 저장됩니다. Laravel에서는 보통 뷰 템플릿을 [Blade 템플릿 언어](/docs/11.x/blade)를 사용해 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 글로벌 `view` 헬퍼를 사용해 이렇게 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]  
> Blade 템플릿 작성 방법에 대해 더 알고 싶으신가요? 시작을 위해 [Blade 문서 전체](/docs/11.x/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue로 뷰 작성하기

PHP의 Blade를 사용해 프론트엔드 템플릿을 작성하는 대신 React나 Vue를 사용해 템플릿을 작성하는 개발자가 점점 늘어나고 있습니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 이 과정을 간편하게 만듭니다. Inertia는 SPA(single-page application)를 만드는 전형적인 복잡함 없이 React/Vue 기반 프론트엔드를 Laravel 백엔드와 쉽게 연결할 수 있게 해주는 라이브러리입니다.

Laravel의 Breeze, Jetstream [스타터 키트](/docs/11.x/starter-kits)는 Inertia 기반 Laravel 애플리케이션의 훌륭한 시작점을 제공합니다. 또한 [Laravel Bootcamp](https://bootcamp.laravel.com)에서는 Vue와 React 예제와 함께 Inertia 기반 Laravel 애플리케이션 개발 과정을 전면적으로 보여줍니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 위치시키거나, Artisan 명령어 `make:view`로 뷰를 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 이 파일이 [Blade 템플릿](/docs/11.x/blade)임을 프레임워크에 알립니다. Blade 템플릿은 HTML과 함께, 값을 쉽게 출력하거나 "if" 문을 작성하거나 데이터 반복 등을 도와주는 Blade 지시문(directives)을 포함합니다.

뷰를 생성한 후에는 애플리케이션의 라우트나 컨트롤러에서 글로벌 `view` 헬퍼를 통해 뷰를 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

뷰는 `View` 파사드(facade)를 사용해 반환할 수도 있습니다:

```
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

위 예제에서 보듯 첫 번째 인수는 `resources/views` 내 뷰 파일 이름에 대응합니다. 두 번째 인수는 뷰에 전달할 데이터 배열입니다. 이 경우 `name` 변수를 전달했고, 이는 [Blade 문법](/docs/11.x/blade)으로 뷰 내에서 출력됩니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉터리 (Nested View Directories)

뷰는 `resources/views` 디렉터리 내에 서브디렉터리로 중첩 저장할 수 있습니다. "점(dot)" 표기법을 사용해 중첩된 뷰를 참조합니다. 예를 들어, 뷰가 `resources/views/admin/profile.blade.php`에 저장된 경우, 다음처럼 라우트나 컨트롤러에서 반환할 수 있습니다:

```
return view('admin.profile', $data);
```

> [!WARNING]  
> 뷰 디렉터리 이름에 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 사용 가능한 첫 번째 뷰 생성하기 (Creating the First Available View)

`View` 파사드의 `first` 메서드를 사용하면, 지정한 뷰 배열 중에서 존재하는 첫 번째 뷰를 반환할 수 있습니다. 이것은 애플리케이션이나 패키지에서 뷰를 커스터마이징하거나 덮어쓸 수 있도록 할 때 유용합니다:

```
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기 (Determining if a View Exists)

뷰가 존재하는지 확인해야 한다면 `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 뷰가 존재하면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기 (Passing Data to Views)

앞선 예제들에서 봤듯이, 뷰에 배열 형태의 데이터를 전달하여 뷰 안에서 사용할 수 있도록 할 수 있습니다:

```
return view('greetings', ['name' => 'Victoria']);
```

이 방식으로 데이터를 전달할 때, 데이터는 키/값 쌍으로 이루어진 배열이어야 합니다. 뷰에 데이터를 전달한 후에는 뷰 내부에서 `<?php echo $name; ?>` 같이 키 이름을 사용해 각 값을 접근할 수 있습니다.

또한, 전체 배열을 `view` 헬퍼 함수에 전달하는 대신 `with` 메서드를 사용해 개별 데이터 조각을 순차적으로 전달할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로 메서드 체이닝이 가능합니다:

```
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰와 데이터 공유하기 (Sharing Data With All Views)

가끔 애플리케이션에서 렌더링되는 모든 뷰에 공통 데이터를 공유해야 할 때가 있습니다. 이런 경우 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 일반적으로는 서비스 프로바이더의 `boot` 메서드 내에 공유 코드를 작성하며, `App\Providers\AppServiceProvider` 클래스에 작성하거나 별도의 서비스 프로바이더를 생성해 넣을 수 있습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 뷰가 렌더링될 때마다 특정 데이터를 뷰에 바인딩하고 싶을 때, 뷰 컴포저를 사용하면 이 로직을 한 곳에 집중시켜 관리할 수 있습니다. 동일한 뷰가 애플리케이션 내 여러 라우트나 컨트롤러에 의해 반환되고 항상 특정 데이터를 필요로 하는 경우 특히 유용합니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/11.x/providers) 중 하나에 등록합니다. 여기서는 `App\Providers\AppServiceProvider`에 등록하는 예를 들겠습니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel에는 클래스 기반 뷰 컴포저를 위한 기본 디렉터리가 없으므로, 개발자가 자유롭게 조직할 수 있습니다. 예를 들어, 모든 뷰 컴포저를 `app/View/Composers` 디렉터리에 모을 수도 있습니다:

```
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        // 클래스 기반 컴포저 등록...
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저 기반 컴포저 등록...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

컴포저가 등록되면, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예시는 다음과 같습니다:

```
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새 프로필 컴포저를 생성합니다.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 뷰에 데이터를 바인딩합니다.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

보시다시피 모든 뷰 컴포저는 [서비스 컨테이너](/docs/11.x/container)를 통해 해결되므로, 필요한 의존성은 컴포저 생성자에서 타입힌트로 주입할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 이름 배열을 전달해 한 번에 여러 뷰에 컴포저를 연결할 수 있습니다:

```
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한 `composer` 메서드는 와일드카드 `*` 문자를 지원하므로, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전까지 기다리는 대신 뷰가 인스턴스화된 직후 바로 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

```
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화하기 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 요청이 들어올 때마다 필요에 따라 컴파일됩니다. 즉, 뷰가 렌더링될 때 Laravel은 컴파일된 뷰 버전이 있는지 확인합니다. 컴파일된 뷰가 존재하면, 원본 뷰가 최신인지 비교하며 최신이 아니면 다시 컴파일합니다.

요청 중에 뷰를 컴파일하는 것은 약간의 성능 저하를 발생시킬 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해 배포 과정에 이 명령어를 포함시키는 것을 권장합니다:

```shell
php artisan view:cache
```

뷰 캐시를 초기화하려면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```