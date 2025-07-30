# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [큐잉](#queueing)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [사용자 식별](#identifying-users)
- [로컬 개발](#local-development)
- [인덱싱](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 조건절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)
- [빌더 매크로](#builder-macros)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색 기능을 간단하게 추가할 수 있도록 드라이버 기반의 솔루션을 제공합니다. 모델 옵저버를 활용해, Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/)와 [MeiliSearch](https://www.meilisearch.com) 드라이버를 기본으로 제공하며, "collection" 드라이버는 로컬 개발용으로 설계되어 외부 의존성이나 서드파티 서비스 없이도 사용할 수 있습니다. 또한, 커스텀 드라이버 작성도 쉽고 자유롭게 자신만의 검색 구성을 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 통해 Scout를 설치하세요:

```
composer require laravel/scout
```

설치 후 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 배포합니다. 이 명령을 실행하면 `config` 디렉터리에 `scout.php` 설정 파일이 생성됩니다:

```
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여 모델과 검색 드라이버 간 동기화를 자동으로 처리합니다:

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
### 드라이버 사전 조건 (Driver Prerequisites)

<a name="algolia"></a>
#### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 파일에 Algolia `id`와 `secret` 인증 정보를 설정해야 합니다. 인증 정보를 구성한 후에는 Composer를 통해 Algolia PHP SDK를 설치해야 합니다:

```
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
#### MeiliSearch

[MeiliSearch](https://www.meilisearch.com)는 속도가 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬 설치 방법이 익숙하지 않다면, Laravel 공식 Docker 개발 환경인 [Laravel Sail](/docs/{{version}}/sail#meilisearch)을 사용할 수 있습니다.

MeiliSearch 드라이버를 사용하려면 Composer로 MeiliSearch PHP SDK를 설치해야 합니다:

```
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그런 다음, `.env` 파일 내에 `SCOUT_DRIVER` 환경 변수와 MeiliSearch `host` 및 `key` 인증 정보를 설정합니다:

```
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

추가 정보는 [MeiliSearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, MeiliSearch 바이너리 버전에 맞는 `meilisearch/meilisearch-php` 버전을 설치했는지 [호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 꼭 확인해야 합니다.

> [!NOTE]
> MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 반드시 [MeiliSearch 서비스의 추가적인 주요 변경 사항](https://github.com/meilisearch/MeiliSearch/releases)도 함께 검토하세요.

<a name="queueing"></a>
### 큐잉 (Queueing)

Scout 사용 시 큐 드라이버 설정이 필수는 아니지만, 큐 드라이버를 설정하는 것을 강력히 권장합니다. 큐 워커를 실행하면 검색 인덱스와 모델 데이터 동기화 작업을 백그라운드에서 처리하게 되어, 웹 애플리케이션의 반응 속도가 개선됩니다.

큐 드라이버 설정을 완료했다면 `config/scout.php` 설정 파일에서 `queue` 옵션을 `true`로 변경하세요:

```
'queue' => true,
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정 (Configuring Model Indexes)

각 Eloquent 모델은 해당 모델의 검색 가능한 레코드를 포함하는 검색 "인덱스"와 동기화됩니다. 간단히 말해, 각각의 인덱스는 MySQL 테이블과 비슷한 역할을 합니다. 기본적으로 모델 이름의 복수형에 해당하는 인덱스에 저장되지만, 모델의 `searchableAs` 메서드를 재정의해 인덱스 이름을 변경할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연동되는 인덱스 이름을 반환합니다.
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
### 검색 가능 데이터 설정 (Configuring Searchable Data)

기본적으로 모델의 `toArray` 메서드로 변환된 모든 데이터가 검색 인덱스에 저장됩니다. 저장할 데이터를 커스터마이징하려면 모델에서 `toSearchableArray` 메서드를 재정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 인덱싱할 데이터 배열을 반환합니다.
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
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정 (Configuring The Model ID)

기본적으로 Scout는 모델의 기본 키를 검색 인덱스에 저장할 모델 고유 ID / 키로 사용합니다. 이 동작을 변경하려면 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 재정의할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용될 값을 반환합니다.
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

<a name="identifying-users"></a>
### 사용자 식별 (Identifying Users)

Algolia를 사용할 때 Scout는 인증된 사용자를 자동 식별할 수도 있습니다. 이는 Algolia 대시보드에서 검색 분석을 할 때 유용합니다. 이 기능을 활성화하려면 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 정의하세요:

```
SCOUT_IDENTIFY=true
```

이 옵션을 켜면 요청 IP 주소와 인증 사용자 고유 식별자가 Algolia에 전달되어, 해당 사용자의 검색 요청과 함께 데이터가 연동됩니다.

<a name="local-development"></a>
## 로컬 개발 (Local Development)

로컬 개발 중에도 Algolia나 MeiliSearch를 사용할 수 있지만, "collection" 엔진이 더 편리할 수 있습니다. collection 엔진은 기존 데이터베이스의 결과를 "where" 조건 및 컬렉션 필터링 방식으로 처리해 검색 결과를 제공합니다. 이 엔진을 사용할 경우 별도의 인덱싱 작업 없이 로컬 DB에서 데이터를 바로 조회합니다.

collection 엔진을 사용하려면 `.env` 파일에서 `SCOUT_DRIVER` 값을 `collection`으로 설정하거나, `config/scout.php` 설정 파일에서 `collection` 드라이버를 명시하면 됩니다:

```ini
SCOUT_DRIVER=collection
```

collection 드라이버를 사용하면 [검색 쿼리 실행](#searching)이 바로 가능하며 Algolia나 MeiliSearch 인덱스 시드와 같은 인덱싱 작업을 수행할 필요가 없습니다.

<a name="indexing"></a>
## 인덱싱 (Indexing)

<a name="batch-import"></a>
### 일괄 가져오기 (Batch Import)

기존 프로젝트에 Scout를 도입할 경우, 이미 존재하는 데이터베이스 레코드를 검색 인덱스로 가져와야 할 수 있습니다. Scout는 이를 위한 `scout:import` Artisan 명령을 제공합니다:

```
php artisan scout:import "App\Models\Post"
```

인덱스에서 해당 모델의 모든 레코드를 삭제하려면 `flush` 명령을 사용할 수 있습니다:

```
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정하기 (Modifying The Import Query)

가져오기 과정에서 모델 조회 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 예를 들어, eager loading이 필요한 관계를 불러오는 데 유용합니다:

```
/**
 * 검색 가능하게 만들기 위해 모델을 조회할 때 사용되는 쿼리를 수정합니다.
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

`Laravel\Scout\Searchable` 트레이트가 추가된 모델 인스턴스를 `save` 또는 `create`하면 자동으로 검색 인덱스에 반영됩니다. 큐를 설정한 경우 이 작업이 백그라운드에서 실행됩니다:

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가하기 (Adding Records Via Query)

Eloquent 쿼리에 `searchable` 메서드를 연결하면, 쿼리 결과를 청크(chunk) 단위로 나눠 검색 인덱스에 일괄적으로 추가합니다. 역시 큐를 설정했다면 백그라운드 작업으로 처리됩니다:

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에도 `searchable`을 호출할 수 있습니다:

```
$user->orders()->searchable();
```

메모리에 이미 있는 Eloquent 모델 컬렉션에도 `searchable`을 호출해 각 모델을 인덱스에 추가할 수 있습니다:

```
$orders->searchable();
```

> [!TIP]
> `searchable` 메서드는 일종의 "업서트(upsert)" 기능입니다. 즉, 인덱스에 존재하면 업데이트하고 없으면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

검색 가능 모델을 업데이트하려면 모델 속성을 변경하고 데이터베이스에 저장하면 됩니다. Scout가 자동으로 검색 인덱스에 변경 내용을 반영합니다:

```
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 수정...

$order->save();
```

또한, Eloquent 쿼리에서 `searchable` 메서드를 호출해 여러 모델을 한꺼번에 업데이트하거나, 없으면 생성할 수 있습니다:

```
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스에 호출하거나 컬렉션 인스턴스에 호출하여 관계 모델 또는 컬렉션 내 모델 전체의 인덱스 데이터를 업데이트할 수도 있습니다:

```
$user->orders()->searchable();

$orders->searchable();
```

<a name="removing-records"></a>
### 레코드 삭제 (Removing Records)

인덱스에서 레코드를 제거하려면 데이터베이스에서 해당 모델을 `delete`하면 됩니다. 이는 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 사용하는 모델도 지원합니다:

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

레코드를 삭제할 때 모델을 먼저 조회하고 싶지 않다면 Eloquent 쿼리에 `unsearchable` 메서드를 호출하세요:

```
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스 혹은 컬렉션 인스턴스에도 `unsearchable`을 호출하면 관계 모델 또는 컬렉션 모델 전체를 인덱스에서 제거합니다:

```
$user->orders()->unsearchable();

$orders->unsearchable();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지 (Pausing Indexing)

때때로 모델에서 발생하는 여러 작업을 한꺼번에 수행하면서 검색 인덱스 동기화를 막고 싶을 수 있습니다. 이럴 땐 `withoutSyncingToSearch` 메서드에 클로저를 넘겨 실행하세요. 클로저 내에서 모델 작업은 인덱스에 반영되지 않습니다:

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 여러 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스 (Conditionally Searchable Model Instances)

특정 조건에 맞을 때만 모델을 검색 가능하게 만들 수 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft"(초안)과 "published"(게시됨) 두 상태를 가질 때, 게시된 글만 검색 가능하도록 제한하려면 모델에 `shouldBeSearchable` 메서드를 정의하세요:

```
/**
 * 모델을 검색 가능하게 할지 여부를 판단합니다.
 *
 * @return bool
 */
public function shouldBeSearchable()
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`, `create`, 쿼리, 관계 작업으로 모델을 조작할 때만 적용됩니다. 반면, `searchable` 메서드를 직접 호출해서 모델 또는 컬렉션을 처리하는 경우에는 이 메서드 결과가 무시됩니다.

<a name="searching"></a>
## 검색 (Searching)

`search` 메서드를 사용해 모델 검색을 시작할 수 있습니다. 이 메서드는 검색어 문자열 하나를 인수로 받아 해당 조건에 맞는 모델을 검색합니다. 이후에는 `get` 메서드를 연결해 검색 결과를 Eloquent 모델 컬렉션으로 반환받으세요:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

검색 결과가 Eloquent 모델 컬렉션으로 반환되므로, 라우트나 컨트롤러에서 바로 리턴하면 자동으로 JSON 변환되어 응답됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과를 Eloquent 모델로 변환하기 전 원본 데이터가 필요하다면 `raw` 메서드를 사용하세요:

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 (Custom Indexes)

검색은 기본적으로 모델의 [`searchableAs`](#configuring-model-indexes) 메서드가 지정한 인덱스에서 수행됩니다. 하지만 `within` 메서드를 사용하면 다른 이름의 인덱스에서 검색하도록 지정할 수도 있습니다:

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 조건절 (Where Clauses)

Scout는 검색 쿼리에 간단한 "where" 조건을 추가할 수 있게 지원합니다. 현재는 기본 숫자 동등 비교만 가능하며, 주로 소유자 ID로 검색 범위를 한정할 때 유용합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn` 메서드를 사용해 여러 값에 대해 결과를 제한할 수 있습니다:

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['paid', 'open']
)->get();
```

검색 인덱스는 관계형 DB가 아니기 때문에 더 복잡한 조건절은 지원하지 않습니다.

<a name="pagination"></a>
### 페이지네이션 (Pagination)

검색 결과 컬렉션뿐 아니라 `paginate` 메서드로 페이징 처리도 가능합니다. 이 메서드는 전통적인 Eloquent 쿼리에서 페이징할 때와 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

첫 번째 인수로 페이지당 결과 개수를 지정할 수도 있습니다:

```
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 받아 Blade 뷰에서 출력하고 페이지 링크를 렌더링하는 것도 일반 쿼리와 동일합니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

물론, 페이지네이터 인스턴스를 라우트나 컨트롤러에서 직접 리턴해 JSON으로 받을 수도 있습니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

인덱싱 중인 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원하고 삭제된 항목도 검색 대상으로 포함해야 한다면, `config/scout.php`의 `soft_delete` 옵션을 `true`로 설정하세요:

```
'soft_delete' => true,
```

이렇게 설정하면 Scout가 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 숨겨진 `__soft_deleted` 속성을 설정합니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해 삭제된 기록을 포함하거나 삭제된 것만 조회할 수 있습니다:

```
use App\Models\Order;

// 삭제된 데이터 포함
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된 데이터만
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!TIP]
> `forceDelete` 메서드로 완전 삭제하면 Scout가 자동으로 인덱스에서도 해당 데이터를 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

특정 검색 엔진의 동작을 고급으로 조정하려면 `search` 메서드의 두 번째 인수로 콜백 클로저를 전달하세요. 예를 들어 Algolia 검색 옵션에 지리 위치 데이터를 추가하는 방식입니다:

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

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기 (Writing The Engine)

내장된 Scout 검색 엔진이 필요에 맞지 않는다면, 자신만의 커스텀 엔진을 만들어 Scout와 연동할 수 있습니다. 이 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음 8개의 메서드를 구현해야 합니다:

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

이 메서드 구현 예시는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 이해에 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기 (Registering The Engine)

커스텀 엔진을 만들고 나면 Scout 엔진 매니저의 `extend` 메서드로 등록합니다. 엔진 매니저 클래스는 Laravel 서비스 컨테이너를 통해 얻으며, 이 등록 코드는 보통 `App\Providers\AppServiceProvider` 클래스나 다른 서비스 프로바이더 `boot` 메서드 안에서 호출합니다:

```
use App\ScoutExtensions\MySqlSearchEngine
use Laravel\Scout\EngineManager;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

등록을 완료하면, 애플리케이션 `config/scout.php` 설정 파일의 기본 `driver` 값을 커스텀 엔진 이름으로 지정하세요:

```
'driver' => 'mysql',
```

<a name="builder-macros"></a>
## 빌더 매크로 (Builder Macros)

Scout 검색 빌더에 커스텀 메서드를 추가하고 싶다면 `Laravel\Scout\Builder` 클래스의 `macro` 메서드를 활용하세요. 일반적으로 매크로 정의는 [서비스 프로바이더](/docs/{{version}}/providers) `boot` 메서드 내에서 작성합니다:

```
use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;
use Laravel\Scout\Builder;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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

`macro` 메서드는 첫번째 인수로 매크로 이름, 두번째 인수로 클로저를 받습니다. 이렇게 정의된 매크로는 `Laravel\Scout\Builder` 인스턴스에서 해당 이름으로 호출할 수 있습니다:

```
use App\Models\Order;

Order::search('Star Trek')->count();
```