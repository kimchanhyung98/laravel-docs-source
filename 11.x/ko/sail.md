# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드하기](#rebuilding-sail-images)
    - [셸 별칭 설정하기](#configuring-a-shell-alias)
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

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 가벼운 커맨드라인 인터페이스입니다. Sail은 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축할 수 있는 훌륭한 출발점을 제공하며, Docker 경험이 없어도 쉽게 사용할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너들을 편리하게 조작할 수 있는 CLI 기능을 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows(WSL2를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새 Laravel 애플리케이션에 자동으로 설치되므로 바로 사용할 수 있습니다. 새 Laravel 애플리케이션 생성 방법은 운영 체제에 맞춘 Laravel의 [설치 문서](/docs/11.x/installation#docker-installation-using-sail)를 참고하세요. 설치 과정에서는 애플리케이션에서 사용할 Sail 지원 서비스들을 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에 Sail을 사용하려면 Composer 패키지 관리자를 통해 Sail을 설치하면 됩니다. 이 과정은 로컬 개발 환경에서 Composer 의존성 설치가 가능하다는 전제가 필요합니다:

```shell
composer require laravel/sail --dev
```

Sail 설치 완료 후, `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트로 퍼블리시하고, `.env` 파일을 수정하여 Docker 서비스 연결에 필요한 환경 변수를 설정합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법에 대한 추가 학습은 이 문서의 나머지 부분을 계속 읽어보세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> Linux용 Docker Desktop을 사용하는 경우, 다음 명령어로 `default` Docker 컨텍스트를 사용하도록 설정해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치하기 (Adding Additional Services)

기존 Sail 설치에 추가 서비스를 넣고 싶다면, `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기 (Using Devcontainers)

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면, `sail:install` 명령어에 `--devcontainer` 옵션을 제공하면 됩니다. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 퍼블리시합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드하기 (Rebuilding Sail Images)

Sail 이미지 내 모든 패키지와 소프트웨어가 최신 상태인지 확인하려면 이미지를 완전히 재빌드할 필요가 있습니다. 다음 명령어로 수행할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 설정하기 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 실행합니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 타이핑하는 대신, 셸 별칭을 설정해서 더 쉽게 실행할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 홈 디렉터리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가하고 셸을 재시작하면 항상 사용할 수 있습니다.

이후부터는 단순히 `sail` 명령어로 Sail을 실행할 수 있습니다. 이 문서의 예제들은 이 별칭이 설정되어 있다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션 개발을 돕는 다양한 Docker 컨테이너를 정의합니다. 각각의 컨테이너는 `docker-compose.yml` 파일의 `services` 설정 안에 항목으로 존재하며, `laravel.test` 컨테이너가 애플리케이션을 서빙하는 주 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 모든 Docker 컨테이너를 시작하려면 다음 `up` 명령어를 실행합니다:

```shell
sail up
```

백그라운드에서 실행하려면 "detached" 모드로 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너 실행 후, 웹 브라우저로 http://localhost 에 접속하여 프로젝트를 확인할 수 있습니다.

컨테이너를 중지하려면, 실행 중인 터미널에서 Control + C를 누르거나 백그라운드 실행 중인 경우 다음 명령어를 사용합니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내부에서 실행되어 로컬 컴퓨터와 격리됩니다. 하지만 Sail은 PHP, Artisan, Composer, Node / NPM 명령어 등 애플리케이션 관련 다양한 명령을 편리하게 실행할 수 있도록 도와줍니다.

**Laravel 공식 문서에서 Composer, Artisan, Node / NPM 명령어가 Sail 없이 실행되는 예제를 볼 수 있습니다.** 이러한 명령어들은 로컬 컴퓨터에 도구들이 설치되어 있다는 가정하에 실행됩니다. Sail로 로컬 개발 환경을 구성했다면 반드시 Sail을 사용해 명령어를 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행하기...
php artisan queue:work

# Laravel Sail 내부에서 Artisan 명령어 실행하기...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기 (Executing PHP Commands)

PHP 명령어는 `php` 명령어를 사용해 실행할 수 있습니다. 실행되는 PHP 버전은 현재 애플리케이션에 설정된 버전입니다. Laravel Sail이 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)에서 확인하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기 (Executing Composer Commands)

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 포함되어 있습니다:

```shell
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 프로젝트에 Composer 의존성 설치하기 (Installing Composer Dependencies for Existing Applications)

팀으로 애플리케이션을 개발하는 경우, 여러분이 최초 생성자가 아닐 수 있습니다. 따라서 애플리케이션 저장소를 로컬에 클론한 후엔 Sail을 포함한 Composer 의존성이 설치되어 있지 않을 수 있습니다.

의존성은 애플리케이션 디렉터리로 이동한 뒤, 아래 명령어로 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 작은 Docker 컨테이너를 사용합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php84-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지 사용 시, 애플리케이션에서 사용할 PHP 버전(`80`, `81`, `82`, `83`, `84`)에 맞는 이미지를 사용해야 합니다.

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

필요하다면 Yarn을 사용해도 됩니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해, 컨테이너가 멈추거나 재시작되어도 데이터가 유지되도록 합니다.

MySQL 컨테이너가 처음 시작되면, 두 개의 데이터베이스를 생성합니다. 하나는 `DB_DATABASE` 환경 변수 값과 동일한 이름의 로컬 개발용 데이터베이스이며, 다른 하나는 `testing`이라는 이름의 테스트 전용 데이터베이스로, 테스트 실행 시 개발 데이터와 충돌하지 않도록 합니다.

컨테이너가 시작되면, 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수 값을 `mysql`로 설정해 MySQL 인스턴스에 연결합니다.

로컬 머신에서 MySQL 데이터베이스에 연결하려면, [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL은 `localhost`의 3306 포트를 통해 접근 가능하며, 인증 정보는 `.env`의 `DB_USERNAME`, `DB_PASSWORD` 값을 사용합니다. 또는 `root` 계정으로 접속할 수 있는데, 이때도 암호는 `DB_PASSWORD` 환경 변수 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택하면, `docker-compose.yml`에 MongoDB Atlas Local 컨테이너가 추가됩니다. 이 컨테이너는 [MongoDB Atlas CLI Local Cloud](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 기능을 제공하며, [검색 인덱스](https://www.mongodb.com/docs/atlas/atlas-search/) 같은 Atlas 기능을 지원합니다. 또한 Docker 볼륨을 사용해 데이터가 유지됩니다.

컨테이너가 시작된 후 애플리케이션의 `.env` 파일에서 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`으로 설정해 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있으나, 필요시 `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정해 인증을 활성화할 수 있습니다. 인증 활성화 시 연결 문자열은 다음 예시와 같이 구성합니다:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와의 원활한 통합을 위해 [MongoDB 공식 Laravel 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 머신에서 MongoDB에 연결하려면, [Compass](https://www.mongodb.com/products/tools/compass) 같은 GUI 도구를 사용하세요. 기본 포트는 `localhost`의 27017입니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml`에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너 역시 Docker 볼륨을 활용하여 데이터 지속성을 유지합니다. 시작 후 `.env` 파일의 `REDIS_HOST`를 `redis`로 설정하여 연결합니다.

로컬에서 GUI를 이용해 연결할 때는 [TablePlus](https://tableplus.com) 같은 도구를 사용하며, 기본적으로 `localhost`의 6379 포트를 통해 접근할 수 있습니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택하면, `docker-compose.yml`에 [Valkey](https://valkey.io/) 컨테이너가 구성됩니다. 이 컨테이너도 Docker 볼륨을 사용해 데이터가 유지됩니다. 애플리케이션 `.env` 파일 내 `REDIS_HOST` 값을 `valkey`로 설정해 연결합니다.

로컬 머신에서 접근할 때도 [TablePlus](https://tableplus.com) 같은 GUI를 사용할 수 있으며, 기본 포트는 `localhost`의 6379입니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면, `docker-compose.yml`에 Meilisearch 컨테이너가 포함됩니다. Meilisearch는 [Laravel Scout](/docs/11.x/scout)과 통합된 강력한 검색 엔진입니다. 컨테이너 시작 후 `.env` 파일의 `MEILISEARCH_HOST` 값을 `http://meilisearch:7700`으로 설정해 연결하세요.

로컬 머신에서는 웹 브라우저에서 `http://localhost:7700`으로 접속해 Meilisearch 관리자 패널을 이용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail에서 [Typesense](https://typesense.org) 서비스를 선택하면, `docker-compose.yml`에 Typesense 컨테이너가 포함됩니다. Typesense는 빠르고 오픈소스인 검색 엔진으로, [Laravel Scout](/docs/11.x/scout#typesense)과 네이티브 통합되어 있습니다. 컨테이너 시작 후 `.env` 파일에 다음 환경 변수를 설정하여 연결합니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 머신에서는 `http://localhost:8108`로 API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 저장소 (File Storage)

애플리케이션이 프로덕션 환경에서 Amazon S3를 사용해 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 선택하는 것이 좋습니다. MinIO는 S3 호환 API를 제공하여, 로컬 개발 시 테스트용 S3 버킷을 만들 필요 없이 Laravel의 `s3` 파일 저장소 드라이버로 작업할 수 있습니다. MinIO 서비스 설치 시 `docker-compose.yml`에 관련 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크를 Amazon S3 외에 MinIO와 같은 S3 호환 스토리지 서비스에 연결하려면 관련 환경 변수만 변경하면 됩니다. 예를 들어, MinIO는 다음과 같이 설정합니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성할 수 있도록, `AWS_URL` 환경 변수도 로컬 URL과 버킷 이름을 포함하여 다음과 같이 설정하는 것이 좋습니다:

```ini
AWS_URL=http://localhost:9000/local
```

버킷 생성은 MinIO 콘솔(http://localhost:8900)에서 진행할 수 있으며, 기본 로그인 아이디는 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]  
> MinIO를 사용할 경우, `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

Laravel은 강력한 테스트 기능을 내장하고 있으며, Sail의 `test` 명령어로 애플리케이션의 [기능 테스트 및 단위 테스트](/docs/11.x/testing)를 실행할 수 있습니다. Pest나 PHPUnit에서 지원하는 모든 CLI 옵션을 `test` 명령어에 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어와 같습니다:

```shell
sail artisan test
```

기본적으로 Sail은 테스트 전용 `testing` 데이터베이스를 생성해 테스트가 현재 데이터베이스 상태에 영향을 미치지 않도록 합니다. 기본 Laravel 설치 시, `phpunit.xml` 파일도 이 데이터베이스를 사용하도록 설정되어 있습니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/11.x/dusk)는 브라우저 자동화 및 테스트를 쉽게 작성할 수 있는 API입니다. Sail 덕분에 Selenium 등의 도구를 로컬 컴퓨터에 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

다음으로 `laravel.test` 서비스의 `depends_on`에 `selenium`을 추가해 의존성을 설정합니다:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이후 Sail을 시작하고 Dusk 테스트를 실행하세요:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용하기

Apple Silicon 칩이 탑재된 로컬 머신에서는 다음과 같이 `selenium` 서비스의 이미지가 `selenium/standalone-chromium`이어야 합니다:

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

Laravel Sail 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit는 애플리케이션이 로컬에서 발송하는 이메일을 가로채어 웹 인터페이스로 이메일 내용을 미리 볼 수 있게 해 줍니다. Sail에서 Mailpit의 기본 호스트는 `mailpit`이며, 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때 웹 브라우저에서 Mailpit 웹 인터페이스에 접근하려면 아래 주소로 접속하세요: http://localhost:8025

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너 안에서 Bash 세션을 시작하여 컨테이너 내 파일, 설치된 서비스 점검 및 임의의 셸 명령 실행이 필요할 때가 있습니다. 이럴 때는 `shell` 명령어를 사용하세요:

```shell
sail shell

sail root-shell
```

또한, [Laravel Tinker](https://github.com/laravel/tinker) 세션을 새로 시작하려면 `tinker` 명령어를 실행합니다:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0 버전을 지원합니다. 기본 PHP 버전은 8.4입니다. 사용 중인 PHP 버전을 변경하려면, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 설정을 수정하세요:

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

또한 PHP 버전에 맞게 애플리케이션 컨테이너의 `image` 이름도 변경할 수 있습니다 (`docker-compose.yml` 내에 설정됨):

```yaml
image: sail-8.2/app
```

설정 변경 후 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 20을 설치합니다. 이미지 빌드 시 설치할 Node 버전을 변경하려면, `docker-compose.yml`에서 `laravel.test` 서비스의 `build.args` 설정을 아래와 같이 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

설정 수정 후 컨테이너 이미지를 재빌드합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료와 사이트를 미리보기 위해 공개적으로 공유하거나 웹훅 연동 테스트를 위해 사이트를 공유해야 할 때가 있습니다. 이때 `share` 명령어를 사용하세요. 실행하면 무작위 `laravel-sail.site` URL이 발급되어 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령어로 사이트를 공유할 때, `trustProxies` 미들웨어를 `bootstrap/app.php`에서 설정해 애플리케이션의 신뢰할 수 있는 프록시를 등록해야 합니다. 그렇지 않으면 URL 생성 헬퍼(`url`, `route`)에서 올바른 HTTP 호스트 정보를 알 수 없습니다:

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

공유할 서브도메인을 원하는 이름으로 지정하려면, `share` 명령어에 `--subdomain` 옵션을 사용하세요:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` 명령어는 [BeyondCode](https://beyondco.de)에서 제공하는 오픈 소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 PHP용 강력한 디버거인 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면 Sail 설정 파일을 퍼블리시한 후, 애플리케이션 `.env` 파일에 다음 변수를 설정하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

퍼블리시된 `php.ini` 파일에 다음 설정이 포함되도록 확인해 Xdebug가 지정된 모드로 활성화됩니다:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정한 후에는 Docker 이미지를 재빌드해야 설정이 적용됩니다:

```shell
sail build --no-cache
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 Mac과 Windows(WSL2)에 맞게 `client_host=host.docker.internal`로 정의되어 있습니다. 만약 Linux에서 Docker 20.10 이상을 사용 중이라면 `host.docker.internal`이 지원되므로 추가 설정이 필요 없습니다.

하지만 Docker 버전이 20.10 이하이며 Linux 환경이라면 `host.docker.internal`이 지원되지 않아, 직접 호스트 IP를 지정해야 합니다. 이를 위해 `docker-compose.yml`에 커스텀 네트워크와 고정 IP를 설정하세요:

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

고정 IP 지정 후 애플리케이션 `.env` 파일에 다음을 추가합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

Artisan 명령어 실행 시 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용합니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug 문서](https://xdebug.org/docs/step_debug#web-application)에 안내된 대로 Xdebug 세션을 브라우저에서 시작하세요.

PhpStorm 사용자라면 JetBrains의 [제로-설정 디버깅 문서](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)를 참고하세요.

> [!WARNING]  
> Laravel Sail은 `artisan serve`로 애플리케이션을 서빙합니다. `artisan serve` 명령어는 Laravel 8.53.0부터 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하 버전에서는 해당 변수들을 지원하지 않아 디버그 연결이 수락되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 환경이기 때문에 원하는 거의 모든 부분을 자유롭게 커스터마이징 할 수 있습니다. Sail의 Dockerfile을 퍼블리시하려면 다음 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

명령어 실행 후, Laravel Sail이 사용하는 Dockerfile과 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 생성됩니다. Sail을 커스터마이징 한 후에는, `docker-compose.yml` 파일에서 애플리케이션 컨테이너 이미지 이름도 변경할 수 있습니다. 여러 Laravel 애플리케이션을 한 기기에서 개발한다면, 컨테이너 이미지 이름을 고유하게 지정하는 것이 중요합니다.

변경을 완료하면 다음 명령어로 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache
```