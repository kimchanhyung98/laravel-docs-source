# 패키지 개발

- [소개](#introduction)
    - [Facade에 대한 참고](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [번역](#translations)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" Artisan 명령어](#about-artisan-command)
- [커맨드](#commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 주된 방법입니다. 패키지는 날짜를 다루기 위한 강력한 도구인 [Carbon](https://github.com/briannesbitt/Carbon)부터 Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연관지을 수 있게 해주는 것까지 다양합니다.

패키지에는 여러 종류가 있습니다. 일부 패키지는 독립적으로 동작하며, 어떤 PHP 프레임워크에서도 사용할 수 있습니다. Carbon과 PHPUnit가 그 예입니다. 이런 패키지들은 `composer.json` 파일에 추가하여 Laravel에서 사용할 수 있습니다.

반면, 일부 패키지는 Laravel에서만 사용하도록 만들어집니다. 이런 패키지는 라우트, 컨트롤러, 뷰, 설정 등 Laravel 애플리케이션을 향상시키기 위한 요소를 포함할 수 있습니다. 본 가이드에서는 주로 Laravel 전용 패키지 개발을 다룹니다.

<a name="a-note-on-facades"></a>
### Facade에 대한 참고

Laravel 애플리케이션을 작성할 때는 contract나 facade를 사용하는 것이 테스트 가능성 면에서 큰 차이가 없습니다. 하지만, 패키지 작성 시에는 Laravel의 모든 테스트 헬퍼에 접근할 수 없습니다. 만약 패키지 테스트를 일반 Laravel 애플리케이션에 설치된 것처럼 작성하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리

Laravel 애플리케이션의 `config/app.php` 설정 파일의 `providers` 옵션은 Laravel이 로드해야 할 서비스 프로바이더 목록을 정의합니다. 사용자가 패키지를 설치할 때, 일반적으로 서비스 프로바이더를 이 목록에 포함시키기를 원할 것입니다. 사용자가 별도로 서비스 프로바이더를 추가하지 않아도 되도록, 패키지의 `composer.json`의 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 서비스 프로바이더 외에도 등록하고 싶은 [facade](/docs/{{version}}/facades)도 지정할 수 있습니다:

```json
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

패키지가 디스커버리 설정이 되면, Laravel이 패키지를 설치할 때 서비스 프로바이더와 facade를 자동으로 등록하므로 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
### 패키지 디스커버리 비활성화

패키지 사용자로서 특정 패키지의 디스커버리를 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 패키지 이름을 나열할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

`dont-discover` 지시어에서 `*` 문자를 사용하면 모든 패키지에 대해 패키지 디스커버리를 비활성화할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
## 서비스 프로바이더

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel을 연결하는 접점입니다. 서비스 프로바이더는 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩을 하거나, 뷰, 설정, 로컬라이제이션 파일 등의 패키지 리소스가 어디에 있는지 Laravel에 알리는 역할을 담당합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으며, 패키지 의존성에 포함시켜야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [관련 문서](/docs/{{version}}/providers)를 참조하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시할 필요가 있습니다. 이를 통해 사용자들은 패키지의 기본 설정값을 쉽게 오버라이드할 수 있습니다. 설정 파일 퍼블리시를 허용하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../config/courier.php' => config_path('courier.php'),
        ]);
    }

이제 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면 파일이 지정된 위치로 복사됩니다. 설정 파일이 퍼블리시되면 다른 설정 파일과 동일하게 값을 불러올 수 있습니다:

    $value = config('courier.option');

> **경고**  
> 설정 파일에 클로저(익명 함수)를 정의하지 마세요. 사용자가 `config:cache` Artisan 명령어를 실행할 때 직렬화가 제대로 되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

패키지의 설정 파일을 애플리케이션에 퍼블리시한 복사본과 병합할 수도 있습니다. 사용자가 오버라이드하고자 하는 값만 정의할 수 있게 해줍니다. 설정값을 병합하려면, 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드는 첫 번째 인자로 패키지 설정 파일 경로, 두 번째 인자로 애플리케이션의 설정 파일 이름을 받습니다:

    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        $this->mergeConfigFrom(
            __DIR__.'/../config/courier.php', 'courier'
        );
    }

> **경고**  
> 이 메서드는 설정 배열의 1단계 요소만 병합합니다. 다차원 배열의 옵션을 일부만 정의한 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함되어 있다면 `loadRoutesFrom` 메서드를 사용하여 불러올 수 있습니다. 이 메서드는 애플리케이션의 라우트 캐시 여부를 자동으로 판단하며, 캐시된 경우 라우트 파일을 불러오지 않습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
    }

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `loadMigrationsFrom` 메서드를 사용해 Laravel이 마이그레이션을 어떻게 불러와야 하는지 알릴 수 있습니다. 이 메서드는 패키지의 마이그레이션 경로를 유일한 인자로 받습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
    }

패키지의 마이그레이션이 등록되면, `php artisan migrate` 명령어를 실행할 때 자동으로 적용됩니다. 애플리케이션 `database/migrations` 디렉터리로 따로 내보낼 필요가 없습니다.

<a name="translations"></a>
### 번역

패키지에 [번역 파일](/docs/{{version}}/localization)이 포함되어 있다면 `loadTranslationsFrom` 메서드를 사용해서 Laravel에 어떻게 불러올지 알릴 수 있습니다. 예를 들어 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 아래와 같이 추가합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
    }

패키지 번역은 `package::file.line` 규칙으로 참조할 수 있습니다. 예를 들어, `courier` 패키지의 `messages` 파일에 있는 `welcome` 라인을 다음처럼 불러올 수 있습니다:

    echo trans('courier::messages.welcome');

<a name="publishing-translations"></a>
#### 번역 퍼블리싱

패키지의 번역 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. 예를 들어 `courier` 패키지의 번역 파일을 퍼블리시하려면:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

        $this->publishes([
            __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
        ]);
    }

이제 사용자가 Laravel의 `vendor:publish` Artisan 명령어를 실행하면 번역 파일이 퍼블리시됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면 뷰가 어디에 있는지 알려줘야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하세요. 이 메서드는 뷰 템플릿 경로와 패키지 이름 두 가지 인수를 받습니다. 예를 들어 `courier` 패키지라면, 아래와 같이 작성할 수 있습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
    }

패키지 뷰는 `package::view` 형식으로 참조할 수 있습니다. 이제 뷰 경로가 등록되었으니, 아래와 같이 `courier` 패키지의 `dashboard` 뷰를 불러올 수 있습니다:

    Route::get('/dashboard', function () {
        return view('courier::dashboard');
    });

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용하면 Laravel은 실제로 뷰를 위해 두 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 지정한 디렉터리입니다. 즉, `courier` 패키지를 예로 들면, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 디렉터리에 커스텀 뷰를 만들었는지 확인한 후 없으면 패키지의 뷰 디렉터리에서 뷰를 찾습니다. 이렇게 하면 패키지 사용자가 패키지의 뷰를 쉽게 커스터마이즈 또는 오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시할 수 있게 하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 아래와 같이 배열로 뷰 경로와 퍼블리시 위치를 지정합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
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

이제 사용자가 `vendor:publish` Artisan 명령어를 실행하면 패키지의 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하거나 비표준 디렉터리에 컴포넌트를 배치하는 패키지를 만들고 있다면, Laravel이 컴포넌트를 찾을 수 있도록 클래스와 태그 별칭을 등록해야 합니다. 일반적으로 이 작업은 패키지 서비스 프로바이더의 `boot` 메서드에서 하면 됩니다:

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        Blade::component('package-alert', AlertComponent::class);
    }

컴포넌트가 등록되면, 다음과 같이 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 오토로딩

또는, `componentNamespace` 메서드를 사용하여 네임스페이스 기준으로 컴포넌트 클래스를 오토로딩할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스 아래에 `Calendar`와 `ColorPicker` 컴포넌트가 있다고 가정하면:

    use Illuminate\Support\Facades\Blade;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

이제 `package-name::` 구문으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환하여 해당 클래스를 자동으로 찾습니다. "dot" 점 표기법을 사용하여 하위 디렉터리도 지원합니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지에 익명 컴포넌트가 포함되어 있다면, 반드시 패키지의 "views" 디렉터리 아래 `components` 디렉터리 안에 두어야 합니다 (이는 [`loadViewsFrom` 메서드](#views)로 지정된 경로입니다). 그러면 패키지의 뷰 네임스페이스와 함께 컴포넌트 이름을 사용할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" Artisan 명령어

Laravel의 내장 `about` Artisan 명령어는 애플리케이션 환경 및 설정 요약을 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 이 명령어의 출력에 정보를 추가할 수 있습니다. 일반적으로 이 정보는 패키지 서비스 프로바이더의 `boot` 메서드에서 추가합니다:

    use Illuminate\Foundation\Console\AboutCommand;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
    }

<a name="commands"></a>
## 커맨드

패키지의 Artisan 커맨드를 Laravel에 등록하려면 `commands` 메서드를 사용할 수 있습니다. 이 메서드는 커맨드 클래스명 배열을 인자로 받습니다. 커맨드가 등록되면 [Artisan CLI](/docs/{{version}}/artisan)로 실행할 수 있습니다:

    use Courier\Console\Commands\InstallCommand;
    use Courier\Console\Commands\NetworkCommand;

    /**
     * 패키지 서비스를 부트스트랩합니다.
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

<a name="public-assets"></a>
## 퍼블릭 에셋

패키지에 JavaScript, CSS, 이미지 등의 에셋이 포함되어 있다면, 서비스 프로바이더의 `publishes` 메서드를 사용하여 애플리케이션의 `public` 디렉터리로 퍼블리시할 수 있습니다. 아래 예시에서는 관련 에셋 그룹 태그(`public`)도 추가하여, 연관 자산을 쉽게 그룹으로 퍼블리시할 수 있습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../public' => public_path('vendor/courier'),
        ], 'public');
    }

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 자산이 지정된 위치로 복사됩니다. 보통 패키지 업데이트 때마다 에셋을 덮어써야 하므로, `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

패키지의 에셋과 리소스를 그룹별로 따로 퍼블리시할 수 있습니다. 예를 들어, 사용자가 설정 파일만 따로 퍼블리시하도록 하거나 에셋 퍼블리시를 강제하지 않게 만들 수 있습니다. 서비스 프로바이더의 `publishes` 메서드 호출 시 "태그" 기능을 사용하면 됩니다. 아래 예시는 `courier` 패키지에서 `courier-config`와 `courier-migrations`라는 두 퍼블리시 그룹 태그를 정의하는 방법입니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
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

이제 사용자는 `vendor:publish` 명령어 실행 시 해당 태그를 참조하여 그룹별로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```
