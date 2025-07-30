# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 전제 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능한 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [where 절](#where-clauses)
    - [페이징](#pagination)
    - [soft deleting](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)는 단순한 드라이버 기반 솔루션으로, [Eloquent 모델](/docs/10.x/eloquent)에 전체 텍스트 검색 기능을 추가할 수 있습니다. 모델 옵저버를 활용해 Scout는 Eloquent 레코드와 검색 인덱스가 자동으로 동기화되도록 관리합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본 제공하며, 로컬 개발용으로 외부 의존성이나 서드파티 서비스가 필요 없는 "collection" 드라이버도 포함하고 있습니다. 또, 필요에 따라 간단하게 커스텀 드라이버를 작성해 Scout 기능을 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 관리자를 사용해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

설치 후 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 퍼블리시합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리에 생성합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로 검색 가능하게 만들 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여 모델과 검색 드라이버 간 동기화를 자동으로 수행합니다:

```
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
### 큐잉 (Queueing)

Scout 사용을 위해 큐 드라이버 설정은 필수는 아니지만, 설정할 것을 강력히 권장합니다. 큐 워커를 실행하면 모델과 검색 인덱스 동기화 작업이 큐에 할당되어, 웹 인터페이스의 응답 속도가 크게 개선됩니다.

큐 드라이버를 설정한 후 `config/scout.php` 설정 파일에서 `queue` 옵션을 `true`로 설정하세요:

```
'queue' => true,
```

`queue` 옵션이 `false`인 경우에도 Algolia, Meilisearch 같은 일부 드라이버는 항상 비동기적으로 인덱싱 작업을 수행하므로, Laravel 내에서 인덱스 작업 완료 후에도 검색 엔진 자체에는 반영이 즉시 되지 않을 수 있음을 기억해야 합니다.

Scout 작업에 사용할 연결과 큐를 지정하려면 `queue` 설정을 배열 형태로 정의할 수 있습니다:

```
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

이 경우, 해당 연결과 큐에서 작업을 처리하려면 큐 워커를 직접 실행해야 합니다:

```
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 전제 조건 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는 `config/scout.php` 설정 파일에 Algolia `id`와 `secret` 자격 증명을 설정해야 합니다. 설정 후 Composer를 사용해 Algolia PHP SDK를 설치하세요:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 빠르고 오픈 소스인 검색 엔진입니다. 로컬에 Meilisearch 설치 방법을 모를 경우, Laravel 공식 지원 Docker 개발 환경인 [Laravel Sail](/docs/10.x/sail#meilisearch)을 참고하세요.

Meilisearch 드라이버를 사용할 때는 Composer로 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 후 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch `host`, `key` 자격 증명을 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용 중인 Meilisearch 바이너리 버전에 맞는 `meilisearch/meilisearch-php` 버전을 설치해야 하므로 [바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)도 확인하세요.

> [!WARNING]  
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 Meilisearch 서비스 자체의 [추가 파괴적 변경 사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 검토해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 빠르고 오픈 소스인 검색 엔진으로 키워드 검색, 의미 검색, 지리 검색, 벡터 검색을 지원합니다.

Typesense는 [직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

이후 `.env` 파일에 `SCOUT_DRIVER`와 Typesense 호스트, API 키 자격 증명을 설정합니다:

```env
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

필요 시 포트, 경로, 프로토콜도 지정할 수 있습니다:

```env
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

추가 설정 및 컬렉션 스키마 정의는 `config/scout.php` 설정 파일에서 가능합니다. Typesense 관련 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장용 데이터 준비

Typesense를 사용할 때는 모델의 기본 키를 문자열로, 생성일(created_at)을 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드를 정의해야 합니다:

```php
/**
 * 모델의 인덱싱 가능한 데이터 배열을 반환합니다.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray()
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```

또한, `config/scout.php` 내에서 Typesense 컬렉션 스키마를 정의해야 합니다. 이 스키마는 Typesense로 검색 가능한 각 필드의 데이터 유형을 설명합니다. 사용 가능한 모든 스키마 옵션은 [Typesense 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 변경해야 할 경우, `scout:flush`와 `scout:import` 명령어로 기존 데이터와 스키마를 모두 초기화하거나, Typesense API를 사용해 데이터를 삭제하지 않고도 스키마를 수정할 수 있습니다.

소프트 삭제가 적용된 모델이라면 `config/scout.php` 내 해당 모델 Typesense 스키마에 `__soft_deleted` 필드를 정의하세요:

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
#### 동적 검색 매개변수

Typesense는 검색 작업 시 `options` 메서드를 이용해 [검색 매개변수](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 수정할 수 있습니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정 (Configuring Model Indexes)

각 Eloquent 모델은 해당 모델의 모든 검색 가능한 레코드를 포함하는 하나의 검색 "인덱스"와 동기화됩니다. 쉽게 말해, 인덱스는 MySQL 테이블과 비슷합니다. 기본적으로 각 모델은 보통 모델 이름의 복수형에 해당하는 인덱스에 저장됩니다. 하지만 모델의 `searchableAs` 메서드를 오버라이드해 인덱스 이름을 직접 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연결된 인덱스 이름 반환
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 설정 (Configuring Searchable Data)

기본적으로 모델의 전체 `toArray` 데이터가 검색 인덱스에 저장됩니다. 저장할 데이터를 직접 제어하고 싶다면 `toSearchableArray` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱싱 가능한 데이터 배열을 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열을 커스터마이징...

        return $array;
    }
}
```

Meilisearch와 같이 필터 기능이 데이터 타입을 엄격히 요구하는 검색 엔진을 사용할 경우, 숫자는 올바른 타입으로 캐스팅해 설정해야 합니다:

```
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정 (Meilisearch)

Scout의 다른 드라이버와 달리 Meilisearch는 필터용 속성(filterable attributes), 정렬 속성(sortable attributes) 등 인덱스 검색 설정을 사전에 정의해야 합니다.

필터 가능 속성은 Scout의 `where` 메서드로 필터링하려는 컬럼이고, 정렬 가능 속성은 `orderBy` 메서드를 쓰려는 컬럼입니다. `scout` 설정 파일 내 `meilisearch` 항목의 `index-settings` 배열에서 설정하세요:

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
            // 기타 설정 필드...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

소프트 삭제가 적용된 모델이라면 `index-settings` 배열 내에서 해당 모델의 인덱스 필터링이 자동으로 지원됩니다. 별도 필터나 정렬 속성이 없다면 빈 배열로 설정해도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

인덱스 설정을 변경한 후에는 반드시 `scout:sync-index-settings` Artisan 명령어를 실행해 Meilisearch에 설정 내용을 동기화해야 합니다. 배포 프로세스에 포함하는 것도 추천합니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정 (Configuring the Model ID)

기본적으로 Scout는 모델의 기본 키를 검색 인덱스에서 모델 고유 키로 사용합니다. 이 동작을 변경하려면 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용될 값 반환
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용될 키 이름 반환
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정 (Configuring Search Engines per Model)

검색 시 기본적으로 `scout` 설정 파일에 정의된 기본 검색 엔진이 사용됩니다. 하지만 특정 모델에 대해 검색 엔진을 바꾸고 싶으면 모델의 `searchableUsing` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\EngineManager;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 모델 인덱싱에 사용할 엔진 반환
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별 (Identifying Users)

Scout는 [Algolia](https://algolia.com)를 사용할 때 인증된 사용자를 자동으로 식별해 연동할 수 있습니다. 이 기능은 Algolia 대시보드에서 사용자별 검색 분석에 유용합니다. 사용하려면 `.env` 파일에 `SCOUT_IDENTIFY`를 `true`로 설정하세요:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화 하면 요청 IP 주소와 인증된 사용자의 고유 식별자가 Algolia에 전달되어 검색 요청과 연결됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]  
> 데이터베이스 엔진은 현재 MySQL 및 PostgreSQL을 지원합니다.

작거나 중간규모 데이터베이스나 낮은 부하 환경이라면 Scout의 "database" 엔진을 사용하는 게 편리합니다. 이 엔진은 기존 데이터베이스에서 `where like` 절과 전체 텍스트 인덱스를 활용해 쿼리 결과를 필터링하여 검색 결과를 산출합니다.

사용하려면 `.env` 파일의 `SCOUT_DRIVER` 값을 `database`로 설정하거나 `scout` 설정 파일에서 `database` 드라이버를 지정하세요:

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 설정한 후 [검색 가능한 데이터](#configuring-searchable-data)를 설정하고, 곧바로 [검색 기능](#searching)을 사용할 수 있습니다. Algolia, Meilisearch, Typesense 같은 서드파티 검색 엔진에 데이터를 인덱싱하는 절차가 불필요합니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 검색 가능한 모든 모델 속성에 대해 `where like` 쿼리를 실행합니다. 하지만 상황에 따라 성능이 좋지 않을 수 있습니다. 따라서 일부 컬럼에 대해 전체 텍스트 검색을 하거나, 문자열 전체가 아닌 접두사 일치(`example%`)만 검색하는 전략을 별도로 지정할 수 있습니다.

이를 위해 `toSearchableArray` 메서드에 PHP 속성(attributes)을 부여하세요. 추가 검색 전략이 지정되지 않은 컬럼은 기본 `where like` 전략을 따릅니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱싱 가능한 데이터 배열을 반환합니다.
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
> 컬럼에 전체 텍스트 검색을 지정하기 전에 해당 컬럼에 전체 텍스트 인덱스가 생성되어 있는지 확인하세요. ([전체 텍스트 인덱스 문서](/docs/10.x/migrations#available-index-types))

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

Algolia, Meilisearch, Typesense 엔진 대신 로컬 개발 환경에서 간단히 사용하려면 "collection" 엔진을 선택할 수 있습니다. 이 엔진은 기존 데이터베이스에서 `where` 절과 컬렉션 필터링으로 검색 결과를 산출하며, 모델 인덱싱 작업은 필요 없습니다.

사용하려면 `.env` 파일에 `SCOUT_DRIVER`를 `collection`으로 설정하거나 `scout` 설정 파일에서 `collection` 드라이버를 지정하세요:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 설정했다면, 곧바로 [검색](#searching)을 수행할 수 있습니다. Algolia, Meilisearch, Typesense 같은 검색 엔진에 인덱싱할 필요가 없습니다.

#### 데이터베이스 엔진과의 차이점

"database"와 "collection" 엔진 모두 데이터베이스를 직접 조회한다는 점에서 유사하지만, 컬렉션 엔진은 전체 텍스트 인덱스나 `LIKE` 절을 사용하지 않습니다. 대신 모든 레코드를 가져와 Laravel의 `Str::is` 헬퍼로 속성 값에 검색어가 포함됐는지 판별합니다.

컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스에서 작동하며(SQLite, SQL Server 포함) 가장 포터블하지만, database 엔진보다는 효율성이 떨어집니다.

<a name="indexing"></a>
## 인덱싱 (Indexing)

<a name="batch-import"></a>
### 일괄 가져오기 (Batch Import)

기존 프로젝트에 Scout를 도입할 때 미리 저장된 데이터가 있다면, `scout:import` Artisan 명령어로 모든 레코드를 검색 인덱스에 가져올 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

모델 인덱스에서 모든 레코드를 삭제하려면 `flush` 명령을 사용합니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 일괄 저장 쿼리 커스터마이징

일괄 가져오기에 사용할 쿼리를 수정하고 싶으면 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 여기서 관계를 eager 로드하는 등 쿼리 최적화를 할 수 있습니다:

```
use Illuminate\Database\Eloquent\Builder;

/**
 * 일괄 검색 가능 처리 시 모델 조회 쿼리 수정
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]  
> 큐를 사용해 일괄 가져올 때는 `makeAllSearchableUsing` 메서드가 적용되지 않을 수 있습니다. 모델 컬렉션이 작업 큐에서 처리될 때 관계 복원이 이루어지지 않습니다. (/docs/10.x/queues#handling-relationships)

<a name="adding-records"></a>
### 레코드 추가 (Adding Records)

`Laravel\Scout\Searchable` 트레이트를 쓰는 모델에서 인스턴스를 `save` 또는 `create` 하면 자동으로 검색 인덱스에도 저장됩니다. 큐를 사용하는 경우 백그라운드에서 큐 워커가 처리합니다:

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리에 `searchable` 메서드를 체인으로 호출하여 레코드 컬렉션을 인덱스에 추가할 수 있습니다. 내부적으로 결과를 청크 단위로 나누어 작업하며, 큐를 사용하면 비동기로 처리됩니다:

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에도 `searchable` 메서드를 호출할 수 있습니다:

```
$user->orders()->searchable();
```

이미 메모리 내에 Eloquent 모델 컬렉션이 있을 경우에도 `searchable` 메서드를 사용할 수 있습니다:

```
$orders->searchable();
```

> [!NOTE]  
> `searchable` 메서드는 "upsert" 연산과 같습니다. 즉, 인덱스에 이미 있다면 업데이트, 없으면 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

모델 속성을 변경하고 `save` 하면 검색 인덱스도 자동으로 업데이트됩니다:

```
use App\Models\Order;

$order = Order::find(1);

// 주문 내용 수정...

$order->save();
```

쿼리 인스턴스에 `searchable`을 호출해 해당 조건에 맞는 모델 컬렉션을 업데이트할 수도 있습니다. 인덱스에 없다면 새로 생성됩니다:

```
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스에서도 `searchable` 호출이 가능합니다:

```
$user->orders()->searchable();
```

모델 컬렉션에도 호출할 수 있습니다:

```
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 임포트 전 레코드 수정

검색 가능 처리 전에 컬렉션을 조작해야 할 경우(예: 관계 eager loading), 모델에 `makeSearchableUsing` 메서드를 정의하세요:

```
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능 처리 중인 모델 컬렉션 조작
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제 (Removing Records)

검색 인덱스에서 제거하려면 모델을 데이터베이스에서 `delete`하면 됩니다. 소프트 삭제 모델도 지원합니다:

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 직접 조회하지 않고 삭제하려면 쿼리 인스턴스에 `unsearchable` 메서드를 사용하세요:

```
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스에서도 호출 가능합니다:

```
$user->orders()->unsearchable();
```

모델 컬렉션에서 호출해도 적용됩니다:

```
$orders->unsearchable();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지 (Pausing Indexing)

한 번에 여러 모델 작업을 하면서 인덱스 동기화를 막고 싶을 때는 `withoutSyncingToSearch` 메서드에 클로저를 넘겨 사용합니다. 클로저 내에서 수행된 작업은 인덱스에 반영되지 않습니다:

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스 (Conditionally Searchable Model Instances)

특정 조건에서만 모델을 검색 가능하게 하고 싶다면, `shouldBeSearchable` 메서드를 모델에 정의하세요. 예를 들어, `App\Models\Post`가 "draft" 또는 "published" 상태일 때, "published" 상태만 검색 가능하도록 할 수 있습니다:

```
/**
 * 모델이 검색 가능해야 하는지 판단
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`, `create`, 쿼리 또는 관계를 통한 조작에만 적용됩니다. `searchable` 메서드를 직접 호출하면 이 메서드 결과를 무시합니다.

> [!WARNING]  
> 데이터베이스 엔진 사용 시 `shouldBeSearchable` 메서드가 적용되지 않습니다. 항상 검색 가능한 데이터가 DB에 저장되기 때문입니다. 데이터베이스 엔진에서는 대신 [where 절](#where-clauses)을 활용하세요.

<a name="searching"></a>
## 검색 (Searching)

모델에서 `search` 메서드를 호출해 검색을 시작할 수 있습니다. 검색어를 문자열로 넘기고, `get` 메서드를 연쇄 호출해 결과 모델들을 조회합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout는 검색 결과를 Eloquent 모델 컬렉션으로 반환하므로, 라우트나 컨트롤러에서 그대로 반환하면 JSON으로 자동 변환됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과를 Eloquent 모델로 변환하기 전의 원본 데이터가 필요하면 `raw` 메서드를 사용하세요:

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

검색 시 기본적으로 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 지정한 인덱스를 사용합니다. 특정 인덱스에서 검색하고 싶으면 `within` 메서드를 이용하세요:

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### where 절 (Where Clauses)

Scout 검색 쿼리에 간단한 "where" 조건을 추가할 수 있습니다. 현재는 숫자 동등 검사 위주이며, 주로 소유자 ID 기준 제한에 유용합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn`을 사용해 컬럼 값이 지정한 배열에 포함되는지 검사할 수 있습니다:

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

반대로 `whereNotIn`은 컬럼 값이 배열에 포함되지 않을 때 결과에 포함합니다:

```
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스가 관계형 DB가 아니기 때문에 더 복잡한 where 조건은 지원하지 않습니다.

> [!WARNING]  
> Meilisearch 사용 시에는 Scout의 where 절을 사용하기 전에 반드시 [필터 가능 속성 설정](#configuring-filterable-data-for-meilisearch)을 완료해야 합니다.

<a name="pagination"></a>
### 페이징 (Pagination)

`paginate` 메서드로 검색 결과 페이지네이션을 사용할 수 있습니다. 이 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환하므로 일반 Eloquent 페이징과 같이 다룰 수 있습니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

1페이지당 결과 수를 지정하려면 `paginate` 첫 인자로 숫자를 넘기세요:

```
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 Blade에서 출력하고 페이지 링크를 렌더링하는 예:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

API로 JSON 응답을 반환하려면 페이지네이터 인스턴스를 그대로 리턴하면 됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]  
> 검색 엔진은 Eloquent 모델의 글로벌 스코프를 인지하지 못하므로, Scout 페이징을 사용하는 애플리케이션에서는 글로벌 스코프 사용을 피하거나 검색 시 글로벌 스코프 조건을 재구현해야 합니다.

<a name="soft-deleting"></a>
### soft deleting

소프트 삭제된 모델을 인덱스에도 저장하면서 검색하려면, `config/scout.php` 파일에서 `soft_delete` 옵션을 `true`로 설정하세요:

```
'soft_delete' => true,
```

이 설정이 활성화되면 Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고 `__soft_deleted` 숨김 속성을 설정합니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드를 포함하거나 검색할 수 있습니다:

```
use App\Models\Order;

// 소프트 삭제 포함 검색
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 레코드만 검색
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]  
> `forceDelete`로 영구 삭제 시에는 Scout가 인덱스에서 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

검색 엔진 동작을 고급으로 커스터마이즈하려면 `search` 메서드 두 번째 인자로 클로저를 넘기세요. 예를 들어 Algolia 검색에 지리 위치 필터를 추가할 수 있습니다:

```
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
#### Eloquent 결과 쿼리 커스터마이징

Scout가 검색 엔진에서 일치하는 모델 ID를 가져온 후, Eloquent를 통해 실제 모델들을 조회합니다. 이때 `query` 메서드에 클로저를 전달해 Eloquent 쿼리 빌더를 직접 조작할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

단, 이 콜백은 이미 검색 엔진 결과 후 호출되므로, 결과 "필터링"용이 아니라 연관 데이터 로딩 등 용도로만 사용하세요. 필터링은 [Scout where 절](#where-clauses)을 써야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기

기본 제공 엔진으로 필요 기능을 구현할 수 없을 경우, 직접 커스텀 엔진을 작성해 Scout에 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 확장해야 하고, 아래 여덟 가지 메서드를 반드시 구현해야 합니다:

```
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

작성 시 `Laravel\Scout\Engines\AlgoliaEngine` 클래스 구현을 참고하면 많은 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진을 작성한 후 Laravel 서비스 컨테이너에서 Scout의 엔진 매니저(`EngineManager`)를 받아 `extend` 메서드로 등록하세요. 이 코드는 보통 `App\Providers\AppServiceProvider`나 다른 서비스 프로바이더의 `boot` 메서드에 작성합니다:

```
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

등록한 후에는 `config/scout.php` 설정 파일에서 기본 드라이버로 지정할 수 있습니다:

```
'driver' => 'mysql',
```