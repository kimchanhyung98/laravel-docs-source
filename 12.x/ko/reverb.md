# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
    - [애플리케이션 자격증명](#application-credentials)
    - [허용된 오리진](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션 환경에서 Reverb 실행](#production)
    - [오픈 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 빠르고 확장 가능한 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 [이벤트 브로드캐스팅 도구](/docs/{{version}}/broadcasting)와 원활하게 통합됩니다.

<a name="installation"></a>
## 설치

`install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 구성

내부적으로 `install:broadcasting` Artisan 명령어는 `reverb:install` 명령을 실행하여 합리적인 기본 구성 옵션으로 Reverb를 설치합니다. 구성을 변경하려는 경우, Reverb의 환경 변수 또는 `config/reverb.php` 설정 파일을 업데이트하여 변경할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격증명

Reverb에 연결하기 위해서는 클라이언트와 서버 간에 Reverb "애플리케이션" 자격증명이 교환되어야 합니다. 이 자격증명은 서버에서 설정되며, 클라이언트의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용하여 자격증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 오리진

클라이언트 요청의 출처로 허용할 오리진은 `config/reverb.php` 파일의 `apps` 섹션 내 `allowed_origins` 설정 값을 업데이트하여 정의할 수 있습니다. 허용되지 않은 오리진에서 오는 모든 요청은 거부됩니다. 모든 오리진을 허용하려면 `*`를 사용할 수 있습니다:

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

일반적으로 Reverb는 설치된 애플리케이션을 위한 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 설치로 여러 애플리케이션을 지원할 수도 있습니다.

예를 들어, 단일 Laravel 애플리케이션이 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하도록 만들고 싶을 수 있습니다. 이는 애플리케이션의 `config/reverb.php` 설정 파일에 여러 `apps`를 정의함으로써 가능합니다:

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

대부분의 경우, 보안 WebSocket 연결은 상위 웹 서버(Nginx 등)에 의해 처리된 다음 요청이 Reverb 서버로 프록시됩니다.

그러나 로컬 개발 중과 같이 Reverb 서버가 보안 연결을 직접 처리해야 할 때도 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/{{version}}/valet)를 사용하고 있고, 애플리케이션에 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행한 경우, 사이트에 대해 생성된 Herd/Valet 인증서를 사용하여 Reverb 연결을 보안할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나, Reverb 서버를 시작할 때 명시적으로 호스트 옵션을 전달하면 됩니다:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되므로, 위 명령을 실행하면 Reverb 서버는 보안 WebSocket 프로토콜(`wss`)을 통해 `wss://laravel.test:8080`에서 접근할 수 있습니다.

또한, 애플리케이션의 `config/reverb.php` 설정 파일에 `tls` 옵션을 정의하여 인증서를 직접 선택할 수도 있습니다. `tls` 옵션 배열 내에는 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 인증서 옵션 중 원하는 값을 사용할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행

Reverb 서버는 `reverb:start` Artisan 명령어로 시작할 수 있습니다:

```shell
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되어 모든 네트워크 인터페이스에서 접근할 수 있습니다.

커스텀 호스트나 포트를 지정하려면 서버 시작 시 `--host` 및 `--port` 옵션을 사용하세요:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST` 및 `REVERB_PORT`와 혼동해서는 안 됩니다. 전자는 Reverb 서버 자체가 실행될 호스트와 포트를 지정하며, 후자는 Laravel이 브로드캐스트 메시지를 보낼 위치를 지정합니다. 예를 들어, 프로덕션 환경에서 public Reverb 호스트네임(포트 443)에서 요청을 받아 Reverb 서버(0.0.0.0:8080)로 라우팅할 수 있습니다. 이 경우 환경 변수는 다음과 같이 설정합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능 향상을 위해, Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. Reverb 서버를 통해 전송되는 데이터 스트림을 확인하려면 `reverb:start` 명령어에 `--debug` 옵션을 제공하세요:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 장기 실행 프로세스이므로, 코드 변경 사항이 반영되려면 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 서버를 중지하기 전에 모든 연결을 정상적으로 종료합니다. Supervisor와 같은 프로세스 관리자를 사용하여 Reverb를 실행 중이라면, 모든 연결이 종료된 후 프로세스 관리자가 자동으로 서버를 재시작합니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링

Reverb는 [Laravel Pulse](/docs/{{version}}/pulse)와의 통합을 통해 모니터링 할 수 있습니다. Reverb의 Pulse 통합을 활성화하면 서버에서 처리되는 연결 및 메시지 수를 추적할 수 있습니다.

통합을 활성화하려면 먼저 [Pulse를 설치](/docs/{{version}}/pulse#installation)해야 합니다. 그런 다음, Reverb의 리코더를 애플리케이션의 `config/pulse.php` 설정 파일에 추가하세요:

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

다음으로, 각 리코더의 Pulse 카드를 [Pulse 대시보드](/docs/{{version}}/pulse#dashboard-customization)에 추가하세요:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. 이 정보가 Pulse 대시보드에 올바르게 표시되도록 하려면 Reverb 서버에서 반드시 `pulse:check` 데몬을 실행해야 합니다. [수평 확장](#scaling) 구성으로 Reverb를 실행 중인 경우 이 데몬은 서버 중 하나에서만 실행하면 됩니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행

WebSocket 서버는 장기 실행 프로세스이기 때문에, 서버가 보유한 리소스에서 가능한 최적의 연결 수를 효율적으로 처리할 수 있도록 서버 및 호스팅 환경에서 몇 가지 최적화가 필요할 수 있습니다.

> [!NOTE]
> 사이트가 [Laravel Forge](https://forge.laravel.com)로 관리되는 경우, "애플리케이션" 패널에서 Reverb 최적화를 자동으로 적용할 수 있습니다. Reverb 통합을 활성화하면 Forge가 필요한 확장 설치와 연결 수 제한 증가 등, 서버를 프로덕션 환경에 맞게 최적화해줍니다.

<a name="open-files"></a>
### 오픈 파일

각 WebSocket 연결은 클라이언트나 서버에서 분리될 때까지 메모리상에 유지됩니다. 유닉스 및 유사 유닉스 환경에서는 각 연결이 파일로 표시됩니다. 하지만 운영체제, 애플리케이션 모두 오픈 파일 수에 대한 제한이 있습니다.

<a name="operating-system"></a>
#### 운영체제

유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 오픈 파일 수를 확인할 수 있습니다:

```shell
ulimit -n
```

이 명령어는 서로 다른 사용자에 허용된 오픈 파일 제한을 표시합니다. `/etc/security/limits.conf` 파일을 편집하여 값을 변경할 수 있습니다. 예를 들어, `forge` 사용자의 최대 오픈 파일 수를 10,000으로 업데이트하려면 다음과 같이 합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용해 서버의 WebSocket 연결을 관리합니다. 기본적으로 이 이벤트 루프는 추가 확장 없이 사용 가능한 `stream_select`로 구동됩니다. 하지만 `stream_select`는 일반적으로 1,024개의 오픈 파일로 제한됩니다. 따라서 1,000개 이상의 동시 연결을 처리하려면 동일한 제한에 얽매이지 않는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 `ext-uv` 확장이 사용 가능할 때 자동으로 해당 이벤트 루프를 사용합니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 경우, Reverb는 서버의 웹에 직접 노출되지 않는 포트에서 실행됩니다. 따라서 트래픽을 Reverb로 라우팅하려면 리버스 프록시를 구성해야 합니다. Reverb가 호스트 `0.0.0.0`, 포트 `8080`에서 실행 중이고, 서버가 Nginx 웹 서버를 사용한다면 다음과 같은 Nginx 사이트 설정으로 Reverb 서버를 위한 리버스 프록시를 정의할 수 있습니다:

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
> Reverb는 `/app`에서 WebSocket 연결을 받고, `/apps`에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버가 이 두 URI 모두를 서빙할 수 있는지 확인하세요. [Laravel Forge](https://forge.laravel.com)로 서버를 관리하는 경우, Reverb 서버는 기본적으로 올바르게 설정됩니다.

일반적으로, 웹 서버는 서버 과부하를 방지하기 위해 허용된 연결 수를 제한합니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 업데이트하세요:

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

위 설정은 프로세스당 최대 10,000개의 Nginx 작업자(worker)를 허용합니다. 또한 Nginx의 오픈 파일 제한도 10,000으로 설정합니다.

<a name="ports"></a>
### 포트

유닉스 기반 운영체제는 서버에서 열 수 있는 포트 수를 제한할 수 있습니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력은 서버가 최대 28,231(60,999 - 32,768)개의 연결을 처리할 수 있음을 보여줍니다(각 연결이 하나의 포트를 필요로 하므로). 연결 수를 늘리려면 [수평 확장](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 설정 파일에서 포트 범위를 업데이트하여 사용할 수 있는 포트 수를 증가시킬 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우, Supervisor와 같은 프로세스 관리자를 사용하여 Reverb 서버가 계속 실행되도록 해야 합니다. Supervisor로 Reverb를 관리한다면, 서버의 `supervisor.conf` 파일에서 `minfds` 설정을 변경해 Supervisor가 Reverb 서버 연결에 필요한 파일을 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

단일 서버에서 허용하는 것보다 더 많은 연결을 처리해야 한다면, Reverb 서버를 수평적으로 확장할 수 있습니다. Redis의 퍼블리시/구독(publish/subscribe) 기능을 활용하여 Reverb는 여러 서버에 걸쳐 연결을 관리할 수 있습니다. 애플리케이션의 Reverb 서버 중 하나가 메시지를 수신하면, 해당 서버는 Redis를 사용해 들어오는 메시지를 모든 다른 서버로 전파합니다.

수평 확장을 활성화하려면, 애플리케이션 `.env` 설정 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

그 다음, 모든 Reverb 서버가 통신할 수 있는 전용 중앙 Redis 서버를 준비해야 합니다. Reverb는 [애플리케이션에 설정된 기본 Redis 연결](/docs/{{version}}/redis#configuration)을 사용해 메시지를 모든 Reverb 서버로 퍼블리시합니다.

Reverb의 스케일링 옵션을 활성화하고 Redis 서버를 구성했다면, Redis 서버와 통신 가능한 여러 서버에서 `reverb:start` 명령어를 실행하면 됩니다. 이 Reverb 서버들은 로드 밸런서 뒤에 배치하여, 들어오는 요청을 서버들에 고르게 분산시켜야 합니다.