# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 요구사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [워커(Worker) 수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [워커 리로드](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 리포지토리 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업(Concurrent Tasks)](#concurrent-tasks)
- [틱(Tick)과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)은 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 사용하여 라라벨 애플리케이션의 성능을 대폭 향상시킵니다. Octane은 애플리케이션을 한 번 부팅하여 메모리에 유지하고, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 이용해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후, `octane:install` 아티즌(Artisan) 명령어를 실행하면 Octane 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 요구사항

> [!WARNING]  
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/)이 필요합니다.

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP

[Laravel Sail](/docs/{{version}}/sail)로 애플리케이션을 개발하려면, 다음 명령어를 통해 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` 아티즌 명령어에 `--server=frankenphp` 옵션을 사용해 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 사용하여 애플리케이션을 서비스하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3 활성화가 필요하다면 다음과 같이 수정하세요:

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

일반적으로 `https://localhost`로 FrankenPHP Sail 애플리케이션에 접속해야 하며, `https://127.0.0.1` 사용은 추가 구성 필요로 인해 [비추천](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker)됩니다.

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP

FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 향상되며, FrankenPHP의 정적 설치에 포함되지 않은 추가 확장도 사용할 수 있습니다. 또한 공식 Docker 이미지를 통해 Windows와 같이 FrankenPHP가 기본적으로 지원하지 않는 플랫폼에서도 실행이 가능합니다. 공식 Docker 이미지는 로컬 개발 및 운영 환경에 모두 적합합니다.

FrankenPHP를 사용하는 Laravel 애플리케이션을 컨테이너화할 때 아래의 Dockerfile 예제를 참고할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # 다른 PHP 확장도 여기에 추가...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 다음과 같은 Docker Compose 파일로 실행할 수 있습니다:

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

`php artisan octane:start` 명령에 `--log-level` 옵션을 명시적으로 전달하면 Octane은 FrankenPHP의 네이티브 로거를 사용하며, 별도의 설정이 없다면 구조화된 JSON 로그를 생성합니다.

Docker 환경에서 FrankenPHP를 사용하는 추가 정보는 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리를 기반으로 작동합니다. RoadRunner 기반 Octane 서버를 처음 시작하면 Octane이 바이너리 다운로드 및 설치를 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/{{version}}/sail)로 개발하려면, 다음 명령어를 통해 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음으로 Sail 쉘을 실행한 뒤, `rr` 실행파일로 Linux 기반 최신 RoadRunner 바이너리를 받으세요:

```shell
./vendor/bin/sail shell

# Sail 쉘 내부에서...
./vendor/bin/rr get-binary
```

그리고, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 아래와 같이 추가합니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로, `rr` 바이너리의 실행 권한을 부여한 뒤, Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Laravel Octane을 서비스하려면 Swoole PHP 확장을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장도 설치해야 하며, PECL로 설치할 수 있습니다:

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용할 때도 Swoole에서 제공하는 동시 작업, 틱, 인터벌 등의 기능을 동일하게 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]  
> Sail로 Octane 애플리케이션을 서비스하기 전에, 최신 버전의 Laravel Sail을 사용하고, 애플리케이션 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는, 공식 Docker 기반 개발 환경인 [Laravel Sail](/docs/{{version}}/sail)을 이용하여 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 설치되어 있으나, `docker-compose.yml` 파일에 추가적인 설정이 필요합니다.

먼저, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요:

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

Swoole은 추가로 몇 가지 설정 옵션을 지원하며, 필요시 `octane` 설정 파일에 추가할 수 있습니다. 이러한 옵션은 기본 설정 파일에는 포함되어 있지 않지만, 수정이 필요할 땐 아래와 같이 설정할 수 있습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스

Octane 서버는 `octane:start` 아티즌 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에 명시된 서버를 사용합니다:

```shell
php artisan octane:start
```

별도 설정이 없으면 Octane은 8000번 포트로 서버를 구동하므로, 웹 브라우저에서 `http://localhost:8000`을 통해 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 서비스

기본적으로 Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. `OCTANE_HTTPS` 환경 변수를 `config/octane.php` 설정 파일에서 `true`로 지정하면 HTTPS를 통한 서비스 시 생성되는 모든 링크에 `https://` 프리픽스가 붙도록 할 수 있습니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 서비스

> [!NOTE]  
> 자체 서버 구성이 익숙하지 않거나 여러 서비스를 직접 관리하고 싶지 않다면 [Laravel Forge](https://forge.laravel.com) 사용을 권장합니다.

프로덕션 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 제공해야 합니다. 이를 통해 정적 자산(이미지, 스타일시트 등) 제공이 가능하고, SSL 인증서 종료도 관리할 수 있습니다.

아래는 Nginx로 사이트의 정적 자산을 제공하면서 8000번 포트에서 실행 중인 Octane 서버로 프록시하는 예제 설정입니다:

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

Octane 서버가 시작될 때 애플리케이션이 한 번만 로드되어 메모리에 유지되므로, 파일을 수정해도 바로 적용되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가해도 서버를 재시작하기 전까지는 반영되지 않습니다. 이런 문제를 해결하고 싶다면, `--watch` 플래그를 사용해 애플리케이션 내 파일 변경을 감지하여 서버를 자동 재시작할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전, 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트에도 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 파일 및 디렉터리는 애플리케이션의 `config/octane.php` 설정 파일 내 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커(Worker) 수 지정

기본적으로 Octane은 시스템의 각 CPU 코어마다 하나의 애플리케이션 요청 워커를 시작합니다. 이 워커들은 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령 실행 시 `--workers` 옵션을 통해 시작할 워커 수를 직접 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용한다면 ["작업 워커"](concurrent-tasks) 수를 추가로 지정할 수도 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

메모리 누수를 방지하기 위해 Octane은 각 워커가 500개의 요청을 처리하면 워커를 우아하게 재시작시킵니다. 이 수치는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 리로드

`octane:reload` 명령어로 Octane 서버의 애플리케이션 워커를 우아하게 재시작할 수 있습니다. 주로 배포 이후, 새로 배포된 코드가 메모리에 반영되어 다음 요청부터 적용되도록 할 때 사용합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` 아티즌 명령어로 Octane 서버를 중지할 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` 아티즌 명령어로 현재 Octane 서버의 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번 부팅하여 요청을 처리하는 동안 메모리에 유지하기 때문에, 애플리케이션 개발 시 몇 가지 주의사항이 있습니다. 예를 들어, 서비스 프로바이더의 `register` 및 `boot` 메서드는 요청 워커가 최초 부팅될 때 한 번만 실행됩니다. 이후 요청에서 같은 애플리케이션 인스턴스가 재사용됩니다.

따라서, 애플리케이션 서비스 컨테이너나 요청 객체를 생성자에 주입하는 경우, 해당 객체가 다음 요청에서 오래된 컨테이너나 요청 인스턴스를 참조할 수 있으니 주의해야 합니다.

Octane은 기본적으로 프레임워크의 상태를 각 요청마다 초기화하지만, 여러분의 애플리케이션에서 생성된 글로벌 상태까지 항상 리셋할 순 없습니다. 아래에서 Octane에서 문제가 발생할 수 있는 흔한 상황 및 해결 방법을 다룹니다.

<a name="container-injection"></a>
### 컨테이너 주입

원칙적으로 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 아래의 바인딩은 전체 서비스 컨테이너를 싱글톤으로 등록된 객체에 주입합니다:

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

이 예제에서 `Service` 인스턴스가 애플리케이션 부팅 중에 해석되면 컨테이너가 서비스에 주입되고, 이후 요청에서도 같은 컨테이너 인스턴스가 사용됩니다. 이로 인해 부팅 주기 후반 혹은 후속 요청에서 새로 추가된 바인딩이 누락될 수 있습니다.

해결책으로, 바인딩을 싱글톤으로 등록하지 않거나, 현재 컨테이너 인스턴스를 항상 참조하는 클로저로 주입할 수 있습니다:

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
### 요청 주입

마찬가지로 HTTP 요청 인스턴스를 싱글톤 객체의 생성자에 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 다음과 같이 요청 객체를 싱글톤에 주입할 수 있습니다:

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

이 경우, 서비스가 부팅 시점에 해석되면 해당 HTTP 요청이 서비스에 주입되고 이후 요청에서도 같은 요청 인스턴스를 참조하게 되어, 모든 헤더, 입력 및 쿼리스트링 등 요청 데이터가 잘못 됩니다.

해결 방안으로는 바인딩을 싱글톤으로 등록하지 않거나, 현재 요청 인스턴스를 항상 참조하는 클로저로 주입하는 방법이 있습니다. 또는, 가장 권장되는 방법은, 필요한 요청 정보를 런타임에 해당 객체의 메서드로 전달하는 것입니다:

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

글로벌 `request` 헬퍼는 애플리케이션이 현재 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]  
> `Illuminate\Http\Request` 타입힌트를 컨트롤러 메서드와 라우트 클로저에서 사용하는 것은 안전합니다.

<a name="configuration-repository-injection"></a>
### 설정 리포지토리 주입

마찬가지로, 설정 리포지토리 인스턴스를 다른 객체의 생성자에 주입하는 것도 일반적으로 권장되지 않습니다. 예를 들어, 아래와 같이 구성 리포지토리를 싱글톤 객체에 주입하는 바인딩이 있습니다:

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

이 예제에서 요청 간 설정값이 변경되어도, 해당 서비스는 초기 설정 리포지토리 인스턴스만 참조하므로 새로운 값을 알 수 없습니다.

해결책으로, 바인딩을 싱글톤으로 하지 않거나, 항상 현재 설정 리포지토리 인스턴스를 참조하는 클로저로 주입할 수 있습니다:

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

글로벌 `config` 헬퍼를 사용하면 항상 최신 설정 리포지토리를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적 배열 등에 데이터를 추가하면 메모리 누수가 발생합니다. 예를 들어, 아래의 컨트롤러는 요청마다 static `$data` 배열에 데이터가 계속 추가되어 메모리 누수가 발생합니다:

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

애플리케이션을 개발할 때 이러한 유형의 메모리 누수를 만들지 않도록 각별히 주의해야 합니다. 로컬 개발 환경에서 애플리케이션의 메모리 사용량을 반드시 모니터링 하세요.

<a name="concurrent-tasks"></a>
## 동시 작업(Concurrent Tasks)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때는 경량화된 백그라운드 작업을 통해 동시 처리가 가능합니다. Octane의 `concurrently` 메서드를 사용해 이를 구현할 수 있습니다. PHP 배열 디스트럭처링과 함께 사용해 각 작업 결과를 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업(Concurrent Task)은 Swoole의 "task worker"를 활용하며, 요청과는 완전히 다른 프로세스에서 실행됩니다. 동시 작업을 처리할 수 있는 워커 수는 `octane:start` 명령의 `--task-workers` 옵션으로 지정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드를 사용할 때는 Swoole의 task 시스템 제한으로 인해 1024개를 초과하지 않도록 해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick)과 인터벌

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 지정된 초마다 실행되는 "tick(틱)" 작업을 등록할 수 있습니다. `tick` 메서드를 통해 틱 콜백을 등록합니다. 첫 번째 인수는 틱커 이름, 두 번째 인수는 일정 주기마다 호출되는 콜러블입니다.

예를 들어, 아래는 10초마다 콜백을 실행합니다(일반적으로 `boot` 메서드 내에서 등록):

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버 부팅 시 즉시 콜백을 실행한 후, 지정한 주기마다 반복 실행할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때는 Octane 캐시 드라이버를 활용할 수 있습니다. 이 드라이버는 초당 최대 2백만 건의 읽기/쓰기 성능을 제공하므로, 극한의 캐시 속도가 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 서버 내 모든 워커가 데이터를 공유할 수 있습니다. 단, 서버가 재시작되면 모든 캐시 데이터는 삭제됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]  
> Octane 캐시에 허용되는 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

일반적인 캐시 메서드 외에도 Octane 캐시 드라이버는 주기적으로 새로고침되는 인터벌 캐시를 지원합니다. 이런 캐시는 지정된 초마다 자동 갱신되며, 서비스 프로바이더의 `boot` 메서드 내에서 등록하는 것이 좋습니다. 예를 들어, 아래의 캐시는 5초마다 갱신됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용하면, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 높은 성능을 제공하며, 서버 내 모든 워커가 데이터를 공유할 수 있습니다. 단, 서버가 재시작되면 테이블 내 데이터가 모두 삭제됩니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 배열에서 정의합니다. 최대 행 개수가 1000개인 예제 테이블이 기본 설정되어 있습니다. 문자열 컬럼의 최대 크기도 아래와 같이 지정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메서드를 사용하세요:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]  
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.
