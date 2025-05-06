# 테스트: 시작하기

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [테스트 병렬 실행](#running-tests-in-parallel)
    - [테스트 커버리지 리포트](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)

<a name="introduction"></a>
## 소개

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로, PHPUnit을 이용한 테스트 지원이 기본으로 포함되어 있으며, 애플리케이션에는 이미 `phpunit.xml` 파일이 설정되어 있습니다. 프레임워크에는 또한 애플리케이션을 간결하게 테스트할 수 있는 편리한 헬퍼 메서드들이 제공됩니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 하위 디렉터리가 포함되어 있습니다. 유닛 테스트(Unit Test)는 코드의 아주 작은, 고립된 부분에 집중합니다. 대부분의 유닛 테스트는 하나의 메서드에 집중하는 경우가 많습니다. "Unit" 테스트 디렉터리 내의 테스트는 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션의 데이터베이스나 다른 프레임워크 서비스를 사용할 수 없습니다.

기능 테스트(Feature Test)는 여러 객체 간의 상호작용이나 JSON 엔드포인트에 대한 전체 HTTP 요청 등 좀 더 넓은 범위를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트여야 합니다. 이러한 유형의 테스트가 시스템 전체가 의도한 대로 동작하는지에 대한 가장 큰 확신을 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리에는 모두 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 진행할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수로 인해 [환경 구성](/docs/{{version}}/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 Laravel은 세션과 캐시를 자동으로 `array` 드라이버로 구성하므로, 테스트 중에는 세션이나 캐시 데이터가 저장되지 않습니다.

필요에 따라 테스트 환경의 다른 구성 값도 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 삭제해야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

또한 프로젝트의 루트에 `.env.testing` 파일을 생성할 수도 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령어를 실행할 때, 기본 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

Laravel에는 애플리케이션의 기본 `TestCase` 클래스에 적용되는 `CreatesApplication` 트레이트가 있습니다. 이 트레이트에는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드가 포함되어 있습니다. 이 트레이트는 일부 기능(예: Laravel의 병렬 테스트 기능)이 이에 의존하므로, 원래 위치에서 변경하지 않는 것이 중요합니다.

<a name="creating-tests"></a>
## 테스트 생성

새로운 테스트 케이스를 생성하려면, `make:test` Artisan 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하려면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 테스트를 생성하려면, `make:test` 명령어에 `--pest` 옵션을 추가할 수 있습니다:

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]  
> 테스트 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

생성된 테스트에서는 [PHPUnit](https://phpunit.de)을 사용하듯이 테스트 메서드를 정의할 수 있습니다. 테스트를 실행하려면, 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하세요:

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 기본 테스트 예시.
         */
        public function test_basic_test(): void
        {
            $this->assertTrue(true);
        }
    }

> [!WARNING]  
> 테스트 클래스 내에서 `setUp` / `tearDown` 메서드를 직접 정의하는 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로는 사용자 정의 `setUp` 메서드의 시작 부분에서 `parent::setUp()`을, `tearDown` 메서드의 마지막에 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행

앞에서 언급한 것처럼, 테스트를 작성한 후에는 `phpunit` 명령어로 테스트를 실행할 수 있습니다:

```shell
./vendor/bin/phpunit
```

`phpunit` 명령 외에도, `test` Artisan 명령어를 사용하여 테스트를 수행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 용이하게 하기 위해 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`phpunit` 명령에 전달할 수 있는 인자들은 모두 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행

기본적으로 Laravel과 PHPUnit은 싱글 프로세스 내에서 순차적으로 테스트를 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트 시간을 크게 단축할 수 있습니다. 시작하려면, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그 다음, `test` Artisan 명령어 실행 시 `--parallel` 옵션을 포함하세요:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 사용 가능한 CPU 코어 수만큼 프로세스를 생성합니다. 하지만, `--processes` 옵션을 사용해 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]  
> 병렬 테스트 실행 시 일부 PHPUnit 옵션(`--do-not-cache-result` 등)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 구성되어 있으면, Laravel은 병렬로 실행 중인 각 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 테스트 데이터베이스는 각 프로세스마다 고유한 토큰이 접미사로 붙게 됩니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면, Laravel은 `your_db_test_1`, `your_db_test_2`와 같은 테스트 데이터베이스를 생성 및 사용합니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어 호출 사이에 유지되어, 이후의 테스트 실행에서도 재사용됩니다. 하지만, `--recreate-databases` 옵션을 사용하여 데이터베이스를 다시 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

때때로, 애플리케이션의 테스트에 사용되는 특정 자원을 여러 테스트 프로세스에서 안전하게 사용할 수 있도록 준비해야 할 수도 있습니다.

`ParallelTesting` 파사드를 사용하여, 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시에 실행될 코드를 지정할 수 있습니다. 각 클로저는 프로세스 토큰인 `$token`과 현재 테스트 케이스인 `$testCase` 변수를 전달받을 수 있습니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Artisan;
    use Illuminate\Support\Facades\ParallelTesting;
    use Illuminate\Support\ServiceProvider;
    use PHPUnit\Framework\TestCase;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 부트스트랩.
         */
        public function boot(): void
        {
            ParallelTesting::setUpProcess(function (int $token) {
                // ...
            });

            ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
                // ...
            });

            // 테스트 데이터베이스 생성 시 실행됩니다...
            ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
                Artisan::call('db:seed');
            });

            ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
                // ...
            });

            ParallelTesting::tearDownProcess(function (int $token) {
                // ...
            });
        }
    }

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근

애플리케이션의 테스트 코드 어디에서든 현재 병렬 프로세스의 "토큰"을 사용하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 각 테스트 프로세스마다 고유한 문자열 식별자이며, 병렬 테스트 실행 간 자원을 분리하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스가 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포트

> [!WARNING]  
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 테스트 케이스가 실제로 애플리케이션 코드를 얼마나 커버하는지 확인하고 싶을 수 있습니다. 이를 위해, `test` 명령어 실행 시 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제

`--min` 옵션을 사용해 애플리케이션의 테스트 커버리지 최소 기준을 설정할 수 있습니다. 이 기준에 미달할 경우 테스트가 실패하게 됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링

Artisan 테스트 러너는 애플리케이션의 가장 느린 테스트를 나열하는 편리한 기능도 제공합니다. `test` 명령어에 `--profile` 옵션을 추가하면, 가장 느린 10개의 테스트 목록을 확인할 수 있으며 이를 통해 어떤 테스트를 개선해 테스트 속도를 높일 수 있을지 쉽게 파악할 수 있습니다:

```shell
php artisan test --profile
```
