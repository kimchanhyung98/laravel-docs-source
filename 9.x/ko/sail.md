# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [쉘 별칭 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행하기](#executing-php-commands)
    - [Composer 명령어 실행하기](#executing-composer-commands)
    - [Artisan 명령어 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령어 실행하기](#executing-node-npm-commands)
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
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 가벼운 커맨드라인 인터페이스입니다. Sail은 PHP, MySQL, Redis를 사용하는 Laravel 애플리케이션 개발을 위한 훌륭한 출발점을 제공하며, Docker에 대한 사전 경험이 필요하지 않습니다.

Sail의 핵심은 `docker-compose.yml` 파일과 프로젝트 루트에 저장된 `sail` 스크립트입니다. 이 `sail` 스크립트는 `docker-compose.yml`에 정의된 Docker 컨테이너와 상호작용하기 위한 편리한 CLI 인터페이스를 제공합니다.

Laravel Sail은 macOS, Linux, Windows(WSL2를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

Laravel Sail은 모든 새 Laravel 애플리케이션에 자동으로 설치되므로 바로 사용할 수 있습니다. 새로운 Laravel 애플리케이션 생성 방법은 운영체제에 맞는 Laravel [설치 문서](/docs/9.x/installation)를 참고하세요. 설치 과정에서 애플리케이션에서 사용할 Sail 지원 서비스 선택을 요청받게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에 Sail을 사용하려면 Composer 패키지 매니저를 통해 Sail을 설치하면 됩니다. 물론, 이러한 과정은 로컬 개발 환경에서 Composer 의존성 설치가 가능한 경우에 해당합니다.

```shell
composer require laravel/sail --dev
```

Sail 설치 후에는 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 게시합니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작하세요. Sail 사용법을 계속 배우고 싶다면 문서의 나머지 부분을 읽어보세요:

```shell
./vendor/bin/sail up
```

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기 (Adding Additional Services)

기존 Sail 설치에 추가 서비스를 더하고 싶다면 `sail:add` Artisan 명령어를 실행하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기 (Using Devcontainers)

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 그러면 기본 `.devcontainer/devcontainer.json` 파일이 애플리케이션 루트에 게시됩니다:

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
### 쉘 별칭 설정하기 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용하여 호출됩니다:

```shell
./vendor/bin/sail up
```

하지만 매번 `vendor/bin/sail`을 입력하는 대신, 다음과 같은 쉘 별칭을 설정해 더 쉽게 Sail 명령어를 실행할 수 있습니다:

```shell
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
```

이 별칭을 항상 사용할 수 있도록 홈 디렉토리의 쉘 설정 파일(`~/.zshrc` 또는 `~/.bashrc`)에 추가한 후, 쉘을 재시작하세요.

별칭이 설정되면, `sail`만 입력해 Sail 명령어를 실행할 수 있습니다. 문서의 이후 예제들은 이 별칭이 설정되었다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting & Stopping Sail)

Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션 개발에 필요한 다양한 Docker 컨테이너들을 정의합니다. 각 컨테이너는 `docker-compose.yml` 내 `services` 설정의 항목입니다. `laravel.test` 컨테이너는 실제 애플리케이션을 서비스하는 주요 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 실행 중인 다른 웹 서버나 데이터베이스가 없는지 확인하세요. 애플리케이션의 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행하세요:

```shell
sail up
```

백그라운드에서 컨테이너를 실행하려면 "분리 모드(detached)"로 실행할 수 있습니다:

```shell
sail up -d
```

컨테이너가 시작된 뒤에는 웹 브라우저에서 http://localhost 에 접속해 프로젝트를 확인할 수 있습니다.

컨테이너를 중지하려면, 실행 중인 터미널에서 Control + C를 누르거나, 백그라운드에서 실행 중인 경우 `stop` 명령어를 사용하세요:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail 사용 시 애플리케이션은 Docker 컨테이너 내에서 실행되며 로컬 컴퓨터와 분리되어 있습니다. Sail은 PHP, Artisan, Composer, Node / NPM 명령어 등 다양한 명령어를 애플리케이션에 편리하게 실행할 수 있도록 지원합니다.

**Laravel 문서를 볼 때 종종 Composer, Artisan, Node / NPM 명령어가 Sail 없이 로컬에서 실행하는 예제를 볼 수 있는데, 이는 해당 도구들이 로컬에 설치되어 있다는 가정 하에 작성된 것입니다.** 만약 로컬 Laravel 개발 환경으로 Sail을 사용한다면, 반드시 해당 명령어를 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령어 실행...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행하기 (Executing PHP Commands)

`php` 명령어를 사용하여 PHP 명령어를 실행할 수 있습니다. 이 명령어들은 애플리케이션에 구성된 PHP 버전을 사용해 실행됩니다. Sail에서 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 확인하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행하기 (Executing Composer Commands)

`composer` 명령어로 Composer 명령어를 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer 2.x가 설치되어 있습니다:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 프로젝트에 Composer 의존성 설치하기 (Installing Composer Dependencies For Existing Applications)

팀과 함께 개발하는 애플리케이션인 경우, 직접 애플리케이션을 생성하지 않았을 수 있습니다. 따라서 애플리케이션 저장소를 클론 한 뒤에는 Sail을 포함해 Composer 의존성이 설치되어 있지 않습니다.

애플리케이션 디렉터리로 이동한 후 다음 명령어를 실행해 의존성을 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 작은 Docker 컨테이너를 사용합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php82-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지는 애플리케이션에서 사용하려는 PHP 버전에 맞춰(`74`, `80`, `81`, `82`) 선택해야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행하기 (Executing Artisan Commands)

Artisan 명령어는 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행하기 (Executing Node / NPM Commands)

Node 명령어는 `node` 명령어로, NPM 명령어는 `npm` 명령어로 실행합니다:

```shell
sail node --version

sail npm run dev
```

필요시 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여, 컨테이너를 중지하거나 재시작해도 데이터가 유지되도록 합니다.

MySQL 컨테이너가 처음 시작될 때, 두 개의 데이터베이스가 생성됩니다. 하나는 `DB_DATABASE` 환경 변수 값으로 지정되는 로컬 개발용 데이터베이스이며, 다른 하나는 `testing`이라는 테스트 전용 데이터베이스로, 테스트가 개발 데이터에 영향을 끼치지 않도록 합니다.

컨테이너를 시작한 후에는 애플리케이션 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정하면 MySQL 인스턴스에 연결할 수 있습니다.

로컬 시스템에서 그래픽 데이터베이스 관리 도구(예: [TablePlus](https://tableplus.com))를 사용해 애플리케이션 MySQL 데이터베이스에 접속할 수 있습니다. 기본적으로 MySQL은 `localhost`의 3306 포트에서 접근 가능하며, 접속 자격증명은 `.env` 파일의 `DB_USERNAME` 및 `DB_PASSWORD` 변수 값을 따릅니다. 또는 `root` 사용자로 접속할 수도 있으며, `root` 사용자도 `DB_PASSWORD` 변수값을 비밀번호로 사용합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. Redis 컨테이너 역시 Docker 볼륨을 사용하여 데이터를 유지합니다. 컨테이너가 시작된 후 애플리케이션 `.env` 파일의 `REDIS_HOST`를 `redis`로 설정하면 Redis 인스턴스에 연결할 수 있습니다.

로컬 컴퓨터에서 데이터베이스 관리 도구(예: [TablePlus](https://tableplus.com))로 접근할 수 있습니다. 기본 포트는 `localhost`의 6379입니다.

<a name="meilisearch"></a>
### MeiliSearch

Sail 설치 시 [MeiliSearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml`에 해당 검색엔진 서비스가 포함됩니다. MeiliSearch는 [Laravel Scout](/docs/9.x/scout)에서 사용할 수 있는 검색 엔진입니다. 컨테이너가 시작된 후 `.env` 파일에서 `MEILISEARCH_HOST`를 `http://meilisearch:7700`로 설정하세요.

로컬에서는 웹 브라우저를 통해 `http://localhost:7700` 에 접속해 MeiliSearch 관리 패널을 사용할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 Amazon S3를 통해 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 선택하는 것을 권장합니다. MinIO는 S3 호환 API를 제공하여, 프로덕션 환경에서 사용되는 실제 S3 버킷이 아닌 로컬 환경에서 개발용으로 사용할 수 있습니다.

MinIO를 설치하면 `docker-compose.yml`에 MinIO 구성 섹션이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일은 `s3` 디스크 구성을 포함합니다. 이를 통해 Amazon S3뿐 아니라 MinIO 같은 S3 호환 스토리지를 사용할 수 있으며, `.env` 환경 변수만 적절히 변경하면 됩니다. MinIO 사용 시, 파일시스템 환경 변수는 다음과 같이 설정해야 합니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하게 하려면 `AWS_URL` 환경 변수도 애플리케이션 로컬 URL과 버킷 이름이 포함되도록 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 http://localhost:8900 에서 사용할 수 있으며, 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 MinIO 사용 시 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행하기 (Running Tests)

Laravel은 훌륭한 테스트 지원 기능을 제공합니다. Sail의 `test` 명령어로 애플리케이션의 [기능 테스트 및 단위 테스트](/docs/9.x/testing)를 실행할 수 있습니다. PHPUnit에서 지원하는 모든 CLI 옵션도 전달 가능합니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 Artisan의 `test` 명령어와 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 테스트 중 기존 데이터베이스 상태에 영향을 주지 않도록 `testing` 전용 데이터베이스를 만듭니다. 기본 Laravel 설치에서는 `phpunit.xml` 파일도 이 데이터베이스를 사용하도록 설정되어 있습니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/9.x/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API입니다. Sail 덕분에 로컬 컴퓨터에 Selenium이나 기타 도구를 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 사용하려면 애플리케이션 `docker-compose.yml`에서 Selenium 서비스를 주석 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

`laravel.test` 서비스가 `selenium`에 의존하도록 `depends_on` 항목도 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로 Sail을 시작하고 `dusk` 명령어로 테스트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용하기

로컬 머신이 Apple Silicon 칩을 탑재한 경우, `selenium` 서비스는 다음 이미지를 사용해야 합니다:

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 이메일 미리보기 (Previewing Emails)

Laravel Sail 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 애플리케이션에서 발송하는 이메일을 가로채어 브라우저에서 미리볼 수 있도록 웹 인터페이스를 제공합니다. Mailpit 기본 호스트는 `mailpit`이며, 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때는 http://localhost:8025 에서 Mailpit 웹 인터페이스에 접속할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너 내에서 Bash 세션을 시작하고 싶을 때는 `shell` 명령어를 사용하세요. 이 명령어는 컨테이너 내부 파일과 서비스 점검 및 임의 쉘 명령어 실행을 가능하게 합니다:

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

Sail은 현재 PHP 8.2, 8.1, 8.0, 7.4 버전을 지원하며, 기본 PHP 버전은 8.2입니다. 애플리케이션을 제공할 PHP 버전을 변경하려면 `docker-compose.yml`에서 `laravel.test` 컨테이너의 `build` 정의를 변경하세요:

```yaml
# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

또한, 애플리케이션의 `docker-compose.yml`에서 `image` 이름도 사용하려는 PHP 버전에 맞게 업데이트할 수 있습니다:

```yaml
image: sail-8.1/app
```

`docker-compose.yml`을 수정한 후에는 컨테이너 이미지를 재빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 18을 설치합니다. 이미지 빌드 시 설치될 Node 버전을 변경하려면 `docker-compose.yml`에서 `laravel.test` 서비스의 `build.args` 설정을 변경하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

`docker-compose.yml` 수정 후 컨테이너 이미지를 재빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

외부 동료에게 사이트를 공개하거나 웹훅 연동 테스트를 위해 사이트를 공유할 필요가 있을 수 있습니다. `share` 명령어로 사이트를 공유하면, 무작위 `laravel-sail.site` URL을 발급받아 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

사이트 공유 시 `TrustProxies` 미들웨어에서 애플리케이션 신뢰 프록시를 설정해야 합니다. 그렇지 않으면 `url`, `route` 같은 URL 생성 헬퍼가 올바른 호스트를 인식하지 못합니다:

```
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

공유 사이트에 원하는 서브도메인을 지정하려면, `share` 명령어 실행 시 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)에서 만든 오픈 소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)에 의해 운영됩니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 PHP용 강력한 디버거인 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면, 애플리케이션 `.env` 파일에 몇 가지 변수를 추가해 Xdebug를 [설정](https://xdebug.org/docs/step_debug#mode)해야 합니다. Sail 시작 전 적절한 모드를 설정하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 Mac과 Windows(WSL2)를 위해 `client_host=host.docker.internal`로 정의되어 있습니다. 로컬 머신이 Linux라면 Docker Engine 17.06.0 이상, Compose 1.16.0 이상 버전이 실행 중인지 확인해야 하며, 그렇지 않으면 수동으로 환경 변수를 정의해야 합니다.

먼저, 다음 명령어로 적절한 호스트 IP 주소를 확인합니다. `<container-name>`은 애플리케이션 컨테이너 이름이며 보통 `_laravel.test_1` 같은 형태입니다:

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

IP 주소를 확인한 뒤 `.env` 파일에 `SAIL_XDEBUG_CONFIG` 변수를 정의하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

`debug` 명령어로 Artisan 명령어 실행 시 디버깅 세션을 시작할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug를 사용해 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)의 안내를 참고해 브라우저에서 Xdebug 세션을 시작하세요.

PhpStorm을 사용하는 경우, JetBrain의 [제로 구성 디버깅 문서](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)도 참고하시기 바랍니다.

> [!WARNING]
> Laravel Sail은 `artisan serve`로 애플리케이션을 구동합니다. `artisan serve` 명령어는 Laravel 8.53.0부터 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 인식합니다. 그 이전 버전(8.52.0 이하)은 이 변수를 지원하지 않아 디버그 연결을 수용하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 단순히 Docker이므로 거의 모든 부분을 자유롭게 커스터마이징할 수 있습니다. Sail의 Dockerfile들을 게시하려면 `sail:publish` 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

명령어 실행 후 Laravel Sail에서 사용하는 Dockerfile과 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 생성됩니다. 커스터마이징 완료 후 `docker-compose.yml`에서 애플리케이션 컨테이너 이미지 이름을 변경할 수도 있습니다. 여러 Laravel 애플리케이션을 동일 머신에서 개발하는 경우 이미지 이름을 고유하게 지정하는 것이 중요합니다.

수정 후에는 `build` 명령어로 컨테이너 이미지를 다시 빌드하세요:

```shell
sail build --no-cache
```