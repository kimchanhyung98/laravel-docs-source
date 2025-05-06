# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치](#installing-sail-into-existing-applications)
    - [셸 별칭 구성](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령 실행하기](#executing-sail-commands)
    - [PHP 명령 실행](#executing-php-commands)
    - [Composer 명령 실행](#executing-composer-commands)
    - [Artisan 명령 실행](#executing-artisan-commands)
    - [Node / NPM 명령 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
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
- [Xdebug로 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이즈](#sail-customization)

<a name="introduction"></a>
## 소개

[Laravel Sail](https://github.com/laravel/sail)은 라라벨의 기본 Docker 개발 환경을 다루기 위한 가볍고 간편한 명령줄 인터페이스입니다. Sail은 Docker에 대한 사전 지식 없이도 PHP, MySQL, Redis를 활용한 라라벨 애플리케이션 구축을 빠르게 시작할 수 있도록 해줍니다.

Sail의 핵심은 프로젝트 루트에 있는 `docker-compose.yml` 파일과 `sail` 스크립트입니다. 이 스크립트는 `docker-compose.yml` 파일로 정의된 Docker 컨테이너들을 쉽게 다룰 수 있는 CLI 도구를 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 신규 라라벨 애플리케이션에 자동으로 설치되기 때문에 즉시 사용할 수 있습니다. 새 라라벨 애플리케이션을 만드는 방법은 운영체제에 맞는 라라벨 [설치 문서](/docs/{{version}}/installation#docker-installation-using-sail)를 참고하세요. 설치 과정에서 애플리케이션에서 사용할 Sail의 지원 서비스 목록을 선택할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치

기존 라라벨 애플리케이션에 Sail을 사용하고 싶다면 Composer 패키지 매니저로 Sail을 설치하면 됩니다. 아래 단계는 기존의 개발 환경에서 Composer 의존성을 설치할 수 있다는 것을 전제로 합니다:

```shell
composer require laravel/sail --dev
```

Sail을 설치한 후, `sail:install` Artisan 명령어를 실행합니다. 이 명령은 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 생성하고, Docker 서비스와 연결할 수 있도록 `.env` 파일을 수정해줍니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법에 대해 계속 배우려면 아래의 문서를 따라가세요:

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> Docker Desktop for Linux를 사용 중인 경우, 아래 명령으로 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 서비스를 추가하고 싶다면 `sail:add` Artisan 명령을 사용하세요:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면, `sail:install` 명령에 `--devcontainer` 옵션을 추가해 실행하세요. 이 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 만들어줍니다:

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 구성

기본적으로 Sail 명령은 모든 신규 라라벨 애플리케이션에 포함된 `vendor/bin/sail` 스크립트로 실행됩니다:

```shell
./vendor/bin/sail up
```

매번 `vendor/bin/sail`을 입력하는 대신, 명령어를 더 편하게 사용하려면 셸 별칭을 설정할 수 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

항상 사용할 수 있도록 이 별칭을 홈 디렉터리 내 셸 설정 파일(`~/.zshrc` 또는 `~/.bashrc` 등)에 추가한 후, 셸을 재시작하세요.

별칭이 설정되면, `sail` 만 입력해도 Sail 명령을 실행할 수 있습니다. 이후 예제에서는 이 별칭이 적용되었다고 가정합니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일에는 여러 Docker 컨테이너가 정의되어 있습니다. 각 컨테이너는 `docker-compose.yml` 파일의 `services` 설정 내 항목입니다. `laravel.test` 컨테이너가 애플리케이션을 제공하는 주 컨테이너입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 동작 중이지 않은지 확인하세요. 모든 Docker 컨테이너를 시작하려면 `up` 명령을 실행하세요:

```shell
sail up
```

백그라운드에서 모든 Docker 컨테이너를 실행하려면 "detached" 모드로 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너가 모두 시작되면 웹 브라우저에서 http://localhost 로 프로젝트에 접속할 수 있습니다.

컨테이너를 중지하려면, Control + C로 실행을 중지하거나, 백그라운드에서 실행 중이라면 `stop` 명령을 사용하세요:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령 실행하기

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 실행되어 로컬 컴퓨터와 분리되어 있습니다. 하지만 Sail은 임의의 PHP 명령, Artisan 명령, Composer 명령, Node / NPM 명령 등을 손쉽게 실행할 수 있도록 해줍니다.

**Laravel 공식 문서에서는 종종 Sail을 명시하지 않고 Composer, Artisan, Node / NPM 등의 명령 실행 예시를 보여줍니다.** 이는 해당 도구들이 로컬 컴퓨터에 설치되어 있다는 전제입니다. Sail을 사용해 개발하는 경우 이러한 명령도 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행...
php artisan queue:work

# Laravel Sail에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령 실행

PHP 명령은 `php` 명령어로 실행할 수 있습니다. 명령은 애플리케이션에 설정된 PHP 버전으로 실행됩니다. Sail에서 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령 실행

Composer 명령은 `composer` 명령어로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer 2.x가 포함되어 있습니다:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 애플리케이션에서 Composer 의존성 설치

팀 개발 중에 새로 코드를 내려받았다면, Sail을 포함한 모든 Composer 의존성이 설치되지 않은 상태일 수 있습니다.

이 경우, 애플리케이션 디렉터리로 이동해서 아래 명령으로 의존성을 설치하세요. 이 명령은 PHP와 Composer만 포함된 Docker 컨테이너를 이용해 설치합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지를 사용할 때는 애플리케이션에서 사용할 PHP 버전(`80`, `81`, `82`, `83`)과 일치시켜야 합니다.

<a name="executing-artisan-commands"></a>
### Artisan 명령 실행

Laravel Artisan 명령은 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령 실행

Node 명령은 `node`로, NPM 명령은 `npm`으로 실행할 수 있습니다:

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

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해, 컨테이너를 중지·재시작해도 데이터가 유지됩니다.

MySQL 컨테이너가 처음 시작되면 두 개의 데이터베이스가 생성됩니다. 하나는 `DB_DATABASE` 환경변수의 값을 가진 개발용 데이터베이스, 다른 하나는 `testing`이라는 테스트용 데이터베이스입니다. 테스트가 개발 데이터에 영향을 주지 않도록 분리해줍니다.

컨테이너를 시작한 이후엔 `.env` 파일의 `DB_HOST` 환경변수를 `mysql`로 지정해 MySQL 인스턴스와 연결할 수 있습니다.

로컬에서 애플리케이션의 MySQL DB에 연결하려면 [TablePlus](https://tableplus.com)와 같은 GUI DB 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL DB는 `localhost`의 3306 포트에서, 접근 권한은 `DB_USERNAME`, `DB_PASSWORD` 환경변수 값에 맞게 설정되어 있습니다. 또는 `root` 사용자로도 `DB_PASSWORD` 값을 비밀번호로 사용해 접속할 수 있습니다.

<a name="redis"></a>
### Redis

`docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 있습니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여, 데이터가 지속적으로 유지됩니다. 컨테이너를 시작한 후, `.env` 파일에서 `REDIS_HOST` 환경변수를 `redis`로 설정하면 연결할 수 있습니다.

로컬에서 Redis DB에 연결하고 싶다면 [TablePlus](https://tableplus.com) 등과 같은 GUI 도구를 사용할 수 있습니다. 기본적으로 6379 포트로 접근할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 검색 엔진에 대한 항목이 추가됩니다. [Laravel Scout](/docs/{{version}}/scout)와 [호환](https://github.com/meilisearch/meilisearch-laravel-scout)되며, 컨테이너를 시작한 후 `.env` 파일의 `MEILISEARCH_HOST` 환경변수 값을 `http://meilisearch:7700`으로 지정해 연결할 수 있습니다.

로컬에서 웹 기반 관리 패널은 `http://localhost:7700`에서 접근 가능합니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml` 파일에 이 고속 오픈소스 검색 엔진 항목이 추가됩니다. [Laravel Scout](/docs/{{version}}/scout#typesense)에 기본 통합되어 있습니다. 컨테이너를 시작한 후 아래 환경변수를 설정해 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬에서도 `http://localhost:8108`을 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

프로덕션 환경에서는 Amazon S3를 사용하여 파일을 저장할 예정이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 추가 설치할 것을 추천합니다. MinIO는 S3 호환 API를 제공하며, 테스트 스토리지 버킷을 별도로 생성하지 않아도 로컬 개발에서 라라벨의 `s3` 스토리지 드라이버를 활용할 수 있도록 해줍니다. MinIO 설치 시, 애플리케이션의 `docker-compose.yml`에 관련 설정이 추가됩니다.

기본적으로, 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 들어 있습니다. Amazon S3 뿐만 아니라 MinIO 등 S3 호환 파일 스토리지와도 연동하려면, 아래와 같이 환경 변수만 변경하면 됩니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO 사용 시 라라벨 Flysystem이 제대로 URL을 생성하도록 하려면, 버킷명까지 포함된 로컬 URL로 `AWS_URL` 환경변수를 설정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

MinIO 콘솔은 `http://localhost:8900`에서 접근 가능하며, 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]  
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
## 테스트 실행

라라벨은 이미 강력한 테스트 환경을 제공하며, Sail의 `test` 명령으로 [기능 및 단위 테스트](/docs/{{version}}/testing)를 쉽게 실행할 수 있습니다. PHPUnit에서 사용하는 CLI 옵션도 그대로 사용할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령은 `test` Artisan 명령과 동일합니다:

```shell
sail artisan test
```

기본적으로 Sail은 별도의 `testing` 데이터베이스를 생성해, 실제 데이터와 테스트 데이터가 섞이지 않게 합니다. 라라벨의 기본 설치에서는 `phpunit.xml` 파일도 이 테스트 DB를 사용하도록 설정됩니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 명확하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 로컬 컴퓨터에 Selenium 등 별도 도구를 설치하지 않고도 테스트를 실행할 수 있습니다. 먼저 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요:

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

다음으로, `laravel.test` 서비스에 `depends_on` 항목에 `selenium`이 포함되었는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로, Sail을 시작한 후 `dusk` 명령으로 Dusk 테스트 스위트를 실행할 수 있습니다:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서의 Selenium

로컬 장치가 Apple Silicon 칩인 경우, `selenium` 서비스는 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다:

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
## 이메일 미리보기

Laravel Sail의 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 발송되는 이메일을 가로채고, 웹 인터페이스를 통해 브라우저에서 메일 내용을 확인할 수 있게 해줍니다. Sail 사용 시 기본 Host는 `mailpit`이며 포트 1025를 통해 연결됩니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025 에서 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때로는 애플리케이션 컨테이너 내부에서 Bash 세션을 시작하고 싶을 수 있습니다. 이 경우 `shell` 명령어를 사용해 컨테이너에 접속할 수 있으며, 파일 목록 확인, 설치된 서비스 점검, 임의의 셸 명령 실행 등이 가능합니다:

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

Sail은 현재 PHP 8.3, 8.2, 8.1, 8.0 기반의 애플리케이션 실행을 지원합니다. 기본 PHP 버전은 8.3입니다. PHP 버전을 변경하려면 `docker-compose.yml`의 `laravel.test` 컨테이너의 `build` 설정을 업데이트하세요:

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

또한, 사용하는 PHP 버전에 맞게 `image` 이름도 업데이트할 수 있습니다. 이 옵션도 `docker-compose.yml`에 있습니다:

```yaml
image: sail-8.1/app
```

설정을 변경한 후에는 컨테이너 이미지를 리빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 20을 설치합니다. 설치되는 Node 버전을 바꾸려면, `docker-compose.yml`의 `laravel.test` 서비스의 `build.args` 설정을 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

변경 후에는 컨테이너 이미지를 리빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유

공개적으로 사이트를 동료에게 보여주거나 웹훅 통합을 테스트해야 할 때가 있습니다. 이럴 땐 `share` 명령을 사용할 수 있습니다. 명령 실행 시, 임의의 `laravel-sail.site` URL이 발급되어 외부에서 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

이 명령을 사용할 경우, `TrustProxies` 미들웨어에서 신뢰할 수 있는 프록시를 올바르게 설정해야 합니다. 그렇지 않으면 `url`, `route` 등에서 생성되는 URL이 올바른 호스트로 처리되지 않을 수 있습니다:

```php
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

공유 사이트의 서브도메인을 직접 지정하려면, `share` 명령에 `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` 명령은 [BeyondCode](https://beyondco.de)가 만든 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅

Laravel Sail의 Docker 설정에는 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug 활성화를 위해 몇 가지 환경 변수를 `.env` 파일에 추가해야 하며, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#mode)도 참고하세요. Xdebug를 활성화하려면 Sail 시작 전에 아래처럼 모드를 지정해야 합니다:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### Linux 호스트 IP 설정

내부적으로는 `XDEBUG_CONFIG` 환경변수가 `client_host=host.docker.internal`로 정의되어 있어 Mac 및 Windows(WSL2)에 자동 적용됩니다. 리눅스의 경우 Docker Engine 17.06.0+ 및 Compose 1.16.0+ 이상을 사용해야 하며, 아니라면 환경변수를 아래와 같이 수동 설정해야 합니다.

먼저 아래 명령으로 컨테이너에서 사용할 올바른 호스트 IP 주소를 확인하세요. `<container-name>`에는 주로 `_laravel.test_1` 등으로 끝나는 컨테이너 이름을 넣습니다.

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

확인한 IP 주소로 `.env`에 `SAIL_XDEBUG_CONFIG` 변수를 설정하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`debug` 명령은 Artisan 명령 실행 시 디버깅 세션을 시작합니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저로 애플리케이션을 접속하며 디버깅하려면, [Xdebug 안내](https://xdebug.org/docs/step_debug#web-application)를 따라 브라우저에서 Xdebug 세션을 시작하세요.

PhpStorm을 사용한다면 [제로-구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrain 공식 문서를 참고하세요.

> [!WARNING]  
> Laravel Sail은 애플리케이션 서비스를 위해 `artisan serve`를 활용합니다. `artisan serve`는 Laravel 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수만 지원합니다. 8.52.0 이하 버전에서는 디버깅 연결이 제대로 동작하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이즈

Sail은 Docker 기반 서비스이므로 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 Dockerfile 및 설정 파일을 직접 서버에 배포하려면 아래의 명령을 실행하세요:

```shell
sail artisan sail:publish
```

이 명령을 실행하면, Laravel Sail에서 사용하는 Dockerfile 및 기타 설정 파일이 애플리케이션 루트의 `docker` 디렉터리로 복사됩니다. 커스터마이즈 후에는 애플리케이션 컨테이너 이미지의 이름을 변경하고, 그에 맞게 `build` 명령으로 컨테이너를 리빌드해야 합니다. 하나의 장치에서 여러 라라벨 앱을 Sail로 개발한다면, 이미지 이름을 고유하게 지정하는 것이 중요합니다:

```shell
sail build --no-cache
```
