# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 구성](#server-configuration)
    - [Nginx](#nginx)
- [최적화](#optimization)
    - [오토로더 최적화](#autoloader-optimization)
    - [구성 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [디버그 모드](#debug-mode)
- [Forge / Vapor로 손쉬운 배포](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었을 때, 애플리케이션이 최대한 효율적으로 실행되도록 할 수 있는 몇 가지 중요한 작업들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 좋은 출발점들을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버가 아래 최소 PHP 버전과 확장 모듈을 갖추었는지 확인해야 합니다:

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
## 서버 구성

<a name="nginx"></a>
### Nginx

만약 Nginx를 구동하는 서버에 애플리케이션을 배포한다면, 아래의 구성 파일을 웹 서버 설정의 시작점으로 사용할 수 있습니다. 대부분의 경우 서버 환경에 맞게 이 파일을 커스터마이징해야 할 것입니다. **서버 관리를 지원받고 싶다면, Laravel의 공식 서버 관리 및 배포 서비스인 [Laravel Forge](https://forge.laravel.com)를 사용하는 것을 고려하세요.**

아래 구성과 같이 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 설정해야 합니다. 절대 `index.php` 파일을 프로젝트 루트로 옮기려 하지 마세요. 그렇게 하면 프로젝트 루트에 있는 민감한 설정 파일들이 외부에 노출될 위험이 있습니다:

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

프로덕션에 배포할 때에는 Composer의 클래스 오토로더 맵을 최적화하여, Composer가 특정 클래스를 로드할 적절한 파일을 빠르게 찾을 수 있도록 해야 합니다:

```shell
composer install --optimize-autoloader --no-dev
```

> [!NOTE]  
> 오토로더 최적화 외에도, 항상 `composer.lock` 파일을 프로젝트 소스 코드 저장소에 포함하는 것이 중요합니다. `composer.lock` 파일이 있을 경우 프로젝트 의존성 설치 속도가 훨씬 빨라집니다.

<a name="optimizing-configuration-loading"></a>
### 구성 캐싱

프로덕션 배포 시 배포 과정에서 반드시 `config:cache` Artisan 명령어를 실행해야 합니다:

```shell
php artisan config:cache
```

이 명령어는 Laravel의 모든 구성 파일을 하나의 캐싱된 파일로 합쳐, 프레임워크가 구성 값을 불러올 때 파일 시스템 접근 횟수를 크게 줄여줍니다.

> [!WARNING]  
> `config:cache` 명령을 실행할 때는 구성 파일 내에서 `env` 함수만 호출하도록 주의해야 합니다. 구성이 캐싱되면 `.env` 파일이 더 이상 로드되지 않으며, `env` 함수로 접근하는 `.env` 변수들은 모두 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션에서 [이벤트 디스커버리(event discovery)](/docs/10.x/events#event-discovery)를 사용한다면, 배포 과정 시 애플리케이션의 이벤트-리스너 매핑 캐시를 생성해야 합니다. `event:cache` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

라우트가 많은 대규모 애플리케이션을 개발하는 경우, 배포 과정에서 `route:cache` Artisan 명령어를 꼭 실행해야 합니다:

```shell
php artisan route:cache
```

이 명령어는 모든 라우트 등록을 하나의 캐싱된 파일 내 단일 메서드 호출로 줄여, 수백 개의 라우트 등록 시 성능을 크게 향상합니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션에 배포할 때, 배포 과정에서 `view:cache` Artisan 명령어를 꼭 실행하세요:

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여 요청 시마다 컴파일하지 않게 함으로써, 뷰 반환 시 성능을 개선합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 구성 파일 내의 debug 옵션은 사용자에게 실제로 얼마나 많은 오류 정보를 노출할지 결정합니다. 기본적으로 이 옵션은 애플리케이션 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> **프로덕션 환경에서는 해당 값이 항상 `false`로 설정되어야 합니다. 만약 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되면, 민감한 구성 값이 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor로 손쉬운 배포

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버를 관리할 준비가 되어 있지 않거나, 강력한 Laravel 애플리케이션을 운영하는 데 필요한 다양한 서비스를 직접 설정하는 게 부담스럽다면, [Laravel Forge](https://forge.laravel.com)가 훌륭한 대안이 될 수 있습니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공자에 서버를 생성할 수 있고, Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션 구축에 필요한 도구들을 설치·관리합니다.

> [!NOTE]  
> Laravel Forge로 배포하는 완전한 가이드가 필요하다면 [Laravel Bootcamp](https://bootcamp.laravel.com/deploying)와 Forge 관련 [Laracasts 동영상 시리즈](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고하세요.

<a name="laravel-vapor"></a>
#### Laravel Vapor

완전히 서버리스(serverless)이며 자동 확장되는 Laravel용 배포 플랫폼을 원한다면, [Laravel Vapor](https://vapor.laravel.com)를 확인해보세요. Laravel Vapor는 AWS를 기반으로 한 서버리스 Laravel 배포 플랫폼입니다. Vapor를 통해 Laravel 인프라를 런칭하고, 서버리스의 확장성과 단순함에 빠져보세요. Laravel 팀이 프레임워크와 완벽하게 연동되도록 세심하게 튜닝한 Vapor 덕분에, 익숙한 방식으로 계속해서 Laravel 애플리케이션을 개발할 수 있습니다.