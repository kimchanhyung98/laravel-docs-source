# 프로세스

- [소개](#introduction)
- [프로세스 실행](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID 및 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [프로세스 풀 이름 지정](#naming-pool-processes)
    - [풀 프로세스 ID 및 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 페이크](#faking-processes)
    - [특정 프로세스 페이크](#faking-specific-processes)
    - [프로세스 시퀀스 페이크](#faking-process-sequences)
    - [비동기 프로세스 생명주기 페이크](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어설션](#available-assertions)
    - [불필요한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/7.0/components/process.html)를 감싼 간결하고 표현력 있는 API를 제공하여, Laravel 애플리케이션에서 외부 프로세스를 손쉽게 호출할 수 있도록 지원합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 최적의 개발자 경험에 초점을 맞추고 있습니다.

<a name="invoking-processes"></a>
## 프로세스 실행

프로세스를 실행하려면 `Process` 파사드에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 완료될 때까지 대기하며, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 방법 모두 살펴보겠습니다. 먼저, 기본적인 동기 프로세스 실행 및 결과 확인 방법을 알아보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

`run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에는 여러 유용한 메서드가 포함되어 있어 프로세스 결과를 검사할 수 있습니다:

```php
$result = Process::run('ls -la');

$result->successful();
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
#### 예외 발생

프로세스 결과의 종료 코드가 0보다 큰 경우(즉, 실패를 나타내는 경우) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

프로세스를 실행하기 전에 그 행동을 커스터마이즈해야 할 수도 있습니다. Laravel에서는 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 옵션을 자유롭게 조정할 수 있습니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용하여 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값

`input` 메서드를 사용하면 프로세스의 표준 입력(standard input)에 입력값을 제공할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

프로세스는 기본적으로 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 하지만 `timeout` 메서드로 이 동작을 변경할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 사용하세요:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무 출력도 반환하지 않고 실행될 수 있는 최대 초를 지정합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 통해 프로세스에 환경 변수를 제공할 수 있습니다. 실행된 프로세스는 시스템에 정의된 모든 환경 변수도 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속받은 환경 변수를 제거하려면 해당 환경 변수 값을 `false`로 지정하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 이용해 프로세스에서 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입출력을 프로그램의 입출력과 연결해, 예를 들어 Vim, Nano 같은 에디터를 프로세스로 열 수 있게 해줍니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞에서 언급한 것처럼, 프로세스 결과의 `output`(stdout) 및 `errorOutput`(stderr) 메서드를 사용해 프로세스 출력을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드의 두 번째 인자로 클로저를 전달하면 실시간으로 출력을 수집할 수 있습니다. 클로저는 "type"(출력 종류: `stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또, 특정 문자열이 프로세스 출력에 포함되어 있는지 간편하게 확인할 수 있도록 `seeInOutput` 및 `seeInErrorOutput` 메서드도 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 지나치게 많은 출력을 생성할 때, 이 출력을 사용할 필요가 없다면 출력 수집 자체를 비활성화하여 메모리를 절약할 수 있습니다. 이를 위해 프로세스 빌드 시 `quietly` 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 사용하고 싶을 수 있습니다. 이러한 작업을 “파이프(piping)”라고 하며, `Process` 파사드의 `pipe` 메서드로 쉽게 구현할 수 있습니다. `pipe` 메서드는 파이프된 프로세스들을 동기적으로 실행하며, 파이프라인 내 마지막 프로세스의 결과를 반환합니다:

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

만약 파이프라인을 구성하는 개별 프로세스를 커스터마이즈할 필요가 없다면, `pipe` 메서드에 명령어 문자열 배열을 간단히 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

실시간으로 프로세스 출력을 수집하려면, `pipe` 메서드의 두 번째 인자로 클로저를 전달하면 됩니다. 클로저는 출력 종류(`stdout`, `stderr`)와 출력 문자열을 인자로 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel은 각 파이프라인 내부의 프로세스에 `as` 메서드로 문자열 키를 지정하는 것도 지원합니다. 이 키는 출력 클로저에도 전달되어 출력이 어느 프로세스에서 나온 것인지 식별할 수 있습니다:

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

`run` 메서드가 동기적으로 프로세스를 실행하는 반면, `start` 메서드는 프로세스를 비동기적으로 실행할 수 있습니다. 이를 통해 프로세스가 백그라운드에서 실행되는 동안 애플리케이션은 다른 작업을 계속 수행할 수 있습니다. 프로세스가 실행된 후에는 `running` 메서드를 통해 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

위에서 볼 수 있듯, `wait` 메서드를 호출하여 프로세스가 완료될 때까지 기다린 후 프로세스 결과 인스턴스를 받아올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 시그널

`id` 메서드는 실행 중인 프로세스의 운영체제 할당 프로세스 ID를 조회합니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 사용해 실행 중인 프로세스에 "시그널"을 보낼 수 있습니다. 미리 정의된 시그널 상수는 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때 전체 현재 출력을 `output` 및 `errorOutput` 메서드로 확인할 수 있지만, `latestOutput` 및 `latestErrorOutput` 메서드를 이용하면 마지막 조회 이후로 발생한 출력만 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

동기식 실행과 마찬가지로, 비동기 프로세스에서도 `start` 메서드의 두 번째 인자로 클로저를 전달하면 실시간으로 출력을 받을 수 있습니다. 클로저에는 출력 종류와 출력 문자열이 전달됩니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 기다리는 대신, `waitUntil` 메서드를 통해 프로세스 출력 기반 조건이 만족되었을 때 대기를 멈출 수도 있습니다. 클로저가 `true`를 반환하면 Laravel은 프로세스가 끝나기를 더 이상 기다리지 않습니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스가 실행 중일 때, `ensureNotTimedOut` 메서드로 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 프로세스가 타임아웃된 경우 [타임아웃 예외](#timeouts)를 발생시킵니다:

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

Laravel은 동시에 여러 개의 비동기 프로세스를 풀(pool)로 관리할 수 있게 도와주며, 이를 통해 여러 작업을 손쉽게 병렬 실행할 수 있습니다. 시작하려면 `Illuminate\Process\Pool` 인스턴스를 인자로 받는 클로저를 `pool` 메서드에 전달하세요.

클로저 안에서 풀에 속할 프로세스들을 정의할 수 있습니다. 프로세스 풀을 `start`로 시작하면, `running` 메서드로 현재 실행 중인 프로세스 컬렉션을 가져올 수 있습니다:

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

모든 풀 프로세스가 완료될 때까지 기다렸다가, `wait` 메서드로 각 프로세스의 결과 인스턴스를 키로 접근할 수 있는 배열 객체로 받아올 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

조금 더 간결하게, `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 즉시 시작하고 결과를 곧바로 받아올 수 있습니다. 이는 PHP의 배열 구조 분해(destructuring) 문법과 결합하면 더욱 표현력이 좋습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 프로세스 풀 이름 지정

숫자 키로 프로세스 풀 결과를 접근하는 것은 표현력이 떨어지므로, Laravel에서는 `as` 메서드를 통해 풀 내 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키 역시 `start`에 전달된 클로저에도 넘겨져 어떤 프로세스의 출력인지 쉽게 알 수 있습니다:

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
### 풀 프로세스 ID 및 시그널

프로세스 풀의 `running` 메서드는 풀 내의 모든 실행 중인 프로세스 컬렉션을 반환하므로, 개별 프로세스의 ID에 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또, 편리하게 풀 전체에 시그널을 보내고 싶다면 `signal` 메서드를 호출하면 풀 내 모든 프로세스에 시그널이 전달됩니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

Laravel의 여러 서비스와 마찬가지로, 프로세스 서비스 역시 간편하고 표현력 있게 테스트를 작성할 수 있는 기능을 제공합니다. `Process` 파사드의 `fake` 메서드를 사용하면, 프로세스가 실행될 때 Laravel이 스텁/더미 결과를 반환하도록 할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이크

Laravel의 페이크 프로세스 기능을 살펴보기 위해, 프로세스를 실행하는 경로(route)를 예시로 들어보겠습니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 경로(route)를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인자 없이 호출하면 모든 프로세스 실행에 대해 더미(성공) 결과가 반환되도록 할 수 있습니다. 또한 해당 프로세스가 실제로 실행(호출)되었는지 [어설트(assert)](#available-assertions)할 수도 있습니다:

```php tab=Pest
<?php

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 단순 프로세스 어설션...
    Process::assertRan('bash import.sh');

    // 프로세스 설정값 검사...
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

        // 단순 프로세스 어설션...
        Process::assertRan('bash import.sh');

        // 프로세스 설정값 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

위와 같이, `Process` 파사드에 `fake`를 호출하면 기본적으로 아무 출력 없이 항상 성공하는 프로세스 결과가 반환됩니다. 하지만 `Process` 파사드의 `result` 메서드를 사용해 페이크 프로세스의 출력과 종료 코드를 쉽게 지정할 수 있습니다:

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
### 특정 프로세스 페이크

앞서 본 예시처럼, `Process` 파사드의 `fake` 메서드에 배열을 전달하면 개별 명령어별로 서로 다른 페이크 결과를 지정할 수 있습니다.

배열의 키는 페이크할 명령 패턴을 나타내고 값은 결과입니다. `*`(별표)는 와일드카드로 사용 가능합니다. 페이크로 지정하지 않은 명령은 실제로 실행됩니다. 명령의 페이크/스텁 결과를 작성할 때는 `Process` 파사드의 `result` 메서드를 사용하면 됩니다:

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

페이크 프로세스의 종료 코드나 에러 출력을 커스터마이즈할 필요가 없다면, 간단히 결과 문자열을 값으로 써도 됩니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크

테스트 중에 동일한 명령을 여러 번 호출하는 경우, 각 프로세스 호출마다 서로 다른 페이크 결과를 지정하고 싶을 수 있습니다. 이때는 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 페이크

지금까지는 주로 `run` 메서드를 이용한 동기식 페이크 프로세스에 대해 다루었습니다. 그러나 `start`로 실행되는 비동기 프로세스와 상호작용하는 코드를 테스트해야 한다면, 좀 더 섬세한 페이크 방법이 필요합니다.

예를 들어, 아래와 같은 비동기 프로세스와 상호작용하는 경로를 생각해봅시다:

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

이 프로세스를 제대로 페이크 하려면, `running` 메서드가 몇 번 `true`를 반환해야 하는지 지정할 수 있어야 합니다. 또한 여러 줄의 출력값도 차례대로 반환되게 지정하고 싶을 수 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예제에서, `output` 및 `errorOutput` 메서드를 이용해 여러 줄의 출력이 순차적으로 반환되게 지정할 수 있습니다. 페이크 프로세스의 최종 종료 코드는 `exitCode` 메서드로, `running` 메서드가 `true`를 반환할 횟수는 `iterations` 메서드로 설정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어설션

[앞서 설명한](#faking-processes) 것처럼, Laravel은 기능 테스트를 위한 다양한 프로세스 어설션 메서드를 제공합니다. 아래에 각 어설션을 소개합니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 호출(실행)되었는지 어설트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드에는 클로저를 전달할 수도 있으며, 이 클로저는 프로세스 인스턴스와 프로세스 결과 인스턴스를 인자로 받아, 프로세스의 옵션을 확인할 수 있습니다. 클로저가 `true`를 반환하면 어설션은 "통과"합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`$process`는 `Illuminate\Process\PendingProcess`, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 호출되지 않았는지 어설트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 동일하게, `assertDidntRun`에도 클로저를 전달할 수 있으며, 클로저가 `true`를 반환하면 어설션은 "실패"합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정한 횟수만큼 호출되었는지 어설트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes`도 클로저를 받을 수 있으며, 클로저가 `true`를 반환하고 프로세스가 지정한 횟수만큼 호출되었다면 어설션이 "통과"합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 방지

각 테스트 또는 전체 테스트 스위트 전반에 걸쳐 모든 프로세스 호출이 반드시 페이크 되도록 보장하고 싶다면, `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드를 호출하면 페이크 결과가 없는 프로세스 호출은 실제 실행되지 않고 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 페이크 응답이 반환됩니다...
Process::run('ls -la');

// 예외가 발생합니다...
Process::run('bash import.sh');
```
