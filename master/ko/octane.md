# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 전제 조건](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통해 애플리케이션 서비스하기](#serving-your-application-via-https)
    - [Nginx를 통해 애플리케이션 서비스하기](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [작업자 수 지정하기](#specifying-the-worker-count)
    - [최대 요청 수 지정하기](#specifying-the-max-request-count)
    - [작업자 재시작하기](#reloading-the-workers)
    - [서버 중지하기](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 리포지토리 주입](#configuration-repository-injection)
- [메모리 누수 관리하기](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Octane](https://github.com/laravel/octane)은 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 강력한 애플리케이션 서버를 활용해 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번만 부팅하여 메모리에 유지한 후, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후에는 `octane:install` Artisan 명령어를 실행해 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 전제 조건 (Server Prerequisites)

> [!WARNING]
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/)를 필요로 합니다.

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 자동으로 FrankenPHP 바이너리를 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP

[Laravel Sail](/docs/master/sail)을 사용해 개발할 계획이라면, 다음 명령어를 실행하여 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

그다음 `octane:install` Artisan 명령어로 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 이용해 애플리케이션을 서비스할 때 사용하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3를 활성화하려면 다음과 같이 수정하세요:

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

일반적으로 FrankenPHP Sail 애플리케이션에는 `https://localhost`로 접근하는 것이 좋으며, `https://127.0.0.1` 사용은 추가 설정이 필요하며 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP

FrankenPHP 공식 Docker 이미지는 정적 설치 버전에서 누락된 확장 프로그램 지원과 더 나은 성능을 제공합니다. 또한 Windows와 같이 공식적으로 지원하지 않는 플랫폼에서도 실행할 수 있게 도와줍니다. 공식 이미지는 로컬 개발과 프로덕션 모두에 적합합니다.

다음 Dockerfile을 시작점으로 사용해 FrankenPHP를 이용한 Laravel 애플리케이션 컨테이너를 만들 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 다음 Docker Compose 파일을 활용해 애플리케이션을 실행할 수 있습니다:

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달하면 Octane은 FrankenPHP의 기본 로거를 사용하며, 별도 설정이 없으면 구조화된 JSON 로그를 생성합니다.

더 자세한 Docker 환경에서 FrankenPHP 실행 정보는 [공식 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리를 사용합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 RoadRunner 바이너리를 다운로드 및 설치할지 묻습니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/master/sail)을 사용하는 경우, 다음 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

그런 다음 Sail 셸을 시작해 `rr` 실행 파일을 사용해 최신 Linux용 RoadRunner 바이너리를 받으세요:

```shell
./vendor/bin/sail shell

# Sail 셸 내부...
./vendor/bin/rr get-binary
```

애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 이용해 애플리케이션을 서비스할 때 사용하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

`rr` 바이너리가 실행 가능하도록 권한을 부여하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션을 Swoole 서버로 서비스하려면 Swoole PHP 확장 프로그램을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 서버를 사용하려면 Open Swoole PHP 확장을 설치해야 합니다. PECL을 통해 설치하는 것이 일반적입니다:

```shell
pecl install openswoole
```

Open Swoole을 Laravel Octane과 함께 사용하면, 동시 작업, 틱, 인터벌과 같은 Swoole이 제공하는 기능을 똑같이 누릴 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]
> Sail을 통한 Octane 애플리케이션 서비스를 시작하기 전에, Laravel Sail 최신 버전인지 확인하고 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache` 명령을 실행하세요.

Swoole 기반 Octane 애플리케이션은 Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/master/sail)로 개발할 수 있습니다. Sail은 기본적으로 Swoole 확장을 포함하지만, `docker-compose.yml` 파일을 조정해야 합니다.

먼저 `docker-compose.yml` 파일 내 `laravel.test` 서비스에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이는 Sail이 PHP 개발 서버 대신 Octane을 이용해 애플리케이션을 서비스할 때 사용하는 명령어입니다:

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

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 구성 옵션을 지원합니다. 이 옵션들은 기본 설정 파일에는 포함되지 않습니다.

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

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 애플리케이션의 `octane` 설정 파일 내 `server` 옵션에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 브라우저에서 `http://localhost:8000`으로 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통해 애플리케이션 서비스하기

기본적으로 Octane에서 실행되는 애플리케이션은 `http://` 접두사가 붙은 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일 내 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, Octane은 Laravel에게 모든 생성된 링크에 `https://` 접두사를 붙이라고 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통해 애플리케이션 서비스하기

> [!NOTE]
> 만약 직접 서버 설정을 관리할 준비가 안 되어 있거나, 견고한 Laravel Octane 애플리케이션 운영에 필요한 다양한 서비스 설정이 익숙하지 않다면, 완전 관리형 Laravel Octane 지원을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보시기 바랍니다.

운영 환경에서는 Nginx 또는 Apache 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스하는 것이 좋습니다. 이렇게 하면 웹 서버가 이미지, 스타일시트 같은 정적 자산을 제공하고 SSL 인증서 종료를 관리할 수 있습니다.

아래 Nginx 설정 예시에서는 Nginx가 사이트의 정적 자산을 서비스하고, 포트 8000번에서 실행 중인 Octane 서버에 요청을 프록시합니다:

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
### 파일 변경 감시 (Watching for File Changes)

Octane 서버가 시작될 때 애플리케이션을 메모리에 한 번만 로드하기 때문에, 애플리케이션 파일 변경 사항은 브라우저 새로 고침 시 곧바로 반영되지 않습니다. 예를 들어 `routes/web.php`에 경로 정의를 추가해도 서버를 재시작해야 적용됩니다.

편의를 위해 `--watch` 플래그를 사용하면 애플리케이션 내 파일 변경이 감지될 때 자동으로 서버를 재시작하도록 Octane에 지시할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에, 로컬 개발 환경에 [Node](https://nodejs.org)를 설치해야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉토리와 파일은 애플리케이션의 `config/octane.php` 설정 파일 내 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 작업자 수 지정하기 (Specifying the Worker Count)

기본적으로 Octane은 머신의 CPU 코어 수만큼의 요청 작업자를 시작합니다. 이 작업자들이 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령어 실행 시 `--workers` 옵션으로 작업자 수를 직접 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 서버를 사용할 경우, ["task workers"](#concurrent-tasks) 수 또한 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정하기 (Specifying the Max Request Count)

메모리 누수 방지 차원에서, Octane은 작업자가 500개의 요청을 처리하면 작업자를 점진적으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 작업자 재시작하기 (Reloading the Workers)

배포 후 새로 배포한 코드가 메모리에 반영되도록 Octane 서버 작업자들을 점진적으로 재시작할 수 있습니다. `octane:reload` 명령어를 사용하세요:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지하기 (Stopping the Server)

Octane 서버를 중지하려면 다음 Artisan 명령어를 실행하세요:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인하기 (Checking the Server Status)

현재 Octane 서버 상태는 `octane:status` Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번만 부팅해 메모리에 유지하며 요청을 처리하므로, 애플리케이션을 구축할 때 유의할 점이 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더 `register`와 `boot` 메서드는 요청 작업자가 처음 부팅될 때 한 번만 실행됩니다. 이후 요청에서는 동일한 애플리케이션 인스턴스를 재사용합니다.

따라서 애플리케이션 서비스 컨테이너나 요청(HTTP Request)을 객체 생성자에 주입하는 경우, 이후 요청에서 오래된(스테일) 버전의 컨테이너나 요청 데이터를 가지게 될 수 있어 조심해야 합니다.

Octane은 기본 프레임워크 상태는 요청 간에 자동으로 재설정하지만, 애플리케이션이 생성하는 전역 상태는 항상 알 수 없습니다. 따라서 Octane 친화적으로 애플리케이션을 작성하는 방법을 숙지해야 합니다. 아래에서 Octane 사용 시 흔히 문제를 일으키는 사례들을 다룹니다.

<a name="container-injection"></a>
### 컨테이너 주입 (Container Injection)

일반적으로 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체 생성자에 직접 주입하는 것을 피해야 합니다. 다음 예시는 애플리케이션 서비스 컨테이너를 단일 인스턴스로 바인딩된 객체 생성자에 주입하는 코드입니다:

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

예를 들어, `Service` 인스턴스가 애플리케이션 부팅 시 생성되면, 같은 컨테이너 인스턴스가 이후 요청에서도 `Service` 객체에 유지됩니다. 특정 애플리케이션에는 문제가 없을 수 있으나, 부팅 이후에 새로 추가된 바인딩을 컨테이너가 알지 못하는 문제를 일으킬 수 있습니다.

해결책으로는 바인딩을 단일 인스턴스(singleton)로 등록하지 않거나, 현재 컨테이너 인스턴스를 항상 반환하는 클로저를 서비스에 주입하는 방법이 있습니다:

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

글로벌 `app` 헬퍼 함수와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입 (Request Injection)

일반적으로 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체 생성자에 직접 주입하는 것을 피해야 합니다. 다음 예시는 HTTP 요청 인스턴스를 단일 인스턴스로 바인딩된 객체 생성자에 주입하는 경우입니다:

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

이 경우, `Service` 인스턴스가 애플리케이션 부팅 시 생성되면, 그 요청 인스턴스가 이후 요청 시에도 유지되어 헤더, 입력값, 쿼리 문자열 등 요청 관련 데이터가 부정확합니다.

해결방법은 바인딩을 단일 인스턴스로 등록하지 않거나, 현재 요청 인스턴스를 반환하는 클로저를 서비스에 주입하는 방법, 혹은 가장 권장하는 방법으로는 특정 요청 정보를 런타임에 메서드 인수로 전달하는 것입니다:

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드와 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 리포지토리 주입 (Configuration Repository Injection)

일반적으로 설정 리포지토리 인스턴스를 다른 객체 생성자에 직접 주입하는 것을 피해야 합니다. 예를 들어 다음 코드는 설정 리포지토리를 단일 인스턴스 객체에 주입하는 사례입니다:

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

요청 간에 설정 값이 변경되면, 이 서비스에서는 원래 주입된 리포지토리 인스턴스를 참조하여 최신 값을 얻지 못합니다.

해결책은 바인딩을 단일 인스턴스로 등록하지 않거나, 설정 리포지토리 인스턴스를 반환하는 클로저를 주입하는 방법입니다:

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

글로벌 `config` 헬퍼는 항상 최신 설정 리포지토리를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리하기 (Managing Memory Leaks)

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, static 배열에 데이터를 계속 추가하면 메모리 누수가 발생합니다. 다음 컨트롤러 예시는 요청이 올 때마다 static `$data` 배열에 데이터를 추가하여 메모리 누수가 발생하는 사례입니다:

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

애플리케이션을 구축할 때는 이런 메모리 누수를 조심해야 하며, 로컬 개발 중에 메모리 사용량을 모니터링하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 경우, Octane의 `concurrently` 메서드를 통해 경량 백그라운드 작업을 동시에 실행할 수 있습니다. PHP 배열 구조 분해와 함께 사용해 각 작업 결과를 받는 것도 가능합니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업은 Swoole의 "task workers"를 이용해 요청과는 별도의 프로세스에서 실행됩니다. 동시 작업 처리용 작업자 수는 `octane:start` 명령어의 `--task-workers` 옵션을 통해 설정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 호출 시 Swoole 작업 시스템의 제한으로 1024개를 초과하는 작업은 제공하지 않는 것이 좋습니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌 (Ticks and Intervals)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 지정한 초마다 실행되는 "틱" 작업을 등록할 수 있습니다. `tick` 메서드로 틱 콜백을 등록하며, 첫 번째 인수는 틱 이름, 두 번째 인수는 지정된 인터벌마다 호출될 콜러블입니다.

예시에서는 10초마다 호출되는 클로저를 등록합니다. 일반적으로 `tick` 메서드는 애플리케이션 서비스 프로바이더 `boot` 메서드 내부에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 함께 사용하면 Octane 서버가 처음 부팅되는 즉시 틱 콜백을 실행하고, 이후 N초마다 반복 호출하도록 할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 초당 200만 건 이상의 읽기/쓰기 속도를 제공하는 Octane 캐시 드라이버를 활용할 수 있습니다. 뛰어난 캐시 입출력 성능이 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반이며, 서버 내 모든 작업자가 캐시된 데이터를 공유합니다. 하지만 서버 재시작 시 캐시 데이터는 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시의 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌 (Cache Intervals)

Laravel 캐시 시스템의 일반 메서드 외에도, Octane 캐시 드라이버는 인터벌 기반 캐시를 지원합니다. 지정된 인터벌마다 자동으로 갱신되며, 애플리케이션 서비스 프로바이더 `boot` 메서드에서 등록해야 합니다. 다음 예시는 5초마다 갱신되는 캐시입니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 상호작용할 수 있습니다. Swoole 테이블은 높은 성능 처리량을 제공하며 서버 내 모든 작업자가 해당 데이터에 접근할 수 있지만, 서버 재시작 시 데이터는 삭제됩니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 배열에서 정의합니다. 최대 1000행을 허용하는 샘플 테이블이 기본적으로 포함되어 있습니다. 문자열 컬럼 크기는 컬럼 타입 뒤에 크기를 명시해 설정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블 접근은 `Octane::table` 메서드를 사용합니다:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole 테이블이 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.