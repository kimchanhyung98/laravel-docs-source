# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
- [최적화](#optimization)
    - [오토로더 최적화](#autoloader-optimization)
    - [설정 로딩 최적화](#optimizing-configuration-loading)
    - [라우트 로딩 최적화](#optimizing-route-loading)
    - [뷰 로딩 최적화](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [Forge / Vapor를 이용한 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 작동할 수 있도록 몇 가지 중요한 작업을 수행할 수 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 좋은 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버의 PHP 버전과 확장들이 아래 최소 요구사항을 충족하는지 확인해야 합니다:

<div class="content-list" markdown="1">

- PHP 버전 8.0 이상
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

Nginx를 실행하는 서버에 애플리케이션을 배포하는 경우, 아래 예시 설정 파일을 웹 서버 설정의 출발점으로 사용할 수 있습니다. 대부분의 경우 서버 구성에 따라 이 파일을 맞춤 설정해야 합니다. **서버 관리에 도움이 필요하다면, [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 서버 관리 및 배포 서비스를 고려해보세요.**

아래 설정처럼 웹 서버가 모든 요청을 `public/index.php` 파일로 전달하도록 반드시 구성해야 합니다. `index.php` 파일을 프로젝트 루트로 이동하려 시도해서는 안 됩니다. 프로젝트 루트에서 애플리케이션을 서빙할 경우 중요한 설정 파일들이 웹에 노출될 위험이 있습니다.

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

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="optimization"></a>
## 최적화

<a name="autoloader-optimization"></a>
### 오토로더 최적화

프로덕션 환경에 배포할 때는 Composer의 클래스 오토로더 맵을 최적화하여 Composer가 주어진 클래스를 빠르게 찾을 수 있도록 해야 합니다:

```shell
composer install --optimize-autoloader --no-dev
```

> [!NOTE]
> 오토로더 최적화 외에도, 항상 `composer.lock` 파일을 프로젝트 소스 관리 저장소에 포함하는 것이 좋습니다. `composer.lock` 파일이 있으면 프로젝트의 의존성을 훨씬 빠르게 설치할 수 있습니다.

<a name="optimizing-configuration-loading"></a>
### 설정 로딩 최적화

프로덕션에 애플리케이션을 배포할 때는 배포 과정 중에 `config:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시 파일로 결합하여, 설정 값을 불러올 때 프레임워크가 파일시스템에 접근하는 횟수를 크게 줄여줍니다.

> [!WARNING]
> `config:cache` 명령어를 실행하면, 설정 파일 내에서 `env` 함수를 호출할 때 반드시 주의해야 합니다. 설정이 캐시되면 `.env` 파일이 로드되지 않으므로 `.env` 변수에 대한 모든 `env` 함수 호출은 `null`을 반환합니다.

<a name="optimizing-route-loading"></a>
### 라우트 로딩 최적화

라우트가 많은 큰 애플리케이션을 개발하는 경우, 배포 과정 중에 `route:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령어는 모든 라우트 등록 정보를 하나의 메서드 호출로 줄인 캐시 파일로 만들어 수백 개의 라우트를 등록할 때 라우트 등록 성능을 개선합니다.

<a name="optimizing-view-loading"></a>
### 뷰 로딩 최적화

프로덕션 배포 시, `view:cache` Artisan 명령어를 실행하여 애플리케이션의 Blade 뷰를 미리 컴파일해야 합니다:

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일해서, 요청 시 뷰가 즉시 렌더링되도록 하여 성능을 향상시킵니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 에러에 관한 정보를 사용자에게 얼마나 많이 보여줄지 결정합니다. 기본적으로 이 옵션은 애플리케이션 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

**프로덕션 환경에서는 이 값은 항상 `false`로 설정해야 합니다. 만약 프로덕션에서 `APP_DEBUG`가 `true`로 설정되어 있으면, 민감한 설정 값들이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor를 이용한 배포

<a name="laravel-forge"></a>
#### Laravel Forge

서버 설정을 직접 관리할 준비가 안 되었거나, Laravel 애플리케이션을 안정적으로 운영하는 데 필요한 다양한 서비스를 직접 구성하는 데 자신이 없다면, [Laravel Forge](https://forge.laravel.com)가 훌륭한 대안입니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공자에 서버를 생성할 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 Laravel 애플리케이션 구축 시 필요한 모든 도구를 설치하고 관리해 줍니다.

> [!NOTE]
> Laravel Forge를 이용한 배포의 전체 가이드를 원하면, [Laravel Bootcamp](https://bootcamp.laravel.com/deploying)와 Laracasts에서 제공하는 Forge [비디오 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고하세요.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전 서버리스(serverless) 방식의 자동 확장 배포 플랫폼을 원한다면, Laravel에 최적화된 [Laravel Vapor](https://vapor.laravel.com)를 확인해 보세요. Laravel Vapor는 AWS 기반의 서버리스 Laravel 배포 플랫폼입니다. Vapor를 통해 Laravel 인프라를 시작하면 서버 관리를 걱정하지 않고도 확장 가능한 간결한 환경을 누릴 수 있습니다. Laravel Vapor는 프레임워크를 만든 개발자들이 직접 조율하여, 익숙한 방식 그대로 Laravel 애플리케이션을 계속 개발할 수 있도록 최적화되어 있습니다.