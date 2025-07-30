# Eloquent: 변형자(Mutators) 및 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [엑세서(Accessors)와 뮤테이터(Mutators)](#accessors-and-mutators)
    - [엑세서 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅 (Attribute Casting)](#attribute-casting)
    - [배열과 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 실행 시 캐스팅](#query-time-casting)
- [사용자 정의 캐스트 (Custom Casts)](#custom-casts)
    - [값 객체 캐스팅 (Value Object Casting)](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 매개변수](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

엑세서(accessors), 뮤테이터(mutators), 그리고 속성 캐스팅(attribute casting)은 Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 그 값을 변환할 수 있게 해줍니다. 예를 들어, 데이터베이스에 값을 저장할 때 [Laravel 암호화 도구](/docs/11.x/encryption)를 사용해 값을 암호화하고, Eloquent 모델에서 접근할 때 자동으로 속성을 복호화하도록 설정할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델에서 접근할 때 자동으로 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 엑세서(Accessors)와 뮤테이터(Mutators)

<a name="defining-an-accessor"></a>
### 엑세서 정의하기

엑세서는 Eloquent 속성 값을 모델에서 접근할 때 변형하는 역할을 합니다. 엑세서를 정의하려면 모델에서 보호된(protected) 메서드를 작성하여 엑세스할 속성을 나타내야 합니다. 이 메서드 이름은 실제 모델 속성이나 데이터베이스 열 이름을 "카멜 케이스(camel case)" 형태로 표현한 이름과 일치해야 합니다.

예를 들어, `first_name` 속성에 대한 엑세서를 정의하려면, Eloquent가 이 속성의 값을 가져오려고 할 때 자동으로 호출될 엑세서 메서드를 다음과 같이 작성합니다. 모든 엑세서 및 뮤테이터 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 반환 타입을 선언해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first_name)을 가져옵니다.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```

모든 엑세서 메서드는 `Attribute` 인스턴스를 반환하며, 이 객체는 속성이 어떻게 접근되고, 선택적으로 변형(mutate)될지 정의합니다. 위 예제에서는 속성을 가져오는 방식만 정의했으며, `Attribute` 클래스 생성자에 `get` 인수를 전달했습니다.

컬럼의 원래 값이 엑세서에 전달되므로, 이 값을 조작하여 원하는 결과를 반환할 수 있습니다. 엑세서 값을 사용하려면, 모델 인스턴스에서 `first_name` 속성에 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]  
> 계산된(엑세서) 값을 모델의 배열 또는 JSON 표현에 반영하려면, [해당 속성들을 배열에 추가(append)해줘야 합니다](/docs/11.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로부터 값 객체 생성하기

때로는 하나의 엑세서에서 모델의 여러 속성을 조합해 하나의 "값 객체(value object)"로 변환해야 할 때가 있습니다. 이를 위해 `get` 클로저가 두 번째 인수로 `$attributes` 배열을 받을 수 있으며, 이 배열에는 현재 모델의 모든 속성이 들어있습니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소 정보를 다룹니다.
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

엑세서에서 값 객체를 반환하는 경우, 값 객체에 대한 변경 사항이 모델이 저장되기 전에 자동으로 모델에 동기화됩니다. 이는 Eloquent가 엑세서가 반환하는 인스턴스를 보존하여, 엑세서가 호출될 때마다 동일한 인스턴스를 반환하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

그러나 계산 비용이 큰 문자열이나 불리언과 같은 원시형 값에 대해서도 캐싱을 활성화하고 싶을 때가 있습니다. 이럴 때는 엑세서 정의 시 `shouldCache` 메서드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로 속성의 객체 캐싱 동작을 비활성화하려면, 엑세서 정의 시 `withoutObjectCaching` 메서드를 호출하면 됩니다:

```php
/**
 * 사용자의 주소 정보를 다룹니다.
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
### 뮤테이터 정의하기

뮤테이터는 Eloquent 속성에 값을 설정할 때 그 값을 변형하는 역할을 합니다. 뮤테이터를 정의하려면, 엑세서와 마찬가지로 `set` 인수를 지정하면 됩니다. 예를 들어, `first_name` 속성에 대한 뮤테이터를 정의하면, 해당 속성에 값을 설정할 때 자동으로 이 뮤테이터가 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first_name)을 다룹니다.
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

뮤테이터 클로저는 속성에 설정되는 값을 받아서 조작한 후, 조작된 값을 반환해야 합니다. 위 예제에서는 `Sally`가 입력되면 `strtolower`를 적용한 후 모델 내부의 `$attributes` 배열에 저장합니다.

뮤테이터를 사용하는 방법은 단순히 모델 인스턴스에서 속성에 값을 할당하는 것과 같습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<a name="mutating-multiple-attributes"></a>
#### 여러 속성을 변형하기

때로는 뮤테이터에서 근본 모델의 여러 속성을 설정해야 할 때가 있습니다. 이 경우, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델의 실제 속성(데이터베이스 컬럼)과 대응되어야 합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소 정보를 다룹니다.
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

속성 캐스팅은 엑세서와 뮤테이터와 유사한 기능을 제공하지만, 모델에 별도의 메서드를 정의하지 않아도 됩니다. 대신, 모델의 `casts` 메서드에서 배열을 반환해 해당 속성을 공통 데이터 타입으로 간편하게 변환할 수 있습니다.

`casts` 메서드 반환 배열의 키는 캐스팅할 속성 이름이며, 값은 캐스팅하려는 타입명입니다. 지원하는 캐스트 타입은 다음과 같습니다:

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

예를 들어, `is_admin`이라는 속성이 데이터베이스에는 정수형(`0` 또는 `1`)으로 저장되어 있지만, 모델에서는 불리언으로 다루고 싶다면 다음과 같이 캐스팅을 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들을 지정합니다.
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

캐스트를 정의한 후부터는 모델에서 `is_admin` 속성에 접근할 때 항상 불리언으로 변환된 값을 받게 됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

실행 중에 임시로 캐스트를 추가하고 싶을 경우에는 `mergeCasts` 메서드를 사용하면, 기존 캐스트에 병합됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]  
> `null` 값인 속성은 캐스팅되지 않습니다. 또한 관계명과 동일한 이름의 캐스트를 정의하거나, 모델의 기본 키 컬럼에 캐스트를 할당해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면, 모델 속성을 [플루언트(Fluent) `Illuminate\Support\Stringable` 객체](/docs/11.x/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스트할 속성들을 지정합니다.
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
### 배열(Array) 및 JSON 캐스팅

`array` 캐스트는 주로 JSON 직렬화된 컬럼을 다룰 때 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 타입 컬럼에 JSON 문자열이 저장되어 있다면, 해당 속성에 `array` 캐스트를 지정해 두면, Eloquent 모델에서 이 속성을 접근할 때 자동으로 JSON 문자열이 PHP 배열로 역직렬화(deserialize)됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스트할 속성들을 지정합니다.
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

이렇게 하면 `options` 속성을 읽으면 JSON이 배열로 변환되어 나오고, 설정할 때는 배열이 자동으로 직렬화되어 JSON으로 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 특정 필드만 간결하게 업데이트 하려면, [JSON 컬럼의 대량 할당(mass assignable)](/docs/11.x/eloquent#mass-assignment-json-columns) 허용 후 다음처럼 `->` 연산자를 사용해 `update` 메서드를 호출할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### 배열 객체(ArrayObject) 및 컬렉션(Collection) 캐스팅

표준 `array` 캐스트는 많이 사용되지만, 단점도 있습니다. `array` 캐스트는 원시형 타입을 반환하기 때문에 배열 오프셋(offset)을 직접 변형하는 것이 불가능합니다. 예를 들어 다음 코드는 PHP 오류를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value; // 오류 발생
```

이를 해결하기 위해 Laravel은 JSON 속성을 PHP [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이것은 Laravel의 [사용자 정의 캐스트(custom cast)](#custom-casts) 구현을 통해, 개별 오프셋이 변경될 때도 올바르게 캐싱하고 변환하여 오류를 막는 특수한 처리입니다. `AsArrayObject` 캐스트는 다음처럼 지정합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스트할 속성들을 지정합니다.
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

마찬가지로 Laravel은 해당 JSON 속성을 Laravel [컬렉션(Collection)](/docs/11.x/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스트할 속성들을 지정합니다.
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

만약 기본 컬렉션 클래스 대신 커스텀 컬렉션 클래스를 사용하고 싶다면 캐스트 인자로 클래스명을 전달하면 됩니다:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스트할 속성들을 지정합니다.
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

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 PHP `DateTime` 클래스를 확장하는 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 자동 캐스팅합니다. 추가 날짜 속성을 캐스팅하려면, 모델의 `casts` 메서드에 `date` 또는 `datetime`, 또는 `immutable_date`, `immutable_datetime` 타입을 추가하면 됩니다.

`date` 또는 `datetime` 캐스트 시 날짜 포맷을 지정할 수도 있으며, 지정한 포맷은 모델이 배열이나 JSON으로 직렬화될 때 사용됩니다:

```php
/**
 * 캐스트할 속성들을 지정합니다.
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

날짜 캐스팅된 속성에 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 할당할 수 있습니다. Eloquent가 올바르게 변환하여 데이터베이스에 저장합니다.

모델의 모든 날짜 직렬화 기본 포맷을 직접 지정하고 싶다면, 모델에 `serializeDate` 메서드를 정의하세요. 이 메서드는 데이터베이스 저장 시 포맷에는 영향을 주지 않습니다:

```php
/**
 * 배열 또는 JSON 직렬화를 위한 날짜를 준비합니다.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 저장할 날짜 포맷은 `$dateFormat` 속성으로 지정할 수 있습니다:

```php
/**
 * 모델 날짜 컬럼의 저장 형식입니다.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스팅은 모델 직렬화 시 애플리케이션의 `timezone` 설정과 관계없이 UTC ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 변환됩니다. Laravel에서는 애플리케이션 전체에서 UTC 타임존을 일관되게 사용하는 것을 권장합니다. 이 방식이 PHP와 JavaScript 기반 다른 날짜 라이브러리와의 최대 호환성을 보장합니다.

`datetime:Y-m-d H:i:s`와 같은 커스텀 포맷을 지정하면, 직렬화 시 내부 Carbon 인스턴스의 타임존(보통 애플리케이션 timezone 설정)이 사용됩니다. 다만, `created_at`, `updated_at` 같은 `timestamp` 컬럼은 예외로 항상 UTC로 직렬화됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로 속성을 캐스팅할 수도 있습니다. 이를 위해 모델의 `casts` 메서드에서 속성과 Enum 클래스를 지정하세요:

```php
use App\Enums\ServerStatus;

/**
 * 캐스트할 속성들을 지정합니다.
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

캐스팅 이후부터는 해당 속성에 Enum 인스턴스가 자동으로 캐스팅되어, Enum 값을 쉽게 비교하거나 변경할 수 있습니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

때로는 모델의 한 컬럼에 Enum 값 배열을 저장해야 할 때가 있습니다. 이 경우 Laravel이 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스트할 속성들을 지정합니다.
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

`encrypted` 캐스트는 Laravel 내장 [암호화 기능](/docs/11.x/encryption)을 이용해 모델 속성을 암호화해서 저장합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트도 일반 캐스트와 마찬가지로 작동하지만, 실제 데이터는 데이터베이스에 암호화된 상태로 저장됩니다.

암호화된 텍스트의 길이는 예측 불가능하고 평문보다 길기 때문에, 데이터베이스 컬럼은 반드시 `TEXT` 타입 이상의 충분한 크기로 지정하는 것이 좋습니다. 또한 암호화된 속성은 데이터베이스에서 직접 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 `app` 설정 파일의 `key`값(보통 환경 변수 `APP_KEY`)을 사용해 문자열을 암호화합니다. 만약 암호화 키를 변경해야 한다면, 암호화된 속성들의 값을 새 키로 수동 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 실행 시 캐스팅

가끔 쿼리 실행 과정에서 캐스팅을 적용해야 할 때가 있습니다. 예를 들어, 생 RAW 값이나 서브쿼리를 선택할 경우입니다. 예를 들어 다음 쿼리를 보세요:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리에서 `last_posted_at` 속성은 단순 문자열입니다. 이 값을 `datetime`으로 캐스팅하고 싶으면, `withCasts` 메서드를 활용할 수 있습니다:

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
## 사용자 정의 캐스트 (Custom Casts)

Laravel에는 여러 유용한 내장 캐스트 타입이 있지만, 필요에 따라 직접 캐스트 타입을 정의할 수도 있습니다. 캐스트 클래스를 생성하려면 `make:cast` Artisan 명령어를 사용하세요. 새 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast Json
```

모든 사용자 정의 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 `get`과 `set` 메서드 정의를 요구합니다. `get` 메서드는 데이터베이스의 원시(raw) 값을 변환하여 캐스트된 값으로 반환하고, `set` 메서드는 캐스트된 값을 원시로 변환해 데이터베이스에 저장할 수 있게 합니다.

예를 들어, 내장된 `json` 캐스트를 사용자 정의 캐스트로 재구현하는 방법은 다음과 같습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * 주어진 값을 캐스팅합니다.
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

이제 사용자 정의 캐스트를 모델의 속성에 클래스명으로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스트할 속성들을 지정합니다.
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
### 값 객체 캐스팅 (Value Object Casting)

캐스팅할 값은 원시 타입에만 국한되지 않고 객체로도 가능하며, 여러 모델 값을 하나의 값 객체로 묶을 수도 있습니다. 이 경우 `set` 메서드는 모델 내부에 저장할 원시 키/값 배열을 반환해야 합니다.

예를 들어, 두 개의 모델 속성을 하나의 `Address` 값 객체로 캐스팅하는 사용자 정의 캐스트 클래스는 다음과 같습니다. `Address` 클래스는 `lineOne`, `lineTwo`라는 퍼블릭 속성이 있다고 가정합니다:

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
     * 주어진 값을 캐스팅합니다.
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
            throw new InvalidArgumentException('입력 값이 Address 인스턴스가 아닙니다.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅된 속성은 모델이 저장되기 전에 변경 사항이 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]  
> 값 객체가 들어있는 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent가 내부적으로 캐싱하므로, 동일 속성을 다시 접근하면 같은 객체 인스턴스가 반환됩니다.

이 객체 캐싱 기능을 비활성화하고 싶다면, 사용자 정의 캐스트 클래스에 `withoutObjectCaching`이라는 public 프로퍼티를 선언하고 `true`로 설정하세요:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델이 `toArray` 및 `toJson` 메서드로 변환될 때, 사용자 정의 캐스트에서 반환하는 값 객체들도 일반적으로 `Arrayable` 또는 `JsonSerializable` 인터페이스를 구현했다면 정상적으로 직렬화됩니다. 하지만 서드파티 라이브러리의 값 객체는 이들 인터페이스 구현이 어려울 수 있습니다.

이 경우 사용자 정의 캐스트 클래스가 값 객체를 직접 직렬화하도록 지정할 수 있습니다. `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고 `serialize` 메서드를 정의하면 됩니다:

```php
/**
 * 값 객체의 직렬화된 표현을 반환합니다.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(Model $model, string $key, mixed $value, array $attributes): string
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 인바운드 캐스팅 (Inbound Casting)

가끔 모델에 값을 설정(set)할 때만 변환하고, 모델에서 값을 가져올 때는 아무 작업도 하지 않는 사용자 정의 캐스트가 필요할 수 있습니다.

이런 "인바운드 전용" 캐스트는 `CastsInboundAttributes` 인터페이스를 구현하며, `set` 메서드만 정의하면 됩니다. Artisan 명령어의 `--inbound` 옵션을 사용해 인바운드 캐스트 클래스를 생성할 수도 있습니다:

```shell
php artisan make:cast Hash --inbound
```

대표적인 예로 해시 캐스트가 있습니다. 예를 들어, 전달받은 값을 지정된 알고리즘으로 해시하는 캐스트는 다음과 같습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 클래스 인스턴스를 생성합니다.
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
### 캐스트 매개변수

사용자 정의 캐스트를 모델에 붙일 때, 클래스명 뒤에 `:`를 붙이고 쉼표로 구분한 매개변수를 전달할 수 있으며, 이 매개변수들은 캐스트 클래스 생성자의 인자로 전달됩니다:

```php
/**
 * 캐스트할 속성들을 지정합니다.
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
### 캐스터블(Castables)

애플리케이션의 값 객체가 스스로 캐스트를 정의할 수 있게 하려면, 모델에 직접 사용자 정의 캐스트 클래스를 붙이는 대신, 값 객체 클래스가 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하도록 할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 클래스는 반드시 `castUsing` 메서드를 정의하여 이 클래스의 캐스팅을 책임질 캐스터 클래스명을 반환해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 본 객체에 대한 캐스터 클래스를 반환합니다.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

`Castable` 클래스를 사용할 때에도 `casts` 메서드에서 값을 설정하며, 인자를 전달하고 싶다면 클래스명 뒤에 붙이면 됩니다. 이 인자는 `castUsing` 메서드에 전달됩니다:

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
#### 캐스터블과 익명 클래스 활용

PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 캐스터블을 조합하면, 값 객체와 캐스팅 로직을 하나의 객체로 정의할 수 있습니다. 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현하는 익명 클래스를 반환하면 됩니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 본 객체에 대한 캐스터 클래스를 익명 클래스로 반환합니다.
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