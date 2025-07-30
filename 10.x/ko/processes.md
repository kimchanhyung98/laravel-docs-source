# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출하기](#invoking-processes)
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
    - [프로세스 가짜 처리](#faking-processes)
    - [특정 프로세스 가짜 처리](#faking-specific-processes)
    - [프로세스 시퀀스 가짜 처리](#faking-process-sequences)
    - [비동기 프로세스 수명주기 가짜 처리](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 단언문](#available-assertions)
    - [예기치 않은 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 기반으로, 표현력이 뛰어나고 최소한의 API를 제공합니다. 이를 통해 Laravel 애플리케이션 내에서 외부 프로세스를 편리하게 호출할 수 있습니다. Laravel의 프로세스 기능은 가장 흔히 사용되는 경우에 집중하여 뛰어난 개발자 경험을 제공합니다.

<a name="invoking-processes"></a>
## 프로세스 호출하기

프로세스를 호출하려면 `Process` 파사드의 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출한 뒤 실행이 종료될 때까지 기다리며, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 가지 방식을 모두 살펴보겠습니다. 먼저 기본 동기 프로세스 호출과 결과 확인 방법부터 보겠습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

`run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 확인하는 데 유용한 여러 메서드를 제공합니다:

```php
$result = Process::run('ls -la');

$result->successful();
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
#### 예외 발생하기

프로세스 결과를 받고 종료 코드가 0보다 큰 경우(즉, 실패를 나타내는 경우) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶다면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

프로세스 호출 전에 동작 방식을 조정해야 할 수도 있습니다. 다행히 Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 여러 프로세스 기능을 쉽게 설정할 수 있게 합니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용해 프로세스의 작업 디렉터리를 지정할 수 있습니다. 지정하지 않은 경우 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 사용하면 프로세스의 표준 입력을 통해 데이터를 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. 그러나 `timeout` 메서드를 통해 이 값을 조정할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또는 `forever` 메서드를 호출해 타임아웃을 완전히 비활성화할 수 있습니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 출력 없이 최대 몇 초 동안 실행될 수 있는지 지정합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 사용해 프로세스에 환경 변수를 전달할 수 있습니다. 단, 호출된 프로세스는 시스템에 정의된 환경 변수들을 그대로 상속받습니다:

```php
$result = Process::forever()
            ->env(['IMPORT_PATH' => __DIR__])
            ->run('bash import.sh');
```

상속된 환경 변수를 제거하려면 해당 변수에 `false` 값을 지정하면 됩니다:

```php
$result = Process::forever()
            ->env(['LOAD_PATH' => false])
            ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드로 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력과 출력에 연결하여 Vim 또는 Nano처럼 편집기를 프로세스 형태로 열 수 있게 합니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞서 설명했듯이, 프로세스 출력은 프로세스 결과의 `output`(표준 출력) 및 `errorOutput`(표준 에러 출력) 메서드를 통해 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드에 두 번째 인수로 클로저를 전달하면 출력이 실시간으로 수집됩니다. 이 클로저는 두 개의 인수—출력 유형(`stdout` 또는 `stderr`)과 출력 문자열—를 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 `seeInOutput` 및 `seeInErrorOutput` 메서드도 제공하여 특정 문자열이 프로세스 출력에 포함되었는지 쉽게 확인할 수 있습니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 매우 많은 출력을 생성하지만 출력이 필요 없다면, 메모리 소비를 줄이기 위해 출력 수집을 완전히 비활성화할 수 있습니다. 이를 위해 프로세스 설정 중 `quietly` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

가끔 하나의 프로세스 출력을 다른 프로세스 입력으로 연결하고 싶을 때가 있습니다. 이를 "파이핑"이라고 하며, `Process` 파사드의 `pipe` 메서드로 손쉽게 할 수 있습니다. `pipe`는 동기적으로 파이프라인 프로세스들을 실행하고 마지막 프로세스 결과를 반환합니다:

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

파이프라인을 구성하는 개별 프로세스를 커스텀할 필요가 없다면, 단순히 명령어 문자열 배열을 `pipe`에 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

`pipe`에도 `run`과 마찬가지로 두 번째 인수로 클로저를 전달하여 실시간 출력을 받을 수 있습니다. 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

또한, `as` 메서드를 사용해 파이프라인 내 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키는 `pipe` 메서드에 제공한 출력 클로저에도 전달되어, 출력이 어느 프로세스에서 발생했는지 알 수 있습니다:

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

`run` 메서드는 동기적으로 프로세스를 실행하지만, `start` 메서드는 비동기적으로 프로세스를 실행할 수 있습니다. 비동기 실행 시 애플리케이션이 프로세스 실행 중에도 다른 작업을 수행할 수 있습니다. 프로세스가 시작된 후, `running` 메서드로 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

또한 `wait` 메서드를 호출하여 프로세스가 종료될 때까지 기다리고 프로세스 결과를 얻을 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드로 운영체제가 할당한 실행 중인 프로세스 ID를 조회할 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드는 실행 중인 프로세스에 시그널을 보낼 때 사용합니다. 미리 정의된 시그널 상수 목록은 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, `output` 및 `errorOutput` 메서드로 현재까지 전체 출력을 확인할 수 있습니다. 하지만 `latestOutput`과 `latestErrorOutput` 메서드는 마지막으로 출력이 조회된 이후 발생한 최신 출력만 가져옵니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드와 마찬가지로, `start` 메서드에 두 번째 인수로 클로저를 전달하면 비동기 프로세스의 출력을 실시간으로 수집할 수 있습니다. 이 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

<a name="concurrent-processes"></a>
## 동시 프로세스

Laravel은 또한 동시성을 지원하는 비동기 프로세스 풀을 손쉽게 관리할 수 있게 합니다. 이를 통해 여러 작업을 동시에 실행할 수 있습니다. `pool` 메서드를 호출하면 `Illuminate\Process\Pool` 인스턴스가 전달되는 클로저를 받으며, 이 내부에서 프로세스 풀에 포함할 프로세스를 정의합니다. `start` 메서드로 프로세스 풀을 시작한 후, `running` 메서드를 통해 현재 실행 중인 프로세스 컬렉션을 조회할 수 있습니다:

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

`wait` 메서드를 호출하면 풀 내 모든 프로세스가 종료될 때까지 기다리고 각 프로세스 결과에 키를 통해 접근할 수 있는 배열 형태의 객체를 반환합니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

또한 `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 실행하고 즉시 모든 결과가 반환될 때까지 대기할 수 있습니다. 이 기능은 PHP 배열 디스트럭처링과 결합할 때 특히 표현력이 뛰어납니다:

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

숫자 키로 프로세스 풀 결과에 접근하는 것은 표현력이 떨어질 수 있으므로, Laravel은 `as` 메서드로 각 풀 프로세스에 문자열 키를 지정할 수 있게 합니다. 지정한 키는 출력 클로저에 함께 전달되어 어느 프로세스가 출력을 발생시켰는지 알 수 있습니다:

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

프로세스 풀의 `running` 메서드를 통해 실행 중인 모든 프로세스 컬렉션에 접근 가능하므로, 각 프로세스 ID에 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 편리하게 `signal` 메서드를 호출해 풀 내 모든 프로세스에 한 번에 시그널을 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

Laravel 서비스들은 테스트 작성이 쉽고 표현력 있게 할 수 있도록 도와주는 기능들을 제공합니다. Laravel의 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면, 프로세스가 호출될 때마다 가짜 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 가짜 처리

프로세스 가짜 처리를 이해하기 위해, 프로세스를 호출하는 라우트를 생각해봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출해 모든 호출된 프로세스가 성공한 가짜 결과를 반환하도록 할 수 있습니다. 이와 더불어, 특정 프로세스가 실행됐는지 [단언문](#available-assertions)으로 확인할 수도 있습니다:

```php
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

        // 간단한 프로세스 실행 단언...
        Process::assertRan('bash import.sh');

        // 또는 프로세스 구성 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

`Process` 파사드의 `fake` 메서드를 호출하면 Laravel은 항상 출력 없는 성공한 프로세스 결과를 반환합니다. 하지만 `result` 메서드를 사용하면 가짜 프로세스의 출력과 종료 코드를 쉽게 지정할 수 있습니다:

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
### 특정 프로세스 가짜 처리

앞 예시에서 보았듯, `fake` 메서드는 호출할 프로세스마다 다른 가짜 결과를 지정할 수 있도록 배열을 인수로 받을 수 있습니다.

배열의 키는 가짜 처리하고자 하는 명령어 패턴이며 값은 그에 대응하는 결과입니다. `*` 문자는 와일드카드로 사용 가능합니다. 가짜 처리하지 않은 프로세스는 실제로 호출됩니다. `result` 메서드로 이런 프로세스의 결과를 쉽게 만들 수 있습니다:

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

종료 코드나 에러 출력을 지정할 필요 없다면, 단순 문자열로 가짜 프로세스 결과를 지정하는 편이 더 편리할 수도 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 가짜 처리

테스트 대상 코드가 동일 명령을 가진 여러 프로세스를 호출할 경우, 호출 횟수마다 다른 가짜 결과를 지정할 수 있습니다. 이는 `Process` 파사드의 `sequence` 메서드로 구현할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
                ->push(Process::result('First invocation'))
                ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 수명주기 가짜 처리

지금까지는 주로 `run` 메서드를 이용한 동기 프로세스 가짜 처리에 대해 이야기했습니다. 그러나 `start`를 통해 실행되는 비동기 프로세스와 상호작용하는 코드를 테스트하려면 더 정교한 가짜 처리 기술이 필요합니다.

예를 들어, 비동기 프로세스와 상호작용하는 다음과 같은 라우트가 있다고 가정해 봅시다:

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

이 프로세스를 적절히 가짜 처리하려면, `running` 메서드가 몇 번 `true`를 반환해야 하는지 기술할 수 있어야 하며, 순차적으로 반환할 여러 출력 라인도 지정할 수 있어야 합니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예시에서 `output` 및 `errorOutput` 메서드로 순차적으로 반환할 여러 출력 라인을 지정합니다. `exitCode`는 가짜 프로세스의 최종 종료 코드를 나타내고, `iterations`는 `running` 메서드가 `true`를 몇 번 반환할지 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 단언문

앞서 [프로세스 가짜 처리](#faking-processes)에서 언급했듯, Laravel은 기능 테스트를 위한 여러 프로세스 단언문을 제공합니다. 아래에서 각 단언문을 설명합니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 실행되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan`은 클로저 인수도 받으며, 이 클로저는 프로세스와 프로세스 결과 인스턴스를 전달받아 프로세스 설정을 검사할 수 있습니다. 클로저가 `true`를 반환하면 단언이 통과합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`assertRan` 클로저의 `$process`는 `Illuminate\Process\PendingProcess`, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 실행되지 않았음을 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertDidntRun`도 클로저 인수를 받으며, 이 클로저에서 프로세스와 프로세스 결과 인스턴스를 확인할 수 있습니다. 클로저가 `true`를 반환하면 단언이 실패합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정한 횟수만큼 실행되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes`도 클로저 인수를 받아 프로세스 구성 옵션을 검사할 수 있습니다. 클로저가 `true`를 반환하고 지정한 횟수만큼 실행되었다면 단언이 통과합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 예기치 않은 프로세스 방지

개별 테스트나 전체 테스트 스위트 내에서 호출되는 모든 프로세스가 가짜 처리되었는지 보장하고 싶다면 `preventStrayProcesses` 메서드를 호출하세요. 이 메서드를 호출하면 가짜 결과가 없는 프로세스 호출 시 실제 프로세스 실행 대신 예외가 발생합니다:

```
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 가짜 응답 반환...
Process::run('ls -la');

// 예외 발생...
Process::run('bash import.sh');
```