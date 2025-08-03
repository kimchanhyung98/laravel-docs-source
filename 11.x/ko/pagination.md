# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 페이지네이터 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 사용자 지정](#customizing-pagination-urls)
- [페이지네이션 결과 출력](#displaying-pagination-results)
    - [페이지네이션 링크 범위 조정하기](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 사용자 지정](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 접근법은 신선한 바람과 같은 편리함을 제공할 것입니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/11.x/queries) 및 [Eloquent ORM](/docs/11.x/eloquent)와 통합되어 있으며, 별도의 설정 없이도 데이터베이스 레코드를 간편하고 쉽게 페이지네이션할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다; 그러나 Bootstrap 페이지네이션도 지원합니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용하는 경우, 애플리케이션의 `tailwind.config.js` 파일의 `content` 키에 Laravel 페이지네이션 뷰를 참조하도록 설정하여 해당 Tailwind 클래스가 제거되지 않도록 해야 합니다:

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

항목을 페이지네이션하는 여러 방법이 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/11.x/queries) 또는 [Eloquent 쿼리](/docs/11.x/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지에 따라 쿼리의 "limit"와 "offset"을 자동으로 설정합니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 인수 값에서 감지합니다. 이 값은 Laravel에서 자동으로 인식되며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

다음 예제에서는 `paginate` 메서드에 전달하는 인수가 페이지당 표시하고 싶은 항목 수뿐입니다. 이번 예제에서는 페이지당 15개의 항목을 표시하도록 지정했습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자 보여주기.
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

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리와 일치하는 총 레코드 수를 계산합니다. 이는 페이지네이터가 전체 페이지 수를 알기 위함입니다. 그러나 만약 애플리케이션 UI에서 총 페이지 수를 보여줄 계획이 없다면, 이 레코드 수 계산 쿼리는 불필요합니다.

따라서 UI에 단순히 "다음" 및 "이전" 링크만 표시하면 되는 경우, `simplePaginate` 메서드를 사용하면 조회 쿼리를 한 번만 실행하여 효율적으로 페이지네이션할 수 있습니다:

```
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션 (Paginating Eloquent Results)

[Eloquent](/docs/11.x/eloquent) 쿼리도 페이지네이션할 수 있습니다. 아래 예제에서는 `App\Models\User` 모델을 페이지네이션하고, 페이지당 15개의 레코드를 표시하도록 지정했습니다. 이처럼 문법은 쿼리 빌더의 페이지네이션과 거의 동일합니다:

```
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 절 같은 다른 조건을 쿼리에 설정한 뒤 `paginate` 메서드를 호출할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

```
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

또한 `cursorPaginate` 메서드를 사용해 Eloquent 모델을 커서 페이지네이션할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용하기

때로는 애플리케이션 화면에 두 개 이상의 별도 페이지네이터를 표시해야 하는 경우가 있습니다. 하지만 두 페이지네이터 인스턴스가 모두 현재 페이지 번호를 저장하기 위해 `page` 쿼리 문자열 파라미터를 사용한다면 충돌이 발생할 수 있습니다. 이 문제를 해결하려면 `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인자로 페이지네이터가 현재 페이지를 저장하는 데 사용할 쿼리 문자열 이름을 지정할 수 있습니다:

```
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate`는 SQL의 "offset" 절을 사용해 쿼리를 생성하는 반면, 커서 페이지네이션은 정렬된 컬럼 값을 비교하는 "where" 절을 만들어 가장 효율적인 데이터베이스 성능을 제공합니다. 이 방법은 대용량 데이터셋과 무한 스크롤 UI에 특히 적합합니다.

오프셋 페이지네이션은 쿼리 문자열에 페이지 번호를 포함하는 데 반해, 커서 페이지네이션은 쿼리 문자열에 "cursor"라는 인코딩된 문자열을 넣습니다. 이 커서는 다음 페이지네이션 시작 위치와 이동 방향을 포함합니다:

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 통해 커서 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 가져오면, 일반적인 `paginate` 및 `simplePaginate` 메서드를 사용할 때처럼 [페이지네이션 결과를 출력](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터의 인스턴스 메서드에 대한 자세한 내용은 [커서 페이지네이터 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]  
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어 있어야 하며, 정렬하는 컬럼들은 페이지네이션 대상 테이블에 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션 비교

오프셋 페이지네이션과 커서 페이지네이션의 차이를 보여주기 위해, `users` 테이블을 `id` 컬럼 기준으로 정렬하여 "두 번째 페이지" 결과를 가져오는 SQL 예제를 살펴보겠습니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션은 다음과 같은 장점이 있습니다:

- 대규모 데이터셋에서는 "order by" 컬럼이 인덱스되어 있을 경우, "offset" 절은 이전의 모든 데이터를 스캔하기 때문에 커서 페이지네이션이 더 빠릅니다.
- 자주 데이터가 수정되는 데이터셋에서는 오프셋 페이지네이션이 사용자가 보고 있는 페이지에 최근 추가되거나 삭제된 레코드 때문에 중복되거나 누락된 결과를 보여줄 수 있습니다.

하지만 커서 페이지네이션은 다음과 같은 제한점이 있습니다:

- `simplePaginate`처럼 "다음"과 "이전" 링크만 지원하며, 페이지 번호 링크 생성은 지원하지 않습니다.
- 주문 기준이 되는 컬럼은 적어도 하나의 고유 컬럼이거나 고유한 컬럼 조합이어야 합니다. null 값을 포함한 컬럼은 지원하지 않습니다.
- "order by" 절의 쿼리 표현식은 별칭(alias)이 붙고 select 절에도 포함되어야 지원됩니다.
- 인수를 포함한 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이지네이터 생성하기 (Manually Creating a Paginator)

때로는 이미 메모리에 저장된 배열을 가지고 직접 페이지네이션 인스턴스를 생성하고 싶을 수 있습니다. 이럴 때는 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator` 또는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 직접 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 전체 항목 수를 알 필요가 없기 때문에 마지막 페이지 인덱스를 구하는 메서드는 없습니다. 반면 `LengthAwarePaginator`는 `Paginator`와 거의 같은 인수를 받지만, 전체 항목 수를 반드시 지정해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate` 메서드에 대응하고, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate` 메서드에 대응합니다.

> [!WARNING]  
> 수동으로 페이지네이터를 생성할 때는 전달하는 결과 배열을 직접 적절히 "분할(slice)"해서 넘겨야 합니다. 방법이 익숙하지 않다면 PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 사용자 지정 (Customizing Pagination URLs)

기본적으로 페이지네이터가 생성하는 링크는 현재 요청 URI와 일치합니다. 그러나 페이지네이터의 `withPath` 메서드를 활용하면 링크 생성 시 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 형식의 링크를 생성하게 하려면, `withPath` 메서드에 `/admin/users`를 전달하면 됩니다:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 덧붙이기

`appends` 메서드를 사용하여 페이지네이션 링크의 쿼리 문자열에 값을 추가할 수 있습니다. 예를 들어, 모든 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 호출합니다:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리 문자열을 페이지네이션 링크에 덧붙이고 싶다면 `withQueryString` 메서드를 사용하세요:

```
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 조각 덧붙이기

페이지네이션 링크에 "해시 조각(hash fragment)"을 추가하려면 `fragment` 메서드를 사용하세요. 예를 들어, 모든 페이지네이션 링크 끝에 `#users`를 덧붙이려면 다음과 같이 호출합니다:

```
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 출력 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 받고, `simplePaginate` 메서드는 `Illuminate\Pagination\Paginator` 인스턴스를 반환합니다. 마지막으로 `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 관한 다양한 정보를 제공하는 메서드를 포함하고 있으며, 동시에 이 페이지네이터 인스턴스는 반복(iterable)이 가능해 배열처럼 루프 처리할 수 있습니다. 따라서 결과를 받아온 뒤엔 [Blade](/docs/11.x/blade)를 사용해 결과를 출력하고 페이지 링크를 렌더링할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합 내 나머지 페이지로의 링크를 렌더링해 줍니다. 이때 각 링크에는 이미 적절한 `page` 쿼리 문자열 변수가 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 범위 조정하기 (Adjusting the Pagination Link Window)

페이지네이터는 현재 페이지뿐 아니라 현재 페이지 앞뒤로 세 개씩 총 7개의 페이지 링크를 표시합니다. `onEachSide` 메서드를 사용하면, 현재 페이지를 중심으로 표시되는 추가 링크 수를 조절할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

위 예시는 현재 페이지 왼쪽과 오른쪽에 각 5개의 추가 페이지 링크를 표시합니다.

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기 (Converting Results to JSON)

Laravel 페이지네이터 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공합니다. 덕분에 페이지네이션 결과를 쉽게 JSON으로 변환할 수 있습니다. 또한 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 직렬화됩니다:

```
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 생성하는 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 포함됩니다. 실제 결과 데이터는 `data` 키에서 확인 가능합니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환했을 때 생성되는 JSON 예시입니다:

```
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
## 페이지네이션 뷰 사용자 지정 (Customizing the Pagination View)

기본적으로 페이지네이션 링크 출력에 사용하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 그러나 Tailwind를 사용하지 않는다면, 직접 원하는 뷰를 정의할 수 있습니다. 페이지네이터 인스턴스에서 `links` 메서드를 호출할 때 첫 번째 인자로 뷰 이름을 전달하면 해당 뷰를 사용할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터를 전달하는 경우... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 쉬운 방법은 `vendor:publish` 명령어로 페이지네이션 뷰를 `resources/views/vendor` 디렉터리로 내보내 수정하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령을 실행하면 뷰 파일이 `resources/views/vendor/pagination` 폴더에 생성됩니다. 이 디렉터리 내 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 대응하므로, 원하는 대로 이 파일을 편집해 HTML을 수정할 수 있습니다.

기본 페이지네이션 뷰를 다르게 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하세요:

```
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 부트스트랩 처리.
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)를 기반으로 한 페이지네이션 뷰도 포함하고 있습니다. 기본적으로 Tailwind 뷰를 사용하지 않고 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 부트스트랩 처리.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음 메서드를 통해 페이지네이션 관련 추가 정보를 제공합니다:

<div class="overflow-auto">

| 메서드 | 설명 |
| --- | --- |
| `$paginator->count()` | 현재 페이지에 포함된 항목 수를 반환합니다. |
| `$paginator->currentPage()` | 현재 페이지 번호를 반환합니다. |
| `$paginator->firstItem()` | 결과 중 첫 번째 항목의 번호를 반환합니다. |
| `$paginator->getOptions()` | 페이지네이터 설정 옵션을 반환합니다. |
| `$paginator->getUrlRange($start, $end)` | 지정한 범위의 페이지 링크 URL을 생성합니다. |
| `$paginator->hasPages()` | 여러 페이지로 나눌만큼 충분한 항목이 있는지 판단합니다. |
| `$paginator->hasMorePages()` | 더 많은 데이터가 존재하는지 판단합니다. |
| `$paginator->items()` | 현재 페이지 항목들을 반환합니다. |
| `$paginator->lastItem()` | 결과 중 마지막 항목의 번호를 반환합니다. |
| `$paginator->lastPage()` | 마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시 없음) |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL을 반환합니다. |
| `$paginator->onFirstPage()` | 현재 페이지가 첫 페이지인지 판단합니다. |
| `$paginator->perPage()` | 페이지당 표시할 항목 수를 반환합니다. |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 반환합니다. |
| `$paginator->total()` | 전체 일치하는 항목 수를 반환합니다. (`simplePaginate` 사용 시 없음) |
| `$paginator->url($page)` | 지정한 페이지 번호의 URL을 반환합니다. |
| `$paginator->getPageName()` | 페이지 번호를 저장하는 쿼리 문자열 변수명을 반환합니다. |
| `$paginator->setPageName($name)` | 페이지 번호를 저장하는 쿼리 문자열 변수명을 설정합니다. |
| `$paginator->through($callback)` | 콜백을 통해 각 항목을 변환합니다. |

</div>

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

커서 페이지네이터 인스턴스는 다음 메서드를 통해 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                       |
| ------------------------------- | ---------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지에 포함된 항목 수를 반환합니다.                 |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 반환합니다.                           |
| `$paginator->getOptions()`      | 페이지네이터 설정 옵션을 반환합니다.                        |
| `$paginator->hasPages()`        | 여러 페이지로 나눌만큼 충분한 항목이 있는지 판단합니다.     |
| `$paginator->hasMorePages()`    | 더 많은 데이터가 존재하는지 판단합니다.                    |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리 문자열 변수명을 반환합니다.           |
| `$paginator->items()`           | 현재 페이지 항목들을 반환합니다.                           |
| `$paginator->nextCursor()`      | 다음 데이터 세트의 커서 인스턴스를 반환합니다.             |
| `$paginator->nextPageUrl()`     | 다음 페이지의 URL을 반환합니다.                            |
| `$paginator->onFirstPage()`     | 현재 페이지가 첫 페이지인지 판단합니다.                    |
| `$paginator->onLastPage()`      | 현재 페이지가 마지막 페이지인지 판단합니다.                |
| `$paginator->perPage()`         | 페이지당 표시할 항목 수를 반환합니다.                       |
| `$paginator->previousCursor()`  | 이전 데이터 세트의 커서 인스턴스를 반환합니다.             |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 반환합니다.                            |
| `$paginator->setCursorName()`   | 커서를 저장하는 쿼리 문자열 변수명을 설정합니다.           |
| `$paginator->url($cursor)`      | 지정한 커서 인스턴스에 대한 URL을 반환합니다.              |

</div>