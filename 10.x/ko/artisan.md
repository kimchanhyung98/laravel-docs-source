# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [격리 가능한 명령어](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [필수 입력값 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력하기](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그래밍 방식 명령어 실행](#programmatically-executing-commands)
    - [명령어 내에서 다른 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁(stub) 사용자화](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션 개발 시 도움이 되는 여러 유용한 명령어들을 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면, `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어는 해당 명령어의 사용 가능한 인수와 옵션을 보여주고 설명하는 "도움말" 화면을 포함하고 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

만약 [Laravel Sail](/docs/10.x/sail)을 로컬 개발 환경으로 사용 중이라면, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 한다는 점을 기억하세요. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 Laravel 프레임워크를 위한 강력한 REPL(Read-Eval-Print Loop)로, [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동됩니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만 이전에 애플리케이션에서 제거한 경우, Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]  
> Laravel 애플리케이션과 상호작용할 때 실시간 리로드, 여러 줄 코드 편집, 자동 완성 기능을 원한다면 [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker는 Eloquent 모델, 잡, 이벤트 등 애플리케이션 전반과 명령줄에서 상호작용할 수 있게 합니다. Tinker 환경으로 들어가려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker 설정 파일은 `vendor:publish` 명령어로 퍼블리시 할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]  
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션을 사용합니다. 따라서 tinker를 사용할 경우, 잡을 디스패치할 때 `Bus::dispatch` 또는 `Queue::push` 메서드를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록 (Command Allow List)

Tinker는 쉘 내에서 실행할 수 있는 Artisan 명령어를 제한하는 "허용 목록"을 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어를 실행할 수 있습니다. 추가 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다:

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 생성하지 않을 클래스

Tinker는 일반적으로 상호작용하는 클래스들을 자동으로 별칭(alias)합니다. 하지만 일부 클래스는 절대 별칭을 생성하지 않도록 지정하고 싶을 수 있습니다. 이때 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스명을 나열하세요:

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan에서 기본 제공하는 명령어 외에도, 사용자 정의 명령어를 만들 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 보관하지만, Composer로 로드할 수 있다면 원하는 위치에 저장해도 됩니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 명령어 클래스를 생성합니다. 이 디렉터리가 없더라도 `make:command` 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature` 및 `description` 속성에 적절한 값을 정의해야 합니다. 이 값들은 `list` 화면에 명령어를 표시할 때 사용됩니다. `signature` 속성은 [명령어의 입력 기대값](#defining-input-expectations)을 정의할 수 있게 해 줍니다. 명령어가 실행될 때 `handle` 메서드가 호출되며, 명령어 실행 로직은 이 메서드에 작성합니다.

다음은 명령어 예시입니다. `handle` 메서드에는 필요한 의존성을 주입 받을 수 있는데, Laravel [서비스 컨테이너](/docs/10.x/container)가 이 메서드의 시그니처에 타입힌팅 된 모든 의존성을 자동으로 주입합니다:

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
> 재사용성을 높이기 위해, 콘솔 명령어는 가볍게 유지하고 작업은 애플리케이션 서비스에 위임하는 것이 좋은 습관입니다. 위 예시처럼 이메일 발송의 핵심 로직을 서비스 클래스에 맡긴 경우를 참고하세요.

<a name="closure-commands"></a>
### 클로저 명령어

클로저(Closure)를 기반으로 명령어를 정의하는 방식은 클래스 기반 선언의 대안입니다. 라우트 클로저가 컨트롤러 대신 쓰이는 것과 비슷하게, 명령어 클로저는 명령어 클래스 대신 쓰일 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드 내에서 Laravel은 `routes/console.php` 파일을 로드합니다:

```
/**
 * Register the closure based commands for the application.
 */
protected function commands(): void
{
    require base_path('routes/console.php');
}
```

이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션 내 콘솔 진입점(라우트)을 만듭니다. 여기서는 `Artisan::command` 메서드로 클로저 기반의 모든 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 두 개의 인수를 받는데, 하나는 [명령어 시그니처](#defining-input-expectations), 다른 하나는 명령어의 인수와 옵션을 받는 클로저입니다:

```
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 기본 명령어 인스턴스에 바인딩되어, 클래스 명령어에서 접근 가능한 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

명령어 인수 및 옵션 외에도, 클로저는 [서비스 컨테이너](/docs/10.x/container)에서 해결할 추가 의존성을 타입힌팅으로 받을 수 있습니다:

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 기반 명령어에 설명을 추가하려면 `purpose` 메서드를 사용하세요. 이 설명은 `php artisan list` 또는 `php artisan help` 실행 시 표시됩니다:

```
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 격리 가능한 명령어

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신 중이어야 합니다.

한 번에 한 인스턴스만 명령어가 실행되도록 보장하고 싶을 때가 있습니다. 이때 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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

`Isolatable`로 표시된 명령어는 자동으로 `--isolated` 옵션이 추가됩니다. 이 옵션으로 호출 시, Laravel은 애플리케이션 기본 캐시 드라이버를 사용해 원자적 락(atomic lock)을 시도하며 다른 인스턴스가 이미 실행 중이라면 실행을 막습니다. 다만, 이 경우에도 정상 종료 코드로 종료합니다:

```shell
php artisan mail:send 1 --isolated
```

실행 불가 시 반환할 종료 코드를 지정하려면 `--isolated` 옵션에 값을 줄 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어 이름을 이용해 캐시 락 키를 생성합니다. 이 키에 명령어의 인수나 옵션을 포함시키고 싶다면 `isolatableId` 메서드를 Artisan 명령어 클래스에 정의하면 됩니다:

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

기본적으로 락은 명령어 실행이 완료되면 만료됩니다. 명령어가 중단될 경우 1시간 후 자동 만료됩니다. 시간 조절을 원한다면 `isolationLockExpiresAt` 메서드를 정의해 만료 시간을 반환하세요:

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

콘솔 명령어를 작성할 때, 사용자로부터 인수나 옵션을 통해 입력을 받는 경우가 많습니다. Laravel에서는 명령어 클래스의 `signature` 속성을 이용해 사용자에게 기대하는 입력을 매우 간편하게 정의할 수 있습니다. `signature` 속성은 이름, 인수, 옵션을 한 줄의 라우트 스타일 문법으로 표현합니다.

<a name="arguments"></a>
### 인수

사용자가 입력하는 모든 인수와 옵션은 중괄호 `{}`로 감쌉니다. 다음 예시는 `user`라는 필수 인수 하나를 정의합니다:

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
### 옵션

옵션은 옵션형 사용자 입력입니다. 명령줄에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값이 있을 수도 있고 없을 수도 있습니다. 값이 없는 옵션은 부울(Boolean) 스위치처럼 동작합니다. 다음은 값이 없는 옵션 예시입니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위에서 `--queue` 스위치를 전달하면 옵션의 값이 `true`이고, 전달하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 반드시 지정해야 하는 옵션은 이름 뒤에 `=`를 붙여 표시합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

명령어 실행 시, 다음과 같이 옵션에 값을 지정할 수 있습니다. 옵션을 지정하지 않으면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

기본값을 지정할 수도 있습니다. 사용자가 옵션을 지정하지 않으면 기본값이 사용됩니다:

```
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 붙이려면 옵션 이름 앞에 단축키를 적고 `|` 문자로 구분하세요:

```
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어 호출 시 옵션 단축키는 하나의 하이픈과 함께 사용하며 값 지정 시 `=` 없이 바로 값을 붙입니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

입력값이 여러 개 올 경우에는 `*` 문자를 사용할 수 있습니다. 예를 들어, 다음과 같이 인수를 정의하면:

```
'mail:send {user*}'
```

명령줄에서 `user` 인수에 여러 값을 순서대로 전달할 수 있습니다. 예:

```shell
php artisan mail:send 1 2
```

이 경우 `user` 값은 `[1, 2]` 배열이 됩니다.

`*`와 선택적 인수를 합쳐 0개 이상의 인수를 받을 수도 있습니다:

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 갖는 옵션을 선언할 때도 동일하게 각 값에 옵션 이름을 붙여 전달해야 합니다:

```
'mail:send {--id=*}'
```

명령 실행 예:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수나 옵션에 설명을 붙이려면 이름과 설명을 콜론(:)으로 구분합니다. 여러 줄에 걸쳐 정의해도 무방합니다:

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
### 필수 입력값 프롬프트

필수 인수가 없을 경우 기본적으로 에러가 발생합니다. 대신, `PromptsForMissingInput` 인터페이스를 구현하면 필수 인수가 없을 때 자동으로 사용자에게 입력을 요청하도록 할 수 있습니다:

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

Laravel은 인수 이름이나 설명을 활용해 자연스러운 질문으로 사용자에게 입력을 요청합니다. 질문 문구를 직접 지정하려면 `promptForMissingArgumentsUsing` 메서드를 구현해 인수명 키에 매핑된 질문을 배열로 반환하면 됩니다:

```
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array
 */
protected function promptForMissingArgumentsUsing()
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

프롬프트에 플레이스홀더를 추가하려면 질문과 플레이스홀더를 배열 튜플로 반환하세요:

```
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 동작을 완전히 커스터마이징하려면, 사용자에게 질문하고 답변을 반환하는 클로저를 제공할 수도 있습니다:

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
> 자세한 내용 및 사용법은 [Laravel Prompts](/docs/10.x/prompts) 문서를 참고하세요.

옵션에 관한 프롬프트를 명령어 내에서 직접 수행하려면 `handle` 메서드에 삽입할 수도 있습니다. 다만, 자동 프롬프트와 함께 옵션 프롬프트를 실행하려면 `afterPromptingForMissingArguments` 메서드를 구현하는 방법이 있습니다:

```
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 *
 * @param  \Symfony\Component\Console\Input\InputInterface  $input
 * @param  \Symfony\Component\Console\Output\OutputInterface  $output
 * @return void
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output)
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
### 입력값 가져오기

명령어 실행 중, 인수와 옵션의 값을 가져와야 할 때가 많습니다. `argument`와 `option` 메서드를 사용하면 각 값에 접근할 수 있습니다. 존재하지 않는 인수나 옵션을 요청하면 `null`을 반환합니다:

```
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한꺼번에 가져오려면 `arguments` 메서드를 사용하세요:

```
$arguments = $this->arguments();
```

옵션도 같은 방식으로 `option`과 `options` 메서드를 통해 단일 또는 모든 옵션을 가져올 수 있습니다:

```
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]  
> [Laravel Prompts](/docs/10.x/prompts)는 콘솔 애플리케이션에 아름답고 사용하기 쉬운 폼을 추가하는 PHP 패키지로, 플레이스홀더와 유효성 검사 같은 브라우저 단말 기능을 갖추고 있습니다.

출력을 보여주는 것 외에도 명령어 실행 중 사용자 입력을 요청할 수 있습니다. `ask` 메서드는 질문을 표시하고 사용자의 입력을 받아 반환합니다:

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

`ask` 메서드는 두 번째 인자로 기본값을 받을 수 있어, 입력이 없으면 기본값이 반환됩니다:

```
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 같지만, 입력값을 터미널에 표시하지 않습니다. 비밀번호와 같은 민감한 정보를 받을 때 유용합니다:

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청하기

간단한 예/아니오 질문은 `confirm` 메서드를 사용하세요. 기본적으로 `false`를 반환하며, 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다:

```
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 `true`로 지정하려면 두 번째 인자로 `true`를 전달하세요:

```
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 선택지 목록을 제공해 자동 완성을 지원합니다. 사용자는 자동 완성 추천 외에 다른 답변도 입력할 수 있습니다:

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

두 번째 인자로 클로저를 넘겨 입력할 때마다 동적으로 자동 완성 후보를 받아오도록 할 수도 있습니다. 클로저는 현재까지 입력한 문자열을 받고 배열을 반환해야 합니다:

```
$name = $this->anticipate('What is your address?', function (string $input) {
    // 자동 완성 후보 반환...
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택 질문

사전에 정의된 선택지 중에서 고르도록 하려면 `choice` 메서드를 사용하세요. 기본 선택지는 세 번째 인자로 기본값 인덱스를 전달해 지정할 수 있습니다:

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한, 네 번째와 다섯 번째 인자로 최대 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

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

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용하세요. 각각의 메서드는 목적에 맞는 ANSI 색상을 자동으로 적용합니다. 예를 들어, 일반 정보 메시지는 `info` 메서드가 녹색 텍스트로 표시합니다:

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

오류 메시지는 `error` 메서드를 사용하며, 보통 빨간색 텍스트로 표시됩니다:

```
$this->error('Something went wrong!');
```

색이 없는 일반 텍스트 출력은 `line` 메서드를 사용하세요:

```
$this->line('Display this on the screen');
```

빈 줄을 출력할 때는 `newLine` 메서드를 사용합니다:

```
// 빈 줄 하나 출력...
$this->newLine();

// 빈 줄 세 개 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행과 열의 데이터를 올바르게 포매팅해 출력하기 쉽게 도와줍니다. 컬럼 이름 배열과 데이터를 전달하면, Laravel이 자동으로 너비와 높이를 계산해 정렬해 줍니다:

```
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

긴 작업의 진행 상황을 시각적으로 알려 줄 때 진행 바가 유용합니다. `withProgressBar` 메서드는 반복 가능한 값을 전달받아 아이템마다 진행 상태를 갱신합니다:

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행 바를 수동으로 제어하고 싶다면, 먼저 전체 단계 수를 지정하고 각 아이템 처리 후 `advance`를 호출하세요:

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
> 더 자세한 설정은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

모든 콘솔 명령어는 애플리케이션의 "콘솔 커널"인 `App\Console\Kernel` 클래스 내에서 등록됩니다. 이 클래스의 `commands` 메서드 안에는 `load` 메서드 호출이 있습니다. `load`는 지정한 디렉터리의 명령어들을 스캔해 Artisan에 자동 등록합니다. 필요한 경우, 추가 위치를 스캔하기 위해 `load`를 여러 번 호출할 수도 있습니다:

```
/**
 * Register the commands for the application.
 */
protected function commands(): void
{
    $this->load(__DIR__.'/Commands');
    $this->load(__DIR__.'/../Domain/Orders/Commands');

    // ...
}
```

명령어를 수동 등록하려면, `App\Console\Kernel` 클래스에 `$commands` 프로퍼티를 정의한 뒤 명령어 클래스명을 배열로 추가하세요. Artisan 부팅 시 해당 명령어들이 서비스 컨테이너를 통해 자동 등록됩니다:

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식 명령어 실행

 때때로 명령줄이 아닌 곳에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 예를 들면 라우트나 컨트롤러 내에서 명령어를 실행할 때가 그렇습니다. `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. 첫 번째 인자로 명령어 시그니처나 클래스명을, 두 번째 인자로 명령어 파라미터 배열을 받으며, 종료 코드가 반환됩니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

또는 전체 명령어를 문자열 그대로 넘길 수도 있습니다:

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

옵션이 배열 타입 입력을 받는다면, 배열을 직접 넘겨서 여러 값을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 부울 값 전달

`migrate:refresh` 명령어의 `--force` 플래그처럼, 문자열 값이 아닌 부울 값을 지정해야 한다면 true 또는 false로 값을 넘기세요:

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 이용하면 Artisan 명령어를 큐에 넣어 백그라운드에서 처리할 수 있습니다. 사용 전 큐를 설정하고 큐 워커가 실행 중인지 확인하세요:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`과 `onQueue` 메서드를 체인으로 연결해 특정 연결이나 큐로 명령어를 지정할 수 있습니다:

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 내에서 다른 명령어 호출

기존 Artisan 명령어 내에서 다른 명령어를 호출하고 싶을 때가 있습니다. 이때 `call` 메서드를 사용하세요. 첫 번째 인자로 호출할 명령어 이름, 두 번째 인자로 인수 및 옵션 배열을 받습니다:

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

출력을 모두 숨기고 호출하려면 `callSilently` 메서드를 사용하세요. 호출 방식은 `call`과 동일합니다:

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램 종료 요청 시그널입니다. Artisan 명령어 내에서 이런 시그널을 감지해 특정 코드를 실행하려면 `trap` 메서드를 사용하세요:

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

여러 시그널을 동시에 감지하려면 배열을 전달하세요:

```
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 사용자화

Artisan의 `make` 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 생성 시에는 입력에 기반해 값이 채워지는 "stub" 파일을 사용합니다. 생성되는 파일에 약간의 수정을 원하는 경우, `stub:publish` 명령어로 가장 많이 쓰이는 스텁 파일을 애플리케이션 내부에 복사해 사용자화할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시 된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이곳에서 수정한 내용은 Artisan `make` 명령어 실행 시 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 중 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, 그리고 `Illuminate\Console\Events\CommandFinished`.  
- `ArtisanStarting` 이벤트는 Artisan이 시작하자마자 발생합니다.  
- `CommandStarting` 이벤트는 명령어가 바로 실행되기 전 발생합니다.  
- `CommandFinished` 이벤트는 명령어 실행이 끝나면 발생합니다.