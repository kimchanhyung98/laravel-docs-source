# Eloquent: 직렬화 (Serialization)

- [소개](#introduction)
- [모델과 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel로 API를 구축할 때 모델과 연관관계를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 편리하게 처리하는 메서드들을 제공하며, 모델의 직렬화 형태에 포함될 속성을 제어할 수 있습니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 보다 견고하게 처리하는 방법은 [Eloquent API 리소스](/docs/master/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [연관관계](/docs/master/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하세요. 이 메서드는 재귀적으로 작동하여 모든 속성과 관계(관계 안의 관계도 포함)를 배열로 변환합니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 관계는 제외하려면 `attributesToArray` 메서드를 사용하세요:

```php
$user = User::first();

return $user->attributesToArray();
```

또한 전체 모델 [컬렉션](/docs/master/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로 `toJson`도 재귀적으로 작동하여 모든 속성과 관계를 JSON으로 변환합니다. PHP에서 [지원하는 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson` 메서드를 호출합니다:

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 JSON으로 변환되므로, Laravel 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. 이때 Laravel이 자동으로 Eloquent 모델과 컬렉션을 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계는 JSON 객체의 속성으로 자동 포함됩니다. 또, Eloquent의 관계 메서드는 "camel case"로 정의되어 있지만, 관계의 JSON 속성 이름은 "snake case"로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

모델의 배열 또는 JSON 표현에 포함될 속성을 제한하고 싶을 때(예: 비밀번호) `$hidden` 속성을 모델에 추가하세요. 이 속성에 나열된 항목은 직렬화 시 제외됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화할 때 숨겨야 하는 속성들.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 관계를 숨기고 싶다면, 관계 메서드 이름을 `$hidden` 속성에 추가하세요.

또는 `$visible` 속성을 사용해 포함할 속성만 명시하는 "허용 목록"을 정의할 수도 있습니다. 이 배열에 없는 속성은 직렬화 시 모두 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에 표시할 속성들.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

평소에는 숨겨진 속성을 특정 모델 인스턴스에서 보이도록 하려면 `makeVisible` 메서드를 사용하세요. 이 메서드는 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();
```

반대로 평소에 보이는 속성을 숨기려면 `makeHidden` 메서드를 사용하세요:

```php
return $user->makeHidden('attribute')->toArray();
```

가시성 설정 전체를 임시로 덮어쓰려면 각각 `setVisible`과 `setHidden` 메서드를 사용하세요:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때 데이터베이스 열에는 없지만 추가하고 싶은 속성을 넣고 싶다면, 먼저 해당 값을 위한 [액세서](/docs/master/eloquent-mutators)를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자 여부인지 판단.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 액세서를 배열과 JSON 표현에 항상 포함시키려면, 모델의 `appends` 속성에 해당 속성명을 추가하세요. 속성명은 PHP 메서드는 camel case이지만, 직렬화 시에는 보통 snake case로 표기합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 배열 표현에 추가할 액세서 목록.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends` 배열에 속성이 추가되면, 해당 속성은 모델의 배열과 JSON 표현 모두에 포함됩니다. 또한 `visible` 및 `hidden` 설정도 함께 적용됩니다.

<a name="appending-at-run-time"></a>
#### 실행 시점에 추가하기

실행 중에 특정 모델 인스턴스에 속성을 추가하려면 `append` 메서드를 사용하세요. 또는 `setAppends` 메서드로 추가할 속성 전체 배열을 덮어쓸 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 사용자 지정

기본 직렬화 포맷을 변경하고 싶으면 `serializeDate` 메서드를 오버라이드하세요. 이 메서드는 데이터베이스 저장 시 날짜 형식에 영향을 주지 않습니다:

```php
/**
 * 배열 또는 JSON 직렬화를 위해 날짜를 준비합니다.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 형식 사용자 지정

모델의 [캐스트 선언](/docs/master/eloquent-mutators#attribute-casting)에서 각 Eloquent 날짜 속성의 직렬화 포맷을 지정할 수 있습니다:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```