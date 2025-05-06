# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 번째 단계](#first-steps)
    - [Homestead 구성](#configuring-homestead)
    - [Nginx 사이트 구성](#configuring-nginx-sites)
    - [서비스 구성](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [Alias 설정](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상 사용 방법](#daily-usage)
    - [SSH 연결](#connecting-via-ssh)
    - [사이트 추가](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [Mailpit 설정](#configuring-mailpit)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

Laravel은 여러분의 로컬 개발 환경을 포함해 전체 PHP 개발 경험이 즐거울 수 있도록 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는 사전 구성된 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버, 기타 서버 소프트웨어를 별도로 설치하지 않고도 쾌적한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신의 관리 및 프로비저닝을 간단하고 우아하게 처리할 수 있습니다. Vagrant 박스는 완전히 폐기할 수 있으며, 문제가 생기면 몇 분 만에 박스를 파괴하고 다시 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 모든 운영체제에서 동작하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, 기타 Laravel 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!WARNING]
> Windows를 사용하신다면 VT-x(하드웨어 가상화)를 활성화해야 할 수 있습니다. 이는 보통 BIOS에서 설정할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용 중인 경우, VT-x 접근을 위해 Hyper-V를 비활성화해야 할 수 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Ubuntu 22.04
- Git
- PHP 8.3
- PHP 8.2
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
- Node (Yarn, Bower, Grunt, Gulp 포함)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

</div>

<a name="optional-software"></a>
### 선택적 소프트웨어

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

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
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby 버전 관리)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk 유틸리티

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 첫 번째 단계

Homestead 환경을 실행하기 전에 반드시 [Vagrant](https://developer.hashicorp.com/vagrant/downloads) 및 아래에서 지원하는 프로바이더 중 하나를 설치해야 합니다.

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이들 소프트웨어는 모든 주요 운영체제용 쉬운 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 무료로 제공됩니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 저장소를 호스트 컴퓨터에 클론하여 설치할 수 있습니다. Homestead 가상 머신이 여러분의 모든 Laravel 애플리케이션의 호스트 역할을 하게 되므로, `Homestead` 폴더를 "홈" 디렉터리 안에 클론하는 것이 좋습니다. 이 디렉터리를 본 문서에서는 "Homestead 디렉터리"로 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead 저장소를 클론한 후에는 `release` 브랜치로 체크아웃해야 합니다. 이 브랜치에는 항상 최신 안정 버전이 포함되어 있습니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로, Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. `Homestead.yaml`은 Homestead 설치에 관한 모든 설정을 정의하는 곳입니다. 이 파일은 Homestead 디렉터리에 생성됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 구성

<a name="setting-your-provider"></a>
#### 프로바이더 설정

여러분의 `Homestead.yaml` 파일에 있는 `provider` 키로 어떤 Vagrant 프로바이더(`virtualbox` 또는 `parallels`)를 사용할지 지정하세요:

    provider: virtualbox

> [!WARNING]
> Apple Silicon을 사용하는 경우 Parallels 프로바이더가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더 목록을 나타냅니다. 이 폴더의 파일이 변경되면 로컬 컴퓨터와 Homestead 가상 환경 간에 동기화가 이루어집니다. 필요한 만큼 여러 폴더를 공유하도록 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 문법을 사용하지 말고, `C:\Users\user\Code\project1`처럼 전체 경로를 사용하세요.

각 애플리케이션별로 별도의 폴더 매핑을 제공하세요. 모든 애플리케이션이 포함된 하나의 큰 디렉토리를 매핑하는 대신, 각각 매핑하는 것이 좋습니다. 폴더를 매핑하면 가상 머신이 해당 폴더의 모든 파일에 대한 디스크 IO를 추적해야 하므로, 파일 수가 많을 경우 성능 저하가 있을 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 현재 디렉토리(`.`)를 마운트해서는 안 됩니다. 이 경우 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않아 추가 기능이 작동하지 않거나 이상 현상이 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 폴더 매핑에 `type` 옵션을 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것이 좋습니다. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉토리의 사용자/그룹 권한을 올바르게 유지합니다.

Vagrant의 [동기화 폴더](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)가 지원하는 모든 옵션도 `options` 키 아래에 나열해 전달할 수 있습니다:

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
### Nginx 사이트 구성

Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml`의 `sites` 속성으로 "도메인"을 Homestead 환경의 폴더에 쉽게 맵핑할 수 있습니다. 샘플 사이트 구성은 기본적으로 포함되어 있습니다. 필요에 따라 원하는 만큼 사이트를 추가할 수 있습니다. Homestead는 여러분이 작업 중인 각 Laravel 애플리케이션의 가상화된 환경 역할을 할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Homestead 가상 머신 프로비저닝 후 `sites` 속성을 변경한 경우, 터미널에서 `vagrant reload --provision` 명령을 실행해 가상 머신의 Nginx 구성을 최신 상태로 만드세요.

> [!WARNING]
> Homestead 스크립트는 최대한 불변성을 유지하도록 설계되었습니다. 하지만 프로비저닝 중 문제가 발생한다면 `vagrant destroy && vagrant up` 명령으로 머신을 파괴한 후 재생성하세요.

<a name="hostname-resolution"></a>
#### 호스트 이름(도메인) 해석

Homestead는 `mDNS`를 이용한 자동 호스트네임 해석을 제공합니다. `Homestead.yaml`에 `hostname: homestead`를 설정하면 `homestead.local`로 접근할 수 있습니다. macOS, iOS, Linux 데스크톱 배포판에는 기본적으로 `mDNS`가 포함되어 있습니다. Windows에서는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트네임은 [프로젝트별 설치](#per-project-installation)에서 가장 잘 동작합니다. 하나의 Homestead 인스턴스에 여러 사이트를 호스팅하는 경우, 사용자의 컴퓨터 `hosts` 파일에 웹사이트의 "도메인"을 추가하세요. 이 파일은 macOS와 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 위치합니다. 아래와 같이 추가하면 됩니다:

```text
192.168.56.56  homestead.test
```

IP 주소가 여러분의 `Homestead.yaml`에 설정된 값과 동일한지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면 브라우저에서 사이트를 확인할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 구성

Homestead는 기본적으로 여러 서비스를 시작하지만, 프로비저닝 중 활성화 또는 비활성화할 서비스를 사용자 정의할 수 있습니다. 예를 들어, `Homestead.yaml`의 `services` 옵션을 수정해 PostgreSQL 활성화와 MySQL 비활성화가 가능합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

나열된 순서에 따라 명시된 서비스는 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml` 파일을 원하는 대로 수정하였다면 Homestead 디렉토리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고, 자동으로 공유 폴더와 Nginx 사이트를 구성합니다.

머신을 파괴하려면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역에 설치해 모든 프로젝트에서 하나의 Homestead 가상 머신을 공유하는 대신, 각 프로젝트별로 Homestead 인스턴스를 구성할 수 있습니다. 프로젝트별 설치는 `Vagrantfile`을 프로젝트에 포함시켜 팀원이나 협업자가 리포지터리 클론 후 바로 `vagrant up` 할 수 있어 유리합니다.

Composer 패키지 관리자를 사용해 프로젝트에 Homestead를 설치하세요:

```shell
composer require laravel/homestead --dev
```

Homestead 설치 후, Homestead의 `make` 명령을 실행하면 `Vagrantfile`과 `Homestead.yaml` 파일이 프로젝트 루트에 생성됩니다. 이 명령은 `Homestead.yaml`의 `sites`와 `folders`를 자동으로 구성합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 다음 터미널에서 `vagrant up`을 실행하고, 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 [호스트네임 해석](#hostname-resolution)을 사용하지 않는 경우, `homestead.test`나 원하는 도메인을 `/etc/hosts` 파일에 추가해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불린 값으로 활성화/비활성화하며, 일부는 여러 설정 옵션을 가질 수 있습니다:

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
    - dragonflydb: true
    - elasticsearch:
        version: 7.9.0
    - eventstore: true
        version: 21.2.0
    - flyway: true
    - gearman: true
    - golang: true
    - grafana: true
    - influxdb: true
    - logstash: true
    - mariadb: true
    - meilisearch: true
    - minio: true
    - mongodb: true
    - neo4j: true
    - ohmyzsh: true
    - openresty: true
    - pm2: true
    - python: true
    - r-base: true
    - rabbitmq: true
    - rustc: true
    - rvm: true
    - solr: true
    - timescaledb: true
    - trader: true
    - webdriver: true
```

<a name="elasticsearch"></a>
#### Elasticsearch

지원되는 Elasticsearch 버전을 직접 지정할 수 있으며, 반드시 `주.부.패치`의 정확한 버전 번호여야 합니다. 기본 설치는 'homestead'라는 이름의 클러스터를 만듭니다. Elasticsearch에는 운영체제 메모리의 절반을 초과하여 할당하지 말아야 하므로, Homestead 가상 머신의 메모리가 최소 배 이상인지 확인하세요.

> [!NOTE]
> [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)에서 추가 설정 방법을 확인하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL의 드롭인 대체재이므로, 애플리케이션의 데이터베이스 설정에서 여전히 `mysql` 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치 시 데이터베이스 사용자 이름은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치 시 데이터베이스 사용자 이름은 `homestead`, 비밀번호 역시 `secret`으로 설정됩니다. Neo4j 브라우저는 브라우저에서 `http://homestead.test:7474`로 접속할 수 있습니다. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)이 모두 Neo4j 클라이언트 요청을 처리합니다.

<a name="aliases"></a>
### Alias 설정

Homestead 가상 머신에 Bash alias를 추가하려면 Homestead 디렉터리의 `aliases` 파일을 수정하세요:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일을 업데이트한 후에는 `vagrant reload --provision` 명령으로 Homestead를 다시 프로비저닝하세요. 새 alias가 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전에 Homestead 디렉터리에서 아래 명령어로 현재 가상 머신을 제거하세요:

```shell
vagrant destroy
```

그 다음 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면, 원래 클론한 위치에서 다음 명령을 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령은 GitHub의 최신 Homestead 코드, 태그를 받아오고, 최신 태그 릴리스를 체크아웃합니다. 최신 안정 릴리스를 Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인하세요.

프로젝트의 `composer.json` 파일을 통해 Homestead를 설치했다면, 반드시 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고, 의존성을 업데이트하세요:

```shell
composer update
```

다음으로, `vagrant box update` 명령으로 Vagrant 박스를 업데이트하세요:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후, Homestead 디렉터리에서 `bash init.sh` 명령을 실행해 추가 설정 파일을 업데이트하세요. `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 물어봅니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 최신 Vagrant 설치를 사용하려면 Homestead 가상 머신을 재생성해야 합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상 사용 방법

<a name="connecting-via-ssh"></a>
### SSH 연결

Homestead 디렉터리에서 `vagrant ssh` 명령을 실행하여 가상 머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 사이트 추가

Homestead 환경이 프로비저닝되어 실행 중이라면, 다른 Laravel 프로젝트를 위한 Nginx 사이트도 추가할 수 있습니다. 한 대의 Homestead 환경에 원하는 만큼 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트는 `Homestead.yaml`에 다음과 같이 추가하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트를 추가하기 전에 해당 프로젝트 디렉토리에 [폴더 매핑](#configuring-shared-folders)이 구성되어 있는지 확인하세요.

Vagrant가 `hosts` 파일을 자동 관리하지 않는다면, 해당 파일에도 새로운 사이트를 추가해야 합니다. macOS와 Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`입니다:

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 후, Homestead 디렉터리에서 `vagrant reload --provision`을 실행하세요.

<a name="site-types"></a>
#### 사이트 타입

Homestead는 Laravel 기반 프로젝트 외에 다른 프로젝트도 쉽게 실행할 수 있는 여러 "사이트 타입"을 지원합니다. 예를 들어, `statamic` 사이트 타입을 이용해 Statamic 애플리케이션을 손쉽게 Homestead에 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 타입: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
#### 사이트 파라미터

사이트에 Nginx `fastcgi_param` 값을 추가하려면 `params` 사이트 지시자를 사용하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수

글로벌 환경 변수는 `Homestead.yaml` 파일에 다음과 같이 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml`을 수정한 후에는 머신을 `vagrant reload --provision` 명령으로 다시 프로비저닝해야 합니다. 이것은 모든 설치된 PHP 버전의 PHP-FPM 설정도 함께 업데이트합니다.

<a name="ports"></a>
### 포트

기본적으로 아래 포트가 Homestead 환경으로 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80
- **HTTPS:** 44300 → 443

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

원한다면 추가로 포트를 Vagrant 박스로 포워딩할 수 있습니다. `Homestead.yaml`에 `ports` 설정을 추가하세요. 변경 후에는 `vagrant reload --provision`을 꼭 실행하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

아래는 추가적으로 매핑할 수 있는 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22
- **ngrok UI:** 4040 → 4040
- **MySQL:** 33060 → 3306
- **PostgreSQL:** 54320 → 5432
- **MongoDB:** 27017 → 27017
- **Mailpit:** 8025 → 8025
- **Minio:** 9600 → 9600

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 하나의 가상 머신에서 여러 PHP 버전을 지원합니다. `Homestead.yaml` 파일에서 각 사이트별로 사용할 PHP 버전을 지정할 수 있습니다. 사용 가능한 PHP 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내](#connecting-via-ssh)에서는 CLI에서 다음과 같이 지원되는 모든 PHP 버전을 사용할 수 있습니다:

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
php8.3 artisan list
```

CLI에서 기본 PHP 버전을 변경하려면 Homestead 가상 머신 내에서 아래 명령을 실행하세요:

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
php83
```

<a name="connecting-to-databases"></a>
### 데이터베이스 연결

기본적으로 MySQL과 PostgreSQL 모두에 `homestead` 데이터베이스가 생성되어 있습니다. 호스트 컴퓨터의 데이터베이스 클라이언트에서 `127.0.0.1`의 포트 `33060`(MySQL) 또는 `54320`(PostgreSQL)으로 접속하세요. 두 데이터베이스의 사용자명과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트 머신에서 데이터베이스에 접속할 때만 이 비표준 포트를 사용하세요. Laravel 애플리케이션이 가상 머신 내에서 실행되는 경우 기본 포트(3306, 5432)를 사용합니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 Homestead 가상 머신이 파괴될 때 데이터베이스를 자동으로 백업할 수 있습니다. 이를 이용하려면 Vagrant 2.1.0 이상이 필요합니다. 구 버전 Vagrant는 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 켜려면 `Homestead.yaml`에 아래와 같이 추가하세요:

```yaml
backup: true
```

설정 후 `vagrant destroy` 명령을 실행하면 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉토리에 데이터베이스가 내보내집니다. 해당 디렉토리는 Homestead 설치 폴더나 [프로젝트별 설치](#per-project-installation) 방식이라면 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 [스케줄러](/docs/{{version}}/scheduling)를 이용해 `schedule:run` 아티즌 명령을 1분마다 실행하는 방식으로 크론 작업을 처리합니다. `routes/console.php`에 정의된 스케줄을 검사해 어떤 작업을 실행할지 결정합니다.

특정 Homestead 사이트에 `schedule:run` 명령을 적용하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 등록됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)은 실제로 메일을 발송하지 않고도 발신 메일을 가로채 확인할 수 있습니다. 사용하려면 애플리케이션의 `.env` 파일을 아래와 같이 설정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

설정 후 `http://localhost:8025`에서 Mailpit 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 가진 오픈 소스 오브젝트 스토리지 서버입니다. Minio를 설치하려면 [features](#installing-optional-features) 섹션에 아래 옵션을 추가하세요:

    minio: true

기본적으로 9600 포트에서 사용 가능합니다. `http://localhost:9600`에서 Minio 제어판에 접근할 수 있습니다. 기본 엑세스 키는 `homestead`, 시크릿 키는 `secretkey`입니다. 반드시 `us-east-1` 리전을 사용하세요.

`.env` 파일에도 다음 설정이 필요합니다:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시자를 추가하세요. 정의 후 `vagrant reload --provision` 실행을 잊지 마세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원되는 `policy` 값: `none`, `download`, `upload`, `public`.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 내에서 [Laravel Dusk](/docs/{{version}}/dusk) 테스트를 실행하려면 Homestead 설정에서 [webdriver 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

`webdriver`를 활성화했다면, 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유

동료나 고객과 현재 작업 내용을 공유하고 싶을 때가 있습니다. Vagrant에는 `vagrant share` 명령을 통한 내장 환경 공유 기능이 있지만, `Homestead.yaml`에 여러 사이트를 설정한 경우에는 사용할 수 없습니다.

이 문제를 해결하기 위해 Homestead에는 자체 `share` 명령이 포함되어 있습니다. 먼저 [`vagrant ssh`](#connecting-via-ssh)로 Homestead 가상 머신에 접속한 후, 아래 명령을 실행하세요. 이 명령은 `Homestead.yaml`에 설정된 사이트 중 하나를 공유합니다:

```shell
share homestead.test
```

명령을 실행하면 Ngrok 화면에 공유 사이트의 공개 URL과 활동 로그가 표시됩니다. 원하는 리전, 서브도메인 등 Ngrok 실행 옵션을 추가로 지정하고 싶다면 이렇게 사용할 수 있습니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTP 대신 HTTPS로 공유하려면 `share` 대신 `sshare` 명령을 사용하세요.

> [!WARNING]
> Vagrant는 본질적으로 보안이 취약하므로 `share` 명령을 실행하면 가상 머신이 인터넷에 노출됨을 반드시 인지하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 이용한 스텝 디버깅을 지원합니다. 예를 들어, 브라우저에서 페이지에 접근하면 PHP가 IDE와 연결되어 실행 중인 코드를 점검 및 수정할 수 있습니다.

기본적으로 Xdebug는 구동 중이며 언제든 연결을 받을 준비가 되어 있습니다. CLI에서도 Xdebug를 활성화해야 한다면 Homestead 가상 머신 내에서 `sudo phpenmod xdebug`를 실행하세요. 이후 IDE 안내에 따라 디버깅을 활성화하고, 브라우저 확장 또는 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)으로 Xdebug를 트리거하세요.

> [!WARNING]
> Xdebug 활성화 시 PHP 실행이 매우 느려질 수 있습니다. 비활성화하려면 Homestead 가상 머신 내에서 `sudo phpdismod xdebug`를 실행한 후 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동시작

웹 서버에 요청하는 기능 테스트를 디버깅할 때, 맞춤 헤더나 쿠키로 트리거하지 않고 자동으로 Xdebug를 시작하는 것이 더 쉽습니다. Xdebug를 자동으로 시작하려면 Homestead 가상 머신 내의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일에서 아래 설정을 추가하세요:

```ini
; Homestead.yaml에 다른 서브넷이 지정된 경우 IP 주소가 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 셸 alias를 사용하세요:

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션 프로파일링 서비스입니다. 결과를 호출 그래프와 타임라인으로 제공하는 대화형 UI를 지원하며, 개발/스테이징/운영 환경 모두에서 사용 가능(실제 사용자에겐 오버헤드 없음)합니다. 또한 코드 및 `php.ini` 설정에 대한 성능, 품질, 보안 점검도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈 소스 웹 크롤링/테스트/스크래핑 툴로, Blackfire와 함께 작동해 프로파일링 시나리오를 스크립트할 수 있습니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 설정을 사용하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격증명은 [Blackfire 계정](https://blackfire.io/signup) 등록이 필요합니다. 명령행 도구 및 브라우저 확장 등 다양한 프로파일링 방법을 제공합니다. 더 자세한 내용은 [Blackfire 공식 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml`의 `networks` 속성으로 Homestead 가상 머신의 네트워크 인터페이스를 조정할 수 있습니다. 필요한 만큼 여러 인터페이스를 구성하세요:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브릿지 모드](https://developer.hashicorp.com/vagrant/docs/networking/public_network)를 사용하려면 `type`을 `public_network`로 변경하고, `bridge` 설정을 추가하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 `ip` 옵션을 지우세요:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크가 사용할 디바이스를 변경하려면 `dev` 옵션을 추가하세요. 기본값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead 루트 디렉터리의 `after.sh` 스크립트를 사용해 Homestead를 확장할 수 있습니다. 이 파일에서 가상 머신을 추가로 구성하는 데 필요한 셸 명령을 추가하세요.

Homestead를 커스터마이즈하려다 보면 Ubuntu에서 패키지의 기존 설정을 유지할지 아니면 새 파일로 덮어쓸지 물어보는 경우가 있습니다. 이런 프롬프트를 피하려면 패키지 설치 시 아래 명령을 사용하세요:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징

팀원과 Homestead를 함께 사용할 때, 자신만의 개발 스타일에 맞게 Homestead를 조정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리(즉, `Homestead.yaml`이 있는 곳)에 `user-customizations.sh` 파일을 생성하고 원하는 커스터마이징을 넣으세요. 단, 이 파일은 버전 관리에 포함시키지 마세요.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이 덕분에 Homestead가 호스트 운영체제의 DNS 설정을 사용할 수 있습니다. 이를 변경하려면 `Homestead.yaml`에 아래와 같이 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```
