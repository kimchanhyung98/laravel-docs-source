# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 걸음](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭 설정](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용법](#daily-usage)
    - [SSH 접속](#connecting-via-ssh)
    - [추가 사이트 추가](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트 설정](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 일정 설정](#configuring-cron-schedules)
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

Laravel은 PHP 개발 환경 전체를 쾌적하게 만드는 것을 목표로 합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식으로 제공되는 사전 구성된 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버 또는 기타 서버 소프트웨어를 설치하지 않아도 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 구성할 수 있는 간편하고 우아한 방법을 제공합니다. Vagrant 박스는 완전히 폐기 가능하므로 문제가 생기면 몇 분 안에 박스를 삭제하고 재생성할 수 있습니다!

Homestead는 Windows, macOS, Linux 어떤 시스템에서도 실행 가능하며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함하고 있습니다.

> [!WARNING]
> Windows 사용자는 하드웨어 가상화(VT-x)를 BIOS 설정에서 활성화해야 할 수도 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

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
### 첫 걸음

Homestead 환경을 실행하기 전, [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 아래 지원 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이들 소프트웨어는 대부분 운영 체제에 대해 시각적 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 비용은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 저장소를 호스트 컴퓨터에 클론하여 설치할 수 있습니다. Homestead 가상 머신은 모든 Laravel 프로젝트의 호스트가 되므로, 사용자 홈 디렉토리에 `Homestead` 폴더를 만들어 클론하는 것을 권장합니다. 이 문서에서는 이 경로를 "Homestead 디렉토리"라고 지칭합니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

클론 후에는 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치는 항상 최신 안정 버전을 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로, `bash init.sh` 명령을 실행하여 `Homestead.yaml` 구성 파일을 생성하세요. 이 파일에서 Homestead 설정을 구성하며 Homestead 디렉토리에 위치합니다:

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

`Homestead.yaml` 파일의 `provider` 키로 사용할 Vagrant 프로바이더를 지정합니다: `virtualbox` 또는 `parallels`:

```
provider: virtualbox
```

> [!WARNING]
> Apple Silicon 칩을 사용하는 경우, Parallels 프로바이더를 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성에는 Homestead 환경과 공유할 폴더를 나열합니다. 이 폴더 내 파일 변경 사항은 로컬 컴퓨터와 Homestead 가상 머신 간에 동기화됩니다. 필요한 만큼 공유 폴더를 구성할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자의 경우 `~/` 경로 문법을 사용하지 말고 `C:\Users\user\Code\project1` 처럼 전체 경로를 사용해야 합니다.

하나의 큰 디렉토리를 통으로 매핑하는 대신, 각 애플리케이션별로 개별 폴더 매핑을 지정하세요. 폴더 매핑 시, 가상 머신은 폴더 내 모든 파일의 디스크 IO를 추적해야 하므로, 파일이 많으면 성능 저하를 경험할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 현재 디렉토리(`.`)를 마운트하지 마세요. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않으며, 선택적 기능이 동작하지 않고 예상치 못한 문제가 발생할 수 있습니다.

`NFS`를 활성화하려면 공유 폴더 매핑에 `type` 옵션을 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS 사용 시 `vagrant-winnfsd` 플러그인 설치를 고려하세요. 이 플러그인은 Homestead 가상 머신 내 파일과 디렉토리에 적절한 사용자/그룹 권한을 유지시켜 줍니다.

Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) 기능에서 지원하는 옵션들은 `options` 키 아래에 나열할 수 있습니다:

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

Nginx가 익숙하지 않아도 괜찮습니다. `Homestead.yaml`의 `sites` 속성으로 도메인과 Homestead 내 특정 폴더를 쉽게 연결할 수 있습니다. 예시 사이트 설정이 `Homestead.yaml`에 포함되어 있습니다. 여러 사이트를 추가해서 Homestead를 각 Laravel 애플리케이션별로 사용할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

`sites` 속성을 변경한 후에는 가상 머신에서 Nginx 설정을 업데이트하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

> [!WARNING]
> Homestead 스크립트는 재실행해도 문제가 없도록 만들어졌지만, 프로비저닝 도중 문제가 생기면 `vagrant destroy && vagrant up` 명령으로 가상 머신을 재생성하세요.

<a name="hostname-resolution"></a>
#### 호스트명 해석

Homestead는 자동 호스트명 해석을 위해 `mDNS`를 사용합니다. `Homestead.yaml` 파일에 `hostname: homestead`를 설정하면, 호스트는 `homestead.local`로 접근할 수 있습니다. macOS, iOS, Linux 데스크탑 배포판은 기본적으로 mDNS를 지원하지만, Windows에서는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명 해석은 [프로젝트별 설치](#per-project-installation) 방식에서 가장 잘 작동합니다. 하나의 Homestead 인스턴스에서 여러 사이트를 호스팅하는 경우, 머신의 `hosts` 파일에 도메인을 추가해 요청을 Homestead 가상 머신으로 리다이렉트할 수 있습니다. MacOS와 Linux에서 `hosts` 파일은 `/etc/hosts`에, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 위치합니다. 추가하는 라인은 다음과 같습니다:

```text
192.168.56.56  homestead.test
```

`Homestead.yaml` 파일에 설정된 IP 주소인지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면, 웹 브라우저에서 다음과 같이 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead는 기본적으로 여러 서비스를 시작하지만, `Homestead.yaml` 파일의 `services` 옵션을 수정하여 필요한 서비스만 켜거나 끌 수 있습니다. 예를 들어 PostgreSQL을 활성화하고 MySQL을 비활성화하려면:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

나열된 순서대로 서비스가 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml`을 원하는 대로 수정한 뒤, Homestead 디렉토리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동으로 구성합니다.

가상 머신을 삭제하려면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역으로 설치하고 모든 프로젝트에서 하나의 가상 머신을 공유하지 않고, 프로젝트별로 Homestead 인스턴스를 구성할 수도 있습니다. 이렇게 하면 프로젝트 레포지토리에 `Vagrantfile`을 함께 배포하여 다른 개발자가 바로 `vagrant up` 명령으로 작업 환경을 시작할 수 있어 편리합니다.

Composer 패키지 관리자를 통해 프로젝트에 Homestead를 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```

설치 후에는 Homestead의 `make` 명령을 호출하여 프로젝트 루트에 `Vagrantfile`과 `Homestead.yaml` 파일을 생성하세요. 이 명령어는 `Homestead.yaml`의 `sites`와 `folders` 지시문도 자동으로 설정합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그다음 터미널에서 `vagrant up` 명령을 실행하고 브라우저에서 `http://homestead.test`로 접근하세요. 자동 [호스트명 해석](#hostname-resolution)을 사용하지 않는다면 `/etc/hosts`에 도메인을 추가해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적으로 설치할 소프트웨어는 `Homestead.yaml`의 `features` 옵션에 설정합니다. 대부분 기능은 불리언 값으로 활성화하거나 비활성화할 수 있으며, 일부 기능은 추가 구성을 지원합니다:

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

Elasticsearch의 지원 버전을 지정할 수 있으며, 정확한 버전 번호(major.minor.patch)를 입력해야 합니다. 기본 설치는 'homestead'라는 이름의 클러스터를 생성합니다. Elasticsearch에 운영 체제 메모리의 절반 이상을 할당하지 말고, Homestead 가상 머신에 Elasticsearch 할당량의 두 배 이상 메모리가 있는지 확인하세요.

> [!NOTE]
> 구성 커스터마이징 방법은 [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL 대체품으로 보통 문제없이 작동하므로, 애플리케이션 데이터베이스 설정에서는 여전히 `mysql` 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치는 데이터베이스 사용자 이름을 `homestead`, 비밀번호를 `secret`으로 설정합니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치 역시 데이터베이스 사용자 이름을 `homestead`, 비밀번호를 `secret`으로 설정합니다. Neo4j 브라우저는 웹 브라우저에서 `http://homestead.test:7474`에 접속해 사용합니다. 포트 `7687` (Bolt), `7474` (HTTP), `7473` (HTTPS)이 Neo4j 클라이언트 요청에 대기 중입니다.

<a name="aliases"></a>
### 별칭 설정

Homestead 디렉토리 내 `aliases` 파일을 수정하여 Bash 별칭을 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일 수정 후에는 `vagrant reload --provision` 명령으로 가상 머신을 재프로비저닝해야 별칭이 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

업데이트 전에 Homestead 디렉토리에서 현재 가상 머신을 삭제해야 합니다:

```shell
vagrant destroy
```

그다음, 소스 코드를 업데이트합니다. 저장소를 클론했다면 클론한 위치에서 다음 명령을 입력하세요:

```shell
git fetch

git pull origin release
```

이 명령어는 GitHub에서 최신 Homestead 코드를 받아오고, 최근 태그를 가져온 후 최신 안정 태그를 체크아웃합니다. 최신 안정 버전 정보는 Homestead의 [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`을 통해 설치했다면 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 다음 명령어로 종속성을 업데이트하세요:

```shell
composer update
```

이후 Vagrant 박스를 업데이트합니다:

```shell
vagrant box update
```

박스 업데이트 후에는 Homestead 디렉토리에서 `bash init.sh` 명령을 실행해 추가 구성 파일들을 업데이트하세요. 이 과정에서 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일들을 덮어쓸지 묻습니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 새 Vagrant 설치판을 적용하려면 가상 머신을 다시 생성하세요:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용법

<a name="connecting-via-ssh"></a>
### SSH 접속

Homestead 디렉토리에서 `vagrant ssh` 명령어로 가상 머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가

Homestead 환경이 프로비저닝되고 실행 중이라면, 추가 Laravel 프로젝트를 위한 Nginx 사이트를 더 만들 수 있습니다. 원하는 만큼 사이트를 추가할 수 있으며, `Homestead.yaml`에 내용을 추가하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트를 추가하기 전, 해당 프로젝트 디렉토리에 대한 [폴더 매핑](#configuring-shared-folders)을 먼저 구성했는지 확인하세요.

Vagrant가 자동으로 "hosts" 파일을 관리하지 않는다면, 새 사이트를 `hosts` 파일에도 추가해야 할 수 있습니다. macOS와 Linux의 경우 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts` 에 위치합니다:

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 후 `vagrant reload --provision` 명령을 실행해 구성 변경을 적용하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 Laravel이 아닌 다른 유형의 프로젝트도 쉽게 실행할 수 있도록 여러 "사이트 타입"을 지원합니다. 예를 들어, Statamic 애플리케이션을 `statamic` 타입으로 쉽게 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원되는 사이트 타입 목록은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (기본값), `proxy` (nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, 및 `zf`입니다.

<a name="site-parameters"></a>
#### 사이트 파라미터

Nginx `fastcgi_param` 값을 사이트에 추가하려면 `params` 지시문을 사용하세요:

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

`Homestead.yaml` 파일에 전역 환경 변수를 정의할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

수정 후에는 `vagrant reload --provision` 명령으로 재프로비저닝해야, 모든 PHP 버전의 PHP-FPM 설정과 `vagrant` 사용자 환경이 갱신됩니다.

<a name="ports"></a>
### 포트 설정

기본적으로 다음 포트들이 Homestead에 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80 포트로 포워딩
- **HTTPS:** 44300 → 443 포트로 포워딩

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

추가 포트를 Vagrant 박스에 포워딩하고 싶다면, `Homestead.yaml`의 `ports` 항목에 설정할 수 있습니다. 변경 후에는 `vagrant reload --provision` 명령을 실행하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

아래는 호스트 머신에서 Vagrant 박스로 매핑할 만한 추가 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22 포트
- **ngrok UI:** 4040 → 4040 포트
- **MySQL:** 33060 → 3306 포트
- **PostgreSQL:** 54320 → 5432 포트
- **MongoDB:** 27017 → 27017 포트
- **Mailpit:** 8025 → 8025 포트
- **Minio:** 9600 → 9600 포트

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 하나의 가상 머신에서 여러 PHP 버전을 동시에 실행할 수 있습니다. 사이트별로 사용할 PHP 버전을 `Homestead.yaml` 파일에서 설정할 수 있습니다. 지원하는 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"이며 기본값은 "8.3"입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내](#connecting-via-ssh)에서는 CLI를 통해 다양한 PHP 버전을 사용할 수 있습니다:

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

기본 PHP CLI 버전을 변경하려면 가상 머신 내에서 다음 명령어 중 하나를 입력하세요:

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

MySQL과 PostgreSQL 모두 기본적으로 `homestead` 데이터베이스가 구성되어 있습니다. 호스트 컴퓨터에서 MySQL 또는 PostgreSQL 클라이언트로 접속하려면 IP `127.0.0.1`과 포트 `33060`(MySQL), `54320`(PostgreSQL)으로 연결하세요. 두 데이터베이스의 사용자명과 비밀번호는 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트 컴퓨터에서 접근할 때만 비표준 포트를 사용하세요. Laravel 애플리케이션에서는 가상 머신 내에서 동작하므로 기본 3306, 5432 포트를 사용해야 합니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 가상 머신이 삭제될 때 자동으로 데이터베이스를 백업할 수 있습니다. 이를 사용하려면 Vagrant 2.1.0 이상을 사용하거나 구버전이라면 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 다음 항목을 추가하세요:

```yaml
backup: true
```

설정 후, `vagrant destroy` 명령어 실행 시 데이터베이스가 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉토리에 내보내집니다. 이 폴더는 Homestead 설치 폴더나 [프로젝트별 설치](#per-project-installation) 시 프로젝트 루트에 존재합니다.

<a name="configuring-cron-schedules"></a>
### 크론 일정 설정

Laravel은 단일 `schedule:run` Artisan 명령을 매 분 실행하여 [크론 작업 예약](/docs/master/scheduling)을 간편하게 처리합니다. 이 명령어는 `routes/console.php` 파일의 작업 일정을 검토해 실행할 작업을 판단합니다.

특정 Homestead 사이트에서 `schedule:run` 명령이 실행되도록 하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

이 설정에 따라 해당 사이트의 크론 작업이 가상 머신 `/etc/cron.d` 디렉토리에 추가됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)은 발송 메일을 가로채 수신자에게 실제 메일을 보내지 않고도 내용을 확인할 수 있는 도구입니다. 시작하려면 애플리케이션의 `.env` 파일을 다음과 같이 설정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit이 설정되면, `http://localhost:8025`에서 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 가진 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 `Homestead.yaml`의 [features](#installing-optional-features) 섹션에 다음을 추가하세요:

```
minio: true
```

기본적으로 Minio는 9600 포트에서 서비스됩니다. `http://localhost:9600`에서 Minio 제어판에 접속할 수 있으며, 기본 액세스 키는 `homestead`, 비밀 키는 `secretkey`입니다. 접속 시 항상 리전으로 `us-east-1`을 사용해야 합니다.

Minio를 사용하려면 `.env` 파일에 다음 설정이 포함되어야 합니다:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio에서 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시문을 추가하고, 정의가 끝나면 `vagrant reload --provision`명령을 실행하세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

`policy` 옵션은 `none`, `download`, `upload`, `public` 중에 선택할 수 있습니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 내에서 [Laravel Dusk](/docs/master/dusk) 테스트를 실행하려면, Homestead 설정에서 [`webdriver` 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

기능 활성화 후, 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기

개발 중인 환경을 동료나 클라이언트와 공유할 때, Vagrant는 `vagrant share` 명령을 제공합니다. 하지만 여러 사이트를 `Homestead.yaml`에 구성했다면 작동하지 않습니다.

이를 해결하기 위해 Homestead는 자체 `share` 명령을 포함합니다. Homestead 가상 머신에 [SSH 접속](#connecting-via-ssh) 후, 다음 명령을 실행해 `homestead.test` 사이트를 공유하세요. 다른 사이트명으로도 대체 가능합니다:

```shell
share homestead.test
```

명령 실행 후 Ngrok 화면이 나타나 로그와 공유된 사이트의 공개 URL을 보여줍니다. 지역, 서브도메인, 기타 Ngrok 옵션을 지정하려면 다음처럼 실행하세요:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS 공유가 필요하면 `share` 대신 `sshare` 명령을 사용하세요.

> [!WARNING]
> Vagrant는 본질적으로 보안이 취약하므로 `share` 명령 실행 시 가상 머신을 인터넷에 노출하는 위험이 있습니다.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 사용한 스텝 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지를 열면 PHP가 IDE와 연결되어 실행 중인 코드를 검사하고 수정할 수 있습니다.

기본적으로 Xdebug는 실행 중이며 연결을 대기합니다. CLI에서 Xdebug를 활성화하려면 Homestead 가상 머신에서 `sudo phpenmod xdebug`를 실행하세요. 이후 IDE 지침대로 설정하고, 브라우저에 확장 프로그램이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)을 설치해 디버깅을 시작하세요.

> [!WARNING]
> Xdebug는 PHP 실행 속도를 크게 느리게 만듭니다. 끄려면 `sudo phpdismod xdebug`를 실행한 후 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버에 요청하는 기능 테스트를 디버깅할 때마다 헤더나 쿠키를 조작하기보다 Xdebug가 자동 시작되게 설정할 수 있습니다. Homestead 가상 머신에 있는 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하여 다음 내용을 추가하세요:

```ini
; Homestead.yaml에 다른 서브넷 IP가 설정된 경우 주소가 달라질 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 쉘 별칭을 사용하세요:

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션 프로파일링 서비스입니다. 인터랙티브 UI에서 호출 그래프와 타임라인으로 프로파일 데이터를 보여줍니다. 개발, 스테이징, 프로덕션 환경 모두에 적합하며 최종 사용자에게는 오버헤드가 없습니다. 또한 코드와 `php.ini` 설정의 성능, 품질, 보안 점검도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 연동해 프로파일 시나리오를 스크립팅할 수 있는 오픈 소스 웹 크롤링 및 테스트 애플리케이션입니다.

활성화하려면 Homestead 설정 파일의 `features` 항목에 다음 내용을 추가하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격 증명 사용을 위해 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 프로파일링 방법을 제공합니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 가상 머신의 네트워크 인터페이스를 구성합니다. 필요한 만큼 인터페이스를 추가할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면 `bridge` 설정을 추가하고 네트워크 타입을 `public_network`로 변경하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 `ip` 옵션을 제거하세요:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크가 사용할 디바이스를 변경하려면 `dev` 옵션을 설정할 수 있습니다. 기본값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead 디렉토리 루트의 `after.sh` 스크립트를 사용해 Homestead를 확장할 수 있습니다. 이 파일에 가상 머신을 적절히 설정하고 커스터마이징하는 데 필요한 셸 명령어를 추가하세요.

패키지 설치 시 Ubuntu가 패키지의 기존 설정을 유지 또는 덮어쓸지 묻는 경우가 있습니다. 이 문제를 피하려면 다음 명령어를 사용해 패키지를 설치하세요. Homestead가 이전에 작성한 설정을 덮어쓰지 않도록 강제합니다:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 맞춤 설정

팀 내에서 Homestead를 개인 개발 스타일에 맞게 조정하고 싶다면, Homestead 디렉토리 루트( `Homestead.yaml` 파일이 있는 같은 디렉토리)에 `user-customizations.sh` 파일을 만들고 원하는 커스터마이징을 추가하세요. 이 파일은 버전 관리 대상에 포함하지 않아야 합니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이렇게 하면 Homestead가 호스트 운영 체제의 DNS 설정을 사용할 수 있습니다. 이를 변경하려면 `Homestead.yaml`에 다음 설정을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```