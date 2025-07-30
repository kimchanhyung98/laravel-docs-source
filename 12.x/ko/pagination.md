# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 페이지네이터 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 표시하기](#displaying-pagination-results)
    - [페이지네이션 링크 표시 범위 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션 구현이 꽤 번거로울 수 있습니다. Laravel의 페이지네이션 시스템은 이를 깔끔하게 해결해주리라 기대합니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/12.x/queries) 및 [Eloquent ORM](/docs/12.x/eloquent)과 통합되어 있으며, 별도의 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이지네이션할 수 있게 해줍니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환되도록 되어 있습니다. 하지만 Bootstrap용 페이지네이션도 지원됩니다.

<a name="tailwind"></a>
#### Tailwind

Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용한다면, `resources/css/app.css` 파일에 다음과 같이 `@source` 지시문이 이미 적절히 설정되어 있습니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

아이템을 페이지네이션하는 여러 방법이 있지만, 가장 간단한 방법은 [쿼리 빌더](/docs/12.x/queries)나 [Eloquent 쿼리](/docs/12.x/eloquent)의 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 현재 사용자가 보고 있는 페이지에 따라 자동으로 쿼리의 `limit`과 `offset`을 설정해 줍니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 인수 값으로 감지되며, Laravel이 이를 자동으로 인식하고 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

다음 예시에서는 `paginate` 메서드에 전달되는 인수는 단 하나, 페이지당 표시할 아이템 수입니다. 여기에서는 페이지당 15개씩 항목을 표시하도록 지정했습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자를 표시합니다.
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

`paginate` 메서드는 쿼리 수행 전에 총 레코드 수를 세어, 페이지네이터가 총 몇 페이지가 필요한지 알 수 있게 해줍니다. 하지만 애플리케이션 UI에서 총 페이지 수를 보여주지 않을 계획이라면, 이 총 레코드 수를 세는 쿼리는 불필요합니다.

따라서 UI에 단순히 "다음", "이전" 링크만 표시한다면, 더 효율적인 쿼리를 수행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

Eloquent 쿼리도 페이지네이션할 수 있습니다. 다음 예시에서는 `App\Models\User` 모델을 페이지네이션하며, 페이지당 15개 레코드를 표시한다고 명시합니다. 구문은 쿼리 빌더 결과를 페이지네이션할 때와 거의 동일합니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

당연히, `where` 조건 등을 적용한 후에도 `paginate` 메서드를 호출할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델 페이지네이션 시에도 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

또한 `cursorPaginate` 메서드를 사용해 커서 페이지네이션도 가능합니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 화면에 여러 페이지네이터 인스턴스 사용하기

애플리케이션 한 페이지 안에서 두 개 이상의 페이지네이터를 동시에 렌더링해야 할 때가 있습니다. 기본 설정에서는 두 페이지네이터 모두 현재 페이지 저장에 같은 `page` 쿼리 문자열 파라미터를 사용하므로 충돌이 발생할 수 있습니다. 이 문제는 `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인자로 페이지네이터가 현재 페이지를 저장할 쿼리 문자열 파라미터 이름을 전달하면 해결할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션 (Cursor Pagination)

`paginate`와 `simplePaginate` 메서드는 SQL의 `offset` 절을 사용해 쿼리를 생성하는 반면, 커서 페이지네이션은 쿼리 내 정렬된 컬럼 값들을 비교하는 `where` 절을 만들어 처리합니다. 이 방식은 Laravel의 모든 페이지네이션 방법 중에서 가장 효율적인 데이터베이스 성능을 제공합니다. 특히 대용량 데이터셋이나 무한 스크롤 UI에 적합합니다.

기존의 오프셋 페이지네이션은 페이지 번호를 쿼리 문자열에 포함하지만, 커서 페이지네이션은 위치와 방향 정보를 포함하는 인코딩된 "커서" 문자열을 쿼리 문자열에 넣습니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

커서 페이지네이터는 쿼리 빌더의 `cursorPaginate` 메서드를 통해 생성할 수 있으며, 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 가져왔다면, 일반적인 `paginate`나 `simplePaginate` 메서드처럼 결과를 표시할 수 있습니다. 커서 페이지네이터의 추가 메서드는 [커서 페이지네이터 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 `order by` 절이 포함되어야 하며, 정렬 대상 컬럼들은 페이지네이션 대상 테이블의 컬럼이어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션 비교

다음 두 SQL 쿼리는 모두 `id` 컬럼으로 정렬된 `users` 테이블에서 두 번째 페이지 결과를 가져옵니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션이 오프셋 페이지네이션보다 갖는 장점은 다음과 같습니다:

- 대용량 데이터셋에서 `order by` 컬럼에 인덱스가 있다면 더 나은 성능을 제공합니다. 오프셋 조건은 앞서 매칭된 모든 데이터를 스캔하기 때문입니다.
- 자주 쓰기 작업이 발생하는 데이터셋에서, 오프셋 페이지네이션은 최근에 새로운 결과가 추가되거나 삭제된 경우 레코드가 누락되거나 중복 개체가 나타날 수 있습니다.

커서 페이지네이션의 제한 사항은 다음과 같습니다:

- `simplePaginate`처럼 오직 "다음"과 "이전" 링크만 지원하며, 페이지 번호 링크 생성 기능은 없습니다.
- 적어도 하나 이상의 고유 컬럼 또는 고유한 컬럼 조합을 기반으로 정렬해야 합니다. `null` 값을 포함하는 컬럼은 지원되지 않습니다.
- `order by` 절 내에 쿼리 표현식이 포함된 경우, 별칭을 가지고 `select` 절에 명시적으로 추가돼야 지원됩니다.
- 파라미터가 포함된 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이지네이터 생성하기

이미 메모리에 가지고 있는 아이템 배열을 사용해 수동으로 페이지네이션 인스턴스를 생성할 때가 있습니다. 이 경우 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 필요에 따라 적절한 클래스를 생성하면 됩니다.

`Paginator`와 `CursorPaginator` 클래스를 생성할 때는 전체 아이템 수를 알 필요가 없으며, 이 때문에 마지막 페이지 인덱스를 조회하는 메서드가 없습니다. 반면 `LengthAwarePaginator`는 전체 아이템 수를 인수로 받으며, 거의 같은 매개변수를 입력받습니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate` 메서드와, `CursorPaginator`는 `cursorPaginate` 메서드와, `LengthAwarePaginator`는 `paginate` 메서드와 대응됩니다.

> [!WARNING]
> 수동으로 페이지네이터를 만들 때는, 배열에서 전달할 데이터만 직접 잘라내어(slice) 주어야 합니다. 방법이 헷갈린다면 PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수 문서를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 하지만 `withPath` 메서드를 사용하면 페이지네이터 링크를 생성할 때 사용하는 URI를 직접 지정할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 형태의 링크를 생성하도록 하려면 `withPath` 메서드에 `/admin/users`를 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가하기

`appends` 메서드를 사용하면 페이지네이션 링크에 쿼리 문자열 값을 덧붙일 수 있습니다. 예를 들어, 모든 페이지네이션 링크에 `sort=votes`를 추가하고 싶다면 다음과 같이 호출하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리 문자열 값을 페이지네이션 링크에 붙이고 싶다면 `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기

페이지네이터가 생성한 URL 끝에 해시(fragment)를 덧붙여야 한다면 `fragment` 메서드를 사용하세요. 예를 들어, 페이지네이션 링크 끝에 `#users`를 붙이고 싶으면 다음과 같이 작성합니다:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시하기

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스가 반환되고, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 대한 여러 메서드를 제공합니다. 또한 페이지네이터는 이터레이터이므로 배열처럼 반복할 수 있습니다. 결과를 가져왔으면 [Blade](/docs/12.x/blade)를 사용해 다음과 같이 결과를 출력하고 페이지 링크를 렌더링할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지로 이동하는 링크를 렌더링합니다. 이 링크들은 이미 적절한 `page` 쿼리 문자열 변수를 포함하고 있습니다. 생성되는 HTML은 기본적으로 [Tailwind CSS](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 표시 범위 조정

페이지네이터가 링크를 표시할 때, 현재 페이지 번호와 함께 현재 페이지 앞뒤 3페이지 링크를 기본으로 보여줍니다. `onEachSide` 메서드를 사용하면 현재 페이지 기준으로 좌우 몇 개의 추가 링크를 표시할지 조절할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

Laravel의 페이지네이터 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며, `toJson` 메서드를 제공합니다. 따라서 페이지네이션 결과를 JSON으로 쉽게 변환할 수 있습니다. 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 포함되며, 결과 레코드는 JSON 배열 내 `data` 키 아래에 있습니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환했을 때 생성되는 JSON 예제입니다:

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
## 페이지네이션 뷰 커스터마이징

기본적으로 페이지네이션 링크를 표시하는 뷰는 [Tailwind CSS](https://tailwindcss.com)와 호환됩니다. 하지만 Tailwind를 사용하지 않는 경우 직접 뷰를 정의할 수도 있습니다. 페이지네이터 인스턴스의 `links` 메서드를 호출할 때, 첫 번째 인수로 뷰 이름을 전달하면 해당 뷰가 사용됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터를 전달하려면... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 간편한 커스터마이징 방법은 `vendor:publish` 명령어로 뷰 파일을 `resources/views/vendor` 디렉토리로 복사하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령으로 애플리케이션 `resources/views/vendor/pagination` 디렉토리에 뷰들이 복사됩니다. 이 디렉토리 내 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰입니다. 이 파일을 편집하면 페이지네이션 HTML을 변경할 수 있습니다.

기본 페이지네이션 뷰 파일을 다른 것으로 지정하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩 처리
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 작성된 페이지네이션 뷰도 제공합니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩 처리
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음 메서드들로 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                                   | 설명                                                                                           |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `$paginator->count()`                   | 현재 페이지에 표시되는 아이템 수를 반환합니다.                                                      |
| `$paginator->currentPage()`             | 현재 페이지 번호를 반환합니다.                                                                   |
| `$paginator->firstItem()`               | 결과 중 첫 번째 아이템의 번호를 반환합니다.                                                       |
| `$paginator->getOptions()`              | 페이지네이터 옵션을 반환합니다.                                                                  |
| `$paginator->getUrlRange($start, $end)` | 지정한 범위의 페이지 URL을 생성합니다.                                                           |
| `$paginator->hasPages()`                | 여러 페이지로 나눌 만큼 아이템이 충분한지 확인합니다.                                            |
| `$paginator->hasMorePages()`            | 더 많은 데이터 항목이 있는지 확인합니다.                                                        |
| `$paginator->items()`                   | 현재 페이지의 아이템들을 반환합니다.                                                            |
| `$paginator->lastItem()`                | 결과 중 마지막 아이템의 번호를 반환합니다.                                                       |
| `$paginator->lastPage()`                | 마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시에는 지원되지 않습니다.)                |
| `$paginator->nextPageUrl()`             | 다음 페이지 URL을 반환합니다.                                                                    |
| `$paginator->onFirstPage()`             | 현재 페이지가 첫 페이지인지 여부를 반환합니다.                                                   |
| `$paginator->onLastPage()`              | 현재 페이지가 마지막 페이지인지 여부를 반환합니다.                                               |
| `$paginator->perPage()`                 | 페이지당 표시할 아이템 수를 반환합니다.                                                          |
| `$paginator->previousPageUrl()`         | 이전 페이지 URL을 반환합니다.                                                                    |
| `$paginator->total()`                   | 전체 일치하는 아이템 수를 반환합니다. (`simplePaginate` 사용 시에는 지원되지 않습니다.)          |
| `$paginator->url($page)`                | 특정 페이지 번호에 대한 URL을 반환합니다.                                                        |
| `$paginator->getPageName()`             | 페이지 번호 저장에 사용되는 쿼리 문자열 변수명을 반환합니다.                                      |
| `$paginator->setPageName($name)`        | 페이지 번호 저장에 사용될 쿼리 문자열 변수명을 설정합니다.                                        |
| `$paginator->through($callback)`        | 콜백 함수를 이용해 각 아이템을 변환합니다.                                                      |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음 메서드들로 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                               |
| ------------------------------- | ------------------------------------------------------------------ |
| `$paginator->count()`           | 현재 페이지에 표시되는 아이템 수를 반환합니다.                        |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 반환합니다.                                   |
| `$paginator->getOptions()`      | 페이지네이터 옵션을 반환합니다.                                     |
| `$paginator->hasPages()`        | 여러 페이지로 나눌 만큼 아이템이 충분한지 확인합니다.               |
| `$paginator->hasMorePages()`    | 더 많은 데이터 항목이 있는지 확인합니다.                           |
| `$paginator->getCursorName()`   | 커서 저장에 사용되는 쿼리 문자열 변수명을 반환합니다.                |
| `$paginator->items()`           | 현재 페이지의 아이템을 반환합니다.                                 |
| `$paginator->nextCursor()`      | 다음 아이템 세트에 대한 커서 인스턴스를 반환합니다.                 |
| `$paginator->nextPageUrl()`     | 다음 페이지 URL을 반환합니다.                                      |
| `$paginator->onFirstPage()`     | 현재 페이지가 첫 페이지인지 여부를 반환합니다.                     |
| `$paginator->onLastPage()`      | 현재 페이지가 마지막 페이지인지 여부를 반환합니다.                |
| `$paginator->perPage()`         | 페이지당 표시할 아이템 수를 반환합니다.                            |
| `$paginator->previousCursor()`  | 이전 아이템 세트에 대한 커서 인스턴스를 반환합니다.               |
| `$paginator->previousPageUrl()` | 이전 페이지 URL을 반환합니다.                                     |
| `$paginator->setCursorName()`   | 커서 저장에 사용될 쿼리 문자열 변수명을 설정합니다.                |
| `$paginator->url($cursor)`      | 특정 커서 인스턴스에 대한 URL을 반환합니다.                       |

</div>