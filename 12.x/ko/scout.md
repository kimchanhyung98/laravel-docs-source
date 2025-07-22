# 라라벨 스카우트 (Laravel Scout)

- [소개](#introduction)
- [설치](#installation)
    - [큐잉](#queueing)
- [드라이버 사전 준비 사항](#driver-prerequisites)
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
    - [배치 가져오기](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 업데이트](#updating-records)
    - [레코드 삭제](#removing-records)
    - [인덱싱 일시중지](#pausing-indexing)
    - [조건부로 인덱싱할 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색하기](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이징](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/12.x/eloquent)에 전체 텍스트 검색 기능을 추가할 수 있도록, 드라이버 기반의 간단한 솔루션을 제공합니다. 모델 옵저버를 사용하여 Scout가 Eloquent 레코드와 검색 인덱스가 항상 동기화되도록 자동으로 관리합니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), MySQL / PostgreSQL (`database`) 드라이버를 제공합니다. 이외에도, Scout에는 외부 의존성이나 서드 파티 서비스 없이 로컬 개발에서 사용할 수 있도록 설계된 "컬렉션" 드라이버가 포함되어 있습니다. 또한, 직접 커스텀 드라이버를 작성하는 것도 매우 간단하므로, 본인만의 검색 구현 방식으로 Scout를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

우선, Composer 패키지 매니저를 사용해 Scout를 설치합니다.

```shell
composer require laravel/scout
```

Scout를 설치한 후, `vendor:publish` 아티즌 명령어를 이용해 Scout 설정 파일을 배포해야 합니다. 이 명령은 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉토리에 생성합니다.

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 기능을 추가하고자 하는 모델에 `Laravel\Scout\Searchable` 트레이트를 추가합니다. 이 트레이트는 검색 드라이버와 모델의 동기화를 자동으로 관리하는 모델 옵저버를 등록합니다.

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

Scout를 사용하기 위해 반드시 필요한 것은 아니지만, 라이브러리를 사용하기 전에 [큐 드라이버](/docs/12.x/queues)를 설정하는 것을 강력히 권장합니다. 큐 워커를 실행하면, 모델 정보를 검색 인덱스에 동기화하는 모든 작업이 큐로 처리되어, 웹 인터페이스의 반응 속도가 크게 향상됩니다.

큐 드라이버를 설정한 후에는 `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 변경합니다.

```php
'queue' => true,
```

`queue` 옵션을 `false`로 설정해도, Algolia나 Meilisearch처럼 일부 Scout 드라이버는 항상 비동기적으로 레코드를 인덱싱한다는 점을 기억해야 합니다. 즉, 라라벨 애플리케이션 내에서 인덱싱 작업이 완료되어도, 검색 엔진에서 새로운 또는 수정된 레코드가 바로 반영되지 않을 수 있습니다.

Scout 작업이 사용할 커넥션과 큐를 지정하려면, `queue` 설정 옵션을 배열로 지정할 수 있습니다.

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```

물론, 커넥션과 큐를 커스터마이징했다면 해당 커넥션과 큐에서 작업을 처리하도록 큐 워커를 실행해야 합니다.

```shell
php artisan queue:work redis --queue=scout
```

<a name="driver-prerequisites"></a>
## 드라이버 사전 준비 사항

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는, `config/scout.php` 설정 파일에서 Algolia의 `id`와 `secret` 자격 증명을 반드시 입력해야 합니다. 자격 증명을 설정한 후에는, Composer 패키지 매니저로 Algolia PHP SDK를 설치해야 합니다.

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬 컴퓨터에 Meilisearch를 설치하는 방법을 잘 모를 경우, [Laravel Sail](/docs/12.x/sail#meilisearch), 즉 공식 Docker 개발 환경을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 경우, Composer를 통해 Meilisearch PHP SDK를 설치해야 합니다.

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

애플리케이션의 `.env` 파일에 `SCOUT_DRIVER` 환경 변수와 함께 Meilisearch `host`, `key` 자격증명을 지정해 주세요.

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 추가 정보는 [Meilisearch 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하십시오.

또한, `meilisearch/meilisearch-php`의 버전이 실제 Meilisearch 바이너리 버전과 호환되는지, [Meilisearch의 바이너리 호환 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 통해 반드시 확인하시기 바랍니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때는 반드시 Meilisearch 서비스 자체에 대해 [추가적인 변경사항](https://github.com/meilisearch/Meilisearch/releases)을 확인해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈 소스 검색 엔진으로, 키워드 검색, 시맨틱 검색, 지오 검색, 벡터 검색을 지원합니다.

[직접 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)을 하거나, [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치해 주세요.

```shell
composer require typesense/typesense-php
```

그리고 애플리케이션의 .env 파일에 `SCOUT_DRIVER` 환경 변수, Typesense의 host 및 API key 자격증명을 추가합니다.

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/12.x/sail)을 사용하는 경우, Docker 컨테이너 이름을 기반으로 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수 있습니다. 설치의 port, path, protocol 값을 선택적으로 지정할 수도 있습니다.

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정 및 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 확인할 수 있습니다. 자세한 옵션은 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참고 바랍니다.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense에 저장할 데이터 준비

Typesense를 사용할 때는, 검색 대상 모델에 `toSearchableArray` 메서드를 정의하여 모델의 기본 키를 문자열로, 생성일자를 UNIX 타임스탬프로 캐스팅해야 합니다.

```php
/**
 * 모델의 인덱스 대상 데이터 배열을 반환합니다.
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

또한, Typesense 컬렉션 스키마를 애플리케이션의 `config/scout.php` 파일에 정의해야 합니다. 컬렉션 스키마는 Typesense를 통해 검색되는 각 필드의 데이터 타입을 나타냅니다. 스키마에서 설정 가능한 옵션에 대한 자세한 내용은 [Typesense API 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 수정해야 하는 경우, `scout:flush` 및 `scout:import`를 실행하여 기존 인덱스된 데이터를 모두 삭제 후 스키마를 다시 생성할 수 있습니다. 또는 Typesense API를 이용해 인덱스된 데이터는 그대로 두고 컬렉션의 스키마만 변경할 수도 있습니다.

소프트 삭제 가능한 모델의 경우, 모델의 Typesense 스키마에 `__soft_deleted` 필드를 반드시 정의해야 합니다.

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

Typesense에서는 검색 작업을 수행할 때 `options` 메서드를 사용하여 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 지정할 수 있습니다.

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

각 Eloquent 모델은 해당 모델의 모든 검색 가능 레코드를 담는 특정 검색 "인덱스"와 동기화됩니다. 쉽게 말하면, 각 인덱스는 MySQL 테이블과 유사하다고 생각할 수 있습니다. 기본적으로 각 모델은 일반적으로 "테이블" 이름과 일치하는 인덱스에 저장됩니다. 보통 모델의 복수형 이름이 사용됩니다. 하지만, 모델의 `searchableAs` 메서드를 오버라이드하여 인덱스 명을 자유롭게 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델과 연관된 인덱스의 이름을 반환합니다.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```

<a name="configuring-searchable-data"></a>
### 검색 데이터 설정

기본적으로 모델의 `toArray` 결과 전체가 검색 인덱스에 저장됩니다. 인덱스에 동기화할 데이터를 직접 지정하고 싶다면, 모델에서 `toSearchableArray` 메서드를 오버라이드하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * 모델의 인덱스 대상 데이터 배열을 반환합니다.
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

Meilisearch와 같은 일부 검색 엔진에서는 필터링 연산(`>`, `<` 등)이 올바른 타입의 데이터에만 적용됩니다. 따라서 이런 엔진을 사용할 때에는, 검색 데이터 커스터마이즈 과정에서 숫자 값은 반드시 올바른 타입으로 캐스팅해 주어야 합니다.

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

때때로 Algolia 인덱스에 추가적인 설정을 하고 싶은 경우가 있습니다. 이 설정들은 Algolia UI에서 직접 관리할 수도 있지만, 애플리케이션의 `config/scout.php` 파일에서 직접 관리하는 것이 더 효율적일 수 있습니다.

이 방법을 사용하면 애플리케이션의 CI/CD(자동 배포 파이프라인)에서 인덱스 설정 배포가 가능하며, 수동 작업 없이 여러 환경에서도 설정 일관성을 유지할 수 있습니다. 필터링 속성, 랭킹, 페이싱 등 [지원되는 모든 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 지정할 수 있습니다.

시작하려면, 각 인덱스별 설정을 `config/scout.php` 파일에 추가하세요.

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

특정 인덱스의 모델이 소프트 삭제 기능을 가지고 있고, `index-settings` 배열에 포함되어 있다면, Scout는 해당 인덱스에서 소프트 삭제 모델에 대한 페이싱도 자동으로 지원합니다. 소프트 삭제 모델에서 특별히 지정할 페이싱 속성이 없다면, 아래와 같이 빈 항목만 추가해도 됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

애플리케이션의 인덱스 설정을 변경한 후에는 `scout:sync-index-settings` 아티즌 명령어를 실행해야 합니다. 이 명령은 Algolia에 현재 설정을 동기화합니다. 배포 자동화 과정의 일부로 이 명령을 실행하는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### 필터링 데이터 및 인덱스 설정 (Meilisearch)

Scout의 다른 드라이버와 달리 Meilisearch는 필터링 속성, 정렬 속성 등 [지정 가능한 인덱스 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 사전에 정의해야 합니다.

필터링 속성은 Scout의 `where` 메서드로 필터링하고자 하는 모든 속성이고, 정렬 속성은 `orderBy` 메서드로 정렬하고자 하는 모든 속성입니다. 인덱스 설정을 정의하려면, 애플리케이션의 scout 설정 파일의 `meilisearch` 항목에서 `index-settings` 부분을 조정하면 됩니다.

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

특정 인덱스의 모델이 소프트 삭제 기능을 가지고 있고, `index-settings` 배열에 포함되어 있다면, Scout는 해당 인덱스에서 소프트 삭제 모델에 대한 필터링도 자동으로 지원합니다. 소프트 삭제 모델에서 특별히 지정할 필터링 또는 정렬 속성이 없다면, 아래와 같이 빈 항목만 추가해도 됩니다.

```php
'index-settings' => [
    Flight::class => []
],
```

설정을 완료한 후에는 반드시 `scout:sync-index-settings` 아티즌 명령어를 실행해야 하며, 이 명령은 Meilisearch 인덱스 설정을 동기화합니다. 배포 자동화 과정의 일부로 이 명령을 실행하는 것이 좋습니다.

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키(primary key)를 검색 인덱스에 저장할 모델의 고유 ID/키로 사용합니다. 이 동작을 커스터마이즈하려면, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 오버라이드하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * 모델 인덱싱에 사용할 값을 반환합니다.
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

보통 Scout는 애플리케이션의 `scout` 설정 파일에 명시된 기본 검색 엔진을 사용합니다. 그러나 특정 모델에 대해 검색 엔진을 변경하고 싶다면, 해당 모델의 `searchableUsing` 메서드를 오버라이드할 수 있습니다.

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
     * 모델을 인덱싱할 때 사용할 엔진을 반환합니다.
     */
    public function searchableUsing(): Engine
    {
        return app(EngineManager::class)->engine('meilisearch');
    }
}
```

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시, 검색 작업에 인증된 사용자를 자동으로 식별해주기도 합니다. 사용자 식별 기능을 활성화하면 Algolia 대시보드에서 검색 분석을 할 때 유용합니다. 애플리케이션의 `.env` 파일에 `SCOUT_IDENTIFY` 환경 변수를 `true`로 지정하면 이 기능을 사용할 수 있습니다.

```ini
SCOUT_IDENTIFY=true
```

이 기능이 활성화되면, 요청의 IP 주소와 인증된 사용자의 주요 식별자가 Algolia에 전달되어, 해당 사용자가 만든 검색 요청과 데이터가 연관됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

애플리케이션이 소규모 또는 중간 규모의 데이터베이스와 연동하거나, 작업량이 적다면, Scout의 "database" 엔진을 사용하는 것이 더욱 편리할 수 있습니다. 데이터베이스 엔진은 기본적으로 "where like" 절과 전체 텍스트 인덱스를 조합하여, 기존 데이터베이스에서 결과를 필터링해 검색 결과를 도출합니다.

데이터베이스 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수 값을 `database`로 설정하거나, `scout` 설정 파일에서 직접 `database` 드라이버를 명시하면 됩니다.

```ini
SCOUT_DRIVER=database
```

데이터베이스 엔진을 선호 드라이버로 지정한 뒤에는 [검색 데이터 설정](#configuring-searchable-data)을 완료하세요. 그 다음, 모델에서 [검색 쿼리 실행](#searching) 이 바로 가능합니다. Algolia, Meilisearch, Typesense와는 달리, 인덱싱(예: 검색 엔진별로 데이터를 따로 미리 등록하는 작업)이 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이징

기본적으로 데이터베이스 엔진은 [검색 필드로 설정한](#configuring-searchable-data) 모든 모델 속성에 대해 "where like" 쿼리를 실행합니다. 하지만 경우에 따라 이 방식은 성능에 좋지 않은 영향을 미칠 수 있습니다. 이럴 때는 일부 컬럼만 전체 텍스트 검색으로 처리한다거나, 혹은 문자열의 일부(접두사, 예: `example%`)만을 대상으로 하여 LIKE 조건을 적용하도록 검색 전략을 지정할 수 있습니다.

이 동작을 지정하려면, 모델의 `toSearchableArray` 메서드에 PHP 속성을 할당하면 됩니다. 별도로 전략을 지정하지 않은 컬럼은 여전히 기본 "where like" 전략을 사용합니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델의 인덱스 대상 데이터 배열을 반환합니다.
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
> 특정 컬럼에 전체 텍스트 쿼리 제한을 두려면, 해당 컬럼에 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 반드시 있어야 합니다.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발에서도 Algolia, Meilisearch, Typesense와 같은 검색 엔진을 사용할 수 있지만, "collection" 엔진으로 시작하는 것이 더 편리할 수 있습니다. 컬렉션 엔진은 기존 데이터베이스에서 "where" 절과 컬렉션 필터링을 사용해 검색 결과를 구합니다. 이 엔진을 사용할 경우, 별도의 인덱싱 작업 없이 데이터베이스에서 바로 모델을 가져옵니다.

컬렉션 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수를 `collection`으로 설정하거나, `scout` 설정 파일에서 직접 `collection` 드라이버를 명시하면 됩니다.

```ini
SCOUT_DRIVER=collection
```

컬렉션 드라이버가 선호 드라이버로 지정된 후에는, 모델에서 [검색 쿼리 실행](#searching)이 바로 가능합니다. 이 엔진 역시 Algolia, Meilisearch, Typesense처럼 별도의 인덱싱 작업 없이 사용할 수 있습니다.

#### 데이터베이스 엔진과의 차이점

언뜻 보면 "database"와 "collections" 엔진은 매우 비슷해 보입니다. 둘 다 데이터베이스에서 직접 검색 결과를 가져오지만, 컬렉션 엔진은 전체 텍스트 인덱스나 LIKE 쿼리를 사용하지 않습니다. 모든 가능한 레코드를 가져온 후, Laravel의 `Str::is` 헬퍼로 속성 값에 검색 문자열이 포함되어 있는지를 검사합니다.

컬렉션 엔진은 모든 Laravel 지원 관계형 데이터베이스(예: SQLite, SQL Server)에서도 작동하는 가장 이식성이 높은 엔진이지만, Scout의 데이터베이스 엔진보다는 효율이 떨어집니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 가져오기

기존 프로젝트에 Scout를 적용하는 경우, 이미 존재하는 데이터베이스 레코드를 인덱스에 가져와야 할 수 있습니다. Scout는 이를 위해 `scout:import` 아티즌 명령어를 제공합니다. 이 명령을 통해 해당 모델의 모든 레코드를 검색 인덱스에 등록할 수 있습니다.

```shell
php artisan scout:import "App\Models\Post"
```

`scout:queue` 명령을 사용하면 [큐 작업](/docs/12.x/queues)으로 대량의 기존 레코드를 가져올 수 있습니다.

```shell
php artisan scout:queue "App\Models\Post" --chunk=500
```

`flush` 명령은 모델의 모든 레코드를 검색 인덱스에서 제거할 때 사용합니다.

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정

모델 전체를 가져올 때 사용할 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 이 메서드는 예를 들어, 가져오기 전에 반드시 eager 로드되어야 하는 연관관계가 있을 때 유용합니다.

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * 모든 모델을 검색 대상으로 만들 때 사용할 쿼리를 수정합니다.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```

> [!WARNING]
> `makeAllSearchableUsing` 메서드는 큐를 사용해 모델을 배치 가져올 경우에는 동작하지 않을 수 있습니다. 큐로 모델 컬렉션을 처리할 때 연관관계는 [복원되지 않습니다](/docs/12.x/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

`Laravel\Scout\Searchable` 트레이트를 모델에 추가하면, `save`나 `create`로 모델 인스턴스를 저장하기만 해도 자동으로 검색 인덱스에 등록됩니다. [큐를 사용하도록 설정했다면](#queueing) 이 작업은 백그라운드에서 큐 워커가 처리합니다.

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```

<a name="adding-records-via-query"></a>
#### 쿼리로 레코드 추가

Eloquent 쿼리를 사용해 여러 모델 컬렉션을 인덱스에 추가하고 싶다면, `searchable` 메서드를 쿼리 뒤에 연결하세요. 이 메서드는 쿼리 결과를 [청크 단위로](https://laravel.kr/docs/12.x/eloquent#chunking-results) 나누어 인덱스에 추가합니다. 역시 큐가 설정되어 있다면 모든 청크가 백그라운드에서 처리됩니다.

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```

Eloquent 관계 인스턴스에서도 바로 `searchable`을 호출할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 Eloquent 모델 컬렉션을 메모리에 가지고 있다면, 해당 컬렉션 인스턴스에서 직접 `searchable`을 호출해 바로 인덱스에 추가할 수 있습니다.

```php
$orders->searchable();
```

> [!NOTE]
> `searchable` 메서드는 일종의 "upsert" 동작입니다. 즉, 모델 레코드가 이미 인덱스에 있으면 업데이트되고, 없으면 인덱스에 새로 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 인스턴스의 속성을 수정한 후 데이터베이스에 `save` 하면 됩니다. Scout가 자동으로 인덱스에도 변경 내용을 반영합니다.

```php
use App\Models\Order;

$order = Order::find(1);

// 주문을 수정하고...

$order->save();
```

Eloquent 쿼리 인스턴스에서 바로 `searchable`을 호출해 여러 모델을 업데이트할 수도 있습니다. 인덱스에 없는 모델은 새로 생성됩니다.

```php
Order::where('price', '>', 100)->searchable();
```

특정 관계의 모든 모델을 한 번에 인덱스에 업데이트하려면, 관계 인스턴스에서 `searchable`을 사용할 수 있습니다.

```php
$user->orders()->searchable();
```

이미 컬렉션 형태로 모델을 가지고 있다면, 컬렉션에서 `searchable`을 호출해 각 인스턴스를 인덱스에 업데이트하면 됩니다.

```php
$orders->searchable();
```

<a name="modifying-records-before-importing"></a>
#### 인덱싱 전 레코드 수정

검색에 임포트하기 전, 컬렉션의 모델을 사전 준비해야 하는 경우가 있습니다. 예를 들어, 인덱스에 효율적으로 추가할 수 있도록 연관관계 데이터를 eager 로드할 때가 그렇습니다. 이럴 땐, 해당 모델에 `makeSearchableUsing` 메서드를 정의합니다.

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * 검색 가능한 모델로 만들 때 컬렉션을 수정합니다.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```

<a name="removing-records"></a>
### 레코드 삭제

검색 인덱스에서 레코드를 삭제하려면, 데이터베이스에서 모델을 `delete` 하기만 하면 됩니다. [소프트 삭제](/docs/12.x/eloquent#soft-deleting) 가능한 모델도 동일하게 처리할 수 있습니다.

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```

모델을 직접 찾지 않고 레코드를 삭제하고 싶다면, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용하면 됩니다.

```php
Order::where('price', '>', 100)->unsearchable();
```

특정 관계에 포함된 모든 모델의 인덱스를 삭제하고 싶다면, 관계 인스턴스에서 `unsearchable`을 호출하세요.

```php
$user->orders()->unsearchable();
```

이미 컬렉션으로 모델을 갖고 있다면, 컬렉션 인스턴스에서 `unsearchable`을 호출해 해당 인스턴스를 인덱스에서 제거할 수 있습니다.

```php
$orders->unsearchable();
```

인덱스에서 모든 레코드를 한 번에 제거하려면, `removeAllFromSearch` 메서드를 사용합니다.

```php
Order::removeAllFromSearch();
```

<a name="pausing-indexing"></a>
### 인덱싱 일시중지

가끔 여러 Eloquent 작업을 한 번에 수행하되, 이 작업 동안에는 검색 인덱스와 동기화를 하지 않길 원할 때가 있습니다. 이럴 때는 `withoutSyncingToSearch` 메서드를 이용하세요. 이 메서드는 하나의 클로저를 인자로 받아 바로 실행하며, 클로저 내의 모델 작업은 인덱스와 동기화하지 않습니다.

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // 모델 작업 수행...
});
```

<a name="conditionally-searchable-model-instances"></a>
### 조건부로 인덱싱할 모델 인스턴스

특정 조건에서만 모델을 검색 가능하게 해야 할 때가 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft"(초안) 또는 "published"(게시됨) 상태일 수 있고, "published" 상태만 검색 대상이 되길 원할 수 있습니다. 이럴 때는 모델에 `shouldBeSearchable` 메서드를 정의합니다.

```php
/**
 * 모델이 검색 대상이 될지 여부를 반환합니다.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```

`shouldBeSearchable` 메서드는 모델을 `save`, `create`, 쿼리, 관계 등으로 조작할 때만 적용됩니다. 직접적으로 모델이나 컬렉션에서 `searchable` 메서드를 호출하는 경우, `shouldBeSearchable`의 반환값을 무시하게 됩니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에는 적용되지 않습니다. 이 엔진을 사용할 때는 모든 검색 데이터가 항상 데이터베이스에 저장되기 때문입니다. 유사한 동작이 필요하다면 [where 절](#where-clauses)을 사용하세요.

<a name="searching"></a>
## 검색하기

모델에 대해 검색을 시작하려면 `search` 메서드를 사용하면 됩니다. 이 메서드는 검색할 문자열을 인자로 받고, 그 후 `get` 메서드를 연결해 검색 결과에 해당하는 Eloquent 모델 컬렉션을 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```

Scout 검색 결과는 Eloquent 모델 컬렉션이기 때문에, 라우트 또는 컨트롤러에서 바로 반환하면 자동으로 JSON으로 변환됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```

Eloquent 모델로 변환되기 전, 원시 검색 결과를 그대로 받고 싶다면 `raw` 메서드를 사용할 수 있습니다.

```php
$orders = Order::search('Star Trek')->raw();
```

<a name="custom-indexes"></a>
#### 커스텀 인덱스 사용

검색 쿼리는 기본적으로 모델의 [searchableAs](#configuring-model-indexes) 메서드에서 지정된 인덱스에 대해 실행됩니다. 그러나, `within` 메서드를 사용해 원하는 커스텀 인덱스를 지정할 수도 있습니다.

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있도록 지원합니다. 현재로서는 숫자 값의 equals(동등) 비교만 지원하며, 주로 소유자 ID로 범위를 제한할 때 유용합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

또한, `whereIn` 메서드를 사용하면 컬럼 값이 특정 배열 안에 포함되어 있는지 확인할 수 있습니다.

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```

`whereNotIn` 메서드는 해당 컬럼 값이 주어진 배열에 포함되어 있지 않은 레코드만 조회합니다.

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```

검색 인덱스는 관계형 데이터베이스가 아니기 때문에, 위에서 설명한 것 외의 복잡한 "where" 절은 현재 지원되지 않습니다.

> [!WARNING]
> Meilisearch를 사용하는 경우, Scout의 "where" 절을 사용하기 전 반드시 [필터링 가능한 속성](#configuring-filterable-data-for-meilisearch)을 설정해야 합니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 단순히 조회하는 것 외에도, `paginate` 메서드를 통해 검색 결과를 페이지네이션할 수 있습니다. 이 메서드는 [기존 Eloquent 쿼리에서 페이지네이션한 것](/docs/12.x/pagination)처럼 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```

페이지당 표시할 모델 개수를 첫 번째 인자로 지정할 수 있습니다.

```php
$orders = Order::search('Star Trek')->paginate(15);
```

결과를 받은 후, [Blade](/docs/12.x/blade)에서 페이지네이션 결과와 링크 렌더링도 Eloquent와 동일하게 할 수 있습니다.

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 받아오길 원한다면, 라우트나 컨트롤러에서 바로 페이징 인스턴스를 반환하면 됩니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프 처리를 인지하지 못하기 때문에, Scout의 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프 사용을 자제해야 합니다. 또는, Scout로 검색할 때 글로벌 스코프의 조건을 별도로 재현하도록 해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

인덱스된 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting) 기능을 사용 중이고, 소프트 삭제 모델까지 함께 검색하고 싶다면 `config/scout.php` 설정 파일의 `soft_delete` 옵션을 `true`로 지정하세요.

```php
'soft_delete' => true,
```

이 옵션이 `true`일 때 Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않고, 인덱스에 숨겨진 `__soft_deleted` 속성을 설정합니다. 이후 `withTrashed` 또는 `onlyTrashed` 메서드를 사용해 검색 시 소프트 삭제 레코드를 포함하거나, 이것만 조회할 수 있습니다.

```php
use App\Models\Order;

// 검색 결과에 삭제된 레코드를 포함...
$orders = Order::search('Star Trek')->withTrashed()->get();

// 삭제된 레코드만 반환...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

> [!NOTE]
> 소프트 삭제 모델을 `forceDelete`로 완전히 삭제하면, Scout가 자동으로 인덱스에서 이를 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이징

검색 엔진의 동작을 더욱 세밀하게 커스터마이징해야 할 경우, `search` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백을 이용해 검색 쿼리가 Algolia로 전달되기 전에 지오로케이션 데이터를 추가할 수 있습니다.

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

Scout가 검색 엔진에서 일치하는 Eloquent 모델의 기본 키 목록을 받아오고 나면, Eloquent로 실제 모델을 모두 조회합니다. 이 쿼리를 더 커스터마이즈하려면 `query` 메서드를 사용하세요. `query` 메서드는 Eloquent 쿼리 빌더 인스턴스를 인자로 받는 클로저를 허용합니다.

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 일치하는 모델의 기본 키가 검색 엔진에서 이미 결정된 이후에 실행되므로, 필터링 목적으로 사용하면 안 됩니다. 이런 경우엔 [Scout의 where 절](#where-clauses)을 사용해야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성하기

기본 제공되는 Scout 검색 엔진으로 만족할 수 없다면, 직접 커스텀 엔진을 작성하여 Scout에 등록할 수 있습니다. 자신이 만든 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속해야 합니다. 이 추상 클래스에는 반드시 구현해야 하는 여덟 개의 메서드가 있습니다.

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

이 메서드들의 실제 구현이 궁금하다면, `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 큰 도움이 됩니다. 이 클래스는 각 메서드를 어떻게 구현해야 할지 구체적으로 보여주는 좋은 예시입니다.

<a name="registering-the-engine"></a>
#### 엔진 등록하기

커스텀 엔진을 작성해 완성했다면, Scout 엔진 매니저의 `extend` 메서드를 사용해 Scout에 등록할 수 있습니다. 엔진 매니저는 라라벨 서비스 컨테이너에서 해결할 수 있습니다. `App\Providers\AppServiceProvider`의 `boot` 메서드, 또는 애플리케이션에서 사용하는 다른 서비스 제공자에서 `extend`를 호출하세요.

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

이제 엔진을 등록했다면, 애플리케이션의 `config/scout.php` 설정 파일에서 Scout의 기본 `driver`로 지정해 사용할 수 있습니다.

```php
'driver' => 'mysql',
```