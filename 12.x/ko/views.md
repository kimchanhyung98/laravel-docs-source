# 뷰 (Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [가장 먼저 존재하는 뷰 반환](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유](#sharing-data-with-all-views)
- [뷰 컴포저(View Composer)](#view-composers)
    - [뷰 크리에이터(View Creator)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

라우트나 컨트롤러에서 전체 HTML 문서를 문자열로 직접 반환하는 것은 현실적으로 비효율적입니다. 다행히 뷰(View)를 이용하면 모든 HTML 코드를 별도의 파일에 분리해 관리할 수 있습니다.

뷰는 컨트롤러 또는 애플리케이션의 비즈니스 로직과 화면 표시 로직을 분리해 주며, `resources/views` 디렉터리에 저장됩니다. 라라벨에서는 주로 [Blade 템플릿 언어](/docs/12.x/blade)를 사용하여 뷰를 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- resources/views/greeting.blade.php 에 저장된 뷰 예시 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰는 `resources/views/greeting.blade.php`에 저장되어 있으므로, 다음과 같이 전역 `view` 헬퍼를 통해 반환할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성 방법에 대해 더 알고 싶으신가요? 자세한 내용은 [Blade 공식 문서](/docs/12.x/blade)를 참고해 주세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

Blade로 PHP 기반 프론트엔드 템플릿을 작성하는 대신, 많은 개발자들은 React나 Vue를 사용한 템플릿 작성을 선호하기도 합니다. 라라벨에서는 [Inertia](https://inertiajs.com/)라는 라이브러리를 통해, 복잡한 SPA 빌드 과정 없이 React 또는 Vue 프론트엔드를 라라벨 백엔드에 쉽고 편리하게 연결할 수 있습니다.

라라벨의 [React 및 Vue 애플리케이션 스타터 키트](/docs/12.x/starter-kits)는 Inertia 기반의 새로운 라라벨 프로젝트를 시작할 때 훌륭한 기반을 제공합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 직접 생성하거나, `make:view` 아티즌 명령어를 사용해 뷰를 만들 수 있습니다.

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/12.x/blade)임을 프레임워크에 알립니다. Blade 템플릿에는 일반 HTML과 함께 Blade 지시어를 포함할 수 있어, 값 출력, if문 작성, 데이터 반복 등 다양한 작업이 가능합니다.

뷰를 생성한 뒤에는, 애플리케이션의 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 해당 뷰를 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한 `View` 파사드를 이용해 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

여기서 첫 번째 인수는 `resources/views` 디렉터리에 있는 뷰 파일명을, 두 번째 인수는 뷰에 사용할 데이터 배열을 의미합니다. 예제에서는 `name` 변수를 전달하고, 이 값은 [Blade 문법](/docs/12.x/blade)을 통해 뷰에서 표시됩니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰 파일은 `resources/views` 하위의 서브디렉터리에도 배치할 수 있습니다. 중첩된 뷰를 참조할 때는 "도트(`.`) 표기법"을 사용합니다. 예를 들어, 뷰 파일이 `resources/views/admin/profile.blade.php`에 있으면, 라우트나 컨트롤러에서 아래와 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에는 `.` 문자를 포함하면 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 가장 먼저 존재하는 뷰 반환

`View` 파사드의 `first` 메서드를 사용하면, 여러 개의 뷰 중에서 가장 먼저 존재하는 뷰를 반환할 수 있습니다. 이 기능은 애플리케이션이나 패키지에서 뷰를 커스터마이징(재정의) 할 수 있도록 할 때 유용합니다.

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

특정 뷰가 존재하는지 확인해야 할 경우, `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 해당 뷰가 있으면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞선 예시에서 보았듯이, 데이터 배열을 뷰에 전달하여 원하는 값을 뷰에서 사용할 수 있습니다.

```php
return view('greetings', ['name' => 'Victoria']);
```

이런 방식으로 데이터를 전달할 때는, 키/값 쌍으로 이루어진 배열 형태여야 합니다. 뷰에서 데이터를 전달한 후에는, 해당 키를 사용하여 뷰 내에서 값에 접근할 수 있습니다. 예를 들어 `<?php echo $name; ?>`처럼 사용할 수 있습니다.

전체 데이터 배열을 한 번에 전달하는 대신, `with` 메서드를 사용해 뷰에 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 체이닝하여 메서드를 이어서 사용할 수 있습니다.

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유

때로는 애플리케이션에서 렌더링되는 모든 뷰에 동일한 데이터를 공유해야 할 때가 있습니다. 이 경우, `View` 파사드의 `share` 메서드를 사용하면 됩니다. 보통 각 서비스 프로바이더의 `boot` 메서드에서 `share` 메서드를 호출합니다. 직접 `App\Providers\AppServiceProvider` 클래스에 추가하거나, 별도의 서비스 프로바이더를 생성하여 관리할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션의 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션의 부트스트랩 처리.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## 뷰 컴포저(View Composer)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰에서 항상 필요한 데이터를 바인딩하고자 한다면, 뷰 컴포저를 이용해 관련 로직을 한 곳에 모아 관리할 수 있습니다. 여러 라우트나 컨트롤러에서 동일한 뷰를 반환하면서, 항상 특정 데이터가 필요할 때 특히 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나에 등록합니다. 여기서는 `App\Providers\AppServiceProvider` 내에 관련 로직을 구현한다고 가정하겠습니다.

뷰 컴포저를 등록할 때는 `View` 파사드의 `composer` 메서드를 사용합니다. 라라벨에는 클래스 기반 뷰 컴포저를 위한 기본 디렉터리가 정해져 있지 않으므로, 여러분이 원하는 방식으로 구조화하면 됩니다. 예를 들어, `app/View/Composers` 디렉터리에 모든 뷰 컴포저 클래스를 저장할 수 있습니다.

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
     * 애플리케이션의 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션의 부트스트랩 처리.
     */
    public function boot(): void
    {
        // 클래스 기반 컴포저 등록
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저(익명 함수) 기반 컴포저 등록
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

이렇게 컴포저를 등록하면, 이제 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 `profile` 뷰가 렌더링될 때마다 실행됩니다. 아래는 컴포저 클래스의 예시입니다.

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * 새로운 프로필 컴포저 인스턴스 생성자.
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

보시는 것처럼, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/12.x/container)를 통해 의존성 주입이 가능하므로, 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 하나의 컴포저 연결하기

하나의 뷰 컴포저를 여러 뷰에 동시에 적용하려면, `composer` 메서드의 첫 번째 인수로 뷰 목록 배열을 전달하면 됩니다.

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한, `composer` 메서드는 모든 뷰에 대해 컴포저를 적용할 수 있도록 `*` 와일드카드 문자도 지원합니다.

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creator)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아닌 뷰 인스턴스가 생성되자마자 바로 실행된다는 점이 다릅니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 이용하면 됩니다.

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 요청 시점에 필요할 때마다 컴파일됩니다. 어떤 뷰를 렌더링해야 할 요청이 발생하면, 라라벨은 해당 뷰의 컴파일된 파일이 존재하는지 확인합니다. 존재한다면, 원본 뷰 파일이 컴파일된 파일보다 더 최근에 수정되었는지를 체크하고, 컴파일된 뷰가 없거나 원본이 더 최신이라면 뷰를 다시 컴파일합니다.

요청 중에 뷰를 컴파일하는 과정은 성능에 다소 영향을 줄 수 있습니다. 이를 개선하기 위해 라라벨은 `view:cache` 아티즌 명령어를 제공하며, 이 명령을 실행하면 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일할 수 있습니다. 좀 더 나은 성능을 위해서, 배포 프로세스 중 이 명령을 실행해 두는 것을 추천합니다.

```shell
php artisan view:cache
```

뷰 캐시를 초기화하거나 제거할 때는 다음과 같이 `view:clear` 명령어를 사용할 수 있습니다.

```shell
php artisan view:clear
```
