# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [쉘 별칭 설정](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와의 상호작용](#interacting-with-sail-databases)
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
- [Xdebug를 이용한 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이즈](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경을 다루기 위한 경량의 커맨드라인 인터페이스입니다. Sail을 사용하면 별도의 Docker 지식 없이도 PHP, MySQL, Redis로 Laravel 애플리케이션을 손쉽게 구축할 수 있는 좋은 출발점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너와 상호작용할 수 있는 편리한 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, 그리고 Windows([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 사용)를 지원합니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치

기존 Laravel 애플리케이션에서 Sail을 사용하고자 한다면, Composer 패키지 매니저를 통해 Sail을 설치할 수 있습니다. 물론, 이 단계는 현재 개발 환경에서 Composer 종속성 설치가 가능하다는 전제하에 진행합니다.

```shell
composer require laravel/sail --dev
```

Sail 설치가 완료되면, `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 복사하고, Docker 서비스와 연결에 필요한 환경 변수들을 `.env` 파일에 추가합니다.

```shell
php artisan sail:install
```

마지막으로, Sail을 시작하면 됩니다. Sail 사용법에 대해 더 자세히 알고 싶다면, 이 문서의 나머지 부분을 계속 읽으십시오.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Docker Desktop for Linux를 사용하는 경우, 다음 명령어를 실행하여 반드시 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`. 또한, 컨테이너 내부에서 파일 권한 관련 오류가 발생하는 경우, `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 지정해야 할 수 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 설치

기존 Sail 설치에 다른 서비스를 추가하려면, `sail:add` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 전달할 수 있습니다. 이 옵션을 사용하면, 기본 `.devcontainer/devcontainer.json` 파일이 애플리케이션 루트에 생성됩니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

가끔 모든 Sail 이미지를 완전히 재빌드하여 이미지 내의 소프트웨어와 패키지를 최신 상태로 유지하고 싶을 때가 있습니다. 이럴 때는 `build` 명령어를 사용하면 됩니다.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 쉘 별칭 설정

기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함되어 있는 `vendor/bin/sail` 스크립트를 통해 실행합니다.

```shell
./vendor/bin/sail up
```

하지만, 매번 `vendor/bin/sail`을 입력하는 대신, 쉘 별칭을 설정해서 더 간편하게 Sail 명령어를 실행할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

해당 별칭을 항상 사용할 수 있도록 홈 디렉터리 내의 쉘 설정 파일(예: `~/.zshrc`, `~/.bashrc`)에 추가한 후 쉘을 재시작하면 됩니다.

별칭 설정이 완료되면, 이제 단순히 `sail`만 입력해서 Sail 명령어를 실행할 수 있습니다. 이 문서의 나머지 예제들은 모두 별칭이 설정된 환경을 전제로 합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일에는 여러 Docker 컨테이너가 정의되어 있으며, 이 컨테이너들은 함께 작동해서 Laravel 애플리케이션을 쉽게 개발할 수 있도록 돕습니다. 각 컨테이너는 `compose.yaml` 파일의 `services` 섹션에 항목으로 포함되어 있습니다. `laravel.test` 컨테이너는 실제로 애플리케이션을 서비스하는 메인 컨테이너입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행되고 있지 않은지 반드시 확인하세요. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 사용하세요.

```shell
sail up
```

모든 Docker 컨테이너를 백그라운드(Detached 모드)에서 실행하려면 다음과 같이 합니다.

```shell
sail up -d
```

애플리케이션의 컨테이너들이 모두 시작되면, 웹 브라우저에서 http://localhost 로 프로젝트에 접속할 수 있습니다.

컨테이너를 중지하려면, Control + C를 눌러 컨테이너 실행을 중지합니다. 만약 컨테이너가 백그라운드에서 실행되고 있다면, `stop` 명령어를 사용할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되므로 로컬 컴퓨터와는 분리된 상태입니다. 그러나 Sail은 PHP, Artisan, Composer, Node/NPM 등 다양한 명령어를 손쉽게 실행할 수 있도록 도와주는 편리한 방법을 제공합니다.

**Laravel 공식 문서에서는 Sail을 명시하지 않은 Composer, Artisan, Node/NPM 명령어 예제가 자주 등장합니다.** 이런 예제들은 해당 도구들이 로컬에 직접 설치되어 있을 때를 가정한 것입니다. Sail로 로컬 개발을 할 경우, 다음과 같이 Sail을 통해 명령어를 실행해야 합니다.

```shell
# 로컬에서 Artisan 명령어 실행 예시...
php artisan queue:work

# Laravel Sail에서 Artisan 명령어 실행 예시...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php`를 사용해 실행할 수 있습니다. 이런 명령어들은 애플리케이션에 설정된 PHP 버전으로 실행됩니다. Sail에서 지원하는 PHP 버전에 대한 자세한 내용은 [PHP 버전 문서](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer`를 통해 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 이미 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan`을 사용해서 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 명령어는 `node`, NPM 명령어는 `npm`으로 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

원한다면, NPM 대신 Yarn을 사용할 수도 있습니다.

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와의 상호작용 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여, 컨테이너를 중지·재시작해도 데이터가 유지됩니다.

또한, MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스를 자동으로 생성합니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수 값으로 이름이 정해지며 로컬 개발용입니다. 두 번째 데이터베이스는 `testing`이라는 이름으로, 테스트 전용 데이터베이스입니다. 이를 통해 개발 데이터와 테스트 데이터가 분리되어 안전하게 관리됩니다.

컨테이너가 시작되면, 애플리케이션에서 MySQL에 접속하려면 `.env` 파일의 `DB_HOST`를 `mysql`로 설정해야 합니다.

로컬 컴퓨터에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 GUI 기반 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost` 3306 포트에서 사용 가능하며, 접근 권한은 `DB_USERNAME`, `DB_PASSWORD` 환경 변수 값과 일치합니다. 또는, `root` 사용자로도 접속할 수 있으며 이때 비밀번호 역시 `DB_PASSWORD` 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, 애플리케이션의 `compose.yaml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너가 추가됩니다. 이는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 Atlas 기능을 포함한 MongoDB 도큐먼트 데이터베이스를 제공합니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하며, 컨테이너를 중지·재시작해도 데이터가 유지됩니다.

컨테이너가 실행되면, `.env` 파일의 `MONGODB_URI` 변수를 `mongodb://mongodb:27017`로 설정하여 애플리케이션에서 MongoDB에 접속할 수 있습니다. 인증은 기본적으로 비활성화되어 있지만, `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정하고 `mongodb` 컨테이너를 시작하면 인증을 활성화할 수 있습니다. 그 경우, 연결 문자열에 인증 정보를 추가합니다.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 애플리케이션을 원활하게 연동하려면, [MongoDB에서 공식 유지보수하는 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

그리고 [Compass](https://www.mongodb.com/products/tools/compass)와 같은 GUI 도구를 사용해, 로컬 컴퓨터에서 MongoDB 데이터베이스(`localhost` 27017 포트)에 접속할 수 있습니다.

<a name="redis"></a>
### Redis

애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하거나 재시작해도 데이터가 유지됩니다. 컨테이너가 시작되면, `.env` 파일의 `REDIS_HOST` 환경 변수 값을 `redis`로 지정하면 애플리케이션에서 Redis 인스턴스에 접속할 수 있습니다.

로컬 컴퓨터에서는 [TablePlus](https://tableplus.com) 등 GUI 데이터베이스 관리 도구로 접속할 수 있으며, 기본적으로 `localhost` 6379 포트가 사용됩니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, 애플리케이션의 `compose.yaml` 파일에 [Valkey](https://valkey.io/) 컨테이너가 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하여 데이터의 영속성을 보장합니다. 애플리케이션의 `.env` 파일에서 `REDIS_HOST`를 `valkey`로 설정하면 해당 컨테이너와 연결할 수 있습니다.

로컬 컴퓨터에서는 [TablePlus](https://tableplus.com)와 같은 GUI 관리 도구를 사용해서, 기본적으로 `localhost` 6379 포트로 Valkey 데이터베이스에 접속할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com) 서비스를 Sail 설치 시 선택했다면, 애플리케이션의 `compose.yaml` 파일에 이 강력한 검색엔진 항목이 추가됩니다. Meilisearch는 [Laravel Scout](/docs/12.x/scout)와 연동하여 사용할 수 있습니다. 컨테이너가 실행된 후, `.env` 파일에서 `MEILISEARCH_HOST` 값을 `http://meilisearch:7700`으로 변경하여 Meilisearch와 연결할 수 있습니다.

로컬 컴퓨터에서는 웹브라우저에서 `http://localhost:7700`으로 이동해 Meilisearch의 웹 관리 패널을 사용할 수 있습니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org) 서비스를 Sail 설치 시 선택했다면, 애플리케이션의 `compose.yaml` 파일에 이 빠르고 오픈소스인 검색엔진 항목이 추가됩니다. Typesense는 [Laravel Scout](/docs/12.x/scout#typesense)와도 연동됩니다. 컨테이너 실행 후, 아래와 같은 환경 변수들을 애플리케이션의 `.env` 파일에 설정하면 됩니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서는 `http://localhost:8108`을 통해 Typesense의 API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 Amazon S3를 파일 스토리지로 사용한다면, Sail 설치 시 [RustFS](https://rustfs.com) 서비스를 추가로 설치할 수 있습니다. RustFS는 S3와 호환되는 API를 지원하므로, 실제 S3 환경에 테스트용 버킷을 만들지 않고도 로컬 환경에서 Laravel의 `s3` 파일 시스템 드라이버를 자유롭게 사용할 수 있습니다. RustFS를 추가하면 `compose.yaml` 파일에도 RustFS 관련 설정이 자동으로 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 포함되어 있습니다. Amazon S3뿐 아니라 RustFS와 같이 S3 호환 서비스를 연동하려면 관련 환경 변수만 변경해주면 됩니다. RustFS 사용 시 환경 변수는 다음과 같이 설정합니다.

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 기본적으로 뛰어난 테스트 지원을 제공합니다. Sail의 `test` 명령어를 통해 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있으며, Pest나 PHPUnit에서 허용하는 모든 CLI 옵션도 함께 사용할 수 있습니다.

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

Sail은 기본적으로 테스트 전용으로 분리된 `testing` 데이터베이스를 생성하여, 테스트 실행 시 기존 데이터베이스 상태에 영향을 주지 않도록 보호합니다. 기본 Laravel 설치에서는 Sail이 `phpunit.xml` 파일에 테스트 전용 데이터베이스를 자동으로 설정해줍니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium 같은 도구를 별도로 설치하지 않아도 Dusk 테스트를 실행할 수 있습니다. 먼저, 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스 부분을 주석 해제해 주세요.

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

그 다음, `laravel.test` 서비스가 `selenium`에 의존하도록 `depends_on` 설정을 추가하세요.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

이제 Sail을 실행한 후 아래와 같이 `dusk` 명령어로 Dusk 테스트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서의 Selenium

Apple Silicon 칩이 탑재된 컴퓨터라면, `selenium` 서비스 이미지를 `selenium/standalone-chromium`으로 변경해야 합니다.

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

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 개발 중 애플리케이션에서 발송되는 이메일을 가로채어, 웹 인터페이스를 통해 브라우저에서 편하게 미리볼 수 있도록 해줍니다. Sail을 사용할 때 Mailpit의 기본 호스트는 `mailpit`이며 1025 포트를 사용합니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, http://localhost:8025 에 접속하면 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

가끔 애플리케이션 컨테이너 내부에서 Bash 세션을 시작해야 할 필요가 있습니다. 이때는 `shell` 명령어로 컨테이너에 접속해 내부 파일과 설치된 서비스, 기타 임의의 쉘 명령어를 실행할 수 있습니다.

```shell
sail shell

sail root-shell
```

[Laravel Tinker](https://github.com/laravel/tinker) 세션을 새로 시작하려면 `tinker` 명령어를 사용합니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 PHP 8.4, 8.3, 8.2, 8.1, 8.0을 지원하며, 기본으로 PHP 8.4가 사용됩니다. 다른 PHP 버전으로 애플리케이션을 서비스하려면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 정의를 변경하세요.

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

또한, 실제 사용 중인 PHP 버전을 반영하도록 `image` 이름도 함께 변경할 수 있습니다. 이 역시 `compose.yaml` 파일에서 지정합니다.

```yaml
image: sail-8.2/app
```

`compose.yaml` 파일을 수정한 후에는 컨테이너 이미지를 반드시 재빌드 해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 시 설치되는 Node 버전을 변경하려면, `compose.yaml` 파일의 `laravel.test` 서비스 `build.args` 섹션에서 `NODE_VERSION` 값을 원하는 버전으로 지정합니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

환경설정을 변경한 후에는 반드시 컨테이너 이미지를 재빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나, 웹훅(Webhook) 통합 테스트를 위해 외부에 사이트를 잠시 공개해야 할 때가 있습니다. 이럴 때는 `share` 명령어를 사용하세요. 해당 명령어를 실행하면 임의의 `laravel-sail.site` URL이 발급되며, 이 주소로 애플리케이션을 외부에서 접속할 수 있습니다.

```shell
sail share
```

`share` 명령어를 이용해 사이트를 공유할 때는, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용해 반드시 신뢰할 수 있는 프록시(proxy)를 설정해야 합니다. 그렇지 않으면 `url` 또는 `route` 헬퍼를 사용할 때 올바른 HTTP 호스트를 인식하지 못할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유할 서브도메인을 직접 지정하려면 `share` 명령어에 `subdomain` 옵션을 추가하세요.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [Expose](https://github.com/beyondcode/expose)라는 [BeyondCode](https://beyondco.de)에서 개발한 오픈소스 터널링 서비스로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug를 이용한 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 구성은 [Xdebug](https://xdebug.org/)를 지원하므로, 강력하고 인기 있는 PHP 디버거를 사용할 수 있습니다. Xdebug를 활성화하려면, 우선 [Sail 구성을 퍼블리시](#sail-customization)했는지 확인한 뒤, `.env` 파일에 아래와 같이 환경 변수를 추가합니다.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고 퍼블리시한 `php.ini` 파일에 아래 내용을 추가해 지정한 모드로 Xdebug가 활성화되도록 합니다.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정한 후에는 반드시 Docker 이미지를 재빌드해야 설정이 적용됩니다.

```shell
sail build --no-cache
```

#### Linux 호스트 IP 구성

내부적으로, `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 설정되어 있으며, Mac이나 Windows(WSL2)에서는 추가 설정 없이 정상 동작합니다. 리눅스 환경에서 Docker 20.10 이상을 사용할 경우에도 `host.docker.internal`을 그대로 이용할 수 있으니 별도 설정이 필요 없습니다.

그러나 Docker 20.10 미만 버전에서는 `host.docker.internal`을 지원하지 않으므로 직접 호스트 IP를 지정해야 합니다. 이를 위해 `compose.yaml`에 사용자 지정 네트워크를 정의하고 컨테이너에 고정 IP를 할당합니다.

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

이후 애플리케이션의 `.env` 파일에 SAIL_XDEBUG_CONFIG 변수를 다음과 같이 지정하세요.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`debug` 명령어를 사용하면, Artisan 명령어를 실행할 때 Xdebug 세션을 시작할 수 있습니다.

```shell
# Xdebug 없이 Artisan 명령어 실행 예시...
sail artisan migrate

# Xdebug을 활성화한 상태로 Artisan 명령어 실행 예시...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저에서 애플리케이션과 상호작용하며 디버깅하려면, [Xdebug에서 제공하는 가이드](https://xdebug.org/docs/step_debug#web-application)를 따라 Xdebug 세션을 시작하면 됩니다.

PhpStorm을 사용하는 경우, JetBrains 공식 문서의 [제로-구성 디버깅(Zero-configuration debugging)](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 가이드를 참고하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션 서비스에 `artisan serve`를 사용합니다. `artisan serve` 명령어는 Laravel 8.53.0 이상에서만 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하 버전에서는 이 변수들이 제대로 인식되지 않아 디버그 연결이 불가합니다.

<a name="sail-customization"></a>
## 커스터마이즈 (Customization)

Sail은 Docker 기반이기 때문에 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 Dockerfile을 퍼블리시하려면, 아래와 같이 `sail:publish` 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

이 명령어를 실행하면 Dockerfile 및 구성 파일들이 애플리케이션의 루트에 있는 `docker` 디렉터리로 복사됩니다. Sail을 커스터마이즈한 후에는, 컨테이너 이미지 이름을 `compose.yaml` 파일에서 변경할 수 있습니다. 이후 반드시 컨테이너를 `build` 명령어로 재빌드해야 합니다. 여러 개의 Laravel 애플리케이션을 한 컴퓨터에서 동시에 개발하는 경우, 이미지에 고유한 이름을 부여하는 것이 특히 중요합니다.

```shell
sail build --no-cache
```
