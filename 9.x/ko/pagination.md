# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이즈](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환하기](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이즈](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [Cursor Paginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 접근 방식이 신선한 바람이 되었으면 합니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries) 및 [Eloquent ORM](/docs/{{version}}/eloquent)에 통합되어 있으며 별도의 설정 없이 데이터베이스 레코드를 편리하고 손쉽게 페이지네이션할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만 Bootstrap 페이지네이션도 지원합니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용하는 경우, 애플리케이션의 `tailwind.config.js` 파일 내 `content` 키에 Laravel의 페이지네이션 뷰가 참조되도록 하여 해당 Tailwind 클래스가 제거되지 않도록 해야 합니다.

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

아이템을 페이지네이션하는 방법은 여러 가지가 있습니다. 가장 단순한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 설정합니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 값을 기준으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하고, 페이지네이터가 생성한 링크에 자동으로 삽입됩니다.

이 예시에서는 `paginate` 메서드에 표시하려는 "페이지당" 항목 수만 전달합니다. 이 경우, 한 페이지에 `15`개의 항목을 표시하도록 지정합니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * 모든 애플리케이션 유저 표시.
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

<a name="simple-pagination"></a>
#### 간단 페이지네이션

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리와 일치하는 총 레코드 수를 카운트합니다. 이는 페이지네이터가 전체 페이지 수를 알 수 있도록 하기 위함입니다. 하지만, 애플리케이션 UI에서 전체 페이지 수를 표시할 계획이 없다면 레코드 갯수 쿼리는 불필요합니다.

따라서, 애플리케이션 UI에서 "다음", "이전" 링크만 표시하면 되는 경우, 더 효율적인 단일 쿼리를 수행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

    $users = DB::table('users')->simplePaginate(15);

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리에 대해서도 페이지네이션이 가능합니다. 이 예시에서는 `App\Models\User` 모델을 페이지네이션하고 한 페이지에 15개의 레코드를 표시합니다. 문법은 쿼리 빌더 결과를 페이지네이션할 때와 거의 동일합니다:

    use App\Models\User;

    $users = User::paginate(15);

물론, 쿼리에 `where` 절 등 다른 제약 조건을 설정한 후 `paginate` 메서드를 호출할 수도 있습니다:

    $users = User::where('votes', '>', 100)->paginate(15);

또한, Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

    $users = User::where('votes', '>', 100)->simplePaginate(15);

비슷하게, Eloquent 모델에 대해 `cursorPaginate` 메서드를 사용할 수도 있습니다:

    $users = User::where('votes', '>', 100)->cursorPaginate(15);

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용

하나의 화면에 두 개의 별도 페이지네이터가 표시되어야 할 때가 있습니다. 하지만 두 페이지네이터 인스턴스가 모두 `page` 쿼리 문자열 파라미터를 사용하면 충돌이 발생할 수 있습니다. 이 경우, 원하는 쿼리 문자열 파라미터 이름을 `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인자로 전달하여 충돌을 해결할 수 있습니다:

    use App\Models\User;

    $users = User::where('votes', '>', 100)->paginate(
        $perPage = 15, $columns = ['*'], $pageName = 'users'
    );

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate` 및 `simplePaginate`가 SQL의 "offset" 절을 사용하는 것과 달리, 커서 페이지네이션은 쿼리에서 정렬된 컬럼들의 값을 비교하는 "where" 절을 구성하여, Laravel의 모든 페이지네이션 방식 중 가장 효율적인 데이터베이스 성능을 제공합니다. 이 방식은 대용량 데이터셋과 "무한 스크롤" UI에 특히 적합합니다.

오프셋 기반 페이지네이션과 달리, 커서 기반 페이지네이션은 페이지네이터가 생성한 URL 쿼리 문자열에 페이지 번호 대신 "커서" 문자열이 포함됩니다. 커서는 다음 페이지네이션 쿼리가 시작될 위치와 방향을 담은 인코딩된 문자열입니다.

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 통해 커서 기반 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

    $users = DB::table('users')->orderBy('id')->cursorPaginate(15);

커서 페이지네이터 인스턴스를 가져오면, 일반적인 `paginate`, `simplePaginate`을 사용할 때와 마찬가지로 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터가 제공하는 인스턴스 메서드에 대한 자세한 내용은 [커서 페이지네이터 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> **경고**  
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어 있어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 보여주기 위해 예시 SQL 쿼리를 살펴보겠습니다. 아래 두 쿼리는 모두 `id`로 정렬된 `users` 테이블의 "두 번째 페이지" 결과를 보여줍니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 다음과 같은 이점을 제공합니다:

- 대용량 데이터셋의 경우, "order by" 컬럼이 인덱싱되어 있다면 커서 페이지네이션이 더 나은 성능을 제공합니다. "offset" 절은 이전에 매칭된 모든 데이터를 스캔하기 때문입니다.
- 데이터 삽입/삭제가 빈번한 데이터셋에서 오프셋 페이지네이션은 레코드를 건너뛰거나 중복 표시할 수 있습니다. 커서 방식은 이러한 문제가 적습니다.

하지만 커서 페이지네이션에는 아래와 같은 제한 사항도 있습니다:

- `simplePaginate`처럼 "다음" 및 "이전" 링크만 표시할 수 있으며, 페이지 번호 링크 생성을 지원하지 않습니다.
- 정렬이 최소 하나의 유니크 컬럼(혹은 유니크 조합) 기준이어야 합니다. `null` 값이 있는 컬럼은 지원하지 않습니다.
- "order by" 절의 쿼리 표현식은 별칭(alias) 지정 및 "select" 절에도 추가되어야만 지원됩니다.
- 쿼리 표현식에 파라미터가 들어가는 경우는 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성

이미 메모리에 있는 배열로 페이지네이션 인스턴스를 수동으로 생성해야 할 때가 있습니다. 경우에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 중 하나를 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 전체 아이템 수를 알 필요가 없으나, 따라서 마지막 페이지 인덱스를 가져오는 메서드는 제공하지 않습니다. `LengthAwarePaginator`는 인자 구성이 거의 같지만, 전체 결과 수의 카운트가 필요합니다.

정리하면, `Paginator`는 쿼리 빌더의 `simplePaginate`에, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate`에 각각 대응됩니다.

> **경고**  
> 페이지네이터 인스턴스를 수동으로 생성할 땐 결과 배열을 직접 "슬라이스(slice)" 해서 전달해야 합니다. 방법이 궁금하다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이즈

기본적으로 페이지네이터가 생성한 링크는 현재 요청의 URI를 따릅니다. 하지만 페이지네이터의 `withPath` 메서드를 사용하면 링크 생성 시 사용하는 URI를 커스터마이즈할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 형태의 링크를 생성하도록 하려면 `withPath`에 `/admin/users`를 넘기면 됩니다:

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->withPath('/admin/users');

        //
    });

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가

페이지네이션 링크의 쿼리 문자열에 값을 추가하려면 `appends` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 호출합니다:

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->appends(['sort' => 'votes']);

        //
    });

전체 요청의 쿼리 문자열 값을 모두 링크에 추가하고 싶다면 `withQueryString` 메서드를 사용하세요.

    $users = User::paginate(15)->withQueryString();

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터가 생성한 URL에 "해시 프래그먼트"를 추가해야 하는 경우, `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 붙이고 싶다면 다음과 같이 호출합니다:

    $users = User::paginate(15)->fragment('users');

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드는 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환하고, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 대한 다양한 메서드를 제공합니다. 또한 이 페이지네이터 인스턴스는 배열처럼 반복(iterate)할 수 있어, 결과를 표시하고 [Blade](/docs/{{version}}/blade)에서 페이지 링크를 렌더링할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 다른 페이지로 이동할 수 있는 링크를 렌더링합니다. 각 링크에는 올바른 `page` 쿼리 문자열이 이미 포함되어 있습니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터가 페이지네이션 링크를 표시할 때, 현재 페이지와 이전 3개, 이후 3개의 페이지 링크를 함께 보여줍니다. `onEachSide` 메서드를 사용하면, 가운데 슬라이딩 윈도우 내에서 현재 페이지 양 옆에 몇 개의 추가 링크를 표시할지 제어할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

Laravel 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하고, `toJson` 메서드를 제공하므로 페이지네이션 결과를 쉽게 JSON으로 변환할 수 있습니다. 또한, 페이지네이터 인스턴스를 라우트나 컨트롤러 액션에서 반환하면 자동으로 JSON이 변환됩니다:

    use App\Models\User;

    Route::get('/users', function () {
        return User::paginate();
    });

페이지네이터에서 반환된 JSON에는 `total`, `current_page`, `last_page` 등 메타 정보가 담깁니다. 결과 레코드는 JSON 배열의 `data` 키에 포함됩니다. 아래는 라우트에서 페이지네이터 인스턴스를 반환했을 때 생성되는 예시 JSON입니다:

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
## 페이지네이션 뷰 커스터마이즈

기본적으로, 페이지네이션 링크를 표시하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 하지만 Tailwind를 사용하지 않는 경우, 해당 링크를 렌더링할 커스텀 뷰를 정의할 수 있습니다. 페이지네이터 인스턴스에서 `links` 메서드를 호출할 때 뷰 이름을 첫 번째 인자로 넘기면 됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 쉬운 방법은 `vendor:publish` 명령어로 페이지네이션 뷰를 `resources/views/vendor` 디렉터리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어는 뷰를 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 복사합니다. 이 안의 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당합니다. 이 파일을 수정하여 페이지네이션 HTML을 변경할 수 있습니다.

기본 페이지네이션 뷰 파일을 다른 파일로 지정하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView`, `defaultSimpleView` 메서드를 호출하면 됩니다:

    <?php

    namespace App\Providers;

    use Illuminate\Pagination\Paginator;
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

<a name="using-bootstrap"></a>
### Bootstrap 사용하기

Laravel은 [Bootstrap CSS](https://getbootstrap.com/) 기반의 페이지네이션 뷰도 제공합니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

    use Illuminate\Pagination\Paginator;

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        Paginator::useBootstrapFive();
        Paginator::useBootstrapFour();
    }

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 아래 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

| 메서드 | 설명 |
|--------|------|
| `$paginator->count()` | 현재 페이지에서 보여지는 아이템 수를 반환합니다. |
| `$paginator->currentPage()` | 현재 페이지 번호를 반환합니다. |
| `$paginator->firstItem()` | 결과에서 첫 번째 아이템의 번호를 가져옵니다. |
| `$paginator->getOptions()` | 페이지네이터 옵션을 반환합니다. |
| `$paginator->getUrlRange($start, $end)` | 페이지네이션 URL의 범위를 생성합니다. |
| `$paginator->hasPages()` | 여러 페이지로 나누기에 충분한 아이템이 있는지 확인합니다. |
| `$paginator->hasMorePages()` | 데이터 저장소에 더 많은 아이템이 있는지 확인합니다. |
| `$paginator->items()` | 현재 페이지에 대한 아이템을 반환합니다. |
| `$paginator->lastItem()` | 결과에서 마지막 아이템의 번호를 반환합니다. |
| `$paginator->lastPage()` | 사용 가능한 마지막 페이지의 번호를 반환합니다. (`simplePaginate`에서 사용 불가) |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL을 반환합니다. |
| `$paginator->onFirstPage()` | 현재 페이지가 첫 번째 페이지인지 확인합니다. |
| `$paginator->perPage()` | 페이지당 보여질 아이템 수를 반환합니다. |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 반환합니다. |
| `$paginator->total()` | 데이터 저장소에서 매칭되는 총 아이템 수를 반환합니다. (`simplePaginate`에서 사용 불가) |
| `$paginator->url($page)` | 특정 페이지 번호에 해당하는 URL을 반환합니다. |
| `$paginator->getPageName()` | 현재 페이지 정보를 저장하는 쿼리 문자열 변수명을 반환합니다. |
| `$paginator->setPageName($name)` | 페이지 정보를 저장할 쿼리 문자열 변수명을 설정합니다. |


<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음과 같은 추가적인 페이지네이션 정보를 제공합니다:

| 메서드 | 설명 |
|--------|------|
| `$paginator->count()` | 현재 페이지의 아이템 개수를 반환합니다. |
| `$paginator->cursor()` | 현재 커서 인스턴스를 반환합니다. |
| `$paginator->getOptions()` | 페이지네이터 옵션을 반환합니다. |
| `$paginator->hasPages()` | 여러 페이지로 나누기에 충분한 아이템이 있는지 확인합니다. |
| `$paginator->hasMorePages()` | 데이터 저장소에 더 많은 아이템이 있는지 확인합니다. |
| `$paginator->getCursorName()` | 커서 정보를 저장하는 쿼리 문자열 변수명을 반환합니다. |
| `$paginator->items()` | 현재 페이지의 아이템을 반환합니다. |
| `$paginator->nextCursor()` | 다음 아이템 셋의 커서 인스턴스를 반환합니다. |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL을 반환합니다. |
| `$paginator->onFirstPage()` | 현재 페이지가 첫 번째 페이지인지 확인합니다. |
| `$paginator->onLastPage()` | 현재 페이지가 마지막 페이지인지 확인합니다. |
| `$paginator->perPage()` | 페이지당 보여줄 아이템 수를 반환합니다. |
| `$paginator->previousCursor()` | 이전 아이템 셋의 커서 인스턴스를 반환합니다. |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 반환합니다. |
| `$paginator->setCursorName()` | 커서 정보를 저장할 쿼리 문자열 변수명을 설정합니다. |
| `$paginator->url($cursor)` | 특정 커서 인스턴스에 해당하는 URL을 반환합니다. |