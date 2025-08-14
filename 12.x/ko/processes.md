# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 실행](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 네이밍](#naming-pool-processes)
    - [풀 프로세스 ID와 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 페이크](#faking-processes)
    - [특정 프로세스 페이크](#faking-specific-processes)
    - [프로세스 시퀀스 페이크](#faking-process-sequences)
    - [비동기 프로세스 라이프사이클 페이크](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [의도치 않은 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 기반으로 한 표현력 있고 최소한의 API를 제공하여, Laravel 애플리케이션에서 외부 프로세스를 손쉽게 실행할 수 있도록 지원합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례에 집중되어 있으며, 뛰어난 개발자 경험을 제공합니다.

<a name="invoking-processes"></a>
## 프로세스 실행

프로세스를 실행하려면 `Process` 파사드에서 제공하는 `run`과 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 해당 프로세스가 완전히 끝날 때까지 기다립니다. 반면, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 두 방식 모두 이 문서에서 다루며, 먼저 기본적인 동기 프로세스를 실행하고 그 결과를 확인하는 방법부터 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 확인할 수 있는 다양한 유용한 메서드를 제공합니다.

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

프로세스 결과가 있고, 만약 종료 코드가 0보다 크면(즉, 실패인 경우) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶다면, `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 그대로 `ProcessResult` 인스턴스를 반환합니다.

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

실행 전에 프로세스의 동작을 원하는 대로 커스터마이즈해야 할 때가 있습니다. 다행히 Laravel은 작업 디렉토리, 타임아웃, 환경 변수 등 다양한 프로세스 성질을 쉽게 조정할 수 있도록 해줍니다.

<a name="working-directory-path"></a>
#### 작업 디렉토리 경로

`path` 메서드를 사용하여 프로세스의 작업 디렉토리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면, 현재 실행 중인 PHP 스크립트의 작업 디렉토리를 상속합니다.

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 이용해 프로세스의 "표준 입력"으로 데이터를 전달할 수 있습니다.

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. 하지만 `timeout` 메서드로 이 동작을 원하는 값으로 조정할 수 있습니다.

```php
$result = Process::timeout(120)->run('bash import.sh');
```

프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 호출하세요.

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드를 사용하면, 출력이 없는 상태로 프로세스가 최대 몇 초 동안 실행될 수 있는지 지정할 수 있습니다.

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

환경 변수는 `env` 메서드를 통해 프로세스에 전달할 수 있습니다. 실행되는 프로세스는 시스템에 정의되어 있는 모든 환경 변수도 상속합니다.

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경 변수 중에서 특정 환경 변수를 제거하고 싶다면, 해당 환경 변수 값을 `false`로 넘겨주면 됩니다.

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 사용하면 프로세스에 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력/출력과 연결하여 Vim이나 Nano와 같은 에디터를 프로세스로 실행할 수 있게 합니다.

```php
Process::forever()->tty()->run('vim');
```

> [!WARNING]
> TTY 모드는 Windows 환경에서는 지원되지 않습니다.

<a name="process-output"></a>
### 프로세스 출력

앞서 설명한 것처럼, 프로세스 결과에서는 `output`(stdout) 및 `errorOutput`(stderr) 메서드를 사용해 프로세스 출력을 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드의 두 번째 인수로 클로저를 전달하여 실시간으로 출력을 수집할 수도 있습니다. 이 클로저는 "출력 타입"(`stdout` 또는 `stderr`)과 실제 출력 문자열을 전달받습니다.

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel에서는 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공하여, 프로세스 출력에 특정 문자열이 포함되어 있는지 쉽게 확인할 수 있도록 도와줍니다.

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 출력하는 데이터가 많아서 굳이 그 결과를 확인하지 않아도 된다면, 출력을 아예 가져오지 않음으로써 메모리를 절약할 수 있습니다. 이를 위해 프로세스 빌드 단계에서 `quietly` 메서드를 호출하세요.

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 사용하고 싶을 때가 있습니다. 이를 "파이핑"이라고 하며, `Process` 파사드의 `pipe` 메서드로 쉽게 구현할 수 있습니다. `pipe` 메서드는 파이프로 연결한 프로세스들을 동기적으로 실행하고, 파이프라인 내에서 마지막 프로세스의 결과를 반환합니다.

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

파이프라인을 구성하는 개별 프로세스를 별도로 커스터마이즈할 필요가 없는 경우, 커맨드 문자열의 배열을 `pipe` 메서드에 바로 전달해도 됩니다.

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

실행 중인 파이프라인의 출력도, `pipe` 메서드의 두 번째 인수로 클로저를 전달하여 실시간으로 수집할 수 있습니다. 이 클로저는 "출력 타입"(`stdout` 또는 `stderr`)과 실제 출력 문자열을 전달받습니다.

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

파이프라인 내 각 프로세스에 `as` 메서드를 사용해 문자열 키를 지정할 수도 있습니다. 이 키는 출력 클로저에도 전달되어, 어떤 프로세스가 해당 출력을 생성했는지 구분할 수 있도록 해줍니다.

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 비동기 프로세스

`run` 메서드는 프로세스를 동기적으로 실행하지만, `start` 메서드를 사용하면 비동기적으로 프로세스를 실행할 수 있습니다. 이를 활용하면 프로세스가 백그라운드에서 실행되는 동안 애플리케이션이 다른 작업을 계속 수행할 수 있습니다. 프로세스 실행 후에는 `running` 메서드를 이용해 프로세스가 아직 실행 중인지 확인할 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

이처럼 `wait` 메서드를 호출하여, 프로세스가 완료될 때까지 기다리고 `ProcessResult` 인스턴스를 받을 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드를 활용하면, 현재 실행 중인 프로세스의 운영 체제 할당 프로세스 ID를 얻을 수 있습니다.

```php
$process = Process::start('bash import.sh');

return $process->id();
```

실행 중인 프로세스에 '시그널'을 보내려면 `signal` 메서드를 사용하세요. 사전에 정의된 시그널 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다.

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, `output`와 `errorOutput` 메서드로 현재까지의 전체 출력을 확인할 수 있습니다. 또한, `latestOutput`와 `latestErrorOutput` 메서드를 사용해, 마지막으로 출력을 확인한 이후로 추가된 출력만을 가져올 수도 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드와 마찬가지로, 비동기 프로세스 실행 시에도 `start` 메서드의 두 번째 인수로 클로저를 전달하면 실시간으로 출력을 수집할 수 있습니다. 이 클로저는 "출력 타입"(`stdout` 또는 `stderr`)과 출력 문자열을 전달받습니다.

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스 종료까지 기다리는 대신, 출력 조건에 따라 대기 중단을 원할 경우 `waitUntil` 메서드를 사용할 수 있습니다. 이 메서드에 전달된 클로저가 `true`를 반환하면 Laravel은 대기를 즉시 중단합니다.

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스가 실행 중일 때, `ensureNotTimedOut` 메서드를 호출하여 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 이 메서드는 [타임아웃 예외](#timeouts)를 던집니다.

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

Laravel은 여러 비동기 프로세스를 동시에 풀(pool)로 관리하는 것도 아주 간단하게 해줍니다. 이를 통해 여러 작업을 동시에 손쉽게 실행할 수 있습니다. 먼저, `Illuminate\Process\Pool` 인스턴스를 클로저로 전달받는 `pool` 메서드를 실행해 시작합니다.

이 클로저 안에서 풀에 포함할 프로세스를 정의할 수 있습니다. 풀을 `start` 메서드로 시작하면, `running` 메서드를 통해 현재 실행 중인 모든 프로세스의 [컬렉션](/docs/12.x/collections)을 얻을 수 있습니다.

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

이처럼, 모든 풀 프로세스가 실행을 마치고 결과를 받아 올 때는 `wait` 메서드를 사용합니다. `wait`는 배열처럼 접근 가능한 객체를 반환하며, 각 키로 풀 내 프로세스의 `ProcessResult` 인스턴스를 확인할 수 있습니다.

```php
$results = $pool->wait();

echo $results[0]->output();
```

좀 더 간단한 구문이 필요한 경우, `concurrently` 메서드를 사용해 비동기 프로세스 풀을 바로 시작하고 바로 결과를 기다릴 수도 있습니다. PHP의 배열 구조 분해와 결합하면 문법이 더욱 간결해집니다.

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 네이밍

숫자 키로 프로세스 풀 결과에 접근하는 것은 명확하지 않을 수 있습니다. Laravel에서는 각 풀 프로세스에 문자열 키를 `as` 메서드로 지정할 수 있습니다. 이 키는 `start` 메서드에 전달된 클로저에도 전달되어, 어떤 프로세스의 출력인지 구분이 가능합니다.

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

풀의 `running` 메서드는 현재 실행 중인 모든 프로세스의 컬렉션을 반환하므로, 여기에서 각 프로세스의 ID에 쉽게 접근할 수 있습니다.

```php
$processIds = $pool->running()->each->id();
```

또한, 풀 전체에 대해 `signal` 메서드를 호출하면 풀 내 모든 프로세스에 동일한 시그널을 보낼 수 있습니다.

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

다양한 Laravel 서비스가 손쉽고 표현력 있게 테스트를 작성할 수 있도록 지원하듯, 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드를 통해, 프로세스 실행 시 더미 결과(스텁)를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이크

Laravel의 프로세스 페이크 기능을 살펴보기 위해, 프로세스를 실행하는 다음의 라우트 예시를 가정해보겠습니다.

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출하면, 모든 실행된 프로세스에 대해 항상 성공한 가짜 결과를 반환하게 할 수 있습니다. 추가로, 해당 프로세스가 실제로 실행됐는지 [어설트](#available-assertions)할 수도 있습니다.

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 단순 프로세스 어설션...
    Process::assertRan('bash import.sh');

    // 또는 프로세스 설정 값을 확인...
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

        // 단순 프로세스 어설션...
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정 값을 확인...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

위 예시처럼 `fake` 메서드를 호출하면, 항상 성공한(출력 없는) 프로세스 결과를 반환합니다. 하지만, `Process` 파사드의 `result` 메서드를 활용해 출력값과 종료 코드를 원하는 대로 지정할 수도 있습니다.

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

위에서 살펴본 것처럼, `fake` 메서드에 배열을 전달하면 각 프로세스별로 다른 가짜 결과를 지정할 수 있습니다.

배열의 키에는 페이크할 커맨드 패턴을, 값에는 그 결과를 지정합니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 페이크하지 않은 명령은 실제로 실행됩니다. `Process` 파사드의 `result` 메서드를 활용해 페이크 결과를 생성할 수 있습니다.

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

종료 코드나 에러 출력을 커스터마이즈할 필요가 없다면, 간단히 문자열로 결과를 지정하는 것이 편리할 수 있습니다.

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크

테스트 대상 코드가 동일한 명령을 여러 번 실행한다면, 각 실행에 대해 각각 다른 가짜 결과를 반환해야 할 수 있습니다. 이때는 `Process` 파사드의 `sequence` 메서드를 활용하세요.

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 라이프사이클 페이크

여기까지는 `run` 메서드로 동기 실행된 프로세스 페이크 중심으로 설명했습니다. 하지만 비동기적으로 `start`로 실행되는 프로세스와 상호작용하는 코드를 테스트하려면, 페이크 프로세스를 좀 더 세밀하게 묘사할 필요가 있습니다.

예를 들어, 아래와 같이 비동기 프로세스와 상호작용하는 라우트가 있다고 해보겠습니다.

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

이 프로세스를 제대로 페이크하려면, `running` 메서드가 몇 번 `true`를 반환해야 할지 지정할 수 있어야 하며, 여러 줄의 출력을 순차적으로 리턴해 주기를 원할 수 있습니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다.

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

이 예시를 살펴보면, `output`과 `errorOutput` 메서드로 여러 줄의 출력을 순서대로 지정할 수 있습니다. 또한, `exitCode` 메서드로 마지막 종료 코드를, `iterations` 메서드로 `running`이 몇 번 `true`를 반환할지 지정할 수 있습니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션

[앞에서 설명한 것처럼](#faking-processes), Laravel은 기능 테스트에서 사용할 수 있는 여러 프로세스 어서션 메서드를 제공합니다. 아래에서 각각의 어서션을 살펴봅니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 실행되었는지 어설트합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 받을 수 있습니다. 클로저에는 프로세스 인스턴스와 프로세스 결과가 전달되어 프로세스의 설정 옵션을 확인할 수 있습니다. 클로저가 `true`를 반환하면 어설션은 '성공'으로 처리됩니다.

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

여기서 `$process` 파라미터는 `Illuminate\Process\PendingProcess`의 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult`의 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 실행되지 않았는지 어설트합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`처럼, `assertDidntRun`에도 클로저를 전달해 프로세스 설정값을 확인할 수 있습니다. 클로저가 `true`를 반환하면 어설션은 '실패'로 간주합니다.

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정한 횟수만큼 실행되었는지 어설트합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 또한 클로저를 받을 수 있습니다. 클로저가 `true`를 반환하고, 프로세스가 지정 횟수만큼 실행되면 어설션은 '성공'입니다.

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 의도치 않은 프로세스 방지

테스트 코드 또는 전체 테스트 스위트에서 모든 프로세스가 반드시 페이크 되도록 강제하려면, `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드 호출 이후에는, 페이크 결과가 준비되지 않은 프로세스가 실행될 경우 실제로 실행하지 않고 예외를 던집니다.

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 페이크 결과가 반환됨...
Process::run('ls -la');

// 예외 발생!
Process::run('bash import.sh');
```
