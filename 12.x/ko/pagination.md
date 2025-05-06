# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 표시하기](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. 하지만 Laravel의 페이지네이션 방식은 쾌적한 경험을 목표로 하고 있습니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent)와 통합되어 있으며, 별도의 설정 없이 데이터베이스 레코드를 쉽고 편리하게 페이지네이션할 수 있습니다.

기본적으로, 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만 Bootstrap 페이지네이션도 지원합니다.

<a name="tailwind"></a>
#### Tailwind

만약 Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용한다면, 애플리케이션의 `resources/css/app.css` 파일은 이미 Laravel 페이지네이션 뷰를 적절히 `@source`하도록 구성되어 있습니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

아이템을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 현재 보고 있는 페이지를 기준으로 쿼리의 "limit"과 "offset" 설정을 자동으로 처리합니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리스트링 인자의 값으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

이 예시에서는 `paginate` 메서드에 "페이지당 표시할 아이템 수"만 인자로 전달합니다. 여기서는 페이지당 `15`개 아이템을 표시합니다:

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
#### 간단한 페이지네이션

`paginate` 메서드는 레코드를 데이터베이스에서 조회하기 전에 쿼리와 일치하는 전체 레코드 수를 카운트합니다. 이렇게 하면 전체 페이지 수 등을 알 수 있습니다. 그러나 UI에 전체 페이지 수를 표시할 계획이 없다면, 이 카운트 쿼리는 불필요합니다.

따라서, UI에 "다음"과 "이전" 링크만 표시하면 충분하다면, `simplePaginate` 메서드를 사용해 더 효율적인 한 번의 쿼리로 페이지네이션할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리 역시 페이지네이션할 수 있습니다. 아래 예시에서는 `App\Models\User` 모델을 페이지네이션하며, 페이지당 15개 레코드를 표시하도록 지정했습니다. 쿼리 빌더의 페이지네이션과 거의 동일한 문법을 가지고 있습니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, 쿼리에 `where` 등 다른 조건을 추가한 뒤 `paginate`를 호출할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

마찬가지로 Eloquent 모델에 대해 `cursorPaginate` 메서드를 사용할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 개의 페이지네이터 인스턴스 사용하기

때때로 한 화면에서 별도의 두 페이지네이터를 렌더링해야 할 수도 있습니다. 하지만 두 페이지네이터 모두 현재 페이지를 저장하는 데 `page` 쿼리 인자를 사용하면 서로 충돌이 발생할 수 있습니다. 이 문제를 해결하려면, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인자로 페이지네이터의 현재 페이지를 저장할 쿼리 인자명을 지정할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate`와 `simplePaginate`가 SQL의 "offset" 구문을 활용하는 것과 달리, 커서 페이지네이션은 쿼리에서 정렬된 컬럼 값을 비교하는 "where" 절을 생성하여, Laravel의 모든 페이지네이션 방법 중 가장 뛰어난 데이터베이스 성능을 제공합니다. 커서 페이지네이션은 대용량 데이터셋이나 "무한 스크롤" UI에 특히 적합합니다.

offset 기반 페이지네이션이 URL 쿼리문에 페이지 번호를 포함하는 반면, 커서 기반 페이지네이션은 쿼리스트링에 "cursor" 문자열을 포함합니다. 커서는 다음 페이지네이션 쿼리가 어디에서 시작할지와 방향을 인코딩한 문자열입니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 사용해 커서 기반 페이지네이터 인스턴스를 만들 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 얻었다면, 보통의 `paginate`나 `simplePaginate`에서처럼 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터에서 제공하는 인스턴스 메서드에 대한 자세한 정보는 [커서 페이지네이터 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면, 쿼리에 "order by" 절이 반드시 포함되어야 합니다. 또한 정렬에 사용되는 컬럼은 페이징을 하는 테이블에 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이점을 설명하기 위해 예시 SQL 쿼리를 살펴보겠습니다. 아래 두 쿼리는 모두 `users` 테이블을 `id` 기준 오름차순 정렬하여 "두 번째 페이지" 결과를 보여줍니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 방식에 비해 아래와 같은 장점이 있습니다:

- 대용량 데이터셋에서, 정렬 컬럼에 인덱스가 있다면 커서 페이지네이션이 더 뛰어난 성능을 보입니다. "offset" 절은 이전까지의 데이터 전체를 탐색해야 하기 때문입니다.
- 쓰기 작업이 잦은 데이터셋에서는, 오프셋 페이지네이션이 레코드를 건너뛰거나 중복 표시할 수 있습니다. 사용자가 보고 있는 페이지에 최근 추가/삭제가 발생했다면 그렇습니다.

다만, 커서 페이지네이션의 제한사항은 다음과 같습니다:

- `simplePaginate`와 같이 "다음"과 "이전" 링크만 제공하며, 페이지 번호별 링크 생성은 지원하지 않습니다.
- 정렬이 반드시 하나 이상의 유니크 컬럼(또는 컬럼 조합) 기준이어야 하며, `null` 값을 가진 컬럼은 사용할 수 없습니다.
- "order by" 절에 쿼리 표현식을 사용할 경우 반드시 별칭을 지정하고 "select" 절에 추가해야 합니다.
- 파라미터를 포함한 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성하기

가끔 이미 메모리에 배열로 안고 있는 아이템을 직접 페이지네이션 인스턴스에 전달해 생성하고 싶을 때가 있습니다. 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스를 직접 생성할 수 있습니다.

`Paginator` 및 `CursorPaginator` 클래스는 결과 집합의 전체 아이템 수를 알 필요가 없으며, 그렇기에 마지막 페이지의 인덱스를 조회하는 메서드는 지원되지 않습니다. 반면, `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인자를 받지만, 전체 아이템 수를 반드시 전달받아야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`, `CursorPaginator`는 `cursorPaginate`, `LengthAwarePaginator`는 `paginate`에 각각 대응합니다.

> [!WARNING]
> 페이지네이터 인스턴스를 수동으로 생성할 때는 반드시 결과 배열을 "슬라이스"해서 전달해야 합니다. 이에 대해 잘 모르겠다면, [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징

기본적으로, 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 그러나, 페이지네이터의 `withPath` 메서드를 사용하면 링크에 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, `http://example.com/admin/users?page=N` 같은 링크를 만들고 싶다면, `/admin/users`를 `withPath`에 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리스트링 값 추가하기

페이지네이션 링크의 쿼리스트링에 값을 추가하려면 `appends` 메서드를 사용하세요. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 호출하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 모든 쿼리스트링 값을 페이지네이션 링크에 추가하려면 `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 붙일 필요가 있다면 `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 추가하고 싶다면 다음과 같이 호출하세요:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시하기

`paginate`를 호출하면 `Illuminate\Pagination\LengthAwarePaginator`의 인스턴스가, `simplePaginate`를 호출하면 `Illuminate\Pagination\Paginator`의 인스턴스가 반환됩니다. 마지막으로, `cursorPaginate`를 호출하면 `Illuminate\Pagination\CursorPaginator`의 인스턴스가 반환됩니다.

이 객체들은 결과 집합을 설명하는 다양한 메서드를 제공합니다. 보조 메서드 외에도 페이지네이터 인스턴스들은 배열처럼 반복(loop)할 수 있습니다. 따라서 결과를 받아온 후 다음과 같이 [Blade](/docs/{{version}}/blade)에서 결과를 표시하고 페이지 링크를 렌더링할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지 링크를 렌더링합니다. 각 링크는 이미 올바른 `page` 쿼리 변수 값을 포함합니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터가 페이지네이션 링크를 표시할 때, 현재 페이지 번호와 함께 현재 페이지 기준 앞뒤 3개 링크가 표시됩니다. `onEachSide` 메서드를 사용해, 페이지네이터가 생성하는 가운데 이동형 윈도우 내 양옆에 표시할 추가 링크 개수를 설정할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

Laravel 페이지네이터 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현해, `toJson` 메서드를 제공합니다. 즉, 페이지네이션 결과를 매우 쉽게 JSON으로 변환할 수 있습니다. 또는, 페이지네이터 인스턴스를 라우트나 컨트롤러 액션에서 반환해도 JSON으로 자동 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page` 등 여러 메타 정보가 포함되고, 결과 레코드는 JSON 배열 내의 `data` 키를 통해 확인할 수 있습니다. 아래는 라우트에서 페이지네이터 인스턴스를 반환했을 때의 JSON 예시입니다:

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
            // 레코드 ...
        },
        {
            // 레코드 ...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이징

기본적으로, 페이지네이션 링크를 렌더링하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 그러나 Tailwind를 사용하지 않는 경우 페이지네이션 링크를 렌더링하는 뷰를 직접 정의할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드에 뷰 이름을 첫 번째 인자를 전달하면 됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달 -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만, 페이지네이션 뷰를 커스터마이징하는 가장 쉬운 방법은 다음 artisan 명령어로 뷰 파일을 `resources/views/vendor` 디렉토리 아래로 내보내 수정하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

명령 실행 시, 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰 파일이 복사됩니다. 여기서 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당하며, 이 파일을 수정해 페이지네이션 HTML을 원하는 대로 바꿀 수 있습니다.

기본 페이지네이션 뷰 파일을 변경하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출해 지정할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩핑
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/) 기반 페이지네이션 뷰도 기본 제공합니다. 기본 Tailwind 뷰가 아닌 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩핑
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 아래 메서드를 통해 추가 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드 | 설명 |
| --- | --- |
| `$paginator->count()` | 현재 페이지의 아이템 개수 반환 |
| `$paginator->currentPage()` | 현재 페이지 번호 반환 |
| `$paginator->firstItem()` | 결과 중 첫 번째 아이템의 번호 반환 |
| `$paginator->getOptions()` | 페이지네이터 옵션 반환 |
| `$paginator->getUrlRange($start, $end)` | 지정한 범위의 페이지네이션 URL 생성 |
| `$paginator->hasPages()` | 다수의 페이지로 분할할 수 있는지 확인 |
| `$paginator->hasMorePages()` | 데이터 저장소에 추가 아이템이 있는지 확인 |
| `$paginator->items()` | 현재 페이지의 아이템 반환 |
| `$paginator->lastItem()` | 결과 중 마지막 아이템의 번호 반환 |
| `$paginator->lastPage()` | 마지막 페이지의 번호 반환 (`simplePaginate` 사용 시 제공되지 않음) |
| `$paginator->nextPageUrl()` | 다음 페이지 URL 반환 |
| `$paginator->onFirstPage()` | 첫 페이지인지 확인 |
| `$paginator->onLastPage()` | 마지막 페이지인지 확인 |
| `$paginator->perPage()` | 페이지당 아이템 수 반환 |
| `$paginator->previousPageUrl()` | 이전 페이지 URL 반환 |
| `$paginator->total()` | 데이터 저장소의 총 일치 아이템 개수 반환 (`simplePaginate` 사용 시 제공되지 않음) |
| `$paginator->url($page)` | 특정 페이지 번호의 URL 반환 |
| `$paginator->getPageName()` | 페이지를 저장하는 쿼리스트링 변수명 반환 |
| `$paginator->setPageName($name)` | 페이지 쿼리스트링 변수명 지정 |
| `$paginator->through($callback)` | 콜백을 사용해 각 아이템 변환 |

</div>

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 아래 메서드를 통해 추가 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                       |
| ------------------------------- | ---------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지의 아이템 개수 반환                             |
| `$paginator->cursor()`          | 현재 커서 인스턴스 반환                                   |
| `$paginator->getOptions()`      | 페이지네이터 옵션 반환                                    |
| `$paginator->hasPages()`        | 다수의 페이지로 분할할 수 있는지 확인                     |
| `$paginator->hasMorePages()`    | 데이터 저장소에 추가 아이템이 있는지 확인                 |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리스트링 변수명 반환                   |
| `$paginator->items()`           | 현재 페이지의 아이템 반환                                 |
| `$paginator->nextCursor()`      | 다음 아이템 셋의 커서 인스턴스 반환                      |
| `$paginator->nextPageUrl()`     | 다음 페이지의 URL 반환                                    |
| `$paginator->onFirstPage()`     | 첫 페이지인지 확인                                        |
| `$paginator->onLastPage()`      | 마지막 페이지인지 확인                                    |
| `$paginator->perPage()`         | 페이지당 아이템 수 반환                                   |
| `$paginator->previousCursor()`  | 이전 아이템 셋의 커서 인스턴스 반환                      |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL 반환                                    |
| `$paginator->setCursorName()`   | 커서 쿼리스트링 변수명 지정                              |
| `$paginator->url($cursor)`      | 특정 커서 인스턴스의 URL 반환                             |

</div>