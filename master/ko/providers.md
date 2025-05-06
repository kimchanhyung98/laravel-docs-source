# 서비스 프로바이더

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [Register 메소드](#the-register-method)
    - [Boot 메소드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션의 부트스트랩 과정의 중심입니다. 여러분의 애플리케이션뿐만 아니라, Laravel의 핵심 서비스들 또한 서비스 프로바이더를 통해 부트스트랩 됩니다.

그렇다면 "부트스트랩"이란 무엇일까요? 일반적으로 부트스트랩이란 **각종 요소를 등록하는 것**을 의미합니다. 여기에는 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 그리고 라우트 등록도 포함됩니다. 서비스 프로바이더는 애플리케이션을 설정하는 중심적인 위치입니다.

Laravel은 메일러, 큐, 캐시 등과 같은 핵심 서비스를 부트스트랩하기 위해 내부적으로 수십 개의 서비스 프로바이더를 사용합니다. 이들 대부분은 "지연(deferred)" 프로바이더로, 제공하는 서비스가 실제로 필요할 때에만 로드되며, 모든 요청마다 항상 로드되지는 않습니다.

모든 사용자 정의 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 아래 문서에서는 여러분만의 서비스 프로바이더를 작성하고 이를 Laravel 애플리케이션에 등록하는 방법을 배울 수 있습니다.

> [!NOTE]
> Laravel이 요청을 처리하는 방식과 내부적으로 어떻게 동작하는지 더 알고 싶다면, Laravel [요청 라이프사이클](/docs/{{version}}/lifecycle)에 관한 문서를 참조하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 프로바이더는 `register` 메소드와 `boot` 메소드를 포함합니다. `register` 메소드에서는 **오직 [서비스 컨테이너](/docs/{{version}}/container)에만 바인딩을 등록**해야 합니다. 이 메소드 안에서는 이벤트 리스너, 라우트, 또는 기타 기능 등록을 해서는 안 됩니다.

Artisan CLI의 `make:provider` 명령어를 사용하면 새로운 프로바이더를 생성할 수 있습니다. Laravel은 자동으로 새 프로바이더를 애플리케이션의 `bootstrap/providers.php` 파일에 등록합니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### Register 메소드

앞서 언급했듯이, `register` 메소드 내부에서는 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록해야 합니다. 이벤트 리스너, 라우트, 또는 다른 어떤 기능도 이곳에서 등록해서는 안 됩니다. 만약 그렇게 할 경우, 아직 로드되지 않은 서비스 프로바이더에서 제공하는 서비스를 실수로 사용할 수 있습니다.

다음은 기본적인 서비스 프로바이더 예시입니다. 서비스 프로바이더의 모든 메소드 내에서는 서비스 컨테이너에 접근할 수 있는 `$app` 프로퍼티를 사용할 수 있습니다:

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

이 서비스 프로바이더는 오직 `register` 메소드만 정의되어 있으며, 이 메소드에서는 서비스 컨테이너에 `App\Services\Riak\Connection`의 구현을 등록합니다. 아직 Laravel의 서비스 컨테이너가 익숙하지 않다면 [관련 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 프로퍼티

여러 개의 간단한 바인딩을 서비스 프로바이더에서 등록해야 하는 경우, 각 컨테이너 바인딩을 수동으로 등록하는 대신 `bindings` 및 `singletons` 프로퍼티를 사용할 수 있습니다. 서비스 프로바이더가 프레임워크에 의해 로드될 때, 이 프로퍼티를 자동으로 확인하여 바인딩을 등록합니다:

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
     * 등록할 모든 컨테이너 바인딩
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글턴
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
### Boot 메소드

그렇다면, [뷰 컴포저](/docs/{{version}}/views#view-composers)를 서비스 프로바이더에서 등록해야 할 경우는 어떻게 해야 할까요? 이 경우에는 `boot` 메소드에서 등록해야 합니다. **이 메소드는 다른 모든 서비스 프로바이더가 등록된 후에 호출**되므로, 프레임워크에서 등록된 모든 서비스에 접근할 수 있습니다:

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
#### Boot 메소드 의존성 주입

서비스 프로바이더의 `boot` 메소드에 타입힌트를 지정하여 의존성을 주입받을 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)가 필요한 의존성을 자동으로 주입해줍니다:

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

모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에 등록됩니다. 이 파일은 애플리케이션의 서비스 프로바이더 클래스명을 담고 있는 배열을 반환합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

`make:provider` Artisan 명령어를 실행하면, Laravel은 자동으로 생성된 프로바이더를 `bootstrap/providers.php` 파일에 추가합니다. 하지만 직접 프로바이더 클래스를 생성한 경우에는 수동으로 해당 클래스를 배열에 추가해야 합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## 지연 프로바이더

만약 여러분의 프로바이더가 **오직** [서비스 컨테이너](/docs/{{version}}/container) 안에 바인딩만 등록한다면, 실제로 등록된 바인딩이 필요할 때까지 그 등록을 지연시킬 수 있습니다. 이런 프로바이더의 로드를 지연시키면, 파일 시스템에서 매 요청마다 로드되지 않으므로 애플리케이션의 성능이 향상됩니다.

Laravel은 지연 서비스 프로바이더가 제공하는 모든 서비스 목록과 그 서비스 프로바이더 클래스명을 컴파일하여 저장합니다. 그리고 이러한 서비스 중 하나를 해석(resolving)하려고 할 때에만 해당 서비스 프로바이더를 불러옵니다.

프로바이더의 로드를 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메소드를 정의해야 합니다. `provides` 메소드는 프로바이더가 등록한 서비스 컨테이너 바인딩을 반환해야 합니다:

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