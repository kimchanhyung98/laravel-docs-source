# Eloquent: 시작하기

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [DB 연결](#database-connections)
    - [기본 속성값](#default-attribute-values)
    - [Eloquent의 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 분할(청킹)](#chunking-results)
    - [Lazy 컬렉션을 활용한 청킹](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입과 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [Upsert(있으면 수정, 없으면 삽입)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [전역 스코프](#global-scopes)
    - [지역 스코프](#local-scopes)
    - [Pending 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버(Observer)](#observers)
    - [이벤트 뮤트(비활성화)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와의 상호작용을 즐겁게 해주는 객체-관계 매퍼(ORM)인 Eloquent를 포함합니다. Eloquent를 사용할 때에는 데이터베이스의 각 테이블에 해당하는 “모델”이 존재하며, 이 모델을 통해 테이블과 상호작용합니다. 테이블에서 레코드를 조회할 뿐만 아니라, Eloquent 모델을 활용해 테이블에 레코드를 삽입, 수정, 삭제할 수도 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성하세요. 데이터베이스 구성에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/{{version}}/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해봅시다. 모델 클래스는 보통 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model`을 확장합니다. [Artisan 명령어](/docs/{{version}}/artisan) `make:model`을 사용해서 새 모델을 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델과 동시에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)를 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 등 다양한 관련 클래스를 함께 생성할 수도 있습니다. 옵션을 조합하면 여러 클래스를 한 번에 생성할 수 있습니다:

```shell
# 모델과 FlightFactory 클래스 생성
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델과 FlightSeeder 클래스 생성
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델과 FlightController 클래스 생성
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, 리소스 컨트롤러, 폼 리퀘스트 클래스 생성
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 모두 생성 (전체)
php artisan make:model Flight --all
php artisan make:model Flight -a

# Pivot 모델 생성
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 구조 확인

모델의 모든 속성과 관계를 코드만 보고 한눈에 파악하기 어렵다면, `model:show` Artisan 명령어로 모델의 속성과 관계 구조를 한 번에 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령으로 생성된 모델들은 `app/Models` 디렉터리에 위치합니다. 기본 모델 클래스를 살펴보며 Eloquent가 따르는 주요 관례를 알아봅시다:

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

위 예시에서 Eloquent에 `Flight` 모델이 어떤 테이블과 매칭되는지 명시하지 않는 걸 볼 수 있습니다. 관례상, 클래스명을 "스네이크 케이스"로 바꾸고 복수형으로 만든 이름이 테이블명으로 사용됩니다. 따라서, 위에서 `Flight` 모델은 `flights` 테이블과, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결됩니다.

테이블명이 이 관례와 맞지 않을 경우, 모델에 `table` 속성을 정의하여 명시적으로 테이블명을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 연관된 테이블명
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본키

Eloquent는 기본적으로 각 모델에 `id`라는 이름의 기본키 컬럼이 있다고 가정합니다. 다른 컬럼을 기본키로 사용하려면 `primaryKey` 속성을 지정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 테이블의 기본키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, Eloquent는 기본키가 자동증가하는 정수라고 가정합니다. 만약 자동증가나 숫자가 아닌 기본키를 사용하고 싶다면, 모델에 `$incrementing` 속성을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 자동 증가 사용 여부
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본키가 문자열인 경우, `$keyType` 속성을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본키 데이터 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본키

Eloquent는 각 모델에 고유한 "ID"가 있어야 하므로, 복합 기본키를 지원하지 않습니다. 하지만, 테이블에 여러 컬럼을 대상으로 고유 인덱스를 추가하는 것은 가능합니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본키로 자동증가 정수 대신 UUID(범용 고유 식별자)를 사용할 수도 있습니다. UUID는 36자 길이의 영숫자 식별자입니다.

UUID를 기본키로 사용하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 그리고 해당 컬럼이 [UUID 타입](/docs/{{version}}/migrations#column-method-uuid)이어야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // 예: "8f8e8478-9035-4d23-b9a7-62f4d2612ce5"
```

기본적으로 `HasUuids` 트레이트는 ["정렬 가능" UUID](/docs/{{version}}/strings#method-str-ordered-uuid)를 생성합니다. 이는 인덱싱에 더 효율적입니다.

UUID 생성 방식을 직접 바꾸고 싶다면 모델에 `newUniqueId` 메서드를 정의하세요. 또한, UUID를 부여할 컬럼을 지정하려면 `uniqueIds` 메서드를 정의하면 됩니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 새 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID 할당 대상 컬럼
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

또는 26자 길이의 ULID(우니크 lexicographically sortable identifiers)를 사용할 수도 있습니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 적용하면 됩니다. 해당 컬럼은 [ULID 타입](/docs/{{version}}/migrations#column-method-ulid)이어야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // 예: "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a name="timestamps"></a>
### 타임스탬프

Eloquent는 기본적으로 모델의 테이블에 `created_at` 과 `updated_at` 컬럼이 존재한다고 가정하고, 레코드가 작성·수정될 때 자동으로 값을 채웁니다. 이 기능을 사용하지 않으려면 `$timestamps` 속성을 `false`로 지정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 타임스탬프 관리 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프 포맷을 바꾸고 싶다면 `$dateFormat` 속성을 지정합니다. 이 속성은 DB 저장 및 직렬화(배열/JSON 변환)시 포맷을 결정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 칼럼의 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 바꾸려면 `CREATED_AT`와 `UPDATED_AT` 상수를 지정할 수 있습니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프를 수정하지 않고 모델을 조작하고 싶을 땐, `withoutTimestamps` 메서드로 클로저 내부에서 모델 작업을 수행할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 앱의 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 별도의 연결을 사용하고 싶을 경우, `$connection` 속성을 지정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 해당 모델이 사용할 연결명
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성값

모델 인스턴스를 새로 생성하면 기본적으로 아무런 속성값이 채워져 있지 않습니다. 특정 속성에 기본값을 설정하려면 `$attributes` 속성을 정의하면 됩니다. 값은 DB에서 읽어온 원본 형식이어야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 속성의 기본값
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
### Eloquent의 엄격성 설정

Eloquent의 동작 방식을 다양한 상황에 맞게 설정할 수 있습니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩을 방지할지 여부를 설정합니다. 예를 들면, 운영 환경이 아닐 때만 지연 로딩을 꺼서 개발 중 실수로 인해 운영에 영향이 없도록 할 수 있습니다. 이 메서드는 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 부트스트랩
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또, 모델에 없는 속성을 할당하려 할 때 예외를 던지길 원하면 `preventSilentlyDiscardingAttributes` 메서드를 호출하세요. 이는 `fillable`에 없는 속성 할당 시의 예기치 않은 실수 방지에 도움이 됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/{{version}}/migrations#generating-migrations)을 생성했다면, 이제 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델을 강력한 [쿼리 빌더](/docs/{{version}}/queries)로 생각할 수 있으며, 이 모델을 통해 연관된 테이블을 유연하게 조회할 수 있습니다. 모델의 `all` 메서드는 해당 모델의 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌딩

`all` 메서드는 모델의 모든 레코드를 반환하지만, Eloquent는 [쿼리 빌더](/docs/{{version}}/queries)이므로 추가 제약 조건을 쌓아 `get` 메서드로 결과를 얻을 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->take(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로 Laravel [쿼리 빌더](/docs/{{version}}/queries)가 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리 작성 시 이 메서드들을 활용하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

DB에서 가져온 Eloquent 모델 인스턴스가 있다면 `fresh` 또는 `refresh` 메서드로 새 데이터를 다시 가져올 수 있습니다. `fresh`는 새로 조회한 모델 인스턴스를 반환하며 기존 인스턴스에 영향이 없습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 인스턴스의 속성을 DB의 최신 값으로 덮어씁니다. 로드된 관계도 새로고침됩니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`, `get` 등으로 여러 레코드를 조회할 때, 반환값은 일반 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스입니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection`을 상속하며, [다양한 유용한 컬렉션 메서드](/docs/{{version}}/collections#available-methods)를 제공합니다. 예를 들어 `reject` 메서드는 클로저 결과에 따라 컬렉션에서 모델을 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션에는 [Eloquent 모델 컬렉션 전용 특화 메서드](/docs/{{version}}/eloquent-collections#available-methods)도 있습니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로 배열처럼 반복문을 돌릴 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 분할(청킹)

`all`이나 `get`으로 수 만 건을 한 번에 불러오면 메모리가 부족할 수 있습니다. 이럴 때는 `chunk` 메서드를 사용해 데이터를 효율적으로 분할 처리하세요.

`chunk` 메서드는 지정한 갯수만큼 모델을 부분적으로 조회해 클로저로 처리합니다. 따라서, 한 번에 전체를 로딩하지 않으므로 메모리 사용이 대폭 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

첫 번째 인자는 분할 단위(건수)이며, 두 번째 인자인 클로저는 각 청크마다 호출됩니다.

`chunk` 메서드를 사용해 조회한 결과의 특정 컬럼을 반복 처리하면서 동시에 수정(update)할 경우, `chunkById`를 이용해야 예기치 않은 결과를 방지할 수 있습니다. `chunkById`는 내부적으로 이전 청크 마지막 모델의 id보다 큰 id를 기준으로 다음 청크를 조회합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`, `lazyById`는 자체적으로 `where` 조건을 추가하므로, 여러 조건을 함께 사용하려면 [논리 그룹핑](/docs/{{version}}/queries#logical-grouping)으로 감싸는 게 좋습니다:

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
### Lazy 컬렉션을 활용한 청킹

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행하지만, 각 청크를 바로 콜백에 넘기는 대신, 납작하게(flatten) 이어진 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)를 반환하여 전체 결과를 스트림처럼 사용할 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

조회 중 특정 컬럼을 업데이트해야 한다면 `lazyById`를 사용하면 안전합니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

또한 `lazyByIdDesc`로 기준 컬럼의 내림차순으로 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy`와 유사하게 `cursor` 메서드를 사용하면 수 만 건을 반복할 때 메모리 점유를 크게 줄일 수 있습니다.

`cursor`는 한 번만 쿼리를 실행하지만, 실제로 반복문이 돌기 전까지 Eloquent 모델 객체가 메모리에 로드되지 않습니다. 따라서 반복문을 돌 때마다 한 번에 한 개씩만 메모리에 올라갑니다.

> [!WARNING]
> `cursor` 메서드는 메모리에 한 번에 한 모델만 보유하므로 eager loading(동시 관계 로딩)을 지원하지 않습니다. 관계 로딩이 필요하다면 [`lazy` 메서드](#chunking-using-lazy-collections)를 사용하세요.

`cursor` 메서드 내부는 PHP의 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection`을 반환합니다. [Lazy 컬렉션](/docs/{{version}}/collections#lazy-collections)에서는 일반 컬렉션의 메서드를, 한 번에 한 모델만 메모리에 올리면서도 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

단, `cursor`는 쿼리 저장소(PHP PDO driver)가 전체 결과 raw 데이터는 내부 버퍼에 보관하므로 결국은 메모리 소진의 한계가 있습니다. 정말 대량일 경우, [`lazy` 메서드](#chunking-using-lazy-collections)를 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리도 지원합니다. 이를 활용하면 관계된 테이블 정보를 하나의 쿼리로 조회할 수 있습니다. 예를 들어, `destinations`와 `flights` 두 테이블에서, 각 도착지별로 가장 최근 도착한 비행기 이름을 하나의 쿼리로 불러올 수 있습니다:

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

마찬가지로, `orderBy`에도 서브쿼리를 사용할 수 있습니다. 아래는 각 도착지에 마지막으로 도착한 비행시간에 따라 정렬하는 예시입니다:

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

특정 쿼리에 일치하는 모든 레코드를 조회하는 대신, `find`, `first`, `firstWhere` 등으로 단일 레코드를 반환할 수 있습니다. 이 메서드들은 컬렉션이 아니라 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본키로 조회
$flight = Flight::find(1);

// 조건에 맞는 첫번째 모델 조회
$flight = Flight::where('active', 1)->first();

// firstWhere는 조건식 축약형
$flight = Flight::firstWhere('active', 1);
```

결과가 없을 경우 다른 처리를 하고 싶다면, `findOr` 또는 `firstOr`에 클로저를 넘겨 결과가 없을 때 실행할 수 있습니다:

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

모델을 못 찾을 경우 예외를 던지게 하고 싶다면, `findOrFail` 또는 `firstOrFail`을 사용하세요. 이들은 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외를 잡아 처리하지 않으면 404 에러가 자동으로 반환됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate`는 지정한 조건에 해당하는 레코드를 찾고, 없다면 속성값 결합으로 새 레코드를 생성합니다.

`firstOrNew`는 조건에 맞는 레코드가 없으면 새 인스턴스만 반환하며, DB에는 아직 저장되지 않은 상태이므로 `save` 메서드로 저장해야 합니다:

```php
use App\Models\Flight;

// 이름으로 조회, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름, 지연여부, 도착 시간까지 설정해서 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름 조회, 없으면 새 인스턴스 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름, 지연, 도착 시간으로 새 인스턴스 반환
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent를 통해서도 `count`, `sum`, `max` 등의 [집계 메서드](/docs/{{version}}/queries#aggregates)를 사용할 수 있으며, 이들은 모델 인스턴스가 아닌 스칼라(단일값)를 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입과 수정

<a name="inserts"></a>
### 삽입

Eloquent로 레코드 조회만 하는 것이 아니라, 새 모델을 DB에 저장할 수도 있습니다. 새 레코드를 추가하려면 인스턴스를 생성한 뒤, 속성값을 세팅한 후 `save`를 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 Flight 저장
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

이 예시에서는 HTTP 요청에서 받은 `name`필드를 `Flight` 모델의 속성으로 할당하고, `save`를 호출하여 DB에 삽입합니다. `save` 호출 시 `created_at`, `updated_at`은 자동 설정되므로 직접 할당할 필요 없습니다.

`create` 메서드로 한 번에 새 모델을 저장하고, 생성된 인스턴스를 반환받을 수도 있습니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 사용 전에는 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 하며, 이는 대량 할당 취약점을 막기 위해서입니다. 자세한 안내는 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

기존 모델을 갱신할 때도 `save`를 사용합니다. 모델을 찾아서 원하는 속성에 값을 할당 후, `save`를 호출하면 됩니다(`updated_at` 자동 처리):

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

조건에 일치하는 모델이 있으면 수정, 없으면 새로 생성하려면 `updateOrCreate`를 사용하세요. 이 메서드는 내부적으로 저장까지 수행하므로 별도 `save` 호출이 필요 없습니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

조건에 맞는 여러 레코드를 동시에 수정하려면, 쿼리에 `update` 메서드를 사용하세요:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update`는 수정할 컬럼/값 배열을 받으며, 결과로 영향을 받은 행의 수를 반환합니다.

> [!WARNING]
> Eloquent의 대량 수정 시 `saving`, `saved`, `updating`, `updated` 등의 이벤트가 발생하지 않습니다. 이는 모델 인스턴스가 개별적으로 로딩되어 갱신되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 확인

Eloquent는 `isDirty`, `isClean`, `wasChanged` 등으로 모델 속성의 변경 상태를 확인할 수 있습니다.

`isDirty`는 모델 조회 이후 속성이 바뀌었는지 확인하며, 특정 속성명을 전달하면 해당 속성만 검사합니다. `isClean`은 변경되지 않았는지 여부를 확인합니다. 샘플:

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

`wasChanged`는 현재 요청 사이클에서 마지막 `save` 때 변경된 속성이 있는지 알려줍니다:

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

`getOriginal`은 모델이 처음 조회되었을 때의 원본 속성값(현재 바뀐 값 무시)을 배열로 반환합니다. 속성명을 넘기면 특정 속성의 원본값을 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 전체 원본 속성 배열
```

`getChanges`는 마지막 `save` 때 실제로 변경된 속성을 배열로 반환합니다:

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
```

<a name="mass-assignment"></a>
### 대량 할당(Mass Assignment)

`create` 메서드는 한 문장으로 새 모델을 생성해 저장할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만, `create`를 사용하려면 반드시 `fillable`이나 `guarded` 속성을 모델에 지정해야 합니다. 이는 Eloquent가 기본적으로 대량 할당 취약점으로부터 보호하기 때문입니다.

대량 할당 취약점은 사용자가 요청에 예기치 않은 필드를 포함시켜 중요한 DB 컬럼까지 임의로 조작할 수 있게 되는 보안상 허점입니다. 예를 들어, 악의적 사용자가 HTTP 요청에 `is_admin` 파라미터를 넘기면, 모델의 `create` 메서드에 의해 관리자 권한을 획득할 수도 있습니다.

따라서, 모델에서 대량 할당을 허용할 속성(컬럼)을 `$fillable` 속성에 명시하세요. 예시: `Flight` 모델에서 `name` 속성만 허용

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 가능한 속성들
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

허용 속성을 지정했으면 `create`로 레코드를 추가할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill`로 속성값을 한 번에 할당할 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 할당할 경우, 각 컬럼의 키를 반드시 `$fillable` 배열에 명시해야 합니다. `guarded` 사용 시에는 중첩 JSON 속성의 대량 업데이트를 지원하지 않습니다:

```php
/**
 * 대량 할당 가능 속성
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 전면 허용

모든 속성을 대량 할당 가능하게 하려면 `$guarded`를 빈 배열로 지정할 수 있습니다. 이 경우 `fill`, `create`, `update`에 넘기는 배열을 항상 신중히 직접 작성해야 합니다:

```php
/**
 * 대량 할당 불가 속성(없음)
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

디폴트로, `$fillable`에 없는 속성이 들어오면 대량 할당 연산에서 조용히 버려집니다. 운영 환경에선 이게 정상이나, 로컬 개발에선 왜 기대한 대로 속성이 반영되지 않는지 혼동을 줄 수 있습니다.

`preventSilentlyDiscardingAttributes` 메서드로 할당 불가 속성의 대량 할당 시 예외를 발생시키게 할 수도 있습니다. 이 메서드는 보통 `AppServiceProvider`의 `boot`에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 서비스 부트스트랩
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upsert(있으면 수정, 없으면 삽입)

Eloquent의 `upsert` 메서드는 한 번에 여러 레코드를 삽입 또는 갱신할 수 있습니다. 첫 번째 인자는 삽입 또는 업데이트할 값이며, 두 번째 인자에는 레코드를 유일하게 식별할 컬럼을, 세 번째 인자에는 이미 있을 경우 업데이트할 컬럼을 지정합니다. 타임스탬프가 활성화돼 있다면, `created_at`, `updated_at`도 자동 설정됩니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert`의 두 번째 인자로 지정된 컬럼이 "기본키" 또는 "유니크" 인덱스여야 합니다. MariaDB, MySQL은 두 번째 인자를 무시하고 테이블의 "기본키"와 "유니크" 인덱스를 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 기존 모델 삭제

위 예시는 모델을 먼저 조회한 뒤 삭제했지만, 기본키를 알고 있다면 바로 삭제할 수도 있습니다. `destroy` 메서드는 단일, 복수, 배열, [컬렉션](/docs/{{version}}/collections) 등 다양한 형태의 기본키를 받아 삭제할 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용 중이라면, `forceDestroy`로 영구 삭제할 수 있습니다:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy`는 각 모델을 개별 로드한 뒤 `delete`를 호출하므로 `deleting`, `deleted` 이벤트가 각각 올바르게 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

조건에 맞는 모델 여러 개를 한 번에 삭제할 수도 있습니다. 아래 예시는 비활성화된 모든 Flight를 삭제하며, 이때 모델 이벤트는 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

모든 모델 삭제는 조건 없이 쿼리를 실행하면 됩니다:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> 대량 삭제문을 실행할 때는 각 모델을 인스턴스로 로드하지 않으므로, `deleting`, `deleted` 이벤트가 발생하지 않습니다.

<a name="soft-deleting"></a>
### 소프트 삭제

실제로 DB에서 레코드를 지우지 않고, `deleted_at`만 세팅해서 "삭제된 것처럼" 동작하도록 할 수 있습니다. 이렇게 하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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
> `SoftDeletes` 트레이트는 자동으로 `deleted_at` 속성을 `DateTime` / `Carbon` 객체로 캐스팅합니다.

DB 테이블에도 `deleted_at` 컬럼이 필요하며, Laravel [스키마 빌더](/docs/{{version}}/migrations)로 쉽게 생성할 수 있습니다:

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

`delete`를 호출하면 실제 삭제 대신 `deleted_at`이 현재 시간으로 세팅·남아있고, 쿼리할 때 소프트 삭제된 모델은 자동으로 결과에 나오지 않습니다.

모델이 소프트 삭제 상태인지 확인하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

소프트 삭제된 모델을 복구하려면, 인스턴스에서 `restore`를 호출하세요. 이 메서드는 `deleted_at`을 `null`로 되돌립니다:

```php
$flight->restore();
```

여러 모델을 쿼리로 복원할 수도 있습니다(이 경우 이벤트는 발생하지 않음):

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[관계](/docs/{{version}}/eloquent-relationships) 쿼리에서도 `restore`를 사용할 수 있습니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 모델 완전 삭제

DB에서 완전 삭제하고 싶다면(즉, 실제로 삭제), `forceDelete`를 사용하세요:

```php
$flight->forceDelete();
```

관계 쿼리에서도 동일하게 사용 가능합니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델도 함께 조회

앞서 이야기했듯, 소프트 삭제 모델은 기본적으로 쿼리 결과에서 제외됩니다. 하지만 `withTrashed`를 쿼리에 추가하면 함께 조회할 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 사용 가능합니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed`는 소프트 삭제된 모델만 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

불필요해진 모델을 주기적으로 삭제하고 싶을 때, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 모델에 추가하세요. 그런 다음, `prunable` 메서드를 구현해 필요 없는 모델을 찾을 쿼리를 반환하면 됩니다:

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
     * Prunable 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable`로 지정된 모델에는 `pruning` 메서드도 구현할 수 있습니다. 이 메서드는 모델 삭제 전 호출되며, 연관 리소스(예: 파일 등)를 같이 정리할 수도 있습니다:

```php
/**
 * 가지치기 준비
 */
protected function pruning(): void
{
    // ...
}
```

이후, `routes/console.php`에서 `model:prune` Artisan 명령을 적절한 주기로 스케줄러에 등록하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령은 `app/Models` 내의 모든 Prunable 모델을 자동 감지합니다. 모델이 다른 위치에 있다면 `--model` 옵션에 클래스명을 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 제외하고 싶다면 `--except` 옵션을 사용하세요:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션으로 실제 가지치기를 실행하지 않고, 삭제될 레코드 수만 미리 확인할 수 있습니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델이 prunable 쿼리에 해당하면, 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 쓴 모델은 쿼리로 한 번에 레코드를 삭제합니다. 이 경우, `pruning` 메서드와 `deleting`, `deleted` 이벤트가 발생하지 않으므로 삭제가 훨씬 효율적입니다:

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
     * Prunable 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 복제(저장되지 않은 복사본)하려면 `replicate`를 사용합니다. 속성이 비슷한 인스턴스를 쉽게 만들 때 유용합니다:

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

복제 시 제외하고 싶은 속성이 있다면 배열로 전달하세요:

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
### 전역 스코프

전역 스코프는 특정 모델의 모든 쿼리에 제약 조건을 추가하는 기능입니다. 예를 들어, Laravel의 [소프트 삭제](#soft-deleting)는 전역 스코프를 사용해 "삭제되지 않은" 모델만 기본적으로 반환합니다. 자체 전역 스코프를 추가하면 모든 쿼리에 특정 조건을 자동 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성

전역 스코프 클래스를 생성하려면 `make:scope` Artisan 명령을 사용하세요. 생성된 스코프는 `app/Models/Scopes`에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성

스코프 작성은 간단합니다. 클래스가 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현해야 하며, `apply` 메서드를 작성합니다. 예시:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 해당 Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 전역 스코프가 쿼리의 select 절에 컬럼을 추가하려면 `select`가 아니라 `addSelect`를 사용하세요. 기존 select 절이 대체되는 문제를 막기 위함입니다.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용

모델에 전역 스코프를 적용하려면 모델에 `ScopedBy` 속성을 두면 됩니다:

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

아니면 모델의 `booted` 메서드에서 `addGlobalScope`로 수동 등록할 수도 있습니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * "booted" 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

예시의 전역 스코프를 등록하면 `User::all()` 쿼리의 결과 SQL은 다음과 같이 됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(클로저) 전역 스코프

간단한 전역 스코프는 클래스 대신 익명 함수(클로저)로도 정의할 수 있습니다. `addGlobalScope`에 첫 인자로 스코프명을 전달하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * "booted" 메서드
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
#### 전역 스코프 제거

특정 쿼리에서 전역 스코프를 해제하려면 `withoutGlobalScope`를 사용하세요. 클래스명 또는 스코프명을 넘깁니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저 스코프일 땐 등록한 문자열 스코프명을 넘깁니다:

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 전부를 해제하려면 `withoutGlobalScopes`를 사용하세요:

```php
// 모든 전역 스코프 제거
User::withoutGlobalScopes()->get();

// 일부만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 지역(Local) 스코프

지역 스코프는 자주 사용하는 특정 쿼리 조건을 메서드로 정의해 재사용할 수 있는 방법입니다. Eloquent 모델 메서드명 앞에 `scope`를 붙여 정의하세요.

스코프는 쿼리 빌더 인스턴스를 반환해야 하며, `void`도 허용됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기있는 유저만 포함하는 스코프
     */
    public function scopePopular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 유저만 포함하는 스코프
     */
    public function scopeActive(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 지역 스코프 사용

스코프를 정의하면 쿼리할 때 `scope` 접두어 없이 메서드처럼 호출할 수 있습니다. 여러 개를 체이닝도 가능합니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or`로 조합하고 싶을 땐, 클로저로 감싸 [논리 그룹핑](/docs/{{version}}/queries#logical-grouping)을 해야 합니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

좀 더 간편하게, “higher order” `orWhere`를 쓰면 클로저 없이도 가능:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

매개변수를 받는 스코프도 정의할 수 있습니다. 쿼리 객체 뒤에 차례대로 인자를 추가하면 그 값이 전달됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입의 유저만 포함하는 스코프
     */
    public function scopeOfType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

사용 예:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending 속성

스코프에서 지정한 조건과 동일한 속성값을 갖는 모델을 스코프 기반으로 생성하려면, `withAttributes` 메서드를 사용하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시 글(Draft) 스코프
     */
    public function scopeDraft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

예시:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

<a name="comparing-models"></a>
## 모델 비교

두 모델 인스턴스가 "같은" 것인지 확인하고 싶을 때는 `is`, `isNot`을 사용하세요. 두 모델의 기본키, 테이블, 연결이 모두 같을 때 `is`는 참입니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

이 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` 같은 [관계형 메서드](/docs/{{version}}/eloquent-relationships)에서도 쓸 수 있습니다. 관련 모델 인스턴스와 비교할 때 쿼리 없이 바로 비교가 가능해 편리합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 앱으로 브로드캐스트하려면 Laravel의 [모델 이벤트 브로드캐스팅](/docs/{{version}}/broadcasting#model-broadcasting)를 참고하세요.

Eloquent 모델은 다양한 순간에 이벤트를 dispatch합니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 모델이 DB에서 조회될 때
- `creating`/`created`: 새 모델이 저장될 때
- `updating`/`updated`: 기존 모델이 수정될 때
- `saving`/`saved`: 생성 또는 수정될 때 (속성이 바뀌지 않아도 발생)
- `*-ing`: 변경/저장이 DB에 반영되기 전
- `*-ed`: DB에 반영된 후

이벤트를 수신하려면, 모델에 `$dispatchesEvents` 속성을 지정해 Eloquent 모델 수명주기의 각 지점에 대한 [이벤트 클래스](/docs/{{version}}/events)를 매핑하세요. 각 이벤트 클래스는 생성자로 해당 모델 인스턴스를 전달받아야 합니다:

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
     * 모델 이벤트 맵
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트를 매핑했다면 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)를 써서 처리하면 됩니다.

> [!WARNING]
> Eloquent의 대량 수정/삭제 시에는 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다.

<a name="events-using-closures"></a>
### 클로저(익명 함수) 사용

이벤트 클래스를 쓰지 않고, 모델 이벤트 발생 시 실행할 클로저를 등록할 수도 있습니다. 보통 `booted` 메서드에서 등록합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * "booted" 메서드
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면, [큐 사용 익명 이벤트 리스너](/docs/{{version}}/events#queuable-anonymous-event-listeners)를 활용해 이벤트를 백그라운드에서 실행할 수도 있습니다:

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

특정 모델의 여러 이벤트를 수신할 땐, 옵저버 클래스로 리스너를 한 데 묶을 수 있습니다. 옵저버 클래스의 각 메서드명은 감시할 Eloquent 이벤트와 일치해야 하며, 인자로 해당 모델 인스턴스를 받습니다. Artisan 명령어로 쉽게 옵저버 클래스를 만들 수 있습니다:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령은 `app/Observers`에 새 옵저버를 만듭니다(폴더가 없으면 자동 생성). 예시:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 핸들러
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 핸들러
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 핸들러
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 핸들러
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 핸들러
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면 모델에 `ObservedBy` 속성을 추가하세요:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

아니면, `AppServiceProvider`의 `boot`에서 `observe` 메서드로 등록할 수도 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 서비스 부트스트랩
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 감시할 수 있는 이벤트로는 `saving`, `retrieved` 등도 있습니다. 자세한 것은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 트랜잭션 안에서 생성될 때는 옵저버가 이벤트 핸들러를 트랜잭션 커밋 후 실행하도록 지시할 수 있습니다. 옵저버에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 트랜잭션 중이 아니면 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 핸들러
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 뮤트(비활성화)

일시적으로 모든 모델 이벤트를 뮤트(비활성화)하고 싶을 땐, `withoutEvents` 메서드로 감싸 실행하면 됩니다. 이 클로저 내부의 코드는 이벤트 없이 실행되며, 클로저 반환값을 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델의 이벤트 없이 저장

특정 모델을 저장 등 작업할 때만 이벤트를 비활성화하고 싶다면 `saveQuietly`를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

마찬가지로 "update", "delete", "soft delete", "restore", "replicate" 등도 무음(Quietly)으로 할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
