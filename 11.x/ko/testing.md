# 테스트: 시작하기

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [병렬 테스트 실행](#running-tests-in-parallel)
    - [테스트 커버리지 보고](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)

<a name="introduction"></a>
## 소개

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)을 이용한 테스트가 기본적으로 지원되며, 애플리케이션을 위해 `phpunit.xml` 파일이 이미 설정되어 있습니다. 프레임워크는 테스트를 효과적으로 작성할 수 있도록 다양한 편리한 헬퍼 메서드도 함께 제공합니다.

기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 하위 디렉터리가 존재합니다. 단위(Unit) 테스트는 코드의 아주 작은 단위에 집중하는 테스트입니다. 대부분의 단위 테스트는 단일 메서드 하나에 집중하기도 합니다. "Unit" 디렉터리의 테스트는 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션의 데이터베이스나 다른 프레임워크 서비스를 사용할 수 없습니다.

기능(Feature) 테스트는 여러 객체의 상호작용이나 JSON 엔드포인트로의 전체 HTTP 요청 등 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로, 대부분의 테스트는 기능(Feature) 테스트로 작성하는 것이 좋습니다. 이러한 유형의 테스트는 시스템 전체가 의도대로 동작하는지 가장 확실하게 보장해줍니다.**

`ExampleTest.php` 파일이 `Feature` 및 `Unit` 테스트 디렉터리 각각에 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 뒤에는 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하여 테스트를 구동할 수 있습니다.

<a name="environment"></a>
## 환경

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [설정 환경](/docs/{{version}}/configuration#environment-configuration)을 자동으로 `testing`으로 지정합니다. 세션과 캐시 역시 자동으로 `array` 드라이버로 설정되어 테스팅 중에는 어떤 세션이나 캐시 데이터도 영구적으로 저장되지 않습니다.

필요하다면 다른 테스트용 환경 설정 값도 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트 실행 전 반드시 `config:clear` 아티즌 명령어로 설정 캐시를 비워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수도 있습니다. 이 파일은 Pest 및 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션으로 아티즌 명령어를 실행할 때, 기본 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성

새 테스트 케이스를 생성하려면 `make:test` 아티즌 명령어를 사용하세요. 기본적으로 테스트 파일은 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용하세요:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]  
> 테스트 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 활용해 사용자 정의가 가능합니다.

테스트가 생성되면, Pest 또는 PHPUnit을 사용해 일반적으로 테스트를 정의하듯 작성할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 사용하세요:

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
     * 간단한 테스트 예시.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]  
> 테스트 클래스에서 직접 `setUp` / `tearDown` 메서드를 정의한다면, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()`을 호출해야 합니다. 일반적으로, 자신만의 `setUp` 시작 부분에서는 `parent::setUp()`을, `tearDown`의 끝부분에서는 `parent::tearDown()`을 호출하세요.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯이, 테스트를 작성한 후에는 `pest` 또는 `phpunit`으로 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` 또는 `phpunit` 명령어 외에도, 아티즌의 `test` 명령어로 테스트를 실행할 수 있습니다. 아티즌 테스트 러너는 개발 및 디버깅에 도움이 되는 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 아티즌 `test` 명령어에도 사용할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬 테스트 실행

기본적으로 Laravel과 Pest/PHPUnit은 하나의 프로세스에서 순차적으로 테스트를 실행합니다. 하지만 테스트를 여러 프로세스에서 동시에 실행하여 실행 시간을 크게 단축할 수 있습니다. 먼저, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그리고 아티즌 `test` 명령어를 실행할 때 `--parallel` 옵션을 추가하세요:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 머신의 CPU 코어 수만큼 프로세스를 생성해서 병렬로 테스트를 실행합니다. 필요하다면 `--processes` 옵션으로 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]  
> 병렬 테스트를 실행할 때, 일부 Pest/PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없는 경우가 있습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결을 구성했다면, Laravel은 각 병렬 프로세스마다 테스트 데이터베이스를 생성하고 마이그레이션을 자동으로 처리해줍니다. 테스트 데이터베이스 이름 끝에는 각 프로세스를 식별할 수 있는 고유의 토큰이 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면, `your_db_test_1`과 `your_db_test_2` 데이터베이스가 생성 및 사용됩니다.

기본적으로 테스트 데이터베이스는 다음번 `test` 아티즌 명령어 실행 시에도 재사용할 수 있도록 유지됩니다. 하지만, `--recreate-databases` 옵션을 이용하면 매번 새로 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅(Hook)

가끔은 여러 테스트 프로세스에서 안전하게 사용할 수 있도록 테스트에서 사용하는 특정 리소스를 미리 준비해야 할 수도 있습니다.

`ParallelTesting` 파사드를 사용하여 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시 실행할 코드를 지정할 수 있습니다. 주어진 클로저는 각각 프로세스 토큰 `$token`과 현재 테스트 케이스 `$testCase` 변수를 전달받습니다:

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

            // 테스트 데이터베이스 생성 시 실행됨...
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

애플리케이션 테스트 코드의 다른 위치에서 현재 병렬 프로세스의 "토큰"을 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 각 테스트 프로세스별로 고유한 문자열이며, 병렬 테스트 간 리소스를 분리할 때 활용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스가 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고

> [!WARNING]  
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때, 테스트 케이스가 실제로 얼마나 많은 애플리케이션 코드를 커버하는지 그리고 어느 코드가 테스트에서 사용되는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 임계치 강제

`--min` 옵션을 사용하여 애플리케이션의 최소 테스트 커버리지 임계치를 설정할 수 있습니다. 임계치에 미달하면 테스트 스위트가 실패하게 됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링

아티즌 테스트 러너에는 애플리케이션에서 가장 느린 테스트를 목록화하는 편리한 기능도 있습니다. `--profile` 옵션과 함께 `test` 명령어를 실행하면, 가장 느린 10개의 테스트가 리스트로 출력되어 테스트 스위트의 성능 개선이 필요한 부분을 쉽게 찾아볼 수 있습니다:

```shell
php artisan test --profile
```
