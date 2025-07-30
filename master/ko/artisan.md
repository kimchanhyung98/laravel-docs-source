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
    - [누락된 입력에 대해 프롬프트 표시하기](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력 받기](#retrieving-input)
    - [입력 프롬프트](#prompting-for-input)
    - [출력 쓰기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [프로그래밍적으로 명령어 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 기본으로 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트에 위치한 `artisan` 스크립트이며, 애플리케이션을 개발하는 동안 유용한 여러 명령어를 제공합니다. 모든 사용 가능한 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 해당 명령어의 인수와 옵션을 설명하는 "도움말" 화면도 포함되어 있습니다. 도움말을 보려면 `help` 다음에 명령어 이름을 입력하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/master/sail)을 사용하는 경우, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 한다는 점을 기억하세요. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 강력한 Laravel 프레임워크용 REPL(Read-Eval-Print Loop) 도구입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션은 기본적으로 Tinker를 포함합니다. 하지만 애플리케이션에서 Tinker를 삭제했었다면 Composer로 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> 라라벨 애플리케이션과 상호작용할 때 핫 리로드, 멀티라인 코드 편집, 자동 완성 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 명령줄에서 Eloquent 모델, 작업(Job), 이벤트 등 Laravel 애플리케이션 전체와 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령어로 Tinker 구성 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업(Job)을 큐에 넣을 때 가비지 컬렉션에 의존합니다. 따라서 Tinker를 사용할 때는 `Bus::dispatch` 또는 `Queue::push`를 사용해서 작업을 디스패치하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 허용 명령어 리스트

Tinker는 내부에서 실행을 허용할 Artisan 명령어의 "허용" 리스트를 사용합니다. 기본적으로는 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 해당 명령어를 추가하세요:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭(alias)을 생성하지 않을 클래스

Tinker는 일반적으로 상호작용하는 클래스에 대해 자동으로 별칭(alias)을 생성합니다. 그러나 일부 클래스에 대해서는 별칭을 만들지 않으려면, `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 명시하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan에서 제공하는 명령어 외에도, 커스텀 명령어를 직접 작성할 수 있습니다. 보통 명령어는 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 로드할 수 있다면 위치는 자유롭게 선택할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 명령어 클래스를 생성합니다. 만약 이 디렉터리가 없다면, `make:command` 명령어를 처음 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성을 적절히 정의해야 합니다. 이 값들은 명령어 목록 화면에서 사용되며, `signature` 속성은 [명령어 입력 기대값](#defining-input-expectations)을 정의하는 데도 활용됩니다. 명령어 실행 시 `handle` 메서드가 호출되므로 실행 로직을 이곳에 작성합니다.

예시 명령어를 살펴보겠습니다. `handle` 메서드에서 필요한 의존성은 메서드 시그니처에 타입힌트를 지정하면 Laravel 서비스 컨테이너가 자동으로 주입해 줍니다:

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
> 명령어를 가볍게 유지하고, 실제 작업 처리는 애플리케이션 서비스에 위임하는 것이 더 재사용성이 높습니다. 위 예시에서는 이메일 발송의 '무거운 작업'을 서비스 클래스로 분리하여 주입하는 방식을 보여줍니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드가 아무 값도 반환하지 않고 정상적으로 실행이 완료되면, 명령어는 성공을 의미하는 `0` 종료 코드로 종료됩니다. 필요하면 정수형 값을 반환하여 종료 코드를 직접 지정할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내 어느 위치에서든, 실패 처리를 하려면 `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어 실행을 멈추고 종료 코드 `1`을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저(Closure) 기반 명령어는 클래스로 콘솔 명령어를 정의하는 대안입니다. 라우트의 클로저가 컨트롤러의 대안인 것처럼 생각하면 됩니다.

`routes/console.php` 파일에는 HTTP 라우트 대신 콘솔 기반 진입점을 정의합니다. 여기에서 `Artisan::command` 메서드를 사용해 클로저 명령어를 정의할 수 있습니다. 이 메서드는 두 개의 인수, 즉 [명령어 시그니처](#defining-input-expectations)와 명령어 인수 및 옵션을 받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 실제 명령어 인스턴스에 바인딩되어 있어서, 전체 명령어 클래스에서 사용할 수 있는 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

명령어 인수와 옵션뿐 아니라, 클로저에 서비스 컨테이너에서 해결할 추가 의존성도 타입힌트로 받을 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 명령어를 정의할 때 `purpose` 메서드를 사용해 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어 실행 시 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 분리 가능한 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

동시에 하나의 명령어 인스턴스만 실행되도록 보장하고 싶을 때가 있습니다. 이 경우 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다:

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

`Isolatable`로 표시한 명령어는 자동으로 `--isolated` 옵션이 추가됩니다. 이 옵션과 함께 명령어를 실행하면, 해당 명령어의 다른 인스턴스가 실행 중인지 확인한 다음 실행합니다. 잠금은 애플리케이션 기본 캐시 드라이버를 사용해 원자적 락으로 수행합니다. 다른 인스턴스가 있다면 명령어는 실행되지 않지만, 명령어는 성공 종료 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어를 실행하지 못할 경우 반환할 종료 코드도 `--isolated` 옵션에 숫자 값을 지정해 설정할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 잠금 ID

기본적으로 Laravel은 명령어 이름을 이용해 캐시 잠금 키를 생성합니다. 그러나 `isolatableId` 메서드를 Artisan 명령어 클래스에 정의하면, 인수나 옵션을 조합해 잠금 키를 커스터마이징할 수 있습니다:

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
#### 잠금 만료 시간

기본적으로 잠금은 명령어가 끝나면 만료되고, 명령어가 중단될 경우 최대 1시간 후 만료됩니다. 잠금 만료 시간을 조정하려면 `isolationLockExpiresAt` 메서드를 명령어에 정의하세요:

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

콘솔 명령어 작성 시 유저로부터 인수(Arguments)나 옵션(Options)을 통해 입력을 받을 필요가 많습니다. Laravel은 명령어 클래스의 `signature` 속성으로 기대하는 입력을 매우 간편하게 정의할 수 있습니다. `signature`는 명령어 이름과 인수, 옵션을 하나의 경로(route) 느낌의 구문으로 표현합니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자가 제공하는 모든 인수와 옵션은 중괄호 `{}`로 감쌉니다. 아래 예시는 필수 인수를 하나 정의한 경우입니다: `user`

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택 사항으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 선택적 인수 + 기본값...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션은 인수와 마찬가지로 사용자 입력 방식의 하나입니다. 옵션은 명령줄에서 `--`를 두 개 붙여 접두합니다. 값 유무에 따라 두 가지 종류가 있습니다. 값이 없는 옵션은 boolean 스위치 역할을 하며 다음은 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서 `--queue` 옵션은 스위치 형태이며, 옵션을 명령어 호출 시 포함하면 값이 `true`가 되고, 없으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 받아야 하는 옵션은 옵션 이름 뒤에 `=`를 붙여 표현합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

명령어를 호출할 때 옵션에 값을 다음과 같이 전달할 수 있고, 전달하지 않은 경우에는 값이 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면, 기본값을 옵션 이름 뒤에 지정하세요. 값이 전달되지 않으면 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정하려면 옵션 이름 앞에 단축키를 두고 `|` 문자로 구분합니다:

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 단축키로 옵션을 사용할 때는 단일 하이픈 `-`을 붙이고, 값 지정 시 `=`는 생략합니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

인수나 옵션이 여러 값을 받을 수 있도록 설정하려면 `*` 문자를 사용할 수 있습니다. 다음은 다중 인수 예시입니다:

```php
'mail:send {user*}'
```

이 때 명령어 호출 시, `user` 인수는 순서대로 배열에 담깁니다. 예:

```shell
php artisan mail:send 1 2
```

`user` 인수는 `[1, 2]` 배열이 됩니다.

`*`는 선택적 인수와 조합할 수도 있습니다. 즉, 0개 이상의 인수를 받을 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

값이 여러 개인 옵션을 정의할 때는 각 값마다 옵션 이름을 붙여서 전달해야 합니다:

```php
'mail:send {--id=*}'
```

위 옵션을 사용하는 명령어 호출 예시:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수나 옵션에 대한 설명은 이름 옆에 콜론(`:`)으로 설명을 추가할 수 있습니다. 명령어 정의가 길어지는 경우, 여러 줄로 나누어 작성해도 됩니다:

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
### 누락된 입력에 대해 프롬프트 표시하기

필수 인수가 없을 때 기본적으로 오류 메시지가 출력됩니다. 그러나 `PromptsForMissingInput` 인터페이스를 구현하면 누락된 인수를 자동으로 프롬프트해 받을 수 있습니다:

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

Laravel이 누락된 인수를 사용자에게 물어볼 때, 인수 이름이나 설명을 이용해 질문을 자동으로 만듭니다. 질문을 커스터마이징하려면 `promptForMissingArgumentsUsing` 메서드를 구현해 인수명별 질문 목록을 반환합니다:

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

질문에 플레이스홀더를 더하고 싶다면, 질문과 플레이스홀더를 배열로 반환하세요:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

직접 프롬프트 동작을 제어하고 싶다면 클로저를 반환할 수도 있습니다:

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
> 더 상세한 프롬프트 사용법은 [Laravel Prompts](/docs/master/prompts) 문서를 참고하세요.

필요 시 [옵션](#options)도 프롬프트할 수 있으며, 명령어 `handle` 메서드 내에서 프롬프트하거나 `afterPromptingForMissingArguments` 메서드를 구현해 인수 프롬프트 후에 실행할 로직을 작성할 수 있습니다:

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
### 입력 받기

명령어 실행 중 인수와 옵션 값을 읽어야 하는 경우가 있습니다. 이 때 `argument`와 `option` 메서드를 사용할 수 있습니다. 존재하지 않는 키를 요청하면 `null`이 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열 형태로 한꺼번에 받아오려면 `arguments` 메서드를, 모든 옵션을 배열로 받으려면 `options` 메서드를 사용하면 됩니다:

```php
$arguments = $this->arguments();

// 특정 옵션 가져오기
$queueName = $this->option('queue');

// 모든 옵션 배열로 가져오기
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/master/prompts)는 콘솔 애플리케이션에 아름다운 사용자 입력 폼을 추가하는 PHP 패키지로, 플레이스홀더, 유효성 검사 등 브라우저에 가까운 기능을 제공합니다.

명령어 실행 도중 사용자에게 입력을 물어볼 수도 있습니다. `ask` 메서드는 질문을 출력하고 답변을 받습니다:

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

`ask` 메서드는 두 번째 인자로 기본값도 받습니다. 사용자가 아무 입력을 하지 않으면 기본값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만 입력 값이 입력 중에 화면에 표시되지 않습니다. 비밀번호 같은 민감한 정보를 받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청

간단한 예/아니오 확인이 필요하면 `confirm` 메서드를 사용할 수 있습니다. 기본값은 `false`이고, `y` 또는 `yes` 입력 시 `true`를 반환합니다:

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요하면 두 번째 인자로 기본이 `true`가 되도록 지정할 수도 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 입력 가능한 값의 자동완성 힌트를 제공합니다. 사용자가 이 힌트에 상관없이 자유롭게 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 클로저를 두 번째 인자로 제공해, 사용자가 입력할 때마다 입력값에 근거한 자동완성 목록을 반환할 수도 있습니다:

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

미리 정해진 선택지 중에서 고르게 하려면 `choice` 메서드가 유용합니다. 세 번째 인자로 기본 선택지의 배열 인덱스를 지정할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째, 다섯 번째 인자로 유효 응답 선택 시도 횟수 제한과 복수 선택 가능 여부를 줄 수도 있습니다:

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

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용하세요. 각각 목적에 따른 ANSI 색상을 자동으로 입혀 줍니다. 예를 들어, 일반적인 정보를 출력하려면 `info`를 사용하면 초록색으로 표시됩니다:

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

에러 메시지를 출력할 때는 `error` 메서드를 사용하며, 보통 빨간색 텍스트로 출력됩니다:

```php
$this->error('Something went wrong!');
```

단순한 무채색 텍스트는 `line`을 사용하세요:

```php
$this->line('Display this on the screen');
```

빈 줄을 출력하려면 `newLine` 메서드를 사용합니다:

```php
// 한 줄 띄우기
$this->newLine();

// 세 줄 띄우기
$this->newLine(3);
```

<a name="tables"></a>
#### 표 출력

`table` 메서드는 여러 행과 열로 구성된 데이터를 깔끔하게 표 형태로 출력할 수 있게 해줍니다. 열 이름과 데이터를 배열로 전달하면 Laravel이 표의 폭과 높이를 자동으로 계산해줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄

오랜 시간 걸리는 작업에서는 진행률 표시줄로 현재 진행 상황을 알려주는 것이 좋습니다. `withProgressBar` 메서드는 반복 가능한 값의 각 이터레이션마다 자동으로 진행률을 갱신해 줍니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 세밀한 제어가 필요하다면, 전체 반복 횟수를 지정하고 직접 진행률을 갱신할 수도 있습니다:

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
> 더 고급 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

기본적으로 Laravel은 `app/Console/Commands` 디렉터리 내 모든 명령어를 자동 등록합니다. 하지만, 필요 시 다른 경로를 `bootstrap/app.php`의 `withCommands` 메서드로 추가해 스캔할 수도 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

또는 명령어 클래스명을 배열로 직접 전달해 수동 등록도 가능합니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

애플리케이션 시작 시 모든 명령어는 서비스 컨테이너를 통해 해결되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍적으로 명령어 실행하기

CLI 외부에서 Artisan 명령어를 실행하려는 경우도 있습니다. 예를 들어, 라우트나 컨트롤러에서 명령어를 실행할 수 있습니다. `Artisan` 파사드의 `call` 메서드를 사용하세요. 첫 번째 인자는 명령어 시그니처 혹은 클래스명, 두 번째는 인수 및 옵션 배열입니다. 종료 코드를 반환합니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

명령어 전체를 문자열로도 넘길 수 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

옵션이 배열을 기대할 경우, 배열 형태로 값을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달하기

`migrate:refresh` 명령어의 `--force` 플래그처럼, 문자열 값을 허용하지 않는 옵션은 `true` 또는 `false`로 전달하세요:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 백그라운드 큐 작업으로 보낼 수 있습니다. 이 기능을 쓰려면 큐 설정과 큐 리스너가 실행 중이어야 합니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`과 `onQueue` 메서드를 이용해 연결과 큐를 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

한 명령어 내에서 다른 명령어를 호출하고 싶을 때 `call` 메서드를 사용하세요. 명령어 이름과 인수 및 옵션 배열을 인자로 받습니다:

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

출력을 숨기고 싶다면 `callSilently` 메서드를 사용하세요. 인터페이스는 `call`과 같습니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 종료 요청 시그널입니다. Artisan 명령어에서 이 시그널을 감지해 처리하려면 `trap` 메서드를 사용하세요:

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

여러 시그널을 한 번에 감지할 수도 있습니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan의 `make` 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 클래스 등 다양한 클래스를 생성합니다. 이 클래스들은 스텁(stub) 파일을 바탕으로 만들어집니다. 생성되는 파일을 조금 수정하고 싶다면 `stub:publish` 명령어로 주요 스텁 파일을 애플리케이션에 퍼블리시해 커스터마이징할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉터리에 위치하며, 수정한 내용은 해당 스텁을 사용하는 `make` 명령어 실행 시 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 3가지 이벤트를 디스패치합니다:  
`Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.

`ArtisanStarting` 이벤트는 Artisan이 실행되자마자 발생하며,  
`CommandStarting` 이벤트는 명령어가 실행되기 직전,  
`CommandFinished` 이벤트는 명령어 실행이 끝난 후 발생합니다.