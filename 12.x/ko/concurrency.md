# 동시성 (Concurrency)

- [소개](#introduction)
- [동시 태스크 실행하기](#running-concurrent-tasks)
- [동시 태스크 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

때로는 서로 의존하지 않는 여러 개의 느린 작업을 실행해야 할 때가 있습니다. 이런 경우, 작업을 동시에 실행하면 애플리케이션의 성능이 크게 향상될 수 있습니다. 라라벨의 `Concurrency` 파사드는 클로저(closure)를 동시에 실행할 수 있도록 간단하고 편리한 API를 제공합니다.

<a name="how-it-works"></a>
#### 동작 방식

라라벨에서는 전달받은 클로저를 직렬화한 뒤, 내부적으로 숨겨진 Artisan CLI 명령어에 클로저를 전달하여 별도의 PHP 프로세스에서 이를 실행합니다. 이때, 클로저는 해당 프로세스 안에서 역직렬화되어 호출되고, 실행 결과는 다시 직렬화되어 부모 프로세스로 반환됩니다.

`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, 그리고 `fork`, `sync`입니다.

`fork` 드라이버는 기본 `process` 드라이버에 비해 더 나은 성능을 제공하지만, PHP의 웹 요청 환경에서는 포크가 지원되지 않기 때문에 PHP의 CLI 환경에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 `spatie/fork` 패키지를 설치해야 합니다:

```shell
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트 환경에서 사용하면 유용합니다. 이 드라이버를 사용하면 모든 동시성이 비활성화되고, 전달된 클로저가 부모 프로세스에서 순차적으로 실행됩니다.

<a name="running-concurrent-tasks"></a>
## 동시 태스크 실행하기

동시(Concurrent) 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하면 됩니다. `run` 메서드는 동시에 실행할 클로저 배열을 인수로 받아, 각 클로저를 하위 PHP 프로세스에서 병렬로 실행합니다:

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

기본 동시성 드라이버를 변경하려면, `config:publish` Artisan 명령어로 `concurrency` 설정 파일을 퍼블리시한 후 해당 파일의 `default` 옵션을 원하는 값으로 수정하면 됩니다:

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 태스크 지연 실행하기

클로저 배열을 동시에 실행하되, 각 클로저의 반환값에는 관심이 없다면 `defer` 메서드를 사용할 수 있습니다. `defer` 메서드를 호출하면, 전달된 클로저는 즉시 실행되지 않고, 사용자에게 HTTP 응답을 보낸 이후에 동시적으로 실행됩니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```
