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

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자가 받게 될 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 하위 집합에 대해 일부 속성을 표시하거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 명확하고 쉽게 JSON으로 변환할 수 있게 해줍니다.

물론 Eloquent 모델이나 컬렉션을 `toJson` 메서드로 변환할 수도 있지만, Eloquent 리소스는 모델과 그 연관관계의 JSON 직렬화를 보다 세밀하고 강력하게 제어할 수 있게 합니다.

<a name="generating-resources"></a>
## 리소스 생성하기 (Generating Resources)

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션 (Resource Collections)

단일 모델을 변환하는 리소스 생성 외에, 모델 컬렉션을 변환하는 리소스도 생성할 수 있습니다. 이렇게 하면 JSON 응답에 해당 리소스 전체 컬렉션과 관련된 링크 또는 기타 메타 정보가 포함될 수 있습니다.

리소스 컬렉션을 생성하려면 리소스를 생성할 때 `--collection` 플래그를 사용해야 합니다. 또는 리소스 이름에 `Collection`이라는 단어를 포함시켜도 Laravel이 컬렉션 리소스를 생성하도록 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

> [!NOTE]
> 이 부분은 리소스와 리소스 컬렉션에 대한 높은 수준의 개요입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 더 깊이 이해하려면 다른 섹션도 꼭 읽어보시길 권장합니다.

리소스를 작성하는 여러 옵션을 살펴보기 전에, Laravel에서 리소스가 어떻게 사용되는지 개념적으로 먼저 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

```php
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

각 리소스 클래스는 `toArray` 메서드를 정의하며, 이는 리소스가 컨트롤러나 라우트에서 응답으로 반환될 때 JSON으로 변환할 속성들의 배열을 리턴합니다.

`$this` 변수를 통해 모델 속성에 직접 접근할 수 있는데, 이는 리소스 클래스가 기본 모델에 대한 속성과 메서드 접근을 자동으로 프록시하기 때문입니다. 리소스가 정의되면 라우트나 컨트롤러에서 이를 반환할 수 있습니다. 리소스는 생성자에서 기본 모델 인스턴스를 받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

편의를 위해 모델의 `toResource` 메서드를 사용할 수 있으며, 이 메서드는 프레임워크 규칙에 따라 모델에 적합한 리소스를 자동으로 찾아 반환합니다:

```php
return User::findOrFail($id)->toResource();
```

`toResource`를 호출할 때 Laravel은 모델의 이름에 맞고 네임스페이스에서 가장 가까운 `Http\Resources` 하위 네임스페이스 내에서 `Resource` 접미사를 가진 리소스를 찾습니다.

<a name="resource-collections"></a>
### 리소스 컬렉션 (Resource Collections)

리소스 컬렉션이나 페이지네이션된 응답을 반환할 때, 라우트나 컨트롤러에서 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는 편의상, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용하여, 프레임워크 규칙에 따라 자동으로 정확한 리소스 컬렉션 클래스를 찾아 반환할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection`을 호출할 때 Laravel은 모델명과 일치하며 `Collection` 접미사를 가진 리소스 컬렉션 클래스를, 모델 네임스페이스와 가까운 `Http\Resources` 네임스페이스 내에서 찾습니다.

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션 (Custom Resource Collections)

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환할 커스텀 메타 데이터를 추가할 수 없습니다. 컬렉션 응답을 커스터마이징하려면 리소스 컬렉션을 별도로 생성해야 합니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면 응답에 포함할 메타 데이터를 쉽게 정의할 수 있습니다:

```php
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

리소스 컬렉션을 정의한 후 라우트나 컨트롤러에서 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 편의상, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

Laravel은 적절한 네임스페이스에서 `Collection` 접미사가 붙은 리소스 컬렉션 클래스를 찾습니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기 (Preserving Collection Keys)

라우트에서 리소스 컬렉션을 반환하면 Laravel이 컬렉션 키를 숫자 순서로 재설정합니다. 하지만 리소스 클래스에 `preserveKeys` 속성을 추가하여 원래 컬렉션 키를 유지하도록 할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 컬렉션 키를 유지할지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys`가 `true`로 설정되면, 라우트나 컨트롤러에서 컬렉션이 반환될 때 컬렉션 키도 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징 (Customizing the Underlying Resource Class)

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션 내 각 아이템을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단일 리소스 클래스는 컬렉션 클래스명에서 `Collection` 접미사를 뗀 이름이며, 개인 취향에 따라 `Resource` 접미사가 붙을 수도 있습니다.

예를 들어, `UserCollection`은 각 사용자 인스턴스를 `UserResource` 리소스로 변환하려 합니다. 이 동작을 변경하려면 리소스 컬렉션의 `$collects` 속성을 오버라이드하세요:

```php
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
> [개념 개요](#concept-overview)를 아직 읽지 않았다면, 이 문서를 계속 진행하기 전에 꼭 읽어보시기 바랍니다.

리소스는 주어진 모델을 배열로 변환하는 역할만 하면 됩니다. 따라서 각 리소스에는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드가 포함되며, 이 배열은 애플리케이션 라우트나 컨트롤러에서 반환될 수 있습니다:

```php
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

리소스를 정의하면 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계 포함하기 (Relationships)

응답에 관련 리소스를 포함하려면, `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 예를 들어, `PostResource` 리소스의 `collection` 메서드를 사용해 사용자의 블로그 게시물을 포함할 수 있습니다:

```php
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
> 연관관계가 이미 로드된 경우에만 포함하려면 [조건부 연관관계](#conditional-relationships) 항목을 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성하기 (Resource Collections)

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 각 모델마다 리소스 컬렉션 클래스를 꼭 생성할 필요는 없고, 모든 Eloquent 모델 컬렉션은 "임시" 리소스 컬렉션을 생성하는 `toResourceCollection` 메서드를 제공합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

그러나 컬렉션과 함께 반환되는 메타 데이터 커스터마이징이 필요하다면 별도의 리소스 컬렉션을 정의해야 합니다:

```php
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

단일 리소스처럼 컬렉션 리소스도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

편의상 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있습니다:

```php
return User::all()->toResourceCollection();
```

Laravel은 가까운 네임스페이스에서 해당 모델과 이름이 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션 클래스가 있는지 찾습니다.

<a name="data-wrapping"></a>
### 데이터 래핑 (Data Wrapping)

기본적으로, 최상위 리소스는 JSON 변환 시 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

최상위 리소스 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 메서드는 매 요청마다 로드되는 `AppServiceProvider` 또는 다른 [서비스 프로바이더](/docs/12.x/providers)에서 호출합니다:

```php
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
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며, 직접 추가한 리소스 컬렉션 내의 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑 (Wrapping Nested Resources)

리소스 연관관계가 어떻게 래핑될지는 전적으로 개발자 자유입니다. 모든 리소스 컬렉션을 중첩 여부와 관계없이 `data` 키로 래핑하려면, 각 리소스에 대해 리소스 컬렉션 클래스를 정의하고 컬렉션을 `data` 키 안에 반환하세요.

최상위 리소스가 두 번 `data` 키로 래핑되는지 걱정할 수 있지만, Laravel은 리소스가 중복 래핑되지 않도록 자동으로 처리하므로 안심해도 됩니다:

```php
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

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때, `withoutWrapping` 메서드를 호출했다 해도 Laravel은 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이션 응답이 항상 페이저 상태에 관한 `meta` 및 `links` 키를 포함하기 때문입니다:

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

페이지네이터 인스턴스를 리소스 컬렉션의 `collection` 메서드나 커스텀 리소스 컬렉션 클래스에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는 페이지네이터의 `toResourceCollection` 메서드를 사용하여 프레임워크 규칙에 따라 자동으로 적합한 리소스 컬렉션을 찾을 수 있습니다:

```php
return User::paginate()->toResourceCollection();
```

페이지네이션 응답은 항상 페이저 상태를 담은 `meta` 및 `links` 키를 포함합니다:

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

페이지네이션 응답에서 `links` 또는 `meta` 키에 포함되는 정보를 변경하고 싶다면 리소스에 `paginationInformation` 메서드를 정의하세요. 이 메서드는 페이징된 데이터 `$paginated`와 기본 정보 배열 `$default`를 받고, `links` 및 `meta` 키를 가진 배열입니다:

```php
/**
 * 리소스의 페이지네이션 정보를 커스터마이징 합니다.
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

특정 조건을 만족할 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하는 경우를 생각할 수 있습니다. Laravel은 이런 상황을 도와주는 여러 헬퍼 메서드를 제공합니다. `when` 메서드는 조건에 따라 속성을 리소스 응답에 추가할 수 있습니다:

```php
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

위 예시에서, `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 응답에 포함됩니다. 만약 `false`면, `secret` 키는 응답에서 제거됩니다. `when` 메서드는 조건부 문 없이 간결하게 작성할 수 있도록 도와줍니다.

`when` 메서드는 두 번째 인자로 클로저도 받을 수 있어, 조건이 참일 때만 값을 계산할 수도 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

속성이 실제 모델에 있는 경우에만 포함하려면 `whenHas` 메서드를 사용할 수 있습니다:

```php
'name' => $this->whenHas('name'),
```

속성이 null 이 아닐 때만 포함하려면 `whenNotNull` 메서드를 사용하세요:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합하기 (Merging Conditional Attributes)

여러 속성이 같은 조건에 따라 응답에 포함되어야 할 때 `mergeWhen` 메서드를 사용하면 좋습니다. 주어진 조건이 참일 때 이 속성들을 병합하여 추가합니다:

```php
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

조건이 `false`면 이 속성들은 응답에서 제외됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열과 숫자 키가 혼합된 배열 내에서 사용하지 말아야 하며, 순서화되지 않은 숫자 키 배열에서도 사용하지 않아야 합니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계 (Conditional Relationships)

속성뿐만 아니라 연관관계도 조건에 따라 포함할 수 있습니다. 모델에 연관관계가 이미 로드되어 있을 때만 리소스 응답에 포함하도록 만들 수 있습니다. 이렇게 하면 컨트롤러가 로드할 연관관계를 결정하고, 리소스는 실제 로드된 경우에만 포함할 수 있어 "N+1" 문제를 줄일 수 있습니다.

`whenLoaded` 메서드는 연관관계가 로드된 경우에만 포함하도록 조건부로 사용합니다. 연관관계 객체 대신 연관관계명을 인자로 받습니다:

```php
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

연관관계가 로드되지 않았다면, `posts` 키가 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트 (Conditional Relationship Counts)

연관관계 자체뿐 아니라 연관관계 카운트도 조건부로 포함할 수 있습니다. 예를 들어 다음과 같이 연관관계 카운트를 로드할 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계 카운트가 모델에 로드된 경우에만 해당 카운트를 포함합니다. 로드되지 않았다면 속성을 제거합니다:

```php
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

`avg`, `sum`, `min`, `max` 와 같은 다른 집계도 `whenAggregated` 메서드로 조건부 포함할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보 (Conditional Pivot Information)

다대다 관계의 중간 테이블 데이터도 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드는 피벗 테이블명을 첫 번째 인자로 받고, 두 번째 인자로 피벗 정보가 있을 때 값을 반환하는 클로저를 받습니다:

```php
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

커스텀 중간 테이블 모델을 사용하는 경우, 중간 테이블 모델 인스턴스를 첫 인자로 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

피벗 정보가 `pivot`이 아닌 다른 액세서로 접근한다면 `whenPivotLoadedAs` 메서드를 사용하세요:

```php
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

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터 추가를 요구합니다. 이에는 자원이나 관련 자원에 대한 `links` 정보 또는 리소스 자체에 관한 메타 정보 등이 포함됩니다. 추가 메타 데이터를 반환할 때는 `toArray` 메서드에서 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 포함할 수 있습니다:

```php
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

추가 메타 데이터를 반환할 때, Laravel이 페이지네이션 응답 시 자동으로 추가하는 `links`나 `meta` 키가 의도치 않게 덮어쓰기 되는 걱정은 없습니다. 정의한 추가 `links`는 페이저가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터 (Top Level Meta Data)

리소스가 최상위 리소스일 때만 특정 메타 데이터를 포함하고 싶을 때가 있습니다. 보통 응답 전체에 관한 메타 정보를 의미합니다. 이런 경우 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 최상위 리소스가 변환될 때만 포함되는 메타 데이터를 배열로 반환해야 합니다:

```php
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
     * 리소스 배열과 함께 반환할 추가 데이터를 얻습니다.
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

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받습니다:

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답 (Resource Responses)

앞서 본 것처럼, 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 클라이언트에 보내기 전에 HTTP 응답을 직접 커스터마이징하고 싶을 때가 있습니다. 두 가지 방법이 있습니다. 첫 번째는 리소스에 `response` 메서드를 체이닝하는 방법입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환해 응답 헤더를 완전히 제어할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return User::find(1)
        ->toResource()
        ->response()
        ->header('X-Value', 'True');
});
```

또 다른 방법은 리소스 클래스 내부에 `withResponse` 메서드를 정의하는 것입니다. 리소스가 최상위 응답으로 반환될 때 호출됩니다:

```php
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
     * 리소스의 아웃고잉 응답을 커스터마이징합니다.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```