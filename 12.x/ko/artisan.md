# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력에 대한 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력 값 조회](#retrieving-input)
    - [입력 요청 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그램 내에서 명령어 실행](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Artisan은 Laravel에 포함된 명령행 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 유용한 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 명령어가 제공하는 인수와 옵션을 보여주고 설명하는 "도움말(help)" 화면도 포함되어 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우, 명령행에서 Artisan 명령어를 실행할 때 반드시 `sail` 명령어를 사용해야 합니다. Sail은 여러분의 애플리케이션 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 Laravel 프레임워크용 강력한 REPL(Read-Eval-Print Loop)입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만, 이전에 애플리케이션에서 제거했다면 Composer를 사용하여 Tinker를 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 여러 줄의 코드 편집, 자동완성을 원한다면 [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 Eloquent 모델, 작업(jobs), 이벤트 등 여러분의 전체 Laravel 애플리케이션과 명령행에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 다음과 같이 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령어를 이용해 Tinker의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 가비지 컬렉션에 의존하여 작업을 큐에 넣습니다. 따라서 Tinker에서는 작업을 디스패치할 때 반드시 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록(Command Allow List)

Tinker는 "허용(allow)" 목록을 사용하여 셸 내에서 실행 가능한 Artisan 명령어를 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭이 적용되지 않아야 하는 클래스

일반적으로 Tinker는 사용자가 클래스와 상호작용할 때 자동으로 클래스를 별칭(alias) 처리합니다. 그러나 일부 클래스는 절대 별칭을 적용하지 않게 하고 싶을 수 있습니다. 이 경우 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가하세요:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성 (Writing Commands)

Artisan이 제공하는 기본 명령어 외에도, 자신만의 커스텀 명령어를 작성할 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉토리에 저장되지만, 원한다면 [다른 디렉토리도 Artisan 명령어 스캔 대상](#registering-commands)으로 지정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성 (Generating Commands)

새로운 명령어를 생성하려면 `make:command` Artisan 명령어를 사용하면 됩니다. 이 명령어는 `app/Console/Commands` 디렉토리에 새로운 명령어 클래스를 생성합니다. 해당 디렉토리가 아직 없다면, 이 Artisan 명령어를 처음 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조 (Command Structure)

명령어를 생성한 뒤에는 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한 `signature` 속성은 [명령어의 입력 기대값](#defining-input-expectations)을 정의하는 데에도 활용됩니다. 명령어가 실행될 때는 `handle` 메서드가 실행되며, 이 메서드에서 명령어의 실제 로직을 작성하면 됩니다.

아래는 예시 명령어입니다. 이 예시에서는 `handle` 메서드를 통해 필요한 의존성을 주입받을 수 있습니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 이 메서드의 시그니처에 타입힌트된 모든 의존성을 자동으로 주입해줍니다.

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
> 코드의 재사용성을 높이기 위해, 콘솔 명령어 자체는 가볍게 유지하고 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예시에서도 '이메일 발송'의 핵심 처리를 서비스 클래스에 위임하고 있습니다.

<a name="exit-codes"></a>
#### 종료 코드 (Exit Codes)

`handle` 메서드에서 아무 값도 반환하지 않고 명령어가 정상적으로 실행되면, 종료 코드는 `0`이 되어 성공을 의미합니다. 하지만 필요하다면 `handle` 메서드에서 정수 값을 반환하여 직접 종료 코드를 지정할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내 어디서든 명령어를 "실패" 상태로 종료하고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령어 실행을 중단하고, 종료 코드를 `1`로 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어 (Closure Commands)

클로저 기반 명령어는 명령어를 클래스가 아닌 클로저로 정의하는 대안입니다. 이 방식은 라우트 클로저가 컨트롤러를 대체할 수 있는 것과 비슷하게, 명령어 클로저는 명령어 클래스를 대체할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않고, 애플리케이션에 대한 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 모두 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와, 명령어의 인수와 옵션을 파라미터로 받는 클로저를 인수로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 내부적으로 명령어 인스턴스에 바인딩되므로, 클래스 기반 명령어에서 사용 가능한 헬퍼 메서드를 모두 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

명령어의 인수 및 옵션 외에도, 명령어 클로저에 추가적으로 [서비스 컨테이너](/docs/12.x/container)에서 해결되는 의존성을 타입힌트로 지정할 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 기반 명령어를 정의할 때 `purpose` 메서드를 사용해 명령어의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령어 실행 시 함께 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

특정 명령어가 동시에 단 하나의 인스턴스만 실행되도록 하고 싶을 때가 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다:

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

`Isolatable`을 구현한 경우, Laravel은 별도의 옵션 추가 없이도 해당 명령어에 자동으로 `--isolated` 옵션을 제공합니다. 명령어를 이 옵션과 함께 실행하면, Laravel은 동일 명령어의 다른 인스턴스가 이미 실행 중인지 확인하여, 그렇다면 실행하지 않습니다. 이는 애플리케이션의 기본 캐시 드라이버를 사용해 원자적(atomic) 락을 획득하는 방식으로 동작합니다. 만약 이미 다른 인스턴스가 실행 중이라면 명령어는 실행되지 않지만, 그래도 정상 종료 상태 코드로 빠져나갑니다:

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행되지 않을 경우 반환할 종료 상태 코드를 지정하려면, `isolated` 옵션에 원하는 상태 코드를 지정할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID (Lock ID)

기본적으로 Laravel은 명령어 이름을 사용해 캐시에 원자적 락을 획득할 키 문자열을 생성합니다. 그러나, 명령어 클래스에 `isolatableId` 메서드를 정의하면 이 키를 커스터마이즈할 수 있습니다. 예를 들어 명령어의 인수나 옵션을 키에 통합할 수 있습니다:

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
#### 락 만료 시간 (Lock Expiration Time)

기본적으로, 격리 락은 명령어 실행이 완료되면 만료됩니다. 또는, 명령어가 중단(interrupt)되어 끝나지 못한 경우 한 시간 후에 만료됩니다. 락 만료 시간을 변경하려면 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의하세요:

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
## 입력 기대값 정의 (Defining Input Expectations)

콘솔 명령어를 작성할 때 사용자가 직접 입력할 인수(argument)나 옵션(option)을 수집해야 할 때가 많습니다. Laravel은 `signature` 속성을 사용하여, 사용자로부터 기대하는 입력값을 매우 편리하게 정의할 수 있게 해줍니다. 이 속성을 통해 명령어 이름, 인수, 옵션 등을 라우트 시그니처와 비슷한 표현식으로 한 번에 정의할 수 있습니다.

<a name="arguments"></a>
### 인수 (Arguments)

사용자 입력 인수와 옵션은 모두 중괄호로 감쌉니다. 아래 예제에서는 `user`라는 필수 인수 하나를 정의하고 있습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션 (Options)

옵션도 인수와 유사하게 사용자 입력의 한 형태로, 명령줄에서 옵션을 전달할 때는 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값을 받는 옵션과 받지 않는 옵션의 두 가지 종류가 있습니다. 값을 받지 않는 옵션은 일종의 불린 "스위치"로 활용됩니다. 아래는 그런 옵션의 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

이 예시에서 `--queue` 스위치는 명령어 실행 시 명시적으로 지정할 수 있습니다. 지정되었다면 옵션 값은 `true`, 지정되지 않았다면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 기대하는 옵션의 경우, 옵션 이름 뒤에 `=` 기호를 붙여 정의합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 사용자는 다음과 같이 옵션의 값을 전달할 수 있습니다. 옵션이 명시되지 않았다면 기본값은 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면 옵션 이름 뒤에 바로 값을 작성하면 됩니다. 사용자가 값 없이 실행하면 이 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션을 정의할 때 단축키를 지정하려면 옵션 이름 앞에 단축키를 적고, `|` 문자로 단축키와 전체 옵션 이름을 구분합니다:

```php
'mail:send {user} {--Q|queue=}'
```

명령행에서 옵션 단축키를 사용할 때는 하이픈 하나만 붙이고, 값을 지정할 때 `=` 기호를 쓰지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열 (Input Arrays)

인수나 옵션이 복수 개의 입력값을 받을 수 있도록 하려면 `*` 문자를 사용합니다. 먼저, 인수에 적용한 예시는 다음과 같습니다:

```php
'mail:send {user*}'
```

이 명령어를 실행할 때, 여러 `user` 인수를 순서대로 명령행에 나열할 수 있습니다. 예를 들어 다음 명령어는 `user`의 값이 `1`, `2`인 배열로 전달됩니다:

```shell
php artisan mail:send 1 2
```

`*` 문자는 선택적 인수와 결합하여, 0개 이상의 입력값도 허용할 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

배열 형태의 옵션도 가능합니다. 이 경우 각 옵션 값은 옵션 이름과 함께 반복해서 지정하면 됩니다:

```php
'mail:send {--id=*}'
```

다음처럼 여러 옵션 값이 전달됩니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명 (Input Descriptions)

인수 또는 옵션에 설명을 추가하려면, 인수/옵션 이름 뒤에 콜론(:)을 붙이고 설명을 적습니다. 명령어 정의가 길어질 경우 여러 줄로 정의해도 무방합니다:

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
### 누락된 입력에 대한 프롬프트 (Prompting for Missing Input)

명령어에 필수 인수가 있을 때 사용자가 인수를 지정하지 않으면 에러 메시지를 보게 됩니다. 대안으로, 명령어가 필수 인수가 빠진 경우 사용자에게 자동으로 입력을 요청(prompt)하도록 설정할 수 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하면 됩니다:

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

Laravel은 필수 인수가 누락된 경우 인수의 이름이나 설명을 활용해 적절히 질문을 만들어, 자동으로 사용자에게 프롬프트를 표시합니다. 수집 질문을 직접 커스터마이즈하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현해, 인수명에 해당하는 질문을 배열로 반환할 수 있습니다:

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

질문과 플레이스홀더(placeholder)를 함께 반환하고 싶으면 튜플로 작성합니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 자체의 동작을 완전히 제어하고 싶다면 사용자에게 질문하고 답변받는 클로저를 반환할 수도 있습니다:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts) 문서에서는 추가적인 프롬프트 유형과 활용법을 더 소개하고 있습니다.

옵션([options](#options))에 대한 입력 프롬프트를 원할 때는, 명령어의 `handle` 메서드에서 직접 프롬프트를 사용할 수 있습니다. 단, 프롬프트가 누락된 인수로 인해 자동으로 표시될 때만 추가로 옵션에 대한 프롬프트를 띄우고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현하세요:

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
## 명령어 입출력 (Command I/O)

<a name="retrieving-input"></a>
### 입력 값 조회 (Retrieving Input)

명령어가 실행되는 동안, 명령어에서 수락한 인수와 옵션의 값을 조회할 필요가 있을 것입니다. 이때는 `argument` 및 `option` 메서드를 사용할 수 있습니다. 해당 인수나 옵션이 존재하지 않으면 `null`이 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 `array`로 취득하려면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 메서드로 값을 가져오며, 옵션 전체를 배열로 받으려면 `options` 메서드를 사용합니다:

```php
// 특정 옵션 값 조회...
$queueName = $this->option('queue');

// 모든 옵션 배열로 조회...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 요청 프롬프트 (Prompting for Input)

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령행 애플리케이션에 아름답고 사용하기 편리한 폼을 추가할 수 있게 해주는 PHP 패키지입니다. 플레이스홀더 텍스트, 유효성 검증 등 브라우저와 유사한 기능을 제공합니다.

출력만 표시할 뿐만 아니라, 명령어 실행 도중 사용자에게 입력을 요청할 수도 있습니다. `ask` 메서드는 질문을 표시하고, 사용자의 응답을 입력 받아 반환합니다:

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

`ask` 메서드는 선택적으로 두 번째 인수에, 사용자가 아무 입력도 하지 않았을 때 반환할 기본값도 지정할 수 있습니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 사용자가 입력하는 내용을 콘솔에 표시하지 않습니다. 비밀번호처럼 민감한 정보를 받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청 (Asking for Confirmation)

사용자에게 단순히 "예/아니오" 답변을 요청해야 한다면 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 사용자가 `y` 또는 `yes`를 입력했을 때 `true`를 반환하며, 그렇지 않으면 `false`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요하다면 두 번째 인수로 `true`를 전달해, 기본적으로 `true`를 반환하도록 설정할 수 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성 (Auto-Completion)

`anticipate` 메서드를 사용하면 입력값에 대해 가능한 선택지를 자동 완성으로 제안할 수 있습니다. 사용자는 그 제안과 무관하게 어떤 값도 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

두 번째 인수로 클로저를 전달하면, 사용자가 입력할 때마다 해당 클로저가 실행되어, 실시간 자동완성 목록을 제공합니다. 클로저는 지금까지 입력된 값을 받아 처리하고, 자동완성 옵션 배열을 반환해야 합니다:

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
#### 다중 선택 (Multiple Choice Questions)

사용자에게 미리 정의한 선택지 중 하나를 입력받고 싶다면 `choice` 메서드를 활용할 수 있습니다. 세 번째 인수로 기본값의 배열 인덱스를 전달하면, 사용자가 직접 선택하지 않았을 때 사용할 선택지가 지정됩니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

아울러, `choice` 메서드는 네 번째, 다섯 번째 인수로 시도 횟수 제한, 다중 선택 허용 여부도 받을 수 있습니다:

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
### 출력 작성 (Writing Output)

콘솔에 출력을 보내려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 이용하세요. 각각의 메서드는 의도에 맞는 ANSI 색상을 사용합니다. 예를 들어, 일반적인 정보 메시지는 `info` 메서드로 표시할 수 있으며, 이는 주로 초록색으로 출력됩니다:

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

에러 메시지를 표시하려면 `error` 메서드를 사용하세요. 주로 빨간색으로 출력됩니다:

```php
$this->error('Something went wrong!');
```

색상 없는 일반 텍스트를 표시하려면 `line` 메서드를 사용하면 됩니다:

```php
$this->line('Display this on the screen');
```

빈 줄을 출력하려면 `newLine` 메서드를 사용하세요:

```php
// 한 줄 출력
$this->newLine();

// 세 줄 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 표 (Tables)

`table` 메서드를 사용하면 여러 행/열로 구성된 데이터를 보기 좋게 포맷할 수 있습니다. 컬럼명과 데이터를 배열로 전달하면, 적절한 너비와 높이로 표가 자동으로 출력됩니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄 (Progress Bars)

작업이 오래 걸릴 때는 진행률 표시줄(progress bar)을 보여주는 것이 사용자에게 도움을 줍니다. `withProgressBar` 메서드를 사용하면, 주어진 iterable 값의 각 반복마다 진행 상태를 자동으로 표시할 수 있습니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행률 표시줄을 수동으로 제어할 필요가 있다면, 전체 단계 수를 먼저 지정한 후 각 항목 처리마다 표시줄을 하나씩 이동시키면 됩니다:

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
> 더 많은 기능은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록 (Registering Commands)

기본적으로, Laravel은 `app/Console/Commands` 디렉토리에 있는 모든 명령어를 자동으로 등록합니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용해, 다른 디렉토리도 Artisan 명령어 탐색 대상으로 추가할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

또한, 단일 명령어 클래스를 직접 등록해야 할 때는 클래스명을 `withCommands`에 전달하면 됩니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅되면, 서비스 컨테이너를 통해 여러분의 모든 명령어가 자동으로 해석되어 Artisan과 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램 내에서 명령어 실행 (Programmatically Executing Commands)

CLI 외부에서 Artisan 명령어를 실행해야 할 경우가 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령어를 실행하고 싶을 때가 그렇습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 활용할 수 있습니다. `call` 메서드는 첫 인수로 명령어의 시그니처 이름이나 클래스명을, 두 번째 인수로 명령어 파라미터 배열을 받습니다. 반환값은 종료 코드입니다:

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

명령어 전체를 문자열로 작성하여 `call` 메서드에 전달해도 됩니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

옵션이 배열을 허용할 경우, 값 배열을 그대로 넘길 수 있습니다:

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
#### 불린 값 전달

문자열 값을 허용하지 않는 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그)에 옵션 값을 지정하려면 `true`나 `false`를 넘기면 됩니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면, Artisan 명령어를 큐잉하여 [큐 워커](/docs/12.x/queues)가 백그라운드에서 처리하도록 할 수 있습니다. 먼저 큐를 설정하고 큐 리스너가 동작 중이어야 합니다:

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

`onConnection`과 `onQueue` 메서드를 이용해 Artisan 명령어를 보낼 커넥션이나 큐를 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출 (Calling Commands From Other Commands)

기존 Artisan 명령어에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용하면 됩니다. 인수로 명령어 이름과 파라미터 배열을 전달하면 됩니다:

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

다른 콘솔 명령어를 호출하되 그 출력까지 모두 숨기고 싶다면 `callSilently` 메서드를 사용하세요. 시그니처는 `call`과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리 (Signal Handling)

운영체제에서는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 운영체제가 프로그램에 종료 요청을 보낼 때 사용됩니다. Artisan 콘솔 명령어에서 특정 시그널을 감지하고 시그널이 발생했을 때 실행할 코드를 작성하려면 `trap` 메서드를 사용할 수 있습니다:

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

여러 시그널을 한 번에 감지하려면, `trap` 메서드에 배열로 시그널 목록을 전달하면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징 (Stub Customization)

Artisan 콘솔의 `make` 계열 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 이 클래스들은 "스텁(stub)" 파일을 기반으로 생성되며, 사용자 입력에 맞게 값이 치환되어 파일이 만들어집니다. 그러나, Artisan이 생성하는 파일을 여러분의 필요에 맞게 수정하고 싶을 수 있습니다. 이럴 때 `stub:publish` 명령어를 사용해 자주 사용하는 스텁 파일을 애플리케이션에 퍼블리시하여 커스터마이징할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉토리에 위치하게 됩니다. 이 파일을 수정하면, Artisan의 `make` 명령어 실행 시 해당 변경사항이 반영된 파일이 생성됩니다.

<a name="events"></a>
## 이벤트 (Events)

Artisan은 명령어 실행 시 다음 세 가지 이벤트를 디스패치합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`입니다. `ArtisanStarting` 이벤트는 Artisan이 실행을 시작할 때 즉시 발생합니다. 이어서, 어떤 명령어가 실행되기 직전에 `CommandStarting` 이벤트가 발생하고, 명령어 작업이 끝난 후에는 `CommandFinished` 이벤트가 발생합니다.
