# 업그레이드 가이드

- [7.x에서 8.0으로 업그레이드](#upgrade-8.0)

<a name="high-impact-changes"></a>
## 영향이 큰 변경사항

<div class="content-list" markdown="1">

- [모델 팩토리](#model-factories)
- [큐 `retryAfter` 메서드](#queue-retry-after-method)
- [큐 `timeoutAt` 프로퍼티](#queue-timeout-at-property)
- [큐 `allOnQueue` 및 `allOnConnection`](#queue-allOnQueue-allOnConnection)
- [페이지네이션 기본값](#pagination-defaults)
- [시더 & 팩토리 네임스페이스](#seeder-factory-namespaces)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경사항

<div class="content-list" markdown="1">

- [PHP 7.3.0 필요](#php-7.3.0-required)
- [실패한 작업 테이블 배치 지원](#failed-jobs-table-batch-support)
- [유지보수 모드 업데이트](#maintenance-mode-updates)
- [`php artisan down --message` 옵션](#artisan-down-message)
- [`assertExactJson` 메서드](#assert-exact-json-method)

</div>

<a name="upgrade-8.0"></a>
## 7.x에서 8.0으로 업그레이드

<a name="estimated-upgrade-time-15-minutes"></a>
#### 예상 업그레이드 소요 시간: 15분

> {note} 가능한 모든 파괴적 변경 사항을 문서화하려고 합니다. 이 중 일부는 프레임워크의 잘 알려지지 않은 부분에 적용될 수 있으므로, 실제로는 일부만이 여러분의 애플리케이션에 영향을 줄 수 있습니다.

<a name="php-7.3.0-required"></a>
### PHP 7.3.0 필요

**영향도: 중간**

최소 PHP 버전이 7.3.0으로 상향되었습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

`composer.json` 파일에서 다음 의존성을 업데이트하세요:

<div class="content-list" markdown="1">

- `guzzlehttp/guzzle`를 `^7.0.1`로
- `facade/ignition`을 `^2.3.6`로
- `laravel/framework`를 `^8.0`으로
- `laravel/ui`를 `^3.0`으로
- `nunomaduro/collision`을 `^5.0`으로
- `phpunit/phpunit`을 `^9.0`으로

</div>

아래의 1st-party 패키지들은 Laravel 8을 지원하기 위한 새로운 주요 버전이 릴리스되었습니다. 해당한다면, 업그레이드 전에 각자의 업그레이드 가이드를 참고하세요:

<div class="content-list" markdown="1">

- [Horizon v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)

</div>

또한, Laravel 인스톨러도 `composer create-project`와 Laravel Jetstream 지원을 위해 업데이트되었습니다. 4.0 미만 버전의 인스톨러는 2020년 10월 이후 동작하지 않으니, 글로벌 인스톨러를 `^4.0`으로 업그레이드하세요.

마지막으로, 애플리케이션에서 사용하는 다른 써드파티 패키지가 Laravel 8을 지원하는 적절한 버전을 사용하는지 반드시 확인하세요.

<a name="collections"></a>
### 컬렉션

<a name="the-isset-method"></a>
#### `isset` 메서드

**영향도: 낮음**

PHP의 일반 동작과 일치하도록, `Illuminate\Support\Collection`의 `offsetExists` 메서드는 이제 `array_key_exists` 대신 `isset`을 사용합니다. 컬렉션 아이템 값이 `null`인 경우 동작이 달라질 수 있습니다:

    $collection = collect([null]);

    // Laravel 7.x - true
    isset($collection[0]);

    // Laravel 8.x - false
    isset($collection[0]);

<a name="database"></a>
### 데이터베이스

<a name="seeder-factory-namespaces"></a>
#### 시더 & 팩토리 네임스페이스

**영향도: 높음**

시더(Seeders)와 팩토리(Factory)에 네임스페이스가 도입되었습니다. 이 변경을 반영하려면 시더 클래스에 `Database\Seeders` 네임스페이스를 추가하세요. 또한 기존의 `database/seeds` 디렉터리는 `database/seeders`로 이름을 변경해야 합니다:

    <?php

    namespace Database\Seeders;

    use App\Models\User;
    use Illuminate\Database\Seeder;

    class DatabaseSeeder extends Seeder
    {
        /**
         * 애플리케이션의 DB를 시드합니다.
         *
         * @return void
         */
        public function run()
        {
            ...
        }
    }

`laravel/legacy-factories` 패키지를 사용하는 경우 팩토리 클래스에는 변경이 필요하지 않습니다. 그러나 팩토리를 업그레이드할 경우, 해당 클래스에 `Database\Factories` 네임스페이스를 추가해야 합니다.

그 다음, `composer.json` 파일에서 `autoload`의 `classmap` 블록을 제거하고, 다음과 같은 네임스페이스 디렉터리 매핑을 추가하세요:

    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\Factories\\": "database/factories/",
            "Database\\Seeders\\": "database/seeders/"
        }
    },

<a name="eloquent"></a>
### Eloquent

<a name="model-factories"></a>
#### 모델 팩토리

**영향도: 높음**

Laravel의 [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories) 기능이 클래스 기반으로 완전히 재작성되어, Laravel 7.x 스타일의 팩토리와 호환되지 않습니다. 업그레이드 과정을 쉽게 하기 위해 `laravel/legacy-factories` 패키지가 제공되며, Laravel 8.x에서 기존 팩토리를 계속 사용할 수 있습니다. Composer로 해당 패키지를 설치하세요:

    composer require laravel/legacy-factories

<a name="the-castable-interface"></a>
#### `Castable` 인터페이스

**영향도: 낮음**

`Castable` 인터페이스의 `castUsing` 메서드는 이제 인자 배열을 받도록 업데이트되었습니다. 이 인터페이스를 구현하는 경우, 다음과 같이 수정하세요:

    public static function castUsing(array $arguments);

<a name="increment-decrement-events"></a>
#### Increment / Decrement 이벤트

**영향도: 낮음**

이제 Eloquent 모델 인스턴스에서 `increment` 또는 `decrement` 메서드를 실행하면, 관련 "update" 및 "save" 모델 이벤트가 올바르게 디스패치됩니다.

<a name="events"></a>
### 이벤트

<a name="the-event-service-provider-class"></a>
#### `EventServiceProvider` 클래스

**영향도: 낮음**

만약 `App\Providers\EventServiceProvider` 클래스에 `register` 함수가 있다면, 이 함수의 시작 부분에 반드시 `parent::register`를 호출해야 합니다. 그렇지 않으면 애플리케이션의 이벤트가 등록되지 않습니다.

<a name="the-dispatcher-contract"></a>
#### `Dispatcher` 계약

**영향도: 낮음**

`Illuminate\Contracts\Events\Dispatcher` 계약의 `listen` 메서드는 `$listener` 프로퍼티를 선택 사항으로 변경했습니다. 이 변경은 리플렉션을 통한 자동 이벤트 타입 감지 지원을 위한 것입니다. 이 인터페이스를 직접 구현한다면, 다음과 같이 수정하세요:

    public function listen($events, $listener = null);

<a name="framework"></a>
### 프레임워크

<a name="maintenance-mode-updates"></a>
#### 유지보수 모드 업데이트

**영향도: 선택적**

Laravel의 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode) 기능이 개선되었으며, 유지보수 템플릿의 사전 렌더링을 지원하여 유지보수 중 사용자가 오류를 만나지 않도록 했습니다. 이를 지원하기 위해, 다음 라인을 `public/index.php` 파일의 기존 `LARAVEL_START` 상수 정의 바로 아래에 추가하세요:

    define('LARAVEL_START', microtime(true));

    if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
        require $maintenance;
    }

<a name="artisan-down-message"></a>
#### `php artisan down --message` 옵션

**영향도: 중간**

`php artisan down` 명령의 `--message` 옵션이 제거되었습니다. 대신, [유지보수 모드 뷰를 사전 렌더링](/docs/{{version}}/configuration#maintenance-mode)하여 원하는 메시지를 표시할 수 있습니다.

<a name="php-artisan-serve-no-reload-option"></a>
#### `php artisan serve --no-reload` 옵션

**영향도: 낮음**

`php artisan serve` 명령에 `--no-reload` 옵션이 추가되었습니다. 이 옵션은 환경 파일 변경 시 서버가 자동 재시작 되지 않게 하며, CI 환경에서 Laravel Dusk 테스트를 실행할 때 주로 유용합니다.

<a name="manager-app-property"></a>
#### Manager 클래스의 `$app` 프로퍼티

**영향도: 낮음**

기존에 deprecated 되었던 `Illuminate\Support\Manager` 클래스의 `$app` 프로퍼티가 제거되었습니다. 이 프로퍼티에 의존했다면, 대신 `$container` 프로퍼티를 사용하세요.

<a name="the-elixir-helper"></a>
#### `elixir` 헬퍼

**영향도: 낮음**

기존에 deprecated 되었던 `elixir` 헬퍼가 제거되었습니다. 이 메서드를 사용 중이라면 [Laravel Mix](https://github.com/JeffreyWay/laravel-mix)로 업그레이드할 것을 권장합니다.

<a name="mail"></a>
### 메일

<a name="the-sendnow-method"></a>
#### `sendNow` 메서드

**영향도: 낮음**

기존에 deprecated 되었던 `sendNow` 메서드가 제거되었습니다. 대신 `send` 메서드를 사용하세요.

<a name="pagination"></a>
### 페이지네이션

<a name="pagination-defaults"></a>
#### 페이지네이션 기본값

**영향도: 높음**

페이지네이터의 기본 스타일이 [Tailwind CSS 프레임워크](https://tailwindcss.com)로 변경되었습니다. 만약 Bootstrap을 계속 사용하고 싶다면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에 아래 메서드를 추가하세요:

    use Illuminate\Pagination\Paginator;

    Paginator::useBootstrap();

<a name="queue"></a>
### 큐

<a name="queue-retry-after-method"></a>
#### `retryAfter` 메서드

**영향도: 높음**

Laravel의 기타 기능과의 일관성을 위해, 큐 작업, 메일러, 알림, 리스너에서 `retryAfter` 메서드와 `retryAfter` 프로퍼티 이름이 `backoff`로 변경되었습니다. 관련 클래스에서 해당 메서드/프로퍼티 이름을 모두 변경하세요.

<a name="queue-timeout-at-property"></a>
#### `timeoutAt` 프로퍼티

**영향도: 높음**

큐 작업, 알림, 리스너에서의 `timeoutAt` 프로퍼티 이름이 `retryUntil`로 변경되었습니다. 관련 클래스에서 해당 프로퍼티 이름을 변경하세요.

<a name="queue-allOnQueue-allOnConnection"></a>
#### `allOnQueue()` / `allOnConnection()` 메서드

**영향도: 높음**

기타 디스패치 메서드와 일관성을 위해, 잡 체이닝에서 사용되던 `allOnQueue()`와 `allOnConnection()` 메서드가 제거되었습니다. 대신 `onQueue()`와 `onConnection()` 메서드를 사용하세요. 이 메서드들은 `dispatch` 호출 전에 체이닝해서 사용해야 합니다:

    ProcessPodcast::withChain([
        new OptimizePodcast,
        new ReleasePodcast
    ])->onConnection('redis')->onQueue('podcasts')->dispatch();

이 변경은 `withChain` 메서드를 사용하는 코드에만 영향을 미치며, 글로벌 `dispatch()` 헬퍼를 사용할 때는 `allOnQueue()`와 `allOnConnection()`이 여전히 사용 가능합니다.

<a name="failed-jobs-table-batch-support"></a>
#### 실패한 작업 테이블 배치 지원

**영향도: 선택적**

[잡 배치](/docs/{{version}}/queues#job-batching) 기능을 사용할 경우 `failed_jobs` 데이터베이스 테이블을 다음과 같이 업데이트해야 합니다. 먼저, 테이블에 새로운 `uuid` 컬럼을 추가하세요:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('failed_jobs', function (Blueprint $table) {
        $table->string('uuid')->after('id')->nullable()->unique();
    });

그 다음, `queue` 설정 파일에서 `failed.driver` 옵션을 `database-uuids`로 변경하세요.

또한, 기존 실패한 작업에 UUID를 생성하려면 다음을 실행하세요:

    DB::table('failed_jobs')->whereNull('uuid')->cursor()->each(function ($job) {
        DB::table('failed_jobs')
            ->where('id', $job->id)
            ->update(['uuid' => (string) Illuminate\Support\Str::uuid()]);
    });

<a name="routing"></a>
### 라우팅

<a name="automatic-controller-namespace-prefixing"></a>
#### 컨트롤러 네임스페이스 자동 프리픽스

**영향도: 선택적**

기존 Laravel 릴리즈에서는 `RouteServiceProvider` 클래스에 `App\Http\Controllers` 값의 `$namespace` 프로퍼티가 있었습니다. 이 값은 컨트롤러 라우트 선언 및 URL 생성 시 자동으로 사용되었습니다.

Laravel 8에서는 이 프로퍼티가 기본적으로 `null`로 설정되어, 컨트롤러 라우트 선언 시 표준 PHP 콜러블 문법을 사용할 수 있습니다. 이로 인해 많은 IDE에서 컨트롤러 클래스로의 이동이 원활해집니다:

    use App\Http\Controllers\UserController;

    // PHP 콜러블 문법 사용...
    Route::get('/users', [UserController::class, 'index']);

    // 문자열 문법 사용...
    Route::get('/users', 'App\Http\Controllers\UserController@index');

대부분의 경우 업그레이드하는 애플리케이션에는 영향을 주지 않습니다. 단, 새 Laravel 프로젝트로 이전하는 경우에는 이 변경에 주의하세요.

기존 자동 프리픽스 방식의 라우팅을 계속 사용하려면, `RouteServiceProvider`의 `$namespace` 값을 원래대로 지정하고, `boot` 메서드 내 라우트 등록에도 해당 값을 사용하세요:

    class RouteServiceProvider extends ServiceProvider
    {
        /**
         * 홈 라우트의 경로.
         * 
         * Laravel 인증 등에서 로그인 후 리디렉션에 사용됨.
         *
         * @var string
         */
        public const HOME = '/home';

        /**
         * 지정할 경우 이 네임스페이스가 컨트롤러 라우트에 자동 적용됩니다.
         *
         * 또한 URL 생성기의 루트 네임스페이스로 설정됩니다.
         *
         * @var string
         */
        protected $namespace = 'App\Http\Controllers';

        /**
         * 라우트 모델 바인딩, 패턴 필터 등 정의.
         *
         * @return void
         */
        public function boot()
        {
            $this->configureRateLimiting();

            $this->routes(function () {
                Route::middleware('web')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/web.php'));

                Route::prefix('api')
                    ->middleware('api')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/api.php'));
            });
        }

        /**
         * 애플리케이션의 속도 제한기 구성.
         *
         * @return void
         */
        protected function configureRateLimiting()
        {
            RateLimiter::for('api', function (Request $request) {
                return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());
            });
        }
    }

<a name="scheduling"></a>
### 스케줄링

<a name="the-cron-expression-library"></a>
#### `cron-expression` 라이브러리

**영향도: 낮음**

Laravel이 의존하는 `dragonmantank/cron-expression` 라이브러리가 `2.x`에서 `3.x`로 업그레이드되었습니다. 이 라이브러리를 직접 사용하는 경우가 아니라면 애플리케이션에 큰 영향을 주지 않습니다. 직접 사용하는 경우 [변경 로그](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md)를 확인하세요.

<a name="session"></a>
### 세션

<a name="the-session-contract"></a>
#### `Session` 계약

**영향도: 낮음**

`Illuminate\Contracts\Session\Session` 인터페이스에 새로운 `pull` 메서드가 추가되었습니다. 이 인터페이스를 직접 구현한다면, 다음처럼 구현을 업데이트하세요:

    /**
     * 주어진 키의 값을 얻고, 바로 지웁니다.
     *
     * @param  string  $key
     * @param  mixed  $default
     * @return mixed
     */
    public function pull($key, $default = null);

<a name="testing"></a>
### 테스트

<a name="decode-response-json-method"></a>
#### `decodeResponseJson` 메서드

**영향도: 낮음**

`Illuminate\Testing\TestResponse` 클래스에 있는 `decodeResponseJson` 메서드는 더이상 어떠한 인자도 받지 않습니다. 대신 `json` 메서드 사용을 고려하세요.

<a name="assert-exact-json-method"></a>
#### `assertExactJson` 메서드

**영향도: 중간**

`assertExactJson` 메서드는 이제 비교되는 배열의 수치 인덱스 키까지 일치하고 동일한 순서일 것을 요구합니다. 숫자 인덱스 배열의 순서에 관계없이 JSON과 배열을 비교하고 싶다면 `assertSimilarJson` 메서드를 사용하세요.

<a name="validation"></a>
### 유효성 검사

<a name="database-rule-connections"></a>
### 데이터베이스 규칙 커넥션

**영향도: 낮음**

`unique` 및 `exists` 룰은 쿼리 수행 시 Eloquent 모델의 `getConnectionName` 메서드를 통해 지정된 커넥션명을 이제 준수합니다.

<a name="miscellaneous"></a>
### 기타

`laravel/laravel`의 [GitHub 저장소](https://github.com/laravel/laravel)에서 변경 사항을 확인해보는 것도 권장합니다. 이 변경 중 많은 부분이 필수는 아니지만 애플리케이션과 파일을 동기화하고 싶을 수도 있습니다. 일부는 이 업그레이드 가이드에 포함되지만, 설정 파일이나 주석 등의 변경은 포함되어있지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/7.x...8.x)를 통해 쉽게 변경 사항을 확인하고 필요한 업데이트만 선택하세요.