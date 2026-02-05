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

API를 구축할 때, Eloquent 모델과 애플리케이션 사용자에게 실제로 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 그룹에는 일부 속성만 표시하고 싶거나, 항상 모델의 특정 연관관계를 JSON 표현에 포함하고 싶을 때가 있습니다. Eloquent의 리소스 클래스는 모델 및 모델 컬렉션을 JSON으로 변환하는 작업을 표현력 있게, 그리고 쉽게 할 수 있도록 지원합니다.

물론, Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용해 언제든지 JSON으로 변환할 수 있습니다. 그러나 Eloquent 리소스는 모델과 연관관계의 JSON 직렬화 과정을 훨씬 더 세밀하고 강력하게 제어할 수 있도록 해줍니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용하세요. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 외에도, 모델 컬렉션을 변환하는 역할을 하는 리소스를 생성할 수도 있습니다. 이를 통해 JSON 응답에 컬렉션 전체와 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면 리소스 생성 시 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection` 단어를 포함하면 Laravel은 해당 리소스가 컬렉션 리소스임을 자동으로 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이는 리소스와 리소스 컬렉션에 대한 상위 개념 설명입니다. 리소스의 커스터마이징 및 사용의 강력함에 대해 더 깊이 이해하려면 아래의 다른 섹션을 꼭 읽어보시기 바랍니다.

리소스를 작성할 때 사용할 수 있는 모든 옵션을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 전체적으로 알아봅시다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스를 응답으로 반환할 때 JSON으로 변환되는 속성 배열을 반환합니다.

모델의 속성에 `$this`로 바로 접근할 수 있다는 점에 주목하세요. 이는 리소스 클래스가 속성 및 메서드 접근을 자동으로 내부 모델로 프록시 처리하기 때문입니다. 리소스를 정의한 뒤에는 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다. 리소스는 생성자를 통해 내부 모델 인스턴스를 전달받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

좀 더 편리하게, 모델의 `toResource` 메서드를 사용할 수 있는데, 이는 프레임워크의 규칙에 따라 모델과 연결된 리소스를 자동으로 찾아 사용합니다:

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면, Laravel은 모델 이름과 일치하고 `Resource` 접미사가 붙은 리소스가 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에 있는지 찾으려고 시도합니다.

리소스 클래스가 이 네이밍 규칙을 따르지 않거나 다른 네임스페이스에 있는 경우, `UseResource` 속성을 사용해 해당 모델의 기본 리소스를 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserResource;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResource;

#[UseResource(CustomUserResource::class)]
class User extends Model
{
    // ...
}
```

또는, `toResource` 메서드에 리소스 클래스를 직접 전달하여 지정할 수도 있습니다:

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스의 컬렉션이나 페이지네이션된 결과를 반환하려면, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하세요:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

혹은, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용하면, 프레임워크가 규칙에 따라 모델의 리소스 컬렉션을 자동으로 찾아 사용합니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`이 접미사로 붙은 리소스 컬렉션이 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에 있는지 찾으려고 시도합니다.

리소스 컬렉션 클래스가 네이밍 규칙을 따르지 않거나 다른 네임스페이스에 위치한다면, `UseResourceCollection` 속성을 사용해 모델의 기본 리소스 컬렉션을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserCollection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResourceCollection;

#[UseResourceCollection(CustomUserCollection::class)]
class User extends Model
{
    // ...
}
```

또는, `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 직접 전달하여 지정할 수 있습니다:

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로, 리소스 컬렉션은 컬렉션과 함께 반환할 추가적인 커스텀 메타 데이터를 허용하지 않습니다. 컬렉션 응답을 커스터마이징하려면, 컬렉션을 표현할 별도의 리소스를 생성하면 됩니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스를 생성했다면, 응답에 포함할 메타 데이터를 자유롭게 정의할 수 있습니다:

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

리소스 컬렉션을 정의한 후에는 라우트나 컨트롤러에서 다음과 같이 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 이용해, 규칙에 따라 자동으로 리소스 컬렉션을 찾도록 할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection` 접미사가 붙은 리소스 컬렉션이 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에 있는지 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 0부터 순차적인 숫자 형태로 재설정합니다. 그러나 리소스 클래스에 `preserveKeys` 속성을 추가하여 컬렉션의 원래 키를 보존할지 여부를 지정할 수 있습니다:

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

`preserveKeys` 속성을 `true`로 설정하면, 컬렉션을 라우트나 컨트롤러에서 반환할 때 컬렉션의 키가 원래 형태로 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 리소스 클래스 커스터마이징

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 채워집니다. 이때 단일 리소스 클래스는 컬렉션 클래스 이름에서 마지막 `Collection`을 뺀 이름으로 인식되며, 사용자의 취향에 따라 이 이름에 `Resource` 접미사가 붙을 수도 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스들을 `UserResource` 리소스로 매핑합니다. 이 동작을 커스터마이징하려면, 리소스 컬렉션의 `$collects` 속성을 오버라이드하세요:

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
> [개념 개요](#concept-overview) 섹션을 먼저 읽어보시길 적극 권장합니다.

리소스는 주어진 모델을 배열로 변환하는 역할만 수행하면 됩니다. 따라서 각 리소스는 모델의 속성을 API에 적합한 배열로 바꾸는 `toArray` 메서드를 포함하고 있으며, 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있습니다:

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

리소스를 정의한 후에는 다음과 같이 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

응답에 연관된 리소스를 포함하고 싶을 때는, 리소스의 `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 예를 들어, 사용자의 블로그 게시물을 `PostResource`의 `collection` 메서드를 사용해 리소스 응답에 추가할 수 있습니다:

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
> 연관관계를 이미 로드한 경우에만 포함하고 싶다면 [조건부 연관관계](#conditional-relationships) 관련 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

개별 리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델 컬렉션 전체를 배열로 변환합니다. 모든 Eloquent 모델 컬렉션은 `toResourceCollection` 메서드를 제공하므로, 각 모델별로 별도의 리소스 컬렉션 클래스를 꼭 작성하지 않아도 "즉석(ad-hoc)" 리소스 컬렉션을 쉽게 만들 수 있습니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

하지만 컬렉션과 함께 반환되는 메타 데이터를 커스터마이즈해야 한다면, 리소스 컬렉션 클래스를 직접 정의해야 합니다:

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

단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

혹은, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용해, 모델의 리소스 컬렉션을 규칙에 따라 자동으로 찾아 반환할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델 이름과 일치하며 `Collection`이 접미사로 붙은 리소스 컬렉션이 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에 있는지 찾으려고 시도합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 리소스 응답이 JSON으로 변환될 때 가장 바깥쪽의 리소스는 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

가장 바깥쪽 리소스의 래핑을 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출하면 됩니다. 보통 이 메서드는 `AppServiceProvider` 또는 모든 요청마다 로드되는 [서비스 프로바이더](/docs/master/providers)에서 호출하는 것이 일반적입니다:

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
> `withoutWrapping` 메서드는 가장 바깥쪽 응답에만 영향을 주며, 리소스 컬렉션에서 직접 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스의 래핑

리소스의 연관관계를 어떻게 래핑할지는 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 언제나 `data` 키로 래핑하려면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고 `data` 키 안에 컬렉션을 반환하면 됩니다.

혹시 이렇게 하면 최상위 리소스가 이중(`data` 키가 두 번) 래핑되는지 궁금할 수 있겠지만, Laravel은 결코 리소스를 이중 래핑되도록 하지 않으므로 리소스 컬렉션의 중첩 수준을 신경 쓸 필요가 없습니다:

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

리소스 응답으로 페이지네이션된 컬렉션을 반환할 경우, `withoutWrapping` 메서드를 호출했다 하더라도 Laravel은 리소스 데이터를 여전히 `data` 키로 래핑합니다. 이는 페이지네이션 응답이 항상 `meta` 및 `links` 키와 페이지네이터 상태 정보를 포함하기 때문입니다:

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

리소스 또는 커스텀 리소스 컬렉션의 `collection` 메서드에 Laravel의 페이지네이터 인스턴스를 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는 페이지네이터의 `toResourceCollection` 메서드를 사용하면, 프레임워크에서 규칙에 따라 페이지네이션된 모델의 리소스 컬렉션을 자동으로 찾아줍니다:

```php
return User::paginate()->toResourceCollection();
```

페이지네이션 응답은 항상 페이지네이터 상태 정보를 담고 있는 `meta` 및 `links` 키를 포함합니다:

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

페이지네이션 응답의 `links` 또는 `meta` 키에 포함되는 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 정의하면 됩니다. 이 메서드는 `$paginated` 데이터와, `links` 및 `meta` 키가 포함된 `$default` 배열을 전달받습니다:

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

특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하고 싶을 때가 있습니다. Laravel은 이런 상황을 위해 다양한 헬퍼 메서드를 제공합니다. 그 중 `when` 메서드는 조건부로 리소스 응답에 속성을 추가하는 데 사용할 수 있습니다:

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

위 예시에서, 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 `secret` 키가 포함됩니다. `false`일 경우에는 해당 키가 리소스 응답에서 제거된 채 클라이언트로 전송됩니다. `when` 메서드를 사용하면, 배열을 빌드할 때 조건문 없이 직관적으로 리소스를 정의할 수 있습니다.

또한, `when` 메서드는 두 번째 인자로 클로저를 받을 수 있기 때문에, 조건이 `true`일 때만 결과값을 계산하도록 작성할 수도 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 내부 모델에 해당 속성이 실제로 존재할 때만 포함할 수 있도록 해줍니다:

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 속성 값이 null이 아닐 때만 리소스 응답에 포함하도록 할 수 있습니다:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

조건이 동일할 때 여러 속성을 응답에 포함하고 싶다면, `mergeWhen` 메서드를 사용하면 됩니다. 해당 조건이 `true`일 때만 속성들이 응답에 병합됩니다:

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

조건이 `false`일 경우, 해당 속성들은 클라이언트로 응답을 전송하기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열과 숫자 키가 혼합된 배열이나, 순서가 맞지 않는 숫자 키가 존재하는 배열에서는 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성뿐 아니라, 모델에 연관관계가 로드되어 있는지에 따라 리소스 응답에 연관관계를 포함할지 여부도 조건부로 제어할 수 있습니다. 이를 통해 컨트롤러가 어떤 연관관계를 로드할지 결정하고, 리소스는 로드된 연관관계만 포함할 수 있게 됩니다. 결과적으로 리소스 내에서 "N+1" 쿼리 문제를 쉽게 방지할 수 있습니다.

`whenLoaded` 메서드는 연관관계를 조건부로 응답에 포함할 때 사용할 수 있습니다. 불필요한 연관관계 조회를 피하기 위해, 이 메서드는 연관관계 객체가 아니라 관계의 이름을 받습니다:

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

위 예시에서, 연관관계가 로드되지 않았다면 `posts` 키가 클라이언트로 전송되기 전 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트

연관관계 자체뿐만 아니라, 모델에 연관관계의 "카운트"가 로드되어 있는지에 따라 리소스 응답에 카운트 정보를 포함할 수도 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계의 카운트가 존재할 때만 리소스 응답에 포함할 수 있도록 도와줍니다. 이 메서드는 연관관계의 카운트가 없으면 불필요하게 속성이 포함되는 것을 방지합니다:

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

`posts` 연관관계의 카운트가 로드되지 않았다면, `posts_count` 키는 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max` 등 다른 종류의 집계도 `whenAggregated` 메서드로 조건부로 응답에 포함시킬 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

리소스 응답에 연관관계 정보뿐만 아니라, 다대다 관계 중간 테이블(피벗 테이블)의 데이터도 조건부로 포함할 수 있습니다. 이를 위해 `whenPivotLoaded` 메서드를 사용합니다. 이 메서드는 첫 번째 인수로 피벗 테이블의 이름을 받고, 두 번째 인수는 피벗 정보가 모델에 있을 때 반환할 값을 반환하는 클로저입니다:

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

연관관계가 [커스텀 중간 테이블 모델](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용할 경우에는, 첫 번째 인수로 중간 테이블 모델 인스턴스를 넘길 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 기본 `pivot`이 아닌 다른 접근자를 사용할 때는, `whenPivotLoadedAs` 메서드를 이용합니다:

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

일부 JSON API 표준은 리소스와 리소스 컬렉션 응답에 메타 데이터 추가를 요구합니다. 여기에는 리소스 자체나 연관 리소스로의 `links`, 또는 리소스에 대한 메타 데이터 등이 포함될 수 있습니다. 만약 리소스에 추가 메타 데이터를 반환하고 싶다면, `toArray` 메서드에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 추가할 수 있습니다:

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

리소스에서 추가 메타 데이터를 반환할 때는, 페이지네이션 응답에서 Laravel이 자동으로 추가해주는 `links`나 `meta` 키와 충돌하는지 걱정할 필요가 없습니다. 추가로 정의한 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

리소스가 최상위 리소스로 반환될 때만 특정 메타 데이터를 추가하고 싶은 경우도 있습니다. 보통 응답 전체에 대한 일반적인 메타 정보 등이 이에 해당합니다. 이 경우, 리소스 클래스에 `with` 메서드를 정의하세요. 이 메서드는 오직 리소스가 최상위로 변환될 때만 응답에 포함될 메타 데이터 배열을 반환합니다:

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
#### 리소스 인스턴스 생성 시 메타 데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 리소스 응답에 추가되어야 할 데이터를 배열로 받습니다:

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

지금까지 읽으셨듯이, 리소스는 라우트와 컨트롤러에서 바로 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만, 때로는 클라이언트에 응답을 보내기 전에 HTTP 응답을 커스터마이징해야 할 필요도 있습니다. 두 가지 방법이 있습니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더 등을 자유롭게 제어할 수 있습니다:

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

또 다른 방법으로, 리소스 클래스 내부에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 응답에서 최상위로 반환될 때 호출됩니다:

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
