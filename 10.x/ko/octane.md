# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 요구 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [Worker 수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [Worker 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [리퀘스트 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 이용해 여러분의 애플리케이션 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅하고 메모리에 유지하며, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

Octane을 설치한 후, `octane:install` Artisan 명령어를 실행하면 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 요구 사항

> [!WARNING]  
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/)가 필요합니다.

<a name="frankenphp"></a>
### FrankenPHP

> [!WARNING]  
> FrankenPHP의 Octane 통합은 베타 단계이며, 프로덕션 환경에서는 주의하여 사용해야 합니다.

[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, early hints, Zstandard 압축 등 현대적인 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Laravel Sail](/docs/{{version}}/sail)로 개발할 계획이라면, 아래 명령어를 통해 Octane과 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` Artisan 명령어로 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 사용해 애플리케이션을 서비스하는 명령어를 담고 있습니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port=80" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3을 활성화하려면 다음과 같이 수정하세요:

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

보통 `https://localhost`로 FrankenPHP Sail 애플리케이션에 접근해야 하며, `https://127.0.0.1` 사용 시 추가 설정이 필요하므로 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP 공식 Docker 이미지를 사용하면 성능이 향상되고, 정적 설치에는 포함되지 않은 추가 확장 기능도 사용할 수 있습니다. 또한 Docker 이미지는 FrankenPHP가 기본적으로 지원하지 않는 플랫폼(예: Windows)에서도 사용할 수 있게 해주므로, 로컬 개발과 운영 환경에 모두 적합합니다.

아래 예시 Dockerfile을 FrankenPHP 기반 Laravel 애플리케이션 컨테이너화의 시작점으로 사용할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 중에는 다음과 같은 Docker Compose 파일을 사용할 수 있습니다:

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

Docker와 함께 FrankenPHP를 실행하는 더 자세한 정보는 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 제작된 RoadRunner 바이너리를 기반으로 합니다. RoadRunner 기반 Octane 서버를 처음 시작하면, Octane이 RoadRunner 바이너리를 다운로드 및 설치해줍니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Laravel Sail](/docs/{{version}}/sail)로 개발할 계획이라면, 아래 명령어를 통해 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http 
```

다음으로 Sail 쉘을 실행한 후, `rr` 실행 파일로 RoadRunner 바이너리를 다운로드합니다:

```shell
./vendor/bin/sail shell

# Sail 쉘 내부에서...
./vendor/bin/rr get-binary
```

그리고 `SUPERVISOR_PHP_COMMAND` 환경 변수를 `laravel.test` 서비스 정의에 추가하세요:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80" # [tl! add]
```

마지막으로, `rr` 바이너리가 실행 가능한지 확인하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Octane 애플리케이션을 서비스하려면, Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하려면, Open Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용하면, Swoole이 제공하는 동시 작업, 틱, 인터벌 등의 기능을 동일하게 활용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole 사용

> [!WARNING]  
> Sail로 Octane 애플리케이션을 서비스하기 전, 최신 버전의 Laravel Sail을 사용하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행해야 합니다.

또는, 공식 Docker 기반 개발 환경인 [Laravel Sail](/docs/{{version}}/sail)을 사용해 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 포함되어 있지만, `docker-compose.yml` 파일의 수정은 필요합니다.

먼저, `SUPERVISOR_PHP_COMMAND` 환경 변수를 `laravel.test` 서비스 정의에 추가하세요:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80" # [tl! add]
```

마지막으로 Sail 이미지를 빌드합니다:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 몇 가지 추가 설정 옵션을 지원합니다. 필요하다면 `octane` 설정 파일에 다음과 같이 추가할 수 있습니다. 이들은 대부분 수정이 필요하지 않아 기본 설정 파일에는 포함되어 있지 않습니다:

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

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에서 지정한 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane 서버는 8000번 포트에서 시작되므로, 웹 브라우저에서 `http://localhost:8000`으로 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 서비스

기본적으로 Octane에서 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php`에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, HTTPS로 서비스를 할 때 모든 생성된 링크가 `https://`로 시작됩니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스

> [!NOTE]  
> 여러분이 직접 서버 설정을 다루거나 Laravel Octane 애플리케이션 실행에 필요한 다양한 서비스를 구성하는 것이 어렵다면, [Laravel Forge](https://forge.laravel.com)를 확인해보세요.

운영 환경에서는 Octane 애플리케이션을 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 서비스해야 합니다. 이렇게 하면, 웹 서버가 정적 자산(이미지, 스타일시트 등)을 서빙하고 SSL 인증서 종료도 관리할 수 있습니다.

아래 Nginx 설정 예시에서는, Nginx가 사이트 정적 자산을 서비스하고, 요청을 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다:

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

Octane 서버가 시작될 때 애플리케이션이 메모리에 한 번만 로드되기 때문에, 애플리케이션 파일의 변경 사항은 브라우저를 새로고침해도 즉시 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가해도 서버를 재시작해야 반영됩니다. 이를 위해 `--watch` 플래그를 사용하면 파일 변경 시 Octane 서버가 자동 재시작됩니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하려면 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리도 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리 및 파일 목록은 애플리케이션의 `config/octane.php` 파일의 `watch` 옵션에서 설정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### Worker 수 지정

기본적으로 Octane은 머신의 CPU 코어 개수만큼 애플리케이션 요청 워커를 시작합니다. 이 워커들이 들어오는 HTTP 요청을 처리합니다. 워커 수를 지정하려면 `octane:start` 명령어 실행 시 `--workers` 옵션을 사용할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용할 경우 ["task worker"](#concurrent-tasks) 수 지정도 가능합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

잠재적인 메모리 누수를 예방하기 위해, Octane은 한 워커가 500개의 요청을 처리하면 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### Worker 재시작

`octane:reload` 명령어로 Octane 서버의 애플리케이션 워커를 정상적으로 재시작할 수 있습니다. 일반적으로 새 코드 배포 후, 최신 코드가 메모리에 반영되어 이후의 요청에 사용되도록 이 명령을 실행해야 합니다:

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

`octane:status` Artisan 명령어로 현재 Octane 서버의 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번만 부팅한 뒤 메모리에 유지하여 요청을 처리하므로, 애플리케이션 개발 시 몇 가지 주의 사항이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅될 때 딱 한 번만 실행됩니다. 이후 요청에서는 동일한 애플리케이션 인스턴스가 재사용됩니다.

따라서, 서비스 컨테이너나 리퀘스트 인스턴스를 객체의 생성자에 주입할 때 특별히 조심해야 합니다. 그렇지 않으면, 해당 객체가 이후 요청에서도 예전 컨테이너나 요청 객체를 계속 참조할 수 있습니다.

Octane은 기본적으로 프레임워크의 상태는 요청마다 자동으로 초기화합니다. 하지만, 여러분이 작성한 글로벌 상태는 Octane이 항상 재설정하는 법을 알지 못할 수 있으므로, Octane 친화적인 방식으로 애플리케이션을 구조화해야 합니다. 아래에서 Octane 사용 시 문제가 될 수 있는 일반적인 상황들을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로 다른 객체의 생성자에 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하지 않는 것이 좋습니다. 예를 들어, 아래와 같이 전체 컨테이너 인스턴스를 싱글톤 객체에 주입하면:

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

이 예제에서 `Service` 인스턴스가 애플리케이션 부팅 과정에서 해석되면, 해당 서비스 인스턴스는 이후 요청에도 동일한 컨테이너를 계속 가지고 있게 됩니다. 이는 애플리케이션에 따라 문제가 되지 않을 수도 있지만, 부팅 이후 또는 후속 요청에서 추가된 바인딩이 누락되는 사례로 이어질 수 있습니다.

이 문제를 해결하려면, 싱글톤 등록을 피하거나, 항상 최신 컨테이너 인스턴스를 반환하는 클로저를 서비스에 주입해야 합니다:

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 리퀘스트 주입

일반적으로 다른 객체의 생성자에 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하지 않는 것이 좋습니다. 아래 예시는 전체 요청 인스턴스를 싱글톤으로 바인딩된 객체에 주입하는 경우입니다:

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

이 경우, `Service` 인스턴스가 부팅 시점에 해석되면, 동일한 요청 인스턴스가 계속 사용되어 이후 요청의 헤더, 입력, 쿼리스트링 등의 데이터가 모두 잘못될 수 있습니다.

해결 방법으로는, 싱글톤 등록 대신 바인딩만 사용하거나, 항상 최신 요청 인스턴스를 반환하는 리졸버 클로저를 서비스에 주입하거나, 가장 권장되는 방법은 객체의 메서드에 필요한 요청 정보만 런타임에 직접 전달하는 것입니다:

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청 인스턴스를 반환하므로, 안전하게 사용할 수 있습니다.

> [!WARNING]  
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

일반적으로 다른 객체의 생성자에 설정 저장소 인스턴스를 주입하지 않는 것이 좋습니다. 예를 들어, 다음은 설정 저장소를 싱글톤 객체에 주입한 예시입니다:

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

이 경우, 요청마다 설정 값이 바뀌더라도 서비스는 초기 저장소 인스턴스만 참조하므로, 최신값을 얻지 못합니다.

해결책으로는, 싱글톤 대신 바인딩만 사용하거나, 설정 저장소 리졸버 클로저를 주입하세요:

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

글로벌 `config` 헬퍼는 항상 최신 설정 저장소를 반환하므로, 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 사이에 애플리케이션을 메모리에 유지합니다. 따라서, 정적으로 관리되는 배열에 데이터를 계속 추가하면 메모리 누수가 발생할 수 있습니다. 예를 들어, 아래 컨트롤러는 요청마다 static `$data` 배열에 데이터를 추가하므로 메모리 누수가 발생합니다:

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

이러한 메모리 누수를 피하려면, 애플리케이션의 메모리 사용량을 로컬 개발 환경에서 꼭 모니터링해야 합니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시, 경량 백그라운드 태스크를 통해 연산을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메서드로 이를 구현할 수 있으며, PHP 배열 디스트럭처링 문법을 활용해 각각의 결과를 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업은 Swoole의 "task worker"를 사용하며, 각 작업은 요청과는 별도의 프로세스에서 실행됩니다. 동시 작업을 처리할 워커의 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 호출 시 Swoole의 태스크 시스템 제한 때문에 1024개를 초과하는 태스크를 제공하지 않아야 합니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 매 n초마다 실행되는 "tick" 동작을 등록할 수 있습니다. `tick` 메서드를 사용하여 콜백을 등록할 수 있습니다. 첫 번째 인자는 티커의 이름을 나타내는 문자열이고, 두 번째 인자는 지정된 간격마다 호출될 콜러블입니다.

아래 예는 10초마다 호출되는 콜로저를 등록합니다. 보통 이 메서드는 서비스 프로바이더의 `boot`에서 호출해야 합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버 부팅 직후와 이후 매 n초마다 콜백을 즉시 실행하도록 명령할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!WARNING]  
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 1초당 최대 2백만 번의 읽기/쓰기 속도를 제공하는 Octane 캐시 드라이버를 사용할 수 있습니다. 매우 빠른 캐시 레이어가 필요한 애플리케이션에 특히 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반으로 동작합니다. 저장된 데이터는 서버 내 모든 워커가 사용할 수 있지만, 서버가 재시작되면 데이터는 모두 사라집니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]  
> Octane 캐시의 최대 엔트리 개수는 애플리케이션의 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel의 일반 캐시 메서드와 더불어, Octane 캐시 드라이버는 자동으로 일정 간격마다 갱신되는 인터벌 캐시를 지원합니다. 이 캐시는 서비스 프로바이더의 `boot` 메서드에서 등록하며, 아래 예시처럼 5초마다 갱신됩니다:

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

Swoole을 사용할 때, [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 임의로 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 뛰어난 성능을 제공하며, 서버 내 모든 워커들이 데이터를 공유할 수 있습니다. 다만, 서버 재시작 시 데이터는 모두 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 배열에 정의합니다. 예시 테이블은 최대 1000개의 행을 허용합니다. 문자열 컬럼의 최대 크기도 아래처럼 지정할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근할 땐 `Octane::table` 메서드를 사용하세요:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]  
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float`뿐입니다.