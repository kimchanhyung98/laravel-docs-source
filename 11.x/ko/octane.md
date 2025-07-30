# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 필수 조건](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 제공](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 제공](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 제공](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [워커 수 지정](#specifying-the-worker-count)
    - [최대 요청 횟수 지정](#specifying-the-max-request-count)
    - [워커 재로드](#reloading-the-workers)
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

[Laravel Octane](https://github.com/laravel/octane)는 고성능 애플리케이션 서버인 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등을 사용하여 애플리케이션의 성능을 대폭 향상시킵니다. Octane은 애플리케이션을 한 번만 부팅한 뒤 메모리 내에 유지하면서 요청을 초고속으로 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후, `octane:install` Artisan 명령어를 실행하면 애플리케이션에 Octane 설정 파일이 설치됩니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 필수 조건 (Server Prerequisites)

> [!WARNING]  
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/) 버전을 필요로 합니다.

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, early hints, Brotli 및 Zstandard 압축과 같은 최신 웹 기능을 지원합니다. Octane 설치 시 서버로 FrankenPHP를 선택하면, Octane이 자동으로 FrankenPHP 바이너리를 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Laravel Sail](/docs/11.x/sail)을 이용해 개발할 계획이라면, 다음 명령어들을 실행하여 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

그 다음 `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 제공할 때 사용할 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2 및 HTTP/3을 활성화하려면 다음과 같이 변경하세요:

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

일반적으로 FrankensteinPHP Sail 애플리케이션에는 `https://localhost`로 접속해야 하며, `https://127.0.0.1`은 추가 설정이 필요하며 사용이 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP 공식 Docker 이미지를 사용하면 성능 향상과 더불어 정적 설치판에 포함되지 않은 추가 확장 기능을 활용할 수 있습니다. 또한, 공식 이미지는 Windows 같은 FrankenPHP가 기본 지원하지 않는 플랫폼에서도 실행할 수 있습니다. 이 이미지는 로컬 개발 및 프로덕션 용도로 모두 적합합니다.

FrankenPHP 기반 Laravel 애플리케이션을 컨테이너화하기 위한 기본 Dockerfile 예시는 다음과 같습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 시에는 다음 Docker Compose 파일을 사용해 애플리케이션을 실행할 수 있습니다:

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시하면 Octane은 FrankenPHP의 네이티브 로거를 사용하며, 별도의 설정이 없으면 구조화된 JSON 형식 로그를 생성합니다.

Docker로 FrankenPHP를 실행하는 자세한 내용은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리를 기반으로 작동합니다. RoadRunner 기반 Octane 서버를 처음 실행할 때 Octane이 RoadRunner 바이너리를 다운로드하고 설치할 것인지 물어봅니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Laravel Sail](/docs/11.x/sail)을 사용 중이라면, 다음 명령어들로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음으로 Sail 셸을 시작한 후 `rr` 실행 파일을 이용해 최신 Linux용 RoadRunner 바이너리를 가져옵니다:

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

그리고 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 서비스를 제공할 때 사용하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 생성하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane을 Swoole 애플리케이션 서버로 구동하려면 Swoole PHP 확장을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버로 Octane을 사용하려면 Open Swoole PHP 확장을 설치해야 합니다. 보통 PECL로 설치합니다:

```shell
pecl install openswoole
```

Open Swoole을 사용하면 Swoole에서 제공하는 동시에 실행 작업, 틱, 인터벌과 같은 기능을 동일하게 활용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail에서 Swoole 사용하기

> [!WARNING]  
> Sail로 Octane 애플리케이션을 제공하기 전에 Laravel Sail의 최신 버전을 사용 중인지 확인하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

[Larael Sail](/docs/11.x/sail)은 Laravel용 공식 Docker 개발 환경으로, 기본적으로 Swoole 확장을 포함하고 있습니다. 다만 `docker-compose.yml` 파일 수정을 필요로 합니다.

시작하려면 애플리케이션의 `docker-compose.yml` 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail에서 PHP 개발 서버 대신 Octane을 실행할 때 사용할 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 재빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 구성

Swoole은 `octane` 설정 파일 내에 추가할 수 있는 몇 가지 옵션을 지원합니다. 기본 설정 파일에는 거의 수정할 필요가 없기에 포함되어 있지 않습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 제공 (Serving Your Application)

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 구성 파일 내 `server` 옵션에서 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 제공

기본적으로 Octane에서 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션 `config/octane.php` 구성 파일 내의 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면 Octane은 생성되는 모든 링크에 `https://`를 접두사로 붙입니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 제공

> [!NOTE]  
> 서버 구성이나 여러 서비스를 직접 관리하는 것이 익숙하지 않다면, [Laravel Forge](https://forge.laravel.com)를 참고하세요.

운영 환경에서는 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 제공하는 것이 좋습니다. 이렇게 하면 웹 서버가 이미지 및 스타일시트 같은 정적 자원을 관리하고 SSL 인증서 종료를 담당할 수 있습니다.

아래 Nginx 설정 예시는 정적 자원을 서비스하고, Octane 서버(포트 8000)로 리버스 프록시하는 구성입니다:

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
### 파일 변경 감시

Octane 서버가 시작될 때 애플리케이션이 메모리 내에서 한 번만 로드되기 때문에, 애플리케이션 파일을 수정해도 브라우저 새로 고침 시 바로 반영되지 않습니다. 예를 들어 `routes/web.php` 파일에 새 라우트를 추가해도 서버를 재시작해야 변경사항이 반영됩니다. 편의상 `--watch` 플래그를 사용하면 Octane이 애플리케이션 파일 변경을 감지할 때마다 서버를 자동으로 재시작합니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에 [Node](https://nodejs.org)가 로컬 개발 환경에 설치되어 있는지 확인하고, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉토리 및 파일은 애플리케이션 `config/octane.php` 구성 파일의 `watch` 옵션을 통해 설정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 수 지정

기본적으로 Octane은 머신의 CPU 코어 수와 동일한 수의 애플리케이션 요청 워커를 시작합니다. 이 워커들은 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령어에서 `--workers` 옵션을 사용하면 시작할 워커 수를 직접 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용할 때는 동시에 시작할 ["task workers"](#concurrent-tasks) 수도 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 횟수 지정

메모리 누수를 방지하기 위해 Octane은 워커가 500개의 요청을 처리하면 해당 워커를 우아하게 재시작합니다. 이 횟수는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재로드

Octane 서버의 애플리케이션 워커는 `octane:reload` 명령어로 우아하게 재시작할 수 있습니다. 주로 배포 후 새로 배포한 코드가 메모리에 반영되도록 할 때 사용합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어를 통해 Octane 서버를 중지할 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

지금 실행 중인 Octane 서버 상태는 `octane:status` Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번만 부팅하고 메모리 내에 유지한 채 요청을 처리하기 때문에 몇 가지 주의할 점이 있습니다. 예를 들어, 애플리케이션 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅할 때 단 한 번만 실행됩니다. 이후 요청에서는 기존 애플리케이션 인스턴스를 재사용합니다.

따라서 애플리케이션 서비스 컨테이너나 요청 객체를 다른 객체의 생성자에 주입할 때는 주의해야 합니다. 이렇게 하면 해당 객체가 이후 요청에서 오래된 컨테이너나 요청 객체를 계속 참조할 수 있습니다.

Octane은 요청 사이에 프레임워크 내부 상태를 자동으로 초기화하지만, 애플리케이션이 생성하는 전역 상태의 초기화는 보장하지 않습니다. 이 때문에 Octane 친화적으로 애플리케이션을 설계하는 방법을 알아두는 것이 중요하며, 아래에서는 Octane 사용 시 문제가 될 수 있는 대표적인 상황들을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 객체의 생성자에 직접 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 다음 코드는 싱글톤으로 등록된 객체에 전체 애플리케이션 컨테이너를 주입하는 예입니다:

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

이 경우, `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성되면 컨테이너가 객체에 주입되고, 이후 요청 동안 동일한 컨테이너 인스턴스가 계속 유지됩니다. 이는 이후 부팅 과정이나 요청에서 새롭게 추가된 바인딩이 컨테이너에 없을 수 있다는 점에서 문제가 될 수 있습니다.

해결책으로는 해당 바인딩을 싱글톤으로 등록하지 않거나, 객체에 컨테이너를 직접 주입하는 대신 현재 컨테이너를 항상 반환하는 클로저를 주입할 수 있습니다:

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

전역 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입

일반적으로 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 객체의 생성자에 직접 주입하는 것은 권장되지 않습니다. 예를 들어, 다음 코드는 싱글톤으로 등록된 객체에 요청 인스턴스를 직접 주입한 예입니다:

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

이 경우 `Service` 객체는 부팅 과정에서 최초 요청 인스턴스를 주입받아 이후 요청에 같은 요청 데이터를 지속적으로 유지합니다. 따라서 요청에 포함된 헤더, 입력 데이터, 쿼리 문자열 등이 올바르지 않게 됩니다.

해결책으로는 싱글톤 등록을 중단하거나, 현재 요청 인스턴스를 반환하는 클로저를 객체에 주입하거나, 가장 권장되는 방법으로는 필요한 요청 정보만 객체 메서드 호출 시 전달하는 것입니다:

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

전역 `request` 헬퍼는 현재 애플리케이션이 처리 중인 요청 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]  
> 컨트롤러 메서드와 라우트 클로저에서는 `Illuminate\Http\Request` 인스턴스에 타입힌트를 사용하는 것이 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

일반적으로 설정 저장소 인스턴스를 생성자에 직접 주입하지 않는 것이 좋습니다. 예를 들어, 다음 코드는 싱글톤에 설정 저장소를 주입한 예시입니다:

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

이 경우 요청 간에 설정값이 변경되어도 `Service` 객체는 최초 생성 시점의 설정 저장소 인스턴스만 참조하므로 변경사항을 반영하지 못합니다.

해결책으로는 싱글톤 등록을 피하거나, 설정 저장소를 항상 최신 인스턴스로 반환하는 클로저를 주입하는 방법이 있습니다:

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

전역 `config` 헬퍼는 항상 최신 설정 저장소 인스턴스를 반환하여 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리 (Managing Memory Leaks)

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적 속성 배열에 데이터를 계속 추가하면 메모리 누수가 발생합니다. 예를 들어 아래 컨트롤러는 각 요청 시마다 정적 `$data` 배열에 랜덤 데이터를 추가해 메모리 누수가 발생합니다:

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

앱을 개발할 때는 이런 메모리 누수가 생기지 않도록 특히 주의해야 하며, 로컬 개발 환경에서 메모리 사용량을 수시로 점검하는 것을 권장합니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole) 확장을 필요로 합니다.

Swoole을 사용하는 경우, Octane의 `concurrently` 메서드를 통하여 경량 백그라운드 작업을 동시에 실행할 수 있습니다. PHP 배열 디스트럭처링과 함께 사용해 각 작업의 결과를 편리하게 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane에서 처리하는 동시 작업은 Swoole의 "task worker"를 사용하며, 요청 처리 프로세스와 완전히 다른 프로세스에서 실행됩니다. task worker 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 호출 시 Swoole task 시스템 제한으로 인해 1024개 이상의 작업을 동시에 제공하지 않는 것이 좋습니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌 (Ticks and Intervals)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole) 확장을 필요로 합니다.

Swoole에서는 지정한 초 간격마다 실행되는 "틱" 작업을 등록할 수 있습니다. `tick` 메서드를 통해 시작할 수 있으며 첫 번째 인자는 틱의 식별 문자열, 두 번째 인자는 해당 주기마다 호출될 콜러블입니다.

예를 들어 10초 간격으로 호출할 클로저를 등록하는 코드는 보통 서비스 프로바이더의 `boot` 메서드에서 작성합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버 부팅 시 즉시 한 번 호출하고, 이후 지정한 인터벌마다 호출하도록 할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole) 확장을 필요로 합니다.

Swoole과 함께 사용 시 Octane 캐시 드라이버를 활용할 수 있으며 초당 최대 200만 번의 읽기/쓰기 성능을 제공합니다. 따라서 매우 빠른 캐시 속도가 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반이며, 서버 내 모든 워커가 캐시 데이터를 공유합니다. 단, 서버 재시작 시 캐시가 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]  
> Octane 캐시의 최대 엔트리 수는 애플리케이션의 `octane` 구성 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel의 일반적인 캐시 동작 외에도, Octane 캐시 드라이버는 인터벌 기반 캐시 기능을 제공합니다. 이 캐시는 지정된 시간 간격으로 자동 갱신되며 서비스 프로바이더의 `boot` 메서드에서 등록해야 합니다. 예를 들어 5초마다 갱신되는 캐시는 다음과 같이 등록합니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]  
> 이 기능은 [Swoole](#swoole) 확장을 필요로 합니다.

Swoole을 사용할 경우, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 빠른 성능을 제공하며 서버 내 모든 워커가 데이터를 공유할 수 있습니다. 단, 서버를 재시작하면 데이터가 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 배열에서 정의합니다. 최대 1000개의 행을 허용하는 예제 테이블이 기본 설정에 포함되어 있습니다. 문자열 컬럼의 최대 크기는 다음과 같이 타입 뒤에 크기를 지정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근할 때는 `Octane::table` 메서드를 사용합니다:

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