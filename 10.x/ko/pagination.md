# 데이터베이스: 페이지네이션

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 사용자 지정](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이징](#customizing-the-pagination-view)
    - [Bootstrap 사용하기](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지네이션이 매우 복잡할 수 있습니다. Laravel의 페이지네이션 접근 방식이 신선한 공기가 되기를 희망합니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/{{version}}/queries) 및 [Eloquent ORM](/docs/{{version}}/eloquent)과 통합되어 기본 설정 없이도 데이터베이스 레코드를 편리하고 쉽게 페이지네이션할 수 있도록 지원합니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 하지만, Bootstrap 페이지네이션도 지원됩니다.

<a name="tailwind-jit"></a>
#### Tailwind JIT

Laravel의 기본 Tailwind 페이지네이션 뷰와 Tailwind JIT 엔진을 사용하는 경우, 애플리케이션의 `tailwind.config.js` 파일의 `content` 키가 Laravel의 페이지네이션 뷰를 참조하도록 하여 Tailwind 클래스가 제거되지 않도록 해야 합니다:

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

아이템을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries) 또는 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 현재 보고 있는 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 설정합니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 스트링 값에 의해 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

이 예제에서는 `paginate` 메서드에 "한 페이지에 표시할 항목 수"만 인수로 전달합니다. 여기서는 한 페이지에 `15`개의 항목을 표시하도록 지정해 보겠습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
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

<a name="simple-pagination"></a>
#### 단순 페이지네이션

`paginate` 메서드는 쿼리와 일치하는 전체 레코드 수를 먼저 계산한 후, 데이터베이스에서 레코드를 가져옵니다. 이렇게 하면 페이지네이터가 전체 페이지 수를 알 수 있어야 하기 때문입니다. 하지만, 애플리케이션 UI에 전체 페이지 수를 표시할 계획이 없다면, 레코드 개수 쿼리는 불필요합니다.

따라서, 애플리케이션 UI에 "다음"과 "이전" 링크만 간단히 표시하면 되는 경우, 단일 효율적인 쿼리를 수행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

    $users = DB::table('users')->simplePaginate(15);

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이지네이션할 수 있습니다. 이 예제에서는 `App\Models\User` 모델을 페이지네이션하고, 한 페이지에 15개의 레코드를 표시하도록 지정합니다. 보시다시피 쿼리 빌더 결과를 페이지네이션하는 것과 거의 동일한 문법입니다.

    use App\Models\User;

    $users = User::paginate(15);

물론 쿼리에서 `where` 절 등 다른 제약조건을 설정한 후에 `paginate` 메서드를 호출할 수도 있습니다:

    $users = User::where('votes', '>', 100)->paginate(15);

Eloquent 모델을 페이지네이션할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

    $users = User::where('votes', '>', 100)->simplePaginate(15);

비슷하게, Eloquent 모델에서 `cursorPaginate` 메서드를 사용하여 커서 기반 페이지네이션도 사용할 수 있습니다:

    $users = User::where('votes', '>', 100)->cursorPaginate(15);

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스

때때로 한 화면에서 두 개의 다른 페이지네이터를 렌더링해야 할 수도 있습니다. 하지만, 두 페이지네이터 인스턴스가 모두 `page` 쿼리 스트링 파라미터를 사용해 현재 페이지를 저장하면 충돌이 발생합니다. 이 문제를 해결하기 위해, `paginate`, `simplePaginate`, `cursorPaginate` 메서드에 세 번째 인수로 페이지네이터의 현재 페이지를 저장할 쿼리 스트링 파라미터 이름을 전달할 수 있습니다:

    use App\Models\User;

    $users = User::where('votes', '>', 100)->paginate(
        $perPage = 15, $columns = ['*'], $pageName = 'users'
    );

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate`와 `simplePaginate`는 SQL의 "offset" 절을 이용하나, 커서 페이지네이션은 쿼리에서 정렬된 컬럼 값들을 비교하는 "where" 절을 구성하여, Laravel의 모든 페이지네이션 방법 중 가장 효율적인 DB 성능을 제공합니다. 이 방법은 대용량 데이터셋 및 "무한 스크롤" 사용자 인터페이스에 특히 적합합니다.

offset 기반 페이지네이션과 달리, 페이지네이터가 생성하는 URL의 쿼리 스트링에 커서 기반 페이지네이션은 "커서" 문자열을 포함합니다. 커서는 다음 페이지네이팅이 시작되어야 할 위치와 방향을 포함하는 인코딩된 문자열입니다:

```nothing
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 사용해 커서 기반 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

    $users = DB::table('users')->orderBy('id')->cursorPaginate(15);

커서 페이지네이터 인스턴스를 얻었다면, 일반적인 [`paginate`, `simplePaginate` 메서드로 페이지네이션 결과를 표시](#displaying-pagination-results)하듯이 결과를 표시할 수 있습니다. 커서 페이지네이터의 인스턴스 메서드에 대한 자세한 정보는 [cursor paginator 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]  
> 커서 페이지네이션을 사용하려면 쿼리에 "order by" 절이 반드시 포함되어야 하며, 정렬하는 컬럼이 페이지네이션하는 테이블에 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 예로 들어 설명하겠습니다. 아래 두 SQL 쿼리는 둘 다 `users` 테이블의 "id"로 정렬된 두 번째 페이지의 결과를 표시합니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션의 장점은 다음과 같습니다:

- 대용량 데이터셋에서 "order by" 컬럼에 인덱스가 있다면 더 좋은 성능을 기대할 수 있습니다. 이는 "offset" 절이 이전에 일치한 모든 데이터를 스캔하기 때문입니다.
- 데이터셋에 쓰기 작업이 자주 일어날 경우, 오프셋 페이지네이션에서는 한 사용자가 보고 있는 페이지에 결과가 추가되거나 삭제되면 레코드를 건너뛰거나 중복 표시할 수 있습니다.

하지만 커서 페이지네이션에는 아래와 같은 제한이 있습니다:

- `simplePaginate`처럼, 커서 페이지네이션은 "다음" 및 "이전" 링크만 생성할 수 있으며, 페이지 번호 링크 생성을 지원하지 않습니다.
- 정렬 기준이 반드시 하나 이상의 유니크 컬럼이거나 조합이어야 합니다. `null` 값이 있는 컬럼은 지원하지 않습니다.
- "order by" 절의 쿼리 표현식은 별칭이 부여되어 "select" 절에도 추가된 경우에만 지원됩니다.
- 파라미터가 있는 쿼리 표현식은 지원되지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성

경우에 따라, 이미 메모리에 있는 배열을 사용하여 직접 페이지네이션 인스턴스를 생성하고 싶을 수 있습니다. 이럴 경우 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스 중 하나를 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 전체 아이템 수를 알 필요가 없지만, 그렇기 때문에 마지막 페이지 인덱스를 가져오는 메서드는 없습니다. 반면 `LengthAwarePaginator`는 전체 아이템 수를 필요로 하며, 거의 동일한 인수를 받습니다.

정리하면, `Paginator`는 쿼리 빌더의 `simplePaginate`와, `CursorPaginator`는 `cursorPaginate`와, `LengthAwarePaginator`는 `paginate`와 각각 대응됩니다.

> [!WARNING]  
> 페이지네이터 인스턴스를 직접 생성할 때는, 직접 전달할 배열을 "슬라이스(slicing)"해야 합니다. 방법이 궁금하다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 사용자 지정

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 하지만, 페이지네이터의 `withPath` 메서드를 활용하면 페이지네이터가 링크 생성 시 사용할 URI를 사용자 지정할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 형태의 링크를 생성하게 하려면 `/admin/users`를 `withPath` 메서드에 전달하면 됩니다:

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->withPath('/admin/users');

        // ...
    });

<a name="appending-query-string-values"></a>
#### 쿼리 스트링 값 추가

`appends` 메서드를 사용하여 페이지네이션 링크의 쿼리 스트링에 값을 추가할 수 있습니다. 예를 들어 `sort=votes`를 각 페이지네이션 링크에 추가하고 싶다면 다음과 같이 호출합니다:

    use App\Models\User;

    Route::get('/users', function () {
        $users = User::paginate(15);

        $users->appends(['sort' => 'votes']);

        // ...
    });

현재 요청의 모든 쿼리 스트링 값을 페이지네이션 링크에 추가하려면 `withQueryString` 메서드를 사용할 수 있습니다:

    $users = User::paginate(15)->withQueryString();

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 추가해야 하는 경우 `fragment` 메서드를 사용할 수 있습니다. 예를 들어 각 링크 끝에 `#users`를 추가하려면 다음과 같이 호출하세요:

    $users = User::paginate(15)->fragment('users');

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스가 반환되고, `simplePaginate`는 `Illuminate\Pagination\Paginator`, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 셋에 대한 여러 메서드를 제공합니다. 이러한 헬퍼 메서드 외에도, 페이지네이터 인스턴스는 반복자(iterators)로 동작해 배열처럼 루프를 돌릴 수 있습니다. 따라서 결과를 받아온 후, [Blade](/docs/{{version}}/blade)를 사용하여 결과와 페이지 링크를 이렇게 표시할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 셋의 나머지 페이지에 대한 링크를 렌더링합니다. 각각의 링크에는 이미 적절한 `page` 쿼리 스트링 변수가 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터가 링크를 표시할 때, 현재 페이지를 중심으로 앞뒤로 3개 정도의 페이지 번호 링크를 표시합니다. `onEachSide` 메서드를 사용하면, 페이지네이터가 생성하는 중간 슬라이딩 윈도우 내에서 현재 페이지 양쪽에 표시할 추가 링크 수를 조정할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel의 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하고 있으며, `toJson` 메서드를 노출하므로, 페이지네이션 결과를 아주 쉽게 JSON으로 변환할 수 있습니다. 라우트나 컨트롤러 액션에서 페이지네이터 인스턴스를 반환하면 자동으로 JSON으로 변환됩니다:

    use App\Models\User;

    Route::get('/users', function () {
        return User::paginate();
    });

페이지네이터의 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함됩니다. 결과 레코드들은 JSON 배열의 `data` 키를 통해 제공됩니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환할 때 만들어지는 JSON 예시입니다:

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

기본적으로 페이지네이션 링크를 표시하기 위해 렌더링되는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. Tailwind를 사용하지 않는다면, 직접 뷰 파일을 정의하여 링크 렌더링 방법을 바꿀 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드에 뷰 이름을 첫 번째 인수로 전달할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달도 가능... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 가장 간편하게 페이지네이션 뷰를 커스터마이징하는 방법은, `vendor:publish` 명령으로 뷰를 `resources/views/vendor` 디렉터리로 내보내서 수정하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령을 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 뷰 파일들이 생성됩니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 대응합니다. 이 파일을 수정하여 HTML을 변경할 수 있습니다.

기본 페이지네이션 뷰 파일을 변경하려면, 앱의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하면 됩니다:

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

<a name="using-bootstrap"></a>
### Bootstrap 사용하기

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)로 제작된 페이지네이션 뷰도 제공합니다. 기본 Tailwind 뷰 대신 이 뷰를 사용하려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하면 됩니다:

    use Illuminate\Pagination\Paginator;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Paginator::useBootstrapFive();
        Paginator::useBootstrapFour();
    }

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다.

| 메서드  | 설명 |
| ------- | ---------------------------------------------------- |
| `$paginator->count()`  | 현재 페이지의 항목 개수를 반환합니다. |
| `$paginator->currentPage()`  | 현재 페이지 번호를 반환합니다. |
| `$paginator->firstItem()`  | 결과 중 첫 번째 아이템의 인덱스를 반환합니다. |
| `$paginator->getOptions()`  | 페이지네이터 옵션을 반환합니다. |
| `$paginator->getUrlRange($start, $end)`  | 페이지네이션 URL 범위를 생성합니다. |
| `$paginator->hasPages()`  | 여러 페이지로 나눌 충분한 항목이 있는지 확인합니다. |
| `$paginator->hasMorePages()`  | 데이터 저장소에 더 많은 항목이 있는지 확인합니다. |
| `$paginator->items()`  | 현재 페이지의 항목을 반환합니다. |
| `$paginator->lastItem()`  | 결과 중 마지막 항목의 인덱스를 반환합니다. |
| `$paginator->lastPage()`  | 마지막 페이지 번호를 반환합니다. (`simplePaginate`에서는 사용 불가) |
| `$paginator->nextPageUrl()`  | 다음 페이지의 URL을 반환합니다. |
| `$paginator->onFirstPage()`  | 페이지네이터가 첫 번째 페이지에 있는지 확인합니다. |
| `$paginator->perPage()`  | 한 페이지에 표시할 항목 수를 반환합니다. |
| `$paginator->previousPageUrl()`  | 이전 페이지의 URL을 반환합니다. |
| `$paginator->total()`  | 데이터 저장소에 일치하는 항목 총 개수를 반환합니다. (`simplePaginate`에서는 사용 불가) |
| `$paginator->url($page)`  | 지정된 페이지 번호의 URL을 반환합니다. |
| `$paginator->getPageName()`  | 페이지를 저장하는 쿼리 스트링 변수 이름을 반환합니다. |
| `$paginator->setPageName($name)`  | 페이지를 저장하는 쿼리 스트링 변수 이름을 설정합니다. |
| `$paginator->through($callback)`  | 콜백을 이용해 각각의 아이템을 변환합니다. |

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음과 같은 메서드로 추가적인 정보를 제공합니다.

| 메서드  | 설명 |
| ------- | ---------------------------------------------------- |
| `$paginator->count()`  | 현재 페이지의 항목 개수를 반환합니다. |
| `$paginator->cursor()`  | 현재 커서 인스턴스를 반환합니다. |
| `$paginator->getOptions()`  | 페이지네이터 옵션을 반환합니다. |
| `$paginator->hasPages()`  | 여러 페이지로 나눌 충분한 항목이 있는지 확인합니다. |
| `$paginator->hasMorePages()`  | 데이터 저장소에 더 많은 항목이 있는지 확인합니다. |
| `$paginator->getCursorName()`  | 커서를 저장하는 쿼리 스트링 변수 이름을 반환합니다. |
| `$paginator->items()`  | 현재 페이지의 항목들을 반환합니다. |
| `$paginator->nextCursor()`  | 다음 아이템 집합의 커서 인스턴스를 반환합니다. |
| `$paginator->nextPageUrl()`  | 다음 페이지의 URL을 반환합니다. |
| `$paginator->onFirstPage()`  | 페이지네이터가 첫 번째 페이지에 있는지 확인합니다. |
| `$paginator->onLastPage()`  | 페이지네이터가 마지막 페이지에 있는지 확인합니다. |
| `$paginator->perPage()`  | 한 페이지에 표시할 항목 개수를 반환합니다. |
| `$paginator->previousCursor()`  | 이전 아이템 집합의 커서 인스턴스를 반환합니다. |
| `$paginator->previousPageUrl()`  | 이전 페이지의 URL을 반환합니다. |
| `$paginator->setCursorName()`  | 커서를 저장하는 쿼리 스트링 변수 이름을 설정합니다. |
| `$paginator->url($cursor)`  | 지정된 커서 인스턴스의 URL을 반환합니다. |