# Laravel Homestead

- [소개](#introduction)
- [설치 & 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정하기](#configuring-homestead)
    - [Nginx 사이트 구성](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [옵션 기능 설치하기](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용](#daily-usage)
    - [SSH로 접속하기](#connecting-via-ssh)
    - [사이트 추가하기](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [MailHog 설정](#configuring-mailhog)
    - [Minio 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
- [디버깅 & 프로파일링](#debugging-and-profiling)
    - [Xdebug를 통한 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire를 통한 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

Laravel은 전체 PHP 개발 환경을 쾌적하게 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는, 미리 구성된 Vagrant 박스입니다. Homestead를 사용하면 로컬 컴퓨터에 PHP, 웹 서버, 기타 서버 소프트웨어를 설치할 필요 없이 훌륭한 개발 환경을 누릴 수 있습니다.

[Vagrant](https://www.vagrantup.com)는 가상머신을 쉽고 우아하게 관리하고 프로비저닝할 수 있도록 도와줍니다. Vagrant 박스는 언제든지 삭제하고 다시 생성할 수 있기 때문에, 문제가 발생하더라도 몇 분 만에 환경을 복구할 수 있습니다!

Homestead는 Windows, macOS, Linux 모두에서 동작하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 거의 모든 필수 소프트웨어를 제공합니다.

> {note} Windows를 사용하는 경우 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 보통 BIOS 설정에서 변경할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용 중이라면, VT-x 접근을 위해 Hyper-V를 비활성화해야 할 수 있습니다.

<a name="included-software"></a>
### 기본 포함 소프트웨어

<div id="software-list" markdown="1">

- Ubuntu 20.04
- Git
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
- PostgreSQL 13
- Composer
- Node (Yarn, Bower, Grunt 및 Gulp 포함)
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
- Docker
- Elasticsearch
- EventStoreDB
- Gearman
- Go
- Grafana
- InfluxDB
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
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk Utilities

</div>

<a name="installation-and-setup"></a>
## 설치 & 설정

<a name="first-steps"></a>
### 첫 단계

Homestead 환경을 실행하기 전에, [Vagrant](https://www.vagrantup.com/downloads.html)와 다음 중 하나의 지원 프로바이더를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어들은 모두 주요 운영체제에서 간단한 시각적 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 리포지터리를 호스트 머신에 클론하여 설치할 수 있습니다. Homestead 가상머신은 모든 Laravel 애플리케이션의 호스트 역할을 하므로 "홈" 디렉터리 내 `Homestead` 폴더에 클론하는 것을 권장합니다. 이 문서 전체에서 이 디렉터리를 "Homestead 디렉터리"로 지칭합니다:

```bash
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Homestead 리포지터리를 클론한 후에는 `release` 브랜치로 체크아웃 해야 합니다. 이 브랜치는 항상 최신 안정화 버전을 포함하고 있습니다:

    cd ~/Homestead

    git checkout release

다음으로, Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 구성 파일을 생성하세요. 이 파일에서 Homestead 설치를 위한 모든 설정을 지정할 수 있습니다. 파일은 Homestead 디렉터리 내에 생성됩니다:

    // macOS / Linux...
    bash init.sh

    // Windows...
    init.bat

<a name="configuring-homestead"></a>
### Homestead 설정하기

<a name="setting-your-provider"></a>
#### 프로바이더 설정

`Homestead.yaml` 파일의 `provider` 키는 어떤 Vagrant 프로바이더를 사용할지 지정합니다. 예시: `virtualbox` 또는 `parallels`

    provider: virtualbox

> {note} Apple Silicon을 사용하는 경우, `Homestead.yaml` 파일에 `box: laravel/homestead-arm`을 추가해야 합니다. Apple Silicon은 Parallels 프로바이더가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유하고자 하는 모든 폴더를 나열합니다. 이 폴더 내 파일들이 변경되면 로컬 머신과 Homestead 가상환경 간에 동기화됩니다. 필요한 만큼 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> {note} Windows 사용자는 `~/` 경로 구문 대신 전체 경로(`C:\Users\user\Code\project1` 등)를 사용해야 합니다.

가능하다면 애플리케이션마다 별도의 폴더 매핑을 생성하고, 모든 애플리케이션을 하나의 폴더에 몰아서 매핑하지 마세요. 하나의 대형 폴더를 매핑하는 경우, 가상머신은 그 폴더 내의 *모든* 파일의 디스크 입출력을 추적해야 하므로 성능이 저하될 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> {note} Homestead 사용 시 현재 디렉터리(`.`)를 마운트해서는 안 됩니다. 이로 인해 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않게 되며, 선택적 기능이 제대로 동작하지 않거나 예기치 않은 결과를 초래할 수 있습니다.

[NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html)를 활성화하려면, 폴더 매핑에 `type` 옵션을 추가하세요:

    folders:
        - map: ~/code/project1
          to: /home/vagrant/project1
          type: "nfs"

> {note} Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 이 플러그인은 Homestead 가상머신 내 파일/디렉터리의 사용자 및 그룹 권한을 올바르게 유지해 줍니다.

[Vagrant Synced Folders](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)가 지원하는 옵션은 `options` 키 아래에 나열하여 전달할 수 있습니다:

    folders:
        - map: ~/code/project1
          to: /home/vagrant/project1
          type: "rsync"
          options:
              rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
              rsync__exclude: ["node_modules"]

<a name="configuring-nginx-sites"></a>
### Nginx 사이트 구성

Nginx에 익숙하지 않아도 걱정하지 마세요. `Homestead.yaml` 파일의 `sites` 속성을 이용하면 쉽게 Homestead 환경 내 폴더에 "도메인"을 매핑할 수 있습니다. 샘플 사이트 구성도 기본 제공됩니다. 필요에 따라 여러 사이트를 Homestead 환경에 추가할 수 있습니다. Homestead는 여러분이 작업 중인 모든 Laravel 애플리케이션을 위한 편리하고 가상화된 환경을 제공합니다:

    sites:
        - map: homestead.test
          to: /home/vagrant/project1/public

Homestead 가상머신 프로비저닝 후 `sites` 속성을 변경했다면, 가상머신 내 Nginx 구성을 갱신하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> {note} Homestead 스크립트는 최대한 멱등성을 보장하도록 설계되어 있지만, 프로비저닝 문제 발생 시 `vagrant destroy && vagrant up` 명령을 통해 머신을 삭제 후 재생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
#### 호스트네임(도메인) 해석

Homestead는 `mDNS`로 호스트네임을 자동으로 등록합니다. 만약 `Homestead.yaml`에 `hostname: homestead`로 설정하면, 해당 호스트는 `homestead.local`로 접근할 수 있습니다. macOS, iOS, 주요 Linux 데스크톱 환경은 기본적으로 `mDNS`를 지원합니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트네임 기능은 [프로젝트별 설치](#per-project-installation)에 가장 적합합니다. 한 Homestead 인스턴스에 여러 사이트를 올릴 경우, 각 웹사이트의 "도메인"을 로컬 컴퓨터의 `hosts` 파일에 직접 추가해야 합니다. `hosts` 파일은 요청을 Homestead 가상머신으로 리다이렉트하는 역할을 하며, macOS/Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`에 위치합니다. 예시:

    192.168.56.56  homestead.test

IP 주소는 `Homestead.yaml`에 설정된 주소와 일치해야 합니다. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면, 웹 브라우저에서 해당 사이트에 접근할 수 있습니다:

```bash
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정

Homestead는 기본적으로 여러 서비스를 시작합니다. 하지만, 프로비저닝 시 활성화/비활성화할 서비스를 직접 지정할 수 있습니다. 예를 들어, PostgreSQL은 활성화하고 MySQL은 비활성화하려면 `Homestead.yaml` 파일 내 `services` 옵션을 아래와 같이 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

`enabled` 및 `disabled` 지시어에 따라 해당 서비스가 활성화 또는 비활성화됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행

`Homestead.yaml`을 원하는 대로 수정했다면, Homestead 디렉터리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상머신을 부팅하고, 공유 폴더 및 Nginx 사이트를 자동으로 구성합니다.

머신을 삭제하려면 `vagrant destroy` 명령을 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역으로 설치하여 모든 프로젝트에서 하나의 Homestead 가상머신을 공유하는 대신, 각 프로젝트에 독립적으로 Homestead 인스턴스를 설정할 수도 있습니다. 프로젝트별 설치는 `Vagrantfile`을 프로젝트에 포함시켜 협업자들이 프로젝트 리포지토리 클론 후 곧바로 `vagrant up`을 실행할 수 있도록 합니다.

Composer 패키지 매니저를 사용해 프로젝트에 Homestead를 설치하세요:

```bash
composer require laravel/homestead --dev
```

설치가 완료되면 Homestead의 `make` 명령어를 실행하여 해당 프로젝트를 위한 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 이 파일들은 프로젝트 루트에 생성됩니다. `make` 명령은 `Homestead.yaml` 내 `sites` 및 `folders` 지시어도 자동으로 구성합니다:

    // macOS / Linux...
    php vendor/bin/homestead make

    // Windows...
    vendor\\bin\\homestead make

이후 터미널에서 `vagrant up` 명령을 실행한 후 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 [호스트네임 해석](#hostname-resolution)을 사용하지 않는 경우, `homestead.test` 등에 대한 `/etc/hosts` 항목 추가를 잊지 마세요.

<a name="installing-optional-features"></a>
### 옵션 기능 설치하기

선택적 소프트웨어 기능들은 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불리언 값으로 활성화/비활성화할 수 있으나, 일부 기능은 추가 구성 옵션도 지원됩니다:

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
        - docker: true
        - elasticsearch:
            version: 7.9.0
        - eventstore: true
            version: 21.2.0
        - gearman: true
        - golang: true
        - grafana: true
        - influxdb: true
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
        - rvm: true
        - solr: true
        - timescaledb: true
        - trader: true
        - webdriver: true

<a name="elasticsearch"></a>
#### Elasticsearch

지원되는 Elasticsearch 버전을 지정할 수 있으며, 반드시 정확한 버전(주.부.패치 형식)이어야 합니다. 기본 설치 시 클러스터 이름은 'homestead'로 생성됩니다. Elasticsearch에 할당하는 메모리는 OS 전체 메모리의 절반을 넘지 않도록 해야 하고, 가상머신 메모리가 Elasticsearch 할당량의 두 배 이상이어야 합니다.

> {tip} [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)에서 구성 방법 등 더 자세한 내용을 확인할 수 있습니다.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 삭제되고 MariaDB가 설치됩니다. MariaDB는 MySQL의 드롭인 교체 역할을 하므로, 애플리케이션 데이터베이스 구성에서 여전히 `mysql` 드라이버를 사용할 수 있습니다.

<a name="mongodb"></a>
#### MongoDB

MongoDB 기본 설치 시, 데이터베이스 username은 `homestead`, password는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j 기본 설치 시, 데이터베이스 username은 `homestead`, password는 `secret`입니다. Neo4j 브라우저는 `http://homestead.test:7474`에서 접근할 수 있습니다. 포트 `7687` (Bolt), `7474` (HTTP), `7473` (HTTPS)이 Neo4j 클라이언트의 요청을 처리할 준비가 되어 있습니다.

<a name="aliases"></a>
### 별칭(Aliases)

Homestead 가상머신에서 Bash 별칭을 추가하려면 Homestead 디렉터리 내 `aliases` 파일을 수정하세요:

    alias c='clear'
    alias ..='cd ..'

파일을 수정한 뒤, 새 별칭을 적용하려면 `vagrant reload --provision` 명령으로 Homestead 가상머신을 재프로비저닝해야 합니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead를 업데이트하기 전에 Homestead 디렉터리에서 다음 명령으로 기존 가상머신을 제거해야 합니다:

    vagrant destroy

이후 Homestead 소스 코드를 업데이트하세요. 리포지터리를 클론한 경우, 클론한 위치에서 다음 명령을 실행하면 됩니다:

    git fetch

    git pull origin release

해당 명령은 최신 Homestead 코드와 태그를 가져온 후 최신 태그 릴리스를 체크아웃합니다. 최신 안정화 버전은 Homestead의 [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

`composer.json` 파일에 Homestead를 설치한 경우 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 다음 명령으로 의존성을 업데이트하세요:

    composer update

다음으로, `vagrant box update` 명령으로 Vagrant 박스를 업데이트합니다:

    vagrant box update

박스 업데이트 후 Homestead 추가 구성파일을 최신화하려면 Homestead 디렉터리에서 `bash init.sh`를 다시 실행하세요. 이때 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 묻는 메시지가 표시됩니다:

    // macOS / Linux...
    bash init.sh

    // Windows...
    init.bat

마지막으로, 최신 Vagrant 설치를 적용하려면 Homestead 가상머신을 재생성해야 합니다:

    vagrant up

<a name="daily-usage"></a>
## 일상적인 사용

<a name="connecting-via-ssh"></a>
### SSH로 접속하기

Homestead 디렉터리에서 `vagrant ssh` 명령을 실행하면 가상머신에 SSH 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 사이트 추가하기

Homestead 환경이 프로비저닝 및 실행된 후, 다른 Laravel 프로젝트용 Nginx 사이트를 추가하고 싶을 수 있습니다. Homestead 환경 하나에서 원하는 만큼 Laravel 프로젝트를 실행할 수 있습니다. 추가하려는 사이트를 `Homestead.yaml` 파일에 등록하세요.

    sites:
        - map: homestead.test
          to: /home/vagrant/project1/public
        - map: another.test
          to: /home/vagrant/project2/public

> {note} 사이트를 추가하기 전, 해당 프로젝트 디렉터리가 [공유 폴더](#configuring-shared-folders)로 매핑되었는지 확인하세요.

Vagrant에서 "hosts" 파일을 자동으로 관리하지 않는 경우, 새 사이트도 해당 파일에 추가해줘야 합니다. macOS 및 Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다:

    192.168.56.56  homestead.test
    192.168.56.56  another.test

사이트를 추가한 후, Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 타입

Homestead는 Laravel 기반이 아닌 프로젝트도 쉽게 동작하도록 몇 가지 "사이트 타입"을 지원합니다. 예를 들어, `statamic` 사이트 타입을 사용해 Statamic 애플리케이션을 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

지원되는 사이트 타입은: `apache`, `apigility`, `expressive`, `laravel`(기본값), `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 입니다.

<a name="site-parameters"></a>
#### 사이트 파라미터

사이트의 Nginx `fastcgi_param` 값을 `params` 지시어로 추가할 수 있습니다:

    sites:
        - map: homestead.test
          to: /home/vagrant/project1/public
          params:
              - key: FOO
                value: BAR

<a name="environment-variables"></a>
### 환경 변수

전역 환경 변수를 `Homestead.yaml` 파일에 추가하여 정의할 수 있습니다:

    variables:
        - key: APP_ENV
          value: local
        - key: FOO
          value: bar

`Homestead.yaml` 파일을 수정한 뒤에는 반드시 `vagrant reload --provision` 명령으로 다시 프로비저닝하세요. 그러면 설치된 모든 PHP 버전의 PHP-FPM 설정과 `vagrant` 사용자 환경이 갱신됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경에 포워딩됩니다:

- **HTTP:** 8000 &rarr; 80
- **HTTPS:** 44300 &rarr; 443

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩

추가로 포트를 Vagrant 박스로 전달하려면, `Homestead.yaml` 파일에 `ports` 구성을 추가하세요. 파일을 수정한 뒤, 반드시 `vagrant reload --provision` 명령을 실행하세요:

    ports:
        - send: 50000
          to: 5000
        - send: 7777
          to: 777
          protocol: udp

다음은 호스트 머신에서 Vagrant 박스로 매핑할 수 있는 추가 Homestead 서비스 포트 목록입니다:

- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailhog:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

<a name="php-versions"></a>
### PHP 버전

Homestead 6부터 하나의 가상머신에서 여러 버전의 PHP를 동시에 사용할 수 있습니다. 특별한 사이트에 사용할 PHP 버전은 `Homestead.yaml`에 지정할 수 있습니다. 사용 가능한 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0"(기본값), "8.1":

    sites:
        - map: homestead.test
          to: /home/vagrant/project1/public
          php: "7.1"

[Homestead 가상머신 내부](#connecting-via-ssh)에서, CLI를 통해 원하는 PHP 버전으로 artisan 명령을 실행할 수 있습니다:

    php5.6 artisan list
    php7.0 artisan list
    php7.1 artisan list
    php7.2 artisan list
    php7.3 artisan list
    php7.4 artisan list
    php8.0 artisan list
    php8.1 artisan list

CLI에서 기본적으로 사용할 PHP 버전 변경은 다음 명령으로 가능합니다(Homestead 가상머신 내부):

    php56
    php70
    php71
    php72
    php73
    php74
    php80
    php81

<a name="connecting-to-databases"></a>
### 데이터베이스 연결

MySQL과 PostgreSQL 모두에 대해 `homestead`라는 데이터베이스가 기본 설정되어 있습니다. 로컬 호스트 머신의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL에 접속하려면, 각각 `127.0.0.1`의 포트 `33060`(MySQL), `54320`(PostgreSQL)으로 연결하세요. 두 데이터베이스의 사용자명과 비밀번호는 `homestead` / `secret`입니다.

> {note} 호스트 머신에서 접속할 때만 이렇게 포트를 사용하세요. Laravel 애플리케이션의 `database` 구성에서는 기본 포트(3306, 5432)를 사용하면 됩니다. 애플리케이션은 _가상머신 내부_에서 실행되기 때문입니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 `vagrant destroy`로 가상머신 삭제 시 데이터베이스를 자동 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상 또는 `vagrant-triggers` 플러그인이 필요합니다. 자동 백업 활성화는 `Homestead.yaml` 파일에 다음을 추가하면 됩니다:

    backup: true

구성이 완료되면 `vagrant destroy` 명령 실행 시 데이터베이스가 `mysql_backup` 및 `postgres_backup` 디렉터리로 내보내집니다(위치는 Homestead 설치 폴더 또는 프로젝트 루트).

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel은 [크론 작업 스케줄링](/docs/{{version}}/scheduling)을 편리하게 제공합니다. 즉, Artisan의 `schedule:run` 명령을 분마다 실행하여 예약된 작업을 자동으로 실행할 수 있습니다.

Homestead 사이트에 대해 `schedule` 옵션을 `true`로 지정하면 해당 사이트의 크론 작업이 자동 등록됩니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상머신의 `/etc/cron.d` 디렉터리에 저장됩니다.

<a name="configuring-mailhog"></a>
### MailHog 설정

[MailHog](https://github.com/mailhog/MailHog)는 아웃바운드 이메일을 실제 수신자에게 전송하지 않고 안전하게 확인할 수 있게 해줍니다. 사용하려면 `.env` 파일을 다음과 같이 변경하세요:

    MAIL_MAILER=smtp
    MAIL_HOST=localhost
    MAIL_PORT=1025
    MAIL_USERNAME=null
    MAIL_PASSWORD=null
    MAIL_ENCRYPTION=null

MailHog 설정을 완료한 후, 대시보드는 `http://localhost:8025`에서 접근할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정

[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 오브젝트 스토리지 서버입니다. 설치하려면, [기능 옵션](#installing-optional-features) 섹션에 다음을 추가하세요:

    minio: true

기본적으로 Minio는 9600포트에서 동작합니다. 컨트롤 패널은 `http://localhost:9600`에서 확인할 수 있으며, 기본 access key는 `homestead`, 비밀 키는 `secretkey`입니다. region은 항상 `us-east-1`로 사용하세요.

애플리케이션의 `config/filesystems.php`에서 S3 디스크 구성을 아래와 같이 맞춰주세요. `use_path_style_endpoint` 옵션과 `url`을 `endpoint`로 변경해야 합니다:

    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
        'endpoint' => env('AWS_URL'),
        'use_path_style_endpoint' => true,
    ]

또한 `.env` 파일에 다음 내용을 추가하세요:

```bash
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml` 파일에 `buckets` 지시어를 추가하세요. 버킷을 정의한 후 터미널에서 `vagrant reload --provision` 명령을 실행하세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원되는 `policy` 값은: `none`, `download`, `upload`, `public` 입니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 테스트를 Homestead 내에서 실행하려면 [`webdriver` 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

활성화 후 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기

동료 또는 고객과 작업 중인 개발 환경을 공유하고 싶을 때가 있습니다. Vagrant는 `vagrant share` 명령으로 환경 공유를 지원하지만, `Homestead.yaml`에 여러 사이트가 설정된 경우 동작하지 않습니다.

이를 해결하기 위해 Homestead는 자체 `share` 명령을 제공합니다. [Homestead 가상머신에 SSH로 접속](#connecting-via-ssh) 후 아래와 같이 `share homestead.test` 명령을 실행하세요. 필요한 경우 `homestead.test` 대신 다른 설정된 사이트명을 사용해도 됩니다:

    share homestead.test

명령 실행 후, ngrok 화면이 나타나고 공유된 사이트의 공개 URL과 로그를 확인할 수 있습니다. 특정 region/subdomain 등 커스텀 ngrok 옵션도 아래처럼 지정할 수 있습니다:

    share homestead.test -region=eu -subdomain=laravel

> {note} Vagrant로 인터넷에 가상머신을 노출하는 것이므로, 사용 시 항상 보안에 유의하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 & 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug를 통한 웹 요청 디버깅

Homestead에는 [Xdebug](https://xdebug.org)를 통한 스텝 디버깅이 지원됩니다. 예를 들어 브라우저에서 페이지에 접근하면 PHP가 IDE와 연결되어 코드 실행 과정을 검사 및 수정할 수 있습니다.

Xdebug는 기본적으로 실행 중이며, 연결 요청을 대기 중입니다. CLI에서 Xdebug를 활성화하려면 가상머신 내에서 `sudo phpenmod xdebug` 명령을 실행하세요. 그 다음 IDE에서 디버깅을 활성화하고, 브라우저에 확장 프로그램 또는 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)을 이용해 Xdebug 트리거를 설정하세요.

> {note} Xdebug가 활성화되면 PHP 처리 속도가 상당히 느려집니다. 비활성화하려면 가상머신 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버로 요청을 보내는 기능 테스트를 디버깅할 때, 테스트 코드를 변경해서 헤더/쿠키 등을 추가하는 대신 자동 시작이 더 편리할 수 있습니다. Xdebug를 항상 자동 시작하려면 가상머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 아래와 같이 변경하세요:

```ini
; Homestead.yaml의 IP 대역이 다르다면 주소가 다를 수 있습니다.
xdebug.remote_host = 192.168.10.1
xdebug.remote_autostart = 1
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상머신 내에서 `xphp` 별칭을 사용하세요:

    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
### Blackfire를 통한 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션 프로파일링 서비스입니다. 호출 그래프 및 타임라인 등, 인터랙티브 UI로 프로파일 데이터를 시각화합니다. 개발, 스테이징, 프로덕션 환경 모두에서 사용할 수 있고, 사용자에게는 성능 저하가 없습니다. 또한, Blackfire는 코드 및 php.ini 설정에 대한 성능/품질/보안 체크도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 연동할 수 있는 오픈소스 웹 크롤링/테스트/스크래핑 툴입니다.

Blackfire를 활성화하려면 `Homestead.yaml` 구성 파일에 아래처럼 "features" 설정을 추가하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 및 클라이언트 자격 증명은 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 다양한 방식의 프로파일링이 가능합니다. 자세한 내용은 [Blackfire 공식 문서](https://blackfire.io/docs/cookbooks/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성으로 가상머신의 네트워크 인터페이스를 설정할 수 있습니다. 원하는 만큼 인터페이스를 추가할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지 네트워크](https://www.vagrantup.com/docs/networking/public_network.html) 인터페이스를 활성화하려면, `type`을 `public_network`로 바꾸고 추가 설정을 입력하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://www.vagrantup.com/docs/networking/public_network.html)를 활성화하려면, 구성에서 `ip` 옵션을 제거하세요:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<a name="extending-homestead"></a>
## Homestead 확장

Homestead 디렉터리의 루트에 있는 `after.sh` 스크립트로 Homestead를 확장할 수 있습니다. 필요한 셸 명령을 이 파일에 자유롭게 추가하여 가상머신을 원하는 대로 맞춤화 할 수 있습니다.

우분투에서 패키지 설치 시 기존 설정 파일을 유지할지 묻는 메시지가 나오지 않도록, 아래 형식으로 설치하면 Homestead가 이미 작성한 설정을 덮어쓰는 일이 없습니다:

    sudo apt-get -y \
        -o Dpkg::Options::="--force-confdef" \
        -o Dpkg::Options::="--force-confold" \
        install package-name

<a name="user-customizations"></a>
### 사용자 맞춤 설정

팀과 함께 Homestead를 사용할 경우, 개인의 개발 스타일에 맞게 Homestead를 조정하고 싶을 수 있습니다. 이를 위해 `Homestead.yaml` 파일과 동일한 위치에 `user-customizations.sh` 파일을 추가해 원하는 수정을 할 수 있습니다(`user-customizations.sh` 파일은 버전관리에서 제외해야 합니다).

<a name="provider-specific-settings"></a>
## 프로바이더별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver`를 `on`으로 설정해 호스트 OS의 DNS 설정을 사용합니다. 동작을 바꾸고 싶다면 `Homestead.yaml`에 다음처럼 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

<a name="symbolic-links-on-windows"></a>
#### Windows에서 심볼릭 링크

Windows에서 심볼릭 링크가 제대로 동작하지 않는다면, `Vagrantfile`에 아래 블록을 추가하세요:

```ruby
config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```
