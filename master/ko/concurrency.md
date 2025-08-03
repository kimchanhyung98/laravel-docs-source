# 동시성 (Concurrency)

- [소개](#introduction)
- [동시 작업 실행하기](#running-concurrent-tasks)
- [동시 작업 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

> [!WARNING]
> Laravel의 `Concurrency` 파사드는 현재 커뮤니티 피드백을 수집하는 베타 단계입니다.

때로는 서로 의존하지 않는 여러 느린 작업을 실행해야 할 때가 있습니다. 여러 작업을 동시 실행하면 성능이 크게 향상되는 경우가 많습니다. Laravel의 `Concurrency` 파사드는 클로저를 동시에 실행할 수 있는 간단하고 편리한 API를 제공합니다.

<a name="concurrency-compatibility"></a>
#### 동시성 호환성

Laravel 10.x에서 11.x로 업그레이드했다면, 애플리케이션의 `config/app.php` 설정 파일 내 `providers` 배열에 `ConcurrencyServiceProvider`를 추가해야 할 수 있습니다:

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

Laravel은 전달된 클로저를 직렬화한 뒤, 내부적으로 Artisan CLI 명령어로 전송합니다. 명령어는 클로저를 역직렬화해 자체 PHP 프로세스 내에서 호출하며, 실행 결과 값을 다시 부모 프로세스로 직렬화해 반환합니다.

`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, `fork`, 그리고 `sync`입니다.

`fork` 드라이버는 기본 `process` 드라이버보다 성능이 더 우수하지만, PHP의 웹 요청 context에서는 포크 기능이 지원되지 않아 CLI 환경에서만 사용할 수 있습니다. 이 드라이버를 사용하려면 `spatie/fork` 패키지를 설치해야 합니다:

```shell
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트 시 모든 동시 실행을 비활성화하고 부모 프로세스 내에서 클로저를 순차 실행하고자 할 때 유용합니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행하기

동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하세요. `run` 메서드는 동시에 실행할 클로저 배열을 인자로 받으며, 각 클로저는 자식 PHP 프로세스에서 병렬로 실행됩니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

특정 드라이버를 사용하려면 `driver` 메서드를 사용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

또는 기본 동시성 드라이버를 변경하려면 `config:publish` Artisan 명령어로 `concurrency` 설정 파일을 퍼블리시한 후, 해당 파일 내 `default` 옵션을 수정하세요:

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연 실행하기

클로저 배열을 동시 실행하되, 클로저가 반환하는 결과에는 관심이 없을 경우 `defer` 메서드를 사용하는 것을 고려하세요. `defer`가 호출되면 클로저는 즉시 실행되지 않고, HTTP 응답이 사용자에게 전송된 뒤에 Laravel이 클로저들을 동시 실행합니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```