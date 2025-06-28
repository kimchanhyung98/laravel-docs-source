# 라라벨 Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 필수 조건](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 제공하기](#serving-your-application)
    - [HTTPS로 애플리케이션 제공하기](#serving-your-application-via-https)
    - [Nginx로 애플리케이션 제공하기](#serving-your-application-via-nginx)
    - [파일 변경 감지 및 반영](#watching-for-file-changes)
    - [워커 개수 지정하기](#specifying-the-worker-count)
    - [최대 요청 수 지정하기](#specifying-the-max-request-count)
    - [워커 재시작하기](#reloading-the-workers)
    - [서버 중지하기](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [Request 주입](#request-injection)
    - [설정 저장소(Configuration Repository) 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 처리 작업](#concurrent-tasks)
- [틱(Tick)과 인터벌(Interval)](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[라라벨 Octane](https://github.com/laravel/octane)은 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등과 같은 강력한 애플리케이션 서버를 사용하여 애플리케이션의 성능을 극대화해줍니다. Octane은 애플리케이션을 한 번만 부팅한 후 메모리에 유지하여, 극강의 속도로 요청을 처리할 수 있도록 지원합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

Octane을 설치한 뒤에는, `octane:install` 아티즌 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 필수 조건

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, Early Hint, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치해줍니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Laravel Sail](/docs/12.x/sail)로 애플리케이션을 개발할 계획이라면, 다음 명령어로 Octane과 FrankenPHP를 설치할 수 있습니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` 아티즌 명령어를 사용해 FrankenPHP 바이너리를 설치합니다.

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수에는 Sail이 Octane을 이용해 애플리케이션을 실행할 때 사용할 명령어가 들어갑니다(PHP 개발 서버가 아닌 Octane으로 실행).

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3을 활성화하려면 아래와 같이 추가 설정을 적용하세요.

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

일반적으로 FrankenPHP Sail 애플리케이션에는 `https://localhost` 주소로 접속하는 것이 권장됩니다. `https://127.0.0.1`을 사용할 경우 추가 설정이 필요하며, [FrankenPHP 문서](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker)에서도 권장하지 않습니다.

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP의 공식 Docker 이미지를 활용하면 더 뛰어난 성능과, FrankenPHP의 정적 설치 버전에 없는 추가 확장 기능을 사용할 수 있습니다. 또한, 공식 이미지를 사용하면 윈도우처럼 FrankenPHP가 기본적으로 지원하지 않는 플랫폼에서도 사용할 수 있습니다. 공식 Docker 이미지는 로컬 개발 및 프로덕션 환경 모두에 적합합니다.

아래 Dockerfile 예시는 FrankenPHP 기반 라라벨 애플리케이션을 컨테이너화할 때 시작점으로 활용할 수 있습니다.

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 환경에서는 아래와 같은 Docker Compose 파일을 이용해 애플리케이션을 실행할 수 있습니다.

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달하면 Octane이 FrankenPHP의 네이티브 로거를 사용하며, 별도의 설정이 없는 한 구조화된 JSON 로그가 생성됩니다.

Docker 기반 FrankenPHP 실행에 대한 자세한 내용은 [FrankenPHP 공식 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리로 동작합니다. RoadRunner 기반의 Octane 서버를 처음 실행하면 Octane이 RoadRunner 바이너리를 다운로드 및 설치하겠냐는 메시지를 표시합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Laravel Sail](/docs/12.x/sail)로 개발하려면, 아래 명령어로 Octane과 RoadRunner를 설치합니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음 단계로 Sail 셸을 실행하고 `rr` 실행 파일을 이용해 최신 리눅스 빌드의 RoadRunner 바이너리를 받아옵니다.

```shell
./vendor/bin/sail shell

# Sail 셸 내부에서...
./vendor/bin/rr get-binary
```

이후, `docker-compose.yml`의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 환경 변수는 Sail이 Octane을 통해 애플리케이션을 실행할 때 사용하는 명령어입니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로, `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드합니다.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버를 사용하여 라라벨 Octane 애플리케이션을 실행하려면 Swoole PHP 확장 기능을 설치해야 합니다. 보통 PECL을 이용해 설치합니다.

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하고 싶다면 Open Swoole PHP 확장 기능을 설치해야 합니다. 일반적으로 PECL을 통해 설치합니다.

```shell
pecl install openswoole
```

라라벨 Octane을 Open Swoole과 함께 사용하면 Swoole이 제공하는 동시 처리, 틱(tick), 인터벌(interval) 기능도 동일하게 활용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole 사용

> [!WARNING]
> Octane 애플리케이션을 Sail로 실행하기 전에 Laravel Sail의 최신 버전이 설치되어 있어야 하며, 애플리케이션의 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 반드시 실행해야 합니다.

또는, [Laravel Sail](/docs/12.x/sail)을 활용해 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 포함되어 있습니다. 그러나 `docker-compose.yml` 파일을 추가로 수정해야 합니다.

설정을 시작하려면, `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수에는 Sail이 Octane을 통해 애플리케이션을 실행할 때 사용되는 명령어가 포함됩니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 빌드합니다.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 필요에 따라 `octane` 설정 파일에서 추가 옵션을 지정할 수 있습니다. 이런 옵션들은 자주 변경할 필요가 없어서 기본 설정 파일엔 포함되어 있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 제공하기

Octane 서버는 `octane:start` 아티즌 명령어로 실행할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에 명시된 `server` 옵션의 값을 사용합니다.

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS로 애플리케이션 제공하기

기본적으로 Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 만약 HTTPS로 애플리케이션을 제공한다면, `config/octane.php` 설정 파일의 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하세요. 이 값을 `true`로 설정하면 Octane에서 라라벨에게 모든 링크를 `https://`로 시작하도록 지시합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx로 애플리케이션 제공하기

> [!NOTE]
> 서버 설정을 직접 관리하거나 다양한 서비스의 설정에 익숙하지 않다면 [Laravel Cloud](https://cloud.laravel.com)를 참고하세요. 이 서비스는 완전히 관리되는 라라벨 Octane 지원을 제공합니다.

프로덕션 환경에서는 반드시 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 실행해야 합니다. 이렇게 하면 이미지, 스타일시트와 같은 정적 자산을 웹 서버가 직접 서빙하고, SSL 인증서 종료도 처리할 수 있습니다.

아래는 Nginx 설정 예시입니다. Nginx가 사이트의 정적 자산을 서빙하고, Octane 서버(8000번 포트)로 프록시 요청을 전달합니다.

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
### 파일 변경 감지 및 반영

Octane 서버가 시작될 때 애플리케이션이 한 번만 메모리에 로드되기 때문에, 코드 파일이 변경되어도 브라우저를 새로 고침해도 즉시 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가하면 서버를 재시작해야만 반영됩니다. 이 과정을 편리하게 하기 위해, `--watch` 옵션을 지정하면 애플리케이션 내 파일이 변경될 때마다 Octane 서버를 자동으로 재시작할 수 있습니다.

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에는 반드시 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일은 `config/octane.php` 설정 파일의 `watch` 옵션에서 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정하기

기본적으로 Octane은 머신의 CPU 코어 개수만큼 애플리케이션 요청 워커를 시작합니다. 이 워커들이 들어오는 HTTP 요청을 분산해 처리합니다. `octane:start` 명령어의 `--workers` 옵션을 통해 원하는 워커 개수를 직접 지정할 수도 있습니다.

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용할 경우 ["태스크 워커(task workers)"](#concurrent-tasks) 개수도 함께 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정하기

의도치 않은 메모리 누수를 방지하기 위해 Octane은 각 워커가 500개의 요청을 처리할 때마다 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작하기

Octane 서버의 애플리케이션 워커를 부드럽게 재시작하려면 `octane:reload` 명령어를 사용하면 됩니다. 일반적으로 배포 후 새로운 코드가 반영되도록 서버 메모리에 올려야 할 때 실행합니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지하기

Octane 서버를 중지하려면 `octane:stop` 아티즌 명령어를 사용하세요.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인하기

Octane 서버의 현재 상태는 `octane:status` 아티즌 명령어로 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번만 부팅해 메모리에 올려놓은 상태에서 요청을 처리하기 때문에, 애플리케이션 개발 시 유의해야 할 점이 몇 가지 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더의 `register`와 `boot` 메서드는 워커가 처음 시작될 때 단 한 번만 실행됩니다. 이후의 요청에서는 동일한 애플리케이션 인스턴스를 재사용하게 됩니다.

이러한 이유로, 애플리케이션 서비스 컨테이너나 요청(request) 객체를 다른 객체의 생성자에 주입할 때에는 각별히 주의해야 합니다. 이렇게 하면 해당 객체가 이후의 요청마다 컨테이너나 요청의 "묵은" 상태를 계속 참조하게 될 수 있습니다.

Octane은 라라벨 프레임워크 자체 상태는 각 요청마다 자동으로 초기화해줍니다. 하지만 애플리케이션에서 생성된 전역 상태는 Octane이 항상 초기화할 수 없으니, Octane 친화적으로 애플리케이션을 짜는 방법을 숙지해야 합니다. 아래에 Octane 사용 시 흔히 문제가 될 수 있는 상황들을 안내합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로 다른 객체의 생성자(Constructor)에서 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하지 않는 것이 좋습니다. 예를 들어, 아래는 서비스 컨테이너 전체를 싱글톤 객체에 주입하는 방식입니다.

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

이 예시는 `Service` 인스턴스가 애플리케이션 부트 과정에서 생성될 경우, 그 컨테이너 인스턴스가 서비스 객체에 주입되고, 이후의 요청에도 같은 컨테이너가 계속 사용되어 버립니다. 상황에 따라 문제가 되지 않을 수도 있지만, 부팅 사이클 도중 혹은 이후 요청에서 추가된 바인딩(binding)이 누락되는 등 예기치 않은 현상이 발생할 수 있습니다.

해결 방법으로는 바인딩을 싱글톤(singleton)이 아닌 일반 바인딩으로 등록하거나, 항상 최신 컨테이너 인스턴스를 반환하는 클로저(Closure)를 주입해야 합니다.

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

글로벌 `app` 헬퍼나 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환하므로, 안전하게 사용할 수 있습니다.

<a name="request-injection"></a>
### Request 주입

일반적으로 다른 객체의 생성자에서 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하지 않는 것이 좋습니다. 아래 예시는 전체 요청 객체를 싱글톤 객체에 주입한 경우입니다.

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

이 경우, `Service` 인스턴스가 애플리케이션 부트 단계에서 생성되면, 그 요청 객체가 서비스에 주입되고, 같은 요청 객체가 이후의 모든 요청에서도 사용되어 버립니다. 이로 인해 헤더, 입력값, 쿼리스트링 등 모든 요청 데이터가 올바르지 않게 됩니다.

해결 방법으로는 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 항상 최신 요청 인스턴스를 반환하는 클로저를 서비스에 주입해야 합니다. 아니면, 가장 추천되는 방법으로 필요한 요청 데이터만 객체의 메서드 호출 시점에 전달하는 것이 좋습니다.

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청 인스턴스를 반환하므로, 애플리케이션 내에서 안전하게 쓸 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드와 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입 힌트로 지정하는 것은 괜찮습니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소(Configuration Repository) 주입

일반적으로 다른 객체의 생성자에 설정 저장소 인스턴스를 주입하는 것도 피해야 합니다. 아래 예시는 설정 저장소를 싱글톤 객체에 주입한 형태입니다.

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

이 경우, 요청 사이에서 설정 값이 변경되더라도 서비스 객체에서는 초기 저장소 인스턴스만 접근할 수 있고, 변경된 값들을 사용할 수 없습니다.

해결 방법으로는 바인딩을 싱글톤이 아닌 일반 바인딩으로 등록하거나, 항상 최신 저장소 인스턴스를 반환하는 클로저를 클래스에 주입하세요.

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
### 메모리 누수 관리

Octane은 요청 사이에 애플리케이션을 계속 메모리에 유지하므로, 정적으로 관리되는 배열 등에 데이터를 추가하게 되면 메모리 누수가 발생할 수 있습니다. 예를 들어, 아래 컨트롤러는 매 요청마다 static `$data` 배열에 값을 추가하므로 메모리 누수가 발생하게 됩니다.

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

애플리케이션을 개발할 때 반드시 이런 형태의 메모리 누수가 발생하지 않도록 각별히 주의해야 합니다. 로컬 개발 시 메모리 사용량을 주기적으로 모니터링하여 새로운 메모리 누수가 발생하지 않도록 관리하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 처리 작업

> [!WARNING]
> 본 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 경량화된 백그라운드 태스크(작업)를 통해 여러 작업을 동시에 처리할 수 있습니다. Octane의 `concurrently` 메서드를 사용하면 여러 작업을 병렬로 실행할 수 있으며, PHP 배열 디스트럭처링 기능과 조합해 각 작업 결과를 쉽게 받아올 수 있습니다.

```php
use App\Models\User;
use App\Models.Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane에서 실행되는 동시 작업은 Swoole의 "태스크 워커(task workers)"를 활용하며, 요청과는 완전히 별도의 프로세스에서 처리됩니다. 처리 가능한 동시 태스크 개수는 `octane:start` 명령어의 `--task-workers` 옵션으로 결정합니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드를 사용할 때는 Swoole 태스크 시스템의 제한으로, 태스크 개수를 1024개 이하로 지정해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick)과 인터벌(Interval)

> [!WARNING]
> 본 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 지정된 초마다 실행되는 "틱(tick)" 작업을 등록할 수 있습니다. `tick` 메서드를 사용해서 작성하며, 첫 번째 인자로는 티커(ticker) 이름(문자열), 두 번째 인자로는 주기적으로 실행될 콜러블을 전달하면 됩니다.

다음 예시는 10초마다 호출되는 클로저를 등록하는 예입니다. 일반적으로는 애플리케이션의 서비스 프로바이더의 `boot` 메서드에서 `tick` 메서드를 호출합니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면, Octane 서버가 처음 부팅될 때 즉시 콜백을 실행하고 이후 매 N초마다 계속 실행하도록 할 수 있습니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]
> 본 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때 Octane 캐시 드라이버를 활용하면, 초당 최대 200만 번 읽기/쓰기 속도를 지원할 수 있습니다. 따라서 초고속 캐싱이 필요한 애플리케이션에서는 매우 유용하게 쓸 수 있습니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 모든 워커가 서버 내 데이터에 접근할 수 있습니다. 단, 캐시된 데이터는 서버가 재시작될 때 모두 삭제됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 저장 가능한 최대 항목 개수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

라라벨 기본 캐시 시스템 메서드 외에도, Octane 캐시 드라이버는 일정 주기마다 자동으로 갱신되는 "인터벌 캐시" 기능을 제공합니다. 이 캐시는 서비스 프로바이더의 `boot` 메서드에서 등록하는 것이 일반적이며, 아래의 예시처럼 5초마다 캐시에 값을 갱신하도록 설정할 수 있습니다.

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블

> [!WARNING]
> 본 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 조작할 수 있습니다. Swoole 테이블은 아주 뛰어난 성능(처리량)을 제공하며, 테이블의 데이터는 모든 워커가 접근할 수 있습니다. 단, 서버가 재시작되면 해당 데이터는 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 설정 배열 내에서 정의해야 합니다. 최대 1000행을 허용하는 테이블 예시가 기본으로 포함되어 있습니다. 문자열 컬럼의 최대 크기는 컬럼 타입 뒤에 크기를 명시하여 지정할 수 있습니다.

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
