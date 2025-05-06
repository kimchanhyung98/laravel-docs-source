# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐 사용](#queueing)
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
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 인덱싱](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전문 검색을 추가할 수 있는 간단한 드라이버 기반 솔루션을 제공합니다. 모델 옵저버를 사용하여 Scout는 Eloquent 레코드의 변경 사항을 즉시 검색 인덱스와 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL (`database`) 드라이버를 기본 제공하고 있습니다. 또한, Scout에는 별도의 외부 의존성이나 써드파티 서비스 없이 로컬 개발용으로 사용할 수 있는 "collection" 드라이버도 포함되어 있습니다. 커스텀 드라이버 작성도 간단하여, Scout를 확장해 직접 필요한 검색 구현체를 추가할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 통해 Scout를 설치합니다:

```shell
composer require laravel/scout
```

설치가 완료되면, `vendor:publish` Artisan 명령어로 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령어는 `config` 디렉터리에 `scout.php` 설정 파일을 생성합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색이 필요한 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여 모델과 검색 드라이버를 항상 동기화합니다:

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
### 큐 사용

Scout를 사용하기 위해 꼭 필요한 것은 아니지만, 개발 시 [큐 드라이버](/docs/{{version}}/queues)를 설정하는 것이 강력히 권장됩니다. 큐 워커를 사용하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐로 처리할 수 있어, 웹 인터페이스의 응답 속도를 크게 향상시킵니다.

큐 드라이버를 설정한 뒤에는 `config/scout.php`의 `queue` 옵션을 `true`로 지정하세요:

```php
'queue' => true,
```

`queue` 옵션이 `false`여도 Algolia, Meilisearch와 같이 항상 비동기로 인덱싱하는 Scout 드라이버도 존재한다는 점을 유의하세요. 즉, Laravel 애플리케이션 내에서 인덱싱 작업이 완료되었더라도, 실제 검색 엔진에는 새로운/업데이트된 레코드가 바로 반영되지 않을 수 있습니다.

Scout 작업에서 사용할 큐 커넥션과 큐 이름을 지정하고 싶다면, 아래처럼 `queue` 옵션을 배열로 정의할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

그리고 별도의 큐 커넥션과 이름을 사용할 경우, 아래와 같이 해당 큐를 처리할 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 파일에 Algolia의 `id`와 `secret` 자격 증명을 설정해야 합니다. 이후 Composer로 Algolia PHP SDK를 설치합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. Meilisearch를 로컬에 설치하는 방법을 잘 모르겠다면, [Laravel Sail](/docs/{{version}}/sail#meilisearch)을 활용할 수 있습니다.

Meilisearch 드라이버 사용 시, Composer로 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 다음, `.env` 파일의 환경 변수로 Meilisearch의 드라이버, 호스트, 키 정보를 넣습니다:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

더 자세한 정보는 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용 중인 Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 버전을 설치했는지 반드시 확인하세요. [바이너리 호환성 정보를 참고](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)하세요.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때, 반드시 [Meilisearch 서비스의 신규 주요 변경사항](https://github.com/meilisearch/Meilisearch/releases)을 확인하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈 소스 검색 엔진으로, 키워드 검색, 의미 기반 검색, 위치(geo), 벡터 검색 등을 지원합니다.

직접 [호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면, Composer로 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그 다음 `.env` 파일에서 Typesense의 드라이버, 호스트, API 키를 설정합니다:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/{{version}}/sail)를 사용한다면, `TYPESENSE_HOST` 환경 변수를 도커 컨테이너 이름과 맞춰야 할 수 있습니다. 포트, 경로, 프로토콜을 추가로 지정할 수도 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션에 대한 추가 설정과 스키마 정의는 `config/scout.php`에서 관리할 수 있습니다. 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장 데이터 준비

Typesense 사용 시, 검색이 가능한 모델에는 반드시 기본 키를 문자열로, 생성일자를 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드가 필요합니다:

```php
/**
 * 모델의 인덱싱 가능한 데이터 배열 반환.
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

Typesense용 컬렉션의 스키마는 `config/scout.php`에서 정의해야 합니다. 스키마는 필드별 데이터 타입을 설명합니다. 모든 스키마 옵션은 [Typesense 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

이미 정의된 Typesense 컬렉션의 스키마를 변경해야 한다면, `scout:flush`와 `scout:import` 명령어로 기존 인덱스 데이터를 모두 삭제하고 스키마를 재생성할 수 있습니다. 또는 Typesense API로 기존 데이터를 삭제하지 않고 컬렉션 스키마를 수정할 수도 있습니다.

모델이 소프트 삭제를 지원한다면, 해당 모델의 Typesense 스키마에 `__soft_deleted` 필드를 정의해야 합니다:

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

Typesense에서는 검색을 실행할 때 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 `options` 메서드로 동적으로 지정할 수 있습니다:

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

각 Eloquent 모델은 지정된 검색 "인덱스"와 동기화됩니다. 각 인덱스는 해당 모델의 모든 검색 가능 레코드를 포함합니다. 기본적으로 각 모델은 모델의 일반적인 "테이블명"과 동일한 이름의 인덱스에 저장됩니다. 일반적으로 모델 이름의 복수형이며, 필요에 따라 `searchableAs` 메서드를 재정의해 사용자 지정 인덱스명을 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연결된 인덱스명을 반환.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 데이터 설정

기본적으로, 모델의 전체 `toArray` 데이터가 검색 인덱스에 저장됩니다. 인덱싱할 데이터를 직접 지정하려면 `toSearchableArray` 메서드를 재정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱싱 가능한 데이터 배열 반환.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열을 커스터마이즈...

        return $array;
    }
}
```

Meilisearch 등 일부 검색 엔진은 데이터 타입이 맞을 때만 필터 연산(`>`, `<` 등)을 지원하므로, 숫자 필드는 반드시 올바른 타입으로 변환해서 반환해야 합니다:

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
#### 인덱스 세팅 설정 (Algolia)

가끔 Algolia 인덱스에 추가 설정이 필요할 수 있습니다. Algolia UI로 설정해도 되지만, `config/scout.php`에서 직접 관리하는 방식이 자동화 및 일관성 유지에 유리합니다. 필터 속성, 랭킹, 패싯 등 [지원하는 모든 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

아래처럼 각 인덱스별 세팅을 지정하세요:

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
            // 기타 설정...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

소프트 삭제 모델이 있다면, `index-settings` 배열에 빈 배열로 추가해주기만 하면 Scout가 해당 인덱스에서 소프트 삭제 패싯을 자동 지원합니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 반드시 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 인덱스 설정을 동기화하세요. 배포 자동화 과정에서 이 명령어를 포함하면 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### Meilisearch 필터링 데이터 및 인덱스 설정

Meilisearch는 필터형, 정렬형, 기타 다양한 인덱스 설정을 미리 정의해야 합니다. 필터링 속성엔 Scout의 `where` 메서드에서 필터링할 속성들을, 정렬 속성엔 `orderBy`로 정렬할 속성들을 적으면 됩니다.

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

소프트 삭제 모델이 있다면 역시 빈 배열로 추가해 설정을 활성화할 수 있습니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 아래 명령어로 Meilisearch 인덱스 설정을 동기화하세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

Scout는 기본적으로 모델의 기본 키를 검색 인덱스에서 고유 ID/키로 사용합니다. 이 동작을 커스터마이즈하려면, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 재정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱스에 사용할 값 반환.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용할 키 이름 반환.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

검색 시, Scout는 기본적으로 `scout` 설정 파일에서 지정된 기본 검색 엔진을 사용합니다. 단, 모델별로 검색 엔진을 다르게 지정하고 싶다면, 모델에서 `searchableUsing` 메서드를 오버라이드하세요:

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
     * 인덱싱에 사용할 엔진 반환.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시, 검색 요청을 수행한 인증 사용자를 자동 식별하는 기능도 제공합니다. 이 기능으로 Algolia 대시보드의 검색 분석에 인증 사용자를 연동할 수 있습니다. `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하세요:

```ini
SCOUT_IDENTIFY=true
```

이렇게 하면, 각 검색 요청 시 요청자의 IP 주소 및 인증된 사용자의 기본 식별자가 Algolia에 전달됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL 및 PostgreSQL만 지원합니다.

소규모 또는 중간 규모 DB를 사용하거나 부하가 적을 때는 Scout의 "database" 엔진을 사용하는 편이 간편할 수 있습니다. 기존 데이터베이스에서 "where like" 절 및 전체 텍스트 인덱스를 이용해 결과를 필터링하여 검색 결과를 제공합니다.

사용하려면 `.env`에서 `SCOUT_DRIVER`를 `database`로 지정하거나 설정 파일에서 지정하세요:

```ini
SCOUT_DRIVER=database
```

설정 후 [검색 데이터](#configuring-searchable-data)를 정의하고, [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense와 달리 데이터베이스 엔진에서는 별도의 인덱싱 작업이 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 database 엔진은 [searchable 필드로 지정한](#configuring-searchable-data) 모든 컬럼에 "where like" 쿼리를 실행합니다. 성능 문제 등이 있다면 일부 컬럼은 전체 텍스트, 일부는 prefix(search string이 앞에 올 때만) 검색으로 변경할 수 있습니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱싱 가능한 데이터 배열 반환.
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
> 전체 텍스트 인덱스를 사용하는 컬럼은 [전체 텍스트 인덱스](/docs/{{version}}/migrations#available-index-types)가 생성되어 있어야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서도 Algolia, Meilisearch, Typesense등을 사용할 수 있지만, 간단히 "collection" 엔진도 사용할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 "where" 구문과 Laravel의 컬렉션 필터링 함수를 사용합니다. 별도 인덱싱이 필요 없습니다.

사용 방법은 `.env`에서 `SCOUT_DRIVER`를 `collection`으로 지정하거나 설정 파일에서 지정하세요:

```ini
SCOUT_DRIVER=collection
```

설정 후 [검색 쿼리](#searching)를 실행할 수 있습니다.

#### 데이터베이스 엔진과의 차이점

"database" 엔진과 "collection" 엔진은 결과를 검색할 때 데이터베이스를 직접 참조한다는 점에서 비슷하지만, collection 엔진은 전체 텍스트 인덱스나 `LIKE` 쿼리가 아니라 모든 레코드를 불러온 뒤 Laravel의 `Str::is` 헬퍼로 일치 여부를 판별합니다.

collection 엔진은 SQLite, SQL Server 등 Laravel이 지원하는 모든 관계형 데이터베이스에서 동작하지만, database 엔진보다 효율성이 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 도입한다면 이미 저장된 데이터베이스 레코드를 인덱스로 임포트할 필요가 있습니다. `scout:import` Artisan 명령어로 진행할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

모델의 인덱스에 있는 모든 레코드를 삭제하려면 `flush` 명령어를 사용하세요:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 수정

배치 임포트에 사용되는 모델 쿼리를 수정하려면, 모델에 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 이 메서드는 관계를 미리 로드하거나 추가 조건을 붙이는 데 유용합니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모든 모델 임포트 쿼리 커스터마이즈.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> `makeAllSearchableUsing`는 큐를 사용할 때는 적용되지 않을 수 있습니다. 모델 컬렉션이 큐 작업으로 처리될 경우 관계가 [자동 복원되지 않습니다](/docs/{{version}}/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

`Laravel\Scout\Searchable` 트레이트가 추가된 모델은 `save` 또는 `create` 호출 시 자동으로 검색 인덱스에 추가됩니다. Scout에서 [큐를 사용](#queueing)하도록 설정한 경우, 이 작업은 백그라운드로 처리됩니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가

Eloquent 쿼리에 `searchable` 메서드를 체인하면, 해당 컬렉션 전체를 검색 인덱스에 추가할 수 있습니다. 결과는 [청크 단위로 처리](/docs/{{version}}/eloquent#chunking-results)되며, 큐를 사용할 경우 백그라운드에서 임포트됩니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계에 대해서도 `searchable` 메서드를 사용할 수 있습니다:

```php
$user->orders()->searchable();
```

이미 Eloquent 컬렉션을 가지고 있다면, 컬렉션 인스턴스에 `searchable`을 호출해 각 모델 인스턴스를 인덱스에 추가할 수 있습니다:

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert" 동작(존재하면 업데이트, 없으면 추가)으로 동작합니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능 모델을 업데이트하려면 Eloquent 모델의 속성 값을 변경 후 `save`하면 됩니다. Scout는 자동으로 인덱스도 갱신합니다:

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 업데이트...

$order->save();
```

Eloquent 쿼리 인스턴스에 `searchable`을 호출해 여러 모델을 한 번에 업데이트할 수도 있습니다:

```php
Order::where('price', '>', 100)->searchable();
```

관계의 모든 모델에 대해 업데이트하려면 관계 인스턴스에 `searchable`을 호출하면 됩니다:

```php
$user->orders()->searchable();
```

이미 컬렉션을 가지고 있다면 해당 컬렉션에 `searchable`을 호출해 일괄 업데이트할 수 있습니다:

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 임포트 전 레코드 변형

임포트 전 모델의 컬렉션을 변형해야 할 때, 예를 들어 관계를 eager load해야 할 때 `makeSearchableUsing` 메서드를 정의할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 인덱싱 직전 컬렉션 변형.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제

인덱스에서 레코드를 삭제하려면 모델을 데이터베이스에서 `delete`하면 됩니다. [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 모델도 마찬가지입니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 미리 조회하지 않고 삭제하려면, 쿼리 인스턴스에 `unsearchable`을 사용할 수 있습니다:

```php
Order::where('price', '>', 100)->unsearchable();
```

관계형 모델 전체를 인덱스에서 삭제하려면 관계 인스턴스에 `unsearchable`을 사용하세요:

```php
$user->orders()->unsearchable();
```

이미 보유한 Eloquent 컬렉션에 대해 `unsearchable`을 사용해 일괄 삭제할 수도 있습니다:

```php
$orders->unsearchable();
```

모든 모델 레코드를 인덱스에서 한 번에 삭제하고 싶다면 `removeAllFromSearch` 메서드 사용:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

여러 Eloquent 작업을 인덱싱 없이 처리해야 할 때, `withoutSyncingToSearch` 메서드를 사용하세요. 이 메서드는 클로저로 감싼 모든 작업에 대해 검색 인덱싱을 일시 중지합니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 인덱싱

특정 상황에서만 모델을 검색 인덱싱하고 싶을 때, 예를 들어 `App\Models\Post` 모델이 "draft" 또는 "published" 상태를 가진다면, "published" 상태만 인덱싱하려면 `shouldBeSearchable` 메서드를 정의하세요:

```php
/**
 * 인덱싱 여부 결정.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

이 메서드는 `save`, `create`, 쿼리, 관계 처리 시에만 적용되며, 직접 `searchable`을 호출하면 무시됩니다.

> [!WARNING]
> `shouldBeSearchable`는 Scout의 "database" 엔진에서는 적용되지 않습니다. database 엔진을 사용할 때는 [where절](#where-clauses)로 동작을 대체하세요.

<a name="searching"></a>
## 검색

`search` 메서드를 사용해 모델 검색을 시작할 수 있습니다. 검색어(문자열)를 인자로 받아 해당 모델을 검색하며, 이어서 `get`을 체인하면 Eloquent 모델 컬렉션으로 결과를 받을 수 있습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이기 때문에 라우트나 컨트롤러에서 그대로 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과의 원시값(raw result)을 보고 싶다면 `raw` 메서드를 사용하세요:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

검색은 기본적으로 모델의 [searchableAs](#configuring-model-indexes)로 지정된 인덱스에서 수행되지만, `within` 메서드로 다른 인덱스를 지정할 수 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where절

Scout는 간단한 "where" 절로 검색 쿼리에 추가 조건을 걸 수 있습니다. 이는 기본적으로 숫자(정수) 값의 동등 비교만 지원하며, 주로 소유자 ID로 범위를 제한할 때 사용합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn` 메서드는 주어진 배열 내의 값이 컬럼에 포함되는지 검사합니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 주어진 배열 내의 값이 컬럼에 포함되지 않는지 검사합니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니므로, 이외의 복잡한 "where" 조건은 지원하지 않습니다.

> [!WARNING]
> Meilisearch를 사용하는 경우, 반드시 [필터 속성](#configuring-filterable-data-for-meilisearch)을 먼저 설정해야 "where" 절을 사용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션

일반 Eloquent 쿼리처럼, Scout 검색 결과도 `paginate` 메서드로 페이지네이션할 수 있습니다. 이 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 항목 수는 첫 번째 인자로 지정합니다:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 Blade에서 일반 Eloquent 페이지네이션과 동일한 방식으로 표시하고 링크를 렌더링하면 됩니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

JSON으로 페이지네이션 결과만 반환하고 싶으면, 라우트나 컨트롤러에서 paginator 인스턴스를 바로 반환하면 됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프(global scope)를 인지하지 못하므로, Scout 페이지네이션이 필요한 앱에서는 글로벌 스코프를 사용하지 않거나, Scout 검색 시 직접 조건을 다시 구현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

[소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 모델을 인덱스에 저장하고, 소프트 삭제된 레코드도 검색하려면 `config/scout.php`의 `soft_delete` 옵션을 `true`로 지정하세요:

```php
'soft_delete' => true,
```

이 옵션이 `true`이면, Scout는 소프트 삭제된 모델을 인덱스에서 제거하는 대신 숨겨진 `__soft_deleted` 속성을 레코드에 추가합니다. 그 후 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제 레코드를 검색할 수 있습니다:

```php
use App\Models\Order;

// 트래시 포함
$orders = Order::search('Star Trek')->withTrashed()->get();

// 트래시만 포함
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제 모델을 `forceDelete`로 영구 삭제하면, Scout 인덱스에서도 자동 삭제됩니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

검색 엔진 동작을 고급 설정으로 커스터마이징해야 할 때는, `search` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어, Algolia에 지리 정보(geo-location)를 옵션에 추가하려면 다음과 같이 작성할 수 있습니다:

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
#### Eloquent 결과 쿼리 커스터마이징

Scout가 검색 엔진에서 일치하는 모델 키 목록을 가져온 뒤, Eloquent가 해당 모델을 찾기 위해 쿼리를 다시 실행합니다. 필요하다면 `query` 메서드에 클로저를 넘겨 Eloquent 쿼리를 커스터마이즈할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 검색 엔진에서 키를 찾은 후 동작하므로, 검색 필터링 용도가 아니라 결과 처리에만 사용해야 합니다. 필터링은 반드시 [Scout where 절](#where-clauses)로 구현하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

기본 제공 Scout 검색 엔진으로 원하는 기능이 구현되지 않을 경우, 직접 커스텀 엔진을 작성해 Scout에 등록할 수 있습니다. 엔진은 반드시 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음 8가지 메서드를 구현해야 합니다:

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

이 메서드의 구현 예시로는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 좋습니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 구현했으면, Scout의 엔진 매니저의 `extend` 메서드로 등록할 수 있습니다. 엔진 매니저는 라라벨 서비스 컨테이너에서 resolve할 수 있으며, 보통 `App\Providers\AppServiceProvider` 등의 부트 메서드 내에서 호출합니다:

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

등록 후에는 `config/scout.php`의 `driver` 설정에 커스텀 엔진 이름을 지정하세요:

```php
'driver' => 'mysql',
```
