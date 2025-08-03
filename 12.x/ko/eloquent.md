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
    - [청크 처리](#chunking-results)
    - [지연 컬렉션으로 청크 처리하기](#chunking-using-lazy-collections)
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
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 프루닝](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [전역 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [대기 속성](#pending-attributes)
- [모델 비교하기](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)

<a name="introduction"></a>
## 소개

Laravel에는 데이터베이스와의 상호작용을 즐겁게 만들어주는 객체 관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용하면, 각 데이터베이스 테이블에 해당하는 모델(Model)이 있으며 이 모델을 통해 테이블과 상호작용합니다. 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, Eloquent 모델을 사용하여 레코드를 삽입, 업데이트, 삭제할 수도 있습니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 구성 문서](/docs/12.x/database#configuration)를 참조하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기

시작하려면 Eloquent 모델을 생성해 봅시다. 모델은 일반적으로 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속받습니다. `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용하면 새 모델을 쉽게 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 같이 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책(policy), 컨트롤러, 폼 요청 클래스도 함께 생성할 수 있으며, 여러 옵션을 조합해 한 번에 여러 클래스를 생성할 수도 있습니다:

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

# 모델, FlightController 리소스 클래스, 그리고 폼 요청 클래스 생성...
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
#### 모델 검사하기

모델의 사용 가능한 모든 속성과 연관관계를 코드만 보고 파악하기 어려울 수 있습니다. 이런 경우 `model:show` Artisan 명령어를 사용해 모델이 가진 속성과 연관관계 목록을 편리하게 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치합니다. 기본적인 모델 클래스를 살펴보고 Eloquent가 따르는 주요 규칙을 설명합니다:

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

위 예제를 보면 `Flight` 모델이 어떤 데이터베이스 테이블에 대응하는지 명시하지 않은 것을 볼 수 있습니다. Eloquent는 기본적으로 클래스 이름의 '스네이크 케이스(snake_case)', 복수형 이름이 테이블 이름이라고 가정합니다. 따라서 `Flight` 모델은 `flights` 테이블과 연결되며, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결된다고 예상합니다.

만약 모델에 대응하는 데이터베이스 테이블 이름이 이 규칙과 다르다면, 모델 내에 `table` 속성을 정의하여 테이블 이름을 수동 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에 연결된 테이블 이름.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델과 연결된 데이터베이스 테이블에 `id`라는 이름의 기본 키가 있다고 가정합니다. 필요에 따라 `$primaryKey` 속성을 정의하여 다른 컬럼을 기본 키로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블에 연결된 기본 키 컬럼명.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한, 기본 키가 자동 증가하는 정수라고 가정하며, 이 경우 기본 키를 자동으로 정수형으로 변환합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본 키를 사용하려면, 모델에 공개 속성 `$incrementing`을 `false`로 설정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 모델의 ID가 자동 증가인가를 나타냄.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아닐 경우, `$keyType` 속성을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본 키 데이터 타입.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### 복합 기본 키("Composite" Primary Keys)

Eloquent 모델은 각각 고유하게 식별할 수 있는 "ID"를 반드시 하나 이상 가져야 하며, 복합 기본 키는 지원하지 않습니다. 그래도 데이터베이스 상에서 여러 컬럼으로 이루어진 고유 인덱스는 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

자동 증가하는 정수 대신 UUID(36자 영숫자, 범용 고유 식별자)를 기본 키로 사용할 수 있습니다.

UUID 키를 사용하려면, 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 물론 해당 모델에는 UUID와 대응하는 기본 키 컬럼이 있어야 합니다:

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

기본적으로 `HasUuids` 트레이트는 ["ordered" UUID](/docs/12.x/strings#method-str-ordered-uuid)를 생성하는데, 이 UUID는 데이터베이스 인덱스 저장에 효율적이고 사전식 정렬이 가능합니다.

특정 모델에서 UUID 생성 방식을 변경하려면 `newUniqueId` 메서드를 정의할 수 있으며, UUID가 적용될 컬럼명을 지정하려면 `uniqueIds` 메서드를 정의할 수 있습니다:

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
 * UUID가 할당될 컬럼명 배열 반환.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

필요하다면 ULID(26자 고유 식별자, 사전식 정렬 가능)를 UUID 대신 사용할 수 있습니다. ULID를 사용하려면 `HasUlids` 트레이트를 모델에 적용하고, 대응하는 ULID 컬럼이 있어야 합니다:

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

기본적으로 Eloquent는 모델에 연결된 데이터베이스 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 가정합니다. 모델 생성 혹은 업데이트 시 이 컬럼은 자동으로 갱신됩니다. 만약 자동 관리하지 않으려면, 모델에 `$timestamps` 속성을 `false`로 설정하세요:

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

타임스탬프 저장 형식을 지정하려면 `$dateFormat` 속성을 설정하세요. 이 속성은 데이터베이스 저장 시 형식과 배열/JSON 직렬화 시 형식을 결정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 타임스탬프 컬럼 저장 형식.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 바꾸려면 `CREATED_AT`과 `UPDATED_AT` 상수를 정의하세요:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델 작업 중 `updated_at` 타임스탬프 수정을 건너뛰려면 `withoutTimestamps` 메서드에 클로저를 넘겨서 작업할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에서 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 다른 연결을 사용하려면 `$connection` 속성을 지정하세요:

```php
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
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

기본적으로 새로 생성된 모델 인스턴스는 속성 값을 포함하지 않습니다. 모델의 일부 속성에 기본값을 지정하려면 `$attributes` 속성에 원시 저장 형식으로 배열을 정의하세요:

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

Laravel은 여러 상황에서 Eloquent 동작과 엄격성을 설정할 수 있는 방법을 제공합니다.

`preventLazyLoading` 메서드를 사용하면 지연 로딩(lazy loading)을 막을 수 있습니다. 예를 들어, 실수로 프로덕션에서 지연 로딩하는 관계가 있어도, 프로덕션에서는 비활성화하고 로컬 개발 환경에서는 활성화할 수 있습니다. 보통 이 메서드는 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

또한 `preventSilentlyDiscardingAttributes` 메서드를 호출하면 `fillable` 배열에 없는 속성을 채우려고 할 때 예외를 던지도록 할 수 있어, 로컬 개발 시 무심코 속성들이 무시되는 것을 방지할 수 있습니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [이에 대응하는 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)을 생성했다면, 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)로 작동하여 모델에 연결된 테이블을 유창하게 조회할 수 있습니다. 모델의 `all` 메서드는 테이블의 모든 레코드를 조회합니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 빌드하기

`all` 메서드는 모든 결과를 반환하지만, Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries)이기 때문에 추가 조건을 붙이고 `get` 메서드를 호출하여 결과를 조회할 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더에서 제공하는 모든 메서드](/docs/12.x/queries)를 활용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침하기

이미 데이터베이스에서 조회한 모델 인스턴스가 있다면, `fresh`와 `refresh` 메서드로 모델을 갱신할 수 있습니다. `fresh`는 새로운 모델 인스턴스를 데이터베이스에서 다시 조회하며, 기존 인스턴스에는 영향을 주지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 현재 모델에 데이터베이스의 최신 데이터를 재적용하며, 로드된 관계도 새로고침합니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

`all`, `get` 같은 메서드는 데이터베이스에서 여러 레코드를 조회하지만, 일반 PHP 배열이 아닌 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 컬렉션 클래스는 Laravel 기본 컬렉션 `Illuminate\Support\Collection`을 확장하였으며, 이 기본 컬렉션 클래스는 데이터를 다루는 데 유용한 [다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어 `reject` 메서드는 클로저 평가 결과에 따라 모델들을 컬렉션에서 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션은 Laravel의 기본 컬렉션에 덧붙인 [추가 메서드](/docs/12.x/eloquent-collections#available-methods)도 제공합니다.

모든 컬렉션은 PHP iterable 인터페이스를 구현하는 덕분에, 배열처럼 foreach 루프를 사용할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크 처리

수만 개의 Eloquent 레코드를 `all`이나 `get`으로 한 번에 로드하면 메모리 부족이 발생할 수 있습니다. 대신 `chunk` 메서드를 사용해 데이터를 효율적으로 처리할 수 있습니다.

`chunk`는 Eloquent 모델을 일부분씩 조회해 클로저에 전달하며, 한 번에 전체가 아닌 일부만 메모리에 로드하여 메모리 사용량을 크게 줄일 수 있습니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드 첫 번째 인자는 한 번에 조회할 레코드 수, 두 번째 인자인 클로저는 각 청크마다 호출됩니다. 각 청크 조회 시 데이터베이스 쿼리가 실행됩니다.

만약 청크 결과를 필터링하고, 반복 중 해당 컬럼 값을 함께 업데이트한다면 `chunkById` 메서드를 사용하세요. 일반 `chunk`는 이런 상황에서 예상치 못한 원치 않는 결과가 발생할 수 있습니다. 내부적으로 `chunkById`는 이전 청크의 마지막 `id`보다 큰 레코드만 조회하여 이런 문제를 방지합니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 자체적으로 "where" 조건을 추가하기 때문에, 추가 조건을 논리 그룹으로 묶어 관리하는 것이 좋습니다:

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
### 지연 컬렉션으로 청크 처리하기

`lazy` 메서드는 내부적으로 [청크 방식](#chunking-results)으로 쿼리를 수행하지만, 각 청크를 클로저에 바로 넘기는 대신 단일 스트림처럼 동작하는 [LazyCollection](/docs/12.x/collections#lazy-collections)으로 반환합니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

필터링 결과를 반복하면서 업데이트해야 한다면 `lazyById`를 사용하세요. `lazyById`도 이전 청크의 마지막 `id`보다 큰 레코드를 조회합니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc`는 `id` 내림차순 정렬로 결과를 필터링할 때 사용할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy`처럼, `cursor` 메서드를 사용하면 수만 건의 Eloquent 모델을 반복할 때 메모리를 크게 절약할 수 있습니다.

`cursor`는 데이터베이스에 단일 쿼리만 실행하지만, 실제 모델은 반복할 때마다 하나씩 메모리에 적재합니다. 즉, 반복 시 모델 하나만 메모리에 유지합니다.

> [!WARNING]
> `cursor`는 한 번에 하나의 모델만 메모리에 유지하므로, 관계 미리 로딩(eager loading)을 지원하지 않습니다. 관계를 미리 로딩해야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

`cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환하며, 일반 컬렉션처럼 많은 메서드를 사용할 수 있지만 한 번에 모델 하나만 메모리에 올립니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor`는 일반 쿼리보다 메모리 사용량이 적긴 하지만, 내부적으로 PHP PDO 드라이버가 raw 쿼리 결과를 버퍼에 모두 캐시하므로 결국 메모리 부족이 발생할 수 있습니다. 아주 큰 데이터셋이라면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 선택

Eloquent는 고급 서브쿼리를 지원하여, 단일 쿼리 내에서 관련 테이블에서 정보를 가져올 수 있습니다. 예를 들어, `destinations` 테이블과 목적지로 향하는 `flights` 테이블이 있다고 가정하겠습니다. `flights` 테이블에는 비행기가 도착한 시간을 나타내는 `arrived_at` 컬럼이 있습니다.

쿼리 빌더의 `select` 혹은 `addSelect`에서 서브쿼리를 사용하여, 각 `destinations`와 해당 목적지로 가장 최근에 도착한 비행기 이름을 한 번에 조회할 수 있습니다:

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

쿼리 빌더의 `orderBy` 메서드도 서브쿼리를 지원합니다. 비슷하게, 마지막 비행 도착 시간을 기준으로 목적지를 정렬할 수 있습니다. 한 번의 쿼리로 수행합니다:

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

쿼리조건과 일치하는 모든 레코드를 조회할 수도 있지만, 단일 레코드를 조회할 때는 `find`, `first`, `firstWhere` 메서드를 사용합니다. 이들은 모델 컬렉션 대신 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// 기본 키로 모델 조회...
$flight = Flight::find(1);

// 쿼리 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건에 맞는 첫 번째 모델 조회 대체 문법...
$flight = Flight::firstWhere('active', 1);
```

결과가 없을 경우 다른 처리를 하고 싶을 때 `findOr`와 `firstOr` 메서드를 사용할 수 있으며, 결과가 없으면 주어진 클로저가 실행되고 그 반환값이 결과가 됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 조회 실패 시 예외 발생

404 응답 등을 위해 모델이 없으면 예외가 발생하도록 하고 싶다면, `findOrFail`과 `firstOrFail` 메서드를 사용하세요. 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외가 던져집니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외를 잡지 않으면 HTTP 404 응답이 자동으로 클라이언트에 전달됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 속성으로 레코드를 찾고 없으면 새로운 레코드를 생성합니다. 생성할 때 첫 번째 인수 배열과 두 번째 옵션 배열을 합쳐서 넣습니다.

`firstOrNew`도 비슷하지만, 레코드를 못 찾으면 새 모델 인스턴스만 생성하고 아직 데이터베이스에 저장하지는 않습니다. 수동으로 `save`를 호출해야 합니다:

```php
use App\Models\Flight;

// 이름으로 항공편 조회, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성과 함께 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 인스턴스 반환
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성과 함께 인스턴스 반환
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회하기

Eloquent 모델은 `count`, `sum`, `max` 등 Laravel [쿼리 빌더의 집계 메서드](/docs/12.x/queries#aggregates)를 그대로 사용할 수 있습니다. 이 메서드들은 모델 인스턴스 대신 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용하면 데이터베이스에서 모델을 조회하는 것뿐 아니라 새 레코드 삽입도 쉽습니다. 새 레코드를 삽입하려면 모델 인스턴스를 생성하고 속성을 값으로 설정한 뒤 `save` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 항공편을 데이터베이스에 저장.
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

위 예제에서 HTTP 요청에서 받은 `name` 값을 `Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save`를 호출하면 테이블에 레코드가 삽입되며, `created_at`과 `updated_at` 타임스탬프도 자동으로 설정됩니다.

또한 `create` 메서드를 사용해 단일 구문으로 모델을 저장할 수 있으며, 생성된 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 사용 전엔 반드시 모델에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이는 대량 할당 취약점 방지를 위한 기본 설정입니다. 대량 할당에 대해 더 알고 싶으면 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

`save` 메서드는 이미 존재하는 모델도 업데이트할 수 있습니다. 모델을 조회하고 변경할 속성을 설정한 뒤 다시 `save`를 호출하세요. `updated_at` 타임스탬프는 자동 갱신됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

종종, 기존 모델을 업데이트하거나 없으면 새로 생성해야 할 때가 있습니다. `updateOrCreate` 메서드는 이 작업을 한 번에 수행하며, `save`를 별도로 호출할 필요가 없습니다:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<a name="mass-updates"></a>
#### 대량 업데이트

쿼리 조건에 맞는 여러 모델을 한 번에 업데이트할 수도 있습니다. 예를 들어, `active`이고 목적지가 `San Diego`인 모든 항공편에 `delayed` 플래그를 설정합니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드에 넘긴 배열은 업데이트할 컬럼과 값 쌍입니다. 반환값은 영향을 받은 행(row) 수입니다.

> [!WARNING]
> Eloquent에서 대량 업데이트를 할 때는 각 모델에 대한 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. 이는 실제 모델을 조회하지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 상태 확인하기

Eloquent는 `isDirty`, `isClean`, `wasChanged` 메서드를 통해 모델 속성의 내부 상태 및 변경 여부를 확인할 수 있습니다.

- `isDirty`: 모델이 조회된 이후 변경된 속성이 있는지 확인합니다. 인수로 특정 속성명이나 배열을 넘겨 검사할 수 있습니다.
- `isClean`: 모델이 조회된 이후 변경되지 않은 속성이 있는지 확인합니다.
- `wasChanged`: 현재 요청 사이클에서 마지막 `save` 호출 시 변경된 속성을 확인합니다.

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
$user->isClean('first_name'); // true

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
```

`getOriginal` 메서드는 처음 조회 시 원본 속성값을 반환하며, 특정 속성값도 인수로 받을 수 있습니다:

```php
$user = User::find(1);

$user->name; // John

$user->name = 'Jack';

$user->getOriginal('name'); // John
```

`getChanges`는 마지막 저장 시 변경된 속성을 배열로, `getPrevious`는 마지막 저장 전 원본 값을 배열로 반환합니다:

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

`create` 메서드를 사용해 새 모델을 한 줄로 저장할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 이 전에 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 명시해야 합니다. 이는 대량 할당(메일폼 등에서 일괄 입력)으로 인한 보안 취약점을 방지하기 위해 기본적으로 막여 있기 때문입니다.

대량 할당 취약점은 사용자가 예상치 못한 필드(예: `is_admin`)를 HTTP 요청에 포함시켜 모델을 조작하는 공격입니다.

먼저, `Flight` 모델의 `name` 속성을 대량 할당 허용할 수 있도록 `$fillable` 배열에 추가합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당을 허용하는 속성들.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

이제 `create` 메서드를 안심하고 사용할 수 있습니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있으면, `fill` 메서드로 동시에 속성을 채울 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 타입 컬럼의 값을 대량 할당할 경우, 아래 예시처럼 JSON의 각 키를 `$fillable` 배열에 명시해야 합니다. `$guarded` 속성은 중첩 JSON 속성 업데이트를 지원하지 않으므로 보안을 위해 주의해야 합니다:

```php
/**
 * 대량 할당이 가능한 속성.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용하기

모든 속성을 대량 할당 가능하게 만들려면 `$guarded`를 빈 배열로 설정할 수 있습니다. 단, 이 경우 `fill`, `create`, `update` 등 메서드에 넘기는 배열은 신뢰할 수 있도록 직접 잘 다뤄야 합니다:

```php
/**
 * 대량 할당이 허용되지 않는 속성.
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 없는 속성은 대량 할당 처리 시 무시됩니다. 로컬 개발 환경에서는 이런 동작이 원치 않는 버그를 유발할 수 있습니다.

Laravel에 대량 할당 허용되지 않는 속성을 채웠을 때 예외를 던지도록 설정할 수 있습니다. 보통 `AppServiceProvider` 의 `boot` 메서드에서 호출합니다:

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

Eloquent의 `upsert` 메서드는 조건에 맞는 레코드를 찾아 있으면 업데이트하고, 없으면 삽입하는 원자적 작업을 수행합니다. 첫 번째 인자는 삽입/업데이트할 값들, 두 번째 인자는 유일 식별 컬럼, 세 번째 인자는 업데이트할 컬럼 배열입니다. 모델이 타임스탬프 기능 활성화되어 있으면 자동으로 `created_at`, `updated_at`을 갱신합니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 DB에서 두 번째 인자로 넘긴 컬럼은 "primary" 또는 "unique" 인덱스가 있어야 합니다. MariaDB와 MySQL 드라이버는 두 번째 인자를 무시하고 테이블의 기본, 고유 인덱스를 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면 인스턴스에서 `delete` 메서드를 호출하면 됩니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 삭제하기

위 예시처럼 모델을 조회한 후 삭제하는 대신, 기본 키를 알고 있으면 `destroy` 메서드로 바로 삭제할 수 있습니다. 인수로 단일 키, 여러 키, 키 배열, 컬렉션을 받을 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

소프트 삭제 모델을 영구 삭제하려면 `forceDestroy` 메서드를 사용하세요:

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 모델을 개별적으로 로드하고 `delete` 메서드를 호출하므로, `deleting`과 `deleted` 이벤트가 모델별로 정상 실행됩니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제하기

쿼리 빌더를 사용해 조건에 맞는 모델을 모두 삭제할 수도 있습니다. 예를 들어, 비활성화된 모든 항공편을 삭제할 때:

```php
$deleted = Flight::where('active', 0)->delete();
```

특정 조건 없이 테이블의 모든 모델을 삭제하려면, 조건 없는 쿼리를 실행하세요:

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> 이 경우 실제 모델을 로드하지 않아 `deleting`과 `deleted` 이벤트가 발생하지 않습니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 모델을 실제로 삭제하는 대신 "소프트 삭제"할 수 있습니다. 소프트 삭제된 모델은 DB에서 삭제되지 않고, `deleted_at` 컬럼에 삭제 시간을 기록합니다. 이를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 변환해 줍니다.

테이블에 `deleted_at` 컬럼을 추가해야 하며, Laravel [스키마 빌더](/docs/12.x/migrations)의 헬퍼 메서드를 이용할 수 있습니다:

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

이제 `delete` 메서드를 호출하면 `deleted_at`에 현재 시각이 저장되고, 데이터는 테이블에 남아 있습니다. 소프트 삭제 모델은 쿼리시 기본적으로 결과에서 제외됩니다.

주어진 모델이 소프트 삭제됐는지 확인하려면 `trashed` 메서드를 사용하세요:

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원하기

소프트 삭제된 모델을 원래대로 복원하려면 모델 인스턴스에서 `restore` 메서드를 호출하세요. 이 메서드는 `deleted_at` 컬럼을 `null`로 만듭니다:

```php
$flight->restore();
```

쿼리 빌더로 여러 모델을 한꺼번에 복원할 수도 있습니다. 이 경우도 이벤트는 발생하지 않습니다:

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

소프트 삭제된 모델을 진짜로 DB에서 완전히 삭제하려면 `forceDelete`를 사용하세요:

```php
$flight->forceDelete();
```

관계 쿼리에서도 동일하게 사용할 수 있습니다:

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함하기

기본적으로 소프트 삭제 모델은 쿼리에서 제외되지만, `withTrashed` 메서드를 사용하면 소프트 삭제 모델도 포함시킬 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

관계 쿼리에서도 호출할 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드는 오직 소프트 삭제된 모델만 조회합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 프루닝(주기적 삭제)

필요 없는 오래된 모델을 주기적으로 삭제하려면, `Illuminate\Database\Eloquent\Prunable` 또는 `MassPrunable` 트레이트를 모델에 추가하고 `prunable` 메서드를 구현하세요. 이 메서드는 삭제 대상 모델을 조회하는 쿼리 빌더를 반환해야 합니다:

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
     * 프루닝 대상 모델 조회 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`Prunable` 모델에 `pruning` 메서드를 정의하면, 모델 삭제 전에 호출되어 연결된 파일 삭제 같은 추가 작업에 이용할 수 있습니다:

```php
/**
 * 프루닝 준비 작업.
 */
protected function pruning(): void
{
    // ...
}
```

설정 후, `model:prune` Artisan 명령어를 `routes/console.php`에 스케줄링 하여 주기적으로 실행하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

기본적으로 `model:prune` 명령어는 `app/Models` 디렉토리에서 프루닝 대상 모델을 자동으로 감지합니다. 다른 위치라면 `--model` 옵션으로 모델 클래스를 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 제외하고 나머지를 프루닝하려면 `--except` 옵션을 사용하세요:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 주면 실제 삭제하지 않고, 삭제 예정인 레코드 수를 미리 알려줍니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델도 조건에 일치하면 `forceDelete` 되어 완전히 삭제됩니다.

<a name="mass-pruning"></a>
#### 대량 프루닝

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하는 모델은 대량 삭제 쿼리로 모델을 삭제합니다. 이 경우 `pruning` 메서드나 `deleting`, `deleted` 이벤트는 호출되지 않으며, 모델을 실제 로드하지 않으므로 프루닝 속도가 더 빠릅니다:

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
     * 프루닝 대상 모델 조회 쿼리 반환.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

`replicate` 메서드를 사용해 기존 모델 인스턴스의 저장되지 않은 복사본을 만들 수 있습니다. 많은 속성이 같은 모델을 복사할 때 유용합니다:

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

복제할 때 제외할 속성을 배열로 넘길 수도 있습니다:

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

전역 스코프는 특정 모델에 대한 모든 쿼리에 조건을 자동으로 추가할 수 있습니다. Laravel 내장 소프트 삭제 기능도 전역 스코프를 활용해 기본적으로 "삭제 안 된" 모델만 조회합니다. 전역 스코프를 직접 작성하면 모든 쿼리에서 일정 조건을 편리하게 유지할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

전역 스코프를 새로 만들려면 `make:scope` Artisan 명령어를 사용하세요. 생성된 스코프 클래스는 `app/Models/Scopes` 디렉토리에 위치합니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성하기

전역 스코프는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현한 클래스입니다. 이 인터페이스는 쿼리 빌더에 제약 조건을 적용하는 `apply` 메서드를 요구합니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 지정된 Eloquent 쿼리 빌더에 스코프를 적용.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프가 select 절에 컬럼을 추가하려면 `select` 대신 `addSelect` 메서드를 사용해야 기존 절을 덮어쓰지 않습니다.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용하기

전역 스코프를 모델에 할당하려면 `ScopedBy` 속성(attribute)을 모델에 붙이세요:

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

또는 모델의 `booted` 메서드에서 `addGlobalScope`를 호출해 수동 등록할 수도 있습니다. 인수로 스코프 인스턴스를 넘깁니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 booted 메서드.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예제에서 `User::all()` 호출 시 다음과 같은 SQL이 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 전역 스코프

간단한 전역 스코프는 별도 클래스를 만들지 않고, 클로저 형태로 정의할 수 있습니다. `addGlobalScope` 메서드에 스코프 이름과 클로저를 넘기면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 booted 메서드.
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

쿼리에서 특정 전역 스코프를 없애려면 `withoutGlobalScope` 메서드를 사용하세요. 클래스로 정의한 스코프는 클래스 이름을 넘기고, 클로저로 정의한 스코프는 이름 문자열을 넘깁니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();

User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 모든 전역 스코프를 제거하려면 `withoutGlobalScopes` 메서드를 사용합니다:

```php
// 모든 전역 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 전역 스코프 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 공통 쿼리 조건들을 재사용할 수 있게 해줍니다. Eloquent 메서드에 `Scope` 속성을 부착해 정의하며, 쿼리 빌더를 인수로 받아 조건을 추가해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기가 많은 사용자만 조회하는 스코프.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 조회하는 스코프.
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

정의한 스코프는 모델 쿼리 시 메서드처럼 호출 가능합니다. 여러 스코프를 체이닝할 수도 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조건과 쓸 때는 람다 클로저로 논리 그룹화를 해야 올바른 쿼리가 생성됩니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

복잡할 경우 Laravel은 "higher order" `orWhere` 메서드도 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 파라미터를 전달하는 것도 가능합니다. 추가 매개변수를 함수에 정의하고, 메서드 호출 시 인자를 넘겨주세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 지정한 타입의 사용자만 조회하는 스코프.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 속성

스코프로 제한한 속성과 일치하는 모델을 생성하려면, 쿼리 빌더에서 `withAttributes` 메서드를 사용합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 초안 상태(Post draft)만 조회하는 스코프.
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

`withAttributes`는 전달한 값으로 `where` 조건을 붙이고, 해당 스코프로 생성한 모델에 기본 속성을 지정합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes`의 `asConditions`를 `false`로 하면 조건 연결 없이 기본 속성만 추가합니다:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교하기

두 모델이 "같은"지 확인해야 할 때가 있습니다. `is`와 `isNot` 메서드를 사용하면 두 모델이 기본 키, 테이블, 데이터베이스 연결이 같은지 쉽게 비교할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`belongsTo`, `hasOne`, `morphTo`, `morphOne` 관계에서도 이 메서드를 사용할 수 있어, 관련 모델을 쿼리 없이 직접 비교할 때 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션에 직접 브로드캐스트하려면 Laravel의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 디스패치해 모델 생명주기 중 여러 시점에 후킹할 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 기존 모델을 DB에서 가져오면 발생
- `creating`/`created`: 새 모델이 처음 저장될 때 발생
- `updating`/`updated`: 기존 모델이 수정되고 `save` 호출 시 발생
- `saving`/`saved`: 생성 또는 업데이트 시 발생 (속성 변경 여부 상관없음)
- 이벤트 이름이 `-ing`로 끝나면 변경전에 호출, `-ed`로 끝나면 변경 후에 호출

모델 이벤트를 듣고 싶으면 Eloquent 모델에 `$dispatchesEvents` 속성을 정의해 이벤트 이름을 커스텀 이벤트 클래스에 매핑하세요. 이벤트 클래스는 affected 모델 인스턴스를 생성자에서 받는 걸 기대합니다:

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

이벤트 정의 후엔 [이벤트 리스너](/docs/12.x/events#defining-listeners)를 통해 이벤트 핸들러를 등록하세요.

> [!WARNING]
> 대량 업데이트, 삭제 시에는 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다. 실제 모델이 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용

커스텀 이벤트 클래스를 만들지 않고, 모델 `booted` 메서드 내에서 클로저를 등록해 이벤트를 처리할 수도 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 booted 메서드.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 [큐 가능한 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 활용해 백그라운드에서 이벤트를 처리할 수도 있습니다:

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

많은 이벤트를 하나의 모델에서 듣는다면, 옵저버 클래스로 그룹화하는 것이 편리합니다. 옵저버 클래스는 이벤트 이름에 해당하는 메서드를 갖고, 각각 영향받는 모델을 인수로 받습니다. `make:observer` Artisan 명령이 옵저버 클래스를 쉽게 생성해줍니다:

```shell
php artisan make:observer UserObserver --model=User
```

클래스는 `app/Observers`에 생성되고, 다음과 같이 생겼습니다:

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

    // ...updated, deleted, restored, forceDeleted 등 다른 이벤트 메서드들
}
```

옵저버를 등록하려면 모델에 `ObservedBy` 속성을 붙이거나:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는 `AppServiceProvider`의 `boot`에서 `observe` 메서드를 호출하세요:

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
> 옵저버는 `saving`, `retrieved` 등 추가 이벤트도 수신할 수 있습니다. 관련 이벤트는 [이벤트 파트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 DB 트랜잭션 내에서 생성될 때 옵저버를 트랜잭션 커밋 후에 이벤트 핸들러가 실행되도록 하려면, 옵저버가 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 트랜잭션이 없으면 즉시 실행됩니다:

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
### 이벤트 음소거

모델 관련 이벤트를 일시적으로 "음소거"해야 할 때가 있습니다. 이때 `withoutEvents` 메서드를 사용합니다. 인수로 클로저를 넘기며, 클로저 내에서 발생하는 모델 이벤트는 디스패치되지 않고, 클로저 반환값을 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 모델 저장하기

특정 모델을 이벤트 없이 "조용히" 저장하고 싶으면 `saveQuietly` 메서드를 사용하세요:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이 외에도 `deleteQuietly`, `forceDeleteQuietly`, `restoreQuietly` 등을 사용해 이벤트 없이 업데이트, 삭제, 복원, 복제 작업을 할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```