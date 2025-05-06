# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [Shell 별칭(alias) 설정](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스 연동](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [파일 저장소](#file-storage)
- [테스트 실행](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [이메일 미리보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유](#sharing-your-site)
- [Xdebug로 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 경량 명령줄 인터페이스입니다. Sail은 PHP, MySQL, Redis를 사용하며, 기존에 Docker 경험이 없어도 바로 Laravel 애플리케이션 개발을 시작할 수 있는 좋은 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. 이 `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 상호작용할 수 있는 편리한 CLI 기능을 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용시)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에 Sail을 사용하려면 Composer 패키지 매니저를 통해 Sail을 설치하면 됩니다. 당연히 아래 과정은 로컬 개발 환경에 Composer 의존성 설치가 가능한 경우에 한합니다:

```shell
composer require laravel/sail --dev
```

Sail이 설치되면 `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml`을 애플리케이션 루트에 복사하고, Docker 서비스 연결에 필요한 환경 변수를 `.env` 파일에 추가합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법을 더 알아보려면 아래 문서를 계속 읽으세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용하는 경우, 다음 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치

기존 Sail 설치에 추가 서비스를 추가하려면, `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers)에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하면 됩니다. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 생성합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

이미지의 모든 패키지와 소프트웨어를 최신 상태로 완전히 재빌드하고 싶을 때가 있습니다. `build` 명령어로 이를 수행할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### Shell 별칭(alias) 설정

기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 실행됩니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 대신, 아래처럼 shell 별칭을 설정해서 더 쉽게 Sail 명령어를 사용할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용하려면, `~/.zshrc`나 `~/.bashrc` 같은 홈 디렉터리의 shell 환경설정 파일에 추가한 후 쉘을 재시작하세요.

별칭 설정 후에는 단순히 `sail`만 입력해서 명령어를 실행할 수 있습니다. 아래 문서의 모든 예제도 이 별칭이 설정되어 있다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 실행에 필요한 다양한 Docker 컨테이너가 정의되어 있습니다. 각 컨테이너는 `docker-compose.yml`의 `services` 항목에 등록되어 있습니다. `laravel.test` 컨테이너가 기본적으로 애플리케이션을 서비스하는 컨테이너입니다.

Sail을 실행하기 전에, 로컬 PC에서 실행 중인 웹 서버나 데이터베이스가 없는지 확인하세요. 애플리케이션의 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 실행하려면 `up` 명령어를 실행하세요:

```shell
sail up
```

백그라운드에서 컨테이너를 실행하려면 "detached" 모드로 실행할 수 있습니다:

```shell
sail up -d
```

애플리케이션 컨테이너가 실행되면, 웹 브라우저에서 http://localhost 로 접속할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C를 누르거나, 백그라운드에서 실행 중인 경우 `stop` 명령어를 사용하세요:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 동작하며 로컬 PC와는 격리됩니다. 하지만 Sail은 PHP, Artisan, Composer, Node/NPM 등 다양한 명령어를 편리하게 실행할 수 있도록 명령어 실행 방법을 제공합니다.

**Laravel 공식 문서를 보면 Sail이 아닌 Composer, Artisan, Node/NPM 명령어를 직접 실행하는 예시가 자주 나타납니다.** 이는 해당 도구가 로컬 PC에 설치되어 있을 때를 기준으로 합니다. Sail을 사용하고 있다면, 아래처럼 Sail을 통해 명령어를 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행...
php artisan queue:work

# Laravel Sail 컨테이너에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령어로 실행할 수 있습니다. 이 때 사용되는 PHP 버전은 여러분의 애플리케이션에 설정된 버전입니다. 사용 가능한 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer가 기본적으로 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 명령어는 `node`로, NPM 명령어는 `npm`으로 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스 연동

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 정의되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해, 컨테이너를 중지하거나 재시작해도 데이터가 유지됩니다.

MySQL 컨테이너가 처음 시작될 때, 개발용 데이터베이스(`DB_DATABASE` 환경 변수의 값을 이름으로 사용)와 테스트 전용 데이터베이스(`testing`)가 자동 생성됩니다.

컨테이너가 실행되면, `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 설정해 MySQL 인스턴스에 연결하세요.

로컬 PC에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 관리 툴을 사용할 수 있습니다. 기본적으로 `localhost` 3306 포트에 접근 가능하며, 접속 정보는 `DB_USERNAME`과 `DB_PASSWORD`를 사용합니다. 또는, `root` 사용자로도 접근 가능합니다(`root`의 비밀번호도 동일하게 환경 변수 값 사용).

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `docker-compose.yml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 추가됩니다. 이는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) 같은 Atlas 기능을 사용할 수 있으며, 마찬가지로 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용합니다.

컨테이너 실행 후, `.env` 파일의 `MONGODB_URI`를 `mongodb://mongodb:27017`로 설정해 MongoDB 인스턴스에 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있지만, `MONGODB_USERNAME` 및 `MONGODB_PASSWORD`를 설정해 인증을 활성화할 수도 있습니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 애플리케이션을 연동하려면, [MongoDB 공식 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치하세요.

로컬 PC에서 [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI 툴을 통해 `localhost` 27017 포트로 접속할 수 있습니다.

<a name="redis"></a>
### Redis

`docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 있습니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너 재시작 시에도 데이터가 유지됩니다. 애플리케이션 `.env` 파일의 `REDIS_HOST` 변수는 `redis`로  설정해야 합니다.

로컬 PC에서 [TablePlus](https://tableplus.com) 같은 GUI 툴을 사용해 `localhost` 6379 포트로 접근할 수도 있습니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `docker-compose.yml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다. `.env` 파일의 `REDIS_HOST` 변수를 `valkey`로 설정해 애플리케이션에서 Valkey에 연결할 수 있습니다.

로컬 PC에서 [TablePlus](https://tableplus.com) 등으로 `localhost` 6379 포트로 Valkey에 접속할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml`에 이 강력한 검색 엔진이 추가됩니다. [Laravel Scout](/docs/{{version}}/scout)와 연동됩니다. 컨테이너 실행 후, `.env` 파일의 `MEILISEARCH_HOST` 변수를 `http://meilisearch:7700`으로 설정하세요.

로컬 PC에서는 웹 브라우저로 `http://localhost:7700`에 접근해 Meilisearch 관리 페이지를 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml`에 초고속 오픈소스 검색 엔진이 포함됩니다. [Laravel Scout](/docs/{{version}}/scout#typesense)와 네이티브로 연동됩니다. 컨테이너 실행 후, 다음 환경 변수를 설정해 Typesense와 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 PC에서는 `http://localhost:8108`을 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 저장소

프로덕션 환경에서 Amazon S3에 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 추가하는 것을 권장합니다. MinIO는 S3 호환 API를 제공하므로, 프로덕션 S3에 "테스트" 버킷을 만들지 않고도 로컬에서 `s3` 파일 시스템 드라이버를 사용할 수 있습니다. MinIO를 설치하면 `docker-compose.yml`에 관련 설정이 자동 추가됩니다.

애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크가 정의되어 있습니다. Amazon S3 대신 MinIO와 같은 S3 호환 서비스를 사용한다면, 관련 환경 변수를 아래처럼 변경하세요:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO를 사용할 때 Flysystem이 올바른 URL을 생성하도록, `AWS_URL` 환경 변수도 설정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔(http://localhost:8900)에서 버킷을 만들 수 있습니다. 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행

Laravel은 뛰어난 내장 테스트 지원을 제공하며, Sail의 `test` 명령어로 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 지원하는 모든 CLI 옵션은 이 `test` 명령에도 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령은 `test` Artisan 명령과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 `testing` 데이터베이스를 별도로 생성해 테스트가 기존 데이터베이스 상태에 영향을 주지 않도록 합니다. Laravel 기본 설치에서는 Sail이 `phpunit.xml` 파일도 자동 설정합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 브라우저 자동화 테스트 API를 제공합니다. Sail 덕분에 로컬 PC에 Selenium 등을 별도 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 먼저, `docker-compose.yml`의 Selenium 서비스 주석을 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

그리고 `laravel.test` 서비스에 `selenium` 의존성을 추가하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작한 후, `dusk` 명령으로 Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium

로컬 PC에 Apple Silicon 칩이 있다면, `selenium/standalone-chromium` 이미지를 사용해야 합니다:

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 이메일 미리보기

Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 중 애플리케이션이 발송하는 이메일을 가로채고, 웹에서 쉽게 미리볼 수 있습니다. Sail 사용 시, Mailpit의 기본 호스트는 `mailpit`이고 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025 에서 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때때로 애플리케이션 컨테이너 내에서 Bash 세션을 시작할 수도 있습니다. `shell` 명령어로 컨테이너 안에 들어가 파일, 설치 서비스, 임의 셸 명령어를 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

또한 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령을 사용할 수 있습니다:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 PHP 8.4, 8.3, 8.2, 8.1, 8.0에서 애플리케이션을 서비스할 수 있습니다. 기본값은 PHP 8.4입니다. 사용 버전을 변경하려면 `docker-compose.yml`의 `laravel.test` 컨테이너의 `build` 값을 다음처럼 수정하세요:

```yaml
# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

또한, `image` 이름도 사용 중인 PHP 버전에 맞게 변경할 수 있습니다. 이 설정 역시 `docker-compose.yml`에 있습니다:

```yaml
image: sail-8.2/app
```

설정 변경 후에는 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 20을 설치합니다. 빌드 시 Node 버전을 변경하려면, `docker-compose.yml`의 `laravel.test` 서비스 내 `build.args`를 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

변경 후 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유

외부에서 사이트를 미리보기하거나, 동료와 공유하거나, 웹훅 연동 테스트를 위해 사이트를 공개해야 할 때가 있습니다. 이럴 때 `share` 명령을 사용하세요. 실행하면 임의의 `laravel-sail.site` URL이 발급되어 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령 사용 시, 반드시 `bootstrap/app.php`의 `trustProxies` 미들웨어에서 신뢰할 프록시를 설정하세요. 그렇지 않으면 URL 헬퍼(`url`, `route`)가 올바른 호스트를 판단하지 못할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 하위 도메인을 직접 지정하려면, `share` 명령에 `subdomain` 옵션을 추가하면 됩니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령은 [BeyondCode](https://beyondco.de)가 만든 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅

Sail의 Docker 구성은 [Xdebug](https://xdebug.org/)를 지원합니다. Xdebug를 활성화하려면 [Sail 설정을 퍼블리시](#sail-customization) 한 다음, 아래 환경 변수를 `.env` 파일에 추가하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

이어, `php.ini` 파일에 아래 설정이 있는지 확인하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 변경한 뒤에는 Docker 이미지를 다시 빌드해야 적용됩니다:

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 설정돼 있어서, Mac과 Windows(WSL2)에서 자동 설정됩니다. 만약 Linux를 사용하고, Docker 20.10 이상 버전이라면 추가 설정이 필요 없습니다.

Docker 20.10 미만 버전에서는 `host.docker.internal`이 지원되지 않으므로, 컨테이너에 고정 IP를 할당해야 합니다. 이를 위해 `docker-compose.yml`에 커스텀 네트워크를 정의하세요:

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

이후, `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 아래와 같이 지정합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용

`debug` 명령어를 사용해 Artisan 명령 실행 시 디버깅 세션을 시작할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug로 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, Xdebug 공식 문서의 [웹 애플리케이션 단계별 디버깅 가이드](https://xdebug.org/docs/step_debug#web-application)를 참고하세요.

PhpStorm을 사용한다면, [제로-설정 디버깅 가이드](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)를 참고하시기 바랍니다.

> [!WARNING]
> Laravel Sail은 `artisan serve`로 애플리케이션을 서비스합니다. `artisan serve`는 Laravel 8.53.0 이상에서만 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 구버전(8.52.0 이하)에서는 이 변수들이 적용되지 않아 디버그 연결이 되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 순수 Docker 기반이므로 거의 모든 부분을 자유롭게 커스터마이징할 수 있습니다. Sail의 Dockerfile 등을 프로젝트에 퍼블리시하려면 `sail:publish` 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

이후, 애플리케이션 루트의 `docker` 디렉터리에서 Dockerfile 및 기타 설정 파일을 수정할 수 있습니다. 커스터마이징 후에는, `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름을 변경하고 재빌드해야 합니다. 한 PC에서 여러 Laravel 프로젝트를 Sail로 개발할 경우 이미지 이름을 고유하게 지정하는 것이 특히 중요합니다:

```shell
sail build --no-cache
```
