# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉터리](#nested-view-directories)
    - [첫 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저 (View Composers)](#view-composers)
    - [뷰 크리에이터 (View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

물론, 라우트(route)나 컨트롤러(controller)에서 전체 HTML 문서 문자열을 직접 반환하는 것은 실용적이지 않습니다. 다행히 뷰(View)는 모든 HTML 코드를 별도의 파일로 분리하여 관리할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러 또는 애플리케이션 로직과 프레젠테이션(표현) 로직을 분리하며, `resources/views` 디렉터리에 저장됩니다. Laravel에서는 보통 [Blade 템플릿 언어](/docs/9.x/blade)를 사용하여 뷰 템플릿을 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

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
> Blade 템플릿 작성법에 대해 더 알고 싶으신가요? 시작하기 위해 전체 [Blade 문서](/docs/9.x/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

Blade를 사용해 PHP에서 직접 프론트엔드 템플릿을 작성하는 대신, React나 Vue를 사용해 템플릿을 작성하는 개발자가 많아지고 있습니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 SPA 구축 시 흔한 복잡함 없이 React나 Vue 프론트엔드를 Laravel 백엔드와 쉽게 연결할 수 있도록 도와줍니다.

Breeze와 Jetstream [스타터 킷](/docs/9.x/starter-kits)은 Inertia 기반 Laravel 애플리케이션을 시작하는 데 좋은 출발점을 제공합니다. 더불어 [Laravel Bootcamp](https://bootcamp.laravel.com)에서는 Vue와 React 예제를 포함해 Inertia 기반 Laravel 애플리케이션 생성 과정을 완전하게 시연합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`resources/views` 디렉터리에 `.blade.php` 확장자를 가진 파일을 생성하면 뷰를 만들 수 있습니다. `.blade.php` 확장자는 이 파일이 [Blade 템플릿](/docs/9.x/blade)임을 프레임워크에 알려줍니다. Blade 템플릿은 HTML과 함께 값을 출력하거나 "if" 문, 반복문 등을 쉽게 작성할 수 있는 Blade 지시자(directives)를 포함합니다.

뷰를 만든 후에는 전역 `view` 헬퍼를 통해 라우트나 컨트롤러에서 뷰를 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한 `View` 파사드(facade)를 이용해 반환할 수도 있습니다:

```
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피, `view` 헬퍼 첫 번째 인자는 `resources/views` 디렉터리 내 뷰 파일의 이름과 대응됩니다. 두 번째 인자는 뷰에서 사용할 데이터 배열입니다. 위 예에서는 `name` 변수를 전달하며, 이것은 Blade 문법을 통해 뷰에 출력됩니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉터리

뷰는 `resources/views` 내 하위 디렉터리에 중첩해서 저장할 수도 있습니다. 이 경우 "점(dot)" 표기법을 사용해 중첩된 뷰를 참조합니다. 예를 들어, 뷰 파일이 `resources/views/admin/profile.blade.php`에 있다면, 애플리케이션 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에 `.` 문자를 포함하지 않아야 합니다.

<a name="creating-the-first-available-view"></a>
### 첫 사용 가능한 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면, 지정한 뷰 목록 중 존재하는 첫 번째 뷰를 반환할 수 있습니다. 애플리케이션이나 패키지에서 뷰를 커스터마이징하거나 덮어쓸 수 있도록 허용할 때 유용합니다:

```
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기

뷰가 존재하는지 확인할 때는 `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 뷰가 존재하면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\View;

if (View::exists('emails.customer')) {
    //
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞 예시에서 보았듯이, 데이터를 배열 형태로 뷰에 전달하여 뷰 내에서 사용할 수 있도록 할 수 있습니다:

```
return view('greetings', ['name' => 'Victoria']);
```

이렇게 전달하는 데이터는 키-값 쌍 배열이어야 하며, 뷰에서는 키에 해당하는 이름으로 각 값에 접근할 수 있습니다. 예를 들어, PHP 템플릿에서는 `<?php echo $name; ?>`로 데이터를 출력할 수 있습니다.

또한, 전체 배열 대신 `with` 메서드를 사용해 개별 데이터를 단계별로 뷰에 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하기 때문에 메서드 체이닝도 가능합니다:

```
return view('greeting')
            ->with('name', 'Victoria')
            ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

가끔 애플리케이션에서 렌더링되는 모든 뷰에 공통 데이터를 공유해야 할 때가 있습니다. 이때는 `View` 파사드의 `share` 메서드를 사용합니다. 보통 `share` 호출은 서비스 프로바이더(Service Provider)의 `boot` 메서드 내에 위치시키는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나 별도의 서비스 프로바이더를 만들어 관리할 수 있습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저 (View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 동일한 뷰가 여러 라우트나 컨트롤러에서 반복적으로 반환되고 항상 특정 데이터를 필요로 할 경우, 뷰 컴포저를 통해 그 로직을 한 곳에 깔끔하게 정리할 수 있습니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/9.x/providers)에 등록합니다. 이 예제에서는 `App\Providers\ViewServiceProvider`라는 별도의 서비스 프로바이더를 생성했다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저용 기본 디렉터리를 따로 제공하지 않으므로, 원하는 구조로 자유롭게 관리할 수 있습니다. 예를 들어, `app/View/Composers` 디렉터리를 만들고 모든 뷰 컴포저 클래스를 이곳에 모을 수 있습니다:

```
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ViewServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        // 클래스 기반 컴포저 등록
        View::composer('profile', ProfileComposer::class);

        // 클로저 기반 컴포저 등록
        View::composer('dashboard', function ($view) {
            //
        });
    }
}
```

> [!WARNING]
> 뷰 컴포저 등록을 위한 새 서비스 프로바이더를 생성했다면, 반드시 `config/app.php`의 `providers` 배열에 해당 프로바이더를 추가해야 합니다.

컴포저가 등록되면, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스 예시는 다음과 같습니다:

```
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 사용자 저장소 구현체.
     *
     * @var \App\Repositories\UserRepository
     */
    protected $users;

    /**
     * 새 프로필 컴포저 생성자.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }

    /**
     * 뷰에 데이터 바인딩하기.
     *
     * @param  \Illuminate\View\View  $view
     * @return void
     */
    public function compose(View $view)
    {
        $view->with('count', $this->users->count());
    }
}
```

보시다시피, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/9.x/container)를 통해 의존성이 자동 주입되므로, 필요한 의존성을 컴포저 생성자에 타입힌트로 지정할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 이름 배열을 넘기면, 하나의 컴포저를 여러 뷰에 동시에 연결할 수 있습니다:

```
use App\Views\Composers\MultiComposer;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한 `composer` 메서드에 와일드카드 `*`를 사용할 수도 있어, 모든 뷰에 한 번에 컴포저를 연결할 수 있습니다:

```
View::composer('*', function ($view) {
    //
});
```

<a name="view-creators"></a>
### 뷰 크리에이터 (View Creators)

뷰 “크리에이터”는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링 되기 직전이 아니라 뷰가 인스턴스화된 직후 즉시 실행된다는 차이가 있습니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 요청 시점에 필요에 따라 컴파일됩니다. 뷰 렌더링 요청이 들어오면 Laravel은 컴파일된 뷰가 존재하는지 확인하고, 존재한다면 원본 뷰 파일이 더 최근에 수정되었는지를 판단합니다. 컴파일된 뷰가 없거나, 원본 뷰가 더 최근에 수정된 경우 뷰를 다시 컴파일합니다.

요청 중 뷰 컴파일은 약간의 성능 저하를 일으킬 수 있어, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 배포 과정 중에 이 명령어를 실행하면 성능 향상에 도움이 됩니다:

```shell
php artisan view:cache
```

뷰 캐시를 지우려면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```