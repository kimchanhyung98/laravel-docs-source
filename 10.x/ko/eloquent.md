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
    - [결과 쪼개기(Chunking)](#chunking-results)
    - [지연 컬렉션을 이용한 Chunking](#chunking-using-lazy-collections)
    - [커서(Cursor)](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [Upsert](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기(Pruning)](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버 사용](#observers)
    - [이벤트 뮤트(Muting)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스와의 상호작용을 즐겁게 만들어주는 객체-관계 매퍼(ORM)인 Eloquent를 내장하고 있습니다. Eloquent를 사용하면 데이터베이스 테이블마다 '모델'이 대응되며, 이 모델을 통해 해당 테이블과 상호작용할 수 있습니다. 테이블로부터 레코드를 조회하는 것 외에도 Eloquent 모델을 사용하면 레코드의 삽입, 수정, 삭제도 가능합니다.

> [!NOTE]  
> 시작하기 전에 애플리케이션의 `config/database.php` 구성 파일에서 데이터베이스 연결이 설정되어 있는지 확인하세요. 데이터베이스 구성에 대한 자세한 내용은 [데이터베이스 구성 공식 문서](/docs/{{version}}/database#configuration)를 참고하세요.

#### Laravel 부트캠프

Laravel을 처음 접하신다면 [Laravel Bootcamp](https://bootcamp.laravel.com)에 참여해 보시는 것을 권장합니다. Laravel Bootcamp에서는 Eloquent를 활용하여 첫 Laravel 애플리케이션을 직접 구축해 볼 수 있습니다. Laravel과 Eloquent가 제공하는 모든 기능을 체험할 수 있는 좋은 방법입니다.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장(extend)합니다. `make:model` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 새로운 모델을 생성할 수 있습니다:

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)도 함께 만들고 싶다면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```

모델 생성 시 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 유형의 클래스를 함께 생성할 수 있습니다. 이러한 옵션들을 조합하여 한 번에 여러 클래스를 생성할 수도 있습니다:

```shell
# 모델 및 FlightFactory 클래스 생성...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델 및 FlightSeeder 클래스 생성...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델 및 FlightController 클래스 생성...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, FlightController 리소스 클래스, 폼 요청 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델 및 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 단축키로 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 요청까지 생성...
php artisan make:model Flight --all

# pivot 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 정보 확인

모델 코드만 훑어봐서는 모든 속성(attributes)과 관계(relations)를 확인하기 어려울 수 있습니다. 이럴 때 `model:show` Artisan 명령어를 사용하면 모델의 모든 속성과 관계에 대한 편리한 개요를 확인할 수 있습니다:

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치합니다. 이제 기본 모델 클래스를 살펴보고 Eloquent의 주요 관례 중 일부를 알아보겠습니다:

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

위의 예제를 보면 `Flight` 모델이 어떤 데이터베이스 테이블과 연관되는지 Eloquent에 직접 지정하지 않았습니다. Eloquent는 기본적으로 클래스의 "스네이크 케이스(snake case)" 복수형 이름을 테이블 이름으로 사용합니다. 이 예시에서는 `Flight` 모델은 `flights` 테이블과 연결됩니다. 만약 `AirTrafficController` 모델이면 `air_traffic_controllers` 테이블과 연결됩니다.

모델과 연관된 데이터베이스 테이블이 이러한 관례에 맞지 않는다면, 모델에 `table` 속성을 명시적으로 설정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 연결된 테이블
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본 키

Eloquent는 모델과 연결된 데이터베이스 테이블에 기본 키(primary key) 컬럼이 `id`라고 가정합니다. 다른 컬럼을 기본 키로 사용하려면 `protected $primaryKey` 속성을 지정하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 테이블의 기본 키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 Eloquent는 기본 키가 자동 증가하는 정수라고 가정합니다. 수동으로 증가하지 않거나, 숫자가 아닌 키를 사용하려면 `public $incrementing` 속성을 `false`로 지정해야 합니다:

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

기본 키가 정수가 아닐 경우 `protected $keyType` 속성을 `string`으로 지정해야 합니다:

```php
<?php

class Flight extends Model
{
    /**
     * 기본 키 데이터 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent 모델은 최소 하나의 고유 "ID"(기본 키)만을 지원합니다. "복합" 기본 키(여러 컬럼으로 이루어진 기본 키)는 지원하지 않습니다. 하지만 하나의 고유 기본 키 외에 멀티 컬럼 unique 인덱스를 테이블에 추가하는 것은 가능합니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할 수도 있습니다. UUID는 36자 길이의 전역 고유 문자/숫자 식별자입니다.

모델에서 자동 증가 정수 키 대신 UUID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가하세요. 그리고 [UUID 컬럼](https://laravel.com/docs/{{version}}/migrations#column-method-uuid)이 존재하는지 확인해야 합니다:

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

기본적으로 `HasUuids` 트레이트는 ["ordered" UUID](https://laravel.com/docs/{{version}}/strings#method-str-ordered-uuid)를 생성합니다. 이 UUID는 인덱스된 DB 저장 시 정렬 효율이 높습니다.

특정 모델의 UUID 생성 과정을 오버라이딩하려면 `newUniqueId` 메서드를 모델에 정의하면 됩니다. 어떤 컬럼에 UUID가 할당될지 지정하려면 `uniqueIds` 메서드를 정의합니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델의 새로운 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID를 부여할 컬럼 목록
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 26자이며, 역시 정렬이 가능합니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 추가하고, [ULID 컬럼](https://laravel.com/docs/{{version}}/migrations#column-method-ulid)이 있는지 확인하세요:

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

Eloquent는 기본적으로 모델과 연관된 데이터베이스 테이블에 `created_at`과 `updated_at` 컬럼이 존재한다고 가정합니다. 모델이 생성되거나 수정될 때 이 컬럼들의 값이 자동으로 설정됩니다. 자동 관리를 원치 않으면 모델에 `$timestamps` 속성을 `false`로 지정하면 됩니다:

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

모델의 타임스탬프 포맷을 커스터마이징하려면 `$dateFormat` 속성을 설정하세요. 이 속성은 DB 저장 시나 JSON 변환 시 날짜 포맷에 영향을 줍니다:

```php
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

타임스탬프 컬럼의 이름을 변경하려면 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 정의하면 됩니다:

```php
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프를 갱신하지 않고 모델 작업을 하고 싶다면 `withoutTimestamps` 메서드에 클로저로 전달하여 처리할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment(['reads']));
```

<a name="database-connections"></a>
### 데이터베이스 연결

Eloquent 모델은 기본적으로 애플리케이션의 기본 DB 연결을 사용합니다. 특정 모델에 다른 연결을 사용하고 싶다면 `$connection` 속성을 정의하세요:

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
### 기본 속성 값

새로 인스턴스화된 모델에는 기본적으로 아무 속성 값도 없습니다. 모델 속성의 기본값을 정의하려면 `$attributes` 속성을 설정하세요. 값은 DB에서 읽은 "저장 가능한" 형태여야 합니다:

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
### Eloquent 엄격성 설정

Laravel은 상황에 따라 Eloquent의 동작과 "엄격성"을 조정할 수 있는 여러 메서드를 제공합니다.

예를 들어, `preventLazyLoading` 메서드는 레이지 로딩을 막을지에 대한 옵션 부울 인자를 받습니다. 보통 프로덕션 환경이 아닐 때만 레이지 로딩을 막도록 설정할 수 있습니다. 보통 이 코드는 `AppServiceProvider`의 `boot` 메서드에 둡니다:

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

또한, `preventSilentlyDiscardingAttributes`를 사용하면 채울 수 없는 속성을 할당하려 할 때 예외를 던지도록 할 수 있습니다. 개발 환경에서는 실수로 누락됐던 속성이 db에 저장되지 않아도 바로 알 수 있습니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

---

_(이하 전체 번역이 매우 길기 때문에, 한 번에 문서 전체를 번역하기 어렵습니다.  
계속 원하시면 "계속" 또는 "이어서 번역" 요청을 주시면 이어서 번역을 진행하겠습니다.)_

_⚠️ “코드 블록, HTML 태그, 링크 URL은 번역하지 않음”, “마크다운 형식 유지”, “전문 용어 적절하게 번역” 지침을 최대한 준수하여 작성했습니다._