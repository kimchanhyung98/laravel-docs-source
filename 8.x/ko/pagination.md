# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [수동으로 페이지네이터 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 방식이 신선하게 느껴지기를 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent)에 통합되어 별도의 설정 없이 데이터베이스 레코드를 간편하게 페이지네이션 할 수 있습니다.

기본적으로, 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만, Bootstrap 페이지네이션도 지원합니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용하는 경우, Tailwind CSS 클래스가 제거되지 않도록 애플리케이션의 `tailwind.config.js` 파일의 `content` 키에 Laravel의 페이지네이션 뷰를 참조하도록 지정해야 합니다:

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
### 쿼리 빌더 결과 페이지네이션

아이템들을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries)나 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지를 기준으로 쿼리의 "제한(limit)"과 "오프셋(offset)"을 자동으로 설정합니다. 기본적으로, 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 값으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성한 링크에도 자동으로 삽입됩니다.

이 예제에서는 `paginate` 메서드에 "페이지당 표시할 항목 수"만 전달합니다. 여기서는 페이지당 15개의 항목을 표시하도록 지정해보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자를 보여줍니다.
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
#### 단순 페이지네이션

`paginate` 메서드는 데이터베이스에서 레코드를 조회하기 전에 쿼리로 일치하는 레코드의 총 개수를 계산합니다. 이를 통해 페이지네이터가 전체 페이지 수를 알 수 있게 됩니다. 하지만, 애플리케이션 UI에서 전체 페이지 수를 표시할 계획이 없다면 레코드 개수 쿼리는 불필요합니다.

따라서, 애플리케이션 UI에 "다음"과 "이전" 링크만 간단히 표시하면 충분하다면, 보다 효율적인 단일 쿼리를 위한 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이지네이션할 수 있습니다. 예를 들어, `App\Models\User` 모델을 페이지네이션하여 페이지당 15개의 레코드를 표시해 봅니다. 문법은 쿼리 빌더 결과의 페이지네이션과 거의 동일합니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론 쿼리에 `where` 절 등 다른 조건을 추가한 후 `paginate`를 사용할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

마찬가지로, Eloquent 모델 페이지네이션에도 `simplePaginate`를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

또한, Eloquent 모델에도 커서 페이지네이션(`cursorPaginate`)을 적용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용하기

때로는 한 화면에 별도의 페이지네이터 두 개를 렌더링해야 할 수도 있습니다. 그러나 두 페이지네이터 모두 현재 페이지를 저장하는 데 `page` 쿼리 문자열 파라미터를 사용하면 충돌이 발생합니다. 이 경우, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수로 쿼리 문자열 파라미터 이름을 지정하여 이를 해결할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate` 및 `simplePaginate`는 SQL "offset" 절을 사용하여 쿼리를 생성하지만, 커서 페이지네이션은 쿼리에 포함된 정렬 열의 값을 비교하는 "where" 절을 만들어 효율적인 데이터베이스 성능을 제공합니다. 커서 페이지네이션은 대용량 데이터셋이나 "무한" 스크롤 UI에 적합합니다.

오프셋 기반 페이지네이션은 URL의 쿼리 문자열에 페이지 번호를 포함시키는 반면, 커서 기반 페이지네이션은 쿼리 문자열에 "커서" 문자열을 추가합니다. 커서는 다음 페이지네이션 쿼리가 시작되어야 할 위치와 방향을 인코딩한 문자열입니다:

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더에서 제공하는 `cursorPaginate` 메서드를 사용하여 커서 기반 페이지네이터 인스턴스를 만들 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 가져온 후에는, `paginate`와 `simplePaginate`를 사용할 때와 마찬가지로 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터가 제공하는 인스턴스 메서드에 대한 추가 정보는 [커서 페이지네이터 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> {note} 커서 페이지네이션을 사용하려면 쿼리에 "order by" 절이 반드시 포함되어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 예시 SQL 쿼리로 살펴보겠습니다. 아래 두 쿼리는 모두 `id`로 정렬된 `users` 테이블의 "두 번째 페이지"를 표시합니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 페이지네이션에 비해 다음과 같은 장점이 있습니다:

- 대용량 데이터셋의 경우, "order by" 열에 인덱스가 있다면 커서 페이지네이션이 더 우수한 성능을 제공합니다. "offset" 절은 기존 데이터를 모두 탐색하기 때문입니다.
- 데이터셋에 쓰기가 빈번할 경우, 오프셋 페이지네이션에서는 사용자가 보는 페이지에 최근 데이터가 추가·삭제되면 레코드가 건너뛰어지거나 중복 표시될 수 있습니다.

하지만 커서 페이지네이션에는 다음과 같은 제한 사항이 있습니다:

- `simplePaginate`와 같이 "다음"과 "이전" 링크만 표시할 수 있으며, 페이지 번호가 있는 링크는 지원하지 않습니다.
- 정렬이 하나 이상의 고유 컬럼 또는 고유한 컬럼 조합을 기반으로 해야 합니다. `null` 값이 있는 컬럼은 지원되지 않습니다.
- "order by" 절의 쿼리 표현식은 반드시 별칭이 붙여져 "select" 절에도 포함되어야만 지원됩니다.

<a name="manually-creating-a-paginator"></a>
### 수동으로 페이지네이터 생성하기

이미 메모리에 있는 배열을 전달하여 직접 페이지네이션 인스턴스를 생성해야 할 때가 있습니다. 이때는 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스를 만들 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 총 항목 수를 알 필요가 없습니다. 그러나 이 때문에 마지막 페이지의 인덱스를 얻는 메서드는 없습니다. 반면, `LengthAwarePaginator`는 거의 같은 인수를 받지만 결과 집합의 총 개수를 추가로 전달해야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`에, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate`에 각각 해당합니다.

> {note} 수동으로 페이지네이터를 만들 때는 결과 배열을 직접 "슬라이스(slice)" 해야 합니다. 방법을 잘 모른다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징

기본적으로 페이지네이터가 생성한 링크는 현재 요청의 URI를 따릅니다. 하지만, 페이지네이터의 `withPath` 메서드를 사용하면 링크 생성 시 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, `http://example.com/admin/users?page=N` 형식의 링크를 생성하려면 다음과 같이 `/admin/users`를 `withPath`에 전달하세요:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    //
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가하기

`appends` 메서드를 사용하면 페이지네이션 링크의 쿼리 문자열에 값을 추가할 수 있습니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 `appends`를 호출하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    //
});
```

현재 요청의 모든 쿼리 문자열 값을 페이지네이션 링크에 추가하고 싶다면 `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기

페이지네이터가 생성한 URL 끝에 "해시 프래그먼트"를 추가해야 한다면, `fragment` 메서드를 사용하세요. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 추가하려면 다음과 같이 호출합니다:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환하고, `simplePaginate`는 `Illuminate\Pagination\Paginator`를 반환합니다. 또한, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 대한 다양한 메서드를 제공합니다. 뿐만 아니라, 페이지네이터 인스턴스는 반복자(Iterator)이므로 배열처럼 루프를 돌릴 수 있습니다. 따라서 결과를 받아서 [Blade](/docs/{{version}}/blade)로 결과를 출력하고 페이지 링크를 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지로 이동하는 링크를 렌더링합니다. 각 링크에는 이미 올바른 `page` 쿼리 문자열 변수가 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환된다는 점을 기억하세요.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터가 링크를 표시할 때, 현재 페이지 번호와 함께 현재 페이지 앞뒤로 3개의 페이지 링크가 출력됩니다. `onEachSide` 메서드를 사용하면, 페이지네이터가 생성하는 링크 집합의 중간 슬라이딩 윈도우에서 현재 페이지의 양쪽에 표시할 추가 링크 개수를 조정할 수 있습니다:

```php
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며 `toJson` 메서드를 제공합니다. 따라서 페이지네이션 결과를 아주 쉽게 JSON으로 변환할 수 있습니다. 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터의 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함됩니다. 결과 레코드는 JSON 배열 내 `data` 키를 통해 접근할 수 있습니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환할 때 생성되는 JSON 예시입니다:

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

기본적으로 페이지네이션 링크를 출력하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. Tailwind를 사용하지 않는다면, 직접 페이지네이션 링크를 렌더링하는 뷰를 정의할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드에 뷰 이름을 첫 번째 인자로 전달하면 됩니다:

```php
{{ $paginator->links('view.name') }}

// 추가 데이터를 뷰에 전달하기
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

가장 쉬운 커스터마이징 방법은 `vendor:publish` 명령어로 뷰를 `resources/views/vendor` 디렉토리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령을 실행하면, 뷰가 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 저장됩니다. 이 안에 있는 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당하며, 직접 이 파일을 수정해 페이지네이션 HTML을 변경할 수 있습니다.

다른 파일을 기본 페이지네이션 뷰로 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출하면 됩니다:

```php
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
### Bootstrap 사용하기

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 만든 페이지네이션 뷰도 제공합니다. 기본 Tailwind 뷰 대신 이 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 페이지네이터의 `useBootstrap` 메서드를 호출하세요:

```php
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
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음 메서드를 통해 페이지네이션 정보를 추가로 제공합니다:

메서드  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 수를 반환합니다.
`$paginator->currentPage()`  |  현재 페이지 번호를 반환합니다.
`$paginator->firstItem()`  |  결과에서 첫 번째 항목의 번호를 반환합니다.
`$paginator->getOptions()`  |  페이지네이터 옵션을 반환합니다.
`$paginator->getUrlRange($start, $end)`  |  페이지네이션 URL 범위를 생성합니다.
`$paginator->hasPages()`  |  여러 페이지로 분할할 수 있는 충분한 항목이 있는지 확인합니다.
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인합니다.
`$paginator->items()`  |  현재 페이지의 항목을 반환합니다.
`$paginator->lastItem()`  |  결과에서 마지막 항목의 번호를 반환합니다.
`$paginator->lastPage()`  |  마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시 제공되지 않음)
`$paginator->nextPageUrl()`  |  다음 페이지의 URL을 반환합니다.
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 확인합니다.
`$paginator->perPage()`  |  페이지당 표시할 항목 수를 반환합니다.
`$paginator->previousPageUrl()`  |  이전 페이지의 URL을 반환합니다.
`$paginator->total()`  |  데이터 저장소의 전체 일치 항목 수를 반환합니다. (`simplePaginate` 사용 시 제공되지 않음)
`$paginator->url($page)`  |  주어진 페이지 번호에 대한 URL을 반환합니다.
`$paginator->getPageName()`  |  페이지를 저장하는 쿼리 문자열 변수명을 반환합니다.
`$paginator->setPageName($name)`  |  페이지를 저장하는 쿼리 문자열 변수명을 설정합니다.

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

메서드  |  설명
-------  |  -----------
`$paginator->count()`  |  현재 페이지의 항목 수를 반환합니다.
`$paginator->cursor()`  |  현재 커서 인스턴스를 반환합니다.
`$paginator->getOptions()`  |  페이지네이터 옵션을 반환합니다.
`$paginator->hasPages()`  |  여러 페이지로 분할할 수 있는 충분한 항목이 있는지 확인합니다.
`$paginator->hasMorePages()`  |  데이터 저장소에 더 많은 항목이 있는지 확인합니다.
`$paginator->getCursorName()`  |  커서를 저장하는 쿼리 문자열 변수명을 반환합니다.
`$paginator->items()`  |  현재 페이지의 항목을 반환합니다.
`$paginator->nextCursor()`  |  다음 항목 집합에 대한 커서 인스턴스를 반환합니다.
`$paginator->nextPageUrl()`  |  다음 페이지의 URL을 반환합니다.
`$paginator->onFirstPage()`  |  현재 페이지가 첫 페이지인지 확인합니다.
`$paginator->perPage()`  |  페이지당 표시할 항목 수를 반환합니다.
`$paginator->previousCursor()`  |  이전 항목 집합에 대한 커서 인스턴스를 반환합니다.
`$paginator->previousPageUrl()`  |  이전 페이지의 URL을 반환합니다.
`$paginator->setCursorName()`  |  커서를 저장하는 쿼리 문자열 변수명을 설정합니다.
`$paginator->url($cursor)`  |  주어진 커서 인스턴스에 대한 URL을 반환합니다.