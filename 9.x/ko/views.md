# 뷰(Views)

- [소개](#introduction)
    - [React / Vue에서 뷰 작성하기](#writing-views-in-react-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [첫 번째 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저](#view-composers)
    - [뷰 크리에이터](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

물론 라우트와 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 실용적이지 않습니다. 다행히도, 뷰는 모든 HTML을 별도의 파일에 배치할 수 있도록 편리한 방법을 제공합니다.

뷰는 컨트롤러/애플리케이션 로직과 표현 로직을 분리하며, `resources/views` 디렉터리에 저장됩니다. Laravel을 사용할 때 뷰 템플릿은 보통 [Blade 템플릿 언어](/docs/{{version}}/blade)를 사용하여 작성합니다. 간단한 뷰는 다음과 같이 생겼을 수 있습니다:

```blade
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 글로벌 `view` 헬퍼를 사용해 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

> **참고**  
> Blade 템플릿 작성법에 대해 더 알고 싶으신가요? 전체 [Blade 문서](/docs/{{version}}/blade)를 참고하세요.

<a name="writing-views-in-react-or-vue"></a>
### React / Vue에서 뷰 작성하기

많은 개발자들이 PHP의 Blade 대신 React 또는 Vue로 프론트엔드 템플릿을 작성하는 방식을 선호하기 시작했습니다. Laravel은 [Inertia](https://inertiajs.com/)라는 라이브러리를 통해 React / Vue 프론트엔드를 Laravel 백엔드와 쉽게 연결할 수 있도록 해줍니다. 이로써 일반적인 SPA 구축의 복잡함 없이 손쉽게 통합할 수 있습니다.

Breeze와 Jetstream [스타터 키트](/docs/{{version}}/starter-kits)는 Inertia 기반의 새로운 Laravel 애플리케이션을 위한 훌륭한 출발점을 제공합니다. 또한, [Laravel 부트캠프](https://bootcamp.laravel.com)는 Inertia를 기반으로 한 Laravel 애플리케이션 구축 과정을 Vue 및 React 예제와 함께 완전히 시연합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링

`.blade.php` 확장자를 가진 파일을 애플리케이션의 `resources/views` 디렉터리에 생성하여 뷰를 만들 수 있습니다. `.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알립니다. Blade 템플릿에서는 HTML과 함께 값을 쉽게 출력하고, 조건문("if"), 데이터 반복 등 다양한 Blade 디렉티브를 사용할 수 있습니다.

뷰를 생성한 후에는 아래와 같이 애플리케이션의 라우트나 컨트롤러에서 글로벌 `view` 헬퍼를 사용해 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

또는 `View` 파사드를 사용해 반환할 수도 있습니다:

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

위에서 알 수 있듯, `view` 헬퍼의 첫 번째 인자는 `resources/views` 디렉터리 내의 뷰 파일 이름과 일치합니다. 두 번째 인자는 뷰에서 사용할 수 있도록 전달할 데이터의 배열입니다. 이 예제에서는 뷰에서 [Blade 문법](/docs/{{version}}/blade)으로 표시되는 `name` 변수를 전달하고 있습니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰는 `resources/views` 디렉터리의 하위 디렉터리에 중첩해서 저장할 수 있습니다. 중첩 뷰 참조 시 "점(.)" 표기법을 사용할 수 있습니다. 예를 들어, 뷰가 `resources/views/admin/profile.blade.php`에 저장되어 있다면 아래와 같이 반환할 수 있습니다:

    return view('admin.profile', $data);

> **경고**  
> 뷰 디렉터리 이름에는 `.` 문자를 사용하지 마세요.

<a name="creating-the-first-available-view"></a>
### 첫 번째 사용 가능한 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면 주어진 뷰 배열 중 사용 가능한 첫 번째 뷰를 반환할 수 있습니다. 이는 애플리케이션 또는 패키지에서 뷰를 커스터마이즈하거나 오버라이드할 수 있도록 할 때 유용합니다:

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

특정 뷰가 존재하는지 확인하려면 `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 뷰가 존재하면 `true`를 반환합니다:

    use Illuminate\Support\Facades\View;

    if (View::exists('emails.customer')) {
        //
    }

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞서 본 예제와 같이 뷰에 데이터를 전달하여 해당 데이터를 뷰 내에서 사용할 수 있습니다:

    return view('greetings', ['name' => 'Victoria']);

이와 같이 정보를 전달할 때 데이터는 키/값 쌍의 배열이어야 합니다. 뷰에 데이터를 제공하면 뷰 내부에서 `<?php echo $name; ?>`와 같이 각 값을 키를 통해 접근할 수 있습니다.

`view` 헬퍼 함수에 전체 배열을 전달하는 대신, `with` 메서드를 사용해 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하여 뷰를 반환하기 전에 메서드 체이닝을 계속할 수 있습니다:

    return view('greeting')
                ->with('name', 'Victoria')
                ->with('occupation', 'Astronaut');

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

간혹 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용하면 됩니다. 일반적으로 `share` 메서드 호출은 서비스 프로바이더의 `boot` 메서드 내에 배치하는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나 별도의 서비스 프로바이더를 생성하여 관리할 수도 있습니다:

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

<a name="view-composers"></a>
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 바인딩해야 하는 데이터가 있다면, 뷰 컴포저를 사용하여 해당 로직을 한 곳에 정리할 수 있습니다. 동일한 뷰가 애플리케이션의 여러 라우트나 컨트롤러에서 반환되고 항상 특정 데이터가 필요할 때 특히 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers)에서 등록합니다. 예시에서는 이 로직을 담기 위한 새로운 `App\Providers\ViewServiceProvider`를 생성했다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록할 수 있습니다. Laravel에는 클래스 기반 뷰 컴포저를 위한 기본 디렉터리가 없으므로, 원하는 대로 구성할 수 있습니다. 예를 들어, 애플리케이션의 모든 뷰 컴포저를 보관할 `app/View/Composers` 디렉터리를 생성할 수 있습니다:

    <?php

    namespace App\Providers;

    use App\View\Composers\ProfileComposer;
    use Illuminate\Support\Facades\View;
    use Illuminate\Support\ServiceProvider;

    class ViewServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         *
         * @return void
         */
        public function boot()
        {
            // 클래스 기반 컴포저 사용...
            View::composer('profile', ProfileComposer::class);

            // 클로저 기반 컴포저 사용...
            View::composer('dashboard', function ($view) {
                //
            });
        }
    }

> **경고**  
> 뷰 컴포저 등록을 위한 새로운 서비스 프로바이더를 만든 경우 `config/app.php` 파일의 `providers` 배열에 서비스 프로바이더를 추가해야 합니다.

이제 컴포저를 등록했으므로, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 예시 컴포저 클래스는 다음과 같습니다:

    <?php

    namespace App\View\Composers;

    use App\Repositories\UserRepository;
    use Illuminate\View\View;

    class ProfileComposer
    {
        /**
         * 사용자 레포지토리 인스턴스
         *
         * @var \App\Repositories\UserRepository
         */
        protected $users;

        /**
         * 새로운 프로필 컴포저 인스턴스 생성
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * 뷰에 데이터 바인딩
         *
         * @param  \Illuminate\View\View  $view
         * @return void
         */
        public function compose(View $view)
        {
            $view->with('count', $this->users->count());
        }
    }

보다시피 모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 컴포저의 생성자에서 필요한 의존성을 타입힌트로 받을 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

하나의 뷰 컴포저를 여러 뷰에 한 번에 연결할 수 있습니다. 이때 `composer` 메서드의 첫 번째 인자로 뷰의 배열을 전달합니다:

    use App\Views\Composers\MultiComposer;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

`composer` 메서드는 `*` 문자를 와일드카드로 허용하여 모든 뷰에 컴포저를 연결할 수도 있습니다:

    View::composer('*', function ($view) {
        //
    });

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 비슷하지만, 렌더링 직전에 실행되는 대신 뷰가 인스턴스화된 직후에 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 요청 시 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면, Laravel은 뷰의 컴파일된 버전이 존재하는지 확인합니다. 파일이 존재한다면, 컴파일되지 않은 원본 뷰가 컴파일된 뷰보다 최근에 수정되었는지도 확인합니다. 컴파일된 뷰가 존재하지 않거나, 원본 뷰가 더 최근에 수정된 경우에는 Laravel이 뷰를 다시 컴파일합니다.

요청 시 뷰를 컴파일하면 성능에 약간의 부정적인 영향을 줄 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` 아티즌 명령어를 제공합니다. 더 나은 성능을 위해 이 명령을 배포 과정의 일부로 실행할 수 있습니다:

```shell
php artisan view:cache
```

뷰 캐시를 비우려면 `view:clear` 명령어를 사용하세요:

```shell
php artisan view:clear
```