# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [첫 번째 사용 가능한 뷰 생성](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composer)](#view-composers)
    - [뷰 크리에이터(View Creator)](#view-creators)
- [뷰 최적화하기](#optimizing-views)

<a name="introduction"></a>
## 소개

라우트나 컨트롤러에서 직접 전체 HTML 문서 문자열을 반환하는 것은 현실적이지 않습니다. 다행히도, 뷰(View)는 모든 HTML을 별도의 파일에 작성할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러/애플리케이션 로직을 프레젠테이션 로직으로부터 분리해 주며, `resources/views` 디렉터리에 저장됩니다. Laravel에서는 보통 뷰 템플릿을 [Blade 템플릿 언어](/docs/{{version}}/blade)를 사용하여 작성합니다. 간단한 뷰는 다음과 같습니다.

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 글로벌 `view` 헬퍼를 사용하여 반환할 수 있습니다.

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

> [!NOTE]  
> Blade 템플릿 작성 방법에 대해 더 알고 싶으신가요? 전체 [Blade 문서](/docs/{{version}}/blade)를 확인해보세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

Blade로 PHP에서 프론트엔드 템플릿을 작성하는 대신, 많은 개발자들은 React나 Vue로 템플릿을 작성하는 것을 선호합니다. [Inertia](https://inertiajs.com/) 라이브러리를 사용하면, Laravel 백엔드와 React/Vue 프론트엔드를 별도의 복잡성 없이 쉽게 연결할 수 있습니다.

Breeze, Jetstream [스타터 키트](/docs/{{version}}/starter-kits)는 Inertia를 기반으로 한 신규 Laravel 애플리케이션의 훌륭한 출발점을 제공합니다. 또한, [Laravel Bootcamp](https://bootcamp.laravel.com)에서는 Inertia를 이용한 Laravel 애플리케이션 개발 과정을 Vue, React 예시와 함께 상세히 다루고 있습니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 생성하거나 `make:view` 아티즌 명령어를 사용하여 뷰를 만들 수 있습니다.

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알립니다. Blade 템플릿은 HTML과 Blade 디렉티브를 함께 포함하며, 값을 출력하거나, "if" 문을 작성하거나, 데이터를 순회하는 등 다양한 기능을 지원합니다.

뷰를 만들었다면, 글로벌 `view` 헬퍼를 사용하여 라우트 또는 컨트롤러에서 해당 뷰를 반환할 수 있습니다.

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

`View` 파사드(Facade)를 사용하여 뷰를 반환할 수도 있습니다.

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

보시다시피, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리 내 뷰 파일의 이름과 일치합니다. 두 번째 인자는 뷰에서 사용할 수 있는 데이터 배열입니다. 이 예시에서는 `name` 변수를 전달하며, 뷰 내에서 [Blade 문법](/docs/{{version}}/blade)으로 출력합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰는 `resources/views`의 서브디렉터리 내에 중첩해서 저장할 수 있습니다. "닷(dot) 표기법"을 이용하면 중첩된 뷰를 참조할 수 있습니다. 예를 들어, 뷰가 `resources/views/admin/profile.blade.php`에 저장되어 있다면, 다음과 같이 반환할 수 있습니다.

    return view('admin.profile', $data);

> [!WARNING]  
> 뷰 디렉터리 이름에 `.` 문자를 포함하지 않도록 하세요.

<a name="creating-the-first-available-view"></a>
### 첫 번째 사용 가능한 뷰 생성

`View` 파사드의 `first` 메서드를 사용하면 여러 뷰 배열에서 첫 번째로 존재하는 뷰를 반환할 수 있습니다. 이는 애플리케이션 또는 패키지가 뷰를 재정의하거나 커스터마이징할 수 있을 때 유용합니다.

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

특정 뷰가 존재하는지 확인해야 할 경우, `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 뷰가 존재하면 `true`를 반환합니다.

    use Illuminate\Support\Facades\View;

    if (View::exists('admin.profile')) {
        // ...
    }

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞선 예시에서처럼, 뷰에 데이터를 전달하여 뷰 내에서 해당 데이터를 사용할 수 있습니다.

    return view('greetings', ['name' => 'Victoria']);

이때 데이터는 키/값 쌍의 배열이어야 합니다. 뷰에 데이터를 제공한 후에는, 해당 키를 사용하여 뷰 내에서 값을 참조할 수 있습니다. 예: `<?php echo $name; ?>`

별도의 데이터 배열을 전달하는 대신, `with` 메서드를 사용하여 개별 데이터를 뷰에 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 추가로 메서드 체이닝이 가능합니다.

    return view('greeting')
                ->with('name', 'Victoria')
                ->with('occupation', 'Astronaut');

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

때로는 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 수도 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 일반적으로, 이러한 코드는 서비스 프로바이더의 `boot` 메서드 내에 작성합니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나, 별도의 서비스 프로바이더를 만들어서 작성해도 됩니다.

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
         * 애플리케이션 서비스의 부트스트랩을 처리합니다.
         */
        public function boot(): void
        {
            View::share('key', 'value');
        }
    }

<a name="view-composers"></a>
## 뷰 컴포저(View Composer)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 뷰가 렌더될 때마다 특정 데이터를 항상 바인딩해야 한다면, 뷰 컴포저를 통해 해당 로직을 한 곳에 모아서 관리할 수 있습니다. 동일한 뷰가 여러 라우트나 컨트롤러에서 반환될 때, 항상 특정 데이터를 필요로 할 경우 특히 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)에 등록합니다. 이 예시에서는 `App\Providers\ViewServiceProvider`라는 새 서비스를 만들었다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용하여 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저를 위한 디폴트 디렉터리가 없으므로, 자유롭게 구조를 만들 수 있습니다. 예를 들어, `app/View/Composers` 디렉터리를 만들어 모든 뷰 컴포저를 보관할 수 있습니다.

    <?php

    namespace App\Providers;

    use App\View\Composers\ProfileComposer;
    use Illuminate\Support\Facades;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\View\View;

    class ViewServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 등록합니다.
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 애플리케이션 서비스의 부트스트랩을 처리합니다.
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

> [!WARNING]  
> 뷰 컴포저 등록을 위해 새로운 서비스 프로바이더를 만든 경우, 반드시 `config/app.php` 설정 파일의 `providers` 배열에 해당 프로바이더를 추가해야 합니다.

컴포저를 등록했다면, 이제 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드는 `profile` 뷰가 매번 렌더링될 때마다 실행됩니다. 컴포저 클래스 예시는 아래와 같습니다.

    <?php

    namespace App\View\Composers;

    use App\Repositories\UserRepository;
    use Illuminate\View\View;

    class ProfileComposer
    {
        /**
         * 새로운 프로필 컴포저 인스턴스를 생성합니다.
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

모든 뷰 컴포저 인스턴스는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 생성자에서 필요한 종속성을 타입힌트로 선언할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 배열을 전달하면 여러 뷰에 동시에 컴포저를 연결할 수 있습니다.

    use App\Views\Composers\MultiComposer;
    use Illuminate\Support\Facades\View;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

`composer` 메서드는 `*` 문자를 와일드카드로 받아, 모든 뷰에 컴포저를 연결할 수도 있습니다.

    use Illuminate\Support\Facades;
    use Illuminate\View\View;

    Facades\View::composer('*', function (View $view) {
        // ...
    });

<a name="view-creators"></a>
### 뷰 크리에이터(View Creator)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링 직전이 아니라 인스턴스화된 즉시 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다.

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## 뷰 최적화하기

기본적으로 Blade 템플릿 뷰는 필요할 때마다 컴파일됩니다. 요청 시, Laravel은 컴파일된 뷰가 존재하는지 확인합니다. 만약 존재한다면, 미컴파일 뷰가 컴파일된 뷰보다 더 최근에 수정되었는지 확인합니다. 컴파일된 뷰가 없거나, 미컴파일 뷰가 더 최근에 수정되었다면 Laravel은 뷰를 다시 컴파일합니다.

요청 중에 뷰를 컴파일하면 성능에 약간의 영향을 미칠 수 있으므로, Laravel은 `view:cache` 아티즌 명령어로 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일할 수 있도록 제공합니다. 더 나은 성능을 원한다면, 배포 프로세스의 일부로 이 명령어를 실행하는 것이 좋습니다.

```shell
php artisan view:cache
```

뷰 캐시를 비우려면 `view:clear` 명령어를 사용할 수 있습니다.

```shell
php artisan view:clear
```
