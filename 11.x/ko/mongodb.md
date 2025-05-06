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

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb)는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로, 높은 쓰기 부하(분석 또는 IoT에 유용)와 높은 가용성(자동 장애 조치가 가능한 복제 세트 구성이 쉬움)으로 널리 사용됩니다. 또한 수평 확장을 위해 데이터베이스를 손쉽게 샤딩할 수 있으며, 집계, 텍스트 검색 또는 지리 공간 쿼리 등을 위한 강력한 쿼리 언어를 제공합니다.

MongoDB는 SQL 데이터베이스처럼 행(row)과 열(column)로 이루어진 테이블에 데이터를 저장하는 대신, 각 레코드를 BSON이라는 이진 데이터 표현 방식의 문서(document)로 저장합니다. 애플리케이션은 이 정보를 JSON 형식으로 가져올 수 있습니다. 문서, 배열, 중첩 문서, 이진 데이터 등 다양한 데이터 타입을 지원합니다.

Laravel과 함께 MongoDB를 사용하기 전에, Composer를 통해 `mongodb/laravel-mongodb` 패키지를 설치하고 사용하는 것을 권장합니다. `laravel-mongodb` 패키지는 MongoDB에서 공식적으로 관리하며, PHP는 MongoDB 드라이버를 통해 MongoDB를 기본적으로 지원하지만, [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지는 Eloquent 및 Laravel의 다양한 기능과의 더 풍부한 통합을 제공합니다:

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## 설치

<a name="mongodb-driver"></a>
### MongoDB 드라이버

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장(extension)이 필요합니다. [Laravel Herd](https://herd.laravel.com)를 사용하거나 `php.new`를 통해 PHP를 설치했다면 이미 해당 확장이 시스템에 설치되어 있을 수 있습니다. 하지만 수동 설치가 필요한 경우, PECL을 통해 설치할 수 있습니다:

```shell
pecl install mongodb
```

MongoDB PHP 확장 설치에 대한 자세한 정보는 [MongoDB PHP 확장 설치 안내](https://www.php.net/manual/en/mongodb.installation.php)를 참고하십시오.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기

MongoDB 커뮤니티 서버는 로컬에서 MongoDB를 실행하는 데 사용할 수 있으며, Windows, macOS, Linux 또는 Docker 컨테이너로 설치할 수 있습니다. MongoDB 설치 방법은 [공식 MongoDB 커뮤니티 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참고하세요.

MongoDB 서버의 연결 문자열은 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

클라우드에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) 사용을 고려하세요.
애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접근하려면, 프로젝트의 IP 액세스 리스트에 [본인의 IP 주소를 클러스터의 네트워크 설정에 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas의 연결 문자열도 `.env` 파일에 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a name="install-the-laravel-mongodb-package"></a>
### Laravel MongoDB 패키지 설치

마지막으로, Composer를 사용해 Laravel MongoDB 패키지를 설치하세요:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]  
> `mongodb` PHP 확장이 설치되어 있지 않으면 이 패키지 설치가 실패합니다. PHP 설정은 CLI와 웹 서버 간에 다를 수 있으므로, 두 환경 모두에서 확장이 활성화되어 있는지 반드시 확인하세요.

<a name="configuration"></a>
## 설정

애플리케이션의 `config/database.php` 설정 파일을 통해 MongoDB 연결을 구성할 수 있습니다. 이 파일에 `mongodb` 드라이버를 사용하는 `mongodb` 연결 정보를 추가하세요:

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

설정이 완료되면, 애플리케이션에서 `mongodb` 패키지와 데이터베이스 연결을 활용하여 다양한 강력한 기능을 사용할 수 있습니다:

- [Eloquent 사용하기](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/): 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 일반 Eloquent 기능 외에도, Laravel MongoDB 패키지는 임베디드(embedded) 관계와 같은 추가 기능을 제공합니다. 또한 MongoDB 드라이버에 직접 접근해 원시 쿼리나 집계 파이프라인 등의 연산도 실행할 수 있습니다.
- 쿼리 빌더를 사용하여 [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/)이 가능합니다.
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)는 MongoDB의 TTL 인덱스 등 기능을 활용해 캐시 만료 항목을 자동으로 삭제합니다.
- `mongodb` 큐 드라이버로 [큐 작업을 디스패치하고 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/)할 수 있습니다.
- [GridFS를 이용한 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/gridfs/)이 [Flysystem의 GridFS 어댑터](https://flysystem.thephpleague.com/docs/adapter/gridfs/)를 통해 가능합니다.
- 데이터베이스 연결이나 Eloquent를 사용하는 대부분의 서드파티 패키지는 MongoDB와 함께 사용할 수 있습니다.

MongoDB와 Laravel 사용법을 더 배우려면, MongoDB의 [빠른 시작 가이드](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/)를 참고하세요.