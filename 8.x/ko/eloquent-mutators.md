# Eloquent: Mutators 및 Casting

- [소개](#introduction)
- [액세서(Accessors) 및 뮤테이터(Mutators)](#accessors-and-mutators)
    - [액세서 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅(Attribute Casting)](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [열거형(Enum) 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트(Custom Casts)](#custom-casts)
    - [값 객체(Value Object) 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [입력 전용(Inbound) 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [Castables](#castables)

<a name="introduction"></a>
## 소개

액세서, 뮤테이터, 속성 캐스팅은 Eloquent 모델 인스턴스에서 속성 값을 조회하거나 설정할 때 변환할 수 있게 해줍니다. 예를 들어, 데이터베이스에 저장할 때 [Laravel 암호화기](/docs/{{version}}/encryption)를 사용해 값을 암호화하고, Eloquent 모델을 통해 접근할 때 자동으로 속성 값을 복호화할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델을 통해 접근할 때 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 액세서(Accessors) 및 뮤테이터(Mutators)

<a name="defining-an-accessor"></a>
### 액세서 정의하기

액세서는 Eloquent 속성 값에 접근할 때 해당 값을 변환하는 메서드입니다. 액세서를 정의하려면, 모델에 `get{Attribute}Attribute` 메서드를 만듭니다. 여기서 `{Attribute}`는 액세스하려는 컬럼 명칭을 스터들 케이스(studly case)로 변환한 이름입니다.

아래 예시는 `first_name` 속성에 대한 액세서를 정의한 것입니다. 이 액세서는 Eloquent가 `first_name` 속성 값을 가져올 때 자동으로 호출됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first name)을 가져옵니다.
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

컬럼의 원본 값이 액세서로 전달되어 변환한 후 리턴할 수 있습니다. 액세서의 값을 얻으려면 단순히 모델 인스턴스에서 `first_name` 속성을 조회하면 됩니다:

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

액세서 내부에서 단일 속성뿐만 아니라, 기존 속성들로부터 새로운 계산 값을 반환하는 것도 가능합니다:

```
/**
 * 사용자의 전체 이름(full name)을 반환합니다.
 *
 * @return string
 */
public function getFullNameAttribute()
{
    return "{$this->first_name} {$this->last_name}";
}
```

> [!TIP]
> 계산된 값을 모델의 배열/JSON 표현에 포함하고 싶다면, [해당 속성을 append 해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="defining-a-mutator"></a>
### 뮤테이터 정의하기

뮤테이터는 Eloquent 속성 값에 설정할 때 값을 변환합니다. 뮤테이터를 정의하려면, 모델에 `set{Attribute}Attribute` 메서드를 만듭니다. 여기서 `{Attribute}`는 설정하려는 컬럼 명칭을 스터들 케이스로 변환한 이름입니다.

다음 예시는 `first_name` 속성에 대한 뮤테이터를 정의한 것입니다. `first_name` 속성을 설정할 때 자동으로 이 뮤테이터가 호출됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(first name)을 설정합니다.
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

뮤테이터는 설정되는 값을 전달받아, 변환 후 Eloquent 모델 내부의 `$attributes` 배열에 직접 설정할 수 있습니다. 뮤테이터를 사용하려면 단순히 모델의 `first_name` 속성을 설정하면 됩니다:

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예시에서 `setFirstNameAttribute` 메서드는 `Sally` 값을 받아 `strtolower` 함수를 적용한 후 내부 `$attributes` 배열에 값을 설정합니다.

<a name="attribute-casting"></a>
## 속성 캐스팅 (Attribute Casting)

속성 캐스팅은 모델에 추가적인 메서드를 정의하지 않고, 속성 값을 공통 데이터 타입으로 변환하는 편리한 방법을 제공합니다. 모델의 `$casts` 속성은 캐스트하려는 속성 이름을 키로, 캐스팅할 타입을 값으로 가지는 배열입니다.

지원되는 캐스트 타입 목록은 다음과 같습니다:

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

예를 들어, 데이터베이스에 `0` 또는 `1` 정수로 저장된 `is_admin` 속성을 불리언으로 캐스팅하려면 다음과 같이 할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록입니다.
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}
```

캐스팅을 정의한 후에는 `is_admin` 속성을 조회할 때 항상 불리언 값으로 반환됩니다. 데이터베이스에 정수형으로 저장되어 있어도 상관없습니다:

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

실행 중에 임시로 새 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 메서드는 기존에 정의된 캐스트에 추가로 병합해줍니다:

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!NOTE]
> `null` 값은 캐스팅되지 않습니다. 또한, 관계 이름과 동일한 속성을 캐스팅하거나 정의하면 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 클래스 캐스트를 사용해 모델 속성을 [플루언트 문자열 객체인 `Illuminate\Support\Stringable`](/docs/{{version}}/helpers#fluent-strings-method-list)로 캐스트할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록입니다.
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

`array` 캐스트는 데이터베이스에 직렬화된 JSON으로 저장된 컬럼을 다룰 때 특히 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 필드에 직렬화된 JSON이 저장된 경우, `array` 캐스트를 지정하면 Eloquent 모델을 통해 접근 시 자동으로 JSON이 PHP 배열로 역직렬화됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록입니다.
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}
```

캐스트가 정의된 후에는 `options` 속성이 JSON에서 자동으로 배열로 변환되어 반환됩니다. 또한, `options` 속성에 배열을 설정하면 자동으로 JSON으로 직렬화되어 저장됩니다:

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성 중 단일 필드만 간단히 업데이트하려면, `update` 메서드 호출 시 `->` 연산자를 사용할 수 있습니다:

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### ArrayObject & Collection 캐스팅

기본 `array` 캐스트는 대부분의 용도에 충분하지만 한 가지 단점이 있습니다. `array` 캐스트는 원시 타입을 반환하기 때문에, 배열 내부의 특정 요소를 직접 수정하면 PHP 오류가 발생합니다. 아래 코드는 오류를 발생시킵니다:

```
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 `AsArrayObject` 캐스트를 제공합니다. 이 캐스트는 JSON 속성을 PHP의 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅합니다. Laravel의 [커스텀 캐스트](#custom-casts) 기능으로 구현되어, 수정된 객체 변경사항을 캐싱해 배열 요소별 직접 변경을 허용합니다. 사용하려면 다음과 같이 속성에 할당하세요:

```
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성 목록입니다.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

비슷하게, `AsCollection` 캐스트를 이용하면 JSON 속성을 Laravel [Collection](/docs/{{version}}/collections) 인스턴스로 변환할 수 있습니다:

```
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성 목록입니다.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 PHP `DateTime` 클래스를 확장한 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 다양한 유용한 날짜/시간 메서드를 제공합니다. 필요에 따라, 모델의 `$casts` 배열에 추가 날짜 속성도 `datetime` 또는 `immutable_datetime` 타입으로 캐스팅할 수 있습니다.

`date` 또는 `datetime` 캐스트를 지정할 때는 형식도 함께 지정할 수 있으며, 이 형식은 [모델이 배열 또는 JSON으로 직렬화될 때](/docs/{{version}}/eloquent-serialization) 사용됩니다:

```
/**
 * 캐스팅할 속성 목록입니다.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

날짜 캐스팅이 적용된 속성에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, `DateTime` 또는 `Carbon` 인스턴스 등 다양한 값을 설정할 수 있으며, 데이터베이스에 올바르게 저장됩니다.

모델에서 모든 날짜를 직렬화할 때 기본 형식을 바꾸고 싶으면, 모델에 `serializeDate` 메서드를 정의하세요. 이 메서드는 데이터베이스 저장 형식에는 영향을 주지 않습니다:

```
/**
 * 배열 / JSON 직렬화를 위한 날짜 형식 준비.
 *
 * @param  \DateTimeInterface  $date
 * @return string
 */
protected function serializeDate(DateTimeInterface $date)
{
    return $date->format('Y-m-d');
}
```

반면, 데이터베이스에 저장할 때 사용할 날짜 형식을 지정하려면 `$dateFormat` 속성을 정의하세요:

```
/**
 * 모델의 날짜 컬럼 저장 형식.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화, 및 시간대

기본적으로 `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정과 관계없이 UTC ISO-8601 형식(`1986-05-28T21:05:54.000000Z`)의 문자열로 직렬화됩니다. Laravel은 애플리케이션의 시간대를 변경하지 않고(기본 `UTC` 유지) UTC 시간대를 일관적으로 사용하는 것을 권장합니다. 이렇게 하면 PHP 및 JavaScript 등 다양한 날짜 처리 라이브러리와 최대한 호환됩니다.

만약 `datetime:Y-m-d H:i:s` 같은 사용자 지정 형식을 적용하면, 직렬화 시 Carbon 인스턴스의 내부 시간대(보통 애플리케이션의 `timezone` 설정 값)가 사용됩니다.

<a name="enum-casting"></a>
### 열거형(Enum) 캐스팅

> [!NOTE]
> Enum 캐스팅은 PHP 8.1 이상에서만 사용할 수 있습니다.

Eloquent는 속성을 PHP의 Enum 타입으로 캐스팅할 수도 있습니다. 모델의 `$casts`에 속성과 캐스팅할 Enum 클래스를 지정하면 됩니다:

```
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성 목록입니다.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

캐스트가 정의된 후, 해당 속성을 조회하거나 설정할 때 자동으로 Enum 인스턴스로 변환됩니다:

```
if ($server->status == ServerStatus::provisioned) {
    $server->status = ServerStatus::ready;

    $server->save();
}
```

<a name="encrypted-casting"></a>
### 암호화 캐스팅 (Encrypted Casting)

`encrypted` 캐스트는 Laravel 내장 [암호화](/docs/{{version}}/encryption) 기능을 사용해 모델 속성을 암호화합니다. 또한, `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트는 암호화되지 않은 동등한 캐스트처럼 동작하지만, 데이터베이스에 저장할 때 암호화됩니다.

암호화된 문자열은 평문보다 길이가 길고 불규칙하므로, 데이터베이스 컬럼 타입을 `TEXT` 이상으로 설정하는 것이 좋습니다. 또한 암호화 속성의 값으로 쿼리하거나 검색하는 것은 불가능합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅

쿼리 실행 중에 원시(raw) 값을 선택하는 경우에도 캐스트를 적용해야 할 때가 있습니다. 예를 들어:

```
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

이 쿼리의 결과에서 `last_posted_at`은 단순 문자열로 반환됩니다. 이를 `datetime` 캐스트로 변환하고 싶다면 `withCasts` 메서드를 사용하세요:

```
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

Laravel은 여러 내장 캐스트 타입을 제공하지만, 때로는 직접 캐스트 타입을 정의해야 할 경우도 있습니다. 이럴 땐 `CastsAttributes` 인터페이스를 구현한 클래스를 만들어 사용합니다.

`CastsAttributes` 인터페이스를 구현한 클래스는 `get`과 `set` 메서드를 반드시 정의해야 합니다. `get` 메서드는 데이터베이스에서 조회한 원시 값(raw value)을 캐스팅된 값으로 변환하고, `set` 메서드는 캐스팅된 값을 데이터베이스에 저장할 원시 값으로 변환합니다. 예시로, 내장 `json` 캐스트를 커스텀 캐스트로 재구현해보겠습니다:

```
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Json implements CastsAttributes
{
    /**
     * 주어진 값을 캐스트합니다.
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
     * 주어진 값을 저장할 용도로 변환합니다.
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

커스텀 캐스트 클래스를 정의한 후에는, 속성에 해당 클래스 이름을 `$casts`에 지정하여 적용할 수 있습니다:

```
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성 목록입니다.
     *
     * @var array
     */
    protected $casts = [
        'options' => Json::class,
    ];
}
```

<a name="value-object-casting"></a>
### 값 객체(Value Object) 캐스팅

값을 원시 타입뿐만 아니라 객체로도 캐스팅할 수 있습니다. 객체 캐스팅은 기본 캐스트와 거의 유사하지만, `set` 메서드는 모델에서 저장할 수 있는 원시 키/값 배열을 반환해야 합니다.

예를 들어, 여러 모델 속성을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트를 구현해보겠습니다. 여기서 `Address` 객체는 `lineOne`과 `lineTwo` 두 개의 공개 프로퍼티를 가진다고 가정합니다:

```
<?php

namespace App\Casts;

use App\Models\Address as AddressModel;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use InvalidArgumentException;

class Address implements CastsAttributes
{
    /**
     * 주어진 값을 캐스트합니다.
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
     * 저장할 용도로 값을 준비합니다.
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
            throw new InvalidArgumentException('주어진 값이 Address 인스턴스가 아닙니다.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅된 인스턴스에서 변경된 내용은 모델이 저장되기 전에 자동으로 동기화됩니다:

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!TIP]
> 값 객체가 포함된 Eloquent 모델을 JSON 또는 배열로 직렬화하려면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델이 `toArray` 또는 `toJson` 메서드로 변환될 때, 커스텀 캐스트 값 객체는 일반적으로 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현하면 자동으로 직렬화됩니다. 하지만 서드파티 라이브러리의 값 객체는 이 인터페이스를 구현하지 못할 수도 있습니다.

따라서, 커스텀 캐스트 클래스가 값 객체의 직렬화를 책임지도록 할 수 있습니다. 이를 위해 커스텀 캐스트 클래스는 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메서드를 정의해야 합니다. 이 메서드는 값 객체의 직렬화된 표현을 반환합니다:

```
/**
 * 값의 직렬화된 표현을 반환합니다.
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
### 입력 전용(Inbound) 캐스팅

가끔 값이 모델에 설정될 때만 변환하고, 조회 시에는 변환하지 않는 커스텀 캐스트가 필요할 수 있습니다. 예를 들어 "해싱(hashing)" 캐스트가 대표적입니다. 입력 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현하며, `set` 메서드만 정의하면 됩니다.

```
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
     * 새로운 캐스트 클래스 인스턴스 생성.
     *
     * @param  string|null  $algorithm
     * @return void
     */
    public function __construct($algorithm = null)
    {
        $this->algorithm = $algorithm;
    }

    /**
     * 저장할 용도로 값을 준비합니다.
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

커스텀 캐스트를 모델에 적용할 때, 클래스 이름 뒤에 `:` 문자를 붙이고 쉼표로 구분된 파라미터를 전달할 수 있습니다. 이 파라미터들은 캐스트 클래스의 생성자에 전달됩니다:

```
/**
 * 캐스팅할 속성 목록입니다.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
### Castables

애플리케이션의 값 객체가 자체 커스텀 캐스트 클래스를 정의하도록 허용하고 싶을 수 있습니다. 이 경우 모델에 커스텀 캐스트 클래스를 직접 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 `$casts`에 지정할 수 있습니다:

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class,
];
```

`Castable` 인터페이스를 구현한 객체는 `castUsing` 메서드를 반드시 정의해야 하며, 이 메서드는 해당 타입 캐스팅을 담당할 캐스트 클래스 이름을 반환합니다:

```
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 캐스팅 시 사용할 캐스트 클래스 이름을 반환합니다.
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

`Castable` 클래스를 사용할 때는 `$casts` 정의 내에 인자도 여전히 전달 가능하며, 이 인자는 `castUsing` 메서드로 전달됩니다:

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
#### Castables 및 익명 캐스트 클래스

`Castable`을 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 결합하면, 값 객체 및 캐스팅 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현한 익명 클래스를 반환하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 캐스팅 시 사용할 캐스트 클래스를 반환합니다.
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