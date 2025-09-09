# 일러퀀트: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [속성의 기본값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과를 청크 단위로 처리](#chunking-results)
    - [Lazy 컬렉션을 이용한 청크 처리](#chunking-using-lazy-collections)
    - [커서 사용](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계값 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입과 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [일괄 할당(Mass Assignment)](#mass-assignment)
    - [Upserts](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거(Muting)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel에는 데이터베이스와 쉽게 상호작용할 수 있게 해주는 객체-관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용할 때는 데이터베이스 테이블마다 해당 테이블과 연관된 "모델"을 만들고, 이를 통해 데이터베이스와 상호작용하게 됩니다. Eloquent 모델은 테이블에서 레코드를 조회할 뿐 아니라, 레코드의 삽입, 수정, 삭제 역시 간편하게 할 수 있습니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 구성에 대한 자세한 내용은 [데이터베이스 구성 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저 Eloquent 모델을 만들어보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장(extends)합니다. 새 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다:

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 유형의 클래스도 함께 생성할 수 있습니다. 이런 옵션들은 조합해서 한 번에 여러 클래스를 만들 수도 있습니다:

```shell
# 모델과 FlightFactory 클래스 생성...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델과 FlightSeeder 클래스 생성...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델과 FlightController 클래스 생성...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델과 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 클래스까지 한 번에 생성(단축키)...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗(pivot) 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 연관관계 확인

모델 코드만 살펴봐서는 해당 모델의 모든 속성과 연관관계를 한눈에 파악하기 어려울 때가 있습니다. 이럴 때는 `model:show` Artisan 명령어를 사용해 모델의 속성과 연관관계를 간편하게 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 이제 기본적인 모델 클래스를 살펴보고, Eloquent의 주요 규칙들을 알아보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    // ...
}
```

<a name="table-names"></a>
### 테이블 이름

위 예제에서 보시다시피, Eloquent에 어떤 데이터베이스 테이블을 사용할지 별도로 명시하지 않았습니다. Eloquent는 관례적으로 "스네이크 케이스(snake case)" 복수형 클래스명을 테이블 이름으로 사용합니다. 즉, `Flight` 모델의 경우 `flights` 테이블을, `AirTrafficController` 모델의 경우 `air_traffic_controllers` 테이블을 사용합니다.

만약 이러한 규칙에 맞지 않는 테이블명을 사용한다면, 모델의 `table` 속성을 직접 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 연관된 테이블명.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델의 데이터베이스 테이블에 기본 키(primary key) 컬럼으로 `id`가 있다고 가정합니다. 만약 다른 컬럼을 기본 키로 사용하려면 모델의 보호된 `$primaryKey` 속성에 해당 컬럼명을 지정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 테이블에 연관된 기본 키명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, Eloquent는 기본 키가 자동으로 증가하는 정수라고 가정하여, 기본 키 값을 자동으로 정수형으로 변환합니다. 자동 증가형 또는 숫자가 아닌 기본 키를 사용하려면, public `$incrementing` 속성을 `false`로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동 증가하는지 여부.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

모델의 기본 키가 정수가 아니라면, 보호된 `$keyType` 속성을 지정해야 합니다. 이 속성에는 문자열 `string`이 들어갑니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본 키 ID의 데이터 타입.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent 모델은 반드시 하나의 기본 키 역할을 하는 "ID" 값을 가져야 하며, 복합 기본 키(여러 컬럼으로 구성된 기본 키)는 지원하지 않습니다. 하지만, 데이터베이스 테이블에는 기본 키 외에도 여러 컬럼을 묶는 유니크 인덱스를 추가할 수는 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

자동 증가 정수 대신 UUID(범용 고유 식별자)를 Eloquent 기본 키로 사용할 수도 있습니다. UUID는 36자의 영문과 숫자가 합쳐진 고유 식별자입니다.

모델의 기본 키로 UUID를 사용하고 싶다면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가하면 됩니다. 이때 모델의 기본 키 컬럼이 [UUID와 호환되게](/docs/12.x/migrations#column-method-uuid) 설계되어 있어야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "8f8e8478-9035-4d23-b9a7-62f4d2612ce5"
```

기본적으로 `HasUuids` 트레이트는 ["Ordered UUID"](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 이런 UUID는 데이터베이스 인덱스 성능을 위해 사전(lexicographical) 순서로 정렬될 수 있습니다.

UUID 생성 방식을 모델마다 오버라이드 하려면 `newUniqueId` 메서드를, UUID 값을 받을 컬럼을 지정하려면 `uniqueIds` 메서드를 모델에 정의하세요:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델을 위한 새 UUID 생성.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자를 받을 컬럼 목록 반환.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 ULID(26자, UUID보다 짧지만 마찬가지로 사전 정렬 가능한 고유 식별자)를 쓸 수 있습니다. 이 경우 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 지정하고, 해당 컬럼이 [ULID와 호환](/docs/12.x/migrations#column-method-ulid)되게 설계되어 있어야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a name="timestamps"></a>
### 타임스탬프

Eloquent는 기본적으로 `created_at`, `updated_at` 컬럼이 모델의 테이블에 존재한다고 가정하며, 모델이 생성/수정될 때 해당 컬럼 값을 자동으로 관리합니다. 자동 생성/수정 타임스탬프가 필요 없다면, `$timestamps` 속성을 모델에 `false`로 지정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 타임스탬프를 사용할지 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델 타임스탬프의 날짜 포맷을 변경하려면, `$dateFormat` 속성을 지정하세요. 이 속성은 데이터베이스 저장 형식 및 모델을 배열 또는 JSON으로 직렬화할 때의 날짜 형식에 모두 적용됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 컬럼 저장 형식
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 직접 지정하려면 `CREATED_AT`, `UPDATED_AT` 상수를 모델에 정의하세요:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프를 갱신하지 않고 모델 작업을 처리하고 싶다면, `withoutTimestamps` 메서드에 클로저를 전달해 모델 작업을 할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

Eloquent 모델은 애플리케이션에서 기본 설정된 데이터베이스 연결을 사용합니다. 특정 모델에서 다른 데이터베이스 연결을 사용하고 싶으면 `$connection` 속성을 지정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 사용할 데이터베이스 연결명.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 속성의 기본값

새로 생성한 모델 인스턴스에는 기본적으로 아무런 속성값이 없습니다. 일부 속성의 기본값을 지정하고 싶다면 `$attributes` 속성에 기본값을 설정하세요. 이 값들은 데이터베이스에서 읽은 값 형식이어야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 속성의 기본값
     *
     * @var array
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```

<a name="configuring-eloquent-strictness"></a>
### Eloquent 엄격성 설정

Laravel은 Eloquent의 다양한 동작과 "엄격함(strictness)"을 제어할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 레이지 로딩(lazy loading)을 금지할지의 여부를 선택적으로 설정할 수 있습니다. 예를 들어, 실서비스(운영) 환경에서는 레이지 로딩을 허용하고 개발환경에서만 금지하는 방식이 가능합니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, `preventSilentlyDiscardingAttributes` 메서드를 통해, Eloquent 모델의 `fillable` 배열에 없는 속성을 대량 할당(mass assignment)하려 할 때 예외를 발생시킬 수 있습니다. 이는 개발 과정에서 원하는 변경이 적용되지 않는 문제를 쉽게 파악하는 데 도움이 됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 조회해볼 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)처럼 동작하여, fluent 방식으로 쿼리를 달고 데이터를 조회할 수 있습니다. 모델의 `all` 메서드는 모델의 테이블에 있는 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌딩

Eloquent의 `all` 메서드는 테이블의 전체 레코드를 조회합니다. 하지만, 각 Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries)이기 때문에, 추가적인 조건을 자유롭게 붙여서 `get` 메서드로 원하는 결과만 가져올 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더](/docs/12.x/queries)에서 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 자유롭게 활용하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh` 와 `refresh` 메서드로 모델을 다시 갱신할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 새로 조회해 반환하며, 기존 인스턴스는 변경하지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 인스턴스 자체를 데이터베이스에서 다시 가져온 값으로 덮어씁니다. 모델에 로드된 연관관계도 새로 갱신됩니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`, `get`과 같은 Eloquent 메서드는 여러 레코드를 조회할 때 단순한 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 상속하며, [다양한 편리한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 클로저의 결과에 따라 컬렉션에서 특정 모델들을 제외할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

기본 컬렉션 메서드 외에도, Eloquent 컬렉션에서만 제공되는 [추가 메서드](/docs/12.x/eloquent-collections#available-methods)도 있습니다.

Laravel의 모든 컬렉션은 PHP의 반복자 인터페이스를 구현하므로 일반 배열처럼 `foreach`로 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리

Eloquent의 `all`이나 `get` 메서드로 수만 건의 레코드를 한 번에 불러오려 하면, 애플리케이션 메모리가 부족할 수 있습니다. 이런 대량 데이터를 효율적으로 처리할 때는 `chunk` 메서드를 사용하는 것이 좋습니다.

`chunk` 메서드는 전체 레코드를 일부(청크)씩 나누어 클로저로 전달하며, 매번 필요한 청크만 메모리에 불러오므로 메모리 사용량이 크게 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 번에 가져올 레코드 수입니다. 두 번째로 넘긴 클로저가 각 청크마다 호출됩니다. 청크마다 쿼리가 실행되어 순차적으로 데이터가 읽혀집니다.

만약 필터 조건으로 사용한 컬럼의 값을 반복문에서 업데이트도 해야 한다면, `chunk` 대신 `chunkById`를 사용하는 것이 안전합니다. `chunk`를 사용하면 일부 레코드가 중복되거나 누락될 수 있기 때문입니다. 내부적으로 `chunkById`는 이전 청크의 마지막 모델보다 큰 `id` 컬럼 값을 가진 모델만을 조회합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById`는 내부적으로 자체적인 "where" 조건을 추가하므로, 직접 조건을 추가할 때는 [논리적 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저로 감싸는 것이 좋습니다:

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) {
    $flights->each->update([
        'departed' => false,
        'cancelled' => true
    ]);
}, column: 'id');
```

<a name="chunking-using-lazy-collections"></a>
### Lazy 컬렉션을 이용한 청크 처리

`lazy` 메서드는 내부적으로 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 즉시 콜백으로 넘기지 않고 [LazyCollection](/docs/12.x/collections#lazy-collections) 객체로 평탄화(flatten)해 반환합니다. 덕분에 대량 데이터를 하나의 스트림처럼 처리할 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

마찬가지로, 컬럼 기반으로 필터링하면서 해당 컬럼을 반복 중에 업데이트해야 한다면 `lazyById`를 써야 합니다. 내부적으로는 이전 청크의 마지막 id보다 큰 레코드만 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`id`를 내림차순 기준으로 필터링하려면 `lazyByIdDesc` 메서드를 사용할 수 있습니다.

<a name="cursors"></a>
### 커서 사용

`lazy`와 비슷하게, `cursor` 메서드는 수만 건의 Eloquent 모델을 반복 처리할 때 애플리케이션 메모리 사용을 획기적으로 줄여줍니다.

`cursor`는 단 한 번만 DB 쿼리를 실행한 뒤, 실제 반복이 일어날 때마다 레코드를 하나씩 Eloquent 모델로 변환합니다. 따라서 반복 도중 한 번에 단 하나의 Eloquent 모델만 메모리에 올리게 됩니다.

> [!WARNING]
> `cursor`는 한 번에 한 모델만 메모리에 있으므로, 연관관계 Eager Loading은 사용할 수 없습니다. 연관관계를 함께 조회해야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

내부적으로 `cursor`는 PHP [generator](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 객체를 반환하며, [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)의 다양한 메서드를 활용할 수 있습니다. 단, 언제나 한 번에 한 레코드만 메모리에 올라갑니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor`는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, 결국에는 [PHP PDO 드라이버가 모든 원본 결과를 버퍼에 캐싱하기 때문에](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php) 메모리가 부족해질 수 있습니다. 아주 대용량 데이터를 다룬다면 [lazy 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 SELECT

Eloquent는 관련 테이블의 정보를 한 번에 조회할 수 있는 고급 서브쿼리 기능을 제공합니다. 예를 들어, `destinations`와 `flights` 테이블이 있고, `flights`에 도착 시간을 나타내는 `arrived_at` 컬럼이 있다면, `select`와 `addSelect` 메서드를 활용해 각 도착지의 최근 도착 비행기 이름을 한 번의 쿼리로 조회할 수 있습니다:

```php
use App\Models\Destination;
use App\Models\Flight;

return Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```

<a name="subquery-ordering"></a>
#### 서브쿼리 정렬

쿼리 빌더의 `orderBy`도 서브쿼리를 지원합니다. 위의 비행기 예시처럼, 도착지 별로 최근 도착한 비행기 시간 순으로 정렬하는 것도 단일 쿼리로 처리할 수 있습니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델/집계값 조회

특정 쿼리에 맞는 레코드 여러 개를 조회하는 것 외에, `find`, `first`, `firstWhere` 메서드를 통해 단일 레코드만 바로 가져올 수도 있습니다. 이 경우 Eloquent 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 모델 조회...
$flight = Flight::find(1);

// 쿼리 조건에 맞는 첫 모델 조회...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건에 맞는 첫 모델 조회(대안)...
$flight = Flight::firstWhere('active', 1);
```

조회 결과가 없을 때 추가 동작을 하고 싶다면, `findOr`, `firstOr` 메서드를 사용할 수 있습니다. 이 메서드는 해당 레코드가 없을 때 클로저를 실행하며, 클로저의 반환값이 최종 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 모델을 찾지 못했을 때 예외

모델을 찾을 수 없을 때 예외를 발생시키는 경우가 종종 있습니다(특히 라우트나 컨트롤러에서 유용). `findOrFail`, `firstOrFail` 메서드는 첫 번째 결과를 반환하거나, 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`을 따로 처리하지 않으면, 클라이언트에 자동으로 404 HTTP 응답이 전송됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 조건으로 데이터베이스 레코드를 검색하고, 없으면 첫 번째 배열(검색 조건)과 선택적 두 번째 배열(생성 속성)을 합쳐 새로운 레코드를 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 거의 같지만, 해당하는 레코드를 찾지 못하면 새 모델 인스턴스만 반환합니다(아직 DB에는 저장되지 않음). 이 경우 직접 `save` 를 호출해야 합니다:

```php
use App\Models\Flight;

// 이름으로 조회하거나, 없으면 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나, 없으면 이름/지연/도착시간 포함 새 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회하거나, 없으면 새 인스턴스 반환...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나, 없으면 해당 속성으로 인스턴스 반환...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델을 사용할 때는, Laravel [쿼리 빌더](/docs/12.x/queries)에서 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/12.x/queries#aggregates)도 사용할 수 있습니다. 이 메서드들은 모델 인스턴스가 아니라 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입과 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때는 데이터 조회뿐 아니라 새 레코드의 삽입도 매우 간단합니다. 새 레코드를 삽입하려면 모델 인스턴스를 생성하고, 속성값을 설정한 뒤, `save` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 비행 정보를 데이터베이스에 저장
     */
    public function store(Request $request): RedirectResponse
    {
        // 요청 유효성 검사...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

이 예제에서는 요청으로 받은 `name` 값을 `App\Models\Flight` 모델의 `name` 속성에 대입했습니다. `save` 메서드를 호출하면 레코드가 DB에 저장되고, 이때 `created_at`, `updated_at` 타임스탬프도 자동으로 저장됩니다.

대신, 한 번에 모델을 생성해 저장하고 싶으면 `create` 메서드를 사용할 수도 있습니다. 반환값은 생성된 모델 인스턴스입니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드 사용 전에는 모델 클래스에 `fillable` 또는 `guarded` 속성을 반드시 명시해야 합니다. 이는 Eloquent 모델이 기본적으로 일괄 할당(대량 할당) 취약점에 대비해 보호되어 있기 때문입니다. 보다 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

이미 존재하는 레코드의 모델을 수정할 때도 `save` 메서드를 사용합니다. 우선 모델을 조회해서 수정할 속성을 바꾼 후, `save`를 호출해 변경사항을 DB에 저장하면 됩니다. `updated_at` 타임스탬프는 자동으로 업데이트됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

가끔은 기존 모델을 업데이트하거나, 조건에 맞는 모델이 없다면 새로 생성해야 할 수 있습니다. `firstOrCreate`와 유사하게, `updateOrCreate` 메서드는 자동으로 DB에 저장되므로 직접 `save`를 호출하지 않아도 됩니다.

아래 예시에서, 출발지가 `Oakland`이고 도착지가 `San Diego`인 비행이 있으면 가격과 할인 컬럼이 업데이트됩니다. 해당 비행이 없으면 첫 번째, 두 번째 인수를 합친 속성으로 새 비행이 생성됩니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트(Mass Updates)

쿼리에 맞는 여러 모델을 한 번에 업데이트할 수도 있습니다. 아래 예제에서는 `active`이고 목적지가 `San Diego`인 모든 비행을 지연 처리합니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 수정할 컬럼-값 쌍의 배열을 인자로 받고, 실행된 레코드 개수를 반환합니다.

> [!WARNING]
> Eloquent로 대량 업데이트를 하면 `saving`, `saved`, `updating`, `updated` 등의 모델 이벤트가 발생하지 않습니다. 대량 업데이트는 실제로 모델을 조회하지 않고 바로 DB에 적용하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 내역 확인

Eloquent는 모델의 내부 상태를 판단해 속성이 언제 어떻게 바뀌었는지 쉽게 알 수 있도록 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

`isDirty`는 모델 조회 후 속성에 변화가 있었는지 확인하며, 특정 속성명 또는 속성 배열을 인자로 전달해 해당 속성만 검사할 수도 있습니다. `isClean`은 속성에 변경이 없었는지 판단하며, 역시 인자를 받을 수 있습니다:

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty(); // true
$user->isDirty('title'); // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true
$user->isClean(['first_name', 'title']); // false

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```

`wasChanged`는 최종적으로 저장한 직후(요청 내) 속성의 변경 여부를 확인합니다. 특정 속성명이나 배열도 인자로 넘길 수 있습니다:

```php
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
$user->wasChanged(['title', 'slug']); // true
$user->wasChanged('first_name'); // false
$user->wasChanged(['first_name', 'title']); // true
```

`getOriginal`은 모델이 처음 조회된 시점의 원본 속성값을 배열로 반환합니다. 특정 속성명을 인자로 넘기면 해당 속성의 최초 값을 받을 수 있습니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 모든 원본 속성값 배열
```

`getChanges`는 마지막 저장 시 변경된 속성값 배열을, `getPrevious`는 저장 전 원래 속성값 배열을 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->update([
    'name' => 'Jack',
    'email' => 'jack@example.com',
]);

$user->getChanges();

/*
    [
        'name' => 'Jack',
        'email' => 'jack@example.com',
    ]
*/

$user->getPrevious();

/*
    [
        'name' => 'John',
        'email' => 'john@example.com',
    ]
*/
```

<a name="mass-assignment"></a>
### 일괄 할당(Mass Assignment)

`create` 메서드는 새 모델을 한 번에 저장할 수 있게 해줍니다. 반환값은 생성된 모델 인스턴스입니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create`를 사용하기 전에 `fillable` 또는 `guarded` 속성을 반드시 지정해야 합니다. 이는 모든 Eloquent 모델이 기본적으로 대량 할당 취약점(Mass Assignment Vulnerability)을 방지하도록 설계되어 있기 때문입니다.

대량 할당 취약점은, 사용자가 예상치 못한 HTTP 요청 필드를 보내 해당 컬럼이 무심코 DB에 저장되는 경우 발생합니다. 예를 들어 악의적인 사용자가 `is_admin` 파라미터를 만들어 보내면, 모델의 `create` 메서드를 통해 관리자로 권한이 상승되는 사고가 발생할 수 있습니다.

따라서 모델에서 대량 할당 가능한 속성을 `$fillable` 배열로 명시해야 합니다. 예를 들어 `Flight` 모델의 `name` 속성만 대량 할당을 허용하고 싶으면 다음과 같이 작성합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용된 속성 목록
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

일괄 할당 가능 속성을 지정했다면, `create` 메서드로 새 레코드를 저장할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 생성된 모델 인스턴스에 배열로 속성을 할당할 때는 `fill` 메서드를 사용할 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 일괄 할당과 JSON 컬럼

JSON 컬럼을 할당할 때도, 컬럼 키를 반드시 `$fillable` 배열에 명시해야 합니다. 보안을 위해 `$guarded` 사용 시에는 중첩 JSON 속성의 업데이트가 지원되지 않습니다:

```php
/**
 * 대량 할당이 허용된 속성
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성을 대량 할당 허용

모든 속성을 대량 할당 가능하게 하고 싶으면, 모델의 `$guarded` 속성을 빈 배열로 만드세요. 단, 이 경우 Eloquent의 `fill`, `create`, `update`에 넘기는 배열을 항상 직접 설계해야 합니다:

```php
/**
 * 대량 할당이 허용되지 않는 속성 목록
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `fillable`에 없는 속성을 대량 할당하면 해당 값은 조용히 무시됩니다. 운영환경에서는 예상되는 동작이나, 개발환경에서는 왜 값이 반영되지 않는지 혼란스러울 수 있습니다.

원할 경우, 대량 할당 시 비허용 속성이 포함되었을 때 예외를 발생시키도록 할 수 있습니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upserts

Eloquent의 `upsert` 메서드는 여러 레코드의 업데이트/생성을 단일 원자 연산으로 처리합니다. 첫 번째 인자는 삽입/업데이트 될 값들, 두 번째 인자는 레코드를 고유하게 식별할 컬럼(들), 세 번째 인자는 이미 존재하는 레코드를 업데이트할 컬럼 배열입니다. 타임스탬프가 활성화 되어 있으면 `created_at`과 `updated_at`이 자동으로 설정됩니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 두 번째 인자의 컬럼에 "primary" 또는 "unique" 인덱스가 있어야만 동작합니다. MariaDB, MySQL 드라이버는 두 번째 인자를 무시하고 항상 테이블의 "primary", "unique" 인덱스만 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 해당 모델 인스턴스의 `delete` 메서드를 호출하세요:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위의 예제처럼, 먼저 모델을 조회한 뒤 삭제하는 것이 일반적이지만, 기본 키 값만 알고 있다면 `destroy`를 이용해 직접 모델 인스턴스를 만들 필요 없이 삭제할 수 있습니다. `destroy`는 단일/여러 기본 키, 키 배열, [컬렉션](/docs/12.x/collections) 모두 지원합니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용할 경우, 완전히 제거(Force Delete)하려면 `forceDestroy`를 사용하세요:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy`는 각각의 모델을 개별적으로 로드하며 `delete`를 따로 호출하므로, `deleting`, `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 모델 삭제

특정 조건에 맞는 모델 전체를 삭제할 수도 있습니다. 아래 예제에서는 상태가 '비활성'인 모든 항공편을 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제 시 모델 이벤트는 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블 전체를 삭제하려면 조건 없이 쿼리를 실행하세요:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent로 대량 삭제 시 `deleting`, `deleted` 이벤트가 발생하지 않습니다. (모델을 조회하지 않고 바로 삭제 쿼리를 실행하기 때문입니다.)

<a name="soft-deleting"></a>
### 소프트 삭제

실제로 레코드를 DB에서 제거하기보다, Eloquent는 레코드를 "소프트 삭제"할 수 있습니다. 소프트 삭제된 모델은 DB에 그대로 남지만, `deleted_at` 속성이 현재 날짜/시간으로 설정됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model
{
    use SoftDeletes;
}
```

> [!NOTE]
> `SoftDeletes` 트레이트는 자동으로 `deleted_at` 속성을 `DateTime`/`Carbon` 인스턴스 타입으로 캐스팅합니다.

DB 테이블에도 `deleted_at` 컬럼을 추가해야 하며, Laravel [스키마 빌더](/docs/12.x/migrations)의 헬퍼를 사용할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```

이제 모델에서 `delete`를 호출하면, 실제로 삭제하지 않고 `deleted_at` 컬럼만 현재 시각으로 설정됩니다. 소프트 삭제 모델을 쿼리하면, 삭제된 레코드는 자동으로 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제 상태인지 판별하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

소프트 삭제된 모델을 다시 활성화(복원)할 때는 `restore` 메서드를 호출합니다. 이 메서드는 해당 모델의 `deleted_at` 컬럼을 `null`로 설정합니다:

```php
$flight->restore();
```

복수 모델을 쿼리 조건으로 복원할 수도 있습니다. 대량 작업이므로 모델 이벤트는 발생하지 않습니다:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[연관관계](/docs/12.x/eloquent-relationships) 쿼리에서도 `restore`를 사용할 수 있습니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 완전 삭제(영구 삭제) 모델

DB에서 해당 레코드를 완전히 제거하고 싶다면, 소프트 삭제된 모델에서 `forceDelete`를 사용하세요:

```php
$flight->forceDelete();
```

Eloquent 연관관계 쿼리에서도 사용할 수 있습니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 쿼리

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함

기본적으로 소프트 삭제된 모델은 쿼리 결과에서 제외되지만, `withTrashed`를 호출하면 결과에 포함시킬 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

[연관관계](/docs/12.x/eloquent-relationships) 쿼리에도 사용할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 오직 소프트 삭제된 모델만 조회

`onlyTrashed` 메서드는 **오직** 소프트 삭제된 레코드만 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

특정 모델 데이터를 주기적으로 삭제(정리)하고 싶을 때는 모델에 `Illuminate\Database\Eloquent\Prunable` 혹은 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하면 됩니다. 트레이트를 추가한 뒤, 더 이상 필요 없는 모델을 조회하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * 가지치기 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

모델에 `Prunable`을 표시했다면, 가지치기 전 `pruning` 메서드도 구현할 수 있습니다. 이 메서드는 모델 삭제 전에 추가 리소스(예: 파일) 정리에 유용합니다:

```php
/**
 * 가지치기 전 작업 정의
 */
protected function pruning(): void
{
    // ...
}
```

구성을 마쳤으면, 애플리케이션의 `routes/console.php` 파일에 `model:prune` Artisan 명령어를 스케줄링하세요. 실행 주기는 자유롭게 지정 가능합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령은 `app/Models` 디렉토리의 "Prunable" 모델을 자동으로 탐색합니다. 모델이 다른 위치에 있다면 `--model` 옵션으로 직접 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 가지치기에서 제외하고 싶다면 `--except` 옵션을 사용하세요:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션으로 `model:prune` 명령 수행 시 실제 가지치기 대신 삭제될 레코드 수를 확인할 수 있습니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델이라도, prunable 쿼리에 해당하는 레코드는 실제로 완전히 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하면, 딜리트 쿼리를 통해 대량으로 레코드를 바로 삭제합니다. 이럴 경우 `pruning` 메서드, `deleting`, `deleted` 이벤트는 발생하지 않으므로, 성능은 훨씬 효율적입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * 가지치기 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 저장되지 않은 복제본으로 만들고 싶을 때 `replicate` 메서드를 사용하세요. 동일한 속성이 많은 모델을 여러 개 만들고 싶을 때 유용합니다:

```php
use App\Models\Address;

$shipping = Address::create([
    'type' => 'shipping',
    'line_1' => '123 Example Street',
    'city' => 'Victorville',
    'state' => 'CA',
    'postcode' => '90001',
]);

$billing = $shipping->replicate()->fill([
    'type' => 'billing'
]);

$billing->save();
```

복제본에서 복사하지 않을 속성이 있다면 배열로 전달할 수 있습니다:

```php
$flight = Flight::create([
    'destination' => 'LAX',
    'origin' => 'LHR',
    'last_flown' => '2020-03-04 11:00:00',
    'last_pilot_id' => 747,
]);

$flight = $flight->replicate([
    'last_flown',
    'last_pilot_id'
]);
```

<a name="query-scopes"></a>
## 쿼리 스코프

<a name="global-scopes"></a>
### 글로벌 스코프

글로벌 스코프는 특정 모델의 모든 쿼리에 일괄적으로 제약을 추가하는 기능입니다. Laravel의 [소프트 삭제](#soft-deleting) 역시 글로벌 스코프를 사용해 이미 삭제된 모델을 자동으로 쿼리에서 제거합니다. 직접 글로벌 스코프를 작성하면 모든 쿼리에 공통 조건을 쉽고 깔끔하게 부여할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성

새 글로벌 스코프를 만들려면, `make:scope` Artisan 명령을 실행하면 됩니다. 생성된 스코프는 `app/Models/Scopes` 폴더에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 구현

글로벌 스코프는 간단히 구성할 수 있습니다. 우선 `make:scope` 명령어로 클래스를 생성하고, 이 클래스가 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하도록 합니다. `apply` 메서드를 정의해 제약 조건(예: where)을 추가하는 방식입니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 특정 Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 select 절에 컬럼을 추가할 때는 `select` 대신 `addSelect`를 사용하세요. 기존 select 절이 의도치 않게 덮어써지는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

글로벌 스코프를 모델에 할당하려면, 해당 모델에 `ScopedBy` 속성을 붙이면 됩니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy([AncientScope::class])]
class User extends Model
{
    //
}
```

또는, 모델의 `booted` 메서드를 오버라이드하여 직접 `addGlobalScope` 메서드로 등록해도 됩니다. 인자로 스코프 인스턴스를 넘겨줍니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예제처럼 `App\Models\User` 모델에 스코프를 적용하면, `User::all()` 호출 시 다음과 같은 SQL 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

간단한 스코프라면 클래스를 따로 만들 필요 없이, 클로저로 글로벌 스코프를 정의할 수도 있습니다. 이때 `addGlobalScope`의 첫 번째 인수로 스코프 이름을 지정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->subYears(2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 글로벌 스코프 제거

특정 쿼리에서 글로벌 스코프를 적용하지 않으려면, `withoutGlobalScope`를 사용하세요. 인자로 스코프 클래스 이름을 전달합니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 스코프를 지정한 경우엔, 직접 지정한 스코프 이름(문자열)을 인자로 넘깁니다:

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 혹은 전체 글로벌 스코프를 제거하려면 `withoutGlobalScopes`, `withoutGlobalScopesExcept` 메서드를 사용하세요:

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 지정된 글로벌 스코프만 남기고 나머지는 제거
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 사용되는 쿼리 제약 조건을 메서드로 미리 정의해, 언제든 재사용할 수 있게 해주는 기능입니다. 예를 들어 "인기 있는 사용자"를 반복적으로 조회해야 한다면, 모델에 아래처럼 `Scope` 속성을 달아 메서드를 추가할 수 있습니다.

스코프는 반드시 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 있는 사용자만 쿼리하도록 스코프 정의
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 쿼리하도록 스코프 정의
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용

스코프를 정의했다면, 쿼리할 때 메서드 체이닝처럼 호출할 수 있습니다. 여러 스코프도 이어서 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or` 조건으로 조합하려면 [논리 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이런 코드가 번거로울 수 있어, Laravel은 클로저 없이도 간단히 여러 스코프를 `orWhere`로 체이닝 할 수 있는 "하이어 오더" 메서드를 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프(파라미터 받는 스코프)

파라미터가 필요한 스코프는, 스코프 메서드 시그니처에 `$query` 뒤에 원하는 인자를 추가하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 쿼리하는 스코프
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

아래처럼 사용할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending 속성

스코프를 활용해, 쿼리 조건에 사용된 속성과 동일한 속성값을 가진 모델을 새로 만들고 싶을 때는, 쿼리에서 `withAttributes` 메서드를 쓸 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시 저장글(draft)만 쿼리하는 스코프
     */
    #[Scope]
    protected function draft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

`withAttributes`는 넘긴 속성값을 쿼리의 where 조건에 추가하고, 스코프를 통해 생성된 모델에도 해당 속성이 할당되게 해줍니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

where 조건에는 포함하지 않고 모델에만 속성을 할당하고 싶다면, `asConditions` 인자를 false로 지정하세요:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 동일한지(동일한 기본 키, 테이블, DB 연결 사용 여부)를 확인하려면 `is`, `isNot` 메서드를 사용할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

또한 `is`, `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/12.x/eloquent-relationships)에서도 쓸 수 있어, 쿼리 없이 연관관계 모델을 비교할 때 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션으로 직접 브로드캐스트하고 싶으신가요? [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 문서를 참고하세요.

Eloquent 모델은 모델의 라이프사이클 여러 지점에서 다양한 이벤트를 발생시킵니다. 이벤트 종류는 다음과 같습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

예를 들어 `retrieved`는 모델이 조회될 때 발생하고, 새 모델이 저장될 때는 `creating`/`created`, 기존 모델이 수정 저장될 때는 `updating`/`updated`가 발생합니다. `saving`/`saved`는 생성 또는 업데이트 시 항상 발생하며, `-ing`로 끝나는 이벤트는 DB에 반영되기 전, `-ed`로 끝나는 이벤트는 반영된 후 발생합니다.

모델 이벤트를 사용하려면, 모델에 `$dispatchesEvents` 속성을 정의해 Eloquent 모델의 라이프사이클 이벤트와 [사용자 이벤트 클래스](/docs/12.x/events)를 매핑하세요. 이벤트 클래스에서는 영향을 받은 모델 인스턴스를 생성자로 전달받습니다:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 모델 이벤트 매핑
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트를 정의/매핑한 뒤에는 [이벤트 리스너](/docs/12.x/events#defining-listeners)를 활용해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent로 대량 업데이트 또는 삭제 쿼리를 실행할 때는 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다. 모델을 개별적으로 조회해서 처리하는 것이 아니기 때문입니다.

<a name="events-using-closures"></a>
### 클로저(익명 함수)로 이벤트 리스닝

별도의 이벤트 클래스를 사용하지 않고, 클로저(익명 함수)로 모델 이벤트 리스너를 등록할 수도 있습니다. 보통 이는 모델의 `booted` 메서드에 작성합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 [큐잉이 가능한 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 활용해 모델 이벤트 리스너를 백그라운드로 실행할 수도 있습니다([큐 시스템](/docs/12.x/queues) 활용):

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버(Observer)

<a name="defining-observers"></a>
#### 옵저버 정의

한 모델에 대해 여러 이벤트 리스닝을 함께 관리하려면 옵저버 클래스를 사용할 수 있습니다. 옵저버 클래스는 들을 이벤트에 따라 메서드명을 맞춰서 작성하며, 각 메서드는 영향을 받은 모델만 인자로 받습니다. `make:observer` Artisan 명령어로 쉽게 클래스를 만들 수 있습니다:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령은 옵저버를 `app/Observers` 디렉터리에 생성합니다. 디렉터리가 없으면 자동으로 만들어줍니다. 생성된 옵저버의 예시는 아래와 같습니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 처리
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 처리
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 처리
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 처리
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 처리
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면, 대응되는 모델에 `ObservedBy` 속성을 붙이면 됩니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

혹은 `AppServiceProvider`의 `boot` 메서드에서, 직접 `observe` 메서드로 등록할 수 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버에서 추가로 들을 수 있는 이벤트(예: `saving`, `retrieved`) 등이 있으며, 구체적인 설명은 [이벤트](#events) 문서에 있습니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 DB 트랜잭션

모델이 데이터베이스 트랜잭션 내에서 생성되는 경우, 트랜잭션이 커밋된 후에만 이벤트 핸들러가 실행되도록 옵저버를 지정할 수 있습니다. 옵저버 클래스에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 트랜잭션이 없으면 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 처리
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거(Muting)

때로는 모델에서 발생하는 모든 이벤트를 일시적으로 비활성화(음소거)할 필요가 있을 수 있습니다. 이럴 때는 `withoutEvents` 메서드를 사용하세요. 이 메서드는 클로저를 인자로 받고, 클로저 내에서 발생하는 모든 이벤트를 중단시킨 뒤, 클로저의 반환값을 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델을 이벤트 없이 저장

특정 모델을 저장(`save`)할 때만 이벤트를 발생시키고 싶지 않다면, `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

`update`, `delete`, `soft delete`, `restore`, `replicate`에도 Quietly 메서드를 사용할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
