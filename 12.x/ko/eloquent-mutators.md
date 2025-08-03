# Eloquent: Mutators & Casting (Eloquent: 뮤터터와 캐스팅)

- [소개](#introduction)
- [액세서(Accessors)와 뮤터터(Mutators)](#accessors-and-mutators)
    - [액세서 정의하기](#defining-an-accessor)
    - [뮤터터 정의하기](#defining-a-mutator)
- [속성 캐스팅 (Attribute Casting)](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시간 캐스팅](#query-time-casting)
- [커스텀 캐스트(Custom Casts)](#custom-casts)
    - [값 객체 캐스팅(Value Object Casting)](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅(Inbound Casting)](#inbound-casting)
    - [캐스트 파라미터(Cast Parameters)](#cast-parameters)
    - [캐스트 값 비교하기(Comparing Cast Values)](#comparing-cast-values)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

액세서(accessors), 뮤터터(mutators), 그리고 속성 캐스팅(attribute casting)은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 그 값을 변환할 수 있도록 도와줍니다. 예를 들어, 데이터베이스에 값을 저장할 때 [Laravel 암호화기](/docs/12.x/encryption)를 사용해 값을 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때는 자동으로 복호화하고 싶을 수 있습니다. 또는 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델에서 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 액세서(Accessors)와 뮤터터(Mutators)

<a name="defining-an-accessor"></a>
### 액세서 정의하기 (Defining an Accessor)

액세서는 Eloquent 속성 값을 읽을 때 그 값을 변환하는 역할을 합니다. 액세서를 정의하려면, 모델 클래스 안에 보호된(protected) 메서드를 생성하고, 해당 메서드 이름은 기본 모델 속성 또는 데이터베이스 컬럼 이름을 카멜 케이스(camelCase)로 표현한 것과 일치해야 합니다.

예제로 `first_name` 속성에 대한 액세서를 정의해보겠습니다. 이 액세서는 Eloquent가 `first_name` 속성 값을 읽으려 할 때 자동으로 호출됩니다. 모든 속성 액세서/뮤터터 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute`의 반환 타입 힌트를 반드시 선언해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first name)을 가져옵니다.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

모든 액세서 메서드는 `Attribute` 인스턴스를 반환하며, 이 인스턴스는 속성이 어떻게 읽히고(그리고 선택적으로 변경될지) 정의합니다. 위 예제에서는 오직 속성 읽기(`get`)만 정의했습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 전달했습니다.

보시는 것처럼, 원래 컬럼의 값이 액세서로 전달되어 그 값을 원하는 대로 조작하고 반환할 수 있습니다. 액세서 값을 접근하려면 Eloquent 모델 인스턴스에서 `first_name` 속성에 단순히 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 만약 이러한 계산된 값들을 JSON이나 배열 변환 결과에 포함하고 싶다면, [해당 속성을 append해야 합니다](/docs/12.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로부터 값 객체 생성하기

때로는 액세서가 여러 모델 속성을 조합해서 하나의 "값 객체"를 생성해야 할 때가 있습니다. 이 경우 `get` 클로저에 두 번째 인자로 `$attributes` 배열을 받을 수 있습니다. 이 배열은 모델의 현재 모든 속성을 포함합니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소(Address)와 상호작용합니다.
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
#### 액세서 캐싱 (Accessor Caching)

액세서가 값 객체를 반환하면, 해당 값 객체에 대해 이뤄진 변경사항은 모델이 저장되기 전에 자동으로 모델에 동기화됩니다. 이는 Eloquent가 액세서가 반환한 객체를 인스턴스 캐시하여, 액세서가 호출될 때마다 동일한 인스턴스를 반환하기 때문에 가능합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 때로는 문자열이나 불리언 같은 원시 값을 캐싱하고 싶을 때가 있습니다. 특히 계산 비용이 큰 경우에 그렇습니다. 이럴 때는 액세서를 정의할 때 `shouldCache` 메서드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 객체 캐시 기능을 비활성화하고 싶다면, 액세서 정의시 `withoutObjectCaching` 메서드를 호출하면 됩니다:

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
### 뮤터터 정의하기 (Defining a Mutator)

뮤터터는 Eloquent 속성 값이 설정될 때 그 값을 변환합니다. 뮤터터를 정의할 때 `set` 인자를 추가로 제공하면 됩니다. `first_name` 속성에 대한 뮤터터를 정의해보겠습니다. 해당 속성에 값을 설정할 때 자동 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first name)과 상호작용합니다.
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

뮤터터 클로저는 설정되는 값을 받고, 값을 조작한 후 변환된 값을 반환해야 합니다. 뮤터터를 사용하려면 단순히 Eloquent 모델의 `first_name` 속성에 값을 할당하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예제에서 `set` 콜백은 `Sally` 값을 받고, `strtolower`를 적용해 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성을 뮤테이트하기 (Mutating Multiple Attributes)

때로는 뮤터터가 기본 모델에 여러 속성을 동시에 설정해야 할 때가 있습니다. 이 경우 `set` 클로저가 배열을 반환할 수 있으며, 배열의 키는 각각 대응하는 모델 속성 또는 데이터베이스 컬럼명이어야 합니다:

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
## 속성 캐스팅 (Attribute Casting)

속성 캐스팅은 액세서와 뮤터터와 유사한 기능을 제공하지만, 별도의 메서드를 정의할 필요 없이 모델의 `casts` 메서드에 간편하게 설정할 수 있습니다. `casts` 메서드는 캐스팅 대상 속성명과 캐스팅할 데이터 타입을 키-값 형태의 배열로 반환합니다.

지원되는 캐스트 타입은 다음과 같습니다:

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
- `decimal:<precision>`
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

예를 들어, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언으로 캐스팅하려면 다음과 같이 정의합니다:

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

캐스트 정의 후에는, `is_admin` 속성에 접근할 때 항상 캐스팅되어 불리언 값으로 반환됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 일시적인 캐스트를 추가하고 싶다면, `mergeCasts` 메서드를 사용하면 됩니다. 이렇게 하면 기존 캐스트에 추가됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` 값은 캐스팅하지 않습니다. 또한 관계 이름과 동일한 이름의 캐스트(또는 속성)를 정의해서는 안 되며, 기본키에 캐스트를 지정하는 것도 피해야 합니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면, 모델 속성을 [fluent Illuminate\Support\Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다:

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
### 배열 및 JSON 캐스팅 (Array and JSON Casting)

`array` 캐스팅은 JSON으로 직렬화된 컬럼을 다룰 때 특히 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 필드 타입으로 JSON이 저장되어 있다면, 해당 속성에 `array` 캐스트를 지정하면 Eloquent 모델에서 접근할 때 자동으로 PHP 배열로 역직렬화됩니다:

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

캐스트가 정의된 후에는 `options` 속성에 접근하면 JSON에서 PHP 배열로 자동 역직렬화되고, 값을 설정하면 다시 JSON으로 자동 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 한 필드를 간단하게 업데이트하려면, 해당 속성을 대량 할당(mass assignable) 하고 `update` 메서드에서 화살표(`->`) 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

유니코드 문자가 이스케이프되지 않은 상태로 JSON 배열 속성을 저장하고 싶으면 `json:unicode` 캐스트를 사용할 수 있습니다:

```php
/**
 * 캐스팅할 속성을 반환합니다.
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
#### ArrayObject와 Collection 캐스팅

표준 `array` 캐스트는 많은 곳에서 적합하지만, 원시 배열 타입을 반환하기 때문에 배열 오프셋을 직접 수정할 수 없는 단점이 있습니다. 아래 코드는 PHP 오류를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php)로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이는 Laravel 커스텀 캐스트 기능을 활용해, 변형된 객체를 캐싱 및 스마트하게 변환하여 배열 인덱스 변경 시 오류가 나지 않도록 합니다. 사용법은 간단하며 속성에 할당하면 됩니다:

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

마찬가지로 Laravel은 `AsCollection` 캐스트를 제공하며 JSON 속성을 Laravel [Collection](/docs/12.x/collections) 인스턴스로 캐스팅합니다:

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

`AsCollection` 캐스트를 사용해 Laravel 기본 컬렉션 대신 커스텀 컬렉션 클래스를 인스턴스화하려면 컬렉션 클래스명을 캐스트 인자로 제공할 수 있습니다:

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

컬렉션 아이템을 특정 클래스 인스턴스로 매핑하려면 `of` 메서드를 사용해 컬렉션의 [mapInto 메서드](/docs/12.x/collections#method-mapinto)를 활용할 수 있습니다:

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성을 반환합니다.
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

컬렉션을 객체로 매핑할 때, 해당 객체는 인스턴스가 데이터베이스에 JSON으로 직렬화되는 방식을 정의하기 위해 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다:

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
     * 새로운 Option 인스턴스 생성자.
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * 인스턴스를 배열로 반환합니다.
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
     * JSON으로 직렬화할 데이터를 지정합니다.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```

<a name="date-casting"></a>
### 날짜 캐스팅 (Date Casting)

기본적으로 Eloquent는 `created_at` 및 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon)의 인스턴스로 캐스팅합니다. Carbon은 PHP의 `DateTime` 클래스를 확장하며 유용한 메서드를 제공합니다. 추가적으로 날짜 속성을 캐스팅하려면 모델의 `casts` 메서드에서 `datetime` 또는 `immutable_datetime` 타입으로 날짜를 지정하면 됩니다.

`date` 또는 `datetime` 캐스트 정의 시 날짜 형식을 지정할 수도 있습니다. 이 형식은 [모델이 배열이나 JSON으로 직렬화될 때](/docs/12.x/eloquent-serialization)에 사용됩니다:

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

날짜로 캐스팅된 컬럼에 UNX 타임스탬프, 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 할당해도 자동으로 올바른 형식으로 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜에 대해 기본 직렬화 형식을 변경하려면, 모델에 `serializeDate` 메서드를 정의할 수 있습니다. 이 메서드는 데이터베이스 저장 형식에는 영향을 주지 않습니다:

```php
/**
 * 배열 또는 JSON 직렬화를 위한 날짜 준비.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 날짜를 저장할 때 사용할 형식을 변경하려면, 모델에 `$dateFormat` 속성을 정의하세요:

```php
/**
 * 모델 날짜 컬럼의 저장 형식.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스트는 어플리케이션 `timezone` 설정과 무관하게 날짜를 UTC ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`) 형식으로 직렬화합니다. 애플리케이션 내에서 UTC 타임존을 일관되게 사용하면 PHP와 JavaScript 날짜 라이브러리와의 상호 운용성을 극대화할 수 있으므로 권장합니다.

캐스트에 사용자 지정 포맷을 지정하면(예: `datetime:Y-m-d H:i:s`), 날짜 직렬화 시 Carbon 인스턴스의 내부 타임존(일반적으로 `timezone` 설정 값)이 사용됩니다. 단, `created_at`, `updated_at` 같은 `timestamp` 컬럼은 예외로 애플리케이션 타임존과 상관없이 항상 UTC로 포맷팅됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로 속성을 캐스팅할 수 있습니다. 모델의 `casts` 메서드에서 해당 속성과 Enum 클래스를 지정하세요:

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

캐스트를 정의한 뒤에는 지정한 속성이 Enum으로 자동 변환되어 작동합니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

컬럼 하나에 Enum 배열을 저장해야 할 때는 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

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
### 암호화된 캐스팅 (Encrypted Casting)

`encrypted` 캐스트는 Laravel의 내장 [암호화 기능](/docs/12.x/encryption)을 사용하여 모델 속성 값을 암호화합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트도 비슷하게 작동하지만, 저장시 값이 암호화됩니다.

암호화된 텍스트의 최종 길이는 예측할 수 없고 원본 텍스트보다 길기 때문에, 해당 데이터베이스 컬럼은 `TEXT` 타입 이상이어야 합니다. 그리고 암호화된 속성 값은 데이터베이스에서 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체 (Key Rotation)

Laravel은 `app` 설정 파일에 지정된 `key` 값을 사용해 문자열을 암호화합니다. 보통 이 값은 환경 변수 `APP_KEY`에 대응합니다. 암호화 키를 변경해야 할 경우, 암호화된 속성 값을 새 키로 수동 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 실행 시 캐스팅 (Query Time Casting)

쿼리를 실행하는 동안 캐스트를 적용해야 할 때가 있습니다. 예를 들어, 테이블에서 raw 값을 선택할 때 다음과 같은 쿼리가 있을 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리 결과의 `last_posted_at` 속성은 단순 문자열인데, 쿼리 시점에 `datetime` 캐스팅을 적용할 수 있다면 좋습니다. `withCasts` 메서드가 이 역할을 합니다:

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
## 커스텀 캐스트 (Custom Casts)

Laravel은 여러 내장 캐스트 타입을 제공하지만, 필요에 따라 자신만의 캐스트 클래스를 정의해야 할 때도 있습니다. 캐스트 클래스를 생성하려면 `make:cast` Artisan 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `get`과 `set` 메서드를 요구합니다. `get` 메서드는 데이터베이스의 원시값을 변환해 캐스트 값으로 만들어야 하고, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 원시값으로 변환해야 합니다.

다음은 기본 내장 `json` 캐스트 타입을 커스텀 캐스트로 재구현한 예입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * 주어진 값을 캐스팅합니다.
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
     * 저장을 위해 주어진 값을 준비합니다.
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

커스텀 캐스트 클래스를 정의한 뒤에는, 클래스명을 모델의 `casts` 배열에 할당해 캐스트할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
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
            'options' => AsJson::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
### 값 객체 캐스팅 (Value Object Casting)

캐스트는 원시 타입에 국한하지 않고 객체 타입으로도 할 수 있습니다. 값 객체를 캐스팅하려면 기본적인 캐스팅과 유사하지만, 값 객체가 여러 데이터베이스 컬럼을 포괄할 경우 `set` 메서드는 모델에 저장할 원시 값들의 키-값 배열을 반환해야 합니다. 값 객체가 단일 컬럼에만 영향을 준다면, 그냥 저장 가능한 값을 반환하면 됩니다.

예제로, 여러 모델 속성을 단일 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의해보겠습니다. 여기서 `Address`는 두 개의 공용 프로퍼티 `lineOne`과 `lineTwo`를 가집니다:

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
     * 주어진 값을 캐스팅합니다.
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
     * 저장을 위해 주어진 값을 준비합니다.
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
            throw new InvalidArgumentException('주어진 값이 Address 인스턴스가 아닙니다.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅된 속성은 해당 값 객체에서 이루어진 변경 사항이 모델이 저장되기 전에 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 만약 값 객체가 포함된 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 해당 값 객체는 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱 (Value Object Caching)

값 객체로 캐스팅된 속성은 Eloquent에서 캐싱되어, 속성을 다시 접근할 때 항상 동일한 인스턴스를 반환합니다.

객체 캐싱 기능을 비활성화하려면, 커스텀 캐스트 클래스에 `public bool $withoutObjectCaching = true;` 프로퍼티를 선언하면 됩니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화 (Array / JSON Serialization)

Eloquent 모델을 `toArray`, `toJson` 메서드로 변환할 때, 커스텀 캐스트 값 객체는 일반적으로 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현하고 있으면 올바르게 직렬화됩니다. 그러나 서드파티 라이브러리의 값 객체는 이 인터페이스를 구현하지 않았을 수 있습니다.

이럴 때는 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메서드를 정의해 직접 직렬화 로직을 구현할 수 있습니다:

```php
/**
 * 값의 직렬화된 표현을 반환합니다.
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
### 인바운드 캐스팅 (Inbound Casting)

때로는 모델에서 속성 값을 읽을 때는 변환하지 않고, 설정할 때만 변환하는 커스텀 캐스트가 필요할 수 있습니다.

이런 인바운드 전용 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이는 `set` 메서드만 요구합니다. `make:cast` Artisan 명령에 `--inbound` 옵션을 사용해 인바운드 전용 캐스트 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

인바운드 전용 캐스트의 대표적인 예는 "해싱" 캐스트입니다. 다음은 해싱 알고리즘을 통해 입력값을 해싱하는 예제입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * 새로운 캐스트 클래스 인스턴스 생성자.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장을 위해 주어진 값을 준비합니다.
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
### 캐스트 파라미터 (Cast Parameters)

모델에 커스텀 캐스트를 지정할 때 클래스명과 함께 `:`로 구분하여 캐스트 인자를 전달할 수 있습니다. 여러 인자는 쉼표로 구분합니다. 이 인자들은 캐스트 클래스 생성자에 전달됩니다:

```php
/**
 * 캐스팅할 속성을 반환합니다.
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
### 캐스트 값 비교하기 (Comparing Cast Values)

두 캐스트된 값이 서로 다른지 판단하고 싶다면, 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 `compare` 메서드를 요구하며, 주어진 두 값이 같으면 `true`, 다르면 `false`를 반환해야 합니다.

이를 통해 Eloquent가 어떤 값이 변경됐다고 인식해 데이터베이스에 업데이트할지 세밀하게 제어할 수 있습니다:

```php
/**
 * 주어진 값들이 같은지 판단합니다.
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
### 캐스터블 (Castables)

애플리케이션의 값 객체가 자체 캐스트 클래스를 정의하도록 허용하고 싶을 수 있습니다. 이 경우 모델에 커스텀 캐스트 클래스를 직접 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는 반드시 `castUsing` 메서드를 정의해야 하며, 이 메서드는 이 값 객체를 캐스팅하는 데 사용할 커스텀 캐스트 클래스명을 반환해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * 이 캐스트 대상에 대해 사용하는 캐스터 클래스명을 반환합니다.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

`Castable` 클래스를 사용할 때도 `casts` 메서드에서 인자를 함께 전달할 수 있으며, 이 인자는 `castUsing` 메서드에 전달됩니다:

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
#### 캐스터블과 익명 캐스트 클래스

PHP [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 캐스터블을 결합해, 값 객체와 캐스팅 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현하는 익명 클래스를 반환하면 됩니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 캐스팅에 사용할 캐스터 클래스를 반환합니다.
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