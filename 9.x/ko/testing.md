# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성하기](#creating-tests)
- [테스트 실행하기](#running-tests)
    - [병렬로 테스트 실행하기](#running-tests-in-parallel)
    - [테스트 커버리지 보고하기](#reporting-test-coverage)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 사실, PHPUnit을 이용한 테스트 지원이 기본으로 포함되어 있고 애플리케이션용 `phpunit.xml` 파일이 이미 설정되어 있습니다. 프레임워크는 애플리케이션 테스트를 직관적으로 할 수 있도록 편리한 헬퍼 메서드도 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉토리 안에는 `Feature`와 `Unit`이라는 두 개의 디렉토리가 있습니다. 단위 테스트(Unit test)는 코드의 아주 작고 독립적인 부분에 집중하는 테스트입니다. 대부분 단위 테스트는 하나의 메서드만을 테스트하는 경우가 많습니다. "Unit" 테스트 디렉토리 내 테스트는 Laravel 애플리케이션을 부트스트랩하지 않기 때문에 데이터베이스나 다른 프레임워크 서비스를 사용할 수 없습니다.

기능 테스트(Feature test)는 여러 객체 간의 상호작용이나 JSON 엔드포인트로의 전체 HTTP 요청 등을 포함해 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트가 되어야 하며, 이러한 테스트가 시스템 전체가 의도한 대로 작동하는지에 대한 가장 확신을 제공합니다.**

`Feature`와 `Unit` 디렉토리에는 각각 `ExampleTest.php` 파일이 기본 제공됩니다. 새 Laravel 애플리케이션 설치 후에는 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수에 따라 자동으로 [설정 환경](/docs/9.x/configuration#environment-configuration)을 `testing`으로 설정합니다. 또한 테스트 중에는 세션과 캐시를 `array` 드라이버로 자동 설정해 세션이나 캐시 데이터가 저장되지 않도록 합니다.

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에 설정할 수 있지만, 테스트 실행 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 비워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

또한, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령을 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

Laravel은 애플리케이션의 기본 `TestCase` 클래스에 적용되는 `CreatesApplication` 트레이트를 포함합니다. 이 트레이트는 테스트를 실행하기 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드를 포함합니다. Laravel 병렬 테스트 기능 등 일부 기능은 이 트레이트가 원래 위치에 있어야 하므로 그대로 두는 것이 중요합니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 테스트는 `tests/Feature` 디렉토리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉토리에 테스트를 생성하려면 `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 테스트를 생성하고 싶다면 `make:test` 명령어에 `--pest` 옵션을 추가하세요:

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]
> 테스트 스텁은 [스텁 게시](/docs/9.x/artisan#stub-customization) 기능을 통해 커스터마이징할 수 있습니다.

테스트가 생성되면, 평소대로 [PHPUnit](https://phpunit.de) 형식으로 테스트 메서드를 작성하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하세요:

```
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 간단한 기본 테스트 예제입니다.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스 내에 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 언급한 것처럼, 테스트를 작성한 후에는 `phpunit`으로 실행할 수 있습니다:

```shell
./vendor/bin/phpunit
```

`phpunit` 명령어 외에 `test` Artisan 명령어로도 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발 및 디버깅을 쉽게 해주는 자세한 테스트 보고서를 제공합니다:

```shell
php artisan test
```

`phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행하기 (Running Tests In Parallel)

기본적으로 Laravel과 PHPUnit은 한 프로세스 내에서 테스트를 순차적으로 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트 소요 시간을 크게 줄일 수 있습니다. 시작하려면, 애플리케이션에 `nunomaduro/collision` 패키지 `^5.3` 이상 버전이 의존성으로 포함되어 있는지 확인하세요. 그런 다음 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가합니다:

```shell
php artisan test --parallel
```

기본적으로 Laravel은 컴퓨터의 CPU 코어 수만큼 프로세스를 만듭니다. 프로세스 수를 조정하려면 `--processes` 옵션을 사용하세요:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시 `--do-not-cache-result` 같은 일부 PHPUnit 옵션은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 설정되어 있으면 Laravel은 병렬 테스트 프로세스마다 테스트 데이터베이스를 자동으로 생성하고 마이그레이션합니다. 각 병렬 프로세스에서 사용하는 테스트 데이터베이스는 프로세스별 고유 토큰이 접미사로 붙습니다. 예를 들어 프로세스가 두 개라면 `your_db_test_1`과 `your_db_test_2`라는 테스트 데이터베이스가 생성되고 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어를 여러 번 호출하더라도 재사용됩니다. 다시 생성하려면 `--recreate-databases` 옵션을 붙이세요:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅 (Parallel Testing Hooks)

때로는 애플리케이션의 테스트가 여러 테스트 프로세스에서 안전하게 자원을 공유할 수 있도록 특정 준비 작업이 필요할 수 있습니다.

`ParallelTesting` 퍼사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp` 및 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 각 프로세스 토큰과 현재 테스트 케이스를 담은 `$token`과 `$testCase` 변수를 인자로 받습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
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

        // 테스트 데이터베이스 생성 시 실행...
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
```

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근하기

테스트 코드의 다른 위치에서 현재 병렬 프로세스의 "토큰"을 조회하려면 `token` 메서드를 사용하세요. 이 토큰은 병렬 테스트 프로세스별로 고유한 문자열 식별자로, 테스트 리소스를 분리하는 데 이용됩니다. 예를 들어 병렬 테스트가 생성하는 테스트 데이터베이스명 끝에 이 토큰이 자동 추가됩니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고하기 (Reporting Test Coverage)

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 설치되어 있어야 합니다.

애플리케이션 테스트 실행 시, 테스트 케이스가 실제로 애플리케이션 코드를 얼마나 커버하는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 설정하기

`--min` 옵션을 사용하면 애플리케이션 테스트가 만족해야 할 최소 커버리지 기준을 정의할 수 있습니다. 이 기준 미만이면 테스트 스위트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```