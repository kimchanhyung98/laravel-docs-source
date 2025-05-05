# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서 페이지네이션은 매우 번거로울 수 있습니다. Laravel의 페이지네이션 방식은 여러분에게 신선한 바람이 되길 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries) 및 [Eloquent ORM](/docs/{{version}}/eloquent)과 통합되어, 별도의 설정 없이 데이터베이스 레코드를 간편하게 페이지네이션 할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만, Bootstrap용 페이지네이션 뷰도 함께 지원합니다.

<a name="tailwind"></a>
#### Tailwind

Tailwind 4.x와 함께 Laravel의 기본 Tailwind 페이지네이션 뷰를 사용하는 경우, 애플리케이션의 `resources/css/app.css` 파일은 이미 Laravel의 페이지네이션 뷰를 `@source`로 올바르게 구성되어 있습니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

항목을 페이지네이션 하는 여러 방법이 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 처리해줍니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 값으로 감지됩니다. 이 값은 Laravel에서 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

아래 예제에서는 `paginate` 메서드에 표시하고자 하는 "페이지 당 항목 수"만 전달합니다. 여기서는 한 페이지당 `15`개의 항목을 표시하도록 지정합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 표시합니다.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### 간단 페이지네이션

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리와 일치하는 전체 레코드 수를 계산합니다. 이는 페이지네이터가 전체 페이지 수를 알 수 있도록 하기 위함입니다. 그러나, 애플리케이션 UI에 전체 페이지 수를 표시할 계획이 없다면, 전체 카운트 쿼리는 불필요합니다.

따라서, UI에 단순히 "다음"과 "이전" 링크만 보여주면 된다면, 효율적인 단일 쿼리를 수행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이지네이션할 수 있습니다. 아래 예시에서는 `App\Models\User` 모델을 15개씩 페이지네이션합니다. 구문이 쿼리 빌더와 거의 동일하다는 것을 알 수 있습니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, 쿼리에 `where` 절 등 다른 조건을 지정한 후에 `paginate` 메서드를 호출할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

마찬가지로, Eloquent 모델에 커서 페이지네이션을 적용하려면 `cursorPaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용

경우에 따라 한 화면에서 서로 다른 페이지네이터를 두 개 렌더링해야 할 수도 있습니다. 그러나 두 페이지네이터 모두 `page` 쿼리 문자열 변수를 사용하면 서로 충돌이 발생합니다. 이 때, 현재 페이지를 저장할 쿼리 문자열 변수의 이름을 `paginate`, `simplePaginate`, `cursorPaginate`의 세 번째 인자로 전달하여 해결할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate`와 `simplePaginate`는 SQL의 "offset" 절을 사용하여 쿼리를 생성하는 반면, 커서 페이지네이션은 쿼리 내에서 정렬된 컬럼의 값을 비교하는 "where" 절을 생성해, Laravel 페이지네이션 방식 중 가장 효율적인 데이터베이스 성능을 제공합니다. 이 방식은 대규모 데이터셋이나 "무한 스크롤" UI에 특히 적합합니다.

Offset 기반 페이지네이션은 쿼리 문자열에 페이지 번호가 포함되지만, 커서 기반 페이지네이션은 "커서" 문자열이 쿼리 문자열에 포함됩니다. 커서는 다음 페이지네이션 쿼리가 어디서부터 시작되어야 하는지와 방향을 나타내는 인코딩된 문자열입니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 기반 페이지네이터 인스턴스는 쿼리 빌더의 `cursorPaginate` 메서드를 통해 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 가져오면, 일반적인 `paginate` 및 `simplePaginate`와 동일하게 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 인스턴스에서 사용할 수 있는 자세한 메서드는 [커서 페이지네이터 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 합니다. 또한 정렬 기준이 되는 컬럼들은 페이지네이션 대상 테이블에 속해 있어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 예로 들어 살펴봅시다. 아래 두 쿼리는 모두 `users` 테이블의 `id` 기준 정렬에서 "두 번째 페이지"를 보여줍니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 방식보다 다음과 같은 이점이 있습니다:

- 대용량 데이터셋에서 "order by" 컬럼에 인덱스가 있다면 성능이 더 뛰어납니다. 이는 "offset"이 이전 매칭 데이터를 모두 훑고 지나가기 때문입니다.
- 데이터 추가 혹은 삭제가 빈번한 경우, 오프셋 페이지네이션은 특정 페이지에서 데이터가 누락되거나 중복되게 표시될 수 있습니다.

하지만 커서 페이지네이션에는 다음과 같은 제약점도 있습니다:

- `simplePaginate`처럼, "다음" 및 "이전" 링크만 제공되며 페이지 번호를 통한 링크는 지원하지 않습니다.
- 정렬 기준이 되는 컬럼이 적어도 한 개의 유니크 컬럼이거나 컬럼 조합이 유니크해야 합니다. `null` 값이 있는 컬럼은 지원되지 않습니다.
- "order by" 절의 쿼리식은 alias로 지정되어 "select" 절에도 포함되어 있어야만 지원됩니다.
- 파라미터가 있는 쿼리식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성

이미 메모리에 가지고 있는 배열을 페이지네이션해야 할 때, 페이지네이터 인스턴스를 직접 생성할 수 있습니다. 이때 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나를 사용할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 전체 항목 수를 알 필요가 없지만, 그래서 마지막 페이지의 인덱스를 구하는 메서드는 없습니다. `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수를 받지만, 결과 전체 항목 수(count)가 필수로 필요합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`와, `CursorPaginator`는 `cursorPaginate`와, `LengthAwarePaginator`는 `paginate` 메서드와 대응됩니다.

> [!WARNING]
> 페이지네이터 인스턴스를 수동으로 생성할 때는, 전달하는 결과 배열을 직접 "슬라이스(slice)"해야 합니다. 방법이 헷갈리신다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수 문서를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 하지만, 페이지네이터의 `withPath` 메서드를 사용하면 링크 생성시 사용할 URI를 커스터마이징할 수 있습니다. 예를 들어, 링크가 `http://example.com/admin/users?page=N` 꼴이 되길 원한다면 `withPath`에 `/admin/users`를 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가

페이지네이션 링크에 쿼리 문자열 값을 추가하려면 `appends` 메서드를 사용할 수 있습니다. 예를 들어, 모든 링크에 `sort=votes`를 추가하려면 다음과 같이 합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리 문자열 값을 그대로 링크에 추가하려면 `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 붙이고 싶다면 `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 모든 링크 끝에 `#users`를 추가하려면 아래와 같이 하세요:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스가 반환되고, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를 반환합니다. `cursorPaginate`를 호출하면 `Illuminate\Pagination\CursorPaginator` 인스턴스가 반환됩니다.

이들 객체는 결과 집합을 설명하는 여러 메서드를 제공합니다. 또한 페이지네이터 인스턴스들은 반복자(iterator)이므로 배열처럼 루프를 돌릴 수 있습니다. 즉, 결과를 가져온 후 아래와 같이 [Blade](/docs/{{version}}/blade)로 결과와 페이지 링크를 출력할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지 링크를 렌더링합니다. 이들 링크에는 이미 올바른 `page` 쿼리 문자열 변수가 포함되어 있습니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터가 링크를 표시할 때, 현재 페이지 번호와 함께 그 앞뒤로 세 페이지씩의 링크가 표시됩니다. `onEachSide` 메서드를 사용하면, 현재 페이지를 기준으로 중간 링크(슬라이딩 윈도우)에 표시되는 추가 링크 수를 제어할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공합니다. 그래서 페이지네이션 결과를 쉽게 JSON으로 변환할 수 있습니다. 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환해도 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 포함됩니다. 실제 데이터 레코드는 `data` 키에 배열로 있습니다. 라우트에서 페이지네이터 인스턴스를 반환했을 때 생성되는 JSON 예시는 다음과 같습니다:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // 레코드...
        },
        {
            // 레코드...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이징

기본적으로 페이지네이션 링크를 렌더링하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환되도록 제공됩니다. Tailwind를 사용하지 않는 경우, 직접 뷰를 작성해 사용할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드에 첫번째 인자로 뷰 이름을 전달해 사용할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달하기... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 간편하게 페이지네이션 뷰를 커스터마이징하는 방법은 `vendor:publish` 커맨드로 뷰 템플릿을 `resources/views/vendor` 디렉토리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면, 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰가 생성됩니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당합니다. 이 파일을 수정해 페이지네이션 HTML을 커스터마이징할 수 있습니다.

다른 뷰 파일을 기본 페이지네이션 뷰로 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Bootstrap 사용하기

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 제작된 페이지네이션 뷰도 제공합니다. Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하면 됩니다:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드 | 설명 |
| --- | --- |
| `$paginator->count()` | 현재 페이지의 항목 개수 반환 |
| `$paginator->currentPage()` | 현재 페이지 번호 반환 |
| `$paginator->firstItem()` | 결과 중 첫 번째 항목의 번호 반환 |
| `$paginator->getOptions()` | 페이지네이터의 옵션 반환 |
| `$paginator->getUrlRange($start, $end)` | 페이지네이션 URL의 범위 생성 |
| `$paginator->hasPages()` | 여러 페이지로 분할할 만큼의 항목이 있는지 판별 |
| `$paginator->hasMorePages()` | 더 많은 항목이 남아있는지 판별 |
| `$paginator->items()` | 현재 페이지의 항목들을 반환 |
| `$paginator->lastItem()` | 결과 중 마지막 항목의 번호 반환 |
| `$paginator->lastPage()` | 마지막 페이지 번호 반환 (`simplePaginate`에서는 사용 불가) |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL 반환 |
| `$paginator->onFirstPage()` | 첫 번째 페이지에 있는지 판별 |
| `$paginator->perPage()` | 페이지당 표시할 항목 수 |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL 반환 |
| `$paginator->total()` | 데이터 저장소 내 총 매칭 항목 수 반환 (`simplePaginate`에서는 사용 불가) |
| `$paginator->url($page)` | 지정한 페이지 번호의 URL 반환 |
| `$paginator->getPageName()` | 페이지를 저장하는 쿼리 문자열 변수명 반환 |
| `$paginator->setPageName($name)` | 페이지를 저장하는 쿼리 문자열 변수명 설정 |
| `$paginator->through($callback)` | 콜백을 사용해 각 항목을 변환 |

</div>

<a name="cursor-paginator-instance-methods"></a>
## 커서 페이지네이터 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음과 같은 메서드로 추가 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                         |
| ------------------------------- | ------------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지의 항목 수 반환                                    |
| `$paginator->cursor()`          | 현재 커서 인스턴스 반환                                       |
| `$paginator->getOptions()`      | 페이지네이터 옵션 반환                                        |
| `$paginator->hasPages()`        | 여러 페이지로 분할할 만큼의 항목이 있는지 판별                |
| `$paginator->hasMorePages()`    | 더 많은 항목이 남아있는지 판별                                |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리 문자열 변수명 반환                       |
| `$paginator->items()`           | 현재 페이지의 항목들 반환                                     |
| `$paginator->nextCursor()`      | 다음 항목 집합을 위한 커서 인스턴스 반환                      |
| `$paginator->nextPageUrl()`     | 다음 페이지로 이동할 URL 반환                                 |
| `$paginator->onFirstPage()`     | 첫 페이지 여부 판별                                           |
| `$paginator->onLastPage()`      | 마지막 페이지 여부 판별                                       |
| `$paginator->perPage()`         | 페이지당 표시할 항목 수                                       |
| `$paginator->previousCursor()`  | 이전 항목 집합을 위한 커서 인스턴스 반환                      |
| `$paginator->previousPageUrl()` | 이전 페이지로 이동할 URL 반환                                 |
| `$paginator->setCursorName()`   | 커서를 저장할 쿼리 문자열 변수명 설정                        |
| `$paginator->url($cursor)`      | 주어진 커서 인스턴스의 URL 반환                               |

</div>