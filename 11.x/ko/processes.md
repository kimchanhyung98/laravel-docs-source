# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 실행하기](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 이름 지정](#naming-pool-processes)
    - [풀 프로세스 ID와 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 모킹](#faking-processes)
    - [특정 프로세스 모킹](#faking-specific-processes)
    - [프로세스 시퀀스 모킹](#faking-process-sequences)
    - [비동기 프로세스 수명주기 모킹](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어설션](#available-assertions)
    - [실행되지 않은 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/7.0/components/process.html) 위에 간결하고 표현력 높은 최소한의 API를 제공하여, Laravel 애플리케이션 내에서 외부 프로세스를 편리하게 실행할 수 있게 합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="invoking-processes"></a>
## 프로세스 실행하기 (Invoking Processes)

프로세스를 실행하려면 `Process` 파사드가 제공하는 `run`과 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 완료될 때까지 기다리는 동기 실행용이며, `start` 메서드는 비동기 실행에 사용됩니다. 이 문서에서는 두 가지 방식을 모두 다룹니다. 먼저 기본적인 동기 프로세스를 실행하고 결과를 확인하는 방법부터 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에는 프로세스 결과를 검사할 수 있는 다양한 유용한 메서드가 포함되어 있습니다:

```php
$result = Process::run('ls -la');

$result->successful();
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
#### 예외 발생시키기

프로세스 결과에서 종료 코드가 0보다 크면 실패로 간주하여 `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면, `throw`와 `throwIf` 메서드를 사용하세요. 프로세스가 실패하지 않았다면 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션 (Process Options)

물론, 프로세스 실행 전에 작업 디렉토리, 타임아웃, 환경 변수 등 다양한 프로세스 동작을 조정해야 할 수도 있습니다. Laravel은 이러한 프로세스 속성을 쉽게 설정할 수 있게 합니다.

<a name="working-directory-path"></a>
#### 작업 디렉토리 경로

`path` 메서드를 사용해 프로세스의 작업 디렉토리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면, 프로세스는 현재 PHP 스크립트가 실행 중인 작업 디렉토리를 상속받습니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 통해 프로세스의 표준 입력으로 데이터를 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로, 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 하지만 `timeout` 메서드로 이 동작을 커스터마이징할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또는 타임아웃 기능을 완전히 비활성화하고 싶다면 `forever` 메서드를 호출하세요:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 출력 없이 최대 몇 초간 실행될 수 있는지 설정하는 데 사용됩니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 이용해 프로세스에 환경 변수를 전달할 수 있습니다. 호출된 프로세스는 기본적으로 운영체제가 정의한 모든 환경 변수를 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속받은 환경 변수를 해당 프로세스에서 제거하려면, 해당 변수의 값을 `false`로 지정하세요:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드는 프로세스에 TTY 모드를 활성화하는 데 사용됩니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력과 출력을 연결하여, 프로세스가 Vim 또는 Nano 같은 편집기를 실행할 수 있도록 합니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력 (Process Output)

앞서 설명한 것처럼, 프로세스 출력은 프로세스 결과의 `output`(표준 출력)과 `errorOutput`(표준 에러 출력) 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드의 두 번째 인자로 클로저를 전달하여 실시간으로 출력을 수집할 수도 있습니다. 클로저는 출력의 "유형"(stdout 또는 stderr)과 출력 문자열 두 개의 인자를 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 `seeInOutput`과 `seeInErrorOutput` 메서드도 제공하는데, 이 메서드들은 특정 문자열이 프로세스 출력에 포함되었는지 빠르게 확인할 수 있게 해줍니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 끄기

관심 없는 대량의 출력을 생성하는 프로세스는 출력 수집을 비활성화하여 메모리를 절약할 수 있습니다. 빌드 중 `quietly` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인 (Pipelines)

가끔 한 프로세스의 출력을 다른 프로세스의 입력으로 연결하고 싶을 때가 있습니다. 이는 흔히 "파이핑(piping)"이라고 합니다. `Process` 파사드의 `pipe` 메서드는 이를 간단하게 처리할 수 있게 합니다. `pipe` 메서드는 동기적으로 파이프라인의 모든 프로세스를 실행하며, 마지막 프로세스의 결과를 반환합니다:

```php
use Illuminate\Process\Pipe;
use Illuminate\Support\Facades\Process;

$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
});

if ($result->successful()) {
    // ...
}
```

파이프라인을 구성하는 개별 프로세스를 커스터마이징할 필요가 없다면, 명령어 문자열 배열을 `pipe` 메서드에 바로 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

`pipe` 메서드의 두 번째 인자로 클로저를 전달하면 실시간으로 출력을 수집할 수 있습니다. 이 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

또한, `as` 메서드를 사용해 파이프라인 내 각 프로세스에 문자열 키를 할당할 수 있습니다. 이 키는 `pipe` 메서드의 출력 클로저에도 전달되므로, 어떤 프로세스의 출력인지 구분할 수 있습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
})->start(function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 비동기 프로세스 (Asynchronous Processes)

`run` 메서드는 동기적으로 프로세스를 실행하지만, `start` 메서드를 사용하면 비동기 방식으로 프로세스를 실행할 수 있습니다. 이는 프로세스가 백그라운드에서 실행되는 동안 애플리케이션이 다른 작업을 계속할 수 있게 합니다. 프로세스를 실행한 뒤에는 `running` 메서드로 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

`wait` 메서드를 호출하면 프로세스 완료를 기다린 후 결과 인스턴스를 받을 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널 (Process IDs and Signals)

`id` 메서드를 사용하면 실행 중인 프로세스에 운영체제가 할당한 프로세스 ID를 가져올 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 사용하면 실행 중인 프로세스에 시그널(signal)을 보낼 수 있습니다. 미리 정의된 시그널 상수 목록은 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, `output`과 `errorOutput` 메서드로 현재까지의 전체 출력을 확인할 수 있습니다. 하지만 마지막으로 출력을 조회한 이후 새로 발생한 출력만 필요하다면 `latestOutput`과 `latestErrorOutput` 메서드를 사용하세요:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드와 마찬가지로, `start` 메서드도 두 번째 인자로 클로저를 받아 실시간 출력을 처리할 수 있습니다. 이 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 기다리지 않고, 출력에 따라 기다림을 멈추고 싶다면 `waitUntil` 메서드를 사용하세요. 이 메서드는 클로저가 `true`를 반환하면 기다림을 멈춥니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="concurrent-processes"></a>
## 동시 프로세스 (Concurrent Processes)

Laravel은 동시 실행되는 비동기 프로세스 풀을 손쉽게 관리할 수 있게 지원합니다. `pool` 메서드를 시작하면 `Illuminate\Process\Pool` 인스턴스를 인수로 받는 클로저를 통해 여러 프로세스를 정의할 수 있습니다.

이 클로저 내에서 풀에 속한 프로세스들을 정의합니다. `start` 메서드로 프로세스 풀을 실행한 뒤, `running` 메서드로 현재 실행 중인 프로세스들의 [컬렉션](/docs/11.x/collections)에 접근할 수 있습니다:

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

$pool = Process::pool(function (Pool $pool) {
    $pool->path(__DIR__)->command('bash import-1.sh');
    $pool->path(__DIR__)->command('bash import-2.sh');
    $pool->path(__DIR__)->command('bash import-3.sh');
})->start(function (string $type, string $output, int $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();
```

모든 풀 내 프로세스가 종료되기를 기다리고 결과를 반환받으려면 `wait` 메서드를 사용합니다. `wait` 메서드는 결과 배열 접근 객체를 반환하여 각 프로세스 결과에 키로 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

편의를 위해 `concurrently` 메서드는 비동기 프로세스 풀을 시작하고 즉시 결과를 기다립니다. PHP 배열 구조 분해와 함께 사용하면 매우 간결한 문법이 됩니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 이름 지정

숫자 키로 프로세스 풀 결과에 접근하는 것은 표현력이 떨어질 수 있으므로, `as` 메서드를 사용해 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키는 `start` 메서드 클로저에도 전달되므로, 출력이 어느 프로세스에 속하는지 구분할 수 있습니다:

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->as('first')->command('bash import-1.sh');
    $pool->as('second')->command('bash import-2.sh');
    $pool->as('third')->command('bash import-3.sh');
})->start(function (string $type, string $output, string $key) {
    // ...
});

$results = $pool->wait();

return $results['first']->output();
```

<a name="pool-process-ids-and-signals"></a>
### 풀 프로세스 ID와 시그널

`running` 메서드는 풀 내 실행 중인 모든 프로세스의 컬렉션을 반환해주므로, 각 프로세스의 OS 프로세스 ID에도 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 풀 전체에 시그널을 보내려면 `signal` 메서드를 풀 인스턴스에 호출하세요. 이는 풀 내 모든 프로세스에 시그널을 전달합니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스가 편리하고 표현력 있는 테스트 작성을 돕는 기능을 제공하며, Laravel의 프로세스 서비스도 예외가 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면 프로세스가 호출될 때 더미 또는 스텁 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 모킹 (Faking Processes)

프로세스 모킹 기능을 실험하기 위해, 한 프로세스를 호출하는 라우트를 가정해봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인자 없이 호출하면 모든 프로세스 호출에 대해 성공한(fake) 결과를 반환하도록 Laravel에 지시할 수 있습니다. 또한, 특정 프로세스가 실행되었는지 [어설션](#available-assertions)할 수도 있습니다:

```php tab=Pest
<?php

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 간단한 프로세스 실행 어설션...
    Process::assertRan('bash import.sh');

    // 또는 프로세스 설정 검사...
    Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
        return $process->command === 'bash import.sh' &&
               $process->timeout === 60;
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // 간단한 프로세스 실행 어설션...
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

`fake` 메서드를 호출하면 Laravel은 항상 출력이 없는 성공한 결과를 반환합니다. `Process` 파사드의 `result` 메서드를 사용하면 손쉽게 모킹할 프로세스의 출력과 종료 코드를 지정할 수 있습니다:

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```

<a name="faking-specific-processes"></a>
### 특정 프로세스 모킹 (Faking Specific Processes)

앞 예제에서 보았듯, `fake` 메서드에 명령어 패턴 키와 결과를 담은 배열을 전달해 프로세스별로 다른 모킹 결과를 지정할 수 있습니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 지정하지 않은 명령어는 실제로 실행됩니다. `Process::result` 메서드로 모킹 결과를 쉽게 생성할 수 있습니다:

```php
Process::fake([
    'cat *' => Process::result(
        output: 'Test "cat" output',
    ),
    'ls *' => Process::result(
        output: 'Test "ls" output',
    ),
]);
```

종료 코드나 표준 에러 출력을 따로 지정하지 않아도 되는 경우, 단순 문자열 형태로 모킹 결과를 지정해도 됩니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 모킹 (Faking Process Sequences)

동일한 명령어를 여러 번 실행하는 코드를 테스트할 때, 각 호출별로 다른 모킹 결과를 제공하고 싶을 수 있습니다. 이럴 때 `Process` 파사드의 `sequence` 메서드를 사용하세요:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 수명주기 모킹 (Faking Asynchronous Process Lifecycles)

지금까지는 주로 동기 실행인 `run` 메서드를 모킹하는 방법을 다뤘습니다. 하지만 비동기 실행을 위한 `start` 메서드를 사용하는 코드를 테스트한다면 좀 더 정교한 모킹이 필요할 수 있습니다.

예를 들어, 다음과 같은 비동기 프로세스를 다루는 라우트를 가정합시다:

```php
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    $process = Process::start('bash import.sh');

    while ($process->running()) {
        Log::info($process->latestOutput());
        Log::info($process->latestErrorOutput());
    }

    return 'Done';
});
```

이 비동기 프로세스를 모킹하려면, `running` 메서드가 몇 번 `true`를 반환할지 정의하고, 여러 차례에 걸친 순차적인 출력도 지정해야 합니다. `Process` 파사드의 `describe` 메서드를 사용하면 가능합니다:

```php
Process::fake([
    'bash import.sh' => Process::describe()
        ->output('First line of standard output')
        ->errorOutput('First line of error output')
        ->output('Second line of standard output')
        ->exitCode(0)
        ->iterations(3),
]);
```

위 예시를 자세히 살펴보면, `output`과 `errorOutput` 메서드로 순서대로 반환될 출력 항목들을 지정할 수 있으며, `exitCode` 메서드는 최종 종료 코드를, `iterations` 메서드는 `running` 메서드가 `true`를 반환할 횟수를 설정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어설션 (Available Assertions)

[앞서 다룬](#faking-processes) 것처럼, Laravel은 기능 테스트를 위한 여러 프로세스 어설션을 제공합니다. 다음은 주요 어설션들입니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 실행되었는지 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 받으며, 이 클로저는 실행된 프로세스(`Illuminate\Process\PendingProcess` 인스턴스)와 결과(`Illuminate\Contracts\Process\ProcessResult` 인스턴스)를 인자로 받습니다. 클로저가 `true`를 반환하면 어설션에 성공합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 실행되지 않았음을 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertDidntRun`도 클로저를 받아 프로세스와 결과를 검사할 수 있습니다. 클로저가 `true`를 반환하면 어설션에 실패합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정된 횟수만큼 실행되었는지 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

이 메서드도 클로저를 받으며, 클로저가 `true`를 반환하고 프로세스가 지정된 횟수 실행되었으면 어설션이 통과합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 실행되지 않은 프로세스 방지 (Preventing Stray Processes)

테스트 중 실행된 모든 프로세스를 반드시 모킹하도록 강제하려면 `preventStrayProcesses` 메서드를 호출하세요. 이후 모킹되지 않은 프로세스가 호출되면 실제 프로세스 실행 대신 예외가 발생합니다:

```
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 모킹된 응답 반환...
Process::run('ls -la');

// 예외 발생...
Process::run('bash import.sh');
```