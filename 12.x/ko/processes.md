# 프로세스 (Processes)

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
    - [풀 프로세스 명명](#naming-pool-processes)
    - [풀 프로세스 ID 및 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 페이크](#faking-processes)
    - [특정 프로세스 페이크](#faking-specific-processes)
    - [프로세스 시퀀스 페이크](#faking-process-sequences)
    - [비동기 프로세스 생명주기 페이크](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [불필요한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html) 위에 직관적이고 최소한의 API를 제공하여, Laravel 애플리케이션 내에서 외부 프로세스를 편리하게 실행할 수 있게 합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="invoking-processes"></a>
## 프로세스 실행 (Invoking Processes)

프로세스를 실행하기 위해서는 `Process` 파사드의 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 실행이 완료될 때까지 기다리며, `start` 메서드는 비동기 방식의 프로세스 실행에 사용됩니다. 이 문서에서는 두 가지 방법 모두를 다룹니다. 먼저, 기본적인 동기 프로세스를 실행하고 결과를 확인하는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 확인할 수 있는 다양한 유용한 메서드를 제공합니다:

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

프로세스 결과를 가지고 있으며, 종료 코드가 0보다 클 경우(즉, 실패를 의미), `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 `ProcessResult` 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션 (Process Options)

시작 전 프로세스의 동작을 세밀하게 제어하고 싶을 수 있습니다. Laravel은 작업 디렉토리, 타임아웃, 환경 변수 등 다양한 프로세스 설정을 쉽게 변경할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 작업 디렉토리 경로

`path` 메서드를 사용해 프로세스의 작업 디렉토리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면, 현재 실행 중인 PHP 스크립트의 작업 디렉토리를 상속하게 됩니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값

`input` 메서드를 사용하여 프로세스의 표준 입력(standard input)을 통해 데이터를 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 하지만 `timeout` 메서드를 통해 이 동작을 변경할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

프로세스의 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 사용할 수 있습니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무런 출력을 반환하지 않고 최대 실행될 수 있는 시간을 초 단위로 지정할 수 있습니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 통해 프로세스에 환경 변수(environment variables)를 전달할 수 있습니다. 실행된 프로세스는 시스템에 정의된 모든 환경 변수도 함께 상속합니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경 변수 중 특정 변수를 제거하고 싶을 경우, 해당 환경 변수에 `false` 값을 지정하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드는 프로세스에서 TTY 모드를 활성화합니다. 이는 프로세스의 입력 및 출력을 프로그램의 입력 및 출력과 연결시켜, 프로세스가 Vim 또는 Nano와 같은 편집기를 열 수 있게 해줍니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력 (Process Output)

앞서 설명한 것처럼, 프로세스 출력은 결과 객체의 `output`(stdout) 및 `errorOutput`(stderr) 메서드로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, 출력 결과를 실시간으로 수집하려면 `run` 메서드의 두 번째 인자로 클로저(익명 함수)를 전달하면 됩니다. 이 클로저는 출력의 "종류"(stdout 또는 stderr)와 출력 문자열을 인자로 전달받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 특정 문자열이 프로세스의 출력 결과에 포함되어 있는지 손쉽게 확인할 수 있도록 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

관심이 없는 많은 양의 출력이 발생하는 프로세스를 실행해야 할 경우, 출력 수집 자체를 비활성화하여 메모리 사용량을 절감할 수 있습니다. 이를 위해 프로세스 빌드 시 `quietly` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인 (Pipelines)

때때로 한 프로세스의 출력을 다음 프로세스의 입력으로 사용하고 싶을 수 있습니다. 이것을 프로세스의 "파이프(piping)"라고 부릅니다. `Process` 파사드의 `pipe` 메서드는 이 기능을 간편하게 제공합니다. `pipe` 메서드는 연결된 프로세스들을 동기적으로 실행하며, 파이프라인의 마지막 프로세스 결과를 반환합니다:

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

파이프라인을 구성하는 각각의 프로세스를 따로 설정할 필요가 없다면, 명령어 문자열 배열을 그대로 `pipe` 메서드에 전달할 수 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

프로세스의 출력 역시, 두 번째 인자로 클로저를 전달하여 실시간으로 받아볼 수 있습니다. 클로저는 출력의 종류(`stdout` 또는 `stderr`)와 출력 문자열을 인자로 전달받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

또한, 파이프라인 내의 각 프로세스에 문자열 키를 `as` 메서드로 지정할 수 있습니다. 이 키 값은 출력 콜백에도 함께 전달되어 어떤 프로세스의 출력인지 식별할 수 있습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 비동기 프로세스 (Asynchronous Processes)

`run` 메서드는 동기식으로 프로세스를 실행하지만, `start` 메서드는 비동기식으로 프로세스를 실행할 수 있습니다. 이를 통해 애플리케이션은 프로세스가 백그라운드에서 실행되는 동안 다른 작업들을 계속 수행할 수 있습니다. 실행된 후에는 `running` 메서드를 사용하여 프로세스가 여전히 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

앞의 예시에서 볼 수 있듯이, `wait` 메서드를 호출하면 프로세스가 종료될 때까지 기다린 뒤, `ProcessResult` 인스턴스를 반환합니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 시그널

`id` 메서드는 실행 중인 프로세스의 운영체제에서 할당한 프로세스 ID를 반환합니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

실행 중인 프로세스에 "시그널(signal)"을 보낼 때는 `signal` 메서드를 사용할 수 있습니다. 미리 정의된 시그널 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, 전체 출력 결과를 `output` 및 `errorOutput` 메서드로 즉시 접근할 수 있습니다. 또한, `latestOutput` 및 `latestErrorOutput` 메서드를 사용하면 이전 출력 이후 새롭게 생성된 내용만 가져올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드와 마찬가지로, `start` 메서드의 두 번째 인자로 클로저를 전달하면 비동기 프로세스의 출력을 실시간으로 받아볼 수 있습니다. 클로저는 출력의 종류(`stdout` 또는 `stderr`)와 출력 문자열을 전달받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 완전히 종료될 때까지 기다리는 대신, 출력 기반으로 대기 동작을 제어할 수도 있습니다. `waitUntil` 메서드는 클로저의 반환값이 `true`가 될 때 프로세스 대기를 중단합니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스 실행 중 해당 프로세스가 타임아웃되지 않았는지 항상 확인하려면 `ensureNotTimedOut` 메서드를 사용할 수 있습니다. 프로세스가 타임아웃된 경우 [타임아웃 예외](#timeouts)가 발생합니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## 동시 프로세스 (Concurrent Processes)

Laravel에서는 여러 비동기 프로세스 풀(pool)을 쉽고 간편하게 관리할 수 있어, 여러 작업을 동시에 병렬로 실행하는 것이 매우 간단합니다. 시작하려면 `pool` 메서드를 호출하세요. 이 메서드는 `Illuminate\Process\Pool` 인스턴스를 인자로 받는 클로저를 전달받습니다.

이 클로저 내에서 풀에 포함될 프로세스를 정의할 수 있습니다. 풀을 `start` 메서드로 실행하면, 실행 중인 프로세스의 [컬렉션](/docs/12.x/collections)에 접근할 수 있습니다:

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

위 예시와 같이, 풀 내 모든 프로세스의 실행이 종료될 때까지 `wait` 메서드로 결과를 받을 수 있습니다. `wait` 메서드는 배열처럼 접근 가능한 객체를 반환하며, 각 프로세스의 키를 통해 `ProcessResult` 인스턴스에 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

좀 더 간단하게, `concurrently` 메서드를 사용해 비동기 프로세스 풀을 시작하고 즉시 결과를 기다릴 수도 있습니다. PHP의 배열 분해 문법과 함께 쓰면 코드를 더 간결하게 만들 수 있습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 명명

풀의 결과를 숫자 인덱스로 접근하는 것은 코드의 가독성이 떨어질 수 있습니다. 그래서 Laravel은 각 풀 프로세스에 `as` 메서드로 문자열 키를 할당할 수 있도록 지원합니다. 이 키 값은 `start` 메서드의 콜백에도 전달되어 출력 주체를 식별할 수 있습니다:

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

풀의 `running` 메서드는 풀에 실행된 모든 프로세스 컬렉션을 반환하므로, 손쉽게 각 프로세스의 ID에 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 편의를 위해 프로세스 풀에 `signal` 메서드를 호출하여 풀의 모든 프로세스에 시그널을 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스들은 테스트를 쉽게 표현적으로 작성할 수 있도록 다양한 기능을 제공합니다. Laravel의 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면, 프로세스 실행시 미리 지정된 더미 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이크 (Faking Processes)

Laravel의 프로세스 페이크 기능을 살펴보기 위해, 다음과 같은 라우트를 상상해보겠습니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 별도의 인자 없이 호출하면 모든 프로세스 실행에 대해 성공(출력 없음) 상태의 더미 결과가 반환됩니다. 또한, 해당 프로세스가 "실제로 실행됐는지" [어서션](#available-assertions)도 할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 간단한 프로세스 어서션...
    Process::assertRan('bash import.sh');

    // 또는 프로세스 설정을 검사할 수도 있습니다...
    Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
        return $process->command === 'bash import.sh' &&
               $process->timeout === 60;
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // 간단한 프로세스 어서션...
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정을 검사할 수도 있습니다...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

설명한 것처럼, `Process` 파사드의 `fake` 메서드는 항상 아무 출력도 없는 성공(0) 상태의 결과를 반환합니다. 그러나 필요하다면 `Process` 파사드의 `result` 메서드로 페이크 프로세스의 출력 및 종료 코드를 손쉽게 지정할 수 있습니다:

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
### 특정 프로세스 페이크 (Faking Specific Processes)

이전 예시에서 볼 수 있듯이, `Process` 파사드는 `fake` 메서드에 배열을 전달해 프로세스별로 다른 페이크 결과를 지정할 수 있습니다.

이 배열의 키는 페이크할 명령어 패턴이고, 값은 해당 결과를 의미합니다. `*` 문자로 와일드카드 처리가 가능하며, 페이크되지 않은 커맨드는 실제로 실행됩니다. 결과 객체는 `Process` 파사드의 `result` 메서드로 간편하게 만들 수 있습니다:

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

프로세스의 종료 코드 또는 에러 출력을 커스텀할 필요가 없다면, 간단히 문자열로 페이크 결과를 지정할 수 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크 (Faking Process Sequences)

테스트 대상 코드에서 같은 명령어가 여러 프로세스에서 반복 호출되는 경우, 각 호출마다 서로 다른 페이크 결과를 할당하고 싶을 수 있습니다. 이때는 `Process` 파사드의 `sequence` 메서드를 활용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 페이크 (Faking Asynchronous Process Lifecycles)

지금까지는 주로 `run` 메서드로 동기적으로 실행하는 프로세스의 페이크에 대해 살펴보았습니다. 하지만, `start`로 비동기적으로 실행되는 프로세스와 상호작용하는 코드를 테스트하려는 경우에는 더 정교한 접근이 필요할 수 있습니다.

예를 들어, 비동기 프로세스와 상호작용하는 아래의 라우트를 생각해봅시다:

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

이 프로세스를 올바르게 페이크하려면, `running` 메서드가 몇 번쯤 `true`를 반환해야 할지 등 페이크 프로세스의 상태 변화도 기술해야 합니다. 또한 여러 줄의 출력 결과도 순서대로 반환할 수 있어야 합니다. 이를 위해서는 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예시처럼, `output` 및 `errorOutput` 메서드로 여러 출력 라인을 순차적으로 지정할 수 있습니다. `exitCode` 메서드는 페이크 프로세스의 최종 종료 코드를 지정하며, `iterations` 메서드는 `running` 메서드가 몇 번 `true`를 반환할지 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션 (Available Assertions)

[앞서 설명한 것처럼](#faking-processes), Laravel은 기능 테스트를 위한 다양한 프로세스 어서션을 제공합니다. 아래에서 각각을 설명합니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 실행되었는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 인자로 받을 수 있는데, 이때 클로저는 프로세스 인스턴스와 결과를 전달받아 프로세스의 설정을 직접 검사할 수 있습니다. 클로저의 반환값이 `true`면 어서션을 "통과"합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

여기서 `$process`는 `Illuminate\Process\PendingProcess`의 인스턴스이며, `$result`는 `Illuminate\Contracts\Process\ProcessResult`의 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 실행되지 않았는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 마찬가지로, `assertDidntRun`에서도 클로저를 전달받아 프로세스 설정을 검사할 수 있습니다. 이때 클로저가 `true`를 반환하면 어서션은 "실패"합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정된 횟수만큼 실행되었는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 역시 클로저를 전달받을 수 있으며, 지정한 조건과 횟수가 모두 일치할 때 어서션을 "통과"합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 방지 (Preventing Stray Processes)

테스트 코드 또는 전체 테스트 스위트 전반에 걸쳐 실행되는 모든 프로세스가 반드시 페이크되어야 함을 보장하려면, `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드를 사용하면, 페이크 결과가 없는 프로세스 실행 시 실제로 프로세스가 실행되지 않고 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 페이크 결과가 반환됨...
Process::run('ls -la');

// 예외가 발생함...
Process::run('bash import.sh');
```
