# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

Laravel은 HTTP 테스트를 단순화할 뿐 아니라, 애플리케이션의 [사용자 정의 콘솔 커맨드](/docs/{{version}}/artisan)를 테스트하기 위한 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

먼저, Artisan 커맨드의 종료 코드(exit code)에 대해 검증하는 방법을 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용해 Artisan 커맨드를 호출하고, 그 결과가 특정 종료 코드로 끝났는지 `assertExitCode` 메서드로 검증할 수 있습니다.

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

특정 종료 코드로 종료되지 않았는지 검증하려면 `assertNotExitCode` 메서드를 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

일반적으로 모든 터미널 커맨드는 성공 시 `0` 코드로, 실패 시 0이 아닌 코드로 종료됩니다. 따라서, 간편하게 성공 혹은 실패를 검증하고 싶을 때는 `assertSuccessful`과 `assertFailed` 어서션을 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel은 `expectsQuestion` 메서드를 사용해 콘솔 커맨드에서 사용자 입력을 손쉽게 "모킹(mock)"할 수 있도록 해줍니다. 또한, 콘솔 커맨드가 출력해야 하는 종료 코드와 텍스트 역시 `assertExitCode` 및 `expectsOutput` 메서드를 사용해 기대값을 지정할 수 있습니다. 다음과 같은 커맨드 예시를 살펴보세요:

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

[라라벨 프롬프트](/docs/{{version}}/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 사용할 경우, `expectsSearch` 어서션으로 사용자 입력, 검색 결과, 선택값을 모킹할 수 있습니다:

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

`doesntExpectOutput` 메서드를 사용해 콘솔 커맨드가 아무런 출력을 생성하지 않는지 검증할 수도 있습니다:

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

`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드는 출력값의 일부분에 대해 검증할 때 사용할 수 있습니다:

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

"예" 또는 "아니오"와 같은 확인을 요구하는 커맨드를 작성할 경우, `expectsConfirmation` 메서드를 사용할 수 있습니다:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 출력 기대값

Artisan의 `table` 메서드를 사용해 정보를 테이블 형식으로 출력하는 커맨드라면, 전체 테이블에 대한 기대값을 작성하는 것이 번거로울 수 있습니다. 이때는 `expectsTable` 메서드를 사용할 수 있습니다. 첫 번째 인자로는 테이블 헤더, 두 번째 인자로는 테이블 데이터를 전달합니다:

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

기본적으로, 애플리케이션에서 테스트 실행 시에는 `Illuminate\Console\Events\CommandStarting`과 `Illuminate\Console\Events\CommandFinished` 이벤트가 발생하지 않습니다. 그러나, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트(trait)를 추가하면 해당 이벤트를 사용할 수 있습니다:

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