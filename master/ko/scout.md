# Laravel Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 필수 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [구성](#configuration)
    - [모델 인덱스 구성](#configuring-model-indexes)
    - [색인 가능한 데이터 구성](#configuring-searchable-data)
    - [모델 ID 구성](#configuring-the-model-id)
    - [모델별 검색 엔진 구성](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [배치 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부로 색인되는 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/master/eloquent)에 전체 텍스트 검색 기능을 추가할 수 있도록 드라이버 기반의 간단한 솔루션을 제공합니다. 모델 옵저버(관찰자)를 사용하여, Scout는 Eloquent 레코드와 검색 인덱스를 자동으로 동기화합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본으로 지원합니다. 추가로 Scout에는 외부 의존성이나 서드파티 서비스를 필요로 하지 않는, 로컬 개발용 "collection" 드라이버도 포함되어 있습니다. 또한, 커스텀 드라이버도 쉽게 작성할 수 있어, 여러분만의 검색 구현체로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용해 Scout를 설치합니다.

```shell
composer require laravel/scout
```

설치가 완료되면 `vendor:publish` Artisan 명령어를 사용해 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령은 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리에 복사합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록해, 해당 모델이 자동으로 검색 드라이버와 동기화되도록 합니다.

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

`database` 또는 `collection` 엔진이 아닌 다른 엔진을 사용할 때는 [큐 드라이버](/docs/master/queues)를 반드시 구성한 뒤에 라이브러리를 사용하는 것을 권장합니다. 큐 워커를 실행하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업이 큐에 쌓이고, 애플리케이션 웹 인터페이스의 응답 속도가 크게 개선됩니다.

큐 드라이버를 구성한 후, `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 지정하세요.

```php
'queue' => true,
```

`queue` 옵션이 `false`로 설정되어 있어도, Algolia나 Meilisearch처럼 일부 Scout 드라이버는 항상 레코드를 비동기적으로 색인합니다. 즉, Laravel 애플리케이션 내에서 색인 작업이 끝났더라도, 검색 엔진에 새로운 레코드나 갱신된 레코드가 즉시 반영되지 않을 수 있습니다.

Scout 작업에서 사용할 connection과 queue를 지정하고 싶다면, `queue` 설정을 배열로 지정할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

물론 Scout 작업에서 사용하는 connection과 queue를 커스터마이징 했다면, 해당 connection과 queue에서 작업을 처리할 수 있도록 큐 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 필수 조건

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는, Algolia의 `id`와 `secret` 자격증명을 `config/scout.php` 파일에 설정해야 합니다. 자격증명 설정 후, Composer로 Algolia PHP SDK도 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈소스인 검색 엔진입니다. 로컬에 Meilisearch를 설치하는 방법을 모르는 경우, Laravel의 공식 Docker 개발 환경인 [Laravel Sail](/docs/master/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 땐, Composer로 Meilisearch PHP SDK를 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그 다음, 애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 Meilisearch의 `host`와 `key` 자격증명을 추가하세요.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 더 많은 정보는 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)에서 확인할 수 있습니다.

또한, Meilisearch 이진 파일 버전과 호환되는 `meilisearch/meilisearch-php`의 버전을 설치해야 하므로, [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 꼭 참고하세요.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 경우, 반드시 Meilisearch 서비스의 [추가적인 주요 변경사항(브레이킹 체인지)](https://github.com/meilisearch/Meilisearch/releases)도 함께 검토해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 키워드 검색, 시맨틱 검색, 위치(지오) 검색, 벡터 검색을 지원하는 고속 오픈소스 검색 엔진입니다.

Typesense는 [셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) 또는 [Typesense Cloud](https://cloud.typesense.org)에서 사용할 수 있습니다.

Typesense를 Scout와 함께 사용하려면 Composer로 Typesense PHP SDK를 설치하세요.

```shell
composer require typesense/typesense-php
```

그리고 애플리케이션의 .env 파일에 `SCOUT_DRIVER` 환경 변수와 Typesense의 host, API key를 설정하세요.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/master/sail)을 사용하는 경우, Docker 컨테이너 이름에 맞춰 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수 있습니다. 또한, 포트, 경로(path), 프로토콜도 선택적으로 지정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션에 대한 추가 설정과 스키마 정의는 애플리케이션의 `config/scout.php` 파일에서 할 수 있습니다. Typesense에 관한 더 자세한 내용은 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참조하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 데이터를 저장하기 위한 준비

Typesense를 사용할 때, 색인할 모델에는 모델의 기본 키를 문자열로, 생성일자를 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드가 반드시 정의되어야 합니다.

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

Typesense 컬렉션 스키마도 애플리케이션의 `config/scout.php` 파일에 정의해야 합니다. 컬렉션 스키마는, Typesense를 통해 검색할 때 각 필드의 데이터 타입을 지정합니다. 사용 가능한 모든 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)에서 확인할 수 있습니다.

컬렉션 스키마를 변경해야 할 경우, `scout:flush`와 `scout:import`를 차례로 실행해 인덱싱된 모든 데이터를 삭제하고 스키마를 재생성할 수 있습니다. 또는, Typesense의 API를 사용해 기존 인덱싱 데이터 손실 없이 컬렉션 스키마를 수정할 수도 있습니다.

색인할 모델이 소프트 삭제를 지원한다면, 해당 모델의 Typesense 컬렉션 스키마에 `__soft_deleted` 필드를 정의해야 합니다.

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

Typesense에서는 `options` 메서드를 이용해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 조정할 수 있습니다.

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

각 Eloquent 모델은 해당 모델의 모든 색인 가능 레코드를 포함하는 특정 검색 "인덱스"와 동기화됩니다. 각 인덱스는 MySQL의 테이블과 비슷하다고 생각하면 이해가 쉽습니다. 기본적으로는 각 모델이 보통의 "테이블" 이름을 인덱스명으로 사용합니다(일반적으로 모델명 복수형). 하지만 `searchableAs` 메서드를 오버라이드해 인덱스 이름을 자유롭게 변경할 수 있습니다.

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
### 색인 가능한 데이터 구성

기본적으로 모델의 전체 `toArray` 형태가 검색 인덱스에 저장됩니다. 색인에 동기화할 데이터를 직접 제어하고 싶다면 모델의 `toSearchableArray` 메서드를 오버라이드하세요.

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

        // 데이터 배열 커스터마이징...

        return $array;
    }
}
```

Meilisearch 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 올바른 타입의 데이터만 대상으로 수행합니다. 이렇게 검색 엔진과 색인할 데이터를 커스터마이즈할 경우, 숫자 값을 올바른 타입으로 캐스팅해야 합니다.

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
#### 인덱스 설정 구성(Algolia)

Algolia 인덱스에 추가 설정을 적용할 때가 있습니다. Algolia UI에서 직접 관리할 수도 있지만, 애플리케이션의 `config/scout.php` 파일 형태로 직접 설정을 관리하면 자동화된 배포 파이프라인을 활용할 수 있어 더욱 효율적입니다. 이를 통해 여러 환경에서 일관된 구성이 보장되고, 수동 설정을 피할 수 있습니다. 필터 속성, 정렬(ranking), 패싯(faceting), [그 밖의 모든 설정들](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

우선, 애플리케이션의 `config/scout.php` 파일의 각 인덱스에 대해 설정을 추가하세요.

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

특정 인덱스의 모델이 소프트 삭제를 지원하고, 해당 모델이 `index-settings` 배열에 포함되어 있다면, Scout가 자동으로 소프트 삭제 모델 인덱스에 대한 faceting 지원을 추가합니다. 소프트 삭제 모델 인덱스에 다른 faceting 속성이 필요 없다면, 해당 모델에 대해 빈 엔트리를 추가하면 됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

인덱스 설정을 구성했다면, 반드시 `scout:sync-index-settings` Artisan 명령어를 실행해야 합니다. 이 명령어는 Algolia에 최신 인덱스 설정을 전달합니다. 배포 시 해당 명령을 자동화하면 더욱 편리합니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능 데이터 및 인덱스 설정 구성(Meilisearch)

Scout의 다른 드라이버와 달리, Meilisearch는 필터 가능 속성, 정렬 가능 속성 등 다양한 [인덱스 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 미리 정의해야 합니다.

필터 가능 속성은 `where` 메서드를 사용할 때 필터링할 속성, 정렬 가능 속성은 `orderBy` 메서드로 정렬할 속성입니다. 인덱스 설정은 `scout` 설정 파일의 `meilisearch` 설정 항목 내 `index-settings` 값을 조정해 지정합니다.

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

특정 인덱스의 모델이 소프트 삭제를 지원하며, 해당 모델이 `index-settings` 배열에 지정되어 있다면, Scout에서 자동으로 소프트 삭제 모델에 대한 필터링 지원을 추가합니다. 소프트 삭제 모델 인덱스에 추가 필터/정렬 속성이 없다면, 빈 엔트리를 추가하세요.

```php
'index-settings' => [
    Flight::class => []
],
```

설정이 끝나면 `scout:sync-index-settings` Artisan 명령어를 실행해 Meilisearch에 최신 인덱스 설정을 알려야 합니다. 배포 시 자동화하는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 구성

Scout는 기본적으로 모델의 기본 키(primary key)를 검색 인덱스에 저장되는 모델의 고유 ID/키로 사용합니다. 이 동작을 커스터마이즈하려면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 색인에 사용할 값 반환
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 색인에 사용할 키 이름 반환
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 구성

일반적으로 Scout는 애플리케이션의 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용합니다. 그러나 특정 모델만 다른 검색 엔진을 사용하고 싶다면, `searchableUsing` 메서드를 오버라이드하면 됩니다.

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
     * 색인에 사용할 엔진 반환
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시, 사용자 식별을 자동으로 적용할 수도 있습니다. 인증된 사용자를 검색 작업과 연계하면 Algolia 대시보드에서 검색 분석(analytics) 시 유용합니다. 사용자 식별을 활성화하려면 애플리케이션의 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하세요.

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면, 요청의 IP 주소와 인증된 사용자의 기본 식별자가 Algolia로 전달되어 해당 데이터를 사용자별 검색 요청에 연결합니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

`database` 엔진은 Laravel Scout를 시작하는 가장 빠른 방법입니다. 이 엔진은 MySQL 또는 PostgreSQL의 전체 텍스트 인덱스와 "where like" 절을 사용해서 쿼리 결과에서 해당 검색값에 맞는 레코드를 추립니다.

데이터베이스 엔진을 사용하려면, 단순히 `SCOUT_DRIVER` 환경 변수를 `database`로 설정하거나, `scout` 설정 파일에서 `database` 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 지정했다면, [색인할 데이터를 구성](#configuring-searchable-data)하고, [검색 쿼리](#searching)를 실행할 수 있습니다. Algolia, Meilisearch, Typesense처럼 별도의 검색 엔진 인덱싱 작업은 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [색인 가능하도록 구성한](#configuring-searchable-data) 모든 모델 속성에 대해 "where like" 쿼리를 실행합니다. 그러나 상황에 따라 성능 저하가 발생할 수 있으므로, 일부 컬럼만 전체 텍스트 검색을 사용하거나, 일부 컬럼은 문자열의 접두사 검색(`example%`)만 사용하도록 조절할 수 있습니다.

이 동작을 지정하려면, 모델의 `toSearchableArray` 메서드에 PHP 속성(attribute)을 지정하세요. 추가적인 검색 전략이 지정되지 않은 컬럼은 기본 "where like" 전략을 그대로 사용합니다.

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
> 컬럼에서 전체 텍스트 검색이 가능하도록 지정하기 전에, 해당 컬럼에 [전체 텍스트 인덱스](/docs/master/migrations#available-index-types)가 설정되어 있는지 확실히 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 시 Algolia, Meilisearch, Typesense 엔진을 사용할 수도 있지만, 시작은 "collection" 엔진이 훨씬 편리할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 "where" 절과 컬렉션 필터링을 활용해 쿼리 결과에서 해당 검색값에 맞는 결과를 추출합니다. 이 엔진을 사용할 때는 별도의 인덱싱 작업 없이, 로컬 데이터베이스에서 모델을 바로 조회합니다.

컬렉션 엔진 사용을 위해서는 `SCOUT_DRIVER` 환경 변수를 `collection`으로 설정하거나, `scout` 설정 파일에서 드라이버를 직접 지정하면 됩니다.

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 지정한 후에는 [검색 쿼리](#searching)를 바로 실행할 수 있습니다. 별도의 인덱싱 작업은 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이점

겉보기엔 "database" 엔진과 "collection" 엔진이 비슷해보이지만, collection 엔진은 전체 텍스트 인덱스나 `LIKE` 절을 사용하지 않습니다. 대신 모든 후보 레코드를 조회한 뒤, Laravel의 `Str::is` 헬퍼로 검색 문자열이 각 모델 속성 값에 포함되어 있는지를 확인합니다.

컬렉션 엔진은 SQLite나 SQL Server를 포함한 Laravel 지원 모든 관계형 데이터베이스에서 동작하므로 이식성이 매우 높지만, Scout의 database 엔진에 비해서 효율성은 상당히 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 가져오기

기존 프로젝트에 Scout를 도입하는 경우, 이미 존재하는 데이터베이스 레코드를 인덱스에 가져와야 할 수 있습니다. Scout에서는 모든 기존 레코드를 검색 인덱스에 가져올 수 있도록 `scout:import` Artisan 명령어를 제공합니다.

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue-import` 명령어를 사용하면 [큐 작업](/docs/master/queues)으로 모든 기존 레코드를 가져올 수 있습니다.

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```

`flush` 명령어를 사용하면 특정 모델의 모든 레코드를 검색 인덱스에서 제거할 수 있습니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 커스터마이징

배치 가져오기에 사용할 모델 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의하면 됩니다. 이 메서드는, 가져오기 전에 관계를 미리 로드(eager load)해야 할 경우에 아주 유용합니다.

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모두 색인할 때 사용할 쿼리 수정
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> `makeAllSearchableUsing` 메서드는 큐를 이용해 배치 가져오기를 진행할 때는 적용되지 않을 수 있습니다. 큐 작업시 모델 컬렉션의 관계는 [복원되지 않습니다](/docs/master/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

모델에 `Laravel\Scout\Searchable` 트레이트를 추가했다면, 인스턴스를 `save` 또는 `create` 만 해주면 자동으로 검색 인덱스에 추가됩니다. Scout를 [큐 작업](#queueing)으로 구성했다면, 이 작업은 백그라운드에서 진행됩니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가

Eloquent 쿼리에 `searchable` 메서드를 체이닝하여 다수의 모델을 한 번에 색인에 추가할 수도 있습니다. 이때, 쿼리 결과가 [조각(chunk)](/docs/master/eloquent#chunking-results) 단위로 처리되어 인덱스에 추가됩니다. Scout가 큐 작업을 사용하도록 설정되어 있다면 역시 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스(`orders()` 등)에서 `searchable`을 호출할 수도 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션을 메모리에 보유하고 있다면, 컬렉션 인스턴스에서 `searchable`을 호출하여 인덱스에 추가할 수 있습니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "upsert" 동작(업데이트 또는 삽입)으로 볼 수 있습니다. 즉, 인덱스에 이미 모델이 있으면 업데이트하고, 없으면 새로 추가합니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 단순히 모델 속성을 변경 후 데이터베이스에 `save`하면 됩니다. Scout가 자동으로 변경 사항을 검색 인덱스에 반영합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문 정보 수정...

$order->save();
```

Eloquent 쿼리 인스턴스에서 `searchable`을 호출해서 다수의 모델을 한 번에 업데이트할 수도 있습니다. 인덱스에 모델이 없으면 새로 추가됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

관계 인스턴스에서도 `searchable`을 호출하여 관계에 속한 모든 모델의 검색 인덱스를 업데이트할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션이 있다면, 컬렉션 인스턴스에서 `searchable`을 호출하여 관련 인덱스를 업데이트할 수 있습니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 가공

몇몇 경우에는 색인에 추가하기 전에 모델 컬렉션을 준비해야 할 때가 있습니다. 예를 들어, 관계를 미리 로드하여 관계 데이터를 인덱스에 함께 추가하고 싶을 수 있습니다. 이럴 때는 해당 모델에 `makeSearchableUsing` 메서드를 정의하세요.

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 색인 처리할 모델 컬렉션 가공
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="conditionally-updating-the-search-index"></a>
#### 색인 업데이트 조건 커스터마이징

기본적으로 Scout는 어떤 속성이 변경되었든 모델이 업데이트될 때마다 검색 인덱스를 갱신합니다. 만약 갱신 조건을 세밀하게 제어하고 싶다면, 모델에 `searchIndexShouldBeUpdated` 메서드를 정의할 수 있습니다.

```php
/**
 * 검색 인덱스를 업데이트할지 여부 결정
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```

<a name="removing-records"></a>
### 레코드 제거

검색 인덱스에서 레코드를 제거하려면, 데이터베이스에서 해당 모델을 `delete`하면 됩니다. 이는 [소프트 삭제](/docs/master/eloquent#soft-deleting) 모델에도 적용됩니다.

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 미리 조회하지 않고 바로 삭제하려면, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용하세요.

```php
Order::where('price', '>', 100)->unsearchable();
```

관계 인스턴스에서도 `unsearchable`을 호출하여 관계에 속한 모든 모델의 검색 인덱스를 제거할 수 있습니다.

```php
$user->orders()->unsearchable();
```

이미 Eloquent 모델 컬렉션이 있다면, 컬렉션 인스턴스에서 `unsearchable`을 호출하여 인덱스에서 일괄 제거할 수 있습니다.

```php
$orders->unsearchable();
```

모델의 모든 레코드를 해당 인덱스에서 제거하려면 `removeAllFromSearch` 메서드를 사용하세요.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

특정 모델에서 여러 Eloquent 작업을 수행할 때, 동기화를 일시적으로 중단하고 싶을 때가 있습니다. 이럴 때는 `withoutSyncingToSearch` 메서드를 사용하면 됩니다. 이 메서드는 즉시 실행되는 하나의 클로저를 인자로 받으며, 해당 클로저 안에서 일어나는 모든 모델 작업은 색인 동기화가 수행되지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델에 대한 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 색인되는 모델 인스턴스

특정 조건에서만 모델을 색인하고 싶을 때가 있습니다. 예를 들어 `App\Models\Post` 모델에 "draft"와 "published" 두 가지 상태가 있다고 가정하면, "published"인 경우에만 색인되도록 하려면 다음과 같이 모델에 `shouldBeSearchable` 메서드를 정의하세요.

```php
/**
 * 모델이 색인 대상인지 여부를 결정
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`, `create` 메서드, 쿼리, 관계를 통한 작업 시에만 적용됩니다. 직접적으로 모델이나 컬렉션에 `searchable`을 호출하면 이 메서드의 반환 값과 상관없이 색인됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진 사용 시 적용되지 않습니다. database 엔진은 모든 색인 데이터를 데이터베이스에 저장하기 때문입니다. database 엔진에서 유사한 기능을 원할 때는 [where 절](#where-clauses)로 구현해야 합니다.

<a name="searching"></a>
## 검색

모델의 `search` 메서드를 사용해 검색을 시작할 수 있습니다. 이 메서드는 검색에 사용할 문자열 하나를 인자로 받고, 이어서 `get` 메서드를 체이닝하여 해당 쿼리에 매칭되는 Eloquent 모델을 가져옵니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout의 검색 결과는 Eloquent 모델 컬렉션이므로, 결과 컬렉션을 바로 라우트나 컨트롤러에서 반환하면 자동으로 JSON 변환됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Eloquent 모델로 변환되기 전, 원시 검색 결과가 필요할 때는 `raw` 메서드를 사용하세요.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스

일반적으로 검색 쿼리는 모델의 [searchableAs](#configuring-model-indexes) 메서드에 지정된 인덱스에서 실행됩니다. 그러나 `within` 메서드를 이용해 별도의 인덱스를 지정하여 검색을 수행할 수도 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있습니다. 현재로서는, 기본 숫자형 동등(equality) 비교만 지원하며, 주로 소유자 ID로 범위를 제한하는 데 유용합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

`whereIn` 메서드는 특정 컬럼값이 배열에 포함되는지 검증합니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 특정 컬럼값이 배열에 포함되지 않은 경우를 필터링합니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니기 때문에, 이 외의 복잡한 "where" 절은 지원되지 않습니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout의 "where" 절을 사용하려면, 반드시 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 미리 설정해야 합니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 단순히 조회하는 것 외에도, `paginate` 메서드를 사용해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 일반 Eloquent 쿼리와 동일하게 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지 당 모델 개수를 첫 번째 인자로 지정할 수 있습니다.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

검색 결과를 [Blade](/docs/master/blade)에서 전통적인 Eloquent 페이지네이션과 동일하게 표시할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 받고 싶다면, 라우트나 컨트롤러에서 paginator 인스턴스를 그대로 반환하면 됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프를 인식하지 못하므로, Scout 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프(global scope)를 사용하지 않는 것이 좋습니다. 또는, 별도의 로직으로 스코프 제약을 Scout 검색 시 재현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

색인된 모델이 [소프트 삭제](/docs/master/eloquent#soft-deleting)를 지원하며, 소프트 삭제된 모델도 검색 대상으로 삼아야 할 때는 `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 설정하세요.

```php
'soft_delete' => true,
```

이 옵션이 `true`이면, Scout는 소프트 삭제된 모델을 검색 인덱스에서 제거하지 않고, 숨겨진 `__soft_deleted` 속성을 색인 레코드에 추가합니다. 이제 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해, 검색 시 소프트 삭제된 레코드를 함께 포함하거나, 소프트 삭제된 레코드만 조회할 수 있습니다.

```php
use App\Models\Order;

// 삭제된 레코드도 함께 결과에 포함...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 소프트 삭제된 레코드만 결과에 포함...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 완전히 삭제하면, Scout는 해당 레코드를 검색 인덱스에서 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

검색 엔진의 동작을 더 세밀하게 제어하려면, `search` 메서드의 두 번째 인자로 클로저(콜백)을 전달할 수 있습니다. 예를 들어, 이 콜백에서 검색 옵션에 지오로케이션 데이터를 추가하여 Algolia에 전달할 수 있습니다.

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

Scout가 검색 엔진에서 일치하는 Eloquent 모델 목록을 받아온 후, Eloquent가 기본 키 기준으로 최종 모델을 조회합니다. 이 쿼리를 개별적으로 커스터마이즈하고 싶다면, `query` 메서드를 사용하세요. `query` 메서드는 Eloquent 쿼리 빌더 인스턴스를 인자로 받는 클로저를 인자로 전달합니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 검색 엔진에서 일치 모델을 조회한 뒤에 실행되므로, 결과를 추가로 "필터링"하는 용도로는 적합하지 않습니다. 필터링이 필요하다면 [Scout where 절](#where-clauses)을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성하기

내장 Scout 검색 엔진으로 요구사항을 해결할 수 없다면, 자체 커스텀 엔진을 구현해서 Scout에 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속받아야 하며, 아래의 8가지 메서드를 반드시 구현해야 합니다.

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

각 메서드의 실제 구현은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스에서 참고할 수 있습니다. 여기를 참고하면 커스텀 엔진 메서드 구현에 많은 도움을 받을 수 있습니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진을 작성한 후에는, Scout의 `extend` 메서드를 사용해 엔진을 등록할 수 있습니다. Scout의 엔진 매니저는 Laravel 서비스 컨테이너에서 해결(resolve)할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스나 그 밖에 애플리케이션에서 사용하는 서비스 프로바이더의 `boot` 메서드에서 호출하면 됩니다.

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

엔진을 등록한 후, 애플리케이션의 `config/scout.php` 파일에서 기본 Scout `driver`로 지정하면 됩니다.

```php
'driver' => 'mysql',
```
