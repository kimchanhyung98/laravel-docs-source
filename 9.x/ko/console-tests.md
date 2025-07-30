# 콘솔 테스트 (Console Tests)

- [소개](#introduction)
- [성공 / 실패 기대값](#success-failure-expectations)
- [입력 / 출력 기대값](#input-output-expectations)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 HTTP 테스트를 단순화하는 것 외에도, 애플리케이션의 [커스텀 콘솔 명령어](/docs/9.x/artisan)를 테스트하기 위한 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대값 (Success / Failure Expectations)

먼저, Artisan 명령어의 종료 코드를 기반으로 단언하는 방법을 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용해 Artisan 명령어를 실행합니다. 그런 다음 `assertExitCode` 메서드를 사용해 명령어가 특정 종료 코드로 완료되었는지 단언합니다:

```
/**
 * 콘솔 명령어 테스트.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

명령어가 특정 종료 코드로 종료되지 않았음을 단언하고 싶다면 `assertNotExitCode` 메서드를 사용할 수 있습니다:

```
$this->artisan('inspire')->assertNotExitCode(1);
```

대부분의 터미널 명령어는 성공 시 종료 코드 `0`을 반환하고, 실패하면 0이 아닌 값을 반환합니다. 따라서 편의를 위해 `assertSuccessful`과 `assertFailed` 단언을 사용해 명령어가 성공 종료했는지 또는 실패 종료했는지 손쉽게 단언할 수 있습니다:

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대값 (Input / Output Expectations)

Laravel은 콘솔 명령어의 사용자 입력을 간편하게 "모의(Mock)"할 수 있도록 `expectsQuestion` 메서드를 제공합니다. 또한 `assertExitCode`, `expectsOutput` 메서드를 통해 콘솔 명령어가 출력할 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음 콘솔 명령어를 고려해봅시다:

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

아래 테스트는 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, `assertExitCode` 메서드를 사용해 이 명령어를 테스트합니다:

```
/**
 * 콘솔 명령어 테스트.
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
```

<a name="confirmation-expectations"></a>
#### 확인 입력 기대값 (Confirmation Expectations)

"예" 또는 "아니오" 형태의 확인 입력을 요구하는 명령어 작성 시 `expectsConfirmation` 메서드를 활용할 수 있습니다:

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### 테이블 출력 기대값 (Table Expectations)

명령어가 Artisan의 `table` 메서드를 사용해 정보를 테이블 형식으로 출력한다면, 전체 테이블 출력 결과를 일일이 단언하는 것이 번거로울 수 있습니다. 이때 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블 헤더 배열을, 두 번째 인자로 테이블 데이터 배열을 받습니다:

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