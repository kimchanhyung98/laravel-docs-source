# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이징](#paginating-query-builder-results)
    - [Eloquent 결과 페이징](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 페이저 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 맞춤화](#customizing-pagination-urls)
- [페이지네이션 결과 출력](#displaying-pagination-results)
    - [페이지네이션 링크 창 조절](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 맞춤화](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 방식이 신선한 변화가 되길 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent)에 통합되어 있으며, 기본 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이징할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환되지만, Bootstrap 페이지네이션도 지원합니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용한다면, 애플리케이션의 `tailwind.config.js` 파일 내 `content` 키에 Laravel 페이지네이션 뷰가 포함되도록 해야 Tailwind 클래스가 삭제되지 않습니다:

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
### 쿼리 빌더 결과 페이징 (Paginating Query Builder Results)

항목을 페이징하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 현재 사용자가 보고 있는 페이지를 기준으로 쿼리의 "limit"와 "offset"을 자동으로 설정해 줍니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 인수 값으로 감지됩니다. 이 값은 Laravel에서 자동으로 인식되며, 페이지네이터가 생성하는 링크에도 자동으로 포함됩니다.

아래 예시에서는 `paginate` 메서드에 전달하는 유일한 인수는 "페이지 당 표시할 항목 수"입니다. 예시에서는 페이지당 `15`개의 항목을 표시하려고 합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자 보여주기.
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

`paginate` 메서드는 먼저 쿼리와 일치하는 총 레코드 수를 계산한 후 데이터를 조회합니다. 이는 페이지네이터가 전체 페이지 수를 알 수 있도록 하기 위함입니다. 그러나 UI에서 총 페이지 수를 표시할 필요가 없다면, 레코드 수 계산 쿼리는 불필요합니다.

따라서, UI에서 단순히 "이전"과 "다음" 링크만 표시하려는 경우에는 `simplePaginate` 메서드를 사용하여 더 효율적인 단일 쿼리를 수행할 수 있습니다:

```
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이징 (Paginating Eloquent Results)

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이징할 수 있습니다. 아래 예시는 `App\Models\User` 모델을 페이징하여 페이지당 15개의 레코드를 표시하는 경우입니다. 쿼리 빌더 결과를 페이징하는 문법과 거의 동일합니다:

```
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 조건 같은 추가 조건 후에 `paginate` 메서드를 호출할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이징할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

```
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

또한 `cursorPaginate` 메서드로 Eloquent 모델을 커서 페이지네이션할 수도 있습니다:

```
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용하기

애플리케이션 화면에 두 개 이상의 서로 다른 페이지네이터를 표시해야 하는 경우가 있습니다. 하지만 두 페이지네이터가 모두 `page` 쿼리 문자열 인수를 사용하면, 현재 페이지 정보가 충돌할 수 있습니다. 이 문제를 해결하려면 `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수로 쿼리 문자열 인수명을 직접 지정하세요:

```
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate`는 SQL의 "offset" 절을 사용해 쿼리를 생성하는 반면, 커서 페이지네이션은 쿼리의 정렬된 컬럼 값을 비교하는 "where" 절을 구성하여 작동합니다. 따라서 Laravel의 모든 페이지네이션 방법 중에서 가장 효율적인 데이터베이스 성능을 제공합니다. 이 방식은 특히 대용량 데이터셋이나 "무한 스크롤" UI에 적합합니다.

오프셋 기반 페이지네이션은 URL에 페이지 번호를 쿼리 문자열로 포함하지만, 커서 기반 페이지네이션은 "커서(cursor)" 문자열을 쿼리 문자열에 넣습니다. 커서는 다음 페이지네이션 쿼리가 시작될 위치와 방향을 포함한 인코딩된 문자열입니다:

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 기반 페이지네이터 인스턴스는 쿼리 빌더의 `cursorPaginate` 메서드로 생성할 수 있으며, 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 얻은 후에는 보통 `paginate`와 `simplePaginate`를 사용할 때처럼 [페이지네이션 결과를 출력](#displaying-pagination-results)하면 됩니다. 인스턴스 메서드에 관한 자세한 내용은 [커서 페이지네이터 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!NOTE]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션 비교

커서 페이지네이션과 오프셋 페이지네이션의 차이를 예시 SQL 쿼리로 살펴보겠습니다. 다음 두 쿼리는 모두 `users` 테이블을 `id`로 정렬한 후 "두 번째 페이지" 결과를 가져옵니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 페이지네이션 대비 다음과 같은 장점이 있습니다:

- 대용량 데이터셋의 경우, "order by" 컬럼이 인덱싱 되어 있다면 커서 페이지네이션이 더 나은 성능을 제공합니다. 오프셋 절은 이전에 일치한 모든 데이터를 스캔하기 때문입니다.
- 자주 쓰기가 일어나는 데이터셋에서, 오프셋 페이지네이션은 최근에 데이터가 추가되거나 삭제된 경우 레코드를 건너뛰거나 중복 표시할 수 있습니다.

하지만 커서 페이지네이션은 다음과 같은 제한점도 있습니다:

- `simplePaginate`처럼, 커서 페이지네이션은 "다음"과 "이전" 링크만 생성하며 페이지 번호가 있는 링크는 만들지 않습니다.
- 최소 한 개 이상의 고유한 컬럼이나 고유 조합 컬럼에 기반한 정렬이어야 하며, `null` 값을 가진 컬럼은 지원하지 않습니다.
- "order by" 절의 쿼리 표현식은 별칭이 부여되어 `select` 절에도 포함된 경우에만 지원됩니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이저 생성하기 (Manually Creating A Paginator)

때로는 이미 메모리 상에 가지고 있는 배열을 사용해 페이지네이션 인스턴스를 직접 만들고 싶을 수 있습니다. 이 경우 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스를 생성하면 됩니다.

`Paginator`와 `CursorPaginator`는 결과 집합의 전체 항목 수를 알 필요가 없지만, 그 때문에 마지막 페이지 인덱스를 가져오는 메서드는 제공하지 않습니다. 반면 `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수를 받지만, 전체 항목 수를 반드시 전달해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`에 대응하며, `CursorPaginator`는 `cursorPaginate`에 대응, `LengthAwarePaginator`는 `paginate`에 대응합니다.

> [!NOTE]
> 페이저 인스턴스를 수동으로 만들 때는, 전달할 결과 배열을 직접 "슬라이스(slice)"해야 합니다. 슬라이스 방법이 궁금하면 PHP 함수 [array_slice](https://secure.php.net/manual/en/function.array-slice.php)를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 맞춤화 (Customizing Pagination URLs)

기본적으로 페이지네이터가 생성하는 링크는 현재 요청 URI와 일치합니다. 하지만 `withPath` 메서드를 통해 페이지네이터가 링크를 생성할 때 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, 페이저 링크를 `http://example.com/admin/users?page=N` 형태로 만들고 싶다면 `/admin/users`를 `withPath`에 전달하세요:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    //
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 덧붙이기 (Appending Query String Values)

`appends` 메서드를 사용하면 페이지네이션 링크의 쿼리 문자열에 값을 추가할 수 있습니다. 예를 들어 모든 페이지네이션 링크에 `sort=votes`를 덧붙이려면 다음과 같이 호출합니다:

```
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    //
});
```

현재 요청의 쿼리 문자열 전체를 페이지네이션 링크에 덧붙이고 싶으면 `withQueryString` 메서드를 사용하면 됩니다:

```
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시(fragment) 조각 덧붙이기 (Appending Hash Fragments)

페이지네이션 링크 URL 끝에 해시(fragment)를 붙이고 싶다면 `fragment` 메서드를 사용하세요. 예를 들어 각 페이지네이션 링크에 `#users`를 덧붙이려면 다음처럼 호출합니다:

```
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 출력 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 받게 되며, `simplePaginate`는 `Illuminate\Pagination\Paginator`, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 인스턴스들은 결과 집합에 관한 여러 메서드를 제공합니다. 그리고 페이지네이터 인스턴스는 반복자(iterable)이므로 배열처럼 순회할 수 있습니다. 따라서 결과를 받은 후엔 [Blade](/docs/{{version}}/blade)를 이용해 결과와 페이지 링크를 출력할 수 있습니다:

```html
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지 링크를 렌더링합니다. 이 링크들은 이미 적절한 `page` 쿼리 문자열 변수를 포함하고 있습니다. 생성된 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 창 조절 (Adjusting The Pagination Link Window)

페이지네이터가 페이지 링크를 출력할 때, 기본적으로 현재 페이지 번호와 전후 세 페이지의 링크를 보여줍니다. `onEachSide` 메서드를 사용하면 중간에 생성되는 페이지 링크에서 현재 페이지 양쪽에 표시할 링크 수를 조절할 수 있습니다:

```
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환 (Converting Results To JSON)

Laravel 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공합니다. 따라서 페이지네이션 결과를 JSON으로 쉽게 변환할 수 있습니다. 또한 라우트 또는 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

```
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page`와 같은 메타 정보가 포함되며, 결과 레코드는 JSON 배열의 `data` 키에 있습니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환해 생성된 JSON 예시입니다:

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
## 페이지네이션 뷰 맞춤화 (Customizing The Pagination View)

기본적으로 페이지네이션 링크를 출력하는 뷰는 [Tailwind CSS](https://tailwindcss.com)와 호환됩니다. Tailwind를 사용하지 않는다면, 직접 링크를 렌더링할 뷰를 자유롭게 정의할 수 있습니다. 페이지네이터 인스턴스에서 `links` 메서드를 호출할 때 첫 번째 인수로 뷰 이름을 전달하면 해당 뷰를 사용합니다:

```
{{ $paginator->links('view.name') }}

// 뷰에 추가 데이터를 전달할 수도 있습니다...
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이지네이션 뷰를 맞춤화하는 가장 쉬운 방법은 `vendor:publish` 명령어로 뷰를 `resources/views/vendor` 디렉토리로 내보내는 것입니다:

```
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어로 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰들이 복사됩니다. 이 디렉토리 내 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당하며, 이 파일을 편집해 HTML을 수정할 수 있습니다.

기본 페이지네이션 뷰를 다른 파일로 지정하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하세요:

```
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 작성된 페이지네이션 뷰도 포함합니다. 기본 Tailwind 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrap` 메서드를 호출하세요:

```
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Paginator::useBootstrap();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드 (Paginator / LengthAwarePaginator Instance Methods)

각 페이지네이터 인스턴스는 다음 메서드를 통해 페이지네이션 정보에 접근할 수 있습니다:

Method  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 개수 가져오기
`$paginator->currentPage()`  |  현재 페이지 번호 가져오기
`$paginator->firstItem()`  |  결과 중 첫 번째 항목의 인덱스 가져오기
`$paginator->getOptions()`  |  페이지네이터 옵션 가져오기
`$paginator->getUrlRange($start, $end)`  |  지정 범위의 페이지 URL 생성
`$paginator->hasPages()`  |  페이지가 여러個로 나뉘어질 만큼 항목이 충분한지 확인
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인
`$paginator->items()`  |  현재 페이지의 항목들 가져오기
`$paginator->lastItem()`  |  결과 중 마지막 항목의 인덱스 가져오기
`$paginator->lastPage()`  |  마지막 페이지 번호 가져오기 (`simplePaginate` 사용 시 미지원)
`$paginator->nextPageUrl()`  |  다음 페이지 URL 가져오기
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 판단
`$paginator->perPage()`  |  페이지 당 표시할 항목 수
`$paginator->previousPageUrl()`  |  이전 페이지 URL 가져오기
`$paginator->total()`  |  데이터 저장소 내 모든 일치 항목 총 개수 (`simplePaginate` 사용 시 미지원)
`$paginator->url($page)`  |  지정한 페이지 번호의 URL 가져오기
`$paginator->getPageName()`  |  쿼리 문자열에서 페이지 번호 저장에 쓰이는 변수명 가져오기
`$paginator->setPageName($name)`  |  쿼리 문자열 변수명 직접 설정

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드 (Cursor Paginator Instance Methods)

커서 페이지네이터 인스턴스는 다음 메서드를 통해 페이지네이션 정보에 접근할 수 있습니다:

Method  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 개수 가져오기
`$paginator->cursor()`  |  현재 커서 인스턴스 가져오기
`$paginator->getOptions()`  |  페이지네이터 옵션 가져오기
`$paginator->hasPages()`  |  페이지가 여러個로 나뉘어질 만큼 항목이 충분한지 확인
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인
`$paginator->getCursorName()`  |  쿼리 문자열에서 커서 정보를 저장하는 변수명 가져오기
`$paginator->items()`  |  현재 페이지의 항목들 가져오기
`$paginator->nextCursor()`  |  다음 항목 집합을 가리키는 커서 인스턴스 가져오기
`$paginator->nextPageUrl()`  |  다음 페이지 URL 가져오기
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 판단
`$paginator->perPage()`  |  페이지 당 표시할 항목 수
`$paginator->previousCursor()`  |  이전 항목 집합을 가리키는 커서 인스턴스 가져오기
`$paginator->previousPageUrl()`  |  이전 페이지 URL 가져오기
`$paginator->setCursorName()`  |  쿼리 문자열에서 커서 정보를 저장하는 변수명을 직접 설정
`$paginator->url($cursor)`  |  지정한 커서 인스턴스에 해당하는 URL 가져오기