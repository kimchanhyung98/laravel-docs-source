# Eloquent: 접근자, 변경자 & 캐스팅

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [입력 값 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Value Object에서 커스텀 캐스팅)](#castables)

<a name="introduction"></a>
## 소개

접근자(Accessor), 변경자(Mutator), 그리고 속성 캐스팅(Attribute Casting)은 Eloquent 모델 인스턴스에서 속성을 읽거나 저장할 때 속성 값을 변환할 수 있게 해주는 기능입니다. 예를 들어, [Laravel 암호화기](/docs/{{version}}/encryption)를 활용하여 값을 데이터베이스에 저장할 때 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성에 접근할 때 해당 값에 변환을 적용합니다. 접근자를 정의하려면 모델에 protected 메서드를 생성하고 해당 속성명을 "카멜 케이스"로 변환해서 메서드명을 지정하세요. 

이 예제에서는 `first_name` 속성에 대한 접근자를 정의합니다. Eloquent는 `first_name` 속성 값을 조회할 때 자동으로 이 접근자를 호출합니다. 모든 접근자/변경자 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름을 가져옵니다.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

모든 접근자 메서드는 속성 접근 및(선택적으로) 변경 방식을 정의하는 `Attribute` 인스턴스를 반환합니다. 위의 예제에서는 속성 조회 방식만 정의하고 있으며, 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 전달하고 있습니다.

위에서처럼, 컬럼의 원래 값이 접근자로 전달되어 값을 조작한 뒤 반환할 수 있습니다. 접근자 값에 접근하려면 모델의 `first_name` 속성에 그대로 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 계산된 값(computed value)을 모델의 배열/JSON 표현에 추가하고 싶다면, [직렬화 시 값을 추가해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 객체 생성(accessor)

때때로 하나의 접근자에서 여러 모델 속성을 변환하여 단일 "값 객체(value object)"로 생성해야 할 수 있습니다. 이 경우, `get` 클로저에 두 번째 인자인 `$attributes`를 받아 사용하세요. 이 배열에는 모델의 현재 모든 속성이 포함되어 전달됩니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소와 상호작용합니다.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```

<a name="accessor-caching"></a>
#### 접근자 캐싱

접근자에서 값을 객체로 반환할 경우, 접근자를 통해 반환된 객체의 값이 변경되면 모델이 저장되기 전에 그 값이 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자로 반환된 인스턴스를 유지해서, 접근자 호출 시마다 같은 인스턴스를 반환하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 문자열이나 불리언 등 단순 값이지만 계산 비용이 크다면 캐싱을 활성화하는 것이 유용할 수 있습니다. 이럴 때는 접근자 정의 시 `shouldCache` 메서드를 호출하세요:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로 객체 캐싱 동작을 비활성화하고 싶으면, `withoutObjectCaching` 메서드를 사용하세요:

```php
/**
 * 사용자의 주소와 상호작용합니다.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
### 변경자 정의하기

변경자는 Eloquent 속성에 값을 설정(set)할 때 변환을 적용합니다. 변경자를 정의하려면 Attribute 정의 시 `set` 인자를 전달하세요. 아래는 `first_name` 속성에 대한 변경자 예시로, 모델의 `first_name` 값을 설정할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 first name 을 다룹니다.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }
}
```

변경자 클로저는 설정하려는 값을 받아서, 변환 후 반환할 수 있습니다. 변경자를 사용하려면 단순히 Eloquent 모델의 `first_name` 속성에 값을 대입하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 코드에서는 `set` 콜백이 `Sally`를 받아서 `strtolower`로 변환한 뒤 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 값 변경하기

변경자가 한 번에 여러 속성 값을 변경해야 할 때는, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 관련 컬럼명을 나타냅니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소와 상호작용합니다.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="attribute-casting"></a>
## 속성 캐스팅

속성 캐스팅은 접근자, 변경자와 유사한 기능을 제공하지만, 별도의 메서드를 정의할 필요 없이 `casts` 메서드에서 속성별로 캐스트 타입을 지정할 수 있다는 점이 다릅니다.

`casts` 메서드는 속성명과 캐스트 타입을 key-value 쌍으로 반환하는 배열이어야 합니다. 지원되는 캐스트 타입은 다음과 같습니다:

<div class="content-list" markdown="1">

- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `hashed`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

예를 들어, 데이터베이스에 정수(0 또는 1)로 저장된 `is_admin` 속성을 불리언으로 캐스팅하려면 다음과 같이 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성을 반환합니다.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'is_admin' => 'boolean',
        ];
    }
}
```

캐스트를 정의하면, `is_admin` 속성은 항상 불리언으로 반환됩니다(설령 DB에 정수로 저장되어있어도):

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시로 다른 캐스트를 추가하고 싶으면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 정의들은 기존 캐스트와 병합됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` 인 속성은 캐스팅되지 않습니다. 또한, 관계명과 동일한 이름으로 캐스트(또는 속성)를 정의하거나, 모델의 기본 키에 캐스트를 할당하지 마세요.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 모델의 속성을 [유연한 `Illuminate\Support\Stringable` 객체](/docs/{{version}}/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성을 반환합니다.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'directory' => AsStringable::class,
        ];
    }
}
```

<a name="array-and-json-casting"></a>
### 배열 및 JSON 캐스팅

`array` 캐스트는 JSON으로 직렬화된 컬럼 처리에 특별히 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 타입으로 직렬화된 값이 저장된 경우, 해당 속성에 `array` 캐스트를 지정하면, Eloquent 모델에서 이 속성에 접근할 때 자동으로 PHP 배열로 역직렬화됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성을 반환합니다.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => 'array',
        ];
    }
}
```

캐스트가 정의되면, `options` 속성에 접근할 때마다 자동으로 JSON에서 PHP 배열로 역직렬화됩니다. 설정 시에는 배열이 자동으로 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 간단 문법으로 수정하려면, [대량 할당 가능](/docs/{{version}}/eloquent#mass-assignment-json-columns)하도록 하고, `->` 연산자를 이용해 `update`할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### ArrayObject 및 Collection 캐스팅

일반적인 `array` 캐스트는 많은 상황에서 충분하지만, 배열의 오프셋을 직접 수정하면 PHP 에러가 발생할 수 있습니다:

```php
$user = User::find(1);

$user->options['key'] = $value; // PHP 에러 발생!
```

이 문제를 해결하려면, Laravel의 `AsArrayObject` 캐스트를 사용하세요. 이 캐스트는 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환하여 개별 오프셋 수정이 가능하게 합니다. `AsArrayObject`를 속성에 지정하려면 다음과 같이 합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsArrayObject::class,
    ];
}
```

비슷하게, `AsCollection` 캐스트를 사용하면 속성을 Laravel의 [Collection](/docs/{{version}}/collections) 인스턴스로 변환할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::class,
    ];
}
```

`AsCollection` 캐스트로 커스텀 컬렉션 클래스를 지정하려면, `using()` 메서드에 클래스명을 전달하세요:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
    ];
}
```

<a name="date-casting"></a>
### 날짜 캐스팅

Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 자동 캐스팅합니다. (Carbon은 PHP `DateTime` 클래스를 확장한 날짜 라이브러리입니다.) 추가적인 날짜 속성이 있다면, 모델의 `casts` 메서드에 해당 캐스트 타입을 추가하세요. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스트 타입으로 지정합니다.

`date` 또는 `datetime` 캐스트 시, 출력 형식을 지정할 수도 있습니다. 이 형식은 [모델을 배열이나 JSON으로 직렬화](/docs/{{version}}/eloquent-serialization)할 때 적용됩니다:

```php
/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'created_at' => 'datetime:Y-m-d',
    ];
}
```

날짜로 캐스트된 컬럼의 값으로는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 지정할 수 있습니다. 각 값은 DB에 알맞게 변환되어 저장됩니다.

모델 전체의 기본 날짜 직렬화 포맷을 커스터마이즈하고 싶다면, `serializeDate` 메서드를 모델에 정의하세요.(이 설정은 DB 저장 형식에는 영향 없음):

```php
/**
 * 배열/JSON 직렬화 시 날짜 포맷을 지정합니다.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

DB에 날짜를 실제로 저장할 때 사용할 형식은 모델의 `$dateFormat` 속성으로 지정할 수 있습니다:

```php
/**
 * 모델의 날짜 컬럼 저장 포맷
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로, `date`와 `datetime` 캐스팅은 타임존 설정과 관계없이 날짜를 UTC ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 다른 PHP/JS 라이브러리와의 호환성을 극대화하려면, 항상 이 직렬화 포맷과 데이터베이스의 UTC 타임존 사용을 권장합니다.

만약 커스텀 포맷(예: `datetime:Y-m-d H:i:s`)을 지정했다면, Carbon 인스턴스의 내부 타임존이 직렬화에 사용됩니다. 보통은 앱의 `timezone` 설정값이 적용됩니다. 단, `created_at`, `updated_at`처럼 `timestamp` 타입 컬럼은 앱의 타임존과 상관없이 항상 UTC로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 PHP [Enum(열거형)](https://www.php.net/manual/en/language.enumerations.backed.php)으로 속성 값을 캐스팅할 수 있도록 지원합니다. 모델의 `casts` 메서드에서 속성과 Enum을 지정하세요:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'status' => ServerStatus::class,
    ];
}
```

캐스트를 지정하면, 해당 속성이 자동으로 Enum 객체와 값 상호 변환을 수행합니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

속성 하나에 Enum 값의 배열을 저장하려면 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 활용하세요:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'statuses' => AsEnumCollection::of(ServerStatus::class),
    ];
}
```

<a name="encrypted-casting"></a>
### 암호화 캐스팅

`encrypted` 캐스트는 Laravel의 [내장 암호화](/docs/{{version}}/encryption) 기능을 통해 모델의 속성 값을 암호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등은 이름 그대로 각각 암호화된 상태로 저장/변환합니다.

암호화된 텍스트의 실제 길이는 예측할 수 없으며 일반 텍스트보다 길기 때문에, 관련 DB 컬럼은 반드시 `TEXT` 타입 이상이어야 합니다. 또한, 암호화된 값은 DB에서 직접 조회나 검색이 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(암호화 키 변경)

Laravel은 앱의 `app` 설정 파일의 `key` 값(보통은 `APP_KEY` 환경 변수)에 기반하여 문자열을 암호화합니다. 만약 암호화 키를 교체해야 한다면, 새 키로 암호화된 속성들을 수동으로 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

쿼리 실행 중에 캐스팅을 적용하고 싶을 때가 있습니다. 예를 들어 Raw 쿼리로 계산된 값을 선택하여 그 컬럼에 별칭을 주는 경우 등입니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리에서 `last_posted_at`은 단순 문자열로 반환됩니다. 이때 `withCasts` 메서드를 사용해서 런타임에 해당 속성만 `datetime` 캐스팅 적용이 가능합니다:

```php
$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->withCasts([
    'last_posted_at' => 'datetime'
])->get();
```

<a name="custom-casts"></a>
## 커스텀 캐스트

Laravel은 다양한 내장 캐스트 타입을 제공하지만, 때로는 직접 캐스트 타입을 정의해야 할 필요가 있습니다. 커스텀 캐스트를 생성하려면 `make:cast` Artisan 명령어를 실행하세요. 생성된 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 내부에 `get`/`set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 읽은 원시값을 변환하고, `set` 메서드는 변환값을 DB에 저장 가능한 포맷으로 바꿉니다. 내장 `json` 캐스트를 예시로 직접 구현해봅니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * 값을 캐스팅합니다.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }

    /**
     * 저장을 위해 값을 준비합니다.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
```

커스텀 캐스트 타입을 정의하고 나면, 클래스명을 속성에 지정해 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성을 반환합니다.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => Json::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
### 값 객체 캐스팅

속성을 단순 타입(prmitive)이 아닌 객체로도 캐스팅할 수 있습니다. 객체로 캐스팅할 경우, `set` 메서드는 키/값 쌍의 배열을 반환하여 각각 실제 모델 속성에 매핑해야 합니다.

예로, 여러 모델 값을 하나의 `Address` 값 객체로 합치는 커스텀 캐스트 클래스를 정의해보겠습니다. `Address` 값 객체는 `lineOne`, `lineTwo` 두 개의 public 속성을 갖는다고 가정합니다:

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address as AddressValueObject;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class Address implements CastsAttributes
{
    /**
     * 값을 캐스팅합니다.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): AddressValueObject
    {
        return new AddressValueObject(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * 저장을 위해 값을 준비합니다.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, string>
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): array
    {
        if (! $value instanceof AddressValueObject) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

객체로 캐스팅한 속성 값을 변경하면, 모델 저장 전에 자동으로 모델에 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체가 포함된 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이 있다면, 해당 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하세요.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent에서 캐싱됩니다. 즉, 같은 속성 값에 여러 번 접근해도 동일한 객체 인스턴스가 반환됩니다.

만약 커스텀 캐스트 클래스의 객체 캐싱을 비활성화하려면, 커스텀 캐스트 클래스에 public 속성 `withoutObjectCaching`을 true로 선언하세요:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

`toArray` 및 `toJson`을 사용해 Eloquent 모델을 배열/JSON으로 변환할 때, 커스텀 캐스트된 값 객체도 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스가 구현되어 있다면 자동으로 잘 직렬화됩니다. 외부 라이브러리의 값 객체처럼 해당 인터페이스를 추가할 수 없는 경우, 커스텀 캐스트 클래스에서 직접 직렬화 책임을 질 수도 있습니다.

이럴 때, 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하면 됩니다. 이 인터페이스의 `serialize` 메서드에서 객체의 직렬화 형태를 반환하세요:

```php
/**
 * 값의 직렬화 표현을 반환합니다.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(Model $model, string $key, mixed $value, array $attributes): string
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 입력 값 캐스팅

가끔 속성의 **입력 값**(set 시에만)만 변환하고, 조회(get) 시에는 원래 값을 그대로 반환하고 싶을 수 있습니다.

입력 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, `set` 메서드만 필요합니다. Artisan 명령어로 생성 시 `--inbound` 옵션을 사용하세요:

```shell
php artisan make:cast Hash --inbound
```

입력 전용 캐스트의 고전적인 예시는 "해시" 캐스트입니다. 아래는 주어진 해시 알고리즘으로 입력 값을 해싱하는 예시입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 클래스 인스턴스 생성자
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장을 위해 값을 준비합니다.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return is_null($this->algorithm)
            ? bcrypt($value)
            : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
### 캐스트 파라미터

커스텀 캐스트를 속성에 지정할 때, 클래스명 뒤에 `:`로 인자를 지정하고, 여러 인자가 있다면 콤마(`,`)로 구분할 수 있습니다. 이 인자들은 캐스트 클래스의 생성자에 전달됩니다:

```php
/**
 * 캐스팅할 속성을 반환합니다.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => Hash::class.':sha256',
    ];
}
```

<a name="castables"></a>
### 캐스터블(Value Object에서 커스텀 캐스팅)

애플리케이션의 값 객체 자체가 어떤 캐스트 클래스를 사용해야 하는지 스스로 정의하게 만들고 싶을 때가 있습니다. 이때는 모델에 커스텀 캐스트 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는 `castUsing` 정적 메서드를 정의해야 하며, 이 메서드는 변환에 사용할 커스텀 캐스트 클래스명을 반환해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 이 객체 변환에 사용할 캐스터 클래스명 반환
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

`Castable` 클래스를 사용할 때도 인자를 `casts` 메서드 정의에서 지정할 수 있으며, 이 값은 `castUsing` 메서드에 전달됩니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class.':argument',
    ];
}
```

<a name="anonymous-cast-classes"></a>
#### 캐스터블 & 익명 캐스트 클래스

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하면, 값 객체와 변환 로직을 하나의 캐스터블 객체로 구현할 수 있습니다. 이때는 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 되며, 이 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 객체 변환에 사용할 캐스터 클래스 반환
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): CastsAttributes
    {
        return new class implements CastsAttributes
        {
            public function get(Model $model, string $key, mixed $value, array $attributes): Address
            {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(Model $model, string $key, mixed $value, array $attributes): array
            {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```