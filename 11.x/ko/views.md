# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [첫 번째로 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

라우트(route)나 컨트롤러(controller)에서 바로 전체 HTML 문서를 문자열로 반환하는 것은 비효율적입니다. 다행히도, 뷰(View)는 모든 HTML을 별도의 파일에 저장할 수 있는 편리한 방법을 제공합니다.

뷰는 컨트롤러/애플리케이션의 로직과 프레젠테이션 로직을 분리해주며, `resources/views` 디렉터리에 저장됩니다. Laravel을 사용할 때, 뷰 템플릿은 주로 [Blade 템플릿 언어](/docs/{{version}}/blade)를 사용하여 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있다면, 글로벌 `view` 헬퍼를 사용하여 다음과 같이 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

> [!NOTE]
> Blade 템플릿 작성 방법에 대해 더 자세히 알고 싶으신가요? [Blade 공식 문서](/docs/{{version}}/blade)를 참고해 시작할 수 있습니다.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자들이 Blade로 PHP에서 프론트엔드 템플릿을 작성하는 대신 React나 Vue를 통해 템플릿을 작성하는 것을 선호합니다. Laravel에서는 [Inertia](https://inertiajs.com/) 덕분에 React / Vue 프론트엔드를 Laravel 백엔드에 복잡한 SPA 구축 과정을 거치지 않고 쉽게 연결할 수 있습니다.

Breeze와 Jetstream [스타터 키트](/docs/{{version}}/starter-kits)는 Inertia로 동작하는 신규 Laravel 애플리케이션의 훌륭한 출발점을 제공합니다. 또한, [Laravel Bootcamp](https://bootcamp.laravel.com)에서는 Vue 및 React 예제를 포함해 Inertia 기반 Laravel 애플리케이션 구축 과정을 자세히 설명합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`.blade.php` 확장자 파일을 애플리케이션의 `resources/views` 디렉터리에 추가하거나, `make:view` 아티즌(Artisan) 명령어를 사용해 뷰를 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알립니다. Blade 템플릿에는 HTML과 Blade 지시문(디렉티브)을 함께 사용할 수 있어, 값 출력, if문, 반복문 등을 쉽게 다룰 수 있습니다.

뷰 파일을 생성했다면, 글로벌 `view` 헬퍼를 통해 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

뷰는 `View` 파사드(facade)를 이용해 반환할 수도 있습니다:

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

보시듯이 `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리의 뷰 파일 이름에 해당합니다. 두 번째 인자는 뷰에서 사용할 수 있는 데이터 배열입니다. 이 예시에서는 뷰에서 [Blade 문법](/docs/{{version}}/blade)으로 출력되는 `name` 변수를 전달합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰는 `resources/views` 하위의 서브디렉터리에 중첩되어 저장할 수 있습니다. 중첩 뷰를 참조할 때는 "점 표기법(dot notation)"을 사용할 수 있습니다. 예를 들어, `resources/views/admin/profile.blade.php`에 뷰가 저장되어 있다면:

    return view('admin.profile', $data);

> [!WARNING]
> 뷰 디렉터리 이름에는 `.`(점) 문자를 사용해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 첫 번째로 사용 가능한 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하여 주어진 뷰 배열에서 처음으로 존재하는 뷰를 반환할 수 있습니다. 이는 패키지나 애플리케이션에서 뷰를 커스터마이즈하거나 덮어쓸 수 있도록 할 때 유용합니다:

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기

뷰가 존재하는지 확인해야 할 경우, `View` 파사드의 `exists` 메서드를 사용할 수 있습니다. 해당 뷰가 있으면 `true`를 반환합니다:

    use Illuminate\Support\Facades\View;

    if (View::exists('admin.profile')) {
        // ...
    }

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞의 예시에서 보았듯이, 데이터 배열을 뷰에 전달해 해당 뷰에서 사용할 수 있게 할 수 있습니다:

    return view('greetings', ['name' => 'Victoria']);

이 방식으로 데이터를 전달할 때는 키/값 쌍으로 이루어진 배열이어야 하며, 뷰에서는 해당 키 이름을 이용해 값을 사용할 수 있습니다(예: `<?php echo $name; ?>`).

`view` 헬퍼에 배열 전체를 전달하는 대신, `with` 메서드를 사용해 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로, 메서드 체이닝을 통해 여러 데이터를 연속적으로 추가할 수 있습니다:

    return view('greeting')
        ->with('name', 'Victoria')
        ->with('occupation', 'Astronaut');

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

애플리케이션에서 렌더링하는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이를 위해 `View` 파사드의 `share` 메서드를 사용할 수 있습니다. 일반적으로 `share` 메서드 호출은 서비스 프로바이더(Service Provider)의 `boot` 메서드에 작성합니다. 기본적으로 `App\Providers\AppServiceProvider` 클래스에 추가하거나, 별도의 서비스 프로바이더를 생성해 관리할 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 필요한 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 필요한 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            View::share('key', 'value');
        }
    }

<a name="view-composers"></a>
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 실행되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 항상 데이터가 바인딩되어야 한다면 뷰 컴포저를 사용해 이러한 로직을 한 곳에 모아두는 것이 좋습니다. 뷰 컴포저는 여러 라우트나 컨트롤러에서 동일한 뷰를 반환하면서 특정 데이터를 항상 필요로 할 때 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나에 등록합니다. 이 예시에서는 `App\Providers\AppServiceProvider`에 해당 로직이 포함된다고 가정합니다.

`View` 파사드의 `composer` 메서드를 통해 뷰 컴포저를 등록할 수 있습니다. Laravel에는 클래스 기반 뷰 컴포저를 위한 기본 디렉터리가 지정되어 있지 않으므로 자유롭게 디렉터리를 만들어 정리하면 됩니다. 예를 들어, `app/View/Composers` 디렉터리를 생성해 모든 뷰 컴포저 클래스를 관리할 수 있습니다:

    <?php

    namespace App\Providers;

    use App\View\Composers\ProfileComposer;
    use Illuminate\Support\Facades;
    use Illuminate\Support\ServiceProvider;
    use Illuminate\View\View;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 필요한 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 필요한 애플리케이션 서비스 부트스트랩
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

이제 컴포저가 등록되었으니, `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드는 `profile` 뷰가 렌더링될 때마다 호출됩니다. 컴포저 클래스 예시는 다음과 같습니다:

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

보시다시피, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 컴포저 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

`composer` 메서드의 첫 번째 인자로 뷰 배열을 전달하면 여러 뷰에 동시에 컴포저를 연결할 수 있습니다:

    use App\Views\Composers\MultiComposer;
    use Illuminate\Support\Facades\View;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

`composer` 메서드는 `*` 문자를 와일드카드로 허용하여, 모든 뷰에 컴포저를 적용할 수도 있습니다:

    use Illuminate\Support\Facades;
    use Illuminate\View\View;

    Facades\View::composer('*', function (View $view) {
        // ...
    });

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 비슷하지만, 뷰가 인스턴스화된 직후 즉시 실행된다는 차이가 있습니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 필요에 따라 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면, Laravel은 컴파일된 뷰 버전이 존재하는지 확인합니다. 컴파일된 파일이 있으면 기존 Blade 파일이 그 이후에 수정되었는지 확인하며, 컴파일된 파일이 없거나 원본 Blade 파일이 더 최근에 수정된 경우, Laravel은 뷰를 다시 컴파일합니다.

요청 시 뷰를 컴파일하면 성능에 약간의 영향을 줄 수 있으므로, Laravel은 모든 뷰를 미리 컴파일하는 `view:cache` 아티즌 명령어를 제공합니다. 성능 향상을 위해 배포(deployment) 과정에 이 명령어를 포함하는 것이 좋습니다:

```shell
php artisan view:cache
```

뷰 캐시를 비우려면 `view:clear` 명령어를 사용할 수 있습니다:

```shell
php artisan view:clear
```
