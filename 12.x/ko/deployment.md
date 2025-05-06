# 배포

- [소개](#introduction)
- [서버 요구 사항](#server-requirements)
- [서버 구성](#server-configuration)
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
- [Laravel Cloud 또는 Forge를 이용한 배포](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 동작하도록 하기 위해 할 수 있는 중요한 작업들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 몇 가지 핵심 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버가 아래의 최소 PHP 버전과 확장 모듈을 갖추었는지 확인해야 합니다:

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
## 서버 구성

<a name="nginx"></a>
### Nginx

Nginx에서 애플리케이션을 배포하는 경우 아래의 구성 파일을 시작점으로 사용할 수 있습니다. 대부분의 경우 서버 환경에 맞게 이 파일을 커스터마이즈해야 합니다. **서버 관리를 지원받고 싶다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 Laravel 플랫폼을 고려해보세요.**

아래 예시와 같이, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 이동하려고 해서는 안 됩니다. 프로젝트 루트에서 애플리케이션을 서비스할 경우 민감한 설정 파일들이 외부에 노출될 수 있습니다.

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

[FrankenPHP](https://frankenphp.dev/)를 사용하여 Laravel 애플리케이션을 서비스할 수도 있습니다. FrankenPHP는 Go로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 통해 Laravel PHP 애플리케이션을 서비스하려면 다음과 같이 `php-server` 명령어를 실행하면 됩니다:

```shell
frankenphp php-server -r public/
```

FrankenPHP에서 [Laravel Octane](/docs/{{version}}/octane) 통합, HTTP/3, 최신 압축, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등, 더 강력한 기능을 활용하고 싶다면 FrankenPHP의 [Laravel 공식 문서](https://frankenphp.dev/docs/laravel/)를 참고하세요.

<a name="directory-permissions"></a>
### 디렉터리 권한

Laravel은 `bootstrap/cache`와 `storage` 디렉터리에 쓰기 작업을 수행해야 하므로, 웹 서버 프로세스 소유자가 이러한 디렉터리에 쓸 수 있는 권한이 있는지 반드시 확인하세요.

<a name="optimization"></a>
## 최적화

애플리케이션을 프로덕션에 배포할 때는 설정, 이벤트, 라우트, 뷰 등 다양한 파일을 캐시해야 합니다. Laravel은 이러한 모든 파일을 한 번에 캐시해주는 편리한 `optimize` Artisan 명령어를 제공합니다. 이 명령은 애플리케이션 배포 과정의 일부로 보통 실행됩니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령으로 생성된 모든 캐시 파일은 물론, 기본 캐시 드라이버의 모든 키도 삭제합니다:

```shell
php artisan optimize:clear
```

다음 문서에서는 `optimize` 명령어가 실행하는 각 개별 최적화 명령어에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

프로덕션 환경에 애플리케이션을 배포할 때에는 배포 과정 중에 반드시 `config:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시 파일로 통합하여, 설정 값을 로드하는 동안 프레임워크가 파일 시스템에 접근하는 횟수를 대폭 줄여줍니다.

> [!WARNING]
> 배포 과정 중에 `config:cache` 명령어를 실행하는 경우, 설정 파일 내부에서만 `env` 함수를 호출해야 합니다. 설정이 캐시되면 `.env` 파일이 로드되지 않으므로, `.env` 변수에 대해 `env` 함수를 호출하면 항상 `null`이 반환됩니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션의 자동 발견된 이벤트-리스너 매핑도 배포 과정에서 캐시해야 합니다. 이는 `event:cache` Artisan 명령을 실행함으로써 할 수 있습니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

규모가 크고 라우트가 많은 애플리케이션을 개발 중인 경우, 배포 과정에서 반드시 `route:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령은 모든 라우트 등록을 하나의 메서드 호출로 축소하여 캐시 파일에 저장하며, 수백 개의 라우트를 등록할 때 라우트 등록 성능을 높여줍니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션에 애플리케이션을 배포할 때에는 배포 과정에 `view:cache` Artisan 명령을 포함해야 합니다:

```shell
php artisan view:cache
```

이 명령은 모든 Blade 뷰를 미리 컴파일하여, 요청 시마다 뷰가 다시 컴파일되지 않아 각 뷰 반환 요청의 성능이 향상됩니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php`의 debug 옵션은 오류 발생 시 사용자에게 얼마나 많은 정보가 표시되는지 제어합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수의 값을 따릅니다.

> [!WARNING]
> **프로덕션 환경에서는 이 값이 항상 `false` 여야 합니다. 만약 `APP_DEBUG` 변수가 프로덕션에서 `true`로 설정되면, 민감한 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 헬스(Health) 라우트

Laravel에는 애플리케이션 상태를 모니터링할 수 있는 내장 헬스 체크(health check) 라우트가 포함되어 있습니다. 프로덕션 환경에서는 이 라우트를 통해 애플리케이션의 상태를 가동 모니터링 도구, 로드 밸런서 또는 Kubernetes와 같은 오케스트레이션 시스템에 보고할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up` 경로에 할당되어 있으며, 애플리케이션이 예외 없이 부팅되었을 경우 200 HTTP 응답을 반환합니다. 그렇지 않은 경우 500 HTTP 응답이 반환됩니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트로 HTTP 요청이 들어오면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 디스패치합니다. 이를 통해 애플리케이션에 맞는 추가적인 헬스 체크를 수행할 수 있습니다. [리스너](/docs/{{version}}/events)에서 데이터베이스나 캐시 상태 등을 점검하고, 문제가 발견되면 리스너에서 바로 예외를 던질 수 있습니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 이용한 배포

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel에 최적화된 완전 관리형 자동 확장 플랫폼을 원한다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해보세요. Laravel Cloud는 관리형 컴퓨트, 데이터베이스, 캐시, 오브젝트 스토리지를 제공하는 강력한 배포 플랫폼입니다.

Cloud에 Laravel 애플리케이션을 배포하고, 확장 가능한 단순함을 직접 경험해보세요. Laravel Cloud는 프레임워크와 완전히 통합되도록 Laravel의 제작진이 직접 튜닝했습니다. 따라서 익숙한 방식대로 개발에만 집중할 수 있습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버를 관리하는 방식을 선호하지만, 모든 서비스 구성에 익숙하지 않다면 [Laravel Forge](https://forge.laravel.com)가 좋은 선택입니다. Forge는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 공급자에 서버를 생성할 수 있도록 지원합니다. 또한, Nginx, MySQL, Redis, Memcached, Beanstalk 등, 견고한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구를 자동으로 설치·관리해줍니다.