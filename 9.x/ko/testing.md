# 테스트: 시작하기

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [테스트 병렬 실행](#running-tests-in-parallel)
    - [테스트 커버리지 리포팅](#reporting-test-coverage)

<a name="introduction"></a>
## 소개

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로, PHPUnit을 이용한 테스트 지원이 기본적으로 포함되어 있으며, 애플리케이션에 이미 `phpunit.xml` 파일이 설정되어 있습니다. 또한, 프레임워크에는 애플리케이션을 명확하게 테스트할 수 있는 편리한 헬퍼 메서드가 기본 제공됩니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 디렉터리가 포함되어 있습니다. 단위 테스트(Unit Test)는 코드의 아주 작은, 독립된 부분에 초점을 맞춘 테스트입니다. 대부분의 단위 테스트는 하나의 메서드에 집중하는 경우가 많습니다. "Unit" 테스트 디렉터리 내의 테스트는 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션의 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

기능 테스트(Feature Test)는 여러 객체 간의 상호작용이나 JSON 엔드포인트에 대한 전체 HTTP 요청 등, 코드의 더 넓은 부분을 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트여야 하며, 이러한 테스트가 시스템 전체가 의도한 대로 동작하는지에 대한 가장 높은 신뢰도를 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리에는 `ExampleTest.php` 파일이 기본 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 구동할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때는, `phpunit.xml` 파일에 정의된 환경 변수 덕분에 Laravel은 [환경 설정](/docs/{{version}}/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 테스트 중에는 세션과 캐시 드라이버가 자동으로 `array`로 설정되어, 테스트 도중 세션이나 캐시 데이터가 저장되지 않습니다.

필요에 따라 추가적인 테스트 환경 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` 아티즌 명령어로 설정 캐시를 비워주시기 바랍니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 PHPUnit 테스트 실행 시 또는 `--env=testing` 옵션을 사용하여 아티즌 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

Laravel은 애플리케이션의 기본 `TestCase` 클래스에 `CreatesApplication` 트레이트를 포함하고 있습니다. 이 트레이트에는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드가 구현되어 있습니다. 이 트레이트는 원래 위치에 그대로 두는 것이 중요하며, Laravel의 병렬 테스트 기능 등 일부 기능이 이 트레이트에 의존합니다.

<a name="creating-tests"></a>
## 테스트 생성

새 테스트 케이스를 생성하려면 `make:test` 아티즌 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하려면 `make:test` 명령어 실행 시 `--unit` 옵션을 추가하면 됩니다:

```shell
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 테스트를 생성하려면 `make:test` 명령어에 `--pest` 옵션을 추가하세요:

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> **참고**  
> 테스트 스텁은 [스텁 커스터마이징](/docs/{{version}}/artisan#stub-customization)를 통해 맞춤 설정할 수 있습니다.

테스트가 생성되면, [PHPUnit](https://phpunit.de)을 사용하여 일반적으로 테스트 메서드를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 입력하면 됩니다:

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예제.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $this->assertTrue(true);
        }
    }

> **경고**  
> 테스트 클래스 내에서 `setUp` / `tearDown` 메서드를 직접 정의한다면, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯이, 테스트를 작성한 후에는 `phpunit`을 이용해서 실행할 수 있습니다:

```shell
./vendor/bin/phpunit
```

`phpunit` 명령어 외에도 `test` 아티즌 명령어로도 테스트를 실행할 수 있습니다. 아티즌 테스트 러너는 개발 및 디버깅을 쉽게 하기 위해 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`phpunit` 명령어에 전달할 수 있는 모든 인수가 아티즌 `test` 명령어에도 전달 가능합니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행

기본적으로, Laravel과 PHPUnit은 단일 프로세스 내에서 순차적으로 테스트를 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트 시간을 크게 단축할 수 있습니다. 이를 시작하려면, 애플리케이션이 `nunomaduro/collision` 패키지의 `^5.3` 이상 버전에 의존하고 있어야 합니다. 그런 다음, `test` 아티즌 명령 실행 시 `--parallel` 옵션을 추가하세요:

```shell
php artisan test --parallel
```

기본적으로 Laravel은 시스템의 CPU 코어 개수만큼 프로세스를 생성합니다. 하지만 `--processes` 옵션을 사용하여 프로세스 개수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> **경고**  
> 병렬로 테스트를 실행할 때는 일부 PHPUnit 옵션(예: `--do-not-cache-result`)을 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트 & 데이터베이스

기본 데이터베이스 연결이 설정되어 있다면, Laravel은 각 병렬 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션을 처리합니다. 테스트 데이터베이스는 각 프로세스마다 고유한 토큰이 접미사로 붙어 생성됩니다. 예를 들어, 병렬 테스트 프로세스가 두 개인 경우, Laravel은 `your_db_test_1`과 `your_db_test_2`를 생성 및 사용합니다.

기본적으로 테스트 데이터베이스는 `test` 아티즌 명령어 호출 간에 유지되어, 이후 테스트 호출에서 재사용할 수 있습니다. 하지만 `--recreate-databases` 옵션을 사용하여 데이터베이스를 다시 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅(Hook)

간혹, 여러 테스트 프로세스가 안전하게 사용할 수 있도록 테스트에서 사용하는 특정 리소스를 준비해야 할 필요가 있을 수 있습니다.

`ParallelTesting` 파사드를 이용하면, 프로세스나 테스트 케이스의 `setUp`이나 `tearDown` 시 실행할 코드를 지정할 수 있습니다. 전달된 클로저는 프로세스 토큰 `$token`과 현재 테스트 케이스 `$testCase` 변수를 인자로 받습니다:

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

            // 테스트 데이터베이스가 생성될 때 실행됨...
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

애플리케이션 테스트 코드 내 어디서든 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 각 테스트 프로세스마다 고유한 문자열 식별자이며, 병렬 테스트 프로세스별로 리소스를 분리하는 용도로 활용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스에서 생성되는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포팅

> **경고**  
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 실제로 테스트 케이스가 애플리케이션 코드를 얼마나 커버하는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제 설정

`--min` 옵션을 이용해 애플리케이션의 최소 테스트 커버리지 기준을 정의할 수 있습니다. 이 기준에 미달할 경우 테스트가 실패 처리됩니다:

```shell
php artisan test --coverage --min=80.3
```