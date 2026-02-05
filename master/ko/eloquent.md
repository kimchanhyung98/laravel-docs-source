# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent strictness 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청킹(Chunking)](#chunking-results)
    - [지연 컬렉션을 활용한 청킹](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계값 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 저장 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 가지치기](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending Attributes](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저를 사용한 이벤트](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거(Muting)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와의 상호작용을 쉽고 재미있게 만들어 주는 객체 관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때 데이터베이스의 각 테이블은 해당 테이블과 연관된 "모델(Model)"이 하나씩 존재합니다. Eloquent 모델을 사용하면 테이블에서 데이터를 조회하는 것은 물론, 레코드를 삽입(insert), 수정(update), 삭제(delete)하는 작업도 매우 간단하게 처리할 수 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 연결에 관한 더 자세한 내용은 [데이터베이스 설정 문서](/docs/master/database#configuration)를 참고하십시오.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해보겠습니다. 일반적으로 모델은 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속받습니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/master/artisan)를 사용합니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/master/migrations)도 함께 만들고 싶다면, `--migration` 또는 `-m` 옵션을 추가할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 타입의 클래스를 함께 생성할 수 있습니다. 이러한 옵션들을 조합하여 여러 클래스를 한 번에 동시에 생성하는 것도 가능합니다.

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

# 모델과 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청을 모두 생성하는 단축키...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 관계 확인

모델의 코드만 훑어봐서는 해당 모델의 모든 속성과 연관관계를 파악하기 어려울 때가 있습니다. 이럴 때 `model:show` Artisan 명령어를 사용하면, 모델의 속성과 관계에 대한 간편한 개요를 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 아래는 기본 모델 클래스 예시이며, Eloquent의 핵심 관례 몇 가지에 대해 살펴보겠습니다.

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

위 예시에서 모델과 매칭되는 데이터베이스 테이블 이름을 별도로 지정하지 않았습니다. Eloquent는 관례적으로 클래스명에 '스네이크 케이스(snake_case)'와 복수형을 적용해 테이블명을 결정합니다. 즉, `Flight` 모델의 경우 `flights` 테이블에 저장된다고 간주하며, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 저장됩니다.

만약 모델이 사용하는 데이터베이스 테이블명이 이러한 관례와 다르다면, 모델의 `table` 속성을 명시적으로 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 연결된 테이블
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델이 매칭되는 테이블에 `id`라는 이름의 기본 키 컬럼이 존재한다고 가정합니다. 필요 시, 모델의 `$primaryKey` 속성을 지정하여 기본 키로 사용할 컬럼 이름을 변경할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블과 연결된 기본 키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

Eloquent는 기본 키가 증가하는 정수 값이라고 가정하고, 자동으로 정수형으로 값을 변환합니다. 만약 증가하지 않거나 숫자가 아닌 기본 키를 쓰고 싶다면, 모델의 `$incrementing` 속성을 `false`로 지정해야 합니다.

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

기본 키가 정수가 아닐 경우, 모델의 `$keyType` 속성을 `string`으로 지정해야 합니다.

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

Eloquent는 각 모델에 하나의 고유한 "ID"가 필요하므로, 복합(2개 이상의 컬럼으로 구성된) 기본 키를 지원하지 않습니다. 대신, 데이터베이스 테이블에 별도의 다중 컬럼 유니크 인덱스를 추가하여 사용할 수 있습니다. 단, Eloquent에서 해당 인덱스를 기본 키로 취급할 수는 없습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

기본 증가형 정수 대신, UUID를 모델의 기본 키로 사용할 수 있습니다. UUID는 36자의 고유 알파-숫자 식별자입니다.

모델에서 UUID를 기본 키로 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가하면 됩니다. 이때 모델의 기본 키 컬럼도 [UUID와 호환되도록](/docs/master/migrations#column-method-uuid) 만들어야 합니다.

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

기본적으로 `HasUuids` 트레이트는 ["ordered" UUID](/docs/master/strings#method-str-ordered-uuid)를 생성합니다. 이 UUID는 색인이 붙은 데이터베이스 저장에 더 효율적이며, 사전순 정렬이 가능합니다.

개별 모델의 UUID 생성 방식을 변경하려면, 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한, UUID가 부여될 컬럼을 지정하려면 `uniqueIds` 메서드를 정의할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델에 대한 새로운 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자가 지정되어야 할 컬럼 목록 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 비슷하지만 길이가 26자이며, ordered UUID와 같이 사전순 정렬이 가능하여 인덱싱 효율이 높습니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 추가하고, [ULID와 호환되는 기본 키 컬럼](/docs/master/migrations#column-method-ulid)을 만들어야 합니다.

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

Eloquent는 기본적으로 모델의 데이터베이스 테이블에 `created_at`, `updated_at` 컬럼이 존재한다고 가정합니다. 모델이 생성되거나 수정될 때 이 컬럼들의 값이 자동으로 설정됩니다. Eloquent가 해당 컬럼을 자동으로 관리하지 않게 하려면, 모델의 `$timestamps` 속성을 `false`로 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 타임스탬프 자동 관리 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델의 타임스탬프 포맷을 사용자 정의하려면, `$dateFormat` 속성을 지정하면 됩니다. 이 속성은 데이터베이스에 저장되는 날짜 속성의 포맷과, 배열 또는 JSON으로 변환될 때의 포맷을 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 컬럼 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼의 이름을 변경하려면 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 각각 정의할 수 있습니다.

```php
<?php

class Flight extends Model
{
    /**
     * "created at" 컬럼명
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * "updated at" 컬럼명
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프를 수정하지 않고 조작하고 싶을 때, `withoutTimestamps` 메서드 내에서 클로저로 감싸 조작할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 별도의 데이터베이스 연결을 사용하고 싶다면 모델에 `$connection` 속성을 명시하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 데이터베이스 연결
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

새롭게 인스턴스화된 모델은 기본적으로 어떠한 속성 값도 가지지 않습니다. 모델의 특정 속성에 대해 기본값을 부여하고 싶다면 `$attributes` 속성을 정의하면 됩니다. 이 속성에 지정하는 값들은 데이터베이스로부터 읽어온 그대로의 "저장 가능한"(raw, storable) 포맷이어야 합니다.

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
### Eloquent strictness 설정

Laravel은 다양한 상황에서 Eloquent의 동작과 "strictness"(엄격성)를 다양하게 설정할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩(lazy loading) 방지 여부를 나타내는 선택적 불리언 인수를 받습니다. 예를 들어, 프로덕션 환경에서는 우발적인 lazy loading이 발생해도 서비스가 정상 동작하게 하면서, 개발 환경에서는 엄격하게 막고 싶을 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

또한 `preventSilentlyDiscardingAttributes` 메서드를 사용하면, 모델의 `fillable` 배열에 포함되지 않은 속성 할당 시 예외를 던지게 할 수 있습니다. 이 기능은 로컬 개발 중 의도하지 않은 속성 수정 문제를 디버깅할 때 유용합니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/master/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 조회할 준비가 되었습니다. 각 Eloquent 모델은 훌륭한 [쿼리 빌더](/docs/master/queries)이기도 하여, 모델을 통해 연관된 테이블을 간편하게 질의할 수 있습니다. 모델의 `all` 메서드는 모델과 연관된 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌더 사용하기

Eloquent의 `all` 메서드는 테이블의 모든 결과를 반환합니다. 하지만 Eloquent 모델은 [쿼리 빌더](/docs/master/queries)이므로, 추가적인 조건을 자유롭게 추가하고 `get`을 호출해 결과를 조회할 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델이 곧 쿼리 빌더이므로, Laravel [쿼리 빌더](/docs/master/queries)에서 제공하는 모든 메서드를 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh` 및 `refresh` 메서드를 사용해 모델을 새로고침할 수 있습니다. `fresh`는 데이터베이스에서 모델을 다시 조회하며 기존 인스턴스에는 영향을 주지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델의 데이터를 데이터베이스에서 다시 가져와 기존 인스턴스를 갱신합니다. 이때 모든 로드된 연관관계도 함께 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all` 및 `get` 등 Eloquent 메서드들은 여러 레코드를 조회합니다. 하지만 반환값은 일반 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스입니다.

Eloquent의 Collection 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 상속하며, [다양한 컬렉션 관련 메서드](/docs/master/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 사용하면 컬렉션에서 특정 모델들을 쉽게 필터링할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 클래스는 [Eloquent 모델 컬렉션을 위한 몇 가지 추가 메서드](/docs/master/eloquent-collections#available-methods)도 제공합니다.

모든 Laravel 컬렉션은 PHP의 반복(iterable) 인터페이스를 구현하므로 배열처럼 반복문(`foreach`)으로 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청킹(Chunking)

`all`이나 `get` 메서드를 통해 수만 개의 레코드를 한 번에 불러오면 메모리가 부족해질 수 있습니다. 이런 경우에는 `chunk` 메서드를 사용해 효율적으로 대량의 모델을 처리할 수 있습니다.

`chunk` 메서드는 지정된 개수 만큼의 Eloquent 모델을 서브셋으로 나눠서 클로저로 전달합니다. 한 번에 청크 단위로만 데이터를 메모리에 올리므로, 많은 모델을 다루면서도 메모리 사용량을 효과적으로 줄일 수 있습니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 번에 가져올 레코드 수이며, 두 번째로 전달하는 클로저는 각 청크마다 호출됩니다. 매번 새로 데이터베이스 쿼리가 실행되어 각 청크의 레코드가 클로저로 넘어갑니다.

만약 결과를 필터링하면서 반복 중에 특정 컬럼(예: `id`)의 값을 업데이트해야 한다면, `chunk` 대신 `chunkById` 메서드를 사용해야 예기치 않은 결과를 방지할 수 있습니다. 내부적으로 `chunkById`는 이전 청크의 마지막 모델보다 `id`가 큰 모델들을 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById` 및 `lazyById`는 자체적으로 "where" 조건을 쿼리에 추가하므로, 직접 조건을 걸 때는 [논리 그룹화](/docs/master/queries#logical-grouping)가 필요할 수 있습니다.

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
### 지연 컬렉션을 활용한 청킹

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 내부적으로 쿼리를 청크로 실행합니다. 하지만 각 청크를 클로저로 넘기지 않고, 펼쳐진(flattened) [LazyCollection](/docs/master/collections#lazy-collections) 스트림 객체로 반환합니다. 즉, 쿼리 전체를 데이터를 한 번에 가져오지 않고, 하나씩 반복 처리할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 메서드로 필터링하면서 컬럼을 업데이트해야 한다면, `lazyById` 메서드를 사용해야 합니다. 이 메서드는 내부적으로 이전 청크의 마지막 모델보다 큰 `id` 값만을 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 통해 `id` 기준 내림차순으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드처럼, `cursor` 메서드를 사용하면 수만 개의 레코드를 순회하는 상황에서 애플리케이션의 메모리 사용량을 크게 줄일 수 있습니다.

`cursor` 메서드는 하나의 데이터베이스 쿼리만 실행하지만, 실제로 반복문을 돌 때마다 모델 인스턴스를 하나씩 메모리에 로드합니다. 즉, 루프를 순회하는 동안 한 번에 한 개의 Eloquent 모델만 메모리에 남겨집니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 하나의 Eloquent 모델만 메모리에 올리므로, eager loading(즉시 로딩)된 연관관계를 지원하지 않습니다. 연관관계를 미리 불러와야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하는 것이 좋습니다.

`cursor` 메서드는 내부적으로 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/master/collections#lazy-collections)은 일반적인 Laravel 컬렉션이 제공하는 대부분의 컬렉션 메서드를 사용하면서도, 한 번에 하나의 모델만 메모리에 올립니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 기존의 쿼리와 달리 한 번에 하나만 메모리에 올리기 때문에 훨씬 적은 메모리를 사용하지만, 결국에는 [PHP의 PDO 드라이버가 모든 쿼리 결과를 내부 버퍼에 캐싱] (https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)하기 때문에, 매우 많은 레코드를 다루는 경우에는 [lazy 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리를 지원하여, 관련된 테이블의 데이터를 단일 쿼리로 가져올 수 있도록 합니다. 예를 들어, 각 최종 목적지별로 가장 최근에 도착한 항공편의 이름을 함께 조회하고 싶을 때, 쿼리 빌더의 `select` 또는 `addSelect` 메서드를 사용해 서브쿼리를 삽입할 수 있습니다.

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

쿼리 빌더의 `orderBy` 메서드 역시 서브쿼리를 지원합니다. 예를 들어, 각 목적지별로 가장 최근에 도착한 시간 기준으로 데이터를 정렬할 수 있습니다. 이 작업도 단일 쿼리로 처리됩니다.

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

조건에 맞는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 등의 메서드를 통해 단일 레코드만 모델 인스턴스로 조회할 수 있습니다.

```php
use App\Models\Flight;

// 기본 키로 조회...
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 조건에 맞는 첫 번째 모델 조회(대안)...
$flight = Flight::firstWhere('active', 1);
```

때때로 결과가 없을 경우 다른 동작을 하고 싶을 때가 있습니다. `findOr`, `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과가 없으면 전달된 클로저를 실행합니다. 클로저에서 반환된 값이 해당 메서드의 결과가 됩니다.

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

특정 모델을 찾지 못했을 때 예외를 던지게 하고 싶을 때가 있습니다. 이는 라우트나 컨트롤러에서 자주 쓰입니다. `findOrFail` 및 `firstOrFail` 메서드는 쿼리 결과가 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException`을 던집니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException` 예외를 잡지 않으면, Laravel은 자동으로 404 HTTP 응답을 클라이언트에게 반환합니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 지정한 컬럼/값 쌍으로 데이터베이스 레코드를 찾으려고 시도합니다. 찾을 수 없으면, 첫 번째 인수와(선택적으로) 두 번째 인수 배열을 합쳐 새 레코드를 생성합니다.

`firstOrNew`는 `firstOrCreate`와 비슷하지만, 모델 인스턴스만 반환하고 데이터베이스에는 아직 저장하지 않습니다. 직접 `save`를 호출해야 실제로 저장됩니다.

```php
use App\Models\Flight;

// 이름으로 항공편을 찾거나, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름, delayed, arrival_time 속성으로 생성(없으면)
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 항공편을 찾거나, 없으면 인스턴스만 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름, delayed, arrival_time 속성으로 인스턴스만 반환(저장 필요)
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델에서도 `count`, `sum`, `max` 등 [Laravel 쿼리 빌더의 집계 메서드](/docs/master/queries#aggregates)를 사용할 수 있습니다. 이러한 메서드는 Eloquent 모델 인스턴스 대신 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 저장 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때는, 데이터 조회뿐만 아니라 새 레코드 삽입도 매우 간단합니다. 새 레코드를 삽입하려면 새로운 모델 인스턴스를 생성하고 속성을 할당한 뒤, `save` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 항공편을 데이터베이스에 저장
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

이 예시에서 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델의 `name` 속성에 할당하고, `save` 메서드를 호출하여 데이터베이스에 저장합니다. 이때 `created_at`, `updated_at` 타임스탬프는 자동으로 설정됩니다.

또는 `create` 메서드를 사용하여 한번에 인스턴스 생성과 저장을 할 수도 있습니다. 반환값은 삽입된 모델 인스턴스입니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하려면 모델 클래스에 `fillable` 이나 `guarded` 속성을 반드시 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점(mass assignment vulnerability)을 방지하기 위해 보호되어 있기 때문입니다. 이에 대한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하십시오.

<a name="updates"></a>
### 업데이트

`save` 메서드는 이미 존재하는 레코드를 업데이트할 때도 사용할 수 있습니다. 먼저 모델을 조회한 뒤, 변경하고자 하는 속성을 할당하고, `save`를 호출하면 됩니다. `updated_at` 타임스탬프는 자동으로 갱신됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

기존 모델을 업데이트하거나, 없다면 새로 생성해야 할 때는 `firstOrCreate`와 유사하게 `updateOrCreate` 메서드를 사용할 수 있습니다. 이 메서드는 모델이 없으면 새로 생성하고, 있으면 업데이트를 수행합니다. 별도의 `save` 호출이 필요 없습니다.

아래 예제에서는 `departure`가 `Oakland`, `destination`이 `San Diego`인 항공편이 있으면 컬럼을 업데이트하고, 없으면 새로 생성합니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

`firstOrCreate`나 `updateOrCreate` 사용 시, 실제로 모델이 새로 생성된 경우를 구분하고 싶으면, `wasRecentlyCreated` 속성을 확인하면 됩니다.

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // 새 항공편 레코드가 삽입됨...
}
```

<a name="mass-updates"></a>
#### 대량 업데이트

특정 조건에 맞는 여러 모델에 대해 한 번에 업데이트할 수도 있습니다. 예를 들어, `active`가 1이고 `destination`이 `San Diego`인 모든 항공편을 지연(delayed) 처리하려면 아래와 같이 쓸 수 있습니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼/값의 쌍을 배열로 받으며, 반환값은 영향을 받은 행의 수입니다.

> [!WARNING]
> Eloquent로 대량 업데이트를 실행하면, 해당 모델에 대해 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. 실제로 모델 인스턴스를 로드하지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 확인

Eloquent에서는 모델의 내부 상태 변화를 확인하기 위한 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다. 이들 메서드를 활용하면 모델 조회 이후 속성의 변경 여부를 쉽게 확인할 수 있습니다.

`isDirty` 메서드는 모델 조회 후 속성이 변경되었는지 확인합니다. 특정 속성명이나 속성명 배열을 인수로 줄 수 있습니다. `isClean`은 변경되지 않은 경우 사용하며 마찬가지로 속성을 지정하는 것도 가능합니다.

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

`wasChanged` 메서드는 모델이 가장 최근 저장된 시점에 어떤 속성이 실제로 변경됐는지 확인합니다. 특정 속성명 또는 배열도 지정할 수 있습니다.

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

`getOriginal` 메서드는 모델 조회 시점의 원본 속성값을 배열로 반환합니다. 특정 속성을 지정하면 해당 값만 반환합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성값 배열...
```

`getChanges`는 최근에 저장된 시점에 변경된 속성만 배열로 반환하고, `getPrevious`는 저장 직전의 원본 속성값을 배열로 반환합니다.

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

`create` 메서드를 사용하면 한 번의 PHP 구문으로 새 모델을 저장할 수 있습니다. 이때 지정된 데이터로 모델을 채우고 저장하며, 생성된 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create`를 사용하기 전에, 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나를 지정해야 합니다. 이는 모든 Eloquent 모델이 대량 할당 취약점으로부터 기본적으로 보호되어 있기 때문입니다.

대량 할당 취약점이란, 사용자가 예기치 않은 HTTP 요청 필드를 전달해 데이터베이스의 의도하지 않은 컬럼(예: `is_admin`)이 변경되는 상황을 의미합니다. 예를 들어 악의적인 사용자가 `is_admin` 필드를 포함해 HTTP 요청을 보내면, 모델의 `create` 메서드를 통해 본인이 관리자로 승격될 수 있습니다.

따라서 보호하고 싶은 속성을 `$fillable` 배열에 명시해두어야 합니다. 예를 들어, `Flight` 모델의 `name`만 대량 할당이 가능하도록 하려면 아래와 같이 작성합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 가능 속성
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

`fillable`에 명시한 후에는 `create`를 사용해 안전하게 레코드를 생성할 수 있습니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 인스턴스가 있다면, `fill` 메서드로 여러 속성을 한 번에 채울 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당 및 JSON 컬럼

JSON 컬럼의 대량 할당 역시, 각 컬럼의 키를 `$fillable` 배열에 지정해야 합니다. 보안을 위해 `guarded`만 지정된 경우에는 중첩된 JSON 속성의 업데이트를 지원하지 않습니다.

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
#### 대량 할당 완전 허용

모든 속성을 대량 할당 가능하게 하려면, 모델의 `$guarded` 속성을 빈 배열로 지정하면 됩니다. 단, `fill`, `create`, `update`에 넘기는 배열을 항상 직접 작성하는 등 각별한 주의가 필요합니다.

```php
/**
 * 대량 할당이 불가능한 속성들
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로 `$fillable`에 포함되지 않은 속성은 대량 할당 시 자동으로 무시(discard)됩니다. 운영 환경에서는 보안상 이 방식이 적합하지만, 개발 환경에서는 직관적이지 않을 수 있습니다.

필요하다면, `preventSilentlyDiscardingAttributes` 메서드를 호출해 대량 할당 시 예외를 발생시킬 수 있습니다. 보통 이 코드는 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

Eloquent의 `upsert` 메서드를 사용하면, 여러 레코드를 한 번에 원자적(atomic)으로 삽입 또는 업데이트할 수 있습니다. 첫 번째 인수로는 삽입 또는 업데이트할 값들, 두 번째 인수로는 테이블 내에서 레코드를 고유하게 식별할 컬럼(들), 세 번째 인수로는 기존 레코드가 있을 때 업데이트되는 컬럼들을 지정합니다. 타임스탬프가 활성화된 경우, `created_at`, `updated_at`이 자동으로 관리됩니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드 두 번째 인수로 지정한 컬럼이 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. MariaDB, MySQL은 이 인수를 무시하고, 테이블의 "primary","unique" 인덱스만을 사용합니다.

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

위 예시에서는 먼저 모델을 조회한 뒤 삭제했습니다. 만약 모델의 기본 키를 이미 알고 있다면, `destroy` 메서드로 바로 삭제할 수 있습니다. 이 메서드는 단일 기본 키, 복수 개의 기본 키, 기본 키 배열, [컬렉션](/docs/master/collections) 등 다양한 데이터를 인수로 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용 중이라면, `forceDestroy` 메서드로 영구적으로 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드하고 `delete`를 호출하므로, 해당 모델의 `deleting`, `deleted` 이벤트가 올바르게 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

물론, Eloquent 쿼리를 통해 조건에 맞는 모든 모델을 삭제할 수도 있습니다. 예를 들어, `active`가 0인 모든 항공편을 삭제하려면 아래와 같이 사용합니다. 대량 삭제에서는 모델 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 모델을 삭제하려면 조건 없이 쿼리를 실행하면 됩니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent의 대량 삭제 쿼리를 실행할 때는, `deleting`, `deleted` 모델 이벤트가 발생하지 않습니다. 내부적으로 모델을 실제로 조회하지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

데이터베이스에서 실제로 레코드를 삭제하는 것 외에도, Eloquent는 "소프트 삭제(soft delete)" 기능을 제공합니다. 소프트 삭제 시 레코드를 DB에서 삭제하지 않고, 모델의 `deleted_at` 속성에 "삭제된" 날짜와 시간이 기록됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하면 됩니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime`/`Carbon` 인스턴스로 변환해줍니다.

테이블에 `deleted_at` 컬럼이 있어야 하며, Laravel [스키마 빌더](/docs/master/migrations)로 쉽게 추가할 수 있습니다.

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

이제 모델에서 `delete`를 호출하면, `deleted_at` 컬럼에 현재 시각이 기록되고, 실제로는 테이블에서 제거되지 않습니다. 소프트 삭제를 사용하면, 기본적으로 소프트 삭제된 레코드는 모든 쿼리에서 자동으로 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 판단하려면 `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원

가끔 소프트 삭제한 모델을 "언삭제"하고 싶을 때가 있습니다. 이때는 모델 인스턴스에서 `restore`를 호출하면, `deleted_at`이 null로 설정되어 복원됩니다.

```php
$flight->restore();
```

또는 쿼리에서 복수의 모델을 복원할 수도 있습니다. 대량 복원 역시 모델 이벤트가 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[연관관계](/docs/master/eloquent-relationships) 쿼리를 통해서도 복원할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

모델을 데이터베이스에서 완전히 삭제해야 할 경우, `forceDelete`를 사용할 수 있습니다.

```php
$flight->forceDelete();
```

Eloquent 연관관계 쿼리에서도 `forceDelete` 메서드를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함 조회

기본적으로 소프트 삭제된 모델은 쿼리에서 제외됩니다. 그러나 `withTrashed` 메서드를 사용하면 소프트 삭제된 모델을 포함하여 쿼리 결과를 반환할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

[연관관계](/docs/master/eloquent-relationships) 쿼리에서도 `withTrashed`를 사용할 수 있습니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed` 메서드를 사용하면 소프트 삭제된 모델만 조회할 수 있습니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

주기적으로 사용하지 않는 모델을 정리하고 싶을 때가 있습니다. 이를 위해, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 모델에 추가하면 주기적으로 자동 가지치기를 할 수 있습니다. 모델 클래스에 `prunable` 메서드를 구현하여 필요 없는 모델을 식별하는 쿼리를 반환하도록 합니다.

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
     * 가지치기가 필요한 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

`Prunable`로 항목을 지정한 모델은, `pruning` 메서드를 추가로 정의해 삭제 직전 부가 리소스(예: 파일 등)를 정리할 수 있습니다.

```php
/**
 * 모델 가지치기 전 준비(파일 삭제 등)
 */
protected function pruning(): void
{
    // ...
}
```

설정이 끝나면, `routes/console.php`에 `model:prune` Artisan 명령어를 스케줄링하면 됩니다. 실행 주기는 자유롭게 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령어는 기본적으로 `app/Models` 디렉터리 아래의 Prunable 모델을 자동 탐지합니다. 모델이 다른 위치에 있을 경우 `--model` 옵션으로 명시할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 제외하고 pruning을 실행하려면 `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 주고 `model:prune` 명령어를 실행하면 실제 pruning 없이 삭제될 레코드의 개수만 미리 확인할 수 있습니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> soft delete 모델도 prunable 쿼리에 매치되면 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 적용하면, 모델이 데이터베이스에서 대량 삭제 쿼리로 삭제됩니다. 이 경우 `pruning` 메서드나, `deleting`, `deleted` 모델 이벤트가 실행되지 않습니다. 모델을 실제로 조회하지 않고 바로 삭제하므로 pruning 성능이 크게 향상됩니다.

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
     * 가지치기가 필요한 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스의 "저장되지 않은" 복제본을 만드는 데는 `replicate` 메서드를 사용합니다. 동일한 속성이 많은 인스턴스를 여러 개 만들어야 할 때 유용합니다.

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

복제 시 특정 속성을 제외하려면 `replicate` 메서드에 배열을 넘기면 됩니다.

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

글로벌 스코프를 사용하면, 특정 모델의 모든 쿼리에 자동으로 조건을 추가할 수 있습니다. 예를 들어, Laravel의 [소프트 삭제](#soft-deleting) 기능은 글로벌 스코프를 활용하여 "삭제되지 않은" 모델만 기본적으로 조회합니다. 직접 글로벌 스코프를 작성하면, 특정 모델의 모든 쿼리에 항상 원하는 조건을 간편하게 추가할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성

새로운 글로벌 스코프를 생성하려면 `make:scope` Artisan 명령어를 사용하며, 생성된 스코프는 `app/Models/Scopes` 디렉터리에 위치합니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프 작성은 매우 간단합니다. 먼저 `make:scope` 명령어로 스코프 클래스를 만들고, 해당 클래스에서 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현합니다. 인터페이스에는 `apply` 메서드가 있으며, 이곳에서 필요한 쿼리 조건을 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 select 절에 컬럼을 추가할 때는 `select` 대신 `addSelect`를 사용해야 기존 select 절이 의도치 않게 대체되는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

글로벌 스코프를 모델에 할당하려면, 해당 모델에 `ScopedBy` 속성(Attribute)을 부여하면 됩니다.

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

또는, 모델의 `booted` 메서드를 오버라이드해서 `addGlobalScope`로 직접 등록할 수도 있습니다.

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

위와 같이 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 호출 시 아래와 같은 SQL이 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(클로저) 글로벌 스코프

Eloquent에서는 클래스가 아닌 클로저로 간단한 글로벌 스코프도 정의할 수 있습니다. `addGlobalScope`의 첫 번째 인수로 스코프명을, 두 번째 인수로 클로저를 전달합니다.

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

특정 쿼리에서 글로벌 스코프를 제거하고 싶다면 `withoutGlobalScope` 메서드를 사용합니다. 인수로는 글로벌 스코프 클래스명을 전달합니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의한 경우에는, 등록 당시의 스코프명을 문자열로 넘겨야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 모든 글로벌 스코프를 삭제하려면 `withoutGlobalScopes`, `withoutGlobalScopesExcept`를 사용할 수 있습니다.

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 제외할 글로벌 스코프만 남기고 모두 제거
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프를 사용하면, 자주 사용하는 쿼리 조건 집합을 재사용 가능한 메서드로 정의할 수 있습니다. 예를 들어, "인기 있는 사용자"만 자주 조회할 경우 아래와 같이 스코프를 메서드로 정의합니다.

스코프 메서드는 반드시 동일한 쿼리 빌더 인스턴스를 반환하거나 `void`여야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자만 포함하도록 쿼리 제약
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 포함하도록 쿼리 제약
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

스코프를 정의했다면, 쿼리에서 스코프 메서드를 바로 호출할 수 있습니다. 여러 스코프를 체인으로 연결하는 것도 가능합니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or` 연산자로 조합할 때는 [논리 그룹화](/docs/master/queries#logical-grouping)가 필요할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이 과정을 더 쉽게 할 수 있게, Laravel은 "higher order" `orWhere` 메서드를 통해 클로저 없이 스코프들을 체인 방식으로 묶을 수 있도록 지원합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적(파라미터 사용) 스코프

파라미터를 받는 스코프 메서드를 사용할 수 있습니다. `$query` 이후에 원하는 매개변수를 추가하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 포함하는 쿼리 제약
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

사용 시에는 메서드에 인자로 넘기면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending Attributes

스코프를 쿼리 제약뿐만 아니라, 해당 조건과 동일한 속성을 자동으로 가진 모델 생성 등에 활용하고 싶다면, 쿼리에서 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 드래프트만 조회하는 스코프
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

`withAttributes`는 쿼리에 `where` 조건을 추가함과 동시에, 해당 속성을 나중에 모델 생성 시 자동으로 포함시킵니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes`에 `asConditions` 인수를 false로 전달하면 쿼리는 추가하지 않고 속성만 설정할 수 있습니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 같은 모델 인지 여부를 확인해야 할 때가 있습니다. `is` 및 `isNot` 메서드로 두 모델이 동일한 기본 키, 테이블, 데이터베이스 연결을 가지는지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`, `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/master/eloquent-relationships) 사용 시에도 지원되므로, 쿼리 없이 관련 모델을 비교할 때도 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 측 애플리케이션으로 실시간 브로드캐스트하고 싶다면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/master/broadcasting#model-broadcasting)을 참고하십시오.

Eloquent 모델은 모델 생명주기의 여러 시점에 다양한 이벤트를 디스패치(dispatch)합니다. 주요 이벤트로는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등이 있습니다.

`retrieved`는 모델이 데이터베이스에서 조회될 때, `creating`/`created`는 최초 저장, `updating`/`updated`는 수정되어 `save`될 때, `saving`/`saved`는 생성 및 수정 양쪽 모두에서 발생하며, `-ing`로 끝나는 이벤트는 변경이 저장되기 전, `-ed`로 끝나는 이벤트는 변경이 저장된 후에 발생합니다.

모델 이벤트를 수신(Listen)하려면, `$dispatchesEvents` 속성에 이벤트와 [이벤트 클래스](/docs/master/events)의 매핑을 정의합니다. 이벤트 클래스는 생성자로 영향을 받는 모델 인스턴스를 받습니다.

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
     * 모델의 이벤트 맵
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트를 정의하고 매핑한 뒤에는, [이벤트 리스너](/docs/master/events#defining-listeners)를 사용해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent의 대량 업데이트 또는 삭제 쿼리를 실행할 경우, 해당 모델의 `saved`, `updated`, `deleting`, `deleted` 이벤트는 발생하지 않습니다. 이는 모델이 실제로 로드되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저를 사용한 이벤트

커스텀 이벤트 클래스를 사용하지 않고, 다양한 모델 이벤트가 발생할 때마다 바로 실행될 클로저를 등록할 수도 있습니다. 보통 이 클로저들은 모델의 `booted` 메서드에서 등록합니다.

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

필요하다면 [큐 가능한 익명 이벤트 리스너](/docs/master/events#queuable-anonymous-event-listeners)를 사용할 수도 있습니다. 이렇게 등록하면 큐(Queue)를 통해 모델 이벤트 리스너가 백그라운드에서 실행됩니다.

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

하나의 모델에 대해 여러 이벤트를 수신(Listen)해야 할 때는, 옵저버를 만들어 리스너를 한 클래스로 모을 수 있습니다. 옵저버 클래스에는 각 Eloquent 이벤트에 대응되는 이름의 메서드를 정의하며, 각 메서드는 영향을 받은 모델을 인수로 받습니다. `make:observer` Artisan 명령어로 옵저버 클래스를 쉽게 생성할 수 있습니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어로 생성된 옵저버는 `app/Observers` 디렉터리에 위치합니다. 디렉터리가 없다면 Artisan이 자동으로 생성해줍니다. 기본 옵저버 클래스는 다음과 같은 구조입니다.

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

옵저버 등록은 해당 모델에 `ObservedBy` 속성(Attribute)을 부여하거나,

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

`AppServiceProvider`의 `boot` 메서드 등에서 `observe` 메서드로 수동 등록할 수도 있습니다.

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
> 옵저버가 수신할 수 있는 이벤트에는 `saving`, `retrieved` 등도 있습니다. 자세한 사항은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 데이터베이스 트랜잭션 내에서 생성될 때, 옵저버가 이벤트 핸들러를 트랜잭션 커밋 후에만 실행하게 하고 싶다면, 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 트랜잭션이 없을 때는 즉시 실행됩니다.

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
### 이벤트 음소거(Muting)

때로 모델에서 발생하는 모든 이벤트를 일시적으로 "음소거(mute)"해야 할 때가 있습니다. 이럴 때는 `withoutEvents` 메서드에 클로저를 넘기면, 해당 클로저 내부의 코드는 이벤트가 발생하지 않으며, 클로저 내부에서 반환한 값이 메서드의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 이벤트 없이 저장

특정 모델에 대해 이벤트를 발생시키지 않고 "저장"하고 싶을 때는 `saveQuietly` 메서드를 사용할 수 있습니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

마찬가지로 "업데이트", "삭제", "소프트 삭제", "복원" 작업도 이벤트 발생 없이 할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
