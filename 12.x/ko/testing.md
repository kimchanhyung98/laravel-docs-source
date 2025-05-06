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

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)를 활용한 테스트 지원이 기본적으로 제공되며, 애플리케이션에 `phpunit.xml` 파일이 이미 설정되어 있습니다. 또한 프레임워크에는 애플리케이션을 명확하게 테스트할 수 있도록 도와주는 다양한 헬퍼 메서드도 함께 제공됩니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 하위 디렉터리가 있습니다. 유닛 테스트(Unit Test)는 코드의 매우 작고 독립적인 부분에 초점을 맞춘 테스트입니다. 실제로 대부분의 유닛 테스트는 한 개의 메서드에 집중하게 됩니다. "Unit" 테스트 디렉터리 내의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로, 애플리케이션의 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

피처 테스트(Feature Test)는 여러 객체 간 상호작용이나, JSON 엔드포인트에 대한 전체 HTTP 요청 등 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 피처 테스트여야 하며, 이러한 테스트가 전체 시스템이 의도한 대로 동작함을 가장 확실하게 보장합니다.**

`Feature`와 `Unit` 테스트 디렉터리 모두에 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 때문에 [환경 구성](/docs/{{version}}/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 세션 및 캐시도 자동으로 `array` 드라이버로 설정되어, 테스트 중에는 세션이나 캐시 데이터가 영구적으로 저장되지 않습니다.

필요하다면 추가적인 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 구성 캐시를 지워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

또한 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest 및 PHPUnit 테스트 실행 시, 또는 `--env=testing` 옵션과 함께 Artisan 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리 내에 테스트를 생성하고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁(stub)은 [스텁 커스터마이징](/docs/{{version}}/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

테스트가 생성되면, Pest 또는 PHPUnit을 사용해 일반적으로 테스트를 작성하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 사용하세요:

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
     * 기본 테스트 예제.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스 내에 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로 자신의 `setUp` 메서드 시작 부분에는 `parent::setUp()`을, `tearDown` 메서드 마지막에는 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯이, 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용하여 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` 또는 `phpunit` 명령 이외에도, `test` Artisan 명령어를 사용하는 것도 가능합니다. Artisan 테스트 러너는 개발 및 디버깅을 돕기 위해 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest`나 `phpunit`에 전달할 수 있는 모든 인자를 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행

기본적으로, Laravel과 Pest / PHPUnit은 단일 프로세스 내에서 테스트를 순차적으로 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 테스트 실행 시간을 크게 단축할 수 있습니다. 시작하려면, `brianium/paratest` Composer 패키지를 개발 의존성(dev)으로 설치해야 합니다. 이후, `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가하세요:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 시스템의 CPU 코어 수만큼의 프로세스를 생성합니다. 하지만 `--processes` 옵션으로 프로세스 수를 조절할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때는, 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 올바르게 구성되어 있다면, Laravel은 각 병렬 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 테스트 데이터베이스는 각 프로세스에 고유한 토큰이 접미사로 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면 Laravel은 `your_db_test_1`과 `your_db_test_2` 데이터베이스를 생성 및 사용하게 됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어가 여러 번 호출되더라도 유지되어, 이후에도 재사용됩니다. 하지만 `--recreate-databases` 옵션을 사용하면 데이터베이스를 새로 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅(Hook)

때로는 애플리케이션 테스트에 사용되는 리소스를 별도의 테스트 프로세스에서 안전하게 사용할 수 있도록 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 사용하면, 프로세스나 테스트 케이스의 `setUp` 및 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰과 현재 테스트 케이스(`$token`, `$testCase`)를 전달받습니다:

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

        // 테스트 데이터베이스가 생성될 때 실행됩니다...
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

애플리케이션 테스트 코드의 다른 위치에서도 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 식별하는 고유 문자열로, 병렬 테스트 프로세스 간에 리소스를 구분하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스로 생성된 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포트

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 각 테스트 케이스가 실제로 애플리케이션 코드를 얼마나 커버(테스트)하는지 파악하고 싶을 수 있습니다. 이를 위해 `test` 명령어를 실행할 때 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 임계값 적용

`--min` 옵션을 사용하여 애플리케이션의 최소 테스트 커버리지 임계값을 지정할 수 있습니다. 이 임계값을 충족하지 못하면 테스트가 실패하게 됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링

Artisan 테스트 러너에는 애플리케이션의 가장 느린 테스트를 간편하게 목록으로 확인할 수 있는 기능도 포함되어 있습니다. `test` 명령어를 `--profile` 옵션과 함께 실행하면, 가장 느린 10개의 테스트가 표시되어 테스트 속도를 개선해야 할 대상을 쉽게 파악할 수 있습니다:

```shell
php artisan test --profile
```
