# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐(Queue) 사용](#queueing)
- [드라이버 사전 준비](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [구성](#configuration)
    - [모델 인덱스 구성](#configuring-model-indexes)
    - [검색 가능한 데이터 구성](#configuring-searchable-data)
    - [모델 ID 구성](#configuring-the-model-id)
    - [모델별 검색 엔진 구성](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [색인(Indexing)](#indexing)
    - [일괄 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시중지](#pausing-indexing)
    - [조건부로 검색 가능한 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절 사용](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [사용자 정의 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 전체 텍스트 검색(Full-Text Search)을 쉽게 추가할 수 있도록 드라이버 기반 해결책을 제공합니다. Scout는 모델 옵저버를 사용하여, Eloquent 레코드가 변경될 때마다 자동으로 검색 인덱스와 동기화하도록 지원합니다.

Scout는 기본적으로 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 제공합니다. 또한, 외부 의존성이나 서드파티 서비스 없이 로컬 개발 시 사용할 수 있는 "collection" 드라이버도 포함하고 있습니다. 직접 사용자 정의 드라이버도 간단하게 작성할 수 있으므로 원하는 검색 방식을 자유롭게 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 통해 Scout를 설치하세요.

```shell
composer require laravel/scout
```

설치 후, `vendor:publish` Artisan 명령어를 실행하여 Scout의 설정 파일을 발행해야 합니다. 이 명령어는 애플리케이션의 `config` 디렉터리에 `scout.php` 설정 파일을 추가합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 대상으로 만들고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트를 추가하면 모델을 자동으로 감지하고, 드라이버와 동기화할 옵저버가 등록됩니다.

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
### 큐(Queue) 사용

`database` 또는 `collection` 엔진이 아닌 다른 엔진을 사용할 경우, Scout를 쓰기 전에 반드시 [큐 드라이버](/docs/12.x/queues)를 먼저 설정할 것을 권장합니다. 큐 워커(queue worker)를 실행하면 모델 정보를 검색 인덱스에 동기화하는 작업이 큐에 적재되어 웹 인터페이스의 응답 속도가 훨씬 빨라집니다.

큐 드라이버를 설정한 후, `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 지정하세요.

```php
'queue' => true,
```

`queue` 옵션이 `false`로 설정되어 있더라도, Algolia와 Meilisearch와 같은 일부 Scout 드라이버는 항상 비동기적으로 레코드를 인덱싱합니다. 즉, Laravel 애플리케이션에서 인덱싱 작업이 완료된 것처럼 보여도, 실제 검색 엔진에는 새로운 또는 변경된 레코드가 바로 반영되지 않을 수 있습니다.

Scout 작업이 사용할 connection과 queue를 직접 지정하려면 `queue` 설정을 배열로 지정할 수도 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

이처럼 connection과 queue를 별도로 지정했다면, 해당 커넥션과 queue에서 작업을 처리하도록 queue 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는, `config/scout.php` 설정 파일에서 Algolia의 `id`와 `secret` 자격증명 정보를 입력해야 합니다. 자격증명 설정이 끝났으면, Composer 패키지 매니저로 Algolia PHP SDK도 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스 기반의 검색 엔진입니다. 로컬에 Meilisearch를 설치하는 방법을 잘 모를 경우에는 Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail#meilisearch) 사용을 권장합니다.

Meilisearch 드라이버를 쓸 때는 Composer 패키지 매니저로 Meilisearch PHP SDK를 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고 `.env` 파일에서 `SCOUT_DRIVER` 환경 변수와 더불어 Meilisearch의 `host`, `key` 자격증명 정보도 설정해야 합니다.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 더 자세한 정보는 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, 사용 중인 Meilisearch 바이너리 버전에 호환되는 `meilisearch/meilisearch-php` 패키지 버전을 설치해야 하니, [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 반드시 확인하세요.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout 버전을 업그레이드할 때는, 반드시 [Meilisearch 서비스의 추가적인 변경사항 및 호환성 이슈](https://github.com/meilisearch/Meilisearch/releases)를 별도로 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 빠르고 오픈소스인 검색 엔진으로, 키워드 검색, 시맨틱(의미 기반) 검색, 지오(위치 기반) 검색, 벡터 검색 등을 지원합니다.

[Typesense를 직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수도 있습니다.

Scout에서 Typesense를 사용하려면 Composer 패키지 매니저로 Typesense PHP SDK를 설치하세요.

```shell
composer require typesense/typesense-php
```

그리고 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 더불어 Typesense의 host 및 API key 자격 증명을 추가하세요.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용할 경우, Docker 컨테이너 이름에 맞게 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수 있습니다. 또한 설치 환경의 port, path, protocol을 옵션으로 지정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션에 대한 추가 설정 및 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 할 수 있습니다. Typesense에 대한 더 자세한 정보는 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense를 사용할 때는, 모델의 기본 키를 문자열로, 생성일자를 UNIX 타임스탬프로 캐스팅하여 `toSearchableArray` 메서드를 정의해야 합니다.

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

Typesense 컬렉션의 스키마는 애플리케이션의 `config/scout.php` 파일에서 정의해야 합니다. 컬렉션 스키마는 Typesense를 통해 검색 가능하게 만들 필드의 데이터 타입을 명시합니다.
모든 스키마 옵션에 대한 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

이미 컬렉션의 스키마를 정의한 이후에 스키마를 변경해야 한다면, `scout:flush` 및 `scout:import` 명령어를 실행하여 기존 인덱스 데이터를 삭제하고 스키마를 재생성할 수 있습니다. 또는 Typesense의 API를 사용하여 인덱싱된 데이터를 삭제하지 않고 컬렉션의 스키마만 수정할 수도 있습니다.

만약 검색 가능한 모델에서 소프트 삭제를 지원한다면, 해당 모델의 Typesense 스키마 내에 `__soft_deleted` 필드를 다음과 같이 정의해야 합니다.

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
#### 동적으로 검색 파라미터 지정

Typesense는 `options` 메서드를 통해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 지정하면서 검색 작업을 실행할 수 있습니다.

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 구성

<a name="configuring-model-indexes"></a>
### 모델 인덱스 구성

각 Eloquent 모델은 그 모델의 모든 검색 가능한 레코드를 담은 특정 검색 "인덱스"와 동기화됩니다. 쉽게 설명하면, 각 인덱스는 마치 MySQL의 테이블처럼 동작합니다. 기본적으로 각 모델은 해당 모델의 표준 "테이블"명과 일치하는 인덱스에 저장됩니다. 일반적으로 모델의 복수형 이름이 인덱스명이 됩니다. 필요에 따라 모델의 `searchableAs` 메서드를 오버라이드하여 인덱스 이름을 커스터마이징할 수 있습니다.

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
### 검색 가능한 데이터 구성

기본적으로, 모델의 전체 `toArray` 결과가 검색 인덱스에 저장됩니다. 인덱스에 동기화할 데이터를 원하는 형태로 직접 지정하려면, 모델에서 `toSearchableArray` 메서드를 오버라이드하면 됩니다.

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

        // 데이터 배열 커스터마이즈...

        return $array;
    }
}
```

Meilisearch 등 일부 검색 엔진에서는 `>`, `<` 등의 필터 연산을 사용할 때 데이터의 타입이 정확히 맞아야 합니다. 이런 경우, 숫자 값은 반드시 올바른 타입으로 캐스팅하여 반환하세요.

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

경우에 따라 Algolia 인덱스에 추가 설정을 적용하고 싶을 수 있습니다. Algolia UI를 통해서도 설정할 수 있지만, 애플리케이션의 `config/scout.php` 파일에서 직접 인덱스 설정 상태를 관리하는 것이 더 편리할 때도 있습니다.

이 방법은 자동화된 배포 파이프라인을 통해 여러 환경에서 인덱스 설정을 일관성 있게 관리할 수 있도록 도와줍니다. 필터 가능한 속성, 정렬, 팩싱(faceting), 또는 [기타 Algolia 지원 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 정의할 수 있습니다.

애플리케이션의 `config/scout.php` 파일에서 각 인덱스별 설정을 추가하세요.

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

소프트 삭제를 지원하는 모델이 `index-settings`에 포함된 경우, 해당 인덱스에서 소프트 삭제 모델의 팩싱도 자동으로 처리됩니다. 소프트 삭제 모델의 팩싱 속성을 추가할 필요가 없다면, 인덱스 설정에 빈 항목만 추가하면 됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정이 끝나면, `scout:sync-index-settings` Artisan 명령어를 실행해야 현재 설정 내용을 Algolia에 반영할 수 있습니다. 이 명령어를 배포(Deploy) 과정의 일부로 자동화하는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터/정렬 가능한 데이터 및 인덱스 설정 구성 (Meilisearch)

Meilisearch는 Scout의 다른 드라이버들과 달리, 검색 인덱스의 필터/정렬 가능한 속성 및 [다른 설정 필드들](https://docs.meilisearch.com/reference/api/settings.html)을 사전에 정의해야 합니다.

필터 가능한 속성은 Scout의 `where` 메서드로 필터링할 속성이며, 정렬 가능한 속성은 `orderBy` 메서드로 정렬할 속성입니다.
이 설정은 애플리케이션의 `scout` 설정 파일에서 `meilisearch` 배열의 `index-settings` 부분에 지정할 수 있습니다.

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

소프트 삭제 모델이 `index-settings`에 포함된 경우, 해당 인덱스에서 소프트 삭제 모델을 필터링할 수 있습니다. 소프트 삭제 모델에 대해 별도의 필터/정렬 속성이 필요 없다면, 빈 항목만 추가해도 무방합니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 마쳤으면, `scout:sync-index-settings` Artisan 명령어를 실행해야 Meilisearch에 적용됩니다. 이 명령어도 배포 과정의 일부로 자동화하는 것을 권장합니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 구성

기본적으로 Scout는 모델의 기본 키(primary key)를 검색 인덱스에 저장할 때 고유 ID/키로 사용합니다. 동작을 커스터마이징하려면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드하면 됩니다.

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
### 모델별 검색 엔진 구성

Scout는 일반적으로 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 하지만 모델별로 검색 엔진을 바꾸고 싶다면, 모델에서 `searchableUsing` 메서드를 오버라이드할 수 있습니다.

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
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 엔진을 사용할 때, 인증된 사용자를 자동으로 식별할 수도 있습니다. 이 기능은 Algolia 대시보드에서 검색 분석 정보를 사용자와 연결해서 확인할 때 유용합니다. 사용자 식별을 활성화하려면, 애플리케이션의 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하세요.

```ini
SCOUT_IDENTIFY=true
```

이 옵션을 활성화할 경우, 요청자의 IP 주소와 인증 사용자의 기본 식별 정보가 Algolia로 전달되어, 사용자의 검색 요청에 데이터가 연결됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

`database` 엔진은 Laravel Scout를 가장 간단하게 시작할 수 있는 방식입니다. 현재 사용 중인 데이터베이스에서 MySQL/PostgreSQL의 Full-Text 인덱스와 "where like" 절을 활용해 쿼리 결과 중 검색에 해당하는 값을 필터링합니다.

데이터베이스 엔진을 사용하려면, `.env` 파일에서 `SCOUT_DRIVER` 값에 `database`를 할당하거나, 애플리케이션의 `scout` 설정 파일에서 `database` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 설정했다면, 먼저 [검색 가능한 데이터 구성](#configuring-searchable-data)을 진행해야 합니다. 그런 다음, [검색 쿼리 실행](#searching)을 시작할 수 있습니다. Algolia, Meilisearch, Typesense 등에서 필요한 별도의 색인 시드 작업은 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로, 데이터베이스 엔진은 [검색 가능한 데이터로 지정된](#configuring-searchable-data) 모든 모델 속성에 "where like" 쿼리를 실행합니다. 하지만 상황에 따라 성능 저하가 발생할 수 있기 때문에, 일부 컬럼만 Full-Text 또는 접두사(Prefix) 문자열 검색(`example%`) 등으로 전략을 분리해 쿼리를 실행할 수 있습니다.

이를 위해 PHP 어트리뷰트를 모델의 `toSearchableArray` 메서드에 지정합니다. 추가 검색 전략이 지정되지 않은 컬럼은 기본 "where like" 전략을 계속 사용합니다.

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
> 컬럼에 Full-Text 쿼리를 사용하도록 지정하기 전에, 해당 컬럼에 [Full-Text 인덱스](/docs/12.x/migrations#available-index-types)가 생성되어 있는지 반드시 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서도 Algolia, Meilisearch, Typesense 등 검색 엔진을 쓸 수 있지만, 더 간편하게 "collection" 엔진을 사용해 볼 수도 있습니다. 컬렉션 엔진은 데이터베이스에 저장된 결과를 "where" 절과 컬렉션 필터링으로 적용하여 쿼리 결과를 도출합니다. 이 방식은 검색 모델을 따로 "인덱싱"할 필요 없이, 로컬 데이터베이스에 저장된 내용을 그대로 사용합니다.

컬렉션 엔진을 사용하려면, `.env` 파일에서 `SCOUT_DRIVER` 값을 `collection`으로 설정하거나, `scout` 설정 파일에서 `collection` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=collection
```

설정이 끝나면 [검색 쿼리 실행](#searching)을 바로 시작할 수 있습니다. 이 엔진은 별도의 인덱싱 과정이 필요 없습니다.

#### 데이터베이스 엔진과의 차이점

"database" 엔진과 "collections" 엔진은 모두 데이터베이스에서 직접 결과를 가져오므로 유사한 것처럼 보입니다. 하지만 collection 엔진은 Full-Text 인덱스나 `LIKE` 절을 사용하지 않고, 모든 후보 레코드를 가져와 `Str::is` 헬퍼를 사용하여 모델 속성 값에 검색어가 포함되어 있는지 판별합니다.

collection 엔진은 SQLite, SQL Server 등 Laravel이 지원하는 모든 관계형 데이터베이스에서 사용할 수 있을 만큼 이식성이 높지만, Scout의 database 엔진에 비해 효율성은 떨어집니다.

<a name="indexing"></a>
## 색인(Indexing)

<a name="batch-import"></a>
### 일괄 가져오기

기존 프로젝트에 Scout를 도입할 때는 이미 데이터베이스에 저장된 레코드가 인덱스에도 반영되어야 할 수 있습니다. Scout는 모든 기존 레코드를 검색 인덱스에 추가하는 `scout:import` Artisan 명령어를 제공합니다.

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` 명령어를 사용하면, [큐 작업](/docs/12.x/queues)으로 기존 레코드를 배치(청크) 단위로 백그라운드에서 인덱스에 추가할 수 있습니다.

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` 명령어를 사용하면 지정 모델의 모든 레코드를 인덱스에서 제거할 수 있습니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 일괄 가져오기 쿼리 수정

일괄 인덱싱 시 불러올 모델 쿼리를 직접 수정하려면, 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 이곳에서 관계 로드(Eager Loading) 등 필요한 쿼리 커스터마이징이 가능합니다.

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
> 큐를 통한 일괄 인덱싱에서는 `makeAllSearchableUsing` 메서드가 동작하지 않을 수 있습니다. 큐 작업에서 모델 컬렉션이 처리될 때는 [관계 데이터가 복원되지 않습니다](/docs/12.x/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

모델에 `Laravel\Scout\Searchable` 트레이트를 추가했다면, 이제 단순히 `save` 또는 `create` 메서드만 호출해도 자동으로 검색 인덱스에 반영됩니다. 큐를 쓴다면 이 작업은 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### Eloquent 쿼리를 통한 레코드 추가

Eloquent 쿼리에 `searchable` 메서드를 체이닝하면 쿼리 결과 컬렉션 전체를 검색 인덱스에 추가할 수 있습니다. Scout의 큐 기능을 쓰면, 쿼리 결과도 자동으로 백그라운드에서 차례로 인덱싱됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계에서도 `searchable` 메서드를 사용할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션이 메모리에 있다면, 해당 컬렉션 인스턴스에 대해 `searchable`을 호출해도 동작합니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert"(존재한다면 업데이트, 없으면 추가) 동작을 합니다. 이미 인덱스에 존재하는 레코드는 업데이트되며, 없는 레코드는 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 원하는 모델 인스턴스의 속성을 변경한 다음 `save`를 호출하세요. Scout는 자동으로 변경 내용을 검색 인덱스에도 반영합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 정보를 수정...

$order->save();
```

`searchable` 메서드를 Eloquent 쿼리 인스턴스에 호출하면 컬렉션 전체를 쉽게 업데이트할 수 있습니다. 만약 인덱스에 모델이 없다면 새로 추가됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

관계 전체에 대해 인덱스를 업데이트하려면 관계 인스턴스에 `searchable`을 호출하세요.

```php
$user->orders()->searchable();
```

이미 메모리에 모델 컬렉션이 있다면, 해당 컬렉션 인스턴스에 대해 `searchable`을 호출할 수 있습니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전에 레코드 수정하기

일괄 인덱싱 전에 모델 컬렉션을 미리 수정해야 할 때가 있습니다. 예를 들어, 관계 데이터를 미리 로드(eager loading)해서 인덱스에 포함하고 싶을 수 있습니다. 이럴 때는 해당 모델에 `makeSearchableUsing` 메서드를 정의하세요.

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

<a name="conditionally-updating-the-search-index"></a>
#### 조건부로 인덱스 업데이트하기

기본적으로 Scout는 어떤 속성이든 수정되면 무조건 모델을 다시 인덱싱합니다. 속성에 따라 인덱싱 여부를 세밀하게 제어하고 싶다면, 모델에 `searchIndexShouldBeUpdated` 메서드를 정의하세요.

```php
/**
 * Determine if the search index should be updated.
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```

<a name="removing-records"></a>
### 레코드 제거

인덱스에서 레코드를 삭제하려면, 단순히 데이터베이스에서 해당 모델을 `delete`하면 됩니다. (소프트 삭제 모델도 동일하게 동작)

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 미리 조회해서 삭제하지 않고 바로 제거하려면, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용하세요.

```php
Order::where('price', '>', 100)->unsearchable();
```

관계 전체에 대해 인덱스를 제거하려면, 관계 인스턴스에 `unsearchable`을 호출하세요.

```php
$user->orders()->unsearchable();
```

이미 Eloquent 모델 컬렉션을 메모리에 가지고 있다면, 컬렉션 인스턴스에 대해 `unsearchable` 메서드를 호출할 수 있습니다.

```php
$orders->unsearchable();
```

모델의 모든 레코드를 색인에서 한 번에 제거하려면 `removeAllFromSearch` 메서드를 사용하세요.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시중지

특정 모델에서 Eloquent 작업을 여러 번 실행하면서, 해당 트랜잭션 동안만 인덱스 동기화를 끊고 싶을 때가 있습니다. 이럴 때는 `withoutSyncingToSearch` 메서드를 사용하세요. 이 메서드는 즉시 실행되는 클로저를 인자로 받아, 해당 클로저 내부의 모든 모델 작업을 인덱스에 적용하지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

상황에 따라 특정 조건을 만족할 때만 모델을 검색 대상으로 삼고 싶을 수 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft", "published" 상태를 가질 수 있고, 오직 "published" 상태인 포스트만 검색 가능하게 만들려면 아래처럼 모델에 `shouldBeSearchable` 메서드를 정의하세요.

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

이 메서드는 `save`, `create`, 쿼리 또는 관계를 통해 모델을 조작할 때만 적용됩니다. 컬렉션이나 모델을 직접 `searchable`로 만드는 경우, 해당 로직이 무시되고 강제로 인덱싱됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진을 사용할 때는 적용되지 않습니다. 데이터베이스 엔진은 모든 검색 가능한 데이터를 데이터베이스에 항상 저장하기 때문입니다. "database" 엔진에서는 대신 [where 절](#where-clauses)을 사용해 비슷한 기능을 구현하세요.

<a name="searching"></a>
## 검색

모델에서 `search` 메서드를 사용해 검색을 시작할 수 있습니다. 검색어로 사용할 문자열 하나를 인수로 받아, 이후 `get` 메서드를 체이닝해 해당 검색 쿼리에 일치하는 Eloquent 모델을 가져올 수 있습니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout에서 반환되는 결과는 Eloquent 모델 컬렉션이므로, 컨트롤러나 라우트에서 바로 반환하면 자동으로 JSON 형태로 변환됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

변환되지 않은, 검색 엔진의 원본 결과를 얻고 싶다면 `raw` 메서드를 사용합니다.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 사용

일반적으로 검색 쿼리는 모델의 [searchableAs](#configuring-model-indexes) 메서드에서 지정한 인덱스를 대상으로 수행됩니다. 하지만, 특정 인덱스에서 검색하려면 `within` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절 사용

Scout는 기본적인 숫자 등호 조건만 지원하는 간단한 "where" 절을 추가할 수 있습니다. 주로 사용자 ID 등으로 검색 범위를 제한하는 데에 사용됩니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한, 컬럼의 값이 주어진 배열에 포함되는지 검사하려면 `whereIn` 메서드를 사용합니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

컬럼의 값이 주어진 배열에 포함되지 않을 때만 결과를 가져오려면 `whereNotIn`을 사용합니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 엔진의 인덱스는 관계형 데이터베이스가 아니기 때문에, 더 복잡한 "where" 조건은 현재 지원하지 않습니다.

> [!WARNING]
> Meilisearch를 사용하는 경우, Scout의 "where" 절을 사용하기 전에 반드시 애플리케이션의 [filterable 속성](#configuring-filterable-data-for-meilisearch)을 미리 구성해야 합니다.

<a name="pagination"></a>
### 페이지네이션

검색 결과를 컬렉션으로만 가져오는 것이 아니라, `paginate` 메서드를 사용해 페이지네이션 형태로 받을 수도 있습니다. 이 메서드는 [일반적인 Eloquent 쿼리를 페이지네이션할 때](/docs/12.x/pagination)처럼 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 가져올 모델 수를 지정하려면 `paginate` 메서드에 원하는 수를 넘깁니다.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

이후 [Blade](/docs/12.x/blade)에서 결과와 페이지 링크를 평소 Eloquent 쿼리 페이지네이션과 동일하게 랜더링 할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 반환하려면, 라우트나 컨트롤러에서 Paginator 인스턴스를 직접 반환하면 됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent의 글로벌 스코프(Global Scope) 정의를 알지 못하기 때문에, Scout 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프를 이용하지 마세요. 혹은 Scout로 검색할 때 직접 글로벌 스코프의 제약 조건을 재구현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

인덱싱된 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 사용하고, 소프트 삭제 모델도 검색할 수 있도록 하려면, `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 변경하세요.

```php
'soft_delete' => true,
```

이 옵션이 활성화되면, Scout는 소프트 삭제된 모델을 인덱스에서 제거하는 대신 각 인덱스 레코드에 숨겨진 `__soft_deleted` 속성을 부여합니다. 이후 검색할 때 `withTrashed` 또는 `onlyTrashed` 메서드를 사용하여 소프트 삭제된 레코드를 포함할 수 있습니다.

```php
use App\Models\Order;

// 삭제된 레코드를 포함한 전체 검색...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된 레코드만 검색...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 영구 삭제하면, Scout가 인덱스에서도 자동으로 해당 레코드를 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

엔진의 고급 검색 동작을 커스터마이징하고 싶다면, `search` 메서드의 두 번째 인수로 클로저를 넘길 수 있습니다. 예를 들어, 검색 옵션에 지오로케이션 데이터를 추가하고 싶다면 아래와 같이 사용할 수 있습니다.

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

Scout가 검색 엔진에서 일치하는 Eloquent 모델의 ID 목록을 받아온 뒤, 실제 모델 전체 데이터를 가져오려면 Eloquent 쿼리가 다시 수행됩니다. 이 과정을 커스터마이징하고 싶다면, `query` 메서드에 클로저를 넘겨, Builder 인스턴스를 조작할 수 있습니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 검색 엔진에서 후보 모델 ID를 다 받아온 뒤 실행됩니다. 그러므로 결과를 "필터"하는 용도로 사용해서는 안되며, [Scout의 Where 절](#where-clauses)를 대신 사용해야 합니다.

<a name="custom-engines"></a>
## 사용자 정의 엔진

<a name="writing-the-engine"></a>
#### 엔진 직접 작성

내장된 Scout 검색 엔진이 원하는 조건에 맞지 않는다면, 직접 사용자 정의 엔진을 만들고 Scout에 등록할 수 있습니다. 사용자 정의 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 여덟 개의 메서드를 반드시 구현해야 합니다.

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

각 메서드 별 구현은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 사용자 정의 엔진을 작성하는 데 좋은 출발점이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

사용자 정의 엔진을 작성했다면, Scout 엔진 매니저의 `extend` 메서드로 등록할 수 있습니다. 엔진 매니저는 Laravel 서비스 컨테이너에서 해결할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 또는 적절한 서비스 프로바이더에서 아래와 같이 작성하세요.

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

엔진 등록 후, 애플리케이션의 `config/scout.php` 설정 파일에서 Scout의 기본 `driver`에 새로 등록한 엔진을 지정하세요.

```php
'driver' => 'mysql',
```
