# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [셸 별칭(shell alias) 설정](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와의 상호작용](#interacting-with-sail-databases)
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
- [사이트 공유](#sharing-your-site)
- [Xdebug로 디버깅하기](#debugging-with-xdebug)
  - [Xdebug CLI 사용](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있도록 가벼운 명령줄 인터페이스(CLI)를 제공합니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 이용해 Laravel 애플리케이션을 쉽게 구축할 수 있는 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너들과 손쉽게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows(WSL2를 통해)에서 사용할 수 있습니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에서 Sail을 사용하려면 Composer 패키지 매니저를 통해 Sail을 설치하면 됩니다. 아래 과정은 로컬 개발 환경에서 Composer 의존성 설치가 가능한 경우에 해당합니다:

```shell
composer require laravel/sail --dev
```

Sail 설치 후, `sail:install` Artisan 명령어를 실행합니다. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 복사하고, Docker 서비스와 연결할 수 있도록 `.env` 파일을 수정합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail의 사용법을 계속 배우려면 이 문서를 계속 읽어보시기 바랍니다:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux에서 Docker Desktop을 사용하는 경우, 아래 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 서비스를 추가하고 싶다면, `sail:add` Artisan 명령어를 실행하면 됩니다:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 활용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers)에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 기본 `.devcontainer/devcontainer.json` 파일을 애플리케이션 루트에 생성합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

Sail 이미지 내 모든 패키지와 소프트웨어를 최신 상태로 유지하려면 이미지를 완전히 재빌드할 수 있습니다. 다음과 같이 실행하세요:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭(shell alias) 설정

기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 실행합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 것이 번거롭다면, 별칭(alias)을 설정해 쉽게 Sail 명령어를 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭이 항상 적용되도록 하려면, 자신의 홈 디렉터리에 위치한 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가한 뒤 셸을 재시작하세요.

이제 별칭이 설정되었으므로, 단순히 `sail`이라고만 입력해도 Sail 명령어를 실행할 수 있습니다. 이 문서의 예제들은 이 별칭이 적용되어 있다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일에는 여러 Docker 컨테이너가 정의되어 있습니다. 이 컨테이너들은 함께 동작하여 Laravel 애플리케이션을 개발할 수 있도록 도와줍니다. 각 컨테이너는 `compose.yaml` 파일 내 `services` 설정에 포함되어 있습니다. `laravel.test` 컨테이너가 기본 애플리케이션 컨테이너로, 실제로 여러분의 애플리케이션을 서비스합니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. `compose.yaml`에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행합니다:

```shell
sail up
```

모든 컨테이너를 백그라운드(detached) 모드로 실행하고 싶다면 다음과 같이 실행하세요:

```shell
sail up -d
```

컨테이너가 시작되면, http://localhost 에서 웹 브라우저로 프로젝트를 확인할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C를 눌러 실행을 멈추거나, 백그라운드로 실행 중일 경우 `stop` 명령어를 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되어 로컬 컴퓨터와 격리됩니다. 하지만 Sail을 사용하면 PHP 명령어, Artisan 명령어, Composer 명령어, Node/NPM 명령어 등 다양한 명령어를 간편하게 실행할 수 있습니다.

**Laravel 공식 문서에서 Composer, Artisan, Node/NPM 명령어가 Sail 없이 안내되는 경우가 많습니다.** 이는 해당 도구들이 로컬 컴퓨터에 직접 설치되어 있다고 가정한 것이지만, Sail 환경을 사용한다면 해당 명령어도 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행...
php artisan queue:work

# Laravel Sail에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령어로 실행할 수 있습니다. 이렇게 하면 애플리케이션에 설정된 PHP 버전이 사용됩니다. Sail에서 사용 가능한 PHP 버전에 대한 자세한 내용은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer가 기본적으로 포함되어 있습니다:

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
## 데이터베이스와의 상호작용 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터베이스에 저장된 데이터가 컨테이너를 중지하거나 재시작해도 유지됩니다.

처음 MySQL 컨테이너가 시작될 때, 두 개의 데이터베이스가 자동 생성됩니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수의 값으로 이름이 지정되며, 로컬 개발에 사용됩니다. 두 번째는 `testing`이라는 이름의 전용 테스트 데이터베이스로, 테스트와 개발 데이터가 섞이지 않도록 합니다.

컨테이너가 시작된 후, 애플리케이션 내부에서 MySQL 인스턴스에 연결하려면 `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 설정하면 됩니다.

로컬 컴퓨터에서 MySQL 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com)와 같은 GUI 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 MySQL은 `localhost`의 포트 3306에서 접근 가능하며, 접속 정보는 `DB_USERNAME`, `DB_PASSWORD` 환경 변수 값과 일치합니다. 또는 `root` 계정으로도 접속할 수 있고, 이때도 비밀번호는 `DB_PASSWORD` 값이 사용됩니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, 애플리케이션의 `compose.yaml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 추가됩니다. 이 컨테이너는 Atlas의 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 기능을 제공합니다. 또한 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다.

컨테이너가 시작된 후 애플리케이션 내부에서 MongoDB에 연결하려면 `.env` 파일의 `MONGODB_URI`를 `mongodb://mongodb:27017`로 설정하세요. 기본적으로 인증은 비활성화되어 있으나, 컨테이너 시작 전에 `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 그리고 연결 문자열에 접속 정보를 포함시킵니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB를 애플리케이션에 매끄럽게 통합하려면 [MongoDB에서 공식적으로 관리하는 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 컴퓨터에서 MongoDB 데이터베이스에 연결하려면 [Compass](https://www.mongodb.com/products/tools/compass)와 같은 GUI를 사용할 수 있습니다. 기본적으로 포트 `27017`에서 접근 가능합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다. 컨테이너가 시작된 후, 애플리케이션 내부에서 Redis 인스턴스에 연결하려면 `.env` 파일의 `REDIS_HOST`를 `redis`로 지정하면 됩니다.

로컬 컴퓨터에서 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com)와 같은 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost`의 포트 6379에서 접근 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `compose.yaml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다. 애플리케이션 내부에서 연결하려면 `.env` 파일의 `REDIS_HOST`를 `valkey`로 설정하세요.

로컬 컴퓨터에서 Valkey 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 등을 사용할 수 있습니다. 기본적으로 포트 6379에서 접근 가능합니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면 `compose.yaml` 파일에 해당 강력한 검색 엔진 항목이 생성됩니다. 이 엔진은 [Laravel Scout](/docs/12.x/scout)와 연동됩니다. 컨테이너가 시작된 후 애플리케이션에서 Meilisearch에 연결하려면 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정하세요.

로컬 컴퓨터에서는 웹 브라우저에서 `http://localhost:7700`에 접속해 Meilisearch의 웹 기반 관리자 패널을 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `compose.yaml` 파일에 이 초고속 오픈소스 검색 엔진 항목이 추가됩니다. 이 엔진 역시 [Laravel Scout](/docs/12.x/scout#typesense)와 기본 연동됩니다. 컨테이너가 시작된 후에는 다음 환경 변수를 설정해 Typesense에 연결합니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서 `http://localhost:8108`을 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 파일 저장소로 Amazon S3를 사용할 계획이라면, Sail 설치 시에 [MinIO](https://min.io) 서비스를 설치하는 것이 좋습니다. MinIO는 S3와 호환되는 API를 제공해, 프로덕션 S3 환경에 테스트용 버킷을 생성하지 않고도 로컬에서 `s3` 파일 시스템 드라이버를 활용하여 개발할 수 있습니다. MinIO를 설치하면 `compose.yaml` 파일에 관련 설정도 자동으로 추가됩니다.

애플리케이션의 `filesystems` 설정 파일에는 기본적으로 `s3` 디스크 설정이 포함되어 있습니다. 해당 디스크를 이용해 Amazon S3 뿐만 아니라 MinIO 등 S3 호환 저장소도 연동할 수 있습니다. MinIO를 사용할 때는 관련 환경 변수를 아래와 같이 설정합니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 통합에서 URL을 제대로 생성하려면, `AWS_URL` 환경 변수도 다음처럼 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 `http://localhost:8900`에서 사용할 수 있으며, 기본 사용자명은 `sail`, 기본 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 뛰어난 테스트 지원을 제공하며, Sail의 `test` 명령어를 통해 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 허용하는 모든 CLI 옵션을 `test` 명령어에도 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어 실행과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 전용 `testing` 데이터베이스를 생성하여 테스트가 실제 데이터베이스 상태에 영향을 주지 않도록 합니다. 기본 Laravel 설치에서는 Sail이 테스트 실행 시에 `phpunit.xml` 파일을 아래와 같이 자동 설정합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화, 테스트 API를 제공합니다. Sail 덕분에 로컬 컴퓨터에 Selenium이나 다른 툴을 설치하지 않아도 Dusk 테스트를 실행할 수 있습니다. 먼저, `compose.yaml` 파일 내 Selenium 서비스를 주석 해제하세요:

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

그리고 `laravel.test` 서비스에 `selenium`이 `depends_on`에 포함되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작한 뒤, Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용

로컬 컴퓨터가 Apple Silicon 칩(M 시리즈 등)을 사용한다면, `selenium` 서비스 이미지로 `selenium/standalone-chromium`을 사용해야 합니다:

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

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 개발 중 애플리케이션이 보내는 이메일을 가로채고, 웹 인터페이스(UI)를 통해 브라우저에서 이메일 내용을 쉽게 미리 볼 수 있게 해줍니다. Sail을 사용할 때 Mailpit의 기본 호스트는 `mailpit`이고, 1025 포트에서 SMTP를 수신합니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때는 웹 브라우저에서 http://localhost:8025 에 접속하여 Mailpit을 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

때때로 애플리케이션의 컨테이너에서 Bash 세션을 시작하고 싶은 경우가 있습니다. `shell` 명령어를 사용하면 컨테이너 내부에 직접 접속하여 파일, 설치된 서비스, 기타 임의의 셸 명령어를 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

[Larevel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0을 지원합니다. 기본값은 PHP 8.4입니다. 사용하고자 하는 PHP 버전을 변경하려면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 항목을 아래와 같이 변경하세요:

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

추가로, 사용 중인 PHP 버전을 이미지 이름에서도 나타내고 싶다면, 이 항목 역시 `compose.yaml` 파일에서 지정할 수 있습니다:

```yaml
image: sail-8.2/app
```

`compose.yaml` 파일을 수정한 후에는, 컨테이너 이미지를 반드시 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 시 설치할 Node 버전을 변경하려면, `compose.yaml` 파일의 `laravel.test` 서비스에서 `build.args` 항목의 `NODE_VERSION` 값을 변경하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

`compose.yaml` 파일을 수정한 후에는, 이미지도 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나, 웹훅 통합을 테스트해야 하는 경우 사이트를 외부에 임시로 공유할 수 있습니다. 이를 위해 `share` 명령어를 사용하세요. 명령어 실행 시 무작위로 발급되는 `laravel-sail.site` URL을 통해 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

사이트를 공유할 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 이용해 신뢰할 프록시를 설정해야 합니다. 이를 지정하지 않으면 `url`, `route` 등 URL 생성 헬퍼 함수가 올바른 HTTP 호스트를 판단하지 못할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 하위 도메인을 직접 지정하고 싶다면, `share` 명령어 실행 시 `subdomain` 옵션을 지정하세요:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)가 개발한 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)가 동작을 지원합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 구성은 강력한 PHP 디버거인 [Xdebug](https://xdebug.org/)를 지원합니다. Xdebug를 활성화하려면 [Sail 구성을 게시](#sail-customization)했는지 확인하고, 애플리케이션의 `.env` 파일에 아래 변수를 추가해 Xdebug를 설정하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

또한 게시된 `php.ini` 파일에 다음 설정이 포함되어야 Xdebug가 지정된 모드에서 활성화됩니다:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini`를 수정한 후에는 도커 이미지를 다시 빌드해야 변경 사항이 반영됩니다:

```shell
sail build --no-cache
```

#### Linux 호스트의 IP 구성

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있어, Mac 및 Windows(WSL2) 환경에서 자동으로 정상 작동합니다. 로컬 머신이 Linux이고 Docker 20.10 이상이면 별도 설정이 필요 없습니다.

하지만 Docker 20.10 이하에서는 Linux에서 `host.docker.internal`이 지원되지 않으므로, 컨테이너에 고정 IP를 할당해 수동으로 호스트 IP를 지정해야 합니다. 아래와 같이 `compose.yaml`에서 커스텀 네트워크와 IP를 지정하세요:

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

고정 IP를 지정한 후에는 `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 다음과 같이 설정합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용

Artisan 명령어를 실행할 때 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug로 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용

웹 브라우저로 애플리케이션을 사용하는 동안 디버깅하려면, Xdebug 공식 문서에 안내된 [브라우저에서 Xdebug 세션 시작 방법](https://xdebug.org/docs/step_debug#web-application)을 참고하세요.

PhpStorm을 사용한다면, JetBrains의 [Zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 문서를 참고하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션을 서비스할 때 `artisan serve`를 사용합니다. `XDEBUG_CONFIG`, `XDEBUG_MODE` 변수를 지원하는 `artisan serve` 명령어는 Laravel 8.53.0 이상에서만 동작합니다. 8.52.0 이하 버전에서는 해당 변수 지원이 없어 디버그 연결이 되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 기반이므로 원하는 대부분의 사항을 자유롭게 커스터마이즈할 수 있습니다. Sail의 Dockerfile을 애플리케이션에 직접 생성하려면 다음 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

실행하면 Dockerfile 및 Sail이 사용하는 기타 설정 파일이 애플리케이션 루트의 `docker` 디렉터리에 복사됩니다. 설치를 커스터마이징한 후에는, 필요하다면 `compose.yaml` 파일에서 애플리케이션 컨테이너의 이미지 이름을 변경할 수 있습니다. 변경 후에는 반드시 아래와 같이 컨테이너 이미지를 재빌드하세요. 여러 Laravel 애플리케이션을 한 머신에서 개발할 경우, 이미지 이름을 각각 다르게 하는 것이 특히 중요합니다:

```shell
sail build --no-cache
```