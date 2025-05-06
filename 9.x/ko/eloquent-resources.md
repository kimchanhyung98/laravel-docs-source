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

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 위치하는 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자에게만 특정 속성을 표시하거나, 항상 모델의 특정 관계를 JSON 표현에 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델과 모델 컬렉션을 JSON으로 변환하는 작업을 더욱 표현력 있게, 그리고 쉽게 할 수 있도록 해줍니다.

물론, Eloquent 모델이나 컬렉션을 `toJson` 메서드를 사용해 항상 JSON으로 변환할 수도 있습니다. 그러나 Eloquent 리소스는 모델 및 그 관계들의 JSON 직렬화에서 더 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령어를 사용하면 됩니다. 기본적으로, 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다.

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 외에도, 모델 컬렉션을 변환하는 역할을 하는 리소스를 생성할 수도 있습니다. 이를 통해 주어진 리소스의 전체 컬렉션과 관련된 링크 및 다른 메타 정보를 JSON 응답에 포함시킬 수 있습니다.

리소스 컬렉션을 생성하려면 리소스 생성 시 `--collection` 플래그를 사용합니다. 또는, 리소스 이름에 `Collection`이라는 단어를 포함시키면 Laravel이 컬렉션 리소스를 생성하도록 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다.

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> **참고**  
> 이 섹션은 리소스와 리소스 컬렉션에 대한 상위 개념적 개요입니다. 리소스가 제공하는 커스터마이징과 강력한 기능을 더 깊이 이해하려면 문서의 다른 섹션도 꼭 읽어보시기 바랍니다.

리소스를 작성할 때 사용 가능한 모든 옵션을 살펴보기 전에, 먼저 Laravel에서 리소스를 어떻게 사용하는지 간단히 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환되어야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환.
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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트 또는 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환해야 할 속성 배열을 반환합니다.

모델의 속성에 `$this`를 통해 직접 접근할 수 있다는 점에 유의하세요. 이는 리소스 클래스가 속성과 메서드 접근을 하위 모델로 자동 위임(proxing)하기 때문에 가능한 일입니다. 리소스가 정의되면, 라우트 또는 컨트롤러에서 해당 모델 인스턴스를 생성자에 주입해 반환할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션 또는 페이지네이션된 응답을 반환하려면, 라우트 또는 컨트롤러에서 리소스 클래스가 제공하는 `collection` 메서드를 사용하여 리소스 인스턴스를 생성해야 합니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

이 방식은 컬렉션과 함께 반환해야 할 커스텀 메타 데이터를 추가하지 못합니다. 컬렉션 응답을 커스터마이즈하려면 컬렉션을 나타내는 전용 리소스를 생성해야 합니다.

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면 응답에 포함할 메타 데이터를 쉽게 정의할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환.
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

리소스 컬렉션을 정의한 후, 라우트 또는 컨트롤러에서 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 유지

라우트에서 리소스 컬렉션을 반환하면, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만 리소스 클래스에 `preserveKeys` 속성을 추가하여 원래의 컬렉션 키를 유지할지 여부를 지정할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스의 컬렉션 키를 유지할지 여부.
     *
     * @var bool
     */
    public $preserveKeys = true;
}
```

`preserveKeys` 속성이 `true`로 설정되면, 컬렉션을 라우트 또는 컨트롤러에서 반환할 때 컬렉션의 키가 유지됩니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```

<a name="customizing-the-underlying-resource-class"></a>
#### 내부 리소스 클래스 커스터마이징

일반적으로 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 해당 단수(싱귤러) 리소스 클래스로 매핑한 결과로 자동 채워집니다. 단수 리소스 클래스는 컬렉션의 클래스 이름에서 `Collection` 부분을 제거한 이름으로 예상됩니다. 또한, 여러분의 취향에 따라 단수 리소스 클래스에 `Resource` 접미사를 붙일 수도, 붙이지 않을 수도 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스를 `UserResource` 리소스에 매핑하려 시도합니다. 이 동작을 변경하려면 리소스 컬렉션의 `$collects` 속성을 오버라이드하면 됩니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 이 리소스가 수집하는(collects) 리소스.
     *
     * @var string
     */
    public $collects = Member::class;
}
```

<a name="writing-resources"></a>
## 리소스 작성

> **참고**  
> 아직 [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 진행하기 전에 먼저 읽어보시기 바랍니다.

본질적으로 리소스는 간단합니다. 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 리소스에는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드가 포함되어, 라우트 또는 컨트롤러에서 반환할 수 있습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환.
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

리소스를 정의한 후에는 라우트 또는 컨트롤러에서 바로 반환할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

<a name="relationships"></a>
#### 관계(리소스 내 관계 포함)

응답에 관련 리소스를 포함하고자 할 경우, 해당 리소스를 `toArray` 메서드에서 반환하는 배열에 추가할 수 있습니다. 이 예시에서는 사용자의 블로그 게시물을 리소스 응답에 추가하기 위해 `PostResource` 리소스의 `collection` 메서드를 활용합니다.

```php
use App\Http\Resources\PostResource;

/**
 * 리소스를 배열로 변환.
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

> **참고**  
> 관계를 이미 로드했을 때만 포함하려면 [조건부 관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 여러 모델의 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다. 모든 리소스는 `collection` 메서드를 제공하여 즉석에서 "ad-hoc" 리소스 컬렉션을 생성할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```

하지만 컬렉션에 반환되는 메타 데이터를 커스터마이즈해야 한다면, 반드시 자신만의 리소스 컬렉션을 정의해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환.
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

단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트 또는 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로 리소스 응답이 JSON으로 변환될 때, 최상위 리소스는 `data` 키로 래핑됩니다. 예를 들어, 다음과 같이 표준 리소스 컬렉션 응답이 구성됩니다.

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

`data` 대신 커스텀 키를 사용하고 싶다면, 리소스 클래스에 `$wrap` 속성을 정의하세요.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 적용할 "data" 래퍼.
     *
     * @var string|null
     */
    public static $wrap = 'user';
}
```

최상위 리소스의 래핑을 비활성화하려면 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 보통은 이 메서드를 여러분의 `AppServiceProvider` 나 모든 요청에서 불러오는 [서비스 프로바이더](/docs/{{version}}/providers) 안에서 호출합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        JsonResource::withoutWrapping();
    }
}
```

> **경고**  
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며, 사용자 정의 리소스 컬렉션에 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 관계가 어떻게 래핑될지 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 중첩과 상관없이 항상 `data` 키로 래핑하고 싶다면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고, 컬렉션을 `data` 키로 반환하세요.

이렇게 하면 최상위 리소스가 `data` 키로 중첩되어 래핑되지 않을지 걱정할 수도 있습니다. 걱정하지 마세요. Laravel은 리소스가 실수로 이중 래핑되지 않도록 보장하므로, 리소스 컬렉션의 중첩 수준에 대해 신경 쓸 필요가 없습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환.
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
#### 데이터 래핑과 페이지네이션

리소스 응답을 통해 페이지네이션된 컬렉션을 반환할 때, `withoutWrapping` 메서드를 호출하더라도 Laravel은 리소스 데이터를 반드시 `data` 키로 래핑합니다. 이는 페이지네이션된 응답에 항상 페이지네이터의 상태 정보를 담는 `meta` 및 `links` 키가 포함되기 때문입니다.

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
### 페이지네이션

Laravel 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다.

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```

페이지네이션된 응답에는 항상 페이지네이터의 상태 정보를 담는 `meta` 와 `links` 키가 포함됩니다.

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
### 조건부 속성

경우에 따라, 특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자" 인 경우에만 값을 포함하는 식입니다. Laravel은 이와 같은 경우를 돕기 위한 다양한 헬퍼 메서드를 제공합니다. `when` 메서드는 조건에 따라 속성을 리소스 응답에 선택적으로 추가할 수 있게 해줍니다.

```php
/**
 * 리소스를 배열로 변환.
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

이 예시에서, `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 리소스 응답에 포함됩니다. 만약 `false`라면, 해당 키는 최종 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 만들 때 조건문을 쓰지 않고도 리소스를 표현력 있게 정의할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저도 받으며, 이 경우 조건이 참일 때에만 값을 계산할 수 있습니다.

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```

`whenHas` 메서드는 실제로 모델에 해당 속성이 존재할 때만 속성을 포함하도록 사용합니다.

```php
'name' => $this->whenHas('name'),
```

또한, `whenNotNull` 메서드를 사용하면 속성 값이 null이 아닐 때만 속성을 리소스 응답에 포함할 수 있습니다.

```php
'name' => $this->whenNotNull($this->name),
```

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

동일한 조건에서만 여러 속성을 리소스 응답에 포함해야 하는 경우, `mergeWhen` 메서드를 사용해 조건이 참일 때만 여러 속성을 한 번에 병합할 수 있습니다.

```php
/**
 * 리소스를 배열로 변환.
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

마찬가지로, 주어진 조건이 `false`라면 이 속성들은 클라이언트에 응답되기 전에 제거됩니다.

> **경고**  
> `mergeWhen` 메서드는 문자열 및 숫자 키가 혼합된 배열 내에서 사용해서는 안 됩니다. 또한, 순차적으로 정렬되지 않은 숫자 키가 있는 배열 내에서도 사용해서는 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 관계

속성뿐만 아니라, 모델에서 관계를 이미 로드한 경우에만 리소스 응답에 관계를 포함할 수 있습니다. 이렇게 하면, 컨트롤러는 모델에 어떤 관계를 로드할지 결정할 수 있고, 리소스는 정말로 로드가 되었을 때만 포함할 수 있습니다. 이 방식은 리소스 내에서 "N+1" 쿼리 문제를 예방하는 데도 도움이 됩니다.

`whenLoaded` 메서드는 관계를 조건부로 로드할 때 사용합니다. 불필요하게 관계를 로드하는 것을 방지하기 위해, 이 메서드는 관계 자체가 아니라 관계의 이름(문자열)을 받습니다.

```php
use App\Http\Resources\PostResource;

/**
 * 리소스를 배열로 변환.
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

이 예시에서, 해당 관계가 로드되지 않았다면 `posts` 키는 클라이언트에 응답되기 전에 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 카운트

조건부로 관계 자체뿐 아니라 관계의 카운트(갯수)를 리소스 응답에 포함할 수도 있습니다. 모델에서 관계의 카운트가 로드된 경우 해당 정보를 포함할 수 있습니다.

```php
new UserResource($user->loadCount('posts'));
```

`whenCounted` 메서드는 특정 관계의 카운트가 리소스 응답에 조건부로 포함되어야 할 때 사용합니다. 이 메서드는 관계의 카운트가 없다면 불필요하게 속성을 포함하지 않습니다.

```php
/**
 * 리소스를 배열로 변환.
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

이 예시에서, `posts` 관계의 카운트가 로드되지 않았다면, 최종 응답에서 해당 키가 제거됩니다.

<a name="conditional-pivot-information"></a>
#### 조건부 피벗(pivot) 정보

많은-대-많은(many-to-many) 관계의 중간 테이블(피벗 테이블) 정보를 리소스 응답에 조건부로 포함하고자 할 때는 `whenPivotLoaded` 메서드를 사용할 수 있습니다. 첫 번째 인자로 피벗 테이블의 이름을 전달하고, 두 번째 인자는 피벗 정보가 사용 가능할 때 반환할 값을 반환하는 클로저여야 합니다.

```php
/**
 * 리소스를 배열로 변환.
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

[커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)를 사용할 경우, 중간 테이블 모델 인스턴스를 첫 번째 인자로 넘길 수도 있습니다.

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```

중간 테이블이 `pivot`이 아닌 다른 접근자(accessor)를 사용하는 경우에는 `whenPivotLoadedAs` 메서드를 사용할 수 있습니다.

```php
/**
 * 리소스를 배열로 변환.
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
### 메타 데이터 추가

일부 JSON API 표준은 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가할 것을 요구합니다. 이에는 리소스 자체 혹은 연관 리소스에 대한 `links` 정보, 혹은 리소스 자체에 대한 메타 정보 등 여러 가지가 포함됩니다. 리소스에 대한 추가 메타 데이터를 반환하려면 `toArray` 메서드에서 함께 반환하면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `link` 정보를 포함할 수 있습니다.

```php
/**
 * 리소스 컬렉션을 배열로 변환.
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

추가 메타 데이터를 리소스에서 반환할 때는, 페이지네이션 응답 시 Laravel이 자동으로 추가하는 `links` 또는 `meta` 키와 충돌할까 걱정할 필요가 없습니다. 여러분이 정의한 `links` 값은 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

최상위 리소스 응답일 때만 특정 메타 데이터를 포함하고 싶을 때도 있습니다. 보통은 전체 응답에 대한 메타 정보가 여기에 해당합니다. 이 메타 데이터는 리소스 클래스에 `with` 메서드를 추가해 정의할 수 있습니다. 이 메서드는 최상위 리소스로 변환될 때만 리소스 응답과 함께 포함할 메타 데이터 배열을 반환해야 합니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * 리소스 컬렉션을 배열로 변환.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        return parent::toArray($request);
    }

    /**
     * 리소스 배열과 함께 반환해야 할 추가 데이터 가져오기.
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
#### 리소스 생성 시 메타 데이터 추가

라우트 또는 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 사용 가능한 `additional` 메서드는 리소스 응답에 추가할 데이터 배열을 받을 수 있습니다.

```php
return (new UserCollection(User::all()->load('roles')))
                ->additional(['meta' => [
                    'key' => 'value',
                ]]);
```

<a name="resource-responses"></a>
## 리소스 응답

앞서 살펴본 것처럼, 리소스는 라우트나 컨트롤러에서 직접 반환할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function ($id) {
    return new UserResource(User::findOrFail($id));
});
```

그러나 때때로, 클라이언트로 전송되기 전에 HTTP 응답을 커스터마이즈해야 할 수도 있습니다. 이 작업은 두 가지 방법으로 할 수 있습니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하여, 응답 헤더를 포함해 응답을 완전히 제어할 수 있습니다.

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return (new UserResource(User::find(1)))
                ->response()
                ->header('X-Value', 'True');
});
```

또는, 리소스 자체에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 최상위 리소스로서 응답될 때 호출됩니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * 리소스를 배열로 변환.
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
     * 리소스 응답을 커스터마이즈합니다.
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
