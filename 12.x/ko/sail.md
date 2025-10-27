# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [셸(alias) 설정](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node/NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
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
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경을 손쉽게 다룰 수 있게 해주는 가벼운 커맨드라인 인터페이스입니다. Sail을 이용하면 Docker에 대한 선행 지식 없이도 PHP, MySQL, Redis 등으로 Laravel 애플리케이션을 빠르게 시작할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 위치하는 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너들을 쉽게 조작할 수 있도록 CLI 방식을 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용)를 지원합니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 신규 Laravel 애플리케이션에 기본적으로 설치되어 있으므로 별도의 추가 설치 없이 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에도 Sail을 사용할 수 있습니다. Composer 패키지 매니저를 이용해 Sail을 설치하면 됩니다. 아래 과정은 로컬 개발 환경에서 Composer 의존성 설치가 가능한 환경에서 진행해야 합니다:

```shell
composer require laravel/sail --dev
```

Sail이 설치되면, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 애플리케이션 루트에 Sail의 `compose.yaml` 파일을 배포하고, Docker 서비스 연결에 필요한 환경 변수를 `.env` 파일에 자동으로 등록합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 실행할 수 있습니다. Sail 사용법에 대해 더 궁금하다면, 이 문서의 아래 내용을 계속 읽어보시기 바랍니다:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux에서 Docker Desktop을 사용하는 경우, 반드시 `default` Docker 컨텍스트를 사용해야 합니다. 다음 명령어를 실행하세요: `docker context use default`. 또한, 컨테이너 내부에서 파일 권한 오류가 발생할 경우, `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 설정해야 할 수 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가

기존 Sail 설치에 다른 서비스를 추가하고 싶은 경우, `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 배포합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드 (Rebuilding Sail Images)

이미지의 패키지와 소프트웨어를 최신 상태로 유지하려면 Sail 이미지를 완전히 재빌드할 수 있습니다. 아래 명령어를 사용하세요:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸(alias) 설정 (Configuring A Shell Alias)

Sail 명령은 기본적으로 모든 신규 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 실행합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 대신, 셸 alias를 설정해서 더 간단하게 명령어를 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 alias를 항상 사용할 수 있도록 하려면, 홈 디렉터리의 셸 설정 파일(`~/.zshrc` 또는 `~/.bashrc` 등)에 위 내용을 추가한 뒤 셸을 재시작하세요.

alias 설정이 완료되면, Sail 명령을 `sail`만 입력으로 간편하게 실행할 수 있습니다. 이 문서의 나머지 예제들은 alias가 이미 설정되어 있다는 가정하에 작성되었습니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일에는 Laravel 애플리케이션을 개발하는 데 필요한 다양한 Docker 컨테이너가 정의되어 있습니다. 각각의 컨테이너는 `compose.yaml` 파일의 `services` 항목에 등록되어 있습니다. 그중에서도 `laravel.test` 컨테이너가 애플리케이션의 주요 역할을 담당합니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹서버나 데이터베이스가 실행되고 있지 않은지 확인하세요. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 실행하려면 아래 명령을 사용하세요:

```shell
sail up
```

백그라운드에서 모든 Docker 컨테이너를 실행하려면 "detached" 모드로 시작할 수 있습니다:

```shell
sail up -d
```

애플리케이션 컨테이너가 실행되면 웹 브라우저에서 http://localhost 주소로 프로젝트에 접근할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C로 실행을 멈추거나, 백그라운드 실행 중일 경우 `stop` 명령을 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되며 로컬 컴퓨터와 격리되어 있습니다. 하지만 Sail은 PHP, Artisan, Composer, Node/NPM 명령어 등 다양한 명령을 쉽게 실행할 수 있는 편리한 방법을 제공합니다.

**Laravel 공식 문서에는 Sail을 명시하지 않은 Composer, Artisan, Node/NPM 명령어들이 자주 등장합니다.** 이는 해당 툴들이 로컬 PC에 설치되어 있다고 가정한 예시입니다. 만약 Sail을 로컬 Laravel 개발 환경으로 사용하고 있다면 이런 명령어들은 Sail을 통해 실행하세요:

```shell
# 로컬에서 Artisan 명령 실행 예시...
php artisan queue:work

# Laravel Sail 컨테이너에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행 (Executing PHP Commands)

PHP 명령어는 `php` 명령을 통해 실행할 수 있습니다. 실행되는 PHP 버전은 애플리케이션에 설정된 버전을 따릅니다. Sail에서 사용 가능한 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행 (Executing Composer Commands)

Composer 명령어는 `composer` 명령을 통해 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer가 기본으로 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행 (Executing Artisan Commands)

Laravel Artisan 명령어 역시 `artisan` 명령을 통해 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node/NPM 명령어 실행 (Executing Node / NPM Commands)

Node 명령어는 `node` 명령으로, NPM 명령어는 `npm` 명령으로 각각 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn도 사용할 수 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하고 다시 시작해도 데이터베이스 데이터가 유지됩니다.

또한, MySQL 컨테이너가 처음 시작될 때, 두 개의 데이터베이스가 자동으로 생성됩니다. 하나는 `DB_DATABASE` 환경 변수 값으로 이름이 정해지며 로컬 개발용 데이터베이스입니다. 다른 하나는 `testing`이라는 이름의 전용 테스트 데이터베이스로, 테스트가 개발 데이터에 영향을 주지 않게 보호합니다.

컨테이너 실행 후, 애플리케이션 내에서 MySQL 인스턴스에 연결하려면 `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 설정하세요.

로컬 PC에서 MySQL 데이터베이스에 직접 연결하려면, [TablePlus](https://tableplus.com)와 같은 그래픽 데이터베이스 툴을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근 가능하며, 접속 정보는 각각 `DB_USERNAME`, `DB_PASSWORD` 환경 변수 값을 사용합니다. 또는 `root` 계정으로도 접속할 수 있습니다. 이 경우 패스워드 역시 `DB_PASSWORD` 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `compose.yaml` 파일에는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 추가됩니다. 이 컨테이너는 Atlas의 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 기능을 제공합니다. 해당 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 활용하므로, 컨테이너를 재시작해도 데이터가 유지됩니다.

컨테이너 실행 후, 애플리케이션 내부에서 MongoDB 인스턴스에 연결하려면 `.env` 파일의 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하세요.

인증은 기본적으로 비활성화되어 있지만, 컨테이너 실행 전에 `MONGODB_USERNAME`, `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 이 경우 연결 문자열에도 인증 정보를 포함해야 합니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 애플리케이션을 쉽게 연동하려면 [MongoDB 공식 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치하면 됩니다.

로컬 PC에서 MongoDB 데이터베이스에 연결하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI를 사용할 수 있습니다. 기본적으로 MongoDB는 `localhost` 27017 포트에서 접근할 수 있습니다.

<a name="redis"></a>
### Redis

또한, `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터를 안전하게 보존합니다. 컨테이너가 실행 중이라면, `.env` 파일의 `REDIS_HOST` 환경 변수 값을 `redis`로 설정하세요.

로컬 PC에서 Redis에 접속하려면, [TablePlus](https://tableplus.com) 등과 같은 툴을 사용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost` 6379 포트에서 접근 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `compose.yaml` 파일에 [Valkey](https://valkey.io/) 컨테이너가 추가됩니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용합니다. 애플리케이션 내에서 컨테이너에 연결하려면, `.env` 파일의 `REDIS_HOST`를 `valkey`로 설정하세요.

Valkey에 로컬 PC에서 접속하려면, 역시 [TablePlus](https://tableplus.com)와 같은 툴을 사용할 수 있습니다. 기본적으로 Valkey 데이터베이스도 `localhost` 6379 포트에서 접근할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, `compose.yaml` 파일에 이 강력한 검색 엔진이 추가됩니다. [Laravel Scout](/docs/12.x/scout)와 쉽게 통합됩니다. 컨테이너가 실행된 후에는, `.env` 파일에 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정하여 애플리케이션에서 Meilisearch에 연결할 수 있습니다.

로컬 PC에서는 `http://localhost:7700` 웹브라우저를 통해 Meilisearch의 웹 관리 콘솔에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `compose.yaml` 파일에 이 초고속 오픈소스 검색 엔진 항목이 추가됩니다. [Laravel Scout](/docs/12.x/scout#typesense)와 기본적으로 연동됩니다. 컨테이너가 실행 중이면, 다음 환경 변수를 설정해 Typesense에 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 PC에서는 `http://localhost:8108`를 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 저장소 (File Storage)

프로덕션 환경에서 Amazon S3를 파일 저장소로 사용하려는 경우, Sail 설치 시 [MinIO](https://min.io) 서비스를 설치하면 유용합니다. MinIO는 S3와 호환되는 API를 제공하므로, 프로덕션 S3 환경에 테스트용 버킷을 생성하지 않고도 로컬에서 Laravel의 `s3` 파일 저장 드라이버로 개발 및 테스트할 수 있습니다. MinIO 설치 시, 애플리케이션의 `compose.yaml` 파일에 관련 설정이 자동으로 추가됩니다.

기본적으로, 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크를 Amazon S3뿐만 아니라, MinIO와 같은 S3 호환 저장 서비스에도 사용할 수 있습니다. 이를 위해 관련 환경 변수만 조정하면 됩니다. 예를 들어 MinIO 사용 시 환경 변수는 다음과 같이 설정하세요:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 통합에서 올바른 URL이 만들어지도록 하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷명을 포함하도록 추가로 설정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 `http://localhost:8900`에서 사용할 수 있으며, 기본 사용자명은 `sail`, 기본 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시, `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 강력한 테스트 지원을 제공합니다. Sail의 `test` 명령을 사용해 애플리케이션의 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있습니다. Pest/PHPUnit이 지원하는 모든 CLI 옵션도 `test` 명령에 동일하게 사용할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령은 실제로 `test` Artisan 명령어를 실행하는 것과 같습니다:

```shell
sail artisan test
```

기본적으로 Sail은 전용 `testing` 데이터베이스를 생성해, 테스트가 기존 데이터베이스에 영향을 주지 않도록 합니다. Laravel의 기본 설치에서는, Sail이 `phpunit.xml` 파일을 자동으로 이 데이터베이스를 사용하도록 설정합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 직관적이고 사용이 편리한 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium 등 별도 툴을 직접 설치하지 않고도 이러한 테스트를 실행할 수 있습니다. 먼저, 애플리케이션의 `compose.yaml` 파일에서 Selenium 관련 주석을 해제하세요:

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

다음으로, 애플리케이션의 `laravel.test` 서비스에 `selenium`에 대한 `depends_on` 항목이 포함되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로 Sail을 실행한 뒤, `dusk` 명령으로 Dusk 테스트를 수행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용

Apple Silicon 칩이 탑재된 Mac에서는, `selenium` 서비스 이미지로 `selenium/standalone-chromium`을 사용해야 합니다:

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

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 개발 중 애플리케이션에서 발송되는 이메일을 가로채어 웹 인터페이스에서 쉽게 미리볼 수 있게 해줍니다. Sail 이용 시 Mailpit의 기본 호스트명은 `mailpit`이며, 포트는 1025번을 사용합니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, 웹 브라우저에서 http://localhost:8025로 접속하면 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

때로는 애플리케이션 컨테이너 내부에서 Bash 세션을 시작해 파일이나 설치된 서비스 상태를 직접 확인하거나 임의의 셸 명령을 실행해야 할 수 있습니다. 이럴 때는 `shell` 명령을 사용해 애플리케이션 컨테이너에 접속할 수 있습니다:

```shell
sail shell

sail root-shell
```

[Laraavel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령을 실행하면 됩니다:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0을 이용해 애플리케이션을 실행할 수 있습니다. 기본적으로 PHP 8.4가 사용됩니다. 애플리케이션에 사용할 PHP 버전을 변경하려면 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 항목을 아래와 같이 수정하세요:

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

또한 사용 중인 PHP 버전을 이미지 이름에 반영하고 싶다면, `compose.yaml` 파일의 `image` 항목을 함께 수정하세요:

```yaml
image: sail-8.2/app
```

설정 변경 후, 컨테이너 이미지를 반드시 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22 버전을 설치합니다. 빌드 시 설치될 Node 버전을 변경하고 싶다면, `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 정의를 다음과 같이 설정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

설정 후 Sail 컨테이너 이미지를 반드시 재빌드해야 적용됩니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

동료와 사이트를 빠르게 미리 공유하거나 웹훅 등 외부 연동 테스트가 필요할 때가 있습니다. 이럴 때는 `share` 명령을 사용하세요. 실행하면 무작위의 `laravel-sail.site` 도메인이 발급되며, 이를 통해 외부에서 애플리케이션에 접속할 수 있습니다:

```shell
sail share
```

사이트를 공유할 때는, URL 생성 헬퍼(`url`, `route` 등)가 올바른 HTTP 호스트를 인식할 수 있도록 애플리케이션의 `bootstrap/app.php` 파일에서 trusted proxies를 반드시 아래와 같이 설정해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

특정 서브도메인으로 공유 URL을 지정하고 싶다면 실행 시 `subdomain` 옵션을 추가하세요:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> 이 `share` 명령은 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 작동합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. 먼저 [Sail 설정을 배포](#sail-customization)한 다음, Xdebug를 활성화할 환경변수를 애플리케이션의 `.env` 파일에 추가하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그 다음, 배포된 `php.ini` 파일에도 다음 설정이 포함되어야 Xdebug가 올바른 모드로 활성화됩니다:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일 변경 이후, 해당 변경 사항이 적용되도록 Docker 이미지를 반드시 재빌드하세요:

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

기본적으로 내부의 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 설정되어 있어 Mac과 Windows(WSL2)에서 Xdebug를 자동으로 지원합니다. 만약 사용하는 리눅스가 Docker 20.10 이상이라면 별도의 설정이 필요하지 않습니다.

하지만 20.10 미만 Docker를 사용하는 리눅스 환경에서는 `host.docker.internal`이 지원되지 않으므로, 직접 고정 IP를 지정해야 합니다. 이를 위해 `compose.yaml` 파일에서 커스텀 네트워크를 아래와 같이 정의하세요:

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

그런 다음, `.env` 파일에 `SAIL_XDEBUG_CONFIG` 변수를 다음과 같이 설정하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용 (Xdebug CLI Usage)

`artisan` 명령어 실행 시 디버그 세션을 시작하려면 `sail debug` 명령어를 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug로 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용 (Xdebug Browser Usage)

웹 브라우저에서 애플리케이션을 직접 사용하면서 디버깅하려면, [Xdebug에서 제공하는 가이드](https://xdebug.org/docs/step_debug#web-application)를 참고해 브라우저에서 Xdebug 세션을 시작하세요.

PhpStorm 사용자는 [제로-구성 디버깅 문서](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)도 참고하면 도움이 됩니다.

> [!WARNING]
> Laravel Sail은 `artisan serve`를 통해 애플리케이션을 서비스합니다. `artisan serve` 명령은 Laravel 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수만 지원합니다. Laravel 8.52.0 이하 버전에서는 지원하지 않으므로 디버그 연결이 동작하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 결국 Docker이기 때문에, 거의 모든 부분을 자유롭게 커스터마이징할 수 있습니다. Sail의 Dockerfile 등 자체 설정 파일을 원한다면, 아래 명령을 실행하여 배포할 수 있습니다:

```shell
sail artisan sail:publish
```

이 명령을 실행하면 Laravel Sail에서 사용하는 Dockerfile 및 기타 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 저장됩니다. Sail 설치 후 커스터마이징을 진행했다면, 애플리케이션 컨테이너의 이미지를 별도의 이름으로 변경할 수 있으며, 이후 `build` 명령으로 컨테이너 이미지를 재빌드해야 합니다. 여러 Laravel 애플리케이션을 한 PC에서 함께 개발할 때 특히 개별 이미지 이름을 사용하는 것이 중요합니다:

```shell
sail build --no-cache
```