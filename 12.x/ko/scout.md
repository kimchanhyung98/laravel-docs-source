# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐 사용하기](#queueing)
- [드라이버 필수 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능한 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별하기](#identifying-users)
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
- [검색하기](#searching)
    - [Where 조건절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 대한 전문 검색(Full-text search)을 간편하게 추가할 수 있는 드라이버 기반 솔루션을 제공합니다. Scout는 모델 옵저버를 활용하여 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL (`database`) 드라이버를 기본 제공하고 있습니다. 또한, 외부 의존성이나 서드파티 서비스가 필요 없는 로컬 개발 환경용 "collection" 드라이버도 포함되어 있습니다. 이외에도, 여러분만의 커스텀 드라이버를 쉽게 만들어 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 Scout를 설치합니다.

```shell
composer require laravel/scout
```

Scout 설치 후에는 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 발행해야 합니다. 이 명령어를 실행하면 `scout.php` 설정 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 대상으로 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 모델 옵저버를 등록하여, 검색 드라이버와 모델 동기화를 자동으로 처리해줍니다.

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
### 큐 사용하기

`database` 또는 `collection` 엔진이 아닌 다른 엔진(예: Algolia, Meilisearch, Typesense 등)을 사용할 때는 [큐 드라이버](/docs/12.x/queues) 설정을 적극 권장합니다. 큐 워커를 실행하면, Scout가 모델 정보를 검색 인덱스에 동기화하는 모든 작업을 큐에 처리할 수 있어 애플리케이션 웹 인터페이스의 응답 속도가 크게 향상됩니다.

큐 드라이버를 설정한 후, `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 변경하세요.

```php
'queue' => true,
```

`queue` 옵션이 `false`로 되어 있어도, Algolia와 Meilisearch같은 일부 Scout 드라이버는 항상 비동기적으로 레코드를 인덱싱합니다. 즉, Laravel 애플리케이션에서 인덱싱 작업이 완료되어도, 검색 엔진에서 새로운 또는 업데이트된 레코드가 즉시 반영되지 않을 수 있습니다.

Scout 작업이 사용하는 연결 및 큐를 지정하려면, `queue` 설정 옵션을 배열 형태로 정의할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

이렇게 연결과 큐를 커스터마이징 했다면, 해당 연결과 큐에서 작업을 처리할 수 있도록 큐 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 필수 조건

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 파일에서 Algolia `id` 및 `secret` 자격 증명을 설정해야 합니다. 자격 증명을 준비한 뒤, Composer 패키지 관리자를 통해 Algolia PHP SDK도 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬 환경에 Meilisearch를 설치하는 방법을 잘 모를 경우, [Laravel Sail](/docs/12.x/sail#meilisearch) 공식 지원 Docker 개발 환경을 활용할 수 있습니다.

Meilisearch 드라이버를 사용할 때는 Composer로 Meilisearch PHP SDK를 설치하세요.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

이후, 애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 함께 Meilisearch `host`, `key` 자격증명을 설정합니다.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 더 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 설치된 Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 패키지 버전을 설치해야 하니, [Meilisearch 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고해주시기 바랍니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 경우, Meilisearch 서비스 자체의 [추가적인 변경 사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 확인하시기 바랍니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠르고 오픈 소스인 검색 엔진으로, 키워드 검색, 시맨틱(의미 기반) 검색, 위치 기반(geo) 검색, 벡터 검색을 지원합니다.

[셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)으로 직접 Typesense를 운영하거나, [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치하세요.

```shell
composer require typesense/typesense-php
```

그리고 애플리케이션의 .env 파일에 `SCOUT_DRIVER`와 Typesense `host`, API 키 자격증명을 설정합니다.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, `TYPESENSE_HOST` 환경 변수를 Docker 컨테이너 이름에 맞게 조정해야 할 수도 있습니다. 설치된 포트, 경로(path), 프로토콜(protocol)도 추가로 지정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정 및 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 지정할 수 있습니다. 더 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 데이터를 저장하기 위한 준비

Typesense를 사용할 때는, 검색 가능한 모델에서 기본키를 문자열로 캐스팅하고 생성일(created_at)을 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드를 정의해야 합니다.

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

Typesense 컬렉션 스키마는 애플리케이션의 `config/scout.php` 파일에서 정의해야 합니다. 컬렉션 스키마는 Typesense로 검색 가능한 각 필드의 데이터 타입을 설명합니다. 사용 가능한 모든 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

이미 정의된 후 컬렉션의 스키마를 변경해야 한다면, `scout:flush` 및 `scout:import` 명령어로 기존 인덱스 데이터를 모두 삭제하고 스키마를 새로 만들 수 있습니다. 인덱싱된 데이터를 삭제하지 않고 컬렉션의 스키마만 수정하려면 Typesense의 API를 사용하세요.

검색 가능한 모델이 소프트 삭제 기능을 사용하는 경우, 모델에 해당하는 Typesense 스키마에서 `__soft_deleted` 필드를 정의해야 합니다.

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

Typesense는 검색 작업을 수행할 때 `options` 메서드를 통해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 수정할 수 있습니다.

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

각 Eloquent 모델은 검색 "인덱스"와 동기화되어, 해당 인덱스에 모든 검색 가능한 레코드가 저장됩니다. 쉽게 말해, 각 인덱스는 MySQL의 테이블과 유사합니다. 기본적으로 각 모델은 일반적으로 "테이블" 이름과 같은 이름의 인덱스에 저장됩니다. 보통은 모델명 복수형입니다. 하지만, 모델의 `searchableAs` 메서드를 오버라이드하여 인덱스 이름을 자유롭게 지정할 수 있습니다.

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
### 검색 가능한 데이터 설정

기본적으로 모델의 `toArray` 데이터 전체가 인덱스에 저장됩니다. 인덱스에 동기화되는 데이터를 조정하려면 모델의 `toSearchableArray` 메서드를 오버라이드하세요.

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

        // 여기에 데이터를 커스터마이징하세요...

        return $array;
    }
}
```

Meilisearch와 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 올바른 타입의 데이터에만 적용할 수 있습니다. 이 엔진들에서 검색 데이터를 커스터마이징할 때는 숫자 값을 반드시 적절한 타입으로 캐스팅해야 합니다.

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
#### 인덱스 설정 커스터마이징 (Algolia)

경우에 따라 Algolia 인덱스에 부가적인 설정을 하고 싶을 수 있습니다. 이 설정을 Algolia UI에서 할 수도 있지만, 애플리케이션의 `config/scout.php` 설정 파일에서 직접 관리하면 자동화된 배포 파이프라인으로 환경마다 일관성을 유지하면서 수작업을 줄일 수 있습니다. 필터링 속성, 랭킹, 분류(faceting), [지원되는 기타 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings) 등 다양한 설정이 가능합니다.

먼저 각 인덱스에 대한 설정을 `config/scout.php` 파일에서 지정하세요.

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
            // 기타 설정 ...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

소프트 삭제를 사용하는 모델이 해당 `index-settings` 배열에 포함될 경우, Scout는 자동으로 해당 인덱스에 소프트 삭제 모델의 분류(faceting) 지원을 추가합니다. 별도로 정의할 분류 속성이 없다면, 빈 배열로도 가능합니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 마쳤으면, 반드시 `scout:sync-index-settings` Artisan 명령어를 실행해야 합니다. 이 명령어는 Algolia에 인덱스 설정을 적용합니다. 자동화 배포에 이 명령어를 추가하는 것도 좋은 방법입니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정(Meilisearch)

Meilisearch는 다른 Scout 드라이버와 달리 필터링 속성, 정렬 속성([지원되는 기타 설정](https://docs.meilisearch.com/reference/api/settings.html) 포함) 등 인덱스 검색 설정을 사전에 정의해야 합니다.

필터링 속성은 Scout의 `where` 메서드를 사용할 때 필터링할 속성이고, 정렬 속성은 `orderBy` 메서드를 사용할 때 정렬할 속성입니다. 인덱스 설정은 `scout` 설정 파일의 `meilisearch` 항목 중 `index-settings` 부분을 수정하여 지정합니다.

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
            // 기타 설정 ...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

소프트 삭제를 사용하는 모델이 `index-settings` 배열에 포함된다면, Scout는 자동으로 해당 인덱스에서 소프트 삭제 모델 필터링을 지원합니다. 별도로 정렬 또는 필터링 속성을 정의할 필요가 없다면 빈 배열로도 가능합니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 완료한 뒤에는 `scout:sync-index-settings` Artisan 명령어를 반드시 실행해야 하며, 이 명령어는 Meilisearch에 인덱스 설정을 동기화합니다. 자동 배포 과정에 이 명령어를 포함시키는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본키(primary key)를 검색 인덱스상에서 유니크한 ID/키로 사용합니다. 이를 커스터마이징하려면, `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드할 수 있습니다.

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
### 모델별 검색 엔진 설정

Scout는 기본적으로 애플리케이션 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 그러나, 특정 모델에 대해 사용할 검색 엔진을 `searchableUsing` 메서드를 오버라이드하여 변경할 수 있습니다.

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
### 사용자 식별하기

Scout는 [Algolia](https://algolia.com) 사용 시 자동으로 사용자를 식별할 수도 있습니다. 인증된 사용자를 검색 작업과 연동하면, Algolia 대시보드에서 검색 분석(analytics)에 도움이 될 수 있습니다. 이를 위해 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하세요.

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면 요청자의 IP주소와 인증된 사용자의 기본 식별자가 Algolia로 전달되어, 해당 사용자가 보낸 모든 검색 요청과 데이터를 연계할 수 있습니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL, PostgreSQL만 지원합니다.

`database` 엔진은 Laravel Scout를 가장 간편하게 시작할 수 있는 방법이며, 기존 데이터베이스에서 MySQL / PostgreSQL 전문(full-text) 인덱스와 "where like" 조건을 활용해 쿼리 결과를 필터링합니다.

데이터베이스 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수 값을 `database`로 지정하거나, `scout` 설정 파일에서 직접 드라이버를 `database`로 설정하면 됩니다.

```ini
SCOUT_DRIVER=database
```

이렇게 지정한 후에는 [검색 가능한 데이터 설정](#configuring-searchable-data)을 참고하여 설정을 마치고, [검색 쿼리 실행](#searching)을 자유롭게 사용할 수 있습니다. Algolia, Meilisearch, Typesense의 인덱싱과 같은 별도의 인덱싱 작업이 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [검색 가능한 데이터로 지정한](#configuring-searchable-data) 모든 모델 속성에 대해 "where like" 쿼리를 실행합니다. 하지만, 상황에 따라 이 전략이 성능 저하를 일으킬 수 있습니다. 따라서 일부 컬럼만 full text 검색 또는 접두어(prefix) 검색("example%") 등으로 구체화할 수 있습니다.

이 설정은 모델의 `toSearchableArray` 메서드에 PHP 어트리뷰트를 추가하여 지정할 수 있습니다. 별도 전략을 지정하지 않은 필드는 기본적으로 "where like" 전략이 적용됩니다.

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
> full text 쿼리 전략을 지정하기 전에, 해당 컬럼이 [full text 인덱스](/docs/12.x/migrations#available-index-types)로 설정되어 있는지 꼭 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서 Algolia, Meilisearch, Typesense와 같은 검색 엔진을 쓰는 대신, 더 빠르게 시작하고 싶다면 "collection" 엔진을 선택할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 검색 쿼리 결과를 불러와 "where"문 및 컬렉션 필터링을 통해 검색 결과를 결정합니다. 이 엔진은 검색 가능한 모델의 인덱싱을 수행할 필요가 없습니다. 즉, 단순히 로컬 데이터베이스에서 레코드를 가져옵니다.

컬렉션 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수 값을 `collection`으로 지정하거나, `scout` 설정 파일에서 `collection` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=collection
```

설정이 끝났으면 [검색 쿼리 실행](#searching)을 바로 사용할 수 있습니다. 별도 인덱싱 작업이 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이점

언뜻 보기엔 "database"와 "collection" 엔진이 매우 비슷하지만, 컬렉션 엔진은 full-text 인덱스나 `LIKE` 쿼리 없이, 모든 가능한 레코드를 불러와서 Laravel의 `Str::is` 헬퍼를 사용해 검색어가 모델 속성 값에 존재하는지 판단합니다.

컬렉션 엔진은 Laravel에서 지원하는 모든 관계형 데이터베이스(예: SQLite, SQL Server 포함)에서 사용할 수 있어 이식성이 높지만, Scout의 데이터베이스 엔진보다 효율이 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 일괄 가져오기

기존 프로젝트에 Scout를 설치한 경우, 이미 존재하는 데이터베이스 레코드를 검색 인덱스에 가져와야 할 수 있습니다. 이럴 때는 `scout:import` Artisan 명령어를 사용하여 모든 기존 레코드를 검색 인덱스에 불러올 수 있습니다.

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` 명령어는 [큐 작업](/docs/12.x/queues)을 통해 일괄적으로 레코드를 가져옵니다.

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` 명령어는 모델의 모든 레코드를 검색 인덱스에서 제거합니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정

배치로 레코드를 인덱스에 가져올 때 조회 쿼리를 수정하고 싶다면, 모델에서 `makeAllSearchableUsing` 메서드를 정의하세요. 예를 들어, 가져오기 전에 연관관계를 eager 로딩하도록 설정할 수 있습니다.

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
> `makeAllSearchableUsing` 메서드는 큐를 사용해 모델을 배치 가져오는 경우에는 적용되지 않을 수 있습니다. 큐 작업에서 모델 컬렉션을 처리할 때는 [연관관계가 복원되지 않습니다](/docs/12.x/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

모델에 `Laravel\Scout\Searchable` 트레이트를 더한 후에는, 단순히 모델 인스턴스를 `save` 또는 `create`하면 자동으로 검색 인덱스에 추가됩니다. Scout가 [큐를 사용하도록 설정](#queueing)되어 있다면, 이 작업은 큐 워커에 의해 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리를 이용해 여러 모델을 검색 인덱스에 추가하려면, Eloquent 쿼리에 `searchable` 메서드를 체인할 수 있습니다. 이 메서드는 쿼리 결과를 [청크로 나누어](/docs/12.x/eloquent#chunking-results) 검색 인덱스에 추가합니다. Scout가 큐를 사용하도록 설정한 경우 모든 청크가 큐 워커에서 백그라운드로 처리됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 연관관계 인스턴스에도 `searchable` 메서드를 사용할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션을 메모리에 가지고 있다면, 그 컬렉션 인스턴스에서도 `searchable` 메서드를 호출할 수 있습니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert" 작업입니다. 즉, 인덱스에 모델 레코드가 이미 존재하면 업데이트되고, 없는 경우 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 해당 모델의 속성을 수정한 뒤 `save` 메서드로 저장하세요. Scout가 변경사항을 검색 인덱스에 자동으로 적용합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 수정...

$order->save();
```

Eloquent 쿼리 인스턴스에서 `searchable` 메서드를 호출해 여러 모델을 한 번에 업데이트할 수도 있습니다. 인덱스에 모델이 없으면 자동으로 생성됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

관계에 포함된 모든 모델의 검색 인덱스 기록을 업데이트하려면, 연관관계 인스턴스에서 `searchable` 메서드를 호출할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션을 가지고 있다면 그 컬렉션에서 `searchable`을 호출해 인덱스를 업데이트할 수도 있습니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 데이터 수정

인덱싱 전에 모델 컬렉션을 준비해야 할 때가 있습니다. 예를 들어, 연관관계를 eager 로딩해서 해당 데이터를 검색 인덱스에 추가하고 싶을 때가 그렇습니다. 이럴 때는 해당 모델에서 `makeSearchableUsing` 메서드를 정의하세요.

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

검색 인덱스에서 레코드를 제거하려면, 데이터베이스에서 해당 모델을 단순히 `delete`하면 됩니다. 소프트 삭제 기능을 사용하더라도 마찬가지입니다.

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 별도로 조회하지 않고 곧바로 제거할 경우, Eloquent 쿼리에서 `unsearchable` 메서드를 사용할 수 있습니다.

```php
Order::where('price', '>', 100)->unsearchable();
```

연관관계에 속한 모든 모델의 검색 인덱스 레코드를 제거하려면, 연관관계 인스턴스에서 `unsearchable`을 호출하세요.

```php
$user->orders()->unsearchable();
```

모델 컬렉션이 이미 있다면, 컬렉션 인스턴스에서 `unsearchable` 메서드를 호출하면 해당 인덱스에서 제거됩니다.

```php
$orders->unsearchable();
```

모든 모델 레코드를 해당 인덱스에서 제거하려면, `removeAllFromSearch` 메서드를 사용하세요.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

여러 모델 작업을 인덱스와 동기화하지 않고 한꺼번에 처리하고 싶을 때는 `withoutSyncingToSearch` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 클로저를 인수로 받아 바로 실행하며, 클로저 내부의 모든 모델 작업은 인덱스와 동기화되지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 관련 작업 ...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

특정 조건에서만 모델을 검색 가능하게 만들고 싶을 때가 있습니다. 예를 들어, `App\Models\Post`가 "draft"(초안) 또는 "published"(발행) 상태일 수 있고, 오직 "published" 상태만 검색 대상이 되어야 한다면 모델에 `shouldBeSearchable` 메서드를 정의하세요.

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`와 `create` 메서드, 쿼리, 연관관계를 통한 모델 조작에만 적용됩니다. `searchable` 메서드를 직접 사용하면 이 메서드의 반환값과 상관없이 강제로 인덱스에 추가됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에는 적용되지 않습니다. database 엔진에서는 모든 searchable 데이터가 항상 DB에 저장됩니다. 이 엔진에서도 비슷한 기능이 필요하다면 [where 조건절](#where-clauses)를 사용하세요.

<a name="searching"></a>
## 검색하기

모델에서 `search` 메서드를 사용해 검색을 시작할 수 있습니다. 이 메서드는 한 개의 문자열을 받아 해당 검색어로 모델을 검색합니다. 이어서 `get` 메서드를 체인해 해당 검색 쿼리와 일치하는 Eloquent 모델을 가져올 수 있습니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션으로 반환되므로, 결과를 라우트나 컨트롤러에서 바로 반환해도 자동으로 JSON으로 변환됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Eloquent 모델로 변환되기 전의 원시(raw) 검색 결과를 받고 싶다면, `raw` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

일반적으로 검색 쿼리는 모델의 [searchableAs](#configuring-model-indexes) 메서드에서 지정한 인덱스에 대해 수행됩니다. 하지만, `within` 메서드를 사용해 다른 인덱스를 지정하여 검색할 수도 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 조건절

Scout에서는 간단한 "where" 조건을 검색 쿼리에 추가할 수 있습니다. 현재는 기본적인 숫자값 동일성 비교만 지원하며, 주로 소유자 ID 등으로 검색 범위를 제한할 때 유용합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한, `whereIn` 메서드를 사용해 컬럼 값이 주어진 배열 내에 포함되어 있는지 확인할 수도 있습니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 컬럼 값이 주어진 배열 내에 포함되어 있지 않은지 확인합니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니기 때문에, 보다 복잡한 "where" 조건은 현재 지원되지 않습니다.

> [!WARNING]
> 애플리케이션에서 Meilisearch를 사용하는 경우, 먼저 [필터링 속성 설정](#configuring-filterable-data-for-meilisearch)을 완료해야 "where" 조건절을 사용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션

결과를 컬렉션으로 가져오는 것 외에, `paginate` 메서드를 사용해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [전통적인 Eloquent 쿼리](/docs/12.x/pagination)와 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 가져올 모델 개수는 `paginate` 메서드의 첫 번째 인수로 지정할 수 있습니다.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

검색 결과를 [Blade](/docs/12.x/blade)에서 일반적인 페이지네이션 쿼리처럼 표시하고 링크도 렌더링할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

결과를 JSON으로 반환하려면 라우트 혹은 컨트롤러에서 페이지네이터 인스턴스를 그대로 리턴하면 됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프(global scope) 정의에 대해 알지 못하므로, Scout 페이지네이션을 사용할 땐 글로벌 스코프를 활용하지 않거나, Scout에서 검색할 때 해당 제약을 직접 구현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

[소프트 삭제](/docs/12.x/eloquent#soft-deleting) 모델을 인덱싱하고 있으며, 소프트 삭제된 모델도 검색 대상으로 하려면 `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 설정하세요.

```php
'soft_delete' => true,
```

이 설정이 `true`이면 Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 인덱스에 숨겨진 `__soft_deleted` 속성을 설정합니다. 그런 다음 검색 시 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드도 함께 혹은 오직 그것만 가져올 수 있습니다.

```php
use App\Models\Order;

// 소프트 삭제된 레코드도 포함
$orders = Order::search('Star Trek')->withTrashed()->get();

// 오직 소프트 삭제된 레코드만 포함
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 영구 삭제하면, Scout가 인덱스에서 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

엔진의 검색 행위를 더욱 세밀하게 제어해야 한다면, `search` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백에서 geo-location 데이터를 검색 옵션에 추가할 수 있습니다.

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

Scout가 검색 엔진에서 일치하는 Eloquent 모델 목록을 가져온 뒤, Eloquent를 사용해 해당 모델의 상세 정보를 불러옵니다. 이 쿼리는 `query` 메서드를 통해 커스터마이징할 수 있습니다. `query` 메서드는 Eloquent 쿼리 빌더 인스턴스를 인수로 받는 클로저를 매개변수로 받습니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 검색 엔진에서 관련 모델을 이미 가져온 후 호출되므로, 결과 "필터링" 용도로는 사용하지 말고 [Scout where 조건절](#where-clauses)을 활용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 구현하기

기본 제공 Scout 검색 엔진이 요구 사항에 맞지 않는다면, 직접 커스텀 엔진을 만들어 Scout에 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 확장해야 하며, 이 클래스는 아래의 8개 메서드를 구현해야 합니다.

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

이 메서드의 구체적인 예시로 `Laravel\Scout\Engines\AlgoliaEngine` 클래스의 구현을 참고하면 커스텀 엔진 개발에 큰 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진을 구현했다면, Scout의 엔진 매니저에서 `extend` 메서드를 사용해 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 꺼낼 수 있습니다. `App\Providers\AppServiceProvider`의 `boot` 메서드나, 애플리케이션에서 사용하는 다른 서비스 프로바이더에서 `extend`를 호출하세요.

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

등록한 뒤에는 애플리케이션의 `config/scout.php` 설정 파일에서 Scout 기본 `driver`를 지정하면 됩니다.

```php
'driver' => 'mysql',
```
