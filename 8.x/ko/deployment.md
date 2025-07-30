# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구 사항](#server-requirements)
- [서버 구성](#server-configuration)
    - [Nginx](#nginx)
- [최적화](#optimization)
    - [자동로더 최적화](#autoloader-optimization)
    - [구성 로딩 최적화](#optimizing-configuration-loading)
    - [라우트 로딩 최적화](#optimizing-route-loading)
    - [뷰 로딩 최적화](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [Forge / Vapor로 배포하기](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었을 때, 애플리케이션이 가능한 효율적으로 동작하도록 하기 위해 할 수 있는 중요한 작업들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하는 데 도움이 되는 기본적인 시작점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크는 몇 가지 시스템 요구 사항을 갖고 있습니다. 웹 서버가 다음 최소 PHP 버전과 확장 기능을 갖추고 있는지 확인해야 합니다:

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
## 서버 구성

<a name="nginx"></a>
### Nginx

애플리케이션을 Nginx가 실행되는 서버에 배포하는 경우, 아래 예시 구성 파일을 웹 서버 설정의 시작점으로 사용할 수 있습니다. 대부분의 경우 서버 구성에 따라 이 파일은 맞춤화가 필요합니다. **서버 관리를 지원받고 싶다면, [Laravel Forge](https://forge.laravel.com)와 같은 Laravel 공식 서버 관리 및 배포 서비스를 고려하시기 바랍니다.**

아래 구성처럼 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 설정했는지 반드시 확인하세요. `index.php` 파일을 프로젝트 루트로 옮기려 하면 안 됩니다. 프로젝트 루트에서 애플리케이션을 제공하면 여러 민감한 구성 파일이 외부에 노출될 위험이 있습니다:

```
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
```

<a name="optimization"></a>
## 최적화

<a name="autoloader-optimization"></a>
### 자동로더 최적화

프로덕션에 배포할 때는 Composer의 클래스 자동로더 맵을 최적화하여, Composer가 클래스에 해당하는 파일을 빠르게 찾을 수 있도록 해야 합니다:

```
composer install --optimize-autoloader --no-dev
```

> [!TIP]
> 자동로더 최적화 외에도, 항상 `composer.lock` 파일을 프로젝트 소스 관리 저장소에 포함하세요. `composer.lock` 파일이 있으면 프로젝트 의존성을 훨씬 빠르게 설치할 수 있습니다.

<a name="optimizing-configuration-loading"></a>
### 구성 로딩 최적화

프로덕션에 애플리케이션을 배포할 때는 배포 과정에서 `config:cache` Artisan 명령어를 반드시 실행해야 합니다:

```
php artisan config:cache
```

이 명령어는 라라벨의 모든 구성 파일을 하나의 캐시된 파일로 합쳐서, 프레임워크가 구성 값을 로딩할 때 파일시스템 접근 횟수를 크게 줄여줍니다.

> [!NOTE]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, 반드시 구성 파일 내에서만 `env` 함수를 호출해야 합니다. 구성 캐시가 생성되면 `.env` 파일은 더 이상 로드되지 않으며, `.env` 변수에 대한 모든 `env` 함수 호출은 `null`을 반환합니다.

<a name="optimizing-route-loading"></a>
### 라우트 로딩 최적화

라우트가 많은 대규모 애플리케이션을 개발하는 경우, 배포 과정에서 `route:cache` Artisan 명령어를 실행하는 것이 좋습니다:

```
php artisan route:cache
```

이 명령어는 모든 라우트 등록을 캐시된 파일 내 하나의 메서드 호출로 축소하며, 수백 개 라우트 등록 시 라우트 등록 성능을 향상합니다.

<a name="optimizing-view-loading"></a>
### 뷰 로딩 최적화

프로덕션 배포 시 배포 과정에서 `view:cache` Artisan 명령어를 실행하는 것이 좋습니다:

```
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여 요청 시 동적으로 컴파일하지 않도록 하여, 뷰 반환 성능을 향상합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 구성 파일의 디버그 옵션은 오류에 대한 상세 정보가 사용자에게 어떻게 표시될지를 결정합니다. 기본값은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

**프로덕션 환경에서는 이 값을 항상 `false`로 설정해야 합니다. `APP_DEBUG` 변수가 프로덕션에서 `true`로 설정되면 애플리케이션의 민감한 구성 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor로 배포하기

<a name="laravel-forge"></a>
#### Laravel Forge

서버 구성을 직접 관리할 준비가 되지 않았거나, 강력한 Laravel 애플리케이션을 운영하는 데 필요한 다양한 서비스를 직접 구성하는 것이 어렵다면, [Laravel Forge](https://forge.laravel.com)는 훌륭한 대안입니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 여러 인프라 제공자 위에 서버를 생성할 수 있습니다. 또한 Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션 구축에 필요한 모든 도구들을 설치하고 관리합니다.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전한 서버리스(serverless) 자동 확장 배포 플랫폼이 필요하다면, [Laravel Vapor](https://vapor.laravel.com)를 확인해 보세요. Laravel Vapor는 AWS를 기반으로 하는 Laravel 전용 서버리스 배포 플랫폼입니다. Vapor 위에 Laravel 인프라를 구축하고 서버리스의 확장성과 단순함에 빠져보세요. Laravel Vapor는 Laravel 제작자들이 프레임워크와 완벽하게 호환되도록 세심하게 조정했기 때문에, 기존과 동일한 방식으로 Laravel 애플리케이션을 계속 작성할 수 있습니다.