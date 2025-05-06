# 아티즌 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [커맨드 작성하기](#writing-commands)
    - [커맨드 생성](#generating-commands)
    - [커맨드 구조](#command-structure)
    - [클로저 커맨드](#closure-commands)
    - [Isolatable 커맨드](#isolatable-commands)
- [입력 기대 정의](#defining-input-expectations)
    - [인자](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [커맨드 입출력](#command-io)
    - [입력 값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [커맨드 등록](#registering-commands)
- [프로그램적으로 커맨드 실행](#programmatically-executing-commands)
    - [다른 커맨드에서 커맨드 호출](#calling-commands-from-other-commands)
- [신호 처리](#signal-handling)
- [스텁 커스터마이즈](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

아티즌(Artisan)은 Laravel에 내장된 커맨드라인 인터페이스입니다. 아티즌은 애플리케이션의 루트에 `artisan` 실행 파일로 존재하며, 애플리케이션을 개발할 때 많은 유용한 커맨드들을 제공합니다. 사용 가능한 모든 아티즌 커맨드 목록을 확인하려면 `list` 커맨드를 사용할 수 있습니다:

```shell
php artisan list
```

각 커맨드는 "도움말(help)" 화면도 포함하고 있어 해당 커맨드의 인자 및 옵션 설명을 확인할 수 있습니다. 도움말 화면을 보려면 커맨드 이름 앞에 `help`를 붙이세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)을 로컬 개발 환경으로 사용 중이라면, 아티즌 커맨드 실행 시 반드시 `sail` 명령줄을 이용해야 합니다. Sail은 아티즌 커맨드를 애플리케이션의 Docker 컨테이너 내에서 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동되는 Laravel 프레임워크용 강력한 REPL(Read-Eval-Print Loop)입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션은 기본적으로 Tinker가 포함되어 있습니다. 만약 기존에 제거했다면 Composer를 이용해 Tinker를 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]  
> Laravel 애플리케이션에서 핫 리로딩, 멀티라인 코드 편집, 자동완성을 경험하고 싶으신가요? [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용 방법

Tinker를 이용하면 Eloquent 모델, 잡, 이벤트 등 Laravel 애플리케이션 전체와 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` 아티즌 커맨드를 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일을 배포(publish)하려면 `vendor:publish` 커맨드를 사용하세요:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]  
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker에서 잡을 디스패치할 땐 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 커맨드 허용 목록

Tinker는 "허용(allow)" 리스트를 사용하여 셸 내에서 실행 가능한 아티즌 커맨드를 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 커맨드를 실행할 수 있습니다. 추가로 허용하고 싶은 커맨드는 `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다:

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a>
#### 별칭이 적용되지 않아야 할 클래스

대부분의 경우, Tinker는 사용자가 상호작용하는 클래스를 자동으로 별칭 처리(alias)합니다. 하지만 일부 클래스는 절대 별칭으로 등록하지 않길 원할 수 있습니다. 이때는 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가하세요:

    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>
## 커맨드 작성하기

아티즌이 제공하는 커맨드 외에도, 자신만의 커스텀 커맨드를 만들 수 있습니다. 커맨드는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 클래스를 로드할 수 있다면 어떤 위치든 자유롭게 저장해도 됩니다.

<a name="generating-commands"></a>
### 커맨드 생성

새 커맨드를 만들려면 `make:command` 아티즌 커맨드를 실행하세요. 이 명령은 새로운 커맨드 클래스를 `app/Console/Commands` 디렉터리에 생성합니다. 이 디렉터리가 없더라도 처음 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 커맨드 구조

커맨드를 생성한 후에는 클래스의 `signature`와 `description` 속성값을 적절하게 정의해야 합니다. 이 속성은 `list` 화면에서 커맨드를 표시할 때 사용됩니다. 또한 `signature` 속성은 [커맨드의 입력 기대값](#defining-input-expectations)을 정의할 수 있게 해줍니다. 커맨드가 실행되면 `handle` 메서드가 호출되며, 이곳에 실제 커맨드의 로직을 작성하면 됩니다.

예제 커맨드를 살펴보겠습니다. `handle` 메서드에서 원하는 의존성을 타입힌트로 요청할 수 있습니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)는 이 시그니처에 타입힌트된 모든 의존성을 자동 주입합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * 콘솔 커맨드의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * 콘솔 커맨드 설명
     *
     * @var string
     */
    protected $description = 'Send a marketing email to a user';

    /**
     * 콘솔 커맨드 실행
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]  
> 코드의 재사용성을 높이기 위해, 콘솔 커맨드는 되도록 가볍게 유지하고 실제 작업은 어플리케이션 서비스에 위임하는 것이 좋습니다. 위 예제처럼 "이메일 전송"의 핵심 처리를 서비스 클래스에 맡기면 좋습니다.

<a name="closure-commands"></a>
### 클로저 커맨드

클로저 기반의 커맨드는 커맨드 클래스로 작성하는 방식 대신 사용할 수 있는 대안입니다. 라우트의 클로저처럼, 커맨드의 클로저도 대체 방식으로 생각할 수 있습니다. 애플리케이션의 `app/Console/Kernel.php` 파일에 있는 `commands` 메서드 안에서, Laravel은 `routes/console.php` 파일을 불러옵니다:

```php
/**
 * Register the closure based commands for the application.
 */
protected function commands(): void
{
    require base_path('routes/console.php');
}
```

이 파일은 HTTP 라우트를 정의하지 않고, 애플리케이션으로 들어오는 콘솔 기반 엔트리포인트(라우트)를 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 커맨드를 정의할 수 있습니다. 이 메서드는 [커맨드 시그니처](#defining-input-expectations)와 커맨드 인자 및 옵션을 받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 실제 커맨드 인스턴스에 바인딩되기 때문에, 클래스 기반 커맨드에서 사용할 수 있는 모든 헬퍼 메서드를 동일하게 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 커맨드는 커맨드 인자와 옵션 외에도, [서비스 컨테이너](/docs/{{version}}/container)에서 주입받을 추가적인 의존성을 타입힌트로 받을 수도 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 커맨드 설명

클로저 기반 커맨드를 정의할 때 `purpose` 메서드를 사용해 커맨드 설명을 추가할 수 있습니다. 설명은 `php artisan list` 또는 `php artisan help` 실행 시 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 커맨드

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

동일한 커맨드를 동시에 단 한 번만 실행되도록 보장하고 싶을 때가 있습니다. 이를 위해 커맨드 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다:

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

커맨드에 `Isolatable`이 적용되면, Laravel은 자동으로 `--isolated` 옵션을 커맨드에 추가합니다. 해당 옵션과 함께 커맨드를 실행하면, 이미 같은 커맨드가 실행 중일 경우 실행되지 않습니다. Laravel은 애플리케이션의 기본 캐시 드라이버를 이용하여 원자적 락을 시도합니다. 이미 실행 중이여서 락을 얻지 못하면 커맨드는 실행되지 않고, 성공 종료 코드로 종료합니다:

```shell
php artisan mail:send 1 --isolated
```

실행하지 못할 때 반환할 종료 코드를 지정하려면 `isolated` 옵션에 원하는 숫자값을 지정하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### Lock ID

기본적으로 Laravel은 커맨드 명칭을 이용해 캐시 락 키를 생성합니다. 이 키를 커스터마이징하려면 커맨드 클래스에 `isolatableId` 메서드를 정의해 인자나 옵션 값을 키에 포함시킬 수 있습니다:

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

기본적으로 락은 커맨드 완료 후 만료됩니다. 만약 커맨드가 중단되어 종료하지 못하면 1시간 후 만료됩니다. 만료 시간을 조정하려면 커맨드에 `isolationLockExpiresAt` 메서드를 정의하면 됩니다:

```php
use DateTimeInterface;
use DateInterval;

/**
 * 커맨드에 대한 isolation 락 만료 시간 결정
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대 정의

콘솔 커맨드를 작성할 때는 사용자로부터 인자 또는 옵션을 통해 입력을 받는 경우가 많습니다. Laravel은 커맨드의 `signature` 속성에서 이러한 입력을 미리 정의할 수 있는 편리한 방식을 제공합니다. 간결하고 라우트와 유사한 문법으로 커맨드명, 인자, 옵션을 한 번에 정의할 수 있습니다.

<a name="arguments"></a>
### 인자

사용자가 입력할 인자와 옵션은 모두 중괄호로 감싸 정의합니다. 예를 들어, 아래 커맨드는 필수 인자 `user` 하나를 정의한 예입니다:

```php
/**
 * 콘솔 커맨드의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인자를 선택적으로 하거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인자...
'mail:send {user?}'

// 기본값이 있는 선택적 인자...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션도 또 다른 형태의 사용자 입력입니다. 커맨드라인에서 두 개의 하이픈(`--`)으로 입력합니다. 값이 없는 옵션(예: `--queue`)은 불리언 스위치로 작동합니다. 예시:

```php
/**
 * 콘솔 커맨드의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서 `--queue` 스위치는 지정되면 true, 지정하지 않으면 false 값을 가집니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값 입력이 필요한 옵션은 옵션명 끝에 `=`를 추가하여 정의합니다:

```php
/**
 * 콘솔 커맨드의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

커맨드 실행 시 옵션 값은 다음과 같이 전달합니다. 옵션을 지정하지 않으면 값은 null입니다:

```shell
php artisan mail:send 1 --queue=default
```

기본값을 주고 싶으면 옵션명 뒤에 값으로 지정합니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 작성 시 단축키를 지정하려면, 옵션명 앞에 넣고 `|`로 구분합니다:

```php
'mail:send {user} {--Q|queue}'
```

커맨드 사용 시 단축키는 한 개의 하이픈, 값은 `=` 없이 이어서 씁니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 개의 인자 또는 옵션 값을 받고 싶다면 `*` 기호를 사용합니다. 예를 들어:

```php
'mail:send {user*}'
```

이 커맨드를 다음과 같이 호출하면 `user` 인자의 값은 [1, 2] 배열이 됩니다:

```shell
php artisan mail:send 1 2
```

`*` 기호를 선택적 인자와 함께 사용하면 0개 이상 입력을 허용합니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 갖는 옵션 정의 시, 각각의 옵션 값은 옵션명과 함께 전달합니다:

```php
'mail:send {--id=*}'
```

여러 개의 `--id` 옵션을 넣으면 배열로 전달받습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인자 및 옵션 설명은 이름 뒤에 콜론(:)과 함께 추가할 수 있습니다. 여러 줄로 나누어 작성해도 무방합니다:

```php
/**
 * 콘솔 커맨드의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력 프롬프트

필수 인자가 없을 경우 사용자는 에러 메시지를 받게 됩니다. 또는 커맨드에 `PromptsForMissingInput` 인터페이스를 구현하면, 필수 인자가 누락되었을 때 자동으로 프롬프트를 보여주도록 할 수 있습니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * 콘솔 커맨드의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Laravel은 인자 이름 또는 설명을 이용해 적절히 문장을 만들어 자동으로 입력을 요구합니다. 프롬프트 질문을 커스터마이즈하고 싶으면 `promptForMissingArgumentsUsing` 메서드를 구현하고, 인자명을 키로 갖는 질문 배열을 반환하세요:

```php
/**
 * 누락된 인자에 대한 프롬프트 질문 정의
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

플레이스홀더(placeholder)가 필요하다면 튜플로 반환하세요:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 사용자 경험 전체를 제어하고 싶다면, 클로저를 사용해 직접 값을 반환할 수도 있습니다:

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
> 더 다양한 프롬프트 및 사용법은 [Laravel Prompts](/docs/{{version}}/prompts) 문서에서 확인할 수 있습니다.

옵션에 대해 [프롬프트](#options)를 하고 싶다면, 커맨드의 `handle` 메서드에 프롬프트를 추가하면 됩니다. 다만, 필수 인자에 대한 프롬프트가 된 이후에만 옵션 프롬프트를 실행하고 싶으면 `afterPromptingForMissingArguments` 메서드를 구현하세요:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * 필수 인자에 대해 프롬프트 후 추가 작업
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
## 커맨드 입출력(I/O)

<a name="retrieving-input"></a>
### 입력값 가져오기

커맨드를 실행하는 동안 인자 및 옵션 값을 접근해야 할 때가 많습니다. 이때는 `argument`와 `option` 메서드를 사용하세요. 값이 없는 경우 null이 반환됩니다:

```php
/**
 * 콘솔 커맨드 실행
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인자를 배열로 가져오고 싶다면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션 값도 `option` 메서드로 얻을 수 있으며, 모든 옵션을 배열로 가져오려면 `options` 메서드를 사용하세요:

```php
// 특정 옵션 하나만...
$queueName = $this->option('queue');

// 모든 옵션을 배열로...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]  
> [Laravel Prompts](/docs/{{version}}/prompts)는 플레이스홀더, 검증 등 브라우저와 유사한 기능의 아름답고 사용자 친화적인 폼을 콘솔 애플리케이션에 추가할 수 있도록 해주는 PHP 패키지입니다.

출력 표시 외에도, 커맨드 실행 중 사용자에게 입력을 요청할 수 있습니다. `ask` 메서드는 질문을 표시하고 사용자 입력을 받아 이를 반환합니다:

```php
/**
 * 콘솔 커맨드 실행
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

`ask` 메서드는 두 번째 인자로 기본값을 받을 수 있습니다. 사용자가 입력을 제공하지 않으면 이 기본값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 유사하지만, 입력 중 콘솔에 값이 보이지 않으므로 비밀번호 등 민감 정보 입력에 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(yes/no) 질문

단순한 "예/아니오" 확인이 필요하다면 `confirm` 메서드를 사용하세요. 기본적으로 false를 반환하지만, 사용자가 y 또는 yes라고 입력하면 true를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 true로 하려면 두 번째 인자로 true를 전달하세요:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성(Auto-Completion)

`anticipate` 메서드를 사용하면 사용자가 입력 중 자동완성 후보를 제공합니다. 입력은 후보 리스트 외의 값도 허용됩니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인자로 클로저를 넘기면, 매 입력마다 호출되어 자동완성 옵션 배열을 반환할 수 있습니다:

```php
$name = $this->anticipate('What is your address?', function (string $input) {
    // 자동완성 옵션 반환...
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택(선택형) 질문

사전 정의된 선택지 중 고르게 할 때는 `choice` 메서드를 사용하세요. 세 번째 인자로 기본값 인덱스를 지정하면 선택하지 않은 경우 그 값이 반환됩니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

최대 시도 횟수, 다중 선택 허용 여부는 네 번째, 다섯 번째 인자로 지정할 수 있습니다:

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

콘솔에 텍스트를 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 목적에 따라 적절한 ANSI 색상을 사용합니다. 일반적인 정보는 `info`(초록색)로 표시합니다:

```php
/**
 * 콘솔 커맨드 실행
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

에러 메시지는 `error` 메서드(빨간색)로 표시하세요:

```php
$this->error('Something went wrong!');
```

일반 텍스트는 `line` 메서드로 표시할 수 있습니다:

```php
$this->line('Display this on the screen');
```

빈 줄을 표시하려면 `newLine` 메서드를 사용하세요:

```php
// 빈 줄 한 개
$this->newLine();

// 빈 줄 세 개
$this->newLine(3);
```

<a name="tables"></a>
#### 표 출력

`table` 메서드는 여러 행/열의 데이터를 보기 좋게 출력해줍니다. 컬럼명과 데이터 배열만 넘기면, Laravel이 자동으로 적절한 크기의 표를 렌더링합니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바(Progress Bar)

작업 시간이 긴 경우, 진행 상황을 표시하는 진행 바가 유용합니다. `withProgressBar` 메서드는 반복자(iterable)를 돌면서 진행 바를 자동으로 단계별로 갱신합니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

좀 더 세밀하게 진행 바 제어가 필요할 때는 직접 단계를 지정하여 갱신할 수 있습니다:

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
> 더 다양한 옵션이 필요하다면 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 커맨드 등록

모든 콘솔 커맨드는 애플리케이션의 `App\Console\Kernel` 클래스(콘솔 커널)에 등록합니다. 이 클래스의 `commands` 메서드에는 커널의 `load` 메서드가 호출될 것입니다. 이 메서드는 `app/Console/Commands` 디렉터리를 스캔해 그 안의 모든 커맨드를 자동으로 아티즌에 등록합니다. 다른 디렉터리도 추가로 스캔하고 싶다면 `load`를 추가로 호출하면 됩니다:

```php
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

필요하다면, 커맨드 클래스 이름을 `$commands` 속성 배열에 수동으로 추가해도 됩니다. 이 속성이 정의되어 있지 않으면 직접 정의하세요. 아티즌이 부팅될 때 [서비스 컨테이너](/docs/{{version}}/container)로 등록 및 해석되어 실행됩니다:

```php
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
## 프로그램적으로 커맨드 실행

CLI 밖에서 아티즌 커맨드를 실행하고 싶을 때가 있습니다. 예를 들어, 라우트 또는 컨트롤러에서 아티즌 커맨드를 실행하고 싶을 때는 `Artisan` 파사드의 `call` 메서드를 사용하세요. 커맨드 시그니처 혹은 클래스 이름, 그리고 두 번째 인자로 파라미터 배열을 전달합니다. 종료코드가 반환됩니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

또는 커맨드 전체를 하나의 문자열로 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

커맨드 옵션이 배열을 받는 경우, 값 배열을 넘겨주면 됩니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달

값이 없는 옵션(예: `migrate:refresh` 커맨드의 `--force` 플래그)에 값을 지정할 땐 true/false를 전달합니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### 아티즌 커맨드 큐로 실행

`Artisan` 파사드의 `queue` 메서드를 사용하면 아티즌 커맨드를 [큐 워커](/docs/{{version}}/queues)에서 백그라운드로 실행할 수 있습니다. 이 기능을 쓰기 전에 큐 설정 및 큐 리스너 실행을 확인하세요:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`, `onQueue` 메서드를 이용해 커맨드 디스패치 시 커넥션/큐도 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 커맨드에서 커맨드 호출

기존 아티즌 커맨드 내에서 다른 커맨드를 호출해야 할 때, `call` 메서드를 사용하세요. 첫 번째 인자는 커맨드 이름, 두 번째 인자는 인자/옵션 배열입니다:

```php
/**
 * 콘솔 커맨드 실행
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

출력을 모두 숨기고 커맨드를 호출하고 싶다면 `callSilently` 메서드를 사용하세요. 시그니처는 `call`와 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 신호 처리

운영체제는 실행 중인 프로세스에 신호를 보낼 수 있습니다. 예를 들어, `SIGTERM`은 프로그램에 종료 요청을 보낼 때 사용하는 신호입니다. 아티즌 콘솔 커맨드에서 신호를 수신하고 처리하려면 `trap` 메서드를 사용하세요:

```php
/**
 * 콘솔 커맨드 실행
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 개의 신호를 동시에 감지하려면 배열로 전달하세요:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이즈

아티즌 콘솔의 `make` 커맨드는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 값이 치환되는 "스텁(stub)" 파일을 기반으로 생성됩니다. 아티즌으로 생성되는 파일에 약간의 변형을 가하고 싶을 때는 `stub:publish` 명령으로 공통 스텁을 애플리케이션에 복사해 원하는대로 수정할 수 있습니다:

```shell
php artisan stub:publish
```

복사된 스텁들은 애플리케이션 루트의 `stubs` 디렉토리에 위치하게 됩니다. 이 파일들을 수정하면, 해당 스텁을 참조하는 클래스 생성 시 반영됩니다.

<a name="events"></a>
## 이벤트

아티즌은 커맨드를 실행할 때 세 가지 이벤트를 dispatch합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 시작되는 즉시, `CommandStarting`은 커맨드 실행 직전, `CommandFinished`는 커맨드 실행 후에 각각 발생합니다.