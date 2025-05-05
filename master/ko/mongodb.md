# MongoDB

- [소개](#introduction)
- [설치](#installation)
    - [MongoDB 드라이버](#mongodb-driver)
    - [MongoDB 서버 시작하기](#starting-a-mongodb-server)
    - [Laravel MongoDB 패키지 설치](#install-the-laravel-mongodb-package)
- [설정](#configuration)
- [기능](#features)

<a name="introduction"></a>
## 소개

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석 또는 IoT에 유용)와 높은 가용성(자동 장애 조치가 가능한 리플리카 세트 구성 용이)을 위해 사용됩니다. 또한 데이터베이스를 수평적으로 손쉽게 분산(샤딩)할 수 있고, 집계, 텍스트 검색, 지리 공간 쿼리 등을 위한 강력한 쿼리 언어를 제공합니다.

SQL 데이터베이스처럼 행 또는 열의 테이블에 데이터를 저장하는 대신, MongoDB의 각 레코드는 BSON(이진 데이터 표현)으로 기술된 문서 형태로 저장됩니다. 이후 애플리케이션은 이 정보를 JSON 형식으로 받아올 수 있습니다. 문서, 배열, 내장 문서, 바이너리 데이터 등 다양한 데이터 타입을 지원합니다.

Laravel에서 MongoDB를 사용하기 전에 Composer를 통해 `mongodb/laravel-mongodb` 패키지 설치 및 사용을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 관리하며, PHP에서 MongoDB 드라이버로 기본 지원되지만, [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지를 사용하면 Eloquent 및 다양한 Laravel 기능과의 통합이 더욱 강화됩니다.

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치

<a name="mongodb-driver"></a>
### MongoDB 드라이버

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장(extension)이 필요합니다. [Laravel Herd](https://herd.laravel.com)를 사용하거나 `php.new`로 PHP를 설치했다면 이미 이 확장이 설치되어 있습니다. 직접 설치가 필요한 경우 PECL을 통해 아래와 같이 설치할 수 있습니다.

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 대한 더 자세한 내용은 [MongoDB PHP 확장 설치 안내서](https://www.php.net/manual/en/mongodb.installation.php)를 참고하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기

MongoDB Community Server를 사용하면 로컬에서 MongoDB를 실행할 수 있으며, Windows, macOS, Linux 혹은 Docker 컨테이너에 설치할 수 있습니다. MongoDB 설치 방법은 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버의 연결 문자열은 `.env` 파일에 다음과 같이 지정합니다.

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 사용할 수 있습니다.
애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접근하려면, [클러스터의 네트워크 설정에서 자신의 IP 주소를 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas 연결 문자열도 `.env` 파일에서 아래와 같이 지정할 수 있습니다.

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치

마지막으로 Composer를 사용해 Laravel MongoDB 패키지를 설치하세요.

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]
> `mongodb` PHP 확장이 설치되어 있지 않으면 패키지 설치가 실패합니다. CLI와 웹 서버의 PHP 설정이 다를 수 있으므로, 두 환경 모두에서 확장이 활성화되어 있는지 확인하세요.

<a name="configuration"></a>
## 설정

애플리케이션의 `config/database.php` 설정 파일에서 MongoDB 연결을 구성할 수 있습니다. 이 파일 내에 `mongodb` 드라이버를 사용하는 연결을 추가하세요.

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

설정이 완료되면, 애플리케이션 내에서 `mongodb` 패키지와 데이터베이스 연결을 사용해 다양한 강력한 기능을 활용할 수 있습니다.

- [Eloquent 사용](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/): 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 기본 Eloquent 기능 외에도, Laravel MongoDB 패키지는 임베디드 관계 등 추가 기능을 제공합니다. 또한 MongoDB 드라이버에 직접 접근해 원시 쿼리, 집계 파이프라인 등 다양한 작업을 수행할 수 있습니다.
- [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/): 쿼리 빌더를 이용해 복잡한 쿼리를 작성할 수 있습니다.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)는 TTL 인덱스 같은 MongoDB 기능을 활용해 만료된 캐시 엔트리를 자동 삭제하도록 최적화되어 있습니다.
- [큐 작업 디스패치 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb` 큐 드라이버를 이용한 작업 처리 지원.
- [GridFS에 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/): [Flysystem의 GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/)를 통해 파일을 저장할 수 있습니다.
- 데이터베이스 연결 또는 Eloquent를 사용하는 대부분의 서드파티 패키지도 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel 사용 방법을 더 자세히 알아보고 싶다면 MongoDB의 [퀵 스타트 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.