# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [고립 실행 가능 명령어](#isolatable-commands)
- [입력 기대값 정의하기](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
- [명령어 입출력](#command-io)
    - [입력 값 가져오기](#retrieving-input)
    - [입력 요청하기](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [프로그래밍적 명령어 실행](#programmatically-executing-commands)
    - [명령어 간 호출](#calling-commands-from-other-commands)
- [신호 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 기본 포함된 커맨드 라인 인터페이스(CLI)입니다. Artisan은 애플리케이션 루트에 위치한 `artisan` 스크립트이며, 애플리케이션을 개발하는 동안 도움이 되는 여러 유용한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

모든 명령어에는 해당 명령어에 사용할 수 있는 인수와 옵션을 보여주고 설명하는 "도움말" 화면도 포함되어 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행합니다:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/9.x/sail)을 사용하는 경우, Artisan 명령어를 호출할 때 `sail` 커맨드 라인을 이용하는 것을 잊지 마세요. Sail은 애플리케이션의 도커 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지로 동작하는 강력한 Laravel용 REPL입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만 애플리케이션에서 제거한 경우, Composer를 통해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 수 있는 그래픽 UI를 찾고 있나요? [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker는 Eloquent 모델, 작업(jobs), 이벤트 등 애플리케이션 전체와 커맨드 라인에서 상호작용할 수 있게 해줍니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

`vendor:publish` 명령어를 사용해 Tinker 설정 파일을 공개할 수도 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수 및 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣을 때 가비지 컬렉션에 의존합니다. 따라서 tinker 사용 시에는 `Bus::dispatch` 또는 `Queue::push`를 이용해 작업을 디스패치하는 것이 안전합니다.

<a name="command-allow-list"></a>
#### 실행 허용 명령어 목록

Tinker 쉘에서는 실행할 수 있는 Artisan 명령어를 "허용(allow)" 목록으로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일 내의 `commands` 배열에 추가할 수 있습니다:

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭이 생성되지 않을 클래스

Tinker는 기본적으로 명령어 내에서 사용하는 클래스에 자동으로 별칭(alias)을 붙입니다. 하지만 일부 클래스는 별칭이 생성되지 않도록 설정할 수도 있습니다. `tinker.php` 설정 파일 내의 `dont_alias` 배열에 해당 클래스를 적으면 됩니다:

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan이 기본 제공하는 명령어 외에도 직접 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉토리에 저장하지만, Composer가 로드할 수 있다면 원하는 곳에 자유롭게 저장할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉토리에 명령어 클래스를 생성합니다. 만약 해당 디렉토리가 없다면 처음 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후, 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 값들은 `list` 화면에서 커맨드를 표시할 때 사용됩니다. `signature`는 [명령어 입력 기대값](#defining-input-expectations)을 정의할 때도 쓰입니다. 명령어 실행 시에는 `handle` 메서드가 호출되며, 여기에 로직을 작성하면 됩니다.

예시 명령어를 살펴보겠습니다. 이 메서드에서는 필요한 의존성을 메서드 시그니처에서 타입힌팅하여 주입받는 모습도 볼 수 있습니다. Laravel의 [서비스 컨테이너](/docs/9.x/container)가 자동으로 의존성을 주입해줍니다.

```
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
     *
     * @param  \App\Support\DripEmailer  $drip
     * @return mixed
     */
    public function handle(DripEmailer $drip)
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 명령어 클래스는 너무 무겁지 않게 유지하고, 실제 작업 수행은 애플리케이션 서비스에 위임하는 것이 코드 재사용성과 유지보수에 좋습니다. 위 예시에서는 이메일 전송이라는 핵심 작업을 서비스 클래스로 분리하여 주입받은 점을 참고하세요.

<a name="closure-commands"></a>
### 클로저 명령어

클로저(Closure) 기반 명령어는 클래스 정의 대신 함수를 이용하는 대안입니다. 라우트의 클로저가 컨트롤러 대안인 것처럼, 명령어 클로저도 클래스 명령어 대체 수단이라 생각하면 됩니다. `app/Console/Kernel.php` 내부의 `commands` 메서드에서는 `routes/console.php` 파일을 로드합니다:

```
/**
 * Register the closure based commands for the application.
 *
 * @return void
 */
protected function commands()
{
    require base_path('routes/console.php');
}
```

`routes/console.php`에는 HTTP 라우트가 정의되지 않고, Artisan 콘솔 명령어 진입점이 정의됩니다. 여기서 `Artisan::command` 메서드를 통해 클로저 명령어를 등록할 수 있습니다. `command` 메서드는 두 인수를 받는데, 첫 번째는 [명령어 시그니처](#defining-input-expectations), 두 번째는 명령어 인수와 옵션을 전달받는 클로저입니다:

```
Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 내부적으로 명령어 인스턴스에 바인딩되므로, 클래스 명령어에서 사용할 수 있는 헬퍼 메서드들을 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

명령어 인수와 옵션뿐만 아니라 추가 의존성도 [서비스 컨테이너](/docs/9.x/container)에서 타입힌팅을 통해 주입받을 수 있습니다:

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명 지정

클로저 명령어를 정의할 때 `purpose` 메서드를 이용해 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 실행 시 표시됩니다:

```
Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### 고립 실행 가능 명령어 (Isolatable Commands)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

때때로 하나의 명령어 인스턴스만 동시에 실행되도록 보장하고 싶을 때가 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다:

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

`Isolatable`로 표시된 명령어에는 자동으로 `--isolated` 옵션이 추가됩니다. 이 옵션과 함께 명령어가 실행되면, Laravel은 기본 캐시 드라이버를 이용해 원자적 잠금(락)을 시도합니다. 만약 이미 같은 명령어 인스턴스가 실행 중이라면 새로운 실행은 중단되고, 명령어는 성공 상태 코드와 함께 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

만약 잠금이 해제되지 않아 명령어를 실행할 수 없을 때 반환할 종료 상태 코드를 직접 지정하고 싶다면, `--isolated` 옵션에 숫자값을 지정할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-expiration-time"></a>
#### 잠금 만료 시간 설정

기본적으로 잠금은 명령어가 완료되면 만료되거나, 명령어가 중단되어 완료할 수 없을 경우 1시간 후 만료됩니다. 이 동작은 명령어 클래스 내에 `isolationLockExpiresAt` 메서드를 정의하여 조정할 수 있습니다:

```php
/**
 * 고립 실행 잠금 만료 시점을 결정합니다.
 *
 * @return \DateTimeInterface|\DateInterval
 */
public function isolationLockExpiresAt()
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대값 정의하기

콘솔 명령어를 작성할 때, 종종 사용자로부터 인수나 옵션을 통해 입력을 받습니다. Laravel은 명령어 클래스의 `signature` 속성을 사용해 예상 입력을 편리하게 정의할 수 있게 해줍니다. `signature`는 명령어 이름, 인수, 옵션을 하나의 표현력 강한 라우트 형태 문법으로 정의하는 데 사용됩니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자가 제공하는 모든 인수와 옵션은 중괄호 `{}`로 감싸 집니다. 다음 예제는 필수 인수 `user`를 정의합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택 사항으로 만들거나 기본값도 정의할 수 있습니다:

```
// 선택적 인수...
'mail:send {user?}'

// 기본값이 있는 선택적 인수...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션(Options)

옵션은 인수와 유사한 형태의 사용자 입력입니다. 명령어에서 옵션은 커맨드 라인에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션은 값을 받는 경우와 받지 않는 경우 두 가지 유형이 있습니다. 값이 없는 옵션은 Boolean 스위치로 작동합니다. 다음 예시는 값 없는 옵션의 예입니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시의 `--queue` 옵션은 커맨드 실행 시 지정할 수 있습니다. 만약 `--queue`가 전달됐다면 값은 `true`가 되며, 전달되지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

값이 반드시 주어져야 하는 옵션은 옵션 이름 뒤에 `=`를 붙여 표시합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 커맨드 실행 시 사용자가 옵션 값을 꼭 지정해야 하며, 지정하지 않을 경우 옵션의 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

기본 옵션값을 지정할 수도 있습니다. 사용자가 별도로 옵션 값을 지정하지 않으면 기본값이 적용됩니다:

```
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키 지정

옵션에 단축키를 부여하려면 전체 옵션 이름 앞에 단축키를 지정하고 `|` 문자로 구분합니다:

```
'mail:send {user} {--Q|queue}'
```

터미널에서 명령어 실행 시 단축키는 하이픈 하나(`-`)만 붙여 사용합니다:

```shell
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a>
### 입력 배열

하나 이상의 값을 받는 인수나 옵션을 정의하려면 `*`를 사용할 수 있습니다. 아래는 인수의 예입니다:

```
'mail:send {user*}'
```

이 경우 각 `user` 인수를 순서대로 커맨드 라인에 전달할 수 있습니다. 예를 들어, 다음 명령은 `user` 값을 `[1, 2]` 배열로 설정합니다:

```shell
php artisan mail:send 1 2
```

`*`와 선택형 인수도 같이 사용할 수 있어, 0개 이상의 인수를 받을 수도 있습니다:

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

값이 여러 개인 옵션을 정의할 때는 각 값마다 옵션 이름을 접두어로 붙여야 합니다:

```
'mail:send {--id=*}'
```

이 명령어는 다음과 같이 여러 번 옵션을 지정할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수나 옵션에 설명을 달아줄 수 있습니다. 인수명 뒤에 콜론(`:`)을 붙이고 설명 내용을 작성합니다. 여러 줄로도 나눠 쓸 수 있습니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="command-io"></a>
## 명령어 입출력

<a name="retrieving-input"></a>
### 입력 값 가져오기

명령어 실행 중에는 입력된 인수와 옵션 값을 얻어와야 할 경우가 많습니다. 이런 경우 `argument`와 `option` 메서드를 사용하세요. 존재하지 않는 인수나 옵션을 요청하면 `null`을 반환합니다:

```
/**
 * Execute the console command.
 *
 * @return int
 */
public function handle()
{
    $userId = $this->argument('user');

    //
}
```

모든 인수를 배열로 가져오려면 `arguments` 메서드를 사용하세요:

```
$arguments = $this->arguments();
```

옵션도 위와 같은 방식으로 `option` 메서드로 특정 옵션을, `options` 메서드로 전체 옵션을 배열로 받을 수 있습니다:

```
// 특정 옵션 가져오기...
$queueName = $this->option('queue');

// 모든 옵션 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 요청하기

출력을 표시하는 것 외에도 명령어 실행 중 사용자에게 입력을 받을 수 있습니다. `ask` 메서드는 질문을 출력하고, 사용자가 입력한 값을 받아 명령어로 반환합니다:

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $name = $this->ask('What is your name?');
}
```

`secret` 메서드는 `ask`와 같지만 사용자가 입력하는 내용이 콘솔에 표시되지 않는 점이 다릅니다. 비밀번호 같은 민감한 정보를 입력받을 때 유용합니다:

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청하기

간단한 "예/아니오" 확인이 필요할 때는 `confirm` 메서드를 사용하세요. 기본값은 `false`이며, 사용자가 `y` 또는 `yes`를 입력하면 `true`가 반환됩니다:

```
if ($this->confirm('Do you wish to continue?')) {
    //
}
```

두 번째 인수에 `true`를 넘기면 기본값이 `true`가 됩니다:

```
if ($this->confirm('Do you wish to continue?', true)) {
    //
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 자동 완성 기능을 제공합니다. 사용자가 입력하는 동안 힌트가 표시되지만, 사용자는 자유롭게 입력할 수 있습니다:

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

두 번째 인수로 클로저를 넘겨서 사용자 입력에 따라 자동 완성 후보를 동적으로 제공할 수도 있습니다:

```
$name = $this->anticipate('What is your address?', function ($input) {
    // 자동 완성 후보 반환...
});
```

<a name="multiple-choice-questions"></a>
#### 선택형 질문

선택지 배열을 미리 제공하고, 사용자가 그 중 선택하게 할 수 있습니다. 세 번째 인수로 기본값 인덱스를 지정할 수 있습니다:

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째, 다섯 번째 인수로 최대 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

```
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

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용할 수 있습니다. 각각 ANSI 색상을 적절히 적용하여 정보를 전달합니다. 예를 들어 일반 정보 메시지는 `info` 메서드를 쓰면 보통 초록색으로 표시됩니다:

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    // ...

    $this->info('The command was successful!');
}
```

오류 메시지를 표시할 때는 `error` 메서드를 사용하며, 보통 빨간색으로 표시됩니다:

```
$this->error('Something went wrong!');
```

색상 없는 일반 텍스트는 `line` 메서드로 출력할 수 있습니다:

```
$this->line('Display this on the screen');
```

빈 줄은 `newLine` 메서드를 사용합니다:

```
// 빈 줄 한 줄 출력...
$this->newLine();

// 빈 줄 세 줄 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드는 여러 행과 열을 잘 정리하여 출력할 수 있게 도와줍니다. 컬럼 이름과 데이터를 배열로 넘기면 Laravel이 적절한 크기를 계산해 테이블을 출력합니다:

```
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄

오래 걸리는 작업에 대해 진행 정도를 알려줄 때 진행률 표시줄이 유용합니다. `withProgressBar` 메서드는 이터러블을 순회하며 자동으로 진행 상태를 보여줍니다:

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
```

직접 진행률 표시줄을 만들고 컨트롤할 수도 있습니다. 전체 업무 개수를 지정하고, 작업 완료 후마다 진행률을 갱신합니다:

```
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
> 더욱 자세한 기능은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

모든 콘솔 명령어는 애플리케이션의 `App\Console\Kernel` 클래스에 등록됩니다. 이 "콘솔 커널"의 `commands` 메서드 내에서는 `load` 메서드를 호출하여 `app/Console/Commands` 디렉토리를 스캔하고, 그 안의 모든 명령어 클래스를 자동 등록합니다. 추가 디렉토리도 자유롭게 스캔하도록 `load`를 호출할 수 있습니다:

```
/**
 * Register the commands for the application.
 *
 * @return void
 */
protected function commands()
{
    $this->load(__DIR__.'/Commands');
    $this->load(__DIR__.'/../Domain/Orders/Commands');

    // ...
}
```

필요하다면 `App\Console\Kernel` 클래스 내 `$commands` 속성에 명령어 클래스들을 직접 추가하여 수동으로도 등록할 수 있습니다. 이 속성이 없다면 직접 정의해주면 됩니다. Artisan 부팅 시 해당 속성 내 명령어가 서비스 컨테이너를 통해 자동 등록됩니다:

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
## 프로그래밍적 명령어 실행

가끔 CLI 외부에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 예를 들어 라우트나 컨트롤러에서 명령어를 실행하는 경우입니다. 이때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. 첫 번째 인수로 명령어 시그니처 또는 클래스명, 두 번째 인수로 명령어 매개변수를 배열로 넘깁니다. 종료 코드를 반환합니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

명령어 전체를 문자열로 넘길 수도 있습니다:

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

배열 값을 받는 옵션이 있다면 배열로 전달할 수 있습니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달하기

`migrate:refresh` 명령어의 `--force` 플래그처럼 문자열 값을 받지 않는 옵션 일 경우, 불리언 값 `true` 또는 `false`를 전달해야 합니다:

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉하기

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 백그라운드 큐 작업으로 처리할 수 있습니다. 큐를 구성하고 리스너가 실행 중이어야 사용 가능합니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

`onConnection`과 `onQueue` 메서드를 체이닝하여 연결과 큐를 지정할 수 있습니다:

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 내에서 다른 명령어 호출하기

기존 Artisan 명령어 내에서 다른 명령어를 호출하고 싶을 수 있습니다. `call` 메서드를 사용하며, 첫 번째는 호출할 명령어 이름, 두 번째는 인수/옵션 배열입니다:

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    //
}
```

다른 명령어를 호출하면서 출력을 숨기고 싶으면 `callSilently` 메서드를 사용하세요. 서명은 `call`과 동일합니다:

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 신호 처리

운영체제는 실행 중인 프로세스에 신호를 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로세스에 종료 요청을 할 때 사용합니다. Artisan 명령어 내에서 이런 신호를 감지하고 처리하려면 `trap` 메서드를 사용할 수 있습니다:

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 신호를 동시에 감지하려면 `trap` 메서드에 배열로 신호를 전달하세요:

```
$this->trap([SIGTERM, SIGQUIT], function ($signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan `make` 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이때 "stub" 파일을 사용하며, 이는 기본 틀이 되는 파일로 입력값에 따라 내용을 채워 생성됩니다. 생성된 파일 내용을 조금 수정하고 싶을 때는 `stub:publish` 명령어로 애플리케이션 내로 스텁을 공개하여 직접 커스터마이징할 수 있습니다:

```shell
php artisan stub:publish
```

공개된 스텁은 애플리케이션 루트의 `stubs` 디렉토리에 위치하며, 수정 사항은 Artisan `make` 명령어로 클래스 생성 시 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 다음 세 가지 이벤트를 발생시킵니다: 
- `Illuminate\Console\Events\ArtisanStarting`: Artisan 실행 직후 발생
- `Illuminate\Console\Events\CommandStarting`: 명령어 실행 직전 발생
- `Illuminate\Console\Events\CommandFinished`: 명령어 종료 후 발생

이벤트를 활용해 명령어 실행 흐름에 맞는 추가 작업을 구현할 수 있습니다.