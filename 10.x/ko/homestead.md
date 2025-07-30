# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 구성하기](#configuring-homestead)
    - [Nginx 사이트 구성하기](#configuring-nginx-sites)
    - [서비스 구성하기](#configuring-services)
    - [Vagrant 박스 시작하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치하기](#installing-optional-features)
    - [별칭](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용법](#daily-usage)
    - [SSH 연결](#connecting-via-ssh)
    - [추가 사이트 추가하기](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 구성하기](#configuring-cron-schedules)
    - [Mailpit 구성하기](#configuring-mailpit)
    - [Minio 구성하기](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅하기](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 PHP 개발 경험 전반, 특히 로컬 개발 환경까지 쾌적하게 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공하는 사전 패키지된 Vagrant 박스로, 로컬 컴퓨터에 PHP, 웹 서버 또는 기타 서버 소프트웨어를 따로 설치하지 않고도 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 설정하는 쉽고 우아한 방법을 제공합니다. Vagrant 박스는 완전히 재설치 가능한 형태로, 문제가 발생하면 몇 분 안에 박스를 삭제하고 다시 생성할 수 있습니다!

Homestead는 Windows, macOS, Linux에서 모두 실행 가능하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, 그리고 멋진 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!WARNING]  
> Windows 사용자는 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 일반적으로 BIOS 설정에서 활성화할 수 있습니다. 만약 UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x 접근을 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어 (Included Software)

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
### 선택적 소프트웨어 (Optional Software)

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
- Webdriver & Laravel Dusk Utility

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정 (Installation and Setup)

<a name="first-steps"></a>
### 첫 단계 (First Steps)

Homestead 환경을 시작하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 아래 지원하는 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

모든 소프트웨어 패키지는 주요 운영체제에 맞는 사용자 친화적인 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치하기 (Installing Homestead)

호스트 머신에 Homestead 저장소를 클론해서 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션을 호스트하게 될 것이므로 홈 디렉토리 내에 `Homestead` 폴더로 클론하는 것을 권장합니다. 본 문서에서는 이 디렉토리를 "Homestead 디렉토리"라 지칭합니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

클론 후 `release` 브랜치로 체크아웃하세요. 이 브랜치에는 항상 최신 안정 버전이 포함되어 있습니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. 이 파일에 Homestead 설치에 필요한 모든 설정을 구성할 수 있으며, Homestead 디렉토리에 위치하게 됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 구성하기 (Configuring Homestead)

<a name="setting-your-provider"></a>
#### 프로바이더 설정하기 (Setting Your Provider)

`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 프로바이더를 지정합니다: `virtualbox` 또는 `parallels`:

```
provider: virtualbox
```

> [!WARNING]  
> Apple Silicon 사용자는 Parallels 프로바이더를 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 구성하기 (Configuring Shared Folders)

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더들을 나열합니다. 해당 폴더 내 파일이 변경되면 로컬 머신과 Homestead 가상 환경 간에 자동으로 동기화됩니다. 필요한 만큼 공유 폴더를 구성할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]  
> Windows 사용자는 `~/` 경로 문법 대신 프로젝트의 절대 경로(예: `C:\Users\user\Code\project1`)를 사용해야 합니다.

각 애플리케이션마다 별도의 폴더 매핑을 해주는 것이 좋습니다. 하나의 큰 디렉토리로 모든 애플리케이션을 매핑할 경우, 가상 머신이 해당 폴더 내 모든 파일의 디스크 입출력 상태를 추적해야 되어 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]  
> Homestead 이용 시 현재 디렉토리인 `.`를 마운트하지 마십시오. 이러면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않아 선택적 기능에 문제가 생기고 프로비저닝 중 예상치 못한 오류가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 활성화하려면 `type` 옵션을 폴더 매핑에 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]  
> Windows에서 NFS 사용 시 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려하세요. 이 플러그인은 Homestead 가상 머신 내 파일과 디렉토리의 올바른 사용자/그룹 권한을 유지합니다.

Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) 문서에 나와 있는 옵션들을 `options` 키 아래에 지정할 수도 있습니다:

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
### Nginx 사이트 구성하기 (Configuring Nginx Sites)

Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 속성을 통해 Homestead 환경 내 폴더에 "도메인"을 쉽게 매핑할 수 있습니다. `Homestead.yaml` 파일에 예시 사이트 구성이 기본으로 포함되어 있습니다. 여러 사이트를 추가하여 여러 Laravel 애플리케이션을 가상 환경에서 편리하게 구동할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

`sites` 속성을 변경한 후에는 Homestead 가상 머신에서 Nginx 구성을 적용하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!WARNING]  
> Homestead 스크립트는 가능한 한 멱등성을 유지하도록 설계되었습니다. 하지만 프로비저닝 중 문제가 발생한다면 `vagrant destroy && vagrant up` 명령으로 가상 머신을 파괴 후 다시 생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
#### 호스트명 해석 (Hostname Resolution)

Homestead는 `mDNS`를 이용해 자동으로 호스트 이름을 해석합니다. `Homestead.yaml`에 `hostname: homestead`로 설정하면 호스트명이 `homestead.local`이 됩니다. macOS, iOS, 그리고 Linux 데스크톱은 기본적으로 `mDNS`를 지원합니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명 기능은 [프로젝트별 설치](#per-project-installation) 시 가장 잘 작동합니다. 하나의 Homestead 인스턴스에서 여러 사이트를 운영한다면, 각 웹 사이트 도메인을 호스트 머신의 `hosts` 파일에 직접 추가하세요. `hosts` 파일은 macOS와 Linux에서 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다. 추가 예시는 다음과 같습니다:

```
192.168.56.56  homestead.test
```

`Homestead.yaml`에 설정한 IP 주소와 일치하는지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 시작하면 웹 브라우저에서 다음과 같이 사이트에 접속할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 구성하기 (Configuring Services)

Homestead는 기본적으로 여러 서비스를 시작하지만, 프로비저닝 시 활성화하거나 비활성화할 서비스를 직접 설정할 수 있습니다. 예를 들어 PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml` 파일 내 `services` 옵션을 다음과 같이 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

명시된 서비스는 `enabled`와 `disabled` 순서에 따라 시작하거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 시작하기 (Launching the Vagrant Box)

`Homestead.yaml` 파일 수정을 마쳤다면 Homestead 디렉토리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더 및 Nginx 사이트를 자동으로 설정합니다.

가상 머신을 삭제하려면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치 (Per Project Installation)

Homestead를 전역(global)으로 설치해 여러 프로젝트에서 같은 가상 머신을 공유하는 대신, 각 프로젝트별로 Homestead 인스턴스를 구성할 수 있습니다. 프로젝트에 `Vagrantfile`을 포함시키면, 다른 개발자가 저장소를 클론한 후 즉시 `vagrant up`으로 환경을 실행할 수 있어 유용합니다.

Composer 패키지 관리자를 사용해 프로젝트에 Homestead를 설치하려면 다음 명령을 실행하세요:

```shell
composer require laravel/homestead --dev
```

설치 후 Homestead의 `make` 명령을 호출해 `Vagrantfile`과 `Homestead.yaml` 파일을 자동 생성합니다. 이들 파일은 프로젝트 루트에 생성되며, `make` 명령은 `Homestead.yaml`에서 `sites`와 `folders` 지시문을 자동으로 구성합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

이후 터미널에서 `vagrant up` 명령을 실행하고 브라우저에서 `http://homestead.test` 주소로 프로젝트에 접속하세요. 자동 [호스트명 해석](#hostname-resolution)을 사용하지 않는다면 `hosts` 파일에 `homestead.test` 또는 원하는 도메인을 추가해야 함을 잊지 마십시오.

<a name="installing-optional-features"></a>
### 선택적 기능 설치하기 (Installing Optional Features)

선택적 소프트웨어는 `Homestead.yaml` 파일 내 `features` 설정을 통해 설치할 수 있습니다. 대부분의 기능은 불리언 값으로 활성화 또는 비활성화 가능하며, 일부는 추가 구성 옵션을 가집니다:

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

Elasticsearch는 정확한 버전 번호(major.minor.patch)를 지정하여 설치할 수 있습니다. 기본 설치는 'homestead'라는 클러스터를 생성합니다. 운영 체제 메모리의 절반 이상을 할당하지 않도록 주의하며, Homestead 머신에 Elasticsearch 메모리 할당량 2배 이상을 확보해야 합니다.

> [!NOTE]  
> 구성을 변경하는 방법은 [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB 기능을 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL의 드롭인 대체 기능을 하므로, 여전히 Laravel 데이터베이스 설정의 `mysql` 드라이버를 사용하세요.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치는 사용자명 `homestead`와 비밀번호 `secret`으로 데이터베이스를 설정합니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j 설치 시도 사용자 `homestead`와 비밀번호 `secret`을 기본으로 설정합니다. Neo4j 브라우저는 웹 브라우저에서 `http://homestead.test:7474` 로 접근할 수 있습니다. `7687` (Bolt), `7474` (HTTP), `7473` (HTTPS) 포트가 Neo4j 클라이언트 요청을 처리합니다.

<a name="aliases"></a>
### 별칭 (Aliases)

Homestead 가상 머신 내 Bash 별칭은 Homestead 디렉토리 안의 `aliases` 파일을 수정해 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일 변경 후에는 `vagrant reload --provision` 명령어를 실행해 변경 사항이 적용되도록 가상 머신을 재프로비저닝해야 합니다.

<a name="updating-homestead"></a>
## Homestead 업데이트 (Updating Homestead)

업데이트를 시작하기 전에 현재 가상 머신을 제거해야 합니다. Homestead 디렉토리에서 다음 명령을 실행하세요:

```shell
vagrant destroy
```

그다음 Homestead 소스 코드를 업데이트합니다. 저장소를 클론한 경우 클론한 위치에서 다음 명령을 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령어들은 GitHub 저장소에서 최신 Homestead 코드를 가져오고 태그를 최신 상태로 만든 다음 최신 안정 버전으로 체크아웃합니다. 최신 안정 버전은 Homestead의 [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json` 파일로 설치한 경우 `composer.json`에서 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 다음으로 의존성 업데이트를 수행하세요:

```shell
composer update
```

다음으로 Vagrant 박스를 업데이트합니다:

```shell
vagrant box update
```

업데이트 후 Homestead 추가 설정 파일을 최신화하기 위해 Homestead 디렉토리에서 `bash init.sh` 명령을 실행하세요. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 묻는 메시지가 표시됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 최신 Vagrant 박스를 활용하기 위해 Homestead 가상 머신을 다시 생성합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용법 (Daily Usage)

<a name="connecting-via-ssh"></a>
### SSH 연결 (Connecting via SSH)

Homestead 디렉토리에서 `vagrant ssh` 명령을 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가하기 (Adding Additional Sites)

Homestead 환경이 프로비저닝되고 가동 중이라면, 다른 Laravel 프로젝트를 위한 Nginx 사이트를 추가하고 싶을 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트는 `Homestead.yaml` 파일에 다음과 같이 추가합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]  
> 사이트를 추가하기 전 프로젝트 디렉토리의 [폴더 매핑](#configuring-shared-folders)을 반드시 설정했는지 확인하세요.

Vagrant가 "hosts" 파일을 자동으로 관리하지 않는다면, 새 사이트를 여기에도 추가해야 합니다. macOS와 Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts` 파일에 위치합니다:

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 후 Homestead 디렉토리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형 (Site Types)

Homestead는 Laravel 기반이 아닌 프로젝트를 쉽게 구동할 수 있도록 다양한 사이트 유형을 지원합니다. 예를 들어, `statamic` 타입의 Statamic 애플리케이션을 쉽게 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원되는 사이트 유형은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`입니다.

<a name="site-parameters"></a>
#### 사이트 매개변수 (Site Parameters)

추가 `fastcgi_param` 값을 Nginx 사이트에 더할 수 있습니다. `params` 지시어를 사용하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수 (Environment Variables)

글로벌 환경 변수는 `Homestead.yaml`에 다음과 같이 정의할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 변경 후 `vagrant reload --provision` 명령을 실행해 모든 PHP 버전의 PHP-FPM 설정과 `vagrant` 사용자의 환경 변수를 업데이트해야 합니다.

<a name="ports"></a>
### 포트 (Ports)

기본적으로 다음 포트들이 Homestead 환경으로 전달됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; 80 포트로 전달
- **HTTPS:** 44300 &rarr; 443 포트로 전달

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 전달 (Forwarding Additional Ports)

추가 포트를 포워딩하려면 `Homestead.yaml` 내 `ports` 설정에 다음과 같이 작성합니다. 변경 후 `vagrant reload --provision`로 프로비저닝을 다시 해야 합니다:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

아래는 추가로 호스트 머신에서 Vagrant 박스로 포트 매핑을 할 수 있는 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; 22 포트
- **ngrok UI:** 4040 &rarr; 4040 포트
- **MySQL:** 33060 &rarr; 3306 포트
- **PostgreSQL:** 54320 &rarr; 5432 포트
- **MongoDB:** 27017 &rarr; 27017 포트
- **Mailpit:** 8025 &rarr; 8025 포트
- **Minio:** 9600 &rarr; 9600 포트

</div>

<a name="php-versions"></a>
### PHP 버전 (PHP Versions)

Homestead는 동일 가상 머신 내에서 여러 PHP 버전을 실행할 수 있습니다. 특정 사이트에 사용할 PHP 버전은 `Homestead.yaml` 설정에서 지정할 수 있으며, 지원하는 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값)입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내부](#connecting-via-ssh)에서도 CLI로 아래 명령어들을 통해 PHP 버전을 전환하며 사용할 수 있습니다:

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

CLI 기본 PHP 버전 변경은 가상 머신 내에서 아래 명령어를 사용하면 됩니다:

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
### 데이터베이스 연결 (Connecting to Databases)

MySQL과 PostgreSQL 용으로 기본 `homestead` 데이터베이스가 제공됩니다. 호스트 머신에서 MySQL 또는 PostgreSQL 클라이언트로 접속하려면 각각 포트 `33060`(MySQL), `54320`(PostgreSQL)을 사용해 `127.0.0.1`에 연결하세요. 사용자명과 비밀번호는 둘 다 `homestead` / `secret`입니다.

> [!WARNING]  
> 호스트 머신에서 데이터베이스에 접속할 때만 위와 같은 비표준 포트를 사용하세요. Laravel 애플리케이션 내의 `database` 설정 파일에서는 가상 머신 내부에서 실행되므로 기본 포트인 3306, 5432를 사용해야 합니다.

<a name="database-backups"></a>
### 데이터베이스 백업 (Database Backups)

Homestead는 가상 머신을 삭제할 때 자동으로 데이터베이스를 백업할 수 있습니다. 이를 위해서는 Vagrant 2.1.0 이상을 사용하거나, 구버전이라면 `vagrant-triggers` 플러그인을 반드시 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 다음을 추가하세요:

```
backup: true
```

이 설정 후 `vagrant destroy` 명령을 실행할 때 데이터베이스가 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉토리에 내보내집니다. 해당 디렉토리는 Homestead 설치 폴더 또는 [프로젝트별 설치](#per-project-installation) 시 프로젝트 루트에 위치합니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 구성하기 (Configuring Cron Schedules)

Laravel은 단일 `schedule:run` Artisan 명령을 매분 실행시키는 방법으로 [크론 작업 스케줄링](/docs/10.x/scheduling)을 간편하게 지원합니다. `schedule:run` 명령은 `App\Console\Kernel` 클래스에 정의된 작업 스케줄을 참조해 해당 작업을 수행합니다.

Homestead 사이트에서 `schedule:run` 명령을 실행하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상 머신 `/etc/cron.d` 디렉토리에 등록됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 구성하기 (Configuring Mailpit)

[Mailpit](https://github.com/axllent/mailpit)은 발신 이메일을 가로채 실제 수신자에게 보내지 않고도 메일 내용을 확인할 수 있게 합니다. 시작하려면 앱의 `.env` 파일을 아래와 같이 설정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit 구성 후에는 `http://localhost:8025`에서 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 구성하기 (Configuring Minio)

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 오브젝트 스토리지 서버입니다. Minio를 설치하려면 `Homestead.yaml`의 [선택적 기능](#installing-optional-features) 부분에 다음을 추가하세요:

```
minio: true
```

기본적으로 Minio는 9600 포트에서 사용 가능하며, `http://localhost:9600`에서 제어판에 접근할 수 있습니다. 기본 액세스 키는 `homestead`, 비밀 키는 `secretkey`입니다. Minio 접속 시 항상 리전(region)은 `us-east-1`을 사용하세요.

Minio를 사용하려면 애플리케이션 `config/filesystems.php` 설정에서 S3 디스크 구성을 다음처럼 조정해야 합니다. `use_path_style_endpoint` 옵션을 추가하고, `url` 키를 `endpoint`로 변경해야 합니다:

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

마지막으로 `.env` 파일에 아래 설정이 포함되어 있어야 합니다:

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio가 구동하는 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시어를 추가하고 난 뒤 `vagrant reload --provision`을 실행합니다:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원되는 `policy` 값은 `none`, `download`, `upload`, `public`입니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/10.x/dusk) 테스트를 Homestead 내에서 실행하려면 `webdriver` 기능을 Homestead 설정에서 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

`webdriver` 기능 활성화 후 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

<a name="sharing-your-environment"></a>
### 환경 공유하기 (Sharing Your Environment)

동료나 클라이언트와 현재 작업 중인 환경을 공유하고 싶을 때가 있습니다. Vagrant는 기본적으로 `vagrant share` 명령어를 지원하지만, 여러 사이트가 있는 경우 작동하지 않습니다.

이 문제를 해결하기 위해 Homestead 자체 `share` 명령을 제공합니다. 먼저 [Homestead 가상 머신에 SSH 접속](#connecting-via-ssh)한 후 `share homestead.test` 명령을 실행하세요. 이 명령은 `Homestead.yaml` 설정 내 `homestead.test` 사이트를 공유합니다. 다른 사이트명으로도 대체 가능합니다:

```shell
share homestead.test
```

명령 실행 후 Ngrok 화면이 나타나며 활동 로그와 공유 URL을 보여줍니다. 커스텀 지역(region), 서브도메인(subdomain) 등 Ngrok 실행 옵션을 지정하려면 다음처럼 명령어에 추가하면 됩니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS로 공유하려면 `share` 대신 `sshare` 명령어를 사용하세요.

> [!WARNING]  
> Vagrant는 본질적으로 보안에 취약하므로, `share` 명령 실행 시 가상 머신이 인터넷에 노출된다는 점을 반드시 인지해야 합니다.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링 (Debugging and Profiling)

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅하기 (Debugging Web Requests With Xdebug)

Homestead는 [Xdebug](https://xdebug.org)를 통한 스텝 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지를 열면 PHP가 IDE에 연결되어 실행 중인 코드를 검사 및 수정할 수 있습니다.

기본적으로 Xdebug는 이미 동작 중이며 연결을 기다리고 있습니다. CLI에서 Xdebug를 활성화하려면 Homestead 가상 머신 내에서 `sudo phpenmod xdebug` 명령을 실행하세요. 이후 IDE 지침에 따라 디버깅을 설정하고, 브라우저에 확장 프로그램이나 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)을 설치해 Xdebug 트리거를 구성합니다.

> [!WARNING]  
> Xdebug는 PHP 실행 속도를 크게 낮춥니다. 비활성화하려면 가상 머신 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작 설정하기 (Autostarting Xdebug)

웹 서버에 요청을 보내는 기능 테스트를 디버깅할 때, 요청에 커스텀 헤더나 쿠키 설정 없이 Xdebug를 자동으로 시작하는 편이 편리합니다. 이를 위해 Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 열어 다음 내용을 추가 또는 수정하세요:

```ini
; Homestead.yaml에 다른 서브넷이 설정된 경우 IP 주소가 달라질 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅 (Debugging CLI Applications)

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신에서 `xphp` 셸 별칭을 사용하세요:

```
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링 (Profiling Applications With Blackfire)

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션의 프로파일링 서비스입니다. 호출 그래프(call-graph)와 타임라인을 인터랙티브 UI에서 보여주며, 개발, 스테이징, 프로덕션 환경 모두에서 사용 가능하면서 최종 사용자에 부담이 없습니다. 또한 코드 및 `php.ini` 설정에 대한 성능, 품질, 보안 점검도 지원합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈 소스 웹 크롤링, 웹 테스트, 웹 스크래핑 도구로 Blackfire와 연동해 프로파일링 시나리오를 스크립트로 작성할 수 있습니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 `features` 섹션에 다음을 추가합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

서버와 클라이언트 자격 증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 다양한 프로파일링 옵션을 제공하며, 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스 (Network Interfaces)

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요에 따라 여러 인터페이스를 자유롭게 구성할 수 있습니다:

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

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 `ip` 옵션을 제거하면 됩니다:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크에 지정한 장치를 변경하려면 `dev` 옵션을 추가하세요. 기본값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장하기 (Extending Homestead)

Homestead 디렉토리 루트에 `after.sh` 스크립트를 만들어 가상 머신을 사용자 맞춤 설정할 수 있습니다. 이 파일에 필요한 셸 명령어를 추가하세요.

패키지 설치 중 Ubuntu가 기존 설정을 유지할지 덮어쓸지 물어보면, 다음 명령어 구문을 사용하여 기존 Homestead 설정을 덮어쓰지 않도록 하세요:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 맞춤 설정 (User Customizations)

팀 내에서 Homestead를 사용할 때, 개인 개발 스타일에 맞게 조정하고 싶다면 Homestead 디렉토리 루트에 `user-customizations.sh` 파일을 만들어 관리할 수 있습니다. 원하는 설정을 모두 작성할 수 있으나, 이 파일은 버전 관리에 포함시키지 않아야 합니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정 (Provider Specific Settings)

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성하여 호스트 운영체제의 DNS 설정을 사용합니다. 이 동작을 변경하려면 `Homestead.yaml`에 다음 옵션을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```