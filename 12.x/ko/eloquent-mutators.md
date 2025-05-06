# Eloquent: 접근자(Accessor), 변경자(Mutator) & 캐스팅(Casting)

- [소개](#introduction)
- [접근자와 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스팅](#custom-casts)
    - [값 객체(Value Object) 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자(Accessor), 변경자(Mutator), 그리고 속성 캐스팅(Casting)을 통해 Eloquent 모델 인스턴스의 속성 값을 조회하거나 설정할 때 값의 변환이 가능합니다. 예를 들어, [Laravel 암호화기](/docs/{{version}}/encryption)를 사용하여 데이터베이스에 값을 저장할 때 암호화하고, Eloquent 모델에서 속성을 접근할 때 자동으로 복호화할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 자동 변환할 수 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자(Accessor)와 변경자(Mutator)

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 속성 값에 접근할 때 Eloquent 속성 값을 변환합니다. 접근자를 정의하려면 모델에 접근 가능한 속성을 나타내는 protected 메서드를 생성합니다. 이 메서드의 이름은 실제 모델 속성/DB 컬럼의 "카멜 케이스" 형태여야 합니다(해당 시).

예시로, `first_name` 속성에 대한 접근자를 정의해 보겠습니다. 이 접근자는 Eloquent가 `first_name` 속성 값을 조회할 때 자동으로 호출됩니다. 모든 접근자/변경자 메서드는 리턴 타입으로 `Illuminate\Database\Eloquent\Casts\Attribute`를 명시해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first_name)을 반환합니다.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

모든 접근자 메서드는 속성이 접근될 때(선택적으로 변경될 때) 어떻게 변환되는지를 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예시에서는 get 인자만 전달하여 조회 시 속성이 변환되는 방식을 정의했습니다.

컬럼의 원본 값이 접근자에 전달되므로, 값을 조작하여 응답할 수 있습니다. 접근자 접근은 모델 인스턴스에서 해당 속성에 단순히 접근하면 됩니다.

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이런 계산된 값을 모델의 배열/JSON 표현에도 포함하고 싶다면, [명시적으로 속성을 추가해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체(Value Object) 만들기

접근자가 여러 모델 속성을 하나의 "값 객체"로 변환해야 할 때가 있습니다. 이런 경우, `get` 클로저에 두 번째 인자로 `$attributes`를 받아서 사용할 수 있습니다. 이 배열에는 모델의 현재 모든 속성이 포함됩니다.

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

접근자에서 값 객체를 반환할 경우, 해당 값 객체에 변경이 생기면 모델이 저장되기 전 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자에서 반환된 인스턴스를 유지하여, 접근자가 다시 호출될 때 동일한 인스턴스를 반환하기 때문입니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 문자열이나 불린 같은 원시 타입에 대해서도, 연산 비용이 크다면 캐싱을 원할 수 있습니다. 이럴 때는 접근자를 정의할 때 `shouldCache` 메서드를 호출하면 됩니다.

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 접근자의 객체 캐싱 동작을 비활성화하려면 `withoutObjectCaching` 메서드를 사용할 수 있습니다.

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

변경자는 속성 값이 설정될 때 값을 변환합니다. 변경자를 정의하려면 Attribute 정의 시 `set` 인자를 추가하면 됩니다. 아래는 `first_name` 속성에 대한 변경자 예시입니다. 모델에서 값이 설정될 때 자동 호출됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름 변경자.
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

변경자 클로저에는 속성에 할당되는 값이 전달되므로, 값을 원하는 대로 조작해 반환할 수 있습니다. 변경자는 속성에 그냥 값을 할당하면 자동으로 호출됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예시에서 `set` 콜백이 `Sally` 값을 받아 `strtolower`를 적용해 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성을 변경하기

변경자가 모델의 여러 속성 값을 설정해야 할 때, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 컬럼명이어야 합니다.

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

속성 캐스팅은 별도의 메서드 생성 없이 접근자 및 변경자의 기능과 유사한 속성 변환 기능을 제공합니다. 모델의 `casts` 메서드에 속성명의 키와 원하는 캐스트 타입값 쌍을 배열로 반환하면 됩니다. 지원되는 캐스트 타입은 다음과 같습니다.

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

예를 들어, 데이터베이스엔 0 또는 1의 정수로 저장된 `is_admin` 속성을 불린으로 캐스팅해보겠습니다.

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

위와 같이 정의하면, 데이터베이스에 정수로 저장되어 있어도 `is_admin`에 접근할 때는 항상 불린으로 변환되어 반환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에서 임시로 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 정의는 기존 캐스트와 병합됩니다.

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null`인 속성은 캐스팅되지 않습니다. 또한 관계명과 동일한 캐스트(또는 속성) 이름을 사용하거나 모델의 기본키(primary key)에 캐스트를 할당해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용해, 모델 속성을 [유연한 Illuminate\Support\Stringable 객체](/docs/{{version}}/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다.

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

`array` 캐스트는 직렬화된 JSON을 저장하는 컬럼에 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼에 직렬화된 JSON이 저장되어 있을 경우, `array` 캐스트를 설정하면 Eloquent 모델에서 해당 속성에 접근할 때 자동으로 PHP 배열로 변환됩니다.

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

캐스트를 정의하면, `options` 속성은 자동으로 PHP 배열로 디코드됩니다. 반대로 값을 저장할 땐 자동으로 JSON 문자열로 직렬화되어 데이터베이스에 저장됩니다.

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 값을 더 간결한 문법으로 업데이트하려면, [속성을 대량 할당 가능](https://laravel.kr/docs/{{version}}/eloquent#mass-assignment-json-columns)하도록 하고 `->` 연산자를 사용해 `update` 메서드로 갱신할 수 있습니다.

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 유니코드가 이스케이프되지 않은 JSON으로 저장하고 싶다면 `json:unicode` 캐스트를 사용할 수 있습니다.

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
#### ArrayObject 및 Collection 캐스팅

일반 `array` 캐스트는 많은 경우 충분하지만, 배열의 원소를 직접 변경할 수 없다는 단점이 있습니다. 예를 들어 아래 코드는 PHP 에러를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 [Custom Casts](#custom-casts)를 사용하여 구현되므로, 변경된 오브젝트를 캐싱하고 각 오프셋을 PHP 오류 없이 수정이 가능합니다. 사용법은 다음과 같습니다.

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

비슷하게, `AsCollection` 캐스트를 사용해 JSON 속성을 Laravel [Collection](/docs/{{version}}/collections) 인스턴스로 반환할 수 있습니다.

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

`AsCollection` 캐스트에 커스텀 컬렉션 클래스를 사용하고 싶다면 클래스명을 인자로 전달합니다.

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

`of` 메서드로 컬렉션 아이템을 [mapInto 메서드](/docs/{{version}}/collections#method-mapinto)를 이용해 특정 클래스로 매핑할 수 있게 할 수도 있습니다.

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

컬렉션을 오브젝트로 매핑할 경우, 해당 오브젝트는 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현해야 데이터베이스에 JSON으로 직렬화가 가능합니다.

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
     * 새로운 Option 인스턴스를 생성합니다.
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
     * JSON 직렬화시 저장할 데이터를 명시합니다.
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
### 날짜(Date) 캐스팅

Eloquent는 기본적으로 `created_at`과 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. 이 클래스는 PHP의 `DateTime`을 확장해 여러 편의 기능을 제공합니다. 모델의 `casts` 메서드에 추가적인 날짜 캐스트를 지정하여, 더 많은 날짜 속성을 캐스팅할 수도 있습니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스팅을 사용합니다.

`date` 또는 `datetime` 캐스팅 시 날짜 포맷을 지정할 수 있고, 이 포맷은 [모델이 배열이나 JSON으로 직렬화될 때](/docs/{{version}}/eloquent-serialization) 사용됩니다.

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

컬럼을 날짜로 캐스팅하면, 모델 속성 값에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 지정할 수 있습니다. 값은 적절히 변환되어 데이터베이스에 저장됩니다.

모든 날짜 속성의 기본 직렬화 포맷을 커스터마이즈하고 싶다면 모델에 `serializeDate` 메서드를 정의합니다. 이 메서드는 값이 데이터베이스에 저장되는 포맷에는 영향주지 않습니다.

```php
/**
 * 배열/JSON 직렬화용 날짜 포맷 지정
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜 컬럼이 실제로 데이터베이스에 저장될 때의 포맷을 지정하려면, `$dateFormat` 속성을 모델에 정의하세요.

```php
/**
 * 모델의 날짜 컬럼 저장 포맷
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 및 타임존

기본적으로, `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정과 관계없이 날짜를 UTC ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`) 문자열로 직렬화합니다. 이러한 직렬화 포맷과, 애플리케이션의 날짜도 기본 `UTC` 타임존을 사용하는 것을 권장합니다. UTC를 일관성 있게 사용하면 PHP 및 JavaScript 기본 날짜 라이브러리와의 호환성이 극대화됩니다.

만약 `date` 또는 `datetime` 캐스팅에 커스텀 포맷(예: `datetime:Y-m-d H:i:s`)을 적용하면 Carbon 인스턴스 내부의 타임존이 직렬화에 반영됩니다. 보편적으로 애플리케이션의 `timezone` 설정이 적용되나, `timestamp` 컬럼(`created_at`, `updated_at`)은 언제나 UTC로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)로 캐스팅하는 것도 지원합니다. 모델의 `casts` 메서드에 속성과 Enum을 지정하면 됩니다.

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

캐스트 지정 후, 속성을 읽거나 저장할 때 Enum이 자동으로 이용됩니다.

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

단일 컬럼에 Enum 배열을 저장하려면, Laravel의 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다.

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

`encrypted` 캐스트는 Laravel 내장 [암호화](/docs/{{version}}/encryption) 기능을 사용해 속성 값을 암호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등은 각각의 비암호화 버전과 동일하게 동작하지만, 저장될 때 암호화된다는 점이 다릅니다.

암호화된 텍스트의 최종 길이는 예측이 어렵고 일반 텍스트보다 길기 때문에, 컬럼 타입을 반드시 `TEXT` 이상으로 지정하세요. 또한, 암호화된 값은 데이터베이스 내에서 검색/조회가 불가능합니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 애플리케이션의 `app` 설정파일의 `key` 값을 사용해 문자열을 암호화합니다. 일반적으로는 `.env`의 `APP_KEY` 값을 사용합니다. 만약 암호화 키를 교체해야 한다면, 기존 암호화된 속성을 반드시 새 키로 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

가끔은 쿼리 실행 중, 예를 들어 테이블에서 RAW 값을 선택할 때, 캐스팅을 적용하고 싶을 수 있습니다. 다음 쿼리를 예로 들어보겠습니다.

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

위 쿼리 결과의 `last_posted_at` 속성은 단순 문자열입니다. 쿼리 실행 시 해당 속성에 `datetime` 캐스팅을 적용하면 편리합니다. 이를 위해 `withCasts` 메서드를 사용할 수 있습니다.

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

Laravel에는 내장 캐스트 타입이 다양하게 있지만, 필요에 따라 직접 캐스트 타입을 만들 수 있습니다. 커스텀 캐스트 클래스를 만들려면 Artisan의 `make:cast` 명령어를 실행하세요. 새 캐스트 클래스는 `app/Casts` 디렉토리에 생성됩니다.

```shell
php artisan make:cast AsJson
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 반드시 `get`과 `set` 메서드를 포함해야 합니다. `get`은 DB의 원본 값을 캐스팅 값으로 변환하고, `set`은 캐스팅 값을 DB에 저장할 원본 값으로 변환합니다. 내장 `json` 캐스트 타입의 예시를 다시 구현해 보겠습니다.

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
     * 저장용 값 준비.
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

이렇게 만든 커스텀 캐스트 타입은 클래스명을 사용해 모델 속성에 지정할 수 있습니다.

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

캐스팅을 원시 타입에만 국한하지 않고, 오브젝트로 변환할 수도 있습니다. 커스텀 캐스트에서 오브젝트를 반환할 때, 여러 컬럼을 포함하는 값 객체라면 `set` 메서드가 저장할 값의 배열 또는 한 컬럼만 영향을 받는다면 값을 반환해야 합니다.

예를 들어, 여러 모델 속성을 하나의 `Address` 값 객체로 변환하는 캐스트 클래스를 다음과 같이 정의할 수 있습니다.

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
     * 저장할 값 준비.
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

값 객체로 캐스팅하면, 값 객체의 변경사항이 모델 저장 전 자동으로 동기화됩니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체가 포함된 Eloquent 모델을 배열 혹은 JSON으로 직렬화할 예정이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐시

값 객체로 캐스팅된 속성은 Eloquent에서 접근 시 캐시되어, 동일한 속성에 재접근하면 같은 인스턴스를 반환합니다.

커스텀 캐스트 클래스의 오브젝트 캐싱을 비활성화하려면, public 속성으로 `withoutObjectCaching`을 선언하면 됩니다.

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray`, `toJson`으로 배열 또는 JSON으로 변환할 때, 커스텀 캐스트 값 객체도 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현한다면 자동으로 직렬화됩니다. 단, 외부 라이브러리의 값 객체는 이 인터페이스 확장이 불가능할 수 있습니다.

이 경우, 커스텀 캐스트 클래스가 직접 직렬화 기능을 담당하도록 할 수 있습니다. 이를 위해 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하면 됩니다. 이 인터페이스는 값 객체의 직렬화를 반환하는 `serialize` 메서드를 요구합니다.

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
### 인바운드 캐스팅(Inbound Casting)

때로 커스텀 캐스트가 모델의 속성 할당(저장)만 다루고, 조회에는 아무 효과가 없는 동작이 필요할 수 있습니다.

이런 인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현(이 인터페이스는 오직 `set` 메서드만 필요)해야 합니다. Artisan 명령어에 `--inbound` 옵션을 추가하면 쉽게 생성할 수 있습니다.

```shell
php artisan make:cast AsHash --inbound
```

가장 흔한 용례는 "해싱" 캐스트입니다. 예를 들어, SHA 또는 bcrypt로 해싱 가능한 인바운드 캐스트 클래스를 만들 수 있습니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * 인스턴스 생성자.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장할 값 준비.
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

커스텀 캐스트를 모델에 지정할 때, 클래스명 다음에 `:`로 구분하여 파라미터(여러 개일 경우 ,로 구분)를 전달할 수 있습니다. 이 파라미터는 캐스트 클래스의 생성자로 전달됩니다.

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

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션의 값 객체 자체가 커스텀 캐스트 클래스를 정의하도록 만들 수도 있습니다. 커스텀 캐스트 클래스를 붙이는 대신 값 객체 클래스에 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하면 됩니다.

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스 구현체는 `castUsing` 메서드를 구현해야 하며, 해당 값 객체로 변환을 담당할 커스텀 캐스터 클래스명을 반환해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * 이 값 대상에서 캐스팅할 때 사용할 캐스터 클래스 반환
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```

Castable 클래스 사용 시, `casts` 정의에서 파라미터도 함께 전달할 수 있습니다. 전달된 파라미터는 `castUsing` 메서드에 인자로 넘어갑니다.

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

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합하면, 값 객체와 캐스팅 로직을 하나의 클래스(익명 캐스터)로 구현할 수 있습니다. 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하며, 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다.

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 값 대상에 대한 캐스팅에 사용할 캐스터 클래스 반환
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
