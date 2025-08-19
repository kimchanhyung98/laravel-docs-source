# Eloquent: 직렬화 (Eloquent: Serialization)

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화](#serializing-to-arrays)
    - [JSON으로 직렬화](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel로 API를 구축할 때는 모델 및 연관관계(relationships)를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 손쉽게 처리할 수 있는 다양한 메서드를 제공하며, 직렬화된 모델 표현에 어떤 속성이 포함될지 제어할 수도 있습니다.

> [!NOTE]
> Eloquent 모델 및 컬렉션을 JSON으로 더 강력하게 직렬화하고 싶다면, [Eloquent API 리소스](/docs/12.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 배열로 직렬화 (Serializing to Arrays)

모델과 로드된 [연관관계](/docs/12.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 연관관계(심지어 연관관계의 연관관계까지)도 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

`attributesToArray` 메서드를 사용하면 연관관계는 제외하고 오직 모델의 속성만 배열로 변환할 수 있습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

또한, [컬렉션](/docs/12.x/eloquent-collections) 전체를 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화 (Serializing to JSON)

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`와 마찬가지로 `toJson`도 재귀적으로 동작하여, 모든 속성과 연관관계가 JSON 형태로 변환됩니다. 또한, PHP에서 [지원하는 모든 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또한, 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson` 메서드가 호출됩니다.

```php
return (string) User::find(1);
```

모델이나 컬렉션이 문자열로 캐스팅될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 그대로 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델 및 컬렉션을 자동으로 JSON으로 직렬화하여 응답합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계도 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, Eloquent 연관관계 메서드는 "카멜 케이스"로 정의되지만, JSON의 속성명은 "스네이크 케이스"로 나타납니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기 (Hiding Attributes From JSON)

때로는 비밀번호와 같이, 모델의 배열이나 JSON 표현에서 특정 속성을 제외하고 싶을 수 있습니다. 이럴 때는 모델에 `$hidden` 프로퍼티를 추가하면 됩니다. `$hidden` 배열에 나열한 속성들은 모델의 직렬화 표현에 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨겨야 할 속성들
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 연관관계를 숨기고 싶을 때는, 연관관계의 메서드 이름을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

또는, `visible` 프로퍼티를 사용하여 오로지 포함하고자 하는 속성만 "허용 리스트(allow list)"로 지정할 수도 있습니다. `$visible` 배열에 없는 속성은 모두 숨겨져서, 배열이나 JSON 변환 시 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에 표시할 속성들
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

일반적으로 숨겨져 있는 속성을 특정 모델 인스턴스에서만 노출하고 싶다면, `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

반대로, 평소에 보이도록 설정된 속성을 임시로 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

모든 visible 혹은 hidden 속성을 일시적으로 완전히 덮어쓰고 싶다면, 각각 `setVisible`, `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기 (Appending Values to JSON)

모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼으로 존재하지 않는 값을 추가하고 싶을 때가 있습니다. 이 경우, 먼저 해당 값에 대한 [accessor](/docs/12.x/eloquent-mutators) 메서드를 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자(Administrator)인지 여부 반환
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 accessor를 항상 모델의 배열 및 JSON 표현에 추가하고 싶다면, 모델의 `appends` 프로퍼티에 해당 속성명을 추가하면 됩니다. 참고로 accessor의 PHP 메서드는 "카멜 케이스"로 정의하지만, `appends`에는 직렬화될 때의 "스네이크 케이스" 속성명을 사용해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 배열 형태에 추가할 accessor 목록
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

이 속성명이 `appends`에 추가되면, 해당 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. 그리고 `appends` 배열에 추가된 속성도 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 추가하기

런타임에서 특정 모델 인스턴스에 속성을 동적으로 추가하고 싶다면, `append` 또는 `mergeAppends` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 이용해 특정 인스턴스의 추가 속성 전체를 덮어쓸 수도 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화 (Date Serialization)

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이즈

기본 직렬화 날짜 포맷을 변경하려면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다.

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
#### 속성별 날짜 포맷 커스터마이즈

특정 Eloquent 날짜 속성만 별도의 직렬화 포맷으로 지정하고 싶다면, 모델의 [cast 선언](/docs/12.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정할 수 있습니다.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
