# 서비스 프로바이더

- [소개](#introduction)
- [서비스 프로바이더 작성](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록](#registering-providers)
- [지연 로딩 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션의 부트스트래핑(시작 설정)이 이루어지는 중심지입니다. 여러분이 작성하는 애플리케이션과 Laravel의 핵심 서비스 모두 서비스 프로바이더를 통해 부트스트랩됩니다.

여기서 "부트스트랩"이란 무엇을 의미할까요? 일반적으로 **등록**(register)한다는 의미로, 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트 등 다양한 것들을 등록하는 작업을 포함합니다. 즉, 서비스 프로바이더는 애플리케이션을 구성하는 중심이 되는 곳입니다.

Laravel은 내부적으로 메일러, 큐, 캐시 등과 같은 핵심 서비스를 부트스트랩하기 위해 수십 개의 서비스 프로바이더를 사용합니다. 이 중 다수는 "지연 로딩(deferred)" 프로바이더로, 매 요청마다 로드되지 않고 해당 서비스가 실제로 필요할 때만 로드됩니다.

사용자가 정의한 모든 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 다음 문서에서는 서비스 프로바이더를 작성하는 방법과 Laravel 애플리케이션에 등록하는 방법을 배울 수 있습니다.

> [!NOTE]  
> Laravel이 요청을 처리하는 방식과 내부적으로 동작하는 방식에 대해 더 알고 싶다면 Laravel [요청 생명주기](/docs/{{version}}/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장(extends)합니다. 대부분의 서비스 프로바이더에는 `register`와 `boot` 두 메서드가 포함되어 있습니다. `register` 메서드 내에서는 **[서비스 컨테이너](/docs/{{version}}/container)에 오직 바인딩만** 해야 합니다. 이벤트 리스너, 라우트, 또는 기타 기능은 `register`에서 등록하지 않아야 합니다.

새로운 프로바이더는 Artisan CLI의 `make:provider` 명령어로 생성할 수 있습니다. Laravel은 새로 생성된 프로바이더를 `bootstrap/providers.php` 파일에 자동으로 등록해줍니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 설명했듯이, `register` 메서드 안에서는 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 해야 하며, 이벤트 리스너나 라우트, 기타 다른 기능은 등록하지 않아야 합니다. 그렇지 않으면 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 실수로 사용할 수 있습니다.

기본적인 서비스 프로바이더 예시를 살펴보겠습니다. 서비스 프로바이더의 어떤 메서드에서도 `$app` 프로퍼티를 통해 서비스 컨테이너에 접근할 수 있습니다:

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

이 서비스 프로바이더는 오직 `register` 메서드만 정의하며, 이 메서드 안에서 서비스 컨테이너에 `App\Services\Riak\Connection` 구현체를 등록하고 있습니다. Laravel의 서비스 컨테이너에 익숙하지 않으시다면 [관련 문서](/docs/{{version}}/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 프로퍼티

여러 개의 단순한 바인딩을 등록해야 한다면, 각각을 수동으로 등록하는 대신 `bindings`와 `singletons` 프로퍼티를 사용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때 이들 프로퍼티가 있는지 자동으로 확인하고 바인딩을 등록합니다:

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
         * 등록해야 할 모든 컨테이너 바인딩
         *
         * @var array
         */
        public $bindings = [
            ServerProvider::class => DigitalOceanServerProvider::class,
        ];

        /**
         * 등록해야 할 모든 컨테이너 싱글톤
         *
         * @var array
         */
        public $singletons = [
            DowntimeNotifier::class => PingdomDowntimeNotifier::class,
            ServerProvider::class => ServerToolsProvider::class,
        ];
    }

<a name="the-boot-method"></a>
### boot 메서드

그렇다면 서비스 프로바이더 안에서 [뷰 컴포저](/docs/{{version}}/views#view-composers)를 등록해야 한다면 어떻게 해야 할까요? 이 경우에는 `boot` 메서드에서 처리해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더가 등록된 이후에 호출**되므로 프레임워크에 등록된 모든 서비스에 접근할 수 있습니다:

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

<a name="boot-method-dependency-injection"></a>
#### boot 메서드 의존성 주입

서비스 프로바이더의 `boot` 메서드에서 의존성을 타입힌트로 명시할 수 있습니다. 그러면 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 필요한 의존성을 주입해줍니다:

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

<a name="registering-providers"></a>
## 프로바이더 등록

모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에 등록됩니다. 이 파일은 애플리케이션의 서비스 프로바이더 클래스명을 포함하는 배열을 반환합니다:

    <?php

    return [
        App\Providers\AppServiceProvider::class,
    ];

`make:provider` Artisan 명령어를 실행하면 Laravel이 자동으로 생성된 프로바이더를 `bootstrap/providers.php` 파일에 추가합니다. 하지만 프로바이더 클래스를 수동으로 작성했다면 직접 배열에 추가해줘야 합니다:

    <?php

    return [
        App\Providers\AppServiceProvider::class,
        App\Providers\ComposerServiceProvider::class, // [tl! add]
    ];

<a name="deferred-providers"></a>
## 지연 로딩 프로바이더

프로바이더가 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 **오직** 등록한다면, 해당 바인딩이 실제로 필요할 때까지 프로바이더의 등록을 지연할 수 있습니다. 이렇게 하면 매 요청마다 파일시스템에서 로드하지 않아도 되기 때문에 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 프로바이더가 제공하는 모든 서비스 목록과 프로바이더 클래스명을 컴파일해서 저장합니다. 그리고 해당 서비스 중 하나를 해결하려고 할 때만 서비스 프로바이더를 로드합니다.

프로바이더의 로딩을 지연하려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고, `provides` 메서드를 정의해야 합니다. `provides` 메서드는 해당 프로바이더에서 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다:

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
