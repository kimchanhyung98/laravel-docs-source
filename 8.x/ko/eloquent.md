# Eloquent: 시작하기

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본키](#primary-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성값](#default-attribute-values)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청킹](#chunking-results)
    - [게으른 결과 스트리밍](#streaming-results-lazily)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [일괄 할당](#mass-assignment)
    - [업서트](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제 모델 조회](#querying-soft-deleted-models)
- [모델 가지치기](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [전역 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)


<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와의 상호작용을 즐겁게 만들어주는 객체-관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때 각 데이터베이스 테이블은 해당 테이블과 상호작용하는 "모델"과 연결됩니다. Eloquent 모델을 통해 데이터 조회 뿐만 아니라, 레코드의 삽입, 수정, 삭제도 할 수 있습니다.

> {tip} 시작하기 전에, 반드시 애플리케이션의 `config/database.php` 구성 파일에서 데이터베이스 연결을 설정해야 합니다. 데이터베이스 구성에 대한 자세한 정보는 [데이터베이스 설정 문서](/docs/{{version}}/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

우선, Eloquent 모델을 생성해봅시다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 아래 Artisan [명령어](/docs/{{version}}/artisan)를 사용하여 새 모델을 생성할 수 있습니다:

    php artisan make:model Flight

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

    php artisan make:model Flight --migration

모델 생성 시 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 등 다양한 클래스도 함께 생성할 수 있습니다. 이런 옵션들을 조합하여 여러 클래스를 동시에 만들 수도 있습니다:

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

# 모델, FlightController 리소스 클래스, 폼 리퀘스트 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모든 구성요소(모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트)를 한 번에 생성...
php artisan make:model Flight --all

# 피벗 모델 생성...
php artisan make:model Member --pivot
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙

`make:model` 명령으로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 기본 모델 클래스를 살펴보고 주요 Eloquent 관례를 알아봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    //
}
```

<a name="table-names"></a>
### 테이블명

위 예제에서 `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 명시하지 않았다는 점을 눈치채셨을 수도 있습니다. 관례상, 클래스의 "스네이크 케이스(snake case)" 복수형 이름이 테이블명으로 사용됩니다. 즉, `Flight` 모델은 기본적으로 `flights` 테이블을, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블을 사용합니다.

만약 모델에 해당하는 데이터베이스 테이블명이 이 관례를 따르지 않는다면, 모델에 `table` 속성을 명시적으로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 연결된 테이블명
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본키

Eloquent는 각 모델의 데이터베이스 테이블에 `id`라는 이름의 기본키 컬럼이 있다고 가정합니다. 필요하다면, 모델 클래스에서 보호된 `$primaryKey` 속성으로 기본키 컬럼명을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블의 기본키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, Eloquent는 기본키가 증가하는 정수값이라고 가정하여 자동으로 기본키를 정수형으로 캐스팅합니다. 자동 증가하지 않거나 숫자가 아닌 기본키를 사용하려면, 모델의 공개 속성 `$incrementing`을 `false`로 지정해야 합니다:

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

기본키가 정수가 아니라면, 모델의 보호된 `$keyType` 속성을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 자동 증가 ID의 데이터 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본키

Eloquent는 각 모델에 기본키 역할을 할 고유 "ID"가 최소 하나 있어야 합니다. "복합" 기본키(여러 컬럼의 조합)는 Eloquent에서 지원하지 않습니다. 다만, 테이블에 고유 인덱스를 추가할 수는 있습니다.

<a name="timestamps"></a>
### 타임스탬프

기본적으로 Eloquent는 모델에 해당하는 데이터베이스 테이블에 `created_at`과 `updated_at` 컬럼이 존재한다고 가정합니다. 모델이 생성 또는 수정될 때 이 컬럼이 자동으로 관리됩니다. 만약 Eloquent가 이 컬럼을 자동 관리하지 않게 하려면, 모델에서 `$timestamps` 속성을 `false`로 지정하면 됩니다:

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

모델의 타임스탬프 형식을 커스터마이징하려면 `$dateFormat` 속성을 설정할 수 있습니다. 이 속성은 DB 저장형식과 배열 혹은 JSON 변환시 사용할 형식 모두를 제어합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 컬럼의 저장 형식
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 변경하고 싶다면 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의하세요:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션의 기본 데이터베이스 연결을 사용합니다. 특정 모델이 다른 연결을 사용하도록 하려면 `$connection` 속성을 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 데이터베이스 연결명
     *
     * @var string
     */
    protected $connection = 'sqlite';
}
```

<a name="default-attribute-values"></a>
### 기본 속성값

새로 생성된 모델 인스턴스에는 기본적으로 아무 속성값도 없습니다. 일부 속성에 대해 기본값을 지정하려면, 모델의 `$attributes` 속성을 사용할 수 있습니다:

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
        'delayed' => false,
    ];
}
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연결된 데이터베이스 테이블](/docs/{{version}}/migrations#writing-migrations)을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/{{version}}/queries)로서 동작하며, 유창하게 모델과 연결된 테이블을 조회할 수 있습니다. 모델의 `all` 메서드는 테이블의 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

Eloquent의 `all` 메서드는 모델 테이블의 모든 결과를 반환합니다. 각 모델이 [쿼리 빌더](/docs/{{version}}/queries) 역할도 하므로 추가 조건을 적용한 뒤 `get` 메서드를 호출할 수 있습니다:

```php
$flights = Flight::where('active', 1)
               ->orderBy('name')
               ->take(10)
               ->get();
```

> {tip} Eloquent 모델은 쿼리 빌더이므로 Laravel의 [쿼리 빌더](/docs/{{version}}/queries) 메서드들을 자유롭게 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로 고침

DB에서 조회한 모델 인스턴스가 이미 있다면, `fresh` 및 `refresh` 메서드로 모델을 "새로 고침"할 수 있습니다. `fresh`는 모델의 새 인스턴스를 DB에서 다시 조회한 결과로 생성합니다. 기존 인스턴스에는 영향을 주지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 모델 인스턴스를 DB의 데이터를 사용해 다시 채웁니다. 이미 로딩된 관계도 함께 새로 고쳐집니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

Eloquent의 `all`, `get`과 같은 메서드를 통해 여러 레코드를 조회할 수 있습니다. 이 메서드들은 일반 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 상속하며, [다양한 도움 메서드들](/docs/{{version}}/collections#available-methods)을 제공합니다. 예를 들어, `reject` 메서드를 사용해 콜백의 결과에 따라 컬렉션에서 모델을 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function ($flight) {
    return $flight->cancelled;
});
```

기본 컬렉션 메서드 외에도, Eloquent 컬렉션에는 [특정 Eloquent 모델 컬렉션을 위한 추가 메서드](/docs/{{version}}/eloquent-collections#available-methods)들이 있습니다.

Laravel의 모든 컬렉션은 PHP의 반복자 인터페이스를 구현하므로 배열처럼 순회할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청킹(Chunking)

`all`이나 `get`으로 수만 개의 Eloquent 모델을 한 번에 읽으면 메모리가 바닥날 수 있습니다. 대신 `chunk` 메서드를 사용하면 대량의 모델을 효율적으로 처리할 수 있습니다.

`chunk`는 일정 개수만큼의 모델을 클로저로 넘겨줍니다. 각 청크만 메모리에 로드하므로 훨씬 적은 메모리로 다룰 수 있습니다:

```php
use App\Models\Flight;

Flight::chunk(200, function ($flights) {
    foreach ($flights as $flight) {
        //
    }
});
```

첫번째 인자는 청크당 레코드 수입니다. 두번째 인자로 전달된 클로저는 데이터베이스로부터 각 청크별로 호출됩니다.

청킹 도중 결과 컬럼을 변경하면서 반복적으로 수정한다면 `chunkById` 메서드를 사용해야 예기치 않은 결과를 방지할 수 있습니다. `chunkById`는 이전 청크의 마지막 모델의 `id`보다 큰 모델만 가져옵니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function ($flights) {
        $flights->each->update(['departed' => false]);
    }, $column = 'id');
```

<a name="streaming-results-lazily"></a>
### 게으른 결과 스트리밍

`lazy` 메서드는 [chunk](#chunking-results)처럼 내부적으로 쿼리를 청크 단위로 실행합니다. 그러나 각 청크를 콜백에 즉시 넘기는 대신, 단일 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)으로 플랫하게 반환합니다. 이를 통해 단일 스트림으로 결과를 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    //
}
```

`lazy`의 결과 컬럼을 변경하면서 반복/수정할 경우에는 `lazyById` 메서드를 사용하세요. `lazyById`는 이전 청크의 마지막 모델의 `id`보다 큰 모델만 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, $column = 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용해 `id`의 내림차순으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서

`lazy`와 유사하게, `cursor` 메서드를 사용하면 메모리 소비를 크게 줄일 수 있습니다.

`cursor`는 단일 쿼리만 실행하지만, 실제로 반복할 때만 각각의 Eloquent 모델을 생성합니다. 따라서 한 번에 하나의 모델만 메모리에 남게 됩니다.

> {note} `cursor`는 한 번에 하나의 모델만 메모리에 유지하므로 관계를 eager load 할 수 없습니다. eager load가 필요하다면 [lazy 메서드](#streaming-results-lazily)를 사용하세요.

내부적으로 PHP의 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    //
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/{{version}}/collections#lazy-collections)은 일반 컬렉션과 유사하게 다양한 메서드를 제공하지만, 한 번에 한 모델만 메모리에 로드됩니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

단, `cursor`도 결국에는 [PHP의 PDO 드라이버가 모든 결과를 내부적으로 버퍼에 캐싱](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)하기 때문에 엄청난 레코드에서는 한계가 있습니다. 매우 많은 데이터라면 [lazy 메서드](#streaming-results-lazily)를 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 select

Eloquent는 고급 서브쿼리도 지원하여 관련 테이블의 정보도 한 번에 가져올 수 있습니다. 예를 들어, 비행 `destinations` 테이블과 해당 목적지로 가는 `flights` 테이블이 있다고 가정해 봅시다. 각 flight는 도착시각(`arrived_at`) 컬럼을 가지고 있습니다.

`select` 및 `addSelect`의 서브쿼리 기능을 활용하면, 하나의 쿼리로 각 목적지별 최종 비행기명을 조회할 수 있습니다:

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

또한, 쿼리 빌더의 `orderBy`에 서브쿼리를 사용할 수 있습니다. 위의 예시로, 목적지별 마지막 도착 비행시간으로 모든 목적지를 정렬할 수 있습니다:

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

조건에 맞는 모든 레코드 뿐만 아니라, `find`, `first`, `firstWhere` 같은 메서드로 단일 레코드도 조회할 수 있습니다. 이 메서드들은 컬렉션 대신 한 건의 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본키로 모델 조회
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// 대안
$flight = Flight::firstWhere('active', 1);
```

쿼리의 첫 결과를 조회하거나, 결과가 없으면 특정 동작을 하고 싶다면 `firstOr` 메서드를 사용할 수 있습니다. 결과가 없으면 주어진 클로저를 실행해 반환 값을 결과로 사용합니다:

```php
$model = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Not Found 예외

모델이 조회되지 않을 때 예외를 던질 수도 있습니다. 라우트나 컨트롤러에서 유용합니다. `findOrFail`, `firstOrFail`은 결과가 없을 때 `Illuminate\Database\Eloquent\ModelNotFoundException`을 던집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외를 캐치하지 않으면 클라이언트에 404 HTTP 응답이 반환됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function ($id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 값이 일치하는 레코드가 있으면 가져오고, 없으면 새로 만들어 저장합니다. 첫 번째 배열에 탐색 조건을, 두 번째 배열에 추가 속성을 넘길 수 있습니다.

`firstOrNew`는 레코드가 없을 경우 새 모델 인스턴스를 반환(저장 안함)하므로, 수동으로 `save` 메서드를 호출해야 합니다:

```php
use App\Models\Flight;

// 없는 경우 새로 생성하여 저장
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 추가 속성도 함께
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 없는 경우 새 인스턴스만 반환(저장X)
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

모델에서 Eloquent의 `count`, `sum`, `max`와 같은 [집계 메서드](/docs/{{version}}/queries#aggregates)를 사용할 수 있습니다. 이 메서드들은 한 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때 모델에 새 레코드를 삽입하는 과정도 간단합니다. 새 모델 인스턴스를 만들고, 속성값을 지정한 뒤 `save`를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새 비행을 데이터베이스에 저장
     */
    public function store(Request $request)
    {
        // 요청 검증...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();
    }
}
```

이 예제에서는 입력된 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name`에 할당했습니다. `save`를 호출하면 레코드가 저장되고, `created_at`, `updated_at`은 자동으로 관리됩니다.

또는 `create` 메서드를 사용해 PHP 한 줄로 새 모델을 저장할 수 있습니다. `create`는 저장된 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create`를 사용하기 전 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이는 대량 할당 취약점 방지를 위해 모든 Eloquent 모델에 기본 적용됩니다. 자세한 내용은 [일괄 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

`save`는 이미 존재하는 모델의 수정에도 사용할 수 있습니다. 모델을 가져와 수정할 속성을 지정한 후 `save`를 호출하면, `updated_at` 값도 자동으로 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<a name="mass-updates"></a>
#### 일괄 수정

일치하는 모든 모델을 한 번에 수정할 수도 있습니다. 아래 예시에서는 `active`이면서 목적지가 `San Diego`인 모든 비행의 `delayed` 값을 1로 바꿉니다:

```php
Flight::where('active', 1)
      ->where('destination', 'San Diego')
      ->update(['delayed' => 1]);
```

`update`는 컬럼과 값을 짝지은 배열을 기대하며, 영향을 받은 행의 수를 반환합니다.

> {note} 일괄 업데이트 시 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. 모델을 조회없이 직접 수정하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 확인

Eloquent에는 모델의 내부 상태와 속성이 언제, 어떻게 바뀌었는지 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드가 있습니다.

`isDirty`는 인스턴스를 처음 조회한 이후 속성이 변경되었는지 판별합니다. 인자에 특정 속성명을 넘기면 해당 속성의 dirty 여부를 확인합니다. `isClean`은 변경되지 않은 속성이 있는지 확인합니다(옵션으로 속성명 지정 가능):

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

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```

`wasChanged`는 마지막 저장 시 변경된 속성이 있는지 확인합니다(특정 속성 지정 가능):

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
$user->wasChanged('first_name'); // false
```

`getOriginal`은 조회 이후 변경 여부와 상관없이 모델의 원래 속성값를 반환합니다. 특정 속성명을 전달하면 해당 속성의 원본값만 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = "Jack";
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 모든 원본 속성배열
```

<a name="mass-assignment"></a>
### 일괄 할당(Mass Assignment)

`create` 메서드를 사용해 한 번에 새 모델을 저장할 수 있습니다. 이 때 모델 인스턴스가 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create`를 사용하기 전 반드시 모델 클래스에 `fillable` 또는 `guarded`를 정의해야 합니다. Eloquent는 기본적으로 모든 모델에 대량 할당 취약점 방지를 적용합니다.

대량 할당 취약점이란, 사용자가 예상치 못한 필드를 HTTP 요청에 담아 보내고, 그 값이 개발자가 의도하지 않은 DB 컬럼을 변경하는 상황을 의미합니다. 예를 들어, 악의적인 사용자가 `is_admin`을 HTTP 요청에 넘기면, create 메서드에서 해당 사용자가 관리자로 승격될 수 있습니다.

따라서, 어떤 속성이 대량 할당 가능한지 모델의 `$fillable` 속성에 명시적으로 정의해야 합니다. 예를 들어, `Flight` 모델의 `name` 속성을 회집 할당 가능한 속성으로 등록:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 가능한 속성
     *
     * @var array
     */
    protected $fillable = ['name'];
}
```

지정 후에는 `create`로 바로 저장할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드로 여러 속성을 한 번에 할당할 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 일괄 할당 & JSON 컬럼

JSON 컬럼에 할당할 때도, 각 column을 `$fillable` 배열에 명시해야 합니다. `guarded` 사용 시에는 중첩 JSON 속성을 일괄 할당할 수 없습니다:

```php
/**
 * 대량 할당 가능한 속성
 *
 * @var array
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 일괄 할당 전체 허용

모든 속성을 대량 할당 가능하게 하려면, 모델의 `$guarded`를 빈 배열로 지정하세요. 단, 이 경우에는 `fill`, `create`, `update`시 전달하는 배열을 반드시 수작업으로 직접 구성해야 합니다:

```php
/**
 * 대량 할당을 막을 속성(없음)
 *
 * @var array
 */
protected $guarded = [];
```

<a name="upserts"></a>
### 업서트(Upserts)

기존 모델을 업데이트 하거나, 없으면 새로 만들고 싶을 때는 `updateOrCreate` 메서드를 사용하세요. 이 메서드는 자동으로 저장까지 해줍니다.

아래 예시에서는 `departure`가 `Oakland`이면서 `destination`이 `San Diego`인 항공편이 있으면 `price`와 `discounted`를 수정, 없으면 새 모델을 생성합니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

여러 레코드를 한 쿼리에서 처리하려면 `upsert`를 사용합니다. 첫 번째 인자는 삽입/수정할 값 배열, 두 번째는 고유 식별 컬럼, 세 번째는 이미 있을 때 수정할 컬럼 배열입니다. 자동으로 `created_at`, `updated_at`이 갱신됩니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

<a name="deleting-models"></a>
## 모델 삭제

모델 인스턴스의 `delete` 메서드를 호출하면 해당 레코드가 삭제됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

`truncate` 메서드는 모델과 연결된 모든 레코드를 한꺼번에 삭제하고, auto-increment ID도 리셋합니다:

```php
Flight::truncate();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 모델 삭제

위에서는 모델을 조회해서 지우지만, 기본키를 알고 있다면 모델 인스턴스 없이도 `destroy`로 삭제할 수 있습니다. 여러 개도 가능하며, 배열이나 [컬렉션](/docs/{{version}}/collections)도 쓸 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

> {note} `destroy`는 각 모델을 개별적으로 조회해 `delete`를 호출하므로, 각 모델마다 `deleting`, `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

조건에 맞는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래는 `active`가 0인 비행을 모두 삭제합니다. 일괄 삭제시 모델 이벤트가 발생하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```

> {note} Eloquent를 통한 일괄 삭제 시 `deleting`, `deleted` 모델 이벤트는 발생하지 않습니다. (모델 인스턴스 없이 바로 삭제함)

<a name="soft-deleting"></a>
### 소프트 삭제

실제 DB에서 레코드를 제거하지 않고, 삭제된 것처럼 처리하고 싶다면 Eloquent의 "소프트 삭제"를 사용할 수 있습니다. 소프트 삭제 시 실제로는 `deleted_at` 속성에 삭제 시각만 새깁니다. 사용하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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

> {tip} `SoftDeletes` 트레이트는 `deleted_at`을 `DateTime`/`Carbon` 인스턴스로 자동 변환해줍니다.

DB 테이블에도 `deleted_at` 컬럼이 있어야 합니다. [스키마 빌더](/docs/{{version}}/migrations)에서 쉽게 추가할 수 있습니다:

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

이제 `delete`를 호출하면 `deleted_at`만 변경되고, 레코드는 테이블에 남아있습니다. 소프트 삭제 모델은 기본적으로 쿼리 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    //
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 복원

소프트 삭제 모델을 복원(undelete)하려면 `restore`를 호출하세요. 이 메서드는 `deleted_at`을 `null`로 되돌립니다:

```php
$flight->restore();
```

쿼리로 복원도 가능합니다(이 경우 모델 이벤트는 일괄 삭제와 마찬가지로 발생하지 않습니다):

```php
Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();
```

관계 쿼리에서도 `restore`를 사용할 수 있습니다:

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

소프트 삭제 모델을 실제로 영구적으로 DB에서 제거하고 싶다면 `forceDelete`를 사용하세요:

```php
$flight->forceDelete();
```

관계 쿼리에서도 적용 가능합니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 포함

기본적으로 소프트 삭제 모델은 쿼리에서 제외됩니다. 포함시키고 싶다면, 쿼리에서 `withTrashed`를 호출하세요:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
```

관계 쿼리에서도 사용할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed`는 소프트 삭제된 모델만 반환합니다:

```php
$flights = Flight::onlyTrashed()
                ->where('airline_id', 1)
                ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning)

더 이상 필요하지 않은 모델을 주기적으로 삭제하려면, 해당 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하세요. 그리고 `prunable` 메서드를 구현하여 가지치기 기준을 반환하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * 가지치기할 모델의 쿼리
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable` 지정 시, `pruning` 메서드도 구현할 수 있습니다. 이 메서드는 모델이 삭제되기 전 호출되며, 저장된 파일 등 연관 리소스를 삭제하는 데 쓸 수 있습니다:

```php
/**
 * 가지치기 전 처리
 */
protected function pruning()
{
    //
}
```

가지치기 모델을 셋업했다면, `App\Console\Kernel`의 스케쥴에 `model:prune` Artisan 명령을 등록하세요:

```php
/**
 * 명령 스케쥴 정의
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('model:prune')->daily();
}
```

명령어는 자동으로 `app/Models` 내 "Prunable" 모델을 감지합니다. 모델 위치가 다르면 `--model` 옵션을 통해 지정할 수 있습니다:

```php
$schedule->command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

가지치기 제외할 모델이 있다면 `--except` 옵션을 활용하세요:

```php
$schedule->command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션으로 가지치기 결과를 시뮬레이션(test)할 수 있습니다(실제 삭제X):

```bash
php artisan model:prune --pretend
```

> {note} 소프트 삭제 모델은 prunable 쿼리에 일치하면 영구적으로(`forceDelete`) 삭제됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기

`MassPrunable` 트레이트를 지정하면 모델을 대량 삭제 쿼리로 처리합니다. 이 경우 `pruning` 메서드나 이벤트가 호출되지 않아 가지치기 효율이 매우 높습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * 가지치기할 모델의 쿼리
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스의 복사본을 만들어 저장하지 않고 생성하려면 `replicate` 메서드를 사용하세요. 비슷한 속성값을 가진 새 모델을 만들 때 유용합니다:

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

복제에서 제외할 속성이 있다면 배열로 지정할 수 있습니다:

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

전역 스코프는 특정 모델에 대한 모든 쿼리에 조건을 자동으로 추가할 수 있습니다. Laravel의 [소프트 삭제](#soft-deleting) 기능도 전역 스코프를 활용합니다.

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성

전역 스코프를 만들려면, `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 만드세요. 파일 위치에는 제약이 없습니다.

`Scope` 인터페이스에는 `apply` 메서드가 있습니다. 이 메서드는 쿼리 빌더에 `where` 등 조건을 추가합니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model)
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> {tip} 전역 스코프에서 쿼리에 select 컬럼을 추가할 땐 기존 select 절을 대체하지 않도록 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용

모델에 전역 스코프를 할당하려면 `booted` 메서드를 오버라이드하고, `addGlobalScope` 메서드로 스코프 인스턴스를 등록하세요:

```php
<?php

namespace App\Models;

use App\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted()
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 스코프 등록 후, `User::all()` 호출시 다음 SQL이 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 클로저 전역 스코프

전역 스코프를 단순히 클로저로 정의할 수도 있습니다. 이 경우 스코프 이름을 첫번째 인자로 넘깁니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected static function booted()
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->subYears(2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 전역 스코프 제거

특정 쿼리에서 전역 스코프를 제거하려면 `withoutGlobalScope`를 사용하세요:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저 스코프의 경우 스코프명을 문자열로 전달합니다:

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 모든 전역 스코프를 제거하려면 `withoutGlobalScopes`를 사용하세요:

```php
// 모든 전역 스코프 제거
User::withoutGlobalScopes()->get();

// 특정 전역 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 쓰는 쿼리 조건을 메서드로 정의해서 재사용할 수 있도록 지원합니다. 메서드명에 `scope` 접두사를 붙여 정의하세요.

스코프 메서드는 쿼리 빌더 인스턴스 또는 void를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자만 필터링
     */
    public function scopePopular($query)
    {
        return $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 필터링
     */
    public function scopeActive($query)
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 활용

정의된 스코프는 쿼리시 scope 접두사 없이 호출합니다. 여러 스코프를 체이닝할 수도 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조합이 필요할 경우, 클로저로 그룹핑할 수 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이 과정을 더 손쉽게 체이닝하려면 Laravel의 "고차 orWhere"를 사용하세요:

```php
$users = App\Models\User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 매개변수를 받으려면, 메서드 시그니처에 `$query` 다음에 인자를 추가해 주세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 유형별 사용자 필터링 스코프
     */
    public function scopeOfType($query, $type)
    {
        return $query->where('type', $type);
    }
}
```

스코프를 호출할 때 인자를 전달할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "동일"한지(기본키, 테이블, 연결이 같은지) 확인하려면 `is`, `isNot` 메서드를 사용하면 됩니다:

```php
if ($post->is($anotherPost)) {
    //
}

if ($post->isNot($anotherPost)) {
    //
}
```

`is`, `isNot`는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](https://laravel.com/docs/{{version}}/eloquent-relationships)에서도 쓸 수 있습니다. 관계 모델을 쿼리없이 비교할 때 유용합니다:

```php
if ($post->author()->is($user)) {
    //
}
```

<a name="events"></a>
## 이벤트

> {tip} Eloquent 이벤트를 프론트엔드로 바로 브로드캐스트하고 싶다면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/{{version}}/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 발생시켜 모델의 라이프사이클 여러 시점에 후킹할 수 있도록 합니다. 가능한 이벤트는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `restoring`, `restored`, `replicating` 등입니다.

* `retrieved` : 모델이 DB에서 조회될 때
* `creating/created` : 모델이 처음 저장될 때
* `updating/updated` : 기존 모델이 수정될 때
* `saving/saved` : 새로 생성 또는 업데이트 될 때(속성 변경 없더라도)
* `-ing` : 변경이 저장되기 **전**
* `-ed` : 변경이 저장된 **후**

모델 이벤트를 리스닝하려면 `$dispatchesEvents` 메서드에 이벤트와 처리할 [이벤트 클래스](/docs/{{version}}/events)를 매핑하세요:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * 모델 이벤트 매핑
     *
     * @var array
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이벤트 매핑 후, [이벤트 리스너](/docs/{{version}}/events#defining-listeners)로 이벤트를 처리할 수 있습니다.

> {note} Eloquent로 일괄 update/delete 쿼리를 실행하는 경우 해당 모델의 이벤트는 발생하지 않습니다(모델을 조회하지 않음).

<a name="events-using-closures"></a>
### 클로저로 이벤트 처리

이벤트 클래스를 직접 만들지 않고, 클로저로 이벤트 핸들러를 등록할 수도 있습니다. 보통 모델의 `booted` 메서드에서 등록합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected static function booted()
    {
        static::created(function ($user) {
            //
        });
    }
}
```

필요하다면 [큐어블 익명 리스너](/docs/{{version}}/events#queuable-anonymous-event-listeners)도 등록할 수 있습니다. 이 경우, 이벤트 리스너는 [큐](/docs/{{version}}/queues)를 통해 백그라운드에서 동작합니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function ($user) {
    //
}));
```

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의

한 모델의 여러 이벤트를 리스닝할 땐 옵저버 클래스에 모아둘 수 있습니다. 메서드명은 Eloquent 이벤트명과 동일하게 작성하세요. 각 메서드는 모델을 인자로 받습니다.

`make:observer` Artisan 명령으로 새 옵저버 클래스를 쉽게 생성할 수 있습니다:

```bash
php artisan make:observer UserObserver --model=User
```

이 명령은 옵저버를 `App/Observers`에 만듭니다(없으면 생성됨). 생성된 옵저버 예시는 다음과 같습니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * 생성 이벤트
     */
    public function created(User $user)
    {
        //
    }

    /**
     * 수정 이벤트
     */
    public function updated(User $user)
    {
        //
    }

    /**
     * 삭제 이벤트
     */
    public function deleted(User $user)
    {
        //
    }

    /**
     * 영구 삭제 이벤트
     */
    public function forceDeleted(User $user)
    {
        //
    }
}
```

옵저버 등록은 모델의 `observe` 메서드를 통해 할 수 있으며, 보통 `App\Providers\EventServiceProvider`의 `boot`에서 등록합니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 이벤트 등록
 */
public function boot()
{
    User::observe(UserObserver::class);
}
```

> {tip} 옵저버는 `saving`, `retrieved` 등 추가 이벤트도 감지할 수 있습니다. [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버 & DB 트랜잭션

모델이 트랜잭션 내에서 생성될 때, 옵저버가 트랜잭션 커밋 후에만 동작하길 원한다면 `$afterCommit` 속성을 옵저버에 지정하세요. 트랜잭션이 없다면 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * 트랜잭션 커밋 후에만 실행
     *
     * @var bool
     */
    public $afterCommit = true;

    public function created(User $user)
    {
        //
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거

일시적으로 모든 모델 이벤트 호출을 "음소거"할 수 있습니다. `withoutEvents` 메서드를 사용하면 전달한 클로저 내의 코드는 이벤트 없이 실행됩니다. 클로저의 반환값이 그대로 리턴됩니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () use () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 이벤트 없이 저장

특정 모델에 대해 이벤트 발생 없이 저장하려면, `saveQuietly`를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```
