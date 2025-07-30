# Laravel Sail (라라벨 세일)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Bash 별칭(alias) 설정하기](#configuring-a-bash-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행하기](#executing-php-commands)
    - [Composer 명령어 실행하기](#executing-composer-commands)
    - [Artisan 명령어 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령어 실행하기](#executing-node-npm-commands)
- [데이터베이스와 연동하기](#interacting-with-sail-databases)
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

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 경량 명령줄 인터페이스(CLI)입니다. Sail은 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축하는 데 훌륭한 출발점을 제공하며, Docker에 대한 사전 지식이 없어도 쉽게 사용할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너를 편리하게 관리할 수 있는 CLI 명령어들을 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows (WSL2를 통한) 환경을 지원합니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 새 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다. 새로운 Laravel 애플리케이션 생성 방법은 운영체제에 맞는 Laravel의 [설치 문서](/docs/{{version}}/installation)를 참고하세요. 설치 과정에서 애플리케이션이 상호작용할 Sail 지원 서비스들을 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에 Sail을 사용하고자 한다면, Composer 패키지 매니저를 통해 간단히 설치할 수 있습니다. 물론, 이 과정은 기존 로컬 개발 환경에 Composer 의존성 설치가 가능하다는 전제 하에 수행해야 합니다:

```
composer require laravel/sail --dev
```

Sail 설치가 완료되면, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 게시(publish)합니다:

```
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 알고 싶다면 이 문서의 나머지 부분을 계속 읽어보세요:

```
./vendor/bin/sail up
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가할 수 있습니다. 이 옵션을 사용하면 기본 `.devcontainer/devcontainer.json` 파일이 애플리케이션 루트에 게시됩니다:

```
php artisan sail:install --devcontainer
```

<a name="configuring-a-bash-alias"></a>
### Bash 별칭(alias) 설정하기

기본적으로 Sail 명령어는 모든 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 호출됩니다:

```bash
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail` 을 입력하는 대신, Bash 별칭을 설정하여 Sail 명령어를 더 간편하게 실행할 수 있습니다:

```bash
alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'
```

별칭 설정 후에는 단순히 `sail` 만 입력해 Sail 명령어를 실행할 수 있습니다. 이 문서의 예제들은 이 별칭 설정이 되어 있다고 가정합니다:

```bash
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션 개발에 필요한 여러 Docker 컨테이너들을 정의합니다. 이 컨테이너들은 `docker-compose.yml` 파일 내 `services` 설정 안에 각각 항목으로 존재합니다. `laravel.test` 컨테이너는 주요 애플리케이션 컨테이너로, 애플리케이션 서비스를 담당합니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이 아닌지 확인하세요. 애플리케이션의 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작하려면 다음 `up` 명령어를 실행합니다:

```bash
sail up
```

백그라운드에서 모든 컨테이너를 실행하려면 "분리(detached)" 모드로 시작할 수 있습니다:

```bash
sail up -d
```

컨테이너가 시작되면, 웹 브라우저에서 http://localhost 로 프로젝트에 접속할 수 있습니다.

컨테이너를 중지하려면, 실행 중인 터미널에서 Control + C를 눌러 정지하거나, 백그라운드 실행 시 `stop` 명령어를 사용할 수 있습니다:

```bash
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 격리된 상태로 실행됩니다. 하지만 Sail은 임의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어 등 다양한 애플리케이션 관련 명령어들을 편리하게 실행할 수 있도록 지원합니다.

**라라벨 공식 문서에서 종종 Composer, Artisan, Node / NPM 명령어가 Sail과 무관하게 설명되는 경우가 있습니다.** 이는 해당 도구들이 로컬 컴퓨터에 직접 설치되어 있다고 가정하는 예시입니다. Sail을 로컬 개발 환경으로 사용하는 경우, 이러한 명령어는 Sail을 통해 실행해야 합니다:

```bash
# 로컬에서 Artisan 명령어 실행하기...
php artisan queue:work

# Laravel Sail 내부에서 Artisan 명령어 실행하기...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기

PHP 명령어는 `php` 명령어를 통해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전을 따릅니다. Laravel Sail에서 사용할 수 있는 PHP 버전에 관해서는 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```bash
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Laravel Sail 애플리케이션 컨테이너에는 Composer 2.x가 기본으로 설치되어 있습니다:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 프로젝트의 Composer 의존성 설치하기

팀 협업 중이라면 애플리케이션을 생성한 사람이 아니기에, 애플리케이션 저장소를 클론한 후에는 Sail을 포함한 Composer 의존성들이 설치되지 않은 상태일 수 있습니다.

애플리케이션 디렉터리로 이동한 뒤, 다음 명령어를 실행해 의존성을 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 소형 Docker 컨테이너를 이용해 설치합니다:

```nothing
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v $(pwd):/var/www/html \
    -w /var/www/html \
    laravelsail/php81-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지를 사용할 때는, 애플리케이션에서 사용할 PHP 버전(`74`, `80`, 또는 `81`)과 동일한 버전을 사용해야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행하기

Laravel Artisan 명령어는 `artisan` 명령어로 실행할 수 있습니다:

```bash
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행하기

Node 명령어는 `node` 명령으로, NPM 명령어는 `npm` 명령으로 실행할 수 있습니다:

```nothing
sail node --version

sail npm run prod
```

필요하다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```nothing
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 연동하기

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 컨테이너 중지 및 재시작에도 유지되도록 합니다. 또한 MySQL 컨테이너 시작 시, `.env` 파일에 설정된 `DB_DATABASE` 환경 변수 값과 일치하는 데이터베이스가 자동으로 생성됩니다.

컨테이너가 실행된 뒤에는, `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정해 애플리케이션에서 MySQL에 연결할 수 있습니다.

로컬 머신에서 애플리케이션 MySQL 데이터베이스에 접속하려면, [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL 접속은 `localhost`의 3306번 포트를 사용합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 Redis 데이터를 유지합니다. 컨테이너 실행 후에는 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `redis`로 설정해 Redis에 연결할 수 있습니다.

로컬 머신에서 Redis 데이터베이스에 접속하려면, TablePlus 같은 GUI 도구를 활용할 수 있습니다. 기본 접속은 `localhost`의 6379번 포트를 사용합니다.

<a name="meilisearch"></a>
### MeiliSearch

Sail 설치 시 [MeiliSearch](https://www.meilisearch.com) 서비스를 선택하면, `docker-compose.yml` 파일에 MeiliSearch 컨테이너 항목이 포함됩니다. MeiliSearch는 [Laravel Scout](/docs/{{version}}/scout)와 호환되는 강력한 검색 엔진입니다. 컨테이너를 시작한 후 `.env` 파일에서 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정해 애플리케이션 내에서 접근할 수 있습니다.

로컬 머신에서는 웹 브라우저에서 `http://localhost:7700` 으로 접속해 MeiliSearch의 웹 관리 패널을 사용할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

프로덕션 환경에서 Amazon S3를 파일 저장소로 사용할 계획이라면, 로컬 개발 과정에서는 [MinIO](https://min.io) 서비스를 설치하는 것을 권장합니다. MinIO는 S3 호환 API를 제공해, 로컬에서 Laravel의 `s3` 파일 스토리지 드라이버를 사용하며 프로덕션 S3 환경에 테스트용 버킷을 만들지 않아도 됩니다. Sail 설치 시 MinIO를 선택하면, `docker-compose.yml` 파일에 MinIO 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정파일에는 `s3` 디스크 구성이 포함되어 있습니다. Amazon S3 이외에도 MinIO 같은 S3 호환 파일 저장소를 사용할 수 있으며, 관련 환경 변수만 수정하면 됩니다. 예를 들어 MinIO를 사용할 경우 환경 변수는 다음과 같이 설정해야 합니다:

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

Laravel은 강력한 테스트 기능을 기본 제공하며, Sail의 `test` 명령어로 애플리케이션의 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. PHPUnit에서 지원하는 모든 CLI 옵션도 `test` 명령에 전달 가능합니다:

```
sail test

sail test --group orders
```

Sail의 `test` 명령은 `artisan test` 명령과 동등합니다:

```
sail artisan test
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium이나 기타 도구를 로컬 컴퓨터에 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

또한, `laravel.test` 서비스에 `depends_on` 항목으로 `selenium`이 포함되어 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로 Sail을 시작한 뒤 `dusk` 명령어로 테스트를 실행할 수 있습니다:

```
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon(애플 실리콘) 환경의 Selenium

로컬 머신이 Apple Silicon 칩 기반이라면, `selenium` 서비스는 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다:

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

Laravel Sail 기본 `docker-compose.yml` 파일에는 [MailHog](https://github.com/mailhog/MailHog) 서비스가 포함되어 있습니다. MailHog는 로컬 개발 중 애플리케이션에서 송신되는 이메일을 가로채 웹 인터페이스를 통해 브라우저에서 이메일을 미리 볼 수 있게 합니다. Sail을 사용할 때 MailHog 기본 호스트는 `mailhog`이며 1025번 포트를 통해 접근할 수 있습니다:

```bash
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025 에 접속해 MailHog 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

종종 애플리케이션 컨테이너 내에서 Bash 세션을 시작해 파일, 설치 서비스 등을 검사하거나 임의의 셸 명령어를 실행하고 싶을 수 있습니다. 이때 `shell` 명령어를 사용하면 애플리케이션 컨테이너에 접속할 수 있습니다:

```nothing
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행하세요:

```bash
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.1, PHP 8.0, PHP 7.4 버전을 지원합니다. 기본 PHP 버전은 PHP 8.1입니다. 애플리케이션을 제공할 PHP 버전을 변경하려면 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 컨테이너의 `build` 정의에서 `context` 값을 변경하세요:

```yaml
# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

또한, 사용할 PHP 버전을 반영하도록 `image` 이름을 변경할 수 있습니다. 이 옵션도 `docker-compose.yml` 파일에 정의되어 있습니다:

```yaml
image: sail-8.1/app
```

`docker-compose.yml`을 수정한 뒤에는 컨테이너 이미지를 재빌드해야 합니다:

```
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 16을 설치합니다. 이미지 빌드 시 설치되는 Node 버전을 변경하려면 애플리케이션 `docker-compose.yml` 파일의 `laravel.test` 서비스 내 `build.args.NODE_VERSION` 값을 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

`docker-compose.yml` 수정 후에는 컨테이너 이미지를 재빌드하세요:

```
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기

동료에게 사이트를 보여주거나 애플리케이션 Webhook 연동을 테스트하려면, `share` 명령어를 사용해 사이트를 공개할 수 있습니다. 이 명령어 실행 후, 무작위 `laravel-sail.site` URL이 발급되고 이를 통해 애플리케이션에 접근할 수 있습니다:

```
sail share
```

사이트 공유 시에는 `TrustProxies` 미들웨어 내 애플리케이션의 신뢰할 수 있는 프록시 설정을 반드시 구성해야 합니다. 그렇지 않으면 URL 생성 헬퍼(`url`, `route` 등)가 올바른 HTTP 호스트를 판단하지 못합니다:

```php
/**
 * This application’s trusted proxies.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

공유 사이트에 서브도메인을 지정하고 싶다면 `share` 명령어에 `--subdomain` 옵션을 사용할 수 있습니다:

```
sail share --subdomain=my-sail-site
```

> [!TIP]
> `share` 명령어는 [BeyondCode](https://beyondco.de)에서 개발한 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)를 기반으로 합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기

Laravel Sail Docker 구성에는 PHP용 인기 있는 강력 디버거 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면, 애플리케이션 `.env` 파일에 몇 가지 변수를 추가해 [Xdebug 설정](https://xdebug.org/docs/step_debug#mode)을 구성해야 합니다. Sail 시작 전 적절한 모드를 설정해야 합니다:

```ini
SAIL_XDEBUG_MODE=develop,debug
```

#### Linux 호스트 IP 설정

기본적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal` 로 정의되어 있어 Mac과 Windows(WSL2) 환경에서 Xdebug가 적절히 작동합니다. 하지만 로컬 머신이 Linux 환경이라면 이 환경 변수를 직접 정의해야 합니다.

먼저, 다음 명령어를 실행해 올바른 호스트 IP 주소를 확인하세요. `<container-name>`은 애플리케이션을 제공하는 컨테이너 이름으로 보통 `_laravel.test_1`로 끝납니다:

```bash
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

IP 주소를 확인한 후, `.env` 파일에 `SAIL_XDEBUG_CONFIG` 변수를 아래와 같이 정의합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`artisan` 명령 실행 시 디버깅 세션을 시작하려면, `sail debug` 명령을 사용할 수 있습니다:

```bash
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug 모드에서 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)에 따라 웹 브라우저에서 Xdebug 세션을 시작하는 방법을 참조하세요.

PhpStorm 사용자는 JetBrains의 [제로-설정 디버깅 문서](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)를 확인하세요.

> [!NOTE]
> Laravel Sail은 내부적으로 `artisan serve` 명령으로 애플리케이션을 제공합니다. `artisan serve` 명령은 Laravel 버전 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 그 이전 버전(8.52.0 및 이하)은 이 변수를 지원하지 않으며 디버그 연결이 허용되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 단순히 Docker 환경이므로, 자유롭게 거의 모든 부분을 커스터마이징할 수 있습니다. Sail의 자체 Dockerfile들을 게시하려면 `sail:publish` 명령어를 실행하세요:

```bash
sail artisan sail:publish
```

이 명령어 이후, Laravel Sail에서 사용하는 Dockerfile 및 기타 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 생성됩니다. Sail 설치를 커스터마이징한 뒤에는 `docker-compose.yml` 파일에서 애플리케이션 컨테이너 이미지 이름을 변경할 수 있습니다. 변경 후에는 컨테이너를 `build` 명령어로 다시 빌드하세요. 하나의 머신에서 여러 Laravel 애플리케이션을 개발한다면 이미지 이름을 고유하게 지정하는 것이 특히 중요합니다:

```bash
sail build --no-cache
```