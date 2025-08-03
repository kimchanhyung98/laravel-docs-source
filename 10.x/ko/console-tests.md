# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대치](#success-failure-expectations)
- [입력 / 출력 기대치](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

Laravel은 HTTP 테스트를 간소화하는 것 외에도, 애플리케이션의 [커스텀 콘솔 명령어](/docs/10.x/artisan)를 테스트하기 위한 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대치

시작하기 위해, Artisan 명령어의 종료 코드에 대한 검증(assertion)을 수행하는 방법을 살펴보겠습니다. 이를 위해 테스트 내에서 `artisan` 메서드를 사용해 Artisan 명령어를 호출합니다. 이후, `assertExitCode` 메서드를 사용하여 명령어가 특정 종료 코드로 완료되었음을 검증합니다:

```
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

또한, 명령어가 특정 종료 코드로 종료되지 않았음을 검증하기 위해 `assertNotExitCode` 메서드를 사용할 수 있습니다:

```
$this->artisan('inspire')->assertNotExitCode(1);
```

물론, 일반적으로 터미널 명령어는 성공할 경우 종료 상태 코드가 `0`이고, 성공하지 못했을 경우 0이 아닌 종료 코드를 반환합니다. 따라서 편의를 위해, 특정 명령어가 성공 종료 코드를 반환했는지 또는 실패 종료 코드를 반환했는지를 검증하기 위해 `assertSuccessful`과 `assertFailed` 메서드를 사용할 수 있습니다:

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대치

Laravel은 `expectsQuestion` 메서드를 통해 콘솔 명령어에 대한 사용자 입력을 쉽게 "모킹(mock)"할 수 있도록 지원합니다. 추가로, 콘솔 명령어가 출력할 것으로 예상하는 종료 코드 및 텍스트를 `assertExitCode`와 `expectsOutput` 메서드를 통해 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령어가 있다고 할 때:

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

아래와 같이 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, 그리고 `assertExitCode` 메서드를 사용하여 이 명령어에 대한 테스트를 작성할 수 있습니다:

```
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
         ->expectsOutputToContain('Taylor Otwell')
         ->doesntExpectOutputToContain('you prefer Ruby')
         ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
#### 확인 응답 기대치

"예" 또는 "아니오" 형태의 확인 응답을 기대하는 명령어를 작성할 때는, `expectsConfirmation` 메서드를 활용할 수 있습니다:

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 기대치

명령어가 Artisan의 `table` 메서드를 이용해 정보를 표 형식으로 출력할 경우, 전체 테이블에 대해 출력 기대치를 작성하는 것이 번거로울 수 있습니다. 대신 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더를, 두 번째 인자로 테이블의 데이터를 받습니다:

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

기본적으로, 애플리케이션 테스트 실행 시 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 발생하지 않습니다. 그러나 특정 테스트 클래스에서 이 이벤트들을 활성화하고 싶다면, 해당 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트(trait)를 추가하면 됩니다:

```
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