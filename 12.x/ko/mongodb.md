# MongoDB

- [소개](#introduction)
- [설치](#installation)
    - [MongoDB 드라이버](#mongodb-driver)
    - [MongoDB 서버 시작](#starting-a-mongodb-server)
    - [Laravel MongoDB 패키지 설치](#install-the-laravel-mongodb-package)
- [설정](#configuration)
- [기능](#features)

<a name="introduction"></a>
## 소개

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석 또는 IoT에 유용)와 높은 가용성(자동 장애 조치가 가능한 복제 세트 구성의 용이성)으로 널리 사용됩니다. 또한 데이터베이스 샤딩을 통해 수평 확장도 간편하며, 집계, 텍스트 검색, 지리 공간 쿼리 등을 위한 강력한 쿼리 언어도 제공합니다.

MongoDB는 SQL 데이터베이스처럼 행(row)이나 열(column)로 구성된 테이블에 데이터를 저장하는 대신, 각 레코드를 BSON이라는 데이터의 이진 표현 형식으로 문서(document)로 저장합니다. 애플리케이션은 이 정보를 JSON 형식으로 가져올 수 있습니다. 문서, 배열, 내장 문서, 바이너리 데이터 등 다양한 데이터 타입을 지원합니다.

MongoDB를 Laravel에서 사용하려면 Composer를 통해 `mongodb/laravel-mongodb` 패키지를 설치 및 사용하는 것을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 관리하고 있으며, PHP는 기본적으로 MongoDB 드라이버를 통해 MongoDB를 지원하지만, [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지는 Eloquent 및 기타 Laravel 기능과의 통합을 더 풍부하게 제공합니다:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치

<a name="mongodb-driver"></a>
### MongoDB 드라이버

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장(extension)이 필요합니다. 만약 [Laravel Herd](https://herd.laravel.com)를 이용해 로컬 환경에서 개발 중이거나, `php.new`를 통해 PHP를 설치한 경우라면 이 확장이 이미 시스템에 설치되어 있을 수 있습니다. 수동으로 확장을 설치하려면 PECL을 통해 다음과 같이 설치할 수 있습니다:

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 대한 자세한 내용은 [MongoDB PHP 확장 설치 안내](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작

MongoDB Community Server는 로컬에서 MongoDB를 실행할 수 있게 해주며, Windows, macOS, Linux 또는 Docker 컨테이너로 설치가 가능합니다. MongoDB 설치 방법은 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버에 대한 연결 문자열은 `.env` 파일에 다음과 같이 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 사용해보세요.
애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접근하려면, [클러스터의 네트워크 설정에서 자신의 IP 주소를 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다. 이는 프로젝트의 IP 접근 리스트에 추가해야 합니다.

MongoDB Atlas 연결 문자열 역시 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치

마지막으로 Composer를 사용해 Laravel MongoDB 패키지를 설치합니다:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> 만약 `mongodb` PHP 확장이 설치되어 있지 않다면, 이 패키지 설치는 실패합니다. PHP 설정은 CLI와 웹 서버에서 다를 수 있으므로, 두 환경 모두에서 확장이 활성화되어 있는지 확인하세요.

<a name="configuration"></a>
## 설정

애플리케이션의 `config/database.php` 설정 파일에서 MongoDB 연결을 구성할 수 있습니다. 이 파일의 `connections` 배열에 `mongodb` 드라이버를 사용하는 연결을 추가하세요:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],
```

<a name="features"></a>
## 기능

설정이 완료되면, 애플리케이션에서 `mongodb` 패키지와 데이터베이스 연결을 사용하여 다양한 강력한 기능을 활용할 수 있습니다:

- [Eloquent 사용](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/) 시, 모델은 MongoDB 컬렉션에 저장됩니다. 표준 Eloquent 기능 외에도, Laravel MongoDB 패키지는 내장 관계(embedded relationships)와 같은 추가 기능을 제공합니다. 패키지는 또한 MongoDB 드라이버에 직접 접근할 수 있도록 하여, Raw 쿼리 및 집계 파이프라인 등의 작업을 실행할 수 있습니다.
- 쿼리 빌더를 사용하여 [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/)이 가능합니다.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)는 TTL 인덱스와 같은 MongoDB 기능을 활용하여 만료된 캐시 항목을 자동으로 제거하도록 최적화되어 있습니다.
- `mongodb` 큐 드라이버를 사용해 [큐 작업 배포 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/)가 가능합니다.
- [GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/)와 함께 [GridFS에 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/)이 가능합니다.
- 데이터베이스 연결이나 Eloquent를 사용하는 대부분의 서드파티 패키지는 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel을 계속해서 배우고 싶다면, MongoDB의 [빠른 시작 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.