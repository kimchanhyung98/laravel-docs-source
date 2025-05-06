# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간소화하는 것 외에도, Laravel은 애플리케이션의 [사용자 정의 콘솔 명령](/docs/{{version}}/artisan)을 테스트할 수 있는 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

우선, Artisan 명령의 종료 코드에 대한 어설션을 수행하는 방법을 알아보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용하여 Artisan 명령을 실행할 수 있습니다. 그런 다음, `assertExitCode` 메서드를 사용하여 명령이 주어진 종료 코드로 완료되었는지 확인할 수 있습니다:

    /**
     * 콘솔 명령을 테스트합니다.
     */
    public function test_console_command(): void
    {
        $this->artisan('inspire')->assertExitCode(0);
    }

명령이 주어진 종료 코드로 종료되지 않았는지 확인하려면 `assertNotExitCode` 메서드를 사용할 수 있습니다:

    $this->artisan('inspire')->assertNotExitCode(1);

일반적으로 모든 터미널 명령은 성공 시 `0`의 상태 코드로, 실패 시 0이 아닌 종료 코드로 종료됩니다. 따라서, 편의상 `assertSuccessful`과 `assertFailed` 어설션을 사용하여 명령이 성공적으로 종료되었는지 또는 실패했는지 확인할 수 있습니다:

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel에서는 `expectsQuestion` 메서드를 사용하여 콘솔 명령의 사용자 입력을 손쉽게 "모의(mock)"할 수 있습니다. 또한, `assertExitCode` 및 `expectsOutput` 메서드를 사용하여 콘솔 명령에서 출력될 것으로 기대되는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령을 생각해볼 수 있습니다:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

아래 테스트 예시에서는 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, `assertExitCode` 메서드를 활용하여 이 명령을 테스트할 수 있습니다:

    /**
     * 콘솔 명령을 테스트합니다.
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

<a name="confirmation-expectations"></a>
#### 확인(Confirmation) 기대값

"예" 또는 "아니오" 형식의 확인을 요구하는 명령을 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### 테이블 기대값

Artisan의 `table` 메서드를 사용하여 정보를 테이블 형식으로 출력하는 명령의 경우, 테이블 전체에 대한 출력 기대값을 작성하는 것은 번거로울 수 있습니다. 대신, `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더, 두 번째 인자로 테이블의 데이터를 받습니다:

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

기본적으로 애플리케이션의 테스트를 실행할 때 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 발생되지 않습니다. 하지만, 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하면 이러한 이벤트를 활성화할 수 있습니다:

    <?php
    
    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\WithConsoleEvents;
    use Tests\TestCase;
    
    class ConsoleEventTest extends TestCase
    {
        use WithConsoleEvents;
    
        // ...
    }
