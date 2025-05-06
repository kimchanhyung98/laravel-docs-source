# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)

<a name="introduction"></a>
## 소개

HTTP 테스트를 간소화하는 것 외에도, Laravel은 애플리케이션의 [커스텀 콘솔 명령](/docs/{{version}}/artisan)을 테스트할 수 있는 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값

먼저, Artisan 명령의 종료 코드에 대한 어서션을 수행하는 방법을 살펴보겠습니다. 이를 위해 `artisan` 메서드를 사용하여 테스트 내에서 Artisan 명령을 실행할 수 있습니다. 이후 `assertExitCode` 메서드를 사용하여 해당 명령이 지정한 종료 코드로 완료되었는지 검증할 수 있습니다:

    /**
     * 콘솔 명령 테스트.
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('inspire')->assertExitCode(0);
    }

`assertNotExitCode` 메서드를 사용하여 명령이 특정 종료 코드로 종료되지 않았는지 검증할 수도 있습니다:

    $this->artisan('inspire')->assertNotExitCode(1);

일반적으로 터미널 명령이 성공적으로 실행되면 상태 코드 `0`으로 종료되고, 실패하면 0이 아닌 코드로 종료됩니다. 따라서 편의상, 명령이 성공적으로 종료되었는지 또는 실패했는지 검증할 때 `assertSuccessful` 및 `assertFailed` 어서션을 활용할 수 있습니다:

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값

Laravel은 `expectsQuestion` 메서드를 사용하여 콘솔 명령에 대한 사용자 입력을 쉽게 "모킹(mock)"할 수 있도록 지원합니다. 또한, `assertExitCode`와 `expectsOutput` 메서드로 콘솔 명령에서 출력될 것으로 예상되는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령을 가정해보겠습니다:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

이 명령을 테스트할 때 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `assertExitCode` 메서드를 아래와 같이 사용할 수 있습니다:

    /**
     * 콘솔 명령 테스트.
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('question')
             ->expectsQuestion('What is your name?', 'Taylor Otwell')
             ->expectsQuestion('Which language do you prefer?', 'PHP')
             ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
             ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
             ->assertExitCode(0);
    }

<a name="confirmation-expectations"></a>
#### 확인(Confirmation) 기대값

예/아니오 형태의 확인 응답을 기대하는 명령을 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### 테이블 기대값

명령에서 Artisan의 `table` 메서드를 사용하여 정보 테이블을 표시하는 경우, 전체 테이블의 출력에 대한 기대값을 작성하는 것이 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더, 두 번째 인자로 테이블 데이터를 받습니다:

    $this->artisan('users:all')
        ->expectsTable([
            'ID',
            'Email',
        ], [
            [1, 'taylor@example.com'],
            [2, 'abigail@example.com'],
        ]);
