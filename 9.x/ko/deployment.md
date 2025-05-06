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
- [Forge / Vapor를 통한 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면, 애플리케이션이 최대한 효율적으로 동작하도록 할 수 있는 중요한 사항들이 있습니다. 이 문서에서는 Laravel 애플리케이션이 올바르게 배포되었는지 확인하기 위한 기본적인 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버가 다음의 최소 PHP 버전 및 확장 모듈을 갖추고 있는지 확인해야 합니다.

<div class="content-list" markdown="1">

- PHP >= 8.0
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

애플리케이션을 Nginx가 실행 중인 서버에 배포하는 경우, 다음의 예시 설정 파일을 참고하여 웹 서버를 구성할 수 있습니다. 대부분의 경우, 이 파일은 서버 환경에 맞게 커스터마이즈가 필요합니다. **서버 관리를 위한 지원이 필요하다면, [Laravel Forge](https://forge.laravel.com) 같은 공식 Laravel 서버 관리 및 배포 서비스를 이용하는 것도 고려해보세요.**

아래 설정처럼, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 옮기려 하지 마세요. 프로젝트 루트에서 애플리케이션을 서비스하면 많은 민감한 설정 파일이 외부에 노출될 수 있습니다.

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

프로덕션 환경에 배포할 때는 Composer의 클래스 오토로더 맵을 최적화해야 하며, 이를 통해 Composer가 클래스를 더 빠르게 로드할 수 있습니다.

```shell
composer install --optimize-autoloader --no-dev
```

> **참고**  
> 오토로더 최적화 외에도, 반드시 `composer.lock` 파일을 프로젝트의 소스 제어 저장소에 포함해야 합니다. `composer.lock` 파일이 있을 때 의존성 설치가 훨씬 빨라집니다.

<a name="optimizing-configuration-loading"></a>
### 설정 로딩 최적화

애플리케이션을 프로덕션 환경에 배포할 때는 배포 과정에서 반드시 `config:cache` 아티즌 명령어를 실행해야 합니다.

```shell
php artisan config:cache
```

이 명령은 Laravel의 모든 설정 파일을 하나의 캐시 파일로 결합하여, 설정 값을 불러올 때 파일 시스템 접근 횟수를 크게 줄여줍니다.

> **경고**  
> 배포 과정에서 `config:cache` 명령을 실행했다면, 반드시 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐시된 이후에는 `.env` 파일이 로드되지 않으며, `.env` 변수를 위한 `env` 함수 호출은 `null`을 반환하게 됩니다.

<a name="optimizing-route-loading"></a>
### 라우트 로딩 최적화

많은 라우트를 가진 대규모 애플리케이션이라면, 배포 과정에서 `route:cache` 아티즌 명령어를 실행해야 합니다.

```shell
php artisan route:cache
```

이 명령은 모든 라우트 등록을 하나의 메소드 호출로 캐시 파일에 축약하여, 수백 개의 라우트를 등록할 때도 라우트 등록 성능을 높여줍니다.

<a name="optimizing-view-loading"></a>
### 뷰 로딩 최적화

애플리케이션을 프로덕션에 배포할 때, 배포 과정에서 꼭 `view:cache` 아티즌 명령어를 실행해야 합니다.

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여, 뷰 반환 시마다 뷰가 즉시 출력될 수 있도록 성능을 개선합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 debug 옵션은 사용자에게 얼마나 많은 오류 정보를 노출할지 결정합니다. 기본적으로 이 옵션은 애플리케이션 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

**프로덕션 환경에서는 이 값이 항상 `false`로 설정되어야 합니다. 만약 프로덕션에서 `APP_DEBUG` 변수가 `true`로 되어 있다면, 민감한 설정 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor를 통한 배포

<a name="laravel-forge"></a>
#### Laravel Forge

서버 설정을 직접 관리할 준비가 되어 있지 않거나, 다양한 서비스를 직접 설정하는 게 부담스럽다면 [Laravel Forge](https://forge.laravel.com)가 훌륭한 대안이 될 수 있습니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에서 서버를 생성할 수 있습니다. 또한, Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구를 설치 및 관리해 줍니다.

> **참고**  
> Laravel Forge를 통한 배포에 대한 전체 가이드가 필요하다면 [Laravel Bootcamp](https://bootcamp.laravel.com/deploying) 및 Laracasts의 Forge [비디오 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고해 보세요.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전히 서버리스이며, Laravel에 최적화된 자동 확장 플랫폼을 원한다면 [Laravel Vapor](https://vapor.laravel.com)를 확인해보세요. Laravel Vapor는 AWS 기반의 Laravel을 위한 서버리스 배포 플랫폼입니다. Vapor에서 Laravel 인프라를 시작하면 서버리스의 확장성과 단순함을 경험할 수 있습니다. Laravel Vapor는 프레임워크와 완벽하게 연동되도록 Laravel 제작진이 직접 조율했으므로, 익숙한 방식대로 Laravel 애플리케이션을 작성할 수 있습니다.