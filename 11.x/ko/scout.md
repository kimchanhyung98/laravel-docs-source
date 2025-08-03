# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 전제 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 가능한 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [색인(Indexing)](#indexing)
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [색인 작업 일시 중지](#pausing-indexing)
    - [조건부 검색 가능 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이징](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)은 [Eloquent 모델](/docs/11.x/eloquent)에 전체 텍스트 검색 기능을 더하는 간단한 드라이버 기반 솔루션을 제공합니다. 모델 옵저버(observer)를 사용하여 Scout는 Eloquent 레코드와 검색 인덱스가 자동으로 동기화되도록 관리합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL (`database`) 드라이버를 기본으로 지원합니다. 추가로 외부 의존성이나 타사 서비스가 필요 없는 로컬 개발용 "collection" 드라이버도 포함되어 있습니다. 또한, 커스텀 드라이버 작성도 간단하며 자신만의 검색 구현으로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 Composer 패키지 매니저를 사용해서 Scout를 설치하세요:

```shell
composer require laravel/scout
```

Scout를 설치한 후에는 `vendor:publish` Artisan 명령어로 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령어는 `scout.php` 구성 파일을 애플리케이션의 `config` 디렉토리에 배포합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하도록 만들고 싶은 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여 모델과 검색 드라이버가 자동으로 동기화되도록 합니다:

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

<a name="queueing"></a>
### 큐잉 (Queueing)

Scout 사용에 큐 설정이 반드시 필요하지는 않지만, 큐 드라이버를 설정하는 것을 강력히 권장합니다. 큐 작업자를 실행하면, Scout가 모델 정보를 검색 인덱스에 동기화하는 모든 작업을 큐에 등록할 수 있어서 애플리케이션 웹 인터페이스의 응답 속도가 크게 향상됩니다.

큐 드라이버를 설정했다면, `config/scout.php` 파일의 `queue` 옵션 값을 `true`로 변경하세요:

```
'queue' => true,
```

`queue` 옵션이 `false`여도 Algolia, Meilisearch 같은 일부 Scout 드라이버는 항상 비동기적으로 인덱싱 작업을 수행한다는 점을 기억하세요. 즉, Laravel 애플리케이션에서 인덱싱 작업이 완료되었더라도 검색 엔진에서 새로운 데이터가 즉시 반영되지 않을 수 있습니다.

Scout 작업이 사용하는 연결 및 큐를 직접 지정하려면, `queue` 설정을 배열로 정의할 수 있습니다:

```
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

만약 큐 연결 및 큐 이름을 커스터마이징했다면, 해당 연결과 큐에서 작업을 처리할 작업자를 반드시 실행해야 합니다:

```
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 전제 조건 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버 사용 시, `config/scout.php`에 Algolia `id`와 `secret` 자격증명을 반드시 설정해야 합니다. 자격증명을 설정한 후에는 Composer를 통해 Algolia PHP SDK를 설치하세요:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬 환경에 Meilisearch를 설치하는 방법이 익숙하지 않으면, Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/11.x/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버 사용 시, Composer를 통해 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고 애플리케이션 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch의 `host` 및 `key` 자격 증명을 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch 관련 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한 Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 버전을 설치하는지 반드시 확인하세요. 관련 내용은 [Meilisearch PHP SDK의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하시기 바랍니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 Meilisearch 서비스 자체의 [추가적인 Breaking Changes](https://github.com/meilisearch/Meilisearch/releases)를 항상 검토해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 빠른 오픈 소스 검색 엔진이며, 키워드 검색, 의미 기반 검색, 위치 기반 검색, 벡터 검색을 지원합니다.

[Typesense를 직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면 Composer를 통해 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그리고 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Typesense 호스트 및 API 키 자격증명을 설정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Larevel Sail](/docs/11.x/sail)를 사용하는 경우 Docker 컨테이너 이름에 맞게 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수 있습니다. 또한 설치 환경에 맞게 포트, 경로, 프로토콜을 선택적으로 지정할 수도 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

추가 설정과 컬렉션 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 확인할 수 있습니다. 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense를 사용할 때는 검색 가능한 모델에 `toSearchableArray` 메서드를 정의해야 하며, 이 메서드에서는 모델의 기본 키를 문자열로 변환하고 생성 일자를 UNIX 타임스탬프로 변환해야 합니다:

```php
/**
 * 모델에서 색인 가능한 데이터 배열을 가져옵니다.
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

Typesense 컬렉션의 스키마는 `config/scout.php` 파일 내에서 정의해야 합니다. 컬렉션 스키마는 Typesense로 검색 가능한 각 필드의 데이터 타입을 설명합니다. 모든 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 정의한 후 변경이 필요한 경우, `scout:flush`와 `scout:import` 명령어를 실행해 기존 모든 색인 데이터를 삭제하고 스키마를 재생성할 수 있습니다. 또는 Typesense API를 사용해 색인 데이터를 제거하지 않고도 컬렉션 스키마를 수정할 수 있습니다.

모델이 소프트 삭제(soft deletable)를 지원한다면, 애플리케이션 `config/scout.php` 내 Typesense 스키마에 `__soft_deleted` 필드를 정의해야 합니다:

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

Typesense는 `options` 메서드를 통해 검색 시 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 조작할 수 있습니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정 (Configuring Model Indexes)

각 Eloquent 모델은 특정 검색 "인덱스"와 동기화됩니다. 이 인덱스는 해당 모델의 모든 검색 가능 레코드를 담고 있습니다. 쉽게 예를 들면, 각 인덱스는 MySQL 테이블과 비슷하다고 생각할 수 있습니다. 기본적으로 모델 이름의 복수형인 모델의 “테이블” 이름과 일치하는 인덱스가 사용됩니다.

인덱스 이름을 커스터마이징하려면 모델에 `searchableAs` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델에 연관된 인덱스 이름을 반환합니다.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 설정 (Configuring Searchable Data)

기본적으로 해당 모델 `toArray`가 전부 검색 인덱스로 동기화됩니다. 동기화할 데이터를 세밀하게 제어하고 싶다면 `toSearchableArray` 메서드를 오버라이드하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 색인 가능한 데이터 배열을 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 원하는 데이터로 커스터마이징 하세요...

        return $array;
    }
}
```

Meilisearch 같은 일부 검색 엔진은 필터 연산자인 (`>`, `<` 등)를 수행할 때 데이터 타입이 정확해야 합니다. 따라서 이런 검색 엔진을 사용할 때는 검색 데이터 내 숫자 값의 타입을 명확히 캐스팅하는 것이 좋습니다:

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

<a name="configuring-indexes-for-algolia"></a>
#### 인덱스 설정(Algolia)

Algolia 인덱스에 추가 설정이 필요한 경우, UI 대신 `config/scout.php`에서 구성할 수 있어 편리합니다. 이를 통해 배포 파이프라인에서 설정을 자동화할 수 있고, 여러 환경에서 일관된 구성을 유지할 수 있습니다.

필터 속성(filterable attributes), 랭킹(ranking), 패싯팅(faceting) 등 [Algolia가 지원하는 모든 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

시작하려면 `config/scout.php` 내 각 인덱스별로 설정을 추가하세요:

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

모델에 소프트 삭제가 적용되어 있고 `index-settings` 배열에 포함된다면, Scout가 자동으로 소프트 삭제 모델 대상 패싯팅 지원을 추가합니다. 별도의 패싯팅 속성이 없는 경우 빈 배열로도 등록할 수 있습니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 설정을 동기화해야 합니다. 이 명령을 배포 프로세스에 포함시키는 것이 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정(Meilisearch)

Meilisearch는 Scout의 다른 드라이버들과 달리, 필터 속성(filterable attributes), 정렬 속성(sortable attributes) 등 [사전 정의된 인덱스 설정](https://docs.meilisearch.com/reference/api/settings.html)이 필요합니다.

필터 속성은 Scout의 `where` 메서드에서 필터링할 속성들이며, 정렬 속성은 `orderBy` 메서드에서 정렬 기준으로 사용할 속성들입니다. 설정은 `config/scout.php` 파일 내 `meilisearch` 설정에 `index-settings` 배열로 추가하세요:

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

소프트 삭제 모델이 포함된 경우에도 Scout가 해당 인덱스에 대해 소프트 삭제 필터를 자동으로 지원하므로, 별도의 속성이 없다면 빈 배열로도 등록할 수 있습니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 후 반드시 `scout:sync-index-settings` 명령어로 Meilisearch에 설정을 동기화하세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정 (Configuring the Model ID)

Scout는 기본적으로 모델의 기본 키를 검색 인덱스 저장에 사용되는 고유 ID/key로 사용합니다. 이 동작을 바꾸고 싶으면 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하세요:

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
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용될 키 이름을 반환합니다.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정 (Configuring Search Engines per Model)

기본적으로 Scout는 `config/scout.php`의 기본 검색 엔진을 사용하지만, 모델별로 검색 엔진을 지정하고 싶다면 `searchableUsing` 메서드를 오버라이드하세요:

```
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
     * 모델 인덱싱에 사용할 엔진을 반환합니다.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별 (Identifying Users)

Scout는 [Algolia](https://algolia.com) 사용 시 인증된 사용자를 자동 식별할 수 있습니다. 이렇게 하면 Algolia 대시보드 내 검색 분석에 인증 사용자 관련 정보가 연결됩니다. 사용자 식별 기능을 켜려면 `.env`에 `SCOUT_IDENTIFY` 변수를 `true`로 설정하세요:

```ini
SCOUT_IDENTIFY=true
```

이 기능 활성화 시 사용자 요청 IP 주소와 인증된 사용자의 식별자가 Algolia에 전달되어, 해당 사용자로 발생한 모든 검색 요청에 데이터가 연결됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

작거나 중간 규모 데이터베이스에서 작업하거나 부하가 적은 애플리케이션엔 Scout의 "database" 엔진을 사용하는 것이 더 편리할 수 있습니다. 이 엔진은 기존 데이터베이스에서 "where like" 절과 전체 텍스트 인덱스를 사용해 검색 결과를 필터링합니다.

데이터베이스 엔진을 사용하려면 `SCOUT_DRIVER` 환경 변수 또는 `scout` 설정 파일에서 드라이버를 `database`로 지정하세요:

```ini
SCOUT_DRIVER=database
```

그런 다음 [검색 데이터 구성](#configuring-searchable-data)을 완료하면, 모델에 대해 [검색 쿼리 실행](#searching)이 가능합니다. Algolia, Meilisearch, Typesense 인덱싱 같은 검색 엔진 색인 구축 과정은 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [검색 가능 설정](#configuring-searchable-data)에 포함된 모든 모델 속성에 대해 "where like" 쿼리를 실행합니다. 하지만 일부 상황에선 성능이 떨어질 수 있기에, 컬럼별로 전체 텍스트 검색을 사용할지, 또는 문자열 접두어(prefix) 검색(`example%`)만 할지 전략을 변경할 수 있습니다.

전략은 모델의 `toSearchableArray` 메서드에 PHP 8+ 속성(attributes)으로 지정합니다. 속성을 지정하지 않은 컬럼은 기본적으로 "where like" 전략을 사용합니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델에서 색인 가능한 데이터 배열을 반환합니다.
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
> 컬럼에 전체 텍스트 검색 쿼리를 지정하기 전에 해당 컬럼에 전체 텍스트 인덱스가 생성되어 있는지 반드시 확인하세요. ([마이그레이션 문서](/docs/11.x/migrations#available-index-types) 참고)

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

로컬 개발 중에는 Algolia, Meilisearch, Typesense 대신 "collection" 엔진을 사용하는 게 더 편리할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 "where" 절과 컬렉션 필터링을 사용하여 검색 결과를 가져오므로, 별도로 인덱싱할 필요가 없습니다.

컬렉션 엔진을 사용하려면 `SCOUT_DRIVER` 환경 변수 또는 `scout` 설정 파일의 드라이버를 `collection`으로 지정하세요:

```ini
SCOUT_DRIVER=collection
```

설정 후에는 바로 모델에서 [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense 인덱싱 과정은 불필요합니다.

#### 데이터베이스 엔진과의 차이점

컬렉션과 데이터베이스 엔진은 모두 데이터베이스에 직접 접근하지만, 컬렉션 엔진은 전체 텍스트 인덱스나 `LIKE` 절을 사용하지 않습니다. 대신 모든 가능한 레코드를 가져온 뒤 Laravel의 `Str::is` 헬퍼로 문자열 내 검색어 존재 여부를 확인합니다.

컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스(SQL Server, SQLite 등 포함)에서 작동해 가장 범용적이지만, 데이터베이스 엔진에 비해 성능이 떨어질 수 있습니다.

<a name="indexing"></a>
## 색인(Indexing)

<a name="batch-import"></a>
### 배치 임포트 (Batch Import)

기존 프로젝트에 Scout를 도입하는 경우 이미 존재하는 데이터베이스 레코드를 인덱스에 임포트해야 할 수 있습니다. Scout는 `scout:import` Artisan 명령어를 제공하며, 이를 통해 모든 기존 레코드를 검색 인덱스에 추가할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

색인에서 모델의 모든 레코드를 제거할 때는 `flush` 명령어를 사용하세요:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 수정

모델을 일괄 임포트할 때 사용하는 쿼리를 커스터마이징하려면, 모델에 `makeAllSearchableUsing` 메서드를 정의하면 됩니다. 여기에 관계 로딩 같은 사전 작업을 포함할 수 있습니다:

```
use Illuminate\Database\Eloquent\Builder;

/**
 * 모든 모델을 검색 가능하게 만들 때 사용하는 쿼리 수정
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 큐를 사용해 배치 임포트 시에는 `makeAllSearchableUsing`이 적용되지 않을 수 있습니다. 큐 작업 처리 중 모델 컬렉션의 관계는 복원되지 않습니다. ([큐 문서](/docs/11.x/queues#handling-relationships) 참고)

<a name="adding-records"></a>
### 레코드 추가 (Adding Records)

`Laravel\Scout\Searchable` 트레이트를 추가한 모델을 `save` 또는 `create` 하면 자동으로 검색 인덱스에 추가됩니다. 큐를 설정한 경우 동기화 작업이 백그라운드에서 실행됩니다:

```
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리 빌더에서 `searchable` 메서드를 호출하면 해당 쿼리 결과가 청크(chunk) 단위로 나누어져 검색 인덱스에 추가됩니다. 큐 설정이 되어있다면 백그라운드 작업으로 처리됩니다:

```
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

관계 모델 인스턴스에도 `searchable` 호출이 가능합니다:

```
$user->orders()->searchable();
```

이미 메모리에 있는 Eloquent 컬렉션이라면 해당 컬렉션에서 바로 `searchable` 메서드를 호출할 수도 있습니다:

```
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "업서트(upsert)" 연산으로 생각할 수 있습니다. 즉, 색인에 이미 존재하는 경우 업데이트하며, 없으면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

검색 가능 모델의 데이터를 변경할 때는 속성 변경 후 `save`하면 됩니다. Scout가 자동으로 검색 인덱스에 변경 사항을 반영합니다:

```
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 수정...

$order->save();
```

Eloquent 쿼리에서도 `searchable` 메서드를 호출해 여러 모델을 업데이트할 수 있습니다. 인덱스에 없던 모델은 새로 생성됩니다:

```
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스 또는 메모리 내 컬렉션에서도 `searchable`을 호출해 인덱스를 업데이트할 수 있습니다:

```
$user->orders()->searchable();

$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 임포트 전 레코드 수정

한꺼번에 모델 컬렉션을 색인 처리하기 전에 관계를 로드하는 등의 준비 작업이 필요할 수 있습니다. 이때는 모델에 `makeSearchableUsing` 메서드를 정의하세요:

```
use Illuminate\Database\Eloquent\Collection;

/**
 * 색인 처리할 모델 컬렉션을 수정합니다.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 제거 (Removing Records)

검색 인덱스에서 레코드를 삭제하려면 모델을 데이터베이스에서 `delete` 하면 됩니다. 소프트 삭제된 모델도 가능합니다:

```
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

삭제 전 모델을 조회하기 싫으면, Eloquent 쿼리에서 `unsearchable` 메서드 사용도 가능합니다:

```
Order::where('price', '>', 100)->unsearchable();
```

관계 또는 메모리 내 컬렉션에서 인덱스를 제거하려면 각각 다음처럼 호출하세요:

```
$user->orders()->unsearchable();

$orders->unsearchable();
```

모델의 모든 색인 데이터를 삭제하려면 `removeAllFromSearch` 메서드를 사용하세요:

```
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 색인 작업 일시 중지 (Pausing Indexing)

동기화 없이 다수의 모델 작업을 수행하려면 `withoutSyncingToSearch` 메서드를 사용하세요. 클로저 인수로 작업을 실행하면 해당 작업에선 색인 동기화가 일시 중지됩니다:

```
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 실행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능 모델 인스턴스 (Conditionally Searchable Model Instances)

특정 조건에서만 모델을 검색 가능하게 만들고 싶을 때, `shouldBeSearchable` 메서드를 정의할 수 있습니다. 예를 들어 `App\Models\Post`가 "draft"와 "published" 상태를 가지며, "published"일 때만 검색 가능하도록 하려면 다음과 같이 작성하세요:

```
/**
 * 모델이 검색 가능한지 결정합니다.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

이 메서드는 `save`, `create`, 쿼리, 관계를 통한 검색 가능한 상태 조작 시에만 적용됩니다. 컬렉션이나 모델에 직접 `searchable`을 호출하면 무시됩니다.

> [!WARNING]
> "database" 엔진 사용 시 `shouldBeSearchable`은 적용되지 않습니다. 데이터는 항상 DB에 저장됩니다. 이때는 [where 절](#where-clauses)을 활용해 비슷한 조건을 구현해야 합니다.

<a name="searching"></a>
## 검색 (Searching)

`search` 메서드로 검색을 시작할 수 있습니다. 문자열 인수 하나를 받아 해당 모델에서 검색합니다. 검색 결과는 Eloquent 모델 컬렉션이므로, `get`을 호출해 결과를 반환받으세요:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트나 컨트롤러에서 바로 반환하면 자동으로 JSON 변환됩니다:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

원본(raw) 검색 결과를 원하면 `raw` 메서드를 사용하세요:

```
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

기본 검색은 모델의 [`searchableAs`](#configuring-model-indexes)에서 반환한 인덱스를 사용합니다. 다른 인덱스를 검색하려면 `within` 메서드를 사용하세요:

```
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절 (Where Clauses)

Scout는 기본적 숫자 동등 비교 where 절을 검색 쿼리에 추가할 수 있습니다. 주로 소유자 ID 기반 제한에 유용합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn` 메서드를 통해 지정된 배열 안에 열 값이 포함되는지 검사할 수 있습니다:

```
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 해당 배열에 포함되지 않는지 검사합니다:

```
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 DB가 아니므로 더 복잡한 where 절은 지원하지 않습니다.

> [!WARNING]
> Meilisearch 사용 시에는 Scout의 where 절을 쓰려면 반드시 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 미리 정의해야 합니다.

<a name="pagination"></a>
### 페이징 (Pagination)

`paginate` 메서드로 검색 결과를 페이징할 수 있습니다. Eloquent 쿼리 페이징과 동일하게 `LengthAwarePaginator` 인스턴스를 반환합니다:

```
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

1페이지당 모델 수를 지정하려면 숫자를 인수로 전달하세요:

```
$orders = Order::search('Star Trek')->paginate(15);
```

Blade 템플릿에서 결과와 페이지 네비게이션 링크를 쉽게 출력 가능합니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

JSON으로 페이징 결과를 반환하려면 라우트나 컨트롤러에서 바로 반환하세요:

```
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 전역 스코프(global scopes)를 인지하지 못합니다. 따라서 Scout 페이징 사용 시, 전역 스코프를 적용하지 않거나 직접 Scout 쿼리 내에서 전역 스코프 조건을 수동으로 재현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

모델이 [소프트 삭제](/docs/11.x/eloquent#soft-deleting)를 지원하고 소프트 삭제된 데이터도 검색 대상에 포함하려면, `config/scout.php` 내 `soft_delete` 옵션을 `true`로 설정하세요:

```
'soft_delete' => true,
```

이 옵션이 `true`이면, Scout는 소프트 삭제된 모델을 검색 인덱스에서 제거하지 않고, 해당 레코드에 숨겨진 `__soft_deleted` 속성을 설정합니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 모델을 포함하거나 선택해서 검색할 수 있습니다:

```
use App\Models\Order;

// 소프트 삭제된 모델 포함 검색
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 모델만 검색
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델이 `forceDelete`로 영구 삭제되면, Scout가 이를 인덱스에서 자동 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

고급 검색 동작을 위해 `search` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어 Algolia 검색에 지리 위치 정보를 추가할 때 다음과 같이 사용할 수 있습니다:

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

Scout가 검색 엔진에서 일치하는 모델 ID 목록을 가져온 뒤, Eloquent가 해당 모델들을 쿼리하는 부분을 커스터마이징할 수 있습니다. `query` 메서드는 Eloquent 쿼리 빌더 인스턴스를 인수로 받는 클로저를 허용합니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 검색 엔진에서 모델 식별자가 조회된 후 실행되므로, 결과 필터링에는 사용하지 말고 [Scout의 where 절](#where-clauses)을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기

기본 제공 검색 엔진으로 원하는 기능 구현이 어렵다면 직접 커스텀 엔진을 작성할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 다음 8개의 추상 메서드를 구현해야 합니다:

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

`Laravel\Scout\Engines\AlgoliaEngine` 클래스의 구현을 참고하면 구현 방법을 이해하는 데 많은 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진 작성 후에는 Scout 엔진 매니저의 `extend` 메서드를 통해 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 해석할 수 있으며, 보통 `App\Providers\AppServiceProvider` 클래스나 다른 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```

그 후 `config/scout.php` 설정 파일에서 기본 드라이버로 새 엔진을 지정하면 됩니다:

```
'driver' => 'mysql',
```