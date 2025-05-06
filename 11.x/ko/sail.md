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
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
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
- [Xdebug를 이용한 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개

[Laravel Sail](https://github.com/laravel/sail)은 라라벨의 기본 도커 개발 환경과 상호작용하기 위한 경량 명령줄 인터페이스입니다. Sail은 도커에 대한 사전 경험 없이도 PHP, MySQL, Redis를 활용한 라라벨 애플리케이션을 쉽고 빠르게 시작할 수 있는 훌륭한 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 도커 컨테이너와 편리하게 상호작용할 수 있는 CLI 명령을 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 경유)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 신규 라라벨 애플리케이션에 자동으로 설치되므로, 즉시 사용할 수 있습니다. 새로운 라라벨 애플리케이션 생성 방법은 운영체제에 맞는 라라벨의 [설치 문서](/docs/{{version}}/installation#docker-installation-using-sail)를 참고하세요. 설치 중 자신의 애플리케이션에서 사용할 Sail 지원 서비스 선택을 요청받게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 라라벨 애플리케이션에 Sail을 사용하고 싶다면 Composer 패키지 매니저를 이용하여 Sail을 설치할 수 있습니다. 물론, 아래 단계는 현재 개발 환경에서 Composer 의존성 패키지 설치가 가능함을 전제로 합니다:

```shell
composer require laravel/sail --dev
```

Sail 설치 후, `sail:install` Artisan 명령어를 실행하세요. 이 명령은 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 배포하고, Docker 서비스 접속에 필요한 환경 변수로 `.env` 파일을 자동으로 수정해줍니다:

```shell
php artisan sail:install
```

마지막으로, Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 배우고 싶다면 아래 문서를 계속 참고하세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> Linux용 Docker Desktop을 사용하는 경우, 반드시 다음 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 새로운 서비스를 추가하려면 `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면 `sail:install` 명령에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 생성합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기

가끔 모든 이미지의 패키지와 소프트웨어가 최신 상태인지 확인하기 위해 Sail 이미지를 완전히 재빌드해야 할 때가 있습니다. `build` 명령을 사용하여 이를 수행할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 설정하기

기본적으로 Sail 명령은 모든 신규 라라벨 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 호출합니다:

```shell
./vendor/bin/sail up
```

하지만 Sail 명령을 반복해서 입력하는 대신, 셸 별칭(alias)을 설정해 좀 더 쉽고 빠르게 Sail 명령을 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

항상 사용할 수 있도록 이 별칭을 홈 디렉터리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가한 후 셸을 재시작하세요.

셸 별칭을 설정하면 이제 단순히 `sail`만 입력하여 Sail 명령을 실행할 수 있습니다. 이 문서의 예시들은 해당 별칭이 설정되었다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

라라벨 Sail의 `docker-compose.yml` 파일에는 다양한 Docker 컨테이너가 정의되어 있어, 이 컨테이너들은 라라벨 애플리케이션 개발을 도와줍니다. 각각의 컨테이너는 `docker-compose.yml` 파일의 `services` 구성에 포함되어 있습니다. `laravel.test` 컨테이너는 실제로 애플리케이션을 서비스 하는 주요 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 애플리케이션의 모든 도커 컨테이너를 시작하려면 `up` 명령을 실행하면 됩니다:

```shell
sail up
```

모든 도커 컨테이너를 백그라운드(분리 모드)로 실행하려면 다음과 같이 실행하세요:

```shell
sail up -d
```

애플리케이션 컨테이너가 시작되면, 브라우저에서 http://localhost 로 접속할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C 입력으로 컨테이너 실행을 중단할 수 있습니다. 또는 백그라운드에서 실행 중이라면 `stop` 명령을 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령 실행하기

Laravel Sail을 사용할 때, 애플리케이션은 도커 컨테이너 안에서 실행되기 때문에 로컬 컴퓨터와 격리되어 있습니다. 그러나 Sail을 이용하면 PHP, Artisan, Composer, Node/NPM 등 다양한 명령을 쉽고 편리하게 실행할 수 있습니다.

**라라벨 공식 문서에서는 Sail 없이 Composer, Artisan, Node/NPM 명령을 직접 실행하는 예시가 종종 등장합니다.** 그런 예시는 해당 도구들이 로컬 컴퓨터에 직접 설치되어 있음을 가정합니다. Sail 환경에서 개발 중이라면 이들 명령을 Sail로 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령 실행하기

PHP 명령은 `php` 명령을 사용해 실행할 수 있습니다. 물론, 이 명령은 애플리케이션에 설정된 PHP 버전으로 실행됩니다. Sail에서 지원하는 PHP 버전에 대해 자세히 알아보려면 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령 실행하기

Composer 명령은 `composer` 명령을 사용해 실행할 수 있습니다. Sail의 애플리케이션 컨테이너는 Composer가 기본 탑재되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 프로젝트에 Composer 의존성 설치하기

여러 명이 한 프로젝트에서 개발하는 경우, 처음 생성된 라라벨 애플리케이션이 아닐 수도 있습니다. 따라서 레포지토리를 복제한 후엔 Sail을 포함한 애플리케이션 Composer 의존성 패키지가 설치되어 있지 않을 수 있습니다.

애플리케이션 디렉토리로 이동한 후, 다음 명령으로 의존성을 설치할 수 있습니다. 이 명령은 PHP와 Composer가 설치된 작은 Docker 컨테이너를 이용하여 의존성을 설치합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php84-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지를 사용할 때에는, 애플리케이션에서 사용할 PHP 버전(`80`, `81`, `82`, `83`, `84`)을 맞춰서 사용해야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령 실행하기

라라벨의 Artisan 명령은 `artisan` 명령어를 사용해 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령 실행하기

Node 명령은 `node` 명령으로, NPM 명령은 `npm` 명령으로 실행할 수 있습니다:

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

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 기본 포함되어 있습니다. 이 컨테이너는 [도커 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지/재시작해도 데이터는 그대로 유지됩니다.

또한 MySQL 컨테이너가 처음 시작되면, 두 개의 데이터베이스가 생성됩니다. 하나는 `DB_DATABASE` 환경변수의 값으로 이름이 붙은 개발용 데이터베이스이고, 두 번째는 `testing`이라는 별도의 테스트용 데이터베이스입니다. 이로 인해 테스트 중에도 실제 데이터베이스에 영향을 주지 않습니다.

컨테이너가 시작된 후, `.env` 파일에서 `DB_HOST` 환경변수를 `mysql`로 설정하여 애플리케이션 내에서 MySQL 인스턴스에 접속할 수 있습니다.

로컬 컴퓨터에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 MySQL은 `localhost`의 3306 포트에서 접근 가능하고, 접속 정보는 `DB_USERNAME`, `DB_PASSWORD` 환경변수 값을 따릅니다. 혹은 root 사용자로도 로그인할 수 있으며 이때 비밀번호는 `DB_PASSWORD`의 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `docker-compose.yml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 포함됩니다. 이 컨테이너는 [Atlas Search Index](https://www.mongodb.com/docs/atlas/atlas-search/) 등 Atlas의 여러 기능을 지원합니다. 역시 [도커 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로 데이터가 영구 보관됩니다.

컨테이너가 시작되면, `.env` 파일의 `MONGODB_URI` 환경변수를 `mongodb://mongodb:27017`로 설정하여 애플리케이션 내부에서 MongoDB에 접속할 수 있습니다. 인증은 기본 비활성화되어 있지만, 컨테이너 시작 전에 `MONGODB_USERNAME`, `MONGODB_PASSWORD` 환경 변수를 설정하면 인증을 사용할 수 있습니다. 연결 문자열에도 아래와 같이 반영해줍니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

애플리케이션과 MongoDB의 원활한 연동을 위해 [MongoDB가 공식적으로 관리하는 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 컴퓨터에서 MongoDB 데이터베이스에 접속하려면 [Compass](https://www.mongodb.com/products/tools/compass)와 같은 GUI를 사용할 수 있습니다. 기본적으로 MongoDB는 `localhost`의 27017 포트에서 접근 가능합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너도 [도커 볼륨](https://docs.docker.com/storage/volumes/)을 사용하며, 컨테이너를 중지/재시작해도 데이터가 유지됩니다. 컨테이너가 시작된 후에는 `.env` 파일의 `REDIS_HOST`를 `redis`로 지정하여 접속할 수 있습니다.

로컬 컴퓨터에서 Redis 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 같은 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 `localhost`의 6379 포트로 접속 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택하면, 애플리케이션의 `docker-compose.yml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너는 [도커 볼륨](https://docs.docker.com/storage/volumes/)을 사용하며, 데이터는 영구 보관됩니다. `.env` 파일의 `REDIS_HOST`를 `valkey`로 지정하여 애플리케이션에서 접속할 수 있습니다.

로컬 컴퓨터에서 접속할 때도 [TablePlus](https://tableplus.com)와 같은 도구를 사용하여 `localhost`의 6379 포트로 연결할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면 `docker-compose.yml` 파일에 해당 이 강력한 검색 엔진을 위한 항목이 포함됩니다. 이는 [Laravel Scout](/docs/{{version}}/scout)와 연동됩니다. 컨테이너를 시작한 후, `.env` 파일의 `MEILISEARCH_HOST`를 `http://meilisearch:7700`으로 설정하여 애플리케이션 내에서 Meilisearch 인스턴스와 연결할 수 있습니다.

로컬 컴퓨터에서는 웹 브라우저로 `http://localhost:7700` 접속 시 Meilisearch의 관리 패널을 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택하면, `docker-compose.yml` 파일에 이 빠르고 오픈소스인 검색 엔진을 위한 항목이 추가됩니다. 이는 [Laravel Scout](/docs/{{version}}/scout#typesense)와 네이티브로 연동됩니다. 컨테이너 실행 후 아래와 같이 환경변수를 설정하여 인스턴스에 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서는 `http://localhost:8108`로 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

운영 환경에서 Amazon S3에 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 선택하는 것이 좋습니다. MinIO는 S3와 호환되는 API를 제공하여 프로덕션 S3 환경에 "테스트" 버킷을 만들 필요 없이 로컬에서도 Laravel의 `s3` 파일 스토리지 드라이버를 사용할 수 있게 해줍니다. 설치 시 `docker-compose.yml` 파일에 MinIO 설정 섹션이 자동 추가됩니다.

기본적으로 `filesystems` 설정 파일에는 이미 `s3` 디스크가 정의되어 있습니다. 이 디스크를 사용해 Amazon S3뿐만 아니라 MinIO 같은 S3 호환 스토리지와도 연동할 수 있습니다. 예시로, MinIO를 사용할 때에는 환경변수 설정을 아래와 같이 변경합니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO 사용 시 적절한 URL이 생성되도록, `AWS_URL` 환경변수를 애플리케이션 로컬 URL과 버킷명이 포함되도록 지정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 `http://localhost:8900`에서 접근 가능하며, 기본 계정은 아이디 `sail`, 비밀번호 `password` 입니다.

> [!WARNING]  
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기

Laravel은 훌륭한 테스트 지원을 기본 제공하며, Sail의 `test` 명령을 이용해 [기능 테스트 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. Pest / PHPUnit이 지원하는 모든 CLI 옵션을 `test` 명령에 함께 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령은 `test` Artisan 명령과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 `testing`이라는 별도의 데이터베이스를 만들어 테스트가 현재 데이터베이스 상태에 영향을 주지 않도록 합니다. 기본 라라벨 설치에서는 `phpunit.xml` 파일도 자동으로 이 데이터베이스를 사용하도록 구성합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에, Selenium 등 추가 도구를 로컬에 설치하지 않고도 이러한 테스트를 바로 실행할 수 있습니다. 시작하려면 `docker-compose.yml`에서 Selenium 서비스의 주석을 해제하세요:

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

다음으로 `laravel.test` 서비스가 `selenium`에 의존하도록 `depends_on` 항목을 추가하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작한 뒤, `dusk` 명령으로 Dusk 테스트 스위트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium

로컬 머신이 Apple Silicon 칩을 사용하는 경우, `selenium` 서비스에는 `selenium/standalone-chromium` 이미지를 사용해야 합니다:

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

Laravel Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 도중 애플리케이션이 발송하는 이메일을 가로채어 웹에서 내용 확인이 가능하도록 해줍니다. Sail에서는 기본적으로 `mailpit` 호스트와 1025번 포트를 사용합니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, 브라우저에서 http://localhost:8025 로 접속해 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때로는 애플리케이션 컨테이너에서 Bash 세션을 직접 열고 싶을 수 있습니다. `shell` 명령을 사용하면 파일과 설치된 서비스 확인 및 컨테이너 내 임의의 셸 명령 실행이 가능합니다:

```shell
sail shell

sail root-shell
```

[Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령을 실행하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전에서 애플리케이션 구동을 지원합니다. 기본 PHP 버전으로는 PHP 8.4가 사용됩니다. 구동 중인 PHP 버전을 변경하려면 `docker-compose.yml` 파일의 `laravel.test` 컨테이너의 `build` 설정을 변경하세요:

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

원한다면 `image` 이름도 PHP 버전에 맞게 변경할 수 있습니다. 이 역시 `docker-compose.yml` 파일에 지정되어 있습니다:

```yaml
image: sail-8.2/app
```

설정 변경 후, 컨테이너 이미지를 반드시 재빌드 하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 20을 설치합니다. Node 버전을 변경하려면 `docker-compose.yml` 파일의 `laravel.test` 서비스에서 `build.args` 설정을 변경하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

설정 변경 후, 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기

동료에게 사이트를 보여주거나 애플리케이션의 webhook 통합을 테스트할 때 사이트를 외부에 임시로 공개해야 할 수 있습니다. 이럴 땐 `share` 명령을 사용하면 됩니다. 명령 실행 후 세션용 무작위 `laravel-sail.site` URL이 생성되며, 이를 통해 사이트에 접근할 수 있습니다:

```shell
sail share
```

사이트 공유 중이라면 `bootstrap/app.php` 파일 내의 `trustProxies` 미들웨어 메서드를 사용해 신뢰할 프록시를 설정해야 합니다. 그렇지 않으면 `url` 및 `route` 등 URL 생성 헬퍼가 올바른 HTTP 호스트를 인식하지 못할 수 있습니다:

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustProxies(at: '*');
    })

공유 시 사용할 서브도메인을 직접 지정하려면 `share` 명령 실행 시 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` 명령은 [BeyondCode](https://beyondco.de)가 만든 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)에 의해 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug를 이용한 디버깅

Laravel Sail의 Docker 구성에는 PHP 디버거로 널리 쓰이는 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면, 먼저 [Sail 구성을 배포](#sail-customization)했는지 확인하세요. 이후 `.env` 파일에 다음과 같이 Xdebug 설정 변수를 추가하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

이어서, 배포된 `php.ini` 파일에도 다음 설정이 들어있는지 확인하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정한 후에는 Docker 이미지를 반드시 재빌드해야 변경이 적용됩니다:

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경변수는 `client_host=host.docker.internal`로 정의되어 Mac과 Windows(WSL2)에서는 별도 설정이 필요 없습니다. 리눅스에서 Docker 20.10 이상을 사용하는 경우에도 `host.docker.internal`이 지원되어 추가설정이 필요 없습니다.

20.10 미만의 Docker 버전을 사용 중인 리눅스 환경에서는 `host.docker.internal`이 지원되지 않으므로, 컨테이너에 static IP를 지정하고 아래 예시처럼 네트워크를 직접 구성해야 합니다:

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

static IP를 지정했다면, `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 아래처럼 추가하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`debug` 명령을 이용해 Artisan 명령 실행 시 디버그 세션을 시작할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저에서 애플리케이션을 동작시키며 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)에 안내된 대로 세션을 시작하세요.

PhpStorm 사용자는 [제로-구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 대한 JetBrains 가이드도 참고하세요.

> [!WARNING]  
> Laravel Sail은 `artisan serve`로 애플리케이션을 서비스합니다. `XDEBUG_CONFIG`, `XDEBUG_MODE` 변수를 인식하는 것은 라라벨 8.53.0 이상부터입니다. 그 이하 버전(8.52.0 이하)에서는 디버그 연결이 지원되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 결국 Docker 기반이므로 거의 모든 구성을 자유롭게 변경할 수 있습니다. Sail의 Dockerfile 및 설정 파일을 개별적으로 프로젝트에 배포하려면 아래 명령을 실행하세요:

```shell
sail artisan sail:publish
```

이 명령을 실행하면, 라라벨 Sail이 사용하는 Dockerfile 등 여러 구성 파일이 애플리케이션 루트의 `docker` 디렉터리에 복사됩니다. Sail을 커스터마이징한 후에는, 애플리케이션 컨테이너의 이미지 이름을 `docker-compose.yml` 파일에서 변경하기를 권장합니다. 이후 `build` 명령을 사용해 컨테이너를 반드시 새로 빌드하세요. 특히 단일 컴퓨터에서 여러 개의 라라벨 애플리케이션을 Sail로 개발 중이라면 이미지 이름에 고유성을 부여하는 것이 중요합니다:

```shell
sail build --no-cache
```
