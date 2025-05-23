# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [속성 기본값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [지연 컬렉션으로 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 정리(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거(Muting)](#muting-events)

<a name="introduction"></a>
## 소개

라라벨은 데이터베이스와 즐겁게 상호작용할 수 있도록 해주는 객체-관계 매퍼(ORM)인 Eloquent를 제공합니다. Eloquent를 사용할 때는 각 데이터베이스 테이블에 해당하는 "모델"이 존재하며, 이 모델을 통해 해당 테이블과 상호작용할 수 있습니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, 레코드를 삽입, 수정, 삭제하는 작업도 지원합니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 미리 구성해야 합니다. 데이터베이스 구성에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고하십시오.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저 Eloquent 모델을 생성해보겠습니다. 일반적으로 모델은 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성하면서 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 동시에 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 팩토리(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 요청(form request) 등 다양한 종류의 클래스도 같이 생성할 수 있습니다. 이 옵션들은 조합해서 한 번에 여러 클래스를 생성할 수도 있습니다.

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

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 동시 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 한 번에 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청을 단축 명령어로 생성...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗(pivot) 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

모델의 코드만 훑어보며 속성이나 연관관계를 모두 파악하기 어려울 때가 있습니다. 이럴 땐 `model:show` Artisan 명령어를 사용해, 해당 모델의 속성과 관계(리레이션)를 한눈에 보여주는 요약 정보를 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치하게 됩니다. 이제 기본적인 모델 클래스를 살펴보고 Eloquent의 주요 관례 몇 가지를 알아보겠습니다.

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

위 예시를 보면 `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 따로 지정하지 않았다는 것을 알 수 있습니다. Eloquent에서는 기본적으로 클래스 이름을 "스네이크 케이스(snake case)"의 복수형으로 변환한 값을 테이블 이름으로 사용합니다. 즉, 위의 경우 `Flight` 모델은 `flights` 테이블과 연결됩니다. 만약 `AirTrafficController` 모델이라면, `air_traffic_controllers` 테이블과 연결됩니다.

만약 모델과 연결된 데이터베이스 테이블의 이름이 이 관례와 다르다면, 모델의 `table` 속성(property)에 테이블 이름을 명시적으로 지정하면 됩니다.

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
### 기본 키

Eloquent는 기본적으로 각 모델이 연결된 데이터베이스 테이블에 `id`라는 이름의 기본 키(primary key) 컬럼이 있다고 가정합니다. 다른 컬럼을 기본 키로 사용하려면, 모델에 `protected $primaryKey` 속성을 지정하세요.

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

또한, Eloquent는 기본 키가 자동 증가(increment)하는 정수(integer) 값이라고 가정하여, 기본 키 값을 자동으로 정수로 변환(cast)해줍니다. 만약 자동 증가가 아니거나 숫자가 아닌 기본 키를 사용하려면, 모델의 `$incrementing` 속성을 `false`로 설정해야 합니다.

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

기본 키가 정수형이 아니라면, 모델에 `protected $keyType` 속성을 `string`으로 정의해야 합니다.

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

Eloquent 모델은 각 모델에 최소한 하나의 고유한 "ID"(기본 키 컬럼)가 있어야 합니다. Eloquent에는 "복합(Composite) 기본 키"는 지원되지 않습니다. 하지만 데이터베이스 테이블에 복수 컬럼으로 이루어진 고유 인덱스를 추가하는 것은 자유롭게 할 수 있습니다(단, 반드시 한 컬럼의 고유 기본 키는 필요합니다).

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

기본 키로 자동 증가 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자 길이의 알파벳+숫자로 이루어진 전역 고유 식별자입니다.

모델에서 자동 증가하는 정수 키 대신 UUID 키를 사용하고 싶다면, 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용할 수 있습니다. 당연히 모델에는 [UUID 타입의 기본 키 컬럼](/docs/12.x/migrations#column-method-uuid)이 있어야 합니다.

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

기본적으로 `HasUuids` 트레이트는 모델에 ["순서가 지정된" UUID](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 이런 UUID는 사전적(lexicographical)으로 정렬할 수 있기 때문에, 인덱스가 걸린 데이터베이스에 저장할 때 효율적입니다.

UUID 생성 방식을 원하는 대로 변경하려면, 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한, 모델에서 어떤 컬럼이 UUID를 받아야 할지 `uniqueIds` 메서드를 정의하여 지정할 수도 있습니다.

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
 * 고유 식별자를 받아야 할 컬럼 목록 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 ULID를 사용할 수도 있습니다. ULID는 UUID와 비슷하나 길이가 26자이며, 마찬가지로 사전적 정렬이 가능한 특징이 있습니다. ULID를 사용하려면, 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 적용하고, [ULID 타입의 기본 키 컬럼](/docs/12.x/migrations#column-method-ulid)이 모델에 있어야 합니다.

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

Eloquent는 기본적으로 각 모델에 연결된 데이터베이스 테이블에 `created_at` 및 `updated_at` 컬럼이 있다고 가정합니다. Eloquent는 모델이 생성되거나 수정될 때 이 컬럼의 값을 자동으로 관리합니다. 이러한 컬럼을 Eloquent가 자동 관리하지 않도록 하고 싶다면, 모델에 `$timestamps` 속성을 `false`로 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 타임스탬프를 사용할지 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델의 타임스탬프 저장 형식을 변경하려면, `$dateFormat` 속성으로 포맷 문자열을 지정하세요. 이 속성은 데이터베이스에 날짜 속성을 저장하는 방식과, 모델이 배열이나 JSON으로 직렬화될 때의 형식을 결정합니다.

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

타임스탬프에 사용되는 컬럼명을 커스터마이즈하려면, 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 각각 원하는 컬럼명으로 지정하면 됩니다.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 값 변경 없이 데이터를 조작하고 싶다면, `withoutTimestamps` 메서드에 클로저를 전달하여 해당 작업을 감싸 수행할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

모든 Eloquent 모델은 기본적으로 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 다른 데이터베이스 연결을 사용하려면, 모델의 `$connection` 속성(property)에 사용하고자 하는 연결 이름을 지정합니다.

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
### 속성 기본값

새로 인스턴스화한 모델은 기본적으로 아무런 속성 값도 포함하지 않습니다. 일부 속성의 기본값을 지정하고 싶다면, 모델에 `$attributes` 속성(property)을 정의하세요. 이 배열에 지정하는 속성 값들은 데이터베이스에서 읽어온 것과 동일한 형식(즉, 가공되지 않은 "저장용" 값)이어야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 속성의 기본값 배열
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

라라벨은 다양한 상황에서 Eloquent의 동작과 "엄격성"을 설정할 수 있도록 여러 메서드를 제공합니다.

가장 먼저, `preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 방지할지 여부를 나타내는 불리언 값을 받습니다. 예를 들어, 운영 환경에서는 지연 로딩이 있더라도 애플리케이션이 정상 작동하도록 허용하고, 개발 환경에서만 지연 로딩을 방지하고 싶을 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 준비(Bootstrap)
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, 모델의 `fillable` 배열에 없는 속성을 할당하려고 할 때 라라벨이 예외를 던지도록 만들려면, `preventSilentlyDiscardingAttributes` 메서드를 호출할 수 있습니다. 이는 로컬 개발 중, 예상치 못한 실수로 잘못된 속성을 할당할 때 오류를 미리 방지하는 데 유용합니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [해당하는 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)이 준비되었다면, 이제 데이터베이스에서 데이터를 가져올 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)로 작동하여 해당 모델에 연결된 테이블을 유연하게 조회할 수 있습니다. 모델의 `all` 메서드는 모델과 연결된 데이터베이스 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드

Eloquent의 `all` 메서드는 모델 테이블의 전체 결과를 반환합니다. 그러나 각 Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries)로 동작하므로, 쿼리에서 조건을 추가한 후 `get` 메서드로 원하는 결과만 조회할 수도 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->take(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더로 동작하므로, 라라벨의 [쿼리 빌더](/docs/12.x/queries)가 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 이 메서드들도 적극적으로 활용해보세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있을 때, `fresh` 및 `refresh` 메서드로 모델을 "새로고침"할 수 있습니다. `fresh` 메서드는 모델을 데이터베이스에서 다시 조회해 새로운 인스턴스를 반환합니다(기존 인스턴스는 변경되지 않음).

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 값으로 다시 채웁니다(리하이드레이트). 또한 해당 모델에 로딩된 모든 관계(리레이션)들도 함께 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 살펴본 것처럼 Eloquent의 `all` 및 `get` 메서드는 다수의 레코드를 데이터베이스에서 조회합니다. 이 메서드들은 결과를 일반 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스로 반환합니다.

Eloquent의 `Collection` 클래스는 라라벨의 기본 `Illuminate\Support\Collection` 클래스를 확장하고 있으며, 데이터 컬렉션을 다루기에 [매우 유용한 다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 사용해 클로저의 반환값에 따라 컬렉션에서 특정 모델들을 제거할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

라라벨의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 전용의 [추가 메서드](/docs/12.x/eloquent-collections#available-methods)들도 제공됩니다.

라라벨의 모든 컬렉션은 PHP의 반복(iterable) 인터페이스를 구현하므로, 배열처럼 foreach 등으로 자유롭게 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

`all`이나 `get` 메서드를 사용해 수만 건 이상의 Eloquent 레코드를 한 번에 조회하면 애플리케이션이 메모리 부족에 빠질 수 있습니다. 이런 경우에는 `chunk` 메서드를 사용해 모델을 나누어 청크 단위로 처리할 수 있습니다.

`chunk` 메서드는 Eloquent 모델 일부만을 조회해서 클로저로 전달합니다. 이 방식은 한 번에 모든 레코드를 가져오지 않고, 현재 청크에 해당하는 모델만 메모리에 올려두어 대량 데이터를 다룰 때 메모리 사용량을 크게 줄일 수 있습니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인자는 한 번에 처리할 레코드 수(청크 크기)입니다. 두 번째 인자로 전달하는 클로저는 각 청크가 조회될 때마다 실행됩니다. 데이터베이스에서 각 청크 단위로 쿼리가 별도로 실행됩니다.

만약 청크를 순회하면서 업데이트할 칼럼을 기준으로 필터링을 한다면, 의도치 않은 결과나 불일치가 발생할 수 있습니다. 이 경우에는 `chunkById` 메서드를 사용해야 합니다. 내부적으로 `chunkById`는 매번 이전 청크의 마지막 모델보다 `id` 컬럼 값이 큰 모델을 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가합니다. 따라서 여러분의 조건 역시 보통 [클로저로 논리 그룹핑](/docs/12.x/queries#logical-grouping)하는 것이 좋습니다.

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
### 지연 컬렉션으로 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게, 내부적으로 쿼리를 청크 단위로 실행합니다. 그러나 각 청크를 콜백에 직접 넘기는 대신, `lazy` 메서드는 Eloquent 모델의 평탄화(flattened)된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환합니다. 이를 통해 결과를 하나의 스트림처럼 자유롭게 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 메서드를 사용하여, 청크를 순회하면서 동시에 업데이트할 컬럼 값을 기준으로 필터링할 경우에는 `lazyById` 메서드를 사용해야 합니다. `lazyById` 역시 내부적으로 이전 청크의 마지막 모델 `id`값보다 큰 모델만을 각각 순회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면, `id`를 기준으로 내림차순 정렬하여 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드와 유사하게, `cursor` 메서드도 수만 건이 넘는 Eloquent 모델을 반복(iterate) 순회할 때 애플리케이션의 메모리 사용량을 크게 줄일 수 있습니다.

`cursor` 메서드는 오직 한 번만 데이터베이스 쿼리를 실행합니다. 그러나 실제로 순회할 때까지 개별 Eloquent 모델을 "하이드레이트(hydrate)"하지 않으므로, 반복하는 동안 한 번에 오직 하나의 Eloquent 모델만 메모리에 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 하나의 모델만 메모리에 가지고 있기 때문에, 관계(리레이션)를 eager load 할 수 없습니다. 관계를 미리 로딩해야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하는 것이 좋습니다.

`cursor` 메서드는 내부적으로 PHP의 [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)은 일반 라라벨 컬렉션에서 제공되는 많은 메서드를, 한 번에 하나의 데이터만 메모리에 올리면서 사용할 수 있게 해줍니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만(한 번에 한 모델만 메모리에 올리므로), 결국 메모리에 제한이 올 수 있습니다. 이는 [PHP의 PDO 드라이버가 모든 원시 쿼리 결과를 내부적으로 버퍼링하기 때문](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 정말 많은 양의 레코드를 다룰 때는 [lazy 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>

### 고급 하위 쿼리

<a name="subquery-selects"></a>
#### 하위 쿼리 선택

Eloquent는 고급 하위 쿼리 기능을 제공합니다. 이를 통해 하나의 쿼리에서 관계된 테이블의 정보를 가져올 수 있습니다. 예를 들어, `destinations`라는 비행 목적지 테이블과, 해당 목적지로의 `flights` 테이블이 있다고 가정해 보겠습니다. `flights` 테이블에는 비행기의 도착 시점을 나타내는 `arrived_at` 컬럼이 존재합니다.

쿼리 빌더의 `select` 및 `addSelect` 메서드에서 제공하는 하위 쿼리 기능을 사용하면, 모든 `destinations`와 그 목적지에 가장 최근에 도착한 비행기의 이름을 하나의 쿼리로 조회할 수 있습니다.

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
#### 하위 쿼리 정렬

또한 쿼리 빌더의 `orderBy` 기능도 하위 쿼리를 지원합니다. 위의 비행기 예제를 계속 사용하면, 이 기능을 활용하여 각 목적지에 마지막으로 도착한 비행기 도착 시점을 기준으로 모든 목적지를 정렬할 수도 있습니다. 이 역시 하나의 데이터베이스 쿼리만 실행하여 처리할 수 있습니다.

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 및 집계값 조회

지정한 쿼리 조건에 맞는 모든 레코드를 조회하는 것 외에도, `find`, `first`, 또는 `firstWhere` 메서드를 사용해 단일 레코드를 가져올 수 있습니다. 이 메서드들은 모델 컬렉션 대신 단일 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본키로 모델 하나를 조회합니다...
$flight = Flight::find(1);

// 지정 쿼리 조건과 일치하는 첫 번째 모델을 조회합니다...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건과 일치하는 첫 번째 모델을 대안적으로 조회합니다...
$flight = Flight::firstWhere('active', 1);
```

때때로 쿼리 결과가 없을 경우 다른 처리를 하고 싶을 수 있습니다. `findOr` 및 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과가 없을 경우 지정한 클로저를 실행합니다. 클로저에서 반환된 값이 해당 메서드의 결과가 됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 존재하지 않을 때 예외 처리

모델을 찾을 수 없을 때 예외를 발생시키고 싶은 경우가 있습니다. 이는 라우트나 컨트롤러에서 특히 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리 결과의 첫 번째 모델을 조회하며, 결과가 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException` 예외를 따로 처리하지 않으면, 라라벨은 자동으로 404 HTTP 응답을 클라이언트로 반환합니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍을 이용해 데이터베이스 레코드를 찾으려고 시도합니다. 해당 모델이 데이터베이스에 존재하지 않으면, 첫 번째 배열 인수와 선택적인 두 번째 배열 인수를 병합하여 새로운 레코드를 삽입합니다.

`firstOrNew` 메서드도 `firstOrCreate`와 비슷하게 동작하지만, 모델이 존재하지 않을 경우 새로운 모델 인스턴스만 반환하고 실제 데이터베이스에는 저장하지 않습니다. `firstOrNew`로 반환된 모델은 데이터베이스에 아직 저장되지 않았으므로, 직접 `save` 메서드를 호출해야 합니다.

```php
use App\Models\Flight;

// 이름으로 조회하거나, 없으면 생성합니다...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나, 없으면 이름, delayed, arrival_time 속성으로 생성합니다...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회하거나, 없으면 새 Flight 인스턴스를 만듭니다...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회하거나, 없으면 해당 속성으로 인스턴스화합니다...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델을 다룰 때도 라라벨 [쿼리 빌더](/docs/12.x/queries)가 제공하는 `count`, `sum`, `max` 등의 [집계 메서드](/docs/12.x/queries#aggregates)를 사용할 수 있습니다. 이러한 메서드는 Eloquent 모델 인스턴스 대신 단일 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때, 데이터베이스로부터 모델을 조회하는 것뿐만 아니라 새로운 레코드를 삽입할 필요도 있습니다. 다행히도 Eloquent에서는 매우 쉽게 처리할 수 있습니다. 데이터베이스에 새 레코드를 추가하려면, 새로운 모델 인스턴스를 생성하고 속성(attribute)을 설정한 후 해당 인스턴스의 `save` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 비행 정보를 데이터베이스에 저장합니다.
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

이 예시에서는 HTTP 요청으로 받은 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. 그리고 `save` 메서드를 호출하면, 데이터베이스에 레코드가 추가됩니다. 이때, 모델의 `created_at`과 `updated_at` 타임스탬프도 자동으로 저장되므로, 따로 관리할 필요가 없습니다.

또한 `create` 메서드를 사용하여 한 번에 새로운 모델을 저장할 수도 있습니다. `create` 메서드는 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에 모델 클래스에 `fillable` 또는 `guarded` 속성(property)을 지정해야 합니다. 이는, 모든 Eloquent 모델이 기본적으로 일괄 할당(mass assignment) 보안 기능에 의해 보호되기 때문입니다. 일괄 할당에 대한 자세한 내용은 [일괄 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

이미 존재하는 모델을 수정할 때도 `save` 메서드를 사용할 수 있습니다. 모델을 업데이트하려면 우선 해당 모델을 조회한 뒤, 수정할 속성을 변경하고 `save`를 호출하면 됩니다. 역시 `updated_at` 타임스탬프는 자동으로 갱신되므로, 별도로 관리할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

경우에 따라, 이미 존재하는 모델을 수정하거나, 일치하는 모델이 없는 경우 새로 만들고 싶을 수 있습니다. `firstOrCreate`와 마찬가지로, `updateOrCreate` 메서드는 모델을 저장까지 해주므로 별도의 `save` 호출이 필요 없습니다.

아래 예시에서, `departure`가 `Oakland`이고 `destination`이 `San Diego`인 비행기가 이미 존재하면 `price`와 `discounted` 컬럼이 업데이트됩니다. 해당 조건의 비행기가 없다면, 두 배열 인자를 병합한 속성으로 새로운 비행기가 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 수정(Mass Updates)

특정 쿼리와 일치하는 다수의 모델에 대해 한 번에 업데이트를 진행할 수도 있습니다. 아래 예시에서는, `active`가 1이고 `destination`이 `San Diego`인 모든 비행기가 지연(delayed) 상태로 표시됩니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 수정할 컬럼과 값을 배열로 받습니다. 반환 값은 실제로 영향을 받은 행(row)의 개수입니다.

> [!WARNING]
> Eloquent를 통해 대량 수정(Mass Update)이 이루어질 경우, 수정된 모델에 대해 `saving`, `saved`, `updating`, `updated` 등의 모델 이벤트가 발생하지 않습니다. 이는 대량 수정 시 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 내역 확인

Eloquent는 모델의 내부 상태를 확인하고, 모델이 처음 조회됐을 때와 비교해 속성 값이 어떻게 달라졌는지 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

`isDirty` 메서드는 모델이 조회된 이후에 속성 값이 변경되었는지 확인합니다. 특정 속성명(문자열 또는 배열)을 인수로 넘기면 해당 속성들 중 하나라도 변경되었는지 확인할 수 있습니다. 반대로 `isClean` 메서드는 조회 이후 속성이 그대로인지 확인하며, 이 역시 속성명을 선택적으로 지정할 수 있습니다.

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

`wasChanged` 메서드는 현재 요청 사이클 내에서 마지막으로 저장(save)할 때 한 번이라도 변경된 속성이 있는지 확인합니다. 필요에 따라 속성명을 전달해 특정 속성이 변경되었는지도 알 수 있습니다.

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

`getOriginal` 메서드는 모델이 처음 조회되었을 때의 속성(원본) 값을 배열로 반환합니다. 특정 속성명을 전달하면 해당 속성의 원본 값을 반환할 수 있습니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열...
```

`getChanges` 메서드는 마지막으로 모델이 저장되었을 때 변경된 항목들의 배열을 반환하며, `getPrevious`는 마지막 저장 이전의 기존 속성값을 배열로 반환합니다.

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

`create` 메서드를 사용하면 한 번의 PHP 구문으로 모델을 "저장"할 수 있습니다. 생성된 모델 인스턴스가 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에, 모델 클래스에 `fillable` 또는 `guarded` 속성을 반드시 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 일괄 할당 취약점(mass assignment vulnerabilities)으로부터 보호되어 있습니다.

일괄 할당 취약점이란, 사용자가 예상하지 못한 HTTP 요청 필드를 전달하고, 그 필드가 의도치 않게 데이터베이스의 컬럼을 변경하는 상황을 의미합니다. 예를 들어, 악의적인 사용자가 HTTP 요청을 통해 `is_admin` 파라미터를 전달하고, 그 값이 모델의 `create` 메서드에 그대로 전달되어 권한이 없는 사용자가 관리자가 될 수 있습니다.

따라서 시작하려면, 어떤 속성을 일괄 할당 가능(mass assignable)하게 할지 `$fillable` 속성으로 지정해야 합니다. 예를 들어, `Flight` 모델의 `name` 속성만 일괄 할당 가능하게 만들 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 일괄 할당 가능한 속성 목록.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

일괄 할당 가능한 속성을 지정하면, `create` 메서드로 새 레코드를 저장할 수 있습니다. 반환값은 새로 생성된 모델 인스턴스입니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스를 가지고 있다면, `fill` 메서드를 사용해 속성값을 한 번에 할당할 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 일괄 할당과 JSON 컬럼

JSON 컬럼을 다룰 때는, 각 컬럼의 키를 모델의 `$fillable` 배열에 반드시 명시해야 합니다. 보안을 위해 `guarded`를 사용할 때는 중첩 JSON 속성의 업데이트는 지원되지 않습니다.

```php
/**
 * 일괄 할당 가능한 속성 목록.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 전체 일괄 할당 허용

모든 속성을 일괄 할당 가능하게 하려면, 모델의 `$guarded` 속성을 빈 배열로 지정하면 됩니다. 이 경우 Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열을 항상 직접 신중하게 구성해야 합니다.

```php
/**
 * 일괄 할당이 불가능한 속성 목록.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 일괄 할당 예외

기본적으로 `$fillable`에 포함되지 않은 속성은 일괄 할당 연산 시 조용히 무시됩니다. 실제 서비스 환경에서는 이러한 동작이 기대치에 맞지만, 로컬 개발 환경에서는 "왜 값이 반영되지 않을까?" 하는 혼란을 야기할 수 있습니다.

필요하다면, Eloquent의 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 일괄 할당 시 할당 불가 속성이 있을 때 예외를 발생시키도록 구성할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 좋습니다.

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
### 업서트(Upserts)

Eloquent의 `upsert` 메서드를 사용하면 하나의 원자적(atomic) 작업으로 레코드를 업데이트하거나 신규로 생성할 수 있습니다. 첫 번째 인수는 삽입 또는 수정할 값이며, 두 번째 인수는 테이블에서 레코드를 고유하게 식별하는 컬럼 목록, 세 번째 인수는 이미 존재하는 레코드는 어떤 컬럼을 수정할 것인지를 지정합니다. `upsert` 메서드는, 모델에서 타임스탬프 사용이 활성화되어 있으면, `created_at`, `updated_at` 값을 자동으로 설정합니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는, `upsert` 메서드의 두 번째 인수로 지정된 컬럼들이 "primary" 또는 "unique" 인덱스를 반드시 가지고 있어야 합니다. MariaDB, MySQL 드라이버에서는 두 번째 인수를 무시하고 테이블의 "primary" 및 "unique" 인덱스를 활용해 기존 레코드 존재를 판단합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 모델 인스턴스의 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 기존 모델 삭제

위의 예시에서는 먼저 모델을 조회한 뒤 `delete`를 호출합니다. 하지만 모델의 기본키를 알고 있다면, 직접 조회하지 않고 `destroy` 메서드로 삭제할 수 있습니다. `destroy` 메서드는 단일 기본키뿐 아니라, 여러 개의 기본키, 기본키 배열, [컬렉션](/docs/12.x/collections)까지 인수로 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제](#soft-deleting) 모델을 사용하는 경우, `forceDestroy` 메서드를 이용해 영구적으로 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드하고, 각각에 대해 `delete` 메서드를 호출하므로, `deleting`, `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 모델 삭제

물론, Eloquent 쿼리로 삭제 조건을 생성하여, 쿼리 기준에 부합하는 모든 모델을 삭제할 수도 있습니다. 아래 예시에서는 `active`가 0인 모든 비행기가 삭제됩니다. 대량 삭제도 대량 수정과 마찬가지로 삭제된 모델들에 대해 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 모델을 삭제하려면, 아무 조건도 추가하지 않고 쿼리를 실행하면 됩니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent를 통해 대량 삭제를 실행할 경우, 삭제된 모델들에 대해 `deleting`, `deleted` 모델 이벤트가 발생하지 않습니다. 이는 실제로 모델이 조회되지 않고 삭제 명령만 실행되기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

데이터베이스에서 실제로 레코드를 삭제하는 대신, Eloquent에서 "소프트 삭제"를 적용할 수도 있습니다. 소프트 삭제된 모델은 데이터베이스에서 실제로 삭제되는 것이 아니라, 모델의 `deleted_at` 속성에 삭제된 일시 정보가 기록될 뿐입니다. 소프트 삭제를 활성화하려면, 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트(trait)를 추가하세요.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 변환(cast)해줍니다.

데이터베이스 테이블에도 `deleted_at` 컬럼을 추가해야 합니다. 라라벨 [스키마 빌더](/docs/12.x/migrations)의 헬퍼 메서드를 활용해 쉽게 컬럼을 만들 수 있습니다.

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

이제 모델의 `delete` 메서드를 호출하면, `deleted_at` 컬럼이 현재 날짜/시간으로 설정됩니다. 단, 실제로 데이터베이스 레코드는 남아 있습니다. 소프트 삭제가 적용된 모델을 조회할 때는, 삭제된(trashed) 모델들이 자동으로 제외됩니다.

특정 모델 인스턴스가 소프트 삭제됐는지 확인하고 싶다면, `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 복구

소프트 삭제된 모델을 다시 "삭제 취소(복구)"하고 싶다면, 모델 인스턴스의 `restore` 메서드를 호출하면 됩니다. 이 메서드는 모델의 `deleted_at` 컬럼을 `null`로 되돌립니다.

```php
$flight->restore();
```

쿼리에서도 `restore` 메서드를 사용할 수 있으며, 대량 작업과 마찬가지로 복구된 모델에 대해서는 이벤트가 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[연관관계](/docs/12.x/eloquent-relationships) 쿼리를 작성할 때도 `restore` 메서드를 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>

#### 모델 영구 삭제하기

때로는 데이터베이스에서 모델을 완전히 삭제해야 할 때가 있습니다. 이럴 때는 `forceDelete` 메서드를 사용하여 소프트 삭제된 모델을 데이터베이스 테이블에서 완전히 제거할 수 있습니다.

```php
$flight->forceDelete();
```

또한, Eloquent 연관관계 쿼리를 작성할 때도 `forceDelete` 메서드를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 조회하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제된 모델도 조회 결과에 포함하기

앞에서 설명한 것처럼, 소프트 삭제된 모델은 쿼리 결과에서 자동으로 제외됩니다. 하지만, 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 결과에 포함하도록 강제할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed` 메서드는 [연관관계](/docs/12.x/eloquent-relationships) 쿼리를 작성할 때도 사용할 수 있습니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드는 소프트 삭제된 모델만을 **단독으로** 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리(Pruning)

때로는 더 이상 필요하지 않은 모델을 주기적으로 삭제해야 할 때가 있습니다. 이를 위해, 주기적으로 정리하고 싶은 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가할 수 있습니다. 트레이트를 모델에 추가한 후, 더 이상 필요하지 않은 모델을 찾아주는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현합니다.

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
     * 정리 대상이 되는 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable`로 지정한 모델에는 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 전에 호출됩니다. 이 메서드를 활용하면, 예를 들어 모델이 데이터베이스에서 완전히 삭제되기 전에 연결되어 있는 파일 등 추가 자원을 미리 정리할 수 있습니다.

```php
/**
 * 정리 작업 전에 실행됩니다.
 */
protected function pruning(): void
{
    // ...
}
```

정리할 모델을 설정했다면, 애플리케이션의 `routes/console.php` 파일에 `model:prune` Artisan 명령어를 스케줄링해야 합니다. 이 명령어 실행 주기는 자유롭게 결정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

백그라운드에서는 `model:prune` 명령어가 애플리케이션의 `app/Models` 디렉터리 안에 있는 "Prunable" 모델을 자동으로 감지합니다. 만약 모델이 다른 경로에 있다면, `--model` 옵션을 사용해서 모델 클래스명을 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

모든 감지된 모델 중에서 특정 모델은 정리 작업에서 제외하고 싶을 때는 `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`prunable` 쿼리가 잘 동작하는지 테스트하려면, `model:prune` 명령어를 `--pretend` 옵션과 함께 실행하면 됩니다. 이때 실제로 삭제가 진행되지는 않고, 몇 개의 레코드가 정리될 대상을 맞는지만 알려줍니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델도 정리 쿼리에 해당된다면, 영구적으로 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리(Mass Pruning)

모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하면, 대량 삭제 쿼리를 통해 데이터베이스에서 모델이 삭제됩니다. 이 경우, `pruning` 메서드는 호출되지 않으며, `deleting` 및 `deleted` 모델 이벤트도 발생하지 않습니다. 이는 삭제 전에 모델이 실제로 조회되지 않기 때문에, 정리 작업을 훨씬 더 효율적으로 만들어 줍니다.

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
     * 정리 대상이 되는 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제하기

기존 모델 인스턴스를 복제하여 아직 저장되지 않은 복사본을 만들고 싶을 때는 `replicate` 메서드를 사용하면 됩니다. 이 메서드는 서로 많은 속성이 비슷한 모델 인스턴스를 다룰 때 유용하게 활용할 수 있습니다.

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

새 모델로 복제할 때, 하나 이상의 속성을 복제 대상에서 제외하고 싶으면 그 속성명을 배열로 `replicate` 메서드에 전달하면 됩니다.

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
### 글로벌 스코프(Global Scopes)

글로벌 스코프(Global Scope)를 사용하면, 특정 모델의 모든 쿼리에 자동으로 제약 조건을 추가할 수 있습니다. 라라벨의 [소프트 삭제](#soft-deleting) 기능도 글로벌 스코프를 활용해 데이터베이스에서 "삭제되지 않은" 모델만 조회하도록 합니다. 직접 글로벌 스코프를 작성하면 모든 쿼리에서 특정 제약 조건을 자동으로 적용할 때 편리합니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성하기

새로운 글로벌 스코프를 생성하려면 `make:scope` Artisan 명령어를 실행합니다. 생성된 스코프는 애플리케이션의 `app/Models/Scopes` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성하기

글로벌 스코프를 작성하는 것은 매우 간단합니다. 먼저, `make:scope` 명령어로 클래스를 생성하고, 이 클래스가 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하도록 만듭니다. `Scope` 인터페이스는 `apply`라는 단 하나의 메서드만 구현하면 됩니다. `apply` 메서드에서는 필요에 따라 쿼리에 `where` 조건이나 그 외 다양한 절을 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 Eloquent 쿼리 빌더에 스코프를 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 쿼리의 select 절에 컬럼을 추가해야 한다면 `select` 대신 `addSelect` 메서드를 사용해야 합니다. 이를 통해 쿼리의 기존 select 절이 의도치 않게 대체되는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용하기

모델에 글로벌 스코프를 적용하려면, 모델에 `ScopedBy` 속성(Attribute)을 선언하는 방법이 있습니다.

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

또는, 모델의 `booted` 메서드를 오버라이드하여 직접 스코프 인스턴스를 모델의 `addGlobalScope` 메서드에 등록할 수도 있습니다. `addGlobalScope` 메서드는 스코프 인스턴스를 인자로 받습니다.

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

위 예시에서처럼 `App\Models\User` 모델에 스코프를 추가했다면, `User::all()` 메서드를 호출할 때 다음과 같은 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

Eloquent에서는 클래스를 별도로 생성하지 않고도 클로저(익명 함수)를 활용하여 글로벌 스코프를 정의할 수 있습니다. 비교적 간단한 조건이라면 별도의 클래스를 만들 필요 없이 클로저로 구현하는 것이 편리합니다. 클로저를 사용해서 글로벌 스코프를 정의할 때는, `addGlobalScope` 메서드의 첫 번째 인수로 스코프의 이름을 문자열로 지정해야 합니다.

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
            $builder->where('created_at', '<', now()->subYears(2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 글로벌 스코프 해제하기

특정 쿼리에서 글로벌 스코프를 제거하고 싶다면, `withoutGlobalScope` 메서드를 사용하면 됩니다. 이 메서드는 클래스명을 유일한 인수로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의된 글로벌 스코프라면, 해당 스코프 지정에 사용한 문자열 이름을 인수로 넘깁니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 혹은 모든 글로벌 스코프를 동시에 제거하고 싶다면, `withoutGlobalScopes` 메서드를 사용할 수 있습니다.

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프(Local Scopes)

로컬 스코프를 사용하면, 자주 사용하는 쿼리 제약 조건 집합을 간단하게 정의해서 재사용할 수 있습니다. 예를 들어, "인기 있는" 사용자만 반복적으로 조회해야 하는 경우 로컬 스코프를 활용할 수 있습니다. 스코프를 정의하려면, Eloquent 메서드에 `Scope` 속성(Attribute)을 추가하면 됩니다.

스코프 메서드는 항상 동일한 쿼리 빌더 인스턴스 혹은 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 있는 사용자만 포함되도록 쿼리 제한
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 포함되도록 쿼리 제한
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

스코프를 정의한 후에는, 모델을 쿼리할 때 스코프 메서드를 바로 호출할 수 있습니다. 여러 스코프를 체이닝해서 사용할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 쿼리 연산자로 여러 Eloquent 모델 스코프를 결합하려면, [논리 그룹화](/docs/12.x/queries#logical-grouping)을 위해 클로저를 사용할 수도 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 이렇게 하면 코드가 장황해질 수 있으므로, 라라벨에서는 클로저 없이도 스코프를 유연하게 연결할 수 있도록 "하이 오더(higher order)" `orWhere` 메서드를 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프(Dynamic Scopes)

스코프에 매개변수를 전달하고 싶은 경우, 메서드 시그니처에 파라미터를 추가하면 됩니다. 쿼리 빌더(`$query`) 인자 뒤에 파라미터를 추가하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입의 사용자만 포함되도록 쿼리 제한
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

메서드 시그니처에 원하는 인수를 추가했다면, 스코프를 호출할 때 해당 값을 전달하면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 속성(Pending Attributes)

스코프를 사용해, 스코프 쿼리에서 사용한 속성과 동일한 속성을 가진 모델을 생성하고 싶다면, 쿼리를 작성할 때 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 초안만 포함되도록 쿼리 스코프
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

`withAttributes` 메서드는 주어진 속성으로 `where` 조건을 쿼리에 추가하며, 또한 스코프를 사용해 생성하는 모델에도 해당 속성을 자동으로 추가합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드가 쿼리 조건을 추가하지 않고 오직 생성될 모델에만 속성을 부여하도록 하려면, `asConditions` 인수를 `false`로 지정하면 됩니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

가끔 두 모델이 같은지(동일한 엔터티인지) 확인해야 할 때가 있습니다. `is` 및 `isNot` 메서드를 사용하면 두 모델이 같은 기본 키, 테이블, 데이터베이스 연결을 가지는지 쉽게 검증할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is` 및 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/12.x/eloquent-relationships)에서도 사용할 수 있습니다. 쿼리를 추가로 실행하지 않고도 관련 모델을 비교하고 싶을 때 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트(Events)

> [!NOTE]
> Eloquent 이벤트를 클라이언트 사이드 애플리케이션에 직접 브로드캐스트하고 싶나요? 라라벨의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 문서를 참고하세요.

Eloquent 모델은 여러 가지 이벤트를 발생시켜서 모델의 라이프사이클 다음 단계에 후킹할 수 있도록 해줍니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

`retrieved` 이벤트는 기존 모델을 데이터베이스에서 조회할 때 발생합니다. 모델을 처음 저장할 때는 `creating` 및 `created` 이벤트가 발생합니다. 기존 모델을 수정하고 `save` 메서드를 호출하면 `updating` / `updated` 이벤트가 발생합니다. 모델을 생성하거나 업데이트할 때는(속성이 변경되지 않아도) `saving` / `saved` 이벤트가 발생합니다. 이름이 `-ing`으로 끝나는 이벤트는 변경사항이 데이터베이스에 반영되기 **전**에, `-ed`로 끝나는 이벤트는 반영된 **후**에 발생합니다.

모델 이벤트를 리스닝하려면, Eloquent 모델에 `$dispatchesEvents` 속성을 정의하세요. 이 속성은 Eloquent 모델의 여러 단계에 대해 직접 만든 [이벤트 클래스](/docs/12.x/events)와의 매핑을 담당합니다. 각 모델 이벤트 클래스는 생성자에서 영향을 받는 모델 인스턴스를 전달 받게 됩니다.

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
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의하고 매핑한 다음에는, [이벤트 리스너](/docs/12.x/events#defining-listeners)를 사용해 이벤트를 다루면 됩니다.

> [!WARNING]
> Eloquent를 사용해 대량 업데이트 또는 대량 삭제 쿼리를 실행하면, 해당 모델 엔티티에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다. 이는 대량 작업 시 개별적으로 모델이 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저로 이벤트 리스닝

사용자 정의 이벤트 클래스를 만드는 대신, 여러 모델 이벤트가 발생할 때 실행할 클로저를 등록할 수도 있습니다. 일반적으로 이런 클로저는 모델의 `booted` 메서드 안에서 등록합니다.

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

만약 필요하다면, [큐잉 가능한(Background 실행되는) 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)도 모델 이벤트 등록에 사용할 수 있습니다. 이 방법을 사용하면, 라라벨이 해당 이벤트 리스너를 애플리케이션의 [큐](/docs/12.x/queues)를 통해 백그라운드에서 실행하게 됩니다.

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

특정 모델에서 여러 이벤트를 감지해야 한다면, 옵저버(observer)를 사용하여 모든 리스너를 하나의 클래스로 묶을 수 있습니다. 옵저버 클래스의 메서드 이름은 감지하려는 Eloquent 이벤트에 해당하는 이름을 갖게 됩니다. 각각의 메서드는 영향을 받는 모델 인스턴스를 유일한 인수로 전달받습니다. 새로운 옵저버 클래스를 생성하는 가장 쉬운 방법은 `make:observer` Artisan 명령어를 사용하는 것입니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어를 실행하면 새로운 옵저버가 `app/Observers` 디렉터리에 생성됩니다. 만약 해당 디렉터리가 없다면, Artisan이 자동으로 만들어 줍니다. 생성된 옵저버 클래스는 다음과 같은 형태입니다.

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

옵저버를 등록하려면, 해당 모델에 `ObservedBy` 속성(attribute)을 추가할 수 있습니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, 감시하려는 모델에서 `observe` 메서드를 직접 호출해 수동으로 옵저버를 등록할 수도 있습니다. 일반적으로 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 옵저버를 등록합니다.

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
> 옵저버가 감지할 수 있는 이벤트에는 `saving`과 `retrieved`처럼 추가적인 이벤트도 있습니다. 이러한 이벤트에 대해서는 [이벤트(Event)](#events) 문서에서 자세히 설명합니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델 객체들이 데이터베이스 트랜잭션 내에서 생성될 때, 트랜잭션이 커밋된 후에만 옵저버의 이벤트 핸들러를 실행하고 싶은 경우가 있을 수 있습니다. 이럴 때는 옵저버 클래스에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 데이터베이스 트랜잭션이 진행 중이 아니라면, 이벤트 핸들러는 곧바로 실행됩니다.

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
### 이벤트 발생 "음소거"(Mute)하기

가끔 모델에서 발생하는 모든 이벤트를 일시적으로 "음소거(비활성화)"해야 할 때가 있습니다. 이럴 때는 `withoutEvents` 메서드를 사용할 수 있습니다. `withoutEvents` 메서드는 유일한 인수로 클로저(익명 함수)를 받습니다. 이 클로저 내부에서 실행되는 모든 코드는 모델 이벤트를 발생시키지 않으며, 클로저가 반환하는 값이 `withoutEvents`의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델을 이벤트 없이 저장하기

특정 모델 인스턴스를 이벤트를 발생시키지 않고 "저장"하고 싶을 때가 있습니다. 이럴 때는 `saveQuietly` 메서드를 사용하면 됩니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

또한, "update", "delete", "soft delete", "restore", "replicate" 등과 같은 작업도 이벤트를 발생시키지 않고 처리할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```