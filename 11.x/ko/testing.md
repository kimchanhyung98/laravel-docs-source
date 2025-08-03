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

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de) 지원이 기본으로 포함되어 있으며, 애플리케이션에 맞게 이미 설정된 `phpunit.xml` 파일이 제공됩니다. 프레임워크는 또한 애플리케이션을 표현력 있게 테스트할 수 있도록 돕는 여러 편리한 헬퍼 메서드를 함께 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉토리는 `Feature`와 `Unit` 두 개의 디렉토리를 포함합니다. 유닛 테스트는 코드의 아주 작은, 고립된 부분에 집중하는 테스트입니다. 대부분의 유닛 테스트는 보통 단일 메서드를 테스트하는 경우가 많습니다. "Unit" 테스트 디렉토리 내의 테스트는 Laravel 애플리케이션을 부트하지 않으므로 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

반면, 기능 테스트(Feature tests)는 여러 객체가 서로 상호작용하는 방식이나 JSON 엔드포인트에 대한 완전한 HTTP 요청을 포함해 코드의 더 큰 부분을 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트여야 합니다. 이런 유형의 테스트가 시스템 전체가 의도한 대로 작동하는지에 대해 가장 큰 신뢰를 제공하기 때문입니다.**

`Feature`와 `Unit` 테스트 디렉토리에는 각각 `ExampleTest.php` 파일이 제공됩니다. Laravel을 새로 설치한 후에는 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어로 테스트를 실행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 때문에 자동으로 [환경 설정](/docs/11.x/configuration#environment-configuration)을 `testing`으로 설정합니다. 또한 Laravel은 세션과 캐시를 `array` 드라이버로 자동 설정해 테스트 중에 세션이나 캐시 데이터가 유지되지 않도록 합니다.

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트 실행 전에 반드시 Artisan의 `config:clear` 명령어로 구성 캐시를 비워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 만들어둘 수 있습니다. 이 파일은 Pest, PHPUnit 테스트를 실행하거나 `--env=testing` 옵션을 사용해 Artisan 명령어를 실행할 때 `.env` 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉토리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉토리에 테스트를 생성하려면 `make:test` 명령어에 `--unit` 옵션을 추가하면 됩니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]  
> 테스트 스텁은 [stub publishing](/docs/11.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

테스트가 생성되면 Pest 또는 PHPUnit을 사용해 평소처럼 테스트를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하세요:

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
     * 기본 테스트 예시입니다.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]  
> 테스트 클래스 내에서 직접 `setUp` / `tearDown` 메서드를 정의할 경우 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 보통 `setUp` 메서드 시작 부분에 `parent::setUp()`를, `tearDown` 메서드 마지막에 `parent::tearDown()`를 호출하세요.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 설명한 것처럼 테스트를 작성한 후에는 `pest` 또는 `phpunit`으로 다음과 같이 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest`나 `phpunit` 명령어 외에도 Artisan `test` 명령어로 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 자세한 테스트 보고서를 제공하여 개발과 디버깅을 쉽게 해줍니다:

```shell
php artisan test
```

`pest`나 `phpunit` 명령어에 전달할 수 있는 인수를 Artisan `test` 명령어에도 동일하게 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬 테스트 실행하기 (Running Tests in Parallel)

기본적으로 Laravel과 Pest / PHPUnit은 테스트를 단일 프로세스에서 순차적으로 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치하세요. 이후 `test` Artisan 명령어에 `--parallel` 옵션을 추가해 실행합니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 기기의 CPU 코어 수만큼 프로세스를 생성합니다. `--processes` 옵션으로 프로세스 수를 조정할 수도 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]  
> 병렬 테스트 실행 시 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결을 구성했다면, Laravel은 병렬 프로세스마다 별도의 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 테스트 데이터베이스는 각 프로세스의 고유 토큰을 접미사로 붙여 구별됩니다. 예를 들어 병렬 테스트 프로세스가 두 개라면 `your_db_test_1`과 `your_db_test_2` 테스트 데이터베이스가 생성되고 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령을 반복 호출해도 유지되어 다음 호출 시 재사용됩니다. 그러나 `--recreate-databases` 옵션을 사용하면 테스트 데이터베이스를 다시 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

가끔 애플리케이션 테스트에서 여러 병렬 프로세스가 안전하게 공유해야 할 리소스를 준비할 필요가 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시 실행할 코드를 지정할 수 있습니다. 전달되는 클로저들은 각각 프로세스 토큰(`$token`)과 현재 테스트 케이스(`$testCase`) 변수를 받습니다:

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
     * 애플리케이션 서비스를 부트스트랩합니다.
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

애플리케이션 테스트 코드의 다른 위치에서 현재 병렬 프로세스의 토큰에 접근하려면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 식별하는 고유 문자열입니다. 예를 들어 Laravel은 병렬 테스트 프로세스가 생성하는 테스트 데이터베이스 이름에 자동으로 이 토큰을 덧붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고하기 (Reporting Test Coverage)

> [!WARNING]  
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov) 확장 모듈이 필요합니다.

테스트를 실행하면서 실제 애플리케이션 코드가 얼마나 테스트에 포함되는지 또는 테스트 실행 시 어떤 코드가 사용되는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어에 `--coverage` 옵션을 추가해 실행할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 적용하기

`--min` 옵션을 사용하여 애플리케이션 테스트 커버리지의 최소 기준값을 정할 수 있습니다. 이 기준에 미달하면 테스트 스위트는 실패로 간주됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 러너에는 애플리케이션에서 가장 느린 테스트를 쉽게 확인할 수 있는 기능도 포함되어 있습니다. `--profile` 옵션을 추가해 `test` 명령어를 실행하면, 가장 느린 10개의 테스트 목록을 보여줘 테스트 속도 개선이 필요한 부분을 쉽게 찾을 수 있습니다:

```shell
php artisan test --profile
```