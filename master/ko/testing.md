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

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로, [Pest](https://pestphp.com) 및 [PHPUnit](https://phpunit.de)과의 테스트 지원이 기본적으로 포함되어 있으며, 이미 `phpunit.xml` 파일이 애플리케이션에 설정되어 있습니다. 또한 프레임워크에는 어플리케이션을 명확하게 테스트할 수 있도록 해주는 편리한 헬퍼 메서드들도 함께 제공됩니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 디렉터리가 있습니다. 단위 테스트(Unit test)는 코드의 아주 작고 고립된 부분에 집중하는 테스트입니다. 대부분의 단위 테스트는 아마도 하나의 메서드에 집중합니다. "Unit" 테스트 디렉터리 내부의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로, 애플리케이션의 데이터베이스나 다른 프레임워크 서비스를 이용할 수 없습니다.

기능 테스트(Feature test)는 여러 객체들이 서로 어떻게 상호작용하는지 또는 JSON 엔드포인트에 대한 전체 HTTP 요청까지 포함해 코드의 더 넓은 부분을 테스트할 수 있습니다. **일반적으로, 대부분의 테스트는 기능 테스트가 되어야 하며, 이러한 유형의 테스트가 시스템 전체가 의도한 대로 동작하는지에 대한 가장 큰 신뢰를 제공합니다.**

`ExampleTest.php` 파일은 `Feature`와 `Unit` 테스트 디렉터리 모두에 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령을 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수로 인해 [설정 환경](/docs/{{version}}/configuration#environment-configuration)이 자동으로 `testing`으로 설정됩니다. Laravel은 또한 세션과 캐시를 `array` 드라이버로 자동 설정하여, 테스트 중에 세션 또는 캐시 데이터가 영구적으로 저장되지 않도록 합니다.

필요하다면 추가로 테스트 환경의 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 `config:clear` Artisan 명령어로 설정 캐시를 꼭 삭제해야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가적으로, 프로젝트의 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션으로 Artisan 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로, 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리 내에 테스트를 생성하고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁(Stub)은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

테스트가 생성되었으면, Pest 또는 PHPUnit을 이용해 평소처럼 테스트를 정의하면 됩니다. 테스트 실행은 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어로 할 수 있습니다:

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
> 테스트 클래스 내에 직접 `setUp` / `tearDown` 메서드를 정의할 경우, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 각각 호출해야 합니다. 일반적으로, `setUp` 메서드 시작 부분에서 `parent::setUp()`을, `tearDown` 메서드 끝에서 `parent::tearDown()`을 호출하면 됩니다.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯, 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용하여 테스트를 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` 또는 `phpunit` 명령 외에도, `test` Artisan 명령어를 사용하여 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발 및 디버깅을 쉽게 하기 위해 상세한 테스트 보고서를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달 가능한 모든 인자를 Artisan `test` 명령에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행

기본적으로 Laravel과 Pest / PHPUnit은 테스트를 한 개의 프로세스에서 순차적으로 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트에 소요되는 시간을 크게 줄일 수 있습니다. 우선, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그런 다음 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 포함하면 됩니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 사용 가능한 CPU 코어 수만큼 프로세스를 생성합니다. 원한다면 `--processes` 옵션으로 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때에는 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 설정되어 있다면, Laravel은 테스트를 실행하는 각 병렬 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 테스트 데이터베이스 이름은 프로세스마다 고유한 토큰이 접미사로 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면, Laravel은 `your_db_test_1`과 `your_db_test_2`와 같은 테스트 데이터베이스를 생성 및 사용합니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령 호출 사이에 그대로 유지되어, 이후의 `test` 실행에서도 재사용됩니다. 하지만, `--recreate-databases` 옵션을 사용하여 데이터베이스를 새로 만들 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

가끔은 애플리케이션 테스트에서 여러 테스트 프로세스가 안전하게 사용할 수 있도록 특정 리소스를 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 이용하면 프로세스 또는 테스트 케이스의 `setUp` 및 `tearDown` 시점에 코드를 실행하도록 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰을 담은 `$token`과 현재 테스트 케이스인 `$testCase`를 각각 파라미터로 받습니다:

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
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
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
#### 병렬 테스트 토큰 접근

애플리케이션 테스트 코드의 다른 위치에서 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스에 대한 고유한 문자열 식별자이며, 병렬 테스트 프로세스별로 리소스를 분리하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스가 생성한 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포트

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 실제로 테스트들이 애플리케이션 코드를 얼마나 커버하는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령 실행 시 `--coverage` 옵션을 전달할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제 적용

`--min` 옵션을 이용해 애플리케이션의 최소 테스트 커버리지 기준을 정의할 수 있습니다. 이 기준에 미달할 경우 테스트 스위트는 실패하게 됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링

Artisan 테스트 러너에는 애플리케이션의 가장 느린 테스트 목록을 출력하는 편리한 기능도 포함되어 있습니다. `--profile` 옵션과 함께 `test` 명령어를 실행하면 가장 느린 10개의 테스트 목록이 출력되어, 테스트 스위트의 속도를 향상시킬 수 있는 테스트를 쉽게 찾아볼 수 있습니다:

```shell
php artisan test --profile
```
