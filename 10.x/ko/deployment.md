# 배포

- [소개](#introduction)
- [서버 요구 사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
- [최적화](#optimization)
    - [오토로더 최적화](#autoloader-optimization)
    - [설정 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [Forge / Vapor를 통한 간편 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 실행되도록 할 수 있는 몇 가지 중요한 사항이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 훌륭한 시작점을 안내합니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버가 다음의 최소 PHP 버전과 확장 기능을 가지고 있는지 확인해야 합니다.

<div class="content-list" markdown="1">

- PHP >= 8.1
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

Nginx가 설치된 서버에 애플리케이션을 배포하는 경우, 다음 설정 파일을 참고하여 웹 서버를 설정할 수 있습니다. 대부분의 경우, 이 파일은 서버 환경에 따라 커스터마이즈 해야 합니다. **서버 관리를 위한 지원이 필요하다면, [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 서버 관리 및 배포 서비스를 고려해보세요.**

아래 설정과 같이, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 해야 합니다. `index.php` 파일을 프로젝트 루트로 옮기지 마십시오. 프로젝트 루트에서 애플리케이션을 서비스할 경우, 여러 민감한 설정 파일이 외부에 노출될 수 있습니다.

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
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
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

프로덕션 환경에 배포할 때는 Composer의 클래스 오토로더 맵을 최적화하여, Composer가 클래스에 맞는 파일을 더욱 빠르게 찾을 수 있도록 해야 합니다.

```shell
composer install --optimize-autoloader --no-dev
```

> [!NOTE]  
> 오토로더 최적화 외에도, 프로젝트의 소스 컨트롤 저장소에 `composer.lock` 파일을 반드시 포함해야 합니다. `composer.lock` 파일이 있으면 프로젝트의 의존성을 훨씬 더 빠르게 설치할 수 있습니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

애플리케이션을 프로덕션 환경에 배포할 때는, 배포 과정 중 반드시 `config:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan config:cache
```

이 명령은 모든 Laravel 설정 파일을 하나의 캐시된 파일로 결합하여, 프레임워크가 설정 값을 로드할 때 파일 시스템에 접근하는 횟수를 대폭 줄여줍니다.

> [!WARNING]  
> 배포 과정에서 `config:cache` 명령을 실행했다면, 설정 파일 내에서만 `env` 함수를 사용하도록 해야 합니다. 설정이 캐시되면 `.env` 파일이 로드되지 않으므로, 설정 파일 이외에서 `env` 함수를 호출하면 `null`이 반환됩니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션에서 [이벤트 자동 탐색](/docs/{{version}}/events#event-discovery)을 사용한다면, 배포 과정에서 이벤트-리스너 매핑을 캐싱해야 합니다. 이를 위해 배포 시 `event:cache` Artisan 명령어를 실행하세요.

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

많은 라우트를 가진 대규모 애플리케이션을 개발하는 경우, 배포 과정에서 `route:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan route:cache
```

이 명령은 모든 라우트 등록 정보를 하나의 메서드 호출로 캐시된 파일에 저장하여, 수백 개의 라우트를 등록할 때 라우트 등록 성능을 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

애플리케이션을 프로덕션 환경에 배포할 때, 배포 과정에서 `view:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan view:cache
```

이 명령은 모든 Blade 뷰를 미리 컴파일하여, 요청 시마다 뷰를 컴파일하지 않아도 되어 뷰를 반환하는 각 요청의 성능이 향상됩니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 오류에 대한 정보를 사용자가 얼마나 볼 수 있는지 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

> [!WARNING]  
> **프로덕션 환경에서는 이 값이 항상 `false`여야 합니다. 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되어 있으면, 민감한 설정 정보가 최종 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor를 통한 간편 배포

<a name="laravel-forge"></a>
#### Laravel Forge

서버 설정을 직접 관리하는 것이 어렵거나, Laravel 애플리케이션을 운영하기 위한 다양한 서비스를 직접 설정하는 것이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)가 훌륭한 대안이 될 수 있습니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에 서버를 생성할 수 있습니다. 또한, Nginx, MySQL, Redis, Memcached, Beanstalk 등 안정적인 Laravel 애플리케이션 개발에 필요한 도구들을 설치 및 관리해 줍니다.

> [!NOTE]  
> Laravel Forge를 활용한 전체 배포 가이드가 필요하다면 [Laravel Bootcamp](https://bootcamp.laravel.com/deploying)와 Laracasts의 Forge [영상 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고해보세요.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전한 서버리스 환경에서 자동으로 확장되는 Laravel 전용 배포 플랫폼이 필요하다면 [Laravel Vapor](https://vapor.laravel.com)를 살펴보세요. Laravel Vapor는 AWS 기반의 서버리스 배포 플랫폼으로, Laravel 인프라를 손쉽게 구축할 수 있으며 확장성과 단순함을 겸비하고 있습니다. Laravel Vapor는 Laravel 제작진이 프레임워크와 완벽하게 동작하도록 맞춤 최적화되어 있어, 익숙한 방식 그대로 개발을 이어갈 수 있습니다.