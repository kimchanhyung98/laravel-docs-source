# 일러퀀트: 직렬화 (Eloquent: Serialization)

- [소개](#introduction)
- [모델과 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화](#serializing-to-arrays)
    - [JSON으로 직렬화](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel로 API를 구축할 때, 자주 모델과 그 연관관계(relationships)를 배열이나 JSON으로 변환해야 합니다. 일러퀀트(Eloquent)는 이러한 변환을 손쉽게 할 수 있는 다양한 메서드를 제공하며, 모델 직렬화 시 포함할 속성을 제어할 수 있는 방법도 지원합니다.

> [!NOTE]
> 일러퀀트 모델과 컬렉션의 JSON 직렬화를 보다 강력하게 다루고 싶다면 [일러퀀트 API 리소스](/docs/master/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화 (Serializing Models and Collections)

<a name="serializing-to-arrays"></a>
### 배열로 직렬화 (Serializing to Arrays)

모델과 그에 로드된 [연관관계](/docs/master/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용합니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 연관관계(하위 연관관계까지 포함)가 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 연관관계는 포함하지 않으려면 `attributesToArray` 메서드를 사용할 수 있습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

또한, 모델의 전체 [컬렉션](/docs/master/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화 (Serializing to JSON)

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로 `toJson`도 재귀적으로 동작하여, 모든 속성과 연관관계가 JSON으로 변환됩니다. 또한, [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다.

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

모델과 컬렉션은 문자열로 변환될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 일러퀀트 객체를 직접 반환할 수 있습니다. 라라벨은 컨트롤러나 라우트에서 반환되는 일러퀀트 모델과 컬렉션을 자동으로 JSON으로 직렬화해 반환합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

일러퀀트 모델을 JSON으로 변환할 때, 로드된 연관관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, 일러퀀트의 연관관계 메서드는 "카멜 케이스(camel case)"로 정의되지만, JSON의 속성에서는 "스네이크 케이스(snake case)"로 변환되어 노출됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기 (Hiding Attributes From JSON)

때로는 비밀번호와 같이 배열 또는 JSON 표현에 포함하고 싶지 않은 속성이 있을 수 있습니다. 이런 경우, 모델에 `$hidden` 속성을 추가합니다. `$hidden` 배열에 명시된 속성들은 직렬화 과정에서 결과에 포함되지 않습니다.

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
> 연관관계를 숨기고 싶다면, 해당 연관관계의 메서드명을 모델의 `$hidden` 속성에 추가하면 됩니다.

반대로, `$visible` 속성을 사용해 배열 또는 JSON 표현에 포함할 속성의 "허용 목록"을 정의할 수도 있습니다. `$visible` 배열에 포함되지 않은 속성들은 직렬화 시 결과에서 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에 표시될 속성들
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 표시 여부를 일시적으로 변경하기

특정 상황에서, 평소에는 숨겨진 속성을 일시적으로 보이도록 하려면 `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 변경된 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

반대로, 평소에 보이는 속성 중 일부를 숨기려면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

모든 visible 또는 hidden 속성을 임시로 재정의하고 싶다면, 각각 `setVisible` 또는 `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가 (Appending Values to JSON)

모델을 배열이나 JSON으로 변환할 때 데이터베이스 컬럼에 없는 속성을 추가하고 싶을 때가 있습니다. 이 경우, 먼저 해당 값을 위한 [접근자(Accessor)](/docs/master/eloquent-mutators)를 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자(administrator)인지 확인합니다.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 접근자를 모델의 배열 또는 JSON 표현에 항상 포함하려면, 모델의 `appends` 속성에 속성명을 추가합니다. 참고로, 접근자의 PHP 메서드는 "카멜 케이스"로 정의하지만, `appends`에 명시할 때는 일반적으로 직렬화된 "스네이크 케이스" 형식을 사용합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 배열 형태에 추가할 접근자 목록
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

이렇게 `appends`에 속성을 추가하면, 해당 속성은 배열 및 JSON 표현 모두에 포함됩니다. `appends` 배열에 포함된 속성도 모델의 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 추가하기

런타임에서 모델 인스턴스에 추가 속성을 덧붙이려면 `append` 또는 `mergeAppends` 메서드를 사용할 수 있습니다. 또는, `setAppends` 메서드를 이용해 해당 인스턴스의 모든 추가 속성 목록을 재정의할 수도 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

반대로, 모델에 추가된 모든 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용할 수 있습니다.

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화 (Date Serialization)

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 날짜 포맷을 변경하려면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다.

```php
/**
 * 날짜를 배열/JSON 직렬화에 맞게 준비합니다.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

특정 일러퀀트 날짜 속성의 직렬화 포맷을 개별적으로 지정하고 싶다면, 모델의 [캐스팅 선언](/docs/master/eloquent-mutators#attribute-casting)을 통해 날짜 포맷을 지정할 수 있습니다.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
