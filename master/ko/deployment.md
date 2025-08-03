# 배포 (Deployment)

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
- [헬스 라우트](#the-health-route)
- [Laravel Cloud 또는 Forge를 통한 배포](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 작동하도록 할 수 있는 중요한 작업들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위해 고려해야 할 좋은 시작점들을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버가 다음 최소 PHP 버전과 확장 모듈을 갖추고 있는지 확인해야 합니다:

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

Nginx를 사용하는 서버에 애플리케이션을 배포할 경우, 웹 서버 구성을 위한 시작점으로 다음 설정 파일을 참고할 수 있습니다. 대부분의 경우 서버 환경에 맞게 이 파일을 수정해야 합니다. **서버 관리를 돕는 지원이 필요하면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 Laravel 플랫폼을 사용하는 것을 고려하세요.**

아래 설정처럼 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 꼭 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 옮기지 마세요. 프로젝트 루트에서 애플리케이션을 제공하면 민감한 설정 파일들이 외부에 노출될 위험이 있습니다.

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

[FrankenPHP](https://frankenphp.dev/)도 Laravel 애플리케이션을 서비스하는 데 사용될 수 있습니다. FrankenPHP는 Go 언어로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP로 Laravel 애플리케이션을 실행하려면 다음과 같이 `php-server` 명령어를 사용하면 됩니다:

```shell
frankenphp php-server -r public/
```

Laravel Octane과의 [통합](/docs/master/octane), HTTP/3, 최신 압축, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등 FrankenPHP가 지원하는 강력한 기능을 활용하려면, FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하세요.

<a name="directory-permissions"></a>
### 디렉토리 권한

Laravel은 `bootstrap/cache` 및 `storage` 디렉토리에 쓰기 작업을 수행해야 하므로, 웹 서버 프로세스 사용자에게 이 디렉토리들에 대한 쓰기 권한이 부여되어 있는지 확인해야 합니다.

<a name="optimization"></a>
## 최적화

프로덕션 환경에 애플리케이션을 배포할 때는 설정 파일, 이벤트, 라우트, 뷰 등 다양한 파일들을 캐싱해야 합니다. Laravel은 모든 캐싱 작업을 한 번에 처리하는 편리한 `optimize` Artisan 명령어를 제공합니다. 이 명령어는 일반적으로 배포 과정 중에 호출되어야 합니다:

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령어가 생성한 모든 캐시 파일과 기본 캐시 드라이버에 저장된 모든 키들을 삭제하는 데 사용할 수 있습니다:

```shell
php artisan optimize:clear
```

다음 문서에서는 `optimize` 명령어로 실행되는 각 세부 최적화 명령어들을 살펴보겠습니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

프로덕션에 배포할 때는 `config:cache` Artisan 명령어를 배포 과정 중에 반드시 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시 파일로 결합하여, 설정 값을 읽기 위해 프레임워크가 파일 시스템에 접근하는 횟수를 크게 줄여줍니다.

> [!WARNING]
> `config:cache` 명령어를 실행할 경우, 설정 파일 내에서 `env` 함수를 직접 호출하는 부분이 거의 없어야 합니다. 캐시가 한번 만들어지면 `.env` 파일은 로드되지 않고, `.env` 변수에 대한 `env` 함수 호출은 항상 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션에서 자동 탐색된 이벤트 - 리스너 매핑을 배포 과정에서 캐싱해야 합니다. 이는 `event:cache` Artisan 명령어를 실행하여 수행할 수 있습니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

많은 라우트를 가진 대규모 애플리케이션의 경우, 배포 과정에서 반드시 `route:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령어는 라우트 등록들을 하나의 캐시 파일 내 단일 메소드 호출로 압축해, 수백 개 라우트 등록 시 성능을 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션에 배포할 때는 `view:cache` Artisan 명령어를 실행하여 모든 Blade 뷰를 미리 컴파일해야 합니다:

```shell
php artisan view:cache
```

이 명령어는 요청 시 뷰가 필요할 때마다 컴파일하는 일을 줄여서 뷰 렌더링 성능을 개선합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일 내의 debug 옵션은 사용자에게 오류 정보를 얼마나 상세히 보여줄지 결정합니다. 기본적으로 이 옵션은 애플리케이션 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 프로덕션 환경에서는 이 값을 항상 `false`로 설정해야 합니다. `APP_DEBUG` 변수가 프로덕션에서 `true`로 설정되어 있으면, 민감한 설정 값이 최종 사용자에게 노출될 위험이 있습니다.

<a name="the-health-route"></a>
## 헬스 라우트

Laravel은 애플리케이션 상태를 모니터링하는데 사용할 수 있는 내장 헬스 체크 라우트를 제공합니다. 프로덕션에서 이 라우트는 uptime 모니터, 로드 밸런서, Kubernetes 같은 오케스트레이션 시스템에 애플리케이션 상태를 보고하는 데 활용할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up` 경로에서 서비스되며, 애플리케이션이 예외 없이 정상 부팅되면 200 HTTP 응답 코드를 반환합니다. 문제가 있으면 500 HTTP 응답 코드를 반환합니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 다음과 같이 설정할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트로 HTTP 요청이 들어오면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트를 발송해 추가적인 앱 상태 점검을 할 수 있게 합니다. 이 이벤트의 [리스너](/docs/master/events) 내에서 데이터베이스나 캐시 상태를 점검할 수 있으며, 문제가 발견되면 리스너에서 예외를 던져 상태를 알릴 수 있습니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 통한 배포

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel에 최적화된 완전 관리형 자동 확장 배포 플랫폼을 원한다면, [Laravel Cloud](https://cloud.laravel.com)를 확인해보세요. Laravel Cloud는 매니지드 컴퓨트, 데이터베이스, 캐시, 객체 스토리지를 제공하는 강력한 Laravel 배포 플랫폼입니다.

Laravel Cloud에서 애플리케이션을 실행하면 확장 가능한 간편함에 반하게 될 것입니다. Laravel 개발자들이 직접 최적화한 플랫폼으로, 기존에 익숙한 방식대로 Laravel 애플리케이션을 계속 작성할 수 있습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

서버 관리는 직접 하되, Laravel 애플리케이션을 제대로 운영하기 위한 여러 컴포넌트 설정이 부담스럽다면 [Laravel Forge](https://forge.laravel.com)를 이용할 수 있습니다. Forge는 Laravel 애플리케이션용 VPS 서버 관리 플랫폼입니다.

Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공자에서 서버를 생성할 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 견고한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구를 설치 및 관리합니다.