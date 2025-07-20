# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [단일 실행 보장 명령어(Isolatable Commands)](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력값 프롬프트](#prompting-for-missing-input)
- [명령어 I/O](#command-io)
    - [입력값 조회](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그램적으로 명령어 실행](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 파일 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 기본 포함되어 있는 명령줄 인터페이스(CLI)입니다. Artisan은 애플리케이션의 루트에 위치한 `artisan` 스크립트로 제공되며, 애플리케이션을 개발하는 동안 도움이 되는 다양한 명령어를 제공합니다. 모든 사용 가능한 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

각 명령어에는 해당 명령어가 사용할 수 있는 인수와 옵션을 보여주는 "help" 화면이 있습니다. help 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/12.x/sail)을 사용하는 경우, Artisan 명령어를 실행할 때는 `sail` 명령줄을 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내부에서 Artisan 명령어를 실행합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크용 강력한 REPL이며, [PsySH](https://github.com/bobthecow/psysh) 패키지로 동작합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 애플리케이션에서 Tinker를 제거했다면, Composer를 이용해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션에 대한 상시 코드 재시작(핫 리로딩), 여러 줄 코드 편집, 자동 완성 등 상호작용성을 원하신다면 [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 이용하면 Eloquent 모델, 작업(Job), 이벤트 등 전체 Laravel 애플리케이션과 명령줄에서 직접 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요.

```shell
php artisan tinker
```

Tinker의 설정 파일을 `vendor:publish` 명령어로 배포할 수도 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣을 때 가비지 컬렉션에 의존합니다. 따라서 tinker에서 작업을 큐로 보내려면 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록(Command Allow List)

Tinker는 내부적으로 "허용(Allow)" 목록을 사용하여, 어떤 Artisan 명령어가 shell 내에서 실행 가능한지 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 별칭이 지정되지 않아야 하는 클래스

Tinker는 일반적으로 상호작용하는 클래스에 대해 자동으로 별칭을 지정합니다. 하지만 일부 클래스는 별칭을 지정하지 않도록 설정할 수 있습니다. 이를 위해 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan이 기본 제공하는 명령어 외에도, 여러분만의 커스텀 명령어를 직접 만들 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉토리에 저장되지만, 필요하다면 [Artisan 명령어를 위한 다른 디렉토리 검색](#registering-commands)도 설정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새로운 명령어를 만들려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉토리에 새 명령어 클래스를 생성합니다. 해당 디렉토리가 아직 없다면, 최초 실행 시 자동으로 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 뒤에는, 클래스의 `signature` 및 `description` 속성(property)에 적절한 값을 지정해야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한 `signature` 속성에서 [명령어의 입력(expectation) 정의](#defining-input-expectations)도 가능합니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 여기에서 명령어에 필요한 주요 로직을 구현하면 됩니다.

예시 명령어 코드를 살펴보면, 의존성이 필요한 경우 해당 의존성을 `handle` 메서드의 타입힌트로 요청할 수 있다는 점을 볼 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)는 타입힌트된 모든 의존성을 자동으로 주입해줍니다.

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Send a marketing email to a user';

    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 코드의 재사용성을 높이기 위해, 콘솔 명령어 클래스는 가볍게 작성하고, 실제 주요 작업은 애플리케이션 서비스로 위임하는 것이 좋은 습관입니다. 위 예시에서도 핵심 로직(이메일 전송)을 서비스 클래스로 분리해 주입받아 사용하고 있습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 정상 실행되면, 종료코드 `0`으로 종료되어 성공임을 알립니다. 하지만 필요하다면 `handle` 메서드에서 정수값을 반환해 종료 코드(Exit Code)를 명시적으로 지정할 수도 있습니다.

```php
$this->error('Something went wrong.');

return 1;
```

명령어의 어느 메서드에서든 명시적으로 "실패" 처리를 하고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 호출 시 즉시 실행을 중단하고, 종료 코드 `1`로 반환됩니다.

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스 형태로 명령어를 만드는 것 대신, 라우트에 클로저를 사용하는 것처럼 직접 작성할 수 있는 대안입니다.

`routes/console.php` 파일은 HTTP 라우트가 아니라 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일 내에서는 `Artisan::command` 메서드를 사용하여 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 클로저(인수/옵션을 인자로 받음) 두 가지를 인자로 받습니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 내부적으로 명령어 인스턴스에 바인딩되어 있으므로, 일반 명령어 클래스에서 사용할 수 있는 각종 헬퍼 메서드를 모두 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입 힌트

명령어 클로저 내에서는 인수와 옵션 외에도, [서비스 컨테이너](/docs/12.x/container)에서 해결하고 싶은 추가 의존성을 타입힌트로 지정할 수 있습니다.

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명 추가

클로저 기반 명령어에 대한 설명은 `purpose` 메서드로 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어에서 출력됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 단일 실행 보장 명령어(Isolatable Commands)

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 합니다. 또한, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

어떤 명령어는 한 번에 단 하나의 인스턴스만 실행되도록 하고 싶을 때가 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

명령어에 `Isolatable`을 선언하면, 명령어에 옵션 정의를 따로 추가하지 않아도 Laravel이 `--isolated` 옵션을 자동으로 사용할 수 있도록 만들어줍니다. 해당 옵션으로 명령어를 실행할 경우, 같은 명령어의 다른 인스턴스가 이미 실행 중인 경우 실행되지 않습니다. 이는 애플리케이션의 기본 캐시 드라이버를 통해 원자적(atomic) 락을 획득하려는 방식으로 동작합니다. 만약 이미 실행 중인 인스턴스가 있다면 명령어는 실행되지 않지만, 실행 성공 상태 코드로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

명령어가 이미 실행 중인 상황에서 반환할 상태 코드를 지정하고 싶다면 `isolated` 옵션의 값으로 원하는 종료 코드를 전달하면 됩니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID(Lock ID)

기본적으로, 락을 위한 문자열 키는 명령어 이름을 사용해 생성됩니다. 그러나 명령어 클래스에 `isolatableId` 메서드를 정의하면, 인수나 옵션 값 등을 조합해 직접 키 값을 커스텀할 수 있습니다.

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### 락 만료 시간(Lock Expiration Time)

기본적으로 고립화 락(isolation lock)은 명령어 실행 후 해제되며, 명령어가 강제 종료되어 완료되지 못한 경우에는 1시간 후 만료됩니다. 락의 만료 시간을 직접 조정하고 싶다면, 명령어에 `isolationLockExpiresAt` 메서드를 정의하세요.

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대값 정의

콘솔 명령어를 작성할 때, 인수(argument)나 옵션(option)을 통해 사용자에게 입력값을 받는 경우가 많습니다. Laravel에서는 명령어의 `signature` 속성(property)에 간단명료한 경로(route)와 유사한 문법을 이용하여 입력값의 이름, 인수, 옵션을 모두 한 번에 정의할 수 있습니다.

<a name="arguments"></a>
### 인수(Arguments)

모든 사용자 입력 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서는 `user`라는 필수 인수를 정의하고 있습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나, 기본값을 부여하는 것도 가능합니다.

```php
// 선택적(optional) 인수...
'mail:send {user?}'

// 선택적 인수에 기본값 지정...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션 역시 인수와 유사하게 사용자 입력값의 한 형태입니다. CLI에서는 옵션을 두 개의 하이픈(`--`)으로 구분합니다. 옵션에는 값을 받는 옵션과 값을 받지 않는 옵션(불리언 스위치)이 있습니다. 불리언 옵션의 예시를 살펴보겠습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서 `--queue` 스위치는 명령어 실행 시 함께 전달할 수 있습니다. 스위치를 넘기면 옵션 값은 `true`, 미지정시에는 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 필요한 옵션(Options With Values)

다음은 값 입력이 반드시 필요한 옵션의 예시입니다. 옵션 이름 뒤에 `=` 기호를 붙여 작성하면 됩니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 아래와 같이 값을 직접 넘겨줘야 하며, 지정하지 않으면 기본적으로 `null`이 됩니다.

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면, 옵션명 뒤에 곧바로 기본값을 적어주면 됩니다. 사용자가 값을 넘기지 않으면 이 값이 자동으로 사용됩니다.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키(Option Shortcuts)

옵션 정의 시 단축키를 함께 지정하려면, 이름 앞에 단축키를 적고 `|` 문자로 구분해주면 됩니다.

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어 실행 시 단축키는 한 개의 하이픈으로 시작하며, 값을 넘길 때는 `=` 기호를 붙이지 않습니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열(Input Arrays)

여러 개의 입력값을 받을 인수나 옵션을 정의하려면 `*` 문자를 사용할 수 있습니다. 먼저 인수에 적용하는 예를 봅니다.

```php
'mail:send {user*}'
```

이렇게 정의하면, 명령어 실행 시 여러 `user` 값을 순서대로 넘길 수 있습니다. 아래와 같이 입력하면 `user` 인수는 값이 1, 2인 배열이 됩니다.

```shell
php artisan mail:send 1 2
```

또한, `*` 문자는 선택적 인수와도 조합할 수 있어 0개 이상 입력을 허용합니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열(Option Arrays)

여러 값을 받을 옵션의 경우, 전달하는 각 값마다 옵션명을 반복해서 사용합니다.

```php
'mail:send {--id=*}'
```

아래와 같이 여러 번 옵션을 작성하면, 명령어 내에서 `--id` 옵션이 배열로 전달됩니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력값 설명(Input Descriptions)

인수나 옵션에 대해 설명을 추가하고 싶다면, 이름과 설명을 콜론(`:`)으로 구분해 작성하면 됩니다. 설명이 길어지면 여러 줄로 나누어 가독성을 높일 수 있습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력값 프롬프트(Prompting for Missing Input)

명령어가 필수 인수를 포함한다면, 입력받지 않을 경우 사용자에게 오류 메시지가 표시됩니다. 또는, 필수 인수가 누락된 경우 Laravel이 자동으로 프롬프트를 띄워 사용자로부터 입력을 받을 수 있도록 설정할 수 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하세요.

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Laravel이 필수 인수를 입력받아야 하는 상황이 오면, 인수 이름이나 설명을 활용해 적절하게 질문을 표시하여 자동으로 값을 입력받습니다. 만약 이 질문 문구를 직접 커스텀하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현해 인수명별로 배열로 반환하면 됩니다.

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

질문과 함께 플레이스홀더(예시 입력)도 함께 표시하고 싶다면, 튜플로서 배열에 정의하면 됩니다.

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 동작을 완전히 직접 제어하고 싶다면, 사용자를 프롬프트하고 결과값을 반환하는 클로저를 지정할 수도 있습니다.

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts) 공식 문서에는 다양한 프롬프트 유형과 활용 방법이 자세히 나와 있습니다.

명령어의 `handle` 메서드에서 [옵션](#options)에 대한 추가 입력 프롬프트를 띄울 수도 있습니다. 다만, 누락된 인수 프롬프트가 표시된 뒤에만 옵션 프롬프트를 추가로 실행하고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현해 활용할 수 있습니다.

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
## 명령어 I/O

<a name="retrieving-input"></a>
### 입력값 조회

명령어 실행 도중, 명령어로 받은 인수와 옵션의 값을 조회해야 할 때가 많습니다. `argument`와 `option` 메서드로 손쉽게 값을 얻을 수 있습니다. 해당 인수나 옵션이 없으면 `null`이 반환됩니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수 값을 `array`로 한 번에 받고자 한다면 `arguments` 메서드를 사용하면 됩니다.

```php
$arguments = $this->arguments();
```

옵션도 `option` 또는 `options` 메서드를 통해 간단하게 조회할 수 있습니다.

```php
// 특정 옵션만 조회...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 조회...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 아름답고 편리한 CLI 양식 및 입력 기능(플레이스홀더, 유효성 검증 등)을 제공하는 PHP 패키지입니다.

명령어 출력뿐만 아니라, 명령어 실행 중 사용자에게 입력을 받아야 할 때가 있습니다. `ask` 메서드는 지정한 질문으로 사용자에게 입력을 요청하고, 입력받은 값을 반환합니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

`ask` 메서드의 두 번째 인자로 기본값을 전달하면, 사용자가 아무 값도 입력하지 않았을 때 해당 값이 반환됩니다.

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 유사하나, 입력한 값이 콘솔에 표시되지 않아 비밀번호와 같은 민감 정보 입력에 적합합니다.

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확답(Yes/No) 입력

사용자에게 단순히 "예/아니오" 형태의 확인을 받고 싶다면, `confirm` 메서드를 사용할 수 있습니다. 기본적으로 사용자가 `y` 또는 `yes`라고 입력하면 `true`를 반환하며, 그렇지 않으면 `false`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

확인 프롬프트의 기본값을 `true`로 하고 싶다면, 두 번째 인자에 `true`를 넘기면 됩니다.

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성(Auto-Completion)

`anticipate` 메서드는 입력값에 대한 자동 완성 제안을 제공합니다. 사용자는 제안된 값과 상관없이 자유롭게 입력할 수 있습니다.

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인자로 클로저를 넘길 수도 있습니다. 사용자가 타이핑할 때마다 클로저가 호출되며, 입력값을 인자로 받아 자동 완성에 활용할 수 있는 배열을 반환해야 합니다.

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택(Multiple Choice) 질문

사전에 정의된 여러 선택지 중 하나(또는 여러 개)를 입력받고 싶다면, `choice` 메서드를 사용할 수 있습니다. 세 번째 인자로 기본값의 배열 인덱스를 전달하면, 기본 선택값을 설정할 수 있습니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한 네 번째, 다섯 번째 인자로는 최대 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### 출력 작성

콘솔에 출력을 보내려면, `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 용도에 따라 적절한 ANSI 색상을 사용합니다. 예를 들어, `info` 메서드는 보통 초록색으로 정보를 출력합니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

에러 메시지를 표시할 때는 `error` 메서드를 사용하세요. 에러 메시지는 일반적으로 빨간색으로 표시됩니다.

```php
$this->error('Something went wrong!');
```

색상이 없는 단순 텍스트는 `line` 메서드를 사용하면 됩니다.

```php
$this->line('Display this on the screen');
```

빈 줄을 출력하려면 `newLine` 메서드를 사용할 수 있습니다.

```php
// 한 줄 출력
$this->newLine();

// 세 줄 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 표(Table) 출력

`table` 메서드는 여러 행/열로 구성된 데이터를 보기 좋게 테이블 형태로 출력할 수 있습니다. 컬럼 명과 데이터만 전달하면, Laravel이 알아서 표의 너비/높이를 맞춥니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바(Progress Bar)

처리 시간이 오래 걸리는 작업에는 진행 정도를 보여주는 프로그레스바를 사용할 수 있습니다. `withProgressBar` 메서드를 사용하면, 지정한 컬렉션(또는 이터러블)을 순회하며 진행 바를 자동으로 갱신해줍니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

좀 더 세밀하게 제어하고 싶다면, 먼저 전체 단계 수를 지정해서 프로그레스 바를 만들고, 각 항목마다 수동으로 `advance`를 호출할 수 있습니다.

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> [!NOTE]
> 더 고급 옵션은 [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

Laravel은 기본적으로 `app/Console/Commands` 디렉토리의 모든 명령어를 자동으로 등록합니다. 그러나 필요하다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 이용해 다른 디렉토리도 Artisan 명령어 탐색 대상으로 추가할 수 있습니다.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

그리고 명령어 클래스를 직접 지정해서 개별적으로 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션 내의 모든 명령어는 [서비스 컨테이너](/docs/12.x/container)로 해결(resolve)되고, Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램적으로 명령어 실행

때로는 CLI에서가 아니라, 라우트나 컨트롤러 등 애플리케이션 내부에서 Artisan 명령어를 실행해야 할 수 있습니다. 이 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. 첫 번째 인자는 명령어의 시그니처 이름 또는 클래스명, 두 번째 인자는 명령어에 전달할 파라미터 배열입니다. 실행 후 종료 코드가 반환됩니다.

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

명령어 전체 문자열을 그대로 `call` 메서드에 넘길 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

만약 명령어가 배열 옵션을 받는다면, 해당 옵션 값에 배열을 그대로 넘기면 됩니다.

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달

문자열 값을 받지 않는 플래그 옵션(예: `migrate:refresh`의 `--force` 플래그)을 지정할 때는 `true` 또는 `false`를 값으로 넘기면 됩니다.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐 처리

`Artisan` 파사드의 `queue` 메서드를 이용하면, Artisan 명령어를 [큐 워커](/docs/12.x/queues)가 백그라운드에서 처리하도록 큐잉할 수도 있습니다. 이 메서드를 사용하기 전에는 큐 설정을 완료하고 큐 리스너가 실행 중이어야 합니다.

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`, `onQueue` 메서드를 추가로 사용하면, 명령어를 실행할 큐 커넥션이나 큐 이름을 세부적으로 지정할 수 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출

기존의 콘솔 명령어 클래스 내에서 다른 콘솔 명령어를 호출하는 것이 필요할 수 있습니다. 이 때는 `call` 메서드를 사용하면 됩니다. 명령어 이름과 인수/옵션 배열을 인자로 전달하십시오.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

다른 콘솔 명령어를 호출하되, 해당 명령어의 출력물을 모두 감추고 싶다면 `callSilently` 메서드를 사용할 수 있습니다. 메서드 사용법은 `call`과 동일합니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있는 기능을 제공합니다. 예를 들어 `SIGTERM` 시그널은 프로그램에 종료 요청을 알릴 때 사용됩니다. Artisan 콘솔 명령어에서 시그널을 수신하여 특정 동작을 실행하고 싶다면 `trap` 메서드를 이용하면 됩니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 시그널을 한 번에 감지하고 싶다면, `trap` 메서드에 배열을 전달하면 됩니다.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 파일 커스터마이징

Artisan 콘솔의 `make` 명령어들은 컨트롤러, 작업(Job), 마이그레이션, 테스트 등 다양한 클래스를 생성해줍니다. 이 클래스들은 입력값에 따라 내용을 채워 넣는 "스텁(stub)" 파일을 기반으로 생성됩니다. 만약 Artisan이 생성하는 파일을 입맛대로 조정하고 싶다면, `stub:publish` 명령어로 기본 스텁 파일을 프로젝트 내에 복사해 직접 수정할 수 있습니다.

```shell
php artisan stub:publish
```

스텁 파일은 애플리케이션 루트의 `stubs` 디렉토리에 위치하게 되며, 수정한 내용은 이후 Artisan의 `make` 계열 명령어로 클래스를 생성할 때 모두 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan이 명령어를 실행할 때는 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
- `ArtisanStarting` 이벤트는 Artisan이 실행을 시작하자마자 바로 발생합니다.  
- 그다음, 명령어가 실행되기 직전에 `CommandStarting` 이벤트가 발생하고,  
- 마지막으로 명령어가 실행을 마치면 `CommandFinished` 이벤트가 발생합니다.