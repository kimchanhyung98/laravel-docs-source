# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드하기](#rebuilding-sail-images)
    - [셸 별칭 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령 실행하기](#executing-sail-commands)
    - [PHP 명령 실행하기](#executing-php-commands)
    - [Composer 명령 실행하기](#executing-composer-commands)
    - [Artisan 명령 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령 실행하기](#executing-node-npm-commands)
- [데이터베이스와 상호작용하기](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [파일 스토리지](#file-storage)
- [테스트 실행하기](#running-tests)
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

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 경량 명령줄 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용해 Laravel 애플리케이션을 쉽게 시작할 수 있는 좋은 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows(WSL2를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새 Laravel 애플리케이션에 자동으로 설치되어 즉시 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에서 Sail을 사용하고 싶다면 Composer 패키지 관리자를 통해 Sail을 설치할 수 있습니다. 물론 이 방법은 기존 개발 환경이 Composer 의존성을 설치할 수 있는 조건을 전제로 합니다:

```shell
composer require laravel/sail --dev
```

Sail이 설치된 후에는 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트로 퍼블리시하고, Docker 서비스와 연결하기 위해 필요한 환경 변수들을 `.env` 파일에 추가합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용 방법을 계속 배우려면 이 문서의 나머지 부분을 읽어주세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용 중이라면 다음 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 추가 서비스를 넣고 싶다면 `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainers 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 내에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json` 파일을 애플리케이션 루트에 게시하도록 지시합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기 (Rebuilding Sail Images)

때때로 Sail 이미지 내의 모든 패키지와 소프트웨어가 최신 상태인지 확인하기 위해 이미지를 완전히 재빌드하고 싶을 수 있습니다. 다음 명령어로 할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 설정하기 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 새 Laravel 애플리케이션과 함께 포함되는 `vendor/bin/sail` 스크립트를 통해 실행합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 대신, 셸 별칭을 설정해 더 쉽게 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있도록 홈 디렉터리 내의 셸 설정 파일(`~/.zshrc` 또는 `~/.bashrc`)에 추가한 후 셸을 재시작하세요.

별칭 설정 후에는 단순히 `sail`만 입력해 Sail 명령어를 실행할 수 있습니다. 이후 예제에서 이 별칭을 사용한다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션을 빌드하는 데 도움을 주는 다양한 Docker 컨테이너들을 정의하고 있습니다. 이 컨테이너들은 `docker-compose.yml` 내 `services` 설정의 각 항목으로 구성됩니다. `laravel.test` 컨테이너는 애플리케이션을 서비스하는 주요 컨테이너입니다.

Sail을 시작하기 전에 로컬에서 실행 중인 다른 웹 서버나 데이터베이스가 없는지 확인해야 합니다. 애플리케이션 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령을 실행하세요:

```shell
sail up
```

백그라운드에서 컨테이너를 실행하려면 'detached' 모드로 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너가 시작되면 웹 브라우저에서 http://localhost 로 프로젝트에 접근할 수 있습니다.

모든 컨테이너를 중지하려면 실행 중인 터미널에서 Control + C를 눌러 실행을 멈추거나, 백그라운드 실행 중이라면 `stop` 명령을 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령 실행하기 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되어 로컬 컴퓨터와 격리됩니다. 하지만 Sail은 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어를 손쉽게 실행할 방법을 제공합니다.

**Laravel 문서를 읽다 보면 종종 Sail을 언급하지 않은 Composer, Artisan, Node / NPM 명령어 예시를 보게 됩니다.** 이 예시들은 로컬 컴퓨터에 해당 도구들이 설치된 상태를 가정합니다. Sail을 로컬 Laravel 개발 환경으로 사용할 때는 명령어를 반드시 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행하기...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령 실행하기...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령 실행하기 (Executing PHP Commands)

`php` 명령어를 사용하여 PHP 명령을 실행할 수 있습니다. 물론, 이 명령들은 애플리케이션에 설정된 PHP 버전으로 실행됩니다. Laravel Sail에서 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령 실행하기 (Executing Composer Commands)

`composer` 명령어를 통해 Composer 명령 실행이 가능합니다. Laravel Sail 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령 실행하기 (Executing Artisan Commands)

Laravel Artisan 명령은 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령 실행하기 (Executing Node / NPM Commands)

`node` 명령으로 Node 명령을 실행하고, `npm` 명령으로 NPM 명령을 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

필요하다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 컨테이너가 중지되거나 재시작되어도 유지되도록 합니다.

또한, MySQL 컨테이너가 처음 시작되면 두 개의 데이터베이스를 생성합니다. 첫 번째는 `DB_DATABASE` 환경 변수 값을 사용한 개발용 데이터베이스이며, 두 번째는 `testing`이라는 별도의 테스트용 데이터베이스로, 테스트 실행 시 개발 데이터를 방해하지 않도록 해줍니다.

컨테이너가 시작된 후 애플리케이션 내에서 MySQL 인스턴스에 연결하려면 `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 설정하세요.

로컬 컴퓨터에서 MySQL에 연결하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL은 `localhost`의 3306 포트에서 접근 가능하며, 인증 정보는 `.env` 파일의 `DB_USERNAME`과 `DB_PASSWORD` 값을 이용합니다. 또는 `root` 사용자로 연결할 수도 있는데 이때도 `DB_PASSWORD` 값이 비밀번호로 사용됩니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `docker-compose.yml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 포함됩니다. 이는 Atlas 기능(예: [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/))을 갖춘 MongoDB 도큐먼트 데이터베이스입니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터의 지속성을 보장합니다.

컨테이너 시작 후에는 애플리케이션 `.env` 파일의 `MONGODB_URI`를 `mongodb://mongodb:27017`로 설정해 MongoDB 인스턴스에 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있지만, 컨테이너 시작 전에 `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정해 인증을 활성화할 수 있습니다. 이 경우 연결 문자열에 인증 정보를 포함해야 합니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 원활히 통합하려면 [MongoDB 공식 Laravel 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬에서 MongoDB 데이터베이스에 연결하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI 도구 사용을 권장합니다. 기본적으로 `localhost`의 27017 포트에서 접근 가능합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml`에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)으로 데이터가 유지됩니다. 컨테이너를 시작한 후에는 애플리케이션 `.env` 파일 내 `REDIS_HOST`를 `redis`로 설정해 Redis에 연결할 수 있습니다.

로컬 머신에서는 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 앱을 통해 접속할 수 있습니다. 기본적으로 `localhost` 6379 포트에서 접근 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `docker-compose.yml`에 [Valkey](https://valkey.io/) 컨테이너 항목이 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터 지속성을 보장합니다. 애플리케이션에서는 `.env` 파일 내 `REDIS_HOST`를 `valkey`로 설정하여 접속할 수 있습니다.

로컬 머신에서는 [TablePlus](https://tableplus.com) 같은 데이터베이스 관리 앱을 통해 접속할 수 있으며, 기본값으로는 `localhost` 6379 포트를 사용합니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면 `docker-compose.yml` 파일에 Laravel Scout와 통합된 강력한 검색 엔진인 Meilisearch 항목이 포함됩니다. 컨테이너를 시작한 후에는 `.env` 파일에 `MEILISEARCH_HOST`를 `http://meilisearch:7700`으로 설정해 연결할 수 있습니다.

로컬 머신 웹 브라우저에서 `http://localhost:7700`에 접속하면 Meilisearch의 웹 기반 관리자 패널을 사용 가능합니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택하면 `docker-compose.yml` 파일에 [Laravel Scout](/docs/12.x/scout#typesense)과 기본 통합된 고속 오픈소스 검색 엔진인 Typesense 항목이 포함됩니다. 컨테이너를 시작한 후 `.env` 파일에 다음 환경 변수를 설정해 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서는 `http://localhost:8108`를 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 Amazon S3로 파일을 저장할 계획이라면, 로컬 개발 시 [MinIO](https://min.io) 서비스를 설치하는 것이 좋습니다. MinIO는 S3 호환 API를 제공하여, 실제 프로덕션 S3 버킷을 생성하지 않고도 Laravel의 `s3` 파일 스토리지 드라이버를 사용해 로컬에서 개발할 수 있게 해줍니다. Sail 설치 중 MinIO를 선택하면 애플리케이션의 `docker-compose.yml`에 MinIO 설정이 추가됩니다.

기본적으로 애플리케이션 `filesystems` 설정 파일에 `s3` 디스크 구성이 이미 들어있으며, 이 디스크는 Amazon S3뿐 아니라 MinIO 같은 S3 호환 스토리지 서비스와도 연결할 수 있습니다. 환경 변수에서 해당 서비스에 맞게 설정값을 수정하면 됩니다. 예를 들어 MinIO 사용 시 `FILESYSTEM_DISK`와 관련된 환경 변수는 다음과 같이 설정할 수 있습니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Flysystem 통합이 URL을 적절히 생성하도록 하려면 `AWS_URL` 변수에 애플리케이션 로컬 URL과 버킷 이름을 포함해 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

버킷 생성은 `http://localhost:8900`에서 접속 가능한 MinIO 콘솔에서 할 수 있습니다. MinIO 콘솔 기본 사용자명은 `sail`이며 기본 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 저장 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

Laravel은 훌륭한 기본 테스트 지원을 제공하며, Sail의 `test` 명령어로 애플리케이션의 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있습니다. Pest 또는 PHPUnit에서 지원하는 CLI 옵션들도 이 명령어에 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어와 같습니다:

```shell
sail artisan test
```

기본적으로, Sail은 테스트가 개발 중인 데이터베이스 상태에 영향을 주지 않도록 별도의 `testing` 데이터베이스를 생성합니다. 기본 Laravel 설치에서는 `phpunit.xml` 파일도 이 테스트 데이터베이스를 사용하도록 설정됩니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API입니다. Sail 덕분에 로컬 컴퓨터에 Selenium 등을 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

다음으로 `laravel.test` 서비스에 `selenium`이 `depends_on`에 포함되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로, Sail을 실행하여 Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon 환경의 Selenium

Apple Silicon 칩이 탑재된 로컬 머신에서는 `selenium` 서비스에 `selenium/standalone-chromium` 이미지를 사용해야 합니다:

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

Laravel Sail의 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 발송한 이메일을 가로채 웹 인터페이스로 편리하게 미리볼 수 있도록 합니다. Sail 사용 시 Mailpit 기본 호스트는 `mailpit`, 기본 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, 웹 브라우저에서 Mailpit 인터페이스를 다음 URL에서 접근할 수 있습니다: http://localhost:8025

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너 내에서 Bash 세션을 시작하려면 `shell` 명령어를 사용할 수 있습니다. 이를 통해 컨테이너의 파일과 설치된 서비스를 살펴보고 임의의 쉘 명령어를 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작할 때는 `tinker` 명령어를 사용하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전을 지원합니다. 기본 PHP 버전은 PHP 8.4입니다. 프로젝트에서 사용되는 PHP 버전을 변경하려면 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 컨테이너의 `build` 정의를 업데이트하세요:

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

또한, 사용 중인 PHP 버전에 맞게 `image` 이름도 수정할 수 있습니다. 이 역시 `docker-compose.yml` 파일에서 설정합니다:

```yaml
image: sail-8.2/app
```

설정을 변경한 후에는 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 이미지 빌드 시 설치할 Node 버전을 변경하려면 `docker-compose.yml` 파일 내 `laravel.test` 서비스의 `build.args`를 다음과 같이 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

설정 변경 후에는 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료와 사이트를 미리보거나 애플리케이션과 웹훅 연동 테스트를 위해 사이트를 공개해야 할 때가 있습니다. 이럴 때는 `share` 명령어를 사용하세요. 실행하면 임의의 `laravel-sail.site` 서브도메인 URL이 부여되어 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령어를 사용할 때는 애플리케이션 `bootstrap/app.php` 파일 내 `trustProxies` 미들웨어 메서드를 통해 신뢰할 프록시를 설정해야 합니다. 그렇지 않으면 `url`이나 `route` 같은 URL 생성 헬퍼가 올바른 HTTP 호스트를 인식하지 못할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 서브도메인을 직접 지정하려면 `share` 명령어 실행 시 `subdomain` 옵션을 사용하세요:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 인기 있고 강력한 PHP 디버거인 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면 먼저 [Sail 설정을 퍼블리시](#sail-customization)해야 합니다. 이후 애플리케이션 `.env` 파일에 다음 변수를 추가해 Xdebug를 구성하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

퍼블리시된 `php.ini` 파일에 다음 설정이 포함되어 있는지 확인하여 지정한 모드로 Xdebug가 활성화되도록 합니다:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 변경 후 Docker 이미지를 재빌드하여 변경 사항을 반영하세요:

```shell
sail build --no-cache
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 Mac과 Windows(WSL2)를 위해 `client_host=host.docker.internal`로 정의되어 있습니다. 만약 로컬 머신이 Linux이고 Docker 20.10 이상을 사용한다면 `host.docker.internal`이 존재하여 별도 설정이 필요 없습니다.

Docker 버전이 20.10 미만인 Linux에서는 `host.docker.internal`을 지원하지 않으므로 수동으로 호스트 IP를 지정해야 합니다. 이를 위해 `docker-compose.yml`에서 커스텀 네트워크를 정의하고 컨테이너에 고정 IP를 부여하세요:

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

고정 IP 설정 후 `.env` 파일에 아래 변수를 추가해 주세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

`artisan` 명령어 실행 시 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면 [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)의 지침을 따라 브라우저에서 Xdebug 세션을 시작해야 합니다.

PhpStorm을 사용한다면 JetBrains에서 제공하는 [제로-설정 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 문서를 참고하세요.

> [!WARNING]
> Laravel Sail은 `artisan serve`로 애플리케이션을 제공합니다. `artisan serve` 명령어는 Laravel 8.53.0 버전부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 그 이하 버전(8.52.0 및 이전)은 이 변수들을 지원하지 않아 디버그 연결을 받을 수 없습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 단지 Docker일 뿐이므로 거의 모든 것을 자유롭게 커스터마이징할 수 있습니다. Sail의 Dockerfile 등을 퍼블리시하려면 다음 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

이 명령어를 실행하면 Laravel Sail이 사용하는 Dockerfile과 기타 설정 파일이 애플리케이션 루트의 `docker` 디렉터리에 배치됩니다. Sail 설치를 커스터마이징한 후에는 `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름을 변경할 수 있습니다. 특히 한 컴퓨터에서 여러 Laravel 애플리케이션을 개발 중이라면 이미지 이름을 고유하게 설정하는 것이 중요합니다.

변경 후 컨테이너를 다시 빌드할 때는 다음 명령어를 사용하세요:

```shell
sail build --no-cache
```