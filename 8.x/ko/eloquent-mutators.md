# Eloquent: 변경자(Mutator) & 캐스팅(Casting)

- [소개](#introduction)
- [접근자 & 변경자](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변경자 정의하기](#defining-a-mutator)
- [속성 캐스팅(Attribute Casting)](#attribute-casting)
    - [배열 & JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스팅](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열/JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자(Accessor), 변경자(Mutator), 그리고 속성 캐스팅은 Eloquent 모델 인스턴스에서 속성 값을 가져오거나 설정할 때 값을 변환할 수 있도록 도와줍니다. 예를 들어, [Laravel 암호화기](/docs/{{version}}/encryption)를 사용하여 저장 시 값을 암호화하고, Eloquent 모델에서 접근할 때 자동으로 복호화할 수 있습니다. 또는, 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환할 수 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자 & 변경자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성 값에 접근할 때 값을 변환합니다. 접근자를 정의하려면, 모델에 접근하고자 하는 컬럼명의 "studly case"로 `get{Attribute}Attribute` 메서드를 만듭니다.

다음 예시에서는 `first_name` 속성에 대한 접근자를 정의합니다. 이 접근자는 Eloquent가 `first_name` 속성 값을 가져오려고 할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름을 가져옵니다.
     *
     * @param  string  $value
     * @return string
     */
    public function getFirstNameAttribute($value)
    {
        return ucfirst($value);
    }
}
```

보시다시피, 컬럼의 원래 값이 접근자에 전달되어 조작한 다음 반환할 수 있습니다. 접근자 값을 사용하려면 모델 인스턴스에서 해당 속성에 단순히 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

접근자 안에서 단일 속성뿐만 아니라, 기존 속성값을 이용해 새로운 값을 반환하는 것도 가능합니다:

```php
/**
 * 사용자의 전체 이름을 가져옵니다.
 *
 * @return string
 */
public function getFullNameAttribute()
{
    return "{$this->first_name} {$this->last_name}";
}
```

> {tip} 이러한 계산된 값을 모델의 배열/JSON 표현에 추가하려면, [값을 appends 속성에 추가](/docs/{{version}}/eloquent-serialization#appending-values-to-json)해야 합니다.

<a name="defining-a-mutator"></a>
### 변경자 정의하기

변경자는 Eloquent 속성에 값을 설정할 때 값을 변환합니다. 변경자를 정의하려면, 모델에 접근하고자 하는 컬럼명의 "studly case"로 `set{Attribute}Attribute` 메서드를 만듭니다.

`first_name` 속성에 대한 변경자를 다음과 같이 정의할 수 있습니다. 이 변경자는 모델의 `first_name` 속성에 값을 설정할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름을 설정합니다.
     *
     * @param  string  $value
     * @return void
     */
    public function setFirstNameAttribute($value)
    {
        $this->attributes['first_name'] = strtolower($value);
    }
}
```

변경자는 설정되는 값을 받아 필요한 변환 후 Eloquent 모델의 내부 `$attributes` 속성에 저장합니다. 변경자 사용 예시는 다음과 같습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

이 예시에서 `setFirstNameAttribute` 함수는 `Sally` 값을 받아 `strtolower` 함수를 적용 후 결과값을 내부 `$attributes` 배열에 설정합니다.

<a name="attribute-casting"></a>
## 속성 캐스팅(Attribute Casting)

속성 캐스팅은 접근자/변경자와 유사한 기능을 제공하지만 별도의 메서드 정의 없이, 모델의 `$casts` 속성만 사용해 공통 데이터 타입으로 속성을 변환하도록 할 수 있습니다.

`$casts` 속성은 속성명과 변환할 타입을 키-값 쌍으로 갖는 배열이어야 합니다. 지원되는 캐스팅 타입은 다음과 같습니다:

<div class="content-list" markdown="1">

- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- `decimal:`<code>&lt;digits&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

속성 캐스팅 시연을 위해, 데이터베이스에 정수(`0` 또는 `1`)로 저장된 `is_admin` 속성을 불리언 값으로 캐스팅해보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 하는 속성.
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}
```

캐스트를 정의하면, 데이터베이스 값이 정수여도 `is_admin` 속성에 접근할 때 항상 불리언으로 변환됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

실행 중에 일시적으로 새로운 캐스트를 추가해야 한다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 정의는 기존 캐스트 정보에 더해집니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> {note} 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 관계명과 동일한 속성명/캐스트는 정의하지 않아야 합니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 이용해 모델 속성을 [fluent `Illuminate\Support\Stringable` 객체](/docs/{{version}}/helpers#fluent-strings-method-list)로 캐스팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 하는 속성.
     *
     * @var array
     */
    protected $casts = [
        'directory' => AsStringable::class,
    ];
}
```

<a name="array-and-json-casting"></a>
### 배열 & JSON 캐스팅

`array` 캐스팅은 직렬화된 JSON으로 저장된 컬럼 작업에 유용합니다. 데이터베이스에 `JSON` 또는 `TEXT` 타입으로 직렬화된 JSON이 있다면, 해당 속성에 `array` 캐스팅을 지정하면 모델에서 접근할 때 자동으로 PHP 배열로 역직렬화됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 하는 속성.
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}
```

캐스트를 정의하면, `options` 속성을 가져올 때 자동으로 PHP 배열로 역직렬화됩니다. 값을 변경하여 저장하면 다시 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

좀 더 짧은 문법으로 JSON 필드의 한 부분만 업데이트하려면, `update` 메서드에서 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### ArrayObject & Collection 캐스팅

표준 `array` 캐스팅은 대부분의 상황에서 충분하지만, 배열의 일부 오프셋을 직접 수정하는 것은 불가능합니다. 예를 들어, 아래 코드는 PHP 에러를 유발합니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 변환하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 [커스텀 캐스팅](#custom-casts) 기능을 사용하여 구현되며, 배열의 일부만 수정해도 PHP 에러가 발생하지 않습니다. 사용 방법은 다음과 같습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅해야 하는 속성.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

마찬가지로, Laravel은 JSON 속성을 [Collection](/docs/{{version}}/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅해야 하는 속성.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at` 및 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon)(PHP `DateTime` 클래스 확장) 인스턴스로 캐스팅합니다. 추가로 날짜 속성을 캐스팅하려면 `$casts` 배열에 `datetime` 또는 `immutable_datetime` 캐스팅 타입을 지정하면 됩니다.

`date` 또는 `datetime` 캐스트를 정의할 때 날짜 포맷을 지정할 수 있습니다. 이 포맷은 [모델이 배열이나 JSON으로 직렬화](/docs/{{version}}/eloquent-serialization)될 때 사용됩니다:

```php
/**
 * 캐스팅해야 하는 속성.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

날짜로 캐스팅된 컬럼은 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스 등 다양한 형태로 값을 설정할 수 있습니다.

모든 모델의 날짜 직렬화 기본 포맷을 지정하려면, 모델에 `serializeDate` 메서드를 정의할 수 있습니다. 이 메서드는 실제 데이터베이스 저장 형식에는 영향을 주지 않습니다:

```php
/**
 * 배열/JSON 직렬화를 위한 날짜 준비.
 *
 * @param  \DateTimeInterface  $date
 * @return string
 */
protected function serializeDate(DateTimeInterface $date)
{
    return $date->format('Y-m-d');
}
```

데이터베이스에 저장할 날짜 포맷을 지정하려면, 모델에 `$dateFormat` 속성을 정의하세요:

```php
/**
 * 모델의 날짜 컬럼 저장 포맷.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화 & 타임존

기본적으로 `date` 및 `datetime` 캐스트는 지정된 앱의 `timezone` 설정과 관계없이 UTC ISO-8601 날짜 문자열(`1986-05-28T21:05:54.000000Z`)로 직렬화됩니다. 이 직렬화 포맷과 UTC 타임존 저장을 권장합니다. 이를 통해 PHP, JavaScript 등과의 상호운용성을 극대화할 수 있습니다.

만약 `datetime:Y-m-d H:i:s` 처럼 커스텀 포맷을 사용하면, Carbon 인스턴스의 내부 타임존이 직렬화에 사용됩니다. 일반적으로 앱의 `timezone` 설정값을 따릅니다.

<a name="enum-casting"></a>
### Enum 캐스팅

> {note} Enum 캐스팅은 PHP 8.1 이상에서만 지원됩니다.

Eloquent는 속성 값을 PHP enum으로 캐스팅할 수도 있습니다. 모델 `$casts` 속성에 해당 속성과 enum 클래스를 지정하세요:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅해야 하는 속성.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

캐스팅을 지정하면, 속성에 접근하거나 할당할 때 enum으로 자동 캐스팅됩니다:

```php
if ($server->status == ServerStatus::provisioned) {
    $server->status = ServerStatus::ready;

    $server->save();
}
```

<a name="encrypted-casting"></a>
### 암호화 캐스팅

`encrypted` 캐스트는 모델의 속성 값을 Laravel의 [암호화 기능](/docs/{{version}}/encryption)으로 암호화합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등도 암호화된 채로 동작합니다.

암호화된 값은 평문보다 길이가 더 길고 예측이 불가능하므로, 컬럼 타입을 반드시 `TEXT` 이상으로 설정해야 합니다. 또한, 암호화된 값은 데이터베이스에서 검색·쿼리할 수 없습니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

쿼리 실행 시, 예를 들어 테이블에서 RAW 값을 가져올 때 임시 캐스트를 적용할 수 있습니다. 다음 쿼리를 보세요:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

여기서 결과의 `last_posted_at` 속성은 단순 문자열입니다. 여기에 `datetime` 캐스팅을 적용하려면 `withCasts` 메서드를 사용하세요:

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
## 커스텀 캐스팅

Laravel에는 다양한 내장 캐스트 타입이 있지만, 필요에 따라 직접 캐스트 타입을 정의할 수도 있습니다. 이를 위해 `CastsAttributes` 인터페이스를 구현하는 클래스를 정의하세요.

이 인터페이스를 구현한 클래스는 `get`과 `set` 메서드를 반드시 정의해야 합니다. `get` 메서드는 데이터베이스에서 가져온 원시 값을 캐스트된 값으로 변환하고, `set` 메서드는 캐스트된 값을 데이터베이스에 저장할 수 있도록 변환합니다. 아래는 내장된 `json` 캐스트 타입을 직접 구현한 예시입니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Json implements CastsAttributes
{
    /**
     * 주어진 값을 캐스팅합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return array
     */
    public function get($model, $key, $value, $attributes)
    {
        return json_decode($value, true);
    }

    /**
     * 값을 저장할 수 있도록 변환합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  array  $value
     * @param  array  $attributes
     * @return string
     */
    public function set($model, $key, $value, $attributes)
    {
        return json_encode($value);
    }
}
```

커스텀 캐스트 타입을 정의하면 모델 속성에 클래스명을 지정하여 적용할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅해야 하는 속성.
     *
     * @var array
     */
    protected $casts = [
        'options' => Json::class,
    ];
}
```

<a name="value-object-casting"></a>
### 값 객체 캐스팅

원시 타입뿐 아니라 객체로도 값을 캐스팅할 수 있습니다. 값 객체로의 커스텀 캐스팅을 정의하는 방법은 원시 타입과 거의 동일하지만, `set` 메서드는 키/값 배열을 반환하여 모델의 원시 속성값으로 설정되도록 해야 합니다.

예를 들어, 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트를 만들어보겠습니다. `Address` 값 객체에는 `lineOne`, `lineTwo` 두 개의 public 속성이 있다고 가정합니다.

```php
<?php

namespace App\Casts;

use App\Models\Address as AddressModel;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use InvalidArgumentException;

class Address implements CastsAttributes
{
    /**
     * 주어진 값을 캐스팅합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return \App\Models\Address
     */
    public function get($model, $key, $value, $attributes)
    {
        return new AddressModel(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * 값을 저장할 수 있도록 변환합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  \App\Models\Address  $value
     * @param  array  $attributes
     * @return array
     */
    public function set($model, $key, $value, $attributes)
    {
        if (! $value instanceof AddressModel) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅 시 해당 객체의 값이 변경되면, 모델 저장 전에 자동으로 모델과 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> {tip} 값 객체를 가진 Eloquent 모델을 JSON이나 배열로 직렬화할 계획이 있다면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 `toArray`나 `toJson` 메서드로 변환할 때, 커스텀 캐스트 값 객체도 보통 같이 직렬화됩니다(`Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스 구현 필요). 그러나 외부 라이브러리의 값 객체는 이 인터페이스를 구현하지 못할 수 있습니다.

이럴 때, 커스텀 캐스트 클래스가 값 객체 직렬화를 담당하도록 지정할 수 있습니다. 이를 위해 커스텀 캐스트 클래스에 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고 `serialize` 메서드를 정의합니다:

```php
/**
 * 값의 직렬화 표현 반환.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $value
 * @param  array  $attributes
 * @return mixed
 */
public function serialize($model, string $key, $value, array $attributes)
{
    return (string) $value;
}
```

<a name="inbound-casting"></a>
### 인바운드(입력 전용) 캐스팅

때때로, 속성 값을 가져올 때는 변환하지 않고 설정할 때만 변환하고 싶을 수 있습니다. 대표적인 예로 "해시" 캐스팅이 있습니다. 입력 전용 캐스트는 `CastsInboundAttributes` 인터페이스를 구현하며, `set` 메서드만 필요합니다.

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;

class Hash implements CastsInboundAttributes
{
    /**
     * 해싱 알고리즘.
     *
     * @var string
     */
    protected $algorithm;

    /**
     * 새 캐스트 클래스 인스턴스 생성자.
     *
     * @param  string|null  $algorithm
     * @return void
     */
    public function __construct($algorithm = null)
    {
        $this->algorithm = $algorithm;
    }

    /**
     * 값을 저장할 수 있도록 변환합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  array  $value
     * @param  array  $attributes
     * @return string
     */
    public function set($model, $key, $value, $attributes)
    {
        return is_null($this->algorithm)
                    ? bcrypt($value)
                    : hash($this->algorithm, $value);
    }
}
```

<a name="cast-parameters"></a>
### 캐스트 파라미터

커스텀 캐스트를 모델에 적용할 때, 클래스명 뒤에 `:`를 붙여 파라미터를 전달할 수 있습니다. 여러 파라미터는 쉼표로 구분합니다. 파라미터는 캐스트 클래스 생성자에 전달됩니다.

```php
/**
 * 캐스팅해야 하는 속성.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션의 값 객체가 자체적으로 커스텀 캐스트 클래스를 정의하도록 할 수도 있습니다. 이때 모델에 커스텀 캐스트 클래스를 직접 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 지정합니다:

```php
use App\Models\Address;

protected $casts = [
    'address' => Address::class,
];
```

`Castable` 인터페이스를 구현한 객체는 `castUsing` 메서드를 정의해야 하며, 이 메서드는 캐스팅에 사용할 커스텀 캐스트 클래스명을 반환합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 캐스팅/복원을 담당하는 캐스터 클래스명 반환.
     *
     * @param  array  $arguments
     * @return string
     */
    public static function castUsing(array $arguments)
    {
        return AddressCast::class;
    }
}
```

캐스터블 클래스 사용 시에도 `$casts`에서 파라미터 인자를 전달할 수 있으며, 해당 인자는 `castUsing` 메서드로 전달됩니다:

```php
use App\Models\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
#### 캐스터블 & 익명 캐스트 클래스

"캐스터블"을 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 함께 사용하여 값 객체와 캐스팅 로직을 단일 객체로 정의할 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하면 됩니다. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 캐스팅/복원을 위한 캐스터 클래스 반환.
     *
     * @param  array  $arguments
     * @return object|string
     */
    public static function castUsing(array $arguments)
    {
        return new class implements CastsAttributes
        {
            public function get($model, $key, $value, $attributes)
            {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set($model, $key, $value, $attributes)
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
