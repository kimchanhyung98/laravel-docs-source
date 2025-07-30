# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계](#aggregates)
- [선택문](#select-statements)
- [원시 표현식](#raw-expressions)
- [조인](#joins)
- [유니언](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All 절](#where-any-all-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전체 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한과 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [삽입문](#insert-statements)
    - [업서트](#upserts)
- [수정문](#update-statements)
    - [JSON 컬럼 수정](#updating-json-columns)
    - [증가와 감소](#increment-and-decrement)
- [삭제문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 편리하고 유창한 인터페이스를 제공하여 데이터베이스 쿼리를 작성하고 실행할 수 있게 합니다. 애플리케이션에서 대부분의 데이터베이스 작업에 사용할 수 있고, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽히 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 쿼리 바인딩으로 전달하는 문자열을 따로 정리하거나 검증할 필요가 없습니다.

> [!WARNING]  
> PDO는 컬럼명을 바인딩하는 것을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조되는 컬럼명(예: "order by" 컬럼)을 결정하도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드에서 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table`은 지정한 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하며, 이를 통해 쿼리에 여러 조건을 체인으로 추가한 뒤, `get` 메서드를 사용하여 쿼리 결과를 받을 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 표시합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 컬렉션 내 각 결과는 PHP의 `stdClass` 객체 인스턴스입니다. 각 컬럼 값은 객체의 속성으로 접근할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]  
> Laravel 컬렉션은 데이터를 매핑하거나 축소하는 데 매우 강력한 다양한 메서드를 제공합니다. 보다 자세한 내용은 [컬렉션 문서](/docs/10.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 한 행 또는 한 컬럼 값 조회하기

데이터베이스 테이블에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

전체 행이 필요하지 않고 컬럼의 단일 값만 추출하려면 `value` 메서드를 사용하세요. 이 메서드는 컬럼 값을 직접 반환합니다:

```
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 특정 컬럼 값 목록 조회하기

특정 컬럼 값만 담긴 `Illuminate\Support\Collection` 인스턴스를 얻으려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예제는 사용자들의 `title` 컬렉션을 조회합니다:

```
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인수로 키용 컬럼을 지정하여, 컬렉션의 키로 사용할 컬럼을 지정할 수도 있습니다:

```
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개의 데이터 레코드와 작업할 때는 `DB` 파사드에서 제공하는 `chunk` 메서드 사용을 고려하세요. 이 메서드는 한 번에 적은 양의 결과를 불러와 클로저에 전달해 처리할 수 있습니다. 예를 들어, `users` 테이블 전체를 100개씩 청크 단위로 조회할 수 있습니다:

```
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 더 이상의 청크 처리를 중단할 수 있습니다:

```
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리하는 동안 데이터베이스 레코드를 변경하는 경우, 청크 결과가 예상치 못하게 변할 수 있습니다. 그래서 레코드를 업데이트할 경우에는 항상 `chunkById` 메서드 사용을 권장합니다. 이 메서드는 기본 키를 기준으로 자동으로 페이지네이션합니다:

```
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

> [!WARNING]  
> 청크 콜백에서 레코드를 수정하거나 삭제할 때, 기본 키나 외래 키의 변경이 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기

`lazy` 메서드는 [`chunk` 메서드](#chunking-results)처럼 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백에 전달하는 대신 [`LazyCollection`](/docs/10.x/collections#lazy-collections)을 반환하여 결과를 하나의 스트림처럼 처리할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

청크 처리와 마찬가지로, 내부의 레코드를 수정할 경우 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드들은 기본 키를 기준으로 자동 페이지네이션을 수행합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]  
> 반복 처리 중에 레코드를 수정하거나 삭제할 경우, 기본 키나 외래 키 변화가 쿼리에 영향을 주어 일부 결과가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 메서드를 제공합니다. 쿼리를 구성한 후 원하는 집계 메서드를 호출하세요:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 절과 결합해 집계 결과를 더욱 정교하게 조정할 수 있습니다:

```
$price = DB::table('orders')
                ->where('finalized', 1)
                ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

`count` 메서드를 사용해 조건에 맞는 레코드가 존재하는지 확인하는 대신, `exists`와 `doesntExist` 메서드를 사용할 수 있습니다:

```
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## 선택문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정하기

항상 모든 컬럼을 선택하는 게 아닐 수 있습니다. `select` 메서드를 사용하면 쿼리의 커스텀 "select" 절을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->select('name', 'email as user_email')
            ->get();
```

`distinct` 메서드를 사용하면 중복 없는 결과만 반환할 수 있습니다:

```
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고 여기에 컬럼을 추가해서 기존 select 절에 더하고 싶으면 `addSelect` 메서드를 사용하세요:

```
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 (Raw Expressions)

쿼리에 임의의 문자열을 삽입할 필요가 있을 때는 `DB` 파사드의 `raw` 메서드를 사용해 원시 표현식을 만들 수 있습니다:

```
$users = DB::table('users')
             ->select(DB::raw('count(*) as user_count, status'))
             ->where('status', '<>', 1)
             ->groupBy('status')
             ->get();
```

> [!WARNING]  
> 원시 표현식은 쿼리에 문자열로 직접 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드

`DB::raw` 메서드 대신 다음 메서드들을 사용해 쿼리 각 부분에 원시 표현식을 삽입할 수 있습니다. **다만, 원시 표현식이 포함된 쿼리는 Laravel이 SQL 인젝션 방어를 보장하지 못함을 꼭 유념하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))`를 대신해 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 선택적으로 받을 수 있습니다:

```
$orders = DB::table('orders')
                ->selectRaw('price * ? as price_with_tax', [1.0825])
                ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw`는 원시 "where" 절을 쿼리에 삽입할 때 사용합니다. 두 메서드 역시 바인딩 배열을 두 번째 인수로 받을 수 있습니다:

```
$orders = DB::table('orders')
                ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절의 원시 문자열 값을 지정할 때 사용합니다. 선택적으로 바인딩 배열을 두 번째 인수로 전달할 수 있습니다:

```
$orders = DB::table('orders')
                ->select('department', DB::raw('SUM(price) as total_sales'))
                ->groupBy('department')
                ->havingRaw('SUM(price) > ?', [2500])
                ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 원시 문자열을 제공할 때 사용합니다:

```
$orders = DB::table('orders')
                ->orderByRaw('updated_at - created_at DESC')
                ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 원시 문자열을 제공할 때 사용합니다:

```
$orders = DB::table('orders')
                ->select('city', 'state')
                ->groupByRaw('city, state')
                ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 (Inner Join) 절

쿼리 빌더로 조인 절을 추가할 수 있습니다. 기본적인 내부 조인은 `join` 메서드를 사용합니다. 첫 번째 인자는 조인할 대상 테이블명이고, 그 다음 인자들은 조인 조건에 관련된 컬럼들입니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->join('contacts', 'users.id', '=', 'contacts.user_id')
            ->join('orders', 'users.id', '=', 'orders.user_id')
            ->select('users.*', 'contacts.phone', 'orders.price')
            ->get();
```

<a name="left-join-right-join-clause"></a>
#### 왼쪽 조인 / 오른쪽 조인 절

내부 조인 대신 "left join"이나 "right join"을 수행하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 사용법은 `join`과 동일합니다:

```
$users = DB::table('users')
            ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();

$users = DB::table('users')
            ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 절

`crossJoin` 메서드를 사용하면 "크로스 조인"을 수행할 수 있습니다. 크로스 조인은 첫 번째 테이블과 조인 대상 테이블 사이의 카테시안 곱을 생성합니다:

```
$sizes = DB::table('sizes')
            ->crossJoin('colors')
            ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 조건을 지정하려면 `join` 메서드의 두번째 인수로 클로저를 전달하세요. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받으며, 조인 절에 조건을 지정할 수 있습니다:

```
DB::table('users')
        ->join('contacts', function (JoinClause $join) {
            $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
        })
        ->get();
```

조인에 "where" 절을 추가하고 싶으면 `JoinClause` 인스턴스가 제공하는 `where`와 `orWhere` 메서드를 사용할 수 있습니다. 이때 두 컬럼 비교 대신 특정 값을 기준으로 비교합니다:

```
DB::table('users')
        ->join('contacts', function (JoinClause $join) {
            $join->on('users.id', '=', 'contacts.user_id')
                 ->where('contacts.user_id', '>', 5);
        })
        ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 서브쿼리를 조인할 수 있습니다. 이들은 세 개의 인수를 받는데, 서브쿼리, 그 별칭, 그리고 관련 컬럼을 정의하는 클로저입니다. 다음 예제는 각 사용자 레코드에 해당 사용자의 가장 최근 게시글의 `created_at` 타임스탬프를 포함합니다:

```
$latestPosts = DB::table('posts')
                   ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                   ->where('is_published', true)
                   ->groupBy('user_id');

$users = DB::table('users')
        ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
            $join->on('users.id', '=', 'latest_posts.user_id');
        })->get();
```

<a name="lateral-joins"></a>
#### 래터럴 조인 (Lateral Joins)

> [!WARNING]  
> 래터럴 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral`과 `leftJoinLateral` 메서드를 사용해 서브쿼리와 "래터럴 조인"을 수행할 수 있습니다. 두 인수는 서브쿼리와 별칭입니다. 조인 조건은 서브쿼리 내부의 `where` 절 내에서 지정합니다. 래터럴 조인은 각 행마다 평가되며 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

아래 예시는 사용자 목록과 각 사용자의 최근 3개 게시글을 가져오는 방법입니다. 사용자당 최대 3개의 행이 결과에 포함될 수 있습니다. 조인 조건은 서브쿼리 내부의 `whereColumn` 절로 현재 사용자 행을 참조합니다:

```
$latestPosts = DB::table('posts')
                   ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
                   ->whereColumn('user_id', 'users.id')
                   ->orderBy('created_at', 'desc')
                   ->limit(3);

$users = DB::table('users')
            ->joinLateral($latestPosts, 'latest_posts')
            ->get();
```

<a name="unions"></a>
## 유니언 (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "union" 하는 편리한 메서드를 제공합니다. 예를 들어, 초기 쿼리를 만든 뒤 `union` 메서드로 다른 쿼리와 합칠 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
            ->whereNull('first_name');

$users = DB::table('users')
            ->whereNull('last_name')
            ->union($first)
            ->get();
```

`union` 외에 `unionAll` 메서드도 있습니다. 이 메서드는 중복 결과를 제거하지 않고 모두 포함하는 쿼리를 만듭니다. 메서드 시그니처는 `union`과 같습니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드로 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 호출에는 세 개의 인수가 필요합니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스가 지원하는 모든 연산자 사용 가능), 세 번째는 비교할 값입니다.

예를 들어, `votes` 컬럼 값이 `100`이고 `age` 컬럼 값이 `35`보다 큰 사용자들을 조회하는 쿼리는 다음과 같습니다:

```
$users = DB::table('users')
                ->where('votes', '=', 100)
                ->where('age', '>', 35)
                ->get();
```

편의를 위해, 어떤 컬럼이 특정 값과 같음을 확인할 때는 두 번째 인자만 넘겨도 됩니다. 이 경우 Laravel은 `=` 연산자를 사용한다고 가정합니다:

```
$users = DB::table('users')->where('votes', 100)->get();
```

다음과 같이 데이터베이스가 지원하는 모든 연산자도 사용할 수 있습니다:

```
$users = DB::table('users')
                ->where('votes', '>=', 100)
                ->get();

$users = DB::table('users')
                ->where('votes', '<>', 100)
                ->get();

$users = DB::table('users')
                ->where('name', 'like', 'T%')
                ->get();
```

조건 배열을 `where` 메서드에 전달할 수도 있습니다. 배열의 각 요소는 `where`에 전달할 세 인수로 이루어진 배열이어야 합니다:

```
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]  
> PDO는 컬럼명에 대한 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에 참조되는 컬럼명을 결정하지 않도록 반드시 주의하세요.

<a name="or-where-clauses"></a>
### Or Where 절

여러 개의 `where` 메서드를 체인으로 연결하면 기본적으로 각 Where 절은 `and`로 연결됩니다. 하지만 `orWhere` 메서드를 사용하면 `or` 연산자로 조건을 연결할 수 있습니다. `orWhere`는 `where`와 동일한 인자를 받습니다:

```
$users = DB::table('users')
                    ->where('votes', '>', 100)
                    ->orWhere('name', 'John')
                    ->get();
```

"or" 조건을 괄호로 묶는 그룹으로 만들고 싶다면 `orWhere` 첫 번째 인자로 클로저를 전달하세요:

```
$users = DB::table('users')
            ->where('votes', '>', 100)
            ->orWhere(function (Builder $query) {
                $query->where('name', 'Abigail')
                      ->where('votes', '>', 50);
            })
            ->get();
```

위 예제는 다음 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]  
> `orWhere` 호출은 항상 괄호로 그룹화해, 글로벌 범위(global scopes)가 적용됐을 때 의도하지 않은 동작을 방지해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`, `orWhereNot` 메서드로 쿼리 제약 조건을 부정할 수 있습니다. 예를 들어, 클리어런스 중인 상품이나 가격이 10 미만인 상품을 쿼리에서 제외할 수 있습니다:

```
$products = DB::table('products')
                ->whereNot(function (Builder $query) {
                    $query->where('clearance', true)
                          ->orWhere('price', '<', 10);
                })
                ->get();
```

<a name="where-any-all-clauses"></a>
### Where Any / All 절

여러 컬럼에 동일한 조건을 적용해야 할 때가 있습니다. 예를 들어, 특정 컬럼들 중 하나라도 특정 값과 `LIKE` 조건에 맞는 레코드를 조회할 수 있습니다. `whereAny` 메서드를 사용해 구현할 수 있습니다:

```
$users = DB::table('users')
            ->where('active', true)
            ->whereAny([
                'name',
                'email',
                'phone',
            ], 'LIKE', 'Example%')
            ->get();
```

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

반대로, 모든 컬럼이 조건을 만족하는 레코드를 조회하려면 `whereAll` 메서드를 사용하세요:

```
$posts = DB::table('posts')
            ->where('published', true)
            ->whereAll([
                'title',
                'content',
            ], 'LIKE', '%Laravel%')
            ->get();
```

해당 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

<a name="json-where-clauses"></a>
### JSON Where 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼을 쿼리하는 기능을 제공합니다. 지원 데이터베이스는 MySQL 5.7+, PostgreSQL, SQL Server 2016+, SQLite 3.39.0 이상(와 [JSON1 확장](https://www.sqlite.org/json1.html))입니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용하세요:

```
$users = DB::table('users')
                ->where('preferences->dining->meal', 'salad')
                ->get();
```

`whereJsonContains`는 JSON 배열 내 값 포함 여부를 조회할 때 사용합니다:

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', 'en')
                ->get();
```

MySQL과 PostgreSQL을 사용하는 경우, 배열을 전달해 여러 값을 포함하는지 조회할 수도 있습니다:

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', ['en', 'de'])
                ->get();
```

JSON 배열의 길이로 조회하려면 `whereJsonLength` 메서드를 사용하세요:

```
$users = DB::table('users')
                ->whereJsonLength('options->languages', 0)
                ->get();

$users = DB::table('users')
                ->whereJsonLength('options->languages', '>', 1)
                ->get();
```

<a name="additional-where-clauses"></a>
### 추가 Where 절

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 특정 두 값 사이에 있는지 확인합니다:

```
$users = DB::table('users')
           ->whereBetween('votes', [1, 100])
           ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 특정 두 값 범위 밖에 있는지 확인합니다:

```
$users = DB::table('users')
                    ->whereNotBetween('votes', [1, 100])
                    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 한 컬럼 값이 같은 행 내 두 컬럼 값 사이에 있는지 검사합니다:

```
$patients = DB::table('patients')
                       ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

`whereNotBetweenColumns`는 한 컬럼 값이 두 컬럼 값 범위를 벗어나는지 검사합니다:

```
$patients = DB::table('patients')
                       ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 주어진 배열에 포함되는지 확인합니다:

```
$users = DB::table('users')
                    ->whereIn('id', [1, 2, 3])
                    ->get();
```

`whereNotIn`은 컬럼 값이 배열에 포함되지 않는지 확인합니다:

```
$users = DB::table('users')
                    ->whereNotIn('id', [1, 2, 3])
                    ->get();
```

두 번째 인수에 쿼리 객체를 전달할 수도 있습니다:

```
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
                    ->whereIn('user_id', $activeUsers)
                    ->get();
```

위 예제는 다음 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]  
> 대량의 정수 바인딩 배열을 쿼리에 추가하는 경우 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인지 확인합니다:

```
$users = DB::table('users')
                ->whereNull('updated_at')
                ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아닌지 확인합니다:

```
$users = DB::table('users')
                ->whereNotNull('updated_at')
                ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값을 특정 날짜와 비교할 때 사용합니다:

```
$users = DB::table('users')
                ->whereDate('created_at', '2016-12-31')
                ->get();
```

`whereMonth`는 월 단위 비교에 사용합니다:

```
$users = DB::table('users')
                ->whereMonth('created_at', '12')
                ->get();
```

`whereDay`는 특정 일 단위 비교에 사용합니다:

```
$users = DB::table('users')
                ->whereDay('created_at', '31')
                ->get();
```

`whereYear`는 연 단위 비교에 사용합니다:

```
$users = DB::table('users')
                ->whereYear('created_at', '2016')
                ->get();
```

`whereTime`은 시간 단위 비교에 사용하며, 날짜는 제외합니다:

```
$users = DB::table('users')
                ->whereTime('created_at', '=', '11:20:45')
                ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼의 값이 같은지 확인합니다:

```
$users = DB::table('users')
                ->whereColumn('first_name', 'last_name')
                ->get();
```

비교 연산자를 지정할 수도 있습니다:

```
$users = DB::table('users')
                ->whereColumn('updated_at', '>', 'created_at')
                ->get();
```

또는 배열로 여러 컬럼 비교 조건을 지정할 수도 있으며, 이 조건들은 `and`로 연결됩니다:

```
$users = DB::table('users')
                ->whereColumn([
                    ['first_name', '=', 'last_name'],
                    ['updated_at', '>', 'created_at'],
                ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

쿼리에서 여러 "where" 절을 괄호로 묶어서 쿼리의 논리적 우선순위를 조절할 필요가 있습니다. 특히 `orWhere`를 사용할 때는 쿼리가 예상과 다르게 작동하지 않도록 항상 괄호로 그룹화하는 것이 좋습니다.

`where` 메서드에 클로저를 넘겨 그룹화할 수 있습니다:

```
$users = DB::table('users')
           ->where('name', '=', 'John')
           ->where(function (Builder $query) {
               $query->where('votes', '>', 100)
                     ->orWhere('title', '=', 'Admin');
           })
           ->get();
```

위 코드는 다음 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]  
> 글로벌 범위(global scopes)를 적용할 때 의도치 않은 동작을 방지하려면 `orWhere` 호출을 항상 그룹화하세요.

<a name="advanced-where-clauses"></a>
### 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. `whereExists`는 클로저를 받아, 쿼리 빌더 인스턴스를 주어 "exists" 절 내부에 들어갈 쿼리를 정의하게 합니다:

```
$users = DB::table('users')
           ->whereExists(function (Builder $query) {
               $query->select(DB::raw(1))
                     ->from('orders')
                     ->whereColumn('orders.user_id', 'users.id');
           })
           ->get();
```

또는 클로저 대신 쿼리 객체를 넘길 수도 있습니다:

```
$orders = DB::table('orders')
                ->select(DB::raw(1))
                ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
                    ->whereExists($orders)
                    ->get();
```

두 예제 모두 다음 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 절

서브쿼리 결과를 특정 값과 비교하는 "where" 절을 작성하는 경우, `where` 메서드에 클로저와 비교 값을 넘기면 됩니다. 예를 들어, 최근에 특정 타입의 "membership"이 있는 사용자를 조회할 수 있습니다:

```
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

또는 컬럼과 비교 연산자, 클로저를 넘겨 컬럼과 서브쿼리 결과를 비교할 수도 있습니다. 아래 예시는 평균보다 작은 소득 기록을 조회합니다:

```
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전체 텍스트 Where 절

> [!WARNING]  
> 전체 텍스트 Where 절은 현재 MySQL과 PostgreSQL에서 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드로 [전체 텍스트 인덱스](/docs/10.x/migrations#available-index-types)가 설정된 컬럼에 대해 전체 텍스트 검색 조건을 추가할 수 있습니다. 이 메서드들은 사용중인 데이터베이스에 맞는 적절한 SQL로 변환됩니다. 예를 들어 MySQL에서는 `MATCH AGAINST` 절이 생성됩니다:

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드로 쿼리 결과를 특정 컬럼 기준으로 정렬할 수 있습니다. 첫 번째 인자가 정렬할 컬럼명이고, 두 번째 인자는 `asc` 또는 `desc` 방향입니다:

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->get();
```

여러 컬럼으로 정렬하려면 필요한 만큼 `orderBy`를 연속 호출하면 됩니다:

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->orderBy('email', 'asc')
                ->get();
```

<a name="latest-oldest"></a>
#### `latest`와 `oldest` 메서드

`latest`와 `oldest` 메서드로 날짜 컬럼 기준 간편 정렬이 가능합니다. 기본적으로 `created_at` 기준 정렬하며, 원하는 컬럼명을 전달할 수도 있습니다:

```
$user = DB::table('users')
                ->latest()
                ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용해 무작위로 정렬할 수 있습니다. 이를 활용해 랜덤 사용자 하나를 조회할 수 있습니다:

```
$randomUser = DB::table('users')
                ->inRandomOrder()
                ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거하기

`reorder` 메서드는 기존에 적용된 모든 "order by" 절을 제거합니다:

```
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder`에 컬럼명과 방향을 전달하면 기존 정렬을 제거하고 새 정렬을 적용합니다:

```
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy`와 `having` 메서드

`groupBy`와 `having` 메서드로 쿼리 결과를 그룹화할 수 있습니다. `having`은 `where`과 유사한 시그니처를 가집니다:

```
$users = DB::table('users')
                ->groupBy('account_id')
                ->having('account_id', '>', 100)
                ->get();
```

`havingBetween`을 통해 특정 범위 내 조건으로 결과를 필터링할 수도 있습니다:

```
$report = DB::table('orders')
                ->selectRaw('count(id) as number_of_orders, customer_id')
                ->groupBy('customer_id')
                ->havingBetween('number_of_orders', [5, 15])
                ->get();
```

`groupBy`에 여러 컬럼을 넣어 다중 그룹화를 수행할 수도 있습니다:

```
$users = DB::table('users')
                ->groupBy('first_name', 'status')
                ->having('account_id', '>', 100)
                ->get();
```

복잡한 `having` 조건은 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 제한과 오프셋

<a name="skip-take"></a>
#### `skip`과 `take` 메서드

`skip`과 `take` 메서드로 쿼리 결과의 조회 개수를 제한하거나 처음 몇 개 결과를 건너뛸 수 있습니다:

```
$users = DB::table('users')->skip(10)->take(5)->get();
```

동일한 기능을 하는 `limit`과 `offset` 메서드도 있습니다:

```
$users = DB::table('users')
                ->offset(10)
                ->limit(5)
                ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

가령 HTTP 요청에 특정 값이 포함됐을 때만 `where` 절을 적용하는 등, 조건에 따라 쿼리 조건절을 적용하고 싶을 때 `when` 메서드를 사용합니다:

```
$role = $request->string('role');

$users = DB::table('users')
                ->when($role, function (Builder $query, string $role) {
                    $query->where('role_id', $role);
                })
                ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 클로저를 실행합니다. 위 예는 요청에 `role` 값이 있을 때만 조건을 적용합니다.

`when`에 세 번째 인수로 또 다른 클로저를 전달하면, 첫 번째 인수가 `false`일 때 대신 실행합니다. 아래 예는 조건에 따라 정렬 기준을 다르게 설정하는 예입니다:

```
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
                ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
                    $query->orderBy('votes');
                }, function (Builder $query) {
                    $query->orderBy('name');
                })
                ->get();
```

<a name="insert-statements"></a>
## 삽입문 (Insert Statements)

쿼리 빌더의 `insert` 메서드는 테이블에 레코드를 삽입합니다. 컬럼명과 값의 배열을 인수로 받습니다:

```
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열 배열을 전달하세요. 각 배열은 삽입할 한 레코드를 의미합니다:

```
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 도중 발생하는 오류를 무시합니다. 중복 레코드 오류뿐 아니라 데이터베이스 엔진에 따라 기타 오류도 무시될 수 있습니다. 예를 들어 MySQL에서는 [엄격 모드가 우회됩니다](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution):

```
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리를 사용하여 삽입할 데이터를 결정하면서 새 레코드를 삽입하는 방법입니다:

```
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있을 경우, `insertGetId`를 사용해 레코드를 삽입하고 ID를 즉시 받아올 수 있습니다:

```
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]  
> PostgreSQL에서는 `insertGetId`가 자동 증가 컬럼명을 `id`로 기대합니다. 다른 시퀀스에서 ID를 받아오려면 두 번째 인수로 해당 컬럼명을 넘기세요.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 존재하는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인자는 삽입 또는 업데이트할 값, 두 번째 인자는 테이블 내에서 레코드를 고유하게 식별하는 컬럼 리스트, 세 번째 인자는 기존 레코드가 있으면 업데이트할 컬럼 리스트입니다:

```
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

위 예제는 두 레코드를 삽입하되, 같은 `departure`와 `destination` 값이 이미 있으면 해당 레코드의 `price` 컬럼만 업데이트합니다.

> [!WARNING]  
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드 두 번째 인수에 전달하는 컬럼들에 "기본키" 또는 "유니크" 인덱스가 있어야 합니다. 또한 MySQL 드라이버는 이 인수를 무시하고 테이블의 기본키와 유니크 인덱스를 항상 사용합니다.

<a name="update-statements"></a>
## 수정문 (Update Statements)

쿼리 빌더는 기존 레코드를 수정하는 데 `update` 메서드를 제공합니다. 이 메서드는 업데이트할 컬럼과 값을 배열로 받으며, 영향받은 행 개수를 반환합니다. `where` 절로 쿼리를 제한할 수 있습니다:

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 수정 또는 삽입 (Update or Insert)

기존 레코드가 있으면 수정하고, 없으면 새로 삽입하고 싶을 때 `updateOrInsert` 메서드를 사용합니다. 이 메서드는 찾기 위한 조건 배열과 업데이트할 값 배열 두 개를 받습니다.

존재하는 레코드를 찾으면 두 번째 인수의 값으로 수정하며, 없다면 두 인수의 값들을 합쳐 새 레코드를 만듭니다:

```
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<a name="updating-json-columns"></a>
### JSON 컬럼 수정하기

JSON 컬럼을 수정할 때는 `->` 문법을 사용해 JSON 객체 내 특정 키를 지정하세요. 이 기능은 MySQL 5.7+와 PostgreSQL 9.5+에서 지원됩니다:

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가와 감소

쿼리 빌더는 컬럼 값을 간편하게 증가시키거나 감소시키는 메서드를 제공합니다. 두 메서드 모두 하나 이상의 인자를 받습니다: 컬럼명, 그리고 변경할 값(생략하면 1 증가/감소):

```
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

추가로 증가/감소 작업 중 업데이트할 컬럼들도 지정할 수 있습니다:

```
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

`incrementEach`와 `decrementEach`를 사용하면 여러 컬럼을 한꺼번에 증가 또는 감소시킬 수 있습니다:

```
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## 삭제문 (Delete Statements)

쿼리 빌더의 `delete` 메서드로 테이블의 레코드를 삭제할 수 있습니다. 영향받은 행 수를 반환하며, `where` 절과 함께 제한할 수 있습니다:

```
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

테이블의 모든 레코드를 삭제하고, 자동 증가 번호를 초기화하려면 `truncate` 메서드를 사용하세요:

```
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
#### 테이블 트렁케이션과 PostgreSQL

PostgreSQL에서 테이블을 트렁케이션 하면 `CASCADE` 동작이 적용되어, 외래 키로 연결된 다른 테이블의 관련 레코드도 함께 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문에 비관적 잠금을 적용하는 메서드를 제공합니다. "공유 잠금(shared lock)"을 실행하려면 `sharedLock`을 호출하세요. 공유 잠금은 트랜잭션 완료 전까지 선택한 행을 수정하지 못하도록 막습니다:

```
DB::table('users')
        ->where('votes', '>', 100)
        ->sharedLock()
        ->get();
```

또한 `lockForUpdate` 메서드는 "for update" 잠금을 수행합니다. 이는 선택한 행이 수정되거나 다른 공유 잠금으로 선택되는 것을 막습니다:

```
DB::table('users')
        ->where('votes', '>', 100)
        ->lockForUpdate()
        ->get();
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하는 도중에 `dd`와 `dump` 메서드를 사용해 현재 쿼리 바인딩과 SQL을 출력할 수 있습니다. `dd`는 디버그 정보 출력 후 요청 실행을 중단하고, `dump`는 계속 실행합니다:

```
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드는 바인딩이 모두 치환된 완전한 SQL을 출력합니다:

```
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```