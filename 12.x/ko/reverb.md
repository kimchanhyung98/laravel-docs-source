# Laravel Reverb (Laravel Reverb)

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
    - [애플리케이션 인증 정보](#application-credentials)
    - [허용된 오리진](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [운영 환경에서 Reverb 실행](#production)
    - [오픈 파일 수](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 빠르고 확장성 높은 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 [이벤트 브로드캐스팅 도구](/docs/12.x/broadcasting)와도 매끄럽게 통합됩니다.

<a name="installation"></a>
## 설치

`install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다.

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 구성

`install:broadcasting` Artisan 명령어는 내부적으로 `reverb:install` 명령어를 실행하여, Reverb를 합리적인 기본 설정값과 함께 설치합니다. 설정을 변경하고 싶다면, Reverb의 환경 변수나 `config/reverb.php` 설정 파일을 수정하면 됩니다.

<a name="application-credentials"></a>
### 애플리케이션 인증 정보

Reverb에 연결하려면, 클라이언트와 서버 간에 Reverb "애플리케이션" 인증 정보를 교환해야 합니다. 이 인증 정보는 서버에 설정되며, 클라이언트의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용하여 이 인증 정보를 정의할 수 있습니다.

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 오리진

클라이언트 요청을 허용할 오리진(origin)을 `config/reverb.php` 설정 파일의 `apps` 섹션 내 `allowed_origins` 설정값을 수정하여 지정할 수 있습니다. 허용되지 않은 오리진에서의 모든 요청은 거부됩니다. 모든 오리진을 허용하려면 `*`를 사용할 수 있습니다.

```php
'apps' => [
    [
        'app_id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]
```

<a name="additional-applications"></a>
### 추가 애플리케이션

일반적으로 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 설치로 여러 애플리케이션을 동시에 서비스할 수도 있습니다.

예를 들어, 하나의 Laravel 애플리케이션이 여러 애플리케이션에 대해 Reverb를 통해 WebSocket 연결을 제공하고 싶을 수 있습니다. 이를 위해 애플리케이션의 `config/reverb.php` 설정 파일에서 여러 `apps`를 정의하면 됩니다.

```php
'apps' => [
    [
        'app_id' => 'my-app-one',
        // ...
    ],
    [
        'app_id' => 'my-app-two',
        // ...
    ],
],
```

<a name="ssl"></a>
### SSL

대부분의 경우, 안전한 WebSocket 연결은 요청이 Reverb 서버로 프록시되기 전에 상위 웹 서버(Nginx 등)에서 처리됩니다.

하지만, 예를 들어 로컬 개발 환경 등에서는 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 수 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/12.x/valet)에서 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행해 애플리케이션을 보안 처리했다면, 사이트에 대해 생성된 Herd 또는 Valet 인증서를 사용하여 Reverb 연결을 보호할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나, Reverb 서버를 시작할 때 명시적으로 호스트명 옵션을 전달하세요.

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd 및 Valet 도메인은 `localhost`로 해석되므로, 위와 같이 명령어를 실행하면 Reverb 서버를 `wss://laravel.test:8080`에서 안전한 WebSocket 프로토콜(`wss`)로 접근할 수 있게 됩니다.

또한, `config/reverb.php` 설정 파일의 `tls` 옵션을 통해 수동으로 인증서를 지정할 수도 있습니다. `tls` 옵션 배열 안에는 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 값을 제공할 수 있습니다.

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행

Reverb 서버는 `reverb:start` Artisan 명령어를 사용하여 시작할 수 있습니다.

```shell
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접근할 수 있습니다.

호스트 또는 포트를 직접 지정하려면 서버 시작 시 `--host` 및 `--port` 옵션을 사용할 수 있습니다.

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 설정 파일에서 `REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수를 지정할 수도 있습니다.

`REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST` 및 `REVERB_PORT`와 혼동해서는 안 됩니다. 전자는 Reverb 서버 자체가 동작할 호스트와 포트를 의미하며, 후자는 Laravel이 브로드캐스트 메시지를 어디로 보낼지 지정하는 값입니다. 예를 들어, 운영 환경에서는 공개 Reverb 호스트명(`ws.laravel.com`)의 443번 포트에서 요청을 받아 `0.0.0.0:8080`의 Reverb 서버로 라우팅할 수 있습니다. 이 경우 환경 변수 예시는 다음과 같습니다.

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능 향상을 위해 Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. Reverb 서버를 통과하는 데이터 흐름을 보고 싶다면, `reverb:start` 명령어에 `--debug` 옵션을 추가할 수 있습니다.

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 장시간 실행되는 프로세스이므로, 코드에 변경이 있어도 서버를 재시작해야 반영됩니다. 서버를 재시작하려면 `reverb:restart` Artisan 명령어를 실행하세요.

`reverb:restart` 명령은 모든 연결을 정상적으로 종료한 후 서버를 중지합니다. Supervisor와 같은 프로세스 관리자를 함께 사용하고 있다면, 모든 연결이 종료된 후 프로세스 관리자가 서버를 자동으로 다시 시작합니다.

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링

Reverb는 [Laravel Pulse](/docs/12.x/pulse)와의 통합을 통해 모니터링할 수 있습니다. Reverb의 Pulse 통합을 활성화하면, 서버가 처리하는 연결 수와 메시지 수를 추적할 수 있습니다.

이 통합을 활성화하려면 먼저 [Pulse를 설치](/docs/12.x/pulse#installation)했는지 확인해야 합니다. 이후, Reverb의 기록자(recorder)를 애플리케이션의 `config/pulse.php` 설정 파일에 추가하세요.

```php
use Laravel\Reverb\Pulse\Recorders\ReverbConnections;
use Laravel\Reverb\Pulse\Recorders\ReverbMessages;

'recorders' => [
    ReverbConnections::class => [
        'sample_rate' => 1,
    ],

    ReverbMessages::class => [
        'sample_rate' => 1,
    ],

    // ...
],
```

다음으로, 각 기록자에 해당하는 Pulse 카드를 [Pulse 대시보드](/docs/12.x/pulse#dashboard-customization)에 추가하세요.

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 일정 주기로 새 업데이트를 폴링하여 기록됩니다. 이 정보가 Pulse 대시보드에 올바르게 표시되기 위해서는, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. [수평 확장](#scaling) 구성에서 Reverb를 운영한다면, 이 데몬은 반드시 한 대의 서버에서만 실행해야 합니다.

<a name="production"></a>
## 운영 환경에서 Reverb 실행

WebSocket 서버의 특성상 장시간 실행되므로, Reverb 서버가 서버의 리소스에 맞는 최적의 연결 수를 효과적으로 처리할 수 있도록 서버와 호스팅 환경을 최적화해야 할 수 있습니다.

> [!NOTE]
> 사이트가 [Laravel Forge](https://forge.laravel.com)로 관리 중이라면, "Application" 패널에서 Reverb에 맞게 서버를 자동으로 최적화할 수 있습니다. Reverb 통합을 활성화하면, Forge가 필요한 확장 프로그램 설치, 연결 허용 수 증가 등 서버를 운영 환경에 맞게 자동 구성합니다.

<a name="open-files"></a>
### 오픈 파일 수

각 WebSocket 연결은 클라이언트나 서버가 연결을 끊을 때까지 메모리에 유지됩니다. 유닉스 및 유닉스 계열 환경에서는 각 연결이 파일로 표시됩니다. 그러나 운영 체제와 애플리케이션 수준 모두에서 열 수 있는 파일 수에 제한이 있을 수 있습니다.

<a name="operating-system"></a>
#### 운영 체제

유닉스 기반 운영 체제에서, `ulimit` 명령으로 열 수 있는 파일의 수를 확인할 수 있습니다.

```shell
ulimit -n
```

이 명령은 사용자별 허용된 파일 개수 제한 값을 보여줍니다. `/etc/security/limits.conf` 파일을 편집하여 값을 변경할 수 있습니다. 예를 들어, `forge` 사용자의 최대 오픈 파일 수를 10,000으로 늘리려면 다음과 같이 설정합니다.

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

Reverb는 내부적으로 WebSocket 연결 관리를 위해 ReactPHP 이벤트 루프를 사용합니다. 기본적으로는 추가 확장 없이 동작하는 `stream_select` 기반 이벤트 루프가 사용됩니다. 그러나 `stream_select`는 일반적으로 1,024개의 오픈 파일로 제한됩니다. 동시에 1,000개 이상의 연결을 처리하려면, 이 제한이 없는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 `ext-uv` 확장 프로그램이 설치되어 있으면 자동으로 해당 루프로 전환합니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다.

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 경우 Reverb는 서버의 웹 외부에서 접근할 수 없는 포트에서 동작합니다. 따라서 Reverb로 트래픽을 라우팅하려면 리버스 프록시 설정이 필요합니다. Reverb가 `0.0.0.0` 호스트와 `8080` 포트에서 동작하고, 서버가 Nginx 웹 서버를 사용하는 경우, 아래 Nginx 사이트 구성 예시처럼 리버스 프록시를 설정할 수 있습니다.

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://0.0.0.0:8080;
    }

    ...
}
```

> [!WARNING]
> Reverb는 `/app`에서 WebSocket 연결을, `/apps`에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버가 이 두 URI 모두를 서비스할 수 있는지 반드시 확인해야 합니다. [Laravel Forge](https://forge.laravel.com)로 서버를 관리하는 경우, 기본적으로 적절하게 Reverb 서버가 구성됩니다.

일반적으로 웹 서버는 과부하를 방지하기 위해 허용되는 연결 수에 제한을 둡니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면, `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 수정하세요.

```nginx
user forge;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
worker_rlimit_nofile 10000;

events {
  worker_connections 10000;
  multi_accept on;
}
```

위 구성은 프로세스당 최대 10,000개의 Nginx 워커를 생성할 수 있도록 해줍니다. 또한 Nginx의 오픈 파일 제한도 10,000으로 설정됩니다.

<a name="ports"></a>
### 포트

유닉스 기반 운영 체제에서는 하나의 서버에서 열 수 있는 포트의 수에도 제한이 있습니다. 아래 명령어로 현재 허용된 포트 범위를 확인할 수 있습니다.

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위와 같이 출력된 경우, 한 서버에서 최대 28,231개(60,999 - 32,768) 연결을 처리할 수 있습니다. 각 연결이 사용 가능한 포트를 필요로 하기 때문입니다. 더 많은 연결을 늘리고 싶다면, [수평 확장](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 설정 파일에서 허용된 포트 범위를 늘려 사용할 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우, Supervisor와 같은 프로세스 관리자를 사용해 Reverb 서버가 항상 실행 중임을 보장해야 합니다. Supervisor로 Reverb를 실행한다면, `supervisor.conf` 파일의 `minfds` 설정값도 수정하여 Supervisor가 연결 유지에 필요한 파일을 충분히 열 수 있도록 해야 합니다.

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

하나의 서버가 허용하는 연결 수 이상의 처리가 필요하다면, Reverb 서버를 수평 확장할 수 있습니다. Redis의 publish/subscribe 기능을 활용해, 여러 서버에 걸쳐 연결 관리를 할 수 있습니다. 애플리케이션의 Reverb 서버 중 한 곳에서 메시지를 수신하면, 해당 서버가 Redis를 통해 들어온 메시지를 다른 모든 서버로 브로드캐스트합니다.

수평 확장을 활성화하려면, 애플리케이션의 `.env` 파일에 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요.

```env
REVERB_SCALING_ENABLED=true
```

그리고 모든 Reverb 서버가 통신할 전용 중앙 Redis 서버를 준비해야 합니다. Reverb는 [애플리케이션의 기본 Redis 연결](/docs/12.x/redis#configuration)을 사용해 모든 Reverb 서버에 메시지를 게시합니다.

Reverb의 스케일링 옵션을 활성화하고 Redis 서버를 구성했다면, Redis와 통신 가능한 여러 서버에서 `reverb:start` 명령어를 실행하기만 하면 됩니다. 이 Reverb 서버들은 로드 밸런서 뒤에 두어, 모든 요청이 여러 서버로 고르게 분산되도록 해야 합니다.

<a name="events"></a>
## 이벤트

Reverb는 연결 및 메시지 처리 과정에서 내부적으로 다양한 이벤트를 발생시킵니다. 이 이벤트들에 [리스너를 등록](/docs/12.x/events)하여 연결 관리, 메시지 교환 시 필요한 동작을 수행할 수 있습니다.

Reverb가 발생시키는 주요 이벤트는 다음과 같습니다.

#### `Laravel\Reverb\Events\ChannelCreated`

채널이 생성될 때 발생합니다. 이는 일반적으로 특정 채널에 첫 번째 연결이 구독할 때 발생합니다. 이벤트에는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스가 전달됩니다.

#### `Laravel\Reverb\Events\ChannelRemoved`

채널이 제거될 때 발생합니다. 일반적으로 마지막 연결이 채널 구독을 취소할 때 발생하며, 이벤트에는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스가 전달됩니다.

#### `Laravel\Reverb\Events\ConnectionPruned`

서버에서 만료된 연결(stale connection)이 정리될 때 발생합니다. 이벤트에는 `Laravel\Reverb\Contracts\Connection` 인스턴스가 전달됩니다.

#### `Laravel\Reverb\Events\MessageReceived`

클라이언트 연결로부터 메시지가 수신될 때 발생합니다. 이벤트에는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`가 전달됩니다.

#### `Laravel\Reverb\Events\MessageSent`

클라이언트 연결로 메시지를 보낼 때 발생합니다. 이벤트에는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`가 전달됩니다.
