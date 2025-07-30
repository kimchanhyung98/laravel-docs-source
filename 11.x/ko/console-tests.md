# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대치](#success-failure-expectations)
- [입력 / 출력 기대치](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간편하게 해주는 것 외에도, Laravel은 애플리케이션의 [커스텀 콘솔 명령어](/docs/11.x/artisan)를 테스트할 수 있는 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대치

먼저, Artisan 명령어의 종료 코드에 대한 단언(assertion)을 어떻게 하는지 살펴보겠습니다. 이를 위해 테스트 내에서 `artisan` 메서드를 사용해 Artisan 명령어를 호출합니다. 그리고 `assertExitCode` 메서드로 명령어가 지정한 종료 코드로 종료했는지 단언합니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 명령어 테스트.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

`assertNotExitCode` 메서드를 사용해 특정 종료 코드로 종료하지 않았음을 단언할 수도 있습니다:

```
$this->artisan('inspire')->assertNotExitCode(1);
```

일반적으로 모든 터미널 명령은 성공 시 종료 코드 `0`을 반환하고, 실패 시는 0이 아닌 값을 반환합니다. 따라서 편의상 `assertSuccessful`과 `assertFailed` 단언을 사용하여 명령어가 성공적으로 종료했는지 여부를 확인할 수 있습니다:

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대치

Laravel은 콘솔 명령어에서 사용자의 입력을 쉽게 "모의(Mock)" 할 수 있게 `expectsQuestion` 메서드를 제공합니다. 또한, `assertExitCode`와 `expectsOutput` 메서드를 통해 명령어가 출력할 것으로 예상되는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령어가 있다고 가정해보겠습니다:

```
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

다음과 같은 테스트로 이 명령어를 검사할 수 있습니다:

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
 * 콘솔 명령어 테스트.
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

[Laravel Prompts](/docs/11.x/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 사용하는 경우, `expectsSearch` 단언을 활용해 사용자의 입력, 검색 결과, 선택값을 모의할 수 있습니다:

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
 * 콘솔 명령어 테스트.
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

`doesntExpectOutput` 메서드를 사용하면 콘솔 명령어가 어떤 출력도 생성하지 않는지 단언할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 명령어 테스트.
 */
public function test_console_command(): void
{
    $this->artisan('example')
            ->doesntExpectOutput()
            ->assertExitCode(0);
}
```

`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드는 출력의 일부에 대해 단언할 때 유용합니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * 콘솔 명령어 테스트.
 */
public function test_console_command(): void
{
    $this->artisan('example')
            ->expectsOutputToContain('Taylor')
            ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
#### 확인 대기 기대치

"예/아니오" 형태의 확인 응답을 기대하는 명령어를 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 표 기대치

명령어가 Artisan의 `table` 메서드를 사용해 표 형태로 정보를 표시할 때, 전체 표 출력에 대한 기대치를 작성하는 것은 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용하세요. 이 메서드는 표의 헤더를 첫 번째 인수로, 데이터는 두 번째 인수로 받습니다:

```
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

기본적으로, `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 애플리케이션 테스트 실행 중에는 발생하지 않습니다. 하지만, 특정 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하면 해당 클래스에서 이 이벤트들을 활성화할 수 있습니다:

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