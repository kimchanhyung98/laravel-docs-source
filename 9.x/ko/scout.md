# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [드라이버 전제 조건](#driver-prerequisites)
    - [큐잉](#queueing)
- [설정](#configuration)
    - [모델 인덱스 구성](#configuring-model-indexes)
    - [검색 가능 데이터 구성](#configuring-searchable-data)
    - [모델 ID 구성](#configuring-the-model-id)
    - [모델별 검색 엔진 구성](#configuring-search-engines-per-model)
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
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)
- [빌더 매크로](#builder-macros)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)은 간단하고 드라이버 기반의 풀텍스트 검색 기능을 [Eloquent 모델들](/docs/9.x/eloquent)에 추가할 수 있는 솔루션입니다. 모델 옵저버를 사용하여 Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [MeiliSearch](https://www.meilisearch.com), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본으로 포함합니다. 또한 Scout는 컬렉션 드라이버도 포함하는데, 이는 로컬 개발 환경에서 사용하도록 설계되었으며 외부 의존성이나 타사 서비스를 요구하지 않습니다. 무엇보다도, 커스텀 드라이버 작성이 간단하며 자신만의 검색 구현체로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 통해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

Scout를 설치한 후에는 `vendor:publish` Artisan 명령어를 사용하여 Scout 설정 파일을 발행해야 합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 복사합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여 모델과 검색 드라이버 간 동기화를 자동으로 수행합니다:

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

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건 (Driver Prerequisites)

<a name="algolia"></a>
#### Algolia

Algolia 드라이버를 사용할 때는 Algolia `id`와 `secret` 자격증명을 `config/scout.php` 설정 파일에 구성해야 합니다. 자격증명을 구성한 후에는 Composer를 통해 Algolia PHP SDK를 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
#### MeiliSearch

[MeiliSearch](https://www.meilisearch.com)는 매우 빠르고 오픈소스인 검색 엔진입니다. 로컬 머신에 MeiliSearch 설치 방법이 궁금하다면 Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/9.x/sail#meilisearch)을 사용할 수 있습니다.

MeiliSearch 드라이버를 사용할 때는 Composer를 통해 MeiliSearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 다음, 애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 MeiliSearch `host`, `key` 자격증명을 설정합니다:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

MeiliSearch에 관한 더 자세한 내용은 [MeiliSearch 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, MeiliSearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 버전을 설치했는지 [MeiliSearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)에서 꼭 확인해야 합니다.

> [!WARNING]
> MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 MeiliSearch 서비스 자체의 [추가적인 중단 변경사항](https://github.com/meilisearch/MeiliSearch/releases)을 반드시 검토해야 합니다.

<a name="queueing"></a>
### 큐잉 (Queueing)

Scout를 사용하기 위해 반드시 필요한 것은 아니지만, [큐 드라이버](/docs/9.x/queues)를 설정하는 것을 강력히 권장합니다. 큐 워커를 실행하면 모델 데이터를 검색 인덱스와 동기화하는 작업들이 큐에 쌓이고, 웹 인터페이스의 응답 시간 개선에 큰 도움이 됩니다.

큐 드라이버를 설정한 후, `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 설정하세요:

```
'queue' => true,
```

`queue` 옵션이 `false`로 설정되어 있어도, Algolia와 Meilisearch 같은 일부 Scout 드라이버는 항상 비동기식으로 레코드를 인덱싱하니 참고하세요. 즉, Laravel 애플리케이션 내에서 인덱싱 작업은 완료되었더라도 검색 엔진에 반영되기까지 시간이 걸립니다.

Scout 작업에 사용할 연결과 큐를 명시적으로 지정하려면 `queue` 옵션을 배열 형태로 정의할 수 있습니다:

```
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 구성 (Configuring Model Indexes)

각 Eloquent 모델은 "인덱스"라는 검색 공간과 동기화되며, 이 인덱스에는 해당 모델에 대한 모든 검색 가능한 레코드가 저장됩니다. 쉽게 말해 각 인덱스는 MySQL 테이블과 같은 개념입니다. 기본적으로 각 모델은 모델 이름의 복수형과 일치하는 인덱스 이름에 저장됩니다. 다만, 모델 내 `searchableAs` 메서드를 오버라이드하면 인덱스 이름을 자유롭게 설정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 이 모델에 연관된 인덱스 이름을 반환합니다.
     *
     * @return string
     */
    public function searchableAs()
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능 데이터 구성 (Configuring Searchable Data)

기본적으로, 특정 모델의 전체 `toArray` 결과가 검색 인덱스에 저장됩니다. 인덱스에 동기화할 데이터를 직접 커스터마이징하고 싶다면, 모델의 `toSearchableArray` 메서드를 오버라이드하면 됩니다:

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
     * @return array
     */
    public function toSearchableArray()
    {
        $array = $this->toArray();

        // 데이터 배열을 커스터마이징하세요...

        return $array;
    }
}
```

MeiliSearch와 같은 일부 검색 엔진은 필터 연산자(`>`, `<` 등)를 적용할 때 정해진 타입의 데이터만 허용하므로, 검색 가능 데이터를 커스터마이징할 때는 숫자 값들은 반드시 정확한 타입으로 캐스팅해야 합니다:

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
#### 필터 가능 데이터 및 인덱스 설정 구성 (MeiliSearch)

Scout의 다른 드라이버와 달리, MeiliSearch는 필터 가능 속성(filterable attributes), 정렬 가능 속성(sortable attributes), 그리고 [기타 지원 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 사전에 정의해야 합니다.

필터 가능 속성은 Scout의 `where` 메서드를 사용할 때 필터링하려는 속성을 의미하고, 정렬 가능 속성은 `orderBy` 메서드를 사용할 때 정렬 기준이 되는 속성입니다. 인덱스 설정을 정의하려면 애플리케이션 `scout` 설정 파일의 `meilisearch` 항목 내 `index-settings` 부분을 다음과 같이 조정하세요:

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

만약 인덱스와 연관된 모델이 소프트 삭제를 지원하며 `index-settings` 배열에 포함되어 있다면, Scout는 자동으로 해당 인덱스에서 소프트 삭제된 모델을 필터링할 수 있도록 지원합니다. 별도의 필터 가능 속성이나 정렬 가능 속성을 정의할 필요가 없다면 빈 배열만 추가해도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 완료한 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해야 합니다. 이 명령어는 MeiliSearch에 현재 설정된 인덱스 구성을 알려줍니다. 배포 프로세스에 이 명령어를 포함시키는 것이 편리합니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 구성 (Configuring The Model ID)

기본적으로 Scout는 모델의 기본 키를 고유한 식별자(ID)로 사용하여 검색 인덱스에 저장합니다. 이 행동을 변경하고 싶다면 모델 내 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용될 모델의 고유 값을 반환합니다.
     *
     * @return mixed
     */
    public function getScoutKey()
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용될 키 이름을 반환합니다.
     *
     * @return mixed
     */
    public function getScoutKeyName()
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 구성 (Configuring Search Engines Per Model)

검색 시, 기본적으로 애플리케이션의 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 그러나 특정 모델에 대해 검색 엔진을 변경하려면 해당 모델의 `searchableUsing` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\EngineManager;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 이 모델에 사용될 검색 엔진을 반환합니다.
     *
     * @return \Laravel\Scout\Engines\Engine
     */
    public function searchableUsing()
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별 (Identifying Users)

Scout는 [Algolia](https://algolia.com) 사용 시 자동으로 사용자를 식별하는 기능을 제공합니다. 인증된 사용자를 검색 작업과 연관시키면 Algolia 대시보드에서 검색 분석에 도움이 됩니다. 이 기능은 애플리케이션 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 정의하여 활성화할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면 요청의 IP 주소와 인증된 사용자의 기본 식별자를 Algolia에 전달하여 검색 요청에 이 데이터가 함께 포함되도록 합니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

소규모에서 중규모 데이터베이스를 다루거나 작업 부하가 적은 애플리케이션이라면 Scout의 "database" 엔진을 사용하는 것이 편리할 수 있습니다. 데이터베이스 엔진은 기존 데이터베이스에서 결과를 필터링할 때 "where like" 절과 풀텍스트 인덱스를 사용하여 적절한 검색 결과를 결정합니다.

데이터베이스 엔진을 사용하려면, 애플리케이션 `.env` 파일 또는 `scout` 설정 파일에 `SCOUT_DRIVER` 값을 `database`로 지정하세요:

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 드라이버로 지정하면, [검색 가능 데이터](#configuring-searchable-data)를 설정한 뒤 [검색 쿼리 실행](#searching)이 가능합니다. Algolia나 MeiliSearch 인덱싱 같은 별도의 검색 인덱스 생성 작업은 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [검색 가능하도록 구성한](#configuring-searchable-data) 모든 모델 속성에 대해 "where like" 쿼리를 수행합니다. 그러나 경우에 따라 성능 저하가 생길 수 있으므로, 일부 컬럼은 풀텍스트 검색을 사용하거나 문자열의 접두사만 검색하는 방식 (`example%`)을 이용하도록 검색 전략을 설정할 수 있습니다.

이 동작은 `toSearchableArray` 메서드에 PHP 속성(Attribute)을 할당하여 지정합니다. 추가 검색 전략이 적용되지 않은 컬럼은 기본적으로 "where like" 전략을 계속 사용합니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱싱 가능 데이터 배열을 반환합니다.
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

> [!WARNING]
> 풀텍스트 쿼리를 사용할 컬럼을 지정하기 전에 해당 컬럼에 [풀텍스트 인덱스](/docs/9.x/migrations#available-index-types)가 설정되어 있는지 반드시 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

로컬 개발 환경에서는 Algolia나 MeiliSearch 대신 "collection" 엔진도 편리하게 사용할 수 있습니다. 컬렉션 엔진은 데이터베이스 조회 결과에 "where" 절과 컬렉션 필터링을 적용하여 검색 결과를 결정합니다. 이 엔진은 검색 가능 모델을 별도로 인덱싱할 필요 없이 로컬 데이터베이스에서 직접 조회합니다.

컬렉션 엔진을 사용하려면 `.env` 파일 혹은 `scout` 설정 파일에서 `SCOUT_DRIVER` 값을 `collection`으로 설정하세요:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 기본 드라이버로 지정한 후에는 [검색 쿼리 실행](#searching)이 가능하며, Algolia나 MeiliSearch 인덱싱 작업은 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이점

처음 봤을 때 "database"와 "collection" 엔진은 유사해 보이지만, 컬렉션 엔진은 풀텍스트 인덱스나 `LIKE` 절을 사용하지 않습니다. 대신 가능한 모든 레코드를 가져온 뒤 Laravel의 `Str::is` 헬퍼를 이용해 검색어가 모델 속성 값에 존재하는지 판단합니다.

컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스(SQLit, SQL Server 포함)에서 작동하는 가장 범용적인 검색 엔진이지만, 데이터베이스 엔진보다는 효율성이 떨어집니다.

<a name="indexing"></a>
## 인덱싱 (Indexing)

<a name="batch-import"></a>
### 일괄 가져오기 (Batch Import)

기존 프로젝트에 Scout를 도입하는 경우, 이미 DB에 저장된 데이터를 인덱스에 가져와야 할 수 있습니다. 이를 위해 Scout는 모든 기존 레코드를 검색 인덱스로 가져오는 `scout:import` Artisan 명령어를 제공합니다:

```shell
php artisan scout:import "App\Models\Post"
```

`flush` 명령어는 지정한 모델의 모든 검색 인덱스 레코드를 삭제합니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정하기

일괄 가져오기용 모델을 조회하는 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 이 메서드는 모든 모델을 인덱싱 전 미리 로드해야 할 연관관계(eager loading)를 설정할 때 유용합니다:

```
/**
 * 모든 모델을 검색 가능하도록 만들 때 사용할 쿼리를 수정합니다.
 *
 * @param  \Illuminate\Database\Eloquent\Builder  $query
 * @return \Illuminate\Database\Eloquent\Builder
 */
protected function makeAllSearchableUsing($query)
{
    return $query->with('author');
}
```

<a name="adding-records"></a>
### 레코드 추가 (Adding Records)

모델에 `Laravel\Scout\Searchable` 트레이트를 추가하면, 모델 인스턴스를 `save` 또는 `create` 할 때 자동으로 검색 인덱스에도 등록됩니다. 만약 [큐](#queueing)를 설정했다면, 이 작업은 백그라운드에서 큐 워커에 의해 수행됩니다:

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통해 레코드 추가

Eloquent 쿼리를 통해 모델 컬렉션을 검색 인덱스에 추가하려면, Eloquent 쿼리 빌더에 `searchable` 메서드를 체인으로 호출하세요. 이 메서드는 쿼리 결과를 나누어 가져와 검색 인덱스에 추가합니다. 큐를 설정했다면 각 청크(chunk)는 큐 워커가 백그라운드에서 처리합니다:

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에도 `searchable` 메서드를 호출할 수 있습니다:

```
$user->orders()->searchable();
```

이미 메모리에 Eloquent 모델 컬렉션이 있다면 컬렉션 인스턴스에 `searchable`을 호출해 대응하는 인덱스에 추가할 수 있습니다:

```
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert"(업데이트 또는 삽입) 작업으로 볼 수 있습니다. 즉, 인덱스에 이미 레코드가 존재하면 업데이트하고, 없으면 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

검색 가능 모델을 업데이트하려면, 모델 인스턴스의 속성을 수정한 후 `save`만 하면 됩니다. Scout가 자동으로 검색 인덱스에 변경 사항을 적용합니다:

```
use App\Models\Order;

$order = Order::find(1);

// 주문 업데이트...

$order->save();
```

Eloquent 쿼리 빌더에 `searchable`을 호출하면 컬렉션 단위로 인덱스를 업데이트할 수 있습니다. 인덱스에 없으면 새로 만듭니다:

```
Order::where('price', '>', 100)->searchable();
```

관계에 속한 모든 모델 인덱스를 업데이트하려면 관계 인스턴스에 `searchable`을 호출하세요:

```
$user->orders()->searchable();
```

컬렉션 인스턴스에 `searchable` 호출로 모델 인스턴스를 인덱스에 업데이트하는 것도 가능합니다:

```
$orders->searchable();
```

<a name="removing-records"></a>
### 레코드 제거 (Removing Records)

인덱스에서 레코드를 제거하려면, 데이터베이스에서 모델을 `delete` 하면 됩니다. 소프트 삭제 모델도 지원합니다:

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 먼저 조회하지 않고 바로 삭제하고 싶다면 Eloquent 쿼리 빌더에 `unsearchable` 메서드를 호출하세요:

```
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스에 대해 모든 검색 인덱스 레코드를 제거하려면 `unsearchable`을 호출할 수 있습니다:

```
$user->orders()->unsearchable();
```

컬렉션 인스턴스에 `unsearchable`을 호출하면 모델 인스턴스를 인덱스에서 제거합니다:

```
$orders->unsearchable();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지 (Pausing Indexing)

때로는 모델에 대해 일괄 작업을 수행하면서 인덱스 동기화를 잠시 멈춰야 할 경우가 있을 수 있습니다. 이때 `withoutSyncingToSearch` 메서드를 사용합니다. 이 메서드는 즉시 실행되는 클로저를 인수로 받고, 클로저 내부에서 발생하는 모든 모델 작업은 인덱스에 동기화되지 않습니다:

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스 (Conditionally Searchable Model Instances)

어떤 경우에는 특정 조건에 따라 모델을 검색 가능하게 만들고 싶을 수 있습니다. 예를 들어 `App\Models\Post` 모델이 "draft"(임시 저장) 상태와 "published"(게시됨) 상태를 가진다면, 오직 "published" 상태인 경우에만 검색 가능하도록 할 수 있습니다. 이때 모델에 `shouldBeSearchable` 메서드를 정의하세요:

```
/**
 * 모델이 검색 가능해야 하는지 여부를 판별합니다.
 *
 * @return bool
 */
public function shouldBeSearchable()
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`와 `create` 메서드, 쿼리, 관계를 통해 모델 작업 시에만 적용됩니다. 직접 `searchable` 메서드로 모델이나 컬렉션을 검색 가능하게 만들 경우 이 메서드의 반환값은 무시됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에서는 적용되지 않습니다. 왜냐하면 데이터베이스 엔진에서는 모든 검색 가능 데이터를 언제나 DB에 저장하기 때문입니다. 이 엔진 사용 시에는 [where 절](#where-clauses)을 이용해 필터링하는 방식으로 조건부 검색 구현을 해야 합니다.

<a name="searching"></a>
## 검색 (Searching)

모델에서 검색을 시작하려면 `search` 메서드를 사용하세요. 이 메서드는 한 개의 문자열을 인수로 받으며, 이 문자열로 모델들을 검색합니다. 검색 후 `get` 메서드를 체인해서 조건에 맞는 Eloquent 모델들을 가져올 수 있습니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션으로 반환되기 때문에, 라우트나 컨트롤러에서 바로 반환해도 JSON으로 자동 변환됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

원시 검색 결과를 Eloquent 모델로 변환되기 전에 그대로 받고 싶다면 `raw` 메서드를 사용하세요:

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 (Custom Indexes)

검색 쿼리는 보통 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 지정한 인덱스에서 실행됩니다. 필요하다면 `within` 메서드로 검색할 인덱스를 커스텀하게 지정할 수 있습니다:

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### where 절 (Where Clauses)

Scout에서는 간단한 "where" 절을 검색 쿼리에 추가할 수 있습니다. 현재 이 절들은 기본적인 숫자 동등 비교만 지원하며, 주로 소유자 ID 같은 검색 결과 범위 제한에 유용합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn` 메서드를 써서 특정 값 집합으로 결과를 제한할 수도 있습니다:

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['paid', 'open']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니므로, 더 복잡한 where 절은 현재 지원하지 않습니다.

> [!WARNING]
> MeiliSearch를 사용 중이라면 Scout의 "where" 절을 사용하기 전에 반드시 애플리케이션의 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 설정해야 합니다.

<a name="pagination"></a>
### 페이지네이션 (Pagination)

모델 컬렉션을 가져오는 대신, `paginate` 메서드로 검색 결과를 페이지 단위로 나눌 수 있습니다. 이 메서드는 전통적인 Eloquent 쿼리에서 페이지네이션을 했을 때와 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

한 페이지당 결과 개수를 지정하려면 `paginate` 메서드에 숫자를 전달하세요:

```
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 가져온 후, [Blade](/docs/9.x/blade)에서 전통적인 Eloquent 쿼리와 마찬가지로 다음과 같이 출력하고 페이지 네비게이션 링크를 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

물론, JSON으로 페이지네이션 결과를 바로 반환하고 싶다면 라우트나 컨트롤러에서 페이징 객체를 그대로 반환하면 됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프 정의를 인지하지 못하기 때문에, Scout 페이지네이션을 사용할 때 글로벌 스코프를 사용하지 않는 것이 좋습니다. 부득이하게 글로벌 스코프를 사용한다면, Scout 검색 시 글로벌 스코프 조건을 직접 재구현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

색인된 모델이 [소프트 삭제](/docs/9.x/eloquent#soft-deleting)를 지원하며, 소프트 삭제된 모델까지 검색 대상에 포함시키려면 `config/scout.php` 설정 파일 내 `soft_delete` 옵션을 `true`로 설정하세요:

```
'soft_delete' => true,
```

이 옵션이 `true`일 때, Scout는 소프트 삭제된 모델을 검색 인덱스에서 제거하지 않고 숨겨진 `__soft_deleted` 속성을 레코드에 설정합니다. 그 뒤 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해 소프트 삭제 레코드를 포함하거나 특정해서 검색할 수 있습니다:

```
use App\Models\Order;

// 소프트 삭제 포함하여 검색 결과 가져오기...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 것만 검색 결과에 포함하기...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델이 `forceDelete`로 영구 삭제되면, Scout는 자동으로 해당 모델을 검색 인덱스에서 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

검색 엔진의 동작을 고급으로 커스터마이징하려면, `search` 메서드 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어, Algolia 검색 시 지리 정보(geo-location)를 옵션에 추가할 수 있습니다:

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

Scout가 검색 엔진에서 일치하는 모델 ID 목록을 받으면, Eloquent를 통해 해당 기본 키로 모델들을 조회합니다. 이 Eloquent 쿼리 빌더는 `query` 메서드에 전달한 클로저를 통해 수정할 수 있습니다. 클로저는 Eloquent 쿼리 빌더 인스턴스를 인수로 받습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')
    ->query(fn ($query) => $query->with('invoices'))
    ->get();
```

이 콜백은 검색된 모델 목록을 받은 후 실행되므로, 결과 필터링 목적보다는 추가 관계 로딩 등 후처리에 활용하세요. 결과 필터링은 [Scout where 절](#where-clauses)을 사용해야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기 (Writing The Engine)

내장된 Scout 검색 엔진이 요구사항에 맞지 않는다면, 커스텀 엔진을 직접 작성하여 Scout에 등록할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 아래 8개 메서드를 구현해야 합니다:

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

`Laravel\Scout\Engines\AlgoliaEngine` 클래스 구현을 참고하면 각 메서드를 구현하는 좋은 출발점이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기 (Registering The Engine)

커스텀 엔진을 작성한 후에는 Scout 엔진 매니저의 `extend` 메서드를 통해 등록하세요. 엔진 매니저는 Laravel 서비스 컨테이너에서 해제할 수 있으며, `App\Providers\AppServiceProvider` 등의 서비스 프로바이더 `boot` 메서드 내에서 호출하는 것이 일반적입니다:

```
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
```

엔진 등록 후, 애플리케이션 `config/scout.php` 설정 파일에서 기본 Scout 드라이버(`driver`)를 등록한 엔진 이름으로 지정하세요:

```
'driver' => 'mysql',
```

<a name="builder-macros"></a>
## 빌더 매크로 (Builder Macros)

Scout 검색 빌더에 자신만의 커스텀 메서드를 추가하고 싶다면 `Laravel\Scout\Builder` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 매크로는 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드에서 정의합니다:

```
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
```

`macro` 함수는 첫 번째 인자로 매크로 이름, 두 번째 인자로 클로저를 받으며, `Laravel\Scout\Builder` 인스턴스에서 매크로 이름으로 호출 시 클로저가 실행됩니다:

```
use App\Models\Order;

Order::search('Star Trek')->count();
```