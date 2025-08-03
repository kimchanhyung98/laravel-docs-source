# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성하기](#creating-tests)
- [테스트 실행하기](#running-tests)
    - [병렬 테스트 실행하기](#running-tests-in-parallel)
    - [테스트 커버리지 보고하기](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)를 이용한 테스트 지원이 기본 내장되어 있으며, `phpunit.xml` 파일도 애플리케이션에 대해 이미 설정되어 있습니다. 프레임워크는 또한 애플리케이션을 표현력 있게 테스트할 수 있도록 편리한 헬퍼 메서드를 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉토리에는 `Feature`와 `Unit` 두 개의 디렉토리가 있습니다. 유닛 테스트(Unit test)는 코드의 아주 작고 독립적인 부분에 초점을 맞춘 테스트입니다. 사실 대다수 유닛 테스트는 하나의 메서드에 집중하는 경우가 많습니다. "Unit" 테스트 디렉토리 내 테스트는 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

반면, Feature 테스트는 여러 객체가 어떻게 상호작용하는지 또는 JSON 엔드포인트에 대한 전체 HTTP 요청까지 아우르는 더 큰 범위의 코드를 테스트할 수 있습니다. **일반적으로 여러분의 대부분 테스트는 Feature 테스트이어야 합니다. 이러한 테스트는 시스템 전체가 의도대로 작동하는지 가장 확실한 신뢰를 제공합니다.**

`Feature`와 `Unit` 테스트 디렉토리 모두에 `ExampleTest.php` 파일이 제공됩니다. Laravel 애플리케이션을 새로 설치한 후 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 설정 (Environment)

테스트 실행 시, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수를 기반으로 자동으로 [구성 환경](/docs/12.x/configuration#environment-configuration)을 `testing`으로 설정합니다. Laravel은 또한 테스트가 진행되는 동안 세션과 캐시가 지속되지 않도록 세션과 캐시 드라이버를 `array`로 자동 구성합니다.

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트 실행 전에 반드시 `config:clear` Artisan 명령어를 사용해 구성 캐시를 비워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest 또는 PHPUnit 테스트 실행이나 `--env=testing` 옵션을 사용한 Artisan 명령 실행 시 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉토리에 만들어집니다:

```shell
php artisan make:test UserTest
```

만약 `tests/Unit` 디렉토리에 테스트를 생성하고 싶다면, `make:test` 명령어를 실행할 때 `--unit` 옵션을 추가하세요:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [stub publishing](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

테스트가 생성되면, Pest 또는 PHPUnit을 이용해 평소처럼 테스트를 정의하세요. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행합니다:

```php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});
```

```php tab=PHPUnit
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
> 테스트 클래스 내에서 직접 `setUp` / `tearDown` 메서드를 정의할 경우에는 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 보통 `setUp` 메서드 시작 부분에 `parent::setUp()`을, `tearDown` 메서드 종료 부분에 `parent::tearDown()`을 호출하세요.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 언급했듯이 테스트를 작성한 후에는 `pest` 또는 `phpunit` 명령어로 테스트를 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest`나 `phpunit` 외에도, `test` Artisan 명령어를 실행하여 테스트를 수행할 수 있습니다. Artisan 테스트 실행기는 개발과 디버깅을 돕기 위해 상세한 테스트 보고서를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수를 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬 테스트 실행하기 (Running Tests in Parallel)

기본적으로 Laravel과 Pest / PHPUnit은 단일 프로세스 내에서 테스트를 순차적으로 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 테스트 수행 시간을 크게 단축할 수 있습니다. 시작하려면 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치하세요. 그 다음 `test` Artisan 명령어에 `--parallel` 옵션을 포함해 실행합니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본 설정은 머신의 CPU 코어 수만큼 프로세스를 생성합니다. `--processes` 옵션을 사용해 프로세스 수를 조정할 수도 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시, 일부 Pest / PHPUnit 옵션들(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

주 데이터베이스 연결을 구성한 경우, Laravel은 병렬로 실행 중인 각 테스트 프로세스를 위해 자동으로 테스트 데이터베이스를 생성하고 마이그레이션합니다. 테스트 데이터베이스 이름에는 프로세스마다 고유한 토큰이 접미사로 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면 `your_db_test_1`, `your_db_test_2` 데이터베이스가 각각 생성되고 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어를 여러 번 호출해도 유지되어 이후 테스트 실행 때 재사용됩니다. 다만, `--recreate-databases` 옵션을 사용하면 테스트 데이터베이스를 다시 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅(Parallel Testing Hooks)

가끔 애플리케이션 테스트에서 사용하는 특정 리소스를 여러 테스트 프로세스가 안전하게 사용할 수 있도록 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 단계에서 실행할 코드를 지정할 수 있습니다. 전달받는 클로저는 각각 프로세스 토큰 `$token`과 현재 테스트 케이스 `$testCase` 변수를 받습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // 테스트 데이터베이스 생성 시 실행...
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
#### 병렬 테스트 토큰 접근

애플리케이션 테스트 코드 내 다른 위치에서 현재 병렬 테스트 프로세스의 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 식별하는 고유한 문자열이며, 병렬 테스트 프로세스별로 리소스를 구분하는 데 활용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스가 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고하기 (Reporting Test Coverage)

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov) 확장 모듈이 필요합니다.

애플리케이션 테스트를 실행할 때, 실제로 테스트가 앱 코드의 어느 부분을 얼마나 실행하는지 알고 싶을 수 있습니다. 이를 위해 `test` 명령어를 호출할 때 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 적용하기

`--min` 옵션을 사용해 애플리케이션에 대한 최소 테스트 커버리지 기준을 정의할 수 있습니다. 기준을 충족하지 못하면 테스트 스위트는 실패 처리됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 실행기는 애플리케이션에서 가장 느린 테스트 목록을 쉽게 보여주는 편리한 기능도 포함합니다. `--profile` 옵션을 붙여 `test` 명령어를 호출하면 느린 테스트 10개를 보여줍니다. 이를 통해 어떤 테스트를 개선해야 테스트 속도를 높일 수 있는지 쉽게 파악할 수 있습니다:

```shell
php artisan test --profile
```