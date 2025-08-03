# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉토리](#nested-view-directories)
    - [첫 번째 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론, 라우트나 컨트롤러에서 전체 HTML 문서를 문자열로 직접 반환하는 것은 현실적이지 않습니다. 다행히도 뷰(View)는 모든 HTML을 별도의 파일로 분리하여 관리할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러나 애플리케이션 로직과 프레젠테이션 로직(화면 표시 로직)을 분리하며, 기본적으로 `resources/views` 디렉토리에 저장됩니다. Laravel에서는 보통 [Blade 템플릿 언어](/docs/master/blade)를 사용하여 뷰 템플릿을 작성합니다. 간단한 뷰는 다음과 같을 수 있습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 전역 `view` 헬퍼를 사용해서 다음과 같이 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성법에 대해 더 알고 싶다면, 전체 [Blade 문서](/docs/master/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

PHP 내에서 Blade로 프론트엔드 템플릿을 작성하는 대신, 많은 개발자가 React나 Vue를 사용하여 템플릿을 작성하는 것을 선호합니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 React/Vue 프론트엔드를 Laravel 백엔드에 연결하는 과정을 매우 간단하게 만들어 SPA(Single Page Application) 개발의 복잡성을 크게 줄여줍니다.

Laravel의 [React 및 Vue 애플리케이션 스타터 키트](/docs/master/starter-kits)는 Inertia로 구동되는 Laravel 애플리케이션의 좋은 시작점을 제공합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

애플리케이션의 `resources/views` 디렉토리에 `.blade.php` 확장자를 가진 파일을 만들어 뷰를 생성할 수 있으며, Artisan의 `make:view` 명령어를 사용해 생성할 수도 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/master/blade)임을 프레임워크에 알립니다. Blade 템플릿은 HTML과 Blade 지시문을 포함하여 값을 쉽게 출력하거나, 조건문, 반복문 등을 작성할 수 있게 해줍니다.

뷰를 생성한 후에는 앱의 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 뷰를 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또는 `View` 파사드(Facade)를 사용해 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉토리에 있는 뷰 파일명을 나타냅니다. 두 번째 인자는 뷰에서 사용할 데이터를 담은 배열입니다. 여기서는 `name` 변수를 전달하고, Blade 문법을 이용해 뷰에서 출력합니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉토리

뷰는 `resources/views` 디렉토리 내 하위 폴더에도 중첩해서 저장할 수 있습니다. 이 경우에는 '닷 표기법(dot notation)'을 사용해 중첩 뷰를 참조합니다. 예를 들어 `resources/views/admin/profile.blade.php`에 뷰가 저장되어 있다면, 다음과 같이 호출할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉토리 이름에는 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 첫 번째 사용 가능한 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면, 배열에 나열된 뷰들 중 가장 먼저 존재하는 뷰를 반환할 수 있습니다. 이는 애플리케이션이나 패키지에서 뷰를 사용자별로 커스터마이징하거나 덮어쓸 수 있을 때 유용합니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기

특정 뷰가 존재하는지 확인하려면 `View` 파사드의 `exists` 메서드를 사용하세요. 만약 뷰가 존재하면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기 (Passing Data to Views)

앞서 예시에서 보았듯이, 뷰에 데이터를 전달할 때는 배열 형식으로 전달하여 뷰 내부에서 해당 데이터를 사용할 수 있도록 합니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

이렇게 넘기는 데이터는 키와 값의 쌍으로 이루어진 배열이어야 합니다. 뷰에 데이터를 전달한 후에는 뷰 내부에서 키명을 이용해 각 값을 접근할 수 있습니다. 예를 들어 `<?php echo $name; ?>`와 같이 사용할 수 있습니다.

`view` 헬퍼에 전체 배열을 넘기는 대신, `with` 메서드를 사용해 데이터 항목을 하나씩 추가하는 방법도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 메서드 체이닝을 통해 여러 데이터를 연이어 전달할 수 있습니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

가끔 애플리케이션에서 렌더링되는 모든 뷰에 공통 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용하면 됩니다. 일반적으로 `share` 메서드는 서비스 프로바이더의 `boot` 메서드 안에서 호출하는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나 별도의 서비스 프로바이더를 만들어 관리할 수 있습니다:

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

뷰 컴포저는 뷰가 렌더링될 때마다 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰를 렌더링할 때마다 특정 데이터를 바인딩해야 한다면, 뷰 컴포저를 사용해 관련 로직을 한 곳에 모아 관리할 수 있습니다. 동일한 뷰가 여러 라우트나 컨트롤러에서 반복해서 반환되고 항상 일정한 데이터가 필요할 경우 특히 유용합니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/master/providers) 중 한 곳에서 등록합니다. 여기서는 `App\Providers\AppServiceProvider`가 이 역할을 담당한다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel은 기본적으로 클래스 기반 뷰 컴포저용 디렉터리를 제공하지 않으므로 자유롭게 원하는 구조로 정리할 수 있습니다. 예를 들어, `app/View/Composers` 디렉터리를 만들어 애플리케이션의 모든 뷰 컴포저를 모아둘 수 있습니다:

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
        // 클래스 기반 컴포저 등록...
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저(Closure) 기반 컴포저 등록...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

이제 컴포저가 등록되어, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 자동 실행됩니다. 컴포저 클래스의 예시는 다음과 같습니다:

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

모든 뷰 컴포저는 [서비스 컨테이너](/docs/master/container)를 통해 의존성 주입이 되므로, 필요한 의존성은 생성자에서 타입 힌트로 선언하면 자동으로 주입됩니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 이름 배열을 넘겨 여러 뷰에 한 번에 같은 컴포저를 연결할 수 있습니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한 `composer` 메서드는 와일드카드 `*` 문자를 허용하므로, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 크리에이터는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아니라 뷰 인스턴스가 생성되자마자 즉시 실행된다는 점에서 다릅니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 필요 시점에 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면, Laravel은 우선 해당 뷰의 컴파일된 버전이 있는지 확인합니다. 만약 컴파일된 뷰 파일이 없거나, 원본 뷰가 마지막으로 수정된 시점이 컴파일된 뷰보다 최신일 경우 뷰를 다시 컴파일합니다.

요청 중 뷰 컴파일은 약간의 성능 저하를 일으킬 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해 배포 과정에서 이 명령어를 실행하는 것이 좋습니다:

```shell
php artisan view:cache
```

뷰 캐시를 삭제하려면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```