# 프로세스(Processes)

- [소개](#introduction)
- [프로세스 호출](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID 및 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 명명하기](#naming-pool-processes)
    - [풀 프로세스 ID 및 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 모킹하기](#faking-processes)
    - [특정 프로세스 모킹하기](#faking-specific-processes)
    - [프로세스 시퀀스 모킹하기](#faking-process-sequences)
    - [비동기 프로세스 라이프사이클 모킹하기](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어설션](#available-assertions)
    - [예상치 못한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 기반으로 하는 간결하고 직관적인 API를 제공하여, Laravel 애플리케이션에서 외부 프로세스를 간편하게 호출할 수 있도록 지원합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 뛰어난 개발 경험에 중점을 두고 있습니다.

<a name="invoking-processes"></a>
## 프로세스 호출

프로세스를 호출하려면 `Process` 파사드가 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출하고 해당 프로세스의 실행이 완료될 때까지 대기합니다. 반면, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 본 문서에서는 두 가지 접근 방법을 모두 살펴보겠습니다. 먼저, 기본적인 동기 프로세스를 호출하고 결과를 확인하는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에는 프로세스 결과를 다양한 방식으로 확인할 수 있는 여러 유용한 메서드가 포함되어 있습니다:

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

프로세스 결과가 있고, 종료 코드가 0보다 크면(`실패`임) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 만약 프로세스가 실패하지 않았다면 프로세스 결과 인스턴스가 그대로 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

프로세스를 호출하기 전에 다양한 동작을 커스터마이즈해야 할 수 있습니다. Laravel은 워킹 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 기능을 조정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 워킹 디렉터리 경로

`path` 메서드를 사용하여 프로세스의 워킹 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 현재 실행 중인 PHP 스크립트의 워킹 디렉터리를 상속받게 됩니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값 전달

`input` 메서드를 사용하여 프로세스의 표준 입력으로 데이터를 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외가 발생합니다. `timeout` 메서드를 통해 이 동작을 조정할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 사용하세요:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 일정 시간 이상 출력을 내지 않을 때의 최대 허용 초를 지정합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 통해 환경 변수를 프로세스에 전달할 수 있습니다. 호출되는 프로세스는 시스템에 정의된 모든 환경 변수도 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경 변수를 제거하고 싶으면 해당 변수 값을 `false`로 지정하세요:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드는 프로세스에 TTY 모드를 활성화할 때 사용합니다. TTY 모드는 프로그램의 입력/출력을 프로세스와 연결하므로, vim이나 nano 같은 에디터를 실행할 수 있습니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞서 살펴본 것처럼, 프로세스 결과의 `output`(표준 출력)과 `errorOutput`(표준 에러)을 통해 결과를 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드에 두 번째 인자로 클로저를 전달하면, 실시간으로 값을 받을 수도 있습니다. 이 클로저는 "출력 타입"(`stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또, 주어진 문자열이 프로세스 출력에 포함되어 있는지 쉽게 확인할 수 있도록 `seeInOutput` 및 `seeInErrorOutput` 메서드도 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

특정 프로세스가 많은 출력을 내보내지만, 해당 내용이 불필요하다면, 출력 수집을 완전히 비활성화해 메모리를 절약할 수 있습니다. 이를 위해 프로세스 빌드 시 `quietly` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 사용하고 싶을 때가 있습니다. 이를 "파이프(piping)"이라고도 하며, `Process` 파사드의 `pipe` 메서드를 사용하면 쉽게 구현할 수 있습니다. 이 메서드는 파이프라인 내의 모든 프로세스를 동기적으로 실행하고, 마지막 프로세스의 결과를 반환합니다:

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

파이프라인을 구성하는 개별 프로세스를 커스터마이즈하지 않아도 된다면, 명령어 문자열의 배열을 `pipe` 메서드에 바로 전달할 수 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

또한, 두 번째 인자로 클로저를 전달하여, 파이프라인 출력도 실시간으로 수집할 수 있습니다. (출력 타입과 출력 문자열을 제공합니다):

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

파이프라인 내 각 프로세스에 대해 `as` 메서드로 문자열 키를 부여할 수도 있습니다. 이 키는 파이프 출력 클로저에도 함께 전달되며, 어떤 프로세스의 출력인지 구분할 수 있습니다:

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

`run` 메서드는 프로세스를 동기적으로 호출하지만, `start` 메서드는 프로세스를 비동기적으로 실행합니다. 이로써 애플리케이션은 프로세스가 백그라운드에서 실행되는 동안 다른 작업을 계속 수행할 수 있습니다. 프로세스를 시작한 후에는 `running` 메서드를 통해 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

보셨다시피, `wait` 메서드를 호출해 프로세스 종료까지 대기하며, 결과 인스턴스를 얻을 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 시그널

`id` 메서드를 통해 운영체제가 할당한 실행중인 프로세스 ID를 알 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 사용 가능한 시그널 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)를 참고하세요:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때는, `output` 및 `errorOutput` 메서드로 전체 출력을 확인할 수 있습니다. 혹은 `latestOutput`과 `latestErrorOutput` 메서드로 마지막으로 읽은 이후 새로 발생한 출력만 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드처럼, `start` 메서드의 두 번째 인자로 클로저를 전달하면 비동기 프로세스의 실시간 출력을 수집할 수 있습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 끝날 때까지 무조건 기다리는 대신, `waitUntil` 메서드를 사용하여 특정 출력이 나오면 대기를 중지할 수 있습니다. 클로저가 `true`를 반환하면 프로세스가 종료되지 않아도 대기를 멈춥니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스가 실행 중일 때, `ensureNotTimedOut` 메서드로 타임아웃 여부를 체크할 수 있습니다. 이 메서드는 프로세스가 타임아웃 된 경우 [타임아웃 예외](#timeouts)를 발생시킵니다:

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

Laravel은 여러 개의 비동기 프로세스를 풀(pool)로 쉽게 관리할 수 있도록 도와줍니다. 이를 통해 여러 작업을 동시에 실행할 수 있습니다. 시작하려면, `Illuminate\Process\Pool` 인스턴스를 제공받는 클로저를 `pool` 메서드에 넘겨주면 됩니다.

이 클로저에서 풀에 속하는 프로세스를 정의할 수 있습니다. 풀을 `start` 메서드로 시작하면, [컬렉션](/docs/{{version}}/collections) 형태로 실행 중인 프로세스들의 목록을 `running` 메서드로 얻을 수 있습니다:

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

위 예제와 같이, 모든 풀 프로세스의 실행이 완료되기를 기다렸다가, `wait` 메서드로 결과를 한 번에 해결할 수 있습니다. `wait` 메서드에서는 풀 내 각 프로세스의 키로 해당 결과 인스턴스에 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

좀 더 간결하게, `concurrently` 메서드를 사용하면 비동기 풀을 즉시 시작하고, 결과를 바로 기다릴 수 있습니다. PHP의 배열 구조 분해와 조합하면 더욱 직관적인 문법을 제공합니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 명명하기

숫자 키로 풀 프로세스 결과에 접근하는 것은 가독성이 떨어질 수 있습니다. 그래서 `as` 메서드를 사용해 각각의 풀 프로세스에 문자열 키를 부여할 수 있습니다. 이 키는 `start` 메서드에 제공된 클로저에도 전달되어, 출력 주체를 식별할 수 있습니다:

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

풀의 `running` 메서드는 모든 실행 중인 프로세스 컬렉션을 반환하므로, 각 프로세스별로 직접 ID에 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 풀의 모든 프로세스에 시그널을 동시에 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

여러 Laravel 서비스는 테스트 작성을 쉽게 할 수 있는 기능을 제공합니다. 프로세스 서비스 역시 예외가 아닙니다. `Process` 파사드의 `fake` 메서드를 이용하면, 프로세스 호출 시 더미(모킹) 결과를 반환하도록 지정할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 모킹하기

예를 들어, 프로세스를 호출하는 라우트가 있다고 가정해보겠습니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드에 인자 없이 호출하면 모든 프로세스 호출에 대해 가짜 성공 결과를 반환하도록 Laravel에 지시할 수 있습니다. 또한, 특정 프로세스가 "실행되었는지" [어설션](#available-assertions)까지 할 수 있습니다:

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

    // 또는, 프로세스 설정값 검사...
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

        // 또는, 프로세스 설정값 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

언급한 것처럼, `Process` 파사드에서 `fake` 메서드를 호출하면 기본적으로 출력 없는 성공 결과가 항상 반환됩니다. 하지만, `Process` 파사드의 `result` 메서드를 이용해 모킹되는 프로세스의 출력값과 종료 코드를 지정할 수도 있습니다:

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
### 특정 프로세스 모킹하기

앞선 예제에서처럼, 명령어별로 서로 다른 모킹 결과를 지정할 수 있습니다. `Process` 파사드의 `fake` 메서드에 배열을 전달하면 됩니다.

배열의 키는 모킹할 명령 패턴이며, 값은 해당 결과입니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 모킹되지 않은 명령어는 실제 프로세스가 실행됩니다. 각 명령어에 대한 더미 결과는 `Process` 파사드의 `result` 메서드로 지정할 수 있습니다:

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

종료 코드나 에러 출력 결과를 커스터마이즈하지 않아도 된다면, 문자열로 간단히 지정할 수 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 모킹하기

같은 명령어로 여러 프로세스를 호출하는 코드를 테스트할 때, 각 호출마다 다른 결과를 부여하고 싶다면 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 라이프사이클 모킹하기

지금까지는 주로 `run` 메서드를 통한 동기 프로세스 모킹을 다뤘습니다. 하지만 `start`를 통해 비동기 프로세스와 상호작용하는 코드를 테스트해야 한다면, 좀 더 정교하게 가짜 프로세스를 정의해야 할 수 있습니다.

예를 들어, 아래와 같이 비동기 프로세스를 다루는 라우트가 있다고 가정해보겠습니다:

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

이 프로세스를 제대로 모킹하려면, `running` 메서드가 몇 번 `true`를 반환해야 하는지 지정할 수 있어야 하며, 각 단계별로 여러 줄의 출력값도 순차적으로 지정할 수 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예제에서 `output`과 `errorOutput` 메서드로 여러 줄의 출력 내용을 순서대로 지정할 수 있습니다. 마지막 종료 코드는 `exitCode` 메서드로, `running` 메서드가 true를 반환할 횟수는 `iterations` 메서드로 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어설션

[앞서 설명한](#faking-processes) 것처럼, Laravel은 여러가지 프로세스 테스트 어설션을 제공합니다. 아래에서 하나씩 살펴보겠습니다.

<a name="assert-process-ran"></a>
#### assertRan

지정한 프로세스가 호출되었는지 어설션합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 받을 수 있으며, 프로세스 인스턴스와 결과 인스턴스를 넘겨줍니다. 클로저가 true를 반환하면 어설션이 통과합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`$process`는 `Illuminate\Process\PendingProcess` 인스턴스, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

지정한 프로세스가 호출되지 않았는지 어설션합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertDidntRun`에도 클로저를 넘겨받아, 조건이 true면 어설션이 실패합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

지정한 프로세스가 요청한 횟수만큼 호출되었는지 어설션합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

여기에도 클로저를 넘겨 같은 방식으로 프로세스 설정을 검사할 수 있습니다. 클로저가 true를 반환하고, 지정된 횟수만큼 호출되면 어설션이 통과합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 예상치 못한 프로세스 방지

테스트나 전체 테스트 스위트에서 모든 프로세스 호출이 반드시 모킹되었는지 보장하고 싶다면 `preventStrayProcesses` 메서드를 사용할 수 있습니다. 이 메서드를 호출하면, 모킹 결과가 없는 프로세스는 실제로 실행되지 않고 예외가 발생합니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 모킹 결과가 반환됨
Process::run('ls -la');

// 예외 발생
Process::run('bash import.sh');
```
