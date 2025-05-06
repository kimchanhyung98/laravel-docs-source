# Eloquent: 직렬화

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화](#serializing-to-arrays)
    - [JSON으로 직렬화](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel로 API를 구축할 때 모델과 관계를 배열이나 JSON으로 변환해야 할 때가 많습니다. Eloquent는 이러한 변환을 편리하게 처리할 수 있는 메서드와, 직렬화된 모델 표현에 어떤 속성이 포함될지를 제어할 수 있는 방법을 제공합니다.

> [!NOTE]  
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더 강력하게 제어하고 싶다면 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화

모델과 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 작동하므로, 모든 속성과 모든 관계(관계의 관계까지 포함)가 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 모델의 속성만 배열로 변환하고, 관계는 포함하지 않습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

[컬렉션](/docs/{{version}}/eloquent-collections) 전체를 배열로 변환할 때는 컬렉션 인스턴스에서 `toArray`를 호출하면 됩니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화

모델을 JSON으로 변환하려면, `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로, `toJson`도 재귀적으로 모든 속성과 관계를 JSON으로 변환합니다. 또한 [PHP가 지원하는 모든 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는, 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson` 메서드가 호출됩니다.

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅할 때 JSON으로 변환되기 때문에, 라우트나 컨트롤러에서 Eloquent 객체를 바로 반환할 수 있습니다. 이 경우 Laravel이 자동으로 모델과 컬렉션을 JSON으로 직렬화합니다.

```php
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계(Relationships)

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, Eloquent 관계 메서드는 “카멜 케이스(camel case)”로 정의되지만, 관계의 JSON 속성명은 “스네이크 케이스(snake case)”로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

비밀번호와 같이 모델의 배열 또는 JSON 표현에서 특정 속성을 제외하고 싶을 때가 있습니다. 이를 위해 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 포함된 속성들은 직렬화된 결과에 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 숨길 속성
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]  
> 관계를 숨기고 싶다면, 관계 메서드의 이름을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

반대로, 모델의 배열과 JSON 표현에서 포함할 속성의 "허용 목록"을 정의하고 싶을 땐, `$visible` 속성을 사용할 수 있습니다. `$visible` 배열에 없는 속성들은 직렬화 시 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 보여줄 속성
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 표시/숨김 임시 변경

특정 모델 인스턴스에서 임시로 숨겨둔 속성을 표시하고 싶으면, `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();
```

반대로 원래는 보이는 속성을 임시로 숨기고 싶다면, `makeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();
```

모든 보임/숨김 속성을 임시로 전환하고자 할 땐 각각 `setVisible`, `setHidden` 메서드를 사용하면 됩니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열 또는 JSON으로 변환할 때, 데이터베이스 컬럼에 대응하지 않는 속성을 추가하고 싶을 때가 있습니다. 이 경우, 우선 [접근자(Accessor)](/docs/{{version}}/eloquent-mutators)를 정의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자(Admin)인지 여부를 반환
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

해당 접근자가 항상 모델의 배열 및 JSON 표현에 포함되도록 하려면, 모델의 `appends` 속성에 속성명을 추가하세요. 참고로, 접근자 PHP 메서드는 보통 “카멜 케이스”로 정의되지만, 직렬화 시엔 일반적으로 “스네이크 케이스”를 사용합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 형태에 추가할 접근자
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

속성을 `appends` 리스트에 추가하면, 모델의 배열 및 JSON 표현에 해당 값이 포함됩니다. `appends` 배열의 속성 역시 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 값 추가

런타임 시, 모델 인스턴스에 추가적인 속성을 `append` 메서드로 추가할 수 있습니다. 또는, `setAppends` 메서드로 추가 속성 배열 자체를 오버라이드할 수도 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 날짜 포맷을 변경하려면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스 저장 포맷에는 영향을 주지 않습니다.

```php
/**
 * 배열 / JSON 직렬화를 위한 날짜 준비
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

각각의 Eloquent 날짜 속성별로 직렬화 포맷을 지정하고 싶다면, 모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정할 수 있습니다.

```php
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```
