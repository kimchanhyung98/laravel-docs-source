# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키(Primary Keys)](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성값](#default-attribute-values)
    - [Eloquent 엄격 모드 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 단위로 처리하기](#chunking-results)
    - [Lazy 컬렉션을 사용한 청크 처리](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계값 조회하기](#retrieving-single-models)
    - [모델 조회 또는 생성하기](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제하기](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 정리(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending Attributes](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용하기](#events-using-closures)
    - [옵서버(Observers)](#observers)
    - [이벤트 음소거(Muting)](#muting-events)

<a name="introduction"></a>
## 소개

라라벨은 데이터베이스와의 상호작용을 쉽고 즐겁게 만들어주는 ORM(Object-Relational Mapper)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때 각 데이터베이스 테이블은 해당 테이블과 상호작용하는 "모델(Model)"과 연결됩니다. Eloquent 모델을 이용하면 데이터베이스 테이블에서 레코드를 조회하는 것뿐 아니라, 레코드 추가, 수정, 삭제도 할 수 있습니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 먼저 구성해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 만들어보겠습니다. 모델 클래스는 일반적으로 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성할 때는 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 사용하면 됩니다.

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 요청(form request) 등 다양한 유형의 클래스도 동시에 생성할 수 있습니다. 이러한 옵션들은 조합하여 여러 클래스를 한 번에 만들 수 있습니다.

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

# 모델, FlightController 리소스 클래스, 그리고 폼 요청 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러를 한 번에 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청을 모두 한 번에 생성하는 단축키...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 관계 확인

때로는 코드만 훑어봐서는 모델에 어떤 속성(attribute)과 연관관계(relationship)가 있는지 알기 어려울 수 있습니다. 이럴 때는 Artisan의 `model:show` 명령어를 사용해보세요. 이 명령어는 모델의 모든 속성과 연관관계를 한눈에 살펴볼 수 있도록 요약하여 보여줍니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 저장됩니다. 이제 기본 모델 클래스를 살펴보고, Eloquent의 주요 관례(convention)에 대해 알아보겠습니다.

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

위의 예시에서 보셨듯이, Eloquent에게 어떤 데이터베이스 테이블이 `Flight` 모델과 연결되는지 별도로 지정하지 않았습니다. Eloquent는 기본적으로 클래스 이름을 스네이크 케이스로 변환한 뒤 복수형(plural)으로 만들어 테이블 이름으로 사용합니다. 즉, `Flight` 모델은 `flights` 테이블에, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 데이터를 저장한다고 가정합니다.

만약 모델과 연결되는 데이터베이스 테이블이 이 규칙을 따르지 않는다면, 모델의 `table` 속성(property)을 정의하여 테이블 이름을 직접 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연결된 테이블명.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키(Primary Keys)

Eloquent는 각 모델에 연결된 데이터베이스 테이블이 `id`라는 이름의 기본 키(primary key) 컬럼을 가진다고 가정합니다. 만약 다른 컬럼을 기본 키로 사용하고 싶다면, 모델에 `protected $primaryKey` 속성을 정의하여 변경할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블의 기본 키 컬럼명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 Eloquent는 기본 키가 자동 증가하는 정수(integer) 값이라고 간주하여, 자동으로 정수로 형변환합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용하고 싶다면, 모델의 `public $incrementing` 속성을 `false`로 지정해야 합니다.

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

기본 키가 정수 타입이 아니라면, 모델에 `protected $keyType` 속성을 정의하고 값을 `string`으로 지정해야 합니다.

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
#### "복합" 기본 키(Composite Primary Keys)

Eloquent 모델은 최소한 하나의 고유하게 식별할 수 있는 "ID"를 기본 키로 가져야 합니다. Eloquent 모델에서는 "복합" 기본 키(여러 컬럼으로 이루어진 기본 키)는 지원하지 않습니다. 하지만 테이블의 고유한 기본 키와 별도로 여러 컬럼으로 구성된 유니크 인덱스를 데이터베이스에 추가하는 것은 가능합니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할 수도 있습니다. UUID(범용 고유 식별자)는 36자리의 문자열로, 전세계적으로 유일한 식별 값입니다.

모델의 기본 키로 UUID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트(trait)를 모델에 적용하면 됩니다. 물론 해당 모델이 [UUID 컬럼 타입](/docs/12.x/migrations#column-method-uuid)의 기본 키 컬럼을 갖추고 있어야 합니다.

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

기본적으로 `HasUuids` 트레이트는 모델에 ["순서형(Ordered) UUID"](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 이 UUID는 사전식(lexicographical) 정렬이 가능하여 데이터베이스 인덱싱 시 더 효율적입니다.

특정 모델에서 UUID 생성 방식을 오버라이드하려면 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한 어떤 컬럼에 UUID를 부여할지 지정하고 싶다면 `uniqueIds` 메서드를 모델에 구현할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델용 UUID 새로 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 유니크 식별자를 부여할 컬럼 지정
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26글자이며, 순서형 UUID처럼 사전식 정렬이 가능합니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 적용하고, [ULID 컬럼 타입](/docs/12.x/migrations#column-method-ulid)의 기본 키 컬럼을 갖추어야 합니다.

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

Eloquent는 기본적으로 모델과 연결된 데이터베이스 테이블에 `created_at`, `updated_at` 컬럼이 있다고 가정합니다. 모델이 생성 또는 수정될 때 이 컬럼들을 자동으로 관리합니다. 이러한 컬럼의 자동 관리를 원하지 않는다면, 모델의 `$timestamps` 속성을 `false`로 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 타임스탬프를 관리할지 여부.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프의 저장 형식을 커스터마이즈하고 싶다면, 모델의 `$dateFormat` 속성을 설정하세요. 이 속성은 데이터베이스에 저장될 때와, 모델이 배열이나 JSON으로 직렬화(serialization)될 때의 형식에 모두 적용됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 컬럼 저장 형식.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프에 사용되는 컬럼명을 변경하고 싶다면, 모델에 `CREATED_AT`와 `UPDATED_AT` 상수를 정의하면 됩니다.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프가 변경되지 않도록 모델 연산을 수행하고 싶을 때는, `withoutTimestamps` 메서드에 클로저를 넘겨 해당 범위 내에서 작업을 처리할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 사용하는 데이터베이스 연결을 바꾸고 싶다면, 모델에 `$connection` 속성을 정의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 데이터베이스 연결 이름.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성값

새롭게 인스턴스화한 모델 객체는 기본적으로 아무런 속성값도 가지고 있지 않습니다. 특정 속성의 기본값을 지정하고 싶다면 `$attributes` 속성을 모델에 정의할 수 있습니다. `$attributes` 배열의 값들은 데이터베이스에서 읽어온 "저장 가능한" 원시 형태여야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 속성의 기본값.
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
### Eloquent 엄격 모드 설정

라라벨은 Eloquent의 동작이나 "엄격함(strictness)"을 다양한 상황에 맞게 설정할 수 있는 여러 메서드를 제공합니다.

우선, `preventLazyLoading` 메서드는 "지연 로딩(lazy loading)"이 방지되어야 하는지를 나타내는 불리언 인수를 선택적으로 받을 수 있습니다. 예를 들어, 운영 환경에서는 지연 로딩을 허용하되, 개발 환경에서는 실수로 코드에 지연 로딩이 남아 있는 경우 에러를 방지하고자 막을 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출해, 채워질 수 없는(unfillable) 속성에 값을 할당하려 할 때 예외를 발생하도록 할 수 있습니다. 이 기능은, 모델의 `fillable` 배열에 없는 속성에 값을 채우는 실수를 개발 중에 빨리 발견하는 데 도움이 됩니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 준비했다면, 이제 데이터베이스에서 데이터를 조회할 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)처럼 동작하며, 연결된 테이블에 대해 다양한 방식으로 유연하게 쿼리를 작성할 수 있습니다. 모델의 `all` 메서드를 호출하면 해당 모델과 연결된 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

Eloquent의 `all` 메서드는 모델의 테이블 내 모든 결과를 반환합니다. 하지만 각 Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries)이기도 하므로, 쿼리에 조건을 추가하고 `get` 메서드를 호출해 원하는 결과를 가져올 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더 역할도 하므로, 라라벨의 [쿼리 빌더](/docs/12.x/queries)가 제공하는 다양한 메서드들을 함께 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 이들 메서드도 유용하게 활용하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회해온 Eloquent 모델 인스턴스가 있다면, `fresh`와 `refresh` 메서드를 통해 모델을 "새로고침"할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회하여, 기존 인스턴스와는 별도의 새로운 인스턴스를 반환합니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 값으로 다시 불러와서 갱신합니다. 또한 이미 로드된 모든 연관관계도 새롭게 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

지금까지 살펴본 것처럼 Eloquent의 `all`이나 `get` 같은 메서드는 여러 레코드를 한 번에 조회합니다. 이때 반환되는 값은 단순한 PHP 배열이 아니라, `Illuminate\Database\Eloquent\Collection` 인스턴스입니다.

Eloquent의 `Collection` 클래스는 라라벨의 기본 `Illuminate\Support\Collection` 클래스를 상속합니다. 이 클래스는 데이터 컬렉션을 다루는 데 유용한 [다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 사용하면, 전달된 클로저의 결과에 따라 컬렉션에서 모델을 제외할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

라라벨의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 클래스에는 [Eloquent 모델 컬렉션에서만 사용 가능한 전용 메서드](/docs/12.x/eloquent-collections#available-methods)들도 준비되어 있습니다.

모든 라라벨 컬렉션은 PHP의 iterable 인터페이스를 구현하고 있기 때문에, 일반 배열처럼 반복문으로 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 단위로 처리하기

`all`이나 `get` 메서드를 사용해 수만 건 이상의 Eloquent 레코드를 한 번에 로드하려 하면, 애플리케이션이 메모리를 과도하게 소모할 수 있습니다. 이런 경우 보다 효율적인 처리를 위해 `chunk` 메서드를 사용할 수 있습니다.

`chunk` 메서드는 Eloquent 모델을 남은 전체가 아니라, 일부 단위(청크)로 나누어 처리합니다. 즉, 현재 청크에 해당하는 모델만 한 번에 조회하고, 이들만 클로저로 전달해서 처리하기 때문에, 대량의 모델을 다룰 때 메모리 사용량이 크게 줄어듭니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 번에 조회할 레코드 개수입니다. 두 번째 인수로 전달하는 클로저는 각 청크마다 한 번씩 호출됩니다. 내부적으로 각 청크마다 별도의 데이터베이스 쿼리가 실행됩니다.

조회 결과를 특정 컬럼 기준으로 필터링하면서, 동시에 그 컬럼의 값을 업데이트하는 작업을 한다면 `chunk` 메서드 대신 `chunkById` 메서드를 사용해야 안전합니다. 그렇지 않으면 처리 도중 예상치 못한 결과가 발생할 수 있습니다. `chunkById`는 항상 이전 청크에서 마지막으로 처리된 모델의 `id` 컬럼보다 큰 값만을 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 내부적으로 자체적으로 "where" 조건을 쿼리에 추가하므로, 자신의 쿼리 조건을 클로저로 논리 그룹핑해서 사용하는 것이 좋습니다.

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
### Lazy 컬렉션을 사용한 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게, 내부적으로 쿼리를 청크 단위로 실행합니다. 하지만 `chunk`가 각 청크를 직접 콜백 함수에 넘기는 것과 달리, `lazy`는 평면화(flattened)된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환합니다. 이를 통해 전체 결과를 하나의 스트림처럼 순회할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

결과를 필터링하며 동시에 컬럼 값을 업데이트해야 할 때는 `lazy` 대신 `lazyById` 메서드를 사용하세요. 내부적으로, 이 메서드는 이전 청크의 마지막 모델보다 큰 `id` 값만을 읽어들입니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id` 컬럼의 내림차순 기준으로 결과를 필터링하여 읽어들일 수도 있습니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy` 메서드와 비슷하게, `cursor` 메서드도 수만 건에 이르는 Eloquent 모델 레코드를 순회할 때 애플리케이션의 메모리 사용량을 크게 줄여줍니다.

`cursor` 메서드는 단 한 번의 데이터베이스 쿼리만 실행하며, 각 Eloquent 모델은 실제로 반복문에서 사용할 때 그때그때 메모리상에 "하이드레이션(hydration)"됩니다. 즉, 반복을 진행하는 동안 한 번에 메모리에 올라가는 모델 객체는 1개뿐입니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 하나의 모델만 메모리에 올리기 때문에, 관계(relationship)의 eager loading을 지원하지 않습니다. 관계를 한꺼번에 미리 로드해야 할 경우 [lazy 메서드](#chunking-using-lazy-collections)의 사용을 고려하세요.

내부적으로 `cursor` 메서드는 PHP [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 사용해서 동작합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`가 반환하는 값은 `Illuminate\Support\LazyCollection` 인스턴스입니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)을 사용하면, 라라벨 컬렉션의 다양한 메서드를 한 번에 하나의 모델만 메모리에 올리면서 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

비록 `cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, 결국에는 한계에 도달할 수 있습니다. 그 이유는 [PHP의 PDO 드라이버가 모든 원시 쿼리 결과를 내부 버퍼에 캐싱하기 때문](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 정말 많은 수의 Eloquent 레코드를 다루어야 한다면, [lazy 메서드](#chunking-using-lazy-collections)를 사용하는 것이 더 안전합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 select

Eloquent는 고급 서브쿼리도 지원하므로, 한 번의 쿼리로 연관 테이블에서 원하는 정보를 함께 조회할 수 있습니다. 예를 들어, 목적지 `destinations` 테이블과 각 목적지로 이동하는 `flights` 테이블이 있다고 가정해봅시다. `flights` 테이블에는 해당 비행기가 목적지에 도착한 시간을 나타내는 `arrived_at` 컬럼이 있습니다.

쿼리 빌더의 `select` 및 `addSelect` 메서드로 제공되는 서브쿼리 기능을 이용해, 모든 `destinations`와 각 목적지에 마지막으로 도착한 비행기의 이름을 한 번의 쿼리로 조회할 수 있습니다.

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
#### 서브쿼리 정렬(Subquery Ordering)

또한 쿼리 빌더의 `orderBy` 함수 역시 서브쿼리를 지원합니다. 위의 항공편 예시에서, 각 목적지에 마지막으로 도착한 비행기가 언제 도착했는지에 따라 목적지들을 정렬할 수 있습니다. 이 역시 하나의 데이터베이스 쿼리로 가능합니다.

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

주어진 쿼리 조건에 일치하는 모든 레코드를 조회하는 것뿐 아니라, `find`, `first`, `firstWhere` 메서드를 통해 단일 레코드를 조회할 수도 있습니다. 이들 메서드는 모델의 컬렉션이 아닌, 하나의 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본 키로 모델 조회
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// 조건에 맞는 첫 번째 모델을 조회하는 대체 방법
$flight = Flight::firstWhere('active', 1);
```

조회 결과가 없을 때 다른 작업을 수행하고 싶을 때는, `findOr` 및 `firstOr` 메서드를 사용하면 됩니다. 이 메서드들은 결과가 있으면 해당 모델 인스턴스를 반환하고, 없으면 전달된 클로저를 실행하여 반환된 값을 결과로 사용합니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 조회 실패 예외 처리

결과를 찾지 못했을 때 예외를 throw하고 싶을 때도 있습니다. 이는 라우트나 컨트롤러 등에서 유용합니다. `findOrFail` 및 `firstOrFail` 메서드는 쿼리 결과 중 첫 번째 레코드를 반환하지만, 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 잡히지 않으면, 라라벨은 자동으로 404 HTTP 응답을 클라이언트에 반환합니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성하기

`firstOrCreate` 메서드는 지정한 컬럼/값 쌍으로 데이터베이스 레코드를 찾으려고 시도합니다. 만약 데이터베이스에 해당 모델이 존재하지 않으면, 첫 번째 배열 인자와(선택적으로) 두 번째 배열 인자 값을 합친 속성값으로 레코드를 새로 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 비슷하게 주어진 속성에 맞는 레코드를 찾으려고 시도합니다. 하지만 조회 결과가 없으면 새 모델 인스턴스를 반환만 하고, 아직 데이터베이스에는 저장하지 않습니다. 따라서 `firstOrNew`로 반환받은 모델을 실제로 저장하려면 `save` 메서드를 직접 호출해야 합니다.

```php
use App\Models\Flight;

// 이름으로 flight 조회, 없으면 새로 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 flight 조회, 없으면 name, delayed, arrival_time까지 속성 포함해 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 flight 조회, 없으면 새 Flight 인스턴스 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 flight 조회, 없으면 name, delayed, arrival_time 속성 포함해 새 인스턴스 반환
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>

### 집계(Aggregate) 값 조회

Eloquent 모델을 다룰 때, 라라벨 [쿼리 빌더](/docs/12.x/queries)를 통해 제공되는 `count`, `sum`, `max`와 같은 [집계 메서드](/docs/12.x/queries#aggregates)도 사용할 수 있습니다. 이러한 메서드는 예상대로 Eloquent 모델 인스턴스가 아닌 단일(스칼라) 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

물론, Eloquent를 사용할 때 단순히 데이터베이스에서 모델을 조회하는 것뿐만 아니라 새 레코드를 삽입해야 할 때도 있습니다. Eloquent를 이용하면 이 작업도 매우 간단합니다. 데이터베이스에 새 레코드를 삽입하려면, 새로운 모델 인스턴스를 생성하고 필요한 속성(attribute)을 설정한 뒤, 해당 인스턴스에서 `save` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 데이터베이스에 새 항공편을 저장합니다.
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

이 예제에서는 들어온 HTTP 요청에서 `name` 필드를 가져와 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당하고 있습니다. 이후 `save` 메서드를 호출하면, 데이터베이스에 해당 레코드가 삽입됩니다. `save`가 호출될 때 모델의 `created_at`, `updated_at` 타임스탬프도 자동으로 설정되므로, 직접 값을 지정할 필요가 없습니다.

또한, `create` 메서드를 사용하면 한 줄의 PHP 코드로 새 모델을 "저장"할 수도 있습니다. `create` 메서드는 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하기 전에 모델 클래스에 `fillable` 또는 `guarded` 속성을 반드시 지정해야 합니다. 이것은 Eloquent 모델이 기본적으로 대량 할당 취약점(mass assignment vulnerability)으로부터 보호받기 때문입니다. 대량 할당에 대해 더 자세히 알고 싶다면 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

데이터베이스에 이미 존재하는 모델을 수정할 때도 `save` 메서드를 사용할 수 있습니다. 모델을 수정하려면, 먼저 해당 모델을 조회한 뒤 변경하려는 속성 값을 설정하고, `save` 메서드를 호출하면 됩니다. 이때도 `updated_at` 타임스탬프가 자동으로 갱신되므로 직접 지정할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

간혹, 이미 존재하는 모델을 수정하거나 일치하는 모델이 없다면 새로 생성해야 하는 상황이 있습니다. 이럴 때 `firstOrCreate`와 유사하게 동작하는 `updateOrCreate` 메서드를 사용할 수 있습니다. 이 메서드는 모델을 저장해주므로 별도의 `save` 호출이 필요 없습니다.

아래 예제에서, `departure`가 `Oakland`이고, `destination`이 `San Diego`인 항공편이 이미 존재한다면 해당 `price`와 `discounted` 컬럼이 수정됩니다. 만약 해당 조건의 항공편이 없다면, 두 인수의 배열이 합쳐져 새로운 항공편이 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

특정 조건에 맞는 여러 모델에 대해 대량으로 업데이트를 수행할 수도 있습니다. 아래 예제에서는 `active`가 1이고 `destination`이 `San Diego`인 모든 항공편이 지연(delayed) 처리됩니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼과 값의 쌍으로 이루어진 배열을 인수로 받으며, 영향을 받은 행(row)의 개수를 반환합니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트를 실행할 경우, 해당 모델에 대해 `saving`, `saved`, `updating`, `updated`와 같은 이벤트가 발생하지 않습니다. 이는 대량 업데이트 시 모델이 실제로 조회되지 않고 바로 쿼리가 실행되기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 내역 확인

Eloquent는 모델의 내부 상태를 확인하고, 속성(attribute)이 원래 조회되었을 때와 어떻게 달라졌는지 파악할 수 있도록 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

`isDirty` 메서드는 모델을 조회한 이후 속성값이 변경되었는지 확인합니다. 특정 속성명(문자열)이나 속성명 배열을 전달하여 해당 속성 중 하나라도 변경되었는지 확인할 수 있습니다. 반대로 `isClean` 메서드는 해당 속성이 조회 이후 변경되지 않았는지 판별합니다. 이 또한 속성명을 인수로 받을 수 있습니다.

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

`wasChanged` 메서드는 현재 요청 사이클 내에서 마지막으로 모델을 저장했을 때 속성값이 변경되었는지 확인합니다. 특정 속성명이 변경되었는지 확인하려면 인수로 속성명을 전달할 수 있습니다.

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

`getOriginal` 메서드는 모델이 조회된 이후 어떠한 변경이 있었든 상관없이, 모델의 원래 속성값이 담긴 배열을 반환합니다. 특정 속성의 원래 값을 얻고 싶으면 속성명을 인수로 전달합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열...
```

`getChanges` 메서드는 최근에 모델이 저장될 때 변경된 속성들을 배열로 반환합니다. 반면, `getPrevious` 메서드는 저장 직전의 속성값을 배열로 반환합니다.

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

단일 PHP 구문만으로 새로운 모델을 "저장"하려면 `create` 메서드를 사용할 수 있습니다. 이 메서드는 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드 사용 전에는 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이 속성들은 모든 Eloquent 모델이 기본적으로 대량 할당 취약점으로부터 보호받기 때문에 필수입니다.

대량 할당 취약점이란, 사용자가 예기치 않은 HTTP 요청 필드를 전달하고, 해당 필드가 예상하지 못했던 데이터베이스 컬럼까지 변경하는 상황을 의미합니다. 예를 들어, 악의적인 사용자가 HTTP 요청에 `is_admin` 파라미터를 추가하고, 이것이 모델의 `create` 메서드로 전달되어 자신에게 관리자 권한을 부여할 수도 있습니다.

따라서, 우선적으로 어떤 모델 속성을 대량 할당 가능하게 할지 `$fillable` 속성을 통해 명확히 지정해야 합니다. 예를 들어, `Flight` 모델의 `name`만 대량 할당을 허용하려면 다음과 같이 작성합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 가능한 속성 목록
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

대상 속성을 명시한 후에는, 이제 `create` 메서드를 통해 데이터베이스에 새 레코드를 삽입할 수 있습니다. `create`는 새로 만들어진 모델 인스턴스를 반환합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 생성된 모델 인스턴스가 있다면, `fill` 메서드를 사용해 여러 속성을 한 번에 할당할 수도 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼도 대량 할당 대상에 포함하려면, 해당 컬럼의 키를 `$fillable` 배열에 반드시 명시해야 합니다. 보안을 위해, `guarded` 속성을 사용할 경우 중첩 JSON 속성의 대량 업데이트는 지원되지 않습니다.

```php
/**
 * 대량 할당이 가능한 속성 목록
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 전체 대량 할당 허용

모든 속성을 대량 할당 가능하게 하려면, 모델의 `$guarded` 속성을 빈 배열로 지정하면 됩니다. 이렇게 모델을 “unguard” 했다면, Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열을 항상 직접 신경 써서 만들어야 합니다.

```php
/**
 * 대량 할당이 불가능한 속성 목록
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로, `$fillable`에 포함되지 않은 속성은 대량 할당 시 조용히 무시됩니다. 이는 운영 환경에서는 예상된 동작이지만, 로컬 개발 단계에서는 모델 변경이 잘 반영되지 않아 혼란을 겪을 수 있습니다.

만약, 대량 할당 시 할당 불가능한 속성이 있을 때 Laravel이 예외를 던지도록 하려면 `preventSilentlyDiscardingAttributes` 메서드를 호출하면 됩니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트(Upserts)

Eloquent의 `upsert` 메서드는 단일 원자적 연산으로 레코드를 "업데이트 또는 삽입"할 수 있습니다. 첫 번째 인자는 삽입 또는 업데이트할 값들의 배열이고, 두 번째 인자는 해당 테이블에서 레코드를 고유하게 식별할 컬럼(들)입니다. 마지막 세 번째 인자는 동일한 레코드가 있을 때 업데이트해야 할 컬럼들의 배열입니다. 모델에 타임스탬프가 활성화되어 있다면, `upsert`는 `created_at`, `updated_at` 도 자동으로 처리합니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert`의 두 번째 인자에 명시한 컬럼에 "primary" 또는 "unique" 인덱스가 존재해야 합니다. 또한, MariaDB와 MySQL 드라이버는 두 번째 인자를 무시하고 항상 테이블의 "primary" 및 "unique" 인덱스를 사용하여 기존 레코드 존재 여부를 판별합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 해당 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 예제에서는 먼저 모델을 조회한 뒤 `delete`를 호출합니다. 하지만 모델의 기본 키 값을 알고 있다면, 굳이 모델을 조회하지 않고도 `destroy` 메서드로 바로 삭제할 수 있습니다. 이 메서드는 하나의 기본 키뿐만 아니라 여러 개, 배열 혹은 [컬렉션](/docs/12.x/collections) 형태의 기본 키도 인수로 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제](#soft-deleting) 모델을 사용하는 경우, `forceDestroy` 메서드를 이용해 영구 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드하여 `delete` 메서드를 실행합니다. 이렇게 해야 각 모델에 대해 `deleting`, `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 모델 삭제

물론 쿼리를 직접 작성하여 조건에 맞는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래 예제에서는 `active`가 0으로 비활성화된 모든 항공편을 삭제합니다. 대량 업데이트처럼, 대량 삭제 시에도 삭제된 모델에 대해 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

모든 테이블의 모델을 삭제하려면, 조건 없이 쿼리를 실행하면 됩니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent를 통해 대량 삭제 쿼리를 실행할 경우, 삭제된 모델에 대해 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 이는 해당 모델이 실제로 조회되지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

실제로 데이터베이스에서 레코드를 완전 삭제하는 것뿐만 아니라, Eloquent는 "소프트 삭제"도 지원합니다. 소프트 삭제된 모델은 데이터베이스에서 완전히 삭제되지 않고, `deleted_at` 속성에 해당 모델이 "삭제"된 시점의 날짜와 시간이 저장됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트(trait)를 추가하면 됩니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` / `Carbon` 인스턴스로 변환해줍니다.

또한 데이터베이스 테이블에 `deleted_at` 컬럼을 추가해야 합니다. 라라벨 [스키마 빌더](/docs/12.x/migrations)를 이용해 이를 간단히 생성할 수 있습니다.

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

이제 모델에서 `delete` 메서드를 호출하면, 해당 레코드의 `deleted_at` 컬럼에 현재 일시가 기록되고, 데이터는 테이블에 남게 됩니다. 소프트 삭제가 활성화된 모델을 조회할 때, 소프트 삭제된 모델은 자동으로 모든 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 확인하려면, `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

때로는 소프트 삭제된 모델을 "복원"해야 할 때가 있습니다. 소프트 삭제된 모델 인스턴스에서는 `restore` 메서드를 호출하면, 해당 모델의 `deleted_at` 컬럼이 `null`로 설정되어 모델이 복원됩니다.

```php
$flight->restore();
```

여러 모델을 한 번에 복원할 수도 있습니다. 마찬가지로, 이러한 대량 작업 역시 복원된 모델에 대해 이벤트가 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

이 메서드는 [연관관계](/docs/12.x/eloquent-relationships) 쿼리에서도 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구적으로 모델 삭제

정말로 데이터베이스에서 모델을 완전히 삭제해야 하는 경우, `forceDelete` 메서드를 사용하면 소프트 삭제된 모델도 완전히 제거할 수 있습니다.

```php
$flight->forceDelete();
```

이 메서드는 Eloquent 연관관계 쿼리에도 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함해서 조회

앞서 언급했듯이, 소프트 삭제 모델은 기본적으로 쿼리 결과에서 제외됩니다. 하지만 쿼리 빌더에서 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델 포함 결과를 얻을 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed`는 [연관관계](/docs/12.x/eloquent-relationships) 쿼리에서도 사용할 수 있습니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회

`onlyTrashed` 메서드를 사용하면 오직 **소프트 삭제된 모델**만 조회할 수 있습니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

필요하지 않은 모델을 주기적으로 삭제하고 싶을 때가 있습니다. 이를 위해, 주기적으로 가지치기(prune)할 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하면 됩니다. 그 다음, 삭제 대상 모델을 반환하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현합니다.

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
     * 가지치기 대상 모델 쿼리를 반환합니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

모델에 `Prunable`을 사용할 때, 필요하다면 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 전에 호출되며, 모델에 연관된 파일이나 다른 리소스를 삭제하는 등 영구 삭제 직전에 필요한 작업을 수행할 때 유용합니다.

```php
/**
 * 가지치기를 위한 사전 작업을 수행합니다.
 */
protected function pruning(): void
{
    // ...
}
```

가지치기 대상 모델을 구성했으면, 애플리케이션의 `routes/console.php` 파일에 `model:prune` 아티즌 명령어를 예약해두어야 합니다. 해당 명령어를 실행할 간격은 자유롭게 선택할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

이 명령어는 자동으로 애플리케이션의 `app/Models` 디렉터리에 있는 "Prunable" 모델을 감지합니다. 모델이 다른 위치에 있다면, `--model` 옵션으로 모델 클래스명을 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

가지치기에서 제외할 모델을 지정하려면, `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 사용하여, 실제로 실행하지 않고 얼마나 많은 레코드가 삭제될지 테스트해볼 수 있습니다. 이 때, `model:prune` 명령어는 삭제될 레코드 수만을 출력합니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델이 가지치기 쿼리에 일치하면 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트가 적용된 모델은, 대량 삭제 쿼리를 사용하여 데이터베이스에서 삭제됩니다. 따라서 `pruning` 메서드나 `deleting`, `deleted` 모델 이벤트가 호출되지 않습니다. 모델을 실제로 조회하지 않고 바로 삭제하므로, 가지치기 처리가 훨씬 효율적입니다.

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
     * 가지치기 대상 모델 쿼리를 반환합니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제(Replicating Models)

이미 존재하는 모델 인스턴스의 미저장(unsaved) 복사본을 만드려면 `replicate` 메서드를 사용하세요. 같은 속성을 가진 모델이 여러 개 필요한 경우 특히 유용합니다.

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

복제할 때, 복제 대상에 포함되지 않게 하고 싶은 속성이 있다면 배열로 `replicate` 메서드에 전달할 수 있습니다.

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
### 전역 스코프(Global Scopes)

전역 스코프는 해당 모델에 대한 모든 쿼리에 특정 제약조건을 자동으로 추가할 수 있게 해줍니다. 라라벨의 [소프트 삭제](#soft-deleting) 기능 역시 전역 스코프를 활용하여 기본적으로 "삭제되지 않은" 모델만 조회되도록 처리합니다. 직접 전역 스코프를 작성하면, 특정 모델의 모든 쿼리에 공통 조건을 적용하기가 훨씬 간편해집니다.

<a name="generating-scopes"></a>
#### 스코프 생성

새로운 전역 스코프를 만들려면, `make:scope` 아티즌 명령어를 사용하세요. 생성된 클래스는 애플리케이션의 `app/Models/Scopes` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성

전역 스코프는 매우 간단하게 작성할 수 있습니다. 먼저, `make:scope` 명령어로 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현한 클래스를 생성합니다. 인터페이스에서는 오직 하나, `apply` 메서드만 필수로 구현해야 합니다. `apply` 메서드에서는 필요에 따라 쿼리에 `where` 조건이나 다양한 구절을 추가할 수 있습니다.

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
> 전역 스코프에서 쿼리의 select 절에 컬럼을 추가할 때는 반드시 `select` 대신 `addSelect` 메서드를 사용해야 합니다. 그렇지 않으면 기존 select 절이 의도치 않게 모두 대체될 수 있습니다.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용

전역 스코프를 모델에 적용하려면, 모델 클래스에 `ScopedBy` 속성을 부여하면 됩니다.

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

또는, 모델의 `booted` 메서드를 오버라이딩 한 뒤 `addGlobalScope` 메서드로 직접 전역 스코프 인스턴스를 등록할 수도 있습니다. 이 메서드는 스코프 인스턴스를 인자로 받습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예제처럼 `App\Models\User` 모델에 스코프를 적용하면, `User::all()`을 호출할 때 다음과 같은 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>

#### 익명 글로벌 스코프

Eloquent은 별도의 클래스를 만들 필요 없이 간단한 스코프를 정의할 때 특히 유용하게, 클로저(익명 함수)를 사용하여 글로벌 스코프를 정의할 수 있습니다. 클로저를 사용해 글로벌 스코프를 정의할 때는 `addGlobalScope` 메서드의 첫 번째 인자로 직접 지정한 스코프 이름을 전달해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
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
#### 글로벌 스코프 제거하기

특정 쿼리에서 글로벌 스코프를 제거하고 싶다면 `withoutGlobalScope` 메서드를 사용하면 됩니다. 이 메서드는 제거할 글로벌 스코프의 클래스명을 유일한 인자로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

또는, 클로저로 글로벌 스코프를 정의했다면, 스코프를 정의할 때 지정한 문자열 이름을 인자로 넘기면 됩니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 글로벌 스코프를 제거하거나, 쿼리의 모든 글로벌 스코프를 제거하고 싶다면 `withoutGlobalScopes` 메서드를 사용하세요.

```php
// 모든 글로벌 스코프를 제거합니다...
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거합니다...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 애플리케이션 전체에서 쉽게 재사용할 수 있는 쿼리 제약 조건의 묶음을 정의할 수 있도록 해줍니다. 예를 들어, "인기 많은" 사용자 목록을 자주 조회해야 한다고 가정해봅시다. 스코프를 정의하려면 Eloquent 메서드에 `Scope` 속성을 추가하면 됩니다.

스코프는 항상 동일한 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 쿼리를 "인기 많은 사용자"로만 제한하는 스코프입니다.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 쿼리를 "활성 사용자"로만 제한하는 스코프입니다.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용하기

스코프를 정의한 후에는 모델을 조회할 때 해당 스코프 메서드를 바로 호출할 수 있습니다. 다양한 스코프를 체이닝해서 사용할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 Eloquent 모델 스코프를 `or` 쿼리 연산자로 결합하려면, 올바른 [논리 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만, 이런 방식이 번거로울 수 있기 때문에 Laravel에서는 클로저를 사용하지 않고도 스코프를 간단하게 연결할 수 있는 "고차원(higher order)" `orWhere` 메서드를 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 다이나믹 스코프

가끔은 인자를 받는 스코프가 필요할 경우가 있습니다. 이를 위해, 스코프 메서드 시그니처에 원하는 추가 인자를 `$query` 파라미터 다음에 정의하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입의 사용자로만 쿼리를 제한하는 스코프입니다.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

이제 스코프 메서드 시그니처에 원하는 인자를 추가했으므로, 스코프를 사용할 때 해당 인자를 넘기면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending Attributes

스코프를 사용해 쿼리를 구성할 때, 쿼리 조건에 사용된 것과 동일한 속성(attribute)을 가진 모델을 생성하고 싶다면, 쿼리 빌드 과정에서 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 쿼리를 임시글만 조회하도록 제한하는 스코프입니다.
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

`withAttributes` 메서드는 지정한 속성을 조건으로 `where` 절을 쿼리에 추가할 뿐만 아니라, 해당 스코프를 이용해 생성된 모델 인스턴스에도 같은 속성을 추가합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않도록 하려면, `asConditions` 인자를 `false`로 지정하면 됩니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

가끔 두 모델이 "같은" 모델인지 판별해야 할 때가 있습니다. `is`와 `isNot` 메서드를 사용하면 두 모델의 기본키, 테이블, 데이터베이스 연결이 동일한지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`와 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/12.x/eloquent-relationships)에서도 사용할 수 있습니다. 이 메서드는 관련 모델을 조회하기 위한 쿼리를 실행하지 않고도 비교할 수 있어서 특히 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 사이드 애플리케이션으로 바로 브로드캐스팅하고 싶으신가요? 라라벨의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 기능을 확인해보세요.

Eloquent 모델은 여러 이벤트를 발생시키며, 이를 통해 모델의 라이프사이클 내에서 다음과 같은 시점에 후킹(hook)할 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

`retrieved` 이벤트는 데이터베이스에서 기존 모델을 조회했을 때 발생합니다. 새 모델을 처음 저장할 때는 `creating`과 `created` 이벤트가 발생합니다. 기존 모델을 수정해 `save` 메서드를 호출할 경우에는 `updating` / `updated` 이벤트가 발생합니다. `saving` / `saved` 이벤트는 모델을 생성하거나 업데이트할 때, 심지어 속성이 변경되지 않았더라도 발생합니다. 이벤트 이름이 `-ing`로 끝나는 경우에는 모델의 변화가 실제로 저장되기 전에 실행되며, `-ed`로 끝나는 이벤트는 변화가 저장된 후에 실행됩니다.

모델 이벤트를 수신하려면, Eloquent 모델에 `$dispatchesEvents` 프로퍼티를 정의해야 합니다. 이 프로퍼티는 Eloquent 모델 라이프사이클의 지점을 여러분이 직접 정의한 [이벤트 클래스](/docs/12.x/events)와 매핑합니다. 각 모델 이벤트 클래스는 생성자를 통해 영향을 받은 모델 인스턴스를 받게 됩니다.

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
     * 모델의 이벤트 맵입니다.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의하고 매핑한 후에는 [이벤트 리스너](/docs/12.x/events#defining-listeners)를 통해 해당 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 통해 일괄 업데이트(mass update)나 일괄 삭제(mass delete) 쿼리를 실행하는 경우, 해당 모델들에는 `saved`, `updated`, `deleting`, `deleted` 모델 이벤트가 발생하지 않습니다. 이는 모델 인스턴스가 실제로 조회되지 않고 쿼리가 실행되기 때문입니다.

<a name="events-using-closures"></a>
### 클로저로 이벤트 등록하기

커스텀 이벤트 클래스를 사용하는 대신, 모델 이벤트 발생 시 실행할 클로저 함수를 등록할 수도 있습니다. 일반적으로 이런 클로저는 모델의 `booted` 메서드에서 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 이벤트 등록 시 [큐 처리되는 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 사용할 수도 있습니다. 이를 사용하면 애플리케이션의 [큐](/docs/12.x/queues)를 통해 이벤트 리스너가 백그라운드에서 실행되도록 할 수 있습니다.

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의하기

한 모델에서 여러 이벤트를 감지해야 한다면, 옵저버를 사용해서 모든 리스너를 하나의 클래스로 그룹화할 수 있습니다. 옵저버 클래스의 메서드 이름은 리스닝할 Eloquent 이벤트 이름을 반영합니다. 이 각 메서드는 영향을 받은 모델 인스턴스를 유일한 인자로 받습니다. 새로운 옵저버 클래스를 만들려면 Artisan의 `make:observer` 명령어를 사용하는 것이 가장 쉽습니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어를 실행하면 새로운 옵저버가 `app/Observers` 디렉터리에 생성됩니다. 디렉터리가 존재하지 않으면 Artisan이 자동으로 생성해줍니다. 생성된 옵저버는 아래와 같이 보일 것입니다.

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트를 처리합니다.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트를 처리합니다.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트를 처리합니다.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트를 처리합니다.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트를 처리합니다.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면 해당 모델에 `ObservedBy` 속성을 선언하면 됩니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, 수동으로 옵저버를 등록하고 싶다면, 관찰하고자 하는 모델에서 `observe` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에 등록하는 것이 일반적입니다.

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션의 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 감지할 수 있는 이벤트는 `saving`, `retrieved` 등 추가적으로 더 있습니다. 이러한 이벤트는 [이벤트](#events) 문서에서 더 자세히 다룹니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 데이터베이스 트랜잭션 내부에서 생성되는 경우, 옵저버의 이벤트 핸들러가 트랜잭션 커밋 이후에만 실행되도록 지정하고 싶을 수 있습니다. 이를 위해 옵저버에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 만약 데이터베이스 트랜잭션이 진행 중이 아니라면, 이벤트 핸들러는 즉시 실행됩니다.

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트를 처리합니다.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 비활성화(뮤트)하기

가끔은 모델에서 발생하는 모든 이벤트를 잠시 "비활성화(mute)"해야 할 때가 있습니다. 이럴 때는 `withoutEvents` 메서드를 사용하면 됩니다. `withoutEvents` 메서드는 클로저를 유일한 인자로 받으며, 클로저 내부에서 실행되는 모든 코드는 이벤트를 발생시키지 않습니다. 그리고 클로저가 반환하는 값이 그대로 `withoutEvents`의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 저장 시 이벤트 비활성화하기

특정 모델을 저장할 때만 이벤트를 발생시키지 않으려면 `saveQuietly` 메서드를 사용하세요.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

또한, "update", "delete", "soft delete", "restore", "replicate" 같은 작업도 이벤트 없이 조용히 실행할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```