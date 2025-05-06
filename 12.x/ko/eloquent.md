# Eloquent: 시작하기

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [Lazy 컬렉션으로 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 갱신](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [갱신](#updates)
    - [일괄 할당(Mass Assignment)](#mass-assignment)
    - [Upsert](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 정리(Prune)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 중지(muting)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와 즐겁게 상호작용할 수 있도록 Eloquent라는 객체-관계 매퍼(ORM)를 포함하고 있습니다. Eloquent를 사용하면 각 데이터베이스 테이블에 해당하는 "모델"이 존재하며, 이 모델을 통해 해당 테이블과 상호작용할 수 있습니다. Eloquent 모델을 사용하면 데이터베이스에서 레코드를 조회하는 것뿐 아니라 테이블에 레코드를 삽입, 수정, 삭제할 수도 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해 주세요. 데이터베이스 구성에 대한 자세한 내용은 [데이터베이스 구성 문서](/docs/{{version}}/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해봅시다. 모델은 보통 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 상속받습니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/{{version}}/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)도 함께 생성하려면 `--migration` 혹은 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책(policy), 컨트롤러, 폼 요청과 같은 다양한 클래스도 함께 생성할 수 있으며, 여러 옵션을 조합할 수 있습니다.

```shell
# 모델 및 FlightFactory 클래스 생성
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델 및 FlightSeeder 클래스 생성
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델 및 FlightController 클래스 생성
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, FlightController 리소스, 폼 요청 클래스 생성
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델 및 FlightPolicy 클래스 생성
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 동시 생성
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 통합 생성
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델(pivot) 생성
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

때로는 모델 코드만 보고 모든 속성과 관계를 파악하기가 어려울 수 있습니다. 이럴 때 `model:show` Artisan 명령어를 사용하면, 모델의 속성과 관계들을 편리하게 한눈에 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 기본 모델 클래스를 살펴보면서 Eloquent의 주요 관례를 알아보겠습니다.

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

위 예시에서 Eloquent가 `Flight` 모델에 해당하는 데이터베이스 테이블명을 별도로 지정하지 않았다는 점을 알 수 있습니다. 관례상, 클래스 이름을 "스네이크 케이스(snake_case)", 복수형으로 변환한 이름이 테이블명으로 사용됩니다. 즉, `Flight` 모델은 `flights` 테이블, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결됩니다.

만약 모델과 연결될 데이터베이스 테이블이 이러한 관례를 따르지 않는 경우, 모델의 `table` 속성을 정의하여 테이블명을 직접 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 이 모델이 연관된 테이블
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본키

Eloquent는 각 모델의 연관 테이블에 기본키 컬럼으로 `id`가 있다고 가정합니다. 만약 다른 컬럼을 기본키로 사용하려면 모델에 보호된 `$primaryKey` 속성을 정의할 수 있습니다.

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

또한, Eloquent는 기본키가 증가하는 정수형이라고 가정하여 자동으로 정수형으로 형변환합니다. 증가하지 않는(non-incrementing) 또는 숫자가 아닌 기본키를 사용할 경우, 모델의 공개 속성 `$incrementing`을 `false`로 지정해야 합니다.

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

기본키가 정수형이 아니면, 모델에 보호된 `$keyType` 속성을 `string`으로 명시해야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * 기본키의 데이터 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본키

Eloquent에서는 최소 하나의 고유한 "ID"가 기본키 역할을 해야 하며, "복합(composite)" 기본키는 지원되지 않습니다. 그러나 테이블의 고유한 기본키에 더해 여러 컬럼으로 이루어진 unique 인덱스는 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

기본키로 자동 증가하는 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자의 전역적으로 고유한 영숫자 식별자입니다.

모델에 자동 증가 정수 대신 UUID를 기본키로 사용하려면, 해당 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 물론, 모델에 [UUID 컬럼](/docs/{{version}}/migrations#column-method-uuid)이 있어야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => '유럽 여행']);

$article->id; // "8f8e8478-9035-4d23-b9a7-62f4d2612ce5"
```

기본적으로 `HasUuids` 트레이트는 모델에 ["정렬 가능한(ordered) UUID"](/docs/{{version}}/strings#method-str-ordered-uuid)를 생성합니다. 이 UUID는 색인된 데이터베이스 저장에 더 효율적입니다.

직접 UUID 생성 방식을 변경하려면, 모델에 `newUniqueId` 메소드를 정의할 수 있습니다. 또한, 어떤 컬럼에 UUID를 적용할지 `uniqueIds` 메소드로 지정할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델을 위한 새로운 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * 고유 식별자가 할당될 컬럼들 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26자로 더 짧으며, 정렬 가능하다는 장점이 있습니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 사용하세요. [ULID 컬럼](/docs/{{version}}/migrations#column-method-ulid)도 생성해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => '아시아 여행']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a name="timestamps"></a>
### 타임스탬프

Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼이 테이블에 존재한다고 가정합니다. 모델이 생성되거나 수정될 때 이 컬럼은 Eloquent가 자동으로 값을 관리합니다. 자동으로 관리하지 않으려면, 모델의 `$timestamps` 속성을 `false`로 지정하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 타임스탬프를 가질지 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

모델의 타임스탬프 포맷을 변경하려면 `$dateFormat` 속성을 설정하세요. 이 속성은 데이터베이스에 저장되는 날짜 형식 및 모델을 배열/JSON으로 직렬화할 때의 포맷을 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 날짜 컬럼 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프로 사용될 컬럼명을 변경하려면 각 상수를 정의하면 됩니다.

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 컬럼이 변경되지 않게 모델 작업을 하고자 한다면, `withoutTimestamps` 메소드로 클로저 안에서 조작할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션의 기본 데이터베이스 연결을 사용합니다. 모델마다 별도의 연결을 원한다면, 모델의 `$connection` 속성을 지정하면 됩니다.

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
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성값

새로 생성된 모델 인스턴스는 기본적으로 아무런 속성값도 갖고 있지 않습니다. 일부 속성에 기본값을 지정하려면 모델의 `$attributes` 속성에 키와 값을 지정하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 기본 속성값
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

Laravel은 다양한 상황에서 Eloquent의 동작 및 "엄격성"을 구성할 수 있는 여러 방법을 제공합니다.

먼저, `preventLazyLoading` 메소드는 lazy loading(지연 로딩)을 막을지 결정하는 불리언 인자를 받습니다. 보통 개발 환경에서만 lazy loading을 비활성화해, 프로덕션에서는 실수로 lazy loading이 발생해도 정상 동작하도록 설정합니다. 이 메소드는 일반적으로 `AppServiceProvider`의 `boot` 메소드에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩(초기화)
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한, `preventSilentlyDiscardingAttributes` 메소드를 통해, 모델의 `fillable` 배열에 없는 속성을 할당하려 할 때 예외를 던질 수 있습니다. 개발 중 예상치 못한 속성이 무시되는 일을 방지할 수 있습니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [연관된 데이터베이스 테이블](/docs/{{version}}/migrations#generating-migrations)를 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 되었습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/{{version}}/queries)처럼 동작하여 데이터베이스 테이블을 유연하게 쿼리할 수 있습니다. 모델의 `all` 메소드를 사용하면 해당 테이블의 모든 레코드를 조회할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성

Eloquent의 `all` 메소드는 테이블의 모든 결과를 반환합니다. 그러나 각 모델이 [쿼리 빌더](/docs/{{version}}/queries) 역할도 하므로, 다양한 조건을 추가하고 `get` 메소드로 결과를 조회할 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->take(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이기도 하므로, [쿼리 빌더](/docs/{{version}}/queries)가 제공하는 모든 메소드도 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 데이터베이스로부터 조회한 Eloquent 모델 인스턴스가 있다면, `fresh` 및 `refresh` 메소드로 모델을 "새로고침"할 수 있습니다. `fresh`는 데이터베이스에서 새로 모델을 다시 가져오며 기존 인스턴스는 변경되지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메소드는 기존 모델의 데이터를 데이터베이스에서 받아온 최신 데이터로 다시 채웁니다. 또한 로드된 관계들도 모두 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 본 것처럼, Eloquent의 `all` 및 `get` 메소드는 데이터베이스에서 여러 레코드를 조회합니다. 하지만 이 메소드들은 단순 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 상속받아 다양한 [유용한 메소드](/docs/{{version}}/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메소드를 통해 closure의 결과에 따라 모델을 컬렉션에서 걸러낼 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel 기본 컬렉션 클래스가 제공하는 메소드 이외에도, Eloquent 컬렉션에는 [Eloquent 모델 컬렉션 전용 메소드](/docs/{{version}}/eloquent-collections#available-methods)가 추가되어 있습니다.

모든 Laravel 컬렉션은 PHP의 반복(이터러블) 인터페이스를 구현하므로 배열처럼 foreach로 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

`all` 또는 `get` 메소드로 수만 건의 Eloquent 레코드를 한 번에 불러오면 애플리케이션의 메모리가 부족할 수 있습니다. 이 경우 `chunk` 메소드를 사용하여 대량의 레코드를 메모리 효율적으로 처리할 수 있습니다.

`chunk` 메소드는 일부 Eloquent 모델 집합만을 선택해 클로저에 전달해 처리하도록 하므로, 한 번에 전체 레코드를 메모리에 올리지 않아 효율적입니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메소드의 첫 번째 인자는 한번에 가져올 레코드의 개수이고, 두 번째 인자인 클로저는 각 청크마다 호출됩니다.

만약 청크 처리와 동시에 결과 레코드의 컬럼값을 갱신할 경우, `chunkById` 메소드를 사용하세요. 이 메소드는 내부적으로 각 chunk의 마지막 모델 기준으로 다음 chunk의 조회조건을 삼아, 정합성 있는 결과를 보장합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById` 및 `lazyById` 메소드에서는 쿼리에 자체적으로 "where" 조건을 추가하므로, 직접 조건을 묶고 싶다면 클로저로 래핑하세요.

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
### Lazy 컬렉션으로 청크 처리

`lazy` 메소드는 [chunk 메소드](#chunking-results)와 유사하게 동작하지만, 결과를 바로 콜백에 넘기지 않고 평탄화된 [LazyCollection](/docs/{{version}}/collections#lazy-collections)으로 반환합니다. 이를 통해 거대한 결과를 스트림 처리하듯 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

만약 결과 레코드를 갱신 상태로 필터링하며 순회한다면, `lazyById` 메소드를 사용하세요. 이는 내부적으로 이전 청크의 마지막 모델 id보다 큰 id를 갖는 레코드를 다음 청크로 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메소드로 id의 내림차순 조건도 사용할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy`와 유사하게, `cursor` 메소드를 사용하면 수만 건의 레코드를 순회할 때 애플리케이션의 메모리 사용량을 대폭 줄일 수 있습니다.

`cursor` 메소드는 단일 쿼리만 실행하지만, 개별 모델 인스턴스는 실제로 순회하기 전까지 생성되지 않습니다. 따라서 한 번에 하나의 모델 인스턴스만 메모리에 보유하므로 메모리가 대폭 절감됩니다.

> [!WARNING]
> `cursor` 메소드는 한 번에 하나의 Eloquent 모델만 메모리에 있기 때문에, 관계를 eager load할 수 없습니다. 관계를 미리 불러와야 한다면 [lazy 메소드](#chunking-using-lazy-collections)를 고려하세요.

내부적으로 `cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/{{version}}/collections#lazy-collections)은 일반 컬렉션의 다양한 메소드를 동일하게 이용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메소드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만, [PHP의 PDO 드라이버가 내부적으로 모든 원시 쿼리 결과를 버퍼에 캐시](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)하기 때문에 메모리 한계가 매우 큰 경우 [lazy 메소드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리를 지원하여 한 번의 쿼리로 관련 테이블의 정보를 함께 당길 수 있습니다. 예를 들어, `destinations` 테이블과 `flights` 테이블이 있고, 각 항공편에 `arrived_at` 컬럼이 있다고 가정합시다.

`select` 및 `addSelect`의 서브쿼리 기능을 사용해, 각 도착지별로 가장 최근에 도착한 항공편명을 같이 조회할 수 있습니다.

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

쿼리 빌더의 `orderBy` 함수로도 서브쿼리를 지원합니다. 항공편 예시에서 각 도착지의 마지막 항공편이 도착한 시각 기준으로 모든 도착지를 정렬할 수 있습니다.

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

주어진 쿼리에 일치하는 모든 레코드를 조회하는 것 외에, `find`, `first`, `firstWhere` 메소드로 단일 레코드만 조회할 수도 있습니다. 이들은 모델 컬렉션이 아닌 단일 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본키로 모델 조회
$flight = Flight::find(1);

// 조건에 일치하는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// firstWhere로 대체 가능
$flight = Flight::firstWhere('active', 1);
```

결과가 없는 경우 다른 동작을 하고 싶다면, `findOr`와 `firstOr` 메소드를 사용하여 인스턴스가 없으면 클로저를 실행하는 등 행동을 정의할 수 있습니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 미조회(Not Found) 예외

모델이 조회되지 않을 때 예외를 발생시키고 싶은 경우가 있습니다(특히 라우트/컨트롤러에서 유용). `findOrFail`, `firstOrFail` 메소드를 사용하면 결과가 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외가 발생합니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`을 잡지 않으면, 자동으로 404 HTTP 응답이 반환됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메소드는 주어진 컬럼/값쌍으로 레코드를 찾으려 시도하다가, 찾지 못하면 속성을 결합하여 레코드를 삽입합니다.

`firstOrNew` 메소드는 일치하는 레코드를 찾지 못하면 새 모델 인스턴스를 반환하지만, 데이터베이스에는 아직 저장하지 않습니다. 직접 `save` 호출이 필요합니다.

```php
use App\Models\Flight;

// name 컬럼으로 조회, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// name, delayed, arrival_time 지정
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// name으로 조회, 없으면 새 인스턴스
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// name, delayed, arrival_time 지정 후 인스턴스
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델로 조회할 때, Laravel [쿼리 빌더](/docs/{{version}}/queries)가 제공하는 `count`, `sum`, `max` 등의 [집계 메소드](/docs/{{version}}/queries#aggregates)를 사용해 결과를 스칼라 값으로 반환받을 수 있습니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 갱신

<a name="inserts"></a>
### 삽입

Eloquent로 모델을 조회하는 것뿐 아니라, 새 레코드를 데이터베이스에 삽입할 수도 있습니다. 새로운 모델 인스턴스를 생성하고 속성값을 할당한 후, `save` 메소드를 호출하면 레코드가 삽입됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * DB에 새 항공편 저장
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

이 예제에서는, HTTP 요청으로 전달된 name 필드를 `Flight` 모델의 name 속성에 할당했습니다. `save`를 호출하면, `created_at`, `updated_at` 타임스탬프도 자동으로 설정됩니다.

대체로 `create` 메소드로 하나의 PHP 문장으로 새 모델을 "저장"할 수도 있습니다. 이 메소드 역시 새로 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 사용 전 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나는 꼭 지정해야 합니다. 이것은 mass assignment 공격을 막기 위해 필요합니다. 자세한 내용은 [일괄 할당 문서](#mass-assignment)를 참고해 주세요.

<a name="updates"></a>
### 갱신

이미 DB에 존재하는 모델을 `save`로 갱신할 수도 있습니다. 갱신할 속성을 원하는대로 할당하고 `save`만 다시 호출하면 됩니다. `updated_at` 값도 자동 갱신됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

기존 모델 업데이트 또는 없으면 새로 생성하려면, `firstOrCreate`처럼 동작하는 `updateOrCreate` 메소드를 사용할 수 있습니다. 

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 일괄 업데이트(Mass Updates)

쿼리에 일치하는 모델을 한 번에 갱신할 수도 있습니다. 아래 예시는 모든 활성 `San Diego`행 항공편을 지연 처리합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메소드는 업데이트할 컬럼/값 쌍의 배열을 인자로 받고, 영향받은 행의 개수를 반환합니다.

> [!WARNING]
> Eloquent의 일괄 업데이트시엔 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. (모델 인스턴스가 실제로 조회되지 않기 때문입니다.)

<a name="examining-attribute-changes"></a>
#### 속성 변화 확인

Eloquent는 모델의 내부 상태 변화를 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메소드를 제공합니다.

`isDirty`는 속성이 처음 조회된 이후 변경되었는지 판별합니다. 속성명 또는 배열도 인자로 넘길 수 있습니다. `isClean`은 변경되지 않았는지 판별하며, 역시 특정 속성 지정이 가능합니다.

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

`wasChanged`는 모델이 마지막으로 저장되었을 때 속성이 실제로 변경됐는지 여부를 확인합니다. 역시 속성명을 넘길 수 있습니다.

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

`getOriginal` 메소드는 조회됐던 시점의 원래 속성값 배열을, 인자로 속성명을 넘기면 해당 속성의 원래 값만 반환합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원래 속성들 배열...
```

`getChanges`는 마지막 저장시점에 변경된 속성만 배열로 반환합니다.

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
### 일괄 할당(Mass Assignment)

`create` 메소드를 사용하면 하나의 PHP 문장으로 모델을 생성·저장할 수 있습니다. 

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, 사용 전 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나를 반드시 지정해야 합니다. 모든 Eloquent 모델은 일괄 할당 취약점을 기본적으로 차단합니다.

일괄 할당(Mass Assignment) 취약점은 사용자가 예상치 못한 HTTP 요청 필드를 전달해, DB 내 의도하지 않은 컬럼을 변경시키는 경우에 발생합니다. 예를 들어 악의적인 사용자가 `is_admin` 필드를 전달하면, 모델의 `create` 메소드로 인해 관리자 권한이 부여될 수 있습니다.

따라서, 모델에서 mass assignment가 가능한 속성을 `$fillable`로 명시해야 합니다. 예를 들어 Flight 모델의 name 속성을 mass assignment 가능하도록 하려면 다음과 같이 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 일괄 할당 가능한 속성
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

`fillable` 지정 후에는 `create`로 새 레코드 삽입이 가능합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 생성한 인스턴스에는 `fill` 메소드로 속성값을 채울 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### Mass Assignment와 JSON 컬럼

JSON 컬럼에 할당할 경우, 해당 컬럼의 키 역시 `$fillable` 배열에 명시해야 합니다. 보안을 위해, `guarded` 속성을 사용할 경우 중첩 JSON 속성 갱신을 지원하지 않습니다.

```php
/**
 * 일괄 할당 가능한 속성
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 일괄 할당 허용

모든 속성을 mass assignment 가능하게 하려면, `$guarded`를 빈 배열로 지정하면 됩니다. 하지만 이 경우에도, `fill`, `create`, `update`에 전달하는 배열을 항상 손수 구성해야 보안을 지킬 수 있습니다.

```php
/**
 * 일괄 할당이 불가능한 속성
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### Mass Assignment 예외

기본적으로 `$fillable`에 포함되지 않은 속성은 조용히 무시됩니다. 실운영에서는 예상된 동작이나, 개발 단계에서는 의도한 모델 변경이 적용되지 않아 혼란을 줄 수 있습니다.

이럴 때 `preventSilentlyDiscardingAttributes` 메소드로, 할당 불가 속성일 경우 예외를 던지도록 할 수 있습니다. 이 메소드는 AppServiceProvider의 `boot`에서 사용하면 좋습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩(초기화)
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### Upserts

Eloquent의 `upsert` 메소드는 한 번의 처리를 통해 레코드를 새로 넣거나, 이미 있을 경우 갱신할 수 있습니다. 첫 인자는 삽입/갱신할 값들, 두 번째 인자는 레코드 식별 컬럼목록, 세 번째 인자는 해당 레코드를 갱신할 컬럼입니다. 타임스탬프도 자동 관리됩니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 두 번째 인자의 컬럼이 테이블에 "primary" 또는 "unique" 인덱스로 정의되어야 하며, MariaDB/MySQL에선 두 번째 인자를 무시하고 테이블 전체의 primary/unique 인덱스를 자동 적용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면 인스턴스의 `delete` 메소드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 삭제

먼저 모델을 조회한 후 `delete`하는 대신, 기본키를 알고 있다면 `destroy` 메소드로 직접 삭제할 수 있습니다. 단일, 복수, 배열, 컬렉션 타입의 기본키를 모두 지원합니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)은 `forceDestroy` 메소드로 영구 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메소드는 모델을 하나씩 개별 로딩해 `delete` 이벤트 처리와 같은 작업을 정상적으로 수행합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

Eloquent 쿼리로 조건에 맞는 모든 모델을 삭제할 수도 있습니다. 예시에서는 비활성 항공편 전체를 삭제합니다. 일괄 삭제처럼 이벤트는 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

특정 조건 없이 전체 모델 삭제도 가능합니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent의 일괄 삭제문 실행 시, 해당 모델에 대한 `deleting`, `deleted` 이벤트는 발생하지 않습니다.

<a name="soft-deleting"></a>
### 소프트 삭제

모델을 실제로 데이터베이스에서 삭제하지 않고, `deleted_at` 컬럼에 삭제 일시만 기록하는 방식도 지원합니다. 이렇게 하면 쿼리 결과에서 해당 모델이 자동으로 제외됩니다. 이를 위해 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime`/`Carbon` 객체로 캐스팅합니다.

데이터베이스 테이블에 `deleted_at` 컬럼 추가가 필요합니다. Laravel [스키마 빌더](/docs/{{version}}/migrations)를 사용하세요.

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

이제 `delete`를 호출하면 실제로 DB에서 삭제하지 않고 `deleted_at`만 기록됩니다. 소프트 삭제 모델은 쿼리 결과에서 자동으로 제외됩니다.

모델이 소프트 삭제됐는지는 `trashed` 메소드로 확인할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

삭제된 모델을 다시 복원하려면, 인스턴스의 `restore`를 호출하면 됩니다. 이 때 `deleted_at` 값이 null로 처리됩니다.

```php
$flight->restore();
```

쿼리에서도 여러 모델을 한 번에 복원할 수 있습니다. 역시 이벤트는 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[관계 쿼리](/docs/{{version}}/eloquent-relationships)에도 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 영구 삭제

모델을 완전히 삭제하려면 `forceDelete` 메소드를 사용합니다.

```php
$flight->forceDelete();
```

관계 쿼리에도 동일하게 `forceDelete` 사용이 가능합니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함 조회

기본적으로 소프트 삭제 모델은 쿼리 결과에서 제외됩니다. 하지만, `withTrashed` 메소드로 포함시켜 조회할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에도 적용 가능합니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed` 메소드는 **소프트 삭제된 모델만** 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리(Pruning)

불필요해진 모델을 주기적으로 삭제하고 싶다면, 해당 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하세요. 그리고 `prunable` 메소드에서 더 이상 필요하지 않은 모델을 찾는 쿼리에 정의합니다.

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
     * 정리할 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable` 모델 지정시, 삭제 전 호출할 `pruning` 메소드를 정의할 수 있습니다. 파일 등 부가 자원 삭제에 활용 가능합니다.

```php
/**
 * 정리 전 준비 작업
 */
protected function pruning(): void
{
    // ...
}
```

설정 후, 애플리케이션의 `routes/console.php` 파일에서 `model:prune` 명령어를 스케줄링하세요.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

백그라운드에서는 `app/Models` 디렉터리의 "Prunable" 모델들을 자동으로 탐지합니다. 위치가 다를 경우 `--model` 옵션으로 명시하세요.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델을 제외하고 모두 정리하려면 `--except` 옵션을 사용하세요.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`prunable` 쿼리의 결과를 실제 삭제하지 않고 확인만 하고 싶다면, `--pretend` 옵션으로 시뮬레이션이 가능합니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델도 prunable 쿼리에 포함되면 permanent 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리

`Illuminate\Database\Eloquent\MassPrunable` 트레이트가 적용된 모델은 대량 삭제 쿼리로 처리되며, 이 경우 `pruning` 메소드 및 `deleting`, `deleted` 이벤트가 호출되지 않습니다. 즉, 모델을 실제로 조회하지 않아 훨씬 효율적입니다.

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
     * 정리할 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델의 속성을 복사해 미저장된 "복제" 인스턴스를 만들려면 `replicate` 메소드를 사용하세요. 비슷한 속성을 가진 인스턴스가 필요한 경우 편리합니다.

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

특정 속성의 복제를 제외하려면 `replicate` 메소드에 배열로 명시하면 됩니다.

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

글로벌 스코프를 사용하면 한 모델에 대한 모든 쿼리에 공통 제약 조건을 적용할 수 있습니다. Laravel의 [소프트 삭제](#soft-deleting)도 글로벌 스코프 기능을 활용합니다.

<a name="generating-scopes"></a>
#### 스코프 생성

새 글로벌 스코프를 생성하려면 `make:scope` Artisan 명령어를 사용하세요. 생성된 스코프는 `app/Models/Scopes`에 위치합니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현해야 하며, `apply` 메소드를 반드시 정의해야 합니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 스코프를 주어진 쿼리 빌더에 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 select에 컬럼을 추가할 땐, `select` 대신 반드시 `addSelect`를 사용하세요. 기존 select절이 덮어써지는 사고를 방지합니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

모델에 글로벌 스코프를 지정하려면, 모델에 `ScopedBy` 속성을 추가하면 됩니다.

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

또는 모델의 `booted` 메소드에서 `addGlobalScope`를 수동 호출할 수도 있습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

이 스코프를 적용하면 `User::all()` 호출 시 다음 SQL이 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(클로저) 글로벌 스코프

별도의 클래스를 만들 필요 없이, 간단한 글로벌 스코프는 클로저(익명함수)로 정의할 수 있습니다. 이땐 `addGlobalScope`의 첫 번째 인자로 임의의 스코프명을 넘기세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
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

특정 쿼리에서 글로벌 스코프를 해제하려면 `withoutGlobalScope`를 사용합니다. 클래스명을 넘기거나, 클로저 스코프의 경우 지정한 스코프명을 넘기세요.

```php
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 스코프를 제거하려면 `withoutGlobalScopes`를 사용합니다.

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 애플리케이션 내에서 재사용성 높은 쿼리 조건 묶음을 정의할 수 있게 해줍니다. 예를 들어 "인기 유저"만 자주 호출해야 할 때, 메소드에 `Scope` 속성을 붙이면 됩니다.

스코프는 항상 동일한 빌더 인스턴스 또는 void를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용

스코프 정의 후, 해당 메소드를 체이닝해 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 or 조건으로 논리 그룹화할 땐, 클로저로 감싸야 할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

좀 더 간단히, Laravel의 고차 `orWhere` 메소드로 스코프를 자연스럽게 체이닝할 수도 있습니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 파라미터를 전달하려면 `$query` 뒤에 추가 인자를 정의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 지정 타입의 유저만 조회
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

호출 시에는 인자를 넘기면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### Pending 속성

스코프를 사용해 쿼리 조건에 쓰인 속성값으로 모델을 생성할 때, `withAttributes` 메소드를 이용하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시글만 쿼리
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

`withAttributes`는 쿼리에 where 조건을 추가하고, 생성된 모델에도 같은 값을 부여합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

where 조건 추가 없이 속성만 부여하려면 두 번째 인자를 false로 지정하세요.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "같은"지(동일한 PK, 테이블, DB 연결) 판별할 때는 `is`, `isNot` 메소드로 빠르게 비교할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is`, `isNot`는 관계(`belongsTo`, `hasOne`, `morphTo`, `morphOne`) 쪽에서도 동일하게 사용할 수 있습니다. 쿼리를 실행하지 않고도 비교할 때 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 프론트엔드로 브로드캐스트하고 싶으신가요? Laravel의 [모델 이벤트 브로드캐스팅](/docs/{{version}}/broadcasting#model-broadcasting)를 참고하세요.

Eloquent 모델은 여러 시점마다 이벤트를 발생시켜, 다음과 같은 라이프사이클 후킹 지점을 제공합니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 모델이 DB에서 조회될 때
- `creating`, `created`: 새 모델 저장될 때(전/후)
- `updating`, `updated`: 기존 모델 수정/저장될 때(전/후)
- `saving`, `saved`: 생성/수정과 관계없이 save가 불릴 때(전/후)
- `-ing`: DB에 반영되기 "전", `-ed`: 반영된 "후" 호출

이벤트 수신을 시작하려면, 모델에 `$dispatchesEvents` 속성을 정의해 다양한 시점에 이벤트 클래스를 맵핑하세요. 각 이벤트 클래스는 생성자로 영향받은 모델 인스턴스를 전달받습니다.

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

이제 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)로 실제 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent로 일괄 update/delete 쿼리 실행 시, 각 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트는 발생하지 않습니다.

<a name="events-using-closures"></a>
### 클로저 사용

커스텀 이벤트 클래스 대신, 이벤트 발생 시 실행할 클로저를 등록할 수도 있습니다. 보통 모델의 `booted` 메소드에서 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 모델 이벤트 등록에 [큐어블 익명 이벤트 리스너](/docs/{{version}}/events#queuable-anonymous-event-listeners)를 활용, 백그라운드 큐로 이벤트를 처리할 수 있습니다.

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

한 모델의 여러 이벤트에 대해 리스너를 한 클래스로 모으고 싶다면 옵저버를 사용하세요. 옵저버 클래스의 메소드명은 Eloquent 이벤트명을 따릅니다. `make:observer` Artisan 명령어로 쉽게 생성할 수 있습니다.

```shell
php artisan make:observer UserObserver --model=User
```

생성된 옵저버는 `app/Observers`에 위치합니다. 폴더가 없으면 자동 생성됩니다. 초기 모습은 다음과 같습니다.

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    public function created(User $user): void
    {
        // ...
    }

    public function updated(User $user): void
    {
        // ...
    }

    public function deleted(User $user): void
    {
        // ...
    }

    public function restored(User $user): void
    {
        // ...
    }

    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면, 대상 모델에 `ObservedBy` 속성을 붙이면 됩니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는 `AppServiceProvider`의 `boot` 메소드 등에서 모델의 `observe`로 수동 등록할 수 있습니다.

```php
use App\Models\User;
use App\Observers\UserObserver;

public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 `saving`, `retrieved` 등 추가 이벤트도 수신 가능하며, 이는 [이벤트 문서](#events)에 자세히 설명돼 있습니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

트랜잭션 내에서 모델을 생성할 때, 옵저버가 트랜잭션 커밋 후에만 이벤트 핸들러를 실행하도록 하고 싶다면 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하세요. 트랜잭션이 없을 땐 즉시 실행됩니다.

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 중지(Muting)

때때로 모델에서 발생하는 모든 이벤트를 일시적으로 "음소거"할 필요가 있습니다. 이 때 `withoutEvents` 메소드를 사용하세요. 클로저 내부에서 실행되는 모든 이벤트가 발생하지 않으며, 클로저의 반환값이 그대로 반환됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델만 이벤트 없이 저장

특정 모델에 대해서만 이벤트 없이 저장하려면 `saveQuietly` 메소드 사용이 가능합니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

또한 "update", "delete", "soft delete", "restore", "replicate" 등도 `Quietly` 접미사를 붙여 이벤트 없이 처리할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
