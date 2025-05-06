# 프로세스

- [소개](#introduction)
- [프로세스 실행](#invoking-processes)
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
    - [프로세스 페이크](#faking-processes)
    - [특정 프로세스 페이크](#faking-specific-processes)
    - [프로세스 시퀀스 페이크](#faking-process-sequences)
    - [비동기 프로세스 라이프사이클 페이크](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [불필요한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/7.0/components/process.html)를 기반으로 한 간결하고 표현력 있는 API를 제공합니다. 이를 통해 Laravel 애플리케이션에서 외부 프로세스를 쉽게 실행할 수 있습니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례와 개발자 경험에 중점을 두어 설계되었습니다.

<a name="invoking-processes"></a>
## 프로세스 실행

프로세스를 실행하려면 `Process` 파사드의 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 완료될 때까지 대기하며, `start` 메서드는 비동기 방식으로 프로세스를 실행합니다. 이 문서에서는 두 가지 접근 방식을 살펴봅니다. 먼저, 기본 동기 프로세스를 실행하고 결과를 확인하는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에서는 프로세스 결과를 확인할 때 유용한 다양한 메서드를 사용할 수 있습니다:

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

프로세스 결과를 가지고 있고, 종료 코드가 0보다 큰(즉, 실패를 나타내는) 경우 `Illuminate\Process\Exceptions\ProcessFailedException`을 발생시키고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면, 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

물론, 프로세스를 실행하기 전에 동작을 맞춤화해야 할 수도 있습니다. Laravel은 작업 디렉토리, 타임아웃, 환경변수 등 다양한 프로세스 기능을 조정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 작업 디렉토리 경로

`path` 메서드를 사용하여 프로세스의 작업 디렉토리를 지정할 수 있습니다. 이 메서드를 사용하지 않으면 현재 실행 중인 PHP 스크립트의 작업 디렉토리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 사용하여 "표준 입력"을 통해 프로세스에 입력을 제공할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 60초 이상 실행되는 프로세스는 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 하지만 `timeout` 메서드를 사용하여 이 동작을 변경할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또는 프로세스 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 사용하면 됩니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무 출력도 반환하지 않은 채로 실행될 수 있는 최대 초를 지정합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경변수

`env` 메서드를 통해 프로세스에 환경변수를 제공할 수 있습니다. 또한 실행된 프로세스는 시스템에 정의된 모든 환경변수도 상속하게 됩니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경변수를 삭제하려면 해당 환경변수에 `false` 값을 지정하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 사용하면 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력 및 출력에 연결하여, Vim이나 Nano와 같은 편집기를 프로세스로 열 수 있습니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

이전에 설명한 것처럼, 프로세스 결과의 `output`(표준 출력) 및 `errorOutput`(표준 에러) 메서드를 사용하여 프로세스 출력을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, 출력값을 실시간으로 수집하려면 `run` 메서드의 두 번째 인자로 클로저를 전달하면 됩니다. 클로저는 두 개의 인자를 받습니다: 출력의 "타입"(`stdout` 또는 `stderr`)과 실제 출력 문자열입니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 프로세스의 출력에 특정 문자열이 포함되어 있는지 쉽게 확인할 수 있도록 `seeInOutput` 및 `seeInErrorOutput` 메서드도 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

관심 없는 많은 양의 출력이 생성되는 경우, 출력을 아예 비활성화하여 메모리를 절약할 수 있습니다. 이를 위해 프로세스 생성 시 `quietly` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 사용하는 "파이프" 작업이 필요할 수 있습니다. `Process` 파사드의 `pipe` 메서드를 이용하면 파이프라인 구성이 간단합니다. `pipe` 메서드는 모든 파이프 프로세스를 동기적으로 실행하고, 파이프라인에서 마지막 프로세스의 결과를 반환합니다:

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

파이프라인을 구성하는 각 프로세스를 커스터마이즈할 필요가 없다면, 명령어 문자열 배열만 전달해도 됩니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

클로저를 두 번째 인자로 전달하여, 파이프라인의 출력을 실시간으로 수집할 수 있습니다. 클로저는 "타입"(`stdout` 또는 `stderr`)과 출력 문자열을 인자로 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel에서는 `as` 메서드를 통해 파이프라인 내의 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키는 `pipe` 메서드에 전달한 출력 클로저에도 전달되어, 어떤 프로세스의 출력인지 구분할 수 있습니다:

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

`run` 메서드는 프로세스를 동기적으로 실행하지만, `start` 메서드는 프로세스를 비동기적으로 실행할 수 있습니다. 즉, 프로세스가 백그라운드에서 실행되는 동안 애플리케이션이 계속 다른 작업을 수행할 수 있습니다. 프로세스를 실행한 후에는 `running` 메서드를 사용하여 해당 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

위 예시처럼, 프로세스가 완료될 때까지 기다리고 결과 인스턴스를 얻으려면 `wait` 메서드를 사용할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드를 사용하면 운영체제에서 할당한 실행 중인 프로세스의 ID를 가져올 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 이용해 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 미리 정의된 시그널 상수 목록은 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, `output` 및 `errorOutput` 메서드를 사용해 현재까지의 전체 출력을 얻을 수 있습니다. 혹은 `latestOutput`, `latestErrorOutput`을 사용하면 직전 조회 이후의 새로운 출력만 가져올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

동기 방식의 `run` 메서드와 마찬가지로, 비동기 프로세스에서도 `start` 메서드의 두 번째 인자로 클로저를 전달하여 실시간으로 출력을 수집할 수 있습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 종료될 때까지 기다리는 대신, 출력값을 기반으로 대기를 중단하고 싶다면 `waitUntil` 메서드를 사용할 수 있습니다. 클로저가 `true`를 반환하면 대기를 중단합니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="concurrent-processes"></a>
## 동시 프로세스

Laravel은 동시(Concurrent) 비동기 프로세스 풀의 관리를 매우 쉽게 만들어 줍니다. 즉, 여러 작업을 동시에 손쉽게 실행할 수 있습니다. 시작하려면, `Illuminate\Process\Pool` 인스턴스를 받는 클로저를 인자로 하여 `pool` 메서드를 호출합니다.

이 클로저 내에서 풀에 속하는 각 프로세스를 정의할 수 있습니다. `start` 메서드를 호출하여 풀을 실행한 후, `running` 메서드로 현재 실행 중인 프로세스 컬렉션을 가져올 수 있습니다:

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

위에서 볼 수 있듯이, 모든 풀 프로세스의 실행이 끝날 때까지 `wait` 메서드를 통해 대기하고 각 프로세스의 결과를 확인할 수 있습니다. `wait` 메서드는 array-access(배열처럼 접근할 수 있는) 객체를 반환하고, 각 프로세스 결과 인스턴스를 키로 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

좀 더 편리하게, `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 실행하고, 바로 결과를 대기할 수 있습니다. 이때 PHP의 배열 구조 분해 문법과 결합하면 더욱 표현력이 좋아집니다:

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

숫자 키로 풀 프로세스 결과를 접근하는 것은 직관적이지 않을 수 있으므로, Laravel에서는 풀 내 각 프로세스에 문자열 키를 `as` 메서드로 지정할 수 있습니다. 해당 키는 `start` 메서드에 전달한 클로저에도 전달되어 출력이 어떤 프로세스에서 온 것인지 구분할 수 있습니다:

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

풀의 `running` 메서드는 풀 내의 모든 실행된 프로세스 컬렉션을 제공하므로, 해당 프로세스들의 ID에 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한 `signal` 메서드를 풀에 직접 호출해서, 풀 내의 모든 프로세스에 시그널을 동시에 보낼 수도 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

여러 Laravel 서비스는 테스트 작성이 쉽고 표현력 있도록 다양한 기능을 제공합니다. 프로세스 서비스도 예외가 아닙니다. `Process` 파사드의 `fake` 메서드를 이용해, 프로세스 실행 시 더미/스텁 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이크

Laravel의 프로세스 페이크 기능을 살펴보기 위해, 프로세스를 호출하는 라우트를 가정해 보겠습니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드(인자 없이 호출)를 사용하여 모든 프로세스 실행에 대해 성공적인 더미 결과를 반환하도록 Laravel에 지시할 수 있습니다. 또한, 특정 프로세스가 실행되었는지 [assert](#available-assertions)로 검증할 수도 있습니다:

```php tab=Pest
<?php

use Illuminate\Process\PendingProcess;
use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 단순 프로세스 어서션...
    Process::assertRan('bash import.sh');

    // 혹은 프로세스 설정을 검사...
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

        // 단순 프로세스 어서션...
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

설명한 바와 같이, `Process` 파사드의 `fake` 메서드를 호출하면 언제나 출력이 없는 성공적인 프로세스 결과가 반환됩니다. 하지만, `Process` 파사드의 `result` 메서드를 이용해 페이크 프로세스의 출력 값과 종료 코드를 직접 지정할 수도 있습니다:

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

이전 예시에서 보았듯이, `Process` 파사드는 `fake` 메서드에 배열을 전달하여 프로세스별로 다른 더미 반환값을 정의할 수 있습니다.

배열의 키는 페이크할 커맨드 패턴을 나타내며, 값은 해당 결과입니다. `*` 문자를 와일드카드로 사용 가능합니다. 페이크가 지정되지 않은 커맨드는 실제로 실행됩니다. `Process`의 `result` 메서드로 해당 명령어의 스텁/페이크 결과를 만들 수 있습니다:

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

페이크 프로세스의 종료 코드나 에러 출력이 필요 없이 단순 문자열만 지정해도 됩니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크

테스트 대상 코드가 동일 커맨드로 여러 프로세스를 호출한다면, 각 호출마다 다른 페이크 결과를 지정하고 싶을 수 있습니다. 이때 `Process` 파사드의 `sequence` 메서드를 이용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 라이프사이클 페이크

지금까지 논의한 페이크 기능은 주로 `run` 메서드를 사용하는 동기 프로세스에 대한 것이었습니다. 하지만 `start`로 실행되는 비동기 프로세스를 테스트하려면 조금 더 복잡한 페이크 설정이 필요합니다.

예를 들어, 아래와 같이 비동기 프로세스와 상호작용하는 라우트를 가정해봅시다:

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

이 프로세스를 적절히 페이크하기 위해서는, `running` 메서드가 몇 번 `true`를 반환해야 하는지 설정할 수 있어야 합니다. 또한 여러 줄의 출력이 순서대로 반환되도록 설정하고 싶을 수 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예시를 살펴보면, `output`과 `errorOutput` 메서드를 이용해 여러 줄 출력을 순차적으로 지정하고, `exitCode`로 최종 종료 코드를, `iterations`로 `running`이 `true`를 반환할 횟수를 설정할 수 있습니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션

[이미 설명한 것처럼](#faking-processes), Laravel은 기능 테스트를 위한 여러 프로세스 어서션을 제공합니다. 아래에서 각각을 살펴봅니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 호출되었는지 검증합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저를 받을 수 있으며, `process` 인스턴스와 결과를 받아 설정값을 검사할 수 있습니다. 클로저가 `true`를 반환하면 어서션이 통과합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`assertRan`에 전달되는 `$process`는 `Illuminate\Process\PendingProcess` 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult`입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 호출되지 않았는지 검증합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 마찬가지로, 클로저를 전달할 수 있고, 클로저가 `true`를 반환하면 어서션이 실패합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정된 횟수만큼 호출되었는지 검증합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 메서드는 클로저도 받을 수 있으며, 지정한 횟수만큼 실행되고 조건이 맞으면 어서션이 통과합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 방지

테스트 전체 혹은 개별 테스트에서 호출된 모든 프로세스가 반드시 페이크로 처리되었는지 강제하고 싶다면, `preventStrayProcesses` 메서드를 사용할 수 있습니다. 이 메서드를 호출하면, 페이크 결과가 없는 프로세스는 실제 실행되지 않고 예외가 발생합니다:

    use Illuminate\Support\Facades\Process;

    Process::preventStrayProcesses();

    Process::fake([
        'ls *' => 'Test output...',
    ]);

    // 페이크 응답이 반환됨...
    Process::run('ls -la');

    // 예외가 발생함...
    Process::run('bash import.sh');
