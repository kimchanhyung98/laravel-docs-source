# Laravel Octane

- [소개](#introduction)
- [설치](#installation)
- [서버 필수 구성 요소](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 제공](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 제공](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 제공](#serving-your-application-via-nginx)
    - [파일 변경 감시](#watching-for-file-changes)
    - [워커 개수 지정](#specifying-the-worker-count)
    - [최대 요청 수 지정](#specifying-the-max-request-count)
    - [워커 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱 & 인터벌](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개

[Laravel Octane](https://github.com/laravel/octane)는 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 활용해 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅하여 메모리에 유지한 뒤, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

Octane 설치 후, `octane:install` Artisan 명령어를 실행해 Octane 설정 파일을 애플리케이션에 설치할 수 있습니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 필수 구성 요소

> **경고**  
> Laravel Octane은 [PHP 8.0+](https://php.net/releases/)를 필요로 합니다.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리를 기반으로 작동합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 바이너리를 다운로드 및 설치할지 물어봅니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail로 RoadRunner 사용

[Laravel Sail](/docs/{{version}}/sail)로 애플리케이션을 개발하려면, 아래 명령어를 실행해 Octane과 RoadRunner를 설치하세요.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

다음으로 Sail 셸을 시작하고, 최신 RoadRunner 바이너리를 받기 위해 `rr` 실행 파일을 사용하세요.

```shell
./vendor/bin/sail shell

# Sail 셸 내부에서...
./vendor/bin/rr get-binary
```

RoadRunner 바이너리 설치 후 Sail 셸에서 나올 수 있습니다. 이제 애플리케이션이 계속 실행되도록 Sail이 사용하는 `supervisor.conf` 파일을 조정해야 합니다. 먼저 `sail:publish` Artisan 명령어를 실행하세요.

```shell
./vendor/bin/sail artisan sail:publish
```

그 다음, 애플리케이션의 `docker/supervisord.conf` 파일의 `command` 지시문을 변경하여, PHP 개발 서버 대신 Octane이 애플리케이션을 서비스하도록 하세요.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80
```

마지막으로, `rr` 바이너리에 실행 권한을 부여하고 Sail 이미지를 빌드하세요.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버를 사용하여 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다.

```shell
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail로 Swoole 사용

> **경고**  
> Sail을 통해 Octane 애플리케이션을 서비스하기 전에 최신 Laravel Sail을 설치하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는, [Laravel Sail](/docs/{{version}}/sail) 공식 Docker 기반 개발 환경을 사용해 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail은 기본적으로 Swoole 확장 모듈을 포함합니다. 그러나 애플리케이션이 계속 실행되도록 Sail이 사용하는 `supervisor.conf` 파일을 조정해야 합니다. 먼저 `sail:publish` Artisan 명령어를 실행하세요.

```shell
./vendor/bin/sail artisan sail:publish
```

그 다음, PHP 개발 서버 대신 Octane이 애플리케이션을 서비스하도록 `docker/supervisord.conf`의 `command`를 수정하세요.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

마지막으로 Sail 이미지를 빌드하세요.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 `octane` 설정 파일에 필요하다면 추가로 설정할 수 있는 몇 가지 옵션이 있습니다. 이 옵션들은 거의 수정할 필요가 없기 때문에 기본 설정 파일에는 들어있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 제공

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령은 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 사용합니다.

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`을 통해 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
### HTTPS를 통한 애플리케이션 제공

기본적으로 Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. HTTPS 환경에서 애플리케이션을 서비스할 때, `config/octane.php`의 `OCTANE_HTTPS` 환경 변수를 `true`로 설정할 수 있습니다. 이 값을 `true`로 지정하면, Octane이 Laravel에 모든 생성된 링크 앞에 `https://`를 붙이도록 지시합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 제공

> **참고**  
> 직접 서버 구성을 관리할 준비가 되어 있지 않거나 다양한 서비스 구성을 통한 안정적인 Laravel Octane 애플리케이션 운영에 익숙하지 않은 경우, [Laravel Forge](https://forge.laravel.com)를 참고하세요.

프로덕션 환경에서는 Octane 애플리케이션을 Nginx나 Apache와 같은 전통적인 웹 서버 뒤에서 제공하는 것이 좋습니다. 이렇게 하면 정적 자산(이미지, 스타일시트 등) 제공 및 SSL 인증서 관리가 가능합니다.

아래 Nginx 예제는 정적 자산은 Nginx가 제공하고, 다른 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다.

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

Octane 서버를 시작할 때 애플리케이션이 한 번 메모리에 로드되기 때문에, 파일을 수정해도 브라우저를 새로고침하는 것만으로는 변경 사항이 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 추가해도 서버를 재시작하기 전까진 적용되지 않습니다. 편의를 위해, `--watch` 플래그를 사용하여 애플리케이션 내 파일 변경 시 Octane 서버가 자동으로 재시작되도록 할 수 있습니다.

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전에 [Node](https://nodejs.org)가 로컬 개발 환경에 설치되어 있는지 확인하세요. 그리고 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 프로젝트에 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일은 애플리케이션의 `config/octane.php` 파일 내 `watch` 설정 옵션을 통해 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정

기본적으로 Octane은 시스템 CPU 코어 수만큼 요청 워커를 시작합니다. 이 워커들은 들어오는 HTTP 요청을 처리합니다. `octane:start` 명령 실행시 `--workers` 옵션으로 직접 워커 개수를 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4
```

Swoole 서버 사용 시, ["태스크 워커"](concurrent-tasks)를 몇 개 시작할지도 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

메모리 누수를 방지하기 위해 Octane은 워커가 500건의 요청을 처리할 때마다 정상적으로 재시작합니다. 이 요청 수는 `--max-requests` 옵션으로 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 워커 재시작

`octane:reload` 명령으로 Octane 서버의 애플리케이션 워커를 정상적으로 재시작할 수 있습니다. 보통 배포 후 새로 배포한 코드를 메모리에 로드하고 이후 요청들에 적용되게 하려면, 이 과정을 거쳐야 합니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령을 이용해 Octane 서버를 중지할 수 있습니다.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령으로 Octane 서버의 현재 상태를 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane

Octane은 애플리케이션을 한 번 부팅해서 메모리에 유지하며 요청을 서비스합니다. 이로 인해 애플리케이션을 구축할 때 유의해야 할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메소드는 요청 워커가 처음 부팅될 때 한 번만 실행되며, 이후 요청은 같은 애플리케이션 인스턴스를 재사용합니다.

따라서, 애플리케이션 서비스 컨테이너나 요청 인스턴스를 객체의 생성자에 주입할 경우, 요청마다 해당 객체가 오래된 컨테이너나 요청 인스턴스를 참조할 수 있습니다.

Octane은 프레임워크의 1차 상태를 요청마다 자동으로 초기화합니다. 하지만, 애플리케이션 자체가 생성하는 글로벌 상태에 대해서는 Octane이 항상 재설정 방법을 알지 못합니다. 따라서 Octane에 적합한 방식으로 애플리케이션을 구조화하는 방법을 이해해야 합니다. 아래에서 가장 흔히 발생할 수 있는 문제 상황을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 다음 바인딩은 서비스 컨테이너 전체를 싱글톤 객체에 주입합니다.

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

이 예제에서, `Service` 인스턴스가 애플리케이션 부트 과정에서 해석되면, 그 컨테이너가 서비스에 주입되고 이후 모든 요청에서 같은 컨테이너 인스턴스가 유지됩니다. 이는 애플리케이션에 문제가 되지 않을 수도 있지만, 부트 사이클 후반이나 이후 요청에서 바인딩이 추가되어도 컨테이너에 반영되지 않을 위험이 있습니다.

해결 방법으로는 바인딩을 싱글톤으로 등록하지 않거나, 항상 최신 컨테이너 인스턴스를 해석하는 클로저를 주입할 수 있습니다.

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메소드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
### 요청 주입

일반적으로, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 다음 바인딩은 전체 요청 인스턴스를 싱글톤 객체에 주입합니다.

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

이 예제에서 `Service` 인스턴스가 부트 과정에서 해석되면 HTTP 요청이 주입되고, 이후 모든 요청에서 같은 요청 인스턴스를 참조하게 됩니다. 따라서 모든 헤더, 입력값, 쿼리 스트링 등 요청 데이터가 잘못되기 쉽습니다.

해결 방법으로는 바인딩을 싱글톤에서 해제하거나, 항상 최신 요청 인스턴스를 반환하는 클로저를 주입할 수 있습니다. 혹은, 가장 추천하는 방법은 런타임에서 객체가 필요로 하는 구체적인 요청 정보를 해당 메소드에 직접 전달하는 것입니다.

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

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청을 반환하므로 안전하게 사용할 수 있습니다.

> **경고**  
> 컨트롤러 메소드와 라우트 클로저에서 `Illuminate\Http\Request`를 타입힌트로 사용하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

일반적으로, 설정 저장소 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 아래 바인딩은 설정 저장소를 싱글톤 객체에 주입합니다.

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

이 경우, 요청 사이에 설정 값이 변경된다면 해당 서비스는 새로운 값을 볼 수 없습니다. 원래의 저장소 인스턴스에 의존하기 때문입니다.

해결 방법으로는 바인딩을 싱글톤으로 등록하지 않거나, 항상 최신 설정 저장소를 해석하는 클로저를 주입할 수 있습니다.

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

글로벌 `config`는 항상 최신 설정 저장소를 반환하므로 애플리케이션 내에서 안전합니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간에 애플리케이션을 메모리에 유지하므로, 정적으로 관리되는 배열에 데이터를 추가하면 메모리 누수가 발생합니다. 예를 들어, 아래 컨트롤러에서는 각 요청마다 static `$data` 배열에 데이터가 계속 추가되어 메모리 누수가 일어납니다.

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

애플리케이션을 개발할 때 이런 형태의 메모리 누수를 만들지 않도록 주의해야 합니다. 로컬 개발 과정에서 애플리케이션의 메모리 사용량을 모니터링하여 새로운 메모리 누수가 발생하지 않도록 관리하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> **경고**  
> 이 기능은 [Swoole](#swoole) 필요.

Swoole 사용 시, 가벼운 백그라운드 태스크를 통해 작업을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메소드를 사용하여 이를 구현할 수 있습니다. PHP 배열 디스트럭처링과 함께 사용해 각 작업의 결과를 받을 수 있습니다.

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane이 처리하는 동시 작업은 Swoole의 "태스크 워커"를 사용하며, 기존 요청과는 완전히 다른 프로세스에서 실행됩니다. 동시 태스크를 처리할 워커 개수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정합니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메소드 사용 시 Swoole 태스크 시스템의 제한으로 인해 1024개 이상의 태스크를 제공하면 안 됩니다.

<a name="ticks-and-intervals"></a>
## 틱 & 인터벌

> **경고**  
> 이 기능은 [Swoole](#swoole) 필요.

Swoole 사용 시, 일정 간격마다 실행되는 "틱" 작업을 등록할 수 있습니다. `tick` 메소드로 틱 콜백을 등록할 수 있습니다. 첫 번째 인자는 티커의 이름, 두 번째 인자는 지정한 간격마다 호출될 콜러블입니다.

아래 예제는 10초마다 호출되는 클로저를 등록하는 방법입니다. 보통 `tick` 메소드는 서비스 프로바이더의 `boot` 메소드 내에서 호출합니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` 메소드를 사용하면 Octane 서버가 부팅될 때 즉시 틱 콜백을 실행하고, 이후 N초마다 반복 실행할 수 있습니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시

> **경고**  
> 이 기능은 [Swoole](#swoole) 필요.

Swoole 사용 시, Octane 캐시 드라이버를 활용할 수 있습니다. 이 드라이버는 초당 2백만 회 이상의 읽기/쓰기 속도를 제공하며, 빠른 캐시 계층이 필요한 애플리케이션에 적합합니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 동작합니다. 서버 내 모든 워커에서 캐시된 데이터에 접근할 수 있습니다. 하지만 서버가 재시작되면 캐시된 데이터는 삭제됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> **참고**  
> Octane 캐시에 허용되는 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌

Laravel의 일반적인 캐시 시스템 외에도, Octane 캐시 드라이버는 인터벌 기반 캐시를 지원합니다. 이 캐시는 지정한 간격마다 자동으로 갱신되며, 서비스 프로바이더의 `boot` 메소드에서 등록해야 합니다. 아래 예제는 5초마다 갱신되는 캐시 사용 예시입니다.

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블

> **경고**  
> 이 기능은 [Swoole](#swoole) 필요.

Swoole 사용 시, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 제공하며, 서버의 모든 워커에서 데이터를 접근할 수 있습니다. 하지만 서버가 재시작되면 데이터는 사라집니다.

테이블 정의는 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에 작성해야 합니다. 최대 1000행을 허용하는 예제 테이블이 이미 구성되어 있습니다. 문자열 컬럼의 최대 길이는 컬럼 타입 뒤에 숫자로 지정할 수 있습니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메소드를 사용하세요.

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> **경고**  
> Swoole 테이블에서 지원하는 컬럼 타입: `string`, `int`, `float`입니다.