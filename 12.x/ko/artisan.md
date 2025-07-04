# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 기반 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대값 정의하기](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력값 프롬프트 하기](#prompting-for-missing-input)
- [명령어 I/O](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트 하기](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [명령어를 프로그래밍적으로 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

아티즌은 라라벨에 기본으로 포함되어 있는 커맨드 라인 인터페이스입니다. 아티즌은 애플리케이션 루트 디렉터리에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움이 되는 여러 유용한 명령어를 제공합니다. 사용 가능한 모든 아티즌 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

각 명령어에는 "도움말(help)" 화면이 포함되어 있어 해당 명령어에서 사용 가능한 인수와 옵션에 대한 설명과 정보를 확인할 수 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/12.x/sail)을 사용 중이라면, 아티즌 명령어를 실행할 때 `sail` 커맨드 라인을 사용해야 합니다. Sail은 여러분의 애플리케이션이 동작하는 Docker 컨테이너 안에서 아티즌 명령어를 실행합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 라라벨 프레임워크용 강력한 REPL(Read–Eval–Print Loop) 도구로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작합니다.

<a name="installation"></a>
#### 설치

모든 라라벨 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 Tinker를 애플리케이션에서 제거했다면, Composer를 이용해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> 라라벨 애플리케이션과 상호작용할 때 핫 리로딩, 여러 줄 코드 편집, 자동 완성 등의 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 참고하세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 커맨드 라인에서 전체 라라벨 애플리케이션과 직접 상호작용할 수 있습니다. Eloquent 모델, 작업(Job), 이벤트 등도 모두 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` 아티즌 명령어를 실행하세요.

```shell
php artisan tinker
```

`vendor:publish` 명령어를 사용해 Tinker의 설정 파일을 배포(publish)할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업(Job)을 큐에 등록할 때 가비지 컬렉션에 의존합니다. 따라서 tinker에서 작업을 큐잉할 때는 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 권장됩니다.

<a name="command-allow-list"></a>
#### 명령어 허용 리스트

Tinker는 셸 환경 안에서 실행을 허용할 아티즌 명령어를 "허용 리스트(allow list)"로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어가 허용되어 있습니다. 더 많은 명령어를 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭에서 제외할 클래스

보통 Tinker는 셸에서 상호작용할 때 클래스명을 자동으로 별칭(aliased) 처리합니다. 하지만, 특정 클래스는 별칭을 생성하지 않도록 하고 싶을 수 있습니다. 이 경우에는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하세요.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

아티즌이 기본 제공하는 명령어 외에도, 직접 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉터리에 저장하지만, [다른 디렉터리도 등록 가능](#registering-commands)하므로 자유롭게 위치를 정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새로운 명령어를 생성하려면 `make:command` 아티즌 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 새로운 명령어 클래스를 생성합니다. 만약 이 디렉터리가 애플리케이션에 없다면, 처음 `make:command` 명령어를 실행할 때 자동으로 만들어집니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성을 적절하게 지정해주어야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. `signature` 속성에서는 [명령어의 입력값 기대치](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 여기에 명령어의 실제 동작 로직을 작성하면 됩니다.

예시 명령어 코드를 살펴보면, 필요한 의존성을 `handle` 메서드의 타입힌트로 직접 주입받을 수 있습니다. 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 이 의존성들을 자동 주입합니다.

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
> 코드의 재사용성을 높이기 위해 콘솔 명령어 자체의 로직은 가볍게 유지하고, 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예시처럼 이메일 전송과 같은 "무거운 작업"은 별도의 서비스 클래스를 주입해서 처리하는 것이 권장됩니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무런 값을 반환하지 않고 명령어가 정상적으로 실행되면, 명령어는 `0` 종료 코드로 종료되어 성공을 의미합니다. 그러나 필요하다면 `handle` 메서드에서 정수를 반환하여 명령어의 종료 코드를 직접 지정할 수도 있습니다.

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내에서 언제든지 명령어를 "실패" 상태로 종료하고 싶을 경우, `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어 실행을 종료하며, 종료 코드는 항상 `1`이 반환됩니다.

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 기반 명령어

클로저 기반 명령어(Closure Commands)는 명령어를 클래스로 정의하는 대신 클로저(익명 함수)로 정의하는 방법을 제공합니다. 라우트에서 컨트롤러 대신 클로저를 사용할 수 있듯이, 명령어도 클래스 대신 클로저로 작성할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트는 아니지만, 애플리케이션으로 진입하는 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 정의할 수 있습니다. 이 메서드는 두 가지 인자를 받는데, 하나는 [명령어 signature](#defining-input-expectations)이고, 다른 하나는 명령어의 인수와 옵션을 받을 클로저입니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저 내부는 여러분이 작성하는 명령어 클래스의 인스턴스에 바인딩되어, 평소 클래스에서 사용할 수 있는 모든 헬퍼 메서드에 자유롭게 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트(Type-Hinting Dependencies)

명령어의 인수와 옵션 외에도, 클로저의 파라미터 타입으로 [서비스 컨테이너](/docs/12.x/container)에서 해결(주입)하고 싶은 의존성을 지정할 수 있습니다.

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명(Descriptions)

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용해 해당 명령어의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어를 실행할 때 표시됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신할 수 있어야 합니다.

때때로 한 번에 하나의 명령어 인스턴스만 실행되도록 하고 싶을 때가 있습니다. 이를 위해 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

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

명령어에 `Isolatable`을 적용하면, 해당 명령어는 옵션에 `--isolated`가 자동으로 활성화됩니다(명시적으로 옵션으로 선언할 필요 없음). 이 옵션을 붙여 명령어를 실행하면, 현재 동일한 명령어가 이미 실행 중인 상태인지 라라벨이 확인합니다. 확인 방식은 기본 캐시 드라이버를 사용해 원자적 락(atomic lock)을 획득하려 시도합니다. 만약 이미 다른 인스턴스가 실행 중이라면 명령어는 실행되지 않고, 성공적인 종료 코드로 바로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행에 실패했을 때 명령어가 반환해야 할 종료 상태 코드를 직접 지정하고 싶다면, `--isolated` 옵션에 원하는 코드를 지정할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### Lock ID

기본적으로 라라벨은 명령어의 이름을 이용해 캐시에서 원자적 락을 위한 문자열 키를 생성합니다. 만약 이 키를 직접 다르게 정하고 싶다면, Artisan 명령어 클래스에 `isolatableId` 메서드를 정의해 해당 키에 명령어의 인수나 옵션 값을 포함시킬 수 있습니다.

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

격리 락(isolation lock)은 명령어가 정상적으로 종료되면 즉시 만료됩니다. 명령어가 강제 종료되어 완료되지 않을 경우, 락은 1시간 이후 자동 만료됩니다. 만약 락의 만료 시간을 직접 조정하고 싶다면 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의하세요.

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

콘솔 명령어를 작성할 때에는 사용자에게 인수나 옵션 형태로 입력값을 받는 일이 많습니다. 라라벨에서는 명령어 클래스의 `signature` 속성을 활용해, 사용자가 어떤 입력을 제공하길 원하는지 매우 쉽게 정의할 수 있습니다. `signature` 속성에서는 명령어 이름, 인수, 옵션을 한 번에 직관적이고 명확하게 작성할 수 있습니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자가 전달하는 모든 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서는 단일 필수 인수 `user`가 정의되어 있습니다.

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
// 선택적(optional) 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션도 인수와 마찬가지로 사용자 입력의 한 형태입니다. 옵션을 지정할 때는 커맨드 라인에서 두 개의 하이픈(`--`)을 앞에 붙입니다. 옵션은 두 가지 유형이 있습니다. 값(value)을 받는 옵션과 값을 받지 않는 옵션입니다.
값을 받지 않는 옵션은 불리언 "스위치"로 사용됩니다. 다음은 이런 옵션의 예시입니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서 `--queue` 스위치를 명령어 실행 시 지정할 수 있습니다.
`--queue` 옵션이 전달되면 옵션의 값이 `true`가 되고, 전달되지 않으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

이번에는 값(value)을 지정해야 하는 옵션에 대해서 살펴보겠습니다. 사용자가 반드시 값을 지정해야 하는 옵션은 옵션 이름 뒤에 `=` 기호를 붙여 작성합니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이렇게 하면 사용자는 옵션 값을 다음과 같이 전달할 수 있습니다. 만약 옵션을 명시하지 않고 명령어를 실행하면, 해당 옵션의 값은 `null`이 됩니다.

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하고 싶다면, 옵션명 뒤에 기본값을 바로 작성하면 됩니다. 사용자가 옵션 값을 전달하지 않았다면, 이 기본값이 사용됩니다.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키(Shortcut)

옵션 작성 시, 단축키(Shortcut)를 추가하고 싶으면 `|`(파이프) 기호를 사용해 단축키와 전체 옵션 이름을 구분해 앞쪽에 단축키를 명시합니다.

```php
'mail:send {user} {--Q|queue}'
```

명령어를 터미널에서 실행할 때 옵션 단축키는 한 개의 하이픈만 붙이고, 값을 지정할 때는 `=` 기호를 사용하지 않습니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열(Input Arrays)

인수나 옵션에 여러 개의 입력값을 받고 싶다면, `*` 기호를 사용하면 됩니다. 먼저 인수에 적용한 예시를 봅시다.

```php
'mail:send {user*}'
```

이 명령어를 실행할 때 커맨드 라인에서 여러 개의 `user` 인수를 차례대로 전달할 수 있습니다.
예를 들어 다음 명령어를 실행하면 `user` 인수에는 값이 `1`과 `2`인 배열이 전달됩니다.

```shell
php artisan mail:send 1 2
```

`*` 기호는 선택적 인수와 조합하여 0개 이상의 인수를 허용할 수도 있습니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 개의 입력값을 받는 옵션을 정의할 때는, 각각의 옵션 값 앞에 옵션 이름을 붙여서 커맨드 라인에 전달하면 됩니다.

```php
'mail:send {--id=*}'
```

이런 명령어는 여러 개의 `--id` 옵션을 각각 전달해 실행할 수 있습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력값 설명

입력 인수 및 옵션에 설명을 추가하고 싶다면, 이름과 설명 사이를 콜론으로 구분하면 됩니다. 명령어가 복잡하다면 여러 줄로 나누어 작성해도 괜찮습니다.

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
### 누락된 입력값 프롬프트 하기

명령어에 필수 인수(required arguments)가 있을 때, 사용자가 이를 입력하지 않으면 에러 메시지가 출력됩니다. 또는, 필수 입력값이 누락된 경우 자동으로 질문을 띄워 입력값을 받을 수 있도록 명령어를 구성할 수도 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하세요.

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

라라벨은 필수 인수를 직접 입력받아야 할 때 해당 인수 이름이나 설명을 활용해 사용자에게 자동으로 질문을 만들어 프롬프트를 보여줍니다. 만약 질문 문구를 직접 커스터마이즈하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현해 인수 이름을 키로 갖는 질문 배열을 반환하세요.

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

질문과 함께 플레이스홀더(placeholder) 텍스트도 함께 제공하려면, 질문과 플레이스홀더를 튜플로 전달할 수 있습니다.

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트에 대한 완전한 제어가 필요하다면, 사용자의 입력을 직접 받아서 반환하는 클로저를 제공할 수 있습니다.

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
라라벨의 [Prompts](/docs/12.x/prompts) 공식 문서에서 프롬프트 사용법과 모든 세부정보를 확인할 수 있습니다.

만약 [옵션](#options)에 대해 사용자에게 입력을 받게 하고 싶다면, 명령어의 `handle` 메서드 내에서 프롬프트를 포함할 수 있습니다. 단, 누락된 인수에 대해 자동 프롬프트가 동작한 경우에만 추가로 옵션 입력을 받고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하세요.

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

명령어가 실행되는 동안, 사용자가 입력한 인수와 옵션의 값을 코드 상에서 접근해야 할 경우가 많습니다. 이를 위해 `argument`와 `option` 메서드를 사용할 수 있습니다. 해당 인수 또는 옵션이 없으면 `null`이 반환됩니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 `array` 형태로 가져오고 싶다면, `arguments` 메서드를 사용하세요.

```php
$arguments = $this->arguments();
```

옵션도 인수처럼 `option` 메서드로 쉽게 조회할 수 있습니다. 모든 옵션을 배열로 가져오려면 `options` 메서드를 이용하세요.

```php
// 특정 옵션만 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>

### 입력 값 받기

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가하기 위한 PHP 패키지입니다. 플레이스홀더 텍스트와 유효성 검증 등 브라우저와 유사한 기능을 제공합니다.

출력만 표시하는 것 외에도, 명령어 실행 도중 사용자로부터 입력을 받을 수도 있습니다. `ask` 메서드는 지정한 질문을 사용자에게 표시하고, 사용자가 입력한 값을 받아 다시 명령어로 반환합니다.

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

`ask` 메서드는 선택적으로 두 번째 인수를 받을 수 있습니다. 두 번째 인수는 사용자가 아무런 값을 입력하지 않았을 때 반환할 기본값을 지정합니다.

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 사용자가 콘솔에 값을 입력할 때 입력한 내용이 보이지 않습니다. 이 메서드는 비밀번호와 같은 민감한 정보를 요청할 때 유용합니다.

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청하기

사용자에게 간단한 "예 또는 아니오" 형태의 확인을 요청하려면 `confirm` 메서드를 사용할 수 있습니다. 이 메서드는 기본적으로 `false`를 반환합니다. 하지만, 사용자가 프롬프트에 `y` 또는 `yes`라고 입력하면 해당 메서드는 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

필요하다면, `confirm` 메서드의 두 번째 인수에 `true`를 전달하여 확인 프롬프트의 기본값을 `true`로 지정할 수 있습니다.

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드를 사용하면 사용자 입력에 대해 자동 완성 기능을 제공할 수 있습니다. 자동 완성 기능은 힌트를 줄 뿐이며, 사용자는 힌트와 무관하게 원하는 값도 입력할 수 있습니다.

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또한, 두 번째 인수로 클로저(익명 함수)를 전달할 수도 있습니다. 이 클로저는 사용자가 입력할 때마다 호출되며, 현재까지 사용자가 입력한 문자열을 인수로 받고, 자동 완성할 옵션의 배열을 반환해야 합니다.

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

사용자에게 미리 정의된 여러 선택지 중 하나를 선택하게 하려면 `choice` 메서드를 사용할 수 있습니다. 이때, 세 번째 인수로 기본값으로 사용할 배열의 인덱스를 지정할 수 있습니다. 사용자가 아무 옵션도 선택하지 않은 경우 해당 인덱스의 값이 반환됩니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

더불어, `choice` 메서드는 네 번째, 다섯 번째 선택적 인수를 추가로 받을 수 있습니다. 네 번째 인수는 유효한 응답을 선택할 수 있는 최대 시도 횟수, 다섯 번째 인수는 여러 개의 선택이 가능한지 여부를 지정합니다.

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
### 출력하기

콘솔에 출력을 보내기 위해 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 이들 각 메서드는 용도에 따라 적절한 ANSI 컬러를 사용해 메시지를 출력합니다. 예를 들어, 사용자에게 일반적인 정보를 표시하고 싶을 때는 `info` 메서드를 사용하면 콘솔에 초록색 텍스트로 표시됩니다.

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

에러 메시지를 표시하려면 `error` 메서드를 사용합니다. 에러 메시지는 일반적으로 빨간색으로 표시됩니다.

```php
$this->error('Something went wrong!');
```

평범한, 색상이 없는 텍스트를 출력하려면 `line` 메서드를 사용할 수 있습니다.

```php
$this->line('Display this on the screen');
```

빈 줄을 출력해야 할 때는 `newLine` 메서드를 사용할 수 있습니다.

```php
// 한 줄의 빈 줄 출력
$this->newLine();

// 세 줄의 빈 줄 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드를 사용하면 여러 행/열의 데이터를 보기 좋게 포맷팅할 수 있습니다. 컬럼명과 테이블에 표시할 데이터를 전달하면, 라라벨이 자동으로 알맞은 너비와 높이로 테이블을 만들어 출력합니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄

실행 시간이 오래 걸리는 작업에는 진행률 표시줄을 보여주는 것이 사용자의 이해를 돕는 데 유용합니다. `withProgressBar` 메서드를 사용하면 라라벨이 지정한 반복 가능한 값(iterable)을 한 번 순회할 때마다 진행 표시줄의 상태를 자동으로 갱신해가며 보여줍니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

가끔은 진행 표시줄의 업데이트를 좀 더 세밀하게 제어해야 할 수도 있습니다. 먼저 프로세스가 반복할 총 스텝 수를 정의한 뒤, 각 항목을 처리할 때마다 직접 진행률을 갱신할 수 있습니다.

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
> 더 다양한 옵션이 궁금하다면, [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)을 참고해보세요.

<a name="registering-commands"></a>
## 명령어 등록하기

라라벨은 기본적으로 `app/Console/Commands` 디렉터리 아래에 있는 모든 명령어를 자동으로 등록합니다. 하지만, 필요한 경우 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용하여 다른 디렉터리도 Artisan 명령어로 스캔하도록 지정할 수 있습니다.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면, 명령어의 클래스명을 직접 `withCommands` 메서드에 전달해 수동으로 명령어를 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 실행될 때, 애플리케이션 내의 모든 명령어는 [서비스 컨테이너](/docs/12.x/container)를 통해 해결(resolved)되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 명령어를 코드로 실행하기

때로는 CLI가 아닌 곳에서 Artisan 명령어를 실행해야 할 때가 있습니다. 예를 들어, 라우트 또는 컨트롤러 안에서 Artisan 명령어를 실행할 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. `call` 메서드는 첫 번째 인수로 명령어의 시그니처 이름 또는 클래스명을, 두 번째 인수로 명령어 파라미터의 배열을 받습니다. 반환 값은 종료 코드(Exit Code)입니다.

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

또한, entire Artisan 명령어를 문자열로 전달하여 `call` 메서드를 사용할 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

명령어가 배열을 받는 옵션을 정의한 경우, 해당 옵션에 값을 배열로 넣어줄 수 있습니다.

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

문자열이 아닌 값을 받아야 하는 옵션, 예를 들어 `migrate:refresh` 명령의 `--force` 플래그 등에는 해당 옵션의 값으로 `true` 또는 `false`를 전달해야 합니다.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉하기

`Artisan` 파사드의 `queue` 메서드를 사용하면, Artisan 명령어를 큐에 등록해 [큐 워커](/docs/12.x/queues)가 백그라운드에서 처리할 수 있습니다. 이 기능을 사용하기 전에 큐 설정을 먼저 마치고, 큐 리스너가 동작하고 있어야 합니다.

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

`onConnection` 및 `onQueue` 메서드를 이용해 Artisan 명령어를 특정 커넥션 또는 큐에 할당할 수도 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 안에서 또 다른 명령어 호출하기

때로는 기존 Artisan 명령어 내부에서 다른 명령어를 호출하고 싶을 수 있습니다. 이때는 `call` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 이름과 명령어 인수/옵션의 배열을 인수로 받습니다.

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

다른 콘솔 명령어를 호출하되 그 명령어의 모든 출력을 숨기고 싶다면 `callSilently` 메서드를 사용하세요. 이 메서드도 `call` 메서드와 같은 시그니처를 가집니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널(signal) 핸들링

운영체제(OS)는 실행 중인 프로세스에 시그널(신호)을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 운영체제가 프로그램에게 종료를 요청하는 방식입니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하여 특정 코드를 실행하고 싶다면, `trap` 메서드를 사용할 수 있습니다.

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

여러 개의 시그널을 동시에 감지하고 싶을 때는, `trap` 메서드에 시그널 배열을 전달하면 됩니다.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이징

Artisan 콘솔의 `make` 명령어들은 컨트롤러, 작업, 마이그레이션, 테스트 등 여러 종류의 클래스를 생성할 때 사용됩니다. 이들은 여러분이 입력한 값들로 채워지는 "스텁(stub)" 파일을 활용해 생성됩니다. 하지만 Artisan이 만들어주는 기본 파일에 약간의 수정을 가하고 싶을 수도 있습니다. 이를 위해, `stub:publish` 명령어로 가장 일반적으로 쓰이는 스텁 파일을 애플리케이션에 퍼블리시(복사)할 수 있고, 이후 마음껏 커스터마이즈할 수 있습니다.

```shell
php artisan stub:publish
```

퍼블리시된 스텁 파일은 애플리케이션 루트 디렉터리의 `stubs` 폴더 안에 위치하게 됩니다. 이 스텁 파일을 수정하면, 나중에 Artisan `make` 명령어로 해당 클래스를 생성할 때 바로 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 세 종류의 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
`ArtisanStarting` 이벤트는 Artisan이 최초로 실행될 때 디스패치됩니다. 그 다음, 명령어가 실행되기 직전에 `CommandStarting` 이벤트가 발생합니다. 명령어 실행이 끝나면 마지막으로 `CommandFinished` 이벤트가 발생합니다.