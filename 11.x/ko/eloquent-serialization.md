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

Laravel로 API를 개발할 때, 종종 모델과 관계를 배열이나 JSON으로 변환해야 할 필요가 있습니다. Eloquent는 이러한 변환을 간편하게 해주는 메서드와 함께, 직렬화된 모델 표현에 포함할 속성을 제어할 수 있는 방법도 제공합니다.

> [!NOTE]  
> Eloquent 모델 및 컬렉션의 JSON 직렬화를 보다 견고하게 처리하려면 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화

모델과 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하여, 모든 속성과 모든 관계(관계의 관계까지 포함)까지 배열로 변환됩니다:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드는 관계를 제외하고 모델의 속성만 배열로 변환할 때 사용할 수 있습니다:

```php
$user = User::first();

return $user->attributesToArray();
```

전체 [컬렉션](/docs/{{version}}/eloquent-collections)의 모델을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`와 마찬가지로, `toJson` 메서드도 재귀적으로 모든 속성과 관계를 JSON으로 직렬화합니다. 또한, [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는, 모델이나 컬렉션을 문자열로 캐스팅하면 내부적으로 `toJson` 메서드가 자동 호출됩니다:

```php
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 자동으로 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환되는 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한, Eloquent 관계 메서드는 카멜케이스로 정의되어 있지만, 관계의 JSON 속성은 스네이크케이스로 표현됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때때로 비밀번호와 같이 모델의 배열 또는 JSON 표현에서 특정 속성을 제외하고 싶을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 명시된 속성은 모델 직렬화 결과에 포함되지 않습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨겨야 할 속성
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]  
> 관계를 숨기려면 관계의 메서드명을 `$hidden` 속성에 추가하세요.

반대로, 모델의 배열 및 JSON 표현에서 포함할 속성을 "허용 목록"으로 지정하고 싶을 때는 `visible` 속성을 사용할 수 있습니다. `$visible` 배열에 없는 속성은 모델을 배열 또는 JSON으로 변환할 때 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에서 보여질 속성
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

평소에 숨겨져 있던 속성을 특정 모델 인스턴스에서만 임시로 보이게 하고 싶다면, `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();
```

반대로, 기본적으로 보이는 속성을 임시로 숨기고자 한다면 `makeHidden` 메서드를 사용하세요.

```php
return $user->makeHidden('attribute')->toArray();
```

모든 visible 또는 hidden 속성을 임시로 오버라이드하려면 `setVisible` 및 `setHidden` 메서드를 각각 사용할 수 있습니다:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에 직접 대응하지 않는 임의의 속성을 추가하고 싶을 수도 있습니다. 이 경우 먼저 해당 값을 위한 [Accessor](/docs/{{version}}/eloquent-mutators)를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자인지 여부를 결정합니다.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 Accessor가 모델의 배열 및 JSON 표현에 항상 추가되게 하려면, 모델의 `appends` 속성에 속성 이름을 추가하세요. Accessor의 PHP 메서드명이 카멜케이스여도, 속성 이름은 주로 "스네이크케이스"로 참조합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 형태로 변환 시 추가할 Accessor
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

속성이 `appends` 리스트에 추가되면, 이 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. 또한 `appends` 배열에 포함된 속성도 모델에 설정된 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 추가하기

실행 중에 특정 모델 인스턴스에 추가 속성을 동적으로 추가하려면 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 사용해 추가된 속성 배열 전체를 덮어쓸 수도 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 포맷을 커스터마이징하려면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 날짜가 저장되는 방식에는 영향을 미치지 않습니다:

```php
/**
 * 배열/JSON 직렬화를 위한 날짜 준비
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

개별 Eloquent 날짜 속성의 직렬화 포맷을 지정하려면, 모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에 날짜 포맷을 지정하세요:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```