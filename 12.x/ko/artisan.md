# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [독립 실행 가능한 명령어](#isolatable-commands)
- [입력 기대사항 정의하기](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력 프롬프트](#prompting-for-missing-input)
- [명령어 입출력](#command-io)
    - [입력 가져오기](#retrieving-input)
    - [입력 프롬프트](#prompting-for-input)
    - [출력 쓰기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [프로그래밍 방식으로 명령어 실행하기](#programmatically-executing-commands)
    - [명령어 내에서 다른 명령어 호출하기](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 커맨드 라인 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움을 주는 여러 유용한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 "help" 화면이 포함되어 있으며, 명령어의 인수와 옵션을 보여주고 설명합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙입니다:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

만약 [Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용 중이라면, Artisan 명령어를 호출할 때 `sail` 커맨드를 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크를 위한 강력한 REPL로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만, 이전에 애플리케이션에서 제거했다면 Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션 상호작용 시 핫 리로딩, 멀티라인 코드 편집, 자동 완성을 원한다면 [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 Eloquent 모델, 잡, 이벤트 등 Laravel 애플리케이션 전체와 커맨드 라인에서 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker 설정 파일을 게시하려면 `vendor:publish` 명령어를 사용합니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker에서는 작업을 디스패치할 때 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 명령어 허용 목록

Tinker는 셸 내에서 실행 가능한 Artisan 명령어를 "허용" 목록으로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 추가 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭을 하지 않을 클래스

보통 Tinker는 상호작용하는 클래스에 대해 자동으로 별칭(alias)을 생성합니다. 그러나 몇몇 클래스에는 별칭을 생성하지 않게 하려면, `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 나열하세요:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan이 제공하는 명령어 외에도, 자신만의 커스텀 명령어를 만들 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 저장되지만, 다른 디렉터리를 사용하려면 Laravel에게 [다른 디렉터리 스캔 설정](#registering-commands)을 알려주면 됩니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 생성합니다. 만약 애플리케이션에 해당 디렉터리가 없으면, `make:command`를 처음 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 값들은 `list` 화면에서 명령어를 표시할 때 사용됩니다. `signature` 속성은 [명령어 입력 기대사항](#defining-input-expectations)도 정의할 수 있습니다. 명령어 실행 시 `handle` 메서드가 호출되며, 이곳에 명령어 로직을 작성하세요.

다음은 예제 명령어입니다. `handle` 메서드에서 필요한 의존성을 주입받을 수 있고, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 메서드 시그니처에 타입힌트된 모든 의존성을 자동으로 주입합니다:

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
> 코드 재사용성을 높이기 위해, 콘솔 명령어는 가능한 가볍게 유지하고 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋은 실무입니다. 위 예제에서는 이메일 전송의 핵심 로직을 서비스 클래스로 주입받아 처리했습니다.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무것도 반환하지 않고 명령어가 성공적으로 실행되면, 종료 코드는 `0`으로 간주되어 성공을 의미합니다. 하지만 필요하다면 `handle` 메서드가 정수형 값을 반환하여 수동으로 종료 코드를 지정할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내부 어느 메서드에서도 바로 실패시키고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령어 실행을 종료하고 종료 코드를 `1`로 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스를 정의하는 대신 콘솔 명령어를 작성하는 대안입니다. 라우트에서 클로저를 사용하는 것처럼, 클로저 명령어는 클래스 명령어의 대안으로 생각할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션의 콘솔 엔트리 포인트(라우팅)를 정의합니다. 여기에서 `Artisan::command` 메서드를 사용해 클로저 기반 명령어를 정의할 수 있습니다. 이 메서드는 두 개의 인자를 받는데, 첫 번째는 [명령어 시그니처](#defining-input-expectations), 두 번째는 명령어의 인수와 옵션을 받는 클로저입니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 내부적으로 명령어 인스턴스에 바인딩되어 있어, 전체 명령어 클래스에서 사용할 수 있는 모든 헬퍼 메서드에 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

클로저 명령어에서 인수와 옵션 외에, [서비스 컨테이너](/docs/12.x/container)로부터 주입받고 싶은 의존성을 타입힌팅할 수 있습니다:

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

클로저 명령어 정의 시 `purpose` 메서드로 명령어 설명을 더할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령어 실행 시 보여집니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 독립 실행 가능한 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 혹은 `array`여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신 중이어야 합니다.

경우에 따라 명령어 인스턴스가 한번에 하나만 실행되도록 보장하고 싶을 때가 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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

`Isolatable` 상태로 표시된 명령어는 Laravel이 자동으로 `--isolated` 옵션을 추가해 줍니다. 해당 옵션과 함께 호출할 때, Laravel은 애플리케이션 기본 캐시 드라이버를 사용해 원자 잠금(atomic lock)을 시도하여 이미 같은 명령어 인스턴스가 실행 중이면 실행을 건너뜁니다. 하지만 이 경우에도 명령어는 성공 종료 코드로 정상 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어 실행이 불가능할 때 반환할 종료 코드를 지정하고 싶으면 `isolated` 옵션에 상태 코드를 명시할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 잠금 ID

기본적으로 Laravel은 잠금을 걸기 위한 문자열 키를 명령어 이름으로 생성합니다. 하지만 `isolatableId` 메서드를 Artisan 명령어 클래스에 정의하여 인수나 옵션을 키에 포함하도록 키를 커스터마이징할 수 있습니다:

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
#### 잠금 만료 시간

기본적으로 명령어가 종료되면 잠금이 만료됩니다. 명령어가 중단되어 정상 종료하지 못할 경우, 잠금은 1시간 뒤 자동 만료됩니다. `isolationLockExpiresAt` 메서드를 직접 구현하여 잠금 만료 시간을 변경할 수도 있습니다:

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
## 입력 기대사항 정의하기

콘솔 명령어를 작성할 때, 사용자로부터 인수(argument)나 옵션(option)을 통해 입력받는 것이 일반적입니다. Laravel은 `signature` 속성으로 명령어의 이름, 인수, 옵션을 한 줄의 경로(Route)처럼 표현한 문법으로 편리하게 정의할 수 있게 해줍니다.

<a name="arguments"></a>
### 인수 (Arguments)

모든 사용자 입력 인수와 옵션은 중괄호 `{}`로 감쌉니다. 다음 예제는 하나의 필수 인수 `user`를 정의한 경우입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택사항으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션 (Options)

옵션은 인수와 달리, 커맨드 라인에서 `--` 두 개 하이픈으로 시작하는 입력 형태입니다. 옵션은 값이 필요 없는 스위치 형태와 값을 받는 두 종류가 있습니다. 값이 필요 없는 옵션은 불리언 스위치처럼 동작합니다. 예를 들어:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예제에서 `--queue` 스위치를 사용하면 옵션 값은 `true`가 되고, 지정하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 필요한 옵션

값이 필요한 옵션의 이름 뒤에는 `=`을 붙여야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

사용자가 옵션에 값을 넘길 수 있습니다. 옵션이 주어지지 않으면 값은 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

기본값을 지정하려면 이름 뒤에 기본값을 지정하세요:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 바로 가기 키

옵션 이름 앞에 바로 가기 키를 지정할 수 있으며, `|` 구분자로 분리합니다:

```php
'mail:send {user} {--Q|queue}'
```

터미널에서 옵션 바로 가기 키는 한 개의 하이픈만 사용하며, 값 지정 시 `=`를 넣지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

여러 값을 받는 인수나 옵션을 정의하려면 `*` 문자를 사용하세요. 예를 들어, 다수의 인수 값을 받는 인수 정의:

```php
'mail:send {user*}'
```

명령어 실행 시 여러 인수를 순서대로 넘길 수 있습니다. 다음은 `user` 값이 `[1, 2]` 배열로 설정되는 예제입니다:

```shell
php artisan mail:send 1 2
```

`*`는 선택적인 인수와 결합하여 0개 이상의 인수를 받을 수 있게 할 수도 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

다중 값을 받는 옵션은 각각 별도로 옵션 이름과 값을 넘겨야 합니다:

```php
'mail:send {--id=*}'
```

이 경우 다음과 같이 여러 개를 넘길 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수와 옵션에 설명을 추가하려면 콜론 `:`을 써서 이름과 설명을 구분합니다. 길어질 경우 여러 줄에 걸쳐 작성해도 됩니다:

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
### 누락된 입력 자동 프롬프트

필수 인수가 지정되지 않으면 기본적으로 오류 메시지를 출력합니다. 대신, `PromptsForMissingInput` 인터페이스를 구현하면 누락된 필수 인수를 자동으로 프롬프트할 수 있습니다:

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

Laravel은 인수명이나 설명을 참고해 스마트하게 질문을 만듭니다. 커스텀 질문을 사용하려면 `promptForMissingArgumentsUsing` 메서드를 구현해, 인수명 키와 질문값을 가진 배열을 반환하세요:

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

플레이스홀더 텍스트를 넣으려면 질문과 플레이스홀더를 배열 튜플로 반환할 수 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

질문을 완전히 커스터마이징하려면, 사용자에게 직접 프롬프트를 띄우고 정답을 반환하는 클로저도 사용할 수 있습니다:

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
> 더 많은 프롬프트 옵션과 사용법은 [Laravel Prompts](/docs/12.x/prompts) 문서를 참고하세요.

옵션에 대해서도 프롬프트를 띄우려면, 명령어의 `handle` 메서드 내에서 명령어 프롬프트 함수를 사용하거나, 자동 프롬프트가 실행된 후에만 프롬프트를 띄우려면 `afterPromptingForMissingArguments` 메서드를 구현하세요:

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
### 입력 가져오기

명령어 실행 중에 인수나 옵션 값을 얻으려면 `argument` 또는 `option` 메서드를 사용하세요. 존재하지 않는 인수나 옵션은 `null`을 반환합니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 받고 싶다면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션 또한 `option` 메서드로 가져올 수 있으며, 전체 옵션을 배열로 받으려면 `options` 메서드를 사용하세요:

```php
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 명령어 터미널 애플리케이션에 HTML 브라우저 같은 플레이스홀더, 유효성 검사 등 친숙한 폼 입력 기능을 추가하는 PHP 패키지입니다.

명령어 실행 중에 사용자 입력을 받을 수도 있습니다. `ask` 메서드는 질문을 출력하고 사용자의 입력을 받은 뒤 값을 반환합니다:

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

두 번째 인자로 기본값을 줄 수도 있습니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 유사하지만, 입력 내용이 터미널 화면에 표시되지 않아 비밀번호 같은 민감정보 입력에 유용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 질문 (Yes/No)

간단한 Yes/No 확인은 `confirm` 메서드를 사용하세요. 기본값은 `false`이지만, 사용자가 `y` 또는 `yes`를 입력하면 `true`가 반환됩니다:

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 `true`로 변경하려면, 두 번째 인자에 `true`를 넘기세요:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 자동 완성 기능을 제공합니다. 사용자는 힌트를 참고하되 어떤 답변도 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

두 번째 인자로 클로저를 넘기면, 사용자가 타이핑할 때마다 해당 입력을 인자로 받아 자동 완성 후보 리스트를 반환할 수 있습니다:

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

사전 정의된 선택지 중에 고르게 하려면 `choice` 메서드를 사용하세요. 기본 선택지는 세 번째 인자로 넘깁니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

선택 시도 횟수 제한과 다중 선택 허용 여부는 네 번째와 다섯 번째 인자로 지정할 수 있습니다:

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

콘솔로 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용하세요. 각 메서드는 상황에 맞는 ANSI 컬러 코드를 적용합니다. 예를 들어 `info`는 일반적으로 녹색 텍스트로 보여 줍니다:

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

오류 메시지는 `error` 메서드를 사용하며, 보통 빨간색으로 표시됩니다:

```php
$this->error('Something went wrong!');
```

색상이 없는 일반 텍스트는 `line` 메서드를 사용하세요:

```php
$this->line('Display this on the screen');
```

빈 줄을 추가하려면 `newLine` 메서드를 사용합니다:

```php
// 한 줄 빈 줄 출력...
$this->newLine();

// 세 줄 빈 줄 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드는 다중 행과 열 데이터를 화면에 보기 좋게 정렬해 출력합니다. 컬럼 이름과 데이터를 전달해 주세요. Laravel이 적절한 너비와 높이를 자동 계산합니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바

시간이 오래 걸리는 작업 시 진행 상황을 나타내는 진행 바를 출력할 수 있습니다. `withProgressBar` 메서드를 통해 반복 가능한(iterable) 대상 각 요소 처리 시 진행 상황을 자동으로 갱신합니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

수동으로 진행 바를 제어하고 싶다면, 전체 작업 개수를 지정해 진행 바를 만들고, 요소별로 `advance`를 호출하세요:

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
> 심화된 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

Laravel은 기본적으로 `app/Console/Commands` 디렉터리 내 모든 명령어를 자동 등록합니다. 하지만 다른 디렉터리를 Artisan이 스캔하도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일 내 `withCommands` 메서드에 디렉터리 경로를 지정하세요:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면 명령어 클래스 이름을 직접 전달해 수동 등록도 가능합니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅될 때, 모든 등록된 명령어는 [서비스 컨테이너](/docs/12.x/container)를 통해 인스턴스화되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그래밍 방식으로 명령어 실행하기

가끔 CLI가 아닌 다른 곳에서 Artisan 명령어를 실행하고 싶을 때가 있습니다. 예를 들어, 라우트나 컨트롤러에서 명령어를 실행할 수 있습니다. 이때 `Artisan` 파사드의 `call` 메서드를 사용합니다. 첫 번째 인자로 명령어 시그니처나 클래스명을 받고, 두 번째 인자로 인수와 옵션 배열을 받으며, 종료 코드를 반환합니다:

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

문자열 전체를 명령어로 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

명령어 옵션 중 배열로 입력을 받는 경우, 배열 형태로 옵션 값을 넘길 수 있습니다:

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

`migrate:refresh` 명령어의 `--force` 플래그 같은 값이 없는 옵션에 대해 `true` 또는 `false`를 넘겨야 할 경우가 있습니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉하기

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 넣어 백그라운드로 처리할 수 있습니다. 이 기능을 사용하려면 큐 설정 및 큐 리스너가 동작 중이어야 합니다:

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

`onConnection` 및 `onQueue` 메서드로 Artisan 명령어를 디스패치할 연결과 큐를 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 내에서 다른 명령 호출하기

기존 Artisan 명령어 내에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용하세요. `call` 메서드는 호출할 명령어 이름과 인수/옵션 배열을 받습니다:

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

다른 명령어 출력을 숨기고 조용히 호출하려면 `callSilently` 메서드를 사용하세요. 서명과 인자는 `call`과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예컨대 `SIGTERM` 시그널은 프로그램에 종료를 요청합니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하고 처리하고 싶으면 `trap` 메서드를 사용하세요:

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

여러 시그널을 한 번에 감지하려면 `trap` 메서드에 배열로 전달할 수 있습니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan의 `make` 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 이들 클래스는 사용자의 입력에 따라 값을 채우는 "스텁(stub)" 파일을 기반으로 생성됩니다. Artisan이 생성하는 파일에 약간의 수정이 필요하다면 `stub:publish` 명령어로 자주 사용하는 스텁을 애플리케이션으로 게시해 커스터마이징할 수 있습니다:

```shell
php artisan stub:publish
```

게시된 스텁은 애플리케이션 루트의 `stubs` 디렉터리에 위치하며, 이 파일에 변경을 가하면 Artisan의 `make` 명령어 실행 시 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 과정에서 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, 그리고 `Illuminate\Console\Events\CommandFinished`.  
- `ArtisanStarting` 이벤트는 Artisan이 실행되자마자 발생합니다.  
- `CommandStarting` 이벤트는 명령어 실행 직전에 발생합니다.  
- `CommandFinished` 이벤트는 명령어 실행이 끝난 후 발생합니다.