# Eloquent: 뮤테이터와 캐스팅

- [소개](#introduction)
- [접근자와 뮤테이터](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [뮤테이터 정의하기](#defining-a-mutator)
- [속성 캐스팅](#attribute-casting)
    - [배열 및 JSON 캐스팅](#array-and-json-casting)
    - [날짜 캐스팅](#date-casting)
    - [Enum 캐스팅](#enum-casting)
    - [암호화 캐스팅](#encrypted-casting)
    - [쿼리 타임 캐스팅](#query-time-casting)
- [커스텀 캐스트](#custom-casts)
    - [값 객체 캐스팅](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [입력 값 캐스팅(Inbound Casting)](#inbound-casting)
    - [캐스트 파라미터](#cast-parameters)
    - [캐스터블(Castable)](#castables)

<a name="introduction"></a>
## 소개

접근자(accessor), 뮤테이터(mutator), 속성 캐스팅(attribute casting)을 통해 Eloquent 모델 인스턴스의 속성을 가져오거나 설정할 때 값을 쉽게 변환할 수 있습니다. 예를 들어, [Laravel 암호화기](/docs/{{version}}/encryption)를 사용하여 값을 데이터베이스에 저장할 때 암호화하고, Eloquent 모델에서 속성을 조회할 때 자동으로 복호화할 수 있습니다. 또는 데이터베이스에 저장된 JSON 문자열을 Eloquent 모델에서 접근할 때 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자와 뮤테이터

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 Eloquent 속성 값을 조회할 때 변환을 수행합니다. 접근자를 정의하려면, 모델 내에 접근할 속성을 나타내는 protected 메서드를 생성하면 됩니다. 이 메서드명은 해당 모델 속성 · 데이터베이스 컬럼명에 대해 "카멜 케이스(camel case)" 형식이어야 합니다.

예를 들어, `first_name` 속성에 대한 접근자를 정의해보겠습니다. `first_name` 속성의 값을 조회하려고 할 때 Eloquent가 자동으로 접근자를 호출합니다. 모든 속성 접근자 · 뮤테이터 메서드는 `Illuminate\Database\Eloquent\Casts\Attribute` 반환 타입힌트를 선언해야 합니다:

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

모든 접근자 메서드는 속성의 접근 및 필요하다면 변경(뮤테이트) 방법을 정의하는 `Attribute` 인스턴스를 반환합니다. 위 예제에서는 속성의 접근 방법만 정의합니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인자를 전달합니다.

보시다시피, 실제 컬럼의 원본 값이 접근자로 전달되어, 값을 가공하여 반환할 수 있습니다. 접근자 값을 조회하려면, 단순히 모델 인스턴스의 `first_name` 속성을 참조하면 됩니다:

    use App\Models\User;

    $user = User::find(1);

    $firstName = $user->first_name;

> [!NOTE]  
> 이렇게 계산된 값이 모델의 배열/JSON 표현에 포함되길 원한다면, [해당 값을 추가로 등록해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

접근자가 여러 모델 속성을 하나의 "값 객체"로 변환해야 할 때도 있습니다. 이를 위해 `get` 클로저의 두 번째 인자로 `$attributes`를 받아올 수 있습니다. 이 배열에는 모델의 현재 모든 속성이 담겨 전달됩니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소에 접근합니다.
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

접근자를 통해 값 객체를 반환할 때, 해당 값 객체의 변경 내용은 모델을 저장하기 전에 자동으로 모델에 반영됩니다. 이는 Eloquent가 접근자에서 반환된 인스턴스를 기억하여 같은 접근자가 호출될 때마다 동일한 인스턴스를 반환하기 때문입니다:

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = 'Updated Address Line 1 Value';
    $user->address->lineTwo = 'Updated Address Line 2 Value';

    $user->save();

하지만 원시 타입(문자열, 불리언 등)도 캐싱이 필요할 때가 있습니다. 특히 계산 비용이 비쌀 때 그렇습니다. 이럴 땐 접근자를 정의할 때 `shouldCache` 메서드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

속성의 객체 캐싱 동작을 비활성화하고 싶으면, 접근자 정의 시 `withoutObjectCaching` 메서드를 사용할 수 있습니다:

```php
/**
 * 사용자의 주소에 접근합니다.
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

뮤테이터는 Eloquent 속성 값을 설정할 때 변환을 수행합니다. 뮤테이터를 정의하려면, 속성 정의 시 `set` 인자를 제공하면 됩니다. 예를 들어 `first_name` 속성의 뮤테이터를 정의해보겠습니다. 이 뮤테이터는 모델의 `first_name` 속성 값을 설정할 때 자동으로 호출됩니다:

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

뮤테이터 클로저는 설정되는 값을 인자로 받아 처리한 후 가공된 값을 반환해야 합니다. 뮤테이터를 사용하려면, Eloquent 모델에 단순히 `first_name` 속성을 할당하면 됩니다:

    use App\Models\User;

    $user = User::find(1);

    $user->first_name = 'Sally';

이 예제에서 `set` 콜백엔 `Sally`가 전달됩니다. 뮤테이터는 `strtolower` 함수를 적용해서 가공된 값을 모델의 `$attributes` 배열에 저장합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변환하기

뮤테이터가 여러 모델 속성을 입력해야 할 때도 있습니다. 이럴 땐 `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 모델에 매핑되는 실제 속성명이어야 합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자의 주소에 접근합니다.
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

속성 캐스팅(attribute casting)은 접근자 및 뮤테이터와 유사한 기능을 제공하지만, 별도의 메서드 없이 간단히 속성 타입을 변환할 수 있습니다. 모델의 `$casts` 속성에 캐스팅할 속성과 타입을 배열로 등록하면 됩니다.

`$casts` 속성은 캐스팅할 속성명을 키로, 캐스팅할 타입을 값으로 하는 배열이어야 하며, 지원되는 캐스트 타입은 다음과 같습니다:

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

예를 들어, 데이터베이스에 정수형(0 또는 1)으로 저장된 `is_admin` 속성을 불리언으로 캐스팅해보겠습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 캐스팅할 속성.
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

캐스트를 정의하면 데이터베이스에는 정수로 저장되어 있더라도 `is_admin` 속성에 접근할 때마다 항상 불리언으로 반환됩니다:

    $user = App\Models\User::find(1);

    if ($user->is_admin) {
        // ...
    }

런타임에 임시로 새로운 캐스트를 추가하고 싶다면 `mergeCasts` 메서드를 사용할 수 있습니다. 이 정의는 기존의 캐스트에 추가됩니다:

    $user->mergeCasts([
        'is_admin' => 'integer',
        'options' => 'object',
    ]);

> [!WARNING]  
> 값이 `null`인 속성은 캐스팅되지 않습니다. 또한 관계와 동일한 이름이나 모델의 기본키에 대한 캐스트(혹은 속성)를 정의하면 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 캐스팅

`Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용하면 [유연한 `Illuminate\Support\Stringable` 객체](/docs/{{version}}/strings#fluent-strings-method-list)로 속성을 캐스팅할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\AsStringable;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 캐스팅할 속성.
         *
         * @var array
         */
        protected $casts = [
            'directory' => AsStringable::class,
        ];
    }

<a name="array-and-json-casting"></a>
### 배열 및 JSON 캐스팅

`array` 캐스트는 직렬화된 JSON 형태로 저장된 컬럼을 다룰 때 유용합니다. 예를 들어, 데이터베이스에 JSON이나 TEXT 타입 칼럼이 직렬화된 JSON을 담고 있다면, 해당 속성에 `array` 캐스트를 지정하면 Eloquent 모델에서 접근할 때 자동으로 PHP 배열로 복원해줍니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 캐스팅할 속성.
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

캐스트를 정의하면 `options` 속성에 접근할 때 JSON에서 PHP 배열로 변환됩니다. 값을 저장할 때는 자동으로 배열이 JSON으로 직렬화되어 저장됩니다:

    use App\Models\User;

    $user = User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();

더 간결한 문법으로 JSON 속성의 필드 하나를 업데이트하려면, [해당 속성을 대량 할당 가능한(mass assignable) 속성](/docs/{{version}}/eloquent#mass-assignment-json-columns)으로 지정하고 `->` 연산자를 이용한 `update`를 사용할 수 있습니다:

    $user = User::find(1);

    $user->update(['options->key' => 'value']);

<a name="array-object-and-collection-casting"></a>
#### ArrayObject 및 컬렉션 캐스팅

기본 `array` 캐스트는 많은 상황에 적합하지만, 배열 오프셋을 직접 변경할 수 없는 단점이 있습니다. 예를 들어, 아래 코드와 같이 값을 변경하면 PHP 에러가 발생합니다:

    $user = User::find(1);

    $user->options['key'] = $value;

이를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스로 캐스팅해주는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts) 구현을 활용하여, 개별 오프셋 수정 시 PHP 에러 없이 객체가 캐싱·변환됩니다. 사용법은 아래와 같습니다:

    use Illuminate\Database\Eloquent\Casts\AsArrayObject;

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'options' => AsArrayObject::class,
    ];

마찬가지로, `AsCollection` 캐스트를 사용하면 JSON 속성을 Laravel [Collection](/docs/{{version}}/collections) 인스턴스로 변환할 수 있습니다:

    use Illuminate\Database\Eloquent\Casts\AsCollection;

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'options' => AsCollection::class,
    ];

`AsCollection` 캐스트로 기본 컬렉션이 아닌 커스텀 컬렉션 클래스를 사용하고 싶다면, 캐스트 인자에 컬렉션 클래스명을 전달할 수 있습니다:

    use App\Collections\OptionCollection;
    use Illuminate\Database\Eloquent\Casts\AsCollection;

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'options' => AsCollection::class.':'.OptionCollection::class,
    ];

<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP `DateTime`을 확장한 강력한 날짜/시간 라이브러리입니다. 추가로 날짜 속성을 캐스팅하려면, `$casts` 프로퍼티에 해당 속성을 `datetime` 또는 `immutable_datetime` 타입으로 지정하면 됩니다.

`date` 또는 `datetime` 캐스트를 정의할 때, 날짜의 포맷도 지정할 수 있습니다. 포맷은 [모델이 배열 또는 JSON으로 직렬화](/docs/{{version}}/eloquent-serialization)될 때 사용됩니다:

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'created_at' => 'datetime:Y-m-d',
    ];

컬럼이 날짜로 캐스팅되면, 속성 값에 유닉스 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, `DateTime`/`Carbon` 객체를 할당할 수 있으며, 형식에 맞게 데이터베이스에 저장됩니다.

모델의 모든 날짜 기본 직렬화 포맷을 바꾸고 싶다면, 모델에 `serializeDate` 메서드를 정의하면 됩니다. 이 메서드는 데이터베이스 저장 포맷에는 영향을 주지 않습니다:

    /**
     * 날짜를 배열 / JSON 직렬화용으로 준비합니다.
     */
    protected function serializeDate(DateTimeInterface $date): string
    {
        return $date->format('Y-m-d');
    }

데이터베이스 저장 시 실제로 쓸 포맷을 지정하려면, `$dateFormat` 속성을 정의할 수 있습니다:

    /**
     * 날짜 컬럼의 저장 포맷.
     *
     * @var string
     */
    protected $dateFormat = 'U';

<a name="date-casting-and-timezones"></a>
#### 날짜 캐스팅과 직렬화, 그리고 타임존

기본적으로 `date` 및 `datetime` 캐스트로 직렬화된 날짜는 애플리케이션의 `timezone` 설정에 상관없이 항상 UTC ISO-8601 날짜 문자열(`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`)로 변환됩니다. 이 직렬화 포맷과 애플리케이션의 날짜를 UTC 타임존에 저장(설정 변경 없이 기본값인 UTC 유지)하는 것이 강력히 권장됩니다. UTC 타임존을 일관되게 사용하면 PHP/JS의 기타 날짜 처리 라이브러리와의 호환성이 극대화됩니다.

`date` 또는 `datetime` 캐스트에 커스텀 포맷(예: `datetime:Y-m-d H:i:s`)을 적용하면, Carbon 인스턴스의 내부 타임존이 사용됩니다. 일반적으로 이 타임존은 애플리케이션의 `timezone` 설정이 반영됩니다.

<a name="enum-casting"></a>
### Enum 캐스팅

Eloquent는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 직접 캐스팅할 수 있습니다. 사용하려면, 모델의 `$casts` 배열에 캐스팅하려는 속성과 Enum 클래스를 지정하면 됩니다:

    use App\Enums\ServerStatus;

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'status' => ServerStatus::class,
    ];

이렇게 하면 해당 속성에 할당하거나 접근할 때 Enum 객체와 값이 서로 자동 변환됩니다:

    if ($server->status == ServerStatus::Provisioned) {
        $server->status = ServerStatus::Ready;

        $server->save();
    }

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 캐스팅

모델에서 Enum 값들의 배열을 하나의 컬럼에 저장해야 할 경우, Laravel에서 제공하는 `AsEnumArrayObject`, `AsEnumCollection` 캐스트를 사용할 수 있습니다:

    use App\Enums\ServerStatus;
    use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
    ];

<a name="encrypted-casting"></a>
### 암호화 캐스팅

`encrypted` 캐스트를 사용하면 Laravel의 내장 [암호화 기능](/docs/{{version}}/encryption)으로 속성값이 암호화됩니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등도 해당 속성을 암호화하여 저장합니다.

암호화된 텍스트는 평문보다 길고 최종 길이를 예측할 수 없으므로, 관련 데이터베이스 컬럼 타입은 반드시 `TEXT` 이상이어야 합니다. 또한 값이 암호화되어 저장되므로 DB에서 암호화된 필드값을 조회/검색할 수 없습니다.

<a name="key-rotation"></a>
#### 키 롤링(Key Rotation)

Laravel은 애플리케이션의 `app` 설정파일 내 `key` 설정값(일반적으로 환경변수 `APP_KEY`)으로 문자열을 암호화합니다. 암호화 키를 변경(롤링)해야 한다면, 새로운 키로 DB에 저장된 암호화된 속성값을 수동으로 다시 암호화해야 합니다.

<a name="query-time-casting"></a>
### 쿼리 타임 캐스팅

가끔 쿼리 실행 중에 캐스트를 적용해야 할 수 있습니다. 예를 들어, 테이블에서 Raw 값을 조회할 때 다음과 같이 쿼리를 작성했다고 합시다:

    use App\Models\Post;
    use App\Models\User;

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->get();

이 쿼리 결과의 `last_posted_at` 속성은 단순한 문자열로 반환됩니다. 만약 이 속성에 `datetime` 캐스트를 쿼리 실행시에 적용하고 싶다면, `withCasts` 메서드를 사용하면 됩니다:

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->withCasts([
        'last_posted_at' => 'datetime'
    ])->get();

<a name="custom-casts"></a>
## 커스텀 캐스트

Laravel에는 기본적으로 다양한 타입의 편리한 캐스트가 있지만, 필요에 따라 커스텀 캐스트 타입을 만들 수도 있습니다. 캐스트를 생성하려면 `make:cast` 아티즌 명령을 실행하세요. 새로운 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다.

```shell
php artisan make:cast Json
```

모든 커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, `get`과 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스팅값으로 변환하며, `set`은 캐스팅값을 데이터베이스에 저장할 원시값으로 변환해야 합니다. 예시로, Laravel 내장 `json` 캐스트를 커스텀 캐스트로 재구현해보겠습니다.

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
    use Illuminate\Database\Eloquent\Model;

    class Json implements CastsAttributes
    {
        /**
         * 값 캐스팅.
         *
         * @param  array<string, mixed>  $attributes
         * @return array<string, mixed>
         */
        public function get(Model $model, string $key, mixed $value, array $attributes): array
        {
            return json_decode($value, true);
        }

        /**
         * 저장용 값 가공.
         *
         * @param  array<string, mixed>  $attributes
         */
        public function set(Model $model, string $key, mixed $value, array $attributes): string
        {
            return json_encode($value);
        }
    }

커스텀 캐스트 타입을 정의했다면, 클래스명을 속성에 지정해 사용할 수 있습니다:

    <?php

    namespace App\Models;

    use App\Casts\Json;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 캐스팅할 속성.
         *
         * @var array
         */
        protected $casts = [
            'options' => Json::class,
        ];
    }

<a name="value-object-casting"></a>
### 값 객체 캐스팅

캐스팅은 원시 타입에 한정되지 않습니다. 속성을 객체로도 캐스팅할 수 있습니다. 객체로 캐스팅하는 커스텀 캐스트 정의는 원시 타입의 경우와 거의 유사하지만, `set` 메서드는 모델에 저장될 수 있는 키/값 쌍의 배열을 반환해야 합니다.

예시로, 여러 모델 속성을 하나의 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의하겠습니다. 이 객체는 `lineOne`과 `lineTwo` 두 프로퍼티를 갖는다고 가정합니다:

    <?php

    namespace App\Casts;

    use App\ValueObjects\Address as AddressValueObject;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
    use Illuminate\Database\Eloquent\Model;
    use InvalidArgumentException;

    class Address implements CastsAttributes
    {
        /**
         * 값 캐스팅.
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
         * 저장용 값 가공.
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

값 객체로 캐스팅한 후 객체를 변경하면, 저장 전에 모델에 자동으로 반영됩니다:

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = 'Updated Address Value';

    $user->save();

> [!NOTE]  
> 값 객체를 갖는 Eloquent 모델을 배열/JSON으로 직렬화할 계획이라면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스를 구현하는 것이 좋습니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성은 Eloquent에서 캐싱되므로, 동일 속성을 다시 접근하면 항상 같은 객체 인스턴스가 반환됩니다.

특정 커스텀 캐스트 클래스에서 객체 캐싱을 비활성화하고 싶다면, 클래스에 public한 `withoutObjectCaching` 속성을 선언하십시오:

```php
class Address implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```

<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델의 `toArray`, `toJson` 메서드로 배열/JSON 변환 시, 커스텀 캐스트 값 객체는 일반적으로 `Illuminate\Contracts\Support\Arrayable`, `JsonSerializable` 인터페이스가 구현되어 있다면 자동으로 직렬화됩니다. 그러나 서드파티 라이브러리의 값 객체는 인터페이스 구현이 불가능할 수 있습니다.

이럴 때 커스텀 캐스트 클래스에서 값 객체 직렬화를 책임지도록 지정할 수 있습니다. 클래스를 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스로 구현하면, 클래스 내 `serialize` 메서드에서 객체의 직렬화 형태를 반환해야 합니다:

    /**
     * 값의 직렬화 표현 반환.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function serialize(Model $model, string $key, mixed $value, array $attributes): string
    {
        return (string) $value;
    }

<a name="inbound-casting"></a>
### 입력 값 캐스팅(Inbound Casting)

때로는 모델에 값을 할당(set)할 때만 값을 변환하고, 조회(get)할 때는 변환하지 않는 커스텀 캐스트 클래스가 필요할 수 있습니다.

입력 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `set` 메서드만 필요합니다. 아티즌 명령어 실행 시 `--inbound` 옵션을 추가해 생성할 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

입력 전용 캐스트 대표 예시는 "해싱" 캐스트입니다. 예를 들어, 입력값을 주어진 알고리즘으로 해시하는 캐스트를 만들 수 있습니다:

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
    use Illuminate\Database\Eloquent\Model;

    class Hash implements CastsInboundAttributes
    {
        /**
         * 새 인스턴스를 생성합니다.
         */
        public function __construct(
            protected string|null $algorithm = null,
        ) {}

        /**
         * 저장용 값 가공.
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

<a name="cast-parameters"></a>
### 캐스트 파라미터

커스텀 캐스트를 모델에 지정할 때, `:`로 구분하여 파라미터를 전달할 수 있습니다. 여러 파라미터는 쉼표로 구분합니다. 이 파라미터들은 캐스트 클래스 생성자에 전달됩니다:

    /**
     * 캐스팅할 속성.
     *
     * @var array
     */
    protected $casts = [
        'secret' => Hash::class.':sha256',
    ];

<a name="castables"></a>
### 캐스터블(Castable)

애플리케이션의 값 객체가 자체적으로 커스텀 캐스트 클래스를 지정하도록 하고 싶을 수 있습니다. 모델에 커스텀 캐스트 클래스명을 지정하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현한 값 객체 클래스를 속성에 지정해도 됩니다:

    use App\ValueObjects\Address;

    protected $casts = [
        'address' => Address::class,
    ];

`Castable` 인터페이스를 구현한 객체는 `castUsing` 메서드를 반드시 정의해야 하며, 이 메서드는 해당 객체의 변환을 담당하는 캐스터(캐스트 클래스)명을 반환해야 합니다:

    <?php

    namespace App\ValueObjects;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use App\Casts\Address as AddressCast;

    class Address implements Castable
    {
        /**
         * 이 객체의 캐스팅 담당 캐스터 클래스명을 반환합니다.
         *
         * @param  array<string, mixed>  $arguments
         */
        public static function castUsing(array $arguments): string
        {
            return AddressCast::class;
        }
    }

`Castable` 클래스 사용 시에도 `$casts` 정의에 인자를 추가할 수 있습니다. 이 인자는 `castUsing` 메서드에 전달됩니다:

    use App\ValueObjects\Address;

    protected $casts = [
        'address' => Address::class.':argument',
    ];

<a name="anonymous-cast-classes"></a>
#### 캐스터블 & 익명 클래스

"캐스터블"과 PHP [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합하면, 값 객체와 캐스팅 로직을 하나의 캐스터블 객체로 정의할 수 있습니다. 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환하세요. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

    <?php

    namespace App\ValueObjects;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Address implements Castable
    {
        // ...

        /**
         * 이 객체의 캐스팅에 사용할 캐스터 클래스 반환.
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
