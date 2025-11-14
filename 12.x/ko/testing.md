# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [테스트 병렬 실행](#running-tests-in-parallel)
    - [테스트 커버리지 리포트](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)
- [설정 캐싱](#caching-configuration)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계된 프레임워크입니다. 실제로 [Pest](https://pestphp.com) 및 [PHPUnit](https://phpunit.de)와의 테스트 지원이 기본 내장되어 있으며, 애플리케이션에는 이미 `phpunit.xml` 파일이 설정되어 있습니다. 또한 Laravel은 애플리케이션을 손쉽게 테스트할 수 있도록 다양한 헬퍼 메서드를 제공합니다.

기본적으로 `tests` 디렉토리는 `Feature`와 `Unit`이라는 두 개의 하위 디렉토리를 포함합니다. 단위 테스트(Unit test)는 코드의 아주 작은, 고립된 부분에 집중하여 테스트합니다. 실제로 대부분의 단위 테스트는 단일 메서드에 초점을 맞춥니다. "Unit" 디렉토리에 있는 테스트는 Laravel 애플리케이션을 부트시키지 않으므로 데이터베이스나 다른 프레임워크 서비스를 사용할 수 없습니다.

기능 테스트(Feature test)는 코드의 더 넓은 부분을 테스트합니다. 여러 객체가 서로 어떻게 상호작용하는지, 심지어 JSON 엔드포인트로의 전체 HTTP 요청을 포함할 수도 있습니다. **일반적으로 전체 테스트의 대부분은 기능 테스트가 되어야 하며, 이러한 형식의 테스트가 시스템 전체가 의도대로 작동하는지에 대한 신뢰도를 가장 높여줍니다.**

`ExampleTest.php` 파일이 `Feature`와 `Unit` 디렉토리 각각에 제공되어 있습니다. 새로운 Laravel 애플리케이션 설치 후, `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [구성 환경](/docs/12.x/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 세션과 캐시를 `array` 드라이버로 자동 설정하므로, 테스트 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

필요에 따라 다른 테스트 환경용 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 비워주어야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로 프로젝트의 루트 디렉토리에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest 및 PHPUnit 테스트를 실행하거나 Artisan 명령어에 `--env=testing` 옵션을 사용할 때, 기본 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성 (Creating Tests)

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 생성된 테스트는 `tests/Feature` 디렉토리에 위치합니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉토리 내에 테스트를 생성하려면, `make:test` 명령어를 실행할 때 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의가 가능합니다.

테스트가 생성되면, Pest 또는 PHPUnit을 사용하여 평소처럼 테스트 코드를 작성할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 사용하세요:

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
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스에서 직접 `setUp` / `tearDown` 메서드를 정의할 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()`을 각각의 메서드에서 호출해야 합니다. 일반적으로 `setUp` 메서드 초반에는 `parent::setUp()`을, `tearDown` 메서드 끝에는 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

앞서 설명했듯이, 테스트를 작성한 후에는 `pest` 또는 `phpunit`으로 테스트를 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` 또는 `phpunit` 커맨드 외에도 Artisan `test` 명령어를 사용하여 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 쉽게 할 수 있도록 자세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan의 `test` 명령어에도 동일하게 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 테스트 병렬 실행 (Running Tests in Parallel)

기본적으로 Laravel과 Pest / PHPUnit은 테스트를 단일 프로세스에서 순차적으로 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 테스트 소요 시간을 크게 줄일 수 있습니다. 먼저 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치한 후, `test` Artisan 명령어에 `--parallel` 옵션을 추가하세요:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로, 사용자의 시스템에 할당된 CPU 코어 수만큼 프로세스가 생성됩니다. 프로세스 개수는 `--processes` 옵션으로 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 설정되어 있으면, Laravel은 각 병렬 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션을 진행합니다. 테스트 데이터베이스 이름은 각 프로세스별로 고유한 토큰이 접미사로 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면 `your_db_test_1`, `your_db_test_2`와 같은 형식의 데이터베이스가 만들어집니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어 호출 간에 유지되어, 이후 테스트 실행 시 재사용됩니다. 데이터베이스를 새로 생성하려면 `--recreate-databases` 옵션을 사용할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

때때로, 애플리케이션의 테스트가 여러 프로세스에서 안전하게 리소스를 사용할 수 있도록 준비해야 할 필요가 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`, `tearDown` 시 실행할 코드를 지정할 수 있습니다. 전달된 클로저에는 각 프로세스 토큰과 현재 테스트 케이스를 담은 `$token`, `$testCase` 변수가 주어집니다:

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
     * Bootstrap any application services.
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

테스트 코드 내에서 현재 병렬 프로세스의 "토큰"에 접근하려면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 각각의 병렬 테스트 프로세스가 가지는 고유한 문자열 식별자이며, 이를 통해 병렬 프로세스 간 리소스를 구분할 수 있습니다. Laravel은 병렬 테스트 프로세스마다 생성된 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포트 (Reporting Test Coverage)

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 각 테스트 케이스가 실제로 애플리케이션 코드를 얼마만큼 커버하는지 파악하고 싶을 수 있습니다. 이를 위해 테스트 실행 시 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제 적용

`--min` 옵션을 사용하여 애플리케이션의 최소 테스트 커버리지 기준을 지정할 수 있습니다. 이 기준을 충족하지 못하면 테스트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 러너는 가장 느린 테스트 항목을 쉽게 확인할 수 있는 기능도 포함하고 있습니다. `--profile` 옵션을 사용하여 `test` 명령어를 실행하면, 가장 느린 10개의 테스트 목록이 표시되어 느린 테스트를 개선함으로써 전체 테스트 스위트의 속도를 빠르게 할 수 있습니다:

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

테스트를 실행할 때 Laravel은 테스트 메서드마다 애플리케이션을 부팅합니다. 설정 캐시 파일이 없으면, 매 테스트마다 모든 설정 파일을 매번 읽어들이게 됩니다. 테스트 전체 실행 동안 한 번만 설정을 빌드하고 재사용하려면, `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}
```
