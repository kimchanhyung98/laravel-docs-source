# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출하기](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID 및 신호](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 이름 지정하기](#naming-pool-processes)
    - [풀 프로세스 ID 및 신호](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 가짜 처리하기](#faking-processes)
    - [특정 프로세스 가짜 처리하기](#faking-specific-processes)
    - [프로세스 시퀀스 가짜 처리하기](#faking-process-sequences)
    - [비동기 프로세스 생명주기 가짜 처리하기](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [떠돌이 프로세스 방지하기](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/7.0/components/process.html)를 기반으로 직관적이고 간결한 API를 제공합니다. 이를 통해 Laravel 애플리케이션에서 외부 프로세스를 편리하게 호출할 수 있습니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 중점을 두고 있습니다.

<a name="invoking-processes"></a>
## 프로세스 호출하기

프로세스를 호출하려면 `Process` 파사드가 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출하고 종료할 때까지 기다리며, `start` 메서드는 비동기 프로세스 실행에 활용됩니다. 여기서는 두 가지 방식을 모두 살펴보겠습니다. 먼저 기본적인 동기 프로세스를 호출하고 결과를 확인하는 방법부터 보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 확인하는 데 유용한 여러 메서드를 제공합니다:

```php
$result = Process::run('ls -la');

$result->successful();
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
#### 예외 던지기

프로세스 결과에서 종료 코드가 0보다 크면 실패를 의미하므로, `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶을 경우 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 실패하지 않았으면 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

물론, 프로세스를 호출하기 전에 동작을 맞춤 설정해야 할 수도 있습니다. Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 여러 프로세스 기능을 조정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용해 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속받습니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 통해 프로세스 표준 입력(stdin)으로 값을 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. `timeout` 메서드로 이 동작을 설정할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또는 프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 호출하세요:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 출력 없이 최대 대기할 수 있는 시간을 초 단위로 지정합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 통해 프로세스에 환경 변수를 전달할 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경 변수를 제거하려면 해당 변수에 `false` 값을 지정하세요:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 호출하면 프로세스에 TTY 모드를 활성화합니다. TTY 모드는 프로세스의 입력과 출력을 현재 프로그램의 입력과 출력에 연결하여, Vim이나 Nano 같은 편집기를 프로세스로 실행할 수 있게 합니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞서 설명했듯, 프로세스 결과에서 `output` (표준 출력)과 `errorOutput` (표준 에러)을 통해 출력 내용을 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

양방향 실시간 출력도 가능합니다. `run` 메서드의 두 번째 인수로 클로저를 전달하면, 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

`seeInOutput` 및 `seeInErrorOutput` 메서드는 지정한 문자열이 출력에 포함되었는지 간편하게 확인할 수 있습니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

관심 없는 대량의 출력이 있을 경우 메모리 절약을 위해 출력을 완전히 비활성화할 수 있습니다. `quietly` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

한 프로세스의 출력을 다른 프로세스의 입력으로 연결하는 경우가 있습니다. 이를 "파이핑(piping)"이라고 하며, `Process` 파사드의 `pipe` 메서드로 간편하게 구현할 수 있습니다. `pipe` 메서드는 파이프라인 프로세스들을 동기적으로 실행하고 마지막 프로세스의 결과를 반환합니다:

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

파이프라인에 포함된 개별 프로세스 설정이 필요 없다면, 명령어 문자열 배열을 `pipe` 메서드에 바로 전달해도 됩니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

출력을 실시간으로 수집하려면 `pipe`의 두 번째 인수로 클로저를 전달하세요. 클로저는 출력 종류와 출력 문자열을 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

각 프로세스에 문자열 키를 할당하려면 `as` 메서드를 사용하세요. 이 키는 출력 클로저에도 전달되어 어떤 프로세스 출력인지 구분할 수 있습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
})->start(function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 비동기 프로세스

`run` 메서드는 동기적으로 프로세스를 실행하지만, `start` 메서드를 사용하면 비동기 실행이 가능합니다. 이로써 애플리케이션은 백그라운드에서 실행되는 프로세스와 동시에 다른 작업을 수행할 수 있습니다. 프로세스가 호출된 후 `running` 메서드로 실행 중 여부를 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

`wait` 메서드를 호출하면 프로세스가 종료될 때까지 기다렸다가 결과 인스턴스를 얻을 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 신호

`id` 메서드로 운영체제가 할당한 실행 중 프로세스 ID를 가져올 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드로 실행 중인 프로세스에 신호(signal)를 보낼 수 있습니다. 미리 정의된 신호 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행되는 동안 `output` 및 `errorOutput` 메서드로 현재까지의 전체 출력을 확인할 수 있습니다. 또한, `latestOutput` 및 `latestErrorOutput` 메서드로 마지막 조회 이후 새로 발생한 출력을 읽을 수도 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

동기 메서드와 마찬가지로, `start` 메서드 두 번째 인수에 클로저를 전달하면 실시간 출력 수집도 가능합니다. 이 클로저는 출력 유형과 출력 문자열 인자를 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 기다리지 않고 `waitUntil` 메서드를 사용해 출력에 따라 기다림을 중단할 수도 있습니다. 전달된 클로저가 `true`를 반환하면 기다림이 끝납니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스 실행 중 `ensureNotTimedOut` 메서드로 타임아웃이 발생하지 않았는지 확인할 수 있습니다. 타임아웃이 발생했으면 [타임아웃 예외](#timeouts)를 던집니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## 동시 프로세스

Laravel은 여러 비동기 프로세스를 동시에 실행하는 풀(pool) 관리도 간단하게 제공합니다. `pool` 메서드를 호출하면 `Illuminate\Process\Pool` 인스턴스를 인자로 받는 클로저를 전달하여 프로세스 집합을 정의할 수 있습니다.

클로저 내에서 각 프로세스를 풀에 등록하고, `start`로 풀 실행을 시작하면 `running` 메서드로 실행 중인 프로세스 컬렉션을 얻을 수 있습니다:

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

`wait` 메서드는 모든 풀 프로세스가 종료될 때까지 기다렸다가 각각의 결과를 키로 액세스할 수 있는 배열 형태로 반환합니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

편리하게 `concurrently` 메서드를 사용하면 풀을 실행하고 결과를 바로 기다릴 수도 있습니다. PHP 배열 구조 분해와 함께 쓰면 특히 표현력이 좋습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 이름 지정하기

숫자 키로 프로세스 결과에 접근하는 것보다 명확한 이름을 할당하는 것이 좋습니다. `as` 메서드로 각 프로세스에 문자열 키를 지정할 수 있으며, 이 키는 `start` 메서드에 넘기는 클로저에도 전달되어 출력 출처를 구분할 수 있습니다:

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
### 풀 프로세스 ID 및 신호

`running` 메서드가 실행 중인 프로세스의 컬렉션을 제공하므로, 각 풀 프로세스 ID를 쉽게 얻을 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 풀 전체에 신호를 보내려면 풀 인스턴스에서 `signal` 메서드를 호출하세요:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스가 테스트 작성을 쉽게 지원하는 기능을 제공하듯, 프로세스 기능도 예외가 아닙니다. `Process` 파사드의 `fake` 메서드로 프로세스 호출 시 가짜 결과를 반환하도록 설정할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 가짜 처리하기

프로세스 가짜 처리 기능을 소개하기 위해, 프로세스를 호출하는 라우트를 가정해봅니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출하면 모든 호출된 프로세스에 대해 성공적인 가짜 결과를 반환하도록 Laravel을 설정할 수 있습니다. 또한, 특정 프로세스가 호출되었는지 [어서션](#available-assertions)도 수행할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 간단한 프로세스 호출 어서션
    Process::assertRan('bash import.sh');

    // 또는 프로세스 설정 검사
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

        // 간단한 프로세스 호출 어서션
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정 검사
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

`fake` 메서드를 호출하면 항상 성공적인 프로세스 결과를 반환하지만, `Process` 파사드의 `result` 메서드를 사용하면 출력 내용과 종료 코드를 지정해 가짜 결과를 쉽게 만들 수 있습니다:

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
### 특정 프로세스 가짜 처리하기

앞서 예시에서 보았듯, `fake` 메서드에 배열을 넘겨 프로세스별로 가짜 결과를 다르게 지정할 수 있습니다.

키는 가짜 처리할 명령어 패턴이며, `*`는 와일드카드로 사용됩니다. 가짜 처리하지 않은 프로세스는 실제로 호출됩니다. `Process` 파사드의 `result` 메서드로 스텁 결과를 생성할 수 있습니다:

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

종료 코드나 에러 출력을 지정하지 않아도 될 경우, 간단히 문자열로 가짜 결과를 지정할 수도 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 가짜 처리하기

동일한 명령이 여러 차례 호출되는 코드를 테스트할 때는, 각 호출마다 다른 가짜 결과를 지정할 수 있습니다. `Process` 파사드의 `sequence` 메서드로 이를 구현할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 가짜 처리하기

지금까지는 동기 프로세스(`run` 메서드)를 가짜 처리하는 방법을 설명했지만, 비동기 프로세스(`start` 메서드)를 테스트하려면 더 정교한 가짜 설정이 필요할 수 있습니다.

예를 들어, 다음과 같은 라우트가 있다고 가정합니다:

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

이 프로세스를 제대로 가짜 처리하려면 `running` 메서드가 `true`를 몇 번 반환할지 설정하고, 출력 내용도 순차적으로 여러 줄 지정할 수 있어야 합니다. `Process` 파사드의 `describe` 메서드가 이를 지원합니다:

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

예시를 살펴보면, `output`, `errorOutput` 메서드로 순서대로 반환할 출력 줄을 지정할 수 있고, `exitCode`는 종료 코드를 설정하며, `iterations`는 `running`이 `true`를 반환할 횟수를 의미합니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션

[앞서 설명한](#faking-processes) 대로, Laravel은 기능 테스트에 사용할 다양한 프로세스 어서션을 제공합니다. 각 어서션별 사용법을 소개합니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 호출되었는지 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

클로저를 사용해 호출된 프로세스 옵션을 검사할 수도 있습니다. 클로저는 프로세스와 프로세스 결과 인스턴스를 받습니다. 클로저가 `true`를 반환하면 어서션이 성공합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

어서션 클로저의 `$process`는 `Illuminate\Process\PendingProcess`, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 호출되지 않았음을 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

클로저를 전달할 수도 있으며, 클로저가 `true`를 반환하면 어서션이 실패합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정된 횟수만큼 호출되었는지 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

클로저를 사용하면 프로세스 옵션 조건과 호출 횟수를 동시에 검사할 수 있습니다. 클로저가 `true`이고 호출 횟수가 일치하면 어서션이 성공합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 떠돌이 프로세스 방지하기

모든 호출된 프로세스가 가짜 처리되었는지 보장하고 싶을 경우, `preventStrayProcesses` 메서드를 호출하세요. 이 메서드 이후 실제 가짜 결과가 없는 프로세스 실행은 실제 프로세스 시작 대신 예외를 던집니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 가짜 결과를 반환함
Process::run('ls -la');

// 예외가 던져짐
Process::run('bash import.sh');
```