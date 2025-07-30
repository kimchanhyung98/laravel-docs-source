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

Laravel을 사용해 API를 구축할 때, 모델과 연관관계를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 손쉽게 처리할 수 있는 메서드와, 모델의 직렬화된 표현에 포함될 속성을 제어하는 기능을 제공합니다.

> [!NOTE]  
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더욱 강력하게 다루고 싶다면 [Eloquent API 리소스](/docs/10.x/eloquent-resources) 문서도 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 그에 로드된 [연관관계](/docs/10.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하세요. 이 메서드는 재귀적으로 동작하므로, 모델의 속성뿐 아니라 모든 연관관계(연관관계의 연관관계 포함)도 배열로 변환합니다:

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 관계는 포함하지 않으려면 `attributesToArray` 메서드를 사용하세요:

```
$user = User::first();

return $user->attributesToArray();
```

컬렉션 전체를 배열로 변환할 때에도 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로 `toJson`도 재귀적으로 모든 속성과 관계를 JSON으로 변환합니다. 또한, PHP에서 [지원하는 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다:

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 캐스팅하면 자동으로 `toJson` 메서드가 호출됩니다:

```
return (string) User::find(1);
```

모델과 컬렉션이 문자열로 캐스팅될 때 JSON으로 변환되므로, 라우트 또는 컨트롤러에서 Eloquent 객체를 직접 반환해도 됩니다. 이 경우 Laravel이 자동으로 JSON으로 직렬화해 반환합니다:

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 연관관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 연관관계 메서드는 일반적으로 카멜 케이스(camel case)로 정의되어 있지만, JSON 속성명은 스네이크 케이스(snake case)로 변환된다는 점을 기억하세요.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

보통 비밀번호 같은 특정 속성을 모델의 배열 또는 JSON 표현에 포함하지 않으려면, 모델에 `$hidden` 속성을 정의하세요. `$hidden` 속성 배열에 명시된 속성은 모델 직렬화 결과에 포함되지 않습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열로 변환 시 숨길 속성들
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]  
> 연관관계를 숨기고 싶으면, 연관관계 메서드명을 Eloquent 모델의 `$hidden` 배열에 추가하세요.

반대로 `$visible` 속성을 통해 모델의 배열 및 JSON 표현에 포함할 "허용 목록"을 정의할 수도 있습니다. `$visible`에 없는 모든 속성은 직렬화 시 숨겨집니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열로 변환 시 포함할 속성들
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경하기

일반적으로 숨겨진 속성을 특정 모델 인스턴스에서 잠시 보이도록 하려면 `makeVisible` 메서드를 사용하세요. 이 메서드는 모델 인스턴스를 반환합니다:

```
return $user->makeVisible('attribute')->toArray();
```

반대로 일반적으로 보이는 속성을 숨기려면 `makeHidden` 메서드를 사용하세요:

```
return $user->makeHidden('attribute')->toArray();
```

모든 가시 속성 또는 숨김 속성을 임시로 완전히 덮어쓰려면 각각 `setVisible` 및 `setHidden` 메서드를 사용하면 됩니다:

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때 데이터베이스에 대응되는 컬럼이 없는 속성을 추가하고 싶으면, 먼저 해당 값에 대한 [엑세서(accessor)](/docs/10.x/eloquent-mutators)를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자 여부를 판단하는 엑세서
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

엑세서를 항상 모델의 배열 및 JSON 표현에 포함하려면, 모델의 `appends` 속성에 해당 속성명을 추가하세요. 속성명은 PHP 메서드는 카멜 케이스지만, 직렬화 시에는 일반적으로 스네이크 케이스로 표기합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 배열 표현에 추가할 엑세서 목록
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends`에 추가한 속성은 배열과 JSON 표현 모두에 포함되며, `visible` 및 `hidden` 설정도 정상적으로 적용됩니다.

<a name="appending-at-run-time"></a>
#### 런타임에 속성 추가하기

런타임 중 특정 모델 인스턴스에 추가 속성을 붙이려면 `append` 메서드를 사용하면 됩니다. 또는 `setAppends` 메서드를 이용해 해당 인스턴스의 전체 추가 속성 배열을 덮어쓸 수도 있습니다:

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 변경하기

기본 날짜 직렬화 형식을 바꾸려면 `serializeDate` 메서드를 오버라이드하세요. 이 메서드는 데이터베이스 저장용 날짜 포맷에는 영향을 미치지 않습니다:

```
/**
 * 배열 / JSON 직렬화를 위한 날짜 준비
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 개별 속성별 날짜 포맷 지정하기

모델의 [캐스트 선언](/docs/10.x/eloquent-mutators#attribute-casting)에서 날짜 속성별로 직렬화 포맷을 다르게 지정할 수도 있습니다:

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```