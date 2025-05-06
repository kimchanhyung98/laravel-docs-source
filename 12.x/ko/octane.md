# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 필수 조건](#server-prerequisites)
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
- [틱(Tick)과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 사용하여 애플리케이션 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 유지하며, 매우 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

Octane을 설치한 후, `octane:install` Artisan 명령어를 실행하면 Octane의 설정 파일이 애플리케이션에 추가됩니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 필수 조건

> [!WARNING]
> Laravel Octane은 [PHP 8.1 이상](https://php.net/releases/)이 필요합니다.

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축과 같은 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면 Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP

[Laravel Sail](/docs/{{version}}/sail)로 애플리케이션을 개발할 계획이 있다면, 아래 명령어로 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치하세요:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스하는 명령어를 담게 됩니다:

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

일반적으로 FrankenPHP Sail 애플리케이션에 접속할 때는 `https://localhost`를 사용해야 하며, `https://127.0.0.1`은 [추가 설정이 필요하므로 권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 이용한 FrankenPHP

FrankenPHP의 공식 Docker 이미지는 정적 설치판에 포함되지 않은 추가 확장 기능 제공과 성능 향상을 제공하며, FrankenPHP가 기본적으로 지원하지 않는 Windows와 같은 플랫폼에서도 사용할 수 있습니다. FrankenPHP 공식 Docker 이미지는 로컬 개발 및 운영 환경 모두에 적합합니다.

아래 Dockerfile 예시는 FrankenPHP 기반 Laravel 애플리케이션을 컨테이너화할 때 참고용으로 사용할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 아래 Docker Compose 파일로 애플리케이션을 실행할 수 있습니다:

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

`php artisan octane:start` 명령에 `--log-level` 옵션을 명시적으로 전달하면, Octane은 FrankenPHP의 네이티브 로거를 사용해 구조화된 JSON 로그를 출력합니다.

FrankenPHP를 Docker와 함께 사용하는 자세한 방법은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리로 구동됩니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane이 RoadRunner 바이너리를 직접 다운로드하고 설치할 수 있도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/{{version}}/sail)로 애플리케이션을 개발할 경우, 아래 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

다음으로, Sail 셸을 실행한 후 `rr` 실행 파일을 사용해 최신 Linux용 RoadRunner 빌드를 설치하세요:

```shell
./vendor/bin/sail shell

# Sail 셸 내부에서...
./vendor/bin/rr get-binary
```

그 다음, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경변수를 추가하세요:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로, `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 기능을 설치해야 합니다. 일반적으로 PECL을 통해 설치합니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 기능을 설치해야 합니다. 일반적으로 PECL에서 설치합니다:

```shell
pecl install openswoole
```

Open Swoole을 사용할 경우 Swoole과 동일하게 동시 작업, 틱/인터벌 등 모든 기능을 이용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]
> Sail을 통해 Octane 애플리케이션을 서비스하기 전, Laravel Sail이 최신 버전인지 확인하고 애플리케이션의 루트 디렉토리에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는, [Laravel Sail](/docs/{{version}}/sail) 개발 환경을 사용해 Swoole 기반 Octane 애플리케이션을 만들 수도 있습니다. Sail은 기본적으로 Swoole 확장 기능을 포함합니다. 다만, Sail의 `docker-compose.yml` 파일 수정은 필요합니다.

먼저, 아래와 같이 `SUPERVISOR_PHP_COMMAND` 환경변수를 `laravel.test` 서비스 정의에 추가하세요:

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

필요에 따라, Swoole은 기본 `octane` 설정 파일에 포함되지 않은 추가 옵션을 지원합니다:

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

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 이 명령은 기본적으로 애플리케이션의 `octane` 설정 파일에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`으로 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS로 애플리케이션 서비스

Octane에서 구동되는 애플리케이션은 기본적으로 `http://`로 링크가 생성됩니다. 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경변수를 `true`로 설정하면, HTTPS로 서비스 시 링크가 `https://`로 생성됩니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스

> [!NOTE]
> 직접 서버를 구성하거나 다양한 서비스를 직접 설정하는 것이 부담스럽다면, 완전관리형 Laravel Octane 지원을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 살펴보세요.

운영 환경에서는 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스해야 합니다. 이렇게 하면 정적 파일(이미지, CSS 등)은 웹 서버가 처리하고, SSL 인증서 종료도 관리할 수 있습니다.

아래 Nginx 설정 예제에서, Nginx는 정적 파일 서비스를 담당하고, HTTP 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다:

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

Octane 서버는 시작 시 애플리케이션을 한 번만 메모리에 적재하므로, 파일 변경이 있을 경우 브라우저 새로고침만으로는 변경사항이 반영되지 않습니다. (예: `routes/web.php`에 라우트를 추가해도 서버 재시작 전까지 반영되지 않음) 편의를 위해 `--watch` 플래그를 사용하면 애플리케이션 파일 변경 시 Octane 서버가 자동으로 재시작됩니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에 [Node](https://nodejs.org)가 로컬 개발 환경에 설치되어 있어야 하며, [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 프로젝트에 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리/파일은 애플리케이션의 `config/octane.php` 설정 파일의 `watch` 항목에서 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커(Worker) 수 지정

기본적으로 Octane은 서버의 CPU 코어 수만큼 워커를 생성합니다. 이 워커가 HTTP 요청을 처리합니다. 명령 실행 시 `--workers` 옵션으로 직접 워커 수를 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용할 경우 ["태스크 워커"](concurrent-tasks)를 추가로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

메모리 누수를 방지하기 위해, Octane은 워커가 500개의 요청을 처리할 때마다 정상적으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작

`octane:reload` 명령으로 Octane 서버의 워커를 정상적으로 재시작할 수 있습니다. 배포 후 새 코드가 반영되도록 워커를 재시작할 때 주로 사용합니다:

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

`octane:status` Artisan 명령어로 Octane 서버의 현재 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번 부팅하고, 요청을 처리하는 동안 메모리에 유지합니다. 이에 따라 몇 가지 주의해야 할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register` 및 `boot` 메서드는 워커가 최초 부팅될 때 한 번만 실행됩니다. 이후 요청에서는 같은 애플리케이션 인스턴스가 재사용됩니다.

따라서, **애플리케이션 서비스 컨테이너나 요청 인스턴스를 객체 생성자에 주입하면, 그 객체가 이후 요청에서 오래된 컨테이너나 요청 인스턴스를 사용할 수 있으니 주의해야 합니다.**

Octane은 요청마다 프레임워크 상태를 자동으로 초기화해주지만, 개발자가 만든 전역 상태까지 항상 알 수는 없습니다. 아래에서는 Octane 사용 시 문제가 발생할 수 있는 대표적인 상황을 소개합니다.

<a name="container-injection"></a>
### 컨테이너 주입

애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 아래 예시는 전체 애플리케이션 컨테이너를 싱글톤 객체에 주입하고 있습니다:

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

이 경우 서비스가 최초 부팅 과정에서 resolve(해결)되면, 컨테이너 인스턴스가 서비스 객체에 들어가고 이후 요청에서도 같은 컨테이너가 사용됩니다. 이로 인해 나중에 바인딩된 서비스가 누락되는 문제가 발생할 수 있습니다.

해결 방법으로는 바인딩을 싱글톤에서 일반 바인딩으로 변경하거나, 항상 최신 컨테이너를 반환하는 클로저를 서비스에 주입하세요:

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

전역 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
### 요청 주입

마찬가지로, HTTP 요청 인스턴스를 싱글톤 객체 생성자에 바로 주입하는 것은 좋지 않습니다. 아래 예시는 전체 Request 인스턴스를 싱글톤 객체에 전달하고 있습니다:

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

이 경우 Service 인스턴스에는 최초 요청 객체만 계속 주입되므로, 헤더, 입력값, 쿼리스트링 등 모든 요청 데이터가 잘못될 수 있습니다.

해결책으로는 싱글톤 바인딩을 일반 바인딩으로 변경하거나, 항상 최신 요청 인스턴스를 반환하는 클로저를 객체에 주입하세요. 또는, 해당 객체가 실제로 요청 정보가 필요한 시점에 해당 데이터를 메소드 인자로 전달하는 것이 가장 권장되는 방식입니다:

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

전역 `request` 헬퍼는 항상 현재 처리 중인 요청 객체만 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드 및 라우트 클로저에서 `Illuminate\Http\Request`를 타입 힌트하는 것은 허용되고 안전합니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

마찬가지로, 설정 저장소 인스턴스를 다른 객체 생성자에 주입하는 것은 바람직하지 않습니다. 예를 들어, 아래는 설정 저장소를 싱글톤 객체에 주입하는 경우입니다:

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

만약 요청 사이에 설정 값이 변경된다면, 이 서비스는 원래 저장소 인스턴스를 계속 사용하므로 새로운 값에 접근할 수 없습니다.

일반 바인딩으로 변경하거나, 클로저를 통해 항상 최신 설정 저장소를 주입하세요:

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

전역 `config`는 항상 최신 설정 저장소 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 사이에도 애플리케이션을 메모리에 계속 유지합니다. 따라서, 정적(static) 배열 등에 데이터를 추가하는 방식은 메모리 누수를 일으킵니다. 아래 컨트롤러는 각 요청마다 static `$data` 배열에 데이터를 계속 추가하므로 메모리 누수가 발생합니다:

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

이런 형태의 메모리 누수를 피하기 위해 개발 중에는 애플리케이션의 메모리 사용량을 모니터링하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 경량화된 백그라운드 태스크를 통해 작업을 동시 실행할 수 있습니다. Octane의 `concurrently` 메서드를 사용하세요. PHP 배열 디스트럭처링과 결합하여 각 작업의 결과를 가져올 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업은 Swoole의 "태스크 워커"에서 실행되며, 요청을 처리하는 프로세스와는 분리되어 있습니다. 태스크 워커 수는 `octane:start` 명령의 `--task-workers` 디렉티브로 결정합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 실행 시, Swoole의 태스크 시스템 한계로 1024개 이하의 작업만 처리해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick)과 인터벌

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용할 때는 지정한 초 마다 실행되는 "틱(Tick)" 작업을 등록할 수 있습니다. `tick` 메서드를 사용해 콜백을 등록하세요. 첫 번째 인자는 틱 이름(문자열), 두 번째는 실행할 콜러블입니다.

예시로 10초마다 호출되는 Closure를 등록합니다. 보통 `tick` 메서드는 서비스 프로바이더의 `boot`에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면, Octane 서버 부팅 시 최초 한 번 바로 콜백을 실행하고, 이후 N초마다 재실행할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 경우, Octane 캐시 드라이버를 사용할 수 있습니다. 최대 초당 2백만 번의 읽기/쓰기 속도를 제공하기 때문에, 극한의 캐시 성능이 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반입니다. 모든 워커에서 동일한 데이터를 공유할 수 있으나, 서버가 재시작되면 데이터는 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시의 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel의 일반 캐시 메서드 외에, Octane 캐시에는 지정된 주기로 자동 새로고침되는 "interval 기반 캐시" 기능이 있습니다. 이 캐시는 서비스 프로바이더의 `boot` 메서드에서 등록해야 하며, 예를 들어 다음 캐시 값은 5초마다 변경됩니다:

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

Swoole을 사용할 때 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 극한의 성능을 제공하며 모든 워커에서 접근할 수 있지만, 서버가 재시작될 경우 데이터는 모두 사라집니다.

테이블은 애플리케이션 `octane` 설정 파일의 `tables` 설정 배열에서 정의합니다. 예를 들어 최대 1000개의 행을 허용하는 테이블은 아래와 같이 미리 설정되어 있습니다. 문자열 열의 최대 크기는 이름 뒤에 크기를 명시할 수 있습니다:

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