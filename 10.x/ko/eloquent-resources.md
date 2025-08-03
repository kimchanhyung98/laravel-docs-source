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
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자 집합에 대해서만 특정 속성을 표시하거나 모델들의 JSON 표현에 언제나 특정 연관관계를 포함시키고 싶을 수도 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 표현하고 변환하는 과정을 명확하고 쉽게 해줍니다.

물론, 언제든지 Eloquent 모델이나 컬렉션을 `toJson` 메서드로 JSON으로 변환할 수 있지만, Eloquent 리소스를 사용하면 모델과 그 연관관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어가 가능합니다.

<a name="generating-resources"></a>
## 리소스 생성하기

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스들은 애플리케이션의 `app/Http/Resources` 디렉터리에 위치합니다. 리소스들은 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 생성 이외에도, 모델 컬렉션을 변환하는 역할의 리소스를 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 전체 컬렉션에 관련된 링크 및 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면 리소스를 생성할 때 `--collection` 플래그를 사용하거나, 리소스 이름에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스를 생성하도록 인식합니다. 컬렉션 리소스들은 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]  
> 다음은 리소스와 리소스 컬렉션의 개괄적인 개요입니다. 리소스가 제공하는 맞춤화와 강력한 기능들을 깊이 이해하기 위해 문서의 다른 섹션들을 반드시 읽어보시길 권장합니다.

리소스를 작성할 때 가능한 옵션들을 모두 살펴보기 전에, Laravel에서 리소스가 어떻게 사용되는지 고수준으로 먼저 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 나타냅니다. 예를 들어 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 리소스가 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환되어야 하는 속성들의 배열을 반환합니다.

`$this` 변수로부터 모델 속성들에 직접 접근할 수 있다는 점에 주의하세요. 이는 리소스 클래스가 편의성 측면에서 하위 모델에 대한 프로퍼티와 메서드 접근을 자동으로 위임하기 때문입니다. 리소스가 정의되면 라우트나 컨트롤러에서 바로 반환할 수 있습니다. 리소스는 생성자에서 하위 모델 인스턴스를 받습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션이나 페이징된 응답을 반환할 때에는, 라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 해당 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 방법은 컬렉션과 함께 반환해야 할 커스텀 메타 데이터를 추가할 수 없습니다. 컬렉션 응답을 맞춤화하려면 컬렉션 전용 리소스를 생성할 수 있습니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스를 생성한 후에는 응답에 포함할 메타 데이터를 쉽게 정의할 수 있습니다:

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

리소스 컬렉션을 정의한 후에는 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만 컬렉션의 원래 키를 유지할지 여부를 나타내는 `preserveKeys` 속성을 리소스 클래스에 추가할 수 있습니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스 컬렉션의 키를 유지할지 여부입니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys`가 `true`로 설정되면 라우트나 컨트롤러에서 컬렉션을 반환할 때 키가 유지됩니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 맞춤화하기

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 내부 컬렉션의 각 항목을 단수형 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단수 리소스 클래스는 컬렉션 클래스 이름에서 `Collection` 부분이 제거된 이름으로 추측됩니다. 또한 개인 취향에 따라 단수 리소스 클래스에 `Resource` 접미사가 붙기도 합니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스들을 `UserResource` 리소스로 매핑합니다. 이 동작을 변경하려면 리소스 컬렉션의 `$collects` 속성을 오버라이드하면 됩니다:

```
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스가 수집할 리소스 클래스입니다.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성하기

> [!NOTE]  
> 아직 [개념 개요](#concept-overview) 섹션을 읽지 않았다면, 이 문서의 나머지 부분을 진행하기 전에 반드시 확인하시길 권장합니다.

리소스는 주어진 모델을 배열로 변환하는 작업만 필요합니다. 따라서 각 리소스는 `toArray` 메서드를 포함하며 이 메서드는 모델 속성을 API 친화적인 배열로 변환하여 애플리케이션의 라우트나 컨트롤러가 반환할 수 있게 합니다:

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

리소스가 정의되면 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 연관관계 포함하기

리소스 응답에 관련된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 해당 항목을 추가하면 됩니다. 다음 예시에서는 `PostResource` 리소스의 `collection` 메서드를 사용하여 사용자의 블로그 글들을 응답에 추가합니다:

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
> 이미 로드된 경우에만 연관관계를 포함하고 싶다면, [조건부 연관관계](#conditional-relationships) 섹션을 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성하기

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 그러나 각 모델마다 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다. 모든 리소스 클래스는 즉석에서 "임시" 리소스 컬렉션을 생성하는 `collection` 메서드를 제공합니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션과 함께 반환할 메타 데이터를 맞춤화하려면 반드시 별도의 리소스 컬렉션을 정의해야 합니다:

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

단수 리소스와 마찬가지로, 리소스 컬렉션은 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 리소스 응답이 JSON으로 변환될 때 가장 바깥 리소스는 `data` 키로 감싸집니다. 예를 들어 전형적인 리소스 컬렉션 응답은 다음과 같이 보입니다:

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

가장 바깥 리소스의 래핑을 해제하고 싶다면, 기본 클래스인 `Illuminate\Http\Resources\Json\JsonResource` 에서 `withoutWrapping` 메서드를 호출해야 합니다. 보통 이 메서드는 `AppServiceProvider` 또는 매 요청 시 로드되는 다른 [서비스 프로바이더](/docs/10.x/providers)에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]  
> `withoutWrapping` 메서드는 가장 바깥의 응답에만 영향을 주며, 사용자가 직접 리소스 컬렉션 내에 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스 래핑

연관된 리소스 컬렉션들도 모두 `data` 키로 래핑되도록 완전한 자유가 있습니다. 중첩 여부와 상관없이 모든 리소스 컬렉션을 `data` 키로 감싸고 싶다면, 각 리소스마다 컬렉션 클래스를 정의하고 그 안에서 `data` 키 안에 컬렉션을 반환하도록 하세요.

"리소스가 `data` 키 두 번 중첩되는 것 아니냐?"라고 걱정할 수 있지만, Laravel은 중첩 수준과 관계없이 리소스가 이중 래핑되지 않도록 자동으로 처리하므로 걱정하지 않아도 됩니다:

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
#### 데이터 래핑과 페이지네이션

리소스 응답으로 페이징된 컬렉션을 반환할 때에는, `withoutWrapping` 메서드를 호출했더라도 Laravel은 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이징 응답에 항상 페이지네이터 상태에 대한 `meta` 및 `links` 키가 포함되기 때문입니다:

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
### 페이지네이션

Laravel의 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다:

```
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이지네이션 응답에는 언제나 페이지네이터 상태에 대한 `meta` 및 `links` 키가 포함됩니다:

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
#### 페이지네이션 정보 맞춤화하기

페이지네이션 응답의 `links` 혹은 `meta` 키에 포함될 정보를 맞춤화하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `links` 및 `meta` 키가 포함된 기본 배열인 `$default`를 받습니다:

```
/**
 * 리소스의 페이지네이션 정보를 맞춤화합니다.
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
### 조건부 속성

특정 조건이 만족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 경우에만 값을 포함시키고 싶을 수 있습니다. Laravel은 이런 상황을 도와주는 여러 헬퍼 메서드를 제공합니다. `when` 메서드는 조건에 따라 리소스 응답에 속성을 추가할 때 사용할 수 있습니다:

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

이 예시에서, `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 포함됩니다. 만약 `false`라면, `secret` 키는 클라이언트로 보내기 전 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 작성할 때 조건문을 쓰지 않고도 표현식으로 쉽게 리소스를 정의할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저도 받아, 조건이 참일 때만 값을 계산하게 만들 수도 있습니다:

```
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 해당 속성이 실제로 모델에 존재할 때만 포함하도록 할 수 있습니다:

```
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 속성이 `null`이 아닐 경우에만 포함할 수 있습니다:

```
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합하기

여러 속성이 같은 조건일 때만 포함되어야 한다면, `mergeWhen` 메서드를 사용하여 조건이 `true`일 때만 해당 속성들을 응답에 추가할 수 있습니다:

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

조건이 `false`일 때는 클라이언트에 보내기 전에 이 속성들이 응답에서 제거됩니다.

> [!WARNING]  
> `mergeWhen` 메서드는 문자열 및 숫자 키가 혼합된 배열 안에서, 또는 순차적으로 정렬되지 않은 숫자 키 배열 안에서 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성뿐 아니라 연관관계도 조건에 따라 리소스 응답에 포함할 수 있습니다. 이는 컨트롤러에서 모델에 어떤 연관관계를 로드할지 결정하고, 리소스가 실제로 로드된 경우에만 포함하도록 할 때 유용합니다. 이렇게 하면 "N+1" 쿼리 문제를 방지하기도 쉽습니다.

`whenLoaded` 메서드는 연관관계 이름을 인수로 받아서 조건부로 연관관계를 포함할 수 있게 해줍니다:

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

연관관계가 로드되지 않았다면, 응답에서 `posts` 키는 클라이언트에 보내기 전에 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 개수 포함하기

조건부 연관관계를 포함하는 것과 마찬가지로, 연관관계의 개수가 로드된 경우에만 "연관관계 개수"를 응답에 포함할 수도 있습니다:

```
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계 개수 응답에 조건부 포함을 지원하며, 연관관계 개수가 없으면 해당 속성을 포함하지 않습니다:

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

이 경우 `posts` 연관관계의 개수가 로드되지 않았다면, `posts_count` 키는 응답에서 제거됩니다.

`whenAggregated` 메서드를 사용하면 `avg`, `sum`, `min`, `max` 같은 기타 집계값도 조건부로 포함할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

리소스 응답에서 many-to-many 관계의 중간 테이블 데이터를 조건부로 포함하려면 `whenPivotLoaded` 메서드를 사용합니다. 첫 번째 인수로 중간 테이블 이름을 넘기고, 두 번째 인수로 피벗 정보가 있을 때 반환할 값을 리턴하는 클로저를 넘깁니다:

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

[사용자 정의 중간 테이블 모델](/docs/10.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우 `whenPivotLoaded` 메서드에 모델 인스턴스를 넘깁니다:

```
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블의 엑세서가 `pivot`이 아닌 경우에는 `whenPivotLoadedAs` 메서드를 사용하세요:

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
### 메타 데이터 추가

일부 JSON API 표준에서는 리소스 또는 리소스 컬렉션 응답에 메타 데이터를 추가하도록 요구합니다. 일반적으로 이는 리소스 자체 또는 관련 리소스의 `links`나 메타 데이터 같은 정보를 포함합니다. 리소스에 추가 정보를 포함시키려면 `toArray` 메서드에서 배열에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 포함할 수 있습니다:

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

페이지네이션 응답의 경우 Laravel이 자동으로 추가하는 `links`나 `meta` 키와 충돌하지 않도록 주의할 필요가 없습니다. 사용자가 정의한 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

가끔 최상위 리소스 응답에만 특정 메타 데이터를 포함하고 싶을 때가 있습니다. 보통 이는 응답 전체에 대한 메타 정보입니다. 이런 메타 데이터를 정의하려면, 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 리소스가 최상위 리소스일 때만 포함될 메타 데이터 배열을 반환해야 합니다:

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
     * 리소스 배열 응답에 추가적으로 포함해야 할 데이터 배열을 반환합니다.
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
#### 리소스 인스턴스 생성 시 메타 데이터 추가하기

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 메타 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용 가능한 `additional` 메서드는 리소스 응답에 추가할 데이터를 배열로 받습니다:

```
return (new UserCollection(User::all()->load('roles')))
                ->additional(['meta' => [
                    'key' => 'value',
                ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

이미 읽은 것처럼, 리소스는 라우트나 컨트롤러에서 직접 반환될 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

하지만 때론 클라이언트에 보내기 전 HTTP 응답을 커스터마이즈할 필요가 있습니다. 이를 위해 두 가지 방법이 있습니다. 첫 번째는 리소스에 `response` 메서드를 체인으로 호출하는 것입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 응답 헤더를 완전히 제어할 수 있습니다:

```
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
                ->response()
                ->header('X-Value', 'True');
});
```

또 다른 방법은 리소스 클래스 내에 `withResponse` 메서드를 정의하는 겁니다. 이 메서드는 리소스가 가장 바깥의 리소스로 반환될 때 호출됩니다:

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
     * 리소스의 응답을 커스터마이즈합니다.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```