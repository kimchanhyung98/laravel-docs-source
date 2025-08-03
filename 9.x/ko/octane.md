# Laravel Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 필수 조건](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [작업자(worker) 수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [작업자 재시작](#reloading-the-workers)
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

[Laravel Octane](https://github.com/laravel/octane)는 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), 그리고 [RoadRunner](https://roadrunner.dev)와 같은 강력한 애플리케이션 서버를 사용해 애플리케이션의 성능을 크게 향상시킵니다. Octane은 애플리케이션을 한 번만 부팅하고 메모리에 유지한 후 매우 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

설치 후에는 `octane:install` Artisan 명령어를 실행하여 Octane 설정 파일을 애플리케이션에 추가할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 필수 조건 (Server Prerequisites)

> [!WARNING]
> Laravel Octane은 [PHP 8.0 이상](https://php.net/releases/)이 필요합니다.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리가 구동합니다. RoadRunner 기반 Octane 서버를 처음 시작하면 Octane이 RoadRunner 바이너리를 자동으로 다운로드하고 설치할지 묻습니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/9.x/sail) 환경에서 개발할 계획이라면 아래 명령어로 Octane과 RoadRunner를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

다음으로 Sail 셸을 실행하고 `rr` 실행파일을 사용해 최신 Linux용 RoadRunner 바이너리를 받으세요:

```shell
./vendor/bin/sail shell

# Sail 셸 내에서...
./vendor/bin/rr get-binary
```

RoadRunner 바이너리 설치가 완료되면 셸을 종료합니다. 이후 Sail이 애플리케이션을 계속 실행하도록 `supervisor.conf` 설정을 수정해야 합니다. 먼저 `sail:publish` Artisan 명령어를 실행해 기본 설정을 퍼블리시하세요:

```shell
./vendor/bin/sail artisan sail:publish
```

그 다음, 애플리케이션의 `docker/supervisord.conf` 파일 내 `command` 지시문을 다음과 같이 변경해 Sail이 PHP 개발 서버 대신 Octane으로 서비스를 제공하도록 설정합니다:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80
```

마지막으로 `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드합니다:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane을 Swoole 애플리케이션 서버로 실행할 계획이라면 Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]
> Sail을 통해 Octane 애플리케이션을 실행하기 전, 최신 버전의 Laravel Sail이 설치되어 있어야 하며 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행해야 합니다.

또한, Laravel 공식 Docker 개발 환경인 [Laravel Sail](/docs/9.x/sail)을 이용해 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Sail에서는 기본적으로 Swoole 확장 모듈이 포함되어 있습니다. 다만, Sail이 애플리케이션을 계속 실행하도록 `supervisor.conf`를 수정해야 합니다. 우선 `sail:publish` Artisan 명령어를 수행하세요:

```shell
./vendor/bin/sail artisan sail:publish
```

그 후, 애플리케이션의 `docker/supervisord.conf` 파일 내 `command` 지시문을 다음처럼 수정해 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 제공합니다:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

마지막으로 Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 옵션을 지원합니다. 기본 설정 파일에는 포함되어 있지 않으나 필요시 아래처럼 설정할 수 있습니다:

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

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 애플리케이션의 `octane` 설정 파일에서 지정한 `server` 옵션에 따라 서버가 실행됩니다:

```shell
php artisan octane:start
```

기본 포트는 8000이며, 웹 브라우저에서 `http://localhost:8000` 으로 접속해 애플리케이션을 확인할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 서비스 (Serving Your Application Via HTTPS)

기본적으로 Octane 애플리케이션은 링크에 `http://` 접두사를 붙입니다. HTTPS를 이용해 서비스를 제공할 때는 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정할 수 있습니다. 이 값이 `true`로 설정되면 Octane은 Laravel에 생성되는 모든 링크에 `https://` 접두사를 붙이도록 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 서비스 (Serving Your Application Via Nginx)

> [!NOTE]
> 서버 설정에 익숙하지 않거나 복잡한 서비스 구성을 직접 관리하기 어려울 경우, [Laravel Forge](https://forge.laravel.com)를 확인해 보세요.

운영 환경에서는 Nginx나 Apache 같은 웹 서버 뒤에서 Octane 애플리케이션을 서비스해야 합니다. 이렇게 하면 웹 서버가 이미지나 스타일시트 같은 정적 자산을 처리하고 SSL 인증서 종료를 관리할 수 있습니다.

다음은 Nginx 설정 예로, Nginx는 사이트의 정적 자산을 서비스하고 포트 8000에서 동작하는 Octane 서버로 요청을 프록시합니다:

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
### 파일 변경 감시 (Watching For File Changes)

Octane 서버는 애플리케이션을 한 번 메모리에 올린 뒤 실행되기 때문에, 애플리케이션 코드가 변경되어도 서버를 재시작하지 않으면 변경 사항이 반영되지 않습니다. 예를 들어 `routes/web.php`에 라우트를 추가해도 서버를 재시작해야만 적용됩니다. 편의상 `--watch` 옵션을 사용하면 애플리케이션 파일 변경 시 Octane이 자동으로 서버를 재시작하도록 할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에는 로컬 개발 환경에 [Node.js](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일 목록은 애플리케이션의 `config/octane.php` 설정 파일 내 `watch` 옵션에서 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 작업자(worker) 수 지정 (Specifying The Worker Count)

기본적으로 Octane은 서버 머신의 CPU 코어 수만큼 작업자를 시작해 HTTP 요청을 처리합니다. 직접 작업자 수를 지정하려면 `octane:start` 명령어 실행 시 `--workers` 옵션을 사용하세요:

```shell
php artisan octane:start --workers=4
```

Swoole 서버를 사용하는 경우에는 ["task workers"](#concurrent-tasks) 수도 함께 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정 (Specifying The Max Request Count)

메모리 누수를 방지하기 위해 Octane은 각 작업자가 500개의 요청을 처리하면 자동으로 작업자를 재시작합니다. 이 값을 조정하려면 `--max-requests` 옵션을 사용하세요:

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 작업자 재시작 (Reloading The Workers)

배포 후 새 코드를 메모리에 반영하려면 `octane:reload` 명령어로 Octane의 작업자를 우아하게 재시작할 수 있습니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지 (Stopping The Server)

Octane 서버를 종료하려면 `octane:stop` Artisan 명령어를 사용하세요:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

현재 Octane 서버 상태는 `octane:status` Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection & Octane)

Octane은 애플리케이션을 한 번 부팅하여 메모리에 유지하며 요청을 처리하기 때문에 몇 가지 유의할 점이 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더 내 `register`와 `boot` 메서드는 요청 작업자가 처음 부팅될 때 단 한 번만 실행됩니다. 이후 요청들에는 같은 애플리케이션 인스턴스가 재사용됩니다.

따라서 서비스 컨테이너나 요청(Request)을 객체 생성자에 주입할 때 주의해야 합니다. 이렇게 하면 해당 객체는 이후 요청에서 오래된(또는 stale) 컨테이너나 요청 인스턴스를 보유할 수 있습니다.

Octane은 프레임워크에서 제공하는 상태 초기화는 요청 사이에 자동으로 처리하지만, 사용자 애플리케이션에서 생성된 전역 상태 초기화는 항상 알지 못하기 때문에, Octane 친화적으로 애플리케이션을 설계해야 합니다. 아래에서 가장 흔한 문제 상황과 해결책을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입 (Container Injection)

일반적으로, 다른 객체의 생성자에 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하는 것을 피해야 합니다. 예를 들어, 다음 바인딩 코드는 싱글톤으로 바인딩된 객체 생성자에 서비스 컨테이너 전체를 주입합니다:

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app);
    });
}
```

이 경우 `Service` 인스턴스가 애플리케이션 부팅 시점에 생성되면 요청 작업자 간 같은 컨테이너 인스턴스를 계속 보유합니다. 이로 인해 애플리케이션 부팅 과정이나 이후 요청에서 추가된 바인딩을 누락하거나 예기치 않은 동작이 발생할 수 있습니다.

해결책으로는 싱글톤 등록을 중단하거나, 현재 컨테이너 인스턴스를 매번 반환하는 클로저를 주입하는 방법이 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;

$this->app->bind(Service::class, function ($app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입 (Request Injection)

마찬가지로, 다른 객체 생성자에 HTTP 요청 인스턴스를 주입하는 것도 피해야 합니다. 예를 들어 다음 바인딩은 요청 인스턴스를 싱글톤 객체에 주입합니다:

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app['request']);
    });
}
```

이 경우 `Service` 인스턴스는 최초 요청의 HTTP 요청을 보유하므로 이후 요청의 헤더, 입력값, 쿼리 스트링 등이 잘못 표시될 수 있습니다.

해결책으로는 싱글톤 등록을 중단하거나 현재 요청을 반환하는 클로저를 주입하거나, 가장 권장하는 방법으로는 실제 객체 생성 시 필요한 요청 정보를 객체 메서드 인자로 전달하는 것입니다:

```php
use App\Service;

$this->app->bind(Service::class, function ($app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function ($app) {
    return new Service(fn () => $app['request']);
});

// 또는...

$service->method($request->input('name'));
```

전역 `request` 헬퍼는 현재 처리 중인 요청을 항상 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입 (Configuration Repository Injection)

설정 저장소 인스턴스를 다른 객체 생성자에 주입하는 것도 피하는 게 좋습니다. 예를 들어, 다음 바인딩은 설정 저장소를 싱글톤 객체에 주입합니다:

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app->make('config'));
    });
}
```

설정 값이 요청 간 변경되어도 원래 인스턴스를 참조하므로 변경 사항이 반영되지 않을 수 있습니다.

해결책으로 싱글톤 등록을 중단하거나, 현재 설정 저장소를 반환하는 클로저를 주입하는 방법이 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;

$this->app->bind(Service::class, function ($app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

전역 `config` 헬퍼는 항상 최신 설정 저장소를 반환하므로 안전합니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리 (Managing Memory Leaks)

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적 배열 등에 데이터를 계속 추가하면 메모리 누수가 발생합니다. 예를 들어 아래 컨트롤러는 요청마다 정적 배열에 데이터를 계속 추가하므로 누수가 발생합니다:

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return void
 */
public function index(Request $request)
{
    Service::$data[] = Str::random(10);

    // ...
}
```

개발 중에는 이런 메모리 누수를 피하도록 주의해야 하며, 로컬 환경에서 애플리케이션 메모리 사용량을 모니터링하는 것이 권장됩니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole) 사용 시에만 지원됩니다.

Swoole을 사용할 때는 가벼운 백그라운드 작업을 이용해 여러 작업을 동시 실행할 수 있습니다. Octane의 `concurrently` 메서드로 이를 수행할 수 있으며, PHP 배열 분해 문법을 통해 각 작업 결과를 동시에 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane에서 동시 작업은 Swoole의 "task workers"에서 별도의 프로세스로 실행되며, `octane:start` 명령어의 `--task-workers` 옵션으로 할당되는 task worker 수에 의해 작동합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드에 1024개 이상의 작업을 전달해서는 안 되며, 이는 Swoole 작업 시스템의 제한 때문입니다.

<a name="ticks-and-intervals"></a>
## 틱과 인터벌 (Ticks & Intervals)

> [!WARNING]
> 이 기능은 [Swoole](#swoole) 사용 시에만 지원됩니다.

Swoole을 사용하면 일정 간격(초 단위)마다 실행할 틱 작업을 등록할 수 있습니다. `tick` 메서드를 사용해 틱 작업을 등록하며, 첫 번째 인수는 틱커 이름(문자열), 두 번째 인수는 지정한 간격마다 호출될 콜러블입니다.

아래 예시는 10초마다 실행되는 콜백을 서비스 프로바이더의 `boot` 메서드에서 등록하는 방법입니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버가 처음 부팅될 때 즉시 콜백을 실행하고 이후 매 N초마다 반복하도록 설정할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole) 사용 시에만 지원됩니다.

Swoole 사용 시, 초당 200만건 이상의 읽기/쓰기 성능을 갖는 Octane 캐시 드라이버를 사용할 수 있습니다. 이 캐시 드라이버는 처리 속도가 매우 빠르기 때문에 캐시 계층에서 극한의 빠른 읽기/쓰기를 요구하는 애플리케이션에 적합합니다.

이 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 캐시된 모든 데이터는 서버 내 모든 작업자가 공유할 수 있습니다. 단, 서버를 재시작하면 캐시 데이터는 모두 사라집니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에서 허용하는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌 (Cache Intervals)

Laravel 기본 캐시 시스템의 일반 메서드 외에, Octane 캐시는 주기적으로 자동 갱신되는 인터벌 기반 캐시를 제공합니다. 해당 캐시는 서비스 프로바이더의 `boot` 메서드 안에서 등록해야 합니다. 다음 예시는 5초마다 캐시가 갱신됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]
> 이 기능은 [Swoole](#swoole) 사용 시에만 지원됩니다.

Swoole 기반에서 원하는 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 제공하며 서버 내 모든 작업자가 데이터를 공유할 수 있습니다. 다만 서버를 재시작하면 데이터가 소멸합니다.

테이블 정의는 애플리케이션의 `octane` 설정 파일 내 `tables` 배열에서 지정합니다. 최대 1000개 행을 허용하는 예제 테이블이 기본으로 설정되어 있습니다. 문자열 컬럼 크기는 컬럼 타입 뒤에 크기를 명시해 설정합니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메서드를 사용합니다:

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