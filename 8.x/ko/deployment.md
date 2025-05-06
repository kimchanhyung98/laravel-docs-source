# 배포

- [소개](#introduction)
- [서버 요구 사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
- [최적화](#optimization)
    - [오토로더 최적화](#autoloader-optimization)
    - [설정 로딩 최적화](#optimizing-configuration-loading)
    - [라우트 로딩 최적화](#optimizing-route-loading)
    - [뷰 로딩 최적화](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [Forge 또는 Vapor로 배포하기](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 동작하도록 할 수 있는 몇 가지 중요한 사항이 있습니다. 이 문서에서는 Laravel 애플리케이션이 올바르게 배포되었는지 확인할 수 있는 좋은 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버에 다음 최소 PHP 버전 및 확장 기능이 설치되어 있는지 확인해야 합니다:

<div class="content-list" markdown="1">

- PHP >= 7.3
- BCMath PHP 확장
- Ctype PHP 확장
- Fileinfo PHP 확장
- JSON PHP 확장
- Mbstring PHP 확장
- OpenSSL PHP 확장
- PDO PHP 확장
- Tokenizer PHP 확장
- XML PHP 확장

</div>

<a name="server-configuration"></a>
## 서버 설정

<a name="nginx"></a>
### Nginx

Nginx가 실행 중인 서버에 애플리케이션을 배포하는 경우, 다음의 설정 파일을 참고하여 웹 서버를 구성할 수 있습니다. 대부분의 경우, 이 파일은 서버의 환경에 맞게 커스텀해야 합니다. **서버 관리가 필요하다면, [Laravel Forge](https://forge.laravel.com)와 같은 Laravel의 공식 서버 관리 및 배포 서비스를 사용하는 것도 고려해 볼 수 있습니다.**

아래 설정처럼, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 구성되어 있는지 확인하세요. 절대 `index.php` 파일을 프로젝트 루트로 옮겨서 애플리케이션을 서비스하면 안 됩니다. 프로젝트 루트에서 애플리케이션을 서비스하면, 많은 중요한 설정 파일들이 외부에 노출될 수 있습니다.

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
            fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
            include fastcgi_params;
        }

        location ~ /\.(?!well-known).* {
            deny all;
        }
    }

<a name="optimization"></a>
## 최적화

<a name="autoloader-optimization"></a>
### 오토로더 최적화

프로덕션 환경에 배포할 때는 Composer의 클래스 오토로더 맵을 최적화하여, Composer가 클래스에 맞는 파일을 더 빠르게 찾을 수 있도록 해야 합니다:

    composer install --optimize-autoloader --no-dev

> {tip} 오토로더 최적화 외에도, `composer.lock` 파일을 프로젝트의 소스 제어 저장소에 반드시 포함해야 합니다. `composer.lock` 파일이 있으면 프로젝트의 종속성을 훨씬 더 빠르게 설치할 수 있습니다.

<a name="optimizing-configuration-loading"></a>
### 설정 로딩 최적화

애플리케이션을 프로덕션에 배포할 때는, 배포 과정에서 반드시 `config:cache` Artisan 명령어를 실행해야 합니다:

    php artisan config:cache

이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시 파일로 통합하여, 설정 값을 불러올 때 프레임워크가 파일 시스템을 참조하는 횟수를 대폭 줄여줍니다.

> {note} 배포 과정에서 `config:cache` 명령어를 실행하면, 설정 파일 내에서만 `env` 함수를 호출하도록 해야 합니다. 설정이 캐시된 이후에는 `.env` 파일이 로드되지 않으며, `.env` 변수를 위한 `env` 함수 호출은 모두 `null`을 반환합니다.

<a name="optimizing-route-loading"></a>
### 라우트 로딩 최적화

라우트가 많은 대형 애플리케이션을 개발 중이라면, 배포 과정에서 반드시 `route:cache` Artisan 명령을 실행해야 합니다:

    php artisan route:cache

이 명령어는 모든 라우트 등록을 하나의 캐시 파일 내의 단일 메서드 호출로 줄여, 수백 개의 라우트를 등록할 때의 성능을 향상시켜 줍니다.

<a name="optimizing-view-loading"></a>
### 뷰 로딩 최적화

애플리케이션을 프로덕션에 배포할 때는, 배포 과정에서 반드시 `view:cache` Artisan 명령어를 실행해야 합니다:

    php artisan view:cache

이 명령어는 Blade 뷰 전체를 미리 컴파일하여, 각각의 요청 시 뷰가 필요할 때마다 컴파일하지 않도록 하여 성능을 개선합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 에러에 대한 정보가 사용자에게 얼마나 표시되는지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장되어 있는 APP_DEBUG 환경 변수 값을 따릅니다.

**프로덕션 환경에서는 이 값이 항상 `false`가 되어야 합니다. 만약 프로덕션 환경에서 `APP_DEBUG` 변수가 `true`로 설정되어 있다면, 애플리케이션의 최종 사용자에게 중요한 설정 값들이 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge 또는 Vapor로 배포하기

<a name="laravel-forge"></a>
#### Laravel Forge

서버 설정을 직접 관리할 준비가 되어 있지 않거나, 강력한 Laravel 애플리케이션을 운영하는 데 필요한 다양한 서비스를 직접 설정하는 것이 어렵다면 [Laravel Forge](https://forge.laravel.com)를 훌륭한 대안으로 사용할 수 있습니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에서 서버를 생성할 수 있습니다. 또한, Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등 robust한 Laravel 애플리케이션 구축에 필요한 모든 도구를 설치하고 관리해줍니다.

<a name="laravel-vapor"></a>
#### Laravel Vapor

서버리스와 오토스케일링이 적용된 Laravel 전용 배포 플랫폼이 필요하다면 [Laravel Vapor](https://vapor.laravel.com)를 확인해 보세요. Laravel Vapor는 AWS 기반의 Laravel 서버리스 배포 플랫폼입니다. Vapor에서 Laravel 인프라를 실행하고, 서버리스의 확장 가능성과 간편함을 경험해 보세요. Vapor는 Laravel 제작진의 손길로 Laravel 프레임워크와 완벽하게 연동되도록 설계되어 있으므로, 지금까지 하던 대로 Laravel 애플리케이션을 작성할 수 있습니다.