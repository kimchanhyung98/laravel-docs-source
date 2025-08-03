# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉토리](#nested-view-directories)
    - [첫 번째 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론, 경로(routes)나 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 비현실적입니다. 다행히도 뷰(View)는 모든 HTML을 별도의 파일에 둠으로써 이를 간편하게 관리할 수 있게 해줍니다.

뷰는 컨트롤러 또는 애플리케이션 로직과 프레젠테이션 로직을 분리하며, `resources/views` 디렉토리에 저장됩니다. Laravel을 사용할 때 뷰 템플릿은 보통 [Blade 템플릿 언어](/docs/10.x/blade)를 사용해 작성됩니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰는 `resources/views/greeting.blade.php`에 저장되어 있으므로, 전역 `view` 헬퍼를 사용하여 다음과 같이 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]  
> Blade 템플릿 작성 방법에 대해 더 알고 싶다면, [Blade 문서](/docs/10.x/blade)를 참조하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

개발자 중 다수는 Blade를 통해 PHP에서 프론트엔드 템플릿을 작성하는 대신 React나 Vue로 템플릿을 작성하는 것을 선호합니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 React/Vue 프론트엔드를 Laravel 백엔드에 연결하면서 SPA를 만드는 복잡성을 줄여주어 이 과정을 간편하게 만듭니다.

Breeze 또는 Jetstream [스타터 키트](/docs/10.x/starter-kits)는 Inertia를 활용하는 Laravel 애플리케이션 출발점으로 매우 유용합니다. 또한, [Laravel Bootcamp](https://bootcamp.laravel.com)에서는 Vue와 React 예제와 함께 Inertia를 사용하는 Laravel 애플리케이션 구축을 전체적으로 시연합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

애플리케이션의 `resources/views` 디렉토리에 `.blade.php` 확장자를 가진 파일을 생성하거나 `make:view` Artisan 명령어를 사용하여 뷰를 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/10.x/blade)임을 프레임워크에 알립니다. Blade 템플릿 내에서는 HTML과 더불어 값 출력, 조건문(if), 반복문 등 Blade 지시문을 활용할 수 있습니다.

뷰를 생성하고 나면, 전역 `view` 헬퍼를 통해 애플리케이션의 라우트 또는 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한, `View` 파사드를 사용하여 뷰를 반환할 수도 있습니다:

```
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피 `view` 헬퍼에 전달하는 첫 번째 인수는 `resources/views` 디렉토리 내 뷰 파일 이름과 일치합니다. 두 번째 인수는 뷰에 전달할 데이터 배열입니다. 여기서는 `name` 변수를 전달하며, 뷰 내부에서는 [Blade 문법](/docs/10.x/blade)으로 출력됩니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉토리 (Nested View Directories)

`resources/views` 디렉토리 내에 서브디렉토리 형태로 뷰를 중첩할 수도 있습니다. 중첩된 뷰에 접근할 때는 "점(dot)" 표기법을 사용합니다. 예를 들어 뷰 파일 경로가 `resources/views/admin/profile.blade.php`라면, 라우트 또는 컨트롤러에서 아래와 같이 반환할 수 있습니다:

```
return view('admin.profile', $data);
```

> [!WARNING]  
> 뷰 디렉토리 이름에 `.` 문자를 포함하지 않아야 합니다.

<a name="creating-the-first-available-view"></a>
### 첫 번째 사용 가능한 뷰 생성하기 (Creating the First Available View)

`View` 파사드의 `first` 메서드를 사용하면, 여러 뷰 이름을 담은 배열 중에서 사용 가능한 첫 번째 뷰를 반환할 수 있습니다. 이 방법은 애플리케이션이나 패키지가 뷰를 커스터마이징하거나 덮어쓸 수 있도록 허용할 때 유용합니다:

```
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기 (Determining if a View Exists)

뷰가 존재하는지 확인해야 할 때는 `View` 파사드의 `exists` 메서드를 사용하세요. 뷰가 존재하면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기 (Passing Data to Views)

앞의 예시들에서 보았듯이, 데이터를 배열 형태로 뷰에 전달하여 뷰 내에서 사용할 수 있게 할 수 있습니다:

```
return view('greetings', ['name' => 'Victoria']);
```

이렇게 전달할 때 데이터는 키와 값으로 이루어진 배열이어야 합니다. 뷰에 데이터를 전달하면 뷰 내부에서 데이터 키 이름으로 접근할 수 있습니다. 예를 들어 `<?php echo $name; ?>`와 같이 접근합니다.

데이터 전체 배열을 넘기는 대신 `with` 메서드를 이용해 뷰에 개별 데이터를 추가할 수도 있습니다. `with`는 뷰 객체를 반환하므로 메서드를 연속 호출하며 체이닝할 수 있습니다:

```
return view('greeting')
            ->with('name', 'Victoria')
            ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기 (Sharing Data With All Views)

가끔 애플리케이션 내 모든 뷰에 데이터를 공유해야 하는 경우가 있습니다. 이때 `View` 파사드의 `share` 메서드를 사용하세요. 보통 `share` 호출은 서비스 프로바이더의 `boot` 메서드 내에 위치시키는 것이 좋습니다. 일반적으로 `App\Providers\AppServiceProvider`에 넣거나, 별도의 서비스 프로바이더를 생성해 관리할 수 있습니다:

```
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

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 바인딩할 데이터가 있다면, 뷰 컴포저를 사용해 해당 로직을 한 곳에 모아둘 수 있습니다. 동일한 뷰가 여러 경로나 컨트롤러에서 반환되고 일정한 데이터가 필요할 때 특히 유용합니다.

뷰 컴포저는 보통 애플리케이션의 [서비스 프로바이더](/docs/10.x/providers) 중 하나에 등록합니다. 예제에서는 `App\Providers\ViewServiceProvider`를 생성해 이 로직을 관리하는 것으로 가정합니다.

`View` 파사드의 `composer` 메서드로 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저용 기본 디렉토리를 제공하지 않으므로, 자유롭게 구성할 수 있습니다. 예를 들어 `app/View/Composers` 디렉토리를 만들어 뷰 컴포저를 관리할 수 있습니다:

```
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

class ViewServiceProvider extends ServiceProvider
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

> [!WARNING]  
> 뷰 컴포저 등록용 새로운 서비스 프로바이더를 생성했다면, `config/app.php` 설정 파일의 `providers` 배열에 해당 프로바이더를 추가해야 합니다.

컴포저를 등록하고 나면, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예시는 다음과 같습니다:

```
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새로운 프로필 컴포저 생성자.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * 뷰에 데이터 바인딩.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

모든 뷰 컴포저는 [서비스 컨테이너](/docs/10.x/container)를 통해 해결되므로, 컴포저 클래스 생성자에 필요한 의존성을 타입힌트하여 받을 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 붙이기

`composer` 메서드 첫 번째 인수에 뷰 이름 배열을 전달하여 여러 뷰에 동시에 컴포저를 붙일 수 있습니다:

```
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한, `*` 와일드카드를 사용해 모든 뷰에 컴포저를 붙일 수도 있습니다:

```
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터 (View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링 직전에 실행되는 컴포저와 달리 뷰가 인스턴스화되자마자 즉시 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

```
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화 (Optimizing Views)

기본적으로 Blade 뷰는 요청 시점에 필요에 따라 컴파일됩니다. 뷰가 렌더링되는 요청이 들어오면, Laravel은 이미 컴파일된 뷰 파일이 있는지 확인합니다. 파일이 존재할 경우, 원본 뷰보다 컴파일된 뷰가 더 최신인지 비교합니다. 만약 컴파일된 뷰가 없거나 원본 뷰가 더 최근에 수정되었다면, Laravel이 뷰를 다시 컴파일합니다.

요청 중에 뷰를 컴파일하는 것은 성능에 약간 부정적 영향을 줄 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해 배포 과정 중에 이 명령어를 실행하는 것을 권장합니다:

```shell
php artisan view:cache
```

`view:clear` 명령어를 사용하면 뷰 캐시를 삭제할 수 있습니다:

```shell
php artisan view:clear
```