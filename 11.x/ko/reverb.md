# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
    - [허용된 Origin](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행하기](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션 환경에서 Reverb 실행하기](#production)
    - [열린 파일(Open Files)](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 초고속이면서 확장 가능한 실시간 WebSocket 통신 기능을 Laravel 애플리케이션에 직접 제공하며, Laravel에서 제공하는 기존 [이벤트 브로드캐스팅 도구](/docs/{{version}}/broadcasting)와 완벽하게 통합됩니다.

<a name="installation"></a>
## 설치

`install:broadcasting` 아티즌(Artisan) 명령어를 사용하여 Reverb를 설치할 수 있습니다:

```
php artisan install:broadcasting
```

<a name="configuration"></a>
## 설정

`install:broadcasting` 아티즌 명령어는 내부적으로 `reverb:install` 명령어를 실행하여, 적절한 기본 설정으로 Reverb를 설치합니다. 설정을 변경하고 싶다면, Reverb 환경 변수 또는 `config/reverb.php` 설정 파일을 수정하십시오.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명

Reverb와의 연결을 맺기 위해서는 클라이언트와 서버 간에 "애플리케이션" 자격 증명이 교환되어야 합니다. 이 자격 증명은 서버에 설정되며 클라이언트 요청의 유효성을 검증하는 데 사용됩니다. 다음 환경 변수를 통해 자격 증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 Origin

클라이언트 요청을 허용할 Origin을 `config/reverb.php` 파일의 `apps` 섹션 내 `allowed_origins` 설정값에 추가할 수 있습니다. 이 목록에 없는 Origin에서 오는 요청은 거부됩니다. 모든 Origin을 허용하려면 `*`을 사용하십시오:

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

일반적으로 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 인스턴스로 여러 애플리케이션을 서비스할 수도 있습니다.

예를 들어, 하나의 Laravel 애플리케이션이 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하고 싶을 수 있습니다. 이 경우, `config/reverb.php` 파일에서 여러 개의 `apps`를 정의하면 됩니다:

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

대부분의 경우, 보안 WebSocket 연결은 upstream 웹 서버(Nginx 등)에서 처리한 뒤, 요청이 Reverb 서버로 프록시됩니다.

하지만, 로컬 개발 등에서 Reverb 서버가 직접 보안 연결을 처리해야 할 경우가 있습니다. 만약 [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/{{version}}/valet)에서 애플리케이션에 [secure 명령](/docs/{{version}}/valet#securing-sites)을 실행했다면, 사이트의 인증서를 사용해 Reverb 연결을 보호할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트 호스트명으로 지정하거나, Reverb 서버 시작 시 명시적으로 hostname 옵션을 전달하세요:

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되기 때문에 위 명령을 실행하면 `wss://laravel.test:8080` 주소로 보안 WebSocket 프로토콜(`wss`)을 통해 Reverb 서버에 접근할 수 있습니다.

또한 인증서를 직접 선택하고 싶을 경우, `config/reverb.php` 파일에 `tls` 옵션을 정의할 수 있습니다. 이 배열에는 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)이 지원하는 옵션을 사용할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행하기

Reverb 서버는 `reverb:start` 아티즌 명령어로 실행할 수 있습니다:

```sh
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되어, 모든 네트워크 인터페이스에서 접속할 수 있습니다.

특정 host나 port를 지정하려면, 서버 시작 시 `--host` 및 `--port` 옵션을 사용하세요:

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 파일에 `REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT`는, `REVERB_HOST`와 `REVERB_PORT`와 혼동하지 마세요. 앞의 두 변수는 Reverb 서버 자체가 열릴 호스트와 포트를 지정하며, 뒤의 두 변수는 Laravel이 브로드캐스트 메시지를 보낼 주소를 지정합니다. 예를 들어, 운영 환경에서 public Reverb 호스트네임(포트 443)에서 요청을 받아 `0.0.0.0:8080`의 Reverb 서버로 라우팅할 수 있습니다. 이때 환경 변수는 다음처럼 지정됩니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능 향상을 위해, Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. 서버를 통과하는 데이터 스트림을 확인하려면, `reverb:start` 명령에 `--debug` 옵션을 추가하세요:

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 장시간 실행되는 프로세스이기 때문에, 코드 변경 사항이 즉시 반영되지 않습니다. 따라서 변경 반영을 위해 `reverb:restart` 아티즌 명령어로 서버를 재시작하세요.

`reverb:restart` 명령은 모든 연결을 정상적으로 종료한 후 서버를 중지합니다. Supervisor와 같은 프로세스 매니저에서 Reverb를 실행 중인 경우, 모든 연결 종료 후 프로세스 매니저가 자동으로 서버를 다시 시작합니다:

```sh
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링

Reverb는 [Laravel Pulse](/docs/{{version}}/pulse)와의 통합을 통해 모니터링할 수 있습니다. Pulse 통합을 활성화하면, 서버에서 처리되는 연결 및 메시지 수를 추적할 수 있습니다.

통합을 활성화하려면 먼저 [Pulse를 설치](/docs/{{version}}/pulse#installation)해야 합니다. 이후, Reverb의 레코더를 `config/pulse.php` 설정 파일에 추가하세요:

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

그리고 Pulse 대시보드에 각각의 레코더 카드를 추가하세요:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. Pulse 대시보드에서 올바르게 정보를 렌더링하려면, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. [수평 스케일링](#scaling) 구성에서는 한 서버에서만 이 데몬을 실행하십시오.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행하기

WebSocket 서버의 장시간 실행 특성상, 서버가 사용 가능한 리소스 내에서 최적의 연결 수를 효율적으로 처리하도록 서버 및 환경을 최적화해야 할 수도 있습니다.

> [!NOTE]
> [Laravel Forge](https://forge.laravel.com)로 사이트를 관리하는 경우, "애플리케이션" 패널에서 Reverb 최적화를 자동으로 적용할 수 있습니다. Reverb 통합을 활성화하면, 서버에 필요한 확장 모듈 설치부터 연결 수 증가 등 프로덕션 준비 환경 구성이 자동으로 이루어집니다.

<a name="open-files"></a>
### 열린 파일(Open Files)

각 WebSocket 연결은 클라이언트 또는 서버가 연결을 종료할 때까지 메모리에 유지됩니다. 유닉스 및 유닉스 계열 환경에서는 각 연결이 파일로 표현됩니다. 하지만 운영체제와 애플리케이션 수준에서 허용되는 열린 파일 제한이 존재할 수 있습니다.

<a name="operating-system"></a>
#### 운영체제

유닉스 기반 운영체제에서는 `ulimit` 명령어로 열린 파일 수 제한을 확인할 수 있습니다:

```sh
ulimit -n
```

이 명령은 각 사용자에 대해 허용된 열린 파일 제한을 표시합니다. `/etc/security/limits.conf` 파일을 수정하여 값을 변경할 수 있습니다. 예를 들어 `forge` 사용자에 대해 열린 파일 최대치를 10,000으로 설정하려면 다음과 같이 작성합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용하여 WebSocket 연결을 관리합니다. 기본적으로 이 이벤트 루프는 추가 확장 모듈 없이 사용할 수 있는 `stream_select`로 동작하지만, 이는 1,024개의 열린 파일 제한이 있습니다. 1,000개 이상의 동시 연결을 처리하려면 동일한 제약을 받지 않는 다른 이벤트 루프를 사용해야 합니다.

`ext-uv` PHP 확장 기능이 설치되어 있으면, Reverb는 자동으로 이 확장 기반 루프로 전환됩니다. PECL을 통해 설치할 수 있습니다:

```sh
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 경우 Reverb는 서버의 웹 노출이 되지 않는 포트에서 실행됩니다. 따라서 트래픽을 Reverb로 라우팅하기 위해 리버스 프록시를 구성해야 합니다. 예를 들어 Reverb가 `0.0.0.0` 호스트, 8080 포트에서 실행되고, 서버가 Nginx를 사용하는 경우, 다음과 같은 Nginx 사이트 구성으로 리버스 프록시를 만들 수 있습니다:

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
> Reverb는 `/app` URI에서 WebSocket 연결을, `/apps` URI에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버가 이 두 URI를 모두 서비스할 수 있도록 해야 합니다. [Laravel Forge](https://forge.laravel.com)로 서버를 관리하는 경우, 관련 설정이 기본으로 적용되어 있습니다.

일반적으로 웹 서버는 서버 오버로드를 방지하기 위해 연결 수를 제한합니다. Nginx 웹 서버에서 10,000개의 연결을 허용하려면 `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 수정하세요:

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

이 설정으로 프로세스마다 최대 10,000개의 Nginx 워커가 생성될 수 있으며, open file limit도 10,000개로 설정됩니다.

<a name="ports"></a>
### 포트

유닉스 기반 운영체제는 보통 서버에서 열 수 있는 포트 수에 제한이 있습니다. 현재 허용 범위는 아래 명령어로 확인할 수 있습니다:

```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력은 각 연결마다 포트가 필요하기 때문에 최대 28,231개(60,999 - 32,768) 연결을 지원함을 의미합니다. 더 많은 연결을 원한다면 [수평 스케일링](#scaling)을 권장하며, 사용 가능한 포트 범위는 `/etc/sysctl.conf` 파일에서 조정할 수 있습니다.

<a name="process-management"></a>
### 프로세스 관리

Reverb 서버가 계속 실행되도록 하기 위해 Supervisor와 같은 프로세스 매니저를 사용하는 것이 좋습니다. Supervisor에서 Reverb를 실행하는 경우, Supervisor가 필요한 파일 수를 열 수 있도록 `supervisor.conf`의 `minfds` 설정을 업데이트해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

단일 서버에서 감당할 수 있는 연결 수를 초과해야 할 경우, Reverb 서버를 수평적으로 확장할 수 있습니다. Reverb는 Redis의 pub/sub 기능을 활용하여 여러 서버간 연결을 관리합니다. 한 서버가 메시지를 수신하면, 해당 메시지를 Redis를 통해 다른 모든 서버에 전파합니다.

수평 스케일링을 활성화하려면, `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

그리고 모든 Reverb 서버가 통신할 수 있도록 전용 중앙 Redis 서버를 준비해야 합니다. Reverb는 [애플리케이션에서 설정한 기본 Redis 연결](/docs/{{version}}/redis#configuration)을 사용하여 모든 서버에 메시지를 브로드캐스트합니다.

이제 스케일링 옵션을 활성화하고 Redis 서버를 구성했다면, Redis 서버와 통신할 수 있는 여러 서버에서 각각 `reverb:start` 명령을 실행하면 됩니다. 이들 Reverb 서버는 앞단의 로드 밸런서 뒤에 두어 들어오는 요청이 균등하게 분산되도록 합니다.