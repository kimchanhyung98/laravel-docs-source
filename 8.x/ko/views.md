# 뷰 (Views)

- [소개](#introduction)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉터리](#nested-view-directories)
    - [사용 가능한 첫 번째 뷰 생성](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달](#passing-data-to-views)
    - [모든 뷰와 데이터 공유](#sharing-data-with-all-views)
- [뷰 컴포저(View Composers)](#view-composers)
    - [뷰 크리에이터(View Creators)](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론, 라우트나 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 것은 비효율적입니다. 다행히도 뷰는 모든 HTML 코드를 별도의 파일로 분리할 수 있는 편리한 방법을 제공합니다. 뷰는 컨트롤러나 애플리케이션 로직과 프레젠테이션(화면 표시) 로직을 분리하며, `resources/views` 디렉터리에 저장됩니다. 간단한 뷰 예시는 다음과 같습니다:

```html
<!-- resources/views/greeting.blade.php에 저장된 뷰 -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php` 경로에 저장되어 있으므로, 전역 헬퍼 함수 `view`를 사용해 다음과 같이 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!TIP]
> Blade 템플릿 작성 방법에 대해 더 알고 싶다면, [Blade 문서](/docs/{{version}}/blade)를 참고하세요.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating & Rendering Views)

애플리케이션의 `resources/views` 디렉터리에 `.blade.php` 확장자를 가진 파일을 생성하여 뷰를 만들 수 있습니다. `.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/{{version}}/blade)임을 프레임워크에 알려줍니다. Blade 템플릿은 HTML과 Blade 지시어(directives)를 포함하며, 이를 통해 값을 쉽게 출력하거나, if 문 작성, 데이터 반복 처리 등이 가능합니다.

뷰를 만든 후에는, 전역 헬퍼 함수 `view`를 사용해 앱의 라우트나 컨트롤러에서 뷰를 반환할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또한, `View` 파사드(facade)를 통해 뷰를 반환할 수도 있습니다:

```
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피, `view` 헬퍼의 첫 번째 인자는 `resources/views` 내의 뷰 파일 이름과 일치하며, 두 번째 인자는 뷰에 전달할 데이터를 포함한 배열입니다. 위 예시에서는 `name` 변수를 전달했고, Blade 구문을 통해 뷰 안에서 출력합니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉터리 (Nested View Directories)

뷰는 `resources/views` 디렉터리 안에 서브디렉터리(하위 폴더)로도 저장할 수 있습니다. 이런 중첩된 뷰는 "닷(.) 표기법"을 사용해 참조합니다. 예를 들어, 뷰 파일이 `resources/views/admin/profile.blade.php`에 있다면, 다음과 같이 뷰를 반환할 수 있습니다:

```
return view('admin.profile', $data);
```

> [!NOTE]
> 뷰 디렉터리 이름에 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 사용 가능한 첫 번째 뷰 생성 (Creating The First Available View)

`View` 파사드의 `first` 메서드를 사용하면, 주어진 뷰 이름 배열 중에서 가장 먼저 존재하는 뷰를 반환할 수 있습니다. 이는 애플리케이션이나 패키지가 사용자 정의 또는 덮어쓰기가 가능한 뷰를 제공할 때 유용합니다:

```
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인 (Determining If A View Exists)

뷰가 존재하는지 확인해야 할 때는 `View` 파사드의 `exists` 메서드를 사용하세요. 뷰가 존재하면 `true`를 반환합니다:

```
use Illuminate\Support\Facades\View;

if (View::exists('emails.customer')) {
    //
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달 (Passing Data To Views)

앞선 예시에서 보았듯이, 뷰에 데이터를 전달하려면 키-값 쌍을 가진 배열 형태로 데이터를 넘깁니다. 이렇게 하면 뷰 내에서 키 이름으로 데이터를 접근할 수 있습니다:

```
return view('greetings', ['name' => 'Victoria']);
```

이 경우, 뷰에서는 `<?php echo $name; ?>` 형식으로 값을 사용할 수 있습니다.

전체 데이터를 배열로 전달하는 대신 `with` 메서드를 통해 뷰에 개별 데이터를 추가할 수도 있습니다. `with`는 뷰 객체 인스턴스를 반환하므로, 메서드를 연쇄 호출(chaining)할 수 있습니다:

```
return view('greeting')
            ->with('name', 'Victoria')
            ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰와 데이터 공유 (Sharing Data With All Views)

때때로 애플리케이션의 모든 뷰에 공통 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용하세요. 일반적으로 서비스 프로바이더의 `boot` 메서드에 작성합니다. 기본 제공 프로바이더인 `App\Providers\AppServiceProvider`에 추가하거나, 별도의 서비스 프로바이더를 만들어도 됩니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
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
## 뷰 컴포저(View Composers)

뷰 컴포저는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 뷰가 렌더링될 때마다 특정 데이터를 뷰에 바인딩해야 한다면, 뷰 컴포저를 사용해 관련 로직을 한 곳에 모아 관리할 수 있습니다. 같은 뷰가 애플리케이션의 여러 라우트나 컨트롤러에서 반복 반환되고 항상 특정 데이터가 필요할 때 매우 유용합니다.

보통 뷰 컴포저는 앱의 [서비스 프로바이더](/docs/{{version}}/providers) 중 한 곳에 등록합니다. 예를 들어, `App\Providers\ViewServiceProvider` 클래스를 만들어 관련 로직을 담당하게 할 수 있습니다.

`View` 파사드의 `composer` 메서드를 사용해 뷰 컴포저를 등록합니다. Laravel은 기본 클래스 기반 뷰 컴포저 디렉터리를 제공하지 않으므로, 마음대로 조직할 수 있습니다. 예를 들어, 앱 내에 `app/View/Composers` 디렉터리를 만들어 뷰 컴포저들을 보관할 수 있습니다:

```
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ViewServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        // 클래스 기반 컴포저 사용...
        View::composer('profile', ProfileComposer::class);

        // 클로저(익명 함수) 기반 컴포저 사용...
        View::composer('dashboard', function ($view) {
            //
        });
    }
}
```

> [!NOTE]
> 뷰 컴포저 등록을 위한 새 서비스 프로바이더를 생성했다면, `config/app.php` 파일의 `providers` 배열에 해당 서비스를 추가해야 합니다.

컴포저가 등록되고 나면, `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 `profile` 뷰가 렌더링될 때마다 호출됩니다. 다음은 예시 컴포저 클래스입니다:

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
     * 새로운 프로필 컴포저 생성자.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        // 서비스 컨테이너가 의존성을 자동으로 해결해줍니다...
        $this->users = $users;
    }

    /**
     * 뷰에 데이터 바인딩.
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

모든 뷰 컴포저는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해결되므로, 생성자에 필요한 의존성을 타입 힌트로 선언할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 컴포저 연결하기

뷰 컴포저를 한 번에 여러 뷰에 연결하려면 `composer` 메서드 첫 번째 인자로 뷰 배열을 전달하면 됩니다:

```
use App\Views\Composers\MultiComposer;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

`composer` 메서드는 와일드카드(*) 문자도 받아 모든 뷰에 컴포저를 연결할 수 있습니다:

```
View::composer('*', function ($view) {
    //
});
```

<a name="view-creators"></a>
### 뷰 크리에이터(View Creators)

뷰 "크리에이터"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아니라 뷰 인스턴스가 생성된 직후에 실행됩니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 필요할 때마다 컴파일됩니다. 뷰를 렌더링하는 요청이 들어오면, Laravel은 미리 컴파일된 뷰가 존재하는지 확인합니다. 만약 컴파일된 뷰가 없거나, 원본 뷰 파일이 컴파일된 뷰보다 최신이라면, Laravel은 뷰를 다시 컴파일합니다.

요청 시마다 뷰를 컴파일하는 것은 성능에 약간의 부담이 될 수 있으므로, Laravel은 애플리케이션에서 사용하는 모든 뷰를 미리 컴파일하는 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해 배포 과정에서 이 명령어를 실행하는 것이 좋습니다:

```
php artisan view:cache
```

반대로 뷰 캐시를 삭제하려면 `view:clear` 명령어를 사용하세요:

```
php artisan view:clear
```