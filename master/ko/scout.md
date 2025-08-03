# Laravel Scout (라라벨 스카우트)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉(Queueing)](#queueing)
- [드라이버 필요 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
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
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [where 조건절](#where-clauses)
    - [페이징](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Scout](https://github.com/laravel/scout)는 Eloquent 모델에 풀텍스트(full-text) 검색 기능을 쉽게 추가할 수 있는 드라이버 기반 솔루션입니다. 모델 옵저버를 사용하여 Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본 지원합니다. 추가로, 외부 의존성이나 제3자 서비스를 필요로 하지 않는 로컬 개발용 "collection" 드라이버도 포함되어 있습니다. 또한, 커스텀 드라이버를 쉽게 작성할 수 있어 원하는 검색 구현체로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 관리자를 이용해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

설치가 완료되면, Artisan의 `vendor:publish` 명령어를 사용하여 Scout 설정 파일을 애플리케이션의 `config` 디렉토리로 발행합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고 싶은 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여 모델 인스턴스 상태를 검색 드라이버와 자동으로 동기화합니다:

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
### 큐잉 (Queueing)

Scout 사용에 필수는 아니지만, 라이브러리 사용 전에 [큐 드라이버](/docs/master/queues)를 꼭 설정하는 것을 권장합니다. 큐 워커를 실행하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업이 큐에 쌓여 웹 인터페이스의 응답 속도를 높일 수 있습니다.

큐 드라이버 설정 후, `config/scout.php` 내 `queue` 옵션 값을 `true`로 설정하세요:

```php
'queue' => true,
```

`queue` 옵션이 `false`더라도 Algolia, Meilisearch 같은 일부 Scout 드라이버는 항상 비동기 방식으로 인덱싱합니다. 즉, Laravel 애플리케이션 내에서 인덱싱 작업이 완료됐어도 검색 엔진 내에 새로운 레코드가 바로 반영되지 않을 수 있습니다.

Scout 작업이 사용하는 연결 및 큐를 지정하려면, `queue` 옵션에 배열 형식으로 정의할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

연결과 큐를 커스터마이징 했다면, 반드시 해당 연결과 큐에서 작업을 처리할 큐 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 필요 조건 (Driver Prerequisites)

<a name="algolia"></a>
### Algolia

Algolia 드라이버 사용 시, `config/scout.php` 파일에서 Algolia `id`와 `secret` 자격 증명을 설정해야 합니다. 자격 증명 구성 후에는 Composer를 통해 Algolia PHP SDK를 설치하세요:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠른 오픈소스 검색 엔진입니다. 로컬 머신에 Meilisearch 설치 방법을 모른다면, Laravel 공식 도커 개발 환경인 [Laravel Sail](/docs/master/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버 사용 시, Composer를 통해 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

이후 애플리케이션 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch `host`, `key` 자격 정보를 설정하세요:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 더 자세한 내용은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한 Meilisearch 바이너리 버전에 맞는 `meilisearch/meilisearch-php` 버전을 설치하는지 [호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)에서 확인하는 것이 좋습니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때, Meilisearch 서비스 자체의 [추가 파괴적 변경사항](https://github.com/meilisearch/Meilisearch/releases)을 반드시 확인하세요.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 빠르고 오픈소스인 검색 엔진으로 키워드, 의미론적, 지리 정보, 벡터 검색을 지원합니다.

Typesense를 직접 호스팅하거나([자체 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)), [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Typesense와 Scout를 함께 시작하려면 Composer에서 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그리고 `.env` 파일에서 `SCOUT_DRIVER` 변수와 Typesense 호스트 및 API 키를 설정합니다:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

Laravel Sail을 사용하는 경우, `TYPESENSE_HOST` 환경 변수에 도커 컨테이너 이름을 맞게 지정해야 할 수 있습니다. 또한 포트, 경로, 프로토콜을 선택적으로 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

추가 설정과 Typesense 컬렉션 스키마 정의는 애플리케이션의 `config/scout.php`에서 확인할 수 있으며, 자세한 내용은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장용 데이터 준비

Typesense 사용 시, 모델은 `toSearchableArray` 메서드를 정의하여 기본 키를 문자열로 캐스팅하고 생성일을 UNIX 타임스탬프로 변환해야 합니다:

```php
/**
 * 인덱싱 가능한 데이터 배열 반환
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

Typesense 컬렉션 스키마는 `config/scout.php`에 정의하며, 검색 가능한 각 필드의 데이터 타입을 설명합니다. 자세한 스키마 옵션은 [Typesense API 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 변경해야 할 경우, `scout:flush`와 `scout:import` Artisan 명령어를 실행해서 기존 인덱스 데이터를 삭제하고 스키마를 재생성하거나, Typesense API로 스키마를 수정해 데이터 삭제 없이 업데이트할 수 있습니다.

만약 모델이 소프트 삭제를 사용한다면, `config/scout.php`의 Typesense 스키마에 `__soft_deleted` 필드를 추가해야 합니다:

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

Typesense는 `options` 메서드를 통해 검색 수행 시 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 수정할 수 있습니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 설정 (Configuration)

<a name="configuring-model-indexes"></a>
### 모델 인덱스 구성 (Configuring Model Indexes)

각 Eloquent 모델은 해당 모델의 모든 검색 가능 레코드를 포함하는 특정 검색 "인덱스"와 동기화됩니다. 즉, 인덱스는 MySQL 테이블과 비슷한 역할을 합니다. 기본적으로 모델은 모델 이름의 복수형인 "테이블" 이름과 동일한 인덱스에 저장됩니다. 그러나 모델에서 `searchableAs` 메서드를 오버라이드하여 인덱스 이름을 자유롭게 변경할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연결된 인덱스 이름 반환
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 가능 데이터 구성 (Configuring Searchable Data)

기본적으로 모델의 전체 `toArray` 결과가 검색 인덱스에 저장됩니다. 인덱싱되는 데이터를 사용자 정의하려면, 모델에서 `toSearchableArray` 메서드를 오버라이드하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 인덱스에 저장할 데이터 배열 반환
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

Meilisearch와 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 올바른 데이터 타입에 대해서만 수행하므로, 숫자 값은 올바른 타입으로 캐스팅해야 합니다:

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

때로는 Algolia 인덱스에 추가 설정이 필요할 수 있습니다. Algolia UI에서 직접 관리가 가능하지만, 애플리케이션의 자동 배포 파이프라인을 통해 설정을 관리하려면 `config/scout.php` 파일에서 인덱스별 설정을 구성하는 것이 효율적입니다.

필터 가능 속성, 랭킹, 페이싱 등 [지원되는 모든 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

`config/scout.php` 파일에 각 인덱스의 설정을 추가하는 예시는 다음과 같습니다:

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

소프트 삭제가 적용된 모델이 포함된 인덱스의 경우, Scout는 자동으로 소프트 삭제 데이터에 대한 페이싱을 지원합니다. 다른 페이싱 속성이 없는 경우, 빈 배열로 정의할 수 있습니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 변경 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해 Algolia에 현재 설정을 알립니다. 배포 과정에 포함시키는 것도 좋습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정 구성 (Meilisearch)

다른 Scout 드라이버와 달리, Meilisearch는 필터 가능 속성, 정렬 가능 속성 등 [인덱스 검색 설정](https://docs.meilisearch.com/reference/api/settings.html)을 사전에 정의해야 합니다.

`where` 메서드로 필터링할 수 있는 속성은 필터 가능 속성, `orderBy`로 정렬할 속성은 정렬 가능 속성으로 지정합니다. `config/scout.php`에서 `meilisearch` 항목 내 `index-settings`를 조정하세요:

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

소프트 삭제가 적용된 모델이 포함되면 Scout가 소프트 삭제 모델 필터링을 자동 지원합니다. 다른 필터 또는 정렬 속성이 없는 소프트 삭제 모델 인덱스는 빈 배열로도 설정 가능합니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정 변경 후 `scout:sync-index-settings` 명령어를 실행해 Meilisearch에 현재 설정을 알려야 하며, 이 명령은 배포 프로세스에 포함할 수 있습니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 구성 (Configuring the Model ID)

기본적으로 Scout는 모델의 기본 키를 검색 인덱스에 저장하는 고유 식별자로 사용합니다. 이 동작을 바꾸고 싶다면, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드 하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용할 고유 값 반환
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱 키 이름 반환
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 구성 (Configuring Search Engines per Model)

검색 시 기본적으로 애플리케이션의 `scout` 설정 파일에 지정한 기본 검색 엔진을 사용합니다. 특정 모델에 대해 다른 검색 엔진을 사용하려면, 모델에서 `searchableUsing` 메서드를 오버라이드 해서 원하는 엔진을 반환하면 됩니다:

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
     * 이 모델에 사용할 검색 엔진 반환
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별 (Identifying Users)

Scout는 [Algolia](https://algolia.com) 사용 시 인증된 사용자를 자동으로 식별할 수 있도록 지원합니다. Algolia 대시보드에서 사용자별 검색 분석을 볼 때 유용합니다. `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정해 활성화할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 사용하면 요청 IP 주소와 인증된 사용자 기본 식별자가 Algolia에 전달되어, 사용자별 검색 요청이 연동됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진 (Database / Collection Engines)

<a name="database-engine"></a>
### 데이터베이스 엔진 (Database Engine)

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

규모가 작거나 중간 정도이고 작업량이 적은 애플리케이션에서는 Scout의 "database" 엔진 사용이 편리할 수 있습니다. 이 엔진은 데이터베이스의 "where like" 조건과 풀텍스트 인덱스를 활용해 검색 결과를 필터링합니다.

`SCOUT_DRIVER` 환경 변수를 `database`로 설정하거나, `config/scout.php`에서 직접 드라이버를 `database`로 지정해 사용하세요:

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 선택했다면, [검색 가능 데이터](#configuring-searchable-data)를 설정하고 [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense 같은 추가 인덱싱 작업은 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 모델의 모든 검색 가능 속성에 "where like" 쿼리를 실행합니다. 하지만 경우에 따라 성능 이슈가 있을 수 있기에, 일부 컬럼에 대해 풀텍스트 검색 또는 문자열 접두어 검색으로 전략을 달리 지정할 수 있습니다.

`toSearchableArray` 메서드에 PHP 어트리뷰트를 지정하여 컬럼별 검색 전략을 선언합니다. 별도 지정하지 않은 컬럼은 기본 "where like" 전략을 따릅니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 인덱싱 가능한 데이터 배열 반환
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
> 풀텍스트 검색 제약 조건을 지정하기 전에 반드시 해당 컬럼에 [풀텍스트 인덱스](/docs/master/migrations#available-index-types)를 설정했는지 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진 (Collection Engine)

로컬 개발 시 Algolia, Meilisearch, Typesense 대신 Scout의 "collection" 엔진을 사용하는 것이 편리할 수 있습니다. 컬렉션 엔진은 데이터베이스에서 조건절로 결과를 필터링하며, 별도 인덱싱 작업 없이 바로 데이터를 조회합니다.

`SCOUT_DRIVER` 환경 변수를 `collection`으로 설정하거나 `config/scout.php`에서 드라이버를 `collection`으로 지정하면 됩니다:

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 설정한 후에는 바로 [검색 쿼리](#searching)를 실행할 수 있으며, 추가 인덱싱 작업은 필요 없습니다.

#### 데이터베이스 엔진과의 차이점

두 엔진은 모두 데이터베이스에서 직접 결과를 조회하지만, 컬렉션 엔진은 풀텍스트 인덱스나 `LIKE` 조건을 활용하지 않고, 가능한 모든 레코드를 가져와 Laravel의 `Str::is` 헬퍼로 검색어가 포함되었는지 판별합니다.

컬렉션 엔진은 SQLite, SQL Server를 포함한 Laravel 지원 모든 관계형 데이터베이스에서 작동해 가장 이식성이 좋지만, 성능은 데이터베이스 엔진보다 떨어집니다.

<a name="indexing"></a>
## 인덱싱 (Indexing)

<a name="batch-import"></a>
### 일괄 가져오기 (Batch Import)

기존 프로젝트에서 Scout를 도입할 때 이미 저장된 데이터가 있을 수 있습니다. 이런 경우 `scout:import` Artisan 명령어로 모델의 모든 기존 레코드를 인덱스에 일괄 등록할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

`flush` 명령어로는 해당 모델의 인덱스 내 모든 레코드를 삭제할 수 있습니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정

일괄 인덱싱 때 불러오는 쿼리를 변경하려면 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 지연 로딩할 관계를 이곳에서 추가하는 것이 좋습니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모든 모델을 검색 가능하게 만들 때 사용되는 쿼리 수정
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 큐를 사용해 일괄 인덱싱할 경우, 작업 처리 중 모델 컬렉션의 관계는 [복원되지 않습니다](/docs/master/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가 (Adding Records)

모델에 `Searchable` 트레이트를 추가하면, `save` 또는 `create` 할 때마다 해당 레코드가 자동으로 검색 인덱스에 추가됩니다. 큐를 사용하는 설정이라면 백그라운드에서 큐 워커가 처리합니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가

쿼리 결과 컬렉션을 인덱스에 추가하고 싶으면 Eloquent 쿼리에 `searchable` 메서드를 체이닝하세요. 내부적으로 [청킹(chunking)](/docs/master/eloquent#chunking-results) 하여 인덱스에 추가합니다. 큐가 활성화돼 있으면 각 청크가 비동기로 처리됩니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계에도 같은 메서드를 사용할 수 있습니다:

```php
$user->orders()->searchable();
```

이미 메모리에 로드한 컬렉션이 있다면 컬렉션 인스턴스에서 `searchable` 메서드를 호출해 일괄 추가도 가능합니다:

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "업서트(upsert)" 작업으로, 레코드가 인덱스에 있으면 업데이트, 없으면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트 (Updating Records)

검색 가능 모델을 업데이트하려면 모델 속성을 변경 후 `save`만 수행하면 됩니다. Scout가 자동으로 인덱스 동기화를 처리합니다:

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 업데이트...

$order->save();
```

복수의 모델을 업데이트하고 싶으면 Eloquent 쿼리에서 `searchable` 메서드를 호출하면 됩니다. 인덱스에 없는 모델은 새로 생성됩니다:

```php
Order::where('price', '>', 100)->searchable();
```

관계에 포함된 모델 일괄 업데이트도 가능합니다:

```php
$user->orders()->searchable();
```

메모리에 로드한 모델 컬렉션도 마찬가지로 `searchable` 호출로 업데이트할 수 있습니다:

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 수정

관계 데이터를 미리 로드해 인덱스에 효율적으로 포함시키고 싶을 때, 모델에 `makeSearchableUsing` 메서드를 정의할 수 있습니다. 이 메서드는 인덱싱할 모델 컬렉션을 수정해 반환합니다:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능하게 만들려는 모델 컬렉션 수정
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 제거 (Removing Records)

인덱스에서 레코드를 제거하려면 간단하게 데이터베이스에서 모델을 삭제하세요. 소프트 삭제 모델도 지원합니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 조회하지 않고 제거하려면 Eloquent 쿼리에 `unsearchable` 메서드를 사용하세요:

```php
Order::where('price', '>', 100)->unsearchable();
```

관계에 포함된 모델 전부 인덱스에서 제거도 가능합니다:

```php
$user->orders()->unsearchable();
```

이미 메모리에 로드된 모델 컬렉션에서도 `unsearchable` 호출로 제거할 수 있습니다:

```php
$orders->unsearchable();
```

모델의 모든 인덱스 레코드를 제거하려면 다음 메서드를 실행하세요:

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지 (Pausing Indexing)

특정 작업 동안 인덱스 동기화를 멈추려면, `withoutSyncingToSearch` 메서드에 클로저를 전달하여 실행할 수 있습니다. 클로저 내부에서 모델에 대한 동기화가 발생하지 않습니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스 지정 (Conditionally Searchable Model Instances)

특정 조건에서만 모델을 검색 가능하게 만들고 싶을 때 `shouldBeSearchable` 메서드를 정의하세요. 예를 들어 `App\Models\Post` 모델에서 'published' 상태일 때만 검색 가능하도록 할 수 있습니다:

```php
/**
 * 모델이 검색 가능해야 하는지 판단
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

이 메서드는 `save`, `create`, 쿼리, 관계를 통한 모델 조작 시에만 적용됩니다. 직접 `searchable` 메서드를 호출하는 경우 무시됩니다.

> [!WARNING]
> 데이터베이스 엔진에서는 모든 데이터가 항상 DB에 저장되므로, `shouldBeSearchable` 메서드는 무시됩니다. 데이터베이스 엔진 사용 시 비슷한 동작이 필요하다면 [where 조건절](#where-clauses)을 활용하세요.

<a name="searching"></a>
## 검색 (Searching)

모델에서 `search` 메서드를 호출하며 검색을 시작할 수 있습니다. 한 개의 문자열을 전달하면 해당 검색어로 모델을 조회합니다. 그 후, `get` 메서드를 체이닝해 Eloquent 모델 컬렉션을 받으세요:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout의 검색 결과는 Eloquent 모델 컬렉션이므로, 라우트나 컨트롤러에서 직접 JSON으로 반환해도 자동 변환됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

원시 검색 결과를 얻으려면 `raw` 메서드를 사용하세요:

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 사용자 정의 인덱스

검색 쿼리는 기본적으로 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 반환한 인덱스를 사용합니다. 하지만 `within` 메서드로 임의 인덱스를 지정할 수 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### where 조건절

Scout는 간단한 where 조건을 검색 쿼리에 추가하는 것을 지원합니다. 현재는 기본 숫자 동등성 비교만 지원하며, 주로 소유자 ID로 검색 범위를 좁힐 때 유용합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한 `whereIn` 메서드로 특정 컬럼 값이 배열에 포함되는지 확인할 수 있습니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 컬럼 값이 배열에 포함되지 않는지 확인할 때 사용합니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니므로, 더 복잡한 where 조건은 현재 지원하지 않습니다.

> [!WARNING]
> Meilisearch 사용 시, [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 미리 구성해야 Scout의 where 조건을 올바르게 사용할 수 있습니다.

<a name="pagination"></a>
### 페이징 (Pagination)

모델 컬렉션 대신 페이징된 결과를 받고 싶으면 `paginate` 메서드를 사용하세요. 이 메서드는 일반 Eloquent 쿼리를 페이징할 때와 동일한 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 결과수를 지정하려면 `paginate` 메서드에 숫자를 넘겨주세요:

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 화면에 표시하고 페이지 링크를 렌더링할 때는 [Blade](/docs/master/blade)를 아래처럼 사용하면 됩니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

또한, JSON 형태로 페이징 결과를 직접 반환할 수도 있습니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프를 인지하지 못하므로, Scout 페이징을 사용할 때는 글로벌 스코프 사용을 피하거나 스코프 제약 조건을 Scout 검색에 맞게 다시 적용하세요.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

인덱싱된 모델이 [소프트 삭제](/docs/master/eloquent#soft-deleting)를 사용하고 그 데이터도 검색 대상에 포함하고 싶으면, `config/scout.php` 설정에서 `soft_delete` 옵션을 `true`로 설정하세요:

```php
'soft_delete' => true,
```

이 옵션 활성화 시 Scout는 소프트 삭제된 모델을 인덱스에서 삭제하지 않고 `__soft_deleted`라는 숨김 속성으로 표시합니다. 그리고 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 결과를 검색할 수 있습니다:

```php
use App\Models\Order;

// 소프트 삭제된 모델 포함 검색
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 모델만 검색
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 완전 삭제하면 Scout가 인덱스에서 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징 (Customizing Engine Searches)

고급 검색 커스터마이징이 필요하면 `search` 메서드 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어 Algolia 검색 옵션에 지리정보를 추가할 수 있습니다:

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

Scout가 검색 엔진에서 일치하는 모델 ID 목록을 받은 뒤, Eloquent의 기본 키로 실제 모델을 조회하는데, 이 쿼리를 커스터마이징하려면 `query` 메서드를 사용할 수 있습니다. 클로저로 Eloquent 쿼리 빌더 인스턴스를 받습니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이미 검색 엔진에서 결과가 확정된 뒤 동작하므로, 필터링 용도로는 사용하지 말고 Scout의 [where 조건절](#where-clauses)을 활용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진 (Custom Engines)

<a name="writing-the-engine"></a>
#### 엔진 작성하기

내장된 검색 엔진이 요구에 맞지 않는다면 커스텀 엔진을 작성하여 Scout에 등록할 수 있습니다. 커스텀 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 아래 8개 메서드를 반드시 구현해야 합니다:

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

구현 예제와 참고용으로는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 검토하면 좋은 출발점이 될 것입니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진 작성 후, Scout의 엔진 매니저 `extend` 메서드를 사용해 등록합니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 해석할 수 있으며, 보통 `App\Providers\AppServiceProvider` 등 앱 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

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

등록이 완료되면, `config/scout.php` 파일에서 기본 Scout 드라이버로 지정해서 사용하세요:

```php
'driver' => 'mysql',
```