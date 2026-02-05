# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [단일 실행(격리) 명령어](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그램 코드로 명령어 실행](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 기본 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트 디렉터리에 `artisan` 스크립트로 존재하며, 애플리케이션 개발을 도와주는 다양한 유용한 명령어들을 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용하면 됩니다:

```shell
php artisan list
```

각 명령어는 해당 명령어의 사용 가능한 인수와 옵션을 보여주는 “help” 화면도 포함하고 있습니다. 도움말 화면을 보려면, `help` 뒤에 명령어 이름을 붙여 실행하면 됩니다:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/master/sail)을 로컬 개발환경으로 사용한다면, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크를 위한 강력한 REPL로, [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동됩니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 그러나 Tinker를 애플리케이션에서 제거한 적이 있다면, Composer를 사용해 다음과 같이 재설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 실시간 코드 반영(핫 리로딩), 멀티라인 코드 편집, 자동완성을 원하신다면 [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 명령줄에서 Eloquent 모델, 작업(jobs), 이벤트(events) 등 전체 Laravel 애플리케이션과 상호작용할 수 있습니다. Tinker 환경에 진입하려면 다음과 같이 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령어를 사용하여 Tinker의 설정 파일을 배포할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣기 위해 가비지 컬렉션(garbage collection)에 의존합니다. 따라서 Tinker를 사용할 때는 `Bus::dispatch` 혹은 `Queue::push`를 이용해 작업을 디스패치해야 합니다.

<a name="command-allow-list"></a>
#### 명령어 허용 목록

Tinker는 셸 내에서 실행할 수 있는 Artisan 명령어를 지정하는 "허용 목록"을 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하고자 하면, `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭 적용 제외 클래스

보통 Tinker에서는 Tinker 내에서 사용하는 클래스에 대해 자동으로 별칭을 적용합니다. 하지만, 특정 클래스에 대해서는 절대로 별칭을 적용하지 않도록 설정할 수 있습니다. 해당 클래스들을 `tinker.php` 설정 파일의 `dont_alias` 배열에 명시하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan에서 제공하는 기본 명령어 외에도, 직접 커스텀 명령어를 작성할 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉터리에 저장하지만, [Artisan 명령어로 검색할 디렉터리 지정](#registering-commands)을 통해 자유롭게 다른 위치에 저장할 수도 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어를 실행하면 `app/Console/Commands` 디렉터리에 새로운 명령어 클래스가 생성됩니다. 이 디렉터리가 없더라도 걱정하지 마세요. `make:command` Artisan 명령어를 처음 실행할 때 Laravel이 자동으로 생성해줍니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한, `signature` 속성을 통해 [명령어의 입력 기대값](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 이곳에 명령어의 핵심 로직을 작성하면 됩니다.

예시 명령어를 살펴보겠습니다. `handle` 메서드를 통해 필요한 의존성을 주입받을 수 있습니다. Laravel의 [서비스 컨테이너](/docs/master/container)는 이 메서드 시그니처에 타입힌트로 명시한 모든 의존성을 자동으로 주입합니다:

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
> 코드의 재사용성을 높이기 위해, 콘솔 명령어 클래스는 가급적 가볍게 유지하고 핵심 비즈니스 로직은 별도의 애플리케이션 서비스에 위임하는 것이 좋습니다. 위의 예시에서도 이메일 전송의 실제 처리는 서비스 클래스로 분리하여 의존성 주입을 통해 해결하고 있습니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무 것도 반환하지 않고 명령어가 정상적으로 실행되면, 명령어는 성공을 의미하는 `0` 종료 코드로 종료됩니다. 하지만 명령어의 종료 코드를 직접 지정하고자 한다면 `handle` 메서드에서 정수값을 반환할 수 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내부의 어느 위치에서든 명령어를 즉시 "실패" 처리하고 종료시키고 싶다면, `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어 실행을 종료시키고, 종료 코드 `1`을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스 정의 대신 클로저로 콘솔 명령어를 작성할 수 있는 대안입니다. 라우트에서 클로저로 제어기를 대신할 수 있듯이, 명령어에서도 클로저를 클래스의 대안으로 사용할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션으로 진입하는 콘솔 기반 "진입점(라우트)"들을 정의합니다. 이 파일 안에서 `Artisan::command` 메서드를 이용해 클로저 기반 명령어를 모두 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 인수/옵션을 받는 클로저를 인수로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 내부적으로 명령어 인스턴스에 바인딩되므로, 일반 명령어 클래스에서 사용할 수 있는 모든 도우미 메서드에 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저는 명령어의 인수나 옵션 외에도 추가로 필요로 하는 의존성을 [서비스 컨테이너](/docs/master/container)를 통해 타입힌트로 받아올 수 있습니다:

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

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 이용해 명령어에 대한 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어를 실행할 때 출력됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 단일 실행(격리) 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

특정 명령어가 한 번에 한 인스턴스만 실행되도록 보장하고 싶을 때도 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다:

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

명령어를 `Isolatable`로 지정하면, `--isolated` 옵션이 명령어에 자동으로 추가되며 별도로 옵션을 정의할 필요가 없습니다. 해당 옵션과 함께 명령어를 실행하면 Laravel은 동일 명령어의 다른 인스턴스가 실행 중인지 확인하여, 이미 실행 중이라면 새 인스턴스가 실행되지 않도록 보장합니다. 이 기능은 기본 캐시 드라이버를 사용해 원자적 락을 획득함으로써 동작합니다. 만약 다른 인스턴스가 실행 중이라면, 명령어는 실행하지 않고, 성공 상태 코드로 그냥 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행되지 못했을 때 반환할 종료 상태 코드를 직접 지정하려면, `isolated` 옵션에 원하는 값을 지정할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어 이름을 사용해 캐시에 원자적 락을 걸 때 사용할 문자열 키를 생성합니다. 명령어 인수나 옵션 값을 락 키에 포함하고 싶다면, 명령어 클래스에 `isolatableId` 메서드를 정의해 커스터마이징할 수 있습니다:

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

기본적으로 격리 락은 명령어가 종료될 때 해제됩니다. 만약 명령어가 중단되어 정상 종료되지 못하면, 한 시간 후에 락이 만료됩니다. 원하는 만료 시간을 지정하고 싶다면, 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의할 수 있습니다:

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대값 정의

콘솔 명령어를 작성하다 보면 사용자로부터 인수나 옵션을 입력받을 일이 많습니다. Laravel에서는 `signature` 속성을 사용해, 어떤 입력을 받을지 매우 직관적이고, 한 줄의 라우트 문법처럼 간편하게 정의할 수 있습니다.

<a name="arguments"></a>
### 인수

모든 사용자 입력 인수와 옵션은 중괄호로 감싸서 정의합니다. 아래 예시에서는, `user`라는 필수 인수 하나를 갖는 명령어입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나 기본값을 정의할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 선택적 인수에 기본값 설정...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션 역시 인수와 비슷하게 사용자 입력의 한 형태입니다. 옵션은 커맨드라인에서 두 개의 하이픈(`--`)으로 앞에 붙여 전달합니다. 옵션에는 값을 받을 수도 있고, 값을 받지 않고 단순한 불리언 "스위치"로 동작할 수도 있습니다. 아래와 같은 스위치 옵션 예시를 살펴보세요:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

여기서 `--queue` 스위치는 명령어 호출 시 지정할 수 있습니다. 해당 스위치가 전달되면 그 값은 `true`, 지정되지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 필요한 옵션

값을 전달해야 하는 옵션도 있습니다. 사용자가 반드시 값을 입력해야 할 옵션은 옵션 이름 뒤에 `=` 기호를 붙입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 사용자는 아래와 같이 값을 전달할 수 있으며, 값이 전달되지 않으면 기본값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정할 수도 있습니다. 사용자가 값을 지정하지 않으면 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 정의 시 단축키(축약어)를 지정하려면 옵션 이름 앞에 단축키를 쓰고, 전체 옵션명과는 `|` 문자로 구분합니다:

```php
'mail:send {user} {--Q|queue=}'
```

명령어를 터미널에서 실행할 때는 단축키는 한 개의 하이픈(`-`)을 붙이고, 값은 `=` 없이 바로 붙입니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 입력값을 받아야 하는 인수나 옵션이 있다면, 이름에 `*` 기호를 붙여 배열로 받을 수 있습니다. 인수 예시는 다음과 같습니다:

```php
'mail:send {user*}'
```

다음과 같이 실행하면 `user` 인수를 배열로 받게 됩니다. 예를 들어 아래 명령어에서는 `user`가 `[1, 2]` 배열로 해석됩니다:

```shell
php artisan mail:send 1 2
```

`*` 기호는 선택적 인수와 함께 써서 0개 이상의 인수를 허용할 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받아야 할 옵션을 정의할 때는 각 값마다 옵션 이름을 앞에 붙여 전달해야 합니다:

```php
'mail:send {--id=*}'
```

이 명령어는 아래와 같이 여러 `--id` 옵션을 전달해서 실행할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수나 옵션마다 설명을 추가하고 싶을 때는, 이름 뒤에 콜론(`:`)을 붙여 설명을 작성하면 됩니다. 명령어 정의가 너무 길어지면 여러 줄로 나누어도 됩니다:

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

명령어에 필수 인수가 있는데 사용자가 이를 입력하지 않으면, 기본적으로 에러 메시지가 출력됩니다. 혹은 사용자가 필수 입력을 누락했을 때, 자동으로 프롬프트를 띄워 입력을 받을 수도 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하면 됩니다:

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

Laravel이 사용자로부터 필수 인수를 입력받아야 할 때, 인수 이름이나 설명을 활용해 적절한 질문을 자동으로 출력하고 입력을 요청합니다. 질문 문구를 직접 커스터마이즈하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현해서 인수 이름을 키로 하는 질문 배열을 반환하면 됩니다:

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

플레이스홀더(placeholder) 텍스트가 필요하다면 질문, 플레이스홀더 쌍을 튜플로 제공할 수 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트를 완전히 커스터마이즈하려면, 클로저를 제공하고 사용자 입력을 직접 처리해 반환할 수도 있습니다:

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
Laravel의 전체 [Prompts](/docs/master/prompts) 문서에서 다양한 프롬프트 관련 기능과 활용법을 확인할 수 있습니다.

[옵션](#options)에 대해 사용자 선택을 프롬프트로 받고 싶다면, 명령어의 `handle` 메서드에서 프롬프트를 작성할 수 있습니다. 그러나 사용자가 필수 인수를 자동으로 프롬프트받는 경우에만 추가로 프롬프트를 띄우고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하면 됩니다:

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

명령어를 실행하는 도중, 사용자가 입력한 인수와 옵션 값을 받아올 수 있습니다. 인수와 옵션은 각각 `argument`, `option` 메서드를 사용해 가져옵니다. 해당 값이 없으면 `null`이 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한 번에 가져오려면 `arguments` 메서드를 사용하세요:

```php
$arguments = $this->arguments();
```

옵션 역시 `option` 메서드로 가져오고, 모든 옵션을 배열로 얻으려면 `options` 메서드를 사용합니다:

```php
// 특정 옵션 하나를 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/master/prompts)는 커맨드라인 애플리케이션에 직관적인 폼(입력창)과 플레이스홀더, 유효성 검증 등 브라우저 비슷한 사용자 경험을 제공하는 PHP 패키지입니다.

출력뿐만 아니라, 명령어 실행 도중 사용자에게 직접 질문을 하고 응답을 받을 수도 있습니다. `ask` 메서드는 주어진 질문으로 사용자에게 입력을 요청하고, 사용자의 응답을 반환합니다:

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

`ask` 메서드의 두 번째 인수로 기본값을 지정할 수도 있습니다. 입력하지 않으면 이 값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 질문은 동일하나 입력 중에 글자가 표시되지 않습니다. 주로 비밀번호 등 민감한 정보 입력에 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(yes/no) 질문

사용자에게 간단한 "예/아니오" 확인을 요청하려면, `confirm` 메서드를 사용할 수 있습니다. 기본적으로 `no`로 간주되어 `false`가 반환되고, 사용자가 `y` 또는 `yes`를 입력하면 `true`가 반환됩니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요하다면 두 번째 인자에 `true`를 지정해 기본값을 "예"로 만들 수 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드를 사용하면, 입력값에 따라 자동완성 후보를 미리 제시할 수 있습니다. 사용자는 자동완성 목록이 아니라도 원하는 값을 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는, 두 번째 인자로 클로저를 전달해 입력할 때마다 동적으로 자동완성 후보를 생성할 수도 있습니다. 클로저는 입력값을 받아, 자동완성 후보 배열을 반환해야 합니다:

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

사용자에게 미리 정의된 선택지 중에서 입력을 받으려면 `choice` 메서드를 사용할 수 있습니다. 세 번째 인자로 배열의 인덱스를 전달해, 사용자가 아무 것도 선택하지 않을 경우 반환될 기본값을 지정할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한, 네 번째, 다섯 번째 인자를 통해 정답 선택 최대 시도 횟수 설정, 다중 선택 허용 여부도 지정할 수 있습니다:

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

콘솔 창에 출력을 표시하려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 색깔로 메시지를 출력합니다. 예를 들어, 일반 정보는 `info`를 사용하고, 보통 녹색으로 표시됩니다:

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

에러 메시지는 `error`를 사용하며, 보통 빨간색으로 출력됩니다:

```php
$this->error('Something went wrong!');
```

기본 색 없이 평범한 텍스트를 출력하려면 `line`을 사용하세요:

```php
$this->line('Display this on the screen');
```

공백 줄을 출력할 때는 `newLine`을 사용합니다:

```php
// 한 줄 공백...
$this->newLine();

// 세 줄 공백...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행과 컬럼으로 이루어진 데이터를 보기 좋게 출력할 수 있도록 도와줍니다. 컬럼명과 테이블 데이터를 전달하면 Laravel이 자동으로 테이블의 폭과 높이를 계산해 출력해줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 프로그레스 바

오래 걸리는 작업의 경우, 진행 상황을 한눈에 보여주는 프로그레스 바가 유용합니다. `withProgressBar` 메서드를 사용하면, 주어진 iterable 컬렉션을 순회하며 각 항목마다 진행률을 표시합니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

좀 더 수동으로 프로그레스 바를 제어해야 할 때도 있습니다. 먼저 전체 반복 횟수를 지정하고, 각 항목을 처리한 뒤에 바를 직접 이동시키면 됩니다:

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
> 보다 고급 기능이 궁금하다면, [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

Laravel은 기본적으로 `app/Console/Commands` 디렉터리 내의 모든 명령어를 자동으로 등록합니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용해 다른 디렉터리도 Artisan 명령어로 스캔하도록 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면, 명령어 클래스 이름을 직접 지정해 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션 내 모든 명령어가 [서비스 컨테이너](/docs/master/container)에 의해 해석되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램 코드로 명령어 실행

간혹, CLI에서가 아니라 코드 내(예: 라우트나 컨트롤러)에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. 첫 번째 인자로 명령어 시그니처 이름이나 클래스 이름을, 두 번째 인자로 명령어 인수/옵션 배열을 넘기며, 반환값으로는 종료 코드가 리턴됩니다:

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

혹은 전체 Artisan 명령어를 문자열로 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어의 옵션에 배열 타입을 정의했다면, 옵션의 값으로 배열을 넘길 수 있습니다:

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

문자열 값을 허용하지 않는 옵션(예: `migrate:refresh` 명령의 `--force`)에 값을 지정해야 한다면, `true` 또는 `false`를 값으로 넘겨야 합니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용해 Artisan 명령어 실행도 [큐 워커](/docs/master/queues)가 백그라운드에서 처리할 수 있도록 큐잉할 수 있습니다. 이 기능을 쓰려면 큐 설정을 마치고 워커를 실행해야 합니다:

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

`onConnection`과 `onQueue` 메서드로 큐 연결명이나 사용할 큐 이름을 직접 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출

기존 Artisan 명령어 내에서 다른 명령어를 호출해야 하는 경우가 있습니다. `call` 메서드를 사용하면 명령어 이름과 인수/옵션 배열을 전달해 곧바로 호출할 수 있습니다:

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

다른 콘솔 명령어의 모든 출력을 숨기고 싶다면, `callSilently` 메서드를 사용할 수 있습니다. 사용 방법과 시그니처는 `call`과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제들은 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 프로그램에 종료 요청을 보낼 때 사용됩니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하고, 적절한 코드를 실행하고자 할 때는 `trap` 메서드를 사용할 수 있습니다:

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

여러 개의 시그널을 동시에 감지하려면, `trap` 메서드에 시그널 배열을 인자로 넘기면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan 콘솔의 `make` 명령어들은 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 만들어냅니다. 이 클래스들은 “스텁(stub)” 파일을 기반으로 생성되며, 여러분의 입력값에 따라 내부 값이 채워집니다. 만약 Artisan이 만들어내는 파일을 조금 수정하고 싶다면, `stub:publish` 명령어로 주요 스텁 파일들을 애플리케이션에 복사해서 원하는 대로 수정할 수 있습니다:

```shell
php artisan stub:publish
```

복사된 스텁 파일들은 애플리케이션 루트의 `stubs` 디렉터리에 생성됩니다. 여기서 스텁 파일을 수정하면, 해당 스텁을 기반으로 Artisan의 `make` 명령어를 실행할 때마다 변경 사항이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 세 가지 이벤트를 디스패치합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 실행을 시작하자마자 발생합니다. 이후, 각 명령어가 실행되기 직전에 `CommandStarting` 이벤트가, 명령어 실행이 끝나면 `CommandFinished` 이벤트가 차례로 발생합니다.
