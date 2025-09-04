# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드하기](#rebuilding-sail-images)
    - [셸(alias) 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행하기](#executing-php-commands)
    - [Composer 명령어 실행하기](#executing-composer-commands)
    - [Artisan 명령어 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령어 실행하기](#executing-node-npm-commands)
- [데이터베이스와 상호작용하기](#interacting-with-sail-databases)
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
- [사이트 공유하기](#sharing-your-site)
- [Xdebug로 디버깅하기](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 경량의 커맨드라인 인터페이스입니다. Sail을 이용하면 Docker에 대한 사전 지식 없이 PHP, MySQL, Redis를 활용하여 Laravel 애플리케이션을 손쉽게 시작할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 쉽고 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows(WSL2를 통해)에서 사용할 수 있습니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 새로운 Laravel 애플리케이션 생성 시 자동으로 설치되므로 즉시 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에서 Sail을 사용하고자 한다면, Composer 패키지 매니저를 통해 Sail을 간단히 설치할 수 있습니다. 물론, 아래 단계는 현재 로컬 개발 환경에서 Composer 의존성을 설치할 수 있는 경우에 적용됩니다:

```shell
composer require laravel/sail --dev
```

Sail 설치가 완료되면 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 복사하고, Docker 서비스에 연결할 수 있도록 필요한 환경 변수를 `.env` 파일에 추가합니다:

```shell
php artisan sail:install
```

마지막으로, Sail을 시작할 수 있습니다. Sail 사용 방법에 대한 자세한 내용은 아래 문서를 계속 참고하세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux에서 Docker Desktop을 사용하는 경우, 아래 명령어를 실행하여 반드시 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치하기

기존 Sail 환경에 추가 서비스를 추가하고 싶다면 `sail:add` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하기를 원한다면, `sail:install` 명령어 실행 시 `--devcontainer` 옵션을 추가하세요. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 생성합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기

Sail 이미지를 완전히 재빌드하여 최신 패키지 및 소프트웨어가 반영되도록 하고 싶을 때는 아래와 같이 `build` 명령어를 사용할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸(alias) 설정하기

기본적으로 Sail 명령어는 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 실행합니다:

```shell
./vendor/bin/sail up
```

그러나 매번 `vendor/bin/sail`을 입력하는 것이 번거롭다면, 셸 alias를 설정하여 손쉽게 Sail 명령어를 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 alias를 항상 사용할 수 있도록 홈 디렉토리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 위 라인을 추가한 뒤, 셸을 재시작합니다.

alias 설정 이후에는 단순히 `sail` 명령어만 입력해 Sail 명령을 실행할 수 있습니다. 이후 이 문서의 모든 예제도 alias가 적용된 것으로 안내합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일은 여러 Docker 컨테이너를 정의하여 Laravel 애플리케이션 개발을 돕습니다. 각 컨테이너는 `docker-compose.yml` 파일의 `services` 섹션에 정의되어 있습니다. 이 중 `laravel.test` 컨테이너가 주요 애플리케이션 컨테이너로서, 실제로 여러분의 애플리케이션이 실행되는 곳입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 실행 중인 다른 웹 서버나 데이터베이스가 없는지 확인하세요. `up` 명령어로 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작할 수 있습니다:

```shell
sail up
```

모든 컨테이너를 백그라운드(detached) 모드로 실행하고 싶으면 아래 명령을 사용하세요:

```shell
sail up -d
```

애플리케이션의 컨테이너가 모두 시작되면 웹 브라우저에서 http://localhost로 접속할 수 있습니다.

컨테이너를 중지하려면 Control + C를 누르거나, 백그라운드로 실행 중이라면 아래와 같이 `stop` 명령어를 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 로컬 컴퓨터와 격리된 Docker 컨테이너 내에서 실행됩니다. 하지만 Sail은 다양한 명령어(PHP, Artisan, Composer, Node/NPM 명령어 등)를 간편하게 실행할 수 있는 방식을 제공합니다.

**Laravel 공식 문서를 보다 보면, Sail을 거치지 않고 Composer, Artisan, Node/NPM 명령어를 직접 실행하는 예시가 종종 등장합니다.** 해당 예시들은 도구가 로컬에 설치된 경우를 전제로 합니다. 만약 Sail 환경에서 Laravel을 개발 중이라면, 이러한 명령어도 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행...
php artisan queue:work

# Laravel Sail에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기

`php` 명령어로 PHP 관련 명령을 실행할 수 있습니다. 이 명령어는 여러분이 설정한 PHP 버전에서 동작합니다. Laravel Sail에서 사용 가능한 PHP 버전에 대한 자세한 내용은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기

Composer 관련 명령은 `composer` 명령어로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 이미 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행하기

Laravel Artisan 명령어는 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행하기

Node 관련 명령은 `node`, NPM 명령은 `npm` 명령으로 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하고 다시 시작해도 데이터가 유지됩니다.

또한 MySQL 컨테이너가 최초로 실행될 때 두 개의 데이터베이스가 자동 생성됩니다. 첫 번째는 `DB_DATABASE` 환경 변수의 값으로 지정된 이름의 개발용 데이터베이스이며, 두 번째는 `testing`이라는 전용 테스트 데이터베이스입니다. 이를 통해 테스트가 개발 데이터에 영향을 주지 않습니다.

컨테이너가 실행된 후, 애플리케이션 내에서 MySQL에 연결하려면 `.env` 파일의 `DB_HOST` 값을 `mysql`로 지정하면 됩니다.

로컬 컴퓨터에서 MySQL 데이터베이스에 접속하고 싶다면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 MySQL은 `localhost`의 3306 포트에서 사용할 수 있으며, 접속 정보는 `DB_USERNAME`과 `DB_PASSWORD` 환경 변수의 값과 일치합니다. 또는 `root` 사용자로 접속할 수도 있고, 이 때도 비밀번호는 `DB_PASSWORD` 환경 변수의 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `docker-compose.yml` 파일에는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 포함됩니다. 이 컨테이너는 Atlas의 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 기능을 제공합니다. 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다.

컨테이너 실행 후, 애플리케이션 내에서 MongoDB에 연결하려면 `.env` 파일의 `MONGODB_URI`를 `mongodb://mongodb:27017`로 지정하면 됩니다. 기본적으로 인증은 비활성화되어 있지만, `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 관련 인증 정보는 연결 문자열에 포함시키면 됩니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 Laravel의 원활한 연동을 위해, [MongoDB에서 공식적으로 관리하는 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 사용할 수 있습니다.

로컬 컴퓨터에서 MongoDB 데이터베이스에 접속하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI를 사용할 수 있습니다. 기본적으로 MongoDB는 `localhost`의 27017 포트에서 접속할 수 있습니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터가 유지됩니다. 컨테이너가 실행된 후, 애플리케이션 내에서 Redis에 연결하려면 `.env` 파일의 `REDIS_HOST` 값을 `redis`로 설정하면 됩니다.

로컬 컴퓨터에서 Redis 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 도구를 사용할 수 있습니다. 기본적으로 Redis는 `localhost`의 6379 포트에서 사용할 수 있습니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택하면, 애플리케이션의 `docker-compose.yml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터가 유지됩니다. 애플리케이션 내에서는 `.env` 파일의 `REDIS_HOST` 값을 `valkey`로 설정해 이 컨테이너에 접속할 수 있습니다.

로컬 컴퓨터에서 Valkey 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 도구를 사용할 수 있으며, 기본 접속 포트는 6379입니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 강력한 검색 엔진이 추가됩니다. Meilisearch는 [Laravel Scout](/docs/12.x/scout)와 통합되어 사용할 수 있습니다. 컨테이너가 실행된 후, 애플리케이션 내에서는 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 지정해 연결할 수 있습니다.

로컬 컴퓨터에서는 웹 브라우저를 통해 `http://localhost:7700`으로 Meilisearch의 웹 관리 패널에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 빠르고 오픈소스 기반의 검색 엔진이 추가됩니다. Typesense는 [Laravel Scout](/docs/12.x/scout#typesense)와 통합되어 사용할 수 있습니다. 컨테이너 실행 후 다음 환경 변수를 설정해 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬에서는 `http://localhost:8108`을 통해 Typesense의 API에 접속할 수 있습니다.

<a name="file-storage"></a>
## 파일 저장소 (File Storage)

애플리케이션을 운영 환경에서 Amazon S3를 활용해 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 선택할 수 있습니다. MinIO는 S3와 호환되는 API를 제공해, 실제 운영용 S3 버킷을 만들지 않고도 Laravel의 `s3` 파일 스토리지 드라이버를 로컬 개발 중에 사용할 수 있습니다. 설치 시, 애플리케이션의 `docker-compose.yml` 파일에 MinIO 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 설정이 있습니다. Amazon S3 뿐만 아니라 MinIO와 같은 S3 호환 파일 저장소도 환경 변수만 적절히 변경하여 사용할 수 있습니다. MinIO를 사용할 때는 다음과 같이 환경 변수를 지정합니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO 사용 시, Flysystem 통합모듈이 올바른 URL을 생성할 수 있도록 `AWS_URL` 변수도 다음과 같이 지정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 웹 브라우저에서 `http://localhost:8900`으로 접속 가능합니다. 기본 로그인 정보는 사용자명 `sail`, 비밀번호 `password`입니다.

> [!WARNING]
> MinIO 사용 시, `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 뛰어난 테스트 지원을 기본 제공하며, Sail의 `test` 명령어로 애플리케이션의 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 사용할 수 있는 모든 CLI 옵션을 그대로 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어를 실행하는 것과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 테스트 수행 시 실제 데이터베이스와 충돌하지 않도록 `testing`이라는 전용 데이터베이스를 생성합니다. Laravel의 기본 설치에서는 Sail이 `phpunit.xml` 파일도 이 전용 데이터베이스를 사용하도록 자동 구성합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 쉽고 직관적인 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 로컬 컴퓨터에 Selenium 같은 브라우저 자동화 툴을 별도로 설치하지 않고도 이러한 테스트를 실행할 수 있습니다. 사용을 시작하려면, 먼저 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

다음으로 `laravel.test` 서비스가 `selenium`에 종속되어 있도록 `depends_on`에 추가하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작하고 아래 명령어로 Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용

로컬 컴퓨터가 Apple Silicon 칩을 사용한다면, `selenium` 서비스는 `selenium/standalone-chromium` 이미지를 사용해야 합니다:

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
## 이메일 미리보기 (Previewing Emails)

Laravel Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 발송되는 이메일을 가로채 웹 기반 인터페이스로 미리보기를 제공합니다. Sail 사용 시, Mailpit의 기본 호스트는 `mailpit`, 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중이라면 http://localhost:8025 에서 Mailpit 웹 인터페이스에 접속할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션의 컨테이너 내부에서 Bash 세션을 시작하고 싶을 때가 있습니다. 이때 `shell` 명령어를 사용하면 컨테이너에 접속하여 파일과 설치된 서비스 확인, 임의의 셸 명령어 실행이 가능합니다:

```shell
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 사용할 수 있습니다:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전을 지원합니다. 기본 PHP 버전은 8.4입니다. 다른 PHP 버전으로 변경하려면, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 경로를 수정하세요:

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

또한, 실제로 사용하는 PHP 버전을 반영하도록 `image` 이름도 변경할 수 있습니다. 이 설정 역시 `docker-compose.yml` 파일에서 지정합니다:

```yaml
image: sail-8.2/app
```

설정을 모두 마친 뒤에는 반드시 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 시 사용되는 Node 버전을 변경하려면, 애플리케이션의 `docker-compose.yml` 파일의 `laravel.test` 서비스 내 `build.args` 항목을 다음과 같이 수정합니다:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

수정 후 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나, 웹후크 통합을 테스트할 때 애플리케이션을 외부에 공개해야 하는 경우가 있습니다. 이럴 때 `share` 명령어를 사용할 수 있습니다. 명령어 실행 후 임의의 `laravel-sail.site` URL이 발급되며, 해당 링크로 사이트에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령어로 사이트를 공유할 때는, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 통해 신뢰할 수 있는 프록시를 올바르게 지정해야 합니다. 그렇지 않으면, `url`과 `route`와 같은 URL 생성 헬퍼가 올바른 호스트 정보를 알 수 없어 제대로 동작하지 않을 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 서브 도메인을 직접 지정하려면 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 사용합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 구성에는 PHP에서 널리 사용되는 강력한 디버거인 [Xdebug](https://xdebug.org/)가 지원됩니다. Xdebug를 활성화하려면, [Sail 설정을 게시](#sail-customization)한 뒤, 아래와 같이 애플리케이션의 `.env` 파일에 환경 변수를 추가하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

이어서, 게시된 `php.ini` 파일에 아래 설정이 포함되어 있는지 확인하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 변경했다면, 변경 사항이 반영되도록 Docker 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어 있어 Mac 및 Windows(WSL2) 환경에서 Xdebug가 정상 동작합니다. 만약 Linux에서 Docker 20.10 이상을 사용 중이면 `host.docker.internal`이 그대로 지원되므로 별도의 설정이 필요 없습니다.

20.10 이하의 Docker를 Linux에서 사용하는 경우에는 `host.docker.internal`을 지원하지 않으므로, 직접 컨테이너에 고정 IP를 할당해야 합니다. 이때, `docker-compose.yml` 파일에 아래와 같이 커스텀 네트워크를 정의합니다:

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

설정 후, 애플리케이션의 .env 파일에 SAIL_XDEBUG_CONFIG 변수를 아래와 같이 지정합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

Artisan 명령어를 디버깅하며 실행하고 싶을 때는 `sail debug` 명령어를 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug로 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

애플리케이션을 웹 브라우저로 조작하면서 디버깅하려면, [Xdebug에서 안내하는 방법](https://xdebug.org/docs/step_debug#web-application)을 따라 브라우저에서 Xdebug 세션을 시작하세요.

PhpStorm을 사용하는 경우 [제로-설정 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 JetBrains 문서를 참고하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션 구동에 `artisan serve`를 사용합니다. `artisan serve` 명령은 Laravel 8.53.0 이상에서만 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 인식합니다. 8.52.0 이하 버전은 이러한 디버깅 변수를 지원하지 않으니 주의하세요.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 기반이기 때문에, 대부분의 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail 자체 Dockerfile 등을 프로젝트 내로 복사하려면 아래 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

이 명령을 실행하면 Dockerfile 및 관련 설정 파일들이 애플리케이션 루트 `docker` 디렉토리에 복사됩니다. Sail 환경을 커스터마이즈한 뒤에는, 애플리케이션 컨테이너의 `image` 이름을 `docker-compose.yml` 파일에서 고유하게 변경할 수도 있습니다. 특히 하나의 컴퓨터에서 여러 Laravel 프로젝트를 각각 Sail로 개발 중이라면 이미지 이름을 다르게 지정하는 것이 좋습니다. 변경한 뒤에는 반드시 컨테이너를 재빌드하세요:

```shell
sail build --no-cache
```