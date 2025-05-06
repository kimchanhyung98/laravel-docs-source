```markdown
# 패키지 개발

- [소개](#introduction)
    - [파사드에 대한 참고](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" 아티즌 명령어](#about-artisan-command)
- [명령어](#commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 주된 방법입니다. 예를 들어 [Carbon](https://github.com/briannesbitt/Carbon)과 같이 날짜를 다루기 위한 훌륭한 방법을 제공하는 패키지부터, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델과 파일을 연관짓는 패키지까지 종류는 매우 다양합니다.

패키지는 여러 종류가 있습니다. 일부 패키지는 스탠드얼론 패키지로, 어떠한 PHP 프레임워크에서도 동작합니다. Carbon과 PHPUnit가 그 예입니다. 이런 패키지는 `composer.json` 파일에 require하여 Laravel에서 바로 사용할 수 있습니다.

반면, Laravel 전용으로 개발된 패키지들도 있습니다. 이러한 패키지는 Laravel 애플리케이션을 향상시키기 위한 라우트, 컨트롤러, 뷰, 환경설정 등 전용 기능을 제공할 수 있습니다. 이 가이드에서는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고

Laravel 애플리케이션을 개발할 때에는 contract 혹은 facade를 사용하는 것 모두 테스트 가능성 측면에서 크게 차이가 없습니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼를 사용할 수 없을 수 있습니다. 패키지 테스트를 일반 Laravel 애플리케이션에 설치한 것처럼 작성하려면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리

Laravel 애플리케이션의 `config/app.php` 설정 파일의 `providers` 옵션은 Laravel이 로드해야 할 서비스 프로바이더들의 목록을 정의합니다. 사용자가 패키지를 설치하면, 보통 패키지의 서비스 프로바이더가 이 목록에 포함되기를 원할 것입니다. 사용자가 서비스 프로바이더를 수동으로 추가할 필요 없이, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 서비스 프로바이더와 함께, 등록하고자 하는 [파사드](/docs/{{version}}/facades)들도 지정할 수 있습니다:

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

패키지가 디스커버리 설정을 마치면, Laravel은 설치 시에 자동으로 해당 서비스 프로바이더와 파사드를 등록해, 사용자에게 더 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 디스커버리 사용 안 함

특정 패키지의 디스커버리를 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 패키지명을 추가하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

`dont-discover` 지시어에 `*` 문자를 사용해 모든 패키지의 디스커버리를 비활성화할 수도 있습니다:

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

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel을 연결하는 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩을 추가하거나, 뷰, 설정, 언어 파일 등 패키지 리소스의 위치를 Laravel에 알리는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` 컴포저 패키지에 포함되어 있으므로, 패키지의 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 관한 자세한 설명은 [공식 문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정

일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시할 필요가 있습니다. 이를 통해 패키지 사용자는 기본 설정 값을 손쉽게 오버라이드할 수 있습니다. 설정 파일을 퍼블리시 가능하도록 하려면 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/courier.php' => config_path('courier.php'),
        ]);
    }

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 파일이 명시된 경로로 복사됩니다. 설정을 퍼블리시한 뒤에는 일반 설정 파일과 동일하게 값을 읽을 수 있습니다:

    $value = config('courier.option');

> [!WARNING]  
> 설정 파일에 클로저(Closure)를 정의해서는 안 됩니다. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 패키지 기본 설정

패키지의 설정 파일을 애플리케이션에 병합할 수도 있습니다. 이렇게 하면 사용자가 오버라이드하고 싶은 설정만 퍼블리시된 파일에 정의할 수 있습니다. 설정 파일을 병합하려면 서비스 프로바이더의 `register` 메서드 내에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드는 첫 번째 인자로 패키지의 설정 파일 경로를, 두 번째 인자로 애플리케이션 설정 파일명을 받습니다:

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
> 이 메서드는 설정 배열의 1차원만 병합합니다. 다차원 배열을 일부만 오버라이드한 경우 병합되지 않을 수 있습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 이용해 로드할 수 있습니다. 이 메서드는 애플리케이션 라우트가 캐시되어 있다면 파일을 다시 로드하지 않습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
    }

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `loadMigrationsFrom` 메서드를 이용하여 Laravel에 로드 경로를 알릴 수 있습니다. 이 메서드는 패키지 마이그레이션 폴더의 경로를 인자로 받습니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
    }

패키지의 마이그레이션이 등록되면, `php artisan migrate` 명령어 실행 시 자동으로 적용됩니다. 애플리케이션의 `database/migrations` 디렉터리로 따로 복사할 필요가 없습니다.

<a name="language-files"></a>
### 언어 파일

패키지에 [언어 파일](/docs/{{version}}/localization)이 있다면, `loadTranslationsFrom` 메서드를 사용해서 Laravel이 해당 파일을 로드하도록 할 수 있습니다. 예를 들어, 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 다음을 추가하세요:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
    }

패키지의 번역 라인은 `package::file.line` 문법으로 사용합니다. 예를 들어 `courier` 패키지의 `messages` 파일에 있는 `welcome` 번역 라인을 불러올 때:

    echo trans('courier::messages.welcome');

패키지의 JSON 번역 파일을 등록하려면 `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 JSON 파일이 들어있는 폴더 경로를 받습니다:

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
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. 예를 들어 `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 합니다:

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

이후 사용자가 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정한 경로로 복사됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면, 뷰 파일의 위치를 Laravel에 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하며, 첫 번째 인자로 뷰 템플릿 경로, 두 번째 인자로 패키지 이름을 받습니다. 예를 들어, 패키지 이름이 `courier`라면 다음과 같이 등록합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
    }

패키지 뷰는 `package::view` 문법으로 참조할 수 있습니다. 예를 들어 `courier` 패키지의 `dashboard` 뷰를 로드하려면:

    Route::get('/dashboard', function () {
        return view('courier::dashboard');
    });

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용하면, Laravel은 두 곳에서 뷰를 찾습니다: 애플리케이션의 `resources/views/vendor` 디렉터리와, 지정한 패키지 뷰 디렉터리입니다. 즉, 먼저 개발자가 `resources/views/vendor/courier`에 뷰를 커스텀했다면 그 파일을 사용하고, 그렇지 않다면 지정한 패키지 디렉터리를 참조합니다. 이를 통해 패키지 사용자가 뷰를 손쉽게 수정/오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시할 수 있게 하려면 `publishes` 메서드를 이용합니다. 이 메서드는 패키지 뷰 경로와 퍼블리시 위치 배열을 받습니다:

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

패키지 사용자가 `vendor:publish` 명령어를 실행하면, 뷰 파일이 지정 경로로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하는 패키지를 만들거나, 일반적이지 않은 경로에 컴포넌트를 위치시키는 경우, 컴포넌트 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다:

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::component('package-alert', AlertComponent::class);
    }

컴포넌트를 등록하면, 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로드

또는, `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 컨벤션 대로 자동으로 로드할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스 하위에 `Calendar`, `ColorPicker` 컴포넌트가 있을 수 있습니다:

    use Illuminate\Support\Facades\Blade;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

이제 `package-name::` 문법으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환하여 연결되는 클래스를 자동으로 감지합니다. 서브디렉터리도 "dot" 표기법으로 지원합니다.

<a name="anonymous-components"></a>
#### 익명(Anonymous) 컴포넌트

패키지에 익명 컴포넌트가 있다면, 반드시 패키지 "views" 디렉터리 내 `components` 폴더 안에 배치해야 합니다([`loadViewsFrom` 메서드](#views)로 지정된 뷰 경로 기준). 그 후에는 패키지 뷰 네임스페이스를 접두어로 붙여서 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어

Laravel의 내장 `about` 아티즌 명령어는 애플리케이션의 환경 및 설정 요약 정보를 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 해당 명령어의 출력에 정보 항목을 추가할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 정보를 추가합니다:

    use Illuminate\Foundation\Console\AboutCommand;

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
    }

<a name="commands"></a>
## 명령어

패키지의 아티즌 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용합니다. 이 메서드는 명령어 클래스명 배열을 인자로 받습니다. 등록이 완료되면, [아티즌 CLI](/docs/{{version}}/artisan)를 통해 실행할 수 있습니다:

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

<a name="public-assets"></a>
## 퍼블릭 에셋

패키지에 JavaScript, CSS, 이미지 등 에셋이 포함될 수 있습니다. 이러한 에셋을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 아래 예시는 `public` 에셋 그룹 태그도 추가해 관련된 에셋을 손쉽게 퍼블리시할 수 있도록 합니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../public' => public_path('vendor/courier'),
        ], 'public');
    }

사용자가 `vendor:publish` 명령어를 실행하면, 에셋이 지정 위치로 복사됩니다. 패키지가 업데이트될 때마다 에셋을 덮어써야 할 경우가 많기 때문에, `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

에셋이나 리소스 파일을 그룹별로 나누어 별도 퍼블리싱이 필요할 수 있습니다. 예를 들어, 설정 파일만 퍼블리시하고 싶고 에셋은 별도로 퍼블리시 하길 원할 수 있습니다. 이럴 땐 `publishes` 메서드 호출 시 "태그"를 사용해 그룹을 구분할 수 있습니다. 아래는 `courier` 패키지의 `courier-config`, `courier-migrations`라는 두 퍼블리시 그룹을 만드는 예시입니다:

    /**
     * 패키지 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/package.php' => config_path('package.php')
        ], 'courier-config');

        $this->publishes([
            __DIR__.'/../database/migrations/' => database_path('migrations')
        ], 'courier-migrations');
    }

이제 사용자는 `vendor:publish` 명령어 실행 시 태그를 참조하여 특정 그룹만 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```
```