# Eloquent: 변이자(Mutators) & 캐스팅(Casting)

- [소개](#introduction)
- [접근자(Accessors)와 변이자(Mutators)](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변이자 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [열거형(Enums) 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자, 변이자, 그리고 속성 캐스팅은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 값을 변환할 수 있도록 해줍니다. 예를 들어, 데이터베이스에 저장할 때 [라라벨 암호화기](/docs/{{version}}/encryption)를 사용해 값을 암호화한 뒤, Eloquent 모델에서 속성에 접근할 때 자동으로 이를 복호화하고 싶을 때 사용할 수 있습니다. 또는, 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델을 통해 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자(Accessors)와 변이자(Mutators)

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성 값을 조회할 때 해당 값을 변환합니다. 접근자를 정의하려면, 모델에 보호된 메서드로 접근 가능한 속성을 표현하세요. 이 메서드의 이름은 가능하다면 실제 모델 속성/데이터베이스 컬럼의 "카멜 케이스(camel case)" 표현과 일치해야 합니다.

다음 예제에서는 `first_name` 속성의 접근자를 정의합니다. 이 접근자는 Eloquent가 `first_name` 속성을 조회할 때 자동으로 호출됩니다. 모든 속성 접근자/변이자 메서드는 반드시 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 반환해야 합니다:

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

모든 접근자 메서드는 속성이 어떻게 조회(및 선택적으로, 변경)될지 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예제에서는 속성이 어떻게 조회되는지만을 정의하고 있습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 전달했습니다.

보시는 것처럼, 컬럼의 원본 값이 접근자에 전달되므로 값을 조작하고 반환할 수 있습니다. 접근자의 값을 얻으려면 모델 인스턴스에서 `first_name` 속성에 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이러한 계산된 값들을 모델의 배열/JSON 표현에 추가하고 싶다면, [해당 속성들을 수동으로 추가해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체 만들기

때로는 접근자 안에서 여러 모델 속성을 "값 객체" 하나로 변환해야 할 수도 있습니다. 이럴 때는 `get` 클로저에서 두 번째 인자로 `$attributes`를 받을 수 있는데, 여기에 모델의 현재 모든 속성이 배열로 전달됩니다:

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

접근자에서 값 객체를 반환할 때, 값 객체에 어떤 변경이 발생하더라도 모델이 저장되기 전에 해당 변경 내용이 모델에 자동으로 반영됩니다. 이는 Eloquent가 접근자가 반환한 인스턴스를 보관해 두기 때문에, 접근자가 여러 번 호출되어도 동일한 인스턴스를 반환할 수 있기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만, 문자열이나 불린과 같은 원시(primitive) 값에 대해서도 연산 비용이 크다면 캐싱을 직접 켜고 싶을 때가 있습니다. 이런 경우, 접근자를 정의할 때 `shouldCache` 메서드를 사용할 수 있습니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로 객체 캐싱 기능을 끄고 싶다면, `withoutObjectCaching` 메서드를 사용할 수 있습니다:

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
### 변이자 정의하기

변이자는 Eloquent 속성 값을 설정할 때 해당 값을 변환합니다. 변이자를 정의하려면 속성을 정의할 때 `set` 인자를 지정하면 됩니다. 예를 들어, `first_name` 속성의 변이자를 정의해 보겠습니다. 이 변이자는 모델에 `first_name` 값을 설정할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름을 변환합니다.
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

변이자의 클로저는 속성에 설정될 값을 인자로 받아, 이를 조작한 후 반환할 수 있습니다. 변이자를 사용하려면, Eloquent 모델의 `first_name` 속성을 설정하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예제에서, `set` 콜백은 `Sally`라는 값을 받아 `strtolower` 함수를 적용해 모델의 내부 `$attributes` 배열에 설정하게 됩니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변이하기

때로는 변이자에서 여러 개의 실제 모델 속성을 설정해야 할 수도 있습니다. 이럴 때는 `set` 클로저에서 배열을 반환하면 되고, 각 배열의 키는 모델 속성명(혹은 데이터베이스 컬럼명)과 일치해야 합니다:

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

속성 캐스팅은 접근자/변이자와 비슷한 기능을 제공하지만, 별도의 메서드를 추가로 정의하지 않아도 됩니다. 대신, 모델의 `casts` 메서드에서 속성의 이름과 변환하고자 하는 타입을 키-값 쌍으로 반환하면 됩니다.

`casts` 메서드는 다음 타입을 지원합니다:

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

예시로, 데이터베이스에 정수형(`0` 또는 `1`)으로 저장된 `is_admin` 속성을 불린(Boolean) 값으로 캐스팅해보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들 반환
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

이렇게 캐스트를 정의하고 나면, 데이터베이스에서 정수로 저장되어 있어도 `is_admin` 속성을 항상 불리언으로 사용할 수 있습니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시로 새로운 캐스트를 추가하고 싶다면 `mergeCasts` 메서드로 기존 캐스트에 추가할 수 있습니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 관계 이름과 같은 이름의 캐스트나 모델의 기본키에 캐스트를 할당하지 마세요.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 모델 속성을 [유연한 `Illuminate\Support\Stringable` 객체](/docs/{{version}}/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들 반환
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

`array` 캐스트는 직렬화된 JSON이 저장된 컬럼을 사용할 때 유용합니다. 예를 들어, 데이터베이스의 컬럼 타입이 `JSON`, `TEXT` 등으로 되어 있고, 여기에 직렬화된 JSON이 저장된다면, 해당 속성에 `array` 캐스트를 추가하면 자동으로 PHP 배열로 역직렬화되어 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들 반환
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

이렇게 캐스트를 정의하면 `options` 속성에 접근할 때마다 JSON에서 PHP 배열로, 값을 설정할 때는 자동으로 배열이 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 하나의 필드만 간결하게 업데이트하려면, [속성을 대량 할당 가능하도록 만들고](/docs/{{version}}/eloquent#mass-assignment-json-columns) `update` 메서드에서 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

유니코드 문자를 이스케이프하지 않은 JSON으로 배열 속성을 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다:

```php
/**
 * 캐스팅할 속성들 반환
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

기본 `array` 캐스트도 충분히 유용하지만, 배열의 특정 항목만 직접 변경하려 하면 PHP 오류가 발생할 수 있습니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이는 [커스텀 캐스트](#custom-casts) 기능을 응용한 것으로, 개별 항목을 수정해도 PHP 오류가 발생하지 않도록 해 줍니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성들 반환
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

비슷하게, JSON 속성을 Laravel의 [Collection](/docs/{{version}}/collections) 인스턴스로 캐스팅하는 `AsCollection` 캐스트도 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성들 반환
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

`AsCollection` 캐스트에서 Laravel 기본 컬렉션 대신 커스텀 컬렉션 객체를 사용하려면 클래스명을 캐스트 인자로 전달하세요:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
    ];
}
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스(PHP `DateTime` 클래스 확장)로 캐스팅해 다양한 메서드를 제공합니다. 추가 날짜 속성이 필요하다면 모델의 `casts` 메서드에 `datetime` 또는 `immutable_datetime` 캐스트 타입을 사용해 정의할 수 있습니다.

`date` 또는 `datetime` 캐스트를 정의할 때, 날짜의 포맷도 지정할 수 있습니다. 이 포맷은 [모델을 배열이나 JSON으로 직렬화할 때](/docs/{{version}}/eloquent-serialization) 사용됩니다:

```php
/**
 * 캐스팅할 속성들 반환
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

컬럼이 날짜로 캐스팅되어 있다면, 해당 모델 속성에 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime`/`Carbon` 인스턴스를 설정할 수 있습니다. 값은 올바르게 변환되어 데이터베이스에 저장됩니다.

모든 모델의 날짜 직렬화 포맷을 커스텀하려면, 모델에 `serializeDate` 메서드를 정의하세요. 이 메서드는 데이터베이스에 저장하는 포맷에는 영향 주지 않습니다:

```php
/**
 * 배열/JSON 직렬화용 날짜 포맷 지정
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

모델의 날짜가 데이터베이스에 저장될 포맷을 지정하려면, `$dateFormat` 속성을 정의하세요:

```php
/**
 * 날짜 컬럼의 저장 포맷
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`와 `datetime` 캐스트는 앱의 `timezone` 설정과 무관하게 날짜를 UTC의 ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)으로 직렬화합니다. 이 포맷을 항상 사용하고, 앱의 날짜를 UTC에 저장하는 것을 권장합니다. 그렇게 하면 PHP, JavaScript 등 다른 날짜 라이브러리와의 호환성이 극대화됩니다.

만약 `date` 또는 `datetime` 캐스트에 `datetime:Y-m-d H:i:s`처럼 커스텀 포맷이 지정되어 있다면, Carbon 인스턴스의 내부 타임존이 직렬화에 사용됩니다. 보통 이는 앱의 `timezone` 설정값입니다. 단, `created_at`, `updated_at`와 같은 `timestamp` 컬럼은 항상 UTC로 형식화되며 앱의 타임존 설정과 무관합니다.

<a name="enum-casting"></a>
### 열거형(Enums) 캐스팅

Eloquent는 또한 속성 값을 PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)으로 캐스팅하는 기능을 제공합니다. 모델의 `casts` 메서드에 속성과 Enum 타입을 지정하세요:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성들 반환
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

이렇게 하면, 해당 속성에 Enum 인스턴스 할당 및 변환이 자동으로 이뤄집니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

모델 속성에 Enum 값의 배열이 하나의 컬럼에 저장되어야 할 때, Laravel이 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 이용할 수 있습니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅할 속성들 반환
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

`encrypted` 캐스트는 라라벨 내장 [암호화](/docs/{{version}}/encryption) 기능을 사용해 모델 속성 값을 암호화합니다. 뿐만 아니라, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등도 사용할 수 있으며, 저장 시 암호화된 값이 유지됩니다.

암호화된 텍스트의 길이는 예측이 어렵고 일반 텍스트보다 길어지므로, 해당 데이터베이스 컬럼이 반드시 `TEXT` 타입 이상이어야 합니다. 또한, 데이터베이스에 암호화되어 저장되므로 해당 속성 값으로는 직접 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 로테이션

라라벨은 앱의 `app` 설정 파일의 `key` 값(즉, `APP_KEY` 환경 변수)에 따라 문자열을 암호화합니다. 이 키를 변경해야 할 경우, 새 키로 암호화된 속성들을 수동으로 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

쿼리 실행 중, 예를 들어 테이블에서 raw 값을 select 할 때 캐스트를 적용하고 싶을 수 있습니다. 다음과 같은 쿼리를 예로 들어보겠습니다:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

`last_posted_at` 속성은 단순 문자열이 됩니다. 이 속성에 `datetime` 캐스트를 적용하고 싶을 경우, `withCasts` 메서드를 쿼리에 추가할 수 있습니다:

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

라라벨에는 다양한 내장 캐스트 타입이 있지만, 필요한 경우 직접 캐스트 타입을 정의할 수 있습니다. 캐스트를 만드려면 `make:cast` 아티즌 명령어를 사용하세요. 새로운 캐스트 클래스는 `app/Casts` 디렉토리에 생성됩니다:

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 반드시 `get`과 `set` 메서드를 정의해야 합니다. `get`은 데이터베이스에서 조회한 raw 값을 캐스트 값으로 변환하고, `set`은 캐스트 값을 데이터베이스에 저장할 수 있는 raw 값으로 변환합니다. 예시로 내장된 `json` 캐스트를 커스텀 캐스트로 다시 구현해 보겠습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * 값 캐스트
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }

    /**
     * 저장용 값 변환
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
```

커스텀 캐스트 타입을 정의했다면, 해당 클래스명을 모델 속성의 캐스트로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들 반환
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

값을 원시 타입이 아닌 객체로도 캐스팅할 수 있습니다. 값 객체로 캐스팅하는 커스텀 캐스트는 기본적인 원시 타입 캐스팅과 유사하지만, `set` 메서드는 저장 가능한 값들의 키-값 배열을 반환해야 합니다.

예시로, 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의해보겠습니다. `Address` 값 객체는 두 개의 공개 속성(`lineOne`, `lineTwo`)을 가진다고 가정합니다:

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
     * 값 캐스트
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
     * 저장용 값 변환
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

값 객체로 캐스팅할 때 객체의 값이 변경되면, 모델 저장 전에 변경 내용이 자동으로 모델에 반영됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable`과 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 해석되면, Eloquent가 캐시하므로 해당 속성에 재접근할 때마다 동일한 인스턴스를 반환합니다.

커스텀 캐스트 클래스에서 객체 캐싱을 비활성화하려면, 해당 클래스에 공개 속성 `withoutObjectCaching`을 정의하세요:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray`나 `toJson`으로 변환할 때, 커스텀 캐스트 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하고 있다면 직렬화됩니다. 하지만 서드파티 라이브러리의 값 객체 등 인터페이스를 추가할 수 없는 경우도 있을 수 있습니다.

이럴 땐 커스텀 캐스트 클래스에서 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해서 값 객체 직렬화 책임을 맡길 수 있습니다. 이 인터페이스는 `serialize` 메서드가 있으며, 이 메서드는 값 객체의 직렬화된 형태를 반환해야 합니다:

```php
/**
 * 값의 직렬화 표현 반환
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(Model $model, string $key, mixed $value, array $attributes): string
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 인바운드 캐스팅

때로는 모델에 값을 설정할 때만 변환이 필요한 경우가 있습니다. 이런 "인바운드 전용" 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, `set` 메서드만 정의하면 됩니다. 인바운드 전용 캐스트 클래스를 생성하려면 `--inbound` 옵션으로 `make:cast` 명령을 사용할 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

고전적인 인바운드 캐스트 예로 해시(hash) 처리가 있습니다. 다음과 같이 알고리즘을 지정해 들어오는 값을 해시 처리하는 캐스트를 만들 수 있습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 클래스 인스턴스 생성
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장할 값 준비
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

커스텀 캐스트를 모델에 지정할 때 `:` 문자로 클래스를 구분한 뒤, 여러 파라미터를 콤마로 구분해 생성자에 인자로 전달할 수 있습니다:

```php
/**
 * 캐스팅할 속성들 반환
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

애플리케이션의 값 객체에 자체적으로 커스텀 캐스트 클래스를 정의할 수 있도록 만들고 싶을 때가 있습니다. 이때 모델에 커스텀 캐스트 클래스가 아니라, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스명을 지정할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 객체는 `castUsing` 메서드를 반드시 정의해야 하며, 이 메서드는 해당 객체를 캐스팅하는 커스텀 캐스터 클래스명을 반환해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 이 캐스트 대상에서 사용할 캐스터 클래스명 반환
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

`Castable` 클래스 사용 시, `casts` 메서드 정의에서 인자를 전달할 수 있습니다. 이 인자는 `castUsing` 메서드로 전달됩니다:

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

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하면, 값 객체와 캐스팅 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하세요. 이 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 이 캐스트 대상에서 사용할 캐스터 클래스 반환
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
