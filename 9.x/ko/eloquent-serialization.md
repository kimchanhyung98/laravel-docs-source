# Eloquent: 직렬화

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
    - [배열로 직렬화하기](#serializing-to-arrays)
    - [JSON으로 직렬화하기](#serializing-to-json)
- [JSON에서 속성 숨기기](#hiding-attributes-from-json)
- [JSON에 값 추가하기](#appending-values-to-json)
- [날짜 직렬화](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel로 API를 구축할 때, 모델과 관계를 배열이나 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 위한 편리한 메서드를 제공할 뿐만 아니라, 모델 직렬화 시 어떤 속성이 포함될지 제어할 수 있는 기능도 제공합니다.

> **참고**  
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더욱 강력하게 처리하려면 [Eloquent API 리소스](/docs/{{version}}/eloquent-resources) 문서를 참고하세요.

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화하기

모델과 로드된 [관계](/docs/{{version}}/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 관계(관계의 관계까지 포함)도 배열로 변환됩니다.

    use App\Models\User;

    $user = User::with('roles')->first();

    return $user->toArray();

`attributesToArray` 메서드를 사용하면 모델의 속성만 배열로 변환할 수 있으며, 관계는 포함되지 않습니다.

    $user = User::first();

    return $user->attributesToArray();

또한, 모델의 전체 [컬렉션](/docs/{{version}}/eloquent-collections)을 배열로 변환하려면 컬렉션 인스턴스에서 `toArray`를 호출하면 됩니다.

    $users = User::all();

    return $users->toArray();

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하세요. `toArray`와 마찬가지로, `toJson`도 재귀적으로 동작하므로 모든 속성과 관계가 JSON으로 변환됩니다. 또한 PHP에서 [지원하는 JSON 인코딩 옵션](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다.

    use App\Models\User;

    $user = User::find(1);

    return $user->toJson();

    return $user->toJson(JSON_PRETTY_PRINT);

또는, 모델이나 컬렉션을 문자열로 형변환(cast)하면 `toJson` 메서드가 자동으로 호출됩니다.

    return (string) User::find(1);

모델과 컬렉션은 문자열로 변환할 때 JSON으로 직렬화되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. 라라벨은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

    Route::get('users', function () {
        return User::all();
    });

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 관계 메서드는 "카멜 케이스"로 정의되지만, 관계의 JSON 속성명은 "스네이크 케이스"로 제공됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때로는 패스워드 같은 특정 속성이 모델의 배열 또는 JSON 표현에 포함되지 않게 하고 싶을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하세요. `$hidden` 속성에 지정된 속성들은 모델이 직렬화될 때 포함되지 않습니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 배열로 표시할 때 숨길 속성들
         *
         * @var array
         */
        protected $hidden = ['password'];
    }

> **참고**  
> 관계를 숨기려면, $hidden 속성 배열에 관계 메서드 이름을 추가하세요.

반대로 모델 배열이나 JSON에 포함할 속성의 "허용 목록"을 지정하고 싶다면 `$visible` 속성을 사용할 수 있습니다. `$visible` 배열에 없는 속성들은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 배열로 표시할 때 노출할 속성들
         *
         * @var array
         */
        protected $visible = ['first_name', 'last_name'];
    }

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 임시 변경

일반적으로 숨겨진 속성을 특정 모델 인스턴스에서만 노출하고 싶을 때는 `makeVisible` 메서드를 사용할 수 있습니다. 이 메서드는 모델 인스턴스를 반환합니다.

    return $user->makeVisible('attribute')->toArray();

반대로, 보통은 보이는 속성을 일시적으로 숨기고 싶을 때는 `makeHidden` 메서드를 사용할 수 있습니다.

    return $user->makeHidden('attribute')->toArray();

모든 visible 또는 hidden 속성을 임시로 덮어쓰려면, 각각 `setVisible` 및 `setHidden` 메서드를 사용하세요.

    return $user->setVisible(['id', 'name'])->toArray();

    return $user->setHidden(['email', 'password', 'remember_token'])->toArray();

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

모델을 배열이나 JSON으로 변환할 때, DB에 컬럼으로 존재하지 않는 속성을 추가하고 싶을 때가 있습니다. 이럴 때는 먼저 해당 값에 대한 [접근자](/docs/{{version}}/eloquent-mutators)를 정의하세요.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\Attribute;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 사용자가 관리자 여부를 결정
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

접근자를 생성한 후에는 모델의 `appends` 속성에 해당 속성명을 추가하면 됩니다. 접근자의 PHP 메서드는 보통 "카멜 케이스"로 정의되지만, 속성명은 "스네이크 케이스"로 참조한다는 점에 주의하세요.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 모델 배열 형태에 추가할 접근자들
         *
         * @var array
         */
        protected $appends = ['is_admin'];
    }

속성명이 `appends` 목록에 추가되면, 해당 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. 또한 `appends` 배열의 속성도 모델의 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
#### 런타임에 값 추가하기

런타임에 모델 인스턴스가 추가 속성을 포함하도록 하려면 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드로 지정된 모델 인스턴스의 전체 추가 속성 배열을 덮어쓸 수 있습니다.

    return $user->append('is_admin')->toArray();

    return $user->setAppends(['is_admin'])->toArray();

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 포맷 커스터마이징

기본 날짜 직렬화 포맷을 커스터마이징하려면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 DB에 날짜를 저장하는 형식에는 영향을 주지 않습니다.

    /**
     * 배열/JSON 직렬화용 날짜 포맷 준비
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d');
    }

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 포맷 커스터마이징

각 Eloquent 날짜 속성별로 직렬화 포맷을 다르게 지정하고 싶다면, 모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에 날짜 포맷을 지정하세요.

    protected $casts = [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];