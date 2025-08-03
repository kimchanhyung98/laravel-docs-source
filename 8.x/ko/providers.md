# 서비스 프로바이더 (Service Providers)

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 로딩(Deferred) 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션 부트스트래핑의 중심입니다. 여러분의 애플리케이션뿐만 아니라 Laravel 핵심 서비스들 역시 모두 서비스 프로바이더를 통해 부트스트랩됩니다.

그렇다면 "부트스트랩(bootstrapped)"이란 무엇을 의미할까요? 일반적으로, 서비스 컨테이너 바인딩 등록, 이벤트 리스너, 미들웨어, 심지어 라우트 등 다양한 기능을 **등록(register)** 하는 것을 의미합니다. 서비스 프로바이더는 애플리케이션을 구성하는 중심적인 위치입니다.

`config/app.php` 파일을 열면 `providers` 배열을 볼 수 있습니다. 이 배열은 애플리케이션 실행 시 로드될 모든 서비스 프로바이더 클래스들을 나열합니다. 기본적으로 Laravel 핵심 서비스 프로바이더들이 여기에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등 Laravel 핵심 컴포넌트를 부트스트랩합니다. 그리고 많은 프로바이더가 "지연 로딩(deferred)" 프로바이더여서, 매 요청마다 로드되지 않고 실제로 해당 서비스가 필요할 때만 로드됩니다.

이 문서에서는 여러분이 직접 서비스 프로바이더를 작성하고 Laravel 애플리케이션에 등록하는 방법을 배울 수 있습니다.

> [!TIP]
> Laravel이 요청을 처리하고 내부적으로 작동하는 방식을 더 깊이 이해하고 싶다면 Laravel [요청 수명주기(request lifecycle)](/docs/{{version}}/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속받습니다. 대부분의 프로바이더는 `register` 메서드와 `boot` 메서드를 가집니다. `register` 메서드 내에서는 **오직 [서비스 컨테이너](/docs/{{version}}/container)에만 바인딩을 등록해야** 하며, 이벤트 리스너, 라우트, 기타 기능들을 이 메서드에서 등록해서는 안 됩니다.

Artisan CLI를 사용하면 `make:provider` 명령어로 새 프로바이더를 생성할 수 있습니다:

```
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 반드시 [서비스 컨테이너](/docs/{{version}}/container)에만 바인딩을 등록해야 합니다. 이벤트 리스너, 라우트, 기타 기능을 여기서 등록하면, 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 잘못 사용하게 되어 문제가 발생할 수 있습니다.

다음은 기본적인 서비스 프로바이더 예제입니다. 모든 서비스 프로바이더 안에서 `$app` 속성을 통해 서비스 컨테이너에 접근할 수 있습니다:

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
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

이 서비스 프로바이더는 `register` 메서드만 정의하며, 이 메서드 안에서 `App\Services\Riak\Connection` 구현체를 서비스 컨테이너에 싱글톤으로 등록합니다. Laravel 서비스 컨테이너에 익숙하지 않은 경우 [공식 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### bindings 및 singletons 속성

많은 단순 바인딩을 프로바이더에서 등록해야 하는 경우, 각 바인딩을 수동으로 등록하는 대신 `bindings` 와 `singletons` 속성을 사용할 수 있습니다. 프레임워크가 프로바이더를 로드할 때 이러한 속성을 자동으로 확인하고 바인딩을 등록합니다:

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
     * 등록할 모든 컨테이너 바인딩.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글톤.
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

그렇다면 서비스 프로바이더 내에서 [뷰 컴포저(view composer)](/docs/{{version}}/views#view-composers) 같은 것을 등록하려면 어떻게 할까요? 이런 작업은 `boot` 메서드에서 해야 합니다. **`boot` 메서드는 모든 다른 서비스 프로바이더가 등록된 이후에 호출되므로**, 프레임워크가 등록한 모든 서비스를 사용할 수 있는 시점입니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
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
#### boot 메서드 의존성 주입

서비스 프로바이더의 `boot` 메서드는 필요한 의존성을 타입 힌트로 받을 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 의존성을 주입해줍니다:

```
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
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

모든 서비스 프로바이더는 `config/app.php` 구성 파일에 등록됩니다. 이 파일 안의 `providers` 배열에 서비스 프로바이더 클래스 이름을 나열합니다. 기본적으로 Laravel 핵심 서비스 프로바이더들이 이미 이 배열에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등 핵심 컴포넌트를 부트스트랩합니다.

자신의 프로바이더를 등록하려면 배열에 추가하면 됩니다:

```
'providers' => [
    // 기타 서비스 프로바이더

    App\Providers\ComposerServiceProvider::class,
],
```

<a name="deferred-providers"></a>
## 지연 로딩(Deferred) 프로바이더

여러분의 프로바이더가 **오직** [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록한다면, 등록을 해당 바인딩이 실제로 필요할 때까지 지연시킬 수 있습니다. 이렇게 하면 매 요청마다 파일시스템에서 프로바이더를 불러오지 않아도 되어 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 프로바이더가 제공하는 서비스 목록과 프로바이더 클래스 이름을 컴파일해 저장합니다. 그리고 이 서비스 중 하나를 실제로 해결하려 할 때만 해당 프로바이더를 로드합니다.

지연 로딩 프로바이더를 만들려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 합니다. `provides` 메서드는 프로바이더가 등록하는 서비스 컨테이너 바인딩을 배열로 반환해야 합니다:

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
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
     * 이 프로바이더가 제공하는 서비스들 반환.
     *
     * @return array
     */
    public function provides()
    {
        return [Connection::class];
    }
}
```