# Eloquent: 변경자(Mutators) & 캐스팅(Casting) (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자(Accessors)와 변경자(Mutators)](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [입력값 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자(accessor), 변경자(mutator), 그리고 속성 캐스팅 기능을 활용하면, Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 값을 원하는 형태로 변환할 수 있습니다. 예를 들면, [라라벨 암호화기](/docs/12.x/encryption)를 이용해서 특정 값을 데이터베이스에 저장할 때 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화하도록 만들 수 있습니다. 또는, 데이터베이스에 저장되어 있는 JSON 문자열을 Eloquent 모델에서는 배열로 변환해서 사용할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자(Accessors)와 변경자(Mutators)

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자(accessor)는 Eloquent 모델 속성에 접근할 때 해당 값을 변환해주는 역할을 합니다. 접근자를 정의하려면, 모델에서 접근 가능한 속성을 나타내는 `protected` 메서드를 생성해야 합니다. 이 메서드명은 실제 모델 속성명(또는 데이터베이스 컬럼명)을 "카멜 케이스(camel case)"로 변환한 형태여야 합니다.

아래 예시에서는 `first_name` 속성에 대한 접근자를 정의합니다. 이 접근자는 Eloquent에서 `first_name` 속성 값을 가져올 때마다 자동으로 호출됩니다. 모든 속성 접근자/변경자 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다.

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

접근자 메서드는 모두 `Attribute` 인스턴스를 반환하며, 이 객체 안에 해당 속성을 어떻게 접근(조회)할지와, 선택적으로 어떻게 변경(저장)할지를 정의합니다. 위의 예시에서는 속성에 접근할 때만 동작하는 접근 방식을 정의하고 있습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 제공합니다.

보시다시피, 컬럼의 원래 값이 접근자로 전달되어 원하는 대로 가공 후 반환할 수 있습니다. 접근자 값을 가져오려면, 모델 인스턴스에서 해당 속성을 바로 접근하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 만약 이런 계산된 값들을 모델의 배열 또는 JSON 표현에 포함하고 싶다면, [별도로 속성을 추가(Append)해주어야 합니다](/docs/12.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

때로는 한 개의 접근자에서 여러 모델 속성을 조합해서 하나의 "값 객체(value object)"로 반환해야 할 경우도 있습니다. 이럴 때는 `get` 클로저의 두 번째 인자로 `$attributes`를 받을 수 있습니다. 이 값은 해당 모델 인스턴스의 모든 속성을 배열 형태로 제공합니다.

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

접근자에서 값 객체를 반환할 때, 해당 객체에 변경이 발생하면 모델을 저장하기 전에 자동으로 동기화됩니다. 이는 Eloquent가 접근자로 반환된 인스턴스를 내부적으로 계속 유지하기 때문에 가능하며, 접근자를 호출할 때마다 동일한 인스턴스를 반환합니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 문자열이나 불린처럼 단순한 값인 경우에도, 계산 비용이 비싼 작업이라면 캐싱을 활성화하고 싶을 때가 있습니다. 이럴 때는 접근자를 정의할 때 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 속성의 객체 캐싱 기능을 비활성화하고 싶다면, `withoutObjectCaching` 메서드를 호출해주면 됩니다.

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

변경자(mutator)는 Eloquent 모델의 속성 값을 저장하거나 설정할 때 값을 변환해줍니다. 변경자를 정의하려면 속성 정의 시 `set` 인자를 사용하면 됩니다. 여기서는 `first_name` 속성에 대한 변경자를 정의해보겠습니다. 이 변경자는 모델의 `first_name` 속성 값을 설정하려 할 때 자동으로 호출됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름과 상호작용합니다.
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

변경자 클로저에는 속성에 설정하려는 값이 전달되며, 이를 가공해 반환할 수 있습니다. 변경자를 사용하려면 Eloquent 모델에서 해당 속성을 설정만 해주면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예시에서는 `set` 콜백에 `Sally` 값이 전달되고, 변경자는 `strtolower` 함수를 적용해 변환된 값을 모델의 내부 `$attributes` 배열에 저장하게 됩니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 값 동시 변경하기

변경자에서 한 번에 여러 모델 속성 값을 설정하고 싶을 때는, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 실제 모델 속성명(또는 데이터베이스 컬럼명)과 일치해야 합니다.

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

속성 캐스팅(Attribute casting)은 접근자/변경자와 비슷하게, 모델에 별도 메서드를 정의할 필요 없이 속성 값을 원하는 타입으로 쉽게 변환해주는 기능입니다. 모델의 `casts` 메서드를 통해 여러 속성 값을 다양한 타입으로 자동 변환할 수 있습니다.

`casts` 메서드는 배열 형태로, 배열의 키는 캐스팅할 속성명이 되고, 값에는 변환할 타입을 지정합니다. 지원되는 캐스트 타입은 다음과 같습니다.

<div class="content-list" markdown="1">

- `array`
- `AsUri::class`
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

속성 캐스팅의 동작 방식을 이해하기 위해, 데이터베이스에서 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불린 타입으로 캐스팅하는 예시를 살펴보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록을 반환합니다.
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

이와 같이 캐스트를 정의하면, 데이터베이스에는 값이 정수로 저장되어 있어도, 모델에서 `is_admin` 속성에 접근할 때는 항상 불린 타입으로 변환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시로 새로운 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이렇게 추가한 캐스트 설정은 기존에 정의된 캐스트에 합쳐집니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 속성 값이 `null`일 경우에는 캐스팅이 적용되지 않습니다. 그리고, 관계 이름과 동일한 이름의 캐스트(또는 속성)를 정의하거나, 모델의 기본키에 캐스트를 지정하는 것은 절대 해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 모델 속성을 [유연한 Illuminate\Support\Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록을 반환합니다.
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

`array` 캐스트는, 데이터베이스 컬럼이 직렬화된 JSON 형태로 저장되는 경우에 매우 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입 칼럼이 있고, 그 안에 직렬화된 JSON 데이터가 있을 때 `array` 캐스트를 주면 이를 Eloquent 모델에서 자동으로 PHP 배열로 역직렬화해서 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록을 반환합니다.
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

이렇게 캐스트를 정의하면, `options` 속성에 접근할 때마다 자동으로 JSON이 PHP 배열로 변환되어 제공됩니다. 그리고 `options` 속성 값을 배열로 설정하면, 자동으로 JSON 문자열로 직렬화되어 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 특정 필드만 간단히 업데이트하고 싶을 때는 [속성 일괄 대입(mass assignment)](/docs/12.x/eloquent#mass-assignment-json-columns)를 사용할 수 있으며, `update` 메서드에서 `->` 연산자를 활용하면 됩니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드(Unicode)

배열 속성을 JSON으로 저장할 때, 유니코드(한글/일본어 등) 문자가 이스케이핑되지 않은 상태로 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다.

```php
/**
 * 캐스팅할 속성 목록을 반환합니다.
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
#### ArrayObject 및 컬렉션 캐스팅

일반적으로 `array` 캐스트만으로도 충분하지만, 이 방식에는 단점이 있습니다. `array` 캐스트는 원시 배열 타입을 반환하기 때문에, 배열의 일부 값을 직접 변경하려고 하면 PHP 에러가 발생할 수 있습니다. 예를 들어, 다음 코드는 PHP 에러를 유발합니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이런 문제를 해결하기 위해, 라라벨은 JSON 속성 값을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이는 라라벨의 [커스텀 캐스트](#custom-casts) 기능을 사용하여 구현되며, 라라벨이 변형된 객체를 지능적으로 캐싱/변환해 개별 부분(offset)을 직접 수정해도 PHP 에러가 발생하지 않습니다. 사용 방법은 다음과 같습니다.

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성 목록을 반환합니다.
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

마찬가지로, JSON 속성 값을 라라벨 [컬렉션](/docs/12.x/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공합니다.

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성 목록을 반환합니다.
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

`AsCollection` 캐스트를 쓸 때, 라라벨의 기본 컬렉션 클래스 대신 원하는 커스텀 컬렉션 클래스를 인스턴스화하려면, 캐스트 인자로 컬렉션 클래스명을 전달하면 됩니다.

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성 목록을 반환합니다.
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

`of` 메서드를 사용하면 컬렉션의 각 아이템을 [mapInto 메서드](/docs/12.x/collections#method-mapinto)를 통해 특정 클래스에 매핑할 수 있습니다.

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성 목록을 반환합니다.
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

컬렉션을 객체로 매핑할 때, 해당 객체는 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 반드시 구현해야 하며, 이를 통해 인스턴스를 데이터베이스에 JSON으로 직렬화하는 방법을 정의할 수 있습니다.

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
     * Option 인스턴스를 생성합니다.
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
     * JSON 직렬화를 위한 데이터 지정.
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
### 날짜 캐스팅

Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 객체로 변환해줍니다. Carbon은 PHP의 `DateTime` 클래스를 확장한 것이며, 다양한 편리한 메서드를 제공합니다. 추가적인 날짜 속성도, 모델의 `casts` 메서드에 캐스트 타입을 지정해주면 동일하게 다룰 수 있습니다. 일반적으로 날짜는 `datetime`이나 `immutable_datetime` 캐스트 타입으로 변환하는 것이 권장됩니다.

날짜/날짜시간 캐스트를 정의할 때, 원하는 날짜 포맷도 같이 지정할 수 있습니다. 이 포맷은 [모델을 배열 또는 JSON으로 직렬화할 때](/docs/12.x/eloquent-serialization) 사용됩니다.

```php
/**
 * 캐스팅할 속성 목록을 반환합니다.
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

날짜로 캐스팅된 컬럼은, 모델 속성 값에 유닉스 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime` 또는 `Carbon` 인스턴스를 설정할 수 있습니다. 이 값들은 데이터베이스에 저장될 때 자동으로 적절한 형식으로 변환됩니다.

모든 날짜 속성의 직렬화 기본 포맷을 변경하고 싶다면, 모델에 `serializeDate` 메서드를 정의할 수 있습니다. 이 메서드는 데이터베이스에 실제로 저장되는 날짜의 형식에는 영향을 주지 않습니다.

```php
/**
 * 배열/JSON 직렬화를 위한 날짜 포맷 지정
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

반대로, 실제로 데이터베이스에 저장할 날짜 형식을 지정하고 싶다면, 모델에 `$dateFormat` 속성을 선언하면 됩니다.

```php
/**
 * 모델의 날짜 컬럼 저장 형식
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>

#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스팅은 애플리케이션의 `timezone` 설정 옵션에 상관없이 날짜를 UTC ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)으로 직렬화합니다. 항상 이 포맷으로 직렬화하고, 애플리케이션의 날짜도 UTC 타임존으로 저장하는 것을 강력하게 권장합니다. 그러려면 애플리케이션의 `timezone` 설정 값을 기본값인 `UTC`에서 변경하지 않아야 합니다. 애플리케이션 전체에서 UTC 타임존을 일관되게 사용할 경우, PHP와 JavaScript로 작성된 각종 날짜 처리 라이브러리들과의 상호 운용성이 극대화됩니다.

만약 `date`나 `datetime` 캐스팅에 사용자 정의 포맷(예: `datetime:Y-m-d H:i:s`)을 적용하면, 날짜 직렬화 시 Carbon 인스턴스의 내부 타임존이 적용됩니다. 일반적으로 이 값은 애플리케이션의 `timezone` 설정 옵션에 지정된 타임존입니다. 하지만 `created_at`, `updated_at`과 같은 `timestamp` 컬럼은 이러한 동작의 예외이며, 애플리케이션의 타임존 설정과 무관하게 항상 UTC로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로도 캐스팅할 수 있습니다. 이를 위해 모델의 `casts` 메서드에서 해당 속성과 사용할 enum을 지정하면 됩니다.

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

이렇게 캐스트를 지정하면, 해당 속성을 읽고 쓸 때 자동으로 enum 타입으로 변환됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

경우에 따라 하나의 컬럼에 enum 값들의 배열을 저장해야 할 수도 있습니다. 이럴 때는 라라벨에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스팅을 활용할 수 있습니다.

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
### 암호화된 캐스팅

`encrypted` 캐스팅은 라라벨의 내장 [암호화](/docs/12.x/encryption) 기능을 이용하여 모델의 속성 값을 암호화합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스팅 타입도 보통(암호화되지 않은) 타입들과 사용법은 같지만, 해당 값이 DB에 저장될 때 암호화된다는 점만 다릅니다.

암호화된 문자열은 평문일 때보다 더 길고, 최종 길이도 예측할 수 없으므로 관련 데이터베이스 컬럼은 반드시 `TEXT` 타입이나 그보다 넓은 타입이어야 합니다. 게다가 값이 DB에 암호화되어 저장되므로, 암호화된 속성 값을 기준으로 쿼리하거나 검색하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

라라벨은 애플리케이션의 `app` 설정 파일의 `key` 설정값, 일반적으로는 `APP_KEY` 환경 변수를 사용해 문자열을 암호화합니다. 만약 암호화 키를 교체(로테이션)해야 한다면, 새 키를 적용한 뒤 기존의 암호화된 속성 값을 직접 새 키로 다시 암호화해주어야 합니다.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

간혹 쿼리를 실행할 때, 예를 들어 테이블에서 raw 값을 조회할 때 캐스팅을 적용하고 싶을 때도 있습니다. 예를 들어, 아래와 같은 쿼리를 살펴보겠습니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리의 결과로 얻는 `last_posted_at` 속성은 단순 문자열이 됩니다. 이 값에 `datetime` 캐스팅을 쿼리 시점에 적용할 수 있다면 더 편리할 것입니다. 다행히, `withCasts` 메서드를 사용하면 이 기능을 구현할 수 있습니다.

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
## 커스텀 캐스팅(Custom Casts)

라라벨에는 쓸모 있는 다양한 내장 캐스트 타입이 있지만, 때로는 여러분만의 커스텀 캐스트 타입을 필요로 할 수 있습니다. 이를 만들려면 `make:cast` 아티즌 명령어를 실행하세요. 새로 생성된 캐스트 클래스는 `app/Casts` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현한 클래스는 `get`과 `set` 메서드를 반드시 정의해야 합니다. `get` 메서드는 DB에서 읽은 원본 값을 변환해서 반환하고, `set` 메서드는 캐스트된 값을 DB에 저장 가능한 원시 값으로 변환해줍니다. 예시로 내장 `json` 캐스트를 커스텀 캐스트로 다시 구현해보겠습니다.

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

커스텀 캐스트 타입을 정의했다면, 이제 클래스명을 속성에 할당해서 사용할 수 있습니다.

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

기본 타입(숫자, 문자열 등)뿐 아니라, 객체로도 값을 캐스팅할 수 있습니다. 값 객체로의 커스텀 캐스트 구현 방법은 기본 타입에 대한 캐스팅과 거의 같지만, 만약 값 객체가 DB의 여러 컬럼에 걸쳐 있다면, `set` 메서드는 각각의 컬럼에 저장할 키/값 쌍 배열을 반환해야 합니다. 하나의 컬럼만 사용하는 경우라면, 단일 값을 반환하면 됩니다.

예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 만들어보겠습니다. 여기서 `Address` 값 객체는 `lineOne`, `lineTwo` 두 public 속성을 가진다고 가정합니다.

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

값 객체로 캐스팅할 때, 값 객체에 적용한 변경 내용은 모델이 저장되기 전에 자동으로 다시 동기화됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 해석될 때, Eloquent가 해당 객체를 캐싱합니다. 따라서 한 번 접근한 뒤 다시 접근해도 같은 객체 인스턴스가 반환됩니다.

만약 커스텀 캐스트 클래스의 이런 객체 캐싱을 비활성화하고 싶다면, 커스텀 캐스트 클래스에 public `withoutObjectCaching` 프로퍼티를 선언하면 됩니다.

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환하면, 커스텀 캐스트 값 객체도 일반적으로 직렬화됩니다. (단, 값 객체가 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현하는 경우.) 하지만 외부 라이브러리가 제공하는 값 객체는 이 인터페이스를 추가할 수 없는 경우도 있습니다.

이럴 때는 커스텀 캐스트 클래스가 직접 값을 직렬화하도록 지정할 수 있습니다. 그 방법은 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하는 것입니다. 이 인터페이스는 `serialize` 메서드가 존재해야 하며, 값 객체의 직렬화된 표현을 반환해야 합니다.

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
### 인바운드 캐스팅(Inbound Casting)

드물게, 모델에 값을 할당할 때만 값 변환이 필요하고 값을 읽을 때는 변환이 필요하지 않은 상황이 있습니다.

이런 인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `set` 메서드만 정의하면 됩니다. 또, `make:cast` 아티즌 명령에 `--inbound` 옵션을 주면 인바운드 전용 캐스트 클래스를 생성할 수 있습니다.

```shell
php artisan make:cast AsHash --inbound
```

인바운드 전용 캐스트의 대표적인 예는 '해싱' 캐스트입니다. 예를 들어, 인바운드 값을 지정한 알고리즘으로 해싱하는 캐스트를 다음과 같이 정의할 수 있습니다.

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
### 캐스팅 파라미터

모델에 커스텀 캐스트를 지정할 때, 클래스명 뒤에 `:`로 구분해서 파라미터도 지정할 수 있습니다. 여러 파라미터가 필요한 경우 콤마로 구분합니다. 지정된 파라미터는 캐스트 클래스의 생성자로 전달됩니다.

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

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션의 값 객체가 자신만의 커스텀 캐스트 클래스를 정의하게 하고 싶을 수 있습니다. 커스텀 캐스트 클래스를 모델에 직접 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 지정할 수 있습니다.

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현하는 객체는 반드시 `castUsing` 메서드를 정의해야 하며, 이 메서드는 해당 값 객체의 캐스팅/복원을 담당하는 커스텀 캐스터 클래스명을 반환해야 합니다.

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

`Castable` 클래스를 사용할 때도 `casts` 메서드 정의에서 인자를 함께 넘길 수 있습니다. 이 파라미터들은 `castUsing` 메서드를 통해 전달됩니다.

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

"캐스터블(Castable)"을 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 함께 쓰면, 값 객체와 그 값을 변환하는 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 이 방법은 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하는 방식으로 구현할 수 있습니다. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

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