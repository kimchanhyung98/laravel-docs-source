# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 요구사항](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능 데이터 설정](#configuring-searchable-data)
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
    - [인덱싱 일시중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제 지원](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 풀텍스트 검색을 손쉽게 추가할 수 있는, 드라이버 기반 간단한 솔루션을 제공합니다. 모델 옵저버를 사용하여 Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL/PostgreSQL(`database`) 드라이버를 기본 제공합니다. 또한, Scout에는 외부 의존성이나 서드파티 서비스가 필요 없는 "collection" 드라이버도 포함되어 있어 로컬 개발 환경에 적합합니다. 그 밖에도, 커스텀 드라이버 작성이 간단하며 원하는 검색 구현으로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 이용해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

설치 후 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 발행합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 복사합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 자동으로 모델 옵저버를 등록하여 모델과 검색 드라이버의 동기화를 유지합니다:

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

Scout 사용에 필수 사항은 아니지만, [큐 드라이버](/docs/12.x/queues)를 설정하는 것이 매우 권장됩니다. 큐 워커를 실행하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐에 넣어 웹 인터페이스의 반응 속도를 크게 개선합니다.

큐 드라이버를 설정한 후에는 `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 변경하세요:

```php
'queue' => true,
```

`queue` 옵션이 `false`일 때도, Algolia와 Meilisearch 같은 일부 Scout 드라이버는 항상 비동기적으로 인덱싱합니다. 즉, Laravel 애플리케이션 내부에서 인덱스 작업이 완료되더라도, 검색 엔진에서는 새 기록이 바로 반영되지 않을 수 있습니다.

Scout 작업에 사용할 연결과 큐를 지정하려면 `queue` 옵션을 배열형태로 정의하세요:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

연결과 큐를 커스텀 설정하면 해당 연결과 큐에서 작업을 처리할 큐 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 요구사항

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는 `config/scout.php`에서 Algolia `id`와 `secret` 자격 증명을 설정해야 합니다. 자격 증명 설정 후에는 Composer를 통해 Algolia PHP SDK를 설치하세요:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 빠르고 오픈 소스인 검색 엔진입니다. 로컬 머신에 Meilisearch 설치 방법이 궁금하다면, Laravel 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버 사용 시에는 Composer로 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그런 다음, `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch 호스트 및 키 자격 증명을 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 자세한 내용은 [Meilisearch 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한 Meilisearch 바이너리 버전에 호환되는 `meilisearch/meilisearch-php` 버전을 설치했는지 [바이너리 호환성 안내](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 확인해야 합니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 반드시 [Meilisearch 서비스 자체의 추가 파괴적 변경 사항](https://github.com/meilisearch/Meilisearch/releases)를 확인하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 빠르고 오픈 소스인 검색 엔진으로, 키워드 검색, 의미론적 검색, 지리 검색, 벡터 검색을 지원합니다.

Typesense를 직접 호스팅([self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting))하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그 후 `.env` 파일에 `SCOUT_DRIVER`와 Typesense 호스트 및 API 키를 설정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, `TYPESENSE_HOST` 환경 변수는 Docker 컨테이너 이름에 맞게 조정해야 할 수 있습니다. 또한 설치 포트, 경로, 프로토콜도 선택적으로 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

추가 설정과 Typesense 컬렉션 스키마 정의는 애플리케이션의 `config/scout.php` 파일에서 할 수 있습니다. Typesense에 대한 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장용 데이터 준비

Typesense 사용 시, 검색 가능 모델은 기본키를 문자열로, 생성일을 UNIX 타임스탬프로 캐스팅하는 `toSearchableArray` 메서드를 정의해야 합니다:

```php
/**
 * 인덱스에 저장할 데이터 배열을 반환합니다.
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

Typesense 컬렉션 스키마를 애플리케이션의 `config/scout.php`에서 정의하세요. 컬렉션 스키마는 Typesense로 검색 가능한 각 필드의 데이터 유형을 설명합니다. 스키마 옵션 전체에 대한 내용은 [Typesense 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마가 정의된 후 변경이 필요하면 `scout:flush`와 `scout:import` 명령어를 통해 모든 인덱스 데이터를 삭제 후 재생성하거나, Typesense API를 사용해 인덱스 데이터를 유지하며 스키마만 수정할 수 있습니다.

소프트 삭제 가능한 모델이라면, Typesense 스키마에 `__soft_deleted` 필드를 정의해야 합니다(`config/scout.php` 내에서):

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

Typesense는 `options` 메서드를 통해 검색 수행 시 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 변경할 수 있습니다:

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

각 Eloquent 모델은 해당 모델의 모든 검색 가능 레코드를 담는 특정 검색 "인덱스"와 동기화됩니다. 쉽게 말해, 각 인덱스는 MySQL 테이블과 비슷한 개념입니다. 기본적으로 모델은 모델 이름의 복수형을 따르는 테이블명과 동일한 인덱스에 저장됩니다. 하지만 `searchableAs` 메서드를 오버라이드하여 인덱스 이름을 자유롭게 변경할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연관된 인덱스 이름을 반환합니다.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능 데이터 설정

기본적으로 모델의 전체 `toArray` 결과가 인덱스에 저장됩니다. 저장할 데이터를 커스터마이징하려면 모델에서 `toSearchableArray` 메서드를 재정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 인덱스에 저장할 데이터 배열을 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 데이터 배열을 커스터마이징합니다...

        return $array;
    }
}
```

일부 검색 엔진(예: Meilisearch)은 필터 연산자(`>`, `<` 등)를 올바른 타입의 데이터에만 적용합니다. 따라서 이들 엔진을 사용할 때는 숫자형 값들을 적절한 타입으로 캐스팅해야 합니다:

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
#### 인덱스 설정 구성 (Algolia)

Algolia 인덱스에 추가 설정을 적용하고 싶을 때가 있습니다. Algolia UI를 통해 설정할 수도 있지만, 보통은 애플리케이션의 `config/scout.php` 설정 파일에서 직접 관리하는 것이 자동화된 배포 과정에 포함시킬 수 있어 더 효율적입니다. 이렇게 하면 수동 설정 없이 여러 환경에서 인덱스 설정을 일관되게 유지할 수 있습니다.

필터 가능 속성, 랭킹, 패싯팅(faceting), 또는 [그 밖의 지원 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)들을 설정할 수 있습니다.

시작하려면 `config/scout.php` 내 각 인덱스에 설정 값을 추가하세요:

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

만약 소프트 삭제 가능한 모델이 인덱스 설정에 포함되어 있다면 Scout는 해당 인덱스에 소프트 삭제 모델 필터링 기능을 자동 포함합니다. 패싯 속성을 따로 지정하지 않는다면 비어있는 배열만 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 변경 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 동기화하세요. 이 명령어는 배포 프로세스에 포함시키는 것도 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정 구성 (Meilisearch)

Scout 다른 드라이버와는 달리 Meilisearch는 필터 가능 속성(filterableAttributes), 정렬 가능 속성(sortableAttributes) 등 [사전에 정의된 인덱스 검색 설정](https://docs.meilisearch.com/reference/api/settings.html)을 요구합니다.

filterableAttributes는 Scout의 `where` 메서드로 필터링할 때 사용할 속성들이며, sortableAttributes는 `orderBy` 메서드로 정렬할 속성들입니다. 이 설정들은 `config/scout.php` 파일 내 `meilisearch` 설정 부분의 `index-settings` 배열에서 조정합니다:

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

소프트 삭제 가능 모델이 포함된 인덱스라면 Scout가 자동으로 소프트 삭제 필터링을 지원합니다. 별도의 필터나 정렬 속성이 없다면 빈 배열로 설정 가능합니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Meilisearch에 동기화하세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본키를 인덱스에 저장되는 고유 식별자로 사용합니다. 이 동작을 변경하려면 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용할 값을 반환합니다.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용할 키 이름을 반환합니다.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

검색 시 기본적으로 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 하지만 특정 모델별로 사용할 검색 엔진을 바꾸려면 `searchableUsing` 메서드를 오버라이드하세요:

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
     * 이 모델에 사용할 검색 엔진을 반환합니다.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시 검색 작업과 인증된 사용자를 자동 연결하는 기능을 제공합니다. Algolia 대시보드에서 검색 분석 시 도움이 됩니다. `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 정의하여 활성화할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```

이 옵션을 활성화하면 요청자의 IP 주소와 인증된 사용자의 기본 식별자가 Algolia로 전달되어 검색 요청에 관련 데이터가 연동됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

작고 중간 규모 데이터베이스를 다루거나 가벼운 작업 부하가 있는 애플리케이션에서는 Scout "database" 엔진을 간편하게 사용할 수 있습니다. 이 엔진은 모델 속성에 대해 `where like` 조건문과 풀텍스트 인덱스를 사용해 검색 쿼리 결과를 필터링합니다.

`SCOUT_DRIVER` 환경 변수를 `database`로 설정하거나, 애플리케이션 설정 파일에서 직접 `database` 드라이버를 지정하세요:

```ini
SCOUT_DRIVER=database
```

드라이버를 지정한 후 [검색 가능 데이터 설정](#configuring-searchable-data)을 진행하고, [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense 같은 외부 인덱스 엔진을 위한 별도의 인덱싱 과정은 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 모델의 모든 검색 가능 속성에 대해 "where like" 쿼리를 수행합니다. 하지만 상황에 따라 성능이 떨어질 수 있으므로, 특정 컬럼에 대해서만 풀텍스트 쿼리를 하거나 문자열 접두사 검색(`example%`)만 수행하도록 검색 전략을 설정할 수 있습니다.

이 동작은 모델의 `toSearchableArray` 메서드에 PHP 속성(Attribute)을 적용해서 정의합니다. 명시하지 않은 컬럼은 기본 "where like" 전략을 따릅니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 인덱스에 저장할 데이터 배열을 반환합니다.
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
> 컬럼에 풀텍스트 쿼리를 지정하기 전에 해당 컬럼에 [풀텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 달려 있는지 반드시 확인해야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서 Algolia, Meilisearch, Typesense 대신 "collection" 엔진을 사용할 수 있습니다. 컬렉션 엔진은 데이터베이스에서 "where" 절과 컬렉션 필터링 방식으로 검색 결과를 추출합니다. 따라서 "인덱싱" 자체가 필요 없고 로컬 DB에서 모델을 직접 조회합니다.

`SCOUT_DRIVER`를 `collection`로 설정하거나, 설정 파일에 `collection` 드라이버를 지정하면 됩니다:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 지정한 뒤 [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense 같은 인덱싱 과정은 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이점

"database"와 "collection" 엔진은 모두 직접 데이터베이스와 상호작용한다는 점에서 비슷하지만, 컬렉션 엔진은 풀텍스트 인덱스나 `LIKE`절을 사용하지 않고, 대신 모든 가능한 레코드를 불러온 후 Laravel의 `Str::is` 헬퍼를 이용해 검색어가 포함된 데이터를 판별합니다.

컬렉션 엔진은 SQLite, SQL Server 등 Laravel에서 지원하는 모든 관계형 데이터베이스에서 포터블하게 동작하지만, 데이터베이스 엔진에 비해 효율이 낮습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 설치하는 경우, 이미 저장된 데이터베이스 레코드를 검색 인덱스에 임포트해야 할 수 있습니다. Scout는 `scout:import` Artisan 명령어를 제공하며, 이를 통해 기존 레코드를 인덱스에 한 번에 임포트할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

작업을 대기열(큐)로 처리하려면 `scout:queue` 명령어를 사용하세요:

```shell
php artisan scout:queue "App\Models\Post" --chunk=500
```

모델의 모든 인덱스 레코드를 삭제하려면 `flush` 명령어를 사용합니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 수정

임포트할 모델 조회 쿼리를 수정하려면 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 예를 들어, 임포트 전에 관계 데이터를 함께 로드할 때 유용합니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모델 전체를 인덱스에 넣을 때 사용하는 쿼리를 수정합니다.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 모델을 큐로 배치 임포트하는 경우에는, 조인된 관계 데이터가 [복원되지 않는 점](/docs/12.x/queues#handling-relationships)을 주의하세요.

<a name="adding-records"></a>
### 레코드 추가

모델에 `Searchable` 트레이트를 추가한 후, 모델을 `save` 또는 `create`하면 자동으로 인덱스에 레코드가 추가됩니다. 큐를 설정했다면 이 작업은 큐 워커가 백그라운드에서 처리합니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리에 `searchable` 메서드를 체인으로 호출하면, 쿼리 결과를 청크 단위로 나누어 인덱스에 저장합니다. 큐가 설정된 경우 백그라운드에서 처리됩니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

관계에서도 동일하게 사용 가능합니다:

```php
$user->orders()->searchable();
```

이미 메모리에 불러온 Eloquent 모델 컬렉션에도 `searchable` 메서드를 호출하여 인덱스에 저장할 수 있습니다:

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 인덱스에 없는 경우 새로 추가하고, 이미 존재하면 갱신하는 "업서트(upsert)" 기능입니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능 모델을 업데이트하려면 단순히 모델 속성을 변경하고 `save`하세요. Scout가 자동으로 인덱스를 갱신합니다:

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 업데이트...

$order->save();
```

쿼리 인스턴스에도 `searchable`을 호출해 여러 모델을 한 번에 업데이트할 수 있습니다. 없는 경우 새로 추가됩니다:

```php
Order::where('price', '>', 100)->searchable();
```

관계나 컬렉션에도 동일하게 호출 가능합니다:

```php
$user->orders()->searchable();

$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 임포트 전 레코드 수정

컬렉션을 검색 가능 상태로 만들기 전에 관계 데이터를 미리 로드하는 등 준비작업이 필요할 수 있습니다. 모델에 `makeSearchableUsing` 메서드를 정의하여 이를 수행하세요:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능하게 만들기 전, 모델 컬렉션을 수정합니다.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제

레코드를 인덱스에서 제거하려면 모델을 데이터베이스에서 `delete`하면 됩니다. 소프트 삭제 모델도 가능합니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 조회하지 않고 삭제하려면 쿼리에 `unsearchable` 메서드를 호출하세요:

```php
Order::where('price', '>', 100)->unsearchable();
```

관계나 컬렉션에도 동일하게 호출 가능합니다:

```php
$user->orders()->unsearchable();

$orders->unsearchable();
```

모델의 모든 인덱스 기록을 한번에 삭제하려면 `removeAllFromSearch`를 호출하세요:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시중지

일괄 작업 중에 검색 인덱스 동기화를 막고 싶을 때는 `withoutSyncingToSearch` 메서드를 사용하세요. 클로저 내에서의 모델 변경 내용은 인덱스에 반영되지 않습니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스

모델을 특정 조건에서만 검색 가능하도록 만들고 싶다면 `shouldBeSearchable` 메서드를 정의하세요. 예를 들어, `App\Models\Post`에서 "published" 상태인 게시물만 검색 가능하게 할 수 있습니다:

```php
/**
 * 모델을 검색 가능 상태로 둘지 판단합니다.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable`은 `save`, `create`, 쿼리, 관계로 모델을 다룰 때만 적용되고, `searchable` 메서드를 직접 호출하는 경우 무시됩니다.

> [!WARNING]
> "database" 엔진 사용 시에는 검색 가능 데이터가 항상 DB에 저장되기 때문에 `shouldBeSearchable`은 적용되지 않습니다. 이 경우 [where절](#where-clauses)을 사용해 필터링하세요.

<a name="searching"></a>
## 검색

모델 검색은 `search` 메서드를 이용해 문자열을 전달합니다. 기본적으로 `get` 메서드를 추가해 일치하는 Eloquent 모델 컬렉션을 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트나 컨트롤러에서 바로 반환하면 자동으로 JSON 변환됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

원시 검색 결과를 원할 경우 `raw` 메서드를 사용할 수 있습니다:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 지정

보통 모델의 [searchableAs](#configuring-model-indexes) 메서드에 의해 지정된 인덱스에서 검색이 수행됩니다. 필요하다면 `within` 메서드를 사용해 다른 인덱스를 지정할 수도 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where절

Scout 검색 쿼리에 간단한 "where" 절을 추가할 수 있습니다. 현재는 기본적인 숫자 동등 비교만 지원하므로, 주로 소유자 ID 같은 간단한 조건에 사용됩니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn` 메서드는 특정 컬럼 값이 배열 내에 포함되는지 검사합니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn`은 컬럼 값이 배열에 포함되지 않는지 검사합니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니기 때문에, 더 복잡한 where 절은 아직 지원하지 않습니다.

> [!WARNING]
> Meilisearch를 사용하는 경우, [filterable 속성](#configuring-filterable-data-for-meilisearch)을 반드시 사전에 설정해야 Scout의 where절을 사용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션

검색 결과를 컬렉션으로 받는 대신 `paginate` 메서드를 사용해 결과를 페이지네이션할 수 있습니다. Laravel의 전통적 Eloquent 쿼리와 동일하게 `Illuminate\Pagination\LengthAwarePaginator` 객체를 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

몇 개씩 받을지도 첫 인자로 지정할 수 있습니다:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과와 페이지 링크는 [Blade](/docs/12.x/blade)에서 기존 Eloquent 쿼리처럼 표시할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

JSON 반환 시에는 다음과 같이 처리하세요:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 전역 스코프(global scope)를 인지하지 못하므로, Scout 페이지네이션을 사용하는 경우 전역 스코프 사용을 피하거나 검색 시 직접 동일 조건을 반영해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제 지원

검색 대상 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원하고, 소프트 삭제된 모델도 검색하려면 `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 설정하세요:

```php
'soft_delete' => true,
```

이 설정 시 소프트 삭제된 모델은 인덱스에서 제거되는 대신 숨겨진 속성 `__soft_deleted`가 세팅됩니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 모델을 포함하여 검색할 수 있습니다:

```php
use App\Models\Order;

// 소프트 삭제 모델도 포함해 검색
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제 모델만 검색
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> `forceDelete`로 완전 삭제 시, Scout는 자동으로 해당 모델을 인덱스에서 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

고급 검색 동작이 필요한 경우, `search` 메서드의 두 번째 인자로 클로저를 넘길 수 있습니다. 예를 들어 Algolia에 지리 정보 필터를 추가할 수 있습니다:

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

Scout가 검색 엔진에서 키를 조회한 후, Eloquent를 통해 일치하는 모델 데이터를 실제로 가져올 때 사용하는 쿼리도 `query` 메서드로 커스터마이징할 수 있습니다. `query`는 Eloquent 쿼리 빌더를 전달받는 클로저를 인자로 받습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

참고로 이 콜백은 검색 엔진 조회 후에 실행되므로, 결과 필터링 목적이 아니라 결과 전처리에 사용해야 하며, 필터링은 Scout `where`절을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

내장된 Scout 검색 엔진으로 요구사항을 충족하기 어렵다면, 직접 커스텀 엔진을 작성하여 Scout에 등록할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 아래 8개 메서드를 구현해야 합니다:

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

Reference로 `Laravel\Scout\Engines\AlgoliaEngine` 클래스의 구현을 검토하면 좋은 시작점이 될 수 있습니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 작성한 후, Scout 엔진 매니저의 `extend` 메서드를 이용해 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 해석(Resolve)하며, 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록합니다:

```php
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

등록 후에는 설정 파일에서 기본 Scout 드라이버로 지정할 수 있습니다:

```php
'driver' => 'mysql',
```