# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 사전 준비](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 수정](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이즈](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색을 간편하게 추가할 수 있도록, 드라이버 기반의 솔루션을 제공합니다. Scout는 모델 옵저버를 사용하여, Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

Scout는 현재 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본으로 지원합니다. 또한, 외부 종속성과 써드파티 서비스 없이 로컬 개발을 위한 “collection” 드라이버가 내장되어 있습니다. 그 외에 직접 커스텀 드라이버 작성도 쉬워 본인만의 검색엔진 구현을 Scout에 확장하여 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 통해 Scout를 설치합니다:

```shell
composer require laravel/scout
```

설치 후, `vendor:publish` Artisan 명령어로 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령은 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 생성합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가해 주세요. 이 트레이트는 모델 옵저버를 등록하여, 해당 모델을 검색 드라이버와 자동 동기화합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="queueing"></a>
### 큐잉

Scout 사용 시 필수는 아니지만, [큐 드라이버](/docs/{{version}}/queues) 설정을 강력히 권장합니다. 큐 워커를 사용하면 모델 정보를 검색 인덱스에 동기화하는 모든 작업이 큐잉되어, 웹 인터페이스의 응답 속도가 현저히 개선됩니다.

큐 드라이버를 설정했다면, `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 지정하세요:

    'queue' => true,

`queue` 옵션이 `false`여도, Algolia와 Meilisearch 같은 일부 Scout 드라이버는 항상 비동기적으로 인덱싱을 수행함을 잊지 마세요. 즉, 라라벨 애플리케이션 입장에서는 인덱싱 작업이 끝났더라도, 검색 엔진에 데이터가 실시간으로 반영되지 않을 수 있습니다.

Scout 작업에서 사용할 연결(connection)과 큐 이름을 지정하려면, `queue` 설정 옵션을 배열 형태로 지정할 수 있습니다:

    'queue' => [
        'connection' => 'redis',
        'queue' => 'scout'
    ],

물론, Scout 작업에 사용할 연결과 큐를 커스터마이징한 경우, 해당 연결 및 큐를 처리하는 워커를 실행해야 합니다:

    php artisan queue:work redis --queue=scout

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용하려면, `config/scout.php` 설정 파일에서 Algolia의 `id`와 `secret` 자격증명을 반드시 지정해야 합니다. 설정 이후, Composer로 Algolia PHP SDK도 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬에서 Meilisearch를 설치하는 방법을 잘 모르는 경우에는 [Laravel Sail](/docs/{{version}}/sail#meilisearch)을 활용할 수 있습니다.

Meilisearch 드라이버를 사용할 때는 다음과 같이 PHP SDK를 설치하세요:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고, `.env` 파일에서 `SCOUT_DRIVER` 환경 변수 및 Meilisearch의 `host`, `key` 자격증명을 설정해야 합니다:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 추가 정보는 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용하는 Meilisearch 바이너리 버전에 호환되는 `meilisearch/meilisearch-php` 버전을 설치해야 합니다. 호환성은 [Meilisearch 바이너리 호환성 가이드](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하세요.

> [!WARNING]  
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는, [Meilisearch 서비스에 추가적으로 생길 수 있는 주요 변경사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 확인하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 키워드 검색, 의미 기반 검색, 지오 검색, 벡터 검색을 지원하는 초고속 오픈 소스 검색 엔진입니다.

직접 [셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면, Typesense PHP SDK를 Composer로 설치하세요:

```shell
composer require typesense/typesense-php
```

그리고 `.env` 파일에서 `SCOUT_DRIVER` 및 Typesense 호스트와 API 키를 지정하세요:

```env
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

필요하다면 포트, 경로, 프로토콜도 지정할 수 있습니다:

```env
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션에 대한 추가 설정 값과 스키마 정의는 `config/scout.php` 파일에서 할 수 있습니다. 보다 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비하기

Typesense를 사용할 때는, 검색 가능한 모델에 `toSearchableArray` 메소드를 정의하여 모델의 기본키를 문자열로, 생성 날짜를 UNIX 타임스탬프로 캐스팅해야 합니다:

```php
/**
 * Get the indexable data array for the model.
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

Typesense 컬렉션의 필드 데이터 타입과 같은 스키마도 `config/scout.php` 파일에 정의해야 합니다. 스키마 설정의 자세한 필드 옵션은 [Typesense 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

컬렉션의 스키마를 변경해야 하는 경우, `scout:flush` 및 `scout:import`를 실행하여 인덱스된 데이터를 초기화하고 새 스키마로 다시 인덱싱하거나, Typesense API를 사용해 컬렉션 스키마만 수정할 수도 있습니다.

소프트 삭제 기능을 사용하는 경우, `config/scout.php`의 해당 모델 스키마 정의 내에 `__soft_deleted` 필드를 포함시켜야 합니다:

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

Typesense는 `options` 메소드를 통해 검색 시 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 지정할 수 있습니다:

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

각 Eloquent 모델은 해당 모델의 모든 검색 가능한 레코드를 포함한 특정 검색 "인덱스"와 동기화됩니다. 즉, 마치 각 인덱스를 MySQL 테이블처럼 생각할 수 있습니다. 기본적으로 각 모델은 그 모델의 일반적인 "table" 이름과 일치하는 인덱스에 저장됩니다(보통은 복수형). 필요하다면, 모델의 `searchableAs` 메소드를 오버라이드하여 인덱스명을 커스터마이징할 수 있습니다:

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

<a name="configuring-searchable-data"></a>
### 검색 데이터 설정

기본적으로, 모델의 `toArray` 데이터 전체가 검색 인덱스에 저장됩니다. 저장되는 데이터를 커스터마이즈하려면, 모델의 `toSearchableArray` 메소드를 오버라이드 하세요:

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

            // 데이터 배열 커스터마이즈...

            return $array;
        }
    }

Meilisearch 등 일부 검색 엔진은 올바른 데이터 타입에만 필터 연산(`>`, `<` 등)을 사용할 수 있으므로, 검색 데이터 커스터마이즈 시 숫자 값은 반드시 정확한 타입으로 캐스팅해야 합니다:

    public function toSearchableArray()
    {
        return [
            'id' => (int) $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
        ];
    }

<a name="configuring-filterable-data-for-meilisearch"></a>
#### Meilisearch의 필터/인덱스 설정

Scout의 다른 드라이버와 달리 Meilisearch는 필터 가능한 필드, 정렬 가능한 필드 등의 인덱스 검색 설정을 미리 정의해야 합니다.  
필터 가능한 필드는 `where` 메소드로 필터링할 속성, 정렬 가능한 필드는 `orderBy`로 정렬할 속성입니다. 다음 예시처럼 `scout` 설정 파일의 `meilisearch` 엔트리의 `index-settings` 부분을 수정하세요:

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

해당 인덱스의 모델이 소프트 삭제를 지원하고 `index-settings`에 포함된 경우, 해당 인덱스에 대해 소프트 삭제 필터링도 자동 적용됩니다. 필터/정렬 필드 없이 소프트 삭제 모델만 관리할 경우 빈 배열을 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후, `scout:sync-index-settings` Artisan 명령어를 반드시 실행해야 합니다.  
이 명령은 Meilisearch에 설정을 동기화합니다. 배포 프로세스의 일부로 이 명령을 자동화하는 것이 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본키를 인덱스에서 고유 ID/키로 사용합니다. 이 동작을 변경하려면, 모델에서 `getScoutKey`와 `getScoutKeyName`을 오버라이드하세요:

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

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

Scout는 검색 시 기본적으로 `scout` 설정 파일에서 지정한 기본 검색 엔진을 사용합니다. 하지만, 특정 모델에서 사용할 검색 엔진을 바꾸고 싶다면 모델에 `searchableUsing` 메소드를 오버라이드할 수 있습니다:

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
         * Get the engine used to index the model.
         */
        public function searchableUsing(): Engine
        {
            return app(EngineManager::class)->engine('meilisearch');
        }
    }

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시, 인증된 사용자를 검색 요청에 연동할 수 있습니다. 이 기능은 Algolia 대시보드에서 검색 분석 시 유용할 수 있습니다.  
`.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하면 사용자를 식별할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 사용하면 요청의 IP 주소와 인증 사용자의 기본 식별자가 Algolia로 전달되어 해당 검색 요청에 연동됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]  
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

소규모 또는 중간 크기의 데이터베이스를 다루거나 비교적 가벼운 워크로드일 경우 Scout의 "database" 엔진을 사용하는 것이 더 편리할 수 있습니다.  
데이터베이스 엔진은 쿼리 결과를 가져올 때 기존 데이터베이스에서 "where like" 조건문과 전체 텍스트 인덱스를 활용해 검색 결과를 필터링합니다.

이 엔진을 사용하려면 `.env`에서 `SCOUT_DRIVER` 환경변수를 `database`로 지정하거나, `scout` 설정 파일에서 드라이버를 `database`로 지정하면 됩니다:

```ini
SCOUT_DRIVER=database
```

설정 후에는 [검색 데이터 구성](#configuring-searchable-data)을 마친 뒤, 바로 [검색 쿼리 실행](#searching)이 가능합니다.  
Algolia, Meilisearch, Typesense와는 달리 인덱싱 시드 작업은 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이즈

기본적으로 데이터베이스 엔진은 [검색 데이터](#configuring-searchable-data)로 지정된 모든 컬럼에 대해 "where like" 쿼리를 실행합니다. 하지만 이 방법은 성능에 문제가 있을 수 있으므로, 일부 컬럼에 대해 전체 텍스트 검색(full text search) 또는 접두사 기반의 "where like" 제약(`example%`)만 사용하도록 전략을 변경할 수 있습니다.

이 동작은 모델의 `toSearchableArray` 메소드에 PHP 어트리뷰트를 부여해 구체적으로 지정할 수 있습니다. 추가적 검색 전략이 지정되지 않은 컬럼은 기본 "where like" 전략을 사용합니다:

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
> 전체 텍스트 쿼리 제약을 지정하기 전에, 해당 컬럼에 [full text index](/docs/{{version}}/migrations#available-index-types)가 생성되어 있는지 반드시 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발에서 Algolia, Meilisearch, Typesense 엔진을 꼭 사용할 필요 없이, "collection" 엔진으로 더 간편하게 시작할 수 있습니다.  
컬렉션 엔진은 기존 데이터베이스에서 결과를 가져와 "where" 절 및 Laravel 컬렉션의 필터로 검색 결과를 도출합니다.  
이 엔진은 별도의 인덱싱 없이 로컬 데이터베이스에서 모델을 바로 조회합니다.

이 엔진을 사용하려면 `.env`에서 `SCOUT_DRIVER`를 `collection`으로 지정하거나, `scout` 설정 파일에서 드라이버를 `collection`으로 지정하세요:

```ini
SCOUT_DRIVER=collection
```

설정 후, [검색 쿼리 실행](#searching)만 하면 됩니다.  
인덱싱(예: Algolia, Meilisearch, Typesense 인덱스 파일 생성)은 불필요합니다.

#### 데이터베이스 엔진과의 차이점

표면적으로 "database"와 "collection" 엔진은 비슷해 보이지만,  
데이터베이스 엔진은 전체 텍스트 인덱스나 `LIKE` 절로 검색하는 데 비해,  
컬렉션 엔진은 가능한 레코드를 모두 가져와 Laravel의 `Str::is` 헬퍼로 검색어 포함 여부를 체크합니다.

컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스(심지어 SQLite, SQL Server 등)에서 동작하므로 이동성이 가장 높습니다. 다만, database 엔진보다 효율성은 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 일괄 가져오기

기존 프로젝트에 Scout를 도입하는 경우, 이미 존재하는 데이터베이스 레코드를 검색 인덱스에 가져와야 할 수 있습니다.  
Artisan의 `scout:import` 명령어로 모든 레코드를 손쉽게 인덱스에 추가할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

모델의 모든 레코드를 검색 인덱스에서 제거하려면 `flush` 명령을 사용하세요:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정하기

일괄 인덱싱시 모델 가져오는 쿼리를 커스터마이즈하려면 모델에 `makeAllSearchableUsing` 메소드를 정의하세요.  
이곳에서 관계 데이터의 eager loading 등 필요한 사전처리를 할 수 있습니다:

    use Illuminate\Database\Eloquent\Builder;

    /**
     * Modify the query used to retrieve models when making all of the models searchable.
     */
    protected function makeAllSearchableUsing(Builder $query): Builder
    {
        return $query->with('author');
    }

> [!WARNING]  
> 큐를 사용해 일괄 인덱싱을 진행하는 경우에는 `makeAllSearchableUsing`이 적용되지 않을 수 있습니다.  
> 큐에서는 [관계가 복원되지 않습니다](/docs/{{version}}/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

`Laravel\Scout\Searchable` 트레이트를 모델에 추가하면, 해당 모델을 `save` 또는 `create` 할 때마다 자동으로 검색 인덱스에 반영됩니다.  
Scout에서 [큐](#queueing)를 사용할 경우, 이 작업은 큐워커에서 처리됩니다:

    use App\Models\Order;

    $order = new Order;

    // ...

    $order->save();

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가하기

여러 모델을 Eloquent 쿼리로 검색 인덱스에 추가하려면, 쿼리 뒤에 `searchable` 메소드를 체이닝하세요.  
이 메소드는 [결과를 청크(chunk)](/docs/{{version}}/eloquent#chunking-results)로 나눠 인덱스에 추가합니다.  
Scout가 큐를 사용한다면, 각 청크는 큐워커가 백그라운드로 가져와 처리합니다:

    use App\Models\Order;

    Order::where('price', '>', 100)->searchable();

Eloquent 관계에 대해서도 `searchable` 메소드를 호출할 수 있습니다:

    $user->orders()->searchable();

컬렉션에 모델 인스턴스가 이미 담겨 있다면, 컬렉션에 `searchable`을 호출해 각 인스턴스를 인덱스에 추가할 수 있습니다:

    $orders->searchable();

> [!NOTE]  
> `searchable` 메소드는 "upsert" 작업을 수행합니다. 즉, 이미 존재하는 경우 데이터를 업데이트하고, 없다면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 수정

검색되는 모델의 속성을 업데이트한 뒤 `save` 하면, Scout가 자동으로 인덱스에 해당 내용을 반영합니다:

    use App\Models\Order;

    $order = Order::find(1);

    // 주문 수정...

    $order->save();

Eloquent 쿼리 인스턴스에서 `searchable`을 호출하면 여러 모델을 한 번에 갱신할 수 있습니다. 인덱스에 존재하지 않는 모델은 새로 생성됩니다:

    Order::where('price', '>', 100)->searchable();

관계에 대해서도 `searchable`을 호출할 수 있습니다:

    $user->orders()->searchable();

컬렉션에도 동일하게 호출 가능합니다:

    $orders->searchable();

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 데이터 수정

인덱싱 전 모델 컬렉션을 조정하고 싶을 때(ex. 관계 eager load 필요 등),  
모델에 `makeSearchableUsing` 메소드를 정의하세요:

    use Illuminate\Database\Eloquent\Collection;

    /**
     * Modify the collection of models being made searchable.
     */
    public function makeSearchableUsing(Collection $models): Collection
    {
        return $models->load('author');
    }

<a name="removing-records"></a>
### 레코드 삭제

검색 인덱스에서 레코드를 제거하려면, 단순히 데이터베이스에서 모델을 `delete` 하면 됩니다.
[소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 모델도 지원합니다:

    use App\Models\Order;

    $order = Order::find(1);

    $order->delete();

별도로 모델을 조회하지 않고 삭제하려면 쿼리 인스턴스에 `unsearchable`을 호출하세요:

    Order::where('price', '>', 100)->unsearchable();

관계에도 사용할 수 있습니다:

    $user->orders()->unsearchable();

컬렉션 전체에 대해서도 가능합니다:

    $orders->unsearchable();

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

모델의 데이터를 검색 인덱스에 동기화하지 않고 일련의 Eloquent 작업을 실행하고 싶을 때는  
`withoutSyncingToSearch` 메소드를 사용하면 됩니다. 이 메소드는 단일 클로저를 인자로 받으며,  
클로저 내에서 발생한 모델 동작들은 인덱스에 동기화되지 않습니다:

    use App\Models\Order;

    Order::withoutSyncingToSearch(function () {
        // 모델 작업 수행...
    });

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스

모델이 특정 조건일 때만 검색 가능하도록 제한하고 싶다면, 예를 들어,  
`App\Models\Post`에 "draft"(초안)과 "published"(발행됨) 상태가 있을 때,  
"published"인 경우에만 검색 가능하도록 하려면, 모델에 `shouldBeSearchable` 메소드를 정의하세요:

    /**
     * Determine if the model should be searchable.
     */
    public function shouldBeSearchable(): bool
    {
        return $this->isPublished();
    }

`shouldBeSearchable` 메소드는 `save`, `create` 메소드 또는 쿼리, 관계 처리 시에만 적용됩니다.  
`searchable` 메소드로 직접 모델이나 컬렉션을 인덱싱하면 이 조건은 무시됩니다.

> [!WARNING]  
> "database" 엔진을 사용하는 경우에는 `shouldBeSearchable` 메소드가 적용되지 않습니다.  
> 모든 검색 데이터는 항상 데이터베이스에 저장됩니다.  
> 이 엔진에서 유사 동작을 하려면 [where 절](#where-clauses)을 사용하세요.

<a name="searching"></a>
## 검색

`search` 메소드를 이용해 검색을 시작할 수 있습니다. 이 메소드는 검색어 문자열을 받아 해당 조건을 가진 Eloquent 모델을 반환하며, 이어서 `get` 메소드를 체이닝해 실제 결과를 가져옵니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->get();

Scout로 반환된 결과는 Eloquent 모델의 컬렉션이므로, 라우트나 컨트롤러에서 바로 반환하면  
자동으로 JSON으로 변환됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/search', function (Request $request) {
        return Order::search($request->search)->get();
    });

Eloquent 모델로 변환되지 않은 "원본" 검색 결과를 얻으려면, `raw` 메소드를 사용하세요:

    $orders = Order::search('Star Trek')->raw();

<a name="custom-indexes"></a>
#### 커스텀 인덱스

통상적으로는 모델의 [`searchableAs`](#configuring-model-indexes) 메소드에서 지정된 인덱스를 검색합니다.  
하지만 `within` 메소드를 사용해 다른 인덱스에서 검색할 수 있습니다:

    $orders = Order::search('Star Trek')
        ->within('tv_shows_popularity_desc')
        ->get();

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있도록 지원합니다.  
이 절은 주로 기본적인 숫자 동등성(equality) 체크용이며, 소유자 ID 등으로 스코프를 제한하는 데 사용됩니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->where('user_id', 1)->get();

`whereIn` 메소드로 특정 배열 내 값만 검색할 수도 있습니다:

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['open', 'paid']
    )->get();

`whereNotIn` 메소드는 값이 주어진 배열에 없는 경우만 반환합니다:

    $orders = Order::search('Star Trek')->whereNotIn(
        'status', ['closed']
    )->get();

검색 인덱스는 관계형 데이터베이스가 아니므로, 이보다 더 복잡한 where 절은 지원하지 않습니다.

> [!WARNING]  
> Meilisearch를 사용하는 경우, Scout의 "where" 문을 사용하기 전에  
> 반드시 [filterable attributes](#configuring-filterable-data-for-meilisearch) 설정을 마쳐야 합니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 그대로 가져오는 것 외에도, `paginate` 메소드로 페이지네이션이 가능합니다.  
이 메소드는 [Eloquent 쿼리 페이지네이션](/docs/{{version}}/pagination)과 동일하게  
`Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->paginate();

페이지당 개수를 지정하려면 첫 번째 인자로 전달하세요:

    $orders = Order::search('Star Trek')->paginate(15);

결과를 화면에 표시하고 페이지네이션 링크를 렌더링하려면 [Blade](/docs/{{version}}/blade)를 사용하세요:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 반환하려면,  
라우트나 컨트롤러에서 paginator 인스턴스를 그대로 반환하면 됩니다.

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        return Order::search($request->input('query'))->paginate(15);
    });

> [!WARNING]  
> 검색 엔진은 Eloquent 모델의 글로벌 스코프(global scope) 정보를 알지 못하므로,  
> Scout 페이지네이션을 쓰는 애플리케이션에서는 글로벌 스코프 사용을 지양하거나,  
> 검색 시 동일한 조건을 수동으로 추가해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

검색 대상 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 사용하고,  
소프트 삭제된 데이터도 검색하고 싶다면, `config/scout.php`의 `soft_delete` 옵션을 `true`로 지정하세요:

    'soft_delete' => true,

이 설정이 활성화되면 Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고,  
인덱스된 레코드에 숨겨진 `__soft_deleted` 속성을 부여합니다.  
이후에는 `withTrashed` 또는 `onlyTrashed` 메소드로 소프트 삭제된 레코드를 검색할 수 있습니다:

    use App\Models\Order;

    // 삭제된 레코드 포함
    $orders = Order::search('Star Trek')->withTrashed()->get();

    // 삭제 레코드만
    $orders = Order::search('Star Trek')->onlyTrashed()->get();

> [!NOTE]  
> 소프트 삭제된 모델이 `forceDelete`로 완전히 삭제되면, Scout는 자동으로 인덱스에서 해당 항목을 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이즈

검색 엔진의 동작을 고급으로 커스터마이즈해야 할 경우,  
`search` 메소드의 두 번째 인자로 클로저를 전달할 수 있습니다.  
예를 들어, Algolia에 지오로케이션 필터 옵션을 추가하려면 다음과 같이 합니다:

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

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 결과 쿼리 커스터마이즈

Scout가 검색 엔진에서 매칭되는 모델 키 목록을 가져오면,  
Eloquent가 해당 키들을 바탕으로 쿼리를 한 번 더 수행하게 됩니다.  
이 쿼리를 커스터마이즈 하려면 `query` 메소드에 클로저를 넘겨주세요.
이 클로저에는 Eloquent 쿼리 빌더 인스턴스가 전달됩니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

주의: 이 콜백은 이미 검색 엔진에서 매칭된 키가 결정된 이후에 작동하므로,  
여기서는 필터링 용도가 아니라 단순한 수정이나 eager loading 등에 활용해야 합니다.  
필터링이 필요하다면 [Scout where 절](#where-clauses)을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

내장 Scout 검색 엔진으로 충분하지 않은 경우,  
직접 커스텀 엔진을 작성해 Scout에 등록할 수 있습니다.  
엔진은 반드시 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며,  
아래 8개 메소드를 필수로 구현해야 합니다:

    use Laravel\Scout\Builder;

    abstract public function update($models);
    abstract public function delete($models);
    abstract public function search(Builder $builder);
    abstract public function paginate(Builder $builder, $perPage, $page);
    abstract public function mapIds($results);
    abstract public function map(Builder $builder, $results, $model);
    abstract public function getTotalCount($results);
    abstract public function flush($model);

각 메소드의 구현 예시는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스에서 확인하면 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 작성했다면, Scout 엔진 매니저의 `extend` 메소드로 등록할 수 있습니다.  
엔진 매니저는 라라벨 서비스 컨테이너에서 resolve 가능합니다.  
애플리케이션의 `App\Providers\AppServiceProvider` 혹은 기타 서비스 프로바이더의 `boot` 메소드에서 호출하는 것이 보통입니다:

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

등록 후에는 애플리케이션의 `config/scout.php` 파일에서 Scout의 기본 `driver`로  
작성한 엔진을 지정하면 됩니다:

    'driver' => 'mysql',
