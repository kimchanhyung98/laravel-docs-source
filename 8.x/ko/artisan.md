# Artisan 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
- [입력 기대값 정의](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
- [명령어 I/O](#command-io)
    - [입력값 받아오기](#retrieving-input)
    - [입력 요청하기](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령어 등록](#registering-commands)
- [명령어의 프로그래밍적 실행](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 핸들링](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 유용한 다양한 명령어를 제공합니다. 모든 사용 가능한 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다:

    php artisan list

각 명령어에는 사용 가능한 인수와 옵션을 표시하고 설명하는 "도움말" 화면도 포함되어 있습니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙이면 됩니다:

    php artisan help migrate

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/{{version}}/sail)을 로컬 개발 환경으로 사용하는 경우, Artisan 명령어를 실행할 때 반드시 `sail` 커맨드라인을 사용해야 합니다. Sail은 귀하의 애플리케이션 Docker 컨테이너 안에서 Artisan 명령어를 실행합니다:

    ./sail artisan list

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동되는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 다만, 기존 애플리케이션에서 Tinker를 제거한 경우 Composer를 통해 다시 설치할 수 있습니다:

    composer require laravel/tinker

> {tip} Laravel 애플리케이션과 상호작용을 위한 GUI가 필요하신가요? [Tinkerwell](https://tinkerwell.app)을 확인해보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 Eloquent 모델, 작업(Job), 이벤트 등 Laravel 애플리케이션 전체와 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요:

    php artisan tinker

Tinker의 설정 파일을 `vendor:publish` 명령어로 배포할 수도 있습니다:

    php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"

> {note} `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 가비지 컬렉션을 통해 작업을 큐에 올리므로, tinker 환경에서는 작업을 디스패치할 때 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 명령어 허용 목록

Tinker는 "허용" 목록을 사용해 쉘 내에서 실행 가능한 Artisan 명령어를 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어만 실행할 수 있습니다. 추가로 허용하고 싶은 명령어가 있다면, `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a>
#### Alias되지 않아야 할 클래스

일반적으로 Tinker는 상호작용하는 클래스를 자동으로 별칭(alias) 처리합니다. 하지만, 특정 클래스는 절대 별칭되지 않도록 할 수도 있습니다. 이를 위해 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 기입하면 됩니다:

    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>
## 명령어 작성

Artisan에 기본 제공되는 명령어 외에도, 직접 커스텀 명령어를 작성할 수 있습니다. 명령어는 일반적으로 `app/Console/Commands` 디렉터리에 보관되지만, Composer로 로드 가능한 위치라면 자유롭게 저장할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 만들려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 생성합니다. 해당 디렉터리가 없더라도 걱정하지 마세요. 명령어를 처음 실행할 때 자동으로 생성됩니다:

    php artisan make:command SendEmails

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후, 해당 클래스의 `signature`와 `description` 속성에 적절한 값을 정의해야 합니다. 이 속성들은 `list` 화면에서 명령어를 표시할 때 사용되며, `signature`에서는 [입력 값에 대한 기대값](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 여기에 명령어의 로직을 두면 됩니다.

아래는 예시 명령어입니다. `handle` 메서드를 통해 필요한 의존성을 요청할 수 있으며, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 타입힌트된 의존성을 자동으로 주입해줍니다:

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
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

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

> {tip} 코드 재사용성을 높이기 위해, 콘솔 명령어는 가볍게 유지하고 실제 비즈니스 로직은 서비스 클래스에 위임하는 것이 좋습니다. 위 예제에서는 이메일 전송의 핵심 처리를 서비스 클래스에 맡기고 있습니다.

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 클래스로 명령어를 정의하는 대신 사용할 수 있는 대안입니다. 라우트에서 클로저를 사용하는 것처럼, 명령어 클로저도 명령어 클래스를 대체할 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드에서는 Laravel이 `routes/console.php` 파일을 불러옵니다:

```php
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

이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션을 향한 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용하여 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어의 시그니처](#defining-input-expectations)와, 인수와 옵션을 전달받는 클로저를 인수로 받습니다:

```php
Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 해당 명령어 인스턴스에 바인딩되므로, 일반 명령어 클래스에서 접근할 수 있는 모든 헬퍼 메서드를 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 명령어에도 인수와 옵션 외에 [서비스 컨테이너](/docs/{{version}}/container)에서 해결할 의존성을 타입힌트로 지정할 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용해 명령어 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help`를 실행할 때 표시됩니다:

```php
Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="defining-input-expectations"></a>
## 입력 기대값 정의

콘솔 명령어를 작성할 때는 사용자로부터 인수(argument)나 옵션(option)을 통해 입력을 받는 것이 일반적입니다. Laravel은 명령어의 `signature` 속성을 사용해 명확하고 편리하게 입력 기대값을 정의할 수 있게 해줍니다. 이 속성에서는 명령어 이름, 인수 및 옵션을 하나의 라우트 같은 직관적인 문법으로 지정할 수 있습니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자가 제공할 인수와 옵션은 모두 중괄호로 감쌉니다. 다음 예제에서 `user` 인수는 필수입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택적 인수...
mail:send {user?}

// 기본값이 있는 선택적 인수...
mail:send {user=foo}
```

<a name="options"></a>
### 옵션(Options)

옵션 역시 사용자 입력의 한 형태입니다. 옵션은 커맨드라인에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값을 받는 것과 받지 않는 두 가지 유형이 있으며, 값을 받지 않는 옵션은 불리언 "스위치"로 동작합니다. 예제를 살펴보겠습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예제에서 `--queue` 스위치는 Artisan 명령어 호출 시 지정할 수 있습니다. 스위치가 지정되면 해당 옵션의 값은 `true`, 지정하지 않으면 `false`가 됩니다:

    php artisan mail:send 1 --queue

<a name="options-with-values"></a>
#### 값이 있는 옵션

값을 기대하는 옵션의 경우, 옵션명 뒤에 `=` 기호를 붙여야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

명령어 호출 시 다음과 같이 값도 전달할 수 있으며, 옵션을 지정하지 않으면 값은 `null`이 됩니다:

    php artisan mail:send 1 --queue=default

옵션에 기본값을 지정하려면 옵션명 뒤에 기본값을 붙이면 됩니다:

    mail:send {user} {--queue=default}

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 할당할 수도 있습니다. 단축키는 옵션명 앞에 지정하고, `|` 문자로 전체 옵션명과 구분합니다:

    mail:send {user} {--Q|queue}

터미널에서 실행할 때는 단축키 앞에 한 개의 하이픈을 붙여주세요:

    php artisan mail:send 1 -Q

<a name="input-arrays"></a>
### 입력 배열

여러 개의 인수나 옵션 값을 받을 필요가 있다면, `*` 문자를 사용할 수 있습니다. 예를 들어 다음과 같이 지정할 수 있습니다:

    mail:send {user*}

다음과 같이 호출하면 `user`는 `foo`, `bar`의 값을 가진 배열이 됩니다:

    php artisan mail:send foo bar

선택적 인수와 조합하여 0개 이상의 인수를 허용할 수도 있습니다:

    mail:send {user?*}

<a name="option-arrays"></a>
#### 옵션 배열

여러 값을 기대하는 옵션을 정의할 때에는, 각 옵션 값 앞에 옵션명을 붙여야 합니다:

    mail:send {user} {--id=*}

    php artisan mail:send --id=1 --id=2

<a name="input-descriptions"></a>
### 입력 설명

인수나 옵션에 대한 설명을 추가하려면, 인수/옵션명 뒤에 콜론(`:`)과 설명을 붙이면 됩니다. 명령어 시그니처가 길어질 경우 여러 줄에 걸쳐도 괜찮습니다:

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

<a name="command-io"></a>
## 명령어 I/O

<a name="retrieving-input"></a>
### 입력 받아오기

명령어 실행 중, 명령어에서 허용한 인수와 옵션 값을 사용해야 할 때가 많습니다. 이때 `argument`와 `option` 메서드를 사용할 수 있습니다. 인수나 옵션이 존재하지 않을 경우 `null`이 반환됩니다:

```php
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

모든 인수를 `array` 형태로 받아오려면 `arguments` 메서드를 사용합니다:

    $arguments = $this->arguments();

옵션도 똑같이 싱글 값은 `option`, 전체는 `options`로 받아올 수 있습니다:

    // 특정 옵션 값만 받아오기...
    $queueName = $this->option('queue');

    // 전체 옵션을 배열로 받아오기...
    $options = $this->options();

<a name="prompting-for-input"></a>
### 입력 요청하기

명령어에서 출력을 보여주는 것뿐 아니라, 실행 중 사용자 입력을 요구할 수도 있습니다. `ask` 메서드는 사용자가 입력한 값을 명령어로 받아옵니다:

```php
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

`secret` 메서드는 `ask`와 유사하지만, 사용자의 입력이 콘솔에 표시되지 않습니다. 패스워드 등 민감한 정보 입력에 유용합니다:

    $password = $this->secret('What is the password?');

<a name="asking-for-confirmation"></a>
#### 확인 요청(yes/no)

단순한 "예/아니오" 확인이 필요하다면 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 이 메서드는 `false`를 반환하지만, 사용자가 프롬프트에 `y`나 `yes`를 입력하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    //
}
```

기본값을 `true`로 하고 싶다면 두 번째 인자로 `true`를 전달하세요:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    //
}
```

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드는 미리 지정된 선택지로 자동완성을 제공합니다. 사용자는 자동완성 힌트와 다른 값도 입력할 수 있습니다:

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

또한, 두 번째 인자로 클로저를 넘겨 동적으로 자동완성 목록을 반환할 수도 있습니다:

    $name = $this->anticipate('What is your address?', function ($input) {
        // 자동완성 옵션 반환...
    });

<a name="multiple-choice-questions"></a>
#### 다중 선택 질문

사용자에게 미리 정해진 답변 목록 중에서 고르게 하고 싶다면 `choice` 메서드를 사용할 수 있습니다. 옵션을 선택하지 않을 경우 반환되는 기본값의 인덱스는 세 번째 인자입니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한, 네 번째와 다섯 번째 인자로 유효한 응답 선택 시 최대 시도 횟수와 다중 선택 허용 여부를 지정할 수 있습니다:

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

콘솔에 출력을 보내려면 `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 이 메서드들은 각각 목적에 맞는 ANSI 색상을 사용합니다. 예를 들어 `info`는 일반적으로 녹색 텍스트로 출력됩니다:

```php
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

오류 메시지를 출력하려면 `error` 메서드를 사용하세요. 보통 빨간색으로 표시됩니다:

    $this->error('Something went wrong!');

일반 텍스트는 `line` 메서드로 출력합니다:

    $this->line('Display this on the screen');

빈 줄을 추가하려면 `newLine` 메서드를 사용하세요:

    // 빈 줄 한 개 추가...
    $this->newLine();

    // 빈 줄 세 개 추가...
    $this->newLine(3);

<a name="tables"></a>
#### 테이블

`table` 메서드를 사용하면 여러 행/열 데이터를 고르게 정렬해 출력할 수 있습니다. 컬럼명과 데이터만 넘기면 Laravel이 자동으로 폭과 높이를 맞추어 출력합니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄

오래 걸리는 작업의 경우, 처리 진행 상황을 보여주면 사용자가 기다리기 편합니다. `withProgressBar` 메서드를 사용하면 반복 처리시 자동으로 진행률 바가 표시됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
```

더 세밀하게 진행률 바를 제어하려면, 처리할 단계 개수를 정하고 각 항목 처리 후 직접 진행률을 올릴 수 있습니다:

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

> {tip} 더 많은 고급 기능은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

모든 콘솔 명령어는 애플리케이션의 `App\Console\Kernel` 클래스(콘솔 커널)에 등록됩니다. 이 클래스의 `commands` 메서드에서 커널의 `load` 메서드가 호출되는 것을 볼 수 있습니다. `load` 메서드는 `app/Console/Commands` 디렉터리를 스캔해 그 안의 모든 명령어를 Artisan에 자동 등록합니다. 필요하다면 다른 디렉터리도 추가로 스캔할 수 있습니다:

```php
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

필요하다면 명령어의 클래스명을 `App\Console\Kernel` 클래스 내 `$commands` 속성에 수동으로 추가해 직접 등록할 수도 있습니다. 이 속성이 커널에 정의되어 있지 않다면 직접 추가하세요. Artisan이 부팅될 때, 여기에 지정된 클래스를 [서비스 컨테이너](/docs/{{version}}/container)로 해결해서 Artisan에 등록합니다:

```php
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
## 프로그래밍적으로 명령어 실행

때로는 CLI 외부에서 Artisan 명령어를 실행해야 할 때가 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령어를 실행할 수도 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용하세요. 이 메서드는 명령어 시그니처명 또는 클래스명을 첫 번째 인자로, 명령어 파라미터 배열을 두 번째 인자로 받고, 종료 코드를 반환합니다:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

명령어 전체를 문자열로 넘길 수도 있습니다:

    Artisan::call('mail:send 1 --queue=default');

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어 옵션이 배열을 받는다면, 배열 형태로 값을 전달할 수 있습니다:

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

문자열 값을 받지 않는 옵션(예: `migrate:refresh`의 `--force`)에 값을 지정하려면 `true`나 `false`를 전달하세요:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐 처리

`Artisan` 파사드의 `queue` 메서드를 사용하면, Artisan 명령어를 [큐 워커](/docs/{{version}}/queues)가 백그라운드에서 처리하도록 보낼 수도 있습니다. 이를 사용하기 전에 큐가 설정되어 있고, 큐 리스너가 실행 중인지 확인하세요:

```php
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

`onConnection`과 `onQueue` 메서드를 사용하면 별도의 연결이나 큐에 디스패치할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출

기존 Artisan 명령어 내에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 이름과 인수/옵션 배열을 인자로 받습니다:

```php
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

다른 콘솔 명령어를 호출하면서 출력을 모두 숨기고 싶다면 `callSilently` 메서드를 사용하세요. 이 메서드의 시그니처는 `call` 메서드와 같습니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 핸들링

Artisan 콘솔의 기반이 되는 Symfony Console 컴포넌트는 명령어가 처리할 프로세스 시그널(있다면)을 지정할 수 있게 해줍니다. 예를 들어, `SIGINT`와 `SIGTERM` 시그널을 처리하도록 명령어를 설정할 수 있습니다.

이를 위해서는 Artisan 명령 클래스에서 `Symfony\Component\Console\Command\SignalableCommandInterface` 인터페이스를 구현해야 합니다. 이 인터페이스는 `getSubscribedSignals`와 `handleSignal` 두 메서드를 정의해야 합니다:

```php
<?php

use Symfony\Component\Console\Command\SignalableCommandInterface;

class StartServer extends Command implements SignalableCommandInterface
{
    // ...

    /**
     * 명령어가 처리할 시그널 목록 반환
     *
     * @return array
     */
    public function getSubscribedSignals(): array
    {
        return [SIGINT, SIGTERM];
    }

    /**
     * 들어온 시그널 처리
     *
     * @param  int  $signal
     * @return void
     */
    public function handleSignal(int $signal): void
    {
        if ($signal === SIGINT) {
            $this->stopServer();

            return;
        }
    }
}
```

예상할 수 있듯이, `getSubscribedSignals`는 명령어가 처리할 시그널을 배열로 반환하고, `handleSignal`은 해당 시그널을 받아서 필요에 따라 동작합니다.

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan 콘솔의 `make` 명령어는 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 생성할 때 사용됩니다. 이러한 클래스들은 "스텁" 파일을 바탕으로 입력값에 따라 내용을 채워서 생성됩니다. Artisan이 생성하는 파일에 약간의 변경이 필요하다면, `stub:publish` 명령어로 애플리케이션에 가장 많이 쓰이는 스텁을 배포한 뒤, 이를 직접 수정할 수 있습니다:

    php artisan stub:publish

배포된 스텁들은 애플리케이션 루트의 `stubs` 디렉터리에 위치하게 됩니다. 이 스텁을 수정하면, Artisan의 `make` 명령어로 해당 클래스를 생성할 때 변경된 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan이 명령어를 실행할 때는 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
- `ArtisanStarting` 이벤트는 Artisan이 실행되자마자 발생합니다.  
- `CommandStarting` 이벤트는 명령어가 실행되기 바로 직전에 발생합니다.  
- 마지막으로 `CommandFinished` 이벤트는 명령어 실행이 끝났을 때 발생합니다.