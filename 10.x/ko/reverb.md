# Laravel Reverb

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 인증 정보](#application-credentials)
    - [허용된 Origin](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [운영환경에서 Reverb 실행](#production)
    - [열린 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 초고속, 확장 가능한 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 이벤트 브로드캐스팅 도구군과 원활하게 통합됩니다.

<a name="installation"></a>
## 설치

> [!WARNING]  
> Laravel Reverb는 PHP 8.2 이상 및 Laravel 10.47 이상이 필요합니다.

Composer 패키지 관리자를 사용하여 Reverb를 Laravel 프로젝트에 설치할 수 있습니다:

```sh
composer require laravel/reverb
```

패키지가 설치되면 Reverb의 설치 명령어를 실행하여 설정 파일을 게시하고, Reverb에 필요한 환경 변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```sh
php artisan reverb:install
```

<a name="configuration"></a>
## 설정

`reverb:install` 명령어는 합리적인 기본 옵션 세트로 Reverb를 자동으로 구성합니다. 설정을 변경하려면 Reverb의 환경 변수 또는 `config/reverb.php` 설정 파일을 수정하면 됩니다.

<a name="application-credentials"></a>
### 애플리케이션 인증 정보

Reverb에 연결하려면 클라이언트와 서버 간에 Reverb "애플리케이션" 인증 정보 집합이 교환되어야 합니다. 이 인증 정보는 서버에 설정되며 클라이언트로부터의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용하여 인증 정보를 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 Origin

클라이언트 요청이 허용될 수 있는 Origin을 `config/reverb.php` 설정 파일 내 `apps` 섹션의 `allowed_origins` 설정 값을 수정하여 지정할 수 있습니다. 허용된 Origin에 포함되지 않은 Origin에서의 모든 요청은 거부됩니다. 모든 Origin을 허용하려면 `*`를 사용할 수 있습니다:

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
### 추가 애플리케이션

일반적으로 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 그러나 하나의 Reverb 인스턴스에서 여러 애플리케이션을 서비스할 수도 있습니다.

예를 들어, 하나의 Laravel 애플리케이션에서 Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하고자 할 수 있습니다. 이는 애플리케이션의 `config/reverb.php` 파일에서 다수의 `apps`를 정의함으로써 가능합니다:

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

대부분의 경우, 보안 WebSocket 연결(wss)은 요청이 Reverb 서버로 프록시 되기 전에 상위 웹 서버(Nginx 등)에 의해 처리됩니다.

그러나 로컬 개발 환경 등에서는 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 수 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능이나 [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행한 경우, 해당 사이트를 위한 Herd / Valet 인증서를 사용해 Reverb 연결을 보안할 수 있습니다. 이때 `REVERB_HOST` 환경 변수를 사이트 호스트명으로 설정하거나, Reverb 서버를 시작할 때 명시적으로 hostname 옵션을 전달할 수 있습니다:

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되므로, 위 명령을 실행하면 보안 WebSocket 프로토콜(wss)로 `wss://laravel.test:8080`에서 Reverb 서버에 접속할 수 있습니다.

또한, 애플리케이션의 `config/reverb.php` 파일 내 `tls` 옵션을 정의하여 인증서를 수동으로 선택할 수도 있습니다. `tls` 옵션 배열에는 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)이 지원하는 모든 옵션을 지정할 수 있습니다:

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

```sh
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접근할 수 있습니다.

사용자 정의 호스트 또는 포트를 지정해야 한다면, 서버 시작 시 `--host`와 `--port` 옵션을 사용할 수 있습니다:

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 설정 파일에서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수 있습니다.

`REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT`와 `REVERB_HOST`, `REVERB_PORT` 환경 변수는 혼동하지 마세요. 전자는 Reverb 서버 자체가 구동될 호스트와 포트를 지정하고, 후자는 Laravel이 브로드캐스트 메시지를 전송할 위치를 지정합니다. 예를 들어, 운영환경에서는 퍼블릭 Reverb 호스트명(포트 443)에서  `0.0.0.0:8080`으로 요청을 라우팅할 수 있습니다. 이와 같은 경우, 환경 변수는 다음과 같이 정의합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능을 높이기 위해 Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. Reverb 서버를 통과하는 데이터 스트림을 확인하고 싶다면 `reverb:start` 명령어에 `--debug` 옵션을 사용할 수 있습니다:

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 장시간 실행되는 프로세스이므로 코드 변경 사항이 서버에 반영되려면 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 서버를 중지하기 전에 모든 연결을 우아하게 종료합니다. Supervisor와 같은 프로세스 관리자를 사용해 Reverb를 실행하는 경우, 모든 연결이 종료된 후 프로세스 관리자가 서버를 자동으로 재시작합니다:

```sh
php artisan reverb:restart
```

<a name="production"></a>
## 운영환경에서 Reverb 실행

WebSocket 서버의 장시간 실행 특성상, 서버와 호스팅 환경을 최적화하여 사용 가능한 자원 내에서 최적의 연결 수를 효과적으로 처리할 수 있도록 해야 합니다.

> [!NOTE]  
> 사이트가 [Laravel Forge](https://forge.laravel.com)로 관리되고 있다면, "Application" 패널에서 바로 Reverb에 맞춰 서버를 최적화할 수 있습니다. Reverb 통합을 활성화하면, Forge는 필요한 확장 설치 및 허용 연결 수 증대 등 서버 환경을 운영에 맞게 자동으로 준비해줍니다.

<a name="open-files"></a>
### 열린 파일

각 WebSocket 연결은 클라이언트 또는 서버에서 연결을 끊을 때까지 메모리에 유지됩니다. Unix 및 유사 Unix 환경에서는 각 연결이 파일로 표현됩니다. 그러나 운영체제와 애플리케이션 수준 모두에서 열 수 있는 파일 수에 제한이 있습니다.

<a name="operating-system"></a>
#### 운영체제

Unix 기반 운영체제에서는 `ulimit` 명령어로 열린 파일의 최대 개수를 확인할 수 있습니다:

```sh
ulimit -n
```

이 명령어는 각 사용자에 허용된 열린 파일의 수를 표시합니다. 이 값은 `/etc/security/limits.conf` 파일을 편집하여 변경할 수 있습니다. 예를 들어, `forge` 사용자에 대해 열린 파일 최대값을 10,000으로 설정하려면 다음과 같이 합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

Reverb는 내부적으로 서버에서 WebSocket 연결을 관리하기 위해 ReactPHP 이벤트 루프를 사용합니다. 기본 이벤트 루프는 `stream_select`로 동작하며, 별도의 확장이 필요하지 않습니다. 그러나 `stream_select`는 일반적으로 열 수 있는 파일이 1,024개로 제한됩니다. 1,000개 이상의 동시 연결을 처리하려면 동일한 제한을 받지 않는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 이용 가능한 경우 `ext-event`, `ext-ev`, 또는 `ext-uv` 확장에서 제공하는 루프로 자동 전환합니다. 이들 PHP 확장모듈은 모두 PECL로 설치할 수 있습니다:

```sh
pecl install event
# 또는
pecl install ev
# 또는
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 경우 Reverb는 서버의 외부와 직접 연결되지 않는 포트에서 구동됩니다. Reverb로 트래픽을 라우팅하려면 리버스 프록시를 설정해야 합니다. 예를 들어, Reverb가 호스트 `0.0.0.0`의 포트 `8080`에서 구동되고, 서버에서 Nginx 웹 서버를 사용하고 있다면 아래와 같은 Nginx 사이트 설정을 통해 Reverb 서버에 대한 리버스 프록시를 구성할 수 있습니다:

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

보통, 웹 서버는 과부하를 방지하기 위해 허용되는 연결 수를 제한하는 설정이 있습니다. Nginx 웹 서버에서 허용 연결 수를 10,000개로 늘리려면, `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음처럼 수정해야 합니다:

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

위 설정은 프로세스 당 최대 10,000개의 Nginx 워커가 생성될 수 있게 하며, Nginx의 열린 파일 제한도 10,000개로 설정합니다.

<a name="ports"></a>
### 포트

Unix 기반 운영체제는 서버에서 열 수 있는 포트의 수를 제한합니다. 현재 허용된 범위는 다음 명령어로 확인할 수 있습니다:

 ```sh
 cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 결과에 따르면 서버는 최대 28,231개(60,999 - 32,768) 연결을 처리할 수 있습니다. 각 연결에 포트가 필요하므로 그렇습니다. 더 많은 연결을 지원하려면 [수평 확장](#scaling)을 권장하지만, `/etc/sysctl.conf` 설정 파일의 허용 포트 범위를 변경하여 사용할 수 있는 포트 수를 늘릴 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우, Supervisor 같은 프로세스 관리자를 사용해 Reverb 서버가 지속적으로 실행되도록 해야 합니다. Supervisor에서 Reverb를 실행하는 경우, Supervisor가 Reverb 서버에 필요한 연결 파일을 열 수 있도록 `supervisor.conf` 파일의 `minfds` 설정을 아래와 같이 수정해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

단일 서버가 허용할 수 있는 것보다 더 많은 연결을 처리해야 한다면, Reverb 서버를 수평 확장할 수 있습니다. Redis의 publish / subscribe 기능을 활용해 Reverb는 여러 서버에서 연결을 관리할 수 있습니다. 애플리케이션의 Reverb 서버 하나에서 메시지를 받으면, 해당 서버가 Redis를 통해 들어온 메시지를 다른 모든 서버에 게시하게 됩니다.

수평 확장을 활성화하려면 애플리케이션의 `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

다음으로 모든 Reverb 서버가 통신할 수 있는 전용 중앙 Redis 서버를 두어야 합니다. Reverb는 [애플리케이션에 기본으로 설정된 Redis 연결](/docs/{{version}}/redis#configuration)을 사용하여 메시지를 모든 Reverb 서버에 게시합니다.

Reverb의 스케일링 옵션을 활성화하고 Redis 서버를 설정한 후에는, Redis 서버와 통신할 수 있는 여러 서버에서 `reverb:start` 명령어를 실행하면 됩니다. 이러한 Reverb 서버들은 로드밸런서 뒤에 배치되어 들어오는 요청을 균등하게 분산 처리하게 됩니다.