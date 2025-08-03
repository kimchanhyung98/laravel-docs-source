# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 요구 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS로 애플리케이션 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [워커 수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [워커 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), 그리고 [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 이용하여 애플리케이션의 성능을 크게 향상시켜 줍니다. Octane은 애플리케이션을 한 번만 부팅해 메모리에 유지한 후, 매우 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후에는 `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 요구 사항 (Server Prerequisites)

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, 얼리 힌트, Brotli, Zstandard 압축과 같은 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 자동으로 해당 바이너리를 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP

[Laravel Sail](/docs/12.x/sail) 환경에서 개발할 계획이라면, 아래 명령어로 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

그 다음, `octane:install` Artisan 명령어로 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스하기 위해 사용하는 명령어입니다:

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

일반적으로, FrankenPHP Sail 애플리케이션에는 `https://localhost`로 접속하세요. `https://127.0.0.1` 사용 시 추가 설정이 필요하며, 이는 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP

FrankenPHP의 공식 Docker 이미지는 성능 향상 및 정적 설치에 포함되지 않은 추가 확장 지원을 제공합니다. 또한 Windows 같은 지원되지 않는 플랫폼에서 FrankenPHP를 실행하도록 지원합니다. 공식 Docker 이미지는 로컬 개발과 프로덕션 환경 모두에 적합합니다.

다음 Dockerfile을 FrankenPHP 기반의 Laravel 애플리케이션 컨테이너화 시작점으로 사용할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # 다른 PHP 확장 추가 가능...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 다음 Docker Compose 파일을 사용해 애플리케이션을 실행할 수 있습니다:

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 넘기면, Octane은 FrankenPHP의 네이티브 로거를 사용하고 별도 설정이 없으면 구조화된 JSON 로그를 생성합니다.

자세한 내용은 [FrankenPHP 공식 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리를 사용합니다. RoadRunner 기반 Octane 서버를 처음 시작하면, Octane이 바이너리를 다운로드하고 설치하도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/12.x/sail) 환경에서 개발할 계획이라면, 다음 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

그 다음 Sail 셸을 실행해 `rr` 실행 파일로 최신 Linux용 RoadRunner 바이너리를 다운로드합니다:

```shell
./vendor/bin/sail shell

# Sail 쉘 내에서...
./vendor/bin/rr get-binary
```

`docker-compose.yml` 파일 내 `laravel.test` 서비스에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션을 Swoole 서버로 서비스할 경우, Swoole PHP 확장 설치가 필요합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 서버를 사용하려면 Open Swoole PHP 확장을 설치해야 합니다. 역시 PECL로 설치합니다:

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용하면, 동시 작업, 틱, 인터벌 등 Swoole이 제공하는 동일한 기능을 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]
> Sail로 Octane 애플리케이션을 서비스하기 전에 Laravel Sail 최신 버전을 사용 중인지 확인하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는 Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail)로 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Sail은 기본적으로 Swoole 확장이 포함되어 있지만, `docker-compose.yml` 수정이 필요합니다.

먼저 `docker-compose.yml`에서 `laravel.test` 서비스에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 실행하는 명령어입니다:

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

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 설정 옵션을 지원합니다. 이 옵션들은 기본 설정 파일에는 포함되어 있지 않으며, 자주 변경하지 않습니다:

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

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에서 지정한 `server` 옵션에 따라 서버를 실행합니다:

```shell
php artisan octane:start
```

기본 포트는 8000번이며, 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS로 애플리케이션 서비스 (Serving Your Application via HTTPS)

기본적으로 Octane으로 실행되는 애플리케이션은 모든 링크에 `http://`가 붙습니다. 애플리케이션의 `config/octane.php` 설정 파일 내 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, Octane이 Laravel에게 모든 링크를 `https://`로 생성하도록 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스 (Serving Your Application via Nginx)

> [!NOTE]
> 직접 서버 설정을 관리하기 어렵거나 복잡한 서비스를 구성하기 부담된다면 [Laravel Cloud](https://cloud.laravel.com)를 이용해 완전관리형 Laravel Octane 서비스를 사용하세요.

운영 환경에서는 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스해야 합니다. 이렇게 하면 웹 서버가 이미지, 스타일시트 같은 정적 자산을 처리하고 SSL 인증서 종료를 관리할 수 있습니다.

아래 예시 Nginx 설정에서는, Nginx가 정적 자산을 서비스하고 8000번 포트에서 실행 중인 Octane 서버로 프록시 요청을 전달합니다:

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

Octane 서버가 시작될 때 애플리케이션이 메모리에 한번 로드되므로, 파일 변경 내용은 브라우저 새로고침 시 바로 반영되지 않습니다. 예를 들어, `routes/web.php`에 새 라우트를 추가해도 서버가 재시작되기 전까지 반영되지 않습니다. 이때 `--watch` 옵션을 사용하면, 애플리케이션 내 파일 변경 시 자동으로 서버를 재시작하도록 할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하려면, 로컬 개발 환경에 [Node](https://nodejs.org) 설치가 필요하며, 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉토리와 파일은 애플리케이션의 `config/octane.php` 설정 파일 내 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 수 지정 (Specifying the Worker Count)

기본적으로 Octane은 머신의 CPU 코어 수만큼 워커를 생성해 요청을 처리합니다. 직접 워커 수를 지정하려면 `octane:start` 명령어 실행 시 `--workers` 옵션을 사용하세요:

```shell
php artisan octane:start --workers=4
```

Swoole 서버를 사용하는 경우, ["task workers"](#concurrent-tasks) 수도 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정 (Specifying the Max Request Count)

Octane은 워커가 500개의 요청을 처리하면 메모리 누수를 방지하기 위해 해당 워커를 우아하게 재시작합니다. 이 값을 조정하려면 `--max-requests` 옵션을 사용하세요:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작 (Reloading the Workers)

배포 이후 새 코드를 메모리에 로드하려면 `octane:reload` 명령어로 애플리케이션 워커를 우아하게 재시작할 수 있습니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지 (Stopping the Server)

Octane 서버를 중지하려면 `octane:stop` Artisan 명령어를 사용하세요:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

현재 Octane 서버 상태는 `octane:status` 명령어로 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번 부팅해 메모리에 유지하며 요청을 처리하기 때문에, 몇 가지 주의할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 워커가 처음 부팅될 때 단 한 번만 실행되고, 이후 요청에는 같은 애플리케이션 인스턴스를 재사용합니다.

따라서 애플리케이션 서비스 컨테이너 또는 요청 인스턴스를 어느 객체의 생성자에 주입할 경우, 이후 요청에서는 오래된 컨테이너나 요청 객체를 참조할 위험이 있습니다.

Octane은 프레임워크 내부 상태는 요청 간에 자동으로 초기화하지만, 글로벌 상태 같은 애플리케이션이 만든 상태는 자동으로 초기화하지 않습니다. 그러므로 Octane 친화적으로 애플리케이션을 설계하는 방법을 알아둘 필요가 있습니다. 아래 절에서는 Octane 사용 시 흔히 문제를 일으킬 수 있는 상황을 정리합니다.

<a name="container-injection"></a>
### 컨테이너 주입 (Container Injection)

일반적으로, 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 아래 코드는 싱글톤 바인딩에서 전체 컨테이너를 주입합니다:

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

이 경우, `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성되면, 이후 요청마다 같은 컨테이너 인스턴스를 참조하게 되어 부트 사이클 후반이나 다음 요청에서 추가된 바인딩을 인식하지 못할 수 있습니다.

해결 방안으로는 싱글톤 대신 바인딩으로 전환하거나, 컨테이너를 필요할 때마다 현재 인스턴스를 반환하는 콜백으로 주입하는 방법이 있습니다:

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

전역 헬퍼 `app`과 `Container::getInstance()`는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입 (Request Injection)

일반적으로, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것은 권장하지 않습니다. 아래는 싱글톤 바인딩에 요청 인스턴스를 넣은 예시입니다:

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

이 경우, `Service` 인스턴스는 부팅 시점의 `request` 인스턴스를 갖게 되어, 이후 요청 시에도 최초 요청 데이터가 유지되어 헤더, 입력, 쿼리 스트링 등 모든 요청 정보가 부정확해집니다.

해결 방법으로는 바인딩을 싱글톤으로 등록하지 않거나, 현재 요청을 매번 반환하는 콜백을 주입하거나, 권장하는 방법으로는 객체 메서드에 필요한 요청 데이터를 런타임에 전달하는 것입니다:

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

전역 헬퍼 `request`는 애플리케이션이 현재 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 괜찮습니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입 (Configuration Repository Injection)

대체로, 설정 저장소 인스턴스를 다른 객체 생성자에 주입하는 것을 피해야 합니다. 예시로, 싱글톤 바인딩에 설정 저장소를 주입하는 경우입니다:

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

이 경우 요청 간에 설정 값이 변경되어도 이 서비스 인스턴스는 생성 시점의 설정 저장소만 참조합니다.

해결책으로는 바인딩을 싱글톤으로 등록하지 않거나, 매번 최신 설정 저장소를 반환하는 콜백을 주입하는 방법이 있습니다:

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

전역 헬퍼 `config`는 항상 최신 설정 저장소 인스턴스를 반환해 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리 (Managing Memory Leaks)

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적으로 유지되는 배열 등에 데이터를 계속 추가하면 메모리 누수가 발생합니다. 예를 들어, 아래 컨트롤러 코드는 요청마다 static `$data` 배열에 데이터를 계속 추가하므로 메모리 누수를 일으킵니다:

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

애플리케이션을 개발할 때는 이런 유형의 메모리 누수를 피하도록 특히 주의해야 합니다. 개발 중에는 메모리 사용량을 모니터링하며 누수를 발생시키지 않는지 확인하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용 시, Octane의 `concurrently` 메서드로 경량 백그라운드 작업을 동시 실행할 수 있습니다. PHP 배열 비구조화 할당과 함께 결과를 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane이 처리하는 동시 작업은 Swoole의 "task workers"에서 실행되며, 메인 요청과 별도의 프로세스에서 동작합니다. 동시 작업 워커 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정 가능합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드에는 Swoole 태스크 시스템 제한으로 최대 1024개 작업까지만 제공하세요.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌 (Ticks and Intervals)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 지정한 초마다 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드에 첫 번째 인자는 틱 이름 문자열, 두 번째 인자는 지정한 간격으로 실행될 콜러블을 넣습니다.

아래 예시는 10초마다 실행되는 클로저를 등록하는 방법입니다. 일반적으로 서비스 프로바이더의 `boot` 메서드 내에서 호출됩니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 추가하면, Octane 서버 부팅 시점과 이후 매 간격마다 즉시 콜백을 실행하도록 할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 초당 최대 200만 회의 읽기/쓰기 속도를 제공하는 Octane 캐시 드라이버를 활용할 수 있습니다. 이 캐시 드라이버는 빠른 읽기/쓰기 성능이 필요한 애플리케이션에 적합합니다.

이 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 서버 내 모든 워커가 데이터를 공유합니다. 그러나 서버 재시작 시 캐시 데이터는 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 허용되는 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌 (Cache Intervals)

Laravel 캐시 시스템의 일반 메서드 외에, Octane 캐시는 간격 기반 캐시를 지원합니다. 이는 지정된 간격으로 자동 갱신되며, 서비스 프로바이더의 `boot` 메서드 내에 등록해야 합니다. 아래 예는 5초마다 갱신되는 캐시입니다:

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

Swoole 사용 시, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 높은 성능을 제공하며, 서버 내 모든 워커가 데이터를 공유합니다. 단, 서버 재시작 시 데이터는 모두 소실됩니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 배열에 정의합니다. 최대 1000행을 지원하는 예제 테이블이 이미 기본 설정에 포함되어 있습니다. 문자열 컬럼의 최대 크기는 아래와 같이 컬럼 타입 뒤에 크기를 명시해 설정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블 접근은 `Octane::table` 메서드를 사용하세요:

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