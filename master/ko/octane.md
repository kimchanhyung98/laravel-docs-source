# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 요구사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서빙](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 서빙](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서빙](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [워커 개수 지정](#specifying-the-worker-count)
    - [최대 요청 개수 지정](#specifying-the-max-request-count)
    - [워커 리로드](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 리포지토리 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블(Table)](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 활용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 유지하며, 초고속으로 요청을 전달합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 매니저로 설치할 수 있습니다:

```shell
composer require laravel/octane
```

Octane 설치 후, `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 요구사항

> [!WARNING]
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/)이 필요합니다.

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버이며, Early Hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane 설치 과정에서 FrankenPHP를 서버로 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드하여 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Lavavel Sail](/docs/{{version}}/sail)을 활용해 개발할 경우, 아래 명령어로 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

이후 `octane:install` Artisan 명령어로 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 구동할 명령을 담고 있습니다:

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

일반적으로 FrankenPHP Sail 애플리케이션은 `https://localhost`로 접속해야 하며, `https://127.0.0.1` 사용은 추가 설정이 필요하므로 [지양됩니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP 공식 Docker 이미지를 사용하면 성능이 개선되고, FrankenPHP의 정적 설치에 포함되어 있지 않은 확장도 사용할 수 있습니다. 또한 공식 이미지는 Windows와 같이 네이티브 지원하지 않는 플랫폼에서 FrankenPHP 실행을 지원합니다. 이 Docker 이미지는 로컬 개발 및 운영 환경 모두에 적합합니다.

아래 Dockerfile 예제를 시작점으로 활용할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 시에는 다음과 같은 Docker Compose 파일을 사용할 수 있습니다:

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

`php artisan octane:start` 명령에 `--log-level` 옵션을 명시적으로 전달하면, Octane은 FrankenPHP의 기본 로거를 사용해 구조화된 JSON 로그를 생성합니다(별도로 설정하지 않았다면).

Docker에서 FrankenPHP 사용에 관한 자세한 내용은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리로 구동됩니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane이 RoadRunner 바이너리를 다운로드 및 설치할지 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Lavavel Sail](/docs/{{version}}/sail)로 개발할 경우, 아래 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

이후, Sail 셸을 열어서 `rr` 실행 파일을 사용해 최신 리눅스용 RoadRunner 바이너리를 받아옵니다:

```shell
./vendor/bin/sail shell

# Sail 셸 내에서...
./vendor/bin/rr get-binary
```

그리고 `docker-compose.yml`의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리에 실행 권한을 주고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Octane을 실행하려면 Swoole PHP 확장 설치가 필요합니다. 일반적으로 PECL로 설치합니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 서버를 활용하려면 Open Swoole PHP 확장을 설치해야 합니다. 마찬가지로 PECL을 사용할 수 있습니다:

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용하면, Swoole에서 제공하는 동시 작업, 틱, 인터벌 등의 동일한 기능을 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole 사용

> [!WARNING]
> Sail을 통해 Octane 애플리케이션을 구동하기 전에, Laravel Sail을 최신 버전으로 업데이트하고 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는 [Laravel Sail](/docs/{{version}}/sail)에서 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Sail은 Swoole 확장을 기본적으로 포함하고 있습니다. 단, `docker-compose.yml` 파일에 추가 설정이 필요합니다.

시작하려면 다음처럼 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 빌드합니다:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 `octane` 설정 파일에 추가 옵션을 지정할 수 있습니다. 이들은 변경이 드물어 기본 설정 파일에는 포함되어 있지 않습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 서빙

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 옵션에서 지정한 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 구동하므로, 브라우저에서 `http://localhost:8000`으로 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 서빙

기본적으로 Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, Octane이 모든 링크를 `https://`로 생성하도록 라라벨에 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서빙

> [!NOTE]
> 자체 서버 설정이나 서비스 설정이 숙련되지 않았다면, 완전 관리형 Octane 환경을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 확인하세요.

운영 환경에서는 Octane 애플리케이션을 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 서빙해야 합니다. 이를 통해 정적 에셋(이미지, 스타일시트 등)을 웹 서버가 처리하고, SSL 인증서 종료 과정을 제어할 수 있습니다.

아래 Nginx 설정 예시는 사이트의 정적 에셋은 Nginx가 서빙하고, 나머지 요청을 8000번 포트에서 구동 중인 Octane 서버로 프록시하는 방식입니다:

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

Octane 서버가 시작될 때 애플리케이션이 메모리에 적재되므로, 파일을 수정해도 브라우저 새로고침 시 바로 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가해도 서버를 재시작하기 전까진 반영되지 않습니다. 이를 간편하게 하기 위해, `--watch` 플래그를 사용하면 애플리케이션 파일의 변경이 감지될 때마다 Octane이 자동으로 재시작됩니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에, 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 합니다. 또한 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일은 애플리케이션의 `config/octane.php` 파일에서 `watch` 설정 옵션을 통해 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정

Octane은 기본적으로 시스템의 CPU 코어 개수만큼 요청 워커를 시작합니다. 워커들은 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령 실행 시 `--workers` 옵션을 통해 시작할 워커 수를 수동으로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 서버를 사용한다면 ["태스크 워커"](#concurrent-tasks) 개수도 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 개수 지정

메모리 누수를 방지하기 위해 Octane은 각 워커가 500개의 요청을 처리하면 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 리로드

`octane:reload` 명령어로 Octane 서버의 워커를 우아하게 재시작할 수 있습니다. 보통 신규 배포 후 새 코드를 메모리에 반영하고 이후 요청에 사용하려면 이 기능을 이용합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어로 Octane 서버를 종료할 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령어로 현재 Octane 서버의 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번만 부팅하고 요청 처리 시 메모리에 유지합니다. 이에 따라 다음과 같은 몇 가지 주의사항이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 워커가 처음 부팅될 때 단 한 번만 실행됩니다. 이후 요청에서는 동일한 애플리케이션 인스턴스가 재사용됩니다.

따라서 애플리케이션 서비스 컨테이너 또는 요청(Request)을 객체의 생성자에 주입하는 경우 주의해야 합니다. 이렇게 하면 이후 요청에서 해당 객체는 이전 상태의 컨테이너나 요청을 사용하게 될 수 있습니다.

Octane은 기본 프레임워크의 상태는 자동으로 리셋해주지만, 애플리케이션에서 생성한 전역 상태는 Octane이 자동으로 리셋하지 못할 수 있습니다. Octane 친화적으로 애플리케이션을 설계해야 하며, 아래에 대표적인 문제 상황을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로, 애플리케이션 서비스 컨테이너(또는 HTTP 요청 인스턴스)를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 바인딩은 전체 컨테이너를 싱글턴으로 주입합니다:

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

이 예시에서, `Service` 인스턴스가 부트 과정 중 생성된다면, 컨테이너는 서비스에 주입되고 이후 요청에서도 같은 컨테이너가 재사용됩니다. 이는 특정 상황에서는 문제가 나타나지 않을 수도 있지만, 부트 주기 중에 추가된 바인딩이나 이후 추가된 바인딩을 Service에서 사용할 수 없게 만들 수 있습니다.

해결책으로는 싱글턴 바인딩을 중지하거나, 항상 최신 컨테이너 인스턴스를 반환하는 클로저를 주입하는 방법이 있습니다:

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

글로벌 `app` 헬퍼나 `Container::getInstance()`는 항상 최신 컨테이너를 반환하므로 안전하게 사용할 수 있습니다.

<a name="request-injection"></a>
### 요청 주입

역시, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 객체 생성자에 주입하는 것도 피하세요. 예를 들어, 아래는 전체 Request 인스턴스를 싱글턴으로 주입합니다:

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

이 예시에서, `Service` 인스턴스가 부트 과정에서 생성된다면, HTTP Request가 서비스에 주입되고 이후 요청들도 같은 요청 인스턴스를 재사용하게 됩니다. 따라서 헤더, 입력값, 쿼리스트링 등 모든 요청 관련 정보가 잘못되게 됩니다.

해결책으로는 싱글턴 바인딩을 중지하거나, 항상 최신 요청 인스턴스를 반환하는 클로저를 주입하거나, 가장 권장되는 방법으로 객체의 메서드에 필요한 요청 정보를 런타임에 전달하는 것입니다:

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청을 반환하므로 애플리케이션에서 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 타입힌트를 사용하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 리포지토리 주입

일반적으로 설정 리포지토리 인스턴스를 다른 객체의 생성자에 주입하는 것도 피해야 합니다. 아래는 설정 리포지토리를 싱글턴으로 주입하는 예시입니다:

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

이 예시에서, 만약 요청 간에 설정 값이 변경된다면, 서비스는 새로운 값을 사용할 수 없게 됩니다(초기 리포지토리에 의존하기 때문).

해결책으로는 싱글턴 바인딩을 중지하거나, 항상 최신 설정 리포지토리를 반환하는 클로저를 클래스에 주입하면 됩니다:

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

글로벌 `config`는 항상 최신 설정 리포지토리를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간에도 애플리케이션을 메모리에 유지합니다. 따라서 정적(static) 배열 등에 데이터를 쌓으면 메모리 누수가 발생하게 됩니다. 예를 들어, 아래 컨트롤러는 매번 요청 시마다 static `$data` 배열에 데이터를 추가하여 메모리 누수를 일으킵니다:

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

애플리케이션을 개발할 때에는 이러한 메모리 누수가 발생하지 않도록 각별히 주의해야 합니다. 개발 중에는 애플리케이션의 메모리 사용량을 꼭 관찰하여 메모리 누수를 방지하세요.

<a name="concurrent-tasks"></a>
## 동시 작업

> [!WARNING]
> 해당 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 경량 백그라운드 태스크를 통해 동시에 여러 작업을 실행할 수 있습니다. Octane의 `concurrently` 메서드를 이용하여 아래와 같이 여러 연산 결과를 한 번에 병렬로 가져올 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane이 처리하는 동시 태스크는 Swoole의 "태스크 워커"를 사용하며, 각각은 요청과는 별개 프로세스에서 실행됩니다. 태스크 워커 개수는 `octane:start` 명령의 `--task-workers` 옵션으로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 호출 시 Swoole의 태스크 시스템 제한으로 1024개 이하의 태스크만 지정해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌

> [!WARNING]
> 해당 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 주기적으로 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드를 통해 틱 콜백을 등록할 수 있으며, 첫 번째 인자는 틱 이름, 두 번째는 콜백 함수입니다.

아래 예시는 10초마다 콜백을 실행하도록 등록한 것입니다. 일반적으로 `boot` 메서드에서 호출합니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버가 처음 부팅될 때 즉시 틱 콜백을 실행하게 설정할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]
> 해당 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시 Octane 캐시 드라이버를 사용할 수 있습니다. 이 드라이버는 초당 최대 2백만 회의 읽기/쓰기 성능을 제공하므로, 초고속 캐싱이 필요한 애플리케이션에 적합합니다.

Octane 캐시는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 저장된 데이터는 모든 워커에서 접근 가능합니다. 하지만 서버가 재시작될 경우 데이터는 모두 사라집니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시 허용 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 인터벌 캐시

Laravel의 일반 캐시 메서드 외에도, Octane 캐시 드라이버는 특정 주기로 자동 갱신되는 인터벌 캐시를 제공합니다. 이들은 서비스 프로바이더의 `boot` 메서드에서 등록하는 것이 좋습니다. 아래 캐시는 5초마다 데이터가 갱신됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블(Table)

> [!WARNING]
> 해당 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 빠른 성능을 제공하며, 테이블의 데이터는 모든 워커가 공유할 수 있습니다. 단, 서버 리스타트 시 데이터는 모두 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에 정의합니다. 1000개 행을 허락하는 예시 테이블이 이미 설정되어 있습니다. 문자열 컬럼의 최대 길이는 아래와 같이 타입 뒤에 지정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다:

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