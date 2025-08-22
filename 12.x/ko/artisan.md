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
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력 프롬프트 표시](#prompting-for-input)
    - [출력 쓰기](#writing-output)
- [명령어 등록](#registering-commands)
- [명령어 코드로 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 내장된 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움이 되는 다양한 유용한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 "도움말" 화면이 포함되어 있어, 해당 명령어에서 사용할 수 있는 인수와 옵션을 표시하고 설명합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙이면 됩니다:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 한다는 점을 기억하세요. Sail을 이용하면 Artisan 명령어가 애플리케이션의 Docker 컨테이너 내에서 실행됩니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지가 지원하는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만 애플리케이션에서 Tinker를 삭제한 경우 Composer를 사용해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때, 핫리로딩, 멀티라인 코드 편집, 자동완성을 찾고 계신가요? [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용 방법

Tinker를 이용하면 Eloquent 모델, 잡, 이벤트 등 전체 Laravel 애플리케이션을 명령줄에서 직접 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일은 `vendor:publish` 명령어로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 추가할 때 가비지 컬렉션에 의존합니다. 따라서 Tinker를 사용할 때는 잡을 디스패치할 때 `Bus::dispatch`나 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 명령어 허용 리스트

Tinker는 "허용 리스트(allow list)"를 사용하여 해당 셸 내에서 실행할 수 있는 Artisan 명령어를 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 등의 명령어가 허용되어 있습니다. 더 많은 명령어를 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 원하지 않는 클래스

보통 Tinker는 Tinker 안에서 클래스와 상호작용 할 때 자동으로 별칭을 부여합니다. 하지만 일부 클래스는 자동으로 별칭되지 않도록 설정할 수 있습니다. `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 나열하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan이 기본으로 제공하는 명령어 외에도, 사용자 지정 명령어를 직접 만들 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉토리에 저장되지만, [다른 디렉토리도 Artisan 명령어로 스캔](#registering-commands)하도록 설정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새로운 명령어를 만들려면, `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉토리에 새로운 명령어 클래스를 생성합니다. 만약 이 디렉토리가 존재하지 않는다 해도, 처음 `make:command` Artisan 명령어를 실행하면 디렉토리가 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후, 클래스의 `signature` 속성과 `description` 속성에 적절한 값을 지정해야 합니다. 이 값들은 `list` 화면에서 명령어를 표시할 때 사용됩니다. 또한, `signature` 속성을 이용해 [명령어의 입력 기대값](#defining-input-expectations)을 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되며, 실제 명령어의 로직을 이 메서드에 작성하면 됩니다.

아래는 예시 명령어입니다. 명령어의 `handle` 메서드에서 의존성 주입을 통해 필요한 의존성을 요청할 수 있다는 점에 주목하세요. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 이 메서드의 타입힌트에 따른 의존성을 자동으로 주입해줍니다:

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
> 코드의 재사용성을 높이기 위해, 콘솔 명령어 내부의 코드는 가볍게 유지하고 주요 작업은 애플리케이션 서비스에 위임하는 것이 좋은 습관입니다. 위 예시에서도 이메일 발송의 핵심 로직을 서비스 클래스로 분리했습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 정상적으로 실행되면, 종료 코드 `0`으로 명령어가 종료됩니다. 하지만, `handle` 메서드에서 정수값을 반환하여 명령어의 종료 코드를 직접 지정할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내의 어떤 메서드에서든 명령어를 "강제 실패"시키고 싶다면, `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 명령어 실행을 즉시 종료하며, 종료 코드 1을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 콘솔 명령어를 클래스로 정의하는 것의 대안입니다. 이는 라우팅에서 클로저가 컨트롤러의 대안이 되는 것과 비슷하게 생각할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트가 아니라, 콘솔 기반 진입점(라우트)을 애플리케이션에 정의하는 곳입니다. 이 파일 내에서는 `Artisan::command` 메서드를 사용해 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와, 명령어의 인수·옵션을 받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 실제 명령어 인스턴스에 바인딩되므로, 클래스 기반 명령어에서 사용 가능한 모든 헬퍼 메서드들을 동일하게 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 명령어는 입력 인수·옵션 외에도, [서비스 컨테이너](/docs/12.x/container)를 통해 해결할 추가 의존성도 타입힌트로 받을 수 있습니다:

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

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용해 명령어의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어로 확인할 수 있습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

한 번에 하나의 명령어 인스턴스만 실행되도록 보장하고 싶은 경우가 있을 수 있습니다. 이를 위해 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다:

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

명령어에 `Isolatable`을 지정하면 `--isolated` 옵션이 명령어의 옵션에 자동으로 추가됩니다. 명령어를 이 옵션과 함께 실행하면 Laravel은 이미 동일한 명령어가 실행 중인지 확인하여, 실행 중이 아니라면 원자적 락을 획득하고 명령어를 실행합니다. 만약 이미 다른 인스턴스가 실행 중이라면, 명령어는 실행되지 않으나 성공적인 종료 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어를 실행할 수 없을 때 반환할 종료 코드를 지정하고 싶다면, `isolated` 옵션에 값을 지정할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어 이름으로 원자적 캐시 락의 키를 생성합니다. 하지만, 명령어 클래스에 `isolatableId` 메서드를 정의하여 이 키를 커스터마이즈할 수 있으며, 명령어 인수나 옵션 값을 락 키에 통합할 수 있습니다:

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

격리된(락된) 명령어는 기본적으로 명령어가 끝나면 락이 해제됩니다. 명령어가 중단되어 완료되지 못할 경우에는 1시간 후에 락이 만료됩니다. 이 만료 시간을 조정하려면 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의할 수 있습니다:

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

콘솔 명령어를 작성할 때는 사용자로부터 인수(argument)나 옵션(option) 형태로 입력을 받는 경우가 많습니다. Laravel에서는 명령어의 `signature` 속성을 이용해, 한 줄의 명확하고 간결한 라우트 스타일 문법으로 사용자가 입력해야 할 값(이름, 인수, 옵션 등)을 쉽게 정의할 수 있습니다.

<a name="arguments"></a>
### 인수

모든 사용자 입력 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서, 명령어는 필수 인수 `user`를 정의하고 있습니다:

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

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션은 인수와 비슷한 또 다른 형태의 사용자 입력입니다. 옵션은 명령줄에서 제공될 때 두 개의 하이픈(`--`)으로 시작합니다. 옵션은 값을 받을 수도, 받지 않을 수도 있습니다. 값을 받지 않는 옵션은 불리언(참/거짓) "스위치"로 동작합니다. 다음은 불리언 옵션의 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

이 예시에서, `--queue` 스위치는 명령어를 실행할 때 지정할 수 있습니다. 스위치가 전달되면 옵션의 값은 `true`, 그렇지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 받아야 하는 옵션의 경우, 옵션 이름 뒤에 `=`를 붙여 정의합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 옵션 값을 아래와 같이 전달할 수 있습니다. 옵션을 명령어에 지정하지 않으면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

기본값이 있는 옵션을 정의하려면, 옵션 이름 뒤에 기본값을 지정합니다. 사용자가 값을 넘기지 않으면 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정할 때는 단축키를 옵션 이름 앞에 작성하고, 구분자는 `|`를 사용합니다:

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어를 호출할 때, 옵션 단축키는 한 개의 하이픈으로 시작하며, 값을 지정할 때 `=`는 포함하지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 값을 입력받는 인수 또는 옵션을 정의하고 싶을 때는 `*` 기호를 사용할 수 있습니다. 먼저, 인수에 적용한 예시입니다:

```php
'mail:send {user*}'
```

이 예시처럼 명령어를 실행하면, `user` 인수는 명령줄에서 여러 개의 값을 받아 배열이 됩니다. 아래의 명령어는 `user`가 `[1, 2]`가 됩니다:

```shell
php artisan mail:send 1 2
```

이 `*` 기호는 선택적 인수와 조합하여, 0개 이상의 인수를 받을 수도 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받을 옵션을 정의할 때는 각 옵션 값을 옵션 이름과 함께 계속 전달합니다:

```php
'mail:send {--id=*}'
```

아래처럼 여러 번 `--id` 옵션을 전달하면 됩니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수 및 옵션에 설명을 추가하려면, 이름과 설명을 콜론으로 구분합니다. 명령어 정의가 길어질 경우, 여러 줄에 걸쳐 작성해도 됩니다:

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

명령어에 필수 인수가 있는 경우, 사용자가 인수를 제공하지 않으면 오류 메시지가 표시됩니다. 또는, `PromptsForMissingInput` 인터페이스를 구현하여, 필수 인수가 누락되었을 때 사용자에게 질문을 자동으로 프롬프트 할 수 있습니다:

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

Laravel은 필수 인수가 누락된 경우 인수 이름 또는 설명을 이용해 지능적으로 질문을 자동 생성해 사용자에게 묻습니다. 인수를 입력받기 위한 질문을 원하는 방식으로 커스터마이징하려면, `promptForMissingArgumentsUsing` 메서드를 구현하여 인수명을 키로 하는 질문 배열을 반환하면 됩니다:

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

질문과 함께 플레이스홀더 텍스트를 제공하고 싶으면, 질문과 플레이스홀더가 담긴 튜플(배열)을 반환하면 됩니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 과정을 완전히 컨트롤하고 싶으면, 사용자를 프롬프트하고 답변을 반환하는 클로저를 제공할 수도 있습니다:

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
> 더욱 다양한 프롬프트와 사용법에 대해서는 [Laravel Prompts](/docs/12.x/prompts) 문서를 참고하세요.

사용자에게 [옵션](#options) 입력을 선택하거나 직접 입력하도록 안내하려면, 명령어의 `handle` 메서드 내에서 프롬프트를 포함할 수 있습니다. 하지만, 누락된 인수 프롬프트와 함께 동작할 때만 사용자에게 프롬프트를 하고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다:

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
### 입력값 가져오기

명령어가 실행되는 동안, 명령어에 전달된 인수와 옵션 값을 받아야 할 일이 있습니다. 이때는 `argument`와 `option` 메서드를 사용할 수 있습니다. 인수 또는 옵션이 없다면 `null`이 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 `array` 형태로 한 번에 가져오려면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 메서드를 쓰거나, 모든 옵션을 배열로 받으려면 `options` 메서드를 사용할 수 있습니다:

```php
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트 표시

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령줄 애플리케이션에 플레이스홀더 및 유효성 검사 같은 브라우저 수준의 기능을 제공하는, 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지입니다.

출력 표시 외에, 명령어 실행 중 사용자에게 입력을 요구할 수도 있습니다. `ask` 메서드는 지정한 질문을 사용자에게 프롬프트 해 입력을 받고, 그 값을 반환합니다:

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

`ask` 메서드는 두 번째 인자로 기본값을 지정할 수 있습니다. 사용자가 아무 값도 입력하지 않으면 기본값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 사용자가 콘솔에 입력하는 값이 화면에 표시되지 않습니다. 이 메서드는 비밀번호 등 민감한 정보를 입력받을 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 질문

간단한 "예/아니오" 확인을 사용자에게 물어야 한다면, `confirm` 메서드를 사용할 수 있습니다. 기본적으로 이 메서드는 `false`를 반환합니다. 하지만 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요하다면, 두 번째 인자로 `true`를 전달해 기본값을 `true`로 지정할 수도 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드를 사용하면 자동 완성 후보값을 제시할 수 있습니다. 단, 자동 완성 후보와 상관없이 사용자는 임의의 값을 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인자로 클로저를 전달해, 사용자의 입력이 들어올 때마다 자동완성 후보를 동적으로 제공할 수도 있습니다. 클로저는 현재까지의 입력값(문자열)을 받아, 자동완성 후보 배열을 반환해야 합니다:

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

미리 정의된 선택지 중 하나를 고르게 하고 싶다면, `choice` 메서드를 사용할 수 있습니다. 세 번째 인자로는 기본값의 인덱스를 넘길 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한 `choice` 메서드는 네 번째, 다섯 번째 인자로, 유효한 답변을 선택할 수 있는 최대 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

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

콘솔에 출력을 보내려면, `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 컬러를 사용해 텍스트를 출력합니다. 예를 들어, 일반 정보 메시지를 출력하려면 `info` 메서드를 사용하는데, 탑재된 대부분의 콘솔에서는 초록색으로 표시됩니다:

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

에러 메시지를 표시하려면 `error` 메서드를 사용하세요. 에러 메시지는 보통 빨간색으로 표시됩니다:

```php
$this->error('Something went wrong!');
```

단순히 일반 텍스트(색상 없음)로 표시하고 싶으면, `line` 메서드를 사용하세요:

```php
$this->line('Display this on the screen');
```

빈 줄을 표시하려면 `newLine` 메서드를 사용하세요:

```php
// 한 줄만 비워쓰기...
$this->newLine();

// 세 줄 비워쓰기...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드를 사용하면 여러 행/열의 데이터를 쉽게 표 형식으로 출력할 수 있습니다. 컬럼명과 데이터를 넘기면, Laravel이 자동으로 적절한 넓이와 높이로 테이블을 렌더링합니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바(Progress Bar)

시간이 오래 걸리는 작업에는, 사용자에게 진행 상황을 알려주는 프로그레스바를 표시할 수 있습니다. `withProgressBar` 메서드를 사용하면 컬렉션 등의 iterable을 순회할 때마다 자동으로 프로그레스바가 갱신됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행바를 수동으로 조작하고 싶을 때는, 총 단계 수를 먼저 설정하고, 각 항목 처리 후 직접 앞으로 진행시키면 됩니다:

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
> 보다 고급 기능이 필요하다면 [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

Laravel은 기본적으로 `app/Console/Commands` 디렉토리의 모든 명령어를 자동으로 등록합니다. 하지만, 필요한 경우 애플리케이션의 `bootstrap/app.php`에서 `withCommands` 메서드를 이용해 추가 디렉토리를 Artisan 명령어 디렉토리로 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면, 명령어 클래스명을 직접 지정하여 명령어를 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션 내의 모든 명령어는 [서비스 컨테이너](/docs/12.x/container)에 의해 해결되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 명령어 코드로 실행하기

때로는 CLI 밖에서 Artisan 명령어를 실행해야 할 수 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령어를 실행할 수도 있죠. 이를 위해 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인자로 명령어의 시그니처 명칭 또는 클래스명을, 두 번째 인자로 명령어 파라미터 배열을 받습니다. 반환값은 종료 코드입니다:

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

또는 전체 Artisan 명령어를 문자열로 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어의 옵션이 배열을 받을 경우, 옵션값을 배열로 넘겨줄 수 있습니다:

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

문자열이 아닌 값을 받는 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그)에는 옵션값을 `true` 또는 `false`로 지정하면 됩니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용해 Artisan 명령어를 큐에 추가하고, [큐 워커](/docs/12.x/queues)를 통해 백그라운드에서 처리할 수도 있습니다. 이 방법을 사용하기 전에, 큐 구성이 완료되어 있고 큐 리스너가 실행 중이어야 합니다:

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

`onConnection`, `onQueue` 메서드를 사용해 어떤 커넥션/큐에 Artisan 명령어가 디스패치될지 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출

기존 Artisan 명령어 내부에서 또 다른 명령어를 호출하고 싶은 경우, `call` 메서드를 사용할 수 있습니다. `call` 메서드는 명령어 이름과 인자/옵션 배열을 인자로 받습니다:

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

다른 콘솔 명령어를 호출하면서 모든 출력을 숨기고 싶다면, `callSilently` 메서드를 사용할 수 있습니다. 이 메서드의 시그니처는 `call` 메서드와 같습니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 프로그램에게 종료를 요청할 때 사용합니다. Artisan 콘솔 명령어에서 이러한 시그널을 감지하고, 발생 시 특정 코드를 실행하려면 `trap` 메서드를 사용할 수 있습니다:

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

여러 개의 시그널을 동시에 감지하고 싶다면, 배열로 시그널 목록을 `trap`에 전달하세요:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan 콘솔의 `make` 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성하는 데 사용합니다. 이 클래스들은 입력값을 바탕으로 "스텁(stub)" 파일을 활용해 생성됩니다. 하지만, Artisan이 생성하는 파일에 일부 변경이 필요하다면, `stub:publish` 명령어로 자주 사용하는 스텁을 애플리케이션에 퍼블리시하여 직접 커스터마이징할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁은 애플리케이션 루트의 `stubs` 디렉토리에 위치하게 됩니다. 스텁 파일을 수정하면, 관련 `make` 명령어로 클래스를 생성할 때 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan 명령어 실행 시, Artisan은 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 실행을 시작하자마자 발생하고, `CommandStarting` 이벤트는 개별 명령어가 실행되기 직전에 발생합니다. 마지막으로, `CommandFinished` 이벤트는 명령어 실행이 끝나면 발생합니다.
