# Laravel Sail

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [셸 별칭(shell alias) 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령 실행하기](#executing-sail-commands)
    - [PHP 명령 실행하기](#executing-php-commands)
    - [Composer 명령 실행하기](#executing-composer-commands)
    - [Artisan 명령 실행하기](#executing-artisan-commands)
    - [Node / NPM 명령 실행하기](#executing-node-npm-commands)
- [데이터베이스와의 상호작용](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [MeiliSearch](#meilisearch)
- [파일 스토리지](#file-storage)
- [테스트 실행](#running-tests)
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

[Laravel Sail](https://github.com/laravel/sail)은 라라벨의 기본 Docker 개발 환경과 상호작용할 수 있는 가벼운 커맨드 라인 인터페이스(CLI)입니다. Sail은 PHP, MySQL, Redis를 활용하여 Docker에 대한 경험이 없어도 쉽게 라라벨 애플리케이션을 구축할 수 있는 훌륭한 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. 이 `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너와 편리하게 상호작용할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정

Laravel Sail은 모든 새로운 라라벨 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 새로운 라라벨 애플리케이션 생성 방법은 운영체제별 라라벨 [설치 문서](/docs/{{version}}/installation)를 참고하세요. 설치 과정에서 Sail이 지원하는 서비스 중 어떤 것과 애플리케이션이 연동될지 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 라라벨 애플리케이션에서 Sail을 사용하려면 Composer 패키지 매니저를 통해 Sail을 설치할 수 있습니다. 물론, 이는 기존 로컬 개발 환경에서 Composer 의존성 설치가 가능한 경우를 전제로 합니다.

```shell
composer require laravel/sail --dev
```

Sail이 설치된 후에는 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 복사해줍니다:

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 학습하려면 문서의 나머지 부분을 계속 읽어주세요:

```shell
./vendor/bin/sail up
```

<a name="adding-additional-services"></a>
#### 추가 서비스 설치

기존 Sail 설치에 추가 서비스를 더하고 싶다면, `sail:add` Artisan 명령어를 실행할 수 있습니다:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하려면, `sail:install` 명령에 `--devcontainer` 옵션을 추가하세요. 이 옵션을 사용하면, 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일이 생성됩니다:

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭(shell alias) 설정하기

기본적으로 Sail 명령어는 모든 새로운 라라벨 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 호출합니다:

```shell
./vendor/bin/sail up
```

하지만 Sail 명령어를 반복해서 입력하는 대신, 셸 별칭(alias)을 설정하면 더 쉽게 명령을 실행할 수 있습니다:

```shell
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
```

이 별칭을 항상 사용할 수 있도록, 홈 디렉터리의 셸 설정 파일(`~/.zshrc` 또는 `~/.bashrc` 등)에 추가하고 셸을 재시작하세요.

별칭 설정이 완료되면, 이제 `sail`만 입력해서 Sail 명령을 실행할 수 있습니다. 이 문서 뒷부분의 예시들은 별칭 설정을 전제로 하고 있습니다:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `docker-compose.yml` 파일은 라라벨 애플리케이션 개발에 도움이 되는 다양한 Docker 컨테이너를 정의합니다. 각 컨테이너는 `docker-compose.yml`파일의 `services` 설정에 포함되어 있습니다. `laravel.test` 컨테이너는 실제로 애플리케이션을 서비스하는 주요 컨테이너입니다.

Sail을 시작하기 전, 로컬 컴퓨터에서 별도의 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 애플리케이션의 `docker-compose.yml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령을 실행합니다:

```shell
sail up
```

모든 컨테이너를 백그라운드에서 실행하려면 "detached" 모드로 시작할 수 있습니다:

```shell
sail up -d
```

컨테이너들이 시작되면, 웹 브라우저에서 http://localhost로 프로젝트에 접속할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C 를 누르면 되고, 컨테이너가 백그라운드에서 실행 중이라면 `stop` 명령을 사용할 수 있습니다:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령 실행하기

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되므로 로컬 컴퓨터와 격리되어 있습니다. 그러나 Sail은 다양한 명령(PHP, Artisan, Composer, Node/NPM 등)을 컨테이너 내에서 쉽게 실행할 수 있도록 도와줍니다.

**라라벨 공식 문서에서 Sail 언급 없이 Composer, Artisan, Node/NPM 명령이 나오더라도, 이는 해당 도구가 로컬에 설치되었음을 전제로 합니다.** 로컬 개발 환경에서 Sail을 사용 중이라면, 이러한 명령도 Sail을 통해 실행해야 합니다:

```shell
# 로컬에서 Artisan 명령 실행...
php artisan queue:work

# Laravel Sail 내에서 Artisan 명령 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령 실행하기

PHP 명령은 `php` 명령어로 실행할 수 있습니다. 이 때 사용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Sail에서 지원하는 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요:

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령 실행하기

Composer 명령은 `composer` 명령어로 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer 2.x가 기본 설치되어 있습니다:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 기존 애플리케이션 Composer 의존성 설치

팀 단위로 개발 시, 애플리케이션을 처음 만드는 사람이 아닐 수도 있습니다. 이 경우 레포지토리를 클론해도 Composer 의존성(예: Sail 포함)이 설치되지 않은 상태입니다.

이럴 때는 애플리케이션 디렉터리로 이동하여 아래 명령어를 실행해 의존성을 설치하세요. 이 명령어는 PHP와 Composer를 포함한 작은 Docker 컨테이너를 사용해 의존성 설치를 진행합니다:

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php82-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` 이미지를 사용할 때, 애플리케이션에 사용할 PHP 버전(`74`, `80`, `81`, `82`)에 맞는 이미지를 선택하세요.

<a name="executing-artisan-commands"></a>
### Artisan 명령 실행하기

Laravel Artisan 명령은 `artisan` 명령어로 실행할 수 있습니다:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령 실행하기

Node 명령은 `node`, NPM 명령은 `npm` 명령어로 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와의 상호작용

<a name="mysql"></a>
### MySQL

애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너 중지 및 재시작 시에도 데이터가 보존됩니다.

또한 MySQL 컨테이너가 처음 실행될 때, 두 개의 데이터베이스를 생성합니다. 첫 번째는 `DB_DATABASE` 환경 변수 값으로 이름이 정해지며, 개발용 데이터베이스입니다. 두 번째는 테스트 전용인 `testing` 데이터베이스로, 테스트 데이터가 개발 데이터와 혼동되지 않도록 합니다.

컨테이너를 시작한 후, `.env` 파일의 `DB_HOST` 환경 변수를 `mysql`로 지정하면 애플리케이션이 MySQL 인스턴스와 연결됩니다.

로컬 컴퓨터에서 GUI 데이터베이스 관리 툴([TablePlus](https://tableplus.com) 등)을 사용해 MySQL 데이터베이스에 접속할 수 있습니다. 기본적으로는 `localhost` 3306 포트에서, 접근 정보는 `DB_USERNAME` 및 `DB_PASSWORD` 환경 변수와 동일하게 설정됩니다. 또는 `root` 사용자로도 접속할 수 있으며, 이 때도 `DB_PASSWORD`를 사용합니다.

<a name="redis"></a>
### Redis

애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 보존됩니다. 컨테이너를 시작한 후, `.env` 파일의 `REDIS_HOST` 환경 변수를 `redis`로 지정하면 애플리케이션 내에서 Redis에 연결할 수 있습니다.

로컬 컴퓨터에서 [TablePlus](https://tableplus.com)와 같은 툴로 Redis 데이터베이스에 접속할 수 있습니다. 기본 포트는 6379입니다.

<a name="meilisearch"></a>
### MeiliSearch

Sail 설치 시 [MeiliSearch](https://www.meilisearch.com) 서비스를 선택했다면, 애플리케이션의 `docker-compose.yml` 파일에 이 강력한 검색 엔진([Laravel Scout](/docs/{{version}}/scout)과 [호환](https://github.com/meilisearch/meilisearch-laravel-scout))이 추가됩니다. 컨테이너를 시작한 후, 애플리케이션 내에서 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`로 설정하면 연결됩니다.

로컬 머신에서 웹 브라우저로 `http://localhost:7700`에 접속하면 MeiliSearch 웹 관리 패널을 사용할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지

프로덕션 환경에서 Amazon S3를 파일 저장소로 사용할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 설치할 수 있습니다. MinIO는 S3 호환 API를 제공하므로, 프로덕션 S3 환경에 "테스트" 버킷을 만들지 않아도 로컬에서 Laravel의 `s3` 파일 스토리지 드라이버를 사용할 수 있습니다. MinIO 선택 시 관련 설정이 `docker-compose.yml`에 추가됩니다.

`filesystems` 설정 파일에는 기본적으로 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크를 Amazon S3뿐 아니라 MinIO 같이 S3 호환 서비스에도 사용할 수 있습니다. 환경변수만 적절히 수정하면 됩니다. 예를 들어, MinIO 사용 시 환경변수 예시는 다음과 같습니다:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO 사용 시 Flysystem이 올바른 URL을 생성할 수 있도록, `AWS_URL` 환경 변수도 다음과 같이 정의하세요:

```ini
AWS_URL=http://localhost:9000/local
```

버킷은 MinIO 콘솔(`http://localhost:8900`)에서 생성할 수 있습니다. 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> **경고**  
> MinIO를 사용할 때 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원하지 않습니다.

<a name="running-tests"></a>
## 테스트 실행

라라벨은 뛰어난 테스트 지원을 기본 제공하며, Sail의 `test` 명령어를 통해 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. PHPUnit이 지원하는 CLI 옵션도 함께 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령 실행과 동일한 동작입니다:

```shell
sail artisan test
```

기본적으로, Sail은 테스트가 현재 데이터베이스 상태에 영향을 주지 않도록 전용 `testing` 데이터베이스를 생성합니다. 기본 라라벨 설치에서는 Sail이 `phpunit.xml`에서도 이 데이터베이스를 사용하도록 자동 설정합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 & 테스트 API를 제공합니다. Sail 덕분에 Selenium이나 기타 도구를 로컬 컴퓨터에 별도로 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 먼저, 애플리케이션의 `docker-compose.yml`에서 Selenium 서비스를 주석 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

그리고 `docker-compose.yml` 파일의 `laravel.test` 서비스에 `selenium`을 `depends_on`에 추가합니다:

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
#### Apple Silicon에서의 Selenium

로컬 머신이 Apple Silicon 칩을 사용한다면, `selenium` 서비스의 이미지를 `seleniarm/standalone-chromium`으로 지정해야 합니다:

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

Laravel Sail 기본 `docker-compose.yml`에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 로컬 개발 시 애플리케이션에서 발송된 이메일을 가로채며, 웹 인터페이스를 통해 이메일을 확인할 수 있습니다. Sail 사용 시 Mailpit 기본 호스트는 `mailpit`, 포트는 1025입니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025에서 Mailpit 웹 인터페이스를 확인할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때때로 애플리케이션 컨테이너 내부에 Bash 세션을 시작하고 싶을 수 있습니다. `shell` 명령어를 사용해 컨테이너에 접속하면, 컨테이너 내부의 파일 및 서비스 확인, 임의 shell 명령 실행 등이 가능합니다:

```shell
sail shell

sail root-shell
```

[Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 사용하세요:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.2, 8.1, 8.0, 7.4에서 애플리케이션을 서비스할 수 있습니다. 기본 PHP 버전은 8.2입니다. PHP 버전을 변경하려면, `docker-compose.yml`의 `laravel.test` 컨테이너의 `build` 정의를 수정하세요:

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

그리고 `image` 이름도 맞게 수정하는 것이 좋습니다. 이 옵션 역시 `docker-compose.yml`에 정의되어 있습니다:

```yaml
image: sail-8.1/app
```

수정 후에는 컨테이너 이미지를 다시 빌드하세요:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전

Sail은 기본적으로 Node 18을 설치합니다. 이미지 빌드 시 설치할 Node 버전을 변경하려면, `docker-compose.yml`의 `laravel.test` 서비스에 있는 `build.args`를 수정하세요:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

수정 후, 컨테이너 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기

가끔 동료에게 사이트를 미리 보여주거나 웹훅 등 외부 연동 테스트를 위해 사이트를 외부에 공유해야 할 수도 있습니다. 이럴 땐 `share` 명령어를 사용하세요. 명령 실행 후 임의의 `laravel-sail.site` URL이 생성되며, 이를 통해 애플리케이션에 접근할 수 있습니다:

```shell
sail share
```

`share` 명령어로 사이트를 공유할 때는, `TrustProxies` 미들웨어에서 애플리케이션의 신뢰하는 프록시(trusted proxies)를 설정하세요. 그렇지 않으면 URL 생성 헬퍼(`url`, `route` 등)가 올바른 HTTP 호스트를 결정하지 못할 수 있습니다:

```php
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

공유 사이트의 서브도메인을 직접 지정하고 싶다면, `subdomain` 옵션을 사용할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```

> **참고**  
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈 소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)로 구동됩니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기

Laravel Sail의 Docker 설정에는 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug는 PHP를 위한 강력한 디버거입니다. Xdebug를 활성화하려면, 몇 가지 변수를 애플리케이션의 `.env` 파일에 추가하여 [Xdebug를 설정](https://xdebug.org/docs/step_debug#mode)해야 합니다. Sail 시작 전, 활성화할 모드에 맞게 환경변수를 설정하세요:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### 리눅스 호스트 IP 설정

내부적으로, `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있어 Mac 및 Windows(WSL2)에서는 자동으로 설정됩니다. 리눅스에서 사용할 경우, Docker Engine 17.06.0+ 및 Compose 1.16.0+를 사용 중임을 확인하세요. 아니라면 아래와 같이 직접 환경 변수를 설정해야 합니다.

우선, 다음 명령어로 올바른 호스트 IP 주소를 확인합니다. 일반적으로 `<container-name>`은 `_laravel.test_1`로 끝나는 애플리케이션 서비스 컨테이너의 이름입니다:

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

확인한 IP 주소를 `.env` 파일의 `SAIL_XDEBUG_CONFIG` 변수에 추가합니다:

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`artisan` 명령 실행 시 디버깅 세션을 시작하려면 `sail debug` 명령을 사용할 수 있습니다:

```shell
# Xdebug 없이 Artisan 명령 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

브라우저를 통해 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug 공식 문서](https://xdebug.org/docs/step_debug#web-application)를 참고하여 웹 브라우저에서 세션을 시작하세요.

PhpStorm을 사용한다면 [무설정(zero-configuration) 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 JetBrain 공식 문서를 참고하세요.

> **경고**  
> Laravel Sail은 애플리케이션 실행에 `artisan serve`를 사용합니다. 이 명령은 Laravel 8.53.0부터 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 지원합니다. 구버전 Laravel(8.52.0 이하)은 이 변수를 지원하지 않아 디버깅 연결이 불가합니다.

<a name="sail-customization"></a>
## 커스터마이징

Sail은 Docker 기반이므로 거의 모든 부분을 자유롭게 커스터마이징할 수 있습니다. Sail 자체 Dockerfile을 배포하려면 다음 명령어를 실행하세요:

```shell
sail artisan sail:publish
```

실행하면 사용 중인 Dockerfile 등 설정 파일이 애플리케이션 루트의 `docker` 디렉터리에 배치됩니다. Sail 설치를 커스터마이즈했다면, `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름도 수정할 수 있습니다. 이후에는 `build` 명령어로 컨테이너를 다시 빌드하세요. 특히 한 머신에서 여러 라라벨 애플리케이션을 Sail로 개발하는 경우 고유의 이미지 이름을 부여하는 것이 좋습니다:

```shell
sail build --no-cache
```