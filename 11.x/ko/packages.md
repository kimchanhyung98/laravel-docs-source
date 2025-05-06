# 패키지 개발

- [소개](#introduction)
    - [파사드에 대한 참고](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정 파일](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" 아티즌 명령어](#about-artisan-command)
- [명령어](#commands)
    - [최적화 명령어](#optimize-commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 주된 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)과 같이 날짜를 쉽게 다루게 해주는 라이브러리부터, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 파일을 Eloquent 모델에 연동하게 해주는 패키지까지 여러 형태가 있습니다.

패키지에는 여러 유형이 있습니다. 어떤 패키지는 독립형으로, 어떤 PHP 프레임워크와도 함께 작동합니다. Carbon과 Pest가 이러한 예시입니다. 이러한 패키지들은 `composer.json`에 추가하여 Laravel에서 사용할 수 있습니다.

반면, Laravel에만 특화된 패키지도 있습니다. 이러한 패키지는 라우트, 컨트롤러, 뷰, 설정 등 Laravel 애플리케이션을 보완하기 위해 특별히 만들어집니다. 이 문서에서는 주로 Laravel에 특화된 패키지 개발을 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고

Laravel 애플리케이션을 작성할 때, contract(계약)나 facade(파사드) 중 무엇을 사용하는지는 큰 차이가 없습니다. 두 방식 모두 비슷한 수준의 테스트 가능성을 제공합니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼를 사용할 수 없을 수도 있습니다. 패키지의 테스트를 일반적인 Laravel 애플리케이션에서 실행하는 것처럼 작성하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 로딩해야 할 서비스 프로바이더 목록이 정의되어 있습니다. 하지만, 사용자가 서비스 프로바이더를 직접 추가하지 않고도, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의해 자동으로 로딩되게 할 수 있습니다. 서비스 프로바이더뿐만 아니라 등록하고 싶은 [파사드](/docs/{{version}}/facades)도 명시할 수 있습니다:

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

패키지가 디스커버리 설정이 되면, 사용자들은 패키지를 설치하기만 하면 Laravel이 자동으로 서비스 프로바이더와 파사드를 등록해 편리하게 사용할 수 있습니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 디스커버리 비활성화

패키지 사용자 입장에서 디스커버리를 비활성화하고 싶을 경우, 애플리케이션의 `composer.json`의 `extra` 섹션에 패키지 이름을 추가하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

모든 패키지의 디스커버리를 비활성화하려면 `dont-discover` 지시문에 `*`를 사용할 수 있습니다:

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

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel 간의 연결 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩을 등록하고, 뷰, 설정, 언어 파일 등 패키지 리소스의 로딩 위치를 Laravel에 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으니, 패키지의 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [공식 문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정 파일

일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시해야 합니다. 이를 통해 패키지 사용자가 설정을 쉽게 오버라이드 할 수 있습니다. 설정 파일 퍼블리싱을 허용하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/courier.php' => config_path('courier.php'),
        ]);
    }

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정한 위치로 복사됩니다. 설정이 퍼블리시된 후에는 일반적인 설정 파일처럼 값을 접근할 수 있습니다:

    $value = config('courier.option');

> [!WARNING]  
> 설정 파일에 클로저를 정의해서는 안 됩니다. 사용자가 `config:cache` Artisan 명령어를 실행할 때 클로저는 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 병합

패키지의 기본 설정 파일을 애플리케이션의 퍼블리시된 설정과 병합할 수도 있습니다. 이를 통해 사용자는 오버라이드하고자 하는 옵션만 정의하면 됩니다. 파일 값을 병합하려면 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom`의 첫 번째 인수는 패키지의 설정 파일 경로, 두 번째 인수는 애플리케이션 설정 파일의 이름입니다:

    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        $this->mergeConfigFrom(
            __DIR__.'/../config/courier.php', 'courier'
        );
    }

> [!WARNING]  
> 이 메서드는 1차원 설정 배열만 병합합니다. 사용자가 다차원 설정 배열을 일부만 정의할 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 있다면, `loadRoutesFrom` 메서드로 로드할 수 있습니다. 이 메서드는 앱의 라우트가 이미 캐시되었다면 중복 불러오지 않습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
    }

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용해 해당 디렉터리나 파일이 마이그레이션임을 알려줄 수 있습니다. 퍼블리시할 때 파일명에 현재 날짜와 시간이 추가되어 복사됩니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishesMigrations([
            __DIR__.'/../database/migrations' => database_path('migrations'),
        ]);
    }

<a name="language-files"></a>
### 언어 파일

패키지에 [언어 파일](/docs/{{version}}/localization)이 있다면, `loadTranslationsFrom`으로 Laravel에서 로딩할 경로를 지정할 수 있습니다. 예를 들어, 패키지명이 `courier`라면, 다음과 같이 서비스 프로바이더의 `boot` 메서드에 추가합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
    }

패키지 언어라인 참조는 `package::file.line` 규칙을 따릅니다. 예를 들어, `messages` 파일의 `welcome` 라인은 다음과 같이 로드할 수 있습니다:

    echo trans('courier::messages.welcome');

JSON 번역 파일을 등록하려면, `loadJsonTranslationsFrom` 메서드를 사용하세요. 이 메서드는 JSON 파일이 위치한 디렉터리 경로를 받습니다:

```php
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리시

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리에 퍼블리시하려면, `publishes` 메서드를 사용하면 됩니다. 예를 들어, `courier` 패키지의 언어 파일 퍼블리시는 다음과 같이 할 수 있습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

        $this->publishes([
            __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
        ]);
    }

이제 사용자가 Laravel의 `vendor:publish` Artisan 명령어를 실행하면 언어 파일이 퍼블리시 위치에 복사됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/{{version}}/views)를 등록하려면, 뷰의 위치를 Laravel에 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 통해 할 수 있습니다. 첫 번째 인수는 뷰 템플릿 경로, 두 번째 인수는 패키지명입니다. 예를 들어 `courier`라면 다음과 같이 등록합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
    }

패키지 뷰 참조는 `package::view` 규칙을 따릅니다. `courier` 패키지의 `dashboard` 뷰를 다음과 같이 불러올 수 있습니다:

    Route::get('/dashboard', function () {
        return view('courier::dashboard');
    });

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom`을 사용하면, Laravel은 기본적으로 두 위치를 확인합니다. 하나는 애플리케이션의 `resources/views/vendor` 디렉터리, 다른 하나는 직접 지정한 패키지의 뷰 디렉터리입니다. 예를 들어, 개발자가 `resources/views/vendor/courier`에 커스텀 뷰를 두었다면, 이 뷰가 우선 적용됩니다. 뷰 커스터마이즈/오버라이드가 매우 쉬워집니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리시

패키지의 뷰를 애플리케이션의 `resources/views/vendor` 디렉터리에 복사하려면, `publishes` 메서드를 사용하세요:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

        $this->publishes([
            __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
        ]);
    }

이제 사용자가 `vendor:publish` Artisan 명령어를 실행하면 패키지의 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하는 패키지이거나, 통상적이지 않은 디렉터리에 컴포넌트를 배치한 경우, 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다:

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::component('package-alert', AlertComponent::class);
    }

컴포넌트가 등록되면, 태그 별칭으로 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는 `componentNamespace` 메서드를 이용해 네임스페이스 기반 규칙에 따라 컴포넌트 클래스를 자동 로딩할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스의 `Calendar`, `ColorPicker` 컴포넌트가 있다면:

    use Illuminate\Support\Facades\Blade;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

이제 다음과 같이 벤더 네임스페이스(`package-name::`)로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 대응되는 클래스를 자동으로 찾습니다. "dot" 표기법으로 하위 디렉터리 사용도 지원됩니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지에 익명 컴포넌트가 포함되어 있다면, 해당 컴포넌트는 `views` 디렉터리 하위의 `components` 폴더에 위치해야 합니다([`loadViewsFrom` 메서드](#views) 참고). 그런 다음, 네임스페이스 프리픽스와 함께 컴포넌트 이름을 사용해 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어

Laravel의 기본 `about` Artisan 명령은 앱 환경과 설정의 개요를 보여줍니다. 패키지는 `AboutCommand` 클래스를 통해 이 명령어의 출력에 추가 정보를 삽입할 수 있습니다. 일반적으로, 서비스 프로바이더의 `boot` 메서드에서 정보를 추가합니다:

    use Illuminate\Foundation\Console\AboutCommand;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
    }

<a name="commands"></a>
## 명령어

패키지의 아티즌(Artisan) 명령어를 등록하려면, `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령 클래스 이름 배열을 받습니다. 명령어가 등록된 후에는 [Artisan CLI](/docs/{{version}}/artisan)로 실행할 수 있습니다:

    use Courier\Console\Commands\InstallCommand;
    use Courier\Console\Commands\NetworkCommand;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->commands([
                InstallCommand::class,
                NetworkCommand::class,
            ]);
        }
    }

<a name="optimize-commands"></a>
### 최적화 명령어

Laravel의 [`optimize` 명령어](/docs/{{version}}/deployment#optimization)는 앱의 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 사용해 패키지의 관련 Artisan 명령어를 등록할 수 있고, 이 명령어는 `optimize` 또는 `optimize:clear` 실행 시 호출됩니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->optimizes(
                optimize: 'package:optimize',
                clear: 'package:clear-optimizations',
            );
        }
    }

<a name="public-assets"></a>
## 퍼블릭 에셋

패키지에서 JavaScript, CSS, 이미지 등의 에셋이 있다면, 서비스 프로바이더의 `publishes` 메서드를 사용해 앱의 `public` 디렉터리로 퍼블리시할 수 있습니다. 아래 예시에서는 `public` 에셋 그룹 태그도 함께 추가합니다. 이 태그로 관련 에셋 그룹을 쉽게 퍼블리시할 수 있습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../public' => public_path('vendor/courier'),
        ], 'public');
    }

패키지 사용자가 `vendor:publish` 명령을 실행하면 에셋이 지정 위치로 복사됩니다. 패키지 업데이트마다 에셋을 덮어써야 하므로, `--force` 플래그를 함께 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

패키지의 에셋이나 리소스를 그룹별로 퍼블리싱하고 싶을 때가 있습니다. 예를 들어 설정 파일만, 또는 마이그레이션만 따로 퍼블리시하고자 할 수 있습니다. 이를 위해 `publishes` 메서드를 호출할 때 "태그"를 지정할 수 있습니다. 아래는 `courier` 패키지의 설정 파일(`courier-config`)과 마이그레이션(`courier-migrations`)에 대해 두 개의 퍼블리시 그룹을 만든 예시입니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/package.php' => config_path('package.php')
        ], 'courier-config');

        $this->publishesMigrations([
            __DIR__.'/../database/migrations/' => database_path('migrations')
        ], 'courier-migrations');
    }

이제 사용자는 태그를 지정해서 각 그룹을 별도로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```
