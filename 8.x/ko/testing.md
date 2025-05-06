# 테스트: 시작하기

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [테스트 병렬 실행](#running-tests-in-parallel)

<a name="introduction"></a>
## 소개

라라벨은 테스트를 염두에 두고 설계되었습니다. 실제로 PHPUnit을 이용한 테스트 지원이 기본적으로 포함되어 있으며, 애플리케이션의 루트에 이미 `phpunit.xml` 파일이 설정되어 있습니다. 프레임워크는 또한 애플리케이션 테스트를 표현력 있게 작성할 수 있도록 다양한 헬퍼 메서드를 제공합니다.

기본적으로 여러분의 애플리케이션 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 디렉터리가 포함되어 있습니다. 단위(Unit) 테스트는 코드의 아주 작고 독립적인 부분에 초점을 맞춥니다. 대부분의 단위 테스트는 아마도 하나의 메서드에 집중할 것입니다. "Unit" 테스트 디렉터리 안의 테스트는 라라벨 애플리케이션을 부팅하지 않으므로, 데이터베이스나 프레임워크의 다른 서비스에 접근할 수 없습니다.

특성(Feature) 테스트는 여러 객체가 어떻게 상호작용하는지 또는 JSON 엔드포인트에 대한 전체 HTTP 요청과 같이, 코드의 더 큰 부분을 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 Feature 테스트로 작성하는 것이 좋습니다. 이러한 유형의 테스트가 시스템 전체가 의도한 대로 동작하는지에 대해 가장 높은 신뢰를 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리에는 `ExampleTest.php` 파일이 기본으로 제공됩니다. 새 라라벨 애플리케이션을 설치한 후 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 실행할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때 라라벨은 `phpunit.xml` 파일에 정의된 환경 변수로 인해 [환경 구성](/docs/{{version}}/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 세션과 캐시 역시 `array` 드라이버로 자동 설정되어, 테스트 중에는 세션이나 캐시 데이터가 저장되지 않습니다.

필요에 따라 다른 테스트 환경 설정값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 `config:clear` 아티즌(Artisan) 명령어로 설정 캐시를 반드시 비워주세요!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

또한, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. PHPUnit 테스트를 실행하거나 `--env=testing` 옵션으로 아티즌 명령어를 사용할 때, 이 파일이 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

라라벨은 애플리케이션의 기본 `TestCase` 클래스에 `CreatesApplication` 트레이트를 포함하고 있습니다. 이 트레이트에는 테스트 실행 전에 라라벨 애플리케이션을 부트스트랩하는 `createApplication` 메서드가 포함되어 있습니다. 일부 기능(예: 라라벨의 병렬 테스트 기능 등)이 의존하므로, 이 트레이트는 원래 위치에 그대로 두는 것이 중요합니다.

<a name="creating-tests"></a>
## 테스트 생성

새로운 테스트 케이스를 생성하려면 `make:test` 아티즌 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

    php artisan make:test UserTest

`tests/Unit` 디렉터리에 테스트를 생성하려면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

    php artisan make:test UserTest --unit

[Pest PHP](https://pestphp.com) 테스트를 생성하려면 `make:test` 명령어에 `--pest` 옵션을 추가할 수 있습니다:

    php artisan make:test UserTest --pest
    php artisan make:test UserTest --unit --pest

> {tip} 테스트 스텁은 [stub 배포](/docs/{{version}}/artisan#stub-customization)를 통해 커스터마이즈할 수 있습니다.

테스트가 생성되면, [PHPUnit](https://phpunit.de)에서처럼 테스트 메서드를 정의할 수 있습니다. 테스트 실행은 콘솔에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어로 할 수 있습니다:

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예시.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $this->assertTrue(true);
        }
    }

> {note} 테스트 클래스 내에서 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯이, 테스트를 작성하면 `phpunit`을 사용하여 실행할 수 있습니다:

    ./vendor/bin/phpunit

`phpunit` 명령어 이외에도, `test` 아티즌 명령어로 테스트를 실행할 수 있습니다. 이 아티즌 테스트 러너는 개발 및 디버깅을 쉽게 하기 위해 상세한 테스트 리포트를 제공합니다:

    php artisan test

`phpunit` 명령어에 전달할 수 있는 모든 인자는 아티즌 `test` 명령어에도 전달할 수 있습니다:

    php artisan test --testsuite=Feature --stop-on-failure

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행

기본적으로 라라벨과 PHPUnit은 단일 프로세스 내에서 테스트를 순차적으로 실행합니다. 그러나, 여러 프로세스에서 동시에 테스트를 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면, 먼저 애플리케이션이 `nunomaduro/collision` 패키지의 버전 `^5.3` 이상을 의존성으로 가지고 있는지 확인하세요. 이후 `test` 아티즌 명령어에 `--parallel` 옵션을 포함하여 실행합니다:

    php artisan test --parallel

기본적으로 라라벨은 시스템의 CPU 코어 수와 동일한 수의 프로세스를 생성합니다. 그러나, `--processes` 옵션을 사용하여 프로세스 수를 조정할 수 있습니다:

    php artisan test --parallel --processes=4

> {note} 병렬로 테스트를 실행할 경우, 일부 PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

라라벨은 테스트를 병렬로 실행하는 각 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 테스트 데이터베이스는 프로세스별로 고유한 토큰이 접미사로 붙습니다. 예를 들어, 2개의 병렬 테스트 프로세스를 사용하는 경우, `your_db_test_1`과 `your_db_test_2` 데이터베이스가 각각 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` 아티즌 명령어를 여러 번 실행해도 그대로 유지되어, 다음 `test` 실행에도 재사용할 수 있습니다. 하지만, `--recreate-databases` 옵션을 사용해 데이터베이스를 새로 생성할 수도 있습니다:

    php artisan test --parallel --recreate-databases

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

가끔 애플리케이션 테스트에서 여러 테스트 프로세스가 안전하게 사용할 수 있도록 리소스를 미리 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 이용해서 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰인 `$token`과 현재 테스트 케이스인 `$testCase` 변수를 인자로 받습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Artisan;
    use Illuminate\Support\Facades\ParallelTesting;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            ParallelTesting::setUpProcess(function ($token) {
                // ...
            });

            ParallelTesting::setUpTestCase(function ($token, $testCase) {
                // ...
            });

            // 테스트 데이터베이스가 생성될 때 실행...
            ParallelTesting::setUpTestDatabase(function ($database, $token) {
                Artisan::call('db:seed');
            });

            ParallelTesting::tearDownTestCase(function ($token, $testCase) {
                // ...
            });

            ParallelTesting::tearDownProcess(function ($token) {
                // ...
            });
        }
    }

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근

애플리케이션 테스트 코드의 어떤 위치에서든 현재 병렬 프로세스의 "토큰"에 접근하려면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 테스트 프로세스마다 고유한 문자 식별자이며 병렬 테스트 프로세스별로 리소스를 구분하는 데 사용할 수 있습니다. 예를 들어, 라라벨은 각 병렬 테스트 프로세스가 생성한 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

    $token = ParallelTesting::token();
