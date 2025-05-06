# Artisan 콘솔

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령 작성하기](#writing-commands)
    - [명령 생성하기](#generating-commands)
    - [명령 구조](#command-structure)
    - [클로저 명령](#closure-commands)
    - [단일 실행 명령(고립 명령)](#isolatable-commands)
- [입력값 정의하기](#defining-input-expectations)
    - [인수(Arguments)](#arguments)
    - [옵션(Options)](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
- [명령 입출력](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력값 프롬프트하기](#prompting-for-input)
    - [출력 작성하기](#writing-output)
- [명령 등록하기](#registering-commands)
- [프로그래밍적으로 명령 실행](#programmatically-executing-commands)
    - [다른 명령에서 명령 호출하기](#calling-commands-from-other-commands)
- [신호 처리](#signal-handling)
- [스텁 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발할 때 도움이 되는 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

모든 명령에는 인수 및 옵션을 표시하고 설명하는 "도움말" 화면이 포함되어 있습니다. 도움말 화면을 보려면 명령 앞에 `help`를 붙이십시오:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면, Artisan 명령을 호출할 때 `sail` 커맨드라인을 사용해야 합니다. Sail은 Artisan 명령어를 애플리케이션의 Docker 컨테이너 안에서 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

Laravel Tinker는 [PsySH](https://github.com/bobthecow/psysh) 패키지가 탑재된 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션은 기본적으로 Tinker를 포함하고 있습니다. 만약 Tinker를 애플리케이션에서 제거했다면, Composer로 다음과 같이 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> **참고**
> Laravel 애플리케이션을 상호작용할 수 있는 그래픽 UI를 찾고 계신가요? [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 Eloquent 모델, 잡(jobs), 이벤트(events) 등 애플리케이션 전체를 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 다음 Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일을 공개하려면 `vendor:publish` 명령어를 사용하세요:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> **경고**
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 tinker를 사용할 때는 `Bus::dispatch`나 `Queue::push`를 사용해 잡을 디스패치하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### 명령 허용 목록

Tinker에서는 어떤 Artisan 명령을 쉘에서 실행할 수 있는지 "허용 목록"을 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령을 실행할 수 있습니다. 더 많은 명령을 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다:

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a>
#### 별칭 처리가 안되길 원하는 클래스

Tinker는 일반적으로 클래스와 상호작용할 때 자동으로 별칭(alias)을 지정합니다. 하지만 특정 클래스는 별칭이 지정되지 않도록 하고 싶을 수 있습니다. 이 경우 `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가하면 됩니다:

    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>
## 명령 작성하기

Artisan에 기본 제공된 명령 외에도 자체 커스텀 명령을 만들 수 있습니다. 명령 클래스는 일반적으로 `app/Console/Commands` 디렉토리에 저장하지만, Composer로 로드할 수만 있다면 원하는 위치를 선택할 수 있습니다.

<a name="generating-commands"></a>
### 명령 생성하기

새 명령을 생성하려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉토리에 새 명령 클래스를 생성합니다. 해당 디렉토리가 없다면, 최초 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령 구조

명령을 생성한 후, 클래스의 `signature`와 `description` 속성에 적절한 값을 지정해야 합니다. 이 속성들은 `list` 화면에서 명령을 표시할 때 사용됩니다. `signature` 속성을 사용해 [명령 입력값의 기대치](#defining-input-expectations)도 정의할 수 있습니다. 명령이 실행되면 `handle` 메서드가 호출됩니다. 이 메서드에 명령의 주요 로직을 작성하세요.

예제 명령을 살펴봅시다. `handle` 메서드를 통해 필요한 의존성도 주입받을 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)는 메서드의 타입힌트를 자동으로 인식하여 의존성을 주입합니다:

    <?php

    namespace App\Console\Commands;

    use App\Models\User;
    use App\Support\DripEmailer;
    use Illuminate\Console\Command;

    class SendEmails extends Command
    {
        /**
         * 콘솔 명령의 이름 및 시그니처
         *
         * @var string
         */
        protected $signature = 'mail:send {user}';

        /**
         * 콘솔 명령의 설명
         *
         * @var string
         */
        protected $description = '마케팅 이메일을 사용자에게 전송';

        /**
         * 콘솔 명령 실행
         *
         * @param  \App\Support\DripEmailer  $drip
         * @return mixed
         */
        public function handle(DripEmailer $drip)
        {
            $drip->send(User::find($this->argument('user')));
        }
    }

> **참고**
> 코드 재사용성을 높이기 위해, 콘솔 명령 로직은 최대한 얇게 작성하고, 실제 작업은 별도의 서비스 클래스에 위임하는 것이 좋습니다. 위의 예시처럼 서비스 클래스를 주입받아 주요 처리를 맡기는 구조를 지향하세요.

<a name="closure-commands"></a>
### 클로저 명령

클로저 기반 명령은 콘솔 명령을 클래스가 아닌 클로저로 정의할 수 있는 대안입니다. 라우트에 대한 클로저를 컨트롤러의 대안으로 쓰는 것과 비슷하게, 명령에 대해서도 클래스가 아닌 클로저로 대체할 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드 내에서 `routes/console.php` 파일을 불러옵니다:

    /**
     * 애플리케이션의 클로저 기반 명령 등록
     *
     * @return void
     */
    protected function commands()
    {
        require base_path('routes/console.php');
    }

이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션의 콘솔 진입점(라우트 역할)을 정의합니다. 이 파일에서 `Artisan::command` 메서드를 이용해 모든 클로저 기반 콘솔 명령을 정의할 수 있습니다. `command` 메서드는 [명령 시그니처](#defining-input-expectations)와 인수 및 옵션을 받을 클로저, 두 개의 인자를 가집니다:

    Artisan::command('mail:send {user}', function ($user) {
        $this->info("Sending email to: {$user}!");
    });

이 클로저는 기본 명령 인스턴스에 바인딩되므로, 일반적인 명령 클래스에서 접근 가능한 모든 헬퍼 메서드를 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

명령 인수와 옵션 외에도, 클로저에서 [서비스 컨테이너](/docs/{{version}}/container)로부터 해결될 의존성을 타입힌트로 지정할 수 있습니다:

    use App\Models\User;
    use App\Support\DripEmailer;

    Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
        $drip->send(User::find($user));
    });

<a name="closure-command-descriptions"></a>
#### 클로저 명령 설명

클로저 기반 명령을 정의할 때, `purpose` 메서드를 사용해 명령에 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 실행 시 표시됩니다:

    Artisan::command('mail:send {user}', function ($user) {
        // ...
    })->purpose('마케팅 이메일을 사용자에게 전송');

<a name="isolatable-commands"></a>
### 단일 실행 명령(고립 명령)

> **경고**
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

특정 명령이 단 한 번만 실행 중이어야 할 때가 있습니다. 이를 위해 명령 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다:

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Contracts\Console\Isolatable;

    class SendEmails extends Command implements Isolatable
    {
        // ...
    }

명령에 `Isolatable`이 적용되면, Laravel은 자동으로 명령에 `--isolated` 옵션을 추가합니다. 이 옵션으로 명령을 실행하면, 이미 실행 중인 동명 명령이 없는지 확인합니다. 이는 기본 캐시 드라이버를 이용해 원자적 락을 획득하려 시도함으로써 구현됩니다. 다른 인스턴스가 실행 중이라면 명령은 실행되지 않으며, 성공 상태 코드로 종료합니다:

```shell
php artisan mail:send 1 --isolated
```

명령이 실행되지 못했을 때 반환할 종료 코드(exit code)를 지정하려면 `isolated` 옵션에 원하는 값을 전달하면 됩니다:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-expiration-time"></a>
#### 락 만료 시간

기본적으로, 고립 락은 명령이 종료됨과 동시에 만료됩니다. 만약 명령이 중단되어 종료되지 못했다면, 락은 1시간 후 만료됩니다. 만료 시간을 변경하려면 명령 클래스에 `isolationLockExpiresAt` 메서드를 정의하면 됩니다:

```php
/**
 * 명령의 고립 락 만료 시점 반환
 *
 * @return \DateTimeInterface|\DateInterval
 */
public function isolationLockExpiresAt()
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
## 입력값 정의하기

콘솔 명령을 작성할 때, 사용자로부터 인수나 옵션 형태로 입력값을 받아야 할 필요가 많습니다. Laravel은 명령의 `signature` 속성을 사용해 예상하는 입력값을 매우 쉽게 정의할 수 있도록 해줍니다. 이 속성을 이용해 명령 이름, 인수, 옵션을 한 번에 읽기 쉬운 라우트-like 형식으로 정의할 수 있습니다.

<a name="arguments"></a>
### 인수(Arguments)

모든 사용자 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서 명령은 필수 인수 `user` 하나를 정의합니다:

    /**
     * 콘솔 명령의 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

인수를 선택적으로 하거나 기본값을 정할 수도 있습니다:

    // 선택적 인수...
    'mail:send {user?}'

    // 기본값이 있는 선택적 인수...
    'mail:send {user=foo}'

<a name="options"></a>
### 옵션(Options)

옵션도 인수와 유사한 사용자 입력입니다. 커맨드라인에서는 옵션 앞에 두 개의 하이픈(`--`)을 붙입니다. 옵션엔 값이 있는 옵션과 값이 없는 옵션(부울 스위치)이 있습니다. 값이 없는 옵션은 단순 true/false 스위치 역할을 하며, 예시:

    /**
     * 콘솔 명령의 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue}';

여기서 `--queue` 스위치는 명령 호출 시 지정할 수 있습니다. 지정하면 해당 옵션 값은 `true`, 지정하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

옵션에 값을 받아야 한다면, 옵션 이름 끝에 `=` 기호를 붙입니다:

    /**
     * 콘솔 명령의 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue=}';

사용자는 아래처럼 옵션에 값을 넘길 수 있으며, 옵션 미지정 시 값은 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션의 기본값은 옵션명 뒤에 즉시 지정할 수 있습니다. 사용자가 값을 안 주면 기본값이 쓰입니다:

    'mail:send {user} {--queue=default}'

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 정의 시 단축키를 지정하려면 옵션 이름 앞에 단축키를 쓰고, `|` 문자로 구분합니다:

    'mail:send {user} {--Q|queue}'

터미널에서 옵션 단축키는 한 개의 하이픈으로 실행합니다:

```shell
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a>
### 입력 배열

인수 혹은 옵션이 여러 개 값을 받도록 하려면 `*` 문자를 사용할 수 있습니다. 예를 들어:

    'mail:send {user*}'

아래처럼 명령어를 실행하면 `user` 인수 값이 `[1, 2]`인 배열이 됩니다:

```shell
php artisan mail:send 1 2
```

선택적 인수와 조합해 0개 이상의 인수를 받을 수도 있습니다:

    'mail:send {user?*}'

<a name="option-arrays"></a>
#### 옵션 배열

옵션이 여러 값을 받을 때는, 각각의 옵션 값 앞에 옵션 이름을 붙여 실행합니다:

    'mail:send {--id=*}'

아래처럼 여러 번 `--id` 옵션을 쓸 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

인수와 옵션에 설명을 붙일 땐, 이름 뒤에 콜론으로 구분합니다. 명령 정의를 여러 줄로 나눠 작성해도 됩니다:

    /**
     * 콘솔 명령의 이름 및 시그니처
     *
     * @var string
     */
    protected $signature = 'mail:send
                            {user : 사용자의 ID}
                            {--queue : 작업을 큐에 넣을지 여부}';

<a name="command-io"></a>
## 명령 입출력

<a name="retrieving-input"></a>
### 입력값 가져오기

명령 실행 중에는 사용자가 넘긴 인수, 옵션 값을 가져와야 합니다. `argument`와 `option` 메서드를 통해 액세스할 수 있으며, 없어도 `null`을 반환합니다:

    /**
     * 콘솔 명령 실행
     *
     * @return int
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

모든 인수를 배열로 얻고 싶으면 `arguments` 메서드를 사용하세요:

    $arguments = $this->arguments();

옵션도 `option` 메서드로 개별적으로, `options` 메서드로 전체 배열을 얻을 수 있습니다:

    // 특정 옵션
    $queueName = $this->option('queue');

    // 전체 옵션 배열
    $options = $this->options();

<a name="prompting-for-input"></a>
### 입력값 프롬프트하기

출력뿐 아니라 명령 실행 중 사용자에게 입력을 요청할 수도 있습니다. `ask` 메서드는 질문을 띄우고 답변을 받아 반환합니다:

    /**
     * 콘솔 명령 실행
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('이름이 무엇인가요?');
    }

`secret` 메서드는 `ask`와 비슷하지만, 입력 시 터미널에 입력값이 보이지 않습니다(비밀번호 등 민감정보에 활용):

    $password = $this->secret('비밀번호를 입력하세요');

<a name="asking-for-confirmation"></a>
#### 확인 프롬프트

"예/아니오" 형태의 확인이 필요하다면 `confirm` 메서드를 활용하세요. 기본적으로 사용자가 `y`나 `yes`를 입력해야 `true`를 반환하고, 그 외에는 `false`를 반환합니다.

    if ($this->confirm('계속 진행할까요?')) {
        //
    }

필요하다면 두 번째 인자로 `true`를 넘겨 기본값을 yes로 바꿀 수도 있습니다:

    if ($this->confirm('계속 진행할까요?', true)) {
        //
    }

<a name="auto-completion"></a>
#### 자동완성

`anticipate` 메서드는 자동완성 가능한 선택지를 줄 수 있습니다. 자동완성과 무관하게 어떤 답변이든 입력 가능합니다:

    $name = $this->anticipate('이름이 무엇인가요?', ['Taylor', 'Dayle']);

또는, 두 번째 인자에 클로저를 넘겨 사용자가 입력을 할 때마다 자동완성 후보를 실시간으로 반환할 수도 있습니다:

    $name = $this->anticipate('주소가 무엇인가요?', function ($input) {
        // 자동완성 후보 반환...
    });

<a name="multiple-choice-questions"></a>
#### 다중 선택질문

미리 정해둔 선택지에서 고르게 하려면 `choice` 메서드를 사용하세요. 선택지 배열 인덱스를 세 번째 인자로 넘겨 기본값을 지정할 수 있습니다:

    $name = $this->choice(
        '이름이 무엇인가요?',
        ['Taylor', 'Dayle'],
        $defaultIndex
    );

최대 시도 횟수, 복수 선택 허용 여부도 네 번째/다섯 번째 인자로 지정할 수 있습니다:

    $name = $this->choice(
        '이름이 무엇인가요?',
        ['Taylor', 'Dayle'],
        $defaultIndex,
        $maxAttempts = null,
        $allowMultipleSelections = false
    );

<a name="writing-output"></a>
### 출력 작성하기

콘솔에 메시지를 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 각각 목적에 맞는 ANSI 색상을 사용합니다. 예를 들어, `info`는 녹색입니다:

    /**
     * 콘솔 명령 실행
     *
     * @return mixed
     */
    public function handle()
    {
        // ...

        $this->info('명령이 성공적으로 실행되었습니다!');
    }

에러 메시지는 `error` 메서드로 빨간색으로 표시할 수 있습니다:

    $this->error('문제가 발생했습니다!');

색 없는 일반 텍스트는 `line` 메서드를 사용하세요:

    $this->line('이 메시지를 표시합니다');

공백 줄을 추가하려면 `newLine` 메서드를 사용합니다:

    // 공백 한 줄
    $this->newLine();

    // 공백 세 줄
    $this->newLine(3);

<a name="tables"></a>
#### 테이블

`table` 메서드를 사용하면 여러 행/열의 데이터를 깔끔한 테이블로 출력할 수 있습니다. 칼럼명과 데이터만 넘기면, Laravel이 자동으로 표의 크기를 계산합니다:

    use App\Models\User;

    $this->table(
        ['Name', 'Email'],
        User::all(['name', 'email'])->toArray()
    );

<a name="progress-bars"></a>
#### 프로그레스 바

실행 시간이 긴 작업에선 프로그레스 바로 진척도를 표시할 수 있습니다. `withProgressBar` 메서드를 사용하면 반복 처리를 할 때마다 진행도가 자동 반영됩니다:

    use App\Models\User;

    $users = $this->withProgressBar(User::all(), function ($user) {
        $this->performTask($user);
    });

더 세밀한 제어가 필요하다면, 먼저 전체 반복 횟수를 지정하고 각 아이템 처리 후 바를 수동으로 진척시키면 됩니다:

    $users = App\Models\User::all();

    $bar = $this->output->createProgressBar(count($users));

    $bar->start();

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();

> **참고**
> 더 다양한 기능은 [Symfony Progress Bar 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령 등록하기

모든 콘솔 명령은 애플리케이션의 "콘솔 커널"인 `App\Console\Kernel` 클래스에 등록됩니다. 이 클래스의 `commands` 메서드 안에서 커널의 `load` 메서드를 호출하는 부분을 볼 수 있습니다. `load`는 `app/Console/Commands` 디렉토리를 스캔하며, 그 안의 모든 명령 클래스를 Artisan에 자동으로 등록합니다. 다른 디렉토리도 추가로 스캔하도록 `load`를 추가로 호출할 수도 있습니다:

    /**
     * 애플리케이션 명령 등록
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');
        $this->load(__DIR__.'/../Domain/Orders/Commands');

        // ...
    }

필요하다면, `App\Console\Kernel` 클래스 내에 `$commands` 속성을 정의하고, 여기에 명령 클래스명을 추가해 수동으로 등록할 수 있습니다. 이 속성이 없다면 직접 정의해야 합니다. Artisan이 부팅될 때 이 속성의 명령들은 [서비스 컨테이너](/docs/{{version}}/container)로 해결(resolve)되어 등록됩니다:

    protected $commands = [
        Commands\SendEmails::class
    ];

<a name="programmatically-executing-commands"></a>
## 프로그래밍적으로 명령 실행

CLI 밖(예: 라우트나 컨트롤러 등)에서 Artisan 명령을 실행하고 싶을 때가 있습니다. 이때는 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. 첫 번째 인자로 명령 시그니처 혹은 클래스명, 두 번째 인자로 명령 파라미터 배열을 전달하면, 종료 코드(exit code)를 반환합니다:

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        $exitCode = Artisan::call('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

아니면 전체 Artisan 명령을 문자열로 전달해도 됩니다:

    Artisan::call('mail:send 1 --queue=default');

<a name="passing-array-values"></a>
#### 배열 값 전달

옵션이 배열을 받을 경우, 옵션에 값 배열을 입력하면 됩니다:

    use Illuminate\Support\Facades\Artisan;

    Route::post('/mail', function () {
        $exitCode = Artisan::call('mail:send', [
            '--id' => [5, 13]
        ]);
    });

<a name="passing-boolean-values"></a>
#### 불리언 값 전달

문자열 값을 받지 않는 옵션(예: `migrate:refresh`의 `--force`)을 업데이트해야 한다면, 옵션값에 `true`/`false`를 넘기면 됩니다:

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

<a name="queueing-artisan-commands"></a>
#### Artisan 명령 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면, [큐 워커](/docs/{{version}}/queues)로 백그라운드에서 Artisan 명령을 처리할 수도 있습니다. 이 기능을 사용하기 전에 큐 설정과 큐 리스너 실행이 필요합니다:

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        Artisan::queue('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

`onConnection` 및 `onQueue`를 연결하여 커맨드를 보낼 커넥션이나 큐도 지정할 수 있습니다:

    Artisan::queue('mail:send', [
        'user' => 1, '--queue' => 'default'
    ])->onConnection('redis')->onQueue('commands');

<a name="calling-commands-from-other-commands"></a>
### 다른 명령에서 명령 호출하기

기존 Artisan 명령 내에서 다른 명령을 호출하고 싶을 때가 있습니다. `call` 메서드를 사용하면 됩니다. 명령명과 인수/옵션 배열을 넘깁니다:

    /**
     * 콘솔 명령 실행
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

명령 실행 시 모든 출력을 숨기려면 `callSilently` 메서드를 이용하세요. 시그니처는 `call`과 동일합니다:

    $this->callSilently('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

<a name="signal-handling"></a>
## 신호 처리

운영체제는 실행 중인 프로세스에 신호(signal)를 보낼 수 있습니다. 예를 들어, `SIGTERM`은 프로그램 종료 요청 신호입니다. Artisan 콘솔 명령에서 특정 신호를 감지해 동작하게 하려면 `trap` 메서드를 사용하면 됩니다:

    /**
     * 콘솔 명령 실행
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

여러 신호를 동시에 감지하려면, 신호 배열을 `trap`에 넘기면 됩니다:

    $this->trap([SIGTERM, SIGQUIT], function ($signal) {
        $this->shouldKeepRunning = false;

        dump($signal); // SIGTERM / SIGQUIT
    });

<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan 콘솔의 `make` 명령은 컨트롤러, 잡(jobs), 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 "스텁(stub) 파일"을 이용해 만들어지며, 입력값 기반으로 일부 내용이 채워집니다. Artisan이 생성하는 파일에 약간의 수정을 하고 싶다면, `stub:publish` 명령을 사용해 주요 스텁 파일을 애플리케이션에 퍼블리시한 후 직접 수정할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁은 애플리케이션 루트의 `stubs` 디렉토리에 위치합니다. 이 스텁 파일을 변경하면, 향후 해당 종류의 클래스를 Artisan의 `make` 명령으로 생성할 때 변경된 내용이 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan 실행 직후 발생하고, 그다음 `CommandStarting` 이벤트가 명령 실행 직전 발생합니다. 마지막으로 명령이 끝나면 `CommandFinished` 이벤트가 발생합니다.