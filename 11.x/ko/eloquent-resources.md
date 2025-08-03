# Eloquent: API 리소스 (Eloquent: API Resources)

- [소개](#introduction)
- [리소스 생성하기](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성하기](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 연관관계](#conditional-relationships)
    - [메타 데이터 추가하기](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개 (Introduction)

API를 구축할 때, Eloquent 모델과 실제 애플리케이션 사용자가 받는 JSON 응답 사이에 변환 계층(transform layer)이 필요할 수 있습니다. 예를 들어, 일부 사용자에 대해서만 특정 속성을 표시하거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 표현하는 과정을 명료하고 손쉽게 할 수 있도록 도와줍니다.

물론, Eloquent 모델이나 컬렉션을 `toJson` 메서드로 직접 변환할 수도 있지만, Eloquent 리소스는 모델 및 연관관계의 JSON 직렬화에 대해 보다 세밀하고 강력한 제어권을 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성하기 (Generating Resources)

리소스 클래스를 생성하려면, `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 생성된 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 위치합니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속받습니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션 (Resource Collections)

개별 모델을 변환하는 리소스 외에도, 모델 컬렉션을 변환할 책임이 있는 리소스를 생성할 수 있습니다. 이를 통해 JSON 응답에 링크나 컬렉션 전체에 관한 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용하거나 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel이 컬렉션용 리소스를 생성합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속받습니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

> [!NOTE]  
> 아래는 리소스 및 리소스 컬렉션에 대한 상위 수준 개요입니다. 리소스가 제공하는 맞춤화 및 강력한 기능을 깊이 이해하려면 이 문서의 다른 섹션도 반드시 읽어보시길 권장합니다.

리소스를 작성할 때 사용 가능한 옵션을 자세히 살펴보기 전에, Laravel에서 리소스가 어떻게 사용되는지 상위 수준에서 먼저 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 표현합니다. 예를 들어, 간단한 `UserResource` 클래스는 다음과 같습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 리소스가 라우트나 컨트롤러에서 응답으로 반환될 때 JSON으로 변환될 속성 배열을 반환합니다.

`$this` 변수를 통해 모델 속성에 직접 접근할 수 있다는 점에 주의하세요. 이는 리소스 클래스가 자동으로 이 속성 및 메서드 접근을 내부의 원본 모델로 프록시하기 때문입니다. 리소스가 정의된 후에는 이를 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자에서 내부 모델 인스턴스를 받습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션 (Resource Collections)

리소스 컬렉션 또는 페이지네이션된 응답을 반환할 때는, 라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 해당 리소스 클래스의 `collection` 메서드를 사용해야 합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 방법은 컬렉션과 함께 반환해야 할 맞춤 메타 데이터를 추가할 수 없습니다. 컬렉션 응답을 맞춤화하고 싶다면, 컬렉션을 표현하는 별도의 리소스를 생성하세요:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스 생성 후에는 응답에 포함할 필요한 메타 데이터를 쉽게 정의할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
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

리소스 컬렉션을 정의한 후에는, 라우트나 컨트롤러에서 이를 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기 (Preserving Collection Keys)

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만, 리소스 클래스에 `preserveKeys` 속성을 추가하여 원래 컬렉션 키를 유지할지 여부를 지정할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스 컬렉션 키의 유지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 가 `true`로 설정된 경우, 컬렉션이 라우트 또는 컨트롤러에서 반환될 때 컬렉션의 키가 유지됩니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 리소스 클래스 커스터마이징 (Customizing the Underlying Resource Class)

보통, 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 아이템을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단일 리소스 클래스는 컬렉션 클래스 이름에서 끝의 `Collection` 부분을 제외한 이름으로 간주되며, 개인 취향에 따라 이름 뒤에 `Resource`가 붙을 수도, 안 붙을 수도 있습니다.

예를 들어, `UserCollection`은 제공된 사용자 인스턴스들을 `UserResource` 리소스로 매핑하려 시도합니다. 이 동작을 변경하려면, 컬렉션 리소스 내부에서 `$collects` 속성을 재정의할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스가 수집하는 리소스 클래스입니다.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성하기 (Writing Resources)

> [!NOTE]  
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 진행하기 전에 반드시 개념 개요 섹션을 읽어보시길 권장합니다.

리소스는 주어진 모델을 배열로 변환하는 것만 필요로 합니다. 따라서, 각 리소스에는 `toArray` 메서드가 포함되어 있어 모델의 속성을 API 친화적인 배열로 변환하며, 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
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

리소스를 정의한 후, 라우트 또는 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 연관관계 포함하기 (Relationships)

응답에 연관된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 관련 리소스를 추가할 수 있습니다. 다음 예제에서는 `PostResource` 리소스의 `collection` 메서드를 사용해 사용자의 블로그 게시글을 함께 응답합니다:

```
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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
> 연관관계가 이미 로드된 경우에만 포함시키고 싶다면, [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성하기 (Resource Collections)

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 컬렉션마다 별도의 리소스 컬렉션 클래스를 반드시 정의해야 하는 것은 아닙니다. 모든 리소스에 `collection` 메서드가 있기 때문에, 즉시 "임시" 리소스 컬렉션을 생성할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션과 함께 반환하는 메타 데이터를 커스터마이징하려면, 자체 리소스 컬렉션 클래스를 정의해야 합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
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

단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트 또는 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑 (Data Wrapping)

기본적으로 리소스의 최상위 레벨 응답은 `data` 키로 래핑(wrap)되어 JSON으로 변환됩니다. 예를 들어, 전형적인 리소스 컬렉션 응답은 다음과 같습니다:

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

최상위 리소스 래핑을 비활성화하려면, 기본 클래스인 `Illuminate\Http\Resources\Json\JsonResource`에서 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 메서드는 `AppServiceProvider` 혹은 모든 요청 시 로드되는 다른 [서비스 프로바이더](/docs/11.x/providers) 내에서 호출해야 합니다:

```
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]  
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며, 사용자가 직접 추가한 리소스 컬렉션 내부의 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑 (Wrapping Nested Resources)

리소스의 연관 관계들이 어떻게 래핑될 것인지 결정하는 것은 전적으로 개발자에게 달려 있습니다. 모든 리소스 컬렉션을 중첩 관계에 상관없이 `data` 키로 래핑하고 싶다면, 각 리소스에 대한 리소스 컬렉션 클래스를 정의하고, 해당 컬렉션을 `data` 키 내에 반환하면 됩니다.

최상위 리소스가 `data` 키로 중첩 두 번 래핑되는지 걱정할 수 있으나, Laravel은 중복 래핑을 방지하기 때문에 리소스 컬렉션의 중첩 수준에 대해 신경쓸 필요가 없습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return ['data' => $this->collection];
    }
}
```

<a name="data-wrapping-and-pagination"></a>
#### 데이터 래핑과 페이지네이션 (Data Wrapping and Pagination)

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는, `withoutWrapping`이 호출되었어도 Laravel이 자동으로 리소스 데이터를 `data` 키로 감쌉니다. 이는 페이지네이션 응답이 `meta`와 `links` 키를 포함하며, 페이지네이터 상태 정보를 담고 있기 때문입니다:

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
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="pagination"></a>
### 페이지네이션 (Pagination)

`collection` 메서드나 커스텀 리소스 컬렉션에 Laravel의 페이지네이터 인스턴스를 전달할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이지네이션된 응답은 항상 페이지네이터 상태 정보를 담은 `meta` 및 `links` 키를 포함합니다:

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
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```

<a name="customizing-the-pagination-information"></a>
#### 페이지네이션 정보 커스터마이징 (Customizing the Pagination Information)

페이지네이션 응답의 `links` 또는 `meta` 키에 포함된 정보를 맞춤화하고 싶다면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 기본적으로 제공되는 `links` 및 `meta` 정보를 담은 `$default` 배열을 인자로 받습니다:

```
/**
 * 리소스의 페이지네이션 정보를 커스터마이징합니다.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array $paginated
 * @param  array $default
 * @return array
 */
public function paginationInformation($request, $paginated, $default)
{
    $default['links']['custom'] = 'https://example.com';

    return $default;
}
```

<a name="conditional-attributes"></a>
### 조건부 속성 (Conditional Attributes)

경우에 따라 특정 조건을 만족할 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 값을 포함시키고자 할 수 있습니다. Laravel은 이런 상황을 지원하기 위한 여러 헬퍼 메서드를 제공합니다. `when` 메서드를 사용해 조건에 따라 속성 추가를 제어할 수 있습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

위 예에서 현재 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때에만 `secret` 키가 최종 응답에 포함됩니다. 만약 `false`라면 `secret` 키는 클라이언트로 전달되기 전에 해당 응답에서 제거됩니다. `when` 메서드 덕분에 배열을 구성할 때 조건문 없이도 리소스를 명료하게 작성할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저를 받아, 조건이 `true`일 때만 값을 동적으로 계산할 수도 있습니다:

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 모델에 실제로 해당 속성이 존재할 때만 포함하도록 할 수 있습니다:

```
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 속성이 `null`이 아닌 경우에만 포함할 때 사용합니다:

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합 (Merging Conditional Attributes)

여러 속성을 동일 조건 하에서만 포함시키고 싶을 때는 `mergeWhen` 메서드를 사용하면 됩니다. 주어진 조건이 `true`인 경우에만 배열 내부에 여러 속성을 병합해서 포함시켜 줍니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

조건이 `false`이면 해당 속성들은 클라이언트에 전달되기 전에 응답에서 제거됩니다.

> [!WARNING]  
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 섞인 배열에서 사용하지 않는 것이 좋으며, 순차적이지 않은 숫자 키 배열에서도 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계 (Conditional Relationships)

속성뿐 아니라 연관관계도 조건부로 로드할 수 있습니다. 연관관계가 모델에 이미 로드된 경우에만 리소스 응답에 포함하도록 할 수 있습니다. 이를 통해 컨트롤러는 필요한 연관관계만 로드하고, 리소스는 실제 로드된 연관관계만 쉽게 포함시켜 "N+1" 쿼리 문제를 피하기 편리합니다.

`whenLoaded` 메서드는 연관관계를 조건부로 포함하는 데 사용됩니다. 불필요한 쿼리를 막기 위해 관계 자체가 아니라 관계 이름을 인수로 받습니다:

```
use App\Http\Resources\PostResource;

/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

연관관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전달되기 전에 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트 (Conditional Relationship Counts)

연관관계뿐 아니라 연관관계의 "카운트" 역시 조건부로 포함할 수 있습니다. 예를 들어:

```
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드를 사용하면 카운트가 실제 로드된 경우에만 연관관계 카운트가 리소스 응답에 포함됩니다. 로드되지 않았으면 해당 카운트 속성이 제외됩니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

이 외에 `avg`, `sum`, `min`, `max` 등 다른 집계 메서드도 `whenAggregated`를 이용해 조건부로 포함할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보 (Conditional Pivot Information)

다대다(many-to-many) 연관관계의 중간 테이블 데이터를 조건부로 포함하려면 `whenPivotLoaded` 메서드를 사용하세요. 첫 번째 인자로 피벗 테이블 이름을 받고, 두 번째 인자에는 피벗 정보가 있을 때 반환할 값을 계산하는 클로저를 받습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

커스텀 중간 테이블 모델을 사용하는 경우, 그 모델 인스턴스를 첫 번째 인자로 넘길 수도 있습니다:

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 `pivot`이 아닌 다른 접근자를 사용하는 경우 `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
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

JSON API 표준에 따라, 리소스 혹은 리소스 컬렉션 응답에 메타 데이터를 추가해야 할 수도 있습니다. 예를 들어, 리소스 또는 관련 리소스에 대한 `links`나 자원 자체에 관한 메타 정보 등을 포함할 수 있습니다. 추가 메타 데이터를 반환하려면 `toArray` 메서드에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션을 변환할 때 `links` 정보를 넣을 수 있습니다:

```
/**
 * 리소스를 배열로 변환합니다.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'data' => $this->collection,
        'links' => [
            'self' => 'link-value',
        ],
    ];
}
```

리소스에서 추가 메타 데이터를 반환할 때, Laravel이 페이지네이션 응답 시 자동으로 추가하는 `links` 또는 `meta` 키를 실수로 덮어쓸 걱정은 하지 않아도 됩니다. 사용자 정의 `links`는 페이지네이터가 제공하는 링크와 자동으로 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터 (Top Level Meta Data)

때로는 리소스가 가장 최상위에서 반환될 때에만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 이는 보통 응답 전체에 대한 메타 정보를 의미합니다. 이 경우, 리소스 클래스에 `with` 메서드를 추가해 최상위 리소스가 변환될 때 포함할 메타 데이터를 배열 형태로 반환하도록 정의합니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return parent::toArray($request);
    }

    /**
     * 리소스 배열과 함께 반환할 추가 데이터를 가져옵니다.
     *
     * @return array<string, mixed>
     */
    public function with(Request $request): array
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
#### 리소스 생성 시 메타 데이터 추가하기 (Adding Meta Data When Constructing Resources)

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터 추가가 가능합니다. 모든 리소스가 제공하는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받습니다:

```
return (new UserCollection(User::all()->load('roles')))
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답 (Resource Responses)

앞서 보았듯, 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

하지만, 때로는 클라이언트에 응답을 보내기 전에 HTTP 응답을 커스터마이징해야 할 수도 있습니다. 이 경우 두 가지 방법이 있습니다. 먼저, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하여 응답 헤더를 완전히 제어할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
        ->response()
        ->header('X-Value', 'True');
});
```

또는, 리소스 클래스 자체에 `withResponse` 메서드를 정의하여, 리소스가 최상위에서 반환될 때 호출되도록 할 수도 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환합니다.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * 리소스 응답의 아웃고잉 HTTP 응답을 맞춤화합니다.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```