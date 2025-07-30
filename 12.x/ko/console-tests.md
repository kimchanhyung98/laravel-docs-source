# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대치](#success-failure-expectations)
- [입력 / 출력 기대치](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간소화하는 것 외에도, Laravel은 애플리케이션의 [사용자 정의 콘솔 명령어](/docs/12.x/artisan)를 테스트할 수 있는 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대치

먼저, Artisan 명령어의 종료 코드에 대한 어설션(assertion)을 수행하는 방법을 알아보겠습니다. 이를 위해 테스트 내에서 `artisan` 메서드를 사용해 Artisan 명령어를 호출합니다. 그리고 `assertExitCode` 메서드를 사용하여 명령어가 지정된 종료 코드로 완료되었는지 확인합니다:

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

`assertNotExitCode` 메서드를 이용하면 명령어가 특정 종료 코드로 종료되지 않았음을 어설션할 수 있습니다:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

일반적으로 터미널 명령어는 성공 시 종료 코드 `0`을, 실패 시에는 0이 아닌 값을 반환합니다. 따라서 편의를 위해 `assertSuccessful`과 `assertFailed` 어설션을 사용해 명령어가 성공적으로 종료되었는지 또는 실패했는지 손쉽게 확인할 수 있습니다:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대치

Laravel은 `expectsQuestion` 메서드를 사용해 콘솔 명령어에서 사용자 입력을 쉽게 "모킹(mock)"할 수 있도록 지원합니다. 또한, 콘솔 명령어가 출력할 것으로 예상하는 종료 코드와 텍스트를 `assertExitCode` 및 `expectsOutput` 메서드를 통해 지정할 수 있습니다. 다음과 같은 콘솔 명령어를 예로 들어 보겠습니다:

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

다음과 같이 이 명령어를 테스트할 수 있습니다:

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

만약 [Laravel Prompts](/docs/12.x/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 활용한다면, `expectsSearch` 어설션을 사용해 사용자의 입력, 검색 결과 및 선택을 모킹할 수 있습니다:

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

또한 콘솔 명령어가 출력을 내지 않을 것으로 예상할 때는 `doesntExpectOutput` 메서드를 사용해 어설션할 수 있습니다:

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

출력의 일부만 포함하는지 여부를 검증하려면 `expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드를 사용하세요:

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
#### 확인 기대치

"예/아니오" 답변을 요구하는 확인(confirm) 절차가 포함된 명령어를 작성할 때는 `expectsConfirmation` 메서드를 사용하세요:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 기대치

명령어가 Artisan의 `table` 메서드를 사용해 정보를 테이블 형태로 출력할 때, 전체 테이블 출력에 대한 기대치를 작성하는 것은 다소 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용하는 것이 편리합니다. 이 메서드는 첫 번째 인수로 테이블의 헤더 배열을, 두 번째 인수로 테이블의 데이터 배열을 받습니다:

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

기본적으로 애플리케이션 테스트 실행 시 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 발생하지 않습니다. 하지만 특정 테스트 클래스에서 이 이벤트들을 활성화하려면, 해당 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하세요:

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