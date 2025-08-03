# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성하기](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [청킹(분할 처리) 결과](#chunking-results)
    - [지연 컬렉션을 이용한 청킹](#chunking-using-lazy-collections)
    - [커서 활용](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회하기](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 갱신](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [갱신](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기 (Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 범위 (Scopes)](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 뮤팅](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와 상호작용하기 즐겁도록 만들어진 ORM(Object-Relational Mapper)인 Eloquent를 포함하고 있습니다. Eloquent를 사용하면 각 데이터베이스 테이블마다 해당 테이블과 상호작용하는 데 사용되는 "모델"이 존재합니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, 레코드를 삽입, 수정, 삭제하는 것도 가능합니다.

> [!NOTE]  
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 반드시 데이터베이스 연결을 구성해야 합니다. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 구성 문서](/docs/10.x/database#configuration)를 참고하세요.

#### Laravel 부트캠프

Laravel 초보라면 [Laravel Bootcamp](https://bootcamp.laravel.com)를 자유롭게 이용해 보세요. Bootcamp는 Eloquent를 사용해 첫 Laravel 애플리케이션을 만드는 과정을 안내해 줍니다. Laravel과 Eloquent가 제공하는 모든 기능을 빠르게 익히는 좋은 방법입니다.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기 (Generating Model Classes)

먼저 Eloquent 모델을 만들어 보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/10.x/artisan)를 사용하세요:

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/10.x/migrations) 파일도 함께 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 추가할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 공장(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 리퀘스트(form request) 같은 다양한 클래스를 함께 생성할 수도 있습니다. 이런 옵션은 조합해서 여러 클래스를 한 번에 생성할 수도 있습니다:

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

# 모델, FlightController 리소스 클래스, 폼 리퀘스트 클래스 생성
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 한 번에 생성
php artisan make:model Flight --all

# 피벗 모델 생성
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인하기

모델의 코드만 보고 모델이 가진 속성과 연관관계 전체를 파악하기 어려울 수 있습니다. 이럴 때 `model:show` Artisan 명령어를 사용하면, 모델의 속성과 연관관계에 대한 편리한 개요를 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙 (Eloquent Model Conventions)

`make:model` 명령어로 생성된 모델은 기본적으로 `app/Models` 디렉터리에 위치합니다. 아래 기본 모델 클래스를 살펴보고, Eloquent가 따르는 주요 규칙들에 대해 이야기해 보겠습니다:

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
### 테이블 이름 (Table Names)

위 예제를 보면, `Flight` 모델과 연결된 데이터베이스 테이블 이름을 Eloquent에 따로 알려주지 않았습니다. 기본 규칙으로, 클래스 이름을 스네이크 케이스(snake_case)로 바꾸고 복수형으로 만들어 테이블 이름으로 가정합니다. 따라서 `Flight` 모델은 `flights` 테이블과 연결되고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결됩니다.

모델과 매칭되는 테이블 이름이 이 규칙과 다르다면, 모델 클래스의 `table` 속성을 직접 정의해 테이블 이름을 명시할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연결된 테이블 이름
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키 (Primary Keys)

Eloquent는 기본적으로 각 모델과 연결된 테이블에 `id`라는 이름의 기본 키 칼럼이 있다고 가정합니다. 만약 기본 키 칼럼 이름이 다르다면, 모델 클래스에 보호된 `$primaryKey` 속성을 정의해 변경할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블과 연결된 기본 키 칼럼 이름
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 Eloquent는 기본 키가 자동 증가하는 정수형이라고 가정하며, 자동으로 해당 키를 정수형으로 캐스팅합니다. 만약 증가하지 않는 비숫자(primary key) 키를 사용하려면, 공개(퍼블릭) `$incrementing` 속성을 `false`로 설정해야 합니다:

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

기본 키가 정수가 아니라면, `$keyType` 속성을 보호된 상태로 설정해 데이터 타입을 `string`으로 지정해야 합니다:

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
#### "복합" 기본 키 (Composite Primary Keys)

Eloquent는 각 모델에 고유하게 식별할 수 있는 기본 키 하나 이상이 반드시 필요합니다. 하지만 "복합 기본 키"는 Eloquent 모델에서 공식적으로 지원하지 않습니다. 복합 키가 필요하다면, 기본 키 외에 추가적인 다중 컬럼 고유 인덱스를 데이터베이스 테이블에 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키 (UUID and ULID Keys)

자동 증가하는 정수 대신 UUID(primary key)와 ULID를 Eloquent 모델의 기본 키로 사용할 수도 있습니다. UUID는 36자리의 전 세계적으로 유일한 알파벳-숫자 문자열입니다.

UUID를 기본 키로 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 모델에 추가하세요. 단, 모델의 기본 키 컬럼은 [UUID 칼럼과 호환되는 타입](/docs/10.x/migrations#column-method-uuid)인지 확인해야 합니다:

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

기본적으로 `HasUuids` 트레이트는 ["ordered" UUID](/docs/10.x/strings#method-str-ordered-uuid)를 생성하는데, 이들은 데이터베이스 인덱스에 효율적으로 정렬될 수 있습니다.

UUID 생성 방식을 커스터마이징하려면 모델에 `newUniqueId` 메서드를 정의할 수 있고, UUID를 할당할 칼럼을 `uniqueIds` 메서드로 명시할 수도 있습니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델용 새 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자를 할당할 칼럼 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

필요하면 ULID(26자리로 짧으며, UUID처럼 정렬 가능한)도 사용할 수 있습니다. ULID를 쓰려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 사용하고 [ULID 칼럼과 호환되는 컬럼](/docs/10.x/migrations#column-method-ulid)이 있는지 확인하세요:

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
### 타임스탬프 (Timestamps)

기본적으로 Eloquent는 모델과 연결된 테이블에 `created_at`과 `updated_at` 칼럼이 있다고 가정합니다. 모델 생성 및 갱신 시 이 칼럼의 값을 자동으로 설정합니다. 만약 Eloquent가 이 칼럼 자동 처리를 하지 않게 하려면, 모델 내 `$timestamps` 속성을 `false`로 설정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에서 타임스탬프를 사용할지 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프 포맷을 커스터마이징하려면 `$dateFormat` 속성을 설정하세요. 이 속성은 날짜가 데이터베이스에 저장되는 형식과 모델이 배열 또는 JSON으로 직렬화될 때의 형식을 모두 결정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 칼럼 저장 형식
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프를 저장하는 칼럼 이름을 변경하려면, 모델에 `CREATED_AT`과 `UPDATED_AT` 상수를 정의할 수 있습니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프가 변경되지 않도록 모델 작업 중 이를 방지하려면, `withoutTimestamps` 메서드에 작업 클로저를 전달해 실행할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment(['reads']));
```

<a name="database-connections"></a>
### 데이터베이스 연결 (Database Connections)

기본적으로 모든 Eloquent 모델은 애플리케이션 설정의 기본 데이터베이스 연결을 사용합니다. 특정 모델에 별도의 연결을 지정하려면, 모델에 `$connection` 속성을 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에서 사용할 데이터베이스 연결명
     *
     * @var string
     */
    protected $connection = 'sqlite';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값 (Default Attribute Values)

새로 인스턴스화되는 모델은 기본적으로 속성 값이 없습니다. 모델 속성의 기본값을 정의하려면 `$attributes` 속성에 기본값 배열을 지정하세요. 이 속성의 값들은 데이터베이스에서 읽어온 원시(raw) 형태로 저장되어야 합니다:

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
### Eloquent 엄격성 설정 (Configuring Eloquent Strictness)

Laravel은 여러 상황에서 Eloquent 동작과 엄격성을 조절할 수 있는 메서드들을 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 제한할지 여부를 나타내는 불리언 값을 인수로 받습니다. 예를 들어, 프로덕션 환경에서는 지연 로딩을 허용하고 개발 환경에서만 이를 막아, 실수로 프로덕션에서 지연 로딩이 발생해도 정상 작동하도록 할 수 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 호출합니다:

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

또한 `preventSilentlyDiscardingAttributes` 메서드를 호출해 채우기(fill) 대상이 아닌 속성을 무시할 때 예외를 발생하도록 설정할 수 있습니다. 개발 시 이런 설정은 모델의 `fillable` 배열에 추가하지 않은 속성을 잘못 채우는 실수를 방지하는데 도움이 됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기 (Retrieving Models)

모델과 연결된 데이터베이스 테이블이 준비되면, 데이터를 조회해 사용할 수 있습니다. 각 Eloquent 모델은 연결된 테이블을 유창하게 쿼리할 수 있는 강력한 [쿼리 빌더](/docs/10.x/queries)라고 생각할 수 있습니다. 모델의 `all` 메서드는 관련 테이블에서 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

`all` 메서드는 테이블 내 모든 결과를 반환합니다. 그러나 Eloquent 모델이 기본적으로 [쿼리 빌더](/docs/10.x/queries)이므로, 추가 조건을 붙인 뒤 `get` 메서드로 결과를 가져올 수도 있습니다:

```php
$flights = Flight::where('active', 1)
               ->orderBy('name')
               ->take(10)
               ->get();
```

> [!NOTE]  
> Eloquent 모델 쿼리를 작성할 때 Laravel의 [쿼리 빌더](/docs/10.x/queries) 내 모든 메서드를 사용할 수 있으니 참고하세요.

<a name="refreshing-models"></a>
#### 모델 새로 고침하기

이미 데이터베이스에서 조회한 모델 인스턴스가 있다면, `fresh`와 `refresh` 메서드로 모델을 새로 고칠 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회해 새로운 인스턴스를 반환합니다. 기존 인스턴스는 변경되지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 데이터로 다시 초기화합니다. 또한 로드한 연관관계도 모두 새로 고칩니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션 (Collections)

앞서 본 것처럼, Eloquent의 `all` 및 `get` 메서드는 데이터 베이스에서 여러 레코드를 반환하지만, 일반 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent 컬렉션 클래스는 Laravel의 기본 컬렉션인 `Illuminate\Support\Collection` 클래스를 상속하며, [다양한 유용한 메서드](/docs/10.x/collections#available-methods)를 제공합니다. 예를 들면, `reject` 메서드를 이용해 특정 조건에 맞는 모델을 컬렉션에서 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션은 Laravel 기본 컬렉션보다 Eloquent 모델 집합과 상호작용하기 위한 [몇 가지 추가 메서드](/docs/10.x/eloquent-collections#available-methods)도 제공합니다.

또한 Laravel 컬렉션은 PHP iterable 인터페이스를 구현하므로, 배열처럼 컬렉션을 foreach로 반복할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청킹(분할 처리) 결과 (Chunking Results)

메모리가 제한된 환경에서 `all`이나 `get`으로 수만 건의 레코드를 동시에 불러오면 메모리 부족이 발생할 수 있습니다. 이런 경우 `chunk` 메서드를 사용해 레코드들을 작은 단위로 나누어 처리하세요.

`chunk` 메서드는 데이터베이스에서 일정 크기만큼 레코드를 조회해 클로저에 전달합니다. 최종적으로 메모리 사용량이 크게 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인자는 한 번에 처리할 레코드 수입니다. 두 번째 인자인 클로저는 데이터베이스에서 조회된 각 청크(chunk)를 받습니다.

데이터를 필터링하면서 동시에 업데이트해야 한다면, 예기치 않은 결과를 피하기 위해 `chunkById` 메서드를 사용하세요. 내부적으로 `chunkById`는 이전 청크의 마지막 모델 `id`보다 큰 모델만 계속 조회합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, $column = 'id');
```

<a name="chunking-using-lazy-collections"></a>
### 지연 컬렉션을 이용한 청킹 (Chunking Using Lazy Collections)

`lazy` 메서드는 [위에서 본 `chunk` 메서드](#chunking-results)처럼 내부적으로 쿼리를 청크 단위로 실행하지만, 직접 클로저에 전달하는 대신 `LazyCollection` 형태로 평탄화된 결과를 반환합니다. 따라서 쿼리 결과를 하나의 연속된 스트림처럼 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

앞서 `chunkById`처럼 `lazy` 메서드에도 필터링 중 업데이트가 필요하면 `lazyById` 메서드를 사용합니다:

```php
Flight::where('departed', true)
    ->lazyById(200, $column = 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 쓰면, `id` 칼럼을 기준으로 내림차순 정렬하여 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서 (Cursors)

`lazy` 메서드와 비슷하게, `cursor` 메서드도 수만 건의 모델을 반복할 때 메모리 사용량을 크게 줄여줍니다.

`cursor`는 단일 쿼리만 실행하지만, 결과 모델들은 실제로 반복할 때까지 메모리에 올리지 않습니다. 즉, 한 번에 하나의 모델만 메모리에 유지합니다.

> [!WARNING]  
> `cursor` 메서드는 한 번에 하나의 모델만 캐싱하므로, 연관관계를 미리 불러오는 이저 로딩(eager loading)은 지원하지 않습니다. 관계를 미리 불러와야 한다면 [지연 컬렉션(`lazy`)](#chunking-using-lazy-collections) 메서드를 사용하는 것이 좋습니다.

`cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용해 구현되었습니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환하며, [지연 컬렉션](/docs/10.x/collections#lazy-collections)처럼 일반적인 컬렉션 메서드들을 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 메모리 사용량은 훨씬 적지만, 결국 PHP의 PDO 드라이버가 내부적으로 쿼리 결과를 버퍼링하기 때문에 메모리 부족 문제가 완전히 사라지지는 않습니다. 매우 큰 데이터셋일 경우 [지연 컬렉션(`lazy`)](#chunking-using-lazy-collections) 사용을 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리 (Advanced Subqueries)

<a name="subquery-selects"></a>
#### 서브쿼리 선택 (Subquery Selects)

Eloquent는 쿼리 빌더의 `select` 및 `addSelect` 메서드에서 관련 테이블의 정보를 단일 쿼리로 함께 조회하는 고급 서브쿼리 기능도 제공합니다.

예를 들어 비행 목적지 `destinations` 테이블과 해당 목적지로 가는 `flights` 테이블이 있다고 합시다. `flights` 테이블에 도착 시간(`arrived_at`) 칼럼이 있습니다.

다음 쿼리는 각 목적지와 해당 목적지에 가장 최근 도착한 항공편 이름을 단일 쿼리로 조회합니다:

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
#### 서브쿼리 정렬 (Subquery Ordering)

쿼리 빌더의 `orderBy`는 서브쿼리도 지원합니다. 동일한 예시에서 각 목적지별로 가장 최근 비행 도착 일자 기준으로 정렬하는 단일 쿼리를 실행할 수 있습니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 조회하기 (Retrieving Single Models / Aggregates)

주어진 쿼리 조건에 맞는 여러 레코드 대신 단일 모델을 조회하고 싶다면 `find`, `first`, `firstWhere` 메서드를 사용하세요. 이들은 컬렉션이 아닌 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 모델 조회
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// 위와 동일하지만 더 간결한 문법
$flight = Flight::firstWhere('active', 1);
```

조회 결과가 없으면 다른 동작을 하고 싶을 때 `findOr` 또는 `firstOr` 메서드를 사용하세요. 모델 인스턴스가 없으면 전달한 클로저를 실행하고, 클로저가 반환하는 값이 메서드 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 모델 미발견 예외 (Not Found Exceptions)

모델이 없으면 예외를 던지고 싶을 때가 있습니다. 특히 라우트나 컨트롤러에서 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리 결과 첫 모델을 조회하지만, 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외가 잡히지 않을 경우 404 HTTP 응답을 자동 반환합니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성 (Retrieving or Creating Models)

`firstOrCreate` 메서드는 지정한 속성으로 데이터베이스를 찾고, 없으면 첫 번째 배열 인자와 두 번째 배열 인자를 병합해 새 레코드를 생성합니다.

`firstOrNew`는 `firstOrCreate`와 비슷하지만, 모델이 없으면 데이터베이스에 저장하지 않고 새 모델 인스턴스만 반환합니다. 저장하려면 별도로  `save`를 호출하세요:

```php
use App\Models\Flight;

// 이름으로 비행편 찾거나 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 찾거나 없으면 추가 속성 포함해 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 찾거나 없으면 새 인스턴스 생성만 (저장 안 함)
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 찾거나 없으면 인스턴스 생성만 (추가 속성 포함)
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회 (Retrieving Aggregates)

Eloquent 모델에서도 Laravel [쿼리 빌더](/docs/10.x/queries)의 `count`, `sum`, `max` 등의 집계 메서드를 사용할 수 있습니다. 이들은 모델 대신 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 갱신 (Inserting and Updating Models)

<a name="inserts"></a>
### 삽입 (Inserts)

Eloquent에서 단순히 데이터 조회뿐 아니라 새로운 레코드 삽입도 쉽습니다. 새 모델 인스턴스를 만들고 속성을 세팅한 뒤, `save` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 데이터베이스에 새 비행편 저장
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

예제에서 요청의 `name` 필드를 `Flight` 모델의 `name` 속성에 할당 후 `save` 하면, 새 레코드가 테이블에 삽입됩니다. `created_at`과 `updated_at` 타임스탬프는 자동으로 세팅되므로 따로 설정하지 않아도 됩니다.

또는, `create` 메서드를 사용해 단일 구문으로 새 모델을 삽입할 수 있습니다. 삽입 후 모델 인스턴스가 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하려면 모델에 `fillable` 혹은 `guarded` 속성 중 하나를 반드시 지정해야 합니다. 이는 기본적으로 대량 할당 취약점 보호 때문입니다. 대량 할당 관련 내용은 [대량 할당 문서](#mass-assignment)를 참조하세요.

<a name="updates"></a>
### 갱신 (Updates)

`save` 메서드는 이미 있는 모델을 갱신할 때도 사용 가능합니다. 기존 모델을 불러와 수정 후, `save`를 호출하면 업데이트됩니다. `updated_at` 타임스탬프도 자동 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<a name="mass-updates"></a>
#### 대량 갱신 (Mass Updates)

쿼리 조건에 맞는 모델 여러 건을 한 번에 수정할 수도 있습니다. 예를 들어 `active` 상태이고 목적지가 `San Diego`인 모든 비행편을 지연 상태로 표시하려면 다음과 같이 합니다:

```php
Flight::where('active', 1)
      ->where('destination', 'San Diego')
      ->update(['delayed' => 1]);
```

`update` 메서드는 갱신할 칼럼과 값을 배열로 받고, 영향을 받은 행 개수를 반환합니다.

> [!WARNING]  
> Eloquent 대량 갱신 시 대상 모델 이벤트(`saving`, `saved`, `updating`, `updated`)는 발생하지 않습니다. 대량 갱신은 실제로 모델을 불러오지 않고 직접 쿼리 실행하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 검사하기

Eloquent는 모델 상태를 검사하는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

- `isDirty`: 모델이 조회된 이후 속성이 바뀌었는지 검사. 속성명이나 배열을 인자로 받아 해당 속성들이 변경됐는지 확인 가능.
- `isClean`: `isDirty`의 반대로, 속성이 바뀌지 않았는지 검사.
- `wasChanged`: 저장 시점에서 어떤 속성이 변경됐는지 확인.

아래 예시를 참고하세요:

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

`wasChanged`도 비슷하게 속성 변경 여부를 확인합니다:

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

`getOriginal` 메서드는 모델이 처음 조회되었을 때의 원본 속성 배열을 반환합니다. 특정 속성의 원본 값도 인자로 받아 확인할 수 있습니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = "Jack";
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열
```

<a name="mass-assignment"></a>
### 대량 할당 (Mass Assignment)

`create` 메서드를 사용해 새 모델을 단일 문장으로 저장할 때는 `fillable` 또는 `guarded` 속성 값 지정이 필수입니다. 이는 기본적으로 대량 할당 취약점(Unexpected Mass Assignment)을 막기 위함입니다.

대량 할당 취약점은 사용자가 의도하지 않은 HTTP 요청 필드를 보내어 데이터베이스의 칼럼이 예기치 않게 수정될 때 발생합니다. 예를 들어, `is_admin` 같은 파라미터를 보내면 사용자 권한이 임의로 상승할 수 있습니다.

대량 할당을 시작하려면, 모델에 `$fillable` 속성에 허용할 속성명을 명시합니다. 예를 들어 `Flight` 모델의 `name` 속성만 허용하고 싶으면 다음과 같이 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용된 속성들
     *
     * @var array
     */
    protected $fillable = ['name'];
}
```

허용 속성을 지정한 후, `create` 메서드로 새 레코드를 삽입하면 새 모델 인스턴스를 반환받습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 만들어진 모델 인스턴스에는 `fill` 메서드를 이용해 배열로 속성들을 채울 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 형식 칼럼을 대량 할당할 때는, 각 JSON 키 이름(`options->enabled` 같은)을 반드시 `$fillable` 배열에 명시해야 합니다. 보안 때문에 `guarded` 속성 만으로는 중첩 JSON 속성 업데이트를 지원하지 않습니다:

```php
/**
 * 대량 할당 허용 속성
 *
 * @var array
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 전면 허용하기

모델의 모든 속성을 대량 할당 허용하려면 `$guarded` 속성을 빈 배열로 만드세요. 단, 이 경우 `fill`, `create`, `update` 메서드에 넘기는 배열을 직접 꼼꼼히 제작해야 합니다:

```php
/**
 * 대량 할당이 허용되지 않는 속성
 *
 * @var array
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 없으면 대량 할당 시 그 속성은 조용히 무시됩니다. 프로덕션 환경에서는 정상적인 동작이나, 개발 시에는 변경 사항 반영이 안 돼서 헷갈릴 수 있습니다.

이럴 때 `preventSilentlyDiscardingAttributes` 메서드를 호출해, 채우기 대상에 없는 속성을 채우려 하면 예외가 발생하도록 할 수 있습니다. 보통 이 메서드는 앱 서비스 프로바이더 등에서 `boot` 메서드에 작성합니다:

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
### 업서트 (Upserts)

기존 모델을 수정하거나 없으면 새로 생성하려면 `updateOrCreate` 메서드를 사용하세요. 이 메서드는 저장까지 수행하므로 `save`를 별도로 호출할 필요 없습니다.

아래 예시는 `departure`가 `Oakland`이고 `destination`이 `San Diego`인 비행편을 찾아 `price`와 `discounted` 값을 업데이트합니다. 해당 비행편이 없으면 두 번째 인자 값을 합친 새 레코드가 생성됩니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

여러 건을 한 쿼리로 업서트 하려면 `upsert` 메서드를 사용하세요. 첫 번째 인자는 삽입 또는 업데이트할 각 행의 배열, 두 번째 인자는 유니크 식별자를 가진 칼럼들, 세 번째 인자는 이미 존재하는 경우 업데이트할 칼럼 배열입니다. 타임스탬프는 자동 세팅됩니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

> [!WARNING]  
> SQL Server 외 모든 데이터베이스에서 `upsert` 두 번째 인자의 칼럼은 반드시 "primary" 또는 "unique" 인덱스를 갖고 있어야 합니다. MySQL 드라이버는 두 번째 인자를 무시하고 테이블의 "primary" 및 "unique" 인덱스를 기준으로 기존 레코드를 판별합니다.

<a name="deleting-models"></a>
## 모델 삭제 (Deleting Models)

모델 인스턴스에서 `delete` 메서드를 호출해 모델을 삭제할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

`truncate` 메서드는 모델과 연결된 모든 DB 레코드를 삭제하며, 자동 증가 ID도 초기화합니다:

```php
Flight::truncate();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 바로 삭제하기

기본 키만 알고 있다면, 모델을 조회하지 않고 `destroy` 메서드로 곧바로 삭제할 수도 있습니다. 단일 키, 여러 키, 키 배열, [컬렉션](/docs/10.x/collections) 모두 인자로 넣을 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

> [!WARNING]  
> `destroy`는 각 모델을 개별 조회 후 `delete` 메서드를 호출하므로, `deleting`과 `deleted` 이벤트가 제대로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 다중 모델 삭제

쿼리 조건에 맞는 여러 모델을 한 번에 삭제할 수 있습니다. 예를 들어 비활성 상태인 모든 비행편을 삭제하려면:

```php
$deleted = Flight::where('active', 0)->delete();
```

> [!WARNING]  
> Eloquent를 통한 대량 삭제 시 모델 이벤트(`deleting`, `deleted`)는 발생하지 않습니다. 실제로 모델 인스턴스를 조회하지 않고 직접 쿼리 실행하기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

레코드를 실제로 삭제하지 않고, `deleted_at` 속성에 삭제 시점을 기록해 논리적으로 삭제하는 소프트 삭제 기능도 제공합니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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
> `SoftDeletes` 트레이트는 자동으로 `deleted_at` 속성을 `DateTime` / `Carbon` 인스턴스로 캐스팅해 줍니다.

데이터베이스 테이블에도 `deleted_at` 칼럼을 추가해야 합니다. Laravel의 [스키마 빌더](/docs/10.x/migrations)에 소프트 삭제를 위한 헬퍼 메서드가 있습니다:

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

이제 모델의 `delete` 메서드를 호출하면 `deleted_at` 칼럼에 현재 날짜 및 시간 값이 저장되고, 실제 데이터는 테이블에 남아 있습니다. 소프트 삭제된 모델은 쿼리 결과에서 자동 제외됩니다.

모델 인스턴스가 소프트 삭제된 상태인지 확인하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복구하기

소프트 삭제된 모델을 다시 살리고 싶을 때는 인스턴스에서 `restore` 메서드를 호출합니다. 이 메서드는 `deleted_at` 컬럼 값을 `null`로 만듭니다:

```php
$flight->restore();
```

쿼리에서 다수 모델을 복구할 때도 `restore`를 사용하며, 이 경우 대량 처리이므로 이벤트는 발생하지 않습니다:

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
#### 영구 삭제하기

소프트 삭제된 모델을 데이터베이스에서 완전히 삭제하려면 `forceDelete` 메서드를 사용합니다:

```php
$flight->forceDelete();
```

관계 쿼리에서도 사용 가능합니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리하기 (Querying Soft Deleted Models)

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함시키기

기본적으로 소프트 삭제된 모델은 쿼리 결과에서 제외됩니다. 그러나 `withTrashed` 메서드를 체인에 추가하면 소프트 삭제 모델도 결과에 포함시킵니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
```

관계 쿼리에서도 회수 가능합니다:

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
## 모델 가지치기 (Pruning Models)

필요 없는 오래된 모델을 주기적으로 삭제하고 싶으면, 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하세요. 그리고 `prunable` 메서드에 삭제할 모델 조건을 반환하도록 구현합니다:

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
     * 가지치기 대상 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`prunable`을 지정한 모델에 `pruning` 메서드를 구현할 수도 있는데, 가지치기 바로 전에 추가 작업(파일 삭제 등)을 할 때 유용합니다:

```php
/**
 * 가지치기 전 준비 작업
 */
protected function pruning(): void
{
    // ...
}
```

구성 후 `model:prune` Artisan 명령어를 `App\Console\Kernel` 내 스케줄러에 등록하세요. 원하는 주기로 실행하면 됩니다:

```php
/**
 * 애플리케이션 명령 스케줄 정의
 */
protected function schedule(Schedule $schedule): void
{
    $schedule->command('model:prune')->daily();
}
```

`model:prune` 명령어는 기본적으로 `app/Models` 디렉터리 내 "Prunable" 모델을 자동 감지합니다. 다른 위치라면 `--model` 옵션에 모델 클래스 배열을 지정하세요:

```php
$schedule->command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 가지치기 대상에서 제외할 때는 `--except` 옵션을 사용합니다:

```php
$schedule->command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 이용하면 실제 삭제는 하지 않고 몇 건이 삭제될지 미리 점검할 수 있습니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]  
> 소프트 삭제 모델은 가지치기 대상이 되면 완전히 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기 (Mass Pruning)

`MassPrunable` 트레이트를 쓰는 모델은 마치 대량 삭제처럼 대량 쿼리로 삭제합니다. 따라서 `pruning` 메서드, `deleting`/`deleted` 이벤트가 호출되지 않고, 최적화된 방식으로 처리됩니다:

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
     * 가지치기 대상 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제 (Replicating Models)

기존 모델 인스턴스를 저장되지 않은 상태로 복사할 때 `replicate` 메서드를 사용할 수 있습니다. 공통 속성이 많은 모델 인스턴스 복제에 유용합니다:

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

복제 시 일부 속성을 제외하고 싶으면 `replicate`에 제외할 속성 이름 배열을 전달할 수 있습니다:

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
## 쿼리 범위 (Query Scopes)

<a name="global-scopes"></a>
### 글로벌 스코프 (Global Scopes)

글로벌 스코프는 특정 모델에 대해 모든 쿼리에 조건을 강제로 추가하는 기능입니다. Laravel 내부의 [소프트 삭제](#soft-deleting)도 글로벌 스코프를 이용해 삭제된 모델을 자동 제외합니다. 자신의 글로벌 스코프를 정의하면, 모든 관련 쿼리에 공통 조건을 편리하게 붙일 수 있습니다.

<a name="generating-scopes"></a>
#### 글로벌 스코프 생성하기

`make:scope` Artisan 명령어로 글로벌 스코프 클래스를 생성하면, `app/Models/Scopes` 디렉터리에 스코프 클래스가 만들어집니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성하기

글로벌 스코프 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하며, 반드시 `apply` 메서드를 포함해야 합니다. `apply`에서는 쿼리 빌더에 필요한 조건을 추가합니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]  
> 스코프로 쿼리 select 절에 칼럼을 추가할 때는 `select` 대신 `addSelect`를 사용하세요. 기존의 select 절이 덮어써지는 것을 방지합니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용하기

모델에 글로벌 스코프를 적용하려면, `ScopedBy` 속성을 사용하는 방법이 가장 간단합니다:

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

또는 모델의 `booted` 메서드를 오버라이드하고 `addGlobalScope`를 호출해 직접 등록할 수도 있습니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

이후 `User::all()`을 호출하면 다음 SQL 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프 (Anonymous Global Scopes)

간단한 글로벌 스코프라면 클래스 없이 클로저를 사용해 정의할 수도 있습니다. 이 때는 `addGlobalScope`의 첫 번째 인자로 스코프 이름을 지정해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 "booted" 메서드
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

쿼리에서 특정 글로벌 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용하세요. 클래스 기반 스코프는 클래스명을, 클로저 스코프는 이름 문자열을 인자로 전달합니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 혹은 모든 글로벌 스코프를 제거하려면 `withoutGlobalScopes`를 사용합니다:

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 특정 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프 (Local Scopes)

로컬 스코프는 자주 사용하는 쿼리 조건을 모델 내 메서드로 정의해 재사용할 수 있습니다. 메서드 이름 앞에 `scope`를 붙여 선언하며, 쿼리 빌더 인자를 받아야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 있는 사용자만 조회하는 스코프
     */
    public function scopePopular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 조회하는 스코프
     */
    public function scopeActive(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용하기

스코프 메서드 호출 시 `scope` 접두사는 빼고 호출합니다. 여러 스코프를 체인 연결할 수도 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조건과 결합해 여러 스코프를 연결할 때는 클로저를 써서 그룹핑하는 것이 필요합니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

더 간단히 하려면 Laravel의 "higher order" `orWhere` 메서드가 클로저 없이도 자연스러운 체인 호출을 허용합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프 (Dynamic Scopes)

스코프가 인자를 받을 수 있도록 하려면 모델 메서드 시그니처에 인자를 추가하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입 사용자만 조회하는 스코프
     */
    public function scopeOfType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

인자를 넣어 스코프를 호출할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```

<a name="comparing-models"></a>
## 모델 비교 (Comparing Models)

두 모델이 같은지 확인할 때는 `is`와 `isNot` 메서드를 사용하세요. 두 모델의 기본 키, 테이블, 데이터베이스 연결이 같은지 여부를 봅니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](/docs/10.x/eloquent-relationships)에도 `is`, `isNot` 메서드가 지원되어 쿼리없이 비교 시 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트 (Events)

> [!NOTE]  
> Eloquent 이벤트를 클라이언트 애플리케이션에 실시간으로 전송하고 싶다면 Laravel의 [모델 이벤트 브로드캐스팅](/docs/10.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 라이프사이클 각 단계에서 여러 이벤트를 발생시킵니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

모델이 데이터베이스에서 조회될 때 `retrieved` 이벤트가 발생합니다. 신규 저장 시 `creating` 과 `created`가, 수정 시 `updating` / `updated`가 발생합니다. `saving` / `saved`는 생성/수정 모두에서 호출되며, 속성 변경 여부와 무관합니다. 이벤트 이름 끝이 `-ing`면 변경 전, `-ed`면 변경 후에 호출됩니다.

모델 이벤트를 감지하려면, Eloquent 모델에 `$dispatchesEvents` 속성을 정의하세요. 이것은 라이프사이클 이벤트를 여러분의 [이벤트 클래스](/docs/10.x/events)로 매핑합니다. 각 이벤트 클래스는 생성자에서 영향을 받은 모델 인스턴스를 받는 구조여야 합니다:

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

이후 [이벤트 리스너](/docs/10.x/events#defining-listeners)를 활용해 이벤트를 처리할 수 있습니다.

> [!WARNING]  
> Eloquent에서 대량 업데이트 또는 삭제 시, 영향을 받은 모든 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트는 발생하지 않습니다. 모델을 실제로 불러오지 않고 직접 쿼리 실행하기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용 (Using Closures)

커스텀 이벤트 클래스 대신, 이벤트가 발생할 때 실행되는 클로저를 등록할 수 있습니다. 일반적으로 모델의 `booted` 메서드에서 등록합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요에 따라 [큐블 익명 이벤트 리스너](/docs/10.x/events#queuable-anonymous-event-listeners)를 이용해 이벤트 처리를 백그라운드 큐로 분리할 수도 있습니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버 (Observers)

<a name="defining-observers"></a>
#### 옵저버 정의하기

한 모델의 여러 이벤트를 듣는다면, 하나의 옵저버 클래스에 리스너를 모아 관리할 수 있습니다. 옵저버 메서드 이름은 듣고자 하는 이벤트와 동일하며, 인자로 영향을 받은 모델 인스턴스를 받습니다. 옵저버 클래스를 만드는 가장 쉬운 방법은 `make:observer` Artisan 명령어입니다:

```shell
php artisan make:observer UserObserver --model=User
```

옵저버는 `app/Observers` 디렉터리에 생성되며, 없으면 생성됩니다. 기본 코드는 다음과 같습니다:

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

옵저버 등록은 모델에 `ObservedBy` 속성을 붙이는 방법이 간단합니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, 앱의 `App\Providers\EventServiceProvider` 내 `boot` 메서드에서 `observe` 메서드를 수동 호출할 수 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 이벤트 등록
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]  
> 옵저버는 `saving`, `retrieved` 등 더 많은 이벤트를 수신할 수도 있습니다. 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 DB 트랜잭션

모델 생성이 데이터베이스 트랜잭션 안에서 일어날 때, 옵저버가 트랜잭션 커밋 후에 이벤트 핸들러를 실행하도록 하려면 `ShouldHandleEventsAfterCommit` 인터페이스를 옵저버 클래스에 구현하세요. 트랜잭션이 없으면 즉시 실행합니다:

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
### 이벤트 뮤팅 (Muting Events)

가끔 모델에서 발생하는 모든 이벤트를 일시적으로 무시하고 싶을 때가 있습니다. `withoutEvents` 메서드를 사용하면, 클로저 내부 실행 동안 이벤트가 디스패치되지 않습니다. 클로저 반환값은 `withoutEvents`가 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장하기

특정 모델에 대해 이벤트를 발생시키지 않고 저장하고 싶다면 `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이와 유사하게 `update`, `delete`, `soft delete`, `restore`, `replicate`에도 이벤트 없이 실행하는 메서드가 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```