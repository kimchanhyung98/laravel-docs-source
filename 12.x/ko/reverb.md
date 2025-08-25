# Laravel Reverb (Laravel Reverb)

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
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
## 소개 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb)는 Laravel 애플리케이션에 초고속이면서 스케일이 가능한 실시간 WebSocket 통신 기능을 직접 제공합니다. 또한, Laravel이 기본적으로 제공하는 다양한 [이벤트 브로드캐스팅 도구](/docs/12.x/broadcasting)와도 완벽하게 통합됩니다.

<a name="installation"></a>
## 설치 (Installation)

다음과 같이 `install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다.

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 설정 (Configuration)

`install:broadcasting` Artisan 명령어는 내부적으로 `reverb:install` 명령어를 실행하여, Reverb를 합리적인 기본 설정값과 함께 설치합니다. 만약 설정을 변경하고 싶다면, Reverb의 환경 변수 또는 `config/reverb.php` 설정 파일을 수정하면 됩니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명

Reverb에 연결을 확립하려면, 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명(credential)을 주고받아야 합니다. 이 자격 증명은 서버에 설정되며, 클라이언트 요청을 검증하는 데 사용됩니다. 다음과 같은 환경 변수를 사용하여 자격 증명을 정의할 수 있습니다.

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 오리진

클라이언트 요청을 허용할 오리진(origin) 목록을 `config/reverb.php` 파일의 `apps` 섹션 내 `allowed_origins` 설정값에서 정의할 수 있습니다. 허용된 오리진에 없는 곳에서의 요청은 모두 거부됩니다. 모든 오리진을 허용하려면 `*`를 사용할 수 있습니다.

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

일반적으로 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 설치로 여러 애플리케이션을 동시에 서비스하는 것도 가능합니다.

예를 들어, 하나의 Laravel 애플리케이션에서 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하고 싶을 수 있습니다. 이를 위해서는 애플리케이션의 `config/reverb.php` 설정 파일에서 여러 개의 `apps`를 정의하면 됩니다.

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

대부분의 경우, 보안 WebSocket 연결(`wss`)은 상위(업스트림) 웹 서버(Nginx 등)가 요청을 Reverb 서버로 전달하기 전에 처리합니다.

하지만, 로컬 개발 환경과 같이 Reverb 서버가 직접 보안 연결을 처리해야 할 상황이 있을 수 있습니다. 만약 [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/12.x/valet)에서 해당 애플리케이션에 대해 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행했다면, 사이트에 대해 생성된 Herd/Valet 인증서를 사용하여 Reverb 연결에 보안을 적용할 수 있습니다. 이를 위해서는, `REVERB_HOST` 환경 변수를 사이트의 호스트명(도메인)으로 설정하거나 Reverb 서버를 시작할 때 명시적으로 `hostname` 옵션을 전달합니다.

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 resolve되기 때문에, 위 명령어를 실행하면 Reverb 서버에 대해 보안 WebSocket 프로토콜(`wss`)로 `wss://laravel.test:8080` 경로로 접근할 수 있습니다.

직접 인증서를 지정하고 싶다면, 애플리케이션의 `config/reverb.php` 설정 파일의 `tls` 옵션에 [PHP의 SSL context 옵션](https://www.php.net/manual/en/context.ssl.php) 중 원하는 값을 지정할 수 있습니다.

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행 (Running the Server)

Reverb 서버는 `reverb:start` Artisan 명령어를 사용하여 실행할 수 있습니다.

```shell
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접근할 수 있습니다.

호스트(host)나 포트(port)를 별도로 지정하려면, 서버를 실행할 때 `--host`와 `--port` 옵션을 사용하면 됩니다.

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 환경 설정 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

`REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST`, `REVERB_PORT`와 혼동해서는 안 됩니다. 앞의 환경 변수는 Reverb 서버 자체가 어떤 호스트와 포트에서 실행될지 지정하는 것이고, 뒤의 환경 변수는 Laravel이 브로드캐스트 메시지를 어디로 보낼지 지정합니다. 예를 들어, 운영 환경에서 공용 Reverb 호스트명(포트 443)에서 `0.0.0.0:8080`에서 실행 중인 Reverb 서버로 요청을 라우팅한다면, 환경 변수는 아래와 같이 설정됩니다.

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅 (Debugging)

성능 향상을 위해 Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. 서버를 통과하는 데이터 스트림을 보고 싶다면, `reverb:start` 명령어 실행 시 `--debug` 옵션을 사용할 수 있습니다.

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작 (Restarting)

Reverb는 장시간 실행되는 프로세스이기 때문에, 코드 변경 사항이 서버에 바로 반영되지 않습니다. 코드를 수정했다면 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 서버를 중지하기 전 모든 연결이 안전하게 종료되도록 합니다. Supervisor와 같은 프로세스 관리자를 사용하여 Reverb를 실행 중인 경우, 모든 연결이 종료된 후 프로세스 관리자가 서버를 자동으로 재시작합니다.

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링 (Monitoring)

Reverb는 [Laravel Pulse](/docs/12.x/pulse)와의 통합을 통해 모니터링할 수 있습니다. Reverb의 Pulse 통합 기능을 활성화하면, 서버에서 처리되는 연결 수와 메시지 개수를 추적할 수 있습니다.

통합을 활성화하려면 먼저 [Pulse를 설치](/docs/12.x/pulse#installation)해야 합니다. 이후, 애플리케이션의 `config/pulse.php` 설정 파일에 Reverb의 recorder를 추가합니다.

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

그리고 각 recorder에 해당하는 Pulse 카드를 [Pulse 대시보드](/docs/12.x/pulse#dashboard-customization)에 추가합니다.

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동 정보는 주기적으로 새 업데이트를 폴링하여 기록됩니다. 이 정보가 Pulse 대시보드에 올바르게 표시되도록 하려면, 반드시 Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. 만약 [수평 스케일링](#scaling)이 적용된 환경이라면, 이 데몬은 서버 중 한 곳에서만 실행하면 충분합니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행 (Running Reverb in Production)

WebSocket 서버의 특성상 장시간 동안 실행되므로, 사용 가능한 서버 리소스 범위 내에서 최대한의 연결을 효과적으로 처리할 수 있도록 서버와 호스팅 환경을 최적화해야 할 수 있습니다.

> [!NOTE]
> 사이트가 [Laravel Forge](https://forge.laravel.com)로 관리된다면, "Application" 패널에서 Reverb 통합을 활성화하여 자동으로 서버를 Reverb에 최적화할 수 있습니다. Reverb 통합을 활성화하면, Forge가 필요한 확장 프로그램 설치 및 허용 가능한 연결 수 증가 등 프로덕션 환경 최적화를 자동으로 수행합니다.

<a name="open-files"></a>
### 오픈 파일 (Open Files)

각 WebSocket 연결은 클라이언트 또는 서버가 연결을 종료할 때까지 메모리에 유지됩니다. 유닉스 및 유사 유닉스 환경에서는, 이러한 각 연결이 파일로 표현됩니다. 하지만, 운영체제 및 애플리케이션 차원에서 허용되는 오픈 파일 수에 제한이 있을 수 있습니다.

<a name="operating-system"></a>
#### 운영체제 (Operating System)

유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 오픈 파일 수를 확인할 수 있습니다.

```shell
ulimit -n
```

이 명령어로 사용자별 오픈 파일 한도(limits)를 확인할 수 있습니다. 값을 늘리려면, `/etc/security/limits.conf` 파일을 수정하면 됩니다. 예를 들어, `forge` 사용자의 오픈 파일 최대값을 10,000으로 늘리려면 아래와 같이 설정합니다.

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프 (Event Loop)

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용하여 서버에서 WebSocket 연결을 관리합니다. 기본적으로 이 이벤트 루프는 별도 확장 없이 사용할 수 있는 `stream_select`를 사용하여 구동됩니다. 다만, `stream_select`는 일반적으로 1,024개의 오픈 파일만 지원하므로, 1,000개가 넘는 동시 연결을 처리하려면 제한이 없는 다른 이벤트 루프가 필요합니다.

Reverb는 `ext-uv` 확장 프로그램이 설치되어 있으면 자동으로 해당 이벤트 루프로 전환됩니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다.

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버 (Web Server)

대부분의 경우, Reverb는 서버의 외부에 노출되지 않는(non web-facing) 포트에서 실행됩니다. 따라서 Reverb로 트래픽을 전달하려면 리버스 프록시(reverse proxy) 구성이 필요합니다. 예를 들어, Reverb가 `0.0.0.0:8080`에서 실행되고, 서버에서 Nginx를 사용한다면 아래와 같은 Nginx 사이트 설정으로 리버스 프록시를 구성할 수 있습니다.

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
> Reverb는 `/app` 경로에서 WebSocket 연결을 받고, `/apps` 경로에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버는 이 두 URI 모두 서비스할 수 있어야 합니다. [Laravel Forge](https://forge.laravel.com)로 서버를 관리하는 경우, Reverb 서버가 기본적으로 올바르게 구성되어 배포됩니다.

웹 서버 설정에서는 서버 과부하를 방지하기 위해 일반적으로 연결 수에 제한이 걸려 있습니다. Nginx 웹 서버에서 허용 연결 수를 10,000까지 늘리려면, `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 수정하면 됩니다.

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

위 설정은 프로세스당 최대 10,000개의 Nginx 워커를 생성할 수 있도록 하며, 동시에 오픈 파일 한도 역시 10,000개로 지정합니다.

<a name="ports"></a>
### 포트 (Ports)

유닉스 기반 운영체제는 서버에서 동시에 열 수 있는 포트 개수에 기본적으로 제한을 둡니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다.

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위와 같이 출력된다면, 32,768부터 60,999까지 즉, 최대 28,231개(60,999 - 32,768)의 연결을 지원할 수 있음을 의미합니다(각 연결당 포트가 하나 필요). 연결 수를 늘리려면 [수평 스케일링](#scaling)을 권장하지만, `/etc/sysctl.conf` 파일을 수정하여 서버의 포트 범위를 확장하여 사용할 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리 (Process Management)

대부분의 경우, Supervisor와 같은 프로세스 관리자를 활용해 Reverb 서버가 지속적으로 실행되도록 관리해야 합니다. Supervisor를 사용하여 Reverb를 실행할 경우, Supervisor가 Reverb 서버 연결을 위해 충분한 파일을 열 수 있도록 서버의 `supervisor.conf` 파일에서 `minfds` 값을 적절하게 늘려야 합니다.

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링 (Scaling)

단일 서버가 허용하는 최대 연결 수 이상을 처리해야 할 상황이라면 Reverb 서버를 수평으로(scale out) 확장할 수 있습니다. Redis의 publish/subscribe 기능을 활용하여, Reverb는 여러 서버에 분산된 연결을 관리할 수 있습니다. 한 서버가 메시지를 수신하면, 해당 서버는 Redis를 사용해 모든 다른 서버에 메시지를 전파합니다.

수평 스케일링을 활성화하려면, 애플리케이션의 `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정합니다.

```env
REVERB_SCALING_ENABLED=true
```

그리고 모든 Reverb 서버가 통신할 수 있도록 별도의 중앙 Redis 서버가 필요합니다. Reverb는 [애플리케이션에서 기본으로 설정된 Redis 연결](/docs/12.x/redis#configuration)을 통해 모든 Reverb 서버에 메시지를 퍼블리시합니다.

수평 스케일링 옵션을 켜고 Redis 서버를 설정한 후에는, Redis 서버와 통신할 수 있는 여러 서버에서 각각 `reverb:start` 명령어를 실행하면 됩니다. 이때 Reverb 서버들은 로드 밸런서 뒤에 배치하여, 들어오는 요청을 서버 간에 골고루 분산하도록 해야 합니다.
