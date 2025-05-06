# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Bash 별칭 설정하기](#configuring-a-bash-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용하기](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [MeiliSearch](#meilisearch)
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
## 소개

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 경량 커맨드라인 인터페이스입니다. Sail을 사용하면 Docker 경험이 없어도 PHP, MySQL, Redis와 함께 Laravel 애플리케이션을 손쉽게 개발할 수 있는 훌륭한 출발점을 제공받습니다.

Sail의 핵심은 프로젝트 루트에 저장된 `docker-compose.yml` 파일과 `sail` 스크립트입니다. 이 `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 활용)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 신규 Laravel 애플리케이션에서 자동으로 설치되므로 즉시 사용을 시작할 수 있습니다. 새 Laravel 애플리케이션을 만드는 방법은 각 운영체제별 Laravel의 [설치 문서](/docs/{{version}}/installation)를 참고하세요. 설치 과정에서 애플리케이션에서 사용할 Sail 지원 서비스들을 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에서 Sail을 사용하려면 Composer 패키지 관리자로 Sail을 설치할 수 있습니다. 이 단계는 로컬 개발 환경에서 Composer 의존성 설치가 가능한 상황을 전제로 합니다.

    composer require laravel/sail --dev

Sail 설치 후, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 생성합니다.

    php artisan sail:install

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 알고싶다면 이 문서를 계속 읽어주세요.

    ./vendor/bin/sail up

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 내에서 개발을 원한다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션을 사용하면 기본 `.devcontainer/devcontainer.json` 파일이 애플리케이션 루트에 생성됩니다.

    php artisan sail:install --devcontainer

<a name="configuring-a-bash-alias"></a>
### Bash 별칭 설정하기

기본적으로 Sail 명령어는 모든 신규 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 실행합니다.

```bash
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하기 번거롭기 때문에 Bash 별칭을 설정하면 좀 더 쉽게 Sail 명령어를 실행할 수 있습니다.

```bash
alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'
```

별칭 설정 후에는 그냥 `sail`만 입력해서 명령어를 사용할 수 있습니다. 본 문서의 예제들은 별칭이 설정되어 있다고 가정합니다:

```bash
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 개발에 필요한 다양한 Docker 컨테이너 구성이 정의되어 있습니다. 각각의 컨테이너는 `docker-compose.yml` 파일의 `services` 설정 항목에 등록되어 있습니다. `laravel.test` 컨테이너가 애플리케이션을 실제로 서빙하는 주 컨테이너입니다.

Sail 시작 전, 로컬 컴퓨터에 다른 웹서버나 데이터베이스가 실행되고 있지 않은지 확인하세요. `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행하면 됩니다:

```bash
sail up
```

모든 Docker 컨테이너를 백그라운드에서 실행하려면 "detached" 모드로 Sail을 시작할 수 있습니다:

```bash
sail up -d
```

애플리케이션 컨테이너가 모두 시작되면 웹 브라우저에서 http://localhost 로 접속할 수 있습니다.

컨테이너 실행을 중단하려면 Control + C를 누르거나, 백그라운드 모드로 실행 중이라면 `stop` 명령어를 사용하세요:

```bash
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 실행되며, 로컬 컴퓨터와는 격리되어 있습니다. 하지만 Sail은 다양한 명령어(PHP 임의 명령어, Artisan, Composer, Node/NPM 등)를 애플리케이션에 편리하게 실행할 수 있는 기능을 제공합니다.

**Laravel 공식 문서에서 Composer, Artisan, Node/NPM 명령어 예제가 Sail을 명시하지 않고 나오는 경우가 자주 있습니다.** 이러한 예제는 해당 도구들이 로컬에 설치되어 있음을 전제로 합니다. Sail 환경을 쓴다면 해당 명령어에 Sail을 함께 사용하세요:

```bash
# 로컬에서 Artisan 명령어 실행 예시...
php artisan queue:work

# Laravel Sail에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령을 통해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Sail이 지원하는 PHP 버전에 관한 더 자세한 정보는 [PHP 버전 문서](#sail-php-versions)를 참고하세요.

```bash
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령을 통해 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer 2.x가 설치되어 있습니다.

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 애플리케이션에 Composer 의존성 설치

팀과 협업하면서 개발하는 경우 Laravel 애플리케이션을 직접 생성하지 않았을 수 있습니다. 이런 경우 리포지토리를 클론해도 Sail을 포함한 Composer 의존성이 설치되어 있지 않게 됩니다.

아래 명령어를 통해 애플리케이션 디렉터리에서 의존성을 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 작은 Docker 컨테이너를 활용해 의존성 설치를 진행합니다.

```nothing
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v $(pwd):/var/www/html \
    -w /var/www/html \
    laravelsail/php81-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지를 사용할 땐, 실제 애플리케이션에서 사용할 예정인 PHP 버전(`74`, `80`, `81`)과 동일한 버전을 선택해야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan` 명령을 통해 실행할 수 있습니다.

```bash
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 명령어는 `node`, NPM 명령어는 `npm`으로 실행할 수 있습니다.

```nothing
sail node --version

sail npm run prod
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다.

```nothing
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기

<a name="mysql"></a>
### MySQL

`docker-compose.yml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여, 여러분이 컨테이너를 중지하거나 재시작해도 데이터베이스 데이터가 유지됩니다. 또한 MySQL 컨테이너가 시작될 때, `DB_DATABASE` 환경 변수에 지정된 이름과 동일한 데이터베이스가 자동 생성됩니다.

컨테이너가 시작된 후에는, 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정해 애플리케이션이 MySQL 인스턴스에 연결할 수 있습니다.

로컬 머신에서 MySQL 데이터베이스에 연결하려면, [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 클라이언트를 사용할 수도 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost` 3306 포트에서 접근할 수 있습니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml`에도 [Redis](https://redis.io) 컨테이너 항목이 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 활용해 중지 및 재시작 시에도 Redis 데이터가 유지됩니다. 컨테이너가 시작된 후 `.env` 파일의 `REDIS_HOST` 환경 변수를 `redis`로 설정하면 Redis 인스턴스에 연결할 수 있습니다.

로컬 머신에서 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 GUI 클라이언트도 이용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost` 6379 포트에서 접근 가능합니다.

<a name="meilisearch"></a>
### MeiliSearch

Sail 설치 시 [MeiliSearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 강력한 검색 엔진 항목이 추가됩니다. MeiliSearch는 [Laravel Scout](/docs/{{version}}/scout)과 [호환](https://github.com/meilisearch/meilisearch-laravel-scout)됩니다. 컨테이너가 시작된 후, `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정하면 애플리케이션에서 인스턴스에 연결할 수 있습니다.

로컬 머신에서는 웹브라우저에서 `http://localhost:7700`에 접속하면 MeiliSearch의 웹 관리 인터페이스에 접속할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

프로덕션 환경에서 Amazon S3를 사용하여 파일을 저장할 계획이라면 Sail 설치 시 [MinIO](https://min.io) 서비스를 추가하는 것이 유용합니다. MinIO는 S3와 호환되는 API를 제공하므로, 실제 S3에 테스트 버킷을 생성하지 않아도 로컬에서 Laravel의 `s3` 파일 스토리지 드라이버를 테스트할 수 있습니다. 설치 시 MinIO를 선택하면 관련 설정이 `docker-compose.yml`에 추가됩니다.

기본적으로, 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 설정이 포함되어 있습니다. 이 디스크는 Amazon S3뿐 아니라 MinIO 등 S3 호환 스토리지 서비스와 연결할 수 있도록 환경 변수를 적절히 설정하면 됩니다. 예를 들어 MinIO 사용 시는 다음과 같이 환경 변수를 지정할 수 있습니다:

```ini
FILESYSTEM_DRIVER=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
## 테스트 실행하기

Laravel은 강력한 테스트 지원을 기본 제공하며, Sail의 `test` 명령어로 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. PHPUnit에서 지원하는 CLI 옵션도 그대로 사용할 수 있습니다.

    sail test

    sail test --group orders

Sail의 `test` 명령어는 `test` Artisan 명령어와 동일합니다:

    sail artisan test

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 쉽고 표현력 있는 브라우저 자동화 및 테스트 API를 제공합니다. Sail을 이용하면 Selenium이나 기타 도구를 로컬에 별도로 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 먼저, 애플리케이션의 `docker-compose.yml`에서 Selenium 서비스를 주석 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

그리고 `laravel.test` 서비스가 `selenium`에 의존성을 갖도록 `depends_on` 항목에 추가하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 실행시킨 후, 다음과 같이 Dusk 테스트 스위트를 실행하면 됩니다:

    sail dusk

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium

로컬 머신이 Apple Silicon 칩(M1/M2 등)을 사용하는 경우, `selenium` 서비스에서 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다:

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 이메일 미리보기

Laravel Sail의 기본 `docker-compose.yml`에는 [MailHog](https://github.com/mailhog/MailHog) 서비스가 포함되어 있습니다. MailHog는 로컬 개발 시 애플리케이션에서 전송하는 이메일을 인터셉트하여, 웹 인터페이스를 통해 브라우저에서 확인할 수 있도록 해줍니다. Sail을 사용할 때 MailHog의 기본 호스트는 `mailhog`이고 포트는 1025입니다:

```bash
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중이면, 브라우저에서 http://localhost:8025 로 접속해 MailHog 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때때로, 애플리케이션 컨테이너 내부에서 Bash 세션을 시작하고 싶을 때가 있습니다. 이때는 `shell` 명령어로 컨테이너에 접속할 수 있으며, 파일 구조 및 설치된 서비스 확인, 임의의 쉘 명령어 실행 등이 가능합니다.

```nothing
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행하면 됩니다.

```bash
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.1, PHP 8.0, PHP 7.4에서 애플리케이션을 서비스할 수 있습니다. Sail의 기본 PHP 버전은 현재 8.1입니다. 서비스할 PHP 버전을 변경하려면, `docker-compose.yml`의 `laravel.test` 컨테이너의 `build` 항목을 원하는 PHP 버전 디렉토리로 변경하세요:

```yaml
# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

또한, PHP 버전에 맞춰 `image` 이름도 함께 수정하는 것이 좋습니다. 이 설정 역시 `docker-compose.yml`에서 지정합니다:

```yaml
image: sail-8.1/app
```

설정을 변경한 후에는 컨테이너 이미지를 다시 빌드해야 합니다:

    sail build --no-cache

    sail up

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 16을 설치합니다. 빌드 시 설치될 Node 버전을 변경하려면, `docker-compose.yml`의 `laravel.test` 서비스에 있는 `build.args` 항목의 값을 수정하세요.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

수정 후에는 컨테이너 이미지를 다시 빌드하세요.

    sail build --no-cache

    sail up

<a name="sharing-your-site"></a>
## 사이트 공유하기

동료에게 사이트를 미리 보여주거나 웹훅 통합 같은 외부 테스트가 필요할 때, `share` 명령어로 사이트를 외부에 공개할 수 있습니다. 명령어 실행 시 무작위의 `laravel-sail.site` 도메인이 발급되며, 해당 URL로 애플리케이션을 외부에 공유할 수 있습니다:

    sail share

`share` 기능을 사용할 때는, 애플리케이션의 `TrustProxies` 미들웨어에서 신뢰하는 프록시를 반드시 올바르게 지정해야 합니다. 이를 설정하지 않으면 `url`, `route`와 같은 헬퍼가 올바른 HTTP 호스트를 판별하지 못할 수 있습니다:

    /**
     * 애플리케이션의 신뢰하는 프록시들
     *
     * @var array|string|null
     */
    protected $proxies = '*';

공유 도메인의 하위 도메인을 직접 지정하려면, `subdomain` 옵션을 사용하세요:

    sail share --subdomain=my-sail-site

> {tip} `share` 명령어는 [BeyondCode](https://beyondco.de)가 개발한 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose) 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기

Laravel Sail의 Docker 구성은 PHP용 인기 디버거인 [Xdebug](https://xdebug.org/)를 지원합니다. Xdebug를 활성화하려면, 애플리케이션의 `.env` 파일에 [Xdebug 설정](https://xdebug.org/docs/step_debug#mode)을 위한 변수를 몇 가지 추가해야 합니다. Xdebug를 활성화하려면 Sail을 시작하기 전에 적절한 모드를 지정해야 합니다.

```ini
SAIL_XDEBUG_MODE=develop,debug
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어 있어 Mac 및 Windows(WSL2) 환경에서 Xdebug가 자동으로 설정됩니다. 그러나 로컬 머신이 Linux라면 이 환경 변수를 수동으로 지정해야 합니다.

아래 커맨드를 실행해 환경 변수에 입력할 올바른 호스트 IP 주소를 얻으세요(`container-name`에는 애플리케이션을 서비스하는 컨테이너 이름을 넣습니다. 보통 `_laravel.test_1`로 끝납니다):

```bash
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

얻은 호스트 IP로 `.env` 파일에 아래와 같이 추가합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

Artisan 명령어 실행 시 디버깅 세션을 시작할 때는 `sail debug` 명령어를 사용할 수 있습니다.

```bash
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug 공식 설명서](https://xdebug.org/docs/step_debug#web-application)의 가이드를 따라 Xdebug 세션을 시작하세요.

PhpStorm 사용자라면, [제로 구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 JetBrain 문서를 참고하세요.

> {note} Laravel Sail은 애플리케이션을 서빙하기 위해 `artisan serve`를 사용합니다. `artisan serve` 명령어는 Laravel 8.53.0부터 `XDEBUG_CONFIG`, `XDEBUG_MODE` 변수를 지원합니다. 더 구버전(Laravel 8.52.0 이하)에서는 해당 변수를 지원하지 않으므로 디버그 연결이 불가합니다.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 본질적으로 Docker이기 때문에 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 Dockerfile을 애플리케이션에 복사하고 싶다면 아래 명령어를 실행하세요.

```bash
sail artisan sail:publish
```

이 명령어를 실행하면, Laravel Sail이 사용하는 Dockerfile 및 기타 설정 파일이 애플리케이션 루트의 `docker` 디렉토리에 복사됩니다. 커스터마이즈 후에는, `docker-compose.yml` 파일에서 애플리케이션 컨테이너의 이미지 이름을 원하는 값으로 변경할 수 있습니다. 변경 후 반드시 `build` 명령어로 이미지를 다시 빌드해야 합니다. 특히 하나의 컴퓨터에서 여러 Laravel 애플리케이션을 개발할 때는 각기 다른 이미지 이름을 지정하면 충돌을 방지할 수 있습니다.

```bash
sail build --no-cache
```
