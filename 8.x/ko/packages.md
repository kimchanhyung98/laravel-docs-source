# 패키지 개발

- [소개](#introduction)
    - [파사드에 대한 참고](#a-note-on-facades)
- [패키지 자동 발견](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [번역](#translations)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
- [명령어](#commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 기본적인 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜를 다루는 훌륭한 도구가 될 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연동하게 해주는 패키지일 수도 있습니다.

패키지에는 여러 유형이 있습니다. 어떤 패키지는 독립형(stand-alone)으로 제작되어, 어떤 PHP 프레임워크에서도 동작합니다. Carbon과 PHPUnit가 독립형 패키지의 예입니다. 이들과 같은 패키지는 `composer.json` 파일에 추가함으로써 Laravel에서 사용할 수 있습니다.

반면, Laravel 전용으로 개발된 패키지도 있습니다. 이 패키지들은 Laravel 애플리케이션에 특화된 라우트, 컨트롤러, 뷰, 설정 등이 포함될 수 있습니다. 이 가이드에서는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고

Laravel 애플리케이션을 작성할 때는 계약(Contracts)이나 파사드(Facades) 중 무엇을 사용해도 테스트 용이성에는 큰 차이가 없습니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼를 사용할 수 없기 때문에 상황이 다릅니다. 패키지 테스트를 일반적인 Laravel 애플리케이션 내부에 설치된 것처럼 작성하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 발견(Discovery)

Laravel 애플리케이션의 `config/app.php` 설정 파일에서 `providers` 옵션은 로드해야 할 서비스 프로바이더 목록을 정의합니다. 다른 사람이 당신의 패키지를 설치할 때, 보통 당신의 서비스 프로바이더가 이 리스트에 포함되길 원할 것입니다. 사용자가 직접 서비스 프로바이더를 추가하지 않고도 자동으로 등록되게 하려면, 패키지의 `composer.json` 파일 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 서비스 프로바이더 외에도, 등록하고자 하는 [파사드](/docs/{{version}}/facades)도 지정할 수 있습니다.

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

패키지가 자동 발견(Discovery) 설정이 완료되면, Laravel은 패키지가 설치될 때 자동으로 서비스 프로바이더와 파사드를 등록하므로, 사용자에게 매우 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
### 패키지 자동 발견(Discovery) 비활성화

패키지 사용자가 특정 패키지의 자동 발견을 비활성화하려면, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 패키지 이름을 명시할 수 있습니다:

    "extra": {
        "laravel": {
            "dont-discover": [
                "barryvdh/laravel-debugbar"
            ]
        }
    },

애플리케이션의 `dont-discover` 항목에 `*` 문자를 사용하면, 모든 패키지의 자동 발견을 비활성화할 수 있습니다.

    "extra": {
        "laravel": {
            "dont-discover": [
                "*"
            ]
        }
    },

<a name="service-providers"></a>
## 서비스 프로바이더

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel을 연결하는 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 여러 리소스(뷰, 설정, 로케일 파일 등)를 바인딩하거나 로드 위치를 알려주는 역할을 담당합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 가지 메서드를 포함하고 있습니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으므로, 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적을 더 자세히 알고 싶다면 [공식 문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정(Configuration)

일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 퍼블리시해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정을 쉽게 재정의할 수 있습니다. 설정 파일을 퍼블리시하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../config/courier.php' => config_path('courier.php'),
        ]);
    }

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정한 위치로 복사됩니다. 퍼블리시된 설정 값은 기존 설정과 동일하게 접근할 수 있습니다.

    $value = config('courier.option');

> {note} 설정 파일 내에 클로저를 정의하지 않아야 합니다. 사용자가 `config:cache` Artisan 명령어를 실행할 때 직렬화가 제대로 되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

패키지의 기본 설정 파일을 애플리케이션에 퍼블리시된 복사본과 병합할 수도 있습니다. 이를 통해 사용자는 설정 파일의 수정하고 싶은 옵션만 재정의하면 되고, 나머지는 그대로 사용할 수 있습니다. 설정 값을 병합하려면 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom`은 첫 번째 인수로 패키지의 설정 파일 경로를, 두 번째 인수로 애플리케이션 설정 파일명을 받습니다:

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->mergeConfigFrom(
            __DIR__.'/../config/courier.php', 'courier'
        );
    }

> {note} 이 메소드는 설정 배열의 1단계(depth)만 병합합니다. 사용자가 다차원 설정 배열을 일부만 정의하면, 누락된 항목은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함된다면, `loadRoutesFrom` 메서드를 사용해 라우트를 로드할 수 있습니다. 이 메서드는 애플리케이션의 라우트가 이미 캐시되어 있는지 자동으로 확인하며, 이미 캐시된 경우에는 패키지 라우트 파일을 다시 로드하지 않습니다.

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
    }

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `loadMigrationsFrom` 메서드로 마이그레이션 파일 경로를 지정할 수 있습니다:

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
    }

패키지의 마이그레이션이 등록되면, `php artisan migrate` 명령어를 실행할 때 자동으로 실행됩니다. 애플리케이션의 `database/migrations` 폴더로 복사할 필요가 없습니다.

<a name="translations"></a>
### 번역

패키지에 [번역 파일](/docs/{{version}}/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드를 이용해 Laravel이 번역 파일을 어디서 불러올지 알려줄 수 있습니다. 예를 들어, 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 아래와 같이 추가합니다.

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');
    }

패키지 번역은 `package::file.line` 형태로 참조합니다. 즉, `courier` 패키지의 `messages` 파일에 있는 `welcome` 라인을 다음과 같이 불러올 수 있습니다:

    echo trans('courier::messages.welcome');

<a name="publishing-translations"></a>
#### 번역 퍼블리싱

패키지 번역 파일을 애플리케이션의 `resources/lang/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요.

    /**
     * Bootstrap any package services.
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

이제 사용자가 `vendor:publish` Artisan 명령어를 실행하면, 번역 파일이 지정한 위치로 퍼블리시됩니다.

<a name="views"></a>
### 뷰(Views)

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면 뷰 파일이 어디에 있는지 알려줘야 합니다. 이는 서비스 프로바이더의 `loadViewsFrom` 메서드를 통해 지정할 수 있습니다. 첫 번째 인수는 뷰 템플릿의 경로, 두 번째 인수는 패키지의 이름입니다. 예를 들어 패키지 이름이 `courier`라면 다음과 같이 등록합니다:

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
    }

패키지 뷰는 `package::view` 형식으로 참조할 수 있습니다. 서비스 프로바이더에 뷰 경로가 등록된 후에는 다음과 같이 뷰를 로드할 수 있습니다:

    Route::get('/dashboard', function () {
        return view('courier::dashboard');
    });

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이딩

`loadViewsFrom`을 사용하면 Laravel은 실제로 두 위치에서 뷰를 조회합니다: 애플리케이션의 `resources/views/vendor` 디렉터리, 그리고 지정한 패키지 디렉터리입니다. 예를 들어 `courier` 패키지의 경우, 먼저 개발자가 `resources/views/vendor/courier`에 뷰를 직접 두었는지를 확인하고, 없다면 패키지 디렉터리를 조회합니다. 이를 통해 패키지 사용자는 쉽고 자유롭게 뷰를 커스터마이즈 할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰를 `resources/views/vendor` 디렉터리로 퍼블리시하고자 한다면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요:

    /**
     * Bootstrap the package services.
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

이제 사용자가 `vendor:publish` Artisan 명령어를 실행하면, 패키지의 뷰가 지정된 위치로 퍼블리시됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

패키지에 [뷰 컴포넌트](/docs/{{version}}/blade#components)가 포함되어 있다면, `loadViewComponentsAs` 메서드를 통해 컴포넌트의 태그 프리픽스와 클래스 이름 배열을 등록할 수 있습니다. 예를 들어 프리픽스가 `courier`, 컴포넌트가 `Alert`와 `Button`이면 서비스 프로바이더 `boot` 메서드에 다음과 같이 작성합니다:

    use Courier\Components\Alert;
    use Courier\Components\Button;

    /**
     * Bootstrap any package services.
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

뷰 컴포넌트가 등록되면, 뷰에서 다음과 같이 컴포넌트를 사용할 수 있습니다:

    <x-courier-alert />

    <x-courier-button />

<a name="anonymous-components"></a>
#### 익명(Anonymous) 컴포넌트

익명 컴포넌트는 반드시 패키지의 "views" 디렉터리 내에 `components` 폴더에 위치해야 합니다(`loadViewsFrom`에 지정한 경로 기준). 그리고 컴포넌트 이름 앞에 패키지 네임스페이스를 붙여 렌더링할 수 있습니다:

    <x-courier::alert />

<a name="commands"></a>
## 명령어(Commands)

패키지에서 Artisan 명령어를 등록하려면, `commands` 메서드를 사용하세요. 이 메서드는 커맨드 클래스 이름의 배열을 받습니다. 명령어가 등록되면, [Artisan CLI](/docs/{{version}}/artisan)로 실행할 수 있습니다:

    use Courier\Console\Commands\InstallCommand;
    use Courier\Console\Commands\NetworkCommand;

    /**
     * Bootstrap any package services.
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

패키지에 JavaScript, CSS, 이미지 등 에셋이 포함된 경우, 서비스 프로바이더의 `publishes` 메서드를 사용하여 애플리케이션의 `public` 디렉터리로 퍼블리시할 수 있습니다. 아래 예시에서는 `public` 에셋 그룹 태그를 추가해, 연관된 에셋 그룹을 쉽게 퍼블리시할 수 있습니다:

    /**
     * Bootstrap any package services.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../public' => public_path('vendor/courier'),
        ], 'public');
    }

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 에셋이 지정 위치로 복사됩니다. 패키지 업데이트 시 에셋을 매번 덮어써야 할 필요가 있다면, `--force` 플래그를 사용할 수 있습니다:

    php artisan vendor:publish --tag=public --force

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

여러 리소스와 에셋을 별도로 퍼블리시하고자 할 수 있습니다. 예를 들어, 사용자에게 패키지 설정 파일만 퍼블리시하고 에셋은 별도로 퍼블리시할 수 있게 하려면, 퍼블리시 시 태그(tag)를 지정할 수 있습니다. 예를 들어, `courier` 패키지를 위한 두 개의 퍼블리시 그룹(`courier-config`, `courier-migrations`)을 다음과 같이 서비스 프로바이더의 `boot` 메서드에서 정의할 수 있습니다:

    /**
     * Bootstrap any package services.
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

이제 사용자는 태그를 지정하여 해당 그룹만 퍼블리시할 수 있습니다:

    php artisan vendor:publish --tag=courier-config