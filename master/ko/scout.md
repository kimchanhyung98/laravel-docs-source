# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 사전 준비사항](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스/컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 정지](#pausing-indexing)
    - [조건부 인덱싱](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색(full-text search)을 손쉽게 추가할 수 있는 동작 기반(driver based) 솔루션을 제공합니다. 모델 옵저버를 활용하여, Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), MySQL / PostgreSQL(`database`) 드라이버를 기본으로 제공합니다. 또한, Scout에는 외부 의존성이나 타사 서비스가 필요 없는 로컬 개발용 "컬렉션" 드라이버도 포함되어 있습니다. 나아가, 커스텀 드라이버 작성도 단순하여 여러분만의 검색 구현체를 Scout에 확장할 수 있습니다.

<a name="installation"></a>
## 설치

우선 Composer 패키지 매니저를 통해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

Scout를 설치한 후, `vendor:publish` Artisan 명령어로 Scout 설정 파일을 게시하세요. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 생성합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레잇을 추가하세요. 이 트레잇은 모델 옵저버를 등록하여 해당 모델과 검색 드라이버를 자동으로 동기화합니다:

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
### 큐잉

Scout를 반드시 큐와 함께 사용해야 하는 것은 아니지만, 라이브러리 사용 전 [큐 드라이버](/docs/{{version}}/queues) 설정을 강력히 권장합니다. 큐 워커를 실행하면, Scout는 모델 정보를 검색 인덱스에 동기화하는 모든 작업을 큐에 적재하므로, 웹 인터페이스의 응답 속도를 크게 개선할 수 있습니다.

큐 드라이버를 설정했다면, `config/scout.php` 설정 파일에서 `queue` 옵션을 `true`로 설정하세요:

```php
'queue' => true,
```

`queue` 옵션이 `false`이어도, Algolia나 Meilisearch와 같은 일부 Scout 드라이버는 항상 비동기로 인덱싱을 수행한다는 점을 유의하세요. 즉, Laravel 애플리케이션 내에서 인덱스 작업이 완료되어도, 검색 엔진에서 신규 및 변경된 레코드가 즉시 반영되지 않을 수 있습니다.

Scout 작업에서 사용할 연결(connection)과 큐 이름(queue)을 지정하고 싶다면, `queue` 설정을 배열로 정의할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

이렇게 연결 및 큐를 커스터마이징했다면, 해당 큐 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비사항

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는, `config/scout.php` 설정 파일에서 Algolia의 `id`와 `secret` 정보를 지정해야 합니다. 자격 증명 설정 후, Composer로 Algolia PHP SDK를 추가 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠른 오픈소스 검색 엔진입니다. Meilisearch를 로컬에 설치하는 법을 모르겠다면, [Laravel Sail](/docs/{{version}}/sail#meilisearch) 도커 개발 환경의 지원을 활용할 수 있습니다.

Meilisearch 드라이버 사용 시 Composer로 Meilisearch PHP SDK를 설치하세요:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고 애플리케이션 `.env` 파일에 `SCOUT_DRIVER`와 Meilisearch의 `host`, `key` 정보를 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 자세한 사항은 [공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하여, 사용 중인 Meilisearch 바이너리 버전에 맞는 PHP SDK 버전을 반드시 설치해야 합니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 [주요 변경 사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 확인하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈소스 검색 엔진으로서 키워드 검색, 시맨틱 검색, 지오 검색, 벡터 검색을 지원합니다.

[셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) 또는 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그리고 `.env` 파일에 `SCOUT_DRIVER`, Typesense 호스트와 API 키를 지정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/{{version}}/sail)을 사용하는 경우, `TYPESENSE_HOST` 값이 도커 컨테이너명과 일치하는지 확인하세요. 또한 포트, 경로, 프로토콜을 별도로 지정할 수도 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

추가 설정 및 컬렉션 스키마 정의는 `config/scout.php`에서 할 수 있습니다. 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고해 주세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense를 이용할 때는 모델의 기본키를 문자열로, 생성일을 유닉스 타임스탬프로 캐스팅하는 `toSearchableArray` 메서드를 반드시 정의해야 합니다:

```php
/**
 * 모델의 인덱스화 데이터 배열 반환.
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

Typesense 컬렉션 스키마 역시 `config/scout.php`에 정의해야 합니다. 각 필드의 데이터 타입 정보 등 스키마 파라미터는 [공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 수정해야 한다면 `scout:flush` 및 `scout:import` 명령어로 기존 데이터를 삭제 후 재생성하거나, Typesense API로 직접 스키마를 변경할 수 있습니다.

소프트 삭제 모델을 인덱싱할 때는 `config/scout.php`의 컬렉션 스키마에 `__soft_deleted` 필드를 추가해야 합니다:

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

Typesense는 `options` 메서드를 활용하여 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 지정할 수 있습니다:

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

각 Eloquent 모델은 해당 모델의 모든 검색 레코드를 담은 검색 "인덱스"와 동기화됩니다. 각 인덱스는 MySQL 테이블과 유사하다고 이해할 수 있습니다. 기본적으로 각 모델은 테이블 이름(일반적으로 모델명 복수형)의 인덱스에 저장됩니다. 인덱스명을 변경하고 싶다면, 모델에서 `searchableAs` 메서드를 오버라이드하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연관된 인덱스명 반환.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 데이터 설정

기본적으로 모델의 `toArray` 결과 전체가 검색 인덱스에 저장됩니다. 인덱싱되는 데이터를 커스터마이징하고 싶다면, `toSearchableArray` 메서드를 오버라이드하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱스화 데이터 배열 반환.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열 커스터마이징...

        return $array;
    }
}
```

Meilisearch 등의 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 위해 데이터 타입이 정확해야만 합니다. 따라서, 숫자형 데이터를 인덱싱할 때에는 캐스팅도 잊지 마세요:

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
#### 인덱스 설정(Algolia)

경우에 따라 인덱스에 추가 설정(필터 필드, 정렬, 파셋 등)을 적용할 수 있습니다. 이는 Algolia UI로 설정할 수도 있지만, `config/scout.php`에서 직접 관리하면 배포 자동화 및 환경 일관성을 유지할 수 있습니다.

각 모델별 인덱스 설정은 아래와 같이 지정할 수 있습니다:

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
            // 기타 설정 필드...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

소프트 삭제 모델이 인덱싱 대상일 경우, Scout는 해당 인덱스의 파셋 필드를 자동으로 추가합니다. 별다른 파셋 필드가 없어도 아래와 같이 빈 배열로 지정하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 완료 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 인덱스 설정을 반영하세요(배포 파이프라인에 포함하는 것을 권장):

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### Meilisearch - 필터링/정렬 필드 및 인덱스 설정

Meilisearch는 필터/정렬/기타 설정 필드를 미리 정의해야 합니다(자세한 설정 필드는 [공식 문서](https://docs.meilisearch.com/reference/api/settings.html) 참고).

`where`로 필터링할 필드는 filterableAttributes, `orderBy`로 정렬할 필드는 sortableAttributes로 별도 지정해야 합니다. 예시:

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

소프트 삭제 모델은 빈 배열로 지정해도 자동 지원됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 아래 명령어로 설정 값을 Meilisearch에 동기화하세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본키를 인덱스에 저장되는 고유 ID로 사용합니다. 다른 키를 사용하려면 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱스에 사용될 값 반환.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱스에 사용될 키명 반환.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

기본적으로 모든 모델은 `scout` 설정 파일에 정의된 기본 검색 엔진을 사용하지만, `searchableUsing` 메서드를 오버라이드하면 특정 모델만 별도의 검색 엔진을 사용할 수 있습니다:

```php
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
     * 모델에 사용할 엔진 반환.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

[Algolia](https://algolia.com) 드라이버 사용 시, Scout는 인증 사용자와 검색 요청을 연동할 수 있습니다. 이는 Algolia 대시보드에서 검색 분석 시 유용합니다. `.env`에 `SCOUT_IDENTIFY=true`를 지정하면 활성화됩니다:

```ini
SCOUT_IDENTIFY=true
```

이 기능이 활성화되면, 요청자의 IP와 인증 사용자의 primary 키가 Algolia에 함께 전달되어 검색 로그에 남습니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 MySQL과 PostgreSQL만 지원합니다.

소규모 또는 중간 규모 데이터베이스, 가벼운 부하의 앱이라면 Scout의 "database" 엔진을 사용하는 것이 더 편리할 수 있습니다. 이 엔진은 기존 DB에서 "where like" 절과 풀텍스트 인덱스를 활용하여 검색 결과를 필터링합니다.

database 엔진을 사용하려면, `.env` 파일 또는 `scout` 설정 파일에 아래처럼 지정하세요:

```ini
SCOUT_DRIVER=database
```

설정 후, [검색 데이터 설정](#configuring-searchable-data)을 완료하고 [검색 쿼리 실행](#searching)에 바로 들어갈 수 있습니다. Algolia/Meilisearch/Typesense처럼 미리 인덱싱할 필요가 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 모든 검색 가능 컬럼에 대해 "where like" 쿼리가 실행됩니다. 하지만, 일부 컬럼에는 풀텍스트 검색이나 프리픽스 검색만 적용하는 등 성능 최적화를 원한다면 메서드에 PHP 속성을 지정할 수 있습니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱스화 데이터 배열 반환.
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
> 풀텍스트 검색을 위한 인덱스는 해당 컬럼에 반드시 [풀텍스트 인덱스](/docs/{{version}}/migrations#available-index-types)가 있어야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 때 Algolia, Meilisearch, Typesense 등 외부 엔진 없이 "collection" 엔진을 사용하면 편리합니다. 이 엔진은 DB에서 레코드를 가져온 뒤 Laravel의 `Str::is` 헬퍼로 검색어가 포함되는지 검사합니다(별도 인덱싱 불필요).

사용 방법은 아래와 같습니다:

```ini
SCOUT_DRIVER=collection
```

설정 후에는 바로 [검색 쿼리 실행](#searching)이 가능합니다.

#### 데이터베이스 엔진과의 차이점

database 엔진과 collection 엔진은 모두 DB 데이터를 직접 조회합니다. 하지만 collection 엔진은 풀텍스트/LIKE 검색 대신 모든 레코드를 불러와 `Str::is`로 검사합니다. 따라서 모든 관계형 데이터베이스에서 동작하며, 데이터베이스 엔진보다 느릴 수 있습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 도입할 경우, 기존 DB 레코드를 인덱스에 임포트해야 할 수 있습니다. 이를 위해 `scout:import` Artisan 명령어를 사용하세요:

```shell
php artisan scout:import "App\Models\Post"
```

모델의 인덱스화 데이터를 모두 지우려면:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 커스터마이징

배치 임포트 시 불러올 모델 쿼리를 수정하려면 `makeAllSearchableUsing` 메서드를 모델에 정의하세요. 연관 관계를 미리 로드할 때 유용합니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 배치 임포트 시 모델 쿼리 커스터마이즈.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> `makeAllSearchableUsing`은 큐에서 배치 임포트 시에는 적용되지 않습니다. 큐에서 연관 관계는 [복구되지 않습니다](/docs/{{version}}/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

모델에 `Searchable` 트레잇이 추가되어 있다면, 인스턴스를 `save` 또는 `create` 할 때 자동으로 인덱스에 추가됩니다(큐가 설정되었다면 백그라운드 처리):

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리 기반 인덱싱

컬렉션을 쿼리로 선택해 인덱스에 추가하려면 Eloquent 쿼리 뒤에 `searchable`을 체인하세요. 검색 작업은 자동으로 청크로 분할되어 처리됩니다(큐 사용 시 백그라운드로 실행):

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

관계(Relationship) 인스턴스 또는 메모리에 이미 불러온 컬렉션에도 바로 사용할 수 있습니다:

```php
$user->orders()->searchable();
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert"처럼 동작하여, 기존에 인덱스에 있으면 업데이트하고, 없으면 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트

인덱싱된 모델의 프로퍼티를 수정 후 `save` 하면 자동으로 검색 인덱스도 갱신됩니다:

```php
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```

컬렉션 또는 관계에 대해선 쿼리 인스턴스에 `searchable`을 호출합니다:

```php
Order::where('price', '>', 100)->searchable();
$user->orders()->searchable();
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 데이터 가공

인덱싱 전 관계를 eager load 등으로 가공하려면 `makeSearchableUsing`를 정의하세요:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 인덱싱될 모델 컬렉션 가공.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제

모델을 DB에서 삭제하면 인덱스에서도 해당 레코드가 삭제됩니다(소프트 삭제 포함):

```php
use App\Models\Order;

$order = Order::find(1);
$order->delete();
```

모델을 조회하지 않고 바로 삭제할 땐 `unsearchable`을 사용하세요:

```php
Order::where('price', '>', 100)->unsearchable();
$user->orders()->unsearchable();
$orders->unsearchable();
```

아예 모든 레코드를 삭제하려면:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 정지

다량의 DB 작업(트랜잭션, 마이그레이션 등) 중 인덱싱을 일시 중지하고 싶다면, `withoutSyncingToSearch`로 묶어서 실행하세요:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 여러 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델

특정 조건에서만 인덱싱하고 싶다면, 예를 들어 게시글이 "퍼블리시" 상태일 때만 검색 가능하게 하려면 `shouldBeSearchable` 메서드를 추가하세요:

```php
/**
 * 모델이 인덱싱 대상인지 결정.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

이 메서드는 주로 `save`, `create`, 쿼리, 관계 등 Scout 작업 때만 적용됩니다. 컬렉션이나 모델을 직접 `searchable`로 지정하면 이 메서드는 무시됩니다.

> [!WARNING]
> "database" 엔진 사용 시 `shouldBeSearchable`는 적용되지 않습니다. DB 자체에서 always 검색 데이터를 갖고 있으므로, 이 경우에는 [where절](#where-clauses)로 필터링 방식을 구현하세요.

<a name="searching"></a>
## 검색

모델에서 `search` 메서드를 사용하면 간편하게 검색을 시작할 수 있습니다. 이 메서드는 검색어 문자열을 인자로 받고, `get`으로 일치하는 Eloquent 모델을 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Eloquent 모델 컬렉션이 반환되므로, 직접 라우트/컨트롤러 응답에서 반환하면 자동으로 JSON 변환도 지원됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

엑츄얼 검색 엔진의 원시 결과를 보고 싶다면 `raw` 메서드를 사용하세요:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

기본적으로 모델의 [`searchableAs`](#configuring-model-indexes) 인덱스에서 검색하지만, `within` 메서드로 특정 인덱스를 지정할 수 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where절

Scout는 간단한 "where" 절을 지원합니다. 현재로선 기본 연산(숫자 동일성 검사 등)만 적용되므로, 예를 들어 소유자 ID로 스코프를 제한할 때 쓸 수 있습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn`, `whereNotIn` 메서드는 배열 내/외 포함여부를 검사합니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();

$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

더 복잡한 where절(조인 등)은 지원하지 않습니다.

> [!WARNING]
> Meilisearch 사용 시, [필터 속성](#configuring-filterable-data-for-meilisearch)이 미리 정의되어 있어야 where절이 동작합니다.

<a name="pagination"></a>
### 페이지네이션

`paginate` 메서드를 사용하면 검색 결과를 페이지네이션 할 수 있습니다. 결과는 일반 Eloquent 페이지네이터(`Illuminate\Pagination\LengthAwarePaginator`)와 동일하게 반환됩니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
$orders = Order::search('Star Trek')->paginate(15);
```

Blade에서 페이지네이션 결과 및 링크를 표시하려면:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

API에서 JSON으로 바로 반환하려면:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색엔진은 전역 스코프(global scope)를 인지하지 못하므로, 전역 스코프에 의존하는 페이지네이션 대신 쿼리시 스코프의 조건을 직접 적용하세요.

<a name="soft-deleting"></a>
### 소프트 삭제

인덱싱 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 대상이고, 소프트 삭제된 모델도 검색하고 싶다면 `config/scout.php`에서 `soft_delete` 옵션을 `true`로 설정하세요:

```php
'soft_delete' => true,
```

이 옵션을 켜면, 삭제 시 검색 인덱스에서 레코드를 실제 삭제하는 대신, 숨겨진 `__soft_deleted` 속성에 상태값을 넣어둡니다. 검색 시에는 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제 레코드를 조회할 수 있습니다:

```php
use App\Models\Order;

// 소프트 삭제 포함하여 조회
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제만 조회
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> `forceDelete`로 영구 삭제하면, 인덱스에서도 완전히 제거됩니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

검색 엔진의 동작을 직접 변경하고 싶다면, `search` 메서드의 두 번째 인자로 콜백(클로저)을 넘겨 직접 옵션을 조작할 수 있습니다. 예를 들어, geo-location 필터를 추가할 수 있습니다:

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
#### Eloquent 결과 쿼리 커스텀

Scout가 검색 엔진에서 일치하는 기본키를 조회한 다음, Eloquent로 모델을 실제로 select 할 때 수행되는 쿼리를 `query` 메서드로 커스터마이징할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 쿼리는 이미 검색 결과가 정해진 후에만 동작하므로, 모델 필터링에 사용하지 마시고, where 절 등은 [Scout where절](#where-clauses)을 사용해야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

내부 내장 엔진으로 요구사항을 만족할 수 없을 때는, 직접 커스텀 엔진을 만들어 등록할 수 있습니다. 엔진 클래스는 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속하여 8개 메서드를 구현해야 합니다:

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

자세한 구현은 `Laravel\Scout\Engines\AlgoliaEngine`를 참고하면 유용합니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 작성한 후에는, Scout의 엔진 매니저의 `extend` 메서드로 등록하세요. ServiceProvider의 `boot` 메서드에서 호출하면 됩니다:

```php
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

등록이 완료되면, `config/scout.php`에서 기본 드라이버로 지정하세요:

```php
'driver' => 'mysql',
```
