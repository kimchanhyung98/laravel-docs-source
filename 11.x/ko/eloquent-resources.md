# Eloquent: API 리소스

- [소개](#introduction)
- [리소스 생성하기](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성하기](#writing-resources)
    - [데이터 감싸기](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 관계](#conditional-relationships)
    - [메타 데이터 추가하기](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 사용자에게 반환되는 JSON 응답 사이에 위치하는 변환 계층이 필요할 수 있습니다. 예를 들어, 일부 사용자에게는 특정 속성만 표시하고 싶거나, 항상 모델의 특정 관계를 JSON 표현에 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 이러한 모델 및 모델 컬렉션을 JSON으로 변환하는 작업을 명확하고 쉽게 처리할 수 있도록 도와줍니다.

물론 언제든 Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용해 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스를 사용하면 모델과 관계의 JSON 직렬화 과정을 더 세밀하고 강력하게 제어할 수 있습니다.

<a name="generating-resources"></a>
## 리소스 생성하기

리소스 클래스를 생성하려면 `make:resource` 아티즌 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 위치합니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션 자체를 변환하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 전체 컬렉션과 관련된 링크나 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스 생성 시 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection`을 포함하면 Laravel은 해당 리소스를 컬렉션 리소스로 간주합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]  
> 이 부분은 리소스와 리소스 컬렉션에 대한 전반적인 개요입니다. 리소스의 커스터마이즈와 확장 기능을 제대로 이해하고 싶다면 문서의 다른 섹션들도 꼭 읽어보세요.

리소스를 작성할 때 사용할 수 있는 모든 옵션을 살펴보기 전에, 먼저 Laravel 내에서 리소스가 어떻게 사용되는지 간략히 살펴봅니다. 하나의 리소스 클래스는 JSON 구조로 변환해야 할 하나의 모델을 나타냅니다. 예를 들어, 간단한 `UserResource` 클래스는 다음과 같이 작성할 수 있습니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트 또는 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환되어야 할 속성 배열을 반환합니다.

모델 속성에 `$this` 변수를 통해 직접 접근할 수 있습니다. 이는 리소스 클래스가 프로퍼티 및 메서드 접근을 자동으로 해당 모델로 프록싱하여 편리하게 사용할 수 있도록 하기 때문입니다. 리소스가 정의되면, 라우트나 컨트롤러에서 인스턴스를 생성해 반환할 수 있습니다. 리소스는 생성자를 통해 모델 인스턴스를 전달받습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스들의 컬렉션이나 페이지네이션된 응답을 반환할 경우, 리소스 클래스가 제공하는 `collection` 메서드를 사용해야 합니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

이 방식은 컬렉션에 추가로 반환해야 할 커스텀 메타 데이터를 포함할 수 없습니다. 컬렉션 응답을 커스터마이징하려면, 컬렉션을 나타내는 전용 리소스를 생성해야 합니다:

```shell
php artisan make:resource UserCollection
```

리소스 컬렉션 클래스가 생성되면, 응답에 포함해야 할 메타 데이터를 쉽게 정의할 수 있습니다:

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

리소스 컬렉션을 정의한 후, 라우트나 컨트롤러에서 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존하기

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 그러나 리소스 클래스에 `preserveKeys` 속성을 추가해 컬렉션의 원래 키를 보존할지 지정할 수 있습니다:

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

`preserveKeys` 속성이 `true`로 설정되면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 키가 보존됩니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all()->keyBy->id);
    });

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

보통 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단수형 리소스 클래스에 매핑한 결과로 자동 설정됩니다. 단수형 리소스 클래스는 컬렉션 클래스에서 `Collection` 부분을 제거한 이름으로 추정됩니다. 또한 취향에 따라 단수형 리소스 클래스에 `Resource` 접미사가 붙을 수도 있고 아닐 수도 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스를 `UserResource`로 매핑하려고 시도합니다. 이 동작을 커스터마이즈 하려면 컬렉션 리소스 클래스의 `$collects` 속성을 오버라이드할 수 있습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 이 리소스가 수집하는 리소스 클래스.
         *
         * @var string
         */
        public $collects = Member::class;
    }

<a name="writing-resources"></a>
## 리소스 작성하기

> [!NOTE]  
> [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 계속 읽기 전에 반드시 읽어볼 것을 권장합니다.

리소스는 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 모든 리소스는 모델의 속성을 API에 적합한 배열로 변환하는 `toArray` 메서드를 포함해야 하며, 이 배열은 라우트나 컨트롤러에서 반환할 수 있습니다:

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

리소스가 정의되면 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="relationships"></a>
#### 관계

응답에 연관된 다른 리소스도 포함하고 싶다면, 해당 리소스를 `toArray` 메서드에서 반환하는 배열에 추가하면 됩니다. 이 예시에서는 `PostResource`의 `collection` 메서드를 사용하여 사용자의 블로그 포스트를 응답에 추가합니다:

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

> [!NOTE]  
> 관련 관계가 이미 로드된 경우에만 포함하고 싶다면 [조건부 관계](#conditional-relationships) 항목을 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 하나의 모델을 배열로 변환하는 반면, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 하지만 모든 모델마다 별도의 리소스 컬렉션 클래스를 정의할 필요는 없습니다. 모든 리소스에는 "즉석" 리소스 컬렉션을 생성하는 `collection` 메서드가 제공되기 때문입니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

그러나 컬렉션에 반환되는 메타 데이터를 커스터마이즈해야 한다면, 직접 리소스 컬렉션 클래스를 정의해야 합니다:

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

단일 리소스와 마찬가지로, 리소스 컬렉션도 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="data-wrapping"></a>
### 데이터 감싸기

기본적으로 가장 바깥 리소스는 JSON으로 변환될 때 `data` 키로 감싸집니다. 즉, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

가장 바깥 리소스의 감싸기를 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 이 메서드는 보통 `AppServiceProvider`나 애플리케이션의 모든 요청에서 로드되는 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출하는 것이 좋습니다:

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

> [!WARNING]  
> `withoutWrapping` 메서드는 오직 가장 바깥 응답에만 영향을 주며, 직접 리소스 컬렉션에 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 감싸기

리소스의 관계가 어떻게 감싸질지 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 중첩 수준에 관계없이 `data` 키로 꼭 감싸고 싶다면, 각 리소스마다 리소스 컬렉션 클래스를 정의하고 `data` 키로 컬렉션을 반환하세요.

혹시 가장 바깥 리소스가 `data` 키로 두 번 감싸질까 걱정할 수 있지만, Laravel은 리소스를 이중으로 감싸지 않으므로 중첩 수준을 신경 쓰지 않아도 됩니다:

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

<a name="data-wrapping-and-pagination"></a>
#### 데이터 감싸기와 페이지네이션

리소스 응답을 통해 페이지네이션된 컬렉션을 반환할 때는, `withoutWrapping` 메서드를 호출했더라도 Laravel은 리소스 데이터를 무조건 `data` 키로 감쌉니다. 이는 페이지네이션 응답이 항상 페이지네이터의 상태 정보를 담은 `meta` 및 `links` 키를 포함하기 때문입니다:

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

리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 Laravel 페이지네이터 인스턴스를 전달할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::paginate());
    });

페이지네이션된 응답은 항상 페이지네이터의 상태 정보를 담은 `meta` 및 `links` 키를 포함합니다:

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

페이지네이션 응답의 `links`나 `meta` 키에 포함될 정보를 커스터마이즈하고 싶다면, 리소스에 `paginationInformation` 메서드를 정의하면 됩니다. 이 메서드는 `$paginated` 데이터와 기본 정보를 담은 `$default` 배열(즉, `links` 및 `meta` 키 포함)을 전달받습니다:

    /**
     * 리소스의 페이지네이션 정보 커스터마이즈.
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

<a name="conditional-attributes"></a>
### 조건부 속성

종종 특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 특정 값을 포함하고 싶을 수 있습니다. Laravel은 이를 위해 여러 헬퍼 메서드를 제공합니다. `when` 메서드는 조건부로 리소스 응답에 속성을 추가할 때 사용할 수 있습니다:

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

이 예시에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 포함됩니다. `false`를 반환하면 클라이언트로 전송되기 전에 `secret` 키는 응답에서 제거됩니다. `when` 메서드를 사용하면 조건문 없이도 직관적으로 리소스를 정의할 수 있습니다.

`when` 메서드의 두 번째 인자로 클로저를 전달해, 주어진 조건이 `true`일 때만 해당 값을 계산할 수도 있습니다:

    'secret' => $this->when($request->user()->isAdmin(), function () {
        return 'secret-value';
    }),

`whenHas` 메서드는 주어진 속성이 실제로 모델에 있을 때만 포함할 수 있습니다:

    'name' => $this->whenHas('name'),

또한, `whenNotNull` 메서드는 해당 속성이 null이 아닌 경우에만 응답에 포함합니다:

    'name' => $this->whenNotNull($this->name),

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

때로는 동일한 조건에서만 포함되어야 할 여러 속성이 있을 수 있습니다. 이 때는 `mergeWhen` 메서드를 이용해 조건이 `true`일 때만 여러 속성을 한 번에 추가할 수 있습니다:

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

마찬가지로, 조건이 `false`일 경우, 이 속성들은 최종 응답에서 제거됩니다.

> [!WARNING]  
> `mergeWhen` 메서드는 문자열 키와 숫자 키가 혼합된 배열, 혹은 숫자 키가 순차적이지 않은 배열 내에서는 사용해서는 안 됩니다.

<a name="conditional-relationships"></a>
### 조건부 관계

속성뿐만 아니라, 모델에 관계가 이미 로드되었는지 여부에 따라 응답에 조건부로 관계 데이터를 포함할 수 있습니다. 이를 통해 컨트롤러가 어떤 관계를 로드할지 결정할 수 있고, 리소스는 실제로 로드된 경우에만 관계를 포함할 수 있습니다. 궁극적으로 리소스 내 "N+1" 쿼리 문제를 더 쉽게 방지할 수 있습니다.

`whenLoaded` 메서드는 관계가 이미 로드된 경우에만 관계를 포함할 때 사용할 수 있습니다. 불필요한 관계 로드를 방지하기 위해, 이 메서드에는 관계명만 전달합니다:

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

이 예시에서 관계가 로드되지 않은 경우, `posts` 키는 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 카운트

관계 포함뿐만 아니라, 관계의 "카운트"가 이미 모델에 로드된 경우에만 카운트 값을 포함할 수도 있습니다:

    new UserResource($user->loadCount('posts'));

`whenCounted` 메서드는 관계의 카운트가 있을 때만 이를 응답에 포함합니다. 즉, 관계의 카운트가 없으면 응답에 사용되지 않습니다:

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

이 예시에서, `posts` 관계의 카운트가 로드되지 않았다면, `posts_count` 키는 응답에 포함되지 않습니다.

`avg`, `sum`, `min`, `max` 등 다른 유형의 집계도 `whenAggregated` 메서드로 조건부로 포함할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

조건부로 관계 정보를 포함하는 것뿐만 아니라, 다대다 관계의 중간 테이블 데이터도 `whenPivotLoaded` 메서드로 조건부 포함할 수 있습니다. 이 메서드는 첫 번째 인자로 피벗 테이블 이름, 두 번째 인자로 피벗 정보가 있을 때 반환할 값을 리턴하는 클로저를 받습니다:

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

관계가 [커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 사용한다면, 첫 번째 인자에 테이블 모델 인스턴스를 전달할 수 있습니다:

    'expires_at' => $this->whenPivotLoaded(new Membership, function () {
        return $this->pivot->expires_at;
    }),

중간 테이블에서 `pivot` 외의 다른 접근자를 사용한다면, `whenPivotLoadedAs` 메서드를 사용할 수도 있습니다:

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

<a name="adding-meta-data"></a>
### 메타 데이터 추가하기

일부 JSON API 표준은 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가하기를 요구합니다. 이는 일반적으로 리소스나 관련 리소스에 대한 `links` 정보, 또는 리소스 자체에 대한 메타 정보 등입니다. 리소스에 메타 데이터를 추가해야 한다면, `toArray` 메서드 내에 포함시켜 반환하면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 포함할 수 있습니다:

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

리소스에서 메타 데이터를 반환할 때, 페이지네이션된 응답에서 Laravel이 자동으로 추가하는 `links`, `meta` 키를 우발적으로 덮어쓸 걱정은 하지 않아도 됩니다. 따로 정의한 `links` 데이터는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

최상위 리소스일 때만 특정 메타 데이터를 응답에 포함하고 싶을 수 있습니다. 이런 경우, 응답 전체에 대한 메타 정보를 의미하는 경우가 많습니다. 이 메타 데이터는 리소스 클래스에 `with` 메서드를 추가하면 정의할 수 있습니다. 이 메서드는 최상위 리소스로 변환될 때만 메타 데이터를 포함하도록 배열을 반환해야 합니다:

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
         * 리소스 배열과 함께 반환해야 할 추가 데이터 가져오기.
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

<a name="adding-meta-data-when-constructing-resources"></a>
#### 리소스 인스턴스 생성 시 메타 데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때도 최상위 데이터를 추가할 수 있습니다. 모든 리소스에서 제공되는 `additional` 메서드는 응답에 추가로 포함할 데이터를 배열로 받을 수 있습니다:

    return (new UserCollection(User::all()->load('roles')))
        ->additional(['meta' => [
            'key' => 'value',
        ]]);

<a name="resource-responses"></a>
## 리소스 응답

앞서 본 것처럼, 리소스는 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

하지만 때로는 클라이언트로 전송하기 전에 나가는 HTTP 응답을 커스터마이즈해야 할 수 있습니다. 이를 수행하는 방법은 두 가지입니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하며, 응답 헤더 등을 완전히 제어할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user', function () {
        return (new UserResource(User::find(1)))
            ->response()
            ->header('X-Value', 'True');
    });

또는, 리소스 내에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 응답에서 최상위로 반환될 때 호출됩니다:

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
         * 리소스의 나가는 응답을 커스터마이즈합니다.
         */
        public function withResponse(Request $request, JsonResponse $response): void
        {
            $response->header('X-Value', 'True');
        }
    }
