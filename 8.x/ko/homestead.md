# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant 박스 시작하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상 사용법](#daily-usage)
    - [SSH로 연결하기](#connecting-via-ssh)
    - [추가 사이트 추가하기](#adding-additional-sites)
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
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 PHP 개발 경험 전체를 즐겁게 만드는 것을 목표로 하며, 로컬 개발 환경도 그 중 포함됩니다. [Laravel Homestead](https://github.com/laravel/homestead)는 PHP, 웹 서버 및 기타 서버 소프트웨어를 로컬에 설치할 필요 없이 훌륭한 개발 환경을 제공하는 공식적으로 패키징된 Vagrant 박스입니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 쉽고 우아하게 관리하고 구성할 수 있게 해줍니다. Vagrant 박스는 완전히 폐기 가능하여 문제가 생기면 몇 분 만에 박스를 삭제하고 다시 만들 수 있습니다.

Homestead는 Windows, macOS, Linux 시스템에서 실행되며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!NOTE]
> Windows 사용자라면 하드웨어 가상화(VT-x)를 BIOS 설정에서 활성화해야 할 수도 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우, VT-x에 접근하기 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어 (Included Software)

- Ubuntu 20.04
- Git
- PHP 8.1, 8.0, 7.4, 7.3, 7.2, 7.1, 7.0, 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 13
- Composer
- Node (Yarn, Bower, Grunt, Gulp 포함)
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
### 선택적 소프트웨어 (Optional Software)

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
- Webdriver & Laravel Dusk 유틸리티

<a name="installation-and-setup"></a>
## 설치 및 설정 (Installation & Setup)

<a name="first-steps"></a>
### 첫 단계 (First Steps)

Homestead 환경을 시작하기 전에 [Vagrant](https://www.vagrantup.com/downloads.html)와 아래 지원하는 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어들은 모든 주요 운영체제에서 사용하기 쉬운 비주얼 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 하며, 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치하기 (Installing Homestead)

Homestead 저장소를 호스트 컴퓨터에 클론하여 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 할 것이기에, 이 저장소를 "홈" 디렉토리 내 `Homestead` 폴더에 클론하는 것을 권장합니다. 본 문서에서는 이를 "Homestead 디렉토리"라 칭할 것입니다:

```bash
git clone https://github.com/laravel/homestead.git ~/Homestead
```

저장소를 클론한 후 `release` 브랜치를 체크아웃하세요. 이 브랜치에는 항상 최신 안정 버전 Homestead가 포함되어 있습니다:

```
cd ~/Homestead

git checkout release
```

다음으로 `bash init.sh` 명령어를 실행해 `Homestead.yaml` 설정 파일을 생성하세요. 이 파일에 Homestead 설치에 필요한 모든 설정을 구성하게 됩니다. 이 파일은 Homestead 디렉토리에 생성됩니다:

```
// macOS / Linux...
bash init.sh

// Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정 (Configuring Homestead)

<a name="setting-your-provider"></a>
#### 프로바이더 설정 (Setting Your Provider)

`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 프로바이더를 지정합니다: `virtualbox` 또는 `parallels`입니다:

```
provider: virtualbox
```

> [!NOTE]
> Apple Silicon 사용자의 경우 `Homestead.yaml` 에 `box: laravel/homestead-arm` 를 추가해야 합니다. Apple Silicon에는 Parallels 프로바이더가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 구성 (Configuring Shared Folders)

`Homestead.yaml`의 `folders` 속성은 Homestead 환경과 공유할 폴더 리스트를 설정합니다. 이 폴더 내 파일에 변경이 생기면 로컬과 Homestead 가상 머신 간에 동기화됩니다. 필요한 만큼 여러 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!NOTE]
> Windows 사용자는 `~/` 경로 대신 `C:\Users\user\Code\project1` 같은 전체 경로를 사용해야 합니다.

각 애플리케이션은 별도의 폴더 맵핑에 연결하는 것이 좋으며, 모든 앱을 포함하는 단일 대형 디렉토리를 매핑하는 것은 피해야 합니다. 폴더가 크고 파일 수가 많은 경우, 가상 머신이 모든 디스크 IO를 처리해야 해서 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!NOTE]
> Homestead 사용 시 절대 `.` (현재 디렉토리) 를 마운트하지 마십시오. 이 경우 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않아 선택적 기능이 정상 동작하지 않을 수 있습니다.

[NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html)를 사용하려면 폴더 설정에 `type` 옵션을 추가하세요:

```
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!NOTE]
> Windows에서 NFS를 사용할 경우 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려하세요. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉토리의 올바른 사용자/그룹 권한을 유지합니다.

또한, Vagrant의 [동기화 폴더 옵션](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)을 `options` 키 아래에 추가할 수 있습니다:

```
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

Nginx를 잘 모른다고 걱정하지 마십시오. `Homestead.yaml` 파일의 `sites` 속성을 사용하면 Homestead 환경 내 폴더에 "도메인"을 쉽게 매핑할 수 있습니다. `Homestead.yaml`에는 샘플 사이트 설정이 포함되어 있으며, 원하는 만큼 여러 사이트를 추가할 수 있습니다. Homestead는 여러 Laravel 애플리케이션을 위한 편리한 가상 환경 역할을 합니다:

```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

`sites` 설정을 바꾼 후에는 Homestead 가상 머신에서 Nginx 구성을 업데이트하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!NOTE]
> Homestead 스크립트는 가능한 재실행해도 영향을 주지 않게(idempotent) 설계되어 있습니다. 그러나 프로비저닝 문제 발생 시 `vagrant destroy && vagrant up` 명령으로 가상 머신을 삭제 후 재생성하세요.

<a name="hostname-resolution"></a>
#### 호스트명 해석 (Hostname Resolution)

Homestead는 `mDNS`를 사용해 자동으로 호스트명 해석을 제공합니다. `Homestead.yaml`에 `hostname: homestead`를 설정하면 호스트는 `homestead.local`로 접근 가능합니다. macOS, iOS, Linux 데스크톱 배포판에는 기본적으로 `mDNS`가 포함되어 있지만, Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명은 [프로젝트별 설치](#per-project-installation)와 가장 잘 어울립니다. 단일 Homestead 인스턴스에서 여러 사이트를 운영한다면, 호스트 기기의 `hosts` 파일에 각 도메인을 추가할 수 있습니다. 이 파일은 macOS/Linux에선 `/etc/hosts`, Windows에선 `C:\Windows\System32\drivers\etc\hosts`에 위치합니다. 다음과 같이 추가합니다:

```
192.168.56.56  homestead.test
```

`Homestead.yaml`에 설정된 IP 주소와 일치하는지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 시작하면 웹 브라우저에서 해당 사이트에 접근할 수 있습니다:

```bash
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정 (Configuring Services)

Homestead는 기본적으로 여러 서비스를 시작하지만, 프로비저닝 중 활성화 또는 비활성화를 설정할 수 있습니다. 예를 들어 PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml`의 `services` 옵션에서 조정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

`enabled`와 `disabled` 안에 명시된 순서에 따라 서비스가 시작 혹은 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 시작하기 (Launching The Vagrant Box)

`Homestead.yaml`을 원하는 대로 수정한 후, Homestead 디렉토리에서 `vagrant up` 명령어를 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동으로 구성합니다.

가상 머신을 삭제하려면 `vagrant destroy` 명령어를 사용하세요.

<a name="per-project-installation"></a>
### 프로젝트별 설치 (Per Project Installation)

Homestead를 전역으로 설치하여 모든 프로젝트에서 동일한 가상 머신을 공유하는 대신, 각각의 프로젝트에 별도로 Homestead 인스턴스를 설정할 수 있습니다. 프로젝트별 설치는 `Vagrantfile`을 프로젝트와 함께 배포하여, 클론 후 다른 개발자가 바로 `vagrant up` 할 수 있게 하는 장점이 있습니다.

Composer 패키지 매니저를 통해 프로젝트에 Homestead를 설치합니다:

```bash
composer require laravel/homestead --dev
```

설치가 완료되면 Homestead의 `make` 명령어로 프로젝트의 루트에 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 이 명령어는 `Homestead.yaml` 내의 `sites` 및 `folders` 지시문을 자동 설정합니다:

```
// macOS / Linux...
php vendor/bin/homestead make

// Windows...
vendor\\bin\\homestead make
```

그 다음 터미널에서 `vagrant up` 명령어를 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 [호스트명 해석](#hostname-resolution)을 사용하지 않는다면, `homestead.test` 또는 원하는 도메인을 `/etc/hosts` 파일에 추가하는 것을 잊지 마십시오.

<a name="installing-optional-features"></a>
### 선택적 기능 설치 (Installing Optional Features)

선택적 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치됩니다. 대부분의 기능은 부울값으로 활성화/비활성화할 수 있으며, 일부는 여러 구성 옵션을 가질 수 있습니다:

```
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
```

<a name="elasticsearch"></a>
#### Elasticsearch

정확한 버전 번호(major.minor.patch)로 지원되는 Elasticsearch 버전을 지정할 수 있습니다. 기본 설치로 'homestead' 클러스터가 생성됩니다. Elasticsearch가 운영체제 메모리의 절반 이상 사용하지 않도록 해야 하므로 Homestead 가상 머신에 Elasticsearch 할당량의 두 배 이상 메모리가 있어야 합니다.

> [!TIP]
> Elasticsearch를 맞춤 설정하는 방법은 [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL의 대체제 역할을 하므로 애플리케이션 데이터베이스 설정에선 여전히 `mysql` 데이터베이스 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치 시, 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치 시, 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다. Neo4j 브라우저는 웹 브라우저에서 `http://homestead.test:7474`로 엑세스할 수 있습니다. `7687` (Bolt), `7474` (HTTP), `7473` (HTTPS) 포트가 Neo4j 클라이언트 요청을 처리할 준비가 되어 있습니다.

<a name="aliases"></a>
### 별칭 (Aliases)

Homestead 가상 머신에 Bash 별칭을 추가하려면 Homestead 디렉토리 내 `aliases` 파일을 수정하세요:

```
alias c='clear'
alias ..='cd ..'
```

별칭 파일을 수정한 후에는 `vagrant reload --provision` 명령어로 Homestead 가상 머신을 다시 프로비저닝하여 변경 사항이 적용되도록 해야 합니다.

<a name="updating-homestead"></a>
## Homestead 업데이트 (Updating Homestead)

업데이트를 시작하기 전에 다음 명령어로 현재 가상 머신을 삭제해야 합니다:

```
vagrant destroy
```

그다음 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면 클론한 위치에서 다음 명령어를 실행하세요:

```
git fetch

git pull origin release
```

이 명령어는 GitHub 저장소에서 최신 Homestead 코드를 가져오고 최신 태그를 확인한 뒤 최신 안정 버전을 체크아웃합니다. 최신 안정 버전은 Homestead [GitHub 릴리즈 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

`composer.json`으로 설치한 경우, `"laravel/homestead": "^12"`가 포함되어 있는지 확인한 뒤 의존성을 업데이트합니다:

```
composer update
```

그 다음 `vagrant box update` 명령어로 Vagrant 박스를 최신 상태로 만듭니다:

```
vagrant box update
```

Vagrant 박스 업데이트 후, Homestead 추가 설정 파일을 갱신하기 위해 Homestead 디렉토리에서 `bash init.sh` 명령어를 실행하세요. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일 덮어쓸지 여부를 묻습니다:

```
// macOS / Linux...
bash init.sh

// Windows...
init.bat
```

마지막으로, 최신 Vagrant 설치를 사용하기 위해 Homestead 가상 머신을 다시 생성하세요:

```
vagrant up
```

<a name="daily-usage"></a>
## 일상 사용법 (Daily Usage)

<a name="connecting-via-ssh"></a>
### SSH로 연결하기 (Connecting Via SSH)

Homestead 디렉토리에서 `vagrant ssh` 명령어를 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가하기 (Adding Additional Sites)

Homestead 환경이 프로비저닝되고 실행 중이라면, 다른 Laravel 프로젝트를 위한 추가 Nginx 사이트를 설정할 수 있습니다. 하나의 Homestead 환경에서 원하는 만큼 Laravel 프로젝트를 실행 가능합니다. 추가 사이트를 `Homestead.yaml`에 다음과 같이 추가하세요:

```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!NOTE]
> 사이트 추가 전에 해당 프로젝트 디렉토리에 대한 [폴더 매핑](#configuring-shared-folders)이 올바르게 설정되었는지 반드시 확인하세요.

Vagrant가 자동으로 "hosts" 파일을 관리하지 않으면, 새 사이트를 해당 파일에 추가해줘야 할 수도 있습니다. macOS/Linux는 `/etc/hosts`, Windows는 `C:\Windows\System32\drivers\etc\hosts`에 위치합니다:

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트 추가를 마쳤다면 Homestead 디렉토리에서 `vagrant reload --provision` 명령으로 설정을 반영하세요.

<a name="site-types"></a>
#### 사이트 유형 (Site Types)

Homestead는 Laravel 프로젝트가 아닌 다른 유형의 사이트도 쉽게 실행하도록 여러 "사이트 유형"을 지원합니다. 예를 들어, Statamic 애플리케이션을 Homestead에 다음과 같이 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 유형은 `apache`, `apigility`, `expressive`, `laravel` (기본값), `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`입니다.

<a name="site-parameters"></a>
#### 사이트 매개변수 (Site Parameters)

Nginx의 추가 `fastcgi_param` 값을 `params` 지시문을 통해 추가할 수 있습니다:

```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수 (Environment Variables)

전역 환경 변수를 `Homestead.yaml`에 다음과 같이 정의할 수 있습니다:

```
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

파일 수정 후 `vagrant reload --provision` 명령어를 실행해 재프로비저닝하면, 설치된 모든 PHP 버전의 PHP-FPM 구성과 `vagrant` 유저 환경에 이 설정이 반영됩니다.

<a name="ports"></a>
### 포트 (Ports)

기본적으로 다음 포트가 Homestead 환경으로 포워딩됩니다:

- **HTTP:** 8000 → 80
- **HTTPS:** 44300 → 443

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩 (Forwarding Additional Ports)

추가 포트를 포워딩하려면 `Homestead.yaml`에 `ports` 설정을 추가하세요. 파일 변경 후 `vagrant reload --provision`으로 재프로비저닝해야 합니다:

```
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

호스트 머신에서 Vagrant 박스에 매핑할 수 있는 Homestead 서비스의 추가 포트는 다음과 같습니다:

- **SSH:** 2222 → 22
- **ngrok UI:** 4040 → 4040
- **MySQL:** 33060 → 3306
- **PostgreSQL:** 54320 → 5432
- **MongoDB:** 27017 → 27017
- **Mailhog:** 8025 → 8025
- **Minio:** 9600 → 9600

<a name="php-versions"></a>
### PHP 버전 (PHP Versions)

Homestead 6부터 하나의 가상 머신에서 여러 PHP 버전을 사용할 수 있습니다. `Homestead.yaml` 파일에서 각 사이트에 사용할 PHP 버전을 지정하세요. 사용 가능한 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0"(기본), "8.1"입니다:

```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내](#connecting-via-ssh)에서는 CLI에서 다음처럼 원하는 PHP 버전을 사용할 수 있습니다:

```
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
```

CLI 기본 PHP 버전은 가상 머신 내에서 다음 명령어로 변경할 수 있습니다:

```
php56
php70
php71
php72
php73
php74
php80
php81
```

<a name="connecting-to-databases"></a>
### 데이터베이스 연결 (Connecting To Databases)

MySQL과 PostgreSQL 모두 기본적으로 `homestead` 데이터베이스가 설정되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 연결할 땐 `127.0.0.1` 주소에 MySQL은 포트 `33060`, PostgreSQL은 포트 `54320`을 사용하세요. 사용자명과 비밀번호는 둘 다 `homestead` / `secret`입니다.

> [!NOTE]
> 호스트 머신에서 연결할 때만 기본이 아닌 포트를 사용해야 하며, Laravel 애플리케이션이 가상 머신 내에서 실행되므로 Laravel 설정 파일에는 기본 3306, 5432 포트를 사용해야 합니다.

<a name="database-backups"></a>
### 데이터베이스 백업 (Database Backups)

Homestead는 가상 머신 삭제 시 자동으로 데이터베이스 백업을 할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요하며, 이전 버전을 쓰면 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml`에 다음을 추가하세요:

```
backup: true
```

설정 후 `vagrant destroy` 명령어 실행 시 데이터베이스가 `mysql_backup` 와 `postgres_backup` 폴더에 내보내집니다. 해당 폴더는 Homestead 설치 폴더 또는 [프로젝트별 설치](#per-project-installation)시 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정 (Configuring Cron Schedules)

Laravel은 단일 `schedule:run` Artisan 명령어를 통해 간편하게 [크론 작업을 예약](/docs/{{version}}/scheduling)할 수 있습니다. 이 명령은 `App\Console\Kernel` 클래스에서 정의된 스케줄을 검사해 실행할 작업을 결정합니다.

Homestead 사이트에 대해 `schedule:run` 명령을 동작시키려면, 사이트 정의에 `schedule` 옵션을 `true`로 설정하면 됩니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

사이트의 크론 작업은 가상 머신 `/etc/cron.d` 디렉토리에 등록됩니다.

<a name="configuring-mailhog"></a>
### MailHog 설정 (Configuring MailHog)

[MailHog](https://github.com/mailhog/MailHog)는 아웃고잉 이메일을 가로채 실제 송신 없이 내용을 확인할 수 있게 해줍니다. 설정을 시작하려면 애플리케이션 `.env` 파일에서 다음 메일 설정으로 변경하세요:

```
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

MailHog가 구성되면 `http://localhost:8025`에서 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정 (Configuring Minio)

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 가진 오픈소스 오브젝트 스토리지 서버입니다. Minio를 설치하려면 `features` 섹션에 다음 구성을 추가하세요:

```
minio: true
```

기본 포트는 9600이며, `http://localhost:9600`을 통해 Minio 제어판에 접속할 수 있습니다. 기본 액세스 키는 `homestead`, 기본 비밀 키는 `secretkey`입니다. 접속 시에는 항상 `us-east-1` 지역을 사용하세요.

Minio를 사용하려면 애플리케이션 `config/filesystems.php`에서 S3 디스크 설정을 다음과 같이 조정해야 합니다. `use_path_style_endpoint` 옵션을 추가하고, `url` 키를 `endpoint`로 변경합니다:

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

그리고 `.env` 파일에는 다음 옵션들이 포함되어 있어야 합니다:

```bash
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시문을 추가한 후, 터미널에서 `vagrant reload --provision` 명령어를 실행하세요:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원하는 `policy` 값은 `none`, `download`, `upload`, `public` 입니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 테스트를 Homestead에서 실행하려면 Homestead 설정에서 [`webdriver` 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

기능 활성화 후 터미널에서 `vagrant reload --provision`을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기 (Sharing Your Environment)

작업 중인 내용을 동료나 클라이언트와 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령어로 기본 지원하지만, `Homestead.yaml`에 여러 사이트가 설정되어 있으면 작동하지 않습니다.

이 문제 해결을 위해 Homestead는 자체 `share` 명령어를 제공합니다. Homestead 가상 머신에 [SSH로 접속](#connecting-via-ssh)한 후 `share homestead.test` 명령어를 실행하면 `Homestead.yaml` 설정의 `homestead.test` 사이트가 공유됩니다. 이름 대신 다른 설정된 사이트명을 쓸 수 있습니다:

```
share homestead.test
```

명령 실행 후 ngrok 인터페이스가 나타나고, 활동 로그 및 공개 URL이 표시됩니다. 지역, 서브도메인 또는 기타 ngrok 옵션을 지정하려면 다음과 같이 명령어에 추가하세요:

```
share homestead.test -region=eu -subdomain=laravel
```

> [!NOTE]
> Vagrant는 본질적으로 안전하지 않으므로 `share` 명령 실행 시 가상 머신이 인터넷에 노출된다는 점을 꼭 기억하세요.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링 (Debugging & Profiling)

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅 (Debugging Web Requests With Xdebug)

Homestead는 [Xdebug](https://xdebug.org)를 활용한 단계별 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지를 열면 PHP가 IDE에 연결되어 실행 중인 코드를 검사 및 수정할 수 있습니다.

기본적으로 Xdebug는 이미 활성화되어 연결을 기다리고 있습니다. CLI에서 Xdebug를 켤 필요가 있다면 Homestead 가상 머신 내에서 다음 명령을 실행하세요:

```
sudo phpenmod xdebug
```

그 후 IDE의 안내에 따라 디버깅을 활성화하고, 브라우저 확장 혹은 [북마클릿](https://www.jetbrains.com/phpstorm/marklets/)으로 Xdebug를 트리거 설정하세요.

> [!NOTE]
> Xdebug는 PHP 실행 속도를 크게 느리게 할 수 있습니다. 비활성화하려면 가상 머신 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작 설정

기능 테스트에서 웹 서버 요청에 대해 디버깅을 자동으로 시작하려면, Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하고 아래 설정을 추가하세요:

```ini
; Homestead.yaml에 다른 서브넷이 지정된 경우 주소가 달라질 수 있습니다...
xdebug.remote_host = 192.168.10.1
xdebug.remote_autostart = 1
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅 (Debugging CLI Applications)

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 셸 별칭을 사용하세요:

```
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링 (Profiling Applications with Blackfire)

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 앱 프로파일링 서비스입니다. 호출 그래프와 타임라인으로 프로파일 데이터를 시각화하며, 개발, 스테이징, 프로덕션에서 사용자에 부담 없이 사용할 수 있습니다. 코드, `php.ini` 설정에 대한 성능, 품질, 보안 검사 기능도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 웹 크롤링, 웹 테스트, 웹 스크래핑을 위한 오픈 소스 도구로 Blackfire와 함께 프로파일링 시나리오를 스크립트할 수 있습니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 `features`에 다음을 추가하세요:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

서버 및 클라이언트 인증 정보는 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 프로파일링 옵션을 제공합니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/cookbooks/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스 (Network Interfaces)

`Homestead.yaml`의 `networks` 속성으로 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 인터페이스를 지정할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지](https://www.vagrantup.com/docs/networking/public_network.html) 인터페이스를 활성화하려면 `bridge` 설정을 추가하고 네트워크 타입을 `public_network`로 설정하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://www.vagrantup.com/docs/networking/public_network.html)를 사용하려면 `ip` 옵션을 제거하면 됩니다:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<a name="extending-homestead"></a>
## Homestead 확장하기 (Extending Homestead)

Homestead 디렉토리 루트에 있는 `after.sh` 스크립트를 통해 Homestead를 확장할 수 있습니다. 이 파일에 필요한 셸 명령어를 추가하여 가상 머신을 적절히 구성하고 맞춤설정할 수 있습니다.

Ubuntu는 패키지 설치 시 기존 설정 파일 유지 여부를 묻습니다. 이를 방지하려면 다음 명령어 옵션을 사용하여 패키지를 설치하세요. 이렇게 하면 Homestead에서 이전에 작성한 설정이 덮어쓰여지지 않습니다:

```
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 맞춤 설정 (User Customizations)

팀과 Homestead를 사용할 때 개인 개발 스타일에 맞게 Homestead를 조정하고 싶다면, Homestead 디렉토리( `Homestead.yaml` 파일과 같은 위치)에 `user-customizations.sh` 파일을 만들고 원하는 설정을 추가하세요. 단, 이 파일은 버전 관리에 포함시키지 않는 것이 좋습니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정 (Provider Specific Settings)

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 옵션을 `on`으로 설정합니다. 이는 Homestead가 호스트 OS의 DNS 설정을 사용할 수 있게 해줍니다. 이 동작을 변경하려면 `Homestead.yaml` 파일에 다음 옵션을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

<a name="symbolic-links-on-windows"></a>
#### Windows에서 심볼릭 링크 문제 해결

Windows에서 심볼릭 링크가 제대로 작동하지 않는 경우, `Vagrantfile`에 다음 블록을 추가하여 문제를 해결할 수 있습니다:

```ruby
config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```