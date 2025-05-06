# 콘솔 테스트

- [소개](#introduction)
- [성공/실패 예상](#success-failure-expectations)
- [입력/출력 예상](#input-output-expectations)

<a name="introduction"></a>
## 소개

HTTP 테스트를 단순화하는 것 외에도, Laravel은 애플리케이션의 [사용자 지정 콘솔 커맨드](/docs/{{version}}/artisan)를 테스트할 수 있는 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공/실패 예상

먼저, Artisan 커맨드의 종료 코드에 대해 어떻게 단언을 할 수 있는지 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용하여 Artisan 커맨드를 호출하고, `assertExitCode` 메서드를 사용해 해당 커맨드가 지정한 종료 코드로 완료되었는지 확인할 수 있습니다:

    /**
     * 콘솔 커맨드 테스트.
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('inspire')->assertExitCode(0);
    }

`assertNotExitCode` 메서드를 사용하여 커맨드가 특정 종료 코드로 종료되지 않았음을 단언할 수도 있습니다:

    $this->artisan('inspire')->assertNotExitCode(1);

일반적으로 모든 터미널 커맨드는 성공적으로 실행되면 `0` 상태 코드로, 실패하면 0이 아닌 종료 코드로 종료됩니다. 따라서 편의상 `assertSuccessful`과 `assertFailed` 단언문을 사용하여 커맨드가 성공적으로, 또는 실패로 종료되었는지 확인할 수 있습니다:

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="input-output-expectations"></a>
## 입력/출력 예상

Laravel은 `expectsQuestion` 메서드를 이용해 콘솔 커맨드에서 사용자 입력을 손쉽게 "모킹"할 수 있습니다. 또한, `assertExitCode`와 `expectsOutput` 메서드를 사용해 콘솔 커맨드가 출력할 것으로 예상되는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 커맨드를 살펴보세요:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

이 커맨드는 아래와 같이 테스트할 수 있으며, 이때 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, `assertExitCode` 메서드를 활용합니다:

    /**
     * 콘솔 커맨드 테스트.
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
             ->expectsOutputToContain('Taylor Otwell')
             ->doesntExpectOutputToContain('you prefer Ruby')
             ->assertExitCode(0);
    }

<a name="confirmation-expectations"></a>
#### 확인(Confirmation) 예상

"예" 또는 "아니오"로 답해야 하는 확인을 요구하는 커맨드를 작성할 때에는, `expectsConfirmation` 메서드를 사용할 수 있습니다:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### 테이블 예상

커맨드가 Artisan의 `table` 메서드를 이용해 정보를 테이블 형태로 출력하는 경우, 전체 테이블에 대해 출력 예상값을 작성하는 것은 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블 헤더를, 두 번째 인자로 테이블 데이터를 받습니다:

    $this->artisan('users:all')
        ->expectsTable([
            'ID',
            'Email',
        ], [
            [1, 'taylor@example.com'],
            [2, 'abigail@example.com'],
        ]);
