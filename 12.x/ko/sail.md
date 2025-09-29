# 라라벨 세일 (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [쉘 별칭(shell alias) 설정](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
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
- [사이트 공유](#sharing-your-site)
- [Xdebug를 통한 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 가벼운 명령줄 인터페이스입니다. Sail은 Docker에 대한 사전 지식 없이 PHP, MySQL, Redis를 활용한 Laravel 애플리케이션을 쉽게 구축할 수 있는 훌륭한 시작점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너와 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows ( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용 )에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 신규 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치

이미 존재하는 Laravel 애플리케이션에서 Sail을 사용하고 싶다면 Composer 패키지 관리자를 통해 간단히 Sail을 설치할 수 있습니다. (물론, 기존 로컬 개발 환경에서 Composer 패키지 설치가 가능한 상황을 가정합니다.)

```shell
composer require laravel/sail --dev
```

Sail 설치 후에는 `sail:install` Artisan 명령어를 실행하세요. 이 명령은 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 생성하고, Docker 서비스와 연결에 필요한 환경 변수로 `.env` 파일을 수정합니다.

```shell
php artisan sail:install
```

마지막으로 Sail을 시작하세요. Sail 사용 방법의 자세한 학습을 원한다면 문서의 나머지 부분을 계속 참고하시기 바랍니다.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용하는 경우, `docker context use default` 명령어를 실행하여 `default` Docker 컨텍스트를 사용해야 합니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치

기존 Sail 설치에 추가 서비스를 추가하고 싶다면, `sail:add` Artisan 명령어를 실행하세요.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고자 한다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 생성합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

이미지에 포함된 모든 패키지와 소프트웨어를 최신 상태로 유지하려면 Sail 이미지를 완전히 다시 빌드할 필요가 있을 수 있습니다. 다음 명령어로 이를 수행할 수 있습니다.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 쉘 별칭(shell alias) 설정

기본적으로 Sail 명령어는 모든 신규 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용합니다.

```shell
./vendor/bin/sail up
```

그러나 Sail 명령어를 실행할 때마다 `vendor/bin/sail`을 반복해서 입력하는 대신, 아래와 같이 쉘 별칭을 설정하면 더욱 편리하게 명령어를 실행할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있도록, 홈 디렉터리의 `~/.zshrc` 혹은 `~/.bashrc` 등 쉘 설정 파일에 위 코드를 추가하고, 쉘을 재시작하세요.

별칭이 잘 설정되었다면 이제 다음과 같이 간단히 명령어를 실행할 수 있습니다. 앞으로 문서의 예제들은 별칭이 설정된 상태를 기본으로 설명합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일은 다양한 Docker 컨테이너를 정의하여 Laravel 애플리케이션 개발을 지원합니다. 각 컨테이너는 `compose.yaml` 파일의 `services` 구성 내에 정의되어 있습니다. `laravel.test` 컨테이너가 애플리케이션을 실제로 서비스하는 주 컨테이너입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행하면 됩니다.

```shell
sail up
```

모든 Docker 컨테이너를 백그라운드에서 실행하려면 "detached" 모드로 시작할 수 있습니다.

```shell
sail up -d
```

컨테이너를 시작한 뒤 웹 브라우저에서 http://localhost 로 프로젝트에 접속할 수 있습니다.

모든 컨테이너를 종료하려면 Control + C 를 눌러 실행을 중단할 수 있습니다. 백그라운드에서 실행 중이라면 `stop` 명령어를 사용하세요.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 실행되며, 로컬 컴퓨터와는 격리되어 있습니다. 그러나 Sail은 PHP, Artisan, Composer, Node / NPM 등 각종 명령어를 애플리케이션에 손쉽게 실행할 수 있는 인터페이스를 제공합니다.

**Laravel 공식 문서를 읽을 때, Sail을 직접 언급하지 않는 Composer, Artisan, Node / NPM 명령어 예시가 자주 등장합니다.** 이는 해당 도구들이 로컬 컴퓨터에 직접 설치되어 있다고 가정합니다. Sail을 사용한다면, 이런 명령어도 Sail을 통해 실행해야 합니다.

```shell
# 로컬에서 Artisan 명령어 실행 예시...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령어를 통해 실행할 수 있습니다. 이때, 실제로 적용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Laravel Sail에서 지원하는 PHP 버전에 대해 더 알아보려면 [PHP 버전 문서](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 이미 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan` 명령어를 통해 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 명령어는 `node`, NPM 명령어는 `npm` 명령어를 통해 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다.

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

`compose.yaml` 파일에는 MySQL 컨테이너에 대한 설정이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 컨테이너를 중지·재시작해도 데이터가 보존됩니다.

또한, MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 자동으로 생성됩니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수의 값을 이름으로 하며 로컬 개발 용도입니다. 두 번째는 테스트 전용 데이터베이스인 `testing`으로, 테스트 데이터와 개발 데이터를 분리하여 테스트가 개발 데이터에 영향을 주지 않도록 합니다.

컨테이너를 시작한 뒤, `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 설정하면 애플리케이션 내부에서 MySQL 인스턴스에 연결할 수 있습니다.

로컬 PC에서 애플리케이션의 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근 가능하며, 로그인 정보는 `.env`의 `DB_USERNAME`, `DB_PASSWORD` 값과 일치합니다. 또는 `root` 계정으로도 접속 가능하며, 이 때도 비밀번호는 `DB_PASSWORD` 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `compose.yaml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 추가됩니다. 이 컨테이너는 Atlas의 [검색 인덱스](https://www.mongodb.com/docs/atlas/atlas-search/) 등 MongoDB Atlas 기능을 포함합니다. 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)으로 데이터가 안전하게 보존됩니다.

컨테이너 시작 후, `.env` 파일의 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 지정하면 애플리케이션 내부에서 MongoDB 인스턴스에 연결할 수 있습니다. 인증은 기본적으로 비활성화되어 있지만, `MONGODB_USERNAME` 및 `MONGODB_PASSWORD` 환경 변수를 미리 설정해두면 인증을 활성화할 수 있습니다. 설정 후 연결 문자열에 자격 증명을 포함하세요.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

애플리케이션과 MongoDB를 원활히 연동하려면 [공식 MongoDB 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치하세요.

로컬 컴퓨터에서 MongoDB 데이터베이스에 연결할 때는 [Compass](https://www.mongodb.com/products/tools/compass) 등 GUI 툴을 사용할 수 있습니다. 기본 포트는 `localhost:27017`입니다.

<a name="redis"></a>
### Redis

`compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 Redis 데이터가 안전하게 저장됩니다. 컨테이너 시작 이후, `.env` 파일의 `REDIS_HOST`를 `redis`로 설정하면 애플리케이션 내부에서 Redis 인스턴스에 연결할 수 있습니다.

로컬에서 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 등의 GUI를 활용할 수 있습니다. 기본 포트는 `localhost:6379`입니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `compose.yaml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)으로 데이터가 보존됩니다. `.env` 파일의 `REDIS_HOST`를 `valkey`로 설정하면 애플리케이션에서 Valkey 인스턴스에 연결할 수 있습니다.

로컬에서 Valkey 데이터베이스에 연결할 때도 [TablePlus](https://tableplus.com) 등을 사용할 수 있습니다. 기본 포트는 `localhost:6379`입니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면, `compose.yaml` 파일에 이 강력한 검색 엔진 항목이 추가됩니다. Meilisearch는 [Laravel Scout](/docs/12.x/scout)와 통합되어 있습니다. 컨테이너 실행 후, `.env` 파일의 `MEILISEARCH_HOST`를 `http://meilisearch:7700`으로 설정하면 애플리케이션과 연동할 수 있습니다.

로컬 PC에서는 웹 브라우저를 통해 `http://localhost:7700`에 접속하여 Meilisearch 관리 페이지에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택하면, `compose.yaml` 파일에 이 빠르고 오픈소스인 검색 엔진 항목이 추가됩니다. Typesense는 [Laravel Scout](/docs/12.x/scout#typesense)와 기본 연동됩니다. 컨테이너 실행 후 다음 환경 변수를 설정하여 애플리케이션에서 Typesense 인스턴스에 연결하세요.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 PC에서는 `http://localhost:8108`을 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 파일을 아마존 S3에 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 함께 설치하는 것이 좋습니다. MinIO는 S3 호환 API를 제공하므로, 실제 S3 환경에 "테스트" 버킷을 만들지 않고도 로컬에서 Laravel의 `s3` 파일 스토리지 드라이버를 개발 환경으로 활용할 수 있습니다. MinIO를 설치하면 `compose.yaml` 파일에 관련 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 포함되어 있습니다. 아마존 S3 뿐만 아니라 MinIO 등 모든 S3 호환 파일 스토리지 서비스를 이 디스크로 사용할 수 있으며, 설정을 위해 연관된 환경 변수만 적절히 변경하면 됩니다. MinIO 사용 시 예시는 다음과 같습니다.

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 연동이 MinIO를 올바르게 처리하게 하려면, `AWS_URL` 환경 변수를 애플리케이션 로컬 URL과 일치하도록 설정하고 버킷명이 URL 경로에 포함되도록 해야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔( http://localhost:8900 )에서 직접 버킷을 생성할 수 있습니다. 콘솔 기본 아이디는 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> `temporaryUrl` 메서드를 사용한 임시 파일 URL 생성은 MinIO에서는 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 기본적으로 뛰어난 테스트 기능을 제공합니다. Sail의 `test` 명령어로 [기능 테스트와 단위 테스트](/docs/12.x/testing)를 쉽게 실행할 수 있습니다. Pest / PHPUnit에서 지원하는 모든 CLI 옵션도 함께 넘겨줄 수 있습니다.

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 아래와 같이 `test` Artisan 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

Sail은 테스트 데이터베이스(`testing`)를 별도로 생성하여, 테스트 실행 시 실제 데이터에 영향을 주지 않도록 합니다. 기본 Laravel 설치에서는 Sail이 `phpunit.xml` 파일을 자동으로 이 테스트 데이터베이스를 가리키도록 구성합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 쉽고 강력한 브라우저 자동화 & 테스트 API를 제공합니다. Sail 덕분에 Selenium 등 도구를 로컬에 설치할 필요 없이 Dusk 테스트를 바로 실행할 수 있습니다. 먼저, 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스 항목의 주석을 해제하세요.

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

그리고 `laravel.test` 서비스의 `depends_on` 항목에 `selenium`을 추가해야 합니다.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이후에 Sail을 실행하고 `dusk` 명령어로 Dusk 테스트를 수행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서의 Selenium

Apple Silicon 칩이 장착된 Mac을 사용한다면, `selenium` 서비스는 반드시 `selenium/standalone-chromium` 이미지를 사용해야 합니다.

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

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 중 애플리케이션에서 발송한 이메일을 가로채고, 웹 인터페이스로 미리볼 수 있게 해줍니다. Sail 사용시 Mailpit의 기본 호스트는 `mailpit`이고, 1025 포트로 접근합니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025 에서 Mailpit 웹 인터페이스에 접속할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너에 Bash 세션으로 접속하고 싶을 때는 `shell` 명령어를 이용하세요. 이는 컨테이너 내부의 파일과 설치된 서비스, 임의의 쉘 명령어를 바로 확인·실행할 수 있게 해줍니다.

```shell
sail shell

sail root-shell
```

또한 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 사용하세요.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전에서 애플리케이션을 서비스할 수 있습니다. 기본 PHP 버전은 PHP 8.4입니다. 사용 PHP 버전을 변경하려면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 섹션을 아래와 같이 수정하세요.

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

원한다면 `image` 이름도 실제 사용 버전에 맞게 업데이트할 수 있습니다.

```yaml
image: sail-8.2/app
```

설정 변경 후에는 컨테이너 이미지를 반드시 재빌드하세요.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 시 설치할 Node 버전을 변경하려면, `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 항목을 아래와 같이 수정하세요.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

수정 후 이미지를 재빌드해야 변경사항이 적용됩니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나, 외부에서 Webhook 테스트를 할 때 등 사이트를 외부에 공개해야 할 때가 있습니다. 이럴 때는 `share` 명령어로 사이트를 손쉽게 공유할 수 있습니다. 명령어 실행 후 무작위의 `laravel-sail.site` URL이 발급되어, 해당 URL로 애플리케이션에 접근할 수 있습니다.

```shell
sail share
```

사이트를 공유할 때, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 신뢰할 수 있는 프록시를 반드시 지정하세요. 그렇지 않으면 `url`, `route`와 같은 URL 생성 헬퍼가 올바른 HTTP 호스트를 인식하지 못할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 서브도메인을 직접 지정하고 싶다면, `subdomain` 옵션을 함께 사용할 수 있습니다.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug를 통한 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 구성은 PHP 디버깅에 널리 사용되는 [Xdebug](https://xdebug.org/)를 지원합니다. Xdebug를 활성화하려면 [Sail 설정을 퍼블리시](#sail-customization)한 뒤, 애플리케이션의 `.env` 파일에 아래 환경 변수를 추가하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고 퍼블리시된 `php.ini` 파일에 Xdebug 설정이 아래와 같이 포함되어 있는지 확인하세요.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini`를 수정한 후에는 이미지 재빌드를 잊지 마세요.

```shell
sail build --no-cache
```

#### 리눅스 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있어 Mac과 Windows (WSL2)에서 Xdebug가 정상 동작합니다. Docker 20.10 이상을 사용하는 Linux에서는 `host.docker.internal` 지원이 기본 제공되어 추가 설정이 필요 없습니다.

만약 Docker 버전이 20.10 미만이라면, `host.docker.internal`이 지원되지 않으므로 수동으로 호스트 IP를 지정해 줘야 합니다. 이를 위해서는 `compose.yaml` 파일에서 커스텀 네트워크와 고정 IP를 설정하세요.

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

고정 IP를 지정했다면 `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 다음과 같이 정의하세요.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`debug` 명령어를 사용하면 Artisan 명령어 실행 시 디버깅 세션을 시작할 수 있습니다.

```shell
# Xdebug를 사용하지 않고 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저에서 애플리케이션을 이용하며 디버그하고 싶다면, [Xdebug에서 제공하는 가이드](https://xdebug.org/docs/step_debug#web-application)를 참조해 세션을 시작하세요.

PhpStorm을 사용하는 경우, [제로-구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 대한 JetBrains 공식 문서도 참고하세요.

> [!WARNING]
> Laravel Sail은 `artisan serve`를 이용해 애플리케이션을 서비스합니다. `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 적용하려면 Laravel 8.53.0 이상이어야 하며, 그 이하 버전에서는 해당 변수가 지원되지 않아 디버그 연결을 사용할 수 없습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 기반이므로 거의 모든 부분을 자유롭게 커스터마이징 할 수 있습니다. Sail에서 사용하는 Dockerfile 등을 퍼블리시하려면 다음 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

실행 후에는 `docker` 디렉터리 아래에 Sail에서 사용하는 Dockerfile 및 설정 파일들이 배치됩니다. 편집을 마친 뒤에는 `compose.yaml` 파일에서 어플리케이션 컨테이너의 이미지 이름을 지정하면 됩니다. 이후 `build` 명령어로 컨테이너를 재빌드하세요. 여러 Laravel 애플리케이션을 한 머신에서 개발할 경우, 이미지 이름을 고유하게 설정하는 것이 중요합니다.

```shell
sail build --no-cache
```
