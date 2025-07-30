# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 요구사항](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스하기](#serving-your-application)
    - [HTTPS로 애플리케이션 서비스하기](#serving-your-application-via-https)
    - [Nginx를 통해 애플리케이션 서비스하기](#serving-your-application-via-nginx)
    - [파일 변경 감시하기](#watching-for-file-changes)
    - [워커 수 지정하기](#specifying-the-worker-count)
    - [최대 요청 수 지정하기](#specifying-the-max-request-count)
    - [워커 재시작하기](#reloading-the-workers)
    - [서버 중지하기](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [구성 리포지토리 주입](#configuration-repository-injection)
- [메모리 누수 관리하기](#managing-memory-leaks)
- [동시 실행 작업](#concurrent-tasks)
- [틱과 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)은 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 사용하여 애플리케이션의 성능을 크게 향상시킵니다. Octane은 애플리케이션을 한 번 부팅하여 메모리에 유지하며, 이후 요청을 매우 빠른 속도로 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```bash
composer require laravel/octane
```

설치 후 `octane:install` Artisan 명령어를 실행하면 Octane의 설정 파일이 애플리케이션에 설치됩니다:

```bash
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 요구사항

> [!NOTE]
> Laravel Octane은 [PHP 8.0+](https://php.net/releases/) 버전이 필요합니다.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리를 사용합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 자동으로 RoadRunner 바이너리를 다운로드하고 설치하겠냐고 물어봅니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/{{version}}/sail)로 애플리케이션을 개발할 계획이라면 다음 명령어로 Octane과 RoadRunner를 설치하세요:

```bash
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

이후 Sail 쉘을 시작해 `rr` 실행 파일을 사용하여 최신 Linux용 RoadRunner 바이너리를 받아야 합니다:

```bash
./vendor/bin/sail shell

# Sail 쉘 내부에서...
./vendor/bin/rr get-binary
```

RoadRunner 바이너리 설치가 완료되면 Sail 쉘을 종료할 수 있습니다. 이제 Sail이 애플리케이션을 유지하도록 사용하는 `supervisor.conf` 파일을 수정해야 합니다. 시작하려면 다음 Artisan 명령어를 실행하세요:

```bash
./vendor/bin/sail artisan sail:publish
```

그 후 `docker/supervisord.conf` 파일의 `command` 지시어를 수정하여 Sail이 PHP 개발 서버 대신 Octane을 사용하도록 만드세요:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=8000
```

마지막으로 `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드합니다:

```bash
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버를 사용해 Laravel Octane 애플리케이션을 구동하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```bash
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!NOTE]
> Sail로 Octane 애플리케이션을 서비스하기 전에 Laravel Sail 최신 버전을 사용 중인지 확인하고 애플리케이션 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는, 공식 Laravel Docker 개발 환경인 [Laravel Sail](/docs/{{version}}/sail)을 사용해 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Sail은 기본적으로 Swoole 확장이 포함되어 있지만, Sail이 애플리케이션을 유지하도록 `supervisor.conf` 파일을 수정해야 합니다. 시작하려면 다음 Artisan 명령어를 실행하세요:

```bash
./vendor/bin/sail artisan sail:publish
```

다음으로 `docker/supervisord.conf` 파일의 `command` 지시어를 수정해 Sail이 PHP 개발 서버가 아닌 Octane을 사용하도록 만드세요:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

마지막으로 Sail 이미지를 빌드합니다:

```bash
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 추가 설정 옵션을 지원합니다. 이 옵션들은 기본 설정 파일에 포함되어 있지 않으며, 일반적으로 수정할 필요가 거의 없습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
];
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스하기

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에 지정된 `server` 옵션에 따라 서버를 실행합니다:

```bash
php artisan octane:start
```

기본적으로 Octane은 포트 8000에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`를 통해 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS로 애플리케이션 서비스하기

기본적으로 Octane 실행 시 생성되는 링크는 `http://`로 시작합니다. `config/octane.php` 설정 파일 내에서 사용되는 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면, Octane은 Laravel에게 모든 생성된 링크에 `https://` 접두사를 붙이도록 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통해 애플리케이션 서비스하기

> [!TIP]
> 자신의 서버 설정을 직접 관리할 준비가 되지 않았거나 다양한 서비스를 구성하기 어렵다면, [Laravel Forge](https://forge.laravel.com)를 참고하세요.

운영 환경에서는 Nginx나 Apache 같은 전통적인 웹 서버 뒤에서 Octane 애플리케이션을 서비스하는 것이 좋습니다. 이렇게 하면 웹 서버가 이미지나 스타일시트 같은 정적 자산을 처리하고, SSL 인증서 종료를 관리할 수 있습니다.

아래 Nginx 구성 예시에서 Nginx는 정적 자산을 제공하고, 포트 8000에서 실행 중인 Octane 서버로 요청을 프록시합니다:

```conf
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
### 파일 변경 감시하기

Octane 서버가 시작될 때 애플리케이션이 한 번 메모리에 로드되므로, 애플리케이션 파일이 변경되어도 브라우저를 새로고침해도 바로 반영되지 않습니다. 예를 들어 `routes/web.php`의 라우트 정의가 바뀌어도 서버를 재시작해야 반영됩니다. 편리하게도 `--watch` 플래그를 사용하면 애플리케이션 내에서 파일 변경이 감지되면 Octane 서버를 자동으로 재시작하게 할 수 있습니다:

```bash
php artisan octane:start --watch
```

이 기능을 사용하기 전에 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```bash
npm install --save-dev chokidar
```

감시할 디렉터리와 파일은 애플리케이션의 `config/octane.php` 설정 파일의 `watch` 옵션에서 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 수 지정하기

기본적으로 Octane은 서버가 제공하는 CPU 코어 당 하나씩 애플리케이션 요청 워커를 시작합니다. 이 워커들이 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령어 실행 시 `--workers` 옵션으로 워커 수를 직접 지정할 수 있습니다:

```bash
php artisan octane:start --workers=4
```

Swoole 서버를 사용하는 경우에는 ["task workers"](#concurrent-tasks) 수 또한 지정할 수 있습니다:

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정하기

메모리 누수 방지를 위해, Octane은 워커가 일정 수의 요청을 처리하면 해당 워커를 점진적으로 재시작할 수 있습니다. 이 동작을 위해 `--max-requests` 옵션을 사용할 수 있습니다:

```bash
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작하기

`octane:reload` 명령어로 Octane 서버의 애플리케이션 워커를 점진적으로 재시작할 수 있습니다. 보통 배포 후 새로운 코드가 메모리에 로드되게 하려면 이 방법을 사용합니다:

```bash
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지하기

`octane:stop` Artisan 명령어로 Octane 서버를 중지할 수 있습니다:

```bash
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인하기

`octane:status` Artisan 명령어로 현재 Octane 서버 상태를 확인할 수 있습니다:

```bash
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번 부팅하여 메모리에 유지하며 요청을 처리하므로, 앱을 작성할 때 몇 가지 주의사항이 있습니다. 예를 들어 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅될 때 한 번만 실행됩니다. 이후 요청에는 동일한 애플리케이션 인스턴스가 재사용됩니다.

따라서 서비스 컨테이너나 요청 객체를 직접 생성자에 주입하는 경우 주의해야 합니다. 이렇게 하면 이후 요청에서는 오래된 컨테이너나 요청이 주입되어 문제가 발생할 수 있습니다.

Octane은 프레임워크 내부 상태를 요청 사이에 자동으로 리셋하지만, 애플리케이션이 만든 전역 상태는 항상 리셋하지 못합니다. 따라서 Octane 친화적으로 애플리케이션을 설계하는 방법을 알아야 합니다. 아래는 Octane 사용 중 흔히 문제를 일으키는 상황들입니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것을 피하는 게 좋습니다. 예를 들면, 아래 코드는 전체 서비스 컨테이너를 싱글톤으로 바인딩된 객체에 주입합니다:

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

이 경우 `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성되면, 이후 요청마다 동일한 컨테이너가 `Service` 인스턴스에 유지됩니다. 이는 특정 애플리케이션에선 문제가 되지 않을 수 있지만, 부팅 사이클이나 이후 요청 중 동적으로 바인딩이 추가되면 컨테이너가 제대로 그 바인딩을 인식하지 못할 위험이 있습니다.

해결책으로는 싱글톤을 중단하거나, 현재 컨테이너 인스턴스를 항상 반환하는 클로저를 주입하는 방법이 있습니다:

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

`app` 헬퍼와 `Container::getInstance()`는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### 요청 주입

일반적으로 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것을 피하는 게 좋습니다. 예를 들면, 아래 코드는 전체 요청 인스턴스를 싱글톤으로 바인딩된 객체에 주입합니다:

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

이 경우 `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성되면, 이후 요청도 동일한 요청 객체를 갖게 되어 헤더, 입력값, 쿼리 문자열 정보 등 모든 요청 데이터가 틀리게 됩니다.

해결책으로는 싱글톤 바인딩을 중단하거나, 현재 요청 인스턴스를 반환하는 클로저를 객체에 주입하는 방법이 있습니다. 또는 가장 권장하는 방법은 객체가 필요로 하는 요청 정보를 실행 시점에 메서드 인수로 전달하는 것입니다:

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

`request` 헬퍼는 항상 현재 애플리케이션이 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> [!NOTE]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 타입힌트를 사용하는 것은 전혀 문제없습니다.

<a name="configuration-repository-injection"></a>
### 구성 리포지토리 주입

일반적으로 구성 리포지토리 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예컨대 아래 코드는 구성 리포지토리를 싱글톤으로 바인딩된 객체에 주입합니다:

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

구성 값이 요청마다 변경될 경우, 해당 서비스는 새 값을 참조하지 않고 처음 의존한 리포지토리 인스턴스를 사용할 것입니다.

해결책은 싱글톤 바인딩을 중단하거나, 현재 구성 리포지토리를 반환하는 클로저를 객체에 주입하는 것입니다:

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

`config` 전역 헬퍼는 항상 최신 구성 리포지토리를 반환하므로 안전하게 사용 가능합니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리하기

Octane은 요청 간 애플리케이션을 메모리에 유지하므로, 정적으로 유지된 배열에 데이터를 추가하면 메모리 누수가 발생합니다. 예를 들어 다음 컨트롤러는 각 요청마다 `Service::$data` 정적 배열에 무작위 문자열을 계속 추가해 메모리 누수가 생깁니다:

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

애플리케이션을 개발할 때 이런 유형의 메모리 누수를 만드는 것을 특별히 주의해야 하며, 로컬 개발 중에 메모리 사용량을 면밀히 모니터링하는 것이 권장됩니다.

<a name="concurrent-tasks"></a>
## 동시 실행 작업

> [!NOTE]
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 Octane의 `concurrently` 메서드를 이용해 경량 백그라운드 작업을 병렬로 실행할 수 있습니다. PHP 배열 디스트럭처링과 함께 사용해 각 작업의 결과를 얻을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane이 처리하는 동시 작업은 Swoole의 "task worker"를 이용하며, 원래 요청과 완전히 다른 프로세스에서 실행됩니다. 동시 작업을 처리할 수 있는 워커 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정할 수 있습니다:

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="ticks-and-intervals"></a>
## 틱과 인터벌

> [!NOTE]
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 지정한 초마다 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드를 사용하며, 첫 번째 인수는 틱커의 이름(문자열), 두 번째 인수는 호출 가능한 콜백이어야 합니다.

예를 들어, 아래처럼 10초마다 호출되는 클로저를 등록할 수 있습니다. 일반적으로 `tick`은 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메서드와 결합하면 Octane 서버가 처음 부팅될 때 즉시 콜백을 호출하고, 이후 N초 주기로 실행하게 할 수도 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> [!NOTE]
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 Octane 캐시 드라이버를 활용할 수 있는데, 초당 200만 건까지 읽고 쓸 수 있는 엄청난 속도를 제공합니다. 따라서 캐시 레이어에서 극도의 읽기/쓰기 속도가 필요한 애플리케이션에 매우 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 서버 내 모든 워커가 저장된 데이터를 공유할 수 있습니다. 다만 서버가 재시작되면 캐시 데이터가 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!TIP]
> Octane 캐시가 허용하는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel 캐시 시스템의 일반 메서드 외에 Octane 캐시 드라이버는 인터벌 기반 캐시를 지원합니다. 이 캐시는 지정한 주기로 자동 갱신되며, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에 등록하는 것이 좋습니다. 예를 들어, 아래 캐시는 5초마다 자동으로 갱신됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5)
```

<a name="tables"></a>
## 테이블

> [!NOTE]
> 이 기능은 [Swoole](#swoole)을 필요로 합니다.

Swoole 사용 시 원하는 대로 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 조작할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 제공하며, 서버 내 모든 워커가 데이터를 공유할 수 있습니다. 단, 서버가 재시작되면 데이터가 모두 소실됩니다.

테이블은 애플리케이션의 `octane` 설정 파일 `tables` 배열에 정의해야 합니다. 이미 최대 1000개 행을 허용하는 예제 테이블이 설정되어 있습니다. 문자열 컬럼의 최대 크기는 아래 예시처럼 컬럼 타입 뒤에 크기를 지정하면 됩니다:

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

> [!NOTE]
> Swoole 테이블이 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.