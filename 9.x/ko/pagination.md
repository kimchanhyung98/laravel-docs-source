# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 페이저 인스턴스 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이징 결과 화면에 출력하기](#displaying-pagination-results)
    - [페이지네이션 링크 범위 조정하기](#adjusting-the-pagination-link-window)
    - [JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 접근 방식은 신선한 바람이 될 것이라 기대합니다. Laravel의 페이저는 [쿼리 빌더](/docs/9.x/queries)와 [Eloquent ORM](/docs/9.x/eloquent)와 통합되어 있으며, 별도의 설정 없이 편리하고 사용하기 쉬운 데이터베이스 레코드 페이지네이션을 제공합니다.

기본적으로 페이저가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환되지만, Bootstrap 페이지네이션 지원도 제공됩니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용한다면, 애플리케이션의 `tailwind.config.js` 파일 내 `content` 키에 Laravel 페이지네이션 뷰 경로를 반드시 포함시켜 Tailwind 클래스가 정리(purge)되지 않도록 해야 합니다:

```js
content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
    './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
],
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션 (Paginating Query Builder Results)

아이템을 페이지네이션하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 [쿼리 빌더](/docs/9.x/queries)나 [Eloquent 쿼리](/docs/9.x/eloquent)의 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지에 따라 자동으로 SQL 쿼리의 `limit`와 `offset`을 설정해줍니다. 기본적으로 현재 페이지는 HTTP 요청의 쿼리 문자열 인자인 `page` 값을 기준으로 인식됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이저가 생성하는 링크에도 자동으로 추가됩니다.

다음 예제에서 `paginate` 메서드에 전달하는 인수는 단지 한 가지, 즉 한 페이지에 보여줄 아이템 수입니다. 여기서는 한 페이지당 `15`개의 아이템을 표시하도록 지정합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션 사용자를 모두 보여줍니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### 간단한 페이지네이션 (Simple Pagination)

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리와 일치하는 전체 레코드 수를 먼저 세는 작업을 수행합니다. 이는 페이저가 전체 페이지 수를 알기 위해 필요합니다. 그러나 애플리케이션 UI에서 전체 페이지 수를 표시할 필요가 없다면, 이 전체 레코드 수를 세는 쿼리는 불필요한 비용이 될 수 있습니다.

따라서 만약 "다음" 및 "이전" 링크만 간단히 표시하려면, `simplePaginate` 메서드를 사용하여 효율적인 단일 쿼리 방식 페이지네이션을 할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션 (Paginating Eloquent Results)

[Eloquent](/docs/9.x/eloquent) 쿼리도 페이지네이션할 수 있습니다. 다음 예시에서는 `App\Models\User` 모델을 페이지네이션하며, 페이지당 15개 레코드를 보여준다고 지정했습니다. 구문은 쿼리 빌더 페이지네이션과 거의 동일함을 알 수 있습니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 절 등 추가 조건을 설정한 후에도 `paginate`를 호출할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

`simplePaginate` 메서드도 Eloquent 모델에 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

마찬가지로, Eloquent 모델에 대해 `cursorPaginate` 메서드를 사용하여 커서 페이지네이션도 할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이저 인스턴스 사용하기

한 화면에 두 개 이상의 별도 페이저를 렌더링해야 할 경우가 있습니다. 이때 두 페이저 인스턴스가 모두 기본 `page` 쿼리 문자열 변수를 사용하면 충돌이 발생합니다. 이 문제를 해결하려면 `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인자로, 현재 페이지를 저장하는 쿼리 문자열 키 이름을 직접 지정할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate`는 SQL의 `offset` 절을 사용하여 쿼리를 생성하지만, 커서 페이지네이션은 쿼리 내 정렬된 컬럼 값을 비교하는 `where` 절을 생성하여 구현합니다. 이는 Laravel의 페이지네이션 메서드 중 가장 효율적인 데이터베이스 성능을 제공합니다. 특히 대용량 데이터셋이나 무한 스크롤 UI에 적합합니다.

오프셋 기반 페이지네이션과 달리, 커서 페이지네이션은 쿼리 문자열에 페이지 번호 대신 "커서(cursor)" 문자열을 포함합니다. 이 커서는 다음 페이지네이션 쿼리가 시작할 위치와 진행 방향을 담은 인코딩된 문자열입니다:

```plaintext
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더에서 `cursorPaginate` 메서드를 호출해 커서 페이저 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이저 인스턴스를 얻으면, `paginate`, `simplePaginate`처럼 [페이징 결과를 출력](#displaying-pagination-results)할 수 있습니다. 커서 페이저가 제공하는 인스턴스 메서드에 대한 자세한 내용은 [커서 페이저 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 `order by` 절이 존재해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션 차이점

오프셋 기반 페이지네이션과 커서 페이지네이션의 차이를 보여주기 위한 예시 SQL 쿼리입니다. 둘 다 `users` 테이블에서 `id`를 기준으로 정렬한 결과의 "두 번째 페이지"를 출력합니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션이 오프셋 페이지네이션보다 갖는 장점은 다음과 같습니다:

- 대용량 데이터셋에서 정렬 컬럼에 인덱스가 있으면 커서 페이지네이션이 더 나은 성능을 제공합니다. 오프셋 절은 앞선 모든 매칭 데이터를 스캔하기 때문입니다.
- 자주 쓰기 작업이 발생하는 데이터셋에서는 오프셋 페이지네이션이 현재 사용자가 보고 있는 페이지에 새롭게 추가되거나 삭제된 레코드 때문에 데이터를 건너뛰거나 중복해서 보여줄 수 있습니다.

하지만 커서 페이지네이션은 다음과 같은 제한 사항도 있습니다:

- `simplePaginate`와 마찬가지로 "다음" 및 "이전" 링크만 생성하며, 페이지 번호가 포함된 링크를 생성하지 못합니다.
- 정렬 기준 컬럼은 반드시 하나 이상의 고유(unique) 컬럼 또는 고유 조합이어야 하며, `null` 값을 가진 컬럼은 지원하지 않습니다.
- `order by` 절 내 쿼리 식은 별칭(alias)이 지정되고 `select` 절에도 포함된 경우에만 지원됩니다.
- 파라미터가 포함된 쿼리 식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이저 인스턴스 생성하기 (Manually Creating A Paginator)

이미 메모리에 가지고 있는 배열 아이템에 대해 수동으로 페이지네이터 인스턴스를 생성할 수도 있습니다. 상황에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나를 생성하면 됩니다.

`Paginator`와 `CursorPaginator`는 전체 아이템 수를 몰라도 되지만, 그래서 마지막 페이지 인덱스를 반환하는 메서드가 없습니다. 반면 `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인자를 받지만, 결과 전체 아이템 수를 반드시 전달해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`와 대응되고, `CursorPaginator`는 `cursorPaginate`, `LengthAwarePaginator`는 `paginate` 메서드와 각각 대응됩니다.

> [!WARNING]
> 수동으로 페이저 인스턴스를 만들 때는 페이저에 넘길 배열 결과를 직접 적절히 잘라(slice) 전달해야 합니다. 방법이 헷갈린다면 PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징 (Customizing Pagination URLs)

기본적으로 페이저가 생성하는 링크는 현재 요청의 URI를 따릅니다. 그러나 페이저의 `withPath` 메서드를 사용하면 링크 생성 시 사용할 URI 경로를 커스터마이징할 수 있습니다. 예를 들어, 페이저가 `http://example.com/admin/users?page=N`과 같은 URL을 생성하게 하려면 다음처럼 `withPath`에 `/admin/users`를 넘기면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    //
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 덧붙이기 (Appending Query String Values)

페이지네이션 링크의 쿼리 문자열에 값을 추가하려면 `appends` 메서드를 사용합니다. 예를 들어 각 페이지 링크에 `sort=votes`를 붙이고 싶다면 다음과 같이 호출하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    //
});
```

현재 요청의 모든 쿼리 문자열을 페이지네이션 링크에 그대로 덧붙이려면 `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 덧붙이기 (Appending Hash Fragments)

페이저가 생성하는 URL 뒤에 "해시 프래그먼트"(`#users` 등)를 덧붙이고 싶다면 `fragment` 메서드를 사용하면 됩니다. 예를 들어 모든 페이지네이션 링크에 `#users`를 덧붙이고 싶다면 다음과 같이 호출하세요:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이징 결과 화면에 출력하기 (Displaying Pagination Results)

`paginate` 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환하고, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를 반환하며, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이들 객체는 결과 집합 관련 여러 정보를 제공하는 메서드를 가지고 있으며, 페이저 인스턴스 자체가 반복 가능한 객체(iterable)이기 때문에 배열처럼 반복문에 사용할 수 있습니다. 따라서 결과를 조회한 후 [Blade](/docs/9.x/blade)를 활용해 다음과 같이 출력할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과의 나머지 페이지에 대한 링크를 렌더링합니다. 이 링크들에는 이미 적절한 `page` 쿼리 문자열 변수가 포함되어 있습니다. `links`가 생성하는 HTML은 기본적으로 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 범위 조정하기 (Adjusting The Pagination Link Window)

페이저가 링크를 표시할 때, 현재 페이지 번호 주변으로 기본적으로 앞뒤 3개 페이지 링크가 표시됩니다. `onEachSide` 메서드를 사용하면 현재 페이지를 기준으로 왼쪽과 오른쪽에 추가로 몇 개의 링크를 보여줄지 조절 가능합니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### JSON으로 변환하기 (Converting Results To JSON)

Laravel 페이저 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공해 페이지네이션 결과를 쉽게 JSON으로 변환할 수 있습니다. 라우트나 컨트롤러 액션에서 페이저 인스턴스를 반환해도 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이저 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 포함되며, 결과 레코드는 `data` 키 아래 배열 형태로 나옵니다. 다음은 라우트에서 페이저를 반환할 때 생성되는 JSON 예시입니다:

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
            // 레코드 내용...
        },
        {
            // 레코드 내용...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이징 (Customizing The Pagination View)

기본적으로 페이지네이션 링크를 렌더링하는 뷰는 [Tailwind CSS](https://tailwindcss.com)와 호환됩니다. 그러나 Tailwind를 사용하지 않는 경우, 직접 뷰를 정의해 사용할 수 있습니다. 페이저 인스턴스에서 `links` 메서드 호출 시 첫 번째 인수로 뷰 이름을 전달하면 해당 뷰가 렌더링됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달하기 -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 편한 방법은 `vendor:publish` Artisan 커맨드를 통해 뷰 파일을 `resources/views/vendor` 디렉토리로 내보내 편집하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령은 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 관련 뷰를 생성합니다. 여기의 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰이며, 이 파일을 수정해 페이지네이션 HTML을 커스터마이징할 수 있습니다.

다른 뷰 파일을 기본 페이지네이션 뷰로 지정하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이저의 `defaultView`와 `defaultSimpleView` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Bootstrap 사용하기 (Using Bootstrap)

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 제작된 페이지네이션 뷰도 포함하고 있습니다. 기본 Tailwind 뷰 대신 이 Bootstrap 뷰를 사용하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이저의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드 (Paginator / LengthAwarePaginator Instance Methods)

각 페이저 인스턴스는 다음과 같은 추가 페이지네이션 정보를 제공하는 메서드를 갖고 있습니다:

| 메서드                       | 설명                                              |
|-----------------------------|-------------------------------------------------|
| `$paginator->count()`         | 현재 페이지에 포함된 아이템 수를 가져옵니다.          |
| `$paginator->currentPage()`   | 현재 페이지 번호를 가져옵니다.                       |
| `$paginator->firstItem()`     | 결과 중 첫 번째 아이템의 전체 집합 내 순번을 가져옵니다. |
| `$paginator->getOptions()`    | 페이저 옵션을 가져옵니다.                           |
| `$paginator->getUrlRange($start, $end)` | 주어진 범위의 페이지 URL들을 생성합니다.            |
| `$paginator->hasPages()`      | 여러 페이지로 나누기 위한 충분한 아이템이 있는지 확인합니다. |
| `$paginator->hasMorePages()`  | 추가 페이지가 더 존재하는지 확인합니다.               |
| `$paginator->items()`         | 현재 페이지에 포함된 아이템들을 가져옵니다.            |
| `$paginator->lastItem()`      | 결과 중 마지막 아이템의 전체 집합 내 순번을 가져옵니다. |
| `$paginator->lastPage()`      | 마지막 페이지 번호를 가져옵니다. (`simplePaginate` 사용 시 존재하지 않음) |
| `$paginator->nextPageUrl()`   | 다음 페이지로 가는 URL을 가져옵니다.                   |
| `$paginator->onFirstPage()`   | 현재 페이지가 첫 페이지인지 확인합니다.                 |
| `$paginator->perPage()`       | 한 페이지당 보여줄 아이템 수를 가져옵니다.               |
| `$paginator->previousPageUrl()` | 이전 페이지로 가는 URL을 가져옵니다.                   |
| `$paginator->total()`          | 전체 아이템 개수를 가져옵니다. (`simplePaginate` 사용 시 존재하지 않음) |
| `$paginator->url($page)`       | 지정한 페이지 번호의 URL을 가져옵니다.                  |
| `$paginator->getPageName()`    | 페이지 번호를 저장하는 쿼리 문자열 변수명을 가져옵니다.     |
| `$paginator->setPageName($name)` | 페이지 번호를 저장하는 쿼리 문자열 변수명을 설정합니다.    |

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메서드 (Cursor Paginator Instance Methods)

각 커서 페이저 인스턴스는 다음과 같은 추가 페이지네이션 정보를 제공하는 메서드를 제공합니다:

| 메서드                          | 설명                                                   |
|--------------------------------|------------------------------------------------------|
| `$paginator->count()`            | 현재 페이지에 포함된 아이템 수를 가져옵니다.                 |
| `$paginator->cursor()`           | 현재 커서 인스턴스를 가져옵니다.                             |
| `$paginator->getOptions()`       | 페이저 옵션을 가져옵니다.                                  |
| `$paginator->hasPages()`         | 여러 페이지로 나누기 위한 충분한 아이템이 있는지 확인합니다.      |
| `$paginator->hasMorePages()`     | 추가 페이지가 더 존재하는지 확인합니다.                        |
| `$paginator->getCursorName()`    | 커서를 저장하는 쿼리 문자열 변수명을 가져옵니다.                 |
| `$paginator->items()`            | 현재 페이지에 포함된 아이템들을 가져옵니다.                     |
| `$paginator->nextCursor()`       | 다음 페이지를 위한 커서 인스턴스를 가져옵니다.                   |
| `$paginator->nextPageUrl()`      | 다음 페이지의 URL을 가져옵니다.                                |
| `$paginator->onFirstPage()`      | 현재 페이지가 첫 페이지인지 확인합니다.                          |
| `$paginator->onLastPage()`       | 현재 페이지가 마지막 페이지인지 확인합니다.                       |
| `$paginator->perPage()`          | 한 페이지당 보여줄 아이템 수를 가져옵니다.                        |
| `$paginator->previousCursor()`   | 이전 페이지를 위한 커서 인스턴스를 가져옵니다.                   |
| `$paginator->previousPageUrl()`  | 이전 페이지의 URL을 가져옵니다.                                |
| `$paginator->setCursorName()`    | 커서를 저장하는 쿼리 문자열 변수명을 설정합니다.                  |
| `$paginator->url($cursor)`       | 지정한 커서 인스턴스에 대한 URL을 가져옵니다.                    |