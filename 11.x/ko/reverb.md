# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
    - [애플리케이션 자격증명](#application-credentials)
    - [허용된 출처](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션에서 Reverb 실행](#production)
    - [열린 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb)는 라라벨 애플리케이션에 초고속이면서 확장 가능한 실시간 WebSocket 통신을 직접 제공합니다. 또한 라라벨의 기존 [이벤트 브로드캐스팅 도구들](/docs/11.x/broadcasting)과 매끄럽게 통합됩니다.

<a name="installation"></a>
## 설치 (Installation)

Reverb는 `install:broadcasting` Artisan 명령어를 사용하여 설치할 수 있습니다:

```
php artisan install:broadcasting
```

<a name="configuration"></a>
## 구성 (Configuration)

내부적으로 `install:broadcasting` Artisan 명령어는 `reverb:install` 명령어를 실행하여 합리적인 기본 설정 옵션과 함께 Reverb를 설치합니다. 설정을 변경하고 싶다면 Reverb의 환경 변수나 `config/reverb.php` 구성 파일을 업데이트하면 됩니다.

<a name="application-credentials"></a>
### 애플리케이션 자격증명 (Application Credentials)

Reverb 연결을 설정하려면 클라이언트와 서버 간에 Reverb “애플리케이션” 자격증명을 교환해야 합니다. 이 자격증명은 서버에서 설정되며 클라이언트 요청을 검증하는 데 사용됩니다. 다음 환경 변수들을 사용해 자격증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 출처 (Allowed Origins)

클라이언트 요청이 발생할 수 있는 출처(origin)를 `config/reverb.php` 구성 파일 내의 `apps` 섹션에서 `allowed_origins` 설정을 수정해 정의할 수 있습니다. 허용되지 않은 출처에서 오는 요청은 거부됩니다. 모든 출처를 허용하려면 `*`를 사용할 수 있습니다:

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
### 추가 애플리케이션 (Additional Applications)

보통 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 설치로 여러 애플리케이션을 서비스하는 것도 가능합니다.

예를 들어, 하나의 라라벨 애플리케이션을 유지하면서 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공할 수 있습니다. 이는 `config/reverb.php` 구성 파일에 여러 `apps`를 정의함으로써 가능합니다:

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

그러나 로컬 개발 환경 등에서는 Reverb 서버가 직접 안전한 연결을 처리하도록 하는 것이 유용할 수 있습니다. 만약 [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/11.x/valet)에서 [secure 명령어](/docs/11.x/valet#securing-sites)를 실행했다면, Herd / Valet가 생성한 인증서를 사용하여 Reverb 연결을 보안할 수 있습니다. 이를 위해서는 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나 Reverb 서버를 시작할 때 명시적으로 호스트명 옵션을 지정하세요:

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되므로 위 명령어를 실행하면, `wss://laravel.test:8080`의 안전한 WebSocket 프로토콜(`wss`)로 Reverb 서버에 접속할 수 있습니다.

또한, `config/reverb.php` 파일에 `tls` 옵션 내에서 직접 인증서를 지정할 수도 있습니다. `tls` 배열 내에는 [PHP SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 제공할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행 (Running the Server)

Reverb 서버는 `reverb:start` Artisan 명령어를 사용해 시작할 수 있습니다:

```sh
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되어 모든 네트워크 인터페이스에서 접근 가능합니다.

호스트나 포트를 지정하려면 서버 시작 시 `--host`와 `--port` 옵션을 사용하세요:

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는 `.env` 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT`는 `REVERB_HOST`와 `REVERB_PORT`와 혼동하면 안 됩니다. 전자는 Reverb 서버 자체가 실행될 호스트와 포트를 지정하고, 후자는 라라벨이 브로드캐스트 메시지를 어디로 보낼지 지정합니다. 예를 들어, 프로덕션 환경에서 `443` 포트의 퍼블릭 Reverb 호스트 이름으로 요청을 받아 `0.0.0.0:8080`에서 실행 중인 Reverb 서버로 라우팅하는 경우, 환경 변수는 다음과 같이 정의합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅 (Debugging)

성능 향상을 위해, 기본적으로 Reverb는 디버그 정보를 출력하지 않습니다. 서버를 통과하는 데이터 스트림을 보고 싶다면 `reverb:start` 명령어에 `--debug` 옵션을 추가하세요:

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작 (Restarting)

Reverb는 장기 실행 프로세스이므로 코드 변경 사항을 적용하려면 서버를 재시작해야 합니다. `reverb:restart` Artisan 명령어를 사용하세요.

이 명령어는 모든 연결이 정상적으로 종료된 후 서버를 중지합니다. Supervisor와 같은 프로세스 관리자를 사용하는 경우, 모든 연결 종료 후 프로세스 관리자가 서버를 자동 재시작합니다:

```sh
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링 (Monitoring)

Reverb는 [Laravel Pulse](/docs/11.x/pulse)와 통합하여 모니터링할 수 있습니다. 이 통합을 활성화하면 서버가 처리 중인 연결 수와 메시지 수를 추적할 수 있습니다.

우선 [Pulse를 설치](/docs/11.x/pulse#installation)한 후, 애플리케이션의 `config/pulse.php` 구성 파일에 Reverb의 레코더(recorders)를 추가하세요:

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

    ...
],
```

그 다음, 각 레코더에 대한 Pulse 카드를 [Pulse 대시보드](/docs/11.x/pulse#dashboard-customization)에 추가하세요:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 상태는 주기적으로 폴링하여 업데이트됩니다. 올바른 출력 보장을 위해 Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. 만약 [수평 확장](#scaling) 구성으로 Reverb를 실행하는 경우, 이 데몬은 여러 서버 중 한 곳에서만 실행해야 합니다.

<a name="production"></a>
## 프로덕션에서 Reverb 실행 (Running Reverb in Production)

WebSocket 서버의 장기 실행 특성 때문에, 서버와 호스팅 환경을 최적화하여 사용 가능한 리소스 내에서 최적의 연결 수를 효과적으로 처리할 수 있도록 해야 합니다.

> [!NOTE]  
> 만약 사이트를 [Laravel Forge](https://forge.laravel.com)로 관리 중이라면, “Application” 패널에서 Reverb 최적화를 자동으로 수행할 수 있습니다. 통합을 활성화하면 Forge가 필요한 확장 설치 및 최대 연결 수 증가 등 프로덕션 환경 준비를 보장합니다.

<a name="open-files"></a>
### 열린 파일 (Open Files)

WebSocket 연결은 클라이언트나 서버 중 하나가 연결을 끊을 때까지 메모리에 유지됩니다. Unix 및 유닉스 계열 환경에서는 각 연결이 파일로 표현됩니다. 하지만 운영체제나 애플리케이션 레벨에서 열린 파일 수 제한이 존재할 수 있습니다.

<a name="operating-system"></a>
#### 운영체제 (Operating System)

Unix 기반 운영체제에서 열린 파일 수 제한은 `ulimit` 명령어로 확인할 수 있습니다:

```sh
ulimit -n
```

이 명령은 사용자별 열린 파일 수 제한을 보여줍니다. 이 값을 변경하려면 `/etc/security/limits.conf` 파일을 편집하면 됩니다. 예를 들어 `forge` 사용자의 열린 파일 최대치를 10,000으로 변경하려면 다음과 같이 작성합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프 (Event Loop)

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용해 서버의 WebSocket 연결을 관리합니다. 기본 이벤트 루프는 `stream_select`를 이용하는데, 이는 추가 확장이 필요 없으나 보통 1,024개의 열린 파일로 제한됩니다. 따라서 1,000개가 넘는 동시 연결을 다루려면 이 제한이 없는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 사용 가능한 경우 자동으로 `ext-uv` 기반의 이벤트 루프로 전환합니다. 이 PHP 확장은 PECL로 설치할 수 있습니다:

```sh
pecl install uv
```

<a name="web-server"></a>
### 웹 서버 (Web Server)

대부분의 경우, Reverb는 서버 내 비웹 공개 포트에서 실행됩니다. 따라서 Reverb로 트래픽을 라우팅하려면 역방향 프록시 설정이 필요합니다. 예를 들어 Reverb가 `0.0.0.0`의 `8080` 포트에서 실행 중이고, Nginx 웹 서버를 사용하는 경우 다음과 같은 사이트 설정으로 역방향 프록시를 정의할 수 있습니다:

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
> Reverb는 `/app` 경로에서 WebSocket 연결을 수신하고, `/apps` 경로에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버는 두 URI에 모두 접근 가능하도록 설정해야 합니다. [Laravel Forge](https://forge.laravel.com)를 사용하는 경우 기본적으로 Reverb 서버가 올바르게 구성됩니다.

일반적으로 웹 서버는 과도한 부하를 방지하기 위해 허용되는 최대 연결 수를 제한합니다. Nginx에서 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일에서 `worker_rlimit_nofile`과 `worker_connections` 값을 다음과 같이 조정합니다:

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

위 설정은 프로세스당 최대 10,000개의 Nginx 워커가 생성되는 것을 허용하며, 열린 파일 제한도 10,000으로 설정합니다.

<a name="ports"></a>
### 포트 (Ports)

Unix 계열 운영체제에서는 서버에서 열 수 있는 포트 수에 제한이 있습니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다:

```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력은 서버가 최대 28,231개(60,999 - 32,768)의 연결을 처리할 수 있음을 의미합니다. 각 연결은 비어있는 포트가 필요하기 때문입니다. 허용 가능한 연결 수를 늘리려면 [수평 확장](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 포트 범위를 늘릴 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리 (Process Management)

대부분의 경우 Supervisor와 같은 프로세스 관리자를 사용해 Reverb 서버가 계속 실행되도록 해야 합니다. Supervisor를 사용하는 경우, 서버의 `supervisor.conf` 파일에서 `minfds` 설정을 업데이트해 Reverb 연결을 처리할 때 필요한 파일을 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링 (Scaling)

단일 서버가 허용한 연결 수보다 많은 연결을 처리해야 하는 경우, Reverb 서버를 수평 확장할 수 있습니다. Redis의 pub/sub 기능을 활용해 여러 서버 사이에 연결을 관리합니다. 애플리케이션 Reverb 서버 중 한 곳에서 메시지가 수신되면 Redis를 통해 다른 서버들에게 해당 메시지를 퍼블리시합니다.

수평 확장을 활성화하려면, `.env` 구성 파일에 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

다음으로 모든 Reverb 서버가 통신할 수 있는 전용 중앙 Redis 서버를 갖춰야 합니다. Reverb는 애플리케이션에 기본 설정된 Redis 연결을 사용해 메시지를 퍼블리시합니다.

이후 Redis 서버와 통신 가능한 여러 서버에서 `reverb:start` 명령어를 실행하면 됩니다. 이 서버들은 로드 밸런서 뒤에 배치해 들어오는 요청을 고르게 분배해야 합니다.