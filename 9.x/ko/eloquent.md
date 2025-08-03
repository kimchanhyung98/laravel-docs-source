# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성하기](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키(Primary Keys)](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격모드 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [청크로 결과 처리하기](#chunking-results)
    - [지연 컬렉션을 이용한 청크 처리](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회하기](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 갱신](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [갱신](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제(Soft Deleting)](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 정리(Pruning)](#pruning-models)
- [모델 복제(Replicating)](#replicating-models)
- [쿼리 스코프(Query Scopes)](#query-scopes)
    - [글로벌 스코프(Global Scopes)](#global-scopes)
    - [로컬 스코프(Local Scopes)](#local-scopes)
- [모델 비교하기](#comparing-models)
- [이벤트](#events)
    - [클로저 이벤트 사용하기](#events-using-closures)
    - [옵저버(Observers)](#observers)
    - [이벤트 비활성화](#muting-events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스와 상호작용하기 쉽게 만들어 주는 객체 관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블은 해당 테이블과 상호작용하기 위한 "모델" 클래스로 대응됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, 레코드 삽입, 갱신, 삭제도 쉽게 할 수 있도록 도와줍니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결 설정을 반드시 완료하세요. 데이터베이스 설정에 관한 자세한 내용은 [데이터베이스 설정 문서](/docs/9.x/database#configuration)를 참고하시기 바랍니다.

#### Laravel 부트캠프

Laravel이 처음이라면, 자유롭게 [Laravel 부트캠프](https://bootcamp.laravel.com)부터 시작해 보세요. 이 부트캠프는 Eloquent를 사용하여 첫 Laravel 애플리케이션을 만드는 과정을 안내합니다. Laravel과 Eloquent가 제공하는 모든 기능을 빠르게 경험할 수 있는 좋은 방법입니다.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기 (Generating Model Classes)

먼저, Eloquent 모델을 생성해 봅시다. 보통 모델은 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 상속받습니다. `make:model` Artisan 명령어를 통해 새 모델을 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성하면서 [데이터베이스 마이그레이션](/docs/9.x/migrations)도 같이 생성하려면 `--migration` 또는 `-m` 옵션을 함께 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 공장(factory), 시더(seeder), 정책(policy), 컨트롤러(controller), 폼 요청(form request) 등 다양한 클래스도 함께 생성할 수 있고, 여러 옵션을 조합해 동시에 여러 클래스를 만들 수도 있습니다:

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

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 생성
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성
php artisan make:model Flight --policy

# 모델과 마이그레이션, 팩토리, 시더, 컨트롤러 생성
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 생성 단축키
php artisan make:model Flight --all

# 피벗 모델 생성
php artisan make:model Member --pivot
```

<a name="inspecting-models"></a>
#### 모델 정보 확인하기

모델 클래스 코드만 보고 모든 속성과 연관관계를 파악하기 어려울 때가 있습니다. 이럴 땐 `model:show` Artisan 명령어를 사용해 보세요. 모델의 속성과 연관관계를 한눈에 보여 줍니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙 (Eloquent Model Conventions)

`make:model` 명령어로 생성하는 모델은 `app/Models` 디렉터리에 위치합니다. 기본 모델 클래스를 살펴보고, Eloquent의 중요한 규칙을 살펴봅시다:

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
### 테이블 이름 (Table Names)

위 예제를 보면, `Flight` 모델에 어떤 데이터베이스 테이블과 연결되는지 명시하지 않은 것을 알 수 있습니다. Eloquent는 관례에 따라 클래스 이름을 스네이크 케이스(snake_case)로 바꾸고 복수형으로 만든 이름을 테이블 이름으로 자동 인식합니다. 즉, `Flight` 모델은 `flights` 테이블에 연결되며, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블과 연결됩니다.

만약 테이블 이름이 이 규칙에 맞지 않는다면, 모델 클래스에 `protected $table` 속성을 정의하여 직접 이름을 지정할 수 있습니다:

```
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
### 기본 키(Primary Keys)

Eloquent는 기본적으로 각 모델에 `id`라는 이름의 기본 키 컬럼이 있다고 가정합니다. 만약 다른 컬럼을 기본 키로 사용하려면 모델에서 `protected $primaryKey` 속성을 정의해 주세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연결된 테이블의 기본 키 컬럼
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

기본 키는 자동 증가하는 정수형 값이라고도 가정합니다. 기본 키가 자동 증가하지 않거나 숫자가 아닌 경우, 모델에 `public $incrementing = false;` 속성을 정의하세요:

```
<?php

class Flight extends Model
{
    /**
     * 모델의 기본 키가 자동 증가하는지 여부
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본 키가 정수가 아니라면, `protected $keyType` 속성을 `string`으로 정의해야 합니다:

```
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
#### 복합 기본 키("Composite" Primary Keys)

Eloquent 모델은 각 모델마다 유일하게 식별 가능한 하나의 "ID"가 반드시 있어야 합니다. 복합 기본 키는 지원하지 않습니다. 대신, 별도로 다중 컬럼 유니크 인덱스를 추가하는 것은 자유롭습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키 (UUID & ULID Keys)

기본 키에 자동 증가 정수 대신 UUID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 물론, 모델 테이블에 [UUID 형식 컬럼](/docs/9.x/migrations#column-method-uuid)이 있어야 합니다:

```
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

기본적으로 `HasUuids` 트레이트는 정렬 가능한(ordered) UUID를 생성하며, 이는 데이터베이스 인덱싱에 더 효율적입니다.

UUID 생성 방식을 직접 정의하고 싶다면, 모델에 `newUniqueId` 메서드를 작성하세요. 또한 UUID를 생성할 컬럼을 지정하려면 `uniqueIds` 메서드를 작성할 수 있습니다:

```
use Ramsey\Uuid\Uuid;

/**
 * 모델에 새 UUID 생성
 *
 * @return string
 */
public function newUniqueId()
{
    return (string) Uuid::uuid4();
}

/**
 * UUID를 부여할 컬럼 목록 반환
 *
 * @return array
 */
public function uniqueIds()
{
    return ['id', 'discount_code'];
}
```

UUID 대신 ULID를 쓸 수도 있습니다. ULID는 UUID와 비슷하지만 26자 길이에 정렬 가능하다는 점이 특징입니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 추가하고, 테이블에 [ULID 형식 컬럼](/docs/9.x/migrations#column-method-ulid)이 있어야 합니다:

```
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

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼이 테이블에 있다고 기대합니다. 레코드 생성 및 갱신 시 자동으로 해당 컬럼을 업데이트해 줍니다. 자동 관리를 원하지 않는다면, 모델에 `public $timestamps = false;` 설정을 추가하세요:

```
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

타임스탬프 저장 형식을 바꾸려면 `$dateFormat` 속성을 지정하세요. 이 속성은 데이터베이스 저장 및 배열/JSON 직렬화 시 날짜 형식을 결정합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 컬럼 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼 이름을 바꾸려면, 모델 상수 `CREATED_AT`과 `UPDATED_AT`을 정의하면 됩니다:

```
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프를 갱신하지 않고 작업하고 싶으면, `withoutTimestamps` 메서드에 클로저를 넘겨 실행하세요:

```
Model::withoutTimestamps(fn () => $post->increment(['reads']));
```

<a name="database-connections"></a>
### 데이터베이스 연결 (Database Connections)

모델은 기본적으로 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 다른 연결을 사용하려면 `$connection` 속성에 연결 이름을 지정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델에서 사용할 데이터베이스 연결 이름
     *
     * @var string
     */
    protected $connection = 'sqlite';
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값 (Default Attribute Values)

새로 생성된 모델 인스턴스는 기본적으로 어떠한 속성 값도 가지지 않습니다. 특정 속성의 기본값을 지정하려면, `$attributes` 배열 속성에 기본값을 생소 데이터 형식(raw)으로 설정하세요:

```
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
### Eloquent 엄격모드 설정 (Configuring Eloquent Strictness)

Eloquent는 다양한 상황에서 동작과 "엄격도"를 조절할 수 있는 메서드를 제공합니다.

우선 `preventLazyLoading` 메서드는 선택적 불리언 값을 받아 지연 로딩(lazy loading)을 막을지 여부를 결정합니다. 예를 들어, 프로덕션 환경에서는 지연 로딩을 허용하되, 개발 환경에서는 막으려 할 때 사용합니다. 보통 이것은 `AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또, `preventSilentlyDiscardingAttributes` 메서드를 사용하면, `fillable` 속성에 없는 속성을 대량 할당할 때 예외를 발생시킬 수 있어 개발 중 오류를 쉽게 발견할 수 있습니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

마지막으로, 실제로 쿼리에서 선택되지 않은 속성(컬럼)에 접근할 때 예외를 발생시키도록 할 수 있는데, `preventAccessingMissingAttributes` 메서드를 사용합니다:

```php
Model::preventAccessingMissingAttributes(! $this->app->isProduction());
```

<a name="enabling-eloquent-strict-mode"></a>
#### Eloquent "엄격모드" 활성화

앞서 설명한 세 가지 행동을 모두 활성화하려면, `shouldBeStrict` 메서드를 호출하면 됩니다:

```php
Model::shouldBeStrict(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기 (Retrieving Models)

모델과 [데이터베이스 테이블](/docs/9.x/migrations#writing-migrations)을 생성했다면, 이제 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 해당 테이블에 대해 강력한 [쿼리 빌더](/docs/9.x/queries) 역할을 합니다. `all` 메서드를 호출하면 모델과 연결된 테이블의 모든 레코드를 가져옵니다:

```
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

`all`은 모든 결과를 반환하지만, 각 모델은 쿼리 빌더이므로 추가 제약을 붙여 `get`으로 결과를 가져올 수 있습니다:

```
$flights = Flight::where('active', 1)
               ->orderBy('name')
               ->take(10)
               ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더 메서드들](/docs/9.x/queries)을 모두 사용할 수 있음을 기억하세요.

<a name="refreshing-models"></a>
#### 모델 새로고침

이미 조회한 모델 인스턴스를 최신 데이터로 새로고침하려면 `fresh` 또는 `refresh` 메서드를 사용합니다. `fresh`는 새로운 데이터로 해당 모델을 다시 조회해 새 인스턴스를 반환합니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh`는 기존 모델 인스턴스를 새 데이터로 다시 채웁니다. 관계 데이터도 함께 갱신됩니다:

```
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션 (Collections)

`all`과 `get`은 여러 레코드를 조회하지만, 평범한 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

`Eloquent\Collection`은 Laravel의 기본 `Illuminate\Support\Collection`을 상속하며, [다양한 유용한 메서드](/docs/9.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드로 특정 조건에 맞는 모델을 제거할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function ($flight) {
    return $flight->cancelled;
});
```

Eloquent 컬렉션은 일반 컬렉션 메서드 외에도 Eloquent 모델 전용 메서드들을 제공합니다.

Laravel 컬렉션은 PHP 반복자 인터페이스를 구현하므로 배열처럼 반복문을 돌릴 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 청크로 결과 처리하기 (Chunking Results)

수만 개 이상의 Eloquent 레코드를 `all`이나 `get`으로 한꺼번에 불러오면 메모리 부족이 발생할 수 있습니다. 이때 `chunk` 메서드를 이용하면 일정 단위로 나누어 처리하며 메모리를 효율적으로 사용할 수 있습니다.

`chunk`는 한 번에 일부 모델만 조회해 클로저에 전달합니다. 청크 단위로만 메모리에 올라가므로 메모리 사용량이 크게 줄어듭니다:

```php
use App\Models\Flight;

Flight::chunk(200, function ($flights) {
    foreach ($flights as $flight) {
        //
    }
});
```

첫 인자는 청크 크기(한 번에 조회할 레코드 수), 두 번째 인자는 청크마다 호출할 클로저입니다. 각 청크마다 쿼리가 실행됩니다.

반복문 도중 일부 컬럼 값을 갱신하면서 조건으로 필터할 때는 `chunkById`를 쓰는 걸 추천합니다. 청크가 항상 이전 모델의 ID보다 큰 레코드만 쿼리하므로, 의도치 않은 결과를 방지할 수 있습니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function ($flights) {
        $flights->each->update(['departed' => false]);
    }, $column = 'id');
```

<a name="chunking-using-lazy-collections"></a>
### 지연 컬렉션을 이용한 청크 처리 (Chunking Using Lazy Collections)

`lazy` 메서드는 `chunk`처럼 내부적으로 청크 단위로 쿼리하지만, 청크를 직접 클로저에 넘기지 않고, 하나로 평탄화된 [`LazyCollection`](/docs/9.x/collections#lazy-collections)을 반환해 결과를 스트림처럼 한꺼번에 처리할 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    //
}
```

`lazy`의 결과를 필터링하면서 값 업데이트를 할 때는, `lazyById` 메서드를 사용하세요:

```php
Flight::where('departed', true)
    ->lazyById(200, $column = 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc`를 쓰면 내림차순 기준 ID 필터링이 가능합니다.

<a name="cursors"></a>
### 커서(Cursor)

`lazy`와 비슷하게, `cursor` 메서드는 수만 건의 레코드를 처리할 때 메모리 사용을 크게 줄입니다.

`cursor`는 데이터베이스에 단 한 번의 쿼리만 보내지만, 실제로 데이터 모델은 반복문에 진입할 때마다 하나씩 메모리에 올려 처리합니다. 따라서 한 번에 하나의 모델만 메모리에 존재하는 셈입니다.

> [!WARNING]
> `cursor`는 한 번에 한 모델씩 처리하기 때문에 관계를 미리 로드(eager load)할 수 없습니다. 만약 관계도 함께 미리 로드해 처리해야 한다면, 대신 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

내부적으로 `cursor`는 PHP [제너레이터(Generator)](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    //
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환하며, 이는 일반 Laravel 컬렉션에서 지원하는 메서드 상당수를 사용할 수 있고, 언제나 모델을 하나씩 메모리에 할당합니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

비록 `cursor`는 메모리 사용이 적지만, 결국은 [PHP PDO 드라이버가 쿼리 결과를 내부에 모두 캐시하기 때문에](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php) 매우 큰 데이터는 메모리가 부족해질 수 있습니다. 감당하기 어려운 양이라면, [lazy 메서드](#chunking-using-lazy-collections)를 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리 (Advanced Subqueries)

<a name="subquery-selects"></a>
#### 서브쿼리 셀렉트 (Subquery Selects)

Eloquent는 관련 테이블에서 정보를 뽑아와 단일 쿼리로 처리할 수 있는 고급 서브쿼리를 지원합니다. 예를 들어 목적지(`destinations`) 테이블과 해당 목적지로의 비행 `flights` 테이블이 있다고 할 때, `flights`테이블의 `arrived_at` 컬럼을 사용해 마지막으로 도착한 비행을 찾는 쿼리를 아래처럼 작성할 수 있습니다:

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
#### 서브쿼리 정렬 (Subquery Ordering)

쿼리 빌더의 `orderBy` 함수도 서브쿼리를 지원합니다. 앞 예시에서 마지막 도착한 비행 시각 기준으로 목적지를 정렬할 수 있습니다. 단일 쿼리로 처리 가능합니다:

```
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 조회하기 (Retrieving Single Models / Aggregates)

여러 레코드를 반환하는 대신 `find`, `first`, `firstWhere` 메서드로 단일 모델을 조회할 수 있습니다. 결과는 컬렉션이 아니라 단일 모델 인스턴스를 반환합니다:

```
use App\Models\Flight;

// 기본 키로 모델 조회
$flight = Flight::find(1);

// 쿼리 조건을 만족하는 첫 번째 모델 조회
$flight = Flight::where('active', 1)->first();

// 쿼리 조건을 만족하는 첫 번째 모델 조회의 대체 기술
$flight = Flight::firstWhere('active', 1);
```

결과가 없을 경우 다른 동작을 하고 싶을 땐 `findOr`나 `firstOr` 메서드를 사용하세요. 결과가 없으면 전달된 클로저를 실행하며, 클로저 반환값이 메서드 결과가 됩니다:

```
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 예외 발생: 모델 미발견 (Not Found Exceptions)

모델을 찾지 못할 때 예외를 발생시켜 라우트나 컨트롤러에서 활용하고 싶다면, `findOrFail`이나 `firstOrFail`을 사용하세요. 찾는 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외가 발생합니다:

```
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

예외를 잡지 않으면 자동으로 404 HTTP 응답이 클라이언트에 전달됩니다:

```
use App\Models\Flight;

Route::get('/api/flights/{id}', function ($id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성하기 (Retrieving Or Creating Models)

`firstOrCreate` 메서드는 주어진 컬럼/값으로 레코드를 찾고, 없으면 첫 번째 배열과 선택적 두 번째 매개변수를 합친 값으로 레코드를 생성합니다.

`firstOrNew`는 마찬가지로 레코드를 조회하지만 없으면 새 모델 인스턴스를 반환하는데, 데이터베이스에는 저장하지 않습니다. 새 인스턴스를 저장하려면 직접 `save`를 호출해야 합니다:

```
use App\Models\Flight;

// 이름으로 조회, 없으면 생성
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성도 포함해 생성
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 인스턴스 생성(저장하지 않음)
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 속성 포함 새 인스턴스 생성(저장하지 않음)
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회하기 (Retrieving Aggregates)

Eloquent 모델에서도 Laravel의 [쿼리 빌더 집계 쿼리들](/docs/9.x/queries#aggregates)을 쓸 수 있습니다. 이때는 모델 인스턴스가 아니라 스칼라 값이 반환됩니다:

```
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 갱신 (Inserting & Updating Models)

<a name="inserts"></a>
### 삽입 (Inserts)

모델을 데이터베이스에 새로 추가할 때는 새 모델 인스턴스를 만들고, 속성을 설정한 뒤 `save`를 호출합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 비행 정보 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // 요청 유효성 검사...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();
    }
}
```

예제에서 HTTP 요청의 `name` 필드를 모델의 `name` 속성에 할당합니다. `save`를 호출하면 DB에 레코드가 삽입되고, 자동으로 `created_at`과 `updated_at` 타임스탬프가 설정됩니다.

또 다른 방법으로, `create` 메서드를 쓰면 한 줄만에 새 모델을 저장하고 인스턴스를 받을 수 있습니다:

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create`를 사용하려면 모델에 `fillable` 혹은 `guarded` 속성을 정의해 대량 할당을 허용해야 합니다. 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참조하세요.

<a name="updates"></a>
### 갱신 (Updates)

`save` 메서드로 이미 데이터베이스에 존재하는 모델도 갱신할 수 있습니다. 모델을 조회하여 속성을 변경한 뒤 `save`를 호출합니다. `updated_at`은 자동 갱신됩니다:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<a name="mass-updates"></a>
#### 대량 갱신 (Mass Updates)

특정 조건에 맞는 다수 모델을 한꺼번에 갱신하려면 쿼리 뒤에 `update` 메서드를 사용하세요. 예를 들어, 활성 상태(`active`)이고 목적지가 `San Diego`인 모든 항공편을 지연 상태로 표시할 때:

```
Flight::where('active', 1)
      ->where('destination', 'San Diego')
      ->update(['delayed' => 1]);
```

`update` 메서드는 갱신할 컬럼과 값(키-값 배열)을 받고, 갱신된 행 개수를 반환합니다.

> [!WARNING]
> 대량 갱신 시에는 모델 이벤트인 `saving`, `saved`, `updating`, `updated`가 발생하지 않습니다. 이는 실제 모델 인스턴스를 조회하지 않고 직접 쿼리를 수행하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 상태 확인하기

Eloquent는 `isDirty`, `isClean`, `wasChanged` 메서드를 통해 모델 내부 상태와 속성 변경 여부를 확인할 수 있습니다.

- `isDirty`는 모델이 로드된 이후 변경된 속성이 있는지 확인합니다. 특정 속성도 지정 가능.
- `isClean`은 로드 이후 변경이 없는 속성을 확인합니다.
- `wasChanged`는 현재 요청 내 마지막 저장 시점에 변경된 속성 여부를 확인합니다.

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

`getOriginal` 메서드는 모델 조회 시점의 원본 속성 값을 배열 또는 특정 속성 단위로 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = "Jack";
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 배열 반환
```

<a name="mass-assignment"></a>
### 대량 할당 (Mass Assignment)

`create` 메서드를 사용해 배열로 새 모델을 저장할 수 있습니다:

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만, 대량 할당을 안전하게 관리하기 위해 `fillable` 또는 `guarded` 속성을 모델에 반드시 설정해야 합니다.

대량 할당 취약점은 예상치 못한 HTTP 필드가 데이터베이스 컬럼을 변경하는 문제입니다. 예를 들어, 악의적 사용자가 `is_admin` 파라미터를 보내어 관리자 권한을 얻는 식입니다.

따라서, 대량 할당을 허용할 속성을 `$fillable` 배열에 명시해야 합니다. 예를 들어, `Flight` 모델에서 `name` 속성을 허용하려면:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당 허용 속성 목록
     *
     * @var array
     */
    protected $fillable = ['name'];
}
```

이후 `create`로 새 모델을 저장할 수 있습니다:

```
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드로 속성 배열을 채울 수 있습니다:

```
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당 & JSON 컬럼

JSON 컬럼에 대량 할당할 때는 `$fillable` 배열에 각 JSON 키도 정확히 명시해야 합니다. 보안을 위해, `guarded` 속성으로 중첩 JSON 속성 업데이트는 지원하지 않습니다:

```
/**
 * 대량 할당 허용 속성 목록
 *
 * @var array
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용

만약 모든 속성을 대량 할당 가능하게 하려면, `$guarded`를 빈 배열로 설정하세요. 단, 직접 전달하는 배열을 정교하게 다뤄야 합니다:

```
/**
 * 대량 할당을 허용하지 않는 속성 목록
 *
 * @var array
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외 처리

기본적으로 `$fillable`에 없는 속성은 대량 할당 시 조용히 무시됩니다. 로컬 개발 중에는 왜 속성 변경이 안 되는지 혼란스러울 수 있습니다.

이때 `preventSilentlyDiscardingAttributes`를 호출하면, 허용되지 않은 속성을 대량 할당할 때 예외를 발생시켜 문제를 직관적으로 파악할 수 있습니다. 보통 서비스 프로바이더 `boot` 메서드에서 설정합니다:

```
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트 (Upserts)

업서트는 조건에 맞는 모델이 있으면 갱신하고, 없으면 새로 생성하는 작업입니다. `updateOrCreate`는 `firstOrCreate`와 달리 저장도 완료하므로 `save`를 따로 호출할 필요가 없습니다:

```
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

한 번에 여러 건 업서트를 하려면 `upsert` 메서드를 사용하세요. 첫 인자는 삽입 또는 갱신할 값들, 두 번째는 레코드를 유일하게 식별할 컬럼들, 세 번째는 기존 레코드가 있을 때 갱신할 컬럼들입니다. 타임스탬프는 자동으로 관리됩니다:

```
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서 두 번째 인자에 지정하는 컬럼에는 기본 키(primary)나 유니크(unique) 인덱스가 있어야 합니다. MySQL에서는 두 번째 인자를 무시하고 자동으로 기본 키와 유니크 인덱스를 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제 (Deleting Models)

모델 인스턴스에서 `delete` 메서드를 호출해 삭제할 수 있습니다:

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

모델 관련 테이블의 모든 레코드를 삭제하고 자동 증가 값도 초기화하려면 `truncate`를 사용하세요:

```
Flight::truncate();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 삭제

기본 키를 알고 있다면, 명시적으로 모델을 조회하지 않고도 `destroy` 메서드로 삭제할 수 있습니다. 단일 키 뿐 아니라 다중 키, 키 배열, 컬렉션 모두 인자로 받을 수 있습니다:

```
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

> [!WARNING]
> `destroy`는 각 모델을 개별로 로드하고 `delete`를 호출하여 `deleting` 및 `deleted` 이벤트가 올바르게 발생하도록 합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

조건에 맞는 모델을 모두 삭제할 수도 있습니다. 예를 들어 비활성(`active`가 0) 모델을 삭제:

```
$deleted = Flight::where('active', 0)->delete();
```

> [!WARNING]
> 대량 삭제 쿼리를 실행하면 해당 모델의 `deleting` 및 `deleted` 이벤트가 발생하지 않습니다. 이는 실제 모델을 로드하지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제 (Soft Deleting)

모델을 실제 삭제하는 대신, `deleted_at` 컬럼에 삭제 시각을 기록하여 논리적 삭제를 할 수도 있습니다. 이렇게 하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요:

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

> [!NOTE]
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` / `Carbon` 객체로 캐스팅해 줍니다.

`deleted_at` 컬럼도 테이블에 추가해야 하며, Laravel 스키마 빌더의 `softDeletes()` 메서드를 사용하면 됩니다:

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

이제 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 시각으로 설정되고 레코드는 테이블에 남아있게 됩니다. 쿼리 시 소프트 삭제된 모델은 기본적으로 제외됩니다.

모델이 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 호출하세요:

```
if ($flight->trashed()) {
    //
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원하기

실수로 삭제한 모델을 복원하려면 `restore` 메서드를 호출하면 됩니다. 이 메서드는 `deleted_at`을 `null`로 설정합니다:

```
$flight->restore();
```

쿼리에서 복원하려면 `restore` 메서드를 사용하며, 대량 복원도 가능합니다. 단, 모델 이벤트는 발생하지 않습니다:

```
Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();
```

관계 쿼리에서도 `restore`를 사용 가능:

```
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 완전 삭제 (Permanently Deleting Models)

소프트 삭제된 모델을 완전히 삭제하려면 `forceDelete` 메서드를 사용하세요:

```
$flight->forceDelete();
```

관계 쿼리에서도 `forceDelete`가 가능합니다:

```
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 모델 포함하기

소프트 삭제된 모델이 기본적으로 쿼리 결과에서 제외되지만, `withTrashed` 메서드를 호출하면 포함시킬 수 있습니다:

```
use App\Models\Flight;

$flights = Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
```

관계 쿼리에서도 사용 가능합니다:

```
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드를 사용하면 오직 소프트 삭제된 모델만 조회합니다:

```
$flights = Flight::onlyTrashed()
                ->where('airline_id', 1)
                ->get();
```

<a name="pruning-models"></a>
## 모델 정리 (Pruning Models)

필요 없는 오래된 모델을 주기적으로 삭제하려면, `Illuminate\Database\Eloquent\Prunable` 또는 `MassPrunable` 트레이트를 모델에 추가하세요. `prunable` 메서드에서 쿼리를 구현해 제거할 모델 조건을 반환하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * 정리 대상 모델 쿼리 반환
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

`pruning` 메서드도 정의 가능하며, 삭제 전 파일 등 추가 리소스를 정리할 때 유용합니다:

```
/**
 * 정리 준비 작업
 *
 * @return void
 */
protected function pruning()
{
    //
}
```

`model:prune` Artisan 명령어를 스케줄러에 등록해 주기적으로 실행하세요:

```
/**
 * 애플리케이션 커맨드 스케줄 정의
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('model:prune')->daily();
}
```

`model:prune` 명령어는 기본적으로 `app/Models` 내 모든 Prunable 모델을 감지하며, `--model` 옵션으로 특정 모델만 지정도 가능합니다:

```
$schedule->command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델을 제외하고 정리하려면 `--except` 옵션을 사용합니다:

```
$schedule->command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션으로 실제 삭제 없이 몇 건을 삭제할지 시뮬레이션할 수도 있습니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제한 모델도 prunable 쿼리와 일치하면 영구 삭제(`forceDelete`) 됩니다.

<a name="mass-pruning"></a>
#### 대량 정리 (Mass Pruning)

`MassPrunable` 트레이트를 사용하면 대량 삭제 쿼리로 모델을 삭제해 `pruning` 메서드 호출이나 `deleting`/`deleted` 모델 이벤트가 발생하지 않습니다. 이는 성능 최적화 목적입니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * 정리 대상 모델 쿼리 반환
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
## 모델 복제 (Replicating Models)

`replicate` 메서드로 기존 모델을 복제해 아직 저장되지 않은 새 인스턴스를 만들 수 있습니다. 공통 속성이 많은 모델을 복제할 때 유용합니다:

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

복제 시 일부 속성만 제외하려면 배열로 지정하면 됩니다:

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
## 쿼리 스코프 (Query Scopes)

<a name="global-scopes"></a>
### 글로벌 스코프 (Global Scopes)

글로벌 스코프는 특정 모델의 모든 쿼리에 공통 조건을 추가할 수 있습니다. Laravel의 소프트 삭제가 이 기능을 사용해 자동으로 "삭제되지 않은" 모델만 조회합니다. 직접 글로벌 스코프를 정의해 전역 쿼리 조건을 쉽게 관리할 수 있습니다.

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현해야 하며, `apply` 메서드에서 쿼리 빌더에 조건을 추가합니다. 스코프 클래스는 프로젝트 내 원하는 위치에 자유롭게 배치하세요:

```
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 스코프를 Eloquent 쿼리 빌더에 적용
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

> [!NOTE]
> 스코프가 쿼리의 select 절에 컬럼을 추가할 때는, 기존 선택절을 덮어쓰지 않도록 반드시 `addSelect` 메서드를 사용하세요.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

스코프를 모델에 적용하려면 모델의 `booted` 메서드를 오버라이드해 `addGlobalScope`에 스코프 인스턴스를 넘깁니다:

```
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     *
     * @return void
     */
    protected static function booted()
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위처럼 `AncientScope`를 추가하면 `User::all()` 호출 시 다음 SQL이 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

간단한 조건일 경우 별도 클래스 없이 클로저를 써서 글로벌 스코프를 정의할 수도 있습니다. 첫번째 인자로 스코프 이름을 지정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
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
#### 글로벌 스코프 제거

특정 쿼리에서 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용합니다. 스코프 클래스 이름 또는 클로저 지정 시 쓴 문자열 이름을 인자로 줍니다:

```
User::withoutGlobalScope(AncientScope::class)->get();
```

익명 스코프일 경우:

```
User::withoutGlobalScope('ancient')->get();
```

여러 스코프 또는 전체 스코프를 제거하려면 `withoutGlobalScopes`를 쓰세요:

```
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프 (Local Scopes)

로컬 스코프는 자주 쓰는 쿼리 조건을 재사용하기 쉽게 메서드로 정의하는 방법입니다. 메서드 이름 앞에 `scope` 접두사를 붙이고 첫 번째 매개변수로 쿼리 빌더를 받으세요.

스코프 메서드는 항상 쿼리 빌더 인스턴스를 반환하거나 `void`여야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 많은 사용자만 포함하는 쿼리 스코프
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopePopular($query)
    {
        return $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 포함하는 스코프
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
#### 로컬 스코프 사용

정의한 후에는 `scope` 접두사 없이 호출합니다. 여러 스코프는 체이닝도 가능합니다:

```
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 조건과 함께 사용해야 한다면 클로저를 써서 논리 그룹핑을 해야 올바른 쿼리가 만들어집니다:

```
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

더 편리하게 하려면, Laravel은 고차 함수 스타일 `orWhere`를 지원하여 클로저 없이 체인 가능하게 합니다:

```
$users = App\Models\User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 파라미터가 있는 동적 스코프

스코프에 인수가 필요하면, 첫 매개변수 `$query` 뒤에 추가로 선언하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 유형 사용자만 포함하는 스코프
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

호출 시 인자를 전달합니다:

```
$users = User::ofType('admin')->get();
```

<a name="comparing-models"></a>
## 모델 비교하기 (Comparing Models)

두 모델이 같은지 여부는 `is`와 `isNot` 메서드로 쉽게 확인할 수 있습니다. 두 모델의 기본 키, 테이블, DB 연결이 모두 같은지 비교합니다:

```
if ($post->is($anotherPost)) {
    //
}

if ($post->isNot($anotherPost)) {
    //
}
```

`belongsTo`, `hasOne`, `morphTo`, `morphOne` 등의 관계에서도 사용할 수 있어, 관계된 모델을 다시 조회하지 않고도 비교 가능해 유용합니다:

```
if ($post->author()->is($user)) {
    //
}
```

<a name="events"></a>
## 이벤트 (Events)

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션으로 직접 브로드캐스트하려면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/9.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 다음과 같은 생명주기 지점에서 이벤트를 발생시켜 개발자가 개입할 수 있게 합니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- 모델이 기존 데이터베이스에서 조회되면 `retrieved` 이벤트가 발생합니다.
- 새 모델을 처음 저장할 때 `creating` 및 `created` 이벤트가 발생합니다.
- 기존 모델을 갱신하면 `updating` / `updated` 이벤트가 발생합니다.
- 모델을 생성하거나 갱신할 때는 `saving` / `saved` 이벤트가 발생합니다(속성이 바뀌지 않아도 발생). `-ing`로 끝나는 이벤트는 데이터베이스 변경 전, `-ed`로 끝나는 이벤트는 변경 후입니다.

모델 이벤트를 수신하려면, 모델에 `$dispatchesEvents` 배열 속성을 정의해 이벤트 클래스와 매핑합니다. 각 이벤트 클래스는 영향을 받은 모델 인스턴스를 생성자에서 받습니다:

```
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
     * 모델 이벤트와 사용자 이벤트 클래스 매핑
     *
     * @var array
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

이후 [이벤트 리스너](/docs/9.x/events#defining-listeners)를 작성해 이벤트를 처리합니다.

> [!WARNING]
> 대량 갱신이나 삭제 쿼리를 실행할 때 `saved`, `updated`, `deleting`, `deleted` 같은 모델 이벤트는 전파되지 않습니다. 실제 모델을 로드하지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 이벤트 사용하기

커스텀 이벤트 클래스 대신, 클로저를 등록할 수도 있습니다. 주로 모델의 `booted` 메서드에서 만듭니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
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

필요하면 [큐 처리 가능한 익명 이벤트 리스너](/docs/9.x/events#queuable-anonymous-event-listeners)로 배경 작업 실행을 지정할 수도 있습니다:

```
use function Illuminate\Events\queueable;

static::created(queueable(function ($user) {
    //
}));
```

<a name="observers"></a>
### 옵저버 (Observers)

<a name="defining-observers"></a>
#### 옵저버 정의

많은 이벤트를 듣는다면 옵저버 클래스로 묶어 관리하는 것이 편리합니다. 옵저버는 메서드 이름이 이벤트 이름과 대응되며, 각 메서드는 영향을 받는 모델 인스턴스를 매개변수로 받습니다. `make:observer` Artisan 명령어로 쉽게 생성 가능합니다:

```shell
php artisan make:observer UserObserver --model=User
```

생성된 옵저버는 기본적으로 `app/Observers` 디렉터리에 위치하며, 다음과 비슷합니다:

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User 모델의 "created" 이벤트 처리
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function created(User $user)
    {
        //
    }

    /**
     * User 모델의 "updated" 이벤트 처리
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function updated(User $user)
    {
        //
    }

    /**
     * User 모델의 "deleted" 이벤트 처리
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function deleted(User $user)
    {
        //
    }
    
    /**
     * User 모델의 "restored" 이벤트 처리
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function restored(User $user)
    {
        //
    }

    /**
     * User 모델의 "forceDeleted" 이벤트 처리
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

옵저버 등록은 `App\Providers\EventServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 모델에 `observe` 메서드를 호출해 합니다:

```
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 이벤트 등록
 *
 * @return void
 */
public function boot()
{
    User::observe(UserObserver::class);
}
```

또는, `App\Providers\EventServiceProvider` 클래스의 `$observers` 배열 속성으로 지정할 수도 있습니다:

```
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 모델 옵저버 목록
 *
 * @var array
 */
protected $observers = [
    User::class => [UserObserver::class],
];
```

> [!NOTE]
> 옵저버는 `saving`, `retrieved` 같은 추가 이벤트도 처리할 수 있습니다. 자세한 내용은 [이벤트 문서](#events)를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

트랜잭션 내에서 모델이 생성될 경우, 트랜잭션 커밋 후에만 옵저버 이벤트 핸들러가 실행되도록 하려면 옵저버 클래스에 `$afterCommit` 속성을 `true`로 정의하세요. 트랜잭션이 없으면 즉시 실행됩니다:

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * 모든 트랜잭션 종료 후 이벤트 처리 여부
     *
     * @var bool
     */
    public $afterCommit = true;

    /**
     * User 모델의 "created" 이벤트 처리
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
### 이벤트 비활성화 (Muting Events)

일시적으로 모델이 발생시키는 이벤트를 모두 비활성화하고 싶다면, `withoutEvents` 메서드에 클로저를 넘겨 실행하세요. 클로저 내의 작업은 이벤트를 발생시키지 않으며, 클로저 반환값이 `withoutEvents` 반환값이 됩니다:

```
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장하기

특정 모델을 저장하되 이벤트를 발생시키지 않으려면, `saveQuietly` 메서드를 사용하세요:

```
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이외에도 `update`, `delete`, `soft delete`, `restore`, `replicate`를 이벤트 없이 실행하는 메서드들이 있습니다:

```
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```