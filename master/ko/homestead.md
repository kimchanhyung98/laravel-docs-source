# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [시작하기](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [Alias(별칭)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용](#daily-usage)
    - [SSH로 접속하기](#connecting-via-ssh)
    - [추가 사이트 추가](#adding-additional-sites)
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
    - [Xdebug로 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 앱 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

Laravel은 PHP 개발 전체 경험을 쾌적하게 만드는데 힘쓰며, 로컬 개발 환경 역시 포함됩니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는 미리 패키징된 Vagrant 박스로, PHP, 웹 서버 또는 기타 서버 소프트웨어를 로컬 머신에 별도로 설치할 필요 없이 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝하는 간편하고 우아한 방법을 제공합니다. Vagrant 박스는 언제든지 폐기할 수 있습니다. 문제가 생기면 박스를 몇 분 만에 삭제하고 재생성할 수 있습니다!

Homestead는 Windows, macOS, Linux 시스템에서 실행되며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어가 포함되어 있습니다.

> [!WARNING]
> Windows를 사용하는 경우, 하드웨어 가상화(VT-x) 기능을 활성화해야 할 수 있습니다. 보통 BIOS에서 설정할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우, VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

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

Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads) 및 다음 중 하나의 지원하는 공급자를 설치해야 합니다.

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어는 모든 주요 운영체제에서 사용할 수 있는 직관적인 설치 관리자를 제공합니다.

Parallels 공급자를 사용하려는 경우 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead는 저장소를 호스트 머신에 클론해서 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로, `홈 디렉터리` 내의 `Homestead` 폴더에 저장소를 클론하는 것이 좋습니다. 문서 전체에서 이 디렉터리를 "Homestead 디렉터리"라고 합니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

저장소를 클론한 후, `release` 브랜치를 체크아웃하세요. 이 브랜치는 항상 최신의 안정 릴리스를 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

다음으로, Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성하세요. 이 파일에서 Homestead 설치의 모든 설정을 구성할 수 있습니다. 파일은 Homestead 디렉터리에 생성됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정

<a name="setting-your-provider"></a>
#### 공급자(provider) 지정

`Homestead.yaml` 파일의 `provider` 키는 어떤 Vagrant 공급자를 사용할지 지정합니다: `virtualbox` 또는 `parallels` 중 선택합니다.

    provider: virtualbox

> [!WARNING]
> Apple Silicon 사용자는 Parallels 공급자 필수입니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더를 나열합니다. 이 폴더 내 파일이 변경되면 로컬 머신과 가상 환경 간에 동기화됩니다. 원하는 만큼 공유 폴더를 추가할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로를 사용하지 말고, 예시처럼 전체 경로(`C:\Users\user\Code\project1`)를 사용해야 합니다.

애플리케이션별로 각각 별도의 폴더로 매핑하는 것이 좋으며, 하나의 큰 디렉터리를 통째로 매핑하는 것은 권장하지 않습니다. 가상 머신은 매핑된 폴더 내 모든 파일의 디스크 IO를 관리하게 되므로, 파일이 많을수록 성능 저하가 발생할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead를 사용할 때 현재 디렉터리(`.`)를 매핑해서는 안 됩니다. 현재 폴더가 `/vagrant`에 매핑되지 않아서 일부 기능이 동작하지 않거나 예기치 않은 문제가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs) 사용을 원하면, 폴더 매핑에 `type` 옵션을 추가하세요.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉터리의 사용자·그룹 권한을 올바르게 유지합니다.

Vagrant의 [공유 폴더 옵션](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)도 `options` 키 하위에 추가할 수 있습니다:

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

Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 속성을 통해 "도메인"을 Homestead 환경 내 디렉터리와 손쉽게 매핑할 수 있습니다. 샘플 구성이 포함되어 있으며, 원하는 만큼 사이트를 추가하여 개별 Laravel 애플리케이션마다 독립적으로 운영할 수 있습니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

사이트 정보를 수정한 후에는 가상 머신에서 `vagrant reload --provision` 명령어를 실행해 Nginx 구성을 새로 고치십시오.

> [!WARNING]
> Homestead 스크립트는 최대한 멱등성(idempotent)을 지향합니다. 프로비저닝 과정에서 문제가 발생한다면 `vagrant destroy && vagrant up`으로 머신을 삭제 후 재생성하세요.

<a name="hostname-resolution"></a>
#### 호스트명(도메인) 해석

Homestead는 `mDNS`를 사용해 자동으로 호스트명을 배포합니다. 예를 들어, `Homestead.yaml`에서 `hostname: homestead`로 지정하면 해당 호스트는 `homestead.local`로 접근할 수 있습니다. macOS, iOS, Linux 배포판은 기본적으로 mDNS를 지원하지만, Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US) 설치가 필요합니다.

자동 호스트명 기능은 [프로젝트별 설치](#per-project-installation)에서 가장 잘 동작합니다. 하나의 Homestead 인스턴스에 여러 사이트를 운영할 경우 각 사이트의 도메인을 머신의 `hosts` 파일에 추가해야 합니다. macOS/Linux에서 `/etc/hosts`, Windows에서 `C:\Windows\System32\drivers\etc\hosts` 위치입니다:

```text
192.168.56.56  homestead.test
```

해당 IP는 `Homestead.yaml`에 설정한 것과 반드시 일치해야 합니다. hosts 파일에 도메인을 추가하고 Vagrant 박스를 실행하면 웹 브라우저로 사이트를 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead는 기본적으로 여러 서비스를 실행하지만, 프로비저닝 시 활성화/비활성화할 서비스를 직접 지정할 수 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml`의 `services` 옵션을 수정하세요.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

명시한 서비스는 `enabled`, `disabled` 순서에 따라 시작/중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행하기

`Homestead.yaml`을 원하는 대로 편집한 후, Homestead 디렉터리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하면서 공유 폴더 및 Nginx 사이트 설정을 자동으로 구성합니다.

기계를 삭제하려면 `vagrant destroy` 명령을 사용하면 됩니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역적으로 설치해 모든 프로젝트에서 같은 가상 머신을 공유하는 대신, 프로젝트마다 별도의 Homestead 인스턴스를 설정할 수도 있습니다. 프로젝트별 설치는 프로젝트의 저장소와 함께 `Vagrantfile`을 전달하여, 협업자가 저장소를 클론한 뒤 곧바로 `vagrant up`을 실행해 환경을 띄울 수 있어 유용합니다.

Composer 패키지 관리자를 사용해 프로젝트에 Homestead를 설치하세요.

```shell
composer require laravel/homestead --dev
```

설치 후 Homestead의 `make` 명령을 실행하여 프로젝트에 맞는 `Vagrantfile` 및 `Homestead.yaml` 파일을 생성하세요. 이 파일들은 프로젝트 루트에 위치하며, `make` 명령이 sites, folders 항목을 자동 설정해줍니다.

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 다음 터미널에서 `vagrant up`을 실행한 후 브라우저에서 `http://homestead.test`로 접근하면 됩니다. 자동 [호스트명 해석](#hostname-resolution)을 사용하지 않는다면 `/etc/hosts` 파일 항목 추가가 필요합니다.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션으로 설치합니다. 대부분의 기능은 boolean 값으로 활성화/비활성화하며, 일부 기능은 추가 옵션을 입력할 수 있습니다.

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

지정된 버전(major.minor.patch 양식)의 Elasticsearch를 사용할 수 있습니다. 기본 설치에서는 'homestead'라는 클러스터가 생성됩니다. Elasticsearch는 운영체제의 메모리 절반을 초과해 할당하지 않는 것이 좋으니, Homestead VM에 최소 두 배 이상의 메모리를 할당해 주세요.

> [!NOTE]
> [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하여 설정 방법을 확인하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL 완전 대체품이므로 애플리케이션의 데이터베이스 설정 파일에서 `mysql` 드라이버를 그대로 사용하면 됩니다.

<a name="mongodb"></a>
#### MongoDB

MongoDB의 기본 사용자명은 `homestead`, 비밀번호는 `secret`입니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j의 기본 사용자명은 `homestead`, 비밀번호는 `secret`입니다. Neo4j 브라우저는 `http://homestead.test:7474` 주소에서 접근 가능합니다. 포트 `7687(Bolt)`, `7474(HTTP)`, `7473(HTTPS)`가 클라이언트 요청에 대응합니다.

<a name="aliases"></a>
### 별칭(Alias)

Homestead 가상 머신에서 사용할 Bash 별칭은 Homestead 디렉터리 내의 `aliases` 파일을 수정하세요:

```shell
alias c='clear'
alias ..='cd ..'
```

파일을 수정한 후 `vagrant reload --provision`으로 반드시 재프로비저닝해야 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전에 현재의 가상 머신을 먼저 삭제하세요.

```shell
vagrant destroy
```

그 다음 Homestead 소스 코드를 업데이트합니다. 저장소를 클론한 경우, 원본 위치에서 다음 명령을 실행합니다.

```shell
git fetch

git pull origin release
```

해당 명령은 최신 Homestead 코드를 가져와 최신 릴리즈로 체크아웃합니다. 최신 릴리즈 버전은 [GitHub Releases 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트 내 `composer.json`으로 Homestead를 설치한 경우, `"laravel/homestead": "^12"` 가 포함되어 있는지 확인하고 다음 명령으로 종속성을 업데이트하세요.

```shell
composer update
```

다음으로 `vagrant box update`로 Vagrant 박스를 업데이트합니다.

```shell
vagrant box update
```

Vagrant 박스 업데이트 후, Homestead 디렉터리에서 `bash init.sh`로 추가 설정 파일을 업데이트하세요. 기존 파일(`Homestead.yaml`, `after.sh`, `aliases`) 덮어쓸지 여부가 안내됩니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로, 새로운 Vagrant 설치를 반영하려면 가상 머신을 재생성하세요:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용

<a name="connecting-via-ssh"></a>
### SSH로 접속하기

Homestead 디렉터리에서 `vagrant ssh`를 실행하면 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가

Homestead를 프로비저닝 및 실행한 후, 추가 Nginx 사이트를 등록해 여러 Laravel 프로젝트를 동시에 운영할 수 있습니다. 사이트를 추가하려면 `Homestead.yaml` 파일에 사이트를 기록하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트 추가 전 [폴더 매핑](#configuring-shared-folders)이 선행돼야 합니다.

"hosts" 파일이 자동 관리되지 않는 경우, 새 사이트 도메인을 해당 파일에 추가해야 합니다. macOS/Linux: `/etc/hosts`, Windows: `C:\Windows\System32\drivers\etc\hosts`

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 뒤 Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 다양한 사이트 "유형"을 지원하여 Laravel 기반이 아닌 프로젝트도 쉽게 운영할 수 있습니다. 예를 들어, Statamic 애플리케이션을 `statamic` 유형으로 추가할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원 유효 유형: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
#### 사이트 파라미터

사이트에서 추가로 Nginx `fastcgi_param` 값을 지정하려면 `params` 지시문을 사용하세요:

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

글로벌 환경 변수를 `Homestead.yaml` 파일에 추가할 수 있습니다.

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

파일 수정 후에 `vagrant reload --provision` 명령을 실행하여 모든 PHP-FPM 버전과 `vagrant` 유저 환경이 반영되게 하세요.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead에 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; 80번 포트로 포워딩
- **HTTPS:** 44300 &rarr; 443번 포트로 포워딩

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

필요하다면 `Homestead.yaml` 내에 `ports` 설정을 이용해 추가 포트 포워딩을 정의할 수 있습니다. 변경 후 `vagrant reload --provision`을 꼭 실행하세요.

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

추가로 매핑할 수 있는 기본 Homestead 서비스 포트 목록입니다:

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
### PHP 버전

Homestead는 여러 PHP 버전을 하나의 가상 머신에서 실행할 수 있습니다. 사이트별로 사용할 PHP 버전을 `Homestead.yaml`에 지정할 수 있습니다. 사용 가능한 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내부](#connecting-via-ssh)에서는 CLI를 이용해 지원되는 PHP 버전을 자유롭게 사용할 수 있습니다:

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

CLI 기본 PHP 버전을 변경하려면 아래 명령을 가상 머신 내에서 실행하세요:

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
### 데이터베이스 접속

MySQL, PostgreSQL 모두에 `homestead` 데이터베이스가 기본 설정되어 있습니다. 호스트 머신의 DB 클라이언트로 접속할 경우, MySQL은 `127.0.0.1:33060`, PostgreSQL은 `127.0.0.1:54320`에 연결해야 합니다. 사용자명·비밀번호는 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트에서 DB로 접속할 때만 비표준 포트를 사용하세요. Laravel 애플리케이션 내에서는 기본 포트(3306, 5432)를 사용해야 합니다. (라라벨은 가상 머신 내부에서 실행됩니다.)

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 가상 머신이 삭제될 때 자동으로 데이터베이스를 백업할 수 있습니다. 이 기능은 Vagrant 2.1.0 이상, 또는 구버전에서는 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 다음 줄을 추가하세요:

```yaml
backup: true
```

설정하면 `vagrant destroy` 실행 시 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉터리로 DB가 백업됩니다. 이 폴더는 Homestead 설치 경로나 [프로젝트별 설치](#per-project-installation) 시 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 [단일 아티즌 명령(schedule:run)](/docs/{{version}}/scheduling)을 1분마다 실행하여 모든 크론 작업을 처리할 수 있게 해줍니다. `routes/console.php`의 스케줄 정의를 참조합니다.

특정 사이트에 대해 `schedule:run`을 실행하려면, 사이트 설정 시 `schedule` 옵션을 `true`로 지정하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)은 발송되는 메일을 실제 수신자에게 보내지 않고 확인할 수 있도록 합니다. 사용하려면 앱의 `.env` 파일을 아래와 같이 수정하세요.

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

[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 오브젝트 스토리지 서버입니다. 설치하려면 [features](#installing-optional-features) 섹션에 아래 설정을 추가하세요.

    minio: true

기본적으로 포트 9600에서 사용할 수 있습니다: `http://localhost:9600`. 기본 access key는 `homestead`, secret key는 `secretkey`입니다. region은 반드시 `us-east-1`이어야 합니다.

`.env`에 다음 값을 추가해야 합니다:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio에서 사용할 "S3" 버킷을 만들려면 `Homestead.yaml`에 `buckets` 설정을 추가하세요. 정의 후 `vagrant reload --provision`을 실행하세요.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

`policy` 값으로 `none`, `download`, `upload`, `public`을 지원합니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 테스트를 Homestead 내에서 실행하려면 [`webdriver` 기능](#installing-optional-features)을 활성화 하세요.

```yaml
features:
    - webdriver: true
```

이후 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유

작업 중인 웹 사이트를 동료나 클라이언트와 공유해야 할 경우가 있습니다. Vagrant에는 이를 위한 내장 `vagrant share` 명령이 있지만, Homestead에 여러 사이트가 구성된 경우 동작하지 않습니다.

이 문제를 위해 Homestead자체 `share` 명령이 있습니다. 먼저 [`vagrant ssh`로 접속](#connecting-via-ssh) 후, 아래와 같이 명령을 실행하세요.

```shell
share homestead.test
```

실행하면 ngrok 화면에 공유 사이트의 공개 URL 및 로그가 표시됩니다. 필요하다면 커스텀 region, 서브도메인 등 ngrok 옵션도 추가로 지정할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS 공유를 원한다면 `sshare` 명령을 이용하세요.

> [!WARNING]
> Vagrant는 본질적으로 보안성이 취약하므로, `share` 명령 사용 시 가상 머신이 인터넷에 노출됨을 유념하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead는 [Xdebug](https://xdebug.org)를 이용한 단계별 디버깅을 지원합니다. 브라우저에서 페이지에 접근하면 PHP가 IDE와 연결되어 코드 실행 과정을 점검·수정할 수 있습니다.

기본적으로 Xdebug가 실행 중이며, 별도의 설정 없이도 IDE 연결을 기다립니다. CLI에서 Xdebug를 활성화하려면 가상 머신 내에서 `sudo phpenmod xdebug`를 실행하세요. IDE의 디버그 설정 및 브라우저 확장/북마클릿[bookmarklet](https://www.jetbrains.com/phpstorm/marklets/) 설정도 필요합니다.

> [!WARNING]
> Xdebug는 PHP 실행 속도를 크게 저하시킬 수 있습니다. 비활성화하려면 Homestead에서 `sudo phpdismod xdebug` 실행 후 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버에 요청을 보내는 기능 테스트를 디버깅할 때 Xdebug가 자동 시작되도록 하는 것이 편리합니다. Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일에 아래 설정을 추가하세요.

```ini
; Homestead.yaml에 다른 IP 대역이 있다면 주소가 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 앱 디버깅

PHP CLI 프로그램을 디버그하려면 가상 머신에서 `xphp` 별칭을 사용하세요.

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 앱 성능 분석을 위한 서비스입니다. 직관적인 UI에서 호출 그래프와 타임라인으로 프로파일 결과를 표시하며, 개발·스테이징·프로덕션 환경 모두에서 사용 가능합니다. 또한, 코드 및 `php.ini` 설정에 대한 성능, 품질, 보안 체크도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈 소스 웹 크롤링, 웹 테스트, 스크래핑 툴로서, Blackfire와 연동해 프로파일링 시나리오 작성을 도와줍니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 항목을 사용하세요.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격 증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. 자세한 옵션 및 사용법은 [Blackfire 공식 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참조하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 인터페이스를 추가할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브릿지 모드](https://developer.hashicorp.com/vagrant/docs/networking/public_network)를 활성화하려면 `public_network` 유형과 `bridge` 설정을 추가합니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP 활성화](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)는 `ip` 옵션을 제거하면 자동 적용됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크가 사용할 장치 지정은 `dev` 옵션을 통해 설정할 수 있습니다. 기본값은 `eth0`입니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장하기

Homestead 디렉터리의 루트에 위치한 `after.sh` 스크립트를 통해 Homestead를 확장할 수 있습니다. 필요한 셸 명령을 이 파일에 추가해 가상 머신 설정과 커스터마이징을 자유롭게 할 수 있습니다.

원치 않는 패키지 설정 덮어쓰기를 방지하려면 아래와 같이 패키지 설치 명령에 옵션을 추가하세요.

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징

팀 작업에서 Homestead 환경을 개인 개발 스타일에 맞게 조정하려면, Homestead 디렉터리 루트(`Homestead.yaml`과 동일한 경로)에 `user-customizations.sh` 파일을 만들어 원하는 설정을 추가하세요. 단, 이 파일은 버전 관리에 포함되지 않아야 합니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 옵션을 `on`으로 설정합니다. 이를 통해 Homestead가 호스트 OS의 DNS 설정을 사용할 수 있습니다. 이 동작을 변경하려면 `Homestead.yaml` 파일에 다음 옵션을 추가하세요.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```