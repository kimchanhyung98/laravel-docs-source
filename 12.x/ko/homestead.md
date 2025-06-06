# 라라벨 Homestead (Laravel Homestead)

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정하기](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치하기](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용](#daily-usage)
    - [SSH를 통한 접속](#connecting-via-ssh)
    - [사이트 추가하기](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 접속](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [Mailpit 설정](#configuring-mailpit)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug를 통한 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire를 통한 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장](#extending-homestead)
- [공급자별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 라라벨 Homestead는 더 이상 적극적으로 유지 관리되지 않는 레거시 패키지입니다. 현대적인 대안으로는 [Laravel Sail](/docs/12.x/sail)을 사용할 수 있습니다.

라라벨은 PHP 개발 경험 전체를 쾌적하게 만들기 위해 노력합니다. 이는 로컬 개발 환경까지도 포함됩니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버, 그 외 기타 서버 소프트웨어를 직접 설치할 필요 없이 바로 완벽한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 손쉽고 우아하게 관리 및 프로비저닝할 수 있는 기능을 제공합니다. Vagrant 박스는 완전히 폐기(재설정)할 수 있으며, 문제가 생기더라도 몇 분 안에 박스를 제거하고 다시 만들 수 있습니다.

Homestead는 Windows, macOS, Linux 모든 운영체제에서 동작하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 라라벨 애플리케이션 개발에 필요한 모든 소프트웨어를 미리 갖추고 있습니다.

> [!WARNING]
> Windows를 사용하는 경우, 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 대부분 BIOS에서 활성화할 수 있습니다. 또한 UEFI 시스템에서 Hyper-V를 사용 중이라면, VT-x에 접근하기 위해 Hyper-V를 비활성화해야 합니다.

<a name="included-software"></a>
### 포함된 소프트웨어

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
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk 유틸리티

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 첫 단계

Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 아래에 안내된 지원되는 공급자 중 하나를 반드시 설치해야 합니다.

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

위 소프트웨어들은 모두 대부분의 운영체제에서 사용하기 쉬운 설치 프로그램을 제공합니다.

Parallels 공급자를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 추가로 설치해야 하며, 별도의 비용은 들지 않습니다.

<a name="installing-homestead"></a>
#### Homestead 설치하기

Homestead는 호스트 컴퓨터에 Homestead 저장소를 클론(clone)하는 방식으로 설치할 수 있습니다. Homestead 가상 머신이 모든 라라벨 애플리케이션의 호스트 역할을 하게 되므로, `Homestead` 폴더를 "홈" 디렉터리 아래에 생성하여 저장소를 여러 프로젝트와 함께 관리하는 것을 추천합니다. 이 문서 전체에서 이 디렉터리를 "Homestead 디렉터리"라고 부르겠습니다.

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Homestead 저장소를 클론한 후에는 `release` 브랜치로 체크아웃해야 합니다. 이 브랜치는 항상 최신 안정화 버전의 Homestead가 포함되어 있습니다.

```shell
cd ~/Homestead

git checkout release
```

다음으로, Homestead 디렉터리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. 이 파일에서 Homestead의 모든 설정을 관리할 수 있습니다. `Homestead.yaml` 파일은 Homestead 디렉터리에 생성됩니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정하기

<a name="setting-your-provider"></a>
#### 공급자(provider) 설정

`Homestead.yaml` 파일의 `provider` 키를 통해 어떤 Vagrant 공급자를 사용할 것인지 지정할 수 있습니다. `virtualbox` 또는 `parallels` 중에서 선택합니다.

```
provider: virtualbox
```

> [!WARNING]
> Apple Silicon(M1, M2 등) 사용자는 Parallels 공급자를 필수로 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성에는 Homestead 환경과 공유할 폴더 목록을 지정합니다. 이 폴더의 파일이 변경되면 로컬 컴퓨터와 Homestead 가상 환경 간에 동기화가 이루어집니다. 필요한 만큼 많은 폴더를 공유로 지정할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 구문 대신 프로젝트의 전체 경로(예: `C:\Users\user\Code\project1`)를 사용해야 합니다.

애플리케이션마다 개별 폴더를 매핑하는 것이 좋으며, 여러 애플리케이션을 포함한 큰 디렉터리를 통째로 공유 폴더로 매핑하는 것은 피해야 합니다. 하나의 폴더를 매핑하면 가상 머신이 그 폴더 내의 *모든* 파일의 디스크 IO를 추적해야 하므로, 파일이 많은 경우 성능 저하가 발생할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead에서는 `.` (현재 디렉터리) 경로를 절대 마운트하면 안 됩니다. 이 경우 Vagrant에서 현재 폴더를 `/vagrant`로 매핑하지 않으므로 선택적 기능이 제대로 동작하지 않거나 예기치 못한 문제가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 폴더 매핑에 `type` 옵션을 추가할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 때는 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것이 좋습니다. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉터리의 사용자/그룹 권한을 올바르게 관리해줍니다.

추가로, Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)에서 지원하는 옵션들을 `options` 키 하위에 작성하여 전달할 수 있습니다.

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

Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 속성을 통해 Homestead 환경의 특정 폴더와 도메인 매핑을 쉽게 지정할 수 있습니다. 예제 사이트 설정이 기본으로 포함되어 있으며, 필요에 따라 여러 사이트를 추가할 수 있습니다. Homestead는 여러분이 작업 중인 각 라라벨 애플리케이션의 편리한 가상 환경이 되어줍니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Homestead 가상 머신을 프로비저닝(provisioning)한 뒤 `sites` 속성을 변경했다면 터미널에서 `vagrant reload --provision` 명령어를 실행하여 가상 머신의 Nginx 설정을 갱신해야 합니다.

> [!WARNING]
> Homestead 스크립트는 가능한 한 멱등성을 보장하도록 제작되었지만, 프로비저닝 중 문제가 생긴다면 `vagrant destroy && vagrant up` 명령어로 가상 머신을 완전히 재설치하는 것이 좋습니다.

<a name="hostname-resolution"></a>
#### 호스트네임(hostname) 해상

Homestead는 자동 호스트네임 해상 기능을 위해 `mDNS`를 사용하여 호스트네임을 배포합니다. `Homestead.yaml` 파일에 `hostname: homestead`로 설정하면 해당 호스트는 `homestead.local`에서 접근할 수 있습니다. macOS, iOS, Linux 데스크톱 배포판에는 기본적으로 `mDNS`가 포함되어 있습니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트네임 기능은 Homestead를 [프로젝트별 설치](#per-project-installation)로 사용할 때 가장 효과적입니다. 하나의 Homestead 인스턴스에서 여러 사이트를 운영하는 경우, 웹사이트의 "도메인"을 여러분이 사용하는 컴퓨터의 `hosts` 파일에 추가해야 합니다. `hosts` 파일을 사용하면 Homestead 사이트로의 요청이 Homestead 가상 머신으로 직접 연결됩니다. 이 파일의 기본 위치는 macOS와 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`입니다. 해당 파일에 아래와 같은 라인을 추가해야 합니다.

```text
192.168.56.56  homestead.test
```

추가한 IP 주소가 `Homestead.yaml` 파일에 지정된 IP와 일치하는지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면 웹 브라우저에서 해당 사이트에 접속할 수 있습니다.

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead에서는 여러 서비스를 기본적으로 실행하지만, 프로비저닝 시 어떤 서비스를 켜고 끌지 직접 지정할 수 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL은 비활성화하고 싶다면 `Homestead.yaml` 파일의 `services` 옵션을 수정하면 됩니다.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

지정한 서비스는 `enabled`와 `disabled` 항목의 순서에 따라 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml` 내용을 원하는 대로 수정했다면, Homestead 디렉터리에서 `vagrant up` 명령어를 실행하세요. Vagrant가 자동으로 가상 머신을 부팅하고 공유 폴더, Nginx 사이트 설정을 자동으로 적용합니다.

머신을 완전히 삭제하려면 `vagrant destroy` 명령어를 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

모든 프로젝트에서 하나의 Homestead 가상 머신을 전역 설치로 사용하는 대신, 프로젝트별로 Homestead 인스턴스를 별도로 구성하여 사용할 수도 있습니다. 프로젝트마다 Homestead를 별도로 구성하는 방식은 프로젝트와 함께 `Vagrantfile`까지 제공할 수 있어, 저장소를 클론한 후 바로 `vagrant up`만 실행하면 환경이 만들어진다는 장점이 있습니다.

프로젝트 디렉터리에 Composer 패키지 매니저로 Homestead를 설치할 수 있습니다.

```shell
composer require laravel/homestead --dev
```

Homestead 설치 후, Homestead의 `make` 명령어를 실행하면 해당 프로젝트를 위한 `Vagrantfile`과 `Homestead.yaml` 파일이 자동으로 생성됩니다. 이 파일들은 프로젝트 루트에 위치하며, `make` 명령어가 `Homestead.yaml` 내 `sites`와 `folders` 지시문도 자동으로 구성해 줍니다.

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

다음으로, 터미널에서 `vagrant up` 명령어를 실행한 후 브라우저에서 `http://homestead.test`로 접속하면 프로젝트를 사용할 수 있습니다. 자동 [호스트네임 해상](#hostname-resolution) 기능을 사용하지 않는 경우에는 반드시 도메인(`homestead.test` 등)을 `/etc/hosts` 파일에 직접 추가해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치하기

선택적 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불리언(true/false) 값으로 활성화할 수 있으며, 일부 기능은 다양한 설정 옵션을 지원합니다.

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

Elasticsearch의 설치 버전은 지원되는 정확한 버전(major.minor.patch)으로 지정할 수 있습니다. 기본 설치 시 'homestead'라는 이름의 클러스터가 생성됩니다. Elasticsearch에는 운영체제 메모리의 절반 이상을 절대 할당하지 않도록 하세요. 즉, Homestead 가상 머신에 Elasticsearch 할당 메모리의 두 배 이상 RAM이 필요합니다.

> [!NOTE]
> [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)에서 설정을 더 세부적으로 커스터마이즈하는 방법을 확인할 수 있습니다.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 대개 MySQL을 대체하여 사용할 수 있으므로, 애플리케이션의 데이터베이스 설정에서 `mysql` 드라이버를 계속 사용하면 됩니다.

<a name="mongodb"></a>
#### MongoDB

MongoDB의 기본 설정에서는 데이터베이스 사용자명이 `homestead`, 비밀번호는 `secret`으로 지정됩니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j의 기본 설치에서는 데이터베이스 사용자명이 `homestead`, 비밀번호가 `secret`으로 지정됩니다. Neo4j 브라우저에 접속하려면 웹 브라우저에서 `http://homestead.test:7474`로 이동하세요. `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS) 포트가 Neo4j 클라이언트에서 요청을 받을 수 있도록 열려 있습니다.

<a name="aliases"></a>
### 별칭(Aliases)

Homestead 가상 머신에서 Bash 별칭을 추가하고 싶다면, Homestead 디렉터리 내의 `aliases` 파일을 수정하면 됩니다.

```shell
alias c='clear'
alias ..='cd ..'
```

파일을 수정한 후에는 `vagrant reload --provision` 명령어로 Homestead 가상 머신을 재프로비저닝(re-provisioning)해야 바뀐 별칭이 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전에 현재 실행 중인 가상 머신을 Homestead 디렉터리에서 아래 명령어로 먼저 삭제하세요.

```shell
vagrant destroy
```

다음으로, Homestead의 소스 코드를 갱신해야 합니다. 저장소를 클론 받았다면, 저장소를 클론했던 위치에서 아래 명령어를 실행하면 됩니다.

```shell
git fetch

git pull origin release
```

이 명령어는 GitHub 저장소에서 최신 Homestead 코드를 가져오고, 최신 태그와 최신 태그 릴리스를 체크아웃합니다. 최신 안정화 릴리스는 Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

만약 프로젝트의 `composer.json` 파일을 통해 Homestead를 설치했다면, `composer.json`에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인한 후 아래 명령어로 의존성을 업데이트하세요.

```shell
composer update
```

그 다음에는 아래와 같이 `vagrant box update` 명령어로 Vagrant 박스를 업데이트해야 합니다.

```shell
vagrant box update
```

Vagrant 박스 업데이트 후 Homestead 디렉터리에서 `bash init.sh` 명령어를 실행해 Homestead의 추가 설정 파일을 갱신해야 합니다. 이 과정에서 기존의 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 여부를 묻는 안내가 표시됩니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로, 최신 Vagrant 설치를 적용하려면 Homestead 가상 머신을 다시 생성해야 합니다.

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용

<a name="connecting-via-ssh"></a>
### SSH를 통한 접속

Homestead 디렉터리에서 터미널에 `vagrant ssh` 명령어를 입력하면 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 사이트 추가하기

Homestead 환경이 프로비저닝 및 실행된 후, 다른 라라벨 프로젝트를 위한 추가 Nginx 사이트를 등록하고 싶을 수 있습니다. Homestead 환경 한 곳에서 원하는 만큼 많은 라라벨 프로젝트를 실행할 수 있습니다. 추가 사이트를 등록하려면 `Homestead.yaml` 파일에 사이트 정보를 추가하면 됩니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트를 추가하기 전에 해당 프로젝트 디렉터리에 대한 [공유 폴더 매핑](#configuring-shared-folders)이 정상적으로 설정되어 있는지 반드시 확인하세요.

Vagrant가 "hosts" 파일을 자동으로 관리하지 않는 경우, 새 사이트 도메인도 직접 hosts 파일에 추가해야 할 수 있습니다. macOS와 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 위치에 있습니다.

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트 정보를 추가했다면 Homestead 디렉터리에서 터미널로 `vagrant reload --provision` 명령어를 실행하세요.

<a name="site-types"></a>
#### 사이트 타입

Homestead는 다양한 "사이트 타입"을 지원하므로, 라라벨 기반이 아닌 프로젝트도 쉽게 실행할 수 있습니다. 예를 들어 Statamic 애플리케이션을 `statamic` 사이트 타입으로 등록할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 타입에는 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 등이 있습니다.

<a name="site-parameters"></a>
#### 사이트 파라미터

`params` 사이트 옵션을 사용하면 개별 Nginx 사이트에 추가 `fastcgi_param` 값을 지정할 수 있습니다.

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

`Homestead.yaml` 파일에 글로벌 환경 변수를 아래와 같이 지정할 수 있습니다.

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 파일을 수정한 후에는 `vagrant reload --provision` 명령어로 가상 머신을 재프로비저닝해야 합니다. 실행 시 설치된 모든 PHP 버전에 대한 PHP-FPM 설정이 갱신되며, `vagrant` 사용자 환경 변수도 반영됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트들이 Homestead 환경으로 포워딩됩니다.

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; 80 포트로 전달
- **HTTPS:** 44300 &rarr; 443 포트로 전달

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

필요하다면, `Homestead.yaml` 파일에서 `ports` 설정을 추가해 Vagrant 박스에 포트를 더 포워딩할 수 있습니다. 파일을 수정한 뒤에는 반드시 `vagrant reload --provision` 명령어로 가상 머신을 다시 프로비저닝해야 합니다.

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

아래는 호스트 머신에서 Vagrant 박스로 포워딩할 수 있는 Homestead 서비스 포트 목록입니다.

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; 22로 전달
- **ngrok UI:** 4040 &rarr; 4040으로 전달
- **MySQL:** 33060 &rarr; 3306으로 전달
- **PostgreSQL:** 54320 &rarr; 5432로 전달
- **MongoDB:** 27017 &rarr; 27017로 전달
- **Mailpit:** 8025 &rarr; 8025로 전달
- **Minio:** 9600 &rarr; 9600으로 전달

</div>

<a name="php-versions"></a>

### PHP 버전

Homestead는 동일한 가상 머신에서 여러 버전의 PHP를 실행할 수 있도록 지원합니다. 각 사이트마다 사용할 PHP 버전을 `Homestead.yaml` 파일 내에서 지정할 수 있습니다. 지원되는 PHP 버전은 다음과 같습니다: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", 그리고 "8.3"(기본값)입니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내에서](#connecting-via-ssh)는 다음과 같이 CLI를 통해 원하는 PHP 버전을 사용할 수 있습니다.

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

CLI에서 기본적으로 사용되는 PHP 버전을 변경하고 싶다면, Homestead 가상 머신 내부에서 다음 명령어 중 하나를 실행하면 됩니다.

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

`homestead`라는 데이터베이스가 MySQL과 PostgreSQL 모두에 기본으로 설정되어 있습니다. 호스트 머신에서 데이터베이스 클라이언트를 이용해 MySQL이나 PostgreSQL에 접속하려면, `127.0.0.1` IP에서 포트 `33060`(MySQL) 또는 `54320`(PostgreSQL)으로 연결하면 됩니다. 두 데이터베이스의 사용자명과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]
> 이와 같은 비표준 포트는 호스트 머신에서 데이터베이스에 접속할 때만 사용해야 합니다. 라라벨 애플리케이션의 `database` 설정 파일에서는 기본 포트인 3306과 5432로 지정해야 합니다. 라라벨은 _가상 머신 내부_에서 실행되기 때문입니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 가상 머신이 삭제될 때 자동으로 데이터베이스를 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상의 버전이 필요합니다. 이전 버전의 Vagrant를 사용 중이라면, `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 데이터베이스 백업을 활성화하려면 `Homestead.yaml` 파일에 다음 옵션을 추가하세요.

```yaml
backup: true
```

설정이 완료되면, `vagrant destroy` 명령어를 실행할 때마다 데이터베이스가 `.backup/mysql_backup`과 `.backup/postgres_backup` 디렉터리에 백업됩니다. 이 디렉터리는 Homestead를 설치한 폴더이거나, [프로젝트 별 설치](#per-project-installation) 방식을 사용할 경우 프로젝트의 루트 디렉터리에 위치하게 됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

라라벨은 매 분마다 한 번씩 `schedule:run` 아티즌 명령어를 실행하도록 예약함으로써 [크론 작업을 쉽게 관리](/docs/12.x/scheduling)할 수 있습니다. `schedule:run` 명령어는 `routes/console.php` 파일에 정의된 작업 스케줄을 확인하여 어떤 작업을 실행할지 결정합니다.

Homestead 사이트에서 `schedule:run` 명령어가 실행되도록 하려면 사이트를 정의할 때 `schedule` 옵션을 `true`로 설정하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)은 발신 이메일을 실제로 수신자에게 발송하지 않고 인터셉트하여 확인할 수 있는 툴입니다. 다음과 같이 애플리케이션의 `.env` 파일을 업데이트하여 Mailpit을 사용할 수 있습니다.

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit을 설정한 후에는 `http://localhost:8025`에서 Mailpit 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 API를 제공하는 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 `Homestead.yaml` 파일의 [features](#installing-optional-features) 섹션에 아래와 같은 설정 옵션을 추가하면 됩니다.

```
minio: true
```

Minio는 기본적으로 9600 포트에서 사용 가능합니다. `http://localhost:9600`에 접속해 Minio 관리 패널을 사용할 수 있습니다. 기본 access key는 `homestead`, 기본 secret key는 `secretkey`입니다. Minio에 접근할 때는 항상 `us-east-1` 리전을 사용해야 합니다.

Minio를 사용하려면 `.env` 파일에 아래와 같은 옵션이 포함되어 있어야 합니다.

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio를 이용해 "S3" 버킷을 생성하려면, `Homestead.yaml` 파일에 `buckets` 지시자를 추가하세요. 버킷 정의를 완료한 후에는 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원되는 `policy` 값은 다음과 같습니다: `none`, `download`, `upload`, `public`.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 내에서 [Laravel Dusk](/docs/12.x/dusk) 테스트를 실행하려면 Homestead 설정에서 [webdriver 기능](#installing-optional-features)을 활성화해야 합니다.

```yaml
features:
    - webdriver: true
```

`webdriver` 기능을 활성화한 후에는 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

<a name="sharing-your-environment"></a>
### 환경 공유

작업 중인 내용을 동료나 클라이언트와 공유하고 싶을 때가 있습니다. Vagrant는 내장된 `vagrant share` 명령어를 통해 이 기능을 지원하지만, `Homestead.yaml` 파일에 여러 사이트가 설정된 경우에는 작동하지 않습니다.

이 문제를 해결하기 위해 Homestead에는 자체적인 `share` 명령어가 포함되어 있습니다. [Homestead 가상 머신에 SSH 접속](#connecting-via-ssh)한 뒤, `share homestead.test` 명령어를 실행하세요. 이 명령어는 `Homestead.yaml` 설정 파일의 `homestead.test` 사이트를 공유합니다. 공유할 사이트 이름은 원하는 대로 변경할 수 있습니다.

```shell
share homestead.test
```

명령어 실행 후에는 Ngrok 화면이 나타나며, 여기서 사이트에 대한 로그와 공개 접근 가능한 URL을 확인할 수 있습니다. 만약 별도의 리전, 서브도메인 등 Ngrok 런타임 옵션을 지정하고자 한다면 아래와 같이 명령어에 추가할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTP 대신 HTTPS로 콘텐츠를 공유하려면 `share` 대신 `sshare` 명령어를 사용해야 합니다.

> [!WARNING]
> Vagrant는 구조적으로 보안에 취약하므로, `share` 명령어 실행 시 가상 머신이 인터넷에 노출된다는 점을 반드시 인지해야 합니다.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅하기

Homestead에는 [Xdebug](https://xdebug.org)를 이용한 단계별 디버깅 기능이 내장되어 있습니다. 예를 들어, 브라우저에서 페이지를 요청하면 PHP가 IDE에 연결되고, 실행 중인 코드를 직접 확인하거나 수정할 수 있습니다.

기본적으로 Xdebug는 바로 실행 가능하며, 연결을 받을 준비가 되어 있습니다. CLI에서 Xdebug를 활성화하려면 Homestead 가상 머신 내에서 `sudo phpenmod xdebug` 명령어를 실행하세요. 이후에는 IDE별 안내에 따라 디버깅을 활성화하면 됩니다. 마지막으로, 브라우저에서 Xdebug를 트리거하려면 익스텐션이나 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)을 사용할 수 있습니다.

> [!WARNING]
> Xdebug를 활성화하면 PHP의 실행 속도가 눈에 띄게 느려집니다. Xdebug를 끄려면 Homestead 가상 머신에서 `sudo phpdismod xdebug` 명령어를 실행한 다음 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버로 요청을 보내는 기능 테스트를 디버깅할 때, 단순히 요청 헤더나 쿠키를 통해 디버깅을 트리거하도록 테스트를 수정하는 것보다 Xdebug를 자동으로 시작하도록 설정하는 것이 더 편리합니다. Xdebug를 자동 시작하려면 Homestead 가상 머신 내의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하고 아래 설정을 추가하십시오.

```ini
; Homestead.yaml에서 IP 주소에 다른 서브넷을 설정했다면, 아래 주소도 달라질 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신에서 `xphp` 셸 별칭을 사용하면 됩니다.

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션을 프로파일링하는 데 사용하는 서비스입니다. 콜 그래프와 타임라인 형태로 프로파일 데이터를 보여주는 인터랙티브 UI를 제공하며, 개발, 스테이징, 운영 환경 모두에 적용할 수 있습니다. 엔드 유저에게는 오버헤드가 없으며, 코드와 `php.ini` 설정의 성능·품질·보안 체크도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 연계해 프로파일링 시나리오를 스크립트로 만드는 오픈 소스 웹 크롤링, 웹 테스트, 웹 스크래핑 도구입니다.

Blackfire를 활성화하려면 `Homestead.yaml` 설정 파일의 "features" 항목을 사용하세요.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 정보는 [Blackfire 계정이 필요](https://blackfire.io/signup)합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 프로파일링 방식을 지원합니다. 자세한 내용은 [Blackfire 공식 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼의 네트워크 인터페이스를 설정할 수 있습니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브릿지(bridged)](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면 네트워크 설정에 `bridge` 옵션을 추가하고, 네트워크 타입을 `public_network`로 바꿉니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 설정에서 `ip` 옵션만 제거하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크에서 사용할 장치를 변경하려면 네트워크 설정에 `dev` 옵션을 추가할 수 있습니다. 기본값은 `eth0`입니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead는 Homestead 디렉터리 루트에 있는 `after.sh` 스크립트를 이용해 확장할 수 있습니다. 이 파일 안에서 가상 머신을 적절히 설정하거나 커스터마이징하기 위해 필요한 모든 셸 명령어를 추가할 수 있습니다.

Homestead를 커스터마이즈할 때 Ubuntu가 패키지의 기존 설정 파일을 유지할 것인지, 새로운 설정 파일로 덮어쓸 것인지 선택하라는 질문을 할 수 있습니다. 이 경우 Homestead에서 미리 설정한 구성을 덮어쓰지 않으려면 아래와 같이 패키지 설치 시 커맨드를 사용하세요.

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징

팀에서 Homestead를 사용할 때, 각자의 개발 스타일에 맞게 Homestead를 설정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리(즉, `Homestead.yaml`이 위치한 폴더)에 `user-customizations.sh` 파일을 생성할 수 있습니다. 이 파일에서 필요한 모든 커스터마이징 작업을 자유롭게 수행할 수 있습니다. 단, `user-customizations.sh` 파일은 버전 관리에 포함하지 않는 것이 좋습니다.

<a name="provider-specific-settings"></a>
## 공급자(Provider)별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

Homestead는 기본적으로 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이를 통해 Homestead 가상 머신이 호스트 운영체제의 DNS 설정을 사용하도록 합니다. 만약 이 동작을 변경하고 싶다면, `Homestead.yaml` 파일에 다음 설정을 추가하세요.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```