# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성하기](#writing-tasks)
    - [작업 정의하기](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [훅](#completion-hooks)
- [작업 실행하기](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업을 손쉽게 실행할 수 있도록 도와주는 도구입니다. [Blade](/docs/{{version}}/blade) 스타일의 문법을 이용해 배포, Artisan 명령어 등의 작업을 간단하게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 공식적으로 지원합니다. 하지만 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows 환경에서도 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 이용해 프로젝트에 Envoy를 설치하세요:

```shell
composer require laravel/envoy --dev
```

Envoy 설치가 완료되면, Envoy 바이너리가 애플리케이션의 `vendor/bin` 디렉토리에 생성됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## 작업 작성하기

<a name="defining-tasks"></a>
### 작업 정의하기

작업(Task)은 Envoy의 기본 빌딩 블록입니다. 작업은 호출 시 원격 서버에서 실행될 셸 명령어들을 정의합니다. 예를 들어, 모든 작업자 서버에서 `php artisan queue:restart` 명령어를 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트의 `Envoy.blade.php` 파일에 정의해야 합니다. 시작 예시는 다음과 같습니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

위에서 볼 수 있듯이, 파일 최상단에 `@servers` 배열을 정의하여 작업 선언시 `on` 옵션을 통해 서버를 참조할 수 있도록 합니다. `@servers` 선언은 항상 한 줄로 작성해야 합니다. `@task` 선언문 내부에는 작업이 호출될 때 서버에서 실행될 셸 명령어들을 넣습니다.

<a name="local-tasks"></a>
#### 로컬 작업

서버의 IP 주소를 `127.0.0.1`로 지정하면 작업을 로컬 컴퓨터에서 강제로 실행할 수 있습니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 가져오기

`@import` 지시어를 사용하면 다른 Envoy 파일을 가져와서 해당 스토리와 작업을 사용할 수 있습니다. 파일을 가져온 후에는, 가져온 Envoy 파일에 정의된 작업을 자신의 Envoy 파일에서 정의한 것처럼 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버

Envoy를 이용하면 여러 서버에서 동시에 작업을 실행할 수 있습니다. 먼저, `@servers` 선언에 추가할 서버를 정의해야 하며 각 서버에 고유 이름을 지정해야 합니다. 서버를 추가로 정의한 뒤 작업의 `on` 배열에 실행할 서버들을 나열하면 됩니다:

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

기본적으로 작업은 각 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 완료된 후에야 두 번째 서버에서 작업이 실행됩니다. 여러 서버에서 작업을 병렬로 실행하고 싶다면 `parallel` 옵션을 작업 선언에 추가하세요:

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

특정 Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어를 사용하면 작업들 전에 실행될 PHP 코드를 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 다른 PHP 파일을 불러와야 하는 경우, `Envoy.blade.php` 파일 상단에서 `@include` 지시어를 사용하세요:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수

필요에 따라 Envoy 작업에 인수를 전달할 수 있습니다. 이를 위해 Envoy 실행 시 커맨드 라인에서 변수 값을 지정하세요:

```shell
php vendor/bin/envoy run deploy --branch=master
```

작업 내에서는 Blade의 "echo" 문법을 사용해 옵션 값을 접근할 수 있습니다. 또한 작업 내에서 Blade의 `if` 문이나 반복문도 사용할 수 있습니다. 예를 들어, `$branch` 변수가 존재하는지 확인한 후 `git pull` 명령어를 실행할 수 있습니다:

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

스토리(Story)는 여러 작업(Task)을 하나의 이름으로 묶어서 사용할 수 있게 해주는 기능입니다. 예를 들어, `deploy` 스토리는 `update-code`와 `install-dependencies` 작업을 정의 내에 나열해 실행할 수 있습니다:

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

스토리를 작성한 후에는 일반 작업과 동일하게 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### 훅

작업과 스토리가 실행될 때 여러 훅(Hook)이 동작합니다. Envoy에서 지원하는 훅 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 훅들 안의 코드는 모두 PHP로 해석되며, 원격 서버가 아닌 로컬에서 실행됩니다.

각 타입의 훅은 원하는 만큼 여러 개 정의할 수 있으며, Envoy 스크립트에서 등장하는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 작업 실행 전에 Envoy 스크립트에 등록된 모든 `@before` 훅이 실행됩니다. `@before` 훅에서는 실행될 작업의 이름을 인수로 받을 수 있습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

각 작업 실행 후 Envoy 스크립트에 등록된 모든 `@after` 훅이 실행됩니다. `@after` 훅에서는 실행된 작업의 이름을 인수로 받을 수 있습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패(종료 코드 0보다 큼)할 경우, 모든 `@error` 훅이 실행됩니다. `@error` 훅에는 실행된 작업의 이름이 전달됩니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행된 경우, 스크립트에 등록된 모든 `@success` 훅이 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 종료된 이후(상태와 관계없이), `@finished` 훅들이 실행됩니다. `@finished` 훅에서는 완료된 작업의 상태 코드를 사용할 수 있으며, 이는 `null`이거나 0 이상의 정수일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // 어느 한 작업에서 오류가 발생했습니다...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업 또는 스토리를 실행하려면 Envoy의 `run` 명령에 실행할 작업이나 스토리의 이름을 전달하면 됩니다. Envoy는 각 서버의 출력 결과를 실시간으로 표시해줍니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### 작업 실행 확인

특정 작업을 서버에서 실행하기 전에 확인 메시지를 받고 싶으면, 해당 작업 선언에 `confirm` 디렉티브를 추가하세요. 이 옵션은 파괴적인(위험한) 작업 시 특히 유용합니다:

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

Envoy는 각 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 디렉티브는 Slack 훅 URL과 채널/사용자명을 인수로 받습니다. Slack 제어판에서 "Incoming WebHooks" 통합을 생성해 웹훅 URL을 얻을 수 있습니다.

첫 번째 인수에는 전체 웹훅 URL을, 두 번째 인수에는 채널명(`#channel`) 또는 사용자명(`@user`)을 전달하세요:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

기본적으로 Envoy 알림은 실행된 작업에 대해 설명하는 메시지를 알림 채널에 보냅니다. 직접 메시지를 지정하려면, 세 번째 인수에 메시지를 입력하면 됩니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### Discord

Envoy는 [Discord](https://discord.com)로의 알림 발송도 지원합니다. `@discord` 디렉티브는 Discord 훅 URL과 메시지를 인수로 받습니다. 서버 설정(Server Settings)에서 "Webhook"을 생성하고, 게시할 채널을 선택해 웹훅 URL을 얻으세요. 이 URL을 `@discord` 디렉티브의 인수로 전달합니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### Telegram

Envoy는 [Telegram](https://telegram.org) 알림도 지원합니다. `@telegram` 디렉티브는 Telegram 봇 ID와 챗 ID를 인수로 받습니다. [BotFather](https://t.me/botfather)를 이용해 새 봇을 생성하면 봇 ID를 확인할 수 있습니다. [@username_to_id_bot](https://t.me/username_to_id_bot)에서 챗 ID를 얻으세요. 두 값을 다음과 같이 전달합니다:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로의 알림도 지원합니다. `@microsoftTeams` 디렉티브는 Teams 웹훅(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인수로 받습니다. [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성해 Teams 웹훅을 얻으세요. Teams API는 메시지 박스의 제목, 요약, 섹션 등의 추가 속성도 지원합니다. 자세한 사항은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인하세요. 받은 웹훅 URL을 아래와 같이 전달합니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
