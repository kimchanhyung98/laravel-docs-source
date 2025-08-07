# Laravel Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 준비 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [워커 개수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [최대 실행 시간 지정](#specifying-the-max-execution-time)
    - [워커 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [Request 주입](#request-injection)
    - [설정 리포지토리 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱(Tick) 및 인터벌(Interval)](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 강력한 애플리케이션 서버를 사용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번만 부팅하여 메모리에 상시 유지한 뒤, 초고속으로 요청을 주입해 서비스합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

Octane을 설치한 후, `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 준비 사항 (Server Prerequisites)

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, Early Hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane은 FrankenPHP 바이너리를 자동으로 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 이용한 FrankenPHP

[Laravel Sail](/docs/12.x/sail)을 사용하여 애플리케이션을 개발하려면, 아래 명령어로 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

이어서, `octane:install` Artisan 명령어를 사용하여 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수에는 Sail이 Octane을 사용해 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3를 활성화하려면 아래와 같이 수정하세요:

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

일반적으로 FrankenPHP Sail 애플리케이션은 `https://localhost`를 통해 접근해야 하며, `https://127.0.0.1`를 사용할 경우 추가 설정이 필요하고 이는 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 이용한 FrankenPHP

FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 더 뛰어나고, 정적 설치에 포함되지 않은 추가 확장기능도 사용할 수 있습니다. 또한 공식 Docker 이미지는 FrankenPHP가 원래 지원하지 않는 Windows와 같은 플랫폼에서도 실행할 수 있도록 해줍니다. FrankenPHP 공식 Docker 이미지는 로컬 개발과 운영 환경 모두에서 사용할 수 있습니다.

FrankenPHP 기반 Laravel 애플리케이션의 컨테이너화를 위한 기본 Dockerfile 예시는 다음과 같습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 아래와 같은 Docker Compose 파일을 사용해 애플리케이션을 실행할 수 있습니다:

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 지정하면, Octane은 FrankenPHP의 기본 로거를 이용하며 별도의 설정이 없다면 구조화된 JSON 로그를 기록합니다.

FrankenPHP를 Docker로 실행하는 방법에 대해 더 알아보려면 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="frankenphp-caddyfile"></a>
#### 사용자 지정 Caddyfile 설정

FrankenPHP를 사용할 때 Octane을 시작하는 시점에 `--caddyfile` 옵션으로 사용자 정의 Caddyfile을 지정할 수 있습니다:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

이를 통해 기본 설정을 넘어 FrankenPHP 구성을 세밀하게 조정할 수 있으며, 사용자 정의 미들웨어 추가, 고급 라우팅 구성, 커스텀 디렉티브 설정 등이 가능합니다. Caddyfile 문법 및 구성 옵션에 대한 자세한 정보는 [공식 Caddy 문서](https://caddyserver.com/docs/caddyfile)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리를 기반으로 동작합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 바이너리를 자동으로 다운로드 및 설치할지 안내해줍니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 이용한 RoadRunner

[Laravel Sail](/docs/12.x/sail)을 사용하여 애플리케이션 개발 시, Octane과 RoadRunner를 다음과 같이 설치합니다:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음으로, Sail 셸을 실행한 뒤 `rr` 실행 파일을 이용해 최신 리눅스 빌드의 RoadRunner 바이너리를 가져옵니다:

```shell
./vendor/bin/sail shell

# Sail shell 안에서...
./vendor/bin/rr get-binary
```

이후, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수에는 Octane이 PHP 개발 서버 대신 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리가 실행 가능하도록 권한을 부여하고, Sail 이미지를 빌드합니다:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 반드시 Swoole PHP 확장(extension)을 설치해야 합니다. 일반적으로 PECL을 통해 다음과 같이 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버로 Laravel Octane을 서비스하려면 Open Swoole PHP 확장을 설치해야 합니다. 역시 PECL을 통해 설치할 수 있습니다:

```shell
pecl install openswoole
```

Laravel Octane에서 Open Swoole을 사용할 경우, Swoole과 동일하게 동시 작업, 틱(Tick), 인터벌(Interval) 기능을 모두 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 이용한 Swoole

> [!WARNING]
> Sail로 Octane 애플리케이션을 서비스하기 전 반드시 Laravel Sail의 최신 버전을 사용하고, 애플리케이션 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행해야 합니다.

또는, [Laravel Sail](/docs/12.x/sail) 공식 Docker 기반 개발 환경에서 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 포함되어 있지만, `docker-compose.yml` 파일의 일부를 수정해야 합니다.

우선, `docker-compose.yml` 파일의 `laravel.test` 서비스 정의 내에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수에는 Octane을 사용해 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 `octane` 설정 파일에서 추가로 지정할 수 있는 몇 가지 옵션을 지원합니다. 대부분 수정이 필요하지 않으므로 기본 설정 파일에는 포함되어 있지 않습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스 (Serving Your Application)

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 브라우저에서 `http://localhost:8000`을 통해 애플리케이션에 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 서비스

Octane으로 실행되는 애플리케이션은 기본적으로 `http://`로 시작하는 링크를 생성합니다. 그러나 `config/octane.php` 설정 파일에서 사용되는 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, HTTPS로 서비스할 때 모든 생성되는 링크에 `https://`가 자동으로 붙도록 할 수 있습니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스

> [!NOTE]
> 서버 구성을 직접 관리하거나, 다양한 서비스들을 직접 설정하는 것이 부담될 경우 [Laravel Cloud](https://cloud.laravel.com)를 고려해보세요. Laravel Cloud는 완전히 관리되는 Laravel Octane 지원을 제공합니다.

운영 환경에서는 Nginx, Apache와 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스하는 것이 좋습니다. 이렇게 하면 이미지, 스타일시트 등 정적 파일을 웹 서버가 서빙하며, SSL 인증서 종료도 관리할 수 있습니다.

아래 Nginx 예제 설정에서는 Nginx가 사이트의 정적 리소스를 서빙하고, 나머지 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```

<a name="watching-for-file-changes"></a>
### 파일 변경 감지

Octane 서버가 시작될 때 애플리케이션은 한 번만 메모리에 로드되므로, 애플리케이션 파일에 변경이 있어도 브라우저를 새로고침했을 때 즉시 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트 정의를 추가해도 서버를 재시작하기 전까지 적용되지 않습니다. 이러한 불편을 해소하기 위해 `--watch` 플래그를 사용하면 애플리케이션 내 파일에 변경이 생길 때마다 Octane이 서버를 자동으로 재시작하도록 할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능 사용 전에는 로컬 개발 환경에 [Node](https://nodejs.org)를 설치해야 하며, 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

어떤 디렉터리와 파일을 감시할지 설정하려면, 애플리케이션의 `config/octane.php` 파일에서 `watch` 설정 옵션을 사용하세요.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정

기본적으로 Octane은 머신의 CPU 코어 개수만큼 요청 워커를 시작합니다. 워커들은 들어오는 HTTP 요청을 처리합니다. 원한다면, `octane:start` 명령어 실행 시 `--workers` 옵션을 사용해 워커 개수를 직접 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용하는 경우, ["Task Worker"](동시 작업 참조) 개수 또한 아래와 같이 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

메모리 누수를 방지하기 위해, Octane은 각 워커가 500개의 요청을 처리하면 워커를 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정 가능합니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
### 최대 실행 시간 지정

Laravel Octane은 기본적으로 애플리케이션의 `config/octane.php` 파일에 있는 `max_execution_time` 옵션을 통해 각 요청에 대한 최대 실행 시간을 30초로 설정합니다:

```php
'max_execution_time' => 30,
```

이 값은 요청이 실행될 수 있는 최대 시간을 초 단위로 의미합니다. 값이 `0`이면 실행 시간 제한이 완전히 비활성화됩니다. 이 옵션은 파일 업로드, 데이터 처리, 외부 서비스 API 호출 등 장시간 실행되는 요청을 처리하는 애플리케이션에서 특히 유용합니다.

> [!WARNING]
> `max_execution_time` 설정을 변경한 경우, 변경 사항이 적용되려면 Octane 서버를 재시작해야 합니다.

<a name="reloading-the-workers"></a>
### 워커 재시작

`octane:reload` 명령어를 사용해 Octane 서버의 애플리케이션 워커를 부드럽게 재시작할 수 있습니다. 보통, 코드 배포 후 새로 배포된 코드가 메모리에 로드되어 이후 요청에 사용될 수 있도록 하기 위해 이 작업을 수행합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어로 Octane 서버를 중지할 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령어를 사용하면 Octane 서버의 현재 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번 부팅한 뒤, 요청을 처리할 때마다 메모리에 유지합니다. 이로 인해 애플리케이션을 개발할 때 몇 가지 유의해야 할 점이 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더 내 `register` 및 `boot` 메서드는 각 워커가 최초 부팅될 때 한 번만 실행됩니다. 이후 요청에서는 동일한 애플리케이션 인스턴스가 재사용됩니다.

이 때문에, 객체의 생성자에서 애플리케이션 서비스 컨테이너 혹은 요청 인스턴스를 주입하면, 이후 요청에서도 오래된 컨테이너 또는 요청이 사용될 수 있습니다.

Octane은 프레임워크 차원의 상태 초기화를 자동으로 처리하지만, 애플리케이션에서 생성된 전역 상태까지는 항상 재설정할 수 없습니다. 따라서 Octane 친화적으로 애플리케이션을 구성하는 방법을 숙지해야 합니다. 아래에서는 Octane 사용 시 문제가 될 수 있는 일반적인 상황들을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로, 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 아래 바인딩은 전체 애플리케이션 서비스 컨테이너를 싱글톤으로 등록되는 객체에 주입합니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```

위 예시에서, 만약 `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성된다면, 해당 서비스 인스턴스는 최초 컨테이너만 유지하고, 이후 요청에서는 변경된 바인딩을 감지하지 못할 수 있습니다.

이러한 경우, 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 항상 최신 컨테이너 인스턴스를 반환하는 클로저를 주입하는 방식으로 우회할 수 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

전역 `app` 헬퍼나 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

<a name="request-injection"></a>
### Request 주입

일반적으로, 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것은 지양해야 합니다. 예시로, 아래 바인딩은 요청 인스턴스를 싱글톤 객체에 주입합니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```

이 경우, `Service` 인스턴스가 애플리케이션 부팅 시점에 생성된다면, 해당 서비스 인스턴스는 최초 요청만 유지하고, 이후 요청에서도 동일 요청 인스턴스를 사용하게 됩니다. 따라서 헤더, 입력값, 쿼리스트링 등 모든 요청 관련 데이터가 잘못될 수 있습니다.

이를 방지하려면, 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 클로저를 주입해 항상 최신 요청 인스턴스를 가져오도록 할 수 있습니다. 가장 권장되는 방법은 필요한 요청 정보를 런타임에 객체의 메서드로 전달하는 것입니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// 또는...

$service->method($request->input('name'));
```

전역 `request` 헬퍼는 항상 현재 애플리케이션이 처리 중인 요청을 반환하므로, 안심하고 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스 타입힌트는 사용해도 괜찮습니다.

<a name="configuration-repository-injection"></a>
### 설정 리포지토리 주입

설정 리포지토리 인스턴스를 다른 객체 생성자에 직접 주입하는 것도 피해야 합니다. 예를 들면, 아래 바인딩은 구성 리포지토리를 싱글톤 객체에 주입합니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```

이 방식으로 객체가 생성될 경우, 요청 간 설정 값이 변경되어도 서비스는 여전히 최초의 설정만 참조합니다.

해결 방법으로는 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 항상 최신 구성 리포지토리를 반환하는 클로저를 주입할 수 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

전역 `config` 헬퍼는 항상 최신 구성 리포지토리를 반환하므로 안전하게 활용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간에도 애플리케이션을 메모리에 유지하므로, 정적으로 유지되는 배열에 데이터를 추가하면 메모리 누수가 발생할 수 있습니다. 아래 컨트롤러 코드는 매 요청마다 static `$data` 배열에 데이터를 누적시켜 메모리 누수를 일으킵니다:

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```

애플리케이션을 만들 때는 이러한 유형의 메모리 누수를 피하는 데 특히 주의해야 하며, 로컬 개발 중 애플리케이션의 메모리 사용량을 모니터링해 새로운 누수가 발생하지 않도록 관리해야 합니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 경우, 경량화된 백그라운드 태스크를 통해 작업을 병렬로 실행할 수 있습니다. Octane의 `concurrently` 메서드를 활용하면 됩니다. PHP 배열 비구조화를 조합하면 각각의 작업 결과를 쉽게 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane에서 처리되는 동시 작업은 Swoole의 "Task Worker"를 이용하며, 요청 처리 프로세스와 완전히 분리된 별도 프로세스에서 실행됩니다. 동시 작업 처리가 가능한 워커 수는 `octane:start` 명령의 `--task-workers` 옵션으로 지정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 호출 시 Swoole Task 시스템의 제약으로 1024개를 초과하는 태스크는 제공하면 안 됩니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick) 및 인터벌(Interval)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 때는 N초마다 지정된 "tick" 작업을 등록할 수 있습니다. `tick` 메서드를 사용해 콜백을 등록할 수 있으며, 첫 번째 인자로 ticker의 이름, 두 번째 인자로 주기적으로 실행할 콜러블을 전달합니다.

아래 예시는 10초마다 클로저를 실행하도록 ticker를 등록하는 방식입니다. 보통 이 코드는 서비스 프로바이더의 `boot` 메서드 안에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버가 최초 부팅될 때 즉시 콜백이 실행된 뒤, N초마다 반복 실행되도록 만들 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 때, Octane 캐시 드라이버를 활용하면 초당 2백만 회 이상의 읽기/쓰기가 가능할 정도로 뛰어난 속도를 자랑합니다. 따라서 극한의 읽기/쓰기 성능이 필요한 캐싱 계층에서 적합합니다.

이 캐시 드라이버는 [Swoole Table](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 합니다. 서버의 모든 워커가 캐시에 저장된 데이터에 접근할 수 있습니다. 단, 서버가 재시작되면 해당 데이터는 모두 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 저장할 수 있는 항목 수의 최대치는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

일반적인 Laravel 캐시 시스템에서 제공하는 메서드와 더불어, Octane 캐시 드라이버는 인터벌 기반 캐시 기능도 제공합니다. 이 캐시는 지정된 주기에 따라 자동으로 새로고침되며, 보통 서비스 프로바이더의 `boot` 메서드 내에서 등록합니다. 아래 예시는 5초마다 새로고침되는 캐시 등록 예시입니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 때는 원하는 구조의 [Swoole Table](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의 및 조작할 수 있습니다. Swoole Table은 매우 뛰어난 성능을 자랑하며, 서버 내 모든 워커에서 해당 데이터에 접근할 수 있습니다. 단, 서버가 재시작되면 테이블 내 데이터는 모두 소멸됩니다.

테이블 정의는 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에서 지정합니다. 1000개의 행을 저장 가능한 테이블 예시가 이미 기본 설정에 포함되어 있습니다. 문자열 컬럼의 최대 크기는 아래와 같이 타입 뒤에 크기를 명시하여 조정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블 데이터에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole Table에서 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.