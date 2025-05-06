# Eloquent: API 리소스

- [소개](#introduction)
- [리소스 생성](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 관계](#conditional-relationships)
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자에게만 특정 속성을 표시하거나, 모델의 JSON 표현에 항상 특정 관계를 포함시키고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 표현력 있게, 쉽게 JSON으로 변환할 수 있게 해줍니다.

물론 Eloquent 모델이나 컬렉션을 그들의 `toJson` 메소드로 항상 JSON으로 변환할 수도 있습니다. 하지만, Eloquent 리소스는 모델 및 그 관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` 아티즌 명령어를 사용할 수 있습니다. 기본적으로, 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델의 컬렉션을 변환하는 책임을 지는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 전체 컬렉션과 관련된 링크 및 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스를 생성해야 함을 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이것은 리소스 및 리소스 컬렉션에 대한 높은 수준의 개요입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 보다 심도 있게 이해하려면 이 문서의 다른 섹션을 읽어 보시기 바랍니다.

리소스를 작성할 때 사용할 수 있는 모든 옵션에 대해 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 높은 수준에서 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 할 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 리소스가 라우트 또는 컨트롤러 메서드에서 반환될 때 JSON으로 변환되어야 하는 속성 배열을 반환하는 `toArray` 메서드를 정의합니다.

모델 속성은 `$this` 변수로 직접 접근할 수 있습니다. 이는 리소스 클래스가 속성 및 메서드 접근을 편리하게 기본 모델에 프록시하기 때문입니다. 리소스를 정의한 후에는, 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자를 통해 모델 인스턴스를 전달받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스의 컬렉션이나 페이지네이션된 응답을 반환하려는 경우, 라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 리소스 클래스가 제공하는 `collection` 메소드를 사용해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 방식은 컬렉션과 함께 반환해야 할 커스텀 메타 데이터를 추가할 수는 없습니다. 컬렉션 리소스 응답을 커스터마이즈하고 싶다면, 컬렉션을 나타내는 전용 리소스를 생성할 수 있습니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함시킬 메타 데이터를 쉽게 정의할 수 있습니다:

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

리소스 컬렉션을 정의한 후, 라우트나 컨트롤러에서 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존하기

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 그러나 리소스 클래스에 컬렉션의 원래 키를 보존할지를 나타내는 `preserveKeys` 속성을 추가할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스의 컬렉션 키를 보존할지 여부를 나타냅니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 속성이 `true`로 설정된 경우, 컬렉션이 라우트나 컨트롤러에서 반환될 때 컬렉션 키가 그대로 보존됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

일반적으로, 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단수 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단수 리소스 클래스는 컬렉션 리소스 클래스 이름에서 끝의 `Collection` 부분을 제거한 이름으로 간주됩니다. 또한, 개인 취향에 따라 단수 리소스 클래스에 `Resource` 접미사를 붙일 수도, 붙이지 않아도 됩니다.

예를 들어, `UserCollection`은 전달된 User 인스턴스를 `UserResource` 리소스로 매핑하려고 시도합니다. 이 동작을 커스터마이즈하려면, 리소스 컬렉션의 `$collects` 속성을 오버라이드할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스가 수집하는 리소스입니다.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성

> [!NOTE]
> [개념 개요](#concept-overview)를 먼저 읽은 뒤 이 문서를 계속 읽는 것이 좋습니다.

리소스는 주어진 모델을 배열로 변환하는 작업만 하면 됩니다. 즉, 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메소드를 포함하고 있으며, 이를 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다:

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

리소스를 정의한 후에는, 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 관계

응답에 관련 리소스를 포함하고 싶은 경우, 리소스의 `toArray` 메소드에서 반환하는 배열에 추가하면 됩니다. 이 예제에서는 `PostResource` 리소스의 `collection` 메소드를 사용해 사용자의 블로그 포스트를 응답에 포함합니다:

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
> 관계를 이미 로드한 경우에만 포함하고자 한다면 [조건부 관계](#conditional-relationships) 문서를 참조하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 모델의 컬렉션을 배열로 변환합니다. 모든 모델마다 리소스 컬렉션 클래스를 정의할 필요는 없습니다. 모든 리소스는 "즉석"으로 리소스 컬렉션을 생성할 수 있는 `collection` 메소드를 제공합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션과 함께 반환할 메타 데이터를 커스터마이즈하려면, 자체 리소스 컬렉션을 정의해야 합니다:

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

단수 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 가장 바깥쪽의 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

가장 바깥쪽 리소스의 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메소드를 호출하면 됩니다. 보통 이 메소드는 `AppServiceProvider`나 모든 요청마다 로드되는 다른 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출해야 합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 모든 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> `withoutWrapping` 메소드는 오직 최상위 응답에만 영향을 주며, 직접 리소스 컬렉션에 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 관계가 어떻게 래핑될지는 완전히 자유롭게 결정할 수 있습니다. 중첩 수준과 상관없이 모든 리소스 컬렉션을 `data` 키로 래핑하고 싶다면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고, 컬렉션을 `data` 키 안에 반환하면 됩니다.

이렇게 하면 최상위 리소스가 두 개의 `data` 키로 래핑되는지 궁금할 수 있습니다. 걱정하지 마세요. Laravel은 리소스가 두 번 래핑되는 것을 방지하므로, 변환하는 리소스 컬렉션의 중첩 수준에 대해 염려할 필요가 없습니다:

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
#### 데이터 래핑 & 페이지네이션

리소스 응답을 통해 페이지네이션된 컬렉션을 반환할 때, `withoutWrapping` 메소드를 호출했더라도 Laravel은 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이션 응답에는 항상 페이지네이터 상태 정보를 담은 `meta` 및 `links` 키가 포함되기 때문입니다:

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

리소스의 `collection` 메소드나 커스텀 리소스 컬렉션에 Laravel 페이지네이터 인스턴스를 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이지네이션 응답에는 항상 페이지네이터 상태 정보를 담은 `meta` 및 `links` 키가 포함됩니다:

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
#### 페이지네이션 정보 커스터마이즈

페이지네이션 응답의 `links`나 `meta` 키에 포함되는 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `links` 및 `meta` 키가 포함된 `$default` 정보 배열을 받습니다:

```php
/**
 * 리소스의 페이지네이션 정보를 커스터마이즈합니다.
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

때때로, 특정 조건이 충족될 때에만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 “관리자” 일 때만 값을 포함하고 싶을 때가 있습니다. Laravel은 이를 지원하기 위한 다양한 헬퍼 메소드를 제공합니다. `when` 메소드를 사용하면 조건부로 속성을 리소스 응답에 추가할 수 있습니다:

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

이 예시에서, 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 `secret` 키가 리소스 응답에 포함됩니다. `false`이면, 클라이언트에게 전송되기 전에 `secret` 키가 제거됩니다. `when` 메소드는 배열을 작성할 때 조건문을 사용하지 않고도 리소스를 표현력있게 정의할 수 있습니다.

`when` 메소드는 두 번째 인수로 클로저도 받을 수 있어, 조건이 `true`일 때만 결과 값을 계산할 수 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메소드는 기본 모델에 속성이 실제로 존재할 때만 속성을 포함합니다:

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메소드는 속성 값이 null이 아닐 때만 리소스 응답에 속성을 포함시킵니다:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

동일한 조건에 따라 여러 속성을 리소스 응답에 포함시켜야 할 때가 있습니다. 이땐, `mergeWhen` 메소드를 사용해 조건이 `true`일 때만 여러 속성을 응답에 추가할 수 있습니다:

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

역시, 조건이 `false`면 클라이언트로 전송되기 전에 이 속성들은 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메소드는 문자열과 숫자 키가 혼합된 배열 내, 또는 순차적으로 정렬되지 않은 숫자 키 배열 내에서 사용해서는 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 관계

속성만이 아니라, 모델에 이미 관계가 로드되어 있는 경우에만 리소스 응답에 관계를 조건부로 포함시킬 수 있습니다. 이를 통해 컨트롤러가 어떤 관계를 로드할지 결정하고, 리소스는 실제로 로드되었을 때만 포함시킬 수 있습니다. 결과적으로, 리소스 내에서 "N+1" 쿼리 문제를 더 쉽게 방지할 수 있습니다.

`whenLoaded` 메소드를 사용하여 관계를 조건부로 포함할 수 있습니다. 명시적으로 관계 전체가 아닌, 관계 이름만 전달하여 불필요한 로드를 방지합니다:

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

이 예시에서, 관계가 로드되지 않았다면 `posts` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 카운트

관계 자체뿐 아니라, 모델에 관계의 개수가 로드되어 있는 경우에만 관계의 "카운트"를 리소스 응답에 조건부로 포함할 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메소드를 이용하면, 관계의 카운트가 존재하는 경우에만 해당 정보를 리소스 응답에 포함시킬 수 있습니다:

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

이 예시에서, `posts` 관계의 카운트가 로드되어 있지 않으면 `posts_count` 키가 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max`와 같은 집계 값도 `whenAggregated` 메소드로 조건부로 로드할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 Pivot 정보

또한, 다대다(many-to-many) 관계의 중간 테이블에서 데이터가 모델에 존재하는 경우에만 이를 리소스 응답에 조건부로 포함시킬 수 있습니다. `whenPivotLoaded` 메소드는 첫 번째 인수로 피벗 테이블의 이름을 받으며, 두 번째 인수로 클로저를 받아 피벗 정보가 모델에 있는 경우 반환할 값을 지정합니다:

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

[커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, `whenPivotLoaded`의 첫 번째 인수로 중간 테이블 모델 인스턴스를 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 `pivot` 이외의 접근자를 사용하는 경우, `whenPivotLoadedAs` 메소드를 사용할 수 있습니다:

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
### 메타 데이터 추가

일부 JSON API 표준은 리소스 및 리소스 컬렉션 응답에 메타 데이터 추가를 요구합니다. 이에는 일반적으로 리소스나 관련 리소스로의 `links` 또는 리소스 자체에 대한 메타 데이터가 포함됩니다. 메타 데이터를 추가로 반환하려면, `toArray` 메소드에서 포함하면 됩니다. 예를 들어, 리소스 컬렉션 변환시 `links` 정보를 포함할 수 있습니다:

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

리소스에서 추가 메타 데이터를 반환할 때, 페이지네이션 응답 시 Laravel이 자동으로 추가하는 `links`나 `meta` 키를 실수로 덮어쓸 염려는 없습니다. 직접 정의한 모든 추가 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

가끔 리소스가 최상위로 반환될 때만 특정 메타 데이터를 포함시키고 싶을 수 있습니다. 보통 이는 응답 전체에 대한 메타 정보입니다. 이를 정의하려면, 리소스 클래스에 `with` 메소드를 추가하세요. 이 메소드는 리소스가 변환되는 최상위 리소스인 경우에만 리소스 응답에 포함할 메타 데이터 배열을 반환해야 합니다:

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
#### 리소스 생성 시 메타 데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때, 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에 제공되는 `additional` 메소드는 리소스 응답에 추가할 데이터를 배열로 전달받습니다:

```php
return (new UserCollection(User::all()->load('roles')))
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

앞서 언급한 대로, 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

그러나, 클라이언트로 전송되기 전에 HTTP 응답을 커스터마이즈해야 할 때가 있습니다. 이를 위한 두 가지 방법이 있습니다. 첫째, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 응답 헤더를 자유롭게 제어할 수 있습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
        ->response()
        ->header('X-Value', 'True');
});
```

또 다른 방법으로, 리소스 클래스 내에 `withResponse` 메소드를 정의할 수 있습니다. 이 메소드는 리소스가 응답에서 최상위 리소스로 반환될 때 호출됩니다:

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
     * 리소스의 응답을 커스터마이즈합니다.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```
