# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 한 가지 주의사항](#a-note-on-facades)
- [패키지 발견 (Package Discovery)](#package-discovery)
- [서비스 프로바이더 (Service Providers)](#service-providers)
- [리소스 (Resources)](#resources)
    - [설정 (Configuration)](#configuration)
    - [라우트 (Routes)](#routes)
    - [마이그레이션 (Migrations)](#migrations)
    - [언어 파일 (Language Files)](#language-files)
    - [뷰 (Views)](#views)
    - [뷰 컴포넌트 (View Components)](#view-components)
    - [“about” Artisan 명령어](#about-artisan-command)
- [명령어 (Commands)](#commands)
    - [최적화 명령어 (Optimize Commands)](#optimize-commands)
- [공개 자산 (Public Assets)](#public-assets)
- [파일 그룹 배포 (Publishing File Groups)](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 예를 들어, 날짜 작업에 좋은 도구인 [Carbon](https://github.com/briannesbitt/Carbon)같은 패키지나, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연결할 수 있게 해주는 패키지가 있습니다.

패키지 유형에는 여러 가지가 있습니다. 어떤 패키지는 독립형(stand-alone)으로, 모든 PHP 프레임워크에서 사용할 수 있습니다. Carbon과 Pest가 그 예입니다. 이런 패키지들은 `composer.json` 파일에 요구(require)하기만 하면 Laravel에서도 사용할 수 있습니다.

반면, Laravel 전용으로 만들어진 패키지도 있습니다. 이들은 라우트, 컨트롤러, 뷰, 설정 파일 등을 포함하여 Laravel 애플리케이션의 기능을 확장하는 데 특화되어 있습니다. 이 가이드는 주로 Laravel 전용 패키지 개발에 초점을 맞추고 있습니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 한 가지 주의사항 (A Note on Facades)

Laravel 애플리케이션을 작성할 때는 계약(contracts)과 파사드(facades)를 사용해도 테스트 가능성이 본질적으로 비슷하므로 크게 신경 쓰지 않아도 됩니다. 하지만 패키지를 개발할 때는 Laravel의 모든 테스트 도구를 사용할 수 없는 경우가 많습니다. 만약 패키지가 Laravel 애플리케이션 내부에 설치된 것처럼 테스트를 작성하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용하는 것이 좋습니다.

<a name="package-discovery"></a>
## 패키지 발견 (Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 로드될 서비스 프로바이더 목록이 있습니다. 그러나 사용자가 직접 서비스 프로바이더를 추가하지 않아도 되도록, 패키지의 `composer.json` 파일 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 그러면 Laravel이 자동으로 로드합니다. 서비스 프로바이더 뿐만 아니라, 등록할 [파사드](/docs/12.x/facades)도 나열할 수 있습니다:

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

패키지가 패키지 발견으로 설정되면, 설치 시 Laravel이 해당 서비스 프로바이더와 파사드를 자동으로 등록하여 사용자에게 편리한 설치 환경을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 발견 비활성화하기 (Opting Out of Package Discovery)

패키지를 사용하는 입장에서 특정 패키지에 대해 자동 발견을 끄고 싶다면, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 해당 패키지 이름을 적어두면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

한편, 모든 패키지에 대해 패키지 발견을 비활성화하려면 `dont-discover`에 `"*"` 문자를 사용하면 됩니다:

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

[서비스 프로바이더](/docs/12.x/providers)는 패키지와 Laravel을 연결하는 핵심 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/12.x/container)에 바인딩 작업을 수행하고 패키지의 뷰, 설정, 언어 파일 등의 리소스를 어디에서 불러올지 Laravel에 알려줍니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장하며, 기본적으로 `register`와 `boot` 메서드 두 개를 가집니다. 이 기본 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으므로, 여러분의 패키지 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 역할에 대해 더 알고 싶으면 [공식 문서](/docs/12.x/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

보통 패키지의 설정 파일을 애플리케이션의 `config` 디렉토리로 복사(퍼블리시)해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정을 쉽게 덮어쓸 수 있습니다. 설정 파일을 퍼블리시할 수 있도록 하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 사용자들이 Laravel의 `vendor:publish` 명령어를 실행하면, 이 파일이 지정된 위치로 복사됩니다. 퍼블리시가 완료되면 설정 값은 일반 설정 파일처럼 접근할 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 안에 클로저(Closure)를 정의하지 마세요. 이들은 사용자가 `config:cache` Artisan 명령어를 실행할 때 제대로 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 (Default Package Configuration)

패키지 설정 파일과 애플리케이션에 퍼블리시된 설정 파일을 병합할 수도 있습니다. 이렇게 하면 사용자가 퍼블리시된 설정 파일에서 오버라이드할 항목만 정의하면 됩니다. 파일 병합은 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 써서 수행합니다.

`mergeConfigFrom`는 첫 번째 인자로 패키지 설정 파일 경로를, 두 번째 인자로 애플리케이션 설정 파일 이름을 받습니다:

```php
/**
 * Register any package services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> 이 메서드는 설정 배열의 첫 번째 단계만 병합합니다. 만약 다차원 배열의 일부만 정의한다면 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 사용해 불러올 수 있습니다. 이 메서드는 애플리케이션 라우트가 이미 캐시되었는지 자동 판단하며, 캐시되었다면 라우트 파일을 다시 로드하지 않습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/12.x/migrations)이 있다면, `publishesMigrations` 메서드를 사용해 Laravel에 알려줄 수 있습니다. Laravel이 마이그레이션을 퍼블리시할 때는 파일명에 현재 날짜와 시간을 자동으로 반영합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishesMigrations([
        __DIR__.'/../database/migrations' => database_path('migrations'),
    ]);
}
```

<a name="language-files"></a>
### 언어 파일 (Language Files)

패키지에 [언어 파일](/docs/12.x/localization)이 포함되어 있으면, `loadTranslationsFrom` 메서드로 Laravel에 불러오는 방식을 알려줘야 합니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음과 같이 작성하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역문은 `package::file.line` 형식으로 참조합니다. 예를 들어 `courier` 패키지의 `messages` 파일 안 `welcome` 번역문을 불러오려면 다음과 같이 작성합니다:

```php
echo trans('courier::messages.welcome');
```

패키지용 JSON 번역 파일은 `loadJsonTranslationsFrom` 메서드를 사용하여 등록할 수 있습니다. 이 메서드는 JSON 파일들이 포함된 경로를 받습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리시하기 (Publishing Language Files)

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉토리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 메서드는 패키지 경로와 복사할 위치를 배열로 받습니다. 예를 들어 `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 작성합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

이제 사용자들이 `vendor:publish` Artisan 명령어를 실행하면 패키지의 언어 파일이 지정된 위치로 복사됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/12.x/views)를 Laravel에 등록하려면, 뷰의 위치를 Laravel에 알려줘야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하며, 이 메서드는 두 개의 인자가 필요합니다: 뷰 템플릿 경로와 패키지 이름. 예를 들어 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 다음을 추가하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 형식으로 참조합니다. 따라서 서비스 프로바이더를 통해 뷰 경로를 등록하면, 다음처럼 `courier` 패키지의 `dashboard` 뷰를 불러올 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 재정의하기 (Overriding Package Views)

`loadViewsFrom` 메서드를 사용하면 Laravel이 뷰에 대해 두 개의 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉토리와 여러분이 지정한 패키지 뷰 디렉토리입니다. 예를 들어 `courier` 패키지를 쓰는 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier`에 커스텀 뷰 파일을 둔 것이 있는지 확인합니다. 만약 없다면 패키지의 원본 뷰 디렉토리에서 뷰를 찾습니다. 이렇게 해서 사용자들이 패키지 뷰를 쉽게 변경하거나 덮어쓸 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리시하기 (Publishing Views)

패키지의 뷰를 애플리케이션의 `resources/views/vendor` 디렉토리로 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하면 됩니다. 이 메서드는 패키지 뷰 경로와 퍼블리시 위치를 배열로 받습니다:

```php
/**
 * Bootstrap the package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

사용자가 `vendor:publish` Artisan 명령어를 실행하면 패키지의 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

Blade 컴포넌트를 사용하는 패키지를 만들거나 비표준 디렉토리에 컴포넌트를 둘 경우, 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 Laravel이 컴포넌트를 인식할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에 컴포넌트를 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

컴포넌트를 등록하면 다음처럼 별칭 태그로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩 (Autoloading Package Components)

또는 `componentNamespace` 메서드를 이용해 컴포넌트 클래스를 규칙에 따라 자동 로딩할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 있다면 다음과 같이 등록합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 패키지 컴포넌트를 `package-name::` 구문으로 별칭을 붙여 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 연결된 클래스를 자동으로 찾습니다. 하위 디렉토리도 "점(dot)" 표기법으로 지원합니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트 (Anonymous Components)

패키지가 익명 컴포넌트를 포함한다면, 반드시 패키지 뷰 디렉토리 내의 `components` 폴더에 위치해야 합니다(`loadViewsFrom`로 지정한 경로 기준). 그런 다음 패키지 뷰 네임스페이스를 붙여 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### “about” Artisan 명령어

Laravel에 내장된 `about` Artisan 명령어는 애플리케이션 환경과 설정의 요약 정보를 제공합니다. 패키지들도 `AboutCommand` 클래스를 통해 이 명령어 출력에 정보를 덧붙일 수 있습니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 추가합니다:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어 (Commands)

패키지의 Artisan 명령어를 Laravel에 등록하려면 `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스명 배열을 받습니다. 등록 후에는 [Artisan CLI](/docs/12.x/artisan)에서 명령어를 실행할 수 있습니다:

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
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

<a name="optimize-commands"></a>
### 최적화 명령어 (Optimize Commands)

Laravel의 [최적화 명령어](/docs/12.x/deployment#optimization)는 애플리케이션 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 사용하면 패키지 고유의 Artisan 명령어를 등록해, `optimize` 및 `optimize:clear` 명령어 실행 시 함께 호출되도록 할 수 있습니다:

```php
/**
 * Bootstrap any package services.
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
```

<a name="public-assets"></a>
## 공개 자산 (Public Assets)

패키지는 JavaScript, CSS, 이미지 같은 자산을 포함할 수 있습니다. 애플리케이션의 `public` 디렉토리로 이런 자산을 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 예시는 `public` 자산 그룹 태그도 추가하는 방법을 보여줍니다. 이렇게 하면 관련 자산 그룹을 쉽게 퍼블리시할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 사용자가 `vendor:publish` 명령어를 실행하면, 자산들이 지정된 위치로 복사됩니다. 보통 자산은 패키지가 업데이트될 때마다 덮어써야 하므로 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 배포 (Publishing File Groups)

별도의 패키지 자산과 리소스 그룹을 따로 퍼블리시하고 싶을 수 있습니다. 예를 들어, 설정 파일만 퍼블리시하고 자산은 강제로 퍼블리시하지 않도록 할 수 있습니다. 이는 서비스 프로바이더 내에서 `publishes` 호출 시 태그를 지정해 관리합니다. 예를 들어, `courier` 패키지의 설정 파일과 마이그레이션에 대해 두 개의 태그(`courier-config`와 `courier-migrations`)를 지정해 봅니다:

```php
/**
 * Bootstrap any package services.
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
```

이제 사용자는 `vendor:publish` 명령어에서 태그를 지정하여 다음처럼 그룹별로 자산을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

또한 `--provider` 플래그를 이용하면 패키지의 서비스 프로바이더에 정의된 모든 퍼블리시 가능한 파일을 한꺼번에 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```