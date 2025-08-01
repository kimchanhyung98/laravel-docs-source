# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 참고 사항](#a-note-on-facades)
- [패키지 자동 등록(디스커버리)](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정 파일](#configuration)
    - [라우트](#routes)
    - [마이그레이션](#migrations)
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

패키지는 라라벨에 기능을 추가하는 기본적인 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜를 편리하게 다룰 수 있는 방법을 제공하거나, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연결하는 기능을 제공하는 등, 다양한 형태일 수 있습니다.

패키지에는 여러 유형이 있습니다. 어떤 패키지는 독립적으로 동작하여, 어떤 PHP 프레임워크와도 사용할 수 있습니다. Carbon과 Pest가 이러한 독립형 패키지의 예시입니다. 이 패키지들은 여러분의 `composer.json` 파일에 추가하기만 하면 라라벨에서 사용할 수 있습니다.

반면, 일부 패키지는 오직 라라벨에서 사용하도록 설계되어 있습니다. 이런 패키지는 라라벨 애플리케이션의 기능을 강화하기 위해 라우트, 컨트롤러, 뷰, 설정 파일 등을 포함할 수 있습니다. 이 가이드에서는 주로 라라벨 전용 패키지의 개발 방법에 대해 설명합니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고 사항

라라벨 애플리케이션을 개발할 때는 contract와 facade 중 어느 쪽을 사용하든 테스트 가능성 측면에서 큰 차이가 없습니다. 다만, 패키지를 개발할 때는 패키지가 라라벨의 모든 테스트 헬퍼를 바로 사용할 수 없는 경우가 많습니다. 만약 패키지 테스트를 실제 라라벨 애플리케이션 내부에 설치된 것처럼 작성하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 등록(디스커버리)

라라벨 애플리케이션의 `bootstrap/providers.php` 파일에는 라라벨이 로드해야 할 서비스 프로바이더 목록이 있습니다. 하지만 사용자가 직접 프로바이더를 이 목록에 추가하지 않아도 되도록, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의하면 라라벨이 자동으로 로드합니다. 서비스 프로바이더 외에도 등록할 [파사드](/docs/12.x/facades)도 이곳에 정의할 수 있습니다.

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

패키지가 자동 등록(디스커버리)에 맞게 설정되면, 라라벨이 해당 패키지가 설치될 때 서비스 프로바이더와 파사드를 자동으로 등록해 사용자에게 더욱 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 자동 등록 사용 안 하기

패키지를 사용하는 입장에서 특정 패키지의 자동 등록(디스커버리)을 비활성화하고 싶을 때는, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 패키지 이름을 나열하면 됩니다.

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

패키지 자동 등록을 모든 패키지에 대해 비활성화하려면, `dont-discover` 설정에 `*` 문자를 사용할 수 있습니다.

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

[서비스 프로바이더](/docs/12.x/providers)는 여러분의 패키지와 라라벨 사이의 연결 고리 역할을 합니다. 서비스 프로바이더는 라라벨의 [서비스 컨테이너](/docs/12.x/container)에 필요한 바인딩을 추가하고, 패키지의 뷰, 설정, 언어 파일 등 리소스가 어디에 있는지 라라벨에게 알려줍니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장하며, `register`와 `boot`라는 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으므로 패키지의 의존성에 이를 추가해야 합니다. 서비스 프로바이더의 구조와 역할에 대해 더 알고 싶다면 [서비스 프로바이더 문서](/docs/12.x/providers)를 참고하십시오.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정 파일

일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시(publish)해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정 값을 쉽게 오버라이드할 수 있습니다. 설정 파일을 퍼블리시하도록 만들려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출합니다.

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

이제 패키지 사용자가 라라벨의 `vendor:publish` 명령어를 실행하면, 해당 파일이 지정된 위치로 복사됩니다. 설정 파일이 퍼블리시된 이후에는 다른 설정 파일과 마찬가지로 값을 가져올 수 있습니다.

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일에는 클로저(익명 함수)를 정의하지 않아야 합니다. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 이 함수들을 올바르게 직렬화(serialize)할 수 없습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 병합

패키지의 설정 파일을 애플리케이션에 퍼블리시된 기존 설정과 병합할 수도 있습니다. 이렇게 하면 사용자가 오버라이드하고 싶은 옵션만 설정 파일에 추가할 수 있습니다. 설정 값 병합은 서비스 프로바이더의 `register` 메서드 안에서 `mergeConfigFrom` 메서드를 사용하면 됩니다.

`mergeConfigFrom` 메서드는 첫 번째 인수로 패키지의 설정 파일 경로, 두 번째 인수로 애플리케이션의 설정 파일명을 받습니다.

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
> 이 메서드는 설정 배열의 최상위 레벨만 병합합니다. 사용자가 다차원 배열 옵션 중 일부만 정의한 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트 파일이 포함되어 있다면, `loadRoutesFrom` 메서드로 라우트를 등록할 수 있습니다. 이 메서드는 애플리케이션의 라우트가 이미 캐시(`route:cache`)되어 있는지도 자동으로 확인하여, 캐시되어 있으면 해당 파일을 다시 로드하지 않습니다.

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
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/12.x/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용해 해당 디렉터리나 파일 안에 마이그레이션이 들어 있다고 라라벨에 알릴 수 있습니다. 라라벨이 마이그레이션을 퍼블리시할 때, 파일 이름의 타임스탬프를 현재 날짜와 시간으로 자동 업데이트합니다.

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
### 언어 파일

패키지에 [언어 파일](/docs/12.x/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드로 라라벨이 언어 파일을 로드하는 방법을 지정할 수 있습니다. 예를 들어, 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 다음 코드를 추가합니다.

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지의 번역 문구는 `package::file.line` 구문을 사용해 참조합니다. 예를 들어, `courier` 패키지의 `messages` 파일에 있는 `welcome` 문구는 아래와 같이 사용할 수 있습니다.

```php
echo trans('courier::messages.welcome');
```

패키지의 JSON 언어 파일을 등록하려면 `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 패키지의 JSON 번역 파일이 들어있는 디렉터리 경로를 인수로 받습니다.

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
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 퍼블리시할 패키지 경로와 복사될 위치를 배열로 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 작성할 수 있습니다.

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

이제 사용자들이 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정한 위치에 퍼블리시됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/12.x/views)를 라라벨에 등록하려면 뷰가 어디에 위치하는지 알려줘야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하면 됩니다. 이 메서드는 뷰 템플릿의 경로와 패키지 이름, 두 개의 인수를 받습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음을 추가합니다.

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지의 뷰는 `package::view` 구문으로 참조합니다. 뷰 경로가 등록되었으면, 예를 들어 `courier` 패키지의 `dashboard` 뷰를 아래와 같이 사용할 수 있습니다.

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용하면, 라라벨은 실제로 두 위치에서 뷰 파일을 찾습니다. 첫 번째는 애플리케이션의 `resources/views/vendor` 디렉터리이고, 두 번째는 `loadViewsFrom`에 지정한 패키지 디렉터리입니다. 예를 들어 `courier` 패키지의 경우, 개발자가 `resources/views/vendor/courier`에 커스텀 뷰를 두었다면, 그것이 우선적으로 사용됩니다. 그렇지 않을 경우, 패키지 디렉터리의 뷰가 사용됩니다. 이 방식은 패키지 사용자가 뷰를 쉽게 커스터마이즈/오버라이드할 수 있게 해줍니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시할 수 있습니다. 이 기능을 사용하면 사용자들이 직접 뷰를 수정할 수 있습니다. `publishes` 메서드는 퍼블리시할 뷰 경로와 위치를 배열로 받습니다.

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

이제 사용자들이 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 뷰가 지정한 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

패키지에서 Blade 컴포넌트를 제공하거나, 일반적인 위치가 아닌 디렉터리에 컴포넌트를 둘 경우, 라라벨에서 해당 컴포넌트 클래스(와 HTML 태그 별칭)를 수동으로 등록해야 합니다. 보통 패키지의 서비스 프로바이더의 `boot` 메서드에서 등록합니다.

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

이렇게 등록한 후에는 별칭 태그로 컴포넌트를 사용할 수 있습니다.

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는, `componentNamespace` 메서드를 사용하면, 컨벤션에 따라 컴포넌트 클래스를 자동으로 로드할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 들어 있다면 다음과 같이 작성할 수 있습니다.

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

이렇게 하면 패키지 벤더 네임스페이스를 사용해 `package-name::` 구문으로 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 관련 클래스를 자동으로 찾아줍니다. 또한, 디렉터리 구분은 "점(.)" 표기법을 사용할 수 있습니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지 내에 익명 컴포넌트를 포함하는 경우, 해당 컴포넌트는 패키지 "views" 디렉터리 안의 `components` 디렉터리에 위치해야 합니다([loadViewsFrom 메서드](#views)에서 지정한 디렉터리 기준). 그런 다음, 패키지의 뷰 네임스페이스 접두어를 붙여 컴포넌트를 사용할 수 있습니다.

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어

라라벨 내장 `about` 아티즌 명령어는 애플리케이션의 환경 및 설정 정보를 요약해서 보여줍니다. 패키지에서도 `AboutCommand` 클래스를 통해 이 명령어의 출력에 추가 정보를 표시할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 이 정보를 추가합니다.

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
## 명령어

패키지에서 제공하는 아티즌 명령어를 라라벨에 등록하려면, `commands` 메서드를 사용하면 됩니다. 이 메서드는 명령어 클래스 이름 배열을 인수로 받습니다. 등록이 완료되면 [Artisan CLI](/docs/12.x/artisan)에서 명령어를 실행할 수 있습니다.

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
### 최적화 명령어

라라벨의 [최적화 명령어](/docs/12.x/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰 등을 캐시합니다. 패키지에서도 `optimizes` 메서드를 사용해, 라라벨의 `optimize` 및 `optimize:clear` 명령어 실행 시 같이 동작할 아티즌 명령어를 등록할 수 있습니다.

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
## 퍼블릭 에셋

패키지에 JavaScript, CSS, 이미지 등과 같은 에셋 파일이 있다면, 이 파일들을 애플리케이션의 `public` 디렉터리에 퍼블리시할 수 있습니다. 이를 위해 서비스 프로바이더의 `publishes` 메서드를 사용합니다. 아래 예시에서는 관련 에셋들을 한 그룹으로 묶기 위한 "public" 태그도 함께 추가합니다.

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

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 에셋이 지정한 위치로 복사됩니다. 일반적으로 패키지 업데이트 시마다 에셋을 덮어써야 할 수 있으므로, `--force` 플래그를 사용할 수 있습니다.

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

패키지의 에셋이나 리소스를 그룹별로 따로 퍼블리시할 수 있도록 설정할 수 있습니다. 예를 들어, 사용자가 패키지의 설정 파일만 선택해서 퍼블리시하고, 에셋은 퍼블리시하지 않도록 할 수 있습니다. 이때 "태그(tag)" 기능을 사용합니다. 예를 들어, `courier` 패키지의 설정 파일(`courier-config`)과 마이그레이션(`courier-migrations`)을 별도 그룹으로 퍼블리시하도록 `boot` 메서드에서 태그를 지정할 수 있습니다.

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

이제 사용자는 퍼블리시할 파일 그룹의 태그를 지정하여 별도로 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag=courier-config
```

또한, `--provider` 플래그를 사용해 서비스 프로바이더에서 정의된 모든 퍼블리시 파일을 한 번에 퍼블리시할 수도 있습니다.

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
