# Eloquent: 변경자 & 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [엑세서와 변경자](#accessors-and-mutators)
    - [엑세서 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [Array 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [Array / JSON 직렬화](#array-json-serialization)
    - [InBound 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스트 값 비교](#comparing-cast-values)
    - [캐스터블](#castables)

<a name="introduction"></a>
## 소개

엑세서(accessor), 변경자(mutator), 그리고 속성 캐스팅(attribute casting)을 활용하면 Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 값을 변환할 수 있습니다. 예를 들어, [Laravel 암호화 도구](/docs/12.x/encryption)를 활용하여 데이터를 데이터베이스에 저장할 때 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 자동 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 엑세서와 변경자

<a name="defining-an-accessor"></a>
### 엑세서 정의하기

엑세서(accessor)는 Eloquent 속성에 접근할 때 그 값을 변환합니다. 엑세서를 정의하려면 모델에 접근할 속성을 나타내는 보호된(protected) 메서드를 생성하십시오. 메서드 이름은 가능하다면 실제 모델 속성(데이터베이스 컬럼)의 "카멜 케이스" 표기법과 일치해야 합니다.

예를 들어, `first_name` 속성에 대한 엑세서를 정의해보겠습니다. 이 엑세서는 `first_name` 속성 값을 가져올 때 Eloquent에 의해 자동으로 호출됩니다. 모든 속성의 엑세서/변경자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환형으로 명시해야 합니다:

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

모든 엑세서 메서드는 `Attribute` 인스턴스를 반환하며, 이 객체를 통해 해당 속성을 어떻게 접근(그리고 선택적으로 변환)할지 정의할 수 있습니다. 위 예제에서는 속성에 접근하는 방법만 정의하고 있습니다. 이를 위해 `Attribute` 클래스의 생성자에 `get` 인자를 전달합니다.

보시다시피, 컬럼의 원래 값이 엑세서로 전달되므로, 원하는 대로 값을 가공해서 반환할 수 있습니다. 엑세서의 값을 사용하려면 모델 인스턴스에서 그냥 `first_name` 속성에 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 계산된 이 값들이 모델의 배열/JSON 표현에 포함되길 원한다면, [값을 명시적으로 추가해야 합니다](/docs/12.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

엑세서가 여러 모델 속성을 하나의 "값 객체(value object)"로 변환해야 할 때도 있습니다. 이를 위해 `get` 클로저에 두 번째 인자로 `$attributes`를 받을 수 있는데, 이 인자에는 모델의 현재 모든 속성이 배열로 전달됩니다:

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
#### 엑세서 캐싱

엑세서에서 값 객체를 반환하면, 해당 객체에 가한 변경 내용이 모델이 저장되기 전에 자동으로 모델에 다시 동기화됩니다. 이는 Eloquent가 엑세서에서 반환된 인스턴스를 내부적으로 저장해서, 엑세서가 호출될 때마다 동일한 인스턴스를 반환하기 때문에 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 만약 문자열이나 불리언처럼 원시 값도 캐싱하고 싶을 때(특히 값 계산이 복잡하거나 비용이 클 경우), 엑세서 정의 시 `shouldCache` 메서드를 사용할 수 있습니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 속성의 객체 캐싱 동작을 비활성화하고 싶다면 `withoutObjectCaching` 메서드를 사용하면 됩니다:

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

변경자(mutator)는 Eloquent 속성에 값을 설정할 때 변환을 수행합니다. 변경자를 정의하려면 속성 정의 시 `set` 인자를 제공하면 됩니다. 이제 `first_name` 속성에 대한 변경자를 정의해보겠습니다. 이 변경자는 해당 모델의 `first_name` 속성 값을 설정할 때 자동으로 호출됩니다:

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

변경자 클로저는 속성에 설정되는 값을 인자로 받아, 이를 가공한 뒤 새로운 값을 반환합니다. 변경자를 사용하려면, Eloquent 모델에서 해당 속성에 값을 대입하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예제에서는 `set` 콜백에 `Sally`가 전달됩니다. 변경자는 `strtolower` 함수를 적용한 결과를 모델 내부의 `$attributes` 배열에 저장하게 됩니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변환하기

때때로, 변경자에서 모델의 여러 속성을 동시에 설정해야 할 수도 있습니다. 이럴 경우, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 속성(데이터베이스 컬럼)명과 맞아야 합니다:

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

속성 캐스팅(attribute casting)은 엑세서와 변경자와 유사한 기능을 제공하지만, 모델에 추가 메서드를 정의하지 않아도 사용할 수 있습니다. 대신, 모델의 `casts` 메서드를 활용하여 속성을 일반적인 데이터 타입으로 편리하게 변환할 수 있습니다.

`casts` 메서드는 캐스팅할 속성명을 키로, 변환할 타입을 값으로 갖는 배열을 반환해야 합니다. 지원되는 캐스트 타입은 다음과 같습니다.

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

속성 캐스팅을 예시로 살펴보겠습니다. 데이터베이스에는 정수(예: `0` 또는 `1`)로 저장된 `is_admin` 필드를 불리언 타입으로 캐스팅해볼 수 있습니다:

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

위처럼 캐스트를 정의하면, 데이터베이스에 정수로 저장되어 있더라도 `is_admin` 속성에 접근할 때 항상 불리언 값으로 캐스팅됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시로 새로운 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드로 정의한 캐스트는 기존 모델의 캐스트 정의와 합쳐집니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` 값인 속성은 캐스팅되지 않습니다. 또한 관계명(relationship)과 이름이 같은 속성이나, 모델의 기본키에 캐스트를 할당해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 모델 속성을 [유연한 Stringable 객체](/docs/12.x/strings#fluent-strings-method-list)로 변환할 수 있습니다:

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
### Array 및 JSON 캐스팅

`array` 캐스트는 직렬화된 JSON으로 저장되는 컬럼을 다룰 때 매우 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼에 직렬화된 JSON이 저장되어 있다면, 해당 속성에 `array` 캐스트를 지정하면 Eloquent 모델에서 해당 속성에 접근할 때 자동으로 PHP 배열로 역직렬화해줍니다:

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

캐스트를 지정하면, `options` 속성에 접근할 때마다 JSON이 자동으로 PHP 배열로 변환됩니다. 반대로 해당 속성에 값을 설정하면, 주어진 배열이 자동으로 JSON 문자열로 직렬화되어 저장됩니다(저장 시):

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 특정 필드만 간결하게 업데이트하려면, [해당 속성을 일괄 할당(mass assignable)으로 지정](/docs/12.x/eloquent#mass-assignment-json-columns)하고 `update` 메서드 호출 시 `->` 연산자를 활용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 JSON에 인코딩하면서 유니코드 문자가 이스케이프되지 않게 저장하려면, `json:unicode` 캐스트를 사용할 수 있습니다:

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
#### Array Object 및 컬렉션 캐스팅

기본 `array` 캐스트는 많은 경우 충분하지만 몇 가지 제약이 있습니다. 예를 들어, `array` 캐스트는 원시형 타입을 반환하므로 배열의 일부 요소만 직접 수정할 수 없습니다. 다음 예시는 PHP 오류를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 라라벨은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 라라벨의 [커스텀 캐스트](#custom-casts) 구현체를 사용하며, 개별 요소의 변경이 PHP 오류 없이 반영될 수 있도록 캐싱 및 변환을 관리합니다. `AsArrayObject` 캐스트 사용 방법은 다음과 같습니다:

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

마찬가지로, 라라벨은 JSON 속성을 라라벨의 [Collection](/docs/12.x/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공합니다:

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

`AsCollection` 캐스트를 사용할 때 라라벨 기본 컬렉션이 아닌 커스텀 컬렉션 클래스를 인스턴스화하도록 하고 싶다면, 캐스트 인자로 컬렉션 클래스명을 전달하면 됩니다:

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

또한, `of` 메서드를 사용하면 컬렉션의 항목을 지정한 클래스의 인스턴스로 [mapInto 메서드](/docs/12.x/collections#method-mapinto)를 통해 자동 변환할 수 있습니다:

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

컬렉션 항목을 객체로 변환할 때, 해당 객체는 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현해야만 각각 배열 및 JSON으로 직렬화하는 방법을 정의할 수 있습니다:

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

라라벨 Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 변환합니다. Carbon은 PHP의 `DateTime` 클래스를 확장한 도구로, 날짜와 시간 관련 유용한 메서드를 다수 제공합니다. 추가적인 날짜 속성을 캐스팅하려면, 모델의 `casts` 메서드에서 해당 속성을 `date` 또는 `datetime`, 혹은 `immutable_datetime` 캐스트 타입 중 하나로 지정하면 됩니다.

`date` 또는 `datetime` 캐스트 지정 시, 날짜 형식(format)도 함께 명시할 수 있습니다. 이 형식은 [모델이 배열이나 JSON으로 직렬화될 때](/docs/12.x/eloquent-serialization)에 사용됩니다:

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

날짜로 캐스팅된 컬럼에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 모두 지정할 수 있습니다. 값은 적절히 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜의 기본 직렬화 형식을 커스터마이즈하려면 `serializeDate` 메서드를 모델에 정의하면 됩니다. 이 메서드는 데이터베이스에 저장될 때가 아니라, 직렬화 시 사용되는 형식만 변경합니다:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜 컬럼이 실제로 데이터베이스에 저장되는 형식을 지정하려면, 모델에 `$dateFormat` 속성을 정의하면 됩니다:

```php
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>

#### 날짜 캐스팅, 직렬화 및 타임존

기본적으로, `date`와 `datetime` 캐스트는 애플리케이션의 `timezone` 설정값에 관계없이 날짜를 UTC ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)의 문자열로 직렬화합니다. 이 직렬화 형식과 애플리케이션의 날짜를 UTC 타임존으로 저장하는 방식(즉, `timezone` 설정을 기본값인 `UTC`로 유지하는 것)을 항상 사용할 것을 강력히 권장합니다. 애플리케이션 전체에서 UTC 타임존을 일관되게 사용하면, PHP나 JavaScript로 작성된 기타 날짜 처리 라이브러리와의 호환성이 극대화됩니다.

만약 `datetime:Y-m-d H:i:s`와 같은 사용자 지정 형식이 `date`나 `datetime` 캐스트에 적용된다면, 날짜 직렬화 시 Carbon 인스턴스의 내부 타임존이 사용됩니다. 보통 이 타임존은 애플리케이션의 `timezone` 설정값을 따릅니다. 하지만 주의할 점은 `created_at`, `updated_at` 같은 `timestamp` 컬럼은 이 규칙에서 예외이며, 애플리케이션의 타임존과 무관하게 항상 UTC로 포맷된다는 점입니다.

<a name="enum-casting"></a>
### Enum(열거형) 캐스팅

Eloquent는 속성 값을 PHP의 [Enum(열거형)](https://www.php.net/manual/en/language.enumerations.backed.php)으로 타입 캐스팅하는 것도 지원합니다. 이를 위해, 모델의 `casts` 메서드에서 캐스팅하려는 속성과 Enum을 지정하면 됩니다.

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

이렇게 모델에 캐스트를 정의한 후에는 해당 속성에 접근할 때마다 자동으로 Enum으로 변환되며, Enum 값을 저장하거나 불러올 수 있습니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

특정 컬럼에 Enum 값의 배열을 저장해야 할 일이 있을 수 있습니다. 이런 경우, Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다.

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

`encrypted` 캐스트는 라라벨의 내장 [암호화](/docs/12.x/encryption) 기능을 사용해 모델의 속성 값을 암호화합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등도 암호화되지 않은 버전과 동일하게 동작하지만, 저장 시 실제 값이 암호화됩니다.

암호화된 텍스트의 길이는 예측할 수 없고 일반 텍스트보다 길어지므로, 암호화 속성이 저장되는 컬럼은 반드시 `TEXT` 타입이나 그보다 더 큰 타입이어야 합니다. 그리고 데이터베이스에 값이 암호화되어 저장되므로, 암호화된 속성에 대해 쿼리하거나 검색하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

라라벨은 애플리케이션의 `app` 설정 파일에 지정된 `key` 설정값(보통은 환경변수 `APP_KEY`)을 이용해 문자열을 암호화합니다. 애플리케이션의 암호화 키를 교체해야 할 경우, 기존에 암호화된 속성들은 수동으로 새 키로 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

테이블에서 raw 값(가공되지 않은 값)을 조회할 때, 쿼리 실행 시점에 캐스트를 적용해야 할 때가 있습니다. 예시로, 아래와 같은 쿼리를 생각해 보세요.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리 결과의 `last_posted_at` 속성은 단순한 문자열로 반환됩니다. 쿼리 실행 시 해당 속성에 `datetime` 캐스트를 적용하고 싶을 수 있습니다. 다행히도, `withCasts` 메서드를 사용하면 이를 쉽게 해결할 수 있습니다.

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

라라벨은 여러 유용한 내장 캐스트 타입을 제공합니다. 그러나 때로는 사용자만의 캐스트 타입이 필요할 수도 있습니다. 캐스트를 생성하려면 `make:cast` Artisan 명령어를 사용하세요. 생성된 캐스트 클래스는 `app/Casts` 디렉터리에 저장됩니다.

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스팅된 값으로 변환하는 역할을 하며, `set` 메서드는 캐스팅된 값을 데이터베이스에 저장 가능한 원시 값으로 변환합니다. 아래는 내장 `json` 캐스트 타입을 커스텀으로 재구현한 예시입니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * 주어진 값을 캐스트합니다.
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

커스텀 캐스트 타입을 정의한 후에는, 해당 클래스명을 이용해 모델의 속성에 캐스트를 지정할 수 있습니다.

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
### 값 객체(Value Object) 캐스팅

캐스팅을 기본 타입에만 제한할 필요는 없습니다. 객체로도 값을 캐스팅할 수 있습니다. 값 객체로 캐스팅하는 커스텀 캐스트 구현 방식은 기본 타입과 매우 비슷합니다. 그러나 값 객체가 여러 데이터베이스 컬럼에 걸쳐 있다면, `set` 메서드는 모델에 저장될 원시 값들의 키/값 쌍 배열을 반환해야 합니다. 값 객체가 단일 컬럼과만 연관된다면, 저장 가능한 값을 단일 값으로 반환하면 됩니다.

아래 예시에서는 여러 모델 속성을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의합니다. `Address` 값 객체에는 `lineOne`과 `lineTwo`라는 두 개의 public 속성이 있다고 가정합니다.

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
     * 주어진 값을 캐스트합니다.
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
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅할 경우, 값 객체를 변경하면 모델이 저장되기 전 자동으로 모델에도 변경 내용이 반영됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON이나 배열로 직렬화하려면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 반드시 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성에 접근하면 Eloquent는 그 객체를 캐싱합니다. 따라서 같은 속성에 다시 접근하면 항상 동일한 객체 인스턴스가 반환됩니다.

만약 커스텀 캐스트 클래스에서 이러한 객체 캐싱 동작을 비활성화하고 싶다면, 캐스트 클래스에서 `withoutObjectCaching`라는 public 속성을 선언하면 됩니다.

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray` 또는 `toJson` 메서드로 배열이나 JSON으로 변환할 때, 커스텀 캐스트 값 객체도 보통 직렬화됩니다(단, 해당 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현한 경우). 하지만 외부 라이브러리의 값 객체는 이 인터페이스를 추가할 수 없을 수도 있습니다.

이럴 때는 커스텀 캐스트 클래스 자체가 직접 직렬화를 담당할 수 있습니다. 이를 위해 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하면 됩니다. 이 인터페이스는 값 객체를 직렬화하는 `serialize` 메서드를 요구합니다.

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
### 입력(Inbound) 캐스팅

때때로, 모델의 속성값을 "설정"할 때만 변환이 필요하고, "조회" 시에는 변환이 필요 없는 커스텀 캐스트를 작성해야 할 수도 있습니다.

입력(Inbound) 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 경우 `set` 메서드만 구현하면 됩니다. 입력 전용 캐스트 클래스를 Artisan 명령어로 생성할 때는 `--inbound` 옵션을 사용하면 됩니다.

```shell
php artisan make:cast AsHash --inbound
```

입력 전용 캐스트의 대표적 예시가 "해시(hash) 처리"입니다. 예를 들어, 특정 알고리즘으로 값을 해싱하는 캐스트를 아래처럼 정의할 수 있습니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 클래스 인스턴스를 생성합니다.
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
### 캐스트 파라미터

커스텀 캐스트를 모델에 연결할 때, `:` 문자로 클래스명과 파라미터를 구분해서 여러 개의 파라미터를 콤마로 구분하여 전달할 수 있습니다. 이 파라미터들은 캐스트 클래스의 생성자에 순서대로 전달됩니다.

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
### 캐스트 값 비교

두 캐스트 값이 변경되었는지 비교하는 방식을 직접 정의하고 싶을 때는, 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현하면 됩니다. 이렇게 하면 Eloquent가 어떤 값을 "변경됨"으로 간주하는지 더 세밀하게 제어할 수 있습니다.

이 인터페이스는 두 값이 같으면 `true`를 반환해야 하는 `compare` 메서드를 요구합니다.

```php
/**
 * 두 값이 같은지 판단합니다.
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
### 캐스터(Castable) 객체

애플리케이션의 값 객체가 스스로 커스텀 캐스트 클래스를 지정하는 기능을 제공하고 싶을 수 있습니다. 이때 커스텀 캐스트 클래스를 모델에 연결하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 직접 지정할 수 있습니다.

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는, 해당 객체의 캐스팅에 사용할 커스텀 캐스트 클래스명을 반환하는 `castUsing` 메서드를 정의해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * 이 캐스트 타겟에 대한 캐스터 클래스명을 반환합니다.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

`Castable` 클래스를 사용할 때도 `casts` 메서드 정의에서 인자를 전달할 수 있으며, 이 인수들은 `castUsing` 메서드로 전달됩니다.

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
#### 캐스터 & 익명 클래스(Anonymous Cast Classes)

"Castable"을 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 결합하면, 값 객체와 그 캐스팅 로직을 하나의 castable 객체로 정의할 수 있습니다. 이를 위해, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 캐스트 타겟에 사용할 캐스터 클래스를 반환합니다.
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