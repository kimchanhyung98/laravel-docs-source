# Eloquent: 직렬화 (Serialization)

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel을 사용해 API를 구축할 때, 모델과 연관 관계를 배열 또는 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 쉽게 할 수 있도록 편리한 메서드를 제공하며, 모델의 직렬화된 표현에 포함할 속성을 제어할 수 있습니다.

> [!NOTE]
> 보다 견고한 Eloquent 모델과 컬렉션의 JSON 직렬화 처리를 위해 [Eloquent API 리소스](/docs/12.x/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [연관 관계](/docs/12.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하세요. 이 메서드는 재귀적으로 호출되어, 모든 속성과 모든 연관 관계(연관 관계의 연관 관계까지 포함)가 배열로 변환됩니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드를 사용하면 모델의 속성만 배열로 변환할 수 있으며, 연관 관계는 변환하지 않습니다:

```php
$user = User::first();

return $user->attributesToArray();
```

또한 모델의 [컬렉션](/docs/12.x/eloquent-collections) 전체를 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로 `toJson` 메서드도 재귀적으로 호출되어 모든 속성과 연관 관계가 JSON으로 변환됩니다. 또한 [PHP가 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스트하면, 자동으로 `toJson` 메서드가 호출됩니다:

```php
return (string) User::find(1);
```

모델과 컬렉션이 문자열로 캐스트될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 Eloquent 모델과 컬렉션을 반환할 경우 자동으로 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관 관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 연관 관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 연관 관계 메서드가 "카멜 케이스(camel case)"로 정의되어 있어도, JSON 속성 이름은 "스네이크 케이스(snake case)"로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

모델의 배열이나 JSON 표현에 포함되는 속성, 예를 들어 비밀번호 같은 것을 제한하고 싶을 때가 있습니다. 이를 위해 모델에 `$hidden` 속성을 추가하세요. `$hidden` 배열에 나열된 속성들은 직렬화된 표현에 포함되지 않습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨겨야 하는 속성들.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 연관 관계를 숨기려면, 해당 연관 관계 메서드 이름을 Eloquent 모델의 `$hidden` 속성에 추가하세요.

또는 `$visible` 속성을 사용해 배열과 JSON 표현에 포함할 "허용 목록(allow list)"을 정의할 수도 있습니다. `$visible` 배열에 포함되지 않은 모든 속성은 배열이나 JSON으로 변환 시 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 표시 시 보이도록 할 속성들.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 표시 여부를 일시적으로 변경하기

일반적으로 숨겨져 있는 특정 속성을 한 모델 인스턴스에서만 보이게 하고 싶다면 `makeVisible` 메서드를 사용하세요. `makeVisible` 메서드는 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();
```

반대로, 일반적으로 보이는 속성 중 일부를 숨기고 싶다면 `makeHidden` 메서드를 사용하세요:

```php
return $user->makeHidden('attribute')->toArray();
```

일시적으로 모든 보이거나 숨길 속성을 한 번에 바꾸고 싶으면 각각 `setVisible`, `setHidden` 메서드를 사용하세요:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

때로는 모델을 배열이나 JSON으로 변환할 때 데이터베이스에 대응하는 컬럼이 없는 속성을 추가하고 싶을 때가 있습니다. 이때는 먼저 해당 값을 위한 [액세서(accessor)](/docs/12.x/eloquent-mutators)를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자인지 여부 결정.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 액세서 속성을 항상 모델의 배열과 JSON 표현에 포함하고 싶으면, 모델의 `appends` 속성에 속성 이름을 추가하세요. 여기서 속성 이름은 일반적으로 액세서의 PHP 메서드는 "카멜 케이스"로 정의되어도, 배열과 JSON에서는 "스네이크 케이스" 형태로 표기합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 배열 표현에 항상 추가할 액세서 목록.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends`에 등록된 속성은 배열과 JSON 표현 모두에 포함되며, `visible`과 `hidden` 설정도 적용됩니다.

<a name="appending-at-run-time"></a>
#### 실행 중에 속성 추가하기

런타임에 모델 인스턴스에 추가 속성을 포함시키려면 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 써서 해당 모델 인스턴스에 추가할 모든 속성 배열을 변경할 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 커스터마이징

`serializeDate` 메서드를 재정의하여 기본 직렬화 날짜 형식을 변경할 수 있습니다. 이 메서드는 데이터베이스 저장 시 날짜 형식에는 영향을 주지 않습니다:

```php
/**
 * 배열 / JSON 직렬화를 위한 날짜 준비.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 형식 커스터마이징

각각의 Eloquent 날짜 속성에 대해 직렬화 포맷을 모델의 [캐스트 선언](/docs/12.x/eloquent-mutators#attribute-casting)에서 지정할 수 있습니다:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```