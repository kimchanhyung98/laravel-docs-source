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

Laravel로 API를 구축할 때 모델과 연관관계를 배열이나 JSON으로 변환해야 하는 경우가 자주 발생합니다. Eloquent는 이러한 변환을 손쉽게 처리할 수 있게 해주는 편리한 메서드를 제공하며, 모델의 직렬화된 표현에 포함할 속성을 제어하는 기능도 포함하고 있습니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 보다 강력하게 다루고 싶다면 [Eloquent API 리소스](/docs/9.x/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [연관관계](/docs/9.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용해야 합니다. 이 메서드는 재귀적이어서 모든 속성과 관계(관계 내 관계 포함)가 배열로 변환됩니다:

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 관계는 포함하지 않으려면 `attributesToArray` 메서드를 사용할 수 있습니다:

```
$user = User::first();

return $user->attributesToArray();
```

또한 전체 [컬렉션](/docs/9.x/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로 `toJson`도 재귀적이어서 모든 속성 및 관계가 JSON으로 변환됩니다. PHP에서 지원하는 [JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다:

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스팅하면 내부적으로 `toJson` 메서드가 자동으로 호출됩니다:

```
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 JSON으로 변환되기 때문에, 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON 직렬화합니다:

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

Eloquent 모델을 JSON으로 변환할 때, 로드된 관계는 자동으로 JSON 객체의 속성에 포함됩니다. 또한, Eloquent 관계 메서드는 "camel case"로 정의되지만, JSON에서의 관계 속성 이름은 "snake case" 형식을 따릅니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

비밀번호 같은 특정 속성을 모델의 배열 또는 JSON 표현에 포함시키고 싶지 않은 경우가 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 나열된 속성들은 직렬화된 모델 표현에 포함되지 않습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 변환 시 숨길 속성들입니다.
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 관계를 숨기려면 해당 관계 메서드명을 Eloquent 모델의 `$hidden` 배열에 추가하세요.

반대로, `$visible` 속성을 사용하여 배열과 JSON 표현에 포함할 "허용 목록"을 정의할 수도 있습니다. `$visible`에 포함되지 않은 속성들은 배열 또는 JSON으로 변환할 때 숨겨집니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 변환 시 보일 속성들입니다.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 일시적으로 속성 표시 상태 변경하기

평소에 숨겨진 속성을 특정 모델 인스턴스에서 일시적으로 보이게 하려면 `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다:

```
return $user->makeVisible('attribute')->toArray();
```

반대로, 평소에 보이는 속성을 숨기려면 `makeHidden` 메서드를 사용하세요:

```
return $user->makeHidden('attribute')->toArray();
```

모델 인스턴스에서 보이거나 숨겨질 속성 전체를 일시적으로 변경하려면 각각 `setVisible`과 `setHidden` 메서드를 사용할 수 있습니다:

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

가끔 모델을 배열이나 JSON으로 변환할 때 데이터베이스에 실제 컬럼이 없는 속성을 추가하고 싶을 수 있습니다. 이럴 때는 먼저 해당 값을 위한 [액세서(accessor)](/docs/9.x/eloquent-mutators)를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자 여부인지 판단합니다.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

액세서를 만든 뒤, 모델의 `appends` 속성에 속성 이름을 추가하세요. 액세서 PHP 메서드는 "camel case"로 정의되어 있지만, 속성 이름은 보통 "snake case" 형식을 사용합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 배열 변환 시 추가할 액세서 속성들입니다.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends` 목록에 속성이 추가되면 모델의 배열과 JSON 표현 모두에 포함됩니다. 이때 `appends`에 포함된 속성들도 모델에 설정된 `visible` 및 `hidden` 규칙을 따릅니다.

<a name="appending-at-run-time"></a>
#### 실행 중에 추가하기

실행 중에 모델 인스턴스에 추가 속성을 붙이고 싶으면 `append` 메서드를 사용하세요. 또는 `setAppends` 메서드를 사용해 그 인스턴스에 붙일 속성 배열을 전체 교체할 수도 있습니다:

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 직렬화 날짜 형식을 커스터마이징하려면 `serializeDate` 메서드를 재정의하세요. 이 메서드는 데이터베이스에 저장할 때의 날짜 포맷에는 영향을 미치지 않습니다:

```
/**
 * 배열 또는 JSON 직렬화를 위한 날짜 준비 메서드입니다.
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

특정 Eloquent 날짜 속성의 직렬화 포맷을 커스터마이징하려면 모델의 [캐스트 선언](/docs/9.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 명시하세요:

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```