# Eloquent: 변경자와 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [열거형 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열/JSON 직렬화](#array-json-serialization)
    - [입력값 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블(Castable)](#castables)

<a name="introduction"></a>
## 소개

접근자(accessor), 변경자(mutator), 그리고 속성(attribute) 캐스팅 기능을 활용하면 Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 해당 값을 변환할 수 있습니다. 예를 들어, [Laravel 암호화기](/docs/12.x/encryption)를 이용해 데이터베이스에 값을 저장할 때는 암호화하고, Eloquent 모델에서 해당 속성에 접근하면 자동으로 복호화하는 방식이 가능합니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때마다 배열로 자동 변환되도록 할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성에 접근할 때 해당 값을 변환합니다. 접근자를 정의하려면, 모델에 해당 속성을 나타내는 protected 메서드를 생성하면 됩니다. 이 메서드 이름은 실제 모델 속성 또는 데이터베이스 컬럼명을 '카멜 케이스(camel case)'로 변환한 형태와 일치해야 합니다.

아래 예시에서는 `first_name` 속성에 대한 접근자를 정의합니다. Eloquent가 `first_name` 속성의 값을 가져올 때 이 접근자가 자동으로 호출됩니다. 모든 접근자/변경자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다.

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

모든 접근자 메서드는 속성의 '접근 방식'과 필요하다면 '변경 방식'을 정의하는 `Attribute` 인스턴스를 반환해야 합니다. 위 예시에서는 속성에 접근하는 방법만 정의하고 있으며, 이를 위해 `Attribute` 클래스의 생성자에 `get` 인자를 전달하고 있습니다.

보시는 것처럼, 컬럼의 원래 값이 접근자로 전달되기 때문에 값을 자유롭게 조작하고 반환할 수 있습니다. 접근자의 값을 사용하려면 모델 인스턴스에서 단순히 `first_name` 속성을 읽으면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이런 방식으로 계산된(computed) 값을 모델의 배열/JSON 표현에 포함하고 싶다면, [별도로 값을 추가해야 합니다](/docs/12.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

경우에 따라 접근자가 여러 모델 속성 값을 조합해 하나의 '값 객체(value object)'를 만들어야 할 수 있습니다. 이럴 때는 `get` 클로저의 두 번째 인수로 `$attributes`를 받을 수 있습니다. 이 배열에는 모델의 현재 전체 속성 정보가 담겨 자동으로 전달됩니다.

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

접근자에서 값 객체를 반환할 때, 값 객체에 변경이 생기면 모델이 저장될 때 해당 변화를 모델에 자동으로 반영합니다. 이는 Eloquent가 접근자가 반환한 인스턴스를 내부적으로 기억했다가, 같은 접근자가 재호출될 때마다 같은 인스턴스를 반환하기 때문에 가능한 동작입니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 문자열이나 불린값처럼 원시값(primitive value)에 대해 캐싱을 활성화하고 싶을 때도 있습니다. 특히, 값 변환 작업이 복잡한 경우라면 성능 향상을 위해 캐싱을 활용할 수 있습니다. 이를 위해 접근자 정의 시 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 속성의 객체 캐싱 동작을 사용하지 않도록 하려면 `withoutObjectCaching` 메서드를 사용할 수 있습니다.

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

변경자는 Eloquent 속성의 값을 저장(설정)할 때 변환을 담당합니다. 변경자를 정의하려면, 속성 정의 시 `set` 인자를 전달하면 됩니다. 이번에는 `first_name` 속성에 대한 변경자를 정의해보겠습니다. 모델에서 `first_name` 속성 값을 설정하면 이 변경자가 자동으로 호출됩니다.

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

변경자 클로저에는 속성에 저장될 값이 전달되며, 이 값을 자유롭게 변환하여 반환할 수 있습니다. 변경자를 실제로 사용하려면 Eloquent 모델의 `first_name` 속성에 값을 할당하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예시에서 `set` 콜백은 `Sally` 값을 인수로 받아서, 이름에 `strtolower` 함수를 적용한 후 결과를 모델의 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 한 번에 변경하기

때로는 변경자가 모델의 여러 속성을 한 번에 설정해야 할 수 있습니다. 이런 경우, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 속성 또는 데이터베이스 컬럼 이름과 일치해야 합니다.

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

속성 캐스팅은 접근자나 변경자처럼 별도의 메서드를 추가로 만들 필요 없이 속성을 변환하는 방법을 제공합니다. 즉, 모델의 `casts` 메서드를 이용해 자주 쓰는 데이터 타입으로 속성을 변환할 수 있습니다.

`casts` 메서드는 캐스팅할 속성명을 키로, 원하는 변환 타입을 값으로 갖는 배열을 반환해야 합니다. 지원되는 캐스팅 타입은 다음과 같습니다.

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

속성 캐스팅을 예로 들어, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 항상 불린(boolean) 값으로 다루고자 하면 다음과처럼 구현할 수 있습니다.

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

이렇게 캐스팅을 정의하면, 데이터베이스에 정수로 저장되어 있더라도 `is_admin` 속성에 접근할 때는 항상 불린 값으로 자동 변환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임 중 임시로 새로운 캐스팅을 추가해야 한다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드를 통해 기존에 정의된 캐스팅에 새로운 설정을 합칠 수 있습니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또, 리레이션십 이름과 같은 속성명에 캐스팅(또는 속성 자체)을 정의하거나, 모델의 기본 키 이름에 캐스트를 적용해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

모델 속성을 [fluent Illuminate\Support\Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 캐스팅하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용할 수 있습니다.

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

`array` 캐스팅은 직렬화된 JSON 데이터를 컬럼에 저장할 때 특히 유용합니다. 예를 들어, 데이터베이스의 `JSON` 또는 `TEXT` 타입 필드에 직렬화된 JSON 데이터가 저장되어 있다면, 해당 속성에 `array` 캐스팅을 지정하면 모델에서 접근 시 자동으로 PHP 배열로 역직렬화됩니다.

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

이제 캐스트를 정의한 후에는, `options` 속성에 접근할 때마다 JSON이 PHP 배열로 자동 변환됩니다. 또한 `options` 속성에 배열을 할당하면, 해당 값은 JSON 형식으로 자동 직렬화되어 데이터베이스에 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

더 간단한 문법으로 JSON 속성의 단일 필드만 업데이트하려면, [속성을 대량 할당 가능하게](/docs/12.x/eloquent#mass-assignment-json-columns) 한 뒤 `update` 메서드를 호출할 때 `->` 연산자를 사용할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 JSON으로 저장할 때 유니코드 문자가 이스케이프되지 않도록 하려면 `json:unicode` 캐스팅을 사용할 수 있습니다.

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

기본 `array` 캐스팅만으로 충분한 경우도 많지만, 몇 가지 제약이 있습니다. `array` 캐스팅의 경우, 반환값이 단순한 원시 배열이기 때문에 배열 요소를 직접 변경하면 PHP 오류가 발생할 수 있습니다. 예를 들어 아래 코드는 에러를 발생시킵니다.

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이런 문제를 해결하기 위해, 라라벨은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스 인스턴스로 변환하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 [커스텀 캐스트](#custom-casts)를 이용해 구현되어 있으며, 변경된 객체를 지능적으로 캐시하고 변환하므로 배열 원소만 개별적으로 수정해도 PHP 오류가 발생하지 않습니다. `AsArrayObject` 캐스트를 사용하려면 속성에 지정해주면 됩니다.

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

마찬가지로, 라라벨은 JSON 속성을 Laravel [컬렉션](/docs/12.x/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공합니다.

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

`AsCollection` 캐스트가 Laravel 기본 컬렉션 클래스가 아닌, 직접 정의한 커스텀 컬렉션 클래스를 사용하도록 하려면 캐스트 인자로 컬렉션 클래스명을 전달하면 됩니다.

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

`of` 메서드를 통해 컬렉션의 [mapInto 메서드](/docs/12.x/collections#method-mapinto)를 사용하여 컬렉션의 각 요소를 특정 클래스 인스턴스로 자동 변환할 수 있습니다.

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

컬렉션을 객체로 매핑할 때, 매핑 대상 객체는 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 모두 구현해야 하며, 각각 데이터베이스에 JSON으로 직렬화할 때 인스턴스를 어떻게 표현할 지를 정의합니다.

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

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP의 `DateTime` 클래스를 확장한 것으로 다양한 유용한 메서드를 제공합니다. 추가적인 날짜 속성도, 모델의 `casts` 메서드에서 날짜 관련 캐스트를 지정해주면 됩니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스팅 타입을 사용합니다.

`date`나 `datetime` 캐스트를 정의할 때는 날짜 포맷을 함께 지정할 수도 있습니다. 이 포맷은 [모델이 배열 또는 JSON으로 직렬화될 때](/docs/12.x/eloquent-serialization) 적용됩니다.

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

데이터베이스 컬럼이 날짜로 캐스트된 경우, 해당 모델 속성값을 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스로 자유롭게 지정할 수 있습니다. Eloquent가 알아서 포맷에 맞게 변환하여 데이터베이스에 저장합니다.

모델의 모든 날짜 속성의 기본 직렬화 포맷을 변경하고 싶다면, 모델에 `serializeDate` 메서드를 정의하면 됩니다. 이 설정은 데이터베이스에 실제로 저장되는 형식이 아닌, 배열/JSON 직렬화 시에만 영향을 줍니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜를 데이터베이스에 실제로 저장할 때 사용할 포맷을 지정하려면, `$dateFormat` 프로퍼티를 모델에 정의하세요.

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

기본적으로 `date`와 `datetime` 캐스팅은 애플리케이션의 `timezone` 설정 옵션에 지정된 타임존과 관계없이 날짜를 UTC ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)의 문자열로 직렬화합니다. 이 직렬화 형식의 사용과, 애플리케이션의 날짜를 UTC 타임존에 저장(즉, `timezone` 설정을 기본값인 `UTC`에서 변경하지 않음)할 것을 강력히 권장합니다. 애플리케이션 전체에 걸쳐 UTC 타임존을 일관적으로 사용하면, PHP 및 JavaScript로 작성된 다른 날짜 관련 라이브러리와의 호환성이 극대화됩니다.

만약 `datetime:Y-m-d H:i:s`와 같이 커스텀 포맷을 `date` 또는 `datetime` 캐스트에 적용하면, Carbon 인스턴스 내부의 타임존이 날짜 직렬화 시 사용됩니다. 일반적으로 이는 애플리케이션의 `timezone` 설정이 지정한 타임존이 됩니다. 하지만, `created_at`과 `updated_at`처럼 `timestamp` 컬럼의 경우에는 예외이며, 애플리케이션의 타임존 설정과 관계없이 항상 UTC로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성(attribute) 값을 PHP의 [열거형(Enums)](https://www.php.net/manual/en/language.enumerations.backed.php)으로도 캐스팅할 수 있습니다. 이를 위해 모델의 `casts` 메서드에서 캐스팅할 속성과 Enum을 지정합니다:

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

이렇게 캐스트를 정의하면, 해당 속성에 접근하거나 값을 할당할 때 자동으로 Enum으로 변환됩니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

때때로 하나의 컬럼에 Enum 값들의 배열을 저장해야 할 수도 있습니다. 이때는 라라벨에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용하면 됩니다:

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
### 암호화 캐스팅

`encrypted` 캐스트는 라라벨의 내장 [암호화](/docs/12.x/encryption) 기능을 이용해 모델의 속성 값을 암호화합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트들은 이름에서 알 수 있듯이 일반(암호화되지 않은) 캐스트들과 같이 동작하지만, 실제로는 데이터베이스에 저장될 때 암호화된 값이 저장됩니다.

암호화된 텍스트의 길이는 예측할 수 없으며 평문보다 길어질 수 있으므로, 속성이 저장될 데이터베이스 컬럼의 타입이 반드시 `TEXT`이거나 그 이상이어야 합니다. 또한 데이터베이스에 암호화된 값이 저장되므로, 해당 속성에 대해 쿼리나 검색을 직접 수행하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 키 롤테이션(Key Rotation)

라라벨은 애플리케이션의 `app` 설정 파일에 지정된 `key` 구성 값(일반적으로 `APP_KEY` 환경 변수)을 사용해 문자열을 암호화합니다. 만약 암호화 키를 변경해야 할 경우, 새 키로 암호화된 속성들을 수동으로 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

테이블에서 원시 값을 조회(select)할 때 등, 쿼리 실행 시점에 캐스팅을 적용하고 싶은 경우가 있습니다. 예를 들어, 아래 쿼리를 살펴봅니다:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

위 쿼리 결과의 `last_posted_at` 속성은 단순 문자열로 반환됩니다. 이 속성에 쿼리 실행 시점에 `datetime` 캐스트를 적용할 수 있으면 좋을 것입니다. 다행히, `withCasts` 메서드를 사용하면 가능합니다:

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

라라벨에는 다양한 내장 캐스트 타입이 존재하지만, 직접 커스텀 캐스트 타입을 정의해야 할 때도 있습니다. 캐스트 클래스를 생성하려면 `make:cast` 아티즌 명령어를 실행하세요. 새로 생성된 캐스트 클래스는 `app/Casts` 디렉터리에 위치합니다:

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하는 클래스는 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스트 값으로 변환하며, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환합니다. 예시로, 내장 `json` 캐스트 타입을 커스텀 캐스트로 재구현해 보겠습니다:

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

커스텀 캐스트 타입을 정의한 후에는 해당 클래스명을 사용하여 모델 속성에 캐스트를 적용할 수 있습니다:

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
### 값 객체 캐스팅(Value Object Casting)

캐스트는 단순한 기본 데이터 타입(primitive type)뿐 아니라 객체(object)로도 변환할 수 있습니다. 객체로의 커스텀 캐스팅을 정의하는 방법은 기본 타입으로 캐스팅할 때와 비슷합니다. 다만, 값 객체가 두 개 이상의 데이터베이스 컬럼과 연결된다면 `set` 메서드는 키/값 쌍의 배열을 반환해야 하고, 하나의 컬럼에만 매핑된다면 저장 가능한 하나의 값만 반환하면 됩니다.

예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 변환하는 커스텀 캐스트 클래스를 만들어보겠습니다. 이때 `Address` 값 객체는 `lineOne`과 `lineTwo`라는 두 개의 public 속성이 있다고 가정합니다:

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

값 객체로 캐스팅할 경우, 값 객체에서 발생한 변경 사항은 모델을 저장하기 전 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이 있다면, 값 객체에 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 반드시 구현해 주세요.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 접근되어 해석(resolve)되면, Eloquent는 해당 객체를 캐싱합니다. 따라서 한 번 접근한 후 다시 속성에 접근하면 동일한 객체 인스턴스가 반환됩니다.

커스텀 캐스트 클래스에서 이런 객체 캐싱 기능을 비활성화하려면, 클래스 내에 public한 `withoutObjectCaching` 속성을 선언하면 됩니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환할 때, 커스텀 캐스트 값 객체는 일반적으로 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하고 있다면 자동으로 직렬화됩니다. 하지만 외부 라이브러리에서 제공하는 값 객체 등, 직접 해당 인터페이스를 추가할 수 없는 상황도 있습니다.

이 경우, 커스텀 캐스트 클래스에서 값 객체를 직접 직렬화하도록 지정할 수 있습니다. 방법은 커스텀 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하도록 하는 것입니다. 이 인터페이스는 클래스 내에 값을 직렬화할 `serialize` 메서드가 있어야 함을 의미합니다. 예시는 다음과 같습니다:

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
### 인바운드(Inbound) 캐스팅

때때로 모델의 속성에 값을 할당(`set`)할 때만 변환이 필요하고, 모델에서 속성을 조회(`get`)할 때는 아무 작업도 필요 없는 커스텀 캐스트가 필요할 수 있습니다.

이 경우에는 `CastsInboundAttributes` 인터페이스만 구현하면 됩니다. 이 인터페이스는 `set` 메서드만 정의하면 됩니다. 인바운드 전용 캐스트 클래스를 생성하려면 `make:cast` 아티즌 명령어에 `--inbound` 옵션을 붙입니다:

```shell
php artisan make:cast AsHash --inbound
```

인바운드 전용 캐스트의 전형적인 예는 "해시" 캐스트입니다. 예를 들어, 주어진 알고리즘을 이용해 값을 해싱하는 캐스트를 정의할 수 있습니다:

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

커스텀 캐스트를 모델에 적용할 때, 클래스명 뒤에 `:` 문자로 구분해 파라미터를 지정할 수 있습니다. 여러 파라미터가 필요한 경우 쉼표(,)로 구분하며, 이 파라미터들은 캐스트 클래스 생성자에 전달됩니다:

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

두 개의 캐스트 값이 변경되었는지 여부를 어떻게 비교할지 직접 정의하려면, 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이를 통해 Eloquent에서 값이 변경되었는지 세밀하게 제어할 수 있으며, 모델이 업데이트될 때 어떤 값이 데이터베이스에 저장될지 결정할 수 있습니다.

이 인터페이스는 클래스에 `compare` 메서드가 있어야 하며, 두 값이 같다고 판단되면 `true`를 반환해야 합니다:

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

애플리케이션의 값 객체가 자체적으로 커스텀 캐스트 클래스를 지정하도록 하고 싶을 수도 있습니다. 이때는 모델에서 커스텀 캐스트 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 할당하면 됩니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현하는 객체는 반드시 `castUsing` 메서드를 정의해야 하며, 이 메서드는 커스팅에 사용될 커스텀 캐스터 클래스명을 반환해야 합니다:

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

`Castable` 클래스를 사용할 때도, `casts` 메서드 정의에서 인자를 전달할 수 있습니다. 이 인자들은 `castUsing` 메서드로 전달됩니다:

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

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합하면, 값 객체와 해당 캐스팅 로직을 하나의 캐스터블 객체로서 정의할 수도 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

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