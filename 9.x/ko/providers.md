# 서비스 프로바이더 (Service Providers)

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 로딩 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션 부트스트래핑의 중심입니다. 여러분이 작성한 애플리케이션뿐 아니라, Laravel의 핵심 서비스들도 서비스 프로바이더를 통해 부트스트래핑됩니다.

그렇다면 "부트스트랩(bootstrapped)"이란 무엇을 의미할까요? 일반적으로 이는 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 그리고 라우트 등록 등 **등록(registering)** 작업을 뜻합니다. 서비스 프로바이더는 애플리케이션을 구성하는 중심 장소입니다.

Laravel과 함께 제공되는 `config/app.php` 파일을 열어보면 `providers` 배열이 있습니다. 이 배열에는 애플리케이션에 로드될 모든 서비스 프로바이더 클래스가 나열되어 있습니다. 기본적으로 Laravel 핵심 서비스 프로바이더 세트가 이 배열에 포함되어 있는데, 이 프로바이더들은 메일러, 큐, 캐시 등과 같은 Laravel 핵심 컴포넌트를 부트스트래핑합니다. 이 중 많은 프로바이더가 "지연 로딩(deferred)" 프로바이더로, 모든 요청마다 로드되지 않고 실제로 그들이 제공하는 서비스가 필요할 때만 로드됩니다.

이 개요에서는 여러분이 직접 서비스 프로바이더를 작성하고, 이를 Laravel 애플리케이션에 등록하는 방법을 배우게 됩니다.

> [!NOTE]  
> Laravel이 요청을 처리하고 내부적으로 작동하는 방식에 대해 더 알고 싶다면, Laravel [요청 생명주기(lifecycle)](/docs/9.x/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속받습니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 포함합니다. `register` 메서드 내에서는 **반드시 [서비스 컨테이너](/docs/9.x/container)에 바인딩만 수행해야 합니다**. 이벤트 리스너, 라우트 등 다른 기능 등록은 절대 `register` 메서드 안에서 시도하면 안 됩니다.

Artisan CLI를 사용하면 `make:provider` 명령어로 새 프로바이더를 생성할 수 있습니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 반드시 [서비스 컨테이너](/docs/9.x/container)에 바인딩 작업만 해야 합니다. 이벤트 리스너, 라우트 또는 다른 기능 등록은 절대 하지 마세요. 그렇지 않으면 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 사용하려다 오류가 발생할 수 있습니다.

기본적인 서비스 프로바이더를 살펴보겠습니다. 서비스 프로바이더 내 모든 메서드에서는 `$app` 속성을 통해 서비스 컨테이너에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션에서 사용할 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(Connection::class, function ($app) {
            return new Connection(config('riak'));
        });
    }
}
```

이 서비스 프로바이더는 `register` 메서드만 정의하며, 이 메서드 내에서 `App\Services\Riak\Connection` 구현체를 서비스 컨테이너에 싱글턴으로 바인딩합니다. Laravel의 서비스 컨테이너가 아직 익숙하지 않다면 [관련 문서](/docs/9.x/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 속성

만약 서비스 프로바이더가 간단한 바인딩을 많이 등록한다면, 각각 바인딩을 수동으로 등록하는 대신 `bindings`와 `singletons` 속성을 활용할 수 있습니다. 프레임워크는 프로바이더가 로드될 때 이 속성들을 자동으로 확인하고, 정의된 바인딩들을 등록해줍니다:

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
     * 등록할 모든 컨테이너 바인딩.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글턴.
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

그렇다면 서비스 프로바이더 내에서 [view composer](/docs/9.x/views#view-composers)를 등록해야 한다면 어떻게 할까요? 이 작업은 `boot` 메서드 안에서 진행해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더가 등록된 후 호출되므로**, 프레임워크가 등록한 모든 서비스를 사용할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션의 서비스 부트스트래핑.
     *
     * @return void
     */
    public function boot()
    {
        View::composer('view', function () {
            //
        });
    }
}
```

<a name="boot-method-dependency-injection"></a>
#### boot 메서드의 의존성 주입

`boot` 메서드에 의존성이 필요한 경우, 타입힌트를 선언할 수 있습니다. [서비스 컨테이너](/docs/9.x/container)가 자동으로 필요한 의존성을 주입해줍니다:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * 애플리케이션 서비스 부트스트래핑.
 *
 * @param  \Illuminate\Contracts\Routing\ResponseFactory  $response
 * @return void
 */
public function boot(ResponseFactory $response)
{
    $response->macro('serialized', function ($value) {
        //
    });
}
```

<a name="registering-providers"></a>
## 프로바이더 등록하기

모든 서비스 프로바이더는 `config/app.php` 설정 파일에서 등록합니다. 이 파일에 있는 `providers` 배열에 서비스 프로바이더 클래스 이름을 나열하면 됩니다. 기본적으로 Laravel 핵심 서비스 프로바이더 세트가 등록되어 있으며, 이들은 메일러, 큐, 캐시 등의 핵심 컴포넌트를 부트스트래핑합니다.

자신의 프로바이더를 등록하려면 배열에 추가하세요:

```php
'providers' => [
    // 기타 서비스 프로바이더들

    App\Providers\ComposerServiceProvider::class,
],
```

<a name="deferred-providers"></a>
## 지연 로딩 프로바이더

만약 프로바이더가 **오직** [서비스 컨테이너](/docs/9.x/container)에 바인딩만 등록한다면, 해당 바인딩 중 하나가 실제로 필요해질 때까지 등록을 미룰 수 있습니다. 프로바이더의 로딩을 지연시키면, 매 요청마다 파일 시스템에서 불필요하게 로드하지 않기 때문에 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 프로바이더가 제공하는 서비스 목록과 각각의 프로바이더 클래스명을 컴파일하여 저장합니다. 그리고 여러분이 이 서비스 중 하나를 해결(resolving)하려 시도할 때만 해당 프로바이더를 로드합니다.

프로바이더 로딩을 지연시키려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고, `provides` 메서드를 정의하세요. `provides` 메서드는 프로바이더가 등록하는 서비스 컨테이너 바인딩들을 배열로 반환해야 합니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(Connection::class, function ($app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * 프로바이더가 제공하는 서비스 반환.
     *
     * @return array
     */
    public function provides()
    {
        return [Connection::class];
    }
}
```