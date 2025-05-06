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
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 수행하는 작업들을 실행하기 위한 도구입니다. [Blade](/docs/{{version}}/blade) 스타일의 문법을 사용하여 배포, Artisan 명령어 실행 등 다양한 작업을 손쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영 체제만을 지원합니다. 하지만 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows 환경에서도 지원이 가능합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용하여 프로젝트에 Envoy를 설치하세요:

    composer require laravel/envoy --dev

Envoy가 설치되면, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉터리 내에 위치하게 됩니다:

    php vendor/bin/envoy

<a name="writing-tasks"></a>
## 작업 작성하기

<a name="defining-tasks"></a>
### 작업 정의하기

작업(task)은 Envoy의 기본 구성 단위입니다. 작업은 작업이 실행될 때 원격 서버에서 실행될 셸 명령어를 정의합니다. 예를 들어, 모든 큐 워커 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일 내에 정의해야 합니다. 아래는 예시입니다:

```bash
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

보시다시피, 파일 상단에는 `@servers` 배열이 정의되어 있으며, 작업 선언에서 `on` 옵션을 통해 이러한 서버를 참조할 수 있습니다. `@servers` 선언은 반드시 한 줄에 작성해야 합니다. `@task` 선언 내부에는 작업이 실행될 때 서버에서 수행할 셸 명령어를 작성합니다.

<a name="local-tasks"></a>
#### 로컬 작업

서버의 IP 주소를 `127.0.0.1`로 지정하면 스크립트를 로컬 컴퓨터에서 강제로 실행할 수 있습니다:

```bash
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy 작업 임포트

`@import` 디렉티브를 사용하면, 다른 Envoy 파일을 불러와 해당 스토리 및 작업을 사용할 수 있습니다. 파일이 임포트된 후에는 해당 파일의 작업을 내 Envoy 파일에서 직접 정의한 것처럼 실행할 수 있습니다:

```bash
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 다중 서버

Envoy는 한 번에 여러 서버에서 작업을 쉽게 실행할 수 있도록 해줍니다. 우선 `@servers` 선언에 추가 서버를 등록하세요. 각 서버에 고유한 이름을 지정해야 합니다. 서버를 등록한 뒤에는 작업의 `on` 배열에 각 서버명을 나열해주면 됩니다:

```bash
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
#### 병렬 실행

기본적으로, 작업은 각 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 모두 끝난 후에 다음 서버에서 작업이 시작됩니다. 여러 서버에서 작업을 병렬로 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 추가하면 됩니다:

```bash
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
### 설정

때때로 Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 수 있습니다. `@setup` 디렉티브를 사용하면, 작업 실행 전에 실행할 PHP 코드 블록을 정의할 수 있습니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

작업 실행 전에 다른 PHP 파일을 불러올 필요가 있다면, `Envoy.blade.php` 파일 상단에서 `@include` 디렉티브를 사용할 수 있습니다:

```bash
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 변수

필요하다면, Envoy 작업을 실행할 때 명령줄에서 인수를 지정할 수 있습니다:

    php vendor/bin/envoy run deploy --branch=master

이렇게 설정한 옵션은 작업 내에서 Blade의 "echo" 문법으로 접근할 수 있습니다. 또한, 작업 내에서 Blade의 `if` 문 및 루프를 사용할 수도 있습니다. 예를 들어 `git pull` 명령을 실행하기 전에 `$branch` 변수가 존재하는지 확인할 수도 있습니다:

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
### 스토리

스토리(story)는 여러 작업을 하나의 편리한 이름 아래에 묶어서 관리할 수 있게 해줍니다. 예를 들어, `deploy`라는 스토리에서 `update-code`와 `install-dependencies` 작업을 함께 실행할 수 있습니다:

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

스토리를 작성한 이후에는, 작업을 호출하는 것과 동일하게 스토리를 실행할 수 있습니다:

    php vendor/bin/envoy run deploy

<a name="completion-hooks"></a>
### 후크(Hooks)

작업과 스토리가 실행될 때 여러 후크가 실행됩니다. Envoy가 지원하는 후크 유형은 `@before`, `@after`, `@error`, `@success`, `@finished` 입니다. 이 후크에 작성한 코드는 모두 PHP로 해석되어 로컬에서 실행되며, 원격 서버에서는 실행되지 않습니다.

각 후크는 원하는 만큼 정의할 수 있으며, Envoy 스크립트 내에서 작성한 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 작업 실행 전에, Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 후크는 실행될 작업의 이름을 전달받습니다:

```php
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

각 작업 실행 후에는 Envoy 스크립트에 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크는 실행된 작업의 이름을 전달받습니다:

```php
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

작업이 실패할 때(종료 코드가 0보다 큰 경우)마다, Envoy 스크립트에 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크는 실행된 작업의 이름을 전달받습니다:

```php
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되면, Envoy 스크립트에 등록된 모든 `@success` 후크가 실행됩니다:

```bash
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 실행된 후(종료 코드와 관계없이), 모든 `@finished` 후크가 실행됩니다. `@finished` 후크는 완료된 작업의 종료 코드(또는 `null`, 0 이상의 `integer`)를 전달받습니다:

```bash
@finished
    if ($exitCode > 0) {
        // 일부 작업에서 오류 발생...
    }
@endfinished
```

<a name="running-tasks"></a>
## 작업 실행하기

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업 또는 스토리를 실행하려면, Envoy의 `run` 명령에 원하는 작업 또는 스토리 이름을 전달하여 실행하세요. Envoy는 작업을 실행하고 원격 서버의 출력을 중계합니다:

    php vendor/bin/envoy run deploy

<a name="confirming-task-execution"></a>
### 작업 실행 확인

특정 작업을 서버에서 실행하기 전에 실행 여부를 확인 받고 싶다면, 작업 선언에 `confirm` 지시문을 추가하면 됩니다. 이 옵션은 파괴적인 작업에 특히 유용합니다:

```bash
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

Envoy는 각 작업 실행 후 [Slack](https://slack.com)으로 알림을 보낼 수 있습니다. `@slack` 디렉티브는 Slack 웹훅 URL과 채널/유저 이름을 인자로 받습니다. 웹훅 URL은 Slack 관리 패널에서 "Incoming WebHooks" 통합을 생성하여 얻을 수 있습니다.

전체 웹훅 URL을 첫 번째 인자로, 두 번째 인자로는 채널명 (`#channel`) 혹은 유저명 (`@user`)을 전달해야 합니다:

    @finished
        @slack('webhook-url', '#bots')
    @endfinished

기본적으로 Envoy 알림은 작업 실행 내역을 알림 채널로 전송합니다. 하지만 세 번째 인자에 메시지를 지정하여 알림 메시지를 원하는 내용으로 덮어쓸 수 있습니다:

    @finished
        @slack('webhook-url', '#bots', 'Hello, Slack.')
    @endfinished

<a name="discord"></a>
### Discord

Envoy는 각 작업 실행 후 [Discord](https://discord.com)로도 알림을 보낼 수 있습니다. `@discord` 디렉티브는 Discord 웹훅 URL과 메시지를 인자로 받습니다. 웹훅 URL은 Discord 서버의 "Webhook"을 생성해 원하는 채널에 설정한 후 얻을 수 있습니다:

    @finished
        @discord('discord-webhook-url')
    @endfinished

<a name="telegram"></a>
### Telegram

Envoy는 각 작업 실행 후 [Telegram](https://telegram.org)으로도 알림을 보낼 수 있습니다. `@telegram` 디렉티브는 텔레그램 봇 ID와 챗 ID를 인자로 받습니다. [BotFather](https://t.me/botfather)로 봇을 생성하면 Bot ID를, [@username_to_id_bot](https://t.me/username_to_id_bot)으로 챗 ID를 얻을 수 있습니다. 이 두 값을 모두 인자로 전달해야 합니다:

    @finished
        @telegram('bot-id','chat-id')
    @endfinished

<a name="microsoft-teams"></a>
### Microsoft Teams

Envoy는 각 작업 실행 후 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 알림을 보낼 수 있습니다. `@microsoftTeams` 디렉티브는 Teams 웹훅(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인자로 받습니다. [새로운 인커밍 웹훅](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성해 Teams 웹훅을 얻을 수 있습니다. Teams API는 제목, 요약, 섹션 등 알림 박스 커스텀을 위한 다양한 속성을 제공합니다. 자세한 사항은 [Microsoft Teams 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하세요. 전체 웹훅 URL을 `@microsoftTeams` 디렉티브에 전달하면 됩니다:

    @finished
        @microsoftTeams('webhook-url')
    @endfinished