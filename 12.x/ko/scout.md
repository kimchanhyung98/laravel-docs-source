# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐 사용하기](#queueing)
- [드라이버 사전 준비사항](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 구성하기](#configuring-model-indexes)
    - [검색 가능한 데이터 구성하기](#configuring-searchable-data)
    - [모델 ID 구성하기](#configuring-the-model-id)
    - [모델별 검색 엔진 구성하기](#configuring-search-engines-per-model)
    - [사용자 식별하기](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [색인(Indexing)](#indexing)
    - [배치 가져오기](#batch-import)
    - [레코드 추가하기](#adding-records)
    - [레코드 업데이트하기](#updating-records)
    - [레코드 삭제하기](#removing-records)
    - [색인 작업 일시중지하기](#pausing-indexing)
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색하기](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)은 [Eloquent 모델](/docs/12.x/eloquent)에 전체 텍스트 검색 기능을 간편히 추가할 수 있는 드라이버 기반 솔루션입니다. Scout는 모델 옵저버를 통해 검색 색인과 Eloquent 레코드를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL (`database`) 드라이버를 기본으로 제공합니다. 또한 로컬 개발 환경에서 외부 의존성이나 서드파티 서비스를 필요로 하지 않는 "컬렉션" 드라이버를 포함합니다. 더불어 간단히 커스텀 드라이버를 작성하여 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 통해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

설치 후에는 `vendor:publish` Artisan 명령어를 사용해 Scout 설정 파일을 게시하세요. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 생성합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로 `Laravel\Scout\Searchable` 트레이트를 검색 가능하게 할 모델에 추가하세요. 이 트레이트는 검색 드라이버와 자동으로 동기화하는 모델 옵저버를 등록합니다:

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
### 큐 사용하기 (Queueing)

Scout를 사용하기 위해 꼭 필요한 것은 아니지만, [큐 드라이버](/docs/12.x/queues) 설정을 강력히 권장합니다. 큐 워커를 실행하면 모델 데이터를 검색 색인과 동기화하는 작업이 큐에 쌓이게 되어, 웹 인터페이스의 응답 속도가 크게 향상됩니다.

큐 드라이버를 구성한 후에는 `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 변경하세요:

```php
'queue' => true,
```

`queue` 옵션이 `false`로 설정되어 있더라도, Algolia나 Meilisearch 같은 일부 드라이버는 항상 비동기적으로 색인을 생성합니다. 즉, Laravel 애플리케이션 내에서 색인 작업이 완료되었다고 해도 검색 엔진이 바로 실제 데이터를 반영하지 않을 수 있습니다.

Scout 작업이 사용할 연결 및 큐를 지정하려면, `queue` 옵션을 배열 형태로 설정할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

연결과 큐를 커스터마이징했다면 해당 연결과 큐에서 작업을 처리할 큐 워커를 반드시 실행하세요:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비사항 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 경우, `config/scout.php` 설정 파일에 Algolia `id`와 `secret` 자격증명을 구성해야 합니다. 자격증명 설정 후에는 Composer를 통해 Algolia PHP SDK를 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠른 오픈 소스 검색 엔진입니다. 로컬 머신 설치 방법을 모를 경우, Laravel 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail#meilisearch)을 사용해 쉽게 설치할 수 있습니다.

Meilisearch 드라이버 사용 시 Composer로 Meilisearch PHP SDK를 설치하세요:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

이후 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch의 `host`, `key` 자격증명을 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 더 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용 중인 Meilisearch 바이너리 버전에 맞는 `meilisearch/meilisearch-php` 버전을 선택해 설치해야 하므로, [Meilisearch 바이너리 호환성 안내](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 확인하시기 바랍니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 경우, Meilisearch 서비스 자체의 [추가적인 주요 변경사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 검토하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 고속의 오픈 소스 검색 엔진으로, 키워드 검색, 의미 기반 검색(semantic search), 지리 검색(geo search), 벡터 검색(vector search)을 지원합니다.

[Typesense를 직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 이용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer를 통해 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

이후 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Typesense의 호스트, API 키 자격증명을 설정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)를 사용하는 경우, `TYPESENSE_HOST` 환경 변수를 Docker 컨테이너 이름으로 조정해야 할 수도 있습니다. 추가로 설치한 인스턴스의 포트, 경로(path), 프로토콜도 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션에 관한 추가 설정과 스키마 정의는 애플리케이션의 `config/scout.php` 파일에 있습니다. 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장용 데이터 준비

Typesense를 사용할 때는 모델의 기본 키를 문자열로 캐스팅하고 생성일을 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드를 반드시 정의해야 합니다:

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

이와 함께, `config/scout.php` 파일 내에서 Typesense 컬렉션의 스키마를 정의해야 합니다. 컬렉션 스키마는 Typesense 검색에 사용되는 필드별 데이터 타입을 설명합니다. 모든 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)에서 확인할 수 있습니다.

스키마를 한 번 정의한 이후 변경하려면, 기존 인덱스 데이터를 삭제하고 다시 생성하는 `scout:flush` 및 `scout:import` 명령어를 실행하거나, Typesense API를 통해 기존 데이터 유지 상태로 스키마만 수정할 수도 있습니다.

모델이 소프트 삭제를 지원하는 경우에는 `config/scout.php` 내 Typesense 스키마에 `__soft_deleted` 필드를 다음과 같이 정의해야 합니다:

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
#### 동적 검색 파라미터 (Dynamic Search Parameters)

Typesense는 검색 작업 시 `options` 메서드를 사용해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 조절하는 기능을 제공합니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 구성하기 (Configuring Model Indexes)

각 Eloquent 모델은 특정 검색 "인덱스"와 동기화되어 해당 모델의 검색 가능한 기록을 담고 있습니다. 즉, 각 인덱스는 MySQL의 테이블과 비슷하다고 생각하면 됩니다. 기본적으로 모델은 보통의 테이블명(주로 모델 이름의 복수형)과 동일한 인덱스에 저장됩니다. 모델별 인덱스 이름을 바꾸려면 모델에서 `searchableAs` 메서드를 오버라이드하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연결된 인덱스 이름을 반환합니다.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 구성하기 (Configuring Searchable Data)

기본적으로 모델의 `toArray` 메서드 결과 전체가 검색 인덱스에 저장됩니다. 저장할 데이터를 맞춤화하려면 `toSearchableArray` 메서드를 모델에 오버라이드하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 색인용 데이터 배열을 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열에 맞춤 변환...

        return $array;
    }
}
```

Meilisearch 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 정확한 타입 데이터에만 지원합니다. 따라서 커스터마이징 시에는 숫자 값의 캐스팅 타입에 유의하세요:

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
#### 인덱스 설정 구성하기 (Algolia)

Algolia 인덱스에 추가 설정을 적용하고자 할 때는 UI 대신 앱의 `config/scout.php` 설정 파일에서 직접 관리하는 것이 편리할 수 있습니다.

이 방식은 수동 설정 없이도 자동화된 배포 파이프라인에 설정을 포함시켜 여러 환경에서 설정 일관성을 유지할 수 있습니다. 필터 가능 속성(filterable attributes), 랭킹, 패싯팅(faceting), 기타 [지원하는 설정 항목](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)도 여기에 포함됩니다.

예를 들어, `config/scout.php`에서 모델별 인덱스 설정을 아래처럼 정의할 수 있습니다:

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
            // 기타 설정 항목들...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```

소프트 삭제를 지원하는 모델이 `index-settings`에 포함되어 있다면, Scout는 해당 인덱스에 소프트 삭제된 모델의 패싯팅(facet) 지원을 자동으로 추가합니다. 만약 소프트 삭제 모델 인덱스에 별도의 패싯팅 속성이 없다면 빈 배열로 설정해줘도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 완료한 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 현재 설정 상태를 알려줘야 합니다. 이 과정을 배포 과정에 포함시키는 것도 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정 (Meilisearch)

Meilisearch는 Scout의 다른 드라이버와 달리, 필터 가능 속성(filterable attributes), 정렬 가능 속성(sortable attributes), 기타 [지원하는 설정 항목](https://docs.meilisearch.com/reference/api/settings.html)을 사전에 정의해야 합니다.

`where` 메서드에서 필터링할 속성이 필터 가능 속성이고, `orderBy`에서 정렬할 속성은 정렬 가능 속성이어야 합니다. 설정 파일의 `meilisearch` 항목 내 `index-settings` 배열에 모델별 설정을 작성하세요:

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
            // 기타 설정 항목들...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```

소프트 삭제가 지원되는 모델이라면 `index-settings`에 포함시키면 자동으로 소프트 삭제 필터링 기능이 추가됩니다. 해당 인덱스에 필터 가능 또는 정렬 가능 속성이 없다면 빈 배열로 작성해도 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

변경 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Meilisearch에 설정을 알려주는 것을 잊지 마세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 구성하기 (Configuring the Model ID)

기본적으로 Scout는 모델의 기본 키를 색인의 고유 식별자로 사용합니다. 이를 커스터마이징하려면 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 색인에 사용될 값을 반환합니다.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 색인에 사용될 키 이름을 반환합니다.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 구성하기 (Configuring Search Engines per Model)

보통 Scout는 `config/scout.php` 설정 파일에서 지정한 기본 검색 엔진을 사용합니다. 하지만 특정 모델만 별도의 검색 엔진을 사용하도록 설정하려면, 모델에서 `searchableUsing` 메서드를 오버라이드하세요:

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
     * 모델에 사용되는 엔진을 반환합니다.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별하기 (Identifying Users)

Scout는 [Algolia](https://algolia.com)를 사용할 때 자동으로 사용자를 식별할 수 있습니다. 이 기능은 사용자가 실행한 검색과 관련된 분석 데이터를 Algolia 대시보드에서 확인할 때 유용합니다. 활성화하려면 앱 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하세요:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 켜면 요청 IP 주소와 인증된 사용자 기본 식별자가 Algolia에 전달되어, 검색 요청과 사용자를 연동시킵니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

작거나 중간 규모 데이터베이스에서 경량 작업이 주라면 Scout의 "database" 엔진이 편리합니다. 데이터베이스 엔진은 기존 데이터베이스에서 "where like" 절과 전체 텍스트 인덱스를 사용해 쿼리 조건에 맞는 검색 결과를 찾습니다.

데이터베이스 엔진을 사용하려면 `SCOUT_DRIVER` 환경 변수를 `database`로 설정하거나 `scout` 설정 파일의 `driver`를 `database`로 지정하세요:

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 기본 드라이버로 설정한 이후에는 [검색 가능한 데이터 구성](#configuring-searchable-data)을 완료하고, [검색 실행하기](#searching)를 시작하면 됩니다. Algolia, Meilisearch, Typesense 등 외부 검색 엔진 색인 작업은 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [검색 가능한](#configuring-searchable-data) 모든 모델 속성에 대해 "where like" 쿼리를 수행합니다. 하지만 경우에 따라 성능 저하가 발생할 수 있기 때문에, 일부 열은 전체 텍스트 검색, 다른 열은 문자열 접두사 검색(`example%`) 등으로 검색 전략을 지정할 수 있습니다.

이 동작은 PHP 8의 속성(attributes)을 모델의 `toSearchableArray` 메서드에 다음과 같이 적용해 지정 가능합니다. 지정하지 않은 모든 컬럼은 기본 "where like" 검색을 사용합니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델 색인용 데이터 배열을 반환합니다.
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
> 컬럼에 전체 텍스트 검색을 적용하려면 먼저 해당 컬럼에 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 설정되어 있어야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

개발 시 Algolia, Meilisearch, Typesense 검색 엔진 사용이 가능하지만, "collection" 엔진으로 시작하면 더 간단할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스 결과를 대상으로 "where" 절과 컬렉션 필터링을 사용해 검색 결과를 찾습니다. 이 엔진을 사용하면 실제 검색용 인덱스를 만들 필요 없이 로컬 데이터베이스에서 직접 데이터를 조회합니다.

컬렉션 엔진을 사용하려면 `SCOUT_DRIVER` 환경 변수를 `collection`으로 설정하거나 `scout` 설정 파일에서 `collection` 드라이버를 지정하세요:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버로 설정 후에는 [검색 실행](#searching)이 가능하며, Algolia, Meilisearch, Typesense 인덱싱은 필요 없습니다.

#### 데이터베이스 엔진과의 차이점

데이터베이스 엔진과 컬렉션 엔진은 모두 직접 데이터베이스에서 조회한다는 점에서 비슷합니다. 하지만 컬렉션 엔진은 전체 텍스트 인덱스나 `LIKE` 절을 사용하지 않고, 가능한 모든 레코드를 가져와 Laravel의 `Str::is` 헬퍼를 활용해 모델 속성 값 내에 검색어가 포함되어 있는지 찾습니다.

컬렉션 엔진은 Laravel에서 지원하는 모든 관계형 데이터베이스(MySQL, SQLite, SQL Server 등)에서 동작하는 가장 이식성 높은 검색 엔진이지만, 데이터베이스 엔진보다는 효율성이 떨어집니다.

<a name="indexing"></a>
## 색인(Indexing)

<a name="batch-import"></a>
### 배치 가져오기 (Batch Import)

기존 프로젝트에 Scout를 도입할 때는 이미 데이터베이스에 있는 레코드를 색인에 넣어야 할 수 있습니다. Scout는 `scout:import` Artisan 명령어로 모든 기존 레코드를 검색 인덱스에 가져올 수 있게 지원합니다:

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` 명령어는 [큐 작업](/docs/12.x/queues)을 사용해 기존 레코드를 가져오는 작업을 실행합니다:

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` 명령어는 모델에 등록된 모든 레코드를 색인에서 삭제합니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정하기

가져오기 시 사용하는 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 예를 들어, 가져오기 전 관련 관계를 미리 로드하는 경우에 좋습니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 일괄 검색 가능 처리시 사용할 쿼리를 수정합니다.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 큐를 사용해 배치 가져오기를 할 경우, 작업 처리 중 모델 관계가 [복원되지 않으므로](/docs/12.x/queues#handling-relationships) 이 메서드가 적용되지 않을 수 있습니다.

<a name="adding-records"></a>
### 레코드 추가하기 (Adding Records)

모델에 `Laravel\Scout\Searchable` 트레이트를 추가한 후, 단순히 모델을 `save`하거나 `create` 하면 자동으로 검색 인덱스에 추가됩니다. 큐를 설정한 경우, 색인 작업은 백그라운드 큐 워커가 담당합니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가하기

Eloquent 쿼리에 `searchable` 메서드를 체인으로 호출해 여러 모델을 한 번에 검색 인덱스에 추가할 수 있습니다. 이 메서드는 결과를 [청크(chunk)](/docs/12.x/eloquent#chunking-results) 단위로 처리합니다. 큐 사용 시 작업들이 모두 백그라운드에서 처리됩니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

관계 쿼리 인스턴스에서도 호출 가능:

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션을 메모리에 갖고 있다면 컬렉션에서 직접 호출해 대응 색인에 저장할 수 있습니다:

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "업서트(upsert)" 작업과 같습니다. 이미 색인에 있는 레코드는 업데이트되고, 없으면 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트하기 (Updating Records)

검색 가능한 모델을 업데이트하려면 단순히 모델 속성을 수정하고 데이터베이스에 `save`하면 됩니다. Scout가 자동으로 색인에 변경 사항을 반영합니다:

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 내역 수정...

$order->save();
```

Eloquent 쿼리에서 `searchable` 메서드를 호출해 여러 모델을 동시에 업데이트할 수도 있습니다. 색인에 없던 모델은 새로 생성됩니다:

```php
Order::where('price', '>', 100)->searchable();
```

관계 쿼리 인스턴스나 이미 메모리에 있는 Eloquent 모델 컬렉션에서도 다음과 같이 호출할 수 있습니다:

```php
$user->orders()->searchable();

$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 가져오기 전 레코드 수정하기

일괄 처리하기 전에 모델 컬렉션을 준비해야 할 때가 있습니다. 예를 들어, 관계 데이터를 효율적으로 검색 인덱스에 포함하기 위해 연관 관계를 미리 로드하는 경우입니다. 이런 때는 모델에 `makeSearchableUsing` 메서드를 정의하세요:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능 처리할 모델 컬렉션을 조작합니다.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제하기 (Removing Records)

색인에서 레코드를 삭제하려면 데이터베이스에서 모델을 `delete` 하면 됩니다. 이는 [소프트 삭제](/docs/12.x/eloquent#soft-deleting) 경우에도 마찬가지입니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 가져오지 않고 바로 삭제하려면 Eloquent 쿼리에서 `unsearchable` 메서드를 호출하세요:

```php
Order::where('price', '>', 100)->unsearchable();
```

관계 쿼리 인스턴스나 모델 컬렉션에서도 `unsearchable`을 호출할 수 있습니다:

```php
$user->orders()->unsearchable();

$orders->unsearchable();
```

모델의 모든 검색 인덱스 기록을 제거하려면 `removeAllFromSearch` 메서드를 사용하세요:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 색인 작업 일시중지하기 (Pausing Indexing)

일괄로 여러 Eloquent 작업을 수행할 때 색인 동기화를 하지 않아야 할 경우, `withoutSyncingToSearch` 메서드에 클로저를 전달해 실행할 수 있습니다. 이 클로저 내에서 발생하는 모델 변경 작업은 색인에 동기화되지 않습니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스 (Conditionally Searchable Model Instances)

특정 조건에서만 모델을 검색 가능하게 할 수도 있습니다. 예를 들어 `App\Models\Post` 모델에 "draft"와 "published" 상태가 있으며, "published" 상태만 검색 가능하도록 하려면 `shouldBeSearchable` 메서드를 정의하세요:

```php
/**
 * 모델이 검색 가능해야 하는지 여부를 판단합니다.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`, `create`, 쿼리, 관계를 통해 모델을 조작할 때만 적용됩니다. 직접 `searchable` 메서드로 모델이나 컬렉션을 처리하면 이 메서드보다 우선합니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에서 동작하지 않습니다. 이 엔진은 모든 데이터를 항상 데이터베이스에 저장하므로, 데이터베이스 엔진을 사용할 때는 [where 절](#where-clauses)을 사용해 비슷한 로직을 구현해야 합니다.

<a name="searching"></a>
## 검색하기 (Searching)

모델 검색은 `search` 메서드로 시작합니다. 하나의 문자열 인수를 받아 해당 문자열로 모델을 검색합니다. 검색 결과는 `get` 메서드를 체인해 Eloquent 모델 컬렉션으로 반환받습니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout의 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트나 컨트롤러에서 그대로 반환하면 JSON으로 자동 변환됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

검색 결과를 Eloquent 모델로 변환하지 않은 원시(raw) 데이터로 받고 싶으면 `raw` 메서드를 사용하세요:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 사용하기

검색은 기본적으로 모델의 [searchableAs](#configuring-model-indexes)에서 지정한 인덱스를 대상으로 수행됩니다. 하지만 `within` 메서드로 검색할 인덱스를 직접 지정할 수도 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절 (Where Clauses)

Scout는 기본 숫자 동등 비교 등의 간단한 "where" 절 추가를 지원합니다. 주로 소유자 ID 등으로 검색 범위를 한정할 때 유용합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn` 메서드를 사용해 특정 컬럼 값이 배열 내에 있는지 검사할 수 있습니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 배열 내에 값이 없는 경우를 검색합니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 색인은 관계형 데이터베이스가 아니므로, 더 복잡한 where 절은 현재 지원하지 않습니다.

> [!WARNING]
> Meilisearch를 사용할 경우, Scout의 "where" 절 기능을 사용하기 전에 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 반드시 설정해야 합니다.

<a name="pagination"></a>
### 페이지네이션 (Pagination)

검색 결과는 단순 컬렉션뿐 아니라 `paginate` 메서드로 페이지별 조회가 가능합니다. 이때 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환하며, 일반 Eloquent 쿼리처럼 [페이지네이션](/docs/12.x/pagination)이 작동합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

한 페이지에 표시할 개수를 첫 번째 인자로 전달할 수도 있습니다:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과는 [Blade](/docs/12.x/blade)에서 일반 쿼리 페이지네이션처럼 다음과 같이 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 받으려면 라우트나 컨트롤러에서 직접 페이저 인스턴스를 반환하면 됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프(global scopes)를 인지하지 못하므로, Scout 페이지네이션 사용하는 애플리케이션에서는 글로벌 스코프 사용을 피하거나, 검색 시 스코프 조건을 다시 수동으로 적용해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

색인 중인 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)되어 있고, 소프트 삭제된 모델을 검색해야 한다면 `config/scout.php`의 `soft_delete` 옵션을 `true`로 설정하세요:

```php
'soft_delete' => true,
```

이 옵션이 활성화되면 Scout는 소프트 삭제된 레코드를 색인에서 삭제하지 않고 `__soft_deleted`라는 숨겨진 속성으로 표시합니다. 이후 검색 시 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해 삭제된 레코드를 함께 조회하거나, 삭제된 레코드만 조회할 수 있습니다:

```php
use App\Models\Order;

// 삭제된 레코드 포함해서 조회...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된 레코드만 조회...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 완전 삭제하면, Scout는 해당 레코드를 자동으로 색인에서 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

엔진별로 고급 검색 커스터마이징이 필요하면 `search` 메서드 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어 Algolia에 지리 위치 데이터를 추가하는 코드입니다:

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

Scout가 검색 엔진에서 매치하는 모델 목록을 받아온 후, Eloquent가 해당 기본 키들로 실제 모델을 조회합니다. 이 쿼리를 커스터마이징하려면 `query` 메서드를 호출하세요. `query`는 Eloquent 쿼리 빌더 인스턴스를 인자로 받는 클로저를 받습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 모델 ID를 검색 엔진에서 구한 후 실행되므로, 결과 필터링은 [Scout where 절](#where-clauses)를 사용해야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기 (Writing the Engine)

기본 제공되는 Scout 검색 엔진이 맞지 않을 경우, 직접 커스텀 엔진을 구현해 Scout에 등록할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음 8개 추상 메서드를 구현해야 합니다:

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

`Laravel\Scout\Engines\AlgoliaEngine` 클래스의 구현체를 참고하면 메서드별 구현 방식을 이해하는 데 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기 (Registering the Engine)

커스텀 엔진을 완성하면 Laravel 서비스 컨테이너에서 Scout의 엔진 매니저를 불러와 `extend` 메서드로 등록해야 합니다. `App\Providers\AppServiceProvider`나 애플리케이션에서 사용하는 다른 서비스 프로바이더의 `boot` 메서드 내에서 호출하세요:

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

등록 후에는 `config/scout.php` 설정 파일에서 기본 `driver`로 커스텀 엔진 이름을 지정할 수 있습니다:

```php
'driver' => 'mysql',
```