# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경 설정](#environment)
- [테스트 생성하기](#creating-tests)
- [테스트 실행하기](#running-tests)
    - [병렬로 테스트 실행하기](#running-tests-in-parallel)
    - [테스트 커버리지 보고](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)을 이용한 테스트 지원이 기본 제공되며, 애플리케이션에 맞게 설정된 `phpunit.xml` 파일도 이미 포함되어 있습니다. 또한 Laravel은 애플리케이션을 표현력 있게 테스트할 수 있도록 도와주는 편리한 헬퍼 메서드를 제공합니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 디렉터리가 있습니다. 단위 테스트(Unit test)는 코드의 아주 작은 부분, 보통은 단일 메서드 하나에 초점을 맞춥니다. "Unit" 테스트 디렉터리 안의 테스트는 Laravel 애플리케이션을 부트스트랩하지 않기 때문에 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

기능 테스트(Feature test)는 여러 객체가 서로 어떻게 상호작용하는지, 또는 JSON 엔드포인트에 대한 전체 HTTP 요청과 같은 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로, 대부분의 테스트는 기능 테스트여야 하며, 이러한 테스트가 시스템 전체가 의도대로 작동하는지에 대해 가장 큰 신뢰를 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리 모두에 `ExampleTest.php` 파일이 기본 제공됩니다. 새 Laravel 애플리케이션을 설치한 후 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 설정 (Environment)

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수들 때문에 자동으로 [환경 구성](/docs/master/configuration#environment-configuration)을 `testing`으로 설정합니다. 또한 Laravel은 세션과 캐시를 `array` 드라이버로 자동 설정하여 테스트 중에는 세션이나 캐시 데이터가 저장되지 않도록 합니다.

필요에 따라 다른 테스트 환경 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 구성 캐시를 삭제하세요!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest나 PHPUnit 테스트 실행 시, 또는 Artisan 명령어에 `--env=testing` 옵션을 지정할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 생성된 테스트는 `tests/Feature` 디렉터리에 위치합니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하려면 `make:test` 명령어에 `--unit` 옵션을 추가하면 됩니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [스텁 게시](/docs/master/artisan#stub-customization)를 통해 커스터마이징할 수 있습니다.

테스트가 생성된 뒤에는, Pest나 PHPUnit을 이용해 평소처럼 테스트를 작성하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하세요:

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
     * 기본 테스트 예시.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스 내에서 `setUp`이나 `tearDown` 메서드를 직접 정의한다면, 반드시 부모 클래스의 `parent::setUp()`이나 `parent::tearDown()` 메서드를 호출해야 합니다. 보통 `setUp` 메서드 시작 부분에서 `parent::setUp()`을, `tearDown` 메서드 끝부분에서 `parent::tearDown()`을 호출하세요.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 설명했듯이, 테스트를 작성한 후에는 `pest` 또는 `phpunit` 명령어로 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest`나 `phpunit` 명령어 외에도 `test` Artisan 명령어를 사용할 수 있으며, 이 명령어는 개발 및 디버깅을 용이하게 하는 자세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 적용할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행하기 (Running Tests in Parallel)

기본적으로 Laravel과 Pest/PHPUnit은 단일 프로세스 내에서 테스트를 순차적으로 실행합니다. 하지만 여러 프로세스에 걸쳐 동시에 테스트를 실행하면 테스트 실행 시간을 크게 단축할 수 있습니다. 우선 `brianium/paratest` Composer 패키지를 개발용 의존성으로 설치하세요. 그런 다음 `test` Artisan 명령 실행 시 `--parallel` 옵션을 포함하면 됩니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 사용 가능한 CPU 코어 수만큼 프로세스를 생성합니다. 직접 프로세스 수를 지정하려면 `--processes` 옵션을 사용하세요:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시 `--do-not-cache-result` 같은 일부 Pest/PHPUnit 옵션은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

주 데이터베이스 연결을 설정한 상태라면 Laravel은 병렬 테스트 실행 중 각 프로세스마다 테스트 데이터베이스를 생성하고 마이그레이션을 자동으로 수행합니다. 이때 테스트 데이터베이스명 뒤에는 프로세스별 고유 토큰이 붙습니다. 예를 들어, 두 개의 병렬 프로세스가 있다면 `your_db_test_1`, `your_db_test_2`와 같이 각각 다른 테스트 데이터베이스를 생성하고 사용하게 됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어를 여러 번 실행해도 유지되어, 이후 테스트 실행에서도 재사용됩니다. 다만 `--recreate-databases` 옵션을 사용하면 데이터베이스를 다시 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅(Parallel Testing Hooks)

때때로, 애플리케이션 테스트에서 사용하는 특정 자원을 여러 테스트 프로세스가 안전하게 사용할 수 있게 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`, `tearDown` 시 실행할 코드를 지정할 수 있습니다. 클로저 함수는 각각 현재 프로세스 토큰(`$token`)과 테스트 케이스 인스턴스(`$testCase`)를 인수로 받습니다:

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
#### 병렬 테스트 토큰에 접근하기

애플리케이션 테스트 코드 내 다른 위치에서 현재 병렬 테스트 프로세스의 고유 문자열 식별자(토큰)를 얻고 싶다면 `token` 메서드를 사용하세요. 이 토큰은 개별 테스트 프로세스를 구분하는 문자열이며, 예를 들어 Laravel이 병렬 테스트 프로세스별로 생성하는 테스트 데이터베이스 이름 끝에 자동으로 붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고 (Reporting Test Coverage)

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행하면서 테스트 케이스가 실제로 애플리케이션 코드를 얼마나 커버하는지, 테스트 실행 시 얼마나 많은 코드가 사용되는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제 적용하기

`--min` 옵션으로 애플리케이션에 대한 최소 테스트 커버리지 기준을 지정할 수 있습니다. 이 기준에 미달할 경우 테스트 스위트가 실패 처리됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 실행기는 가장 느린 테스트들을 목록으로 보여주어 어떤 테스트를 개선해야 하는지 쉽게 파악할 수 있는 편리한 기능도 포함하고 있습니다. `test` 명령어에 `--profile` 옵션을 붙여 실행하면 10개의 가장 느린 테스트가 표시됩니다:

```shell
php artisan test --profile
```