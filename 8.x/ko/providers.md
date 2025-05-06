# 서비스 제공자(Service Providers)

- [소개](#introduction)
- [서비스 제공자 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [서비스 제공자 등록하기](#registering-providers)
- [지연 로딩 제공자](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 제공자는 모든 Laravel 애플리케이션 부트스트래핑의 중심입니다. 여러분의 애플리케이션은 물론, Laravel의 모든 핵심 서비스들도 서비스 제공자를 통해 부트스트랩됩니다.

그런데 여기서 "부트스트랩"이란 무엇을 의미할까요? 일반적으로, **등록(Registration)** 을 의미합니다. 여기에는 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 그리고 라우트까지의 등록이 포함됩니다. 즉, 서비스 제공자는 애플리케이션을 구성하는 중심 공간입니다.

Laravel에 포함된 `config/app.php` 파일을 열어보면 `providers` 배열이 있습니다. 이 배열에는 애플리케이션에 로드될 서비스 제공자 클래스들이 나열되어 있습니다. 기본적으로, Laravel의 핵심 서비스 제공자들이 이 배열에 포함되어 있습니다. 이 제공자들은 메일러, 큐, 캐시 등과 같은 Laravel의 핵심 컴포넌트들을 부트스트랩합니다. 이들 중 다수는 "지연 로딩(deferred)" 제공자입니다. 즉, 이 제공자들은 매 요청마다 로드되는 것이 아니라, 해당 서비스가 실제로 필요할 때에만 로드됩니다.

이번 개요에서는 여러분만의 서비스 제공자를 작성하고, 이를 Laravel 애플리케이션에 등록하는 방법을 배웁니다.

> {tip} Laravel이 요청을 어떻게 처리하고 내부적으로 어떻게 동작하는지 더 알고 싶다면, [요청 생명주기](/docs/{{version}}/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 제공자 작성하기

모든 서비스 제공자는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 대부분의 서비스 제공자는 `register`와 `boot` 메서드를 가집니다. `register` 메서드 내에서는 **오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록** 해야 합니다. 이벤트 리스너, 라우트, 기타 기능적인 요소를 이 메서드 내에서 등록해서는 안 됩니다.

Artisan CLI를 통해 `make:provider` 명령어로 새 서비스 제공자를 생성할 수 있습니다:

    php artisan make:provider RiakServiceProvider

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록해야 합니다. 이 메서드에서 이벤트 리스너, 라우트, 기타 기능을 등록하는 것은 피해야 합니다. 그렇지 않으면, 아직 로드되지 않은 서비스 제공자가 제공하는 서비스를 실수로 사용할 수 있기 때문입니다.

기본적인 서비스 제공자의 예시를 살펴봅시다. 서비스 제공자의 모든 메서드에서 `$app` 속성에 접근 가능하며, 이를 통해 서비스 컨테이너에 접근할 수 있습니다:

```php
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

이 서비스 제공자는 `register` 메서드만 정의하고 있으며, 해당 메서드에서 서비스 컨테이너 내에 `App\Services\Riak\Connection`의 구현을 정의합니다. Laravel의 서비스 컨테이너에 익숙하지 않다면, [서비스 컨테이너 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings`와 `singletons` 프로퍼티

여러 개의 단순한 바인딩을 서비스 제공자에서 등록해야 한다면, 각각을 직접 등록하는 대신 `bindings`와 `singletons` 속성을 사용할 수 있습니다. 프레임워크가 서비스 제공자를 로드할 때, 이 두 프로퍼티를 자동으로 확인하여 바인딩을 등록해줍니다:

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

서비스 제공자에서 [뷰 컴포저(View Composer)](/docs/{{version}}/views#view-composers)를 등록해야 하는 경우는 어떻게 해야 할까요? 이런 동작은 `boot` 메서드에서 수행해야 합니다. **이 메서드는 다른 모든 서비스 제공자가 등록된 뒤에 호출** 되므로, 프레임워크에 의해 등록된 모든 서비스에 접근할 수 있습니다:

```php
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
#### Boot 메서드 의존성 주입

서비스 제공자의 `boot` 메서드에 의존성을 타입힌트로 지정할 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)는 필요한 의존성을 자동으로 주입해줍니다:

```php
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
## 서비스 제공자 등록하기

모든 서비스 제공자는 `config/app.php` 설정 파일에 등록합니다. 이 파일의 `providers` 배열에 서비스 제공자 클래스명을 나열할 수 있습니다. 기본적으로 이 배열에는 여러 Laravel 핵심 서비스 제공자가 포함되어 있으며, 이 제공자들이 메일러, 큐, 캐시 등 Laravel의 핵심 컴포넌트를 부트스트랩합니다.

자신의 제공자를 등록하려면, 배열에 추가하세요:

```php
'providers' => [
    // 다른 서비스 제공자

    App\Providers\ComposerServiceProvider::class,
],
```

<a name="deferred-providers"></a>
## 지연 로딩 제공자(Deferred Providers)

만약 여러분의 서비스 제공자가 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록한다면, 해당 바인딩이 실제로 필요할 때까지 등록을 지연시킬 수 있습니다. 이렇게 하면 매 요청마다 파일시스템에서 로드하지 않아도 되므로, 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 서비스 제공자들이 제공하는 모든 서비스와 서비스 제공자 클래스명을 컴파일하여 저장합니다. 그리고 해당 서비스를 해결해야 할 때에만 해당 서비스 제공자를 로드합니다.

지연 로딩 제공자로 지정하려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 합니다. `provides` 메서드는 제공자가 등록하는 서비스 컨테이너 바인딩을 반환해야 합니다:

```php
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
     * Get the services provided by the provider.
     *
     * @return array
     */
    public function provides()
    {
        return [Connection::class];
    }
}
```
