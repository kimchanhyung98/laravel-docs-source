# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫걸음](#first-steps)
    - [Homestead 구성하기](#configuring-homestead)
    - [Nginx 사이트 구성하기](#configuring-nginx-sites)
    - [서비스 구성하기](#configuring-services)
    - [Vagrant 박스 실행하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상 사용법](#daily-usage)
    - [SSH 연결 방법](#connecting-via-ssh)
    - [추가 사이트 등록](#adding-additional-sites)
    - [환경 변수 설정](#environment-variables)
    - [포트 설정](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 생성](#creating-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [MailHog 설정](#configuring-mailhog)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

Laravel은 PHP 개발 경험 전반을 즐겁게 만들기 위해 노력하며, 여기에 로컬 개발 환경도 포함됩니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식으로 제공되는 미리 구성된 Vagrant 박스로, 로컬 머신에 PHP, 웹 서버, 기타 서버 소프트웨어를 직접 설치할 필요 없이 우수한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 설정하는 간단하고 우아한 방법을 제공합니다. Vagrant 박스는 완전히 폐기 가능하므로, 문제가 생기면 박스를 파괴하고 몇 분 만에 새로 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 시스템에서 모두 실행되며, Laravel 애플리케이션 개발에 필요한 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등을 포함하고 있습니다.

> [!WARNING]
> Windows를 사용하는 경우 하드웨어 가상화(VT-x)를 활성화해야 할 수도 있습니다. 일반적으로 BIOS에서 활성화할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우, VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어


<div id="software-list" markdown="1">

- Ubuntu 20.04
- Git
- PHP 8.2 (기본)
- PHP 8.1
- PHP 8.0
- PHP 7.4
- PHP 7.3
- PHP 7.2
- PHP 7.1
- PHP 7.0
- PHP 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 15
- Composer
- Docker
- Node 18 (Yarn, Bower, Grunt, Gulp 포함)
- Redis
- Memcached
- Beanstalkd
- Mailhog
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

</div>

<a name="optional-software"></a>
### 선택적 소프트웨어


<div id="software-list" markdown="1">

- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- Heroku CLI
- InfluxDB
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python 3
- R
- RabbitMQ
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk 유틸리티

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 첫걸음

Homestead 환경을 시작하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 다음 지원하는 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어들은 모두 주요 운영체제에서 쉽게 설치할 수 있는 GUI 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치하기

Homestead를 설치하려면 호스트 머신에 Homestead 저장소를 클론하세요. Homestead 가상 머신이 모든 Laravel 애플리케이션을 호스팅하기 때문에 홈 디렉토리 내 `Homestead` 폴더에 클론하는 것을 추천합니다. 이 문서에서는 이 디렉토리를 "Homestead 디렉토리"라 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

클론 후에는 항상 최신 안정 버전이 포함된 `release` 브랜치를 체크아웃해야 합니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. 이 파일에 Homestead 설치를 위한 설정을 모두 구성합니다. `Homestead.yaml` 파일은 Homestead 디렉토리에 생성됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 구성하기

<a name="setting-your-provider"></a>
#### 프로바이더 설정하기

`Homestead.yaml` 파일에서 `provider` 키는 어떤 Vagrant 프로바이더를 사용할지 지정합니다: `virtualbox` 또는 `parallels`입니다:

```
provider: virtualbox
```

> [!WARNING]
> Apple Silicon을 사용하는 경우, `Homestead.yaml`에 `box: laravel/homestead-arm`을 추가해야 합니다. Apple Silicon은 Parallels 프로바이더가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 구성하기

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더들을 나열합니다. 이 폴더 내 파일이 변경되면 로컬 머신과 Homestead 가상 환경 간에 동기화됩니다. 원하는 만큼 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 구문 대신 프로젝트에 대한 전체 경로(ex: `C:\Users\user\Code\project1`)를 사용해야 합니다.

개별 애플리케이션마다 각기 다른 폴더 매핑을 하는 것이 좋습니다. 하나의 큰 폴더에 여러 프로젝트를 모두 매핑하면, 가상 머신이 폴더 내 모든 파일의 디스크 I/O를 추적해야 하므로 성능 저하가 발생할 수 있기 때문입니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 현재 디렉토리(`.`)를 마운트해서는 안 됩니다. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않아 선택적 기능이 깨지거나 프로비저닝 중에 예상치 못한 결과가 발생할 수 있습니다.

[NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html)를 사용하려면 폴더 매핑에 `type` 옵션을 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것이 권장됩니다. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉토리에 대해 올바른 사용자/그룹 권한을 유지합니다.

Vagrant의 [동기화 폴더(Synced Folders)](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)에서 지원하는 옵션들은 `options` 키 아래에 나열해 전달할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "rsync"
      options:
          rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
          rsync__exclude: ["node_modules"]
```

<a name="configuring-nginx-sites"></a>
### Nginx 사이트 구성하기

Nginx를 잘 모르는 경우에도 걱정하지 마세요. `Homestead.yaml` 파일의 `sites` 속성을 통해 Homestead 환경 내 특정 폴더에 "도메인"을 쉽게 매핑할 수 있습니다. `Homestead.yaml` 파일에는 예제 사이트 구성이 포함되어 있습니다. 필요한 수만큼 사이트를 추가할 수 있으며, Homestead를 여러 Laravel 애플리케이션을 위한 편리한 가상화 환경으로 활용할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

사이트 속성을 변경한 후에는 가상 머신의 Nginx 구성을 업데이트하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!WARNING]
> Homestead 스크립트는 최대한 멱등성(idempotent)을 보장하도록 작성되었습니다. 하지만 프로비저닝 중 문제가 발생하면 `vagrant destroy && vagrant up` 명령을 통해 머신을 완전히 재생성하는 것을 권장합니다.

<a name="hostname-resolution"></a>
#### 호스트네임 이름 해석

Homestead는 호스트 이름 자동 해석을 위해 `mDNS`를 사용합니다. `Homestead.yaml` 파일에 `hostname: homestead`를 설정하면, 호스트는 `homestead.local` 주소로 접근할 수 있습니다. macOS, iOS, Linux 데스크톱 배포판은 기본적으로 `mDNS`를 지원합니다. Windows를 사용하는 경우, [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트 이름 기능은 [프로젝트별 설치](#per-project-installation)에 가장 적합합니다. 하나의 Homestead 인스턴스에서 여러 사이트를 호스팅하는 경우, 각 사이트 도메인을 로컬 머신의 `hosts` 파일에 추가할 수 있습니다. 이 파일은 macOS 및 Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts` 위치에 있습니다. 다음과 같이 IP 주소와 도메인을 매핑하세요:

```
192.168.56.56  homestead.test
```

`Homestead.yaml` 파일에 지정된 IP 주소와 일치하도록 주의하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면 브라우저를 통해 사이트에 접속할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 구성하기

Homestead는 기본적으로 여러 서비스를 시작하지만 프로비저닝 중 어떤 서비스를 활성화하거나 비활성화할지 사용자 정의할 수 있습니다. 예를 들어 PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml`의 `services` 항목을 수정하세요:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

지정한 서비스들은 `enabled`와 `disabled` 목록에 따라 시작되거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행하기

`Homestead.yaml` 파일 수정을 마쳤으면 Homestead 디렉토리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트 구성을 자동으로 완료합니다.

가상 머신을 파괴하고 싶으면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역으로 설치해 모든 프로젝트가 같은 가상 머신을 공유하는 대신, 각 프로젝트마다 Homestead 인스턴스를 구성할 수도 있습니다. 이 방법은 프로젝트 저장소와 함께 `Vagrantfile`을 포함시켜, 다른 개발자들이 저장소를 클론한 직후 바로 `vagrant up`으로 개발 환경을 실행할 수 있어 유용합니다.

프로젝트에 Composer 패키지로 Homestead를 설치하려면 다음을 실행하세요:

```shell
composer require laravel/homestead --dev
```

설치 후, Homestead의 `make` 명령으로 `Vagrantfile`과 `Homestead.yaml`을 생성합니다. 두 파일은 프로젝트 루트에 생성되며, `make`가 `sites`와 `folders` 지시어를 자동으로 설정합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

마지막으로 터미널에서 `vagrant up`을 실행한 뒤 브라우저에서 `http://homestead.test`로 접속하세요. 자동 [호스트네임 해석](#hostname-resolution)을 사용하지 않는다면, `/etc/hosts`에 `homestead.test` 혹은 원하는 도메인을 등록해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml`의 `features` 설정을 통해 설치할 수 있습니다. 대부분의 기능은 불리언 값으로 켜고 끌 수 있고, 일부는 추가 설정 값을 허용합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
    - cassandra: true
    - chronograf: true
    - couchdb: true
    - crystal: true
    - elasticsearch:
        version: 7.9.0
    - eventstore: true
        version: 21.2.0
    - flyway: true
    - gearman: true
    - golang: true
    - grafana: true
    - heroku: true
    - influxdb: true
    - mariadb: true
    - meilisearch: true
    - minio: true
    - mongodb: true
    - mysql: true
    - neo4j: true
    - ohmyzsh: true
    - openresty: true
    - pm2: true
    - python: true
    - r-base: true
    - rabbitmq: true
    - rvm: true
    - solr: true
    - timescaledb: true
    - trader: true
    - webdriver: true
```

<a name="elasticsearch"></a>
#### Elasticsearch

Elasticsearch 지원 버전을 정확한 버전 번호(주버전.부버전.패치)로 지정할 수 있습니다. 기본 설치시 'homestead'라는 클러스터가 생성됩니다. OS 메모리의 절반 이상은 Elasticsearch에 할당하지 않아야 하므로, Homestead 가상 머신 메모리는 Elasticsearch 할당량의 2배 이상이어야 합니다.

> [!NOTE]
> [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고해 구성 방법을 확인하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL은 제거되고 대신 MariaDB가 설치됩니다. MariaDB는 MySQL의 드롭인 교체품이므로, 애플리케이션의 DB 설정에서는 여전히 `mysql` 드라이버를 사용해야 합니다:

```yaml
features:
  - mariadb: true
```

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치 시, 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치 시, 데이터베이스 사용자명은 `homestead`이고 비밀번호는 `secret`입니다. Neo4j 브라우저에 접속하려면 `http://homestead.test:7474` 주소를 브라우저에서 열면 됩니다. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)가 클라이언트 요청을 처리합니다.

<a name="aliases"></a>
### 별칭(Aliases)

별칭을 추가하려면 Homestead 디렉토리 내 `aliases` 파일을 수정하면 됩니다:

```shell
alias c='clear'
alias ..='cd ..'
```

파일 수정 후, `vagrant reload --provision` 명령으로 가상 머신을 재프로비저닝하여 별칭을 활성화하세요.

<a name="updating-homestead"></a>
## Homestead 업데이트

먼저 현재 가상 머신을 제거하기 위해 Homestead 디렉토리에서 다음 명령을 실행하세요:

```shell
vagrant destroy
```

다음으로 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면 클론한 위치에서 다음을 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령은 GitHub 저장소에서 최신 Homestead 코드를 받아오고 최신 태그를 적용합니다. 최신 안정 버전은 Homestead의 [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`을 통한 설치 시에는 `"laravel/homestead": "^12"`가 포함되어 있는지 확인 후 의존성을 업데이트하세요:

```shell
composer update
```

Vagrant 박스도 다음 명령으로 업데이트하세요:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후에는 `bash init.sh` 명령을 통해 Homestead의 추가 설정 파일들도 업데이트해야 합니다. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일 덮어쓰기 여부를 묻습니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 최신 버전 Vagrant 환경을 적용하려면 가상 머신을 재생성하세요:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상 사용법

<a name="connecting-via-ssh"></a>
### SSH 연결 방법

Homestead 디렉토리에서 `vagrant ssh` 명령을 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 등록

프로비저닝 된 Homestead 환경이 동작 중일 때, 다른 Laravel 프로젝트를 위한 추가 Nginx 사이트를 등록할 수 있습니다. 한 개의 Homestead에서 원하는 만큼 Laravel 프로젝트를 실행할 수 있습니다. 사이트 추가를 위해 `Homestead.yaml` 파일에 사이트를 추가하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트 추가 전에 프로젝트 디렉토리에 대한 [폴더 매핑](#configuring-shared-folders)이 설정되어 있어야 합니다.

Vagrant가 자동으로 `hosts` 파일을 관리하지 않는 경우, 새 사이트를 여기에도 추가해야 합니다. macOS 및 Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts` 파일입니다:

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트 추가 후, Homestead 디렉토리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 Laravel 이외의 프로젝트도 쉽게 실행할 수 있도록 여러 사이트 유형을 지원합니다. 예를 들어 Statamic 애플리케이션을 추가할 때 `statamic` 사이트 유형을 사용할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 유형은 `apache`, `apigility`, `expressive`, 기본값인 `laravel`, `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 등이 있습니다.

<a name="site-parameters"></a>
#### 사이트 파라미터

Nginx `fastcgi_param` 값을 `params` 설정을 통해 사이트별로 추가할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수 설정

전역 환경 변수는 `Homestead.yaml` 파일의 `variables`에 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

수정 후에는 반드시 `vagrant reload --provision` 명령을 실행하여 PHP-FPM 설정과 `vagrant` 사용자 환경을 업데이트하세요.

<a name="ports"></a>
### 포트

기본적으로 다음 포트들이 Homestead 환경으로 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80
- **HTTPS:** 44300 → 443

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

추가 포트를 포워딩하려면 `Homestead.yaml`에 `ports` 설정을 추가하세요. 수정을 마친 뒤에는 `vagrant reload --provision`으로 프로비저닝을 다시 해야 합니다:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

호스트 머신과 Vagrant 박스 간 포워딩할 때 보통 사용하는 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22
- **ngrok UI:** 4040 → 4040
- **MySQL:** 33060 → 3306
- **PostgreSQL:** 54320 → 5432
- **MongoDB:** 27017 → 27017
- **Mailhog:** 8025 → 8025
- **Minio:** 9600 → 9600

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 한 가상 머신에서 여러 PHP 버전을 동시에 실행할 수 있습니다. 사이트별로 사용할 PHP 버전을 `Homestead.yaml`에 지정할 수 있으며, 지원되는 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2"(기본값)입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.4"
```

Homestead 가상 머신 내부에서 CLI로 다음과 같이 PHP 버전을 지정하여 사용할 수 있습니다:

```shell
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
php8.2 artisan list
```

또한 `Homestead.yaml` 에서 CLI 기본 PHP 버전을 다음과 같이 지정 가능하며,

```yaml
php: 8.0
```

가상 머신 내부에서 직접 다음 명령어를 실행해 변경할 수도 있습니다:

```shell
php56
php70
php71
php72
php73
php74
php80
php81
php82
```

<a name="connecting-to-databases"></a>
### 데이터베이스 연결

기본적으로 `homestead` 데이터베이스가 MySQL과 PostgreSQL 모두에 구성되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 MySQL 및 PostgreSQL에 연결하려면 각각 `127.0.0.1`의 포트 `33060`(MySQL) 또는 `54320`(PostgreSQL)으로 접속하세요. 두 데이터베이스 모두 사용자명과 비밀번호는 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트 머신에서 접속할 때만 비표준 포트를 사용해야 하며, Laravel 애플리케이션 안에서는 가상 머신 내에서 실행되므로 기본 3306(MySQL), 5432(PostgreSQL) 포트를 사용하세요.

<a name="creating-databases"></a>
### 데이터베이스 생성

Homestead는 애플리케이션에서 필요로 하는 데이터베이스를 자동으로 생성할 수 있습니다. 프로비저닝 중 데이터베이스 서비스가 동작 중이면 `Homestead.yaml`에 정의된 데이터베이스가 이미 존재하지 않을 경우 생성됩니다:

```yaml
databases:
  - database_1
  - database_2
```

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead 가상 머신이 파괴될 때 자동으로 데이터베이스를 백업할 수 있습니다. 이를 사용하려면 Vagrant 2.1.0 이상 버전이어야 하며, 구버전 사용 시 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 다음을 추가하세요:

```
backup: true
```

이 설정 시 `vagrant destroy` 명령을 실행할 때 데이터베이스가 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉토리로 내보내집니다. 이 경로는 Homestead 설치 폴더이거나, 프로젝트별 설치 시에는 프로젝트 루트입니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 단일 `schedule:run` Artisan 명령을 매분 실행하여 [크론 잡](/docs/9.x/scheduling)을 편리하게 예약할 수 있게 합니다. `schedule:run` 명령은 `App\Console\Kernel` 클래스에 정의된 작업 스케줄을 검사하여 실행할 작업을 판단합니다.

Homestead 사이트에 대해 `schedule:run` 명령 실행을 활성화하려면 `Homestead.yaml`의 사이트 정의에 `schedule: true`를 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉토리에 정의됩니다.

<a name="configuring-mailhog"></a>
### MailHog 설정

[MailHog](https://github.com/mailhog/MailHog)는 메일을 실제 수신자에게 보내지 않고도 발송 내용을 가로채어 검사할 수 있게 해줍니다. 사용하려면 애플리케이션 `.env` 파일에 아래 메일 설정을 적용하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

설정 후에는 `http://localhost:8025`에서 MailHog 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 `Homestead.yaml` 내 [features](#installing-optional-features) 섹션에 다음을 추가하세요:

```
minio: true
```

기본적으로 Minio는 9600 포트에서 구동되며, `http://localhost:9600`에서 제어판에 접속 가능합니다. 기본 액세스 키는 `homestead`, 시크릿 키는 `secretkey`이고, 항상 `us-east-1` 리전을 사용해야 합니다.

Minio를 이용하려면 애플리케이션의 `config/filesystems.php`의 S3 디스크 설정을 조정해야 하며, `use_path_style_endpoint` 옵션을 추가하고 `url` 키를 `endpoint`로 변경해야 합니다:

```
's3' => [
    'driver' => 's3',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION'),
    'bucket' => env('AWS_BUCKET'),
    'endpoint' => env('AWS_URL'),
    'use_path_style_endpoint' => true,
]
```

마지막으로 `.env` 파일에 다음 항목을 포함하세요:

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시어를 추가하고, 버킷 정의 후 `vagrant reload --provision` 명령을 실행하세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원하는 `policy` 값은 `none`, `download`, `upload`, `public`입니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead에서 [Laravel Dusk](/docs/9.x/dusk) 테스트를 실행하려면 Homestead 설정에서 [`webdriver` 기능](#installing-optional-features)을 활성화하세요:

```yaml
features:
    - webdriver: true
```

활성화 후 `vagrant reload --provision` 명령을 실행해야 합니다.

<a name="sharing-your-environment"></a>
### 환경 공유하기

작업 중인 환경을 동료나 고객과 공유하고 싶을 때가 있습니다. Vagrant는 `vagrant share` 명령으로 이를 지원하지만, `Homestead.yaml`에 여러 사이트가 설정된 경우 작동하지 않습니다.

이 문제 해결을 위해 Homestead는 자체 `share` 명령을 제공합니다. [SSH로 Homestead 가상 머신](#connecting-via-ssh)에 접속한 다음 `share homestead.test` 명령을 실행하면 `Homestead.yaml`에 정의된 `homestead.test` 사이트가 공유됩니다. 원하는 다른 사이트도 명령어에 넣을 수 있습니다:

```shell
share homestead.test
```

명령어 실행 시 ngrok 화면이 나타나 활동 로그 및 공개 URL을 표시합니다. 지역(region), 서브도메인(subdomain) 등 ngrok 실행 옵션을 지정하고 싶으면 명령어에 추가하세요:

```shell
share homestead.test -region=eu -subdomain=laravel
```

> [!WARNING]
> Vagrant는 본질적으로 보안이 취약하므로 `share` 명령 사용 시 가상 머신이 인터넷에 노출됩니다.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 통한 단계별 디버깅을 지원합니다. 브라우저에서 페이지에 접근하면 PHP가 IDE에 연결되어 실행 중 코드를 검사 및 수정할 수 있습니다.

기본적으로 Xdebug는 이미 실행 중이며 연결을 대기합니다. CLI에서 Xdebug를 켜거나 끄려면 Homestead 가상 머신 내에서 `sudo phpenmod xdebug` 또는 `sudo phpdismod xdebug` 명령을 실행하세요.

다음으로 IDE 지침에 따라 디버깅을 활성화하고 브라우저에서는 확장 프로그램이나 [북마클릿(bookmarklet)](https://www.jetbrains.com/phpstorm/marklets/)으로 Xdebug 트리거 설정을 하세요.

> [!WARNING]
> Xdebug는 PHP 실행 속도를 크게 느리게 만듭니다. 비활성화하려면 Homestead 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

기능 테스트 등 웹 서버에 요청하는 테스트를 디버그할 때, 커스텀 헤더나 쿠키를 추가하는 대신 Xdebug를 자동으로 시작하는 것이 편리합니다. Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하여 다음 내용을 추가하세요:

```ini
; Homestead.yaml에 지정된 서브넷에 따라 IP가 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 쉘 별칭을 사용하세요:

```
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션을 프로파일링하는 서비스입니다. 호출 그래프와 타임라인을 인터랙티브 UI로 보여주며, 개발, 스테이징, 프로덕션 환경 모두에서 사용할 수 있고 최종 사용자에는 오버헤드가 없습니다. 또한 코드 및 `php.ini` 설정에 대해 성능, 품질, 보안 검사를 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 웹 크롤링, 웹 테스트, 웹 스크래핑 애플리케이션으로 Blackfire와 함께 사용하여 프로파일링 시나리오를 스크립팅할 수 있습니다.

Blackfire 활성화는 Homestead 설정 파일의 `features` 항목에서 다음과 같이 합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

서버 및 클라이언트 자격 증명에는 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구와 브라우저 확장 등 다양한 프로파일링 옵션을 제공합니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 여러 인터페이스를 구성할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지 연결](https://www.vagrantup.com/docs/networking/public_network.html)을 활성화하려면 `bridge` 설정을 추가하고 네트워크 타입을 `public_network`로 변경하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://www.vagrantup.com/docs/networking/public_network.html)를 활성화하려면 `ip` 옵션을 삭제하세요:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<a name="extending-homestead"></a>
## Homestead 확장하기

Homestead 디렉토리 루트의 `after.sh` 스크립트를 수정하여 Homestead를 확장할 수 있습니다. 이 파일에 가상 머신을 적절히 구성하고 맞춤화하기 위한 셸 명령을 추가하면 됩니다.

Ubuntu에서 패키지 설치 시 기존 설정 파일을 덮어쓰지 않고 유지하려면 다음 명령어를 사용하는 것이 좋습니다:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 맞춤 설정

팀과 함께 Homestead를 사용할 때 각자 개발 스타일에 맞게 조정하고 싶다면, Homestead 루트 디렉토리(즉 `Homestead.yaml` 파일과 같은 위치)에 `user-customizations.sh` 파일을 생성하세요. 이 파일에 원하는 설정을 자유롭게 추가할 수 있지만, 버전 관리에서는 제외해야 합니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 두어 호스트 OS의 DNS 설정을 사용합니다. 이 동작을 변경하려면 `Homestead.yaml`에 다음 옵션을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

<a name="symbolic-links-on-windows"></a>
#### Windows에서 심볼릭 링크 문제

Windows에서 심볼릭 링크가 제대로 작동하지 않으면 `Vagrantfile`에 아래 블록을 추가해야 할 수 있습니다:

```ruby
config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```