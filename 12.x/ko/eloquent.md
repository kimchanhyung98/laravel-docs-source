# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [속성의 기본값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청킹(Chunking)](#chunking-results)
    - [Lazy 컬렉션으로 청킹하기](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입과 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제(Soft Deleting)](#soft-deleting)
    - [소프트 삭제 모델 쿼리](#querying-soft-deleted-models)
- [모델 정리(Pruning)](#pruning-models)
- [모델 복제(Replicating)](#replicating-models)
- [쿼리 스코프(Query Scopes)](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [대기 속성(Pending Attributes)](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버(Observers)](#observers)
    - [이벤트 음소거(Muting Events)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel에는 여러분의 데이터베이스와 상호작용을 쉽고 즐겁게 만들어주는 객체 관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블은 해당 테이블과 상호작용하기 위한 "모델"과 매칭됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것 외에도, 테이블에 레코드를 삽입(insert), 수정(update), 삭제(delete)할 수 있게 해줍니다.

> [!NOTE]
> 시작하기 전에, 여러분의 애플리케이션 `config/database.php` 설정 파일에 데이터베이스 연결이 올바르게 설정되어 있는지 확인하십시오. 데이터베이스 설정 방법에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 하나 만들어보겠습니다. 일반적으로 모델은 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations) 파일도 함께 생성하려면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성하는 동시에 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 클래스도 같이 생성할 수 있습니다. 이 옵션들은 조합해서 사용하여 여러 클래스를 한 번에 생성할 수 있습니다:

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

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러를 모두 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청을 모두 생성하는 단축키...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

코드만 훑어보면 모델의 모든 속성(attribute)과 연관관계(relationship)를 파악하기 어려울 때가 있습니다. 이럴 땐 `model:show` Artisan 명령어를 사용해 보세요. 이 명령어는 모델의 속성과 관계를 한눈에 볼 수 있는 요약 정보를 제공합니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 기본적인 모델 클래스를 살펴보고 Eloquent의 주요 관례를 알아보겠습니다:

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

위의 예제에서, `Flight` 모델이 어떤 데이터베이스 테이블과 연동되는지 별도로 명시하지 않았다는 점을 눈치챌 수 있습니다. Eloquent는 기본적으로 클래스 이름을 "스네이크 케이스(snake case)"의 복수형으로 변환하여 테이블 이름으로 사용합니다. 즉, `Flight` 모델은 `flights` 테이블, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 매핑됩니다.

만약 여러분의 모델과 테이블 명칭이 이 규칙을 따르지 않는다면, 모델의 `table` 속성을 직접 지정하여 테이블 이름을 명시할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 테이블 이름.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델과 연관된 데이터베이스 테이블에 `id`라는 이름의 기본 키 컬럼이 있다고 가정합니다. 만약 다른 컬럼을 기본 키로 사용하려면, 모델에서 보호된 `$primaryKey` 속성을 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블과 연관된 기본 키.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

추가로, Eloquent는 기본 키가 자동 증가하는 정수형(integer) 값일 것이라 가정합니다. 즉, Eloquent는 자동으로 기본 키를 정수로 변환합니다. 만약 자동 증가되지 않거나 숫자가 아닌 기본 키를 사용하려면, 모델에 공개 속성 `$incrementing`을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동 증가하는지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수형이 아니라면, 모델에서 보호된 `$keyType` 속성을 `string`으로 지정해야 합니다:

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

Eloquent는 각 모델이 기본 키 역할을 할 수 있는 고유 식별 "ID"를 하나 이상 가져야 한다고 요구합니다. Eloquent 모델에서는 "복합" 기본 키(여러 컬럼을 조합한 기본 키)를 지원하지 않습니다. 그러나 테이블의 고유 기본 키 외에 다중 컬럼 고유 인덱스는 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자의 영숫자이며, 전역적으로 고유한 식별자입니다.

만약 자동 증가 정수형 키 대신 UUID 키를 사용하고자 한다면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레잇을 추가하면 됩니다. 물론 모델에는 [UUID 형태의 기본 키 컬럼](/docs/12.x/migrations#column-method-uuid)이 필요합니다:

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

기본적으로 `HasUuids` 트레잇은 모델에 ["정렬 가능한(ordered)" UUID](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 이러한 UUID는 리소그래픽(lexicographical) 순서로 정렬 가능하므로 인덱스 작업에도 효율적입니다.

특정 모델에 대해 UUID 생성 과정을 오버라이드하고 싶다면, 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한, `uniqueIds` 메서드를 사용해 UUID가 할당되어야 할 컬럼을 지정할 수 있습니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델에 새로운 UUID를 생성합니다.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자를 받아야 하는 컬럼 리스트를 반환합니다.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 "ULID"를 UUID 대신 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26자 길이입니다. 정렬 가능한 UUID처럼 ULID도 리소그래픽 순서로 정렬이 가능해 효율적인 DB 인덱싱이 가능합니다. ULID를 사용하려면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레잇을 추가하고, [ULID 형태의 기본 키 컬럼](/docs/12.x/migrations#column-method-ulid)이 있어야 합니다:

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

Eloquent는 기본적으로 여러분의 모델이 사용하는 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 가정합니다. Eloquent는 모델을 생성할 때 또는 수정할 때 이 컬럼 값을 자동으로 지정합니다. 만약 이러한 컬럼을 Eloquent가 자동으로 관리하지 않기를 원한다면, 모델에서 `$timestamps` 속성을 `false`로 설정하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에서 타임스탬프를 사용할지 여부.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델의 타임스탬프 포맷을 커스터마이즈하고 싶다면, `$dateFormat` 속성을 지정하면 됩니다. 이 속성은 데이터베이스 저장 방식과 모델 배열/JSON 직렬화 시의 날짜 포맷을 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 컬럼의 저장 포맷.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프에 사용되는 컬럼명을 변경하려면, 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 정의하면 됩니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프 값을 변경하지 않고 연산을 수행하려면, `withoutTimestamps` 메서드에 클로저를 전달하여 해당 클로저 내부에서 동작하도록 하면 됩니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에서 기본으로 설정된 데이터베이스 연결을 사용합니다. 특정 모델이 다른 연결을 사용하도록 하려면, 모델에 `$connection` 속성을 지정하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 데이터베이스 연결명.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 속성의 기본값

새로 인스턴스화된 모델 객체에는 기본적으로 아무런 속성값이 설정되어 있지 않습니다. 모델의 일부 속성에 기본값을 지정하고 싶다면, 모델의 `$attributes` 속성에서 설정할 수 있습니다. `$attributes` 배열에 위치하는 값들은 실제 데이터베이스에서 읽힌 값처럼 "원시(storable)" 포맷이어야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 속성의 기본값 설정.
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

Laravel은 여러 상황에서 Eloquent의 동작 방식과 "엄격성"을 설정할 수 있는 다양한 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 lazy loading(지연 로딩)을 방지할지 여부를 나타내는 선택적 불리언 인수를 받습니다. 예를 들어, 실무 환경에서는 lazy loading이 남아 있더라도 기존 코드가 정상 동작하도록 개발/테스트 환경에서만 지연 로딩을 비활성화하는 것이 일반적입니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출하면 할당할 수 없는 속성을 대량 할당(mass assignment)할 때 예외를 던지도록 Laravel을 설정할 수 있습니다. 개발 환경에서 의도치 않게 필드가 무시되면서 발생할 수 있는 오류를 예방해 줍니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [관련 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 조회할 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)로서, 모델이 연동된 데이터베이스 테이블을 유연하게 조회할 수 있게 해줍니다. 모델의 `all` 메서드로 해당 테이블의 모든 레코드를 가져올 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

Eloquent의 `all` 메서드는 테이블 내 모든 결과를 반환합니다. 하지만 각 모델은 [쿼리 빌더](/docs/12.x/queries)이므로, 쿼리에 추가 제약 조건을 더한 뒤 `get` 메서드로 원하는 결과만 조회할 수도 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더 역할도 하므로, Laravel의 [쿼리 빌더](/docs/12.x/queries)가 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 자유롭게 이용해 보세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회한 모델 인스턴스가 있을 때, `fresh`와 `refresh` 메서드로 모델을 "새로고침"할 수 있습니다. `fresh` 메서드는 데이터베이스에서 새롭게 모델을 다시 조회하며, 기존 인스턴스에는 영향을 주지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드를 사용하면 해당 인스턴스 자체가 데이터베이스의 최신 데이터로 교체됩니다. 또한, 이미 로드된 모든 연관관계들도 함께 새로고침됩니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

방금 본 것처럼, `all`과 `get` 같은 Eloquent 메서드는 여러 레코드를 반환합니다. 이때 반환되는 값은 일반 PHP 배열이 아니라, `Illuminate\Database\Eloquent\Collection` 인스턴스입니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장하며, 데이터 컬렉션을 다루는 [다양한 유틸리티 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 클로저에서 정의한 조건에 부합하는 모델을 컬렉션에서 제거할 때 사용할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

또한, 기본 컬렉션에서 제공하는 메서드 이외에도 Eloquent 컬렉션 전용 [추가 메서드](/docs/12.x/eloquent-collections#available-methods)도 사용할 수 있습니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하고 있으므로, 배열처럼 foreach 등 반복문에서 직접 사용할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청킹(Chunking)

`all`이나 `get` 메서드로 수만 개가 넘는 Eloquent 레코드를 한 번에 메모리로 불러오면 애플리케이션이 메모리 부족 에러를 겪을 수 있습니다. 이런 대량 데이터 작업에는 `chunk` 메서드를 사용하는 것이 훨씬 효율적입니다.

`chunk` 메서드는 Eloquent 모델의 일부분(청크)을 조회해 클로저에 전달합니다. 한 번에 현재 청크만 메모리에 불러오기 때문에, 많은 모델을 작업할 때 메모리 사용량이 상당히 감소합니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인자는 한 번에 불러올 레코드 개수입니다. 두 번째 인자로 전달된 클로저는 각 청크 조회 시마다 실행됩니다. 각 청크마다 데이터베이스 쿼리가 실행되어 클로저로 전달됩니다.

단, `chunk` 메서드 내부에서 결과를 필터링하면서 동시에 해당 컬럼 값을 업데이트할 경우, 예기치 않고 일관성 없는 결과가 발생할 수 있습니다. 이럴 때는 항상 `chunkById` 메서드를 사용하세요. `chunkById`는 내부적으로 이전 청크 마지막 모델의 `id`보다 큰 레코드만 가져와서 정확도를 보장합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById`는 자체적으로 "where" 조건을 추가하기 때문에, 사용자 정의 조건을 사용할 땐 [논리적 그룹화](/docs/12.x/queries#logical-grouping)를 권장합니다:

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
### Lazy 컬렉션으로 청킹하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게, 내부적으로 쿼리를 청크 단위로 처리합니다. 하지만 각 청크를 콜백에 바로 전달하는 대신, Eloquent 모델의 평탄화된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여, 결과를 단일 스트림처럼 계속 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

마찬가지로, 필터링하면서 결과 컬럼을 업데이트할 때는 `lazyById` 메서드를 사용하는 것이 좋습니다. 내부적으로 마지막 청크의 마지막 모델의 `id`보다 큰 레코드만 계속해서 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id`의 내림차순 정렬로 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드와 비슷하게, `cursor` 메서드는 수만 개에 달하는 Eloquent 모델을 반복하면서 메모리 사용량을 획기적으로 줄여줍니다.

`cursor`는 단 하나의 데이터베이스 쿼리만 실행하며, 모델 인스턴스는 실제 반복문에서 필요할 때 비로소 메모리로 적재됩니다. 즉, 커서를 사용하면 한 번에 한 개의 Eloquent 모델만 메모리에 올라갑니다.

> [!WARNING]
> `cursor`는 오직 한 번에 하나의 모델만 메모리에 있기 때문에, 관계를 eager load할 수 없습니다. 관계를 eager load해야 한다면 [lazy 메서드](#chunking-using-lazy-collections) 사용을 고려하세요.

내부적으로 `cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)은 일반 Laravel 컬렉션이 제공하는 다양한 메서드를 한 번에 한 모델씩 처리하면서 사용할 수 있게 해줍니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor`는 일반 쿼리에 비해 메모리 사용량이 훨씬 적지만, 결국 [PHP의 PDO 드라이버가 모든 원시 쿼리 결과를 내부 버퍼에 캐싱](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)하기 때문에 한계가 있습니다. 아주 많은 레코드를 다루어야 한다면 [lazy 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리 기능을 지원하여, 한 번의 쿼리로 관련 테이블의 정보를 함께 가져올 수 있습니다. 예를 들어, `destinations` 테이블과 목적지별로 비행 내역이 들어있는 `flights` 테이블이 있다고 가정해봅시다. `flights` 테이블에는 비행이 목적지에 도착한 시점을 저장하는 `arrived_at` 컬럼이 있습니다.

쿼리 빌더의 `select`와 `addSelect` 서브쿼리 기능을 사용하면, 아래와 같이 모든 목적지와 각 목적지에 가장 최근 도착한 비행의 이름을 단일 쿼리로 조회할 수 있습니다:

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

또한, 쿼리 빌더의 `orderBy` 함수는 서브쿼리를 지원합니다. 위의 비행 예에서, 각 목적지에 가장 최근 도착한 시간을 기준으로 목적지를 정렬할 수 있습니다. 이 역시 단 한 번의 데이터베이스 쿼리로 처리됩니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델/집계 조회

특정 조건에 부합하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 메서드를 통해 단일 레코드만 조회할 수도 있습니다. 이 메서드들은 컬렉션이 아닌 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 모델 조회...
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 조건에 맞는 첫 번째 모델을 간편하게 조회하는 대안...
$flight = Flight::firstWhere('active', 1);
```

가끔 원하는 레코드가 없을 때 다른 동작을 하고 싶을 수 있습니다. `findOr`, `firstOr` 메서드는 레코드가 없을 경우 주어진 클로저를 실행합니다. 클로저의 반환값이 메서드 반환값이 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Not Found 예외

특정 모델을 찾지 못했을 때 예외를 던지고 싶을 때가 있습니다. 라우트나 컨트롤러에서 유용합니다. `findOrFail`, `firstOrFail` 메서드는 쿼리 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 잡히지 않으면, 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍으로 데이터베이스에서 레코드를 찾으려고 시도합니다. 찾지 못하면, 첫 번째 배열과 두 번째(선택적) 배열을 병합한 값으로 새로운 레코드를 데이터베이스에 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 마찬가지로 주어진 값과 일치하는 레코드를 찾으려고 시도합니다. 그러나 찾지 못하면, 새로운 모델 인스턴스만 반환하며, 이 인스턴스는 데이터베이스에 저장되지 않은 상태입니다. 이 경우엔 `save` 메서드를 직접 호출해야 합니다:

```php
use App\Models\Flight;

// 이름으로 조회, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 이름·delayed·arrival_time로 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 Flight 인스턴스 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 name·delayed·arrival_time 속성으로 새 인스턴스 반환
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델로 조회할 때도, Laravel [쿼리 빌더](/docs/12.x/queries)를 통해 제공되는 `count`, `sum`, `max` 등의 [집계 메서드](/docs/12.x/queries#aggregates)를 그대로 사용할 수 있습니다. 이들 메서드는 Eloquent 모델 인스턴스가 아닌 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입과 수정

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때는 단순히 조회뿐 아니라 새로운 레코드도 데이터베이스에 손쉽게 삽입할 수 있습니다. 새로운 레코드를 삽입하려면 모델을 인스턴스화하고, 속성을 지정한 후 `save` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 비행 정보를 데이터베이스에 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        // 유효성 검사...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

이 예제에서는 HTTP 요청에서 넘어온 name 필드를 `App\Models\Flight` 인스턴스의 name 속성에 할당했습니다. `save` 메서드를 호출하면 해당 레코드가 데이터베이스에 삽입됩니다. `created_at`, `updated_at` 타임스탬프는 자동으로 지정되므로 따로 설정할 필요가 없습니다.

또는, `create` 메서드로 한 줄에 새 모델을 저장할 수도 있습니다. 이때 삽입된 모델 인스턴스가 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하려면 모델 클래스의 `fillable` 또는 `guarded` 속성 중 하나를 반드시 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당(마스 어사인) 취약점으로부터 보호되기 때문입니다. 마스 어사인에 대한 상세 내용은 [mass assignment 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

`save` 메서드는 이미 데이터베이스에 존재하는 모델의 속성도 수정할 수 있습니다. 모델을 조회하여 필요한 속성을 수정한 뒤 `save`를 호출하면 됩니다. `updated_at` 타임스탬프도 자동으로 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

가끔 기존 모델을 수정하거나, 일치하는 모델이 없으면 새로 생성해야 할 수도 있습니다. 이럴 땐 `firstOrCreate`와 유사하게, `updateOrCreate` 메서드를 사용하면 `save` 없이도 저장까지 자동으로 처리할 수 있습니다.

아래 예시는 `Oakland`에서 `San Diego`로 출발하는 비행이 이미 있다면 `price`와 `discounted` 컬럼이 업데이트되고, 없다면 두 배열을 병합해 새 비행 정보가 생성됩니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

`firstOrCreate`나 `updateOrCreate` 사용 시, 새 모델이 만들어졌는지 기존 모델이 업데이트됐는지 모를 수 있습니다. `wasRecentlyCreated` 속성으로 이를 확인할 수 있습니다:

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // 새 비행 레코드 삽입됨...
}
```

<a name="mass-updates"></a>
#### 대량 업데이트

특정 쿼리에 부합하는 여러 모델을 한 번에 업데이트할 수도 있습니다. 아래 예시는 `active` 상태이고 `destination`이 `San Diego`인 모든 비행을 `delayed` 상태로 표시합니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼/값 쌍을 배열로 받으며, 영향을 받은 행의 수를 반환합니다.

> [!WARNING]
> Eloquent로 대량 업데이트를 실행하면, 대상 모델에 대해 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 이는 대상 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 이력 확인

Eloquent는 내부적으로 모델의 상태를 파악해 속성 변경 이력을 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

`isDirty`는 모델을 조회한 후, 하나 이상의 속성이 바뀌었는지 판단합니다. 특정 속성명이나 속성명 배열을 인자로 전달하면 해당 속성이 변경됐는지 확인합니다. 반대로 `isClean`은 조회 이후 변하지 않은 속성을 판단합니다:

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

`wasChanged`는 최근 저장 시점에 속성이 변경됐는지 판단합니다. 필요시 속성명을 넘겨 특정 속성의 변경 여부도 확인 가능합니다:

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

`getOriginal` 메서드는 모델을 조회한 시점의 원본 속성 배열을 반환합니다. 특정 속성의 원래 값을 얻으려면 속성명을 넘기면 됩니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성값 배열...
```

`getChanges`는 최근 저장 시점에 변경된 속성 배열을, `getPrevious`는 저장 전 원본 값을 반환합니다:

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
### 대량 할당(Mass Assignment)

`create` 메서드를 사용하면 한 줄로 새 모델을 저장할 수도 있습니다. 이때 삽입된 모델 인스턴스가 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create`를 사용하려면 모델 클래스에 반드시 `fillable` 또는 `guarded` 속성 중 한 가지를 지정해야 합니다. 이 속성들은, 모든 Eloquent 모델이 기본적으로 대량 할당(mass assignment) 취약점으로부터 보호되도록 하기 위함입니다.

대량 할당 취약점이란, 사용자가 의도하지 않은 HTTP 요청 필드를 보내 해당 값이 데이터베이스 컬럼까지 변경되도록 만드는 것입니다. 예를 들어, 악의적인 사용자가 요청에 `is_admin` 파라미터를 끼워넣어 관리자 권한을 탈취하는 일이 발생할 수 있습니다.

따라서 대량 할당을 지원하는 속성을 반드시 명확하게 지정해야 합니다. 예를 들어, `Flight` 모델의 `name` 속성만 대량 할당이 가능하도록 할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 가능한 속성 배열.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

이렇게 하면, `create` 메서드로 안전하게 데이터베이스에 레코드를 삽입할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드로 속성을 한 번에 채워 넣을 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼 역시 대량 할당을 지원하려면, 각 컬럼의 키를 모델의 `$fillable` 배열에 명시적으로 지정해야 합니다. 보안을 위해 Laravel은 `guarded` 사용 시 중첩된 JSON 속성의 업데이트를 지원하지 않습니다:

```php
/**
 * 대량 할당 가능한 속성 배열.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 대량 할당 허용

모델의 모든 속성을 대량 할당 가능하게 하려면, `$guarded`를 빈 배열로 지정하면 됩니다. 단, 이 경우에는 Eloquent의 `fill`, `create`, `update` 메서드에 넘길 배열을 항상 직접 설계해야 안전합니다:

```php
/**
 * 대량 할당이 불가능한 속성 배열.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로 `$fillable`에 포함되지 않은 속성은 대량 할당 시 조용히 무시됩니다. 실무 환경에서는 이 동작이 당연하지만, 개발 환경에서는 모델에 값이 적용되지 않아 디버깅에 혼동을 줄 수 있습니다.

이럴 때는, 할당이 불가능한 속성을 대량 할당하려고 시도했을 때 예외를 던지도록 Laravel을 설정할 수 있습니다. 보통은 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트(Upserts)

Eloquent의 `upsert` 메서드를 사용하면, 레코드를 한 번에 "업데이트 또는 삽입"하는 원자적 작업을 처리할 수 있습니다. 첫 번째 인수에는 삽입/업데이트 대상 값(여러 건), 두 번째 인수는 레코드를 고유하게 식별할 컬럼(들), 세 번째 인수는 이미 존재하는 레코드가 있을 때 업데이트할 컬럼들을 지정합니다. `upsert`는 타임스탬프가 활성화되어 있다면 `created_at`, `updated_at`도 자동 설정합니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서, `upsert` 메서드 두 번째 인수에 지정한 컬럼은 "primary" 또는 "unique" 인덱스가 있어야 합니다. MariaDB, MySQL 드라이버의 경우 두 번째 인수는 무시되고, 테이블의 "primary/unique" 인덱스로만 중복 여부를 식별합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 예시처럼 먼저 모델을 조회하여 삭제할 수도 있지만, 기본 키를 알고 있다면 굳이 조회하지 않고 `destroy` 메서드를 통해 여러 방법으로 삭제할 수 있습니다. 단일 기본 키뿐 아니라 여러 개, 배열, [컬렉션](/docs/12.x/collections) 모두 지원합니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용하는 경우, `forceDestroy`로 완전히 삭제할 수 있습니다:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 조회한 뒤 `delete`를 호출하여, 모든 모델의 `deleting`, `deleted` 이벤트가 제대로 발생하도록 동작합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

물론, 쿼리 빌더를 사용해 조건에 맞는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래 예시는 비활성화된 모든 비행을 삭제하며, 대량 업데이트처럼 모델 이벤트는 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블 내의 모든 모델을 삭제하려면, 조건 없이 쿼리를 실행하면 됩니다:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent의 대량 삭제 구문을 사용할 때, 삭제된 모델에 대해 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 모델을 실제로 조회하지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제(Soft Deleting)

Eloquent는 데이터베이스에서 레코드를 실제로 삭제하지 않고 "소프트 삭제"할 수도 있습니다. 소프트 삭제 시, 레코드는 삭제되지 않고 `deleted_at` 속성에 삭제된 날짜와 시간이 기록됩니다. 소프트 삭제를 활성화하려면, 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레잇을 추가하면 됩니다:

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
> `SoftDeletes` 트레잇은 자동으로 `deleted_at` 속성을 `DateTime`/`Carbon` 인스턴스로 캐스팅합니다.

데이터베이스 테이블에도 `deleted_at` 컬럼이 필요합니다. Laravel [스키마 빌더](/docs/12.x/migrations)의 헬퍼 메서드로 이 컬럼을 쉽게 추가할 수 있습니다:

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

이제 모델의 `delete`를 호출하면, `deleted_at` 컬럼에 현재 날짜/시간이 지정되고, 레코드는 테이블에 남아 있게 됩니다. 소프트 삭제 모델을 쿼리할 때는 자동으로 소프트 삭제된 레코드가 제외됩니다.

특정 모델이 소프트 삭제됐는지 확인하려면, `trashed` 메서드를 사용할 수 있습니다:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

가끔 "삭제"된 소프트 삭제 모델을 복원하고 싶을 수 있습니다. 모델 인스턴스에서 `restore`를 호출하면, `deleted_at` 컬럼 값이 `null`로 설정되어 복구됩니다:

```php
$flight->restore();
```

복수의 모델도 쿼리 빌더로 한 번에 복원할 수 있으며, "대량" 연산이기 때문에 복원된 모델에 이벤트는 발생하지 않습니다:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[관계](/docs/12.x/eloquent-relationships) 쿼리에서도 `restore`를 사용할 수 있습니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 완전 삭제(영구 삭제)

어떤 경우에는 데이터베이스에서 진짜로 모델을 제거해야 할 수도 있습니다. 이럴 때는 `forceDelete` 메서드로 완전 삭제를 수행합니다:

```php
$flight->forceDelete();
```

Eloquent 관계 쿼리에서도 `forceDelete`를 사용할 수 있습니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함

앞서 본 것처럼, 소프트 삭제 모델은 쿼리 결과에서 기본적으로 제외됩니다. 하지만 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제 모델도 함께 조회할 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 `withTrashed`를 사용할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed` 메서드를 사용하면 **소프트 삭제된 모델만** 조회할 수 있습니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리(Pruning)

특정 시점 이후로 사용하지 않는 모델을 정기적으로 삭제하고 싶을 때가 있습니다. 이를 위해, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레잇을 정리 대상 모델에 추가할 수 있습니다. 트레잇 추가 후 `prunable` 메서드를 구현해서 더 이상 필요 없는 모델을 조회하는 Eloquent 쿼리 빌더를 반환하십시오:

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
     * 정리 대상 모델 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

모델에 `Prunable`을 지정했다면, 삭제 전에 호출되는 `pruning` 메서드도 정의할 수 있습니다. 이 메서드는 모델과 연관된 파일 등 추가 리소스를 미리 삭제할 때 유용합니다:

```php
/**
 * 정리 전 준비 작업.
 */
protected function pruning(): void
{
    // ...
}
```

정리 대상 모델을 준비한 후에는 애플리케이션의 `routes/console.php`에 `model:prune` Artisan 명령어를 스케줄링해야 합니다. 이 명령어를 실행할 적절한 주기는 자유롭게 선택하면 됩니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령어는 애플리케이션의 `app/Models` 내에서 "Prunable" 모델을 자동으로 감지합니다. 모델이 다른 위치에 있다면, `--model` 옵션으로 클래스명을 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델을 제외하고 나머지만 정리하고 싶을 때는 `--except` 옵션을 사용할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`prunable` 쿼리를 테스트하고 싶다면 `--pretend` 옵션으로 `model:prune` 명령을 실행해 보세요. 실제 실행 대신 삭제될 레코드 개수만 리포트됩니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델도 정리 쿼리에 걸리면 영구적으로 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리(Mass Pruning)

모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레잇이 지정되어 있으면, 정리시 모델을 조회하지 않고 대량 삭제 쿼리로 처리합니다. 따라서 각 모델의 `pruning` 메서드나 모델 이벤트(`deleting`, `deleted`)는 호출되지 않으므로, 정리 작업이 훨씬 효율적입니다:

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
     * 정리 대상 모델 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제(Replicating)

기존 모델 인스턴스를 저장하지 않은 상태로 복사해야 할 때는 `replicate` 메서드를 사용하세요. 이는 여러 속성이 동일한 여러 인스턴스로 작업할 때 특히 유용합니다:

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

복제 대상에서 하나 이상의 속성을 제외하고 싶을 때는 `replicate` 메서드에 배열로 속성명을 전달하세요:

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
## 쿼리 스코프(Query Scopes)

<a name="global-scopes"></a>
### 글로벌 스코프

글로벌 스코프를 사용하면 주어진 모델의 모든 쿼리에 항상 특정 제약 조건을 추가할 수 있습니다. Laravel의 [소프트 삭제](#soft-deleting)도 글로벌 스코프를 이용해 "삭제되지 않은" 모델만 조회하도록 구현되어 있습니다. 여러분도 직접 글로벌 스코프를 작성하면, 지정 모델의 모든 쿼리에 자동으로 조건을 적용할 수 있어 편리합니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성

새 글로벌 스코프를 만들려면 `make:scope` Artisan 명령어를 사용하세요. 이 명령어는 생성된 스코프를 `app/Models/Scopes` 디렉터리에 둡니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프를 작성하는 방법은 간단합니다. 먼저 `make:scope`로 생성된 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현합니다. 이때 반드시 `apply` 메서드를 작성해야 하며, 필요에 따라 `where` 조건이나 기타 연산자를 쿼리에 추가할 수 있습니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 Eloquent 쿼리 빌더에 스코프를 적용합니다.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프에서 쿼리의 select 절에 컬럼을 추가할 때는 기존 select 절이 의도치 않게 대체되는 것을 막기 위해 반드시 `select` 대신 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

글로벌 스코프를 모델에 지정하려면, 모델에 `ScopedBy` 속성(Attribute)을 추가하면 됩니다:

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

또는, 모델의 `booted` 메서드를 오버라이드하고, `addGlobalScope` 메서드를 호출해서 직접 추가할 수도 있습니다. 이 메서드는 스코프 인스턴스를 인수로 받습니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예시처럼 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 호출 시 다음과 같은 SQL쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

단순한 스코프의 경우, 별도의 클래스를 만들지 않고 클로저로 글로벌 스코프를 정의할 수도 있습니다. 클로저로 글로벌 스코프를 지정하는 경우에는 `addGlobalScope`의 첫 번째 인자로 임의의 스코프명을 전달합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
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

특정 쿼리에서 글로벌 스코프를 제거하려면, `withoutGlobalScope` 메서드를 사용합니다. 스코프 클래스명을 인수로 넘기면 됩니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의된 스코프라면, 추가 시 지정한 문자열 이름을 넘기면 됩니다:

```php
User::withoutGlobalScope('ancient')->get();
```

여러개의 또는 모든 글로벌 스코프를 제거하려면, `withoutGlobalScopes` 또는 `withoutGlobalScopesExcept` 메서드를 사용하세요:

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 주어진 글로벌 스코프 외 모두 제거
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 사용하는 쿼리 조건 세트를 메서드 형태로 정의해서, 애플리케이션 전역 어디에서든 쉽게 재사용할 수 있게 해줍니다. 예를 들어, "인기 많은" 사용자를 자주 가져와야 한다면, Eloquent 메서드에 `Scope` 속성을 달아 스코프를 정의하면 됩니다.

스코프 메서드는 항상 동일한 쿼리 빌더 인스턴스나 `void`를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * "인기 있는" 사용자만 포함하는 쿼리를 스코프화.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * "활성화"된 사용자만 포함하는 쿼리를 스코프화.
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

스코프를 정의했다면, 모델 쿼리시 메서드처럼 바로 호출할 수 있습니다. 여러 스코프를 연결(chain)해 사용할 수도 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or` 연산자로 조합하고 싶을 때는 [논리 그룹화](/docs/12.x/queries#logical-grouping)의 올바른 동작을 위해 클로저를 사용할 수도 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

다만 이 작업이 번거로울 수 있으므로, Laravel은 클로저 없이도 스코프 메서드 체인을 연결할 수 있는 "higher order" `orWhere`를 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 파라미터를 받는 동적 스코프

스코프에 인자를 넘겨 다양한 조건으로 사용할 수도 있습니다. 스코프 메서드에 추가 파라미터를 정의하기만 하면 됩니다. (항상 `$query` 다음에 인자를 추가하세요):

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 포함하는 쿼리 스코프.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

호출 시, 인자를 전달하면 됩니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 속성(Pending Attributes)

스코프를 통해 스코프에 사용한 속성과 동일한 속성을 가진 모델도 만들고 싶다면, 쿼리 빌더의 `withAttributes` 메서드를 활용하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * "초안"만 포함하는 쿼리 스코프.
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

`withAttributes`는 전달된 속성으로 쿼리에 `where` 조건을 추가하고, 해당 스코프로 생성되는 모델에도 동일한 속성을 지정합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes`가 쿼리에는 조건을 추가하지 않고 모델 생성시에만 속성 값을 지정하도록 하려면, `asConditions` 인자를 `false`로 지정하세요:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "동일한" 모델인지 확인해야 할 때가 있습니다. `is`, `isNot` 메서드를 사용하면 두 모델이 기본 키, 테이블, 데이터베이스 연결명이 동일한지 빠르게 검사할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`와 `isNot`는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](/docs/12.x/eloquent-relationships)에서 사용시에도 유용합니다. 쿼리를 추가로 발행하지 않고도 관련 모델과 비교할 수 있습니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 사이드 애플리케이션으로 바로 브로드캐스트하고 싶으신가요? Laravel의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 문서를 참고하세요.

Eloquent 모델은 다음과 같은 여러 시점에 이벤트를 디스패치(발생)합니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 모델이 DB에서 조회될 때
- `creating`, `created`: 새로운 모델이 처음 저장될 때
- `updating`, `updated`: 기존 모델 수정 후 `save` 호출 시
- `saving`, `saved`: 모델이 생성·수정될 때(속성 변경 여부와 무관)
- `-ing`(동작 전), `-ed`(동작 후)

모델 이벤트를 리스닝하려면, Eloquent 모델에 `$dispatchesEvents` 속성을 정의합니다. 이 속성에 생명주기 별로 [이벤트 클래스](/docs/12.x/events)를 매핑할 수 있습니다. 각 이벤트 클래스는 생성자로 해당 모델 인스턴스를 받습니다:

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
     * 모델 이벤트와 클래스 매핑.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트를 정의·매핑한 뒤에는, [이벤트 리스너](/docs/12.x/events#defining-listeners)로 필요 로직을 처리할 수 있습니다.

> [!WARNING]
> Eloquent의 대량 업데이트나 삭제 구문을 사용할 때는 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다. 대상 모델이 실제로 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용

커스텀 이벤트 클래스 대신, 각 이벤트에 반응하는 클로저를 등록할 수도 있습니다. 보통 모델의 `booted` 메서드에서 클로저를 등록합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면, [큐 처리 가능한 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 사용할 수 있습니다. 애플리케이션의 [큐](/docs/12.x/queues)를 이용해 이벤트 리스너를 백그라운드에서 실행하도록 할 수 있습니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버(Observers)

<a name="defining-observers"></a>
#### 옵저버 정의

하나의 모델에 대해 여러 이벤트를 리스닝해야 한다면, "옵저버" 클래스로 모든 리스너를 한 곳에 모아 둘 수 있습니다. 옵저버 클래스의 메서드명은 리스닝할 Eloquent 이벤트명을 따릅니다. 각 메서드는 모델 인스턴스를 인수로 받습니다. `make:observer` Artisan 명령어로 쉽고 빠르게 옵저버 클래스를 생성할 수 있습니다:

```shell
php artisan make:observer UserObserver --model=User
```

해당 명령은 새 옵저버를 `app/Observers` 디렉터리에 생성합니다. 디렉터리가 없다면 Artisan이 대신 만들어줍니다. 기본 형태는 다음과 같습니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 핸들러.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 핸들러.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 핸들러.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 핸들러.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 핸들러.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면, 해당 모델에 `ObservedBy` 속성을 추가합니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, `AppServiceProvider`의 `boot` 메서드에서 `observe`로 수동 등록할 수도 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버는 `saving`, `retrieved` 등 추가적인 이벤트도 리스닝할 수 있습니다. 자세한 내용은 [이벤트](#events) 문서에서 확인하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

트랜잭션 내에서 모델이 생성되는 경우, 옵저버 핸들러를 트랜잭션 커밋 후에만 실행하도록 강제할 수 있습니다. 옵저버 클래스가 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면, 트랜잭션 중일 때는 커밋 시점에, 그렇지 않을 때는 바로 이벤트가 처리됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 핸들러.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거(Muting Events)

때로는 모델에서 발생하는 모든 이벤트를 일시적으로 "음소거"해야 할 때가 있습니다. `withoutEvents` 메서드는 클로저를 인수로 받아, 해당 클로저 내부에서 발생하는 모든 모델 이벤트를 비활성화합니다. 클로저의 반환값이 곧 `withoutEvents`의 반환값이 됩니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 한 모델만 이벤트 없이 저장

특정 모델을 이벤트 없이 "저장"해야 할 때는 `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

한 모델의 "업데이트", "삭제", "소프트 삭제", "복원", "복제" 등도 각각 아래처럼 처리할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
