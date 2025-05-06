# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성](#writing-tasks)
    - [작업 정의](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크](#completion-hooks)
- [작업 실행](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 처리하기 위한 도구입니다. [Blade](/docs/{{version}}/blade) 스타일의 문법을 사용하여 배포, Artisan 명령 등 다양한 작업을 손쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제에서만 지원됩니다. 다만, [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows에서도 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

Envoy가 설치되면 애플리케이션의 `vendor/bin` 디렉토리에서 Envoy 실행 파일을 사용할 수 있습니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성

<a name="defining-tasks"></a>
### 작업 정의

작업(Task)은 Envoy의 기본 빌딩 블록으로, 작업이 호출될 때 원격 서버에서 실행되어야 할 셸 명령어를 정의합니다. 예를 들어, 애플리케이션의 모든 큐 워커 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일에 정의해야 합니다. 아래는 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위 예시에서 볼 수 있듯이, 파일 상단에 `@servers` 배열을 정의하여 작업 선언의 `on` 옵션으로 관련 서버를 지정할 수 있습니다. `@servers` 선언은 반드시 한 줄로 작성해야 합니다. 각 `@task` 선언 내에는 해당 작업 실행 시 서버에서 실행할 셸 명령을 작성합니다.

<a name="local-tasks"></a>
#### 로컬 작업

서버의 IP 주소를 `127.0.0.1`로 지정하면 스크립트를 로컬 컴퓨터에서 강제로 실행할 수 있습니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기

`@import` 지시어를 사용하면 다른 Envoy 파일의 스토리와 작업을 가져와서 사용할 수 있습니다. 가져온 후에는 마치 자신의 파일에 정의된 것처럼 해당 작업을 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버

Envoy를 사용하면 여러 서버에서 작업을 쉽게 실행할 수 있습니다. 먼저, `@servers` 선언에 추가 서버를 등록하세요. 각 서버는 고유한 이름을 가져야 합니다. 이후, 작업의 `on` 배열에 서버 이름을 나열하면 됩니다:

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

기본적으로 작업은 각 서버에 직렬로(순차적으로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 끝난 후에 다음 서버에서 실행이 시작됩니다. 여러 서버에서 병렬로 작업을 실행하려면, 작업 선언에 `parallel` 옵션을 추가하세요:

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

Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어로 작업 전에 실행할 PHP 코드 블록을 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 추가 PHP 파일이 필요하다면, `Envoy.blade.php` 파일 상단에서 `@include` 지시어로 파일을 불러올 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수

필요하다면, Envoy 작업 실행 시 커맨드 라인에서 인자를 넘길 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법을 사용하여 옵션을 참조할 수 있습니다. 또한, Blade의 `if` 문이나 반복문도 사용 가능합니다. 예를 들어 `git pull` 명령 실행 전 `$branch` 변수가 존재하는지 확인할 수 있습니다:

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

스토리(Story)는 여러 개의 작업을 하나의 편리한 이름으로 그룹화합니다. 예를 들어 `deploy`라는 스토리가 `update-code`와 `install-dependencies` 작업을 실행하도록 설정할 수 있습니다:

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

스토리를 작성한 후에는 개별 작업을 실행할 때와 동일하게 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 후크

작업과 스토리가 실행될 때 여러 종류의 후크가 실행됩니다. Envoy에서 지원하는 후크 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 후크에 포함된 모든 코드는 PHP로 해석되며, 로컬에서 실행되고 원격 서버에서는 실행되지 않습니다.

각 후크는 원하는 만큼 정의할 수 있으며, Envoy 스크립트에 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 작업 실행 전, Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 후크는 실행될 작업의 이름을 인자로 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

각 작업 실행 후, 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크도 실행된 작업의 이름을 인자로 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패했을 때(종료 상태 코드가 0보다 큰 경우) 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크도 실행된 작업의 이름을 인자로 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 에러 없이 성공적으로 실행된 경우, 등록된 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 실행된 후(종료 상태와 관계없이), 등록된 모든 `@finished` 후크가 실행됩니다. 이때 완료된 작업의 상태 코드를 인자로 받으며, 이 값은 `null`이거나 0 이상의 정수일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 일부 작업에서 에러가 발생했습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면, Envoy의 `run` 명령에 실행할 작업 또는 스토리 이름을 전달하세요. 작업 실행 중에 원격 서버의 출력 결과가 표시됩니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인

특정 작업을 실행하기 전에 한번 더 확인하고 싶다면, 작업 선언에 `confirm` 지시어를 추가하세요. 이 옵션은 위험한(파괴적인) 작업에 특히 유용합니다:

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

Envoy는 각 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 지시어는 Slack 훅 URL과 채널/사용자 이름을 받습니다. "Incoming WebHooks" 통합을 Slack 관리 패널에서 생성하면 Webhook URL을 얻을 수 있습니다.

`@slack` 지시어의 첫 번째 인자로 전체 Webhook URL을, 두 번째 인자로 채널 이름(`#channel`) 또는 사용자 이름(`@user`)을 입력하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 실행된 작업을 설명하는 메시지를 알림 채널로 보냅니다. 하지만, 세 번째 인자로 직접 메시지를 지정하여 이 메시지를 덮어쓸 수 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 각 작업 실행 후 [Discord](https://discord.com)로 알림 전송도 지원합니다. `@discord` 지시어는 Discord 훅 URL과 메시지를 받습니다. 서버 설정에서 "Webhook"을 생성한 후 어떤 채널에 알림을 보낼지 설정하고, 전체 Webhook URL을 `@discord` 지시어에 전달하세요:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 각 작업 실행 후 [Telegram](https://telegram.org)으로도 알림을 보낼 수 있습니다. `@telegram` 지시어는 Telegram Bot ID와 Chat ID를 받습니다. [BotFather](https://t.me/botfather)로 봇을 만들어 Bot ID를, [@username_to_id_bot](https://t.me/username_to_id_bot)으로 유효한 Chat ID를 확인할 수 있습니다. 둘 다 `@telegram` 지시어에 인자로 전달하세요:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 각 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로 알림 전송도 지원합니다. `@microsoftTeams` 지시어는 Teams Webhook(필수), 메시지, 테마 색상(success, info, warning, error), 그리고 옵션 배열을 받습니다. Teams Webhook은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 새로 생성해 얻을 수 있습니다. Teams API는 제목, 요약, 섹션 등 메시지 박스를 커스터마이징할 다양한 속성을 지원합니다. 자세한 내용은 [Microsoft Teams 공식 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인하세요. 전체 Webhook URL을 `@microsoftTeams` 지시어에 전달하면 됩니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
