# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [틴커(REPL)](#tinker)
- [명령어 작성하기](#writing-commands)
    - [명령어 생성하기](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
- [입력 기대치 정의하기](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
- [명령어 입출력](#command-io)
    - [입력 가져오기](#retrieving-input)
    - [입력 요청하기](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령어 등록하기](#registering-commands)
- [프로그램적으로 명령어 실행하기](#programmatically-executing-commands)
    - [다른 명령어에서 명령어 호출하기](#calling-commands-from-other-commands)
- [신호 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 커맨드 라인 인터페이스입니다. Artisan은 애플리케이션의 최상위에 `artisan` 스크립트로 존재하며, 애플리케이션 개발에 도움이 되는 다양한 명령어를 제공합니다. 사용 가능한 Artisan 명령어 목록을 보려면 `list` 명령어를 실행하세요:

```
php artisan list
```

각 명령어에는 명령어의 인수와 옵션을 설명하는 "help" 스크린이 포함되어 있습니다. 도움말을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요:

```
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/{{version}}/sail)을 사용하는 경우, Artisan 명령어를 실행할 때 반드시 `sail` 커맨드를 사용하세요. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```
./sail artisan list
```

<a name="tinker"></a>
### 틴커 (Tinker, REPL)

Laravel Tinker는 Laravel 프레임워크를 위한 강력한 대화형 REPL(Read-Eval-Print Loop)로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만 이전에 애플리케이션에서 제거했다면 Composer를 통해 다시 설치할 수 있습니다:

```
composer require laravel/tinker
```

> [!TIP]
> Laravel 애플리케이션과 상호작용할 수 있는 그래픽 UI를 원하시면 [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker는 Eloquent 모델, 작업(jobs), 이벤트 등을 포함해 애플리케이션 전체와 커맨드 라인에서 상호작용할 수 있게 해줍니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요:

```
php artisan tinker
```

`vendor:publish` 명령어로 Tinker의 설정 파일을 퍼블리시할 수 있습니다:

```
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!NOTE]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker 사용 시에는 `Bus::dispatch` 또는 `Queue::push`를 사용해 작업을 디스패치하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록

Tinker는 셸 내에서 실행할 수 있는 Artisan 명령어를 "허용" 리스트로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 별칭 처리 제외 클래스

기본적으로 Tinker는 상호작용하는 클래스에 대해 자동으로 별칭(alias)을 생성합니다. 그러나 특정 클래스에 대해 별칭 생성을 원하지 않을 경우, `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 나열하면 됩니다:

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성하기

Artisan이 제공하는 기본 명령어 외에, 직접 커스텀 명령어를 작성할 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 저장하지만, Composer가 불러올 수 있는 위치라면 자유롭게 저장소를 선택할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성하기

새 명령어를 생성하려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새로운 명령어 클래스를 생성합니다. 만약 이 디렉터리가 없다면, 최초 실행 시 자동으로 생성됩니다:

```
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는 `signature`와 `description` 속성에 적절한 값을 할당해야 합니다. 이 값들은 `list` 스크린에 명령어를 표시할 때 사용됩니다. `signature` 속성은 [명령어 입력 기대치](#defining-input-expectations)를 정의하는 데도 활용됩니다. 명령어 실행 시 `handle` 메서드가 호출되며, 여기서 명령어 로직을 작성합니다.

다음은 예제 명령어입니다. `handle` 메서드에서 필요한 의존성을 자동 주입하는 데 Laravel [서비스 컨테이너](/docs/{{version}}/container)가 활용됩니다:

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

> [!TIP]
> 코드 재사용과 유지보수를 위해서, 콘솔 명령어는 가능한 가볍게 유지하고 실제 처리는 애플리케이션 서비스에 위임하는 것이 좋은 습관입니다. 위 예제에서 마케팅 이메일 발송의 '무거운 작업'은 서비스 클래스가 담당하고 있습니다.

<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 콘솔 명령어를 클래스로 정의하는 대신 사용할 수 있는 대안입니다. 라우트 클로저가 컨트롤러를 대신하는 것과 유사하게 생각하시면 됩니다. `app/Console/Kernel.php` 파일의 `commands` 메서드에서 Laravel이 `routes/console.php` 파일을 불러옵니다:

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

이 파일은 HTTP 라우트를 정의하지는 않지만, 콘솔 명령어 진입점(라우트)을 정의합니다. 여기서 `Artisan::command` 메서드로 클로저 기반 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 클로저(인수 및 옵션을 받음)를 인수로 받습니다:

```
Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 기본 명령어 인스턴스에 바인딩되어 있어, 클래스 기반 명령어에서 접근 가능한 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌팅

명령어 인수와 옵션뿐 아니라, 클로저 명령어는 서비스 컨테이너에서 해결할 추가 의존성을 타입힌트 할 수도 있습니다:

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 명령어에 설명을 추가하려면 `purpose` 메서드를 사용하세요. 이 설명은 `php artisan list`나 `php artisan help` 명령어 실행 시 표시됩니다:

```
Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="defining-input-expectations"></a>
## 입력 기대치 정의하기

콘솔 명령어 작성 시, 보통 인수(arguments) 또는 옵션(options)을 통해 사용자로부터 입력을 받습니다. Laravel은 명령어 클래스의 `signature` 속성으로 입력 형태를 간결하고 직관적으로 정의할 수 있게 해줍니다. `signature`는 명령어 이름과 각 인수, 옵션을 하나의 라우트형 문법으로 표현합니다.

<a name="arguments"></a>
### 인수(Arguments)

사용자가 제공하는 모든 인수와 옵션은 중괄호 `{}`로 감싸야 합니다. 예를 들어, 다음 명령어는 하나의 필수 인수 `user`를 정의합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택 사항(optional)으로 만들거나 기본값을 지정할 수도 있습니다:

```
// 선택적 인수...
mail:send {user?}

// 기본값이 있는 선택적 인수...
mail:send {user=foo}
```

<a name="options"></a>
### 옵션(Options)

옵션은 인수와 유사한 입력 형식이지만, 커맨드라인에서는 두 개의 하이픈(`--`)으로 시작합니다. 옵션은 값을 받을 수도 있고, 받지 않는 부울 스위치 형태일 수도 있습니다. 다음은 값을 받지 않는 옵션 예제입니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예제에서, `--queue` 옵션이 지정되면 값은 `true`가 되고, 지정하지 않으면 `false`가 됩니다:

```
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값을 받는 옵션

값이 필수인 옵션은 이름 뒤에 `=`를 붙여 정의합니다:

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

사용자는 다음처럼 옵션 값을 지정할 수 있습니다. 옵션이 명령어 호출 시 지정되지 않으면 값은 `null`이 됩니다:

```
php artisan mail:send 1 --queue=default
```

기본값을 지정하려면 기본값을 옵션 이름 뒤에 붙여 주세요. 옵션 값이 없으면 기본값이 사용됩니다:

```
mail:send {user} {--queue=default}
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 지정하려면, `|` 기호를 통해 이름 앞에 단축키를 적습니다:

```
mail:send {user} {--Q|queue}
```

커맨드라인 호출 시 단축키는 하나의 하이픈(`-`)을 붙여 사용합니다:

```
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a>
### 입력 배열

여러 값을 받는 인수나 옵션을 정의하려면 `*` 문자를 사용합니다. 예를 들어, 복수 `user` 인수를 정의하려면:

```
mail:send {user*}
```

명령어 호출 시 다음과 같이 여러 인수를 전달할 수 있습니다. 이 경우 `user` 인수는 `['foo', 'bar']` 배열이 됩니다:

```
php artisan mail:send foo bar
```

`*`는 선택적 인수와도 결합할 수 있어, 0개 이상의 인수를 받을 수 있습니다:

```
mail:send {user?*}
```

<a name="option-arrays"></a>
#### 옵션 배열

복수 값을 받는 옵션은 각각의 값을 옵션 이름과 함께 별도로 지정합니다:

```
mail:send {user} {--id=*}

php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수와 옵션에 설명을 달 수 있으며, 이름과 설명은 콜론(`:`)으로 구분합니다. 여러 줄에 걸쳐 정의할 수도 있습니다:

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
### 입력 가져오기

명령어 실행 중, 인수와 옵션의 값을 가져와야 할 때 `argument`와 `option` 메서드를 사용합니다. 존재하지 않는 인수나 옵션은 `null`을 반환합니다:

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

전체 인수를 배열로 받고 싶으면 `arguments` 메서드를 호출하세요:

```
$arguments = $this->arguments();
```

옵션도 인수와 같이 `option` 메서드로 단일 값을, `options` 메서드로 전체를 배열로 가져올 수 있습니다:

```
// 특정 옵션값 가져오기...
$queueName = $this->option('queue');

// 모든 옵션을 배열로 가져오기...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 요청하기

출력 이외에도, 명령어 실행 중 사용자에게 입력을 요청할 수 있습니다. `ask` 메서드는 질문을 콘솔에 출력하고, 사용자의 입력을 받아 반환합니다:

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

`secret` 메서드는 `ask`와 비슷하지만, 입력값이 콘솔에 표시되지 않아 비밀번호 같은 민감한 정보를 요청할 때 유용합니다:

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청하기

예/아니오 질문을 할 때 `confirm` 메서드를 사용합니다. 기본값은 `false`이고, 사용자가 `y` 또는 `yes`로 응답하면 `true`를 반환합니다:

```
if ($this->confirm('Do you wish to continue?')) {
    //
}
```

기본값을 `true`로 지정하려면 두 번째 인자로 `true`를 전달하세요:

```
if ($this->confirm('Do you wish to continue?', true)) {
    //
}
```

<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 메서드는 자동 완성 후보 값을 제시할 수 있습니다. 사용자는 자동 완성 외의 답변도 자유롭게 입력할 수 있습니다:

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

클로저를 두 번째 인자로 전달하여, 사용자가 입력할 때마다 실시간으로 후보를 제공하도록 할 수도 있습니다:

```
$name = $this->anticipate('What is your address?', function ($input) {
    // 자동 완성 후보 반환...
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택 질문

미리 정의된 선택지에서 사용자에게 골라야 할 때는 `choice` 메서드를 사용합니다. 기본 선택값 인덱스를 세 번째 인자로 지정할 수 있습니다:

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째와 다섯 번째 인자로 최대 재시도 횟수(`$maxAttempts`)와 다중 선택 허용 여부(`$allowMultipleSelections`)를 설정할 수도 있습니다:

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

콘솔에 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 메서드를 사용합니다. 각 메서드는 용도에 맞는 ANSI 색상을 적용합니다. 예를 들어, 일반 정보 출력은 `info` 메서드를 사용하며 일반적으로 초록색으로 표시됩니다:

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

오류 메시지는 `error` 메서드를 사용하며, 보통 빨간색으로 표시됩니다:

```
$this->error('Something went wrong!');
```

색상 없이 일반 텍스트를 출력하려면 `line` 메서드를 사용하세요:

```
$this->line('Display this on the screen');
```

빈 줄을 추가하려면 `newLine` 메서드를 호출합니다:

```
// 빈 줄 한 줄 출력...
$this->newLine();

// 빈 줄 세 줄 출력...
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드는 여러 행과 열의 데이터를 보기 좋게 정렬해 출력합니다. 컬럼명 배열과 데이터 배열만 전달하면, 자동으로 열 너비와 행 높이를 계산해 줍니다:

```
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바(Progress Bars)

작업이 오래 걸릴 때 진행 상황을 표시하는 데 유용합니다. `withProgressBar` 메서드는 주어진 반복자(iterable)를 반복하면서 진행 바를 자동으로 갱신합니다:

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
```

진행 바를 수동으로 제어하고 싶으면, 총 작업 단계를 먼저 정의한 후 작업 처리 후마다 진행 바를 갱신합니다:

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

> [!TIP]
> 더 많은 고급 옵션은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참조하세요.

<a name="registering-commands"></a>
## 명령어 등록하기

모든 콘솔 명령어는 애플리케이션의 "콘솔 커널"인 `App\Console\Kernel` 클래스에서 등록됩니다. 이 클래스의 `commands` 메서드 내에서 `load` 메서드를 호출해 `app/Console/Commands` 디렉터리 내 명령어들을 자동으로 불러와 Artisan에 등록합니다. 필요하면 다른 디렉터리도 추가로 등록할 수 있습니다:

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

수동으로 명령어를 등록하려면 `App\Console\Kernel` 클래스에 `$commands` 속성을 선언하고 클래스 이름을 나열하세요. 이 속성이 정의되지 않았으면 직접 추가하면 됩니다. Artisan이 부트될 때, 이 배열에 나열된 모든 명령어를 서비스 컨테이너에서 해석해 등록합니다:

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
## 프로그램적으로 명령어 실행하기

커맨드 라인 이외의 상황에서 Artisan 명령어를 실행하고 싶을 때가 있습니다. 예를 들어 라우트나 컨트롤러에서 명령어를 호출할 수 있습니다. 이때 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. 첫 번째 인자로 명령어 시그니처 또는 클래스 이름을, 두 번째 인자로 명령어 파라미터 배열을 넘기면 실행 후 종료 코드를 반환합니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

또는 명령어 문자열 전체를 인자로 넘길 수도 있습니다:

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달하기

명령어에 배열 옵션이 정의된 경우, 옵션에 배열 값을 넘길 수 있습니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 부울 값 전달하기

`migrate:refresh` 커맨드의 `--force` 플래그처럼, 문자열 외 값이 필요한 옵션은 `true` 또는 `false` 부울 값으로 전달하세요:

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐에 쌓기

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 넣어서 백그라운드에서 처리할 수 있습니다. 이 기능을 사용하려면 큐를 설정하고 큐 리스너가 실행 중이어야 합니다:

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

`onConnection`과 `onQueue` 메서드를 사용해 명령어를 디스패치할 연결과 큐도 지정할 수 있습니다:

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

때때로 기존 Artisan 명령어에서 다른 명령어를 호출하고 싶을 때가 있습니다. 이럴 때 `call` 메서드를 사용하면 됩니다. 첫 번째 인자로 호출할 명령어 이름, 두 번째 인자로 인수/옵션 배열을 넘기세요:

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

다른 명령어를 호출하면서 모든 출력을 숨기고 싶을 때는 `callSilently` 메서드를 사용하세요. 인자 구성은 `call`과 동일합니다:

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 신호 처리

Artisan 콘솔의 기반인 Symfony Console 컴포넌트는 명령어가 처리할 프로세스 신호를 지정할 수 있습니다. 예를 들어, `SIGINT`와 `SIGTERM` 신호를 처리하도록 명령어를 구성할 수 있습니다.

시작하려면 Artisan 명령어 클래스에서 `Symfony\Component\Console\Command\SignalableCommandInterface` 인터페이스를 구현해야 합니다. 이 인터페이스는 `getSubscribedSignals`와 `handleSignal` 두 메서드 구현을 요구합니다:

```php
<?php

use Symfony\Component\Console\Command\SignalableCommandInterface;

class StartServer extends Command implements SignalableCommandInterface
{
    // ...

    /**
     * Get the list of signals handled by the command.
     *
     * @return array
     */
    public function getSubscribedSignals(): array
    {
        return [SIGINT, SIGTERM];
    }

    /**
     * Handle an incoming signal.
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

`getSubscribedSignals`는 명령어가 처리할 수 있는 신호 배열을 반환하고, `handleSignal`은 신호가 도착했을 때 호출되어 적절히 처리할 수 있게 합니다.

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan의 `make` 명령어는 컨트롤러, 작업(job), 마이그레이션, 테스트 등 여러 클래스를 생성하는 데 사용합니다. 이 클래스들은 입력값을 바탕으로 내용이 채워지는 "스텁(stub)" 파일들을 기반으로 생성됩니다. 하지만, Artisan이 생성하는 파일을 약간 수정하고 싶을 경우가 있을 수 있습니다.

이럴 때 `stub:publish` 명령어로 기본 스텁 파일들을 애플리케이션 내로 퍼블리시하여 직접 수정할 수 있습니다:

```
php artisan stub:publish
```

퍼블리시된 스텁 파일들은 애플리케이션 루트의 `stubs` 디렉터리에 위치하게 됩니다. 이 스텁들을 수정하면, 해당 스텁을 사용하는 Artisan `make` 명령어 실행 시 수정된 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 과정에서 세 가지 이벤트를 디스패치 합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. 

- `ArtisanStarting` 이벤트는 Artisan이 실행 시작하자마자 디스패치됩니다.  
- `CommandStarting` 이벤트는 명령어가 실행되기 직전에 디스패치됩니다.  
- `CommandFinished` 이벤트는 명령어 실행이 완료되었을 때 디스패치됩니다.