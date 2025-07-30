# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 기반 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [입력이 누락된 경우 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력 값 조회](#retrieving-input)
    - [사용자 입력 받기](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [명령어의 코드 실행](#programmatically-executing-commands)
    - [다른 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁(stub) 커스터마이즈](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

아티즌(Artisan)은 라라벨에 기본 포함되어 있는 명령줄 인터페이스입니다. 아티즌은 애플리케이션 루트 디렉터리에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움을 주는 다양한 유용한 명령어를 제공합니다. 사용 가능한 모든 아티즌 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

각 명령어에는 "도움말" 화면이 포함되어 있어서, 명령어의 사용 가능한 인수와 옵션을 보여주고 설명합니다. 도움말 화면을 확인하려면 명령어 이름 앞에 `help`를 붙여주세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우, 아티즌 명령어를 실행할 때 반드시 `sail` 커맨드라인을 사용해야 합니다. Sail을 사용하면, 아티즌 명령어가 애플리케이션의 Docker 컨테이너 안에서 실행됩니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 라라벨 프레임워크를 위한 강력한 REPL이며, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작합니다.

<a name="installation"></a>
#### 설치

모든 라라벨 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 애플리케이션에서 Tinker를 제거했다면, Composer를 통해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> 라라벨 애플리케이션을 다루며, 핫 리로딩, 여러 줄 코드 편집, 자동완성 기능을 원하시나요? [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 Eloquent 모델, 잡(jobs), 이벤트 등 전체 라라벨 애플리케이션과 명령줄로 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` 아티즌 명령어를 실행하세요.

```shell
php artisan tinker
```

Tinker의 설정 파일을 `vendor:publish` 명령어로 배포할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 가비지 컬렉션(garbage collection)에 의존하여 잡을 큐에 등록합니다. 따라서 Tinker를 사용할 때는 잡을 등록할 때 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 허용 명령어 리스트

Tinker는 쉘 환경에서 실행할 수 있는 아티즌 명령어를 "허용 리스트" 방식으로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 추가로 실행하고 싶은 명령어가 있다면, `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭하지 않을 클래스 지정

일반적으로 Tinker는 사용 중인 클래스들을 자동으로 별칭(aliased) 처리합니다. 그러나 특정 클래스는 별칭 처리하지 않도록 할 수도 있습니다. 이때는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하세요.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

아티즌에 기본 제공되는 명령어 외에도, 직접 커스텀 명령어를 만들어 사용할 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, [다른 디렉터리도 아티즌 명령어 위치로 스캔하도록](#registering-commands) 자유롭게 지정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 생성하려면 `make:command` 아티즌 명령어를 사용하세요. 이 명령어는 새로운 명령어 클래스를 `app/Console/Commands` 디렉터리에 만들어줍니다. 만약 애플리케이션에 이 디렉터리가 없다면, `make:command` 명령을 처음 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성(property)에 적절한 값을 지정해야 합니다. 이 값들은 `list` 화면에서 명령어를 표시할 때 사용됩니다. 또한, `signature` 속성은 [명령어에 필요한 입력 값(인수/옵션)](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 실제 명령어의 로직은 이 메서드에 작성하면 됩니다.

아래는 예시 명령어입니다. `handle` 메서드를 통해 필요한 의존성(서비스 등)도 요청할 수 있습니다. 라라벨 [서비스 컨테이너](/docs/12.x/container)는 타입힌트된 모든 의존성을 자동 주입해줍니다.

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
> 코드의 재사용성을 높이기 위해, 명령어 클래스는 최소한의 로직만 넣고, 주요 작업은 애플리케이션 서비스로 위임하는 것이 좋습니다. 위 예시에서도 이메일 발송에 대한 "핵심 작업"은 서비스 클래스로 분리했습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무 것도 반환하지 않고 명령어가 정상적으로 완료되면, 성공을 의미하는 `0` 종료 코드로 종료됩니다. 하지만, `handle` 메서드에서 정수형 값을 반환하여 명령어의 종료 코드를 직접 지정할 수도 있습니다.

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내에서 언제든 "실패"로 종료시키고 싶다면, `fail` 메서드를 사용할 수 있습니다. `fail`은 즉시 명령어 실행을 중단하고 종료 코드 1을 반환합니다.

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 기반 명령어

클로저(closure)를 이용해 명령어 클래스를 따로 만들지 않고도 콘솔 명령어를 정의할 수 있습니다. 라우트 클로저를 사용하는 것과 비슷하게, 명령어 클로저는 명령어 클래스의 대안입니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않고, 애플리케이션의 콘솔 진입 지점(라우트)들을 정의합니다. 이 파일에서 `Artisan::command` 메서드로 모든 클로저 기반 명령어를 등록할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 명령어의 인수·옵션을 받는 클로저를 인수로 받습니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

이 클로저는 내부적으로 명령어 인스턴스와 연결(바인딩)되어, 일반 명령어 클래스에서 사용할 수 있는 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

명령어 클로저는 명령어 인수·옵션 외에도, [서비스 컨테이너](/docs/12.x/container)에서 해결되어야 할 추가 의존성도 타입힌트로 받을 수 있습니다.

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

클로저 기반 명령어를 정의할 때 `purpose` 메서드를 이용하여 명령어 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령 실행 시 표시됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 합니다. 또한 여러 서버가 있다면, 각 서버가 동일한 중앙 캐시 서버와 통신하고 있어야 합니다.

때때로 하나의 명령어 인스턴스만 동시에 실행되도록 보장하고 싶을 수 있습니다. 이런 경우 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

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

명령어에 `Isolatable`을 지정하면, 별도로 옵션을 정의하지 않아도 해당 명령어에 자동으로 `--isolated` 옵션이 추가됩니다. 이 옵션을 사용해 명령어를 실행하면, 이미 동일한 명령어가 실행 중인지 라라벨이 확인합니다. 이를 위해 라라벨은 애플리케이션의 기본 캐시 드라이버를 활용해 원자적(atomic)으로 락을 시도합니다. 다른 인스턴스가 이미 실행 중이면 명령어는 실행되지 않으며, 성공적인 종료 상태 코드로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행되지 못했을 때 반환할 종료 상태 코드를 지정하고 싶다면, `isolated` 옵션에 원하는 값으로 지정할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 라라벨은 명령어 이름을 사용해 캐시에 사용할 문자열 키를 생성합니다. 하지만 `isolatableId` 메서드를 Artisan 명령어 클래스에 정의하여, 명령어의 인수나 옵션 값을 키에 조합하는 등 이 키 값을 커스터마이즈할 수 있습니다.

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

기본적으로 격리 락은 명령어 실행이 종료되면 해제됩니다. 또는 명령어가 중단되어 정상 종료되지 못하면 1시간 뒤 만료됩니다. 커스텀 락 만료 시간이 필요하다면, 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의해 지정할 수 있습니다.

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
## 입력 기대 정의

콘솔 명령어를 작성할 때는 사용자로부터 인수(argument) 또는 옵션(option) 형태로 입력을 받는 경우가 많습니다. 라라벨에서는 명령어 클래스의 `signature` 속성을 이용해, 기대하는 입력 값을 매우 편리하게 정의할 수 있습니다. `signature` 속성 하나로 명령어의 이름, 인수와 옵션을 한 번에 간결한 라우트(route) 문법처럼 지정합니다.

<a name="arguments"></a>
### 인수

사용자가 입력하는 모든 인수(arguments)와 옵션(options)은 중괄호로 감쌉니다. 아래 예시는 필수 인수인 `user`를 정의한 예입니다.

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

// 선택적 인수 + 기본값 지정...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션(option)도 인수와 마찬가지로 사용자 입력을 받는 한 형태입니다. 옵션은 커맨드라인에서 `--`(하이픈 두 개)로 시작합니다. 옵션에는 값이 없는 "스위치"형과, 값을 받는 옵션이 있습니다. 값이 없는 옵션(스위치)은 true/false 부울 형식으로 사용할 수 있습니다. 예시를 봅시다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서 `--queue` 스위치는 아티즌 명령어를 호출할 때 추가할 수 있습니다. 만약 `--queue`를 지정하면, 옵션 값은 `true`가 되고, 그렇지 않으면 `false`입니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

이번엔 사용자가 값을 꼭 지정해야 하는 옵션의 예시를 봅시다. 옵션 이름 뒤에 `=`를 붙여주면, 값 입력이 필수임을 의미합니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이렇게 정의하면, 사용자는 다음과 같이 값을 전달할 수 있습니다. 옵션이 지정되지 않으면 값은 `null`입니다.

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하고 싶을 때는, 옵션 이름 뒤에 바로 값으로 지정하면 됩니다. 사용자가 옵션 값을 전달하지 않으면, 기본값이 사용됩니다.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정하려면, 옵션 정의 시 단축키를 옵션 이름 앞에 두고, `|` 문자를 구분자로 사용하세요.

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어를 실행할 때 단축키 형태로 옵션 값을 전달하면, 하이픈 한 개를 접두어로 사용하며, `=` 문자는 포함하지 않습니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 개의 값 입력을 기대하는 인수 또는 옵션을 정의하고 싶다면, `*` 문자를 사용할 수 있습니다. 먼저, 인수에 적용하는 예시입니다.

```php
'mail:send {user*}'
```

이렇게 정의하면 명령어 실행 시 `user` 인수를 여러 개 전달할 수 있고, 예시의 아래 명령어는 `user`의 값이 `[1, 2]`가 됩니다.

```shell
php artisan mail:send 1 2
```

`*`를 선택적 인수와 조합할 수도 있어, 인수를 0개 이상 입력할 수 있습니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 개의 입력 값을 받는 옵션을 정의할 때도, 각 값마다 옵션 이름을 붙여서 전달해야 합니다.

```php
'mail:send {--id=*}'
```

이런 명령어는 아래처럼 옵션을 여러 번 전달해서 사용할 수 있습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수와 옵션에 설명을 추가하려면, 인수/옵션 이름 뒤에 콜론(`:`)과 설명을 함께 작성하면 됩니다. 한 줄에 정의가 길어질 경우, 여러 줄에 나눠 작성할 수 있습니다.

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
### 입력값 누락 시 프롬프트

명령어에 필수 인수가 포함되어 있지만, 사용자가 이를 생략한 경우 라라벨은 기본적으로 오류 메시지를 출력합니다. 하지만, 명령어 클래스에서 `PromptsForMissingInput` 인터페이스를 구현하면, 라라벨이 누락된 필수 인수에 대해 사용자에게 직접 질문을 던지도록 할 수 있습니다.

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

라라벨이 필수 입력값을 받아야 할 때, 인수 이름이나 설명을 참고하여 자동으로 질문을 생성해 사용자의 입력을 받습니다. 만약 질문 내용을 직접 지정하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현하면 됩니다. 이 메서드는 인수 이름을 키로 하는 질문 배열을 반환해야 합니다.

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

튜플(tuple) 형태로, 플레이스홀더 문구도 같이 제공할 수 있습니다.

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트를 더욱 완전히 커스터마이즈하고 싶을 경우, 사용자에게 질문을 던지고 답변을 반환하는 클로저를 제공할 수도 있습니다.

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
> [Laravel Prompts](/docs/12.x/prompts) 공식 문서에서 추가적인 프롬프트 및 사용법 정보를 확인할 수 있습니다.

사용자가 [옵션](#options)을 입력하도록 프롬프트를 띄우고 싶다면, 명령어의 `handle` 메서드 안에서 직접 프롬프트를 사용할 수도 있습니다. 만약 누락된 인수를 질문해서 받은 뒤에만 프롬프트를 띄우고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하면 됩니다.

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
### 입력 값 조회

명령어 실행 중에는, 명령어가 받은 인수와 옵션의 값을 코드에서 읽어야 할 수 있습니다. 이 때, `argument`와 `option` 메서드를 사용할 수 있습니다. 인수나 옵션이 존재하지 않으면 `null`을 반환합니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한 번에 조회하고 싶으면 `arguments` 메서드를 호출하면 됩니다.

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 `option` 메서드를 사용해 하나만, `options`로 모두 배열로 받으면 됩니다.

```php
// 특정 옵션 조회...
$queueName = $this->option('queue');

// 전체 옵션 배열로 조회...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 사용자 입력 받기

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령줄 애플리케이션에 브라우저처럼 플레이스홀더, 유효성 검사 등이 적용된 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지입니다.

명령어 실행 중에 사용자에게 입력을 요구하는 것도 가능합니다. `ask` 메서드는 질문을 표시하고, 사용자의 답변을 입력받아 반환합니다.

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

`ask` 메서드 두 번째 인수로, 사용자가 아무 값을 입력하지 않았을 때 반환할 기본값을 지정할 수도 있습니다.

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 사용자가 콘솔에 입력하는 동안 입력 값이 화면에 보이지 않습니다. 비밀번호처럼 민감한 정보 입력에 사용할 수 있습니다.

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(yes/no) 입력 받기

단순한 "네/아니오" 형태의 확인을 받고 싶다면, `confirm` 메서드를 사용할 수 있습니다. 이 메서드는 기본적으로 `false`를 반환하지만, 사용자가 `y` 또는 `yes`로 답변하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요에 따라 두 번째 인수로 `true`를 전달하면, 프롬프트의 기본값을 `true`로 지정할 수도 있습니다.

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 여러 선택지(힌트) 중 자동완성이 필요한 경우에 사용할 수 있습니다. 사용자는 자동완성 힌트와 상관없이 임의의 값을 입력할 수 있습니다.

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 전달해 실시간 입력에 따라 동적으로 자동완성 목록을 제공할 수도 있습니다.

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

사용자에게 미리 정의된 선택 목록 중 하나(또는 여러 개)를 선택하게 하고 싶다면, `choice` 메서드를 사용할 수 있습니다. 세 번째 인수로 기본으로 선택될 인덱스를 전달할 수 있습니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한 네 번째, 다섯 번째 인수로 각각 최대 시도 횟수와 다중 선택 허용 여부도 지정할 수 있습니다.

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

콘솔로 텍스트를 출력하려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 컬러로 출력합니다. 예를 들어, `info`는 일반적으로 콘솔에서 녹색 글씨로 표시됩니다.

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

오류 메시지를 표시하려면 `error` 메서드를 사용하세요. 에러 메시지는 보통 빨간색으로 표시됩니다.

```php
$this->error('Something went wrong!');
```

색상 없는 일반 텍스트는 `line`을 사용해서 출력할 수 있습니다.

```php
$this->line('Display this on the screen');
```

빈 줄을 출력하려면 `newLine`을 사용합니다.

```php
// 빈 줄 1개 출력
$this->newLine();

// 빈 줄 3개 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행/열로 구성된 데이터를 보기 좋게 포맷해주는 기능입니다. 컬럼 이름과 데이터 배열만 전달하면, 라라벨이 자동으로 너비와 높이를 계산하여 테이블로 표시합니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행바(Progress Bar)

작업 시간이 긴 명령어에서는 현재 진행률을 보여주는 진행바를 표시할 수 있습니다. `withProgressBar` 메서드를 사용하면, 주어진 반복 가능한 값(iterable)을 순회할 때마다 진행바가 자동으로 업데이트됩니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

진행률 제어를 더 세밀하게 하고 싶을 때는, 전체 반복 횟수를 먼저 정하고, 각 아이템마다 진행바를 직접 한 칸씩 증가시킬 수 있습니다.

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
> 더 다양한 옵션이 필요하다면 [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

기본적으로 라라벨은 `app/Console/Commands` 디렉터리 내의 모든 명령어를 자동으로 등록합니다. 만약 다른 디렉터리에도 아티즌 명령어가 있다면, 애플리케이션의 `bootstrap/app.php`에서 `withCommands` 메서드를 사용해 해당 디렉터리도 스캔하도록 할 수 있습니다.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면, `withCommands`에 명령어 클래스명을 직접 지정해 수동으로 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

아티즌 실행 시, 애플리케이션 내 모든 명령어가 [서비스 컨테이너](/docs/12.x/container)에서 resolve되어 아티즌에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 명령어의 코드 실행

CLI(명령줄) 밖에서 아티즌 명령어를 실행해야 할 경우도 있을 수 있습니다. 예를 들어 라우트나 컨트롤러에서 아티즌 명령어를 실행하고 싶을 때, `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인수로 명령어 시그니처 또는 클래스 이름, 두 번째 인수로 명령어 매개변수 배열을 받습니다. 반환값으로 종료 코드(exit code)가 전달됩니다.

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

또는 전체 아티즌 명령을 문자열로 전달할 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어에서 옵션으로 배열 입력을 정의했다면, 배열 형태로 값을 전달할 수 있습니다.

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

값을 받지 않는 옵션(예: `migrate:refresh` 명령어의 `--force` 플래그 등)에 대해서는, 옵션 값을 `true` 또는 `false`로 지정하세요.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### 아티즌 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면, 아티즌 명령어를 [큐 워커](/docs/12.x/queues)가 백그라운드에서 처리하도록 큐잉할 수도 있습니다. 이 기능을 사용하려면, 먼저 큐 설정을 마치고 큐 리스너가 실행 중이어야 합니다.

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

`onConnection` 및 `onQueue` 메서드를 사용해, 명령어 큐 처리 시 연결(connection)이나 큐 이름을 별도로 지정할 수도 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어 호출

기존 아티즌 명령어에서 또 다른 명령어를 호출하고 싶을 때, `call` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 이름과 인수/옵션 배열을 인수로 받습니다.

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

다른 콘솔 명령어를 호출하면서, 해당 명령어의 출력을 모두 숨기고 싶다면 `callSilently` 메서드를 사용할 수 있습니다. 사용법은 `call`과 동일합니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널(signal)을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 운영체제가 프로그램에 종료를 요청할 때 사용됩니다. 아티즌 콘솔 명령어에서 시그널을 감지하고, 시그널 발생 시 특정 코드를 실행하고 싶다면, `trap` 메서드를 사용할 수 있습니다.

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

한 번에 여러 개의 시그널을 감지하려면, 시그널 배열을 `trap` 메서드에 전달하세요.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이즈

아티즌 콘솔의 `make` 계열 명령어로는 컨트롤러, 잡(jobs), 마이그레이션, 테스트 등 다양한 클래스를 생성할 수 있습니다. 이 클래스들은 "스텁(stub)" 파일을 기반으로, 입력값에 맞춰 일부 내용을 채워서 생성됩니다. 만약 아티즌이 생성하는 파일에 조금씩 변화를 주고 싶다면, `stub:publish` 명령어로 자주 사용하는 스텁 파일들을 애플리케이션 내에 배포한 뒤, 필요에 따라 수정할 수 있습니다.

```shell
php artisan stub:publish
```

배포된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉터리에 위치하게 됩니다. 이 안의 스텁 파일을 수정하면, Artisan `make` 명령어로 생성하는 클래스에 해당 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

아티즌은 명령어 실행 시 아래 세 가지 이벤트를 디스패치(dispatch)합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
`ArtisanStarting` 이벤트는 Artisan이 실행될 때 즉시 발생합니다. 그 다음, 개별 명령어가 실행되기 직전에 `CommandStarting` 이벤트가 발생하며, 마지막으로 명령어 실행이 끝나면 `CommandFinished` 이벤트가 발생합니다.