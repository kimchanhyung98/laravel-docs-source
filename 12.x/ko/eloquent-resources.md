# Eloquent: API 리소스

- [소개](#introduction)
- [리소스 생성](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성하기](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 관계](#conditional-relationships)
    - [메타 데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 위치하는 변환 레이어가 필요할 수 있습니다. 예를 들어, 특정 속성을 일부 사용자에게만 보여주고 싶거나, 모델의 JSON 표현에 항상 특정 관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 표현력 있게 쉽게 변환할 수 있도록 해줍니다.

물론, Eloquent 모델이나 컬렉션을 `toJson` 메서드를 사용해 언제든지 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스를 사용하면 모델과 관계의 JSON 직렬화에 대해 더 세밀하고 견고한 제어가 가능합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션을 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 전체 리소스 컬렉션과 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 만들려면 리소스 생성 시 `--collection` 플래그를 사용하면 됩니다. 또는 리소스 이름에 `Collection`을 포함하면 Laravel이 컬렉션 리소스를 생성해야 한다는 것을 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이는 리소스와 리소스 컬렉션에 대한 상위 수준 개요입니다. 이 문서의 다른 섹션을 읽고 리소스가 제공하는 커스터마이징과 강력함을 더 깊이 이해하는 것이 좋습니다.

리소스를 작성할 때 사용할 수 있는 모든 옵션을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 상위 수준에서 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환되어야 하는 속성의 배열을 반환합니다.

모델 속성은 `$this` 변수에서 직접 접근할 수 있습니다. 이는 리소스 클래스가 프로퍼티 및 메서드 접근을 편리하게 해당 모델로 자동으로 중계(proxy)하기 때문입니다. 리소스가 정의되면 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 해당 모델 인스턴스를 생성자에 전달받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```

편의상, 모델의 `toResource` 메서드를 사용할 수도 있으며, 프레임워크의 규칙에 따라 모델의 리소스를 자동으로 탐색합니다:

```php
return User::findOrFail($id)->toResource();
```

`toResource`를 호출하면 Laravel은 모델의 이름과 일치하고, 선택적으로 `Resource`로 끝나는 리소스를 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에서 찾으려고 시도합니다.

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션이나 페이지네이팅된 응답을 반환하려면, 라우트나 컨트롤러에서 리소스 클래스의 `collection` 메서드를 사용하세요:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있으며, 프레임워크 규칙에 따라 모델의 리소스 컬렉션을 자동으로 탐색합니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면, Laravel은 모델의 이름과 일치하고 `Collection`으로 끝나는 리소스 컬렉션을 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에서 찾으려고 시도합니다.

<a name="custom-resource-collections"></a>
#### 커스텀 리소스 컬렉션

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환해야 할 커스텀 메타 데이터의 추가를 허용하지 않습니다. 컬렉션 응답을 커스터마이징하고 싶다면, 해당 컬렉션을 나타내는 전용 리소스를 생성하면 됩니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함시킬 메타 데이터를 자유롭게 정의할 수 있습니다:

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

정의한 리소스 컬렉션은 라우트나 컨트롤러에서 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수도 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection` 메서드를 호출하면 Laravel은 모델의 이름과 일치하고, `Collection`으로 끝나는 리소스 컬렉션을 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에서 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지하기

리소스 컬렉션을 라우트에서 반환하면 Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 그러나, 컬렉션의 원래 키를 유지하려면, 리소스 클래스에 `preserveKeys` 프로퍼티를 추가하고, 값을 `true`로 설정하면 됩니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스의 컬렉션 키를 보존할지 여부를 지정합니다.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 프로퍼티가 `true`로 설정되면, 라우트나 컨트롤러에서 컬렉션을 반환할 때 컬렉션의 키가 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 하위 리소스 클래스 커스터마이징

일반적으로 리소스 컬렉션의 `$this->collection` 프로퍼티는 컬렉션의 각 항목을 단수형 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단수 리소스 클래스는 컬렉션 클래스 이름에서 끝의 `Collection` 부분을 제거한 이름으로 가정됩니다. 또, 개인 취향에 따라 단수형 리소스 클래스에 `Resource` 접미사가 붙을 수도, 붙지 않을 수도 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스를 `UserResource`로 매핑하려고 시도합니다. 이 동작을 커스터마이즈하려면, 리소스 컬렉션의 `$collects` 프로퍼티를 오버라이드하면 됩니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스 컬렉션이 수집하는 리소스입니다.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성하기

> [!NOTE]
> [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 계속 읽기 전에 꼭 읽어보시기 바랍니다.

리소스는 주어진 모델을 배열로 변환만 하면 됩니다. 즉, 각 리소스는 `toArray` 메서드를 포함하며, 이 메서드는 모델의 속성을 API 친화적인 배열로 변환해 애플리케이션의 라우트나 컨트롤러에서 반환할 수 있게 합니다:

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

리소스를 정의했다면, 이를 라우트나 컨트롤러에서 그대로 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```

<a name="relationships"></a>
#### 관계

응답에 관련 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 예를 들어, 사용자의 블로그 포스트를 리소스 응답에 추가하려면 `PostResource`의 `collection` 메서드를 사용할 수 있습니다:

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
> 관계가 이미 로드된 경우에만 포함하고 싶다면 [조건부 관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스는 단일 모델을 배열로 변환하지만, 리소스 컬렉션은 모델의 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 리소스 컬렉션 클래스를 정의해야 할 필요는 없습니다. 모든 Eloquent 모델 컬렉션은 `toResourceCollection` 메서드를 제공하여 즉석에서 리소스 컬렉션을 생성할 수 있습니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```

그러나 컬렉션과 함께 반환되는 메타 데이터를 커스터마이즈해야 한다면, 직접 리소스 컬렉션을 정의해야 합니다:

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

단수형 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

또는, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있습니다:

```php
return User::all()->toResourceCollection();
```

`toResourceCollection`을 호출하면, Laravel은 모델 이름과 일치하고 `Collection`으로 끝나는 리소스 컬렉션을 모델과 가장 가까운 `Http\Resources` 네임스페이스 내에서 찾으려고 시도합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 가장 바깥쪽 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

가장 바깥 리소스의 래핑을 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출하세요. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`나, 매 요청마다 로드되는 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출해야 합니다:

```php
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
> `withoutWrapping` 메서드는 가장 바깥쪽 응답에만 영향을 주며, 직접 추가한 컬렉션의 `data` 키는 제거되지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩된 리소스 래핑

리소스의 관계가 어떻게 래핑되는지는 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션이 중첩 여부와 상관없이 `data` 키로 래핑되길 원한다면, 각 리소스마다 리소스 컬렉션 클래스를 만들고, `data` 키 내에 컬렉션을 반환하면 됩니다.

혹시 가장 바깥쪽 리소스까지 `data` 키가 두 번 래핑되는지 걱정될 수 있지만, 걱정하지 마세요. Laravel은 이중 래핑이 발생하지 않게 막아줍니다. 따라서 컬렉션의 중첩 수준은 걱정하지 않아도 됩니다:

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

리소스 응답을 통해 페이지네이팅된 컬렉션을 반환하면, `withoutWrapping`이 호출되어도 Laravel은 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이트된 응답은 항상 `meta`와 `links` 키를 포함하여 페이지네이터 상태 정보를 반환하기 때문입니다:

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

Laravel 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

또는, 페이지네이터의 `toResourceCollection` 메서드를 사용할 수 있습니다:

```php
return User::paginate()->toResourceCollection();
```

페이지네이팅된 응답은 항상 `meta`와 `links` 키를 포함하여 페이지네이터 상태 정보를 반환합니다:

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

페이지네이션 응답의 `links`나 `meta` 키에 포함되는 정보를 커스터마이즈하려면, 리소스에 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `links`, `meta` 키가 포함된 `$default` 배열을 인자로 받습니다:

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

특정 조건에서만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하고 싶을 수 있습니다. Laravel은 이런 상황에서 사용할 수 있는 다양한 헬퍼 메서드를 제공합니다. `when` 메서드를 사용하면 조건에 따라 리소스 응답에 속성을 추가할 수 있습니다:

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

이 예제에서 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환하는 경우에만 최종 리소스 응답에 `secret` 키가 포함됩니다. `false`면 클라이언트로 전송되기 전에 `secret` 키가 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들 때 조건문에 의존하지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

`when` 메서드의 두 번째 인자로 클로저를 전달할 수도 있어, 조건이 `true`일 때만 결과값을 계산할 수 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드를 사용하면 실제로 모델에 속성이 있는 경우에만 속성을 포함시킬 수 있습니다:

```php
'name' => $this->whenHas('name'),
```

추가로, `whenNotNull` 메서드는 속성이 null이 아닌 경우에만 응답에 포함시킬 수 있습니다:

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 합치기(Merge)

여러 개의 속성을 동일한 조건에서만 리소스 응답에 포함하고 싶을 때가 있습니다. 이 경우, `mergeWhen` 메서드를 사용해 해당 조건이 `true`일 때만 여러 속성을 응답에 포함시킬 수 있습니다:

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

마찬가지로, 주어진 조건이 `false`일 경우 이 속성들은 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]
> `mergeWhen` 메서드는 문자열과 숫자 키가 섞인 배열 내에서 사용해서는 안 됩니다. 또한, 연속적이지 않은 숫자 키가 포함된 배열에서도 사용하지 마세요.

<a name="conditional-relationships"></a>
### 조건부 관계

속성 로딩을 조건부로 할 수 있을 뿐만 아니라, 모델에서 관계가 이미 로드된 경우에만 리소스 응답에 관계를 조건부로 포함할 수도 있습니다. 이렇게 하면 컨트롤러에서 어떤 관계를 로드할지 결정하고, 리소스에서는 실제로 로드된 경우에만 응답에 포함할 수 있습니다. 궁극적으로 이는 리소스 내에서 "N+1" 쿼리 문제를 예방하는 데 도움이 됩니다.

`whenLoaded` 메서드는 관계를 조건부로 추가할 때 사용할 수 있습니다. 쓸데없이 관계를 로드하지 않기 위해 이 메서드는 관계 자체가 아니라 관계의 이름을 인자로 받습니다:

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

이 예제에서 관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 수(Counts)

관계를 조건부로 포함하는 것과 더불어, 관계의 "개수"도 모델에 개수가 로드된 경우에만 리소스 응답에 조건부로 포함할 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 관계의 개수가 존재하는 경우에만 리소스 응답에 포함시킬 수 있습니다. 이 메서드는 관계의 개수가 존재하지 않으면 속성을 응답에서 제외합니다:

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

이 예제에서 `posts` 관계의 개수가 로드되지 않았다면, `posts_count` 키는 응답에서 제거됩니다.

기타 종류의 집계(`avg`, `sum`, `min`, `max` 등)도 `whenAggregated` 메서드를 통해 조건부로 로드할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗(Pivot) 정보

리소스 응답에 관계 정보뿐만 아니라, 다대다 중간 테이블의 데이터도 `whenPivotLoaded` 메서드를 사용해 조건부로 포함할 수 있습니다. 이 메서드는 첫 번째 인자로 피벗 테이블의 이름을 받고, 두 번째 인자로 피벗 정보가 모델에 존재할 때 반환할 값을 반환하는 클로저를 받습니다:

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

관계가 [커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 사용할 경우, 중간 테이블 모델 인스턴스를 첫 번째 인자로 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블에서 `pivot` 외 다른 접근자(accessor)를 사용하는 경우, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

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

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터 추가가 필요합니다. 예를 들어, 리소스 자체나 관련 리소스에 대한 `links` 혹은 리소스 자체에 대한 메타 정보를 포함하는 경우가 많습니다. 리소스에 메타 데이터를 추가하려면, `toArray` 메서드에 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 다음과 같이 포함할 수 있습니다:

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

리소스에서 추가적인 메타 데이터를 반환해도, 페이지네이션 응답에서 자동으로 추가되는 `links`나 `meta` 키를 덮어쓸 걱정은 필요 없습니다. 여러분이 정의한 추가 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 레벨 메타 데이터

때때로 리소스가 최상위 리소스(응답의 최상단)로 반환될 때만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 보통 전체 응답에 관한 메타 정보가 여기에 해당합니다. 이런 메타 데이터를 정의하려면, 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 리소스가 변환될 때 최상위일 때만 포함할 메타 데이터의 배열을 반환해야 합니다:

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
     * 리소스 배열과 함께 반환될 추가 데이터 반환.
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

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는, 리소스 응답에 추가할 데이터를 배열로 받습니다:

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

앞서 본 것처럼, 리소스는 라우트 및 컨트롤러에서 직접 반환할 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```

하지만 때때로 클라이언트로 전송되기 전에 HTTP 응답을 커스터마이즈할 필요가 있습니다. 이를 달성하는 방법은 두 가지가 있습니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하여, 응답 헤더를 완전히 제어할 수 있습니다:

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

또는, 리소스 내에 `withResponse` 메서드를 정의할 수 있습니다. 이 메서드는 리소스가 응답에서 최상위 리소스로 반환될 때 호출됩니다:

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