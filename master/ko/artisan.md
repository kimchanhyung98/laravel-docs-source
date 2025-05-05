# 아티즌 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [커맨드 작성](#writing-commands)
    - [커맨드 생성](#generating-commands)
    - [커맨드 구조](#command-structure)
    - [클로저 커맨드](#closure-commands)
    - [Isolatable 커맨드](#isolatable-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인자](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [커맨드 I/O](#command-io)
    - [입력 값 가져오기](#retrieving-input)
    - [입력값 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [커맨드 등록](#registering-commands)
- [프로그래밍 방식으로 커맨드 실행](#programmatically-executing-commands)
    - [다른 커맨드에서 커맨드 호출하기](#calling-commands-from-other-commands)
- [시그널 핸들링](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션 개발 시 유용한 여러 명령어를 제공합니다. 사용할 수 있는 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

모든 명령어는 "help" 화면을 제공하며, 해당 명령어에서 사용할 수 있는 인자와 옵션을 표시·설명합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙이세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)를 로컬 개발 환경으로 사용하는 경우, Artisan 명령어를 실행하려면 `sail` 명령줄 명령어를 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동되는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 그러나 애플리케이션에서 Tinker를 제거했다면, Composer를 통해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 멀티라인 코드 편집, 자동완성을 원하신다면 [Tinkerwell](https://tinkerwell.app)을 참고하세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 Eloquent 모델, 작업, 이벤트 등을 포함하여 전체 Laravel 애플리케이션과 명령줄에서 상호 작용할 수 있습니다. Tinker 환경에 진입하려면, `tinker` Artisan 명령어를 실행하세요.

```shell
php artisan tinker
```

`vendor:publish` 명령어로 Tinker의 설정 파일을 게시할 수도 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker에서 작업을 디스패치할 때는 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록

Tinker는 셸 내에서 실행할 수 있도록 허용된 Artisan 명령어의 "허용 목록(allow list)"을 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어만 허용됩니다. 더 많은 명령어를 허용하려면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 만들지 않을 클래스

일반적으로 Tinker는 Tinker에서 상호작용할 때 클래스를 자동으로 별칭(alias) 처리합니다. 하지만 특정 클래스는 절대 별칭이 생성되지 않도록 하고 싶은 경우, `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가할 수 있습니다.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 커맨드 작성

Artisan이 제공하는 명령어 외에도, 자신만의 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 일반적으로 `app/Console/Commands` 디렉토리에 저장되지만, Composer로 로드할 수 있다면 다른 위치에 저장해도 무방합니다.

<a name="generating-commands"></a>
### 커맨드 생성

새 명령어를 생성하려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어를 실행하면 `app/Console/Commands` 디렉토리에 새 명령어 클래스가 생성됩니다. 만약 해당 디렉토리가 없다면, 처음 `make:command`를 실행할 때 자동으로 만들어집니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 커맨드 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성에 적절한 값을 지정해야 합니다. 이 두 속성은 `list` 화면에 명령어가 표시될 때 활용됩니다. `signature` 속성을 사용해서 [커맨드 입력값 기대치](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되니, 실제 명령어 로직은 여기에 구현하세요.

예제 명령어를 살펴봅시다. 아래에서 볼 수 있듯, `handle` 메서드를 통해 필요한 의존성을 의존성 주입(Type Hint) 받을 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)가 메서드에 타입 힌트된 모든 의존성을 자동으로 주입합니다.

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * 콘솔 명령어의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * 콘솔 명령어 설명
     *
     * @var string
     */
    protected $description = '사용자에게 마케팅 이메일을 전송';

    /**
     * 콘솔 명령어 실행
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 코드 재사용성을 높이기 위해, 콘솔 명령어를 가볍게 유지하고 실제 작업은 어플리케이션 서비스로 위임하는 것이 좋습니다. 위 예제에서도 이메일 발송의 "무거운 작업"은 서비스 클래스에 위임하고 있음을 확인할 수 있습니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무 것도 반환하지 않고 명령어가 정상적으로 실행되면, 종료 코드는 `0`(성공)을 반환합니다. 직접 종료 코드를 명시적으로 설정하려면 `handle` 메서드에서 정수를 반환할 수 있습니다.

```php
$this->error('문제가 발생했습니다.');

return 1;
```

명령어 내부의 어느 메서드에서든 명령어를 "실패"시키고 싶다면, `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 실행을 종료하고 종료 코드 1을 반환합니다.

```php
$this->fail('문제가 발생했습니다.');
```

<a name="closure-commands"></a>
### 클로저 커맨드

클로저 기반 명령어는 클래스 대신 클로저로 콘솔 명령어를 정의할 수 있는 대안입니다. 컨트롤러 대신 라우트 클로저를 사용하는 것과 마찬가지로, 명령어 클로저도 명령어 클래스를 대신할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지는 않지만, 애플리케이션의 콘솔 진입점(라우트)을 정의합니다. 이 파일에서 `Artisan::command` 메서드를 사용하여 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. 이 메서드는 [명령어 시그니처](#defining-input-expectations)와 인자·옵션을 받는 클로저를 인수로 받습니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 내부적으로 커맨드 인스턴스에 바인딩되어 있기 때문에, 일반 커맨드 클래스에서 사용할 수 있는 모든 헬퍼 메서드를 자유롭게 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입 힌트

커맨드 클로저는 명령어의 인자와 옵션 외에도, [서비스 컨테이너](/docs/{{version}}/container)에서 꺼내올 추가 의존성도 타입힌트로 받을 수 있습니다.

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 커맨드 설명

클로저 기반 명령어를 정의할 때 `purpose` 메서드를 통해 명령어의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 실행 시 표시됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('사용자에게 마케팅 이메일 전송');
```

<a name="isolatable-commands"></a>
### Isolatable 커맨드

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

때로는 명령어가 한 번에 한 인스턴스만 실행되도록 보장하고 싶을 수 있습니다. 이를 위해, 커맨드 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

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

커맨드에 `Isolatable`이 지정되어 있으면, Laravel은 자동으로 명령어에 `--isolated` 옵션을 추가합니다. 해당 옵션으로 명령어를 실행하면, 이미 실행 중인 동일 명령어가 없을 때만 실행됩니다. 이는 애플리케이션의 기본 캐시 드라이버를 사용해 원자적(atomic) 락을 취득하는 방식으로 구현됩니다. 만약 이미 실행 중이라면 명령어는 실행되지 않지만, 그래도 성공 상태의 종료 코드로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

실행되지 못할 때 반환될 종료 코드를 지정하려면, `isolated` 옵션에 원하는 값을 넘기면 됩니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID

기본적으로 Laravel은 명령어 이름을 사용해 캐시에 원자적 락을 생성하는 데 쓰이는 문자열 키를 만듭니다. `isolatableId` 메서드를 커맨드 클래스에 정의하면 이 키를 커스터마이징할 수 있으며, 인자나 옵션 값을 키에 통합할 수 있습니다.

```php
/**
 * 커맨드의 isolatable ID 반환.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### 락 만료 시간

기본적으로 isolation 락은 명령어가 끝나면 만료됩니다. 또는 명령어가 중단되어 완료되지 않으면 1시간 후 만료됩니다. 만료 시간을 조정하려면, 커맨드에서 `isolationLockExpiresAt` 메서드를 정의하세요.

```php
use DateTimeInterface;
use DateInterval;

/**
 * 커맨드의 isolation 락 만료시점 반환.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대값 정의

콘솔 명령어를 작성할 때, 인자나 옵션 등 사용자 입력을 받아야 할 일이 흔합니다. Laravel은 명령어의 `signature` 속성을 사용해 기대하는 입력값을 매우 손쉽게 정의할 수 있도록 도와줍니다. 시그니처 속성 하나로 명령어의 이름, 인자, 옵션을 선언적이면서도 라우트 문법처럼 명확하게 정의할 수 있습니다.

<a name="arguments"></a>
### 인자

사용자 입력 인자와 옵션은 모두 중괄호로 감쌉니다. 다음 예제에서는 `user`라는 필수 인자 하나가 정의되어 있습니다.

```php
/**
 * 콘솔 명령어의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인자를 선택적으로 만들거나 기본값을 지정할 수도 있습니다.

```php
// 선택적 인자...
'mail:send {user?}'

// 기본값이 있는 선택적 인자...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션도 인자처럼 또 다른 형태의 사용자 입력입니다. 옵션은 명령줄에서 두 개의 하이픈(`--`)으로 시작합니다. 값이 있는 옵션과 값이 필요 없는 옵션(스위치) 두 가지가 있습니다. 스위치는 boolean처럼 동작합니다.

```php
/**
 * 콘솔 명령어의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예에서 `--queue` 스위치를 명령어에 전달할 수 있고, 같은 스위치가 있으면 true, 없으면 false입니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값이 필요한 옵션은 옵션명 끝에 `=` 문자를 붙여 정의합니다.

```php
/**
 * 콘솔 명령어의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이런 경우 사용자는 아래와 같이 옵션 값을 지정할 수 있습니다. 명령어 실행 시 옵션이 없으면 값은 `null`이 됩니다.

```shell
php artisan mail:send 1 --queue=default
```

기본값을 주려면 옵션명 뒤에 기본값을 명시하세요.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션을 정의할 때 단축키를 부여하려면, 옵션명 앞에 단축키를 추가하고, `|` 구분자로 연결하세요.

```php
'mail:send {user} {--Q|queue}'
```

단축키로 명령어를 실행할 때는 한 개의 하이픈으로 시작하고, 값 지정에는 `=` 대신 바로 붙여줍니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 입력값을 받을 인자나 옵션을 정의하려면, `*` 문자를 사용합니다. 우선 인자 예시를 보겠습니다.

```php
'mail:send {user*}'
```

명령어 호출 시 `user` 인자에 여러 값을 순서대로 넘겨줄 수 있습니다. 예를 들어:

```shell
php artisan mail:send 1 2
```

이렇게 실행하면 `user` 인자의 값은 `[1, 2]` 배열이 됩니다.

`*` 문자와 선택적 인자를 같이 쓰면 인자가 0개 이상일 수도 있습니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 받는 옵션을 정의하려면, 전달되는 각 옵션 값 앞에 옵션명을 붙이면 됩니다.

```php
'mail:send {--id=*}'
```

명령어 호출 예시는 다음과 같습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인자나 옵션에 설명을 추가하려면 이름 뒤에 콜론으로 구분 후 설명을 적습니다. 명령어 정의가 길 경우 줄바꿈으로 나눠도 됩니다.

```php
/**
 * 콘솔 명령어의 이름과 시그니처
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : 사용자 ID}
                        {--queue : 작업을 큐에 넣을지 여부}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력 프롬프트

명령어에 필수 인자가 있지만 제공되지 않을 경우, 사용자는 에러 메시지를 받게 됩니다. 대신, 누락된 인자가 있을 때 자동으로 사용자에게 입력을 요청하도록 설정할 수 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하세요.

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * 콘솔 명령어의 이름과 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

필수 인자가 누락되었다면 Laravel은 자동으로 인자명이나 설명에 따라 친절하게 질문을 만들어 입력을 요청합니다. 질문 문구를 커스터마이징하려면 `promptForMissingArgumentsUsing` 메서드를 구현하여, 인자명-질문 쌍의 배열을 반환하면 됩니다.

```php
/**
 * 누락 입력 인자에 대해 사용할 질문 반환
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => '어떤 사용자 ID가 메일을 받아야 하나요?',
    ];
}
```

튜플 배열로 질문과 플레이스홀더를 함께 지정할 수도 있습니다.

```php
return [
    'user' => ['어떤 사용자 ID가 메일을 받아야 하나요?', '예: 123'],
];
```

프롬프트를 완전히 제어하려면, 클로저를 반환해 사용자 입력값을 받을 수 있습니다.

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
> 자세한 사용법과 다양한 프롬프트에 대한 정보는 [Laravel Prompts](/docs/{{version}}/prompts) 문서를 참고하세요.

옵션([options](#options)) 입력도 프롬프트로 받고 싶다면, 명령어의 `handle` 메서드에서 프롬프트를 추가할 수 있습니다. 단, 자동 프롬프트 이후에만 옵션 입력을 프롬프트하고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현하세요.

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * 누락된 인자 입력 프롬프트 후 동작 수행
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: '메일을 큐에 넣으시겠습니까?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
## 커맨드 I/O

<a name="retrieving-input"></a>
### 입력 값 가져오기

명령어가 실행 중일 때, 전달받은 인자와 옵션 값을 코드를 통해 쉽게 접근할 수 있습니다. `argument`, `option` 메서드를 활용하세요. 해당 인자·옵션이 없다면 `null`이 반환됩니다.

```php
/**
 * 콘솔 명령어 실행
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인자를 `array`로 받으려면 `arguments` 메서드를 사용하세요.

```php
$arguments = $this->arguments();
```

옵션도 `option`/`options` 메서드로 쉽게 가져올 수 있습니다.

```php
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력값 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/{{version}}/prompts)는 플레이스홀더, 검증 등 브라우저적 기능을 명령줄에 제공하는, 아름답고 사용자 친화적 폼을 위한 PHP 패키지입니다.

출력뿐만 아니라 사용자에게 정보를 입력받을 수도 있습니다. `ask` 메서드는 사용자에게 질문하고, 입력을 받아 반환합니다.

```php
/**
 * 콘솔 명령어 실행
 */
public function handle(): void
{
    $name = $this->ask('이름이 무엇인가요?');

    // ...
}
```

`ask`는 두 번째 인수로 기본값도 받을 수 있습니다.

```php
$name = $this->ask('이름이 무엇인가요?', 'Taylor');
```

`secret` 메서드는 `ask`와 유사하지만, 입력값이 콘솔에 보이지 않도록 처리합니다. 비밀번호 등 민감한 정보 입력에 유용합니다.

```php
$password = $this->secret('비밀번호는 무엇인가요?');
```

<a name="asking-for-confirmation"></a>
#### 확인(yes/no) 질문

사용자에게 단순한 "예/아니오"를 묻고 싶으면 `confirm` 메서드를 사용하세요. 기본적으로 응답이 `y`(또는 yes)이면 true, 아니면 false를 반환합니다.

```php
if ($this->confirm('계속 진행하시겠습니까?')) {
    // ...
}
```

기본 응답값을 true로 하려면, `confirm`의 두 번째 인수로 true를 넘기면 됩니다.

```php
if ($this->confirm('계속 진행하시겠습니까?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드는 자동완성 후보 목록을 제공합니다. 유저는 자동완성 후보 외의 아무 답이나 제출할 수도 있습니다.

```php
$name = $this->anticipate('이름이 무엇인가요?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 넘기면, 사용자가 입력할 때마다 후보 목록을 동적으로 반환할 수 있습니다.

```php
use App\Models\Address;

$name = $this->anticipate('주소가 무엇인가요?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택 질문

정해진 선택지 중에서 값을 입력받으려면 `choice` 메서드를 사용하세요. 세 번째 인수로 인덱스를 지정하면 선택하지 않을 때 반환할 기본값입니다.

```php
$name = $this->choice(
    '이름이 무엇인가요?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째, 다섯 번째 인수로 최대 시도 횟수, 다중 선택 허용 여부 등을 지정할 수 있습니다.

```php
$name = $this->choice(
    '이름이 무엇인가요?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### 출력 작성

콘솔에 메시지를 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 내용에 적합한 ANSI 색상으로 표시됩니다. 예를 들어 정보를 출력하려면 `info` 메서드를 사용하세요(일반적으로 초록색).

```php
/**
 * 콘솔 명령어 실행
 */
public function handle(): void
{
    // ...

    $this->info('명령어가 성공적으로 실행되었습니다!');
}
```

에러 메시지는 `error` 메서드를 사용하세요(일반적으로 빨간색).

```php
$this->error('문제가 발생했습니다!');
```

색상 없이 평문을 출력하려면 `line` 메서드를 사용하세요.

```php
$this->line('이 내용을 화면에 표시');
```

공백 줄을 출력하려면 `newLine` 메서드를 사용할 수 있습니다.

```php
// 한 줄 출력
$this->newLine();

// 세 줄 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행/열의 데이터를 보기 좋게 출력할 수 있습니다. 컬럼명 배열과 데이터 배열만 넘기면 Laravel이 테이블의 너비와 높이를 자동으로 계산해줍니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

작업 시간이 긴 경우, 작업 진행률을 알려주는 진행 바를 표시할 수 있습니다. `withProgressBar`를 사용하면, 주어진 이터러블 대상마다 진행 바가 진행됩니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 섬세하게 진행 바를 제어하고 싶다면, 전체 단계 수를 정의한 후 각 단계마다 진행 바를 한 칸씩 직접 이동시키면 됩니다.

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
> 추가 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 커맨드 등록

Laravel은 기본적으로 `app/Console/Commands`에 있는 모든 명령어를 자동 등록합니다. 다른 디렉토리도 Artisan 커맨드 경로로 스캔하고 싶다면 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용하세요.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

클래스명을 직접 지정해서 수동 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅되면, 모든 명령어가 [서비스 컨테이너](/docs/{{version}}/container)로부터 resolve되어 Artisan에 등록합니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식으로 커맨드 실행

CLI 이외의 환경(예: 라우트나 컨트롤러)에서 Artisan 명령어를 실행해야 할 일이 있을 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용하세요. 첫 번째 인자로 명령어 시그니처나 클래스 이름, 두 번째 인자로 명령어 파라미터 배열을 넘깁니다. 반환값은 종료 코드입니다.

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

명령어 전체를 문자열로 넘길 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열값 넘기기

옵션에 여러 값을 넘길 필요가 있는 경우(옵션이 배열로 정의된 경우), 값 배열을 직접 전달하세요.

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 넘기기

문자열 대신 true/false 값을 받는 옵션(예: `migrate:refresh`의 `--force` 플래그 등)의 경우, 값으로 true 또는 false를 넘기면 됩니다.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 [큐 워커](/docs/{{version}}/queues)에서 백그라운드로 처리하도록 할 수 있습니다. 이 메서드를 사용하기 전, 큐 설정을 마치고 큐 리스너를 실행 중이어야 합니다.

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`, `onQueue` 메서드로 연결명이나 큐명을 지정할 수도 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 커맨드에서 커맨드 호출하기

때때로 다른 Artisan 명령어 안에서 명령어를 호출하고 싶을 수도 있습니다. 이럴 때는 `call` 메서드를 사용하세요. 명령어명 및 인자/옵션 배열을 넘깁니다.

```php
/**
 * 콘솔 명령어 실행
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

호출시 출력까지 억제하려면 `callSilently` 메서드를 사용하세요. 인자 구성은 `call`과 같습니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 핸들링

운영체제(OS)는 실행 중인 프로세스에 시그널을 전송할 수 있습니다. 예를 들어, `SIGTERM`은 프로그램을 종료하라는 요청입니다. Artisan 콘솔 명령어에서 시그널을 수신하고 발생 시 코드를 실행하고 싶으면 `trap` 메서드를 사용하십시오.

```php
/**
 * 콘솔 명령어 실행
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 시그널을 동시에 감지하려면, 시그널 배열을 `trap`에 넘기세요.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan의 `make` 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 "스텁(stub)" 파일을 기반으로 하며, 입력에 맞게 내용이 채워집니다. 단, 이 스텁에 약간의 변경이 필요하다면 `stub:publish` 명령어로 주요 스텁을 애플리케이션에 복사하여 자유롭게 수정할 수 있습니다.

```shell
php artisan stub:publish
```

복사된 스텁은 애플리케이션 루트의 `stubs` 디렉토리에 위치합니다. 이 스텁을 수정하면 이후 Artisan의 `make` 명령어로 생성되는 클래스에 수정 사항이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 중 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan 실행 직후 발생하며, `CommandStarting`은 명령어 실행 직전, `CommandFinished`는 실행 완료 시 발생합니다.