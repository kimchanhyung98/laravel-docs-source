# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [큐 사용](#queueing)
- [구성](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 대상 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [배치 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제(Soft Deleting)](#soft-deleting)
    - [엔진별 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)
- [빌더 매크로](#builder-macros)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색을 추가하기 위한 간단한, 드라이버 기반의 솔루션을 제공합니다. 모델 옵저버를 사용하여, Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [MeiliSearch](https://www.meilisearch.com), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 지원합니다. 추가로, Scout에는 외부 의존성이나 서드파티 서비스 없이 로컬 개발 환경에서 사용하기 좋은 "collection" 드라이버도 포함되어 있습니다. 또한, 직접 커스텀 드라이버를 작성하는 것도 매우 간단하며, 자신만의 검색 엔진을 자유롭게 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 통해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

Scout를 설치한 후에는 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 배포해야 합니다. 이 명령을 실행하면 `scout.php` 설정 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 대상으로 만들 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여, 모델이 검색 드라이버와 자동으로 동기화되도록 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비

<a name="algolia"></a>
#### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 파일에서 Algolia `id`와 `secret` 자격증명을 설정해야 합니다. 자격증명을 설정한 뒤, Composer 패키지 매니저로 Algolia PHP SDK도 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
#### MeiliSearch

[MeiliSearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬 환경에 MeiliSearch를 설치하는 방법을 잘 모를 경우, Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/{{version}}/sail#meilisearch)을 사용할 수 있습니다.

MeiliSearch 드라이버를 사용할 경우, Composer로 MeiliSearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그런 다음, 애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 MeiliSearch의 `host`, `key` 값을 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

MeiliSearch에 대한 자세한 설명은 [MeiliSearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, [MeiliSearch-php 바이너리 호환성 관련 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하여, 사용하는 MeiliSearch 바이너리 버전에 호환 가능한 `meilisearch/meilisearch-php` 버전을 설치해야 합니다.

> **경고**  
> MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때에는, 항상 [MeiliSearch 서비스의 파괴적 변경 사항](https://github.com/meilisearch/MeiliSearch/releases)이 있는지 확인해야 합니다.

<a name="queueing"></a>
### 큐 사용

Scout를 사용하는 데 필수는 아니지만, [큐 드라이버](/docs/{{version}}/queues)를 미리 설정하면 더 나은 응답 시간을 경험할 수 있습니다. 큐 워커를 실행하면, Scout가 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐에 삽입하여 웹 인터페이스의 응답 속도를 대폭 개선할 수 있습니다.

큐 드라이버를 설정한 후, `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 설정하세요:

    'queue' => true,

`queue` 옵션이 `false`로 설정되어 있더라도, Algolia나 Meilisearch 같은 일부 Scout 드라이버는 항상 비동기로 레코드를 인덱싱한다는 점을 유념해야 합니다. 즉, Laravel 애플리케이션에서 인덱스 작업이 완료되어도, 실제 검색 엔진 결과 반영이 바로 이루어지지 않을 수 있습니다.

Scout 작업이 사용할 연결과 큐를 지정하려면, `queue` 구성을 배열로 정의할 수 있습니다:

    'queue' => [
        'connection' => 'redis',
        'queue' => 'scout'
    ],

<a name="configuration"></a>
## 구성

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

각 Eloquent 모델은 해당 모델에 대한 모든 검색 가능한 레코드를 저장하는 특정 검색 "인덱스"와 동기화됩니다. 즉, 각 인덱스는 MySQL의 테이블처럼 생각할 수 있습니다. 기본적으로는 각 모델이 테이블명과 일치하는 인덱스에 저장됩니다. 대체로 이 값은 모델 이름의 복수형이 사용됩니다. 하지만, 모델의 `searchableAs` 메서드를 오버라이드하여 인덱스명을 자유롭게 지정할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델에 연결된 인덱스의 이름 반환.
         *
         * @return string
         */
        public function searchableAs()
        {
            return 'posts_index';
        }
    }

<a name="configuring-searchable-data"></a>
### 검색 대상 데이터 설정

기본적으로, 해당 모델의 `toArray` 형태 전체가 검색 인덱스에 보관됩니다. 인덱스에 동기화될 데이터를 커스터마이즈하려면, 모델에서 `toSearchableArray` 메서드를 오버라이드할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델을 인덱싱할 데이터 배열 반환.
         *
         * @return array
         */
        public function toSearchableArray()
        {
            $array = $this->toArray();

            // 데이터 배열 커스터마이징...

            return $array;
        }
    }

MeiliSearch와 같이 데이터 타입에 따라 필터 연산(`>`, `<` 등)이 가능한 검색 엔진에서는, 숫자값을 정확한 타입으로 캐스팅해야 필터링이 정상 동작됩니다:

    public function toSearchableArray()
    {
        return [
            'id' => (int) $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
        ];
    }

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터/정렬 속성 및 인덱스 설정(MeiliSearch)

Scout의 다른 드라이버와 달리, MeiliSearch는 필터링 가능 속성과 정렬 가능 속성 등 [지원되는 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 미리 정의해야 합니다.

필터링 가능 속성은 Scout의 `where` 메서드로 필터링할 속성이고, 정렬 가능 속성은 `orderBy` 메서드로 정렬할 속성입니다. 인덱스 설정은 `scout` 설정 파일의 `meilisearch` 항목에서 `index-settings`를 통해 정의할 수 있습니다:

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

해당 인덱스가 소프트 딜리트 가능한 모델일 경우, `index-settings` 배열에 모델이 포함돼 있으면 자동으로 소프트 딜리트 필터링 지원이 설정됩니다. 딱히 다른 필터/정렬 속성이 필요 없는 경우, 아래처럼 빈 항목만 추가해도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 `scout:sync-index-settings` Artisan 명령어를 반드시 실행하여, MeiliSearch에 인덱스 설정 정보를 반영해야 합니다. 배포 자동화에 포함시키면 편리합니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키(primary key)를 검색 인덱스에 저장하는 모델의 고유 ID/키로 사용합니다. 이 동작을 커스터마이즈하려면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * 모델 인덱싱에 사용할 값 반환.
         *
         * @return mixed
         */
        public function getScoutKey()
        {
            return $this->email;
        }

        /**
         * 모델 인덱싱에 사용할 키 명 반환.
         *
         * @return mixed
         */
        public function getScoutKeyName()
        {
            return 'email';
        }
    }

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

보통 Scout는 `scout` 설정 파일의 기본 검색 엔진을 사용합니다. 하지만, 특정 모델에서 사용할 검색 엔진을 변경하려면 `searchableUsing` 메서드를 오버라이드하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\EngineManager;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * 모델 인덱싱에 사용할 엔진 반환.
         *
         * @return \Laravel\Scout\Engines\Engine
         */
        public function searchableUsing()
        {
            return app(EngineManager::class)->engine('meilisearch');
        }
    }

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시 사용자 자동 식별도 지원합니다. 인증된 사용자를 검색 요청과 연계하면, Algolia 대시보드에서 검색 분석 시 유용하게 활용할 수 있습니다. 사용자 식별 기능은 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하여 활성화할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면 요청의 IP 주소와 인증된 사용자의 기본 키도 Algolia에 전달되어, 검색 요청 데이터와 연관됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> **경고**  
> 데이터베이스 엔진은 현재 MySQL 및 PostgreSQL만 지원합니다.

애플리케이션이 소규모~중간 규모 DB를 사용하거나, 부하가 가벼울 경우 Scout의 "database" 엔진으로 빠르게 시작할 수 있습니다. DB 엔진은 기존 DB에서 "where like" 절과 전체 텍스트 인덱스를 활용하여 검색 쿼리에 맞는 결과를 걸러냅니다.

데이터베이스 엔진 사용 방법은, `.env` 파일에서 `SCOUT_DRIVER` 변수를 `database`로 설정하거나, 설정 파일에서 `database` 드라이버를 직접 지정하면 됩니다:

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진이 선택되면 [검색 대상 데이터 설정](#configuring-searchable-data)을 반드시 완료하세요. 그 후 [검색 쿼리 실행](#searching)이 가능합니다. Algolia/MeiliSearch처럼 별도 인덱싱을 위한 시딩 작업이 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 database 엔진은 [검색 대상으로 설정된](#configuring-searchable-data) 모든 모델 속성에 "where like" 쿼리를 실행합니다. 하지만 성능에 문제가 있을 경우, 특정 컬럼을 전체 텍스트 검색 또는 접두어만 검색하는 "where like"로 지정할 수 있습니다.

이 설정은 모델의 `toSearchableArray`에 PHP 속성(Attributes)을 추가해 정의합니다. 별도 검색 전략이 없는 컬럼은 기본 "where like"를 유지합니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델 검색 대상 데이터 배열을 반환.
 *
 * @return array
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray()
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```

> **경고**  
> 전체 텍스트 인덱스를 사용하는 컬럼을 지정할 경우, 해당 컬럼에 [FullText 인덱스](/docs/{{version}}/migrations#available-index-types)가 적용되어 있는지 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발에서 Algolia나 MeiliSearch 대신 "collection" 엔진으로 간편히 시작할 수 있습니다. 컬렉션 엔진은 기존 DB에서 쿼리 결과를 불러온 후, "where" 절과 Laravel의 컬렉션 필터링 기능을 사용합니다. 인덱싱 과정 없이, 모델은 로컬 DB에서 바로 읽어 집니다.

컬렉션 엔진 사용 방법은 `.env` 파일에서 `SCOUT_DRIVER` 변수를 `collection`으로 설정하거나 `scout` 설정 파일에서 직접 지정하면 됩니다:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버가 선택되면 바로 [검색 쿼리 실행](#searching)이 가능합니다. 별도의 인덱싱 작업이 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이점

언뜻 보면 "database"와 "collection" 엔진은 모두 DB에 직접 접근하는 점이 비슷하지만, collection 엔진은 full text 인덱스나 `LIKE` 쿼리를 쓰지 않고, 모든 레코드를 로드한 뒤 Laravel `Str::is` 헬퍼로 검색 문자열이 속성값에 포함되어 있는지 판별합니다.

컬렉션 엔진은 SQLite, SQL Server 등 Laravel이 지원하는 모든 관계형 DB에서 작동하기 때문에 가장 이식성이 높은 검색 엔진입니다. 단, database 엔진보다 효율성은 낮습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 가져오기

기존 프로젝트에 Scout를 도입하는 경우, 이미 DB에 저장된 레코드를 검색 인덱스에 가져와야 할 수 있습니다. Scout는 `scout:import` Artisan 명령어로 기존 레코드를 인덱스에 일괄 등록할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

모델 전체를 인덱스에서 제거하려면 `flush` 명령어를 사용하세요:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정

배치 가져오기 시점에 불러오는 모델 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 이곳에서 관계 로딩(eager loading) 등 필요한 로직을 추가할 수 있습니다:

    /**
     * 전체 모델을 검색 가능하게 만들 때 쿼리 수정.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return \Illuminate\Database\Eloquent\Builder
     */
    protected function makeAllSearchableUsing($query)
    {
        return $query->with('author');
    }

<a name="adding-records"></a>
### 레코드 추가

`Laravel\Scout\Searchable` 트레이트를 모델에 추가했다면, 단순히 `save`나 `create`로 모델을 저장하는 것만으로 자동으로 검색 인덱스에 추가됩니다. Scout를 [큐 작업과 연동](#queueing)하고 있다면, 이 동작도 백그라운드 큐 작업자로 처리됩니다:

    use App\Models\Order;

    $order = new Order;

    // ...

    $order->save();

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가

Eloquent 쿼리를 활용해 여러 모델을 인덱스에 추가하려면, Eloquent 쿼리 체인에 `searchable` 메서드를 사용하세요. 이 메서드는 쿼리 결과를 [청크 단위로 분할](/docs/{{version}}/eloquent#chunking-results)하여 인덱스에 추가합니다. 큐를 사용 중이면, 각 청크도 큐 워커가 백그라운드에서 처리합니다:

    use App\Models\Order;

    Order::where('price', '>', 100)->searchable();

Eloquent 관계 인스턴스에도 `searchable`을 호출할 수 있습니다:

    $user->orders()->searchable();

이미 Eloquent 모델이 담긴 컬렉션이 있다면, 컬렉션 인스턴스에 `searchable`을 호출해 해당 인스턴스를 인덱스에 추가할 수 있습니다:

    $orders->searchable();

> **참고**  
> `searchable` 메서드는 "업서트(upsert)" 동작을 합니다. 즉, 이미 인덱스에 있으면 업데이트, 없으면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 해당 모델의 속성값을 변경하고 `save` 하면 자동으로 검색 인덱스에 반영됩니다:

    use App\Models\Order;

    $order = Order::find(1);

    // 주문 정보 변경...

    $order->save();

Eloquent 쿼리 인스턴스에도 `searchable`을 호출해 다수 모델을 한 번에 업데이트할 수 있습니다. 인덱스에 없다면 새로 추가합니다:

    Order::where('price', '>', 100)->searchable();

관계형 모델의 인덱스도 `searchable`로 일괄 업데이트할 수 있습니다:

    $user->orders()->searchable();

모델 컬렉션이 있다면, 컬렉션의 `searchable` 메서드로 한번에 반영할 수 있습니다:

    $orders->searchable();

<a name="removing-records"></a>
### 레코드 제거

인덱스에서 레코드를 제거하려면, 단순히 해당 모델을 DB에서 `delete` 하면 됩니다. [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 모델도 동일합니다:

    use App\Models\Order;

    $order = Order::find(1);

    $order->delete();

모델 인스턴스를 굳이 불러오지 않고 바로 삭제하고 싶다면, Eloquent 쿼리에 `unsearchable`을 사용하세요:

    Order::where('price', '>', 100)->unsearchable();

관계형 모델도 `unsearchable`로 모든 인덱스 레코드를 제거할 수 있습니다:

    $user->orders()->unsearchable();

컬렉션 인스턴스에 `unsearchable`을 사용하여 인메모리 모델을 인덱스에서 제거할 수도 있습니다:

    $orders->unsearchable();

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

일시적으로 모델 인덱싱을 비활성화한 채 일괄적인 Eloquent 작업을 해야할 때는 `withoutSyncingToSearch` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 클로저를 파라미터로 받으며, 클로저 내부에서 수행된 모든 모델 조작이 인덱스에 반영되지 않습니다:

    use App\Models\Order;

    Order::withoutSyncingToSearch(function () {
        // 여러 모델 작업 수행...
    });

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

특정 조건에서만 모델을 검색 대상으로 만들고 싶을 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "임시 저장" 또는 "공개됨" 상태일 수 있고, 공개된 게시글만 인덱싱하고 싶다면, 모델에서 `shouldBeSearchable` 메서드를 정의하세요:

    /**
     * 이 모델이 검색 가능해야 할지 결정.
     *
     * @return bool
     */
    public function shouldBeSearchable()
    {
        return $this->isPublished();
    }

이 메서드는 `save`, `create`, 쿼리, 관계를 통한 모델 조작 시에 한해 동작합니다. `searchable` 메서드로 직접 인덱싱하면 이 메서드 결과는 무시됩니다.

> **경고**  
> "database" 엔진을 사용할 경우에는 `shouldBeSearchable`이 적용되지 않습니다. 이 때 비슷한 동작을 원하면 [where절](#where-clauses)을 사용하세요.

<a name="searching"></a>
## 검색

모델에서 `search` 메서드를 사용해 검색을 시작할 수 있습니다. 이 메서드에는 검색할 문자열을 인자로 넘기고, `get` 메서드를 체인하여 해당 검색어에 일치하는 Eloquent 모델 컬렉션을 반환받습니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->get();

Scout의 검색 결과는 Eloquent 모델 컬렉션이므로 라우트나 컨트롤러에서 바로 반환해도 자동으로 JSON 으로 변환됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/search', function (Request $request) {
        return Order::search($request->search)->get();
    });

Eloquent 모델로 변환되기 전의 원시 검색 결과를 받고 싶다면 `raw` 메서드를 사용할 수 있습니다:

    $orders = Order::search('Star Trek')->raw();

<a name="custom-indexes"></a>
#### 커스텀 인덱스

일반적으로 검색 쿼리는 모델의 [`searchableAs`](#configuring-model-indexes)로 지정된 인덱스에서 수행됩니다. 별도의 인덱스에서 검색하려면 `within` 메서드를 이용할 수 있습니다:

    $orders = Order::search('Star Trek')
        ->within('tv_shows_popularity_desc')
        ->get();

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 조건을 추가할 수 있습니다. 현재로서는 기본적인 숫자 동등(equality) 조건만 지원되며, 주로 소유자 ID 등으로 범위를 제한하는 데 유용합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->where('user_id', 1)->get();

`whereIn` 메서드로 지정값 집합에 포함된 결과로 제한할 수 있습니다:

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['paid', 'open']
    )->get();

검색 인덱스는 관계형 데이터베이스가 아니므로, 복잡한 "where" 절은 지원되지 않습니다.

> **경고**
> MeiliSearch 사용 시, 반드시 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)이 먼저 설정되어야 Scout의 "where" 절이 동작합니다.

<a name="pagination"></a>
### 페이지네이션

검색 결과를 컬렉션으로 반환하는 것 외에도, `paginate` 메서드로 페이지네이션이 가능합니다. 이 메서드는 [일반 Eloquent 페이지네이션](/docs/{{version}}/pagination)과 동일하게 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->paginate();

한 페이지에 가져올 모델 개수를 첫 번째 인자로 지정할 수 있습니다:

    $orders = Order::search('Star Trek')->paginate(15);

검색 결과와 페이지 링크 렌더링도 [Blade](/docs/{{version}}/blade)를 사용해 일반 쿼리 페이지네이션처럼 출력하면 됩니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 반환하려면, 라우트나 컨트롤러에서 paginator 인스턴스를 바로 반환하면 됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        return Order::search($request->input('query'))->paginate(15);
    });

> **경고**  
> 검색 엔진은 Eloquent 모델의 글로벌 스코프를 알지 못하므로, Scout 페이지네이션에서는 글로벌 스코프를 사용하면 안 됩니다. 필요하다면, 검색 시 직접 조건을 재구성해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제(Soft Deleting)

검색 인덱싱된 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원하며, 소프트 삭제된 모델 검색이 필요하다면 `config/scout.php`의 `soft_delete` 옵션을 `true`로 설정하세요:

    'soft_delete' => true,

이 경우, Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 인덱싱된 레코드에 숨겨진 `__soft_deleted` 속성을 추가합니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드까지 검색 결과에 포함할 수 있습니다:

    use App\Models\Order;

    // 소프트 삭제 포함 모든 결과
    $orders = Order::search('Star Trek')->withTrashed()->get();

    // 소프트 삭제된 결과만
    $orders = Order::search('Star Trek')->onlyTrashed()->get();

> **참고**  
> 소프트 삭제 모델이 `forceDelete`로 영구 삭제되면, Scout는 자동으로 인덱스에서 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진별 검색 커스터마이징

엔진의 검색 동작을 고급 커스터마이징해야 할 경우, `search` 메서드의 두 번째 인자에 클로저를 전달할 수 있습니다. 예를 들어, Algolia 검색 옵션에 지리 정보 데이터를 추가하고 싶으면 다음과 같이 할 수 있습니다:

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
#### Eloquent 결과 쿼리 커스터마이징

Scout가 검색 엔진에서 일치하는 Eloquent 모델의 ID를 얻은 뒤, 이를 기반으로 실제 모델 데이터를 다시 Eloquent 쿼리로 조회합니다. 이 때 `query` 메서드로 이 쿼리를 커스터마이징할 수 있습니다. `query`는 Eloquent 쿼리 빌더 인스턴스를 인자로 갖는 클로저를 받습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')
    ->query(fn ($query) => $query->with('invoices'))
    ->get();
```

이 콜백은 검색 엔진에서 해당 모델 키가 반환된 뒤에 실행되므로, 결과를 "필터링"하는 용도가 아니라 추가 쿼리 기능에만 사용하세요. 필터링이 필요하다면 [Scout의 where절](#where-clauses)을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

Scout 내장 검색 엔진이 요구사항에 맞지 않을 경우, 직접 커스텀 엔진을 작성하여 Scout에 등록할 수 있습니다. 커스텀 엔진은 반드시 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 아래 8개 메서드를 반드시 구현해야 합니다:

    use Laravel\Scout\Builder;

    abstract public function update($models);
    abstract public function delete($models);
    abstract public function search(Builder $builder);
    abstract public function paginate(Builder $builder, $perPage, $page);
    abstract public function mapIds($results);
    abstract public function map(Builder $builder, $results, $model);
    abstract public function getTotalCount($results);
    abstract public function flush($model);

이 메서드들은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스 구현을 참고하면 도움이 됩니다. 해당 구현을 참고하면, 각 메서드의 용도를 쉽게 파악할 수 있습니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

엔진을 작성한 후, Scout의 엔진 매니저의 `extend` 메서드로 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너로부터 받아옵니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드나, 필요한 서비스 프로바이더의 `boot` 메서드에서 호출하세요:

    use App\ScoutExtensions\MySqlSearchEngine
    use Laravel\Scout\EngineManager;

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        resolve(EngineManager::class)->extend('mysql', function () {
            return new MySqlSearchEngine;
        });
    }

엔진이 등록된 후에는, `config/scout.php`의 `driver` 설정에서 기본 드라이버로 지정하면 됩니다:

    'driver' => 'mysql',

<a name="builder-macros"></a>
## 빌더 매크로

Scout 검색 빌더(`Laravel\Scout\Builder`)에서 사용할 커스텀 메서드를 정의하고 싶다면, `macro` 메서드를 사용할 수 있습니다. 보통 "매크로"는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 선언하는 것이 일반적입니다:

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;
    use Laravel\Scout\Builder;

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        Builder::macro('count', function () {
            return $this->engine()->getTotalCount(
                $this->engine()->search($this)
            );
        });
    }

`macro` 함수는 첫 번째 인수로 매크로 이름, 두 번째 인수로 클로저를 받습니다. 정의 후에는 `Laravel\Scout\Builder` 구현 인스턴스에서 매크로 이름으로 호출할 수 있습니다:

    use App\Models\Order;

    Order::search('Star Trek')->count();
