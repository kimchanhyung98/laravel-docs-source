# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [커맨드 작성하기](#writing-commands)
    - [커맨드 생성하기](#generating-commands)
    - [커맨드 구조](#command-structure)
    - [클로저 커맨드](#closure-commands)
    - [동시 실행 방지 커맨드](#isolatable-commands)
- [입력값 정의하기](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [배열 입력값](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력값에 대해 사용자에게 질문하기](#prompting-for-missing-input)
- [커맨드 입출력](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 요청하기](#prompting-for-input)
    - [출력하기](#writing-output)
- [커맨드 등록하기](#registering-commands)
- [프로그래밍 방식으로 커맨드 실행하기](#programmatically-executing-commands)
    - [다른 커맨드에서 커맨드 호출하기](#calling-commands-from-other-commands)
- [신호 처리](#signal-handling)
- [스텁(stub) 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 커맨드 라인 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션 개발에 도움이 되는 다양한 유용한 명령어들을 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어는 사용 가능한 인수와 옵션을 보여주는 "도움말" 화면을 포함합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/11.x/sail)을 사용하는 경우에는 Artisan 명령어를 실행할 때 `sail` 커맨드를 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 강력한 Laravel 프레임워크용 REPL(대화형 쉘)입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 삭제했다면 Composer를 사용하여 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]  
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 다중 행 코드 편집, 자동완성을 원한다면 [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 Eloquent 모델, 잡, 이벤트 등 애플리케이션 내 모든 기능과 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker 설정파일은 `vendor:publish` 명령어를 사용해 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]  
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업 큐에 작업을 넣기 위해 가비지 컬렉션에 의존합니다. 때문에 tinker에서는 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 권장됩니다.

<a name="command-allow-list"></a>
#### 실행 허용 커맨드 목록

Tinker는 쉘 내에서 실행 가능한 Artisan 명령어를 제한하는 "허용" 리스트를 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 추가로 명령어를 허용하려면 `tinker.php` 설정파일의 `commands` 배열에 추가하세요:

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 만들지 않을 클래스

보통 Tinker는 클래스에 접근할 때 자동으로 별칭(alias)을 만듭니다. 하지만 특정 클래스에 대해서는 별칭 생성을 원치 않을 수 있습니다. 이 경우 `tinker.php` 설정파일의 `dont_alias` 배열에 클래스를 추가하면 됩니다:

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 커맨드 작성하기

Artisan에서 제공하는 명령어 외에도 직접 커스텀 명령어를 만들 수 있습니다. 기본적으로 커맨드는 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 로드할 수 있다면 원하는 위치를 자유롭게 선택할 수 있습니다.

<a name="generating-commands"></a>
### 커맨드 생성하기

새 커맨드를 만들려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 새 커맨드 클래스를 생성합니다. 만약 해당 디렉터리가 없으면 처음 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 커맨드 구조

커맨드가 생성되면 클래스의 `signature`와 `description` 속성에 적절한 값을 지정해야 합니다. 이 값들은 `list` 화면에 명령어를 표시할 때 사용됩니다. `signature` 속성을 통해 [커맨드 입력값](#defining-input-expectations)도 정의할 수 있습니다. 커맨드가 실행될 때 호출되는 `handle` 메소드에 커맨드 로직을 작성합니다.

다음은 예시 커맨드입니다. `handle` 메소드 내에서 필요한 의존성은 서비스 컨테이너가 자동으로 주입합니다:

```
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
> 콘솔 명령어는 가능한 가볍게 유지하고, 작업 수행은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예시에서 이메일 발송 기능은 별도의 서비스 클래스에 위임된 것을 참고하세요.

<a name="exit-codes"></a>
#### 종료 코드 (Exit Codes)

`handle` 메소드에서 아무 값도 반환하지 않고 명령어가 성공적으로 실행되면, 종료 코드는 성공을 나타내는 `0`이 됩니다. 그러나 정수 값을 반환해 직접 종료 코드를 지정할 수도 있습니다:

```
$this->error('Something went wrong.');

return 1;
```

명령어 실행 도중 실패 처리를 즉시 하고 싶으면 `fail` 메소드를 사용할 수 있습니다. 이는 즉시 명령어 실행을 중단하고 종료 코드 `1`을 반환합니다:

```
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 커맨드

클래스 대신 클로저(익명 함수)로 커맨드를 정의하는 방법도 있습니다. 라우트 클로저가 컨트롤러의 대안인 것처럼, 커맨드 클로저는 커맨드 클래스의 대안입니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션 내 콘솔 진입점을 정의합니다. 여기서 `Artisan::command` 메서드로 모든 클로저 기반 Artisan 커맨드를 정의할 수 있습니다. 이 메서드는 [커맨드 시그니처](#defining-input-expectations)와 클로저 두 개의 인수를 받습니다:

```
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 기본 커맨드 인스턴스에 바인딩되어 있어, 커맨드 클래스에서 쓰던 모든 도움 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

커맨드 인수 외에도, 서비스 컨테이너에서 자동 주입받을 의존성을 클로저 인수로 타입힌팅할 수 있습니다:

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 커맨드 설명

클로저 커맨드에 설명을 붙이려면 `purpose` 메서드를 사용하세요. 설명은 `php artisan list` 또는 `php artisan help` 명령어 실행 시 표시됩니다:

```
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 동시 실행 방지 커맨드 (Isolatable Commands)

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

동시에 같은 커맨드 인스턴스가 여러 개 실행되는 것을 막고 싶을 때가 있습니다. 이때 커맨드 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

`Isolatable` 인터페이스가 구현된 커맨드는 자동으로 `--isolated` 옵션이 추가됩니다. 이 옵션과 함께 실행하면, Laravel은 기본 캐시 드라이버를 통한 원자적 락을 시도하여 이미 실행 중인 다른 인스턴스가 있으면 실행하지 않습니다. 이 경우에도 명령어는 성공 종료 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

실행 불가능할 때 반환할 종료 코드를 지정하고 싶으면 `--isolated` 옵션에 값을 넣어 실행하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 식별자 (Lock ID)

기본적으로 Laravel은 커맨드 이름을 락의 키로 사용합니다. 하지만 `isolatableId` 메서드를 정의해, 명령어 인수나 옵션을 사용한 맞춤 락 키를 만들 수 있습니다:

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

기본적으로 락은 커맨드 종료 시 만료되고, 만약 강제 종료되면 1시간 후에 만료됩니다. `isolationLockExpiresAt` 메서드를 정의해 만료 시간을 커스터마이징할 수 있습니다:

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
## 입력값 정의하기

콘솔 커맨드 작성 시 사용자가 입력할 인수나 옵션을 받는 게 일반적입니다. Laravel은 커맨드의 `signature` 속성을 통해 기대하는 입력값을 편리하게 정의할 수 있습니다. `signature`는 라우트와 비슷한 문법으로 명령어 이름, 인수, 옵션을 한 번에 지정합니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자 입력 인수와 옵션은 중괄호 `{}`로 감싸서 정의합니다. 아래 예시는 필수 인수 `user`를 정의한 경우입니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택사항으로 만들거나 기본값을 지정할 수도 있습니다:

```
// 선택적 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션은 인수와 마찬가지로 입력의 한 형태이며, 명령줄에서 두 개의 하이픈(`--`)으로 시작합니다. 값이 없는 옵션(스위치)과 값을 받는 옵션 두 가지가 있습니다. 예를 들어 값이 없는 옵션은 불리언 스위치 역할을 합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

`--queue` 스위치가 있으면 값은 `true`, 없으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값을 받는 옵션

값이 필요한 옵션은 이름 뒤에 `=`를 붙여 표시합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

사용자는 다음처럼 옵션 값과 함께 명령어를 호출할 수 있습니다. 옵션이 지정되지 않으면 값은 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정할 수도 있습니다:

```
'mail:send {user} {--queue=default}'
```

옵션 값이 없으면 기본값이 사용됩니다.

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정하려면 `|` 구분자로 단축 이름을 접두어로 구분해 작성하세요:

```
'mail:send {user} {--Q|queue}'
```

터미널에서 단축키는 단일 하이픈(`-`)으로 시작하고, 값 지정시 `=`를 넣지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 배열 입력값

한 개 이상의 값을 받는 인수 또는 옵션을 정의하려면 `*` 문자를 사용합니다. 다음은 다중 인수 예시입니다:

```
'mail:send {user*}'
```

명령어 실행 시 `user` 인수들을 순서대로 전달할 수 있습니다. 예를 들어 아래는 `user`가 `[1, 2]` 배열로 해석됩니다:

```shell
php artisan mail:send 1 2
```

`*`와 선택적 인수를 함께 사용하면 0개 이상의 값이 허용됩니다:

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 배열 옵션

여러 값을 받는 옵션은 이름을 반복해 각각 전달합니다:

```
'mail:send {--id=*}'
```

아래처럼 여러 `--id` 옵션을 명령어에 전달하세요:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수와 옵션에 설명을 붙이려면 이름 뒤에 콜론을 넣고 설명을 작성하세요. 긴 정의가 필요하면 여러 줄로 나누어도 됩니다:

```
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
### 누락된 입력값에 대해 사용자에게 질문하기

필수 인수가 주어지지 않으면 기본적으로 오류가 발생합니다. 그러나 `PromptsForMissingInput` 인터페이스를 구현하면 누락된 인수가 있을 때 자동으로 사용자에게 질문할 수 있습니다:

```
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

Laravel은 인수 이름이나 설명을 바탕으로 지능적으로 질문을 만들어 사용자에게 묻습니다. 커스텀 질문을 만들려면 `promptForMissingArgumentsUsing` 메서드를 구현하고 인수 이름을 키로 한 질문 배열을 반환하세요:

```
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

자리 표시자(placeholder)를 넣으려면 질문과 placeholder가 포함된 튜플을 배열 값으로 사용하세요:

```
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

질문에 대한 완전한 제어가 필요하면, 사용자에게 질문하고 답변을 반환하는 클로저를 값으로 제공할 수 있습니다:

```
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
> 보다 자세한 프롬프트 사용법은 [Laravel Prompts](/docs/11.x/prompts) 문서를 참고하세요.

옵션에 대해 사용자 선택 또는 입력 유도를 하고 싶으면, 커맨드의 `handle` 메서드 내에서 프롬프트를 실행하세요. 다만 누락 인수 질문이 실행된 후에만 유도하고 싶으면 `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다:

```
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
## 커맨드 입출력

<a name="retrieving-input"></a>
### 입력값 가져오기

커맨드 실행 중 사용자가 입력한 인수와 옵션 값을 가져올 때는 `argument`와 `option` 메서드를 사용하세요. 존재하지 않는 인수나 옵션을 요청하면 `null`을 반환합니다:

```
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 가져오려면 `arguments` 메서드를 호출하세요:

```
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 메서드로 값을 가져오고, 모든 옵션 값을 배열로 얻으려면 `options` 메서드를 호출하면 됩니다:

```
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 요청하기

> [!NOTE]  
> [Laravel Prompts](/docs/11.x/prompts)는 콘솔 명령어에 플레이스홀더, 유효성 검사 같은 브라우저 느낌을 더한 폼을 추가하는 PHP 패키지입니다.

명령 실행 도중 사용자 입력을 요청할 수 있습니다. `ask` 메서드는 질문을 출력하고 입력값을 받아 반환합니다:

```
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

`ask` 메서드는 기본값을 두 번째 인수로 받을 수 있습니다. 입력값이 없을 때 기본값이 반환됩니다:

```
$name = $this->ask('What is your name?', 'Taylor');
```

입력값이 보이지 않게 하려면 `secret` 메서드를 사용하세요. 비밀번호같이 민감한 정보 입력에 적합합니다:

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청하기

사용자에게 "예/아니오" 질문을 할 때는 `confirm` 메서드를 사용합니다. 기본값은 `false`이며, 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다:

```
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 `true`로 설정하려면 두 번째 인수에 `true`를 전달하세요:

```
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드를 사용하면 사용자 입력에 대한 자동완성 기능을 제공합니다. 자동완성 힌트는 제안이므로 사용자가 다른 답변을 입력할 수도 있습니다:

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 클로저를 전달하여 입력값에 따른 동적인 제안을 할 수 있습니다:

```
$name = $this->anticipate('What is your address?', function (string $input) {
    // Return auto-completion options...
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택 질문

선택지를 미리 정의해 사용자에게 묻고 싶으면 `choice` 메서드를 사용하세요. 기본값 인덱스를 세 번째 인수로 전달합니다:

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

추가로 네 번째와 다섯 번째 인수로 최대 시도 횟수, 다중 선택 허용 여부를 지정할 수 있습니다:

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### 출력하기

콘솔에 출력할 때는 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용하세요. 각각 목적에 맞는 ANSI 색상이 적용됩니다. 예를 들어, 일반 정보는 `info` 메서드가 초록색으로 출력합니다:

```
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

오류 메시지는 `error` 메서드로 출력하며 일반적으로 빨간색으로 표시됩니다:

```
$this->error('Something went wrong!');
```

일반 텍스트(색상 없이)는 `line` 메서드를 사용합니다:

```
$this->line('Display this on the screen');
```

빈 줄 출력은 `newLine` 메서드를 사용합니다:

```
// 한 줄 빈 줄 출력...
$this->newLine();

// 세 줄 빈 줄 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드를 사용하면 여러 행과 열로 된 데이터를 쉽게 포맷할 수 있습니다. 컬럼 이름과 데이터를 배열 형태로 전달하면 Laravel이 자동으로 알맞은 너비와 높이로 테이블을 그립니다:

```
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 표시줄

긴 작업을 진행할 때는 `withProgressBar` 메서드를 사용해 진행률 바를 보여줄 수 있습니다. 지정한 반복 가능한 값의 각 항목마다 진행 상태가 갱신됩니다:

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 세밀한 컨트롤이 필요하면 진행 바를 직접 생성하고, 전체 단계 수를 지정한 뒤 각 작업 후에 진행 바를 수동으로 갱신할 수 있습니다:

```
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
> 더 자세한 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/7.0/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 커맨드 등록하기

Laravel은 기본적으로 `app/Console/Commands` 디렉터리 내 모든 커맨드를 자동 등록합니다. 다른 디렉터리를 스캔하도록 하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 활용하세요:

```
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하면 명령어 클래스 이름을 명시해 수동으로 등록할 수도 있습니다:

```
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan가 부팅될 때 애플리케이션의 모든 명령어는 [서비스 컨테이너](/docs/11.x/container)에서 해결되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식으로 커맨드 실행하기

가끔 명령줄 외에서 Artisan 명령어를 실행하고자 할 수도 있습니다. 예를 들어 라우트나 컨트롤러 내에서 실행하는 경우입니다. `Artisan` 파사드를 통해 `call` 메서드를 사용하세요. 첫 번째 인수로 명령어 시그니처나 클래스 이름을 전달하며, 두 번째 인수로 명령어 매개변수를 배열로 전달합니다. 반환값은 종료 코드입니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

또한, 전체 명령어 텍스트를 문자열로 통째로 전달할 수도 있습니다:

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

명령어가 배열 옵션을 정의한 경우, 배열 값을 그대로 전달할 수 있습니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달하기

`migrate:refresh` 명령어의 `--force` 플래그 같은 문자열 값을 받지 않는 옵션은 `true` 또는 `false` 불리언 값을 명시적으로 전달하세요:

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉하기

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 보내 백그라운드에서 처리할 수 있습니다. 이를 사용하려면 큐 설정을 하고 큐 리스너를 실행 중이어야 합니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`과 `onQueue` 메서드로 명령어를 보낼 연결 또는 큐를 지정할 수 있습니다:

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 커맨드에서 호출하기

커맨드 내에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용하세요. 명령어 이름과 인수 및 옵션 배열을 전달하면 됩니다:

```
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

출력을 숨기면서 호출하려면 `callSilently` 메서드를 사용하세요. 시그니처는 `call`과 동일합니다:

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 신호 처리

운영체제는 실행 중인 프로세스에 신호를 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램 종료 요청 신호입니다. Artisan 콘솔 명령어에서 신호를 감지하고 처리하려면 `trap` 메서드를 사용하세요:

```
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

한번에 여러 신호를 처리하려면 배열로 전달할 수도 있습니다:

```
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이징

Artisan의 `make` 명령어로 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 스텁 파일을 사용해 템플릿을 채워서 만듭니다. 생성된 파일에 작은 수정이 필요하면 `stub:publish` 명령어로 기본 스텁을 애플리케이션으로 퍼블리시해 직접 수정할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁들은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 스텁을 수정하면 해당 스텁을 참조하는 `make` 명령어로 생성된 클래스에도 변경 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 과정에서 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  

- `ArtisanStarting` 이벤트는 Artisan 실행 시작 시 바로 발생합니다.  
- `CommandStarting` 이벤트는 각 명령어 실행 직전에 발생합니다.  
- `CommandFinished` 이벤트는 명령어 실행 완료 후 발생합니다.