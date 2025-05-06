# Artisan 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령 작성](#writing-commands)
    - [명령 생성](#generating-commands)
    - [명령 구조](#command-structure)
    - [클로저 명령](#closure-commands)
    - [Isolatable 명령](#isolatable-commands)
- [입력 기대 정의](#defining-input-expectations)
    - [인자(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 요청](#prompting-for-missing-input)
- [명령 입출력](#command-io)
    - [입력 값 가져오기](#retrieving-input)
    - [입력 요청](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령 등록](#registering-commands)
- [프로그램 방식의 명령 실행](#programmatically-executing-commands)
    - [다른 명령에서 명령 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁(stub) 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel과 함께 제공되는 명령줄 인터페이스(CLI)입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 유용한 다양한 명령을 제공합니다. 사용 가능한 모든 Artisan 명령 목록을 보려면 `list` 명령을 사용할 수 있습니다:

```shell
php artisan list
```

모든 명령은 "도움말(help)" 화면을 포함하며, 명령에서 사용할 수 있는 인자와 옵션을 보여주고 설명합니다. 도움말 화면을 보려면 명령 이름 앞에 `help`를 붙이세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)를 로컬 개발 환경으로 사용하는 경우, Artisan 명령을 실행할 때는 `sail` 명령줄을 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령을 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 그러나 이전에 애플리케이션에서 Tinker를 제거했다면, Composer를 사용하여 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]  
> Laravel 애플리케이션을 상호작용할 때 핫 리로딩, 멀티라인 코드 편집, 자동 완성을 원하시나요? [Tinkerwell](https://tinkerwell.app)도 확인해 보시기 바랍니다!

<a name="usage"></a>
#### 사용 방법

Tinker를 사용하면 Eloquent 모델, 잡(jobs), 이벤트 등 애플리케이션 전체와 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 진입하려면 다음 Artisan 명령을 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령을 이용해 Tinker의 설정 파일을 공개할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]  
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡이 큐에 올라가도록 가비지 컬렉션에 의존합니다. 따라서 tinker 내에서 잡을 디스패치할 때는 `Bus::dispatch` 또는 `Queue::push`를 사용하세요.

<a name="command-allow-list"></a>
#### 명령 허용 목록

Tinker는 허용(allow) 목록을 이용해 Tinker 셸 내에서 실행할 수 있는 Artisan 명령을 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령이 허용됩니다. 더 많은 명령을 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다:

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭하지 않을 클래스

보통 Tinker는 Tinker 내에서 클래스를 사용할 때 자동으로 별칭(alias)을 생성합니다. 그러나, 일부 클래스는 절대로 별칭을 생성하지 않도록 하고 싶을 수 있습니다. 이 경우 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가하세요:

    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>
## 명령 작성

Artisan에서 제공하는 기본 명령 외에도, 직접 커스텀 명령을 만들 수 있습니다. 명령 클래스는 보통 `app/Console/Commands` 디렉터리에 저장되지만, Composer에서 로드할 수 있다면 원하는 저장소 위치를 자유롭게 선택할 수 있습니다.

<a name="generating-commands"></a>
### 명령 생성

새 명령을 만들려면 `make:command` Artisan 명령을 사용할 수 있습니다. 이 명령은 `app/Console/Commands` 디렉터리에 새 명령 클래스를 생성합니다. 해당 디렉터리가 없다면, 처음 명령을 생성할 때 자동으로 만들어집니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령 구조

명령을 생성한 후에는 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 속성들은 `list` 화면에 명령을 표시할 때 사용됩니다. 또한, `signature` 속성은 [명령의 입력 기대값](#defining-input-expectations)을 정의할 수 있습니다. 명령이 실행될 때는 `handle` 메서드가 호출됩니다. 명령의 로직은 이 메서드에 작성하세요.

다음은 예시 명령입니다. `handle` 메서드에서 타입힌트를 통해 필요한 의존성을 주입받을 수 있으며, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 이를 자동으로 주입해줍니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * 콘솔 명령의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * 콘솔 명령 설명
     *
     * @var string
     */
    protected $description = '마케팅 이메일을 사용자에게 전송합니다';

    /**
     * 콘솔 명령 실행
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]  
> 코드의 재사용성을 높이기 위해, 콘솔 명령은 가능한 한 가볍게 유지하고, 실제 로직은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위의 예시는 이메일 발송의 "실제 처리"를 서비스 클래스에 위임하는 구조입니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무 것도 반환하지 않고 명령이 정상적으로 실행되면, 명령은 `0`의 종료 코드로 성공적으로 종료됩니다. 그러나 `handle` 메서드에서 정수형 값을 반환하여 종료 코드를 명시적으로 지정할 수도 있습니다:

```php
$this->error('문제가 발생했습니다.');

return 1;
```

명령 내 어느 메서드에서든 명령을 "실패" 상태로 종료하고 싶다면, `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령 실행을 중단하고 종료 코드를 `1`로 반환합니다:

```php
$this->fail('문제가 발생했습니다.');
```

<a name="closure-commands"></a>
### 클로저 명령

클래스로 명령을 정의하는 대신, 클로저 기반 명령을 사용할 수 있습니다. 라우트 클로저가 컨트롤러의 대안이 되듯, 클로저 명령 또한 클래스 명령의 대안이 됩니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 콘솔용 진입점(라우트)을 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용해 모든 클로저 기반 명령을 정의할 수 있습니다. 이 메서드는 두 개의 인자를 받습니다: [명령 시그니처](#defining-input-expectations)와 명령의 인자 및 옵션을 받는 클로저입니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 실제 명령 인스턴스에 바인딩되므로, 클래스 명령에서 사용할 수 있는 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

명령의 인자와 옵션 외에도, 클로저 명령은 [서비스 컨테이너](/docs/{{version}}/container)에서 해석할 추가 의존성을 타입힌트로 받을 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령 설명

클로저 기반 명령을 정의할 때 `purpose` 메서드를 사용해 명령의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령 실행 시 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('마케팅 이메일을 사용자에게 전송합니다');
```

<a name="isolatable-commands"></a>
### Isolatable 명령

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

가끔 동시에 한 인스턴스만 실행되도록 명령을 제한하고 싶을 때가 있습니다. 이럴 경우 명령 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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

명령이 `Isolatable`로 표시되면, Laravel은 명령에 `--isolated` 옵션을 자동으로 추가합니다. 이 옵션과 함께 명령을 실행하면 Laravel이 해당 명령의 다른 인스턴스가 이미 실행 중인지 확인합니다. 내부적으로 애플리케이션의 기본 캐시 드라이버를 이용해 원자적 락을 시도합니다. 다른 인스턴스가 실행 중이면 명령은 실행되지 않지만, 종료 상태 코드는 성공으로 반환됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령이 실행되지 못할 때 반환할 종료 상태 코드를 지정하고 싶다면 `isolated` 옵션에 값을 전달하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령의 이름을 사용해 캐시에서 락을 잡을 때 사용할 문자열 키를 생성합니다. 그러나 `isolatableId` 메서드를 명령 클래스에 정의해 인자나 옵션을 포함한 사용자 지정 키를 사용할 수 있습니다:

```php
/**
 * 명령의 Isolatable ID 반환
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### 락 만료 시간

기본적으로 isolation 락은 명령이 완료되면 만료되며, 명령이 중단되어 완료되지 못할 경우 1시간 후에 만료됩니다. 락 만료 시간을 조정하려면 명령에 `isolationLockExpiresAt` 메서드를 정의하세요:

```php
use DateTimeInterface;
use DateInterval;

/**
 * 명령의 isolation 락 만료 시점 결정
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대 정의

콘솔 명령을 작성할 때는 사용자의 입력을 인자(argument)나 옵션(option)으로 받아오는 일이 흔합니다. Laravel에서는 명령의 `signature` 속성을 이용해 입력을 쉽게 정의할 수 있습니다. 이 속성을 통해 명령의 이름, 인자, 옵션을 한 번에 명확하고 직관적으로 정의할 수 있습니다.

<a name="arguments"></a>
### 인자(Arguments)

사용자가 제공하는 모든 인자와 옵션은 중괄호로 감쌉니다. 다음 예시에서 명령은 필수 인자 `user`를 정의합니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인자를 선택적으로 만들거나 기본값을 정의할 수도 있습니다:

```php
// 선택적 인자
'mail:send {user?}'

// 기본값이 있는 선택적 인자
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션도 인자처럼 사용자 입력의 한 형식입니다. 옵션을 커맨드라인에서 제공할 땐 두 개의 하이픈(`--`)으로 시작합니다. 옵션은 값을 받는 것과 받지 않는 것으로 나뉩니다. 값 없는 옵션은 불리언 "스위치" 역할을 합니다.

```php
/**
 * 콘솔 명령의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위에서, `--queue` 스위치를 전달하면 옵션 값은 `true`가 되며, 전달하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 필요로 하는 옵션을 정의하려면 옵션 이름 뒤에 `=`를 붙입니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

옵션이 지정되지 않으면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면, 옵션 이름 뒤에 곧바로 기본값을 붙입니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션을 정의할 때 단축키(축약어)를 할당하려면 옵션 이름 앞에 단축키를 두고, `|` 문자로 전체 옵션명과 구분합니다:

```php
'mail:send {user} {--Q|queue}'
```

단축키를 사용할 때는 한 개의 하이픈(`-`)을 붙이며, 값이 있을 때는 `=` 문자를 사용하지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 개의 입력 값을 받는 인자나 옵션을 정의하려면 `*` 문자를 사용합니다. 다음과 같이 인자를 정의할 수 있습니다:

```php
'mail:send {user*}'
```

명령 호출 시 여러 `user` 인자를 순서대로 전달할 수 있습니다:

```shell
php artisan mail:send 1 2
```

`*` 문자는 선택적 인자와 함께 사용할 수도 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 입력 값을 받는 옵션을 정의할 때는 옵션 이름에 `=*`를 붙입니다:

```php
'mail:send {--id=*}'
```

이 경우, 여러 옵션 값을 각각 `--id`로 전달할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인자와 옵션에 설명을 추가하려면 이름 뒤에 콜론을 붙이고 설명을 입력합니다. 명령 정의가 길어진다면 여러 줄로 나누어도 됩니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : 사용자의 ID}
                        {--queue : 작업을 큐에 넣을지 여부}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력 요청

필수 인자가 빠졌을 경우, 사용자에게 오류 메시지가 표시됩니다. 또는, 명령에서 `PromptsForMissingInput` 인터페이스를 구현해 누락된 인자가 있을 때 자동으로 입력을 요청하도록 할 수도 있습니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * 콘솔 명령의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Laravel은 누락된 필수 인자를 사용자에게 지능적으로 질문하여 입력을 요청합니다. 질문을 커스터마이징하려면, `promptForMissingArgumentsUsing` 메서드를 구현해 질문을 인자 이름을 key로 하는 배열로 반환하세요:

```php
/**
 * 누락된 인자에 대해 커스텀 질문을 반환
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => '어느 사용자 ID로 메일을 보낼까요?',
    ];
}
```

질문과 플레이스홀더를 튜플로 제공할 수도 있습니다:

```php
return [
    'user' => ['어느 사용자 ID로 메일을 보낼까요?', '예: 123'],
];
```

질문 제어를 위해 클로저를 제공할 수도 있습니다:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: '사용자를 검색하세요:',
        placeholder: '예: Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]  
> 더 다양한 프롬프트와 사용법은 [Laravel Prompts](/docs/{{version}}/prompts) 문서를 참조하세요.

옵션([options](#options))을 입력 받으려면 명령의 `handle` 메서드 안에서 프롬프트를 추가할 수 있습니다. 그러나 누락된 인자를 자동으로 프롬프트한 직후에만 프롬프트를 띄우고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하세요:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * 누락된 인자를 프롬프트한 직후 추가 작업
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: '메일을 큐에 넣을까요?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
## 명령 입출력

<a name="retrieving-input"></a>
### 입력 값 가져오기

명령이 실행되는 동안, 명령이 받는 인자 및 옵션 값에 접근해야 할 수 있습니다. 이를 위해 `argument`, `option` 메서드를 사용할 수 있습니다. 값이 없으면 `null`이 반환됩니다:

```php
/**
 * 콘솔 명령 실행
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인자를 배열로 받으려면 `arguments` 메서드를 사용하세요:

```php
$arguments = $this->arguments();
```

옵션 역시 `option` 메서드로 얻거나, `options` 메서드로 모두 배열로 얻을 수 있습니다:

```php
// 특정 옵션 값만
$queueName = $this->option('queue');

// 모든 옵션 값 배열로
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 요청

> [!NOTE]  
> [Laravel Prompts](/docs/{{version}}/prompts)는 플레이스홀더, 검증 등 브라우저와 유사한 기능을 가진 아름답고 사용자 친화적인 CLI 폼을 구현할 수 있는 PHP 패키지입니다.

출력만이 아니라, 명령 실행 중 사용자에게 입력 요청도 할 수 있습니다. `ask` 메서드는 질문을 프롬프트하고, 사용자 입력을 받아서 반환합니다:

```php
/**
 * 콘솔 명령 실행
 */
public function handle(): void
{
    $name = $this->ask('당신의 이름은 무엇인가요?');

    // ...
}
```

`ask` 메서드는 두 번째 인자로 기본 값도 지정할 수 있습니다:

```php
$name = $this->ask('당신의 이름은 무엇인가요?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 입력된 내용이 콘솔에 표시되지 않습니다. 비밀번호 등 민감한 정보를 받기에 유용합니다:

```php
$password = $this->secret('비밀번호를 입력하세요?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청

단순한 '예/아니오' 질문을 하고 싶다면 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 이 메서드는 `false`를 반환하지만 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다:

```php
if ($this->confirm('계속하시겠습니까?')) {
    // ...
}
```

기본값을 예(`true`)로 하고 싶다면 두 번째 인자에 `true`를 전달하세요:

```php
if ($this->confirm('계속하시겠습니까?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 가능한 선택지 자동완성을 제공합니다. 자동완성 힌트가 있어도, 사용자는 원하는 입력을 할 수 있습니다:

```php
$name = $this->anticipate('당신의 이름은?', ['Taylor', 'Dayle']);
```

자동완성 옵션을 동적으로 제공하고 싶다면 클로저를 두 번째 인자로 전달할 수 있습니다:

```php
$name = $this->anticipate('당신의 주소는?', function (string $input) {
    // 자동완성 옵션 반환
});
```

<a name="multiple-choice-questions"></a>
#### 다지선다 질문

미리 지정한 선택지 중에서 질문하고 싶다면 `choice` 메서드를 사용합니다. 세 번째 인자로 기본값의 배열 인덱스값을 전달할 수 있습니다:

```php
$name = $this->choice(
    '당신의 이름은?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째, 다섯 번째 인자로 유효한 답변 선택 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

```php
$name = $this->choice(
    '당신의 이름은?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### 출력 작성

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각각의 메서드는 목적에 맞는 ANSI 컬러로 출력합니다. 예를 들어, `info` 메서드는 보통 초록색 텍스트로 출력됩니다:

```php
/**
 * 콘솔 명령 실행
 */
public function handle(): void
{
    // ...

    $this->info('명령이 성공적으로 실행되었습니다!');
}
```

오류 메시지는 `error` 메서드로 빨간색으로 출력할 수 있습니다:

```php
$this->error('문제가 발생했습니다!');
```

단순한 무색 텍스트는 `line` 메서드를 사용하세요:

```php
$this->line('이 내용을 화면에 표시');
```

빈 줄은 `newLine` 메서드로 출력할 수 있습니다:

```php
// 한 줄 빈 줄 추가
$this->newLine();

// 세 줄 빈 줄 추가
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행/열의 데이터를 테이블 형식으로 쉽게 출력할 수 있도록 해줍니다. 열 이름과 데이터를 넘기면, Laravel이 적절한 폭과 높이로 테이블을 그려줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

시간이 오래 걸리는 작업이라면, 진행 바(progress bar)를 이용해 작업의 진행 상황을 사용자에게 보여줄 수 있습니다. `withProgressBar` 메서드는 반복 처리 중 각 항목에 대해 진행 바를 자동으로 갱신합니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 세밀한 진행 바 조작이 필요하다면, 전체 단계 수를 지정하고 각 항목 처리 후 수동으로 advance를 호출하세요:

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
> 더 발전된 기능은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/7.0/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령 등록

기본적으로, Laravel은 `app/Console/Commands` 디렉터리 내의 모든 명령을 자동으로 등록합니다. 추가 디렉터리를 Artisan 명령 탐색 경로에 포함하려면, 애플리케이션의 `bootstrap/app.php`에서 `withCommands` 메서드를 사용하세요:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면 명령 클래스명을 직접 `withCommands`에 전달해 수동 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션 내 모든 명령은 [서비스 컨테이너](/docs/{{version}}/container)로부터 해석되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램 방식의 명령 실행

CLI(명령줄)이 아닌 코드에서 Artisan 명령을 실행하고 싶을 수도 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령을 호출할 수 있습니다. 이를 위해 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. 첫 번째 인자로 명령의 시그니처 혹은 클래스명, 두 번째 인자로 명령 파라미터 배열을 넘깁니다. 반환값은 종료 코드입니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

명령 전체를 문자열로 넘길 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

옵션이 배열을 받도록 정의되어 있다면, 값 배열을 전달하면 됩니다:

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

문자형 값을 받지 않는 옵션(예: `migrate:refresh` 명령의 `--force` 플래그)을 지정해야 할 때는 `true` 또는 `false`를 값으로 전달해야 합니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령을 큐잉하기

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령을 [큐 워커](/docs/{{version}}/queues)가 백그라운드에서 처리하도록 큐에 넣을 수 있습니다. 이를 사용하기 전에 큐를 설정하고 큐 리스너가 실행 중인지 확인하세요:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`, `onQueue` 메서드로 명령을 보낼 연결(connection)과 큐(queue)를 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령에서 명령 호출

애플리케이션의 한 Artisan 명령 안에서 다른 명령을 호출하고자 할 때 `call` 메서드를 사용할 수 있습니다. 첫 번째 인자는 명령명, 두 번째 인자는 인자/옵션입니다:

```php
/**
 * 콘솔 명령 실행
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

다른 명령을 호출하고 출력은 모두 감추고 싶다면 `callSilently` 메서드를 이용합니다. 시그니처는 `call`과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 프로그램 종료 요청입니다. Artisan 콘솔 명령에서 시그널을 감지해 처리하고 싶을 때는 `trap` 메서드를 사용할 수 있습니다:

```php
/**
 * 콘솔 명령 실행
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 시그널을 한 번에 감지하려면 배열로 전달하면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이징

Artisan 콘솔의 `make` 명령은 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 "stub" 파일을 기반으로 생성되며, 입력 값에 따라 채워집니다. 만약 Artisan이 생성하는 파일을 약간 수정하고 싶다면, `stub:publish` 명령으로 자주 사용되는 stub들을 애플리케이션으로 퍼블리시할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 stub들은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 stub 파일들을 수정하면, Artisan의 `make` 명령으로 생성되는 클래스에 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 실행될 때 즉시 발생합니다. 다음으로, `CommandStarting` 이벤트는 명령이 실행되기 직전에 발생하며, 마지막으로 `CommandFinished` 이벤트는 명령 실행이 끝났을 때 발생합니다.