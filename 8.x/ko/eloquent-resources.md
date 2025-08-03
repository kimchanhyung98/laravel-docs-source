# Eloquent: API 리소스 (Eloquent: API Resources)

- [소개](#introduction)
- [리소스 생성하기](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성하기](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이징 처리](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 연관관계](#conditional-relationships)
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 애플리케이션 사용자가 실제로 받게 되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자에게만 특정 속성을 보여주거나, JSON 표현에 항상 특정 연관 관계를 포함하고 싶을 때가 그렇습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 표현력 있게 쉽게 JSON으로 변환할 수 있게 해줍니다.

물론 Eloquent 모델이나 컬렉션을 `toJson` 메서드로 직접 JSON 변환할 수 있지만, Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화를 더 세밀하고 강력하게 제어할 수 있도록 도와줍니다.

<a name="generating-resources"></a>
## 리소스 생성하기

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다:

```
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 생성 외에도, 모델 컬렉션을 변환하는 리소스를 생성할 수 있습니다. 이를 통해 JSON 응답에 링크나 컬렉션 전체에 관련된 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면 리소스 생성 시 `--collection` 옵션을 사용하거나, 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel이 컬렉션 리소스로 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다:

```
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!TIP]
> 이 섹션은 리소스와 리소스 컬렉션에 대한 높은 수준의 개요입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 깊이 이해하기 위해 이 문서의 다른 섹션도 꼭 읽어보시길 권장합니다.

리소스를 작성하는 다양한 옵션을 살펴보기 전에, Laravel 내에서 리소스가 어떻게 사용되는지 간단히 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환할 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 클래스입니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 리소스가 라우트나 컨트롤러에서 반환될 때 JSON으로 변환되어야 하는 속성들의 배열을 반환합니다.

모델의 속성은 `$this` 변수에서 직접 접근할 수 있습니다. 이는 리소스 클래스가 내부적으로 속성과 메서드 접근을 해당 모델 인스턴스로 자동으로 위임해주기 때문입니다. 정의된 리소스는 라우트나 컨트롤러에서 반환할 수 있으며, 생성자에 모델 인스턴스를 받습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션이나 페이징된 응답을 반환할 때는, 라우트나 컨트롤러에서 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

그러나 이 경우 컬렉션과 함께 반환해야 하는 커스텀 메타 데이터는 추가할 수 없습니다. 컬렉션 응답을 직접 커스터마이징하려면 별도의 컬렉션 리소스를 생성해야 합니다:

```
php artisan make:resource UserCollection
```

생성된 컬렉션 리소스 클래스에서 원하는 메타 데이터를 쉽게 정의할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```

컬렉션 리소스가 정의되면 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 그러나 리소스 클래스에 `preserveKeys` 속성을 추가해서 원래의 키를 유지할지 선택할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스 컬렉션의 원래 키를 유지할지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 속성을 `true`로 설정하면, 라우트나 컨트롤러에서 컬렉션 반환 시 원래 키가 유지됩니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

보통 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단일 리소스 클래스는 컬렉션 클래스명에서 끝의 `Collection`을 뺀 이름으로 추정하며, 개인 취향에 따라 `Resource` 접미사가 붙을 수도 안 붙을 수도 있습니다.

예를 들어, `UserCollection`은 개별 유저를 `UserResource` 클래스로 매핑합니다. 이 동작을 바꾸고자 하면 리소스 컬렉션 클래스에서 `$collects` 속성을 재정의하면 됩니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스가 수집하는 리소스를 지정합니다.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성하기

> [!TIP]
> 만약 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서의 나머지 부분을 읽기 전에 꼭 먼저 읽어보시길 권장합니다.

본질적으로 리소스는 단순합니다. 주어진 모델을 배열로 변환하는 것만 필요합니다. 그래서 각 리소스는 `toArray` 메서드를 갖고 있으며, 이 메서드는 모델의 속성을 API 친화적인 배열로 변환해 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있게 합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```

정의된 리소스는 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 연관관계 포함하기

응답에 연관된 리소스를 포함하려면, 리소스의 `toArray` 메서드가 반환하는 배열에 추가하면 됩니다. 예를 들어, `PostResource`의 `collection` 메서드를 사용해 사용자의 블로그 게시글을 리소스 응답에 포함할 수 있습니다:

```
use App\Http\Resources\PostResource;

/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->posts),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

> [!TIP]
> 연관관계가 미리 로드되어 있을 때만 포함하고 싶다면, [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성하기

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 리소스 컬렉션 클래스를 별도로 만들 필요까지는 없으며, 모든 리소스는 `collection` 메서드를 제공해 즉석에서 "임시" 리소스 컬렉션을 생성할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

컬렉션에 반환되는 메타 데이터를 커스터마이징해야 한다면, 직접 리소스 컬렉션을 정의해야 합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```

단일 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 리소스의 최상위 JSON 결과는 `data` 키 안에 래핑되어 반환됩니다. 예를 들어 전형적인 리소스 컬렉션 응답은 다음과 같습니다:

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ]
}
```

`data` 대신 다른 키를 사용하고 싶다면 리소스 클래스에 `$wrap` 속성을 정의할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 적용할 "data" 래퍼 이름입니다.
     *
     * @var string
     */
    public static $wrap = 'user';
}
```

최상위 리소스 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 보통 이 메서드는 `AppServiceProvider` 또는 모든 요청에서 로드되는 다른 [서비스 프로바이더](/docs/{{version}}/providers) 내에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!NOTE]
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 주며, 리소스 컬렉션에서 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스 래핑

리소스의 연관 관계를 어떻게 래핑할지는 전적으로 자유입니다. 만약 모든 리소스 컬렉션이 중첩 수준과 상관없이 `data` 키로 래핑되도록 하려면, 각 리소스마다 컬렉션 클래스를 정의하고 `data` 키 안에서 반환하면 됩니다.

두 개의 `data` 키로 이중 래핑될까 걱정하실 수 있지만, Laravel은 리소스를 이중으로 래핑하지 않으므로 걱정하지 않아도 됩니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return ['data' => $this->collection];
    }
}
```

<a name="data-wrapping-and-pagination"></a>
#### 데이터 래핑과 페이징 처리

페이징된 컬렉션을 리소스로 반환할 때는, `withoutWrapping` 메서드를 호출했어도 Laravel은 항상 응답 데이터를 `data` 키로 래핑합니다. 이는 페이징 응답에 `meta` 및 `links` 키가 항상 포함되어 페이저 상태 정보를 담기 때문입니다:

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ],
    "links":{
        "first": "http://example.com/pagination?page=1",
        "last": "http://example.com/pagination?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/pagination",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="pagination"></a>
### 페이징 처리

페이저 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이징된 응답은 페이저 상태에 대한 `meta`와 `links` 키를 항상 포함합니다:

```
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com",
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com",
        }
    ],
    "links":{
        "first": "http://example.com/pagination?page=1",
        "last": "http://example.com/pagination?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/pagination",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="conditional-attributes"></a>
### 조건부 속성

때로는 조건에 따라 리소스 응답에 속성을 포함할지 말지 결정하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 값을 포함하고 싶을 수 있습니다. Laravel은 이를 돕기 위한 여러 헬퍼 메서드를 제공합니다. `when` 메서드는 조건에 따라 속성을 리소스 응답에 추가할 수 있습니다:

```
use Illuminate\Support\Facades\Auth;

/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'secret' => $this->when(Auth::user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예시에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때에만 최종 리소스 응답에 포함되고, 아니라면 클라이언트에 보내기 전에 제거됩니다. `when` 메서드는 조건문을 쓰지 않고도 표현력 있게 리소스를 정의하도록 해줍니다.

또한 `when` 메서드는 두 번째 인수로 클로저도 받아, 조건이 `true`일 때만 계산된 값을 반환하도록 할 수 있습니다:

```
'secret' => $this->when(Auth::user()->isAdmin(), function () {
    return 'secret-value';
}),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합하기

같은 조건에 따라 여러 속성을 한꺼번에 리소스 응답에 포함해야 할 때는 `mergeWhen` 메서드를 사용하면, 조건이 참일 때만 배열 내의 여러 속성이 병합되어 포함됩니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        $this->mergeWhen(Auth::user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

해당 조건이 거짓이면 이 속성들은 클라이언트로 보내기 전에 제거됩니다.

> [!NOTE]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 혼합된 배열 내에서 사용하지 마세요. 또한 순차적이지 않은 숫자 키 배열에도 사용하지 않아야 합니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성 로딩 뿐 아니라, 연관 관계도 모델에 미리 로드되어 있을 때만 조건부로 응답에 포함할 수 있습니다. 이를 통해 컨트롤러가 어떤 관계를 로드할지 결정하고, 리소스는 실제 로드된 관계만 포함해서 "N+1" 쿼리 문제를 방지할 수 있습니다.

`whenLoaded` 메서드는 연관 관계를 조건부로 로드하는데 이용할 수 있으며, 관계 자체 대신 관계 이름을 인자로 받습니다:

```
use App\Http\Resources\PostResource;

/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->whenLoaded('posts')),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예에서는 관계가 로드되어 있지 않으면 `posts` 키가 응답에서 삭제됩니다.

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보 포함하기

관계 정보뿐 아니라, 다대다 관계의 중간 테이블 데이터를 조건부로 포함할 수도 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인자로 중간 테이블 이름을 받으며, 두 번째 인자로 피벗 데이터가 존재할 때 반환할 값을 클로저로 받습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoaded('role_user', function () {
            return $this->pivot->expires_at;
        }),
    ];
}
```

만약 관계가 [커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 쓴다면, 중간 테이블 모델 인스턴스를 첫 인자로 넘길 수도 있습니다:

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블 모델에 기본 `pivot` 대신 다른 접근자를 쓰는 경우에는 `whenPivotLoadedAs` 메서드를 사용합니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {
            return $this->subscription->expires_at;
        }),
    ];
}
```

<a name="adding-meta-data"></a>
### 메타 데이터 추가하기

일부 JSON API 표준은 리소스나 리소스 컬렉션 응답에 메타 데이터를 추가하도록 요구합니다. 여기에는 리소스 자체나 연관 리소스에 대한 `links` 같은 정보나 기타 메타 데이터가 포함될 수 있습니다. 리소스에 추가 메타 데이터를 반환하려면 `toArray` 메서드 내에 포함시키면 됩니다. 예를 들어 리소스 컬렉션 변환 시 `links` 정보를 추가할 수 있습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return array
 */
public function toArray($request)
{
    return [
        'data' => $this->collection,
        'links' => [
            'self' => 'link-value',
        ],
    ];
}
```

리소스에서 추가 메타 데이터를 반환할 때, Laravel이 페이징 응답 시 자동으로 추가하는 `links`나 `meta` 키를 덮어쓰는 일이 없도록 걱정할 필요가 없습니다. 정의한 추가 `links`는 페이저가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

가끔 최상위 리소스 응답에만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 이 경우 리소스 클래스에 `with` 메서드를 추가하면 됩니다. 이 메서드는 리소스가 최상위에서 변환될 때만 포함할 메타 데이터를 배열로 반환합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return parent::toArray($request);
    }

    /**
     * 리소스 배열과 함께 반환할 추가 데이터를 반환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function with($request)
    {
        return [
            'meta' => [
                'key' => 'value',
            ],
        ];
    }
}
```

<a name="adding-meta-data-when-constructing-resources"></a>
#### 리소스 생성 시 메타 데이터 추가하기

라우트나 컨트롤러에서 리소스 인스턴스 생성 시에도 최상위 메타 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 배열 데이터를 받아 리소스 응답에 추가합니다:

```
return (new UserCollection(User::all()->load('roles')))
                ->additional(['meta' => [
                    'key' => 'value',
                ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

이미 읽었듯, 리소스는 라우트와 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

하지만 때로는 클라이언트에 응답을 보내기 전에 HTTP 응답을 더 상세하게 제어하고 싶을 때가 있습니다. 이를 위한 방법이 두 가지 있습니다. 첫째, 리소스에 `response` 메서드를 체인해서 호출하는 방법인데, 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환해 응답 헤더를 완전히 제어할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
                ->response()
                ->header('X-Value', 'True');
});
```

둘째, 리소스 자체에 `withResponse` 메서드를 정의하는 방법입니다. 이 메서드는 리소스가 최상위 응답으로 반환될 때 호출됩니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * 리소스에 대한 응답을 커스터마이징합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Illuminate\Http\Response  $response
     * @return void
     */
    public function withResponse($request, $response)
    {
        $response->header('X-Value', 'True');
    }
}
```