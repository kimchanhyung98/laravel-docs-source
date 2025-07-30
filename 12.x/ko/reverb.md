# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격증명](#application-credentials)
    - [허용된 출처](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션 환경에서 Reverb 실행](#production)
    - [열린 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb)는 매우 빠르고 확장 가능한 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 [이벤트 브로드캐스팅 도구](/docs/12.x/broadcasting)와 원활하게 통합됩니다.

<a name="installation"></a>
## 설치 (Installation)

`install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 설정 (Configuration)

`install:broadcasting` Artisan 명령어는 내부적으로 `reverb:install` 명령어를 실행하여, 적절한 기본 설정 옵션과 함께 Reverb를 설치합니다. 설정을 변경하고 싶다면 Reverb의 환경 변수나 `config/reverb.php` 설정 파일을 업데이트하면 됩니다.

<a name="application-credentials"></a>
### 애플리케이션 자격증명 (Application Credentials)

Reverb에 연결을 성립하려면 클라이언트와 서버 간에 Reverb "애플리케이션" 자격증명 세트가 교환되어야 합니다. 이 자격증명은 서버에서 설정되며 클라이언트 요청을 확인하는 데 사용됩니다. 다음 환경 변수를 사용해 자격증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 출처 (Allowed Origins)

클라이언트 요청이 발생할 수 있는 출처도 `config/reverb.php` 설정 파일 `apps` 섹션 내 `allowed_origins` 값으로 정의할 수 있습니다. 허용되지 않은 출처에서 온 요청은 모두 거부됩니다. 모든 출처를 허용하려면 `*`를 사용할 수 있습니다:

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

보통 Reverb는 설치된 단일 애플리케이션을 위한 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 설치로 여러 애플리케이션을 지원하는 것도 가능합니다.

예를 들어, 단일 Laravel 애플리케이션에서 여러 애플리케이션을 위한 WebSocket 연결을 Reverb를 통해 제공하고 싶다면, `config/reverb.php` 설정 파일에 여러 `apps`를 정의하면 됩니다:

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

대부분의 경우, 보안 WebSocket 연결은 상위 웹 서버(Nginx 등)가 처리한 후 요청이 Reverb 서버로 프록시됩니다.

하지만, 로컬 개발 환경 등에서 Reverb 서버가 직접 보안 연결을 처리하도록 하는 것이 유용할 때도 있습니다. 만약 [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/12.x/valet)에서 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행했다면, Herd / Valet이 생성한 인증서를 사용해 Reverb 연결을 보안할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트 호스트명으로 설정하거나 Reverb 서버 시작 시 `--hostname` 옵션으로 호스트명을 명시합니다:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되므로, 위 명령을 실행하면 `wss://laravel.test:8080` 주소로 Reverb 서버에 보안 WebSocket 프로토콜(`wss`)로 접근할 수 있습니다.

또한 `config/reverb.php` 설정 파일에서 `tls` 옵션을 정의하여 직접 인증서를 선택할 수도 있습니다. `tls` 배열에 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 옵션들을 제공할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행 (Running the Server)

Reverb 서버는 `reverb:start` Artisan 명령어로 시작할 수 있습니다:

```shell
php artisan reverb:start
```

기본적으로, Reverb 서버는 `0.0.0.0:8080`에서 시작되어 모든 네트워크 인터페이스에서 접근 가능하게 됩니다.

호스트나 포트를 지정해야 한다면, 서버 실행 시 `--host`와 `--port` 옵션을 사용하세요:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는 애플리케이션의 `.env` 파일에 `REVERB_SERVER_HOST` 와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수 있습니다.

`REVERB_SERVER_HOST` 와 `REVERB_SERVER_PORT` 는 `REVERB_HOST` 와 `REVERB_PORT`와 혼동하면 안 됩니다. 전자는 Reverb 서버 자체를 실행할 호스트와 포트를 지정하며, 후자는 Laravel이 브로드캐스트 메시지를 보낼 위치를 지정합니다. 예를 들어, 프로덕션 환경에서 공개 Reverb 호스트를 포트 `443`으로 받고, 내부적으로 `0.0.0.0:8080`에서 실행되는 Reverb 서버로 요청을 라우팅할 수 있습니다. 이 경우 환경 변수는 다음과 같이 설정됩니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅 (Debugging)

기본적으로 Reverb는 성능 향상을 위해 디버그 정보를 출력하지 않습니다. Reverb 서버에서 오가는 데이터 스트림을 보고 싶다면 `reverb:start` 명령어에 `--debug` 옵션을 추가하면 됩니다:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작 (Restarting)

Reverb는 장기 실행 프로세스이므로, 코드 변경 사항을 반영하려면 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 모든 연결이 정상적으로 종료될 때까지 기다린 뒤 서버를 중지합니다. Supervisor와 같은 프로세스 관리자를 사용 중이라면, 연결 종료 후 프로세스 관리자가 자동으로 서버를 재시작합니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링 (Monitoring)

Reverb는 [Laravel Pulse](/docs/12.x/pulse)와 통합하여 모니터링할 수 있습니다. Pulse 통합을 활성화하면 서버에서 처리 중인 연결 수와 메시지 수를 추적할 수 있습니다.

통합을 활성화하려면 먼저 [Pulse를 설치](/docs/12.x/pulse#installation)했는지 확인하세요. 그리고 애플리케이션 `config/pulse.php` 설정 파일에 Reverb의 레코더를 추가합니다:

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

다음으로 각 레코더의 Pulse 카드들을 [Pulse 대시보드](/docs/12.x/pulse#dashboard-customization)에 추가하세요:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적인 폴링 방식으로 기록됩니다. Pulse 대시보드에서 이 정보가 올바르게 표시되도록 하려면, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. 만약 [수평 확장](#scaling)된 환경에서 Reverb를 실행한다면, 이 데몬은 서버 중 한 곳에서만 실행하면 됩니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행 (Running Reverb in Production)

WebSocket 서버는 장기 실행 구성 특성상, 가용 자원 내 최적의 연결 수를 안정적으로 처리하기 위해 서버 및 호스팅 환경의 일부 최적화가 필요합니다.

> [!NOTE]
> 사이트가 [Laravel Forge](https://forge.laravel.com)로 관리된다면, "Application" 패널에서 Reverb 통합을 활성화해 서버를 자동으로 최적화할 수 있습니다. 이를 통해 필요한 확장 설치, 허용 연결 수 증대 등이 처리됩니다.

<a name="open-files"></a>
### 열린 파일 (Open Files)

각 WebSocket 연결은 클라이언트 또는 서버가 연결을 종료할 때까지 메모리에 유지됩니다. Unix 계열 운영체제에서는 각 연결이 파일로 표현되지만, 운영체제나 애플리케이션 레벨에서 허용하는 열린 파일 수에 제한이 있는 경우가 많습니다.

<a name="operating-system"></a>
#### 운영체제 제한 (Operating System)

Unix 기반 운영체제에서는 `ulimit` 명령어로 허용된 열린 파일 수를 확인할 수 있습니다:

```shell
ulimit -n
```

이 명령어는 사용자별 열린 파일 제한을 보여줍니다. `/etc/security/limits.conf` 파일을 편집해 값을 변경할 수 있습니다. 예를 들어, `forge` 사용자에 대한 최대 열린 파일 수를 10,000으로 설정하려면 다음과 같이 합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프 (Event Loop)

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용해 서버에서 WebSocket 연결을 관리합니다. 기본 이벤트 루프는 추가 확장 필요 없이 동작하는 `stream_select`를 사용합니다. 하지만 `stream_select`는 보통 1,024개의 열린 파일로 제한됩니다. 따라서 1,000개 이상의 동시 연결을 처리하려면 이 제약에 영향을 받지 않는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 `ext-uv` 확장이 설치되어 있으면 자동으로 이를 사용하는 이벤트 루프로 전환합니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버 (Web Server)

대부분의 경우, Reverb는 서버에서 외부 공개용이 아닌 별도 포트에서 실행됩니다. 따라서 Reverb로 트래픽을 전달하려면 리버스 프록시를 설정해야 합니다. Reverb가 `0.0.0.0:8080`에서 실행되고, 서버가 Nginx 웹 서버를 사용하는 경우, Nginx 사이트 설정에 다음과 같이 리버스 프록시를 정의할 수 있습니다:

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
> Reverb는 `/app` 경로에서 WebSocket 연결을 받고, `/apps` 경로에서 API 요청을 처리합니다. 따라서 Reverb 요청을 다루는 웹 서버가 두 URI를 모두 처리할 수 있도록 설정해야 합니다. [Laravel Forge](https://forge.laravel.com)를 사용한다면 기본적으로 올바르게 설정되어 있습니다.

일반적으로 웹 서버는 과부하를 방지하기 위해 허용 연결 수를 제한합니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일의 `worker_rlimit_nofile`과 `worker_connections` 값을 다음과 같이 수정해야 합니다:

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

위 설정은 프로세스 당 최대 10,000 Nginx 워커를 생성할 수 있도록 하며, Nginx의 열린 파일 제한도 10,000으로 설정합니다.

<a name="ports"></a>
### 포트 (Ports)

Unix 기반 운영체제는 서버에서 열 수 있는 포트 수에 제한을 둡니다. 다음 명령으로 현재 허용된 포트 범위를 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

출력 결과는 서버가 최대 28,231개(60,999 - 32,768)의 연결을 처리할 수 있음을 의미합니다. 각 연결에는 사용 가능한 포트가 필요하기 때문입니다. 권장하는 방법은 [수평 확장](#scaling)을 통해 허용 연결 수를 늘리는 것이지만, 서버의 `/etc/sysctl.conf` 설정 파일에서 허용 포트 범위를 조정해 가용 포트 수를 늘릴 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리 (Process Management)

대부분의 경우 Supervisor와 같은 프로세스 관리자를 사용해 Reverb 서버를 항상 실행 상태로 유지해야 합니다. Supervisor로 Reverb를 실행하는 경우, 연결 처리를 위해 필요한 열린 파일을 Supervisor가 확보할 수 있도록 서버의 `supervisor.conf` 파일에 `minfds` 설정을 아래와 같이 업데이트해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링 (Scaling)

단일 서버가 허용 가능한 연결 수 이상을 처리해야 한다면, Reverb 서버를 수평으로 확장할 수 있습니다. Redis의 퍼블리시/구독 기능을 이용해 Reverb는 여러 서버 간 연결을 관리합니다. 애플리케이션의 Reverb 서버 중 하나에 메시지가 도착하면, Redis를 통해 이 메시지가 모든 다른 서버로 퍼블리시됩니다.

수평 확장을 활성화하려면 애플리케이션 `.env` 설정 파일에 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 지정하세요:

```env
REVERB_SCALING_ENABLED=true
```

그 다음, 모든 Reverb 서버가 연결할 수 있는 전용 중앙 Redis 서버를 준비해야 합니다. Reverb는 애플리케이션에 기본으로 설정된 [Redis 연결](/docs/12.x/redis#configuration)을 사용해 메시지를 다른 서버로 퍼블리시합니다.

Reverb의 확장 옵션을 활성화하고 Redis 서버를 구성한 후에는, Redis 서버와 통신할 수 있는 여러 서버에서 단순히 `reverb:start` 명령어를 실행하면 됩니다. 이 Reverb 서버들은 적절한 부하 분산 장치 뒤에 배치되어, 들어오는 요청이 모든 서버에 균등하게 분배되도록 해야 합니다.