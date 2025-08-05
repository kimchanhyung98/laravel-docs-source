# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 신호](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 이름 지정](#naming-pool-processes)
    - [풀 프로세스 ID와 신호](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 모의](#faking-processes)
    - [특정 프로세스 모의](#faking-specific-processes)
    - [프로세스 시퀀스 모의](#faking-process-sequences)
    - [비동기 프로세스 라이프사이클 모의](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 단언문](#available-assertions)
    - [불필요한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 기반으로 간결하고 표현력 있는 API를 제공하여, 여러분의 Laravel 애플리케이션에서 외부 프로세스를 손쉽게 호출할 수 있도록 합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 중점을 두고 설계되었습니다.

<a name="invoking-processes"></a>
## 프로세스 호출 (Invoking Processes)

프로세스를 호출하려면, `Process` 파사드에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 완료될 때까지 기다리며, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 방식을 모두 살펴보겠습니다. 먼저, 기본적인 동기 방식 프로세스를 호출하고 그 결과를 확인하는 방법을 보겠습니다:

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
#### 예외 발생 (Throwing Exceptions)

프로세스 결과를 받아서, 종료 코드가 0보다 클 때(즉, 실패한 경우) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면, `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면, 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션 (Process Options)

때때로, 프로세스를 실행하기 전에 동작을 세밀하게 조정해야 할 수 있습니다. Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 기능을 손쉽게 설정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로 지정 (Working Directory Path)

`path` 메서드를 사용하여 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면, 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속받습니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값 지정 (Input)

`input` 메서드를 통해 프로세스의 표준 입력으로 입력값을 제공할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃 (Timeouts)

기본적으로 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 하지만, `timeout` 메서드를 통해 이 동작을 변경할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또는, 프로세스 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 호출할 수 있습니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무런 출력을 반환하지 않고 실행될 수 있는 최대 초를 지정할 수 있습니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수 (Environment Variables)

`env` 메서드를 사용하여 프로세스에 환경 변수를 제공할 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속받은 환경 변수 중 하나를 제거하고 싶다면, 해당 환경 변수의 값을 `false`로 지정하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드 (TTY Mode)

`tty` 메서드를 사용하여 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입출력을 프로그램의 입출력과 연결하여, 프로세스가 Vim 또는 Nano와 같은 편집기를 열 수 있도록 해줍니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력 (Process Output)

앞서 설명한 것처럼, 프로세스의 출력은 프로세스 결과 객체에서 `output`(stdout), `errorOutput`(stderr) 메서드를 통해 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, 출력 결과를 실시간으로 받아올 수도 있는데, 이 경우 `run` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다. 이 클로저는 "타입"(stdout 또는 stderr)과 출력 문자열 두 개의 인수를 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또한 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공하여, 출력 결과에 특정 문자열이 포함되어 있는지 손쉽게 확인할 수 있게 도와줍니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화 (Disabling Process Output)

프로세스가 매우 많은 출력을 쏟아내지만, 이 내용이 필요하지 않을 때는, 출력값 가져오기를 완전히 비활성화하여 메모리 사용을 줄일 수 있습니다. 이를 위해 프로세스 구성 시 `quietly` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인 (Pipelines)

때때로 한 프로세스의 출력을 다른 프로세스의 입력으로 사용하고자 할 수 있습니다. 이처럼 한 프로세스의 출력을 다른 프로세스로 "파이핑"하는 과정을 쉽게 구현할 수 있도록, `Process` 파사드는 `pipe` 메서드를 제공합니다. 이 메서드는 파이프라인의 각 프로세스를 동기적으로 실행한 후, 마지막 프로세스의 결과를 반환합니다:

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

파이프라인을 구성하는 각 프로세스를 세부적으로 설정할 필요가 없다면, 단순히 명령어 문자열 배열을 `pipe` 메서드에 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

실시간으로 파이프라인 출력을 받고자 한다면, 두 번째 인수로 클로저를 전달하세요. 이 클로저는 "타입"(stdout 또는 stderr)과 출력 문자열 두 개의 인수를 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel에서는 파이프라인의 각 프로세스에 `as` 메서드를 통해 문자열 키를 부여할 수도 있습니다. 이 키는 출력 처리 클로저에도 함께 전달되어, 어떤 프로세스의 출력인지 쉽게 식별할 수 있습니다:

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

`run` 메서드는 프로세스를 동기적으로 실행하는 반면, `start` 메서드는 비동기적으로 프로세스를 실행할 수 있습니다. 이 방식을 사용하면 프로세스가 백그라운드에서 실행되는 동안에도 애플리케이션이 다른 작업을 계속 수행할 수 있습니다. 프로세스가 시작된 후에는, `running` 메서드를 통해 프로세스 실행 여부를 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

보시다시피, `wait` 메서드를 호출하여 프로세스가 완전히 종료될 때까지 기다리고, 프로세스 결과 인스턴스를 받아올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 신호 (Process IDs and Signals)

`id` 메서드는 실행 중인 프로세스의 운영체제에서 할당된 프로세스 ID를 반환합니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 통해 실행 중인 프로세스에 "신호(signal)"를 보낼 수 있습니다. 미리 정의된 신호 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인하실 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력 (Asynchronous Process Output)

비동기 프로세스가 실행 중일 때, `output` 및 `errorOutput` 메서드를 사용하여 전체 출력을 실시간으로 받아올 수 있습니다. 또한, `latestOutput` 및 `latestErrorOutput` 메서드를 이용하면, 마지막으로 출력을 받아온 이후 새롭게 만들어진 출력만 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드와 마찬가지로, 비동기 프로세스의 출력도 `start` 메서드의 두 번째 인수로 클로저를 전달하여 실시간으로 받아올 수 있습니다. 이 클로저는 "타입"(stdout 또는 stderr)과 출력 문자열 두 개의 인수를 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 대기하는 대신, `waitUntil` 메서드를 사용하여 프로세스 출력에 따라 대기를 멈출 수 있습니다. `waitUntil`에 넘긴 클로저가 `true`를 반환하면, 프로세스가 아직 종료되지 않았더라도 대기가 중지됩니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃 (Asynchronous Process Timeouts)

비동기 프로세스가 실행 중일 때, `ensureNotTimedOut` 메서드를 사용해 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 만약 타임아웃된 경우에는 [타임아웃 예외](#timeouts)가 발생합니다:

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

Laravel은 동시 실행되는 비동기 프로세스의 풀(pool)을 쉽게 다룰 수 있는 기능을 제공하여, 여러 작업을 동시에 효율적으로 수행할 수 있게 해줍니다. 먼저, `pool` 메서드를 호출하여 사용을 시작하세요. 이 메서드는 `Illuminate\Process\Pool` 인스턴스를 받는 클로저를 인수로 받습니다.

이 클로저 내에서 풀에 속하는 프로세스를 정의할 수 있습니다. 풀을 `start` 메서드로 실행한 뒤에는, `running` 메서드를 사용해 [컬렉션](/docs/12.x/collections) 형태로 동작 중인 프로세스 목록에 접근할 수 있습니다:

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

위 예시처럼, `wait` 메서드를 호출하여 풀에 포함된 모든 프로세스가 완료될 때까지 대기하고, 각 프로세스의 결과에 접근할 수 있습니다. `wait` 메서드는 배열처럼 접근 가능한 객체를 반환합니다. 이 객체를 통해 각 프로세스의 실행 결과 인스턴스에 키를 통해 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

또는, 편의상 `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 시작하고 곧바로 결과를 대기할 수 있습니다. 이 방법은 PHP의 배열 구조 분해와 함께 사용하면 더욱 읽기 쉬운 코드를 작성할 수 있습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 이름 지정 (Naming Pool Processes)

숫자 키로 프로세스 풀 결과에 접근하는 것은 명확하지 않을 수 있으므로, `as` 메서드를 이용해 풀 내 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키는 `start` 메서드에 전달하는 클로저에도 함께 전달되어, 어떤 프로세스에 대한 출력인지 쉽게 알 수 있습니다:

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
### 풀 프로세스 ID와 신호 (Pool Process IDs and Signals)

프로세스 풀의 `running` 메서드는 풀 내에서 실행 중인 모든 프로세스의 컬렉션을 제공합니다. 이를 통해 각 풀 프로세스의 ID에도 손쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 편의상 프로세스 풀에 대해 `signal` 메서드를 호출하여 풀 내 모든 프로세스에 신호를 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 다양한 서비스는 손쉽고 표현력 있는 테스트 작성을 위한 기능을 제공합니다. 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면, 프로세스 실행 시 실제가 아닌 더미 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 모의 (Faking Processes)

Laravel의 프로세스 모의 기능을 살펴보기 위해, 프로세스를 호출하는 라우트를 만들었다고 가정해 봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출하여 모든 프로세스에 대해 성공적인 모의 결과를 반환하도록 할 수 있습니다. 또한, [단언문](#available-assertions)을 이용해 특정 프로세스가 "실행되었는지" 확인할 수도 있습니다:

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 단순 프로세스 단언...
    Process::assertRan('bash import.sh');

    // 또는, 프로세스 설정 값 확인...
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

        // 단순 프로세스 단언...
        Process::assertRan('bash import.sh');

        // 또는, 프로세스 설정 값 확인...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

앞서 설명한 대로, `Process` 파사드의 `fake` 메서드는 항상 출력이 없는 성공적인 프로세스 결과를 반환하도록 만듭니다. 하지만, `Process` 파사드의 `result` 메서드를 사용하면 모의 프로세스의 출력 및 종료 코드를 손쉽게 지정할 수 있습니다:

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
### 특정 프로세스 모의 (Faking Specific Processes)

앞선 예제와 같이 `Process` 파사드는 각 프로세스별로 다른 모의 결과를 배열 형태로 지정할 수 있습니다.

배열의 키에는 모의할 명령 패턴을, 값에는 해당 결과를 지정합니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 모의 설정이 없는 명령은 실제로 실행됩니다. `Process` 파사드의 `result` 메서드를 사용하여 이러한 명령의 모의 결과를 만들 수 있습니다:

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

모의 프로세스의 종료 코드나 에러 출력을 커스텀할 필요가 없다면, 더 간단하게 문자열로 결과를 지정할 수도 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 모의 (Faking Process Sequences)

테스트 중인 코드가 같은 명령어로 여러 번 프로세스를 호출한다면, 각 호출별로 다른 모의 결과를 부여하고 싶을 수 있습니다. 이를 위해 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 라이프사이클 모의 (Faking Asynchronous Process Lifecycles)

지금까지는 주로 `run` 메서드를 이용해 동기적으로 호출되는 프로세스의 모의에 대해 다뤘습니다. 하지만, `start`를 사용해 비동기 프로세스를 다루는 코드를 테스트할 때는 더 정교한 모의 설정이 필요할 수 있습니다.

예를 들어, 다음처럼 비동기 프로세스를 다루는 라우트를 상상해 봅시다:

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

이 프로세스를 적절히 모의하려면, `running` 메서드가 몇 번이나 `true`를 반환해야 하는지 지정할 수 있어야 하며, 여러 줄의 출력도 순차적으로 반환하고 싶을 수 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예시처럼, `output`과 `errorOutput` 메서드로 여러 줄의 출력을 순차적으로 지정할 수 있습니다. `exitCode` 메서드는 모의 프로세스의 최종 종료 코드를, `iterations` 메서드는 `running` 메서드가 `true`를 반환할 횟수를 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 단언문 (Available Assertions)

[앞서 설명한 대로](#faking-processes), Laravel은 기능 테스트를 위한 여러 프로세스 단언문을 제공합니다. 아래에서 각 단언문을 살펴보겠습니다.

<a name="assert-process-ran"></a>
#### assertRan

주어진 프로세스가 실행되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 받을 수 있습니다. 이 클로저는 프로세스 인스턴스와 프로세스 결과를 받아, 구성 옵션을 자유롭게 검사할 수 있습니다. 클로저가 `true`를 반환하면 단언이 "성공"한 것으로 간주합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

클로저에 전달되는 `$process`는 `Illuminate\Process\PendingProcess` 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

주어진 프로세스가 실행되지 않았음을 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 마찬가지로, `assertDidntRun`도 클로저를 받을 수 있습니다. 이 클로저가 `true`를 반환하면 단언이 "실패"하게 됩니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

주어진 프로세스가 특정 횟수만큼 실행되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 메서드도 클로저를 받을 수 있습니다. 클로저가 `true`를 반환하고, 프로세스가 지정된 횟수만큼 실행되었다면 단언이 "성공"합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 방지 (Preventing Stray Processes)

테스트 개별 단위 또는 전체 테스트에서 모든 프로세스가 반드시 모의(faked)돼 있어야 한다면, `preventStrayProcesses` 메서드를 호출하세요. 이 메서드를 호출한 후 모의 결과가 없는 프로세스를 실행하면 실제 실행 대신 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 모의 응답이 반환됨...
Process::run('ls -la');

// 예외가 발생함...
Process::run('bash import.sh');
```
