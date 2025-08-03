# 서비스 프로바이더 (Service Providers)

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 로딩 프로바이더(Deferred Providers)](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 Laravel 애플리케이션 부트스트래핑(초기화) 과정의 핵심 위치입니다. 여러분의 애플리케이션뿐 아니라 Laravel의 모든 코어 서비스도 서비스 프로바이더를 통해 부트스트래핑됩니다.

그렇다면 "부트스트래핑(bootstrapped)"이란 무엇을 의미할까요? 일반적으로 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어 그리고 라우트까지 **등록(register)** 하는 과정을 뜻합니다. 서비스 프로바이더는 애플리케이션을 설정하는 중심 역할을 합니다.

Laravel에 기본 포함된 `config/app.php` 파일을 열어보면 `providers` 배열을 찾을 수 있습니다. 이 배열은 애플리케이션에 로드될 모든 서비스 프로바이더 클래스들을 나열합니다. 기본적으로 Laravel 코어 서비스 프로바이더 일부가 선언되어 있으며, 이 프로바이더들은 메일러, 큐, 캐시 등 Laravel의 핵심 컴포넌트를 부트스트래핑합니다. 많은 프로바이더는 "지연 로딩(deferred)" 프로바이더로, 매 요청마다 로드되지 않고 필요한 서비스가 실제로 호출될 때에만 로드됩니다.

이 문서에서는 서비스 프로바이더를 직접 작성하고 Laravel 애플리케이션에 등록하는 방법을 배우게 됩니다.

> [!NOTE]  
> Laravel이 요청을 처리하고 내부적으로 어떻게 동작하는지 더 알고 싶다면, Laravel [요청 주기(Request Lifecycle)](/docs/10.x/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 프로바이더는 `register` 메서드와 `boot` 메서드를 포함합니다. 

`register` 메서드 내에서는 **서비스 컨테이너에만 바인딩(binding)해야 하며**, 절대 이벤트 리스너, 라우트, 다른 기능을 등록하지 말아야 합니다.

Artisan CLI를 이용하면 `make:provider` 명령어로 새 프로바이더를 생성할 수 있습니다.

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 안에서는 서비스 컨테이너에만 바인딩해야 하며, 이벤트 리스너나 라우트 등의 기능을 등록하지 않아야 합니다. 그렇지 않으면, 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 사용하려다가 오류가 발생할 수 있습니다.

가장 기본적인 서비스 프로바이더 예제를 살펴봅시다. 어떤 서비스 프로바이더 메서드든 `$app` 속성에 접근할 수 있으며, `$app`은 서비스 컨테이너에 접근할 수 있게 해줍니다.

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

위 서비스 프로바이더는 `register` 메서드만 정의하여, `App\Services\Riak\Connection`을 서비스 컨테이너에 싱글톤으로 등록하고 있습니다. Laravel 서비스 컨테이너에 익숙하지 않다면 [공식 문서](/docs/10.x/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### bindings와 singletons 속성

서비스 프로바이더에서 다수의 단순 바인딩을 등록해야 한다면, 매번 수동으로 등록하는 대신 `bindings`와 `singletons` 속성을 활용할 수 있습니다. 프레임워크가 로드될 때 이 속성들을 자동으로 확인하고 바인딩을 등록해 줍니다.

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
     * 등록할 모든 컨테이너 바인딩들.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글톤들.
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

그렇다면 서비스 프로바이더 내에서 [뷰 컴포저(view composer)](/docs/10.x/views#view-composers)를 등록하고 싶으면 어떻게 해야 할까요? 이 경우 `boot` 메서드 안에서 처리해야 합니다. 

`boot` 메서드는 **모든 서비스 프로바이더가 등록된 이후 호출되므로**, 프레임워크에 의해 등록된 모든 서비스에 접근할 수 있습니다.

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
#### boot 메서드 의존성 주입

서비스 프로바이더의 `boot` 메서드에 의존성 주입을 받을 수도 있습니다. 서비스 컨테이너가 필요한 모든 의존성을 자동으로 주입해 줍니다.

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

모든 서비스 프로바이더는 `config/app.php` 설정 파일 내 `providers` 배열에 등록합니다. 이 배열에 서비스 프로바이더 클래스 이름을 나열하면 됩니다. 기본적으로 Laravel 코어 서비스 프로바이더들이 이미 등록되어 있으며, 이들이 메일러, 큐, 캐시 등 핵심 컴포넌트를 부트스트래핑합니다.

사용자 정의 프로바이더는 아래처럼 배열에 추가하세요:

```php
'providers' => ServiceProvider::defaultProviders()->merge([
    // 기타 서비스 프로바이더들

    App\Providers\ComposerServiceProvider::class,
])->toArray(),
```

<a name="deferred-providers"></a>
## 지연 로딩 프로바이더(Deferred Providers)

프로바이더가 **오직 서비스 컨테이너 바인딩만 등록한다면**, 실제 해당 바인딩 중 하나가 사용될 때까지 프로바이더의 등록을 미룰 수 있습니다. 이렇게 하면 매 요청마다 파일 시스템에서 프로바이더를 로드하지 않아도 되어 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 프로바이더가 제공하는 서비스 목록과 프로바이더 클래스를 컴파일하여 저장합니다. 이후 이 서비스들 중 하나를 해석(resolve)하려 시도할 때 해당 프로바이더를 로드합니다.

프로바이더를 지연 로딩하려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 하며, `provides`는 해당 프로바이더가 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다.

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