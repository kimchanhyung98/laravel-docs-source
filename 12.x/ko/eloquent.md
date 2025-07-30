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
    - [청크 단위 결과 처리](#chunking-results)
    - [지연 컬렉션 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회하기](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트](#upserts)
- [모델 삭제하기](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 가지치기 (Pruning)](#pruning-models)
- [모델 복제하기](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [대기 속성](#pending-attributes)
- [모델 비교하기](#comparing-models)
- [이벤트](#events)
    - [클로저 사용하기](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와 상호작용을 즐겁게 만들어 주는 객체 관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블은 해당 테이블과 상호작용하는 데 사용하는 "모델"과 연결됩니다. Eloquent 모델을 통해 데이터베이스 레코드를 조회할 수 있을 뿐 아니라 삽입, 업데이트, 삭제도 할 수 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 구성에 대한 자세한 내용은 [데이터베이스 구성 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기

먼저, Eloquent 모델을 생성해 보겠습니다. 모델은 일반적으로 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다:

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 만들고 싶다면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 등 다양한 유형의 클래스도 함께 생성할 수 있습니다. 이 옵션들은 조합하여 여러 클래스를 한꺼번에 생성할 수도 있습니다:

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

# 모델과 FlightController 리소스 클래스, 폼 리퀘스트 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델과 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 단축키로 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 한 번에 생성...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인하기

모델의 코드만 보고 모든 사용할 수 있는 속성이나 연관관계를 파악하기 어려울 수 있습니다. 이때 `model:show` Artisan 명령어를 사용하면 모델의 속성과 관계를 편리하게 요약해서 보여줍니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규약

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치합니다. 간단한 모델 클래스를 살펴보고 Eloquent의 주요 규약을 설명하겠습니다:

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

위 예제를 보면 `Flight` 모델에 대응하는 데이터베이스 테이블 이름을 명시하지 않았습니다. 기본 규약에 따라 클래스 이름을 "스네이크 케이스" 복수형으로 변환한 이름이 테이블명으로 사용됩니다. 따라서 `Flight` 모델은 `flights` 테이블을 사용하고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블을 사용합니다.

규약에 맞지 않는 테이블명을 가진 모델의 경우, 모델에 `table` 속성을 정의해서 직접 테이블명을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연관된 테이블명.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 기본적으로 모델에 대응하는 테이블의 기본 키 컬럼명이 `id`라고 가정합니다. 만약 다르면 모델에 `$primaryKey` 보호 속성을 정의하여 다른 컬럼명을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블과 연관된 기본 키 컬럼명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, 기본 키는 자동 증가하는 정수형으로 가정합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용하려면, 모델에 공개 `$incrementing` 속성을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 기본 키가 자동 증가하는지 여부.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아닌 경우에는 `keyType` 보호 속성을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본 키의 데이터 타입.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent 모델은 고유한 하나의 기본 키를 가져야 합니다. 복합 기본 키는 지원하지 않습니다. 하지만 기본 키 외에 여러 컬럼으로 이루어진 고유 인덱스는 테이블에 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

자동 증가 정수 대신 UUID를 기본 키로 사용할 수 있습니다. UUID는 36자 길이의 유니버설 고유 식별자입니다.

모델이 UUID 키를 사용하도록 하려면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 이 때 해당 모델에는 UUID와 매칭되는 기본 키 컬럼이 존재해야 합니다:

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

기본적으로 `HasUuids` 트레이트는 [순서가 있는(ordered) UUIDs](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 순서가 있는 UUID는 사전식 정렬이 가능해 데이터베이스 인덱스 저장에 효과적입니다.

UUID 생성 방식을 커스텀하려면 모델에 `newUniqueId` 메서드를 정의할 수 있고, UUID를 발급할 컬럼을 지정하려면 `uniqueIds` 메서드를 정의할 수도 있습니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델의 새 UUID 생성.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID가 적용될 컬럼 목록 반환.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

ULID를 UUID 대신 사용할 수도 있습니다. ULID는 26자 길이로, UUID와 비슷하지만 더 짧고 역시 사전식 정렬이 가능합니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 적용하고, ULID에 매칭되는 기본 키 컬럼이 있어야 합니다:

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

기본적으로 Eloquent는 모델에 대응하는 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 기대합니다. 모델 생성 또는 업데이트 시 자동으로 이 컬럼들이 세팅됩니다. 자동 관리하지 않으려면 모델에 `$timestamps` 속성을 `false`로 설정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 타임스탬프 자동 관리 여부.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프 형식을 바꾸려면 `$dateFormat` 속성을 설정합니다. 이 속성은 데이터베이스에 저장하는 형식과 배열 혹은 JSON 직렬화 시 포맷을 결정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 날짜 컬럼 저장 형식.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼 이름을 바꾸려면 모델 안 `CREATED_AT`과 `UPDATED_AT` 상수를 정의할 수 있습니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프 갱신 없이 작업하려면 `withoutTimestamps` 메서드에 클로저를 전달해 작업할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

모든 Eloquent 모델은 기본적으로 애플리케이션에서 설정한 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 다른 연결을 사용하려면 `$connection` 속성에 연결명을 설정하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 사용할 데이터베이스 연결명.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

새로 인스턴스화되는 모델은 기본적으로 아무 속성 값도 갖고 있지 않습니다. 일부 속성의 기본값을 지정하려면 `$attributes` 보호 속성을 설정할 수 있습니다. 속성 값은 데이터베이스에서 읽은 것처럼 그대로 저장 가능한 원시 형태여야 합니다:

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
### Eloquent 엄격성 설정

Laravel은 다양한 상황에서 Eloquent의 동작과 "엄격성"을 조절할 수 있는 방법을 제공합니다.

`preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 방지할지 여부를 불리언 인수로 받습니다. 예를 들어, 프로덕션 환경에서는 지연 로딩 사용을 허용하고, 개발 환경에서만 방지하도록 할 수 있습니다. 보통 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

`preventSilentlyDiscardingAttributes` 메서드를 호출하면, 채우기 불가능한 속성을 암묵적으로 무시하는 대신 예외를 던지게 할 수 있습니다. 이 방식은 로컬 개발 시 'fillable' 배열에 추가하지 않은 속성 설정 시 오류 발견에 도움됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 생성했다면 데이터 조회를 시작할 준비가 된 것입니다. 각 Eloquent 모델은 데이터베이스 쿼리를 유창하게 작성할 수 있는 강력한 [쿼리 빌더](/docs/12.x/queries)로 생각할 수 있습니다. `all` 메서드는 관련 테이블에서 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

`all` 메서드는 모든 결과를 반환하나, Eloquent 모델들은 [쿼리 빌더 메서드](/docs/12.x/queries)를 활용할 수 있으므로 추가 조건을 붙이고 `get` 메서드로 결과를 가져올 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel 쿼리 빌더의 모든 메서드를 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회한 모델 인스턴스가 있다면, `fresh` 또는 `refresh` 메서드로 모델을 새로고침할 수 있습니다. `fresh` 메서드는 DB에서 모델을 다시 조회하며 기존 모델에 영향은 미치지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 최신 데이터로 다시 채우며, 로드된 모든 관계도 새로고침합니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`과 `get` 메서드는 여러 레코드를 조회하지만, 순수 PHP 배열 대신 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장하며, 데이터 컬렉션을 다루는 유용한 [다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 클로저 결과에 따라 컬렉션에서 모델을 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션은 Laravel 기본 컬렉션과 별개로 [모델 컬렉션 전용 추가 메서드](/docs/12.x/eloquent-collections#available-methods)도 제공합니다.

Laravel 컬렉션은 PHP의 iterable 인터페이스를 구현하므로, 배열처럼 foreach로 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크 단위 결과 처리

`tens of thousands` 단위의 대량 데이터는 `all`이나 `get` 메서드로 한꺼번에 로드하면 메모리가 부족해질 수 있습니다. 이때 `chunk` 메서드를 사용하면 모델을 분할해서 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 일정 크기 청크 단위로 모델을 가져와 클로저에 넘깁니다. 한 번에 청크만 메모리에 존재하므로 대용량 데이터 작업 시 메모리 사용량이 크게 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 청크 당 가져올 레코드 수이며, 두 번째 인수 클로저는 각 청크를 처리하는 콜백입니다. 각 청크마다 DB 쿼리가 실행되어 데이터를 가져옵니다.

쿼리에서 결과를 필터링하며 반복 중에 해당 컬럼 값을 업데이트할 경우 `chunkById` 메서드를 사용해야 예기치 못한 문제를 방지할 수 있습니다. 내부적으로 `chunkById`는 이전 청크에서 가장 큰 `id`보다 큰 레코드를 가져옵니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById`는 쿼리에 자동으로 "where" 조건을 추가하므로, 자신의 조건을 [논리 그룹화](/docs/12.x/queries#logical-grouping)하려면 클로저로 묶는 것이 좋습니다:

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
### 지연 컬렉션 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 뒤에서 청크 단위로 쿼리하지만, 클로저 인자로 각 청크를 전달하는 대신 평탄화된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여 데이터를 스트림처럼 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 메서드 결과를 필터링하며 반복 중 업데이트할 경우 `lazyById` 메서드를 사용하세요. 내부적으로 `lazyById`는 이전 청크의 마지막 `id`보다 큰 모델을 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드로는 `id` 내림차순으로 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy`와 비슷하게, `cursor` 메서드도 메모리 사용량을 상당히 줄일 수 있는 방법입니다. `cursor` 메서드는 한번의 쿼리를 실행하지만, 각 모델은 실제로 반복할 때마다 개별적으로 로드됩니다. 따라서 반복 시 항상 메모리에 한 개 모델만 존재합니다.

> [!WARNING]
> `cursor`는 메모리에 항상 한 모델만 유지하므로 관계를 즉시 로드할 수 없습니다. 관계를 eager 로드해야 하면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

내부적으로 `cursor` 메서드는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)을 이용하면 일반 컬렉션 메서드 상당수를 적은 메모리로 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 적은 메모리를 쓰지만, PHP의 PDO 드라이버가 원시 쿼리 결과를 내부 버퍼에 캐시하기 때문에 결국 메모리 부족이 발생할 수 있습니다. 매우 큰 레코드 집합을 다룰 경우 [lazy 메서드](#chunking-using-lazy-collections)를 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리 지원을 제공합니다. 이를 통해 연관 테이블의 정보를 한 번 쿼리로 가져올 수 있습니다. 예를 들어, `destinations` 테이블과 `flights` 테이블이 있고, `flights`에 비행 도착 시각 `arrived_at` 컬럼이 있다고 가정합니다.

쿼리 빌더의 `select` 및 `addSelect` 메서드에 서브쿼리를 전달하면, 각 도착지별로 가장 최근에 도착한 비행기의 이름을 단일 쿼리로 조회할 수 있습니다:

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

쿼리 빌더의 `orderBy` 메서드도 서브쿼리를 지원합니다. 위 예제에서, 각 도착지별로 마지막 비행기 도착 시각을 기준으로 내림차순 정렬할 수도 있습니다. 한 쿼리로 처리합니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 조회하기

조건에 맞는 여러 레코드 조회 외에도 `find`, `first`, `firstWhere` 메서드로 단일 모델을 조회할 수 있습니다. 이들은 컬렉션 대신 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 조회...
$flight = Flight::find(1);

// 쿼리 제약 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건에 맞는 첫 번째 모델 조회 대체 방법...
$flight = Flight::firstWhere('active', 1);
```

조건에 맞는 결과가 없을 때 다른 작업을 수행하려면 `findOr`와 `firstOr` 메서드를 사용하세요. 결과가 없을 시 인자로 전달한 클로저를 실행하며, 클로저의 반환값이 메서드의 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 모델 미발견 시 예외

컨트롤러나 라우트에서는 모델 미발견 시 예외를 던지는 경우가 많습니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리 첫 결과를 반환하되, 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외가 처리되지 않으면 Laravel은 자동으로 클라이언트에 404 HTTP 응답을 전송합니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍으로 DB 레코드를 찾고, 없으면 첫 번째 인자와 두 번째 인자를 병합한 속성으로 새로운 레코드를 생성합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 비슷하지만, 모델이 없으면 DB에 저장하지 않고 새 모델 인스턴스만 반환합니다. 수동으로 `save` 해야 DB에 반영됩니다:

```php
use App\Models\Flight;

// 이름으로 조회, 없으면 새로 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지정 속성으로 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 인스턴스 반환...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지정 속성으로 인스턴스 생성...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델에서 Laravel [쿼리 빌더 집계 메서드](/docs/12.x/queries#aggregates)인 `count`, `sum`, `max` 등을 사용할 수 있습니다. 이 메서드는 Eloquent 모델이 아니라 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때, 모델 조회뿐만 아니라 삽입 작업도 빈번합니다. 새 데이터 삽입은 새 모델 인스턴스를 생성하고 속성을 설정한 뒤 `save` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 데이터베이스에 새로운 비행 정보 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        // 요청 검증...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

위 예제에서, HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당했습니다. `save` 메서드 호출 시 레코드가 DB에 삽입되며, 이 과정에서 `created_at`과 `updated_at` 타임스탬프도 자동으로 설정됩니다.

대안으로, `create` 메서드를 사용하면 한 문장으로 새 모델을 저장할 수 있습니다. `create`는 삽입된 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create`를 사용하기 전 모델에 반드시 `fillable` 또는 `guarded` 속성을 정의해야 합니다. 왜냐하면 Eloquent 모델은 기본적으로 대량 할당 공격을 방지하기 때문입니다. 대량 할당에 관한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

`save` 메서드는 이미 존재하는 모델을 업데이트할 때도 사용할 수 있습니다. 기존 모델을 조회하고 속성을 바꾼 뒤 `save`를 호출하면, `updated_at` 타임스탬프가 자동 갱신되어 저장됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

조건에 맞는 모델이 있으면 업데이트하고, 없으면 새로 생성하는 작업도 가능합니다. `firstOrCreate`와 비슷하게 `updateOrCreate`는 모델을 즉시 데이터베이스에 저장합니다.

아래 예제는 `Oakland` 출발지와 `San Diego` 목적지를 갖는 항공편이 있으면 가격(`price`)과 할인여부(`discounted`)를 업데이트하고, 없으면 새로운 레코드를 삽입합니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

특정 조건에 맞는 모델로 일괄 업데이트도 가능합니다. 다음 예제는 활동 중이고 목적지가 `San Diego`인 모든 항공편을 지연 상태로 표시합니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update`는 컬럼과 값 쌍을 담은 배열을 받고, 영향을 받은 행 수를 반환합니다.

> [!WARNING]
> Eloquent를 통한 대량 업데이트 시 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 이는 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 확인하기

Eloquent는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공해 모델 속성 변경 상태를 확인할 수 있습니다.

- `isDirty`는 모델 조회 이후 변경된 속성이 있는지 판단합니다. 속성명이나 속성 배열을 인자로 받아 특정 속성의 변경 여부를 확인할 수 있습니다.
- `isClean`은 변경되지 않은 속성을 확인. 인자도 받을 수 있습니다.
- `wasChanged`는 현재 요청 사이클에서 마지막 저장 시점에 변경된 속성을 확인하며 특정 속성도 지정 가능.

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty();         // true
$user->isDirty('title');  // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean();         // false
$user->isClean('title');  // false
$user->isClean('first_name'); // true

$user->save();

$user->isDirty();         // false
$user->isClean();         // true
```

또한 `getOriginal` 메서드는 모델이 처음 조회됐을 때의 원래 속성 값을 반환합니다. 특정 속성만 인자로 전달하면 해당 속성의 원래 값을 가져옵니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원래 속성 배열 반환
```

`getChanges`는 마지막 저장 시 변경된 속성 배열을 반환하고, `getPrevious`는 마지막 저장하기 전 원래 값 배열을 반환합니다:

```php
$user = User::find(1);

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
### 대량 할당

`create` 메서드는 단일 PHP 문장으로 새 모델을 저장할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 대량 할당을 사용하려면 모델에 반드시 `fillable` 또는 `guarded` 속성을 정의해야 합니다. Eloquent는 기본적으로 대량 할당 공격을 방지합니다.

대량 할당 공격은 사용자가 의도하지 않은 HTTP 요청 필드를 전달해 DB의 예상치 못한 컬럼이 변경되는 취약점입니다. 예를 들어, 악의로 `is_admin` 파라미터를 보내어 관리자 권한을 얻을 수 있습니다.

따라서 시작하려면, 모델에 대량 할당이 허용된 속성을 `$fillable` 속성으로 정의해야 합니다. 예시는 `name` 속성만 대량 할당 가능하도록 정의한 모습입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 허용 속성 목록.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

이후 `create` 메서드로 새 레코드를 삽입할 수 있으며, 생성된 모델 인스턴스를 반환받습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면 `fill` 메서드로 속성 집합을 채울 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼에 값을 할당할 때는 각각의 JSON 키가 `$fillable` 배열에 명시되어야 합니다. 보안을 위해 Laravel은 `guarded` 속성 사용 시 중첩 JSON 업데이트를 지원하지 않습니다:

```php
/**
 * 대량 할당 허용 속성 목록.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용하기

모든 속성을 대량 할당 가능하게 하려면 모델의 `$guarded` 속성을 빈 배열로 정의할 수 있습니다. 이 경우, 언제나 `fill`, `create`, `update` 메서드에 전달하는 배열 값을 직접 주의 깊게 관리해야 합니다:

```php
/**
 * 대량 할당 금지 속성 목록.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 없는 속성은 대량 할당 시 암묵적으로 무시됩니다. 로컬 개발 시에는 변경이 안 되는 원인을 파악하기 어려울 수 있습니다.

원하지 않는 속성 할당 시 예외를 발생시키려면 `preventSilentlyDiscardingAttributes` 메서드를 호출합니다. 보통 `AppServiceProvider`의 `boot` 메서드에 넣어 사용합니다:

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
### 업서트

Eloquent의 `upsert` 메서드를 사용하면 조건에 따라 레코드를 한번에 업데이트하거나 생성할 수 있습니다. 첫 번째 인자는 삽입 또는 업데이트할 값 배열이고, 두 번째 인자는 고유 레코드를 식별할 컬럼(들), 세 번째 인자는 업데이트할 컬럼 배열입니다. 모델에 타임스탬프가 설정되어 있으면 `created_at`과 `updated_at`도 자동 갱신됩니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 두 번째 인자의 컬럼들이 "primary" 또는 "unique" 인덱스여야 합니다. MariaDB와 MySQL은 두 번째 인자를 무시하고 테이블의 "primary" 및 "unique" 인덱스만 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제하기

모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출합니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제하기

위와 같이 데이터베이스에서 모델을 조회한 후 삭제하였지만, 기본 키를 알고 있다면 명시적 조회 없이 `destroy` 메서드를 호출해 삭제할 수 있습니다. 매개변수로 단일 기본 키, 다수 기본 키, 기본 키 배열, 또는 기본 키 컬렉션을 전달할 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

소프트 삭제 모델을 영구 삭제하려면 `forceDestroy` 메서드를 사용합니다:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별 조회 후 `delete`를 호출하며, 모델의 `deleting`과 `deleted` 이벤트가 올바르게 발생하도록 합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제하기

쿼리 기반으로 조건에 맞는 여러 모델을 삭제할 수도 있습니다. 예를 들어 `active`가 아닌 모든 항공편을 삭제할 수 있습니다. 대량 삭제도 이벤트를 발생시키지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 모델을 삭제하려면 조건 없이 쿼리를 실행하세요:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> 대량 삭제 시 `deleting`과 `deleted` 이벤트가 발생하지 않습니다. 삭제할 모델을 실제로 조회하지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 실제로 데이터베이스에서 레코드를 제거하는 대신 소프트 삭제도 지원합니다. 소프트 삭제 시 `deleted_at` 속성에 삭제 일시가 기록되며, 실제 레코드는 남아 있습니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime`/`Carbon` 인스턴스로 캐스팅합니다.

`deleted_at` 컬럼도 테이블에 추가해야 하며, Laravel [스키마 빌더](/docs/12.x/migrations)에 헬퍼가 있습니다:

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

이제 모델의 `delete`를 호출하면 `deleted_at`에 현재 시간이 설정되고, DB 레코드는 테이블에 그대로 남습니다. 소프트 삭제를 사용하는 모델은 기본 쿼리에서 소프트 삭제된 레코드를 제외합니다.

모델 인스턴스가 소프트 삭제 상태인지 확인하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원하기

소프트 삭제된 모델을 "복원"하려면 인스턴스에서 `restore` 메서드를 호출하세요. `deleted_at`이 `null`로 설정됩니다:

```php
$flight->restore();
```

쿼리에서도 `restore` 메서드를 사용해 여러 모델을 복원할 수 있습니다. 대량 복원은 이벤트를 발생시키지 않습니다:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

관계 쿼리에서도 `restore`가 가능합니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제하기

데이터베이스에서 모델을 완전히 삭제하려면 `forceDelete` 메서드를 호출하세요:

```php
$flight->forceDelete();
```

관계 쿼리에서도 가능합니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함하기

앞서 설명했듯, 소프트 삭제된 모델은 기본 쿼리 결과에서 제외됩니다. 하지만 `withTrashed` 메서드를 호출하면 쿼리에 소프트 삭제 모델 포함시킬 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 `withTrashed` 사용할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드는 **소프트 삭제된 모델만** 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기 (Pruning)

더 이상 필요 없는 모델을 주기적으로 삭제하려면, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 모델에 추가하세요. 이후 `prunable` 메서드를 구현하여 삭제 대상 모델을 찾아 리턴하는 Eloquent 쿼리 빌더를 반환합니다:

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
     * 가지치기 대상 모델 쿼리 생성.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable`을 적용한 모델에 `pruning` 메서드를 정의하면 삭제 직전 호출됩니다. 모델 삭제 전에 저장 파일 등 부가 자원을 정리할 때 유용합니다:

```php
/**
 * 가지치기 준비 작업.
 */
protected function pruning(): void
{
    // ...
}
```

모델을 구성했다면, Artisan `model:prune` 명령어를 `routes/console.php` 파일에서 스케줄해 주기적으로 실행하도록 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

내부적으로 `model:prune` 명령어는 `app/Models` 폴더에 있는 `Prunable` 모델을 자동 인식합니다. 모델 위치가 다르면 `--model` 옵션으로 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 가지치기에서 제외하려면 `--except` 옵션을 사용하세요:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션과 함께 `model:prune` 명령어를 실행하면 실제로는 삭제하지 않고 몇 개가 삭제될지 출력합니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델도 `prunable` 쿼리에 따라 삭제 시 `forceDelete`되어 영구 삭제됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기 (Mass Pruning)

`MassPrunable` 트레이트를 사용한 모델은 대량 삭제 쿼리로 모델을 삭제합니다. 따라서 `pruning` 메서드와 `deleting`, `deleted` 이벤트가 호출되지 않습니다. 실제 모델을 로드하지 않아 처리 효율이 매우 높습니다:

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
     * 가지치기 대상 모델 쿼리 생성.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제하기

기존 모델을 복제한 후 저장하지 않은 새 복사본을 만들려면 `replicate` 메서드를 사용하세요. 속성이 많이 겹치는 모델 생성 시 편리합니다:

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

새 모델에 복제하지 않을 속성을 배열로 전달할 수도 있습니다:

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

글로벌 스코프는 특정 모델의 모든 쿼리에 제약 조건을 추가하는 방법입니다. Laravel 소프트 삭제 기능도 글로벌 스코프를 사용해 삭제한 모델을 자동 제외합니다. 글로벌 스코프를 직접 작성하면 특정 제약 조건을 모든 쿼리에 편리하게 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

새 글로벌 스코프를 생성하려면 `make:scope` Artisan 명령어를 사용하세요. 생성된 스코프는 `app/Models/Scopes` 디렉토리에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성하기

글로벌 스코프 작성을 위해 `make:scope` 명령어로 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 만듭니다. 이 인터페이스는 `apply` 메서드를 요구하며, 쿼리 빌더에 `where` 같은 조건을 추가할 수 있습니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Eloquent 쿼리 빌더에 스코프 적용.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 쿼리의 선택절에 컬럼을 추가할 때는 기존 선택절을 덮어쓰지 않도록 `select` 대신 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용하기

글로벌 스코프를 모델에 적용하려면 `ScopedBy` 속성을 모델에 지정하세요:

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

또는 모델의 `booted` 메서드를 오버라이드해 `addGlobalScope` 메서드를 호출해 추가할 수도 있습니다:

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

이렇게 추가한 후 `User::all()` 호출 시 다음과 같은 SQL이 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

간단한 글로벌 스코프는 클래스를 만들지 않고 클로저를 사용할 수도 있습니다. 이때 `addGlobalScope` 메서드 첫 번째 인자로 스코프 이름을 지정해야 합니다:

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
#### 글로벌 스코프 제거하기

쿼리에서 글로벌 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용하세요. 구현체가 클래스명이라면 클래스명, 클로저 스코프면 이름을 인자로 전달합니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 글로벌 스코프 또는 모든 글로벌 스코프를 제거하려면 `withoutGlobalScopes` 메서드를 사용합니다:

```php
// 모든 글로벌 스코프 제거...
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프 제거...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 쿼리 조건의 공통 집합을 정의해 애플리케이션 내 여러 곳에서 재사용할 수 있게 해줍니다. 스코프 메서드에는 `Scope` 속성을 붙입니다.

스코프 메서드는 변경된 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 투표수가 100 이상인 인기 사용자를 제한하는 스코프.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 제한하는 스코프.
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

정의한 스코프 메서드는 모델 쿼리 시 호출해 사용할 수 있으며, 여러 스코프를 체이닝할 수 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조건으로 여러 스코프를 결합할 때는 [논리적 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 Laravel은 클로저 없이도 스코프 체인을 부드럽게 이어주는 하이어 오더 `orWhere` 메서드를 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 매개변수가 필요할 경우, `$query` 매개변수 다음에 추가로 입력받으면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입의 사용자만 제한하는 스코프.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

이후 쿼리 시 인자를 전달해 호출합니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 속성

스코프를 통해 제한 조건뿐 아니라, 해당 조건에 맞는 속성을 가진 새 모델을 생성할 때 같은 속성을 자동으로 가지도록 할 수도 있습니다. `withAttributes` 메서드를 쿼리빌더에 사용하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 초안 상태만 제한하는 스코프.
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

`withAttributes`는 전달된 속성으로 `where` 조건을 추가할 뿐 아니라, 생성된 모델에도 해당 속성을 포함시킵니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes`가 조건을 추가하지 않게 하려면 `asConditions` 인자를 `false`로 설정하세요:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

두 모델이 동일한지 확인해야 할 경우 `is`와 `isNot` 메서드를 사용할 수 있습니다. 이들은 기본 키, 테이블, DB 연결이 모두 같은지 비교합니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](/docs/12.x/eloquent-relationships)에서도 이 메서드를 활용해 관련된 모델을 쿼리 없이 비교할 수 있습니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트에 바로 브로드캐스트하려면 Laravel [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 다음과 같은 라이프사이클 이벤트를 발생시켜 훅을 걸 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 기존 모델을 데이터베이스에서 조회할 때 발생
- `creating`과 `created`: 새 모델을 처음 저장 할 때 발생
- `updating`과 `updated`: 기존 모델이 수정돼 `save` 호출하면 발생
- `saving`과 `saved`: 새 모델 생성 또는 업데이트 시 발생, 속성 변경과 무관
- `-ing`형 이벤트는 변경 사항이 저장되기 전 발생
- `-ed`형 이벤트는 변경 사항이 저장 후 발생

모델 이벤트를 듣기 위해서는 모델에 `$dispatchesEvents` 속성을 정의하고, Eloquent 이벤트명과 사용자 이벤트 클래스를 매핑하세요. 이벤트 클래스는 생성자에서 영향 받는 모델 인스턴스를 받도록 만들어야 합니다:

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
     * 모델 이벤트 매핑.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이후 [이벤트 리스너](/docs/12.x/events#defining-listeners)로 이벤트를 처리합니다.

> [!WARNING]
> 대량 업데이트 또는 삭제 시, 모델 이벤트(`saved`, `updated`, `deleting`, `deleted`)는 발생하지 않습니다. 모델이 실제로 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용하기

사용자 이벤트 클래스를 만들지 않고, 모델 이벤트 발생 시 수행할 클로저를 등록할 수 있습니다. 보통 모델의 `booted` 메서드에 등록합니다:

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

필요하다면 [큐블 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 사용해 모델 이벤트를 백그라운드 큐 작업으로 실행할 수도 있습니다:

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

특정 모델에 다수 이벤트를 듣는 경우, 옵저버 클래스로 관련 리스너를 한 곳에 모을 수 있습니다. 옵저버 클래스 메서드명은 이벤트명과 일치하며, 각 메서드는 영향 받는 모델을 인자로 받습니다. `make:observer` Artisan 명령어로 옵저버를 쉽게 만들 수 있습니다:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어는 `app/Observers` 디렉토리에 옵저버 클래스를 생성합니다. 해당 디렉토리가 없으면 Artisan이 만듭니다. 기본 옵저버 예시는 다음과 같습니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User 모델 "created" 이벤트 처리.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User 모델 "updated" 이벤트 처리.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User 모델 "deleted" 이벤트 처리.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User 모델 "restored" 이벤트 처리.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User 모델 "forceDeleted" 이벤트 처리.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버 등록은 모델에 `ObservedBy` 속성을 부여하거나, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `observe` 메서드를 호출해 수동 등록할 수 있습니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

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
> 옵저버가 들을 수 있는 이벤트는 `saving`이나 `retrieved` 등 추가로 더 있습니다. 더 자세한 내용은 [이벤트](#events) 문서를 참조하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 모델을 생성하는 경우, 옵저버가 트랜잭션 커밋 후에만 이벤트 핸들러를 실행하도록 설정할 수 있습니다. 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하세요. 트랜잭션이 없으면 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User 모델 "created" 이벤트 처리.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거

때때로 모델 이벤트를 일시적으로 "음소거"할 필요가 있습니다. `withoutEvents` 메서드는 클로저를 인자로 받아, 클로저 내에서 실행되는 모델 이벤트 발생을 막고 클로저 반환값을 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장하기

특정 모델 저장 시 이벤트를 발생시키고 싶지 않다면 `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

다음과 같이 업데이트, 삭제, 소프트 삭제, 복원, 복제에도 이벤트 없이 수행할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```