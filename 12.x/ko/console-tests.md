# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

Laravel은 HTTP 테스트를 단순화할 뿐만 아니라, 애플리케이션의 [사용자 정의 콘솔 명령어](/docs/{{version}}/artisan)를 테스트할 수 있는 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

먼저, Artisan 명령어의 종료 코드를 어떻게 단언할 수 있는지 살펴보겠습니다. 이를 위해 `artisan` 메서드를 사용하여 테스트 내에서 Artisan 명령어를 실행하고, `assertExitCode` 메서드를 사용해 해당 명령어가 지정한 종료 코드로 완료되었는지 단언합니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

명령어가 지정한 종료 코드로 종료되지 않았음을 단언하려면 `assertNotExitCode` 메서드를 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

일반적으로 모든 터미널 명령어는 성공 시 상태 코드 `0`으로, 실패 시 0이 아닌 종료 코드로 종료됩니다. 따라서, 편의상 명령어가 정상적으로 또는 비정상적으로 종료되었는지 단언하기 위해 `assertSuccessful`과 `assertFailed` 어설션을 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel은 `expectsQuestion` 메서드를 사용하여 콘솔 명령어에 대한 사용자 입력을 손쉽게 "모킹"할 수 있습니다. 또한, `assertExitCode`와 `expectsOutput` 메서드를 통해 콘솔 명령어가 출력하는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령어가 있다고 가정해봅시다:

```php
Artisan::command('question', function () {
    $name = $this->ask('What is your name?');

    $language = $this->choice('Which language do you prefer?', [
        'PHP',
        'Ruby',
        'Python',
    ]);

    $this->line('Your name is '.$name.' and you prefer '.$language.'.');
});
```

이 명령어는 아래와 같이 테스트할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
}
```

[Laravel Prompts](/docs/{{version}}/prompts)에서 제공하는 `search` 또는 `multisearch` 함수를 사용할 때는, `expectsSearch` 어설션으로 사용자 입력, 검색 결과, 선택 값을 모킹할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
}
```

콘솔 명령어가 아무런 출력도 생성하지 않았음을 단언하려면 `doesntExpectOutput` 메서드를 사용할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
}
```

출력 중 일부 문자열만 포함하는지 여부를 단언하려면 `expectsOutputToContain`과 `doesntExpectOutputToContain` 메서드를 사용할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
#### 확인(Confirmation) 기대값

"예" 또는 "아니오"와 같이 확인(answer confirmation)을 요구하는 명령을 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 기대값

명령어가 Artisan의 `table` 메서드를 사용해 정보를 테이블 형식으로 출력할 경우, 전체 테이블에 대한 출력 기대값을 작성하는 것은 번거로울 수 있습니다. 이때는 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블 헤더, 두 번째 인자로 테이블 데이터를 받습니다:

```php
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);
```

<a name="console-events"></a>
## 콘솔 이벤트

기본적으로, 애플리케이션 테스트 실행 시 `Illuminate\Console\Events\CommandStarting`과 `Illuminate\Console\Events\CommandFinished` 이벤트는 디스패치되지 않습니다. 하지만, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하면 해당 이벤트를 활성화할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

uses(WithConsoleEvents::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithConsoleEvents;
use Tests\TestCase;

class ConsoleEventTest extends TestCase
{
    use WithConsoleEvents;

    // ...
}
```
