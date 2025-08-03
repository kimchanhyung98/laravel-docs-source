# 릴리스 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 9](#laravel-9)

<a name="versioning-scheme"></a>
## 버전 관리 체계 (Versioning Scheme)

Laravel과 기타 공식 패키지들은 [Semantic Versioning](https://semver.org)을 준수합니다. 주요 프레임워크 버전은 매년 약 2월에 출시되며, 마이너 및 패치 릴리스는 주 단위로 자주 이루어질 수 있습니다. 마이너 및 패치 릴리스에는 **절대** 파괴적 변경사항은 포함되지 않습니다.

애플리케이션이나 패키지에서 Laravel 프레임워크나 그 컴포넌트를 참조할 때는 `^9.0` 같은 버전 제약 조건을 사용하는 것이 좋습니다. 주요 릴리스에서는 파괴적 변경이 있을 수 있기 때문입니다. 하지만 새로운 주요 릴리스로 1일 이내에 안전하게 업데이트할 수 있도록 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수 (Named Arguments)

[명명된 인수](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스를 개선하기 위해 필요에 따라 함수 인수 이름을 변경할 수 있으므로, Laravel 메서드를 호출할 때 명명된 인수를 사용하는 경우 향후 파라미터 이름이 변경될 수 있음을 유념하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리스는 버그 수정이 18개월, 보안 수정은 2년간 제공합니다. Lumen을 포함한 기타 라이브러리들은 최신 주요 릴리스에만 버그 수정이 제공됩니다. 또한 Laravel에서 지원하는 데이터베이스 버전을 꼭 확인하시기 바랍니다. ([지원 데이터베이스 버전](https://laravel.com/docs/9.x/database#introduction))

| 버전    | PHP (*)       | 출시일          | 버그 수정 종료일  | 보안 수정 종료일  |
| ------- | ------------- | --------------- | ---------------- | ----------------- |
| 6 (LTS) | 7.2 - 8.0     | 2019년 9월 3일  | 2022년 1월 25일  | 2022년 9월 6일    |
| 7       | 7.2 - 8.0     | 2020년 3월 3일  | 2020년 10월 6일  | 2021년 3월 3일    |
| 8       | 7.3 - 8.1     | 2020년 9월 8일  | 2022년 7월 26일  | 2023년 1월 24일   |
| 9       | 8.0 - 8.2     | 2022년 2월 8일  | 2023년 8월 8일   | 2024년 2월 6일    |
| 10      | 8.1 - 8.3     | 2023년 2월 14일 | 2024년 8월 6일   | 2025년 2월 4일    |

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>End of life</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>Security fixes only</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-9"></a>
## Laravel 9

이미 아시다시피 Laravel은 Laravel 8 릴리스부터 매년 릴리스 주기로 전환했습니다. 이전에는 주요 버전이 6개월마다 출시되었습니다. 이 전환은 커뮤니티의 유지보수 부담을 줄이고, 파괴적 변경 없이도 놀랍고 강력한 새 기능을 빠르게 제공하는 데에 도움을 주고자 하는 의도입니다. 예를 들어 Laravel 8에서는 병렬 테스트 지원, 개선된 Breeze 스타터 킷, HTTP 클라이언트 개선, "has one of many" 같은 새로운 Eloquent 관계 유형 등 다양한 강력한 기능들이 하위 호환성을 깨지 않고 출시되었습니다.

이런 약속에 따라 현재 릴리스에서는 놀라운 새 기능 제공에 집중하며, 미래의 "주요" 릴리스들은 상위 의존성 업그레이드 등의 "유지보수" 작업 위주가 될 가능성이 큽니다. 이는 이 릴리스 노트에서도 확인할 수 있습니다.

Laravel 9는 Symfony 6.0 컴포넌트, Symfony Mailer, Flysystem 3.0 지원, 향상된 `route:list` 출력, Laravel Scout 데이터베이스 드라이버, 새로운 Eloquent Accessor / Mutator 문법, Enums를 이용한 암묵적 라우트 바인딩 등 다양한 버그 수정 및 사용성 개선을 이어가고 있습니다.

<a name="php-8"></a>
### PHP 8.0

Laravel 9.x는 PHP 8.0 이상을 요구합니다.

<a name="symfony-mailer"></a>
### Symfony Mailer

_Symfony Mailer 지원은 [Dries Vints](https://github.com/driesvints), [James Brooks](https://github.com/jbrooksuk), [Julius Kiekbusch](https://github.com/Jubeki) 님이 기여했습니다._

이전 버전에서는 [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html)를 사용해 이메일을 발송했지만, 이제는 유지보수가 중단되어 Symfony Mailer로 대체되었습니다.

자세한 내용과 호환성 확인을 위해 [업그레이드 가이드](/docs/9.x/upgrade#symfony-mailer)를 참고하세요.

<a name="flysystem-3"></a>
### Flysystem 3.x

_Flysystem 3.x 지원은 [Dries Vints](https://github.com/driesvints) 님이 기여했습니다._

Laravel 9.x는 파일 시스템 조작의 근간인 Flysystem을 3.x 버전으로 업그레이드했습니다. Flysystem은 `Storage` 파사드가 제공하는 모든 파일 시스템 기능을 담당합니다.

자세한 내용과 호환성 확인을 위해 [업그레이드 가이드](/docs/9.x/upgrade#flysystem-3)를 참고하세요.

<a name="eloquent-accessors-and-mutators"></a>
### 향상된 Eloquent Accessors / Mutators

_향상된 Eloquent Accessors / Mutators는 [Taylor Otwell](https://github.com/taylorotwell) 님이 기여했습니다._

Laravel 9.x는 Eloquent의 [액세서(accessor)와 뮤테이터(mutator)](/docs/9.x/eloquent-mutators#accessors-and-mutators)를 정의하는 새로운 방식을 도입했습니다. 이전 버전에서는 접두사가 붙은 메서드로만 정의할 수 있었습니다:

```php
public function getNameAttribute($value)
{
    return strtoupper($value);
}

public function setNameAttribute($value)
{
    $this->attributes['name'] = $value;
}
```

하지만 Laravel 9.x부터는 `Illuminate\Database\Eloquent\Casts\Attribute` 타입 힌트를 반환하는 단일 접두사 없는 메서드로 정의할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

public function name(): Attribute
{
    return new Attribute(
        get: fn ($value) => strtoupper($value),
        set: fn ($value) => $value,
    );
}
```

또한, 이 새로운 접근법은 커스텀 캐스트 클래스와 마찬가지로 반환되는 객체 값을 캐시합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

public function address(): Attribute
{
    return new Attribute(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="enum-casting"></a>
### Enum Eloquent 속성 캐스팅

> [!WARNING]
> Enum 캐스팅은 PHP 8.1 이상에서만 사용 가능합니다.

_Enum 캐스팅은 [Mohamed Said](https://github.com/themsaid) 님이 기여했습니다._

Eloquent는 이제 PHP의 백된(Enum backed) [Enum](https://www.php.net/manual/en/language.enumerations.backed.php)으로 속성 값을 캐스팅할 수 있습니다. 모델의 `$casts` 속성 배열에 속성과 enum을 지정하면 됩니다:

```
use App\Enums\ServerStatus;

/**
 * 캐스팅이 적용될 속성들
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

모델에서 캐스팅을 정의하면 해당 속성에 접근하거나 변경할 때 자동으로 Enum 타입과 상호 변환됩니다:

```
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="implicit-route-bindings-with-enums"></a>
### Enums를 이용한 암묵적 라우트 바인딩

_암묵적 Enum 바인딩은 [Nuno Maduro](https://github.com/nunomaduro) 님이 기여했습니다._

PHP 8.1은 [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)를 지원합니다. Laravel 9.x는 라우트 정의에서 Enum 타입 힌트를 지정할 수 있도록 하여, URL 경로에서 해당 세그먼트가 유효한 Enum 값이면 라우트를 실행합니다. 그렇지 않으면 자동으로 HTTP 404 응답을 반환합니다. 예를 들어, 다음과 같은 Enum이 있다면:

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

라우트는 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 호출됩니다. 그렇지 않으면 HTTP 404가 반환됩니다:

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="forced-scoping-of-route-bindings"></a>
### 강제 스코핑된 라우트 바인딩

_강제 스코핑 바인딩은 [Claudio Dekker](https://github.com/claudiodekker) 님이 기여했습니다._

이전 버전에서 라우트 정의 시 두 번째 Eloquent 모델을 첫 번째 모델의 자식 관계로 강제 범위 설정(scoping)하는 경우가 있었습니다. 예를 들어 특정 사용자에 해당하는 slug로 블로그 게시물을 조회하는 라우트:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

커스텀 키로 암묵적 바인딩을 할 때 Laravel은 부모-자식 관계를 추론하여 자동으로 자식 모델 쿼리를 부모 범위로 제한합니다. 그러나 이 기능은 이전에 커스텀 키를 사용할 때만 작동했습니다.

Laravel 9.x부터는 커스텀 키가 없어도 `scopeBindings` 메서드를 호출해 "자식" 바인딩의 범위를 설정할 수 있습니다:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또한, 라우트 그룹 전체에 대해 스코프 바인딩을 적용할 수도 있습니다:

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="controller-route-groups"></a>
### 컨트롤러 라우트 그룹

_라우트 그룹 개선은 [Luke Downing](https://github.com/lukeraymonddowning) 님이 기여했습니다._

이제 `controller` 메서드를 사용해 라우트 그룹 전체의 공통 컨트롤러를 지정할 수 있습니다. 그런 다음 각 라우트에서는 호출할 컨트롤러 메서드명만 지정하면 됩니다:

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="full-text"></a>
### 전문 검색 인덱스 및 WHERE 절

_전문 검색 인덱스와 "where" 절 기능은 [Taylor Otwell](https://github.com/taylorotwell)과 [Dries Vints](https://github.com/driesvints) 님이 기여했습니다._

MySQL 또는 PostgreSQL 사용 시, 컬럼 정의에 `fullText` 메서드를 사용해 전문 검색 인덱스를 생성할 수 있습니다:

```
$table->text('bio')->fullText();
```

또한, `whereFullText`와 `orWhereFullText` 메서드를 이용해 전문 검색 인덱스가 적용된 컬럼에 대해 전문 검색 조건을 추가할 수 있습니다. 내부적으로 데이터베이스에 맞는 적절한 SQL 문법으로 변환됩니다. 예를 들어, MySQL에서는 `MATCH AGAINST` 구문으로 변환됩니다:

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="laravel-scout-database-engine"></a>
### Laravel Scout 데이터베이스 엔진

_Laravel Scout 데이터베이스 엔진은 [Taylor Otwell](https://github.com/taylorotwell)과 [Dries Vints](https://github.com/driesvints) 님이 기여했습니다._

애플리케이션이 작은 규모거나 중간 규모 데이터베이스를 사용하거나 작업 부하가 적다면, 전용 검색 서비스(Algolia, MeiliSearch 등) 대신 Scout의 "database" 엔진을 사용할 수 있습니다. 이 엔진은 기존 데이터베이스에서 "where like" 조건과 전문 검색 인덱스를 이용해 쿼리를 필터링하여 검색 결과를 제공합니다.

Scout 데이터베이스 엔진에 대해 더 알고 싶으면 [Scout 문서](/docs/9.x/scout)를 참고하세요.

<a name="rendering-inline-blade-templates"></a>
### 인라인 Blade 템플릿 렌더링

_인라인 Blade 템플릿 렌더링은 [Jason Beggs](https://github.com/jasonlbeggs), 인라인 Blade 컴포넌트 렌더링은 [Toby Zerner](https://github.com/tobyzerner) 님이 기여했습니다._

때로는 원시 Blade 템플릿 문자열을 HTML로 변환해야 할 때가 있습니다. `Blade` 파사드의 `render` 메서드를 사용해 다음과 같이 처리할 수 있습니다. 이 메서드는 템플릿 문자열과 선택적인 데이터 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

마찬가지로, `renderComponent` 메서드로 클래스 컴포넌트를 렌더링할 수 있으며, 컴포넌트 인스턴스를 인수로 전달합니다:

```php
use App\View\Components\HelloComponent;

return Blade::renderComponent(new HelloComponent('Julian Bashir'));
```

<a name="slot-name-shortcut"></a>
### 슬롯 이름 단축 문법

_슬롯 이름 단축 문법은 [Caleb Porzio](https://github.com/calebporzio) 님이 기여했습니다._

이전 버전에서는 슬롯 이름을 `x-slot` 태그의 `name` 속성으로 지정했습니다:

```blade
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Laravel 9.x부터는 더 간편한 단축 문법으로 슬롯 이름을 지정할 수 있습니다:

```xml
<x-slot:title>
    Server Error
</x-slot>
```

<a name="checked-selected-blade-directives"></a>
### @checked / @selected Blade 지시어

_@checked와 @selected Blade 지시어는 [Ash Allen](https://github.com/ash-jc-allen), [Taylor Otwell](https://github.com/taylorotwell) 님이 기여했습니다._

HTML 폼 요소에서 조건에 따라 `checked` 속성을 쉽고 직관적으로 출력하기 위해 `@checked` 지시어를 사용할 수 있습니다. 조건이 `true`일 경우 `checked`를 출력합니다:

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

유사하게, `@selected` 지시어로 select 요소 option 태그에 `selected` 속성을 지정할 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

<a name="bootstrap-5-pagination-views"></a>
### Bootstrap 5 페이징 뷰

_Bootstrap 5 페이징 뷰는 [Jared Lewis](https://github.com/jrd-lewis) 님이 기여했습니다._

Laravel은 이제 [Bootstrap 5](https://getbootstrap.com/)를 사용한 페이지네이션 뷰를 포함합니다. 기본 Tailwind 뷰 대신 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 다음을 추가하세요:

```
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Paginator::useBootstrapFive();
}
```

<a name="improved-validation-of-nested-array-data"></a>
### 중첩 배열 데이터 유효성 검사 개선

_중첩 배열 데이터 유효성 검사 개선은 [Steve Bauman](https://github.com/stevebauman) 님이 기여했습니다._

유효성 검사 규칙을 할당할 때 배열 내 각 요소의 값을 참조해야 할 경우가 있습니다. 이제 `Rule::forEach` 메서드를 사용해 해결할 수 있습니다. `forEach`는 배열 속성의 각 요소마다 호출되는 클로저를 받아 해당 요소에 적용할 규칙들을 배열로 반환해야 합니다. 클로저에는 값과 명시적, 완전 확장된 속성 이름이 전달됩니다:

```
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function ($value, $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="laravel-breeze-api"></a>
### Laravel Breeze API 및 Next.js

_Laravel Breeze API 스캐폴딩과 Next.js 스타터 킷은 [Taylor Otwell](https://github.com/taylorotwell)과 [Miguel Piedrafita](https://twitter.com/m1guelpf) 님이 기여했습니다._

[Laravel Breeze](/docs/9.x/starter-kits#breeze-and-next) 스타터 킷에 "API" 스캐폴딩 모드와 Next.js 기반 [프론트엔드 구현](https://github.com/laravel/breeze-next)이 추가되었습니다. 이 스타터 킷은 JavaScript 프론트엔드를 위한 Laravel Sanctum 인증 API 백엔드를 빠르게 시작하는 데 유용합니다.

<a name="exception-page"></a>
### 개선된 Ignition 예외 페이지

_Ignition은 [Spatie](https://spatie.be/)에서 개발했습니다._

오픈소스 예외 디버그 페이지인 Ignition이 완전히 새롭게 디자인됐습니다. Laravel 9.x에 포함된 새 Ignition은 라이트 / 다크 테마 지원, 커스터마이징 가능한 "에디터에서 열기" 기능 등 다양한 개선점을 제공합니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/483853/149235404-f7caba56-ebdf-499e-9883-cac5d5610369.png"/>
</p>

<a name="improved-route-list"></a>
### 개선된 `route:list` CLI 출력

_개선된 `route:list` CLI 출력은 [Nuno Maduro](https://github.com/nunomaduro) 님이 기여했습니다._

Laravel 9.x에서는 `route:list` 명령어 출력물이 크게 개선되어, 라우트 정보를 훨씬 보기 좋고 탐색하기 쉽게 표시합니다.

<p align="center">
<img src="https://user-images.githubusercontent.com/5457236/148321982-38c8b869-f188-4f42-a3cc-a03451d5216c.png"/>
</p>

<a name="test-coverage-support-on-artisan-test-Command"></a>
### Artisan `test` 명령으로 테스트 커버리지 확인

_테스트 커버리지 기능은 [Nuno Maduro](https://github.com/nunomaduro) 님이 기여했습니다._

Artisan의 `test` 명령에 `--coverage` 옵션이 추가되어 테스트가 얼마나 코드를 커버하는지 CLI에서 직접 확인할 수 있습니다:

```shell
php artisan test --coverage
```

커버리지 결과가 CLI 출력에 표시됩니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>

또한 최소 커버리지 기준을 지정할 수 있는 `--min` 옵션이 도입되어, 기준 이하일 경우 테스트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/149989853-a29a7629-2bfa-4bf3-bbf7-cdba339ec157.png"/>
</p>

<a name="soketi-echo-server"></a>
### Soketi Echo 서버

_Soketi Echo 서버는 [Alex Renoki](https://github.com/rennokki) 님이 개발했습니다._

Laravel 9.x 전용은 아니지만, Laravel에서는 Node.js 기반의 [Laravel Echo](/docs/9.x/broadcasting) 호환 웹소켓 서버인 Soketi 문서 작업에 최근 참여했습니다. Soketi는 Pusher나 Ably 대신 직접 웹소켓 서버를 운영하려는 애플리케이션에 훌륭한 오픈소스 대안입니다.

자세한 내용은 [방송 문서](/docs/9.x/broadcasting)와 [Soketi 문서](https://docs.soketi.app/)를 참고하세요.

<a name="improved-collections-ide-support"></a>
### 향상된 Collections IDE 지원

_Collections IDE 지원 개선은 [Nuno Maduro](https://github.com/nunomaduro) 님이 기여했습니다._

Laravel 9.x는 컬렉션에 제네릭 스타일 타입 정의를 추가하여 IDE 및 정적 분석기에서 컬렉션을 더 잘 이해할 수 있게 했습니다. [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections)나 [PHPStan](https://phpstan.org)과 같은 도구가 네이티브로 Laravel 컬렉션을 더 정확하게 파악할 수 있습니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/151783350-ed301660-1e09-44c1-b549-85c6db3f078d.gif"/>
</p>

<a name="new-helpers"></a>
### 새로운 헬퍼 함수

Laravel 9.x는 애플리케이션에서 사용하기 편리한 두 가지 새 헬퍼 함수를 도입했습니다.

<a name="new-helpers-str"></a>
#### `str` 헬퍼 함수

`str` 함수는 주어진 문자열에 대해 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이는 `Str::of` 메서드와 동일합니다:

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

인수가 없으면 `str` 함수는 `Illuminate\Support\Str` 인스턴스를 반환합니다:

```
$snake = str()->snake('LaravelFramework');

// 'laravel_framework'
```

<a name="new-helpers-to-route"></a>
#### `to_route` 헬퍼 함수

`to_route` 함수는 지정한 이름 라우트로 리다이렉트하는 HTTP 응답을 생성하여, 라우트나 컨트롤러에서 이름 라우트로 쉽게 리다이렉트할 수 있도록 합니다:

```
return to_route('users.show', ['user' => 1]);
```

필요한 경우, 세 번째와 네 번째 인자로 HTTP 상태 코드와 추가 응답 헤더를 전달할 수 있습니다:

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```