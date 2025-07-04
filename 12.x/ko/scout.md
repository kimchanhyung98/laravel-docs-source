# 라라벨 Scout (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉 설정](#queueing)
- [드라이버 사전 준비 사항](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [환경설정](#configuration)
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
    - [인덱싱 일시중지](#pausing-indexing)
    - [조건부 인덱싱 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이즈](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[라라벨 Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 전체 텍스트 검색 기능을 손쉽게 추가할 수 있는, 드라이버 기반의 간단한 솔루션을 제공합니다. 모델 옵저버를 활용하여, Scout는 Eloquent 레코드와 검색 인덱스의 동기화를 자동으로 관리해줍니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL (`database`) 드라이버와 함께 제공됩니다. 또한, Scout는 외부 의존성이나 서드파티 서비스 없이 로컬 개발 환경에서 사용할 수 있도록 설계된 "collection" 드라이버도 제공합니다. 그리고 직접 커스텀 드라이버를 작성하는 것도 매우 간단하므로, 필요에 따라 Scout를 확장하여 자신만의 검색 엔진을 구현할 수도 있습니다.

<a name="installation"></a>
## 설치

우선, Composer 패키지 관리자를 통해 Scout를 설치합니다.

```shell
composer require laravel/scout
```

설치가 완료되면, `vendor:publish` 아티즌 명령어를 사용하여 Scout 설정 파일을 배포해야 합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리에 생성합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 가능하게 만들고 싶은 모델에 `Laravel\Scout\Searchable` 트레이트를 추가해줍니다. 이 트레이트를 적용하면 모델 옵저버가 자동 등록되어 해당 모델이 사용하는 검색 드라이버와 자동으로 동기화됩니다.

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
### 큐잉 설정

Scout를 사용하기 위해 큐 드라이버를 반드시 설정해야 하는 것은 아니지만, 라이브러리 사용 전 [큐 드라이버](/docs/12.x/queues) 설정을 강력히 권장합니다. 큐 워커를 실행하면 모델 데이터를 검색 인덱스와 동기화하는 모든 작업이 큐로 처리되어, 애플리케이션 웹 인터페이스의 응답 속도가 훨씬 빨라집니다.

큐 드라이버를 설정했다면, `config/scout.php` 설정 파일에서 `queue` 옵션 값을 `true`로 지정합니다.

```php
'queue' => true,
```

`queue` 옵션을 `false`로 설정한 경우에도 주의할 점이 있습니다. Algolia, Meilisearch 등 일부 Scout 드라이버는 항상 비동기적으로 레코드를 인덱싱합니다. 즉, 라라벨 애플리케이션에서 인덱싱 작업이 끝나더라도 실제 검색 엔진에는 바로 반영되지 않을 수 있습니다.

Scout 작업이 사용할 연결(connection)과 큐(queue)를 지정하고 싶다면, `queue` 설정 옵션을 배열로 지정할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

물론, Scout 작업에 사용할 연결과 큐를 직접 지정했다면, 해당 연결과 큐를 처리하는 워커를 반드시 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비 사항

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용하려면, `config/scout.php` 설정 파일에 Algolia `id`와 `secret` 자격 정보를 입력해 주어야 합니다. 자격 정보를 지정한 후에는 Composer 패키지 관리자를 통해 Algolia PHP SDK를 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠른 오픈소스 검색 엔진입니다. Meilisearch를 로컬에서 설치하는 방법을 잘 모른다면, 라라벨의 공식 Docker 개발 환경인 [Laravel Sail](/docs/12.x/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 때는, Composer 패키지 관리자를 사용해 Meilisearch PHP SDK를 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고 애플리케이션의 `.env` 파일에서 `SCOUT_DRIVER` 환경 변수와 함께, Meilisearch `host` 및 `key` 자격 정보를 설정합니다.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 관한 자세한 정보는 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고해 주십시오.

또한 `meilisearch/meilisearch-php`의 버전이 사용하는 Meilisearch 바이너리 버전과 호환되는지 [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 확인하는 것이 좋습니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는, 반드시 Meilisearch 서비스 자체의 [추가적인 변경사항이나 큰 변경점](https://github.com/meilisearch/Meilisearch/releases)을 꼼꼼히 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈소스 검색 엔진으로, 키워드 검색, 시맨틱(의미 기반) 검색, 지오(공간 위치) 검색, 벡터 검색을 지원합니다.

Typesense는 [셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout에서 Typesense를 사용하려면 Composer 패키지 관리자를 통해 Typesense PHP SDK를 설치합니다.

```shell
composer require typesense/typesense-php
```

그리고 애플리케이션의 `.env` 파일에서 `SCOUT_DRIVER` 환경 변수와 Typesense `host`, API key 자격 정보를 설정합니다.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용할 경우, Docker 컨테이너 이름에 맞게 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수도 있습니다. 또한, 설치 환경에 따라 포트, 경로, 프로토콜도 선택적으로 지정할 수 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션과 관련된 추가적인 설정 및 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 찾을 수 있습니다. Typesense에 대해 더 많은 정보를 원하신다면 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하시기 바랍니다.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense를 사용할 때 검색 가능한 모델은, 모델의 기본 키(primary key)를 문자열로, 생성일(created_at)을 UNIX 타임스탬프로 변환하여 반환하는 `toSearchableArray` 메서드를 반드시 정의해야 합니다.

```php
/**
 * 모델의 인덱싱 가능한 데이터 배열을 반환합니다.
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

또한, Typesense 컬렉션의 스키마도 반드시 애플리케이션의 `config/scout.php` 파일에 정의해야 합니다. 컬렉션 스키마란 Typesense를 통한 필드별 데이터 타입 등 검색 가능한 각 필드에 대한 정의입니다. 자세한 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 확인하세요.

이미 정의한 Typesense 컬렉션의 스키마를 변경해야 할 경우, `scout:flush`와 `scout:import` 명령어를 통해 기존 인덱스 데이터 전체를 삭제하고 스키마를 재생성할 수 있습니다. 또는 Typesense의 API를 활용해 이미 인덱싱된 데이터를 삭제하지 않고도 컬렉션 스키마를 수정할 수 있습니다.

검색 가능한 모델이 소프트 삭제(soft delete)를 지원한다면, 해당 모델의 Typesense 스키마에 아래와 같이 `__soft_deleted` 필드를 정의해야 합니다.

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

Typesense는 검색 수행 시 `options` 메서드를 통해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 지정할 수 있습니다.

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```

<a name="configuration"></a>
## 환경설정

<a name="configuring-model-indexes"></a>
### 모델 인덱스 설정

각 Eloquent 모델은 해당 모델의 모든 검색 가능한 레코드를 담는 특정 검색 "인덱스(index)"와 동기화됩니다. 쉽게 말해, 각 인덱스는 MySQL 테이블과 비슷하다고 생각할 수 있습니다. 일반적으로 각 모델은 모델의 "테이블" 이름과 동일한 인덱스에 저장됩니다. 보통 이는 모델명을 복수형으로 쓴 이름입니다. 다만, 원하는 경우 `searchableAs` 메서드를 모델에서 오버라이드하여 인덱스 이름을 자유롭게 커스터마이즈할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 매칭되는 인덱스 이름을 반환합니다.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 데이터 설정

기본적으로 모델의 `toArray`를 통해 변환된 전체 데이터가 검색 인덱스에 저장됩니다. 인덱스에 동기화할 데이터를 직접 제어하고 싶다면, 모델에서 `toSearchableArray` 메서드를 오버라이드할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱싱 데이터 배열을 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // 이곳에서 원하는 데이터로 $array를 커스터마이즈하세요.

        return $array;
    }
}
```

Meilisearch와 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 올바른 타입의 데이터에 대해서만 지원합니다. 따라서 이런 검색 엔진을 사용할 때는, 검색 데이터 내 숫자 값 등은 타입을 반드시 맞춰 변환하여 저장해야 합니다.

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
#### 인덱스 설정 (Algolia)

간혹 Algolia 인덱스의 추가적인 설정이 필요할 수 있습니다. 이러한 설정은 Algolia UI에서 직접 관리할 수도 있지만, 애플리케이션의 `config/scout.php` 설정 파일에서 직접 컨트롤하면 더 효율적으로 배포 관리가 가능합니다.

이 방식으로 관리하면 자동화된 배포 파이프라인을 통해 설정을 손쉽게 반영할 수 있고, 여러 환경에서 인덱스 설정의 일관성도 보장할 수 있습니다. 필터링 필드, 랭킹, 패싯(faceting) 등 [다양한 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

설정 방법은, `config/scout.php` 파일 내에서 각 인덱스별로 설정 값을 추가해주면 됩니다.

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

특정 인덱스의 모델이 소프트 삭제(soft delete)를 지원하고 `index-settings` 배열에 포함되어 있다면, Scout는 해당 인덱스에서 소프트 삭제 모델의 패싯 자동 지원을 추가해줍니다. 소프트 삭제 모델을 위한 별도의 패싯 필드가 없다면, 아래와 같이 빈 배열로 추가해도 무방합니다.

```php
'index-settings' => [
    Flight::class => []
],
```

인덱스 설정을 모두 지정했다면, 반드시 `scout:sync-index-settings` 아티즌 명령을 실행해야 합니다. 이 명령은 현재 설정 파일에 지정된 인덱스 설정을 Algolia에 반영합니다. 배포 자동화 과정에 이 명령을 추가하는 것도 좋은 방법입니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터 가능한 데이터 및 인덱스 설정 (Meilisearch)

Scout의 다른 드라이버와 달리, Meilisearch는 필터링, 정렬, 기타 여러 인덱스 설정을 사전에 정의해야 합니다. ([참고: 기타 설정 가능 필드](https://docs.meilisearch.com/reference/api/settings.html))

'필터 가능한 속성(filterable attributes)'이란 Scout의 `where` 메서드로 필터링할 계획인 속성을 의미하고, '정렬 가능한 속성(sortable attributes)'은 `orderBy`로 정렬하고픈 속성입니다. 이러한 인덱스 설정은 `scout` 설정 파일의 `meilisearch` 항목 내 `index-settings` 부분에서 지정합니다.

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

특정 인덱스의 모델이 소프트 삭제를 지원하면서 `index-settings` 배열에 포함되어 있다면, Scout는 이 인덱스에서 소프트 삭제 모델의 필터링 지원을 자동으로 추가합니다. 필터나 정렬 속성이 따로 없더라도, 아래처럼 빈 배열로 추가해도 문제없습니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정이 끝났다면, 반드시 `scout:sync-index-settings` 아티즌 명령을 실행해야 합니다. 이 명령은 현재 설정 파일의 인덱스 세팅을 Meilisearch에 동기화합니다. 실제 배포 시 이 명령을 배포 과정에 포함시키는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키(primary key)를 인덱스상의 고유 ID/키로 사용합니다. 이 방식을 변경하고 싶다면, 모델에서 `getScoutKey` 및 `getScoutKeyName` 메서드를 오버라이드할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 인덱싱에 사용할 값 반환
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * 인덱싱에 사용할 키 이름 반환
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

기본적으로 Scout는 `scout` 설정 파일에 지정된 기본 검색 엔진을 사용해서 검색을 수행합니다. 하지만 특정 모델에 대해서는 `searchableUsing` 메서드를 오버라이드해서 사용할 검색 엔진을 지정할 수 있습니다.

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
     * 인덱싱에 사용할 엔진 반환
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시 자동으로 사용자 식별 기능도 지원합니다. 이는 검색 작업과 관련해 인증된 사용자를 Algolia 대시보드의 검색 분석에 연동하고 싶을 때 유용하게 활용됩니다. 해당 기능을 활성화하려면 애플리케이션의 `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 설정하면 됩니다.

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면 사용자의 IP 주소와, 인증된 사용자의 기본 식별자가 Algolia로 전달되어 검색 요청에 연결됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

애플리케이션이 소규모~중간 규모의 데이터베이스를 다루거나, 복잡하지 않은 워크로드를 가진 경우에는 Scout의 "database" 엔진으로 빠르게 시작할 수 있습니다. 이 엔진은 "where like" 문과 전체 텍스트 인덱스를 활용해 기존 데이터베이스에서 검색 결과를 추출합니다.

데이터베이스 엔진을 사용하려면, 환경 변수 `SCOUT_DRIVER` 값을 `database`로 지정하거나, `scout` 설정 파일에서 드라이버를 직접 `database`로 명시하면 됩니다.

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 기본 드라이버로 지정했으면, [검색 데이터 설정](#configuring-searchable-data)을 반드시 완료해야 합니다. 그 후 [검색 쿼리 실행](#searching)을 통해 모델을 검색할 수 있습니다. 이 엔진을 사용할 때에는 Algolia, Meilisearch, Typesense 등 외부 인덱싱 작업이 전혀 필요하지 않습니다.

#### 데이터베이스 검색 전략 커스터마이징

데이터베이스 엔진은 기본적으로, [검색 데이터로 지정한](#configuring-searchable-data) 모든 모델 속성(attribute)에 대해 "where like" 쿼리를 실행합니다. 하지만 상황에 따라 이 방식이 성능상 문제가 될 수 있으므로, 일부 컬럼에 대해서만 전체 텍스트 검색 쿼리나 접두사(prefix) 검색(문자열 앞부분에서만 검색, `example%`)을 적용하도록 전략을 세분화할 수 있습니다.

이 동작을 지정하려면, 모델의 `toSearchableArray` 메서드에 PHP 속성(attributes)을 할당합니다. 별도로 지정되지 않은 컬럼은 기존 "where like" 방식이 그대로 적용됩니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱싱 데이터 배열 반환
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
> 특정 컬럼에 대해 전체 텍스트 쿼리 전략을 적용하기 전, 해당 컬럼이 [full text 인덱스](/docs/12.x/migrations#available-index-types)로 등록되어 있는지 반드시 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 환경에서 Algolia, Meilisearch, Typesense 엔진을 설치해 사용해도 되지만, "collection" 엔진으로 간단히 시작하는 것도 좋은 방법입니다. 이 엔진은 데이터베이스의 데이터를 바탕으로 "where" 조건과 컬렉션 필터링을 사용해 검색 결과를 추출합니다. 별도의 인덱싱 작업 없이, 검색 가능한 모델을 그냥 데이터베이스에서 가져와서 검색하는 방식입니다.

컬렉션 엔진을 사용하려면 환경 변수 `SCOUT_DRIVER` 값을 `collection`으로 지정하거나, `scout` 설정 파일에서 드라이버를 명시합니다.

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버를 지정하면, [검색 쿼리 실행](#searching)을 통해 모델을 검색할 수 있습니다. 인덱싱 작업(Algolia, Meilisearch, Typesense 등)은 필요하지 않습니다.

#### 데이터베이스 엔진과의 차이

처음 보면 "database"와 "collection" 엔진이 비슷해 보일 수 있습니다. 둘 다 데이터베이스에서 직접 검색 결과를 추출하는 점은 같지만, 컬렉션 엔진은 전용 full text 인덱스나 `LIKE` 조건문을 전혀 사용하지 않습니다. 대신, 모든 가능 레코드를 불러와서 라라벨의 `Str::is` 헬퍼로 속성 값 내 검색어 존재 여부를 검사하는 방식입니다.

컬렉션 엔진은 모든 라라벨 지원 관계형 데이터베이스(예: SQLite, SQL Server 포함)에서 동작하기 때문에 가장 범용성이 높지만, 성능 면에서는 Scout의 데이터베이스 엔진이 더 효율적이라 할 수 있습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 도입할 때, 이미 데이터베이스에 등록되어 있는 데이터를 인덱스로 임포트할 필요가 있습니다. Scout에서는 기존 모든 레코드를 검색 인덱스로 한 번에 임포트할 수 있도록 `scout:import` 아티즌 명령어를 제공합니다.

```shell
php artisan scout:import "App\Models\Post"
```

모델의 모든 레코드를 검색 인덱스에서 제거하고자 할 때는 `flush` 명령어를 사용할 수 있습니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 수정

모든 모델을 임포트할 때 사용되는 쿼리를 커스터마이즈하려면, 모델에서 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 예를 들어, 임포트 전에 특정 연관관계를 eager 로딩하고 싶을 때 이 메서드를 활용할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모델 전체를 검색 가능하게 만들 때 실행되는 쿼리를 수정합니다.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> 모델을 배치 임포트할 때 큐를 사용하는 경우에는 `makeAllSearchableUsing` 메서드가 적용되지 않을 수도 있습니다. 큐 작업에서 모델 컬렉션이 처리될 때 연관관계는 [복원되지 않습니다](/docs/12.x/queues#handling-relationships).

### 레코드 추가하기

`Laravel\Scout\Searchable` 트레이트를 모델에 추가한 후에는, 단순히 모델 인스턴스를 `save`하거나 `create`만 해주면 자동으로 해당 인스턴스가 검색 인덱스에 추가됩니다. 만약 Scout에서 [큐 사용을 설정](#queueing)해두었다면, 이 작업은 큐 워커가 백그라운드에서 자동으로 처리합니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리를 통해 여러 모델을 검색 인덱스에 추가하고 싶을 때는, Eloquent 쿼리 뒤에 `searchable` 메서드를 체이닝하면 됩니다. `searchable` 메서드는 쿼리 결과를 [청크 단위](/docs/12.x/eloquent#chunking-results)로 분할하여 각 레코드를 검색 인덱스에 추가합니다. 역시 Scout에서 큐 사용을 설정해 두었다면, 모든 청크가 큐 워커를 통해 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에서도 `searchable` 메서드를 호출할 수 있습니다.

```php
$user->orders()->searchable();
```

또는 이미 메모리에 Eloquent 모델 컬렉션이 있다면, 해당 컬렉션 인스턴스에서 `searchable` 메서드를 호출하여 각 모델 인스턴스를 해당 인덱스에 추가할 수 있습니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 "업서트(upsert)" 연산으로 간주할 수 있습니다. 즉, 인덱스에 이미 모델 레코드가 있다면 업데이트되고, 없다면 인덱스에 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 수정하기

검색이 가능한 모델을 수정하려면, 그저 해당 모델 인스턴스의 속성(property)을 변경하고 데이터베이스에 `save`하면 됩니다. Scout가 검색 인덱스에도 변경 사항을 자동으로 반영합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문(order) 정보 수정...

$order->save();
```

Eloquent 쿼리 인스턴스에서 직접 `searchable` 메서드를 호출해 여러 모델을 일괄 업데이트할 수도 있습니다. 만약 검색 인덱스에 모델이 없으면 새로 생성됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

관계에서 모든 모델의 검색 인덱스 레코드를 업데이트하려면 관계 인스턴스에서 `searchable`을 호출하면 됩니다.

```php
$user->orders()->searchable();
```

또는 이미 메모리에 Eloquent 모델 컬렉션이 있다면, 해당 컬렉션 인스턴스에서 `searchable`을 호출해 각 모델 인스턴스를 인덱스에 업데이트할 수 있습니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전에 레코드 가공하기

검색 가능하게 만들기 전에 모델 컬렉션을 별도로 가공해야 할 때가 있습니다. 예를 들어 관련 데이터를 효율적으로 인덱싱하려고 관계를 eager loading 하고 싶을 수 있습니다. 이를 위해, 해당 모델 클래스에 `makeSearchableUsing` 메서드를 정의할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능하도록 만드는 모델 컬렉션을 수정합니다.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 제거하기

인덱스에서 레코드를 제거하려면, 그냥 해당 모델을 데이터베이스에서 `delete`하면 됩니다. [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 사용하는 경우도 동일하게 동작합니다.

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

레코드를 삭제하기 전에 모델을 굳이 조회하지 않고 바로 삭제하고 싶다면, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용할 수 있습니다.

```php
Order::where('price', '>', 100)->unsearchable();
```

관계의 모든 모델에 대해 검색 인덱스에서 레코드를 제거하려면 관계 인스턴스에서 `unsearchable`을 호출하면 됩니다.

```php
$user->orders()->unsearchable();
```

또는 이미 메모리에 Eloquent 모델 컬렉션이 있다면, 그 컬렉션 인스턴스에서 `unsearchable` 메서드를 호출하여 각각의 인스턴스를 인덱스에서 제거할 수 있습니다.

```php
$orders->unsearchable();
```

모델의 모든 레코드를 인덱스에서 완전히 제거하려면, `removeAllFromSearch` 메서드를 사용하면 됩니다.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

때로는 모델 데이터를 검색 인덱스와 동기화하지 않고 Eloquent로 여러 작업을 일괄 처리하고 싶을 수 있습니다. 이때는 `withoutSyncingToSearch` 메서드를 사용하면 됩니다. 이 메서드는 하나의 클로저를 받아 즉시 실행하며, 해당 클로저 내에서 이뤄지는 모든 모델 작업은 인덱스에 동기화되지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 여기서 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 검색 가능한 모델 인스턴스

특정 조건일 때만 모델을 검색 가능하게 만들고 싶을 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft"(임시 저장)와 "published"(공개됨)라는 두 가지 상태를 가진다고 상상해보겠습니다. 이 중에서 "published" 상태의 글만 검색되도록 하고 싶은 경우, 모델에 `shouldBeSearchable` 메서드를 정의할 수 있습니다.

```php
/**
 * 이 모델이 검색 가능해야 하는지 결정합니다.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 `save`와 `create` 메서드, 쿼리, 관계를 통한 모델 작업 시에만 적용됩니다. 직접 모델이나 컬렉션에 `searchable`을 호출하면, `shouldBeSearchable`의 결과를 무시하고 무조건 검색 가능 상태가 됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진을 사용할 때는 적용되지 않습니다. 데이터베이스 엔진은 모든 검색 가능한 데이터를 항상 데이터베이스에 저장하기 때문입니다. 데이터베이스 엔진 환경에서 비슷한 효과를 내려면 [where 조건절](#where-clauses)을 사용하는 것이 좋습니다.

<a name="searching"></a>
## 검색하기

`search` 메서드를 사용해 모델 검색을 시작할 수 있습니다. 이 메서드는 검색어 문자열 하나를 인수로 받아 모델을 검색합니다. 이후 검색 쿼리 뒤에 `get` 메서드를 체이닝해서, 주어진 검색어에 해당하는 Eloquent 모델들을 가져올 수 있습니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이 반환되므로, 이를 라우트나 컨트롤러에서 그대로 반환하면 자동으로 JSON으로 변환됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Eloquent 모델로 변환되지 않은, 원시 검색 결과를 원하는 경우에는 `raw` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 지정

검색 쿼리는 보통 모델의 [searchableAs](#configuring-model-indexes) 메서드에서 지정한 인덱스에서 수행됩니다. 그러나 `within` 메서드를 사용하면 별도의 커스텀 인덱스를 지정해 검색할 수 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 조건절

Scout에서는 검색 쿼리에 간단한 "where" 조건절을 추가할 수 있습니다. 현재는 기본적인 숫자 값 일치(동등) 체크만 지원하며, 주로 소유자 ID로 검색 범위를 제한하고자 할 때 유용합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한, 해당 컬럼 값이 주어진 배열에 포함되어 있는지 확인할 때는 `whereIn` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

반대로, 컬럼 값이 주어진 배열에 포함되지 않았는지 확인하려면 `whereNotIn` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니므로, 더 복잡한 "where" 조건절은 현재 지원되지 않습니다.

> [!WARNING]
> 애플리케이션에서 Meilisearch를 사용한다면, Scout의 "where" 조건절을 사용하기 전에 애플리케이션의 [filterable attributes](#configuring-filterable-data-for-meilisearch)를 반드시 설정해야 합니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 조회하는 것 외에도, `paginate` 메서드를 사용해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [전통적인 Eloquent 쿼리](/docs/12.x/pagination)처럼 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 가져올 모델 개수를 첫 번째 인수로 지정할 수 있습니다.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 가져왔다면, [Blade](/docs/12.x/blade)를 통해 전통적인 Eloquent 페이지네이션처럼 결과를 출력하고 페이지 링크를 렌더링할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

물론, 페이지네이터 인스턴스를 라우트나 컨트롤러에서 반환하면 결과를 JSON형식으로 받을 수도 있습니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프 정의 내용을 알지 못하므로, Scout 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프를 사용하지 않는 것이 좋습니다. 꼭 사용해야 한다면, Scout를 이용한 검색 시 글로벌 스코프의 제약 조건을 별도로 다시 구현해 주세요.

<a name="soft-deleting"></a>
### 소프트 삭제(Soft Deleting)

인덱싱하는 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 사용하는 경우, 소프트 삭제된 모델을 검색 대상으로 포함시키려면 `config/scout.php` 설정 파일의 `soft_delete` 옵션을 `true`로 변경하면 됩니다.

```php
'soft_delete' => true,
```

이 옵션이 `true`일 때는, Scout가 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 인덱싱된 레코드에 숨겨진 `__soft_deleted` 속성을 추가해 표시해둡니다. 이제 검색 시 `withTrashed` 또는 `onlyTrashed` 메서드를 호출해 소프트 삭제된 레코드를 함께 조회할 수 있습니다.

```php
use App\Models\Order;

// 삭제된(휴지통) 레코드도 결과에 포함해서 가져오기...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된(휴지통) 레코드만 결과에 포함해서 가져오기...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제된 모델이 `forceDelete`를 사용해 완전히 삭제(영구 삭제)될 경우, Scout가 인덱스에서 해당 모델을 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 동작 커스터마이징

엔진의 검색 동작을 고급 커스터마이징해야 할 때는, `search` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백을 활용해 검색 쿼리를 Algolia로 전달하기 전에 지오로케이션(위치 기반) 데이터를 검색 옵션에 추가할 수 있습니다.

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

Scout가 검색 엔진으로부터 일치하는 Eloquent 모델 리스트를 받아온 뒤에는, Eloquent가 기본키로 실제 모델 데이터를 조회합니다. 이때 사용할 쿼리를 커스터마이징하고 싶다면, `query` 메서드로 클로저를 넘겨주면 됩니다. 이 클로저에는 Eloquent 쿼리 빌더 인스턴스가 인수로 전달됩니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 검색 엔진에서 관련 모델이 모두 조회된 다음에 실행되므로, 결과 "필터링" 용도가 아니라 추가적인 쿼리 커스터마이징 용도로만 사용해야 합니다. 결과 필터링이 필요하다면 [Scout where 조건절](#where-clauses)을 사용하세요.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 직접 작성하기

Scout에 내장된 검색 엔진이 요구사항에 맞지 않는다면, 직접 커스텀 엔진을 작성하여 Scout에 등록할 수 있습니다. 새로운 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 하며, 이 추상 클래스에는 반드시 구현해야 할 8개의 메서드가 있습니다.

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

각 메서드를 실제로 구현하는 예시는 `Laravel\Scout\Engines\AlgoliaEngine` 클래스에서 참고하는 것이 좋습니다. 이 클래스의 예제를 살펴보면 각 메서드를 어떻게 구현할지 파악하는 데 많은 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진을 작성했다면, Scout의 엔진 매니저의 `extend` 메서드를 통해 등록할 수 있습니다. Scout 엔진 매니저는 라라벨 서비스 컨테이너에서 `resolve`로 가져올 수 있습니다. 엔진 등록은 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드(또는 다른 서비스 프로바이더의 `boot` 메서드) 안에서 처리합니다.

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

이제 엔진이 등록되었으니, 애플리케이션의 `config/scout.php` 설정 파일에서 기본 Scout `driver`로 사용할 엔진 명을 지정해주면 됩니다.

```php
'driver' => 'mysql',
```