# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이징](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 범위 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메소드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메소드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 접근 방식이 신선한 숨결이 되길 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries) 및 [Eloquent ORM](/docs/{{version}}/eloquent)과 통합되어 있어 별도의 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이지네이션할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만 Bootstrap 페이지네이션도 지원됩니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 함께 사용하는 경우, 애플리케이션의 `tailwind.config.js` 파일의 `content` 키가 Laravel의 페이지네이션 뷰를 참조하도록 설정해야 Tailwind 클래스가 제거되지 않습니다.

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

항목을 페이지네이션 하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지를 기준으로 쿼리의 "limit"과 "offset"을 자동으로 설정해줍니다. 기본적으로 현재 페이지는 HTTP 요청의 쿼리 스트링 중 `page` 값으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

이 예제에서 `paginate` 메서드에 전달하는 유일한 인자는 한 "페이지당" 보여줄 항목 개수입니다. 여기서는 한 페이지에 `15`개의 항목만 보여주도록 명시합니다.

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * 모든 애플리케이션 사용자 표시
         */
        public function index(): View
        {
            return view('user.index', [
                'users' => DB::table('users')->paginate(15)
            ]);
        }
    }

<a name="simple-pagination"></a>
#### 간단한 페이지네이션

`paginate` 메서드는 쿼리로 매칭된 전체 레코드의 개수를 먼저 계산한 후, 실제 데이터베이스에서 레코드를 가져옵니다. 이는 페이지네이터가 전체 페이지 수를 알 수 있도록 하기 위함입니다. 하지만 애플리케이션 UI에 전체 페이지 수를 표시할 필요가 없다면 레코드 수 쿼리가 불필요할 수 있습니다.

따라서 UI에 "다음"과 "이전" 링크만 단순히 표시할 필요가 있다면, 효율적인 단일 쿼리를 실행하는 `simplePaginate` 메서드를 사용할 수 있습니다.

    $users = DB::table('users')->simplePaginate(15);

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이지네이션 할 수 있습니다. 이 예제에서는 `App\Models\User` 모델을 페이지네이션하며, 한 페이지에 15개의 레코드를 표시하도록 지정합니다. 쿼리 빌더 결과를 페이지네이션하는 방법과 거의 동일한 문법임을 알 수 있습니다.

    use App\Models\User;

    $users = User::paginate(15);

물론, 쿼리에 `where` 절 등 다른 조건을 추가한 뒤 `paginate` 메서드를 호출할 수도 있습니다.

    $users = User::where('votes', '>', 100)->paginate(15);

또한 Eloquent 모델을 페이지네이션 할 때도 `simplePaginate` 메서드를 사용할 수 있습니다.

    $users = User::where('votes', '>', 100)->simplePaginate(15);

마찬가지로, Eloquent 모델에 대해 커서 페이지네이션을 원한다면 `cursorPaginate` 메서드를 사용할 수 있습니다.

    $users = User::where('votes', '>', 100)->cursorPaginate(15);

<a name="multiple-paginator-instances-per-page"></a>
#### 한 화면에 여러 페이지네이터 인스턴스 사용

하나의 화면에 두 개의 별도 페이지네이터를 표시해야 하는 경우가 있습니다. 하지만 두 페이지네이터 인스턴스가 모두 `page` 쿼리 스트링 파라미터를 사용한다면 충돌이 발생합니다. 이 문제를 해결하려면, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수로 사용할 쿼리 스트링 파라미터의 이름을 지정할 수 있습니다.

    use App\Models\User;

    $users = User::where('votes', '>', 100)->paginate(
        $perPage = 15, $columns = ['*'], $pageName = 'users'
    );

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate` 및 `simplePaginate`는 SQL의 "offset" 절을 사용하여 쿼리를 생성합니다. 커서 페이지네이션은 쿼리에서 정렬된 컬럼의 값을 비교하는 "where" 절을 생성하여 모든 Laravel 페이지네이션 방식 중 가장 효율적인 데이터베이스 성능을 제공합니다. 이 방법은 대용량 데이터셋 및 "무한 스크롤" UI에 특히 적합합니다.

offset 기반 페이지네이션은 페이지 번호가 쿼리 스트링에 포함되지만, 커서 기반 페이지네이션은 "커서"라는 문자열이 쿼리 스트링에 포함됩니다. 커서는 다음 페이지네이션 쿼리가 어디서 시작해야 할지와 방향을 담고 있는 인코딩된 문자열입니다.

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 통해 커서 기반 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

    $users = DB::table('users')->orderBy('id')->cursorPaginate(15);

커서 페이지네이터 인스턴스를 얻은 뒤에는, `paginate` 및 `simplePaginate`와 마찬가지로 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터의 인스턴스 메서드에 대한 자세한 정보는 [cursor paginator instance method documentation](#cursor-paginator-instance-methods)에서 확인할 수 있습니다.

> [!WARNING]  
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 하며, 정렬 컬럼은 페이지네이션하는 테이블의 컬럼이어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 보여주기 위해 몇 가지 SQL 예제를 살펴보겠습니다. 아래의 두 쿼리는 모두 `id` 기준으로 정렬된 `users` 테이블의 "두 번째 페이지"를 보여줍니다.

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 페이지네이션에 비해 다음과 같은 장점이 있습니다.

- 대용량 데이터셋의 경우 "order by" 컬럼에 인덱스가 있다면 커서 페이지네이션이 더 뛰어난 성능을 제공합니다. 반면 오프셋은 이전 데이터 전체를 스캔해야 합니다.
- 데이터가 자주 추가·삭제되는 경우, 오프셋 페이지네이션은 레코드를 건너뛰거나 중복 표시를 일으킬 수 있습니다.

단, 커서 페이지네이션에는 다음과 같은 제한이 있습니다.

- `simplePaginate`와 마찬가지로 "다음" 및 "이전" 링크만 표시할 수 있으며, 페이지 번호 링크 생성은 지원하지 않습니다.
- 정렬 기준이 적어도 하나의 고유 컬럼(또는 고유한 컬럼 조합)이어야 합니다. `null` 값이 있는 컬럼은 지원되지 않습니다.
- "order by" 절에 쿼리 표현식이 있다면, 반드시 별칭(aliased)이 있어야 하며 "select" 절에도 추가되어야 지원됩니다.
- 파라미터가 있는 쿼리 표현식은 지원되지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성

메모리에 이미 존재하는 배열 데이터를 기반으로 페이지네이션 인스턴스를 직접 만들고 싶을 때가 있습니다. 이 때 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나의 인스턴스를 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과셋의 전체 항목 개수를 알 필요가 없습니다. 이 때문에 마지막 페이지의 인덱스를 얻는 메서드를 제공하지 않습니다. 반면 `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수를 받지만, 전체 결과셋의 개수도 반드시 필요합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`에, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate`에 각각 대응합니다.

> [!WARNING]  
> 직접 페이지네이터 인스턴스를 만들 때는, 전달할 결과 배열도 직접 "slice" 해야 합니다. 구체적인 방법은 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참조하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이징

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 하지만 페이지네이터의 `withPath` 메서드를 사용하면 링크 생성 시 URI를 커스터마이즈할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N`과 같은 링크를 생성하게 하려면, `withPath` 메서드에 `/admin/users`를 전달하면 됩니다.

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->withPath('/admin/users');

        // ...
    });

<a name="appending-query-string-values"></a>
#### 쿼리 스트링 값 추가

`appends` 메서드를 사용해 페이지네이션 링크에 쿼리 스트링 값을 추가할 수 있습니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 `appends`를 호출하면 됩니다.

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->appends(['sort' => 'votes']);

        // ...
    });

현재 요청의 모든 쿼리 스트링 값을 페이지네이션 링크에 추가하고 싶다면, `withQueryString` 메서드를 사용할 수 있습니다.

    $users = User::paginate(15)->withQueryString();

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 추가하고 싶다면, `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 붙이려면 아래와 같이 하면 됩니다.

    $users = User::paginate(15)->fragment('users');

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드는 `Illuminate\Pagination\LengthAwarePaginator`의 인스턴스를 반환하며, `simplePaginate`는 `Illuminate\Pagination\Paginator`의 인스턴스를 반환합니다. 그리고 마지막으로, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과셋을 설명하는 여러 메서드를 제공합니다. 또한 페이지네이터 인스턴스는 반복자(iterator)이기도 하므로, 배열처럼 루프를 돌릴 수도 있습니다. 결과를 받아온 뒤, [Blade](/docs/{{version}}/blade)를 통해 결과를 표시하고 페이지 링크를 렌더링할 수 있습니다.

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과셋의 나머지 페이지로 이동할 수 있는 링크를 렌더링합니다. 각 링크에는 이미 적절한 `page` 쿼리 변수 값이 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 범위 조정

페이지네이터가 페이지네이션 링크를 표시할 때, 현재 페이지 번호와 함께 앞뒤로 3개의 페이지 링크가 표시됩니다. `onEachSide` 메서드를 사용해 현재 페이지를 기준으로 중간 윈도우에서 양쪽에 표시할 페이지 링크 개수를 제어할 수 있습니다.

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel의 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하고 있어, `toJson` 메서드를 이용해 페이지네이션 결과를 손쉽게 JSON으로 변환할 수 있습니다. 또한 페이지네이터 인스턴스를 라우트나 컨트롤러에서 반환하면 자동으로 JSON으로 변환됩니다.

    use App\Models\User;

    Route::get('/users', function () {
        return User::paginate();
    });

페이지네이터에서 반환되는 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보와, 레코드는 `data` 키를 통해 접근할 수 있습니다. 다음은 페이지네이터 인스턴스를 라우트에서 반환할 경우 생성되는 JSON 예시입니다.

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

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이징

기본적으로 페이지네이션 링크를 표시하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. Tailwind를 사용하지 않는 경우, 직접 원하는 뷰를 정의해 이 링크들을 렌더링할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드 호출 시, 첫 번째 인자로 뷰 이름을 전달할 수 있습니다.

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달 -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이지네이션 뷰를 커스터마이징하는 가장 간편한 방법은 `vendor:publish` 명령어로 해당 뷰를 `resources/views/vendor` 디렉터리로 내보내는 것입니다.

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 뷰 파일이 저장됩니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당합니다. HTML을 수정하려면 이 파일을 편집하면 됩니다.

다른 파일을 기본 페이지네이션 뷰로 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출하면 됩니다.

    <?php

    namespace App\Providers;

    use Illuminate\Pagination\Paginator;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 부트스트랩
         */
        public function boot(): void
        {
            Paginator::defaultView('view-name');

            Paginator::defaultSimpleView('view-name');
        }
    }

<a name="using-bootstrap"></a>
### Bootstrap 사용

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 제작된 페이지네이션 뷰도 내장하고 있습니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요.

    use Illuminate\Pagination\Paginator;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Paginator::useBootstrapFive();
        Paginator::useBootstrapFour();
    }

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메소드

각 페이지네이터 인스턴스는 다음 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다.

<div class="overflow-auto">

| 메서드 | 설명 |
| --- | --- |
| `$paginator->count()` | 현재 페이지의 항목 개수 반환 |
| `$paginator->currentPage()` | 현재 페이지 번호 반환 |
| `$paginator->firstItem()` | 결과 중 첫 항목의 결과 번호 반환 |
| `$paginator->getOptions()` | 페이지네이터 옵션 반환 |
| `$paginator->getUrlRange($start, $end)` | 페이지네이션 URL 범위 생성 |
| `$paginator->hasPages()` | 여러 페이지로 나눌 만큼 항목이 있는지 확인 |
| `$paginator->hasMorePages()` | 더 많은 항목이 남아있는지 확인 |
| `$paginator->items()` | 현재 페이지의 항목 반환 |
| `$paginator->lastItem()` | 결과 중 마지막 항목의 결과 번호 반환 |
| `$paginator->lastPage()` | 마지막 페이지의 번호 반환 (`simplePaginate`에서는 사용 불가) |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL 반환 |
| `$paginator->onFirstPage()` | 첫 페이지에 있는지 확인 |
| `$paginator->perPage()` | 페이지당 표시할 항목 개수 |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL 반환 |
| `$paginator->total()` | 전체 일치 항목 수 반환 (`simplePaginate`에서는 사용 불가) |
| `$paginator->url($page)` | 특정 페이지 번호의 URL 반환 |
| `$paginator->getPageName()` | 페이지 정보를 저장하는 쿼리 스트링 변수 이름 반환 |
| `$paginator->setPageName($name)` | 페이지 정보를 저장할 쿼리 스트링 변수 이름 설정 |
| `$paginator->through($callback)` | 콜백을 사용하여 각 항목 변환 |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메소드

각 커서 페이지네이터 인스턴스는 다음 메서드를 통해 추가 정보를 제공합니다.

<div class="overflow-auto">

| 메서드                          | 설명                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `$paginator->count()`           | 현재 페이지의 항목 개수 반환                                 |
| `$paginator->cursor()`          | 현재 커서 인스턴스 반환                                      |
| `$paginator->getOptions()`      | 페이지네이터 옵션 반환                                       |
| `$paginator->hasPages()`        | 여러 페이지로 나눌 만큼 항목이 있는지 확인                   |
| `$paginator->hasMorePages()`    | 더 많은 항목이 남아있는지 확인                               |
| `$paginator->getCursorName()`   | 커서를 저장하는 쿼리 스트링 변수 이름 반환                   |
| `$paginator->items()`           | 현재 페이지의 항목 반환                                      |
| `$paginator->nextCursor()`      | 다음 항목들의 커서 인스턴스 반환                             |
| `$paginator->nextPageUrl()`     | 다음 페이지의 URL 반환                                       |
| `$paginator->onFirstPage()`     | 첫 페이지에 있는지 확인                                      |
| `$paginator->onLastPage()`      | 마지막 페이지에 있는지 확인                                  |
| `$paginator->perPage()`         | 페이지당 표시할 항목 개수                                    |
| `$paginator->previousCursor()`  | 이전 항목들의 커서 인스턴스 반환                             |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL 반환                                       |
| `$paginator->setCursorName()`   | 커서를 저장할 쿼리 스트링 변수 이름 설정                     |
| `$paginator->url($cursor)`      | 특정 커서 인스턴스의 URL 반환                                 |

</div>