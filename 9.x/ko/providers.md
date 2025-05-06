# 서비스 프로바이더

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [Register 메서드](#the-register-method)
    - [Boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연(Deferred) 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션 부트스트래핑의 중심입니다. 여러분의 애플리케이션뿐만 아니라, Laravel의 모든 핵심 서비스들도 서비스 프로바이더를 통해 부트스트랩됩니다.

여기서 "부트스트랩"이란 무엇일까요? 일반적으로 **등록(registering)** 을 의미하며, 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트 등을 등록하는 것을 포함합니다. 서비스 프로바이더는 여러분의 애플리케이션을 구성할 수 있는 중심 위치입니다.

Laravel에 포함된 `config/app.php` 파일을 열어보면, `providers` 배열이 있습니다. 이 배열에는 애플리케이션을 위해 로드될 모든 서비스 프로바이더 클래스가 나열되어 있습니다. 기본적으로 Laravel의 핵심 서비스 프로바이더 셋이 이 배열에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등과 같은 핵심 Laravel 컴포넌트들을 부트스트랩합니다. 이들 중 많은 프로바이더는 "지연(deferred)" 프로바이더로 설정되어 있습니다. 즉, 매 요청마다 로드되는 것이 아니라, 실제로 해당 서비스가 필요할 때만 로드됩니다.

이 개요에서는 자신만의 서비스 프로바이더를 작성하고, 이를 Laravel 애플리케이션에 등록하는 방법을 배웁니다.

> **참고**  
> Laravel이 요청을 처리하고 내부적으로 어떻게 동작하는지 더 알고 싶다면, Laravel [요청 라이프사이클](/docs/{{version}}/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 포함합니다. `register` 메서드 내에서는 **오직 [서비스 컨테이너](/docs/{{version}}/container) 에 바인딩하는 작업만** 수행해야 합니다. 이벤트 리스너, 라우트 또는 기타 기능의 등록을 `register` 메서드 내에서 시도해서는 안 됩니다.

Artisan CLI는 `make:provider` 명령어로 새로운 프로바이더를 생성할 수 있습니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### Register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 오직 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩하는 작업만 해야 합니다. 이벤트 리스너, 라우트, 기타 기능의 등록을 시도해서는 안 됩니다. 그렇지 않으면, 아직 로드되지 않은 다른 서비스 프로바이더가 제공하는 서비스를 실수로 사용할 수 있습니다.

기본적인 서비스 프로바이더 예제를 살펴봅시다. 서비스 프로바이더의 메서드 내에서는 항상 `$app` 속성을 사용할 수 있는데, 이 속성을 통해 서비스 컨테이너에 접근할 수 있습니다:

    <?php

    namespace App\Providers;

    use App\Services\Riak\Connection;
    use Illuminate\Support\ServiceProvider;

    class RiakServiceProvider extends ServiceProvider
    {
        /**
         * 어플리케이션 서비스를 등록합니다.
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

이 서비스 프로바이더는 오직 `register` 메서드만 정의하며, 이를 통해 서비스 컨테이너에 `App\Services\Riak\Connection`의 구현을 바인딩합니다. Laravel의 서비스 컨테이너에 익숙하지 않다면, [관련 문서](/docs/{{version}}/container)를 확인하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 속성

서비스 프로바이더에서 여러 개의 간단한 바인딩을 등록해야 한다면, 각각 수동으로 바인딩하는 대신 `bindings` 및 `singletons` 속성을 사용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때, 이 속성들을 자동으로 확인하고 바인딩을 등록합니다:

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

<a name="the-boot-method"></a>
### Boot 메서드

서비스 프로바이더 내에서 [뷰 컴포저](/docs/{{version}}/views#view-composers)를 등록해야 한다면 어떻게 해야 할까요? 이는 `boot` 메서드에서 수행해야 합니다. **이 메서드는 다른 모든 서비스 프로바이더가 등록된 후에 호출되므로, 프레임워크에 의해 등록된 모든 서비스에 접근할 수 있습니다:**

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;
    use Illuminate\Support\ServiceProvider;

    class ComposerServiceProvider extends ServiceProvider
    {
        /**
         * 어플리케이션 서비스를 부트스트랩합니다.
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

<a name="boot-method-dependency-injection"></a>
#### Boot 메서드 의존성 주입

서비스 프로바이더의 `boot` 메서드에서 의존성을 타입힌트로 지정할 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)가 필요한 의존성을 자동으로 주입합니다:

    use Illuminate\Contracts\Routing\ResponseFactory;

    /**
     * 어플리케이션 서비스를 부트스트랩합니다.
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

<a name="registering-providers"></a>
## 프로바이더 등록하기

모든 서비스 프로바이더는 `config/app.php` 설정 파일에서 등록됩니다. 이 파일의 `providers` 배열에 서비스 프로바이더의 클래스명을 나열할 수 있습니다. 기본적으로 Laravel의 핵심 서비스 프로바이더들이 이 배열에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등과 같은 핵심 Laravel 컴포넌트들을 부트스트랩합니다.

프로바이더를 등록하려면, 배열에 추가하세요:

    'providers' => [
        // 다른 서비스 프로바이더

        App\Providers\ComposerServiceProvider::class,
    ],

<a name="deferred-providers"></a>
## 지연(Deferred) 프로바이더

프로바이더가 [서비스 컨테이너](/docs/{{version}}/container)에 **오직 바인딩만 수행한다면**, 등록을 해당 바인딩이 실제로 필요할 때까지 지연시킬 수 있습니다. 이러한 프로바이더의 로드를 지연하면, 애플리케이션 성능이 향상됩니다. 이는 매 요청마다 파일 시스템에서 프로바이더를 로드하지 않기 때문입니다.

Laravel은 지연서비스 프로바이더가 제공하는 모든 서비스 목록과 해당 프로바이더 클래스명을 컴파일하고 저장합니다. 그런 다음, 이 중 하나의 서비스를 해결하려고 할 때만 Laravel이 해당 프로바이더를 로드합니다.

프로바이더의 로드를 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의하세요. 이 메서드는 프로바이더가 등록한 서비스 컨테이너 바인딩을 반환해야 합니다:

    <?php

    namespace App\Providers;

    use App\Services\Riak\Connection;
    use Illuminate\Contracts\Support\DeferrableProvider;
    use Illuminate\Support\ServiceProvider;

    class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
    {
        /**
         * 어플리케이션 서비스를 등록합니다.
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
         * 프로바이더가 제공하는 서비스를 반환합니다.
         *
         * @return array
         */
        public function provides()
        {
            return [Connection::class];
        }
    }