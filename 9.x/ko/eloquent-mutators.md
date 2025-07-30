# Eloquent: 뮤테이터 및 캐스팅 (Eloquent: Mutators & Casting)

- [소개](#introduction)
- [액세서 및 뮤테이터](#accessors-and-mutators)
    - [액세서 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [열거형 캐스팅](#enum-casting)
    - [암호화된 캐스팅](#encrypted-casting)
    - [쿼리 시점 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [인바운드 캐스팅](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개 (Introduction)

액세서, 뮤테이터, 그리고 속성 캐스팅은 Eloquent 모델 인스턴스의 속성 값을 가져오거나 설정할 때 변환 기능을 제공합니다. 예를 들어, 데이터베이스에 저장되는 값을 Laravel 암호화 도구([Laravel encrypter](/docs/9.x/encryption))로 암호화했다가, Eloquent 모델에서 해당 속성을 접근할 때 자동으로 복호화할 수 있습니다. 또는 데이터베이스에 JSON 문자열로 저장된 값을 Eloquent 모델에서 접근할 때 배열로 변환해서 사용할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 액세서 & 뮤테이터 (Accessors & Mutators)

<a name="defining-an-accessor"></a>
### 액세서 정의하기 (Defining An Accessor)

액세서는 Eloquent 속성 값에 접근할 때 값을 변환하는 역할을 합니다. 액세서를 정의하려면, 모델에 보호된 메서드를 생성하며, 메서드 이름은 관련된 실제 모델 속성(데이터베이스 컬럼)의 "camel case" 형식과 일치해야 합니다.

예를 들어, `first_name` 속성에 대한 액세서를 정의해 보겠습니다. 이 액세서는 Eloquent가 `first_name` 속성 값을 가져오려 할 때 자동으로 호출됩니다. 모든 액세서 및 뮤테이터 메서드는 반환 타입 힌트로 `Illuminate\Database\Eloquent\Casts\Attribute`를 반드시 선언해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(First Name)을 가져옵니다.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => ucfirst($value),
        );
    }
}
```

모든 액세서 메서드는 `Attribute` 인스턴스를 반환하며, 이 인스턴스는 해당 속성의 접근(access) 및 선택적으로 변환(mutation) 방식을 정의합니다. 위 예제에서는 `get` 인자를 사용해 속성을 어떻게 접근할지 정의했습니다.

액세서로 전달되는 값은 컬럼의 원본 값이며, 이를 가공하거나 조작한 후 반환할 수 있습니다. 액세서의 값을 사용하려면 단순히 모델 인스턴스에서 `first_name` 속성을 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> 만약 액세서로 계산한 값을 모델의 배열 또는 JSON 표현에 포함하고 싶으면, [배열/JSON 표현에 추가하기](/docs/9.x/eloquent-serialization#appending-values-to-json) 설정을 해주어야 합니다.

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

종종 액세서가 여러 속성을 조합해 하나의 "값 객체(value object)"를 생성해야 할 때가 있습니다. 이때 `get` 클로저에 두 번째 인자로 `$attributes`를 받을 수 있으며, 이는 현재 모델의 모든 속성을 담은 배열입니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소를 관리합니다.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```

<a name="accessor-caching"></a>
#### 액세서 캐싱 (Accessor Caching)

값 객체를 반환하는 액세서의 경우, 해당 객체에 대한 변경사항은 모델이 저장(save)되기 전에 자동으로 동기화됩니다. 이는 Eloquent가 액세서에서 반환된 인스턴스를 계속 유지하면서 동일한 인스턴스를 반복 사용하기 때문입니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

하지만 문자열이나 불리언 같은 원시형 값에 대해 계산 비용이 많이 들 경우, 캐싱을 활성화하고 싶을 수 있습니다. 이때 액세서 정의 시 `shouldCache()` 메서드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn ($value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

만약 속성의 객체 캐싱 기능을 비활성화하고 싶다면, 액세서 정의 시 `withoutObjectCaching()` 메서드를 호출하세요:

```php
/**
 * 사용자의 주소를 관리합니다.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
### 뮤테이터 정의하기 (Defining A Mutator)

뮤테이터는 Eloquent 속성 값이 설정(set)될 때 값을 변환합니다. 뮤테이터를 정의하려면 `set` 인자를 제공하면 됩니다. 예를 들어 `first_name` 속성에 뮤테이터를 정의하면, 해당 속성을 모델에 세팅할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 이름(First Name)을 관리합니다.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn ($value) => ucfirst($value),
            set: fn ($value) => strtolower($value),
        );
    }
}
```

뮤테이터 클로저는 설정되는 값을 받아서 조작한 후, 조작된 값을 반환해야 합니다. 뮤테이터를 사용하는 방법은 매우 간단히, 모델의 `first_name` 속성을 설정하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

위 예시에서 `set` 콜백은 `'Sally'` 값을 받아 `strtolower` 함수를 적용한 소문자 값으로 내부 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 뮤테이터

때때로 뮤테이터는 모델의 여러 속성을 동시에 변경해야 할 때가 있습니다. 이럴 때는 `set` 클로저에서 배열을 반환할 수 있으며, 배열의 각 키는 모델의 컬럼 이름과 맞아야 합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소를 관리합니다.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
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

속성 캐스팅은 액세서/뮤테이터를 별도로 정의하지 않고도 모델의 `$casts` 속성에 타입 변환 정보를 배열 형태로 지정해서 사용할 수 있도록 하는 편리한 기능입니다.

`$casts` 배열의 키는 캐스팅 대상 속성명, 값은 캐스팅할 타입을 지정합니다. 지원하는 타입은 다음과 같습니다:

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
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

예를 들어, 데이터베이스에 정수 `0` 또는 `1`로 저장되어 있는 `is_admin` 컬럼을 Boolean으로 캐스팅하려면, 다음과 같이 `$casts`에 등록합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들입니다.
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}
```

캐스팅을 지정한 후에는, 데이터베이스 값이 정수형이어도 속성 값을 접근하면 항상 Boolean 값으로 변환해서 반환합니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

실행 중에 임시로 캐스팅을 추가하고 싶을 때는 `mergeCasts` 메서드를 사용하세요. 이때 추가된 캐스트 설정은 기존 모델 캐스트에 병합됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한, 관계 이름과 동일한 이름으로 캐스트나 속성을 정의해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 이용하면 모델의 속성을 [fluent `Illuminate\Support\Stringable` 객체](/docs/9.x/helpers#fluent-strings-method-list)로 캐스팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들입니다.
     *
     * @var array
     */
    protected $casts = [
        'directory' => AsStringable::class,
    ];
}
```

<a name="array-and-json-casting"></a>
### 배열 및 JSON 캐스팅 (Array & JSON Casting)

`array` 캐스트는 JSON 직렬화된 컬럼에서 특히 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 타입 필드에 저장된 직렬화된 JSON 문자열을 `array` 캐스트로 지정하면, Eloquent에서 속성에 접근할 때 자동으로 PHP 배열로 역직렬화됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들입니다.
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}
```

캐스트 정의 후, `options` 속성을 배열 형태로 바로 사용할 수 있습니다. 속성 값을 설정할 때도 배열을 제공하면 자동으로 JSON으로 직렬화되어 저장됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

JSON 속성의 단일 필드만 업데이트하려면, `update` 메서드에서 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
#### 배열 객체 및 컬렉션 캐스팅

기본 `array` 캐스트는 편리하지만, 반환 타입이 원시 배열이므로 배열의 오프셋을 직접 수정할 수 없는 단점이 있습니다. 다음 코드는 PHP 오류를 발생시킵니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```

이 문제를 해결하기 위해 Laravel은 `AsArrayObject` 캐스트를 제공합니다. 이 캐스트는 JSON 속성을 PHP의 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅하며, Laravel의 [커스텀 캐스트](#custom-casts)를 활용해 변경된 오프셋을 스마트하게 감지하고 캐시합니다. 사용법은 다음과 같습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

마찬가지로 Laravel은 JSON 속성을 Laravel의 [Collection](/docs/9.x/collections) 인스턴스로 캐스팅하는 `AsCollection` 캐스트도 제공합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

<a name="date-casting"></a>
### 날짜 캐스팅 (Date Casting)

기본적으로 Eloquent는 `created_at`과 `updated_at` 컬럼을 PHP `DateTime` 클래스 확장판인 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. 추가적으로 모델의 날짜 속성도 `$casts` 배열에 캐스팅 타입을 지정해 관리할 수 있습니다. 일반적으로 `date` 또는 `datetime`, `immutable_date`, `immutable_datetime` 타입을 사용합니다.

`date` 또는 `datetime` 캐스팅 시, 날짜 포맷을 지정할 수도 있습니다. 이 포맷은 모델을 배열 또는 JSON으로 직렬화할 때 적용됩니다:

```php
/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

날짜로 캐스팅된 컬럼에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 혹은 `DateTime` / `Carbon` 인스턴스를 할당할 수 있으며, Eloquent가 이를 데이터베이스에 맞게 올바르게 변환해 저장합니다.

모델 전반에 대한 날짜 직렬화 포맷을 변경하려면, 모델에 `serializeDate` 메서드를 정의하세요. 이 메서드는 데이터베이스 저장 포맷에 영향을 주지 않고, 배열 또는 JSON 직렬화 시의 포맷만 조절합니다:

```php
/**
 * 배열 / JSON 직렬화를 위한 날짜 준비.
 *
 * @param  \DateTimeInterface  $date
 * @return string
 */
protected function serializeDate(DateTimeInterface $date)
{
    return $date->format('Y-m-d');
}
```

또한, 모델의 날짜 컬럼 저장 포맷을 바꾸려면 `$dateFormat` 속성을 정의하십시오:

```php
/**
 * 모델 날짜 컬럼의 저장 포맷입니다.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅, 직렬화 및 시간대

기본적으로 `date` 및 `datetime` 캐스트는 애플리케이션의 `timezone` 설정과 상관없이 날짜를 UTC ISO-8601 문자열 (`1986-05-28T21:05:54.000000Z`)로 직렬화합니다. 가능한 한 UTC 시간대를 일관되게 사용하는 것이 PHP 및 JavaScript 등 다른 라이브러리와 호환성을 높이는 데 권장됩니다.

만약 `datetime:Y-m-d H:i:s` 같은 맞춤 형식을 사용하면, Carbon 인스턴스의 내부 시간대(보통 앱의 `timezone` 설정에 따름)를 기준으로 직렬화됩니다.

<a name="enum-casting"></a>
### 열거형 캐스팅 (Enum Casting)

> [!WARNING]
> 열거형 캐스팅은 PHP 8.1 이상에서만 사용 가능합니다.

Eloquent는 속성 값을 PHP [열거형(Enums)](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로 캐스팅할 수 있습니다. `$casts` 배열에 속성과 대응하는 Enum 클래스를 지정하면 됩니다:

```php
use App\Enums\ServerStatus;

/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

이렇게 설정 후에는 속성을 Enum 객체로 읽고, Enum 값을 할당할 수 있습니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
#### 배열 형태의 Enum 캐스팅

때로는 단일 컬럼에 여러 개의 Enum 값을 배열로 저장해야 할 수도 있습니다. 이럴 때 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 활용할 수 있습니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
];
```

<a name="encrypted-casting"></a>
### 암호화된 캐스팅 (Encrypted Casting)

`encrypted` 캐스트는 Laravel 내장 [암호화](/docs/9.x/encryption) 기능을 사용해 모델 속성 값을 암호화합니다. `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 캐스트도 각각 암호화된 상태로 동작합니다. 

암호화된 값은 평문보다 길이가 불규칙하고 더 길기 때문에 관련 데이터베이스 컬럼은 `TEXT` 타입 이상이어야 합니다. 암호화된 값은 데이터베이스에서 직접 검색하거나 쿼리하는 것이 불가능하니 참고하세요.

<a name="key-rotation"></a>
#### 키 교체 (Key Rotation)

Laravel 암호화는 애플리케이션 `app` 설정의 `key` 값을 사용하며, 일반적으로 `.env` 파일의 `APP_KEY` 환경 변수 값과 일치합니다. 암호화 키를 교체할 때는 기존 암호화된 속성들을 새 키로 수동 재암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 시점 캐스팅 (Query Time Casting)

쿼리 실행 시 원시 값을 선택할 때도 캐스팅을 적용할 수 있습니다. 예를 들어, 다음과 같은 쿼리 결과의 `last_posted_at` 컬럼은 단순 문자열로 반환됩니다:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

이 컬럼에 `datetime` 캐스팅을 적용하려면 `withCasts` 메서드를 이용하세요:

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

Laravel에 내장된 캐스트 타입도 많지만, 필요에 따라 직접 캐스트 클래스를 정의할 수도 있습니다. 커스텀 캐스트 클래스를 생성하려면 Artisan의 `make:cast` 명령어를 사용하여 `app/Casts` 디렉토리에 클래스를 만드세요:

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `get`과 `set` 메서드를 반드시 정의해야 합니다. `get` 메서드는 데이터베이스에서 가져온 원시 값을 캐스트된 값으로 변환하고, `set` 메서드는 캐스트된 값을 데이터베이스에 저장할 원시 값으로 변환합니다.

다음은 내장된 `json` 캐스트를 커스텀 캐스트로 재구현한 예시입니다:

```php
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
     * 저장을 위한 값을 준비합니다.
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

정의한 커스텀 캐스트 타입은 클래스 이름을 사용해 모델의 `$casts`에 할당할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\Json;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 캐스팅할 속성들입니다.
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

값을 반드시 원시형으로만 캐스팅할 필요는 없으며, 객체로도 캐스팅할 수 있습니다. 객체로 캐스팅 시 `set` 메서드는 모델에 저장할 순수 원시 값을 키-값 배열 형태로 반환해야 한다는 점만 다릅니다.

예시로, 여러 모델 값을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 만들어 봅니다. `Address` 값 객체는 `lineOne`과 `lineTwo` 두 개의 공개 프로퍼티가 있다고 가정합니다:

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address as AddressValueObject;
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
     * @return \App\ValueObjects\Address
     */
    public function get($model, $key, $value, $attributes)
    {
        return new AddressValueObject(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * 저장을 위한 값을 준비합니다.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  \App\ValueObjects\Address  $value
     * @param  array  $attributes
     * @return array
     */
    public function set($model, $key, $value, $attributes)
    {
        if (! $value instanceof AddressValueObject) {
            throw new InvalidArgumentException('주어진 값이 Address 인스턴스가 아닙니다.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```

값 객체로 캐스팅하면, 값을 변경하면 저장 직전에 모델에 자동으로 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 값 객체를 포함한 Eloquent 모델을 JSON 또는 배열로 직렬화할 계획이라면, 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화 (Array / JSON Serialization)

Eloquent 모델이 `toArray` 또는 `toJson` 메서드로 변환될 때, 커스텀 캐스트 값 객체는 보통 `Arrayable`과 `JsonSerializable` 인터페이스를 구현하면 자동으로 직렬화됩니다. 그러나 서드파티 라이브러리가 제공하는 값 객체는 인터페이스를 구현하지 않은 경우가 많습니다.

이때, 커스텀 캐스트 클래스가 직렬화 책임을 직접 맡도록 하려면 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 하며, `serialize` 메서드를 정의해 값 객체를 직렬화된 형태로 반환해야 합니다:

```php
/**
 * 값의 직렬화 표현을 반환합니다.
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
### 인바운드 캐스팅 (Inbound Casting)

때때로 모델의 속성 값을 가져올 때는 변환할 필요가 없고, 설정할 때만 변환을 적용하는 커스텀 캐스트가 필요할 수 있습니다.

이런 인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, `set` 메서드만 정의하면 됩니다. `make:cast` Artisan 명령을 `--inbound` 옵션과 함께 실행하면 인바운드 전용 캐스트 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

인바운드 캐스트의 대표적인 예는 해싱 캐스트입니다. 예를 들어, 주어진 알고리즘으로 값을 해싱하는 캐스트를 작성할 수 있습니다:

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
     * 새 캐스트 인스턴스를 생성합니다.
     *
     * @param  string|null  $algorithm
     * @return void
     */
    public function __construct($algorithm = null)
    {
        $this->algorithm = $algorithm;
    }

    /**
     * 저장할 값을 준비합니다.
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
### 캐스트 파라미터 (Cast Parameters)

커스텀 캐스트를 모델에 붙일 때 클래스명 뒤에 `:` 문자로 구분해 여러 파라미터를 쉼표로 구분하여 지정할 수 있습니다. 이 파라미터들은 캐스트 클래스의 생성자에 전달됩니다:

```php
/**
 * 캐스팅할 속성들입니다.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션의 값 객체가 스스로 맞춤 캐스팅 방식을 정의하도록 할 수도 있습니다. 이때는 모델에 커스텀 캐스트 클래스를 붙이는 대신 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 붙입니다:

```php
use App\Models\Address;

protected $casts = [
    'address' => Address::class,
];
```

`Castable` 인터페이스를 구현한 클래스는 `castUsing` 메서드를 정의해야 하며, 이 메서드는 해당 클래스와 매핑할 커스텀 캐스트 클래스명을 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\Address as AddressCast;

class Address implements Castable
{
    /**
     * 캐스팅에 사용할 캐스터 클래스명을 반환합니다.
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

`Castable` 클래스를 사용할 때도, `$casts` 배열에 인자를 붙여 넘길 수 있으며, 이 인자들은 `castUsing` 메서드에 전달됩니다:

```php
use App\Models\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
#### 캐스터블과 익명 캐스트 클래스 (Castables & Anonymous Cast Classes)

`Castable`과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 결합하면, 값 객체와 캐스팅 로직을 하나의 객체로 정의할 수 있습니다. 이를 위해 값 객체의 `castUsing` 메서드에서 `CastsAttributes` 인터페이스를 구현하는 익명 클래스를 반환하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * 캐스팅 클래스 또는 익명 캐스트 클래스를 반환합니다.
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