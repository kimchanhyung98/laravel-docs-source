# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [Setup](#setup)
    - [변수](#variables)
    - [스토리(Stories)](#stories)
    - [후킹(Hooks)](#completion-hooks)
- [작업 실행하기](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림(Notification)](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 수행하는 작업을 실행하기 위한 도구입니다. [Blade](/docs/{{version}}/blade) 형식의 문법을 사용하여, 배포, Artisan 명령어 실행 등 다양한 작업을 손쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만을 공식 지원합니다. 하지만, [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용해 Windows에서 Envoy를 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 이용해 Envoy를 프로젝트에 설치하세요:

```shell
composer require laravel/envoy --dev
```

Envoy가 설치되면, Envoy 바이너리는 애플리케이션의 `vendor/bin` 디렉터리에서 사용할 수 있습니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기

<a name="defining-tasks"></a>
### 작업 정의하기

작업(Task)은 Envoy의 기본 구성 요소입니다. 작업은 해당 작업이 실행될 때 원격 서버에서 어떤 셸 명령어가 실행될지 정의합니다. 예를 들어, 모든 큐 워커 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

Envoy의 모든 작업은 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일에 정의해야 합니다. 시작 예시는 다음과 같습니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시에서 알 수 있듯이, 파일 상단에서 `@servers` 배열을 정의하여 작업 선언 시 `on` 옵션을 통해 해당 서버를 참조할 수 있습니다. `@servers` 선언은 항상 한 줄로 작성해야 합니다. 작업 내부에는 태스크 실행 시 수행될 셸 명령어를 정의합니다.

<a name="local-tasks"></a>
#### 로컬 작업

스크립트를 로컬 컴퓨터에서 실행하려면, 서버 IP 주소를 `127.0.0.1`로 지정하세요:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기

`@import` 디렉티브를 사용하면 다른 Envoy 파일을 가져와 해당 스토리와 작업을 자신의 Envoy 파일에서 사용할 수 있습니다. 가져온 후에는 자신의 Envoy 파일에 정의된 작업처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버

Envoy는 여러 서버에서 작업을 쉽게 실행할 수 있도록 해줍니다. 먼저, `@servers` 선언에 서버를 추가하세요. 각 서버는 고유한 이름을 가져야 합니다. 추가 서버를 정의했다면, 작업의 `on` 배열에 각각의 서버 이름을 나열하면 됩니다:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### 병렬 실행

기본적으로 작업은 각 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 완료된 후 두 번째 서버에서 실행이 시작됩니다. 여러 서버에 병렬로 작업을 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 추가하세요:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### Setup

가끔씩 Envoy 작업 실행 전에 임의의 PHP 코드를 실행해야 할 수 있습니다. 이럴 때 `@setup` 디렉티브를 사용해 작업 실행 전 실행될 PHP 코드 블록을 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 수행 전 추가 PHP 파일이 필요하다면, `Envoy.blade.php` 파일 상단에서 `@include` 디렉티브를 사용할 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수

필요에 따라, Envoy 작업 실행 시 커맨드 라인에서 인수를 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법으로 옵션 값을 사용할 수 있습니다. 또한 Blade의 `if` 문이나 반복문도 사용 가능합니다. 예를 들어, `git pull` 명령 실행 전 `$branch` 변수가 존재하는지 확인할 수 있습니다:

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
### 스토리(Stories)

스토리는 여러 작업을 하나의 편리한 이름으로 묶어 실행할 수 있게 도와줍니다. 예를 들어, `deploy` 스토리에서 `update-code`와 `install-dependencies` 작업을 차례로 실행할 수 있습니다:

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

스토리를 작성한 후에는 작업과 동일하게 실행할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후킹(Hooks)

작업과 스토리가 실행될 때 다양한 후킹(hook)이 실행됩니다. Envoy가 지원하는 후킹 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 후킹 안의 모든 코드는 PHP로 해석되며, 원격 서버가 아니라 로컬에서 실행됩니다.

각 후킹은 원하는 만큼 정의할 수 있으며, Envoy 스크립트에 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업 실행 전에, Envoy 스크립트에서 등록된 모든 `@before` 후킹이 실행됩니다. `@before` 후킹은 실행될 작업의 이름을 전달받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후, Envoy 스크립트에서 등록된 모든 `@after` 후킹이 실행됩니다. `@after` 후킹은 실행된 작업의 이름을 전달받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패(종료 코드가 0 초과) 할 때마다, 등록된 모든 `@error` 후킹이 실행됩니다. `@error` 후킹은 실행된 작업의 이름을 전달받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 완료되면, 등록된 모든 `@success` 후킹이 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이(종료 코드에 상관없이) 실행된 후, 등록된 모든 `@finished` 후킹이 실행됩니다. `@finished` 후킹은 완료된 작업의 상태 코드(또는 `null`, 0 이상의 `integer`)를 전달받습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 한 작업에서 오류가 발생함...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업 또는 스토리를 실행하려면 Envoy의 `run` 명령어에 실행할 작업 또는 스토리 이름을 전달하세요. Envoy는 작업을 실행하면서 원격 서버의 출력을 표시합니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인

서버에서 특정 작업을 실행하기 전에 확인 프롬프트를 받고 싶다면, 작업 선언에 `confirm` 디렉티브를 추가하세요. 이는 파괴적인 작업(예: 데이터 삭제)에 특히 유용합니다:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## 알림(Notification)

<a name="slack"></a>
### Slack

Envoy는 각 작업이 실행된 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 디렉티브는 Slack hook URL과 채널 / 사용자명을 인수로 받습니다. Slack 제어판에서 "Incoming WebHooks" 통합을 생성하면 Webhook URL을 얻을 수 있습니다.

첫 번째 인수로 전체 Webhook URL을, 두 번째 인수로 채널명 (`#channel`)이나 사용자명 (`@user`)을 전달하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 실행된 작업을 설명하는 메시지를 알림 채널로 보냅니다. 세 번째 인수로 메시지를 전달해 사용자 지정 메시지를 보낼 수 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 [Discord](https://discord.com)로도 작업 실행 후 알림을 보낼 수 있습니다. `@discord` 디렉티브는 Discord hook URL과 메시지를 인수로 받습니다. 서버 설정에서 "Webhook"을 새로 생성해 Webhook URL을 얻을 수 있습니다. Webhook URL 전체를 `@discord` 디렉티브에 전달하세요:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 [Telegram](https://telegram.org)으로도 각 작업 실행 후 알림을 보낼 수 있습니다. `@telegram` 디렉티브는 Telegram 봇 ID와 채팅 ID를 인수로 받습니다. [BotFather](https://t.me/botfather)로 새 봇을 생성하면 Bot ID를, [@username_to_id_bot](https://t.me/username_to_id_bot)으로 유효한 Chat ID를 얻을 수 있습니다. 두 값을 모두 `@telegram` 디렉티브에 전달하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)에도 각 작업 실행 후 알림을 보낼 수 있습니다. `@microsoftTeams` 디렉티브는 Teams Webhook(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인수로 받습니다. [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 새로 생성해 Teams Webhook을 얻을 수 있습니다. Teams API는 제목, 요약, 섹션 등 메시지 상자를 맞춤화할 다양한 속성을 지원합니다. 자세한 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. Webhook URL 전체를 `@microsoftTeams` 디렉티브에 전달하세요:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```