# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭 설정](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상 사용법](#daily-usage)
    - [SSH 접속](#connecting-via-ssh)
    - [추가 사이트 등록](#adding-additional-sites)
    - [환경 변수 설정](#environment-variables)
    - [포트 설정](#ports)
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
    - [Blackfire로 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [프로바이더 별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 로컬 개발 환경을 포함하여 전체 PHP 개발 경험을 쾌적하게 만드는 데 힘쓰고 있습니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공하는 사전 패키지된 Vagrant 박스로, 로컬 머신에 PHP, 웹 서버 또는 기타 서버 소프트웨어를 직접 설치하지 않고도 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝하는 간단하면서도 우아한 방법을 제공합니다. Vagrant 박스는 완전히 폐기 가능해서 문제가 발생하면 몇 분 내에 박스를 파괴하고 다시 생성할 수 있습니다!

Homestead는 Windows, macOS, Linux 어떤 시스템에서도 실행 가능하며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어가 포함되어 있습니다.

> [!WARNING]  
> Windows를 사용하는 경우, 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 일반적으로 BIOS에서 설정할 수 있습니다. UEFI 시스템 위에서 Hyper-V를 사용 중이라면 VT-x 접속을 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

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
- Webdriver & Laravel Dusk 유틸리티

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정 (Installation and Setup)

<a name="first-steps"></a>
### 첫 단계 (First Steps)

Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)를 설치하고 다음 지원되는 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어들은 모두 인기 운영체제용으로 사용하기 쉬운 그래픽 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치 (Installing Homestead)

호스트 머신에 Homestead 저장소를 클론하여 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션을 호스팅하기 때문에, 보통 홈 디렉토리 아래 `Homestead` 폴더에 클론하는 것을 권장합니다. 이 문서에서는 이를 "Homestead 디렉토리"라 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

클론한 뒤에는 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치는 항상 Homestead의 최신 안정 버전을 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

그 다음, Homestead 디렉토리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 설정 파일을 생성하세요. 이 파일에서 Homestead 설치에 필요한 모든 설정을 구성합니다. 파일은 Homestead 디렉토리에 생성됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정 (Configuring Homestead)

<a name="setting-your-provider"></a>
#### 프로바이더 설정 (Setting Your Provider)

`Homestead.yaml` 파일의 `provider` 키는 사용하고자 하는 Vagrant 프로바이더를 지정합니다: `virtualbox` 또는 `parallels` 중 선택합니다.

```
provider: virtualbox
```

> [!WARNING]  
> Apple Silicon 사용자는 반드시 Parallels 프로바이더를 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정 (Configuring Shared Folders)

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더 목록입니다. 이 폴더 내의 파일 변경 사항은 로컬 머신과 Homestead 가상 환경 간에 자동 동기화됩니다. 필요한 만큼 여러 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]  
> Windows 사용자는 `~/` 구문 대신 프로젝트의 전체 경로(`C:\Users\user\Code\project1` 같은)를 사용해야 합니다.

각 애플리케이션 폴더마다 개별적으로 맵핑하는 것이 좋습니다. 하나의 큰 디렉토리를 모두 맵핑하면, 가상 머신이 폴더 내 모든 파일의 디스크 IO를 추적해야 해서 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]  
> Homestead 사용 시 현재 디렉토리(`.`)를 마운트하지 마세요. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않아 일부 선택적 기능에 문제가 발생하고 프로비저닝 결과가 예기치 않게 됩니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 폴더 맵핑에 `type` 옵션을 추가합니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]  
> Windows에서 NFS를 쓸 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려하세요. 이 플러그인은 Homestead 가상 머신 내 파일과 디렉토리 권한을 올바르게 유지합니다.

Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) 옵션을 `options` 키 아래에 추가할 수도 있습니다:

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
### Nginx 사이트 설정 (Configuring Nginx Sites)

Nginx를 잘 모른다고 해도 걱정하지 마세요. `Homestead.yaml` 파일의 `sites` 속성은 Homestead 환경에서 실제 폴더에 도메인을 쉽게 매핑할 수 있도록 합니다. 기본 `Homestead.yaml`에 샘플 설정이 포함되어 있습니다. 필요한 만큼 여러 사이트를 추가할 수 있으며, Homestead는 작업 중인 모든 Laravel 애플리케이션을 위한 편리한 가상 환경입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

사이트 설정을 변경한 후에는 Homestead 가상 머신에서 Nginx 설정을 갱신하기 위해 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

> [!WARNING]  
> Homestead 스크립트는 가능한 한 멱등성을 갖추도록 설계되었습니다. 하지만 프로비저닝에 문제가 발생하면 `vagrant destroy && vagrant up` 명령어를 실행해 가상 머신을 완전히 새로 만드세요.

<a name="hostname-resolution"></a>
#### 호스트명 해석 (Hostname Resolution)

Homestead는 `mDNS`를 이용해 자동 호스트명 해석을 제공합니다. `Homestead.yaml`에 `hostname: homestead`를 설정하면 호스트가 `homestead.local` 도메인으로 접속됩니다. macOS, iOS, Linux 데스크탑은 기본적으로 `mDNS`를 지원합니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명 해석은 [프로젝트별 설치](#per-project-installation)에 가장 적합합니다. 단일 Homestead 인스턴스에서 여러 사이트를 호스팅한다면, 각 도메인을 로컬 머신의 `hosts` 파일에 추가하여 요청을 Homestead 가상 머신으로 전환할 수 있습니다. macOS, Linux에서는 `/etc/hosts`에 위치하며, Windows는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다. 예시는 다음과 같습니다:

```
192.168.56.56  homestead.test
```

`Homestead.yaml`에 설정한 IP 주소가 맞는지 반드시 확인하세요. 도메인을 `hosts`에 추가하고 Vagrant 박스를 실행하면 웹 브라우저에서 다음과 같이 사이트에 접속할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정 (Configuring Services)

Homestead는 기본적으로 여러 서비스를 시작하지만, `Homestead.yaml` 파일 내 `services` 옵션을 수정하여 프로비저닝 시 활성화하거나 비활성화할 서비스를 선택할 수 있습니다. 예를 들어 PostgreSQL은 활성화하고 MySQL은 비활성화하려면 다음과 같이 설정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

`enabled`와 `disabled` 지시어의 순서에 따라 서비스가 시작 혹은 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행 (Launching the Vagrant Box)

`Homestead.yaml` 설정을 마쳤으면 Homestead 디렉토리에서 `vagrant up` 명령어를 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더 및 Nginx 사이트를 자동으로 설정합니다.

가상 머신을 제거하려면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치 (Per Project Installation)

Homestead를 전역에 설치하고 모든 프로젝트에 동일한 가상 머신을 공유하는 대신, 각 프로젝트마다 Homestead 인스턴스를 따로 구성할 수도 있습니다. 이렇게 하면 프로젝트에 `Vagrantfile`을 포함시켜 다른 작업자들이 저장소를 클론한 후 즉시 `vagrant up`을 실행할 수 있어 편리합니다.

Composer 패키지 관리자를 통해 프로젝트에 Homestead를 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```

설치가 끝나면 Homestead의 `make` 커맨드를 호출해 프로젝트 루트에 `Vagrantfile`과 `Homestead.yaml`을 생성하세요. `make` 명령은 `Homestead.yaml` 내 `sites`와 `folders` 지시어도 자동으로 구성합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 다음 터미널에서 `vagrant up`을 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 호스트명 해석을 사용하지 않는다면 `/etc/hosts` 파일에 `homestead.test` 또는 원하는 도메인 항목을 직접 추가해야 합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치 (Installing Optional Features)

선택적 소프트웨어는 `Homestead.yaml` 파일 내 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불리언 값으로 사용 여부를 지정하고, 일부 기능은 여러 설정 옵션을 지원합니다:

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

Elasticsearch의 구체적인 버전을 지정할 수 있으며, 형식은 `major.minor.patch` 형태의 정확한 버전 번호여야 합니다. 기본 설치는 'homestead'라는 클러스터를 생성합니다. Elasticsearch에 OS 메모리의 절반 이상을 할당하지 않도록 주의하고, 가상 머신 메모리는 해당 용량의 최소 두 배 이상이어야 합니다.

> [!NOTE]  
> [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고해 구성 방법을 확인하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL은 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL과 완벽 호환되므로, 애플리케이션의 데이터베이스 설정에서는 여전히 `mysql` 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치 시 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치 시 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`입니다. Neo4j 브라우저는 `http://homestead.test:7474`에서 접근 가능합니다. `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS) 포트가 Neo4j 클라이언트 요청을 처리합니다.

<a name="aliases"></a>
### 별칭 설정 (Aliases)

Homestead 가상 머신 내 Bash 별칭은 Homestead 디렉토리 내 `aliases` 파일을 수정하여 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일을 수정한 후에는 `vagrant reload --provision` 명령어로 가상 머신을 다시 프로비저닝하여 별칭이 적용되도록 해야 합니다.

<a name="updating-homestead"></a>
## Homestead 업데이트 (Updating Homestead)

업데이트 전에 현재 가상 머신을 삭제하려면 Homestead 디렉토리에서 다음 명령어를 실행하세요:

```shell
vagrant destroy
```

그 다음 Homestead 소스 코드를 업데이트합니다. 저장소를 클론한 경우 클론한 위치에서 다음 명령어를 실행하세요:

```shell
git fetch

git pull origin release
```

위 명령어는 GitHub 저장소에서 최신 Homestead 코드를 가져오고 태그를 갱신한 뒤 최신 안정 버전을 체크아웃합니다. 최신 안정 버전은 Homestead [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json` 파일로 Homestead를 설치한 경우, 의존성을 업데이트하려면 `composer.json`에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인한 후 다음을 실행하세요:

```shell
composer update
```

그 다음 `vagrant box update` 명령어로 Vagrant 박스를 업데이트하세요:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후 Homestead 디렉토리에서 `bash init.sh` 명령어를 실행하여 추가 설정 파일들을 업데이트합니다. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 묻습니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 최신 Vagrant 설치를 적용하려면 Homestead 가상 머신을 다시 생성해야 합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상 사용법 (Daily Usage)

<a name="connecting-via-ssh"></a>
### SSH 접속 (Connecting via SSH)

Homestead 디렉토리에서 `vagrant ssh` 명령어를 실행해 가상 머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 등록 (Adding Additional Sites)

Homestead 환경이 실행 중일 때, 다른 Laravel 프로젝트를 위한 Nginx 사이트를 추가할 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 동시에 실행할 수 있습니다. 추가 사이트는 `Homestead.yaml`에 다음처럼 설정합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]  
> 사이트를 추가하기 전에 해당 프로젝트 디렉토리에 대한 [폴더 매핑](#configuring-shared-folders) 설정이 되어 있는지 확인해야 합니다.

Vagrant가 자동으로 "hosts" 파일을 관리하지 않는다면, 새 사이트를 로컬 머신의 `hosts` 파일에 직접 추가해야 할 수 있습니다. macOS, Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`입니다:

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 후 Homestead 디렉토리에서 `vagrant reload --provision` 명령어를 실행하세요.

<a name="site-types"></a>
#### 사이트 유형 (Site Types)

Homestead는 Laravel 외 다른 프로젝트를 편리하게 실행할 수 있도록 다양한 사이트 유형을 지원합니다. 예컨대 Statamic 애플리케이션을 추가하려면 `statamic` 타입을 사용할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원하는 사이트 유형은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본), `proxy`(nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`가 있습니다.

<a name="site-parameters"></a>
#### 사이트 매개변수 (Site Parameters)

Nginx의 `fastcgi_param` 값을 추가하려면 `params` 지시어를 사용하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수 설정 (Environment Variables)

전역 환경 변수는 `Homestead.yaml`의 `variables` 항목에 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 변경 후에는 `vagrant reload --provision` 명령어를 실행해 기계를 다시 프로비저닝해야 합니다. 이 과정에서 PHP-FPM 설정과 `vagrant` 사용자의 환경 변수가 업데이트됩니다.

<a name="ports"></a>
### 포트 설정 (Ports)

기본적으로 다음 포트들이 Homestead 환경에 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; 80 포트로 포워딩
- **HTTPS:** 44300 &rarr; 443 포트로 포워딩

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩 (Forwarding Additional Ports)

추가 포트를 포워딩하려면 `Homestead.yaml`에 `ports` 설정을 추가하고 프로비저닝 후 머신을 재시작하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

추가로 매핑할 수 있는 Homestead 서비스 포트는 다음과 같습니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailpit:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

</div>

<a name="php-versions"></a>
### PHP 버전 (PHP Versions)

Homestead는 동일 가상 머신에서 여러 PHP 버전을 실행할 수 있습니다. 사이트별로 사용할 PHP 버전을 `Homestead.yaml`에 다음과 같이 지정할 수 있으며, 지원 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본)입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내부](#connecting-via-ssh)에서는 CLI에서 다음처럼 원하는 PHP 버전을 사용할 수 있습니다:

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

CLI 기본 PHP 버전을 변경하려면 Homestead 가상 머신 내부에서 아래 명령어를 실행하세요:

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

MySQL과 PostgreSQL 모두 기본적으로 `homestead` 데이터베이스가 설정되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 MySQL(`33060` 포트) 또는 PostgreSQL(`54320` 포트)에 접속할 때는 `127.0.0.1` 주소에 접속하세요. 사용자명과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]  
> 이 비표준 포트들은 호스트 머신에서 데이터베이스에 접속할 때만 사용해야 하며, Laravel 애플리케이션 내의 `database` 설정에서는 기본 포트인 3306(MySQL), 5432(PostgreSQL)을 사용합니다. 이유는 Laravel 앱이 가상 머신 내부에서 실행되기 때문입니다.

<a name="database-backups"></a>
### 데이터베이스 백업 (Database Backups)

Homestead는 가상 머신을 파괴할 때 데이터베이스를 자동으로 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이어야 하며, 이전 버전이라면 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 아래를 추가하세요:

```
backup: true
```

구성 시 `vagrant destroy` 실행 시 `.backup/mysql_backup` 및 `.backup/postgres_backup` 폴더에 데이터베이스를 내보냅니다. 이 폴더는 Homestead를 설치한 위치나 [프로젝트별 설치](#per-project-installation)인 경우 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정 (Configuring Cron Schedules)

Laravel은 단일 `schedule:run` Artisan 명령을 1분마다 실행해 여러 예약 작업을 관리하는 방식을 제공합니다. 이 명령은 `routes/console.php`에 정의된 예약 작업을 확인하여 실행합니다.

Homestead 사이트에 대해 `schedule:run` 명령을 실행하려면 사이트 정의 시 `schedule` 옵션을 `true`로 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

사이트 당 크론 잡 설정은 Homestead 가상 머신의 `/etc/cron.d` 디렉토리에 저장됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정 (Configuring Mailpit)

[Mailpit](https://github.com/axllent/mailpit)은 발송 중인 이메일을 외부로 보내지 않고 가로채어 내용을 확인하도록 돕는 도구입니다. 시작하려면 애플리케이션의 `.env` 파일에서 다음 메일 설정을 사용하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit 설정 후에는 `http://localhost:8025`에서 대시보드를 확인할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정 (Configuring Minio)

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 가진 오픈 소스 객체 저장 서버입니다. Minio를 설치하려면 `Homestead.yaml`의 [features](#installing-optional-features) 섹션에 다음을 추가합니다:

```
minio: true
```

기본적으로 Minio는 9600 포트를 사용하며, 제어판은 `http://localhost:9600`에서 접근 가능합니다. 기본 액세스 키는 `homestead`, 비밀 키는 `secretkey`이며, 항상 `us-east-1` 지역을 사용해야 합니다.

`.env` 파일에는 다음 설정이 포함되어야 합니다:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio 기반의 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시어를 추가하세요. 버킷 정의 후에는 `vagrant reload --provision` 명령어로 가상 머신을 재프로비저닝합니다:

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

[Laravel Dusk](/docs/11.x/dusk) 테스트를 Homestead 내에서 실행하려면 `webdriver` 기능을 활성화하세요:

```yaml
features:
    - webdriver: true
```

활성화 후에는 `vagrant reload --provision` 명령어로 프로비저닝을 다시 수행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기 (Sharing Your Environment)

작업 중인 내용을 동료나 클라이언트와 공유하고 싶을 때가 있습니다. Vagrant는 `vagrant share` 명령을 지원하지만, `Homestead.yaml`에 다중 사이트가 구성된 경우 제대로 동작하지 않습니다.

이 문제를 해결하기 위해 Homestead는 자체 `share` 명령을 포함합니다. 먼저 [Homestead 가상 머신에 SSH 접속](#connecting-via-ssh)한 뒤 `share homestead.test` 명령어를 실행하세요. 이 명령은 `Homestead.yaml` 내 설정된 `homestead.test` 사이트를 공유합니다. 다른 사이트도 동일하게 대체할 수 있습니다:

```shell
share homestead.test
```

명령 실행 후 Ngrok 화면이 나타나며 활동 로그와 공개 접근 가능한 사이트 URL이 표시됩니다. 특수 지역, 서브도메인 등 Ngrok 옵션도 아래처럼 추가할 수 있습니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS로 공유하려면 `share` 대신 `sshare` 명령을 사용하세요.

> [!WARNING]  
> Vagrant는 기본적으로 보안이 취약하므로 `share` 명령 실행 시 가상 머신이 인터넷에 노출됨을 유념하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링 (Debugging and Profiling)

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅 (Debugging Web Requests With Xdebug)

Homestead는 [Xdebug](https://xdebug.org)를 통한 단계별 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지를 열면 PHP가 IDE에 연결되어 실행 중인 코드를 점검하고 수정할 수 있습니다.

기본적으로 Xdebug는 이미 실행 중이며 연결을 대기합니다. CLI에서 Xdebug를 활성화하려면 Homestead 가상 머신 내부에서 `sudo phpenmod xdebug`를 실행하세요. 그 다음 IDE 지침에 따라 디버깅을 활성화하고 브라우저 확장이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)으로 디버깅 트리거를 설정합니다.

> [!WARNING]  
> Xdebug는 PHP 실행 속도를 크게 저하시킵니다. 비활성화하려면 가상 머신 내에서 `sudo phpdismod xdebug` 후 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작 설정 (Autostarting Xdebug)

웹 서버 요청을 수행하는 기능 테스트를 디버깅할 때, 커스텀 헤더나 쿠키를 테스트 코드에 추가하는 대신 Xdebug 자동 시작을 설정하는 것이 편리합니다. Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정해 다음 내용을 추가하세요:

```ini
; Homestead.yaml에서 IP 서브넷이 다르면 이 값도 변경할 수 있음
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅 (Debugging CLI Applications)

PHP CLI 애플리케이션을 디버깅할 때는 Homestead 가상 머신 내에서 `xphp` 셸 별칭을 사용하세요:

```
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 프로파일링 (Profiling Applications With Blackfire)

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션 프로파일링 서비스로, 호출 그래프와 타임라인을 통해 인터랙티브한 프로필 데이터를 제공합니다. 개발, 스테이징, 프로덕션 환경에서 사용할 수 있고, 사용자에게 추가 오버헤드를 발생시키지 않습니다. 또한 코드, `php.ini` 설정에 대한 성능, 품질, 보안 검사를 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈소스 웹 크롤링, 테스트, 스크래핑 도구로 Blackfire와 연동해 프로파일링 시나리오를 자동화합니다.

활성화하려면 Homestead 설정 파일의 `features` 항목에 아래를 추가하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 여러 프로파일링 방법이 제공됩니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스 (Network Interfaces)

`Homestead.yaml`의 `networks` 속성은 가상 머신 네트워크 인터페이스를 구성합니다. 원하는 만큼 여러 인터페이스를 설정할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지 네트워크](https://developer.hashicorp.com/vagrant/docs/networking/public_network)를 활성화하려면 네트워크 타입을 `public_network`로 변경하고 `bridge` 설정을 추가하세요:

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

네트워크가 사용하는 디바이스를 변경하려면 `dev` 옵션을 추가하세요. 기본값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장하기 (Extending Homestead)

Homestead 디렉토리 루트의 `after.sh` 스크립트를 사용해 가상 머신을 확장할 수 있습니다. 이 파일에 가상 머신을 적절히 구성하고 커스터마이징하는데 필요한 셸 명령을 추가하세요.

패키지 설치 시 Ubuntu가 기존 설정 유지 또는 새 설정 파일 덮어쓰기를 묻는 경우가 있습니다. 이를 방지하려면 아래 명령어를 사용해 기존 Homestead 설정을 덮어쓰지 않도록 하세요:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징 (User Customizations)

팀과 함께 Homestead를 사용 시, 각자 개발 스타일에 맞게 Homestead를 조정할 수 있습니다. Homestead 디렉토리(즉, `Homestead.yaml` 파일이 있는 폴더) 루트에 `user-customizations.sh` 파일을 생성하고 원하는 설정을 추가하세요. 다만 이 파일은 버전 관리 대상에서 제외해야 합니다.

<a name="provider-specific-settings"></a>
## 프로바이더 별 설정 (Provider Specific Settings)

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver` 설정

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성하여 호스트 OS의 DNS 설정을 사용합니다. 이 동작을 변경하려면 `Homestead.yaml`에 다음과 같이 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```