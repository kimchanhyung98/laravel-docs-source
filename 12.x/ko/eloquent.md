# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 컨벤션](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성(stricness) 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청킹(Chunking)](#chunking-results)
    - [Lazy 컬렉션을 이용한 청킹](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [일괄 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [예정된 속성(Pending Attributes)](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 활용](#events-using-closures)
    - [옵서버(Observer)](#observers)
    - [이벤트 음소거(Muting Events)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 Eloquent라는 객체-관계 매퍼(ORM)를 포함하고 있어 데이터베이스와 쉽고 즐겁게 상호작용할 수 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블은 해당 테이블과 상호작용하는 "모델(Model)"에 매핑됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐 아니라 레코드를 삽입, 수정, 삭제하는 것도 가능합니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 설정해야 합니다. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저 Eloquent 모델을 생성해봅니다. 모델은 일반적으로 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성할 때는 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 만들고 싶다면, `--migration` 또는 `-m` 옵션을 사용하면 됩니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책(Policy), 컨트롤러, 폼 요청 등 다양한 타입의 클래스를 동시에 생성할 수 있으며, 여러 옵션을 조합하여 여러 클래스를 한 번에 만들 수도 있습니다:

```shell
# 모델 및 FlightFactory 클래스 생성...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델 및 FlightSeeder 클래스 생성...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델 및 FlightController 클래스 생성...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델 및 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 동시 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 한번에 생성...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 관계 확인

간혹 모델의 모든 속성(attribute)과 연관관계(relationship)를 코드만으로 파악하기 어려울 수 있습니다. 이럴 때는 `model:show` Artisan 명령어를 사용하여 모델의 속성과 관계를 한눈에 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 컨벤션

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치하게 됩니다. 아래의 기본 모델 클래스를 예시로, Eloquent의 주요 컨벤션(관례)에 대해 살펴보겠습니다.

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
### 테이블명

위의 예시를 보면, `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 명시하지 않은 것을 볼 수 있습니다. Eloquent는 기본적으로 클래스명을 "스네이크 케이스(snake case)"로 변환한 복수형을 테이블명으로 사용합니다. 따라서 `Flight` 모델은 `flights` 테이블에, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 매핑됩니다.

만약 모델이 매핑되는 데이터베이스 테이블명이 이 관례와 다르다면, 모델의 `table` 속성을 직접 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델과 연결된 테이블명
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델이 매핑된 테이블의 기본 키 컬럼명이 `id`라고 가정합니다. 필요하다면, 모델의 protected `$primaryKey` 속성에 다른 컬럼명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블의 기본 키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

Eloquent는 기본 키가 오토 인크리먼트(자동 증가) 되는 정수(integer)라고 가정하고, 기본 키 값을 자동으로 정수로 변환(cast)합니다. 만약 자동 증가가 아니거나, 숫자가 아닌 기본 키 값을 쓰고 싶다면, 모델 내에 public `$incrementing` 속성을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동 증가하는지 여부
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아니라면, 모델에 protected `$keyType` 속성을 정의하고 값을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본 키 ID의 데이터 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent 모델은 최소 하나 이상의 고유한 "ID"를 필요로 하며, 복합(여러 컬럼을 조합한) 기본 키는 지원하지 않습니다. 하지만, 테이블의 고유(primary) 기본 키 외에 다중 컬럼(unique index) 인덱스는 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

기본적으로 Eloquent 모델의 기본 키로 오토 인크리먼트되는 정수를 사용하지만, 대신 UUID(범용 고유 식별자)를 사용할 수도 있습니다. UUID는 36자의 영문-숫자 조합 고유 식별자입니다.

모델에서 오토 인크리먼트 정수 대신 UUID 키를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트(trait)를 모델에 적용합니다. 물론 [UUID 형태의 기본 키 컬럼](/docs/12.x/migrations#column-method-uuid)이 테이블에 존재해야 합니다.

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

기본적으로 `HasUuids` 트레이트는 ["ordered" UUID](/docs/12.x/strings#method-str-ordered-uuid)를 생성하며, 인덱스된 데이터베이스에 저장할 때 더 효율적입니다(사전순 정렬 가능).

모델의 UUID 생성 방식을 오버라이드하려면 모델에 `newUniqueId` 메서드를 정의할 수 있습니다. 뿐만 아니라 `uniqueIds` 메서드를 정의하여 어떤 컬럼이 UUID를 받아야 하는지 지정할 수도 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델을 위한 새 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID를 받아야 할 컬럼 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 26자의 ULID(고유 식별자, Universally Unique Lexicographically Sortable Identifier)를 사용할 수도 있습니다. ULID 역시 사전순 정렬이 가능해서 인덱싱이 효율적입니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 적용하고, [ULID 형태의 기본 키 컬럼](/docs/12.x/migrations#column-method-ulid)이 있어야 합니다.

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

Eloquent는 기본적으로 모델과 매핑된 테이블에 `created_at`, `updated_at` 컬럼이 있다고 가정합니다. 모델이 생성되거나 수정될 때, Eloquent가 이 컬럼의 값을 자동으로 관리해줍니다. Eloquent가 자동으로 이 컬럼을 관리하지 않기를 원한다면, 모델에 `$timestamps` 속성을 `false`로 설정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 타임스탬프 자동 관리 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델 타임스탬프의 저장(포맷) 형태를 커스터마이징하려면, `$dateFormat` 속성을 설정하면 됩니다. 이 속성은 DB 저장/직렬화 시 포맷을 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 컬럼의 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 변경하려면, `CREATED_AT`, `UPDATED_AT` 상수를 모델에 정의하세요.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프가 변경되지 않게 하면서 작업하려면, `withoutTimestamps` 메서드에 클로저를 전달하여 해당 클로저 내부에서 작업을 수행합니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션의 기본(default) 데이터베이스 연결을 사용합니다. 특정 모델이 다른 데이터베이스 연결을 사용하게 하려면, 모델에 `$connection` 속성을 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 사용할 데이터베이스 연결
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

기본적으로 새로 인스턴스화된 모델에는 어떠한 속성 값도 들어 있지 않습니다. 모델의 일부 속성에 기본값을 정의하려면 `$attributes` 속성에 배열 형태로 지정하세요. `$attributes`에 들어가는 값들은 DB에서 읽은 원본 raw 형태여야 합니다.

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
### Eloquent 엄격성(stricness) 설정

Laravel에서는 Eloquent의 동작 방식, 특히 "엄격성(strictness)" 관련하여 여러 설정 메서드를 제공합니다.

우선, `preventLazyLoading` 메서드는 lazy loading(지연 로딩)을 방지할지 여부를 boolean 변수로 지정합니다. 예를 들어, 프로덕션 환경에서는 지연 로딩을 허용하고, 개발/테스트 환경에서는 방지하게 할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 사용합니다.

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

또한, `preventSilentlyDiscardingAttributes` 메서드를 사용하면 fillable이 아닌 속성에 값을 할당하려고 할 때 예외를 발생시킬 수 있습니다. 이는 `fillable`에 지정되지 않은 속성을 할당하려 할 때, 로컬 개발 환경에서 원인을 빠르게 파악할 수 있게 도와줍니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)까지 준비가 되었다면, 이제 데이터베이스에서 데이터를 조회할 수 있습니다. 각 Eloquent 모델은 관련 데이터베이스 테이블을 대상으로하는 강력한 [쿼리 빌더](/docs/12.x/queries)라고 볼 수 있습니다. 모델의 `all` 메서드는 모델이 연결된 데이터베이스 테이블에서 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성

Eloquent의 `all` 메서드는 테이블의 모든 레코드를 반환합니다. 하지만, Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries)이기도 하므로 다양한 쿼리 조건을 추가하고, `get` 메서드로 결과를 조회할 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더로 동작하므로, Laravel의 [쿼리 빌더](/docs/12.x/queries)에서 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리 작성 시 이 메서드들도 참고하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

데이터베이스에서 조회한 Eloquent 모델 인스턴스가 이미 있다면, `fresh`와 `refresh` 메서드로 모델을 새로고침할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회하여 새로 반환하지만, 기존 인스턴스는 변경되지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 데이터로 재하이드레이트(rehydrate)합니다. 또한 이미 로드된 연관관계도 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

Eloquent의 `all`이나 `get` 같은 메서드는 여러 레코드를 조회하며, 이 때 단순한 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장한 것으로, [데이터 컬렉션을 조작하는 데 유용한 다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 사용해 클로저 조건에 따라 컬렉션에서 모델을 제외할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel의 기본 컬렉션 클래스에서 제공하는 메서드뿐만 아니라, Eloquent 컬렉션 클래스는 [Eloquent 모델 컬렉션 전용의 메서드](/docs/12.x/eloquent-collections#available-methods)도 추가로 제공합니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로, 배열처럼 반복문으로 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청킹(Chunking)

`all`이나 `get` 메서드로 수만 개의 Eloquent 레코드를 한 번에 로드하면 애플리케이션이 메모리 부족에 빠질 수 있습니다. 이럴 때는 `chunk` 메서드를 이용해 대량의 모델을 메모리 효율적으로 처리하세요.

`chunk` 메서드는 일부 레코드만 조회하여 클로저로 전달합니다. 이 방법은 한 번에 전체를 불러오는 대신 각 chunk마다 따로 쿼리를 실행함으로써 메모리 사용량을 크게 줄일 수 있습니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk`의 첫 번째 인자는 한 번에 가져올 레코드 수, 두 번째 인자는 각 chunk에 대해 실행할 클로저입니다. 데이터베이스 쿼리는 각 chunk를 가져올 때마다 한 번씩 실행됩니다.

청킹 중에 참조하는 컬럼 값을 업데이트 하면서 결과를 필터링해야 한다면, `chunk` 대신 `chunkById` 메서드를 사용해야 합니다. 그렇지 않으면 예기치 않은 동작이 발생할 수 있습니다. `chunkById`는 내부적으로 이전 chunk의 마지막 모델보다 `id`가 큰 모델만 계속해서 읽어옵니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 자체적으로 추가적인 "where" 조건을 쿼리에 붙이므로, 여러 직접 작성한 조건들은 클로저 내부에서 [논리적 그룹화](/docs/12.x/queries#logical-grouping)하는 것이 좋습니다:

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
### Lazy 컬렉션을 이용한 청킹

`lazy` 메서드는 내부적으로 [chunk 메서드](#chunking-results)처럼 쿼리를 청크 단위로 실행하지만, 각 chunk를 콜백으로 전달하는 대신, 단일 플랫 형태의 [LazyCollection](/docs/12.x/collections#lazy-collections)으로 반환합니다. 이를 통해 큰 결과 집합을 하나의 스트림처럼 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 메서드 사용 시, 순회하면서 업데이트하는 컬럼 값을 기준으로 필터링할 필요가 있다면, `lazyById`를 사용하세요. 이는 내부적으로 이전 chunk의 마지막 모델보다 `id`가 큰 모델만 읽어옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id`의 내림차순으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy`와 유사하게, `cursor` 메서드 역시 수만 개의 Eloquent 레코드를 반복 순회할 때 메모리 사용량을 대폭 줄여줍니다.

`cursor` 메서드는 생성된 단일 쿼리로 결과를 가져오지만, 실제로 모델을 순회(traverse)할 때까지 Eloquent 모델 인스턴스를 메모리에 적재하지 않습니다. 따라서 반복 중 한 번에 하나의 모델만 메모리상에 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 항상 한 번에 하나의 Eloquent 모델만 메모리에 유지하므로, 연관관계 eager loading은 지원하지 않습니다. 만약 eager loading이 필요하다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

내부적으로 `cursor`는 PHP의 [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)을 통해 한 번에 한 모델만 메모리에 유지하면서도 컬렉션 메서드를 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, PDO 드라이버가 모든 원시 쿼리 결과를 내부적으로 버퍼링하기 때문에 결국엔 메모리가 한계에 다다릅니다. 만약 정말 많은 레코드를 다뤄야 한다면, [lazy 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리 지원을 제공하며, 이를 통해 한 번의 쿼리로 여러 테이블에서 정보를 가져올 수 있습니다. 예를 들어, `destinations`(목적지) 테이블과 각 목적지로 가는 `flights`(비행편) 테이블이 있다고 가정해보겠습니다. `flights` 테이블엔 도착 시간(`arrived_at`)이 기록되어 있습니다.

쿼리 빌더의 `select`와 `addSelect` 메서드로 서브쿼리를 추가하여 목적지와 각 목적지에 최근에 도착한 비행편명을 한 번의 쿼리로 조회할 수 있습니다:

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

또한 쿼리 빌더의 `orderBy` 기능도 서브쿼리를 지원합니다. 위 예시를 이어, 가장 최근에 비행편이 도착한 목적지 기준으로 정렬까지 한 번의 쿼리로 할 수 있습니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 조회

쿼리 조건에 일치하는 모든 레코드를 조회하는 것뿐만 아니라, `find`, `first`, `firstWhere` 메서드를 사용해 단일 레코드를 조회할 수도 있습니다. 이 메서드들은 컬렉션이 아닌 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 특정 모델 조회...
$flight = Flight::find(1);

// 쿼리 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 위의 대체 방법...
$flight = Flight::firstWhere('active', 1);
```

때때로 조회 결과가 없을 때 다른 동작을 하고 싶을 수 있습니다. `findOr`, `firstOr` 메서드는 모델 인스턴스를 반환하거나, 결과가 없으면 주어진 클로저를 실행합니다. 클로저가 반환하는 값이 메서드의 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 조회 실패 예외

특정 모델을 찾지 못했을 때 예외를 발생시키고 싶을 때도 있습니다(특히 라우트나 컨트롤러에서). `findOrFail`, `firstOrFail` 메서드는 쿼리에서 첫 번째 결과를 반환하거나, 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 잡히지 않을 경우, Laravel은 자동으로 404 HTTP 응답을 클라이언트에 반환합니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍으로 레코드를 탐색합니다. 만약 데이터베이스에 해당 레코드가 없다면, 첫 번째 배열 인수와 (선택적으로) 두 번째 배열 인수를 병합한 값으로 새로운 레코드를 생성(삽입)합니다.

`firstOrNew` 메서드도 유사합니다. 그러나, 모델이 없을 때 새 모델 인스턴스만 반환하고, 실제 DB 삽입은 하지 않습니다. 이럴 땐 직접 `save` 메서드로 저장해야 합니다:

```php
use App\Models\Flight;

// 이름으로 조회, 없으면 새로 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성까지 포함해 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 인스턴스 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성 포함해 새 인스턴스 반환
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델로 작업할 때, Laravel [쿼리 빌더](/docs/12.x/queries)에서 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/12.x/queries#aggregates)도 사용할 수 있습니다. 이 메서드들은 Eloquent 모델 인스턴스가 아니라 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때, 모델 조회뿐 아니라 새 레코드도 삽입할 수 있습니다. 새로운 레코드를 삽입하려면, 모델 인스턴스를 생성하고 각 속성을 할당한 뒤, `save` 메서드를 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 비행편을 데이터베이스에 저장
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

이 예제에서는 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당하고, `save` 메서드 호출 시 DB에 레코드가 삽입됩니다. 이때 `created_at`, `updated_at` 타임스탬프는 자동으로 설정되므로 직접 넣을 필요가 없습니다.

또는, 한 번에 새로운 모델을 저장하려면 `create` 메서드를 사용할 수도 있습니다. `create` 메서드는 생성된(삽입된) 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하기 전에 모델 클래스에서 `fillable` 또는 `guarded` 속성을 반드시 지정해야 합니다. 모든 Eloquent 모델은 대량 할당 취약점(Mass Assignment Vulnerability)으로부터 보호되기 때문입니다. 자세한 내용은 [일괄 할당(Mass Assignment)](#mass-assignment) 문서를 참고하세요.

<a name="updates"></a>
### 수정

`save` 메서드는 이미 DB에 존재하는 모델을 수정할 때도 사용됩니다. 모델을 먼저 불러온 다음, 수정할 속성을 할당하고, `save`를 호출하면 됩니다. 이때 `updated_at` 타임스탬프도 자동으로 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

기존 모델이 있으면 수정, 없으면 새로 생성해야 하는 경우에는 `updateOrCreate` 메서드를 활용할 수 있습니다. 이 메서드는 `firstOrCreate`와 비슷하게 동작하며, 결과 모델은 항상 저장(persisted)됩니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

`firstOrCreate` 또는 `updateOrCreate`를 사용할 때 새 모델이 생성된 것인지 기존이 수정된 것인지 모를 경우, `wasRecentlyCreated` 속성을 참고하세요:

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // 새 기록이 삽입됨
}
```

<a name="mass-updates"></a>
#### 대량 업데이트

특정 조건에 일치하는 다수의 모델을 한 번에 업데이트할 수도 있습니다. 예를 들어, `active`이고 `destination`이 `San Diego`인 모든 비행편을 지연(delay) 처리하려면 다음처럼 합니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드의 인수는 업데이트할 컬럼/값(key/value)들의 배열이며, 결과는 영향을 받은 행(row)의 개수입니다.

> [!WARNING]
> Eloquent로 대량 업데이트를 실행할 때는 해당 모델 객체가 실제로 조회되거나 인스턴스화되지 않기 때문에 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경점 검사

Eloquent는 모델의 내부 상태 및 DB 조회 시점과 비교해 속성이 어떻게 달라졌는지 알려주는 `isDirty`, `isClean`, `wasChanged` 등의 메서드를 제공합니다.

`isDirty`는 모델이 조회된 이후 어떤 속성이 수정되었는지 확인합니다. 특정 속성명이나 배열을 전달해 부분 검사도 할 수 있습니다. 반대로 `isClean`은 속성이 변경되지 않았는지 검증합니다:

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

`wasChanged`는 모델이 마지막으로 저장된 시점에 어떤 속성이 실제로 변경되어 DB에 반영됐는지 확인합니다. 특정 속성명이나 배열로 부분 체크도 가능합니다:

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

`getOriginal` 메서드는 모델이 최초로 조회된 시점의 속성값(변경 유무와 상관없이)을 배열로 반환합니다. 인수로 속성명을 전달하면 특정 속성의 원래 값을 가져올 수 있습니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열 반환
```

`getChanges`는 모델이 마지막으로 저장될 때 실제로 변경된 속성만 배열로 반환하고, `getPrevious`는 저장 전 원래의 속성값을 배열로 반환합니다:

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

`create` 메서드는 한 줄의 PHP 문장으로 새 모델을 저장할 수 있게 해줍니다. 이때 메서드의 반환값은 생성된 모델 인스턴스입니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하기 전에는 반드시 모델 클래스에 `fillable`이나 `guarded` 속성 중 하나를 지정해야 합니다. 모든 Eloquent 모델은 일괄 할당 취약점으로부터 보호됩니다.

일괄 할당 취약점(Mass Assignment Vulnerability)이란, 사용자가 예상치 못한 HTTP 요청 필드명을 전달하여 의도치 않은 데이터베이스 컬럼이 변경될 때 발생합니다. 예를 들어, 악의적인 사용자가 `is_admin`이라는 필드를 요청에 포함시켜 관리자 권한을 획득할 수도 있습니다.

따라서, 모델에서 일괄 할당을 허용할 속성을 `$fillable` 속성에 명시합니다. 아래는 `Flight` 모델에서 `name`만 일괄 할당 가능하도록 지정한 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 일괄 할당 가능한 속성
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

이제 `create` 메서드로 해당 속성에 값을 할당해 DB에 레코드를 삽입할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드를 사용해 배열로 값을 할당할 수도 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 일괄 할당과 JSON 컬럼

JSON 컬럼에 값을 할당할 때, 각 JSON 컬럼의 키도 모델의 `$fillable` 배열에 포함해야 합니다. 보안상, Laravel은 `guarded` 속성 사용 시 중첩된 JSON 속성 업데이트를 지원하지 않습니다:

```php
/**
 * 일괄 할당 가능한 속성
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 일괄 할당 허용

모델의 모든 속성을 일괄 할당(mass assignable) 가능하게 하려면 `$guarded` 속성을 빈 배열로 설정합니다. 단, 이 경우 `fill`, `create`, `update` 등에 넘기는 배열을 손수 검증해야 하니 각별히 주의해야 합니다:

```php
/**
 * 일괄 할당 금지 속성(없음)
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 일괄 할당 예외

기본적으로 `$fillable`에 없는 속성은 일괄 할당 시 조용히 무시됩니다. 프로덕션 환경에선 의도된 동작이지만, 개발 환경에서 모델 변경 사항이 반영되지 않아 헷갈릴 수 있습니다.

이때 Laravel에 "fillable에 없는 속성을 일괄 할당 시 예외를 던지라"고 지시할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 다음처럼 호출합니다:

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
### 업서트(Upserts)

Eloquent의 `upsert` 메서드는 한 번의 원자적(atomic) 연산으로 레코드를 업데이트하거나 삽입(생성)할 수 있게 해줍니다. 첫 번째 인자는 삽입/업데이트할 값들의 배열, 두 번째는 레코드를 고유하게 식별할 컬럼, 세 번째는 이미 레코드가 있을 때 업데이트할 컬럼을 지정합니다. `upsert`는 타임스탬프가 켜진 모델에 대해 자동으로 `created_at`, `updated_at`을 설정합니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert`의 두 번째 인자인 컬럼에 "primary" 또는 "unique" 인덱스가 설정되어 있어야 합니다. MariaDB, MySQL 드라이버는 두 번째 인수를 무시하고 항상 테이블의 "primary" 및 "unique" 인덱스만 사용해 충돌을 감지합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델 인스턴스의 `delete` 메서드를 호출해 모델을 삭제할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 예제에서는 모델을 먼저 조회한 후 `delete`를 호출하지만, 기본 키 값을 안다면 모델을 직접 조회하지 않고도 `destroy` 메서드로 삭제할 수 있습니다. 이 메서드는 단일, 복수, 배열, [컬렉션](/docs/12.x/collections) 형태의 기본 키를 모두 지원합니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 쓸 경우, `forceDestroy` 메서드로 영구 삭제도 가능합니다:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 불러와 `delete`를 호출하므로, 삭제 이벤트(`deleting`, `deleted`)가 올바르게 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

Eloquent 쿼리로 조건에 맞는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래는 활성 상태가 아닌(비활성) 비행기들을 모두 삭제하는 예시입니다. 대량 삭제 시에는 개별 모델 이벤트가 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

조건 없이 실행하면 테이블의 모든 레코드를 삭제할 수도 있습니다:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent로 대량 삭제할 때는, 삭제 이벤트(`deleting`, `deleted`)가 발생하지 않습니다. 이는 삭제되는 모델을 실제로 불러오지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

DB에서 레코드를 실제로 삭제하는 것 외에도, Eloquent는 모델을 "소프트 삭제(Soft Delete)"할 수도 있습니다. 소프트 삭제는 DB에서 데이터를 실제로 지우지 않고, `deleted_at` 컬럼에 삭제 일시를 기록하는 방식입니다. 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하면 소프트 삭제가 활성화됩니다:

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 캐스팅해줍니다.

데이터베이스 테이블에도 `deleted_at` 컬럼을 추가해야 하며, Laravel [스키마 빌더](/docs/12.x/migrations)에서 이를 쉽게 추가/삭제하는 헬퍼 메서드를 제공합니다:

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

이제 모델의 `delete` 메서드를 호출하면 DB의 `deleted_at` 컬럼에는 현재 시간으로 값이 기록되지만, 데이터는 실제로 삭제되지 않습니다. 그리고 소프트 삭제 모델을 조회할 때는 해당 모델이 자동으로 결과에서 제외됩니다.

모델이 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

소프트 삭제된 모델을 "복구"하려면, 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. 이 메서드는 `deleted_at` 컬럼을 `null`로 만듭니다:

```php
$flight->restore();
```

여러 모델을 한 번에 복구하려면 쿼리에서 `restore`를 사용하세요. 역시 대량 작업이므로 개별 모델 이벤트는 발생하지 않습니다:

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
#### 모델 완전 삭제

DB에서 모델을 완전 삭제해야 할 경우, 소프트 삭제된 모델 인스턴스에서 `forceDelete` 메서드를 사용하면 해당 레코드를 영구 삭제합니다:

```php
$flight->forceDelete();
```

연관관계 쿼리에서도 `forceDelete`를 사용할 수 있습니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함해서 조회

앞서 언급했듯, 소프트 삭제된 모델은 기본적으로 자동으로 쿼리 결과에서 제외됩니다. 그러나 `withTrashed` 메서드를 쿼리에 붙이면 결과에 소프트 삭제 모델도 포함됩니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed`는 [연관관계](/docs/12.x/eloquent-relationships) 쿼리에서도 사용할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed` 메서드는 소프트 삭제된 모델만 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

주기적으로 불필요한 모델을 삭제해야 할 때가 있습니다. 이를 위해 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 모델에 추가할 수 있습니다. 트레이트를 추가한 뒤 `prunable` 메서드를 구현해, 더 이상 필요 없는 모델을 반환하는 Eloquent 쿼리 빌더를 작성합니다:

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
     * 가지치기(query)할 모델 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

`Prunable`로 지정한 모델은, 필요할 경우 `pruning` 메서드를 추가할 수도 있습니다. 이 메서드는 해당 모델이 삭제되기 전에 호출됩니다. 모델에 연관된 추가 자원(예: 파일 등)을 영구 삭제 전에 정리하는 데 사용할 수 있습니다:

```php
/**
 * 모델 가지치기 준비
 */
protected function pruning(): void
{
    // ...
}
```

가지치기 작업을 설정한 후에는, `model:prune` Artisan 명령어를 애플리케이션의 `routes/console.php`에 스케줄링하세요. 실행 주기는 상황에 맞게 결정하면 됩니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령어는 자동으로 `app/Models` 디렉토리의 "Prunable" 모델을 감지합니다. 모델이 다른 경로에 있다면, `--model` 옵션으로 모델 클래스명을 직접 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 가지치기에서 제외하고 싶다면, `--except` 옵션을 사용합니다:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`prunable` 쿼리를 테스트해보고 싶다면, `--pretend` 옵션으로 `model:prune` 명령어를 실행하세요. 이때 실제 삭제 없이, 삭제 대상 레코드 개수만 출력합니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델이라도, prunable 쿼리에 해당되면 `forceDelete`로 영구 삭제됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트가 적용된 모델은 SQL 대량 삭제 쿼리를 사용해 삭제됩니다. 따라서 `pruning` 메서드는 호출되지 않으며, `deleting`, `deleted` 이벤트도 발생하지 않습니다. 모델을 개별적으로 불러오지 않으므로 가지치기 과정이 더욱 효율적입니다:

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
     * 가지치기(query)할 모델 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 사용해 저장되지 않은(unsaved) 복사본을 만들고 싶을 때는 `replicate` 메서드를 사용할 수 있습니다. 속성이 대부분 동일한 여러 인스턴스를 만들어야 할 때 효과적입니다.

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

복제 시 특정 속성은 빼고 싶다면, 그 속성명의 배열을 `replicate`에 전달하면 됩니다:

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

글로벌 스코프를 사용하면 특정 모델의 모든 쿼리에 제약조건을 자동으로 추가할 수 있습니다. Laravel의 [소프트 삭제](#soft-deleting) 기능은 바로 이 글로벌 스코프를 활용하여 삭제되지 않은 모델만 조회하도록 동작합니다. 직접 글로벌 스코프를 작성하면, 특정 조건을 모든 쿼리에 일관되게 적용하기가 더욱 편해집니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성

새로운 글로벌 스코프 클래스를 생성하려면, `make:scope` Artisan 명령어를 사용합니다. 이 명령어는 `app/Models/Scopes` 디렉토리에 스코프 파일을 생성합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프 작성 방법은 간단합니다. `make:scope` 명령어로 생성된 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현합니다. 이 인터페이스에서 요구하는 것은 `apply` 메서드 하나입니다. 이 메서드 안에서 쿼리에 `where` 등의 조건을 추가하면 됩니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프에서 select 구문에 컬럼을 추가한다면, 기존 select 구문이 의도치 않게 대체되지 않도록 반드시 `select`가 아닌 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

모델에 글로벌 스코프를 적용하려면, 모델에 `ScopedBy` 속성(Attribute)을 붙이면 됩니다:

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

또는, 수동으로 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope`를 호출하는 방법도 있습니다. `addGlobalScope`에는 스코프 클래스의 인스턴스를 넘깁니다:

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

위 예시처럼 스코프를 적용하면, `User::all()` 호출 시 실제로 다음과 같은 SQL이 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(Anonymous) 글로벌 스코프

간단한 글로벌 스코프라면, 클래스를 따로 만들지 않고 클로저로 정의할 수도 있습니다. 이럴 때는 `addGlobalScope`의 첫 번째 인수로 임의의 스코프명을 같이 지정합니다:

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
            $builder->where('created_at', '<', now()->minus(years: 2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 글로벌 스코프 제거

특정 쿼리에서 글로벌 스코프를 빼고 싶다면, `withoutGlobalScope` 메서드를 사용하세요. 인수엔 스코프 클래스명을 넘깁니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의한 경우엔, 글로벌 스코프명 문자열을 넘깁니다:

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개(또는 전체) 글로벌 스코프를 제거하고 싶을 땐, `withoutGlobalScopes`와 `withoutGlobalScopesExcept`를 사용할 수 있습니다:

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 특정 글로벌 스코프만 남기고 나머지 제거
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 쓰는 쿼리 조건 세트를 쉽게 재활용하도록 해줍니다. 예를 들어, "인기(Popular) 사용자만 조회" 같은 조건이 자주 필요하다면, Eloquent 메서드에 `Scope` 속성을 붙여 스코프를 정의할 수 있습니다.

스코프는 항상 동일한 쿼리 빌더 인스턴스 또는 void를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자만 포함하도록 쿼리 스코프
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 포함하도록 쿼리 스코프
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

스코프를 정의하면, 모델 쿼리에서 스코프 메서드를 연쇄적으로 호출할 수 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 or 조건으로 묶을 땐, [논리적 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 써야 할 수도 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이 과정이 번거롭다면, Laravel의 "higher order" `orWhere` 방법을 사용해 더욱 간결하게 체이닝할 수 있습니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적(Dynamic) 스코프

파라미터를 받는 스코프도 쉽게 만들 수 있습니다. 쿼리 스코프 메서드 시그니처에 `$query` 이후 파라미터를 추가하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입의 사용자로 쿼리 스코프
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

스코프 메서드에 인자를 추가했다면, 실제 쿼리 호출 시 함께 넘기면 됩니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 예정된 속성(Pending Attributes)

스코프를 이용해 쿼리뿐 아니라, 조건에 맞는 속성을 가진 모델을 생성하려면 쿼리 빌더에서 `withAttributes` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시글만 조회하도록 쿼리 스코프
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

`withAttributes` 메서드는 주어진 속성으로 쿼리에 `where` 조건을 추가하고, 해당 속성이 있는 모델을 생성합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

속성을 실제 쿼리 조건으로 쓰지 않고 싶다면, `asConditions` 인수를 `false`로 설정하세요:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "동일한"지 여부를 확인해야 할 때가 있습니다. `is`, `isNot` 메서드를 사용해 두 모델이 동일한 기본 키, 테이블, DB 연결을 갖는지 간단히 검사할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

이 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` 등 [관계](/docs/12.x/eloquent-relationships)에서도 사용할 수 있습니다. 관련 모델이 쿼리를 타지 않고 바로 비교할 수 있어 편리합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션으로 직접 브로드캐스팅하고 싶다면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 디스패치(dispatch)하며, 이를 통해 모델의 생명주기 중 특정 시점에 후킹(hooking)할 수 있습니다. 이벤트 종류는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등이 있습니다.

각 이벤트는 다음과 같이 발생합니다:
- `retrieved`: 모델이 DB로부터 조회될 때
- `creating`, `created`: 새 모델이 처음 저장될 때
- `updating`, `updated`: 기존 모델이 수정된 후 `save` 메서드가 호출될 때
- `saving`, `saved`: 모델이 생성/수정될 때(속성이 변경되지 않아도)
- `-ing`로 끝나는 이벤트들은 변경이 실제 DB에 반영되기 "이전"에, `-ed`로 끝나는 이벤트들은 반영 "이후"에 발생합니다

모델의 이벤트를 리스닝하려면, 모델의 `$dispatchesEvents` 속성에서 Eloquent 이벤트와 [이벤트 클래스](/docs/12.x/events)를 매핑하세요. 각 모델 이벤트 클래스는 영향을 받은 모델 인스턴스를 생성자 인자로 받습니다:

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
     * 모델 이벤트별 매핑
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의/매핑한 뒤에는, [이벤트 리스너](/docs/12.x/events#defining-listeners)로 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent에서 대량 업데이트/삭제 쿼리가 실행될 때는, 해당 모델 이벤트(`saved`, `updated`, `deleting`, `deleted`)가 발생하지 않습니다. 이는 모델이 실제로 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 활용

이벤트 클래스를 따로 만들지 않고, 클로저 형태의 리스너를 등록해도 됩니다. 일반적으로 이 클로저 등록은 모델의 `booted` 메서드에서 수행합니다:

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

필요하다면, [큐로 처리되는 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)도 사용할 수 있습니다. 이 경우 이벤트 리스너가 백그라운드 큐에서 실행됩니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵서버(Observer)

<a name="defining-observers"></a>
#### 옵서버 정의

한 모델에 대해 많은 이벤트를 리스닝하려면, 옵서버 클래스를 통해 리스너를 한 곳에 모아서 정의할 수 있습니다. 옵서버 클래스에는 각 Eloquent 이벤트와 동일한 이름의 메서드를 만듭니다. 모든 메서드는 영향을 받은 모델 인스턴스를 인수로 받습니다. 옵서버 클래스를 만드는 가장 쉬운 방법은 `make:observer` Artisan 명령어를 사용하는 것입니다:

```shell
php artisan make:observer UserObserver --model=User
```

옵서버는 `app/Observers` 디렉토리에 생성되며, 해당 디렉토리가 없으면 Artisan이 자동 생성합니다. 기본 옵서버 예시는 다음과 같습니다:

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

옵서버를 등록하는 방법은 두 가지입니다. 첫째, 모델에 `ObservedBy` 속성을 붙입니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, `AppServiceProvider`의 `boot` 메서드 등에서 `observe` 메서드로 수동 등록할 수도 있습니다:

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
> `saving`, `retrieved` 등, 옵서버에서 리슨할 수 있는 추가 이벤트가 있습니다. 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵서버와 DB 트랜잭션

모델이 데이터베이스 트랜잭션 중 생성되는 경우, 옵서버에서 이벤트 핸들러를 트랜잭션 커밋 후에만 실행하게 할 수 있습니다. 이를 위해 옵서버 클래스에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현합니다. 트랜잭션 중이 아니면 즉시 이벤트 핸들러가 실행됩니다:

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
### 이벤트 음소거(Muting Events)

일시적으로 특정 모델의 이벤트 디스패치를 중지(음소거)하고 싶으면 `withoutEvents` 메서드를 사용할 수 있습니다. 이 메서드는 클로저를 받아, 그 안에서 발생하는 모델 이벤트를 모두 비활성화합니다. 반환값은 클로저에서 반환된 값입니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 저장 시 이벤트 비활성화

특정 모델 인스턴스의 저장 시점에만 이벤트를 발생시키지 않으려면, `saveQuietly` 메서드를 사용할 수 있습니다:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

마찬가지로, "update", "delete", "soft delete", "restore", "replicate" 동작도 각각 `updateQuietly`, `deleteQuietly`, `forceDeleteQuietly`, `restoreQuietly` 등으로 이벤트 없이 실행할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
