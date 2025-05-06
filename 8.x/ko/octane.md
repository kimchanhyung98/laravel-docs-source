# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 요구사항](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS를 통한 서비스](#serving-your-application-via-https)
    - [Nginx를 통한 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [Worker 수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [Worker 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입 & Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [Request 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱 & 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 통해 여러분의 애플리케이션 성능을 대폭 향상시킵니다. Octane은 애플리케이션을 한 번 부팅하고 메모리에 유지한 채, supersonic 속도로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

```bash
composer require laravel/octane
```

Octane 설치 후에는 `octane:install` Artisan 명령어를 실행해 애플리케이션에 Octane의 설정 파일을 설치하세요:

```bash
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 요구사항

> {note} Laravel Octane은 [PHP 8.0+](https://php.net/releases/)가 필요합니다.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리에 의해 구동됩니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane이 RoadRunner 바이너리를 다운로드하여 설치하는 과정을 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Laravel Sail](/docs/{{version}}/sail)로 개발할 계획이라면 다음 명령어를 사용하여 Octane 및 RoadRunner를 설치하세요:

```bash
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

다음으로, Sail 셸을 시작해서 `rr` 실행 파일로 RoadRunner 바이너리의 최신 리눅스 빌드를 받아옵니다:

```bash
./vendor/bin/sail shell

# Sail 셸 내에서...
./vendor/bin/rr get-binary
```

RoadRunner 바이너리 설치 후, Sail 셸 세션을 종료합니다. 이후, Sail이 애플리케이션을 계속 실행하도록 `supervisor.conf` 파일을 수정해야 합니다. 우선 `sail:publish` Artisan 명령어를 실행하세요:

```bash
./vendor/bin/sail artisan sail:publish
```

다음으로, 애플리케이션의 `docker/supervisord.conf` 파일의 `command` 지시어를 아래와 같이 수정하여 Sail이 PHP 개발 서버가 아닌 Octane으로 애플리케이션을 서비스하도록 하세요:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=8000
```

마지막으로, `rr` 바이너리의 실행 권한을 부여하고 Sail 이미지를 빌드합니다:

```bash
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션을 Swoole로 서비스하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치합니다:

```bash
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> {note} Sail로 Octane 애플리케이션을 제공하기 전에, 최신 버전의 Laravel Sail이 설치되어 있는지 확인하고 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는 [Laravel Sail](/docs/{{version}}/sail), 공식 Docker 기반 개발 환경을 사용하여 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail에는 Swoole 확장이 기본 포함되어 있습니다. 그러나, 애플리케이션을 계속 실행하도록 Sail이 사용하는 `supervisor.conf` 파일을 수정해야 합니다. 우선 `sail:publish` Artisan 명령어를 실행하세요:

```bash
./vendor/bin/sail artisan sail:publish
```

다음으로, `docker/supervisord.conf` 파일의 `command` 지시어를 아래와 같이 수정합니다:

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

마지막으로 Sail 이미지를 빌드합니다:

```bash
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 `octane` 설정 파일에 필요시 추가할 수 있는 몇 가지 추가 설정 옵션을 지원합니다. 대개 변경하지 않으므로 기본 설정 파일에는 포함되어 있지 않습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
];
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 기본적으로 이 명령어는 `octane` 설정 파일의 `server` 설정 옵션에 지정된 서버를 사용합니다:

```bash
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 서비스

Octane을 통해 실행되는 애플리케이션은 기본적으로 `http://`로 접두사가 붙은 링크를 생성합니다. `config/octane.php` 설정 파일 내에서 사용하는 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면 HTTPS 환경에서 애플리케이션을 서비스할 수 있습니다. 이 값을 `true`로 하면, Octane이 모든 생성된 링크에 `https://`로 접두사를 붙이도록 Laravel에게 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 서비스

> {tip} 서버 설정에 익숙하지 않거나 robust한 Laravel Octane 애플리케이션 실행에 필요한 다양한 서비스 설정이 부담스럽다면 [Laravel Forge](https://forge.laravel.com)를 참고하세요.

운영 환경에서는 기존 웹 서버(Nginx 혹은 Apache) 뒤에서 Octane 애플리케이션을 서비스하는 것이 좋습니다. 이렇게 하면 정적 자산(이미지, 스타일시트 등) 및 SSL 인증서 관리를 웹 서버가 담당하게 됩니다.

아래의 Nginx 설정 예시에서는 정적 자산은 Nginx가 제공하고 나머지 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다:

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
### 파일 변경 감지

Octane 서버가 시작될 때 애플리케이션이 메모리에 한번만 로딩되므로, 코드 변경 사항은 브라우저를 새로고침해도 반영되지 않습니다. 예를 들어, `routes/web.php` 파일에 라우트를 추가하였다면 서버 재시작 전까지 반영되지 않습니다. 이런 불편을 줄이기 위해, `--watch` 플래그를 사용하면 애플리케이션 내 파일이 변경될 때마다 자동으로 서버를 재시작하도록 Octane에 지시할 수 있습니다:

```bash
php artisan octane:start --watch
```

이 기능을 사용하기 전에, 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 합니다. 그리고 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감지 라이브러리도 설치해야 합니다:

```bash
npm install --save-dev chokidar
```

관찰할 디렉터리 및 파일은 `config/octane.php` 파일의 `watch` 옵션에서 설정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### Worker 수 지정

기본적으로, Octane은 기기의 CPU 코어 수 만큼의 request worker를 시작합니다. 이 worker들은 유입되는 HTTP 요청을 처리합니다. `octane:start` 명령어에서 `--workers` 옵션으로 원하는 worker 수를 직접 지정할 수 있습니다:

```bash
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용할 때는 ["task worker"](#concurrent-tasks) 수를 다음과 같이 지정할 수 있습니다:

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

의도치 않은 메모리 누수를 방지하기 위해, Octane은 워커가 특정 요청 수를 처리한 후 워커를 정상적으로 재시작할 수 있습니다. `--max-requests` 옵션을 사용하여 설정할 수 있습니다:

```bash
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### Worker 재시작

`octane:reload` 명령어로 Octane 서버의 application worker를 정상적으로 재시작할 수 있습니다. 배포 후 새롭게 배포된 코드가 메모리에 반영되어 이후 요청에 적용되게 하려면 이렇게 하세요:

```bash
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어를 통해 Octane 서버를 중지할 수 있습니다:

```bash
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령어로 Octane 서버의 현재 상태를 확인할 수 있습니다:

```bash
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입 & Octane

Octane은 애플리케이션을 한 번 부팅하고, 요청을 처리하는 동안 메모리에 유지합니다. 그로 인해 개발 시 고려해야 할 주의점이 몇 가지 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메소드는 워커가 처음 부팅될 때 단 한 번만 실행됩니다. 이후 요청마다 동일한 애플리케이션 인스턴스가 재사용됩니다.

따라서, 서비스 컨테이너 또는 요청 인스턴스를 어떤 객체의 생성자(constructor)에 주입할 때 주의해야 합니다. 그렇게 할 경우, 해당 객체가 이후 요청에서 오래된(구식) 컨테이너나 요청 인스턴스를 갖게 될 수 있습니다.

Octane은 프레임워크의 1차 상태는 매 요청마다 자동으로 리셋하지만, 여러분이 직접 생성한 글로벌 상태는 항상 적절히 리셋하지 못합니다. 따라서 Octane 친화적인 애플리케이션 구조를 이해하는 게 중요합니다. 아래는 Octane 사용 시 자주 문제가 되는 몇 가지 상황을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로, 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 아래와 같이 전체 서비스 컨테이너를 싱글턴에 주입하는 바인딩이 있습니다:

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

이 예시에서 `Service` 인스턴스가 애플리케이션 부팅 과정에서 resolve 된다면, 해당 컨테이너 인스턴스가 서비스에 주입되고, 이후 요청에서 동일한 컨테이너가 `Service` 인스턴스에 유지됩니다. 이는 여러분의 애플리케이션에서 문제가 없을 수도 있지만, 부팅 도중 혹은 이후 요청에서 추가된 바인딩을 놓치는 등 예기치 못한 동작이 발생할 수도 있습니다.

해결법으로는 싱글턴이 아닌 일반 바인딩으로 등록하거나, 현재 컨테이너 인스턴스를 항상 resolve하는 클로저를 주입하세요:

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메소드는 항상 최신 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
### Request 주입

애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 일반적으로 피해야 합니다. 예를 들어, 전체 요청 인스턴스를 싱글턴에 주입하는 바인딩은 다음과 같습니다:

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

이 경우, `Service` 인스턴스가 애플리케이션 부팅 과정에서 resolve 될 때 HTTP 요청이 주입되고, 이후 요청에서도 동일한 요청이 유지됩니다. 따라서 모든 헤더, 입력, 쿼리스트링 데이터 등이 잘못될 수 있습니다.

해결법으로는 싱글턴이 아닌 일반 바인딩으로 등록하거나, 항상 최신 요청 인스턴스를 resolve하는 클로저를 주입하는 방법이 있습니다. 또는, 추천 방법으로 객체가 필요한 요청 정보를 런타임에 명시적으로 메서드에 전달하세요:

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청을 반환하므로, 안전하게 사용할 수 있습니다.

> {note} 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request`를 타입-힌트하는 것은 괜찮습니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

설정 저장소 인스턴스를 다른 객체의 생성자에 주입하는 것은 일반적으로 피해야 합니다. 예를 들어, 설정 저장소를 싱글턴에 주입하는 바인딩입니다:

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

이 경우, 요청 간에 설정 값이 변경되어도 서비스가 최초 주입된 설정 저장소만 참조하게 되어 새로운 값에 접근할 수 없습니다.

해결법으로는 싱글턴이 아닌 바인딩으로 등록하거나, 항상 최신 설정 저장소 인스턴스를 resolve하는 클로저를 주입하세요:

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

글로벌 `config` 헬퍼는 항상 최신 설정 저장소를 반환하므로, 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간에 애플리케이션을 메모리에 유지합니다. 따라서, 정적 배열 등에 데이터를 추가하면 메모리 누수가 발생할 수 있습니다. 아래의 컨트롤러는 요청이 들어올 때마다 정적 `$data` 배열에 데이터를 계속 추가하므로 메모리 누수가 일어납니다:

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

이런 유형의 메모리 누수가 발생하지 않도록 각별히 주의해야 하며, 로컬 개발 중 애플리케이션의 메모리 사용량을 모니터링하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> {note} 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 경량화된 백그라운드 태스크를 통해 작업을 동시 실행할 수 있습니다. 이는 Octane의 `concurrently` 메서드를 통해 구현할 수 있습니다. PHP 배열 해체 기능과 함께 사용하면, 각 작업의 결과를 손쉽게 받을 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane이 처리하는 동시 작업은 Swoole의 "task worker"에서 실행되며, 요청과는 별도의 프로세스에서 동작합니다. 동시 태스크 처리를 위한 worker 수는 `octane:start` 명령의 `--task-workers` 옵션으로 결정됩니다:

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="ticks-and-intervals"></a>
## 틱 & 인터벌

> {note} 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole 사용 시 지정한 초마다 실행되는 "틱" 작업을 등록할 수 있습니다. `tick` 메서드로 "틱" 콜백을 등록하면 됩니다. 첫 번째 인자는 ticker의 이름, 두 번째 인자는 지정된 주기에 실행될 콜러블입니다.

예를 들어, 10초마다 호출되는 클로저를 등록할 수 있습니다. 보통 `tick` 메소드는 애플리케이션 서비스 프로바이더의 `boot` 메소드에서 호출됩니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메서드를 사용하면, Octane 서버 부팅 시점과 이후 N초마다 즉시 틱 콜백을 실행하도록 지시할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> {note} 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용하면, 최대 초당 2백만 번의 읽기/쓰기 속도를 제공하는 Octane 캐시 드라이버를 사용할 수 있습니다. 따라서, 캐싱 계층에서 극도의 읽기/쓰기 성능이 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)로 동작합니다. 서버 내 모든 worker가 캐시에 저장된 데이터에 접근할 수 있습니다. 단, 서버가 재시작되면 캐시된 데이터는 모두 소실됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> {tip} Octane 캐시에 허용되는 최대 엔트리 수는 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel의 일반적인 캐시 시스템 메서드 외에, Octane 캐시 드라이버는 인터벌 기반 캐시도 제공합니다. 해당 캐시는 지정한 주기마다 자동으로 갱신되며, 애플리케이션 서비스 프로바이더의 `boot` 메소드에서 등록하는 것이 좋습니다. 아래는 5초마다 갱신되는 캐시 예시입니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5)
```

<a name="tables"></a>
## 테이블

> {note} 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의/조작할 수 있습니다. Swoole 테이블은 뛰어난 성능을 제공하며, 서버의 모든 worker가 데이터를 접근할 수 있습니다. 단, 서버가 재시작되면 데이터가 모두 소실됩니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 설정 배열에 정의합니다. 1000개 행을 허용하는 예시 테이블이 미리 구성되어 있습니다. 문자열 컬럼의 최대 크기는 아래와 같이 타입 뒤에 크기를 지정해 설정할 수 있습니다:

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

> {note} Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.