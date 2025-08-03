# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성하기](#generating-model-classes)
- [Eloquent 모델 규약](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [청크 단위 처리](#chunking-results)
    - [래지 컬렉션을 사용한 청크 단위 처리](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 데이터 조회하기](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 데이터 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제하기](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 가지치기(Pruning)](#pruning-models)
- [모델 복제하기](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [전역 스코프(Global Scopes)](#global-scopes)
    - [지역 스코프(Local Scopes)](#local-scopes)
    - [대기 속성(Pending Attributes)](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저를 사용한 이벤트](#events-using-closures)
    - [옵저버(Observers)](#observers)
    - [이벤트 무음 처리](#muting-events)

<a name="introduction"></a>
## 소개

Laravel에는 데이터베이스와 즐겁게 상호작용할 수 있도록 해주는 객체 관계 매퍼(Object-Relational Mapper, ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용할 때 각 데이터베이스 테이블은 해당 테이블과 상호작용하는 데 사용되는 "모델"에 대응됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라 테이블에 레코드를 삽입, 업데이트, 삭제할 수 있습니다.

> [!NOTE]  
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 설정해야 합니다. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/11.x/database#configuration)를 참고하세요.

#### Laravel 부트캠프

Laravel이 처음이라면, [Laravel 부트캠프](https://bootcamp.laravel.com)를 방문해 보세요. Laravel 부트캠프는 Eloquent를 사용해 첫 번째 Laravel 애플리케이션을 만드는 과정을 자세히 안내합니다. Laravel과 Eloquent가 제공하는 모든 기능을 한눈에 파악하기 좋은 방법입니다.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기

시작하려면 Eloquent 모델을 만들어 보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 상속받습니다. `make:model` Artisan 명령어를 사용해 새 모델을 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/11.x/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책, 컨트롤러, 폼 요청 클래스와 같은 다양한 클래스도 함께 생성할 수 있습니다. 서로 다른 옵션을 조합해 여러 클래스를 한 번에 만들 수도 있습니다:

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

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 모두 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델과 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델과 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 클래스 생성 단축 옵션...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인하기

코드를 훑어보는 것만으로는 모델에 어떤 속성과 연관관계가 있는지 파악하기 어려운 경우가 있습니다. 이럴 때 `model:show` Artisan 명령어를 사용하면 모델의 속성과 연관관계 정보를 간편하게 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규약

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 다음은 기본 모델 클래스 예시입니다. Eloquent의 주요 규약 몇 가지를 같이 살펴보겠습니다:

```
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

위 예시에서 보셨듯이 `Flight` 모델에 대응되는 데이터베이스 테이블 이름을 따로 지정하지 않았습니다. Eloquent는 기본적으로 클래스명을 "스네이크 케이스(snake_case)" 형태의 복수형으로 바꾼 것을 테이블 이름으로 사용합니다. 따라서 `Flight` 모델은 `flights` 테이블과 자동으로 연결되고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결됩니다.

만약 모델에 대응되는 데이터베이스 테이블 이름이 이러한 기본 규칙에 맞지 않는 경우, 모델 클래스 내에 `table` 속성을 정의하여 직접 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델과 연결된 테이블 이름입니다.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 모델에 연결된 데이터베이스 테이블이 기본 키 컬럼으로 `id`를 가진다고 가정합니다. 다른 컬럼을 기본 키로 사용하고 싶다면, 모델 클래스에서 `$primaryKey` 속성을 정의해 해당 컬럼명을 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연결된 테이블의 기본 키 컬럼명입니다.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 Eloquent는 기본 키가 자동 증가하는 정수형이라고 가정합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용하려면, 공개 속성 `$incrementing`을 `false`로 설정해야 합니다:

```
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동 증가하는지 여부입니다.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아닌 경우, `$keyType` 속성을 `string`으로 설정하여 기본 키 데이터 타입을 명시해야 합니다:

```
<?php

class Flight extends Model
{
    /**
     * 기본 키 ID의 데이터 타입입니다.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### 복합 기본 키("Composite" Primary Keys)

Eloquent 모델은 고유 식별자로서 최소 하나의 "ID"가 반드시 필요합니다. 복합 기본 키(여러 컬럼으로 구성된 기본 키)는 지원하지 않습니다. 다만, 기본 키 이외에 여러 컬럼으로 구성된 고유 인덱스는 자유롭게 생성할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

자동 증가하는 정수 대신 UUID를 사용해 Eloquent 모델의 기본 키를 만들 수 있습니다. UUID는 36자리의 전 세계 고유 식별자입니다.

모델에서 UUID 기본 키를 사용하고 싶으면, `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 모델에 추가하세요. 물론, 모델의 데이터베이스 테이블에 UUID 대응 컬럼이 있어야 합니다([UUID 컬럼 방법](/docs/11.x/migrations#column-method-uuid)):

```
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

기본적으로 `HasUuids` 트레이트는 ["정렬 가능한" UUID](/docs/11.x/strings#method-str-ordered-uuid)를 생성합니다. 이들은 레거시식 UUID보다 데이터베이스 인덱싱에 더 효율적입니다.

특정 모델에서 UUID 생성 로직을 재정의하려면 `newUniqueId` 메서드를 정의할 수 있습니다. 또한, UUID가 부여될 컬럼을 `uniqueIds` 메서드로 지정할 수도 있습니다:

```
use Ramsey\Uuid\Uuid;

/**
 * 모델에 부여할 새로운 UUID를 생성합니다.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID가 부여되어야 하는 컬럼명을 포함하는 배열을 반환합니다.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

UUID 대신 ULID를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26자리이며, 정렬 가능하다는 점도 비슷합니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 추가하세요. 그리고 ULID 대응 컬럼이 데이터베이스에 있어야 합니다([ULID 컬럼 방법](/docs/11.x/migrations#column-method-ulid)):

```
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

기본적으로 Eloquent는 모델과 연결된 데이터베이스 테이블에 `created_at` 및 `updated_at` 컬럼이 존재한다고 가정합니다. 모델 생성 또는 업데이트 시 자동으로 이 컬럼들이 관리됩니다. 만약 이러한 자동 관리가 원치 않는다면, 모델에 `$timestamps` 속성을 `false`로 설정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 타임스탬프가 자동으로 관리되는지 여부입니다.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델 타임스탬프의 저장 형식을 변경하고 싶다면 `$dateFormat` 속성을 설정할 수 있습니다. 이 속성은 데이터베이스 저장 및 배열/JSON 직렬화 시 날짜 형식을 결정합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 컬럼 저장 형식입니다.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼 이름을 직접 지정하고 싶으면 `CREATED_AT`과 `UPDATED_AT` 상수를 모델에 정의하세요:

```
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프를 변경하지 않고 모델 작업을 수행하려면 `withoutTimestamps` 메서드에 클로저를 넘겨 작업할 수 있습니다:

```
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션 기본 데이터베이스 연결을 사용합니다. 특정 모델에 다른 연결을 지정하려면 모델에 `$connection` 속성을 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 사용할 데이터베이스 연결명입니다.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

새로 생성한 모델 인스턴스에는 기본적으로 속성 값이 없습니다. 모델의 어떤 속성에 기본값을 지정하고 싶으면 `$attributes` 속성을 설정하세요. 이 때, 기본값들은 데이터베이스에서 읽은 원시(raw) 상태 값이어야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 속성 기본값들입니다.
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

Laravel은 다양한 상황에서 Eloquent 동작의 엄격함(strictness)을 설정할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩을 방지할지 여부를 불리언 인수로 받습니다. 예를 들어, 프로덕션 환경에서는 지연 로딩을 허용하지만 로컬 개발 환경에서는 방지하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드 내에서 호출됩니다:

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

또한 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 `fillable` 배열에 없는 속성이 대량 할당될 때 예외를 발생시키도록 설정할 수 있습니다. 이렇게 하면 로컬 개발 중에 의도하지 않은 속성 무시로 인해 발생할 수 있는 문제를 조기에 발견할 수 있습니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [연관된 데이터베이스 테이블이 준비되면](/docs/11.x/migrations#generating-migrations) 데이터 조회를 시작할 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/11.x/queries) 역할도 하여, 해당 모델과 연결된 테이블에 대한 데이터베이스 쿼리를 유창하게 작성할 수 있습니다. 모델의 `all` 메서드는 테이블 내 모든 레코드를 가져옵니다:

```
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드

`all` 메서드는 테이블의 모든 결과를 반환합니다. 하지만 모델은 쿼리 빌더이므로, 추가 조건을 붙이고 `get` 메서드를 호출해 원하는 결과만 조회할 수 있습니다:

```
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->take(10)
    ->get();
```

> [!NOTE]  
> Eloquent 모델에서 Laravel의 [쿼리 빌더](/docs/11.x/queries)가 제공하는 모든 메서드를 사용할 수 있으니 참고하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 불러온 모델 인스턴스가 있다면, `fresh` 또는 `refresh` 메서드로 모델을 "새로고침"할 수 있습니다. `fresh`는 데이터베이스에서 다시 모델을 불러오지만 기존 모델 인스턴스는 변경하지 않습니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 모델 인스턴스의 속성과 함께 로드된 관계까지 데이터베이스 상태로 갱신합니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`, `get` 메서드들은 단순 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

`Collection` 클래스는 Laravel 기본 `Illuminate\Support\Collection`을 상속하며, 데이터 컬렉션을 다루기 위한 풍부한 메서드들을 제공합니다. 예를 들어, `reject` 메서드를 사용해 특정 조건에 맞는 모델을 컬렉션에서 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션에는 Eloquent 모델 컬렉션에 특화된 몇 가지 추가 메서드도 있습니다.

Laravel 컬렉션들은 PHP의 iterable 인터페이스를 구현하므로, 마치 배열처럼 반복문을 통해 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크 단위 처리

`all`이나 `get` 메서드로 수만 건 이상의 Eloquent 레코드를 한 번에 불러오면 메모리 부족 문제가 발생할 수 있습니다. 이럴 때 `chunk` 메서드를 사용하면 대량 데이터를 부분 단위로 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 지정한 개수 만큼 레코드를 조회해 클로저로 전달합니다. 한번에 메모리에 올리는 양이 적어 메모리 사용량이 대폭 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

첫 번째 인수는 청크 단위로 받을 레코드 개수이며, 두 번째 인수인 클로저는 청크마다 호출됩니다.

만약 청크 결과에서 특정 컬럼을 기준으로 조건을 걸고 해당 컬럼을 업데이트하며 처리한다면, `chunkById` 메서드를 쓰는 것이 좋습니다. `chunk` 메서드는 이 경우 의도치 않은 결과가 발생할 수 있기 때문입니다. `chunkById`는 내부적으로 마지막 청크의 `id`보다 큰 값을 가진 레코드를 넘어가면서 읽습니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 추가로 쿼리에 `where` 조건을 붙이므로, 자신의 조건은 `[논리 그룹화](/docs/11.x/queries#logical-grouping)`를 활용해 묶어주는 것이 좋습니다:

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
### 래지 컬렉션을 사용한 청크 단위 처리

`lazy` 메서드는 [청크 단위 처리](#chunking-results)와 유사하게 데이터를 부분 조회하지만, 클로저에 바로 전달하는 대신 전체 결과가 단일 스트림처럼 처리 가능한 [`LazyCollection`](/docs/11.x/collections#lazy-collections)을 반환합니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

만약 `lazy` 메서드 결과에서 특정 컬럼을 기준으로 조건을 걸고 업데이트를 병행해야 한다면 `lazyById` 메서드를 사용하세요. 내부적으로 `id` 컬럼 기준으로 누적 처리됩니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id` 내림차순 정렬 기준으로 처리할 수도 있습니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy` 메서드처럼, `cursor` 메서드도 수만 건 이상 데이터 조회 시 메모리 사용량을 크게 줄여줍니다.

`cursor`는 단 한 번의 쿼리를 실행하되, 모델 인스턴스를 실제로 순회할 때까지 생성하지 않고 한 번에 하나씩 메모리에 보관합니다.

> [!WARNING]  
> `cursor`는 메모리에 모델을 하나만 올리므로 관계를 사전로딩(eager load)할 수 없습니다. 관계 로딩이 필요하면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

내부적으로 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. 일반 컬렉션과 유사한 메서드들을 이용하면서도 한 번에 하나씩 메모리에 올리고 순회 가능합니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 메모리 사용을 훨씬 줄여주지만, PHP의 PDO 드라이버의 내부 결과 버퍼링 때문에 결국 메모리가 부족해질 수 있습니다. 매우 많은 레코드를 다뤄야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리를 지원하여 관련 테이블에서 정보를 한 번의 쿼리로 가져올 수 있습니다.

예를 들어 `destinations` 테이블과, 도착 시간을 나타내는 `arrived_at` 컬럼이 있는 `flights` 테이블이 있다고 가정해 봅시다.

쿼리 빌더의 `select`, `addSelect` 메서드에서 서브쿼리를 활용해 모든 목적지와 해당 목적지로 가장 최근 도착한 비행기 이름을 한 번에 조회할 수 있습니다:

```
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

쿼리 빌더는 `orderBy` 안에 서브쿼리도 지원합니다.

같은 예시에서 마지막 비행기 도착 시점 기준으로 목적지를 정렬할 수도 있습니다:

```
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 데이터 조회하기

쿼리에 맞는 모든 결과를 조회하는 것 외에 `find`, `first`, `firstWhere` 메서드를 이용해 단일 모델 인스턴스를 받아올 수도 있습니다:

```
use App\Models\Flight;

// 기본 키 기준으로 모델 조회...
$flight = Flight::find(1);

// 쿼리 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건에 맞는 첫 모델 조회 대체 문법...
$flight = Flight::firstWhere('active', 1);
```

찾는 결과가 없을 때 다른 동작을 수행하고 싶다면, `findOr`와 `firstOr` 메서드를 사용할 수 있습니다. 결과가 없으면 주어진 클로저를 실행하며, 클로저 반환값이 최종 결과가 됩니다:

```
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 찾을 수 없음 예외

모델을 찾지 못했을 경우 예외를 던지고 싶은 경우가 있습니다. 특히 라우트나 컨트롤러에서 유용합니다. `findOrFail` 및 `firstOrFail` 메서드는 쿼리 결과가 없을 때 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

이 예외를 잡지 않으면 자동으로 404 HTTP 응답이 클라이언트에 전달됩니다:

```
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 지정한 조건으로 데이터베이스에서 레코드를 찾고, 없으면 첫 번째 배열 인수의 조건과 두 번째 배열 인수를 합친 속성으로 새 레코드를 생성하고 저장합니다.

`firstOrNew`는 동일한 조건으로 레코드를 조회하지만, 없으면 새 모델 인스턴스만 반환하며 저장하지는 않습니다(직접 `save` 호출 필요):

```
use App\Models\Flight;

// 이름으로 비행기 조회, 없으면 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지연 여부와 도착 시간도 함께 지정해 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 모델 인스턴스 초기화...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지정한 속성 포함 새 인스턴스 생성...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 데이터 조회

Eloquent 모델에서 Laravel [쿼리 빌더](/docs/11.x/queries)가 제공하는 `count`, `sum`, `max` 등의 [집계 메서드](/docs/11.x/queries#aggregates)를 사용할 수 있습니다. 이들은 모델 인스턴스 대신 스칼라 값을 반환합니다:

```
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때는 모델을 데이터베이스에 삽입하는 것도 매우 간편합니다. 새 모델 인스턴스를 생성한 뒤, 속성을 설정하고 `save` 메서드를 호출하세요:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 비행기를 데이터베이스에 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        // 요청 데이터 유효성 검사...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

위 예제에서 HTTP 요청으로 받은 `name` 필드를 `Flight` 모델의 `name` 속성에 할당하고, `save`를 호출해 데이터베이스에 삽입합니다. `save` 시 자동으로 `created_at`과 `updated_at` 타임스탬프가 설정됩니다.

또는 `create` 메서드를 이용해 한 줄로 새 모델을 저장하고 삽입된 모델 인스턴스를 받을 수 있습니다:

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

`create` 메서드를 사용하려면 먼저 모델 클래스에서 `fillable` 또는 `guarded` 속성을 정의해 대량 할당(mass assignment) 보호를 해야 합니다. 대량 할당에 관한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

존재하는 데이터도 `save` 메서드로 업데이트할 수 있습니다. 모델을 조회해 변경할 속성을 지정하고 `save`를 호출하면 됩니다. `updated_at`은 자동으로 갱신됩니다:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

기존 모델이 있으면 업데이트하고, 없으면 새로 생성하고 싶다면 `updateOrCreate` 메서드를 사용할 수 있습니다. 이 메서드는 내부적으로 모델을 저장하기 때문에 따로 `save`를 호출할 필요가 없습니다:

```
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

여러 모델을 조건으로 한꺼번에 업데이트할 수도 있습니다. 예를 들어, 활성 상태이며 목적지가 `San Diego`인 모든 비행기를 지연 상태로 표시하려면:

```
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 칼럼과 값을 담은 배열을 받습니다. 작업 결과로 영향을 받은 행 수를 반환합니다.

> [!WARNING]  
> Eloquent에서 대량 업데이트 시 해당 모델들의 `saving`, `saved`, `updating`, `updated` 이벤트는 발생하지 않습니다. 모델 자체를 조회하지 않고 바로 쿼리를 실행하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 상태 확인하기

Eloquent는 모델 내부 상태를 검사해 속성이 변경됐는지 알 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

- `isDirty`: 모델 로드 이후 속성이 변경되었는지 검사. 특정 속성 또는 속성 배열도 전달 가능
- `isClean`: 속성이 변경되지 않았는지 검사. 인수로 속성명도 전달 가능
- `wasChanged`: 마지막 저장 작업 시 속성이 변경되었는지 검사. 속성명 전달 가능

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

원본 속성값을 확인하려면 `getOriginal` 메서드를 사용합니다. 인수로 특정 속성명을 넘기면 해당 속성의 원본 값을 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = "Jack";
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열 반환
```

<a name="mass-assignment"></a>
### 대량 할당

`create` 메서드는 한 줄로 모델을 생성하고 저장할 수 있으며, 삽입된 모델 인스턴스를 반환합니다:

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 대량 할당 이전에 모델 클래스에서 `fillable` 또는 `guarded` 속성을 정의해야 합니다. 기본적으로 Eloquent는 대량 할당 취약점을 막기 위해 이를 요구합니다.

대량 할당 취약점은 유저가 예상치 못한 HTTP 요청 필드를 보내 모델 속성을 임의로 조작할 때 발생할 수 있습니다. 예를 들어 인증되지 않은 유저가 `is_admin` 파라미터를 보내어 권한 상승하는 상황입니다.

따라서 어떤 속성을 대량 할당 가능하게 열어둘지 `$fillable` 배열에 명확히 지정하는 것이 중요합니다. 예를 들어, `Flight` 모델의 `name` 속성만 대량 할당을 허용하려면:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용되는 속성명 배열입니다.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

`fillable` 설정 후에는 `create`로 바로 삽입하거나, 이미 생성한 모델 인스턴스에 `fill` 메서드로 속성을 채울 수 있습니다:

```
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 타입 컬럼에 값을 대량 할당하려면, JSON 키도 `fillable`에 명시해야 합니다. Laravel은 보안을 위해 `guarded` 설정 시 중첩 JSON 속성 업데이트를 지원하지 않습니다:

```
/**
 * 대량 할당이 허용되는 속성들입니다.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용하기

모든 속성을 대량 할당 가능하게 하려면 모델의 `$guarded` 속성을 빈 배열로 설정할 수 있습니다. 이 경우 `fill`, `create`, `update` 메서드에 전달하는 배열은 반드시 직접 조작해서 넘겨야 안전합니다:

```
/**
 * 대량 할당 허용하지 않는 속성 배열 또는 false
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 속하지 않는 속성은 조용히 무시됩니다. 프로덕션 환경에서는 기대하는 동작이지만, 로컬 개발 때 왜 속성이 반영되지 않는지 혼란스러울 수 있습니다.

이럴 경우 예외를 발생시키도록 Laravel 설정할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```
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

`upsert` 메서드는 단일 원자적 작업으로 존재하는 데이터를 업데이트하거나, 없으면 새 데이터로 삽입합니다. 첫 번째 인자는 삽입 또는 업데이트할 값들의 배열, 두 번째 인자는 테이블 내 고유한 레코드를 식별할 컬럼명 배열, 세 번째 인자는 업데이트할 컬럼 배열입니다.

`upsert`는 모델에 타임스탬프가 활성화돼 있으면 자동으로 `created_at`, `updated_at`을 갱신합니다:

```
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]  
> SQL Server를 제외한 모든 데이터베이스는 두 번째 인수에 지정한 컬럼에 "기본키" 또는 "유니크" 인덱스가 있어야 합니다. MariaDB와 MySQL 드라이버는 `upsert` 두 번째 인수를 무시하고, 테이블의 기본키와 유니크 인덱스를 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제하기

모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출하세요:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키 기준 기존 모델 삭제

위 예시에서는 먼저 모델을 조회한 후 삭제했습니다. 하지만 기본 키를 알고 있으면 `destroy` 메서드를 통해 조회 없이 삭제할 수 있습니다. 단일 키, 여러 키, 배열 또는 컬렉션 모두 받을 수 있습니다:

```
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

소프트 삭제 기능을 사용하면 `forceDestroy`를 통해 영구 삭제할 수 있습니다:

```
Flight::forceDestroy(1);
```

> [!WARNING]  
> `destroy`는 각 모델을 개별 조회 후 `delete`를 호출하므로 `deleting`과 `deleted` 이벤트가 정확히 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

조건에 맞는 모든 모델을 한꺼번에 삭제 가능하며, `active`가 0인 비행기 모두 삭제 예시는 다음과 같습니다. 대량 삭제 시는 이벤트가 발생하지 않으니 주의하세요:

```
$deleted = Flight::where('active', 0)->delete();
```

조건을 지정하지 않고 쿼리로 테이블 내 모든 모델을 삭제할 수도 있습니다:

```
$deleted = Flight::query()->delete();
```

> [!WARNING]  
> 대량 삭제 시 모델 이벤트(`deleting`, `deleted`)는 발생하지 않습니다. 모델들을 조회하지 않고 바로 삭제 쿼리를 실행하기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

단순히 레코드를 삭제하는 대신 "소프트 삭제"도 할 수 있습니다. 소프트 삭제하면 실제로 데이터가 삭제되지는 않고 `deleted_at` 속성에 삭제 시각이 기록됩니다.

소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 포함하세요:

```
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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime`/`Carbon` 인스턴스로 캐스팅합니다.

데이터베이스 테이블에 `deleted_at` 컬럼도 추가해야 하며, Laravel [스키마 빌더](/docs/11.x/migrations)의 헬퍼 메서드를 사용할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```

`delete` 호출 시 `deleted_at` 컬럼에 시각이 기록되고 레코드는 테이블에 남아있지만, 소프트 삭제 활성화된 모델 조회 시 자동으로 제외됩니다.

해당 모델이 소프트 삭제됐는지 확인하려면 `trashed` 메서드를 사용하세요:

```
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

실수로 삭제했거나 다시 활성화하고 싶으면, 모델 인스턴스에서 `restore` 메서드를 호출하면 `deleted_at`이 `null`로 초기화됩니다:

```
$flight->restore();
```

쿼리에서도 복구 가능하며, 여기서도 복수 모델 복원이 가능하지만 이벤트는 발생하지 않습니다:

```
Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();
```

관계 쿼리에서도 `restore`를 사용할 수 있습니다:

```
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

진짜 완전한 삭제가 필요하다면 소프트 삭제 모델에 `forceDelete` 메서드를 호출하세요:

```
$flight->forceDelete();
```

관계 쿼리에서도 `forceDelete`를 사용할 수 있습니다:

```
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함하기

기본적으로 소프트 삭제된 모델은 조회 결과에서 제외됩니다. 하지만 `withTrashed` 메서드를 사용하면 삭제된 모델도 포함해서 조회할 수 있습니다:

```
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 사용할 수 있습니다:

```
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드는 오직 소프트 삭제된 모델만 조회합니다:

```
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

필요 없는 모델을 주기적으로 삭제하려면, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 모델에 추가하세요. 그리고 `prunable` 메서드에서 삭제 조건 쿼리를 작성합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * 삭제 대상 모델을 조회하는 쿼리입니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable`을 설정한 모델은 `pruning` 메서드를 추가해 실제 삭제 전 처리 작업을 할 수 있습니다(파일 정리 등):

```
/**
 * 모델 삭제 전 준비 작업입니다.
 */
protected function pruning(): void
{
    // ...
}
```

가지치기 설정 후, Artisan `model:prune` 명령어를 스케줄에 등록해 주기적으로 실행하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령어는 기본적으로 `app/Models` 내의 prunable 모델을 자동으로 탐지합니다. 모델이 다른 경로에 있다면 `--model` 옵션으로 지정할 수 있습니다:

```
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델을 제외하고 가지치기하려면 `--except` 옵션을 사용하세요:

```
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션과 함께 실행하면 실제 삭제 없이 삭제될 레코드 수만 출력합니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]  
> 소프트 삭제 모델의 경우, 가지치기 조건에 맞으면 실제로 `forceDelete`를 통해 완전 삭제됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하면 대량 삭제 쿼리로 모델을 삭제합니다. 이 때 `pruning` 메서드 호출과 `deleting`, `deleted` 이벤트 발생이 없으므로 처리 속도가 매우 빠릅니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * 삭제 대상 모델을 조회하는 쿼리입니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제하기

`replicate` 메서드를 사용하면 기존 모델 인스턴스를 새로운 저장되지 않은 복사본으로 만들 수 있습니다. 여러 속성을 공유하는 모델들을 복제해야 할 때 유용합니다:

```
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

복제 시 제외할 속성을 배열로 넘길 수도 있습니다:

```
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
### 전역 스코프(Global Scopes)

전역 스코프를 설정하면 특정 모델 쿼리에 항상 특정 조건을 자동으로 적용할 수 있습니다. Laravel 내장 기능인 [소프트 삭제](#soft-deleting)의 경우, 삭제된 모델을 자동 제외하는 데 전역 스코프를 활용합니다.

자신만의 전역 스코프를 만들어 전 애플리케이션에서 특정 제약 조건을 자동으로 적용하는 데 편리합니다.

<a name="generating-scopes"></a>
#### 스코프 생성

새 전역 스코프 클래스를 만들려면 `make:scope` Artisan 명령어를 사용하세요. 생성된 스코프 클래스는 `app/Models/Scopes` 디렉터리에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성

전역 스코프는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스입니다. `apply` 메서드가 필수이며, 쿼리 빌더에 `where` 조건 등을 추가하는 역할을 합니다:

```
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
> 전역 스코프에서 `select` 절에 컬럼을 추가할 때는 기존 선택 컬럼이 덮어쓰이지 않도록 `select` 대신 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용

모델 클래스에 `ScopedBy` 속성을 지정하면 전역 스코프를 할당할 수 있습니다:

```
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

또는 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope`를 호출해 수동으로 스코프를 등록할 수도 있습니다:

```
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 부트스트랩 메서드입니다.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위와 같이 `App\Models\User` 모델에 스코프를 추가하면 `User::all()` 호출 시 다음과 같은 SQL 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 전역 스코프

긴 클래스를 만들지 않고 간단한 스코프는 클로저로도 정의할 수 있습니다. 이 경우 `addGlobalScope` 첫 번째 인수로 원하는 이름을 지정해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 부트스트랩 메서드입니다.
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
#### 전역 스코프 해제

특정 쿼리에서 전역 스코프를 제외하려면 `withoutGlobalScope` 메서드를 사용하세요. 인수로 스코프 클래스명이나 익명 스코프 이름을 넘깁니다:

```
User::withoutGlobalScope(AncientScope::class)->get();
```

```
User::withoutGlobalScope('ancient')->get();
```

여러 개 혹은 모든 전역 스코프를 제외하려면 `withoutGlobalScopes`를 사용합니다:

```
// 모든 전역 스코프 제외...
User::withoutGlobalScopes()->get();

// 일부 스코프 제외...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 지역 스코프(Local Scopes)

지역 스코프는 공통 쿼리 조건 묶음을 정의해 재사용하기 편리하도록 해줍니다. 모델 메서드명 앞에 `scope`를 붙여 정의합니다.

스코프는 항상 같은 쿼리 빌더 인스턴스를 반환하거나 `void`여야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자 조건을 추가하는 스코프입니다.
     */
    public function scopePopular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자 조건을 추가하는 스코프입니다.
     */
    public function scopeActive(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 지역 스코프 사용하기

스코프가 정의된 후에는, `scope` 접두어 없이 스코드 이름만 호출해 쿼리에 적용할 수 있습니다. 여러 스코프 호출도 체인으로 연결할 수 있습니다:

```
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 연산자로 여러 스코프를 결합할 때는 의도치 않은 논리 오류가 있을 수 있으므로, 클로저로 감싸 논리 그룹화하는 것이 안전합니다:

```
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

Laravel은 클로저 없이도 스코프 체인을 가능하게 하는 고차원 `orWhere` 메서드를 제공합니다:

```
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

인자를 받는 스코프도 가능합니다. 인자는 `$query` 다음에 선언합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 조회하는 스코프입니다.
     */
    public function scopeOfType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

스코프 호출 시 인자를 넘겨 사용하세요:

```
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 속성(Pending Attributes)

스코프 내에서 지정한 조건과 같은 속성을 가진 모델을 생성하고자 하면 `withAttributes` 메서드를 활용할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 숨김 상태인 임시 초안 글만 조회하는 스코프입니다.
     */
    public function scopeDraft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

`withAttributes`는 지정한 속성을 쿼리에 `where` 조건으로 추가할 뿐 아니라, 스코프로 생성된 모델의 기본 속성으로도 설정합니다:

```
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

<a name="comparing-models"></a>
## 모델 비교하기

두 모델이 같은지 다른지 판단할 때는 `is`와 `isNot` 메서드를 사용합니다. 이들은 모델이 같은 기본 키, 테이블, 연결을 사용하는지 여부를 검사합니다:

```
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`belongsTo`, `hasOne`, `morphTo`, `morphOne`과 같은 관계에서도 `is`와 `isNot` 메서드를 사용할 수 있습니다. 관계 모델과 직접 DB 조회 없이 비교할 때 유용합니다:

```
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]  
> Eloquent 이벤트를 클라이언트에 직접 브로드캐스팅하려면 Laravel의 [모델 이벤트 브로드캐스팅](/docs/11.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 발생시켜, 모델 생명주기 내 다양한 시점에 훅을 걸 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 기존 모델을 DB에서 조회할 때 발생
- `creating`/`created`: 새 모델이 처음 저장될 때 발생
- `updating`/`updated`: 기존 모델이 수정되어 저장될 때 발생
- `saving`/`saved`: 모델 생성 또는 업데이트 시 항상 발생
- `-ing`로 끝나는 이벤트는 저장 전, `-ed`로 끝나는 이벤트는 저장 후 발생

모델 이벤트를 리스닝하려면 모델에 `$dispatchesEvents` 배열 속성을 정의하고, 각 이벤트명에 대응하는 이벤트 클래스를 할당하세요. 이벤트 클래스는 생성자에 영향을 받은 모델 인스턴스를 받습니다:

```
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
     * 모델 이벤트와 사용자 이벤트 클래스를 매핑합니다.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

`$dispatchesEvents` 설정 후에는 Laravel [이벤트 리스너](/docs/11.x/events#defining-listeners)로 이벤트를 처리할 수 있습니다.

> [!WARNING]  
> Eloquent로 대량 업데이트나 삭제 시 모델 이벤트(`saved`, `updated`, `deleting`, `deleted`)가 발생하지 않습니다. 모델을 실제 조회하지 않고 쿼리를 직접 실행하기 때문입니다.

<a name="events-using-closures"></a>
### 클로저를 사용한 이벤트

별도의 이벤트 클래스를 만들지 않고, 이벤트 발생 시 실행할 클로저를 직접 등록할 수 있습니다. 일반적으로 모델의 `booted` 메서드 내에 작성합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 부트스트랩 메서드입니다.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요 시 [큐잉 가능한 익명 이벤트 리스너](/docs/11.x/events#queuable-anonymous-event-listeners)를 활용해 이벤트 핸들러를 백그라운드 큐에서 실행할 수도 있습니다:

```
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버(Observers)

<a name="defining-observers"></a>
#### 옵저버 정의하기

여러 모델 이벤트를 한 클래스에 묶어 관리하려면 옵저버를 사용하세요. 옵저버 클래스는 이벤트명과 일치하는 메서드를 가지고, 해당 메서드는 영향을 받은 모델 인스턴스를 인수로 받습니다. `make:observer` Artisan 명령어가 새 옵저버 클래스 생성을 편리하게 해줍니다:

```shell
php artisan make:observer UserObserver --model=User
```

생성된 옵저버는 보통 `app/Observers` 디렉터리에 위치하며, 예시는 다음과 같습니다:

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User 모델이 "created" 이벤트 발생 시 처리.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User 모델이 "updated" 이벤트 발생 시 처리.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User 모델이 "deleted" 이벤트 발생 시 처리.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User 모델이 "restored" 이벤트 발생 시 처리.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User 모델이 "forceDeleted" 이벤트 발생 시 처리.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버 등록은 모델에 `ObservedBy` 속성을 붙이는 방법이 있습니다:

```
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는 `AppServiceProvider`의 `boot` 메서드 등에서 수동으로 등록할 수도 있습니다:

```
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
> 옵저버는 `saving`, `retrieved` 등 추가 모델 이벤트도 처리할 수 있습니다. 자세한 내용은 [이벤트 문서](#events)를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 트랜잭션 내에서 생성될 때, 옵저버가 트랜잭션 커밋 후에만 이벤트를 핸들링하도록 하려면, 옵저버 클래스가 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하게 하세요.

트랜잭션이 진행 중이 아니면 즉시 호출됩니다:

```
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 처리 메서드
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 무음 처리

일시적으로 모델 관련 이벤트를 발생시키고 싶지 않을 때 `withoutEvents` 메서드를 사용할 수 있습니다. 클로저 내에서는 이벤트가 발생하지 않으며, 클로저의 반환값이 `withoutEvents` 반환값이 됩니다:

```
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델을 이벤트 무음으로 저장하기

특정 모델을 저장할 때 이벤트를 발생시키지 않고 싶으면 `saveQuietly` 메서드를 사용하세요:

```
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

`update`, `delete`, `soft delete`, `restore`, `replicate` 작업도 `*Quietly` 버전으로 이벤트를 무음화할 수 있습니다:

```
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
