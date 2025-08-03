# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [디렉토리 권한](#directory-permissions)
- [최적화](#optimization)
    - [설정 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [헬스 체크 라우트](#the-health-route)
- [Laravel Cloud 또는 Forge를 이용한 배포](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었을 때, 애플리케이션이 최대한 효율적으로 동작하도록 하기 위한 중요한 작업들이 있습니다. 본 문서에서는 Laravel 애플리케이션이 올바르게 배포되었는지 확인하기 위한 기본적인 시작점들을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크를 사용하기 위해서는 시스템 요구사항이 있습니다. 웹 서버가 다음 최소 PHP 버전과 확장 기능들을 갖추고 있는지 확인해야 합니다:

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

Nginx가 실행되는 서버에 애플리케이션을 배포하는 경우, 아래 예시를 출발점으로 삼아 웹 서버 설정 파일을 구성할 수 있습니다. 서버 설정에 따라 이 파일은 대부분 맞춤 설정이 필요합니다. **서버 관리를 돕고 싶으시다면, 완전 관리형 Laravel 플랫폼인 [Laravel Cloud](https://cloud.laravel.com)를 사용하는 것도 고려해보세요.**

아래 예시처럼, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 반드시 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 옮겨서 실행하면, 민감한 설정 파일들이 외부에 노출되어 보안상 매우 위험하므로 절대로 그렇게 해서는 안 됩니다:

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

[FrankenPHP](https://frankenphp.dev/)도 Laravel 애플리케이션을 서비스하는 데 사용할 수 있습니다. FrankenPHP는 Go 언어로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 이용하여 Laravel PHP 애플리케이션을 서비스하려면, 간단히 `php-server` 명령어를 실행하면 됩니다:

```shell
frankenphp php-server -r public/
```

FrankenPHP가 지원하는 더 강력한 기능들 — 예를 들어 [Laravel Octane](/docs/12.x/octane) 통합, HTTP/3, 최신 압축, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등을 활용하려면, FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하세요.

<a name="directory-permissions"></a>
### 디렉토리 권한

Laravel은 `bootstrap/cache`와 `storage` 디렉토리에 쓰기 작업을 수행해야 합니다. 따라서 웹 서버 프로세스의 소유자에게 이 디렉토리들에 대한 쓰기 권한이 부여되어 있는지 반드시 확인하세요.

<a name="optimization"></a>
## 최적화

애플리케이션을 프로덕션 환경에 배포할 때는 설정 파일, 이벤트, 라우트, 뷰 등 다양한 파일들을 캐싱해야 합니다. Laravel은 이 모든 캐싱 작업을 한 번에 간편하게 실행할 수 있도록 `optimize` Artisan 명령어를 제공합니다. 이 명령어는 보통 배포 과정에서 실행합니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령어로 생성된 모든 캐시 파일과, 기본 캐시 드라이버에 저장된 모든 키를 삭제할 때 사용합니다:

```shell
php artisan optimize:clear
```

아래에서는 `optimize` 명령어가 내부적으로 실행하는 세부 최적화 명령어들을 살펴보겠습니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

프로덕션에 배포할 때 반드시 `config:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel 설정 파일 전체를 하나의 캐시 파일로 결합하여, 설정 값을 불러올 때 파일 시스템 접근 횟수를 크게 줄여줍니다.

> [!WARNING]
> `config:cache` 명령어를 실행하면, 설정 파일 내에서 반드시 `env` 함수를 호출하지 않도록 주의해야 합니다. 설정이 캐싱되면 `.env` 파일은 더 이상 로드되지 않고, `env` 함수가 반환하는 값은 모두 `null`이 됩니다.

<a name="caching-events"></a>
### 이벤트 캐싱

자동으로 발견된 이벤트와 리스너 매핑 정보를 배포 과정에서 캐싱하는 것이 좋습니다. 이는 `event:cache` Artisan 명령어로 실행할 수 있습니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

많은 라우트를 가진 대규모 애플리케이션의 경우, `route:cache` Artisan 명령어를 꼭 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령어는 수백 개의 라우트 등록 작업을 단일 메서드 호출로 줄인 캐시 파일로 압축하여, 라우트 등록 성능을 크게 향상합니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션에 배포할 때는 `view:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여 요청 시점에 바로 사용할 수 있도록 해, 뷰 렌더링 성능을 높입니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 오류가 발생했을 때 사용자에게 보여주는 정보의 정도를 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 있는 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> **프로덕션 환경에서는 이 값이 항상 `false`로 설정되어야 합니다. `APP_DEBUG` 변수가 `true`로 설정되면, 애플리케이션의 민감한 설정 정보가 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 헬스 체크 라우트

Laravel은 애플리케이션 상태를 모니터링할 수 있는 내장 헬스 체크 라우트를 제공합니다. 프로덕션 환경에서는 이 라우트를 이용해 애플리케이션 상태를 가동 시간 모니터링, 로드 밸런서, 또는 Kubernetes 같은 오케스트레이션 시스템에 알릴 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up` 경로에서 서비스되며, 애플리케이션이 예외 없이 정상 부팅되었으면 HTTP 200 응답을 반환합니다. 예외가 발생하면 HTTP 500 응답을 반환합니다. 해당 라우트 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트로 HTTP 요청이 오면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 발생시키므로, 이벤트 [리스너](/docs/12.x/events)에서 데이터베이스나 캐시 상태 등 애플리케이션 관련 추가 헬스 체크를 수행할 수 있습니다. 문제가 감지되면 리스너 내에서 예외를 발생시키면 됩니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 이용한 배포

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel에 최적화된 완전 관리형 오토스케일링 배포 플랫폼을 원한다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해보세요. Laravel Cloud는 관리되는 컴퓨트, 데이터베이스, 캐시, 오브젝트 스토리지를 제공하는 강력한 Laravel 배포 플랫폼입니다.

Laravel Cloud에서 Laravel 애플리케이션을 시작하여 확장 가능한 간편함을 경험해보세요. Laravel 제작자들이 직접 조율한 Laravel Cloud는 프레임워크와 완벽하게 통합되어, 익숙한 방식 그대로 Laravel 애플리케이션을 개발할 수 있습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버를 관리하되, 다양한 서비스를 설정하는 데 어려움이 있다면 [Laravel Forge](https://forge.laravel.com)를 활용하세요. Forge는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 공급자에서 서버를 생성할 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션 환경을 구축하는 데 필요한 툴들을 자동으로 설치·관리합니다.