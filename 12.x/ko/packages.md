# 패키지 개발

- [소개](#introduction)
    - [파사드(Facade)에 대한 참고 사항](#a-note-on-facades)
- [패키지 자동 등록(Package Discovery)](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정(Configuration)](#configuration)
    - [마이그레이션(Migrations)](#migrations)
    - [라우트(Routes)](#routes)
    - [언어 파일(Language Files)](#language-files)
    - [뷰(Views)](#views)
    - [뷰 컴포넌트(View Components)](#view-components)
    - ["About" Artisan 명령어](#about-artisan-command)
- [명령어(Commands)](#commands)
    - [최적화 명령어](#optimize-commands)
- [퍼블릭 자산(Public Assets)](#public-assets)
- [파일 그룹 퍼블리싱(Publishing File Groups)](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)과 같이 날짜를 다루기 위한 탁월한 도구이거나, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연결할 수 있게 해주는 패키지일 수 있습니다.

패키지에는 여러 종류가 있습니다. 일부 패키지는 독립형(stand-alone)으로, 어떤 PHP 프레임워크에서도 동작합니다. Carbon과 Pest가 그 예입니다. 이들 패키지는 `composer.json` 파일에 추가하여 Laravel에서 사용할 수 있습니다.

반면, 어떤 패키지들은 Laravel 전용으로 개발되었습니다. 이러한 패키지는 라우트, 컨트롤러, 뷰, 그리고 Laravel 애플리케이션을 확장하기 위한 설정 등을 포함할 수 있습니다. 이 가이드에서는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드(Facade)에 대한 참고 사항

Laravel 애플리케이션을 작성할 때는 컨트랙트(Contracts)나 파사드(Facade)를 사용하는 것이 테스트 용이성 측면에서 거의 동일하므로 특별히 신경 쓸 필요가 없습니다. 하지만 패키지를 개발할 때는 Laravel의 모든 테스트용 헬퍼에 접근하지 못할 수도 있습니다. 패키지 테스트를 실제 Laravel 애플리케이션에 설치된 것처럼 작성하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 등록(Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일은 로드되어야 할 서비스 프로바이더 목록을 포함하고 있습니다. 그러나 사용자가 직접 서비스 프로바이더를 목록에 추가하도록 요구하지 않고, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의하면 Laravel이 자동으로 로드할 수 있습니다. 서비스 프로바이더 외에도, 등록하고 싶은 [파사드](/docs/{{version}}/facades)도 함께 정의할 수 있습니다:

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

패키지가 디스커버리(discovery) 설정을 마치면, Laravel은 패키지를 설치할 때 자동으로 서비스 프로바이더와 파사드를 등록하여 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 자동 등록 해제

패키지 사용자가 자동 등록 기능을 비활성화하고 싶을 경우, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 해당 패키지 이름을 추가할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

`dont-discover` 지시어에 `*` 문자를 사용하면 모든 패키지의 자동 등록을 비활성화할 수 있습니다:

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

[서비스 프로바이더](/docs/{{version}}/providers)는 패키지와 Laravel을 연결해주는 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 객체를 바인딩하고, 뷰·설정·언어 파일 등의 패키지 리소스를 로드하는 위치를 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot`라는 두 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 들어 있으므로, 패키지의 의존성에 추가해야 합니다. 구조와 역할에 대해서는 [관련 문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정(Configuration)

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시해야 합니다. 이렇게 하면 사용자들이 기본 설정 값을 쉽게 오버라이드(재정의)할 수 있습니다. 설정 파일을 퍼블리시 가능하게 만들고자 한다면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

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

이제 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 파일이 지정된 위치로 복사됩니다. 설정이 퍼블리시되고 나면, 다른 설정 파일처럼 값을 참조할 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일에 클로저(Closure)를 정의해서는 안 됩니다. 클로저는 사용자가 `config:cache` Artisan 명령어를 실행할 때 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

패키지의 기본 설정 파일과 애플리케이션의 퍼블리시된 사본을 병합할 수도 있습니다. 이렇게 하면 사용자는 오버라이드가 필요한 옵션만 설정 파일에 정의할 수 있고, 나머지는 기본값이 적용됩니다. 설정 파일 값을 병합하려면, 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드의 첫 번째 인자는 패키지의 설정 파일 경로, 두 번째 인자는 애플리케이션이 사용하는 설정 파일 이름입니다.

```php
/**
 * Register any application services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> 이 방법은 설정 배열의 1차원만 병합합니다. 사용자가 다차원 설정 배열을 부분적으로 정의하면, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트(Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드로 로드할 수 있습니다. 이 메서드는 애플리케이션 라우트가 캐시되어 있는지 자동으로 확인하고, 이미 캐시된 경우에는 라우트 파일을 다시 로드하지 않습니다.

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
### 마이그레이션(Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용하여 주어진 디렉터리나 파일이 마이그레이션임을 Laravel에 알릴 수 있습니다. 마이그레이션이 퍼블리시될 때, 파일명에 포함된 타임스탬프가 자동으로 현재 일시로 갱신됩니다.

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
### 언어 파일(Language Files)

패키지에 [언어 파일](/docs/{{version}}/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드를 사용해 Laravel에 로드 방법을 알려줄 수 있습니다. 예시로, 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 아래와 같이 추가하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 라인은 `package::file.line` 구문을 사용해 참조합니다. 예를 들어 `courier` 패키지의 `messages` 파일에 들어 있는 `welcome` 라인을 불러오려면 아래와 같이 사용할 수 있습니다:

```php
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일은 `loadJsonTranslationsFrom` 메서드로 등록할 수 있습니다. 이 메서드는 JSON 번역 파일이 들어 있는 디렉터리 경로를 인자로 받습니다.

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

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리에 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 메서드는 퍼블리시할 패키지 파일 경로와 대상 경로의 배열을 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 하면 됩니다:

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

이제 사용자가 Laravel의 `vendor:publish` Artisan 명령어를 실행하면, 언어 파일이 지정된 위치로 퍼블리시됩니다.

<a name="views"></a>
### 뷰(Views)

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면, 뷰가 어디에 있는지 Laravel에 알려주어야 합니다. `loadViewsFrom` 메서드를 사용하며, 첫 번째 인자는 뷰 템플릿 경로, 두 번째 인자는 패키지 이름입니다. 예를 들어, 패키지 이름이 `courier`라면 `boot` 메서드에 아래와 같이 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 구문을 통해 참조됩니다. 즉, 뷰 경로가 등록된 후에는 아래처럼 `courier` 패키지의 `dashboard` 뷰를 로드할 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드는 실제로 두 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와, 지정한 패키지 뷰 디렉터리입니다. 예를 들어 `courier` 패키지의 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 디렉터리에 커스텀 뷰를 넣었는지 확인합니다. 그렇지 않다면, 지정한 패키지 뷰 디렉터리에서 뷰를 찾습니다. 이 구조는 사용자들이 패키지의 뷰를 쉽게 커스터마이즈/오버라이드할 수 있게 해줍니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰를 애플리케이션의 `resources/views/vendor` 디렉터리에 퍼블리시할 수 있습니다. `publishes` 메서드를 사용하여 패키지 뷰 경로와 대상 퍼블리시 경로를 배열로 전달하세요:

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

이제 사용자들이 `vendor:publish` Artisan 명령어를 실행하면, 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트(View Components)

Blade 컴포넌트를 활용하거나 비표준 디렉터리에 컴포넌트를 둘 경우, 컴포넌트 클래스와 HTML 태그 alias를 수동으로 등록해야 Laravel이 컴포넌트를 찾을 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

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

등록한 후에는 alias로 아래와 같이 렌더할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로드

또는 `componentNamespace` 메서드를 사용하면 규칙에 따라 컴포넌트 클래스를 자동 로드할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스에 `Calendar`, `ColorPicker` 컴포넌트가 있다면 아래처럼 등록합니다:

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

이제 벤더 네임스페이스를 이용하여 아래와 같이 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 pascal-case로 변환하여 해당 클래스를 자동으로 찾습니다. "dot" 표기법을 사용하여 서브디렉터리도 지원합니다.

<a name="anonymous-components"></a>
#### 익명(Anonymous) 컴포넌트

패키지에 익명 컴포넌트가 있다면, 반드시 [loadViewsFrom 메서드](#views)로 지정한 뷰 디렉터리 하위의 `components` 디렉터리 안에 위치해야 합니다. 그런 다음, 컴포넌트 이름 앞에 패키지 뷰 네임스페이스를 붙여 렌더할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" Artisan 명령어

Laravel 내장 `about` Artisan 명령어는 애플리케이션의 환경 및 설정 요약 정보를 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 해당 명령어 출력에 정보를 추가할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 정보를 추가합니다:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어(Commands)

패키지의 Artisan 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용하세요. 이 메서드는 명령어 클래스명 배열을 인자로 받습니다. 명령어 등록이 끝나면 [Artisan CLI](/docs/{{version}}/artisan)에서 사용할 수 있습니다:

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
### 최적화 명령어(Optimize Commands)

Laravel의 [optimize 명령어](/docs/{{version}}/deployment#optimization)는 애플리케이션의 설정·이벤트·라우트·뷰를 캐시합니다. 패키지의 Artisan 명령어도 `optimizes` 메서드로 등록해, `optimize`와 `optimize:clear` 명령이 실행될 때 호출할 수 있습니다:

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
## 퍼블릭 자산(Public Assets)

패키지에 JavaScript, CSS, 이미지 등 자산이 있을 수 있습니다. 이러한 퍼블릭 자산을 애플리케이션의 `public` 디렉터리에 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 아래 예시에서는 관련 자산을 그룹으로 묶는 `public` 태그도 추가합니다:

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

사용자가 `vendor:publish` 명령을 실행하면 자산이 지정 위치로 복사됩니다. 패키지가 업데이트될 때마다 자산을 덮어써야 하므로, `--force` 플래그를 사용하세요:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱(Publishing File Groups)

패키지 자산과 리소스를 여러 그룹으로 나누어 별도로 퍼블리시하고 싶을 수 있습니다. 예를 들어 설정 파일만, 또는 마이그레이션 파일만 퍼블리시할 수 있도록 태그를 지정할 수 있습니다. `courier` 패키지의 경우, `boot` 메서드에서 `courier-config`와 `courier-migrations` 퍼블리시 그룹을 아래와 같이 정의할 수 있습니다:

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

이제 사용자는 퍼블리시 그룹 태그를 명시해 아래처럼 개별적으로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

또는 `--provider` 플래그로 서비스 프로바이더에 정의된 모든 퍼블리시 파일을 한 번에 퍼블리시할 수도 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
