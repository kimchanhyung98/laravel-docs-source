# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드하기](#rebuilding-sail-images)
    - [셸 별칭(alias) 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령 실행](#executing-sail-commands)
    - [PHP 명령 실행](#executing-php-commands)
    - [Composer 명령 실행](#executing-composer-commands)
    - [Artisan 명령 실행](#executing-artisan-commands)
    - [Node / NPM 명령 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [파일 스토리지](#file-storage)
- [테스트 실행](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [이메일 미리보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유하기](#sharing-your-site)
- [Xdebug로 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 경량화된 커맨드라인 인터페이스입니다. Sail은 PHP, MySQL, Redis를 이용한 Laravel 애플리케이션을 구축할 때 Docker에 대한 사전 경험 없이도 훌륭한 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 활용)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 신규 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에서 Sail을 사용하고 싶다면 Composer 패키지 매니저를 통해 Sail을 설치할 수 있습니다. 물론 이 과정은 로컬 개발 환경에 Composer 의존성 설치가 가능한 상태임을 전제로 합니다:

```shell
composer require laravel/sail --dev
```

Sail을 설치한 후, `sail:install` Artisan 명령을 실행할 수 있습니다. 이 명령은 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 게시하고, Docker 서비스와 연결하는 데 필요한 환경 변수를 `.env` 파일에 추가합니다:

```shell
php artisan sail:install
```

마지막으로, Sail을 시작할 수 있습니다. Sail 사용법을 더 배우고 싶다면 이 문서의 나머지 부분을 참고하세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux에서 Docker Desktop을 사용 중이라면, 다음 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치하기

Sail 설치 후 추가로 서비스를 더하고 싶다면, `sail:add` Artisan 명령을 사용할 수 있습니다:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령에 `--devcontainer` 옵션을 추가하면 됩니다. 이 옵션은 기본 `.devcontainer/devcontainer.json` 파일을 애플리케이션 루트에 게시합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기

Sail 이미지의 모든 패키지와 소프트웨어를 최신 상태로 유지하려면 이미지를 완전히 재빌드해야 할 수 있습니다. 다음과 같이 `build` 명령으로 할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭(alias) 설정하기

기본적으로 Sail 명령은 모든 신규 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 호출합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 대신, 셸 별칭(alias)을 등록하여 Sail 명령을 더 간편하게 사용할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

항상 사용할 수 있도록 이 별칭을 홈 디렉터리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가한 후 셸을 재시작하세요.

별칭이 설정되면 이후 Sail 명령은 단순히 `sail`로 실행할 수 있습니다. 이 문서의 나머지 예제들은 별칭이 설정되었다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션 구축에 필요한 다양한 Docker 컨테이너를 정의합니다. 각각의 컨테이너는 `docker-compose.yml` 파일 내 `services` 설정에서 확인할 수 있습니다. `laravel.test` 컨테이너는 애플리케이션을 서비스하는 주요 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 웹 서버나 데이터베이스가 동작하고 있지 않은지 확인하세요. 애플리케이션의 `docker-compose.yml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령을 실행하세요:

```shell
sail up
```

모든 컨테이너를 백그라운드(데몬) 모드로 시작하려면 `-d` 옵션을 사용하세요:

```shell
sail up -d
```

모든 컨테이너가 시작되면 웹 브라우저에서 http://localhost로 프로젝트에 접근할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C를 누르거나, 백그라운드에서 실행 중이라면 `stop` 명령을 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령 실행

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 실행되며, 로컬 컴퓨터와 격리됩니다. 그러나 Sail은 다양한 명령어(PHP, Artisan, Composer, Node / NPM 등)를 애플리케이션에 대해 실행할 수 있도록 편리한 방법을 제공합니다.

**Laravel 공식 문서에서는 Sail을 언급하지 않은 Composer, Artisan, Node / NPM 명령 예시들이 자주 등장합니다.** 이 예제들은 해당 도구가 로컬 컴퓨터에 설치되어 있음을 전제로 합니다. Sail로 환경을 구성한 경우 이러한 명령들은 Sail로 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행...
php artisan queue:work

# Laravel Sail 컨테이너에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령 실행

`php` 명령으로 PHP 명령을 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Sail이 지원하는 PHP 버전 정보는 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령 실행

`composer` 명령으로 Composer 명령을 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령 실행

`artisan` 명령으로 Laravel Artisan 명령을 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령 실행

Node 명령은 `node`로, NPM 명령은 `npm`으로 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 정의되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하거나 재시작해도 데이터가 보존됩니다.

또한 MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 자동 생성됩니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수의 값으로 이름이 지정되며 로컬 개발용입니다. 두 번째는 `testing`이라는 테스트 전용 데이터베이스로, 테스트 코드가 개발 데이터에 영향을 주지 않도록 보장합니다.

컨테이너를 시작했다면, `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 지정하여 애플리케이션에서 MySQL에 연결할 수 있습니다.

로컬 컴퓨터에서 그래픽 데이터베이스 관리 툴([TablePlus](https://tableplus.com) 등)을 이용해 연결하려면, 기본적으로 MySQL은 `localhost`의 3306 포트에서 접근할 수 있으며, 아이디와 비밀번호는 `DB_USERNAME`과 `DB_PASSWORD` 환경 변수의 값을 사용합니다. 또는 `root` 사용자로 접속할 수도 있으며, 이 경우 비밀번호는 역시 `DB_PASSWORD` 환경 변수의 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `docker-compose.yml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 추가됩니다. 이 컨테이너는 [Atlas Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 기능도 포함하는 MongoDB 문서 데이터베이스를 제공합니다. 또한 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다.

컨테이너 실행 후, `.env` 파일의 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하면 애플리케이션 내부에서 MongoDB에 연결할 수 있습니다. 인증 기능은 기본적으로 비활성화되어 있으나, 컨테이너 실행 전 `MONGODB_USERNAME`, `MONGODB_PASSWORD` 환경 변수를 설정하면 인증을 활성화할 수 있습니다. 그 후 접속 문자열에 자격증명을 추가하세요:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

애플리케이션에 MongoDB를 원활하게 연결하기 위해 [MongoDB 공식 Laravel 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 컴퓨터에서 [Compass](https://www.mongodb.com/products/tools/compass) 등 그래픽 툴로 접속하려면 기본적으로 `localhost`의 27017 포트로 접근할 수 있습니다.

<a name="redis"></a>
### Redis

`docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너도 정의되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터가 계속 유지됩니다. 컨테이너 실행 후, `.env` 파일의 `REDIS_HOST` 변수를 `redis`로 입력하면 애플리케이션 내부에서 Redis 인스턴스에 연결할 수 있습니다.

로컬 컴퓨터에서 [TablePlus](https://tableplus.com) 같은 데이터베이스 관리 툴로 연결하려면, 기본적으로 Redis는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택하면, `docker-compose.yml` 파일에 [Valkey](https://valkey.io/)가 추가됩니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로 데이터가 유지됩니다. 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 변수를 `valkey`로 설정하면 이 컨테이너로 연결할 수 있습니다.

로컬 컴퓨터에서 [TablePlus](https://tableplus.com) 같은 툴로 연결할 때도 기본적으로 `localhost`의 6379 포트에서 사용할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 강력한 검색 엔진이 포함됩니다. [Laravel Scout](/docs/{{version}}/scout)와 통합되어 있습니다. 컨테이너 실행 후, `.env` 파일에서 `MEILISEARCH_HOST` 변수를 `http://meilisearch:7700`으로 설정하면 애플리케이션에서 Meilisearch에 연결할 수 있습니다.

로컬 브라우저에서는 `http://localhost:7700`으로 접속하여 Meilisearch의 웹 기반 관리 패널을 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 빠르고 오픈소스인 검색 엔진이 추가됩니다. [Laravel Scout](/docs/{{version}}/scout#typesense)와 네이티브로 통합되어 있습니다. 컨테이너 실행 후, 다음 환경 변수를 설정하면 애플리케이션에서 Typesense에 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서는 `http://localhost:8108`로 API에 접속할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

프로덕션 환경에서 Amazon S3를 사용할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 함께 설치하는 것이 좋습니다. MinIO는 S3 호환 API를 제공하여, 실제 S3 환경에 테스트용 버킷을 만들지 않고도 로컬에서 `s3` 파일 스토리지 드라이버로 개발할 수 있게 해줍니다. MinIO를 설치하면 `docker-compose.yml` 파일에 관련 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 들어 있습니다. 이 디스크로 Amazon S3 뿐만 아니라 MinIO 등 S3 호환 파일 스토리지 서비스와도 연동할 수 있습니다. 환경 변수만 적절히 수정하면 됩니다. 예를 들어 MinIO 사용 시 파일시스템 환경 변수를 다음과 같이 정의하세요:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷명이 포함되도록 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔(http://localhost:8900)에서 버킷을 생성할 수 있습니다. 기본 MinIO 콘솔 아이디는 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행

Laravel은 기본적으로 강력한 테스트 지원을 제공하며, Sail의 `test` 명령을 이용해 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 허용하는 모든 CLI 옵션도 함께 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령은 `test` Artisan 명령과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 `testing` 전용 데이터베이스를 생성하여, 테스트가 현재 데이터베이스 상태에 영향을 주지 않도록 합니다. 기본 Laravel 설치에서는 Sail이 자동으로 `phpunit.xml` 파일 또한 올바르게 구성합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 간결하고 사용하기 편한 브라우저 자동화 및 테스트 API를 제공합니다. Sail을 활용하면 로컬 컴퓨터에 Selenium 등 별도 도구를 설치하지 않고도 이 테스트를 실행할 수 있습니다. 시작하려면, 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

그리고 `laravel.test` 서비스에 `selenium`이 의존 서비스로 설정되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작한 뒤, `dusk` 명령으로 Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용

로컬 컴퓨터가 Apple Silicon 칩을 사용할 경우, `selenium/standalone-chromium` 이미지를 사용해야 합니다:

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

Laravel Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 중 애플리케이션에서 발송한 이메일을 가로채고, 웹 인터페이스를 통해 이메일 내용을 브라우저에서 미리볼 수 있게 해줍니다. Sail에서는 기본적으로 Mailpit의 호스트가 `mailpit`이고, 포트 1025에 연결됩니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중이라면 http://localhost:8025에서 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때로는 애플리케이션 컨테이너 내부에서 Bash 세션을 시작하고 싶을 때가 있습니다. `shell` 명령을 사용해서 내부로 진입할 수 있으며, 서비스나 파일을 탐색하거나 임의의 셸 명령을 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

[Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령을 사용하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0을 통한 서비스 제공을 지원합니다. 기본 PHP 버전은 8.4입니다. PHP 버전을 변경하려면 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 경로를 수정하세요:

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

또한, 사용 중인 PHP 버전에 맞게 `image` 이름도 변경할 수 있습니다. 이 설정 역시 `docker-compose.yml` 파일에 있습니다:

```yaml
image: sail-8.2/app
```

`docker-compose.yml` 파일을 수정했다면, 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 20을 설치합니다. 설치되는 Node 버전을 변경하려면, `docker-compose.yml` 파일의 `laravel.test` 서비스에서 `build.args` 항목을 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

수정 후에는 컨테이너 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기

외부에 사이트를 잠시 공개하거나, 동료에게 미리보기를 보여주거나, 웹훅 통합을 테스트할 때 사이트를 공유해야 할 수 있습니다. 이 경우 `share` 명령을 사용하세요. 실행하면 무작위 `laravel-sail.site` URL이 발급되며, 이 URL로 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령으로 사이트를 공유할 때, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드로 신뢰할 수 있는 프록시를 설정해야 합니다. 그렇지 않으면 `url` 및 `route`와 같은 URL 생성 헬퍼가 올바른 HTTP 호스트를 파악하지 못할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 서브도메인을 직접 지정하려면 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령은 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose) 기반입니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅

Laravel Sail의 Docker 구성은 강력한 PHP 디버거인 [Xdebug](https://xdebug.org/)를 지원합니다. Xdebug를 활성화하려면 [Sail 설정을 게시](#sail-customization)한 상태여야 하며, 아래와 같이 애플리케이션의 `.env` 파일에 변수들을 추가하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고 게시된 `php.ini`의 다음 설정이 포함되어 있는지 확인하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini`를 수정했다면 Docker 이미지를 재빌드하여 변경사항을 반영하세요:

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어 있으므로 Mac과 Windows(WSL2)에서는 별도의 설정이 필요 없습니다. Linux에서 Docker 20.10 이상을 사용한다면 `host.docker.internal`도 바로 사용할 수 있습니다.

만약 Docker 20.10 미만의 리눅스 환경이라면 `host.docker.internal`이 지원되지 않으므로, 컨테이너에 고정 IP를 직접 할당해야 합니다. `docker-compose.yml`에 커스텀 네트워크를 설정하세요:

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

고정 IP를 할당했다면, `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 설정하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

Artisan 명령을 디버깅 세션으로 실행하려면 `sail debug` 명령을 사용하세요:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug로 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저로 애플리케이션에 접근하면서 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)의 안내에 따라 디버깅 세션을 시작하세요.

PhpStorm 환경이라면 [제로설정(Zero-configuration) 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 문서를 참고하세요.

> [!WARNING]
> Laravel Sail은 `artisan serve` 명령으로 애플리케이션을 서비스합니다. `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수는 Laravel 8.53.0 이상에서만 지원됩니다. 8.52.0 이하 버전에서는 지원되지 않으니 유의하세요.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 Docker이기 때문에 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 자체 Dockerfile을 게시하려면, 아래 명령을 실행하세요:

```shell
sail artisan sail:publish
```

명령 실행 시 Dockerfile 및 관련 설정 파일들이 애플리케이션의 `docker` 디렉터리에 복사됩니다. 커스터마이즈 후에는 애플리케이션 컨테이너의 `docker-compose.yml` 파일에서 이미지 이름을 바꾸고, 반드시 컨테이너를 다시 빌드해야 합니다. 같은 컴퓨터에서 여러 Laravel 애플리케이션을 개발하는 경우에는 컨테이너 이미지에 고유 이름을 주는 것이 특히 중요합니다:

```shell
sail build --no-cache
```
