# 동시성

- [소개](#introduction)
- [동시 작업 실행하기](#running-concurrent-tasks)
- [동시 작업 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

> [!WARNING]
> Laravel의 `Concurrency` 파사드는 현재 커뮤니티 피드백을 수집하는 동안 베타 버전입니다.

때로는 서로 의존하지 않는 여러 개의 느린 작업을 실행해야 할 때가 있습니다. 많은 경우 이러한 작업을 동시에 실행하면 성능을 크게 향상시킬 수 있습니다. Laravel의 `Concurrency` 파사드는 클로저를 동시에 실행할 수 있는 간단하고 편리한 API를 제공합니다.

<a name="concurrency-compatibility"></a>
#### 동시성 호환성

Laravel 10.x 애플리케이션에서 Laravel 11.x로 업그레이드한 경우, 애플리케이션의 `config/app.php` 설정 파일의 `providers` 배열에 `ConcurrencyServiceProvider`를 추가해야 할 수도 있습니다.

```php
'providers' => ServiceProvider::defaultProviders()->merge([
    /*
     * 패키지 서비스 프로바이더...
     */
    Illuminate\Concurrency\ConcurrencyServiceProvider::class, // [tl! add]

    /*
     * 애플리케이션 서비스 프로바이더...
     */
    App\Providers\AppServiceProvider::class,
    App\Providers\AuthServiceProvider::class,
    // App\Providers\BroadcastServiceProvider::class,
    App\Providers\EventServiceProvider::class,
    App\Providers\RouteServiceProvider::class,
])->toArray(),
```

<a name="how-it-works"></a>
#### 동작 방식

Laravel은 전달된 클로저를 직렬화한 후, 이를 숨겨진 Artisan CLI 명령어로 전달하여 클로저를 역직렬화하고 각기 독립된 PHP 프로세스에서 실행합니다. 클로저의 실행이 끝나면, 반환된 값은 다시 부모 프로세스로 직렬화되어 전달됩니다.

`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, 그리고 `fork`, `sync` 드라이버입니다.

`fork` 드라이버는 기본 `process` 드라이버에 비해 성능이 더 우수하지만, PHP가 웹 요청 중에는 포크를 지원하지 않기 때문에 오직 PHP의 CLI 환경에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면, 우선 `spatie/fork` 패키지를 설치해야 합니다:

```shell
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트 환경에서, 동시성을 모두 비활성화하고 클로저를 순차적으로 부모 프로세스 내에서 실행하고자 할 때 유용합니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행하기

동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하면 됩니다. `run` 메서드는 동시에 자식 PHP 프로세스에서 실행되어야 하는 클로저의 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

특정 드라이버를 사용하고 싶다면 `driver` 메서드를 사용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

또는, 기본 동시성 드라이버를 변경하고 싶다면, `config:publish` Artisan 명령어를 통해 `concurrency` 설정 파일을 퍼블리시한 뒤 해당 파일 내의 `default` 옵션을 수정하세요:

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연 실행하기

여러 개의 클로저를 동시에 실행하되 반환값에는 관심이 없다면, `defer` 메서드 사용을 고려할 수 있습니다. `defer` 메서드를 호출하면, 전달된 클로저들은 즉시 실행되지 않고 HTTP 응답이 사용자에게 전송된 후에 동시에 실행됩니다.

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```