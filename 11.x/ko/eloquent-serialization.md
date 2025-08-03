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

Laravel을 사용해 API를 구축할 때, 모델과 연관 관계를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 편리하게 할 수 있는 메서드들을 포함하고 있으며, 모델의 직렬화된 표현에 포함될 속성을 제어할 수도 있습니다.

> [!NOTE]  
> Eloquent 모델과 컬렉션의 JSON 직렬화를 보다 강력하게 다루는 방법은 [Eloquent API 리소스](/docs/11.x/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델과 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [관계들](/docs/11.x/eloquent-relationships)을 배열로 변환하려면 `toArray` 메서드를 사용해야 합니다. 이 메서드는 재귀적으로 동작하기 때문에, 모든 속성과 관계(관계의 관계 포함)가 배열로 변환됩니다:

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

모델의 속성만 배열로 변환하고 관계는 제외하려면 `attributesToArray` 메서드를 사용할 수 있습니다:

```
$user = User::first();

return $user->attributesToArray();
```

또한 전체 모델 [컬렉션](/docs/11.x/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다:

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로, `toJson` 메서드는 재귀적으로 모든 속성과 관계를 JSON으로 변환합니다. 또한 PHP에서 지원하는 [JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다:

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

모델과 컬렉션이 문자열로 캐스팅될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수도 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계

Eloquent 모델을 JSON으로 변환할 때, 로드된 관계들은 JSON 객체 내 속성으로 자동 포함됩니다. 또한 Eloquent 관계 메서드명은 보통 "camel case" 형식을 사용하지만, 관계가 JSON 속성으로 표현될 때는 "snake case"로 변환되어 포함됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

모델의 배열 또는 JSON 표현에 포함될 속성을 제한하고 싶을 때가 있습니다. 예를 들어 비밀번호 같은 민감한 정보가 그 대상입니다. 이 경우 모델에 `$hidden` 속성을 추가하세요. `$hidden` 배열에 나열된 속성들은 모델의 직렬화된 표현에 포함되지 않습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 직렬화 시 숨겨야 할 속성들.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]  
> 관계를 숨기려면, 해당 관계 메서드명을 Eloquent 모델의 `$hidden` 배열에 추가하세요.

또한, `visible` 속성을 사용하여 배열 또는 JSON 표현에 포함할 속성의 "허용 목록"을 정의할 수도 있습니다. `$visible` 배열에 포함되지 않은 모든 속성은 모델을 배열이나 JSON으로 변환할 때 자동으로 숨겨집니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열에 노출될 속성들.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 임시로 속성 노출 범위 변경하기

일부 기본적으로 숨겨진 속성을 특정 모델 인스턴스에서 보여주고 싶다면, `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다:

```
return $user->makeVisible('attribute')->toArray();
```

반대로, 기본적으로 보이는 속성을 숨기고 싶다면 `makeHidden` 메서드를 사용하면 됩니다:

```
return $user->makeHidden('attribute')->toArray();
```

또한 전체 `visible` 또는 `hidden` 속성 배열을 임시로 바꾸려면 `setVisible`과 `setHidden` 메서드를 각각 사용할 수 있습니다:

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

가끔 모델을 배열이나 JSON으로 변환할 때 데이터베이스 테이블에는 없는 속성을 추가하고 싶을 수 있습니다. 이럴 때는 우선 해당 값에 대한 [액세서(accessor)](/docs/11.x/eloquent-mutators)를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자인지 여부 판별 액세서.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

이 액세서를 모델의 배열 및 JSON 표현에 항상 추가하려면, 모델의 `appends` 속성 배열에 해당 액세서 이름을 포함시키면 됩니다. 액세서 이름은 PHP 메서드명은 보통 camel case를 따르지만, `appends` 배열에 추가할 때는 snake case 형식을 따르는 점을 유의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 배열에 자동 추가할 액세서 속성들.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends`에 추가된 속성들은 모델의 배열 및 JSON 표현에 포함되며, 동시에 모델의 `visible` 및 `hidden` 설정도 그대로 적용됩니다.

<a name="appending-at-run-time"></a>
#### 실행 시 값 추가하기

실행 중에 특정 모델 인스턴스에 추가 속성을 더하고 싶을 때는 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 사용해 추가할 전체 속성 배열을 한 번에 덮어쓸 수도 있습니다:

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 사용자 정의

기본 직렬화 날짜 형식을 바꾸고 싶다면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스 저장 시 포맷에는 영향을 주지 않습니다:

```
/**
 * 배열 또는 JSON 직렬화를 위한 날짜 준비.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 형식 사용자 정의

각각 Eloquent 날짜 속성의 직렬화 형식을 커스터마이징하려면, 모델의 [캐스트 선언](/docs/11.x/eloquent-mutators#attribute-casting)에서 날짜 형식을 지정할 수 있습니다:

```
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
