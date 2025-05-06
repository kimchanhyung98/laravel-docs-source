# Eloquent: API 리소스

- [소개](#introduction)
- [리소스 생성하기](#generating-resources)
- [개념 개요](#concept-overview)
    - [리소스 컬렉션](#resource-collections)
- [리소스 작성하기](#writing-resources)
    - [데이터 래핑](#data-wrapping)
    - [페이지네이션](#pagination)
    - [조건부 속성](#conditional-attributes)
    - [조건부 관계](#conditional-relationships)
    - [메타데이터 추가](#adding-meta-data)
- [리소스 응답](#resource-responses)

<a name="introduction"></a>
## 소개

API를 구축할 때, Eloquent 모델과 실제로 사용자에게 반환되는 JSON 응답 사이에 변환 레이어가 필요할 수 있습니다. 예를 들어, 특정 사용자에게만 일부 속성을 표시하고 싶거나, 항상 모델의 JSON 표현에 특정 관계를 포함하고 싶을 수 있습니다. Eloquent의 리소스 클래스는 모델 및 모델 컬렉션을 JSON으로 변환하는 표현적이고 쉬운 방법을 제공합니다.

물론, 항상 Eloquent 모델이나 컬렉션의 `toJson` 메서드를 사용하여 JSON으로 변환할 수 있습니다. 하지만 Eloquent 리소스는 모델과 그 관계의 JSON 직렬화에 대해 더 세밀하고 강력한 제어를 제공합니다.

<a name="generating-resources"></a>
## 리소스 생성하기

리소스 클래스를 생성하려면 `make:resource` 아티즌(Artisan) 명령어를 사용할 수 있습니다. 기본적으로 리소스는 애플리케이션의 `app/Http/Resources` 디렉터리에 생성됩니다. 리소스는 `Illuminate\Http\Resources\Json\JsonResource` 클래스를 상속합니다:

    php artisan make:resource UserResource

<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스 외에도, 모델 컬렉션을 변환하는 리소스도 생성할 수 있습니다. 이를 통해, 리소스 컬렉션 전체와 관련된 링크나 기타 메타 정보도 JSON 응답에 포함시킬 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스를 생성할 때 `--collection` 플래그를 사용하세요. 또는 리소스 이름에 `Collection`을 포함하면, 라라벨이 컬렉션 리소스를 생성하도록 인식합니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 상속합니다:

    php artisan make:resource User --collection

    php artisan make:resource UserCollection

<a name="concept-overview"></a>
## 개념 개요

> {tip} 이 문서는 리소스와 리소스 컬렉션의 하이레벨 개요입니다. 리소스가 제공하는 맞춤화와 강력한 기능을 깊이 이해하려면 이 문서의 다른 섹션을 꼭 읽어보세요.

리소스를 작성할 때 사용 가능한 모든 옵션을 알아보기 전에, 우선 라라벨에서 리소스가 어떻게 사용되는지 하이레벨로 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 리소스를 배열로 변환합니다.
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

모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 라우트나 컨트롤러 메서드에서 리소스가 응답으로 반환될 때 JSON으로 변환할 속성의 배열을 반환합니다.

모델 속성에 `$this`를 통해 직접 접근할 수 있다는 점을 주목하세요. 이는 리소스 클래스가 속성과 메서드 접근을 자동으로 해당 모델로 프록시해주기 때문입니다. 리소스가 정의된 후에는 라우트나 컨트롤러에서 반환할 수 있습니다. 리소스는 생성자에서 대상 모델 인스턴스를 받습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function ($id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="resource-collections"></a>
### 리소스 컬렉션

리소스 컬렉션 또는 페이지네이션된 응답을 반환하려면, 리소스 클래스가 제공하는 `collection` 메서드를 사용하여 라우트나 컨트롤러에서 리소스 인스턴스를 생성해야 합니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

이 방법은 컬렉션과 함께 반환되어야 할 메타데이터를 추가할 수 없습니다. 리소스 컬렉션 응답을 커스터마이징하려면 컬렉션을 나타내는 별도의 리소스를 생성하세요:

    php artisan make:resource UserCollection

리소스 컬렉션 클래스가 생성되면, 응답에 포함할 메타데이터를 쉽게 정의할 수 있습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 리소스 컬렉션을 배열로 변환합니다.
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

정의한 리소스 컬렉션은 라우트 또는 컨트롤러에서 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존하기

라우트에서 리소스 컬렉션을 반환하면, 라라벨은 컬렉션의 키를 숫자 순서로 재설정합니다. 하지만, 리소스 클래스에 `preserveKeys` 속성을 추가하면 컬렉션의 원래 키를 보존할지 지정할 수 있습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 리소스 컬렉션의 키를 보존할지 여부
         *
         * @var bool
         */
        public $preserveKeys = true;
    }

`preserveKeys` 속성이 `true`로 설정된 경우, 컬렉션이 라우트 또는 컨트롤러에서 반환될 때 키가 보존됩니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all()->keyBy->id);
    });

<a name="customizing-the-underlying-resource-class"></a>
#### 하위 리소스 클래스 커스터마이징

일반적으로 컬렉션 리소스의 `$this->collection` 속성은 컬렉션의 각 아이템을 단일 리소스 클래스로 매핑한 결과로 자동 설정됩니다. 단일 리소스 클래스는 컬렉션의 클래스 이름에서 끝의 `Collection`을 뺀 이름으로 추정됩니다. 개인적인 선호에 따라, 단일 리소스 클래스에 `Resource` 접미사를 붙일 수도, 붙이지 않을 수도 있습니다.

예를 들어, `UserCollection`은 주어진 유저 인스턴스를 `UserResource` 리소스로 매핑합니다. 이 동작을 커스터마이즈 하려면, 리소스 컬렉션의 `$collects` 속성을 오버라이드하세요:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 이 리소스 컬렉션이 수집하는 리소스 클래스
         *
         * @var string
         */
        public $collects = Member::class;
    }

<a name="writing-resources"></a>
## 리소스 작성하기

> {tip} [개념 개요](#concept-overview)를 아직 읽지 않았다면, 이 문서를 진행하기 전에 꼭 읽어 보시길 권장합니다.

실질적으로, 리소스는 단순합니다. 특정 모델을 배열로 변환하면 됩니다. 그래서 각 리소스에는 모델의 속성을 API 친화적 배열로 변환하는 `toArray` 메서드가 들어 있습니다. 이 배열은 애플리케이션의 라우트나 컨트롤러에서 반환됩니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 리소스를 배열로 변환합니다.
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

리소스를 정의했다면, 라우트나 컨트롤러에서 곧바로 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function ($id) {
        return new UserResource(User::findOrFail($id));
    });

<a name="relationships"></a>
#### 관계

응답에 연관된 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드에서 반환하는 배열에 이를 추가하면 됩니다. 이 예제에서는 `PostResource` 리소스의 `collection` 메서드를 사용하여 사용자의 블로그 게시글을 리소스 응답에 추가합니다:

    use App\Http\Resources\PostResource;

    /**
     * 리소스를 배열로 변환합니다.
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

> {tip} 이미 로드된 관계만 포함하고 싶다면, [조건부 관계](#conditional-relationships) 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스는 단일 모델을 배열로 변환한다면, 리소스 컬렉션은 모델의 컬렉션을 배열로 변환합니다. 하지만, 모든 모델마다 별도의 리소스 컬렉션 클래스를 정의할 필요는 없습니다. 모든 리소스에는 "즉석" 리소스 컬렉션을 생성하는 `collection` 메서드가 있기 때문입니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/users', function () {
        return UserResource::collection(User::all());
    });

단, 컬렉션과 함께 반환되는 메타데이터를 커스터마이징해야 한다면, 자체적으로 리소스 컬렉션을 정의해야 합니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 리소스 컬렉션을 배열로 변환합니다.
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

단일 리소스처럼, 리소스 컬렉션도 라우트나 컨트롤러에서 바로 반환할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::all());
    });

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 리소스 응답이 JSON으로 변환될 때 가장 바깥쪽 리소스는 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같습니다:

    {
        "data": [
            {
                "id": 1,
                "name": "Eladio Schroeder Sr.",
                "email": "therese28@example.com",
            },
            {
                "id": 2,
                "name": "Liliana Mayert",
                "email": "evandervort@example.com",
            }
        ]
    }

기본 `data` 대신 임의의 키를 사용하고 싶다면, 리소스 클래스에 `$wrap` 속성을 정의하면 됩니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 적용될 "data" 래퍼
         *
         * @var string
         */
        public static $wrap = 'user';
    }

가장 바깥쪽 리소스의 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스의 `withoutWrapping` 메서드를 호출하세요. 보통 이 메서드는 모든 요청에 로드되는 `AppServiceProvider` 또는 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출해야 합니다:

    <?php

    namespace App\Providers;

    use Illuminate\Http\Resources\Json\JsonResource;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 등록
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스 부트스트랩
         *
         * @return void
         */
        public function boot()
        {
            JsonResource::withoutWrapping();
        }
    }

> {note} `withoutWrapping` 메서드는 최상위 응답에만 영향을 주며, 수동으로 추가한 `data` 키는 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑하기

리소스의 관계가 어떻게 래핑될지는 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 (중첩과 상관없이) `data` 키로 래핑하려면, 각 리소스별로 리소스 컬렉션 클래스를 정의하고 그 안에서 컬렉션을 `data` 키에 담아 반환하면 됩니다.

혹시 이렇게 하면 바깥 리소스가 두 번 `data` 키로 래핑될까 걱정할 수도 있지만, 라라벨은 결코 리소스를 이중 래핑하지 않으니 컬렉션의 중첩 수준을 신경 쓸 필요가 없습니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class CommentsCollection extends ResourceCollection
    {
        /**
         * 리소스 컬렉션을 배열로 변환합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return array
         */
        public function toArray($request)
        {
            return ['data' => $this->collection];
        }
    }

<a name="data-wrapping-and-pagination"></a>
#### 데이터 래핑과 페이지네이션

페이지네이션된 컬렉션을 리소스 응답으로 반환할 때는, `withoutWrapping`을 호출했더라도 리소스 데이터는 `data` 키로 래핑됩니다. 이는 페이지네이션 응답에 항상 페이지네이터 상태와 관련된 `meta`, `links` 키가 포함되기 때문입니다:

    {
        "data": [
            {
                "id": 1,
                "name": "Eladio Schroeder Sr.",
                "email": "therese28@example.com",
            },
            {
                "id": 2,
                "name": "Liliana Mayert",
                "email": "evandervort@example.com",
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

<a name="pagination"></a>
### 페이지네이션

라라벨 페이지네이터 인스턴스를 리소스의 `collection` 메서드나 커스텀 리소스 컬렉션에 전달할 수 있습니다:

    use App\Http\Resources\UserCollection;
    use App\Models\User;

    Route::get('/users', function () {
        return new UserCollection(User::paginate());
    });

페이지네이션 응답에는 항상 페이지네이터 상태와 관련된 `meta`, `links` 키가 포함됩니다:

    {
        "data": [
            {
                "id": 1,
                "name": "Eladio Schroeder Sr.",
                "email": "therese28@example.com",
            },
            {
                "id": 2,
                "name": "Liliana Mayert",
                "email": "evandervort@example.com",
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

<a name="conditional-attributes"></a>
### 조건부 속성

특정 조건이 충족될 때만 리소스 응답에 속성을 포함하고 싶을 때가 있습니다. 예를 들어, 현재 사용자가 "관리자"일 때만 값을 포함하고 싶을 수 있습니다. 라라벨은 이런 상황에서 도움이 되는 다양한 헬퍼 메서드를 제공합니다. `when` 메서드를 사용하면 조건부로 속성을 응답에 추가할 수 있습니다:

    use Illuminate\Support\Facades\Auth;

    /**
     * 리소스를 배열로 변환합니다.
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
            'secret' => $this->when(Auth::user()->isAdmin(), 'secret-value'),
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }

이 예시에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 때만 최종 리소스 응답에 포함됩니다. `false`를 반환한다면, 클라이언트로 전송되기 전 리소스 응답에서 `secret` 키가 제거됩니다. `when` 메서드는 배열 구성시 조건문을 사용하지 않고도 리소스를 표현적으로 정의할 수 있게 해줍니다.

`when` 메서드는 두 번째 인자로 클로저도 받으므로, 조건이 `true`일 때만 값을 계산할 수 있습니다:

    'secret' => $this->when(Auth::user()->isAdmin(), function () {
        return 'secret-value';
    }),

<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

동일한 조건을 기준으로 여러 속성을 리소스 응답에 포함하고 싶을 때가 있습니다. 이런 경우 `mergeWhen` 메서드를 사용하여 조건이 `true`일 때만 여러 속성을 응답에 포함할 수 있습니다:

    /**
     * 리소스를 배열로 변환합니다.
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
            $this->mergeWhen(Auth::user()->isAdmin(), [
                'first-secret' => 'value',
                'second-secret' => 'value',
            ]),
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }

조건이 `false`일 경우, 이 속성들은 응답에서 제거됩니다.

> {note} `mergeWhen` 메서드는 문자열과 숫자 키가 혼합된 배열이나, 순차적이지 않은 숫자 키가 있는 배열 내에서 사용해서는 안됩니다.

<a name="conditional-relationships"></a>
### 조건부 관계

속성 로드뿐만 아니라, 리소스 응답에 모델에 이미 로드된 관계만 조건부로 포함할 수 있습니다. 이렇게 하면 어떤 관계를 로드할지는 컨트롤러에서 결정하고 실제로 로드된 관계만 리소스에 포함시킬 수 있습니다. 궁극적으로 이는 리소스 내에서 "N+1" 쿼리 문제를 더 쉽게 피할 수 있게 해 줍니다.

`whenLoaded` 메서드는 관계 이름을 받아 조건부로 관계를 불러올 때 사용할 수 있습니다. 불필요하게 관계를 로드하지 않도록, 이 메서드는 관계 자체가 아닌 이름을 인자로 받습니다:

    use App\Http\Resources\PostResource;

    /**
     * 리소스를 배열로 변환합니다.
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

이 예에서 관계가 로드되지 않았다면, `posts` 키는 클라이언트로 전송되기 전 응답에서 제거됩니다.

<a name="conditional-pivot-information"></a>
#### 조건부 중간 테이블(pivot) 정보

관계 정보를 리소스 응답에 조건부로 포함하는 것뿐만 아니라, 다대다(many-to-many) 관계의 중간 테이블 정보도 `whenPivotLoaded` 메서드로 조건부로 포함할 수 있습니다. `whenPivotLoaded`는 첫번째 인자로 피벗(중간) 테이블 이름, 두번째 인자로는 피벗 정보가 모델에 있을 경우 값을 반환하는 클로저를 받습니다:

    /**
     * 리소스를 배열로 변환합니다.
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

관계가 [커스텀 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 이용한다면, `whenPivotLoaded`의 첫 번째 인자로 중간 테이블 모델 인스턴스를 전달하세요:

    'expires_at' => $this->whenPivotLoaded(new Membership, function () {
        return $this->pivot->expires_at;
    }),

중간 테이블에서 `pivot` 외의 접근자를 사용하는 경우, `whenPivotLoadedAs` 메서드를 사용할 수 있습니다:

    /**
     * 리소스를 배열로 변환합니다.
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

<a name="adding-meta-data"></a>
### 메타데이터 추가

일부 JSON API 표준은 리소스 및 리소스 컬렉션 응답에 메타데이터 추가를 요구합니다. 이는 주로, 리소스나 관련 리소스로의 `links`, 또는 리소스 자체의 메타데이터 등이 포함됩니다. 리소스에 추가 메타데이터를 반환해야 한다면, `toArray` 메서드 내에서 같이 반환하세요. 예를 들어, 리소스 컬렉션 변환 시 `links` 정보를 포함할 수 있습니다:

    /**
     * 리소스를 배열로 변환합니다.
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

리소스에서 추가 메타데이터를 반환할 때, 라라벨이 페이지네이션 응답에서 자동으로 추가하는 `links`, `meta` 키를 덮어쓸 염려는 하지 않아도 됩니다. 직접 정의한 `links`는 페이지네이터가 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타데이터

때로는 리소스가 최상위 리소스로 반환될 때만 특정 메타데이터를 포함하고 싶을 수 있습니다. 보통 전체 응답에 대한 메타 정보가 이에 해당합니다. 이런 메타데이터를 정의하려면, 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 리소스가 변환될 때 최상위일 경우에만 포함할 메타데이터 배열을 반환해야 합니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\ResourceCollection;

    class UserCollection extends ResourceCollection
    {
        /**
         * 리소스 컬렉션을 배열로 변환합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return array
         */
        public function toArray($request)
        {
            return parent::toArray($request);
        }

        /**
         * 리소스 배열과 함께 반환해야 할 추가 데이터
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

<a name="adding-meta-data-when-constructing-resources"></a>
#### 리소스 생성 시 메타데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용 가능한 `additional` 메서드는 응답에 추가될 데이터를 배열로 받습니다:

    return (new UserCollection(User::all()->load('roles')))
                    ->additional(['meta' => [
                        'key' => 'value',
                    ]]);

<a name="resource-responses"></a>
## 리소스 응답

앞서 읽은 것처럼, 리소스는 라우트 및 컨트롤러에서 직접 반환할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user/{id}', function ($id) {
        return new UserResource(User::findOrFail($id));
    });

그러나 때로는 클라이언트로 전송되기 전에 HTTP 응답을 커스터마이즈해야 할 수도 있습니다. 이를 위한 방법은 두 가지입니다. 첫 번째로, 리소스에 `response` 메서드를 체이닝할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하므로, 응답 헤더를 완전히 제어할 수 있습니다:

    use App\Http\Resources\UserResource;
    use App\Models\User;

    Route::get('/user', function () {
        return (new UserResource(User::find(1)))
                    ->response()
                    ->header('X-Value', 'True');
    });

또는 리소스 내부에 `withResponse` 메서드를 정의할 수도 있습니다. 이 메서드는 리소스가 응답의 최상위 리소스로 반환될 때 호출됩니다:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class UserResource extends JsonResource
    {
        /**
         * 리소스를 배열로 변환합니다.
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
         * 리소스의 응답을 커스터마이즈합니다.
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