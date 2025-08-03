# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [분리 가능한 명령어](#isolatable-commands)
- [입력 기대값 정의하기](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [입력 누락 시 프롬프트 표시하기](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력 값 가져오기](#retrieving-input)
    - [입력 프롬프트 띄우기](#prompting-for-input)
    - [출력 쓰기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [프로그래밍 방식으로 명령어 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 커맨드 라인 인터페이스입니다. Artisan은 애플리케이션의 루트에 있는 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움이 되는 여러 유용한 명령어들을 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용하세요:

```shell
php artisan list
```

모든 명령어는 또한 사용 가능한 인수와 옵션을 보여주고 설명하는 "도움말" 화면을 포함합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/12.x/sail)을 사용하고 있다면, Artisan 명령어를 호출할 때 반드시 `sail` 명령어 라인을 사용해야 한다는 점을 기억하세요. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 Laravel 프레임워크용 강력한 REPL(Read–Eval–Print Loop)입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 애플리케이션에서 Tinker를 제거했다면, Composer를 사용하여 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 멀티라인 코드 편집, 자동완성 기능을 원하면 [Tinkerwell](https://tinkerwell.app)을 확인하세요!

<a name="usage"></a>
#### 사용법

Tinker는 명령줄에서 Eloquent 모델, 잡, 이벤트 등 애플리케이션 전반과 상호작용할 수 있도록 해줍니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령어를 사용해 Tinker 설정 파일을 배포할 수도 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker를 사용할 때는 작업을 디스패치할 때 `Bus::dispatch`나 `Queue::push`를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 실행 허용 명령어 리스트

Tinker는 셸 내에서 실행할 수 있는 Artisan 명령어를 결정하기 위해 "allow" 리스트를 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 추가로 허용할 명령어가 있다면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭 처리 제외 클래스

보통 Tinker는 사용자가 상호작용하는 클래스에 대해 자동으로 별칭을 생성합니다. 하지만 특정 클래스에 대해서는 별칭을 생성하지 않도록 지정할 수도 있습니다. `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 나열하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan이 기본 제공하는 명령어 외에, 직접 사용자 정의 명령어를 작성할 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 저장하지만, Laravel에 [다른 디렉터리도 Artisan 명령어로 스캔하도록](#registering-commands) 지시하면 원하는 위치에 저장할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새 명령어를 생성하려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 생성합니다. 만약 해당 디렉터리가 없다면, `make:command`를 처음 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성을 적절하게 정의해야 합니다. 이 속성들은 명령어가 `list` 화면에 보여질 때 사용됩니다. `signature`는 [명령어 입력 기대값](#defining-input-expectations)을 정의할 때도 사용됩니다. 그리고 명령어가 실행될 때 `handle` 메서드가 호출되며, 이 메서드에 명령어 로직을 작성하면 됩니다.

아래는 예시 명령어입니다. `handle` 메서드에서 필요한 의존성을 주입받을 수 있음을 참고하세요. Laravel [서비스 컨테이너](/docs/12.x/container)가 메서드 시그니처에 타입힌트를 달아둔 모든 의존성을 자동으로 주입해줍니다:

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
> 코드 재사용성을 높이기 위해, 콘솔 명령어는 가급적 가볍게 유지하고 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋은 습관입니다. 위 예시에서 서비스 클래스를 주입받아 이메일 발송 작업의 핵심 처리를 위임한 것을 주목하세요.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 성공적으로 실행되면 종료 코드는 `0`으로 간주되어 성공을 의미합니다. 하지만 `handle` 메서드는 필요에 따라 정수형 값을 반환해 명령어의 종료 코드를 직접 지정할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내 어디서든 실패 처리를 하고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령어 실행을 중단하고 종료 코드 `1`을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스 대신 간단한 클로저 함수를 정의하는 대안입니다. 라우트 클로저가 컨트롤러 대안인 것처럼, 클로저 명령어도 커맨드 클래스 대체 수단으로 생각할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션의 콘솔 접근 경로(라우트)를 정의합니다. 이 파일에서 `Artisan::command` 메서드로 모든 클로저 명령어를 정의할 수 있습니다. `command` 메서드는 두 개의 인수를 받는데, 첫 번째는 [명령어 시그니처](#defining-input-expectations)이고, 두 번째는 명령어 인수와 옵션을 받는 클로저입니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 실제 명령어 인스턴스에 바인딩되므로, 일반 명령어 클래스에서 사용 가능한 모든 헬퍼 메서드에 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

클로저 명령어는 인수와 옵션을 받을 뿐 아니라, [서비스 컨테이너](/docs/12.x/container)를 통해 요청된 추가 의존성도 타입힌팅으로 주입받을 수 있습니다:

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

클로저 명령어를 정의할 때 `purpose` 메서드를 이용해 명령어 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 실행 시 출력됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 분리 가능한 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션에서 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

때로 하나의 명령어 인스턴스만 동시에 실행되도록 제한하고 싶을 수 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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

`Isolatable`로 표시된 명령어는 명령어 옵션에 자동으로 `--isolated`가 추가됩니다. 이 옵션과 함께 명령어를 실행하면, Laravel은 동일 명령어가 이미 실행 중인 경우 해당 명령어 실행을 막습니다. 실행 제한 시에도 명령어는 성공 종료 코드로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

원하지 않은 실행 시 반환할 종료 코드를 지정하려면 `isolated` 옵션에 값을 넣으면 됩니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어 이름을 사용해 캐시에서 원자 락을 위한 키 문자열을 생성합니다. 필요한 경우 명령어 클래스에 `isolatableId` 메서드를 정의하여 인수나 옵션을 키에 포함시킬 수 있습니다:

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

기본적으로 락은 명령어 실행이 끝나면 만료됩니다. 만약 명령어가 중간에 중단된다면 락은 1시간 후에 자동 만료됩니다. 락 만료 시간을 커스터마이징하려면 명령어에 `isolationLockExpiresAt` 메서드를 구현하세요:

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
## 입력 기대값 정의하기

콘솔 명령어를 작성할 때, 보통 사용자로부터 인수(argument) 또는 옵션(option) 형태로 입력을 받습니다. Laravel은 명령어 클래스의 `signature` 속성을 통해 사용자가 입력해야 할 값을 편리하고 간결한 라우트 유사 문법으로 정의할 수 있게 합니다.

<a name="arguments"></a>
### 인수

사용자 입력 인수와 옵션은 중괄호 `{}`로 묶습니다. 다음 예시는 반드시 받아야 할 필수 인수 `user`를 정의합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택사항으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션은 인수와 유사한 사용자 입력 형태이며, 커맨드라인에서 전달할 때는 두 개의 하이픈(`--`)을 접두어로 붙입니다. 옵션 종류는 값이 필요한 것과 필요 없는 두 가지로 나뉩니다. 값이 없는 옵션은 불리언 스위치 역할을 합니다. 예시를 보겠습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

`--queue` 스위치가 명령어 실행 시 포함되면 옵션 값은 `true`가 되고, 포함하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 받아야 하는 옵션을 정의하려면 옵션 이름 끝에 `=`를 붙여야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

사용자는 다음과 같이 옵션에 값을 전달할 수 있습니다. 옵션이 명령어 실행 시 지정되지 않으면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에도 기본값을 지정할 수 있습니다. 사용자가 값을 제공하지 않으면 기본값을 사용합니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 정의 시 단축키를 지정하려면, 옵션 이름 앞에 단축 키를 쓰고 `|`로 구분합니다:

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 옵션 단축키를 사용할 때는 단일 하이픈을 붙이고, 값 지정 시 `=`는 사용하지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 값을 받는 인수나 옵션을 정의하려면 `*` 문자를 사용합니다. 먼저 인수가 여러 개 올 수 있음을 나타내는 예:

```php
'mail:send {user*}'
```

이 명령어를 실행할 때, `user` 인수를 여러 개 순서대로 전달할 수 있습니다. 예를 들어 아래 명령어는 `user` 인수에 `[1, 2]` 배열이 전달됩니다:

```shell
php artisan mail:send 1 2
```

`*`문자는 선택적 인수와도 함께 쓸 수 있어 0개 이상의 인수를 받도록 할 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받을 옵션은 각 값을 옵션 이름 앞에 붙여 여러 번 전달합니다:

```php
'mail:send {--id=*}'
```

아래 명령어처럼 여러 번 `--id` 옵션을 전달할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수와 옵션에 설명을 붙이려면 이름과 설명 사이를 콜론 `:`으로 구분합니다. 긴 내용을 작성해야 할 땐 여러 줄로 나누어 작성할 수 있습니다:

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
### 입력 누락 시 프롬프트 표시하기

필수 인수를 입력하지 않으면 에러가 발생합니다. 그러나 `PromptsForMissingInput` 인터페이스를 구현하면, 누락된 필수 인수가 있을 때 자동으로 사용자에게 질문하여 값을 받을 수 있습니다:

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

Laravel은 누락된 인수가 있으면 인수 이름이나 설명을 바탕으로 적절한 질문을 자동 생성해 사용자에게 묻습니다. 질문을 커스터마이즈하려면 `promptForMissingArgumentsUsing` 메서드를 구현해 인수명별로 질문 배열을 반환하세요:

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

다음과 같이 질문과 플레이스홀더 텍스트를 튜플로 함께 제공할 수도 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 동작을 완전히 제어하려면 클로저를 제공해 사용자에게 질문을 띄우고 답변을 반환하도록 구현할 수 있습니다:

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
> 자세한 내용은 [Laravel Prompts](/docs/12.x/prompts) 문서를 참고하세요.

옵션에 대해 사용자에게 선택 또는 입력 프롬프트를 띄우려면, 명령어 `handle` 메서드 내에 코드를 추가하거나, 누락 인수 입력 프롬프트 이후에만 작동하도록 하려면 `afterPromptingForMissingArguments` 메서드를 구현하세요:

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
## 명령어 입출력

<a name="retrieving-input"></a>
### 입력 값 가져오기

명령어 실행 중 인수와 옵션 값을 가져와야 할 때, `argument`와 `option` 메서드를 사용하세요. 존재하지 않는 인수나 옵션은 `null`을 반환합니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 받고 싶으면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 메서드로 특정 옵션 값을, `options` 메서드로 모든 옵션을 배열로 받을 수 있습니다:

```php
// 특정 옵션 값 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트 띄우기

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가하는 PHP 패키지로, 플레이스홀더 텍스트와 유효성 검사 등 브라우저 스타일의 기능을 제공합니다.

출력을 보여주는 것 외에도, 명령어 실행 중 사용자 입력을 요청할 수 있습니다. `ask` 메서드는 질문을 출력하고 사용자의 입력을 받으며, 입력값을 반환합니다:

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

`ask` 메서드는 두 번째 인수로 기본값을 정할 수도 있습니다. 사용자가 아무 입력도 하지 않으면 이 기본값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 입력 내용을 화면에 표시하지 않습니다. 비밀번호 등 민감한 정보를 받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청

간단한 예/아니오 질문을 할 때는 `confirm` 메서드를 사용하세요. 기본 반환값은 `false`이며, 사용자가 `y` 또는 `yes`라고 입력하면 `true`를 반환합니다:

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 `true`로 바꾸려면 두 번째 인자로 `true`를 넘기면 됩니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드는 가능한 답변 목록을 제시해 자동완성을 지원합니다. 사용자는 목록 이외의 답변도 자유롭게 할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 전달해, 사용자가 입력할 때마다 실시간으로 자동완성 후보를 반환하도록 할 수 있습니다:

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

사용자에게 미리 정의된 선택지 목록을 보여주려면 `choice` 메서드를 사용하세요. 기본값 인덱스를 세 번째 인수로 전달할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

추가로 네 번째, 다섯 번째 인수로 최대 선택 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

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
### 출력 쓰기

콘솔에 출력을 보낼 때는 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드들을 사용하세요. 각 메서드는 용도에 맞는 ANSI 컬러를 적용해 출력합니다. 예를 들어 사용자에게 일반 정보를 보여줄 땐 보통 녹색으로 출력되는 `info` 메서드를 사용합니다:

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

오류 메시지는 보통 붉은색으로 표시되는 `error` 메서드로 출력합니다:

```php
$this->error('Something went wrong!');
```

`line` 메서드는 컬러 없이 단순한 텍스트를 출력할 때 사용합니다:

```php
$this->line('Display this on the screen');
```

`newLine` 메서드는 빈 줄을 출력합니다:

```php
// 빈 줄 한 줄 출력...
$this->newLine();

// 빈 줄 세 줄 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드는 여러 행과 열로 된 데이터를 깔끔하게 표 형태로 출력해줍니다. 컬럼명과 데이터 배열만 넘겨주면, Laravel이 자동으로 테이블 크기를 조절합니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

오래 걸리는 작업 시 진행 상태를 표시하면 유용합니다. `withProgressBar` 메서드에 반복 가능한 객체와 각 반복마다 실행할 콜백을 넘기면 진행 바가 표시됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행 바 업데이트를 수동으로 제어해야 하는 경우, 전체 단계 수를 지정해 진행 바를 생성하고 각 반복에서 직접 진행 바를 갱신하면 됩니다:

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
> 고급 설정에 대해서는 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

기본적으로 Laravel은 `app/Console/Commands` 디렉터리 내 모든 명령어를 자동으로 등록합니다. 하지만 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용해 다른 디렉터리를 Artisan 명령어 스캔 대상으로 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면 명령어 클래스를 직접 `withCommands` 메서드에 지정해 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅할 때 애플리케이션 내 모든 명령어가 [서비스 컨테이너](/docs/12.x/container)를 통해 해석되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식으로 명령어 실행하기

명령어를 CLI 외에서 실행하고 싶을 때도 있습니다. 예를 들어 라우트나 컨트롤러에서 Artisan 명령어를 실행할 수 있습니다. `Artisan` 페사드의 `call` 메서드를 사용하세요. 이 메서드는 첫 번째 인수로 명령어 시그니처 또는 클래스 이름을 받고, 두 번째 인수로 명령어 매개변수 배열을 받습니다. 종료 코드는 반환됩니다:

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

전체 명령어를 문자열로 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

명령어 옵션이 배열을 받도록 정의되어 있다면, 배열을 넘겨 여러 값을 전달할 수 있습니다:

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
#### 불리언 값 전달하기

`migrate:refresh` 명령어의 `--force` 플래그처럼 문자열 값을 받지 않는 옵션에는 `true` 또는 `false` 불리언 값을 전달해야 합니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉하기

`Artisan` 페사드의 `queue` 메서드를 사용하면 Artisan 명령어를 백그라운드에서 [큐 워커](/docs/12.x/queues)로 처리하도록 큐잉할 수 있습니다. 이 기능을 사용하기 전에 큐를 설정하고 큐 리스너가 실행 중인지 확인하세요:

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

`onConnection`과 `onQueue` 메서드를 사용해 Artisan 명령어를 보낼 큐 커넥션과 큐 이름을 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

기존 Artisan 명령어에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용하세요. 이 메서드는 호출할 명령어 이름과 인수/옵션 배열을 받습니다:

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

다른 명령어 출력 없이 조용히 호출하려면 `callSilently` 메서드를 쓰면 됩니다. 사용법은 `call` 메서드와 같습니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램 종료 요청 시그널입니다. Artisan 콘솔 명령어에서 시그널을 감지해 특정 코드를 실행하고 싶다면 `trap` 메서드를 사용하세요:

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

여러 시그널을 동시에 처리할 때는 시그널 배열을 넘기면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan의 `make` 명령어들은 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 사용자의 입력에 따라 값들이 채워지는 "스텁(stub)" 파일을 기반으로 생성됩니다. 그러나 Artisan이 생성하는 파일을 조금 수정하고 싶을 때도 있죠. 이럴 때는 `stub:publish` 명령어를 사용해 가장 자주 쓰이는 스텁을 애플리케이션 내에 배포할 수 있습니다:

```shell
php artisan stub:publish
```

배포된 스텁은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 파일을 수정하면, Artisan의 `make` 명령어로 생성하는 해당 클래스들에 변경 사항이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, 그리고 `Illuminate\Console\Events\CommandFinished`. 

- `ArtisanStarting`: Artisan 실행이 시작되자마자 발생합니다.
- `CommandStarting`: 명령어가 실행되기 직전에 발생합니다.
- `CommandFinished`: 명령어 실행이 완료된 후 발생합니다.