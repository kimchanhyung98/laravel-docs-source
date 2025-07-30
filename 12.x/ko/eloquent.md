# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 명](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 커넥션](#database-connections)
    - [속성의 기본값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [청크 단위로 결과 처리](#chunking-results)
    - [Lazy 컬렉션을 이용한 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계값 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [일괄 할당](#mass-assignment)
    - [Upsert](#upserts)
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
    - [클로저 사용하기](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)

<a name="introduction"></a>
## 소개

라라벨에는 Eloquent라는 객체-관계 매퍼(ORM)가 내장되어 있어 데이터베이스와 쾌적하게 상호작용할 수 있습니다. Eloquent를 사용할 때 데이터베이스의 각 테이블에는 해당 테이블과 연결되어 상호작용을 담당하는 "모델"이 존재합니다. Eloquent 모델을 이용하면 데이터베이스 테이블에서 레코드를 조회하는 것은 물론, 새로운 레코드를 삽입하거나, 기존 레코드를 수정 및 삭제하는 작업도 쉽게 수행할 수 있습니다.

> [!NOTE]
> 시작하기 전에 반드시 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 커넥션을 구성해야 합니다. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해보겠습니다. 일반적으로 모델 클래스는 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속받아야 합니다. 새로운 모델을 생성하려면 [Artisan 명령어](/docs/12.x/artisan)인 `make:model`을 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 만들고 싶다면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

또한, 모델을 생성하면서 팩토리(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 리퀘스트(form request) 등 다양한 클래스를 동시에 생성할 수도 있습니다. 아래의 옵션들을 조합하여 여러 클래스를 한 번에 생성할 수 있습니다.

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

# 모델, FlightController 리소스 클래스, 폼 리퀘스트 클래스 동시 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러를 한 번에 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트까지 한 번에 생성(단축키)...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

모델의 코드만 보고는 해당 모델에 어떤 속성(attribute)과 연관관계(relationship)가 있는지 파악하기 어려운 경우가 있습니다. 이럴 때는 `model:show` Artisan 명령어를 사용하면 한눈에 모델의 속성과 관계 정보를 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델들은 `app/Models` 디렉터리에 위치하게 됩니다. 기본적인 모델 클래스를 살펴보고 Eloquent에서 적용하는 주요 관례(convention)들을 알아보겠습니다.

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
### 테이블 명

위 예제에서 볼 수 있듯이, Eloquent에게 `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 별도로 지정하지 않았습니다. Eloquent에서는 관례적으로 클래스 이름을 "스네이크 케이스 + 복수형(snake case, plural)"으로 변환해서 테이블명을 결정합니다. 즉, `Flight` 모델은 기본적으로 `flights` 테이블에, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 데이터를 저장한다고 간주합니다.

만약 해당 모델과 연결된 데이터베이스 테이블명이 이 규칙과 다르다면, 모델 클래스 내에 `table` 속성을 직접 정의하여 사용할 테이블명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 연결된 테이블명.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델이 매핑되는 테이블에 `id`라는 이름의 기본 키 컬럼이 있다고 가정합니다. 만약 기본 키 컬럼의 이름이 다르다면, 모델 내에 보호된 `$primaryKey` 속성을 정의하여 다른 컬럼명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블의 기본 키 컬럼명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

추가로, Eloquent는 기본 키가 자동 증가하는 정수값이라고 가정합니다. 즉, Eloquent는 기본 키를 자동으로 정수형으로 변환합니다. 만약 자동 증가가 아니거나 숫자가 아닌 문자열 등 다른 타입의 기본 키를 사용하고 싶다면, 모델에 공개 속성 `$incrementing`을 `false`로 설정해야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * 모델 ID가 자동 증가하는지 여부.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아닌 경우에는, 모델에 보호된 `$keyType` 속성을 `string`으로 지정해야 합니다.

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
#### "복합" 기본 키

Eloquent는 각 모델에 하나의 기본 키(ID)가 반드시 존재해야 하며, 이 값이 모델을 구분할 수 있는 유일한 값 역할을 해야 합니다. Eloquent 모델에서는 "복합 기본 키(두 개 이상의 컬럼을 조합한 키)"를 지원하지 않습니다. 단, 데이터베이스 테이블에서는 복합 유니크 인덱스를 추가해 둘 수 있습니다(이 인덱스는 기본 키와 별개로 구성).

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수값 대신, UUID를 사용할 수도 있습니다. UUID(범용 고유 식별자)는 36자리의 영숫자 문자열로, 전 세계적으로 중복되지 않는 값으로 생성됩니다.

만약 모델에서 자동 증가하는 정수형 키 대신 UUID 키를 사용하고 싶다면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가합니다. 그리고 모델의 [UUID 타입 기본 키 컬럼](/docs/12.x/migrations#column-method-uuid)이 실제로 존재하는지 반드시 확인해야 합니다.

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

기본적으로 `HasUuids` 트레이트는 ["정렬 가능한(ordered) UUID"](/docs/12.x/strings#method-str-ordered-uuid)를 자동으로 생성해줍니다. 이런 UUID는 일반 UUID에 비해 데이터베이스 인덱싱 시 더 효율적으로 저장될 수 있습니다(사전순 정렬이 가능).

원한다면, 모델에서 UUID 생성 방식을 직접 오버라이드할 수도 있습니다. 이를 위해 `newUniqueId` 메서드를 모델에 정의하거나, `uniqueIds` 메서드로 어떤 컬럼에 UUID를 부여할지 지정할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델을 위한 새로운 UUID 생성.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID가 자동 할당될 컬럼명 목록 반환.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26자리의 영숫자 문자열로 조금 더 짧습니다. 또한, 정렬 가능한 성격을 가지고 있어 데이터베이스 인덱싱에 효율적입니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 추가해야 하며, [ULID 타입 기본 키 컬럼](/docs/12.x/migrations#column-method-ulid)도 실제로 존재해야 합니다.

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

기본적으로 Eloquent는 모델과 연관된 데이터베이스 테이블에 `created_at`과 `updated_at` 컬럼이 존재한다고 가정합니다. Eloquent는 모델이 생성되거나 수정될 때 이 컬럼의 값을 자동으로 저장/변경합니다. 만약 이러한 컬럼을 자동으로 관리하고 싶지 않다면, 모델의 `$timestamps` 속성을 `false`로 지정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 타임스탬프 자동 관리 여부.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프의 저장 형식을 커스텀하고 싶다면, 모델의 `$dateFormat` 속성에 원하는 포맷을 지정할 수 있습니다. 이 속성은 데이터베이스에 날짜 속성을 저장하거나, 배열 또는 JSON으로 직렬화될 때의 형식을 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 날짜 컬럼 저장 포맷.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프가 저장될 컬럼의 이름을 변경하고 싶다면, 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 정의할 수 있습니다.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델을 수정하되 `updated_at` 타임스탬프를 변경하지 않고 싶다면, `withoutTimestamps` 메서드에 클로저로 전달하여 모델 작업을 수행할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 커넥션

기본적으로 모든 Eloquent 모델은 애플리케이션에 기본으로 설정된 데이터베이스 커넥션을 사용합니다. 하지만 특정 모델이 특별한 커넥션을 사용해야 한다면, 모델의 `$connection` 속성에 해당 커넥션의 이름을 지정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델에서 사용할 데이터베이스 커넥션명.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 속성의 기본값

새롭게 인스턴스화한 모델 객체에는 기본적으로 속성(attribute) 값이 존재하지 않습니다. 만약 특정 속성에 대해 기본값을 미리 정의하고 싶다면, `$attributes` 속성 배열에 저장할 수 있습니다. 이 배열에는 실제 데이터베이스에서 읽어온 것처럼 "저장 가능한 원시형 값"을 넣어야 합니다.

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
### Eloquent 엄격성 설정

라라벨은 Eloquent의 동작과 "엄격성(strictness)"을 여러 상황에 맞게 조정할 수 있는 다양한 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 인수로 불리언 값을 받아, 지연 로딩(lazy loading)을 방지할지 여부를 설정합니다. 예를 들어, 운영 환경이 아닐 때만 지연 로딩을 비활성화하여, 운영 환경의 정상 작동을 저해하지 않으면서도 개발 환경에서 문제가 조기에 발견되도록 할 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 호출합니다.

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

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출하면, fillable 속성에 추가되지 않은 값을 할당할 때 예외를 발생시키도록 할 수 있습니다. 이 기능은 fillable 배열에 없는 속성에 값을 할당하는 실수를 로컬 개발 환경에서 조기에 감지하는 데 도움이 됩니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)처럼 동작하므로, 해당 모델과 연결된 테이블에서 유연하게 데이터를 조회할 수 있습니다. 모델의 `all` 메서드를 사용하면, 해당 테이블의 모든 레코드를 조회할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

Eloquent의 `all` 메서드는 테이블의 모든 레코드를 반환합니다. 하지만 각 Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries) 역할도 하므로, 조건을 추가한 후 `get` 메서드를 사용하여 원하는 결과만 조회할 수도 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이기 때문에, 라라벨 [쿼리 빌더](/docs/12.x/queries)의 모든 메서드를 함께 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 적극적으로 활용해보세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

데이터베이스에서 조회한 Eloquent 모델 인스턴스를 이미 가지고 있다면, `fresh` 및 `refresh` 메서드를 이용해 모델을 새로고침할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회하여 새로운 인스턴스를 반환하며, 기존 인스턴스에는 영향을 주지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 값으로 다시 불러와 갱신합니다. 또한 이 모델에 이미 로딩된 모든 연관관계도 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 살펴본 Eloquent의 `all` 및 `get` 메서드는 데이터베이스에서 여러 레코드를 조회합니다. 하지만 이들 메서드는 일반 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 객체를 반환합니다.

Eloquent의 `Collection` 클래스는 라라벨의 기본 `Illuminate\Support\Collection` 클래스를 확장하여, [데이터 컬렉션을 다루기 위한 다양한 유용한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 컬렉션에서 특정 조건에 해당하는 모델을 제외시킬 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

라라벨의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 클래스에는 [Eloquent 모델 컬렉션에 특화된 추가 메서드](/docs/12.x/eloquent-collections#available-methods)들도 포함되어 있습니다.

그리고 라라벨의 모든 컬렉션은 PHP의 반복자 인터페이스를 구현하므로, 일반 배열처럼 반복문으로 사용할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크 단위로 결과 처리

`all` 또는 `get` 메서드로 수만 건 이상의 Eloquent 레코드를 한 번에 메모리로 불러오면, 애플리케이션의 메모리가 부족해질 수 있습니다. 이런 경우에는 `chunk` 메서드를 사용하여 대량의 모델을 더 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 Eloquent 모델의 일부분(청크)을 한 번에 조회하고, 이들을 클로저에 전달하여 처리합니다. 즉, 매번 현재 청크만 메모리로 읽어오기 때문에, 많은 수의 데이터를 효율적으로 다룰 수 있습니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 번에 받아올 레코드 개수를 지정합니다. 두 번째 인수로 전달되는 클로저는 조회된 각 청크마다 호출됩니다. 클로저 호출 전후로 데이터베이스 쿼리가 실행되어, 각각의 청크 데이터를 새롭게 로드하게 됩니다.

조회 결과를 기준 컬럼으로 필터링하면서, 동시에 해당 컬럼을 반복(iteration) 중 갱신해야 하는 상황이라면 `chunkById` 메서드를 사용해야 합니다. 이런 경우 `chunk` 메서드를 사용하면 예기치 않은 결과가 발생할 수 있습니다. 내부적으로 `chunkById` 메서드는 이전 청크의 마지막 모델의 `id` 값을 이용해 `id`가 그 값보다 큰 모델만 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 보통은 사용자 조건들을 클로저 안에서 [논리적으로 그룹핑](/docs/12.x/queries#logical-grouping)하여 명확하게 작성하는 것이 좋습니다.

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
### Lazy 컬렉션을 이용한 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 내부적으로 쿼리를 청크 단위로 실행합니다. 다만, 각 청크를 클로저로 넘기는 대신, 결과를 평면화(flatten)된 [LazyCollection](/docs/12.x/collections#lazy-collections) 형태로 반환하여 결과를 단일 스트림처럼 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

반복문 도중 조건 컬럼을 기준으로 데이터를 필터링하면서 해당 컬럼도 계속 업데이트해야 한다면, `lazyById` 메서드를 사용해야 합니다. 내부적으로 이 메서드는 이전 청크의 마지막 모델의 `id` 값 이후의 모델만 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

그리고 `lazyByIdDesc` 메서드를 사용하면 `id` 컬럼의 내림차순 기준으로 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드와 비슷하게, `cursor` 메서드도 수만 건 이상의 Eloquent 모델 레코드를 반복 처리할 때 애플리케이션 메모리 사용량을 획기적으로 줄일 수 있습니다.

`cursor` 메서드는 단 한 번의 데이터베이스 쿼리만 실행하지만, Eloquent 모델 하나가 실제로 반복문에서 사용될 때까지는 인스턴스를 메모리로 불러오지 않습니다. 때문에 반복 처리를 할 때 한 번에 단일 모델만 메모리에 읽어오게 됩니다.

> [!WARNING]
> `cursor` 메서드는 언제나 한 번에 오직 한 개의 Eloquent 모델만 메모리에 보관하므로, eager loading(관계를 미리 로딩)할 수 없습니다. 관계를 미리 불러와야 한다면 [lazy 메서드](#chunking-using-lazy-collections) 사용을 고려하세요.

내부적으로 `cursor` 메서드는 PHP의 [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 동작합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`의 반환값은 `Illuminate\Support\LazyCollection` 인스턴스입니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)을 활용하면 단일 모델만 메모리에 올리면서도 라라벨 컬렉션에서 사용할 수 있는 다양한 메서드를 함께 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, 결국 언젠가는 메모리가 부족해질 수 있습니다. 이는 [PHP의 PDO 드라이버가 내부적으로 모든 원시 쿼리 결과를 버퍼에 저장하기 때문](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 아주 많은 레코드를 다루어야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 다양한 고급 서브쿼리 기능을 제공합니다. 이를 활용하면 하나의 쿼리로 여러 관련 테이블의 정보를 가져올 수 있습니다. 예를 들어, `destinations` 테이블(도착지)과 `flights` 테이블(각 도착지로의 비행)이 있다고 가정합니다. `flights` 테이블에는 해당 비행이 도착지에 도착한 시점을 나타내는 `arrived_at` 컬럼이 존재합니다.

쿼리 빌더의 `select` 및 `addSelect` 메서드를 사용한 서브쿼리를 통해, 모든 `destinations`와 해당 도착지에 가장 최근에 도착한 비행기의 이름을 단일 쿼리로 조회할 수 있습니다.

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
#### 서브쿼리로 정렬하기

또한, 쿼리 빌더의 `orderBy` 함수 역시 서브쿼리를 지원합니다. 앞선 예시와 같이, 각 도착지에 마지막으로 도착한 비행기 도착 시간을 기준으로 모든 도착지를 정렬할 수도 있습니다. 이 역시 단일 데이터베이스 쿼리로 가능합니다.

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

주어진 쿼리에 해당하는 모든 레코드를 조회할 수 있을 뿐 아니라, `find`, `first`, `firstWhere` 등의 메서드를 통해 단일 레코드를 조회할 수도 있습니다. 이 메서드들은 여러 모델의 컬렉션이 아니라 단일 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본 키로 모델을 조회...
$flight = Flight::find(1);

// 쿼리 조건에 맞는 첫 번째 모델을 조회...
$flight = Flight::where('active', 1)->first();

// 조건에 맞는 첫 번째 모델을 조회하는 또 다른 방법...
$flight = Flight::firstWhere('active', 1);
```

결과가 없을 경우 특정 동작을 수행하고 싶을 수도 있습니다. `findOr`와 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과가 없을 경우 주어진 클로저를 실행합니다. 클로저의 반환값이 해당 메서드의 반환값으로 사용됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Not Found 예외 처리

조회 결과가 없을 때 예외를 발생시키고 싶을 수도 있습니다. 이는 라우트나 컨트롤러에서 유용하게 활용할 수 있습니다. `findOrFail`, `firstOrFail` 메서드는 쿼리 결과 중 첫 번째 값을 반환하며, 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 잡히지 않은 경우, 404 HTTP 응답이 자동으로 사용자(클라이언트)에게 반환됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 지정한 컬럼/값 쌍을 사용하여, 데이터베이스에서 레코드를 찾으려고 시도합니다. 만약 모델을 찾지 못하면, 첫 번째 배열 인자와 선택적 두 번째 배열 인자를 병합한 속성값으로 새 레코드를 데이터베이스에 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 비슷하게 지정한 속성에 해당하는 레코드를 찾으려 시도합니다. 다만, 모델을 찾지 못하면 새 모델 인스턴스를 반환합니다. 단, `firstOrNew`가 반환하는 모델은 아직 데이터베이스에 저장되지 않은 상태이므로, 직접 `save` 메서드를 호출해서 저장해야 합니다.

```php
use App\Models\Flight;

// 이름으로 flight를 조회하거나, 없다면 새로 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름, delayed, arrival_time 속성으로 조회하거나 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 flight를 조회하거나, 새 Flight 인스턴스 생성...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름, delayed, arrival_time으로 조회하거나 새 인스턴스 생성...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>

### 집계값 조회하기

Eloquent 모델을 사용할 때, Laravel [쿼리 빌더](/docs/12.x/queries)가 제공하는 `count`, `sum`, `max`와 같은 [집계 메서드](/docs/12.x/queries#aggregates)를 함께 사용할 수 있습니다. 이 메서드들은 예상대로 Eloquent 모델 인스턴스가 아닌 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 레코드 삽입

물론 Eloquent를 사용할 때는 데이터베이스에서 모델을 조회하는 것만 아니라 새로운 레코드를 삽입하는 작업도 필요합니다. Eloquent는 이러한 작업도 아주 간단하게 처리할 수 있습니다. 데이터베이스에 새 레코드를 삽입하려면, 새로운 모델 인스턴스를 생성하고 속성(attribute)을 설정합니다. 이후, 모델 인스턴스에서 `save` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

위 예시에서, HTTP 요청에서 받은 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. 그리고 `save` 메서드를 호출하면 데이터베이스에 레코드가 삽입됩니다. 이 때 `created_at`과 `updated_at` 타임스탬프도 자동으로 설정되므로, 별도로 값을 지정할 필요가 없습니다.

또는, `create` 메서드를 사용해 한 줄의 PHP 코드로 새로운 모델을 "저장"할 수도 있습니다. `create` 메서드는 저장된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하기 전에 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이는 모든 Eloquent 모델이 기본적으로 대량 할당(mass assignment) 취약점으로부터 보호되기 때문입니다. 대량 할당에 대한 자세한 설명은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 레코드 수정

`save` 메서드는 이미 데이터베이스에 존재하는 모델을 수정할 때도 사용할 수 있습니다. 모델을 수정하려면, 먼저 원하는 모델을 조회하고, 변경할 속성에 값을 할당한 뒤, 다시 `save` 메서드를 호출하면 됩니다. 이때 역시 `updated_at` 타임스탬프는 자동으로 갱신되므로, 따로 값을 할당할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

특정 모델이 있으면 수정하고, 없으면 새로 만들어야 할 경우도 있습니다. `firstOrCreate`와 마찬가지로, `updateOrCreate` 메서드는 해당 조건의 모델을 저장하므로, 따로 `save`를 호출할 필요가 없습니다.

아래 예시에서, `departure`가 `Oakland`이고 `destination`이 `San Diego`인 flight가 이미 존재한다면 해당 flight의 `price`와 `discounted` 컬럼이 업데이트됩니다. 만약 해당하는 flight가 없다면, 두 번째 인자로 전달한 속성이 병합되어 새로운 flight가 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트(Mass Updates)

특정 쿼리에 맞는 여러 모델을 한 번에 업데이트할 수도 있습니다. 아래 예시에서는 `active`가 1이고 `destination`이 `San Diego`인 모든 flight가 지연(delayed) 처리됩니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼과 값의 쌍을 배열로 전달받습니다. 또한, 이 메서드는 영향을 받은(업데이트된) 행(row)의 개수를 반환합니다.

> [!WARNING]
> Eloquent로 대량 업데이트를 수행할 때는, 해당 모델에 대해 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. 이는 대량 업데이트 시 실제로 모델 인스턴스를 조회하지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 내역 확인

Eloquent는 모델의 내부 상태를 확인하거나, 특정 속성이 언제 어떻게 변경되었는지 파악할 수 있도록 `isDirty`, `isClean`, `wasChanged` 등의 메서드를 제공합니다.

`isDirty` 메서드는 모델을 조회한 이후 속성이 변경되었는지를 확인합니다. 특정 속성명이나 속성명 배열을 전달하여 해당 속성(들)이 변경되었는지도 확인할 수 있습니다. 반대로 `isClean` 메서드는 속성이 변경되지 않고 동일하게 유지되고 있는지를 확인합니다. 이 메서드 역시 옵션으로 속성명을 받을 수 있습니다.

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

`wasChanged` 메서드는 모델이 최근 저장될 때(현재 요청 내에서) 속성 중 실제로 값이 변경되었는지 알려줍니다. 필요한 경우 특정 속성명을 인자로 넘겨 해당 속성의 변경 여부만 확인할 수 있습니다.

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

`getOriginal` 메서드는 모델을 처음 조회했을 당시의 속성값 배열을 반환합니다. 필요하다면 속성명을 지정해 해당 속성의 초기값만 받을 수도 있습니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원래의 모든 속성을 포함한 배열...
```

`getChanges`는 모델이 마지막으로 저장되었을 때 변경된 속성들만 배열로 반환하며, `getPrevious`는 마지막 저장 직전에 가지고 있던 속성값을 배열로 반환합니다.

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

PHP의 한 줄 코드를 통해 새 모델을 "저장"할 때 `create` 메서드를 사용할 수 있습니다. `create` 메서드는 저장된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만, `create` 메서드를 사용하기 전에 모델 클래스에 반드시 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이는 모든 Eloquent 모델이 기본적으로 대량 할당 취약점으로부터 보호되고 있기 때문입니다.

대량 할당 취약점은 사용자가 예기치 않은 HTTP 요청 필드를 전달할 때 발생할 수 있습니다. 이로 인해, 원래 의도하지 않은 데이터베이스 컬럼이 변경될 수 있습니다. 예를 들어 악의적인 사용자가 `is_admin` 파라미터를 전송하고, 이 값이 모델의 `create` 메서드로 전달된다면 관리자 권한이 부여되는 일이 생길 수도 있습니다.

따라서, 대량 할당을 허용할 모델 속성을 명확하게 지정해야 합니다. 모델의 `$fillable` 속성에 할당할 수 있는 속성명을 배열로 선언해주면 됩니다. 아래 예시에서는 `Flight` 모델의 `name` 속성을 대량 할당이 가능하도록 설정했습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

대량 할당 가능한 속성 배열을 지정했다면, 위에서 설명한 `create` 메서드를 사용해 새 레코드를 추가할 수 있습니다. `create`는 새로 생성된 모델 인스턴스를 반환합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드를 사용해 속성값을 한번에 할당할 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 대량 할당하려면, 각 컬럼의 할당 키(예: `options->enabled`)를 `$fillable` 배열에 명시해야 합니다. 보안상, 라라벨은 `guarded` 속성을 사용하는 상황에서 중첩된 JSON 속성의 업데이트를 지원하지 않습니다.

```php
/**
 * The attributes that are mass assignable.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 대량 할당 허용

모델의 **모든** 속성을 대량 할당 가능하게 하려면, `$guarded` 속성을 빈 배열로 지정하면 됩니다. 단, 이 경우에는 `fill`, `create`, `update`에 전달하는 배열을 항상 직접 신중하게 작성해야 합니다.

```php
/**
 * The attributes that aren't mass assignable.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 포함되지 않은 속성들은 대량 할당을 시도해도 아무런 동작 없이 무시됩니다. 프로덕션 환경에서는 이것이 기대한 동작이지만, 로컬 개발 환경에서는 왜 데이터가 반영되지 않는지 혼란을 줄 수 있습니다.

원한다면, 대량 할당할 수 없는 속성에 값을 할당하려 할 때 예외가 발생하도록 설정할 수 있습니다. 이를 위해 `preventSilentlyDiscardingAttributes` 메서드를 사용할 수 있으며, 일반적으로 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upsert

Eloquent의 `upsert` 메서드는 한 번의 원자적(atomic) 동작으로 여러 레코드를 업데이트 또는 생성할 때 사용할 수 있습니다. 첫 번째 인자는 삽입 또는 업데이트할 값 배열이고, 두 번째 인자는 각 레코드를 고유하게 식별하는 컬럼(들)을 지정합니다. 마지막 세 번째 인자는 이미 존재하는 레코드가 있을 때 업데이트할 컬럼(들)을 지정합니다. 타임스탬프가 활성화된 경우 `created_at`과 `updated_at` 값도 자동으로 세팅됩니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인자(고유 식별 컬럼)에 "primary" 또는 "unique" 인덱스가 필요합니다. 또한, MariaDB와 MySQL 드라이버의 경우 두 번째 인자가 항상 테이블의 "primary" 및 "unique" 인덱스를 사용하여 기존 레코드를 식별합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 해당 모델 인스턴스에서 `delete` 메서드를 호출합니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 삭제

위 예시처럼 삭제 전에 먼저 해당 모델을 데이터베이스에서 조회할 수 있습니다. 하지만, 모델의 기본 키 값을 알고 있다면, `destroy` 메서드를 사용해 명시적으로 조회하지 않고도 삭제할 수 있습니다. `destroy`는 단일 기본 키뿐만 아니라, 여러 개의 키, 기본 키 배열, 또는 [컬렉션](/docs/12.x/collections)도 인수로 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제](#soft-deleting)를 사용하는 경우, `forceDestroy`를 통해 해당 모델을 완전히 삭제할 수도 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드한 후 `delete`를 호출하므로, 각 모델에 대해 `deleting`, `deleted` 이벤트가 올바르게 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 사용한 모델 삭제

특정 조건에 부합하는 모든 모델을 삭제하려면 Eloquent 쿼리를 사용할 수 있습니다. 아래 예시에서는 `active`가 0인 flight를 모두 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제는 각 모델에 대한 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블 내 모든 모델을 삭제하려면 조건 없이 쿼리를 실행하면 됩니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent에서 대량 삭제 문장을 실행할 때는, 삭제된 모델에 대해 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 이는 삭제 시 모델이 실제로 조회되지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제(Soft Deleting)

데이터베이스에서 레코드를 진짜로 삭제하는 대신, Eloquent는 "소프트 삭제" 기능도 제공합니다. 소프트 삭제되는 경우 레코드는 삭제되지 않고, 대신 `deleted_at` 속성에 삭제 시각이 기록됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트(trait)를 추가하면 됩니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 변환해줍니다.

데이터베이스 테이블에 `deleted_at` 컬럼도 추가해야 합니다. Laravel [스키마 빌더](/docs/12.x/migrations)는 이 컬럼을 쉽게 추가해주는 헬퍼 메서드를 제공합니다.

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

이제 모델에서 `delete` 메서드를 호출하면 `deleted_at` 컬럼에 현재 일시가 기록됩니다. 실제로는 데이터베이스에서 레코드가 삭제되지 않습니다. 소프트 삭제 기능이 활성화된 모델을 조회하면, 소프트 삭제된 레코드는 자동으로 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

때로는 소프트 삭제된 모델을 "복구"하고 싶을 수 있습니다. 이럴 때는 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. 이 메서드는 모델의 `deleted_at` 값을 `null`로 되돌립니다.

```php
$flight->restore();
```

쿼리에서 여러 모델을 한 번에 복구할 수도 있습니다. 역시, 대량 조작과 마찬가지로 해당 모델에 대한 이벤트는 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[관계](/docs/12.x/eloquent-relationships) 쿼리에서도 `restore` 메서드를 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 소프트 삭제 모델 완전 삭제

경우에 따라 모델을 데이터베이스에서 완전히 삭제하고 싶을 수 있습니다. 소프트 삭제된 모델의 경우, `forceDelete` 메서드를 호출하면 해당 레코드가 테이블에서 영구적으로 제거됩니다.

```php
$flight->forceDelete();
```

Eloquent 관계(relationship) 쿼리에서도 `forceDelete`를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델까지 함께 조회

앞서 설명했던 것처럼, 소프트 삭제된 모델은 기본적으로 쿼리 결과에서 자동으로 제외됩니다. 하지만, 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 결과에 포함시킬 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed`는 [관계](/docs/12.x/eloquent-relationships) 쿼리에서도 사용할 수 있습니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회

`onlyTrashed` 메서드는 소프트 삭제된 모델만 **오직** 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning Models)

불필요해진 모델을 주기적으로 정리하여 삭제하고 싶을 때가 있습니다. 이를 위해 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가할 수 있습니다. 트레이트를 추가한 후, 필요한 모델만 선별할 수 있도록 `prunable` 메서드를 구현하면 됩니다. 이 메서드는 더 이상 필요하지 않은 모델을 조회하는 Eloquent 쿼리 빌더를 반환해야 합니다.

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
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

모델을 `Prunable`로 표시했다면, `pruning` 메서드도 구현할 수 있습니다. 이 메서드는 모델이 삭제되기 직전에 호출되며, 예를 들어 저장된 파일 등 모델과 연관된 데이터를 미리 삭제하고자 할 때 유용합니다.

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```

가지치기 모델 설정이 끝나면, 애플리케이션의 `routes/console.php` 파일에 `model:prune` Artisan 명령어를 스케줄링해야 합니다. 실행 주기는 자유롭게 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

내부적으로 `model:prune` 명령어는 `app/Models` 디렉터리 내에서 "Prunable" 모델을 자동으로 탐지합니다. 만약 모델이 다른 위치에 있다면 `--model` 옵션을 사용해 클래스명을 직접 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

모든 모델 중 특정 모델만 가지치기에서 제외하고 싶다면, `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션과 함께 `model:prune` 명령어를 실행하면 쿼리 결과 실제로 얼마나 많은 레코드가 삭제될지 미리 확인할 수도 있습니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 쿼리 조건에 맞는 소프트 삭제 모델도 가지치기 대상이 된다면, 해당 모델은 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하는 모델은, 삭제할 때 대량 삭제 쿼리가 사용됩니다. 이 경우, `pruning` 메서드는 호출되지 않으며, `deleting`, `deleted` 등의 이벤트도 발생하지 않습니다. 즉, 대량 가지치기는 실제로 모델을 조회하지 않아 더욱 효율적으로 처리됩니다.

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
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 복제해, 아직 저장되지 않은 새 인스턴스를 만들 때는 `replicate` 메서드를 사용할 수 있습니다. 동일한 속성이 많은 모델을 여러 개 생성해야 할 때 유용합니다.

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

복제에서 특정 속성을 제외하려면, 제외할 속성 배열을 `replicate` 메서드에 전달하면 됩니다.

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

글로벌 스코프는 특정 모델에 대한 **모든** 쿼리에 제약 조건을 추가할 수 있는 기능입니다. 라라벨의 [소프트 삭제](#soft-deleting) 기능도 글로벌 스코프를 활용하여, 삭제되지 않은(활성) 모델만 자동으로 조회하도록 구현되어 있습니다. 직접 글로벌 스코프를 만들면, 해당 모델이 사용되는 모든 쿼리에 공통된 조건을 일관성 있게 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

새로운 글로벌 스코프를 생성하려면, `make:scope` Artisan 명령어를 실행하면 됩니다. 이 명령어는 생성한 스코프 파일을 애플리케이션의 `app/Models/Scopes` 디렉터리에 저장합니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프는 비교적 간단하게 작성할 수 있습니다. 먼저, `make:scope` 명령어로 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 생성합니다. 이 인터페이스에는 `apply`라는 단 하나의 메서드만 구현하면 됩니다. `apply` 메서드 안에서 쿼리에 `where` 조건 등 필요한 절(clause)을 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프에서 쿼리의 select 절에 컬럼을 추가하려면, 기존의 select 절이 의도치 않게 대체되지 않도록 반드시 `addSelect` 메서드를 사용해야 합니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용하기

글로벌 스코프를 모델에 적용하려면, 해당 모델에 `ScopedBy` 속성을 추가하면 됩니다.

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

또는, 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope` 메서드로 직접 스코프를 등록할 수도 있습니다. 이 메서드는 인수로 스코프 인스턴스를 받습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예시처럼 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 실행 시 아래와 같은 SQL 쿼리가 수행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>

#### 익명 글로벌 스코프

Eloquent에서는 클래스 파일을 따로 만들 필요가 없는 간단한 글로벌 스코프의 경우, 클로저(익명 함수)를 사용하여 글로벌 스코프를 정의할 수도 있습니다. 클로저를 사용해 글로벌 스코프를 정의할 때는, `addGlobalScope` 메서드의 첫 번째 인수로 사용자가 원하는 스코프 이름을 지정해야 합니다.

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

특정 쿼리에서 글로벌 스코프를 제거하고 싶다면, `withoutGlobalScope` 메서드를 사용할 수 있습니다. 이 메서드는 글로벌 스코프 클래스명을 유일한 인수로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

혹은, 글로벌 스코프를 클로저로 정의했다면, 할당한 글로벌 스코프의 문자열 이름을 전달해야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 전체 글로벌 스코프를 제거하려면 `withoutGlobalScopes` 메서드를 사용할 수 있습니다.

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 애플리케이션 전반에서 자주 사용할 수 있는 쿼리 제약조건을 공통적으로 정의할 때 유용합니다. 예를 들어, "인기 있는" 사용자만 자주 조회해야 할 때 사용할 수 있습니다. 스코프를 정의하려면, Eloquent 메서드에 `Scope` 어트리뷰트를 추가하세요.

스코프 메서드는 항상 동일한 쿼리 빌더 인스턴스나 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 쿼리를 인기 있는 사용자로 제한하는 스코프.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 쿼리를 활성 사용자로 제한하는 스코프.
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

스코프를 정의한 뒤에는 모델 쿼리 시 스코프 메서드를 호출할 수 있습니다. 여러 스코프를 연쇄적으로 호출하는 것도 가능합니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 개의 Eloquent 모델 스코프를 `or` 쿼리 연산자로 결합하려면, 올바른 [논리 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 이 방법은 불편할 수 있으므로, 라라벨에서는 클로저 없이 스코프를 더욱 유연하게 연결할 수 있는 "고차" `orWhere` 메서드를 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 매개변수를 전달하고 싶을 때가 있습니다. 이럴 땐, 스코프 메서드의 시그니처에 원하는 추가 매개변수를 정의하기만 하면 됩니다. 이때 스코프 매개변수는 `$query` 매개변수 뒤에 작성해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 전달된 타입의 사용자만 포함하는 쿼리 스코프.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

스코프 메서드에 필요한 인수를 추가한 후에는, 스코프 호출 시 인수를 전달하면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending 속성들

스코프를 활용해 쿼리에서 제한에 사용한 속성과 동일한 속성을 가진 모델을 생성하고 싶다면, 스코프 쿼리 작성 시 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 쿼리를 임시글(초안)만 포함하도록 제한하는 스코프.
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

`withAttributes` 메서드는 주어진 속성을 이용해 쿼리에 `where` 조건을 추가하고, 또한 스코프를 통해 생성되는 모델에 해당 속성을 추가합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않게 하려면, `asConditions` 인수를 `false`로 지정하면 됩니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

때로는 두 모델이 "동일"한지 판별해야 할 때가 있습니다. `is` 및 `isNot` 메서드를 사용하면 두 모델의 기본 키, 테이블, 데이터베이스 연결이 같은지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`와 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne`과 같은 [연관관계](/docs/12.x/eloquent-relationships) 사용 시에도 지원됩니다. 이 메서드는 쿼리 없이 연관된 모델을 비교하고 싶을 때 특히 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 직접 클라이언트 사이드 애플리케이션으로 브로드캐스트하고 싶으신가요? 라라벨의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 기능을 참고하세요.

Eloquent 모델은 여러 종류의 이벤트를 디스패치(발송)하여, 모델 생명주기의 각 순간에 후킹할 수 있도록 도와줍니다. 지원되는 이벤트로는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등이 있습니다.

`retrieved` 이벤트는 기존 모델을 데이터베이스에서 가져왔을 때 발생합니다. 새 모델을 처음 저장하면 `creating`과 `created` 이벤트가 디스패치됩니다. 기존 모델을 수정하고 `save`를 호출할 때는 `updating` / `updated` 이벤트가, 모델을 생성 또는 업데이트할 때(속성이 변경되지 않은 경우에도)는 `saving` / `saved` 이벤트가 각각 실행됩니다. 이벤트 이름이 `-ing`으로 끝나면 모델 변경이 실제로 저장되기 전에, `-ed`로 끝나면 저장된 후에 디스패치된다는 점을 기억하세요.

모델 이벤트를 수신하려면, Eloquent 모델에 `$dispatchesEvents` 프로퍼티를 정의하세요. 이 프로퍼티는 Eloquent 모델 생명주기의 여러 지점을 사용자 정의 [이벤트 클래스](/docs/12.x/events)에 매핑합니다. 각 모델 이벤트 클래스는 생성자를 통해 영향을 받는 모델 인스턴스를 전달받을 것으로 예상합니다.

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
     * 모델 이벤트 맵.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의하고 매핑한 후에는 [이벤트 리스너](/docs/12.x/events#defining-listeners)를 통해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 사용해 대량의 update 또는 delete 쿼리를 실행하면, 영향을 받는 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트가 디스패치되지 않습니다. 대량 업데이트 또는 삭제 시 실제로 모델을 조회하지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저를 활용한 이벤트 등록

별도의 이벤트 클래스를 사용하지 않고, 다양한 모델 이벤트가 디스패치될 때 실행되는 클로저를 등록할 수도 있습니다. 일반적으로 이러한 클로저는 모델의 `booted` 메서드 안에서 등록합니다.

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

필요하다면 모델 이벤트 리스너 등록 시 [큐 지원 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 활용할 수도 있습니다. 이 경우, 라라벨이 모델 이벤트 리스너를 애플리케이션의 [큐](/docs/12.x/queues)에서 백그라운드로 실행하도록 지시할 수 있습니다.

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

특정 모델에 대해 여러 이벤트를 동시에 수신하고 싶을 경우, 개별 리스너 대신 옵저버 클래스로 리스너를 한 곳에 모을 수 있습니다. 옵저버 클래스의 메서드 이름은 수신하고자 하는 Eloquent 이벤트명과 일치해야 하며, 각 메서드는 영향을 받는 모델을 유일한 인수로 전달받습니다. 새로운 옵저버 클래스를 만들려면, `make:observer` Artisan 명령어를 사용하는 것이 가장 편리합니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어는 새 옵저버를 `app/Observers` 디렉터리에 생성합니다. 해당 디렉터리가 없다면 Artisan이 자동으로 만들어 줍니다. 생성된 옵저버는 다음과 같은 모습을 가집니다.

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 핸들러.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 핸들러.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 핸들러.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 핸들러.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 핸들러.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버 등록은 해당 모델에 `ObservedBy` 어트리뷰트를 추가하여 할 수 있습니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

혹은, 옵저버를 수동으로 등록하려면 대상 모델에서 `observe` 메서드를 호출하면 됩니다. 일반적으로 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 옵저버를 등록할 수 있습니다.

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
> 옵저버가 수신할 수 있는 추가 이벤트(ex: `saving`, `retrieved`)도 있습니다. 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 데이터베이스 트랜잭션 내에서 생성되고 있을 때, 옵저버가 이벤트 핸들러를 트랜잭션 커밋 이후에만 실행하도록 하고 싶을 수 있습니다. 이 경우, 옵저버에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 만약 트랜잭션이 진행 중이 아니라면 이벤트 핸들러는 즉시 실행됩니다.

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 핸들러.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 일시 중지(Muting Events)

모델에서 발생하는 모든 이벤트를 잠시 "무시(mute)"해야 할 때가 있습니다. 이런 경우, `withoutEvents` 메서드를 사용하면 됩니다. 이 메서드는 클로저를 유일한 인수로 받으며, 해당 클로저 내부에서 실행되는 코드는 모델 이벤트를 디스패치하지 않습니다. 그리고 클로저의 반환값이 곧 `withoutEvents` 메서드의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 저장 시 이벤트 발생 방지

특정 모델을 저장하면서 이벤트를 발생시키지 않으려면 `saveQuietly` 메서드를 사용할 수 있습니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

또한 특정 모델에 대해 "업데이트", "삭제", "소프트 삭제", "복원", "복제" 작업도 모든 이벤트를 발생시키지 않고 실행할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```