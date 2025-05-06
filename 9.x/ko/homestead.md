# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정하기](#configuring-homestead)
    - [Nginx 사이트 설정하기](#configuring-nginx-sites)
    - [서비스 설정하기](#configuring-services)
    - [Vagrant 박스 실행하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치하기](#installing-optional-features)
    - [별칭(Alias)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용법](#daily-usage)
    - [SSH로 접속하기](#connecting-via-ssh)
    - [추가 사이트 추가하기](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 접속](#connecting-to-databases)
    - [데이터베이스 생성](#creating-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 일정 설정하기](#configuring-cron-schedules)
    - [MailHog 설정](#configuring-mailhog)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 앱 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장](#extending-homestead)
- [공급자별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

Laravel은 여러분의 로컬 개발 환경을 포함하여 전체 PHP 개발 경험을 더욱 즐겁게 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 PHP, 웹 서버, 그 외 서버 소프트웨어를 로컬에 직접 설치할 필요 없이, 멋진 개발 환경을 제공해주는 공식 사전 패키징된 Vagrant 박스입니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 단순하고 우아하게 관리 및 프로비저닝할 수 있는 방법을 제공합니다. Vagrant 박스는 언제든지 폐기할 수 있습니다. 무언가 잘못된다면 박스를 파괴하고 몇 분 안에 다시 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 시스템 어디에서나 실행 가능하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 및 놀라운 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> **경고**  
> Windows를 사용하는 경우, 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 이는 일반적으로 BIOS를 통해 설정할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어

- Ubuntu 20.04
- Git
- PHP 8.2 (기본값)
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

<a name="optional-software"></a>
### 선택적 소프트웨어

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
- Webdriver & Laravel Dusk 도구

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 첫 단계

Homestead 환경을 시작하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)를 설치하고 아래 중 하나의 지원되는 공급자를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어들은 모든 주요 운영체제에서 쉽게 사용할 수 있는 설치 프로그램을 제공합니다.

Parallels 공급자를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 저장소를 호스트 머신에 클론하여 설치할 수 있습니다. "홈" 디렉토리 내에 `Homestead` 폴더를 만들어 클론하는 것이 좋으며, 이 Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 합니다. 본 문서에서는 이 디렉토리를 "Homestead 디렉토리"라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead 저장소를 클론한 후, `release` 브랜치를 체크아웃해야 합니다. 이 브랜치는 항상 Homestead의 최신 안정 릴리스를 포함하고 있습니다:

```shell
cd ~/Homestead

git checkout release
```

그 다음, Homestead 디렉토리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. 이 파일에 Homestead 설치를 위한 모든 설정을 하게 됩니다. 해당 파일은 Homestead 디렉토리에 생성됩니다:

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

`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 공급자(VirtualBox 또는 Parallels)를 지정합니다:

    provider: virtualbox

> **경고**  
> Apple Silicon을 사용하는 경우 `Homestead.yaml` 파일에 `box: laravel/homestead-arm`을 추가해야 합니다. Apple Silicon은 Parallels 공급자를 필요로 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더들을 나열합니다. 이 폴더 내 파일을 변경하면 로컬과 가상 머신 사이가 동기화됩니다. 필요한 만큼 많은 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> **경고**  
> Windows 사용자는 `~/` 경로 대신 전체 경로(`C:\Users\user\Code\project1`)를 사용해야 합니다.

각 애플리케이션 별로 개별 폴더 매핑을 해야 하며, 여러 애플리케이션이 들어있는 큰 디렉토리를 한 번에 매핑하는 것은 권장하지 않습니다. VM은 매핑한 폴더 내 모든 파일의 디스크 IO를 추적해야 하므로, 파일이 많을수록 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> **경고**  
> Homestead를 사용할 때는 절대 `.`(현재 디렉토리)를 마운트하지 마세요. 이는 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않게 하며, 선택적 기능들이 동작하지 않거나 예기치 못한 결과를 유발합니다.

[NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html)를 활성화하려면, 매핑에 `type` 옵션을 추가하세요:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> **경고**  
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 이 플러그인은 파일 및 디렉토리의 올바른 사용자/그룹 권한을 유지하도록 도와줍니다.

또한, Vagrant의 [Synced Folders](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)가 지원하는 옵션을 `options` 키 아래에 나열하여 전달할 수 있습니다:

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
### Nginx 사이트 설정하기

Nginx가 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 속성을 사용하면 "도메인"을 Homestead 환경 내 폴더에 쉽게 매핑할 수 있습니다. 예시 사이트 설정은 기본 `Homestead.yaml` 파일에 포함되어 있습니다. 필요에 따라 원하는 만큼 사이트를 추가할 수 있습니다. Homestead는 여러분이 작업하는 모든 Laravel 애플리케이션에 대해 편리한 가상 환경을 제공합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Homestead 가상 머신을 프로비저닝한 후에 `sites` 속성을 변경했다면, 터미널에서 `vagrant reload --provision` 명령어를 실행하여 Nginx 설정을 업데이트하세요.

> **경고**  
> Homestead 스크립트는 최대한 멱등적으로 설계되어 있습니다. 그러나 프로비저닝 중 문제가 발생한다면, `vagrant destroy && vagrant up` 명령어로 머신을 파괴하고 재생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
#### 호스트 이름 해상

Homestead는 `mDNS`를 사용하여 호스트 이름을 자동으로 게시합니다. `Homestead.yaml`에 `hostname: homestead`를 설정하면, 해당 호스트는 `homestead.local`로 접근할 수 있습니다. macOS, iOS, Linux 데스크탑 배포판은 기본적으로 `mDNS`를 지원합니다. Windows를 사용하는 경우 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명 기능은 [프로젝트별 설치](#per-project-installation)에서 가장 잘 동작합니다. 하나의 Homestead 인스턴스에 여러 사이트를 호스팅하는 경우에는, PC의 `hosts` 파일에 웹사이트의 "도메인"을 추가해야 합니다. 이 파일은 macOS나 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`입니다. 이 파일에 아래와 같이 추가합니다:

    192.168.56.56  homestead.test

`Homestead.yaml`에 설정된 IP와 동일해야 합니다. hosts 파일에 도메인을 추가하고 Vagrant 박스를 실행한 뒤 웹 브라우저를 통해 사이트에 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정하기

Homestead는 기본적으로 여러 서비스를 시작하지만, 프로비저닝 시 활성화/비활성화할 서비스를 직접 지정할 수 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml` 파일의 `services` 옵션을 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

명시한 서비스들은 `enabled` 및 `disabled` 키의 순서에 따라 실행 혹은 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행하기

`Homestead.yaml`을 원하는 대로 수정한 뒤, Homestead 디렉토리에서 `vagrant up` 명령어를 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더 및 Nginx 사이트를 자동으로 설정합니다.

머신을 종료하려면 `vagrant destroy` 명령어를 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역으로 설치해 모든 프로젝트에서 같은 가상 머신을 공유하는 대신, 각 프로젝트마다 Homestead 인스턴스를 개별적으로 구성할 수 있습니다. 이 방식은 `Vagrantfile`을 프로젝트와 함께 배포할 수 있으므로, 다른 사람이 프로젝트를 클론한 즉시 `vagrant up`으로 환경을 바로 실행할 수 있습니다.

Composer 패키지 매니저를 사용해 Homestead를 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```

설치 후, 프로젝트에 대해 `make` 명령어를 실행하여 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 이 파일들은 프로젝트 루트에 위치하게 되며, `sites` 및 `folders` 옵션도 자동으로 설정됩니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 후 터미널에서 `vagrant up` 명령어를 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접속할 수 있습니다. 자동 [호스트명 해상](#hostname-resolution)을 사용하지 않을 경우, `homestead.test` 도메인을 `/etc/hosts` 파일에 추가해야 한다는 점을 잊지 마세요.

<a name="installing-optional-features"></a>
### 선택적 기능 설치하기

선택적 소프트웨어는 `Homestead.yaml`의 `features` 옵션을 통해 설치합니다. 대부분의 기능은 불린 값으로 활성화/비활성화하며, 일부 기능은 여러 구성 옵션을 지원합니다:

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

Elasticsearch의 지원 버전을 명확히(주.소.수) 지정할 수 있습니다. 기본 설치는 'homestead'라는 클러스터를 생성합니다. Elasticsearch 할당 메모리보다 Homestead VM 메모리가 2배 이상인지 반드시 확인하세요.

> **참고**  
> [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하여 설정을 맞춤화할 수 있습니다.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL과 호환되므로, 애플리케이션의 데이터베이스 설정에서는 `mysql` 드라이버를 계속 사용해야 합니다:

```yaml
features:
  - mariadb: true
```

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치는 사용자명을 `homestead`로, 비밀번호는 `secret`으로 설정합니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치는 사용자명을 `homestead`로, 비밀번호는 `secret`으로 설정합니다. Neo4j 브라우저는 웹 브라우저로 `http://homestead.test:7474`에서 접속할 수 있습니다. `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS) 포트가 Neo4j 클라이언트를 위해 열려 있습니다.

<a name="aliases"></a>
### 별칭(Alias)

Homestead 가상 머신에서 사용할 bash 별칭을 Homestead 디렉토리 내 `aliases` 파일을 수정해 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

파일 수정 후 `vagrant reload --provision` 명령어를 실행해 별칭을 적용하세요.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전, Homestead 디렉토리에서 아래 명령어로 기존 가상 머신을 제거해야 합니다:

```shell
vagrant destroy
```

그 다음, Homestead 소스 코드를 업데이트 해야 합니다. 저장소에서 클론했다면 클론한 위치에서 다음 명령어를 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령어는 최신 Homestead 코드를 가져오고, 가장 최신 태그 릴리스를 체크아웃합니다. 최신 안정 릴리스는 Homestead [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`으로 설치한 경우 `"laravel/homestead": "^12"`가 있는지 확인한 뒤 아래와 같이 의존성을 업데이트하세요:

```shell
composer update
```

다음은 `vagrant box update`로 Vagrant 박스를 업데이트합니다:

```shell
vagrant box update
```

Vagrant 박스 업데이트 후, Homestead 디렉토리에서 `bash init.sh` 명령어를 실행하여 부가 설정 파일을 갱신하세요. 기존 파일(`Homestead.yaml`, `after.sh`, `aliases`)을 덮어쓸지 여부를 묻는 창이 뜸니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 Vagrant의 최신 설치를 적용하려면 가상 머신을 재생성 해야 합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용법

<a name="connecting-via-ssh"></a>
### SSH로 접속하기

Homestead 디렉토리에서 `vagrant ssh` 명령어로 가상 머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가하기

Homestead 환경이 프로비저닝되고 실행 중이라면, 다른 Laravel 프로젝트를 위한 추가 Nginx 사이트를 생성할 수 있습니다. 하나의 Homestead 환경에서 원하는 만큼 많은 Laravel 프로젝트를 실행할 수 있습니다. 사이트를 추가하려면 `Homestead.yaml`에 아래처럼 추가합니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> **경고**  
> 새 사이트를 추가하기 전에 반드시 해당 프로젝트의 [폴더 매핑](#configuring-shared-folders)이 되어 있는지 확인하세요.

Vagrant가 "hosts" 파일을 자동 관리하지 않는다면, 신규 사이트를 hosts 파일에도 수동으로 추가해야 합니다. `/etc/hosts`(macOS/Linux), `C:\Windows\System32\drivers\etc\hosts`(Windows):

    192.168.56.56  homestead.test
    192.168.56.56  another.test

사이트를 추가한 후 `vagrant reload --provision` 명령어로 변경 사항을 반영하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 Laravel 이외의 프로젝트도 쉽게 실행할 수 있도록 다양한 사이트 "type"을 지원합니다. 예를 들어, `statamic` 사이트 타입으로 Statamic 애플리케이션을 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원되는 사이트 유형: `apache`, `apigility`, `expressive`, `laravel`(기본값), `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
#### 사이트 파라미터

사이트의 Nginx `fastcgi_param` 값을 추가하려면 사이트 설정에 `params`를 추가하세요:

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

`Homestead.yaml` 파일에 전역 환경 변수를 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml`을 수정한 후 `vagrant reload --provision` 명령어로 가상 머신을 재프로비저닝 하세요. 그러면 모든 PHP-FPM 버전에 적용되고, `vagrant` 사용자 환경도 갱신됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경으로 포워딩됩니다:

- **HTTP:** 8000 &rarr; 80으로 포워딩
- **HTTPS:** 44300 &rarr; 443으로 포워딩

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

원한다면 `Homestead.yaml` 파일에 `ports` 항목을 추가해 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. 설정 후, 반드시 `vagrant reload --provision`을 실행해야 합니다:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

추가적으로 매핑 가능할 수 있는 Homestead 서비스 포트 예시는 다음과 같습니다:

- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailhog:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

<a name="php-versions"></a>
### PHP 버전

Homestead는 같은 가상 머신 내에서 다중 PHP 버전 실행을 지원합니다. 각 사이트에서 사용할 PHP 버전을 `Homestead.yaml`에 지정할 수 있습니다. 사용 가능한 PHP 버전은: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2"(기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.4"
```

[Homestead 가상 머신 내](#connecting-via-ssh)에서, 다음과 같이 CLI에서 원하는 PHP 버전을 사용할 수 있습니다:

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

CLI에서 사용할 PHP 버전을 `Homestead.yaml`에 지정할 수도 있습니다:

```yaml
php: 8.0
```

혹은 Homestead 안의 가상 머신에서 아래 명령을 직접 실행해 변경할 수 있습니다:

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
### 데이터베이스 접속

MySQL 및 PostgreSQL 모두에 대해 `homestead` 데이터베이스가 기본 구성됩니다. 호스트 머신에서 MySQL이나 PostgreSQL에 접속하려면 `127.0.0.1`의 `33060`(MySQL) 또는 `54320`(PostgreSQL) 포트로 접속하세요. ID와 비밀번호 모두 `homestead` / `secret`입니다.

> **경고**  
> 호스트 머신에서 연결할 때만 이 포트를 사용해야 하며, Laravel 앱에서는(가상 머신 내에서) 기본 포트 3306(Mysql), 5432(PostgreSQL)을 사용하세요.

<a name="creating-databases"></a>
### 데이터베이스 생성

Homestead는 애플리케이션에 필요한 데이터베이스를 자동으로 생성할 수 있습니다. 프로비저닝 중 데이터베이스 서비스가 실행 중이라면 `Homestead.yaml` 파일에 나열된 각 데이터베이스가 없을 경우 생성됩니다:

```yaml
databases:
  - database_1
  - database_2
```

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 가상 머신이 파괴될 때 데이터베이스를 자동으로 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요하며, 이전 버전이라면 `vagrant-triggers` 플러그인을 설치해야 합니다. 활성화는 `Homestead.yaml`에 다음을 추가하면 됩니다:

    backup: true

설정하면 `vagrant destroy` 명령어 실행 시, 데이터베이스가 `.backup/mysql_backup`, `.backup/postgres_backup` 디렉터리에 백업됩니다. 이 디렉터리는 Homestead 설치 위치 혹은 [프로젝트별 설치](#per-project-installation)시엔 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 일정 설정하기

Laravel은 [크론 작업 예약](/docs/{{version}}/scheduling)을 지원합니다. `schedule:run` 아티즌 명령어를 매 분마다 실행하면, `App\Console\Kernel`에 정의된 예약 작업을 수행하게 됩니다.

특정 Homestead 사이트에서 `schedule:run` 명령어가 실행되게 하려면, 사이트 설정에서 `schedule` 옵션을 `true`로 지정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 cron 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉토리에 정의됩니다.

<a name="configuring-mailhog"></a>
### MailHog 설정

[MailHog](https://github.com/mailhog/MailHog)를 통해 발송 메일을 실제로 보내지 않고 가로채서 확인할 수 있습니다. 사용하려면, 애플리케이션의 `.env` 파일을 아래와 같이 수정하세요:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

MailHog 설정 후, `http://localhost:8025`에서 MailHog 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 오브젝트 스토리지 서버입니다. 설치하려면 [features](#installing-optional-features) 영역에 아래처럼 추가하세요:

    minio: true

기본적으로 Minio는 9600 포트에서 동작합니다. 제어판은 `http://localhost:9600`에서 접근할 수 있으며, 기본 Access Key는 `homestead`, Secret Key는 `secretkey`입니다. region은 항상 `us-east-1`을 사용하세요.

Minio 사용을 위해서는 애플리케이션의 `config/filesystems.php`에서 S3 디스크 구성을 아래처럼 해야 합니다:

    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
        'endpoint' => env('AWS_URL'),
        'use_path_style_endpoint' => true,
    ]

그리고 `.env` 파일을 아래와 같이 설정하세요:

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio 기반의 "S3" 버킷을 프로비저닝하려면, `Homestead.yaml`에 `buckets` 항목을 추가합니다. 설정 후 반드시 `vagrant reload --provision`을 실행하세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

`policy` 지원 값: `none`, `download`, `upload`, `public`

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 테스트를 Homestead에서 실행하려면 [`webdriver` 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

활성화 후 `vagrant reload --provision`을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기

작업 중인 환경을 동료나 고객에게 공유하려 할 때, Vagrant는 `vagrant share` 명령어로 이 기능을 지원합니다. 하지만 `Homestead.yaml`에 여러 사이트가 설정되어 있을 때는 동작하지 않습니다.

이 문제를 해결하기 위해 Homestead에는 자체 `share` 명령이 있습니다. 우선 [Homestead에 SSH로 접속](#connecting-via-ssh)한 후 `share homestead.test` 명령을 실행하세요. 이 명령은 `Homestead.yaml`의 설정된 사이트 중 `homestead.test`를 공유합니다. 물론 다른 사이트도 지정할 수 있습니다:

```shell
share homestead.test
```

명령을 실행하면 Ngrok 화면에 접근 로그와 외부에서 접속할 수 있는 URL이 표시됩니다. region, 서브도메인 등 ngrok 실행 시 추가 옵션도 사용할 수 있습니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```

> **경고**  
> Vagrant 공유는 기본적으로 보안이 강하지 않으므로, `share` 명령 사용 시 VM이 인터넷에 노출된다는 점을 인지하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅

Homestead에는 [Xdebug](https://xdebug.org)를 활용한 스텝 디버깅이 내장되어 있습니다. 예를 들어, 브라우저에서 페이지에 접근하면 PHP가 IDE로 연결되어 실행 중 코드의 점검과 수정이 가능합니다.

기본적으로 Xdebug는 실행 중이며 연결을 대기합니다. CLI에서 Xdebug 활성화/비활성화는 Homestead 내에서 `sudo phpenmod xdebug` 또는 `sudo phpdismod xdebug` 명령으로 수행할 수 있습니다.

IDE 안내에 따라 디버깅을 활성화하고, 브라우저 확장이나 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)으로 Xdebug를 트리거 하세요.

> **경고**  
> Xdebug가 활성화되면 PHP 속도가 느려집니다. CLI에서 `sudo phpdismod xdebug` 후 FPM 서비스를 재시작하면 비활성화할 수 있습니다.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버 요청을 포함한 기능 테스트 시, 디버깅 요청에 헤더나 쿠키를 수동으로 추가하지 않고도 Xdebug를 자동으로 시작하는 것이 편리합니다. 자동 시작하려면, Homestead 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 다음처럼 수정하세요:

```ini
; Homestead.yaml의 서브넷이 다르면 아래 IP가 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 앱 디버깅

PHP CLI 애플리케이션을 디버깅하려면, Homestead 내에서 `xphp` 별칭을 사용하세요:

    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션의 성능 프로파일링 서비스입니다. 호출 그래프, 타임라인 등 다양한 시각화가 제공되며, 개발/테스트/운영 환경에서 엔드유저에 영향 없이 동작합니다. 또한 코드 및 `php.ini`의 품질/성능/보안 검사 기능도 있습니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 시나리오 기반 웹 크롤/웹 테스트/웹 스크래핑을 지원하는 오픈소스 도구로, Blackfire와 연동 가능합니다.

Blackfire 활성화는 Homestead 설정 파일의 "features" 항목에 아래처럼 지정합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버와 클라이언트 자격증명 발급에는 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 다양한 프로파일링 방법이 제공되니 [자세한 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 가상 머신의 네트워크 인터페이스를 구성합니다. 필요한 만큼 여러 인터페이스를 설정할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지드 네트워크](https://www.vagrantup.com/docs/networking/public_network.html)를 활성화하려면 `bridge` 설정과 함께 네트워크 Type을 `public_network`로 변경하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://www.vagrantup.com/docs/networking/public_network.html)를 사용하려면, `ip` 옵션을 삭제하세요:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead 디렉토리 루트의 `after.sh` 스크립트로 Homestead를 확장할 수 있습니다. 이 파일에 가상 머신에서 원하는 셸 명령을 추가하세요.

커스터마이징 중 Ubuntu에서 기존 패키지 설정을 유지할지 새로운 설정 파일로 덮어쓸지 묻는 경우가 있을 수 있습니다. 이를 방지하려면, 아래와 같이 설치하세요:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징

팀에서 Homestead를 사용할 때, 개인 개발 스타일에 맞게 수정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉토리 루트(즉, `Homestead.yaml`이 위치한 곳)에 `user-customizations.sh` 파일을 만들어 임의의 설정을 추가하세요. 단, 이 파일은 버전 관리에 포함하지 마십시오.

<a name="provider-specific-settings"></a>
## 공급자별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 옵션을 `on`으로 설정합니다. 이를 통해 Homestead가 호스트 운영체제의 DNS를 사용할 수 있습니다. 이 설정을 변경하려면 `Homestead.yaml`에 아래와 같이 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

<a name="symbolic-links-on-windows"></a>
#### Windows의 심볼릭 링크 문제

Windows에서 심볼릭 링크가 제대로 동작하지 않는 경우, `Vagrantfile`에 다음 블록을 추가하세요:

```ruby
config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```
