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

Laravel로 API를 개발할 때 모델과 관계를 배열이나 JSON으로 변환해야 할 때가 많습니다. Eloquent는 이러한 변환을 편리하게 처리할 수 있는 메서드를 제공하며, 직렬화된 모델 표현에 포함될 속성을 제어할 수 있게 해줍니다.

> [!NOTE]
> Eloquent 모델 및 컬렉션의 JSON 직렬화를 더욱 강력하게 다루고 싶다면 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화

모델과 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 관계(관계의 관계까지도)도 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 모델 속성만 배열로 변환하며 관계는 변환하지 않습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

또한, [컬렉션](/docs/{{version}}/eloquent-collections) 전체도 컬렉션 인스턴스에서 `toArray`를 호출하여 배열로 변환할 수 있습니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`처럼, `toJson`도 재귀적으로 동작하여 모든 속성과 관계가 JSON으로 변환됩니다. 또한, [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션도 지정할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는, 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson`이 호출됩니다.

```php
return (string) User::find(1);
```

모델과 컬렉션을 문자열로 캐스팅하면 JSON으로 변환되기 때문에, 라우트나 컨트롤러에서 Eloquent 객체를 바로 반환해도 됩니다. 라라벨은 라우트 또는 컨트롤러에서 반환될 때 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환되면, 로드된 관계도 자동으로 JSON 객체의 속성으로 포함됩니다. 또한 Eloquent 관계 메서드는 "카멜 케이스"로 정의되지만, 해당 관계의 JSON 속성명은 "스네이크 케이스"로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때로는 비밀번호와 같이 모델의 배열 또는 JSON 표현에서 제외하고 싶은 속성이 있을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하세요. `$hidden` 배열에 지정된 속성은 직렬화된 모델 표현에 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨길 속성들
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 관계를 숨기려면, 관계의 메서드명을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

반대로, 모델의 배열 및 JSON 표현에 반드시 포함할 허용 목록을 정의하려면 `visible` 속성을 사용할 수 있습니다. `$visible` 배열에 없는 속성은 배열 또는 JSON으로 변환할 때 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 표시할 속성들
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

일반적으로 숨겨진 속성을 특정 모델 인스턴스에서만 보이게 하려면 `makeVisible` 메서드를 사용하세요. `makeVisible`은 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();
```

반대로, 일반적으로 표시되는 속성을 숨기려면 `makeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();
```

모든 표시 또는 숨김 속성 설정을 임시로 덮어쓰고 싶다면 각각 `setVisible`, `setHidden` 메서드를 사용하세요.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼이 없는 속성도 추가하고 싶을 수 있습니다. 이를 위해 우선 해당 값에 대한 [접근자](/docs/{{version}}/eloquent-mutators)를 정의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자 여부 판단
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

접근자가 항상 배열 및 JSON 표현에 추가되길 원한다면 모델의 `appends` 속성에 속성명을 추가하면 됩니다. 참고로 접근자 메서드는 "카멜 케이스"로 정의되지만, 속성명은 직렬화 시 "스네이크 케이스"로 참조됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 형태로 변환 시 추가할 접근자 목록
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

속성을 `appends` 목록에 추가하면 모델의 배열, JSON 표현에 모두 포함됩니다. 또한 `appends` 배열 내 속성 역시 모델에 설정된 `visible` 및 `hidden` 값의 영향을 받습니다.

<a name="appending-at-run-time"></a>
#### 런타임에 추가하기

런타임에 모델 인스턴스에 속성을 동적으로 추가하려면 `append` 메서드를 사용하세요. 또는, `setAppends` 메서드로 런타임에 추가 속성 배열 자체를 재정의할 수 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이즈

기본 직렬화 형식을 바꾸려면 `serializeDate` 메서드를 오버라이드 하면 됩니다. 이 메서드는 데이터베이스에 날짜가 저장될 때의 형식에는 영향을 미치지 않습니다.

```php
/**
 * 배열/JSON 직렬화를 위한 날짜 포맷 준비
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 개별 속성별 날짜 포맷 커스터마이즈

개별 Eloquent 날짜 속성의 직렬화 형식을 지정하려면, 모델의 [형변환 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정하세요.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```