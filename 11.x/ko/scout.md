# Laravel Scout

- [소개](#introduction)
- [설치](#installation)
    - [큐 사용](#queueing)
- [드라이버 필수 조건](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [설정](#configuration)
    - [모델 인덱스 설정](#configuring-model-indexes)
    - [검색 대상 데이터 설정](#configuring-searchable-data)
    - [모델 ID 설정](#configuring-the-model-id)
    - [모델별 검색 엔진 설정](#configuring-search-engines-per-model)
    - [사용자 식별](#identifying-users)
- [데이터베이스 / 컬렉션 엔진](#database-and-collection-engines)
    - [데이터베이스 엔진](#database-engine)
    - [컬렉션 엔진](#collection-engine)
- [인덱싱](#indexing)
    - [배치 임포트](#batch-import)
    - [레코드 추가](#adding-records)
    - [레코드 수정](#updating-records)
    - [레코드 제거](#removing-records)
    - [인덱싱 일시 중지](#pausing-indexing)
    - [조건부 검색 모델 인스턴스](#conditionally-searchable-model-instances)
- [검색](#searching)
    - [Where 절](#where-clauses)
    - [페이지네이션](#pagination)
    - [소프트 삭제](#soft-deleting)
    - [엔진 검색 커스터마이즈](#customizing-engine-searches)
- [커스텀 엔진](#custom-engines)

<a name="introduction"></a>
## 소개

[Laravel Scout](https://github.com/laravel/scout)는 [Eloquent 모델](/docs/{{version}}/eloquent)에 전체 텍스트 검색을 쉽게 추가할 수 있도록 드라이버 기반의 간단한 솔루션을 제공합니다. 모델 옵저버를 활용하여, Scout는 여러분의 Eloquent 레코드와 검색 인덱스를 자동으로 동기화해줍니다.

현재 Scout는 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 MySQL / PostgreSQL(`database`) 드라이버를 기본으로 제공합니다. 또한, Scout에는 외부 의존성이나 서드파티 서비스가 필요 없는 로컬 개발용 "collection" 드라이버도 포함되어 있습니다. 더욱이, 커스텀 드라이버 작성도 간단하여 직접 원하는 검색 구현을 확장하여 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 통해 Scout를 설치하세요:

```shell
composer require laravel/scout
```

설치 후, `vendor:publish` Artisan 명령어를 사용하여 Scout 설정 파일을 퍼블리시해야 합니다. 이 명령어는 `scout.php` 설정 파일을 애플리케이션의 `config` 디렉터리로 복사합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

마지막으로, 검색 대상 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델의 변경 사항이 검색 드라이버와 자동으로 동기화될 수 있도록 옵저버를 등록합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;
    }

<a name="queueing"></a>
### 큐 사용

Scout를 사용하는 데 필수는 아니지만, 라이브러리 도입 전 [큐 드라이버](/docs/{{version}}/queues) 설정을 적극 권장합니다. 큐 워커를 실행하면 모델 정보를 검색 인덱스와 동기화하는 모든 작업을 큐잉할 수 있어 웹 인터페이스의 응답 시간이 크게 개선됩니다.

큐 드라이버를 설정했다면 `config/scout.php` 설정 파일의 `queue` 옵션 값을 `true`로 지정하세요:

    'queue' => true,

`queue` 옵션이 `false`로 되어 있더라도, Algolia와 Meilisearch와 같은 일부 Scout 드라이버는 항상 비동기로 인덱싱을 처리한다는 점을 기억하세요. 즉, Laravel 애플리케이션 내에서 인덱스 작업이 끝나더라도 실제 검색 엔진에서는 즉시 반영되지 않을 수 있습니다.

Scout job에서 사용할 연결(connection) 및 큐(queue)를 지정하려면 `queue` 옵션을 배열로 정의할 수 있습니다:

    'queue' => [
        'connection' => 'redis',
        'queue' => 'scout'
    ],

이처럼 연결 및 큐를 커스터마이즈하면, 해당 큐에서 job을 처리할 워커를 실행해야 합니다:

    php artisan queue:work redis --queue=scout

<a name="driver-prerequisites"></a>
## 드라이버 필수 조건

<a name="algolia"></a>
### Algolia

Algolia 드라이버 사용 시, `config/scout.php` 설정 파일에 Algolia의 `id`와 `secret` 자격 증명을 입력해야 합니다. 자격 증명 입력 후 Composer로 Algolia PHP SDK도 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 매우 빠르고 오픈 소스인 검색 엔진입니다. 로컬에 Meilisearch를 설치하는 방법을 모르겠다면 [Laravel Sail](/docs/{{version}}/sail#meilisearch), 즉 공식적인 도커 개발 환경을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 때는 Composer로 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

그리고 애플리케이션의 `.env` 파일에서 `SCOUT_DRIVER` 환경 변수와 Meilisearch의 `host`, `key` 자격 증명을 지정합니다:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```

Meilisearch에 대한 자세한 사항은 [Meilisearch 공식 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참고하세요.

또한, [Meilisearch의 바이너리 호환성 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 참고하여 사용하는 Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 버전을 설치해야 합니다.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 경우, 반드시 [Meilisearch 서비스의 주요 변경점](https://github.com/meilisearch/Meilisearch/releases)을 검토해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 고속의 오픈소스 검색 엔진으로, 키워드 검색, 시맨틱 검색, 지오 검색, 벡터 검색을 지원합니다.

[셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) 또는 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer로 Typesense PHP SDK를 설치하세요:

```shell
composer require typesense/typesense-php
```

그리고 애플리케이션의 .env 파일에 `SCOUT_DRIVER` 환경 변수와 Typesense 호스트 및 API 키를 지정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```

[Laravel Sail](/docs/{{version}}/sail)을 사용하는 경우, Docker 컨테이너 이름에 맞게 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수 있습니다. 또한 설치된 포트, 경로 및 프로토콜도 선택적으로 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```

Typesense 컬렉션의 추가 설정과 스키마 정의는 애플리케이션의 `config/scout.php` 설정 파일에서 할 수 있습니다. 더 많은 정보는 [Typesense 공식 문서](https://typesense.org/docs/guide/#quick-start)를 참고하세요.

<a name="preparing-data-for-storage-in-typesense"></a>
#### Typesense 저장을 위한 데이터 준비

Typesense를 사용할 경우, 검색 가능한 모델에 반드시 `toSearchableArray` 메서드를 정의하여 모델의 기본 키는 문자열로, 생성 일자는 UNIX 타임스탬프로 변환해야 합니다:

```php
/**
 * 모델의 인덱싱 가능한 데이터 배열 반환.
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

Typesense 컬렉션 스키마도 애플리케이션의 `config/scout.php` 파일에 정의해야 합니다. 컬렉션 스키마는 Typesense에서 검색할 수 있는 각 필드의 데이터 타입을 지정합니다. 사용 가능한 모든 스키마 옵션은 [Typesense 공식 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참고하세요.

스키마를 변경해야 한다면, `scout:flush`와 `scout:import`를 실행해서 기존 데이터를 삭제하고 스키마를 재생성하거나, Typesense API를 이용해 데이터 삭제 없이 스키마를 변경할 수 있습니다.

모델이 소프트 삭제 가능한 경우, 해당 모델의 Typesense 스키마에 `__soft_deleted` 필드를 정의해야 합니다:

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
#### 다이내믹 검색 파라미터

Typesense는 검색 작업을 수행할 때 `options` 메서드를 통해 [검색 파라미터](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 수정할 수 있습니다:

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

각 Eloquent 모델은 해당 모델의 모든 검색 가능 레코드를 포함하는 검색 "인덱스"와 동기화됩니다. 즉, 각 인덱스를 MySQL의 테이블과 비슷하게 생각할 수 있습니다. 기본적으로, 각 모델은 모델의 보통 "테이블" 이름과 일치하는 인덱스로 저장됩니다. 일반적으로는 복수형 모델명입니다. 하지만 `searchableAs` 메서드를 오버라이드하여 원하는 인덱스 이름을 지정할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델과 관련된 인덱스 이름 반환.
         */
        public function searchableAs(): string
        {
            return 'posts_index';
        }
    }

<a name="configuring-searchable-data"></a>
### 검색 대상 데이터 설정

기본적으로, 모델의 `toArray` 전체 결과가 검색 인덱스로 저장됩니다. 어떤 데이터만 검색 인덱스에 동기화할지 지정하려면 `toSearchableArray` 메서드를 오버라이드하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class Post extends Model
    {
        use Searchable;

        /**
         * 모델 인덱싱용 데이터 배열 반환.
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

Meilisearch와 같은 일부 검색 엔진은 필터 연산(`>`, `<` 등)을 제대로 타입이 지정된 데이터에서만 수행합니다. 따라서 숫자 값은 적절한 타입으로 캐스팅하도록 신경써야 합니다:

    public function toSearchableArray()
    {
        return [
            'id' => (int) $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
        ];
    }

<a name="configuring-indexes-for-algolia"></a>
#### 인덱스 설정(Algolia)

Algolia 인덱스에 추가 설정이 필요할 때는, Algolia UI 말고 `config/scout.php` 파일에서 직접 관리할 수 있습니다. 이 방법은 자동 배포 파이프라인에 포함시켜 수동 설정 없이 여러 환경에서 일관성을 유지할 수 있게 해줍니다. 필터 가능 속성이나 랭킹, 패싯 등 [다양한 인덱스 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings) 가능 필드를 구성할 수 있습니다.

설정을 위해서는 `config/scout.php` 파일 내에서 각 인덱스별로 설정을 추가하세요:

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

해당 인덱스의 모델이 소프트 삭제 가능(soft deletable)하면서 `index-settings` 배열에 포함되어 있다면, Scout는 소프트 삭제 모델에 대한 패싯(faceting)도 지원합니다. 별도 설정이 필요 없을 때는 빈 배열로 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

앱의 인덱스 설정을 적용한 후에는 `scout:sync-index-settings` Artisan 명령어를 실행해야 합니다. 이 명령어는 현재 설정된 인덱스 구성을 Algolia에 전달합니다. 배포 프로세스에 포함하면 편리합니다:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-filterable-data-for-meilisearch"></a>
#### Meilisearch의 필터 가능 데이터 및 인덱스 설정

Scout의 다른 드라이버와 달리, Meilisearch는 필터 가능 속성, 정렬 가능 속성 등 [여러 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)를 사전 정의해야 합니다.

필터 가능 속성은 Scout의 `where` 메서드로 필터링할 속성, 정렬 가능 속성은 `orderBy`로 정렬할 속성입니다. 설정은 `scout` 설정 파일 내 `meilisearch` 부분의 `index-settings` 배열에서 관리하세요:

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

해당 인덱스의 모델이 소프트 삭제 가능(soft deletable)하면서 추가적인 필터 혹은 정렬 가능 속성이 없다면 빈 배열로 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```

설정이 끝나면, 반드시 `scout:sync-index-settings` Artisan 명령어로 Meilisearch에 인덱스 설정을 반영하세요:

```shell
php artisan scout:sync-index-settings
```

<a name="configuring-the-model-id"></a>
### 모델 ID 설정

기본적으로 Scout는 모델의 기본 키를 검색 인덱스에 저장되는 고유 ID/키로 사용합니다. 이를 바꾸려면 `getScoutKey`와 `getScoutKeyName`를 오버라이드하면 됩니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Laravel\Scout\Searchable;

    class User extends Model
    {
        use Searchable;

        /**
         * 인덱스로 사용할 키 값 반환.
         */
        public function getScoutKey(): mixed
        {
            return $this->email;
        }

        /**
         * 인덱스로 사용할 키 이름 반환.
         */
        public function getScoutKeyName(): mixed
        {
            return 'email';
        }
    }

<a name="configuring-search-engines-per-model"></a>
### 모델별 검색 엔진 설정

검색 시, Scout는 기본적으로 `scout` 설정 파일의 기본 검색 엔진을 사용합니다. 하지만 모델별로 `searchableUsing` 메서드를 오버라이드해 별도의 검색 엔진을 지정할 수 있습니다:

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

<a name="identifying-users"></a>
### 사용자 식별

Scout는 [Algolia](https://algolia.com) 사용 시에 자동으로 사용자를 식별할 수 있습니다. 인증된 사용자를 검색 작업과 연동해 Algolia 대시보드에서 검색 분석을 도울 수 있습니다. 이 기능을 활성화하려면 `.env` 파일에 `SCOUT_IDENTIFY` 환경변수를 `true`로 지정하세요:

```ini
SCOUT_IDENTIFY=true
```

이 기능을 활성화하면 요청자의 IP 주소와 인증된 사용자의 기본 식별자가 Algolia로 전달되어, 해당 사용자의 검색 요청과 연관됩니다.

<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 데이터베이스 엔진은 현재 MySQL과 PostgreSQL만 지원합니다.

소규모~중간 규모의 데이터베이스나 부하가 낮은 애플리케이션에서는 Scout의 "database" 엔진을 사용하는 것이 편리할 수 있습니다. 이 엔진은 기존 데이터베이스에서 "where like" 절과 전체텍스트 인덱스를 활용하여 검색 결과를 필터링합니다.

데이터베이스 엔진 사용 시에는 단순히 `SCOUT_DRIVER` 환경 변수를 `database`로 설정하거나 설정 파일에서 `database` 드라이버를 지정하면 됩니다:

```ini
SCOUT_DRIVER=database
```

설정 후, [검색 대상 데이터 구성](#configuring-searchable-data)을 하세요. 이후 [검색 쿼리 실행](#searching)이 가능합니다. Algolia, Meilisearch, Typesense 등에 필요했던 인덱싱 작업은 필요 없습니다.

#### 데이터베이스 검색 전략 커스터마이즈

기본적으로 database 엔진은 [검색 가능 데이터](#configuring-searchable-data)로 설정한 각 모델 속성에 대해 "where like" 쿼리를 실행합니다. 그러나 성능 향상을 위해 일부 컬럼에서는 전체텍스트 검색이나 접두어("example%") 혹은 전체 문자열("%example%") 검색 방식만 적용하도록 설정할 수 있습니다.

이 동작을 지정하려면, 모델의 `toSearchableArray` 메서드에 PHP 애트리뷰트를 지정하세요. 추가 검색 전략이 지정되지 않은 컬럼은 기본적으로 "where like"를 사용합니다:

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * 모델 인덱싱 데이터 배열 반환.
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
> 전체텍스트 쿼리 제약을 적용하기 전에 해당 컬럼에 [full text index](/docs/{{version}}/migrations#available-index-types)가 지정되어 있는지 확인하세요.

<a name="collection-engine"></a>
### 컬렉션 엔진

로컬 개발 시 Algolia, Meilisearch, Typesense 엔진 대신 "collection" 엔진 사용하는 것도 편리합니다. 이 엔진은 기존 데이터베이스에서 "where" 절과 컬렉션 필터링을 이용해서 결과를 구하며, 별도의 "인덱싱" 작업 없이 로컬 DB에서 모델을 불러옵니다.

"collection" 엔진 사용 시에는 `SCOUT_DRIVER` 환경변수를 `collection`으로 지정하거나 설정 파일에서 `collection` 드라이버를 설정하세요:

```ini
SCOUT_DRIVER=collection
```

설정 후, [검색 쿼리 실행](#searching)이 가능합니다. 별도의 인덱싱 작업은 필요 없습니다.

#### 데이터베이스 엔진과의 차이점

"database"와 "collection" 엔진은 모두 데이터베이스에서 직접 검색 결과를 가져온다는 점에서 비슷해보입니다. 하지만, collection 엔진은 전체텍스트 인덱스나 `LIKE` 쿼리를 사용하지 않고 모든 레코드를 불러와서 Laravel의 `Str::is` 헬퍼로 검색 문자열의 일치 여부를 검사합니다.

컬렉션 엔진은 Laravel이 지원하는 모든 관계형 데이터베이스(예: SQLite, SQL Server)에서도 사용할 수 있지만 database 엔진보다 효율적이지는 않습니다.

<a name="indexing"></a>
## 인덱싱

<a name="batch-import"></a>
### 배치 임포트

기존 프로젝트에 Scout를 도입한다면 이미 DB에 쌓여있는 레코드를 인덱스로 가져올 필요가 있습니다. `scout:import` Artisan 명령어를 사용하여 모든 기존 레코드를 검색 인덱스로 임포트할 수 있습니다:

```shell
php artisan scout:import "App\Models\Post"
```

`flush` 명령어를 사용하면 모델의 모든 레코드를 검색 인덱스에서 제거할 수 있습니다:

```shell
php artisan scout:flush "App\Models\Post"
```

<a name="modifying-the-import-query"></a>
#### 임포트 쿼리 커스터마이즈

배치 임포트 시 모델 전체를 불러오는 쿼리를 커스터마이즈하고 싶다면 모델에 `makeAllSearchableUsing` 메서드를 정의하세요. 예를 들어, 임포트 직전에 관계 데이터를 모두 Eager Loading 할 수 있습니다:

    use Illuminate\Database\Eloquent\Builder;

    /**
     * 모델 전체를 검색 가능하게 할 때 사용할 쿼리 수정.
     */
    protected function makeAllSearchableUsing(Builder $query): Builder
    {
        return $query->with('author');
    }

> [!WARNING]
> 큐를 사용해 배치 임포트를 하는 경우, `makeAllSearchableUsing` 메서드를 쓸 수 없습니다. 관계 데이터는 [복원되지 않습니다](/docs/{{version}}/queues#handling-relationships).

<a name="adding-records"></a>
### 레코드 추가

`Laravel\Scout\Searchable` 트레이트를 모델에 추가한 뒤, 단순히 모델 인스턴스를 `save`하거나 `create`만 하면 자동으로 검색 인덱스에 추가됩니다. 큐를 [사용하도록 설정](#queueing)했다면, 이 작업은 백그라운드에서 이루어집니다:

    use App\Models\Order;

    $order = new Order;

    // ...

    $order->save();

<a name="adding-records-via-query"></a>
#### 쿼리를 통한 레코드 추가

Eloquent 쿼리를 이용해 모델 컬렉션을 검색 인덱스에 추가하고 싶다면, 쿼리 뒤에 `searchable` 메서드를 체이닝하세요. 이 메서드는 쿼리 결과를 [청크 기준으로](/docs/{{version}}/eloquent#chunking-results) 나눠서 인덱스에 추가합니다. 큐를 사용했다면 각 청크도 백그라운드에서 임포트됩니다:

    use App\Models\Order;

    Order::where('price', '>', 100)->searchable();

Eloquent 관계 인스턴스에도 `searchable`을 사용할 수 있습니다:

    $user->orders()->searchable();

이미 메모리에 Eloquent 모델 컬렉션이 있다면 해당 컬렉션 인스턴스에 `searchable`을 호출하세요:

    $orders->searchable();

> [!NOTE]
> `searchable` 메서드는 "upsert" 연산으로 볼 수 있습니다. 즉, 인덱스에 이미 기록이 있으면 수정되고, 없으면 추가됩니다.

<a name="updating-records"></a>
### 레코드 수정

검색 가능한 모델 정보를 수정하려면 단순히 모델 프로퍼티를 변경한 뒤 `save`만 하면 됩니다. Scout가 자동으로 검색 인덱스에 변경 사항을 반영합니다:

    use App\Models\Order;

    $order = Order::find(1);

    // 주문 정보 수정...

    $order->save();

Eloquent 쿼리 인스턴스에 `searchable` 메서드를 호출해서 모델 컬렉션을 수정할 수도 있습니다. 인덱스에 없는 모델이면 새로 생성됩니다:

    Order::where('price', '>', 100)->searchable();

Eloquent 관계 인스턴스에서도 `searchable`을 호출하여 관련 모든 모델의 인덱스 레코드를 업데이트할 수 있습니다:

    $user->orders()->searchable();

이미 메모리에 모델 컬렉션이 있다면 그 인스턴스에 `searchable`을 호출하세요:

    $orders->searchable();

<a name="modifying-records-before-importing"></a>
#### 임포트 직전 레코드 수정

검색 가능하게 만들기 전에 모델 컬렉션을 준비해야 할 때가 있습니다. 예를 들어, 인덱스에 효율적으로 추가하려면 관계 데이터를 Eager Loading 해야 할 수 있습니다. 이렇게 하려면 해당 모델에 `makeSearchableUsing` 메서드를 정의하세요:

    use Illuminate\Database\Eloquent\Collection;

    /**
     * 검색 가능하게 만들 모델 컬렉션 수정.
     */
    public function makeSearchableUsing(Collection $models): Collection
    {
        return $models->load('author');
    }

<a name="removing-records"></a>
### 레코드 제거

검색 인덱스에서 레코드를 제거하려면, 데이터베이스에서 모델을 `delete` 하면 됩니다. [Soft Delete](/docs/{{version}}/eloquent#soft-deleting) 모델도 가능합니다:

    use App\Models\Order;

    $order = Order::find(1);

    $order->delete();

모델을 미리 가져오지 않고 레코드만 바로 삭제하려면 Eloquent 쿼리 인스턴스의 `unsearchable`을 사용하세요:

    Order::where('price', '>', 100)->unsearchable();

관계 인스턴스에서도 `unsearchable`을 호출할 수 있습니다:

    $user->orders()->unsearchable();

컬렉션 인스턴스에서도 `unsearchable`을 호출하여 해당 모델을 인덱스에서 제거할 수 있습니다:

    $orders->unsearchable();

전체 모델 레코드를 인덱스에서 모두 제거하려면 `removeAllFromSearch`를 호출하세요:

    Order::removeAllFromSearch();

<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

특정 모델에서 여러 개의 Eloquent 작업을 인덱스에 반영하지 않고 한꺼번에 처리해야 할 때가 있습니다. 이럴 때는 `withoutSyncingToSearch` 메서드를 활용할 수 있습니다. 이 메서드는 클로저 하나를 인자로 받아 즉시 실행하며, 해당 클로저 안에서 일어나는 모든 모델 작업은 인덱싱에 반영되지 않습니다:

    use App\Models\Order;

    Order::withoutSyncingToSearch(function () {
        // 모델 작업 수행...
    });

<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 모델 인스턴스

특정 조건에서만 모델을 인덱스에 반영하고 싶을 때가 있습니다. 예를 들어 `App\Models\Post`가 "초안(draft)"이거나 "발행(published)" 상태를 가질 수 있다면, "published"만 검색 가능하도록 정하고 싶을 수 있습니다. 이럴 땐 모델에 `shouldBeSearchable` 메서드를 정의하세요:

    /**
     * 모델이 검색 가능해야 하는지 여부 반환.
     */
    public function shouldBeSearchable(): bool
    {
        return $this->isPublished();
    }

`shouldBeSearchable` 메서드는 `save`나 `create`, 쿼리, 관계를 통한 작업에만 적용됩니다. 컬렉션이나 모델에 직접적으로 `searchable` 메서드를 사용하는 경우에는 이 메서드 결과를 무시합니다.

> [!WARNING]
> `shouldBeSearchable` 메서드는 Scout의 "database" 엔진에는 적용되지 않습니다. database 엔진을 사용할 때는 [Where 절](#where-clauses)에 조건을 추가하는 방식으로 해결하세요.

<a name="searching"></a>
## 검색

모델에서 `search` 메서드만으로 검색을 시작할 수 있습니다. 이 메서드는 검색어를 인자로 받으며, `get` 메서드를 체이닝하여 해당 검색 쿼리에 일치하는 Eloquent 모델을 반환받습니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->get();

Scout 검색 결과는 Eloquent 모델의 컬렉션이므로, 라우트나 컨트롤러에서 직접 반환하면 자동으로 JSON으로 변환됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/search', function (Request $request) {
        return Order::search($request->search)->get();
    });

원시(raw) 검색 결과를 Eloquent로 변환하지 않고 얻고 싶다면 `raw` 메서드를 사용하세요:

    $orders = Order::search('Star Trek')->raw();

<a name="custom-indexes"></a>
#### 커스텀 인덱스

검색 쿼리는 보통 모델의 [`searchableAs`](#configuring-model-indexes) 메서드에서 지정한 인덱스에서 수행됩니다. 하지만, `within` 메서드로 다른 커스텀 인덱스를 지정할 수 있습니다:

    $orders = Order::search('Star Trek')
        ->within('tv_shows_popularity_desc')
        ->get();

<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 간단한 "where" 절을 추가할 수 있습니다. 현재로서는 기본적인 숫자 등호 비교만 지원하며 주로 소유자 ID별로 검색 결과를 범위 한정하는 데 유용합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->where('user_id', 1)->get();

`whereIn` 메서드는 지정한 컬럼 값이 주어진 배열에 포함될 때만 결과를 반환합니다:

    $orders = Order::search('Star Trek')->whereIn(
        'status', ['open', 'paid']
    )->get();

`whereNotIn`은 주어진 컬럼 값이 배열에 포함되지 않을 때만 결과를 반환합니다:

    $orders = Order::search('Star Trek')->whereNotIn(
        'status', ['closed']
    )->get();

검색 인덱스는 관계형 데이터베이스가 아니므로, 더 복잡한 "where" 절은 지원하지 않습니다.

> [!WARNING]
> Meilisearch를 쓰는 경우, 반드시 [필터 가능 속성](#configuring-filterable-data-for-meilisearch)을 설정해야 Scout의 "where" 절을 사용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션

검색 결과를 컬렉션으로 받아올 수 있을 뿐만 아니라, `paginate` 메서드를 이용해 페이지네이션 처리도 가능합니다. 이 메서드는 [전통적인 Eloquent 쿼리 페이지네이션](/docs/{{version}}/pagination)과 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다:

    use App\Models\Order;

    $orders = Order::search('Star Trek')->paginate();

페이지별로 가져올 모델 개수를 첫 번째 인자로 지정할 수 있습니다:

    $orders = Order::search('Star Trek')->paginate(15);

검색 결과와 페이지 링크는 [Blade](/docs/{{version}}/blade)로 전통적인 Eloquent 페이지네이션과 똑같이 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```

페이지네이션 결과를 JSON으로 받고 싶다면, 라우트나 컨트롤러에서 paginator 인스턴스를 직접 반환하면 됩니다:

    use App\Models\Order;
    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        return Order::search($request->input('query'))->paginate(15);
    });

> [!WARNING]
> 검색 엔진은 Eloquent 모델의 글로벌 스코프 정의를 인식하지 못하므로, Scout의 페이지네이션을 사용하는 앱에서는 글로벌 스코프를 사용하지 않거나, 검색 시 스코프 제약을 직접 구현해야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

인덱싱된 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 사용하며, 소프트 삭제된 모델도 검색 대상에 포함하려면 `config/scout.php` 파일의 `soft_delete` 옵션을 `true`로 지정하세요:

    'soft_delete' => true,

이 옵션이 `true`이면, Scout는 소프트 삭제된 모델을 인덱스에서 제거하지 않습니다. 대신 인덱스에 숨겨진 `__soft_deleted` 속성을 추가합니다. 검색할 때는 `withTrashed` 또는 `onlyTrashed` 메서드로 소프트 삭제된 레코드도 반환할 수 있습니다:

    use App\Models\Order;

    // 소프트 삭제된 레코드도 포함
    $orders = Order::search('Star Trek')->withTrashed()->get();

    // 소프트 삭제된 레코드만 포함
    $orders = Order::search('Star Trek')->onlyTrashed()->get();

> [!NOTE]
> 소프트 삭제된 모델을 `forceDelete`로 영구 삭제하면, Scout가 검색 인덱스에서도 해당 기록을 자동으로 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 커스터마이즈

검색 엔진의 동작을 더욱 커스터마이즈할 필요가 있다면, `search` 메서드에 두 번째 인자로 클로저를 전달할 수 있습니다. 예를 들어, Algolia로 보내기 전 검색 옵션에 지리정보(geo-location)를 추가할 수 있습니다:

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

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 결과 쿼리 커스터마이즈

Scout가 검색 엔진에서 매칭되는 Eloquent 모델을 가져온 후, Eloquent를 이용해 기본 키로 모든 모델을 검색합니다. 이 쿼리를 커스터마이즈하려면 `query` 메서드를 호출하세요. 이 메서드는 Eloquent 쿼리 빌더 인스턴스를 인자로 받는 클로저를 전달합니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```

이 콜백은 이미 관련 모델을 검색 엔진에서 가져온 뒤 호출되므로, 결과를 "필터링"하려면 [Scout Where 절](#where-clauses)을 사용해야 합니다.

<a name="custom-engines"></a>
## 커스텀 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

내장 Scout 검색 엔진이 요구사항에 맞지 않으면, 커스텀 엔진을 만들어 Scout에 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 상속하고, 다음 여덟 가지 메서드를 구현해야 합니다:

    use Laravel\Scout\Builder;

    abstract public function update($models);
    abstract public function delete($models);
    abstract public function search(Builder $builder);
    abstract public function paginate(Builder $builder, $perPage, $page);
    abstract public function mapIds($results);
    abstract public function map(Builder $builder, $results, $model);
    abstract public function getTotalCount($results);
    abstract public function flush($model);

각 메서드의 구체 구현은 `Laravel\Scout\Engines\AlgoliaEngine` 클래스를 참고하면 도움이 됩니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

커스텀 엔진을 작성했다면, Scout 엔진 매니저의 `extend` 메서드를 사용해 등록할 수 있습니다. 엔진 매니저는 서비스 컨테이너에서 resolve 할 수 있습니다. `App\Providers\AppServiceProvider`의 `boot` 메서드나 애플리케이션에서 사용하는 서비스 프로바이더에 등록하는 것이 좋습니다:

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

등록 후에는, 앱의 `config/scout.php` 설정 파일에서 Scout의 기본 `driver`로 지정할 수 있습니다:

    'driver' => 'mysql',