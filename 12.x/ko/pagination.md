# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이즈](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 수 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이즈](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 방식이 한층 더 신선하게 느껴지시길 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/12.x/queries) 및 [Eloquent ORM](/docs/12.x/eloquent)와 통합되어 있고, 데이터베이스 레코드를 손쉽게 페이지네이션할 수 있는 간편한 기능을 기본 설정 없이 제공합니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 또한, Bootstrap 페이지네이션 지원도 가능합니다.

<a name="tailwind"></a>
#### Tailwind

Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용하는 경우, 애플리케이션의 `resources/css/app.css` 파일에 이미 Laravel의 페이지네이션 뷰를 올바르게 `@source`하도록 설정되어 있을 것입니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션 (Paginating Query Builder Results)

페이지네이션에는 여러 가지 방법이 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/12.x/queries)나 [Eloquent 쿼리](/docs/12.x/eloquent)에 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 현재 사용자가 보고 있는 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 설정해줍니다. 기본적으로, 현재 페이지는 HTTP 요청의 쿼리 문자열 인수 중 `page`의 값을 통해 감지합니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성한 링크에도 자동으로 포함됩니다.

이 예시에서, `paginate` 메서드에 전달하는 유일한 인수는 "한 페이지에 보여줄 항목의 개수"입니다. 여기서는 한 페이지에 `15`개 항목을 보여주도록 지정해보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
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

`paginate` 메서드는 데이터베이스에서 레코드를 조회하기 전에 쿼리로 매칭되는 총 레코드 수를 계산합니다. 이렇게 하면 페이지네이터가 전체 페이지 수를 알 수 있게 됩니다. 하지만, 애플리케이션 UI에서 전체 페이지 수 표시가 필요하지 않다면, 이 기록 카운트 쿼리는 불필요합니다.

따라서, 애플리케이션 UI에서 "다음"과 "이전" 링크만 간단하게 표시하면 되는 경우, `simplePaginate` 메서드를 사용하여 한 번의 효율적인 쿼리만 실행할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션 (Paginating Eloquent Results)

[Eloquent](/docs/12.x/eloquent) 쿼리도 페이지네이션할 수 있습니다. 아래 예시에서는 `App\Models\User` 모델을 페이지네이션하며, 한 페이지에 15개의 레코드를 표시합니다. 쿼리 빌더로 페이지네이션할 때와 거의 동일한 문법임을 알 수 있습니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, 쿼리에서 `where` 절 등 다른 조건을 설정한 후에도 `paginate` 메서드를 호출할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델에서 `simplePaginate` 메서드를 사용할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

마찬가지로, Eloquent 모델에서 `cursorPaginate` 메서드를 사용해 커서 페이지네이션을 할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에서 여러 Paginator 인스턴스 사용

하나의 화면에서 두 개 이상의 페이지네이터를 렌더링해야 하는 경우가 있습니다. 하지만, 두 페이지네이터 인스턴스 모두 현재 페이지 정보를 저장하기 위해 `page` 쿼리 문자열 파라미터를 사용하면, 두 페이지네이터가 서로 충돌하게 됩니다. 이런 경우, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수로 페이지네이터의 현재 페이지를 저장할 쿼리 문자열 파라미터명을 넘겨서 문제를 해결할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate`가 SQL의 "offset" 절을 사용하는 반면, 커서 페이지네이션은 쿼리에서 정렬된 컬럼의 값을 비교하는 "where" 절을 만들어 훨씬 효율적으로 데이터를 가져옵니다. 이 방식은 특히 대용량 데이터셋과 "무한 스크롤" 같은 인터페이스에 적합합니다.

offset 기반 페이지네이션은 URL 쿼리 문자열에 페이지 번호를 포함하지만, 커서 기반 페이지네이션은 "cursor"라는 문자열을 쿼리 문자열에 넣습니다. 이 커서는 다음 페이지네이션 쿼리를 시작할 위치와 방향이 인코딩된 문자열입니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 기반 페이지네이터 인스턴스는 쿼리 빌더의 `cursorPaginate` 메서드를 사용해 생성합니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 얻었다면, [`paginate`와 `simplePaginate`를 사용할 때와 마찬가지로](#displaying-pagination-results) 페이지네이션 결과를 표시할 수 있습니다. 커서 페이지네이터가 제공하는 인스턴스 메서드에 대한 자세한 정보는 [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 필요합니다. 또한, 정렬에 사용하는 컬럼은 페이지네이션하는 테이블에 반드시 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 vs. 오프셋 페이지네이션 (Cursor vs. Offset Pagination)

offset 페이지네이션과 커서 페이지네이션의 차이를 살펴보기 위해 SQL 예제를 보겠습니다. 둘 모두 `users` 테이블을 `id`로 정렬했을 때 "두 번째 페이지"의 결과를 보여줍니다:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션의 오프셋 페이지네이션 대비 장점은 다음과 같습니다:

- 대용량 데이터셋의 경우, 정렬 컬럼에 인덱스가 잡혀 있으면 커서 페이지네이션이 더 나은 성능을 보입니다. "offset"은 이전의 모든 데이터들을 스캔하게 되지만, 커서는 바로 다음 지점에서 가져오기 때문입니다.
- 쓰기 작업이 빈번한 데이터셋에서는 오프셋 페이지네이션 사용 시 사용자가 보고 있는 페이지에 데이터가 추가되거나 삭제되면 레코드가 누락되거나 중복으로 표시될 수 있습니다.

반면, 커서 페이지네이션은 다음과 같은 제약이 있습니다:

- `simplePaginate`와 마찬가지로, "다음"과 "이전" 링크로만 탐색할 수 있고, 특정 페이지 번호로 바로 이동하는 링크는 지원하지 않습니다.
- 정렬 기준이 반드시 하나 이상의 유일한 컬럼 혹은 컬럼 조합이어야 하며, `null` 값이 포함된 컬럼은 지원하지 않습니다.
- "order by" 절의 쿼리 식은 반드시 별칭이 있고 "select" 절에도 추가되어 있어야만 지원됩니다.
- 파라미터가 들어간 쿼리 식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성 (Manually Creating a Paginator)

이미 메모리상에 들고 있는 배열 데이터를 대상으로 페이지네이터 인스턴스를 수동으로 생성하고 싶을 때도 있습니다. 이런 경우, 필요에 맞게 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나를 직접 만들어 사용할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 전체 항목의 개수를 알 필요가 없습니다. 하지만, 그렇기 때문에 마지막 페이지의 인덱스를 가져오는 메서드는 제공하지 않습니다. 반면, `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수로 생성할 수 있지만, 전체 항목의 개수를 반드시 전달해야 합니다.

즉, `Paginator`는 쿼리 빌더에서 사용하는 `simplePaginate`, `CursorPaginator`는 `cursorPaginate`, `LengthAwarePaginator`는 `paginate`와 일치하는 동작을 합니다.

> [!WARNING]
> 페이지네이터 인스턴스를 수동으로 생성할 때는, 결과 배열을 직접 "슬라이스(slice)"해서 전달해야 합니다. 방법을 모를 경우 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이즈 (Customizing Pagination URLs)

기본적으로 페이지네이터에서 생성하는 링크는 현재 요청의 URI를 그대로 따릅니다. 하지만, 페이지네이터의 `withPath` 메서드를 사용하면 페이지네이터가 링크를 생성할 때 사용하는 URI를 커스터마이즈할 수 있습니다. 예를 들어, 페이지네이터 링크가 `http://example.com/admin/users?page=N` 형태로 나가길 원한다면 `/admin/users`를 `withPath` 메서드에 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가하기 (Appending Query String Values)

페이지네이션 링크의 쿼리 문자열에 값을 추가하려면 `appends` 메서드를 사용하면 됩니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 호출하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리 문자열 값을 페이지네이션 링크에 추가하려면 `withQueryString` 메서드를 사용하세요:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기 (Appending Hash Fragments)

페이지네이터가 생성하는 URL의 끝에 "해시 프래그먼트"를 추가하려면, `fragment` 메서드를 이용하세요. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 붙이려면 다음과 같이 하면 됩니다:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를, `simplePaginate` 메서드는 `Illuminate\Pagination\Paginator` 인스턴스를 받게 됩니다. 마지막으로, `cursorPaginate` 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합을 설명하는 다양한 메서드를 제공합니다. 또, 페이지네이터 인스턴스 자체가 이터레이터이므로 배열처럼 루프를 돌릴 수 있습니다. 즉, 결과를 가져온 뒤에는 [Blade](/docs/12.x/blade)를 통해 결과 목록과 페이지 링크를 아래와 같이 쉽게 표시할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지로 이동할 수 있는 링크를 렌더링합니다. 이 링크들에는 이미 적절한 `page` 쿼리 문자열 변수가 포함되어 있습니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 수 조정 (Adjusting the Pagination Link Window)

페이지네이터가 페이지네이션 링크를 표시할 때, 현재 페이지와 함께 그 앞뒤로 3페이지씩의 링크가 보여집니다. `onEachSide` 메서드를 통해, 현재 페이지 기준 중간에 표시되는 링크 개수를 자유롭게 조절할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환 (Converting Results to JSON)

Laravel의 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며, `toJson` 메서드를 제공합니다. 따라서 페이지네이션 결과를 쉽게 JSON으로 변환할 수 있습니다. 또, 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함되며, 실제 레코드 데이터는 JSON 배열의 `data` 키를 통해 제공됩니다. 다음은 페이지네이터 인스턴스를 라우트에서 반환했을 때 생성되는 JSON 예시입니다:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이즈 (Customizing the Pagination View)

기본적으로, 페이지네이션 링크를 렌더링할 때 사용하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환되도록 되어있습니다. 하지만 Tailwind를 사용하지 않을 경우, 원하는 형태의 뷰를 직접 정의할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드에 첫 번째 인수로 뷰 이름을 넘기면 해당 뷰를 사용할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 넘기기 -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이지네이션 뷰를 가장 쉽게 커스터마이즈하는 방법은 `vendor:publish` 명령어를 통해 뷰를 앱의 `resources/views/vendor` 디렉토리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면 뷰가 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 복사됩니다. 이 디렉토리의 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당하며, 이 파일을 편집해서 페이지네이션 HTML을 원하는 스타일로 수정할 수 있습니다.

기본 페이지네이션 뷰로 다른 파일을 지정하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/) 기반의 페이지네이션 뷰도 기본으로 제공합니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 혹은 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 아래와 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                                  | 설명                                                                                           |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `$paginator->count()`                   | 현재 페이지에 포함된 항목의 개수를 반환합니다.                                                   |
| `$paginator->currentPage()`             | 현재 페이지 번호를 반환합니다.                                                                  |
| `$paginator->firstItem()`               | 현재 결과에서 첫 번째 항목의 번호를 반환합니다.                                                  |
| `$paginator->getOptions()`              | 페이지네이터 옵션을 반환합니다.                                                                 |
| `$paginator->getUrlRange($start, $end)` | 지정된 페이지 범위에 대한 페이지네이션 URL 배열을 생성합니다.                                    |
| `$paginator->hasPages()`                | 여러 페이지로 분할할 만큼 충분한 항목이 있는지 판단합니다.                                       |
| `$paginator->hasMorePages()`            | 데이터 저장소에 더 많은 항목이 있는지 판단합니다.                                                |
| `$paginator->items()`                   | 현재 페이지의 항목 배열을 반환합니다.                                                           |
| `$paginator->lastItem()`                | 현재 결과에서 마지막 항목의 번호를 반환합니다.                                                  |
| `$paginator->lastPage()`                | 마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시 미지원)                                 |
| `$paginator->nextPageUrl()`             | 다음 페이지로 이동할 URL을 반환합니다.                                                           |
| `$paginator->onFirstPage()`             | 현재 페이지가 첫 번째 페이지인지 판단합니다.                                                     |
| `$paginator->onLastPage()`              | 현재 페이지가 마지막 페이지인지 판단합니다.                                                      |
| `$paginator->perPage()`                 | 한 페이지에 표시할 항목 개수를 반환합니다.                                                       |
| `$paginator->previousPageUrl()`         | 이전 페이지로 이동할 URL을 반환합니다.                                                           |
| `$paginator->total()`                   | 데이터 저장소의 전체 항목 수를 반환합니다. (`simplePaginate` 사용 시 미지원)                      |
| `$paginator->url($page)`                | 지정한 페이지 번호에 해당하는 URL을 반환합니다.                                                  |
| `$paginator->getPageName()`             | 페이지 정보를 저장하는 쿼리 문자열 변수명을 반환합니다.                                          |
| `$paginator->setPageName($name)`        | 페이지 정보를 저장하는 쿼리 문자열 변수명을 설정합니다.                                          |
| `$paginator->through($callback)`        | 각 항목에 콜백을 적용하여 변환합니다.                                                           |

</div>

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드 (Cursor Paginator Instance Methods)

각 커서 페이지네이터 인스턴스는 아래와 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                               |
| ------------------------------- | ------------------------------------------------------------------ |
| `$paginator->count()`           | 현재 페이지의 항목 개수를 반환합니다.                               |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 반환합니다.                                   |
| `$paginator->getOptions()`      | 페이지네이터 옵션을 반환합니다.                                     |
| `$paginator->hasPages()`        | 여러 페이지로 분할할 만큼 충분한 항목이 있는지 판단합니다.           |
| `$paginator->hasMorePages()`    | 데이터 저장소에 더 많은 항목이 있는지 판단합니다.                    |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리 문자열 변수명을 반환합니다.                    |
| `$paginator->items()`           | 현재 페이지의 항목 배열을 반환합니다.                               |
| `$paginator->nextCursor()`      | 다음 항목 집합의 커서 인스턴스를 반환합니다.                        |
| `$paginator->nextPageUrl()`     | 다음 페이지 URL을 반환합니다.                                       |
| `$paginator->onFirstPage()`     | 현재 페이지가 첫 번째 페이지인지 판단합니다.                        |
| `$paginator->onLastPage()`      | 현재 페이지가 마지막 페이지인지 판단합니다.                         |
| `$paginator->perPage()`         | 한 페이지에 표시할 항목 개수를 반환합니다.                           |
| `$paginator->previousCursor()`  | 이전 항목 집합의 커서 인스턴스를 반환합니다.                        |
| `$paginator->previousPageUrl()` | 이전 페이지 URL을 반환합니다.                                       |
| `$paginator->setCursorName()`   | 커서를 저장하는 쿼리 문자열 변수명을 설정합니다.                    |
| `$paginator->url($cursor)`      | 지정한 커서 인스턴스에 해당하는 URL을 반환합니다.                   |

</div>
