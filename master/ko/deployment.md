# 배포(Deployment)

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 구성](#server-configuration)
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

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 실행되기 위해 할 수 있는 중요한 사항이 몇 가지 있습니다. 이 문서에서는 Laravel 애플리케이션이 제대로 배포되었는지 확인하기 위한 기본적인 지침들을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크를 동작시키기 위해 필요한 시스템 요구사항이 있습니다. 웹 서버에 아래의 최소 PHP 버전과 확장 모듈이 설치되어 있는지 확인하세요:

<div class="content-list" markdown="1">

- PHP >= 8.2
- Ctype PHP 확장 모듈
- cURL PHP 확장 모듈
- DOM PHP 확장 모듈
- Fileinfo PHP 확장 모듈
- Filter PHP 확장 모듈
- Hash PHP 확장 모듈
- Mbstring PHP 확장 모듈
- OpenSSL PHP 확장 모듈
- PCRE PHP 확장 모듈
- PDO PHP 확장 모듈
- Session PHP 확장 모듈
- Tokenizer PHP 확장 모듈
- XML PHP 확장 모듈

</div>

<a name="server-configuration"></a>
## 서버 구성

<a name="nginx"></a>
### Nginx

애플리케이션을 Nginx를 사용하는 서버에 배포하는 경우, 아래의 설정 파일을 참고하여 웹 서버를 설정할 수 있습니다. 실제 서버 환경에 따라 파일을 수정해야 할 수 있습니다. **서버 관리를 도와줄 관리형 Laravel 플랫폼을 원한다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 서비스를 고려하세요.**

아래의 설정처럼, 모든 요청이 애플리케이션의 `public/index.php` 파일로 전달되도록 웹 서버를 구성해야 합니다. `index.php` 파일을 프로젝트 루트로 옮기지 마세요. 루트에서 애플리케이션을 제공하면 여러 민감한 설정 파일이 외부에 노출될 수 있습니다:

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

[FrankenPHP](https://frankenphp.dev/)도 Laravel 애플리케이션을 서비스하는 데 사용할 수 있습니다. FrankenPHP는 Go로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP의 `php-server` 명령어로 Laravel PHP 애플리케이션을 간단히 실행할 수 있습니다:

```shell
frankenphp php-server -r public/
```

HTTP/3, 모던 압축, [Laravel Octane](/docs/{{version}}/octane) 통합, Laravel 애플리케이션을 단일 바이너리로 패키징 등 FrankenPHP가 지원하는 강력한 기능을 활용하려면 FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하세요.

<a name="directory-permissions"></a>
### 디렉토리 권한

Laravel은 `bootstrap/cache` 및 `storage` 디렉토리에 쓰기 작업이 필요합니다. 따라서 웹 서버 프로세스 소유자가 해당 디렉토리에 쓸 수 있는 권한을 가지고 있는지 반드시 확인하세요.

<a name="optimization"></a>
## 최적화

애플리케이션을 프로덕션 환경에 배포할 때는 설정, 이벤트, 라우트, 뷰 등 다양한 파일을 캐싱하는 것이 좋습니다. Laravel은 이 모든 파일을 캐싱하는 편리한 `optimize` 아티즌(Artisan) 명령어를 제공합니다. 이 명령어는 보통 배포 프로세스의 일부로 실행해야 합니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령어로 생성된 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거합니다:

```shell
php artisan optimize:clear
```

아래 문서에서는 `optimize` 명령어가 실행하는 각 세부 최적화 명령어에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

애플리케이션을 프로덕션 환경에 배포할 때는, 배포 프로세스 중 `config:cache` 아티즌 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령은 Laravel의 모든 설정 파일을 하나의 캐시 파일로 병합하여, 설정 값을 불러올 때 프레임워크가 파일 시스템에 접근하는 횟수를 대폭 줄여줍니다.

> [!WARNING]
> 배포 시 `config:cache` 명령어를 실행하는 경우, 반드시 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐시되면 `.env` 파일이 로드되지 않으며, 이후 `.env` 값을 가져오기 위한 `env` 함수 호출은 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

배포 시 애플리케이션이 자동으로 탐지한 이벤트-리스너 매핑 정보를 캐싱해야 합니다. 배포 과정 중 `event:cache` 아티즌 명령어를 실행하면 됩니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

많은 라우트를 가진 대규모 애플리케이션이라면 배포 과정에서 반드시 `route:cache` 아티즌 명령어를 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령은 모든 라우트 등록을 하나의 메서드 호출로 변환하여 캐시 파일에 저장함으로써, 수백 개의 라우트를 등록할 때 라우트 등록 성능을 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

애플리케이션을 프로덕션 환경에 배포할 때는, 배포 과정 중 `view:cache` 아티즌 명령어를 실행해야 합니다:

```shell
php artisan view:cache
```

이 명령은 모든 Blade 뷰를 미리 컴파일하여, 요청 시마다 뷰를 매번 컴파일하지 않아도 되고, 성능이 크게 향상됩니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 에러 발생 시 사용자에게 표시되는 정보의 수준을 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

> [!WARNING]
> **프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 만약 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되면, 민감한 설정 값이 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 헬스 체크 라우트

Laravel은 애플리케이션의 상태를 모니터링할 수 있는 내장 헬스 체크 라우트를 제공합니다. 프로덕션 환경에서 이 라우트는 업타임 모니터, 로드 밸런서, Kubernetes와 같은 오케스트레이션 시스템에 애플리케이션의 상태를 보고하는 데 사용할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up`에서 제공되며, 애플리케이션이 예외 없이 부팅된 경우 HTTP 200 응답을 반환합니다. 그렇지 않은 경우 HTTP 500 응답이 반환됩니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 수정할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트로 HTTP 요청이 들어오면, Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 디스패치합니다. 이벤트의 [리스너](/docs/{{version}}/events) 내에서 데이터베이스나 캐시 등의 상태를 추가로 확인할 수 있습니다. 만약 애플리케이션에 문제가 감지되면, 리스너에서 예외를 던져 헬스 체크 실패를 알릴 수 있습니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 이용한 배포

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel에 최적화된 완전 관리형, 오토스케일링 배포 플랫폼이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보세요. Laravel Cloud는 컴퓨트, 데이터베이스, 캐시, 오브젝트 스토리지까지 관리해주는 강력한 배포 플랫폼입니다.

Cloud에서 Laravel 애플리케이션을 배포하면 확장성과 간편함에 만족할 것입니다. Laravel Cloud는 프레임워크 제작자들이 최적화한 플랫폼으로, 익숙하게 개발하던 방식 그대로 Laravel을 작성할 수 있습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버를 관리하고 싶지만, robust한 Laravel 애플리케이션에 필요한 다양한 서비스를 직접 구성하기 어렵다면, [Laravel Forge](https://forge.laravel.com)가 있습니다. Forge는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에 서버를 만들 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 robust한 Laravel 애플리케이션에 필요한 모든 도구의 설치와 관리를 지원합니다.