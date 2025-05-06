# 릴리즈 노트

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 9](#laravel-9)

<a name="versioning-scheme"></a>
## 버전 관리 정책

Laravel 및 기타 1차 제공 패키지들은 [시맨틱 버전 관리](https://semver.org)를 따릅니다. 주요 프레임워크 릴리즈는 매년(약 2월) 출시되며, 마이너 및 패치 릴리즈는 매주 출시될 수 있습니다. 마이너 및 패치 릴리즈에는 **절대** 하위 호환성에 영향을 주는 변경 사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 컴포넌트를 참조할 때는 반드시 `^9.0`과 같은 버전 제약 조건을 사용해야 합니다. 왜냐하면 주요 릴리즈에는 하위 호환성 이슈가 포함될 수 있기 때문입니다. 하지만, 새 주요 릴리즈로의 업그레이드가 하루 이내에 완료될 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트

[네임드 아규먼트](https://www.php.net/manual/kr/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 정책에 포함되지 않습니다. Laravel 코드베이스 개선을 위해 함수 인자명을 필요에 따라 변경할 수 있습니다. 따라서 Laravel 메서드 호출 시 네임드 아규먼트를 사용할 때는 추후 인자 이름이 변경될 가능성을 염두에 두고 주의해서 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

Laravel의 모든 릴리즈에는 18개월 동안 버그 수정, 2년 동안 보안 패치가 제공됩니다. Lumen을 포함한 모든 추가 라이브러리는 최신 주요 릴리즈만 버그 수정이 제공됩니다. 또한, Laravel이 지원하는 데이터베이스 버전도 [여기](/docs/{{version}}/database#introduction)에서 확인하세요.

| 버전 | PHP (*) | 릴리즈 | 버그 수정 지원 종료 | 보안 패치 지원 종료 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | 2019년 9월 3일 | 2022년 1월 25일 | 2022년 9월 6일 |
| 7 | 7.2 - 8.0 | 2020년 3월 3일 | 2020년 10월 6일 | 2021년 3월 3일 |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 패치만 지원</div>
    </div>
</div>

(*) 지원하는 PHP 버전

<a name="laravel-9"></a>
## Laravel 9

알다시피, Laravel은 8 버전부터 연 1회 릴리즈로 전환하였습니다. 이전에는 6개월마다 주요 버전이 출시되었으나, 이 변화는 커뮤니티의 유지 보수 부담을 완화하고, 개발팀이 혁신적인 기능을 도입하면서도 깨지는 변경 없이 더 많은 기능을 제공하도록 하기 위함입니다. 그 결과, 병렬 테스트 지원, 개선된 Breeze 스타터 키트, HTTP 클라이언트 향상, "has one of many"와 같은 새로운 Eloquent 관계 타입 등 하위 호환성을 해치지 않는 다양한 기능이 Laravel 8에 도입되었습니다.

이처럼, 현재 릴리즈에 강력한 기능을 계속 추가하는 정책으로 인해 향후 "주요" 릴리즈는 주로 상위 의존성 업그레이드와 같은 "유지 관리" 작업을 위해 사용될 가능성이 높습니다. 이는 이 릴리즈 노트에서 확인할 수 있습니다.

Laravel 9는 Symfony 6.0 컴포넌트, Symfony Mailer, Flysystem 3.0, 개선된 `route:list` 출력, Laravel Scout 데이터베이스 드라이버, 새로운 Eloquent 접근자/변경자 문법, Enum을 통한 암시적 라우트 바인딩 등 다양한 버그 수정 및 사용성 개선을 도입하면서 8.x에서의 발전을 이어갑니다.

<a name="php-8"></a>
### PHP 8.0

Laravel 9.x는 PHP 8.0 이상의 버전을 필요로 합니다.

<a name="symfony-mailer"></a>
### Symfony Mailer

_Symfony Mailer 지원은 [Dries Vints](https://github.com/driesvints)_, [James Brooks](https://github.com/jbrooksuk), [Julius Kiekbusch](https://github.com/Jubeki)가 기여했습니다.

이전 Laravel 릴리즈에서는 [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) 라이브러리를 통해 메일을 발송했습니다. 하지만 해당 라이브러리는 더 이상 유지되지 않으며 Symfony Mailer로 대체되었습니다.

Symfony Mailer와의 호환을 위해, [업그레이드 가이드](/docs/{{version}}/upgrade#symfony-mailer)를 참고하세요.

<a name="flysystem-3"></a>
### Flysystem 3.x

_Flysystem 3.x 지원은 [Dries Vints](https://github.com/driesvints)가 기여했습니다._

Laravel 9.x는 Flysystem의 상위 의존성을 3.x로 업그레이드합니다. Flysystem은 `Storage` 파사드가 제공하는 모든 파일시스템 동작을 담당합니다.

애플리케이션이 Flysystem 3.x에 호환되는지 확인하려면 [업그레이드 가이드](/docs/{{version}}/upgrade#flysystem-3)를 참조하세요.

<a name="eloquent-accessors-and-mutators"></a>
### 개선된 Eloquent 접근자/변경자

_개선된 Eloquent 접근자/변경자는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Laravel 9.x는 새로운 방식의 Eloquent [접근자 및 변경자](/docs/{{version}}/eloquent-mutators#accessors-and-mutators) 정의법을 제공합니다. 이전에는 아래와 같이 접두사가 붙은 메서드로만 접근자/변경자를 정의할 수 있었습니다.

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

이제는 `Illuminate\Database\Eloquent\Casts\Attribute`를 반환하도록 타입 힌트를 주는 비접두사 단일 메서드로 접근자와 변경자를 정의할 수 있습니다:

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

또한, 이 방식은 [커스텀 캐스트 클래스](/docs/{{version}}/eloquent-mutators#custom-casts)처럼 반환 객체 값을 캐싱합니다:

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

> **경고**  
> Enum 캐스팅은 PHP 8.1+에서만 사용할 수 있습니다.

_Enum 캐스팅은 [Mohamed Said](https://github.com/themsaid)가 기여했습니다._

Eloquent는 이제 PHP ["백업(Backed)" Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 타입으로 속성 값을 캐스팅할 수 있습니다. 모델의 `$casts` 프로퍼티에 해당 속성과 enum을 지정하세요:

    use App\Enums\ServerStatus;

    /**
     * 캐스팅할 속성 리스트
     *
     * @var array
     */
    protected $casts = [
        'status' => ServerStatus::class,
    ];

이후 모델의 해당 속성 접근 시, 지정한 enum으로 자동 변환됩니다:

    if ($server->status == ServerStatus::Provisioned) {
        $server->status = ServerStatus::Ready;

        $server->save();
    }

<a name="implicit-route-bindings-with-enums"></a>
### Enum을 활용한 암시적 라우트 바인딩

_암시적 Enum 바인딩은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

PHP 8.1부터 [Enum](https://www.php.net/manual/en/language.enumerations.backed.php) 지원이 추가되었습니다. Laravel 9.x에서는 Enum을 라우트 정의에 타입힌트로 사용할 수 있고, 해당 URI 세그먼트가 올바른 Enum 값일 경우에만 라우트가 실행됩니다. 그렇지 않을 경우 자동으로 HTTP 404가 반환됩니다.

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

예를 들어, 아래 라우트에서 `{category}` 세그먼트가 `fruits` 또는 `people`일 때만 호출됩니다:

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="forced-scoping-of-route-bindings"></a>
### 라우트 바인딩의 강제 스코프 지정

_강제 스코프 바인딩은 [Claudio Dekker](https://github.com/claudiodekker)가 기여했습니다._

이전 Laravel 버전에서는 라우트 정의에서 두 번째 Eloquent 모델이 첫 번째 모델의 자식임을 스코프할 수 있습니다. 예를 들어, 특정 사용자의 블로그 포스트를 slug로 조회하는 경우:

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    });

중첩 라우트 파라미터에서 커스텀 키를 사용할 경우, Laravel은 자동으로 관계명을 추측해 부모 모델에 대해 쿼리를 스코프합니다. 하지만 이 동작은 자식 바인딩에 커스텀 키를 지정할 때만 지원되었습니다.

Laravel 9.x부터는 커스텀 키가 없어도 명시적으로 `scopeBindings` 메서드를 호출해 자식 바인딩 스코프 지정이 가능합니다:

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    })->scopeBindings();

또는 라우트 그룹 전체에 대해 스코프 바인딩을 적용할 수 있습니다:

    Route::scopeBindings()->group(function () {
        Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
            return $post;
        });
    });

<a name="controller-route-groups"></a>
### 컨트롤러 라우트 그룹

_라우트 그룹 개선은 [Luke Downing](https://github.com/lukeraymonddowning)가 기여했습니다._

`controller` 메서드를 사용해 그룹 내 모든 라우트의 공통 컨트롤러를 지정할 수 있습니다. 이후 각 라우트에는 컨트롤러 메서드 이름만 명시하면 됩니다.

    use App\Http\Controllers\OrderController;

    Route::controller(OrderController::class)->group(function () {
        Route::get('/orders/{id}', 'show');
        Route::post('/orders', 'store');
    });

<a name="full-text"></a>
### 전문(Full Text) 인덱스/Where 절

_전문 인덱스 및 "where" 절은 [Taylor Otwell](https://github.com/taylorotwell), [Dries Vints](https://github.com/driesvints)가 기여했습니다._

MySQL 또는 PostgreSQL 사용 시, 컬럼 정의에 `fullText` 메서드를 추가해 전문 인덱스를 생성할 수 있습니다:

    $table->text('bio')->fullText();

또한, `whereFullText` 및 `orWhereFullText` 메서드를 사용해 [full text index](/docs/{{version}}/migrations#available-index-types)가 적용된 컬럼에 전문 "where" 절을 추가할 수 있습니다. Laravel이 데이터베이스 종류에 맞는 적절한 SQL로 변환해줍니다. 예) MySQL의 경우 `MATCH AGAINST` 절 생성:

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

<a name="laravel-scout-database-engine"></a>
### Laravel Scout 데이터베이스 엔진

_Laravel Scout 데이터베이스 엔진은 [Taylor Otwell](https://github.com/taylorotwell), [Dries Vints](https://github.com/driesvints)가 기여했습니다._

애플리케이션이 소규모~중규모 데이터베이스를 사용하거나 가벼운 쿼리만 필요하다면, 별도의 검색 서비스(Algolia, MeiliSearch 등) 대신 Scout의 "database" 엔진을 사용할 수 있습니다. 데이터베이스 엔진은 기존 데이터베이스에서 "where like" 및 전문 인덱스를 활용해 검색 결과를 반환합니다.

Scout 데이터베이스 엔진 관련 자세한 내용은 [Scout 문서](/docs/{{version}}/scout)를 참조하세요.

<a name="rendering-inline-blade-templates"></a>
### 인라인 Blade 템플릿 렌더링

_인라인 Blade 템플릿 렌더링은 [Jason Beggs](https://github.com/jasonlbeggs), 인라인 Blade 컴포넌트 렌더링은 [Toby Zerner](https://github.com/tobyzerner)가 기여했습니다._

Raw Blade 템플릿 문자열을 HTML로 변환이 필요할 때, `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 이 메서드는 Blade 템플릿 문자열과(옵션) 데이터를 받아 렌더링합니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

또한, `renderComponent` 메서드로 인스턴스를 직접 넘겨 클래식 컴포넌트도 렌더링할 수 있습니다:

```php
use App\View\Components\HelloComponent;

return Blade::renderComponent(new HelloComponent('Julian Bashir'));
```

<a name="slot-name-shortcut"></a>
### Slot 이름 단축 문법

_Slot 이름 단축 문법은 [Caleb Porzio](https://github.com/calebporzio)가 기여했습니다._

기존에는 `x-slot` 태그에 `name` 속성을 사용해 슬롯 이름을 지정했습니다:

```blade
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

하지만 Laravel 9.x부터 더 짧은 아래 문법을 사용할 수 있습니다:

```xml
<x-slot:title>
    Server Error
</x-slot>
```

<a name="checked-selected-blade-directives"></a>
### Checked / Selected Blade 디렉티브

_Checked, selected Blade 디렉티브는 [Ash Allen](https://github.com/ash-jc-allen), [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

이제 `@checked` 디렉티브로 체크박스 input이 체크되었는지 간단히 표시할 수 있습니다. 조건이 true면 `checked`를 출력합니다:

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

마찬가지로, `@selected` 디렉티브로 select 옵션이 선택되었는지도 쉽게 표시할 수 있습니다:

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
### Bootstrap 5 페이지네이션 뷰

_Bootstrap 5 페이지네이션 뷰는 [Jared Lewis](https://github.com/jrd-lewis)가 기여했습니다._

Laravel에는 이제 [Bootstrap 5](https://getbootstrap.com/)로 제작된 페이지네이션 뷰가 기본 포함됩니다. 기존 Tailwind 뷰 대신 사용하고 싶다면, `App\Providers\AppServiceProvider`의 `boot` 메서드 안에서 paginator의 `useBootstrapFive`를 호출하세요:

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

<a name="improved-validation-of-nested-array-data"></a>
### 중첩 배열 데이터 검증 개선

_중첩 배열 인풋 검증 개선은 [Steve Bauman](https://github.com/stevebauman)이 기여했습니다._

중첩 배열의 각 요소별로 검증 규칙을 다르게 할 때, 이제 `Rule::forEach` 메서드를 사용할 수 있습니다. 이 메서드는 검증 대상 배열의 각 반복 시 클로저를 호출하며, 해당 요소의 값과 완전한 속성 이름을 전달합니다. 클로저는 해당 배열 요소에 적용할 검증 규칙 배열을 반환해야 합니다:

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

<a name="laravel-breeze-api"></a>
### Laravel Breeze API & Next.js

_Laravel Breeze API 스캐폴딩 및 Next.js 스타터 키트는 [Taylor Otwell](https://github.com/taylorotwell), [Miguel Piedrafita](https://twitter.com/m1guelpf)가 기여했습니다._

[Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-next) 스타터 키트에 "API" 스캐폴딩 모드와 함께 [Next.js](https://nextjs.org) [프론트엔드 구현체](https://github.com/laravel/breeze-next)가 추가되었습니다. 이 키트를 사용하면 자바스크립트 프론트엔드용으로 Laravel Sanctum 인증 API 백엔드를 손쉽게 시작할 수 있습니다.

<a name="exception-page"></a>
### Ignition 예외 페이지 개선

_Ignition은 [Spatie](https://spatie.be/)가 개발하였습니다._

Spatie가 만든 오픈 소스 예외 디버깅 페이지 Ignition이 완전히 새로 디자인되어 Laravel 9.x에 포함되었습니다. 새로운 Ignition은 라이트/다크 테마, 편집기에서 열기 커스터마이즈, 기타 다양한 기능을 제공합니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/483853/149235404-f7caba56-ebdf-499e-9883-cac5d5610369.png"/>
</p>

<a name="improved-route-list"></a>
### `route:list` CLI 출력 개선

_개선된 `route:list` CLI 출력은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

Laravel 9.x에서 `route:list` CLI의 출력이 크게 개선되어, 라우트 정의를 탐색할 때 더욱 보기 편해졌습니다.

<p align="center">
<img src="https://user-images.githubusercontent.com/5457236/148321982-38c8b869-f188-4f42-a3cc-a03451d5216c.png"/>
</p>

<a name="test-coverage-support-on-artisan-test-Command"></a>
### Artisan `test` 커맨드로 테스트 커버리지 측정

_Artisan `test` 커맨드 커버리지 기능은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

Artisan `test` 커맨드에 새롭게 추가된 `--coverage` 옵션을 사용해, 현재 테스트들이 코드 베이스를 얼마나 커버하는지 확인할 수 있습니다:

```shell
php artisan test --coverage
```

테스트 커버리지 결과는 CLI 출력에 바로 표시됩니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>

또한, 커버리지 퍼센트에 최소 임계값을 지정하려면 `--min` 옵션을 사용하세요. 임계값을 충족하지 못하면 테스트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/149989853-a29a7629-2bfa-4bf3-bbf7-cdba339ec157.png"/>
</p>

<a name="soketi-echo-server"></a>
### Soketi Echo 서버

_Soketi Echo 서버는 [Alex Renoki](https://github.com/rennokki)가 개발했습니다._

Laravel 9.x 전용은 아니지만, Laravel은 최근 Node.js 기반 [Laravel Echo](/docs/{{version}}/broadcasting) 호환 Web Socket 서버인 Soketi의 문서화에 도움을 주었습니다. Soketi는 Pusher, Ably 등 상용 서비스를 대체해 직접 Web Socket 서버를 운영하고 싶은 서비스에 훌륭한 오픈 소스 대안입니다.

Soketi 사용에 대한 자세한 내용은 [브로드캐스팅 문서](/docs/{{version}}/broadcasting) 및 [Soketi 공식 문서](https://docs.soketi.app/)를 참고하세요.

<a name="improved-collections-ide-support"></a>
### 컬렉션 IDE 지원 개선

_컬렉션 IDE 지원 개선은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

Laravel 9.x에서는 컬렉션 컴포넌트에 "제너릭" 스타일 타입 정의가 추가되어, IDE 및 정적 분석 툴 지원이 향상되었습니다. [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections)과 [PHPStan](https://phpstan.org) 등에서 Laravel 컬렉션을 더욱 잘 이해하게 됩니다.

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/151783350-ed301660-1e09-44c1-b549-85c6db3f078d.gif"/>
</p>

<a name="new-helpers"></a>
### 신규 헬퍼 함수

Laravel 9.x에는 다음과 같이 두 가지 새로운 편리한 헬퍼 함수가 도입되었습니다.

<a name="new-helpers-str"></a>
#### `str`

`str` 함수는 지정 문자열로 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 같습니다:

    $string = str('Taylor')->append(' Otwell');

    // 'Taylor Otwell'

인수가 없으면 `str` 함수는 `Illuminate\Support\Str` 인스턴스를 반환합니다:

    $snake = str()->snake('LaravelFramework');

    // 'laravel_framework'

<a name="new-helpers-to-route"></a>
#### `to_route`

`to_route` 함수는 지정한 네임드 라우트로의 리디렉션 HTTP 응답을 생성하며, 라우트나 컨트롤러에서 명확하게 리다이렉트할 수 있습니다:

    return to_route('users.show', ['user' => 1]);

필요하다면, 세 번째, 네 번째 인수로 HTTP 상태 코드와 추가 헤더를 지정할 수도 있습니다:

    return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);