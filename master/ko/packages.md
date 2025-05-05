# 패키지 개발

- [소개](#introduction)
    - [파사드에 대한 안내](#a-note-on-facades)
- [패키지 자동 등록](#package-discovery)
- [서비스 제공자](#service-providers)
- [리소스](#resources)
    - [설정 파일](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" 아티즌 명령어](#about-artisan-command)
- [아티즌 명령어](#commands)
    - [최적화 명령어](#optimize-commands)
- [공개 자산](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 기본적인 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)과 같이 날짜를 다루는 좋은 방법부터, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연관시킬 수 있는 패키지까지 다양합니다.

패키지에는 여러 가지 유형이 있습니다. 몇몇 패키지는 독립형으로, 어떤 PHP 프레임워크와도 함께 동작합니다. Carbon과 Pest가 이러한 독립형 패키지에 속합니다. 이러한 패키지들을 Laravel에서 사용하려면 `composer.json` 파일에 추가하면 됩니다.

반면, 다른 패키지는 Laravel과 함께 사용하도록 특별히 설계되었습니다. 이러한 패키지는 라우트, 컨트롤러, 뷰, 설정 등을 제공하여 Laravel 애플리케이션을 확장합니다. 이 가이드는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 안내

Laravel 애플리케이션을 작성할 때는 계약(contracts)이나 파사드(facades) 중 어느 것을 사용하든 테스트 가능성의 수준이 거의 동일하므로 큰 차이가 없습니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼에 접근할 수 없을 때가 많습니다. 만약 일반적인 Laravel 애플리케이션 환경에서처럼 패키지 테스트 코드를 작성하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 등록(Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 Laravel이 로드해야 하는 서비스 제공자 목록이 있습니다. 그러나 사용자가 직접 서비스 제공자를 목록에 추가하지 않아도, 패키지의 `composer.json` 파일의 `extra` 섹션에 등록하면 Laravel에서 자동으로 불러옵니다. 서비스 제공자뿐 아니라, 등록하고 싶은 [파사드](/docs/{{version}}/facades)도 함께 명시할 수 있습니다.

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

패키지가 자동 등록을 지원하도록 구성되면, 사용자가 설치할 때 Laravel은 서비스 제공자와 파사드를 자동으로 등록하여 손쉬운 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 자동 등록 비활성화

패키지를 사용하는 입장에서 특정 패키지의 자동 등록을 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 패키지 이름을 추가하면 됩니다.

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

`dont-discover` 지시문 안에 `*`를 넣으면 모든 패키지의 자동 등록을 비활성화할 수 있습니다.

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
## 서비스 제공자

[서비스 제공자](/docs/{{version}}/providers)는 패키지와 Laravel을 연결하는 지점입니다. 서비스 제공자는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 필요한 기능을 바인드하고, 패키지의 리소스(뷰, 설정, 언어 파일 등)가 어디에 위치하는지 Laravel에 알립니다.

서비스 제공자는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으므로 패키지의 의존성에 추가해야 합니다. 서비스 제공자의 구조와 목적에 대한 자세한 내용은 [공식 문서](/docs/{{version}}/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정 파일

보통 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 퍼블리시해야 합니다. 이렇게 하면 패키지 사용자는 기본 설정값을 쉽게 덮어쓸 수 있습니다. 설정 파일을 퍼블리시하려면 서비스 제공자의 `boot` 메서드에서 `publishes` 메서드를 호출하세요.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 지정한 위치로 파일이 복사됩니다. 퍼블리시된 설정 파일의 값은 다른 설정 파일과 동일하게 사용할 수 있습니다.

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일에서는 클로저(closure)를 정의하지 않아야 합니다. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 병합

패키지 설정 파일을 애플리케이션에 퍼블리시한 설정 파일과 병합할 수도 있습니다. 이렇게 하면 사용자는 덮어쓰고 싶은 옵션만 퍼블리시된 설정 파일에 정의할 수 있습니다. 설정값을 병합하려면 서비스 제공자의 `register` 메서드 내에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드는 첫 번째 인자로 패키지 설정 파일 경로를, 두 번째 인자로 애플리케이션 설정 파일 이름을 받습니다.

```php
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
> 이 방식은 설정 배열의 1차원만 병합합니다. 사용자가 다차원 배열에서 일부만 정의하면 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드로 불러올 수 있습니다. 이 메서드는 애플리케이션의 라우트 캐시 여부를 자동으로 감지하여, 이미 캐시된 경우에는 파일을 불러오지 않습니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있다면, `publishesMigrations` 메서드로 마이그레이션 디렉터리 또는 파일을 지정할 수 있습니다. 퍼블리시 시점에 파일 이름의 타임스탬프가 현재 날짜와 시간으로 자동 변경됩니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
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

패키지에 [언어 파일](/docs/{{version}}/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드로 Laravel에 로딩 경로를 알려줄 수 있습니다. 예를 들어, 패키지가 `courier`라면 서비스 제공자의 `boot` 메서드에 아래와 같이 추가합니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 구문은 `패키지::파일.키` 방식의 규칙으로 참조합니다. 예를 들어, `courier` 패키지의 `messages` 파일 내 `welcome` 구문을 불러오려면 아래처럼 작성합니다.

```php
echo trans('courier::messages.welcome');
```

JSON 번역 파일을 사용하는 경우, `loadJsonTranslationsFrom` 메서드에 패키지의 JSON 번역 파일 폴더 경로를 지정하면 됩니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리싱하고 싶다면, 서비스 제공자의 `publishes` 메서드를 이용하세요. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리싱하는 경우는 다음과 같습니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정된 위치로 복사됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/{{version}}/views)를 Laravel에 등록하려면 뷰 위치를 알려주어야 합니다. 서비스 제공자의 `loadViewsFrom` 메서드를 이용하면 됩니다. 이 메서드는 뷰 템플릿 경로와 패키지 이름, 두 개의 인자를 받습니다. 예를 들어, 패키지 이름이 `courier`라면 다음과 같이 등록합니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지의 뷰는 `패키지::뷰` 규칙으로 참조합니다. 예를 들어 `courier` 패키지의 `dashboard` 뷰를 불러오려면 다음과 같이 하면 됩니다.

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용할 때, Laravel은 실제로 두 곳의 뷰 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 패키지에서 지정한 경로입니다. `courier` 패키지를 예로 들면, Laravel은 우선 개발자가 `resources/views/vendor/courier` 디렉터리에 커스텀 뷰를 넣어뒀는지 확인하고, 없으면 패키지의 뷰 디렉터리를 사용합니다. 이를 통해 패키지 사용자는 뷰를 손쉽게 커스터마이징/오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시하려면 서비스 제공자의 `publishes` 메서드를 이용하면 됩니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` 아티즌 명령어를 실행하면 지정한 위치로 뷰가 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하는 패키지를 개발하거나 비표준 디렉터리에 컴포넌트를 둘 경우, 컴포넌트 클래스와 HTML 태그 별칭을 수동 등록해야 합니다. 일반적으로 패키지의 서비스 제공자 `boot` 메서드에서 이를 등록합니다.

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록이 완료되면, HTML 태그 별칭을 이용해 컴포넌트를 사용할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는 `componentNamespace` 메서드로 네임스페이스 기준 자동 로딩을 구성할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 있다면:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이제 `package-name::` 구문을 사용하여 컴포넌트를 불러올 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 연결된 클래스를 자동으로 감지합니다. 서브디렉터리는 "dot" 표기법으로 지정할 수 있습니다.

<a name="anonymous-components"></a>
#### 익명(Anonymous) 컴포넌트

패키지에 익명 컴포넌트가 있을 경우, 반드시 패키지의 "views" 디렉터리 아래 `components` 폴더에 위치해야 합니다(`loadViewsFrom` 메서드에 지정한 디렉터리 기준). 이후 패키지 뷰 네임스페이스를 접두어로 붙여서 사용할 수 있습니다.

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어

Laravel이 내장한 `about` 아티즌 명령어는 애플리케이션의 환경 및 설정 정보를 요약해 보여줍니다. 패키지는 `AboutCommand` 클래스를 통해 추가적인 정보를 이 명령어 출력에 더할 수 있습니다. 보통 서비스 제공자의 `boot` 메서드에서 다음과 같이 추가합니다.

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * 애플리케이션 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 아티즌 명령어

패키지의 아티즌 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용할 수 있습니다. 이 메서드는 커맨드 클래스명 배열을 인자로 받습니다. 등록된 후에는 [Artisan CLI](/docs/{{version}}/artisan)에서 실행할 수 있습니다.

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * 패키지 서비스를 부트스트랩 합니다.
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

Laravel의 [`optimize` 명령어](/docs/{{version}}/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. 패키지 자체의 아티즌 명령어도 `optimize` 및 `optimize:clear` 명령어가 실행될 때 호출될 수 있도록 하려면 `optimizes` 메서드를 사용하세요.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
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
## 공개 자산(Public Assets)

패키지에 JavaScript, CSS, 이미지와 같은 자산 파일이 있는 경우, 서비스 제공자의 `publishes` 메서드를 사용하여 애플리케이션의 `public` 디렉터리로 퍼블리시하도록 할 수 있습니다. 아래 예시에서는 `public` 자산 그룹 태그도 추가하여 관련 자산을 그룹별로 쉽게 관리할 수 있도록 하였습니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 자산 파일이 지정 위치로 복사됩니다. 일반적으로 패키지 업데이트 시마다 자산 파일을 덮어써야 하므로 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

패키지의 자산이나 리소스를 그룹별로 따로 퍼블리시하고 싶은 경우, `publishes` 메서드 호출 시 태그를 지정해서 각기 다른 그룹으로 만들 수 있습니다. 예를 들어, `courier` 패키지에서 설정 파일(`courier-config`)과 마이그레이션(`courier-migrations`)을 그룹으로 나누어 태그화 하는 예시는 다음과 같습니다.

```php
/**
 * 패키지 서비스를 부트스트랩 합니다.
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

패키지 사용자는 이제 `vendor:publish` 명령어에 태그를 지정하여 해당 그룹만 선택적으로 퍼블리시할 수 있습니다.

```shell
php artisan vendor:publish --tag=courier-config
```