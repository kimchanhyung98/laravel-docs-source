# 서비스 프로바이더

- [소개](#introduction)
- [서비스 프로바이더 작성](#writing-service-providers)
    - [Register 메서드](#the-register-method)
    - [Boot 메서드](#the-boot-method)
- [프로바이더 등록](#registering-providers)
- [지연(Deferred) 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션 부트스트랩의 중심입니다. 여러분의 애플리케이션뿐만 아니라 Laravel의 모든 핵심 서비스들은 서비스 프로바이더를 통해 부트스트랩됩니다.

그렇다면 여기서 "부트스트랩"이란 무엇을 의미할까요? 일반적으로 **등록(registering)**하는 것을 의미합니다. 여기에는 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 루트(Route) 등이 포함됩니다. 서비스 프로바이더는 애플리케이션을 설정하는 중심지 역할을 합니다.

Laravel에 포함된 `config/app.php` 파일을 열어보면, `providers` 배열을 확인할 수 있습니다. 이 배열에는 애플리케이션을 위해 로드될 모든 서비스 프로바이더 클래스가 나열되어 있습니다. 기본적으로, 이 배열에는 Laravel의 핵심 서비스 프로바이더들이 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등과 같은 Laravel의 핵심 컴포넌트들을 부트스트랩합니다. 이러한 프로바이더 중 다수는 "지연(deferred)" 프로바이더로, 모든 요청에서 로드되는 것이 아니라, 실제로 해당 서비스가 필요할 때만 로드됩니다.

이 개요에서는 자신만의 서비스 프로바이더를 작성하고, 이를 Laravel 애플리케이션에 등록하는 방법을 배울 수 있습니다.

> [!NOTE]  
> Laravel이 요청을 어떻게 처리하고 내부적으로 동작하는지 더 자세히 알고 싶다면 [라라벨 요청 생명주기](/docs/{{version}}/lifecycle) 문서를 확인해보세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 포함합니다. `register` 메서드 내에서는 **오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만** 해야 합니다. 이 메서드 안에서는 이벤트 리스너, 라우트, 또는 기타 기능을 등록하면 안 됩니다.

Artisan CLI를 사용하여 `make:provider` 명령어로 새 프로바이더를 생성할 수 있습니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### Register 메서드

앞서 언급했듯이, `register` 메서드에서는 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩하는 일만 해야 합니다. 이 메서드 안에서 이벤트 리스너, 라우트, 기타 기능을 등록하려 해서는 안 됩니다. 그렇지 않으면, 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 실수로 사용할 수도 있습니다.

아래는 기본적인 서비스 프로바이더의 예입니다. 서비스 프로바이더의 어떤 메서드에서든 `$app` 속성에 접근할 수 있으며, 이 속성을 통해 서비스 컨테이너에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

이 서비스 프로바이더는 오직 `register` 메서드만을 정의하고, 이 메서드를 사용해 서비스 컨테이너에 `App\Services\Riak\Connection`의 구현체를 바인딩합니다. Laravel의 서비스 컨테이너에 익숙하지 않다면, [서비스 컨테이너 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings`와 `singletons` 속성

여러 개의 단순한 바인딩을 서비스 프로바이더에 등록해야 하는 경우, 각 컨테이너 바인딩을 수동으로 등록하는 대신 `bindings`와 `singletons` 속성을 사용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때, 이 속성들을 자동으로 확인하고 바인딩을 등록합니다:

```php
<?php

namespace App\Providers;

use App\Contracts\DowntimeNotifier;
use App\Contracts\ServerProvider;
use App\Services\DigitalOceanServerProvider;
use App\Services\PingdomDowntimeNotifier;
use App\Services\ServerToolsProvider;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 등록되어야 할 모든 컨테이너 바인딩
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록되어야 할 모든 컨테이너 싱글턴
     *
     * @var array
     */
    public $singletons = [
        DowntimeNotifier::class => PingdomDowntimeNotifier::class,
        ServerProvider::class => ServerToolsProvider::class,
    ];
}
```

<a name="the-boot-method"></a>
### Boot 메서드

서비스 프로바이더 내에서 [뷰 컴포저](/docs/{{version}}/views#view-composers)를 등록해야 한다면 어떻게 해야 할까요? 이는 `boot` 메서드에서 처리해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더가 등록된 이후에 호출되므로**, 프레임워크에서 등록한 모든 서비스에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::composer('view', function () {
            // ...
        });
    }
}
```

<a name="boot-method-dependency-injection"></a>
#### Boot 메서드 의존성 주입

서비스 프로바이더의 `boot` 메서드에 의존성을 타입힌트로 지정할 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)가 필요한 모든 의존성을 자동으로 주입해줍니다:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
## 프로바이더 등록

모든 서비스 프로바이더는 `config/app.php` 설정 파일에 등록됩니다. 이 파일에는 여러분의 서비스 프로바이더 클래스 이름을 나열할 수 있는 `providers` 배열이 있습니다. 기본적으로 이 배열에는 Laravel의 핵심 서비스 프로바이더들이 포함되어 있습니다. 기본 프로바이더들은 메일러, 큐, 캐시 등과 같은 Laravel의 핵심 컴포넌트들을 부트스트랩합니다.

프로바이더를 등록하려면 배열에 추가하세요:

```php
'providers' => ServiceProvider::defaultProviders()->merge([
    // Other Service Providers

    App\Providers\ComposerServiceProvider::class,
])->toArray(),
```

<a name="deferred-providers"></a>
## 지연(Deferred) 프로바이더

프로바이더가 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만을 등록한다면, 등록된 바인딩 중 하나가 실제로 필요할 때까지 로드를 지연시킬 수 있습니다. 이런 방식을 사용하면 서비스가 매 요청마다 파일 시스템에서 로드되지 않으므로 애플리케이션의 성능이 향상됩니다.

Laravel은 지연 서비스 프로바이더가 제공하는 모든 서비스의 목록과 서비스 프로바이더 클래스 이름을 컴파일하여 저장합니다. 그런 다음, 해당 서비스 중 하나를 해결하려고 할 때에만 Laravel이 서비스 프로바이더를 로드합니다.

프로바이더의 로드를 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 합니다. `provides` 메서드는 프로바이더가 등록하는 서비스 컨테이너 바인딩을 반환해야 합니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```
