# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격 모드 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [지연 컬렉션을 이용한 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트(upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 프루닝(pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [보류 중인 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 일시 중지](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와 쉽게 상호작용할 수 있도록 도와주는 객체-관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블에는 해당 테이블과 상호작용하기 위한 "모델"이 대응됩니다. 데이터베이스 테이블에서 레코드를 조회하는 것 외에도, Eloquent 모델은 테이블에 레코드를 삽입, 업데이트 및 삭제할 수도 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성하세요. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/master/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

시작하려면 Eloquent 모델을 생성해 보겠습니다. 모델 클래스는 보통 `app\Models` 디렉터리에 위치하고, `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. `make:model` [Artisan 명령어](/docs/master/artisan)를 사용해 새로운 모델을 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성할 때 함께 [데이터베이스 마이그레이션](/docs/master/migrations)까지 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성하면서 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등의 여러 클래스를 동시에 생성할 수도 있으며, 옵션을 조합하여 한 번에 여러 클래스를 생성할 수 있습니다:

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

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 클래스 생성 단축키...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 확인하기

가끔 모델 코드만 봐서는 사용 가능한 속성(attribute)과 연관관계(relationships)를 모두 알기 어려울 수 있습니다. 이럴 경우 `model:show` Artisan 명령어를 사용하세요. 이 명령어는 모델의 속성과 연관관계에 대한 편리한 개요를 제공합니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 기본적인 모델 클래스를 살펴보고 Eloquent의 주요 관례를 알아봅시다:

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

위 예제를 보면, `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 Eloquent에 명시하지 않았습니다. 관례상 클래스 이름의 "스네이크 케이스(snake case)" 복수형이 테이블 이름으로 사용됩니다. 따라서 `Flight` 모델은 `flights` 테이블과 연동되고, `AirTrafficController` 모델의 경우 `air_traffic_controllers` 테이블과 연동됩니다.

관례에 맞지 않는 테이블명을 사용하는 경우에는 모델에 `protected $table` 속성을 정의하여 직접 테이블명을 지정할 수 있습니다:

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
### 기본 키

Eloquent는 각 모델의 테이블에 기본 키 컬럼으로 `id`가 있다고 가정합니다. 다른 컬럼명을 기본 키로 사용하려면 모델에 `protected $primaryKey` 속성을 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블과 연결된 기본 키 컬럼명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, Eloquent는 기본 키가 자동 증가하는 정수형 값이라고 가정하며, 기본 키를 자동으로 정수형으로 변환합니다. 자동 증가하지 않거나 비정수형 기본 키를 사용하려면, 모델에 `public $incrementing` 속성을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 ID 자동 증가 여부 표시.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아닐 경우, `protected $keyType` 속성을 `string`으로 정의해야 합니다:

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
#### 복합 기본 키("Composite" Primary Keys)

Eloquent 모델은 기본 키로 최소 하나의 고유 식별자("ID")를 요구합니다. 복합 기본 키는 지원하지 않지만, 테이블에 기본 키 외에 추가 다중 컬럼 고유 인덱스를 추가하는 것은 가능합니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

자동 증가 정수를 기본 키로 사용하는 대신 UUID를 사용할 수도 있습니다. UUID는 36자리의 범용 고유 식별자입니다.

UUID 키를 사용하려면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 적용하세요. 그리고 [UUID 컬럼 유형을 갖는 기본 키](/docs/master/migrations#column-method-uuid)가 테이블에 있어야 합니다:

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

기본적으로 `HasUuids`는 인덱싱에 효율적인 ["ordered" UUID](/docs/master/strings#method-str-ordered-uuid)를 생성합니다.

UUID 생성 방식을 변경하려면, 모델에 `newUniqueId` 메서드를 정의하세요. 또한 UUID를 적용할 컬럼명을 `uniqueIds` 메서드로 지정할 수도 있습니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델의 새로운 UUID 생성.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID가 부여될 컬럼 목록 반환.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 적용하고, [ULID 컬럼 유형의 기본 키](/docs/master/migrations#column-method-ulid)가 테이블에 있어야 합니다. ULID는 UUID와 유사하지만 26자리이며, 역시 인덱싱에 유리한 정렬이 가능합니다:

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

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼이 테이블에 있다고 가정하며, 모델 생성이나 갱신 시 자동으로 이 컬럼들을 설정합니다. 이 자동 관리 기능을 비활성화하려면, 모델에 `public $timestamps` 속성을 `false`로 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 타임스탬프 사용 여부 표시.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프 저장 형식을 변경하려면, 모델에 `$dateFormat` 속성을 설정하세요. 이 속성은 데이터베이스 내 저장 방식과 배열/JSON 직렬화 시 포맷에 영향을 줍니다:

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

타임스탬프 컬럼 이름을 변경하려면, `CREATED_AT` 및 `UPDATED_AT` 상수를 모델에 정의할 수 있습니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프를 수정하지 않고 작업하려면 `withoutTimestamps` 메서드로 클로저를 감싸 실행하세요:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델이 다른 연결을 사용하도록 하려면 모델에 `protected $connection` 속성을 정의하세요:

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
### 기본 속성 값

새로 생성된 모델 인스턴스는 기본적으로 속성 값이 비어 있습니다. 모델의 일부 속성에 기본값을 지정하려면 모델에 `$attributes` 속성 배열을 정의할 수 있습니다. 이 배열의 값은 데이터베이스에서 읽어온 원시 사양과 동일한 형태 여야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 속성의 기본값 정의.
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

Laravel은 Eloquent 동작 및 "엄격 모드(strictness)"를 다양한 상황에 맞게 구성할 수 있는 여러 방법을 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩 기능을 차단할지 여부를 위한 선택적 불리언 인수를 받습니다. 예를 들어, 프로덕션이 아닌 환경에서만 지연 로딩을 비활성화해 프로덕션 환경에서 실수로 지연 로딩되는 상황에도 문제가 없도록 할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출하면, `fillable`에 등록되지 않은 속성에 값을 채우려 시도할 때 예외가 던져집니다. 이는 개발 단계에서 원치 않는 속성 무시 문제를 예방하는 데 도움이 됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [관련 데이터베이스 테이블](/docs/master/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 해당 테이블을 쿼리할 수 있는 강력한 [쿼리 빌더](/docs/master/queries) 역할을 합니다. 모델의 `all` 메서드는 테이블 내 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

`all` 메서드는 테이블의 모든 결과를 반환합니다. 그러나 Eloquent 모델은 [쿼리 빌더](/docs/master/queries)이므로, 추가 제약 조건을 붙여 `get` 메서드로 결과를 조회할 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->take(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더 메서드](/docs/master/queries)를 모두 사용할 수 있음을 기억하세요.

<a name="refreshing-models"></a>
#### 모델 새로 고침

이미 데이터베이스에서 조회된 모델 인스턴스가 있다면, `fresh`와 `refresh` 메서드를 통해 모델을 "갱신"할 수 있습니다. `fresh`는 데이터베이스에서 다시 모델을 조회하여 기존 인스턴스에 영향을 주지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 모델 인스턴스를 데이터베이스의 새로운 데이터로 다시 채우며, 로드된 연관관계도 갱신합니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`이나 `get` 같은 메서드는 여러 개의 레코드를 조회하지만, 일반 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent `Collection` 클래스는 Laravel의 `Illuminate\Support\Collection` 클래스를 상속하므로, 다양한 유용한 메서드로 데이터를 다룰 수 있습니다. 예를 들어, `reject` 메서드를 이용해 클로저 결과에 따라 컬렉션에서 일부 모델을 제외할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

기본 컬렉션에 더해, Eloquent 컬렉션은 Eloquent 모델 컬렉션을 다루기 위한 추가 메서드들도 제공합니다.

Laravel 컬렉션은 PHP 반복자(Iterator)를 구현하므로, 배열처럼 foreach로 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

만약 수만 건의 Eloquent 레코드를 `all`이나 `get`으로 전부 불러오면 메모리가 부족해질 수 있습니다. 대신 `chunk` 메서드를 사용해 데이터를 일정 크기의 묶음(청크)으로 나누어 처리하는 것이 효과적입니다.

`chunk`는 모델의 일부씩 불러와 클로저에서 처리하게 해 대량 데이터도 메모리를 적게 사용하며 처리할 수 있게 돕습니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

첫 번째 인수는 한 번에 가져올 레코드 수, 두 번째 인수는 각 청크를 처리할 클로저입니다. 각 청크마다 쿼리가 실행되어 클로저에 전달됩니다.

`chunk` 메서드로 조회 결과를 필터링하면서 동시에 결과를 업데이트해야 한다면, 예기치 않은 결과를 막기 위해 `chunkById` 메서드를 사용하세요. 이 메서드는 이전 청크의 마지막 `id`보다 큰 레코드만 순차로 가져옵니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById`는 자체적으로 "where" 조건을 추가하므로, 논리 그룹핑([Logical Grouping](/docs/master/queries#logical-grouping))을 위해 조건을 클로저로 묶는 것이 바람직합니다:

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
### 지연 컬렉션을 이용한 청크 처리

`lazy` 메서드는 `chunk`와 비슷하게 내부적으로 쿼리를 청크 단위로 실행하지만, 클로저에 청크 전체를 넘기지 않고, `LazyCollection` 형태로 평탄화(flatten)해서 결과 스트림을 제공합니다. 이렇게 하면 결과를 한 번에 한 모델씩 순차적으로 처리할 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 결과를 필터링하면서 변경할 경우에는 `lazyById` 메서드를 사용하세요. 내부적으로 항상 이전 청크 마지막 `id`보다 큰 레코드를 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id` 내림차순으로 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서

`lazy`와 유사하게, `cursor` 메서드는 수만 건의 레코드를 메모리를 매우 적게 사용하며 순회할 수 있습니다.

`cursor`는 단 하나의 쿼리를 실행하며, 실제 모델은 순회할 때마다 동적으로 생성합니다. 즉, 메모리에 모델이 한 번에 하나만 존재합니다.

> [!WARNING]
> `cursor`는 메모리를 적게 사용하지만, 한 번에 하나의 모델만 인스턴스화하므로 관계를 eager 로딩할 수 없습니다. 관계가 필요할 경우 `lazy` 메서드를 사용하세요.

내부적으로 `cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 객체를 반환합니다. [Lazy collections](/docs/master/collections#lazy-collections)는 일회성 모델 로딩과 다양한 컬렉션 메서드를 함께 쓸 수 있게 합니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor`는 메모리를 덜 사용하지만, 결국 PHP PDO 드라이버가 쿼리 결과 전체를 내부 버퍼에 저장하기 때문에 무한정 메모리가 유지되는 것은 아닙니다. 매우 대용량 데이터의 경우 [lazy 메서드](#chunking-using-lazy-collections) 사용을 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 단일 쿼리로 관련 테이블에서 정보를 가져올 수 있는 고급 서브쿼리를 지원합니다. 예를 들어, 비행지_destination 테이블과 해당 목적지로 향하는 항공편_flight 테이블이 있다고 가정합니다. `_flights` 테이블에는 항공편이 도착한 시각을 나타내는 `arrived_at` 컬럼이 있습니다.

`select` 또는 `addSelect`의 서브쿼리를 사용해 모든 목적지와 각 목적지에 가장 최근에 도착한 항공편 이름을 단일 쿼리로 조회할 수 있습니다:

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

쿼리 빌더의 `orderBy` 메서드에 서브쿼리를 사용할 수도 있습니다. 위 예시에서 각 목적지가 가장 최근에 도착한 항공편의 도착 시각 순으로 정렬할 수 있습니다. 이 역시 단일 쿼리로 수행할 수 있습니다:

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

여러 레코드 조회 외에도, `find`, `first`, `firstWhere` 메서드를 사용해 단일 레코드를 조회할 수 있습니다. 이들은 컬렉션 대신 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 모델 조회
$flight = Flight::find(1);

// 쿼리 제약 조건에 맞는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// 위와 동일한 기능의 대안
$flight = Flight::firstWhere('active', 1);
```

결과가 없을 때 다른 작업을 수행하려면 `findOr`와 `firstOr` 메서드를 사용하세요. 레코드가 없으면 클로저가 실행되고, 클로저 반환값이 메서드 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 찾을 수 없을 경우 예외 발생

종종 모델이 없을 때 예외를 던지고 싶을 수 있습니다. 이런 경우에는 `findOrFail` 및 `firstOrFail` 메서드를 사용하세요. 이들은 쿼리의 첫 결과를 반환하고, 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외가 처리되지 않으면, 404 HTTP 응답이 클라이언트로 자동 반환됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 조건으로 데이터베이스에서 레코드를 찾고, 없으면 첫 번째 인수 배열과 두 번째 인수 배열을 병합한 속성으로 새 레코드를 삽입합니다.

`firstOrNew`는 레코드를 찾지 못하면 저장되지 않은 새 모델 인스턴스를 반환합니다. 직접 `save`를 호출해 저장해야 합니다:

```php
use App\Models\Flight;

// 이름으로 조회하거나 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나 없으면 추가 속성으로 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회하거나 없으면 인스턴스 생성만 (저장 X)
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나 없으면 지정 속성으로 인스턴스 생성
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델과 상호작용할 때, Laravel [쿼리 빌더](/docs/master/queries)의 `count`, `sum`, `max` 등 [집계 메서드](/docs/master/queries#aggregates)도 함께 사용할 수 있습니다. 이 메서드들은 Eloquent 모델이 아닌 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent는 데이터베이스에 새 레코드를 삽입하는 과정을 간단하게 만듭니다. 새로운 모델 인스턴스를 생성하고 속성을 설정한 후, `save` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 비행 정보 저장
     */
    public function store(Request $request): RedirectResponse
    {
        // 요청 유효성 검사…

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

위 예에서, HTTP 요청의 `name` 필드를 `Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save` 메서드 호출 시 `created_at`과 `updated_at` 타임스탬프가 자동으로 설정되므로 별도로 설정할 필요 없습니다.

대안으로 `create` 메서드를 이용하면 단일 문장으로 새 모델을 저장할 수 있고, 저장된 모델 인스턴스를 반환받습니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드 사용 전에는 반드시 모델에 `fillable` 혹은 `guarded` 속성을 설정해 대량 할당 취약점을 방지해야 합니다. 대량 할당에 관한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참조하세요.

<a name="updates"></a>
### 업데이트

`save` 메서드는 이미 존재하는 모델을 업데이트할 때도 사용됩니다. 모델을 조회하여 원하는 속성을 수정한 뒤 `save`를 호출하세요. `updated_at` 타임스탬프도 자동 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

가끔 기존 모델 업데이트나 없으면 새 모델 생성 작업이 필요할 수 있습니다. `firstOrCreate`처럼 `updateOrCreate` 메서드는 모델을 저장하므로 별도로 `save`를 호출할 필요가 없습니다.

아래 예시에서 `departure`가 'Oakland', `destination`이 'San Diego'인 항공편이 있으면 `price`와 `discounted` 컬럼을 업데이트하고, 없으면 병합된 속성으로 새 항공편을 만듭니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

쿼리 조건에 맞는 여러 모델을 한 번에 업데이트할 수도 있습니다. 예를 들어, `active` 상태이고 `destination`이 'San Diego'인 비행 정보를 모두 지연 상태로 표시하는 방법입니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드 인수로는 업데이트할 컬럼-값 배열을 전달하며, 영향을 받은 행 수를 반환합니다.

> [!WARNING]
> Eloquent 모델을 대상으로 대량 업데이트를 실행할 때는 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 이는 쿼리 실행 시 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 확인

Eloquent는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공해 모델의 내부 상태를 확인하여 어떤 속성이 변경되었는지 알 수 있습니다.

- `isDirty`: 모델이 처음 불러올 때와 다르게 변경된 속성이 있는지 확인합니다. 특정 속성명이나 배열을 인수로 전달할 수 있습니다.
- `isClean`: 속성이 변경되지 않았는지 확인합니다. 인수로 특정 속성명을 전달할 수 있습니다.
- `wasChanged`: 모델이 마지막으로 저장된 이후 변경된 속성이 있는지 확인합니다.

예:

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

`wasChanged` 사용 예:

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

`getOriginal` 메서드는 모델이 처음 조회된 당시 속성 값을 배열로 반환하며, 특정 속성명으로 개별 값을 불러올 수도 있습니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열 반환
```

`getChanges` 메서드는 마지막 저장 시 변경된 속성 배열을 반환합니다:

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

단일 구문으로 새 모델을 저장할 때 `create` 메서드를 이용할 수 있으며, 새 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 앞서 말했듯이, `create`를 사용하기 전에 모델에 `fillable` 혹은 `guarded` 속성을 반드시 정의해야 합니다. 이는 기본적으로 대량 할당 취약점을 막기 위한 보호 장치입니다.

대량 할당 취약점은 사용자가 예상하지 않은 HTTP 요청 필드를 보내 데이터베이스의 민감 컬럼(예: `is_admin`)이 조작될 위험이 있습니다.

이를 방지하려면, 모델 내 `$fillable` 배열에 명시적으로 대량 할당을 허용할 속성을 지정해야 합니다. 예를 들어, `Flight` 모델의 `name` 속성만 허용하는 경우:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당을 허용할 속성 목록.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

`fillable` 정의 후 다음과 같이 `create`를 안전하게 사용할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면 `fill` 메서드로 배열 형태의 속성을 일괄 할당할 수도 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### JSON 컬럼과 대량 할당

JSON 컬럼에 값을 할당할 때는, 각 JSON 키를 `$fillable` 배열에 명시해야 합니다. 보안을 위해 `guarded` 속성에는 네스트된 JSON 필드 업데이트가 지원되지 않습니다:

```php
/**
 * 대량 할당을 허용할 속성.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용하기

모델의 모든 속성을 대량 할당 가능하도록 하려면, `$guarded` 속성을 빈 배열로 정의하세요. 이 경우 `fill`, `create`, `update` 등에 전달하는 배열은 반드시 직접 신중하게 작성해야 합니다:

```php
/**
 * 대량 할당을 금지할 속성 (빈 배열이면 모두 허용).
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로, `$fillable`에 포함되지 않은 속성은 대량 할당 시 조용히 무시됩니다. 프로덕션 환경에서는 정상 동작이나, 개발 중에는 왜 값이 할당되지 않는지 헷갈릴 수 있습니다.

원할 경우, `preventSilentlyDiscardingAttributes` 메서드를 호출해 무시된 경우 예외가 발생하도록 할 수 있습니다. 보통 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 단일 원자 작업으로 레코드를 업데이트하거나 새로 생성합니다. 첫 인수는 삽입 또는 업데이트할 값 배열, 두 번째 인수는 레코드를 고유하게 식별할 컬럼(또는 컬럼 배열), 세 번째 인수는 기존 레코드가 있으면 업데이트할 컬럼 배열입니다. 타임스탬프가 활성화된 모델인 경우 `created_at`과 `updated_at`도 자동으로 설정합니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 두 번째 인수에 지정한 컬럼에 "기본 키" 또는 "고유" 인덱스가 필요합니다. MariaDB와 MySQL 드라이버는 두 번째 인수를 무시하고 해당 테이블의 기본 및 고유 인덱스를 항상 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델 인스턴스에서 `delete` 메서드를 호출해 삭제할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 코드는 모델을 데이터베이스에서 먼저 조회 후 삭제하지만, 기본 키만 알고 있다면 `destroy` 메서드를 사용해 직접 삭제할 수 있습니다. 단일 키, 여러 키, 키 배열, 키 컬렉션 모두 인수로 가능합니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

만약 [소프트 삭제(soft deleting)](#soft-deleting) 기능을 사용 중이라면 `forceDestroy` 메서드로 영구 삭제할 수 있습니다:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별로 로드하고 `delete`를 호출하여 `deleting` 및 `deleted` 이벤트가 적절히 발송되도록 합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 모델 삭제

쿼리를 사용해 조건에 맞는 모델을 한번에 삭제할 수도 있습니다. 아래 예시에서는 비활성화된 모든 항공편을 삭제합니다. 대량 삭제 시에도 이벤트는 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

모든 모델을 삭제하려면 조건 없이 쿼리를 실행하세요:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> 대량 삭제 시에는 `deleting` 및 `deleted` 이벤트가 호출되지 않습니다. 이는 실제 모델을 조회하지 않고 쿼리가 직접 실행되기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 레코드를 실제로 삭제하는 대신 "소프트 삭제"를 할 수 있습니다. 소프트 삭제된 모델은 테이블에 남아 있지만 `deleted_at` 속성에 삭제 시점 타임스탬프가 기록됩니다. 이를 활성화하려면 모델에서 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 사용하세요:

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
> `SoftDeletes` 트레이트는 `deleted_at`을 `DateTime` / `Carbon` 객체로 자동 변환해줍니다.

테이블에도 `deleted_at` 컬럼이 있어야 하며, Laravel [스키마 빌더](/docs/master/migrations)에 `softDeletes` 헬퍼 메서드가 있습니다:

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

`delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 시각으로 설정되며, 데이터는 남겨집니다. 소프트 삭제된 모델은 기본 쿼리에서 자동 제외됩니다.

소프트 삭제 여부는 `trashed` 메서드로 확인할 수 있습니다:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 복원

소프트 삭제된 모델은 `restore` 메서드를 호출해 복원할 수 있으며, 이때 `deleted_at`이 `null`로 설정됩니다:

```php
$flight->restore();
```

쿼리에서 여러 모델을 복원할 수도 있습니다. 이 경우도 마찬가지로 이벤트는 발생하지 않습니다:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

관계 쿼리에서도 `restore` 메서드를 사용할 수 있습니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

소프트 삭제된 모델을 실제로 데이터베이스에서 완전히 삭제하려면 `forceDelete` 메서드를 사용하세요:

```php
$flight->forceDelete();
```

관계 쿼리에서도 영구 삭제가 가능합니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제된 모델 포함

기본 쿼리는 소프트 삭제된 모델을 제외하지만, `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 포함할 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 호출 가능합니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회

`onlyTrashed` 메서드는 **소프트 삭제된 모델만** 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 프루닝(pruning)

주기적으로 더 이상 필요 없는 모델을 삭제하고 싶을 때, `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하세요. 그 후 `prunable` 메서드에서 삭제할 조건 쿼리를 작성합니다:

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
     * 프루닝 할 모델 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable` 모델에 `pruning` 메서드를 정의해, 모델 삭제 전에 추가 작업(예: 저장된 파일 삭제)을 할 수 있습니다:

```php
/**
 * 프루닝 전 처리.
 */
protected function pruning(): void
{
    // ...
}
```

구성 후 `routes/console.php`에 `model:prune` Artisan 명령을 스케줄링하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령은 앱의 `app/Models` 디렉터리 내 "Prunable" 모델을 자동으로 감지합니다. 모델 위치가 다를 경우 `--model` 옵션으로 클래스 명을 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

모든 감지된 모델 중 일부만 제외하려면 `--except` 옵션을 사용하세요:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 붙여 실행하면 실제 삭제 없이 삭제 대상 개수를 보고합니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델은 프루닝 쿼리 조건에 맞으면 영구 삭제(`forceDelete`) 됩니다.

<a name="mass-pruning"></a>
#### 대량 프루닝

`Illuminate\Database\Eloquent\MassPrunable` 트레이트가 달린 모델은 대량 삭제 쿼리로 삭제합니다. 이때 `pruning` 메서드 호출 및 `deleting`, `deleted` 이벤트 실행이 없으므로 훨씬 효율적입니다:

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
     * 프루닝 할 모델 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 복제해 저장되지 않은 새 인스턴스를 만들 때 `replicate` 메서드를 사용합니다. 유사한 속성의 모델 인스턴스를 만들 때 유용합니다:

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

복제 시 특정 속성만 제외하려면 `replicate`에 제외할 속성 배열을 전달하세요:

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

글로벌 스코프를 이용하면 특정 모델의 모든 쿼리에서 조건을 자동으로 추가할 수 있습니다. Laravel의 [소프트 삭제 기능](#soft-deleting)이 바로 글로벌 스코프를 이용해 "삭제되지 않은" 모델만 조회하는 좋은 예입니다.

<a name="generating-scopes"></a>
#### 글로벌 스코프 생성

새 글로벌 스코프는 `make:scope` Artisan 명령으로 만드세요. 생성된 스코프 클래스는 `app/Models/Scopes` 디렉터리에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

`make:scope`로 생성된 스코프 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현합니다. `apply` 메서드만 구현하면 되고, 쿼리 빌더에 필요한 제약 조건을 추가하면 됩니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Eloquent 쿼리에 스코프 적용.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 쿼리에 컬럼을 추가할 때는 `addSelect`를 사용하세요. `select`는 기존 선택 절을 대체할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

모델에 글로벌 스코프를 적용하려면, `ScopedBy` 속성을 모델에 붙이거나:

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

모델의 `booted` 메서드를 오버라이드해 `addGlobalScope` 메서드를 호출할 수도 있습니다:

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

이 스코프가 적용된 후 `User::all()` 호출 시 다음 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

간단한 글로벌 스코프는 별도의 클래스 없이 클로저를 사용해 정의할 수 있습니다. 이 경우 `addGlobalScope`의 첫 번째 인수로 스코프 이름을 직접 정해야 합니다:

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

특정 쿼리에서 글로벌 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용합니다. 클래스 이름 또는 클로저 정의 시 붙인 이름을 인수로 전달하세요:

```php
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 글로벌 스코프 혹은 모든 스코프를 제거하려면 `withoutGlobalScopes` 메서드를 사용하세요:

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 특정 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 재사용 가능한 쿼리 제약 조건 집합을 정의할 수 있게 해줍니다. 예를 들어, "인기 사용자"만 조회하는 스코프를 만들 수 있습니다. 메서드 이름 앞에 접두사 `scope`를 붙여 정의합니다.

스코프 메서드는 항상 쿼리 빌더 인스턴스나 `void`를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자만 조회하는 스코프.
     */
    public function scopePopular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 조회하는 스코프.
     */
    public function scopeActive(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용하기

정의한 스코드는 쿼리 시 `scope` 접두사 없이 호출합니다. 여러 스코프도 체이닝 가능:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

복합 조건 일부에 `or` 연산자를 사용하려면 클로저로 조건 그룹핑이 필요할 수 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이를 간단히 하기 위해 "고차원" `orWhere` 문법도 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프가 인자를 받을 수도 있습니다. 필요한 매개변수를 `$query` 다음에 선언하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 조회하는 스코프.
     */
    public function scopeOfType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

호출 시 인자를 전달할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 보류 중인 속성

스코프 내 속성을 모델 생성 시에도 적용하려면, 스코프 쿼리에 `withAttributes` 메서드를 사용하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시 저장(draft) 상태만 조회하는 스코프.
     */
    public function scopeDraft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

`withAttributes`는 쿼리에 해당 조건을 추가하고, 스코프로 새 모델 생성 시 이 속성을 자동 적용합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "동일"한지 여부는 `is`와 `isNot` 메서드로 확인할 수 있습니다. 이 메서드는 두 모델의 기본 키, 테이블, 데이터베이스 연결이 같은지 비교합니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

이 메서드들은 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](/docs/master/eloquent-relationships) 객체에서도 사용할 수 있어, 관련 모델을 조회 없이 비교할 때 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션으로 직접 브로드캐스트하고 싶다면 Laravel의 [모델 이벤트 브로드캐스팅](/docs/master/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 발송해 모델 생명주기의 다양한 시점에 대응할 수 있습니다. 주요 이벤트로는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`이 있습니다.

- `retrieved`: 기존 모델을 데이터베이스에서 조회할 때 발송
- `creating`/`created`: 새 모델을 처음 저장할 때 발송
- `updating`/`updated`: 기존 모델을 수정해 저장할 때 발송
- `saving`/`saved`: 모델이 생성 또는 업데이트될 때 항상 발송 (속성 변경 여부 관계없음)
- 이벤트 이름이 `-ing`로 끝나면 변경 전, `-ed`로 끝나면 변경 후에 발송됨

이벤트를 수신하려면, Eloquent 모델에 `$dispatchesEvents` 배열을 정의해 각 이벤트에 대응하는 커스텀 이벤트 클래스를 지정하면 됩니다. 각 이벤트 클래스 생성자에는 해당 모델 인스턴스가 전달됩니다:

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

이벤트에 대응하는 [리스너](/docs/master/events#defining-listeners)를 정의해 처리할 수 있습니다.

> [!WARNING]
> 대량 업데이트 또는 삭제 쿼리 실행 시, 해당 모델들에 대한 `saved`, `updated`, `deleting`, `deleted` 이벤트는 발송되지 않습니다. 이는 실제 모델을 불러오지 않고 직접 쿼리로 작업하기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용

별도 이벤트 클래스를 만들지 않고, 모델 내 `booted` 메서드에서 이벤트에 대한 클로저를 등록할 수도 있습니다:

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

필요하다면 [큐 가능 익명 이벤트 리스너](/docs/master/events#queuable-anonymous-event-listeners)를 사용해 이벤트 리스너를 백그라운드 큐에서 실행할 수도 있습니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의

많은 이벤트를 리스닝해야 할 경우, 옵저버 클래스로 이벤트 수신기를 한곳에 모을 수 있습니다. 옵저버 클래스는 수신할 이벤트 이름과 같은 메서드를 갖고, 메서드 인수로 영향을 받은 모델을 받습니다. 옵저버 클래스는 `make:observer` Artisan 명령으로 쉽게 생성합니다:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령은 `app/Observers` 디렉터리에 옵저버 클래스를 생성합니다. 예:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 처리.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 처리.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 처리.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 처리.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 처리.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버 등록은 모델에 `ObservedBy` 속성을 붙이거나:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

`AppServiceProvider`의 `boot` 메서드에서 `observe` 메서드로 등록할 수도 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스 초기화.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버는 `saving`이나 `retrieved` 같은 추가 이벤트도 리스닝할 수 있습니다. 더 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델 생성이 데이터베이스 트랜잭션 내에서 이루어질 때, 옵저버 이벤트 핸들러가 트랜잭션 커밋 후에만 실행되도록 하려면, 옵저버가 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하도록 하세요. 트랜잭션이 없으면 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 처리.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 일시 중지

가끔 모델 이벤트를 일시적으로 "뮤트(mute)"하고 싶을 때가 있습니다. `withoutEvents` 메서드를 사용하면 클로저 내에서 실행되는 코드에 대해 이벤트가 발생하지 않습니다. 클로저의 반환값을 `withoutEvents`가 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장

모델을 저장할 때 이벤트 없이 처리하려면 `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이벤트 없이 `update`, `delete`, `soft delete`, `restore`, `replicate` 등의 작업도 가능합니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```