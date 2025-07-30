# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 주의점](#a-note-on-facades)
- [패키지 발견](#package-discovery)
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
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 기본적인 방법입니다. 패키지는 예를 들어 날짜 작업에 유용한 [Carbon](https://github.com/briannesbitt/Carbon)이나 Eloquent 모델에 파일을 연결할 수 있게 해주는 Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 다양합니다.

패키지에는 여러 종류가 있습니다. 일부 패키지는 독립형으로, 어떤 PHP 프레임워크와도 함께 동작합니다. Carbon이나 Pest가 독립형 패키지의 예입니다. 이들 패키지는 모두 `composer.json` 파일에 의존성으로 추가하여 Laravel과 함께 사용할 수 있습니다.

반면에, 다른 패키지들은 Laravel 전용으로 설계되어, 라우트, 컨트롤러, 뷰, 설정을 포함해 Laravel 애플리케이션을 강화하기 위해 만들어집니다. 이 가이드에서는 주로 Laravel 전용 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 주의점 (A Note on Facades)

Laravel 애플리케이션을 작성할 때는 계약(contracts)이나 파사드(facades)를 사용해도 대체로 테스트 가능성에 큰 차이가 없습니다. 하지만 패키지를 작성할 때는, 패키지 자체가 Laravel의 모든 테스트 도구에 접근할 수 없는 경우가 많습니다. 만약 패키지를 일반 Laravel 애플리케이션 안에 설치된 것처럼 테스트하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 발견 (Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 로드되어야 할 서비스 프로바이더 리스트가 포함되어 있습니다. 하지만 사용자가 직접 서비스 프로바이더를 추가하도록 요구하는 대신, 패키지의 `composer.json` 파일 `extra` 섹션에 서비스 프로바이더를 정의할 수 있어 Laravel이 자동으로 로드할 수 있습니다. 서비스 프로바이더 외에도 등록할 파사드도 나열할 수 있습니다:

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

패키지가 패키지 발견으로 구성되면, 해당 패키지를 설치할 때 Laravel이 서비스 프로바이더와 파사드를 자동으로 등록하여 사용자가 더 편리하게 설치할 수 있습니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 발견 사용 안 함 설정

만약 패키지 소비자 입장에서 특정 패키지에 대해 패키지 발견을 비활성화하고 싶다면, 애플리케이션 `composer.json` 파일의 `extra` 섹션에 패키지 이름을 다음과 같이 나열할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

애플리케이션 내 모든 패키지에 대해 패키지 발견을 비활성화하려면, `dont-discover` 지시어에 `*` 문자를 사용할 수 있습니다:

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

[서비스 프로바이더](/docs/11.x/providers)는 패키지와 Laravel 사이 연결 고리 역할을 합니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/11.x/container)에 바인딩을 담당하며, 뷰, 설정, 언어 파일 같은 패키지 리소스를 어디서 불러올지 Laravel에 알려줍니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장하며 `register` 와 `boot` 두 개의 메서드를 포함합니다. 이 `ServiceProvider` 기본 클래스는 `illuminate/support` Composer 패키지에 위치하므로, 패키지 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 역할에 대해 더 자세히 알고 싶다면 [관련 문서](/docs/11.x/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

보통 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 퍼블리시해야 합니다. 이렇게 하면 패키지 사용자들이 기본 설정을 손쉽게 덮어쓸 수 있습니다. 서비스를 제공하는 프로바이더의 `boot` 메서드 안에서 `publishes` 메서드를 호출하여 설정 파일을 퍼블리시할 수 있게 만드세요:

```
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

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정한 위치로 복사됩니다. 설정이 퍼블리시 된 후에는 다른 설정 파일처럼 다음과 같이 값을 읽을 수 있습니다:

```
$value = config('courier.option');
```

> [!WARNING]  
> 설정 파일 내부에 클로저(익명 함수)를 정의해서는 안 됩니다. `config:cache` Artisan 명령어 실행 시 제대로 직렬화되지 않기 때문입니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 (Default Package Configuration)

사용자가 퍼블리시한 설정 파일에서 필요한 항목만 오버라이드하도록 하려면, 애플리케이션의 설정 파일과 패키지의 설정 파일을 병합하는 것이 좋습니다. 이 작업은 서비스 프로바이더의 `register` 메서드 안에서 `mergeConfigFrom` 메서드를 사용해 처리합니다.

`mergeConfigFrom` 메서드는 첫 번째 인자로 패키지 설정 파일 경로를, 두 번째 인자로는 애플리케이션 내 설정 파일 이름을 받습니다:

```
/**
 * 애플리케이션 서비스 등록
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]  
> 이 메서드는 설정 배열의 첫 번째 레벨만 병합합니다. 만약 사용자가 다차원 설정 배열 일부만 정의하면, 정의하지 않은 항목은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 사용해 라우트를 불러올 수 있습니다. 이 메서드는 애플리케이션의 라우트 캐시 상태를 자동으로 감지하여, 이미 캐시되어 있다면 라우트 파일을 다시 로드하지 않습니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/11.x/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용하여 해당 디렉터리 또는 파일이 마이그레이션임을 Laravel에 알릴 수 있습니다. Laravel은 마이그레이션을 퍼블리시할 때 파일명 내 타임스탬프를 현재 날짜와 시간으로 자동 변경합니다:

```
/**
 * 패키지 서비스 부트스트랩
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

패키지에 [언어 파일들](/docs/11.x/localization)이 있다면, `loadTranslationsFrom` 메서드를 사용해 Laravel에 로드 방법을 알려줍니다. 예를 들어 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 다음을 추가합니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 문구는 `package::file.line` 구문으로 참조할 수 있습니다. 예를 들어 `courier` 패키지의 `messages` 파일에 있는 `welcome` 번역문을 로드할 때는 다음과 같이 작성합니다:

```
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일을 등록하려면 `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 JSON 번역 파일이 위치한 디렉터리 경로를 인자로 받습니다:

```php
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션 `lang/vendor` 디렉터리에 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 패키지 경로들과 퍼블리시 위치를 담은 배열을 받습니다. `courier` 패키지의 언어 파일을 퍼블리시할 때 예시는 다음과 같습니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` Artisan 명령어를 실행하면, 언어 파일이 지정된 경로로 복사됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/11.x/views)를 Laravel에 등록하려면, 뷰 파일 경로를 Laravel에 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하면 됩니다. 이 메서드는 두 개의 인자를 받는데, 첫 번째는 뷰 템플릿 경로, 두 번째는 패키지 이름입니다. 예를 들어 패키지 이름이 `courier`라면 다음과 같이 작성합니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 구문으로 참조합니다. 예를 들어 이미 서비스 프로바이더에서 뷰 경로를 등록한 후에는 `courier` 패키지의 `dashboard` 뷰를 다음처럼 로드할 수 있습니다:

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용할 때, Laravel은 실제로 두 군데 뷰 경로를 등록합니다: 애플리케이션 내 `resources/views/vendor` 디렉터리와, 패키지 쪽 뷰 디렉터리입니다. 예를 들어 `courier` 패키지를 사용할 때 Laravel은 먼저 개발자가 `resources/views/vendor/courier` 디렉터리에 올린 커스텀 뷰가 있는지 확인하고, 없으면 패키지의 뷰 디렉터리를 살펴봅니다. 이 시스템 덕분에 패키지 사용자는 손쉽게 패키지 뷰를 커스터마이징하거나 덮어쓸 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰를 애플리케이션 내에서 퍼블리시 가능하도록 만들려면, 서비스 프로바이더의 `publishes` 메서드를 사용합니다. `publishes` 메서드는 패키지 뷰 경로와 원하는 배포 경로를 배열 형태로 받습니다. 예시는 다음과 같습니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` Artisan 명령어를 실행하면 뷰가 지정한 경로로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

패키지에서 Blade 컴포넌트를 사용하거나 비표준 위치에 컴포넌트를 두는 경우, Laravel이 해당 컴포넌트 클래스를 찾을 수 있도록 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드 안에서 컴포넌트를 등록합니다:

```
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

컴포넌트를 등록하면, 해당 태그 별칭을 사용해 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

대신 `componentNamespace` 메서드를 사용해 네임스페이스 단위로 컴포넌트를 자동 로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지가 `Nightshade\Views\Components` 네임스페이스에 `Calendar`와 `ColorPicker` 컴포넌트를 두고 있다면 다음과 같이 등록합니다:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

그러면 다음과 같이 공급자 네임스페이스를 접두사로 사용해 컴포넌트를 호출할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 연결된 클래스도 자동으로 찾습니다. 하위 디렉터리는 점(`.`) 표기법을 사용해 지원됩니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지에 익명 컴포넌트가 있다면, 반드시 패키지의 뷰 디렉터리 내 `components` 하위 디렉터리에 위치시켜야 합니다(이는 [`loadViewsFrom` 메서드](#views)에서 지정된 경로 기준입니다). 이후 컴포넌트는 패키지의 뷰 네임스페이스를 접두사로 붙여 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" Artisan 명령어

Laravel 내장 `about` Artisan 명령어는 애플리케이션 환경 및 설정 정보를 요약해 보여줍니다. 패키지는 이 명령어 출력에 추가 정보를 포함시킬 수 있는데, `AboutCommand` 클래스를 사용하면 됩니다. 보통 이 정보는 패키지 서비스 프로바이더 `boot` 메서드에서 추가합니다:

```
use Illuminate\Foundation\Console\AboutCommand;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어 (Commands)

패키지의 Artisan 명령어를 Laravel에 등록하려면 `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스 이름들의 배열을 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/11.x/artisan)를 통해 실행할 수 있습니다:

```
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * 패키지 서비스 부트스트랩
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

Laravel의 [`optimize` 명령어](/docs/11.x/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 통해, `optimize`와 `optimize:clear` 명령어 실행 시 호출할 패키지 고유의 Artisan 명령어를 등록할 수 있습니다:

```
/**
 * 패키지 서비스 부트스트랩
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
## 퍼블릭 에셋 (Public Assets)

패키지에 JavaScript, CSS, 이미지 같은 에셋이 포함되어 있을 수 있습니다. 이 에셋을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 예시에서는 `public` 에셋 그룹 태그도 추가하여 관련 에셋 묶음을 쉽게 퍼블리시할 수 있도록 했습니다:

```
/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 에셋이 지정한 위치로 복사됩니다. 패키지 업데이트시 에셋을 덮어써야 하므로 보통 `--force` 옵션을 함께 사용합니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지 에셋과 리소스들을 그룹별로 따로 퍼블리시 하도록 할 수도 있습니다. 예를 들어 사용자가 패키지 구성 파일만 퍼블리시하고 에셋은 퍼블리시하지 않도록 허용할 수 있습니다. 이때 서비스 프로바이더에서 `publishes` 메서드를 호출할 때 태그를 지정하면 됩니다. 다음은 `courier` 패키지의 `courier-config` 와 `courier-migrations` 두 퍼블리시 그룹 태그를 지정한 예시입니다:

```
/**
 * 패키지 서비스 부트스트랩
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

이제 사용자는 `vendor:publish` 명령어를 실행할 때 태그를 지정해 그룹별로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```