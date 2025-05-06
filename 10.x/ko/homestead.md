# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [시작하기](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용법](#daily-usage)
    - [SSH로 접속하기](#connecting-via-ssh)
    - [추가 사이트 등록](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [Mailpit 설정](#configuring-mailpit)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
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

Laravel은 여러분의 로컬 개발 환경을 포함하여 전체 PHP 개발 경험이 즐거울 수 있도록 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는 미리 구성된 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버 또는 기타 서버 소프트웨어를 설치할 필요 없이 우수한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 쉽게 관리하고 프로비저닝할 수 있는 우아한 방법을 제공합니다. Vagrant 박스는 언제든 폐기 가능합니다. 문제가 생기더라도 박스를 몇 분 만에 삭제하고 다시 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 어디서나 실행되며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 훌륭한 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!WARNING]  
> Windows를 사용하는 경우 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 이는 일반적으로 BIOS에서 활성화할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함 소프트웨어

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
### 시작하기

Homestead 환경을 시작하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads) 및 다음 중 하나의 지원되는 프로바이더를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

위 소프트웨어들은 모든 주요 운영 체제용 쉬운 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 이는 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 저장소를 호스트 머신에 클론하여 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로, 홈 디렉터리 내 `Homestead` 폴더에 저장소를 클론하는 것을 권장합니다. 본 문서에서는 이 디렉터리를 "Homestead 디렉터리"로 지칭합니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead 저장소를 클론한 후에는 `release` 브랜치로 체크아웃해야 합니다. 이 브랜치는 항상 최신 안정 버전의 Homestead를 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

그 다음 Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 구성 파일을 생성합니다. 이 파일에서 Homestead 설치를 위한 모든 설정을 지정할 수 있으며, Homestead 디렉터리에 위치하게 됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정

<a name="setting-your-provider"></a>
#### 프로바이더 설정

`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 프로바이더가 무엇인지 지정합니다: `virtualbox` 또는 `parallels`:

    provider: virtualbox

> [!WARNING]  
> Apple Silicon을 사용하는 경우 Parallels 프로바이더가 필수입니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더 목록을 지정합니다. 이 폴더 내 파일이 변경되면, 로컬 컴퓨터와 Homestead 가상 환경 간에 동기화됩니다. 필요한 만큼 많은 공유 폴더를 구성할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]  
> Windows 사용자는 `~/` 경로를 사용하지 말고, `C:\Users\user\Code\project1` 처럼 전체 경로를 사용해야 합니다.

여러 애플리케이션을 하나의 큰 디렉터리가 아닌 각각 개별 폴더에 매핑하는 것이 좋습니다. 폴더를 매핑하면 가상 머신이 해당 폴더 내 모든 파일의 디스크 IO를 추적해야 하므로, 파일이 많은 경우 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]  
> Homestead 사용 시 현재 디렉터리(`.`)를 마운트해서는 안 됩니다. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않아 일부 선택적 기능이 작동하지 않거나 예기치 않은 결과를 초래할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 폴더 매핑에 `type` 옵션을 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]  
> Windows에서 NFS를 사용할 때는 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려하세요. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉터리의 올바른 사용자/그룹 권한을 유지해 줍니다.

Vagrant의 [동기화 폴더(Synced Folders)](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)가 지원하는 옵션도 `options` 키 하위에 지정할 수 있습니다:

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
### Nginx 사이트 설정

Nginx에 익숙하지 않으셔도 괜찮습니다. `Homestead.yaml`의 `sites` 속성을 이용하면 "도메인"을 Homestead 환경 내 폴더에 쉽게 매핑할 수 있습니다. 예시 사이트 설정이 `Homestead.yaml` 파일에 포함되어 있습니다. 필요한 만큼 많은 사이트를 추가할 수 있으니, Homestead를 다양한 Laravel 애플리케이션의 편리한 가상 환경으로 활용할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

`sites` 속성을 변경한 후에는 터미널에서 `vagrant reload --provision` 명령을 실행하여 가상 머신의 Nginx 설정을 업데이트해야 합니다.

> [!WARNING]  
> Homestead 스크립트는 최대한 멱등성이 보장되도록 설계되었습니다. 하지만 프로비저닝 중 문제가 발생하면 `vagrant destroy && vagrant up` 명령으로 머신을 삭제한 후 재생성하세요.

<a name="hostname-resolution"></a>
#### 호스트네임(도메인) 해상

Homestead는 `mDNS`를 사용해 호스트네임을 자동으로 게시합니다. `Homestead.yaml`에 `hostname: homestead`로 지정하면, 호스트는 `homestead.local`에서 접근할 수 있습니다. macOS, iOS, Linux는 기본적으로 `mDNS`를 지원합니다. Windows에서는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트네임은 [프로젝트별 설치](#per-project-installation) 방식에서 가장 효과적입니다. 여러 사이트를 단일 Homestead 인스턴스에서 운영할 경우, 각 웹사이트의 "도메인"을 로컬 머신의 `hosts` 파일에 등록하세요. `hosts` 파일은 Homestead 사이트 요청을 가상 머신으로 리디렉션합니다. macOS/Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts` 위치입니다. 예시는 다음과 같습니다:

    192.168.56.56  homestead.test

등록된 IP 주소는 반드시 `Homestead.yaml` 파일에 설정된 값이어야 합니다. 도메인 추가 후 Vagrant 박스를 실행하면 웹 브라우저에서 사이트에 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead는 여러 서비스를 기본적으로 시작합니다. 하지만 프로비저닝 시 활성 또는 비활성화할 서비스를 커스터마이즈할 수 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml`의 `services` 옵션을 수정하세요:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

지정된 서비스는 `enabled` 및 `disabled` 지시에 따라 순서대로 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml`을 원하는 대로 수정한 후, Homestead 디렉터리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더 및 Nginx 사이트를 자동으로 설정합니다.

머신을 종료하려면 `vagrant destroy` 명령을 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역으로 설치하여 모든 프로젝트에서 동일한 Homestead 가상 머신을 공유하는 대신, 관리하는 각 프로젝트별로 Homestead 인스턴스를 구성할 수도 있습니다. 프로젝트별 설치 시 `Vagrantfile`을 함께 제공할 수 있으므로, 다른 개발자가 저장소를 클론 한 후 바로 `vagrant up`으로 개발 환경을 실행할 수 있다는 장점이 있습니다.

Composer 패키지 매니저를 이용해 프로젝트에 Homestead를 설치하세요:

```shell
composer require laravel/homestead --dev
```

설치 후, Homestead의 `make` 명령을 실행하여 프로젝트용 `Vagrantfile`과 `Homestead.yaml` 파일을 생성하세요. 이 파일들은 프로젝트의 루트에 위치합니다. `make` 명령이 자동으로 `Homestead.yaml`의 `sites` 및 `folders`를 초기화합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 다음 `vagrant up`을 실행하면 브라우저에서 `http://homestead.test`로 프로젝트에 접속할 수 있습니다. 자동 [호스트네임 해상](#hostname-resolution)을 사용하지 않는 경우, `homestead.test` 또는 원하는 도메인에 대한 `/etc/hosts` 파일 항목을 추가해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml`의 `features` 옵션에서 활성화/비활성화할 수 있습니다. 대부분의 기능은 불리언 값으로 활성/비활성화하며, 일부 기능은 추가 설정이 가능합니다.

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

지원되는 Elasticsearch 버전을 지정할 수 있으며(정확한 major.minor.patch 버전 필요), 기본 설치 클러스터명은 'homestead'입니다. Elasticsearch에는 운영체제 메모리의 절반 이상을 할당하지 마세요. 즉, Homestead 가상 머신은 Elasticsearch 할당량의 두 배 이상 메모리가 필요합니다.

> [!NOTE]  
> 환경을 커스터마이즈하려면 [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL의 대체재이므로 애플리케이션의 데이터베이스 설정에서 여전히 `mysql` 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치에서는 데이터베이스 사용자명이 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치에서는 데이터베이스 사용자명이 `homestead`, 비밀번호는 `secret`으로 설정됩니다. Neo4j 브라우저에는 `http://homestead.test:7474`으로 접근할 수 있습니다. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)은 Neo4j 클라이언트 요청에 사용할 수 있게 열려 있습니다.

<a name="aliases"></a>
### 별칭(Aliases)

Homestead 가상 머신에 Bash 별칭을 추가하려면 Homestead 디렉터리 내 `aliases` 파일을 수정하세요:

```shell
alias c='clear'
alias ..='cd ..'
```

별칭 파일을 수정한 후에는 `vagrant reload --provision`을 실행해야 변경된 별칭이 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전에, 먼저 기존 가상 머신을 Homestead 디렉터리에서 제거하세요:

```shell
vagrant destroy
```

다음으로, Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면, 저장소 경로에서 다음 명령을 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령은 GitHub 저장소에서 최신 Homestead 코드를 가져오고, 최신 태그를 가져오며, 최신 안정 버전으로 체크아웃합니다. 최신 안정 버전은 Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`을 통해 Homestead를 설치했다면 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고, 의존성을 업데이트하세요:

```shell
composer update
```

이후 Vagrant 박스도 업데이트하세요:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후에는 Homestead 디렉터리에서 `bash init.sh`를 실행하여 추가 구성 파일을 갱신할 수 있습니다. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 확인 메시지가 표시됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로, 최신 Vagrant 설치를 사용하도록 Homestead 가상 머신을 재생성해야 합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용법

<a name="connecting-via-ssh"></a>
### SSH로 접속하기

Homestead 디렉터리에서 `vagrant ssh` 명령을 실행하면 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 등록

Homestead 환경이 프로비저닝되고 실행 중이라면, 다른 Laravel 프로젝트를 위한 Nginx 사이트를 추가하고 싶을 수 있습니다. 하나의 Homestead 환경에서 원하는 만큼 많은 Laravel 프로젝트를 운영할 수 있습니다. 추가하려는 사이트를 `Homestead.yaml`에 등록하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]  
> 사이트 등록 전에 [공유 폴더 설정](#configuring-shared-folders)이 필요합니다.

Vagrant가 자동으로 "hosts" 파일을 관리하지 않을 경우, 새로운 사이트도 hosts 파일에 추가해야 할 수 있습니다. macOS/Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`입니다:

    192.168.56.56  homestead.test
    192.168.56.56  another.test

사이트를 추가한 후, Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 다양한 "사이트 유형"을 지원하여, Laravel 기반이 아닌 프로젝트도 쉽게 운영할 수 있습니다. 예를 들어, Statamic 애플리케이션을 `statamic` 사이트 유형으로 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원되는 사이트 유형은 다음과 같습니다: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
#### 사이트 파라미터

사이트에 Nginx의 추가적인 `fastcgi_param` 값을 지정하려면 `params` 지시자를 사용하세요:

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

전역 환경 변수는 `Homestead.yaml` 파일에 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 파일을 수정한 후에는 `vagrant reload --provision` 명령을 실행하여 머신을 다시 프로비저닝하세요. 이는 모든 PHP 버전의 PHP-FPM 설정을 갱신하며, `vagrant` 사용자 환경도 업데이트합니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경으로 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80으로 포워딩
- **HTTPS:** 44300 → 443으로 포워딩

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

원하는 경우 `Homestead.yaml` 파일의 `ports` 구성 항목을 통해 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. 구성 변경 후 `vagrant reload --provision` 명령으로 머신을 다시 프로비저닝하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

아래는 호스트 머신에서 Vagrant 박스로 매핑할 수 있는 추가 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22번 포트
- **ngrok UI:** 4040 → 4040번 포트
- **MySQL:** 33060 → 3306번 포트
- **PostgreSQL:** 54320 → 5432번 포트
- **MongoDB:** 27017 → 27017번 포트
- **Mailpit:** 8025 → 8025번 포트
- **Minio:** 9600 → 9600번 포트

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 하나의 가상 머신에서 여러 PHP 버전 사용을 지원합니다. 특정 사이트에 사용할 PHP 버전은 `Homestead.yaml`에서 지정할 수 있습니다. 지원되는 PHP 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내](#connecting-via-ssh)에서는 CLI에서 원하는 PHP 버전으로 artisan 등 명령을 실행할 수 있습니다:

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

CLI에서 기본 PHP 버전을 변경하려면 가상 머신 내부에서 아래 명령을 실행하세요:

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

MySQL과 PostgreSQL 모두에 대해 `homestead` 데이터베이스가 기본적으로 구성되어 있습니다. 로컬 머신의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL에 접속하려면 `127.0.0.1`의 포트 `33060`(MySQL) 또는 `54320`(PostgreSQL)으로 접속해야 합니다. 사용자명과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]  
> 호스트 머신에서 데이터베이스에 접속할 때만 이 비표준 포트를 사용해야 합니다. 가상 머신 내 Laravel 애플리케이션의 `database` 설정 파일에서는 기본 포트(3306, 5432)를 사용하세요.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead 가상 머신을 삭제할 때 자동으로 데이터베이스 백업을 할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요하거나, 오래된 버전에서는 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 아래 라인을 추가하세요:

    backup: true

설정 후 `vagrant destroy` 명령이 실행되면 Homestead가 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉터리에 데이터베이스를 내보냅니다. 이 디렉터리는 Homestead를 설치한 폴더 또는 [프로젝트별 설치](#per-project-installation)에서는 프로젝트 루트에 위치합니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 [크론 작업 스케줄링](/docs/{{version}}/scheduling)을 위해 매 분마다 `schedule:run` 아티즌 명령을 실행하도록 설정할 수 있습니다. 이 명령은 `App\Console\Kernel` 클래스의 스케줄을 분석하여 어느 작업을 실행할지 결정합니다.

Homestead 사이트에서 `schedule:run`을 매 분마다 실행하게 하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 지정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)을 사용하면 발송되는 이메일을 실제 수신자에게 보내지 않고 가로채어 내용을 확인할 수 있습니다. 사용을 시작하려면 애플리케이션의 `.env` 파일을 다음과 같이 설정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

설정 후, `http://localhost:8025`에서 Mailpit 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 오픈 소스 오브젝트 스토리지 서버입니다. 설치하려면, `Homestead.yaml`의 [features](#installing-optional-features) 섹션에 아래와 같이 추가하세요:

    minio: true

기본적으로 Minio는 9600번 포트에서 사용할 수 있습니다. `http://localhost:9600`에서 Minio 관리자 패널에 접속할 수 있습니다. 기본 access key는 `homestead`, secret key는 `secretkey`입니다. region은 항상 `us-east-1`을 사용하세요.

Minio를 사용하려면 애플리케이션의 `config/filesystems.php` 파일의 S3 디스크 설정을 아래와 같이 조정하세요. `use_path_style_endpoint` 옵션을 추가하고, `url` 키를 `endpoint`로 변경해야 합니다:

```php
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

그리고 `.env` 파일에 다음 항목이 있는지 확인하세요:

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시자를 추가하세요. 버킷 정의 후 터미널에서 `vagrant reload --provision` 명령을 실행하세요:

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

Homestead에서 [Laravel Dusk](/docs/{{version}}/dusk) 테스트를 실행하려면, Homestead 설정의 [`webdriver` 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

`webdriver` 기능 활성화 후 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기

때때로 작업 중인 내용을 동료나 고객과 공유해야 할 경우가 있습니다. Vagrant에는 내장된 `vagrant share` 명령이 있지만, `Homestead.yaml`에 여러 사이트가 구성되어 있으면 작동하지 않습니다.

이 문제를 해결하기 위해 Homestead는 자체 `share` 명령을 제공합니다. 먼저, [`vagrant ssh`](#connecting-via-ssh)로 Homestead 가상 머신에 접속한 후, `share homestead.test` 명령을 실행하세요. 이 명령은 `Homestead.yaml`에 등록된 `homestead.test` 사이트를 공유합니다. 원하는 다른 사이트명으로 대체할 수도 있습니다:

```shell
share homestead.test
```

명령을 실행하면 ngrok 화면이 표시되고, 공유 사이트의 접속 가능한 퍼블릭 URL 및 활동 로그가 나타납니다. 커스텀 region, 서브도메인, 기타 ngrok 설정을 지정하려면 다음과 같이 명령에 추가하세요:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTP가 아닌 HTTPS로 콘텐츠를 공유하려면 `share` 대신 `sshare` 명령을 사용할 수 있습니다.

> [!WARNING]  
> Vagrant는 본질적으로 보안성을 보장하지 않으며, `share` 명령을 사용할 땐 가상 머신이 인터넷에 노출된다는 사실을 기억하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 이용한 스텝 디버깅을 지원합니다. 예를 들어, 브라우저로 페이지에 접속하면 PHP가 IDE로 연결되어 실행 중인 코드를 검사하고 수정할 수 있습니다.

기본적으로 Xdebug는 이미 실행 중이며 연결을 수신할 준비가 되어 있습니다. CLI에서 Xdebug를 활성화하려면, Homestead 가상 머신에서 `sudo phpenmod xdebug` 명령을 입력하세요. IDE에서 디버깅 활성화 방법은 IDE의 안내를 따르세요. 또한 브라우저에서 확장 기능이나 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)을 이용해 Xdebug를 트리거해야 할 수도 있습니다.

> [!WARNING]  
> Xdebug는 PHP 실행을 상당히 느리게 만듭니다. 비활성화하려면 Homestead 가상 머신 내에서 `sudo phpdismod xdebug`를 실행한 후 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버에 요청하는 기능 테스트에서 Xdebug를 자동 시작하는 것이 개발에 더 편리합니다. 자동 시작하려면 Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 다음과 같이 수정하세요:

```ini
; Homestead.yaml에 다른 IP 대역이 지정된 경우, 이 주소는 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 쉘 별칭을 사용하세요:

    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션의 프로파일링을 위한 서비스입니다. 호출 그래프와 타임라인 형태의 인터랙티브 UI를 제공하며, 개발, 스테이징, 운영 환경에서 사용할 수 있고, 최종 사용자에게 별도의 오버헤드가 발생하지 않습니다. 또한 Blackfire는 코드 및 `php.ini` 환경 설정에 대한 성능, 품질, 보안 체크도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 크롤링, 웹 테스트, 스크래핑 기능을 제공하는 오픈 소스 도구로서 Blackfire와 연동하여 프로파일링 시나리오를 스크립팅할 수 있습니다.

Blackfire를 활성화하려면 Homestead 구성 파일의 "features" 설정을 사용하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 자격증명과 클라이언트 자격증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 프로파일링 옵션을 제공합니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml`의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 여러 인터페이스를 추가할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지 네트워크](https://developer.hashicorp.com/vagrant/docs/networking/public_network)를 활성화하려면 `type`을 `public_network`로 변경하고, `bridge` 설정을 추가하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp) 사용을 원한다면 `ip` 옵션을 생략하세요:

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

Homestead는 Homestead 디렉터리 루트의 `after.sh` 스크립트를 이용해 확장할 수 있습니다. 이 파일에서 가상 머신을 더 잘 구성하고 커스터마이즈하는 데 필요한 임의의 셸 명령을 추가할 수 있습니다.

Ubuntu에서 패키지를 설치할 때, 기존 설정 파일을 유지할지 새 파일로 덮어쓸지 묻는 메시지가 표시될 수 있습니다. 이를 방지하려면 다음 명령을 사용하여 Homestead가 작성한 기존 구성 파일이 덮어쓰이지 않게 하세요:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이즈

팀과 함께 Homestead를 사용할 때 개발 환경을 자신의 취향에 맞게 조정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리 루트(즉, `Homestead.yaml`이 있는 폴더)에 `user-customizations.sh` 파일을 만들면 됩니다. 이 파일에 원하는 설정을 자유롭게 추가할 수 있지만, `user-customizations.sh`는 버전 관리하지 않는 것이 좋습니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver`를 `on` 상태로 설정합니다. 이를 통해 Homestead가 호스트 운영체제의 DNS 설정을 사용할 수 있습니다. 이 동작을 변경하려면 `Homestead.yaml`에 아래 설정을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```