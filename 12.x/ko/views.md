# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [첫 번째로 사용 가능한 뷰 생성](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저](#view-composers)
    - [뷰 크리에이터](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

라우트(route)나 컨트롤러에서 HTML 전체 문서 문자열을 직접 반환하는 것은 비효율적입니다. 다행히도, 뷰(View)는 모든 HTML 코드를 별도의 파일에 담아 관리할 수 있게 해주는 편리한 방법을 제공합니다.

뷰는 컨트롤러/애플리케이션 로직과 프리젠테이션 로직을 분리해주며, `resources/views` 디렉터리에 저장됩니다. Laravel에서는 보통 [Blade 템플릿 언어](/docs/{{version}}/blade)를 이용해 뷰 템플릿을 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 다음과 같이 글로벌 `view` 헬퍼를 사용하여 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성 방법에 대해 더 알아보고 싶으신가요? 자세한 내용은 [Blade 문서](/docs/{{version}}/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자들이 PHP의 Blade를 통해 프론트엔드 템플릿을 작성하는 대신, React 또는 Vue로 템플릿을 작성하는 방식을 선호하기 시작했습니다. Laravel은 [Inertia](https://inertiajs.com/) 라이브러리를 통해 React/Vue 프론트엔드를 Laravel 백엔드와 손쉽게 연결할 수 있도록 지원하므로, 전형적인 SPA 구축의 복잡성을 제거할 수 있습니다.

[React 및 Vue 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)는 Inertia 기반의 새로운 Laravel 애플리케이션을 시작하는 데 훌륭한 출발점을 제공합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

뷰는 애플리케이션의 `resources/views` 디렉터리에 `.blade.php` 확장자로 파일을 생성하거나, `make:view` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알립니다. Blade 템플릿은 HTML과 더불어 Blade 지시문(디렉티브)을 포함할 수 있으며, 값을 쉽게 출력하거나, "if" 문을 작성하고, 데이터를 반복 처리하는 등 다양한 기능을 지원합니다.

뷰를 생성한 후에는 글로벌 `view` 헬퍼를 사용해 라우트나 컨트롤러에서 뷰를 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

뷰는 `View` 파사드(Facade)를 사용해 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시는 것처럼, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리 내 뷰 파일의 이름과 대응합니다. 두 번째 인자는 뷰에서 사용할 수 있도록 전달할 데이터의 배열입니다. 여기서는 `name` 변수를 전달하고 있으며, 뷰 내부에서 [Blade 문법](/docs/{{version}}/blade)으로 출력되고 있습니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰 파일은 `resources/views` 디렉터리 내의 하위 디렉터리에도 위치할 수 있습니다. 이때 "닷(dot) 표기법"을 사용해 중첩된 뷰를 참조할 수 있습니다. 예를 들어, 뷰 파일이 `resources/views/admin/profile.blade.php`에 저장되어 있다면, 다음과 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에는 `.`(닷) 문자를 포함하지 않아야 합니다.

<a name="creating-the-first-available-view"></a>
### 첫 번째로 사용 가능한 뷰 생성

`View` 파사드의 `first` 메서드를 사용하면, 특정 뷰 배열 중 가장 먼저 존재하는 뷰를 생성할 수 있습니다. 이는 애플리케이션이나 패키지에서 뷰를 커스터마이즈하거나 덮어쓸 수 있도록 허용할 때 유용합니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

뷰가 존재하는지 확인해야 할 때는 `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 뷰가 존재하면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞서 보았듯이, 데이터를 배열 형태로 뷰에 전달하여 해당 데이터를 뷰에서 사용할 수 있도록 할 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

이 방식으로 정보를 전달할 때는 키/값 쌍의 배열을 사용해야 하며, 뷰에서는 해당 키를 통해 값에 접근할 수 있습니다. 예: `<?php echo $name; ?>`

`view` 헬퍼 함수에 완전한 배열을 전달하는 대신, `with` 메서드를 사용해 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체의 인스턴스를 반환하므로, 뷰를 반환하기 전 메서드 체이닝도 가능합니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

가끔 애플리케이션에서 렌더링되는 모든 뷰에 동일한 데이터를 공유해야 할 필요가 있습니다. 이를 위해 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 일반적으로 `share` 메서드 호출은 서비스 프로바이더의 `boot` 메서드 내에 위치시킵니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나, 별도의 서비스 프로바이더를 생성해서 관리할 수도 있습니다:

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
## 뷰 컴포저

뷰 컴포저(View Composer)는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 각 뷰가 렌더될 때마다 바인딩해야 할 데이터가 있다면, 뷰 컴포저를 활용해 해당 로직을 한 곳에 정리할 수 있습니다. 여러 라우트나 컨트롤러에서 동일한 뷰가 반환되고, 항상 특정 데이터가 필요할 때 특히 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나에서 등록합니다. 여기서는 `App\Providers\AppServiceProvider`에 해당 로직이 있다고 가정하겠습니다.

`View` 파사드의 `composer` 메서드를 통해 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저를 위한 기본 디렉터리를 제공하지 않으므로, 자유롭게 구조를 구성할 수 있습니다. 예를 들어, 모든 뷰 컴포저를 위한 `app/View/Composers` 디렉터리를 만들 수 있습니다:

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

        // 클로저(Closure) 기반 컴포저 사용
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

이제 컴포저가 등록되었으므로, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예시는 다음과 같습니다:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새 프로필 컴포저 인스턴스 생성
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

보시다시피, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자에서 필요한 의존성을 타입힌트로 작성할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 하나의 컴포저를 여러 뷰에 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 배열을 전달해, 하나의 뷰 컴포저를 여러 뷰에 동시에 연결할 수 있습니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

`composer` 메서드는 와일드카드로 `*` 문자를 지원하여, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아니라 인스턴스화된 직후에 실행됩니다. 뷰 크리에이터를 등록하려면, `creator` 메서드를 이용합니다:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 요청 시(on demand) 컴파일됩니다. 뷰가 렌더링되는 요청이 실행되면, Laravel은 컴파일된 뷰 파일의 존재 여부를 확인합니다. 파일이 존재하면, 미컴파일(원본) 뷰가 컴파일된 뷰보다 최신인지 검사합니다. 컴파일된 뷰가 없거나, 미컴파일 뷰가 더 최근에 수정된 경우, Laravel은 뷰를 재컴파일합니다.

요청 중에 뷰를 컴파일하는 것은 성능에 약간의 부정적 영향을 줄 수 있습니다. 따라서 Laravel에서는 모든 뷰를 미리 컴파일해둘 수 있도록 `view:cache` Artisan 명령어를 제공합니다. 성능을 높이기 위해 배포 과정의 일부로 이 명령어를 실행할 수 있습니다:

```shell
php artisan view:cache
```

뷰 캐시를 비우려면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```
