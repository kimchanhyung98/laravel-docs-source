# Laravel Envoy (Laravel Envoy)

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [다중 서버](#multiple-servers)
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
## 소개 (Introduction)

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 공통 작업을 수행하기 위한 도구입니다. [Blade](/docs/9.x/blade) 스타일 문법을 사용하여 손쉽게 배포, Artisan 명령어 실행 등 작업을 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제에서만 지원되며, Windows 사용자는 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 통해 지원할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 통해 프로젝트에 Envoy를 설치합니다:

```shell
composer require laravel/envoy --dev
```

설치가 완료되면, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉토리에 위치합니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 작업 정의하기 (Defining Tasks)

작업은 Envoy의 기본 단위입니다. 작업은 호출 시 원격 서버에서 실행될 쉘 명령어를 정의합니다. 예를 들어, 애플리케이션의 큐 작업자 서버 전체에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

Envoy 작업은 모두 애플리케이션 루트의 `Envoy.blade.php` 파일에서 정의해야 합니다. 다음은 기본 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시에서 `@servers` 배열을 파일 상단에 한 줄로 정의했습니다. 이를 통해 작업 선언에서 `on` 옵션으로 해당 서버들을 참조할 수 있습니다. `@task` 내부에는 작업 실행 시 각 서버에서 실행할 쉘 명령어를 작성합니다.

<a name="local-tasks"></a>
#### 로컬 작업 (Local Tasks)

로컬 컴퓨터에서 스크립트를 실행하도록 강제하려면 서버 IP를 `127.0.0.1`로 지정하세요:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기 (Importing Envoy Tasks)

`@import` 지시어를 사용하여 다른 Envoy 파일을 가져올 수 있으며, 이 파일들의 스토리와 작업이 현재 파일에 추가됩니다. 가져온 작업들은 마치 본인의 Envoy 파일에 정의된 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버 (Multiple Servers)

Envoy는 여러 서버에 작업을 쉽게 실행할 수 있습니다. 먼저 `@servers` 선언에 추가 서버를 등록하세요. 각 서버는 고유한 이름을 가져야 합니다. 추가 정의한 서버는 작업의 `on` 배열에 나열해 지정할 수 있습니다:

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

기본적으로 작업은 각 서버에서 순차적으로 실행됩니다. 즉, 첫 서버에서 작업이 완료되어야 다음 서버에서 실행이 시작됩니다. 여러 서버에 병렬로 작업을 실행하고 싶다면 작업 선언에 `parallel` 옵션을 추가하세요:

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

Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어를 사용해 작업 실행 전에 실행할 PHP 코드를 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

추가로, 작업 실행 전에 필요한 PHP 파일을 불러오려면 `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용할 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

필요시, 명령어 실행 시 인수를 지정해 Envoy 작업에 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법으로 옵션 값을 사용할 수 있고, `if`문이나 반복문도 작성할 수 있습니다. 예를 들어, `$branch` 변수가 존재하는지 확인한 후 `git pull` 명령을 실행하는 방법은 다음과 같습니다:

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

스토리는 여러 작업을 하나의 편리한 이름 아래 묶는 기능입니다. 예를 들어, `deploy` 스토리는 `update-code`와 `install-dependencies` 작업을 순서대로 실행합니다:

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

스토리가 작성되면 작업 실행 방식과 동일하게 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

작업과 스토리가 실행될 때 여러 후크가 실행됩니다. Envoy가 지원하는 후크 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 후크 안의 코드는 모두 PHP로 해석되며 로컬에서 실행됩니다. 즉, 작업이 실행되는 원격 서버가 아니라 로컬에서 수행됩니다.

동일한 후크를 여러 개 정의할 수 있으며, 작성 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업 실행 전에, Envoy 스크립트 내 등록된 모든 `@before` 후크가 실행됩니다. 후크는 실행될 작업 이름을 전달받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후, 모든 `@after` 후크가 실행됩니다. 후크는 실행된 작업 이름을 전달받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업 실패 시(종료 코드가 0보다 큰 경우), 모든 `@error` 후크가 실행됩니다. 후크는 실패한 작업 이름을 전달받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되었을 때, 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

작업 실행이 종료되면, 종료 상태와 상관없이 모든 `@finished` 후크가 실행됩니다. 후크는 작업 종료 코드를 전달받는데, 값은 `null`이거나 0 이상의 정수입니다:

```blade
@finished
    if ($exitCode > 0) {
        // 작업 중 오류가 있었습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기 (Running Tasks)

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면 Envoy의 `run` 명령어를 사용하고 실행할 작업 또는 스토리 이름을 전달하세요. 실행 중 출력 결과가 원격 서버로부터 출력됩니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인 (Confirming Task Execution)

서버에서 특정 작업을 실행하기 전에 확인 메시지를 받고 싶으면 작업 선언에 `confirm` 옵션을 추가하세요. 특히 파괴적인 작업에 유용합니다:

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

Envoy는 작업이 실행된 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 웹후크 URL과 채널 또는 사용자명을 인수로 받습니다. 웹후크 URL은 Slack 제어판에서 "Incoming WebHooks" 통합을 생성하여 얻을 수 있습니다.

첫 번째 인수는 전체 웹후크 URL, 두 번째 인수는 채널명(`#channel`) 또는 사용자명(`@user`)입니다:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 실행된 작업 내용을 알림 메시지로 전송하지만, 세 번째 인수로 사용자 지정 메시지를 전달해 메시지를 덮어쓸 수 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 작업 실행 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹후크 URL과 메시지를 받습니다. 웹후크 URL은 Discord 서버 설정에서 "Webhook"을 생성하고 원하는 채널을 선택하여 얻을 수 있습니다. 전체 URL을 인수로 전달하세요:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 작업 실행 후 [Telegram](https://telegram.org)으로도 알림을 보낼 수 있습니다. `@telegram` 지시어는 Telegram Bot ID와 Chat ID를 받습니다. Bot ID는 [BotFather](https://t.me/botfather)를 통해 새 봇을 생성하여 얻고, 유효한 Chat ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)을 통해 얻을 수 있습니다. 두 인수를 전체로 전달하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)에도 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 Teams 웹후크(URL, 필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인수로 받습니다. Teams 웹후크는 새로운 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) 생성으로 얻습니다. 메시지 박스의 제목, 요약, 섹션 등 Teams API의 다양한 속성을 설정할 수 있습니다. 자세한 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 웹후크 URL을 인수로 전달하세요:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```