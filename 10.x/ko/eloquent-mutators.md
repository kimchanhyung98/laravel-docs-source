# Eloquent: 뮤테이터 및 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [엑세서(Accessor) 및 뮤테이터(Mutator)](#accessors-and-mutators)
    - [엑세서 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅 (Attribute Casting)](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트 (Custom Casts)](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

엑세서(accessors), 뮤테이터(mutators), 그리고 속성 캐스팅(attribute casting)은 Eloquent 모델 인스턴스의 속성 값을 가져오거나 설정할 때 값을 변환할 수 있게 해줍니다. 예를 들어, 데이터베이스에 저장할 때 [Laravel 암호화기(Laravel encrypter)](/docs/10.x/encryption)를 사용해 값을 암호화하고, Eloquent 모델에서 해당 속성에 접근할 때 자동으로 복호화할 수 있습니다. 혹은 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델로 접근할 때 PHP 배열로 변환하고자 할 수 있습니다.

<a name="accessors-and-mutators"></a>
## 엑세서(Accessor) 및 뮤테이터(Mutator)

<a name="defining-an-accessor"></a>
### 엑세서 정의하기

엑세서는 Eloquent 속성의 값을 읽을 때 변환하는 기능입니다. 엑세서를 정의하려면, 모델 내에 보호된(protected) 메서드를 만들고 이 메서드 이름은 실제 모델 속성 혹은 데이터베이스 컬럼명을 카멜케이스(camelCase) 형태로 표현해야 합니다.

예를 들어, `first_name` 속성에 대한 엑세서를 정의해 보겠습니다. 이 엑세서는 `first_name` 속성 값을 가져올 때 자동으로 호출됩니다. 모든 엑세서 및 뮤테이터 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute`를 반환 타입 힌트로 선언해야 합니다.

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

모든 엑세서 메서드는 `Attribute` 인스턴스를 반환하는데, 이 인스턴스는 속성을 어떻게 읽을지(get), 그리고 선택적으로 어떻게 쓸지(set)를 정의합니다. 위 예제에서는 읽기 방법만 정의했습니다. `get` 인수에 전달한 콜백이 실제 원본 컬럼 값 `$value`를 받아 조작 후 반환하는 방식입니다.

엑세서 값에 접근하려면, 모델 인스턴스에서 해당 속성을 간단히 조회하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]  
> 엑세서로 계산된 값을 모델의 배열 혹은 JSON 표현에 포함시키려면, [해당 속성을 append 해야 합니다](/docs/10.x/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 생성하기

엑세서가 여러 모델 속성을 결합해 단일 "값 객체(value object)"를 반환하도록 할 수도 있습니다. 이 경우 `get` 콜백은 두 번째 인수로 `$attributes` 배열을 받을 수 있는데, 여기에 모델의 모든 현재 속성들이 담겨 자동으로 전달됩니다.

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소를 다룹니다.
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

값 객체를 반환하는 엑세서에서, 값 객체에 한 번 변경을 가하면 모델이 저장되기 전에 해당 변경 사항이 모델에 자동으로 동기화됩니다. 이는 Eloquent가 엑세서가 반환하는 인스턴스를 캐싱하여, 엑세서가 다시 호출될 때 같은 인스턴스를 반환하기 때문입니다.

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

반면 문자열이나 불값처럼 계산 비용이 높은 원시 값에 대해서도 캐싱하고 싶을 때는, 엑세서 정의 시 `shouldCache` 메서드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 객체 캐싱을 끄고 싶으면 `withoutObjectCaching` 메서드를 호출하세요:

```php
/**
 * 사용자의 주소를 다룹니다.
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

뮤테이터는 Eloquent 속성에 값을 설정할 때 변환됩니다. 뮤테이터를 정의하려면, 엑세서를 정의할 때와 비슷하게 `set` 인수를 제공하면 됩니다. 다음은 `first_name` 속성에 대한 뮤테이터 예제이며, 이 뮤테이터는 `first_name` 속성에 값을 설정할 때 자동 호출됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름을 다룹니다.
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

뮤테이터 콜백은 해당 속성에 설정되는 원래 값을 받아 조작한 뒤 변환된 값을 반환하며, 내부 `$attributes` 배열에 저장합니다. 뮤테이터를 사용하려면 Eloquent 모델의 해당 속성에 값을 할당하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 경우, `set` 콜백은 `Sally` 값을 받아 모든 문자를 소문자로 변환해 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변형하기

때로는 뮤테이터가 여러 속성을 동시에 변경해야 할 수도 있습니다. 이 경우 `set` 클로저에서 배열을 반환하면, 배열의 키가 속성명과 매치되어 여러 속성을 한 번에 설정할 수 있습니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소를 다룹니다.
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

속성 캐스팅은 엑세서, 뮤테이터를 따로 정의하지 않고도 모델의 `$casts` 속성을 통해 일반적인 데이터 타입으로 속성을 자동 변환할 수 있는 편리한 기능입니다.

`$casts` 프로퍼티는 배열이며, 키는 캐스팅할 속성명, 값은 캐스팅할 타입을 지정합니다. 지원하는 타입은 다음과 같습니다:

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

예를 들어, 데이터베이스에 `0` 또는 `1`로 저장된 `is_admin` 속성을 불리언으로 캐스팅해보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들.
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}
```

이렇게 하면 `is_admin`에 접근할 때 항상 불리언 타입으로 자동 변환됩니다.

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```

런타임에 임시 캐스팅을 추가할 경우, `mergeCasts` 메서드를 이용할 수 있습니다. 이 정의는 기존 캐스팅에 병합됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]  
> `null` 값인 속성은 캐스팅되지 않습니다. 또한 관계 이름과 같은 이름의 캐스트나 모델의 기본키(primary key)에 대한 캐스트는 정의해서는 안 됩니다.

<a name="stringable-casting"></a>
#### 스트링어블(Stringable) 캐스팅

속성을 [fluent `Illuminate\Support\Stringable` 객체](/docs/10.x/strings#fluent-strings-method-list)로 캐스팅하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들.
     *
     * @var array
     */
    protected $casts = [
        'directory' => AsStringable::class,
    ];
}
```

<a name="array-and-json-casting"></a>
### 배열 및 JSON 캐스팅

`array` 캐스트는 직렬화된 JSON을 저장하는 컬럼에 매우 유용합니다. 데이터베이스 컬럼이 `JSON` 또는 `TEXT` 타입으로 JSON 직렬화된 값을 저장할 때, 해당 속성에 `array` 캐스트를 설정하면 Eloquent 모델에서 자동으로 PHP 배열로 역직렬화됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들.
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}
```

이제 `options` 속성에 접근하면 JSON 문자열이 자동으로 배열로 변환되며, 값을 설정하면 다시 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 특정 필드만 간단히 갱신하려면, 해당 속성을 [대량 할당 가능(mass assignable)](/docs/10.x/eloquent#mass-assignment-json-columns)으로 만들고 `->` 연산자를 이용해 `update` 메서드에 다음과 같이 전달하세요:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### 배열 객체(ArrayObject) 및 컬렉션 캐스팅

일반적인 `array` 캐스트는 동작은 하지만 한계가 있습니다. 반환 값이 원시 배열이므로 배열의 개별 오프셋을 직접 변경할 수 없어 다음과 같은 코드는 PHP 오류가 발생합니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이를 해결하기 위해 Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 인스턴스로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts) 기능을 이용해 구현되어, 개별 오프셋 변경 시에도 오류 없이 캐싱과 변환을 지능적으로 관리합니다. 사용법은 다음과 같습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

마찬가지로 Laravel은 JSON 속성을 [컬렉션(Collection)](/docs/10.x/collections) 인스턴스로 캐스팅하는 `AsCollection` 캐스트도 제공합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

`AsCollection` 캐스트가 Laravel 기본 컬렉션 대신 커스텀 컬렉션 클래스를 인스턴스화 하도록 하려면, 캐스트 인수로 컬렉션 클래스명을 제공하세요:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class.':'.OptionCollection::class,
];
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 PHP `DateTime` 클래스를 확장한 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. 추가적인 날짜 속성도 모델의 `$casts` 배열에 `datetime` 또는 `immutable_datetime` 타입을 지정하여 캐스팅할 수 있습니다.

`date` 또는 `datetime` 캐스트를 정의할 때는 날짜의 포맷을 지정할 수도 있으며, 이는 [모델이 배열이나 JSON으로 직렬화될 때](/docs/10.x/eloquent-serialization) 적용됩니다:

```php
/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

날짜 캐스트로 캐스팅된 컬럼 값에는 UNIX 타임스탬프, `Y-m-d` 형식 문자열, `DateTime` 또는 `Carbon` 인스턴스를 설정할 수 있습니다. Eloquent가 올바르게 변환 후 데이터베이스에 저장합니다.

모델 내 `serializeDate` 메서드를 정의해 모든 날짜 값 직렬화 시 기본 포맷을 변경할 수도 있습니다. (데이터베이스 저장용 포맷과는 별도입니다)

```php
/**
 * 배열 / JSON 직렬화를 위한 날짜 준비.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 저장할 날짜의 포맷 지정은 `$dateFormat` 프로퍼티로 합니다:

```php
/**
 * 모델의 날짜 컬럼 저장 포맷.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 그리고 타임존

기본적으로 `date`, `datetime` 캐스트는 앱의 `timezone` 설정과 상관없이 UTC ISO-8601 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 직렬화됩니다. Laravel에서는 애플리케이션 내 모든 날짜를 UTC 시간대 기준으로 저장하고 직렬화하는 것을 권장합니다. 이렇게 하면 PHP, JavaScript 등 다양한 날짜 조작 라이브러리 간의 호환성이 극대화됩니다.

만약 `datetime:Y-m-d H:i:s`와 같은 맞춤 포맷을 사용하는 경우, 직렬화 시 `Carbon` 인스턴스 내부의 시간대가 적용됩니다. 이는 일반적으로 앱 설정 내 `timezone` 값 기반입니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 PHP [Backed Enums](https://www.php.net/manual/en/language.enumerations.backed.php)으로 속성을 캐스팅할 수 있습니다. 모델의 `$casts` 속성에 속성명과 Enum 클래스를 지정하면 됩니다:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

캐스팅 후에는 해당 속성으로 Enum 인스턴스를 주고받을 수 있습니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

단일 컬럼에 Enum 배열을 저장할 필요가 있을 때는 Laravel이 제공하는 `AsEnumArrayObject` 혹은 `AsEnumCollection` 캐스트를 사용하세요:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
];
```

<a name="encrypted-casting"></a>
### 암호화된 캐스팅

`encrypted` 캐스트는 Laravel 내장 [암호화 기능](/docs/10.x/encryption)을 이용해 모델 속성을 암호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object` 캐스트 및 `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트도 일반 캐스트와 동일하게 동작하지만, 저장 시 복호화된 값이 데이터베이스에 암호화된 상태로 저장됩니다.

암호화된 문자열의 길이는 예측할 수 없으며, 일반 텍스트보다 길기 때문에 데이터베이스 컬럼 타입은 `TEXT` 이상으로 설정해야 합니다. 또한 암호화된 속성은 데이터베이스에서 직접 쿼리하거나 검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 교체(Key Rotation)

Laravel은 앱 `app` 구성 파일 내 `key` 설정(`APP_KEY` 환경 변수)으로 문자열을 암호화합니다. 암호화 키를 교체할 때는 암호화된 모든 속성을 새 키로 수동 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

쿼리 중 원시(raw) 값을 선택할 경우 캐스트가 자동 적용되지는 않습니다. 예를 들어 다음과 같은 쿼리가 있다고 하면:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

`last_posted_at` 값은 단순 문자열로 반환될 뿐입니다. 이 속성에 `datetime` 캐스트를 쿼리 시점에 적용하려면 `withCasts` 메서드를 사용하세요:

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

Laravel은 다양한 내장 캐스트를 제공하지만, 직접 캐스트 클래스를 만들어야 할 경우도 있습니다. `make:cast` Artisan 명령어로 커스텀 캐스트 클래스를 생성할 수 있으며, 기본적으로 `app/Casts` 디렉터리에 위치합니다:

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, `get` 메서드와 `set` 메서드를 반드시 정의해야 합니다. `get`은 데이터베이스에서 원시 값 받아 변환된 캐스트 값으로 반환하며, `set`은 캐스트 값을 원시 저장 가능한 값으로 변환해 반환합니다. 예를 들어 내장 `json` 캐스트를 커스텀 캐스트로 다시 구현하면 다음과 같습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class Json implements CastsAttributes
{
    /**
     * 값을 캐스팅합니다.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(Model $model, string $key, mixed $value, array $attributes): array
    {
        return json_decode($value, true);
    }

    /**
     * 저장을 위한 값 준비.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(Model $model, string $key, mixed $value, array $attributes): string
    {
        return json_encode($value);
    }
}
```

만든 커스텀 캐스트 클래스 이름을 모델의 `$casts` 배열에 지정하면 적용됩니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들.
     *
     * @var array
     */
    protected $casts = [
        'options' => Json::class,
    ];
}
```

<a name="value-object-casting"></a>
### 값 객체 캐스팅 (Value Object Casting)

캐스팅 대상은 원시 타입뿐 아니라 객체도 가능합니다. 객체 캐스팅은 원시 타입 캐스팅과 매우 유사하지만, `set` 메서드는 모델 속성에 저장될 원시 값의 키/값 배열을 반환해야 합니다.

다음 예시는 여러 모델 속성을 단일 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스입니다. `Address` 값 객체는 공개 프로퍼티로 `lineOne`과 `lineTwo`를 가집니다:

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
     * 값을 캐스팅합니다.
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
     * 저장을 위한 값 준비.
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

값 객체에 대한 캐스팅 시, 해당 객체에 변경을 가하면 저장 전에 변경사항이 모델에 자동 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]  
> 값 객체를 포함한 Eloquent 모델을 JSON 또는 배열로 직렬화하려면, 값 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체 캐스팅 속성은 Eloquent가 캐싱하여, 동일 속성에 다시 접근할 때 같은 인스턴스를 반환합니다.

커스텀 캐스트 클래스의 객체 캐싱을 끄려면, 캐스트 클래스에 `public bool $withoutObjectCaching = true;` 프로퍼티를 선언하세요:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 배열이나 JSON으로 변환할 때(`toArray`, `toJson` 메서드), 값 객체가 `Arrayable` 및 `JsonSerializable`인터페이스를 구현하면 커스텀 캐스트가 일반적으로 직렬화를 지원합니다. 다만, 서드파티 라이브러리의 값 객체와 같이 이 인터페이스를 구현할 수 없는 경우도 있습니다.

이럴 때는 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현시켜, `serialize` 메서드를 통해 값 객체를 직접 직렬화할 수 있게 할 수 있습니다:

```php
/**
 * 값의 직렬화된 표현을 반환합니다.
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

커스텀 캐스트가 모델에 값을 설정하는 동작만 하도록 할 수도 있습니다. 이런 '인바운드 전용' 캐스트는 `CastsInboundAttributes` 인터페이스를 구현하고, `set` 메서드만 정의하면 됩니다.

`make:cast` Artisan 명령 시 `--inbound` 옵션을 사용해 인바운드 전용 캐스트 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

대표적인 예는 해싱 캐스팅입니다. 예를 들어 입력값을 특정 해시 알고리즘으로 변환하는 캐스트 클래스를 만들면 다음과 같습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class Hash implements CastsInboundAttributes
{
    /**
     * 새 캐스트 인스턴스 생성자.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * 저장할 값을 준비합니다.
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

커스텀 캐스트를 모델에 적용할 때, 클래스 이름 뒤에 `:` 문자로 구분해 여러 파라미터를 쉼표로 구분해 전달할 수 있습니다. 이 인자들은 캐스트 클래스 생성자로 전달됩니다:

```php
/**
 * 캐스팅할 속성들.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
### 캐스터블(Castables)

값 객체 클래스가 자체 커스텀 캐스트 클래스를 정의하도록 만들 수 있습니다. 이 경우 모델에 커스텀 캐스트 클래스 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 등록합니다:

```php
use App\ValueObjects\Address;

protected $casts = [
    'address' => Address::class,
];
```

`Castable` 인터페이스를 구현한 클래스는 반드시, 어떤 캐스터 클래스를 사용할지 알려주는 `castUsing` 메서드를 정의해야 합니다. 이 메서드는 커스텀 캐스트 클래스명을 문자열로 반환합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 캐스팅 대상 클래스에 사용할 캐스터 클래스명을 반환합니다.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AddressCast::class;
    }
}
```

`Castable` 클래스를 사용할 때도 `$casts` 배열에 인자를 지정할 수 있으며, 이 인자는 `castUsing` 메서드에 전달됩니다:

```php
use App\ValueObjects\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
#### 캐스터블 & 익명 캐스트 클래스

PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 캐스터블을 결합하면, 값 객체와 캐스팅 로직을 한 번에 정의하는 단일 캐스터블 객체를 만들 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현한 익명 클래스를 반환하세요:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 대상 클래스로 캐스팅하기 위한 캐스터를 반환합니다.
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