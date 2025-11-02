# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [단일 실행 보장 명령어](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [명령어 I/O](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그래밍 방식 명령어 실행](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이즈](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan(아티즌)은 Laravel에 기본 포함되어 있는 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트 경로에 `artisan` 스크립트로 위치하며, 애플리케이션을 개발하는 데 도움이 되는 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 실행하면 됩니다:

```shell
php artisan list
```

모든 명령어에는 해당 명령어의 인수 및 옵션을 보여주고 설명해주는 "도움말(help)" 화면이 포함되어 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 함을 기억하세요. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크를 위한 강력한 REPL 환경으로, [PsySH](https://github.com/bobthecow/psysh) 패키지에 의해 동작합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 애플리케이션에서 Tinker를 제거했다면, Composer를 사용해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션에서 핫 리로딩, 여러 줄 코드 편집, 자동완성 기능을 원한다면 [Tinkerwell](https://tinkerwell.app)을 참고해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 커맨드라인에서 전체 Laravel 애플리케이션과 상호작용할 수 있습니다. Eloquent 모델, 작업(job), 이벤트 등도 모두 사용 가능합니다. Tinker 환경에 진입하려면 아래와 같이 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일을 공개하려면 `vendor:publish` 명령어를 사용할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡이 큐에 등록될 때 garbage collection(가비지 컬렉션)에 의존합니다. 따라서 tinker에서는 잡을 디스패치할 때 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록

Tinker는 "허용(allow)" 목록을 사용하여, 어떤 Artisan 명령어가 Tinker 셸 내에서 실행될 수 있는지 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어는 실행할 수 있습니다. 더 많은 명령어를 허용하려면, `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 별칭을 만들지 않을 클래스

일반적으로 Tinker는 Tinker 내에서 상호작용하는 클래스에 대해 자동으로 별칭을 만듭니다. 그러나 특정 클래스는 절대 별칭을 만들지 않도록 하고 싶을 수 있습니다. 이를 위해서는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan에서 제공하는 명령어 외에도, 사용자가 직접 커스텀 명령어를 만들 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 저장하지만, [다른 디렉터리도 Artisan 명령어를 검색하도록](#registering-commands) 설정하면 원하는 위치에 저장할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 생성하려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 생성합니다. 해당 디렉터리가 존재하지 않더라도 걱정하지 마세요. `make:command` 명령어를 처음 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어가 생성되면, 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해주어야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한 `signature` 속성을 이용해 [명령어의 입력 기대값](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되고, 주요 로직을 이 메서드에 작성합니다.

예제 명령어를 살펴보겠습니다. 아래 예제에서는 필요한 의존성을 `handle` 메서드에서 타입 힌트로 요청할 수 있으며, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 이러한 의존성을 주입합니다:

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
> 코드의 재사용성을 높이기 위해, 콘솔 명령어 자체의 로직을 가볍게 유지하고 핵심 작업은 애플리케이션 서비스로 분리하는 것이 좋습니다. 위 예제에서처럼, "실제 이메일 발송"과 같은 복잡한 작업은 서비스 클래스를 주입해 수행하는 방식이 권장됩니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 정상적으로 실행되면, 명령어는 성공을 의미하는 `0` 종료 코드로 종료됩니다. 그러나 필요하다면 `handle` 메서드에서 정수 값을 반환하여 명령어의 종료 코드를 수동으로 지정할 수 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내의 어떤 메서드에서든 명령어를 "실패" 상태로 즉시 종료하고 싶다면, `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어 실행을 중지하고 종료 코드 1을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스를 정의하지 않고도 콘솔 명령어를 작성할 수 있는 대안입니다. 라우트에서 클로저를 컨트롤러 대신 사용할 수 있듯이, 커맨드 클로저도 명령어 클래스를 대체할 수 있습니다.

`routes/console.php` 파일에는 HTTP 라우트가 정의되는 것은 아니지만, 애플리케이션으로 진입하는 콘솔 기반 진입점을 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 모두 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와, 인수와 옵션을 전달받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 내부적으로 명령어 인스턴스에 바인딩되므로, 일반 명령어 클래스에서 사용할 수 있는 여러 헬퍼 메서드를 동일하게 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입 힌트

클로저 명령어에서도 명령어의 인수 및 옵션을 전달받는 것과 더불어, [서비스 컨테이너](/docs/12.x/container)에서 해결하고 싶은 의존성을 타입 힌트로 지정할 수 있습니다:

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

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 이용해 명령어에 대한 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어 실행 시 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 단일 실행 보장 명령어

> [!WARNING]
> 이 기능을 사용하려면, 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

때때로 한 번에 명령어의 인스턴스가 단 하나만 실행되도록 보장하고 싶을 수 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현해주면 됩니다:

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

이렇게 명령어를 `Isolatable`로 표시하면, Artisan은 명령어 옵션에 `--isolated`를 자동으로 추가하여 별도로 정의하지 않아도 사용할 수 있습니다. 이 옵션과 함께 명령어가 호출되면, Laravel은 기본 캐시 드라이버를 이용해 원자적(atomic) 락을 시도하여 명령어 동일 실행을 방지합니다. 이미 다른 인스턴스가 실행 중이면, 명령어는 실행되지 않고 성공적인 상태 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행되지 않을 때 반환하고 싶은 상태 코드를 지정하려면, `isolated` 옵션에 원하는 코드를 전달하면 됩니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어의 이름을 사용해 캐시에 설정할 원자적 락의 문자열 키를 생성합니다. 하지만, 필요하다면 Artisan 명령어 클래스에 `isolatableId` 메서드를 정의하여 키로 사용할 값을 커스터마이즈할 수 있습니다. 이를 통해 명령어의 인수나 옵션 값을 키에 포함할 수 있습니다:

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
#### 락 만료 시간

기본적으로 isolation 락은 명령어가 끝나면 만료되며, 명령어가 중단되어 종료되지 못해도 1시간 후에 자동으로 만료됩니다. 락 만료 시간을 조정하려면, 커맨드에서 `isolationLockExpiresAt` 메서드를 정의하세요:

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

콘솔 명령어를 작성할 때, 사용자로부터 인수(argument)나 옵션(option) 형태로 입력을 받는 경우가 많습니다. Laravel은 명령어 클래스의 `signature` 속성에서 표현력 있는 라우트와 유사한 문법으로 기대하는 입력값을 매우 편리하게 정의할 수 있도록 합니다.

<a name="arguments"></a>
### 인수

사용자가 입력하는 모든 인수와 옵션은 중괄호로 감쌉니다. 다음 예제에서는 필수 인수 `user`를 하나 정의합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나, 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 선택적 인수 및 기본값 설정...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션은 인수와 마찬가지로 사용자 입력의 한 종류입니다. 옵션은 명령줄에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값을 받는 유형과, 값을 받지 않는(즉, 불린 스위치로 동작하는) 유형이 있습니다. 아래 예제는 불린 스위치 옵션의 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위에서 `--queue` 스위치는 Artisan 명령어 호출 시 지정할 수 있습니다. `--queue` 스위치가 전달되면 옵션의 값은 `true`, 전달되지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

다음은 값을 받는 옵션 예제입니다. 사용자가 옵션의 값을 반드시 지정해야 할 때는, 옵션 이름 뒤에 `=` 기호를 붙입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 예제의 경우, 아래처럼 옵션에 값을 전달할 수 있고, 옵션을 생략하면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에도 기본값을 지정할 수 있습니다. 사용자가 옵션 값을 전달하지 않으면 기본값이 대신 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정하려면, 옵션 이름 앞에 작성하고 `|` 문자로 구분합니다:

```php
'mail:send {user} {--Q|queue=}'
```

명령어를 터미널에서 실행할 때, 옵션 단축키는 한 개의 하이픈으로 시작하고 값은 `=` 없이 바로 붙입니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

하나의 인수 또는 옵션에 여러 입력값을 원한다면, `*` 문자를 이용하세요. 인수 예제를 먼저 보겠습니다:

```php
'mail:send {user*}'
```

이렇게 하면 명령줄에서 여러 `user` 인수를 순서대로 전달할 수 있습니다. 다음 명령은 `user` 값으로 `[1, 2]` 배열을 제공합니다:

```shell
php artisan mail:send 1 2
```

`*`를 선택적 인수와 결합하면 입력하지 않을 수도, 여러 개를 입력할 수도 있게 됩니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받는 옵션을 정의할 때는, 각 값마다 옵션 이름을 앞에 명시해야 합니다:

```php
'mail:send {--id=*}'
```

이 명령어는 다음과 같이 여러 `--id` 옵션을 전달해 호출할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수와 옵션에 콜론(`:`)으로 구분해 설명을 추가할 수 있습니다. 정의가 길다면 여러 줄로 나누어 작성해도 괜찮습니다:

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
### 누락된 입력 프롬프트

명령어에 필수 인수가 있는데 사용자가 입력하지 않을 경우, 에러 메시지를 받게 됩니다. 대신, 필수 인수가 누락됐을 때 명령어가 사용자에게 자동으로 질문하도록 구성할 수 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하면 됩니다:

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

Laravel이 필수 인수를 사용자로부터 받아야 할 필요가 있으면, 인수 이름이나 설명에 기반해 자동으로 적절한 질문을 던집니다. 만약 이 질문을 커스터마이즈하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현하여 인수 이름 => 질문 형태의 배열을 반환할 수 있습니다:

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

플레이스홀더 텍스트도 배열 안에 튜플 형식으로 함께 지정할 수 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

더 완전한 제어가 필요하다면, 클로저를 제공하여 질문과 답변 과정을 직접 처리할 수도 있습니다:

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
> [Laravel Prompts](/docs/12.x/prompts) 문서에서 더 다양한 프롬프트 및 사용법을 확인할 수 있습니다.

옵션을 [입력받는 프롬프트](#options)로 사용자에게 제시하고 싶다면, 명령어의 `handle` 메서드 내에서 프롬프트를 사용할 수 있습니다. 단, 필수 인수 자동 프롬프트와 함께 옵션 프롬프트도 처리하고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하세요:

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
### 입력값 가져오기

명령어가 실행되는 도중에, 명령어가 허용한 인수와 옵션의 값을 가져와야 할 수 있습니다. 각각의 값은 `argument` 및 `option` 메서드를 통해 가져올 수 있습니다. 해당 인수나 옵션이 없으면 `null`을 반환합니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 가져오려면 `arguments` 메서드를 사용하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 또는 `options` 메서드로 값이나 전체 배열을 쉽게 얻을 수 있습니다:

```php
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령줄 애플리케이션에서 자리표시자, 유효성 검증 등 웹 브라우저와 비슷한 방식의 사용자 친화적인 폼을 구축할 수 있게 해주는 PHP 패키지입니다.

출력뿐 아니라, 명령어 실행 중 사용자의 입력을 받을 수도 있습니다. `ask` 메서드는 주어진 질문을 출력하고 사용자로부터 입력을 받아 반환합니다:

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

`ask` 메서드는 두 번째 인수로 사용자 입력이 없을 때 반환할 기본값도 지정할 수 있습니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 유사하지만, 콘솔에 입력할 때 사용자 입력이 보이지 않습니다. 비밀번호 등 민감한 정보를 받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(yes/no) 프롬프트

간단한 "예/아니오" 질문을 하고 싶으면 `confirm` 메서드를 사용할 수 있습니다. 사용자가 `y` 또는 `yes`라고 입력하면 true를 반환하고, 기본값으로는 false를 반환합니다:

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 yes로 하고 싶을 땐 두 번째 인수에 true를 전달하세요:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드를 사용하면, 미리 정의한 선택지들에 대해 입력 자동완성을 제공할 수 있습니다. 자동완성 힌트와 무관하게 사용자는 어떤 답변이든 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는, 두 번째 인수로 클로저를 넘겨 문자 입력 시마다 자동완성 목록을 실시간으로 반환할 수 있습니다:

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
#### 다중 선택 질문

미리 정해진 선택지 중 하나를 선택하게 하고 싶다면 `choice` 메서드를 사용할 수 있습니다. 선택지가 선택되지 않을 때 반환할 기본값의 배열 인덱스를 세 번째 인수로 지정할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

추가로 최대 시도 횟수, 여러 개 선택 허용 여부 등 네 번째, 다섯 번째 인수로 옵션을 조정할 수도 있습니다:

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

콘솔에 출력을 보내려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 이용하세요. 각각 ANSI 컬러로 적절한 색상을 사용합니다. 예를 들어, 일반적인 안내 메시지는 보통 녹색의 `info` 메서드로 표시합니다:

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

에러 메시지를 표시할 때는 주로 붉은색의 `error` 메서드를 사용합니다:

```php
$this->error('Something went wrong!');
```

색깔 없는 일반 텍스트 출력을 원할 땐 `line` 메서드를 사용하세요:

```php
$this->line('Display this on the screen');
```

빈 줄을 삽입하려면 `newLine` 메서드를 사용하세요:

```php
// 한 줄 띄우기
$this->newLine();

// 세 줄 띄우기
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드를 통해 여러 행/열의 데이터를 보기 좋게 포맷된 표로 출력할 수 있습니다. 컬럼 이름과 데이터 배열만 넘기면, Laravel이 표의 너비와 높이를 자동으로 계산해줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

처리 시간이 오래 걸리는 작업에는, 사용자가 현재 진행도를 알도록 진행 바(progress bar)를 표시할 수 있습니다. `withProgressBar` 메서드를 사용하면, 주어진 반복가능(iterable) 값의 각 회차마다 진행 바를 표시할 수 있습니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행 바의 어드밴스(advance) 제어를 직접 하고 싶을 때는, 반복 횟수를 미리 정한 뒤 각 처리 후에 한 단계씩 이동시키세요:

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
> 더 고급 진행 바 옵션이 필요하다면, [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

Laravel은 기본적으로 `app/Console/Commands` 디렉터리 내의 모든 명령어를 자동으로 등록합니다. 그러나 `bootstrap/app.php` 파일의 `withCommands` 메서드를 사용하여 다른 디렉터리도 Artisan 명령어 검색 대상으로 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면, 명령어 클래스명을 직접 전달하여 수동 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션 내부의 모든 명령어는 [서비스 컨테이너](/docs/12.x/container)에서 해결되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식 명령어 실행

때때로 CLI 외의 환경(예: 라우트나 컨트롤러 등)에서 Artisan 명령어를 실행해야 할 수 있습니다. 이 때는 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. 첫 번째 인수로 명령어의 시그니처 이름이나 클래스명, 두 번째 인수로 파라미터 배열을 넘겨 실행하면 됩니다. 반환값은 종료 코드(exit code)입니다:

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

또는 전체 Artisan 명령어를 문자열로 한 번에 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어에서 옵션이 배열을 받는다면, 해당 옵션에 배열 형태로 값을 전달할 수 있습니다:

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

문자열 값을 받지 않는 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그)에는 옵션 값으로 `true` 또는 `false`를 전달하세요:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 등록하여 [큐 워커](/docs/12.x/queues)가 백그라운드에서 처리하도록 할 수도 있습니다. 사용 전에 큐 설정 및 리스너가 동작 중인지 확인하세요:

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

그리고 `onConnection`, `onQueue` 메서드로 연결 또는 큐 이름도 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

기존 Artisan 명령어 내에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 이용하세요. 이 메서드는 명령어 이름과 인수/옵션 배열을 받습니다:

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

다른 콘솔 명령어를 호출하되, 출력은 모두 숨기고 싶다면 `callSilently` 메서드를 사용하세요. 시그니처는 `call` 메서드와 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제에서는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 운영체제가 프로그램에 종료를 요청하는 방식입니다. Artisan 콘솔 명령어에서 시그널을 감지하고 추가 동작을 수행하려면 `trap` 메서드를 활용하세요:

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

여러 개의 시그널을 동시에 감지하고 싶다면 배열로 `trap` 메서드에 전달하면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이즈

Artisan 콘솔의 `make` 명령어들은 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 "스텁(stub)" 파일을 사용해 클래스를 만듭니다. 이러한 스텁 파일에 일부 변경을 가하고 싶다면, `stub:publish` 명령어를 사용해 필요한 스텁 파일을 애플리케이션에 퍼블리시(publish) 할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 스텁 파일을 수정하면, Artisan의 `make` 명령어로 생성되는 해당 클래스에 변경 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 실행되자마자 발생하며, 그 다음에는 커맨드가 실행되기 직전에 `CommandStarting` 이벤트가, 마지막으로 커맨드 실행이 끝나면 `CommandFinished` 이벤트가 발생합니다.
