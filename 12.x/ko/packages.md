# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드 관련 참고사항](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
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
    - [재시작(리로드) 명령어](#reload-commands)
- [퍼블릭 애셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel의 기능을 확장하는 기본적인 방법입니다. 예를 들어, [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜를 다루기 위한 훌륭한 방법을 제공하는 패키지나, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연결할 수 있도록 해주는 패키지 등이 있습니다.

패키지는 종류에 따라 구분할 수 있습니다. 일부 패키지는 독립적(stand-alone)으로 동작하여, 어떤 PHP 프레임워크에서도 사용할 수 있습니다. Carbon과 Pest가 대표적인 예시입니다. 이러한 패키지들은 `composer.json` 파일에 추가(require)하여 Laravel에서 그대로 사용할 수 있습니다.

반면, Laravel에서만 사용하도록 설계된 패키지도 있습니다. 이러한 패키지들은 라우트, 컨트롤러, 뷰, 그리고 Laravel 애플리케이션을 개선하기 위한 설정 파일 등 Laravel에 특화된 부분을 포함하고 있습니다. 이 가이드에서는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드 관련 참고사항

Laravel 애플리케이션을 작성할 때에는 contract(인터페이스)나 파사드(facade)를 사용하는 것이 테스트 가능성 측면에서 거의 동일한 수준을 제공합니다. 그러나 패키지를 작성할 때는, 패키지가 Laravel의 모든 테스팅 헬퍼에 접근할 수 없다는 점을 유의해야 합니다. 일반적인 Laravel 애플리케이션처럼 패키지 테스트를 작성하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리 (Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 로딩할 서비스 프로바이더 목록이 포함되어 있습니다. 그러나 패키지 사용자가 이 목록에 서비스 프로바이더를 직접 추가하지 않도록, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의하면 Laravel이 자동으로 로딩해줍니다. 서비스 프로바이더 외에도, 등록이 필요한 [파사드](/docs/12.x/facades)도 함께 지정할 수 있습니다:

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

패키지가 디스커버리 설정을 완료했다면, 사용자가 패키지를 설치할 때 Laravel이 자동으로 서비스 프로바이더와 파사드를 등록하므로 손쉬운 설치 경험을 제공할 수 있습니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 디스커버리 비활성화

만약 특정 패키지의 디스커버리를 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 해당 패키지명을 추가하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

디스커버리를 모든 패키지에 대해 비활성화하려면, `dont-discover` 지시문 내에서 `*` 문자를 사용할 수 있습니다:

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

[서비스 프로바이더](/docs/12.x/providers)는 패키지와 Laravel을 연결하는 접점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/12.x/container)에 바인딩을 등록하고, 뷰, 설정, 언어 파일 등 패키지 리소스가 어디에 위치해 있는지 Laravel에 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot`라는 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으므로, 패키지의 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 자세히 알아보고 싶다면 [관련 문서](/docs/12.x/providers)를 참고하시기 바랍니다.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 파일 (Configuration)

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리싱해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정 옵션을 쉽게 오버라이드(덮어쓰기) 할 수 있습니다. 설정 파일을 퍼블리싱할 수 있도록 하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하면 됩니다:

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

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 지정한 위치로 설정 파일이 복사됩니다. 퍼블리싱된 설정 값은 다음처럼 일반 설정 파일과 동일하게 접근할 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일에서 클로저(익명 함수)를 정의해서는 안 됩니다. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 직렬화가 올바르게 처리되지 않습니다.

<a name="default-package-configuration"></a>
#### 패키지 설정 기본값 병합하기

패키지의 설정 파일을 애플리케이션에 퍼블리싱하는 것 외에도, 기본값을 함께 병합할 수 있습니다. 이를 통해 사용자는 오버라이드가 필요한 옵션만 설정 파일에 지정하면 되고, 나머지는 패키지 기본값을 사용할 수 있습니다. 설정 파일 값을 병합하려면, 서비스 프로바이더의 `register` 메서드 내에서 `mergeConfigFrom` 메서드를 사용합니다.

`mergeConfigFrom` 메서드는 첫 번째 인수로 패키지 설정 파일의 경로, 두 번째 인수로 애플리케이션 내 설정 파일명을 받습니다:

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
> 이 메서드는 설정 배열의 1단계만 병합합니다. 다차원 설정 배열을 부분적으로 정의하면, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 사용해 라우트 파일을 로드할 수 있습니다. 이 메서드는 애플리케이션의 라우트 캐시 여부를 자동으로 확인하고, 이미 캐시되어 있다면 라우트 파일을 추가로 로드하지 않습니다:

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

패키지에 [데이터베이스 마이그레이션](/docs/12.x/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 통해 Laravel에 마이그레이션 폴더 또는 파일이 어디에 있는지 알릴 수 있습니다. Laravel이 마이그레이션을 퍼블리시하면, 파일명에 현재 날짜와 시간이 반영된 타임스탬프가 자동으로 갱신됩니다:

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

패키지에 [언어 파일](/docs/12.x/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드를 사용해 Laravel에 해당 파일을 로드하는 방법을 알려줄 수 있습니다. 예를 들어, 패키지명이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 아래와 같이 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지의 번역 문자열은 `package::file.line` 형식으로 참조할 수 있습니다. 예를 들어, `courier` 패키지의 `messages` 파일에 정의된 `welcome` 문구를 다음과 같이 로드할 수 있습니다:

```php
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일을 등록하고 싶다면, `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 패키지의 JSON 번역 파일이 포함된 디렉터리의 경로를 받습니다:

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

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 패키지 경로와 퍼블리시할 위치의 배열을 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 작성합니다:

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

이제 사용자가 Laravel `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정한 위치에 퍼블리시됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/12.x/views)를 Laravel에 등록하려면, 해당 뷰 파일의 경로를 알려주어야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하면 됩니다. 이 메서드는 첫 번째 인수로 뷰 파일이 위치한 경로, 두 번째 인수로 패키지명을 받습니다. 예를 들어, 패키지명이 `courier`일 때는 아래와 같습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지의 뷰는 `package::view` 형식으로 참조할 수 있습니다. 따라서 뷰 경로가 서비스 프로바이더에 등록되면, 아래처럼 `courier` 패키지의 `dashboard` 뷰를 로드할 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom`을 사용할 때, Laravel은 실제로 두 곳을 뷰 경로로 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 패키지에서 지정한 뷰 디렉터리입니다. 예를 들어 `courier` 패키지의 경우, 먼저 개발자가 `resources/views/vendor/courier`에 뷰 파일을 커스터마이즈하여 넣었는지 확인한 뒤, 없으면 패키지의 기본 뷰 디렉터리에서 파일을 로드합니다. 이를 통해 패키지 사용자는 쉽게 뷰를 커스터마이즈하거나 오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰 파일을 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. 이 메서드는 패키지 뷰 경로와 원하는 퍼블리시 위치의 배열을 받습니다:

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

이제 사용자가 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 뷰 파일이 지정한 곳에 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

Blade 컴포넌트를 사용하는 패키지를 만들거나, 컴포넌트를 기본이 아닌 디렉터리에 배치한다면, 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 Laravel이 컴포넌트를 올바르게 찾을 수 있습니다. 보통 이 등록 작업은 패키지 서비스 프로바이더의 `boot` 메서드에서 수행합니다:

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

등록이 완료되면 해당 컴포넌트를 다음과 같이 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는, `componentNamespace` 메서드를 이용해 컴포넌트 클래스 저장소를 네임스페이스 기반으로 자동 로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스 아래 `Calendar`와 `ColorPicker` 컴포넌트가 있다면 다음처럼 등록할 수 있습니다:

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

이렇게 하면, 벤더 네임스페이스와 함께 `package-name::` 문법으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스(PascalCase)로 변환해 해당 클래스를 자동으로 연결합니다. 서브디렉터리는 "점(.) 표기법"으로 사용할 수 있습니다.

<a name="anonymous-components"></a>
#### 익명(Anonymous) 컴포넌트

패키지에 익명(anonymous) 컴포넌트가 포함되어 있다면, 해당 컴포넌트는 패키지 "뷰" 디렉터리 하위의 `components` 디렉터리에 위치해야 합니다([loadViewsFrom 메서드](#views)로 지정한 디렉터리 기준). 이후 컴포넌트 이름 앞에 패키지의 뷰 네임스페이스를 붙여서 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어 ("About" Artisan Command)

Laravel의 내장 `about` 아티즌 명령어는 애플리케이션 환경과 설정 개요를 제공합니다. 패키지에서는 `AboutCommand` 클래스를 통해 이 명령어의 출력 정보에 추가적인 내용을 포함할 수 있습니다. 보통은 패키지 서비스 프로바이더의 `boot` 메서드에서 다음처럼 정보를 추가합니다:

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

패키지의 아티즌 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스명의 배열을 인수로 받습니다. 등록된 명령어는 [아티즌 CLI](/docs/12.x/artisan)를 통해 실행할 수 있습니다:

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

Laravel의 [optimize 명령어](/docs/12.x/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 사용하면, 패키지에서 `optimize`와 `optimize:clear`가 실행될 때 함께 실행될 자체 아티즌 명령어를 등록할 수 있습니다:

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

<a name="reload-commands"></a>
### 재시작(리로드) 명령어 (Reload Commands)

Laravel의 [reload 명령어](/docs/12.x/deployment#reloading-services)는 실행 중인 서비스를 종료시켜 시스템 프로세스 모니터가 자동으로 다시 시작할 수 있도록 해줍니다. `reloads` 메서드를 사용하면, `reload` 명령어가 실행될 때 호출될 패키지의 자체 아티즌 명령어를 등록할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->reloads('package:reload');
    }
}
```

<a name="public-assets"></a>
## 퍼블릭 애셋 (Public Assets)

패키지에 JavaScript, CSS, 이미지와 같은 애셋이 포함될 수 있습니다. 이러한 애셋을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하면 됩니다. 아래 예시에서는 `public` 애셋 그룹 태그도 추가하여 관련 애셋 그룹을 쉽게 퍼블리시할 수 있도록 했습니다:

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

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 애셋이 지정한 위치로 복사됩니다. 패키지의 업데이트 시마다 자주 덮어써야 하므로, `--force` 플래그를 함께 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지의 애셋과 리소스를 그룹별로 별도 퍼블리시할 수 있습니다. 예를 들어, 패키지의 모든 애셋을 퍼블리시하지 않고 설정 파일만 따로 퍼블리시할 수 있도록 하려면, `publishes` 메서드에서 태그(tag)를 지정하면 됩니다. 아래 예시는 `courier` 패키지에 대해 두 개의 퍼블리시 그룹(`courier-config`와 `courier-migrations`)을 정의하는 방식입니다:

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

이제 사용자는 퍼블리시 명령어에서 해당 태그를 지정하여 특정 그룹만 별도로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

패키지 서비스 프로바이더에서 정의한 모든 퍼블리셔블 파일을 한 번에 퍼블리시하려면, `--provider` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
