# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [태스크 작성하기](#writing-tasks)
    - [태스크 정의하기](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크](#completion-hooks)
- [태스크 실행하기](#running-tasks)
    - [태스크 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 자동화하는 도구입니다. [Blade](/docs/{{version}}/blade) 스타일 문법을 사용하여 배포, Artisan 명령 등 다양한 작업을 간편하게 설정할 수 있습니다. Envoy는 현재 Mac과 Linux 운영체제만 지원하며, Windows 환경에서는 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 통해 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용해 Envoy를 프로젝트에 설치하세요:

```
composer require laravel/envoy --dev
```

설치가 완료되면 Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉터리에 생성됩니다:

```
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 태스크 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 태스크 정의하기 (Defining Tasks)

태스크는 Envoy의 기본 단위로, 원격 서버에서 실행할 쉘 명령을 정의합니다. 예를 들어, 모든 큐 작업 서버에서 `php artisan queue:restart` 명령을 실행하는 태스크를 정의할 수 있습니다.

모든 Envoy 태스크는 프로젝트 루트에 `Envoy.blade.php` 파일 내에 정의해야 합니다. 다음은 시작을 돕는 예제입니다:

```bash
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예제에서 `@servers`에는 여러 서버 배열이 정의되어 있으며, 각 태스크 `on` 옵션에서 이 서버 이름으로 참조할 수 있습니다. `@servers` 선언은 한 줄로 작성되어야 합니다. `@task` 안에는 해당 태스크 실행 시 원격 서버에서 실행할 쉘 명령을 배치합니다.

<a name="local-tasks"></a>
#### 로컬 태스크 (Local Tasks)

스크립트를 로컬 컴퓨터에서 실행하려면 서버 IP 주소로 `127.0.0.1`을 지정하면 됩니다:

```bash
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 태스크 가져오기 (Importing Envoy Tasks)

`@import` 지시어를 사용해 다른 Envoy 파일을 가져올 수 있으며, 해당 파일에 정의된 스토리와 태스크를 자신의 Envoy 파일에 병합할 수 있습니다. 가져온 파일 내 태스크들은 마치 자신의 Envoy 파일에 정의된 것처럼 실행할 수 있습니다:

```bash
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버 (Multiple Servers)

Envoy는 여러 서버에 동시에 태스크를 실행할 수 있도록 지원합니다. 먼저, `@servers`에 여러 서버를 추가해 고유 이름을 부여하세요. 그런 다음 태스크의 `on` 옵션에 실행할 서버 이름 배열을 작성하면 됩니다:

```bash
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### 병렬 실행 (Parallel Execution)

기본적으로 태스크는 각 서버에서 순차적으로 실행됩니다. 즉, 첫 번째 서버 태스크가 끝나야 두 번째 서버에서 실행합니다. 여러 서버에서 병렬로 실행하려면 태스크 선언에 `parallel` 옵션을 추가하세요:

```bash
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정 (Setup)

Envoy 태스크 실행 전 임의의 PHP 코드를 실행해야 할 때가 있습니다. 이때 `@setup` 지시어를 사용해서 태스크 전에 실행할 PHP 코드를 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

태스크 실행 전에 다른 PHP 파일을 반드시 포함해야 한다면 `Envoy.blade.php` 맨 위에 `@include` 지시어를 사용할 수 있습니다:

```bash
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

필요시, Envoy 태스크를 실행할 때 커맨드 라인에서 인수를 넘겨줄 수 있습니다:

```
php vendor/bin/envoy run deploy --branch=master
```

태스크 내에서는 Blade의 출력 문법을 이용해 전달된 값을 사용할 수 있고, 조건문과 반복문도 포함할 수 있습니다. 예를 들어 `$branch` 변수 존재 여부를 확인하고 `git pull` 명령을 실행하는 예시는 다음과 같습니다:

```bash
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask
```

<a name="stories"></a>
### 스토리 (Stories)

스토리는 여러 태스크를 하나의 이름으로 그룹화한 것입니다. 예를 들어 `deploy` 스토리는 `update-code`와 `install-dependencies` 태스크를 순서대로 실행하도록 정의할 수 있습니다:

```bash
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask
```

정의한 스토리는 마치 태스크처럼 다음과 같이 실행할 수 있습니다:

```
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

태스크와 스토리가 실행되는 과정에서 여러 후크가 실행됩니다. Envoy에서 지원하는 후크 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 후크에 작성된 코드는 PHP로 해석되며, 원격 서버가 아닌 로컬에서 실행됩니다.

각 후크는 여러 개를 작성할 수 있으며, 스크립트에 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 태스크 실행 전에 `@before` 후크에 정의된 내용들이 실행됩니다. 후크 내에서는 실행 예정인 태스크 이름을 `$task` 변수로 받을 수 있습니다:

```php
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

각 태스크 실행 후에 `@after` 후크에 정의된 내용들이 실행됩니다. 수행된 태스크 이름이 `$task` 변수에 전달됩니다:

```php
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

태스크가 실패할 경우(종료 상태 코드가 `0`보다 클 때), `@error` 후크가 실행됩니다. 태스크 이름은 `$task` 변수로 전달됩니다:

```php
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

태스크가 모두 에러 없이 정상적으로 실행되면 `@success` 후크가 실행됩니다:

```bash
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 태스크 실행이 종료된 후(종료 상태 코드와 무관하게) `@finished` 후크가 실행됩니다. 종료 상태 코드는 `$exitCode` 변수로 전달되며, null 또는 0 이상의 정수입니다:

```bash
@finished
    if ($exitCode > 0) {
        // 태스크 중 하나에 오류가 발생했습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 태스크 실행하기 (Running Tasks)

애플리케이션 `Envoy.blade.php` 파일에 정의한 태스크 또는 스토리를 실행하려면 Envoy의 `run` 명령어를 통해 실행할 이름을 지정하세요. 태스크 실행 중 원격 서버의 출력 결과가 실시간으로 표시됩니다:

```
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 태스크 실행 확인 (Confirming Task Execution)

중요하거나 파괴적인 작업을 실행하기 전에 사용자 확인을 받고 싶다면 태스크 선언에 `confirm` 옵션을 추가하세요:

```bash
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## 알림 (Notifications)

<a name="slack"></a>
### Slack

Envoy는 태스크 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어에는 Slack 웹훅 URL과 채널명 또는 사용자명을 전달해야 합니다. Slack 제어판에서 "Incoming WebHooks" 통합을 생성하여 웹훅 URL을 받으세요.

첫 번째 인자로 전체 웹훅 URL을 넘기고, 두 번째 인자는 채널(`#channel`) 또는 사용자(`@user`) 이름을 넣습니다:

```
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본 알림 메시지 대신 커스텀 메시지를 보내려면 세 번째 인자로 텍스트를 넘기면 됩니다:

```
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 [Discord](https://discord.com)에도 알림을 지원합니다. `@discord` 지시어는 Discord 웹훅 URL을 인자로 받습니다. Discord 서버 설정에서 "Webhook"을 생성한 후 전체 웹훅 URL을 전달하세요:

```
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

[Telegram](https://telegram.org) 알림도 지원합니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 인자로 받습니다. [BotFather](https://t.me/botfather)를 통해 봇 ID를 생성하고, [@username_to_id_bot](https://t.me/username_to_id_bot)을 통해 채팅 ID를 조회하세요:

```
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

[Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) 알림도 지원합니다. `@microsoftTeams` 지시어는 필수 인자로 Teams 웹훅 URL을 받으며, 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 추가로 받을 수 있습니다. Teams 웹훅은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) 생성 과정을 통해 획득할 수 있습니다. 메시지 박스의 제목, 요약, 섹션 등 다양한 속성 설정이 가능하며 상세 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 웹훅 URL을 전달하면 됩니다:

```
@finished
    @microsoftTeams('webhook-url')
@endfinished
```