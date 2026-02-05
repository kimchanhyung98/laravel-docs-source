# Eloquent: 접근자 & 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [이진(Binary) 캐스팅](#binary-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블(Castable)](#castables)

<a name="introduction"></a>
## 소개

접근자(accessor), 변경자(mutator), 그리고 속성(attribute) 캐스팅 기능을 활용하면 Eloquent 모델 인스턴스에서 속성 값을 조회할 때나 설정할 때 값을 자유롭게 변환할 수 있습니다. 예를 들어, [Laravel 암호화기](/docs/master/encryption)를 사용하여 데이터를 데이터베이스에 저장할 때는 암호화하고, Eloquent 모델에서 속성을 접근할 때는 자동으로 복호화하는 것이 가능합니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 자동 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자(accessor)는 Eloquent 속성 값을 접근할 때 자동으로 값을 변환하여 반환합니다. 접근자를 정의하려면, 모델에서 액세스하려는 속성을 나타내는 protected 메서드를 생성하면 됩니다. 이 메서드의 이름은 해당 속성(컬럼 이름)을 "카멜 케이스(camel case)"로 변환한 형태여야 합니다.

다음 예제에서는 `first_name` 속성에 대해 접근자를 정의합니다. Eloquent에서 `first_name` 속성 값을 조회할 때 이 접근자가 자동으로 호출됩니다. 모든 접근자/변경자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다:

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

접근자 메서드는 모두 속성의 접근 방식(및 필요에 따라 변경 방식)을 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예제에서는 속성을 접근하는 방법만 정의하고 있습니다. 이를 위해 `Attribute` 클래스의 생성자에 `get` 인자를 전달합니다.

보시다시피, 컬럼의 원래 값이 접근자에 전달되어 값을 조작 후 반환할 수 있습니다. 접근자의 값을 사용하려면 모델 인스턴스에서 해당 속성에 직접 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이렇게 계산된(computed) 값을 모델의 배열/JSON 표현에 포함하려면, [값을 JSON에 추가하는 방법](/docs/master/eloquent-serialization#appending-values-to-json)을 참고하세요.

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체 만들기

가끔은 접근자를 통해 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 경우도 있습니다. 이때는 `get` 클로저에 두 번째 인수인 `$attributes`를 선언할 수 있으며, 이 배열에는 모델의 현재 모든 속성이 담겨 전달됩니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소에 접근
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

접근자에서 값 객체를 반환할 경우, 그 객체에 대한 변경 사항은 모델 저장 전에 자동으로 모델 속성에 반영됩니다. Eloquent는 접근자에서 반환된 인스턴스를 캐싱하여, 접근자가 호출될 때마다 같은 객체 인스턴스를 반환하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 문자열이나 불리언처럼 원시(primitive) 값에 대해서도 캐싱이 필요할 때가 있습니다. 특히, 계산 비용이 높은 값이라면 캐싱을 권장합니다. 이때는 접근자를 정의할 때 `shouldCache` 메서드를 호출하십시오:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

속성의 객체 캐싱 기능을 비활성화하고 싶다면, 접근자 정의 시 `withoutObjectCaching` 메서드를 호출하십시오:

```php
/**
 * 사용자의 주소에 접근
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

변경자(mutator)는 Eloquent 속성 값을 설정할 때 자동으로 변환합니다. 변경자를 정의하려면 속성 정의 시 `set` 인자를 제공하면 됩니다. 아래는 `first_name` 속성에 대한 변경자를 정의하는 예제이며, 이 변경자는 `first_name` 값을 설정할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름에 접근
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

변경자 클로저에는 속성에 설정될 값이 전달되므로 이 값을 조작한 뒤 반환하면 됩니다. 해당 변경자를 사용하려면 Eloquent 모델에서 속성 값을 설정하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예제에서는 `set` 콜백이 'Sally' 값을 인수로 받아, `strtolower` 처리를 한 후 변경된 값을 모델의 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성에 대한 변경

경우에 따라 변경자가 모델의 여러 속성 값을 한 번에 설정해야 할 수도 있습니다. 이때는 `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 속성/컬럼명과 일치해야 하며, 해당 값이 각각 저장됩니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소에 접근
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

속성 캐스팅은 접근자 및 변경자와 유사한 기능을 제공하지만, 모델에서 별도의 메서드를 정의하지 않고도 손쉽게 속성 타입 변환이 가능합니다. 이를 위해 모델의 `casts` 메서드를 정의하면 됩니다.

`casts` 메서드는 반환값이 배열이며, 배열의 키는 캐스팅할 속성명, 값은 해당 컬럼을 변환할 타입을 명시합니다. 지원되는 캐스트 타입은 다음과 같습니다:

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

다음은 속성 캐스팅을 활용해 데이터베이스에 정수(0 또는 1)로 저장된 `is_admin` 속성을 불리언 값으로 자동 변환하는 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 할 속성을 반환합니다.
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

이처럼 캐스트를 정의하면, 데이터베이스에 정수로 저장된 값이라도 `is_admin` 속성을 접근할 때마다 항상 불리언 값으로 변환됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시로 새로운 캐스트를 추가하고자 할 때는 `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드를 통해 새롭게 정의한 캐스트 항목이 기존 정의와 병합됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 리레이션십과 동일한 이름의 캐스트(또는 속성)를 정의하거나, 모델의 기본 키에 캐스트를 적용해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용해, 모델 속성을 [유연한 Illuminate\Support\Stringable 객체](/docs/master/strings#fluent-strings-method-list)로 변환할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 할 속성을 반환합니다.
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

`array` 캐스트는 직렬화된(serialized) JSON 형식 컬럼을 다룰 때 매우 유용합니다. 데이터베이스의 `JSON` 타입이나 `TEXT` 컬럼에 JSON 형태로 값이 저장되어 있다면, 해당 속성에 `array` 캐스트를 지정함으로써 Eloquent 모델에서 해당 값을 PHP 배열로 자동 변환해줍니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 할 속성을 반환합니다.
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

한 번 캐스트가 정의되면, `options` 속성에 직접 접근하여 JSON이 자동으로 PHP 배열로 역직렬화됩니다. 또한, `options` 속성에 배열을 대입하면 자동으로 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 간편하게 업데이트하려면, [속성을 대량 할당 가능](/docs/master/eloquent#mass-assignment-json-columns)하도록 한 뒤 `update` 메서드에서 `->` 연산자를 활용하면 됩니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 이스케이프되지 않은(unescaped) 유니코드 JSON으로 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다:

```php
/**
 * 캐스팅해야 할 속성을 반환합니다.
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

표준 `array` 캐스트는 대부분의 경우 충분하지만, 원시 타입으로 반환되기 때문에 배열의 offset을 직접 조작하면 PHP 오류가 발생할 수 있습니다. 예를 들어:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이러한 문제를 해결하기 위해, Laravel에서는 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 JSON 속성을 변환하는 `AsArrayObject` 캐스트 타입을 제공합니다. 이 기능은 [커스텀 캐스트](#custom-casts)를 사용해 구현되어 있어, 개별 offset 변경 시 PHP 오류 없이 객체가 지능적으로 캐싱/변환됩니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

비슷하게, Eloquent 속성을 Laravel의 [Collection](/docs/master/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공됩니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

`AsCollection` 캐스트에서 Laravel 기본 컬렉션이 아닌 사용자 정의 컬렉션 클래스를 사용하려면, 캐스트 인자로 해당 클래스명을 지정하면 됩니다:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

`of` 메서드를 사용하면, 컬렉션의 [mapInto 메서드](/docs/master/collections#method-mapinto)를 통해 컬렉션 항목들을 특정 클래스로 매핑할 수 있습니다:

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

컬렉션을 객체로 매핑할 경우, 해당 객체는 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해 데이터베이스에 JSON으로 직렬화되는 방식을 정의해야 합니다:

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
     * 새로운 Option 인스턴스 생성
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * 배열로 변환
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
     * JSON 직렬화 데이터 지정
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

Eloquent 모델에서 [binary 타입](/docs/master/migrations#column-method-binary)의 `uuid` 또는 `ulid` 컬럼을 자동 증가 ID 컬럼과 함께 사용하는 경우, `AsBinary` 캐스트를 이용해 해당 값을 바이너리와 문자열 형태로 쉽고 자동으로 변환할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsBinary;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

캐스트를 정의한 후에는 UUID/ULID 속성 값을 객체 인스턴스 또는 문자열로 대입할 수 있습니다. Eloquent가 자동으로 바이너리로 변환해서 저장하고, 조회 시에는 항상 문자열 값으로 반환합니다:

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 객체(즉, PHP `DateTime` 클래스 확장)에 자동으로 매핑합니다. 여기에 다양한 메서드를 사용할 수 있습니다. 추가적인 날짜 속성이 있다면 모델의 `casts` 메서드에 해당 속성을 `datetime` 또는 `immutable_datetime` 등으로 지정합니다.

날짜 또는 날짜시간 캐스트를 정의할 때, 포맷을 함께 지정할 수 있습니다. 이 포맷은 [모델을 배열/JSON으로 직렬화](/docs/master/eloquent-serialization)할 때 사용됩니다:

```php
/**
 * 캐스팅해야 할 속성을 반환합니다.
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

날짜로 캐스트된 컬럼은 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스 등 다양한 방식으로 값을 설정할 수 있으며, 적절히 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜 속성의 기본 직렬화 포맷은 `serializeDate` 메서드를 오버라이드하여 지정할 수 있습니다. 이 메서드는 데이터베이스에 저장되는 값의 포맷에는 영향을 주지 않습니다:

```php
/**
 * 날짜를 배열/JSON 직렬화용 문자열로 준비
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 날짜를 실제로 저장할 때 사용하는 포맷은 모델의 `$dateFormat` 프로퍼티로 지정하십시오:

```php
/**
 * 모델 날짜 컬럼의 저장 포맷
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스트는 애플리케이션의 `timezone` 환경설정과 관계없이 UTC ISO-8601 날짜 문자열 (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화됩니다. 대부분의 경우, 이 직렬화 포맷 및 기본 `UTC` 타임존 설정을 변경하지 않을 것을 강력하게 권장합니다. 이 규칙을 일관성 있게 따르면, PHP 및 JavaScript의 다양한 날짜 라이브러리들과의 호환성이 최대한 보장됩니다.

만약 `date` 혹은 `datetime` 캐스트에 사용자 정의 포맷(예: `datetime:Y-m-d H:i:s`)을 지정하면, Carbon 인스턴스의 내부 타임존이 적용되어 직렬화됩니다(대부분은 애플리케이션 `timezone` 환경설정에 따름). 단, `created_at`, `updated_at` 등 `timestamp` 컬럼만큼은 항상 UTC로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent에서는 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)로 캐스팅하는 기능도 제공합니다. 이를 위해 모델의 `casts` 메서드에서 속성과 Enum을 지정하면 됩니다:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

캐스트를 정의하면, 해당 속성 값은 Enum 인스턴스로 자동 변환되어 사용할 수 있습니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

모델에서 Enum 값의 배열을 하나의 컬럼에 저장해야 할 때도 있습니다. 이때는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅해야 할 속성을 반환합니다.
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

`encrypted` 캐스트는 Laravel 내장 [암호화](/docs/master/encryption) 기능을 이용해 속성 값을 암호화/복호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등의 캐스트는 비암호화 버전과 동일하게 동작하나, 데이터베이스에 저장되는 값이 암호화됩니다.

암호화된 데이터는 평문보다 길어질 수 있으므로, 해당 컬럼을 반드시 `TEXT` 타입 이상으로 지정하세요. 데이터 값이 암호화되므로 쿼리로 조회(search)하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 키(Key) 교체(로테이션)

Laravel은 `app` 설정 파일의 `key` 설정값(일반적으로 `APP_KEY` 환경 변수)을 이용해 문자열을 암호화합니다. 애플리케이션의 암호화 키를 교체(로테이션)해야 할 경우, [안전하게 키 교체하는 방법](/docs/master/encryption#gracefully-rotating-encryption-keys)을 참고하세요.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

특정 쿼리를 실행할 때 임시로 캐스트를 적용해야 하는 상황도 있습니다. 예를 들어, 테이블에서 raw 값으로 컬럼을 선택(select)하는 쿼리에서 다음과 같이 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

위 쿼리 결과의 `last_posted_at` 속성은 단순 문자열로 반환됩니다. 이 속성에 `datetime` 캐스트를 쿼리 실행 시점에만 적용하려면, `withCasts` 메서드를 이용할 수 있습니다:

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

Laravel에는 유용한 기본 캐스트 타입들이 제공되지만, 개발자가 직접 캐스트 타입을 정의할 수도 있습니다. 커스텀 캐스트 클래스를 생성하려면, `make:cast` Artisan 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `get` 및 `set` 메서드를 반드시 정의해야 합니다. `get` 메서드는 데이터베이스의 원래 값을 캐스트 값으로 변환하는 역할, `set` 메서드는 캐스트 값을 데이터베이스 저장을 위한 형태로 변환하는 역할입니다. 아래 예제는 Laravel 내장 `json` 캐스트 타입을 직접 구현한 것입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * 주어진 값을 캐스팅
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
     * 저장용 값 변환
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

커스텀 캐스트 타입을 정의한 후, 클래스명을 활용해 모델 속성에 바로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 할 속성을 반환합니다.
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
### 값 객체 캐스팅

Eloquent 속성을 원시 타입뿐 아니라 객체로도 캐스팅할 수 있습니다. 특히 값 객체가 여러 데이터베이스 컬럼에 걸쳐 있다면, 커스텀 캐스트의 `set` 메서드는 컬럼 키/값 쌍의 배열을 반환해야 하며, 하나의 컬럼에만 영향을 줄 경우에는 값만 반환하면 됩니다.

예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 클래스 구현 예시입니다. `Address` 값 객체는 `lineOne`, `lineTwo` 두 속성을 가집니다:

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
     * 주어진 값을 캐스팅
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
     * 저장용 값 변환
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

값 객체로 캐스팅할 때, 값 객체의 내용을 수정하면 모델 저장 전에 자동으로 모델에 반영됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable` 과 `JsonSerializable` 인터페이스를 반드시 구현하십시오.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스트된 속성을 접근하면, Eloquent가 객체를 캐시하므로 이후 같은 속성에 접근할 때 동일한 객체 인스턴스를 반환합니다.

커스텀 캐스트 클래스의 객체 캐싱 동작을 비활성화하려면, 커스텀 캐스트 클래스에 public `withoutObjectCaching` 프로퍼티를 선언하고 `true` 값을 할당합니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson`을 통해 배열이나 JSON으로 변환하면, 커스텀 캐스트 값 객체도 보통 직렬화됩니다(단, 값 객체가 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 구현 시에만 가능). 외부 라이브러리의 값 객체처럼 인터페이스 구현이 불가능하다면, 커스텀 캐스트 클래스에서 직접 직렬화 로직을 담당하도록 할 수 있습니다.

이 경우 커스텀 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `serialize` 메서드를 요구합니다. 반환값이 직렬화된 형태가 되어야 합니다:

```php
/**
 * 값의 직렬화 표현 반환
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
### 인바운드 캐스팅

간혹 속성 값이 모델에 "설정(set)"될 때만 값을 변환하고, 조회(get) 시에는 별도 처리를 하지 않는 단방향(인바운드 only) 커스텀 캐스트가 필요할 수 있습니다.

인바운드 전용 커스텀 캐스트 클래스를 만들려면 `CastsInboundAttributes` 인터페이스를 구현하면 됩니다(`set` 메서드만 필요). `make:cast` Artisan 명령어에 `--inbound` 옵션을 추가해 클래스를 만들 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```

예시) 해싱(Hashing) 캐스트처럼, 저장 시에만 특정 해시 알고리즘으로 값을 변환하는 클래스를 만들 수 있습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 클래스 인스턴스 생성
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장용 값 변환
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

커스텀 캐스트를 모델에 지정할 때, 클래스 이름 뒷부분에 `:`로 구분해서 파라미터를 전달할 수 있습니다(여러 파라미터는 쉼표로 구분). 이 파라미터들은 캐스트 클래스의 생성자에 전달됩니다:

```php
/**
 * 캐스팅해야 할 속성을 반환합니다.
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

두 캐스트 값이 실제로 변경되었는지 판단하는 로직을 커스텀하게 정의하고 싶다면, 커스텀 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현하여 세밀하게 비교 동작을 제어할 수 있습니다.

이 인터페이스는 두 값이 같은지 여부를 반환하는 `compare` 메서드를 요구합니다:

```php
/**
 * 주어진 값들이 동일한지 판단
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

애플리케이션의 값 객체에서 자체적으로 커스텀 캐스트 클래스를 지정하고 싶을 수도 있습니다. 이럴 때는 모델에 커스텀 캐스트 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 바로 지정할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체 클래스는, 실제로 캐스팅을 담당할 커스텀 캐스터 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * 이 값 타입을 캐스팅할 때 사용할 캐스터 클래스명을 반환
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

`Castable` 클래스 사용시에도 `casts` 메서드에서 인자를 추가로 지정할 수 있으며, 이 인자는 `castUsing` 메서드에 그대로 전달됩니다:

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
#### 캐스터블 & 익명(Anonymous) 캐스트 클래스

"캐스터블" 기능과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하면, 값 객체와 캐스팅 로직을 하나의 캐스터블 객체로 구현할 수 있습니다. 이를 위해, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하며, 이 익명 클래스가 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 값 타입을 캐스팅할 때 사용할 캐스터 클래스(익명 클래스) 반환
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