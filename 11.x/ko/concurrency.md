# 동시성 (Concurrency)

- [소개](#introduction)
- [동시 작업 실행하기](#running-concurrent-tasks)
- [동시 작업 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

> [!WARNING]
> Laravel의 `Concurrency` 파사드는 현재 커뮤니티 피드백 수집을 위해 베타 상태입니다.

때로는 서로 의존하지 않는 여러 느린 작업을 병렬로 실행해야 할 때가 있습니다. 이러한 작업들을 동시에 실행하면 많은 경우 성능이 크게 향상될 수 있습니다. Laravel의 `Concurrency` 파사드는 클로저(Closure)를 동시 실행할 수 있는 간단하고 편리한 API를 제공합니다.

<a name="concurrency-compatibility"></a>
#### 동시성 호환성

Laravel 10.x에서 11.x로 업그레이드한 경우, 애플리케이션의 `config/app.php` 설정 파일 내 `providers` 배열에 `ConcurrencyServiceProvider`를 추가해야 할 수 있습니다:

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
#### 동작 원리

Laravel은 클로저를 직렬화(serialize)하여 숨겨진 Artisan CLI 명령어로 전달하고, 이 명령어는 클로저를 역직렬화(unserialize)해 별도의 PHP 프로세스 내에서 실행합니다. 클로저가 실행된 후 반환된 값은 부모 프로세스로 다시 직렬화되어 전달됩니다.

`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, `fork`, 그리고 `sync`입니다.

`fork` 드라이버는 기본 `process` 드라이버보다 성능이 향상되지만, PHP가 웹 요청 중에는 포킹을 지원하지 않기 때문에 CLI 환경에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 먼저 `spatie/fork` 패키지를 설치해야 합니다:

```bash
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트시에 모든 동시성을 비활성화하고, 클로저를 부모 프로세스 내에서 순차적으로 실행하고자 할 때 유용합니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행하기

동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하면 됩니다. `run` 메서드는 자식 PHP 프로세스에서 동시에 실행될 클로저 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

특정 드라이버를 사용하려면 `driver` 메서드를 이용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

또는 기본 동시성 드라이버를 변경하려면 `config:publish` Artisan 명령어로 `concurrency` 설정 파일을 발행한 후, 해당 파일 내 `default` 옵션을 수정하세요:

```bash
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연 실행하기

클로저 배열을 동시 실행하되, 클로저가 반환하는 결과는 필요하지 않은 경우 `defer` 메서드 사용을 고려하세요. `defer` 메서드가 호출되면 즉시 클로저를 실행하지 않고, 사용자에게 HTTP 응답이 전송된 이후에 Laravel이 클로저를 동시 실행합니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```