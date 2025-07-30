# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [셸 별칭 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행하기](#executing-php-commands)
    - [Composer 명령어 실행하기](#executing-composer-commands)
    - [Artisan 명령어 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령어 실행하기](#executing-node-npm-commands)
- [데이터베이스와 상호작용하기](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
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

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 가벼운 커맨드 라인 인터페이스입니다. Sail은 PHP, MySQL, Redis를 사용해서 Laravel 애플리케이션을 구축할 수 있도록 훌륭한 시작점을 제공하며, Docker 경험이 없어도 쉽게 사용할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 있는 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너를 편리하게 제어할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows(WSL2를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새 Laravel 애플리케이션에 자동으로 설치되어 즉시 사용할 수 있습니다. 새 Laravel 애플리케이션을 생성하는 방법은 운영체제별 Laravel [설치 문서](/docs/10.x/installation#docker-installation-using-sail)를 참고하세요. 설치 과정에서 애플리케이션이 사용할 Sail 지원 서비스 선택을 요청받게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에서 Sail을 사용하고자 한다면 Composer 패키지 매니저를 통해 간단히 설치할 수 있습니다. 이 절차는 기존의 로컬 개발 환경이 Composer 의존성 설치를 지원한다고 가정합니다:

```shell
composer require laravel/sail --dev
```

Sail 설치 후, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 배포하고, Docker 서비스에 연결하기 위해 필요한 환경 변수를 `.env` 파일에 설정합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법을 계속하려면 이 문서의 나머지 부분을 읽어보세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> Linux용 Docker Desktop을 사용 중이라면, 다음 명령어로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치하기

이미 설치한 Sail에 추가 서비스를 붙이고 싶다면, `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가할 수 있습니다. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 배포합니다:

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 설정하기 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 실행됩니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 반복 입력하는 대신, 좀 더 쉽게 Sail 명령어를 실행할 수 있도록 셸 별칭을 설정할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있도록 하려면, 홈 디렉토리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 추가하고 셸을 재시작하세요.

별칭 설정 후에는 단순히 `sail` 명령어만 입력해서 Sail 명령어를 실행할 수 있습니다. 이 문서에 나오는 예제들은 이 별칭이 설정되어 있다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 구축을 위한 다양한 Docker 컨테이너가 정의되어 있습니다. 이들 컨테이너는 모두 `docker-compose.yml` 파일 내의 `services` 설정에 포함되어 있습니다. `laravel.test` 컨테이너는 애플리케이션을 서비스하는 주 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 애플리케이션 `docker-compose.yml`에 정의된 모든 컨테이너를 실행하려면 `up` 명령어를 실행하면 됩니다:

```shell
sail up
```

백그라운드에서 실행하려면, detached 모드로 Sail을 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너가 시작되면 브라우저에서 http://localhost 으로 프로젝트에 접근할 수 있습니다.

컨테이너를 중지하려면, 실행 중일 때 Control + C 키를 누르거나, 백그라운드 실행 중이라면 `stop` 명령어를 사용하세요:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail 환경에서 애플리케이션은 Docker 컨테이너 내에서 실행되며 로컬 컴퓨터와는 분리되어 있습니다. 하지만 Sail은 다양한 명령들을 손쉽게 실행할 수 있도록 도와줍니다. 예를 들어 임의의 PHP 명령어, Artisan, Composer, Node / NPM 명령어들을 컨테이너 안에서 실행 가능합니다.

**Laravel 문서에서 종종 Composer, Artisan, Node / NPM 명령어를 Sail을 거치지 않고 실행하는 예제를 보게 됩니다.** 이것은 해당 툴들이 로컬 컴퓨터에 설치되어 있다는 가정을 의미합니다. 하지만 Sail 환경에서는 이러한 명령어들을 반드시 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행하기...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령어 실행하기...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기 (Executing PHP Commands)

PHP 명령어는 `php` 명령어로 실행합니다. 이 명령어는 애플리케이션에 설정된 PHP 버전을 사용합니다. Laravel Sail이 지원하는 PHP 버전에 관한 내용은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기 (Executing Composer Commands)

Composer 명령어는 `composer`를 통해 실행합니다. Laravel Sail 애플리케이션 컨테이너에는 Composer 2.x가 기본 설치되어 있습니다:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 프로젝트에서 Composer 의존성 설치하기

팀과 함께 개발 중인 경우, 애플리케이션을 처음 만든 사람이 아닐 수 있습니다. 따라서 리포지터리를 복제한 후 Laravel 애플리케이션의 모든 Composer 의존, Sail 포함, 이 설치되어 있지 않을 수 있습니다.

의존성을 설치하려면 애플리케이션 디렉터리로 이동해서 아래 명령어를 실행하세요. 이 명령어는 PHP와 Composer가 들어 있는 작은 Docker 컨테이너를 실행하여 의존성을 설치합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지는 애플리케이션에서 사용할 PHP 버전(`80`, `81`, `82` 또는 `83`)과 일치해야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행하기 (Executing Artisan Commands)

Laravel Artisan 명령어는 `artisan` 명령어로 실행합니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행하기 (Executing Node / NPM Commands)

Node 명령어는 `node`로, NPM 명령어는 `npm`으로 실행합니다:

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

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 설정이 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여, 컨테이너를 중지하거나 재시작해도 데이터가 유지됩니다.

첫 실행 시 MySQL 컨테이너는 두 개의 데이터베이스를 생성합니다. 하나는 `DB_DATABASE` 환경 변수 값으로 지정된 개발용 데이터베이스이고, 다른 하나는 테스트 전용 데이터베이스 `testing`입니다. 테스트 데이터베이스는 테스트가 개발 데이터에 영향을 주지 않도록 분리하는 용도입니다.

컨테이너가 시작된 후 애플리케이션 내에서 MySQL 접속을 원한다면 `.env` 파일에서 `DB_HOST`를 `mysql`로 설정하세요.

로컬 머신에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 툴을 써도 됩니다. 기본적으로 MySQL은 `localhost` 3306 포트로 접근 가능하며, 인증은 `.env`에 설정된 `DB_USERNAME`과 `DB_PASSWORD`를 사용합니다. 또는 `root` 사용자로도 연락 가능하며 이때 비밀번호는 `DB_PASSWORD` 값이 사용됩니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml`에는 [Redis](https://redis.io) 컨테이너 설정도 포함됩니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)로 인해 데이터가 지속됩니다. 컨테이너 시작 후 `.env`에서 `REDIS_HOST`를 `redis`로 설정하면 애플리케이션에서 연결할 수 있습니다.

로컬 머신에서 Redis에 접속하려면 [TablePlus](https://tableplus.com) 같은 툴을 사용할 수 있으며, 기본 접속 정보는 `localhost` 6379 포트입니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, 애플리케이션 `docker-compose.yml`에 이 빠르고 강력한 검색 엔진에 대한 설정이 포함됩니다. Meilisearch는 [Laravel Scout](/docs/10.x/scout)와 호환됩니다([호환 정보](https://github.com/meilisearch/meilisearch-laravel-scout)).

컨테이너가 시작되면 `.env`에서 `MEILISEARCH_HOST`를 `http://meilisearch:7700`으로 설정해 애플리케이션과 연결할 수 있습니다.

로컬 머신에서는 브라우저로 `http://localhost:7700`에 접속해 Meilisearch의 웹 관리 인터페이스를 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml`에 이 빠르고 오픈 소스인 검색 엔진의 설정이 추가됩니다. Typesense는 [Laravel Scout](/docs/10.x/scout#typesense)와 기본 통합되어 있습니다.

컨테이너가 시작된 후, 애플리케이션 `.env` 파일에 다음 환경 변수를 설정해 연결합니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 머신에서는 `http://localhost:8108`를 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

애플리케이션을 운영 환경에서 Amazon S3에 파일을 저장하려 한다면, Sail 설치 시 [MinIO](https://min.io) 서비스를 설치하는 것이 좋습니다. MinIO는 S3와 호환되는 API를 제공해, 실제 운영 환경에 "테스트" 버킷을 만들지 않고도 로컬에서 Laravel의 `s3` 파일 스토리지 드라이버를 사용해 개발할 수 있습니다.

MinIO를 설치하면 `docker-compose.yml` 파일에 MinIO 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정에는 `s3` 디스크 구성이 이미 있습니다. MinIO를 사용하려면 관련 환경 변수들을 `s3` 디스크 설정에 맞게 `.env` 파일에서 다음과 같이 수정하세요:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO를 사용할 때 Laravel Flysystem이 올바른 URL을 생성하도록 하려면, `AWS_URL` 환경 변수를 로컬 URL과 버킷 이름을 포함하는 형태로 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 `http://localhost:8900`에서 접근할 수 있으며, 기본 사용자명은 `sail`, 기본 비밀번호는 `password`입니다.

> [!WARNING]  
> MinIO를 사용할 경우, `temporaryUrl` 메서드로 임시 저장소 URL을 생성하는 것은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

Laravel은 기본적으로 강력한 테스트 지원을 제공합니다. Sail의 `test` 명령어로 애플리케이션의 [기능 및 단위 테스트](/docs/10.x/testing)를 실행할 수 있습니다. PHPUnit에서 허용하는 모든 CLI 옵션도 `test` 명령어에 전달 가능합니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어와 동일합니다:

```shell
sail artisan test
```

기본적으로, Sail은 `testing`이라는 별도의 데이터베이스를 생성해 테스트가 기존 데이터베이스 상태에 영향을 주지 않도록 합니다. 기본 Laravel 설치 시 `phpunit.xml` 파일도 이 데이터베이스를 사용하도록 설정됩니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/10.x/dusk)는 직관적이고 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium 등 별도 도구 설치 없이 브라우저 테스트가 가능합니다. 시작하려면 애플리케이션 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

다음으로 `laravel.test` 서비스의 `depends_on` 항목에 `selenium`이 포함되어 있는지 확인합니다:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 시작하고 `dusk` 명령어로 Dusk 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용하기

로컬 머신이 Apple Silicon 칩을 사용한다면, `selenium` 서비스는 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다:

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 이메일 미리보기 (Previewing Emails)

Laravel Sail 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 중 애플리케이션이 보내는 이메일을 가로채 웹 인터페이스에서 메일 내용을 미리볼 수 있게 합니다. Sail을 사용할 때 Mailpit 기본 호스트는 `mailpit`이고 1025 포트로 노출됩니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때 웹 브라우저에서 http://localhost:8025 로 접속해 Mailpit UI를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너 내에서 Bash 세션을 시작하고 싶을 때는 `shell` 명령어를 사용할 수 있습니다. 이를 통해 컨테이너 내부 파일이나 서비스 상태를 확인하거나 임의의 셸 명령어를 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.3, 8.2, 8.1, 8.0 버전을 지원하며 기본 PHP 버전은 8.3입니다. 애플리케이션에 사용할 PHP 버전을 변경하려면 `docker-compose.yml` 내 `laravel.test` 컨테이너의 `build` 설정을 수정하세요:

```yaml
# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

또한, `image` 이름도 애플리케이션에서 사용할 PHP 버전을 반영하도록 변경할 수 있습니다:

```yaml
image: sail-8.1/app
```

`docker-compose.yml` 수정 후에는 컨테이너 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 20을 설치합니다. 이미지 빌드 시 설치할 Node 버전을 변경하려면 `docker-compose.yml` 파일의 `laravel.test` 서비스 내 `build.args` 아래 `NODE_VERSION` 값을 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

`docker-compose.yml` 수정 후에는 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료와 사이트를 공개적으로 공유하거나 웹훅 통합 테스트를 할 필요가 있을 때, `share` 명령어를 사용하면 무작위 `laravel-sail.site` URL이 발급되어 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령어로 공유 중이라면, `TrustProxies` 미들웨어에서 애플리케이션의 신뢰할 수 있는 프록시를 설정해야 합니다. 그렇지 않으면 URL 생성 헬퍼(`url`, `route` 등)가 올바른 HTTP 호스트를 인식하지 못합니다:

```
/**
 * 애플리케이션의 신뢰할 수 있는 프록시입니다.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

공유할 사이트의 서브도메인을 직접 지정하려면 `share` 명령어 실행 시 `subdomain` 옵션을 제공합니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)를 기반으로 합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail Docker 설정에는 PHP용 강력한 디버거 [Xdebug](https://xdebug.org/)가 포함되어 있습니다. Xdebug를 활성화하려면 애플리케이션 `.env` 파일에 몇 가지 환경 변수를 추가하여 [Xdebug 설정](https://xdebug.org/docs/step_debug#mode)을 구성해야 합니다. Sail 시작 전에 적절한 모드를 설정해야 합니다:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### Linux 호스트 IP 설정

기본적으로 `XDEBUG_CONFIG` 환경 변수는 Mac과 Windows(WSL2)를 위한 `client_host=host.docker.internal`로 설정되어 있습니다. Linux 환경이라면 Docker Engine 17.06.0+ 및 Compose 1.16.0+를 사용해야 하며, 그렇지 않으면 아래처럼 직접 환경 변수를 설정해야 합니다.

먼저, 호스트 IP 주소를 찾으려면 `<container-name>`에 애플리케이션을 서비스하는 컨테이너 이름(대개 `_laravel.test_1`로 끝남)을 넣어 아래 명령어를 실행하세요:

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

찾은 IP 주소를 `.env` 파일의 `SAIL_XDEBUG_CONFIG` 변수에 설정합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

`artisan` 명령어 실행시 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug 켜고 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저를 통한 디버깅은 [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)에 안내된 단계에 따라 세션을 시작하세요.

PhpStorm을 사용한다면 [JetBrains의 제로-설정 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 문서를 참고하세요.

> [!WARNING]  
> Laravel Sail은 애플리케이션을 제공하기 위해 `artisan serve`를 사용합니다. `artisan serve` 명령어는 Laravel 버전 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하 버전에서는 디버그 연결을 수락하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 Docker 기반이므로 거의 모든 부분을 자유롭게 수정할 수 있습니다. Sail의 Dockerfile들을 배포하려면 `sail:publish` 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

이 명령어 실행 후 Dockerfile 및 기타 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 생성됩니다. Sail 환경을 커스터마이징한 뒤에는 `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름을 변경하는 것이 좋습니다. 특히 한 시스템에서 여러 Laravel 애플리케이션을 개발 중일 때는 고유한 이미지 이름이 필요합니다:

```shell
sail build --no-cache
```