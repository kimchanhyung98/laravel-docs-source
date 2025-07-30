# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출하기](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 실행 프로세스](#concurrent-processes)
    - [풀 프로세스에 이름 지정하기](#naming-pool-processes)
    - [풀 프로세스 ID와 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 가짜 처리하기](#faking-processes)
    - [특정 프로세스 가짜 처리하기](#faking-specific-processes)
    - [프로세스 시퀀스 가짜 처리하기](#faking-process-sequences)
    - [비동기 프로세스 생명주기 가짜 처리하기](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [유령 프로세스 방지하기](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 감싸는 표현력 있고 최소한의 API를 제공하여 Laravel 애플리케이션에서 외부 프로세스를 편리하게 호출할 수 있도록 합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발자 경험에 중점을 두고 설계되었습니다.

<a name="invoking-processes"></a>
## 프로세스 호출하기

프로세스를 호출하려면 `Process` 파사드가 제공하는 `run`과 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출하고 해당 프로세스가 완료될 때까지 대기하며, `start` 메서드는 비동기적으로 프로세스를 실행하는 데 사용합니다. 이 문서에서는 두 가지 방법을 모두 살펴보겠습니다. 먼저 기본적인 동기 프로세스를 호출하고 결과를 확인하는 방법을 알아보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론 `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 검사하는 데 유용한 다양한 메서드를 제공합니다:

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

프로세스 결과가 있고, 종료 코드가 0보다 클 경우(즉, 실패를 나타낼 때) `Illuminate\Process\Exceptions\ProcessFailedException` 인스턴스를 던지고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

물론 프로세스를 호출하기 전에 동작을 사용자 정의해야 할 때가 있습니다. 다행히 Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 설정을 조정할 수 있도록 합니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용하면 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 사용하면 프로세스의 표준 입력(stdin)을 통해 입력 값을 제공할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException`을 던집니다. 그러나 `timeout` 메서드로 이 동작을 사용자 정의할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또한 프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 호출하면 됩니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 출력 없이 실행될 수 있는 최대 초 수를 지정하는 데 사용할 수 있습니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 사용하여 프로세스에 환경 변수를 제공할 수 있습니다. 호출된 프로세스는 시스템에서 정의된 모든 환경 변수도 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속받은 환경 변수를 호출된 프로세스에서 제거하려면 해당 변수에 `false` 값을 전달하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 사용하여 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력이 프로그램의 입력과 출력에 연결되도록 해서, 프로세스가 Vim이나 Nano 같은 편집기를 여는 것을 허용합니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞서 언급했듯이 프로세스 출력은 프로세스 결과의 `output`(stdout)과 `errorOutput`(stderr) 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

그러나 출력은 `run` 메서드의 두 번째 인수로 클로저를 전달하여 실시간으로 수집할 수도 있습니다. 클로저는 출력의 "종류" (`stdout` 또는 `stderr`)와 출력 문자열 두 인수를 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 `seeInOutput`과 `seeInErrorOutput` 메서드도 제공하여, 프로세스 출력에 특정 문자열이 포함되어 있는지 쉽고 편리하게 확인할 수 있습니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 매우 많은 출력을 생성하지만 해당 출력에 관심이 없을 경우, 출력 결과 수집을 완전히 비활성화하여 메모리를 절약할 수 있습니다. 이를 위해 `quietly` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때때로 한 프로세스의 출력을 다른 프로세스의 입력으로 연결하고 싶을 때가 있습니다. 이를 흔히 프로세스의 출력을 다른 프로세스에 "파이핑"한다고 합니다. `Process` 파사드가 제공하는 `pipe` 메서드는 이를 쉽게 구현해줍니다. `pipe` 메서드는 연결된 프로세스들을 동기적으로 실행하며, 파이프라인에서 마지막 프로세스의 결과를 반환합니다:

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

파이프라인을 구성하는 개별 프로세스를 세밀하게 제어할 필요가 없으면, 단순히 명령어 문자열 배열을 `pipe` 메서드에 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

`pipe` 메서드의 두 번째 인수로 클로저를 전달하면 출력이 실시간으로 수집됩니다. 이 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열 두 인수를 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

또한 Laravel은 `as` 메서드를 통해 파이프라인 내 각 프로세스에 문자열 키를 할당할 수 있습니다. 이 키는 `pipe` 메서드의 출력 클로저에도 전달되어 어떤 프로세스에서 출력된 것인지 알 수 있습니다:

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

`run` 메서드는 동기적으로 프로세스를 호출하지만, `start` 메서드는 비동기적으로 프로세스를 실행하는 데 사용됩니다. 이를 통해 프로세스가 백그라운드에서 실행되는 동안 애플리케이션이 다른 작업을 계속 수행할 수 있습니다. 프로세스가 호출된 후, `running` 메서드를 사용해 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

보시다시피, `wait` 메서드를 호출하여 프로세스가 종료될 때까지 대기하고 프로세스 결과 인스턴스를 얻을 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드를 사용해 실행 중인 프로세스에 운영체제가 할당한 프로세스 ID를 조회할 수 있습니다:

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

비동기 프로세스가 실행되는 동안, `output`과 `errorOutput` 메서드를 통해 지금까지의 전체 출력을 조회할 수 있습니다. 또한 `latestOutput`과 `latestErrorOutput`을 사용하면 이전 출력 조회 이후에 생긴 최근 출력만 접근할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

또한 `start` 메서드의 두 번째 인수에 클로저를 전달하여 비동기 프로세스의 출력을 실시간으로 수집할 수 있습니다. 클로저는 출력 유형(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 기다리는 대신, `waitUntil` 메서드를 사용해 출력 조건에 따라 기다림을 중단할 수 있습니다. `waitUntil`에 전달된 클로저가 `true`를 반환할 때 Laravel은 프로세스 종료를 기다리는 것을 멈춥니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스 실행 중에 `ensureNotTimedOut` 메서드를 호출해 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 이 메서드는 프로세스가 타임아웃되었다면 [타임아웃 예외](#timeouts)를 던집니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## 동시 실행 프로세스

Laravel은 또한 여러 비동기 프로세스 풀을 쉽게 관리할 수 있도록 지원하여 많은 작업을 동시에 실행할 수 있습니다. 시작하려면, `pool` 메서드를 호출하고 `Illuminate\Process\Pool` 인스턴스를 인수로 받는 클로저를 전달합니다.

이 클로저 내에서 풀에 소속될 프로세스들을 정의할 수 있습니다. `start` 메서드로 프로세스 풀이 시작된 후, `running` 메서드를 통해 실행 중인 프로세스들의 [컬렉션](/docs/12.x/collections)을 접근할 수 있습니다:

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

보시다시피, `wait` 메서드를 사용하면 모든 풀 프로세스가 종료할 때까지 대기하며 결과를 가져올 수 있습니다. `wait`는 각 프로세스 결과에 키로 접근할 수 있는 배열 형태 객체를 반환합니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

또는 편의를 위해 `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 시작하고 즉시 결과를 기다릴 수 있습니다. 이는 PHP 배열 구조 분해 문법과 결합하면 매우 표현력이 풍부한 코드를 작성할 수 있습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스에 이름 지정하기

숫자 키로 풀 프로세스 결과에 접근하는 것은 표현력이 떨어집니다. 그래서 Laravel은 `as` 메서드를 통해 각 프로세스에 문자열 키를 할당할 수 있게 해줍니다. 이 키는 `start` 메서드에 전달된 클로저에도 함께 전달되어 어떤 프로세스 출력인지 구분할 수 있습니다:

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

프로세스 풀의 `running` 메서드가 풀 내 모든 실행된 프로세스 컬렉션을 제공하므로, 아래와 같이 각 프로세스의 운영체제 할당 프로세스 ID를 쉽게 조회할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

편의를 위해 프로세스 풀에 `signal` 메서드를 호출하면 풀 내 모든 프로세스에 한 번에 시그널을 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스가 편리하고 표현력이 높은 테스트 작성을 지원하는 기능을 제공하며, Laravel의 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드는 프로세스가 호출될 때마다 가짜/더미 결과를 반환하도록 Laravel에 지시할 수 있게 합니다.

<a name="faking-processes"></a>
### 프로세스 가짜 처리하기

Laravel의 프로세스 가짜 처리 기능을 살펴보기 위해, 프로세스를 호출하는 라우트를 상상해 봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, 인수 없이 `Process` 파사드의 `fake` 메서드를 호출하면 모든 호출된 프로세스에 대해 가짜의 성공적인 결과를 반환하도록 Laravel을 설정할 수 있습니다. 뿐만 아니라, 특정 프로세스가 "실행되었는지" [어서션](#available-assertions)까지 할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 단순 프로세스 실행 어서션...
    Process::assertRan('bash import.sh');

    // 혹은 프로세스 설정 검사...
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

        // 단순 프로세스 실행 어서션...
        Process::assertRan('bash import.sh');

        // 혹은 프로세스 설정 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

앞서 논의한 대로, `Process` 파사드에 `fake` 메서드를 호출하면 Laravel은 항상 출력 없는 성공적인 프로세스 결과를 반환합니다. 하지만 `Process` 파사드의 `result` 메서드를 통해 출력과 종료 코드를 손쉽게 지정할 수도 있습니다:

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

이전 예제를 보면, `Process` 파사드의 `fake` 메서드는 배열을 받아 명령어 패턴별로 다른 가짜 결과를 지정할 수 있습니다.

이 배열의 키는 가짜 처리할 명령어 패턴을 나타내며, `*`는 와일드카드 문자로 사용할 수 있습니다. 가짜 처리하지 않은 명령어는 실제로 실행됩니다. `Process` 파사드의 `result` 메서드를 이용해 이런 명령어의 더미 결과를 쉽게 생성할 수 있습니다:

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

종료 코드나 오류 출력을 변경할 필요가 없으면, 다음처럼 단순 문자열로 가짜 결과를 지정하는 편이 더 편리할 수도 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 가짜 처리하기

테스트하는 코드가 동일한 명령어로 여러 번 프로세스를 호출한다면, 각 호출에 다른 가짜 결과를 지정하고 싶을 수 있습니다. 이럴 때 `Process` 파사드의 `sequence` 메서드를 사용하면 됩니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 가짜 처리하기

지금까지는 주로 `run` 메서드를 사용해 동기적으로 호출되는 프로세스를 가짜 처리하는 방법을 논의했습니다. 하지만 `start` 메서드를 사용해 비동기 호출되는 프로세스와 상호작용하는 코드를 테스트하려면 더 정교한 가짜 기술이 필요합니다.

예를 들어, 아래와 같이 비동기 프로세스와 상호작용하는 라우트를 생각해 봅시다:

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

이 프로세스를 제대로 가짜 처리하려면, `running` 메서드가 몇 번 `true`를 반환할지 지정할 수 있어야 합니다. 또한 연속해서 반환될 여러 줄 출력을 지정하고 싶을 수도 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예제를 좀 더 자세히 살펴보면, `output`과 `errorOutput` 메서드로 순서대로 반환할 여러 출력 라인을 지정할 수 있습니다. `exitCode` 메서드는 가짜 프로세스의 최종 종료 코드를 지정합니다. `iterations` 메서드는 `running` 메서드가 몇 번 `true`를 반환할지도 설정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션

앞서 [언급한 것처럼](#faking-processes), Laravel은 특징 테스트에서 사용할 수 있는 여러 프로세스 어서션을 제공합니다. 아래에서 각 어서션에 대해 설명하겠습니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 호출되었음을 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan`은 클로저도 인수로 받을 수 있으며, 해당 클로저는 프로세스 인스턴스와 프로세스 결과를 인수로 받아 프로세스 설정을 검사할 수 있습니다. 클로저가 `true`를 반환하면 어서션이 통과합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`assertRan` 클로저에 전달되는 `$process`는 `Illuminate\Process\PendingProcess` 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 호출되지 않았음을 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertDidntRun`도 클로저를 받아 프로세스와 결과를 검사할 수 있습니다. 이 클로저가 `true`를 반환하면 어서션이 "실패"합니다(즉, 해당 프로세스가 호출된 것으로 간주됨):

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정한 횟수만큼 호출되었음을 검증합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 또한 클로저를 받아 프로세스와 결과를 검사할 수 있습니다. 클로저가 `true`를 반환하고, 해당 프로세스가 지정한 횟수만큼 호출되었다면 어서션이 통과합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 유령 프로세스 방지하기

개별 테스트나 전체 테스트 스위트 내에서 호출되는 모든 프로세스를 가짜 처리했는지 확실히 하고 싶다면 `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드 호출 이후에는 대응하는 가짜 결과가 없는 프로세스 호출이 실제 프로세스 시작 대신 예외를 발생시킵니다:

```php
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