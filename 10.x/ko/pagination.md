# 데이터베이스: 페이징 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이징](#paginating-query-builder-results)
    - [Eloquent 결과 페이징](#paginating-eloquent-results)
    - [커서 페이징(Cursor Pagination)](#cursor-pagination)
    - [수동으로 페이저 인스턴스 생성하기](#manually-creating-a-paginator)
    - [페이징 URL 커스터마이징](#customizing-pagination-urls)
- [페이징 결과 표시](#displaying-pagination-results)
    - [페이지 링크 범위 조정하기](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이징 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이징 구현이 매우 번거로울 수 있습니다. Laravel의 페이징 방식은 새로운 활력소가 되길 바랍니다. Laravel의 페이저는 [쿼리 빌더](/docs/10.x/queries)와 [Eloquent ORM](/docs/10.x/eloquent)과 통합되어 있어, 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이징할 수 있습니다.

기본적으로 페이저가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환되지만, Bootstrap 페이징 지원도 제공합니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이징 뷰와 Tailwind JIT 엔진을 사용 중이라면, 애플리케이션의 `tailwind.config.js` 파일 내 `content` 키에 Laravel의 페이징 뷰 경로가 포함되어 있어야 해당 Tailwind 클래스가 정리(purge)되지 않습니다:

```js
content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
    './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
],
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이징

항목을 페이징하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/10.x/queries) 또는 [Eloquent 쿼리](/docs/10.x/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지를 기준으로 쿼리의 "limit"과 "offset" 설정을 자동으로 처리합니다. 기본적으로 현재 페이지는 HTTP 요청에서 `page` 쿼리 문자열 인수의 값으로 감지됩니다. 이 값은 Laravel이 자동으로 찾아내며, 페이저가 생성하는 링크에도 자동으로 포함됩니다.

다음 예제에서는 `paginate` 메서드에 인수로 "페이지 당 표시할 항목 수"만 전달합니다. 여기서는 페이지당 `15`개의 항목을 표시하도록 지정했습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 보여줍니다.
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
#### 심플 페이징(Simple Pagination)

`paginate` 메서드는 쿼리에 매칭되는 전체 레코드 수를 먼저 계산한 후, 데이터베이스에서 실제 레코드를 조회합니다. 이는 페이저가 총 몇 페이지가 있는지 알기 위해서입니다. 그러나 UI에서 총 페이지 수를 보여줄 필요가 없을 경우, 전체 레코드 수를 조회하는 쿼리는 불필요합니다.

따라서, 애플리케이션 UI에 단순히 "다음(Next)" 및 "이전(Previous)" 링크만 표시하려면 `simplePaginate` 메서드를 사용해 더 효율적인 단일 쿼리를 수행할 수 있습니다:

```
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이징

[Eloquent](/docs/10.x/eloquent) 쿼리도 페이징할 수 있습니다. 다음 예제에서는 `App\Models\User` 모델을 페이징하며, 페이지 당 15개 레코드를 표시하도록 합니다. 쿼리 빌더와 거의 동일한 문법임을 볼 수 있습니다:

```
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 절과 같은 추가 조건을 설정한 후에 `paginate` 메서드를 호출할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 `simplePaginate` 메서드로 페이징할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

유사하게, `cursorPaginate` 메서드를 사용해 Eloquent 모델을 커서 페이징할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이저 인스턴스 사용하기

어떤 경우에는 한 페이지 내에 애플리케이션이 여러 개의 별도 페이저를 렌더링해야 할 때가 있습니다. 그런데 두 페이저 인스턴스 모두 현재 페이지를 저장하는 쿼리 문자열 파라미터로 `page`를 사용할 경우 충돌이 발생합니다. 이 문제를 해결하려면, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수로 페이지 번호를 저장할 쿼리 문자열 파라미터 이름을 지정할 수 있습니다:

```
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이징(Cursor Pagination)

`paginate`, `simplePaginate`는 SQL의 "offset" 절을 사용해 쿼리를 생성하지만, 커서 페이징은 쿼리 내 정렬에 사용된 컬럼들의 값을 비교하는 "where" 절을 만들어 실행합니다. 이 방식은 Laravel의 페이징 방법 중 가장 효율적인 데이터베이스 성능을 제공합니다. 대용량 데이터셋과 무한 스크롤 UI에 특히 적합합니다.

오프셋 기반 페이징과 달리, 커서 페이징은 페이저가 생성하는 URL 쿼리 문자열에 페이지 번호 대신 "커서(cursor)" 문자열을 포함합니다. 커서는 다음 페이지 쿼리를 시작할 위치와 페이징 방향 정보를 담은 인코딩된 문자열입니다:

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 기반 페이저 인스턴스는 쿼리 빌더의 `cursorPaginate` 메서드로 생성할 수 있으며, 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이져 인스턴스를 얻으면, `paginate` 및 `simplePaginate`와 마찬가지로 [페이징 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이저 인스턴스가 지원하는 메서드에 대해서는 [커서 페이저 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]  
> 커서 페이징을 활용하려면 쿼리에 반드시 `order by` 절이 포함되어야 하며, 정렬에 사용되는 컬럼들은 페이징하는 테이블에 속해 있어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이징과 오프셋 페이징 비교

오프셋 페이징과 커서 페이징의 차이를 SQL 쿼리 예시로 살펴보겠습니다. 두 쿼리 모두 `users` 테이블에서 `id` 순으로 정렬된 결과 중 "두 번째 페이지"를 보여줍니다:

```sql
# 오프셋 페이징...
select * from users order by id asc limit 15 offset 15;

# 커서 페이징...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이징은 오프셋 페이징 대비 다음과 같은 장점이 있습니다:

- 대용량 데이터셋에서, 정렬 컬럼에 인덱스가 있으면 더 빠른 성능을 제공합니다. 이는 "offset" 절이 이전에 매칭된 모든 데이터를 스캔해야 하는 것과 다릅니다.
- 자주 쓰기 작업이 발생하는 데이터셋에서, 오프셋 페이징은 최근 추가되거나 삭제된 레코드 때문에 레코드가 누락되거나 중복 표시될 수 있습니다.

하지만 커서 페이징에는 다음과 같은 제한 사항도 있습니다:

- `simplePaginate`와 마찬가지로 커서 페이징은 "다음" 및 "이전" 링크만 지원하며 숫자 페이지 링크는 지원하지 않습니다.
- 최소 하나의 고유 컬럼 또는 고유 조합 컬럼을 기준으로 정렬해야 하며, `null` 값이 포함된 컬럼은 지원하지 않습니다.
- `order by` 절에 사용된 쿼리 표현식은 별칭(alias)이 있고 `select` 절에도 포함되어야 지원됩니다.
- 파라미터가 포함된 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이저 인스턴스 생성하기

이미 메모리에 가지고 있는 항목 배열을 수동으로 페이징 인스턴스로 만들고 싶을 때가 있습니다. 이 경우 요구사항에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나를 직접 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 전체 항목 개수를 알 필요가 없습니다. 때문에 이 클래스들은 마지막 페이지 인덱스 조회 메서드를 제공하지 않습니다. 반면 `LengthAwarePaginator`는 `Paginator`와 거의 같은 인수를 받지만, 전체 항목 수를 반드시 전달해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`에, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate`에 대응합니다.

> [!WARNING]  
> 수동으로 페이저 인스턴스를 만들 때는, 페이저에 넘기는 배열을 직접 원하는 페이징 범위로 "slice" 해야 합니다. 방법을 모른다면 PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이징 URL 커스터마이징

기본적으로 페이저가 생성하는 링크는 현재 요청 URI와 일치합니다. 그러나 페이저의 `withPath` 메서드를 사용하면 링크 생성 시 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, 페이저가 `http://example.com/admin/users?page=N` 형태의 링크를 생성하도록 하려면, `withPath` 메서드에 `/admin/users`를 전달하면 됩니다:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가하기

페이징 링크에 추가 쿼리 문자열을 붙이고 싶으면 `appends` 메서드를 사용하세요. 예를 들어, 각각의 페이징 링크 뒤에 `sort=votes`를 추가하려면 아래처럼 호출합니다:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리 문자열 값을 페이징 링크에 덧붙이고 싶으면 `withQueryString` 메서드를 사용하세요:

```
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트(fragment) 추가하기

페이징 링크 URL 뒤에 "해시 조각(해시 fragment)"을 추가해야 할 경우, `fragment` 메서드를 사용하면 됩니다. 예를 들어, 모든 페이징 링크에 `#users`를 덧붙이려면 아래처럼 호출하세요:

```
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이징 결과 표시

`paginate` 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합과 관련된 여러 정보를 제공하는 메서드를 갖고 있습니다. 또한 페이저 인스턴스는 반복자(iterator)이기도 하여, 배열처럼 `foreach` 문으로 순회할 수 있습니다. 따라서 결과를 조회한 후에는, [Blade](/docs/10.x/blade)를 사용해 다음과 같이 결과와 페이지 링크를 표시할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지들에 대한 링크를 렌더링합니다. 각 링크에는 이미 적절한 `page` 쿼리 문자열 변수가 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/) 호환형임을 기억하세요.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지 링크 범위 조정하기

기본적으로 페이저가 페이지 링크를 표시할 때, 현재 페이지 번호와 함께 현재 페이지 앞뒤 3개의 페이지 링크를 표시합니다. `onEachSide` 메서드를 사용하면, 현재 페이지 중간 영역 주변의 추가 링크 개수를 조절할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

위 예시는 앞뒤 각 5개씩 더 많은 페이지 링크를 보여줍니다.

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

Laravel 페이저 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공합니다. 따라서 페이징 결과를 JSON으로 변환하는 것이 매우 쉽습니다. 또한 라우트 또는 컨트롤러 액션에서 페이저 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

```
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이저에서 생성되는 JSON은 `total`, `current_page`, `last_page` 등 메타 정보를 포함합니다. 데이터 레코드는 JSON 배열의 `data` 키로 제공됩니다. 다음은 라우트에서 페이저 인스턴스를 반환할 때 생성되는 JSON 예시입니다:

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
## 페이징 뷰 커스터마이징

기본적으로 페이징 링크를 표시할 때 렌더링되는 뷰는 [Tailwind CSS](https://tailwindcss.com)와 호환됩니다. 그러나 Tailwind를 사용하지 않는다면, 자유롭게 링크를 렌더링할 뷰를 직접 정의할 수 있습니다. 페이저 인스턴스의 `links` 메서드 호출 시 뷰 이름을 첫 인수로 넘기면 해당 뷰가 사용됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터를 전달할 수도 있습니다... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이징 뷰를 커스터마이징하는 가장 쉬운 방법은, `vendor:publish` 명령어로 뷰들을 `resources/views/vendor` 디렉토리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰가 복사됩니다. 이 디렉토리 내 `tailwind.blade.php` 파일이 기본 페이징 뷰에 해당하며, 이 파일을 수정하여 페이징 HTML을 변경할 수 있습니다.

기본 페이징 뷰 파일을 다른 파일로 지정하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이저의 `defaultView`와 `defaultSimpleView` 메서드를 호출하세요:

```
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스들을 부트스트랩합니다.
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)를 사용해 구축한 페이징 뷰도 기본으로 제공합니다. Tailwind 기본 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이저의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스들을 부트스트랩합니다.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이저 인스턴스는 다음 메서드를 통해 페이징 결과에 대한 다양한 정보를 제공합니다:

Method  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 수를 반환합니다.
`$paginator->currentPage()`  |  현재 페이지 번호를 반환합니다.
`$paginator->firstItem()`  |  결과에서 첫 번째 항목의 인덱스를 반환합니다.
`$paginator->getOptions()`  |  페이저 옵션들을 반환합니다.
`$paginator->getUrlRange($start, $end)`  |  지정한 범위의 페이지 URL을 생성합니다.
`$paginator->hasPages()`  |  여러 페이지로 분할할 만큼 항목이 있는지 확인합니다.
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인합니다.
`$paginator->items()`  |  현재 페이지의 항목들을 반환합니다.
`$paginator->lastItem()`  |  결과 중 마지막 항목의 인덱스를 반환합니다.
`$paginator->lastPage()`  |  마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시에는 제공되지 않음)
`$paginator->nextPageUrl()`  |  다음 페이지 URL을 반환합니다.
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 확인합니다.
`$paginator->perPage()`  |  페이지 당 표시할 항목 수를 반환합니다.
`$paginator->previousPageUrl()`  |  이전 페이지 URL을 반환합니다.
`$paginator->total()`  |  전체 항목 수를 반환합니다. (`simplePaginate` 사용 시에는 제공되지 않음)
`$paginator->url($page)`  |  지정한 페이지 번호의 URL을 반환합니다.
`$paginator->getPageName()`  |  페이지 번호를 저장하는 쿼리 문자열 변수명을 반환합니다.
`$paginator->setPageName($name)`  |  페이지 번호를 저장하는 쿼리 문자열 변수명을 설정합니다.
`$paginator->through($callback)`  |  콜백 함수로 각 항목을 변환합니다.

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

각 커서 페이저 인스턴스는 다음 메서드를 통해 페이징 결과에 관한 추가 정보를 제공합니다:

Method  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 수를 반환합니다.
`$paginator->cursor()`  |  현재 커서 인스턴스를 반환합니다.
`$paginator->getOptions()`  |  페이저 옵션들을 반환합니다.
`$paginator->hasPages()`  |  여러 페이지로 분할할 만큼 항목이 있는지 확인합니다.
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인합니다.
`$paginator->getCursorName()`  |  커서를 저장하는 쿼리 문자열 변수명을 반환합니다.
`$paginator->items()`  |  현재 페이지의 항목들을 반환합니다.
`$paginator->nextCursor()`  |  다음 항목 집합에 대한 커서 인스턴스를 반환합니다.
`$paginator->nextPageUrl()`  |  다음 페이지 URL을 반환합니다.
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 확인합니다.
`$paginator->onLastPage()`  |  현재 페이지가 마지막 페이지인지 확인합니다.
`$paginator->perPage()`  |  페이지 당 표시할 항목 수를 반환합니다.
`$paginator->previousCursor()`  |  이전 항목 집합에 대한 커서 인스턴스를 반환합니다.
`$paginator->previousPageUrl()`  |  이전 페이지 URL을 반환합니다.
`$paginator->setCursorName()`  |  커서를 저장하는 쿼리 문자열 변수명을 설정합니다.
`$paginator->url($cursor)`  |  지정한 커서 인스턴스의 URL을 반환합니다.