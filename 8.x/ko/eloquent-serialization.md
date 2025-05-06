# Eloquent: 직렬화(Serialization)

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel로 API를 구축할 때 모델과 관계(Relationship)를 배열 또는 JSON으로 변환하는 경우가 많습니다. Eloquent는 이러한 변환을 편리하게 처리할 수 있는 메서드를 제공하며, 또한 직렬화된 모델 표현에 어떤 속성이 포함될지 제어할 수 있습니다.

> {tip} Eloquent 모델과 컬렉션의 JSON 직렬화를 더 견고하게 처리하고 싶다면 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources)에 대한 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 미리 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면, `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 관계(관계의 관계까지 포함)가 배열로 변환됩니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 모델의 속성만 배열로 변환하며, 관계는 포함하지 않습니다:

```php
$user = User::first();

return $user->attributesToArray();
```

또한, 모델의 전체 [컬렉션](/docs/{{version}}/eloquent-collections)도 컬렉션 인스턴스에서 `toArray` 메서드를 호출하여 배열로 변환할 수 있습니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`처럼 `toJson`도 재귀적으로 동작하여, 모든 속성과 관계가 JSON으로 변환됩니다. 또한 [PHP가 지원하는](https://secure.php.net/manual/en/function.json-encode.php) 모든 JSON 인코딩 옵션을 지정할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또한, 모델 또는 컬렉션을 문자열로 캐스팅하면 `toJson` 메서드가 자동으로 호출됩니다:

```php
return (string) User::find(1);
```

모델과 컬렉션이 문자열로 캐스팅될 때 JSON으로 변환되므로, 애플리케이션의 라우트 또는 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. 라라벨은 라우트 또는 컨트롤러에서 Eloquent 모델과 컬렉션을 반환할 때 이를 자동으로 JSON으로 직렬화합니다:

```php
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계(Relationships)

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 또한 Eloquent 관계는 "카멜 케이스" 메서드명으로 정의되지만, 관계의 JSON 속성은 "스네이크 케이스"로 표현됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때로는 비밀번호 등, 모델의 배열 또는 JSON 표현에서 특정 속성을 제외하고 싶을 수 있습니다. 이를 위해 모델에 `$hidden` 속성을 추가하세요. `$hidden` 속성에 나열된 속성들은 직렬화된 모델 표현에 포함되지 않습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 숨겨질 속성.
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> {tip} 관계를 숨기려면 관계의 메서드명을 Eloquent 모델의 `$hidden` 속성에 추가하세요.

또는, `visible` 속성을 사용해 모델의 배열 및 JSON 표현에서 포함시킬 속성을 "허용 리스트"로 정의할 수 있습니다. `$visible` 배열에 없는 모든 속성은 배열 또는 JSON으로 변환 시 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 표시할 속성.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 표시여부 임시 변경하기

일반적으로 숨겨진 속성을 특정 모델 인스턴스에서만 보이게 하고 싶다면, `makeVisible` 메서드를 사용하세요. `makeVisible`은 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();
```

반대로, 일반적으로 보이는 속성을 임시로 숨기고 싶다면 `makeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때, DB 컬럼에 직접 대응되지 않는 속성을 추가하고 싶을 수 있습니다. 그러려면 먼저 해당 값에 대한 [접근자(Accessor)](/docs/{{version}}/eloquent-mutators)를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자인지 판별.
     *
     * @return bool
     */
    public function getIsAdminAttribute()
    {
        return $this->attributes['admin'] === 'yes';
    }
}
```

액세서 정의 후, 속성명을 모델의 `appends` 속성에 추가하세요. 액세서의 PHP 메서드는 "카멜 케이스"로 정의되지만, 속성명은 보통 "스네이크 케이스"의 직렬화 표현을 사용합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 배열 표현에 추가할 액세서 목록.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

속성이 `appends` 목록에 추가되면, 모델의 배열 및 JSON 표현 모두에 포함됩니다. `appends` 배열의 속성도 `visible`, `hidden` 속성 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 값 추가하기

런타임에서 모델 인스턴스에 추가적인 속성을 추가하고 싶으면 `append` 메서드를 사용하세요. 또는 `setAppends` 메서드로 주어진 모델 인스턴스의 전체 추가 속성 배열을 덮어쓸 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 날짜 포맷을 커스터마이즈하고 싶다면 `serializeDate` 메서드를 오버라이딩하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다:

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

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

개별 Eloquent 날짜 속성의 직렬화 포맷을 지정하려면, 모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정하면 됩니다:

```php
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```
