# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [여러 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크(Hooks)](#completion-hooks)
- [작업 실행하기](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 손쉽게 수행할 수 있게 해 주는 도구입니다. [Blade](/docs/10.x/blade) 스타일 문법을 사용하여 배포, Artisan 명령어 실행 등 다양한 작업을 쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 지원하며, Windows 환경에서는 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 통해 사용 가능합니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 통해 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

설치가 완료되면, 애플리케이션의 `vendor/bin` 디렉토리에 Envoy 실행 파일이 생성됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 작업 정의하기 (Defining Tasks)

작업(Task)은 Envoy의 기본 단위로, 작업이 호출될 때 원격 서버에서 실행될 셸 명령어를 정의합니다. 예를 들어, 애플리케이션의 큐 워커 서버에서 `php artisan queue:restart` 명령어를 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일 안에 정의해야 합니다. 시작을 위한 예시는 다음과 같습니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시처럼 파일 상단에 `@servers` 배열로 서버들을 정의하면, 이후 작업 선언 시 `on` 옵션에서 해당 서버들을 참조할 수 있습니다. `@servers` 선언은 항상 한 줄로 작성해야 하며, `@task` 선언 내에는 작업 실행 시 서버에서 수행할 셸 명령어를 작성합니다.

<a name="local-tasks"></a>
#### 로컬 작업 (Local Tasks)

작업을 로컬 컴퓨터에서 실행하도록 강제하려면, 서버 IP를 `127.0.0.1`로 지정하세요:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 불러오기 (Importing Envoy Tasks)

`@import` 지시어를 사용하여 다른 Envoy 파일을 불러오면, 그 안의 스토리와 작업이 현재 파일에 추가됩니다. 불러온 작업들은 마치 현재 Envoy 파일에 정의된 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 여러 서버 (Multiple Servers)

Envoy는 여러 서버에 걸쳐 작업을 쉽게 실행하도록 지원합니다. 먼저 `@servers` 선언에 서버를 추가하고, 각 서버에 고유 이름을 부여하세요. 그런 다음 작업의 `on` 배열에 서버 이름들을 나열하여 작업을 실행할 서버들을 지정할 수 있습니다:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### 병렬 실행 (Parallel Execution)

기본적으로 작업은 각 서버에 순차적으로 실행됩니다. 즉, 첫 번째 서버 작업이 끝난 후 두 번째 서버에서 실행됩니다. 여러 서버에서 작업을 병렬로 실행하려면 작업 선언에 `parallel` 옵션을 추가하세요:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정 (Setup)

Envoy 작업 실행 전에 임의의 PHP 코드를 실행해야 할 경우, `@setup` 지시어를 사용해 PHP 코드 블록을 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 다른 PHP 파일을 불러와야 한다면, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용하세요:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

필요에 따라 Envoy 작업 실행 시 명령어 인수를 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법으로 옵션에 접근할 수 있고, `if` 문 및 반복문도 사용할 수 있습니다. 예를 들어, `git pull`을 실행하기 전에 `$branch` 변수가 존재하는지 확인하는 코드는 다음과 같습니다:

```blade
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

스토리는 여러 작업을 하나의 이름으로 묶는 기능입니다. 예를 들어, `deploy` 스토리는 `update-code`와 `install-dependencies` 작업을 순서대로 실행하도록 정의할 수 있습니다:

```blade
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

스토리 작성 후에는 작업 실행과 동일하게 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

작업과 스토리가 실행될 때 여러 후크가 실행됩니다. Envoy가 지원하는 후크는 `@before`, `@after`, `@error`, `@success`, `@finished`가 있으며, 모두 PHP 코드로 해석되어 로컬에서 실행됩니다. 후크 코드는 작업이 상호작용하는 원격 서버가 아닌 로컬에서만 실행됩니다.

후크는 원하는 만큼 여러 개 정의할 수 있으며, 스크립트에 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업 실행 전, Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. 이 후크들은 실행될 작업 이름을 인수로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후, Envoy 스크립트의 모든 `@after` 후크가 실행되며, 실행된 작업 이름이 인수로 전달됩니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업 실패 시(exit 코드가 0보다 클 때), 모든 `@error` 후크가 실행됩니다. 실패한 작업 이름을 인수로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 에러 없이 성공적으로 실행된 경우, `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업 실행이 끝난 후(성공, 실패와 관계없이), `@finished` 후크가 실행됩니다. 이 후크는 종료 코드(exit code)를 인수로 받으며, 이는 `null`이거나 0 이상의 정수일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 작업 중 오류가 있었습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기 (Running Tasks)

애플리케이션의 `Envoy.blade.php`에 정의된 작업이나 스토리를 실행하려면, Envoy의 `run` 명령어에 실행할 작업 또는 스토리 이름을 전달하세요. Envoy는 작업을 실행하며 원격 서버에서 출력되는 결과를 실시간으로 표시합니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인 (Confirming Task Execution)

특정 작업을 실행하기 전에 사용자에게 확인을 요청하도록 하려면, 작업 선언에 `confirm` 디렉티브를 추가하세요. 이는 특히 위험한 작업을 수행할 때 유용합니다:

```blade
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

Envoy는 각 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 훅 URL과 채널 또는 사용자 이름을 인자로 받습니다. Slack 제어판에서 "Incoming WebHooks" 통합을 생성하여 웹훅 URL을 획득할 수 있습니다.

첫 번째 인자에는 전체 웹훅 URL을, 두 번째 인자에는 채널 이름(`#channel`) 혹은 사용자 이름(`@user`)을 전달하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy는 실행한 작업에 대한 메시지를 알림 채널에 보냅니다. 하지만 세 번째 인자를 전달해 원하는 메시지로 덮어쓸 수도 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

각 작업 실행 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹훅 URL과 메시지를 받습니다. 서버 설정에서 "Webhook"을 생성하고, 알림을 받을 채널을 선택해 웹훅 URL을 획득하세요. 전체 URL을 `@discord` 지시어에 전달합니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

[Telegram](https://telegram.org)으로도 작업 실행 알림을 보낼 수 있습니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 인자로 받습니다. 봇 ID는 [BotFather](https://t.me/botfather)를 통해 새 봇을 생성해 얻으며, 유효한 채팅 ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)를 통해 확인할 수 있습니다. 봇 ID와 채팅 ID를 완전한 문자열로 `@telegram` 지시어에 전달하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

[Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)에도 작업 이후 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 Teams 웹훅 URL(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 받습니다. Teams 웹훅 URL은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)으로 생성할 수 있습니다. Teams API는 제목, 요약, 섹션 등 메시지 커스터마이징이 가능한 추가 속성도 지원합니다. 자세한 내용은 [Microsoft Teams 공식 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 웹훅 URL을 `@microsoftTeams` 지시어에 넘기면 됩니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```