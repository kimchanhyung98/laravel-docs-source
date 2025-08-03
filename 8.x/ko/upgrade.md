# 업그레이드 가이드 (Upgrade Guide)

- [7.x 버전에서 8.0 버전으로 업그레이드하기](#upgrade-8.0)

<a name="high-impact-changes"></a>
## 주요 영향 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [모델 팩토리 (Model Factories)](#model-factories)
- [큐 `retryAfter` 메서드](#queue-retry-after-method)
- [큐 `timeoutAt` 속성](#queue-timeout-at-property)
- [큐 `allOnQueue` 및 `allOnConnection` 메서드](#queue-allOnQueue-allOnConnection)
- [페이지네이션 기본값 (Pagination Defaults)](#pagination-defaults)
- [시더 및 팩토리 네임스페이스 (Seeder & Factory Namespaces)](#seeder-factory-namespaces)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [PHP 7.3.0 이상 필요](#php-7.3.0-required)
- [실패 작업 테이블 배치 지원 (Failed Jobs Table Batch Support)](#failed-jobs-table-batch-support)
- [유지보수 모드 업데이트 (Maintenance Mode Updates)](#maintenance-mode-updates)
- [`php artisan down --message` 옵션 변경](#artisan-down-message)
- [`assertExactJson` 메서드 변경](#assert-exact-json-method)

</div>

<a name="upgrade-8.0"></a>
## 7.x 버전에서 8.0 버전으로 업그레이드하기 (Upgrading To 8.0 From 7.x)

<a name="estimated-upgrade-time-15-minutes"></a>
#### 예상 업그레이드 소요 시간: 15분

> [!NOTE]
> 가능한 모든 파괴적 변경 사항을 문서화하려고 노력했습니다. 그러나 프레임워크의 잘 알려지지 않은 부분에서 발생하는 변경 사항도 있으므로, 실제로는 이 변경 사항들 중 일부만 애플리케이션에 영향을 줄 수 있습니다.

<a name="php-7.3.0-required"></a>
### PHP 7.3.0 이상 필요 (PHP 7.3.0 Required)

**영향 가능성: 중간**

최소 지원 PHP 버전이 7.3.0으로 상향 조정되었습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

`composer.json` 파일 내에서 다음 의존성을 업데이트하세요:

<div class="content-list" markdown="1">

- `guzzlehttp/guzzle` 을 `^7.0.1` 로
- `facade/ignition` 을 `^2.3.6` 로
- `laravel/framework` 을 `^8.0` 로
- `laravel/ui` 을 `^3.0` 로
- `nunomaduro/collision` 을 `^5.0` 로
- `phpunit/phpunit` 을 `^9.0` 로

</div>

아래 첫 번째 파티 패키지들은 Laravel 8 지원을 위해 주요 버전이 업데이트되었습니다. 해당하는 경우, 개별 업그레이드 가이드를 먼저 반드시 확인하세요:

<div class="content-list" markdown="1">

- [Horizon v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)

</div>

추가로, Laravel 설치 도구(installer)가 `composer create-project` 와 Laravel Jetstream을 지원하도록 업데이트되었습니다. 2020년 10월 이후로 버전 4.0 미만의 설치 도구는 동작하지 않으니, 전역 설치 도구를 가능한 빨리 `^4.0` 으로 업그레이드하세요.

마지막으로, 애플리케이션에서 사용하는 타사 패키지들도 Laravel 8 지원용 올바른 버전을 사용 중인지 확인해야 합니다.

<a name="collections"></a>
### 컬렉션 (Collections)

<a name="the-isset-method"></a>
#### `isset` 메서드 변경 (The `isset` Method)

**영향 가능성: 낮음**

기존 `Illuminate\Support\Collection` 클래스의 `offsetExists` 메서드가 `array_key_exists` 대신 `isset` 을 사용하도록 변경되어, null 값이 포함된 컬렉션 아이템에 대해 동작이 다르게 될 수 있습니다:

```
$collection = collect([null]);

// Laravel 7.x - true
isset($collection[0]);

// Laravel 8.x - false
isset($collection[0]);
```

<a name="database"></a>
### 데이터베이스 (Database)

<a name="seeder-factory-namespaces"></a>
#### 시더 및 팩토리 네임스페이스 변경 (Seeder & Factory Namespaces)

**영향 가능성: 높음**

시더(Seeder)와 팩토리에 네임스페이스가 추가되었습니다. 이에 따라 시더 클래스에는 `Database\Seeders` 네임스페이스를 명시해야 하며, 이전의 `database/seeds` 디렉터리는 `database/seeders` 로 이름을 변경해야 합니다:

```
<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * 애플리케이션 데이터베이스 시드 실행
     *
     * @return void
     */
    public function run()
    {
        ...
    }
}
```

`laravel/legacy-factories` 패키지를 사용하는 경우, 기존 팩토리 클래스는 변경할 필요가 없습니다. 하지만 업그레이드된 팩토리를 사용하려면, 팩토리 클래스에 `Database\Factories` 네임스페이스를 추가해야 합니다.

다음으로, `composer.json` 의 `autoload` 영역에서 기존 `classmap` 블록을 제거하고, 다음과 같이 네임스페이스 기반 클래스 경로 맵핑을 추가해야 합니다:

```
"autoload": {
    "psr-4": {
        "App\\": "app/",
        "Database\\Factories\\": "database/factories/",
        "Database\\Seeders\\": "database/seeders/"
    }
},
```

<a name="eloquent"></a>
### 엘로퀀트 (Eloquent)

<a name="model-factories"></a>
#### 모델 팩토리 (Model Factories)

**영향 가능성: 높음**

Laravel의 [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories) 기능이 클래스 기반으로 완전히 재작성되어, 이전 7.x 스타일 팩토리와 호환되지 않습니다. 하지만 업그레이드를 쉽게 하기 위해 기존 팩토리를 Laravel 8.x에서 계속 사용할 수 있게 해주는 `laravel/legacy-factories` 패키지가 제공됩니다. 다음 커맨드를 통해 설치할 수 있습니다:

```
composer require laravel/legacy-factories
```

<a name="the-castable-interface"></a>
#### `Castable` 인터페이스 변경 (The `Castable` Interface)

**영향 가능성: 낮음**

`Castable` 인터페이스의 `castUsing` 메서드가 인수로 배열을 받도록 변경되었습니다. 이 인터페이스를 구현 중이라면, 다음과 같이 수정해야 합니다:

```
public static function castUsing(array $arguments);
```

<a name="increment-decrement-events"></a>
#### 증가/감소 이벤트 (Increment / Decrement Events)

**영향 가능성: 낮음**

Eloquent 모델 인스턴스에서 `increment` 또는 `decrement` 메서드를 실행할 때, 적절한 "update" 및 "save" 관련 모델 이벤트가 발생되도록 개선되었습니다.

<a name="events"></a>
### 이벤트 (Events)

<a name="the-event-service-provider-class"></a>
#### `EventServiceProvider` 클래스 (The `EventServiceProvider` Class)

**영향 가능성: 낮음**

`App\Providers\EventServiceProvider` 클래스에 `register` 메서드가 포함되어 있다면, 이 메서드 시작 부분에 반드시 `parent::register`를 호출해야 합니다. 이를 호출하지 않으면 애플리케이션 이벤트가 등록되지 않습니다.

<a name="the-dispatcher-contract"></a>
#### `Dispatcher` 계약 (The `Dispatcher` Contract)

**영향 가능성: 낮음**

`Illuminate\Contracts\Events\Dispatcher` 계약의 `listen` 메서드가 `$listener` 인수를 선택적으로 받도록 변경되었습니다. 이 변경은 reflection을 활용한 이벤트 타입 자동 감지를 지원하기 위한 것입니다. 수동 구현 시 다음과 같이 수정해야 합니다:

```
public function listen($events, $listener = null);
```

<a name="framework"></a>
### 프레임워크 (Framework)

<a name="maintenance-mode-updates"></a>
#### 유지보수 모드 업데이트 (Maintenance Mode Updates)

**영향 가능성: 선택적**

Laravel 8.x에서 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)가 개선되어, 유지보수 모드 템플릿 사전 렌더링을 지원합니다. 이를 통해 종료 사용자에게 유지보수 중 오류가 노출되는 상황이 줄어듭니다.

이 기능을 지원하기 위해 `public/index.php` 파일 내 `LARAVEL_START` 정의 바로 아래에 아래 코드를 추가해야 합니다:

```
define('LARAVEL_START', microtime(true));

if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
    require $maintenance;
}
```

<a name="artisan-down-message"></a>
#### `php artisan down --message` 옵션 변경 (The `php artisan down --message` Option)

**영향 가능성: 중간**

`php artisan down` 명령어의 `--message` 옵션이 제거되었습니다. 대신 [유지보수 모드 뷰를 사전 렌더링](/docs/{{version}}/configuration#maintenance-mode) 하는 방식을 사용해 메시지를 정의하는 것을 권장합니다.

<a name="php-artisan-serve-no-reload-option"></a>
#### `php artisan serve --no-reload` 옵션 추가 (The `php artisan serve --no-reload` Option)

**영향 가능성: 낮음**

`php artisan serve` 명령어에 `--no-reload` 옵션이 추가되었습니다. 이 옵션을 사용하면 환경파일 변경 시 서버가 자동 재시작되지 않습니다. 주로 CI 환경에서 Laravel Dusk 테스트를 실행할 때 유용합니다.

<a name="manager-app-property"></a>
#### Manager 클래스 `$app` 속성 제거 (Manager `$app` Property)

**영향 가능성: 낮음**

`Illuminate\Support\Manager` 클래스 내에서 이전에 deprecated 상태였던 `$app` 속성이 삭제되었습니다. 만약 이 속성을 사용하던 경우, 대신 `$container` 속성을 사용하세요.

<a name="the-elixir-helper"></a>
#### `elixir` 헬퍼 제거 (The `elixir` Helper)

**영향 가능성: 낮음**

더 이상 사용되지 않는 `elixir` 헬퍼 함수가 삭제되었습니다. 해당 기능을 계속 사용하고 있다면 [Laravel Mix](https://github.com/JeffreyWay/laravel-mix)로 업그레이드하는 것을 권장합니다.

<a name="mail"></a>
### 메일 (Mail)

<a name="the-sendnow-method"></a>
#### `sendNow` 메서드 제거 (The `sendNow` Method)

**영향 가능성: 낮음**

이전 버전에서 deprecated 되었던 `sendNow` 메서드가 완전히 제거되었습니다. 대신 `send` 메서드를 사용하세요.

<a name="pagination"></a>
### 페이지네이션 (Pagination)

<a name="pagination-defaults"></a>
#### 페이지네이션 기본 스타일 변경 (Pagination Defaults)

**영향 가능성: 높음**

기본 페이지네이터가 이제 [Tailwind CSS 프레임워크](https://tailwindcss.com)를 스타일 기본값으로 사용합니다.

Bootstrap 스타일을 계속 사용하려면, 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에 다음 코드를 추가해야 합니다:

```
use Illuminate\Pagination\Paginator;

Paginator::useBootstrap();
```

<a name="queue"></a>
### 큐 (Queue)

<a name="queue-retry-after-method"></a>
#### `retryAfter` 메서드 변경 (The `retryAfter` Method)

**영향 가능성: 높음**

일관성을 위해 큐 잡, 메일러, 알림, 리스너의 `retryAfter` 메서드와 `retryAfter` 속성명이 `backoff` 으로 변경되었습니다. 애플리케이션 내 관련 클래스에서 해당 이름을 수정해야 합니다.

<a name="queue-timeout-at-property"></a>
#### `timeoutAt` 속성 변경 (The `timeoutAt` Property)

**영향 가능성: 높음**

큐 잡, 알림, 리스너의 `timeoutAt` 속성명이 `retryUntil` 으로 변경되었습니다. 애플리케이션 내에서 이 속성명을 업데이트해야 합니다.

<a name="queue-allOnQueue-allOnConnection"></a>
#### `allOnQueue()` / `allOnConnection()` 메서드 제거 (The `allOnQueue()` / `allOnConnection()` Methods)

**영향 가능성: 높음**

잡 체이닝 시 사용하던 `allOnQueue()` 및 `allOnConnection()` 메서드가 제거되었습니다. 대신 `onQueue()` 와 `onConnection()` 메서드를 사용하세요. 이 메서드들은 `dispatch` 호출 전에 사용해야 합니다:

```
ProcessPodcast::withChain([
    new OptimizePodcast,
    new ReleasePodcast
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

참고로 이 변경 사항은 `withChain` 메서드를 사용할 때만 영향을 미칩니다. 전역 `dispatch()` 헬퍼를 사용할 때는 `allOnQueue()` 와 `allOnConnection()` 메서드가 여전히 존재합니다.

<a name="failed-jobs-table-batch-support"></a>
#### 실패 작업 테이블 배치 지원 (Failed Jobs Table Batch Support)

**영향 가능성: 선택적**

Laravel 8.x의 [잡 배칭(job batching)](/docs/{{version}}/queues#job-batching) 기능을 사용하려면, 실패 작업(`failed_jobs`) 데이터베이스 테이블에 새로운 `uuid` 컬럼을 추가해야 합니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('failed_jobs', function (Blueprint $table) {
    $table->string('uuid')->after('id')->nullable()->unique();
});
```

또한 `queue` 설정 파일 내 `failed.driver` 옵션을 `database-uuids` 로 변경해야 합니다.

기존 실패 작업에 UUID를 생성하고 싶다면 다음 코드도 사용할 수 있습니다:

```
DB::table('failed_jobs')->whereNull('uuid')->cursor()->each(function ($job) {
    DB::table('failed_jobs')
        ->where('id', $job->id)
        ->update(['uuid' => (string) Illuminate\Support\Str::uuid()]);
});
```

<a name="routing"></a>
### 라우팅 (Routing)

<a name="automatic-controller-namespace-prefixing"></a>
#### 컨트롤러 네임스페이스 자동 접두사 해제 (Automatic Controller Namespace Prefixing)

**영향 가능성: 선택적**

과거 Laravel 릴리스에서 `RouteServiceProvider` 클래스는 `$namespace` 속성에 `App\Http\Controllers` 값을 기본으로 설정하고, 이를 이용해 컨트롤러 라우트 선언을 자동으로 네임스페이스 접두사 처리했습니다.

Laravel 8에서는 이 값이 기본적으로 `null` 로 설정되어 있으며, PHP 호출 가능한(callable) 배열 구문을 사용해 컨트롤러를 지정하도록 유도합니다. 이는 다수 IDE에서 컨트롤러 클래스로 쉽게 이동할 수 있도록 해줍니다:

```php
use App\Http\Controllers\UserController;

// PHP callable 구문 사용...
Route::get('/users', [UserController::class, 'index']);

// 문자열 구문 사용...
Route::get('/users', 'App\Http\Controllers\UserController@index');
```

일반적으로 기존 애플리케이션에는 기존 `$namespace` 속성 설정이 유지되어 있으므로 큰 영향은 없습니다. 하지만 새로운 Laravel 프로젝트를 생성해 업그레이드하는 경우에는 브레이킹 체인지로 작용할 수 있습니다.

원래 자동 네임스페이스 접두사를 계속 사용하고 싶다면, `RouteServiceProvider` 의 `$namespace` 속성을 설정하고 `boot` 메서드의 라우트 등록 시 이를 참조하도록 변경하세요:

```php
class RouteServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션의 "홈" 경로입니다.
     *
     * 로그인 후 Laravel 인증이 사용자를 리디렉션하는 경로입니다.
     *
     * @var string
     */
    public const HOME = '/home';

    /**
     * 지정하면, 이 네임스페이스가 컨트롤러 라우트에 자동 적용됩니다.
     * 또한 URL 생성기의 루트 네임스페이스로 사용됩니다.
     *
     * @var string
     */
    protected $namespace = 'App\Http\Controllers';

    /**
     * 라우트 모델 바인딩, 패턴 필터 등 정의
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
     * 애플리케이션의 속도 제한기 구성
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
```

<a name="scheduling"></a>
### 스케줄링 (Scheduling)

<a name="the-cron-expression-library"></a>
#### `cron-expression` 라이브러리 버전 변경 (The `cron-expression` Library)

**영향 가능성: 낮음**

Laravel이 의존하는 `dragonmantank/cron-expression` 라이브러리가 `2.x` 버전에서 `3.x` 버전으로 업데이트되었습니다. 대부분의 애플리케이션에 파괴적 변경은 없지만, 직접 이 라이브러리를 사용하는 경우 [변경 로그](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md)를 검토하세요.

<a name="session"></a>
### 세션 (Session)

<a name="the-session-contract"></a>
#### `Session` 계약의 `pull` 메서드 추가 (The `Session` Contract)

**영향 가능성: 낮음**

`Illuminate\Contracts\Session\Session` 계약에 새 `pull` 메서드가 추가되었습니다. 해당 계약을 수동으로 구현하는 경우 다음 메서드를 구현해야 합니다:

```
/**
 * 지정된 키의 값을 가져오고, 해당 키를 세션에서 삭제합니다.
 *
 * @param  string  $key
 * @param  mixed  $default
 * @return mixed
 */
public function pull($key, $default = null);
```

<a name="testing"></a>
### 테스트 (Testing)

<a name="decode-response-json-method"></a>
#### `decodeResponseJson` 메서드 변경 (The `decodeResponseJson` Method)

**영향 가능성: 낮음**

`Illuminate\Testing\TestResponse` 클래스의 `decodeResponseJson` 메서드는 이제 인수를 받지 않습니다. 대신 `json` 메서드 사용을 고려하세요.

<a name="assert-exact-json-method"></a>
#### `assertExactJson` 메서드 변경 (The `assertExactJson` Method)

**영향 가능성: 중간**

`assertExactJson` 메서드는 이제 비교 대상 배열의 숫자형 키가 일치하고 순서도 같아야 합니다. 숫자 키 배열 순서에 관계없이 JSON을 비교하고 싶으면 `assertSimilarJson` 메서드를 사용하세요.

<a name="validation"></a>
### 유효성 검사 (Validation)

<a name="database-rule-connections"></a>
#### 데이터베이스 규칙 연결 (Database Rule Connections)

**영향 가능성: 낮음**

`unique` 및 `exists` 유효성 검사 규칙은 이제 Eloquent 모델의 `getConnectionName` 메서드로 명시된 연결명을 존중하여 쿼리를 수행합니다.

<a name="miscellaneous"></a>
### 기타 (Miscellaneous)

또한 `laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)에 반영된 변경 사항도 확인하는 것을 권장합니다. 많은 변경 사항이 필수는 아니지만, 애플리케이션과의 동기화를 위해 해당 파일을 유지하는 것이 좋습니다.

이 중에서는 본 업그레이드 가이드에 다루는 것과 설정 파일이나 주석 변경 등 별도로 다루지 않는 부분도 있습니다.

[GitHub 비교 도구](https://github.com/laravel/laravel/compare/7.x...8.x)로 쉽게 변경 사항을 확인하고, 중요하다고 판단되는 업데이트만 선택할 수 있습니다.