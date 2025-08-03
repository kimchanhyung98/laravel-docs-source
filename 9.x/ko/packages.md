# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 주의사항](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [마이그레이션](#migrations)
    - [라우트](#routes)
    - [번역](#translations)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - [“About” Artisan 명령어](#about-artisan-command)
- [명령어](#commands)
- [공용 자산](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 날짜 작업을 위한 훌륭한 도구인 [Carbon](https://github.com/briannesbitt/Carbon)이나, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연결할 수 있게 해 주는 패키지까지 다양한 형태가 있습니다.

패키지에는 여러 유형이 있습니다. 일부 패키지는 독립형으로, PHP 프레임워크 어디서나 작동합니다. Carbon과 PHPUnit가 이에 해당합니다. 이런 패키지는 모두 Laravel에서 `composer.json` 파일에 포함시켜 사용할 수 있습니다.

반면, 일부 패키지는 Laravel 전용으로 설계되어 라우트, 컨트롤러, 뷰, 설정 등 Laravel 애플리케이션을 확장하기 위한 기능을 포함합니다. 이 가이드는 주로 Laravel 전용 패키지 개발에 중점을 둡니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 주의사항 (A Note On Facades)

Laravel 애플리케이션을 작성할 때는 계약(contracts)이나 파사드(facades)를 사용하는 것이 테스트 가능성 측면에서 거의 차이가 없습니다. 그러나 패키지를 작성할 경우, 보통 Laravel의 모든 테스트 도구에 접근할 수 없습니다. 만약 패키지가 일반적인 Laravel 애플리케이션에 설치된 것처럼 테스트를 작성하고 싶다면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리 (Package Discovery)

Laravel 애플리케이션의 `config/app.php` 설정 파일에서 `providers` 옵션은 Laravel이 로드할 서비스 프로바이더 목록을 정의합니다. 사용자가 패키지를 설치할 때, 보통 귀하의 서비스 프로바이더를 이 목록에 포함시키고자 합니다. 사용자가 직접 목록에 추가하게 하는 대신, 귀하의 패키지 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의할 수 있습니다. 서비스 프로바이더뿐 아니라 등록하고자 하는 [파사드](/docs/9.x/facades)도 같이 나열할 수 있습니다:

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

패키지가 디스커버리 설정되면, 패키지가 설치될 때 Laravel이 자동으로 서비스 프로바이더와 파사드를 등록해 주어, 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
### 패키지 디스커버리 비활성화하기 (Opting Out Of Package Discovery)

패키지 사용자로서 특정 패키지에 대해 디스커버리를 비활성화하고 싶을 경우, 애플리케이션 `composer.json` 파일의 `extra` 섹션에 해당 패키지 이름을 나열하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

또는 모든 패키지에 대해 디스커버리를 일괄 비활성화하려면, `dont-discover` 지시문에 `*` 문자를 사용할 수 있습니다:

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

[서비스 프로바이더](/docs/9.x/providers)는 Laravel과 패키지를 연결하는 접점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/9.x/container)에 객체를 바인딩하고 뷰, 설정, 로컬라이제이션 파일 등 패키지 리소스를 Laravel에 알려주는 역할을 합니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register`와 `boot` 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 위치하므로, 패키지 의존성에 이 패키지를 추가해야 합니다. 서비스 프로바이더의 구조와 역할에 대해 더 알고 싶으면 [공식 문서](/docs/9.x/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

대부분의 경우, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 퍼블리싱해야 합니다. 이렇게 하면 패키지 사용자가 기본 설정을 쉽게 덮어쓸 수 있습니다. 설정 파일을 퍼블리싱 가능하게 만들려면 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 사용자가 Laravel의 `vendor:publish` 명령어를 실행할 때 해당 파일이 위에서 지정한 위치로 복사됩니다. 퍼블리싱된 설정 파일은 다른 설정 파일과 동일하게 접근할 수 있습니다:

```
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 내에서 클로저(익명 함수)를 정의하면 안 됩니다. `config:cache` Artisan 명령어 실행 시 직렬화가 불가능하기 때문입니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정 (Default Package Configuration)

패키지 설정 파일과 애플리케이션에 퍼블리시된 설정 파일을 병합할 수도 있습니다. 이렇게 하면 사용자는 퍼블리시된 설정에서 원하는 옵션만 덮어쓸 수 있습니다. 설정 병합은 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용해 진행하세요.

`mergeConfigFrom` 메서드는 첫 번째 인자로 패키지 설정 파일 경로를, 두 번째 인자로 애플리케이션 설정명(파일명에서 `.php` 제외)을 받습니다:

```
/**
 * 애플리케이션 서비스 등록.
 *
 * @return void
 */
public function register()
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> 이 메서드는 설정 배열의 첫 번째 깊이의 값만 병합합니다. 다차원 배열에서 일부만 정의하면, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에서 라우트를 포함하고 있다면 `loadRoutesFrom` 메서드를 이용해 로드할 수 있습니다. 이 메서드는 애플리케이션 라우트가 캐시되었는지 자동으로 확인하며, 캐시된 경우 라우트 파일을 로드하지 않습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/9.x/migrations)이 포함된 경우, `loadMigrationsFrom` 메서드를 사용해 Laravel에 로드를 알릴 수 있습니다. 이 메서드는 마이그레이션 경로 하나만 인자로 받습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
}
```

패키지 마이그레이션이 등록되면, `php artisan migrate` 명령어 실행 시 자동으로 마이그레이션이 수행됩니다. 별도로 애플리케이션 `database/migrations` 디렉터리로 마이그레이션 파일을 복사할 필요가 없습니다.

<a name="translations"></a>
### 번역 (Translations)

패키지에 [번역 파일](/docs/9.x/localization)이 포함된 경우, `loadTranslationsFrom` 메서드를 사용해 Laravel에 번역 파일 로드를 알릴 수 있습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더 `boot` 메서드에 다음과 같이 추가하세요:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역은 `package::file.line` 형태로 참조합니다. 예를 들어 `courier` 패키지의 `messages` 파일 내 `welcome` 문장을 다음과 같이 불러올 수 있습니다:

```
echo trans('courier::messages.welcome');
```

<a name="publishing-translations"></a>
#### 번역 파일 퍼블리싱 (Publishing Translations)

패키지 번역 파일을 애플리케이션 `lang/vendor` 디렉터리로 퍼블리싱하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. 이 메서드는 패키지 경로와 원하는 퍼블리시 위치를 배열로 받습니다. 예를 들면 `courier` 패키지의 번역 파일을 퍼블리시하는 코드는 다음과 같습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

사용자가 `vendor:publish` Artisan 명령어를 실행하면, 패키지 번역이 지정된 위치로 복사됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰 파일](/docs/9.x/views)을 Laravel에 등록하려면, 뷰가 위치한 경로를 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하며, 이 메서드는 뷰 경로와 패키지 이름 두 인자를 받습니다. 예를 들어 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음과 같이 추가하세요:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 문법으로 참조합니다. 한번 경로를 등록하면, `courier` 패키지의 `dashboard` 뷰는 다음과 같이 사용할 수 있습니다:

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드 (Overriding Package Views)

`loadViewsFrom` 메서드를 사용할 때, Laravel은 실제로 애플리케이션 `resources/views/vendor` 디렉터리와 패키지 지정 디렉터리 두 곳을 뷰 경로로 등록합니다. `courier` 패키지 예시로, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 경로에 뷰를 맞춤화했는지 확인합니다. 맞춤 설정된 뷰가 없으면 패키지 내 지정한 뷰 경로를 검색합니다. 따라서 패키지 사용자들은 쉽게 뷰를 커스터마이즈하거나 덮어쓸 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱 (Publishing Views)

패키지 뷰 파일을 사용자 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시하게 만들고 싶으면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 메서드는 패키지 뷰 경로와 퍼블리시할 경로를 배열로 받습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 사용자가 `vendor:publish` 명령어를 실행하면 패키지 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

패키지가 Blade 컴포넌트를 사용하거나 비표준 디렉터리에 컴포넌트를 둔 경우, 컴포넌트 클래스와 HTML 태그 별칭을 Laravel에 수동으로 등록해야 합니다. 보통 컴포넌트 등록은 패키지 서비스 프로바이더의 `boot` 메서드에서 이뤄집니다:

```
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Blade::component('package-alert', AlertComponent::class);
}
```

컴포넌트가 등록되면, 다음과 같이 태그 별칭을 사용해 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로드 (Autoloading Package Components)

대안으로 `componentNamespace` 메서드를 사용해 네임스페이스 컨벤션으로 컴포넌트를 자동 로드할 수 있습니다. 예를 들어 `Nightshade` 패키지가 `Nightshade\Views\Components` 네임스페이스에 `Calendar`, `ColorPicker` 컴포넌트를 가진다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면, 패키지 컴포넌트를 다음과 같이 벤더 네임스페이스 접두어와 함께 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 해당 컴포넌트 이름을 PascalCase 클래스명으로 연결해 자동으로 컴포넌트를 찾아줍니다. 하위 디렉터리 또한 "dot" 표기법으로 지원합니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트 (Anonymous Components)

패키지에 익명 컴포넌트가 있을 경우, 반드시 패키지 뷰 디렉터리 내 `components` 폴더에 위치해야 합니다 (`loadViewsFrom` 메서드에 의해 지정된 위치). 이후에는 패키지 뷰 네임스페이스를 접두사로 사용해 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### “About” Artisan 명령어 (About Artisan Command)

Laravel 내장 `about` Artisan 명령어는 애플리케이션 환경과 설정 요약을 보여줍니다. 패키지는 `AboutCommand` 클래스를 사용해 추가 정보를 이 명령어 출력에 제공할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 다음과 같이 추가합니다:

```
use Illuminate\Foundation\Console\AboutCommand;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어 (Commands)

패키지의 Artisan 명령어를 Laravel에 등록하려면 `commands` 메서드를 사용하세요. 이 메서드는 명령어 클래스명을 배열로 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/9.x/artisan)에서 실행할 수 있습니다:

```
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
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
## 공용 자산 (Public Assets)

패키지에는 JavaScript, CSS, 이미지 같은 자산이 포함될 수 있습니다. 이러한 자산을 애플리케이션 `public` 디렉터리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 예에서는 `public` 자산 그룹 태그도 추가해 관련 자산들을 쉽게 퍼블리시할 수 있게 했습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면 자산이 지정된 위치로 복사됩니다. 패키지 업데이트 때마다 자산을 덮어써야 할 경우가 많으므로 `--force` 옵션을 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지 자산 및 리소스를 별도 그룹으로 나누어 퍼블리시하게 할 수 있습니다. 예를 들어 사용자가 자산을 퍼블리시하지 않고 설정 파일만 퍼블리시하도록 허용할 수 있습니다. 이는 서비스 프로바이더의 `publishes` 메서드에서 태그를 지정해 수행합니다. 예를 들어, `courier` 패키지에서는 다음과 같이 `courier-config`와 `courier-migrations` 두 태그를 `boot` 메서드에 정의할 수 있습니다:

```
/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishes([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

이제 사용자들은 `vendor:publish` 명령어를 실행할 때 태그를 지정해 각 그룹을 별도로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```