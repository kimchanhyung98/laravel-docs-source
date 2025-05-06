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

API를 구축할 때, Eloquent 모델과 실제로 애플리케이션 사용자에게 반환되는 JSON 응답 사이에 변환 레이어가 필요할 수 있습니다. 예를 들어, 특정 사용자 집합에 대해서만 특정 속성을 표시하거나, 모델의 JSON 표현에 항상 특정 관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델 및 모델 컬렉션을 JSON으로 표현력 있게 그리고 쉽게 변환할 수 있도록 해줍니다.

물론, `toJson` 메서드를 사용하여 언제든지 Eloquent 모델이나 컬렉션을 JSON으로 변환할 수 있습니다. 하지만, Eloquent 리소스는 모델 및 그 관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어가 가능합니다.

<a name="generating-resources"></a>
## 리소스 생성

리소스 클래스를 생성하려면 `make:resource` Artisan 명령을 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉토리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 확장합니다:

```shell
php artisan make:resource UserResource
```

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스뿐만 아니라, 모델 컬렉션 전체를 변환하는 역할을 하는 리소스도 생성할 수 있습니다. 이를 통해 JSON 응답에 링크나 관련 메타 정보와 같은 컬렉션 전체에 해당하는 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스를 생성할 때 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection`이라는 단어를 포함하면 Laravel은 컬렉션 리소스를 생성합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```

<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]  
> 이 섹션은 리소스 및 리소스 컬렉션의 상위 개요를 설명합니다. 리소스가 제공하는 맞춤화와 강력한 기능을 더 깊이 이해하려면 문서의 다른 섹션을 꼭 읽어보시기 바랍니다.

리소스를 작성하면서 사용 가능한 모든 옵션을 살펴보기 전에, 먼저 Laravel에서 리소스가 어떻게 사용되는지 상위 수준에서 알아보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 표현합니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 경로나 컨트롤러에서 리소스를 응답으로 반환할 때 JSON으로 변환할 속성 배열을 반환합니다.

모델의 프로퍼티를 `$this` 변수에서 직접 접근할 수 있다는 점에 유의하세요. 이는 리소스 클래스가 자동으로 속성 및 메서드 접근을 기본 모델에 위임하기 때문입니다. 리소스를 정의하면, 경로나 컨트롤러에서 다음과 같이 반환할 수 있습니다. 리소스는 생성자를 통해 해당 모델 인스턴스를 받습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스의 컬렉션이나 페이지네이션된 응답을 반환하려면, 경로나 컨트롤러에서 리소스 인스턴스를 생성할 때 리소스 클래스의 `collection` 메서드를 사용해야 합니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

이 방법은 컬렉션과 함께 반환해야 하는 커스텀 메타 데이터를 추가할 수 없습니다. 컬렉션 응답을 커스텀하고 싶다면, 컬렉션을 표현하는 전용 리소스를 만들어야 합니다:

```shell
php artisan make:resource UserCollection
```

컬렉션 리소스 클래스를 생성한 후, 응답에 포함해야 할 메타 데이터를 쉽게 정의할 수 있습니다:

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

정의된 컬렉션 리소스는 경로나 컨트롤러에서 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

경로에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 초기화합니다. 하지만, 컬렉션의 원래 키를 보존하도록 리소스 클래스에 `preserveKeys` 프로퍼티를 추가할 수 있습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 리소스 컬렉션 키 보존 여부
         *
         * @var bool
         */
        public $preserveKeys = true;
    }

`preserveKeys` 프로퍼티를 `true`로 설정하면, 경로나 컨트롤러에서 컬렉션을 반환할 때 컬렉션의 키가 보존됩니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all()->keyBy->id);
    });

<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 커스터마이징

일반적으로, 리소스 컬렉션의 `$this->collection` 프로퍼티는 컬렉션의 각 항목을 단일 리소스 클래스로 매핑한 결과로 자동 설정됩니다. 단일 리소스 클래스는 컬렉션 클래스명에서 마지막 `Collection` 부분을 뺀 클래스명으로 간주합니다. 또한, 개인 취향에 따라 단수 리소스 클래스가 `Resource`로 끝나거나 끝나지 않을 수 있습니다.

예를 들어, `UserCollection`은 주어진 사용자 인스턴스를 `UserResource` 리소스로 매핑하려고 시도합니다. 이 동작을 커스터마이징하려면 리소스 컬렉션의 `$collects` 속성을 오버라이드할 수 있습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 이 리소스가 모으는 리소스.
         *
         * @var string
         */
        public $collects = Member::class;
    }

<a name="writing-resources"></a>
## 리소스 작성

> [!NOTE]  
> [개념 개요](#concept-overview)를 아직 읽지 않았다면, 본 문서를 진행하기 전에 꼭 읽어보시기 바랍니다.

리소스는 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 리소스는 모델의 속성을 API 친화적인 배열로 변환하는 `toArray` 메서드를 포함하고 있으며, 이 배열은 애플리케이션의 경로나 컨트롤러에서 반환될 수 있습니다:

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

리소스를 정의하면, 이를 경로나 컨트롤러에서 직접 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="relationships"></a>
#### 관계

응답에 연관된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 이를 추가하면 됩니다. 아래 예제에서는 `PostResource` 리소스의 `collection` 메서드를 사용해 사용자의 블로그 포스트를 리소스 응답에 포함합니다:

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
> 관계가 이미 로드된 경우에만 포함하도록 하려면, [조건부 관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스는 단일 모델을 배열로 변환하는 반면, 컬렉션 리소스는 모델의 컬렉션을 배열로 변환합니다. 하지만 모든 모델에 대해 리소스 컬렉션 클래스를 반드시 정의할 필요는 없습니다. 모든 리소스에는 "즉석" 리소스 컬렉션을 생성하는 `collection` 메서드가 존재하기 때문입니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

하지만, 컬렉션과 함께 반환되는 메타 데이터를 커스터마이징해야 한다면, 별도의 컬렉션 리소스를 정의해야 합니다:

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

단일 리소스처럼, 컬렉션 리소스 또한 경로나 컨트롤러에서 바로 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 가장 외부의 리소스는 리소스 응답이 JSON으로 변환될 때 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

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

만약 가장 외부 리소스의 래핑을 비활성화하고 싶다면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하면 됩니다. 일반적으로 이 메서드는 애플리케이션의 모든 요청에서 로드되는 `AppServiceProvider` 또는 다른 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출해야 합니다:

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
> `withoutWrapping` 메서드는 가장 외부의 응답에만 영향을 주며, 직접 리소스 컬렉션에 추가한 `data` 키를 제거해주지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

관계 래핑 방식을 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 중첩 수준에 상관없이 `data` 키로 래핑하고 싶다면, 각 리소스에 대해 리소스 컬렉션 클래스를 정의하고, `data` 키 내에 컬렉션을 반환하면 됩니다.

이렇게 하면 최상위 리소스가 `data` 키로 두 번 래핑될지 궁금할 수 있습니다. 걱정하지 마세요. Laravel은 리소스가 실수로 두 번 래핑되는 것을 방지하므로, 변환할 리소스 컬렉션의 중첩 정도에 대해 걱정할 필요가 없습니다:

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
#### 데이터 래핑 및 페이지네이션

리소스 응답을 통해 페이지네이션된 컬렉션을 반환할 때, `withoutWrapping` 메서드를 호출했더라도 Laravel은 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지네이션 응답에 항상 페이지네이터 상태에 관한 `meta` 및 `links` 키가 포함되기 때문입니다:

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

페이지네이션 응답은 항상 페이지네이터 상태 정보를 담은 `meta`와 `links` 키를 포함합니다:

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

페이지네이션 응답의 `links` 또는 `meta` 키에 포함되는 정보를 커스터마이징하려면, 리소스에서 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 기본적으로 포함된 `$default` 배열(즉, `links`, `meta` 키 포함)을 받습니다:

    /**
     * 리소스의 페이지네이션 정보 커스터마이징
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

특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하고 싶을 수 있습니다. Laravel은 이러한 상황을 위한 다양한 헬퍼 메서드를 제공합니다. `when` 메서드를 사용하여 조건부로 속성을 리소스 응답에 추가할 수 있습니다:

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

이 예시에서, 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 `secret` 키가 포함됩니다. 이 메서드가 `false`를 반환한다면, 클라이언트에 응답이 전달되기 전에 `secret` 키는 리소스 응답에서 제거됩니다. `when` 메서드를 사용하면, 배열을 빌드할 때 조건문을 작성하지 않고도 표현력 있게 리소스를 정의할 수 있습니다.

`when` 메서드는 두 번째 인수로 클로저도 받을 수 있으며, 조건이 `true`일 때만 최종 값을 계산합니다.

    'secret' => $this->when($request->user()->isAdmin(), function () {
        return 'secret-value';
    }),

`whenHas` 메서드는 실제로 모델에 해당 속성이 있을 때만 속성을 포함하도록 사용됩니다:

    'name' => $this->whenHas('name'),

또한, `whenNotNull` 메서드는 속성이 null이 아닐 때만 리소스 응답에 포함할 수 있게 해줍니다:

    'name' => $this->whenNotNull($this->name),

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

같은 조건에 따라 여러 속성을 리소스 응답에 포함해야 할 수도 있습니다. 이럴 때는, `mergeWhen` 메서드를 사용하여 지정한 조건이 `true`일 때만 여러 속성을 응답에 포함할 수 있습니다:

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

조건이 `false`인 경우, 해당 속성들은 클라이언트로 보내지기 전에 리소스 응답에서 제거됩니다.

> [!WARNING]  
> `mergeWhen` 메서드는 문자열 및 숫자 키가 혼합된 배열 안에서, 또는 순서대로 정렬되지 않은 숫자 키가 있는 배열 안에서는 사용하지 않아야 합니다.

<a name="conditional-relationships"></a>
### 조건부 관계

속성을 조건부로 로드할 뿐만 아니라, 리소스 응답에 포함할 관계도 모델에 해당 관계가 이미 로드된 경우에만 포함할 수 있습니다. 이를 통해 컨트롤러에서 모델에 어떤 관계를 로드할지 결정하고, 리소스에서는 실제로 로드된 경우에만 포함할 수 있습니다. 결과적으로, 리소스 내에서 "N+1" 쿼리 문제를 쉽게 방지할 수 있습니다.

`whenLoaded` 메서드는 관계가 이미 로드된 경우에만 포함하도록 해줍니다. 불필요하게 관계를 로드하는 것을 피하기 위해, 이 메서드는 관계 자체가 아닌 관계의 이름을 받습니다:

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

이 예제에서, 해당 관계가 로드되어 있지 않으면, 최종 리소스 응답에서 `posts` 키가 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 카운트

조건부로 관계를 포함하는 것 이외에도, 모델에 해당 관계의 카운트가 로드되어 있으면 관계 "카운트"를 리소스 응답에 포함할 수 있습니다:

    new UserResource($user->loadCount('posts'));

`whenCounted` 메서드는 관계의 카운트가 로드되어 있는 경우에만 리소스 응답에 카운트를 포함합니다. 카운트가 없으면 불필요하게 속성이 포함되지 않습니다.

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

이 예시에서, `posts` 관계의 카운트가 로드되어 있지 않으면, `posts_count` 키가 최종 리소스 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max`와 같은 다른 집계(aggregate)도 `whenAggregated` 메서드로 조건부로 로드할 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

<a name="conditional-pivot-information"></a>
#### 조건부 Pivot 정보

리소스 응답에 관계 정보를 조건부로 포함시키는 것 외에도, `whenPivotLoaded` 메서드를 사용하여 다대다(many-to-many) 관계의 중간 테이블 데이터도 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인수로 피벗 테이블 이름을, 두 번째 인수로는 피벗 정보가 모델에 있을 때 반환할 값을 담은 클로저를 받습니다:

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

관계가 [커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 사용한다면, `whenPivotLoaded`의 첫 번째 인수로 중간 테이블 모델 인스턴스를 전달할 수 있습니다:

    'expires_at' => $this->whenPivotLoaded(new Membership, function () {
        return $this->pivot->expires_at;
    }),

중간 테이블이 `pivot` 이외의 접근자를 사용할 경우, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

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
### 메타 데이터 추가

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터 추가를 요구합니다. 이는 보통 리소스나 관련 리소스에 대한 `links`, 리소스 자체에 관한 메타 데이터 등이 포함됩니다. 리소스에 추가 메타 데이터를 반환하려면, `toArray` 메서드에 이를 포함시키면 됩니다. 예를 들어, 리소스 컬렉션 변환 시 `link` 정보를 포함할 수 있습니다:

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

리소스에서 추가 메타 데이터를 반환할 때, 페이지네이션 응답에서 Laravel이 자동으로 추가하는 `links` 또는 `meta` 키를 실수로 덮어쓸 걱정은 필요 없습니다. 추가로 정의한 `links` 값은 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 루트 레벨 메타 데이터

때로는 자원 응답에서 루트(최상위) 리소스일 때만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 보통 응답 전체에 대한 메타 정보를 포함합니다. 이러한 메타 데이터를 정의하려면, 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 최상위 리소스가 변환될 때만 응답에 포함할 메타 데이터 배열을 반환해야 합니다:

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
         * 리소스 배열과 함께 반환할 추가 데이터
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
#### 리소스 생성 시 메타 데이터 추가

경로나 컨트롤러에서 리소스 인스턴스를 생성할 때 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용 가능한 `additional` 메서드는 리소스 응답에 추가할 데이터를 배열로 받습니다:

    return (new UserCollection(User::all()->load('roles')))
                    ->additional(['meta' => [
                        'key' => 'value',
                    ]]);

<a name="resource-responses"></a>
## 리소스 응답

이미 읽으셨듯이, 리소스는 경로나 컨트롤러에서 직접 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function (string $id) {
        return new UserResource(User::findOrFail($id));
    });

그러나 클라이언트로 응답이 전송되기 전에 HTTP 응답을 커스터마이징해야 하는 경우도 있습니다. 이를 달성하는 방법은 두 가지가 있습니다. 먼저, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로 응답 헤더를 완전히 제어할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user', function () {
        return (new UserResource(User::find(1)))
                    ->response()
                    ->header('X-Value', 'True');
    });

또는, 리소스 내부에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 응답의 최상위 리소스로 반환될 때 호출됩니다:

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
         * 리소스의 아웃고잉 응답 커스터마이징
         */
        public function withResponse(Request $request, JsonResponse $response): void
        {
            $response->header('X-Value', 'True');
        }
    }
