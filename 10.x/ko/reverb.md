# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
    - [허용된 출처](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [프로덕션 환경에서 Reverb 실행](#production)
    - [열린 파일 수](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb)는 Laravel 애플리케이션에 초고속, 확장 가능한 실시간 WebSocket 통신 기능을 직접 제공하며, Laravel의 기존 이벤트 브로드캐스팅 도구들과 원활하게 통합됩니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Laravel Reverb는 PHP 8.2+ 및 Laravel 10.47+ 버전이 필요합니다.

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Reverb를 설치할 수 있습니다:

```sh
composer require laravel/reverb
```

패키지 설치가 완료되면, Reverb 설치 명령어를 실행하여 설정 파일을 공개하고, 필요한 환경 변수들을 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```sh
php artisan reverb:install
```

<a name="configuration"></a>
## 설정 (Configuration)

`reverb:install` 명령어는 합리적인 기본 옵션 세트를 사용하여 Reverb를 자동으로 설정합니다. 설정을 변경하고 싶다면, 환경 변수 또는 `config/reverb.php` 설정 파일을 수정하여 구성할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명 (Application Credentials)

Reverb에 연결하기 위해서는 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명 세트를 교환해야 합니다. 이 자격 증명은 서버에서 설정되며 클라이언트 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용해 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 출처 (Allowed Origins)

클라이언트 요청이 발생할 수 있는 출처를 제한하려면 `config/reverb.php` 파일의 `apps` 섹션 내 `allowed_origins` 값에 원본 도메인을 지정하세요. 명시되지 않은 출처에서 오는 요청은 거부됩니다. 모든 출처를 허용하려면 `*`를 사용합니다:

```php
'apps' => [
    [
        'id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]
```

<a name="additional-applications"></a>
### 추가 애플리케이션 (Additional Applications)

일반적으로 Reverb는 설치된 애플리케이션 한 개에 대해 WebSocket 서버를 제공합니다. 하지만 단일 Reverb 설치로 여러 애플리케이션에 서비스를 제공하는 것도 가능합니다.

예를 들어, 하나의 Laravel 애플리케이션 내에서 Reverb를 통해 여러 애플리케이션용 WebSocket 연결을 관리하고 싶을 수 있습니다. 이는 `config/reverb.php` 파일에 여러 `apps` 배열을 정의하여 구현할 수 있습니다:

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

대부분의 경우, 안전한 WebSocket 연결(wss)은 상위 웹 서버(Nginx 등)가 처리하며, 요청은 프록시를 거쳐 Reverb 서버로 전달됩니다.

하지만 로컬 개발 환경 등에서는 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 수 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/10.x/valet)에서 [secure 명령어](/docs/10.x/valet#securing-sites)를 실행한 경우, Herd / Valet가 생성한 인증서를 사용해 Reverb 연결을 보안할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트 호스트명으로 설정하거나, Reverb 서버 실행 시 `--hostname` 옵션으로 명시합니다:

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인이 `localhost`로 해석되므로, 위 명령을 실행하면 Reverb 서버가 `wss://laravel.test:8080` 주소로 보안 WebSocket 프로토콜(wss)를 통해 접근 가능합니다.

인증서를 직접 선택하려면 `config/reverb.php` 설정 파일 내 `tls` 옵션 배열에 [PHP SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php) 중 하나를 정의할 수 있습니다:

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

```sh
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 실행되어 모든 네트워크 인터페이스에서 접근 가능합니다.

다른 호스트 또는 포트를 지정하려면 `--host`와 `--port` 옵션을 사용해 서버를 시작하세요:

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수 있습니다.

여기서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT`는 실제 Reverb 서버가 구동되는 호스트와 포트를 지정하는 반면, `REVERB_HOST`와 `REVERB_PORT`는 Laravel이 브로드캐스트 메시지를 전달할 대상 주소를 지시합니다. 예를 들어, 프로덕션 환경에서 공개 Reverb 호스트의 443번 포트로 들어오는 요청을 `0.0.0.0:8080`에서 실행 중인 Reverb 서버로 라우팅할 경우, 환경 변수는 아래와 같이 정의합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅 (Debugging)

성능 향상을 위해 Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. 통과하는 데이터 스트림을 확인하고 싶다면 `reverb:start` 명령에 `--debug` 옵션을 추가하세요:

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작 (Restarting)

Reverb는 장기 실행 프로세스이므로, 코드 변경 사항을 적용하려면 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령은 모든 연결을 원활하게 종료한 후 서버를 중지합니다. Supervisor 같은 프로세스 관리자를 사용 중이라면, 연결 종료 후 서버가 자동으로 재시작됩니다:

```sh
php artisan reverb:restart
```

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행 (Running Reverb in Production)

WebSocket 서버가 장시간 실행되는 특성상, 서버와 호스팅 환경에 최적화 작업을 수행해야 서버 리소스에 맞는 적절한 연결 수를 안정적으로 처리할 수 있습니다.

> [!NOTE]  
> 여러분의 사이트가 [Laravel Forge](https://forge.laravel.com)에서 관리되고 있다면, "Application" 패널에서 Reverb 통합을 활성화하여 자동으로 서버 최적화를 진행할 수 있습니다. Forge는 필요한 확장 설치 및 허용 연결 수 증대 등을 포함해 서버를 프로덕션 준비 상태로 설정합니다.

<a name="open-files"></a>
### 열린 파일 수 (Open Files)

WebSocket 연결은 클라이언트 또는 서버가 연결을 종료할 때까지 메모리에 유지됩니다. 유닉스 계열 운영체제에서는 각 연결이 파일 하나로 표현되며, 운영체제와 애플리케이션 수준에서 열린 파일 수의 제한이 존재합니다.

<a name="operating-system"></a>
#### 운영체제 (Operating System)

유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 열린 파일 수를 확인할 수 있습니다:

```sh
ulimit -n
```

이 명령은 사용자별 열린 파일 수 제한을 출력합니다. `/etc/security/limits.conf` 파일을 수정해 값을 변경할 수 있습니다. 예를 들어, `forge` 사용자에 대해 열린 파일 최대 수를 10,000으로 설정하려면 다음과 같이 작성합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프 (Event Loop)

Reverb는 내부적으로 ReactPHP 이벤트 루프를 사용해 서버에서 WebSocket 연결을 관리합니다. 기본적으로 `stream_select`를 사용하는데, 이 방법은 추가 확장 설치가 필요 없지만 보통 1,024개의 열린 파일까지만 지원합니다. 따라서 1,000개 이상의 동시 연결을 처리하려면 제한이 없는 다른 이벤트 루프를 사용해야 합니다.

Reverb는 사용 가능한 경우 자동으로 `ext-event`, `ext-ev`, 또는 `ext-uv`를 사용하는 이벤트 루프로 전환합니다. 이 PHP 확장들은 모두 PECL을 통해 설치할 수 있습니다:

```sh
pecl install event
# or
pecl install ev
# or
pecl install uv
```

<a name="web-server"></a>
### 웹 서버 (Web Server)

대부분의 경우 Reverb는 서버 내에서 웹이 직접 노출되지 않는 포트에서 실행됩니다. 따라서 Reverb로의 트래픽 라우팅을 위해 리버스 프록시를 설정해야 합니다. Reverb가 `0.0.0.0:8080`에서 실행 중이고, Nginx를 웹 서버로 사용하는 경우, 다음과 같이 리버스 프록시를 구성할 수 있습니다:

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

대부분의 웹 서버는 서버 과부하 방지를 위해 연결 수 제한을 설정합니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일의 `worker_rlimit_nofile`과 `worker_connections` 값을 수정하세요:

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

위 설정은 프로세스당 최대 10,000개의 Nginx 작업자를 생성할 수 있게 하며, 열린 파일 수 제한 또한 10,000으로 설정합니다.

<a name="ports"></a>
### 포트 (Ports)

유닉스 기반 운영체제는 서버에서 열 수 있는 포트의 개수를 제한합니다. 현재 허용 포트 범위는 다음 명령어로 확인할 수 있습니다:

```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

출력 결과는 서버가 최대 28,231개(60,999 - 32,768)의 연결을 처리할 수 있음을 의미합니다. 각 연결마다 사용 가능한 포트가 필요하기 때문입니다. 허용 연결 수를 늘리려면 [수평 확장](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 포트 범위를 확장해 개방 가능한 포트 수를 늘릴 수 있습니다.

<a name="process-management"></a>
### 프로세스 관리 (Process Management)

대부분의 경우 Supervisor 같은 프로세스 관리자를 사용하여 Reverb 서버가 항상 실행 중인지 보장해야 합니다. Supervisor를 사용 중이라면 `supervisor.conf` 파일에서 `minfds` 설정을 10,000 이상으로 조정하여 Supervisor가 Reverb 연결 처리를 위한 파일을 충분히 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링 (Scaling)

단일 서버에서 처리 가능한 연결 수를 넘어야 할 경우, Reverb 서버를 수평 확장할 수 있습니다. Redis의 publish / subscribe 기능을 이용하여 여러 서버 간 연결을 관리할 수 있습니다. 애플리케이션의 한 Reverb 서버가 메시지를 수신하면, Redis를 사용해 모든 다른 서버로 해당 메시지를 브로드캐스트합니다.

수평 확장을 활성화하려면, 애플리케이션 `.env` 파일에 다음 환경 변수를 추가하세요:

```env
REVERB_SCALING_ENABLED=true
```

그 다음, 모든 Reverb 서버가 통신할 전용 중앙 Redis 서버를 준비해야 합니다. Reverb는 애플리케이션에 구성된 [기본 Redis 연결 설정](/docs/10.x/redis#configuration)을 사용해 메시지를 всех Reverb 서버에 전송합니다.

스케일링을 활성화하고 Redis 서버를 구성한 후에는, Redis와 통신 가능한 여러 서버에서 `reverb:start` 명령을 실행하십시오. 이러한 Reverb 서버들은 로드 밸런서 뒤에 위치해 요청을 고르게 분배 받아야 합니다.