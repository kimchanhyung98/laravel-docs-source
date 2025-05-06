# 뷰(Views)

- [소개](#introduction)
- [뷰 생성 및 렌더링하기](#creating-and-rendering-views)
    - [중첩 뷰 디렉터리](#nested-view-directories)
    - [처음으로 사용 가능한 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인하기](#determining-if-a-view-exists)
- [뷰에 데이터 전달하기](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개

물론, 라우트(route)와 컨트롤러(controller)에서 HTML 문서를 문자열로 직접 반환하는 것은 비효율적입니다. 다행히 뷰(View)는 모든 HTML 코드를 별도의 파일에 쉽게 분리할 수 있도록 편리한 방법을 제공합니다. 뷰는 컨트롤러/애플리케이션 로직과 프리젠테이션(화면 표시) 로직을 분리하며, `resources/views` 디렉터리에 저장됩니다. 간단한 뷰는 다음과 같이 구현할 수 있습니다:

```html
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 전역 `view` 헬퍼(helper)를 사용하여 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

> {tip} Blade 템플릿 작성 방법에 대해 더 알고 싶다면 전체 [Blade 문서](/docs/{{version}}/blade)를 참고하세요.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링하기

애플리케이션의 `resources/views` 디렉터리에 `.blade.php` 확장자를 가진 파일을 생성하여 뷰를 만들 수 있습니다. `.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알립니다. Blade 템플릿에는 HTML과 Blade 지시문이 함께 포함될 수 있어, 값을 바로 출력하거나, "if" 문을 생성하거나, 데이터 반복 등 다양한 작업이 쉽게 가능합니다.

뷰를 생성한 후, 전역 `view` 헬퍼를 사용하여 라우트나 컨트롤러에서 반환할 수 있습니다:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

또한 `View` 파사드(Facade)를 통해서도 뷰를 반환할 수 있습니다:

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

보시다시피, `view` 헬퍼에 전달되는 첫 번째 인자는 `resources/views` 디렉터리 내의 뷰 파일 이름과 대응합니다. 두 번째 인자는 뷰에서 사용할 수 있는 데이터 배열입니다. 이 예시에서는 `name` 변수를 전달하며, 이는 [Blade 문법](/docs/{{version}}/blade)으로 뷰에서 출력합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉터리

뷰 파일들은 `resources/views` 디렉터리 내의 하위 디렉터리에 중첩될 수도 있습니다. 중첩된 뷰는 "닷(dot) 표기법"을 이용해 참조할 수 있습니다. 예를 들어, 뷰가 `resources/views/admin/profile.blade.php`에 저장되어 있으면, 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

    return view('admin.profile', $data);

> {note} 뷰 디렉터리 이름에 `.`(닷) 문자는 사용할 수 없습니다.

<a name="creating-the-first-available-view"></a>
### 처음으로 사용 가능한 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면, 주어진 뷰 배열 중 최초로 존재하는 뷰를 반환할 수 있습니다. 애플리케이션이나 패키지에서 뷰를 커스터마이징하거나 덮어쓸 수 있도록 할 때 유용합니다:

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인하기

특정 뷰가 존재하는지 확인해야 할 경우, `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 해당 뷰가 존재하면 `true`를 반환합니다:

    use Illuminate\Support\Facades\View;

    if (View::exists('emails.customer')) {
        //
    }

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달하기

앞선 예시에서 보았듯, 뷰에 데이터 배열을 전달하여 뷰 내에서 데이터를 사용할 수 있습니다:

    return view('greetings', ['name' => 'Victoria']);

이 방식으로 정보를 전달할 때, 데이터는 key/value 쌍을 갖는 배열이어야 합니다. 뷰에 데이터를 제공한 후에는, 뷰 내에서 해당 키를 사용해 각 값을 접근할 수 있습니다. 예: `<?php echo $name; ?>`.

`view` 헬퍼 함수에 데이터 배열을 모두 전달하는 대신, `with` 메서드를 사용하여 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로 다른 메서드를 체이닝해서 사용할 수 있습니다:

    return view('greeting')
                ->with('name', 'Victoria')
                ->with('occupation', 'Astronaut');

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

때때로, 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용합니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나, 별도의 서비스 프로바이더를 생성하여 관리할 수도 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;

    class AppServiceProvider extends ServiceProvider
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
            View::share('key', 'value');
        }
    }

<a name="view-composers"></a>
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백이나 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 연결하고 싶은 데이터가 있다면, 뷰 컴포저를 사용하면 해당 로직을 한 곳에 모아서 관리할 수 있습니다. 뷰 컴포저는 동일한 뷰가 여러 라우트나 컨트롤러에서 반환될 때 항상 특정 데이터가 필요할 경우 특히 유용합니다.

보통 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 내에 등록합니다. 여기서는 이 로직을 관리할 새로운 `App\Providers\ViewServiceProvider`를 생성했다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel은 클래스 기반 뷰 컴포저를 위한 기본 디렉터리를 제공하지 않으므로, 원하는 구조로 자유롭게 구성할 수 있습니다. 예를 들어, 모든 뷰 컴포저를 위한 `app/View/Composers` 디렉터리를 만들 수 있습니다:

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
            // 클래스 기반 컴포저 예시 ...
            View::composer('profile', ProfileComposer::class);

            // 클로저 기반 컴포저 예시 ...
            View::composer('dashboard', function ($view) {
                //
            });
        }
    }

> {note} 뷰 컴포저 등록을 위한 새 서비스 프로바이더를 만들 경우, 반드시 `config/app.php`의 `providers` 배열에 해당 서비스 프로바이더를 추가해야 합니다.

이제 컴포저가 등록되었으므로, `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. 컴포저 클래스의 예시를 살펴보겠습니다:

    <?php

    namespace App\View\Composers;

    use App\Repositories\UserRepository;
    use Illuminate\View\View;

    class ProfileComposer
    {
        /**
         * 유저 레포지토리 구현체
         *
         * @var \App\Repositories\UserRepository
         */
        protected $users;

        /**
         * 새로운 프로필 컴포저 생성
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            // 서비스 컨테이너가 의존성을 자동으로 주입합니다.
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

보시다시피, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)로부터 해결(resolved)되므로, 컴포저 생성자에서 필요한 의존성을 타입힌트(Type hint)로 명시할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 컴포저를 여러 뷰에 한번에 연결하기

`composer` 메서드의 첫 번째 인자에 뷰의 배열을 전달하면, 여러 뷰에 컴포저를 동시에 연결할 수 있습니다:

    use App\Views\Composers\MultiComposer;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

`composer` 메서드는 와일드카드로 `*` 문자도 허용하므로, 모든 뷰에 컴포저를 연결할 수도 있습니다:

    View::composer('*', function ($view) {
        //
    });

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링 직전에 실행되는 것이 아니라, 인스턴스화된 직후에 바로 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용하세요:

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## 뷰 최적화

기본적으로 Blade 템플릿 뷰는 요청 시점(on demand)에 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면, Laravel은 해당 뷰의 컴파일된 버전이 존재하는지 확인합니다. 만약 파일이 존재한다면, 아직 컴파일되지 않은 뷰 파일이 컴파일된 뷰 파일보다 더 최근에 수정되었는지 추가로 확인합니다. 만약 컴파일된 뷰가 없거나, 원본 파일이 더 최근에 수정된 경우, Laravel이 뷰를 새롭게 컴파일합니다.

요청 중에 뷰를 컴파일하는 것은 성능에 약간의 영향을 줄 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` 아티즌(Artisan) 명령어를 제공합니다. 성능 향상을 위해 이 명령어를 배포(deploy) 과정에 포함하는 것이 좋습니다:

    php artisan view:cache

뷰 캐시를 삭제하려면 `view:clear` 명령어를 사용하세요:

    php artisan view:clear
