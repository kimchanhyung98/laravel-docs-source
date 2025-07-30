# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 주의사항](#a-note-on-facades)
- [패키지 발견(디스커버리)](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - [“About” Artisan 명령어](#about-artisan-command)
- [명령어](#commands)
    - [최적화 명령어](#optimize-commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel에 기능을 추가하는 기본적인 방법입니다. 패키지는 날짜 작업에 유용한 [Carbon](https://github.com/briannesbitt/Carbon)이나 Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델과 파일을 연결할 수 있는 패키지 같은 다양한 형태가 있습니다.

패키지에는 여러 종류가 있습니다. 일부 패키지는 독립형으로, 즉 어떤 PHP 프레임워크에서도 동작합니다. Carbon과 Pest가 독립형 패키지의 예입니다. 이들 패키지는 `composer.json` 파일에 요구 사항으로 추가해 Laravel에서 사용할 수 있습니다.

반면, 다른 패키지들은 Laravel 전용으로 설계되어 라우트, 컨트롤러, 뷰, 설정 등이 Laravel 애플리케이션을 확장하기 위해 특화되어 있습니다. 이 가이드는 주로 Laravel 특정 패키지 개발에 중점을 둡니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 주의사항

Laravel 애플리케이션을 작성할 때 일반적으로 계약(contracts)이나 파사드(facades)를 사용해도 테스트 가능성에 큰 차이가 없습니다. 하지만 패키지를 작성할 때, Laravel의 모든 테스트 도구에 접근할 수 없는 경우가 많습니다. 만약 패키지 테스트를 Laravel 애플리케이션 안에서 설치된 것처럼 작성하길 원한다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 발견(디스커버리)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일은 Laravel이 로드할 서비스 프로바이더 목록을 포함합니다. 하지만 사용자가 직접 서비스 프로바이더를 목록에 추가하도록 요구하는 대신, 패키지의 `composer.json` 파일 내 `extra` 섹션에 프로바이더를 정의하면 Laravel이 자동으로 로드합니다. 서비스 프로바이더뿐 아니라 등록할 [파사드](/docs/master/facades)도 명시할 수 있습니다:

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

패키지가 자동 발견(discovery)으로 설정되면, 설치 시 Laravel이 서비스 프로바이더와 파사드를 자동으로 등록하므로 사용자에게 편리한 설치 환경을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 발견 비활성화

패키지 사용자가 특정 패키지에 대해 자동 발견을 비활성화하고 싶으면, 자신의 애플리케이션 `composer.json` 파일의 `extra` 섹션에 해당 패키지를 나열할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

모든 패키지 자동 발견을 끄려면 `dont-discover`에 `*`를 추가하세요:

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

[서비스 프로바이더](/docs/master/providers)는 패키지와 Laravel 간의 연결 고리입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/master/container)에 바인딩 작업을 수행하고, 뷰(view), 설정(configuration), 언어 파일(language file) 같은 패키지 리소스 경로를 Laravel에 알려줍니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며 `register`와 `boot` 두 가지 메서드를 포함합니다. 해당 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되며, 이 패키지를 자신의 패키지 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶으면 [공식 문서](/docs/master/providers)를 참고하세요.

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 설정

보통 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 퍼블리시(publish)해야 합니다. 이것은 패키지 사용자들이 기본 설정을 쉽게 덮어쓸 수 있도록 합니다. 설정 파일을 퍼블리시하려면, 서비스 프로바이더의 `boot` 메서드 내에서 `publishes` 메서드를 호출하세요:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` Artisan 명령어를 실행하면 파일이 지정된 위치로 복사됩니다. 퍼블리시된 구성 값은 다른 설정 파일과 똑같이 접근할 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 내에 클로저(익명 함수)를 정의해서는 안 됩니다. `config:cache` Artisan 명령어 실행 시 직렬화 문제가 발생합니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

또한 패키지 기본 설정 파일을 애플리케이션에 퍼블리시된 설정과 병합할 수 있습니다. 이렇게 하면 사용자들이 퍼블리시된 설정 파일에서 오직 덮어쓰고자 하는 옵션만 정의하면 됩니다. 설정 병합은 서비스 프로바이더의 `register` 메서드 내 `mergeConfigFrom` 메서드를 사용해 처리합니다.

`mergeConfigFrom`는 첫 번째 인자로 패키지 설정 파일 경로를, 두 번째 인자로 애플리케이션 설정 파일 이름을 받습니다:

```php
/**
 * 애플리케이션 서비스 등록.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> 이 메서드는 설정 배열의 최상위(첫 번째 레벨)만 병합합니다. 다차원 배열에서 일부만 정의할 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 사용해 로드할 수 있습니다. 이 메서드는 애플리케이션 라우트가 캐시되어 있는지 자동으로 확인하며, 캐시되어 있으면 라우트 파일을 다시 로드하지 않습니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/master/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용해 해당 파일 또는 디렉터리의 마이그레이션임을 알릴 수 있습니다. Laravel이 마이그레이션을 퍼블리시할 때 파일명 내 타임스탬프가 현재 시각을 반영하여 자동으로 갱신됩니다:

```php
/**
 * 패키지 서비스 부트스트랩.
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

패키지에 [언어 파일](/docs/master/localization)이 있다면, `loadTranslationsFrom` 메서드를 사용해 Laravel에 로드 방식을 알려줄 수 있습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음과 같이 추가합니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 구문은 `package::file.line` 형식으로 참조합니다. 예를 들어 `courier` 패키지의 `messages` 파일 안 `welcome` 문구는 아래처럼 불러올 수 있습니다:

```php
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일을 등록하려면, `loadJsonTranslationsFrom` 메서드를 사용하세요. 이 메서드는 JSON 번역 파일들이 들어 있는 디렉터리 경로를 받습니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더 내 `publishes` 메서드를 사용하세요. `publishes` 메서드는 패키지 원본 경로와 퍼블리시 위치 배열을 받습니다. 예를 들어 `courier` 패키지 언어 파일을 퍼블리시하려면 다음과 같이 작성합니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

이제 사용자가 `vendor:publish` Artisan 명령어를 실행 시 언어 파일이 지정된 위치로 퍼블리시됩니다.

<a name="views"></a>
### 뷰

패키지의 [뷰](/docs/master/views)를 Laravel에 등록하려면, Laravel에 뷰 위치를 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하면 됩니다. 이 메서드는 첫 번째 인자로 뷰 템플릿 경로, 두 번째 인자로 패키지 이름을 받습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더 `boot` 메서드에 아래와 같이 작성합니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 구문으로 참조합니다. 예를 들어 `courier` 패키지의 `dashboard` 뷰는 다음과 같이 불러올 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이딩

`loadViewsFrom` 메서드를 사용하면 Laravel은 실제로 두 곳을 검색합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 지정한 패키지 뷰 디렉터리입니다. 예를 들어 `courier` 패키지의 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 폴더에 커스터마이즈한 뷰가 있는지 확인합니다. 해당 뷰가 없으면 패키지 뷰 경로에서 검색합니다. 이렇게 해서 사용자들은 손쉽게 패키지 뷰를 커스터마이즈하거나 덮어쓸 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

뷰를 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시할 수 있게 하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. `publishes` 메서드는 패키지 뷰 경로와 퍼블리시 위치를 배열로 받습니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 사용자가 `vendor:publish` 명령어를 실행하면 뷰 파일이 지정한 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하는 패키지를 만들거나 비표준 디렉터리에 컴포넌트를 둔 경우, 컴포넌트 클래스와 HTML 태그 별칭(alias)을 명시적으로 등록해야 Laravel이 컴포넌트를 인식합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록한 컴포넌트는 다음과 같이 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는 `componentNamespace` 메서드를 사용해 특정 네임스페이스 내 컴포넌트를 자동 로딩할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 있을 경우:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 `package-name::` 구문으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 Pascal 케이스로 변환하여 해당 클래스를 자동으로 찾습니다. 서브디렉터리는 점(.) 표기법도 지원합니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

익명 컴포넌트가 있다면, 반드시 패키지의 "views" 디렉터리 내 `components` 폴더에 위치해야 합니다(`loadViewsFrom` 메서드로 등록된 경로 기준). 익명 컴포넌트는 다음과 같이 패키지 뷰 네임스페이스 접두어를 붙여 렌더링합니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### “About” Artisan 명령어

Laravel 내장 `about` Artisan 명령어는 애플리케이션 환경과 설정 상태를 요약해 보여줍니다. 패키지는 `AboutCommand` 클래스를 통해 추가 정보를 이 출력에 덧붙일 수 있습니다. 보통 패키지 서비스 프로바이더 `boot` 메서드 내에서 정보를 추가합니다:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어

패키지의 Artisan 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용합니다. 이 메서드는 명령어 클래스 이름 배열을 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/master/artisan)를 통해 실행할 수 있습니다:

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * 패키지 서비스 부트스트랩.
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

Laravel의 [`optimize` 명령어](/docs/master/deployment#optimization)는 애플리케이션 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 사용하면, `optimize` 및 `optimize:clear` 명령어 실행 시 호출되어야 할 패키지 자체 Artisan 명령어를 등록할 수 있습니다:

```php
/**
 * 패키지 서비스 부트스트랩.
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

패키지는 JavaScript, CSS, 이미지 같은 에셋을 포함할 수 있습니다. 이 에셋을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 예제에서는 관련된 에셋들을 그룹화하는 `public` 태그도 추가합니다:

```php
/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

패키지 사용자가 `vendor:publish` 명령어를 실행할 때, 에셋은 지정된 위치로 복사됩니다. 패키지가 업데이트될 때마다 에셋을 덮어써야 할 경우가 많으므로 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱

패키지 자산과 리소스를 별개로 그룹화해 퍼블리시하도록 할 수 있습니다. 예를 들어, 패키지 설정 파일은 퍼블리시하되, 에셋은 선택적으로 퍼블리시하게끔 구분할 수 있습니다. 이를 위해 서비스 프로바이더에서 `publishes` 호출 시 태그(tag)를 지정할 수 있습니다. 예를 들어 `courier` 패키지에서 `courier-config`와 `courier-migrations` 두 개의 태그로 퍼블리시 그룹을 만드는 방법:

```php
/**
 * 패키지 서비스 부트스트랩.
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

사용자는 `vendor:publish` 명령어에 태그를 지정하여 해당 그룹만 별도로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```