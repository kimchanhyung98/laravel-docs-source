# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대치](#success-failure-expectations)
- [입력 / 출력 기대치](#input-output-expectations)

<a name="introduction"></a>
## 소개

Laravel은 HTTP 테스트를 간소화하는 것 외에도, 애플리케이션의 [커스텀 콘솔 명령어](/docs/{{version}}/artisan)를 테스트하기 위한 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대치

먼저, Artisan 명령어의 종료 코드에 관한 단언(assertion)을 하는 방법을 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용하여 Artisan 명령어를 호출합니다. 이어서 `assertExitCode` 메서드를 사용해 명령어가 특정 종료 코드로 완료되었음을 단언합니다:

```
/**
 * 콘솔 명령어를 테스트합니다.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

명령어가 특정 종료 코드로 종료되지 않았음을 확인하려면 `assertNotExitCode` 메서드를 사용할 수 있습니다:

```
$this->artisan('inspire')->assertNotExitCode(1);
```

물론 모든 터미널 명령어는 일반적으로 성공했을 때 `0` 종료 코드를 반환하고, 실패했을 때는 0이 아닌 값을 반환합니다. 따라서 편의를 위해 `assertSuccessful`과 `assertFailed` 단언 메서드를 사용할 수 있으며, 이를 통해 명령어가 성공적인 종료 코드로 종료되었는지 여부를 검증할 수 있습니다:

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대치

Laravel은 콘솔 명령어에 대한 사용자 입력을 `expectsQuestion` 메서드를 통해 쉽게 "모킹"할 수 있도록 지원합니다. 게다가, `assertExitCode`와 `expectsOutput` 메서드를 사용해 콘솔 명령어가 출력할 것으로 예상하는 종료 코드와 텍스트를 명시할 수 있습니다. 다음 콘솔 명령어를 예로 들어 보겠습니다:

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

다음 테스트 코드는 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `assertExitCode` 메서드를 이용하여 위 명령어를 테스트하는 예시입니다:

```
/**
 * 콘솔 명령어를 테스트합니다.
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
```

<a name="confirmation-expectations"></a>
#### 확인 입력 기대치

사용자가 "예" 또는 "아니오"로 확인을 입력하는 명령어를 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 기대치

만약 명령어가 Artisan의 `table` 메서드를 사용해 정보를 테이블 형식으로 출력한다면, 전체 테이블에 대한 출력 기대치를 작성하는 것이 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용할 수 있으며, 이 메서드는 첫 번째 인수로 테이블 헤더를, 두 번째 인수로 테이블 데이터를 받습니다:

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