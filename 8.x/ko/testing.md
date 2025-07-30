# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성하기](#creating-tests)
- [테스트 실행하기](#running-tests)
    - [병렬로 테스트 실행하기](#running-tests-in-parallel)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 PHPUnit을 이용한 테스트 지원이 기본적으로 포함되어 있으며, `phpunit.xml` 파일이 이미 애플리케이션에 맞게 설정되어 있습니다. 프레임워크는 또한 애플리케이션을 표현력 있게 테스트할 수 있도록 편리한 헬퍼 메서드도 제공합니다.

기본적으로, 애플리케이션의 `tests` 디렉토리에는 `Feature`와 `Unit` 두 개의 하위 디렉토리가 있습니다. 유닛 테스트(Unit test)는 코드에서 매우 작고 독립적인 부분에 집중하는 테스트를 의미합니다. 대부분의 유닛 테스트는 아마도 단일 메서드에 집중할 것입니다. "Unit" 테스트 디렉토리에 있는 테스트들은 Laravel 애플리케이션을 부팅하지 않기 때문에 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

반면에 Feature 테스트는 여러 객체가 상호작용하는 방식이나 JSON 엔드포인트에 대한 전체 HTTP 요청까지 포함하여 더 큰 코드 범위를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 Feature 테스트여야 하며, 이런 종류의 테스트가 시스템 전체가 의도대로 작동함을 가장 신뢰할 수 있게 보장합니다.**

`Feature`와 `Unit` 테스트 디렉토리 모두에 `ExampleTest.php` 파일이 기본으로 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행해 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 자동으로 환경 구성을 `testing`으로 설정합니다. 또한 Laravel은 테스트 중에는 세션 및 캐시 드라이버를 `array`로 자동 설정하여, 테스트 실행 중 세션이나 캐시 데이터가 저장되지 않도록 합니다.

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수들은 애플리케이션의 `phpunit.xml` 파일에서 설정 가능하지만, 테스트 실행 전에 반드시 `config:clear` Artisan 명령어로 구성 캐시를 지우는 것을 잊지 마세요!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 PHPUnit 테스트 실행 시 또는 `--env=testing` 옵션을 사용해 Artisan 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
#### `CreatesApplication` 트레이트

Laravel은 애플리케이션의 기본 `TestCase` 클래스에 적용되는 `CreatesApplication` 트레이트를 포함하고 있습니다. 이 트레이트는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드를 제공합니다. Laravel의 병렬 테스트 기능 등 일부 기능이 이 트레이트에 의존하므로, 원래 위치에 그대로 두는 것이 중요합니다.

<a name="creating-tests"></a>
## 테스트 생성하기 (Creating Tests)

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용하세요. 기본적으로 테스트는 `tests/Feature` 디렉토리에 생성됩니다:

```
php artisan make:test UserTest
```

만약 `tests/Unit` 디렉토리에 테스트를 생성하려면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 테스트를 만들고 싶다면, `make:test` 명령어에 `--pest` 옵션을 추가하세요:

```
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!TIP]
> 테스트 스텁(stub)은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

테스트가 생성되면, 평소대로 [PHPUnit](https://phpunit.de)을 사용해 테스트 메서드를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하세요:

```
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $this->assertTrue(true);
    }
}
```

> [!NOTE]
> 테스트 클래스 내에서 `setUp` / `tearDown` 메서드를 직접 정의할 경우 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

앞서 설명했듯, 테스트를 작성한 뒤에는 `phpunit` 명령어로 테스트를 실행할 수 있습니다:

```
./vendor/bin/phpunit
```

또한 `phpunit` 명령어 외에 Artisan의 `test` 명령어로도 테스트를 실행할 수 있습니다. Artisan 테스트 실행기는 개발 및 디버깅을 돕기 위해 상세한 테스트 보고서를 제공합니다:

```
php artisan test
```

`phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 동일하게 전달할 수 있습니다:

```
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행하기 (Running Tests In Parallel)

기본적으로 Laravel과 PHPUnit은 단일 프로세스에서 순차적으로 테스트를 실행합니다. 하지만 여러 프로세스에서 테스트를 동시에 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면, 애플리케이션이 `nunomaduro/collision` 패키지 버전 `^5.3` 이상에 의존하는지 확인하세요. 그런 다음 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가합니다:

```
php artisan test --parallel
```

기본적으로 Laravel은 머신의 CPU 코어 수만큼 프로세스를 생성합니다. 생성할 프로세스 수는 `--processes` 옵션으로 조절할 수 있습니다:

```
php artisan test --parallel --processes=4
```

> [!NOTE]
> 병렬 테스트 실행 시 `--do-not-cache-result` 같은 일부 PHPUnit 옵션은 지원되지 않을 수 있습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스 (Parallel Testing & Databases)

Laravel은 병렬 테스트 프로세스 각각을 위해 테스트 데이터베이스 생성과 마이그레이션을 자동으로 처리합니다. 각 프로세스에 대해 고유한 프로세스 토큰이 붙은 테스트 데이터베이스가 만들어집니다. 예를 들어, 병렬 테스트가 2개 프로세스일 경우, `your_db_test_1`, `your_db_test_2`와 같은 테스트 데이터베이스가 생성 및 사용됩니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어가 여러 번 호출되더라도 유지되어 다음 호출 시 다시 사용 가능합니다. 하지만 `--recreate-databases` 옵션을 사용해 데이터베이스를 재생성할 수도 있습니다:

```
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅 (Parallel Testing Hooks)

가끔 애플리케이션 테스트가 사용하는 자원을 여러 테스트 프로세스가 안전하게 공유하도록 준비해야 할 때가 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 각각 현재 프로세스 토큰 `$token`과 테스트 케이스 객체 `$testCase`를 인자로 받습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
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

        // 테스트 데이터베이스가 생성될 때 실행
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
#### 병렬 테스트 토큰 접근하기 (Accessing The Parallel Testing Token)

애플리케이션의 테스트 코드 어디서든 현재 병렬 테스트 프로세스의 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 고유한 문자열 식별자이며, 병렬 테스트 프로세스별로 자원을 분리하는 데 활용됩니다. 예를 들어, Laravel이 생성하는 테스트 데이터베이스 이름 뒤에 자동으로 이 토큰을 붙입니다:

```
$token = ParallelTesting::token();
```