# 배포 (Deployment)

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
- [헬스 라우트](#the-health-route)
- [Forge / Vapor를 이용한 편리한 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 동작하도록 하기 위해 할 수 있는 중요한 작업들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 좋은 출발점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버에 다음 최소 PHP 버전과 확장 기능들이 설치되어 있는지 확인해야 합니다:

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

Nginx를 실행하는 서버에 애플리케이션을 배포하는 경우, 아래 예시 설정 파일을 웹 서버 구성 기본값으로 사용할 수 있습니다. 다만, 대부분의 경우 서버 구성에 맞게 해당 파일을 커스터마이징해야 할 것입니다. **서버 관리에 어려움이 있으시면 [Laravel Forge](https://forge.laravel.com)와 같은 Laravel 공식 서버 관리 및 배포 서비스를 고려해 보십시오.**

아래 설정처럼, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 반드시 확인해야 합니다. `index.php` 파일을 프로젝트 루트로 옮겨서 서비스를 제공하려고 하면 중요한 설정 파일들이 외부에 노출될 수 있으므로 절대 시도하지 마십시오:

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

[FrankenPHP](https://frankenphp.dev/)를 이용해 Laravel 애플리케이션을 호스팅할 수도 있습니다. FrankenPHP는 Go 언어로 작성된 현대적 PHP 애플리케이션 서버입니다. Laravel PHP 애플리케이션을 FrankenPHP로 실행하려면 단순히 `php-server` 명령어를 실행하면 됩니다:

```shell
frankenphp php-server -r public/
```

FrankenPHP가 제공하는 Laravel Octane 통합, HTTP/3, 최신 압축 기술, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등 강력한 기능을 활용하려면 FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하시기 바랍니다.

<a name="directory-permissions"></a>
### 디렉터리 권한

Laravel이 `bootstrap/cache` 및 `storage` 디렉터리에 쓸 수 있도록 웹 서버 프로세스 소유자가 이 디렉터리들에 쓰기 권한을 가지고 있는지 확인해야 합니다.

<a name="optimization"></a>
## 최적화

프로덕션에 애플리케이션을 배포할 때는 설정, 이벤트, 라우트, 뷰 등 다양한 파일들을 캐싱하는 것이 좋습니다. Laravel은 이 모든 파일들을 캐싱하는 편리한 `optimize` Artisan 명령어를 제공합니다. 보통 이 명령어는 애플리케이션의 배포 프로세스에서 호출됩니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize`가 생성한 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거할 때 사용할 수 있습니다:

```shell
php artisan optimize:clear
```

이후 문서에서는 `optimize` 명령어가 실행하는 개별 최적화 명령들에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

프로덕션 환경에 애플리케이션을 배포할 때는 배포 과정에서 반드시 `config:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 설정 파일들을 하나의 캐시 파일로 결합하여, 설정 값을 불러올 때 파일시스템 접근 횟수를 크게 줄여줍니다.

> [!WARNING]  
> `config:cache` 명령어를 실행하면 `.env` 파일은 더 이상 로드되지 않으므로, 설정 파일 내에서 `env` 함수를 호출할 때는 주의해야 합니다. 구성 캐시가 된 이후 `env` 함수는 `.env` 변수값에 대해 항상 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션의 자동 발견된 이벤트-리스너 매핑도 배포 과정에서 캐싱하는 것이 좋습니다. 이는 `event:cache` Artisan 명령어로 수행할 수 있습니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

라우트가 많은 대규모 애플리케이션이라면, 배포 시 `route:cache` Artisan 명령어를 반드시 실행하십시오:

```shell
php artisan route:cache
```

이 명령어는 모든 라우트 등록을 하나의 메서드 호출로 단일 캐시 파일에 묶어, 수백 개의 라우트 등록 시 성능을 크게 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션 배포 시 `view:cache` Artisan 명령어를 실행하는 것도 중요합니다:

```shell
php artisan view:cache
```

이 명령어는 Blade 뷰 파일들을 미리 컴파일하여 요청 시 뷰를 바로 렌더링할 수 있도록 하여, 각 요청의 성능을 개선합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 에러 발생 시 사용자에게 얼마나 많은 정보를 보여줄지 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> **프로덕션 환경에서는 항상 이 값이 `false`로 설정되어 있어야 합니다. `APP_DEBUG`가 `true`로 설정된 경우, 민감한 설정 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 헬스 라우트

Laravel은 애플리케이션 상태 모니터링을 위한 기본 헬스 체크 라우트를 제공합니다. 프로덕션에서는 이 라우트를 활용해 업타임 모니터, 로드 밸런서, Kubernetes와 같은 오케스트레이션 시스템에서 애플리케이션 상태를 확인할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up` URL로 제공되며, 애플리케이션이 예외 없이 정상 부팅되면 HTTP 200 응답을, 그렇지 않으면 HTTP 500 응답을 반환합니다. 이 라우트의 URI는 `bootstrap/app` 파일에서 다음과 같이 설정할 수 있습니다:

```
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트에 HTTP 요청이 들어오면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 발생시키므로, 해당 이벤트의 [리스너](/docs/11.x/events) 안에서 애플리케이션의 데이터베이스나 캐시 상태 등 추가 상태 점검을 할 수 있습니다. 문제가 감지되면 리스너에서 예외를 던지면 됩니다.

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor를 이용한 편리한 배포

<a name="laravel-forge"></a>
#### Laravel Forge

서버 구성을 직접 관리할 준비가 되지 않았거나, Laravel 애플리케이션을 운영하는 데 필요한 다양한 서비스를 직접 설정하는 것이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)를 고려해 보십시오.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공자에서 서버를 생성할 수 있습니다. Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등 견고한 Laravel 애플리케이션 운영에 필요한 도구들을 자동으로 설치하고 관리해 줍니다.

> [!NOTE]  
> Laravel Forge를 이용한 배포 가이드가 필요하다면, [Laravel Bootcamp](https://bootcamp.laravel.com/deploying)와 Laracasts에서 제공하는 Forge [동영상 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고하십시오.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전 서버리스(serverless)이며 자동 확장되는 Laravel 전용 배포 플랫폼을 원한다면 [Laravel Vapor](https://vapor.laravel.com)를 확인해 보십시오. Laravel Vapor는 AWS 기반의 서버리스 배포 플랫폼으로, 서버 없이도 인프라를 쉽게 구축하고 확장할 수 있습니다. Laravel의 제작자가 직접 최적화하여 Laravel 애플리케이션을 기존처럼 계속 작성하면서도 서버리스의 장점을 누릴 수 있습니다.