# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 관한 주의 사항](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - [내장 `about` Artisan 명령어](#about-artisan-command)
- [명령어](#commands)
- [퍼블릭 자산](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 수단입니다. 패키지는 예를 들어 [Carbon](https://github.com/briannesbitt/Carbon) 같은 날짜 작업을 위한 훌륭한 라이브러리일 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연관시키는 패키지일 수도 있습니다.

패키지에는 여러 종류가 존재합니다. 일부 패키지는 독립형(stand-alone)으로, 특정 PHP 프레임워크와 무관하게 작동합니다. Carbon과 PHPUnit가 이에 해당합니다. 이들 패키지는 `composer.json` 파일에 요구 사항으로 추가하여 Laravel과 함께 사용할 수 있습니다.

반면에, 다른 패키지는 Laravel 전용으로 설계됩니다. 이들 패키지는 라우트, 컨트롤러, 뷰, 설정 같은 항목들을 포함하여 Laravel 애플리케이션을 확장하는 데 특화되어 있습니다. 이 가이드는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 관한 주의 사항 (A Note on Facades)

Laravel 애플리케이션을 작성할 때는 Contracts(인터페이스)나 Facades 중 어느 것을 사용하든 테스트 가능성 측면에서 본질적으로 동일한 수준을 제공합니다. 하지만 패키지를 작성할 때는 Laravel의 모든 테스트 헬퍼에 접근할 수 없는 경우가 많습니다. 패키지를 일반 Laravel 애플리케이션 내부에 설치된 것처럼 테스트하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리 (Package Discovery)

Laravel 애플리케이션의 `config/app.php` 설정 파일에서 `providers` 옵션은 Laravel에서 로드할 서비스 프로바이더 목록을 정의합니다. 패키지를 설치할 때 보통 해당 패키지의 서비스 프로바이더가 이 목록에 포함되길 원합니다. 사용자가 직접 수동으로 서비스 프로바이더를 목록에 추가하는 대신, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 서비스 프로바이더뿐만 아니라 등록할 [파사드](/docs/10.x/facades)도 명시할 수 있습니다:

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

패키지가 디스커버리용으로 설정되면, 패키지 설치 시 Laravel이 자동으로 서비스 프로바이더와 파사드를 등록해주어 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 디스커버리 비활성화 (Opting Out of Package Discovery)

패키지 사용자로서 특정 패키지에 대해 디스커버리를 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 다음과 같이 패키지 이름을 나열하세요:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

모든 패키지에 대해 패키지 디스커버리를 비활성화하려면, `dont-discover` 지시자에 `*` 문자를 사용하세요:

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
## 서비스 프로바이더 (Service Providers)

[서비스 프로바이더](/docs/10.x/providers)는 패키지와 Laravel을 연결하는 접점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/10.x/container)에 바인딩 작업을 하며, 뷰, 설정, 언어 파일 등 패키지의 리소스를 어디서 로드할지 Laravel에 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, 두 가지 메서드 `register`와 `boot`을 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으며, 이를 귀하 패키지의 의존성으로 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [공식 문서](/docs/10.x/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉토리에 퍼블리싱해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정 값을 쉽게 재정의할 수 있습니다. 설정 파일을 퍼블리싱할 수 있게 하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정된 위치로 복사됩니다. 퍼블리싱된 설정 값은 다른 설정 파일과 동일하게 접근할 수 있습니다:

```
$value = config('courier.option');
```

> [!WARNING]  
> 설정 파일 내에 클로저(익명 함수)를 정의하지 마십시오. `config:cache` Artisan 명령어 사용 시 클로저는 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 (Default Package Configuration)

패키지 설정 파일과 애플리케이션에 퍼블리싱된 설정 파일을 병합할 수도 있습니다. 이렇게 하면 사용자는 퍼블리싱된 설정 중에서 실제로 재정의하려는 옵션만 작성하면 됩니다. 병합하려면 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드는 패키지 설정 파일 경로를 첫 번째 인자로, 애플리케이션 설정 파일 이름을 두 번째 인자로 받습니다:

```
/**
 * 애플리케이션 서비스를 등록합니다.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]  
> 이 메서드는 설정 배열의 최상위 레벨만 병합합니다. 다차원 배열을 부분적으로 정의한 경우, 누락된 옵션들은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함된 경우, `loadRoutesFrom` 메서드를 사용하여 Laravel에 라우트를 로드하라고 알릴 수 있습니다. 이 메서드는 애플리케이션 라우트가 캐시된 경우 라우트 파일을 로드하지 않도록 자동 감지합니다:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/10.x/migrations)이 있다면, `loadMigrationsFrom` 메서드를 사용하여 Laravel에 마이그레이션 로드 방법을 알려주십시오. 이 메서드는 패키지 마이그레이션 경로를 인자로 받습니다:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
}
```

패키지 마이그레이션이 등록되면, `php artisan migrate` 명령어 실행 시 자동으로 실행됩니다. 애플리케이션의 `database/migrations` 디렉토리로 마이그레이션을 별도로 내보낼 필요가 없습니다.

<a name="language-files"></a>
### 언어 파일 (Language Files)

패키지에 [언어 파일](/docs/10.x/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드를 사용하여 Laravel에 로드 방법을 알려주십시오. 예를 들어 패키지 이름이 `courier`일 경우, 서비스 프로바이더 `boot` 메서드에 다음을 추가합니다:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 문자열은 `package::file.line` 구문으로 참조합니다. 예를 들어 `courier` 패키지의 `messages` 파일 안 `welcome` 라인을 다음과 같이 불러올 수 있습니다:

```
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일을 등록하려면 `loadJsonTranslationsFrom` 메서드를 사용하세요. 이 메서드는 JSON 번역 파일이 위치한 디렉토리 경로를 인자로 받습니다:

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
#### 언어 파일 퍼블리싱 (Publishing Language Files)

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉토리로 퍼블리싱하고 싶다면, 서비스 프로바이더에서 `publishes` 메서드를 사용하십시오. `publishes` 메서드는 패키지 경로와 퍼블리시 위치를 매핑하는 배열을 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리싱하려면 다음과 같이 합니다:

```
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
```

이제 사용자가 `vendor:publish` Artisan 명령어를 실행할 때, 언어 파일이 지정한 위치로 퍼블리싱됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/10.x/views)를 Laravel에 등록하려면, 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하여 뷰 경로를 알려야 합니다. 이 메서드는 뷰 템플릿 경로와 패키지 이름 두 개의 인자를 받습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음과 같이 작성합니다:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 구문으로 참조할 수 있습니다. 따라서 `courier` 패키지의 `dashboard` 뷰를 불러오려면 다음과 같이 합니다:

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드 (Overriding Package Views)

`loadViewsFrom` 메서드 사용 시 Laravel은 뷰를 위한 두 위치를 등록합니다. 하나는 애플리케이션의 `resources/views/vendor` 디렉토리이고, 다른 하나는 지정한 패키지 뷰 디렉토리입니다. 예를 들어 `courier` 패키지의 경우, Laravel은 먼저 개발자가 애플리케이션 `resources/views/vendor/courier` 경로에 뷰를 커스터마이즈했는지 확인합니다. 만약 커스터마이즈된 뷰가 없으면 패키지 내 뷰 디렉토리에서 뷰를 찾습니다. 이를 통해 사용자는 패키지 뷰를 쉽게 재정의할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱 (Publishing Views)

패키지 뷰를 애플리케이션 `resources/views/vendor` 디렉토리로 퍼블리싱 가능하게 하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. `publishes`는 패키지 뷰 경로와 퍼블리시 위치를 배열로 받습니다:

```
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
```

이제 사용자가 `vendor:publish` Artisan 명령어 실행 시, 뷰 파일들이 지정한 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

Blade 컴포넌트를 사용하는 패키지를 개발하거나, 컴포넌트를 비표준 디렉토리에 두는 경우에는 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 Laravel이 컴포넌트를 인식합니다. 보통은 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

컴포넌트가 등록되면, 별칭을 통해 다음과 같이 렌더링 가능합니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩 (Autoloading Package Components)

또는 `componentNamespace` 메서드를 사용하여 네임스페이스 이름 규칙에 따른 자동 로딩을 설정할 수도 있습니다. 예를 들어 `Nightshade` 패키지 내에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 위치한다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 아래와 같은 네임스페이스별 구문으로 패키지 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 PascalCase로 변환하여 자동으로 연결된 클래스를 찾습니다. 또한, 서브디렉토리는 점(`.`) 표기법을 사용해 지원합니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트 (Anonymous Components)

패키지에 익명 컴포넌트가 있다면, 반드시 패키지의 뷰 디렉토리 내 `components` 폴더에 위치해야 합니다 (위 `loadViewsFrom` 메서드에서 지정한 경로 기준). 이렇게 하면 컴포넌트 이름 앞에 패키지 뷰 네임스페이스를 붙여서 렌더링 할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### 내장 `about` Artisan 명령어 ("About" Artisan Command)

Laravel 내장 `about` Artisan 명령어는 애플리케이션 환경과 설정 정보를 요약하여 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 추가 정보를 이 명령어 출력에 포함시킬 수 있습니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 추가합니다:

```
use Illuminate\Foundation\Console\AboutCommand;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어 (Commands)

패키지의 Artisan 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스 이름들의 배열을 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/10.x/artisan)를 통해 실행할 수 있습니다:

```
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
```

<a name="public-assets"></a>
## 퍼블릭 자산 (Public Assets)

패키지는 JavaScript, CSS, 이미지 같은 자산을 포함할 수 있습니다. 이런 자산을 애플리케이션의 `public` 디렉토리로 퍼블리싱하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 예제에선 `public` 자산 그룹 태그도 추가하여 관련 자산을 쉽게 퍼블리싱하도록 합니다:

```
/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

패키지 사용자가 `vendor:publish` 명령어를 실행하면 자산이 지정된 위치로 복사됩니다. 패키지가 업데이트 될 때마다 자산을 덮어쓰기 위해 `--force` 플래그를 같이 사용하는 것이 일반적입니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지의 자산과 리소스를 그룹별로 나누어 선택적으로 퍼블리시하도록 하고 싶을 수 있습니다. 예를 들어, 패키지 설정 파일은 퍼블리시하지만 자산 파일은 퍼블리시하지 않도록 할 수도 있습니다. 이를 위해 서비스 프로바이더에서 `publishes` 메서드 호출 시 "태그"를 지정하여 그룹핑할 수 있습니다. 예를 들어 `courier` 패키지에서 `courier-config`와 `courier-migrations` 두 그룹을 다음과 같이 지정할 수 있습니다:

```
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
```

사용자는 다음과 같이 태그를 지정해서 각 그룹을 따로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```