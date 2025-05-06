# 아티즌 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대 정의하기](#defining-input-expectations)
    - [인자(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열(Input Arrays)](#input-arrays)
    - [입력 설명(Input Descriptions)](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [명령어 입출력(I/O)](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력 프롬프트하기](#prompting-for-input)
    - [출력하기](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그램적으로 명령어 실행하기](#programmatically-executing-commands)
    - [명령어 내에서 다른 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이즈](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 내장된 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 유용한 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용하세요:

```shell
php artisan list
```

각 명령어에는 명령어가 사용할 수 있는 인자와 옵션을 보여주고 설명하는 "help" 화면도 포함되어 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙이세요:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)을 로컬 개발 환경으로 사용 중이라면, Artisan 명령을 실행할 때 `sail` CLI를 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 안에서 Artisan 명령을 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 하는 Laravel 프레임워크용 강력한 REPL(대화형 쉘)입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 Tinker를 제거했다면 Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션을 다루면서 핫 리로딩, 멀티라인 코드 편집, 자동완성을 원하신다면 [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 Eloquent 모델, 작업(Job), 이벤트 등 애플리케이션 전체를 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령을 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일을 배포하려면 `vendor:publish` 명령을 사용하세요:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메소드는 잡을 큐에 넣기 위해 가비지 컬렉션을 의존합니다. 따라서 Tinker에서는 `Bus::dispatch` 또는 `Queue::push`를 사용해서 잡을 큐로 보내는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록(Command Allow List)

Tinker는 "허용" 목록을 사용하여 쉘 내에서 실행할 수 있는 Artisan 명령어를 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령이 허용됩니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 피해야 할 클래스(Classes That Should Not Be Aliased)

보통 Tinker에서는 사용하는 클래스들을 자동으로 별칭(alias) 처리합니다. 그러나 특정 클래스는 별칭을 하지 않도록 설정하고 싶을 수 있습니다. 이 경우, 해당 클래스를 `tinker.php`의 `dont_alias` 배열에 추가하세요:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan에서 제공하는 명령어 이외에도, 직접 커스텀 명령어를 만들 수 있습니다. 명령어는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 로드할 수 있다면 원하는 위치에 저장해도 됩니다.

<a name="generating-commands"></a>
### 명령어 생성

새로운 명령어를 만들기 위해서는 `make:command` Artisan 명령을 사용할 수 있습니다. 이 명령은 `app/Console/Commands` 디렉터리에 새 명령 클래스 파일을 생성합니다. 만약 이 디렉터리가 없다면 최초 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후, 클래스의 `signature`와 `description` 속성에 적절한 값을 설정해야 합니다. 이 속성들은 `list` 화면에 명령어를 표시할 때 사용됩니다. `signature` 속성에서는 [명령어의 입력 기대값](#defining-input-expectations)도 정의할 수 있습니다. `handle` 메소드는 명령어가 실행될 때 호출되며, 여기에 명령어의 실제 로직을 작성하면 됩니다.

아래는 예시 명령어입니다. `handle` 메소드에서 필요한 의존성을 타입힌트로 명시하면 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 주입합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * 콘솔 명령의 이름과 시그니처.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * 콘솔 명령의 설명.
     *
     * @var string
     */
    protected $description = '사용자에게 마케팅 이메일을 전송합니다';

    /**
     * 콘솔 명령 실행.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 코드 재사용성을 높이기 위해, 콘솔 명령어는 최대한 가볍게 만들고 주요 작업은 서비스 클래스에 위임하는 것이 좋습니다. 위 예시에서도 이메일 전송의 "실질적 역할"은 별도의 서비스 클래스를 통해 수행됩니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메소드가 아무 값도 반환하지 않고 성공적으로 실행되면, 명령은 `0`의 종료 코드로 종료되어 성공을 나타냅니다. 명령의 종료 코드(Exit code)를 직접 지정하고 싶다면 `handle`에서 정수형 값을 반환하면 됩니다:

```php
$this->error('문제가 발생했습니다.');

return 1;
```

명령 내 어떤 메소드에서든 명령을 즉시 "실패"로 종료시키고 싶다면 `fail` 메소드를 사용할 수 있습니다. 이 메소드는 즉시 실행을 중단하고 종료 코드 1로 명령을 마칩니다:

```php
$this->fail('문제가 발생했습니다.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저(Closure) 기반 명령어는 명령 클래스를 정의하는 것과는 다른 대안을 제공합니다. 컨트롤러 대신 라우트 클로저를 사용할 수 있는 것처럼, 명령어 클로저도 명령 클래스의 대체 방식입니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하는 파일이 아니지만, 애플리케이션으로 진입하는 콘솔 기반 엔트리 포인트(라우트) 역할을 합니다. 이 파일에서는 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 모두 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와, 명령어 인자와 옵션을 받는 클로저 두 개의 인수를 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 해당 명령 인스턴스에 바인딩되므로, 클래스 기반 명령에서 사용할 수 있는 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

명령어 클로저는 명령어 인자나 옵션 외에도, [서비스 컨테이너](/docs/{{version}}/container)에서 해결할 추가 의존성도 타입힌트로 받을 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 기반 명령어를 정의할 때 `purpose` 메서드로 명령어의 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help`를 실행할 때 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('사용자에게 마케팅 이메일을 전송합니다');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버를 공유해야 합니다.

동일 명령 인스턴스가 동시에 여러 개 실행되지 않도록 제어하고 싶을 수 있습니다. 이럴 때 명령 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다:

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

명령을 `Isolatable`로 표시하면, Laravel은 명령에 자동으로 `--isolated` 옵션을 추가합니다. 이 옵션으로 명령을 호출하면, 이미 같은 명령의 다른 인스턴스가 실행 중인지 확인 후 없으면 실행합니다. 내부적으로는 애플리케이션의 기본 캐시 드라이버로 원자적 락을 획득하여 이를 구현합니다. 이미 실행 중이면 실행하지 않고, 명령은 성공 상태(exit code 0)로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어가 실행될 수 없을 때 반환할 종료 코드를 지정하려면 `isolated` 옵션에 원하시는 값을 지정하면 됩니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### Lock ID

기본적으로 Laravel은 명령어 이름을 사용하여 캐시에서 락을 획득할 때 사용할 키 문자열을 생성합니다. 명령어 클래스에서 `isolatableId` 메서드를 정의하여 이 키를 커스터마이즈할 수 있습니다. 예를 들어 명령의 인자나 옵션을 키에 통합할 수 있습니다:

```php
/**
 * 명령어의 isolatable ID 반환.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### 락 만료시간

기본적으로 isolation 락은 명령이 끝남과 동시에 만료됩니다. 명령이 중단되어 종료할 수 없을 때는 1시간 후 만료됩니다. 락 만료시간을 조정하려면 명령 클래스에서 `isolationLockExpiresAt` 메서드를 정의하세요:

```php
use DateTimeInterface;
use DateInterval;

/**
 * 명령어 isolation 락 만료 시점 정의.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대 정의하기

콘솔 명령어를 작성할 때, 사용자의 입력을 인자(Argument)나 옵션(Option) 형태로 받는 경우가 많습니다. Laravel은 명령 클래스의 `signature` 속성을 통해 이러한 입력값 정의를 매우 간편하게 제공합니다. `signature`에서는 명령어 이름, 인자, 옵션을 라우트 스타일로 일괄적으로 선언할 수 있습니다.

<a name="arguments"></a>
### 인자(Arguments)

사용자에서 전달받는 모든 인자와 옵션은 중괄호로 감쌉니다. 아래 예시에서는 `user`라는 필수 인자 하나를 정의합니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인자를 선택적으로 하거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인자
'mail:send {user?}'

// 선택적 인자와 기본값 지정
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션도 인자처럼 사용자 입력의 한 형태입니다. 옵션은 명령줄에서 제공할 때 두 개의 하이픈(`--`)을 접두사로 붙입니다. 옵션에는 값이 필요한 옵션과 값이 필요 없는(불리언 스위치) 옵션 두 가지가 있습니다. 아래는 값을 필요로 하지 않는 스위치형 옵션 예시입니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

이 예시에서 `--queue` 스위치는 Artisan 명령 호출 시 지정할 수 있습니다. 만약 전달되면 옵션의 값은 `true`, 전달되지 않으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값이 필요한 옵션은 옵션 이름 끝에 `=` 기호를 붙여 나타냅니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

사용자는 아래와 같이 옵션 값도 함께 전달할 수 있습니다. 옵션이 지정되지 않으면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면 옵션명 뒤에 기본값을 씁니다. 사용자가 옵션 값을 전달하지 않으면 이 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 정의 시 단축키(Shortcut)를 지정하고 싶다면 옵션 이름 앞에 단축키를 쓰고, `|` 문자로 구분합니다:

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어를 실행할 때 단축키 옵션은 한 개의 하이픈만 붙이며, 값을 줄 때는 `=` 없이 바로 붙입니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열(Input Arrays)

인자나 옵션이 여러 값을 받을 수 있도록 하려면 `*` 문자를 사용합니다. 아래는 여러 값을 받을 수 있는 인자 정의 예시입니다:

```php
'mail:send {user*}'
```

이렇게 하면 명령어 호출 시 여러 `user` 인자를 배열로 받을 수 있습니다. 예를 들면 아래와 같이 입력하면 `user` 값은 `[1, 2]`가 됩니다:

```shell
php artisan mail:send 1 2
```

`*` 문자를 선택적 인자와 함께 써서, 인자의 수가 0개 이상이 되도록 할 수도 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

옵션이 여러 값을 받을 수 있도록 정의하려면 아래와 같이 합니다. 각각의 옵션 값은 옵션 이름을 반복해서 전달해야 합니다:

```php
'mail:send {--id=*}'
```

아래처럼 여러 개의 `--id` 옵션 값을 전달해서 실행할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명(Input Descriptions)

입력 인자나 옵션에 설명을 달고 싶을 때는 콜론으로 이름과 설명을 구분합니다. 명령어 정의가 길어질 경우 여러 줄로 나눠 써도 무방합니다:

```php
/**
 * 콘솔 명령의 이름과 시그니처.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : 유저의 ID}
                        {--queue : 이 잡을 큐에 넣을지 여부}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력값 프롬프트

명령어의 필수 인자를 사용자가 입력하지 않으면 에러 메시지가 표시됩니다. 대신 해당 인자가 빠졌을 때 자동으로 입력 프롬프트를 띄우게 하려면 `PromptsForMissingInput` 인터페이스를 구현하세요:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * 콘솔 명령의 이름과 시그니처.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Laravel이 필수 인자를 입력받아야 하면, 해당 인자 이름이나 설명을 이용해 자동으로 질문합니다. 질문 문구를 직접 지정하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현하여, 인자명 키와 질문 값 쌍의 배열을 반환하세요:

```php
/**
 * 누락된 입력 인자 프롬프트 질문 반환.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => '어떤 사용자 ID로 메일을 보낼까요?',
    ];
}
```

튜플(질문, 플레이스홀더) 형태로 플레이스홀더 텍스트도 제공할 수 있습니다:

```php
return [
    'user' => ['어떤 사용자 ID로 메일을 보낼까요?', '예: 123'],
];
```

프롬프트를 완전히 커스터마이즈하고 싶다면, 클로저를 반환해 사용자에게 직접 입력을 받아올 수도 있습니다:

```php
use App\Models\User;
use function Laravel\Prompts\search;

return [
    'user' => fn () => search(
        label: '사용자 검색:',
        placeholder: '예: Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
> 더 많은 프롬프트 예제와 사용법은 [Laravel Prompts](/docs/{{version}}/prompts) 문서에서 확인하실 수 있습니다.

명령어의 `handle` 메소드에서 추가로 옵션을 프롬프트할 수도 있습니다. 다만, 누락된 인자 프롬프트 이후에만 옵션 프롬프트를 띄우고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하세요:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * 사용자에게 누락 인자 프롬프트 후 실행되는 동작 정의.
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
## 명령어 입출력(I/O)

<a name="retrieving-input"></a>
### 입력값 가져오기

명령어 실행 중, 받은 인자나 옵션 값을 사용해야 할 때가 있습니다. `argument`와 `option` 메소드를 사용하세요. 인자나 옵션이 없다면 `null`이 반환됩니다:

```php
/**
 * 콘솔 명령어 실행.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인자를 `array` 형태로 가져오려면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로, `option` 또는 모든 옵션을 `options` 메소드로 배열 형태로 조회할 수 있습니다:

```php
// 특정 옵션 조회...
$queueName = $this->option('queue');

// 모든 옵션 배열로 조회...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/{{version}}/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가하는 PHP 패키지로, 플레이스홀더와 입력 유효성 검사 등 브라우저 수준의 기능을 지원합니다.

출력뿐 아니라 명령 실행 중 사용자 입력을 직접 받을 수도 있습니다. `ask` 메서드는 질문을 띄우고, 사용자의 입력값을 받아 반환합니다:

```php
/**
 * 콘솔 명령어 실행.
 */
public function handle(): void
{
    $name = $this->ask('이름이 무엇인가요?');

    // ...
}
```

사용자 입력이 없을 때 반환할 기본값도 두 번째 인수로 지정할 수 있습니다:

```php
$name = $this->ask('이름이 무엇인가요?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 사용자가 콘솔에서 입력할 때 글자가 보이지 않습니다. 비밀번호 등 민감 정보 입력에 유용합니다:

```php
$password = $this->secret('비밀번호를 입력해주세요.');
```

<a name="asking-for-confirmation"></a>
#### 예/아니오 확인

사용자에게 단순히 "예/아니오"를 묻고 싶다면 `confirm` 메서드를 사용하세요. 기본값은 `false`입니다. 사용자가 `y` 또는 `yes`를 입력하면 `true`가 반환됩니다.

```php
if ($this->confirm('계속하시겠습니까?')) {
    // ...
}
```

확인 프롬프트의 기본값을 `true`로 하려면 두 번째 인수에 `true`를 넘기세요:

```php
if ($this->confirm('계속하시겠습니까?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성(Auto-Completion)

`anticipate` 메서드는 가능한 선택지에 대해 자동완성을 지원합니다. 사용자는 힌트 이외의 답변도 입력할 수 있습니다.

```php
$name = $this->anticipate('이름이 무엇인가요?', ['Taylor', 'Dayle']);
```

자동완성 옵션을 동적으로 지정하려면, 두 번째 인수에 클로저를 전달하세요. 사용자가 타이핑할 때마다 클로저가 호출되어 결과 배열을 반환하면 됩니다:

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
#### 다중 선택(Multiple Choice)

사용자에게 미리 정의된 선택지 목록을 질문하려면 `choice` 메서드를 사용하세요. 세 번째 인수로 인덱스를 지정하면 기본값으로 사용됩니다:

```php
$name = $this->choice(
    '이름이 무엇인가요?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한, 네 번째와 다섯 번째 인수로 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

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
### 출력하기

콘솔에 정보를 표시할 때는 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각 출력방식은 용도에 맞는 ANSI 컬러를 사용합니다. 예를 들어, `info`는 주로 녹색으로 표시됩니다:

```php
/**
 * 콘솔 명령어 실행.
 */
public function handle(): void
{
    // ...

    $this->info('명령이 성공적으로 실행되었습니다!');
}
```

에러 메시지를 표시하려면 `error` 메서드를 사용하세요. 일반적으로 빨간색으로 출력됩니다:

```php
$this->error('문제가 발생했습니다!');
```

평범한(색 없는) 텍스트는 `line` 메서드를 사용하세요:

```php
$this->line('이 텍스트를 출력');
```

빈 줄을 삽입하려면 `newLine` 메서드를 사용하세요:

```php
// 하나의 빈 줄
$this->newLine();

// 세 줄
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드는 여러 행/열의 데이터 출력을 깔끔하게 자동 포매팅합니다. 컬럼명과 데이터 배열만 넘기면 됩니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 프로그레스 바

오래 걸리는 작업의 경우, 진행률을 보여주는 프로그레스 바(progress bar)를 표시하면 유용합니다. `withProgressBar` 메서드를 사용하면, 전달한 iterable 데이터를 순회할 때마다 프로그레스 바가 진행됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 세밀하게 프로그레스 바를 제어하려면 아래처럼 작성할 수 있습니다:

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
> 더 고급 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

Laravel은 기본적으로 `app/Console/Commands` 디렉터리의 모든 명령어를 자동으로 등록합니다. 추가로 다른 디렉터리도 Artisan 명령이 검색되게 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용하세요:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면 각 명령어 클래스를 직접 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 애플리케이션의 모든 명령은 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해결되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램적으로 명령어 실행하기

CLI(콘솔)가 아닌 곳에서 Artisan 명령어를 실행해야 할 경우가 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령을 실행하고자 할 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. 첫 인수로 명령 시그니처 또는 클래스 이름, 두 번째 인수로 명령 인자 배열을 받습니다. 종료 코드가 반환됩니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

명령어 전체를 문자열로 넘겨 호출할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어 옵션이 배열을 받을 수 있도록 정의되었다면, 해당 옵션에 배열을 넘길 수 있습니다:

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

문자열 값을 받지 않는 옵션(예: `migrate:refresh` 명령의 `--force` 플래그)에 값을 지정하려면, 옵션 값으로 `true`나 `false`를 전달하세요:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 [큐 워커](/docs/{{version}}/queues)에서 백그라운드로 처리할 수 있습니다. 사용 전 큐를 설정하고 큐 리스너를 실행 중이어야 합니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`과 `onQueue` 메서드를 사용해 명령을 보낼 연결 또는 큐 이름도 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 내에서 다른 명령어 호출

기존의 Artisan 명령어에서 다른 명령어를 호출하고 싶으면, `call` 메서드를 사용할 수 있습니다. 첫 인수로 명령 이름, 두 번째 인수로 인자/옵션 배열을 넘깁니다:

```php
/**
 * 콘솔 명령어 실행.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

다른 콘솔 명령과 모든 출력을 감추고 싶다면 `callSilently` 메서드를 사용하세요. 시그니처는 `call` 과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제에서는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램 종료 요청 신호입니다. Artisan 콘솔 명령에서 시그널을 감지하고 발생시 특정 코드를 실행하려면 `trap` 메서드를 사용하세요:

```php
/**
 * 콘솔 명령어 실행.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 개의 시그널을 동시에 감지하려면 시그널 배열을 `trap`에 넘기면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이즈

Artisan 콘솔의 `make` 명령은 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 "스텁(stub)" 파일을 기반으로 하고, 입력값에 따라 알맞게 파일이 생성됩니다. 하지만 생성된 파일의 일부를 수정하고 싶다면 `stub:publish` 명령으로 기본 스텁들을 애플리케이션에 퍼블리시 한 후 직접 커스터마이즈 할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 파일을 편집하면 이후 Artisan `make` 명령으로 관련 클래스를 생성할 때 커스텀 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting`은 Artisan 실행 즉시, `CommandStarting`은 명령 실행 직전, `CommandFinished`는 명령 실행이 끝나면 각각 발생합니다.