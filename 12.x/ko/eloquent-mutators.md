# Eloquent: 접근자(Mutators) & 캐스팅(Casting) (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [이진(Binary) 캐스팅](#binary-casting)
    - [날짜(Date) 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화(Encrypted) 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [사용자 정의 캐스팅](#custom-casts)
    - [값 객체(Value Object) 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드(입력 전용) 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자, 변경자, 그리고 속성 캐스팅 기능을 사용하면, Eloquent 모델 인스턴스에서 속성을 조회하거나 설정할 때 속성 값을 변환할 수 있습니다. 예를 들어, [Laravel의 암호화 엔진](/docs/12.x/encryption)을 사용하여 데이터베이스에 저장할 때 값을 암호화하고, Eloquent 모델에서 해당 속성을 조회할 때 자동으로 복호화할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 모델에서 접근할 때 배열로 변환하는 것도 가능합니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자(Accessor)는 Eloquent 속성 값을 조회할 때 변환하는 역할을 합니다. 접근자를 정의하려면, 모델에 해당 속성을 나타내는 보호된 메서드를 생성하세요. 이 메서드의 이름은 실제 모델 속성/데이터베이스 컬럼의 "카멜 케이스(camel case)" 형태여야 합니다.

아래 예시에서는 `first_name` 속성에 대한 접근자를 정의합니다. 이 접근자는 Eloquent에서 `first_name` 값을 조회할 때마다 자동으로 호출됩니다. 모든 접근자/변경자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입의 반환 값을 명시해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

모든 접근자 메서드는 접근 및(선택적으로) 변경을 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예시에서는 속성에 접근하는 방법만 정의하였으며, 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 전달하였습니다.

보시는 것처럼, 원본 컬럼 값이 접근자에 전달되어 값을 조작 및 반환할 수 있습니다. 접근자 값을 조회하려면 모델 인스턴스에서 `first_name` 속성에 단순히 접근하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이러한 계산된(computed) 값들을 모델의 배열/JSON 표현에 추가하고 싶다면, [별도로 append를 지정해주어야 합니다](/docs/12.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

때로는 접근자가 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 때가 있습니다. 이를 위해 `get` 클로저에 두 번째 인수 `$attributes`를 받을 수 있습니다. 이 인수에는 현재 모델의 모든 속성이 배열로 담겨 자동으로 전달됩니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
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

접근자에서 값 객체를 반환할 경우, 값 객체에 가한 변경사항이 모델이 저장되기 전 자동으로 모델에 반영됩니다. 이는 Eloquent가 접근자로 반환된 인스턴스를 보관하여, 접근자가 호출될 때마다 동일한 인스턴스를 반환하기 때문입니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 계산 비용이 큰 문자열이나 불리언 등 원시 값에도 캐싱을 적용하고 싶을 때가 있습니다. 이 경우, 접근자 정의 시 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 속성의 객체 캐싱을 비활성화하고 싶을 경우 `withoutObjectCaching` 메서드를 호출할 수 있습니다.

```php
/**
 * Interact with the user's address.
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

변경자(Mutator)는 Eloquent 모델 속성을 설정할 때 값을 변환합니다. 변경자를 정의하려면, 속성 정의 시 `set` 인자를 제공하면 됩니다. 예를 들어, `first_name` 속성의 변경자를 정의해보겠습니다. 모델에서 `first_name` 속성을 설정하려 할 때 자동으로 변경자가 호출됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Interact with the user's first name.
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

변경자 클로저는 속성에 설정하려는 값을 받아 이를 조작하여 반환할 수 있습니다. 변경자를 사용하기 위해서는 Eloquent 모델에서 단순히 `first_name` 속성에 값을 할당하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예시에서 `set` 콜백이 `Sally` 값을 받아 `strtolower` 함수를 적용하여 내부 `$attributes` 배열에 결과 값을 설정합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 값 변경하기

변경자에서 모델의 여러 속성을 동시에 설정해야 할 때도 있습니다. 이 경우 `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델과 매핑되는 실제 속성/데이터베이스 컬럼 이름이어야 합니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
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
## 속성 캐스팅 (Attribute Casting)

속성 캐스팅은 접근자 및 변경자와 유사한 기능을 제공하지만, 별도의 메서드 정의 없이도 속성 타입 변환을 쉽게 할 수 있도록 도와줍니다. 모델의 `casts` 메서드에서 캐스팅할 속성과 타입을 정의하면 됩니다.

`casts` 메서드는 반환값으로 캐스팅할 속성명을 키로, 캐스팅할 타입을 값으로 하는 배열을 반환해야 합니다. 지원되는 캐스팅 타입은 다음과 같습니다.

<div class="content-list" markdown="1">

- `array`
- `AsFluent::class`
- `AsStringable::class`
- `AsUri::class`
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

속성 캐스팅의 예로, 데이터베이스에는 정수(`0` 또는 `1`)로 저장되어 있는 `is_admin` 속성을 boolean으로 캐스팅하는 방법을 살펴보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
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

캐스트를 정의하면, 데이터베이스에 integer로 저장되어 있더라도 `is_admin` 속성을 조회하면 항상 boolean 값으로 변환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 일시적으로 새로운 캐스트를 추가하고 싶을 경우 `mergeCasts` 메서드를 사용할 수 있습니다. 이렇게 정의된 캐스트는 기존 캐스트에 병합됩니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 관계와 이름이 겹치는 속성에는 캐스트를 정의해서는 안 되며, 모델의 기본 키에도 캐스트를 할당하지 않아야 합니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스팅 클래스를 이용하면 모델 속성을 [플루언트 Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 변환할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
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

`array` 캐스팅은 직렬화된 JSON 형태로 저장된 컬럼을 사용할 때 특히 유용합니다. 데이터베이스에서 `JSON` 또는 `TEXT` 컬럼 타입에 직렬화된 JSON이 저장되어 있다면, 해당 속성에 `array` 캐스트를 추가하면 Eloquent 모델에서 속성을 접근할 때 자동으로 PHP 배열로 변환됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
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

캐스트가 정의된 이후에는 `options` 속성을 접근하면 자동으로 JSON에서 PHP 배열로 역직렬화됩니다. 반대로 값을 설정할 때는 전달한 배열이 JSON으로 직렬화되어 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 간결하게 업데이트하고 싶을 때는, [해당 속성을 대량 할당 가능하도록 지정](/docs/12.x/eloquent#mass-assignment-json-columns)하고, `update` 메서드에서 `->` 연산자를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 JSON으로 저장할 때 이스케이프 되지 않은 유니코드 문자로 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다.

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => 'json:unicode',
    ];
}
```

<a name="array-object-and-collection-casting"></a>
#### Array Object 및 Collection 캐스팅

일반적인 `array` 캐스팅은 많은 경우에 충분하지만, 몇 가지 단점이 존재합니다. `array` 캐스팅은 원시 타입을 반환하므로 배열의 오프셋을 직접 변경할 수 없습니다. 예를 들어 아래 코드처럼 사용하면 PHP 에러가 발생합니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 [사용자 정의 캐스팅](#custom-casts) 기반으로 구현되어 있으며, 변형된 객체를 캐시 및 변환하여 개별 오프셋을 안전하게 조작할 수 있습니다. 사용 방법은 다음과 같습니다.

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * Get the attributes that should be cast.
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

마찬가지로, `AsCollection` 캐스트를 사용하면 JSON 속성을 Laravel [컬렉션](/docs/12.x/collections) 인스턴스로 변환할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
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

`AsCollection` 캐스트가 Laravel의 기본 컬렉션 클래스가 아니라 여러분이 만든 커스텀 컬렉션 클래스를 인스턴스화하길 원한다면, 캐스트 인자로 컬렉션 클래스명을 전달하면 됩니다.

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
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

또한, `of` 메서드를 사용하면 컬렉션 항목을 지정한 클래스로 변환할 수 있습니다. ([mapInto 메서드 참고](/docs/12.x/collections#method-mapinto))

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::of(Option::class)
    ];
}
```

컬렉션을 객체로 매핑할 때, 해당 객체는 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하여 데이터베이스에 JSON으로 직렬화하는 방법을 정의해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Support\Arrayable;
use JsonSerializable;

class Option implements Arrayable, JsonSerializable
{
    public string $name;
    public mixed $value;
    public bool $isLocked;

    /**
     * Create a new Option instance.
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * Get the instance as an array.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'value' => $this->value,
            'is_locked' => $this->isLocked,
        ];
    }

    /**
     * Specify the data which should be serialized to JSON.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```

<a name="binary-casting"></a>
### 이진(Binary) 캐스팅

Eloquent 모델에 [바이너리 타입](/docs/12.x/migrations#column-method-binary)의 `uuid` 또는 `ulid` 컬럼이 있고, 자동증가 ID 컬럼이 추가로 있을 경우, `AsBinary` 캐스트를 사용하면 해당 값을 이진(binary) 표현과 일반 문자열 표현 사이에서 자동으로 변환할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Casts\AsBinary;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'uuid' => AsBinary::uuid(),
        'ulid' => AsBinary::ulid(),
    ];
}
```

캐스트를 모델에 정의하면, UUID/ULID 속성값에 객체 인스턴스 또는 문자열을 할당할 수 있습니다. Eloquent가 자동으로 이진 표현으로 변환해 저장하며, 값을 조회할 때는 항상 일반 문자열로 반환됩니다.

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### 날짜(Date) 캐스팅

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP의 `DateTime` 클래스를 확장하여 다양한 유용한 기능을 제공합니다. 추가적으로 다른 날짜 속성을 캐스팅하려면 모델의 `casts` 메서드에 정의하면 됩니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 타입으로 캐스팅합니다.

`date` 또는 `datetime` 캐스팅 시, 날짜 포맷도 지정할 수 있습니다. 이 포맷은 [모델을 배열이나 JSON으로 직렬화할 때](/docs/12.x/eloquent-serialization) 사용됩니다.

```php
/**
 * Get the attributes that should be cast.
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

날짜 컬럼으로 캐스팅된 속성에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 할당할 수 있습니다. 값은 올바르게 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜 직렬화 기본 포맷을 변경하려면 모델에 `serializeDate` 메서드를 정의하세요. 이 메서드는 데이터베이스에 저장되는 포맷에는 영향을 주지 않습니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스 저장용 날짜 퍼맷을 지정하려면 모델에 `$dateFormat` 속성을 지정하세요.

```php
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 타임존

기본적으로, `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정에 관계없이 UTC의 ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)으로 날짜를 직렬화합니다. 애플리케이션의 날짜를 UTC로 저장하고, `timezone` 설정을 기본값(UTC)에서 변경하지 않고 사용할 것을 강력히 권장합니다. 일관적으로 UTC를 사용하면 PHP, JavaScript의 타 라이브러리와의 호환성이 극대화됩니다.

`date` 또는 `datetime` 캐스트에 커스텀 포맷(`datetime:Y-m-d H:i:s` 등)을 지정한 경우, Carbon 인스턴스의 내부 타임존이 직렬화시 적용됩니다. 이는 보통 애플리케이션의 `timezone` 설정과 동일합니다. 단, `created_at`, `updated_at` 같은 `timestamp` 컬럼은 예외적으로 항상 UTC로 저장 및 직렬화됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 캐스팅할 수도 있습니다. 이를 위해 모델의 `casts` 메서드에 속성과 Enum을 지정합니다.

```php
use App\Enums\ServerStatus;

/**
 * Get the attributes that should be cast.
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

캐스트를 모델에 정의하면 해당 속성은 Enum과 상호작용할 때 자동으로 Enum 객체로 변환됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

모델이 단일 컬럼에 Enum 값들의 배열을 저장해야 할 때도 있습니다. 이때는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 이용하면 됩니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * Get the attributes that should be cast.
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
### 암호화(Encrypted) 캐스팅

`encrypted` 캐스트는 Laravel의 내장 [암호화](/docs/12.x/encryption) 기능을 사용해 모델 속성 값을 암호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트 또한, 그 비암호화 버전과 동일하게 동작하지만 데이터를 데이터베이스에 저장할 때 암호화된다는 점이 다릅니다.

암호화된 텍스트는 최종적으로 평문보다 더 길고 길이를 예측할 수 없으므로, 해당 데이터베이스 컬럼은 `TEXT` 타입 이상이어야 합니다. 또한 암호화된 값은 데이터베이스에서 직접 조회하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 애플리케이션 `app` 설정 파일의 `key` 값(일반적으로 `APP_KEY` 환경 변수)에 따라 문자열을 암호화합니다. 키를 교체해야 할 경우, 암호화된 속성은 새로운 키로 수동으로 다시 암호화해주어야 합니다.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

쿼리 실행 시점에(즉시) 캐스팅을 적용해야 하는 경우가 있습니다. 예를 들어, 테이블에서 raw 값을 선택(select)할 때 아래와 같은 쿼리가 있다고 합시다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리 결과의 `last_posted_at` 속성은 단순 문자열입니다. 쿼리를 실행할 때 이 속성에 `datetime` 캐스트를 적용하고 싶다면 `withCasts` 메서드를 사용할 수 있습니다.

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
## 사용자 정의 캐스팅 (Custom Casts)

Laravel에는 다양한 내장 캐스트 타입이 있지만, 필요에 따라 직접 캐스트 타입을 정의할 수도 있습니다. 캐스트를 생성하려면 `make:cast` Artisan 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉토리에 생성됩니다.

```shell
php artisan make:cast AsJson
```

모든 사용자 정의 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, `get`, `set` 메서드를 필수로 정의해야 합니다. `get`은 데이터베이스의 원시 값을 캐스트 값으로 변환하고, `set`은 반대로 캐스트 값을 데이터베이스에 저장할 수 있는 값으로 변환합니다. 아래는 내장 `json` 캐스트를 직접 구현하는 예시입니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return json_encode($value);
    }
}
```

캐스트 타입을 정의한 후에는, 클래스명을 속성에 지정하여 캐스트를 적용할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsJson::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
### 값 객체(Value Object) 캐스팅

단순한 원시 타입뿐 아니라 객체로도 캐스팅할 수 있습니다. 값 객체로의 캐스팅 구현은 원시 타입 캐스팅과 비슷하지만, 여러 데이터베이스 컬럼을 아우르는 값 객체라면 `set`에서 키/값 쌍 배열을 반환해야 합니다. 단일 컬럼만 영향을 미친다면 저장 가능한 값을 단일 값으로 반환하면 됩니다.

예시로, 여러 모델 값을 하나의 `Address` 값 객체로 변환하는 사용자 정의 캐스트를 정의해 보겠습니다. `Address` 객체에는 `lineOne`, `lineTwo` 두 개의 public 속성이 있다고 가정합니다.

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class AsAddress implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): Address {
        return new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, string>
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        if (! $value instanceof Address) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅된 속성에 변경사항이 생긴 경우, 모델이 저장되기 전에 해당 값이 자동 동기화됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 배열이나 JSON으로 직렬화할 예정이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 반드시 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 조회되면, Eloquent는 객체를 캐시합니다. 즉, 해당 속성에 다시 접근해도 같은 인스턴스가 반환됩니다.

사용자 정의 캐스트 클래스에서 이 객체 캐싱 동작을 비활성화하려면, 클래스에 public 속성으로 `withoutObjectCaching`을 선언하세요.

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델에서 `toArray` 또는 `toJson` 메서드를 사용해 배열이나 JSON으로 변환하면, 사용자 정의 캐스트 값 객체 역시 (해당 객체가 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현하는 한) 직렬화됩니다. 하지만, 서드파티 라이브러리가 제공하는 값 객체처럼 그런 인터페이스를 추가할 수 없는 경우가 있을 수 있습니다.

이때는 사용자 정의 캐스트 클래스가 값 객체의 직렬화를 담당하도록 지정할 수 있습니다. 이 경우, 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 하며, 직렬화된 형태를 반환하는 `serialize` 메서드를 추가해야 합니다.

```php
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(
    Model $model,
    string $key,
    mixed $value,
    array $attributes,
): string {
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 인바운드(입력 전용) 캐스팅

가끔은 값이 모델에 설정될 때만 변환되며, 조회 시에는 변환 작업이 필요 없는 사용자 정의 캐스트 클래스가 필요할 수 있습니다.

이런 인바운드 전용(custom cast)은 `CastsInboundAttributes` 인터페이스만 구현하면 되며, 이 인터페이스에는 `set` 메서드 하나만 필요합니다. Artisan의 `make:cast` 명령어에 `--inbound` 옵션을 추가해 생성할 수 있습니다.

```shell
php artisan make:cast AsHash --inbound
```

인바운드 전용 캐스트의 대표적인 예는 "해시" 캐스트입니다. 예를 들어, 주어진 알고리즘을 통해 값을 해시하는 캐스트를 정의할 수 있습니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * Create a new cast class instance.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return is_null($this->algorithm)
            ? bcrypt($value)
            : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
### 캐스트 파라미터

사용자 정의 캐스트를 모델에 추가할 때, `:` 문자로 클래스명과 파라미터를 구분하여 여러 개의 파라미터를 콤마로 구분해 지정할 수 있습니다. 이 파라미터들은 캐스트 클래스의 생성자로 전달됩니다.

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => AsHash::class.':sha256',
    ];
}
```

<a name="comparing-cast-values"></a>
### 캐스트 값 비교

두 캐스트 값이 동일한지 비교하는 로직을 직접 정의하고 싶을 경우, 사용자 정의 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현하면 됩니다. 이를 통해 Eloquent가 값이 변경된 것으로 인식해야 모델을 저장할지 세밀하게 제어할 수 있습니다.

이 인터페이스는 두 값이 같으면 `true`를 반환하는 `compare` 메서드를 요구합니다.

```php
/**
 * Determine if the given values are equal.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $firstValue
 * @param  mixed  $secondValue
 * @return bool
 */
public function compare(
    Model $model,
    string $key,
    mixed $firstValue,
    mixed $secondValue
): bool {
    return $firstValue === $secondValue;
}
```

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션에서 사용하는 값 객체가 고유의 커스텀 캐스트 클래스를 정의하도록 하고 싶을 때는, 모델에 캐스트 클래스를 직접 지정하는 대신 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정할 수도 있습니다.

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는, 해당 클래스에서 커스텀 캐스트 클래스를 반환하는 `castUsing` 메서드를 정의해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

`Castable` 클래스를 사용할 때도, `casts` 메서드 정의에 인자를 전달할 수 있습니다. 전달된 인자는 `castUsing` 메서드로 전달됩니다.

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

"캐스터블" 기능과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하여 값 객체와 캐스팅 로직을 단일 객체로 정의할 수도 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * Get the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): CastsAttributes
    {
        return new class implements CastsAttributes
        {
            public function get(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): Address {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): array {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```
