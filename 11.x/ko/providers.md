# 서비스 제공자 (Service Providers)

- [소개](#introduction)
- [서비스 제공자 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [서비스 제공자 등록하기](#registering-providers)
- [지연 제공자 (Deferred Providers)](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 제공자는 모든 Laravel 애플리케이션 부트스트래핑의 중심입니다. 여러분의 애플리케이션뿐만 아니라 Laravel의 모든 핵심 서비스도 서비스 제공자를 통해 부트스트랩됩니다.

그렇다면 여기서 "부트스트랩"이란 무엇을 의미할까요? 일반적으로 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 심지어는 라우트까지 포함하여 **등록하는 것**을 의미합니다. 서비스 제공자는 애플리케이션을 설정하는 중심 장소입니다.

Laravel은 메일러, 큐, 캐시 등 핵심 서비스를 부트스트랩하기 위해 내부적으로 수십 개의 서비스 제공자를 사용합니다. 이들 중 다수는 "지연" 제공자로, 이는 모든 요청에서 항상 로드되는 것이 아니라 제공하는 서비스가 실제로 필요할 때만 로드된다는 뜻입니다.

사용자가 정의한 모든 서비스 제공자는 `bootstrap/providers.php` 파일에 등록됩니다. 이 문서에서는 여러분이 직접 서비스 제공자를 작성하고 Laravel 애플리케이션에 등록하는 방법을 배우게 됩니다.

> [!NOTE]  
> Laravel이 요청을 처리하고 내부적으로 어떻게 작동하는지 더 알고 싶다면, Laravel [요청 수명주기](/docs/11.x/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 제공자 작성하기

모든 서비스 제공자는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 대부분의 서비스 제공자는 `register` 메서드와 `boot` 메서드를 포함합니다. `register` 메서드 안에는 **서비스 컨테이너에 바인딩만 등록해야 합니다**. 이벤트 리스너, 라우트, 기타 기능들을 이 메서드 안에서 등록하려 해서는 안 됩니다.

Artisan CLI의 `make:provider` 명령어를 사용하면 새 서비스 제공자를 생성할 수 있습니다. Laravel은 새로 생성된 제공자를 자동으로 애플리케이션의 `bootstrap/providers.php` 파일에 등록합니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 말했듯이, `register` 메서드 안에서는 서비스 컨테이너에 바인딩만 등록해야 합니다. 이벤트 리스너, 라우트, 또는 다른 기능은 이 메서드에서 등록하려 하지 마세요. 그렇지 않으면 아직 로드되지 않은 서비스 제공자가 제공하는 서비스를 잘못 사용하게 될 수 있습니다.

기본적인 서비스 제공자를 살펴봅시다. 서비스 제공자의 메서드 어디서든 `$app` 속성에 접근할 수 있는데, 이는 서비스 컨테이너에 접근할 수 있게 해줍니다:

```
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

이 서비스 제공자는 `register` 메서드만 정의하고, 여기서 `App\Services\Riak\Connection` 구현을 서비스 컨테이너에 정의합니다. Laravel의 서비스 컨테이너가 아직 익숙하지 않다면 [관련 문서](/docs/11.x/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 속성

여러 개의 간단한 바인딩을 등록해야 할 경우, 각각을 수동으로 등록하기보다 `bindings` 및 `singletons` 속성을 사용하는 것이 더 간편할 수 있습니다. 프레임워크가 서비스 제공자를 로드할 때 이 속성들을 자동으로 검사하여 바인딩들을 등록합니다:

```
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
     * 등록할 모든 컨테이너 바인딩
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글톤
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
### boot 메서드

그렇다면 서비스 제공자 내에서 [뷰 컴포저(View Composer)](/docs/11.x/views#view-composers)를 등록하고 싶다면 어떻게 해야 할까요? 이런 작업은 `boot` 메서드 안에서 수행해야 합니다. **`boot` 메서드는 다른 모든 서비스 제공자가 등록된 후에 호출되므로**, 프레임워크에 의해 등록된 다른 모든 서비스에 접근할 수 있습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
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
#### boot 메서드 의존성 주입

서비스 제공자의 `boot` 메서드에서 타입 힌트를 통해 의존성을 주입받을 수 있습니다. [서비스 컨테이너](/docs/11.x/container)가 필요한 의존성을 자동으로 주입합니다:

```
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
## 서비스 제공자 등록하기

모든 서비스 제공자는 `bootstrap/providers.php` 설정 파일에 등록됩니다. 이 파일은 애플리케이션 서비스 제공자 클래스명들의 배열을 반환합니다:

```
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

`make:provider` Artisan 명령어로 서비스 제공자를 생성하면 Laravel이 자동으로 `bootstrap/providers.php` 파일에 추가합니다. 하지만 클래스 파일을 수동으로 작성한 경우에는 배열에 직접 추가해야 합니다:

```
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## 지연 제공자 (Deferred Providers)

만약 여러분의 서비스 제공자가 서비스 컨테이너에 바인딩만 등록한다면, 실제로 등록된 바인딩 중 하나가 필요해질 때까지 제공자 등록을 지연시킬 수 있습니다. 이런 지연 등록은 요청마다 파일 시스템에서 제공자를 항상 로드하는 비용을 줄여 애플리케이션 성능을 개선합니다.

Laravel은 지연 제공자가 제공하는 모든 서비스와 해당 제공자 클래스명 목록을 컴파일하고 저장합니다. 그리고 여러분이 해당 서비스 중 하나를 해결하려 할 때 비로소 그 서비스 제공자를 로드합니다.

제공자 로드를 지연시키려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 합니다. `provides` 메서드는 서비스 제공자가 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다:

```
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