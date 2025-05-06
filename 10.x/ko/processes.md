# 프로세스

- [소개](#introduction)
- [프로세스 호출](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 명명](#naming-pool-processes)
    - [풀 프로세스 ID와 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 페이킹](#faking-processes)
    - [특정 프로세스 페이킹](#faking-specific-processes)
    - [프로세스 시퀀스 페이킹](#faking-process-sequences)
    - [비동기 프로세스 라이프사이클 페이킹](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어서션](#available-assertions)
    - [불필요한 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 감싸는 간결하고 표현력 있는 API를 제공합니다. 이를 통해 외부 프로세스를 Laravel 애플리케이션에서 쉽게 호출할 수 있습니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례에 집중되어 있으며, 개발자 경험을 극대화합니다.

<a name="invoking-processes"></a>
## 프로세스 호출

프로세스를 호출하려면 `Process` 파사드에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 실행하고 완료될 때까지 기다리지만, `start` 메서드는 비동기적으로 프로세스를 실행할 때 사용합니다. 본 문서에서는 두 가지 접근 방식을 모두 살펴봅니다. 먼저, 기본 동기 프로세스를 호출하고 그 결과를 확인하는 방법을 살펴보겠습니다:

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

프로세스 결과를 가지고 있고, 종료 코드가 0보다 큰 경우(즉, 실패를 의미)에 `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면, `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 프로세스 결과 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션

물론, 프로세스를 호출하기 전에 그 동작을 커스터마이즈할 필요가 있을 때도 있습니다. 다행히도 Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 속성을 조정할 수 있게 해줍니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용하여 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 사용하지 않으면, 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력

`input` 메서드를 사용하여 프로세스의 "표준 입력"에 입력값을 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. 하지만, `timeout` 메서드를 통해 이 동작을 커스터마이즈할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또한, 프로세스 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 사용할 수 있습니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무런 출력을 반환하지 않고 실행될 수 있는 최대 시간을(초 단위로) 지정할 때 사용합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

환경 변수는 `env` 메서드를 통해 프로세스에 전달할 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 상속합니다:

```php
$result = Process::forever()
            ->env(['IMPORT_PATH' => __DIR__])
            ->run('bash import.sh');
```

상속된 환경 변수를 제거하고 싶다면, 해당 환경 변수의 값을 `false`로 지정하면 됩니다:

```php
$result = Process::forever()
            ->env(['LOAD_PATH' => false])
            ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 사용하여 프로세스의 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력 및 출력을 프로그램의 입력/출력에 연결하므로, Vim·Nano와 같은 에디터를 프로세스로 실행할 때 유용합니다:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### 프로세스 출력

앞에서 설명했듯이, 프로세스 결과의 `output`(표준 출력, stdout)과 `errorOutput`(표준 에러, stderr) 메서드를 통해 프로세스 출력을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

또한, `run` 메서드의 두 번째 인자로 클로저를 전달하면 실시간으로 출력을 수집할 수도 있습니다. 이 클로저는 출력의 "타입"(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또한 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공하여, 프로세스 출력에 특정 문자열이 포함되어 있는지 쉽게 확인할 수 있게 합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 너무 많은 출력을 보내고 있는데, 해당 출력이 필요 없다면 출력을 완전히 비활성화하여 메모리 사용을 절약할 수 있습니다. 이를 위해 프로세스 작성 시 `quietly` 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 전달하고 싶을 수 있습니다. 보통 이를 "파이프"라고 부릅니다. `Process` 파사드에서 제공하는 `pipe` 메서드로 쉽게 구현할 수 있습니다. `pipe` 메서드는 모든 파이프라인 프로세스를 동기적으로 실행하며, 파이프라인에서 마지막 프로세스의 결과를 반환합니다:

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

파이프라인을 구성하는 개별 프로세스를 커스터마이즈할 필요가 없다면, 명령어 문자열의 배열을 `pipe` 메서드에 전달하면 됩니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

출력 역시 두 번째 인자로 클로저를 전달해 실시간으로 수집할 수 있습니다. 클로저는 "타입"(stdout 또는 stderr)과 출력 문자열을 받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

또한, `as` 메서드를 통해 각 파이프라인 프로세스에 문자 키를 지정할 수 있습니다. 이 키는 출력 클로저에도 전달되어, 어떤 프로세스의 출력인지를 구별할 수 있게 합니다:

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

`run` 메서드는 동기적으로 프로세스를 호출하지만, `start` 메서드를 사용하면 비동기적으로 프로세스를 호출할 수 있습니다. 이를 통해 애플리케이션이 프로세스가 백그라운드에서 실행되는 동안 다른 작업을 계속 수행할 수 있습니다. 프로세스가 호출되면 `running` 메서드를 사용하여 현재 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

위 코드처럼, `wait` 메서드를 호출하여 프로세스가 완료될 때까지 기다리고 프로세스 결과 인스턴스를 가져올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드를 사용하여 실행 중인 프로세스의 운영체제 할당 프로세스 ID를 가져올 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 사용하여 실행 중인 프로세스에 "시그널"을 보낼 수 있습니다. 미리 정의된 시그널 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, 전체 출력은 `output` 및 `errorOutput` 메서드를 통해 접근할 수 있습니다. 그러나, `latestOutput` 및 `latestErrorOutput`을 사용하면 마지막으로 출력을 가져온 이후부터의 새 출력을 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` 메서드처럼, `start` 메서드의 두 번째 인자로 클로저를 전달하면 비동기 프로세스의 출력을 실시간으로 수집할 수 있습니다. 클로저는 출력의 타입(`stdout` 또는 `stderr`)과 출력 문자열을 인수로 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

<a name="concurrent-processes"></a>
## 동시 프로세스

Laravel은 여러 개의 비동기 프로세스를 풀로 쉽게 관리할 수 있도록 해주어, 여러 작업을 동시에 간단하게 실행할 수 있게 합니다. 먼저, `Illuminate\Process\Pool` 인스턴스를 인수로 받는 클로저를 `pool` 메서드에 전달합니다.

이 클로저 내에서 풀에 포함할 프로세스들을 정의할 수 있습니다. 풀 프로세스를 `start` 메서드로 시작하면, `running` 메서드를 사용해 실행 중인 프로세스의 [컬렉션](/docs/{{version}}/collections)에 접근할 수 있습니다:

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

이처럼, `wait` 메서드를 사용해 풀 내 모든 프로세스가 완료될 때까지 기다리고 각 결과를 가져올 수 있습니다. `wait` 메서드는 배열 액세스가 가능한 객체를 반환하며, 해당 키로 각 풀 프로세스의 결과 인스턴스에 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

또는 편리하게, `concurrently` 메서드를 사용해 비동기 프로세스 풀을 시작하고 곧바로 결과를 기다릴 수도 있습니다. PHP 배열 비구조화와 함께 사용하면 더욱 표현력 있는 구문을 제공할 수 있습니다:

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

숫자 키로 풀 결과에 접근하는 것은 직관적이지 않을 수 있으므로, `as` 메서드를 사용해 각 풀 프로세스에 문자 키를 지정할 수 있습니다. 이 키는 `start` 메서드에 전달하는 클로저에도 제공되어, 어떤 프로세스 출력인지 구분할 수 있습니다:

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

풀의 `running` 메서드는 모든 실행된 프로세스 컬렉션을 제공하므로, 각 프로세스의 ID에 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 풀에 시그널을 보내고 싶다면 `signal` 메서드를 사용할 수 있습니다. 이 방법으로 풀 내 모든 프로세스에 동시에 시그널을 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트

많은 Laravel 서비스들은 쉽게 테스트를 작성할 수 있도록 해주며, 프로세스 서비스도 예외는 아닙니다. `Process` 파사드의 `fake` 메서드를 사용하면 프로세스가 호출될 때 모의(더미) 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이킹

Laravel의 프로세스 페이킹 기능을 확인하기 위해, 프로세스를 호출하는 라우트를 예시로 살펴봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출하면 모든 프로세스 호출에 대해 성공적인 더미 결과를 반환하도록 할 수 있습니다. 또한, 특정 프로세스가 "실행"되었는지 [어설트](#available-assertions)도 할 수 있습니다:

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

        // 단순 프로세스 어서션
        Process::assertRan('bash import.sh');

        // 또는 프로세스 설정값 검사
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

설명했듯이, `fake` 메서드를 호출하면 아무 출력도 없는, 항상 성공적인 프로세스 결과가 반환됩니다. 하지만 `Process` 파사드의 `result` 메서드를 통해 페이크 프로세스의 출력값과 종료 코드를 지정할 수도 있습니다:

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
### 특정 프로세스 페이킹

앞선 예시와 같이, `Process` 파사드는 프로세스마다 다른 페이크 결과를 가지도록 배열을 `fake` 메서드에 전달할 수 있습니다.

배열의 키는 페이킹하고 싶은 명령 패턴을, 값은 그에 해당하는 결과를 의미합니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 페이킹되지 않은 모든 프로세스 명령어는 실제로 실행됩니다. `Process` 파사드의 `result` 메서드를 이용해 더미 결과를 만들 수 있습니다:

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

페이크 프로세스의 종료 코드나 에러 출력을 커스터마이즈할 필요가 없다면, 간단히 문자열만 지정해도 됩니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이킹

테스트 코드가 동일한 명령으로 여러 프로세스를 호출한다면, 각 호출마다 다른 페이크 결과를 지정할 수 있습니다. 이를 위해 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
                ->push(Process::result('First invocation'))
                ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 라이프사이클 페이킹

지금까지는 주로 `run` 메서드를 이용해 동기적으로 호출되는 프로세스의 페이킹만 다뤘습니다. 하지만, `start`를 통해 비동기적으로 호출되는 프로세스와 상호작용하는 코드를 테스트하려면 더 정교한 페이킹이 필요할 수 있습니다.

예를 들어, 다음과 같이 비동기 프로세스와 상호작용하는 라우트가 있다고 가정해봅시다:

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

이 프로세스를 적절히 페이킹하려면, `running` 메서드가 몇 번 `true`를 반환해야 하는지 지정할 수 있어야 하며, 여러 줄의 출력도 순차적으로 반환하도록 지정할 수 있어야 합니다. 이를 위해 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다:

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

위 예시를 살펴보면, `output`과 `errorOutput` 메서드를 통해 반환할 여러 줄의 출력을 순차적으로 지정할 수 있습니다. `exitCode` 메서드는 페이크 프로세스의 최종 종료 코드를 지정합니다. 마지막으로, `iterations` 메서드는 `running` 메서드가 몇 번 `true`를 반환해야 하는지 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어서션

[앞에서 설명한 바](#faking-processes)와 같이, Laravel은 여러분의 기능 테스트를 위한 다양한 프로세스 어서션을 제공합니다. 아래에서 각 어서션에 대해 설명합니다.

<a name="assert-process-ran"></a>
#### assertRan

지정된 프로세스가 호출되었는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 받을 수 있으며, 프로세스 인스턴스와 프로세스 결과 인스턴스를 인수로 넘겨주어 프로세스의 설정값을 검사할 수 있습니다. 클로저가 `true`를 반환하면 어서션이 "성공"합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`assertRan` 클로저의 `$process`는 `Illuminate\Process\PendingProcess`의 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult`의 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

지정한 프로세스가 호출되지 않았는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 마찬가지로, `assertDidntRun` 메서드도 클로저를 받을 수 있습니다. 이 클로저는 프로세스 인스턴스와 결과를 전달받으며, 만약 `true`를 반환하면 어서션이 "실패"합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

지정한 프로세스가 지정된 횟수만큼 실행되었는지 어서트합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 메서드 역시 클로저를 받을 수 있습니다. 이 클로저가 `true`를 반환하고, 프로세스가 지정된 횟수만큼 실행됐다면 어서션이 "성공"합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 방지

테스트(개별 테스트 혹은 전체 테스트 스위트)에서 호출되는 모든 프로세스가 반드시 페이킹되었는지 보장하고 싶다면, `preventStrayProcesses` 메서드를 사용할 수 있습니다. 이 메서드를 호출하면, 대응되는 페이크 결과가 없는 프로세스는 실제로 실행되는 대신 예외를 발생시킵니다:

    use Illuminate\Support\Facades\Process;

    Process::preventStrayProcesses();

    Process::fake([
        'ls *' => 'Test output...',
    ]);

    // 페이크 결과가 반환됨
    Process::run('ls -la');

    // 예외가 발생함
    Process::run('bash import.sh');
