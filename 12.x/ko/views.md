# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉터리](#nested-view-directories)
    - [사용 가능한 첫 번째 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저 (View Composers)](#view-composers)
    - [뷰 크리에이터 (View Creators)](#view-creators)
- [뷰 최적화하기](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론, 라우트나 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 실용적이지 않습니다. 다행히도 뷰는 모든 HTML을 별도 파일로 분리하여 관리할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러나 애플리케이션 로직과 프레젠테이션 로직을 분리하며, `resources/views` 디렉터리에 저장됩니다. Laravel에서 뷰 템플릿은 보통 [Blade 템플릿 언어](/docs/12.x/blade)를 사용해 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 전역 `view` 헬퍼를 사용하여 다음과 같이 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성법에 대해 더 알고 싶으신가요? 시작하려면 전체 [Blade 문서](/docs/12.x/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자가 Blade를 통한 PHP 프론트엔드 템플릿 작성 대신 React나 Vue로 템플릿을 작성하는 것을 선호하고 있습니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 React / Vue 프론트엔드를 Laravel 백엔드와 간편하게 연결할 수 있도록 지원하며, SPA 구축의 복잡함을 최소화합니다.

[React 및 Vue 애플리케이션 스타터 키트](/docs/12.x/starter-kits)는 Inertia를 사용하는 다음 Laravel 애플리케이션을 쉽게 시작할 수 있게 도와줍니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

뷰는 `.blade.php` 확장자로 애플리케이션의 `resources/views` 디렉터리에 파일을 생성하거나 `make:view` Artisan 명령어로 만들 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/12.x/blade)임을 프레임워크에 알립니다. Blade 템플릿은 HTML과 함께 값 출력, 조건문 작성, 데이터 반복 처리 등의 Blade 지시자를 포함합니다.

뷰를 만든 후, 전역 `view` 헬퍼를 사용해 애플리케이션 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한, `View` 파사드를 사용해 다음과 같이 뷰를 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리 내 뷰 파일명을 뜻하며, 두 번째 인자는 뷰에 전달할 데이터 배열입니다. 이 예제에서는 Blade 구문으로 `name` 변수를 뷰 내에서 출력합니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉터리

뷰는 `resources/views` 디렉터리 내 하위 폴더에 중첩할 수 있습니다. 중첩된 뷰는 "점(.)" 표기법으로 참조합니다. 예를 들어, 뷰가 `resources/views/admin/profile.blade.php`에 저장되어 있다면, 다음과 같이 라우트나 컨트롤러에서 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에 `.` 문자는 포함하지 않아야 합니다.

<a name="creating-the-first-available-view"></a>
### 사용 가능한 첫 번째 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면, 주어진 여러 뷰 목록 중 존재하는 첫 번째 뷰를 반환할 수 있습니다. 이 기능은 애플리케이션이나 패키지에서 뷰를 사용자 정의하거나 덮어쓸 수 있게 할 때 유용합니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기

뷰가 존재하는지 확인하려면 `View` 파사드의 `exists` 메서드를 사용할 수 있으며, 존재하면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기 (Passing Data to Views)

앞 예시들에서 보았듯이, 뷰에 데이터를 전달할 때는 키/값 쌍이 담긴 배열을 넘겨 줍니다. 이렇게 전달된 데이터는 뷰에서 각 키를 사용해 접근할 수 있습니다. 예컨대, `<?php echo $name; ?>` 처럼 사용할 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

배열 대신 `with` 메서드를 사용해 뷰에 개별 데이터를 전달할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 메서드 체이닝이 가능합니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

가끔은 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이럴 경우 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 보통은 서비스 프로바이더의 `boot` 메서드에서 호출하며, `App\Providers\AppServiceProvider` 클래스에 넣거나 별도의 서비스 프로바이더를 생성해 관리할 수 있습니다:

```php
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
     * 애플리케이션 부트스트랩 작업을 수행합니다.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저 (View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 매번 렌더링될 때 바인딩되어야 하는 데이터가 있다면, 뷰 컴포저는 그 로직을 한 곳에 깔끔하게 정리할 수 있도록 도와줍니다. 특히, 여러 라우트나 컨트롤러에서 같은 뷰를 반환하고 항상 특정 데이터를 전달해야 할 때 유용합니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나에 등록합니다. 여기서는 `App\Providers\AppServiceProvider`에 등록한다고 가정하겠습니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저의 기본 디렉터리를 제공하지 않으니, 원하는 대로 구조를 잡을 수 있습니다. 예를 들어, 애플리케이션 내 `app/View/Composers` 디렉터리를 만들어 모든 뷰 컴포저를 관리할 수 있습니다:

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
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 부트스트랩 작업을 수행합니다.
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

이제 `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예제는 다음과 같습니다:

```php
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

보면 모든 뷰 컴포저는 [서비스 컨테이너](/docs/12.x/container)를 통해 해결되므로, 생성자의 의존성 타입 힌트를 활용해 필요한 의존성을 주입받을 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 배열을 넘겨 여러 뷰에 한 번에 컴포저를 연결할 수 있습니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한 `composer` 메서드는 와일드카드 문자 `*`를 지원해 모든 뷰에 대해 컴포저를 연결할 수 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터 (View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아닌 뷰가 인스턴스화된 직후 즉시 실행된다는 점이 다릅니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화하기 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 필요할 때마다 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면 Laravel은 해당 뷰의 컴파일된 버전이 존재하는지 검사합니다. 만약 존재한다면, 컴파일되지 않은 원본 뷰가 컴파일된 뷰보다 최근에 수정되었는지 확인합니다. 컴파일된 뷰가 없거나 원본 뷰가 더 최근이면 뷰를 재컴파일합니다.

요청 중에 뷰를 컴파일하는 것은 성능에 약간 부정적인 영향을 끼칠 수 있으므로, Laravel은 `view:cache` Artisan 명령어를 제공해 애플리케이션에서 사용되는 모든 뷰를 미리 컴파일할 수 있도록 지원합니다. 배포 과정에서 이 명령어를 실행하면 성능 향상에 도움이 됩니다:

```shell
php artisan view:cache
```

`view:clear` 명령어로 뷰 캐시를 삭제할 수 있습니다:

```shell
php artisan view:clear
```