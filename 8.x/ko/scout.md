# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [큐잉](#queueing)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능한 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [사용자 식별](#identifying-users)
- [로컬 개발 환경](#local-development)
- [인덱싱](#indexing)
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)
- [빌더 매크로](#builder-macros)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색을 간편하게 추가할 수 있는 드라이버 기반의 솔루션을 제공합니다. 모델 옵저버를 활용하여, Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/) 및 [MeiliSearch](https://www.meilisearch.com) 드라이버를 기본으로 제공합니다. 또한, 외부 의존성이나 서드파티 서비스 없이 로컬 개발을 위해 설계된 "collection" 드라이버도 포함되어 있습니다. 커스텀 드라이버 작성도 매우 간단하며, 여러분만의 검색 구현체로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저로 Scout를 설치하세요:

    composer require laravel/scout

설치가 완료되면, `vendor:publish` Artisan 명령어를 이용해 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리에 생성합니다:

    php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레잇을 추가하세요. 이 트레잇은 모델 옵저버를 등록하여, 검색 드라이버와 모델이 자동으로 동기화되도록 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="algolia"></a>
#### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 파일에 Algolia `id` 및 `secret` 정보를 설정해야 합니다. 자격 증명 설정 후, Composer 패키지 매니저로 Algolia PHP SDK도 설치해야 합니다:

    composer require algolia/algoliasearch-client-php

<a name="meilisearch"></a>
#### MeiliSearch

[MeiliSearch](https://www.meilisearch.com)는 매우 빠르고 오픈소스인 검색 엔진입니다. 로컬 머신에 MeiliSearch를 설치하는 방법을 잘 모르는 경우, [Laravel Sail](/docs/{{version}}/sail#meilisearch) 사용을 권장합니다.

MeiliSearch 드라이버를 사용할 때는 Composer로 MeiliSearch PHP SDK를 설치해야 합니다:

    composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle

그리고 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 MeiliSearch `host`, `key` 자격 증명을 추가하세요:

    SCOUT_DRIVER=meilisearch
    MEILISEARCH_HOST=http://127.0.0.1:7700
    MEILISEARCH_KEY=masterKey

MeiliSearch에 대한 더 많은 정보는 [MeiliSearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, [MeiliSearch의 바이너리 호환성에 대한 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하여 설치한 `meilisearch/meilisearch-php`의 버전이 바이너리와 호환되는지 확인해야 합니다.

> {note} MeiliSearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 항상 [MeiliSearch의 주요 변경 사항](https://github.com/meilisearch/MeiliSearch/releases)을 검토하세요.

<a name="queueing"></a>
### 큐잉

Scout를 사용하기 위해 꼭 필요하지는 않지만, 라이브러리 사용 전에 [큐 드라이버](/docs/{{version}}/queues) 설정을 강력히 권장합니다. 큐 워커를 구동하면 Scout가 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐에 넣어 처리할 수 있으므로, 웹 인터페이스의 응답 속도가 크게 개선됩니다.

큐 드라이버를 구성한 후에는 `config/scout.php` 파일의 `queue` 옵션 값을 `true`로 설정하세요:

    'queue' => true,

<a name="configuration"></a>
## 설정

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

각 Eloquent 모델은 해당 모델의 모든 검색 가능한 레코드를 포함하는 검색 "인덱스"와 동기화됩니다. 즉, 각 인덱스는 MySQL 테이블처럼 생각할 수 있습니다. 기본적으로 각 모델은 그 모델의 일반적인 "테이블" 이름과 일치하는 인덱스에 저장됩니다. 일반적으로 이는 모델 이름의 복수형으로 지정됩니다. 하지만, 모델의 `searchableAs` 메서드를 오버라이드하여 인덱스명을 자유롭게 커스터마이징할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델과 연관된 인덱스명을 반환합니다.
         *
         * @return string
         */
        public function searchableAs()
        {
            return 'posts_index';
        }
    }

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 설정

기본적으로, 주어진 모델의 전체 `toArray` 형태가 검색 인덱스에 저장됩니다. 인덱스에 동기화되는 데이터를 커스터마이징하려면, 모델에서 `toSearchableArray` 메서드를 오버라이드할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델의 인덱싱 데이터 배열 반환.
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

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키를 인덱스에 저장되는 고유 ID/키로 사용합니다. 이 동작을 커스터마이징하려면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * 모델을 인덱싱할 때 사용할 값 반환.
         *
         * @return mixed
         */
        public function getScoutKey()
        {
            return $this->email;
        }

        /**
         * 인덱싱에 사용할 키 이름 반환.
         *
         * @return mixed
         */
        public function getScoutKeyName()
        {
            return 'email';
        }
    }

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com)를 사용할 때, 사용자를 자동으로 식별할 수 있습니다. 인증된 사용자를 검색 작업과 연동하면 Algolia 대시보드에서 검색 분석을 볼 때 유용합니다. `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정해 활성화할 수 있습니다:

    SCOUT_IDENTIFY=true

이 기능을 활성화하면, 요청자의 IP 주소와 인증된 사용자의 기본 식별자가 Algolia로 전송되어 해당 사용자의 검색 요청에 이 데이터가 연결됩니다.

<a name="local-development"></a>
## 로컬 개발 환경

로컬 개발 중 Algolia나 MeiliSearch 검색 엔진을 자유롭게 사용할 수 있지만, "collection" 엔진을 사용하는 것이 더 간편할 수 있습니다. collection 엔진은 기존 데이터베이스의 결과에서 "where" 절 및 컬렉션 필터를 사용하여 검색 결과를 도출합니다. 이 엔진을 사용하면 검색 가능한 모델을 별도로 "인덱싱"할 필요 없이 데이터베이스에서 직접 조회합니다.

collection 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수를 `collection`으로 설정하거나, 애플리케이션의 scout 설정 파일에서 직접 지정하세요:

```ini
SCOUT_DRIVER=collection
```

collection 드라이버를 지정한 후, [검색 쿼리 실행](#searching)이 가능합니다. Algolia나 MeiliSearch 인덱싱처럼 별도의 인덱싱 작업은 필요하지 않습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 설치하는 경우, 이미 존재하는 데이터베이스 레코드들을 인덱스로 가져와야 할 수 있습니다. Scout는 `scout:import` Artisan 명령어를 제공하며, 이를 이용하면 기존 레코드 전체를 검색 인덱스로 임포트할 수 있습니다:

    php artisan scout:import "App\Models\Post"

`flush` 명령어로 모델의 모든 레코드를 인덱스에서 제거할 수 있습니다:

    php artisan scout:flush "App\Models\Post"

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 수정

배치 임포트에 사용되는 모델 쿼리를 수정하려면, 모델에 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 주로 임포트 전 Eager 로딩이 필요한 관계를 불러올 때 활용합니다:

    /**
     * 모든 모델을 검색 가능하게 만들 때 사용할 쿼리 수정.
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

모델에 `Laravel\Scout\Searchable` 트레잇을 추가하면, 단순히 모델 인스턴스를 `save`하거나 `create`하면 자동으로 검색 인덱스에 추가됩니다. [큐를 사용하도록](#queueing) 구성한 경우 이 작업은 백그라운드에서 처리됩니다:

    use App\Models\Order;

    $order = new Order;

    // ...

    $order->save();

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리를 통해 모델 집합을 검색 인덱스에 추가하려면, `searchable` 메서드를 쿼리에 체이닝하면 됩니다. `searchable` 메서드는 쿼리 결과를 [청크로 분할](/docs/{{version}}/eloquent#chunking-results)하여 검색 인덱스에 추가합니다. 큐가 활성화된 경우 각 청크는 큐 워커에서 백그라운드로 임포트됩니다:

    use App\Models\Order;

    Order::where('price', '>', 100)->searchable();

Eloquent 리레이션 인스턴스에도 `searchable`을 호출할 수 있습니다:

    $user->orders()->searchable();

이미 메모리에 Eloquent 모델 집합이 있다면, 컬렉션 인스턴스에서 바로 `searchable`을 호출해 각 모델 인스턴스를 인덱스에 추가할 수 있습니다:

    $orders->searchable();

> {tip} `searchable` 메서드는 "업서트(upsert)" 연산으로 볼 수 있습니다. 즉, 인덱스에 기존 모델 레코드가 있으면 갱신되고, 없으면 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 모델 인스턴스의 속성을 변경한 뒤 `save`만 해주면 됩니다. Scout가 변경사항을 자동으로 검색 인덱스에 반영합니다:

    use App\Models\Order;

    $order = Order::find(1);

    // 주문 정보 업데이트...

    $order->save();

Eloquent 쿼리 인스턴스에서 `searchable`을 호출해 모델 집합을 업데이트할 수도 있습니다. 인덱스에 모델이 없으면 새로 생성됩니다:

    Order::where('price', '>', 100)->searchable();

관계에 속한 모든 모델의 검색 인덱스 레코드를 업데이트하려면, 관계 인스턴스에서 `searchable`을 호출하면 됩니다:

    $user->orders()->searchable();

이미 메모리에 Eloquent 모델 집합이 있다면, 컬렉션에서 `searchable`을 호출해 인덱스를 업데이트할 수도 있습니다:

    $orders->searchable();

<a name="removing-records"></a>
### 레코드 삭제

검색 인덱스에서 레코드를 제거하려면, 데이터베이스에서 모델을 간단히 `delete` 하면 됩니다. [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 모델에도 동일하게 적용됩니다:

    use App\Models\Order;

    $order = Order::find(1);

    $order->delete();

레코드를 삭제하기 전 모델을 조회하고 싶지 않다면, Eloquent 쿼리 인스턴스의 `unsearchable` 메서드를 사용할 수 있습니다:

    Order::where('price', '>', 100)->unsearchable();

리레이션 인스턴스에 포함된 모든 모델의 검색 인덱스 레코드를 제거하려면 `unsearchable`을 호출하세요:

    $user->orders()->unsearchable();

이미 메모리에 모델 컬렉션이 있다면, 해당 컬렉션에서 직접 `unsearchable`을 호출해 인덱스에서 제거할 수 있습니다:

    $orders->unsearchable();

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

때때로, 일련의 Eloquent 연산을 수행할 때 모델 데이터를 인덱스와 동기화하지 않아야 할 수도 있습니다. 이럴 땐 `withoutSyncingToSearch` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 클로저를 받아 즉시 실행하며, 그 안에서 발생한 모델 작업은 인덱스에 반영되지 않습니다:

    use App\Models\Order;

    Order::withoutSyncingToSearch(function () {
        // 모델 작업 수행...
    });

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

특정 조건하에서만 모델을 검색 가능하게 만들고 싶을 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "임시 저장(draft)" 또는 "게시됨(published)" 상태일 수 있을 때, "게시됨" 상태만 검색 가능하게 만들고 싶다면, 모델에 `shouldBeSearchable` 메서드를 정의하세요:

    /**
     * 모델이 검색 가능해야 하는지 여부 결정.
     *
     * @return bool
     */
    public function shouldBeSearchable()
    {
        return $this->isPublished();
    }

`shouldBeSearchable` 메서드는 `save`, `create` 메서드, 쿼리, 관계를 통한 모델 조작에만 적용됩니다. `searchable` 메서드로 직접 모델이나 컬렉션을 검색 가능하게 만들면, 이 메서드의 결과를 무시하고 인덱싱합니다.

<a name="searching"></a>
## 검색

모델에서 `search` 메서드를 사용해 검색을 시작할 수 있습니다. `search` 메서드는 검색할 문자열을 인자로 받고, 이어서 `get` 메서드를 체이닝하여 해당 검색 쿼리에 일치하는 Eloquent 모델을 조회하게 됩니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->get();

Scout 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트나 컨트롤러에서 결과를 직접 반환하면 JSON으로 자동 변환됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/search', function (Request $request) {
        return Order::search($request->search)->get();
    });

Eloquent 모델로 변환되기 전 원시 검색 결과를 얻고 싶다면, `raw` 메서드를 사용하세요:

    $orders = Order::search('Star Trek')->raw();

<a name="custom-indexes"></a>
#### 커스텀 인덱스

검색 쿼리는 보통 모델의 [`searchableAs`](#configuring-model-indexes) 메서드로 지정한 인덱스에서 수행됩니다. 하지만 `within` 메서드를 사용해 검색할 인덱스를 임의로 지정할 수 있습니다:

    $orders = Order::search('Star Trek')
        ->within('tv_shows_popularity_desc')
        ->get();

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있습니다. 현재 이 절은 기본적인 숫자 동등 비교만 지원하며, 주로 소유자 ID로 쿼리 범위를 제한하는 데 유용합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->where('user_id', 1)->get();

`whereIn` 메서드를 사용하면, 특정 값 집합에 결과를 한정할 수 있습니다:

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['paid', 'open']
    )->get();

검색 인덱스는 관계형 데이터베이스가 아니므로, 보다 복잡한 "where" 절은 현재 지원되지 않습니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 직접 조회하는 것 외에도, `paginate` 메서드를 사용해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [일반적인 Eloquent 쿼리에서 페이지네이션](/docs/{{version}}/pagination)할 때처럼 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->paginate();

페이지당 항목 수를 지정하려면, `paginate` 메서드의 첫 번째 인자로 개수를 전달하세요:

    $orders = Order::search('Star Trek')->paginate(15);

결과를 조회한 후, [Blade](/docs/{{version}}/blade)를 사용해 결과와 페이지 링크를 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

또는 페이지네이션 결과를 JSON으로 반환하고자 한다면, 라우트나 컨트롤러에서 페이지네이터 인스턴스를 직접 반환하면 됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        return Order::search($request->input('query'))->paginate(15);
    });

<a name="soft-deleting"></a>
### 소프트 삭제

인덱싱된 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원하고, 소프트 삭제된 모델까지 검색하려면, `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 설정하세요:

    'soft_delete' => true,

이 옵션이 `true`일 때 Scout는 소프트 삭제된 모델을 인덱스에서 실제로 제거하지 않고, 인덱스된 레코드에 숨겨진 `__soft_deleted` 속성을 추가합니다. 이후 검색 시 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드까지 조회할 수 있습니다:

    use App\Models\Order;

    // 삭제된 레코드를 포함해 결과 조회...
    $orders = Order::search('Star Trek')->withTrashed()->get();

    // 삭제된 레코드만 조회...
    $orders = Order::search('Star Trek')->onlyTrashed()->get();

> {tip} 소프트 삭제된 모델을 `forceDelete`로 영구 삭제하면 Scout가 인덱스에서도 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

엔진의 검색 동작을 고급으로 커스터마이즈해야 하는 경우, `search` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백을 통해 지리 정보 데이터를 검색 옵션에 추가할 수 있습니다:

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

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

기본 제공 Scout 검색 엔진이 요구사항에 맞지 않는 경우, 자신만의 커스텀 엔진을 만들어 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 확장해야 하며, 해당 클래스에는 반드시 구현해야 할 8개의 메서드가 있습니다:

    use Laravel\Scout\Builder;

    abstract public function update($models);
    abstract public function delete($models);
    abstract public function search(Builder $builder);
    abstract public function paginate(Builder $builder, $perPage, $page);
    abstract public function mapIds($results);
    abstract public function map(Builder $builder, $results, $model);
    abstract public function getTotalCount($results);
    abstract public function flush($model);

각 메서드의 구현은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스에서 참고할 수 있으며, 자신만의 엔진을 구현할 때 좋은 출발점이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 작성했다면, Scout 엔진 매니저의 `extend` 메서드를 활용해 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 가져올 수 있으며, `App\Providers\AppServiceProvider`의 `boot` 메서드(또는 사용하는 서비스 프로바이더)에서 호출해야 합니다:

    use App\ScoutExtensions\MySqlSearchEngine;
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

엔진을 등록한 후에는, `config/scout.php`의 기본 Scout `driver`로 지정할 수 있습니다:

    'driver' => 'mysql',

<a name="builder-macros"></a>
## 빌더 매크로

커스텀 Scout 검색 빌더 메서드를 정의하려면, `Laravel\Scout\Builder` 클래스의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 "매크로"는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 정의합니다:

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

`macro` 함수는 첫 번째 인자로 매크로 이름, 두 번째 인자로 클로저를 받습니다. 매크로명으로 `Laravel\Scout\Builder` 구현체에서 호출하면, 해당 클로저가 실행됩니다:

    use App\Models\Order;

    Order::search('Star Trek')->count();
