# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드하기](#rebuilding-sail-images)
    - [쉘 별칭 설정하기](#configuring-a-shell-alias)
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
- [파일 저장](#file-storage)
- [테스트 실행하기](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [이메일 미리보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유하기](#sharing-your-site)
- [Xdebug 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 가벼운 커맨드라인 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용해 Laravel 애플리케이션을 손쉽게 시작할 수 있는 훌륭한 출발점입니다.

Sail의 핵심은 프로젝트 루트에 저장된 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 상호작용할 수 있는 편리한 명령줄 도구입니다.

Laravel Sail은 macOS, Linux, Windows(WSL2를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 새로 생성한 모든 Laravel 애플리케이션에 자동으로 설치되므로, 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에서 Sail을 사용하려면 Composer 패키지 매니저를 통해 Sail을 설치하면 됩니다. 단, 기존 로컬 개발 환경에서 Composer 의존성 설치가 가능하다는 전제입니다:

```shell
composer require laravel/sail --dev
```

Sail 설치가 완료되면 `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 배포하고, Docker 서비스에 연결하는 데 필요한 환경 변수를 `.env` 파일에 추가합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법을 계속 배우려면 이 문서의 나머지 부분을 계속 읽어주세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux에서 Docker Desktop을 사용한다면, 다음 명령어로 `default` Docker 컨텍스트를 사용하도록 설정해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치하기 (Adding Additional Services)

기존 Sail 설치에 서비스를 추가하고 싶다면, `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 이용하기 (Using Devcontainers)

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가해 실행하세요. 이 옵션은 기본 `.devcontainer/devcontainer.json` 파일을 애플리케이션 루트에 배포합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기 (Rebuilding Sail Images)

가끔 Sail 이미지의 모든 패키지와 소프트웨어를 최신 상태로 완전히 재빌드하고 싶을 수 있습니다. 다음 명령어로 실행할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 쉘 별칭 설정하기 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 실행합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`를 입력하는 대신, 아래와 같은 쉘 별칭을 설정하면 더 쉽게 명령어를 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있게 하려면, 홈 디렉토리의 쉘 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가한 뒤 쉘을 재시작하세요.

별칭 설정 후에는 `sail`만 입력해 Sail 명령어를 실행할 수 있습니다. 이 문서의 나머지 예제는 별칭이 설정되었다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일은 함께 작동하는 다양한 Docker 컨테이너를 정의합니다. 이 컨테이너들은 모두 `docker-compose.yml`의 `services` 설정 내에 있습니다. `laravel.test` 컨테이너는 애플리케이션을 서비스하는 주 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중인지 확인하세요. 애플리케이션의 `docker-compose.yml` 파일에 정의된 모든 컨테이너를 시작하려면 `up` 명령어를 실행하세요:

```shell
sail up
```

백그라운드에서 컨테이너를 실행하고 싶다면 "detached" 모드로 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너가 실행된 후, 웹 브라우저에서 http://localhost 에서 프로젝트에 접속할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C를 누르거나, 백그라운드 실행 중인 경우 `stop` 명령어를 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail을 사용하면 애플리케이션은 Docker 컨테이너 내에서 실행되어 로컬 컴퓨터와 격리됩니다. 하지만 Sail은 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어 등 다양한 명령어를 애플리케이션 내에서 편리하게 실행할 수 있는 방법을 제공합니다.

**Laravel 문서에서 Composer, Artisan, Node / NPM 명령어는 종종 Sail을 언급하지 않고 소개됩니다.** 해당 예제들은 해당 툴들이 로컬 컴퓨터에 설치되었다고 가정한 것입니다. Sail을 로컬 개발 환경으로 사용한다면, 이러한 명령어는 반드시 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기 (Executing PHP Commands)

PHP 명령어는 `php` 명령어로 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Sail에서 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기 (Executing Composer Commands)

Composer 명령어는 `composer` 명령어를 사용해 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행하기 (Executing Artisan Commands)

Laravel Artisan 명령어는 `artisan` 명령어로 실행합니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행하기 (Executing Node / NPM Commands)

Node 명령어는 `node` 명령어로, NPM 명령어는 `npm` 명령어로 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

필요하면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 컨테이너가 중지되거나 재시작 되어도 데이터가 유지됩니다.

처음 MySQL 컨테이너가 시작될 때, 두 개의 데이터베이스가 자동 생성됩니다. 첫 번째는 `DB_DATABASE` 환경 변수 값을 사용하는 개발용 데이터베이스이고, 두 번째는 `testing`이라는 테스트 전용 데이터베이스로, 테스트가 개발 데이터에 영향을 끼치지 않도록 분리합니다.

컨테이너가 실행된 후, 애플리케이션 내에서 MySQL에 연결하려면 `.env` 파일의 `DB_HOST` 값을 `mysql`로 설정하세요.

로컬 컴퓨터에서 MySQL에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 툴을 사용할 수 있습니다. 기본 MySQL 접속 정보는 `localhost`의 3306번 포트이며, 로그인 정보는 `.env`의 `DB_USERNAME`과 `DB_PASSWORD` 값을 따릅니다. 또는 `root` 사용자로 접속할 수도 있으며 이 경우에도 비밀번호는 `DB_PASSWORD` 값입니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택하면, 애플리케이션의 `docker-compose.yml`에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 포함됩니다. 이 컨테이너는 Atlas 기능인 [검색 인덱스](https://www.mongodb.com/docs/atlas/atlas-search/)를 제공하는 문서형 데이터베이스입니다. 데이터는 Docker 볼륨을 통해 컨테이너 중지 시에도 유지됩니다.

컨테이너 실행 후, 애플리케이션 내 `.env` 파일의 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하세요. 인증은 기본적으로 비활성화 되어 있지만, `MONGODB_USERNAME`, `MONGODB_PASSWORD` 환경 변수를 설정해 인증을 활성화할 수 있습니다. 인증을 활성화했다면 연결 문자열에 인증 정보를 추가하세요:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와의 원활한 통합을 위해 [MongoDB 공식 Laravel 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬에서 MongoDB에 접속하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI 툴을 사용할 수 있습니다. 기본 접속 정보는 `localhost`의 27017번 포트입니다.

<a name="redis"></a>
### Redis

`docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너 역시 데이터 유지를 위해 Docker 볼륨을 사용합니다. 컨테이너가 시작되면 `.env` 파일의 `REDIS_HOST` 값을 `redis`로 설정해 애플리케이션에서 Redis에 연결하세요.

로컬에서 Redis에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 툴을 사용할 수 있으며, 기본적으로 `localhost`의 6379번 포트에 접속 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 설치했다면, `docker-compose.yml` 파일에 [Valkey](https://valkey.io/) 컨테이너가 포함됩니다. 이 컨테이너도 Docker 볼륨을 사용하여 데이터를 유지합니다. 애플리케이션 내 `.env`의 `REDIS_HOST` 값을 `valkey`로 설정하여 Valkey에 연결할 수 있습니다.

로컬에서 Valkey에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 툴을 사용할 수 있으며, 기본적으로 `localhost`의 6379번 포트를 통해 접속 가능합니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면, 애플리케이션의 `docker-compose.yml`에 Laravel Scout과 통합된 강력한 검색 엔진 Meilisearch가 포함됩니다. 컨테이너 시작 후, `.env` 파일의 `MEILISEARCH_HOST`를 `http://meilisearch:7700`으로 설정해 연결하세요.

로컬에서 Meilisearch 웹 관리 패널에 접속하려면 웹 브라우저에서 http://localhost:7700 을 방문하면 됩니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택하면, Laravel Scout와 기본 통합된 초고속 오픈소스 검색 엔진 Typesense가 `docker-compose.yml`에 포함됩니다. 컨테이너 시작 후 다음 환경 변수를 `.env` 파일에 설정하세요:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬에서 Typesense API는 http://localhost:8108 을 통해 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 저장 (File Storage)

프로덕션 환경에서 Amazon S3를 사용해 파일을 저장하려면, Sail 설치 시 [MinIO](https://min.io) 서비스를 추가하는 것이 좋습니다. MinIO는 S3 호환 API를 제공해 로컬 개발환경에서 Laravel의 `s3` 파일 저장 드라이버를 사용하며 테스트용 S3 버킷을 프로덕션에 생성하지 않아도 됩니다. MinIO 서비스를 설치하면 `docker-compose.yml`에 MinIO 설정이 추가됩니다.

기본적으로 `filesystems` 구성 파일에는 이미 `s3` 디스크 설정이 포함되어 있습니다. MinIO처럼 S3 호환 파일 저장소를 사용하려면 환경변수를 적절히 수정하세요. 예를 들어 MinIO 사용 시 환경변수는 아래와 같습니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel Flysystem이 올바른 URL을 생성하려면 `AWS_URL` 환경변수에 애플리케이션 로컬 URL과 버킷명을 포함한 값을 지정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

버킷은 MinIO 콘솔(http://localhost:8900)에서 생성할 수 있으며, 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 저장 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

Laravel은 기본적으로 강력한 테스트 지원을 제공합니다. Sail의 `test` 명령어를 사용해 애플리케이션의 [기능 및 단위 테스트](/docs/master/testing)를 실행할 수 있습니다. Pest 또는 PHPUnit에서 지원하는 모든 CLI 옵션도 `test` 명령어에 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 Artisan의 `test` 명령어와 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 테스트가 현재 데이터베이스 상태에 영향을 주지 않도록 `testing` 데이터베이스를 별도로 생성합니다. 기본 Laravel 설치에서는 `phpunit.xml` 파일도 테스트 실행 시 이 데이터베이스를 사용하도록 설정합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/master/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium 등 별도의 도구 설치 없이 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `docker-compose.yml`에서 Selenium 서비스를 주석 해제하세요:

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

다음으로, `laravel.test` 서비스의 `docker-compose.yml` 파일에 `selenium`이 `depends_on` 항목에 포함되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이후 Sail을 시작하고 `dusk` 명령어로 테스트를 실행하면 됩니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon용 Selenium

로컬 머신이 Apple Silicon 칩을 사용하는 경우, `selenium` 서비스는 `selenium/standalone-chromium` 이미지를 사용해야 합니다:

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

Laravel Sail의 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 보내는 이메일을 가로채 미리보기할 수 있는 웹 인터페이스를 제공합니다. Sail 이용 시 Mailpit의 기본 호스트는 `mailpit`이며 1025번 포트를 사용합니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, 웹 브라우저에서 http://localhost:8025 로 접속하면 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너 내에서 Bash 세션을 시작하고 싶다면, `shell` 명령어를 이용할 수 있습니다. 이를 통해 컨테이너 내부 파일과 설치된 서비스를 확인하거나 임의의 쉘 명령어를 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

또한 새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 실행하려면 `tinker` 명령어를 사용하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전을 지원합니다. 기본 PHP 버전은 8.4입니다. 애플리케이션에 사용될 PHP 버전을 변경하려면, `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 설정 내 경로를 수정하세요:

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

뿐만 아니라 사용 중인 PHP 버전을 이미지 이름에 반영하려면, `docker-compose.yml` 파일의 `image` 이름도 수정하세요:

```yaml
image: sail-8.2/app
```

수정 후 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 20을 설치합니다. 이미지 빌드 시 설치할 Node 버전을 변경하려면, `docker-compose.yml` 파일에서 `laravel.test` 서비스의 `build.args` 내 `NODE_VERSION` 값을 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

수정 후, 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나 웹훅 연동 테스트를 위해 공개적으로 사이트를 공유해야 할 때가 있습니다. `share` 명령어를 사용하면 무작위로 생성된 `laravel-sail.site` URL을 통해 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

사이트 공유 시, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용해 신뢰할 수 있는 프록시를 적절히 설정해야 합니다. 설정하지 않으면 `url`, `route` 같은 URL 생성 헬퍼가 올바른 HTTP 호스트를 판단하지 못합니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 하위 도메인을 직접 지정하고 싶다면 `share` 명령어에 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)가 제공하는 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 PHP용 강력한 디버거인 [Xdebug](https://xdebug.org/)가 포함되어 있습니다. Xdebug를 활성화하려면, 우선 [Sail 설정 파일을 퍼블리시](#sail-customization)하세요. 그 다음 애플리케이션 `.env` 파일에 아래 변수를 추가해 설정합니다:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고 퍼블리시한 `php.ini` 파일에 아래 설정이 포함되어 있는지 확인하여 지정한 모드로 Xdebug가 활성화되도록 하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정한 후에는 변경 사항이 반영되도록 Docker 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 설정돼 Mac과 Windows(WSL2)에서 Xdebug가 올바르게 동작합니다. Linux에서 Docker 20.10 이상을 사용 중이라면 `host.docker.internal`이 지원되므로 별도 설정이 필요 없습니다.

그러나 Docker 버전이 20.10 미만이라면 Linux에서 `host.docker.internal`이 지원되지 않아 직접 호스트 IP를 설정해야 합니다. 이를 위해 `docker-compose.yml`에서 사용자 정의 네트워크를 정의하고 컨테이너에 고정 IP를 할당하세요:

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

고정 IP를 설정한 후, 애플리케이션 `.env` 파일에서 `SAIL_XDEBUG_CONFIG` 변수를 다음과 같이 정의하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

Artisan 명령어를 실행할 때 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용하세요:

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저로 애플리케이션과 상호작용하면서 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)에 나와있는 브라우저에서 Xdebug 세션을 시작하는 방법을 참고하세요.

PhpStorm을 사용한다면, JetBrains의 [제로 설정 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 문서를 참고하시기 바랍니다.

> [!WARNING]
> Laravel Sail은 애플리케이션을 `artisan serve`를 통해 서비스합니다. `artisan serve` 명령어는 Laravel 8.53.0 버전부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하 버전에서는 이 변수를 지원하지 않아 디버그 연결이 동작하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 기반이므로, 거의 모든 부분을 자유롭게 커스터마이징할 수 있습니다. Sail의 Dockerfile과 설정 파일을 퍼블리시하려면 `sail:publish` 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

이 명령어 실행 후, Laravel Sail에서 사용하는 Dockerfile과 설정 파일들이 애플리케이션 루트의 `docker` 디렉토리에 복사됩니다. 커스터마이징 후에는 `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름을 변경할 수 있습니다. 그리고 변경 사항을 반영하려면 반드시 컨테이너 이미지를 재빌드하세요. 여러 Laravel 애플리케이션을 한 머신에서 Sail로 개발한다면 각 애플리케이션에 고유한 이미지 이름을 부여하는 것이 중요합니다:

```shell
sail build --no-cache
```