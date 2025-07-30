# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성하기](#creating-tests)
- [테스트 실행하기](#running-tests)
    - [병렬로 테스트 실행하기](#running-tests-in-parallel)
    - [테스트 커버리지 보고하기](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 처음부터 테스트를 염두에 두고 설계되었습니다. 실제로, PHPUnit을 통한 테스트 지원이 기본 내장되어 있으며, 애플리케이션용 `phpunit.xml` 파일이 이미 설정되어 있습니다. 또한, Laravel은 애플리케이션을 표현식처럼 간결하게 테스트할 수 있도록 편리한 헬퍼 메서드들도 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉터리에는 두 개의 하위 디렉터리인 `Feature`와 `Unit`이 있습니다. 유닛(Unit) 테스트는 코드의 아주 작은 부분, 일반적으로 하나의 메서드에 초점을 맞춘 테스트입니다. "Unit" 테스트 디렉터리 내 테스트는 Laravel 애플리케이션을 부트스트랩하지 않으므로 데이터베이스나 프레임워크의 다른 서비스에 접근할 수 없습니다.

반면 기능(Feature) 테스트는 몇몇 객체 간 상호작용이나 심지어 JSON 엔드포인트에 대한 완전한 HTTP 요청과 같은 코드의 더 큰 부분을 테스트할 수 있습니다. **일반적으로 전체 테스트의 대부분은 기능 테스트여야 하며, 이러한 테스트가 시스템 전체가 의도한 대로 작동하는지 가장 높은 신뢰도를 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리 모두에서 `ExampleTest.php` 파일이 제공됩니다. 새 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/phpunit` 또는 `php artisan test` 명령어로 테스트를 실행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 때문에 자동으로 [환경 설정(environment configuration)](/docs/10.x/configuration#environment-configuration)을 `testing`으로 설정합니다. 또한, Laravel은 세션과 캐시 드라이버를 `array`로 자동 설정하여 테스트 실행 중 세션이나 캐시 데이터가 영구 저장되지 않도록 합니다.

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수 설정은 애플리케이션의 `phpunit.xml` 파일에서 할 수 있지만, 테스트 실행 전에 반드시 `config:clear` Artisan 명령어로 구성 캐시를 비워야 변경 사항이 반영됩니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션을 사용해 Artisan 명령어를 실행할 때 기본 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

Laravel은 애플리케이션의 기본 `TestCase` 클래스에 적용되는 `CreatesApplication` 트레이트를 포함합니다. 이 트레이트는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드를 포함하고 있습니다. 병렬 테스트 기능 같은 일부 기능이 이 트레이트에 의존하기 때문에 원래 위치에서 변경하지 않고 유지하는 것이 중요합니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 생성된 테스트는 `tests/Feature` 디렉터리에 위치합니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하려면 `make:test` 명령어 실행 시 `--unit` 옵션을 추가합니다:

```shell
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 테스트를 생성하고 싶다면 `make:test` 명령어에 `--pest` 옵션을 제공합니다:

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]  
> 테스트 스텁(stub)은 [스텁 퍼블리싱(stub publishing)](/docs/10.x/artisan#stub-customization)을 통해 사용자화할 수 있습니다.

테스트가 생성되면 일반적으로 [PHPUnit](https://phpunit.de)을 사용하듯 테스트 메서드를 정의할 수 있습니다. 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어로 테스트를 실행하세요:

```
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 기본 테스트 예제입니다.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]  
> 테스트 클래스 내에서 직접 `setUp` 또는 `tearDown` 메서드를 정의한다면, 반드시 부모 클래스의 `parent::setUp()` 및 `parent::tearDown()` 메서드를 호출해야 합니다. 보통 `setUp` 메서드에서는 시작 부분에 `parent::setUp()`을 호출하고, `tearDown` 메서드에서는 끝 부분에 `parent::tearDown()`을 호출하는 것이 좋습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 언급했듯이, 테스트를 작성한 후에는 `phpunit` 명령어를 사용해 실행할 수 있습니다:

```shell
./vendor/bin/phpunit
```

또한 `phpunit` 명령어 외에 `test` Artisan 명령어를 사용해 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발 및 디버깅을 용이하게 하기 위해 자세한 테스트 보고서를 제공합니다:

```shell
php artisan test
```

`phpunit` 명령어로 전달 가능한 인수는 모두 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행하기 (Running Tests in Parallel)

기본적으로 Laravel과 PHPUnit은 단일 프로세스에서 순차적으로 테스트를 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 실행 시간을 크게 단축할 수 있습니다. 시작하려면 개발용 의존성으로 `brianium/paratest` Composer 패키지를 설치하세요. 그런 다음 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가합니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 사용자의 머신 CPU 코어 수만큼 프로세스를 생성합니다. 프로세스 수를 조절하려면 `--processes` 옵션을 사용하세요:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]  
> 병렬 테스트 실행 중에는 일부 PHPUnit 옵션(`--do-not-cache-result` 등)을 사용할 수 없을 수 있습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 설정되어 있으면, Laravel은 병렬 테스트별로 테스트 데이터베이스를 자동으로 생성하고 마이그레이션을 진행합니다. 이 테스트 데이터베이스들은 각 프로세스별 고유한 토큰이 접미사로 붙어 구분됩니다. 예를 들어, 두 개 프로세스가 실행되면 `your_db_test_1`, `your_db_test_2` 데이터베이스가 생성 및 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어 여러 차례 호출 간에 유지되어 재사용됩니다. 하지만 `--recreate-databases` 옵션을 사용하면 테스트 실행 시마다 새로 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 후크(Hooks)

때때로, 여러 테스트 프로세스가 동시에 사용할 특정 리소스를 사전에 준비해야 할 수도 있습니다.

`ParallelTesting` 파사드를 사용하면 각 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 지정된 클로저는 각각 현재 프로세스 토큰(`$token`)과 테스트 케이스(`$testCase`) 변수를 전달받습니다:

```
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

        // 테스트 데이터베이스가 생성될 때 실행...
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
```

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근하기

애플리케이션 테스트 코드의 다른 어디서든 현재 병렬 프로세스의 "토큰"을 사용하고 싶다면 `token` 메서드를 호출하면 됩니다. 이 토큰은 각 테스트 프로세스 고유의 문자열 식별자로, 병렬 테스트 프로세스 간에 리소스를 분리할 때 사용할 수 있습니다. 예를 들어, Laravel은 이 토큰을 모든 병렬 테스트 프로세스가 생성하는 테스트 데이터베이스 이름 끝에 자동으로 덧붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고하기 (Reporting Test Coverage)

> [!WARNING]  
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov) 확장 설치가 필요합니다.

애플리케이션 테스트를 실행할 때, 테스트가 실제로 애플리케이션 코드의 어느 부분을 얼마나 덮고 있는지 파악하고자 할 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 적용하기

`--min` 옵션을 사용하면 테스트 커버리지에 대한 최소 기준을 설정할 수 있습니다. 이 기준에 미치지 못하면 테스트 스위트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 러너는 애플리케이션에서 가장 느린 테스트들을 목록으로 보여주는 편리한 기능도 포함합니다. `--profile` 옵션을 붙여 `test` 명령어를 실행하면 느린 테스트 10개가 출력되어 어느 테스트를 개선해야 테스트 속도를 높일 수 있는지 쉽게 확인할 수 있습니다:

```shell
php artisan test --profile
```