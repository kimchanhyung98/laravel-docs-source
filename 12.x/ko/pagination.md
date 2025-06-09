# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 기반 페이지네이션](#cursor-pagination)
    - [페이지네이터 직접 생성하기](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이즈](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 범위 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이즈](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 번거롭고 복잡할 수 있습니다. 라라벨에서는 페이지네이션이 훨씬 쉽고 간편하게 처리됩니다. 라라벨의 페이지네이터는 [쿼리 빌더](/docs/12.x/queries)와 [Eloquent ORM](/docs/12.x/eloquent) 모두에 통합되어 있으며, 별도의 설정 없이도 데이터베이스 레코드를 쉽게 페이지네이션할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 바로 호환됩니다. 또한 Bootstrap을 사용하는 페이지네이션 뷰도 지원합니다.

<a name="tailwind"></a>
#### Tailwind

Tailwind 4.x와 함께 라라벨의 기본 Tailwind 페이지네이션 뷰를 사용하는 경우, 애플리케이션의 `resources/css/app.css` 파일은 이미 라라벨의 페이지네이션 뷰를 `@source`로 올바르게 설정하고 있습니다.

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

아이템을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/12.x/queries)나 [Eloquent 쿼리](/docs/12.x/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지를 기준으로 쿼리의 "limit" 및 "offset"을 자동으로 설정합니다. 기본적으로 현재 페이지는 HTTP 요청의 쿼리스트링에서 `page` 인수의 값으로 결정됩니다. 이 값은 라라벨에서 자동으로 인식하며, 페이지네이터가 생성하는 링크에도 자동으로 포함됩니다.

아래 예시에서는 `paginate` 메서드에 한 페이지만큼 보여줄 항목 수만 인수로 전달합니다. 여기서는 한 페이지에 `15`개 항목을 보여주도록 하겠습니다.

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
#### 단순 페이지네이션

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리에 일치하는 전체 레코드 개수를 계산합니다. 이렇게 하는 이유는 페이지네이터가 총 페이지 수를 알아야 하기 때문입니다. 하지만 UI에 전체 페이지 숫자를 보여줄 계획이 없다면, 전체 개수를 구하는 쿼리는 불필요할 수 있습니다.

따라서, 애플리케이션 UI에서 "이전"과 "다음" 버튼만 표시하면 충분하다면, 성능이 더 좋은 `simplePaginate` 메서드를 사용할 수 있습니다. 이 메서드는 기록 개수를 세지 않으므로 한 번의 효율적인 쿼리만 실행됩니다.

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/12.x/eloquent) 쿼리도 동일하게 페이지네이션할 수 있습니다. 아래 예제에서는 `App\Models\User` 모델을 15개 레코드씩 페이지네이션합니다. 쿼리 빌더로 페이지네이션하는 방법과 거의 동일합니다.

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 같은 쿼리 조건을 추가한 후에도 `paginate` 메서드를 사용할 수 있습니다.

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다.

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

마찬가지로, `cursorPaginate` 메서드를 사용하여 Eloquent 모델의 커서 기반 페이지네이션도 할 수 있습니다.

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에서 여러 페이지네이터 인스턴스 사용하기

애플리케이션에서 하나의 화면에 두 개 이상의 서로 다른 페이지네이터를 동시에 표시해야 하는 경우가 있습니다. 이때 두 페이지네이터 인스턴스가 모두 `page` 쿼리 문자열 파라미터를 사용한다면 서로 충돌이 발생할 수 있습니다. 이런 충돌을 피하려면, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수에 해당 페이지네이터가 사용할 쿼리 문자열 파라미터 이름을 지정하면 됩니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 기반 페이지네이션

`paginate`와 `simplePaginate` 메서드는 SQL의 "offset" 절을 이용해 페이지네이션 쿼리를 생성합니다. 반면, 커서 기반 페이지네이션은 쿼리에서 정렬된 컬럼의 값을 비교하는 "where" 절을 사용하여, 라라벨의 페이지네이션 방식 중 가장 효율적으로 동작합니다. 특히 대량 데이터셋 또는 "무한 스크롤" 방식의 UI에 적합합니다.

오프셋 기반 페이지네이션에서는 URL 쿼리스트링에 페이지 번호가 포함되지만, 커서 기반 페이지네이션에서는 "커서(cursor)"라는 문자열이 쿼리스트링에 포함됩니다. 커서는 다음 페이지 쿼리를 어디서부터 시작할지와, 어떤 방향으로 페이지네이션 할지를 인코딩한 문자열입니다.

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더에서 `cursorPaginate` 메서드를 호출하면 커서 기반 페이지네이터 인스턴스를 만들 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 받은 후에는, [페이지네이션 결과를 표시](#displaying-pagination-results)할 때 `paginate` 또는 `simplePaginate` 때와 동일하게 활용할 수 있습니다. 커서 페이지네이터에서 제공하는 인스턴스 메서드에 대해서는 [커서 페이지네이터 인스턴스 메서드](#cursor-paginator-instance-methods) 문서를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 필요합니다. 또한, 쿼리에서 정렬에 사용되는 컬럼은 반드시 페이지네이션하려는 테이블에 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션과 오프셋 페이지네이션의 비교

오프셋 페이지네이션과 커서 페이지네이션의 차이점을 이해하기 위해 예시 SQL 쿼리를 살펴보겠습니다. 아래 두 쿼리는 모두 `users` 테이블을 `id` 기준으로 정렬한 상태에서 "두 번째 페이지"의 결과를 보여줍니다.

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 기반 페이지네이션은 오프셋 기반 방식에 비해 다음과 같은 장점이 있습니다.

- 데이터셋이 매우 큰 경우, "order by"에 사용된 컬럼에 인덱스가 붙어 있다면 커서 페이지네이션이 더 나은 성능을 보입니다. 오프셋은 앞에 있는 모든 데이터를 조회해야 하는 반면, 커서는 건너뛰지 않고 바로 시작 위치에서 조회할 수 있기 때문입니다.
- 데이터가 자주 추가/삭제되는 환경에서는, 오프셋 페이지네이션으로 결과를 표시할 때 페이지가 변경되는 과정에서 일부 레코드가 빠지거나 중복 표시될 수 있습니다.

하지만 커서 기반 페이지네이션에는 다음과 같은 제한이 있습니다.

- `simplePaginate`와 같이, "이전"과 "다음" 링크만 제공할 수 있고, 페이지 번호로 이동하는 링크는 지원하지 않습니다.
- 정렬 기준(ORDER BY)에 반드시 고유 컬럼(또는 컬럼 조합)이 필요합니다. 또한 컬럼에 `null` 값이 있으면 사용할 수 없습니다.
- "order by" 절의 쿼리 표현식은 반드시 별칭(alias)으로 지정되어 "select" 절에도 포함해야 지원됩니다.
- 파라미터가 사용된 쿼리 표현식은 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 직접 생성하기

때로는 이미 메모리에 가지고 있는 배열 데이터를 이용해 직접 페이지네이션 인스턴스를 만들어야 할 때가 있습니다. 이때는 용도에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나의 인스턴스를 수동으로 생성하면 됩니다.

`Paginator`와 `CursorPaginator` 클래스는 전체 아이템 개수를 알 필요가 없습니다. 그러나 이런 특성 때문에, 마지막 페이지의 인덱스를 구하는 등의 메서드는 없습니다. 반면, `LengthAwarePaginator`는 거의 비슷한 인수를 받지만 전체 아이템 개수도 요구합니다.

정리하면, `Paginator`는 쿼리 빌더의 `simplePaginate`와, `CursorPaginator`는 `cursorPaginate`와, `LengthAwarePaginator`는 `paginate`와 각각 대응됩니다.

> [!WARNING]
> 직접 페이지네이터 인스턴스를 만들 때는, 결과 배열을 페이지 단위로 "슬라이스(slice)"해서 전달해야 합니다. 이 방법이 궁금하다면 PHP의 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이즈

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI를 그대로 사용합니다. 하지만 `withPath` 메서드를 사용하면 링크에 사용할 URI를 직접 지정할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 같은 링크를 생성하게 하려면, `withPath`에 `/admin/users`를 전달하면 됩니다.

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

`appends` 메서드를 사용하면, 페이지네이션 링크에 쿼리스트링 값을 추가할 수 있습니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 붙이고 싶다면, 다음과 같이 `appends`를 호출하면 됩니다.

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 쿼리스트링 값을 모두 페이지네이션 링크에 추가하려면, `withQueryString` 메서드를 사용할 수 있습니다.

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가하기

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 붙이고 싶을 때는, `fragment` 메서드를 사용할 수 있습니다. 예를 들어 모든 링크 끝에 `#users`를 붙이려면 다음과 같이 구현합니다.

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드를 호출하면 결과로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를, `simplePaginate`를 호출하면 `Illuminate\Pagination\Paginator` 인스턴스를, 그리고 `cursorPaginate`를 호출하면 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환받게 됩니다.

이들 객체는 결과 집합에 대한 다양한 메서드를 제공합니다. 또한 페이지네이터 인스턴스는 반복자(이터러블)이므로, 배열처럼 루프를 돌릴 수 있습니다. 따라서 결과를 받아와 다음과 같이 [Blade](/docs/12.x/blade)에서 레코드와 페이지 링크를 쉽게 출력할 수 있습니다.

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 나머지 페이지로 이동할 수 있는 페이지 링크들을 렌더링합니다. 각각의 링크에는 이미 올바른 `page` 쿼리 변수값이 포함되어 있습니다. 참고로, `links` 메서드가 생성하는 HTML 마크업은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 바로 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 범위 조정

페이지네이션 링크를 표시할 때 기본적으로 현재 페이지를 중심으로 앞뒤 3페이지까지의 링크가 표시됩니다. `onEachSide` 메서드를 이용하면, 현재 페이지를 기준으로 양옆에 표시될 추가 링크 수를 원하는 만큼 조정할 수 있습니다.

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

라라벨의 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하고 있어, `toJson` 메서드를 통해 매우 간편하게 페이지네이션 결과를 JSON으로 변환할 수 있습니다. 또한, 페이지네이터 인스턴스를 라우트나 컨트롤러에서 직접 반환해도 자동으로 JSON으로 변환됩니다.

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

이렇게 반환된 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함됩니다. 실제 결과 데이터는 JSON 객체의 `data` 키에 배열로 담깁니다. 아래는 페이지네이터 인스턴스를 라우트에서 반환할 때 생성되는 JSON 예시입니다.

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
            // 레코드...
        },
        {
            // 레코드...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이즈

기본적으로 페이지네이션 링크를 출력하는 뷰는 [Tailwind CSS](https://tailwindcss.com)와 호환되는 형태로 제공됩니다. 만약 Tailwind 대신 다른 CSS 프레임워크를 사용하거나, 직접 커스터마이즈된 뷰를 만들고 싶다면 필요한 대로 뷰를 정의할 수 있습니다. 페이지네이터 인스턴스에서 `links` 메서드를 호출할 때, 첫 번째 인수로 뷰 이름을 지정할 수 있습니다.

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰로 추가 데이터 전달하기... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

가장 쉬운 커스터마이즈 방법은 `vendor:publish` artisan 명령어로 페이지네이션 뷰 파일을 프로젝트에 복사하는 것입니다.

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령을 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 뷰 파일들이 복사됩니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰이므로, 해당 파일을 수정하여 HTML 구조를 원하는 대로 바꿀 수 있습니다.

만약 기본 페이지네이션 뷰로 다른 파일을 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `defaultView`와 `defaultSimpleView` 메서드를 호출해 변경할 수 있습니다.

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
### Bootstrap 사용하기

라라벨은 [Bootstrap CSS](https://getbootstrap.com/)를 기반으로 한 페이지네이션 뷰도 제공합니다. 기본 Tailwind 뷰 대신 Bootstrap용 뷰를 사용하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하면 됩니다.

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
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다.

<div class="overflow-auto">

| 메서드                                  | 설명                                                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `$paginator->count()`                   | 현재 페이지에 표시되는 항목 개수를 반환합니다.                                                                        |
| `$paginator->currentPage()`             | 현재 페이지 번호를 반환합니다.                                                                                        |
| `$paginator->firstItem()`               | 결과 중 첫 번째 아이템의 번호를 반환합니다.                                                                           |
| `$paginator->getOptions()`              | 페이지네이터 옵션을 반환합니다.                                                                                      |
| `$paginator->getUrlRange($start, $end)` | 지정 구간의 페이지 URL 목록을 생성합니다.                                                                             |
| `$paginator->hasPages()`                | 여러 페이지로 나눌만큼 충분한 데이터가 있는지 확인합니다.                                                             |
| `$paginator->hasMorePages()`            | 추가 페이지가 존재하는지 확인합니다.                                                                                  |
| `$paginator->items()`                   | 현재 페이지의 아이템 목록을 반환합니다.                                                                               |
| `$paginator->lastItem()`                | 결과 중 마지막 아이템의 번호를 반환합니다.                                                                            |
| `$paginator->lastPage()`                | 마지막 페이지 번호를 반환합니다. (`simplePaginate` 사용 시에는 값이 없습니다.)                                         |
| `$paginator->nextPageUrl()`             | 다음 페이지의 URL을 반환합니다.                                                                                       |
| `$paginator->onFirstPage()`             | 첫 페이지에 있는지 확인합니다.                                                                                        |
| `$paginator->onLastPage()`              | 마지막 페이지에 있는지 확인합니다.                                                                                    |
| `$paginator->perPage()`                 | 한 페이지에 표시할 항목 개수를 반환합니다.                                                                            |
| `$paginator->previousPageUrl()`         | 이전 페이지의 URL을 반환합니다.                                                                                       |
| `$paginator->total()`                   | 전체 데이터 저장소 내 일치하는 항목 수를 반환합니다. (`simplePaginate`에서는 지원하지 않습니다.)                        |
| `$paginator->url($page)`                | 특정 페이지 번호에 해당하는 URL을 반환합니다.                                                                         |
| `$paginator->getPageName()`             | 페이지 번호를 저장하는 쿼리 문자열 변수명을 반환합니다.                                                               |
| `$paginator->setPageName($name)`        | 페이지 번호를 저장하는 쿼리스트링 변수명을 설정합니다.                                                                |
| `$paginator->through($callback)`        | 각 아이템을 주어진 콜백을 통해 변환합니다.                                                                            |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스도 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다.

<div class="overflow-auto">

| 메서드                          | 설명                                                                 |
| ------------------------------- | -------------------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지의 항목 개수를 반환합니다.                                 |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 반환합니다.                                      |
| `$paginator->getOptions()`      | 페이지네이터 옵션을 반환합니다.                                       |
| `$paginator->hasPages()`        | 여러 페이지로 나눌만큼 충분한 데이터가 있는지 확인합니다.              |
| `$paginator->hasMorePages()`    | 추가 페이지가 존재하는지 확인합니다.                                  |
| `$paginator->getCursorName()`   | 커서 값을 저장하는 쿼리 문자열 변수명을 반환합니다.                    |
| `$paginator->items()`           | 현재 페이지의 아이템 목록을 반환합니다.                                |
| `$paginator->nextCursor()`      | 다음 데이터셋을 위한 커서 인스턴스를 반환합니다.                       |
| `$paginator->nextPageUrl()`     | 다음 페이지의 URL을 반환합니다.                                       |
| `$paginator->onFirstPage()`     | 첫 페이지에 있는지 확인합니다.                                        |
| `$paginator->onLastPage()`      | 마지막 페이지에 있는지 확인합니다.                                    |
| `$paginator->perPage()`         | 한 페이지에 표시될 항목 개수를 반환합니다.                            |
| `$paginator->previousCursor()`  | 이전 데이터셋을 위한 커서 인스턴스를 반환합니다.                       |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 반환합니다.                                       |
| `$paginator->setCursorName()`   | 커서를 저장하는 쿼리 변수명을 설정합니다.                             |
| `$paginator->url($cursor)`      | 특정 커서 인스턴스에 대응하는 URL을 반환합니다.                        |

</div>
