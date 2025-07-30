# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 주의사항](#a-note-on-facades)
- [패키지 자동 등록](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정 파일](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [번역 파일](#translations)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
- [커맨드](#commands)
- [공개 자산](#public-assets)
- [파일 그룹 게시](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 날짜를 다루는 훌륭한 라이브러리인 [Carbon](https://github.com/briannesbitt/Carbon)부터, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델과 파일을 연관시켜주는 패키지 등 다양합니다.

패키지는 여러 종류가 있습니다. 일부 패키지는 독립형으로, 어떤 PHP 프레임워크와도 작동합니다. Carbon이나 PHPUnit가 그 예입니다. 이런 패키지들은 `composer.json`에 요구사항으로 추가하여 Laravel에서도 사용할 수 있습니다.

반면, 일부 패키지는 Laravel 전용으로 설계되어, 라우트, 컨트롤러, 뷰 또는 설정이 Laravel 애플리케이션을 보완하도록 만들어져 있습니다. 이 가이드는 주로 Laravel에 특화된 그런 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 주의사항 (A Note On Facades)

Laravel 애플리케이션을 작성할 때는 컨트랙트(contract)나 파사드(facade)를 사용하는 것이 테스트 가능성 측면에서 큰 차이가 없습니다. 하지만 패키지를 작성할 때는 Laravel의 모든 테스트 헬퍼를 이용할 수 없는 경우가 많습니다. 패키지를 마치 일반 Laravel 애플리케이션 내부에 설치된 것처럼 테스트하려면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 등록 (Package Discovery)

Laravel 애플리케이션의 `config/app.php` 설정 파일에서 `providers` 옵션은 Laravel이 로드할 서비스 프로바이더 목록을 정의합니다. 누군가 당신의 패키지를 설치할 때, 보통 서비스 프로바이더를 이 목록에 포함시키길 원합니다. 수동으로 목록에 추가하도록 요구하는 대신, 패키지의 `composer.json` 파일 내 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 파사드도 함께 등록하고 싶다면 다음 예처럼 지정하세요:

```
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},
```

이렇게 자동 등록을 설정하면, 패키지를 설치할 때 Laravel이 서비스 프로바이더와 파사드를 자동으로 등록하여, 사용자가 더 편리하게 설치할 수 있습니다.

<a name="opting-out-of-package-discovery"></a>
### 패키지 자동 등록 비활성화 (Opting Out Of Package Discovery)

패키지를 사용하는 측에서 특정 패키지의 자동 등록을 비활성화하려면, 애플리케이션 `composer.json`의 `extra` 섹션에 해당 패키지명을 나열하면 됩니다:

```
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

모든 패키지에 대해 자동 등록을 끄려면 `*` 문자를 사용할 수 있습니다:

```
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
## 서비스 프로바이더 (Service Providers)

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel을 연결하는 접점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩을 등록하고, 뷰, 설정, 로컬라이제이션 같은 패키지 자원이 어디에서 로드되는지 Laravel에 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으며, 이를 여러분 패키지의 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 파일 (Configuration)

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 게시(publish)해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정을 쉽게 덮어쓸 수 있습니다. 설정 파일을 게시 가능하게 하려면, 서비스 프로바이더의 `boot` 메서드 내에서 `publishes` 메서드를 호출하세요:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정된 위치로 복사됩니다. 게시된 설정 파일 값은 다른 설정 파일과 마찬가지로 접근할 수 있습니다:

```
$value = config('courier.option');
```

> [!NOTE]
> 설정 파일에 클로저를 정의해서는 안 됩니다. `config:cache` Artisan 명령어 실행 시 올바르게 직렬화되지 않기 때문입니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 (Default Package Configuration)

패키지 설정 파일과 애플리케이션에 게시된 설정 파일을 합칠 수 있습니다. 이렇게 하면 사용자가 게시된 설정 파일에서 덮어쓰고자 하는 옵션만 정의할 수 있습니다. 설정 병합은 서비스 프로바이더의 `register` 메서드 내에서 `mergeConfigFrom` 메서드를 사용해 수행합니다.

`mergeConfigFrom`의 첫 번째 인자는 패키지 설정 파일 경로, 두 번째 인자는 애플리케이션 내 설정 이름입니다:

```
/**
 * 애플리케이션 서비스 등록.
 *
 * @return void
 */
public function register()
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!NOTE]
> 이 메서드는 설정 배열의 최상위 레벨만 병합합니다. 다중 차원 배열 구성에서 일부만 정의하면 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있으면, `loadRoutesFrom` 메서드를 사용해 Laravel에 라우트 파일을 불러오는 방법을 알릴 수 있습니다. 이 메서드는 애플리케이션 라우트 캐시 여부를 자동으로 감지해, 이미 캐시된 경우 라우트를 다시 로드하지 않습니다:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `loadMigrationsFrom` 메서드를 사용해 Laravel에게 마이그레이션 경로를 알려줄 수 있습니다. 이 메서드는 패키지 내 마이그레이션 경로만 매개변수로 받습니다:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
}
```

패키지 마이그레이션이 등록되면, `php artisan migrate` 실행 시 자동으로 마이그레이션이 실행됩니다. 애플리케이션의 `database/migrations` 디렉터리에 별도로 복사할 필요가 없습니다.

<a name="translations"></a>
### 번역 파일 (Translations)

패키지에 [번역 파일](/docs/{{version}}/localization)이 포함된 경우, `loadTranslationsFrom` 메서드로 Laravel에게 로드 방법을 알려야 합니다. 예컨대 패키지 이름이 `courier`라면, 다음과 같이 서비스 프로바이더의 `boot` 메서드에 추가하세요:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');
}
```

패키지 번역은 `패키지명::파일명.라인키` 형태로 사용됩니다. 예를 들어 `courier` 패키지의 `messages` 파일 내 `welcome` 키를 불러오려면:

```
echo trans('courier::messages.welcome');
```

<a name="publishing-translations"></a>
#### 번역 파일 게시 (Publishing Translations)

패키지 번역 파일을 애플리케이션의 `resources/lang/vendor` 디렉터리로 게시하고 싶으면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. `publishes`는 패키지 경로와 게시 위치를 배열로 받습니다. 예를 들어 `courier` 패키지 번역 파일을 게시하려면 다음과 같이 작성합니다:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');

    $this->publishes([
        __DIR__.'/../resources/lang' => resource_path('lang/vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` 명령을 실행하면, 번역 파일이 지정한 위치에 복사됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면, 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용해 뷰 경로를 알려야 합니다. 이 메서드는 뷰 템플릿 경로와 패키지 이름 두 개의 인수를 받습니다. 예를 들어 패키지 이름이 `courier`라면, `boot` 메서드에 다음을 추가하세요:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `패키지명::뷰명` 규칙으로 불러옵니다. 따라서 한 번 등록한 후에는 다음처럼 `courier` 패키지의 `dashboard` 뷰를 불러올 수 있습니다:

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드 (Overriding Package Views)

`loadViewsFrom` 메서드 사용 시, Laravel은 뷰를 위해 두 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 지정한 패키지 뷰 디렉터리입니다. 예를 들어 `courier` 패키지라면, 개발자가 `resources/views/vendor/courier`에 맞춤형 뷰를 두었는지 먼저 확인하고, 없으면 패키지의 뷰를 사용합니다. 이를 통해 패키지 사용자가 뷰를 쉽게 커스터마이징할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 게시 (Publishing Views)

뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 게시 가능하게 하려면, 서비스 프로바이더에서 `publishes` 메서드를 사용하세요. 이 메서드는 패키지 내 뷰 경로와 게시 위치를 배열로 받습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 사용자가 `vendor:publish` Artisan 명령어를 실행하면, 패키지 뷰들이 지정 위치에 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

패키지에 [뷰 컴포넌트](/docs/{{version}}/blade#components)가 포함되어 있다면, `loadViewComponentsAs` 메서드로 Laravel에 로드 방법을 알려야 합니다. 이 메서드는 뷰 컴포넌트 태그 접두사와 뷰 컴포넌트 클래스 배열 두 개의 인자를 받습니다. 예를 들어 패키지 접두사가 `courier`이고, `Alert`와 `Button` 컴포넌트를 가진다면 다음과 같이 하면 됩니다:

```
use Courier\Components\Alert;
use Courier\Components\Button;

/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewComponentsAs('courier', [
        Alert::class,
        Button::class,
    ]);
}
```

이렇게 등록하면, 뷰에서 아래와 같이 사용할 수 있습니다:

```
<x-courier-alert />

<x-courier-button />
```

<a name="anonymous-components"></a>
#### 익명 컴포넌트 (Anonymous Components)

익명 컴포넌트가 포함된 경우, 반드시 패키지 뷰 디렉터리 내에 `components` 폴더를 위치시켜야 합니다 (`loadViewsFrom`에 지정한 경로 기준). 그리고 뷰에서는 패키지 뷰 네임스페이스를 접두사로 붙여 다음과 같이 렌더링합니다:

```
<x-courier::alert />
```

<a name="commands"></a>
## 커맨드 (Commands)

패키지 Artisan 커맨드를 Laravel에 등록하려면 `commands` 메서드를 사용하세요. 이 메서드는 커맨드 클래스의 배열을 인수로 받습니다. 등록된 후에는 [Artisan CLI](/docs/{{version}}/artisan)를 통해 실행할 수 있습니다:

```
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a name="public-assets"></a>
## 공개 자산 (Public Assets)

패키지에 JavaScript, CSS, 이미지 같은 공개 자산이 있을 수 있습니다. 이를 애플리케이션의 `public` 디렉터리로 게시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 다음 예시에서는 `public` 자산 그룹 태그도 함께 추가하여 관련 자산 그룹을 쉽게 게시할 수 있습니다:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 패키지 사용자가 `vendor:publish` 명령 실행 시 자산이 지정 경로로 복사됩니다. 패키지 업데이트 시 자주 덮어써야 하므로 `--force` 플래그를 함께 사용할 수 있습니다:

```
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 게시 (Publishing File Groups)

패키지 자산과 리소스를 그룹별로 분리하여 게시하도록 할 수 있습니다. 예를 들어, 패키지 설정 파일만 게시하게 하고 자산까지 강제로 게시하지 않도록 태그를 지정할 수 있습니다. `publishes` 메서드 호출 시 태그를 부여하는 방법이 있습니다. 예를 들어 `courier` 패키지에 대해 `courier-config`와 `courier-migrations` 두 게시 그룹을 등록하는 예:

```
/**
 * 부트스트랩 패키지 서비스들.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishes([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

사용자는 태그를 지정하여 그룹별로 게시할 수 있습니다:

```
php artisan vendor:publish --tag=courier-config
```