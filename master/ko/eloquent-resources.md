# Eloquent: API 리소스 (Eloquent: API Resources)

- [소개](#introduction)
- [리소스 생성](#generating-resources)
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
## 소개

API를 구축할 때, Eloquent 모델과 애플리케이션 사용자에게 실제로 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 집합에 대해서만 특정 속성을 표시하거나, JSON 표현에 항상 특정 연관관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 표현력 있게 쉽게 변환할 수 있도록 해줍니다.

물론, Eloquent 모델이나 컬렉션을 `toJson` 메서드로 직접 JSON으로 변환할 수도 있지만, Eloquent 리소스는 모델과 그 연관관계들의 JSON 직렬화에 대해 더 세밀하고 견고한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령을 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 생성 외에, 모델 컬렉션을 변환하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 링크나 컬렉션 전체와 관련된 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용하거나, 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel이 컬렉션 리소스를 생성하도록 인지합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이 개요는 리소스 및 리소스 컬렉션에 대한 고수준 개념 설명입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 더 깊이 이해하려면 문서의 다른 섹션들도 꼭 읽어보시길 권장합니다.

리소스를 작성할 때 사용할 수 있는 다양한 옵션에 대해 자세히 살펴보기 전에, Laravel에서 리소스가 어떻게 사용되는지 고수준으로 먼저 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 해당 리소스가 라우트나 컨트롤러 메서드에서 응답으로 반환될 때 JSON으로 변환될 속성들을 배열 형태로 반환합니다.

`$this` 변수에서 직접 모델 속성에 접근하는 것을 볼 수 있는데, 이는 리소스 클래스가 기본적으로 모델의 속성과 메서드 접근을 편리하게 프록시로 전달하기 때문입니다. 리소스가 정의되면 이를 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자에서 기본 모델 인스턴스를 받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션이나 페이지네이션된 응답을 반환할 때는, 라우트나 컨트롤러에서 리소스 클래스가 제공하는 `collection` 메서드를 사용하여 리소스 인스턴스를 생성해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 경우 컬렉션과 함께 반환되어야 하는 커스텀 메타 데이터를 추가할 수 없습니다. 컬렉션 응답을 커스터마이징하려면 별도의 컬렉션 리소스를 만들어야 합니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함할 메타 데이터를 쉽게 정의할 수 있습니다:

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

컬렉션 리소스를 정의한 뒤에는 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지

라우트에서 리소스 컬렉션을 반환할 때 Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만 `preserveKeys` 속성을 리소스 클래스에 추가하면 컬렉션의 원래 키를 유지할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스 컬렉션의 키를 유지할지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys`가 `true`로 설정되면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 키가 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

보통 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 맵핑한 결과로 자동 채워집니다. 기본적으로 컬렉션 클래스 이름에서 `Collection` 부분을 제거한 이름이 단일 리소스 클래스 이름으로 간주됩니다. 또한 단일 리소스 클래스 이름이 `Resource`로 끝나거나 끝나지 않을 수 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스를 `UserResource`라는 리소스 클래스로 변환하려고 시도합니다. 이 동작을 변경하려면 리소스 컬렉션에서 `$collects` 속성을 재정의할 수 있습니다:

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
## 리소스 작성하기

> [!NOTE]
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 진행하기 전에 꼭 읽어보시길 권장합니다.

리소스는 단순히 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드를 포함합니다. 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다:

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

리소스를 정의한 후에는 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 연관관계 포현

응답에 연관된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드가 반환하는 배열에 연관된 리소스를 추가하면 됩니다. 예를 들어, 사용자의 블로그 게시글들을 포함하려면 `PostResource` 리소스의 `collection` 메서드를 사용합니다:

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
> 이미 로드된 경우에만 연관관계를 포함하려면 [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션 작성

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 별도의 컬렉션 리소스를 반드시 정의할 필요는 없습니다. 모든 리소스는 즉석에서 "ad-hoc" 컬렉션 리소스를 생성해주는 `collection` 메서드를 제공하기 때문입니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션 반환 시 메타 데이터를 커스터마이징해야 한다면, 직접 컬렉션 리소스를 정의하는 것이 필요합니다:

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

단일 리소스처럼, 컬렉션 리소스도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 최상위 리소스는 JSON으로 변환될 때 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

만약 최상위 리소스 래핑을 비활성화하고 싶다면, `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 일반적으로 이 메서드는 모든 요청 시 로드되는 `AppServiceProvider`나 다른 [서비스 프로바이더](/docs/master/providers)에서 호출하는 것이 좋습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 주며, 리소스 컬렉션 내에 직접 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스 래핑

리소스의 연관관계가 어떻게 래핑되는지는 전적으로 개발자 자유입니다. 모든 리소스 컬렉션을 중첩 여부와 상관없이 `data` 키로 래핑하려면, 각 리소스마다 컬렉션 클래스를 정의하고 데이터 배열을 `data` 키로 감싸서 반환하면 됩니다.

중첩되어도 최상위 리소스가 `data` 키 두 번으로 이중 래핑되지 않는지 걱정된다면, 걱정하지 않아도 됩니다. Laravel은 리소스의 이중 래핑을 자동으로 방지합니다:

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
#### 데이터 래핑과 페이지네이션

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는 `withoutWrapping` 메서드를 호출해도 Laravel이 `data` 키로 리소스 데이터를 래핑합니다. 이는 페이지네이션 응답에 항상 `meta`와 `links` 키가 포함되어 페이지네이터 상태 정보를 제공하기 때문입니다:

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

Laravel 페이지네이터 인스턴스를 리소스 컬렉션 생성 시 `collection` 메서드나 커스텀 컬렉션 생성자에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이지네이션된 응답은 항상 페이지네이터 상태 정보를 담은 `meta`와 `links` 키를 포함합니다:

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
#### 페이지네이션 정보 커스터마이징

`links` 또는 `meta` 키에 포함할 페이지네이션 정보를 커스터마이징하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 기본 `$default` 배열(여기에는 `links`와 `meta` 키가 포함됨)을 인수로 받습니다:

```php
/**
 * 페이지네이션 응답의 정보를 커스터마이징합니다.
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

때때로 특정 조건에 따라서만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 값을 포함시킬 수 있습니다. Laravel은 이를 돕는 다양한 헬퍼 메서드를 제공합니다. `when` 메서드를 사용하여 조건부로 속성을 추가할 수 있습니다:

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

이 예에서, 현재 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 경우에만 `secret` 키가 최종 리소스 응답에 포함됩니다. 만약 `false`라면, 클라이언트에 전송되기 전에 `secret` 키는 제거됩니다. `when` 메서드는 조건문 없이도 표현력 있게 리소스를 정의할 수 있도록 도와줍니다.

`when` 메서드는 두 번째 인수로 클로저(무명 함수)를 받아, 조건이 `true`일 경우에만 값을 계산하도록 할 수도 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 해당 속성이 실제로 존재할 경우에만 속성을 포함합니다:

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 속성이 null이 아닐 경우에 속성을 포함합니다:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

여러 속성이 같은 조건에서만 포함되어야 하는 경우, `mergeWhen` 메서드를 사용해서 조건이 참일 때만 여러 속성을 병합할 수 있습니다:

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

조건이 `false`인 경우, 이 속성들은 클라이언트에 전송되기 직전에 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 혼합된 배열 내에서는 사용하지 말아야 하며, 순차적이지 않은 숫자 키 배열에서도 사용하지 않아야 합니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성뿐 아니라, 관계도 조건부로 포함할 수 있습니다. 모델에 연관관계가 이미 로드되었을 때만 리소스 응답에 관계를 포함시켜, 컨트롤러가 어떤 관계를 로드할지 결정하고 리소스에서는 실제로 로드된 관계만 쉽게 포함하도록 하는 기능입니다. 이렇게 하면 리소스 내 N+1 쿼리 문제를 방지하는 데 도움이 됩니다.

`whenLoaded` 메서드는 연관관계가 로드된 경우에만 포함시키는 데 사용합니다. 이 메서드는 연관관계 객체 대신 관계 이름을 받아 불필요한 쿼리를 방지합니다:

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

관계가 로드되지 않았다면, 해당 키(`posts`)는 클라이언트로 전송되기 전에 자동으로 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 개수

연관관계를 포함하는 것 외에, 모델에 관계 개수가 로드되었을 때만 개수를 포함하도록 조건부로 처리할 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 관계 개수가 로드된 경우에만 해당 카운트 속성을 리소스 응답에 포함시킵니다. 관계 개수가 로드되지 않았으면 자동으로 제외합니다:

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

이 예에서는 `posts` 관계 개수가 로드되지 않았다면 `posts_count` 키가 제거됩니다.

또한, `avg`, `sum`, `min`, `max` 같은 집계함수 결과도 `whenAggregated` 메서드를 사용해 조건부로 로드할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 Pivot 정보

다대다 관계 중간 테이블의 데이터도 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드는 피벗 테이블 이름을 첫 번째 인수로 받고, 두 번째 인수로는 피벗 정보가 존재할 경우 반환할 값을 반환하는 클로저를 받습니다:

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

중간 테이블에 [커스텀 중간 테이블 모델](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, `whenPivotLoaded` 메서드의 첫 번째 인자로 모델 인스턴스를 넘길 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

피벗 데이터가 `pivot` 대신 다른 접근자를 사용하는 경우에는, `whenPivotLoadedAs` 메서드를 사용하세요:

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
### 메타 데이터 추가하기

일부 JSON API 표준은 리소스 혹은 리소스 컬렉션 응답에 메타 데이터 추가를 요구합니다. 보통 리소스나 관련 리소스에 대한 `links` 정보나, 리소스 자체에 대해 추가 정보가 포함됩니다. 리소스에 메타 데이터를 추가하고 싶으면 `toArray` 메서드 내에서 포함하면 됩니다. 예를 들어, 컬렉션에 `links` 정보를 포함할 수 있습니다:

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

리소스에서 추가 메타 데이터를 반환할 때 Laravel이 페이지네이션 응답에 자동으로 추가하는 `links` 혹은 `meta` 키를 덮어쓰거나 하지 않을까 걱정할 필요가 없습니다. 개발자가 정의한 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

가끔 리소스가 최상위 리소스인 경우에만 특정 메타 데이터를 포함시키고 싶을 수 있습니다. 이는 보통 응답 전체에 대한 메타 정보를 포함하는 용도입니다. 이런 메타 데이터를 정의하려면 리소스 클래스에 `with` 메서드를 추가합니다. 이 메서드는 해당 리소스가 최상위 리소스일 때만 포함되는 메타 데이터를 배열로 반환해야 합니다:

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
     * 리소스 배열과 함께 반환될 추가 데이터를 가져옵니다.
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
#### 리소스 생성 시 메타 데이터 추가하기

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 메타 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받습니다:

```php
return (new UserCollection(User::all()->load('roles')))
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

리소스는 이미 라우트나 컨트롤러에서 직접 반환할 수 있다는 것을 알았습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

하지만 때때로 JSON 응답을 클라이언트에 보내기 전에 HTTP 응답을 더 커스터마이징해야 할 때가 있습니다. 이를 처리하는 두 가지 방법이 있습니다. 먼저, 리소스에 `response` 메서드를 체이닝하는 방법입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 응답 헤더를 완전히 제어할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
        ->response()
        ->header('X-Value', 'True');
});
```

또는, 리소스 클래스에 `withResponse` 메서드를 정의할 수 있습니다. 리소스가 최상위 응답으로 반환될 때 이 메서드가 호출됩니다:

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
     * 리소스의 나가는 응답을 커스터마이징합니다.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```