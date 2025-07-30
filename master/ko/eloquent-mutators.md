# Eloquent: 변성자(Mutators) & 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [접근자(Accessors)와 변성자(Mutators)](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변성자 정의하기](#defining-a-mutator)
- [속성(Attribute) 캐스팅](#attribute-casting)
    - [배열과 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시점(Query Time) 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅(Value Object Casting)](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅(Inbound Casting)]
    - [캐스트 파라미터](#cast-parameters)
    - [Castable 인터페이스](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

접근자(accessors), 변성자(mutators), 그리고 속성 캐스팅(attribute casting)을 사용하면 모델 인스턴스에서 Eloquent 속성 값을 조회하거나 설정할 때 그 값을 변환할 수 있습니다. 예를 들어, 데이터베이스에 저장할 때 값을 Laravel 암호화기([encrypter](/docs/master/encryption))로 암호화하고, Eloquent 모델을 통해 접근할 때 자동으로 복호화하고 싶을 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델에서 접근할 때 배열로 변환하고 싶을 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자(Accessors)와 변성자(Mutators)

<a name="defining-an-accessor"></a>
### 접근자 정의하기 (Defining an Accessor)

접근자는 속성 값을 읽을 때 해당 값을 변환하는 기능입니다. 접근자를 정의하려면, 모델에 접근 가능한 속성을 나타내는 `protected` 메서드를 만드십시오. 이 메서드의 이름은 실제 모델 속성(데이터베이스 컬럼) 이름을 카멜케이스(camelCase) 형식으로 표현한 이름과 일치해야 합니다.

아래 예에서는 `first_name` 속성에 대한 접근자를 정의합니다. 이 접근자는 Eloquent가 `first_name` 속성 값을 가져올 때 자동으로 호출됩니다. 모든 접근자 및 변성자 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute`를 반환 타입 힌트로 선언해야 합니다:

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

모든 접근자 메서드는 `Attribute` 인스턴스를 반환하며, 이 인스턴스는 속성이 어떻게 접근되고(그리고 선택적으로 변형될지) 정의합니다. 이 예제에서는 `get` 인수를 사용하여 속성이 어떻게 접근되는지 정의했습니다.

보시다시피 컬럼의 원래 값이 접근자에 전달되어 원하는 대로 조작하고 반환할 수 있습니다. 접근자의 값을 가져오려면 모델 인스턴스에서 해당 속성에 바로 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 이러한 계산된 값을 모델의 배열 또는 JSON 표현에 추가하고 싶다면, [값을 배열/JSON에 추가하기](/docs/master/eloquent-serialization#appending-values-to-json) 기능을 사용하십시오.

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로부터 값 객체 만들기

가끔은 접근자가 여러 속성을 조합해 단일 "값 객체(value object)"로 변환해야 할 경우가 있습니다. 이렇게 하려면 `get` 클로저에 두 번째 인수로 `$attributes` 배열을 받을 수 있으며, 이는 현재 모델의 모든 속성을 포함합니다:

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

접근자가 값 객체를 반환하면, 해당 값 객체에 대한 모든 변경사항은 모델이 저장되기 전에 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자가 반환하는 인스턴스를 유지하여 접근자가 호출될 때마다 같은 인스턴스를 반환하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

단, 문자열이나 불리언 같은 원시값에 대한 캐싱을 활성화하고 싶을 때도 있습니다. 특히 계산 비용이 높은 값일 경우에 유용합니다. 이를 위해 접근자를 정의할 때 `shouldCache` 메서드를 호출하십시오:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

만약 객체 캐싱을 비활성화하고 싶다면, 속성을 정의할 때 `withoutObjectCaching` 메서드를 호출합니다:

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
### 변성자 정의하기 (Defining a Mutator)

변성자는 속성 값을 설정할 때 그 값을 변환하는 기능입니다. 변성자를 정의하려면, `Attribute` 정의 시 `set` 인수를 제공하면 됩니다. 예를 들어, `first_name` 속성에 대한 변성자를 정의해보겠습니다. 이 변성자는 모델에서 해당 속성 값을 설정할 때 자동으로 호출됩니다:

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

변성자 클로저는 설정하려는 값을 인수로 받으며, 이를 원하는 방식으로 조작해 반환하면 모델 내부의 `$attributes` 배열에 저장됩니다.

사용 예:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예제에서 `'Sally'` 값이 `set` 콜백으로 전달되고, `strtolower` 함수가 적용된 후 소문자 버전이 내부 속성 배열에 저장됩니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변형하기

가끔 변성자가 여러 속성을 동시에 설정해야 할 때가 있습니다. 이럴 경우 `set` 클로저에서 배열을 반환하여 각 키에 대응하는 실제 속성을 지정할 수 있습니다:

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
## 속성(Attribute) 캐스팅

속성 캐스팅은 접근자와 변성자와 유사하게 작동하지만, 별도의 메서드를 정의하지 않고도 모델의 `casts` 메서드를 통해 기본 데이터 타입으로 속성을 변환하는 편리한 방법입니다.

`casts` 메서드는 키가 변환할 속성 이름이고, 값은 변환하려는 타입인 배열을 반환해야 합니다. 지원되는 캐스트 타입은 다음과 같습니다:

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

예를 들어, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언으로 캐스팅해보겠습니다:

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

캐스트를 정의한 후 `is_admin` 속성은 항상 불리언으로 접근됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시 캐스트를 추가하려면 `mergeCasts` 메서드를 사용할 수 있습니다. 이렇게 하면 기존 캐스트에 추가됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` 값은 캐스팅되지 않습니다. 또한, 관계명과 동일한 이름의 캐스트 또는 속성을 정의하거나 모델의 기본 키에 캐스트를 할당해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용해, 속성을 [Illuminate\Support\Stringable 객체](https://laravel.kr/docs/9.x/strings#fluent-strings-method-list)로 캐스팅할 수 있습니다:

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
### 배열과 JSON 캐스팅 (Array and JSON Casting)

`array` 캐스트는 직렬화된 JSON 컬럼을 다룰 때 유용합니다. 데이터베이스 내 `JSON` 또는 `TEXT` 타입 컬럼이 JSON 문자열일 경우, `array` 캐스트를 지정하면 Eloquent 모델에서 접근할 때 자동으로 JSON 문자열이 PHP 배열로 변환되고, 할당 시에는 배열이 JSON으로 직렬화됩니다:

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

캐스트 정의 후, `options` 속성에 접근하면 PHP 배열로 역직렬화되고, 배열을 변경해 다시 할당하면 자동으로 JSON 문자열로 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 컬럼 내 특정 필드만 업데이트하려면, 해당 속성을 대량 할당 가능(mass assignable)하게 만들고, `update` 메서드와 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="json-and-unicode"></a>
#### JSON과 유니코드

배열 속성을 유니코드 이스케이프 없이 JSON으로 저장하고 싶으면 다음과 같이 `json:unicode` 캐스트를 사용하세요:

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

기본 `array` 캐스트는 충분히 활용 가능하지만, 배열의 개별 요소를 직접 수정할 수 없다는 단점이 있습니다. 예를 들어, 아래와 같이 배열 요소를 직접 변경하려고 하면 PHP 오류가 발생합니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 `AsArrayObject` 캐스트를 제공하는데, 이 캐스트는 JSON 속성을 PHP [ArrayObject 클래스](https://www.php.net/manual/en/class.arrayobject.php)로 변환합니다. Laravel의 커스텀 캐스트 기능을 활용해 객체 캐싱과 변환을 지능적으로 처리해 줍니다. 사용하는 방법은 다음과 같습니다:

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

비슷하게, `AsCollection` 캐스트는 JSON 속성을 Laravel [컬렉션(Collection)](/docs/master/collections) 인스턴스로 변환합니다:

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

`AsCollection` 캐스트가 Laravel 기본 컬렉션 대신 커스텀 컬렉션 클래스를 인스턴스화하도록 하려면, 컬렉션 클래스 이름을 인수로 전달하면 됩니다:

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

<a name="date-casting"></a>
### 날짜 캐스팅 (Date Casting)

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP `DateTime` 클래스를 상속받아 유용한 메서드를 제공합니다. 추가로 캐스팅할 날짜 타입이 있다면 모델의 `casts` 메서드 내에 `date`, `datetime`, `immutable_date`, `immutable_datetime` 타입으로 지정하세요.

날짜 캐스트에 대해 포맷을 지정할 수도 있으며, 이 포맷은 [모델을 배열이나 JSON으로 직렬화할 때](/docs/master/eloquent-serialization) 사용됩니다:

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

날짜 캐스트 컬럼에 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜+시간 문자열, 또는 `DateTime` / `Carbon` 인스턴스를 설정할 수 있으며, 올바르게 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜의 기본 직렬화 포맷을 변경하려면, 모델에 `serializeDate` 메서드를 정의합니다. 이 메서드는 데이터베이스 저장 포맷에는 영향을 미치지 않습니다:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 저장할 때 사용할 날짜 포맷은 `$dateFormat` 속성을 통해 지정할 수 있습니다:

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

기본적으로 `date` 및 `datetime` 캐스트는 애플리케이션 `timezone` 설정과 무관하게 UTC ISO-8601 형식(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)으로 직렬화됩니다. 애플리케이션 내에서 UTC 타임존을 일관되게 사용하는 것을 권장합니다. 이는 PHP/JavaScript 등 다른 날짜 라이브러리와의 최대 호환성을 보장해줍니다.

만약 `datetime:Y-m-d H:i:s`와 같은 커스텀 포맷을 쓰면, 내부의 Carbon 인스턴스 타임존이 직렬화 시 사용됩니다. 보통 이는 애플리케이션 `timezone` 설정과 일치할 것입니다. 단, `created_at`, `updated_at` 같은 `timestamp` 타입은 예외로 항상 UTC 기준으로 포맷됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로 캐스팅할 수 있습니다. 모델의 `casts` 메서드에 속성과 Enum 클래스를 지정하면 됩니다:

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

이렇게 하면 해당 속성에 접근할 때 Enum 객체로 자동 변환되고, Enum 값으로 설정하면 자동으로 기본 값으로 저장됩니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

몇몇 경우 하나의 컬럼에 Enum 값 배열을 저장해야 할 때가 있습니다. 이때 Laravel이 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

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
### 암호화된 캐스팅 (Encrypted Casting)

`encrypted` 캐스트는 Laravel의 내장 [암호화](/docs/master/encryption) 기능을 사용해 속성 값을 암호화해 저장합니다. 이 밖에도 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트가 제공되며, 평범한 캐스트와 동일하지만 저장 시 값이 암호화됩니다.

암호화된 값의 최종 길이가 예측 불가능하고 평문보다 더 길어지므로, 관련 데이터베이스 컬럼은 `TEXT` 타입 이상이어야 합니다. 또, 암호화된 값은 조회나 검색이 불가능하니 유의하세요.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 `app` 설정 파일의 `key` 값(`APP_KEY` 환경변수와 동일)을 사용해 문자열을 암호화합니다. 만약 암호화 키를 교체할 경우, 암호화된 속성 값을 새 키로 수동 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점(Query Time) 캐스팅

쿼리 시점에 캐스팅을 적용해야 할 때도 있습니다. 예를 들어, 다음과 같은 쿼리를 보십시오:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```

위 쿼리에서 결과의 `last_posted_at` 속성은 문자열로 반환됩니다. 실행 시점에 `datetime` 캐스트를 적용하려면 `withCasts` 메서드를 사용하면 됩니다:

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

Laravel은 여러 내장 캐스트 타입을 제공하지만, 상황에 따라 직접 커스텀 캐스트를 작성할 수도 있습니다. 캐스트 클래스를 만들려면 `make:cast` Artisan 명령어를 실행하세요. 새 클래스를 `app/Casts` 디렉터리에 생성합니다:

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, `get`과 `set` 메서드를 정의해야 합니다. `get`은 데이터베이스의 원시 값을 캐스팅된 값으로 변환하고, `set`은 캐스팅된 값을 데이터베이스에 저장 가능한 원시 값으로 변환합니다.

아래는 내장 `json` 캐스트를 커스텀 캐스트로 구현한 예제입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
```

커스텀 캐스트를 정의한 후에는, 모델의 `casts` 메서드에 캐스트 클래스명을 지정해 연결할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
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
            'options' => Json::class,
        ];
    }
}
```

<a name="value-object-casting"></a>
### 값 객체 캐스팅 (Value Object Casting)

캐스팅은 원시 타입에만 국한되지 않고 객체 타입으로도 할 수 있습니다. 객체형 커스텀 캐스트는 원시형 캐스트와 유사하지만, `set` 메서드는 모델에 저장할 원시 값들의 키/값 배열을 반환해야 합니다.

예를 들어, 여러 모델 속성을 조합해 `Address` 값 객체로 캐스팅하는 커스텀 캐스트를 구현합니다. 이 값 객체는 `lineOne`, `lineTwo`라는 두 개의 공개 속성을 가진다고 가정합니다:

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
     * Cast the given value.
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
     * Prepare the given value for storage.
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

값 객체 캐스팅 시, 값 객체에서 이루어진 변경사항은 모델이 저장되기 전에 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함하는 Eloquent 모델을 JSON이나 배열로 직렬화할 때는, 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하도록 하십시오.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 조회될 때 Eloquent가 캐시해서, 같은 속성에 접근하면 동일한 객체 인스턴스를 반환합니다.

커스텀 캐스트 클래스에서 객체 캐싱을 비활성화하려면, 클래스에서 공개된 `withoutObjectCaching` 속성을 선언하면 됩니다:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화 (Array / JSON Serialization)

Eloquent 모델이 `toArray` 또는 `toJson` 메서드로 배열 또는 JSON으로 변환될 때, 커스텀 캐스트가 반환하는 값 객체는 보통 `Arrayable`, `JsonSerializable` 인터페이스를 구현하면 자동으로 직렬화됩니다. 그러나 서드파티 라이브러리의 값 객체처럼 이 인터페이스들이 구현되어 있지 않을 수도 있습니다.

따라서, 커스텀 캐스트 클래스가 직접 값 객체를 직렬화하도록 할 수 있습니다. 이를 위해, 캐스트 클래스는 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고 `serialize` 메서드를 정의해야 합니다. 이 메서드는 값 객체의 직렬화된 표현을 반환합니다:

```php
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(Model $model, string $key, mixed $value, array $attributes): string
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 인바운드 캐스팅(Inbound Casting)

때때로 모델에 값을 설정할 때만 변환하고, 조회 시에는 아무 작업도 하지 않는 캐스트가 필요할 수 있습니다.

이 경우 `CastsInboundAttributes` 인터페이스를 구현하는 커스텀 캐스트를 작성해야 하며, `set` 메서드만 정의하면 됩니다. `make:cast` Artisan 명령어에 `--inbound` 옵션을 주어 인바운드 전용 캐스트 클래스를 만들 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

전형적인 인바운드 전용 캐스트 예로, 입력 값을 해싱하는 캐스트가 있습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
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
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return is_null($this->algorithm)
            ? bcrypt($value)
            : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
### 캐스트 파라미터 (Cast Parameters)

커스텀 캐스트에 파라미터를 전달해야 할 때는 클래스명 뒤에 `:` 기호로 구분하여 쉼표로 여러 인수를 전달할 수 있습니다. 전달된 파라미터들은 캐스트 클래스 생성자의 인수로 전달됩니다:

```php
/**
 * Get the attributes that should be cast.
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
### Castable 인터페이스

애플리케이션의 값 객체 클래스가 자체적으로 커스텀 캐스트를 정의하도록 허용할 수도 있습니다. 이때는 모델에 직접 커스텀 캐스트 클래스를 연결하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 `casts` 메서드에 지정하세요:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```

`Castable` 인터페이스를 구현한 클래스는 `castUsing` 메서드를 선언해야 하며, 이 메서드는 캐스팅을 책임질 커스터마이즈된 캐스트 클래스를 반환합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

`Castable` 클래스를 사용할 때도 `casts` 정의 시 인수를 전달할 수 있으며, 이 인수들은 `castUsing` 메서드로 전달됩니다:

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
#### Castable과 익명 캐스트 클래스 (Castables & Anonymous Cast Classes)

PHP 익명 클래스(anonymous classes)를 활용하면, 값 객체와 캐스팅 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현하는 익명 클래스를 반환하면 됩니다:

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