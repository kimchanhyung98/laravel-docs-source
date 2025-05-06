# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간소화하는 것과 더불어, Laravel은 애플리케이션의 [사용자 지정 콘솔 커맨드](/docs/{{version}}/artisan)를 테스트할 수 있는 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

먼저, Artisan 커맨드의 종료 코드(exit code)에 대한 어설션 방법을 알아보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용하여 Artisan 커맨드를 호출하고, `assertExitCode` 메서드로 커맨드가 특정 종료 코드로 완료되었는지 검증할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 커맨드를 테스트합니다.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

`assertNotExitCode` 메서드를 사용하여 커맨드가 특정 종료 코드로 끝나지 않았음을 확인할 수도 있습니다:

    $this->artisan('inspire')->assertNotExitCode(1);

일반적으로 모든 터미널 명령어는 성공 시 `0`의 상태 코드로 종료되고, 실패 시 0이 아닌 코드로 종료됩니다. 따라서, 편의상 `assertSuccessful` 및 `assertFailed` 어설션을 통해 커맨드가 성공적으로 종료되었는지, 그렇지 않은지를 검증할 수 있습니다:

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel에서는 `expectsQuestion` 메서드를 사용하여 콘솔 커맨드의 사용자 입력을 손쉽게 "모킹(mock)"할 수 있습니다. 또한, 콘솔 커맨드에서 출력될 것으로 예상되는 종료 코드와 텍스트를 각각 `assertExitCode`, `expectsOutput` 메서드를 통해 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 커맨드를 살펴봅시다:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

이 커맨드는 다음과 같은 테스트로 검증할 수 있습니다:

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
 * 콘솔 커맨드를 테스트합니다.
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

[Laravel Prompts](/docs/{{version}}/prompts)에서 제공하는 `search` 또는 `multisearch` 함수를 사용하는 경우, `expectsSearch` 어설션을 이용해 사용자의 입력, 검색 결과, 선택 값까지 모킹할 수 있습니다:

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
 * 콘솔 커맨드를 테스트합니다.
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

또한, 콘솔 커맨드가 아무 출력도 하지 않음을 `doesntExpectOutput` 메서드를 사용하여 검증할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 커맨드를 테스트합니다.
 */
public function test_console_command(): void
{
    $this->artisan('example')
            ->doesntExpectOutput()
            ->assertExitCode(0);
}
```

`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드는 출력 값의 일부가 포함되는지, 포함되지 않는지를 검증할 때 사용할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 커맨드를 테스트합니다.
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

"예" 또는 "아니오"와 같은 답변의 확인을 기대하는 커맨드를 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### 테이블 기대값

커맨드에서 Artisan의 `table` 메서드를 사용해 테이블 형태로 정보를 보여주는 경우, 전체 표에 대해 출력 기대값을 작성하는 것은 번거로울 수 있습니다. 이런 경우 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블 헤더, 두 번째 인자로 테이블 데이터를 받습니다:

    $this->artisan('users:all')
        ->expectsTable([
            'ID',
            'Email',
        ], [
            [1, 'taylor@example.com'],
            [2, 'abigail@example.com'],
        ]);

<a name="console-events"></a>
## 콘솔 이벤트

기본적으로, 애플리케이션의 테스트를 실행하는 동안에는 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트가 디스패치되지 않습니다. 하지만, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하면 해당 이벤트를 활성화할 수 있습니다:

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