# MongoDB

- [소개](#introduction)
- [설치](#installation)
    - [MongoDB 드라이버](#mongodb-driver)
    - [MongoDB 서버 시작하기](#starting-a-mongodb-server)
    - [Laravel MongoDB 패키지 설치하기](#install-the-laravel-mongodb-package)
- [설정](#configuration)
- [기능](#features)

<a name="introduction"></a>
## 소개 (Introduction)

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하 처리(분석이나 IoT에 유용)와 높은 가용성(자동 장애 조치가 가능한 레플리카 세트 설정 용이성) 때문에 널리 사용됩니다. 또한 데이터베이스를 수평 확장할 수 있도록 샤딩이 쉽고, 집계, 텍스트 검색, 지리 공간 쿼리 등을 수행할 수 있는 강력한 쿼리 언어를 제공합니다.

SQL 데이터베이스처럼 행과 열의 테이블에 데이터를 저장하는 대신, MongoDB의 각 레코드는 BSON(Binary JSON) 형식으로 표현된 문서(document)입니다. 애플리케이션은 이 데이터를 JSON 형식으로 가져올 수 있습니다. MongoDB는 문서, 배열, 중첩 문서, 바이너리 데이터 등 다양한 데이터 타입을 지원합니다.

Laravel에서 MongoDB를 사용하기 전에, Composer를 통해 `mongodb/laravel-mongodb` 패키지를 설치하여 사용하는 것을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 유지 관리하며, PHP의 MongoDB 드라이버로는 기본 지원되지만, 이 패키지는 Eloquent와 그 외 Laravel 기능들과의 통합을 더욱 풍부하게 제공합니다:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치 (Installation)

<a name="mongodb-driver"></a>
### MongoDB 드라이버 (MongoDB Driver)

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장 모듈이 필요합니다. 만약 [Laravel Herd](https://herd.laravel.com) 또는 `php.new`로 PHP를 설치해 개발 중이라면 이미 이 확장 모듈이 설치되어 있을 것입니다. 하지만 직접 설치해야 하는 경우 PECL을 통해 설치할 수 있습니다:

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 관한 자세한 내용은 [MongoDB PHP extension 설치 안내](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기 (Starting a MongoDB Server)

MongoDB Community Server는 Windows, macOS, Linux 환경에서 로컬로 MongoDB를 실행하는 데 사용할 수 있으며, Docker 컨테이너 형태로도 제공됩니다. MongoDB 설치 방법은 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버의 연결 문자열은 `.env` 파일에서 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드에서 MongoDB를 호스팅하고자 한다면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 고려하세요.
애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접근하려면, 반드시 클러스터 네트워크 설정에서 [본인의 IP 주소를 IP 접근 목록에 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas 연결 문자열도 `.env` 파일에서 다음과 같이 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치하기 (Install the Laravel MongoDB Package)

마지막으로 Composer를 사용해 Laravel MongoDB 패키지를 설치하세요:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]  
> `mongodb` PHP 확장 모듈이 설치되어 있지 않으면 패키지 설치가 실패합니다. CLI와 웹 서버의 PHP 설정이 다를 수 있으니, 두 환경 모두에서 확장 모듈이 활성화되어 있는지 확인하세요.

<a name="configuration"></a>
## 설정 (Configuration)

MongoDB 연결 설정은 애플리케이션의 `config/database.php` 파일에서 할 수 있습니다. 해당 파일에 `mongodb` 접속 정보를 추가하고 `mongodb` 드라이버를 사용하도록 설정합니다:

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
## 기능 (Features)

설정이 완료되면 `mongodb` 패키지와 데이터베이스 연결을 활용하여 다양한 강력한 기능을 이용할 수 있습니다:

- [Eloquent 사용](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/) : MongoDB 컬렉션에 모델을 저장하고, 일반 Eloquent 기능 외에도 임베디드 관계(embedded relationships) 등 추가 기능을 제공합니다. 또한 MongoDB 드라이버에 직접 접근하여 원시 쿼리나 집계 파이프라인 연산도 수행할 수 있습니다.
- [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) : 쿼리 빌더를 활용해 복잡한 쿼리를 작성할 수 있습니다.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) : TTL 인덱스 같은 MongoDB의 기능에 최적화되어 만료된 캐시 항목을 자동으로 삭제합니다.
- [큐 작업 디스패치 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) : `mongodb` 큐 드라이버를 이용해 큐 작업을 실행할 수 있습니다.
- [GridFS에 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/gridfs/) : [Flysystem용 GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/)를 통해 가능합니다.
- 데이터베이스 연결 또는 Eloquent를 사용하는 대부분의 서드파티 패키지를 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel 사용법을 계속 배우려면 MongoDB의 [빠른 시작 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.