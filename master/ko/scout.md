# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉 설정](#queueing)
- [드라이버 사전 준비사항](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 데이터 구성](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 지정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 조건절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이즈](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/master/eloquent)에 전체 텍스트 검색 기능을 간단하게 추가할 수 있는 드라이버 기반 솔루션을 제공합니다. Scout는 모델 옵저버(observer)를 활용하여, Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), MySQL / PostgreSQL(`database`) 드라이버를 기본으로 지원합니다. 또한, 외부 의존성이 필요 없는 로컬 개발용 "collection" 드라이버도 포함되어 있습니다. 필요에 따라 직접 커스텀 드라이버를 작성해서 Scout 기능을 확장할 수도 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해서 Scout를 설치하세요.

```shell
composer require laravel/scout
```

설치 후, `vendor:publish` Artisan 명령어로 Scout 설정 파일을 배포해야 합니다. 이 명령어는 `config` 디렉터리에 `scout.php` 설정 파일을 복사합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 기능을 적용하려는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델과 검색 드라이버를 동기화하는 옵저버를 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```

<a name="queueing"></a>
### 큐잉 설정

`database`나 `collection`이 아닌 엔진을 사용할 경우, Scout를 실제로 활용하기 전에 [큐 드라이버](/docs/master/queues) 설정을 강력하게 권장합니다. 큐 워커를 운영하면, 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐에 적재하여, 애플리케이션 웹 UI의 응답 속도를 크게 향상할 수 있습니다.

큐 드라이버를 설정한 후, `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 변경하세요.

```php
'queue' => true,
```

`queue` 옵션이 `false`여도, Algolia 및 Meilisearch 등 일부 Scout 드라이버는 항상 비동기로 레코드를 인덱싱한다는 점을 기억해야 합니다. 즉, 라라벨 애플리케이션에서 인덱스 작업이 완료되어도, 실제 검색 엔진에는 곧바로 변경사항이 반영되지 않을 수 있습니다.

Scout 작업에서 사용할 연결(connection)과 큐 이름(queue)을 지정하고 싶다면 배열 형태로 설정할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

연결 및 큐 이름을 커스텀 설정한 경우, 해당 connection/queue에서 작업을 처리할 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비사항

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 쓸 때는, Algolia `id`와 `secret` 인증 정보를 `config/scout.php` 파일에 설정해야 합니다. 인증 정보를 입력한 뒤, Composer 패키지 관리자를 이용해 Algolia PHP SDK를 설치하세요.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈소스인 검색 엔진입니다. 로컬 머신에서 Meilisearch를 설치하는 방법을 모를 경우, Laravel 공식 Docker 개발 환경인 [Laravel Sail](/docs/master/sail#meilisearch)을 참고하세요.

Meilisearch 드라이버를 사용하려면 Composer로 Meilisearch PHP SDK를 추가 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 다음, `.env` 파일에 `SCOUT_DRIVER`와 Meilisearch의 `host`, `key` 정보를 설정하세요.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 더 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용 중인 Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` SDK 버전을 반드시 설치해야 합니다. [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하세요.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는, 반드시 Meilisearch 서비스 자체의 [추가적인 주요 변경사항](https://github.com/meilisearch/Meilisearch/releases)도 함께 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 엄청나게 빠른 오픈소스 검색 엔진으로, 키워드 검색·의미 기반 검색·지리 정보 검색·벡터 검색을 모두 지원합니다.

Typesense는 [직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면, Composer로 Typesense PHP SDK를 설치하세요.

```shell
composer require typesense/typesense-php
```

그리고, `.env` 파일에 `SCOUT_DRIVER`와 Typesense의 host/API key 정보를 지정합니다.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/master/sail) 사용 시에는 Docker 컨테이너 이름에 맞게 `TYPESENSE_HOST` 설정을 조정해야 할 수 있습니다. 포트, 경로, 프로토콜도 옵션으로 지정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정 및 스키마 정의는 `config/scout.php` 파일에서 가능합니다. 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense 사용 시, 검색 가능한 모델에서 반드시 `toSearchableArray` 메서드를 정의하여, 모델의 기본키를 문자열로, 생성일자를 UNIX 타임스탬프로 변환해야 합니다.

```php
/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray(): array
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```

Typesense 컬렉션 스키마도 `config/scout.php` 파일에 정의해야 합니다. 스키마에서는 Typesense로 검색 가능하게 만들 각 필드의 데이터 타입을 지정합니다. 스키마 옵션에 대한 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 수정해야 한다면, `scout:flush`와 `scout:import`를 순서대로 실행해 인덱스 데이터를 전부 삭제 및 재생성하거나, Typesense API로 기존 데이터를 유지한 채 컬렉션 스키마만 수정할 수 있습니다.

검색 가능한 모델이 소프트 삭제 기능을 사용할 경우, 해당 모델의 Typesense 스키마에 `__soft_deleted` 필드를 반드시 정의해야 합니다.

```php
User::class => [
    'collection-schema' => [
        'fields' => [
            // ...
            [
                'name' => '__soft_deleted',
                'type' => 'int32',
                'optional' => true,
            ],
        ],
    ],
],
```

<a name="typesense-dynamic-search-parameters"></a>
#### 동적 검색 파라미터

Typesense는 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 `options` 메서드로 동적으로 지정할 수 있습니다.

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 설정

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

각 Eloquent 모델은 하나의 검색 "인덱스"와 동기화됩니다(인덱스는 해당 모델의 모든 검색 대상 레코드를 담는 저장소이며, MySQL의 테이블과 비슷하게 생각할 수 있습니다). 기본적으로, 각 모델은 해당 모델의 일반 테이블명과 같은 인덱스에 저장됩니다(주로 모델의 복수형 이름). 필요하다면 `searchableAs` 메서드를 오버라이딩해서 인덱스명을 커스텀할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 데이터 구성

기본적으로, 모델의 `toArray` 전체 결과가 검색 인덱스에 저장됩니다. 만약 인덱스에 저장될 데이터를 커스터마이징하고 싶다면, `toSearchableArray` 메서드를 오버라이딩할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the indexable data array for the model.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 커스텀 데이터 배열 작성...

        return $array;
    }
}
```

일부 검색 엔진(예: Meilisearch)은 필터 연산(`>`, `<` 등)을 올바른 타입의 데이터에만 수행할 수 있습니다. 따라서, 이런 엔진을 사용할 때는 숫자 값이 올바른 타입으로 형변환되어야 합니다.

```php
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="configuring-indexes-for-algolia"></a>
#### 인덱스 설정 구성(Algolia)

Algolia 인덱스에 추가 설정을 적용하고 싶을 때, Algolia UI 대신 애플리케이션의 `config/scout.php` 파일에서 직접 관리하는 것이 효율적이고, 여러 환경에서 설정을 일관되게 유지할 수 있습니다. 필터 속성, 순위, 페이싱(faceting) 등 다양한 [설정 필드](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)를 등록할 수 있습니다.

`config/scout.php` 파일에 각 인덱스별 설정을 추가하세요.

```php
use App\Models\User;
use App\Models\Flight;

'algolia' => [
    'id' => env('ALGOLIA_APP_ID', ''),
    'secret' => env('ALGOLIA_SECRET', ''),
    'index-settings' => [
        User::class => [
            'searchableAttributes' => ['id', 'name', 'email'],
            'attributesForFaceting'=> ['filterOnly(email)'],
            // 기타 추가 설정...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

소프트 삭제가 적용된 모델 인덱스를 `index-settings` 배열에 포함했다면, Scout가 자동으로 soft deleted 모델을 페이싱 속성에 포함시킵니다. 소프트 삭제 모델 인덱스에 추가 페이싱 속성이 없다면 빈 항목만 등록해도 됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후, `scout:sync-index-settings` Artisan 명령어를 실행해야 실제 Algolia로 전달됩니다. 배포 파이프라인에 자동 배포를 추가하는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정(Meilisearch)

Meilisearch는 필터 가능한 속성, 정렬 가능한 속성 등 [지원되는 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 사전에 지정해야 합니다.

`where` 메서드로 필터링할 속성은 `filterableAttributes`, `orderBy`로 정렬할 속성은 `sortableAttributes`로 각각 등록하세요. `scout` 설정 파일의 `meilisearch` 항목에서 지정합니다.

```php
use App\Models\User;
use App\Models\Flight;

'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        User::class => [
            'filterableAttributes'=> ['id', 'name', 'email'],
            'sortableAttributes' => ['created_at'],
            // 기타 설정...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

소프트 삭제 모델도 `index-settings`에 빈 항목만 등록하면 soft deleted 모델 필터링이 자동 지원됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정 완료 후, 아래 명령을 실행해 Meilisearch에 적용하세요.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

Scout는 모델의 기본 키(primary key)를 인덱스의 고유 ID/키로 사용합니다. 이 동작을 커스텀하고 싶다면 `getScoutKey`, `getScoutKeyName` 메서드를 오버라이딩할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 지정

기본적으로 Scout는 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용하지만, 개별 모델에서 `searchableUsing` 메서드를 오버라이딩해 엔진을 변경할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\Scout;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

[Algolia](https://algolia.com) 사용 시, Scout를 통해 사용자 식별을 활성화하면, 인증된 사용자와 검색 연산을 연동시킴으로써 Algolia 대시보드에서 사용자별 검색 분석 데이터를 확인할 수 있습니다. `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하면 활성화됩니다.

```ini
SCOUT_IDENTIFY=true
```

이렇게 하면, 사용자의 검색 요청마다 요청자의 IP주소와 인증된 사용자의 기본 식별자가 Algolia로 함께 전송됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

`database` 엔진은 Laravel Scout를 가장 빠르게 시작할 수 있는 방법입니다. MySQL, PostgreSQL의 전체 텍스트 인덱스와 "where like" 조건을 활용해, 기존 데이터베이스에서 쿼리 결과를 필터링하여 검색 결과를 도출합니다.

데이터베이스 엔진을 사용하려면, `.env`에 `SCOUT_DRIVER=database`로 지정하거나 `scout` 설정 파일에 직접 드라이버를 명시하세요.

```ini
SCOUT_DRIVER=database
```

드라이버 지정 후에는 [검색 데이터 구성](#configuring-searchable-data)을 완료한 뒤, 모델에 대해 [검색 쿼리 실행](#searching)이 가능합니다. Algolia, Meilisearch, Typesense에서 별도의 인덱싱 작업이 필요한 것과 달리, 데이터베이스 엔진은 인덱싱 작업이 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이즈

기본적으로, 데이터베이스 엔진은 [설정된 전체 검색 속성](#configuring-searchable-data)마다 "where like" 쿼리를 실행합니다. 상황에 따라 성능 저하가 있을 수 있으므로, 일부 컬럼만 전체 텍스트 검색(full text) 쿼리를 사용하거나, 접두사(prefix)만 LIKE로 검색하도록 전략을 지정할 수 있습니다.

PHP 속성(Attributes)을 `toSearchableArray`에 할당하면 됩니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray(): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```

> [!WARNING]
> 컬럼에 전체 텍스트 쿼리를 적용하려면, 해당 컬럼에 [full text 인덱스](/docs/master/migrations#available-index-types)가 부여되어 있는지 반드시 확인해야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서 Algolia, Meilisearch, Typesense 대신 "collection" 엔진으로 간편하게 시작할 수도 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 WHERE 조건과 컬렉션 필터링만 활용하여 검색 결과를 반환하므로, 별도의 인덱싱 과정 없이 사용할 수 있습니다.

`.env`에 `SCOUT_DRIVER=collection`으로 지정하거나 설정 파일에서 명시하세요.

```ini
SCOUT_DRIVER=collection
```

설정 후, 모델에 대해 [검색 쿼리 실행](#searching)이 바로 가능합니다. Algolia, Meilisearch, Typesense 등에서 필요한 인덱싱 작업을 따로 할 필요가 없습니다.

#### 데이터베이스 엔진과의 차이점

"database" 엔진과 "collection" 엔진 모두 결과를 데이터베이스에서 직접 가져옵니다. 그러나 컬렉션 엔진은 전체 텍스트 인덱스나 LIKE 쿼리를 사용하지 않고, 모든 레코드를 불러온 뒤, Laravel의 `Str::is` 헬퍼로 속성값에 검색어가 포함되어 있는지 확인합니다.

컬렉션 엔진은 SQLite, SQL Server 등 Laravel이 지원하는 모든 관계형 데이터베이스에서 동작하지만, 데이터베이스 엔진에 비해 성능이 훨씬 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 일괄 가져오기

기존 프로젝트에 Scout를 도입하는 경우, 이미 존재하는 데이터베이스 레코드를 검색 인덱스로 일괄 가져와야 할 수 있습니다. `scout:import` Artisan 명령어를 이용하면 전체 레코드를 한 번에 인덱스에 추가할 수 있습니다.

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` 명령어로 [큐 작업](/docs/master/queues) 기반의 일괄 인덱싱도 가능합니다.

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` 명령어는 해당 모델의 모든 인덱스 레코드를 한 번에 삭제합니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 일괄 가져오기 쿼리 수정

일괄 인덱싱 전, 쿼리에 eager loading 등 별도의 조건을 추가하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하면 됩니다.

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * Modify the query used to retrieve models when making all of the models searchable.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 큐를 이용해 일괄 인덱싱할 때는 `makeAllSearchableUsing`이 적용되지 않을 수 있습니다. 큐에서 처리되는 모델 컬렉션은 [관계가 복원되지 않습니다](/docs/master/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

모델에 `Laravel\Scout\Searchable` 트레이트를 추가한 뒤, 단순히 모델 인스턴스를 `save` 또는 `create`하면 자동으로 검색 인덱스에 등록됩니다. [큐잉](#queueing)이 활성화된 경우, 인덱싱은 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 대량 추가

Eloquent 쿼리에 `searchable` 메서드를 연결하여, 여러 모델을 한 번에 인덱싱할 수 있습니다. 이 메서드는 쿼리 결과를 [청크 단위로 분할](/docs/master/eloquent#chunking-results)해 모두 인덱스에 등록합니다. 큐잉 설정 시 모든 청크가 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에서도 `searchable`을 사용할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 메모리 내에 Eloquent 컬렉션이 있다면, 컬렉션 인스턴스에서 직접 호출할 수 있습니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 일종의 upsert 연산(이미 인덱스에 존재하면 업데이트, 없으면 추가)으로 동작합니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 평소처럼 프로퍼티를 수정한 뒤 `save`만 하면 Scout가 알아서 인덱스에 반영합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 수정...

$order->save();
```

Eloquent 쿼리 인스턴스에 `searchable`을 붙이면, 여러 레코드의 인덱스 레코드를 일괄 업데이트할 수 있습니다. 인덱스에 존재하지 않는 레코드는 새로 추가됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스에서도 사용할 수 있습니다.

```php
$user->orders()->searchable();
```

컬렉션 인스턴스에도 동일하게 적용됩니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 가공

검색 가능 처리 직전, 모델 컬렉션을 수정(예: eager 로딩)하고 싶다면 해당 모델에 `makeSearchableUsing` 메서드를 정의하세요.

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * Modify the collection of models being made searchable.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 제거

검색 인덱스에서 레코드를 제거하려면, 데이터베이스에서 모델을 삭제(`delete`)만 하면 됩니다. [소프트 삭제](/docs/master/eloquent#soft-deleting) 모델에도 적용됩니다.

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 미리 조회하지 않고 일괄 삭제하려면, Eloquent 쿼리 인스턴스에 `unsearchable`을 사용하세요.

```php
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스에도 적용할 수 있습니다.

```php
$user->orders()->unsearchable();
```

컬렉션 인스턴스의 모든 레코드를 인덱스에서 제거하려면:

```php
$orders->unsearchable();
```

모델 전체의 인덱스 레코드를 모두 삭제하려면, `removeAllFromSearch` 메서드를 사용하세요.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

여러 번의 Eloquent 연산 중에 인덱스 동기화를 잠시 멈출 때는, `withoutSyncingToSearch` 메서드를 사용하면 됩니다. 이 메서드는 클로저 내부 코드에서 발생한 모델 연산을 인덱스에 반영하지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 여러 모델 연산 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

특정 조건 하에서만 모델이 검색 가능하도록 하고 싶은 경우, 예를 들어 게시글이 "draft" 또는 "published" 상태일 때, "published"만 인덱싱하려면, 해당 모델에 `shouldBeSearchable` 메서드를 정의하세요.

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`save`, `create`, 쿼리, 관계를 통한 조작에만 `shouldBeSearchable`이 적용됩니다. 직접 `searchable`을 호출하면 이 조건이 무시됩니다.

> [!WARNING]
> "database" 엔진 사용 시에는 `shouldBeSearchable`이 적용되지 않습니다. `database` 엔진은 모든 검색 데이터를 DB에 저장하므로, 같은 결과를 원한다면 [where 조건절](#where-clauses)을 사용해야 합니다.

<a name="searching"></a>
## 검색

모델의 `search` 메서드로 검색을 시작할 수 있습니다. 이 메서드는 검색어 문자열을 받아, 해당 쿼리에 일치하는 Eloquent 모델을 리턴합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색은 Eloquent 모델 컬렉션을 반환하므로, 라우트나 컨트롤러에서 곧바로 JSON으로 내보낼 수도 있습니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과를 Eloquent 모델로 변환하기 전의 원시 데이터를 얻으려면 `raw` 메서드를 사용하세요.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

보통 검색은 모델의 [searchableAs](#configuring-model-indexes)에서 지정한 인덱스에서 수행됩니다. 만약 다른 인덱스를 검색하고 싶다면, `within` 메서드로 지정할 수 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 조건절

Scout는 기본적이고 단순한 "where" 조건을 검색 쿼리에 추가할 수 있습니다. 현재는 주로 소유자 ID 등 숫자 값 동등성 비교만 지원합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn` 메서드로 여러 값 중 하나를 포함하는 경우를 검사할 수 있습니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn`은 배열 밖의 값들만 검색합니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니므로 더 복잡한 "where" 조건은 지원되지 않습니다.

> [!WARNING]
> Meilisearch 사용 시, 먼저 [filterable attributes 설정](#configuring-filterable-data-for-meilisearch)을 마쳐야 합니다.

<a name="pagination"></a>
### 페이지네이션

검색 결과도 `paginate` 메서드를 통해 페이지네이션 할 수 있습니다. 이 메서드는 [`Illuminate\Pagination\LengthAwarePaginator`](/docs/master/pagination) 인스턴스를 반환하며, 기존 Eloquent 페이지네이션과 동일하게 사용할 수 있습니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 항목 수를 지정하려면 첫 번째 인자로 넘겨주세요.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

검색 결과와 페이지 링크는 [Blade](/docs/master/blade)에서 일반적으로 렌더링할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

JSON으로 페이지네이션 결과를 반환하려면, 라우트나 컨트롤러에서 paginator 인스턴스를 바로 반환하면 됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프(global scope) 정의를 알지 못하므로, Scout 페이지네이션 환경에서는 글로벌 스코프를 사용하지 않거나, Scout로 검색할 때 수동으로 동일한 조건을 추가해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

검색 인덱싱 모델이 [소프트 삭제](/docs/master/eloquent#soft-deleting)일 경우, 소프트 삭제된 모델도 검색 대상으로 하고 싶으면, `config/scout.php`의 `soft_delete` 옵션을 `true`로 설정하세요.

```php
'soft_delete' => true,
```

이 옵션을 활성화하면, Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 대신 레코드에 숨겨진 `__soft_deleted` 속성을 추가합니다. 이후 검색 시, `withTrashed`나 `onlyTrashed` 메서드로 소프트 삭제 데이터를 검색할 수 있습니다.

```php
use App\Models\Order;

// 소프트 삭제된 데이터도 포함
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 데이터만 반환
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제 모델이 `forceDelete`로 영구 삭제될 때는, Scout에서도 자동으로 인덱스에서 제거됩니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이즈

엔진의 검색 동작을 고급 수준으로 커스터마이징하고 싶다면, `search` 메서드의 두 번째 인자로 클로저를 전달하면 됩니다. 예를 들어, Algolia에 지오로케이션 데이터를 추가하고 싶을 때 아래와 같이 사용할 수 있습니다.

```php
use Algolia\AlgoliaSearch\SearchIndex;
use App\Models\Order;

Order::search(
    'Star Trek',
    function (SearchIndex $algolia, string $query, array $options) {
        $options['body']['query']['bool']['filter']['geo_distance'] = [
            'distance' => '1000km',
            'location' => ['lat' => 36, 'lon' => 111],
        ];

        return $algolia->search($query, $options);
    }
)->get();
```

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 결과 쿼리 커스터마이즈

Scout가 검색 엔진으로부터 일치하는 Eloquent 모델의 기본 키를 받아온 후, 실제 데이터는 Eloquent 쿼리로 가져옵니다. 이 때 `query` 메서드에 클로저를 전달하면, 쿼리 빌더를 활용해 결과 쿼리를 커스터마이징할 수 있습니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 검색 엔진에서 결과를 받아온 후 실행되므로, 결과 "필터링" 목적이 아닌 Eager Loading 등에만 사용해야 합니다. 필터링은 [Scout where 조건절](#where-clauses)을 활용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 구현

기본 제공되는 Scout 검색 엔진이 요구 사항에 맞지 않는다면, 직접 엔진을 구현해 Scout에 등록할 수 있습니다. 직접 구현하는 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속받아야 하며, 다음 8개 메서드를 반드시 구현해야 합니다.

```php
use Laravel\Scout\Builder;

abstract public function update($models);
abstract public function delete($models);
abstract public function search(Builder $builder);
abstract public function paginate(Builder $builder, $perPage, $page);
abstract public function mapIds($results);
abstract public function map(Builder $builder, $results, $model);
abstract public function getTotalCount($results);
abstract public function flush($model);
```

각 메서드 구현 예시는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 좋습니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진 구현 후에는 Scout의 엔진 매니저에 등록해야 합니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 해결할 수 있으며, 일반적으로 `App\Providers\AppServiceProvider` 클래스 또는 기타 서비스 프로바이더의 `boot` 메서드에서 `extend`로 등록합니다.

```php
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

엔진 등록 후, `config/scout.php` 파일의 `driver` 항목을 커스텀 엔진으로 지정하면 됩니다.

```php
'driver' => 'mysql',
```
