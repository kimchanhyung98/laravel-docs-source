# Eloquent: 접근자 & 변환(Casting)

- [소개](#introduction)
- [접근자 & 변조자(Mutators)](#accessors-and-mutators)
    - [접근자 정의하기](#defining-an-accessor)
    - [변조자 정의하기](#defining-a-mutator)
- [속성 형 변환(Attribute Casting)](#attribute-casting)
    - [Array & JSON 형 변환](#array-and-json-casting)
    - [날짜 형 변환](#date-casting)
    - [Enum 형 변환](#enum-casting)
    - [암호화 형 변환](#encrypted-casting)
    - [쿼리 실행 시 형 변환](#query-time-casting)
- [커스텀 변환 정의하기](#custom-casts)
    - [값 객체 변환](#value-object-casting)
    - [배열 / JSON 직렬화](#array-json-serialization)
    - [입력값에 대한 변환(Inbound Casting)](#inbound-casting)
    - [변환 파라미터(Cast Parameters)](#cast-parameters)
    - [캐스터블(Castables)](#castables)

<a name="introduction"></a>
## 소개

접근자(Accessor), 변조자(Mutator), 속성 형 변환(Attribute Casting)은 Eloquent 모델 인스턴스에서 속성을 가져오거나 설정할 때 값을 변환할 수 있게 해줍니다. 예를 들어, [Laravel의 암호화 도구](/docs/{{version}}/encryption)를 이용해 값을 DB에 저장할 때 암호화하고, Eloquent 모델에서 해당 속성을 읽을 때 자동으로 복호화할 수 있습니다. 또는, DB에 JSON 문자열로 저장된 값을 Eloquent 모델을 통해 배열로 변환할 수도 있습니다.

<a name="accessors-and-mutators"></a>
## 접근자 & 변조자

<a name="defining-an-accessor"></a>
### 접근자 정의하기

접근자는 속성 값에 접근할 때 변환 동작을 수행합니다. 접근자를 정의하려면, 모델에 접근할 속성에 해당하는 protected 메소드를 만들어야 하며, 이 메소드의 이름은 실제 모델 속성/DB 컬럼의 카멜케이스(camel case) 표기와 일치해야 합니다.

아래 예제에서는 `first_name` 속성에 대한 접근자를 정의합니다. 접근자는 Eloquent가 `first_name` 속성의 값을 가져올 때 자동으로 호출됩니다. 모든 접근자/변조자 메소드는 `Illuminate\Database\Eloquent\Casts\Attribute` 타입을 리턴해야 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\Attribute;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 사용자 이름 접근자(getter)
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

모든 접근자 메소드는 속성을 어떻게 읽을지(선택적으로 쓸지도) 정의하는 `Attribute` 인스턴스를 반환합니다. 예제에서는 읽기 동작만 정의하였고, `Attribute` 클래스 생성자에 `get` 인자를 전달합니다.

보시다시피, 접근자에는 컬럼의 원래 값이 넘어와서 값을 조작하고 반환할 수 있습니다. 접근자 값을 읽으려면, 모델 인스턴스에서 그냥 해당 속성에 접근하면 됩니다:

    use App\Models\User;

    $user = User::find(1);

    $firstName = $user->first_name;

> **참고**  
> 계산된 값들이 배열/JSON 변환 시 결과에 포함되길 원한다면, [별도의 작업이 필요합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성으로 값 객체 만들기

경우에 따라 접근자가 여러 모델 속성을 하나의 "값 객체"로 변환해야 할 수도 있습니다. 이 때는 `get` 클로저의 두 번째 인자로 `$attributes`를 받아서, 모든 모델 속성이 배열로 전달되도록 할 수 있습니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자 주소 속성을 다룹니다.
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
#### 접근자 캐싱

접근자에서 값 객체를 반환하는 경우, 해당 객체에서 변경된 사항은 모델 저장 시 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자에서 반환된 인스턴스를 내부적으로 재사용하기 때문입니다:

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = '변경된 주소 1';
    $user->address->lineTwo = '변경된 주소 2';

    $user->save();

또한 문자열, 불린 등 원시 타입 값에 대해서도 성능상 캐싱을 하고 싶을 수 있습니다. 이럴 때는 접근자 정의 시 `shouldCache` 메소드를 호출하면 됩니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn ($value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

반대로, 객체 캐싱 행동을 비활성화하려면 `withoutObjectCaching` 메소드를 사용하세요:

```php
/**
 * 사용자 주소 접근자
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
### 변조자(Mutator) 정의하기

변조자는 속성에 값을 할당할 때 변환 동작을 실행합니다. 변조자를 정의하려면, 속성 정의 시 `set` 인자를 전달하면 됩니다. 아래는 `first_name` 속성에 대한 변조자 예제입니다. 이 변조자는 해당 속성 값을 모델에 할당할 때 자동으로 호출됩니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\Attribute;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 사용자 이름 변조자(setter)
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

변조자의 클로저에는 설정하려는 값이 들어오며, 이 값을 조작해서 반환하면 됩니다. 사용 예시는 다음과 같습니다:

    use App\Models\User;

    $user = User::find(1);

    $user->first_name = 'Sally';

이 경우, `set` 콜백이 `Sally` 값을 받아 `strtolower` 함수로 소문자 변환 후 모델의 내부 `$attributes` 배열에 저장하게 됩니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 한 번에 변경하기

변조자에서 여러 속성을 한 번에 설정하려면, `set` 클로저에서 배열을 반환하면 됩니다. 배열의 각 키는 실제 속성/DB 컬럼명에 대응해야 합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * 사용자 주소 변조자
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
## 속성 형 변환(Attribute Casting)

속성 형 변환은 접근자/변조자와 비슷한 기능을 제공하지만, 별다른 메소드를 직접 정의하지 않아도 됩니다. 모델의 `$casts` 속성에 형 변환 정보를 지정하면 공통 데이터 타입으로 손쉽게 변환할 수 있습니다.

`$casts` 속성은 속성명(키)과 변환하려는 타입(값)의 배열이어야 하며, 지원하는 변환 타입은 아래와 같습니다:

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

예를 들어, DB에 0 또는 1로 저장된 `is_admin` 속성을 boolean으로 캐스팅하고 싶다면 아래와 같이 하면 됩니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 형 변환할 속성 지정
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

이후 해당 속성을 읽으면 언제나 boolean으로 변환되어 반환됩니다:

    $user = App\Models\User::find(1);

    if ($user->is_admin) {
        //
    }

런타임에 임시로 형 변환을 추가하려면 `mergeCasts` 메소드를 사용하세요. 이 때 정의된 변환은 기존 캐스팅 정의에 추가됩니다:

    $user->mergeCasts([
        'is_admin' => 'integer',
        'options' => 'object',
    ]);

> **경고**  
> 값이 `null`인 속성은 변환되지 않습니다. 또한 관계명과 동일한 이름의 속성에 캐스트(또는 속성)를 지정해서는 안 됩니다.

<a name="stringable-casting"></a>
#### Stringable 형 변환

`Illuminate\Database\Eloquent\Casts\AsStringable`를 사용하면 모델 속성을 [유연한 `Illuminate\Support\Stringable` 객체](/docs/{{version}}/helpers#fluent-strings-method-list)로 변환할 수 있습니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\AsStringable;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 형 변환할 속성 지정
         *
         * @var array
         */
        protected $casts = [
            'directory' => AsStringable::class,
        ];
    }

<a name="array-and-json-casting"></a>
### Array & JSON 형 변환

`array` 캐스트는 직렬화된 JSON 값이 저장된 컬럼에 매우 유용합니다. 예를 들어, DB에 `JSON` 또는 `TEXT` 타입 컬럼에 직렬화된 JSON이 저장되어 있다면, `array` 캐스트를 지정하게 되면 Eloquent 모델에서 해당 속성을 읽을 때 자동으로 PHP 배열로 변환해줍니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 형 변환할 속성 지정
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

캐스트를 정의하면, `options` 속성을 읽을 때 자동으로 JSON에서 PHP 배열로 역직렬화됩니다. 값을 설정할 때는 전달한 배열을 JSON으로 직렬화해서 저장합니다:

    use App\Models\User;

    $user = User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();

더 간결하게 JSON 속성의 일부만 직접 업데이트하려면 `update` 메소드에 `->` 연산자를 사용할 수 있습니다:

    $user = User::find(1);

    $user->update(['options->key' => 'value']);

<a name="array-object-and-collection-casting"></a>
#### ArrayObject & Collection 형 변환

기본 `array` 캐스트로 충분한 경우도 있지만, 배열 오프셋을 직접 수정하려면 PHP 에러가 발생할 수 있습니다:

    $user = User::find(1);

    $user->options['key'] = $value;

이 문제를 해결하려면, JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php)로 변환하는 `AsArrayObject` 캐스트를 사용할 수 있습니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts) 구현을 바탕으로 하며, 오프셋 수정이 자유롭고, PHP 에러가 발생하지 않습니다:

    use Illuminate\Database\Eloquent\Casts\AsArrayObject;

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'options' => AsArrayObject::class,
    ];

비슷하게, JSON 속성을 Laravel [Collection](/docs/{{version}}/collections) 인스턴스로 변환하는 `AsCollection` 캐스트도 제공됩니다:

    use Illuminate\Database\Eloquent\Casts\AsCollection;

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'options' => AsCollection::class,
    ];

<a name="date-casting"></a>
### 날짜 형 변환

기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 변환합니다(Carbon은 PHP의 `DateTime`을 확장한 클래스입니다). 추가적인 날짜 속성을 캐스팅하려면 모델 `$casts` 배열에 해당 속성을 추가하면 됩니다. 일반적으로는 `datetime` 또는 `immutable_datetime` 타입이 적합합니다.

`date` 또는 `datetime` 캐스트 정의 시, 포맷도 지정할 수 있습니다. 이 포맷은 [모델의 배열/JSON 직렬화 시](docs/{{version}}/eloquent-serialization) 적용됩니다:

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'created_at' => 'datetime:Y-m-d',
    ];

날짜로 캐스트된 컬럼 값에는 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime`/`Carbon` 인스턴스를 할당할 수 있습니다. DB에는 올바른 형식으로 저장됩니다.

모델 전체의 날짜 기본 직렬화 포맷을 변경하고 싶다면 `serializeDate` 메소드를 모델에 정의하면 됩니다. 이 메소드는 DB 저장 형식에 영향을 주지 않습니다:

    /**
     * 배열/JSON 직렬화를 위한 날짜 포맷 반환
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d');
    }

모델의 날짜 값을 DB에 저장할 때 사용할 포맷을 지정하려면 `$dateFormat` 속성을 정의하세요:

    /**
     * 날짜 컬럼의 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';

<a name="date-casting-and-timezones"></a>
#### 날짜 형변환, 직렬화, 그리고 타임존

기본적으로 `date` 및 `datetime` 형 변환은 날자를 항상 UTC ISO-8601 날짜 문자열(`1986-05-28T21:05:54.000000Z`)로 직렬화합니다. 애플리케이션의 `timezone` 설정값과는 무관하며, UTC를 기본으로 사용하는 것이 권장됩니다. 이렇게 하면 PHP와 JavaScript 등 다양한 라이브러리와의 호환성이 극대화됩니다.

만일 `datetime:Y-m-d H:i:s`처럼 커스텀 포맷을 지정하면, Carbon 인스턴스 내부 타임존(주로 애플리케이션 `timezone` 설정이 사용됩니다)이 직렬화에 적용됩니다.

<a name="enum-casting"></a>
### Enum 형 변환

> **경고**  
> Enum 형 변환은 PHP 8.1 이상에서만 지원됩니다.

Eloquent는 속성 값을 PHP [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 캐스팅 할 수도 있습니다. 모델의 `$casts` 속성에 Enum 클래스를 지정하면 됩니다:

    use App\Enums\ServerStatus;

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'status' => ServerStatus::class,
    ];

이제 모델에서 속성에 접근하거나 할당할 때 Enum 인스턴스로 자동 변환됩니다:

    if ($server->status == ServerStatus::Provisioned) {
        $server->status = ServerStatus::Ready;

        $server->save();
    }

<a name="casting-arrays-of-enums"></a>
#### Enum 배열 형 변환

모델이 하나의 컬럼에 여러 Enum 값을 배열로 저장해야 할 때는, Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

    use App\Enums\ServerStatus;
    use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
    ];

<a name="encrypted-casting"></a>
### 암호화 형 변환

`encrypted` 캐스트는 모델 속성 값을 Laravel의 내장 [암호화](/docs/{{version}}/encryption) 기능으로 암호화해 저장합니다. 또한 `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, `AsEncryptedCollection` 등도 제공되며, 비암호화 버전과 사용법은 동일하나 DB에는 암호화되어 저장됩니다.

암호화된 값은 평문보다 길어질 수 있고 크기를 예측할 수 없으므로, 해당 컬럼 타입이 `TEXT` 이상이어야 합니다. 또한 DB 내 값이 암호화되어 있으므로, 쿼리로 암호화된 속성 값을 조회/검색하는 것은 불가능합니다.

<a name="key-rotation"></a>
#### 암호화 키 교체(Key Rotation)

Laravel은 앱 설정 파일의 `key` 값(보통 `.env`의 `APP_KEY`)을 사용하여 문자열을 암호화합니다. 만약 키를 교체해야 하는 경우 기존 암호화 속성들을 새 키로 직접 재암호화해주어야 합니다.

<a name="query-time-casting"></a>
### 쿼리 실행 시 형 변환

때로는 쿼리 실행 시에만 형 변환이 필요할 수 있습니다(예: 테이블에서 raw value를 조회하는 경우). 예를 들어, 아래와 같은 서브쿼리를 생각해 볼 수 있습니다:

    use App\Models\Post;
    use App\Models\User;

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->get();

이 때 결과의 `last_posted_at` 속성은 문자열로 반환됩니다. 이 값을 조회 시에만 `datetime`으로 캐스팅하려면, `withCasts` 메소드를 사용할 수 있습니다:

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->withCasts([
        'last_posted_at' => 'datetime'
    ])->get();

<a name="custom-casts"></a>
## 커스텀 변환(Cast) 정의하기

Laravel은 다양한 기본 캐스트 타입도 제공하지만, 직접 커스텀 캐스트 타입을 정의할 수 있습니다. 캐스트를 만들려면 Artisan 명령어를 사용하세요. 새 캐스트 클래스는 `app/Casts` 디렉터리에 생성됩니다:

```shell
php artisan make:cast Json
```

커스텀 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현해야 하며, 반드시 `get`과 `set` 메소드가 필요합니다. DB의 값을 가져올 때 변환하는 동작은 `get`, 값을 저장할 때 변환하는 동작은 `set` 메소드에 작성합니다. 예제에서는 `json` 캐스트를 커스텀으로 구현했습니다:

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Json implements CastsAttributes
    {
        /**
         * 값을 캐스트해서 반환
         */
        public function get($model, $key, $value, $attributes)
        {
            return json_decode($value, true);
        }

        /**
         * 저장을 위한 값 준비
         */
        public function set($model, $key, $value, $attributes)
        {
            return json_encode($value);
        }
    }

커스텀 캐스트 타입을 정의했다면, 모델 속성에 클래스명을 지정해 사용할 수 있습니다:

    <?php

    namespace App\Models;

    use App\Casts\Json;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 형 변환할 속성 지정
         *
         * @var array
         */
        protected $casts = [
            'options' => Json::class,
        ];
    }

<a name="value-object-casting"></a>
### 값 객체 형 변환

기본 타입뿐 아니라 객체로도 속성 변환이 가능합니다. 객체로 변환하는 커스텀 캐스트를 만드는 방법은 원시형과 유사하지만, `set` 메소드에서 키/값 쌍의 배열을 반환해야 하며, 각 키는 DB 컬럼에 대응해야 합니다.

예를 들어 두 개의 값을 가진 `Address` 값 객체로 여러 모델 속성을 변환하는 커스텀 캐스트 클래스는 다음과 같습니다:

    <?php

    namespace App\Casts;

    use App\ValueObjects\Address as AddressValueObject;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
    use InvalidArgumentException;

    class Address implements CastsAttributes
    {
        public function get($model, $key, $value, $attributes)
        {
            return new AddressValueObject(
                $attributes['address_line_one'],
                $attributes['address_line_two']
            );
        }

        public function set($model, $key, $value, $attributes)
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

값 객체로 캐스트된 경우, 값 객체를 수정하면 모델 저장시 자동으로 동기화 처리됩니다:

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = '변경된 주소 값';

    $user->save();

> **참고**  
> 값 객체를 포함하는 Eloquent 모델을 JSON 또는 배열로 직렬화할 계획이라면, 해당 값 객체에 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="array-json-serialization"></a>
### 배열/JSON 직렬화

Eloquent 모델이 `toArray`나 `toJson`으로 변환될 때, 커스텀 캐스트된 값 객체가 만약 `Arrayable`·`JsonSerializable` 인터페이스를 구현한다면 값 역시 올바르게 직렬화됩니다. 그러나 외부 라이브러리의 값 객체 등은 직접 변경이 어려울 수도 있습니다.

이런 경우에는 커스텀 캐스트 클래스에 직접 직렬화 책임을 지정할 수 있습니다. 이를 위해 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현하고, `serialize` 메소드 내에 객체의 직렬 로직을 작성합니다:

    /**
     * 값의 직렬화 표현 반환
     */
    public function serialize($model, string $key, $value, array $attributes)
    {
        return (string) $value;
    }

<a name="inbound-casting"></a>
### 입력값에 대한 변환(Inbound Casting)

때로는 값이 모델에 세팅될 때만 동작하고, 읽을 때는 아무 동작도 하지 않는 커스텀 캐스트가 필요할 수 있습니다.

입력값 변환 전용 캐스트는 `CastsInboundAttributes` 인터페이스를 구현하며, `set` 메소드만 구현하면 됩니다. Artisan 명령에서 `--inbound` 옵션으로 이 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast Hash --inbound
```

입력값 전용 캐스트의 대표적 예시는 "해시" 캐스트입니다:

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;

    class Hash implements CastsInboundAttributes
    {
        protected $algorithm;

        public function __construct($algorithm = null)
        {
            $this->algorithm = $algorithm;
        }

        public function set($model, $key, $value, $attributes)
        {
            return is_null($this->algorithm)
                        ? bcrypt($value)
                        : hash($this->algorithm, $value);
        }
    }

<a name="cast-parameters"></a>
### 변환 파라미터(Cast Parameters)

커스텀 캐스트에 파라미터를 전달하고 싶을 때 클래스명 뒤에 `:`로 구분하여 지정할 수 있습니다. 여러 파라미터는 콤마로 구분합니다. 이 값들은 캐스트 클래스의 생성자로 전달됩니다:

    /**
     * 형 변환할 속성 지정
     *
     * @var array
     */
    protected $casts = [
        'secret' => Hash::class.':sha256',
    ];

<a name="castables"></a>
### 캐스터블(Castables)

애플리케이션의 값 객체가 자체적으로 커스텀 캐스터 클래스를 정의하도록 할 수도 있습니다. 이 경우 모델에 커스텀 캐스터를 지정하는 대신, 해당 값 객체 클래스에 `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하면 됩니다:

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class,
    ];

`Castable` 인터페이스를 구현하는 객체는 `castUsing` 정적 메소드를 통해 변환에 사용할 캐스터 클래스명을 반환해야 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use App\Casts\Address as AddressCast;

    class Address implements Castable
    {
        public static function castUsing(array $arguments)
        {
            return AddressCast::class;
        }
    }

캐스터블 클래스 사용 시, `$casts` 정의에서 파라미터를 넘길 수도 있으며, 파라미터는 `castUsing` 메소드에 전달됩니다:

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class.':argument',
    ];

<a name="anonymous-cast-classes"></a>
#### 캐스터블 & 익명 캐스트 클래스

"캐스터블"과 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)를 조합하면, 값 객체와 그 변환 로직을 하나의 객체로 묶어 정의할 수 있습니다. `castUsing` 메소드에서 익명 클래스를 반환하며, 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Address implements Castable
    {
        // ...

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
