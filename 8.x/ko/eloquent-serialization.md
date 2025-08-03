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

Laravel로 API를 만들 때, 모델과 연관된 관계들을 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 쉽고 편리하게 할 수 있는 메서드들을 제공하며, 직렬화된 모델 표현에 포함할 속성을 제어할 수 있는 방법도 포함하고 있습니다.

> [!TIP]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더 견고하게 처리하는 방법에 대해서는 [Eloquent API resources](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 그에 로드된 [관계](https://laravel.com/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 작동하여 모든 속성과 모든 관계(관계 안의 관계까지)를 배열로 변환합니다:

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

또한 전체 [컬렉션](https://laravel.com/docs/{{version}}/eloquent-collections)에 대해 `toArray` 메서드를 호출하여 배열로 변환할 수 있습니다:

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로 `toJson`도 모든 속성과 관계를 재귀적으로 JSON으로 변환합니다. 또한 PHP에서 지원하는 [JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)도 지정할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

또는 모델이나 컬렉션을 문자열로 타입 캐스팅하면 자동으로 `toJson` 메서드를 호출합니다:

```
return (string) User::find(1);
```

모델과 컬렉션은 문자열로 캐스팅될 때 JSON으로 변환되기 때문에, 애플리케이션의 라우트 혹은 컨트롤러에서 바로 Eloquent 객체를 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환되는 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계들은 JSON 객체 내의 속성으로 자동 포함됩니다. 그리고 Eloquent 관계 메서드는 내부적으로 camelCase 방식으로 정의되지만, JSON 속성명은 snake_case 형식으로 직렬화됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

비밀번호 같은 특정 속성을 모델의 배열 혹은 JSON 표현에서 제외하고 싶을 때가 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하세요. `$hidden` 배열에 포함된 속성들은 직렬화된 모델 표현에 포함되지 않습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열로 변환할 때 숨길 속성들입니다.
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> [!TIP]
> 관계를 숨기고 싶다면, 해당 관계 메서드 이름을 `$hidden` 배열에 추가하세요.

반대로, `$visible` 속성을 사용해 명시적으로 포함할 속성 목록(허용 리스트)을 지정할 수도 있습니다. `$visible` 배열에 포함되지 않은 모든 속성은 배열이나 JSON으로 변환 시 숨겨집니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 변환 시 보여줄 속성 목록입니다.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

일시적으로 숨겨진 속성을 특정 모델 인스턴스에서 보이도록 하려면 `makeVisible` 메서드를 사용하세요. 이 메서드는 수정된 모델 인스턴스를 반환합니다:

```
return $user->makeVisible('attribute')->toArray();
```

반대로, 기본적으로 보이는 속성을 숨기고 싶으면 `makeHidden` 메서드를 사용합니다:

```
return $user->makeHidden('attribute')->toArray();
```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때 DB 컬럼에 없는 속성을 추가하고 싶을 때가 있습니다. 이럴 때는 먼저 그 값을 위한 [액세서(accessor)](https://laravel.com/docs/{{version}}/eloquent-mutators)를 정의하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 관리자(admin)인지 판단합니다.
     *
     * @return bool
     */
    public function getIsAdminAttribute()
    {
        return $this->attributes['admin'] === 'yes';
    }
}
```

액세서를 정의한 후, 모델의 `appends` 속성 배열에 추가할 속성명을 넣습니다. 속성명은 PHP 메서드는 camelCase로 되어있지만 (예: `getIsAdminAttribute`), 직렬화된 이름은 snake_case(예: `is_admin`)를 사용합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 배열 형태 모델에 추가할 액세서 속성들입니다.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

`appends` 목록에 추가된 속성은 모델 배열 및 JSON 표현에 포함되며, `visible`과 `hidden` 설정도 함께 적용됩니다.

<a name="appending-at-run-time"></a>
#### 실행 중에 값 추가하기

실행 중 모델 인스턴스에 추가 속성을 붙이려면 `append` 메서드를 사용하세요. 또는 `setAppends` 메서드로 현재 인스턴스의 `appends` 속성을 완전히 덮어쓸 수도 있습니다:

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 커스터마이징

기본 날짜 직렬화 형식을 바꾸고 싶으면 `serializeDate` 메서드를 오버라이드하세요. 이 메서드는 데이터베이스에 저장되는 날짜 형식에는 영향을 끼치지 않습니다:

```
/**
 * 배열/JSON 직렬화를 위한 날짜 준비 메서드입니다.
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
#### 속성별 날짜 형식 커스터마이징

모델의 개별 날짜 속성에 대해 직렬화 형식을 다르게 지정하려면, 모델의 [캐스트 선언](https://laravel.com/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 형식을 지정하세요:

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```