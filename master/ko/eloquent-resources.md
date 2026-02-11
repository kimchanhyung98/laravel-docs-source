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
- [JSON:API 리소스](#jsonapi-resources)
    - [JSON:API 리소스 생성](#generating-jsonapi-resources)
    - [속성 정의](#defining-jsonapi-attributes)
    - [연관관계 정의](#defining-jsonapi-relationships)
    - [리소스 타입 및 ID](#jsonapi-resource-type-and-id)
    - [희소 필드셋 및 포함](#jsonapi-sparse-fieldsets-and-includes)
    - [링크 및 메타](#jsonapi-links-and-meta)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때는 Eloquent 모델과 실제로 사용자에게 반환되는 JSON 응답 사이에 변환 계층이 필요할 수 있습니다. 예를 들어, 특정 사용자 그룹에는 일부 속성만 표시하고, 다른 사용자에는 표시하지 않거나, 모델의 JSON 표현에 항상 특정 연관관계를 포함하도록 할 수도 있습니다. Eloquent의 리소스 클래스는 여러분의 모델과 컬렉션을 JSON으로 쉽게 변환할 수 있도록 명확하고 효율적인 방법을 제공합니다.

물론, 항상 Eloquent 모델이나 컬렉션에서 `toJson` 메서드를 사용해 직접 JSON 형태로 변환할 수도 있습니다. 하지만 Eloquent 리소스를 사용하면, 모델과 그 연관관계의 JSON 직렬화를 더욱 세밀하고 강력하게 제어할 수 있습니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용합니다. 기본적으로 생성된 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 위치하게 됩니다. 각 리소스 클래스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

단일 모델을 변환하는 리소스 외에도, 여러 모델의 컬렉션을 변환하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 해당 리소스 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함시킬 수 있습니다.

리소스 컬렉션을 만들려면 리소스 생성 시 `--collection` 플래그를 사용하면 됩니다. 또는, 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel이 컬렉션 리소스를 생성해야 함을 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이 부분은 리소스 및 리소스 컬렉션에 대한 개괄적인 안내입니다. 리소스의 확장성과 커스터마이징에 대해 더 깊이 이해하려면 문서의 다른 섹션도 꼭 참고하시기 바랍니다.

다양한 커스터마이징 방법을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 전반적으로 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환할 단일 모델을 나타냅니다. 예를 들어, 아래는 간단한 `UserResource` 리소스 클래스입니다.

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 해당 리소스가 라우트 또는 컨트롤러에서 응답으로 반환될 때 JSON으로 변환할 속성 배열을 반환합니다.

여기서 `$this`를 통해 모델의 속성에 바로 접근할 수 있는데, 이는 리소스 클래스가 내부적으로 해당 모델에 대한 속성 및 메서드 접근을 자동으로 위임(proxy)하기 때문입니다. 이렇게 정의한 리소스는 라우트 또는 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자에 해당 모델 인스턴스를 전달받아 동작합니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

더 편리하게, 모델의 `toResource` 메서드를 사용할 수도 있습니다. 이 메서드는 프레임워크의 규칙에 따라 자동으로 해당 모델의 리소스를 찾아줍니다.

```php
return User::findOrFail($id)->toResource();
```

`toResource` 메서드를 호출하면, Laravel은 모델명과 일치하고 선택적으로 `Resource`로 끝나는 리소스 클래스를 모델의 네임스페이스와 가까운 `Http\Resources` 네임스페이스 내에서 찾으려 시도합니다.

리소스 클래스가 이 규칙을 따르지 않거나 다른 네임스페이스에 있다면, `UseResource` 속성(attribute)을 이용하여 모델의 기본 리소스를 명시할 수 있습니다.

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

또는 `toResource` 메서드에 리소스 클래스를 직접 전달할 수도 있습니다.

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```

<a name="resource-collections"></a>
### 리소스 컬렉션

여러 리소스의 컬렉션이나 페이지네이션된 응답을 반환할 때는, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하는 것이 좋습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는 더 간편하게, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다. 이 메서드는 프레임워크의 규칙에 따라 모델에 알맞은 리소스 컬렉션을 자동으로 찾아줍니다.

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델명과 일치하고 `Collection`으로 끝나는 리소스 컬렉션 클래스를 모델의 네임스페이스와 가까운 `Http\Resources` 네임스페이스 내에서 찾으려 시도합니다.

리소스 컬렉션 클래스가 이 규칙을 따르지 않거나 다른 네임스페이스에 있다면, `UseResourceCollection` 속성을 이용해 모델의 기본 리소스 컬렉션을 명시할 수 있습니다.

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

또한, `toResourceCollection` 메서드에 리소스 컬렉션 클래스를 직접 전달할 수도 있습니다.

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로, 리소스 컬렉션은 컬렉션과 함께 반환되어야 할 커스텀 메타 데이터를 직접 추가하는 것을 지원하지 않습니다. 컬렉션 응답을 커스터마이즈하고 싶다면, 컬렉션을 나타내는 전용 리소스를 생성해 활용할 수 있습니다.

```shell
php artisan make:resource UserCollection
```

생성된 리소스 컬렉션 클래스에서 응답에 포함할 메타 데이터를 쉽게 정의할 수 있습니다.

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

이런 방식으로 작성한 리소스 컬렉션은 라우트 또는 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는 Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있습니다. 이 경우에도 프레임워크 규칙에 따라 모델의 리소스 컬렉션이 자동으로 매핑됩니다.

```php
return User::all()->toResourceCollection();
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존하기

라라벨에서 리소스 컬렉션을 라우트에서 반환할 때, 기본적으로 컬렉션의 키는 0부터 시작하는 순차 번호로 리셋됩니다. 하지만, 리소스 클래스에 `preserveKeys` 속성을 추가하여 원래의 컬렉션 키를 유지하도록 설정할 수 있습니다.

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

`preserveKeys` 속성이 `true`로 설정되면, 컬렉션을 라우트나 컨트롤러에서 반환할 때 원래 키가 그대로 유지됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 연결되는 리소스 클래스 커스터마이징

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 해당 리소스 클래스(단수형)에 매핑한 결과로 자동 채워집니다. 단수형 리소스 클래스는 컬렉션 클래스명에서 뒤의 `Collection` 부분만 제거한 이름으로 간주합니다. 또, 개발자의 취향에 따라 단수형 클래스명의 끝에 `Resource`가 붙을 수도, 안 붙을 수도 있습니다.

예를 들어, `UserCollection`은 사용자 인스턴스를 `UserResource` 리소스로 매핑하려 시도합니다. 이 동작을 커스터마이즈하려면, 컬렉션 리소스에서 `$collects` 속성을 오버라이드하면 됩니다.

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
> [개념 개요](#concept-overview) 섹션을 먼저 읽고 진행하시기를 권장합니다.

리소스의 목적은 주어진 모델을 배열로 변환하는 것입니다. 각 리소스는 모델의 속성을 API에 적합한 배열로 변환하는 `toArray` 메서드를 포함하며, 이 배열은 애플리케이션의 라우트나 컨트롤러에서 직접 반환될 수 있습니다.

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

정의한 리소스는 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 연관관계

응답에 연관 리소스도 포함하려면, 리소스의 `toArray` 메서드에서 반환하는 배열에 연관관계 데이터를 추가하면 됩니다. 예를 들어, 사용자 리소스에서 해당 사용자의 게시글을 함께 포함시키는 경우 아래와 같이 작성할 수 있습니다.

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
> 연관관계를 이미 로드했을 경우에만 포함하려는 경우에는 [조건부 연관관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 모델의 컬렉션을 배열로 변환합니다. 모든 Eloquent 모델 컬렉션에서는 `toResourceCollection` 메서드를 활용해 바로 리소스 컬렉션을 생성할 수 있으므로, 각 모델마다 별도의 리소스 컬렉션 클래스를 정의할 필요는 없습니다.

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

하지만 컬렉션과 함께 반환할 메타 데이터를 커스터마이즈해야 할 필요가 있다면, 별도의 리소스 컬렉션을 정의해야 합니다.

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

단수형 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 바로 반환할 수 있습니다.

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

`toResourceCollection`를 호출하면 라라벨은 컬렉션 네임스페이스 안에서 모델 이름과 일치하고 `Collection`으로 끝나는 리소스 컬렉션을 자동 탐색합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 최상위 리소스는 JSON 응답으로 변환될 때 `data` 키로 감싸집니다. 일반적인 리소스 컬렉션의 응답 예시는 아래와 같습니다.

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

최상위 리소스의 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 보통 이 메서드는 모든 요청마다 실행되는 `AppServiceProvider` 또는 [서비스 프로바이더](/docs/master/providers)에서 호출하는 것이 일반적입니다.

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
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 주며, 직접 추가한 `data` 키에는 영향을 주지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 연관관계가 어떻게 래핑될지는 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션이 중첩 여부와 관계없이 항상 `data` 키로 감싸이길 원한다면, 각 리소스에 리소스 컬렉션 클래스를 만들고 `data` 키로 컬렉션을 반환하면 됩니다.

이렇게 하면 최상위 리소스가 두 번 `data`로 감싸이지는 않을까 걱정할 수도 있지만, 라라벨은 리소스가 중복으로 감싸이지 않도록 내부적으로 처리하기 때문에 중첩 수준에 신경 쓸 필요가 없습니다.

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

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는, 이미 `withoutWrapping`을 호출했더라도 리소스 데이터가 `data` 키 아래에 감싸집니다. 페이지네이션 응답에는 항상 페이지네이터 상태 정보를 담고 있는 `meta` 및 `links` 키가 포함되기 때문입니다.

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

라라벨의 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는, 편리하게 페이지네이터의 `toResourceCollection` 메서드를 사용할 수도 있습니다.

```php
return User::paginate()->toResourceCollection();
```

페이지네이션 응답에는 항상 페이지네이터의 상태 정보를 담고 있는 `meta` 및 `links` 키가 포함됩니다.

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

페이지네이션 응답의 `links`나 `meta` 키에 포함되는 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와, `links` 및 `meta` 키를 포함하는 `$default` 배열을 인자로 받습니다.

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

특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때에만 값을 포함시키고 싶을 수 있습니다. Laravel은 이러한 상황을 돕기 위한 다양한 헬퍼 메서드를 제공합니다. `when` 메서드는 조건부로 속성을 추가할 수 있도록 해줍니다.

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

위 예시에서, 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때에만 최종 리소스 응답에 `secret` 키가 포함됩니다. 만약 `false`를 반환하면, 클라이언트에 응답을 보내기 전에 `secret` 키가 제거됩니다. `when` 메서드를 이용하면 조건문을 직접 작성하지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

`when` 메서드의 두 번째 인자로 클로저를 전달할 수도 있습니다. 이렇게 하면 조건이 `true`일 때만 해당 값을 계산할 수 있습니다.

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 실제로 모델에 속성이 존재할 때만 그 속성을 응답에 포함시킵니다.

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드는 값이 null이 아닐 때만 응답에 속성을 포함합니다.

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

여러 속성을 동일한 조건에 의해 응답에 포함시켜야 할 때가 있습니다. 이럴 때는 `mergeWhen` 메서드를 사용해, 주어진 조건이 `true`일 때만 여러 속성을 한 번에 응답에 추가할 수 있습니다.

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

마찬가지로, 조건이 `false`이면 이 속성들은 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열과 숫자 키가 혼합된 배열, 또는 순차적이지 않은 숫자 키가 포함된 배열에서는 사용하면 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 연관관계

속성뿐 아니라, 연관관계도 모델에 이미 로드되어 있는 경우에만 응답에 포함시킬 수 있습니다. 이렇게 하면 컨트롤러에서 어떤 연관관계를 로드할지 결정하고, 리소스에서는 실제로 로드된 연관관계만 쉽게 포함시킬 수 있습니다. 궁극적으로 이런 방식은 리소스 내부에서 "N+1" 쿼리 문제를 방지하는 데 용이합니다.

`whenLoaded` 메서드는 연관관계의 이름을 인자로 받아, 해당 연관관계가 로드된 경우에만 응답에 포함되도록 도와줍니다. 실제 연관관계 객체가 아니라 이름을 인자로 사용한다는 점에 주의하세요.

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

예시에서 해당 연관관계가 로드되어 있지 않으면, 응답에서 `posts` 키는 자동으로 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 연관관계 카운트

연관관계 자체뿐만 아니라, 연관관계의 "카운트"(개수) 역시 모델에 이미 로드되어 있는 경우에만 응답에 포함시킬 수 있습니다.

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 연관관계의 카운트가 존재하는 경우에만 해당 값을 리소스 응답에 포함합니다.

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

연관관계 카운트가 로드되어 있지 않으면, `posts_count` 키는 응답에서 자동으로 제거됩니다.

평균(`avg`), 합계(`sum`), 최소(`min`), 최대(`max`) 같은 기타 집계값도 `whenAggregated` 메서드로 조건부로 포함할 수 있습니다.

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

다대다(many-to-many) 연관관계의 중간 테이블에서 온 데이터 역시 조건부로 리소스에 포함할 수 있습니다. 이를 위해 `whenPivotLoaded` 메서드를 사용할 수 있으며, 첫 번째 인자로 피벗 테이블 이름을, 두 번째 인자로 피벗 데이터가 있을 때 반환할 값을 반환하는 클로저를 넘깁니다.

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

연관관계가 [커스텀 중간 테이블 모델](/docs/master/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하는 경우, 첫 번째 인자로 중간 테이블 모델의 인스턴스를 전달할 수 있습니다.

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블에서 기본 accessor가 `pivot`이 아니라면, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다.

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

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가하는 것이 필요합니다. 여기에는 리소스나 연관 리소스로 연결되는 `links`나 리소스 자체에 대한 메타 정보 등이 해당됩니다. 리소스에 추가 메타 데이터를 반환하려면, `toArray` 메서드에 해당 정보를 포함하면 됩니다. 예시로, 리소스 컬렉션 변환 시 `links` 정보를 넣을 수 있습니다.

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

리소스에서 추가 메타 데이터를 반환할 때는, 라라벨이 페이지네이션된 응답에서 자동으로 추가하는 `links` 또는 `meta` 키를 덮어쓸까 걱정하지 않아도 됩니다. 직접 정의한 `links`는 페이지네이터의 링크와 자동으로 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

최상위 리소스가 응답될 때만 일부 메타 데이터를 포함하고 싶을 때가 있습니다. 보통 전체 응답에 관한 메타 정보가 해당되며, 이런 경우에는 리소스 클래스에 `with` 메서드를 정의하면 됩니다. 이 메서드는 최상위 리소스가 변환될 때만 응답에 포함할 메타 데이터 배열을 반환해야 합니다.

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

라우트 또는 컨트롤러에서 리소스 인스턴스 생성 시 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 응답에 추가로 포함할 데이터 배열을 인자로 받습니다.

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```

<a name="jsonapi-resources"></a>
## JSON:API 리소스

라라벨은 [JSON:API 명세](https://jsonapi.org/)를 준수하는 응답을 생성하는 `JsonApiResource` 리소스 클래스를 제공합니다. 이 클래스는 기본 `JsonResource`를 확장하며, 리소스 객체 구조, 연관관계, 희소 필드셋, 포함 요청 등을 자동 처리하고, `Content-Type` 헤더를 `application/vnd.api+json`으로 설정합니다.

> [!NOTE]
> 라라벨의 JSON:API 리소스는 응답 직렬화를 담당합니다. 필터/정렬 등 JSON:API 쿼리 파라미터 입력도 처리하려면 [Spatie의 Laravel Query Builder](https://spatie.be/docs/laravel-query-builder/v6/introduction) 패키지와 함께 사용하는 것을 권장합니다.

<a name="generating-jsonapi-resources"></a>
### JSON:API 리소스 생성

JSON:API 리소스를 생성하려면, `make:resource` Artisan 명령에 `--json-api` 플래그를 추가하면 됩니다.

```shell
php artisan make:resource PostResource --json-api
```

이렇게 생성한 클래스는 `Illuminate\Http\Resources\JsonApi\JsonApiResource`를 상속하며, `$attributes`, `$relationships` 프로퍼티를 정의할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

class PostResource extends JsonApiResource
{
    /**
     * The resource's attributes.
     */
    public $attributes = [
        // ...
    ];

    /**
     * The resource's relationships.
     */
    public $relationships = [
        // ...
    ];
}
```

JSON:API 리소스도 일반 리소스와 마찬가지로 라우트나 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```

또는 모델의 `toResource` 메서드를 사용할 수 있습니다.

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```

이렇게 하면 JSON:API 명세에 맞는 응답이 반환됩니다.

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World",
            "body": "This is my first post."
        }
    }
}
```

JSON:API 리소스 컬렉션도 `collection` 또는 `toResourceCollection` 메서드로 반환할 수 있습니다.

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```

<a name="defining-jsonapi-attributes"></a>
### 속성 정의

JSON:API 리소스에서 속성을 정의하는 방법은 두 가지가 있습니다.

가장 간단한 방법은 리소스의 `$attributes` 속성에 포함할 속성명을 배열 값으로 선언하는 것입니다. 이때 값은 내부 모델에서 직접 읽어옵니다.

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```

더 세밀하게 속성을 제어하려면, 리소스의 `toAttributes` 메서드를 오버라이드할 수 있습니다.

```php
/**
 * Get the resource's attributes.
 *
 * @return array<string, mixed>
 */
public function toAttributes(Request $request): array
{
    return [
        'title' => $this->title,
        'body' => $this->body,
        'is_published' => $this->published_at !== null,
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```

<a name="defining-jsonapi-relationships"></a>
### 연관관계 정의

JSON:API 리소스는 JSON:API 명세를 따르는 연관관계 정의를 지원합니다. 연관관계는 클라이언트가 `include` 쿼리 파라미터로 요청했을 때에만 직렬화됩니다.

#### `$relationships` 속성

리소스에서 포함 가능한 연관관계는 `$relationships` 배열 속성에 선언할 수 있습니다.

```php
public $relationships = [
    'author',
    'comments',
];
```

단순히 연관관계 이름만 적으면, 라라벨이 Eloquent 연관관계를 찾아 적절한 리소스 클래스를 자동으로 결정합니다. 특정 리소스 클래스를 명시하려면 키/값 쌍으로 정의할 수 있습니다.

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```

또는 `toRelationships` 메서드를 오버라이드하여 직접 반환할 수도 있습니다.

```php
/**
 * Get the resource's relationships.
 */
public function toRelationships(Request $request): array
{
    return [
        'author' => UserResource::class,
        'comments',
    ];
}
```

#### 연관관계 포함 요청

클라이언트는 `include` 쿼리 파라미터로 연관된 리소스를 요청할 수 있습니다.

```
GET /api/posts/1?include=author,comments
```

이렇게 하면, 응답의 `relationships` 키 안에 리소스 식별자 객체가 포함되고, `included` 배열에는 완전한 리소스 객체가 포함되어 반환됩니다.

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "relationships": {
            "author": {
                "data": {
                    "id": "1",
                    "type": "users"
                }
            },
            "comments": {
                "data": [
                    {
                        "id": "1",
                        "type": "comments"
                    }
                ]
            }
        }
    },
    "included": [
        {
            "id": "1",
            "type": "users",
            "attributes": {
                "name": "Taylor Otwell"
            }
        },
        {
            "id": "1",
            "type": "comments",
            "attributes": {
                "body": "Great post!"
            }
        }
    ]
}
```

중첩 연관관계는 dot(점) 표기법을 사용하여 포함시킬 수 있습니다.

```
GET /api/posts/1?include=comments.author
```

<a name="jsonapi-relationship-depth"></a>
#### 연관관계 깊이

기본적으로, 중첩 연관관계 포함은 최대 깊이에 제한이 있습니다. 이 제한을 커스터마이즈하려면, 보통 애플리케이션의 서비스 프로바이더에서 `maxRelationshipDepth` 메서드를 호출하면 됩니다.

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```

<a name="jsonapi-resource-type-and-id"></a>
### 리소스 타입 및 ID

기본적으로, 리소스의 `type`은 리소스 클래스 이름에서 파생됩니다. 예를 들어, `PostResource`는 `posts`, `BlogPostResource`는 `blog-posts` 타입을 생성합니다. `id`는 모델의 기본 키에서 가져옵니다.

이 값을 커스터마이즈하려면, 리소스의 `toType` 및 `toId` 메서드를 오버라이드하면 됩니다.

```php
/**
 * Get the resource's type.
 */
public function toType(Request $request): string
{
    return 'articles';
}

/**
 * Get the resource's ID.
 */
public function toId(Request $request): string
{
    return (string) $this->uuid;
}
```

예를 들어, `AuthorResource`가 `User` 모델을 감싸더라도 타입을 `authors`로 변경할 수 있습니다.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
### 희소 필드셋 및 포함

JSON:API 리소스는 [희소 필드셋(sparse fieldsets)](https://jsonapi.org/format/#fetching-sparse-fieldsets)을 지원하므로, 클라이언트가 `fields` 쿼리 파라미터로 각 리소스 타입에 대해 반환할 속성을 세부적으로 지정할 수 있습니다.

```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

이 요청은 `posts` 리소스에는 `title`과 `created_at`만, `users` 리소스에는 `name`만 포함하게 됩니다.

<a name="jsonapi-ignoring-query-string"></a>
#### 쿼리 문자열 무시

특정 리소스 응답에서 희소 필드셋 필터링을 비활성화하려면, `ignoreFieldsAndIncludesInQueryString` 메서드를 호출하세요.

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```

<a name="jsonapi-including-previously-loaded-relationships"></a>
#### 이전에 로드된 연관관계 포함

기본적으로 연관관계는 `include` 쿼리 파라미터로 요청했을 때만 응답에 포함됩니다. 쿼리 문자열과 무관하게 미리 eager load된 모든 연관관계를 항상 포함하고 싶다면, `includePreviouslyLoadedRelationships` 메서드를 호출할 수 있습니다.

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```

<a name="jsonapi-links-and-meta"></a>
### 링크 및 메타

JSON:API 리소스 객체에 링크와 메타 정보를 추가하려면, 리소스에서 `toLinks` 및 `toMeta` 메서드를 오버라이드하면 됩니다.

```php
/**
 * Get the resource's links.
 */
public function toLinks(Request $request): array
{
    return [
        'self' => route('api.posts.show', $this->resource),
    ];
}

/**
 * Get the resource's meta information.
 */
public function toMeta(Request $request): array
{
    return [
        'readable_created_at' => $this->created_at->diffForHumans(),
    ];
}
```

이렇게 하면 응답 데이터 객체에 `links`와 `meta` 키가 추가됩니다.

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "links": {
            "self": "https://example.com/api/posts/1"
        },
        "meta": {
            "readable_created_at": "2 hours ago"
        }
    }
}
```

<a name="resource-responses"></a>
## 리소스 응답

이전 섹션에서 소개한 것처럼, 리소스는 라우트와 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 클라이언트로 응답을 보내기 전에 HTTP 응답을 커스터마이즈해야 할 때가 있습니다. 이를 위한 두 가지 방법이 있습니다.

첫 번째 방법은 리소스에 `response` 메서드를 체이닝하는 것입니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 응답 헤더를 완전히 제어할 수 있습니다.

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

또는, 리소스 클래스 내부에 `withResponse` 메서드를 정의할 수 있습니다. 이 메서드는 해당 리소스가 최상위 리소스로 응답될 때 호출됩니다.

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
