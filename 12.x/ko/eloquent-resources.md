# Eloquent: API 리소스 (Eloquent: API Resources)

- [소개](#introduction)
- [리소스 생성](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 연관관계](#conditional-relationships)
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때 Eloquent 모델과 실제로 사용자에게 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자에게만 특정 속성을 보여주거나, 항상 특정 연관관계를 모델의 JSON 표현에 포함시키고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 표현력 있게 그리고 손쉽게 변환할 수 있도록 해줍니다.

물론 Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용해 언제든지 JSON으로 변환할 수 있습니다. 그러나 Eloquent 리소스를 사용하면 모델과 그 연관관계의 JSON 직렬화 과정을 훨씬 더 세밀하게 그리고 견고하게 제어할 수 있습니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 생성뿐만 아니라, 모델 컬렉션을 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함시킬 수 있습니다.

리소스 컬렉션을 생성하려면 리소스를 생성할 때 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel이 해당 리소스를 컬렉션 리소스로 생성함을 자동으로 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이 섹션은 리소스와 리소스 컬렉션에 대한 상위 수준 개요입니다. 리소스의 커스터마이징 및 제공되는 다양한 기능을 깊이 이해하려면 문서의 다른 섹션도 반드시 참고하시기 바랍니다.

자세한 기능에 들어가기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 상위 수준에서 살펴봅시다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 의미합니다. 예를 들어, 아래는 간단한 `UserResource` 리소스 클래스 예시입니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환될 속성 배열을 반환합니다.

모델의 속성은 `$this` 변수에서 바로 접근할 수 있다는 점에 주목하세요. 이는 리소스 클래스가 속성 및 메서드 접근을 자동으로 하위 모델로 프록시하여 편리하게 접근할 수 있도록 해주기 때문입니다. 리소스를 정의한 뒤에는 라우트나 컨트롤러에서 인스턴스를 생성해 바로 반환할 수 있습니다. 생성자에 모델 인스턴스를 전달하면 됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

편리하게 사용하려면, 모델의 `toResource` 메서드를 사용할 수도 있습니다. 이 메서드는 프레임워크의 규칙에 따라 자동으로 해당 모델의 리소스를 찾아 사용합니다.

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면, Laravel은 모델의 이름과 일치하고 `Resource` 접미사가 붙은 리소스를 해당 모델 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스 안에서 자동으로 탐색합니다.

<a name="resource-collections"></a>
### 리소스 컬렉션

만약 리소스의 컬렉션이나 페이지네이션 응답을 반환하려면, 라우트 혹은 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용해야 합니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는, 더욱 편리하게 사용하려면 Eloquent 컬렉션의 `toResourceCollection` 메서드를 활용할 수 있습니다. 이 메서드는 프레임워크 규칙에 따라 해당 모델의 리소스 컬렉션을 자동으로 찾아 반환합니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델의 이름과 일치하고 `Collection` 접미사가 붙은 리소스 컬렉션을 해당 모델 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스 안에서 탐색합니다.

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환할 추가 메타 데이터를 추가할 수 없습니다. 컬렉션 응답에 메타 데이터를 커스터마이즈하여 포함하려면, 컬렉션을 표현하는 별도 리소스 클래스를 생성해야 합니다.

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함시킬 메타 데이터를 쉽게 정의할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
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

리소스 컬렉션 정의 후, 라우트 또는 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다.

```php
return User::all()->toResourceCollection();
```

이렇게 하면, Laravel은 해당 모델 네임스페이스의 `Http\Resources` 안에서 모델 이름 + `Collection` 리소스 컬렉션을 자동으로 탐색합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

라우트에서 리소스 컬렉션을 반환할 때 Laravel은 컬렉션의 키를 숫자 순서로 재정렬합니다. 하지만 리소스 클래스에 `preserveKeys` 속성을 추가하면 컬렉션의 원래 키가 유지되도록 설정할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Indicates if the resource's collection keys should be preserved.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 속성이 `true`로 설정되면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 컬렉션의 키가 그대로 유지됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이즈

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 해당 단수 리소스 클래스에 매핑한 결과로 자동 채워집니다. 단수 리소스 클래스는 컬렉션 클래스 이름에서 마지막 `Collection` 부분을 뗀 형태로 가정하며, 필요에 따라 `Resource` 접미사가 있을 수도, 없을 수도 있습니다.

예를 들어, `UserCollection`은 주어진 User 인스턴스들을 `UserResource` 리소스에 매핑하려고 시도합니다. 이 동작을 커스터마이즈하려면 리소스 컬렉션의 `$collects` 속성을 오버라이드할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * The resource that this resource collects.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성

> [!NOTE]
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 섹션을 진행하기 전에 반드시 참고하세요.

리소스는 주어진 모델을 배열로 변환하기만 하면 됩니다. 즉, 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드를 포함하며, 이 배열을 애플리케이션의 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
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

리소스를 정의한 후에는, 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

응답에 관련 리소스를 포함시키고 싶을 때는, 리소스의 `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 아래 예시에서는 `PostResource`의 `collection` 메서드를 활용해 사용자의 블로그 게시글을 리소스 응답에 추가합니다.

```php
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

/**
 * Transform the resource into an array.
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
> 연관관계를 이미 로드한 경우에만 포함하고 싶다면 [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스는 개별 모델을 배열로 변환하는 반면, 리소스 컬렉션은 모델의 컬렉션 전체를 배열로 변환합니다. 모든 Eloquent 모델 컬렉션은 "즉석(ad-hoc)" 리소스 컬렉션을 손쉽게 생성할 수 있도록 `toResourceCollection` 메서드를 제공하므로, 모든 모델마다 별도로 리소스 컬렉션 클래스를 정의할 필요는 없습니다.

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

하지만 컬렉션에 반환할 메타 데이터를 커스터마이즈해야 한다면, 직접 리소스 컬렉션을 정의해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
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

단수 리소스와 마찬가지로, 컬렉션 리소스도 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있습니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드 호출 시, Laravel은 해당 모델 네임스페이스의 `Http\Resources` 안에서 모델 이름 + `Collection` 리소스 컬렉션을 자동으로 찾습니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 최상위 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 감싸집니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 아래와 같이 반환됩니다.

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

최상위 리소스의 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출하세요. 일반적으로 이 메서드는 `AppServiceProvider` 또는 모든 요청에 로드되는 [서비스 프로바이더](/docs/12.x/providers)에서 호출하는 것이 좋습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        JsonResource::withoutWrapping();
    }
}
```

> [!WARNING]
> `withoutWrapping` 메서드는 오직 최상위 응답에만 영향을 주며, 개발자가 직접 추가한 리소스 컬렉션의 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스 래핑

리소스의 연관관계 데이터가 어떻게 래핑될지는 완전히 자유롭게 결정할 수 있습니다. 모든 컬렉션 리소스를 항상 `data` 키로 래핑하고 싶다면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고 응답 배열에서 컬렉션을 `data` 키에 넣어 반환하세요.

혹시 이렇게 하면 최상위 리소스가 `data` 키로 두 번 래핑될까 걱정하실 수도 있습니다. 걱정하지 마세요! Laravel은 리소스가 중첩되어도 `data` 키가 중복되지 않도록 자동으로 처리합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
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

리소스 응답으로 페이지네이션된 컬렉션을 반환할 때에는, `withoutWrapping` 메서드를 호출했다 하더라도 Laravel이 리소스 데이터를 항상 `data` 키로 래핑합니다. 이는 페이지네이션 응답에 항상 `meta`와 `links` 키가 포함되기 때문입니다.

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

리소스 또는 커스텀 컬렉션에 Laravel의 페이지네이터 인스턴스를 전달할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는, 페이지네이터의 `toResourceCollection` 메서드를 사용하는 방법도 있습니다. 이 방식은 프레임워크 규칙에 따라 자동으로 모델의 컬렉션 리소스를 탐색합니다.

```php
return User::paginate()->toResourceCollection();
```

페이지네이션 응답에는 항상 페이지네이터 상태에 대한 정보를 담고 있는 `meta` 및 `links` 키가 포함됩니다.

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

페이지네이션 응답의 `links`나 `meta` 키에 포함된 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 정의하면 됩니다. 이 메서드는 `$paginated` 데이터와 기본 정보를 담고 있는 `$default` 배열(`links` 및 `meta` 키 포함)을 인자로 받습니다.

```php
/**
 * Customize the pagination information for the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array  $paginated
 * @param  array  $default
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

특정 조건이 만족될 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때에만 특정 값을 포함시키고 싶을 때가 있습니다. Laravel은 이런 상황에서 다양한 헬퍼 메서드를 제공합니다. `when` 메서드를 활용하면 조건부로 속성을 리소스 응답에 추가할 수 있습니다.

```php
/**
 * Transform the resource into an array.
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

위 예시에서, 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 `secret` 키가 리소스 응답에 포함됩니다. 만약 `false`면 `secret` 키는 응답에서 제거됩니다. `when` 메서드를 활용하면 직접 조건문을 배열 내부에 작성하지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

`when` 메서드는 두 번째 인자로 클로저도 받을 수 있으므로, 특정 조건이 참일 때만 값을 계산하도록 할 수도 있습니다.

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 기본 모델에 실제로 해당 속성이 존재할 때만 속성을 응답에 포함합니다.

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 속성이 null이 아닐 경우에만 속성을 포함시킵니다.

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

어떤 경우에는 같은 조건에 따라 여러 속성을 리소스 응답에 포함해야 할 수도 있습니다. 이때는 `mergeWhen` 메서드를 사용하여, 주어진 조건이 `true`일 때만 여러 속성을 한꺼번에 응답에 포함시킬 수 있습니다.

```php
/**
 * Transform the resource into an array.
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

조건이 `false`인 경우, 이 속성들은 클라이언트에 응답하기 전에 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 혼합된 배열이나, 순차적으로 정렬되지 않은 숫자 키의 배열 안에서는 사용하지 마세요.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성 값을 조건부로 포함시키는 것 외에도, 모델에서 연관관계를 이미 로드했는지 여부에 따라 연관관계를 조건부로 리소스 응답에 포함시킬 수 있습니다. 이를 통해 컨트롤러에서 어떤 연관관계를 로드할지 결정하고, 리소스에서는 실제로 로드된 경우에만 포함시킬 수 있습니다. 궁극적으로 리소스 내부에서 "N+1" 쿼리 문제를 손쉽게 피할 수 있습니다.

`whenLoaded` 메서드는 연관관계가 이미 로드된 경우에만 이를 포함시킵니다. 이 메서드는 불필요한 연관관계 로드를 피하기 위해 연관관계 자체가 아니라 연관관계의 이름을 인자로 받습니다.

```php
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
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

위 예시에서, 해당 연관관계가 로드되지 않은 경우 `posts` 키는 클라이언트에 응답되기 전에 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트

연관관계를 조건부로 포함하는 것 외에도, 연관관계의 "카운트"가 로드된 경우에만 조건적으로 응답에 포함시킬 수 있습니다.

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계의 카운트가 존재할 때만 이를 리소스 응답에 포함시킵니다. 만약 카운트 정보가 없으면 해당 속성은 포함되지 않습니다.

```php
/**
 * Transform the resource into an array.
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

이 예시에서, `posts` 연관관계의 카운트가 로드되지 않았다면 `posts_count` 키는 응답에서 제거됩니다.

그 외에도 `avg`, `sum`, `min`, `max` 등의 집계 값도 `whenAggregated` 메서드를 사용해서 조건부로 로드할 수 있습니다.

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗(pivot) 정보

연관관계 정보뿐만 아니라, 다대다(many-to-many) 연관관계의 중간 테이블(pivot) 데이터도 `whenPivotLoaded` 메서드를 사용해 조건부로 리소스 응답에 포함시킬 수 있습니다. 첫 번째 인자로 피벗 테이블 이름을, 두 번째 인자로 클로저(피벗 정보가 있을 시 반환할 값을 반환)를 전달하면 됩니다.

```php
/**
 * Transform the resource into an array.
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

연관관계에서 [커스텀 중간 테이블 모델](/docs/12.x/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, 첫 번째 인자로 중간 테이블 모델 인스턴스를 전달할 수 있습니다.

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

그리고 중간 테이블이 `pivot` 이외의 접근자를 사용하는 경우, `whenPivotLoadedAs` 메서드를 활용할 수도 있습니다.

```php
/**
 * Transform the resource into an array.
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

일부 JSON API 표준은 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가하도록 요구합니다. 여기에는 리소스 자체나 관련 리소스에 대한 `links`, 또는 해당 리소스의 메타 데이터 등이 포함될 수 있습니다. 리소스에 추가적인 메타 데이터를 반환해야 한다면, `toArray` 메서드에서 이를 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 링크 정보를 포함시킬 수 있습니다.

```php
/**
 * Transform the resource into an array.
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

리소스에서 추가적인 메타 데이터를 반환할 경우, 페이지네이션 응답에서 자동으로 추가되는 `links` 나 `meta` 키와 충돌을 걱정할 필요는 없습니다. 추가적으로 정의한 `links` 정보는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

경우에 따라, 최상위 리소스 응답에만 메타 데이터를 포함시키고 싶을 수 있습니다. 이는 주로 전체 응답에 관한 메타 정보일 때 사용됩니다. 이 메타 데이터를 정의하려면 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 리소스가 최상위로 변환될 때에만 추가할 메타 데이터 배열을 반환해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return parent::toArray($request);
    }

    /**
     * Get additional data that should be returned with the resource array.
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

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 응답에 추가할 데이터를 배열로 받아들입니다.

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

앞서 본 것처럼, 리소스는 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 때로는 클라이언트에 응답이 전송되기 전 HTTP 응답을 커스터마이즈해야 할 수도 있습니다. 이를 위한 방법은 다음 두 가지가 있습니다. 첫째, 리소스에서 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하여 응답의 헤더 등을 직접 제어할 수 있도록 해줍니다.

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

혹은, 리소스 내부에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 최상위 응답으로 반환될 때 호출됩니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
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
     * Customize the outgoing response for the resource.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```