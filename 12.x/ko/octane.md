# Laravel Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 준비 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스하기](#serving-your-application)
    - [HTTPS로 애플리케이션 서비스하기](#serving-your-application-via-https)
    - [Nginx로 애플리케이션 서비스하기](#serving-your-application-via-nginx)
    - [파일 변경 감지하기](#watching-for-file-changes)
    - [워커 수 지정하기](#specifying-the-worker-count)
    - [최대 요청 수 지정하기](#specifying-the-max-request-count)
    - [최대 실행 시간 지정하기](#specifying-the-max-execution-time)
    - [워커 재시작하기](#reloading-the-workers)
    - [서버 중지하기](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱(tick) 및 인터벌(interval)](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 사용하여 여러분의 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 최초에 한 번 실행해 메모리에 상주시킨 뒤, 매우 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

Octane을 설치한 후, `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 준비 사항

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, Early Hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Lavel Sail](/docs/12.x/sail)을 사용해 애플리케이션을 개발할 예정이라면, 다음 명령어를 실행하여 Octane과 FrankenPHP를 설치할 수 있습니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치하세요.

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스하는 데 사용하는 명령어가 됩니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3를 활성화하려면 아래와 같이 수정합니다.

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

일반적으로 `https://localhost`를 통해 FrankenPHP Sail 애플리케이션에 접근해야 하며, `https://127.0.0.1`는 추가 설정이 필요하므로 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 향상되며, 정적 설치판에 포함되지 않은 추가 확장도 사용할 수 있습니다. 또한 공식 Docker 이미지는 FrankenPHP가 기본적으로 지원하지 않는 Windows와 같은 플랫폼에서도 구동할 수 있습니다. FrankenPHP 공식 Docker 이미지는 로컬 개발과 프로덕션 환경 모두에 적합합니다.

FrankenPHP로 구동되는 Laravel 애플리케이션을 컨테이너화하기 위해 아래 Dockerfile을 참고할 수 있습니다.

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 아래 Docker Compose 파일을 사용해 애플리케이션을 실행할 수 있습니다.

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달할 경우, Octane은 FrankenPHP의 기본 로거를 사용하고, 별도로 설정하지 않았다면 구조화된 JSON 로그를 생성합니다.

Docker로 FrankenPHP를 실행하는 방법에 대한 자세한 내용은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리를 이용합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane이 자동으로 RoadRunner 바이너리를 다운로드 및 설치할 수 있도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Laravel Sail](/docs/12.x/sail)로 애플리케이션 개발을 계획 중이라면, 아래 명령어를 사용하여 Octane과 RoadRunner를 설치하세요.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음으로 Sail 셸을 실행하고, `rr` 실행 파일을 사용하여 최신 Linux용 RoadRunner 바이너리를 받으세요.

```shell
./vendor/bin/sail shell

# Sail 셸 내부에서...
./vendor/bin/rr get-binary
```

그 후, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스하기 위한 명령어를 담고 있습니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로, `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지 빌드를 수행하세요.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션을 Swoole 애플리케이션 서버로 서비스하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다.

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Laravel Octane 애플리케이션을 Open Swoole 애플리케이션 서버로 서비스하려면 Open Swoole PHP 확장 모듈을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다.

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용하면 Swoole이 제공하는 동시 작업, 틱(tick), 인터벌 등과 동일한 기능을 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole 사용

> [!WARNING]
> Octane 애플리케이션을 Sail로 서비스하기 전에, Laravel Sail의 최신 버전을 사용하고, 애플리케이션 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는, [Laravel Sail](/docs/12.x/sail) (Laravel의 공식 Docker 기반 개발 환경)을 이용하여 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail에는 기본적으로 Swoole 확장 모듈이 포함되어 있습니다. 하지만 Sail의 `docker-compose.yml` 파일을 수정해야 합니다.

먼저, `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 PHP 개발 서버 대신 Octane을 사용해 애플리케이션을 서비스하는 명령어가 됩니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로, Sail 이미지를 빌드합니다.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 추가 옵션을 지원합니다. 이 옵션들은 자주 변경할 필요가 없으므로 기본 설정 파일에는 포함되어 있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스하기

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 이 명령어는 기본적으로 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 사용합니다.

```shell
php artisan octane:start
```

기본적으로 Octane은 8000 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS로 애플리케이션 서비스하기

기본적으로 Octane으로 실행 중인 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, HTTPS로 서비스할 때 모든 링크가 `https://`로 생성되도록 할 수 있습니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx로 애플리케이션 서비스하기

> [!NOTE]
> 직접 서버 설정을 관리하길 원하지 않거나 Laravel Octane 애플리케이션을 robust하게 운영하는 데 필요한 여러 서비스를 설정하는 데 익숙하지 않은 경우, [Laravel Cloud](https://cloud.laravel.com)의 완전관리형 Laravel Octane 지원을 참고하세요.

운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 기존 웹 서버 뒤에서 서비스하는 것이 좋습니다. 이렇게 하면 웹 서버가 정적 에셋(이미지, 스타일시트 등) 제공과 SSL 인증서 종료를 담당할 수 있습니다.

아래 Nginx 설정 예제에서, Nginx는 사이트의 정적 에셋을 서비스하고, Octane 서버(8000 포트)로 요청을 프록시합니다.

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
### 파일 변경 감지하기

Octane 서버가 시작될 때 애플리케이션이 메모리에 로드되므로, 애플리케이션 파일을 수정해도 브라우저를 새로고침하는 것만으로 변경사항이 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가하더라도 서버를 재시작하기 전까지 변경사항이 적용되지 않습니다. 이러한 불편함을 해소하기 위해 `--watch` 플래그를 사용하면 애플리케이션의 파일이 변경될 때마다 Octane이 자동으로 서버를 재시작할 수 있습니다.

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에는 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, [Chokidar](https://github.com/paulmillr/chokidar) 파일 감지 라이브러리를 프로젝트에 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

감시할 디렉토리 및 파일은 애플리케이션의 `config/octane.php` 설정 파일의 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 수 지정하기

기본적으로 Octane은 머신의 CPU 코어 수만큼 애플리케이션 요청 워커를 실행합니다. 이 워커들은 각기 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령어 실행 시 `--workers` 옵션을 사용해 직접 워커 수를 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용하는 경우, ["작업 워커(task workers)"](#concurrent-tasks) 수도 추가로 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정하기

메모리 누수를 방지하기 위해, Octane은 각 워커가 500번의 요청을 처리하면 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
### 최대 실행 시간 지정하기

Laravel Octane은 애플리케이션의 `config/octane.php` 설정 파일에서 `max_execution_time` 옵션을 통해 기본적으로 30초의 최대 요청 실행 시간을 지정합니다.

```php
'max_execution_time' => 30,
```

이 설정값은 외부 서비스 API 호출이나 파일 업로드, 데이터 처리 등 장시간 실행되는 요청을 처리하는 애플리케이션에 유용합니다. `0`으로 설정하면 실행 시간 제한이 완전히 비활성화됩니다.

> [!WARNING]
> `max_execution_time` 설정을 변경한 경우, 변경사항이 적용되려면 Octane 서버를 반드시 재시작해야 합니다.

<a name="reloading-the-workers"></a>
### 워커 재시작하기

`octane:reload` 명령어를 통해 Octane 서버의 애플리케이션 워커를 우아하게 재시작할 수 있습니다. 일반적으로 배포 후 새로운 코드를 메모리로 로드하여 이후 요청부터 적용되도록 할 때 사용합니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지하기

`octane:stop` Artisan 명령어로 Octane 서버를 중지할 수 있습니다.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인하기

`octane:status` Artisan 명령어로 Octane 서버의 현재 상태를 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 최초에 한 번만 부팅하고, 요청을 처리하는 동안 계속 메모리에 유지합니다. 따라서 애플리케이션을 개발할 때 몇 가지 주의할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅될 때 한 번만 실행됩니다. 그 이후의 요청에서는 동일한 애플리케이션 인스턴스가 재사용됩니다.

이 때문에, 애플리케이션의 서비스 컨테이너나 요청(request)을 어떤 객체의 생성자(constructor)에 주입할 경우, 이후 요청에서 해당 객체가 오래된 컨테이너나 요청을 참조하게 될 수 있습니다.

Octane은 라라벨 내부의 프레임워크 상태는 요청마다 자동으로 초기화하지만, 여러분의 애플리케이션이 만든 전역 상태까지는 항상 초기화하지 못할 수 있습니다. 따라서 Octane 친화적인 방식으로 애플리케이션을 개발하는 방법을 숙지해야 합니다. 여기서는 Octane 사용 시 문제가 될 수 있는 일반적인 상황을 다룹니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로, 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 바인딩은 전체 서비스 컨테이너를 싱글톤으로 바인딩된 객체에 주입합니다.

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

이 예시에서 `Service` 인스턴스가 애플리케이션 부팅 도중에 생성되었다면, 컨테이너가 서비스에 주입되고 이후 요청마다 동일한 컨테이너 인스턴스가 계속 사용됩니다. 이는 여러분의 애플리케이션에서 문제를 일으키지 않을 수도 있지만, 부팅 과정 또는 이후의 요청에서 추가된 바인딩이 누락되는 등 예기치 않은 현상이 발생할 수도 있습니다.

대안으로, 바인딩을 싱글톤이 아닌 일반 바인딩으로 변경하거나, 항상 최신 컨테이너를 반환하는 클로저를 객체에 주입하는 방식으로 해결할 수 있습니다.

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

전역 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

<a name="request-injection"></a>
### 요청 주입

일반적으로, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 바인딩은 요청 인스턴스를 싱글톤으로 바인딩된 객체에 주입합니다.

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

이 예시에서 `Service` 인스턴스가 애플리케이션 부팅 도중에 생성되었다면, HTTP 요청이 서비스에 주입되고 이후 요청마다 동일한 요청 인스턴스가 계속 사용됩니다. 이로 인해 모든 헤더, 입력값, 쿼리스트링 등 요청 데이터가 잘못될 수 있습니다.

해결 방법으로는 바인딩을 싱글톤으로 등록하지 않거나, 항상 최신 요청을 참조하는 클로저를 객체에 주입하는 방법, 또는 런타임에 필요한 요청 데이터만 객체의 메서드에 전달하는 것이 가장 추천되는 방식입니다.

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

전역 `request` 헬퍼는 항상 현재 애플리케이션이 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트로 받는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

일반적으로, 설정 저장소 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 바인딩은 설정 저장소를 싱글톤으로 바인딩된 객체에 주입합니다.

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

이 예시에서, 만약 설정값이 요청 중간에 변경된다면 해당 서비스는 변경된 값을 사용할 수 없습니다. 이는 원본 저장소 인스턴스에 의존하기 때문입니다.

대안으로, 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 항상 최신 설정 저장소를 반환하는 클로저를 객체에 주입할 수 있습니다.

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

전역 `config` 헬퍼는 언제나 최신 설정 저장소 인스턴스를 반환하므로, 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 사이에 애플리케이션을 메모리에 유지합니다. 때문에, 정적으로 유지되는 배열 등에 데이터를 계속 추가하면 메모리 누수가 발생하게 됩니다. 아래 컨트롤러 예시는 각 요청마다 static `$data` 배열에 값을 추가하므로 메모리 누수가 발생합니다.

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

애플리케이션을 개발할 때 이러한 종류의 메모리 누수가 발생하지 않도록 주의해야 하며, 로컬 개발 중 애플리케이션의 메모리 사용량을 점검해 새로운 누수가 생기지는 않는지 꾸준히 확인하는 것을 권장합니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 가벼운 백그라운드 태스크를 통해 작업을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메서드를 사용하면, PHP 배열 구조 분해와 조합해 각 작업의 결과를 손쉽게 받아올 수 있습니다.

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane에서 처리하는 동시 작업은 Swoole의 "작업 워커(task workers)"를 이용하며, 요청과는 완전히 별도의 프로세스에서 실행됩니다. 동시 작업을 처리할 수 있는 워커 수는 `octane:start` 명령의 `--task-workers` 옵션으로 설정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드를 사용할 때, Swoole의 task 시스템 한계로 인해 작업 수는 1024개를 넘지 않도록 해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱(tick) 및 인터벌(interval)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 일정 간격마다 실행되는 "틱(tick)" 작업을 추가할 수 있습니다. `tick` 메서드를 사용해 틱 콜백을 등록할 수 있습니다. 첫 번째 인자는 티커의 이름(문자열)이고, 두 번째 인자는 지정된 간격마다 호출할 콜러블입니다.

아래 예시는 10초마다 클로저를 실행하는 방법입니다. 일반적으로 `tick` 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면, Octane 서버가 최초 부팅할 때 바로 틱 콜백을 실행하고 그 이후 N초마다 실행하도록 할 수 있습니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 최대 초당 2백만 건의 읽기/쓰기 속도를 제공하는 Octane 캐시 드라이버를 사용할 수 있습니다. 이 캐시 드라이버는 캐싱 계층에서 극한의 속도가 필요한 애플리케이션에 매우 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반으로 동작합니다. 저장된 모든 캐시 데이터는 서버 내 모든 워커가 공유할 수 있습니다. 단, 서버가 재시작되면 캐시된 데이터는 모두 삭제됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 허용되는 최대 엔트리 개수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

라라벨의 일반적인 캐시 시스템 메서드뿐 아니라, Octane 캐시 드라이버는 인터벌 기반 캐시 기능도 제공합니다. 이 캐시들은 지정된 주기마다 자동으로 갱신되며, 서비스 프로바이더의 `boot` 메서드에서 등록하는 것이 권장됩니다. 아래 예시는 5초마다 새로고침되는 캐시입니다.

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

Swoole 사용 시, [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 성능을 제공하며, 이 테이블의 데이터는 서버 내 모든 워커에서 접근할 수 있습니다. 하지만 서버가 재시작되면 데이터는 모두 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 설정 배열에서 정의해야 합니다. 최대 1000개의 행을 허용하는 예시 테이블이 이미 기본 설정되어 있습니다. 문자열 컬럼의 최대 길이는 아래 예시처럼 컬럼 타입 뒤에 숫자를 추가하여 지정할 수 있습니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다.

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
