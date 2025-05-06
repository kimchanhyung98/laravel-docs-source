# Eloquent: 시작하기

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [Lazy 컬렉션을 사용한 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [대량 할당](#mass-assignment)
    - [Upsert](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 가지치기](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [Pending 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 Eloquent라는 객체 관계 매퍼(ORM)를 포함하고 있어 데이터베이스와의 상호작용을 즐겁게 만들어 줍니다. Eloquent를 사용하면 각 데이터베이스 테이블에는 해당 테이블과 상호작용을 담당하는 "모델"이 대응됩니다. 데이터베이스 테이블로부터 레코드를 조회할 뿐만 아니라, Eloquent 모델을 사용하여 테이블에 레코드를 삽입, 수정, 삭제할 수도 있습니다.

> [!NOTE]  
> 시작하기 전에 애플리케이션의 `config/database.php` 환경설정 파일에서 데이터베이스 연결을 반드시 구성하세요. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/{{version}}/database#configuration)를 참고하세요.

#### Laravel 부트캠프

Laravel를 처음 접한다면, [Laravel 부트캠프](https://bootcamp.laravel.com)에 참여해 보세요. 부트캠프는 Eloquent를 사용하여 첫 Laravel 애플리케이션을 만드는 과정을 안내합니다. Laravel과 Eloquent의 모든 기능을 둘러볼 수 있는 좋은 방법입니다.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

Eloquent 모델을 만들면서 시작해봅시다. 모델은 보통 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하세요:

```shell
php artisan make:model Flight
```

모델 생성 시 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 유형의 클래스를 함께 생성할 수 있습니다. 아래와 같이 옵션을 조합해 한 번에 여러 클래스를 생성할 수 있습니다:

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

# 모델, FlightController 리소스 클래스 및 폼 요청 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청 생성(단축키)...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗(pivot) 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

모델의 코드만 훑어봐서는 어떤 속성과 관계가 있는지 파악하기 어려울 때가 있습니다. 이럴 때는 모델의 모든 속성과 관계를 한눈에 볼 수 있는 `model:show` Artisan 명령어를 사용해보세요:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치하게 됩니다. 간단한 모델 클래스를 예로 Eloquent의 주요 관례를 살펴봅시다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        // ...
    }

<a name="table-names"></a>
### 테이블 이름

위 예제를 보면, `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 지정하지 않았음을 알 수 있습니다. 관례에 따라, 클래스 이름을 스네이크케이스 복수형으로 변환한 이름이 테이블 이름으로 사용됩니다. 따라서 이 경우 Eloquent는 `Flight` 모델이 `flights` 테이블에 레코드를 저장한다고 가정합니다. 만약 `AirTrafficController`라는 모델이 있다면, 테이블 이름은 `air_traffic_controllers`가 됩니다.

모델의 실제 데이터베이스 테이블 이름이 이 관례를 따르지 않는다면, 모델에 `table` 속성을 선언하여 테이블 이름을 직접 지정할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 모델이 연관된 테이블.
         *
         * @var string
         */
        protected $table = 'my_flights';
    }

<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델의 연결 테이블에 기본 키로 `id` 컬럼이 있다고 가정합니다. 다른 기본 키 컬럼을 사용하고 싶다면, 모델에 `$primaryKey` 보호 속성을 선언하여 지정할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 테이블의 기본 키.
         *
         * @var string
         */
        protected $primaryKey = 'flight_id';
    }

또한 Eloquent는 기본 키가 자동 증가하는 정수 값일 것이라고 가정합니다. 만약 자동 증가하지 않는 값이나 숫자가 아닌 기본 키를 사용하려면, 모델에서 공개 속성 `$incrementing`을 `false`로 설정해야 합니다:

    <?php

    class Flight extends Model
    {
        /**
         * 모델의 ID가 자동 증가하는지 여부.
         *
         * @var bool
         */
        public $incrementing = false;
    }

기본 키가 정수가 아니라면, `$keyType` 보호 속성을 `string`으로 지정 해야 합니다:

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

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent는 각 모델에 최소 한 개의 고유 "ID"(기본 키)가 있어야 합니다. Eloquent 모델에서는 "복합" 기본 키를 지원하지 않습니다. 하지만 하나의 고유 기본 키 외에 여러 컬럼에 대한 추가 고유 인덱스를 데이터베이스 테이블에 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자 길이의 전역적으로 유일한 영숫자 식별자입니다.

모델에서 자동 증가 정수 대신 UUID 키를 사용하려면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용하세요. 물론 모델에 [UUID 기본 키 컬럼](/docs/{{version}}/migrations#column-method-uuid)을 추가해야 합니다.

    use Illuminate\Database\Eloquent\Concerns\HasUuids;
    use Illuminate\Database\Eloquent\Model;

    class Article extends Model
    {
        use HasUuids;

        // ...
    }

    $article = Article::create(['title' => 'Traveling to Europe']);

    $article->id; // "8f8e8478-9035-4d23-b9a7-62f4d2612ce5"

기본적으로 `HasUuids` 트레이트는 모델에 ["정렬 가능한" UUID](/docs/{{version}}/strings#method-str-ordered-uuid)를 생성합니다. 이러한 UUID는 사전순으로 정렬이 가능해 인덱싱된 데이터베이스 저장에 더 효율적입니다.

특정 모델에서 UUID 생성 방식을 직접 오버라이드하려면 모델에 `newUniqueId` 메서드를 정의하세요. 또한 어떤 컬럼에 UUID를 할당할지 지정하고 싶으면 `uniqueIds` 메서드를 정의합니다:

    use Ramsey\Uuid\Uuid;

    /**
     * 모델의 새 UUID 생성
     */
    public function newUniqueId(): string
    {
        return (string) Uuid::uuid4();
    }

    /**
     * 고유 식별자를 받아야 하는 컬럼을 반환
     *
     * @return array<int, string>
     */
    public function uniqueIds(): array
    {
        return ['id', 'discount_code'];
    }

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 26자로, UUID와 비슷하지만 더 짧으며, 역시 효율적인 인덱싱을 위해 사전순 정렬이 가능합니다. ULID를 사용하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 사용하세요. 모델에 [ULID 타입의 기본 키 컬럼](/docs/{{version}}/migrations#column-method-ulid)이 있어야 합니다:

    use Illuminate\Database\Eloquent\Concerns\HasUlids;
    use Illuminate\Database\Eloquent\Model;

    class Article extends Model
    {
        use HasUlids;

        // ...
    }

    $article = Article::create(['title' => 'Traveling to Asia']);

    $article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"

<a name="timestamps"></a>
### 타임스탬프

기본적으로 Eloquent는 모델이 연관된 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 가정합니다. 모델이 생성되거나 수정되면 Eloquent가 자동으로 이 컬럼 값을 설정합니다. 자동으로 타임스탬프를 관리하지 않으려면 모델의 `$timestamps` 속성 값을 `false`로 지정하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 모델에서 타임스탬프를 사용할지 여부.
         *
         * @var bool
         */
        public $timestamps = false;
    }

모델의 타임스탬프 포맷을 커스터마이즈하려면 `$dateFormat` 속성에 저장 방식을 지정하세요. 이 속성은 데이터베이스에 값이 저장되는 방식과, 배열 또는 JSON으로 직렬화될 때의 포맷을 결정합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 모델 날짜 컬럼의 저장 포맷.
         *
         * @var string
         */
        protected $dateFormat = 'U';
    }

타임스탬프 컬럼의 이름을 변경하려면 모델에 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의합니다:

    <?php

    class Flight extends Model
    {
        const CREATED_AT = 'creation_date';
        const UPDATED_AT = 'updated_date';
    }

모델의 `updated_at` 타임스탬프 수정 없이 작업을 수행하려면, `withoutTimestamps` 메서드로 클로저를 감싸 사용합니다:

    Model::withoutTimestamps(fn () => $post->increment('reads'));

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션의 기본 데이터베이스 연결을 사용합니다. 특정 모델에서 사용할 데이터베이스 연결을 지정하려면 `$connection` 속성을 정의하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 모델이 사용할 데이터베이스 연결명.
         *
         * @var string
         */
        protected $connection = 'mysql';
    }

<a name="default-attribute-values"></a>
### 기본 속성 값

새로 인스턴스화한 모델 객체는 기본적으로 어떠한 속성 값도 갖지 않습니다. 일부 속성에 대한 기본값을 정의하려면 모델의 `$attributes` 속성을 활용하세요. `$attributes` 배열에 선언한 값은 데이터베이스에서 막 읽힌 값 처럼 "원시 값" 형태여야 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 모델의 기본 속성 값.
         *
         * @var array
         */
        protected $attributes = [
            'options' => '[]',
            'delayed' => false,
        ];
    }

<a name="configuring-eloquent-strictness"></a>
### Eloquent 엄격성 설정

Laravel에서는 다양한 상황에서 Eloquent의 동작 및 "엄격성"을 설정할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 lazy loading(지연 로딩)을 방지할지 여부를 결정하는 불리언 인수를 받습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다:

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

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출해 할당할 수 없는 속성을 채우려고 할 때 Laravel이 예외를 던지도록 할 수 있습니다. 이는 모델의 `fillable` 배열에 없는 속성을 할당 시, 개발 환경에서 혼란을 방지하는 데 도움이 됩니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회

모델과 [해당 데이터베이스 테이블](/docs/{{version}}/migrations#generating-migrations)이 준비되었다면, 데이터베이스에서 데이터를 조회할 수 있습니다. 각 Eloquent 모델은 강력한 [쿼리 빌더](/docs/{{version}}/queries)와 같아서, 모델에 연결된 테이블을 유연하게 조회할 수 있습니다. 모델의 `all` 메서드는 해당 테이블의 모든 레코드를 조회합니다:

    use App\Models\Flight;

    foreach (Flight::all() as $flight) {
        echo $flight->name;
    }

<a name="building-queries"></a>
#### 쿼리 빌드

Eloquent의 `all` 메서드는 모델 테이블의 모든 결과를 반환합니다. Eloquent 모델은 [쿼리 빌더](/docs/{{version}}/queries)이므로, 쿼리에 제약을 추가한 뒤 `get` 메서드로 결과를 가져올 수도 있습니다:

    $flights = Flight::where('active', 1)
        ->orderBy('name')
        ->take(10)
        ->get();

> [!NOTE]  
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더](/docs/{{version}}/queries)에서 제공하는 모든 메서드를 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 갱신

데이터베이스에서 조회한 Eloquent 모델 인스턴스를 이미 가지고 있다면, `fresh` 및 `refresh` 메서드로 모델을 "새로고침"할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 가져오며, 기존 인스턴스는 변하지 않습니다:

    $flight = Flight::where('number', 'FR 900')->first();

    $freshFlight = $flight->fresh();

`refresh` 메서드는 기존 모델 인스턴스를 데이터베이스의 최신 데이터로 다시 채워줍니다. 또한, 로드된 관계들도 모두 갱신됩니다:

    $flight = Flight::where('number', 'FR 900')->first();

    $flight->number = 'FR 456';

    $flight->refresh();

    $flight->number; // "FR 900"

<a name="collections"></a>
### 컬렉션

앞서 보았듯, Eloquent의 `all` 및 `get`과 같은 메서드는 데이터베이스에서 여러 레코드를 조회합니다. 하지만 이들은 일반 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 컬렉션 클래스인 `Illuminate\Support\Collection`을 확장한 것으로, 컬렉션을 다루기 위한 [다양한 편리한 메서드](/docs/{{version}}/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 클로저의 결과에 따라 컬렉션에서 모델을 제외할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel의 기본 컬렉션에 있는 메서드 이외에도, Eloquent 컬렉션 클래스에는 [Eloquent 모델 컬렉션에 특화된 몇 가지 추가 메서드](/docs/{{version}}/eloquent-collections#available-methods)도 있습니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로 배열처럼 루프를 돌릴 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

`all` 또는 `get` 메서드로 수만 개의 Eloquent 레코드를 한 번에 로드하려고 하면 메모리 부족이 발생할 수 있습니다. 이런 경우에는 `chunk` 메서드를 사용해 보다 효율적으로 다량의 모델을 처리할 수 있습니다.

`chunk` 메서드는 Eloquent 모델의 일부를 가져와 클로저로 전달해줍니다. 한 번에 현재 청크만 메모리에 올라가기 때문에 대량의 데이터를 다루기에도 메모리 사용량이 급격히 줄어듭니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk`의 첫 번째 인수는 "청크"당 가져올 레코드 수입니다. 두 번째 인수로 전달된 클로저는 데이터베이스에서 각 청크가 조회될 때마다 호출됩니다.

결과를 반복하며 특정 컬럼의 값을 업데이트해야 한다면 `chunkById` 메서드를 사용하는 것이 좋습니다. `chunkById`는 내부적으로 이전 청크의 마지막 레코드의 `id` 값보다 큰 값만을 가져오기 때문에, 보다 일관된 결과를 얻을 수 있습니다:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById`는 내부적으로 쿼리에 별도의 "where" 조건을 추가하므로, 자체적인 조건을 [클로저로 논리 묶음](https://laravel.kr/docs/{{version}}/queries#logical-grouping)으로 작성하는 것이 좋습니다:

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
### Lazy 컬렉션을 사용한 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 동작하지만, 각 청크를 바로 콜백으로 넘기지 않고 펼쳐진 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)을 반환하여 결과를 하나의 스트림처럼 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 방식으로 필터링하는 경우, 결과를 업데이트할 컬럼 기준으로 반복 처리해야 한다면 `lazyById` 메서드를 사용하세요. 이 경우에도 이전 청크 마지막 모델의 `id`보다 큰 레코드만 내부적으로 계속 조회합니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`id`의 내림차순으로 결과를 필터링하려면 `lazyByIdDesc` 메서드를 사용할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드와 마찬가지로, `cursor` 메서드는 수만 개가 넘는 Eloquent 모델을 반복할 때 애플리케이션의 메모리 소모를 크게 줄여줍니다.

`cursor` 메서드는 단 하나의 데이터베이스 쿼리만 실행하며, 실제로 반복될 때마다 Eloquent 모델을 한 개씩만 메모리에 로드합니다.

> [!WARNING]  
> `cursor` 메서드는 한 번에 하나의 Eloquent 모델만 메모리에 유지하므로, 관계를 eager load(선로드)할 수 없습니다. 관계가 필요하다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하는 것이 좋습니다.

내부적으로 `cursor`는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/{{version}}/collections#lazy-collections)은 일반 Laravel 컬렉션의 여러 메서드를, 한 번에 하나의 모델만 메모리에 올리면서 사용할 수 있게 해줍니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor`는 메모리 사용량이 적지만, 결국 어느 지점에선 메모리가 부족할 수 있습니다. 이는 [PHP의 PDO 드라이버가 쿼리 결과를 내부적으로 버퍼링하기 때문](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 수십만 개 이상의 모델을 다룬다면 [`lazy` 메서드](#chunking-using-lazy-collections) 사용을 권장합니다.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent에서는 관계된 테이블에서 정보를 한 번의 쿼리로 추출할 수 있는 고급 서브쿼리를 지원합니다. 예를 들어, `destinations` 테이블과 그 목적지로 향하는 `flights` 테이블이 있을 때, 각 목적지별로 가장 최근에 도착한 항공편의 이름을 아래와 같이 조회할 수 있습니다:

    use App\Models\Destination;
    use App\Models\Flight;

    return Destination::addSelect(['last_flight' => Flight::select('name')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
    ])->get();

<a name="subquery-ordering"></a>
#### 서브쿼리 정렬

쿼리 빌더의 `orderBy`에서도 서브쿼리를 사용할 수 있습니다. 예를 들어, 목적지별 최신 도착 항공편 시간으로 목적지 정렬이 가능합니다:

    return Destination::orderByDesc(
        Flight::select('arrived_at')
            ->whereColumn('destination_id', 'destinations.id')
            ->orderByDesc('arrived_at')
            ->limit(1)
    )->get();

<a name="retrieving-single-models"></a>
## 단일 모델/집계 조회

특정 조건에 일치하는 모든 레코드를 조회하는 것 외에, `find`, `first`, 혹은 `firstWhere` 메서드로 단일 레코드만 조회할 수도 있습니다. 이들 메서드는 모델 컬렉션이 아니라 단일 모델 인스턴스를 반환합니다:

    use App\Models\Flight;

    // 기본 키로 모델 조회
    $flight = Flight::find(1);

    // 쿼리 제약 조건에 맞는 첫 번째 모델 조회
    $flight = Flight::where('active', 1)->first();

    // 위와 동일하지만 more concise
    $flight = Flight::firstWhere('active', 1);

결과가 없을 경우 클로저를 실행하고 싶다면 `findOr` 및 `firstOr` 메서드를 사용할 수 있습니다. 클로저의 반환값이 최종 결과로 간주됩니다:

    $flight = Flight::findOr(1, function () {
        // ...
    });

    $flight = Flight::where('legs', '>', 3)->firstOr(function () {
        // ...
    });

<a name="not-found-exceptions"></a>
#### Not Found 예외 처리

모델을 찾지 못할 경우 예외를 던지고 싶을 때가 있습니다. 특히 라우트나 컨트롤러에서 유용합니다. `findOrFail`, `firstOrFail`은 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

    $flight = Flight::findOrFail(1);

    $flight = Flight::where('legs', '>', 3)->firstOrFail();

예외가 잡히지 않으면 클라이언트에 404 HTTP 응답이 자동으로 전송됩니다:

    use App\Models\Flight;

    Route::get('/api/flights/{id}', function (string $id) {
        return Flight::findOrFail($id);
    });

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 지정한 컬럼/값 쌍으로 DB 레코드를 찾습니다. 데이터베이스에 해당 값이 없으면 두 번째 배열 인자와 병합한 값으로 새 레코드를 삽입합니다.

`firstOrNew` 메서드 역시 지정한 조건에 맞는 레코드를 찾으려 시도하지만, 찾지 못하면 새 모델 인스턴스를 반환합니다. 이 인스턴스는 아직 DB에 저장되지 않았으므로, 직접 `save`를 호출해야 합니다:

    use App\Models\Flight;

    // 이름으로 조회 또는 없으면 생성
    $flight = Flight::firstOrCreate([
        'name' => 'London to Paris'
    ]);

    // 이름으로 조회 또는 다른 속성까지 포함해서 생성
    $flight = Flight::firstOrCreate(
        ['name' => 'London to Paris'],
        ['delayed' => 1, 'arrival_time' => '11:30']
    );

    // 이름으로 조회 또는 새 객체 인스턴스 반환(저장 안 함)
    $flight = Flight::firstOrNew([
        'name' => 'London to Paris'
    ]);

    // 이름으로 조회 또는 인스턴스 + 속성까지 포함해 반환
    $flight = Flight::firstOrNew(
        ['name' => 'Tokyo to Sydney'],
        ['delayed' => 1, 'arrival_time' => '11:30']
    );

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent 모델을 다룰 때도 Laravel [쿼리 빌더](/docs/{{version}}/queries)가 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/{{version}}/queries#aggregates)를 사용할 수 있습니다. 이러한 메서드는 Eloquent 모델 인스턴스 대신 스칼라 값을 반환합니다:

    $count = Flight::where('active', 1)->count();

    $max = Flight::where('active', 1)->max('price');

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때, 모델 조회뿐 아니라 새로운 레코드 삽입도 손쉽게 처리할 수 있습니다. DB에 새 레코드를 삽입하려면 모델 인스턴스를 생성하고, 속성을 설정한 뒤, `save` 메서드를 호출하세요:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\Flight;
    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class FlightController extends Controller
    {
        /**
         * 새 항공편 정보를 데이터베이스에 저장
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

이 예제에서는 HTTP 요청에서 `name` 필드를 받아, `App\Models\Flight` 모델 인스턴스의 `name`에 할당합니다. `save` 메서드 호출 시 레코드가 테이블에 삽입되며, Eloquent는 `created_at` 및 `updated_at` 타임스탬프를 자동으로 설정합니다. 직접 설정할 필요는 없습니다.

또는, `create` 메서드를 이용하면 한 번의 구문으로 새 모델을 "저장"할 수 있습니다. 이때 삽입된 모델 인스턴스가 반환됩니다:

    use App\Models\Flight;

    $flight = Flight::create([
        'name' => 'London to Paris',
    ]);

단, `create` 메서드를 사용하려면 모델에 `fillable` 또는 `guarded` 속성 중 하나를 지정해야 합니다. 기본적으로 모든 Eloquent 모델은 대량 할당의 위험으로부터 보호되기 때문입니다. 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 수정

이미 존재하는 모델도 `save` 메서드로 수정할 수 있습니다. 모델을 조회한 후 원하는 속성을 변경하여 `save`를 호출하세요. `updated_at` 타임스탬프도 자동으로 업데이트됩니다:

    use App\Models\Flight;

    $flight = Flight::find(1);

    $flight->name = 'Paris to London';

    $flight->save();

경우에 따라, 기존 모델을 수정하거나 없다면 새로 생성하고 싶을 수 있습니다. `updateOrCreate` 메서드는 `firstOrCreate`와 유사하게 동작하며, 일치하는 모델이 있다면 수정하고, 없으면 생성합니다:

    $flight = Flight::updateOrCreate(
        ['departure' => 'Oakland', 'destination' => 'San Diego'],
        ['price' => 99, 'discounted' => 1]
    );

<a name="mass-updates"></a>
#### 대량 수정

지정한 쿼리에 일치하는 모델을 한꺼번에 수정할 수도 있습니다. 아래 예제에서는 `active`이고 `destination`이 'San Diego'인 항공편을 모두 지연됨(delayed) 상태로 마킹합니다:

    Flight::where('active', 1)
        ->where('destination', 'San Diego')
        ->update(['delayed' => 1]);

`update` 메서드는 수정할 컬럼-값 쌍의 배열을 기대하며, 수정된 레코드 수를 반환합니다.

> [!WARNING]  
> Eloquent의 대량 수정(mass update) 시, `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 이 경우 모델 인스턴스를 조회하지 않고 바로 업데이트하기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변화 감지

Eloquent에는 모델이 원래 조회된 후 내부 속성 상태가 어떻게 변경되었는지 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드가 있습니다.

`isDirty`는 모델의 속성 중 변경된 것이 있는지 확인합니다. 속성명을 하나 또는 배열로 넘겨 해당 속성이 "dirty"한지 체크할 수 있습니다. `isClean`은 해당 속성이 조회 이후 변하지 않았는지 확인합니다:

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

`wasChanged`는 모델이 최근 저장될 때 어떤 속성이 변경되었는지 확인합니다:

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

`getOriginal`은 조회 당시 원본 속성을 배열로 반환합니다. 특정 속성의 원래 값을 알고 싶다면 속성명을 넘기면 됩니다:

    $user = User::find(1);

    $user->name; // John
    $user->email; // john@example.com

    $user->name = "Jack";
    $user->name; // Jack

    $user->getOriginal('name'); // John
    $user->getOriginal(); // 원본 속성 배열...

<a name="mass-assignment"></a>
### 대량 할당

`create` 메서드를 사용하면 하나의 PHP 문장으로 새 모델을 "저장"할 수 있습니다. 결과로 삽입된 모델 인스턴스가 반환됩니다:

    use App\Models\Flight;

    $flight = Flight::create([
        'name' => 'London to Paris',
    ]);

단, 이 메서드 사용 전 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나를 정의해야 합니다. 이는 모든 Eloquent 모델이 대량 할당 취약점으로부터 기본적으로 보호되기 때문입니다.

대량 할당 취약점은 사용자가 예기치 않은 HTTP 요청 필드를 보내고, 이것이 DB의 허용되지 않은 컬럼 값을 변경할 수 있을 때 발생합니다. 예를 들어, 악의적인 사용자가 `is_admin` 파라미터를 전달하여 관리자로 자신의 권한을 올릴 수 있게 될 수도 있습니다.

따라서 우선, 어떤 속성을 대량 할당 가능하게 만들지 `$fillable` 속성에 정의해야 합니다. 예를 들어 `name` 속성을 mass assignable로 만들려면:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 대량 할당 가능한 속성.
         *
         * @var array<int, string>
         */
        protected $fillable = ['name'];
    }

지정한 속성은 이제 `create` 메서드로 DB에 안전하게 삽입할 수 있습니다:

    $flight = Flight::create(['name' => 'London to Paris']);

이미 모델 인스턴스가 있다면, `fill` 메서드로 여러 속성을 한 번에 할당할 수도 있습니다:

    $flight->fill(['name' => 'Amsterdam to Frankfurt']);

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 대량 할당할 때는, 각 컬럼의 키를 `$fillable` 배열에 각각 지정해야 합니다. 보안상, Laravel은 `guarded`를 사용할 때 중첩된 JSON 속성 업데이트를 지원하지 않습니다:

    /**
     * 대량 할당 가능한 속성.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'options->enabled',
    ];

<a name="allowing-mass-assignment"></a>
#### 전체 대량 할당 허용

모든 속성을 대량 할당 가능하게 하려면 `$guarded`를 빈 배열로 지정하면 됩니다. 이 경우, Eloquent의 `fill`, `create`, `update`에 넘길 배열은 반드시 직접 안전하게 구성해야 합니다:

    /**
     * 대량 할당을 금지하는 속성.
     *
     * @var array<string>|bool
     */
    protected $guarded = [];

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로 `$fillable`에 없는 속성은 대량 할당 시 자동으로 무시됩니다. 실서비스에서는 합리적이지만, 개발 과정에서는 왜 속성 값이 반영되지 않는지 혼란스러울 수 있습니다.

필요하다면, 할당할 수 없는 속성을 대량 할당할 때 예외를 던지도록 `preventSilentlyDiscardingAttributes`를 사용할 수 있습니다. 보통 `AppServiceProvider`의 `boot`에서 등록합니다:

    use Illuminate\Database\Eloquent\Model;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
    }

<a name="upserts"></a>
### Upsert

Eloquent의 `upsert` 메서드는 여러 레코드를 한 번에 원자적(atomic)으로 삽입 혹은 수정할 수 있게 해줍니다. 첫 번째 인수는 삽입 또는 수정할 값 목록, 두 번째 인수는 레코드를 고유하게 식별하는 컬럼, 세 번째 인수는 기존 레코드가 있을 때 수정할 컬럼 리스트입니다. 타임스탬프가 활성화 되어 있다면, `created_at`과 `updated_at` 값도 자동으로 갱신됩니다:

    Flight::upsert([
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ], uniqueBy: ['departure', 'destination'], update: ['price']);

> [!WARNING]  
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 두 번째 인수의 컬럼이 "primary" 또는 "unique" 인덱스를 가져야 합니다. MariaDB, MySQL 드라이버는 두 번째 인수를 무시하고 테이블의 primary/unique 인덱스만 사용합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면 인스턴스에서 `delete` 메서드를 호출하면 됩니다:

    use App\Models\Flight;

    $flight = Flight::find(1);

    $flight->delete();

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 모델 삭제

위 예제는 모델을 조회한 뒤 `delete`를 호출했습니다. 기본 키를 알고 있다면 `destroy` 메서드로 조회 없이 바로 삭제할 수 있습니다. 단일 기본 키, 여러 키, 배열, [컬렉션](/docs/{{version}}/collections) 형태 모두 지원합니다:

    Flight::destroy(1);

    Flight::destroy(1, 2, 3);

    Flight::destroy([1, 2, 3]);

    Flight::destroy(collect([1, 2, 3]));

[소프트 삭제 모델](#soft-deleting) 사용 시, 영구 삭제를 하려면 `forceDestroy` 메서드를 사용하세요:

    Flight::forceDestroy(1);

> [!WARNING]  
> `destroy` 메서드는 각 모델을 개별적으로 로드 후 `delete`를 호출하므로, 각 모델별로 `deleting` 및 `deleted` 이벤트가 정상적으로 발생합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

쿼리를 사용하여 조건에 맞는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래 예제는 `active`가 0인 비활성 항공편을 모두 삭제합니다. 대량 삭제 역시 삭제된 모델에 대해서는 이벤트가 발생하지 않습니다:

    $deleted = Flight::where('active', 0)->delete();

테이블에 있는 전체 모델을 삭제하려면 조건 없이 쿼리를 실행하세요:

    $deleted = Flight::query()->delete();

> [!WARNING]  
> Eloquent에서 대량 삭제를 실행할 때 `deleting`, `deleted` 모델 이벤트는 트리거되지 않습니다. 모델을 실제로 조회하지 않고 바로 삭제 명령을 내리기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 실제로 레코드를 삭제하지 않고 "소프트 삭제"하는 기능도 제공합니다. 소프트 삭제 되면 데이터베이스에서 삭제되는 대신, 모델의 `deleted_at` 속성에 삭제된 시각이 기록됩니다. 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\SoftDeletes;

    class Flight extends Model
    {
        use SoftDeletes;
    }

> [!NOTE]  
> `SoftDeletes` 트레이트는 자동으로 `deleted_at` 속성을 `DateTime` 또는 `Carbon` 인스턴스 형 변환해 줍니다.

테이블에도 `deleted_at` 컬럼이 추가되어야 합니다. Laravel [스키마 빌더](/docs/{{version}}/migrations)는 이를 쉽게 생성하는 메서드를 제공합니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('flights', function (Blueprint $table) {
        $table->softDeletes();
    });

    Schema::table('flights', function (Blueprint $table) {
        $table->dropSoftDeletes();
    });

모델에서 `delete`를 호출하면, 실제로 삭제되지 않고 `deleted_at`이 현재 시각으로 설정됩니다. 소프트 삭제가 적용된 모델을 쿼리에서 조회하면 자동으로 제외됩니다.

모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용하세요:

    if ($flight->trashed()) {
        // ...
    }

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 해제

소프트 삭제된 모델을 "복원(un-delete)"할 수도 있습니다. 모델 인스턴스에서 `restore`를 호출하면 `deleted_at`이 `null`로 설정되어 복원됩니다:

    $flight->restore();

쿼리로 여러 모델을 한 번에 복원할 수도 있습니다. 이 역시 대량 복원에서는 이벤트가 발생하지 않습니다:

    Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();

[관계 쿼리](/docs/{{version}}/eloquent-relationships)에서도 `restore`를 사용할 수 있습니다:

    $flight->history()->restore();

<a name="permanently-deleting-models"></a>
#### 영구 삭제

가끔 데이터베이스에서 모델을 완전히 삭제해야 할 때가 있습니다. 이때는 `forceDelete` 메서드를 사용하면 소프트 삭제 모델도 실제로 제거됩니다:

    $flight->forceDelete();

Eloquent 관계 쿼리에서도 사용할 수 있습니다:

    $flight->history()->forceDelete();

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 포함하여 조회

앞서 언급했듯, 소프트 삭제된 모델은 자동으로 쿼리에서 제외됩니다. 그러나 `withTrashed`를 호출하면 쿼리 결과에 소프트 삭제 모델도 포함시킬 수 있습니다:

    use App\Models\Flight;

    $flights = Flight::withTrashed()
        ->where('account_id', 1)
        ->get();

[관계 쿼리](/docs/{{version}}/eloquent-relationships)에서도 사용 가능합니다:

    $flight->history()->withTrashed()->get();

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 모델만 조회

`onlyTrashed`는 오직 소프트 삭제된 모델만 조회합니다:

    $flights = Flight::onlyTrashed()
        ->where('airline_id', 1)
        ->get();

<a name="pruning-models"></a>
## 모델 가지치기

더 이상 필요 없는 모델을 주기적으로 삭제(prune)하고 싶을 때가 있습니다. 이 경우 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하면 됩니다. 이후 필요 없는 모델 쿼리를 반환하는 `prunable` 메서드를 작성하세요:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Prunable;

    class Flight extends Model
    {
        use Prunable;

        /**
         * 가지치기할 모델 쿼리 반환.
         */
        public function prunable(): Builder
        {
            return static::where('created_at', '<=', now()->subMonth());
        }
    }

`Prunable`을 적용한 모델에 대해, 삭제 전에 호출할 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드에서는 해당 모델과 연관된 추가 리소스(예: 저장된 파일 등)를 함께 삭제할 수 있습니다:

    /**
     * 가지치기 전 처리 메서드
     */
    protected function pruning(): void
    {
        // ...
    }

구성한 prunable 모델에 대해, 애플리케이션의 `routes/console.php` 파일에서 `model:prune` Artisan 명령어를 스케줄링하세요:

    use Illuminate\Support\Facades\Schedule;

    Schedule::command('model:prune')->daily();

`model:prune` 명령어는 자동으로 `app/Models` 안에서 "Prunable" 모델을 감지합니다. 다른 위치에 있다면 `--model` 옵션으로 클래스명을 지정해줄 수 있습니다:

    Schedule::command('model:prune', [
        '--model' => [Address::class, Flight::class],
    ])->daily();

특정 모델만 제외하고 가지치기하려면 `--except`를 사용하세요:

    Schedule::command('model:prune', [
        '--except' => [Address::class, Flight::class],
    ])->daily();

계획된 쿼리로 가지치기를 시뮬레이션(pretend) 하고 싶다면, `--pretend` 옵션을 사용합니다:

```shell
php artisan model:prune --pretend
```

> [!WARNING]  
> 소프트 삭제 모델도 쿼리 일치 시 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 가지치기

모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레이트가 적용된 경우, DB에서 실제로 모델을 조회하지 않고 질의문으로 대량 삭제가 이뤄집니다. 이 경우 `pruning` 메서드나 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 삭제 효율이 매우 높아집니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\MassPrunable;

    class Flight extends Model
    {
        use MassPrunable;

        /**
         * 가지치기할 모델 쿼리 반환.
         */
        public function prunable(): Builder
        {
            return static::where('created_at', '<=', now()->subMonth());
        }
    }

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스를 저장하지 않은 채 복사본으로 만들고 싶을 때는 `replicate` 메서드를 사용하세요. 같은 속성을 공유하는 인스턴스가 많을 때 유용합니다:

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

새 모델로 복제 시 제외할 속성이 있다면 `replicate`에 배열로 전달하면 됩니다:

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

<a name="query-scopes"></a>
## 쿼리 스코프

<a name="global-scopes"></a>
### 글로벌 스코프

글로벌 스코프는 특정 모델의 모든 쿼리에 제약을 추가하고 싶을 때 사용합니다. Laravel의 [소프트 삭제](#soft-deleting)도 글로벌 스코프를 활용하여 삭제되지 않은 모델만 조회합니다. 자체 글로벌 스코프를 작성하면 일관되게 제약 조건을 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성

새 글로벌 스코프는 `make:scope` Artisan 명령어로 생성할 수 있습니다. 생성된 스코프 클래스는 `app/Models/Scopes` 디렉터리에 위치하게 됩니다:

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프 작성은 간단합니다. `make:scope` 명령어로 클래스 생성 후 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현합니다. `apply` 메서드에서 쿼리에 필요한 제약을 추가합니다:

    <?php

    namespace App\Models\Scopes;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Scope;

    class AncientScope implements Scope
    {
        /**
         * 해당 스코프를 Eloquent 쿼리 빌더에 적용
         */
        public function apply(Builder $builder, Model $model): void
        {
            $builder->where('created_at', '<', now()->subYears(2000));
        }
    }

> [!NOTE]  
> 스코프가 쿼리의 select 절에 컬럼을 추가한다면, 기존 select를 덮어쓰지 않게 하기 위해 `select` 대신 `addSelect`를 사용하세요.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

모델에 글로벌 스코프를 적용하려면 `ScopedBy` 특성(Attribute)을 모델에 지정하세요:

    <?php

    namespace App\Models;

    use App\Models\Scopes\AncientScope;
    use Illuminate\Database\Eloquent\Attributes\ScopedBy;

    #[ScopedBy([AncientScope::class])]
    class User extends Model
    {
        //
    }

또는, 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope`로 직접 등록할 수도 있습니다:

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

이렇게 하면 `User::all()` 호출 시 다음과 같은 SQL 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(클로저) 글로벌 스코프

Eloquent는 클래스를 별도로 정의하지 않고 클로저로 글로벌 스코프를 지정할 수도 있습니다. 이때는 `addGlobalScope`의 첫 번째 인자로 이름을 정하고, 두 번째 인자로 클로저를 넘깁니다:

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

<a name="removing-global-scopes"></a>
#### 글로벌 스코프 제거

특정 쿼리에서 글로벌 스코프를 제거하고 싶으면 `withoutGlobalScope` 메서드를 사용하세요. 인자로 클래스명을 넘깁니다:

    User::withoutGlobalScope(AncientScope::class)->get();

클로저로 정의한 글로벌 스코프라면, 스코프를 지정할 때 쓴 이름(문자열)을 넘기세요:

    User::withoutGlobalScope('ancient')->get();

복수 개 또는 전체 글로벌 스코프를 제거하려면 `withoutGlobalScopes`를 사용하세요:

    // 모든 글로벌 스코프 제거
    User::withoutGlobalScopes()->get();

    // 일부만 제거
    User::withoutGlobalScopes([
        FirstScope::class, SecondScope::class
    ])->get();

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 애플리케이션 전역에서 자주 쓰는 쿼리 제약 묶음을 정의할 수 있게 해줍니다. 예를 들어 "인기 있는" 사용자만 자주 조회해야 할 때 유용합니다. 스코프는 Eloquent 모델 메서드 앞에 `scope`를 접두어로 붙여 정의합니다.

스코프는 항상 동일 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 인기 있는 사용자만 포함
         */
        public function scopePopular(Builder $query): void
        {
            $query->where('votes', '>', 100);
        }

        /**
         * 활성 사용자만 포함
         */
        public function scopeActive(Builder $query): void
        {
            $query->where('active', 1);
        }
    }

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 활용

스코프를 정의한 후, 쿼리 시 해당 메서드를 접두어 `scope` 없이 사용할 수 있습니다. 여러 스코프 체이닝도 가능합니다:

    use App\Models\User;

    $users = User::popular()->active()->orderBy('created_at')->get();

여러 스코프를 논리적으로 묶어(or 조건으로) 사용하려면 클로저를 활용해야 할 수도 있습니다:

    $users = User::popular()->orWhere(function (Builder $query) {
        $query->active();
    })->get();

이 방식을 더 쉽게 하기 위해, Laravel은 "고차" `orWhere` 메서드도 제공합니다:

    $users = User::popular()->orWhere->active()->get();

<a name="dynamic-scopes"></a>
#### 동적 스코프

스코프에 파라미터를 받고 싶으면, 쿼리 파라미터 이후 추가 파라미터를 선언하면 됩니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 주어진 타입의 사용자만 포함
         */
        public function scopeOfType(Builder $query, string $type): void
        {
            $query->where('type', $type);
        }
    }

이제 스코프 사용 시 인자를 넘길 수 있습니다:

    $users = User::ofType('admin')->get();

<a name="pending-attributes"></a>
### Pending 속성

스코프에서 사용된 조건과 동일한 값으로 모델을 생성하려면, 쿼리 생성 시 `withAttributes` 메서드를 사용할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Builder;
    use Illuminate\Database\Eloquent\Model;

    class Post extends Model
    {
        /**
         * 임시글만 포함
         */
        public function scopeDraft(Builder $query): void
        {
            $query->withAttributes([
                'hidden' => true,
            ]);
        }
    }

`withAttributes`는 쿼리에 전달한 속성에 대해 where 제약을 걸고, 나중에 해당 쿼리로 만든 모델에도 동일 속성을 부여합니다:

    $draft = Post::draft()->create(['title' => 'In Progress']);

    $draft->hidden; // true

<a name="comparing-models"></a>
## 모델 비교

두 모델이 동일한지 확인해야 할 때가 있습니다. `is`, `isNot` 메서드로 두 모델이 기본 키, 테이블, DB 연결이 같은지 쉽게 비교할 수 있습니다:

    if ($post->is($anotherPost)) {
        // ...
    }

    if ($post->isNot($anotherPost)) {
        // ...
    }

`is`, `isNot`는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [관계](/docs/{{version}}/eloquent-relationships)에도 제공됩니다. 쿼리를 실행하지 않고 연관 모델을 비교할 때 유용합니다:

    if ($post->author()->is($user)) {
        // ...
    }

<a name="events"></a>
## 이벤트

> [!NOTE]  
> 모델 이벤트를 클라이언트로 브로드캐스트하고 싶다면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/{{version}}/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 트리거하며, 모델 라이프사이클의 다음 순간을 후킹할 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

- `retrieved`: 모델이 DB에서 조회될 때 발생
- `creating`, `created`: 새 모델 저장 전/후 발생
- `updating`, `updated`: 기존 모델 수정 전/후 발생 (`save` 호출 필요)
- `saving`, `saved`: 모델 생성/수정 모두 트리거 (속성 값 변경 여부와 무관)
- `-ing` 접미사는 DB 반영 전, `-ed`는 후

모델 이벤트를 듣기 위해서는 Eloquent 모델에 `$dispatchesEvents` 속성을 정의해서, 다양한 이벤트 지점에 [사용자 이벤트 클래스](/docs/{{version}}/events)를 매핑해야 합니다:

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
         * 모델의 이벤트 맵
         *
         * @var array<string, string>
         */
        protected $dispatchesEvents = [
            'saved' => UserSaved::class,
            'deleted' => UserDeleted::class,
        ];
    }

이벤트 정의 및 매핑 후에는 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)에서 처리할 수 있습니다.

> [!WARNING]  
> Eloquent에서 대량 update/delete 쿼리 실행 시, 해당 모델의 `saved`, `updated`, `deleting`, `deleted` 이벤트가 발생하지 않습니다.

<a name="events-using-closures"></a>
### 클로저 활용

이벤트 클래스 대신 클로저로도 모델 이벤트를 등록할 수 있습니다. 보통 모델의 `booted` 메서드에서 클로저를 등록하세요:

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

필요하다면 [큐 지원 익명 이벤트 리스너](/docs/{{version}}/events#queuable-anonymous-event-listeners)를 활용해, 백그라운드 작업으로도 실행할 수 있습니다:

    use function Illuminate\Events\queueable;

    static::created(queueable(function (User $user) {
        // ...
    }));

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의

한 모델의 여러 이벤트를 감시하려면 옵저버 클래스를 쓰면 좋습니다. 옵저버 클래스의 메서드 이름은 듣고자 하는 Eloquent 이벤트와 일치합니다. 메서드 인수는 영향을 받은 모델 인스턴스입니다. 옵저버 클래스를 만들려면 [make:observer] Artisan 명령어를 이용하세요:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령은 새 옵저버 클래스를 `app/Observers`에 생성합니다. 디렉터리가 없으면 Artisan이 만들어줍니다. 기본 템플릿은 아래와 같습니다:

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

옵저버는 모델에 `ObservedBy` 특성으로 등록할 수 있습니다:

    use App\Observers\UserObserver;
    use Illuminate\Database\Eloquent\Attributes\ObservedBy;

    #[ObservedBy([UserObserver::class])]
    class User extends Authenticatable
    {
        //
    }

또는, 모델에서 직접 `observe` 메서드를 호출해 수동 등록도 가능합니다(일반적으로 `AppServiceProvider`의 `boot`에서):

    use App\Models\User;
    use App\Observers\UserObserver;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        User::observe(UserObserver::class);
    }

> [!NOTE]  
> 옵저버는 `saving`, `retrieved` 등 추가 이벤트도 들을 수 있습니다. 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 DB 트랜잭션

모델이 데이터베이스 트랜잭션 중 생성될 때, 옵저버가 트랜잭션 커밋 후에만 이벤트 핸들러를 실행하도록 하고 싶다면 옵저버에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하세요. 트랜잭션이 없을 경우 즉시 실행됩니다:

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

<a name="muting-events"></a>
### 이벤트 음소거

모델에서 발생하는 모든 이벤트를 일시적으로 "음소거(mute)"할 필요가 있을 수도 있습니다. 이 경우 `withoutEvents` 메서드로 클로저 내부 코드 실행 중 모델 이벤트를 비활성화할 수 있습니다. 클로저의 반환값은 그대로 반환됩니다:

    use App\Models\User;

    $user = User::withoutEvents(function () {
        User::findOrFail(1)->delete();

        return User::find(2);
    });

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 이벤트 음소거 저장

특정 모델의 "저장(save)"만 이벤트 발생 없이 처리하려면 `saveQuietly` 메서드를 쓸 수 있습니다:

    $user = User::findOrFail(1);

    $user->name = 'Victoria Faith';

    $user->saveQuietly();

"update", "delete", "soft delete", "restore", "replicate" 등의 작업도 조용히(이벤트 없이) 처리할 수 있습니다:

    $user->deleteQuietly();
    $user->forceDeleteQuietly();
    $user->restoreQuietly();
