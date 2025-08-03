# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 Paginator 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 출력하기](#displaying-pagination-results)
    - [페이지네이션 링크 창 조절하기](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크들에서는 페이지네이션 구현이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 접근 방식이 신선한 경험이 되길 바랍니다. Laravel의 paginator는 [query builder](/docs/master/queries) 및 [Eloquent ORM](/docs/master/eloquent)과 밀접하게 통합되어 있어, 별도의 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이지네이션할 수 있습니다.

기본적으로 paginator가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만 Bootstrap 페이지네이션도 지원하고 있습니다.

<a name="tailwind"></a>
#### Tailwind

Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용하는 경우, 애플리케이션의 `resources/css/app.css` 파일이 이미 Laravel의 페이지네이션 뷰를 `@source`하도록 올바르게 설정되어 있습니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션 (Paginating Query Builder Results)

페이지네이션을 구현하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 [query builder](/docs/master/queries)나 [Eloquent 쿼리](/docs/master/eloquent)에 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 현재 사용자가 보고 있는 페이지에 따라 자동으로 쿼리의 `limit`과 `offset`을 설정해줍니다. 기본적으로 현재 페이지 정보는 HTTP 요청의 쿼리 스트링에서 `page` 인수로 감지됩니다. Laravel이 이 값을 자동으로 감지하며, paginator가 생성하는 링크에도 자동으로 포함됩니다.

다음 예시는 `paginate` 메서드에 넘긴 유일한 인수가 한 페이지당 표시할 아이템 수인 경우입니다. 이 예에서는 한 페이지에 `15`개의 아이템을 화면에 보여주도록 지정했습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자를 보여줍니다.
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
#### 단순 페이지네이션 (Simple Pagination)

`paginate` 메서드는 데이터베이스에서 레코드를 조회하기 전에 해당 쿼리와 일치하는 총 레코드 수를 계산합니다. 이렇게 해야 paginator가 전체 페이지 수를 알 수 있기 때문입니다. 하지만 만약 애플리케이션 UI에서 전체 페이지 수를 표시하지 않는다면, 전체 레코드 수를 계산하는 쿼리는 불필요합니다.

따라서 UI에서 단순히 "다음"과 "이전" 링크만 표시하고 싶다면, 더 효율적으로 작동하는 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션 (Paginating Eloquent Results)

[Eloquent](/docs/master/eloquent) 쿼리에서도 페이지네이션을 사용할 수 있습니다. 다음 예시는 `App\Models\User` 모델을 페이지네이션하며, 한 페이지에 15개의 레코드를 표시하도록 지정한 예입니다. 보시다시피, 쿼리 빌더 결과 페이지네이션과 거의 동일한 문법입니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, `paginate` 메서드는 `where` 절 등 쿼리에 추가 제약을 건 다음 호출할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델 페이지네이션 시 `simplePaginate` 메서드도 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

비슷하게, Eloquent 모델에서 커서 페이지네이션을 할 때는 `cursorPaginate` 메서드를 사용합니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 Paginator 인스턴스 사용하기

애플리케이션 화면 한 곳에 두 개 이상의 paginator를 렌더링해야 하는 경우가 있습니다. 이때 두 paginator가 모두 `page` 쿼리 스트링 인수를 사용하면 서로 충돌하게 됩니다. 이런 충돌을 방지하기 위해, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수에 각 paginator가 사용할 쿼리 스트링 변수를 지정할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate` 메서드는 SQL의 `offset` 절을 사용해 쿼리를 생성하지만, 커서 페이지네이션은 쿼리 내 정렬된 컬럼의 값을 비교하는 `where` 절을 구성하는 방식으로 작동합니다. 이는 Laravel 페이지네이션 방식 중 데이터베이스 성능이 가장 뛰어난 방법입니다. 특히 대용량 데이터셋이나 "무한 스크롤" UI에 적합합니다.

오프셋 페이지네이션은 paginator가 생성하는 URL 쿼리 스트링에 페이지 번호를 포함하지만, 커서 페이지네이션은 쿼리 스트링에 인코딩된 "커서" 문자열을 포함합니다. 이 커서는 다음 페이지네이션 쿼리의 시작 위치와 진행 방향을 담고 있습니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 기반 paginator 인스턴스는 쿼리 빌더의 `cursorPaginate` 메서드를 통해 생성할 수 있으며, 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 paginator 인스턴스를 받은 후에는 `[페이지네이션 결과 출력하기](#displaying-pagination-results)` 절에서 설명하는 것처럼, `paginate`나 `simplePaginate` 메서드를 사용할 때와 마찬가지로 결과와 링크를 출력할 수 있습니다. 커서 paginator가 제공하는 인스턴스 메서드에 대한 자세한 내용은 [커서 paginator 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 합니다. 또한, 정렬하는 컬럼들은 페이지네이션하는 테이블의 컬럼이어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션 비교

오프셋 페이지네이션과 커서 페이지네이션의 차이점을 이해하기 위해, 두 가지 예시 SQL 쿼리를 살펴보겠습니다. 다음 두 쿼리는 모두 `users` 테이블에서 `id` 기준으로 정렬했을 때 "두 번째 페이지" 결과를 조회합니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션이 오프셋 페이지네이션에 비해 가진 장점은 다음과 같습니다:

- 대용량 데이터셋에서, "order by" 컬럼이 인덱스화되어 있으면 커서 페이지네이션이 훨씬 빠릅니다. 오프셋 절은 이전 데이터를 전부 스캔하기 때문입니다.
- 잦은 쓰기가 발생하는 데이터셋에서는, 오프셋 페이지네이션이 데이터를 누락하거나 중복 표시할 수 있습니다. 예를 들어, 사용자가 보고 있는 페이지 바로 전에 데이터가 추가 혹은 삭제된 경우 그렇습니다.

반면, 커서 페이지네이션의 제한사항은 다음과 같습니다:

- `simplePaginate` 처럼, "다음"과 "이전" 링크만 표시할 수 있고, 페이지 번호가 포함된 링크는 지원하지 않습니다.
- 정렬 기준에 반드시 고유한 한 개 이상의 컬럼 또는 조합이 있어야 하며, `null` 값을 가진 컬럼은 지원하지 않습니다.
- "order by" 절에 사용된 쿼리 표현식은, 별칭(alias)이 지정되어 `select` 절에도 포함되어 있어야 합니다.
- 파라미터가 포함된 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 Paginator 생성하기 (Manually Creating a Paginator)

이미 메모리에 가지고 있는 아이템 배열을 직접 페이지네이터에 넘겨 수동으로 생성하고 싶을 때가 있습니다. 이 경우 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스 중 하나를 생성해서 사용할 수 있습니다.

`Paginator`와 `CursorPaginator`는 결과 집합의 전체 아이템 수를 알 필요가 없습니다. 그래서 이 클래스들은 마지막 페이지 인덱스를 조회하는 메서드를 제공하지 않습니다. 반면, `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수를 받지만, 총 아이템 수를 반드시 입력해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate` 메서드와, `CursorPaginator`는 `cursorPaginate` 메서드와, `LengthAwarePaginator`는 `paginate` 메서드와 대응됩니다.

> [!WARNING]
> 수동으로 paginator 인스턴스를 만들 때는, 전달하는 결과 배열을 직접 "슬라이스"해야 합니다. 슬라이스 방법이 고민된다면, PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수 문서를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징 (Customizing Pagination URLs)

기본적으로 paginator가 생성하는 링크는 현재 요청의 URI를 기준으로 합니다. 그러나 `withPath` 메서드를 사용하면 링크를 생성할 때 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, paginator가 `http://example.com/admin/users?page=N`와 같은 링크를 생성하도록 하려면, `withPath` 메서드에 `/admin/users`를 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 스트링 값 추가하기 (Appending Query String Values)

`appends` 메서드를 사용하면 페이지네이션 링크의 쿼리 스트링에 값을 추가할 수 있습니다. 예를 들어, 모든 페이지네이션 링크에 `sort=votes`를 추가하려면 다음처럼 호출합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

`withQueryString` 메서드를 사용하면 현재 요청의 모든 쿼리 스트링 값을 페이지네이션 링크에 한꺼번에 추가할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기 (Appending Hash Fragments)

페이지네이션 링크에 "해시 프래그먼트"를 추가하고 싶을 경우 `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크 끝에 `#users` 해시를 추가하려면 다음과 같이 호출하세요:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 출력하기 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 받게 되고, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 대해 여러 유용한 메서드를 제공합니다. 또한 paginator 인스턴스는 반복자(iterator)이므로 배열처럼 `foreach` 등 루프로 돌릴 수 있습니다. 데이터를 받은 후에는 [Blade](/docs/master/blade)를 이용해 결과와 페이지 링크를 아래와 같이 출력할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 세트의 나머지 페이지용 링크를 렌더링해 줍니다. 각 링크는 이미 적절한 `page` 쿼리 스트링 변수를 포함합니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 창 조절하기 (Adjusting the Pagination Link Window)

paginator가 페이지네이션 링크를 표시할 때 현재 페이지 번호뿐만 아니라, 현재 페이지 기준으로 앞뒤 3개씩의 링크도 표시합니다. `onEachSide` 메서드를 사용하면, 현재 페이지를 가운데로 하는 링크 그룹 양쪽에 몇 개의 추가 링크를 표시할지 조절할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기 (Converting Results to JSON)

Laravel의 paginator 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며, `toJson` 메서드를 제공하므로 페이지네이션 결과를 매우 쉽게 JSON으로 변환할 수 있습니다. 또한 라우트 또는 컨트롤러 액션에서 paginator 인스턴스를 반환하면 자동으로 JSON 형태로 응답합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

paginator가 생성하는 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 포함되며, 실제 결과 레코드는 JSON 배열의 `data` 키에 들어 있습니다. 다음은 라우트에서 paginator를 반환했을 때 생성되는 JSON 예시입니다:

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
## 페이지네이션 뷰 커스터마이징 (Customizing the Pagination View)

기본적으로 페이지네이션 링크를 표시할 때 사용하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 하지만 Tailwind를 사용하지 않는 경우, 자유롭게 자신만의 뷰를 만들어서 이 링크들을 렌더링할 수 있습니다. paginator 인스턴스에서 `links` 메서드를 호출할 때 첫 번째 인수로 뷰 이름을 전달하면 해당 뷰가 사용됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터를 전달할 때... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

그러나 가장 쉬운 방법은 `vendor:publish` 명령어로 페이지네이션 뷰를 `resources/views/vendor` 디렉토리로 내보내 수정하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어는 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰들을 배치합니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당합니다. 이 파일을 수정해 페이지네이션 HTML을 변경할 수 있습니다.

만약 기본 페이지네이션 뷰를 다른 파일로 지정하고 싶으면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 paginator의 `defaultView`와 `defaultSimpleView` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Bootstrap 사용하기 (Using Bootstrap)

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)를 사용해 만든 페이지네이션 뷰도 포함하고 있습니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 paginator의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드 (Paginator / LengthAwarePaginator Instance Methods)

각 paginator 인스턴스는 다음 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드 | 설명 |
| --- | --- |
| `$paginator->count()` | 현재 페이지에 표시된 아이템 개수를 가져옵니다. |
| `$paginator->currentPage()` | 현재 페이지 번호를 반환합니다. |
| `$paginator->firstItem()` | 결과 중 첫 번째 아이템의 순번을 반환합니다. |
| `$paginator->getOptions()` | paginator 설정 옵션을 가져옵니다. |
| `$paginator->getUrlRange($start, $end)` | 지정한 범위의 페이지 URL 목록을 생성합니다. |
| `$paginator->hasPages()` | 여러 페이지로 분할할 만큼 아이템이 충분한지 판단합니다. |
| `$paginator->hasMorePages()` | 더 많은 페이지가 있는지 판단합니다. |
| `$paginator->items()` | 현재 페이지의 아이템들을 가져옵니다. |
| `$paginator->lastItem()` | 결과 중 마지막 아이템의 순번을 반환합니다. |
| `$paginator->lastPage()` | 마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시 지원 안 함) |
| `$paginator->nextPageUrl()` | 다음 페이지 URL을 반환합니다. |
| `$paginator->onFirstPage()` | 현재 첫 페이지인지 판단합니다. |
| `$paginator->perPage()` | 한 페이지에 표시할 아이템 개수를 반환합니다. |
| `$paginator->previousPageUrl()` | 이전 페이지 URL을 반환합니다. |
| `$paginator->total()` | 전체 아이템 개수를 반환합니다. (`simplePaginate` 사용 시 지원 안 함) |
| `$paginator->url($page)` | 지정한 페이지 번호에 대한 URL을 반환합니다. |
| `$paginator->getPageName()` | 페이지 번호를 저장하는 쿼리 스트링 변수명을 반환합니다. |
| `$paginator->setPageName($name)` | 페이지 번호를 저장하는 쿼리 스트링 변수명을 설정합니다. |
| `$paginator->through($callback)` | 콜백 함수를 통해 각 아이템을 변환합니다. |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메서드 (Cursor Paginator Instance Methods)

각 cursor paginator 인스턴스는 다음 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                       |
| ------------------------------- | ----------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지에 표시된 아이템 개수를 반환합니다.             |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 가져옵니다.                           |
| `$paginator->getOptions()`      | paginator 설정 옵션을 가져옵니다.                          |
| `$paginator->hasPages()`        | 여러 페이지로 분할할 만큼 아이템이 충분한지 판단합니다.     |
| `$paginator->hasMorePages()`    | 더 많은 페이지가 있는지 판단합니다.                        |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리 스트링 변수명을 반환합니다.           |
| `$paginator->items()`           | 현재 페이지의 아이템들을 가져옵니다.                       |
| `$paginator->nextCursor()`      | 다음 페이지의 커서 인스턴스를 반환합니다.                 |
| `$paginator->nextPageUrl()`     | 다음 페이지 URL을 반환합니다.                              |
| `$paginator->onFirstPage()`     | 현재 첫 페이지인지 판단합니다.                              |
| `$paginator->onLastPage()`      | 현재 마지막 페이지인지 판단합니다.                         |
| `$paginator->perPage()`         | 한 페이지에 표시할 아이템 개수를 반환합니다.               |
| `$paginator->previousCursor()`  | 이전 페이지의 커서 인스턴스를 반환합니다.                 |
| `$paginator->previousPageUrl()` | 이전 페이지 URL을 반환합니다.                              |
| `$paginator->setCursorName()`   | 커서를 저장하는 쿼리 스트링 변수명을 설정합니다.           |
| `$paginator->url($cursor)`      | 지정한 커서 인스턴스에 대한 URL을 반환합니다.             |

</div>