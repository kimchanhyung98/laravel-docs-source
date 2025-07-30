# Laravel Envoy

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

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 수행하는 일반적인 작업을 실행하기 위한 도구입니다. [Blade](/docs/11.x/blade) 스타일의 문법을 사용하여 배포, Artisan 명령어 실행 등 다양한 작업을 간편하게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영 체제만 지원합니다. 다만 Windows 사용자는 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 활용하여 실행할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 통해 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

설치가 완료되면 Envoy 실행 파일이 애플리케이션 `vendor/bin` 디렉토리에 위치합니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기 (Writing Tasks)

<a name="defining-tasks"></a>
### 작업 정의하기 (Defining Tasks)

작업(Task)은 Envoy의 기본 구성 요소입니다. 작업은 호출될 때 원격 서버에서 실행할 셸 명령을 정의합니다. 예를 들어, 애플리케이션의 모든 큐 작업자 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 `Envoy.blade.php` 파일에 정의해야 합니다. 다음은 시작을 위한 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위처럼 파일 상단에 `@servers` 배열을 정의하고, 작업 내에서는 `on` 옵션을 통해 참조할 서버를 지정할 수 있습니다. `@servers` 선언은 항상 한 줄에 작성되어야 하며, 각 `@task` 블록 안에는 작업 호출 시 서버에서 실행할 셸 명령들을 위치시킵니다.

<a name="local-tasks"></a>
#### 로컬 작업 (Local Tasks)

`127.0.0.1` IP를 서버 주소로 지정하면 스크립트를 로컬 컴퓨터에서 강제로 실행할 수 있습니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기 (Importing Envoy Tasks)

`@import` 지시어를 사용해 다른 Envoy 파일을 임포트하면, 해당 파일의 스토리와 작업들이 현재 파일에 추가됩니다. 이후 임포트한 작업들을 마치 자신의 Envoy 파일에 정의된 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버 (Multiple Servers)

Envoy는 여러 서버에서 작업을 쉽게 실행할 수 있습니다. 우선 `@servers` 선언에 추가 서버를 등록하세요. 각 서버에는 고유한 이름을 지정해야 합니다. 작업 선언 시 `on` 옵션을 배열로 정의하여 여러 서버를 나열할 수 있습니다:

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

기본적으로 작업은 각 서버에서 순차적으로 실행됩니다. 즉, 첫 번째 서버에서 작업이 끝나야 두 번째 서버에서 실행이 시작됩니다. 여러 서버에서 작업을 병렬로 실행하려면 작업 선언에 `parallel` 옵션을 `true`로 추가하세요:

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

가끔 Envoy 작업 실행 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어를 사용해 작업 전에 실행할 PHP 코드를 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 다른 PHP 파일을 불러와야 한다면, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용할 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수 (Variables)

필요 시 Envoy 작업에 인수를 전달할 수 있습니다. Envoy를 실행할 때 커맨드라인에서 옵션을 지정하세요:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내부에서는 Blade의 출력 구문을 사용하여 옵션에 접근할 수 있습니다. 또한 Blade의 조건문과 반복문도 작업 내에서 사용할 수 있습니다. 예를 들어, `git pull` 명령을 실행하기 전에 `$branch` 변수가 존재하는지 확인할 수 있습니다:

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

스토리는 여러 작업을 하나의 편리한 이름으로 묶어줍니다. 예를 들어 `deploy` 스토리는 `update-code`와 `install-dependencies` 작업들을 지정해 한꺼번에 실행하도록 할 수 있습니다:

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

스토리를 작성한 뒤에는 작업과 같은 방식으로 실행할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크 (Hooks)

작업이나 스토리가 실행될 때, 여러 후크들이 실행됩니다. Envoy가 지원하는 후크는 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 후크들 내부의 코드는 모두 PHP로 해석되며, 원격 서버가 아닌 로컬에서 실행됩니다.

각 후크는 여러 번 정의할 수 있으며, 스크립트 내에 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

작업이 실행되기 전에 모든 `@before` 후크가 실행됩니다. 후크는 실행할 작업의 이름을 인수로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

작업 실행 후, 등록된 모든 `@after` 후크가 실행됩니다. 후크는 실행이 완료된 작업 이름을 인수로 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패할 경우(종료 코드가 0보다 클 경우) 모든 `@error` 후크가 실행됩니다. 후크는 실패한 작업 이름을 인수로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되면 등록된 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

작업 실행이 모두 끝나면(종료 상태와 관계없이) 모든 `@finished` 후크가 실행됩니다. 이 후크는 완료된 작업의 종료 코드를 인수로 받으며, 값은 `null`이거나 `0` 이상인 정수일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 작업 중 오류가 있었습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기 (Running Tasks)

애플리케이션에 정의된 `Envoy.blade.php` 파일 내 작업 또는 스토리를 실행하려면 Envoy의 `run` 명령어를 사용하며, 실행할 작업 또는 스토리 이름을 전달하세요. Envoy는 작업을 실행하면서 원격 서버의 출력 내용을 실시간으로 보여줍니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인 (Confirming Task Execution)

특정 작업을 실행하기 전에 사용자 확인을 받고 싶다면, 작업 선언에 `confirm` 옵션을 추가하세요. 이 옵션은 특히 파괴적인 작업에 유용합니다:

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

Envoy는 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 웹훅 URL과 채널 또는 사용자 이름을 인수로 받습니다. 웹훅 URL은 Slack 제어판에서 "Incoming WebHooks" 통합을 생성하여 얻을 수 있습니다.

첫 번째 인수는 전체 웹훅 URL이며, 두 번째 인수는 채널명(`#channel`)이나 사용자명(`@user`)이어야 합니다:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 실행된 작업에 대한 메시지를 자동으로 전송합니다. 그러나 세 번째 인수로 직접 메시지를 지정할 수도 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 작업 실행 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹훅 URL과 메시지를 인수로 받습니다. 웹훅 URL은 Discord 서버 설정에서 "Webhook"을 생성하고 해당 채널을 지정하여 얻을 수 있습니다. 전체 웹훅 URL을 전달해야 합니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 작업 실행 후 [Telegram](https://telegram.org)으로 알림을 보낼 수 있습니다. `@telegram` 지시어는 Telegram 봇 ID와 채팅 ID를 인수로 받습니다. 봇 ID는 [BotFather](https://t.me/botfather)를 통해 새 봇을 만들 때 얻을 수 있으며, 채팅 ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)을 통해 확인할 수 있습니다. 두 값을 모두 넘겨야 합니다:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 알림을 보낼 수 있습니다. `@microsoftTeams` 지시어는 Teams 웹훅 URL(필수), 메시지, 테마 색상(success, info, warning, error), 그리고 옵션 배열을 인수로 받습니다. Teams 웹훅 URL은 [incoming webhook 생성 방법](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 참고하여 얻을 수 있습니다. Teams API는 제목, 요약, 섹션 등 메시지 박스를 사용자화할 수 있는 다양한 속성을 지원하며, 자세한 내용은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 웹훅 URL을 넘겨야 합니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```