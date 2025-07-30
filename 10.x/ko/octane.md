# Laravel Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 요구사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [워커 수 지정하기](#specifying-the-worker-count)
    - [최대 요청 수 지정하기](#specifying-the-max-request-count)
    - [워커 재시작하기](#reloading-the-workers)
    - [서버 중지하기](#stopping-the-server)
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

[Laravel Octane](https://github.com/laravel/octane)은 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), 그리고 [RoadRunner](https://roadrunner.dev) 같은 강력한 애플리케이션 서버를 사용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 후 메모리에 유지하며, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후, `octane:install` Artisan 명령어를 실행하여 Octane 설정 파일을 애플리케이션에 설치하세요:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 요구사항 (Server Prerequisites)

> [!WARNING]  
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/) 버전을 필요로 합니다.

<a name="frankenphp"></a>
### FrankenPHP

> [!WARNING]  
> FrankenPHP의 Octane 통합은 베타 단계로 프로덕션 환경에서 사용할 때는 주의가 필요합니다.

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, 얼리 힌트(early hints)와 Zstandard 압축 같은 최신 웹 기능을 지원합니다. Octane 설치 시, FrankenPHP를 서버로 선택하면 자동으로 FrankenPHP 바이너리를 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 이용한 FrankenPHP

[Laravel Sail](/docs/10.x/sail)로 애플리케이션 개발을 계획하고 있다면 다음 명령어로 Octane 및 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

그다음 `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 사용해 애플리케이션을 띄울 때 사용할 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port=80" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3를 활성화하려면 다음과 같이 설정하세요:

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

일반적으로 FrankenPHP Sail 애플리케이션에는 `https://localhost` 주소로 접속하는 것이 권장됩니다. `https://127.0.0.1` 사용 시 추가 설정이 필요하며 이는 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 이용한 FrankenPHP

FrankenPHP 공식 Docker 이미지를 사용하면 성능 향상과 정적 설치에 포함되지 않은 추가 확장기능 사용이 가능합니다. 또한, 공식 Docker 이미지는 Windows와 같이 FrankenPHP가 기본적으로 지원하지 않는 플랫폼에서 구동할 수 있도록 지원합니다. 공식 이미지는 로컬 개발뿐 아니라 프로덕션 환경에도 적합합니다.

다음 Dockerfile은 FrankenPHP 기반 Laravel 애플리케이션을 컨테이너화하는 시작점입니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 아래 Docker Compose 파일을 사용해 애플리케이션을 실행할 수 있습니다:

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

Docker에서 FrankenPHP 실행 관련 자세한 내용은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리를 기반으로 합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane은 RoadRunner 바이너리 다운로드와 설치를 제안합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 이용한 RoadRunner

[Laravel Sail](/docs/10.x/sail)로 개발할 경우 다음 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http 
```

그 후, Sail 셸을 열고 `rr` 실행 파일을 사용해 최신 Linux 용 RoadRunner 바이너리를 받아오세요:

```shell
./vendor/bin/sail shell

# Sail 셸 내에서...
./vendor/bin/rr get-binary
```

마지막으로, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 사용해 애플리케이션을 실행할 때 사용하는 명령입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80" # [tl! add]
```

`rr` 바이너리가 실행 가능하도록 권한을 설정하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션 서버로 Swoole을 사용하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Laravel Octane 애플리케이션 서버로 Open Swoole을 사용하려면 Open Swoole PHP 확장을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install openswoole
```

Open Swoole을 사용하면 Swoole이 제공하는 동시 작업, 틱, 인터벌과 같은 기능을 그대로 활용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 이용한 Swoole

> [!WARNING]  
> Sail을 통해 Octane 애플리케이션을 서비스하기 전에 Laravel Sail 최신 버전을 사용 중인지 확인하고, 애플리케이션 루트 디렉터리에서 `./vendor/bin/sail build --no-cache` 명령을 실행하세요.

또는 [Laravel Sail](/docs/10.x/sail)을 사용해 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail은 기본적으로 Swoole 확장을 포함하지만, `docker-compose.yml` 파일은 직접 수정해야 합니다.

시작하려면, `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 사용해 애플리케이션을 실행할 때 쓰는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80" # [tl! add]
```

마지막으로, Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 추가 구성 옵션을 지원합니다. 기본 설정 파일에는 자주 변경할 필요가 없으므로 포함되어 있지 않습니다:

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

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션 `octane` 설정 파일에 지정된 `server` 옵션에 따라 서버를 선택합니다:

```shell
php artisan octane:start
```

Octane은 기본 포트 8000에서 서버를 시작하며, 따라서 웹 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 서비스 (Serving Your Application via HTTPS)

기본적으로 Octane으로 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. `config/octane.php` 내 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, Octane은 모든 링크를 `https://`로 생성하도록 Laravel에 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스 (Serving Your Application via Nginx)

> [!NOTE]  
> 서버 구성에 익숙하지 않거나 Laravel Octane 애플리케이션 운영에 필요한 다양한 서비스 구성이 부담된다면 [Laravel Forge](https://forge.laravel.com)를 참고하세요.

프로덕션 환경에서는 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스하는 것이 좋습니다. 이렇게 하면 정적 자원(이미지, 스타일시트 등) 서빙과 SSL 인증서 관리 등을 웹 서버가 담당하게 됩니다.

아래 Nginx 예제 구성에서는 Nginx가 정적 자원을 서비스하고, 요청은 포트 8000에서 실행 중인 Octane 서버로 프록시합니다:

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

Octane 서버가 시작할 때 애플리케이션을 한 번만 메모리에 로드하기 때문에, 소스 코드 변경은 서버 재시작 전까지 반영되지 않습니다. 예를 들어, `routes/web.php`에 새로운 라우트가 추가되어도 서버 재시작 없이는 적용되지 않습니다.

편의를 위해 `--watch` 옵션을 사용하면 애플리케이션 내 파일이 변경될 때 자동으로 서버를 재시작할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하려면 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하고, 프로젝트에 파일 감시 라이브러리 [Chokidar](https://github.com/paulmillr/chokidar)를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일 목록은 `config/octane.php` 설정 내 `watch` 옵션으로 조정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 수 지정하기 (Specifying the Worker Count)

기본적으로 Octane은 CPU 코어 수만큼 애플리케이션 요청 워커를 시작합니다. 이 워커들은 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령 실행 시 `--workers` 옵션으로 워커 수를 수동 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 서버를 사용하는 경우에는 ["task workers"](#concurrent-tasks) 수도 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정하기 (Specifying the Max Request Count)

메모리 누수를 방지하기 위해 Octane은 워커가 500개의 요청을 처리하면 워커를 유연하게 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작하기 (Reloading the Workers)

Octane 서버의 애플리케이션 워커를 유연하게 재시작하려면 `octane:reload` 명령을 사용하세요. 배포 후 새로 배포된 코드가 메모리에 반영되어 이후 요청에 적용되도록 할 때 주로 사용됩니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지하기 (Stopping the Server)

Octane 서버를 중지하려면 `octane:stop` Artisan 명령어를 실행하세요:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인하기

현재 Octane 서버 상태를 확인하려면 `octane:status` Artisan 명령어를 사용하세요:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번 부팅해 메모리에 유지하면서 요청을 처리하기 때문에 몇 가지 주의 사항이 필요합니다. 예를 들어, 애플리케이션 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅할 때 단 한 번 실행됩니다. 그 이후 요청부터는 같은 애플리케이션 인스턴스가 재사용됩니다.

따라서, 애플리케이션 서비스 컨테이너나 요청 객체를 생성자의 인수로 주입할 때 주의해야 합니다. 이렇게 주입된 객체는 이후 요청에서 오래된 컨테이너나 요청 객체를 가지고 있을 수 있습니다.

Octane은 프레임워크의 기본 상태를 요청 간에 자동으로 초기화하지만, 애플리케이션에서 생성된 글로벌 상태는 초기화하지 못할 수 있습니다. 그러므로 Octane 친화적인 애플리케이션을 작성하는 방법에 대해 알아야 합니다. 아래는 Octane 사용 중 자주 발생하는 문제 상황들입니다.

<a name="container-injection"></a>
### 컨테이너 주입 (Container Injection)

일반적으로 다른 객체 생성자의 인수로 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 주입하는 것을 피하는 것이 좋습니다. 아래 예제는 싱글톤으로 바인딩된 객체에 전체 애플리케이션 서비스 컨테이너를 주입하는 경우입니다:

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

이 경우, `Service` 인스턴스가 애플리케이션 부팅 시점에 생성되면 같은 컨테이너 객체가 이후 요청에도 유지됩니다. 일부 애플리케이션에서는 문제가 없을 수 있지만, 때때로 컨테이너가 나중에 등록되는 바인딩을 알지 못하는 상황이 발생할 수 있습니다.

해결 방법으로는 싱글톤 등록을 중지하거나, 현재 컨테이너 인스턴스를 항상 해결하는 클로저를 서비스에 주입하는 방식이 있습니다:

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

글로벌 `app` 헬퍼나 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입 (Request Injection)

기본적으로 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것을 피하는 것이 좋습니다. 아래 예는 싱글톤 객체에 요청 전체를 주입하는 경우입니다:

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

이런 경우, `Service` 인스턴스가 부팅 시 생성되면 같은 요청 객체가 이후 요청에도 유지되고, 헤더, 입력값, 쿼리 문자열 등 모든 요청 데이터가 올바르지 않은 상태가 됩니다.

해결 방법으로 싱글톤 등록을 중지하거나 현재 요청을 해결하는 클로저를 주입하는 방법, 또는 가장 권장하는 방법인 필요한 요청 데이터를 실행 시점에 메서드 인자로 전달하는 방법이 있습니다:

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

글로벌 `request` 헬퍼는 현재 애플리케이션이 처리 중인 요청을 항상 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]  
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request`를 타입힌트하는 것은 적절합니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입 (Configuration Repository Injection)

기본적으로 설정 저장소 인스턴스를 객체 생성자에 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 다음은 싱글톤 객체에 설정 저장소를 주입하는 예입니다:

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

이 경우 요청 간 설정 값이 변경되어도 서비스가 원래 저장소 인스턴스를 참조하기 때문에 변경 사항을 인지하지 못합니다.

해결책으로는 싱글톤 등록을 중지하거나, 설정 저장소를 항상 최신 인스턴스로 해결하는 클로저를 주입하는 방법이 있습니다:

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

글로벌 `config` 헬퍼는 항상 최신 설정 저장소 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리 (Managing Memory Leaks)

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적 배열 등에 데이터를 계속해서 추가하는 경우 메모리 누수가 발생합니다. 예를 들면 다음 컨트롤러는 정적 `$data` 배열에 요청마다 데이터를 추가하여 메모리 누수가 생깁니다:

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

애플리케이션을 작성할 때 이러한 메모리 누수 문제가 발생하지 않도록 주의하고, 로컬 개발 환경에서 메모리 사용량을 모니터링하는 것을 권장합니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 Octane의 `concurrently` 메서드를 통해 경량 백그라운드 작업을 동시 실행할 수 있습니다. PHP 배열 구조 분해와 함께 사용하여 각 작업의 결과를 쉽게 가져올 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업은 Swoole의 "task workers" 프로세스에서 실행되며, 요청 워커와는 완전히 다른 프로세스 내에서 작동합니다. 동시 작업 처리 가능한 워커 수는 `octane:start` 명령 시 `--task-workers` 옵션으로 지정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 호출 시 Swoole 태스크 시스템 제한으로 1024개 이상의 작업을 동시에 전달하지 않아야 합니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌 (Ticks and Intervals)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 일정 간격으로 실행되는 "틱" 작업을 등록할 수 있습니다. `tick` 메서드로 등록하며 첫 번째 인수는 틱커 이름 문자열, 두 번째는 지정된 간격마다 호출될 콜러블입니다.

아래 예시는 10초마다 호출되는 클로저를 등록한 예제입니다. 일반적으로 서비스 프로바이더 `boot` 메서드 내에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버가 시작될 때 틱 콜백을 즉시 실행하고, 이후에도 매 N초마다 실행하도록 할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 Octane 캐시 드라이버를 사용할 수 있으며, 초당 최대 200만 건의 읽기/쓰기 속도를 제공합니다. 따라서 캐시 계층에서 극한의 속도를 필요로 하는 애플리케이션에 매우 적합합니다.

이 캐시는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 캐시에 저장된 모든 데이터는 서버 내 모든 워커가 공유합니다. 단, 서버가 재시작되면 캐시 데이터는 사라집니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]  
> Octane 캐시의 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌 (Cache Intervals)

Laravel 캐시 시스템의 일반적인 메서드 외에, Octane 캐시는 인터벌 기반 캐시 기능을 제공합니다. 이 캐시는 지정한 시간 간격마다 자동으로 갱신되며, 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 등록합니다. 예를 들어, 다음 캐시는 5초마다 갱신됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 사용자 정의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 높은 성능을 제공하고 서버 내 모든 워커가 접근 가능하며, 서버 재시작 시 데이터는 삭제됩니다.

테이블은 애플리케이션 `octane` 설정 파일의 `tables` 배열 내에 정의합니다. 최대 1000행을 허용하는 예제 테이블이 기본적으로 구성되어 있습니다. 문자열 컬럼의 최대 크기는 타입 뒤에 크기를 지정해 설정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근할 때는 `Octane::table` 메서드를 사용하세요:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]  
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float` 입니다.