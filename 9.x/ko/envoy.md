# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [여러 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크](#completion-hooks)
- [작업 실행하기](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 손쉽게 관리·실행할 수 있는 도구입니다. [Blade](/docs/{{version}}/blade) 스타일의 문법을 사용하여 배포, Artisan 명령 등 다양한 작업을 간편하게 설정할 수 있습니다. Envoy는 현재 Mac과 Linux 운영체제만을 공식 지원하며, [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows에서도 사용이 가능합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 프로젝트에 Envoy를 설치합니다:

```shell
composer require laravel/envoy --dev
```

Envoy가 설치되면, Envoy 바이너리가 애플리케이션의 `vendor/bin` 디렉토리에 위치하게 됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기

<a name="defining-tasks"></a>
### 작업 정의하기

작업(Task)은 Envoy의 기본 구성 요소입니다. 작업은 해당 작업이 호출될 때 원격 서버에서 실행되어야 할 셸 명령을 정의합니다. 예를 들어, 모든 Queue 워커 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 만들 수 있습니다.

Envoy 작업은 반드시 애플리케이션 루트에 있는 `Envoy.blade.php` 파일에 작성해야 합니다. 아래는 시작 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시처럼, 파일 상단에 `@servers` 배열을 정의하여 각 서버를 구성할 수 있으며, 작업의 `on` 옵션에서 정의한 서버 이름을 참조할 수 있습니다. `@servers` 선언은 반드시 한 줄에 작성해야 합니다. 각 `@task` 선언 내에는 해당 작업이 호출될 때 서버에서 실행될 셸 명령을 적어야 합니다.

<a name="local-tasks"></a>
#### 로컬 작업

스크립트를 내 컴퓨터(로컬)에서 실행하고 싶다면 서버의 IP 주소를 `127.0.0.1`로 지정하면 됩니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기

`@import` 디렉티브를 사용하면, 다른 Envoy 파일을 가져와 그 안의 스토리와 작업을 내 Envoy 파일에 추가할 수 있습니다. 가져온 후에는 내 Envoy 파일에 정의된 것처럼 해당 작업들을 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 여러 서버

Envoy는 여러 서버에서 작업을 손쉽게 실행할 수 있게 도와줍니다. 우선 `@servers` 선언에 추가 서버를 정의하고, 각 서버는 고유한 이름을 가져야 합니다. 작업 선언의 `on` 배열에 실행할 서버 이름을 나열합니다:

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

기본적으로 작업은 서버마다 순차적으로 실행됩니다. 즉, 첫 번째 서버에서 작업이 끝난 후에 다음 서버에서 작업이 실행됩니다. 여러 서버에서 병렬로 작업을 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 추가하세요:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정

Envoy 작업을 실행하기 전에 임의의 PHP 코드를 미리 실행해야 하는 경우, `@setup` 디렉티브로 해당 PHP 블록을 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전 다른 PHP 파일을 포함해야 한다면, Envoy 파일 상단에 `@include` 디렉티브를 사용할 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수

필요하다면 Envoy 작업 호출 시 커맨드라인에서 인수를 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법을 사용해 옵션 값을 사용할 수 있습니다. 또한 Blade의 if 문이나 반복문도 작업 내에서 사용할 수 있습니다. 예를 들어, `$branch` 변수가 존재할 때만 `git pull` 명령을 실행하는 방식은 다음과 같습니다:

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
### 스토리

스토리는 여러 작업을 하나의 편리한 이름 아래 묶을 수 있게 해줍니다. 예를 들어, `deploy` 스토리는 내부에 `update-code`와 `install-dependencies` 작업을 포함하여 순차적으로 실행할 수 있습니다:

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

스토리를 작성한 뒤에는 작업을 실행하는 것과 동일하게 커맨드라인에서 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크

작업이나 스토리가 실행될 때, 여러 종류의 후크(Hook)가 실행됩니다. Envoy에서 지원하는 후크 형식은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 후크들에 들어가는 코드는 모두 PHP로 해석되어 로컬에서 실행되며, 작업이 실행되는 원격 서버에서는 실행되지 않습니다.

각 후크는 원하는 만큼 정의할 수 있으며, Envoy 스크립트에 나온 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 작업 실행 전에 Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. 이 후크는 실행될 작업의 이름을 인수로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

각 작업 실행 후에는 등록된 모든 `@after` 후크가 실행됩니다. 이 후크는 실행된 작업의 이름을 인수로 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패(종료 상태 코드가 0보다 클 경우)하면 등록된 모든 `@error` 후크가 실행됩니다. 이 후크는 실행된 작업의 이름을 인수로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되었다면 등록한 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 종료된 후(성공/실패 여부 무관하게), 등록된 모든 `@finished` 후크가 실행됩니다. 이 후크는 작업의 종료 상태 코드(`null` 또는 0 이상의 정수)를 인수로 받습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 하나 이상의 작업에서 에러가 발생했습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면, Envoy의 `run` 명령과 실행할 작업/스토리 이름을 입력합니다. Envoy는 작업을 실행하면서 원격 서버의 실시간 출력을 표시합니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인

서버에서 특정 작업을 실행하기 전 확인 메시지를 받고 싶다면, 작업 선언에 `confirm` 옵션을 추가하세요. 이 옵션은 파괴적인 작업(데이터 삭제 등)에 특히 유용합니다:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## 알림

<a name="slack"></a>
### Slack

Envoy는 각 작업 실행 이후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 디렉티브는 Slack Webhook URL과 채널/사용자 이름을 인수로 받습니다. Webhook URL은 Slack 관리 패널에서 "Incoming WebHooks" 통합 기능을 통해 생성할 수 있습니다.

첫 번째 인수에는 전체 Webhook URL을, 두 번째 인수에는 채널 이름(`#channel`)이나 사용자 이름(`@user`)을 넣으면 됩니다:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 해당 작업의 실행 내역을 슬랙 채널로 전송합니다. 직접 메시지를 작성하려면 세 번째 인수로 메시지를 전달하세요:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 [Discord](https://discord.com)로 작업 실행 결과를 알릴 수도 있습니다. `@discord` 디렉티브는 Discord Webhook URL과 메시지를 인수로 받습니다. Webhook URL은 서버 설정에서 "Webhook"을 생성하여 얻을 수 있습니다. Webhook URL을 `@discord` 디렉티브에 전달하세요:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 [Telegram](https://telegram.org)으로도 작업 알림을 지원합니다. `@telegram` 디렉티브는 텔레그램 Bot ID와 Chat ID를 인수로 받습니다. Bot ID는 [BotFather](https://t.me/botfather)로 새 봇을 생성하여, Chat ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)으로 확인할 수 있습니다. 두 값을 `@telegram` 디렉티브에 입력하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) 알림도 지원합니다. `@microsoftTeams` 디렉티브는 Teams Webhook(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인수로 받을 수 있습니다. Webhook은 Teams의 [Incoming Webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) 기능을 통해 생성할 수 있습니다. Teams API는 제목, 요약, 섹션 등 메시지 박스 커스터마이즈를 위한 다양한 속성을 제공하며, 자세한 내용은 [Microsoft Teams 공식 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인할 수 있습니다. Webhook URL을 `@microsoftTeams` 디렉티브에 전달하세요:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```