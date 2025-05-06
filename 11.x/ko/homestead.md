# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [시작하기](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [옵션 기능 설치](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적 사용법](#daily-usage)
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

Laravel은 PHP 개발 환경 전체를 즐겁고 생산적으로 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는, 미리 구성된 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버, 기타 서버 소프트웨어를 설치하지 않고도 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 간편하고 우아하게 관리 및 프로비저닝하는 방법을 제공합니다. Vagrant 박스는 언제든지 손쉽게 삭제 및 재생성할 수 있습니다. 문제가 발생해도 몇 분 내에 박스를 다시 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 등 모든 운영체제에서 실행할 수 있으며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 놀라운 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!WARNING]  
> Windows를 사용하는 경우 하드웨어 가상화(VT-x) 기능을 활성화해야 할 수도 있습니다. BIOS를 통해 대부분 활성화할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우, VT-x 사용을 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

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
### 옵션 소프트웨어

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
- RVM (Ruby 버전 관리자)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk 유틸리티

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 시작하기

Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 다음 지원 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이 모든 소프트웨어는 주요 운영체제에서 손쉽게 사용할 수 있는 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면, [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 무료로 제공됩니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead는 호스트 머신에 Homestead 저장소를 클론하여 설치할 수 있습니다. Homestead 가상머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로, "home" 디렉터리 내 `Homestead` 폴더에 저장소를 클론하는 것이 좋습니다. 이 문서에서는 이를 "Homestead 디렉터리"라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

저장소를 클론한 뒤에는 `release` 브랜치로 체크아웃해야 합니다. 이 브랜치는 항상 Homestead의 최신 안정 버전을 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로, Homestead 디렉터리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 파일을 생성합니다. 이 파일에서 Homestead의 모든 설정을 지정할 수 있으며, Homestead 디렉토리에 저장됩니다:

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

`Homestead.yaml` 파일의 `provider` 키는 사용하려는 Vagrant 프로바이더가 `virtualbox`인지 `parallels`인지 지정합니다:

    provider: virtualbox

> [!WARNING]  
> Apple Silicon(M1/M2 등) 시스템에서는 Parallels 프로바이더를 필수로 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더 목록입니다. 이 폴더 내의 파일이 변경되면, 로컬 컴퓨터와 Homestead 가상환경 간에 자동으로 동기화됩니다. 필요한 만큼 여러 개의 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]  
> Windows 사용자는 `~/` 경로 문법을 사용하지 말고, 예를 들어 `C:\Users\user\Code\project1`처럼 전체 경로를 사용해야 합니다.

각 애플리케이션마다 별도의 폴더 매핑을 사용하는 것이 좋습니다. 하나의 큰 폴더를 전체로 매핑하면, 폴더 내 모든 파일의 디스크 I/O를 VM이 추적해야 하므로 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]  
> Homestead 사용 시, 현재 디렉토리(`.`)를 마운트하지 마세요. 그러면 `/vagrant`로 폴더가 매핑되지 않아 옵션 기능이 깨지고, 예기치 않은 결과가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 mapping에 `type` 옵션을 지정하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]  
> Windows에서 NFS 사용 시 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 이 플러그인은 Homestead VM 내 파일과 디렉토리의 올바른 사용자/그룹 권한을 유지합니다.

Vagrant의 [공유 폴더 옵션](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)도 `options` 키 하위에 지정할 수 있습니다:

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

Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 속성을 사용해 "도메인"을 Homestead 환경의 폴더에 간단히 매핑할 수 있습니다. 샘플 사이트 설정이 기본으로 포함되어 있습니다. 필요에 따라 여러 사이트를 추가할 수 있어, 모든 Laravel 애플리케이션 개발 환경으로 활용할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

사이트 설정을 변경한 후에는, 터미널에서 `vagrant reload --provision` 명령어를 실행하여 가상머신 내 Nginx 설정을 갱신해야 합니다.

> [!WARNING]  
> Homestead 스크립트는 가능하면 멱등(idempotent)하게 작성되어 있지만, 프로비저닝 중 문제가 발생한다면 `vagrant destroy && vagrant up` 명령어로 머신을 제거하고 재생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
#### 호스트네임(도메인명) 해상

Homestead는 `mDNS`를 이용해 호스트 이름을 자동으로 발행합니다. `Homestead.yaml`에서 `hostname: homestead`로 지정하면 `homestead.local`로 접근할 수 있습니다. macOS, iOS, Linux는 기본적으로 mDNS를 지원합니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=ko_KR&locale=ko_KR)를 설치해야 합니다.

자동 호스트네임은 [프로젝트별 설치](#per-project-installation)에서 가장 효과적입니다. 하나의 Homestead 인스턴스에 여러 사이트를 호스팅할 경우, 각 사이트의 "도메인"을 자신의 컴퓨터 `hosts` 파일에 추가하는 것이 좋습니다. macOS·Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 경로입니다. 예를 들어 다음과 같이 추가합니다:

    192.168.56.56  homestead.test

IP 주소가 `Homestead.yaml`에 지정된 값과 일치하는지 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행한 뒤에는 브라우저로 사이트에 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead는 기본적으로 여러 서비스를 시작합니다. 하지만 프로비저닝 시 어떤 서비스를 활성/비활성화할지 선택할 수 있습니다. 예를 들어 PostgreSQL은 활성화, MySQL은 비활성화하려면 `Homestead.yaml`의 `services` 옵션을 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

기재한 순서에 따라 지정된 서비스가 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml`을 원하는 대로 편집한 뒤, Homestead 디렉터리에서 `vagrant up` 명령어를 실행하세요. Vagrant가 가상머신을 시작하고, 공유 폴더와 Nginx 사이트를 자동으로 구성합니다.

머신을 삭제하려면 `vagrant destroy` 명령어를 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역(global)으로 설치하여 여러 프로젝트에서 공유하는 대신, 각 프로젝트마다 별도 Homestead 인스턴스를 사용할 수 있습니다. 프로젝트별 Homestead 설치는 프로젝트에 `Vagrantfile`을 함께 제공하여 팀원이 저장소를 클론한 후, 바로 `vagrant up`으로 개발 환경을 구성할 수 있다는 장점이 있습니다.

Composer를 사용해 Homestead를 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```

설치가 완료되면 Homestead의 `make` 명령을 실행하여 프로젝트에 `Vagrantfile`과 `Homestead.yaml`을 생성하세요. 이 파일들은 프로젝트 루트에 생성되며, `make` 명령어가 `Homestead.yaml`의 `sites` 및 `folders` 항목도 자동 설정합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 다음, 터미널에서 `vagrant up` 명령어를 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 [호스트네임 해상](#hostname-resolution)을 사용하지 않는 경우, `homestead.test` 또는 원하는 도메인을 `/etc/hosts` 파일에 추가해야 합니다.

<a name="installing-optional-features"></a>
### 옵션 기능 설치

옵션 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불리언값으로 활성/비활성화하며, 일부 기능은 추가 설정이 가능합니다:

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

지원하는 버전의 Elasticsearch(메이저.마이너.패치)를 정확히 지정해야 합니다. 기본 설치 시 클러스터명은 'homestead'로 생성됩니다. Elasticsearch에 할당하는 메모리는 운영체제의 절반을 넘지 않아야 하므로, Homestead VM의 메모리는 Elasticsearch 할당의 두 배 이상이어야 합니다.

> [!NOTE]  
> 설정 변경 자세한 정보는 [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL과 호환되므로 애플리케이션 DB 설정에서 `mysql` 드라이버를 계속 사용할 수 있습니다.

<a name="mongodb"></a>
#### MongoDB

MongoDB 기본 설치 시 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j를 기본 설치하면 사용자명 `homestead`와 비밀번호 `secret`이 적용됩니다. Neo4j 브라우저는 `http://homestead.test:7474`에서 접근할 수 있습니다. 7687(Bolt), 7474(HTTP), 7473(HTTPS) 포트가 클라이언트 요청을 받을 수 있도록 열려 있습니다.

<a name="aliases"></a>
### 별칭(Aliases)

Homestead 가상머신의 Bash 별칭은 Homestead 디렉터리의 `aliases` 파일을 수정해 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

파일 수정 후, `vagrant reload --provision` 명령어로 Homestead 가상머신을 다시 프로비저닝해야 새 별칭이 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead 업데이트를 시작하기 전, Homestead 디렉터리에서 현재 가상머신을 제거하세요:

```shell
vagrant destroy
```

다음으로 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론한 경우 아래 명령어로 최신 코드를 가져옵니다:

```shell
git fetch

git pull origin release
```

이 명령어는 최신 Homestead 소스 및 태그를 가져오고, 최신 출시 버전으로 체크아웃합니다. 최신 안정 버전은 [Homestead GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`으로 설치한 경우 `"laravel/homestead": "^12"`가 포함되어 있는지 확인한 뒤, 의존성을 업데이트하십시오:

```shell
composer update
```

그 다음, `vagrant box update` 명령어로 Vagrant 박스를 업데이트하세요:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후, Homestead 디렉터리에서 `bash init.sh`를 실행하여 Homestead의 추가 설정 파일을 갱신하세요. 기존의 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 여부를 묻는 메시지가 나옵니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로, 최신 Vagrant 설치를 적용하려면 Homestead 가상머신을 재생성합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적 사용법

<a name="connecting-via-ssh"></a>
### SSH로 접속하기

Homestead 디렉터리에서 `vagrant ssh` 명령어를 실행하여 가상머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 등록

Homestead 환경이 프로비저닝 및 실행 중이라면, 다른 Laravel 프로젝트를 위한 추가 Nginx 사이트를 등록할 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 동시에 운영할 수 있습니다. 추가할 사이트는 `Homestead.yaml` 파일에 등록하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]  
> 해당 프로젝트 디렉터리의 [폴더 매핑](#configuring-shared-folders)이 제대로 설정되어 있는지 확인하세요.

Vagrant가 "hosts" 파일을 자동으로 관리하지 않는 경우, 새 사이트를 hosts 파일에도 추가해야 합니다. macOS/Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`입니다:

    192.168.56.56  homestead.test
    192.168.56.56  another.test

사이트를 추가한 후 Homestead 디렉터리에서 `vagrant reload --provision` 명령어를 실행하세요.

<a name="site-types"></a>
#### 사이트 타입

Homestead는 Laravel이 아닌 다양한 프레임워크 기반의 프로젝트도 쉽게 실행할 수 있도록 여러 가지 "사이트 타입"을 지원합니다. 예를 들어, `statamic` 사이트 타입으로 Statamic 애플리케이션을 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원하는 사이트 타입: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 등이 있습니다.

<a name="site-parameters"></a>
#### 사이트 매개변수

사이트별로 Nginx `fastcgi_param` 값을 추가하려면 `params` 디렉티브를 사용합니다:

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

글로벌 환경 변수는 `Homestead.yaml` 파일에 추가해 정의할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 파일 수정 후, 반드시 `vagrant reload --provision` 명령어로 가상머신을 재Provision해야 모든 PHP 버전의 PHP-FPM 설정과 `vagrant` 사용자 환경이 갱신됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경에 포워딩됩니다:

- **HTTP:** 8000 &rarr; 80
- **HTTPS:** 44300 &rarr; 443

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

필요하다면 `Homestead.yaml` 파일에 `ports` 항목을 추가하여 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. 파일 수정 후 `vagrant reload --provision` 명령어로 반영하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

추가로 매핑할 수 있는 Homestead 서비스 기본 포트 목록은 다음과 같습니다:

- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailpit:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

<a name="php-versions"></a>
### PHP 버전

Homestead는 하나의 가상머신에서 여러 PHP 버전을 실행할 수 있습니다. 사이트별로 `Homestead.yaml` 파일에서 사용할 PHP 버전을 지정할 수 있습니다. 사용 가능한 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상머신 내부](#connecting-via-ssh)에서 아래와 같이 CLI로 특정 PHP 버전을 사용할 수 있습니다:

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

CLI 기본 PHP 버전도 아래 명령어로 변경할 수 있습니다(Homestead VM 내부):

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

MySQL과 PostgreSQL에 대해 `homestead` 데이터베이스가 기본으로 생성됩니다. 호스트의 DB 클라이언트에서 각각 `127.0.0.1:33060`(MySQL), `127.0.0.1:54320`(PostgreSQL)으로 접속하세요. 사용자명과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]  
> 호스트 컴퓨터에서 접속할 때만 이 비표준 포트를 사용하세요. Laravel 애플리케이션 내 DB 설정에서는(가상머신 내부에서는) 기본 포트 3306, 5432를 사용해야 합니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead 가상머신이 제거될 때 데이터베이스를 자동 백업할 수 있습니다. 이를 위해 Vagrant 2.1.0 이상을 사용하거나, 구버전일 경우 `vagrant-triggers` 플러그인 설치가 필요합니다. 자동 백업 기능은 `Homestead.yaml`에 아래와 같이 추가하세요:

    backup: true

설정 후, `vagrant destroy` 실행 시 각 DB가 `.backup/mysql_backup`, `.backup/postgres_backup` 디렉터리에 익스포트됩니다. 이 디렉토리는 Homestead 디렉터리 또는 [프로젝트별 설치](#per-project-installation) 시 프로젝트 루트에 위치합니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 [크론 작업 예약](/docs/{{version}}/scheduling)을 위한 편리한 방법으로, 매 분마다 한 번씩 `schedule:run` Artisan 명령을 예약하도록 제공합니다. 이 명령은 `routes/console.php`에 정의된 스케줄을 기준으로 작업 실행 여부를 검사합니다.

특정 Homestead 사이트에 대해 `schedule:run`이 실행되도록 하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 설정합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트에 대한 크론 작업은 Homestead VM의 `/etc/cron.d` 디렉터리에 생성됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)은 모든 송신 이메일을 실제로 발송하지 않고 가로채 확인할 수 있게 해줍니다. 사용하려면 애플리케이션의 `.env` 파일을 다음과 같이 설정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

설정 후 `http://localhost:8025`에서 Mailpit 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 오브젝트 스토리지 서버입니다. 설치하려면 [옵션 기능 설치](#installing-optional-features)에서 아래와 같이 설정하세요:

    minio: true

기본적으로 Minio는 9600포트에서 실행됩니다. 관리 패널은 `http://localhost:9600`에서 접근할 수 있으며, 기본 액세스 키는 `homestead`, 기본 시크릿 키는 `secretkey`입니다. 접속 시 region은 `us-east-1`을 사용해야 합니다.

사용을 위해 `.env` 파일에 아래와 같이 설정하세요:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio 기반 "S3" 버킷을 사용하려면 `Homestead.yaml`에 `buckets` 항목을 추가하세요. 버킷 정의 후 `vagrant reload --provision` 명령을 실행해야 합니다:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원하는 `policy` 값: `none`, `download`, `upload`, `public`.

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 테스트를 Homestead에서 실행하려면 [`webdriver` 옵션 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

기능 활성화 후, 터미널에서 `vagrant reload --provision` 명령어를 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유

때때로 동료나 클라이언트와 작업 중인 개발 환경을 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령어로 이 기능을 제공하지만, Homestead에서 여러 사이트를 구성한 경우에는 동작하지 않습니다.

이 문제를 해결하기 위해 Homestead만의 `share` 명령어가 제공됩니다. 먼저 [Homestead 가상머신에 SSH로 접속](#connecting-via-ssh) 후, `share homestead.test` 명령을 실행하세요. 이 명령어는 `Homestead.yaml`에 설정된 `homestead.test` 사이트를 외부에 공개합니다. 다른 사이트로 대체할 수도 있습니다:

```shell
share homestead.test
```

명령 실행 시 ngrok 화면이 나타나며, 공개된 URL 및 로그 등이 표시됩니다. 지역(region), 서브도메인 등 ngrok 실행 옵션을 추가할 수도 있습니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS로 공유하려면 `share` 대신 `sshare` 명령을 쓰세요.

> [!WARNING]  
> Vagrant는 본질적으로 보안이 취약하므로 `share` 명령을 실행하면 가상머신이 인터넷에 노출됩니다. 신중히 사용하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 통한 단계별 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지에 접근하면 PHP가 IDE와 연동되어 코드 실행을 확인하고 수정할 수 있습니다.

기본적으로 Xdebug는 항상 실행 중이며, 연결을 받을 준비가 되어 있습니다. CLI에서 Xdebug 활성화가 필요하다면 Homestead VM 내에서 `sudo phpenmod xdebug`를 실행하세요. IDE 설명서를 참조해 디버깅을 활성화하고, 브라우저에서는 Xdebug 트리거를 위한 확장 프로그램 또는 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)을 사용하세요.

> [!WARNING]  
> Xdebug 활성화 시 PHP 실행 속도가 느려집니다. 비활성화하려면 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버에 요청하는 기능 테스트를 디버깅할 때는, 헤더나 쿠키를 직접 수정하기보다 디버깅을 자동 시작하도록 하는 게 편리합니다. 이를 위해 Homestead VM의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정해 다음 설정을 추가하면 됩니다:

```ini
; Homestead.yaml에 지정한 IP 대역이 다르면 이 값도 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면, Homestead VM 내에서 `xphp` 쉘 별칭을 사용하세요:

    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션의 프로파일링 서비스입니다. 호출 그래프와 타임라인 형태의 인터랙티브 프로파일 정보를 제공합니다. 개발, 스테이징, 프로덕션 환경에서 사용할 수 있으며, 최종 사용자에겐 오버헤드가 없습니다. 또한 Blackfire는 코드 및 `php.ini` 설정에 대한 성능, 품질, 보안 검사도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 연동하여 프로파일링 시나리오를 스크립트로 작성할 수 있는 오픈소스 크롤링, 테스트, 스크래핑 도구입니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 항목을 사용하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 다양한 애플리케이션 프로파일링 방법이 제공되며, [공식 문서](https://blackfire.io/docs/php/integrations/laravel/index)에서 자세히 확인할 수 있습니다.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml`의 `networks` 항목은 Homestead VM의 네트워크 인터페이스를 설정합니다. 필요한 만큼 여러 개를 설정할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브릿지(bridged)](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면, `bridge` 설정을 추가하고 네트워크 타입을 `public_network`로 변경하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 사용하려면 `ip` 옵션을 제거하면 됩니다:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크에서 사용할 디바이스를 변경하려면, `dev` 옵션을 추가합니다(기본값: `eth0`):

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead 디렉터리 루트의 `after.sh` 스크립트로 Homestead 환경을 확장할 수 있습니다. 이 파일에 가상머신을 구성·커스터마이즈하는 셸 명령어를 자유롭게 추가하세요.

특정 패키지 설치 시 Ubuntu가 기존 설정 파일을 유지할지 묻는 경우가 있는데, 아래처럼 설치하면 Homestead가 작성해둔 기존 설정이 덮어써지지 않아 안전합니다:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 맞춤 설정

팀과 함께 Homestead를 사용할 때, 개인 스타일에 맞게 더 세밀하게 조정하고 싶은 경우 `Homestead.yaml`이 있는 Homestead 폴더의 루트에 `user-customizations.sh` 파일을 생성하면 됩니다. 이 파일에는 원하는 어떤 커스터마이즈든 자유롭게 할 수 있습니다. 단, 이 파일은 버전 관리에 포함시키지 마세요.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 합니다. 이를 통해 호스트 OS의 DNS 설정을 사용할 수 있습니다. 이 동작을 수정하려면, `Homestead.yaml` 파일에 다음과 같이 옵션을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```