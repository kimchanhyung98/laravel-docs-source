# Eloquent: 직렬화

- [소개](#introduction)
- [모델과 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel로 API를 개발할 때에는 모델과 관계를 배열 또는 JSON으로 변환해야 할 일이 많습니다. Eloquent는 이러한 변환을 간편하게 처리할 수 있는 메서드를 제공하며, 또한 모델 직렬화 시 어떤 속성이 포함될지 제어할 수 있는 방법도 제공합니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더 강력하게 처리하는 방법은 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하세요. 이 메서드는 재귀적으로 동작하여 모든 속성과 모든 관계(그리고 관계의 관계까지)도 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드를 사용하면 모델의 속성만 배열로 변환하며, 관계는 포함되지 않습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

[컬렉션](/docs/{{version}}/eloquent-collections) 전체도 컬렉션 인스턴스의 `toArray`를 호출하여 배열로 변환할 수 있습니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`와 마찬가지로 `toJson`도 재귀적으로 동작하여 모든 속성과 관계도 함께 JSON으로 변환됩니다. 또한 [PHP에서 지원하는 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)도 지정할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또한, 모델이나 컬렉션을 문자열로 캐스팅하면 `toJson` 메서드가 자동으로 호출됩니다.

```php
return (string) User::find(1);
```

모델이나 컬렉션을 문자열로 캐스팅하면 JSON으로 변환되므로, 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환되면, 로드된 관계들도 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, Eloquent 관계 메서드는 "카멜 케이스(camel case)"로 정의되지만, 관계의 JSON 속성은 "스네이크 케이스(snake case)"로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때로는 암호와 같이 모델의 배열 또는 JSON 표현에 포함시키지 않고 싶은 속성이 있을 수 있습니다. 이럴 경우 모델에 `$hidden` 속성을 추가하세요. `$hidden` 배열에 지정된 속성은 직렬화된 모델에서 제외됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨길 속성.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 관계를 숨기려면, 관계의 메서드 이름을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

반대로, `$visible` 속성을 사용하여 모델 배열 및 JSON 표현에 포함할 "허용 목록"을 정의할 수도 있습니다. `$visible` 배열에 없는 모든 속성은 배열 또는 JSON으로 변환 시 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 보이도록 할 속성.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 노출/숨김 임시 변경

일반적으로 숨기는 속성을 특정 모델 인스턴스에서만 보이도록 하려면 `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();
```

마찬가지로, 일반적으로 보이는 속성을 일시적으로 숨기려면 `makeHidden` 메서드를 사용하면 됩니다.

```php
return $user->makeHidden('attribute')->toArray();
```

모든 보이는 속성이나 숨겨진 속성을 일시적으로 완전히 덮어쓰고자 한다면 각각 `setVisible`, `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에 없는 속성을 추가하길 원할 때가 있습니다. 이럴 경우 먼저 해당 값을 위한 [접근자](/docs/{{version}}/eloquent-mutators)를 정의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자 여부 판단.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

접근자를 모델의 배열 및 JSON 표현에 항상 포함시키고 싶다면 모델의 `appends` 속성에 속성 이름을 추가하면 됩니다. 접근자의 PHP 메서드는 "카멜 케이스"지만, 속성 이름은 "스네이크 케이스"로 지정하는 것이 일반적입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 배열 형태로 추가할 접근자.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

속성이 `appends` 목록에 추가되면, 모델의 배열 및 JSON 표현 모두에 포함됩니다. `appends`에 추가된 속성은 모델의 `visible` 및 `hidden` 설정도 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임 중 값 추가

런타임에 모델 인스턴스에 추가 속성을 동적으로 append하고 싶다면 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends`로 전체 추가 속성 배열을 덮어쓸 수 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 포맷을 바꾸려면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장할 때의 포맷에는 영향을 주지 않습니다.

```php
/**
 * 배열/JSON 직렬화용 날짜 준비.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

각각의 Eloquent 날짜 속성별로 직렬화 포맷을 지정하려면 모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 포맷을 설정하세요.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```