# Eloquent 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성하기](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [청크 처리](#chunking-results)
    - [지연 스트리밍 조회](#streaming-results-lazily)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 및 집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 프루닝 (Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저를 사용하는 이벤트](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 비활성화](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와 상호작용을 즐겁게 만들어 주는 객체 관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블에는 그 테이블과 상호작용하기 위한 해당하는 "모델"이 있습니다. 단순히 테이블에서 레코드를 조회하는 것뿐만 아니라, Eloquent 모델을 통해 레코드를 삽입, 업데이트, 삭제하는 것도 가능합니다.

> [!TIP]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성하세요. 데이터베이스 구성에 관한 자세한 내용은 [데이터베이스 구성 문서](/docs/{{version}}/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기

시작하려면 Eloquent 모델을 만들어 보겠습니다. 모델은 보통 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성하기 위해 `make:model` Artisan 명령어를 사용할 수 있습니다:

```
php artisan make:model Flight
```

모델을 생성할 때 동시에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 생성하고 싶다면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```
php artisan make:model Flight --migration
```

모델 생성 시 팩토리(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 요청(form request) 등 다양한 타입의 클래스도 함께 생성할 수 있습니다. 여러 옵션을 조합하여 한 번에 여러 클래스 생성도 가능합니다:

```bash
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

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청을 한 번에 생성하는 단축키...
php artisan make:model Flight --all

# 피벗 모델 생성...
php artisan make:model Member --pivot
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치합니다. 기본 모델 클래스를 살펴보고 Eloquent의 주요 규칙에 대해 설명합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    //
}
```

<a name="table-names"></a>
### 테이블 이름

위 예제를 보면 `Flight` 모델에 어떤 데이터베이스 테이블이 대응되는지 명시하지 않았다는 것을 알 수 있습니다. 관례에 따라, 클래스 이름을 "스네이크 케이스" 복수형으로 변환한 이름이 테이블 이름으로 자동 설정됩니다. 따라서 `Flight` 모델은 `flights` 테이블과 연결되고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 매핑됩니다.

만약 모델에 대응하는 테이블이 위 규칙과 다르다면, 모델 내에 `table` 속성을 정의해 직접 테이블 이름을 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델과 연결된 테이블 이름.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델에 대응되는 데이터베이스 테이블이 `id`라는 기본 키를 갖는다고 가정합니다. 만약 다른 컬럼을 기본 키로 사용하려면, 모델에 보호된 `$primaryKey` 속성을 정의하여 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 테이블과 연결된 기본 키 컬럼.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 기본 키가 자동 증가하는 정수라고 가정하며, 자동으로 정수형으로 캐스팅합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용한다면, 모델에 `public $incrementing` 속성을 `false`로 설정해야 합니다:

```
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동증가인지 여부.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아니라면, `protected $keyType` 속성을 `string`으로 지정해야 합니다:

```
<?php

class Flight extends Model
{
    /**
     * 자동 증가 ID의 데이터 타입.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### 복합 기본 키 (Composite Primary Keys)

Eloquent는 각 모델에 고유한 하나의 기본 키 컬럼이 있어야 하며, 복합 기본 키는 지원하지 않습니다. 하지만 데이터베이스 테이블에 기본 키 이외의 다중 컬럼 유니크 인덱스를 추가하는 것은 가능합니다.

<a name="timestamps"></a>
### 타임스탬프

기본적으로 Eloquent는 모델이 대응하는 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 기대합니다. 모델이 생성되거나 업데이트될 때 자동으로 이 컬럼들의 값이 설정됩니다. 만약 Eloquent가 이 컬럼들을 자동으로 관리하지 않게 하려면, 모델에 `$timestamps` 속성을 `false`로 설정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 타임스탬프가 관리되는지 여부.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프 저장 형식이나 직렬화 시 포맷을 변경하려면 `$dateFormat` 속성을 설정하세요:

```
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

또한 타임스탬프에 사용하는 컬럼명이 기본 `created_at`, `updated_at`이 아니라면, 모델에 `CREATED_AT`과 `UPDATED_AT` 상수를 정의하여 변경할 수 있습니다:

```
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

<a name="database-connections"></a>
### 데이터베이스 연결

모든 Eloquent 모델은 기본적으로 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에 대해 다른 연결을 사용하고 싶다면, 모델에 `$connection` 속성을 정의하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 사용할 데이터베이스 연결 이름.
     *
     * @var string
     */
    protected $connection = 'sqlite';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

새로 생성한 모델 인스턴스는 기본적으로 속성 값이 없습니다. 특정 속성들의 기본값을 지정하고 싶다면, 모델에 `$attributes` 속성을 정의하세요:

```
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
        'delayed' => false,
    ];
}
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 대응되는 데이터베이스 테이블을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델을 강력한 [쿼리 빌더](/docs/{{version}}/queries)로 생각할 수 있으며, 모델과 연결된 테이블을 유연하게 쿼리할 수 있습니다. 예를 들어 `all` 메서드를 사용하면 모델에 대응되는 테이블의 모든 레코드를 가져옵니다:

```
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

`all` 메서드는 테이블의 모든 레코드를 반환하지만, Eloquent 모델 자체가 쿼리 빌더 역할을 하기 때문에 쿼리에 추가 조건을 걸고 `get` 메서드를 호출하여 결과를 얻을 수 있습니다:

```
$flights = Flight::where('active', 1)
               ->orderBy('name')
               ->take(10)
               ->get();
```

> [!TIP]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더 메서드](/docs/{{version}}/queries)를 모두 익혀두면 Eloquent 쿼리 작성에 많이 도움이 됩니다.

<a name="refreshing-models"></a>
#### 모델 새로 고침하기

이미 데이터베이스에서 불러온 모델 인스턴스가 있을 때, `fresh`와 `refresh` 메서드를 통해 모델 데이터를 새로 고칠 수 있습니다. `fresh`는 DB에서 다시 모델을 조회해서 새로운 인스턴스를 반환하지만 기존 인스턴스는 변경하지 않습니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 모델 인스턴스를 데이터베이스로부터 새 데이터로 다시 채우며, 로드된 모든 연관관계도 갱신됩니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`이나 `get`과 같이 여러 레코드를 조회하는 Eloquent 메서드는 일반 PHP 배열을 반환하지 않고 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel 기본 컬렉션인 `Illuminate\Support\Collection`을 확장하며, 여러 유용한 [메서드](/docs/{{version}}/collections#available-methods)를 제공합니다. 예를 들어 `reject` 메서드를 사용해 특정 조건에 맞는 모델들을 컬렉션에서 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function ($flight) {
    return $flight->cancelled;
});
```

기본 컬렉션 클래스에서 제공하는 메서드 외에도 Eloquent 컬렉션에는 Eloquent 모델 컬렉션에 특화된 [추가 메서드들이 있습니다](/docs/{{version}}/eloquent-collections#available-methods).

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로 배열처럼 foreach로 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크 처리

수만 건 이상의 데이터를 `all`이나 `get`으로 전부 불러오는 것은 메모리 부족을 일으킬 수 있습니다. 이럴 때는 `chunk` 메서드를 써서 데이터를 부분 단위로 나누어 처리하세요.

`chunk`는 일정 개수만큼 해당하는 레코드를 조회해 클로저에 넘기고, 이 과정을 청크 단위로 반복합니다. 한 번에 전체 데이터를 불러오지 않아 메모리 부담이 크게 줄어듭니다:

```php
use App\Models\Flight;

Flight::chunk(200, function ($flights) {
    foreach ($flights as $flight) {
        //
    }
});
```

첫 번째 인자는 청크당 레코드 개수를 의미하고, 두 번째 인자는 각 청크마다 호출될 클로저입니다. 각 청크는 독립적인 쿼리로 조회됩니다.

만약 결과를 특정 컬럼으로 필터링하면서 그 컬럼 값을 반복문 내에서 동시에 업데이트하려면 `chunkById` 메서드를 사용하세요. `chunk` 메서드는 이런 동작에서 예상치 못한 결과가 나올 수 있기 때문입니다. `chunkById`는 내부적으로 항상 이전 청크의 마지막 `id`보다 큰 레코드만 조회합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function ($flights) {
        $flights->each->update(['departed' => false]);
    }, $column = 'id');
```

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 조회

`lazy` 메서드는 `chunk`와 유사하게 데이터베이스 쿼리를 청크 단위로 실행하지만, 클로저에 직접 넘기지 않고 **평탄화된** `LazyCollection` 형태로 반환해 결과를 하나씩 스트림처럼 순회할 수 있게 해줍니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    //
}
```

`lazy` 조건에 따라 데이터를 필터링하며 업데이트해야 한다면 `lazyById` 메서드를 사용하세요. 내부적으로 역시 `chunkById`처럼 작동해 안전한 반복을 보장합니다:

```php
Flight::where('departed', true)
    ->lazyById(200, $column = 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 조건에 따라 `id` 내림차순으로 정렬해서 지연 스트리밍할 수도 있습니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy`와 비슷한 기능을 하며, 수만 건 이상의 레코드를 조회할 때 메모리 사용량을 크게 줄일 수 있는 `cursor` 메서드도 있습니다.

`cursor`는 단일 쿼리를 실행하지만, 실제 모델 인스턴스는 반복할 때마다 하나씩 메모리에 로드됩니다. 따라서 한 번에 메모리에 하나의 모델만 유지합니다.

> [!NOTE]
> `cursor`는 메모리를 절약하기 위해 한 번에 하나의 모델만 유지하므로, 관계를 미리 로드하는 eager loading은 지원하지 않습니다. 관계를 eager loading하려면 [lazy 메서드](#streaming-results-lazily)를 사용하세요.

`cursor`는 PHP의 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용해 구현되었습니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    //
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. Lazy 컬렉션을 사용하면 일반 Laravel 컬렉션의 다양한 메서드를 사용할 수 있으면서도 메모리 소모를 최소화할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 메모리를 적게 쓰지만 PHP PDO 드라이버가 내부적으로 결과를 전부 버퍼에 캐싱하기 때문에 결국 메모리가 부족해질 수 있습니다. 매우 큰 데이터셋에는 [lazy 메서드](#streaming-results-lazily)를 사용하는 것이 좋습니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리 기능도 지원하여, 연관된 여러 테이블에서 정보를 한 번에 가져올 수 있습니다. 예를 들어 `destinations` 테이블과 목적지로의 `flights` 테이블이 있고 `flights`에 도착 시각을 나타내는 `arrived_at` 컬럼이 있다고 해봅시다.

서브쿼리 기능을 활용해 각 목적지와 해당 목적지에 가장 최근에 도착한 항공편 이름을 한 번의 쿼리로 선택할 수 있습니다:

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

쿼리 빌더의 `orderBy`에서도 서브쿼리를 쓸 수 있습니다. 예를 들어 기존 예시에서 각 목적지를 최근 도착한 비행 시각 기준으로 정렬할 수 있습니다. 이 역시 한 번의 쿼리로 수행 가능합니다:

```
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 및 집계 조회

특정 조건에 맞는 모든 레코드뿐만 아니라, `find`, `first`, `firstWhere` 같은 메서드를 통해 단일 모델을 쉽게 조회할 수 있습니다. 이들 메서드는 컬렉션이 아닌 단일 모델 인스턴스를 반환합니다:

```
use App\Models\Flight;

// 기본 키로 모델을 조회...
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 위와 같은 동작을 하는 firstWhere 메서드...
$flight = Flight::firstWhere('active', 1);
```

쿼리 결과가 없을 경우 첫 번째 결과를 조회하거나 다른 동작을 할 수도 있습니다. `firstOr` 메서드는 결과가 있으면 첫 번째 모델을 반환하지만, 없으면 지정한 클로저를 실행하고 그 결과를 반환합니다:

```
$model = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Not Found 예외 처리

모델을 조회하지 못했을 때 예외를 발생시키는 것이 필요한 경우가 있습니다. 라우트나 컨트롤러에서 자주 활용됩니다. `findOrFail` 및 `firstOrFail` 메서드는 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외를 처리하지 않으면 자동으로 HTTP 404 응답을 클라이언트에 반환합니다:

```
use App\Models\Flight;

Route::get('/api/flights/{id}', function ($id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍으로 데이터베이스에서 레코드를 찾고, 없으면 두 번째 인수와 합친 속성으로 새 레코드를 삽입합니다.

`firstOrNew`는 같은 방식으로 레코드를 찾지만, 없으면 새 모델 인스턴스를 반환합니다(데이터베이스에는 저장하지 않습니다). 저장하려면 따로 `save` 메서드를 호출해야 합니다:

```
use App\Models\Flight;

// 이름으로 항공편 조회, 없으면 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지연 여부와 도착 시간도 동시에 설정하여 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 Flight 인스턴스 생성...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 지연 여부와 도착 시간도 포함시켜 새 인스턴스 생성...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델과 함께 Laravel 쿼리 빌더가 제공하는 `count`, `sum`, `max` 등의 집계 함수도 사용할 수 있습니다. 이 메서드들은 Eloquent 모델 인스턴스가 아닌 스칼라 값을 반환합니다:

```
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent로 모델을 조회하는 것뿐 아니라, 새 레코드를 삽입하는 것도 간단합니다. 새 모델 인스턴스를 만들고 속성을 설정한 후 `save` 메서드를 호출하면 됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 항공편 정보를 데이터베이스에 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 요청 유효성 검증...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();
    }
}
```

위 예제는 HTTP 요청 데이터 중 `name` 값을 받아 `Flight` 모델의 `name` 속성에 할당하고, `save` 호출 시점에 데이터베이스에 삽입합니다. `created_at`, `updated_at` 타임스탬프도 자동으로 설정되므로 수동으로 설정할 필요가 없습니다.

또는 `create` 메서드를 써서 한 줄로 새 모델 인스턴스를 저장할 수도 있습니다. 이때 `create`는 새로 생성된 모델 인스턴스를 반환합니다:

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create`를 사용하려면 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나를 반드시 지정해야 합니다. 이는 기본적으로 모든 Eloquent 모델이 대량 할당 공격(mass assignment)으로부터 보호되기 때문입니다. 대량 할당에 관한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

기존 데이터도 `save` 메서드로 쉽게 수정할 수 있습니다. 모델을 조회해서 업데이트할 속성을 설정한 뒤 `save`를 호출합니다. `updated_at` 타임스탬프도 자동 갱신됩니다:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<a name="mass-updates"></a>
#### 대량 업데이트

조건에 맞는 모델들을 묶어서 업데이트할 수도 있습니다. 예를 들어 `active` 상태이고 `destination` 컬럼이 `San Diego`인 모든 항공편을 지연 상태로 표시할 때:

```
Flight::where('active', 1)
      ->where('destination', 'San Diego')
      ->update(['delayed' => 1]);
```

`update`는 업데이트할 컬럼과 값을 배열로 받고, 영향을 받은 행의 수를 반환합니다.

> [!NOTE]
> 대량 업데이트 시 Eloquent 모델 인스턴스를 직접 조회하지 않기 때문에, `saving`, `saved`, `updating`, `updated` 같은 모델 이벤트는 발생하지 않습니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 상태 검토

Eloquent 모델은 `isDirty`, `isClean`, `wasChanged` 메서드를 제공하여 모델 속성 변경 여부를 체크할 수 있습니다.

`isDirty`는 조회 이후 변경된 속성이 있는지 확인하며, 특정 속성 이름을 넘겨 해당 속성만 검사할 수도 있습니다. 반대로 `isClean`은 변경되지 않은 속성인지 판단합니다:

```
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty();           // true (변경된 속성이 있음)
$user->isDirty('title');    // true
$user->isDirty('first_name'); // false

$user->isClean();           // false
$user->isClean('title');    // false
$user->isClean('first_name'); // true

$user->save();

$user->isDirty();           // false
$user->isClean();           // true
```

`wasChanged`는 마지막 `save` 호출 이후 변경된 속성이 있는지 확인합니다. 특정 속성 이름을 넘길 수도 있습니다:

```
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged();          // true
$user->wasChanged('title');   // true
$user->wasChanged('first_name'); // false
```

`getOriginal`은 최초 조회 시 모델의 원래 속성값들을 배열로 반환하며, 특정 속성 원값만 얻을 수도 있습니다:

```
$user = User::find(1);

$user->name;          // 현재 값, 예: John
$user->email;         // john@example.com

$user->name = "Jack";
$user->name;          // 변경 후 값: Jack

$user->getOriginal('name'); // 원래 값: John
$user->getOriginal();       // 전체 원래 속성 배열
```

<a name="mass-assignment"></a>
### 대량 할당

`create` 메서드는 한 번에 새 모델을 저장할 수 있지만, 이 때 모델에 `$fillable` 또는 `$guarded` 속성 중 하나가 정의되어 있어야 합니다. 이는 기본적으로 모든 Eloquent 모델이 대량 할당(HTTP 요청에서 의도치 않은 필드로 DB 컬럼이 변경되는 공격)에 취약하지 않도록 보호되기 때문입니다.

악의적인 사용자가 `is_admin` 같은 필드를 요청에 끼워 넣어 권한을 획득하는 상황을 방지하기 위해 명시적으로 대량 할당 가능한 속성을 제한해야 합니다.

먼저, 모델의 `$fillable`에 허용할 속성을 지정합니다. 예를 들어 `Flight` 모델에서 `name` 속성을 허용하려면 다음과 같이 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용된 속성들.
     *
     * @var array
     */
    protected $fillable = ['name'];
}
```

이후 `create` 메서드를 사용할 수 있습니다:

```
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면 `fill` 메서드로 여러 속성을 한 번에 채울 수 있습니다:

```
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 대량 할당할 때는 각 키에 대해 `$fillable`에 명시적으로 적어주어야 합니다. 보안을 위해 `guarded` 속성 사용 시 중첩 JSON 속성 업데이트는 지원하지 않습니다:

```
/**
 * 대량 할당이 허용된 속성들.
 *
 * @var array
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 허용

모든 속성을 대량 할당 가능하게 하려면 모델의 `$guarded` 속성을 빈 배열로 설정하면 됩니다. 이렇게 하면 모든 속성이 허용됩니다. 다만 직접 전달하는 배열을 항상 신중히 작성해야 합니다:

```
/**
 * 대량 할당이 금지된 속성들.
 *
 * @var array
 */
protected $guarded = [];
```

<a name="upserts"></a>
### 업서트(Upserts)

기존 레코드가 있으면 업데이트하고, 없으면 새로 생성해야 할 때가 있습니다. `updateOrCreate` 메서드는 주어진 조건에 맞는 레코드를 찾고, 있으면 두 번째 인자로 넘긴 값으로 업데이트하며, 없으면 새로 생성 후 저장합니다.

예:

```
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

한 번에 여러 개의 업서트를 하고 싶다면 `upsert` 메서드를 사용하세요. 첫 번째 인자로 삽입/업데이트할 데이터를, 두 번째 인자로 고유 식별 컬럼을, 세 번째 인자로 기존 레코드가 있을 때 업데이트할 컬럼들을 배열로 넘깁니다. 타임스탬프도 자동으로 설정됩니다:

```
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

<a name="deleting-models"></a>
## 모델 삭제

모델 인스턴스에서 `delete` 메서드를 호출하면 해당 모델을 삭제할 수 있습니다:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

모델에 대응되는 모든 레코드를 삭제하고 자동 증가 ID도 초기화하려면 `truncate` 메서드를 사용합니다:

```
Flight::truncate();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 삭제

위 예제에서는 모델 먼저 조회 후 삭제했지만, 기본 키만 알면 `destroy` 메서드로 직접 삭제할 수 있습니다. 하나 이상의 키, 배열, 컬렉션도 인수로 받을 수 있습니다:

```
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

> [!NOTE]
> `destroy`는 각 모델을 개별 조회한 뒤 `delete`를 호출해 `deleting` 및 `deleted` 이벤트가 적절히 발생하게 합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

조건에 맞는 모델을 쿼리로 삭제할 수도 있습니다. 예를 들어 `active`가 0인 모든 비활성 항공편을 삭제할 때:

```
$deleted = Flight::where('active', 0)->delete();
```

> [!NOTE]
> 대량 삭제에서 모델 이벤트(`deleting`, `deleted`)는 발생하지 않습니다. 이는 모델을 직접 조회하지 않고 삭제하기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 실제로 레코드를 삭제하지 않고 "삭제된 것처럼" 표시하는 소프트 삭제 기능을 제공합니다. 소프트 삭제된 모델은 DB에 남아있지만 `deleted_at` 속성에 삭제 일시가 기록됩니다. 소프트 삭제를 사용하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레잇을 추가하세요:

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

> [!TIP]
> `SoftDeletes` 트레잇은 `deleted_at` 문자열을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 캐스팅해줍니다.

또한 DB 테이블에 `deleted_at` 컬럼을 추가하는 마이그레이션 코드를 작성해야 합니다. Laravel 스키마 빌더에 `softDeletes` 메서드가 준비되어 있습니다:

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

이제 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 시간으로 설정되고, DB 레코드는 삭제되지 않은 상태로 남습니다. 소프트 삭제를 사용하는 모델 쿼리는 자동으로 삭제된 레코드를 제외합니다.

특정 모델이 소프트 삭제된 상태인지 확인하려면 `trashed` 메서드를 사용하세요:

```
if ($flight->trashed()) {
    //
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원

가끔 소프트 삭제된 모델을 다시 활성화하고 싶을 수 있습니다. 모델 인스턴스에서 `restore` 메서드를 호출하면 `deleted_at`을 `null`로 설정해 복원합니다:

```
$flight->restore();
```

복수 모델을 한꺼번에 복원하려면 쿼리에서 `restore`를 호출할 수도 있습니다(이 경우 모델 이벤트는 발생하지 않습니다):

```
Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();
```

관계 쿼리에서도 `restore`가 가능합니다:

```
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

모델을 완전히 삭제하려면 `forceDelete` 메서드를 사용합니다. 소프트 삭제된 모델을 DB에서 영구 삭제할 때 유용합니다:

```
$flight->forceDelete();
```

관계 쿼리에서도 사용할 수 있습니다:

```
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함하기

앞서 말했듯이, 소프트 삭제된 레코드는 기본적으로 조회 결과에 포함되지 않습니다. 하지만 `withTrashed` 메서드를 쓰면 소프트 삭제된 모델도 조회할 수 있습니다:

```
use App\Models\Flight;

$flights = Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
```

관계 쿼리에서도 호출할 수 있습니다:

```
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회하기

`onlyTrashed` 메서드는 오직 소프트 삭제된 모델만 조회합니다:

```
$flights = Flight::onlyTrashed()
                ->where('airline_id', 1)
                ->get();
```

<a name="pruning-models"></a>
## 모델 프루닝 (Pruning)

가끔 더 이상 필요 없는 모델들을 주기적으로 삭제하고 싶을 때, `Illuminate\Database\Eloquent\Prunable` 또는 `MassPrunable` 트레잇을 모델에 추가하면 됩니다. 트레잇 추가 후, 삭제 대상 모델을 반환하는 `prunable` 메서드를 구현하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * 삭제 대상 모델 쿼리 반환.
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

프루닝 전에 추가 작업을 하고 싶다면 모델에 `pruning` 메서드를 정의할 수 있습니다. 예를 들어, 삭제 전에 연관 파일을 삭제하는 등의 작업에 유용합니다:

```
/**
 * 프루닝 전 준비 작업.
 *
 * @return void
 */
protected function pruning()
{
    //
}
```

모델 프루닝 작업을 앱 콘솔 커널의 스케줄러에 등록하는 것을 잊지 마세요. 원하는 주기로 실행하도록 설정하세요:

```
/**
 * 애플리케이션 명령 스케줄 정의.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('model:prune')->daily();
}
```

`model:prune` 명령은 기본적으로 `app/Models` 내의 Prunable 모델을 자동 탐지하지만, 모델이 다른 위치에 있다면 `--model` 옵션으로 클래스 이름들을 지정할 수 있습니다:

```
$schedule->command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

반대로 특정 모델은 제외하고 모두 프루닝하려면 `--except` 옵션을 사용하세요:

```
$schedule->command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션으로 실제로 삭제하지 않고 몇 건이 삭제될지 시뮬레이션해 볼 수 있습니다:

```
php artisan model:prune --pretend
```

> [!NOTE]
> 프루닝 대상인 소프트 삭제 모델은 실제 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 프루닝 Mass Pruning

`MassPrunable` 트레잇을 사용하면 모델을 직접 조회하지 않고 쿼리를 이용해 대량 삭제합니다. 따라서 `pruning` 메서드와 모델 이벤트는 실행되지 않습니다. 대량 삭제로 효율을 크게 높일 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * 삭제 대상 모델 쿼리 반환.
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델을 기반으로 저장되지 않은 복사본을 만들고 싶다면 `replicate` 메서드를 사용합니다. 여러 속성이 같은 모델을 새로 만들 때 편리합니다:

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

복제할 때 제외할 속성이 있으면 배열로 넘길 수 있습니다:

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
### 글로벌 스코프

글로벌 스코프는 해당 모델의 모든 쿼리에 조건을 강제하는 기능입니다. 예를 들어, Laravel의 소프트 삭제 기능은 글로벌 스코프를 이용해 "삭제되지 않은" 모델만 조회하게 만듭니다. 자신만의 글로벌 스코프를 작성하면 특정 모델 쿼리에 공통 조건을 편리하게 적용할 수 있습니다.

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성법

글로벌 스코프는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현한 클래스로 작성합니다. Laravel은 스코프 클래스를 어디에 두어야 한다고 강제하지 않으니, 원하는 위치에 두시면 됩니다.

`Scope` 인터페이스는 `apply` 메서드만 구현하면 됩니다. 쿼리 빌더에 `where` 같은 조건을 추가할 수 있습니다:

```
<?php

namespace App\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 Eloquent 쿼리 빌더에 스코프를 적용합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $builder
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @return void
     */
    public function apply(Builder $builder, Model $model)
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!TIP]
> 스코프가 쿼리의 `select` 칼럼을 수정한다면 `select` 대신 `addSelect`를 사용해야 기존 쿼리의 선택된 칼럼이 덮어쓰이지 않습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 등록

모델에 글로벌 스코프를 추가하려면, 모델의 `booted` 메서드를 오버라이드하고 `addGlobalScope` 메서드를 호출하세요. `addGlobalScope`는 스코프 인스턴스를 받습니다:

```
<?php

namespace App\Models;

use App\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
     *
     * @return void
     */
    protected static function booted()
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

이렇게 등록된 스코프가 있으면 `User::all()`은 다음과 같은 쿼리를 실행합니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

간단한 스코프는 별도 클래스를 만들지 않고 클로저(익명 함수)로 등록할 수도 있습니다. 이때 `addGlobalScope` 호출 시 첫 번째 인자로 문자열 이름을 지정해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
     *
     * @return void
     */
    protected static function booted()
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->subYears(2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 글로벌 스코프 제거하기

특정 쿼리에서 글로벌 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용합니다. 인자로 스코프 클래스 이름이나 클로저 등록 시 지정한 문자열을 넘기면 됩니다:

```
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 스코프를 제거하거나 모든 글로벌 스코프를 제거하는 것도 가능합니다:

```
// 모든 글로벌 스코프 제거...
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 쓰는 쿼리 조건을 모델에 메서드로 정의해 재활용할 수 있게 합니다. 모델 메서드 이름 앞에 `scope` 접두사를 붙여 만듭니다.

스코프 메서드는 항상 같은 쿼리 빌더 인스턴스나 `void`를 반환해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 있는 사용자만 포함하는 스코프.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopePopular($query)
    {
        return $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 포함하는 스코프.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return void
     */
    public function scopeActive($query)
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용법

스코프 정의 후에는 `scope` 접두사 없이 이름만으로 호출할 수 있습니다. 스코프들을 메서드 체이닝으로 이어서 사용할 수도 있습니다:

```
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조건으로 여러 스코프를 조합할 때는 클로저를 써서 논리 그룹화를 해줘야 할 수 있습니다:

```
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 Laravel은 더 간편하게 하려 `orWhere` 고차 메서드를 지원해, 클로저 없이도 연결할 수 있습니다:

```
$users = App\Models\User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프 (파라미터 있는 스코프)

스코프에 매개변수를 추가하고 싶으면, `$query` 인자 뒤에 원하는 인자를 추가하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 유형의 사용자만 조회하는 스코프.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @param  mixed  $type
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopeOfType($query, $type)
    {
        return $query->where('type', $type);
    }
}
```

호출 시 인자를 전달하세요:

```
$users = User::ofType('admin')->get();
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 같은지 비교할 때 `is`와 `isNot` 메서드를 씁니다. 두 모델이 같은 기본 키, 테이블, DB 연결을 갖는지 비교할 때 편리합니다:

```
if ($post->is($anotherPost)) {
    //
}

if ($post->isNot($anotherPost)) {
    //
}
```

이 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` 같은 관계에서도 쓸 수 있습니다. 관련된 모델과 비교할 때 유용합니다:

```
if ($post->author()->is($user)) {
    //
}
```

<a name="events"></a>
## 이벤트

> [!TIP]
> Eloquent 이벤트를 클라이언트 애플리케이션으로 직접 브로드캐스트하려면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/{{version}}/broadcasting#model-broadcasting) 기능을 확인하세요.

Eloquent 모델은 여러 이벤트를 발생시키며, 모델 생명주기 중 다음과 같은 순간에 훅을 걸 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 기존 모델이 DB에서 조회될 때 발생
- `creating` / `created`: 새 모델이 최초로 저장될 때 발생
- `updating` / `updated`: 기존 모델이 수정되고 저장될 때 발생
- `saving` / `saved`: 모델 생성 혹은 업데이트 시 항상 발생 (속성 변경 여부와 무관)
- `-ing`로 끝나는 이벤트는 데이터가 DB에 반영되기 전, `-ed`는 DB 반영 후 발생

모델 이벤트를 수신하려면, 모델에 `$dispatchesEvents` 프로퍼티를 정의해 각 이벤트에 대응하는 커스텀 [이벤트 클래스](/docs/{{version}}/events)를 맵핑하세요. 이벤트 클래스는 생성자에서 영향을 받은 모델 인스턴스를 받습니다:

```
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 모델 이벤트와 연결된 이벤트 클래스 매핑.
     *
     * @var array
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트가 준비되면 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)를 작성해 처리할 수 있습니다.

> [!NOTE]
> 대량 갱신이나 삭제 시 모델을 직접 조회하지 않으므로, `saved`, `updated`, `deleting`, `deleted` 모델 이벤트는 발생하지 않습니다.

<a name="events-using-closures"></a>
### 클로저를 사용하는 이벤트

커스텀 이벤트 클래스 대신, 모델 이벤트에 클로저를 등록해 실행할 수도 있습니다. 보통 모델의 `booted` 메서드 안에 등록합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드.
     *
     * @return void
     */
    protected static function booted()
    {
        static::created(function ($user) {
            //
        });
    }
}
```

필요하면 [큐 가능 익명 이벤트 리스너](/docs/{{version}}/events#queuable-anonymous-event-listeners)를 사용해 비동기로 처리할 수도 있습니다:

```
use function Illuminate\Events\queueable;

static::created(queueable(function ($user) {
    //
}));
```

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의

모델 이벤트가 많다면 옵저버 클래스로 묶어서 관리할 수 있습니다. 옵저버 메서드 이름은 대응하는 Eloquent 이벤트와 같으며, 해당 이벤트가 발생한 모델 인스턴스를 인자로 받습니다. 옵저버 클래스는 `make:observer` Artisan 명령으로 쉽게 생성할 수 있습니다:

```
php artisan make:observer UserObserver --model=User
```

기본적으로 `App/Observers` 디렉토리에 옵저버를 생성하며, 없으면 디렉토리를 만듭니다. 생성된 기본 옵저버 예:

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User가 생성됐을 때 이벤트 처리.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function created(User $user)
    {
        //
    }

    /**
     * User가 업데이트됐을 때 이벤트 처리.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function updated(User $user)
    {
        //
    }

    /**
     * User가 삭제됐을 때 이벤트 처리.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function deleted(User $user)
    {
        //
    }

    /**
     * User가 강제 삭제됐을 때 이벤트 처리.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function forceDeleted(User $user)
    {
        //
    }
}
```

옵저버를 등록하려면 앱의 `App\Providers\EventServiceProvider` 내 `boot` 메서드에서 모델의 `observe` 메서드로 연결하세요:

```
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 이벤트 등록.
 *
 * @return void
 */
public function boot()
{
    User::observe(UserObserver::class);
}
```

> [!TIP]
> 옵저버는 `saving`, `retrieved` 등 더 많은 이벤트도 감지할 수 있으며, 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

트랜잭션 내에서 모델이 생성될 때, 옵저버 이벤트 핸들러가 트랜잭션 커밋 후에 실행되도록 `$afterCommit` 프로퍼티를 옵저버에 설정할 수 있습니다. 트랜잭션이 없으면 핸들러는 즉시 실행됩니다:

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * 모든 트랜잭션 커밋 후 이벤트 처리 여부.
     *
     * @var bool
     */
    public $afterCommit = true;

    /**
     * User가 생성됐을 때 이벤트 처리.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function created(User $user)
    {
        //
    }
}
```

<a name="muting-events"></a>
### 이벤트 비활성화

일시적으로 모델 이벤트를 비활성화하고 싶을 때, `withoutEvents` 메서드를 사용하세요. 이 메서드는 클로저를 인자로 받으며, 클로저 내에서 발생하는 모델 이벤트는 모두 비활성화됩니다. 클로저의 반환값은 다시 `withoutEvents`의 반환값이 됩니다:

```
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 모델 저장하기

특정 모델을 이벤트 없이 저장하려면 `saveQuietly` 메서드를 활용하세요:

```
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```