# Eloquent: API 자원 (API Resources)

- [소개](#introduction)
- [자원 생성하기](#generating-resources)
- [개념 개요](#concept-overview)
    - [자원 컬렉션(Resource Collections)](#resource-collections)
- [자원 작성하기](#writing-resources)
    - [데이터 래핑(Data Wrapping)](#data-wrapping)
    - [페이지네이션(Pagination)](#pagination)
    - [조건부 속성(Conditional Attributes)](#conditional-attributes)
    - [조건부 연관관계(Conditional Relationships)](#conditional-relationships)
    - [메타 데이터 추가하기(Adding Meta Data)](#adding-meta-data)
- [자원 응답(Resource Responses)](#resource-responses)

<a name="introduction"></a>
## 소개 (Introduction)

API를 구축할 때 Eloquent 모델과 실제로 애플리케이션 사용자가 받는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 집합에 대해서만 특정 속성을 보여주거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함하고 싶을 수 있습니다. Eloquent의 자원(Resource) 클래스는 모델과 모델 컬렉션을 명확하고 쉽게 JSON으로 변환할 수 있게 해줍니다.

물론, `toJson` 메서드를 사용해 Eloquent 모델이나 컬렉션을 항상 JSON으로 변환할 수 있지만, Eloquent 자원은 모델과 연관관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 자원 생성하기 (Generating Resources)

자원 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 자원은 애플리케이션의 `app/Http/Resources` 디렉토리에 저장됩니다. 자원은 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 자원 컬렉션 (Resource Collections)

개별 모델을 변환하는 자원을 생성하는 것 외에도, 모델 컬렉션을 변환하는 자원을 생성할 수 있습니다. 이렇게 하면 JSON 응답에 전체 자원 컬렉션과 관련된 링크나 메타 정보 등을 포함할 수 있습니다.

자원 컬렉션을 생성하려면, 자원 생성 시 `--collection` 플래그를 사용하거나, 자원 이름에 `Collection`이라는 단어를 포함하면 Laravel에서는 컬렉션 자원을 생성합니다. 컬렉션 자원은 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

> [!NOTE]
> 이것은 자원과 자원 컬렉션에 대한 개략적인 개요입니다. 자원이 제공하는 맞춤화와 강력한 기능을 더 깊이 이해하려면 문서의 다른 섹션도 꼭 읽어보시길 권장합니다.

자원 작성을 위한 세부 옵션을 살펴보기 전에 Laravel 내에서 자원이 어떻게 사용되는지 상위 개념부터 살펴봅시다. 자원 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 표현합니다. 예를 들어, 간단한 `UserResource` 자원 클래스가 다음과 같습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 자원을 배열로 변환합니다.
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

모든 자원 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 자원이 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환되어야 할 속성 배열을 반환합니다.

`$this` 변수에서 직접 모델 속성에 접근할 수 있는데, 이는 자원 클래스가 편의성을 위해 내부 모델에 대한 속성과 메서드 접근을 자동으로 위임하기 때문입니다. 자원이 정의되면 해당 자원을 라우트나 컨트롤러에서 반환할 수 있습니다. 자원 클래스는 생성자를 통해 내부 모델 인스턴스를 받습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 자원 컬렉션 (Resource Collections)

자원 컬렉션이나 페이징된 응답을 반환할 때는, 라우트나 컨트롤러에서 자원 클래스가 제공하는 `collection` 메서드를 사용해야 합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 방법은 컬렉션과 함께 반환되어야 하는 사용자 정의 메타 데이터를 포함할 수 없습니다. 컬렉션 응답을 맞춤화하려면 컬렉션을 표현하는 전용 자원을 생성하세요:

```shell
php artisan make:resource UserCollection
```

컬렉션 자원 클래스가 생성되면, 응답에 포함할 메타 데이터 등을 쉽게 정의할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 자원 컬렉션을 배열로 변환합니다.
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

컬렉션 자원을 정의한 후 라우트나 컨트롤러에서 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기 (Preserving Collection Keys)

라우트에서 자원 컬렉션을 반환할 때 Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만 자원 클래스에 `preserveKeys` 속성을 추가하여 컬렉션 원래 키를 유지할지 여부를 지정할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 자원 컬렉션의 키를 유지할지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys`를 `true`로 설정하면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 컬렉션 키가 유지됩니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 자원 클래스(customizing the underlying resource class) 맞춤화하기

일반적으로 자원 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 자원 클래스로 매핑한 결과로 자동 채워집니다. 단일 자원 클래스는 컬렉션 클래스 이름에서 뒤쪽의 `Collection` 부분을 뺀 이름으로 추정됩니다. 또한 개인 취향에 따라 단일 자원 클래스 이름에 `Resource`가 붙거나 안 붙을 수 있습니다.

예를 들어, `UserCollection`은 사용자 인스턴스들을 `UserResource` 자원으로 매핑하려 합니다. 이 동작을 맞춤화하려면, 컬렉션 자원의 `$collects` 속성을 오버라이드하세요:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 컬렉션이 수집하는 자원 클래스.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 자원 작성하기 (Writing Resources)

> [!NOTE]
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서의 나머지 부분을 진행하기 전에 반드시 읽어보시길 권장합니다.

요컨대 자원은 단순합니다. 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 자원은 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드를 포함합니다. 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환될 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 자원을 배열로 변환합니다.
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

자원이 정의되면, 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 연관관계 포함하기 (Relationships)

응답에 관련된 자원을 포함하려면, 자원의 `toArray` 메서드가 반환하는 배열에 추가하면 됩니다. 예를 들어, `PostResource`의 `collection` 메서드를 사용해 사용자의 블로그 게시글을 자원 응답에 포함할 수 있습니다:

```
use App\Http\Resources\PostResource;

/**
 * 자원을 배열로 변환합니다.
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

> [!NOTE]
> 로드된 경우에만 연관관계를 포함하려면, [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 자원 컬렉션 (Resource Collections)

자원은 단일 모델을 배열로 변환하는 반면, 자원 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 모델에 대해 별도의 자원 컬렉션 클래스를 반드시 정의할 필요는 없으며, 모든 자원은 즉석에서 "임시" 자원 컬렉션을 생성하는 `collection` 메서드를 제공합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션과 함께 반환되는 메타 데이터 등을 맞춤화하려면, 직접 자원 컬렉션을 정의해야 합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 자원 컬렉션을 배열로 변환합니다.
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

단일 자원과 마찬가지로, 자원 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑 (Data Wrapping)

기본적으로 자원 응답은 JSON으로 변환될 때 가장 바깥쪽에 `data` 키로 감싸집니다. 예를 들어, 일반적인 자원 컬렉션 응답은 다음과 같습니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ]
}
```

`data` 대신 다른 키를 사용하고 싶다면, 자원 클래스에 `$wrap` 속성을 정의하세요:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 적용할 "data" 래핑 키
     *
     * @var string|null
     */
    public static $wrap = 'user';
}
```

래핑을 완전히 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 보통 이 메서드는 `AppServiceProvider`나 요청마다 로드되는 다른 [서비스 프로바이더](/docs/9.x/providers)에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> `withoutWrapping` 메서드는 가장 바깥쪽 응답에만 영향을 주며, 사용자가 직접 자원 컬렉션에 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 자원 래핑 (Wrapping Nested Resources)

자원의 연관관계가 어떻게 래핑될지는 완전히 자유롭게 결정할 수 있습니다. 모든 자원 컬렉션을 중첩 여부와 관계없이 `data` 키로 래핑하고 싶다면, 각 자원마다 자원 컬렉션 클래스를 정의하고 컬렉션을 `data` 키로 감싸서 반환하세요.

이것이 가장 바깥쪽 자원이 `data` 키로 두 번 래핑되지는 않을지 궁금할 수 있지만, 걱정하지 마세요. Laravel은 자원이 이중 래핑되는 것을 방지하므로, 자원 컬렉션의 중첩 수준에 대해 신경 쓸 필요가 없습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * 자원 컬렉션을 배열로 변환합니다.
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
#### 데이터 래핑과 페이지네이션 (Data Wrapping And Pagination)

자원 응답으로 페이징된 컬렉션을 반환할 때는, `withoutWrapping` 메서드를 호출했더라도 Laravel이 자원 데이터를 `data` 키로 강제로 래핑합니다. 이는 페이징 응답이 항상 `meta`와 `links` 키를 포함하여 페이저 상태 정보를 담기 때문입니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
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
### 페이지네이션 (Pagination)

Laravel 페이저 인스턴스를 자원의 `collection` 메서드나 사용자 정의 자원 컬렉션에 전달할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이징된 응답은 항상 페이저 상태 정보를 담은 `meta` 및 `links` 키를 포함합니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
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
### 조건부 속성 (Conditional Attributes)

특정 조건이 충족될 때만 속성을 자원 응답에 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 특정 값을 포함하도록 할 수 있습니다. Laravel은 이를 도와줄 다양한 헬퍼 메서드를 제공합니다. `when` 메서드는 조건부로 자원 응답에 속성을 추가할 때 사용됩니다:

```
/**
 * 자원을 배열로 변환합니다.
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
        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

이 예제에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 응답에 포함됩니다. 조건이 `false`라면 `secret` 키는 클라이언트로 전송되기 전에 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들 때 조건문을 사용하지 않고도 명확하게 자원을 정의할 수 있습니다.

또한 `when` 메서드는 두 번째 인수로 클로저를 받아 조건이 참일 때만 연산해서 값을 반환하도록 할 수 있습니다:

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

또한, `whenHas` 메서드는 해당 속성이 내부 모델에 실제로 존재할 때만 속성을 포함합니다:

```
'name' => $this->whenHas('name'),
```

그리고 `whenNotNull` 메서드는 속성이 null이 아닐 때만 자원 응답에 포함합니다:

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합 (Merging Conditional Attributes)

같은 조건에 기반해 여러 속성을 포함해야 한다면, `mergeWhen` 메서드를 사용할 수 있습니다. 조건이 `true`일 때만 여러 속성을 한꺼번에 응답에 병합합니다:

```
/**
 * 자원을 배열로 변환합니다.
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
        $this->mergeWhen($request->user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

조건이 `false`일 경우, 병합한 속성들은 클라이언트에 응답되기 전에 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자 키와 숫자 키가 혼용된 배열 안이나, 순차적으로 정렬되지 않은 숫자 키 배열 안에서는 사용하지 마세요.

<a name="conditional-relationships"></a>
### 조건부 연관관계 (Conditional Relationships)

속성과 마찬가지로, 연관관계도 모델에 이미 로드된 경우에만 자원 응답에 포함할 수 있습니다. 이렇게 하면 컨트롤러에서 어떤 연관관계를 로드할지 결정하고, 자원에서는 실제 로드된 경우에만 그 연관관계를 포함함으로써 결국 자원 내의 "N+1" 쿼리 문제를 피할 수 있습니다.

`whenLoaded` 메서드는 연관관계를 조건부로 포함할 때 사용합니다. 연관관계를 불필요하게 로드하지 않도록, 관계명(문자열)을 인자로 받습니다:

```
use App\Http\Resources\PostResource;

/**
 * 자원을 배열로 변환합니다.
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

만약 연관관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전에 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 개수 (Conditional Relationship Counts)

연관관계를 조건부로 포함하듯, 해당 연관관계의 "개수"도 로드된 경우에만 자원 응답에 포함할 수 있습니다:

```
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계 개수가 존재할 때만 속성을 포함하여 필요 없는 포함을 방지합니다:

```
/**
 * 자원을 배열로 변환합니다.
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
        'posts_count' => $this->whenCounted('posts'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

`posts` 연관관계 개수가 로드되지 않았다면, `posts_count` 키는 응답에서 제거됩니다.

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보 (Conditional Pivot Information)

관계 응답에 포함된 중간 테이블 데이터(많은 대 많은 관계의 중간 정보)를 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드가 이를 지원하며, 첫 번째 인자로 피벗 테이블 이름을 받고, 두 번째 인자로 피벗 정보가 존재할 때 반환할 값을 제공하는 클로저를 받습니다:

```
/**
 * 자원을 배열로 변환합니다.
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

[사용자 지정 중간 테이블 모델](/docs/9.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, 중간 테이블 모델 인스턴스를 `whenPivotLoaded`의 첫 번째 인자로 전달할 수 있습니다:

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

만약 피벗 정보 접근자가 기본 `pivot`이 아닌 다른 이름일 경우, `whenPivotLoadedAs` 메서드를 사용합니다:

```
/**
 * 자원을 배열로 변환합니다.
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
### 메타 데이터 추가하기 (Adding Meta Data)

일부 JSON API 표준에서는 자원 및 자원 컬렉션 응답에 메타 데이터를 추가할 것을 요구합니다. 여기에는 자원 또는 관련 자원에 대한 `links` 정보나 자원 자체에 대한 메타 데이터가 포함될 수 있습니다. 자원에 대한 추가 메타 데이터를 반환하려면, `toArray` 메서드에 포함하세요. 예를 들어, 자원 컬렉션을 변환할 때 `links` 정보를 추가할 수 있습니다:

```
/**
 * 자원을 배열로 변환합니다.
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

자원에서 추가 메타 데이터를 반환하더라도, 페이징 응답 시 Laravel이 자동으로 생성하는 `links`와 `meta` 키를 실수로 덮어쓸 걱정을 하지 않아도 됩니다. 사용자가 정의하는 추가 `links`는 페이저가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터 (Top Level Meta Data)

가끔 최상위 응답 자원일 때에만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 일반적으로 이는 응답 전체에 대한 메타 정보를 포함합니다. 이렇게 하려면 자원 클래스에 `with` 메서드를 추가하세요. 이 메서드는 자원이 응답의 최상위 자원일 때만 포함될 메타 데이터를 배열로 반환해야 합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 자원 컬렉션을 배열로 변환합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return parent::toArray($request);
    }

    /**
     * 자원 배열과 함께 반환할 추가 데이터를 가져옵니다.
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
#### 자원 생성 시 메타 데이터 추가하기 (Adding Meta Data When Constructing Resources)

라우트나 컨트롤러에서 자원 인스턴스를 생성할 때 최상위 데이터를 추가할 수도 있습니다. 모든 자원에서 사용할 수 있는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받습니다:

```
return (new UserCollection(User::all()->load('roles')))
                ->additional(['meta' => [
                    'key' => 'value',
                ]]);
```

<a name="resource-responses"></a>
## 자원 응답 (Resource Responses)

이미 보았듯이, 자원은 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

하지만 응답이 클라이언트에 전송되기 전에 HTTP 응답을 맞춤화해야 할 때가 있습니다. 이를 위해 두 가지 방법이 있습니다. 첫 번째는 자원에 `response` 메서드를 체인으로 호출하는 방법입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 이로써 응답 헤더를 완전하게 제어할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
                ->response()
                ->header('X-Value', 'True');
});
```

또는 자원 클래스 내부에 `withResponse` 메서드를 정의할 수 있습니다. 자원이 최상위 자원으로서 응답에 반환될 때 이 메서드가 호출되어 응답을 맞춤화할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 자원을 배열로 변환합니다.
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
     * 자원의 응답을 맞춤화합니다.
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