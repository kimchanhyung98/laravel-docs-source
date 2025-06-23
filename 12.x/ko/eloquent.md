# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 커넥션](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격 모드 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과를 청킹해서 가져오기](#chunking-results)
    - [Lazy 컬렉션으로 청킹하기](#chunking-using-lazy-collections)
    - [커서(Cursors)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계값 조회](#retrieving-single-models)
    - [모델 조회 또는 생성하기](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
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
    - [옵저버(Observer)](#observers)
    - [이벤트 음소거(Muting Events)](#muting-events)

<a name="introduction"></a>
## 소개

라라벨에는 Eloquent라는 객체 관계 매퍼(ORM)가 포함되어 있어 데이터베이스를 쉽고 즐겁게 다룰 수 있습니다. Eloquent를 사용할 때는 데이터베이스의 각 테이블마다 해당 테이블과 상호작용할 수 있는 "모델"이 하나씩 존재합니다. Eloquent 모델을 이용하면 테이블에서 레코드를 조회할 뿐만 아니라, 레코드를 테이블에 삽입, 수정, 삭제하는 것 역시 손쉽게 처리할 수 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 커넥션을 먼저 설정해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/12.x/database#configuration)를 참고해 주십시오.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

이제 Eloquent 모델을 하나 만들어 보겠습니다. 일반적으로 모델 클래스는 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속받아 만듭니다. 새로운 모델을 생성할 때는 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/12.x/migrations) 파일도 함께 만들고 싶다면, `--migration` 또는 `-m` 옵션을 붙이면 됩니다.

```shell
php artisan make:model Flight --migration
```

모델을 생성하면서 팩토리, 시더, 정책(Policy), 컨트롤러, 폼 요청 등 다양한 클래스를 함께 만들 수도 있습니다. 아래와 같이 여러 옵션을 조합해서 한 번에 여러 클래스를 생성하는 것도 가능합니다.

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

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러까지 한 번에 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청까지 모두 생성하는 단축키...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 중간(pivot) 테이블용 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

때때로 코드만 훑어봐서는 모델이 어떤 속성(attribute)과 연관관계(relationship)를 가지고 있는지 한눈에 파악하기 어렵습니다. 이럴 때 `model:show` Artisan 명령어를 이용하면, 해당 모델의 속성과 연관관계를 간편하게 한눈에 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성한 모델들은 기본적으로 `app/Models` 디렉토리에 저장됩니다. 기본적인 모델 클래스를 예로 들면서, Eloquent의 주요 관례에 대해 살펴보겠습니다.

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

위의 예시에서 Eloquent에게 `Flight` 모델이 어떤 데이터베이스 테이블과 대응되는지 따로 지정하지 않은 것을 볼 수 있습니다. Eloquent는 별도로 테이블명을 지정하지 않으면, 클래스명을 "스네이크 케이스(snake case)"의 복수형으로 바꾼 이름을 테이블명으로 사용합니다. 즉, `Flight` 모델은 기본적으로 `flights` 테이블과 연결되어 있고, `AirTrafficController` 모델이라면 `air_traffic_controllers` 테이블과 연결된다고 Eloquent는 가정합니다.

만약 해당 모델이 연결되어야 할 테이블명이 이 규칙과 다르다면, 모델에 `table` 프로퍼티를 직접 정의해서 테이블명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 연결된 테이블명
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델의 데이터베이스 테이블에 `id`라는 이름의 기본 키(primary key) 컬럼이 있다고 가정합니다. 만약 이와 다른 컬럼을 기본 키로 사용해야 한다면, 모델에 protected `$primaryKey` 프로퍼티를 정의하여 사용하려는 컬럼명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 테이블과 연결된 기본 키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, Eloquent는 기본 키가 자동 증가하는 정수(integer)라고 가정하여, 자동으로 해당 값을 정수로 변환합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용하려면, 모델에서 public `$incrementing` 프로퍼티를 `false`로 설정해야 합니다.

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

기본 키가 정수가 아니라면, 모델에서 protected `$keyType` 프로퍼티를 정의하여 타입을 `string`으로 지정해 주어야 합니다.

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

Eloquent 모델은 반드시 하나의 고유 "ID"를 필요로 하며, 이 값이 기본 키 역할을 합니다. "복합" 기본 키(두 개 이상의 컬럼으로 이루어진 기본 키)는 Eloquent에서 지원되지 않습니다. 하지만, 테이블에는 추가로 여러 컬럼의 조합으로 유니크 인덱스를 만들 수 있습니다. 단, 기본 키는 하나의 컬럼을 사용해야 합니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가하는 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자리의 영문자와 숫자로 이루어진 범용 고유 식별자입니다.

자동 증가하는 정수 대신 모델에서 UUID를 기본 키로 사용하고 싶다면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레잇을 추가하면 됩니다. 또한, 해당 모델의 [UUID 타입의 기본 키 컬럼](/docs/12.x/migrations#column-method-uuid)을 반드시 데이터베이스에 생성해야 합니다.

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

기본적으로 `HasUuids` 트레잇은 모델에 ["정렬 가능한(ordered) UUID"](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 이런 타입의 UUID는 색인(index)이 적용된 데이터베이스에서 더 효율적으로 정렬, 저장될 수 있습니다.

모델에서 UUID 생성 방법을 커스터마이즈하고 싶다면, `newUniqueId` 메서드를 모델에 직접 정의할 수 있습니다. 또한, 어떤 컬럼에 UUID를 할당할지 `uniqueIds` 메서드로 지정할 수도 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델에 사용할 신규 UUID를 생성합니다.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자(UUID)를 부여할 컬럼을 지정합니다.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만, 26자리로 더 짧고, 마찬가지로 정렬이 효율적이어서 색인을 위해 적합합니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레잇을 추가하고, [ULID 타입의 기본 키 컬럼](/docs/12.x/migrations#column-method-ulid)을 생성해두어야 합니다.

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

기본적으로 Eloquent는 모델과 연관된 데이터베이스 테이블에 `created_at`과 `updated_at` 컬럼이 존재하는 것으로 가정합니다. 그리고 모델이 생성되거나 업데이트될 때 이 값들을 자동으로 관리합니다. 만약 Eloquent가 이런 컬럼을 자동으로 관리하지 않게 하려면, 모델의 `$timestamps` 프로퍼티 값을 `false`로 설정하면 됩니다.

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

타임스탬프의 저장 포맷을 커스터마이즈하려면 모델의 `$dateFormat` 프로퍼티를 설정할 수 있습니다. 이 속성은 데이터베이스에 날짜 속성이 저장되는 형식과, 모델이 배열이나 JSON으로 직렬화(serialized)될 때의 포맷 양쪽 모두에 영향을 미칩니다.

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

타임스탬프로 사용할 컬럼의 이름을 커스터마이즈하고 싶을 때, 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 직접 정의하면 됩니다.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 값이 변경되지 않길 원하는 작업을 수행하려면, `withoutTimestamps` 메서드에 클로저를 전달해서 모델 작업을 처리할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 커넥션

기본적으로 모든 Eloquent 모델은 애플리케이션에서 설정된 기본 데이터베이스 커넥션을 사용합니다. 특정 모델만 별도의 커넥션으로 분리하고 싶다면, 모델에 `$connection` 프로퍼티를 지정해주면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 사용할 데이터베이스 커넥션
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

새로 인스턴스화된 모델 객체는 기본적으로 속성(attribute) 값이 비어 있습니다. 몇몇 속성에 기본값을 지정하고 싶을 때는 모델에 `$attributes` 프로퍼티를 선언하면 됩니다. 이 값들은 데이터베이스에서 읽어온 것과 동일한, 원시 "저장 가능한(storable)" 형식이어야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델의 기본 속성값
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

라라벨은 다양한 상황에서 Eloquent의 동작과 "엄격성(strictness)"을 설정할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 방지할지 여부를 지정하는 불리언 인수를 받을 수 있습니다. 예를 들어 프로덕션 환경에서는 지연 로딩이 우연히라도 발생하더라도 정상적으로 동작하도록 허용하고, 개발 환경에서만 엄격하게 지연 로딩을 금지할 수도 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 일반적입니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, `preventSilentlyDiscardingAttributes` 메서드를 사용하면, 모델의 `fillable` 배열에 정의되어 있지 않은 속성을 설정하려고 할 때 예외를 던지게 할 수 있습니다. 이 설정을 통해, 개발 중에 의도하지 않은 속성 값 할당으로 정확하지 않은 동작이나 에러가 일어나는 것을 방지할 수 있습니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries) 역할을 하며, 해당 모델에 연결된 테이블을 유연하게 쿼리할 수 있습니다. 가장 기본적으로는 모델의 `all` 메서드를 사용해 모든 레코드를 조회할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

Eloquent의 `all` 메서드는 테이블에 있는 모든 레코드를 조회합니다. 하지만 각 Eloquent 모델은 기본적으로 [쿼리 빌더](/docs/12.x/queries)이므로, 쿼리에 조건을 추가한 후 `get` 메서드를 호출해서 원하는 결과만 가져올 수도 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델 자체가 쿼리 빌더 역할을 하기 때문에, 라라벨의 [쿼리 빌더](/docs/12.x/queries)에서 제공하는 모든 메서드를 자유롭게 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 이 메서드들을 활용해 보세요.

<a name="refreshing-models"></a>
#### 모델 새로 고침

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh` 및 `refresh` 메서드를 이용해 모델을 다시 데이터베이스에서 새로 불러올 수 있습니다. `fresh` 메서드는 데이터베이스에서 새로운 상태의 모델을 다시 조회하며, 기존 인스턴스에는 영향을 주지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 같은 인스턴스를 데이터베이스의 최신 값으로 다시 채웁니다(재하이드레이션). 또한 이미 로드된 모든 연관관계도 함께 새로 고쳐집니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 살펴본 것처럼, Eloquent의 `all` 이나 `get` 메서드는 여러 개의 레코드를 한 번에 조회합니다. 이때 PHP의 일반 배열이 반환되는 것이 아니라, `Illuminate\Database\Eloquent\Collection` 인스턴스가 반환됩니다.

Eloquent의 `Collection` 클래스는 라라벨의 기본 `Illuminate\Support\Collection` 클래스를 확장하며, 다양한 [유용한 메서드](/docs/12.x/collections#available-methods)를 제공하여 데이터 컬렉션을 손쉽게 다룰 수 있습니다. 예를 들어, 클로저 결과를 활용해 컬렉션에서 특정 모델을 제거하려면 `reject` 메서드를 사용할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

라라벨의 기본 컬렉션 클래스에서 제공하는 메서드 외에도, Eloquent 컬렉션 전용으로 [몇 가지 추가 메서드](/docs/12.x/eloquent-collections#available-methods)도 있습니다.

라라벨의 모든 컬렉션은 PHP의 반복(iterable) 인터페이스를 구현하고 있으므로, 배열처럼 컬렉션을 자유롭게 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과를 청킹해서 가져오기

`all`이나 `get` 메서드를 통해 수만 건의 Eloquent 레코드를 한 번에 불러오면 애플리케이션이 메모리를 모두 소진할 수 있습니다. 이런 경우 `chunk` 메서드를 사용하면 대량의 모델을 보다 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 지정한 크기만큼 모델을 잘라서(청킹하여) 가져오고, 각각의 청크를 클로저에 전달해 처리합니다. 클로저에는 매번 현재 청크만 전달되므로, 매우 많은 양의 모델을 처리할 때 메모리 사용량을 대폭 줄일 수 있습니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인자는 한 번에 가져올 레코드 개수를 의미합니다. 두 번째 인자인 클로저는 데이터베이스에서 각 청크를 가져올 때마다 실행됩니다. 이때마다 데이터베이스에 쿼리가 실행되어, 새로운 청크가 전달됩니다.

반복문을 돌면서 동시에 필터링 기준이 되는 컬럼을 업데이트해야 한다면, `chunkById` 메서드를 사용하는 것이 좋습니다. 만약 일반 `chunk` 메서드를 사용하면 예상치 못한 결과가 발생할 수 있습니다. 내부적으로 `chunkById` 메서드는 이전 청크의 마지막 모델의 `id`보다 큰 값만 이어서 반환합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 자체적으로 특정 "where" 조건을 쿼리에 추가하므로, 직접 추가하는 조건들은 일반적으로 클로저로 [논리 그룹화](/docs/12.x/queries#logical-grouping)하는 것이 좋습니다.

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
### Lazy 컬렉션으로 청킹하기

`lazy` 메서드는 내부적으로 [chunk 메서드](#chunking-results)와 매우 비슷하게 동작하여, 쿼리를 청크 단위로 실행합니다. 그러나 `lazy` 메서드는 각 청크를 바로 콜백에 전달하는 것이 아니라, 평탄화(Flatten)된 [LazyCollection](/docs/12.x/collections#lazy-collections) 형태로 결과를 반환하여, 결과 전체를 하나의 스트림처럼 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 결과를 반복하면서 동시에 기준 컬럼도 업데이트해야 하는 경우, `lazyById` 메서드를 활용하면 됩니다. 이때도 내부적으로 이전 청크 마지막 모델의 `id`보다 큰 모델을 계속해서 가져옵니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id` 내림차순으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서(Cursors)

`lazy` 메서드처럼, `cursor` 메서드 역시 수만 건의 Eloquent 모델 레코드를 반복 처리할 때 앱의 메모리 사용량을 획기적으로 줄일 수 있습니다.

`cursor` 메서드는 단 하나의 데이터베이스 쿼리만 실행하고, 실제로 모델을 순회할 때마다 개별 Eloquent 모델을 모델 인스턴스로 동적으로 생성해줍니다. 따라서 반복 처리 중 언제나 한 번에 한 개의 Eloquent 모델만 메모리에 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 동시에 한 번에 오직 하나의 모델만 메모리에 존재하므로, 연관관계(eager loading)를 미리 가져올 수 없습니다. 연관관계까지 함께 메모리에 가져와야 한다면 [lazy 메서드](#chunking-using-lazy-collections) 사용을 고려하세요.

`cursor` 메서드는 내부적으로 PHP의 [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 이용해 이 기능을 구현합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)은 일반 라라벨 컬렉션과 동일한 많은 메서드를 사용하면서도, 한 번에 하나의 모델만 메모리에 올려 놓을 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, 결국에는 메모리가 부족해질 수 있습니다. 이는 [PHP의 PDO 드라이버가 내부적으로 모든 원시 쿼리 결과를 버퍼에 캐시하기 때문입니다](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). 정말 방대한 양의 Eloquent 레코드를 다뤄야 한다면, [lazy 메서드](#chunking-using-lazy-collections) 사용을 우선 고려해 주세요.

<a name="advanced-subqueries"></a>

### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 셀렉트

Eloquent는 고급 서브쿼리 기능을 제공하며, 이를 통해 하나의 쿼리로 연관된 테이블에서 정보를 가져올 수 있습니다. 예를 들어, `destinations`(도착지) 테이블과 해당 도착지로 가는 `flights`(항공편) 테이블이 있다고 가정해봅시다. `flights` 테이블에는 항공편이 도착지에 도착한 시점을 나타내는 `arrived_at` 컬럼이 있습니다.

쿼리 빌더의 `select` 및 `addSelect` 메서드에서 제공하는 서브쿼리 기능을 활용하면, 다음과 같이 하나의 쿼리로 모든 `destinations`와 각각의 도착지에 가장 최근 도착한 항공편의 이름을 함께 조회할 수 있습니다.

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

또한 쿼리 빌더의 `orderBy` 함수 역시 서브쿼리를 지원합니다. 앞서 예시로 든 항공편 데이터를 활용해, 각 도착지에 마지막으로 도착한 항공편의 시간 순으로 모든 도착지를 정렬할 수 있습니다. 이 역시 하나의 데이터베이스 쿼리로 실행됩니다.

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 또는 집계값 조회

주어진 쿼리 조건과 일치하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, 또는 `firstWhere` 메서드를 사용하여 단일 레코드를 조회할 수 있습니다. 이들 메서드는 모델 컬렉션이 아니라 단일 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본키로 모델 조회...
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 조건에 맞는 첫 번째 모델을 조회하는 또 다른 방법...
$flight = Flight::firstWhere('active', 1);
```

경우에 따라, 조회 결과가 없을 때 추가 작업을 하고 싶을 수 있습니다. `findOr`와 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과가 없을 경우 전달된 클로저를 실행합니다. 클로저가 반환한 값이 해당 메서드의 결과로 사용됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 조회 실패(찾을 수 없음) 예외

조회 결과가 없을 때 예외를 발생시키고자 할 때가 있습니다. 이는 라우트나 컨트롤러에서 특히 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리의 첫 결과를 조회하며, 결과가 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException` 예외를 잡아내지 않으면, 라라벨이 클라이언트에게 자동으로 404 HTTP 응답을 반환합니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값의 페어를 사용하여 데이터베이스 레코드를 찾으려고 시도합니다. 만약 해당 모델을 데이터베이스에서 찾지 못하면, 첫 번째 배열 인자와(필수) 선택적 두 번째 배열 인자를 병합한 속성값으로 새로운 레코드가 삽입됩니다.

`firstOrNew` 메서드는 `firstOrCreate`와 유사하지만, 모델을 찾지 못했을 때 새로운 모델 인스턴스를 반환합니다. 단, `firstOrNew`가 반환한 모델 인스턴스는 아직 데이터베이스에 저장되지 않았으므로, `save` 메서드를 호출하여 수동으로 저장해야 합니다.

```php
use App\Models\Flight;

// 이름으로 항공편 조회, 없으면 새로 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 항공편 조회, 없으면 name/delayed/arrival_time 속성으로 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 항공편 조회, 없으면 새 Flight 인스턴스 반환...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 항공편 조회, 없으면 해당 속성값으로 새 인스턴스 생성...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델을 다루면서, 라라벨 [쿼리 빌더](/docs/12.x/queries)가 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/12.x/queries#aggregates)도 사용할 수 있습니다. 이러한 메서드는 Eloquent 모델 인스턴스가 아닌 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

물론 Eloquent를 사용할 때, 단순히 모델을 조회하는 것뿐 아니라, 새 레코드를 삽입해야 할 때도 있습니다. Eloquent는 이를 매우 쉽게 할 수 있게 해줍니다. 데이터베이스에 새로운 레코드를 삽입하려면, 새로운 모델 인스턴스를 생성하고 속성을 할당한 뒤, 모델 인스턴스에서 `save` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 항공편을 데이터베이스에 저장합니다.
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

위 예제에서, 들어온 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당하고 있습니다. `save` 메서드를 호출하면 레코드가 데이터베이스에 삽입됩니다. `save`가 호출될 때, 모델의 `created_at` 및 `updated_at` 타임스탬프가 자동으로 설정되므로 직접 설정해줄 필요가 없습니다.

또 다른 방법으로, `create` 메서드를 사용하면 한 줄의 PHP 코드로 모델을 "저장"할 수 있습니다. `create` 메서드는 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에는, 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점(mass assignment vulnerability)으로부터 보호되므로, 이 속성 지정이 필요합니다. 대량 할당에 대한 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

이미 데이터베이스에 존재하는 모델을 수정할 때도 `save` 메서드를 사용할 수 있습니다. 모델을 찾아서 수정할 속성을 할당한 뒤, 다시 `save` 메서드를 호출하면 됩니다. 이때도 `updated_at` 타임스탬프는 자동으로 갱신되므로 직접 설정할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

경우에 따라, 기존 모델을 수정하거나 일치하는 모델이 없을 때 새로 생성하고 싶을 수 있습니다. `firstOrCreate`와 비슷하게, `updateOrCreate` 메서드는 모델을 저장(persist)하므로, 별도의 `save` 호출이 필요 없습니다.

아래 예제에서, 만약 `departure`가 `Oakland`이고 `destination`이 `San Diego`인 항공편이 존재한다면, 해당 항공편의 `price`와 `discounted` 컬럼이 업데이트됩니다. 만약 일치하는 항공편이 없다면, 첫 번째와 두 번째 인자 배열을 병합한 속성값으로 새 항공편이 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 다수 모델 일괄 업데이트

쿼리 조건에 일치하는 여러 모델을 한 번에 업데이트할 수도 있습니다. 아래 예제에서는, `active`가 1이고 `destination`이 `San Diego`인 모든 항공편에 대해 `delayed` 값을 1로 설정합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼과 값을 배열로 입력받으며, 처리된(영향받은) 행의 개수를 반환합니다.

> [!WARNING]
> Eloquent를 통한 대량 업데이트(mass update)에서는 해당 모델에 대해 `saving`, `saved`, `updating`, `updated`와 같은 모델 이벤트가 발생하지 않습니다. 이는 대량 업데이트에서는 실제 모델 인스턴스가 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 사항 확인

Eloquent는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공하여, 모델의 내부 상태와 속성이 어떻게 변경되었는지 쉽게 점검할 수 있습니다.

`isDirty` 메서드는 모델이 조회된 이후 속성값이 변경되었는지를 확인합니다. 속성 이름(또는 속성 이름 배열)을 인수로 전달하면, 해당 속성(들)에 변경이 있었는지 판단할 수 있습니다. `isClean` 메서드는 조회 후 해당 속성이 변경되지 않았는지 확인합니다. 이 메서드 역시 인자로 속성명을 받을 수 있습니다.

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

`wasChanged` 메서드는 현재 요청(사이클) 안에서 모델을 마지막으로 저장(save)할 때 실제로 변경된 속성이 있는지를 확인합니다. 특정 속성명 또는 속성명 배열을 전달하여 해당 속성의 변경 여부만 확인할 수 있습니다.

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

`getOriginal` 메서드는 모델이 조회된 이후로 실제 속성값이 변했다 하더라도, 원본 속성값(전체 또는 단일 속성)을 배열 형태로 반환합니다. 속성명을 인수로 전달하면 해당 속성의 원래 값을 확인할 수 있습니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 전체의 배열 반환...
```

`getChanges` 메서드는 모델이 마지막으로 저장(save)될 때 변경된 속성의 배열을 반환하고, `getPrevious` 메서드는 마지막 저장 이전의 원본 속성값 배열을 반환합니다.

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

`create` 메서드는 한 줄의 PHP 코드로 새 모델을 "저장"할 수 있게 해줍니다. 메서드는 생성된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에, 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점에 대비해 보호되고 있기 때문입니다.

대량 할당 취약점(mass assignment vulnerability)이란 예상치 못한 HTTP 요청 필드가 데이터베이스의 컬럼 값을 변경시키는 경우를 말합니다. 예를 들어, 악의적인 사용자가 HTTP 요청에 `is_admin` 파라미터를 넣고 이를 모델의 `create` 메서드에 그대로 전달하면, 사용자가 관리자로 권한 상승을 할 수도 있습니다.

따라서, 어떤 속성을 대량 할당 가능하도록 허용할지 미리 지정해야 합니다. 이를 위해 `$fillable` 속성을 모델에 선언할 수 있습니다. 아래는 `Flight` 모델에서 `name` 속성을 대량 할당 가능하게 만든 예입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용된 속성 목록입니다.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

대량 할당 허용 속성을 지정했다면, 즉시 `create` 메서드를 사용해 새 레코드를 데이터베이스에 삽입할 수 있습니다. `create` 메서드는 생성된 모델 인스턴스를 반환합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스를 가지고 있다면, `fill` 메서드로 속성값을 배열로 넣어 대량 할당할 수도 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 대량 할당할 경우, 각 컬럼의 대량 할당 가능한 키를 모델의 `$fillable` 배열에 반드시 지정해야 합니다. 보안상의 이유로, 라라벨은 `guarded` 속성을 사용할 때 중첩된 JSON 속성의 대량 할당을 지원하지 않습니다.

```php
/**
 * 대량 할당이 허용된 속성 목록입니다.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 대량 할당 허용

모델의 모든 속성을 대량 할당 가능하게 하고 싶다면, `$guarded` 속성을 빈 배열로 선언할 수 있습니다. 다만, 모델의 보호를 해제하면 Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열을 항상 신중히 수작업으로 작성해야 합니다.

```php
/**
 * 대량 할당 불가 속성 목록입니다.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 포함되지 않은 속성들은 대량 할당 시 조용히 무시되어 적용되지 않습니다. 운영 환경에서는 이러한 동작이 보통은 기대한 대로지만, 개발 중에는 변경이 적용되지 않아 혼란스러울 수 있습니다.

원한다면, 대량 할당 가능한 속성에 없는 속성을 `fill`하려고 할 때 라라벨이 예외를 발생시키도록 할 수 있습니다. 이를 위해 `preventSilentlyDiscardingAttributes` 메서드를 호출하면 됩니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upserts(없으면 삽입, 있으면 업데이트)

Eloquent의 `upsert` 메서드는 한 번의 원자적(atomic) 연산으로 레코드를 업데이트하거나 삽입할 수 있게 해줍니다. 첫 번째 인자는 삽입 또는 업데이트할 값의 배열이고, 두 번째 인자는 테이블에서 레코드를 고유하게 식별하는 컬럼들입니다. 세 번째 인자는 이미 있는 레코드의 어떤 컬럼 값을 업데이트할지 명시하는 배열입니다. `upsert` 메서드는 타임스탬프가 활성화되어 있다면 `created_at`과 `updated_at`을 자동으로 설정합니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인자로 전달한 컬럼들에 "primary" 또는 "unique" 인덱스가 반드시 있어야 합니다. 또한 MariaDB와 MySQL 데이터베이스 드라이버는 이 인수를 무시하고, 자동으로 테이블의 "primary"와 "unique" 인덱스만 사용해 기존 레코드를 판별합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 기존 모델 삭제

위 예제에서는 모델을 먼저 조회한 다음 `delete` 메서드를 호출합니다. 하지만 모델의 기본키를 이미 알고 있다면, 굳이 모델을 직접 조회하지 않고도 `destroy` 메서드로 삭제할 수 있습니다. 이 메서드는 단일 기본키뿐만 아니라, 복수 개의 기본키, 기본키 배열, 또는 [컬렉션](/docs/12.x/collections) 형태도 지원합니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제](#soft-deleting) 모델을 사용할 경우, `forceDestroy` 메서드로 모델을 영구적으로 삭제할 수도 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 조회해서 `delete` 메서드를 호출하므로, 각 모델에 대해 `deleting`, `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 이용한 모델 삭제

특정 조건에 맞는 여러 모델을 일괄적으로 삭제할 수도 있습니다. 아래 예에서는, 비활성화(활성화되지 않음)된 모든 항공편을 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제 시에는 해당 모델에 대한 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 모델을 삭제하려면, 조건 없이 쿼리를 실행하면 됩니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent를 통해 대량 삭제(mass delete)를 실행할 때는, 해당 모델의 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 이는 삭제 명령이 실제로 모델을 조회하지 않고 곧바로 실행되기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제(Soft Deleting)

Eloquent는 레코드를 실제로 데이터베이스에서 제거하는 대신, "소프트 삭제"할 수도 있습니다. 소프트 삭제가 적용된 모델은 데이터베이스에서 실제로 삭제되지 않고, 삭제된 날짜와 시간을 나타내는 `deleted_at` 속성만 설정됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하면 됩니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` / `Carbon` 인스턴스로 변환해줍니다.

또한 데이터베이스 테이블에 `deleted_at` 컬럼도 추가해야 합니다. 라라벨 [스키마 빌더](/docs/12.x/migrations)는 이 컬럼을 쉽게 생성해주는 헬퍼 메서드를 제공합니다.

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

이제, 모델의 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 날짜와 시간으로 설정됩니다. 하지만, 데이터베이스의 실제 레코드는 테이블에 남게 됩니다. 소프트 삭제가 적용된 모델을 조회할 때는, 기본적으로 소프트 삭제된 레코드가 자동으로 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 확인하려면, `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원

때로는 소프트 삭제된 모델을 "취소(복원)"하고 싶을 수 있습니다. 소프트 삭제된 모델 인스턴스에서 `restore` 메서드를 호출하면, 해당 모델의 `deleted_at` 컬럼이 `null`로 설정되어 복원됩니다.

```php
$flight->restore();
```

복수의 모델을 복원할 때 역시 쿼리에서 `restore` 메서드를 사용할 수 있습니다. 이 또한 다른 대량 작업과 마찬가지로, 복원된 모델에 대한 이벤트는 발생하지 않습니다.

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

경우에 따라 모델을 데이터베이스에서 완전히 제거해야 할 때가 있습니다. 이럴 때는 `forceDelete` 메서드를 사용하여 이미 소프트 삭제된 모델을 데이터베이스에서 영구적으로 삭제할 수 있습니다.

```php
$flight->forceDelete();
```

또한, Eloquent 연관관계 쿼리를 작성할 때도 `forceDelete` 메서드를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 쿼리하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제된 모델 포함하기

앞서 설명한 것처럼, 소프트 삭제된 모델은 기본적으로 쿼리 결과에서 자동으로 제외됩니다. 그러나 쿼리에서 소프트 삭제된 모델도 함께 조회하고 싶다면 쿼리에 `withTrashed` 메서드를 호출하면 됩니다.

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

`onlyTrashed` 메서드는 **오직** 소프트 삭제된 모델만 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 가지치기(Pruning Models)

주기적으로 더 이상 필요하지 않은 모델을 삭제해야 할 수도 있습니다. 이를 위해, 주기적으로 정리하고자 하는 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가할 수 있습니다. 트레이트를 모델에 추가한 후, 더 이상 필요하지 않은 모델들을 대상으로 하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현해야 합니다.

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
     * 가지치기할 모델의 쿼리를 반환합니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

모델을 `Prunable`로 지정했다면, 모델에 `pruning` 메서드를 추가로 정의할 수 있습니다. 이 메서드는 모델이 삭제되기 전에 호출됩니다. 이 기능은 예를 들어, 모델이 데이터베이스에서 영구 삭제되기 전에 저장된 파일 등 부가적인 리소스들을 미리 정리하고자 할 때 유용하게 사용할 수 있습니다.

```php
/**
 * 가지치기를 준비합니다.
 */
protected function pruning(): void
{
    // ...
}
```

`prunable` 모델을 설정한 이후에는, 애플리케이션의 `routes/console.php` 파일에 `model:prune` Artisan 명령어를 스케줄링해야 합니다. 이 명령어가 실행될 적절한 간격을 자유롭게 선택할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

내부적으로 `model:prune` 명령어는 애플리케이션의 `app/Models` 디렉토리 내에서 "Prunable" 모델을 자동으로 탐색합니다. 만약 모델이 다른 위치에 있다면 `--model` 옵션을 사용하여 모델 클래스명을 직접 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

모든 모델을 가지치기하는 과정에서 특정 모델은 제외하고 싶다면 `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`prunable` 쿼리가 제대로 동작하는지 테스트하고 싶다면 `model:prune` 명령어에 `--pretend` 옵션을 추가하여 실행하면 됩니다. 이 옵션을 사용하면 명령어가 실제로 데이터를 삭제하지 않고, 삭제될 레코드가 몇 개인지 보고만 해줍니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델도, 해당 가지치기 쿼리에 매치된다면 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기(Mass Pruning)

모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 지정하면, 대량 삭제 쿼리를 이용해 모델이 데이터베이스에서 삭제됩니다. 이 경우 `pruning` 메서드가 호출되지 않으며, `deleting` 및 `deleted` 모델 이벤트도 발생하지 않습니다. 이는 실제로 삭제 전에 개별 모델 인스턴스를 조회하지 않기 때문이며, 결과적으로 가지치기 처리 속도를 크게 향상시킵니다.

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
     * 가지치기할 모델의 쿼리를 반환합니다.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제하기

기존 모델 인스턴스를 저장하지 않은 상태로 복제하려면 `replicate` 메서드를 사용할 수 있습니다. 이 기능은 여러 속성 값이 유사한 모델 인스턴스를 손쉽게 생성해야 할 때 유용합니다.

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

복제 과정에서 일부 속성을 복제에서 제외하고 싶다면 `replicate` 메서드에 배열로 속성명을 지정할 수 있습니다.

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
### 전역 스코프(Global Scopes)

전역 스코프를 사용하면 특정 모델에 대한 모든 쿼리에 제한 조건을 항상 자동으로 추가할 수 있습니다. 라라벨의 [소프트 삭제](#soft-deleting) 기능 역시 전역 스코프를 활용하여 "삭제되지 않은" 모델만 조회되도록 처리하고 있습니다. 직접 전역 스코프를 작성하면, 지정된 모델 쿼리에 원하는 제한 조건이 항상 적용되도록 간편하게 만들 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

새로운 전역 스코프를 생성하려면 `make:scope` Artisan 명령어를 사용합니다. 이 명령어로 생성된 스코프 클래스는 애플리케이션의 `app/Models/Scopes` 디렉터리에 위치합니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성하기

전역 스코프를 작성하는 방법은 간단합니다. 우선, `make:scope` 명령어로 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 생성합니다. 이 `Scope` 인터페이스는 `apply`라는 메서드 구현을 요구합니다. `apply` 메서드 내에서 필요에 따라 `where` 조건이나 기타 쿼리 절을 추가하면 됩니다.

```php
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
> 전역 스코프가 쿼리의 select 절에 컬럼을 추가하는 경우, 기존 select 절이 덮어써지는 것을 방지하기 위해 `select` 대신 `addSelect` 메서드를 사용해야 합니다.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용하기

전역 스코프를 모델에 할당하려면 모델에 `ScopedBy` 애트리뷰트를 부여하면 됩니다.

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

또는, 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope` 메서드로 전역 스코프를 직접 등록할 수도 있습니다. 이 메서드는 스코프의 인스턴스를 인자로 받습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예시처럼 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 메서드 호출 시 다음과 같은 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 전역 스코프(Anonymous Global Scopes)

Eloquent는 또한, 클래스를 따로 만들지 않고 클로저(익명 함수)만으로 전역 스코프를 정의할 수 있도록 지원합니다. 이 기능은 별도의 클래스를 만들 만큼 복잡하지 않은 단순한 스코프에 특히 유용합니다. 클로저로 전역 스코프를 정의할 때는, `addGlobalScope` 메서드의 첫 번째 인자로 원하는 스코프 이름(문자열)을 전달해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
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
#### 전역 스코프 제거하기

특정 쿼리에서 전역 스코프를 제거하고 싶다면 `withoutGlobalScope` 메서드를 사용할 수 있습니다. 이 메서드는 전역 스코프의 클래스명을 인자로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의한 전역 스코프의 경우, 등록 시 사용한 문자열 스코프 이름을 인자로 전달해야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 전역 스코프, 또는 모든 전역 스코프를 제거하려면 `withoutGlobalScopes` 메서드를 사용합니다.

```php
// 모든 전역 스코프 제거...
User::withoutGlobalScopes()->get();

// 일부 전역 스코프만 제거...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프(Local Scopes)

로컬 스코프를 사용하면 애플리케이션 전반에서 반복적으로 사용할 수 있는 쿼리 조건의 집합을 모델에 정의할 수 있습니다. 예를 들어, 자주 "인기 있는 사용자"만 조회하는 쿼리가 필요하다면 로컬 스코프로 구현할 수 있습니다. 스코프를 정의하려면 Eloquent 메서드에 `Scope` 애트리뷰트를 추가하면 됩니다.

스코프 메서드는 항상 동일한 쿼리 빌더 인스턴스, 또는 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 있는 사용자만 쿼리하는 스코프.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 쿼리하는 스코프.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 활용하기

스코프를 정의하면, 모델 쿼리 시 스코프 메서드를 호출해서 사용할 수 있습니다. 여러 스코프를 체이닝해서 연속으로 호출할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 Eloquent 모델 스코프를 `or` 쿼리 연산자로 결합하려면, [논리 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용할 필요가 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 이러한 방식이 번거로울 수 있으므로, 라라벨은 클로저 없이도 스코프를 유연하게 연결할 수 있는 "higher order" `orWhere` 메서드도 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프(Dynamic Scopes)

스코프가 파라미터를 받을 수 있도록 하고 싶을 때는, 스코프 메서드의 시그니처에 추가 인수를 정의하면 됩니다. 스코프 파라미터는 `$query` 파라미터 다음에 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 지정한 타입의 사용자만 쿼리하는 스코프.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

예상 인수를 스코프 메서드에 정의했다면, 해당 스코프를 호출할 때 인수도 같이 전달하면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 보류 속성(Pending Attributes)

스코프를 활용하여, 스코프에서 사용한 쿼리 제약 조건과 동일한 속성값을 가진 모델을 생성하고 싶을 때는, 쿼리 빌더에 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시 저장본(초안)만 쿼리하는 스코프.
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

`withAttributes` 메서드는 주어진 속성을 기반으로 `where` 조건을 추가하고, 또한 해당 속성값을 스코프를 통해 생성된 모델에도 자동으로 추가해줍니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드에 전달하는 속성들을 쿼리의 조건(`where`)으로 추가하지 않고 싶다면 `asConditions` 인자를 `false`로 설정하면 됩니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

두 모델이 "같은 모델"인지 확인해야 할 경우도 있습니다. `is`, `isNot` 메서드를 사용하면 두 모델의 기본 키, 테이블, 데이터베이스 연결이 일치하는지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`, `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/12.x/eloquent-relationships)에서도 사용할 수 있습니다. 이 메서드는 관련 모델을 조회하는 쿼리를 별도로 전송하지 않고도 비교가 가능하다는 점에서 특히 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트(Events)

> [!NOTE]
> Eloquent 이벤트를 클라이언트-사이드 애플리케이션으로 직접 브로드캐스팅하고 싶으신가요? 라라벨의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting) 문서를 참고하세요.

Eloquent 모델은 여러가지 이벤트를 발생시켜, 모델 생명주기에서 다음 순간마다 동작을 연결할 수 있습니다. 예를 들어: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등입니다.

`retrieved` 이벤트는 데이터베이스에서 기존 모델이 조회될 때 발생합니다. 새 모델이 처음 저장될 때는 `creating`, `created` 이벤트가 발생합니다. 기존 모델을 수정하고 `save` 메서드를 호출하면 `updating` / `updated` 이벤트가 발생합니다. 모델을 생성 또는 수정할 때마다 `saving` / `saved` 이벤트가 발생하는데, 이 때는 모델의 속성이 변경되지 않아도 이벤트가 발생합니다. 이름이 `-ing`로 끝나는 이벤트는 모델의 변경사항이 실제로 데이터베이스에 반영되기 **이전**에, `-ed`로 끝나는 이벤트는 반영된 **이후**에 디스패치 됩니다.

모델 이벤트를 수신하려면, 해당 Eloquent 모델에 `$dispatchesEvents` 프로퍼티를 정의하세요. 이 프로퍼티는 Eloquent 모델의 생명주기의 여러 지점과 직접 만든 [이벤트 클래스](/docs/12.x/events)를 매핑합니다. 모델 이벤트 클래스는 반드시 생성자를 통해 모델 인스턴스를 전달받아야 합니다.

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

Eloquent 이벤트를 정의하고 매핑한 뒤에는, [이벤트 리스너](/docs/12.x/events#defining-listeners)를 구현해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 사용해 대량 업데이트 또는 대량 삭제 쿼리를 실행하면, 해당 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 모델 이벤트가 **발생하지 않습니다**. 이는 대량 업데이트나 삭제 시 개별 모델 인스턴스를 실제로 조회하지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저로 이벤트 등록하기

별도의 커스텀 이벤트 클래스를 만들지 않고, 모델 이벤트가 발생할 때 실행될 클로저(익명 함수)를 등록할 수도 있습니다. 일반적으로 이 클로저는 모델의 `booted` 메서드에서 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드입니다.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면, [큐로 처리되는 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 등록할 수도 있습니다. 이렇게 하면 모델 이벤트 리스너가 애플리케이션의 [큐](/docs/12.x/queues)에서 백그라운드로 실행됩니다.

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>

### 옵저버(Observers)

<a name="defining-observers"></a>
#### 옵저버 정의하기

특정 모델에서 여러 이벤트를 감지하고 싶을 때, 각각의 리스너를 개별로 등록하는 대신 **옵저버(Observer)** 클래스를 사용해 모든 이벤트 리스너를 하나의 클래스에 묶어 관리할 수 있습니다. 옵저버 클래스의 각 메서드는 감지하고자 하는 Eloquent 이벤트의 이름을 따르며, 각 메서드는 영향을 받는 모델 인스턴스를 유일한 인수로 전달받습니다. 새로운 옵저버 클래스를 생성하려면 `make:observer` 아티즌 명령어를 사용하는 것이 가장 쉽습니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어를 실행하면 새로운 옵저버 클래스가 `app/Observers` 디렉터리에 생성됩니다. 만약 해당 디렉터리가 없다면 Artisan이 자동으로 만들어줍니다. 새로 생성된 옵저버의 기본 형태는 아래와 같습니다.

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

옵저버를 등록하려면, 해당 모델 클래스에 `ObservedBy` 어트리뷰트를 지정할 수 있습니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, 명시적으로 관찰 대상 모델의 `observe` 메서드를 호출해 옵저버를 등록할 수도 있습니다. 이 방법은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 사용할 수 있습니다.

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 감지할 수 있는 이벤트는 위 예제 외에도 `saving`, `retrieved` 등 추가적으로 더 있습니다. 각각의 이벤트에 대한 자세한 설명은 [이벤트](#events) 문서에서 확인할 수 있습니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 데이터베이스 트랜잭션 내부에서 생성되는 경우, 트랜잭션이 커밋된 이후에만 옵저버의 이벤트 핸들러가 실행되도록 제어할 수 있습니다. 이를 위해 옵저버 클래스에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 만약 트랜잭션이 진행 중이 아니라면 이벤트 핸들러가 즉시 실행됩니다.

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
### 이벤트 뮤트(Muting Events)

때때로, 특정 모델에서 발생하는 모든 이벤트를 잠시 "뮤트(mute, 무시)"해야 할 때가 있습니다. 이럴 땐 `withoutEvents` 메서드를 사용할 수 있습니다. 이 메서드는 클로저를 인수로 받아, 해당 클로저 안에서 실행되는 모든 코드는 모델 이벤트를 발생시키지 않게 됩니다. 또한, 클로저가 반환하는 값은 그대로 `withoutEvents` 메서드의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 저장 시 이벤트 없이 처리하기

특정 모델 인스턴스를 저장하면서 어떠한 이벤트도 발생시키고 싶지 않을 때, `saveQuietly` 메서드를 사용할 수 있습니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이러한 방식으로 모델의 "update", "delete", "soft delete", "restore", "replicate" 작업도 모두 이벤트를 발생시키지 않고 조용히 수행할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```