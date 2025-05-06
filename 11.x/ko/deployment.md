# 배포

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [디렉터리 권한](#directory-permissions)
- [최적화](#optimization)
    - [설정 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [헬스(Health) 라우트](#the-health-route)
- [Forge / Vapor로 간편 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 작동할 수 있도록 몇 가지 중요한 조치를 취할 수 있습니다. 이 문서에서는 Laravel 애플리케이션이 올바르게 배포되었는지 확인하기 위한 몇 가지 좋은 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버가 다음의 PHP 최소 버전 및 확장 모듈을 갖추고 있는지 확인하세요:

<div class="content-list" markdown="1">

- PHP >= 8.2
- Ctype PHP 확장
- cURL PHP 확장
- DOM PHP 확장
- Fileinfo PHP 확장
- Filter PHP 확장
- Hash PHP 확장
- Mbstring PHP 확장
- OpenSSL PHP 확장
- PCRE PHP 확장
- PDO PHP 확장
- Session PHP 확장
- Tokenizer PHP 확장
- XML PHP 확장

</div>

<a name="server-configuration"></a>
## 서버 설정

<a name="nginx"></a>
### Nginx

애플리케이션을 Nginx가 실행 중인 서버에 배포하는 경우, 아래와 같은 설정 파일을 웹 서버 설정의 출발점으로 사용할 수 있습니다. 대부분의 경우 이 파일은 서버 구성에 맞게 커스터마이징해야 할 수 있습니다. **서버 관리에 도움이 필요하다면 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 서버 관리 및 배포 서비스를 고려해 보세요.**

아래 설정 예시처럼, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하는지 반드시 확인하십시오. 프로젝트 루트로 `index.php` 파일을 옮겨서 서비스를 제공해서는 안 되며, 그렇게 할 경우 많은 민감한 설정 파일들이 외부에 노출됩니다.

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev/)로도 Laravel 애플리케이션을 서비스할 수 있습니다. FrankenPHP는 Go로 작성된 현대적인 PHP 애플리케이션 서버입니다. FrankenPHP로 Laravel PHP 애플리케이션을 서비스하려면, 다음처럼 `php-server` 명령어를 실행하면 됩니다:

```shell
frankenphp php-server -r public/
```

FrankenPHP가 지원하는 [Laravel Octane](/docs/{{version}}/octane) 통합, HTTP/3, 최신 압축, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등 더 강력한 기능을 활용하려면 FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하세요.

<a name="directory-permissions"></a>
### 디렉터리 권한

Laravel이 `bootstrap/cache`와 `storage` 디렉터리에 쓸 수 있어야 하므로, 웹 서버 프로세스 소유자가 이들 디렉터리에 쓸 수 있는 권한이 있는지 확인해야 합니다.

<a name="optimization"></a>
## 최적화

애플리케이션을 프로덕션에 배포할 때는 설정, 이벤트, 라우트, 뷰 등 여러 파일을 캐싱해야 합니다. Laravel은 이러한 파일을 모두 캐싱하는 단일 `optimize` 아티즌(Artisan) 명령어를 제공합니다. 이 명령어는 일반적으로 애플리케이션 배포 과정의 일부로 실행해야 합니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령어로 생성된 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거합니다:

```shell
php artisan optimize:clear
```

이후 문서에서는 `optimize` 명령어에서 실행되는 각각의 세부 최적화 명령에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

애플리케이션을 프로덕션에 배포할 때는, 배포 과정에서 반드시 `config:cache` 아티즌 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시 파일로 통합하여, 설정 값을 불러올 때 프레임워크가 파일 시스템에 액세스하는 횟수를 크게 줄여줍니다.

> [!WARNING]  
> 배포 과정에서 `config:cache` 명령어를 실행한다면, 설정 파일 안에서만 `env` 함수를 호출해야 합니다. 일단 설정이 캐시되면 `.env` 파일은 더 이상 로드되지 않으며, `.env` 변수에 대한 모든 `env` 함수 호출은 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

배포 과정에서 애플리케이션의 자동 탐색된 이벤트-리스너 매핑을 캐싱해야 합니다. 이를 위해 배포 시 `event:cache` 아티즌 명령어를 실행할 수 있습니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

라우트가 많은 대형 애플리케이션을 개발 중이라면, 배포 과정에서 반드시 `route:cache` 아티즌 명령어를 실행하세요:

```shell
php artisan route:cache
```

이 명령어는 모든 라우트 등록 내역을 캐시 파일 내의 단일 메서드 호출로 변환하여, 수백 개의 라우트를 등록할 때 라우트 등록 성능을 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

애플리케이션을 프로덕션에 배포할 때는 반드시 `view:cache` 아티즌 명령어를 실행하세요:

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여, 요청 시마다 뷰를 즉석에서 컴파일하지 않아도 되므로 뷰를 반환하는 요청의 성능이 향상됩니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 사용자에게 표시되는 오류 정보의 범위를 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일 내 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> **프로덕션 환경에서는 이 값이 항상 `false`여야 합니다. 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되면, 중요한 설정 값이 사용자에게 노출될 수 있습니다.**

<a name="the-health-route"></a>
## 헬스(Health) 라우트

Laravel에는 애플리케이션의 상태를 모니터링할 수 있는 내장 헬스 체크 라우트가 포함되어 있습니다. 프로덕션에서는 이 라우트가 업타임 모니터링, 로드 밸런서, 혹은 Kubernetes와 같은 오케스트레이션 시스템에 애플리케이션 상태를 보고하는 데 사용될 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up`에서 서비스되며, 애플리케이션이 예외 없이 부팅되었다면 200 HTTP 응답을 반환합니다. 그렇지 않으면 500 HTTP 응답이 반환됩니다. 애플리케이션의 `bootstrap/app` 파일에서 이 라우트의 URI를 설정할 수 있습니다:

    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up', // [tl! remove]
        health: '/status', // [tl! add]
    )

이 라우트로 HTTP 요청이 들어올 때 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 디스패치하여, 애플리케이션에 적합한 추가 헬스 체크를 수행할 수 있게 해줍니다. 이 이벤트의 [리스너](/docs/{{version}}/events) 내에서 데이터베이스 또는 캐시 상태를 점검할 수 있습니다. 애플리케이션에 문제가 감지되면, 리스너에서 예외를 던지기만 하면 됩니다.

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor로 간편 배포

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버 환경을 관리할 준비가 되지 않았거나 Laravel 애플리케이션을 운영하는 데 필요한 여러 서비스를 설정하는 것이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)가 훌륭한 대안이 될 수 있습니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에 서버를 생성할 수 있습니다. 또한, Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구의 설치와 관리를 지원합니다.

> [!NOTE]  
> Laravel Forge로 배포하는 전체 가이드가 필요하신가요? [Laravel 부트캠프](https://bootcamp.laravel.com/deploying)와 Laracasts의 Forge [동영상 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고하세요.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전히 서버리스이면서 자동 확장이 가능한 Laravel 맞춤형 배포 플랫폼이 필요하다면 [Laravel Vapor](https://vapor.laravel.com)를 확인해보세요. Laravel Vapor는 AWS 기반의 서버리스 Laravel 배포 플랫폼입니다. Vapor에서 Laravel 인프라를 시작하고, 서버리스가 주는 확장성의 간편함을 경험하세요. Laravel Vapor는 Laravel 제작진이 프레임워크와 완벽하게 동작하도록 조정했으므로, 익숙한 방식대로 계속해서 Laravel 애플리케이션을 개발할 수 있습니다.