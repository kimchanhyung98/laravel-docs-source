# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
    - [허용된 출처(Allowed Origins)](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행하기](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션 환경에서 Reverb 실행하기](#production)
    - [열린 파일 수](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb)는 빠르고 확장 가능한 실시간 WebSocket 통신 기능을 Laravel 애플리케이션에 직접 제공하며, Laravel이 기본 제공하는 [이벤트 브로드캐스팅 도구들](/docs/master/broadcasting)과 원활하게 통합됩니다.

<a name="installation"></a>
## 설치 (Installation)

`install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 설정 (Configuration)

`install:broadcasting` Artisan 명령어를 실행하면 내부적으로 `reverb:install` 명령어가 실행되어, Reverb가 적절한 기본 설정 옵션과 함께 설치됩니다. 설정을 변경하고 싶다면 환경 변수나 `config/reverb.php` 설정 파일을 수정하여 적용할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명 (Application Credentials)

Reverb에 연결을 수립하려면 클라이언트와 서버 간에 Reverb "애플리케이션" 자격증명 세트를 교환해야 합니다. 이 자격증명은 서버에서 설정되며 클라이언트의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 통해 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 출처 (Allowed Origins)

클라이언트 요청의 출처(origin)를 제한하려면 `config/reverb.php` 설정 파일의 `apps` 섹션 내 `allowed_origins` 값을 업데이트하면 됩니다. 이 목록에 포함되지 않은 출처에서 오는 요청은 거부됩니다. 모든 출처를 허용하려면 `*`를 사용할 수 있습니다:

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

일반적으로 Reverb는 설치된 애플리케이션에 대한 WebSocket 서버를 제공합니다. 하지만 단일 Reverb 설치로 여러 애플리케이션을 동시에 서비스하는 것도 가능합니다.

예를 들어, 하나의 Laravel 애플리케이션이 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하는 경우, `config/reverb.php` 내 `apps` 배열에 여러 앱을 정의하면 됩니다:

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

대부분의 경우, 보안 WebSocket 연결은 Nginx 등 상위 웹 서버에서 처리한 뒤 Reverb 서버로 프록시됩니다.

그러나 로컬 개발 환경 등에서 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 수 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 이용하거나, [Laravel Valet](/docs/master/valet)에서 [secure 명령어](/docs/master/valet#securing-sites)를 실행해 SSL 인증서를 생성한 경우, 이 인증서를 Reverb 연결에 사용할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트 호스트명으로 설정하거나, Reverb 서버 시작 시 명령어 옵션 `--hostname`으로 명시해 주세요:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인이 `localhost`로 해석되므로, 위 명령어 실행 후 Reverb 서버는 `wss://laravel.test:8080` 주소를 통해 보안 WebSocket 프로토콜(`wss`)로 접근 가능해집니다.

또는 `config/reverb.php` 설정 파일의 `tls` 옵션을 직접 정의하여 인증서를 수동으로 지정할 수 있습니다. `tls` 배열 내부에는 [PHP SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 사용할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행하기 (Running the Server)

`reverb:start` Artisan 명령어로 Reverb 서버를 시작할 수 있습니다:

```shell
php artisan reverb:start
```

기본적으로 `0.0.0.0:8080`에서 시작되어 모든 네트워크 인터페이스에서 접근 가능합니다.

호스트나 포트를 지정해야 할 경우, 서버 시작 시 `--host` 및 `--port` 옵션을 사용할 수 있습니다:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는 `.env` 파일에 `REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수를 정의해도 됩니다.

`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 변수는 `REVERB_HOST`와 `REVERB_PORT`와는 다릅니다. 전자는 Reverb 서버가 직접 실행될 호스트와 포트를 지정하고, 후자는 Laravel에게 브로드캐스트 메시지를 보낼 대상 주소를 알려줍니다. 예를 들어, 프로덕션 환경에서 공용 Reverb 호스트가 `443` 포트로 접속을 받고, 실제 Reverb 서버는 `0.0.0.0:8080`에서 실행되는 경우 다음과 같이 설정합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅 (Debugging)

성능 향상을 위해 Reverb는 기본적으로 디버그 출력을 하지 않습니다. 서버를 통해 흐르는 데이터 스트림을 보고 싶으면 `reverb:start` 명령어에 `--debug` 옵션을 추가하세요:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작 (Restarting)

Reverb는 장시간 실행되는 프로세스이므로, 코드 변경 사항을 반영하려면 `reverb:restart` Artisan 명령어를 통해 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 모든 연결을 정상 종료한 뒤 서버를 중지시킵니다. Supervisor 같은 프로세스 관리자를 사용 중이라면, 연결 종료 후 자동으로 재시작됩니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링 (Monitoring)

Reverb는 [Laravel Pulse](/docs/master/pulse)와 연동하여 모니터링할 수 있습니다. Pulse 통합을 활성화하면 서버가 처리하는 연결 수와 메시지 수를 추적할 수 있습니다.

통합 활성화를 위해 먼저 Pulse를 설치해야 합니다(/docs/master/pulse#installation 참조). 이후 애플리케이션의 `config/pulse.php` 설정 파일에 Reverb의 레코더(recorders)를 추가하세요:

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

Pulse 대시보드에 각 레코더에 대응하는 카드 컴포넌트를 추가하세요(/docs/master/pulse#dashboard-customization 참조):

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. 이를 정상적으로 보여주기 위해서는 Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. 수평적 스케일링([스케일링](#scaling))으로 여러 서버를 운영하는 경우, 이 데몬은 한 서버에서만 실행해야 합니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행하기 (Running Reverb in Production)

WebSocket 서버는 장시간 실행되는 특성상, 서버와 호스팅 환경을 최적화해주어야 사용 가능한 리소스 내에서 최대 연결 수를 안정적으로 처리할 수 있습니다.

> [!NOTE]
> [Laravel Forge](https://forge.laravel.com)로 사이트를 관리하는 경우, "Application" 패널에서 Reverb 통합을 활성화해 자동으로 서버 최적화를 적용할 수 있습니다. 이 기능을 켜면 필요한 확장 설치 및 연결 수 제한 증가 작업이 포함됩니다.

<a name="open-files"></a>
### 열린 파일 수 (Open Files)

각 WebSocket 연결은 클라이언트 혹은 서버가 끊을 때까지 메모리에 유지됩니다. Unix 계열 시스템에서는 연결을 파일 단위로 관리하는데, 운영체제와 애플리케이션 수준에서 열린 파일 수 제한이 존재합니다.

<a name="operating-system"></a>
#### 운영체제 설정 (Operating System)

Unix 기반 시스템에서 허용된 열린 파일 수는 `ulimit` 명령어로 확인 가능합니다:

```shell
ulimit -n
```

사용자별 열린 파일 제한을 수정하려면 `/etc/security/limits.conf` 파일을 편집합니다. 예를 들어, `forge` 사용자에 대해 최대 열린 파일 수를 10,000으로 설정하려면 다음과 같이 작성할 수 있습니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프 (Event Loop)

Reverb는 서버 내 WebSocket 연결 관리를 위해 ReactPHP 이벤트 루프를 사용합니다. 기본적으로 `stream_select`를 이용하는데, 이 방법은 추가 확장 없이 동작하지만 보통 1,024개의 열린 파일 제한을 가지고 있습니다. 만약 1,000개 이상의 동시 연결을 처리하려면 이 제한을 넘지 않는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 사용 가능하면 자동으로 `ext-uv` 확장 기반 이벤트 루프로 전환합니다. 해당 PHP 확장은 PECL을 통해 설치 가능합니다:

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버 (Web Server)

대부분의 경우, Reverb는 서버 내에서 외부에 직접 노출되지 않는 포트를 사용합니다. 따라서 Reverb로의 트래픽 라우팅을 위해 리버스 프록시(reverse proxy)를 설정해야 합니다. 예를 들어, Reverb가 `0.0.0.0` 호스트의 `8080` 포트에서 실행 중이고, 서버에서 Nginx를 사용한다면 아래와 같이 사이트 설정에서 리버스 프록시를 구성할 수 있습니다:

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
> Reverb는 WebSocket 요청에서 `/app` 경로를, API 요청에서 `/apps` 경로를 수신합니다. 웹 서버가 이 두 URI 모두를 정상적으로 처리하도록 설정되어야 합니다. [Laravel Forge](https://forge.laravel.com)로 서버를 관리한다면 기본적으로 Reverb 서버가 올바르게 설정되어 있습니다.

일반적으로, 웹 서버는 서버 과부하 방지를 위해 처리 가능한 연결 수를 제한합니다. Nginx 웹 서버의 연결 허용 수를 10,000으로 늘리려면 `nginx.conf` 파일 내 `worker_rlimit_nofile`와 `worker_connections` 값을 아래와 같이 수정해야 합니다:

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

이 설정은 Nginx 프로세스별 최대 10,000개의 워커를 허용하고, 열린 파일 제한도 10,000으로 설정합니다.

<a name="ports"></a>
### 포트 (Ports)

Unix 계열 운영체제는 서버에서 열 수 있는 포트의 수를 제한하는 경우가 많습니다. 현재 허용된 범위는 아래 명령어로 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력은 최대 열 수 있는 연결이 28,231(60,999 - 32,768)임을 뜻합니다. 각각의 연결에는 사용 가능한 포트가 필요하기 때문입니다. 허용 가능한 연결 수를 늘리고 싶으면 [수평적 스케일링](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 포트 범위를 조절하여 직접 늘릴 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리 (Process Management)

대부분의 경우, Supervisor 같은 프로세스 관리자를 사용해 Reverb 서버가 항상 실행되도록 해야 합니다. Supervisor를 이용한다면 `supervisor.conf` 파일 내 `minfds` 설정을 서버가 다룰 연결 수에 맞게 충분히 높여야 합니다. 예를 들어 10,000으로 설정하려면:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링 (Scaling)

한 서버에서 허용하는 연결 수를 초과하는 경우에는 Reverb 서버를 수평적으로 확장할 수 있습니다. Redis의 publish/subscribe 기능을 활용해 여러 서버 간 연결 상태를 관리합니다. 한 서버에서 메시지를 수신하면 Redis를 통해 다른 모든 서버에 해당 메시지를 발행합니다.

수평 스케일링을 활성화하려면 애플리케이션 `.env` 파일에 다음과 같이 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

이후, 모든 Reverb 서버가 통신할 중앙 Redis 서버를 구성해야 합니다. Reverb는 애플리케이션에 기본 설정된 Redis 연결을 사용해 메시지를 발행합니다.

스케일링을 활성화하고 Redis 서버를 설정했다면, Redis와 통신 가능한 여러 서버에서 `reverb:start` 명령어를 실행하면 됩니다. 이 경우, 각 서버들은 로드 밸런서 뒤에 배치하여 들어오는 요청들을 균등하게 분산해야 합니다.