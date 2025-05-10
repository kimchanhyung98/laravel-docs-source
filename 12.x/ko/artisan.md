# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 기반 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대값 정의하기](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열(Input Arrays)](#input-arrays)
    - [입력 설명(Input Descriptions)](#input-descriptions)
    - [누락된 입력값 프롬프트](#prompting-for-missing-input)
- [명령어 I/O](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [명령어 코드상 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [Signal 처리](#signal-handling)
- [스타브(Stub) 커스터마이징](#stub-customization)
- [이벤트(Events)](#events)

<a name="introduction"></a>
## 소개

Artisan은 라라벨에 기본적으로 포함되어 있는 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트 형태로 존재하며, 애플리케이션 개발을 도와주는 다양한 유용한 명령어들을 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

각각의 명령어에는 해당 명령어에서 사용할 수 있는 인수와 옵션을 보여주고 설명하는 "도움말" 화면도 포함되어 있습니다. 도움말을 보려면 명령어 이름 앞에 `help`를 붙여 실행하면 됩니다.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)을 로컬 개발 환경으로 사용하고 있다면, Artisan 명령어를 실행할 때는 반드시 `sail` 명령줄을 이용해야 합니다. Sail은 해당 명령어들을 애플리케이션의 Docker 컨테이너 안에서 실행시켜 줍니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 라라벨 프레임워크를 위한 강력한 REPL 환경(대화형 콘솔)로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작합니다.

<a name="installation"></a>
#### 설치

모든 라라벨 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 Tinker를 삭제했다면 Composer를 통해 Tinker를 재설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> 라라벨 애플리케이션을 터미널에서 다룰 때, 핫 리로딩, 여러 줄 코드 편집, 자동완성 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 참고해보세요!

<a name="usage"></a>
#### 사용 방법

Tinker를 사용하면 Eloquent 모델, 잡(jobs), 이벤트 등 라라벨 애플리케이션 전반을 명령줄에서 직접 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan tinker
```

Tinker의 설정 파일을 배포하고 싶다면 `vendor:publish` 명령어를 사용할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 가비지 컬렉션에 의존해서 잡을 큐에 올립니다. 따라서 tinker 사용 시에는 잡 디스패치를 위해 반드시 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 실행 허용 명령어 목록(Allow List)

Tinker는 쉘 내부에서 실행할 수 있는 Artisan 명령어를 "허용 목록(allow list)"으로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어만 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 별칭을 생성하지 않을 클래스 설정

일반적으로 Tinker는 사용자가 인터랙션하는 클래스들을 자동으로 별칭(alias) 처리해줍니다. 하지만 특정 클래스들은 절대 별칭을 생성하지 않게 하고 싶을 때도 있습니다. 이 경우 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan에서 기본 제공하는 명령어 이외에도, 직접 커스텀 명령어를 만들어 사용할 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉토리에 저장되지만, Composer로 로딩만 가능하다면 다른 위치에 저장해도 무방합니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새로운 명령어를 만들려면 `make:command` Artisan 명령어를 사용하면 됩니다. 이 명령어는 `app/Console/Commands` 디렉토리에 새로운 명령어 클래스를 생성합니다. 만약 이 디렉토리가 없다면, `make:command`를 처음 실행할 때 자동으로 만들어집니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 해당 클래스의 `signature`와 `description` 속성(property)에 적절한 값을 정의해야 합니다. 이 속성들은 `list` 명령어 등에서 명령어 정보를 표시할 때 사용됩니다. 또한 `signature` 속성을 통해 [명령어의 입력값에 대한 기대사항](#defining-input-expectations)도 함께 지정할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되며, 이 안에 명령어의 주요 로직을 작성하면 됩니다.

아래 예시를 살펴보면, `handle` 메서드를 통해 필요한 의존성도 요청할 수 있다는 점에 주목하세요. 라라벨의 [서비스 컨테이너](/docs/{{version}}/container)가 타입힌트된 모든 의존성을 자동으로 주입해줍니다.

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
> 코드 재사용성을 높이려면, 콘솔 명령어에는 꼭 필요한 최소한의 로직만 작성하고 복잡한 처리는 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예시에서도 메일 발송의 실제 처리는 별도의 서비스 클래스에 맡기고 있습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 정상적으로 종료되면, 명령어는 기본적으로 `0`의 종료 코드(성공)를 반환합니다. 필요하다면 `handle` 메서드에서 명시적으로 정수 값을 반환해 종료 코드를 지정할 수도 있습니다.

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내의 어느 위치에서든 명령어를 "실패" 상태로 종료하고 싶다면 `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령 실행을 중단하고, 종료 코드 `1`을 반환합니다.

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 기반 명령어

클로저(익명 함수) 기반 콘솔 명령어는 명령어 클래스를 따로 만들지 않고 간단하게 정의할 수 있는 방법입니다. HTTP 라우트를 정의할 때 컨트롤러 대신 클로저를 사용할 수 있는 것과 비슷하게, 콘솔 환경에서도 이를 대안으로 사용할 수 있습니다.

`routes/console.php` 파일은 실제로 HTTP 라우트를 정의하는 곳은 아니지만, 애플리케이션의 콘솔 기반 진입점(경로)들을 정의합니다. 이 파일 안에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 등록할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 클로저(인수와 옵션을 인자로 받는 함수) 두 가지를 인자로 받습니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 기본적으로 해당 명령어 인스턴스에 바인딩되어, 클래스 기반 명령어에서 사용 가능한 모든 헬퍼 메서드를 이용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 기반 명령어에서도 인수와 옵션 외에 추가로 필요한 의존성이 있다면, 서비스 컨테이너를 통해 타입힌트로 주입받을 수 있습니다.

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명 등록

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용해 명령어 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령어 실행 시 함께 표시됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

동일한 명령어의 인스턴스가 동시에 여러 개 실행되지 않게 하려면 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 명령어 클래스에 구현하면 됩니다.

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

명령어가 `Isolatable`로 표시되면, 라라벨이 자동으로 `--isolated` 옵션을 명령어에 추가합니다. 이 옵션으로 명령어를 실행하면 실행 중인 동일 명령어가 없는지 확인하여, 이미 실행되고 있다면 실행하지 않고 성공 상태의 종료 코드로 바로 종료됩니다. 라라벨은 이를 위해 애플리케이션의 기본 캐시 드라이버를 이용해 atomic lock을 획득하려 시도합니다.

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행되지 못했을 때 반환할 종료 상태 코드를 직접 지정하고 싶다면 `isolated` 옵션에 값을 할당할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### Lock ID

기본적으로 라라벨은 명령어의 이름을 사용해 캐시에 atomic lock을 위한 문자열 키를 생성합니다. 이 키를 커스터마이즈하려면 명령어 클래스에 `isolatableId` 메서드를 정의하고, 인수 및 옵션 값을 조합해 반환하면 됩니다.

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
#### Lock 만료 시간

기본적으로 격리(고립) 락은 명령어가 끝나면 해제되거나, 명령어가 중단되어 끝나지 못할 경우 1시간 후 만료됩니다. 락 만료 시점을 조정하고 싶다면 `isolationLockExpiresAt` 메서드를 추가해 원하는 만료 일시나 기간을 반환하면 됩니다.

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

콘솔 명령어를 작성할 때, 유저로부터 인수나 옵션 등의 입력을 받아야 할 일이 많습니다. 라라벨은 각 명령어의 `signature` 속성을 사용해 기대하는 입력값의 이름, 인수, 옵션을 쉽고 명확하게 한 줄의 라우트 시그니처 형태로 정의할 수 있게 해줍니다.

<a name="arguments"></a>
### 인수(Arguments)

모든 사용자 인수와 옵션은 중괄호로 감싸서 표시합니다. 아래 예시에서는 필수 인수로 `user`가 정의되어 있습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나, 기본값을 지정할 수도 있습니다.

```php
// 선택적 인수...
'mail:send {user?}'

// 기본값을 갖는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션도 인수와 마찬가지로 유저 입력의 한 형태입니다. 옵션은 커맨드라인에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값이 필요한 것과 필요하지 않은 것의 두 종류가 있습니다. 값이 필요하지 않은 옵션은 불리언 "스위치" 역할을 합니다. 예시를 보겠습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위처럼 `--queue` 스위치를 지정하며 명령어를 실행할 수 있습니다. 스위치가 주어지면 옵션 값은 `true`, 없으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값을 받는 옵션

옵션이 값을 반드시 받아야 할 때는, 옵션 이름 뒤에 `=` 기호를 붙여서 표시하면 됩니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이렇게 하면 사용자는 CLI에서 옵션에 값을 전달할 수 있습니다. 옵션이 지정되지 않으면 `null` 값을 갖습니다.

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 부여하려면 옵션 이름 뒤에 값으로 직접 쓸 수 있습니다. 사용자가 값을 지정하지 않으면 기본값이 사용됩니다.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션을 정의할 때 단축키(shortcut)를 부여하고 싶다면, 단축키를 옵션명 앞에 두고 `|` 기호로 구분하면 됩니다.

```php
'mail:send {user} {--Q|queue}'
```

명령어를 실행할 때 단축키는 하나의 하이픈만 붙이고, 값은 `=`를 사용하지 않습니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열(Input Arrays)

여러 개의 입력값이 가능한 인수나 옵션을 정의하려면 `*` 문자를 사용할 수 있습니다. 먼저 여러 개 값을 받을 수 있는 인수 예시를 살펴보겠습니다.

```php
'mail:send {user*}'
```

아래처럼 명령어에 여러 값을 전달하면, `user` 인수에는 배열 형태로 값이 들어갑니다(예를 들어 `1`과 `2`).

```shell
php artisan mail:send 1 2
```

`*` 문자는 선택적 인수와 결합해서, 0개 이상의 입력값을 받을 수도 있습니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받을 수 있는 옵션을 만들 때는 각 값마다 옵션 이름으로 프리픽스를 붙여 전달해야 합니다.

```php
'mail:send {--id=*}'
```

명령어를 실행할 때 아래처럼 여러 번 옵션을 전달합니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력값 설명 달기

인수나 옵션에 대해 설명을 달고 싶을 때는 이름 뒤에 콜론(:)을 붙여 설명을 추가할 수 있습니다. 명령어 정의가 길어진다면 여러 줄로 나눠 작성해도 괜찮습니다.

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
### 누락된 입력값 프롬프트

명령어에 필수 인수가 있지만 사용자가 입력하지 않으면, 일반적으로 에러 메시지가 표시됩니다. 하지만, `PromptsForMissingInput` 인터페이스를 구현하면 누락된 인수가 있을 때 자동으로 프롬프트를 띄워 사용자에게 값을 입력받을 수 있습니다.

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

라라벨은 필요한 인수를 자동으로 질문 형태로 사용자에게 요청합니다. 질문내용은 인수의 이름이나 설명을 기반으로 지능적으로 만들어집니다. 만약 출력되는 질문을 직접 커스터마이즈하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현해 인수 이름을 키로 하고 질문을 값으로 갖는 배열을 반환하면 됩니다.

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

질문과 함께 예시 입력을 플레이스홀더로 표시하고 싶다면 질문, 플레이스홀더 두 개를 포함하는 튜플 형태로 작성할 수 있습니다.

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트를 완전히 제어하고 싶으면, 값을 직접 요청하고 반환하는 클로저를 지정할 수도 있습니다.

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
> [Laravel Prompts](/docs/{{version}}/prompts) 공식 문서에서는 다양한 프롬프트의 사용법과 기능에 대해 더 자세히 안내하고 있습니다.

옵션([options](#options))을 선택하거나 값을 입력받기 위해 프롬프트를 띄우고 싶다면 명령어의 `handle` 메서드에서 직접 프롬프트 코드를 작성하면 됩니다. 자동 인수 프롬프트와 동시에 옵션도 프롬프트하고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하여 사용할 수 있습니다.

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

명령어가 실행되는 동안 인수나 옵션에 전달된 값을 가져와야 할 때가 많습니다. 이때는 `argument` 및 `option` 메서드를 사용할 수 있습니다. 해당 인수/옵션이 없다면 `null`을 반환합니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한 번에 가져오려면 `arguments` 메서드를 사용합니다.

```php
$arguments = $this->arguments();
```

옵션도 `option` 메서드를 통해 하나만 가져오거나, `options` 메서드로 모두 받아올 수 있습니다.

```php
// 특정 옵션만 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/{{version}}/prompts)는 아름답고 편리한 폼, 플레이스홀더, 유효성 검증 등 브라우저 같은 기능까지 명령줄에서 쓸 수 있는 PHP 패키지입니다.

명령어 실행 중 사용자에게 입력값을 직접 물어보고 싶다면 `ask` 메서드를 사용할 수 있습니다. 사용자가 입력한 값을 질문과 함께 받고, 입력값을 그대로 반환합니다.

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

`ask` 메서드는 두 번째 인자로 기본값을 지정할 수도 있으며, 입력이 없을 경우 이에 따라 반환값이 결정됩니다.

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 콘솔에 입력 내용이 보이지 않아 비밀번호 등 민감한 정보를 입력받을 때 유용합니다.

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(Yes/No) 프롬프트

사용자에게 단순한 "예/아니오" 확인이 필요하다면 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 사용자가 프롬프트에 `y` 또는 `yes`를 입력하면 `true`가, 그렇지 않으면 `false`가 반환됩니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

확인 프롬프트의 기본값을 `true`로 지정하고 싶다면, 두 번째 인자로 `true`를 전달할 수 있습니다.

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성(Auto-Completion)

`anticipate` 메서드는 선택 가능한 값에 대해 자동 완성을 지원합니다. 물론 사용자는 자동 완성 목록에 없는 값도 직접 입력할 수 있습니다.

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 자동 완성 값 자체를 클로저로 생성해, 사용자가 입력할 때마다 동적으로 옵션 목록을 만들 수도 있습니다.

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

미리 정의된 선택지 중에서 사용자가 하나(또는 여러 개)를 고르게 하려면 `choice` 메서드를 사용합니다. 세 번째 인자로 기본값의 배열 인덱스를 전달할 수 있으며, 네 번째/다섯 번째 인자는 최대 시도 횟수와 다중 선택 허용 여부를 지정합니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

기타 선택 옵션의 예시:

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
### 출력 작성하기

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 이 메서드들은 목적에 맞는 ANSI 색상을 자동 적용합니다. 예를 들어, 일반 정보를 표시할 때는 보통 `info`를 사용하며, 콘솔에서는 초록색으로 표시됩니다.

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

에러 메시지는 `error` 메서드를 사용하며, 빨간색으로 표시됩니다.

```php
$this->error('Something went wrong!');
```

색상 없이 간단히 메시지를 출력하려면 `line` 메서드를 사용합니다.

```php
$this->line('Display this on the screen');
```

빈 줄을 출력하고 싶을 때는 `newLine` 메서드를 사용할 수 있습니다.

```php
// 빈 줄 한 개 출력...
$this->newLine();

// 빈 줄 세 개 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 표 출력(Tables)

`table` 메서드를 사용하면 여러 행/열의 데이터를 손쉽게 표 형태로 출력할 수 있습니다. 컬럼명과 데이터 배열만 넘기면, 라라벨이 표 크기와 형식을 자동 계산해 예쁘게 보여줍니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률(Progress Bars)

작업 시간이 오래 걸릴 때 진행률 바를 표시해서 사용자가 현재 작업 진행 상황을 알 수 있게 할 수 있습니다. `withProgressBar` 메서드를 사용하면 iterable 값을 루프마다 하나씩 처리할 때마다 진행률이 자동으로 표시됩니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

좀 더 세밀하게 진행률 바의 상태를 제어하고 싶다면, 전체 단계 수를 지정한 뒤, 각각의 항목 처리가 끝날 때마다 수동으로 단계를 넘기면 됩니다.

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
> 보다 다양한 기능 및 고급 진행률 표시 옵션이 궁금하다면 [Symfony Progress Bar component 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

기본적으로 라라벨은 `app/Console/Commands` 디렉토리 안의 모든 명령어를 자동으로 등록합니다. 만약 다른 디렉토리도 Artisan 명령어 스캔 대상에 추가하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용할 수 있습니다.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요할 경우, 명령어 클래스명을 직접 지정해서 수동으로 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때 애플리케이션의 모든 명령어가 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석되어 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 명령어 코드상 실행하기

때로는 CLI가 아닌 환경(예: 라우트, 컨트롤러 등)에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인자로 명령어의 시그니처 이름이나 클래스명을, 두 번째 인자에는 명령어 파라미터 배열을 받으며, 반환값으로 종료 코드를 돌려줍니다.

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

또한 전체 Artisan 명령어를 문자열 형태로 `call` 메서드에 그대로 넘길 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어 옵션이 배열 값을 받을 수 있도록 정의되었다면, 옵션 값에 PHP 배열을 그대로 넘길 수 있습니다.

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

문자열 값이 아닌 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그 등)에 값을 넘길 때는 `true` 또는 `false`를 전달하면 됩니다.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어를 큐잉 처리하기

`Artisan` 파사드의 `queue` 메서드를 이용하면 Artisan 명령어를 큐에 넣어 비동기로 실행(백그라운드에서 처리)할 수도 있습니다. 사용 전 반드시 큐 설정을 마치고 워커를 실행 중이어야 합니다.

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`과 `onQueue` 메서드를 이용하면 명령어를 실행시킬 큐 커넥션이나 큐 채널까지 지정할 수 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

한 명령어 내에서 다른 Artisan 명령어를 호출하고 싶을 때는 `call` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 이름과 인수/옵션 배열을 인자로 받습니다.

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

만약 호출한 명령어의 출력을 모두 숨기고 싶다면 `callSilently` 메서드를 사용하면 됩니다. 시그니처는 `call`과 동일합니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## Signal 처리

운영 체제에서는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램 종료 요청 신호입니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하고, 신호가 발생했을 때 특정 코드를 실행하고 싶다면 `trap` 메서드를 사용할 수 있습니다.

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

한 번에 여러 시그널을 감지하고 싶으면 `trap` 메서드에 시그널 배열을 넘기면 됩니다.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스타브(Stub) 커스터마이징

Artisan 콘솔의 `make` 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 이 클래스들은 "스타브(stub)" 파일을 기반으로 자동 생성됩니다. Artisan이 생성하는 파일을 조금 다르게 만들어야 할 때는 `stub:publish` 명령어로 필요한 스타브 파일을 애플리케이션에 배포해 원하는 대로 수정할 수 있습니다.

```shell
php artisan stub:publish
```

배포된 스타브 파일들은 애플리케이션 루트의 `stubs` 디렉토리 안에 위치합니다. 이 파일들을 수정하면 이후 Artisan의 `make` 명령어를 통해 클래스를 생성할 때 변경 사항이 그대로 반영됩니다.

<a name="events"></a>
## 이벤트(Events)

Artisan으로 명령어를 실행할 때는 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
ArtisanStarting 이벤트는 Artisan이 실행을 시작할 때 바로 발생하고, CommandStarting 이벤트는 개별 명령어를 실행하기 직전에 발생합니다. 마지막으로 CommandFinished 이벤트는 명령어 실행이 종료되면 발생합니다.
