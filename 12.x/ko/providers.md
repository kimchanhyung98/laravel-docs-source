# 서비스 프로바이더

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [Register 메서드](#the-register-method)
    - [Boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연(Deferred) 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션의 부트스트래핑(시동)을 담당하는 핵심 역할을 합니다. 여러분의 애플리케이션뿐만 아니라, Laravel의 코어 서비스들 역시 서비스 프로바이더를 통해 부트스트랩됩니다.

여기서 "부트스트랩한다"는 것은 무엇을 의미할까요? 일반적으로 이것은 **등록(등록)**하는 모든 작업을 의미합니다. 예를 들어, 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트의 등록 등이 있습니다. 서비스 프로바이더는 이러한 애플리케이션 설정의 중심지가 됩니다.

Laravel 내부적으로는 메일러, 큐, 캐시 등과 같은 코어 서비스를 부트스트랩하기 위해 수십 개의 서비스 프로바이더를 사용합니다. 이들 중 다수는 "지연(Deferred)" 프로바이더로, 이들이 제공하는 서비스가 실제로 필요할 때만 로드되고, 모든 요청마다 로드되지는 않습니다.

모든 사용자 정의 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 이후의 문서에서는 자체 서비스 프로바이더를 작성하고 Laravel 애플리케이션에 등록하는 방법을 배우게 됩니다.

> [!NOTE]
> Laravel이 어떻게 요청을 처리하고 내부적으로 동작하는지 더 알아보고 싶다면, Laravel [요청 라이프사이클](/docs/{{version}}/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 포함합니다. `register` 메서드 내에서는 **[서비스 컨테이너](/docs/{{version}}/container)에 오직 바인딩만** 해야 합니다. `register` 메서드 내에서는 이벤트 리스너, 라우트 등 다른 기능들은 등록해서는 안 됩니다.

Artisan CLI를 통해 `make:provider` 명령어로 새로운 프로바이더를 생성할 수 있습니다. Laravel은 자동으로 이 프로바이더를 `bootstrap/providers.php` 파일에 등록합니다.

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### Register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 해야 합니다. 이벤트 리스너, 라우트, 기타 기능을 이 메서드 안에서 등록하면 안 됩니다. 그렇지 않으면 아직 로드되지 않은 서비스 프로바이더에 의존하는 서비스를 실수로 사용할 수 있습니다.

아래는 기본적인 서비스 프로바이더 예시입니다. 서비스 프로바이더의 모든 메서드 내에서 항상 `$app` 프로퍼티를 사용할 수 있으며, 이를 통해 서비스 컨테이너에 접근할 수 있습니다.

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

이 서비스 프로바이더는 `register` 메서드만을 정의하고, 해당 메서드에서 `App\Services\Riak\Connection`의 구현체를 서비스 컨테이너에 바인딩합니다. Laravel의 서비스 컨테이너에 익숙하지 않다면 [관련 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings`와 `singletons` 프로퍼티

여러 개의 단순한 바인딩을 서비스 프로바이더에서 등록해야 한다면, 각 바인딩을 개별적으로 등록하는 대신 `bindings` 및 `singletons` 프로퍼티를 활용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때, 이 프로퍼티들을 자동으로 확인해 바인딩을 등록합니다.

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
     * 등록할 컨테이너 바인딩 전체 목록
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 컨테이너 싱글톤 전체 목록
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

서비스 프로바이더 내에서 [뷰 컴포저](/docs/{{version}}/views#view-composers)와 같은 기능을 등록해야 하는 경우가 있을 수 있습니다. 이런 작업은 `boot` 메서드 내에서 처리해야 합니다. **이 메서드는 모든 서비스 프로바이더가 등록된 후에 호출**되므로, 프레임워크에 의해 등록된 모든 서비스에 접근할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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

서비스 프로바이더의 `boot` 메서드에서 타입힌트를 통해 의존성을 주입할 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)는 필요한 모든 의존성을 자동으로 주입해줍니다.

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
## 프로바이더 등록하기

모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에 등록되어 있습니다. 이 파일은 애플리케이션의 서비스 프로바이더 클래스 이름들의 배열을 반환합니다.

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

`make:provider` Artisan 명령어를 실행하면, Laravel이 자동으로 새로 만들어진 프로바이더를 `bootstrap/providers.php` 파일에 추가합니다. 만약 직접 클래스 파일을 만든 경우, 배열에 직접 프로바이더 클래스를 추가해야 합니다.

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## 지연(Deferred) 프로바이더

프로바이더가 오직 [서비스 컨테이너](/docs/{{version}}/container) 바인딩만을 등록한다면, 이러한 프로바이더의 등록을 바인딩이 실제로 필요해질 때까지 지연(defer)할 수 있습니다. 이러한 프로바이더를 지연 로드하면, 매 요청마다 파일 시스템에서 불러오는 작업이 없어 애플리케이션의 성능이 향상됩니다.

Laravel은 지연 서비스 프로바이더가 제공하는 서비스 이름과 해당 서비스 프로바이더 클래스의 리스트를 컴파일하여 저장합니다. 그런 다음 이러한 서비스 중 하나를 해석(resolve)하려 할 때만 Laravel이 해당 서비스 프로바이더를 불러옵니다.

프로바이더의 로드를 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고, `provides` 메서드를 정의해야 합니다. `provides` 메서드는 해당 프로바이더에서 등록한 서비스 컨테이너 바인딩을 반환해야 합니다.

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
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * 프로바이더가 제공하는 서비스 목록을 반환합니다.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```