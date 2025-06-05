# Eloquent: 접근자, 변경자 & 캐스팅 (Eloquent: Mutators & Casting)

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
    - [입력값 캐스팅](#inbound-casting)
    - [캐스트 매개변수](#cast-parameters)
    - [캐스터블](#castables)

<a name="introduction"></a>
## 소개

접근자(accessor), 변경자(mutator), 그리고 속성 캐스팅(attribute casting)을 사용하면 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 그 값을 원하는 형태로 변환할 수 있습니다. 예를 들어, [라라벨 암호화기](/docs/12.x/encryption)를 사용하여 데이터베이스에 저장할 때 값을 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화하도록 할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 자동으로 PHP 배열로 변환되도록 할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성 값에 접근할 때 그 값을 변환합니다. 접근자를 정의하려면, 모델에 접근 가능한 속성 이름에 해당하는 protected 메서드를 생성하면 됩니다. 이 메서드 이름은 기본적으로 실제 모델 속성/데이터베이스 컬럼 이름을 "카멜 케이스(camel case)"로 변환한 형식을 따릅니다.

예시로, `first_name` 속성에 대한 접근자를 정의해보겠습니다. 이 접근자는 Eloquent에서 `first_name` 속성을 조회할 때 자동으로 호출됩니다. 모든 속성 접근자/변경자 메서드는 반드시 반환 타입으로 `Illuminate\Database\Eloquent\Casts\Attribute`를 명시해야 합니다.

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

접근자 메서드는 모두 속성을 어떻게 접근(조회)하고, 필요하다면 어떻게 변경(설정)할지를 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예시에서는 속성을 어떻게 조회할지(`get`)만 정의하였습니다. 이렇게 하려면, `Attribute` 클래스 생성자에 `get` 인수를 전달하면 됩니다.

보시는 것처럼, 컬럼의 원래 값이 접근자로 전달되어 값을 조작하거나 가공한 뒤 반환할 수 있습니다. 접근자 값을 사용하려면 모델 인스턴스에서 해당 속성을 직접 조회하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 접근자를 통해 계산된 속성 값을 모델의 배열/JSON 표현에 포함시키고 싶다면, [속성 값을 JSON에 추가하는 방법](/docs/12.x/eloquent-serialization#appending-values-to-json)을 참고해 추가로 설정해야 합니다.

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

때로는 접근자에서 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 수도 있습니다. 이럴 때는 `get` 클로저에 두 번째 인수 `$attributes`를 받을 수 있으며, 여기에는 해당 모델의 모든 현재 속성들이 배열로 전달됩니다.

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

접근자에서 값 객체를 반환할 경우, 이 객체가 변경되면 모델이 저장되기 전에 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자에서 반환된 인스턴스를 내부적으로 보관하면서, 매번 같은 인스턴스를 반환하기 때문입니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

반면, 문자열이나 불리언처럼 단순한 값도 계산 비용이 크다면 캐싱을 활성화하고 싶을 수 있습니다. 이럴 때는 접근자 정의 시 `shouldCache` 메서드를 호출할 수 있습니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 객체 캐싱 동작을 비활성화하고 싶다면 `withoutObjectCaching` 메서드를 호출하면 됩니다.

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

변경자는 Eloquent 속성 값이 할당될 때 그 값을 변환합니다. 변경자를 정의하려면, 속성 정의 시 `set` 인수를 전달합니다. 아래는 `first_name` 속성에 대한 변경자를 정의한 예시입니다. 이 변경자는 모델의 `first_name` 속성에 값을 할당할 때 자동으로 호출됩니다.

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

변경자 클로저는 속성에 할당될 값이 인수로 전달되기 때문에, 이 값을 원하는 방식으로 가공한 후 결과 값을 반환하면 됩니다. 변경자를 사용하려면 Eloquent 모델에 `first_name` 속성을 할당하기만 하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예시에서 `set` 콜백은 `Sally` 값을 인수로 받아, `strtolower` 함수를 적용한 후 그 결과를 모델의 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변경하기

변경자에서 기본 모델의 여러 속성을 한 번에 설정해야 할 때도 있습니다. 이럴 때는 `set` 클로저에서 배열을 반환하면 됩니다. 반환하는 배열의 각 키는 실제 모델 속성/DB 컬럼명을 의미합니다.

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
## 속성 캐스팅

속성 캐스팅(attribute casting)은 접근자/변경자와 유사하지만, 별도의 메서드를 정의하지 않고 모델의 `casts` 메서드만으로 속성 값을 일반 데이터 타입으로 쉽게 변환할 수 있도록 해줍니다.

`casts` 메서드는 반환값으로 속성명을 키로, 캐스트할 타입명을 값으로 가지는 배열을 반환해야 합니다. 지원되는 캐스트 타입은 아래와 같습니다.

<div class="content-list" markdown="1">

- `array`
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

속성 캐스팅의 사용 예시로, 데이터베이스에 정수형(`0` 또는 `1`)으로 저장된 `is_admin` 속성을 불리언 값으로 캐스팅해 보겠습니다.

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

이렇게 캐스트를 정의하면, 데이터베이스에 정수로 저장되어 있더라도 모델에서 `is_admin` 속성에 접근하면 항상 불리언 값으로 변환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 일시적으로 새로운 캐스트를 추가하고 싶다면, `mergeCasts` 메서드를 사용할 수 있습니다. 이 캐스트 정의는 이미 모델에 정의된 캐스트에 덧붙여집니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null`인 속성에는 캐스팅이 적용되지 않습니다. 또한, 관계(relationship) 이름 또는 모델의 기본 키와 이름이 같은 속성에 캐스트를 지정하지 않아야 하며, 관계 속성에 캐스트를 정의해서도 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

모델 속성을 [플루언트한 Illuminate\Support\Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 캐스팅하고 싶다면 `Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용할 수 있습니다.

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

`array` 캐스팅은 직렬화된 JSON이 저장된 컬럼을 다룰 때 특히 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입의 필드에 직렬화된 JSON이 저장되어 있다면, 해당 속성에 `array` 캐스팅을 지정하면 Eloquent 모델에서 접근할 때 자동으로 PHP 배열로 역직렬화됩니다.

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

캐스트를 정의하면, 이제 `options` 속성에 접근할 때마다 자동으로 JSON이 PHP 배열로 변환됩니다. 또한, `options` 속성에 값을 할당할 때는 지정한 배열이 자동으로 JSON으로 직렬화되어 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 간결하게 업데이트하고 싶을 경우, [속성을 일괄 할당 가능하도록](/docs/12.x/eloquent#mass-assignment-json-columns) 설정한 후 `->` 연산자를 활용해 `update` 메서드를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 Unicode

배열 속성을 이스케이프되지 않은(unescaped) 유니코드 문자 형태의 JSON으로 저장하고 싶다면, `json:unicode` 캐스팅을 사용할 수 있습니다.

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
#### ArrayObject 및 Collection 캐스팅

일반적인 `array` 캐스팅으로도 충분한 경우가 많지만, 몇 가지 단점도 있습니다. 예를 들어, `array` 캐스팅은 원시 타입을 반환하기 때문에 배열의 오프셋을 직접 변경하면 PHP 오류가 발생할 수 있습니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제 해결을 위해 라라벨은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환해주는 `AsArrayObject` 캐스팅을 제공합니다. 이는 라라벨의 [커스텀 캐스트](#custom-casts) 기능을 사용해 구현되며, 내부적으로 객체의 변형을 캐싱 및 관리해 배열 오프셋 변경도 오류 없이 처리할 수 있습니다. 사용하려면 속성에 해당 캐스트를 지정하면 됩니다.

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

마찬가지로, 라라벨에서는 JSON 속성을 라라벨 [컬렉션](/docs/12.x/collections) 인스턴스로 변환해주는 `AsCollection` 캐스팅도 지원합니다.

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

`AsCollection` 캐스트로 변환할 때 라라벨의 기본 컬렉션 클래스 대신 사용자가 정의한 커스텀 컬렉션 클래스를 사용하고 싶다면, 캐스트 인수로 컬렉션 클래스명을 전달할 수 있습니다.

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

`of` 메서드를 사용하면 컬렉션 내부 아이템을 [mapInto 메서드](/docs/12.x/collections#method-mapinto)를 사용해 특정 클래스 인스턴스로 변환할 수도 있습니다.

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

컬렉션을 객체로 매핑할 경우, 객체는 데이터베이스에 JSON으로 직렬화될 때 그 형식을 정의하기 위해 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 반드시 구현해야 합니다.

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

<a name="date-casting"></a>
### 날짜 캐스팅

Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 자동으로 변환해줍니다. Carbon은 PHP의 `DateTime` 클래스를 상속하며 다양한 유틸리티 메서드를 제공합니다. 추가적인 날짜 속성도 모델의 `casts` 메서드에 날짜 캐스트를 더해 캐스팅할 수 있으며, 일반적으로는 `datetime` 또는 `immutable_datetime` 캐스트 타입을 사용합니다.

`date`나 `datetime` 캐스트를 정의할 때 날짜 포맷도 지정할 수 있습니다. 이 포맷은 [모델이 배열 또는 JSON으로 직렬화](/docs/12.x/eloquent-serialization)될 때 사용됩니다.

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

날짜로 캐스팅된 컬럼에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 할당할 수 있으며, 값은 자동으로 적합한 형태로 데이터베이스에 저장됩니다.

모델의 모든 날짜가 기본적으로 어떻게 직렬화되는지 전역적으로 지정하고 싶다면, 모델에 `serializeDate` 메서드를 정의할 수 있습니다. 이 메서드는 데이터베이스 저장 방식에는 영향을 주지 않습니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜를 실제 데이터베이스에 저장할 때 사용할 포맷을 지정하려면, 모델에 `$dateFormat` 속성을 정의하면 됩니다.

```php
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>

#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스트는, 애플리케이션의 `timezone` 설정값에 관계없이, 날짜를 UTC의 ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화합니다. 이러한 직렬화 포맷을 항상 사용하고, 애플리케이션의 날짜 역시 기본값인 `UTC` 타임존에 두는 것을 강력히 권장합니다. 애플리케이션 전체에서 UTC 타임존을 일관되게 활용하면, PHP와 JavaScript 등 다른 날짜 처리 라이브러리와의 호환성이 극대화됩니다.

만약 `datetime:Y-m-d H:i:s`와 같이 `date`나 `datetime` 캐스트에 커스텀 포맷을 지정하는 경우, 날짜 직렬화에는 Carbon 인스턴스의 내부 타임존이 사용됩니다. 일반적으로 이는 애플리케이션의 `timezone` 설정값이 됩니다. 단, `created_at`이나 `updated_at`과 같은 `timestamp` 타입의 컬럼은 이 규칙의 예외이며, 애플리케이션 타임존 설정과 무관하게 UTC로 항상 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent에서는 속성 값을 PHP [Enum(열거형)](https://www.php.net/manual/en/language.enumerations.backed.php)으로도 캐스팅할 수 있습니다. 이를 위해 모델의 `casts` 메서드에서, 캐스트할 속성과 Enum을 지정하면 됩니다.

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성 리스트를 반환합니다.
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

캐스트를 지정하면, 해당 속성은 접근하거나 저장할 때 자동으로 Enum 인스턴스로 변환됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

때로는 하나의 컬럼에 Enum 값의 배열을 저장해야 할 수 있습니다. 이럴 때는 라라벨에서 제공하는 `AsEnumArrayObject`나 `AsEnumCollection` 캐스트를 활용할 수 있습니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅할 속성 리스트를 반환합니다.
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

`encrypted` 캐스트는 라라벨의 내장 [암호화](/docs/12.x/encryption) 기능을 이용해 모델 속성 값을 암호화합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트는 각각의 비암호화 캐스트처럼 동작하지만, 데이터베이스에 저장될 때는 값이 암호화된다는 차이가 있습니다.

암호화된 텍스트는 평문보다 길이가 길고 예측할 수 없으므로, 관련 컬럼은 반드시 `TEXT` 타입(또는 그 이상)이어야 합니다. 또한 값이 암호화되어 저장되므로, 암호화된 속성 값에 대해 쿼리나 검색을 할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

라라벨은 애플리케이션 설정 파일의 `key` 값(일반적으로는 `APP_KEY` 환경 변수)을 이용해 문자열을 암호화합니다. 만약 애플리케이션의 암호화 키를 변경해야 한다면, 새 키로 암호화할 수 있도록 암호화된 속성들을 직접 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅(Query Time Casting)

쿼리를 실행하면서 임의로 캐스팅을 적용해야 할 때가 있습니다. 예를 들어, 테이블에서 원시 값을 조회하는 경우입니다. 아래 예제를 확인해 보겠습니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리 결과의 `last_posted_at` 속성은 단순한 문자열이 됩니다. 만약 쿼리 실행 시점에 `datetime` 캐스트를 적용하고 싶다면, `withCasts` 메서드를 사용할 수 있습니다.

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
## 커스텀 캐스트(Custom Casts)

라라벨에는 다양한 기본 내장 캐스트 타입이 있지만, 상황에 따라 직접 커스텀 캐스트 타입을 정의해야 할 때가 있습니다. 커스텀 캐스트를 생성하려면 `make:cast` 아티즌 명령어를 실행합니다. 새 캐스트 클래스는 `app/Casts` 디렉토리에 생성됩니다.

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하는 클래스는 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스에서 조회한 원시 값을 캐스트 값으로 변환하고, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환합니다. 예를 들어, 기본 내장 `json` 캐스트를 커스텀 캐스트로 다시 구현할 수 있습니다.

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
     * 저장용 값을 준비합니다.
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

커스텀 캐스트 타입을 정의한 후에는, 클래스명을 이용해 모델 속성에 캐스트를 지정하면 됩니다.

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 리스트를 반환합니다.
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

Eloquent의 캐스팅은 원시 타입뿐만 아니라, 객체로의 변환도 지원합니다. 여러 컬럼의 값을 하나의 값 객체(value object)로 변환하는 커스텀 캐스트도 정의할 수 있습니다.커스텀 객체가 여러 컬럼 값을 관리한다면, `set` 메서드는 키-값 쌍의 배열을 반환하여 각 컬럼에 값을 저장하고, 하나의 컬럼만 관리한다면 저장 가능한 값만 반환하면 됩니다.

예를 들어, 두 개의 컬럼 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의할 수 있습니다. 아래에서는 `Address` 값 객체가 `lineOne`, `lineTwo`라는 속성을 가진다고 가정합니다.

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
     * 저장용 값을 준비합니다.
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

값 객체로 캐스팅할 경우, 값 객체의 속성을 변경하면 모델에 자동으로 반영되어 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 해당 값 객체가 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현하고 있는지 확인하세요.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent가 내부적으로 캐싱합니다. 따라서 해당 속성을 다시 접근할 경우 항상 동일한 객체 인스턴스가 반환됩니다.

커스텀 캐스트 클래스의 이런 객체 캐싱 동작을 비활성화 하고 싶다면, 캐스트 클래스에 `withoutObjectCaching`라는 public 속성을 선언하고 `true`로 지정하면 됩니다.

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환할 때, 커스텀 캐스트의 값 객체도 일반적으로 직렬화됩니다(값 객체가 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현한 경우). 하지만, 외부 라이브러리에서 제공하는 값 객체를 사용하면 직접 이 인터페이스를 추가할 수 없기도 합니다.

이럴 때는 커스텀 캐스트 클래스에서 값 객체를 직렬화하도록 지정할 수 있습니다. 그러려면, 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메서드를 정의하면 됩니다. 이 메서드는 값 객체의 직렬화 형태를 반환해야 합니다.

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
### 인바운드 캐스팅(Inbound Casting)

가끔은 모델 속성에 값을 저장(set)할 때만 변환하고, 조회(get)할 때는 별도의 변환이 필요 없는 커스텀 캐스트가 필요할 때가 있습니다.

이런 인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, `set` 메서드만 정의하면 됩니다. 인바운드 전용 캐스트를 생성하려면, `make:cast` 아티즌 명령에 `--inbound` 옵션을 추가합니다.

```shell
php artisan make:cast AsHash --inbound
```

대표적인 인바운드 캐스트 예시는 "해시" 캐스트입니다. 예를 들어, 특정 알고리즘으로 값에 대해 해시를 적용하는 캐스트를 아래처럼 정의할 수 있습니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * 새로운 캐스트 클래스 인스턴스를 생성합니다.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장용 값을 준비합니다.
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

커스텀 캐스트를 모델에 적용할 때, 클래스명 뒤에 `:`로 구분하여 파라미터를 지정할 수 있습니다. 쉼표로 파라미터를 여러 개 전달할 수도 있습니다. 이 파라미터들은 캐스트 클래스의 생성자에 전달됩니다.

```php
/**
 * 캐스팅할 속성 리스트를 반환합니다.
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
### Castable(캐스터 제공 값 객체)

애플리케이션의 값 객체 자체가 커스텀 캐스트 클래스를 직접 지정할 수 있게 만들 수도 있습니다. 커스텀 캐스트 클래스를 모델이 아닌 값 객체 단에서 지정하려면, 그 값 객체 클래스가 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하도록 합니다.

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는, 실제로 캐스팅을 담당할 커스텀 캐스터 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * 이 캐스팅 대상에 사용할 캐스터 클래스명을 반환합니다.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

`Castable` 클래스를 사용할 때도, `casts` 메서드 정의에서 파라미터를 전달할 수 있습니다. 이 인자들은 `castUsing` 메서드로 전달됩니다.

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
#### Castable & 익명 캐스트 클래스(Anonymous Cast Classes)

"Castable"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하면, 값 객체와 캐스팅 로직을 하나의 객체 내부에 정의할 수 있습니다. 이를 위해, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하고, 그 익명 클래스가 `CastsAttributes` 인터페이스를 구현하도록 하면 됩니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 캐스팅 대상에 사용할 캐스터 클래스를 반환합니다.
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